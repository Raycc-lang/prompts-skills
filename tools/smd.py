# -*- coding: utf-8 -*-
"""smd.py — 单意识别（SMD）练习生成 CLI：单发（流式渲染）/ 批量 / 交互式。

固定使用 claude-sonnet-4-6（默认非思考模式；实测 thinking 提升有限
但延迟显著增加，如需对比加 --thinking）。三个入口共用同一引擎：
任务队列 + worker 线程，每个 worker 持独立客户端，完成即写 Markdown。

用法:
    # 单发：流式实时渲染 Markdown（装了 rich 时），--glow 结束后用 glow 显示
    python smd.py buy
    python smd.py --sentence "I don't buy that excuse." buy
    python smd.py "buy | I don't buy that excuse. | verb"
    python smd.py --glow "novel | Her novel approach..."

    # 批量：每行 "word | sentence | pos"（后两段可空），# 开头为注释行
    python smd.py -f batch.txt --concurrency 2

    # 交互式（无参数时默认进入）：输入即入队，后台处理，完成时通知
    #   命令:  ls  查看状态    q  退出（等待剩余任务完成后退出）
    python smd.py

公共参数:
    --out 输出文件夹   --config 客户端配置   --thinking 开思考模式
    --force 对已有输出的词重新生成（默认跳过，按输出文件名 *_{word}.md 判断）

依赖: rich（可选，pip install rich）——未安装时单发退化为纯文本流式。
"""

import argparse
import glob
import os
import queue
import re
import subprocess
import sys
import threading
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(SCRIPT_DIR, "claude-lite"))

from claude_lite import ClaudeLite

try:
    from rich.console import Console
    from rich.live import Live
    from rich.markdown import Markdown
    _HAS_RICH = True
except ImportError:
    _HAS_RICH = False

MODEL = "claude-sonnet-4-6"
PROMPT_PATH = os.path.join(
    ROOT, "prompts", "English-learning", "Single-Meaning Discrimination Protocol.md"
)
DEFAULT_OUT = os.path.join(ROOT, "smd-output")
DEFAULT_CONFIG = os.path.join(SCRIPT_DIR, "claude-lite", "claude_config.json")
RESET_RE = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2})")


def sanitize(word: str) -> str:
    s = "".join(c if c.isalnum() else "-" for c in word.strip().lower())
    return s.strip("-") or "word"


def parse_line(line: str) -> tuple:
    parts = [p.strip() for p in line.split("|")]
    word = parts[0]
    if not word:
        raise ValueError("word 为空")
    sentence = parts[1] if len(parts) > 1 else ""
    pos = parts[2] if len(parts) > 2 else ""
    return word, sentence, pos


def exists(out: str, word: str) -> bool:
    return bool(glob.glob(os.path.join(out, f"*_{sanitize(word)}.md")))


def build_message(word: str, sentence: str, pos: str) -> str:
    with open(PROMPT_PATH, encoding="utf-8") as f:
        protocol = f.read()
    lines = [f"WORD: {word}"]
    if sentence:
        lines.append(f'SOURCE SENTENCE: "{sentence}"')
    if pos:
        lines.append(f"PART OF SPEECH: {pos}")
    return protocol + "\n\n" + "\n".join(lines)


def save_result(out, word, sentence, pos, reply, latency, conv, mode) -> str:
    os.makedirs(out, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    path = os.path.join(out, f"{stamp}_{sanitize(word)}.md")
    meta = [
        f"# SMD: {word}",
        "",
        f"- 日期: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 模型: {MODEL} ({mode})",
        f"- 延迟: {latency}s",
        f"- 对话: {conv}",
    ]
    if sentence:
        meta.append(f"- 来源句: {sentence}")
    if pos:
        meta.append(f"- 词性: {pos}")
    meta += ["", "---", ""]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(meta) + reply + "\n")
    return path


def final_render(reply: str):
    if _HAS_RICH:
        Console().print(Markdown(reply))
    else:
        print(reply)


