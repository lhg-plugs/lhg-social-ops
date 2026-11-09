<!-- About 简介（推送后填写到仓库 About 栏）：
社媒运营专家：账号定位→内容日历→多平台分发策略→数据复盘，做策略与复盘闭环（执行层分发交给人工与专用工具）。 ｜ 一键安装：/plugin marketplace add lhg-plugs/lhg-social-ops
-->
<!-- topics（推送后打）：claude-code, claude-plugin, agent-skills, social-media, content-strategy, content-calendar, analytics, review -->

<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="lhg-social-ops — 社媒运营专家">
</p>

> **一句话介绍**：社媒运营专家：账号定位→内容日历→多平台分发策略→数据复盘，做策略与复盘闭环（执行层分发交给人工与专用工具）。

**一键安装**：在 Claude Code 里运行

```bash
/plugin marketplace add lhg-plugs/lhg-social-ops
/plugin install lhg-social-ops@lhg-plugs
```

## 它能帮你做出什么

每条产出先过确定性脚本自查，再交人工复核清单——数字全部数自仓库里的审计脚本，不靠模型"自觉"。

| 自查脚本 | 规则数 | blocker | warning | nit | 覆盖 |
|---|---|---|---|---|---|
| `scripts/audit/account_audit.py` | 11 | 2 | 6 | 3 | 发布节奏、话题标签、合规红线、复盘数据、结构 |
| **合计** | **11** | **2** | **6** | **3** | |

- **零 LLM 成本**：规则是纯 Python 脚本，零第三方依赖，本地运行。
- **坏 / 好对照可验**：`fixtures/` 里备有坏/好用例，冒烟测试断言命中情况。
- **冒烟全绿**：`python3 smoke_test.py` 48 项全部通过（JSON 合法、frontmatter 完整、命令/skill/agent 齐全）。

## 它是什么

`lhg-social-ops` 是一个 Claude Code 插件（plugin 为主、skill 为辅）：

- **5 个命令**（小白入口）：`audit` 账号运营体检、`calendar` 内容日历、`positioning` 账号定位、`review` 数据复盘、`social-ops` 社媒运营全流程
- **4 个平台中立 skill**（方法论，可移植到豆包/Workbuddy 等 agent 平台）：lhg-so-calendar, lhg-so-distribute, lhg-so-positioning, lhg-so-review
- **3 个专家 agent**：positioner, reviewer, scheduler
- **2 个 hooks**（`hooks/`：post_draft_remind.py, pre_auto_publish_guard.py），关键操作前自动把关
- **11 条确定性自查规则**：纯 Python 脚本，见上表

## 为什么是它

不是一个 prompt，而是一套互相兜底的机制：

1. **确定性脚本（机器）+ 人工复核清单（人）**：先跑 `scripts/` 下的审计脚本（共 11 条规则），发现分三级：**blocker**（必须修）、**warning**（修或写豁免理由）、**nit**（顺手修）；再按对应 skill 的复核清单过一遍脚本抓不到的（内容真实性、越权、口径一致）。blocker 清零才算做完；为清零改规则算作弊，不许。
2. **硬门，不是提醒**：hooks 在关键操作前自动拦截或警告（见 `hooks/`），而不是只在文档里写一句"请注意"。
3. **方法论沉淀在 skill 里**：流程、检查清单、口径都写在 `skills/` 的方法论里，命令只是入口；换个 agent 平台也能复用同一套做法。
4. **可验，不是可信**：`fixtures/` 备有坏/好对照用例，`smoke_test.py` 一键验证，规则有没有生效、自己跑一遍就知道。

## 快速上手

```bash
# 1. 安装（Claude Code 里运行）
/plugin marketplace add lhg-plugs/lhg-social-ops
/plugin install lhg-social-ops@lhg-plugs

# 2. 社媒运营全流程：账号定位→内容日历→多平台分发策略→数据复盘，一条龙跑完策略闭环
/lhg-social-ops:social-ops "A股财报解读抖音号" --platforms "抖音, 小红书"
```

| 命令 | 作用 | 示例 |
|---|---|---|
| `/lhg-social-ops:audit` | 账号运营体检：跑确定性审计脚本（断更/刷屏/标签/违禁词/复盘指标），输出分级报告。 | `/lhg-social-ops:audit data/` |
| `/lhg-social-ops:calendar` | 内容日历：按定位卡生成 4 周排期（选题/形式/平台/时间/标签），防断更防刷屏。 | `/lhg-social-ops:calendar positioning.md` |
| `/lhg-social-ops:positioning` | 账号定位：人群→价值→差异化三问，输出一句话定位+内容支柱+人设语气卡。 | `/lhg-social-ops:positioning "讲财报的抖音号"` |
| `/lhg-social-ops:review` | 数据复盘：读 posts.json 做周期复盘，输出爆款归因+哑火诊断+下周调整动作。 | `/lhg-social-ops:review data/` |
| `/lhg-social-ops:social-ops` | 社媒运营全流程：账号定位→内容日历→多平台分发策略→数据复盘，一条龙跑完策略闭环。 | `/lhg-social-ops:social-ops "A股财报解读抖音号" --platforms "抖音, 小红书"` |

## 什么时候用 / 什么时候不用（FAQ）

**什么时候用：**

- 你需要账号运营体检时 → 用 `/lhg-social-ops:audit`
- 你需要内容日历时 → 用 `/lhg-social-ops:calendar`
- 你需要账号定位时 → 用 `/lhg-social-ops:positioning`

**什么时候不用：**

- 你只需要其中一个零散能力时 → 本插件是成套流程，单点需求用更轻量的 skill 更合适
- 你希望 AI 完全自由发挥、不接受任何自查与硬门时 → 它的规则审计与 hooks 会介入（可关，但那就别装它）
- 你的场景不在上面命令表覆盖范围内时 → 先看命令表，没有对应命令就别硬套

## 目录结构

```
lhg-social-ops/
├── smoke_test.py          # 一键冒烟测试
├── ATTRIBUTION.md         # 灵感来源与许可声明
├── LICENSE                # MIT
├── README.md              # 本文件
├── .claude-plugin/
├── agents/
├── commands/
├── fixtures/
├── hooks/
├── scripts/
├── skills/
```

## 自检与反馈

本插件自带质检：每次使用后可跑 `python3 smoke_test.py` 一键验证（本次实测 48 项全部通过）。

发现 bug 或有改进建议，以 `[QC] <一句话问题>` 为标题提交到 https://github.com/lhg-plugs/lhg-social-ops/issues，正文写清"复现步骤 → 实际表现 → 期望表现"。

同门插件见 [lhg-plugs](https://github.com/lhg-plugs)，86 个插件的完整矩阵在 [marketplace](https://github.com/lhg-plugs/marketplace) 维护。

## 出品：刘洪光

本插件由真人出镜 IP「刘洪光」（安徽合肥）出品，归属 [lhg-skills](https://github.com/lhg-skills)。

- GitHub 主页：https://github.com/lhg-skills —— 全部 skill 开源在此，欢迎 star
- 抖音：搜「刘老师讲AI实战」
- 微信：lhgsmsw
