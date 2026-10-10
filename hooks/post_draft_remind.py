#!/usr/bin/env python3
"""lhg-social-ops 提醒（警告级，不拦截）：写 drafts/ 下的发布文案 md 时提醒审稿。

触发：PostToolUse / Write|Edit。只做提醒，永远 exit 0、不拦截写入。

逃生方式：LHG_SO_HOOKS_OFF=1（环境变量）可关闭本提醒；
或 /plugin disable lhg-social-ops 停用整个插件。
零第三方依赖。
"""

import json
import os
import sys


def main() -> int:
    if os.environ.get("LHG_SO_HOOKS_OFF") == "1":
        return 0

    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        return 0

    tool_input = payload.get("tool_input", {}) or {}
    file_path = (tool_input.get("file_path", "") or "").replace("\\", "/")
    if not file_path.endswith(".md"):
        return 0
    parts = file_path.split("/")
    if "drafts" not in parts and "draft" not in parts:
        return 0

    msg = (
        "审稿提醒（lhg-social-ops）：%s 疑似待发布的社媒文案。\n"
        "发布前请做三件事：①跑 /lhg-social-ops:audit 扫违禁词/极限词；"
        "②检查标签 2-5 个；③确认发布时间。\n"
        "本插件不做自动发布，请人工手动发布。\n"
        "关闭本提醒：export LHG_SO_HOOKS_OFF=1（当前会话有效）。"
    ) % file_path
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": msg,
        }
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
