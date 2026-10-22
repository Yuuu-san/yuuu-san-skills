# yuuu-san-skills

Codex 全局协作规则与自创技能，用于版本管理、跨设备迁移及后续分享。

## 内容

- `codex/AGENTS.md`：全局协作规则。
- `skills/yuuu-san-roundtable/`：多代理头脑风暴、交叉审查及配套参考文件。

## 当前状态

本仓库从本机现用文件复制建立。全局规则已去除个人称呼和项目专用章节，保留初学者沟通偏好；圆桌技能及配套文件保持原样。项目专用技能由各自项目维护，不纳入本仓库。

仓库文件与本机现用文件是独立副本，编辑任一处不会自动同步另一处。

## 换设备后安装

### 1. 获取仓库

新设备需要先安装 Codex 和 Git。本仓库公开，下载不需要登录 GitHub；向本仓库推送修改仍需要相应的写入权限及 GitHub 身份认证。

在准备存放仓库的目录打开终端，执行：

```sh
git clone https://github.com/Yuuu-san/yuuu-san-skills.git
cd yuuu-san-skills
```

需要从新设备推送更新时，可安装 GitHub CLI（`gh`），运行 `gh auth login` 和 `gh auth setup-git` 配置认证；也可以使用已经配置好的 SSH 或 Git 凭据管理器。

如果已经下载过仓库，在仓库目录执行：

```sh
git status --short
git pull --ff-only origin main
```

先确认 `git status --short` 没有输出；有本地改动时先处理，不继续拉取或覆盖。`--ff-only` 表示只接受可以直接向前更新的版本；如果失败，先核对分支和改动，不使用强制覆盖。

### 2. 确认安装位置

下表中的 `~` 表示当前用户的主目录。Windows 可在资源管理器地址栏输入 `%USERPROFILE%` 打开主目录；macOS 可在 Finder 的“前往文件夹”中输入路径。

| 仓库内的内容 | macOS / Linux 默认安装位置 | Windows 默认安装位置 |
| --- | --- | --- |
| `codex/AGENTS.md` 文件 | `~/.codex/AGENTS.md` | `%USERPROFILE%\.codex\AGENTS.md` |
| `skills/yuuu-san-roundtable/` 整个目录 | `~/.agents/skills/yuuu-san-roundtable/` | `%USERPROFILE%\.agents\skills\yuuu-san-roundtable\` |

全局规则的位置以 Codex 实际使用的 `CODEX_HOME` 为准；未自定义时才使用上表的 `.codex`。如果该目录存在 `AGENTS.override.md`，Codex 会优先使用它；先核对其用途，不能仅复制 `AGENTS.md` 就认为规则已经生效。

新设备按上表安装技能。已有设备可能仍从 `~/.codex/skills/` 加载圆桌技能：先在 Codex 中查看该技能的实际文件路径，更新现有位置即可；不要同时在新旧位置放置两份同名技能。若要迁移，先备份并移出旧副本，再安装到新位置，最后确认技能只出现一次。

Windows 原生 Codex 与 WSL 内的 Codex 使用各自的用户目录；使用哪个环境，就安装到哪个环境的主目录，不默认两边共享配置。

安装位置依据官方文档：[AGENTS.md 的发现规则](https://learn.chatgpt.com/docs/agent-configuration/agents-md)、[本地技能的加载位置](https://learn.chatgpt.com/docs/build-skills)。

### 3. 备份后复制

以下操作用文件管理器即可完成，不需要复制整个 `.codex` 目录。

1. 先查看并备份目标设备原有的 `AGENTS.md` 和 `yuuu-san-roundtable` 目录。备份放到仓库及技能扫描目录之外，例如在“文稿”或“文档”中建立带日期的备份文件夹。需要保留的本机偏好先合并，不能直接丢弃。
2. 将仓库的 `codex/AGENTS.md` 复制到上表的规则位置；缺少父目录时先创建。目标处保留一个 `AGENTS.md` 文件。
3. 将仓库的 `skills/yuuu-san-roundtable` **整个目录**复制到技能父目录下。已有旧技能时，先把旧目录完整移到备份处，再复制新目录，避免旧版本已移除的文件残留。不要只复制 `SKILL.md`，也不要把新目录套在旧目录里面。

安装后的技能结构应为：

```text
yuuu-san-roundtable/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── brainstorming.md
    └── cross-review.md
