# -*- coding: utf-8 -*-
"""chatgpt_lite.py — 轻量 ChatGPT 网页版客户端。

复用 chatgpt2api 的反爬模块（PoW / Turnstile），去掉 Web 服务器、
数据库、账号池等所有多余功能。单文件，直接跑。

用法（命令行）:
    python chatgpt_lite.py "你好"
    python chatgpt_lite.py --thinking "帮我解这道题"
    python chatgpt_lite.py --file prompt.txt --output result.txt
    python chatgpt_lite.py --model gpt-5-6-mini "消息"

用法（模块）:
    from chatgpt_lite import ChatGPTLite
    client = ChatGPTLite.from_tokens("chatgpt_tokens.json")
    reply = client.chat([{"role": "user", "content": "你好"}])

依赖: 需要 chatgpt2api 的 Python 环境（curl_cffi, pybase64 等）。
推荐用 uv run 从 chatgpt2api 目录执行:
    cd C:\\Users\\Ray\\Documents\\Projects\\chatgpt2api
    uv run python <本脚本路径> "你好"
"""

import argparse
import json
import os
import sys
import time
import uuid
from pathlib import Path

# ---------------------------------------------------------------------------
# 把 chatgpt2api 加入 sys.path 以复用其反爬工具模块。优先使用显式配置，
# 否则尝试仓库旁边的同名 checkout，不依赖作者机器上的绝对路径。
# ---------------------------------------------------------------------------
_configured_c2a = os.environ.get("CHATGPT2API_DIR", "").strip()
_candidate_c2a = [Path(_configured_c2a)] if _configured_c2a else []
_candidate_c2a.append(Path(__file__).resolve().parents[2].parent / "chatgpt2api")
for _path in _candidate_c2a:
    if (_path / "utils").is_dir() and str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

try:
    from curl_cffi import requests as cffi_requests          # noqa: E402
    from utils.pow import (                                  # noqa: E402
        build_legacy_requirements_token,
        build_proof_token,
        parse_pow_resources,
    )
    from utils.turnstile import solve_turnstile_token        # noqa: E402
    from utils.helper import iter_sse_payloads, new_uuid     # noqa: E402
except ModuleNotFoundError as exc:
    raise ImportError(
        "chatgpt-lite requires the chatgpt2api checkout and its dependencies. "
        "Set CHATGPT2API_DIR to that checkout, or place it beside this repository."
    ) from exc

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------
BASE_URL = "https://chatgpt.com"
OAUTH_TOKEN_URL = "https://auth.openai.com/oauth/token"
OAUTH_CLIENT_ID = "app_2SKx67EdpoN0G6j64rFvigXD"
DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TOKEN_FILE = os.path.join(SCRIPT_DIR, "chatgpt_tokens.json")


# ---------------------------------------------------------------------------
# Token 管理
# ---------------------------------------------------------------------------
def load_tokens(path: str = DEFAULT_TOKEN_FILE) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_tokens(tokens: dict, path: str = DEFAULT_TOKEN_FILE) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=2, ensure_ascii=False)


