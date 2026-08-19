# -*- coding: utf-8 -*-
"""claude_lite.py — 轻量 Claude.ai 网页版客户端。

通过浏览器 session cookie 直接调用 Claude.ai 内部 API，
无需 API key，无需 Web 服务器。

用法（命令行）:
    python claude_lite.py "你好"
    python claude_lite.py --file prompt.txt --output result.txt
    python claude_lite.py --model claude-sonnet-4-6 "消息"
    python claude_lite.py --thinking --effort high "需要推理的难题"
    python claude_lite.py --list-models

用法（模块）:
    from claude_lite import ClaudeLite
    client = ClaudeLite.from_config("claude_config.json")
    reply, conv_id = client.chat("你好")
    # 开启思考模式（可选 effort: low/medium/high/xhigh/max）
    reply, conv_id = client.chat("难题", thinking=True, effort="high")
    thinking_text = client.last_thinking

首次使用:
    1. 浏览器登录 claude.ai
    2. F12 → Application → Cookies → 复制 sessionKey 的值
    3. 创建 claude_config.json:
       {"session_key": "sk-ant-sid02-xxx"}
    4. 运行脚本，org_id 会自动检测

依赖: requests（或 curl_cffi 用于绕过 Cloudflare）
"""

import argparse
import json
import os
import sys
import time
import uuid as uuid_mod

# ---------------------------------------------------------------------------
# HTTP 客户端：优先 curl_cffi（绕 Cloudflare TLS 指纹），回退 requests
# ---------------------------------------------------------------------------
try:
    from curl_cffi import requests as http
    _IMPERSONATE = "chrome120"
    _HAS_CURL_CFFI = True
except ImportError:
    import requests as http
    _IMPERSONATE = None
    _HAS_CURL_CFFI = False

BASE_URL = "https://claude.ai"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG = os.path.join(SCRIPT_DIR, "claude_config.json")
DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
DEFAULT_MODEL = "claude-sonnet-4-6"

# 思考模式（网页版称 Thinking / Extended thinking）。
# completion payload 用 thinking_mode 控制，取值 extended/standard/auto/off；
# 开启思考用 "extended"。
THINKING_MODE = "extended"
# effort 档位：网页版模型选择器里的 Low/Medium/High/Extra/Max。
# 注意并非每个模型都支持全部档位（如 sonnet-4-6 无 xhigh），
# 但 payload 层面取值范围如下；默认 high。
EFFORT_LEVELS = ("low", "medium", "high", "xhigh", "max")
DEFAULT_EFFORT = "high"


def _detect_system_proxy() -> str:
    try:
        import urllib.request
        proxies = urllib.request.getproxies()
        for scheme in ("https", "http"):
            if scheme in proxies:
                return proxies[scheme]
    except Exception:
        pass
    return ""