def run_single(word, sentence, pos, out, config, thinking, use_glow=False):
    mode = "thinking, effort=low" if thinking else "no-thinking"
    render = "rich 流式渲染" if _HAS_RICH else "纯文本流式"
    print(f"调用 {MODEL} ({mode})，{render}:", flush=True)

    client = ClaudeLite.from_config(config)
    t0 = time.time()

    if _HAS_RICH:
        console = Console()
        # Live 只显示视口内的部分（超出截断），结束后再完整渲染一遍
        live = Live(console=console, refresh_per_second=4,
                    vertical_overflow="ellipsis")
        buf = []

        def on_chunk(piece):
            buf.append(piece)
            live.update(Markdown("".join(buf)))

        with live:
            reply, conv = client.chat(
                build_message(word, sentence, pos), model=MODEL,
                thinking=thinking, effort="low" if thinking else "",
                on_chunk=on_chunk,
            )
    else:
        def on_chunk(piece):
            sys.stdout.write(piece)
            sys.stdout.flush()

        reply, conv = client.chat(
            build_message(word, sentence, pos), model=MODEL,
            thinking=thinking, effort="low" if thinking else "",
            on_chunk=on_chunk,
        )
        print()

    latency = round(time.time() - t0, 1)
    path = save_result(out, word, sentence, pos, reply, latency, conv, mode)
    if use_glow:
        try:
            subprocess.run(["glow", path], check=False)
        except FileNotFoundError:
            print("未找到 glow，改用内置渲染:", flush=True)
            final_render(reply)
    else:
        final_render(reply)
    print(f"已保存: {path}  ({latency}s, {len(reply)} 字符)", flush=True)


