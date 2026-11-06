# Codex 接任说明：深度学习课程、WSL / VS Code、Python 工具链与 Git 学习

> 整理日期：2026-10-16  
> 目的：交给 Codex 在后续对话或代码协助中作为背景。**这是一份按主题整理的交接摘要，而不是逐字聊天记录。**  
> 来源：用户与 ChatGPT 的本轮对话，以及用户在本轮对话中上传的课程模板 `d2l-starter.zip`。明确区分用户已确认的状态、课程模板的已核对内容和有待检查的实际机器状态。

## 0. 给接任 Codex 的首要指示

用户正在从接近零计算机基础开始学习大学课程《动手学深度学习》，希望在学习过程中逐步获得帮助。**不要默认用户了解终端、路径、文件系统、Python 解释器、虚拟环境、包、依赖、版本控制、Git 分支等术语。** 对新命令应说明：在哪种终端运行（PowerShell 还是 Ubuntu Bash）、需要先进入哪个目录、命令作用、预期输出、是否会改变文件、失败时如何验证。一次讲一个小概念，并尽量用用户现有的 `d2l-lab` 项目示例。用户会主动提出细节问题，能接受准确、严谨的解释；数学部分可以讲得更严谨，不必用过度通俗化替代正式定义。

用户目前的主环境是 **Windows + WSL 2 Ubuntu + VS Code Remote WSL**，项目通常在 Ubuntu 的 `/home/huawei/d2l-lab`。用户反馈已经将 WSL 从 C 盘迁移到 D 盘；因此不要再假设虚拟磁盘位于 C 盘，更不要建议手动剪切 `ext4.vhdx`。

如果进行任何改动项目、依赖、Git 历史、远程上传或删除文件的操作：**先告知影响并确认目标**，优先给只读检查命令；避免不必要的 `git reset --hard`、`git clean -fd`、`rm -rf` 或重建整个 WSL。

## 1. 学习背景与课程

- 课程：《动手学深度学习》，上海交通大学数学科学学院开设；用户本学期正在上课。
- 讲义材料主页（地址以后可能调整）：https://zheng-ai-by-hand.netlify.app/deep-learning-ai/materials/
- 此前浏览时，课程按 48 学时、约 15 章讲义组织，含 Python 开发环境、NumPy、数学与优化基础、线性回归、神经网络、卷积网络、注意力/Transformer、语言模型、RAG、工具调用等内容和 Notebook 实验。章节结构以网站最新内容为准。
- 课程原本预设学生有一些 Python 基础，而用户明确表示“从零开始，几乎没有计算机常识”，所以需**补齐课程默认略过的计算机入门知识**。
- 用户尤其希望能够理解工具的工作机制，而不仅是复制命令，例如：`uv run` 的启动过程、`.venv` 的隔离机制与空间占用、Git 如何比较文件、WSL 文件系统与 Windows 的关系、VS Code 的本地/远程配置等。
- 学习指导原则：把数学概念、Python 代码、环境操作三者分开讲，并说明它们如何联系。避免一次灌输过多术语；可以先给最短可执行步骤，再解释细节。

## 2. 用户机器与开发环境：已知状态

### 已确认 / 用户明确反馈

1. 用户使用 Windows，已安装 **WSL 2 的 Ubuntu**。
2. 已通过 **VS Code 连接 WSL: Ubuntu**，在 VS Code 中操作 Ubuntu 终端和 Linux 项目目录。
3. Ubuntu 用户主目录为 `/home/huawei`，课程项目为 `/home/huawei/d2l-lab`（本轮截图与命令中反复使用）。
4. 已安装并使用 `uv`；首次曾执行 `uv run pyproject.toml`，uv 先准备好了虚拟环境和依赖，随后因为 `pyproject.toml` 不是可执行程序而失败。终端当时显示使用 **CPython 3.12.15**、创建 `.venv`、安装约 95 个依赖包。未来应以现场命令确认当前版本。
5. 已操作过 Git 初始化、暂存、提交；对话后段截图显示项目中至少出现过 `Initial commit` 和 `2 nd` 两条提交记录（**实际现在有几条，以 `git log --oneline` 为准**）。
6. 用户有 GitHub 账号；Windows 安装了 **GitHub Desktop**。曾请求练习把 Windows 桌面的一个普通文件夹发布到 GitHub，已获操作指引，但**没有确认练习是否真正执行完毕**。
7. 用户后来问过把整个 WSL 迁移到 D 盘的办法，得到相关命令指导后回复“OK。完成。”；可以认为用户报告**迁移已完成**，但没有提供最终实际路径或迁移日志。
8. 用户熟悉了在 PowerShell 和 Ubuntu Bash 中分别运行命令的概念，仍是初学阶段。

