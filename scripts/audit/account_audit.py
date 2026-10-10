#!/usr/bin/env python3
"""lhg-social-ops 确定性账号审计：11 条规则，零第三方依赖。

扫描目标目录下的 posts.json（发布记录），输出 JSON 与人类可读报告；
有 blocker 时以 exit code 2 退出（供 hooks 与 CI 使用）。

posts.json 格式：[{"id","platform","published_at"(ISO8601),"text",
  "hashtags":[], "views","likes","comments","shares","new_followers"}]

用法：
    python3 account_audit.py --target <数据目录> [--format json|text] [--fail-on blocker|warning|nit]

规则文案均为本项目原创（思路受 claude-social-media-skills 的
buffer-stats/audit-buffer-queue 闭环复盘思想启发，未复制任何第三方原文）。
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

VERSION = "1.0.0"
TOOL = "lhg-social-ops/account-audit"

# 极限词/违禁词（广告法高风险词，命中即 blocker；上下文误伤由人工复核豁免）
EXTREME_WORDS = [
    "国家级", "世界级", "最高级", "最佳", "第一", "顶级", "极致", "首选",
    "首家", "首款", "独家", "绝无仅有", "史无前例", "万能", "祖传",
    "百分百", "100%", "零风险", "保本", "稳赚不赔", "包赚", "一夜暴富",
    "全网最低价", "最低价", "秒杀一切", "彻底根治", "药到病除",
    "保证收益", "承诺收益", "保收益",
]
# 收益/疗效承诺（blocker）
PROMISE_RES = [
    re.compile(r"保证.*收益"),
    re.compile(r"承诺.*收益"),
    re.compile(r"稳赚|包赚|必赚"),
    re.compile(r"根治|治愈|包治"),
    re.compile(r"药到病除"),
    re.compile(r"一夜暴富|暴富神话"),
]

MAX_GAP_DAYS = 7      # 断更红线
SPAM_PER_DAY = 3       # 刷屏红线（同平台同日）
MAX_HASHTAGS = 8       # 标签堆砌红线
ENGAGE_FLOOR = 0.005   # 互动率异常线（播放>=1000 且互动率低于此）
LONG_TEXT = 800        # 文案过长线（字符）


class Finding:
    __slots__ = ("rule_id", "severity", "category", "title", "file", "line", "snippet", "detail")

    def __init__(self, rule_id, severity, category, title, file, line, snippet, detail):
        self.rule_id = rule_id
        self.severity = severity
        self.category = category
        self.title = title
        self.file = file
        self.line = line
        self.snippet = snippet
        self.detail = detail

    def to_dict(self):
        return {
            "rule_id": self.rule_id, "severity": self.severity,
            "category": self.category, "title": self.title,
            "file": self.file, "line": self.line,
            "snippet": self.snippet, "detail": self.detail,
        }


RULES = []
_RULE_BY_ID = {}


def rule(rule_id, severity, category, title, detail):
    def deco(fn):
        r = {"id": rule_id, "severity": severity, "category": category,
             "title": title, "detail": detail}
        _RULE_BY_ID[rule_id] = r
        r["check"] = fn
        RULES.append(r)
        return fn
    return deco


def _F(rule_id, line, snippet):
    r = _RULE_BY_ID[rule_id]
    return Finding(r["id"], r["severity"], r["category"], r["title"],
                   "posts.json", line, snippet[:160], r["detail"])


def parse_dt(s):
    try:
        dt = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


# ---------------- 发布节奏 ----------------

@rule("SO-CAD-001", "warning", "发布节奏", "断更",
      "相邻两篇发布时间间隔超过 7 天。断更超 7 天，算法和粉丝都会把你忘了。")
def r_cad_001(posts, ctx):
    ts = sorted((p["_dt"], p.get("id", "?")) for p in posts if p.get("_dt"))
    out = []
    for (a, ida), (b, idb) in zip(ts, ts[1:]):
        gap = (b - a).days
        if gap > MAX_GAP_DAYS:
            out.append(_F("SO-CAD-001", 0, "%s → %s 间隔 %d 天" % (ida, idb, gap)))
    return out


@rule("SO-CAD-002", "warning", "发布节奏", "刷屏",
      "同一平台同一天发布超过 3 篇。刷屏掉粉又限流，请打散排期。")
def r_cad_002(posts, ctx):
    from collections import Counter
    c = Counter()
    for p in posts:
        if p.get("_dt"):
            c[(p.get("platform", "?"), p["_dt"].date().isoformat())] += 1
    return [_F("SO-CAD-002", 0, "%s %s 发布 %d 篇" % (plat, day, n))
            for (plat, day), n in sorted(c.items()) if n > SPAM_PER_DAY]


@rule("SO-CAD-003", "nit", "发布节奏", "发布时间扎堆",
      "全部内容挤在同一个小时发布。错开高峰，给每篇留出发酵时间。")
def r_cad_003(posts, ctx):
    from collections import Counter
    hours = Counter(p["_dt"].hour for p in posts if p.get("_dt"))
    if len(posts) >= 5 and len(hours) == 1:
        h = next(iter(hours))
        return [_F("SO-CAD-003", 0, "%d 篇全部在 %d 点发布" % (len(posts), h))]
    return []


# ---------------- 话题标签 ----------------

@rule("SO-TAG-001", "warning", "话题标签", "标签缺失",
      "文案没有任何话题标签。白白浪费推荐流量，每篇至少配 2 个标签。")
def r_tag_001(posts, ctx):
    return [_F("SO-TAG-001", 0, "%s 无标签" % p.get("id", "?"))
            for p in posts if not p.get("hashtags")]


@rule("SO-TAG-002", "warning", "话题标签", "标签堆砌",
      "单篇标签超过 8 个。堆砌标签会被判营销号，砍到 2-5 个。")
def r_tag_002(posts, ctx):
    return [_F("SO-TAG-002", 0, "%s 有 %d 个标签" % (p.get("id", "?"), len(p["hashtags"])))
            for p in posts if len(p.get("hashtags") or []) > MAX_HASHTAGS]


# ---------------- 合规红线 ----------------

@rule("SO-RSK-001", "blocker", "合规红线", "极限词/违禁词",
      "文案命中广告法高风险词。这类文案不许发布，改完重跑审计。"
      "（上下文误伤如'第一期节目'，人工复核后豁免。）")
def r_rsk_001(posts, ctx):
    out = []
    for p in posts:
        text = p.get("text", "") or ""
        hits = [w for w in EXTREME_WORDS if w in text]
        if hits:
            out.append(_F("SO-RSK-001", 0, "%s 命中：%s" % (p.get("id", "?"), "、".join(hits[:3]))))
    return out


@rule("SO-RSK-002", "blocker", "合规红线", "收益/疗效承诺",
      "文案含收益保证或疗效承诺类表述。这是封号+罚款的高危区，必须改掉。")
def r_rsk_002(posts, ctx):
    out = []
    for p in posts:
        text = p.get("text", "") or ""
        hit = next((rx for rx in PROMISE_RES if rx.search(text)), None)
        if hit:
            out.append(_F("SO-RSK-002", 0, "%s 命中：%s" % (p.get("id", "?"), hit.pattern)))
    return out


# ---------------- 复盘数据 ----------------

@rule("SO-REV-001", "warning", "复盘数据", "复盘缺关键指标",
      "缺少播放/点赞/评论等关键指标。拿残缺数据复盘等于闭眼开车，先补数。")
def r_rev_001(posts, ctx):
    out = []
    for p in posts:
        missing = [k for k in ("views", "likes", "comments") if p.get(k) is None]
        if missing:
            out.append(_F("SO-REV-001", 0, "%s 缺：%s" % (p.get("id", "?"), "、".join(missing))))
    return out


@rule("SO-REV-002", "warning", "复盘数据", "互动率异常",
      "播放 ≥1000 但互动率 < 0.5%。可能是买量，可能是选题失配——先问用户，别当正常数据用。")
def r_rev_002(posts, ctx):
    out = []
    for p in posts:
        v = p.get("views") or 0
        if v >= 1000:
            eng = ((p.get("likes") or 0) + (p.get("comments") or 0) * 3) / v
            if eng < ENGAGE_FLOOR:
                out.append(_F("SO-REV-002", 0,
                              "%s 播放 %d，互动率 %.2f%%" % (p.get("id", "?"), v, eng * 100)))
    return out


# ---------------- 结构 ----------------

@rule("SO-PLT-001", "nit", "结构", "平台单一",
      "≥3 篇内容只发了 1 个平台。单点风险高，建议至少覆盖 2 个平台。")
def r_plt_001(posts, ctx):
    plats = {p.get("platform", "?") for p in posts}
    if len(posts) >= 3 and len(plats) == 1:
        return [_F("SO-PLT-001", 0, "%d 篇只在 %s 发布" % (len(posts), next(iter(plats))))]
    return []


@rule("SO-TXT-001", "nit", "结构", "文案过长",
      "单篇文案超过 800 字。短视频/图文平台用户没耐心，拆成系列发。")
def r_txt_001(posts, ctx):
    return [_F("SO-TXT-001", 0, "%s 文案 %d 字" % (p.get("id", "?"), len(p.get("text", ""))))
            for p in posts if len(p.get("text", "") or "") > LONG_TEXT]


# ---------------------------------------------------------------- 运行器

def load_posts(target):
    fp = os.path.join(target, "posts.json")
    if not os.path.isfile(fp):
        return None
    try:
        with open(fp, encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception:
        return None
    posts = data if isinstance(data, list) else data.get("posts", [])
    for p in posts:
        p["_dt"] = parse_dt(p.get("published_at"))
    return posts


def main(argv=None):
    ap = argparse.ArgumentParser(description="lhg-social-ops 账号运营确定性审计")
    ap.add_argument("--target", default=".", help="数据目录（含 posts.json）")
    ap.add_argument("--format", choices=["json", "text"], default="text")
    ap.add_argument("--fail-on", choices=["blocker", "warning", "nit"], default="blocker")
    args = ap.parse_args(argv)

    target = os.path.abspath(args.target)
    posts = load_posts(target)
    if posts is None:
        print("target 下没有合法的 posts.json：%s" % args.target, file=sys.stderr)
        return 1

    findings = []
    for r in RULES:
        try:
            findings.extend(r["check"](posts, {}) or [])
        except Exception:
            continue

    sev_rank = {"blocker": 3, "warning": 2, "nit": 1}
    counts = {"blocker": 0, "warning": 0, "nit": 0}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1

    result = {
        "tool": TOOL,
        "version": VERSION,
        "target": args.target,
        "summary": {
            "posts_scanned": len(posts),
            "rules_run": len(RULES),
            "blocker": counts["blocker"],
            "warning": counts["warning"],
            "nit": counts["nit"],
        },
        "findings": [f.to_dict() for f in sorted(
            findings, key=lambda x: (-sev_rank.get(x.severity, 0), x.snippet))],
    }

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        s = result["summary"]
        print("账号运营审计：扫描 %d 篇内容，运行 %d 条规则" % (s["posts_scanned"], s["rules_run"]))
        print("blocker=%d warning=%d nit=%d" % (s["blocker"], s["warning"], s["nit"]))
        for f in result["findings"]:
            print("[%s][%s] %s %s" % (
                f["severity"].upper(), f["rule_id"], f["file"], f["title"]))
            print("    %s" % f["detail"])
            if f["snippet"]:
                print("    → %s" % f["snippet"])

    level = sev_rank[args.fail_on]
    bad = any(sev_rank.get(f.severity, 0) >= level for f in findings)
    return 2 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