class ClaudeLite:
    """极简 Claude.ai 网页版对话客户端。"""

    def __init__(
        self,
        session_key: str,
        org_id: str = "",
        device_id: str = "",
        user_agent: str = "",
        proxy: str = "",
    ):
        self.session_key = session_key
        self.org_id = org_id
        self.device_id = device_id or str(uuid_mod.uuid4())
        self.user_agent = user_agent or DEFAULT_UA
        self.proxy = proxy or _detect_system_proxy()
        # 最近一次 chat 的思考文本（开启 thinking 时填充）
        self.last_thinking = ""

        session_kwargs = {}
        if _HAS_CURL_CFFI:
            session_kwargs["impersonate"] = _IMPERSONATE
            if self.proxy:
                session_kwargs["proxies"] = {
                    "http": self.proxy,
                    "https": self.proxy,
                }
            self.session = http.Session(**session_kwargs)
        else:
            self.session = http.Session()
            if self.proxy:
                self.session.proxies = {
                    "http": self.proxy,
                    "https": self.proxy,
                }

    # -- 工厂 ---------------------------------------------------------------
    @classmethod
    def from_config(cls, path: str = DEFAULT_CONFIG) -> "ClaudeLite":
        with open(path, encoding="utf-8") as f:
            cfg = json.load(f)
        return cls(
            session_key=cfg["session_key"],
            org_id=cfg.get("org_id", ""),
            device_id=cfg.get("device_id", ""),
            user_agent=cfg.get("user_agent", ""),
            proxy=cfg.get("proxy", ""),
        )

    # -- 内部 ---------------------------------------------------------------
    def _headers(self, extra: dict | None = None) -> dict:
        h = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
            "User-Agent": self.user_agent,
            "Origin": BASE_URL,
            "Referer": BASE_URL + "/",
            "anthropic-client-platform": "web_claude_ai",
            "anthropic-device-id": self.device_id,
            "Cookie": (
                f"sessionKey={self.session_key}; "
                f"lastActiveOrg={self.org_id}; "
                f"anthropic-device-id={self.device_id}"
            ),
        }
        if extra:
            h.update(extra)
        return h

    def _ensure_org(self) -> str:
        if self.org_id:
            return self.org_id
        resp = self.session.get(
            BASE_URL + "/api/organizations",
            headers=self._headers({"Accept": "application/json"}),
            timeout=30,
        )
        if resp.status_code != 200:
            raise RuntimeError(
                f"获取组织失败: HTTP {resp.status_code}。"
                f"sessionKey 可能已过期，请重新从浏览器提取。"
            )
        orgs = resp.json()
        if not orgs:
            raise RuntimeError("没有找到组织，请检查账号")
        self.org_id = orgs[0]["uuid"]
        return self.org_id

    def _create_conversation(self) -> str:
        org = self._ensure_org()
        conv_uuid = str(uuid_mod.uuid4())
        resp = self.session.post(
            f"{BASE_URL}/api/organizations/{org}/chat_conversations",
            headers=self._headers({"Accept": "application/json"}),
            json={"uuid": conv_uuid, "name": ""},
            timeout=30,
        )
        if resp.status_code not in (200, 201):
            raise RuntimeError(f"创建对话失败: HTTP {resp.status_code}")
        return conv_uuid

    # -- 模型信息 -----------------------------------------------------------
    def list_models(self, surface: str = "chat") -> list:
        """拉取账号可用模型及各自支持的思考模式 / effort 档位。

        返回 list[dict]，每项含 id / name / disabled / effort_options /
        mode_options。数据来自 /api/bootstrap/{org}/app_start 的
        model_selector_config。
        """
        org = self._ensure_org()
        url = (
            f"{BASE_URL}/api/bootstrap/{org}/app_start"
            f"?statsig_hashing_algorithm=djb2&growthbook_format=sdk"
        )
        resp = self.session.get(
            url,
            headers=self._headers({"Accept": "application/json"}),
            timeout=60,
        )
        if resp.status_code != 200:
            raise RuntimeError(
                f"获取模型配置失败: HTTP {resp.status_code}"
            )
        cfg = resp.json().get("model_selector_config") or []
        out = []
        for surf in cfg:
            if surf.get("id") != surface:
                continue
            for m in surf.get("models", []):
                th = m.get("thinking") or {}
                out.append({
                    "id": m.get("id"),
                    "name": m.get("name"),
                    "section": m.get("section"),
                    "disabled": bool(m.get("disabled")),
                    "thinking_type": th.get("type"),
                    "effort_options": [
                        e.get("id") for e in th.get("effort_options", [])
                    ],
                    "mode_options": [
                        e.get("id") for e in th.get("mode_options", [])
                    ],
                })
        return out

    # -- 对话 ---------------------------------------------------------------
    def chat(
        self,
        prompt: str,
        model: str = DEFAULT_MODEL,
        conversation_id: str = "",
        thinking: bool = False,
        effort: str = "",
        on_chunk: "callable | None" = None,
    ) -> tuple:
        """发送消息，返回 (助手回复文本, 对话 id)。

        conversation_id: 传入则继续该对话（多轮），空则新建。
        thinking: 开启思考模式（payload 里 thinking_mode=extended）。
        effort: 思考努力程度 low/medium/high/xhigh/max；仅在 thinking 时生效，
                留空则用默认 high。
        on_chunk: 可选回调 on_chunk(增量文本)，流式收到正文增量时触发，
                  用于 CLI 实时显示。
        说明：思考过程在服务端进行，网页对话历史可见，但 completion 流通常
        不回传思考文本，故 self.last_thinking 多数情况为空。
        """
        org = self._ensure_org()
        if not conversation_id:
            conversation_id = self._create_conversation()

        payload: dict = {
            "prompt": prompt,
            "timezone": "Asia/Shanghai",
            "locale": "en-US",
            "model": model,
            "attachments": [],
            "files": [],
        }
        if thinking:
            eff = (effort or DEFAULT_EFFORT).lower()
            if eff not in EFFORT_LEVELS:
                raise ValueError(
                    f"effort 取值须为 {EFFORT_LEVELS}，收到 {effort!r}"
                )
            # 网页版 completion 端点用 thinking_mode 控制思考开关
            # （取值 extended/standard/auto/off），effort 控制努力程度。
            # 注意：paprika_mode 会被后端以 "Extra inputs" 拒绝，不能传。
            payload["thinking_mode"] = THINKING_MODE
            payload["effort"] = eff

        url = (
            f"{BASE_URL}/api/organizations/{org}"
            f"/chat_conversations/{conversation_id}/completion"
        )
        headers = self._headers({
            "Referer": f"{BASE_URL}/chat/{conversation_id}",
        })

        resp = self.session.post(
            url, headers=headers, json=payload,
            timeout=300, stream=True,
        )
        if resp.status_code == 429:
            reset = ""
            try:
                inner = json.loads(json.loads(resp.text)["error"]["message"])
                ts = inner.get("resetsAt")
                if ts:
                    reset = time.strftime(
                        "%Y-%m-%d %H:%M", time.localtime(ts)
                    )
            except Exception:
                pass
            raise RuntimeError(
                f"Rate limited (HTTP 429); approximate quota reset: "
                f"{reset or 'unknown'}"
            )
        if resp.status_code != 200:
            body = ""
            try:
                body = resp.text[:300]
            except Exception:
                pass
            raise RuntimeError(
                f"completion 失败: HTTP {resp.status_code} {body}"
            )
        text, thinking_text = self._parse_sse(resp, on_chunk)
        self.last_thinking = thinking_text
        return text, conversation_id

    # -- SSE 解析 -----------------------------------------------------------
    @staticmethod
    def _parse_sse(response, on_chunk=None) -> tuple:
        """解析 SSE 流，返回 (正文, 思考文本)。

        on_chunk: 收到正文增量时回调 on_chunk(增量文本)。
        """
        text = ""
        thinking = ""
        for raw_line in response.iter_lines():
            if not raw_line:
                continue
            line = raw_line.decode("utf-8", errors="ignore")
            if not line.startswith("data:"):
                continue
            data_str = line[5:].strip()
            if not data_str or data_str == "[DONE]":
                continue
            try:
                data = json.loads(data_str)
            except json.JSONDecodeError:
                continue
            if data.get("type") == "completion":
                chunk = data.get("completion", "")
                if chunk:
                    text += chunk
                    if on_chunk:
                        on_chunk(chunk)
            elif data.get("type") == "content_block_delta":
                delta = data.get("delta", {})
                dtype = delta.get("type")
                if dtype == "text_delta":
                    piece = delta.get("text", "")
                    text += piece
                    if on_chunk and piece:
                        on_chunk(piece)
                elif dtype == "thinking_delta":
                    thinking += delta.get("thinking", "")
        return text, thinking


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="轻量 Claude.ai 网页版客户端",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("message", nargs="?", help="要发送的消息")
    parser.add_argument("--file", "-f", help="从文件读取消息")
    parser.add_argument("--output", "-o", help="将回复保存到文件")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL,
                        help=f"模型名（默认 {DEFAULT_MODEL}）")
    parser.add_argument("--config", default=DEFAULT_CONFIG,
                        help="配置文件路径")
    parser.add_argument("--thinking", "-t", action="store_true",
                        help="开启思考模式（thinking_mode=extended）")
    parser.add_argument("--effort", "-e", default="",
                        choices=["", *EFFORT_LEVELS],
                        help=f"思考努力程度（默认 {DEFAULT_EFFORT}，"
                             f"需配合 --thinking）")
    parser.add_argument("--show-thinking", action="store_true",
                        help="把思考过程也打印/保存到输出")
    parser.add_argument("--list-models", action="store_true",
                        help="列出账号可用模型及其思考/effort 支持后退出")
    args = parser.parse_args()

    client = ClaudeLite.from_config(args.config)

    if args.list_models:
        rows = client.list_models()
        if not rows:
            print("（未获取到模型配置）")
            return
        for r in rows:
            flag = "不可用" if r["disabled"] else "可用"
            eff = ",".join(r["effort_options"]) or "-"
            modes = ",".join(r["mode_options"]) or "-"
            print(f"[{flag}] {r['id']}  ({r['name']})")
            print(f"      thinking={r['thinking_type']}  "
                  f"effort=[{eff}]  mode=[{modes}]")
        return

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            message = f.read()
    elif args.message:
        message = args.message
    else:
        parser.error("请提供消息或 --file")

    reply, conv_id = client.chat(
        message, model=args.model,
        thinking=args.thinking, effort=args.effort,
    )

    out = reply
    if args.show_thinking and client.last_thinking:
        out = (
            "<thinking>\n" + client.last_thinking + "\n</thinking>\n\n"
            + reply
        )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"已保存到 {args.output}", file=sys.stderr)
    else:
        print(out)


if __name__ == "__main__":
    main()
