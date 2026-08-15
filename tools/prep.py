# -*- coding: utf-8 -*-
"""prep.py — 每日阅读备料工具。

三种来源，统一输出 reading/<日期>/article.txt：

    python prep.py url <网址>                          抓取网页正文
    python prep.py pdf <文件> [--words N] [--start-page N]  PDF 拆段，每天一小段
    python prep.py paste                               从剪贴板粘贴

PDF 按页记进度（state.json），同一本书自动续读下一段；已经读过
开头的书用 --start-page 指定起点（书的第几页，从 1 数）。
整书文本第一次提取后缓存在 reading/cache/，之后每天秒出。

PDF 进度存在 reading/state.json，同一本书自动续读下一段。
网页正文提取是轻量实现（去 nav/footer/script，取最长文本块），
对反爬/登录墙网站会失败——那种情况用 paste。
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
READING_DIR = os.path.join(ROOT, "reading")
STATE_PATH = os.path.join(READING_DIR, "state.json")

DEFAULT_WORDS = 2000


# ---------------------------------------------------------------- state

def load_state():
    if os.path.isfile(STATE_PATH):
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state):
    os.makedirs(READING_DIR, exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def today_dir():
    d = os.path.join(READING_DIR, datetime.date.today().isoformat())
    os.makedirs(d, exist_ok=True)
    return d


def write_article(text, source_desc):
    text = text.strip()
    if not text:
        sys.exit("内容为空，未写入")
    path = os.path.join(today_dir(), "article.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    wc = len(text.split())
    print(f"已写入: {path}")
    print(f"来源: {source_desc}，约 {wc} 词")
    return path


# ---------------------------------------------------------------- url

_SKIP_TAGS = {"script", "style", "nav", "header", "footer", "aside",
              "form", "iframe", "noscript", "button", "select", "svg"}


def extract_text_from_html(html):
    """轻量正文提取：跳过导航/脚本类标签，按块收集，返回全部可见文本。"""
    from html.parser import HTMLParser

    class P(HTMLParser):
        def __init__(self):
            super().__init__()
            self.depth_skip = 0
            self.blocks = []
            self.cur = []

        def handle_starttag(self, tag, attrs):
            if tag in _SKIP_TAGS:
                self.depth_skip += 1
            elif self.depth_skip == 0 and tag in (
                    "p", "div", "br", "li", "h1", "h2", "h3", "h4",
                    "blockquote", "pre", "tr"):
                self._flush()

        def handle_endtag(self, tag):
            if tag in _SKIP_TAGS and self.depth_skip > 0:
                self.depth_skip -= 1
            elif self.depth_skip == 0 and tag in (
                    "p", "li", "h1", "h2", "h3", "h4", "blockquote", "pre"):
                self._flush()

        def handle_data(self, data):
            if self.depth_skip == 0:
                self.cur.append(data)

        def _flush(self):
            line = " ".join("".join(self.cur).split())
            if line:
                self.blocks.append(line)
            self.cur = []

    p = P()
    p.feed(html)
    p._flush()
    # 去掉过短的碎片块（菜单残留等），保留有一定信息量的
    blocks = [b for b in p.blocks if len(b) >= 40 or len(b.split()) >= 8]
    if not blocks:  # 文章很短时放宽
        blocks = p.blocks
    return "\n\n".join(blocks)


def fetch_url(url):
    import requests
    print(f"抓取: {url}")
    try:
        r = requests.get(url, timeout=20, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/124.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        })
        r.raise_for_status()
    except Exception as e:
        sys.exit(f"抓取失败: {e}\n提示: 有反爬/登录墙的网站请改用 "
                 f"python prep.py paste 手动粘贴")
    r.encoding = r.apparent_encoding or r.encoding
    text = extract_text_from_html(r.text)
    if len(text.split()) < 50:
        sys.exit("提取到的正文过短，可能抓到了登录页/验证页。"
                 "请改用 python prep.py paste")
    return text


# ---------------------------------------------------------------- pdf

def find_pdftotext():
    """定位 pdftotext.exe：PATH -> state 缓存 -> where git -> 常见路径。"""
    p = shutil.which("pdftotext")
    if p:
        return p
    state = load_state()
    cached = state.get("pdftotext")
    if cached and os.path.isfile(cached):
        return cached
    candidates = []
    try:
        r = subprocess.run(["where.exe", "git"], capture_output=True,
                           text=True, timeout=10)
        for line in r.stdout.splitlines():
            line = line.strip()
            if line.lower().endswith("git.exe"):
                candidates.append(os.path.join(
                    os.path.dirname(os.path.dirname(line)),
                    "mingw64", "bin", "pdftotext.exe"))
    except Exception:
        pass
    for base in (os.environ.get("ProgramFiles", r"C:\Program Files"),
                 os.environ.get("ProgramFiles(x86)",
                                r"C:\Program Files (x86)"),
                 os.path.join(os.environ.get("LOCALAPPDATA", ""),
                              "Programs")):
        candidates.append(os.path.join(
            base, "Git", "mingw64", "bin", "pdftotext.exe"))
    for c in candidates:
        if c and os.path.isfile(c):
            state["pdftotext"] = c
            save_state(state)
            return c
    sys.exit("未找到 pdftotext。它通常随 Git for Windows 安装在 "
             "<Git>\\mingw64\\bin\\pdftotext.exe；如果装在别处，"
             "请把它所在目录加进 PATH，或手动在 "
             f"{STATE_PATH} 里写 \"pdftotext\": \"完整路径\"")


def pdf_cache_path(pdf_path):
    h = hashlib.md5(os.path.abspath(pdf_path).encode("utf-8")).hexdigest()[:12]
    cache_dir = os.path.join(READING_DIR, "cache")
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, f"{h}.txt")


def pdftotext_all(pdf_path):
    """整书提取（带缓存），返回按 \\x0c 分页的原始文本。"""
    cache = pdf_cache_path(pdf_path)
    if os.path.isfile(cache):
        with open(cache, encoding="utf-8", errors="replace") as f:
            return f.read()
    exe = find_pdftotext()
    print(f"首次提取整本书文本（pdftotext: {exe}）...", flush=True)
    try:
        subprocess.run([exe, "-enc", "UTF-8", pdf_path, cache],
                       check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        if os.path.isfile(cache):
            os.remove(cache)
        sys.exit(f"pdftotext 失败: {e.stderr.decode(errors='replace')[:200]}")
    with open(cache, encoding="utf-8", errors="replace") as f:
        return f.read()


def clean_page(text):
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    text = re.sub(r"(?<![.!?:;。！？])\n(?=[a-z(])", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def prep_pdf(pdf_path, words_per_day, start_page=None):
    if not os.path.isfile(pdf_path):
        sys.exit(f"文件不存在: {pdf_path}")
    key = os.path.abspath(pdf_path)
    state = load_state()
    pdf_state = state.setdefault("pdf", {})
    entry = pdf_state.get(key, {})

    raw = pdftotext_all(pdf_path)
    pages = raw.split("\x0c")
    # pdftotext 末尾常带一个空页
    while pages and not pages[-1].strip():
        pages.pop()
    total_pages = len(pages)
    if total_pages == 0:
        sys.exit("没提取到任何文本（可能是扫描版 PDF，没有文字层）")

    page = start_page if start_page else entry.get("page", 1)
    if page < 1:
        page = 1
    if page > total_pages:
        print(f"这本书已经读完了（共 {total_pages} 页）")
        ans = input("从头重读? [y/N] ").strip().lower()
        if ans != "y":
            return None
        page = 1

    # 用全书平均每页词数估算每天读几页（封面/目录页词少，不能拿当前页算）
    total_words = sum(len(p.split()) for p in pages)
    avg_words = max(1, total_words // total_pages)
    pages_per_day = max(1, round(words_per_day / avg_words))
    end_page = min(page + pages_per_day - 1, total_pages)

    chunk = "\n\n".join(clean_page(p) for p in pages[page - 1:end_page]
                        if p.strip())
    wc = len(chunk.split())

    print(f"进度: 第 {page}~{end_page} 页 / 共 {total_pages} 页 "
          f"({end_page / total_pages * 100:.0f}%)，本次约 {wc} 词")
    article_path = write_article(
        chunk, f"{os.path.basename(pdf_path)} 第{page}~{end_page}页")
    entry["page"] = end_page + 1
    entry["pages"] = total_pages
    pdf_state[key] = entry
    save_state(state)
    return article_path


# ---------------------------------------------------------------- paste

def read_clipboard():
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    try:
        return root.clipboard_get()
    except tk.TclError:
        sys.exit("剪贴板里没有文本")
    finally:
        root.destroy()


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(
        description="每日阅读备料：url / pdf / paste -> reading/<日期>/article.txt",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_url = sub.add_parser("url", help="抓取网页正文")
    p_url.add_argument("url")

    p_pdf = sub.add_parser("pdf", help="PDF 拆段（每天一小段，自动续读）")
    p_pdf.add_argument("pdf")
    p_pdf.add_argument("--words", type=int, default=DEFAULT_WORDS,
                       help=f"每段词数（默认 {DEFAULT_WORDS}，换算成整数页）")
    p_pdf.add_argument("--start-page", type=int, default=None,
                       help="从第几页开始（书的第几页，从 1 数）")

    sub.add_parser("paste", help="从剪贴板粘贴")

    args = ap.parse_args()

    if args.cmd == "url":
        write_article(fetch_url(args.url), args.url)
    elif args.cmd == "pdf":
        prep_pdf(args.pdf, args.words, args.start_page)
    elif args.cmd == "paste":
        text = read_clipboard()
        print(f"从剪贴板读到 {len(text)} 字符")
        write_article(text, "剪贴板粘贴")


if __name__ == "__main__":
    main()
