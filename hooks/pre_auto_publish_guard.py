#!/usr/bin/env python3
"""lhg-social-ops 硬门：拦截疑似"自动发布到社媒平台"的 Bash 命令。

触发：PreToolUse / Bash。只拦截命令文本命中自动发布模式的情况，
普通命令 0 开销直接放行。

为什么拦截：各平台反营销/反爬策略严，自动化发布易触发风控导致封号；
本插件定位是"策略+复盘"，执行层分发交给人工或专用发布工具。
这不是 bug，是保护。

逃生方式（按推荐度排序）：
  1. 人工手动发布（推荐），或用专用发布工具（如浏览器自动化+人工确认类工具）。
  2. 确认自担风控后果：LHG_SO_HOOKS_OFF=1 <原命令>（单次豁免本次 hook）。
  3. /plugin disable lhg-social-ops（整个插件停用，hooks 不再触发）。

设计原则：正则命中才拦截，未命中一律放行；脚本内部出错 fail-open。
零第三方依赖。
"""

import json
import os
import re
import sys

# 自动发布模式：命中其一即拦截
AUTO_PUBLISH_RES = [
    re.compile(r"auto_?publish", re.I),
    re.compile(r"一键发布"),
    re.compile(r"自动发布"),
    re.compile(r"定时群发"),
    re.compile(r"批量发布"),
    re.compile(r"群发助手"),
    re.compile(r"auto_?poster", re.I),
    re.compile(r"social_?poster", re.I),
]


def main() -> int:
    if os.environ.get("LHG_SO_HOOKS_OFF") == "1":
        return 0

    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        return 0  # 输入解析失败：fail-open

    tool_input = payload.get("tool_input", {}) or {}
    command = tool_input.get("command", "") or ""

    hit = next((rx for rx in AUTO_PUBLISH_RES if rx.search(command)), None)
    if not hit:
        return 0  # 非自动发布命令：快速放行

    reason = (
        "命令被 lhg-social-ops 硬门拦截：检测到疑似自动发布到社媒平台的命令"
        "（命中模式：%s）。\n\n"
        "为什么拦截：各平台反营销策略严，自动化发布易触发风控导致封号；"
        "本插件只做策略+复盘，不做执行层分发。\n\n"
        "正确做法：人工手动发布，或用专用发布工具（浏览器自动化+人工确认类）；\n"
        "发布前先跑 /lhg-social-ops:audit 扫一遍违禁词。\n\n"
        "确认自担风控后果后单次豁免：LHG_SO_HOOKS_OFF=1 <原命令>"
    ) % hit.pattern
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
