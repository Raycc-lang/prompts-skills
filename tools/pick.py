# -*- coding: utf-8 -*-
"""pick.py — 本地网页点选生词，提交后写 batch.txt 并自动跑 smd.py。

    python pick.py            # 用今天的 reading/<日期>/article.txt
    python pick.py -d 2026-08-14
    python pick.py --no-run   # 只写 batch.txt，不自动跑 smd.py
    python pick.py --port 8010

浏览器里：点词选中/取消，侧边栏管理已选，「生成 SMD」提交。
Ctrl+C 结束服务器。
"""

import argparse
import datetime
import html
import json
import os
import re
import socket
import subprocess
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
READING_DIR = os.path.join(ROOT, "reading")
SMD_PATH = os.path.join(SCRIPT_DIR, "smd.py")

WORD_RE = re.compile(r"[A-Za-z][a-zA-Z'-]*[a-zA-Z]|[A-Za-z]")
SENT_END = (".", "!", "?", "。", "!", "?")


# ------------------------------------------------------- article loading

def resolve_day_dir(day=None):
    if day:
        d = os.path.join(READING_DIR, day)
        if not os.path.isdir(d):
            sys.exit(f"目录不存在: {d}")
        return d
    today = os.path.join(READING_DIR, datetime.date.today().isoformat())
    if os.path.isfile(os.path.join(today, "article.txt")):
        return today
    # 回退到最近一个有 article.txt 的日期
    if os.path.isdir(READING_DIR):
        for name in sorted(os.listdir(READING_DIR), reverse=True):
            p = os.path.join(READING_DIR, name, "article.txt")
            if os.path.isfile(p):
                print(f"今天没有 article.txt，使用最近的: {name}")
                return os.path.join(READING_DIR, name)
    sys.exit("没有找到 article.txt。先跑 python tools/prep.py 备料")


def source_sentence(text, start, end):
    s = start
    while s > 0 and text[s - 1] not in SENT_END and text[s - 1] != "\n":
        s -= 1
    e = end
    n = len(text)
    while e < n and text[e] not in SENT_END and text[e] != "\n":
        e += 1
    if e < n and text[e] in SENT_END:
        e += 1
    return " ".join(text[s:e].split())


# ------------------------------------------------------- page rendering

PAGE_CSS = """
:root { color-scheme: light dark; }
* { box-sizing: border-box; }
body { margin:0; font-family: Georgia,'Times New Roman',serif;
       background:#fff; color:#1a1a1a; }
@media (prefers-color-scheme: dark) {
  body { background:#17181c; color:#e2e2e6; }
  #sidebar { background:#1e2026; border-color:#333; }
  .sel-item { background:#26282f; }
  .sel-item button { color:#999; }
  input[type=text] { background:#26282f; color:#e2e2e6; border-color:#444; }
}
.layout { display:flex; min-height:100vh; }
#article { flex:1; padding:32px 28px 120px; max-width:760px;
           font-size:19px; line-height:1.85; }
#article p { margin:0 0 1.2em; }
.w { cursor:pointer; border-radius:3px; padding:0 1px; transition:background .12s; }
.w:hover { background:rgba(59,130,246,.25); }
.w.sel { background:#ffd54a; color:#111; }
@media (prefers-color-scheme: dark) { .w.sel { background:#b58900; color:#fff; } }
.w.dup { text-decoration:underline dotted; }
#sidebar { width:300px; flex-shrink:0; padding:20px 16px; border-left:1px solid #ddd;
           position:sticky; top:0; height:100vh; overflow-y:auto;
           font-family:ui-sans-serif,system-ui,sans-serif; }
#sidebar h2 { font-size:15px; margin:0 0 12px; }
#count { font-weight:700; }
.sel-item { border-radius:8px; padding:8px 10px; margin-bottom:8px; font-size:13px; }
.sel-item .word { font-weight:700; font-size:15px; display:flex;
                  justify-content:space-between; align-items:center; }
.sel-item .word button { border:0; background:none; cursor:pointer;
                         font-size:14px; padding:0 2px; }
.sel-item .sent { color:#888; margin-top:4px; line-height:1.4;
                  max-height:3.9em; overflow:hidden; }
.sel-item select { margin-top:6px; font-size:12px; }
#actions { position:sticky; bottom:0; padding-top:12px; background:inherit; }
#submit { width:100%; padding:12px; font-size:15px; font-weight:700;
          border:0; border-radius:8px; background:#2563eb; color:#fff;
          cursor:pointer; }
#submit:hover { background:#1d4ed8; }
#addrow { display:flex; gap:6px; margin:10px 0; }
#addrow input { flex:1; padding:8px; border:1px solid #ccc; border-radius:6px;
                font-size:13px; }
#addrow button { padding:8px 12px; border:0; border-radius:6px;
                 background:#e5e7eb; cursor:pointer; }
#toast { position:fixed; left:50%; bottom:26px; transform:translateX(-50%);
         background:#111; color:#fff; padding:10px 18px; border-radius:8px;
         font-size:14px; opacity:0; transition:opacity .2s; pointer-events:none; }
#toast.show { opacity:.92; }
#done-overlay { display:none; position:fixed; inset:0; background:rgba(0,0,0,.55);
                align-items:center; justify-content:center; z-index:10; }
#done-overlay .card { background:#fff; color:#111; border-radius:12px;
                      padding:28px 32px; max-width:420px;
                      font-family:ui-sans-serif,system-ui,sans-serif; }
#done-overlay pre { background:#f1f1f1; padding:10px; border-radius:6px;
                    font-size:12px; max-height:220px; overflow:auto;
                    white-space:pre-wrap; }
"""

