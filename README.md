<!-- About 简介（推送后填写到仓库 About 栏）：
社媒运营专家：账号定位→内容日历→多平台分发策略→数据复盘，策略+复盘闭环 ｜ 一键安装：/plugin marketplace add lhg-plugs/lhg-social-ops
-->
<!-- topics（推送后打）：claude-code, claude-plugin, agent-skills, social-media, content-strategy, marketing, chinese -->

# lhg-social-ops：社媒运营专家

> **一句话介绍**：给 AI 装上"社媒运营总监"——账号定位→内容日历→多平台分发策略→数据复盘，专做策略与复盘闭环；执行层分发交给人工与专用工具，不碰自动发布。
>
> **一键安装**：在 Claude Code 里运行
> ```
> /plugin marketplace add lhg-plugs/lhg-social-ops
> /plugin install lhg-social-ops@lhg-plugs
> ```

## 它是什么

`lhg-social-ops` 是一个 Claude Code 插件（plugin 为主、skill 为辅）：

- **5 个命令**（小白入口）：`social-ops` 一句话跑全流程，`positioning` 账号定位，`calendar` 内容日历，`review` 数据复盘，`audit` 账号体检
- **4 个平台中立 skill**（方法论，可移植到豆包/Workbuddy 等 agent 平台）：账号定位、内容日历、多平台分发策略、数据复盘
- **3 个专家 agent**：定位顾问 positioner、排期编排师 scheduler、复盘分析师 reviewer
- **2 个 hooks**：自动发布拦截（硬门，防封号，可一键豁免）、写发布文案时审稿提醒（警告级）
- **11 条确定性审计规则**：纯 Python、零第三方依赖，专治断更/刷屏、标签缺失堆砌、违禁词极限词、复盘缺指标

**差异化定位**：本插件做**策略 + 复盘**，不做执行层分发。自动发布请用人工或专用发布工具（如 AINightCoder/claude-code-social-skills 这类发布向 skill）；本插件的硬门会拦截自动发布命令——这是保护，不是 bug。

## 5 个命令用法

| 命令 | 作用 | 示例 |
|---|---|---|
| `/lhg-social-ops:social-ops` | 一句话 → 社媒运营全流程（定位→日历→分发策略→复盘） | `/lhg-social-ops:social-ops "A股财报解读抖音号" --platforms "抖音, 小红书"` |
| `/lhg-social-ops:positioning` | 账号定位（三问+定位卡+压力测试） | `/lhg-social-ops:positioning "讲财报的抖音号"` |
| `/lhg-social-ops:calendar` | 4 周内容日历（防断更防刷屏） | `/lhg-social-ops:calendar positioning.md` |
| `/lhg-social-ops:review` | 数据复盘（爆款归因+哑火诊断+下周调整） | `/lhg-social-ops:review data/` |
| `/lhg-social-ops:audit` | 账号体检（11 条规则+人工复核） | `/lhg-social-ops:audit data/` |

## 质检说明

质检 = 确定性脚本（机器）+ 人工评审清单（人）：

1. 先跑 `scripts/audit/account_audit.py --target data/`（11 条规则，零 LLM 成本）；
2. 发现分三级：**blocker**（违禁词/极限词、收益或疗效承诺——这类文案不许发布，硬门兜底）、**warning**（断更、刷屏、标签缺失/堆砌、复盘缺指标、互动异常——修或写豁免理由）、**nit**（平台单一、文案过长、发布时间扎堆——顺手修）；
3. 再人工复核脚本抓不到的（极限词误伤、断更是真断更还是没录入、互动异常是买量还是选题失配）。

blocker 清零才算过；为清零改规则算作弊，不许。

## 数据格式

`data/posts.json`：每篇一条，字段 `id / platform / published_at(ISO8601) / text / hashtags[] / views / likes / comments / shares / new_followers`。复盘与审计都读它，先把数据记全，复盘才有意义。

## 目录结构

```
lhg-social-ops/
├── .claude-plugin/          # plugin.json（插件清单）+ marketplace.json（本仓即市场）
├── commands/                # 5 个命令：social-ops / positioning / calendar / review / audit
├── skills/                  # 4 个平台中立 skill（lhg-so-positioning/calendar/distribute/review）
├── agents/                  # 3 个专家 agent（positioner / scheduler / reviewer）
├── hooks/                   # 2 个门：自动发布拦截 / 写文案审稿提醒 + 豁免说明
├── scripts/audit/           # 11 条确定性审计规则（零第三方依赖）
├── fixtures/                # 冒烟测试用例（坏/好发布记录对照）
├── smoke_test.py            # 一键冒烟测试
├── ATTRIBUTION.md           # 灵感来源与许可声明
└── LICENSE                  # MIT
```

## 什么时候用 / 什么时候不用（FAQ）

**什么时候用：**

- 你要新开一个账号，不知道发什么、怎么发时 → 用 `/lhg-social-ops:social-ops` 跑全流程
- 账号做了三个月没起色，怀疑定位错了时 → 用 `/lhg-social-ops:positioning` 重做定位
- 更新节奏乱、时而刷屏时而断更时 → 用 `/lhg-social-ops:calendar` 重建纪律
- 想知道"哪类选题爆、哪类哑、下周调什么"时 → 用 `/lhg-social-ops:review`
- 发之前怕文案踩违禁词、怕被限流时 → 用 `/lhg-social-ops:audit` 体检

**什么时候不用：**

- 你要的是一键自动发布/定时群发工具 → 本插件不做执行层，还会拦截自动发布；去用专用发布工具
- 你只想让 AI 代写 100 篇文案批量发 → 刷屏会被它的审计标 warning，封号风险自己担
- 你的账号已经有成熟 SOP，只缺执行人力 → 本插件是策略方法论，不是代运营