### 不确定，切勿猜测

- 目前 WSL 的确切发行版注册名、存储目录、默认用户与最新软件版本。
- Git 用户名/邮箱究竟如何设置，以及当前 `d2l-lab` 是否已有远程 `origin`。
- GitHub Desktop 的演示仓库是否已发布到 GitHub。
- 当前工作树是否干净、是否有尚未提交的改动。
- WSL 中是否已经为 GitHub 设置 SSH / HTTPS 认证；Windows GitHub Desktop 的登录**不会自动保证** WSL Git 已认证。
- PyTorch 是否已经安装。**课程第一课模板明确不含 PyTorch**，以后训练阶段再安装。

## 3. WSL、Linux 文件系统、Windows 互访

- WSL 2 通过轻量虚拟化运行 Linux，Ubuntu 的 Linux 文件系统通常保存在 Windows 上一个 `ext4.vhdx` 虚拟硬盘文件内。Windows 文件夹看起来只含少数文件，并不意味着 Ubuntu 系统内只有少数文件。
- Linux `/home` 是存放用户目录的上级目录；当前用户的 Home 是 `/home/huawei`，`~` 通常指这里。项目推荐放 `/home/huawei/d2l-lab` 等 Linux 文件系统路径，避免主要在 `/mnt/c/...` 上开发产生的性能/权限差异。
- Windows 文件资源管理器可通过 `\\wsl$\Ubuntu\home\huawei` 或 `\\wsl.localhost\Ubuntu\home\huawei` 访问；发行版名称需核实。在 **Ubuntu 终端**执行 `explorer.exe .` 可以打开当前目录的 Windows 资源管理器窗口。
- **Ubuntu → Windows** 路径典型映射为 `/mnt/c/Users/...`，Windows 盘符如 D 盘通常为 `/mnt/d/...`；可以用 `cp` 复制文件。
- 不要通过 Windows 资源管理器直接修改或移动 `ext4.vhdx`；迁移发行版要使用 WSL 支持的正式迁移/导出办法。
- 迁移到 D 盘只改变 Linux 虚拟磁盘在 Windows 上的存储位置，Linux 内部 `/home/huawei/d2l-lab` 路径应保持不变。

## 4. Ubuntu 终端与 VS Code 入门进度

用户已学：

| 命令/概念 | 用户已了解的基本含义 |
|---|---|
| `pwd` | 显示当前工作目录 |
| `ls` | 查看目录里的文件 |
| `cd dirname` | 进入子目录 |
| `cd ..` | 进入上级目录 |
| `cd ~` | 返回用户 Home |
| `cd /` | 到 Linux 文件系统根目录 |
| `cd -` | 回到上一个工作目录 |
| `explorer.exe .` | 在 Windows 资源管理器打开 Ubuntu 当前目录 |
| `code .` | 让 VS Code 打开当前目录（可能复用或新开窗口） |

已解释 VS Code 界面：左侧文件树属于 **Explorer（资源管理器）**；从 `File > Open Folder` 修改当前打开的根文件夹；集成终端的 `cd` 不会改变 VS Code Explorer 的根目录。VS Code 连 WSL 后新建集成终端默认通常为 Linux 终端，但可手动选 PowerShell。

还讨论了 VS Code 配置/扩展的“本地 Windows vs 远程 WSL”区别：Windows 运行图形界面；某些开发扩展安装在 WSL 并在其扩展宿主中运行，主题/UI 扩展通常在本地；用户设置一般共享，Remote Settings 可覆盖 WSL，工作区还可有 `.vscode/settings.json`。不要说“完全同一套”，也不要说“全部分离”。

## 5. Python、uv、项目模板：准确内容

用户曾在本轮对话上传 `d2l-starter.zip`，其中包含 `d2l-lab/` 目录。已经直接核对压缩包的结构和配置。注意：**这是上传时的模板，并不保证本机项目自上传之后未被修改**。

```text
d2l-lab/
├── README.md
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
├── main.py
├── tests/test_baseline.py
├── .vscode/settings.json
├── .vscode/extensions.json
└── .zed/settings.json
```

`pyproject.toml` 核心内容：

```toml
[project]
name = "d2l-lab"
version = "0.1.0"
requires-python = ">=3.12,<3.13"
dependencies = ["numpy>=2,<3"]

[dependency-groups]
dev = ["ruff>=0.11,<1", "pytest>=8,<10", "jupyterlab>=4,<5", "ipykernel>=6,<8"]

[tool.ruff]
target-version = "py312"
line-length = 88
```

