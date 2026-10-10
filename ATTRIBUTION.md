# 灵感来源与致谢（Attribution）

本插件的**方法论灵感**来自以下优秀的开源项目，**所有实现代码、检测规则与文案均为原创**，未复制任何第三方的原文案。

| 项目 | 作者 / 组织 | 许可 | 链接 | 借鉴了什么思路 |
|---|---|---|---|---|
| claude-code-social-skills | AINightCoder | 未声明（思路借鉴） | https://github.com/ainightcoder/claude-code-social-skills | 多平台社媒 skill 的拆分思路（按平台拆 skill）与"执行层走浏览器自动化"的定位；本插件与其**互补而非重复**——它做执行层分发，本插件做策略+复盘，**未复制其任何代码与文案** |
| claude-social-media-skills | michaellady | 未声明（思路借鉴） | https://github.com/michaellady/claude-social-media-skills | buffer-stats / audit-buffer-queue / tune-posting-schedule 的"数据复盘闭环"思想（发→看数→调排期）；本插件 lhg-so-review 的四段式复盘与"复盘回写日历"受其启发，**方法论与文案均为原创** |
| superpowers | Jesse Vincent（obra） | MIT | https://github.com/obra/superpowers | SDLC 硬门方法论；本插件自动发布拦截的硬门思想受其启发 |
| impeccable | Paul Bakaus（Renaissance Geek） | Apache-2.0 | https://github.com/pbakaus/impeccable | "确定性检测规则 + 规则引擎"的架构思想；本插件审计脚本的规则注册表模式受其启发，**规则条目全部自研** |

## 声明

1. **借鉴思路，实现与文案均为原创**：以上项目的具体文案、规则原文、代码实现均未被复制。本插件的 skill 方法论文案、审计规则、命令流程均为独立撰写。
2. **许可合规**：上述 MIT / Apache-2.0 许可项目允许在保留声明的前提下进行思路借鉴与二次创作。本文件即为保留声明的一部分。未声明许可的项目仅做思路借鉴，未复制其任何受保护表达。
3. **商标与归属**：各项目名称与作者署名归其各自所有者所有。

## 本插件自身的许可

本插件原创部分采用 MIT 许可（见 `LICENSE` 文件），版权所有：刘洪光（https://github.com/lhg-skills）。
