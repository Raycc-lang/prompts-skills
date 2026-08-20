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
import json
import os
import queue
import random
import re
import subprocess
import sys
import tempfile
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


def atomic_write_json(path, payload):
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(
        prefix=os.path.basename(path) + ".", suffix=".tmp", dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(temp_path, path)
    except Exception:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise


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
    stamp = time.strftime("%Y%m%d-%H%M%S") + f"-{time.time_ns() % 1_000_000_000:09d}"
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
    render = "Rich streaming" if _HAS_RICH else "plain-text streaming"
    print(f"Calling {MODEL} ({mode}) with {render}:", flush=True)

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
            print("glow was not found; using the built-in renderer:", flush=True)
            final_render(reply)
    else:
        final_render(reply)
    print(f"Saved: {path} ({latency}s, {len(reply)} characters)", flush=True)


class Runner:
    """任务队列 + worker 线程池，交互式与批量模式共用。"""

    def __init__(self, concurrency, out, config, thinking, force,
                 state_path=None):
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
        self.cooldown_until = 0.0
        self.rate_limit_attempts = 0
        self.retry_lock = threading.Lock()
        # 主动节流（方案 B）：在每个请求前强制间隔，避免突发触发 429。
        # 所有 worker 共享一个"上次请求时刻"，保证全局请求速率平缓。
        self.throttle_lock = threading.Lock()
        self.last_request_at = 0.0
        # 每个对外请求的最小间隔（秒）。并发 n 时，n 个 worker 会交错等待，
        # 实际总体速率被压到约 1/间隔 个请求/秒，从源头避开 claude.ai 限流。
        self.REQUEST_INTERVAL = 12.0
        # 跳过节流（交互式单发等低频场景不想等太久时可置 True）
        self.throttle_enabled = state_path is not None
        self.state_path = state_path
        self.task_states = {}
        self.started_at = time.strftime("%Y-%m-%dT%H:%M:%S")

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
        self._update_task(word, status="running")
        if not self.force and exists(self.out, word):
            info = "Output already exists (use --force to rerun)"
            self._note(word, "skipped", info)
            self._update_task(word, status="skipped", info=info)
            print(f"[SKIPPED] {word}: output already exists", flush=True)
            return
        attempt = 0
        while True:
            attempt += 1
            try:
                if attempt == 1:
                    self._wait_for_cooldown(word, attempt)
                    self._throttle(word)
                    t0 = time.time()
                    reply, conv = client.chat(
                        build_message(word, sentence, pos), model=MODEL,
                        thinking=self.thinking,
                        effort="low" if self.thinking else "",
                    )
                else:
                    # After a 429, allow only one worker to leave the shared
                    # cooldown and probe the service at a time.
                    with self.retry_lock:
                        self._wait_for_cooldown(word, attempt)
                        self._throttle(word)
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
                with self.lock:
                    self.rate_limit_attempts = 0
                info = f"{os.path.basename(path)} ({latency}s)"
                self._note(word, "done", info)
                self._update_task(word, status="done", info=info,
                                  attempt=attempt, next_retry_at=None)
                print(f"[DONE] {word} -> {os.path.basename(path)} ({latency}s)",
                      flush=True)
                return
            except RuntimeError as e:
                msg = str(e)
                if "HTTP 429" in msg:
                    wait, retry_at = self._set_cooldown(msg)
                    self._update_task(word, status="waiting", info=msg,
                                      attempt=attempt, next_retry_at=retry_at)
                    print(f"[RATE LIMITED] {word}: {msg}; attempt {attempt}; "
                          f"next retry at {retry_at} (in {wait / 60:.1f} minutes)",
                          flush=True)
                    continue
                self._note(word, "failed", msg[:120])
                self._update_task(word, status="failed", info=msg[:120],
                                  attempt=attempt)
                print(f"[FAILED] {word}: {msg[:120]}", flush=True)
                return
            except Exception as e:
                msg = f"{type(e).__name__}: {e}"
                self._note(word, "failed", msg[:120])
                self._update_task(word, status="failed", info=msg[:120],
                                  attempt=attempt)
                print(f"[FAILED] {word}: {msg[:120]}", flush=True)
                return

    def _throttle(self, label=""):
        """主动节流：保证相邻两个对外请求之间至少有 REQUEST_INTERVAL 秒。

        用锁让所有 worker 共享 last_request_at，实现"全局"匀速，
        从源头压平请求尖峰，尽量避免触发 claude.ai 的 429 限流。
        若服务端已处于限流 cooldown（slept 过），则跳过额外等待。
        """
        if not self.throttle_enabled:
            return 0.0
        with self.throttle_lock:
            now = time.time()
            wait = max(0.0, self.last_request_at + self.REQUEST_INTERVAL - now)
            if wait > 0:
                # 预约下一个请求时刻，并在释放锁后 sleep，避免锁占用太久
                self.last_request_at = now + self.REQUEST_INTERVAL
                coop = self.REQUEST_INTERVAL
            else:
                self.last_request_at = now
                coop = self.REQUEST_INTERVAL
        if wait > 0:
            tag = f" {label}" if label else ""
            print(f"[THROTTLE]{tag} waiting {wait:.1f}s", flush=True)
            time.sleep(wait)
        return wait

    def _wait_for_cooldown(self, word, attempt):
        with self.lock:
            remaining = self.cooldown_until - time.time()
            retry_at = time.strftime("%Y-%m-%d %H:%M:%S",
                                     time.localtime(self.cooldown_until))
        if remaining > 0:
            print(f"[WAITING] {word}: attempt {attempt}; shared cooldown until "
                  f"{retry_at} ({remaining / 60:.1f} minutes remaining)", flush=True)
            time.sleep(remaining)

    def _set_cooldown(self, msg):
        with self.lock:
            self.rate_limit_attempts += 1
            wait = self._reset_wait(msg, self.rate_limit_attempts)
            self.cooldown_until = max(self.cooldown_until, time.time() + wait)
            deadline = self.cooldown_until
        retry_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(deadline))
        return max(0.0, deadline - time.time()), retry_at

    @staticmethod
    def _reset_wait(msg: str, attempt: int = 1) -> float:
        m = RESET_RE.search(msg)
        if m:
            target = time.mktime(time.strptime(m.group(1), "%Y-%m-%d %H:%M"))
            base = max(60.0, target - time.time() + 60)
        else:
            base = min(3600.0, 600.0 * (2 ** min(max(attempt - 1, 0), 3)))
        return base + random.uniform(5.0, 30.0)

    def _note(self, word, status, info):
        with self.lock:
            self.stats[status] += 1
            self.results.append((word, status, info))

    def _update_task(self, word, **changes):
        if not self.state_path:
            return
        with self.lock:
            task = self.task_states.setdefault(word.casefold(), {"word": word})
            task.update(changes)
            self._write_state_locked("running")

    def _write_state_locked(self, status):
        if not self.state_path:
            return
        tasks = list(self.task_states.values())
        atomic_write_json(self.state_path, {
            "status": status,
            "pid": os.getpid() if status == "running" else None,
            "started_at": self.started_at,
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "total": len(tasks),
            "completed": sum(t.get("status") in ("done", "skipped") for t in tasks),
            "tasks": tasks,
        })

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
        print(f"\n===== Summary: done {s['done']} / failed {s['failed']} / "
              f"skipped {s['skipped']} =====")
        marks = {"done": "+", "failed": "x", "skipped": "-"}
        for word, status, info in rows:
            print(f"  [{marks[status]}] {word}: {info}")

    # -- 批量 --------------------------------------------------------------
    def batch(self, path):
        if not os.path.isfile(path):
            sys.exit(f"Batch file does not exist: {path}")
        tasks = []
        with open(path, encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    tasks.append(parse_line(line))
                except ValueError:
                    print(f"[IGNORED] Invalid format on line {i}: {line[:60]}")
        if not tasks:
            sys.exit("The batch file contains no valid tasks")
        with self.lock:
            self.task_states = {
                word.casefold(): {"word": word, "sentence": sentence, "pos": pos,
                                  "status": "pending", "attempt": 0}
                for word, sentence, pos in tasks
            }
            self._write_state_locked("running")
        for t in tasks:
            self.q.put(t)
        print(f"Queued {len(tasks)} tasks ({MODEL} {self.mode}, "
              f"concurrency {self.concurrency})", flush=True)
        self.q.join()
        for _ in self.workers:
            self.q.put(None)
        for t in self.workers:
            t.join(timeout=5)
        self.summary()
        succeeded = self.stats["failed"] == 0
        with self.lock:
            self._write_state_locked("done" if succeeded else "failed")
        return succeeded


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
    ap.add_argument("--concurrency", type=int, default=1,
                    help="worker 数量（默认 1，避免频繁触发 429 限流）")
    ap.add_argument("--force", action="store_true",
                    help="regenerate words that already have output")
    ap.add_argument("--state", help="JSON job-state file for batch progress")
    ap.add_argument("--glow", action="store_true",
                    help="单发模式：结束后用 glow 显示保存的文件")
    args = ap.parse_args()

    if args.file:
        runner = Runner(args.concurrency, args.out, args.config,
                        args.thinking, args.force, args.state)
        runner.start()
        if not runner.batch(args.file):
            raise SystemExit(1)
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
                        args.thinking, args.force, args.state)
        runner.start()
        runner.interactive()


if __name__ == "__main__":
    main()