PAGE_JS = """
const sel = new Map();  // lower word -> {display, sentence, count}

function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 1600);
}

function spansFor(lower) {
  return document.querySelectorAll('.w[data-lower="' + CSS.escape(lower) + '"]');
}

function toggleWord(el) {
  const lower = el.dataset.lower;
  if (sel.has(lower)) {
    sel.delete(lower);
    spansFor(lower).forEach(s => s.classList.remove('sel', 'dup'));
  } else {
    const spans = spansFor(lower);
    sel.set(lower, {display: el.dataset.word, sentence: el.dataset.sent,
                    count: spans.length});
    spans.forEach((s, i) => s.classList.add('sel'));
    if (spans.length > 1) spans.forEach(s => s.classList.add('dup'));
  }
  renderSidebar();
}

function renderSidebar() {
  const list = document.getElementById('sel-list');
  list.innerHTML = '';
  for (const [lower, info] of sel) {
    const div = document.createElement('div');
    div.className = 'sel-item';
    div.innerHTML =
      '<div class="word"><span>' + esc(info.display) +
      (info.count > 1 ? ' <small>x' + info.count + '</small>' : '') +
      '</span><button title="移除">\\u00d7</button></div>' +
      '<div class="sent">' + esc(info.sentence) + '</div>';
    div.querySelector('button').onclick = () => {
      sel.delete(lower);
      spansFor(lower).forEach(s => s.classList.remove('sel', 'dup'));
      renderSidebar();
    };
    list.appendChild(div);
  }
  document.getElementById('count').textContent = sel.size;
}

function esc(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

document.querySelectorAll('.w').forEach(el => {
  el.addEventListener('click', () => toggleWord(el));
});

document.getElementById('add-btn').onclick = () => {
  const inp = document.getElementById('add-input');
  const w = inp.value.trim();
  if (!w) return;
  const lower = w.toLowerCase();
  if (!sel.has(lower)) {
    sel.set(lower, {display: w, sentence: '', count: 0});
    renderSidebar();
  }
  inp.value = '';
  toast('已添加: ' + w);
};
document.getElementById('add-input').addEventListener('keydown', e => {
  if (e.key === 'Enter') document.getElementById('add-btn').click();
});

document.getElementById('submit').onclick = async () => {
  if (sel.size === 0) { toast('还没选词'); return; }
  const btn = document.getElementById('submit');
  btn.disabled = true; btn.textContent = '提交中...';
  const items = [...sel.values()].map(i => ({word: i.display, sentence: i.sentence}));
  try {
    const r = await fetch('/submit', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({items: items})
    });
    const data = await r.json();
    document.getElementById('done-text').textContent = data.message;
    document.getElementById('done-detail').textContent = data.detail || '';
    document.getElementById('done-overlay').style.display = 'flex';
    btn.textContent = '已提交';
  } catch (e) {
    btn.disabled = false; btn.textContent = '生成 SMD ▸';
    toast('提交失败: ' + e);
  }
};

document.getElementById('close-overlay').onclick = () => {
  document.getElementById('done-overlay').style.display = 'none';
};
"""


def render_page(text, run_smd):
    parts = []
    pos = 0
    for m in WORD_RE.finditer(text):
        parts.append(html.escape(text[pos:m.start()]))
        word = m.group(0)
        sent = source_sentence(text, m.start(), m.end())
        parts.append(
            f'<span class="w" data-word="{html.escape(word, quote=True)}" '
            f'data-lower="{html.escape(word.lower(), quote=True)}" '
            f'data-sent="{html.escape(sent, quote=True)}">'
            f'{html.escape(word)}</span>')
        pos = m.end()
    parts.append(html.escape(text[pos:]))

    # 把换行转换成段落
    body = "".join(parts)
    paras = "".join(
        f"<p>{p.replace(chr(10), '<br>')}</p>"
        for p in body.split("\n\n") if p.strip())

    run_label = "生成 SMD ▸" if run_smd else "写出 batch.txt ▸"
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>选词 — {datetime.date.today().isoformat()}</title>
<style>{PAGE_CSS}</style></head>
<body>
<div class="layout">
  <div id="article">{paras}</div>
  <div id="sidebar">
    <h2>已选 <span id="count">0</span> 词</h2>
    <div id="addrow">
      <input type="text" id="add-input" placeholder="手动添加词/短语">
      <button id="add-btn" type="button">添加</button>
    </div>
    <div id="sel-list"></div>
    <div id="actions">
      <button id="submit" type="button">{run_label}</button>
    </div>
  </div>
