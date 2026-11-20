# 常见分流

遇到重叠时按任务目的选用。技能名称以当前实际清单为准，候选增加时用其正文核对适用范围。

## 需求、排障和审查

用户明确要求圆桌或多代理参与排障、头脑风暴、既有决策复核、方案或路书审查、代码交叉审查时，优先用 `yuuu-san-roundtable`。圆桌排障直接使用该技能内的排障手册。下表也列出单代理排障的入口与圆桌可按需使用的专项工具。

| 任务 | 选择依据 |
| --- | --- |
| 重要方案还有业务决定待定 | 只讨论时用 `grilling` 对齐关键取舍。用户要边确认术语边落文档时，推荐显式调用 `grill-with-docs`，它依赖 `grilling` 和 `domain-modeling`。用户要求梳理业务术语与决策时，参考 `domain-modeling`，依据项目现有词表、契约和决定记录，在用户要求的范围内更新。 |
| 已发生的异常、偶发失败或性能回退 | `diagnosing-bugs` 负责定位和验证。Godot、Android、浏览器或 CI 的专项技能按需取证。回归优先用项目已有入口。用户或项目要求测试先行时用 `tdd`。有明确改法的局部修复可以直接做必要验证。 |
| 改模块接口或提高可测试性 | 用 `codebase-design` 判断接口该暴露什么、测试从哪里进入。用户要扫描现有仓库并找架构改进候选时，推荐显式调用 `improve-codebase-architecture`。调查范围和重构授权以当次任务为准。 |
| 审查差异或 GitHub 问题 | 普通代码审查按实际差异和需求。处理 GitHub PR 评论用 `gh-address-comments`，排查 GitHub Actions 失败用 `gh-fix-ci`。指定 Orca worker 时查 `orchestration`，Orca 工作树和终端操作查 `orca-cli`。 |
| 改技能、接续会话、交接成果 | 技能设计用 `skill-creator`，规则写作按需参考 `writing-for-agents`。需要独立交接文件时推荐显式调用 `handoff`，要求在聊天里交接时直接整理。同一任务继续推进时沿用已有状态和产物。 |

## 界面、工具和交付格式

| 任务 | 选择依据 |
| --- | --- |
| 界面设计与实际验收 | 已采用雨伞设计的项目优先用其项目设计规范和 `huanianji-design:huanianji-design`。通用新 UI 设计或体验精修按现有分工选 `frontend-design` 或 `impeccable`。Godot 实现、React 性能、Android 权限各用对应专项。用户指定 EditHere 时用 `edithere` 收集批注。 |
| 网页或应用排查 | 浏览器业务流程优先项目既有测试，按需用 Playwright。需要查看请求、控制台、页面性能时优先 Chrome DevTools。原生应用需要 GUI 操作时选环境匹配的 Computer Use。 |
| 表格、文档、幻灯片或互动图 | 用户指向正在打开的 Excel 工作簿时选 `spreadsheets:excel-live-control`，执行前核实连接与目标。独立表格文件用 `spreadsheets:Spreadsheets`。Word、PDF、幻灯片按目标格式处理。对话里的交互图与模拟用可视化技能。 |
