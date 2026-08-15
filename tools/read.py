# -*- coding: utf-8 -*-
"""read.py — 全屏终端阅读器，专心读 smd 输出。

    python read.py              # 读今天的（reading/<今天>/smd）
    python read.py -d 2026-08-14
    python read.py --path smd-output   # 读任意文件夹

按键:  n / → / 空格  下一个    p / ←  上一个    q  退出
"""

import argparse
import datetime
import glob
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
READING_DIR = os.path.join(ROOT, "reading")

# Windows GBK 控制台遇到 smd 输出里的 • 等字符会崩，强制 UTF-8
if os.name == "nt":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")

try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
except ImportError:
    sys.exit("需要 rich: python -m pip install rich")


def resolve_dir(args):
    if args.path:
        d = os.path.abspath(args.path)
        if not os.path.isdir(d):
            sys.exit(f"目录不存在: {d}")
        return d
    day = args.day or datetime.date.today().isoformat()
    d = os.path.join(READING_DIR, day, "smd")
    if os.path.isdir(d):
        return d
    if not args.day:
        # 回退到最近有 smd 输出的日期
        if os.path.isdir(READING_DIR):
            for name in sorted(os.listdir(READING_DIR), reverse=True):
                p = os.path.join(READING_DIR, name, "smd")
                if os.path.isdir(p) and glob.glob(os.path.join(p, "*.md")):
                    print(f"今天没有 smd 输出，读最近的: {name}")
                    return p
        # 再回退到全局 smd-output
        fallback = os.path.join(ROOT, "smd-output")
        if os.path.isdir(fallback):
            print(f"reading 下没有 smd 输出，读全局: {fallback}")
            return fallback
    sys.exit(f"没有找到 smd 输出: {d}")


def get_key():
    """跨平台单键读取，返回 'n'/'p'/'q' 等小写字符或方向键名。"""
    if os.name == "nt":
        import msvcrt
        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):  # 特殊键
            ch2 = msvcrt.getwch()
            return {"K": "left", "M": "right"}.get(ch2, "")
        if ch == "\r":
            return "n"
        return ch.lower()
    import termios
    import tty
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            ch2 = sys.stdin.read(2)
            return {"[D": "left", "[C": "right"}.get(ch2, "")
        if ch == "\r":
            return "n"
        return ch.lower()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def main():
    ap = argparse.ArgumentParser(description="全屏阅读 smd 输出")
    ap.add_argument("-d", "--day", help="日期（默认今天，缺了回退最近）")
    ap.add_argument("--path", help="直接指定 md 文件夹")
    args = ap.parse_args()

    d = resolve_dir(args)
    files = sorted(glob.glob(os.path.join(d, "*.md")))
    if not files:
        sys.exit(f"{d} 下没有 .md 文件")

    console = Console()
    idx = 0
    with console.screen():
        while True:
            path = files[idx]
            with open(path, encoding="utf-8") as f:
                content = f.read()
            word = os.path.splitext(os.path.basename(path))[0]
            console.clear()
            console.print(Panel(
                Markdown(content),
                title=f"[{idx + 1}/{len(files)}] {word}",
                subtitle="n/→ 下一个  p/← 上一个  q 退出",
                border_style="blue",
                padding=(0, 2),
            ))
            k = get_key()
            if k in ("q", "\x03", "\x1b"):
                break
            if k in ("n", "right", " ", "j"):
                idx = min(idx + 1, len(files) - 1)
            elif k in ("p", "left", "k"):
                idx = max(idx - 1, 0)
    print(f"读了 {len(files)} 篇中的 {idx + 1} 篇（{d}）")


if __name__ == "__main__":
    main()