## lhg-plugs 插件矩阵

| 插件 | 一句话 | 安装 |
|---|---|---|
| [lhg-fullstack](https://github.com/lhg-plugs/lhg-fullstack) | 小白一句话 → 高质量全栈应用 | `/plugin install lhg-fullstack@lhg-plugs` |
| [lhg-video-edit](https://github.com/lhg-plugs/lhg-video-edit) | 一句话把口播素材剪成爆款短视频（+口播脚本子命令） | `/plugin install lhg-video-edit@lhg-plugs` |
| [lhg-wechat-article](https://github.com/lhg-plugs/lhg-wechat-article) | 公众号写作专家：选题到排版一气呵成 | `/plugin install lhg-wechat-article@lhg-plugs` |
| [lhg-xiaohongshu](https://github.com/lhg-plugs/lhg-xiaohongshu) | 小红书种草专家：卖点到爆款笔记一键生成 | `/plugin install lhg-xiaohongshu@lhg-plugs` |
| [lhg-resume](https://github.com/lhg-plugs/lhg-resume) | 简历优化专家：ATS诊断到模拟面试一条龙 | `/plugin install lhg-resume@lhg-plugs` |
| [lhg-ppt](https://github.com/lhg-plugs/lhg-ppt) | PPT制作专家：述职融资答辩一键成稿 | `/plugin install lhg-ppt@lhg-plugs` |
| [lhg-excel](https://github.com/lhg-plugs/lhg-excel) | 表格数据专家：清洗透视图表一条龙 | `/plugin install lhg-excel@lhg-plugs` |
| [lhg-thesis](https://github.com/lhg-plugs/lhg-thesis) | 毕业论文助手：开题到盲审的写作流水线 | `/plugin install lhg-thesis@lhg-plugs` |
| [lhg-miniprogram](https://github.com/lhg-plugs/lhg-miniprogram) | 小程序开发专家：一句话生成微信小程序 | `/plugin install lhg-miniprogram@lhg-plugs` |
| [lhg-contract](https://github.com/lhg-plugs/lhg-contract) | 合同审查助手：风险条款标红+修改建议 | `/plugin install lhg-contract@lhg-plugs` |
| [lhg-geo](https://github.com/lhg-plugs/lhg-geo) | AI搜索优化专家：品牌在AI回答里的可见度 | `/plugin install lhg-geo@lhg-plugs` |
| [lhg-poster](https://github.com/lhg-plugs/lhg-poster) | 海报设计专家：一句话生成手机端海报 | `/plugin install lhg-poster@lhg-plugs` |
| [lhg-shopify](https://github.com/lhg-plugs/lhg-shopify) | 独立站建站专家：高转化店铺一键搭建 | `/plugin install lhg-shopify@lhg-plugs` |
| [lhg-fiction](https://github.com/lhg-plugs/lhg-fiction) | 网文写作专家：大纲到逐章+人设一致性检测 | `/plugin install lhg-fiction@lhg-plugs` |
| [lhg-drama-script](https://github.com/lhg-plugs/lhg-drama-script) | 短剧剧本专家：分集大纲到单集剧本 | `/plugin install lhg-drama-script@lhg-plugs` |
| [lhg-lit-review](https://github.com/lhg-plugs/lhg-lit-review) | 文献综述专家：框架到引用校验一条龙 | `/plugin install lhg-lit-review@lhg-plugs` |
| [lhg-salary-talk](https://github.com/lhg-plugs/lhg-salary-talk) | 薪酬谈判专家：策略到话术演练 | `/plugin install lhg-salary-talk@lhg-plugs` |
| [lhg-biz-report](https://github.com/lhg-plugs/lhg-biz-report) | 商业分析专家：数据到图文报告一键生成 | `/plugin install lhg-biz-report@lhg-plugs` |
| [lhg-study-abroad](https://github.com/lhg-plugs/lhg-study-abroad) | 留学文书专家：PS推荐信多轮打磨 | `/plugin install lhg-study-abroad@lhg-plugs` |
| [lhg-meal-plan](https://github.com/lhg-plugs/lhg-meal-plan) | 营养食谱专家：测算到一周食谱+采购单 | `/plugin install lhg-meal-plan@lhg-plugs` |
| [lhg-competitor](https://github.com/lhg-plugs/lhg-competitor) | 竞品分析专家：五维框架+对比矩阵+SWOT+差异化建议报告 | `/plugin install lhg-competitor@lhg-plugs` |
| [lhg-social-ops](https://github.com/lhg-plugs/lhg-social-ops) | 社媒运营专家：定位→日历→分发策略→复盘，策略+复盘闭环 | `/plugin install lhg-social-ops@lhg-plugs` |
| *（后续插件在此追加，保持表格格式一致）* | | |

## 自检与反馈

本插件自带质检：每次使用后可跑 `python3 smoke_test.py` 一键验证（JSON 合法、skill/command/agent 完整性、11 条规则、fixtures 命中、hooks 行为）。

发现 bug 或有改进建议，以 `[QC] <一句话问题>` 为标题提交到 https://github.com/lhg-plugs/lhg-social-ops/issues，正文写清"复现步骤 → 实际表现 → 期望表现"。

## 出品：刘洪光

本插件由真人出镜 IP「刘洪光」（安徽合肥）出品，归属 [lhg-skills](https://github.com/lhg-skills)。

- GitHub 主页：https://github.com/lhg-skills —— 全部 skill 开源在此，欢迎 star
- 视频号：搜「刘洪光实名上网」
- 微信：lhgsmsw
