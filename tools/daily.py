# -*- coding: utf-8 -*-
"""daily.py — 一条命令串起当天的英文阅读流程。

    python daily.py                    # 全流程: 备料(若有缺) -> 浏览器阅读工作流
    python daily.py url <网址>         # 先备料再走流程
    python daily.py pdf <文件> [--words N]
    python daily.py paste
    python daily.py --skip-prep        # 今天已有 article.txt,直接打开工作流
    python daily.py --only-read        # 直接打开今天的浏览器工作流

流程: prep(可选) -> reading 浏览器工作流（点选 -> 学词 -> 深度阅读）
提交选词后，SMD 在服务器后台运行，完成后页面自动显示学习内容。
"""

import argparse
import datetime
import json
import os
import socket
import subprocess
import sys
import urllib.parse
import urllib.request
import webbrowser

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
READING_DIR = os.path.join(ROOT, "reading")


def run(cmd, **kw):
    print(f"\n>>> {' '.join(cmd)}\n", flush=True)
    return subprocess.run(cmd, **kw).returncode


def reload_service(day_dir):
    day = os.path.basename(day_dir)
    query = urllib.parse.urlencode({"day": day})
    try:
        with urllib.request.urlopen(
                f"http://127.0.0.1:8009/reload?{query}", timeout=5) as response:
            payload = json.loads(response.read())
            return response.status == 200 and payload.get("day") == day
    except Exception as exc:
        print(f"刷新失败: {exc}", flush=True)
        return False


def main():
    ap = argparse.ArgumentParser(
        description="当天阅读流程一条龙",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", nargs="?", choices=["url", "pdf", "paste"],
                    help="备料方式（不带则检查今天是否已有 article.txt）")
    ap.add_argument("src", nargs="?", help="网址或 PDF 路径")
    ap.add_argument("--words", type=int, default=2000, help="PDF 每段词数")
    ap.add_argument("--start-page", type=int, default=None,
                    help="PDF 从第几页开始（会记住并续读）")
    ap.add_argument("--skip-prep", action="store_true", help="跳过备料")
    ap.add_argument("--only-read", action="store_true", help="只打开浏览器工作流")
    ap.add_argument("--no-run", action="store_true",
                    help="点选提交后不自动跑 smd.py")
    args = ap.parse_args()

    today_dir = os.path.join(READING_DIR, datetime.date.today().isoformat())
    article = os.path.join(today_dir, "article.txt")

    # ---- 备料前先检查端口，复用已有服务
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    service_running = sock.connect_ex(("127.0.0.1", 8009)) == 0
    sock.close()

    if args.only_read:
        if service_running:
            print(f"检测到已有服务在 127.0.0.1:8009，直接打开浏览器", flush=True)
            webbrowser.open("http://127.0.0.1:8009/")
            return 0
        return run([sys.executable, os.path.join(SCRIPT_DIR, "reading.py")])

    if args.cmd:
        prep_cmd = [sys.executable, os.path.join(SCRIPT_DIR, "prep.py"),
                    args.cmd]
        if args.cmd in ("url", "pdf"):
            if not args.src:
                sys.exit(f"{args.cmd} 需要提供来源")
            prep_cmd.append(args.src)
            if args.cmd == "pdf":
                prep_cmd += ["--words", str(args.words)]
                if args.start_page:
                    prep_cmd += ["--start-page", str(args.start_page)]
        if run(prep_cmd) != 0:
            sys.exit("备料失败")
    elif not (args.skip_prep or os.path.isfile(article)):
        sys.exit("今天还没有 article.txt。用法:\n"
                 "  python daily.py url <网址>\n"
                 "  python daily.py pdf <文件>\n"
                 "  python daily.py paste\n"
                 "  python daily.py --skip-prep   (已有 article.txt 时)")

    # ---- 浏览器工作流（备料可能耗时较长，重新检查端口）
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    service_running = sock.connect_ex(("127.0.0.1", 8009)) == 0
    sock.close()
    if service_running:
        # 刷新服务内容，让 reading 重新读取 article.txt
        print("检测到已有服务，发送 /reload 刷新内容...", flush=True)
        if reload_service(today_dir):
            print("服务已刷新，新内容已加载", flush=True)
            webbrowser.open("http://127.0.0.1:8009/")
            return 0
        print("已有端口未能加载今天的阅读内容", flush=True)
        return 1

    read_cmd = [sys.executable, os.path.join(SCRIPT_DIR, "reading.py")]
    if args.no_run:
        read_cmd.append("--no-run")
    return run(read_cmd)


if __name__ == "__main__":
    main()
