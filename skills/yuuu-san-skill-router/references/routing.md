# 常见分流

遇到重叠时按任务目的选用。技能名称以当前实际清单为准，候选增加时用其正文核对适用范围。

## 需求、排障和审查

用户点名用于处理任务的技能优先。用户明确要求圆桌或多代理复核既有决策或交叉审查代码时，用 `yuuu-san-roundtable`。用户点名圆桌排障时，沿用圆桌内的排障流程。未指定技能时按下表选用。

| 任务 | 选择依据 |
| --- | --- |
| 方向讨论、既有决策复核或方案、路书和规格复查 | 用雨伞圆桌（`yuuu-san-roundtable`）。讨论方向走头脑风暴，复核既有决策走决策审核，复查方案、路书和规格走文档审查。按需用 `grilling` 对齐关键取舍。 |
| 需要边确认业务术语边落文档 | 推荐显式调用 `grill-with-docs`，它依赖 `grilling` 和 `domain-modeling`。单独梳理术语与决策时参考 `domain-modeling`，依据现有词表、契约和决定记录，在用户要求的范围内更新。 |
| Bug 排查，包括偶发失败和性能回退 | 用雨伞循环（`yuuu-san-loop`）组织定位、已授权的修复、验证和独立复查。用户只要求定位或只读检查时，交付定位证据、核实结果和验证缺口。Godot、Android 和浏览器等专项技能按需取证。GitHub PR 中的 Actions 检查失败时，用 `gh-fix-ci` 核对日志与失败证据，修复遵守专项和项目的授权要求。回归优先用项目已有入口，要求测试先行时用 `tdd`。雨伞循环不可用时，用 `diagnosing-bugs` 推进并说明独立复查缺口。 |
| 改模块接口或提高可测试性 | 用 `codebase-design` 判断接口该暴露什么、测试从哪里进入。用户要扫描现有仓库并找架构改进候选时，推荐显式调用 `improve-codebase-architecture`。调查范围和重构授权以当次任务为准。 |
| 审查差异或处理 GitHub PR 评论 | 普通代码审查按实际差异和需求。处理 GitHub PR 评论用 `gh-address-comments`。指定 Orca worker 时查 `orchestration`，Orca 工作树和终端操作查 `orca-cli`。 |
| 改技能、接续会话、交接成果 | 技能设计用 `skill-creator`，规则写作按需参考 `writing-for-agents`。需要独立交接文件时推荐显式调用 `handoff`，要求在聊天里交接时直接整理。同一任务继续推进时沿用已有状态和产物。 |

## 界面、工具和交付格式

| 任务 | 选择依据 |
| --- | --- |
| 界面设计与实际验收 | 已采用雨伞设计的项目优先用其项目设计规范和 `huanianji-design:huanianji-design`。通用新 UI 设计或体验精修按现有分工选 `frontend-design` 或 `impeccable`。Godot 实现、React 性能、Android 权限各用对应专项。用户指定 EditHere 时用 `edithere` 收集批注。 |
| 浏览器或原生应用操作与取证 | 浏览器业务流程优先项目既有测试，按需用 Playwright。需要查看请求、控制台、页面性能时优先 Chrome DevTools。原生应用需要 GUI 操作时选环境匹配的 Computer Use。排查实际故障时按 Bug 排查项选择主技能，由这些工具辅助取证。 |
| 表格、文档、幻灯片或互动图 | 用户指向正在打开的 Excel 工作簿时选 `spreadsheets:excel-live-control`，执行前核实连接与目标。独立表格文件用 `spreadsheets:Spreadsheets`。Word、PDF、幻灯片按目标格式处理。对话里的交互图与模拟用可视化技能。 |