- `.python-version` 内容为 `3.12`。
- `main.py` 用 NumPy 计算均方误差 MSE；数组 `target=[9.,11.]`, `baseline=[4.,4.]`，预期输出 `Baseline MSE: 37.0`，并打印 Python 路径、NumPy 版本。
- `tests/test_baseline.py` 中有 **3 个测试**：手算 MSE、数组维度不匹配时报错、空数组时报错。
- `.gitignore` 包括 `.venv/`、`__pycache__/`、`.pytest_cache/`、`.ruff_cache/`、`.ipynb_checkpoints/`、`.env`、`.env.*`、`data/`、`outputs/`。缓存（cache）是完整英语单词，不是缩写。`.ipynb_checkpoints` 更接近 Notebook 检查点而非普通性能缓存。
- `.vscode/extensions.json` 推荐 Python、Pylance、Jupyter、Ruff 插件。
- `.vscode/settings.json` 配置了 `${workspaceFolder}/.venv` 解释器路径、Ruff 格式化器和保存时格式化。

课程模板 README 的验证命令（**在项目根目录内的 WSL Ubuntu 终端运行**）：

```bash
cd ~/d2l-lab
uv sync --locked
uv run --locked main.py
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked pytest -q
uv run --locked jupyter lab
```

项目预期是 MSE=37.0、3 个 pytest 测试通过；项目 README 说明第一课不需要立即下载 PyTorch。

此前解释过的关键点：

- **Python** 是语言/解释器，**uv** 管理 Python 版本、依赖、环境和项目，**Ruff** 做 lint/格式化，**pytest** 做自动测试。
- `pyproject.toml` 是项目配置文本，`uv.lock` 是具体依赖解析与版本锁定结果，`.venv/` 是项目的 Python 虚拟环境文件夹。虚拟环境不是另一台完整虚拟机。
- `uv run pyproject.toml` 会先检查项目配置和同步环境，然后试图执行一个叫 `pyproject.toml` 的命令，最终失败；`uv run --locked python main.py` 或 `uv run --locked main.py` 才正确。
- `--locked` 只要求现有 `uv.lock` 与项目配置一致，禁止自动更新锁文件；省略后可能在必要时解析并更新锁文件，并不是每次都重新安装全部包。
- `uv run python --version` 查项目实际运行的 Python 版本；`uv --version` 查 uv 版本；`uv run python -c "import sys; print(sys.executable)"` 查 Python 解释器实际路径。
- `uv add <package>` 会修改 `pyproject.toml`、`uv.lock` 和环境；课程项目中不要为试验随意添加依赖。
- 不同项目各有 `.venv`，不因名字相同而冲突。Python 解释器可通过符号链接复用；uv 有全局包缓存。**不保证相同依赖在 ext4 上只占用一份磁盘空间**，要留意具体缓存链接/复制策略。
- Ruff 常用安全检查：`uv run --locked ruff check .` 和 `uv run --locked ruff format --check .`；真正执行 `ruff format .` 会修改文件。

## 6. Git 已学知识与本地进度

用户已经理解以下概念，仍需要实际操作巩固：

- Git 是**本地可用**的分布式版本控制工具；GitHub 是基于 Git 的远程代码托管协作平台，2018 年被微软收购。`git commit` ≠ `git push`。
- `git init` 在目录创建 `.git/`；**不自动生成提交**；`.gitignore` 规定忽略规则（主要影响尚未跟踪的文件）。
- 工作区（working tree）：磁盘当前文件；暂存区（index/staging area）：准备提交的版本；提交（commit）：仓库内固定历史对象。`Ctrl+S` 将编辑器内容写到磁盘；`git add` 更新暂存区；`git commit` 生成历史提交。
- VS Code 中 `main.py（索引）` 是只读的暂存区文件视图，非固定的最后一次提交。
- Git 对是否修改的判断基于当前版本与暂存区/提交的文件内容、路径、相关属性；删除再重建同路径、同内容、同相关模式的文件，最终可视为未变。Git Blob 保存字节内容，Tree 记录名称/路径/模式，Commit 指向目录树并记录历史关系。Git 不理解 Python 代码“语义是否相同”。
- `git log --oneline`：每个提交一行；`HEAD -> main` 表示 HEAD 指向当前 main 分支，main 指向某个提交。
- Git 首次提交需配置 `user.name` 和 `user.email`；可以使用本地练习值，不要求真实邮箱或 GitHub 登录，但公开仓库注意隐私；WSL Ubuntu 与 Windows Git 的 global 配置通常分开。
- 用户在 VS Code 首次提交时遇到 `COMMIT_EDITMSG` 编辑器，因首行为空、其余注释行以 `#` 开头，提交信息为空而未完成。之后已完成 `Initial commit`。`.git/COMMIT_EDITMSG` 是 Git 的标准临时提交说明文件，不是版本历史的存放处；`MSG` 是 Message 缩写。
- 后来截图有两次提交：`Initial commit` 和 `2 nd`。实际当前提交历史需重新查看。
- 恢复文件到暂存区版本：`git restore main.py`（默认是从暂存区到工作区）。恢复第一次提交中的文件：先用 `git log --oneline` 获取真实 ID，再用 `git restore --source=<commit-id> -- main.py`（只更新工作区）。如需同时恢复整个项目的已跟踪文件与暂存区，应特别说明 `--staged --worktree` 的影响；会覆盖未提交改动。普通 `git restore` 不保证清理未跟踪文件。