</div>
<div id="toast"></div>
<div id="done-overlay"><div class="card">
  <h3 id="done-text"></h3>
  <pre id="done-detail"></pre>
  <button id="close-overlay" type="button">关闭</button>
</div></div>
<script>{PAGE_JS}</script>
</body></html>"""


# ------------------------------------------------------- server

class PickServer:
    def __init__(self, page_html, day_dir, run_smd, concurrency):
        self.page_html = page_html
        self.day_dir = day_dir
        self.run_smd = run_smd
        self.concurrency = concurrency

    def handler(self):
        outer = self

        class H(BaseHTTPRequestHandler):
            def log_message(self, fmt, *args):
                pass

            def _send(self, code, body, ctype="text/html; charset=utf-8"):
                data = body.encode("utf-8")
                self.send_response(code)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self):
                if self.path in ("/", "/index.html"):
                    self._send(200, outer.page_html)
                else:
                    self._send(404, "not found", "text/plain")

            def do_POST(self):
                if self.path != "/submit":
                    self._send(404, "not found", "text/plain")
                    return
                length = int(self.headers.get("Content-Length", 0))
                try:
                    payload = json.loads(self.rfile.read(length) or b"{}")
                    items = payload.get("items", [])
                except Exception as e:
                    self._send(400, json.dumps(
                        {"message": f"解析请求失败: {e}"}),
                        "application/json; charset=utf-8")
                    return
                msg, detail = outer.submit(items)
                self._send(200, json.dumps(
                    {"message": msg, "detail": detail}, ensure_ascii=False),
                    "application/json; charset=utf-8")

        return H

    def submit(self, items):
        batch_path = os.path.join(self.day_dir, "batch.txt")
        lines = [f"# 选词 {datetime.datetime.now():%Y-%m-%d %H:%M}"]
        for it in items:
            word = (it.get("word") or "").strip()
            if not word:
                continue
            sent = (it.get("sentence") or "").strip()
            lines.append(f"{word} | {sent} | ")
        with open(batch_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        n = len(lines) - 1
        print(f"已写入 {batch_path}（{n} 词）", flush=True)

        if not self.run_smd:
            return f"已写出 {n} 词", batch_path

        smd_out = os.path.join(self.day_dir, "smd")
        cmd = [sys.executable, SMD_PATH, "-f", batch_path,
               "--out", smd_out, "--concurrency", str(self.concurrency)]
        try:
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace")
        except Exception as e:
            return f"batch.txt 已写出，但启动 smd.py 失败: {e}", batch_path

        def drain():
            for line in proc.stdout:
                print("[smd] " + line.rstrip(), flush=True)
            proc.wait()
            print(f"[smd] 结束，返回码 {proc.returncode}，输出 -> {smd_out}",
                  flush=True)

        threading.Thread(target=drain, daemon=True).start()
        return (f"已写出 {n} 词，smd.py 后台运行中（输出 -> {smd_out}）",
                "进度见终端；完成后可运行 python tools/read.py 开始阅读")


# ------------------------------------------------------- main

def free_port(preferred):
    s = socket.socket()
    try:
        s.bind(("127.0.0.1", preferred))
        return preferred
    except OSError:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]
    finally:
        s.close()


def main():
    ap = argparse.ArgumentParser(description="网页点选生词 -> batch.txt -> smd.py")
    ap.add_argument("-d", "--day", help="日期目录（默认今天，缺了回退最近）")
    ap.add_argument("--port", type=int, default=8009)
    ap.add_argument("--no-run", action="store_true",
                    help="只写 batch.txt，不自动跑 smd.py")
    ap.add_argument("--concurrency", type=int, default=2, help="smd 并发")
    ap.add_argument("--no-browser", action="store_true", help="不自动开浏览器")
    args = ap.parse_args()

    day_dir = resolve_day_dir(args.day)
    article_path = os.path.join(day_dir, "article.txt")
    with open(article_path, encoding="utf-8") as f:
        text = f.read()
    print(f"文章: {article_path}（约 {len(text.split())} 词）")

    run_smd = not args.no_run
    page = render_page(text, run_smd)
    srv = PickServer(page, day_dir, run_smd, args.concurrency)

    port = free_port(args.port)
    httpd = ThreadingHTTPServer(("127.0.0.1", port), srv.handler())
    url = f"http://127.0.0.1:{port}/"
    print(f"选词页面: {url}")
    print("提交后 " + ("自动跑 smd.py；" if run_smd else "只写 batch.txt；")
          + "Ctrl+C 结束")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")


if __name__ == "__main__":
    main()
