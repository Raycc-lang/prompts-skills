# -*- coding: utf-8 -*-
"""daily.py — 一条命令串起当天的英文阅读流程。

    python daily.py                    # 全流程: 备料(若有缺) -> 浏览器阅读工作流
    python daily.py url <网址>         # 先备料再走流程
    python daily.py pdf <文件> [--words N]
    python daily.py paste
    python daily.py --skip-prep        # 今天已有 article.txt,直接打开工作流
    python daily.py --only-read        # 直接打开今天的浏览器工作流

流程: prep(可选) -> pick 浏览器工作流（点选 -> 学词 -> 深度阅读）
提交选词后，SMD 在服务器后台运行，完成后页面自动显示学习内容。
"""

import argparse
import datetime
import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
READING_DIR = os.path.join(ROOT, "reading")


def run(cmd, **kw):
    print(f"\n>>> {' '.join(cmd)}\n", flush=True)
    return subprocess.run(cmd, **kw).returncode


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

    # ---- 备料
    if args.only_read:
        return run([sys.executable, os.path.join(SCRIPT_DIR, "pick.py")])

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

    # ---- 浏览器工作流：提交后在同一页面异步生成并进入学习/深读阶段
    pick_cmd = [sys.executable, os.path.join(SCRIPT_DIR, "pick.py")]
    if args.no_run:
        pick_cmd.append("--no-run")
    return run(pick_cmd)


if __name__ == "__main__":
    main()