常用只读检查命令：

```bash
cd ~/d2l-lab
git status
git log --oneline
git diff
git diff --cached
git remote -v
```

GitHub Desktop：用户在 Windows 有 GitHub 账号和 GitHub Desktop，曾询问如何将桌面示例文件夹上传。此前教过 `File > Options > Accounts` 登录、`File > Add Local Repository` 添加普通文件夹（无仓库时 `Create a repository here`）、`Commit to main`、`Publish repository` 并勾选 `Keep this code private`。**尚无用户确认发布成功**；若要继续，应先检查具体状态，而非假设已完成。

## 7. 本地仓库与远程仓库：已解释、待实践

- Local Repository 是本机仓库；Remote Repository 是外部服务器上的仓库，例如 GitHub；GitHub 非唯一远程托管平台。
- `git remote -v` 查看配置；`git remote add origin <URL>` 设置别名；`git push` 上传本地提交；`git fetch` 获取远程更新但不整合当前分支；`git pull` 获取并整合；`git clone` 克隆远程仓库。
- 本地 commit 可以离线进行。远程不会因为本地 commit 自动同步。
- Windows GitHub Desktop 登录与 WSL Git 的身份验证要分别检查。
- 若用户下一步想让 `d2l-lab` 推送至 GitHub：先 `git status`、`git remote -v`、确认是否已有云端仓库及其内容；不要盲目 `git push --force` 或覆盖有历史的远程分支；引导为课程项目设置合适的私有仓库，检查 `.gitignore`、Notebook 输出、密钥等。

## 8. 后续回答时的操作规范

1. 命令要标注环境：例如 **“在 Windows PowerShell 输入”** 或 **“在 VS Code 的 WSL Ubuntu 终端输入”**。
2. 出现路径时解释 Windows 的 `C:\...`、`D:\...` 与 Linux 的 `/home/...`、`/mnt/d/...` 的映射。
3. 分清“保存编辑器文件 / Git 暂存 / Git 提交 / Git 推送”四个完全不同的动作。
4. 不要以为用户知道 `package`、`dependency`、`kernel`、`interpreter`、`shell`、`repository`、`branch` 等概念；首次出现时给一句中文解释与例子。
5. 不要过度重复已教过的内容，用户如果只问具体命令或英文词的意思，优先简短回答，再视需要给例子。
6. 涉及 Git 或格式化工具可能覆盖改动时，先运行 `git status`（必要时 `git diff`），确认未保存改动；不要建议无解释的强制重置。
7. 如果 WSL 因 D 盘迁移出现问题，应先核实 `wsl --list --verbose`、`wsl --version` 和相关发行版实际状态，不要重新安装/注册导致数据风险。
8. 用户通过提问来逐步了解原理，适宜提供“命令 → 发生什么 → 如何验证 → 为什么”的小循环。
9. 如访问课程网站，应核实更新后的讲义内容。若只是回答当前环境概念，可直接基于此文件答复，不必每次联网。

## 9. 给 Codex 的建议接任起手式

如果用户继续学习，先依据具体提问回答；若需要摸清当前 `d2l-lab` 的状态，可以请他从 **WSL Ubuntu 终端**提供下面的**只读输出**（无需一次跑完全部）：

```bash
cd ~/d2l-lab
pwd
uv --version
uv run python --version
git status
git log --oneline -5
git remote -v
```

**不要在没有新需求时擅自重装 Python、重新生成 uv.lock、改 Git 历史、移动 WSL 或执行远程推送。** 用户当前最重要的是形成正确的计算机基础概念，之后逐步完成课程实验。