def refresh_access_token(tokens: dict, path: str = DEFAULT_TOKEN_FILE) -> dict:
    """用 refresh_token 换取新的 access_token。"""
    import urllib.parse
    import urllib.request

    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": tokens["refresh_token"],
        "client_id": OAUTH_CLIENT_ID,
    }).encode()
    req = urllib.request.Request(
        OAUTH_TOKEN_URL,
        data=data,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": DEFAULT_UA,
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        resp = json.loads(r.read())
    tokens["access_token"] = resp["access_token"]
    if resp.get("refresh_token"):
        tokens["refresh_token"] = resp["refresh_token"]
    save_tokens(tokens, path)
    return tokens


# ---------------------------------------------------------------------------
# 核心客户端
# ---------------------------------------------------------------------------
def _detect_system_proxy() -> str:
    """尝试检测系统代理。"""
    try:
        import urllib.request
        proxy_handler = urllib.request.getproxies()
        for scheme in ("https", "http"):
            if scheme in proxy_handler:
                return proxy_handler[scheme]
    except Exception:
        pass
    return ""


class ChatGPTLite:
    """极简 ChatGPT 网页版对话客户端。"""

    def __init__(self, access_token: str, proxy: str = ""):
        self.access_token = access_token
        self.device_id = str(uuid.uuid4())
        self.session_id = str(uuid.uuid4())
        self.user_agent = DEFAULT_UA
        self.pow_script_sources: list[str] = []
        self.pow_data_build = ""

        if not proxy:
            proxy = _detect_system_proxy()
        session_kwargs: dict = {"impersonate": "chrome110"}
        if proxy:
            session_kwargs["proxies"] = {"http": proxy, "https": proxy}
        self.session = cffi_requests.Session(**session_kwargs)
        self.session.headers.update({
            "User-Agent": self.user_agent,
            "Origin": BASE_URL,
            "Referer": BASE_URL + "/",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "OAI-Device-Id": self.device_id,
            "OAI-Session-Id": self.session_id,
            "OAI-Language": "zh-CN",
            "OAI-Client-Version": "prod-a194cd50d4416d3c0b47c740f206b12ce60f5887",
            "OAI-Client-Build-Number": "6708908",
            "Sec-Ch-Ua": '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
        })

    # -- 工厂方法 ----------------------------------------------------------
    @classmethod
    def from_tokens(cls, path: str = DEFAULT_TOKEN_FILE, proxy: str = "") -> "ChatGPTLite":
        tokens = load_tokens(path)
        return cls(tokens["access_token"], proxy=proxy)

    # -- 内部工具 ----------------------------------------------------------
    def _headers(self, path: str, extra: dict | None = None) -> dict:
        h = {
            "Authorization": f"Bearer {self.access_token}",
            "X-OpenAI-Target-Path": path,
            "X-OpenAI-Target-Route": path,
        }
        if extra:
            h.update(extra)
        return h

    def _bootstrap(self) -> None:
        """访问首页，抓取 PoW 脚本列表和 data-build。"""
        resp = self.session.get(
            BASE_URL + "/",
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
            },
            timeout=30,
        )
        self.pow_script_sources, self.pow_data_build = parse_pow_resources(resp.text)
        if not self.pow_script_sources:
            self.pow_script_sources = ["https://chatgpt.com/backend-api/sentinel/sdk.js"]

    def _get_chat_requirements(self) -> dict:
        """prepare + finalize 两步获取 sentinel token。"""
        base = "/backend-api/sentinel/chat-requirements"
        p_token = build_legacy_requirements_token(
            self.user_agent, self.pow_script_sources, self.pow_data_build,
        )

        # prepare
        prepare_path = base + "/prepare"
        resp = self.session.post(
            BASE_URL + prepare_path,
            headers=self._headers(prepare_path, {"Content-Type": "application/json"}),
            json={"p": p_token},
            timeout=30,
        )
        if resp.status_code != 200:
            raise RuntimeError(f"chat-requirements prepare failed: {resp.status_code}")
        prepare_data = resp.json()

        if (prepare_data.get("arkose") or {}).get("required"):
            raise RuntimeError("arkose token required but not implemented")

        # PoW
        proof_token = ""
        pow_info = prepare_data.get("proofofwork") or {}
        if pow_info.get("required"):
            proof_token = build_proof_token(
                pow_info.get("seed", ""),
                pow_info.get("difficulty", ""),
                self.user_agent,
                script_sources=self.pow_script_sources,
                data_build=self.pow_data_build,
            )

        # Turnstile
        turnstile_token = ""
        ts_info = prepare_data.get("turnstile") or {}
        if ts_info.get("required") and ts_info.get("dx"):
            turnstile_token = solve_turnstile_token(ts_info["dx"], p_token) or ""

        # finalize
        finalize_path = base + "/finalize"
        resp = self.session.post(
            BASE_URL + finalize_path,
            headers=self._headers(finalize_path, {"Content-Type": "application/json"}),
            json={
                "prepare_token": prepare_data.get("prepare_token", ""),
                "proof_token": proof_token,
                "turnstile_token": turnstile_token,
            },
            timeout=30,
        )
        if resp.status_code != 200:
            raise RuntimeError(f"chat-requirements finalize failed: {resp.status_code}")
        data = resp.json()
        token = data.get("token", "")
        if not token:
            raise RuntimeError(f"missing chat requirements token: {data}")

        return {
            "token": token,
            "proof_token": proof_token,
            "turnstile_token": turnstile_token,
            "so_token": data.get("so_token", ""),
        }

    # -- 对话 --------------------------------------------------------------
    def chat(
        self,
        messages: list[dict],
        model: str = "auto",
        thinking_effort: str = "",
    ) -> str:
        """发送 messages，返回助手回复文本。

        messages 格式: [{"role": "user", "content": "..."}, ...]
        thinking_effort: "" | "extended"（免费账号仅支持 extended）
        """
        self._bootstrap()
        requirements = self._get_chat_requirements()

        # 转换 messages → ChatGPT 网页格式
        conv_messages = []
        for msg in messages:
            conv_messages.append({
                "id": new_uuid(),
                "author": {"role": msg.get("role", "user")},
                "content": {
                    "content_type": "text",
                    "parts": [msg.get("content", "")],
                },
            })

        payload = {
            "action": "next",
            "messages": conv_messages,
            "model": model,
            "parent_message_id": new_uuid(),
            "conversation_mode": {"kind": "primary_assistant"},
            "conversation_origin": None,
            "force_use_sse": True,
            "history_and_training_disabled": True,
            "timezone": "Asia/Shanghai",
            "timezone_offset_min": -480,
            "websocket_request_id": new_uuid(),
            "client_contextual_info": {
                "is_dark_mode": False,
                "time_since_loaded": 120,
                "page_height": 900,
                "page_width": 1400,
                "pixel_ratio": 2,
                "screen_height": 1440,
                "screen_width": 2560,
            },
        }
        if thinking_effort:
            payload["thinking_effort"] = thinking_effort

        path = "/backend-api/conversation"
        headers = self._headers(path, {
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
            "OpenAI-Sentinel-Chat-Requirements-Token": requirements["token"],
        })
        if requirements["proof_token"]:
            headers["OpenAI-Sentinel-Proof-Token"] = requirements["proof_token"]
        if requirements["turnstile_token"]:
            headers["OpenAI-Sentinel-Turnstile-Token"] = requirements["turnstile_token"]
        if requirements["so_token"]:
            headers["OpenAI-Sentinel-SO-Token"] = requirements["so_token"]

        resp = self.session.post(
            BASE_URL + path,
            headers=headers,
            json=payload,
            timeout=300,
            stream=True,
        )
        if resp.status_code != 200:
            raise RuntimeError(
                f"conversation failed: HTTP {resp.status_code} "
                f"{resp.text[:300] if resp.text else ''}"
            )
        return self._parse_sse(resp)

    def chat_with_retry(
        self,
        messages: list[dict],
        model: str = "auto",
        thinking_effort: str = "",
        token_file: str = DEFAULT_TOKEN_FILE,
        attempts: int = 3,
    ) -> str:
        """带 token 刷新和重试的 chat。"""
        for i in range(attempts):
            try:
                return self.chat(messages, model, thinking_effort)
            except RuntimeError as e:
                err = str(e)
                if ("401" in err or "Unauthorized" in err) and i < attempts - 1:
                    print("  token 过期，刷新中...", file=sys.stderr)
                    tokens = load_tokens(token_file)
                    tokens = refresh_access_token(tokens, token_file)
                    self.access_token = tokens["access_token"]
                    continue
                if i < attempts - 1:
                    wait = 10 * (i + 1)
                    print(f"  重试 {wait}s 后... ({err[:100]})", file=sys.stderr)
                    time.sleep(wait)
                    continue
                raise
        raise RuntimeError("unreachable")

    # -- SSE 解析 ----------------------------------------------------------
    @staticmethod
    def _parse_sse(response) -> str:
        text = ""
        for payload_str in iter_sse_payloads(response):
            if payload_str == "[DONE]":
                break
            try:
                event = json.loads(payload_str)
            except json.JSONDecodeError:
                continue

            # JSON-patch 风格增量
            if "p" in event and "o" in event:
                op = event.get("o")
                value = str(event.get("v") or "")
                if op == "append":
                    text += value
                elif op == "replace":
                    text = value
                continue

            # 完整消息快照
            message = event.get("message")
            if not message and isinstance(event.get("v"), dict):
                message = event["v"].get("message")
            if not message:
                continue
            author = message.get("author") or {}
            if author.get("role") != "assistant":
                continue
            content = message.get("content") or {}
            parts = content.get("parts") or []
            str_parts = [p for p in parts if isinstance(p, str)]
            if str_parts:
                text = "".join(str_parts)
        return text


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="轻量 ChatGPT 网页版客户端",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("message", nargs="?", help="要发送的消息")
    parser.add_argument("--file", "-f", help="从文件读取消息")
    parser.add_argument("--output", "-o", help="将回复保存到文件")
    parser.add_argument("--model", "-m", default="auto", help="模型名（默认 auto）")
    parser.add_argument("--thinking", action="store_true",
                        help="开启思考模式（extended）")
    parser.add_argument("--tokens", default=DEFAULT_TOKEN_FILE,
                        help="token 文件路径")
    parser.add_argument("--proxy", default="", help="代理地址（如 http://127.0.0.1:10808）")
    args = parser.parse_args()

    # 获取消息
    if args.file:
        with open(args.file, encoding="utf-8") as f:
            message = f.read()
    elif args.message:
        message = args.message
    else:
        parser.error("请提供消息或 --file")

    tokens = load_tokens(args.tokens)
    client = ChatGPTLite(tokens["access_token"], proxy=args.proxy)
    thinking = "extended" if args.thinking else ""
    messages = [{"role": "user", "content": message}]

    reply = client.chat_with_retry(
        messages, model=args.model, thinking_effort=thinking,
        token_file=args.tokens,
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(reply)
        print(f"已保存到 {args.output}", file=sys.stderr)
    else:
        print(reply)


if __name__ == "__main__":
    main()