```

### 4. 确认生效

安装后新建一个 Codex 会话。技能未出现时重启 Codex，再检查安装位置。

- 请 Codex“列出当前加载的全局规则来源，确认是否包含初学者沟通偏好”，并核对来源是目标设备上安装的文件。
- 在技能列表中确认能找到 `yuuu-san-roundtable`，并核对实际文件路径。需要测试运行时，可输入“请用 $yuuu-san-roundtable 比较两个简单方案，完成讨论即可，不修改文件”。

圆桌运行需要当前环境提供真实子代理能力；能找到技能不等于该环境能完成多代理讨论。没有该能力时，应明确说明限制，不能把单代理结果称为已完成圆桌。

## 修改本机文件后同步到仓库

日常流程为：**修改本机现用文件 → 验证效果 → 将通用改动同步到仓库 → 审阅差异 → 提交并上传**。本机文件和仓库文件是独立副本，不会自动同步。

### 1. 先更新仓库

在本仓库目录执行：

```sh
git status --short
git pull --ff-only origin main
```

同样先确认工作区没有未处理改动，再执行拉取。多台设备轮流修改时，每次开始同步前都先拉取，减少相互覆盖。

### 2. 同步全局规则的通用改动

用编辑器并排查看本机实际生效的 `AGENTS.md` 和仓库的 `codex/AGENTS.md`，只把需要共享的改动合并到仓库。

**不要直接用本机 `AGENTS.md` 覆盖仓库版本。** 本机文件可能包含个人称呼、本机绝对路径、项目入口和其他仅对当前设备适用的信息。本仓库继续保留初学者沟通偏好，但不加入这些本机内容；项目规则由对应项目维护。

### 3. 同步圆桌技能

先确认本机正在使用的技能目录，可能位于 `.agents/skills/` 或旧环境的 `.codex/skills/`。

将本机圆桌技能的正式文件同步到仓库 `skills/yuuu-san-roundtable/`，包括 `SKILL.md`、`agents/`、`references/` 及实际新增的必要文件。要完整替换时，先将仓库中的旧技能目录移到仓库外备份，再复制本机版本；不要把旧备份、运行日志、临时文件或凭据一起带进仓库。

只同步圆桌技能，不复制整个技能父目录；项目专用技能继续跟随各自项目，不加入本仓库。只改了规则或只改了技能时，仅执行对应部分。

### 4. 审阅、提交、上传

先查看具体差异：

```sh
git status --short
git diff -- codex/AGENTS.md skills/yuuu-san-roundtable/
```

`git diff` 不显示尚未被 Git 跟踪的新文件内容；`git status` 出现新增文件时，也要打开查看。确认没有个人信息、本机路径、凭据和项目专用内容，再暂存指定范围：

```sh
git add -- codex/AGENTS.md skills/yuuu-san-roundtable/
git diff --cached --check
git diff --cached
```

最后一条会展示本次实际准备提交的全部内容。若修改了 README，另执行 `git add -- README.md`，再检查一次暂存差异。不要使用 `git add .` 将无关文件一起提交。

新设备首次提交前，应在该仓库配置自己的 Git 提交身份；推荐使用 GitHub 账户提供的隐私邮箱，避免将个人邮箱写入提交历史。先将下面两个占位值替换为自己的用户名和 GitHub 隐私邮箱，再执行；`--local` 仅设置当前仓库：

```sh
git config --local user.name "你的 GitHub 用户名"
git config --local user.email "你的 GitHub 隐私邮箱"
```

身份配置完成后提交并上传：

```sh
git commit -m "更新全局规则与圆桌技能"
git push origin main
git status --short --branch
```

提交说明按实际修改内容填写。上传成功后，工作区应没有未提交改动，分支也不应显示领先或落后。若推送被拒绝，先保存本地提交，获取并合并其他设备的更新、核对冲突后再推送，不执行强制推送。

### 5. 让其他设备使用新版本

在其他设备的仓库目录执行 `git pull --ff-only origin main`，然后按上面的“备份后复制”步骤重新安装。**拉取仓库只更新仓库副本，不会自动更新 Codex 正在使用的文件。** 目标设备若有独有改动，先比较、保留或合并后再安装。

## 收录边界与验证范围

仅收录通用全局规则与圆桌技能，不迁移账号登录态、API 配置、聊天记录、个人记忆或其他运行数据。本仓库不提供自动安装或自动同步脚本。

安装位置已依据上述官方文档核对；尚未在其他设备实际安装验证，Windows 与 WSL 的步骤也尚未在目标环境实测。

## 许可证

本仓库的全局规则、圆桌技能、配套配置及说明文档采用 [MIT License](LICENSE)。允许使用、修改、商用和再分发，复制或分发本仓库内容时须按许可证要求保留版权与许可声明；无需公开衍生作品的源码。

版权声明使用公开账号名 `Yuuu-san`。技能中列出的外部参考项目遵循各自的许可证，本仓库的 MIT 授权不替代它们的授权。