class Runner:
    """任务队列 + worker 线程池，交互式与批量模式共用。"""

    def __init__(self, concurrency, out, config, thinking, force):
        self.concurrency = max(1, min(concurrency, 4))
        self.out = out
        self.config = config
        self.thinking = thinking
        self.force = force
        self.mode = "thinking, effort=low" if thinking else "no-thinking"
        self.q = queue.Queue()
        self.lock = threading.Lock()
        self.stats = {"done": 0, "failed": 0, "skipped": 0}
        self.running = 0
        self.results = []
        self.workers = []

    def start(self):
        for _ in range(self.concurrency):
            client = ClaudeLite.from_config(self.config)
            t = threading.Thread(target=self._worker, args=(client,), daemon=True)
            t.start()
            self.workers.append(t)

    # -- worker ------------------------------------------------------------
    def _worker(self, client):
        while True:
            task = self.q.get()
            if task is None:
                self.q.task_done()
                break
            with self.lock:
                self.running += 1
            try:
                self._process(client, task)
            finally:
                with self.lock:
                    self.running -= 1
                self.q.task_done()

    def _process(self, client, task):
        word, sentence, pos = task
        if not self.force and exists(self.out, word):
            self._note(word, "skipped", "已有输出（--force 重跑）")
            print(f"[跳过] {word}: 已有输出", flush=True)
            return
        for attempt in (1, 2):
            try:
                t0 = time.time()
                reply, conv = client.chat(
                    build_message(word, sentence, pos), model=MODEL,
                    thinking=self.thinking,
                    effort="low" if self.thinking else "",
                )
                latency = round(time.time() - t0, 1)
                path = save_result(
                    self.out, word, sentence, pos,
                    reply, latency, conv, self.mode,
                )
                self._note(word, "done", f"{os.path.basename(path)} ({latency}s)")
                print(f"[完成] {word} -> {os.path.basename(path)} ({latency}s)",
                      flush=True)
                return
            except RuntimeError as e:
                msg = str(e)
                if "触发限流" in msg and attempt == 1:
                    wait = self._reset_wait(msg)
                    print(f"[限流] {word}: {msg}，休眠 {wait // 60} 分钟后重试",
                          flush=True)
                    time.sleep(wait)
                    continue
                self._note(word, "failed", msg[:120])
                print(f"[失败] {word}: {msg[:120]}", flush=True)
                return

    @staticmethod
    def _reset_wait(msg: str) -> float:
        m = RESET_RE.search(msg)
        if not m:
            return 600.0
        target = time.mktime(time.strptime(m.group(1), "%Y-%m-%d %H:%M"))
        return max(60.0, target - time.time() + 60)

    def _note(self, word, status, info):
        with self.lock:
            self.stats[status] += 1
            self.results.append((word, status, info))

    # -- 交互式 ------------------------------------------------------------
    def interactive(self):
        print(f"交互模式: {MODEL} ({self.mode})，并发 {self.concurrency}，"
              f"输出 -> {self.out}")
        print("  格式:  词 | 来源句 | 词性   （后两段可空）")
        print("  命令:  ls 查看状态    q 退出（等待剩余任务）\n")
        while True:
            try:
                raw = input("词 | 来源句 | 词性> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                raw = "q"
            if not raw:
                continue
            if raw in ("q", "quit", "exit"):
                self.shutdown()
                return
            if raw in ("ls", "status"):
                self.print_stats()
                continue
            try:
                word, sentence, pos = parse_line(raw)
            except ValueError:
                print("格式: 词 | 来源句 | 词性（第一段不能为空）")
                continue
            if not self.force and exists(self.out, word):
                self._note(word, "skipped", "已有输出（--force 重跑）")
                print(f"[跳过] {word}: 已有输出（--force 重跑）")
                continue
            self.q.put((word, sentence, pos))
            print(f"[入队] {word}（排队 {self.q.qsize()}）")

    def print_stats(self):
        with self.lock:
            done, failed, skipped = (
                self.stats["done"], self.stats["failed"], self.stats["skipped"])
            running = self.running
        print(f"状态: 运行中 {running} / 排队 {self.q.qsize()} / "
              f"完成 {done} / 失败 {failed} / 跳过 {skipped}")

    # -- 退出与汇总 ---------------------------------------------------------
    def shutdown(self):
        pending = self.q.qsize() + self.running
        if pending:
            print(f"等待 {pending} 个任务完成（Ctrl+C 放弃剩余）...", flush=True)
            try:
                self.q.join()
            except KeyboardInterrupt:
                print("\n已放弃剩余任务", flush=True)
                self.summary()
                return
        for _ in self.workers:
            self.q.put(None)
        for t in self.workers:
            t.join(timeout=5)
        self.summary()

    def summary(self):
        with self.lock:
            rows = list(self.results)
        if not rows:
            return
        s = self.stats
        print(f"\n===== 汇总: 完成 {s['done']} / 失败 {s['failed']} / "
              f"跳过 {s['skipped']} =====")
        marks = {"done": "+", "failed": "x", "skipped": "-"}
        for word, status, info in rows:
            print(f"  [{marks[status]}] {word}: {info}")

    # -- 批量 --------------------------------------------------------------
    def batch(self, path):
        if not os.path.isfile(path):
            sys.exit(f"批量文件不存在: {path}")
        tasks = []
        with open(path, encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    tasks.append(parse_line(line))
                except ValueError:
                    print(f"[忽略] 第 {i} 行格式错误: {line[:60]}")
        if not tasks:
            sys.exit("批量文件中没有有效任务")
        for t in tasks:
            self.q.put(t)
        print(f"已入队 {len(tasks)} 个任务（{MODEL} {self.mode}，"
              f"并发 {self.concurrency}）", flush=True)
        self.q.join()
        for _ in self.workers:
            self.q.put(None)
        for t in self.workers:
            t.join(timeout=5)
        self.summary()


def main():
    ap = argparse.ArgumentParser(
        description="单意识别（SMD）练习生成器：单发（流式）/ 批量 / 交互式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("input", nargs="?", default="",
                    help='单发: word，或 "word | sentence | pos" 一行式')
    ap.add_argument("-f", "--file", help="批量文件: 每行 word | sentence | pos")
    ap.add_argument("--sentence", default="", help="单发模式来源句（可选）")
    ap.add_argument("--pos", default="", help="单发模式词性（可选）")
    ap.add_argument("--out", default=DEFAULT_OUT, help="输出文件夹")
    ap.add_argument("--config", default=DEFAULT_CONFIG, help="客户端配置文件")
    ap.add_argument("--thinking", action="store_true",
                    help="开启思考模式（默认关闭，effort=low）")
    ap.add_argument("--concurrency", type=int, default=2,
                    help="worker 数量（默认 2，不建议超过 3）")
    ap.add_argument("--force", action="store_true",
                    help="对已有输出的词重新生成")
    ap.add_argument("--glow", action="store_true",
                    help="单发模式：结束后用 glow 显示保存的文件")
    args = ap.parse_args()

    if args.file:
        runner = Runner(args.concurrency, args.out, args.config,
                        args.thinking, args.force)
        runner.start()
        runner.batch(args.file)
    elif args.input:
        if "|" in args.input and not args.sentence:
            word, sentence, pos = parse_line(args.input)
        else:
            word = args.input.strip()
            sentence = args.sentence.strip()
            pos = args.pos.strip()
        if not word:
            ap.error("word 不能为空")
        run_single(word, sentence, pos, args.out, args.config,
                   args.thinking, use_glow=args.glow)
    else:
        runner = Runner(args.concurrency, args.out, args.config,
                        args.thinking, args.force)
        runner.start()
        runner.interactive()


if __name__ == "__main__":
    main()
