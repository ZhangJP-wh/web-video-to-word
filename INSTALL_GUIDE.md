# 网页视频转语音识别文字稿（由千问提供支持）

## 先安装：电脑小白从这里开始

你不需要学编程。最省事的方式是把仓库链接交给**自己电脑上能操作终端和文件的 AI Agent**，让它完成安装；普通聊天窗口只有文字回复，不能代替你操作电脑。

| 你的电脑 | 安装入口 | 验证状态 |
| --- | --- | --- |
| Apple 芯片 Mac（M1/M2/M3/M4 等） | 首次安装.command / bash install.sh | 已在现有 Mac 实测安装和启动 |
| Windows 11，64位 x64（常见 Intel/AMD PC） | install-windows.cmd / install-windows.ps1 | GitHub Windows runner 完整安装/启动验收通过；尚未在全新实体 Windows 11 电脑实测 |
| Intel Mac、Windows 10、Windows ARM/32位、WSL/Linux | 暂无 | 暂不支持自动安装 |

### 方法一：把这一段复制给你电脑上的 Agent（推荐）

> 请把 https://github.com/ZhangJP-wh/web-video-to-word 安装到我的电脑固定目录。先读 README 和安装源码，确认系统支持。Mac 运行 `bash install.sh --open`；Windows x64 运行 `powershell -NoProfile -File .\install-windows.ps1 -Open`。自动安装缺失环境、依赖和 Chromium，运行全部测试和 pip check，启动服务并检查 /health。系统授权/密码及千问登录/验证码让我本人处理。不关闭系统安全、脚本策略或 TLS 校验，不读取日常浏览器 Cookie，不安装本地 ASR，不上传私人资料。失败时按指南修复后重跑；Windows 脚本策略阻止时改用文档的手动 Python 兜底。

**你要做的只有：**把这段话交给 Agent，等待下载和验收，按需确认系统安装授权，最后本人登录千问。Windows 环境齐全时可以接近一键完成；缺环境时使用 WinGet 安装，安装许可和必要的系统授权仍可能需要本人确认。

### 方法二：没有 Agent，自己点几下

1. 点击本页面上方绿色 **Code → Download ZIP**。
2. 下载后“解压缩/全部提取”到一个固定目录，例如 Windows 的 `C:\VideoToWord`，或 Mac 的用户文件夹。不要在压缩包内运行，不要放到受保护的系统目录，安装后不要移动目录。
3. **Mac：**双击 `首次安装.command`。**Windows：**双击 `install-windows.cmd`。保持网络连通，等待依赖、浏览器和测试完成。首次耗时取决于网速，没有固定分钟数。
4. 看到“服务启动及 /health 检查通过”并打开本机网页，即本机安装验收完成。默认地址为 **http://127.0.0.1:8767/**。该地址只在安装工具的这台电脑上使用。
5. 在网页标题旁点击蓝色 **“登录或打开千问”**，在专用窗口中本人登录，处理验证码，完成后关闭登录窗口。Agent 不需要你的密码或 Cookie。
6. 选择一个你有权处理的短音视频文件，或粘贴视频链接，点击橙色 **“开始生成文稿”**。Word 保存到用户“下载”文件夹中的“网页视频转语音识别文字稿（由千问提供支持）”。
7. 下次使用：Mac 双击 `启动工具.command`；Windows 双击 `start-windows.cmd`。重启电脑后要重新启动工具；Windows 当前不自动设置开机启动。

Windows 版本支持范围依据 [Playwright 官方系统要求](https://playwright.dev/python/docs/intro#system-requirements)。Windows Server 2019+ 可用于自动化验收；普通用户优先使用 Windows 11 x64。

### Windows：缺环境、被阻止或安装失败怎么办

- **缺 Python/Node：**入口自动检测 Python 3.12 x64 和 Node.js 22+ x64；使用已有 WinGet 从明确的 `winget` 来源安装 `Python.Python.3.12`（当前用户）与 `OpenJS.NodeJS.LTS`。不安装本地语音模型。授权提示或安装许可由本人处理。
- **没有 WinGet：**到 [Python 3.12.10 官方页面](https://www.python.org/downloads/release/python-31210/) 下载 **Windows installer (64-bit)**，安装时勾选“Add python.exe to PATH”；到 [Node.js 官方页面](https://nodejs.org/en/download) 安装 **22+ LTS Windows x64**。重新打开终端，再重跑安装入口。
- **提示不允许运行 PowerShell 脚本：**不要运行 `Set-ExecutionPolicy`、`-ExecutionPolicy Bypass` 或关闭安全软件。环境安装好后，在项目文件夹地址栏输入 `cmd` 回车，在命令提示符粘贴 `py -3.12 -X utf8 install.py --open`，直接走 Python 兜底。如果 `py` 不存在，改用已安装 Python 3.12 的完整路径。公司电脑的策略限制需由本人联系管理员。
- **WinGet 安装成功但仍提示找不到环境：**关闭终端，重新打开后重跑入口；脚本也会刷新常见 PATH。
- **端口已占用：**Agent 可用 `powershell -NoProfile -File .\install-windows.ps1 -Port 8768 -Open`，以后使用 `start-windows.cmd -Port 8768`。入口不强制停止其他软件。
- **下载失败：**先恢复网络，再重跑入口。完整报错在终端；服务日志 `work/app.log` 仅在本机查看，不公开上传。
- **不要双击 Mac 的 .command 文件：**Windows 使用上面的 .cmd / .ps1 或 Python 入口。无需 WSL、Git Bash 或开发者模式。

### Mac：环境缺失和手动兜底

优先支持原生 Apple Silicon Mac、Python 3.12、arm64 Node.js 22+。Intel Mac 和 Rosetta 终端不支持 Mac 安装入口；Windows 使用上面的独立入口。首次下载需要网络；尚未在另一台全新 Mac 完成从零安装实测。

### 自己安装

1. 点击 **Code → Download ZIP**，解压到固定位置。不要从压缩包内部运行，也不要在安装后移动目录。
2. 双击“首次安装.command”（同 `bash install.sh --open`）。若 Gatekeeper 阻止，在 Finder 对信任的文件右键打开并遵循系统提示，不关闭系统安全保护。
3. 安装器自动检查 macOS/arm64、Python 3.12、Node.js 22+；若已有 `/opt/homebrew/bin/brew`，使用它安装缺失环境，不使用 sudo。Homebrew 自身报错时按其输出处理，再重跑入口。
4. 没有 Homebrew 且缺环境时，安装器一次给出一个明确的“下一步”：安装官方 Python 3.12 macOS universal2 包，或 Node.js 22+ LTS macOS ARM64 包，然后重跑。必要的安装包系统授权由本人完成，不自动安装 Homebrew。
5. 验收完成后网页会打开。点击“登录或打开千问”，本人完成登录/验证码。健康检查只验证本机服务，不能证明千问登录有效或云端转写成功。

入口依次创建/修复 `.venv`（损坏环境重命名为 `.venv.backup-*`，不删除资料）、安装 requirements、pip check、安装 Playwright Chromium、真实启动一次无登录的 Chromium、运行全部测试，再后台启动服务并等待最多30秒验证 `/health`。任何步骤失败都会停止，不报告安装成功。可重复运行；不会停止其他进程或覆盖其他副本的服务。端口占用时使用 `bash install.sh --port 8768 --open`，今后以同端口启动。

常用命令：

```bash
bash install.sh                 # 安装、验收并启动，适合无交互 Agent
bash install.sh --no-start      # 安装和验收，不启动
bash install.sh --start-only --open  # 启动已安装工具并验证；不重新安装依赖
```

双击“启动工具.command”使用默认8767端口。自动登录 Mac 后启动仍为自选功能：双击“启用自动启动.command”，不是首次安装必需步骤。

### 手动兜底和故障处理

可自行安装 [Python 3.12 universal2](https://www.python.org/downloads/release/python-31210/) 和 [Node.js 22+ LTS ARM64](https://nodejs.org/en/download)，然后执行 `python3.12 install.py --open`。安装器使用 macOS 系统证书，保持 HTTPS 验证；若官方 Python 的证书未配置，可运行 Applications/Python 3.12/Install Certificates.command 后重试。已有 Node 的终端 PATH 必须能找到它；`install.sh` 自动加入常见官方及 Homebrew 路径。

安装失败保留终端具体报错；网络下载中断后重跑入口。服务失败时仅在本机查看 `work/app.log`，不要公开上传可能包含任务信息的日志。损坏 venv 的备份可在确认新环境正常后由本人清理。不要删除 `work`，其中有任务和千问专用登录资料。

更新前先停止当前服务（自动启动版本先运行“停用自动启动.command”），备份自己的 work 资料，再更新源码并重跑安装器；需要时重新启用自动启动。朋友电脑不会因 GitHub 更新自动升级。其他副本占用端口时，安装器拒绝复用，不强制关闭。

### 什么算安装完成，什么仍要本人操作

安装器自动检查系统与版本，创建或修复 venv，安装 requirements 和 Playwright Chromium，真实启动一次无登录浏览器，运行全部测试与 pip check，后台启动服务并验证 `/health` 的安装目录及仅 qianwen 引擎。任何一步失败都会停止，不会假报成功。

千问登录/验证码、系统授权，以及 Windows 安装包可能要求的许可确认仍由本人处理。健康检查不代表千问已登录，也不代表一次真实云端转写成功。文件锁、进程管理、FFmpeg 和“打开文档所在位置”已增加 Windows 兼容；自动启动的 launchd 命令仍只适用于 Mac。


## 工具说明


粘贴视频网页链接，工具在 Mac 后台下载音轨，上传到已登录的千问音视频速读，导出完整原文并生成 Word。仅使用千问云端识别，不安装或使用本地语音模型。

## 使用流程

1. 首次安装后，双击“配置千问登录.command”，在专用窗口登录千问，返回终端按回车。
2. 双击“启动工具.command”，打开终端给出的本机网页地址。公开安装版默认为 http://127.0.0.1:8767/。
3. 可点击或拖拽本地音视频文件到上传入口（每次一个，最大6GB），或粘贴 YouTube、哔哩哔哩等视频页面链接，点击橙色“开始生成文稿”。任务添加成功后链接框自动清空，可继续粘贴下一条；提交失败时保留链接。链接输入框关闭浏览器历史自动填充。
4. 稍后回来查看文稿，或点击“打开文档所在位置”。任务记录最新的排在最上面。

本地文件与链接共用橙色“开始生成文稿”按钮，选择文件会清空链接，输入链接会取消文件选择。上传仅复制文件，完成后清理工具副本，不删除用户原文件。千问登录、原文、发言人和时间戳设置沿用现有流程。每份 Word 第一行保留原视频网页链接（本地上传则注明来源文件名），按视频标题或本地文件名命名，包含全部识别原文、时间戳和发言人信息。显著提示：

> 本文稿内容为语音模型识别结果，需要注意：可能有错别字和识别不准确之处。

所有文稿直接保存在 `~/Downloads/网页视频转语音识别文字稿（由千问提供支持）/`，不建立任务二级文件夹。完成文档结构和内容完整性检查后，原下载媒体移入废纸篓，临时音轨清理。程序检查不代表人工确认识别准确率。本工具不生成总结。

## 登录与删除

页面上有标题旁蓝色“登录或打开千问”按钮。识别任务检测到登录失效后显示需要重新登录；点击按钮登录、关闭登录窗口，再点击重试。空闲时不保证实时发现过期，也不会主动抢占屏幕。 首次使用会提示可能未登录；上传或确认上传失败时，在保留具体错误的同时提示可能未登录，建议点击“登录或打开千问”确认后重试。明确的存储或额度限制仍显示原原因，不误报为登录失效。

已完成任务的“删除任务并同步到千问”与“查看 Word 文稿”“打开文档所在位置”同排，不再提供重复下载按钮。每条任务的“删除任务并同步到千问”会停止该任务，将相关本机文件、已完成和未完成 Word、任务记录移入废纸篓；点击“删除任务并同步到千问”会删除对应千问记录，云端删除后无法恢复。删除结果逐项列出工具任务记录、本机文稿及任务文件、对应千问记录，每项成功显示绿色、失败显示红色；千问记录未找到而按成功处理时显示绿色并注明情况。绿色成功提示在卡片消失后显示3秒自动清空；红色失败提示保留；失败原因保留在任务卡片并随刷新显示。成功删除后任务卡片立即从工具列表消失，旧的刷新结果不会把卡片重新显示。云端删除失败则保留本机任务和文稿，提示原因后可重试；未上传的任务只清理本机。仅删除含本工具任务编号且唯一匹配的记录，千问未找到对应记录时仍清理本机，整体按成功处理，并明确注明未找到、未执行云端删除；多个匹配记录或页面/登录异常仍视为失败。模型和登录信息不会上传 GitHub。

后台启动识别进程失败会显示具体失败原因，不会一直停在排队状态；个别任务记录异常不会停止后续队列。

## 上传成功确认

只有千问页面显示本次文件名对应的记录后，才标记上传确认成功。点击确认不再被当作成功依据。等待记录最多2分钟，期间保存页面诊断。没有确认时停止并保留音频，不自动重复上传；需检查页面后再恢复。记录存在也不等于转写完成。

## 运行状态

状态对应实际步骤：下载、提取音频、准备上传音频、连接千问、上传、等待千问结果、导出原文、生成并检查 Word、清理媒体、完成。没有千问内部进度数据时，只显示等待结果，不断言云端正在识别。Word 生成后清理结束或记录清理错误，才显示完成。

## 故障恢复加固

页面加载超时会自动重试，最多3次；复用已经提交的千问任务和保存的文稿链接，不重复上传。登录失效立即提示用户，不自动反复尝试登录。导出菜单等待可见及选项完整后才操作。加载异常保留媒体和页面诊断，文稿验证失败不清理源文件。工具会显示千问页面明确可见的错误提示（如上传失败、额度不足、服务异常），保留文件供重试；未明确报错时不推断原因。千问提示云端存储已满时立即停止并保留本机音频；请用户自行清理千问记录后重试，同步删除按钮可清理对应云端记录。自动恢复不能保证第三方改版、网络中断或服务限额永不影响任务。

## HTTPS 证书

下载依赖 certifi 的可信证书。已将 certifi 列为必需组件并保留，清理旧模型时不会移除；不关闭 HTTPS 证书校验。若下载出现 CERTIFICATE_VERIFY_FAILED，请在项目中执行 `.venv/bin/python -m pip install -r requirements.txt` 恢复依赖后重试。

## 抖音链接

精选页中包含数字 modal_id 的链接会转换成 /video/视频编号 供下载器使用，Word 保留用户原链接。抖音仍可能要求有效浏览器 Cookie 并拒绝自动下载；转换链接不保证成功。当前页面没有抖音登录配置，不读取日常浏览器 Cookie，不绕过访问限制。

## 无声视频

下载文件如果没有音轨，不能做语音识别。工具明确提示并保留媒体；如果网页播放有声音，请提供有声音的版本。工具不会把画面上的文字当作语音识别结果。

## 限制与隐私

这是独立开源工具，“由千问提供支持”表示语音识别使用千问网页服务，不表示千问官方出品或合作授权。

音频上传千问服务器。后台浏览器使用自己的本机登录目录，不读取用户日常浏览器 Cookie。千问页面改版、登录验证、服务额度、网络故障可能导致任务暂停。网页免费政策由服务方决定，本项目不保证永久免费或不限量。

当前按千问页面限制处理单文件：最长 6 小时、音频最大 500MB；超过限制会提示失败。默认选择中英文自由说、不翻译、多人讨论，其他语言需要适配。下载能力由 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 决定，不保证支持所有网页，不绕过付费或 DRM，请处理有权使用的媒体。

## 安装验收与验证范围

Windows 的 PowerShell 完整入口、Chromium 下载/启动、全部测试、pip check、服务健康检查和重复启动已经通过 [GitHub 自动化验收](https://github.com/ZhangJP-wh/web-video-to-word/actions/runs/37684113530)。runner 预置了 Python/Node，因此 WinGet 缺环境安装、本人登录千问和实体新电脑安装不属于这次自动化验收。

安装入口运行 `test_reader test_app test_qianwen test_task_controls test_install test_runtime_compat` 全部测试及 pip check。安装器回归覆盖错误架构/Node版本、损坏环境保留与修复、符号链接保护、依赖失败中止、错误服务身份拒绝和正确服务复用。千问单元测试使用模拟结果，不调用用户账号。

需要验证云端完整流程时，由用户提供获授权的短音频，本人登录后检查千问原文、Word、来源链接、提示、发言人、时间戳及媒体清理。此项涉及用户内容，不属于安装器自动测试。不得把任务记录、个人文稿、音视频、work、.venv、Cookie 或缓存提交仓库。

本次具体验证结果见 `验证记录.json`。另一台全新 Mac、全新实体 Windows 电脑、官方安装包授权、WinGet 和 Homebrew 缺环境安装分支仍需要独立实测，不能承诺所有新电脑无人干预安装。

## 主要文件

`app.py` 网页服务；`reader.py` 下载与 Word；`qianwen_browser.py` 千问后台浏览器；`task_controls.py` 删除任务；`install.sh` 统一环境入口；`install.py` 安装和健康验收；`requirements.txt` 依赖；`INSTALL_GUIDE.md` 含完整源码的安装指南。

自包含安装指南由 `tools/build_guides.py` 从公开源码重建，Markdown 和 Word 同步维护。

本项目采用 MIT 许可证，第三方组件遵循各自许可证。

失败或需要重新登录的任务提供黄色背景、深色文字的“重试任务”按钮。

页面声明浅色 color-scheme，仅影响本页面；独立 Chrome 应用窗口的原生右键菜单仍需实际确认，不保证由网页样式控制。

删除操作采用持久化后台队列：千问浏览器被识别或登录占用时显示等待、空闲后自动执行；关闭页面不取消，服务重启后恢复。重复点击不重复排队；新识别任务让待删除操作优先。等待超过6小时或真实错误时明确提示失败并保留文件。已有运行服务需加载本次更新后生效。

### 千问多页面与登录提示
后台共用一个专用 Chromium 浏览器和登录资料，每个操作使用独立页面，最多两个转写任务并行；删除使用另一个后台页面，同一任务先停止再删除。千问自身的配额和并发限制仍会如实显示。登录状态每分钟检查，验证成功显示“已登录千问”，失效显示“需登录千问”并弹窗提醒；无法验证显示“正在验证登录”。登录窗口需要在当前浏览器操作结束后打开。首次启用请运行“加载本次更新.command”。

更新前已启动的旧任务会继续使用旧浏览器连接；等待其结束后再打开登录窗口。占用、验证失败和未登录会分别提示，不把浏览器占用误报为安装环境错误。本机浏览器控制连接不经过网络代理。

### 查看后台状态与旧版切换
标题旁的湖蓝色“显示任务状态”按钮打开只读状态窗口，显示任务阶段、错误、记录更新时间、登录状态和共享浏览器实际页面截图，每3秒刷新。关闭窗口不停止任务。没有页面截图时明确说明，更新时间不是转写进度。旧版本任务占用浏览器时，可运行“修复浏览器占用并加载更新.command”：核实并停止占用本工具浏览器的旧 reader，保留本地媒体和千问提交记录，再恢复任务；不删除或重置登录资料。切换后需实测千问任务恢复。

B站下载兼容：可选播放接口仅返回访问验证凭据时，保留公开网页已有的播放地址；不会绕过登录、付费或观看权限。网页本身也没有地址时，明确提示下载失败，尚未上传千问。

补充下载重试：B站播放接口只有验证信息时，有限重读公开播放器网页，核对 cid 后提取已有媒体地址，避免误取其他分集。已验证两条失败样例的完整音频下载和解码；这不代表千问转写已完成。

千问Word导出：共享浏览器下载被取消时，使用该次导出事件的原始URL，在同一已登录页面读取文件；验证Word结构后保存。重试复用已保存的千问文稿链接，避免重复上传。

### 固定任务编号与文稿排序
任务按添加顺序分配永久递增编号，标题及Word文件名显示“1 - 视频标题”。删除留空号，重试保留原编号；新任务继续递增，不复用编号。工具列表和Mac文稿文件夹均按编号倒序（Finder按名称倒序，自然数字排序）；尚未完成任务没有Word文件，所以文件夹只包含列表的已完成部分。编号账本位于私人work目录，勿删除以免丢失连续编号。现有任务按添加时间补编号。用户手动切换Finder排序会影响显示，可重新选择名称倒序。

工具Logo采用蓝色圆角底板、红色播放符号与黄色便签图案；网页标题左侧和Mac独立应用Dock共用该图案。更新Mac图标后退出并重新打开独立应用即可加载，后台任务继续运行。

最新图标原始包：[MacAppIcon.zip](icons/MacAppIcon.zip)，包含 macOS ICNS 与各尺寸 PNG。网页标志高度为标题字号的 2.5 倍（以蓝色图案的可见边缘为准，补偿透明留白与阴影），与标题第一行底部对齐；登录状态和显示任务状态按钮位于第二行。

## 仅收到本文档：完整源码

AI Agent 可按 FILE 标记逐个提取文件，再核对文件校验.json；运行 `bash install.sh`。仅提取这里列出的公开源码，不迁移他人的登录资料。

### FILE: .gitignore
```text
.venv/
work/
outputs/
__pycache__/
*.pyc
.DS_Store
.env
.env.*
*cookie*
*.log

.venv.backup-*/
```

### FILE: app.py
```text
"""Loopback-only background transcription and Word export."""
import os
import hashlib
import html
import json
import queue
import re
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, unquote

from runtime_compat import venv_python
from reader import ROOT, WORK, OUTPUT, LEGACY_OUTPUT, NOTICE, save_json, download_url

HOST = '127.0.0.1'
PORT = int(os.environ.get('VIDEO_READER_PORT', '8767'))
tasks = queue.Queue()
pending = set()
mutex = threading.Lock()
generations = {}
cancelled = set()
login_process = None
active_readers = {}
deletion_queue = None
deletion_queue_lock = threading.Lock()

def get_deletion_queue():
    global deletion_queue
    with deletion_queue_lock:
        if deletion_queue is None:
            from deletion_queue import DeletionQueue
            def failed(ident,error):
                folder=WORK/'jobs'/ident
                meta=json.loads((folder/'job.json').read_text()) if (folder/'job.json').exists() else {}
                report=deletion_report(False,meta.get('qianwen_delete_result','deleted' if meta.get('qianwen_cloud_deleted') else 'failed'),error)
                if folder.exists():
                    (folder/'.deleting').unlink(missing_ok=True)
                    save_json(folder/'delete-result.json',report)
                return report
            def stop_target(ident):
                from task_controls import reader_pids,stop_reader
                with mutex:
                    generation=generations.get(ident)
                    if generation:cancelled.add((ident,generation))
                    for pid in reader_pids(ROOT,WORK/'jobs'/ident):stop_reader(pid)
            deletion_queue=DeletionQueue(WORK,delete_task,failed,stop_target)
            deletion_queue.start()
        return deletion_queue


def document_path(ident):
    job = WORK / 'jobs' / ident
    meta = json.loads((job / 'job.json').read_text(encoding="utf-8"))
    path = Path(meta.get('document', '/nonexistent')).resolve()
    migrated = OUTPUT / path.name
    if path.parent in (OUTPUT.parent / '网页视频转语音文稿', OUTPUT.parent / '网页视频转语音识别文字稿') and migrated.is_file():
        path = migrated.resolve()
    if not any(root.resolve() in path.parents for root in (OUTPUT, LEGACY_OUTPUT, ROOT / 'outputs', OUTPUT.parent / '网页视频转语音文稿', OUTPUT.parent / '网页视频转语音识别文字稿')) or not path.is_file():
        raise ValueError('文档不存在')
    return path


def preview_document(ident):
    from docx import Document
    doc = Document(document_path(ident))
    parts = []
    for paragraph in doc.paragraphs:
        text = html.escape(paragraph.text)
        if paragraph.style.name == 'Title':
            parts.append(f'<h1>{text}</h1>')
        elif paragraph.style.name.startswith('Heading'):
            parts.append(f'<h2>{text}</h2>')
        elif paragraph.text == NOTICE:
            parts.append(f'<p class=notice>{text}</p>')
        else:
            parts.append(f'<p>{text}</p>')
    return ('''<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>查看文稿</title>
<style>body{max-width:850px;margin:40px auto;padding:0 24px;font:18px/1.9 -apple-system,sans-serif;color:#24322d}p{white-space:pre-wrap;overflow-wrap:anywhere}a{color:#245441}h1{font-size:30px}.notice{background:#fff3cd;color:#9c0006;font-weight:bold;padding:16px;border-left:4px solid #b07800}</style>'''
            + f'<a href="/">返回任务列表</a> · <a href="/document/{ident}" download>下载 Word</a>'
            + '<main>' + ''.join(parts) + '</main></html>').encode()


def reveal_document(ident):
    path = document_path(ident)
    if os.name == 'nt':
        os.startfile(str(path.parent))
        return
    result = subprocess.run(['/usr/bin/open', '-a', 'Finder', str(path.parent)],
                            capture_output=True, text=True, timeout=15)
    if result.returncode:
        raise ValueError('Mac 未能打开 Finder。请从 Finder 双击启动文件，在正常环境中重启网页服务后再试。')



def fetch_title(ident, url):
    """Resolve metadata independently of the sequential transcription queue."""
    try:
        result = subprocess.run(
            [str(venv_python(ROOT)), '-m', 'yt_dlp', '--skip-download',
             '--no-playlist', '--ignore-no-formats-error', '--no-warnings',
             '--socket-timeout', '8', '--retries', '0', '--print', 'title', download_url(url)],
            capture_output=True, text=True, timeout=40)
        title = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else ''
        if result.returncode or not title or title == 'NA':
            return
        with mutex:
            path = WORK / 'jobs' / ident / 'job.json'
            meta = json.loads(path.read_text(encoding="utf-8"))
            # Active reader owns job.json. Separate metadata avoids competing writes.
            save_json(path.parent / 'page-title.json', {'title': title, 'url': url})
    except (OSError, ValueError, subprocess.SubprocessError):
        pass


def start_title_lookup(ident, url):
    threading.Thread(target=fetch_title, args=(ident, url), daemon=True).start()


def resume_jobs():
    # After restarting the web service, leave an existing reader process running.
    for item in sorted(list_jobs(), key=lambda item: item['created_at']):
        if item.get('state') not in ('completed', 'failed', 'login_required') and not (WORK/'jobs'/item['id']/'.deleting').exists():
            pending.add(item['id'])
            generation=__import__('uuid').uuid4().hex
            generations[item['id']]=generation
            tasks.put((item['id'], item['url'], generation))
            if not item.get('title'):
                start_title_lookup(item['id'], item['url'])

def task_created_at(folder):
    marker = folder / '.prepare.lock'
    path = marker if marker.exists() else folder
    stat = path.stat()
    return getattr(stat, 'st_birthtime', stat.st_mtime)


def list_jobs():
    from task_numbering import numbers
    numbering=numbers(WORK)
    items = []
    for path in (WORK / 'jobs').glob('*/job.json'):
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
            item['id'] = path.parent.name
            item['task_number']=numbering[item['id']]
            deletion=path.parent/'delete-result.json'
            if deletion.exists():item['deletion_result']=json.loads(deletion.read_text(encoding="utf-8"))
            title_path = path.parent / 'page-title.json'
            if not item.get('title') and title_path.exists():
                item['title'] = json.loads(title_path.read_text(encoding="utf-8")).get('title')
            item['created_at'] = item.get('created_at', task_created_at(path.parent))
            item['has_document'] = bool(item.get('document') and Path(item['document']).is_file())
            items.append(item)
        except (ValueError, OSError):
            pass
    return sorted(items,key=lambda item:item['task_number'],reverse=True)


def worker():
    while True:
        ident, url, generation = tasks.get()
        log=None
        try:
            folder = WORK / 'jobs' / ident
            from runtime_compat import file_lock as fcntl
            if (ident,generation) in cancelled or not folder.exists():continue
            with (folder / '.prepare.lock').open('a') as lock:
                while True:
                    if (ident,generation) in cancelled or not folder.exists() or (folder/'.deleting').exists():break
                    try:
                        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        fcntl.flock(lock, fcntl.LOCK_UN)
                        break
                    except BlockingIOError:time.sleep(.2)
            with mutex:
                if (ident,generation) in cancelled or not folder.exists() or (folder/'.deleting').exists():continue
                log=(folder/'run.log').open('ab')
                process=subprocess.Popen([str(venv_python(ROOT)),str(ROOT/'reader.py'),
                     'prepare',url,'--engine',json.loads((folder/'job.json').read_text(encoding="utf-8")).get('engine','qianwen')],
                     stdout=log,stderr=log,start_new_session=True)
                active_readers[ident]=(process,generation)
            result=process.wait();log.close()
            if result==0:(folder/'run.log').unlink(missing_ok=True)
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            record=WORK/'jobs'/ident/'job.json'
            if record.exists() and (ident,generation) not in cancelled:
                try:
                    meta=json.loads(record.read_text(encoding="utf-8"))
                    meta.update(state='failed',error='后台任务未能启动或任务记录异常：'+str(error))
                    save_json(record,meta)
                except (OSError,ValueError):pass
        finally:
            if log is not None:log.close()
            with mutex:
                if generations.get(ident)==generation:
                    pending.discard(ident);generations.pop(ident,None)
                cancelled.discard((ident,generation))
                if active_readers.get(ident,(None,None))[1]==generation:active_readers.pop(ident,None)
            tasks.task_done()


def deletion_report(success, cloud_status, error=''):
    cloud={'deleted':'删除成功','not_uploaded':'无需删除：此任务未上传到千问',
           'not_found':'未找到对应千问记录，未执行云端删除；本机清理按成功处理'}
    local='删除成功' if success else '未删除成功，任务已保留'
    files='删除成功（已移入废纸篓）' if success else ('未全部删除成功，请检查并重试' if cloud_status in cloud else '未执行删除，文件已保留')
    elements=[{'label':'工具任务列表记录','detail':local,'status':'success' if success else 'failed'},
              {'label':'本机文稿及任务文件','detail':files,'status':'success' if success else 'failed'},
              {'label':'对应的千问记录','detail':cloud.get(cloud_status,'删除失败：'+error),'status':'success' if cloud_status in cloud else 'failed'}]
    message=('删除成功' if success else '删除失败')+'\n'+'\n'.join(e['label']+'：'+e['detail'] for e in elements)
    if not success and cloud_status in cloud:message+='\n失败原因：'+error
    return {'status':'success' if success else 'failed','message':message,'elements':elements,'at':time.time()}


def delete_task(ident):
    from task_controls import trash_task, stop_reader
    with mutex:
        generation=generations.get(ident)
        if generation:cancelled.add((ident,generation))
        process=active_readers.get(ident,(None,None))[0]
        if process and process.poll() is None:stop_reader(process.pid)
        folder=WORK/'jobs'/ident
        (folder/'.deleting').touch()
        try:
            # Also stop readers recovered after a web-service restart.
            from task_controls import reader_pids
            for pid in reader_pids(ROOT,folder):stop_reader(pid)
            from runtime_compat import file_lock as fcntl
            with (folder/'.prepare.lock').open('a') as lock:
                deadline=time.monotonic()+15
                while True:
                    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);break
                    except BlockingIOError:
                        if time.monotonic()>deadline:raise ValueError('任务尚未停止，请稍后重试删除')
                        time.sleep(.2)
                result=subprocess.run([str(venv_python(ROOT)),str(ROOT/'qianwen_browser.py'),'delete','--job',ident],capture_output=True,text=True,timeout=120)
                if result.returncode:raise ValueError('千问同步删除失败，本机任务和文稿已保留：'+(result.stderr.strip().splitlines()[-1] if result.stderr.strip() else '后台浏览器未能完成删除'))
        except Exception as error:
            (folder/'.deleting').unlink(missing_ok=True)
            meta=json.loads((folder/'job.json').read_text(encoding="utf-8"))
            if meta.get('state') not in ('completed','failed','login_required'):
                meta.update(state='failed',error='任务已停止，千问同步删除未完成：'+str(error))
                save_json(folder/'job.json',meta)
            raise
        cloud_meta=json.loads((folder/'job.json').read_text(encoding="utf-8"))
        cloud_status=cloud_meta.get('qianwen_delete_result','deleted' if cloud_meta.get('qianwen_cloud_deleted') else 'failed')
        result=trash_task(ROOT,WORK,[OUTPUT,LEGACY_OUTPUT,ROOT/'outputs',OUTPUT.parent/'网页视频转语音文稿'],ident)
        pending.discard(ident);generations.pop(ident,None)
        result['deletion_result']=deletion_report(True,cloud_status)
        result['message']=result['deletion_result']['message']
        return result


auth_check_process = None
auth_check_started = 0

def login_status():
    global auth_check_process,auth_check_started
    if time.time()-auth_check_started>60 and (auth_check_process is None or auth_check_process.poll() is not None) and not (login_process and login_process.poll() is None):
        auth_check_started=time.time()
        with (WORK/"qianwen-auth-check.log").open("ab") as log:
            auth_check_process=subprocess.Popen([str(venv_python(ROOT)),str(ROOT/"qianwen_browser.py"),"check-auth"],stdout=log,stderr=log,start_new_session=True)
    path=WORK/'qianwen-auth.json'
    state=json.loads(path.read_text(encoding="utf-8")) if path.exists() else {'status':'unknown'}
    if not state.get('last_success'):
        successes=[item.get('added_at',0) for item in list_jobs() if item.get('state')=='completed' and item.get('model')=='qianwen-web']
        if successes:state['last_success']=max(successes)
    state['window_open']=bool(login_process and login_process.poll() is None)
    result_path=WORK/'qianwen-login-result.json'
    if login_process and login_process.poll() not in (None,0):
        result=json.loads(result_path.read_text(encoding='utf-8')) if result_path.exists() else {}
        state['error']=result.get('error','千问登录窗口未能打开，请重试；若仍失败请检查登录错误记录。')
    return state


def open_login():
    global login_process
    with mutex:
        if login_process and login_process.poll() is None:return {'ok':True,'message':'登录窗口已经打开。'}
        (WORK/'qianwen-login-result.json').unlink(missing_ok=True)
        with (WORK/'qianwen-login.log').open('ab') as log:
            login_process=subprocess.Popen([str(venv_python(ROOT)),str(ROOT/'qianwen_browser.py'),'login-ui'],
                                           stdin=subprocess.DEVNULL,stdout=log,stderr=log,start_new_session=True)
    return {'ok':True,'message':'正在打开千问登录窗口；登录完成后关闭该窗口即可。'}


def enqueue(url, engine="qianwen"):
    if engine != "qianwen":
        raise ValueError("不支持的语音识别方式")
    ident = hashlib.sha256(url.encode()).hexdigest()[:12]
    local = url.startswith('local://') and (WORK/'jobs'/ident/'job.json').is_file()
    if not local and (urlparse(url).scheme not in ('http', 'https') or not urlparse(url).hostname):
        raise ValueError('请输入完整的 HTTP/HTTPS 视频页面链接')
    ident = hashlib.sha256(url.encode()).hexdigest()[:12]
    folder = WORK / 'jobs' / ident
    folder.mkdir(parents=True, exist_ok=True)
    with mutex:
        if ident in pending:
            return ident
        meta = json.loads((folder / 'job.json').read_text(encoding="utf-8")) if (folder / 'job.json').exists() else {}
        if meta.get('state') == 'completed' and Path(meta.get('document', '/nonexistent')).is_file():
            return ident
        from runtime_compat import file_lock as fcntl
        with (folder / '.prepare.lock').open('a') as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                return ident
            (folder/'.deleting').unlink(missing_ok=True)
            meta.setdefault('created_at', task_created_at(folder))
            meta.update(url=url, state='queued', engine=engine)
            meta.pop('error', None)
            save_json(folder / 'job.json', meta)
            from task_numbering import numbers
            numbers(WORK)
        pending.add(ident)
        generation=__import__('uuid').uuid4().hex
        generations[ident]=generation
        tasks.put((ident, url, generation))
        if not meta.get('title') and not local:
            start_title_lookup(ident, url)
    return ident


MEDIA_EXTENSIONS={'.mp4','.mov','.mkv','.webm','.avi','.wmv','.m4v','.flv','.mp3','.wav','.m4a','.aac','.ogg','.flac','.aiff','.wma','.amr','.mpeg','.mpg','.opus'}

def receive_upload(stream, length, original_name):
    """Stream a browser-selected file into an isolated task; never move the user's original."""
    import uuid, shutil
    from reader import filename
    name=Path(original_name.replace('\\','/')).name
    if Path(name).suffix.lower() not in MEDIA_EXTENSIONS:
        raise ValueError('请选择支持的音频或视频文件')
    if not 0 < length <= 6_000_000_000:
        raise ValueError('文件为空或超过 6GB')
    url='local://'+uuid.uuid4().hex
    ident=hashlib.sha256(url.encode()).hexdigest()[:12]
    folder=WORK/'jobs'/ident
    media=folder/'media';media.mkdir(parents=True)
    target=media/(filename(Path(name).stem)+Path(name).suffix.lower())
    try:
        remaining=length
        with target.open('wb') as output:
            while remaining:
                chunk=stream.read(min(1024*1024,remaining))
                if not chunk:raise ValueError('文件上传中断，请重新选择并提交')
                output.write(chunk);remaining-=len(chunk)
        save_json(folder/'job.json',{'url':url,'source_kind':'local','source_label':'本地上传文件：'+name,
            'title':Path(name).stem,'name':filename(Path(name).stem),'media':str(target),
            'state':'queued','engine':'qianwen','created_at':time.time()})
        return enqueue(url)
    except Exception:
        shutil.rmtree(folder,ignore_errors=True)
        raise


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, data, kind='application/json; charset=utf-8'):
        payload = data if isinstance(data, bytes) else json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', kind)
        self.send_header('Content-Length', str(len(payload)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(payload)

    def allowed(self):
        return self.headers.get('Host') in (f'{HOST}:{PORT}', f'localhost:{PORT}')

    def do_GET(self):
        if not self.allowed():
            return self.reply(403, {'error': '仅允许本机访问'})
        if self.path == '/':
            return self.reply(200, (ROOT / 'index.html').read_bytes(), 'text/html; charset=utf-8')
        if self.path == '/manifest.webmanifest':
            return self.reply(200, (ROOT / 'manifest.webmanifest').read_bytes(), 'application/manifest+json; charset=utf-8')
        if self.path == '/icons/app-icon.svg':
            return self.reply(200, (ROOT / 'icons' / 'app-icon.svg').read_bytes(), 'image/svg+xml; charset=utf-8')
        if self.path == '/health':
            return self.reply(200, {'ok': True, 'project': str(ROOT), 'pid': os.getpid(), 'engines': ['qianwen'], 'task_controls': True, 'local_upload': True, 'cloud_delete': True})
        if self.path == '/runtime/status':
            from runtime_status import snapshot
            return self.reply(200,snapshot(ROOT,list_jobs(),login_status()))
        match=re.fullmatch(r'/runtime/page/([0-9]+)',self.path)
        if match:
            path=WORK/'browser-live'/(match.group(1)+'.png')
            if path.exists():return self.reply(200,path.read_bytes(),'image/png')
            return self.reply(404,{'error':'当前没有可显示的页面截图'})
        if self.path == '/qianwen/status':
            return self.reply(200, login_status())
        if self.path == '/jobs':
            return self.reply(200, list_jobs())
        if self.path == '/deletions':
            return self.reply(200, get_deletion_queue().results())
        match = re.fullmatch(r'/(document|preview)/([0-9a-f]{12})', self.path)
        if match:
            kind, ident = match.groups()
            job = WORK / 'jobs' / ident
            if kind == 'preview':
                try:
                    return self.reply(200, preview_document(ident), 'text/html; charset=utf-8')
                except (OSError, ValueError):
                    return self.reply(404, {'error': '文档不存在'})
            try:
                path = document_path(ident)
            except (OSError, ValueError):
                return self.reply(404, {'error': '文档不存在'})
            mime = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            if path.is_file():
                return self.reply(200, path.read_bytes(), mime)
        self.reply(404, {'error': '未找到'})

    def do_POST(self):
        if not self.allowed() or self.headers.get('Origin') not in (f'http://{HOST}:{PORT}', f'http://localhost:{PORT}'):
            return self.reply(403, {'error': '请求来源不符'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if self.path == '/upload':
                self.connection.settimeout(120)
                return self.reply(200, {'id': receive_upload(self.rfile,length,unquote(self.headers.get('X-File-Name','')))})
            if not 0 < length <= 5_000_000:
                raise ValueError('提交内容为空或过大')
            data = json.loads(self.rfile.read(length))
            if not isinstance(data,dict):raise ValueError('提交内容必须是对象')
            if self.path == '/jobs':
                if not isinstance(data.get('url'),str):raise ValueError('请提交有效的网页链接')
                return self.reply(200, {'id': enqueue(data['url'].strip(), 'qianwen')})
            if self.path == '/qianwen/login':
                return self.reply(200, open_login())
            deletion=re.fullmatch(r'/delete/([0-9a-f]{12})',self.path)
            if deletion:
                ident=deletion.group(1)
                try:
                    report=get_deletion_queue().submit(ident)
                except (ValueError,OSError,subprocess.SubprocessError) as error:
                    folder=WORK/'jobs'/ident
                    meta=json.loads((folder/'job.json').read_text(encoding="utf-8")) if (folder/'job.json').exists() else {}
                    cloud_status=meta.get('qianwen_delete_result','deleted' if meta.get('qianwen_cloud_deleted') else 'failed')
                    report=deletion_report(False,cloud_status,str(error))
                    if folder.exists():save_json(folder/'delete-result.json',report)
                    return self.reply(400,{'error':str(error),'deletion_result':report})
                return self.reply(202,{'ok':True,'deletion_result':report})
            match = re.fullmatch(r'/reveal/([0-9a-f]{12})', self.path)
            if match:
                reveal_document(match.group(1))
                return self.reply(200, {'ok': True})
            self.reply(404, {'error': '未找到'})
        except (ValueError, KeyError, OSError, subprocess.SubprocessError) as error:
            self.reply(400, {'error': str(error)})


if __name__ == '__main__':
    (WORK / 'jobs').mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    get_deletion_queue()
    resume_jobs()
    for _ in range(2):threading.Thread(target=worker, daemon=True).start()
    print(f'网页视频转语音识别文字稿（由千问提供支持）：http://{HOST}:{PORT}', flush=True)
    server.serve_forever()
```

### FILE: bilibili_download.py
```text
"""Retry public page playback data when optional Bilibili API has no streams."""
from urllib.parse import urlsplit,parse_qs,urlencode
from yt_dlp.extractor.bilibili import BiliBiliIE
class BiliBiliPageFallbackIE(BiliBiliIE):
    @classmethod
    def ie_key(cls):return 'BiliBili'
    def _real_extract(self,url):
        self.source_url=url
        return super()._real_extract(url)
    def _download_playinfo(self,*args,**kwargs):
        info=super()._download_playinfo(*args,**kwargs)
        if kwargs.get('fatal') is False and info and 'v_voucher' in info and not self.extract_formats(info):
            self.report_warning('B站播放接口没有返回媒体地址，重新读取公开网页中的播放器数据。')
            bvid,cid=args[:2]
            source=getattr(self,'source_url','https://www.bilibili.com/video/'+bvid+'/')
            part=parse_qs(urlsplit(source).query).get('p',['1'])[0]
            for extra in ({'p':part,'t':'0'},{'p':part}):
                page=self._download_webpage('https://www.bilibili.com/video/'+bvid+'/?'+urlencode(extra),bvid,fatal=False)
                if not page:continue
                state=self._search_json(r'window\.__INITIAL_STATE__\s*=',page,'page state',bvid,default={})
                selected=state.get('videoData',{}).get('cid')
                if str(selected)!=str(cid):continue # Never substitute a different episode.
                play=self._search_json(r'window\.__playinfo__\s*=',page,'page playback',bvid,default={}).get('data',{})
                if self.extract_formats(play):return play
            return None # Preserve initial-page data if these pages also lack streams.
        return info

def register(downloader):
    downloader.add_info_extractor(BiliBiliPageFallbackIE())
```

### FILE: browser_service.py
```text
"""One headless browser owner; clients use separate pages over loopback CDP."""
import os,time,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PORT=18769

def endpoint():
    import urllib.request,json
    try:
        # Loopback control traffic must never go through system/environment proxies.
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(f'http://127.0.0.1:{PORT}/json/version',timeout=1) as r:
            data=json.load(r)
        return data['webSocketDebuggerUrl']
    except Exception:return None

def serve():
    from runtime_compat import file_lock as fcntl
    from playwright.sync_api import sync_playwright
    os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH',str(ROOT/'work/browser-bin'))
    with (ROOT/'work/qianwen-browser.lock').open('a') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:return
        with sync_playwright() as p:
            context=p.chromium.launch_persistent_context(str(ROOT/'work/qianwen-browser-profile'),headless=True,accept_downloads=True,viewport={'width':1920,'height':1600},args=[f'--remote-debugging-port={PORT}','--remote-debugging-address=127.0.0.1'])
            live=ROOT/'work/browser-live';live.mkdir(exist_ok=True)
            last_capture=0
            try:
                while True:
                    if time.time()-last_capture>3:
                        pages=[]
                        for i,page in enumerate(context.pages[1:]):
                            try:
                                page.screenshot(path=str(live/(str(i)+'.png')),timeout=1500)
                                pages.append({'index':i,'title':page.title(),'url':page.url})
                            except Exception:pass
                        from reader import save_json
                        save_json(live/'status.json',{'at':time.time(),'pages':pages})
                        last_capture=time.time()
                    for page in context.pages[1:]:
                        session=context.new_cdp_session(page)
                        target=session.send('Target.getTargetInfo')['targetInfo']['targetId'];session.detach()
                        owner=ROOT/'work/browser-page-owners'/target
                        if owner.exists():
                            try:os.kill(int(owner.read_text()),0)
                            except ProcessLookupError:
                                page.close();owner.unlink(missing_ok=True)
                            except (ValueError,PermissionError):pass
                    context.pages[0].wait_for_timeout(1000)
            finally:context.close()
if __name__=='__main__':serve()
```

### FILE: check_recovery.py
```text
"""Controlled launchd recovery check. Run from the normal Mac user environment."""
import argparse
import json
import os
import plistlib
import subprocess
import time
import urllib.request
from pathlib import Path
from launch_service import LABEL
ROOT=Path(__file__).resolve().parent

def health(port):
    with urllib.request.urlopen(f'http://127.0.0.1:{port}/health',timeout=2) as response:
        data=json.load(response)
    if data.get('project')!=str(ROOT):raise ValueError('页面不属于当前项目，停止测试。')
    return data

def reader_pids():
    pids=set()
    for lock in (ROOT/'work/jobs').glob('*/.prepare.lock'):
        result=subprocess.run(['/usr/sbin/lsof','-t',str(lock)],capture_output=True,text=True)
        pids.update(int(value) for value in result.stdout.split())
    return pids

def run(port):
    report={'passed':False,'tested_at':time.time(),'port':port}
    try:
        path=Path.home()/'Library/LaunchAgents'/(LABEL+'.plist')
        config=plistlib.loads(path.read_bytes())
        if config.get('WorkingDirectory')!=str(ROOT) or not config.get('KeepAlive') or not config.get('AbandonProcessGroup'):
            raise ValueError('启动项不匹配或缺少自动恢复设置，未停止服务。')
        before=health(port);report['before_pid']=before['pid']
        readers=reader_pids()-{before['pid']}
        started=time.monotonic()
        result=subprocess.run(['/bin/launchctl','kill','SIGTERM',f'gui/{os.getuid()}/{LABEL}'],capture_output=True,text=True)
        if result.returncode:raise RuntimeError(result.stderr.strip())
        while time.monotonic()-started<45:
            try:
                after=health(port)
                if after['pid']!=before['pid']:
                    report.update(after_pid=after['pid'],recovery_seconds=round(time.monotonic()-started,2))
                    with urllib.request.urlopen(f'http://127.0.0.1:{port}/jobs') as response:
                        report['task_count']=len(json.load(response))
                    for pid in readers:
                        try:os.kill(pid,0)
                        except ProcessLookupError:raise RuntimeError('原识别进程已退出，需要检查是否正常完成。')
                    report.update(passed=True,preserved_reader_pids=sorted(readers));break
            except OSError:pass
            time.sleep(.5)
        if not report['passed']:raise RuntimeError('45 秒内未观察到网页服务恢复。')
    except (OSError,ValueError,RuntimeError) as error:report['error']=str(error)
    finally:
        (ROOT/'work').mkdir(exist_ok=True)
        (ROOT/'work/recovery-test.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not report['passed']:raise SystemExit('测试未通过或未能执行，请保留以上报错。')
    print('自动恢复实测通过，原识别进程保留。')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8767)
    run(parser.parse_args().port)
```

### FILE: cloud_migration.py
```text
"""One-time migration from local ASR to Qianwen; preserves jobs and documents."""
import json,shutil,subprocess,time
from pathlib import Path
from reader import ROOT,WORK,OUTPUT,save_json
from task_controls import reader_pids,stop_reader
OLD=OUTPUT.parent/'网页视频转语音识别文字稿'
def main():
    for folder in (WORK/'jobs').glob('*'):
        record=folder/'job.json'
        if not record.exists():continue
        meta=json.loads(record.read_text())
        if meta.get('engine')!='qianwen' and meta.get('state')!='completed':
            for pid in reader_pids(ROOT,folder):stop_reader(pid)
            meta.update(engine='qianwen',state='queued');meta.pop('error',None)
        if meta.get('document') and Path(meta['document']).parent==OLD:
            meta['document']=str(OUTPUT/Path(meta['document']).name)
        save_json(record,meta)
        reservation=folder/'export-target.json'
        if reservation.exists():
            value=json.loads(reservation.read_text())
            if Path(value['path']).parent==OLD:value['path']=str(OUTPUT/Path(value['path']).name);save_json(reservation,value)
        for item in folder.iterdir():
            if item.name.startswith('checkpoints-') or item.name=='speaker-turns.json':
                if item.is_dir():shutil.rmtree(item)
                else:item.unlink()
    if OLD.exists():
        if not OUTPUT.exists():OLD.rename(OUTPUT)
        else:
            for item in OLD.iterdir():
                dest=OUTPUT/item.name
                if dest.exists():raise RuntimeError('新旧目录有同名文件，已保留，请检查：'+item.name)
                item.rename(dest)
            OLD.rmdir()
    cache=WORK/'model-cache'
    size=sum(p.stat().st_size for p in cache.rglob('*') if p.is_file() and not p.is_symlink()) if cache.exists() else 0
    shutil.rmtree(cache,ignore_errors=True)
    from importlib.metadata import distributions
    from packaging.requirements import Requirement
    normalize=lambda value:value.lower().replace('_','-').replace('.','-')
    installed={normalize(d.metadata['Name']):d for d in distributions()}
    keep=set(); pending=['yt-dlp','python-docx','imageio-ffmpeg','send2trash','ds-store','playwright','pip','setuptools','packaging','certifi']
    while pending:
        name=normalize(pending.pop())
        if name in keep:continue
        keep.add(name)
        if name not in installed:continue
        for spec in installed[name].requires or []:
            requirement=Requirement(spec)
            if requirement.marker is None or any(requirement.marker.evaluate({'extra':extra}) for extra in ('','default')):pending.append(requirement.name)
    packages=sorted(set(installed)-keep)
    subprocess.run([str(ROOT/'.venv/bin/python'),'-m','pip','uninstall','-y',*packages],check=True)
    subprocess.run([str(ROOT/'.venv/bin/python'),'-m','pip','check'],check=True)
    save_json(WORK/'cloud-migration.json',{'ok':True,'removed_model_cache_bytes':size,'output':str(OUTPUT)})
    print('已移除本地模型及推理组件，文稿文件夹已更新。')
if __name__=='__main__':main()
```

### FILE: deletion_queue.py
```text
"""Persistent pending deletions; busy browser is waiting, never a false failure."""
import json,re,threading,time
from pathlib import Path
from reader import save_json
from runtime_compat import file_lock as fcntl

def browser_busy(work):
    from browser_service import endpoint
    if endpoint():return False
    with (Path(work)/'qianwen-browser.lock').open('a') as handle:
        try:
            fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
            fcntl.flock(handle,fcntl.LOCK_UN)
            return False
        except BlockingIOError:return True

def waiting_report():
    elements=[{'label':label,'status':'pending','detail':detail} for label,detail in [
        ('工具任务列表记录','等待同步删除，暂时保留'),('本机文稿及任务文件','等待同步删除，文件已保留'),
        ('对应的千问记录','等待千问浏览器空闲，将自动重试；若登录窗口开着，请关闭该窗口')]]
    return {'status':'pending','message':'删除已加入后台队列，等待千问浏览器空闲后自动执行。','elements':elements,'at':time.time()}

class DeletionQueue:
    def __init__(self,work,delete,failed,on_submit=lambda ident:None):
        self.work=Path(work);self.folder=self.work/'deletion-queue';self.folder.mkdir(parents=True,exist_ok=True)
        self.delete=delete;self.failed=failed;self.on_submit=on_submit
        self.lock=threading.RLock();self.finished={};self.started=False
    def submit(self,ident):
        if not re.fullmatch('[0-9a-f]{12}',ident):raise ValueError('无效任务编号')
        with self.lock:
            job=self.work/'jobs'/ident
            if not (job/'job.json').exists():raise ValueError('任务已不存在，请刷新列表')
            record=self.folder/(ident+'.json')
            if record.exists():return json.loads(record.read_text())['report']
            self.on_submit(ident)
            (job/'.deleting').touch()
            report=waiting_report();save_json(record,{'id':ident,'created_at':time.time(),'report':report})
            save_json(job/'delete-result.json',report);self.finished.pop(ident,None)
            return report
    def has_pending(self):return any(self.folder.glob('*.json'))
    def results(self):
        with self.lock:
            now=time.time();self.finished={k:v for k,v in self.finished.items() if now-v['at']<600}
            result=dict(self.finished)
            for p in self.folder.glob('*.json'):
                try:result[p.stem]=json.loads(p.read_text())['report']
                except (OSError,ValueError):continue
            return result
    def run_once(self):
        for path in sorted(self.folder.glob('*.json'),key=lambda p:p.stat().st_mtime):
            try:
                record=json.loads(path.read_text());ident=record['id']
                if time.time()-record['created_at']>6*3600:raise ValueError('等待千问浏览器空闲超过6小时，请关闭登录窗口后重试删除')
                if browser_busy(self.work):return
                try:report=self.delete(ident)['deletion_result']
                except Exception as error:
                    if '千问浏览器正在使用中' in str(error):
                        (self.work/'jobs'/ident/'.deleting').touch();return
                    raise
            except Exception as error:
                report=self.failed(path.stem,str(error))
            with self.lock:
                self.finished[path.stem]=report;path.unlink(missing_ok=True)
    def start(self):
        with self.lock:
            if self.started:return
            self.started=True
        def loop():
            while True:
                try:self.run_once()
                except Exception:pass # Records persist for the next pass/restart.
                time.sleep(2)
        threading.Thread(target=loop,daemon=True).start()
```

### FILE: index.html
```text
<!doctype html>
<html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>网页视频转语音识别文字稿（由千问提供支持）</title>
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" type="image/png" sizes="32x32" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAJiElEQVR4nJ2XeYxfVRXHP/e+937L/GZ+s7TMdKbr1JmWFijSIpTFWjWgVhIT3IMIAWLEaDTxL2NMqQjGPyAGFwwJYZEYgtawlpaCtGBqCwIGFKGWlhY6023aWX7re3cx573fTJdATHzJ/b33u/e+c8495/s95zz4gOuRR3zwvPeh914Div/78kpkiCyR+UE71On7vfKglFLuzI3r16fGwC3/W+0tolmJqDNkeK83gOeUNXVSt7yTLWzcF69uK0RfdM5egGMWnoKHwHpw3ivnT74szwrlZV7W5dDIPjDW0QR1zGteN1ZvvGGZ2nGmLjU9Ifc7/0ZhaKH7dTFUN+SLiiQBY8CaVKDIbRmbKU71ebDu5Nxp6x60+E1D3IQ4dg+MxPo7G1ZRl61ihJp2+z2vEMyebZ/s7QuuPDGG9dZ5Z6xyaOWCAG8AE+OUToVPx8i5043x08+teXlMrJwRVZ4dBieOuWeK6KtGVmElHPp5CCTmPbPt92f3BVdWjhP3V0eDHlMPdRAFZWf02Uf+qQca4zqIclpZtDNoY1U6rFfaobRv3WXInJU5lEapoLuowihUwbHDJi506SvHEr63QSm3fhuBoFTdA2HfgfjttnJu4YIdm1m66z7dKC9mx6d+xPKX7mfO6E5MzyB7z/0Cu+dfxFTsSYzBao0EbyY0ZOGQkXrHwyVzNe3K8efdnkIe58OQStXudUmwbMNarJY4dO9hYaj0wuoEuvTSds17o+RffZnCrpdoe/s1/IRB7z/Akud+yyU77mVOPEWYi9DG4YxPFRoHsYVEnn12v7BfMz+X8JtnxzheF5gpFTe99jBYiRvzhQ0ptSxJb5ALda2CS2IJosJbTfXocWzToKoNmIqx45ZZu7Zy2eM/Y9m7rxHlIpQPUIlPDZCResDDRf2ajxQNtzxxjPGwg75OLWsi2Ae5IDAEvaI747ZSRXFfbDLwZEcwNBOFk2M1Y6g3UFM1bBWiffu54LE7WfPiQ/TYBlaHqSfE5aalfKhk2PDUMZJyDx8bKhIJOjLSex2k1C3NGJB4opQ6AmKnWgZ4EqfxVjY4vByvmaCqdXwlwR5vMu+5jVzx+/X0Hj5I7ANi41ndrxluM2x48iiN9m7OW5jHOpN6JaNehg/tCWYMcJY09aX0kZ1pMG3LGy71RuqeRpIaQa2BmqzRrAa073qRwe1PUQ8Vl/bDcMnw002Z8nPnFzDGYrzKDJCc0TJEWC1XeGqqFE5nJ7Z4o3HOZwYZ28pIWgCDS0DSYb46yvuNiC3d53NJHyxps9z69BhxRw/nzCuQJEby7gxFTktgKlsIUxDaVjbLEDkzUjpNQ1sMSSzOBoTijfETPN0xzMPrvs1V6y5iRSnm1s1Habb3sGxeDpO03N5KuDblq2RpnxniTjHAtLKYxCfDgEwEKB3irYLYZ+FIFGFlgtEa3H/21ez6+Ne55opFrJkX85OnjjKen8XwrCLjddBKEypS8OWVoRg2qcQRE0nUQv4ZIfAZ+4icBZ8jsJLHNaH1OBsRJh6OHeXZ0hAPf+4mqisv51urinx0juXO5w7T1xuypu8E5WiEnkKTclSnPWzQHsUUAxkVDk6Uufs/a4jyAV6Zkx5wFpXyN4B32hYw+P5GDuUG2DOwlKE3OukZfZ0jdPHQ8NW8/Onr6V48l68sVSyfZfndi4e45sJ3WTF3HJpNcVOrQGRhEwwldYsLFD2RwSdVrM9nFGAaA4IvIPKOnWuv5eVqmaneRbBkKX9o/oDnCkvZv3gltdWfYHFnwCcHYVmX4a7tx/nqee+yoryP6ogoNSlws5KvUFpKgSDAowNFRB1tGymsTguBc6S13HlH50CZI9d/k7yDgrNUVp7HvvPPoyOCOZHl0nmKJR0xt28Z40srDrBy/ij1o5pcJIqnzyWYcXgvVHY4m2AannwpJK/q1NzJraH8xFjlfJiW2CCw9KsstcZe0xEZuoQfGi4eCBkqJfz48TGCNsfaRSPUDk2lMUykXgtS5eRyahlap/2ATrOPwL5JKWxwVDzgBN20QCjcblFGXOd1xt2g9V/ev7g/YLCYcNvm40wVuhnsmKJRN+RyGY2lrKR9TSpHqGZx0tGk6E5SruUKUNS19HD50zCgA5cmoek2q5UVs/jB6oGARYWEnz9zgqSjm2XdeY4cqxIbizYN6VPSk0qXpbRCazFaRAvhBBsWk2bWhI6whkkgf2oIvKSYrK1KG7WZnCD1fEBnyreO48rdLO2LGK87Eh9RixXtOdXygMviLXUkTRpSfAQHRtoSnI9QTFBreHQIkUlxT2pAvZLU47YwK5eneGD1gGZh3nD71nF0Zzdn94UkiSXU0paF1EyIDyX2mrTCKfmRU4sRNo15WGinac6iOPEGj22qsqm5QA2dC5MVV5sx4MDI5Eh7KWyEYVgwxvpAK3X5/IC5UcxtW8ZRXV0M9QZYqQkoAjzGB0w2A1TBYmKDEcSL/anrxZUJ2lfAhITj7/LgCxPcfeQ6v+D8BSqpu8bE8fpoVhW9V/c9+sL+StO+ogvKJw6XWIin6vxi6wSuvSt1e2LcycKixEtBymedS2gvaTp6Ispn5Sn3RZQHcnTMLVDq04SVPdz1F8Wvxm6mb3iFK3eFvlJL/rFnx6MHBLVpTyht2XUP7L12+JzBB7Vzdrzi1J6Ddd3bnWfwrKjlTkknGVtE8d4xxar8X/nakpdo1COqTajEYZrvJ5uCk4DJhmH3oRK7Js+nf+4cXyyXbKk9Cif3vnfTH29ecK/oDkW5fLHcs/aWp4Mbrrt7YNngzWFRM7yww0VYL0KyLiKrYjKERm05z+aD5/LEv7oxxmHSPBJCkAMdSe5DKU2hrcC8xTkVFtp0oZ0wfn/kTwf+vvvJ6YOr6ZT45TsOFN/c8svZy9ddc9OsxcM3Fsodc4VFadRbne+0ASl1JVElpCcXIVGYUVFSyHTXM73PShpo1I7rsZFH9r/1zh3NeZ85uPOHqt6K5snrGw+Oll594ncdnd2DS+YuW35ZrtS1OIzynToIQuetyhqKTLxOP61sWnOE99PsUWk2Et45wjBQtUZyVDWq+6qHRncePMy/yyuvmNz+XVWZ1qlONUCuz27y+dwbb+X2vfB82KwcDlwxVm02p1whVlQh31nSzkaq3pzwOpAWutVN2VzaZTaTitP1yJvudh0m7c4obQ4XOpNFn7/RnjUfu3mdkpI5c33op7fg4s3W+vJt2X0bsLTj5Dv9q/DpJDDagZL/27ZB79qZbxWWg/+wr2VZ/y8vPTaWMGoQDAAAAABJRU5ErkJggg==">
<meta name="theme-color" content="#245491">
<meta name="color-scheme" content="light">
<style>
:root{color-scheme:light !important}
body{font:16px/1.7 -apple-system,BlinkMacSystemFont,sans-serif;color:#24322d;background:#f4f6f3;max-width:920px;margin:48px auto;padding:0 24px}h1{font-size:32px}h1 button{font-size:14px;padding:6px 10px;font-weight:normal;vertical-align:middle;white-space:nowrap}input,button,.action{font:inherit;padding:10px 14px;border:1px solid #c6d1ca;border-radius:8px}input[type=url]{flex:1;min-width:180px}button,.action{background:#245441;color:white;cursor:pointer;text-decoration:none;display:inline-block}form,.actions{display:flex;gap:12px;flex-wrap:wrap}article{background:white;padding:24px;border:1px solid #e0e7e1;border-radius:12px;margin:20px 0}small{color:#62736b}a{color:#245441}#message{color:#8b4520;white-space:pre-line}#message.success{color:#176538;background:#eaf7ee;padding:12px;border-radius:8px}#message.failure{color:#a52222;background:#fff0f0;padding:12px;border-radius:8px}.delete-result{font-weight:bold;white-space:pre-wrap}.notice{background:#fff3cd;color:#9c0006;padding:14px 18px;border-left:4px solid #b07800;font-weight:bold}.secondary{background:white;color:#245441}
#url::placeholder{color:#757575;opacity:1}#upload-zone{background:#fff;color:#757575;font:inherit;text-align:center;border:1px dashed #c6d1ca;border-radius:8px;padding:12px 14px;cursor:pointer;flex-basis:100%;box-sizing:border-box}#file-name{display:block;font-size:14px;color:#000}#form input[type=url]{order:0}#form button{order:1}#upload-zone{order:2}#qianwen-login{background:#004B93;border-color:#004B93}#qianwen-login:hover{background:#003B75}#form button{background:#D65A00;border-color:#D65A00}#form button:hover{background:#B94D00}.retry-task{background:#FFD54F;border-color:#FFD54F;color:#24322d}.retry-task:hover{background:#FFC928;border-color:#FFC928}#runtime-show{background:#169bb4;border-color:#169bb4}#runtime-show:hover{background:#127e93}#runtime-dialog{width:min(850px,90vw);max-height:85vh;border:1px solid #c6d1ca;border-radius:12px;overflow:auto}#runtime-dialog img{max-width:100%;border:1px solid #ddd}#runtime-dialog::backdrop{background:#0005}.tool-logo{width:136px;height:136px;object-fit:contain;flex:none;margin-right:16px;transform:translate(-7.44px,-4px);transform-origin:top left}h1{display:flex;align-items:flex-start;line-height:1;margin-bottom:16px}.tool-title{font-size:60px;line-height:1;font-weight:inherit;min-width:0}.tool-title-main,.tool-title-support{display:block}.tool-title-support{font-size:52px;margin-top:8px;margin-left:-.58em}@media(max-width:800px){.tool-title{font-size:clamp(20px,5.5vw,60px)}.tool-title-support{font-size:.8667em;margin-top:.1333em}.tool-logo{width:2.1667em;height:2.1667em}h1{font-size:clamp(20px,5.5vw,60px)}}.title-actions{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:24px}.title-actions button{font-size:14px;padding:6px 10px;font-weight:normal}</style>
<h1><img class="tool-logo" src="/icons/app-icon.svg" alt="工具Logo"><span class="tool-title"><span class="tool-title-main">网页视频转语音识别文字稿</span><span class="tool-title-support">（由千问提供支持）</span></span></h1>
<div class="title-actions"><button type="button" id="qianwen-login">正在验证登录</button> <button type="button" id="runtime-show">显示任务状态</button></div>
<p>粘贴网页链接，后台下载并默认交给千问识别语音、区分发言人，生成带时间戳、以视频标题命名的 Word。</p>
<form id="form" autocomplete="off"><input id="url" autocomplete="off" aria-label="音视频网页链接" type="url" placeholder="粘贴YouTube、B站、小宇宙等音视频网页链接"><label id="upload-zone" tabindex="0">点击或将音视频文件拖拽到此处上传<input id="media-file" type="file" accept="audio/*,video/*,.mkv,.flac,.opus" hidden><span id="file-name"></span></label><button>开始生成文稿</button></form>
<p class="actions"><span id="login-status" role="status">正在读取登录千问状态…</span></p><p id="message" role="status"></p>
<p class="notice">本文稿内容为语音模型识别结果，需要注意：可能有错别字和识别不准确之处。</p>
<p><small>Word 保存到“下载/网页视频转语音识别文字稿（由千问提供支持）”。音频将上传千问服务器；需要登录时点击上方“登录或打开千问”。完成后直接查看或打开所在位置。Word 完整性检查通过后自动将原音视频移入废纸篓并清理临时音轨。</small></p>
<div id="jobs"></div>
<dialog id="runtime-dialog"><button id="runtime-close" type="button">关闭状态窗口</button><h2>后台任务状态</h2><p>关闭此窗口只隐藏显示，不会停止后台任务。页面截图每几秒更新。</p><div id="runtime-content"></div></dialog>
<script>

const historicalTaskTimes={};
const statusDialog=document.querySelector('#runtime-dialog');
document.querySelector('#runtime-close').onclick=()=>statusDialog.close();
document.querySelector('#runtime-show').onclick=()=>{statusDialog.showModal();refreshRuntime()};
async function refreshRuntime(){if(!statusDialog.open)return;let host=document.querySelector('#runtime-content');try{let response=await fetch('/runtime/status');if(!response.ok)throw Error('状态功能需要加载本次更新');let data=await response.json();host.replaceChildren();function row(text){let p=document.createElement('p');p.textContent=text;host.append(p)}row(data.browser);row('登录：'+(data.login.error||data.login.check_error||({valid:'已验证登录',required:'需要登录',unknown:'尚未确认'}[data.login.status]||'尚未确认')));for(let task of data.tasks){row(task.title+'：'+(stages[task.state]||task.state)+(task.error?'；'+task.error:'')+'；记录更新于 '+task.seconds_since_record_update+' 秒前'+(task.uploaded?'；已确认上传':''))}for(let page of data.pages){row('实际千问页面：'+(page.title||page.url));let img=document.createElement('img');img.alt='正在运行的千问页面截图';img.src='/runtime/page/'+page.index+'?at='+data.at;host.append(img)}if(!data.pages.length)row('当前暂无共享浏览器页面截图；旧任务还未接入共享浏览器时无法显示其实时页面。')}catch(e){host.textContent=e.message}}
setInterval(refreshRuntime,3000);
const stages={queued:'排队中',downloading:'正在下载',downloaded:'下载完成',diarizing:'正在准备千问识别',transcribing:'正在准备千问识别',cloud_preparing:'正在准备上传音频',cloud_transcribing:'等待千问处理结果或加载文稿页面',extracting_audio:'正在提取音频',cloud_connecting:'正在连接千问并检查登录',cloud_uploading:'正在向千问上传音频',cloud_confirming_upload:'等待千问页面确认上传记录（尚未确认成功）',retry_waiting:'页面加载超时，稍后自动重试',generating_document:'正在生成并检查 Word 文稿',cleaning:'Word 已生成，正在清理原音视频和临时文件',cloud_exporting:'正在导出千问原文 Word',completed:'Word 已生成，可以查看',login_required:'需要重新登录千问',failed:'处理失败，进度已保留'};
const msg=document.querySelector('#message');
let deleteNoticeTimer;
function renderDeletionResult(target,result){target.replaceChildren();let heading=document.createElement('div');heading.textContent=result.status==='success'?'删除成功':result.status==='pending'?'正在同步删除…':'删除失败';heading.style.color=result.status==='success'?'#176538':result.status==='pending'?'#8b4520':'#a52222';target.append(heading);if(result.elements){for(let element of result.elements){let row=document.createElement('div');row.textContent=element.label+'：'+element.detail;row.style.color=(element.status==='success'||(!element.status&&/^(删除成功|无需删除|未找到对应千问记录)/.test(element.detail)))?'#176538':element.status==='pending'?'#8b4520':'#a52222';target.append(row)}}else{let row=document.createElement('div');row.textContent=result.message;row.style.color=result.status==='success'?'#176538':'#a52222';target.append(row)}}
function showDeletionResult(result,success){clearTimeout(deleteNoticeTimer);msg.className=success?'success':'failure';renderDeletionResult(msg,result);let displayed=msg.textContent;if(success){deleteNoticeTimer=setTimeout(()=>{if(msg.className==='success'&&msg.textContent===displayed){msg.replaceChildren();msg.className=''}},3000)}}
const deletedTaskIds=new Set();const deletionResults=new Map();let refreshSequence=0;
async function requireControls(){let h=await(await fetch('/health')).json();if(!h.task_controls)throw Error('请双击“加载本次更新.command”，让网页服务加载登录和删除功能。')}
document.querySelector('#qianwen-login').onclick=async()=>{try{await requireControls();let r=await post('/qianwen/login',{});msg.textContent=r.message}catch(e){msg.textContent=e.message}};
let loginPrompted=false;
async function refreshLogin(){try{let h=await(await fetch('/health')).json();if(!h.task_controls){document.querySelector('#login-status').textContent='新功能需要加载本次更新';return}let s=await(await fetch('/qianwen/status')).json();let verified=s.status==='valid'&&Date.now()/1000-s.checked_at<180;document.querySelector('#qianwen-login').textContent=verified?'已登录千问':s.status==='required'?'需登录千问':s.check_error?'登录状态待确认':'正在验证登录';if(verified)loginPrompted=false;if(s.status==='required'&&!loginPrompted){loginPrompted=true;alert('千问未登录或登录已失效，请点击标题旁的登录按钮，完成登录后重试任务。');}let text=s.window_open?'请在千问窗口中完成登录，完成后关闭窗口':s.status==='required'?'千问需要重新登录，请点击标题旁的“登录或打开千问”按钮':s.last_success?'最近成功转写：'+new Date(s.last_success*1000).toLocaleString()+'；任务中会继续验证登录':'登录状态待验证，可能千问未登录；首次使用请点击“登录或打开千问”完成登录';document.querySelector('#login-status').textContent=s.error||(s.check_error?'暂时无法验证千问登录：'+s.check_error:text);if(s.error&&msg.textContent.startsWith('正在打开千问登录窗口')){msg.textContent='打开失败：'+s.error;msg.style.color='#a52222'}}catch(e){document.querySelector('#login-status').textContent='暂时无法读取登录状态'}}
async function post(url,data){let r=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});let j=await r.json();if(!r.ok){let error=Error(j.error);error.deletionResult=j.deletion_result;throw error}return j}
let selectedFile=null;
const zone=document.querySelector('#upload-zone'),picker=document.querySelector('#media-file'),urlInput=document.querySelector('#url');
function selectFile(file){if(!file)return;selectedFile=file;urlInput.value='';document.querySelector('#file-name').textContent=file.name}
picker.onchange=()=>selectFile(picker.files[0]);
zone.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();picker.click()}};
zone.ondragover=e=>{e.preventDefault()};zone.ondrop=e=>{e.preventDefault();if(e.dataTransfer.files.length!==1){msg.textContent='每次请选择一个音视频文件';return}selectFile(e.dataTransfer.files[0])};
urlInput.oninput=()=>{if(urlInput.value){selectedFile=null;picker.value='';document.querySelector('#file-name').textContent=''}};
document.querySelector('#form').onsubmit=async e=>{e.preventDefault();try{if('qianwen'==='qianwen'){let health=await(await fetch('/health')).json();if(!health.engines?.includes('qianwen'))throw Error('网页服务需要加载新版。请完成登录千问配置后再试。')}if(selectedFile){let h=await(await fetch('/health')).json();if(!h.local_upload)throw Error('请双击“加载本次更新.command”启用本地文件入口。');let button=document.querySelector('#form button');button.disabled=true;msg.textContent='正在将文件交给本机后台，请稍候…';try{let r=await fetch('/upload',{method:'POST',headers:{'Content-Type':'application/octet-stream','X-File-Name':encodeURIComponent(selectedFile.name)},body:selectedFile});let j=await r.json();if(!r.ok)throw Error(j.error)}finally{button.disabled=false}}else{if(!urlInput.value.trim())throw Error('请粘贴链接或选择音视频文件');await post('/jobs',{url:urlInput.value,engine:'qianwen'})}deletedTaskIds.clear();selectedFile=null;picker.value='';document.querySelector('#file-name').textContent='';document.querySelector('#url').value='';msg.textContent='已加入后台队列。你可以继续做其他事情，稍后回来查看文稿。';await refresh()}catch(e){msg.textContent=e.message}};
function taskHeading(j){return (j.task_number?j.task_number+' - ':'')+unnumberedHeading(j)}
function unnumberedHeading(j){let title=j.title;if(j.state==='queued')return '待处理 · '+(title||'正在获取标题（'+new URL(j.url).hostname+' / '+(new URL(j.url).searchParams.get('v')||new URL(j.url).pathname.split('/').filter(Boolean).pop()||j.id)+'）');return title||'正在获取标题 · '+j.id}
function link(text,url,style){let a=document.createElement('a');a.textContent=text;a.href=url;if(style)a.className=style;return a}
async function refreshDeletions(){try{let r=await fetch('/deletions');if(!r.ok)return;let reports=await r.json();for(let [id,report] of Object.entries(reports)){if(report.status==='pending'){deletionResults.set(id,report)}else if(deletionResults.get(id)?.status==='pending'){if(report.status==='success'){deletedTaskIds.add(id);deletionResults.delete(id);showDeletionResult(report,true)}else{deletionResults.set(id,report);showDeletionResult(report,false)}}}}catch(e){}}
async function refresh(){const sequence=++refreshSequence;try{await refreshDeletions();let jobs=await(await fetch('/jobs')).json();if(sequence!==refreshSequence)return;jobs=jobs.filter(j=>!deletedTaskIds.has(j.id));jobs.sort((a,b)=>a.task_number&&b.task_number?b.task_number-a.task_number:(b.created_at??historicalTaskTimes[b.id]??b.added_at??Infinity)-(a.created_at??historicalTaskTimes[a.id]??a.added_at??Infinity));let host=document.querySelector('#jobs');host.replaceChildren();for(let j of jobs){let card=document.createElement('article');card.dataset.taskId=j.id;let h=document.createElement('h2');h.textContent=taskHeading(j);card.append(h);let p=document.createElement('p');p.textContent=(j.document&&!j.has_document)?'Word 文件已不在原保存位置，重新提交链接可生成':(stages[j.state]||'状态暂未识别：'+String(j.state));card.append(p);if(j.source_kind==='local'){let source=document.createElement('p');source.textContent=j.source_label;card.append(source)}else card.append(link('原网页',j.url));let deletion=deletionResults.get(j.id)||j.deletion_result;if(deletion){let status=document.createElement('p');status.className='delete-result';status.setAttribute('role','alert');status.style.color=deletion.status==='failed'?'#a52222':'#8b4520';renderDeletionResult(status,deletion);card.append(status)}if(j.error){let err=document.createElement('p');err.textContent=j.error;card.append(err)}if(j.cleanup_error){let note=document.createElement('p');note.textContent='Word 已生成，但部分临时文件未清理：'+j.cleanup_error;card.append(note)}if(j.has_document){let actions=document.createElement('p');actions.className='actions';actions.append(link('查看 Word 文稿','/preview/'+j.id,'action'));let reveal=document.createElement('button');reveal.type='button';reveal.className='secondary';reveal.textContent='打开文档所在位置';let revealStatus=document.createElement('small');revealStatus.setAttribute('role','status');reveal.onclick=async()=>{reveal.disabled=true;revealStatus.textContent='正在打开文件夹…';try{await post('/reveal/'+j.id,{});revealStatus.textContent='已打开 Finder 文件夹。';msg.textContent='已打开文档所在的 Finder 文件夹。'}catch(e){revealStatus.textContent='打开失败：'+e.message;msg.textContent='打开失败：'+e.message}finally{reveal.disabled=false}};actions.append(reveal);actions.append(revealStatus);card.append(actions);let note=document.createElement('small');note.textContent=j.temporary_files_removed?(j.media_trashed?'原音视频已移入废纸篓，临时音轨已清理。':'原音视频与临时音轨已清理。'):'Word 内容未经人工校对。';card.append(note)}let controls=document.createElement('p');controls.className='actions';if(j.state==='failed'||j.state==='login_required'){let retry=document.createElement('button');retry.textContent='重试任务';retry.className='retry-task';retry.onclick=async()=>{try{await post('/jobs',{url:j.url,engine:'qianwen'});await refresh()}catch(e){msg.textContent=e.message}};controls.append(retry)}let remove=document.createElement('button');remove.type='button';remove.className='secondary';remove.style.color='#a52222';remove.textContent='删除任务并同步到千问';if(deletion?.status==='pending'){remove.disabled=true;remove.textContent='正在同步删除…'}remove.onclick=async()=>{if(!confirm('删除“'+(j.title||j.id)+'”？将停止该任务，把本机任务文件和相关文稿移入废纸篓。同时删除对应的千问云端记录，云端删除后无法恢复。'))return;deletionResults.set(j.id,{status:'pending',message:'正在删除并同步到千问，请稍候…'});msg.className='';msg.textContent='正在删除并同步到千问，请稍候…';remove.disabled=true;remove.textContent='正在同步删除…';try{let health=await(await fetch('/health')).json();if(!health.cloud_delete)throw Error('请先双击加载本次更新.command启用千问同步删除');await requireControls();let r=await post('/delete/'+j.id,{});if(r.deletion_result?.status==='pending'){deletionResults.set(j.id,r.deletion_result);msg.className='';renderDeletionResult(msg,r.deletion_result);await refresh();return}deletedTaskIds.add(j.id);++refreshSequence;document.querySelectorAll('article[data-task-id="'+j.id+'"]').forEach(node=>node.remove());deletionResults.delete(j.id);showDeletionResult(r.deletion_result||{status:'success',message:r.message},true);await refresh()}catch(e){let message=e.deletionResult?.message||('删除失败\n工具任务列表记录：未删除成功\n本机文稿及任务文件：未确认删除成功\n对应的千问记录：未确认删除成功\n原因：'+e.message);let report=e.deletionResult||{status:'failed',message};deletionResults.set(j.id,report);showDeletionResult(report,false);let status=card.querySelector('.delete-result');if(!status){status=document.createElement('p');status.className='delete-result';status.setAttribute('role','alert');card.append(status)}status.style.color='#a52222';renderDeletionResult(status,report);remove.disabled=false;remove.textContent='删除任务并同步到千问'}};if(j.has_document){card.querySelector('.actions').append(remove)}else{controls.append(remove)}if(controls.children.length)card.append(controls);host.append(card)}await refreshLogin()}catch(e){msg.textContent='后台连接中断，请重新启动工具。'}}
refresh();setInterval(refresh,6000);
</script></html>
```

### FILE: install-windows.cmd
```text
@echo off
cd /d "%~dp0"
powershell.exe -NoProfile -File "%~dp0install-windows.ps1" -Open %*
set "install_result=%errorlevel%"
if not "%install_result%"=="0" echo Installation failed. See README: Windows manual fallback. Do not disable security or execution policy.
pause
exit /b %install_result%
```

### FILE: install-windows.ps1
```text
﻿# Windows PowerShell 5.1+. Never changes execution policy or disables security.
param([switch]$NoStart, [switch]$StartOnly, [switch]$Open, [int]$Port = 8767)
$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
Set-Location -LiteralPath $PSScriptRoot
function Refresh-Path {
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'User') + ';' + [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + $env:Path
}
function Find-Python {
    $candidates = @("$env:LOCALAPPDATA\Programs\Python\Python312\python.exe", "$env:ProgramFiles\Python312\python.exe")
    $launcher = Get-Command py.exe -ErrorAction SilentlyContinue
    if ($launcher) {
        $found = $null
        try { $found = & $launcher.Source -3.12 -c 'import sys; print(sys.executable)' 2>$null } catch { $found = $null }
        if ($LASTEXITCODE -eq 0 -and $found) { $candidates = @($found) + $candidates }
    }
    $command = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($command -and $command.Source -notlike '*WindowsApps*') { $candidates += $command.Source }
    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate) {
            & $candidate -c 'import sys,platform; sys.exit(not (sys.version_info[:2]==(3,12) and sys.maxsize>2**32 and platform.machine().lower() in (''amd64'',''x86_64'')))' 2>$null
            if ($LASTEXITCODE -eq 0) { return $candidate }
        }
    }
    return $null
}
function Test-Node {
    $node = Get-Command node.exe -ErrorAction SilentlyContinue
    if (-not $node) { return $false }
    & $node.Source -e 'process.exit(process.arch === ''x64'' && Number(process.versions.node.split(''.'')[0]) >= 22 ? 0 : 1)'
    return ($LASTEXITCODE -eq 0)
}
function Install-Package([string]$Id, [string[]]$ExtraArgs) {
    if (-not (Get-Command winget.exe -ErrorAction SilentlyContinue)) {
        throw '缺少 WinGet。下一步：按 README 手动安装官方 Python 3.12 64位和 Node.js LTS x64，然后重跑入口。'
    }
    & winget.exe install --id $Id --exact --source winget --architecture x64 --accept-source-agreements --accept-package-agreements @ExtraArgs
    if ($LASTEXITCODE -ne 0) { throw "WinGet 安装 $Id 未完成。请按上方错误处理或使用 README 官方安装包，再重跑；系统授权由本人完成。" }
    Refresh-Path
}
try {
    if ([Environment]::OSVersion.Platform -ne 'Win32NT' -or [Environment]::OSVersion.Version.Build -lt 17763 -or $env:PROCESSOR_ARCHITECTURE -ne 'AMD64') {
        throw '需要 Windows 11 x64（或 Windows Server 2019+） 和64位 PowerShell。Windows ARM、32位和 WSL 尚不支持。'
    }
    $osInfo = Get-CimInstance Win32_OperatingSystem
    if ($osInfo.ProductType -eq 1 -and [Environment]::OSVersion.Version.Build -lt 22000) {
        throw '需要 Windows 11 x64；当前 Playwright 不正式支持 Windows 10，不能承诺自动安装。'
    }
    Refresh-Path
    $python = Find-Python
    if (-not $python) { Install-Package 'Python.Python.3.12' @('--scope', 'user'); $python = Find-Python }
    if (-not $python) { throw '下一步：重新打开终端后重跑入口；仍失败时安装 README 中的 Python 3.12 64位官方包。' }
    if (-not (Test-Node)) { Install-Package 'OpenJS.NodeJS.LTS' @() }
    if (-not (Test-Node)) { throw '下一步：重新打开终端再重跑；仍失败时安装 Node.js 22+ LTS x64 官方包。' }
    $installArgs = @('install.py', '--port', "$Port")
    if ($NoStart) { $installArgs += '--no-start' }
    if ($StartOnly) { $installArgs += '--start-only' }
    if ($Open) { $installArgs += '--open' }
    & $python @installArgs
    exit $LASTEXITCODE
} catch {
    Write-Host "未完成：$_" -ForegroundColor Red
    exit 1
}
```

### FILE: install.py
```text
#!/usr/bin/env python3
"""Idempotent installation and verified local startup; stdlib only at entry."""
import argparse
import json
import os
import platform
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from runtime_compat import venv_python

ROOT = Path(__file__).resolve().parent
TESTS = ['test_reader', 'test_app', 'test_qianwen', 'test_task_controls', 'test_install', 'test_runtime_compat']


def run(args, **kwargs):
    print('执行：' + ' '.join(map(str, args)), flush=True)
    return subprocess.run(list(map(str, args)), check=True, cwd=ROOT, **kwargs)


def check_environment():
    system, machine = platform.system(), platform.machine().lower()
    if not ((system == 'Darwin' and machine == 'arm64') or (system == 'Windows' and machine in ('amd64', 'x86_64'))):
        raise RuntimeError('支持原生 Apple Silicon Mac 或 Windows 11 x64；不支持 Rosetta、Intel Mac、Windows ARM/32位和 Linux。')
    if system == 'Windows' and sys.maxsize <= 2**32:
        raise RuntimeError('Windows 需要64位 Python 3.12，请安装官方 x64 安装包。')
    if system == 'Windows':
        version = sys.getwindowsversion()
        if version.build < 17763 or (version.product_type == 1 and version.build < 22000):
            raise RuntimeError('需要 Windows 11 x64 或 Windows Server 2019+；当前 Playwright 不正式支持 Windows 10。')
    if sys.version_info[:2] != (3, 12):
        raise RuntimeError('需要 Python 3.12。请运行系统对应的安装入口。')
    node = shutil.which('node')
    if not node:
        raise RuntimeError('缺少 Node.js。请运行系统对应的安装入口。')
    info = json.loads(subprocess.check_output(
        [node, '-p', 'JSON.stringify({version:process.versions.node,arch:process.arch})'], text=True))
    expected_arch = 'x64' if system == 'Windows' else 'arm64'
    if int(info['version'].split('.')[0]) < 22 or info['arch'] != expected_arch:
        raise RuntimeError('需要与系统架构一致的 Node.js 22+。请运行对应系统的安装入口。')


def ensure_venv():
    folder = ROOT / '.venv'
    python = venv_python(ROOT)
    if folder.is_symlink():
        raise RuntimeError('.venv 是符号链接，请先人工核查其目标；安装器不会修改。')
    healthy = False
    if python.exists():
        try:
            info = json.loads(subprocess.check_output([str(python), '-c',
                'import sys,platform,json;print(json.dumps([list(sys.version_info[:2]),platform.machine(),sys.prefix,sys.base_prefix]))'], text=True, timeout=10))
            healthy = info[0] == [3, 12] and info[1].lower() == platform.machine().lower() and Path(info[2]).resolve() == folder.resolve() and info[2] != info[3]
        except (OSError, ValueError, subprocess.SubprocessError):
            pass
    if not healthy:
        if folder.exists():
            # Preserve rather than delete a potentially non-standard environment.
            backup = ROOT / ('.venv.backup-' + str(time.time_ns()))
            folder.rename(backup)
            print(f'旧环境保留在 {backup.name}；任务和登录资料不受影响。', flush=True)
        run([sys.executable, '-m', 'venv', folder])
    return python


def health(port):
    # Bypass ambient HTTP proxies for local checks.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(f'http://127.0.0.1:{port}/health', timeout=2) as response:
        return json.load(response)


def validate_health(data):
    if not (isinstance(data, dict) and data.get('ok') is True and data.get('project') == str(ROOT) and data.get('engines') == ['qianwen']):
        raise RuntimeError('端口上的服务不是本目录的千问工具。请关闭对应旧服务，或使用 --port 选择空闲端口；未停止任何进程。')


def started_service_matches(pid, launcher_pid):
    if pid == launcher_pid:
        return True
    if platform.system() != 'Windows':
        return False
    # Windows venv python.exe redirects to a child interpreter. Verify ancestry,
    # script and working directory rather than accepting an arbitrary PID.
    import psutil
    try:
        process = psutil.Process(pid)
        args = process.cmdline()
        return (any(p.pid == launcher_pid for p in process.parents()) and
                len(args) >= 2 and Path(args[1]).resolve() == ROOT / 'app.py' and
                Path(process.cwd()).resolve() == ROOT)
    except (psutil.NoSuchProcess, psutil.AccessDenied, OSError, ValueError):
        return False


def start_service(python, port):
    try:
        data = health(port)
    except (OSError, ValueError):
        data = None
    if data is not None:
        validate_health(data)
        print('本目录服务已运行，健康检查通过。')
        return
    with socket.socket() as probe:
        try:
            probe.bind(('127.0.0.1', port))
        except OSError as error:
            raise RuntimeError(f'端口 {port} 被占用，请用 --port 选择空闲端口；未停止其他服务。') from error
    env = os.environ.copy()
    env['VIDEO_READER_PORT'] = str(port)
    work = ROOT / 'work'
    work.mkdir(exist_ok=True)
    with (work / 'app.log').open('ab') as log:
        child = subprocess.Popen([str(python), str(ROOT / 'app.py')], cwd=ROOT, env=env,
            stdin=subprocess.DEVNULL, stdout=log, stderr=log,
            **({'creationflags': subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == 'nt' else {'start_new_session': True}))
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        if child.poll() is not None:
            raise RuntimeError('服务启动失败，请查看本机 work/app.log（不要公开上传日志）。')
        try:
            data = health(port)
        except (OSError, ValueError):
            time.sleep(.5)
            continue
        try:
            validate_health(data)
            if not started_service_matches(data.get('pid'), child.pid):
                raise RuntimeError('健康检查的进程与本次启动不一致，请检查端口。')
        except RuntimeError:
            child.terminate()
            raise
        print('服务启动及 /health 检查通过。')
        return
    child.terminate()
    raise RuntimeError('服务健康检查超时，本次启动的进程已请求停止；请查看本机 work/app.log。')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--no-start', action='store_true', help='只安装和验收，不启动服务')
    parser.add_argument('--start-only', action='store_true', help='启动已安装环境并验证健康状态')
    parser.add_argument('--port', type=int, default=8767)
    parser.add_argument('--open', action='store_true', help='健康检查通过后打开工具网页')
    args = parser.parse_args(argv)
    if not 1024 <= args.port <= 65535:
        parser.error('端口应在 1024～65535 之间')
    if args.no_start and args.start_only:
        parser.error('--no-start 和 --start-only 不能同时使用')
    check_environment()
    os.environ['PLAYWRIGHT_BROWSERS_PATH'] = str(ROOT / 'work/browser-bin')
    # macOS system trust roots; never disable TLS verification.
    if Path('/etc/ssl/cert.pem').is_file():
        for key in ('PIP_CERT', 'SSL_CERT_FILE', 'NODE_EXTRA_CA_CERTS'):
            os.environ.setdefault(key, '/etc/ssl/cert.pem')
    if args.start_only:
        python = venv_python(ROOT)
        if not python.exists():
            raise RuntimeError('请先运行系统对应的安装入口完成安装。')
    else:
        python = ensure_venv()
        run([python, '-m', 'ensurepip', '--upgrade'])
        run([python, '-m', 'pip', 'install', '--upgrade', 'pip'])
        run([python, '-m', 'pip', 'install', '-r', ROOT / 'requirements.txt'])
        run([python, '-m', 'pip', 'check'])
        run([python, '-m', 'playwright', 'install', 'chromium'])
        run([python, '-c', 'from playwright.sync_api import sync_playwright\nwith sync_playwright() as p:\n b=p.chromium.launch(); b.close()'])
        run([python, '-m', 'unittest', *TESTS, '-q'])
    if not args.no_start:
        # Bootstrap runs under system Python; Windows process verification uses
        # psutil installed inside the project venv, never the global environment.
        if platform.system() == 'Windows' and Path(sys.prefix).resolve() != (ROOT/'.venv').resolve():
            command = [python, ROOT/'install.py', '--start-only', '--port', str(args.port)]
            if args.open:
                command.append('--open')
            run(command)
            return
        start_service(python, args.port)
        url = f'http://127.0.0.1:{args.port}/'
        print(f'工具地址：{url}\n请点击网页“登录或打开千问”，由本人完成账号登录/验证码。健康检查不代表已登录或云端转写成功。')
        if args.open:
            if os.name == 'nt':
                os.startfile(url)
            else:
                run(['/usr/bin/open', url])
    else:
        print('安装和本机验收完成。运行 bash install.sh --start-only 启动。')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        raise SystemExit(f'未完成：{error}\n修复上述问题后重新运行系统对应的安装入口；不要提交 work、日志或登录资料。')
```

### FILE: install.sh
```text
#!/bin/bash
# No curl | sh, sudo, Gatekeeper changes, or access to browser credentials.
set -euo pipefail
trap 'echo "安装未完成（入口第 $LINENO 行）。请按上方错误处理后重新运行 bash install.sh；若 Homebrew 安装失败，可改用 README 中的官方安装包。" >&2' ERR
cd -- "$(dirname -- "$0")"
export PATH="/opt/homebrew/opt/python@3.12/bin:/opt/homebrew/opt/node@22/bin:/opt/homebrew/bin:/Library/Frameworks/Python.framework/Versions/3.12/bin:/usr/local/bin:$PATH"
if [[ "$(uname -s)" != Darwin || "$(uname -m)" != arm64 ]]; then
  echo '仅支持原生 Apple Silicon Mac。若正在用 Rosetta，请在终端的“显示简介”取消“使用 Rosetta 打开”后重试。' >&2
  exit 1
fi
python_ok() {
  command -v python3.12 >/dev/null && python3.12 -c 'import sys,platform;sys.exit(not (sys.version_info[:2]==(3,12) and platform.machine()=="arm64"))'
}
node_ok() {
  command -v node >/dev/null && node -e 'process.exit(process.arch === "arm64" && Number(process.versions.node.split(".")[0]) >= 22 ? 0 : 1)'
}
if ! python_ok || ! node_ok; then
  if [[ -x /opt/homebrew/bin/brew ]]; then
    echo '使用已有的 Apple Silicon Homebrew 安装缺失环境（不使用 sudo）。'
    if ! python_ok; then /opt/homebrew/bin/brew install python@3.12; fi
    if ! node_ok; then /opt/homebrew/bin/brew install node@22; fi
    hash -r
  fi
fi
if ! python_ok; then
  echo '下一步：打开 https://www.python.org/downloads/release/python-31210/ ，安装 macOS universal2 安装包，然后重新运行 bash install.sh。系统密码由你本人输入。' >&2
  exit 1
fi
if ! node_ok; then
  echo '下一步：打开 https://nodejs.org/en/download ，安装 Node.js 22 或以上 LTS 的 macOS ARM64 安装包，然后重新运行 bash install.sh。系统密码由你本人输入。' >&2
  exit 1
fi
exec python3.12 install.py "$@"
```

### FILE: launch_service.py
```text
"""Manage a per-user launchd service; no administrator privileges required."""
import argparse
import json
import os
import plistlib
import signal
import subprocess
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LABEL = 'com.zhangjp.web-video-to-word'


def configuration(root, port):
    root = Path(root).resolve()
    return {'Label': LABEL, 'ProgramArguments': [str(root / '.venv/bin/python'), str(root / 'app.py')],
            'WorkingDirectory': str(root), 'RunAtLoad': True, 'KeepAlive': True,
            'ThrottleInterval': 10, 'AbandonProcessGroup': True,
            'EnvironmentVariables': {'VIDEO_READER_PORT': str(port),
                'PATH': '/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin',
                'PYTHONUNBUFFERED': '1'},
            'StandardOutPath': str(root / 'work/service.log'),
            'StandardErrorPath': str(root / 'work/service.log')}


def launchctl(*args, check=True):
    result = subprocess.run(['/bin/launchctl', *args], capture_output=True, text=True)
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or 'launchctl 操作失败')
    return result


def stop_standalone(port):
    """Only stop a listener whose executable arguments and cwd match this project."""
    result = subprocess.run(['/usr/sbin/lsof', '-t', f'-iTCP:{port}', '-sTCP:LISTEN'], capture_output=True, text=True)
    for pid in set(result.stdout.split()):
        cwd = subprocess.run(['/usr/sbin/lsof', '-a', '-p', pid, '-d', 'cwd', '-Fn'], capture_output=True, text=True).stdout
        try:
            command = subprocess.run(['/bin/ps', '-p', pid, '-o', 'command='], capture_output=True, text=True).stdout
            matching = str(ROOT / 'app.py') in command
        except OSError:
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/', timeout=2) as response:
                matching = response.read() == (ROOT / 'index.html').read_bytes()
        if 'n' + str(ROOT) + '\n' not in cwd or not matching:
            raise RuntimeError(f'端口 {port} 的进程身份无法确认为本工具，未关闭该进程。')
        os.kill(int(pid), signal.SIGTERM)
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        r = subprocess.run(['/usr/sbin/lsof', '-t', f'-iTCP:{port}', '-sTCP:LISTEN'], capture_output=True, text=True)
        if not r.stdout.strip():
            return
        time.sleep(.25)
    raise RuntimeError('旧网页服务尚未退出，未继续安装。')


def install(port):
    if not (ROOT / '.venv/bin/python').is_file():
        raise RuntimeError('请先完成首次安装。')
    folder = Path.home() / 'Library/LaunchAgents'
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / (LABEL + '.plist')
    config = configuration(ROOT, port)
    if path.exists():
        previous = plistlib.loads(path.read_bytes())
        if previous.get('WorkingDirectory') != str(ROOT):
            raise RuntimeError('已有另一份工具的同名启动项，请先核查，不自动覆盖。')
    domain = f'gui/{os.getuid()}'
    target = domain + '/' + LABEL
    (ROOT / 'work').mkdir(exist_ok=True)
    if launchctl('print', target, check=False).returncode == 0:
        if path.exists() and plistlib.loads(path.read_bytes()) == config:
            launchctl('kickstart', target)
            print(f'自动启动服务已配置：http://127.0.0.1:{port}/')
            return
        launchctl('bootout', target)
    stop_standalone(port)
    path.write_bytes(plistlib.dumps(config))
    path.chmod(0o644)
    launchctl('enable', target)
    try:
        launchctl('bootstrap', domain, str(path))
    except RuntimeError:
        env = os.environ.copy()
        env['VIDEO_READER_PORT'] = str(port)
        with (ROOT / 'work/service.log').open('ab') as log:
            subprocess.Popen(config['ProgramArguments'], cwd=ROOT, env=env,
                             stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True)
        raise
    deadline = time.monotonic() + 25
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/health', timeout=2) as response:
                health = json.load(response)
            if health.get('project') == str(ROOT):
                print(f'自动启动与自动恢复已启用：http://127.0.0.1:{port}/')
                return
        except (OSError, ValueError):
            pass
        time.sleep(.5)
    raise RuntimeError('启动项已安装，但服务未通过健康检查；请查看 work/service.log。')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['install', 'status', 'uninstall'])
    parser.add_argument('--port', type=int, default=8767)
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error('端口应在 1024～65535 之间')
    target = f'gui/{os.getuid()}/{LABEL}'
    if args.action == 'install':
        install(args.port)
    elif args.action == 'status':
        result = launchctl('print', target, check=False)
        print(result.stdout or '本工具自动启动项未加载。')
    else:
        path = Path.home() / 'Library/LaunchAgents' / (LABEL + '.plist')
        if path.exists():
            config = plistlib.loads(path.read_bytes())
            if config.get('WorkingDirectory') != str(ROOT):
                raise RuntimeError('启动项属于其他副本，未删除。')
            launchctl('bootout', target, check=False)
            path.unlink()
        print('已停用本工具的自动启动；Word 和任务记录均保留。')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        raise SystemExit(f'未完成：{error}。若系统限制操作，请从 Finder 双击自动启动设置文件。')
```

### FILE: qianwen_browser.py
```text
"""Qianwen web adapter. Uses an isolated local browser profile, never private APIs."""
import os
from contextlib import contextmanager
import argparse
import re
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', str(ROOT/'work/browser-bin'))
PROFILE = ROOT / 'work/qianwen-browser-profile'
URL = 'https://www.qianwen.com/discover/audioread'
MODEL = 'qianwen-web'


def read_export(path, duration):
    from docx import Document
    doc = Document(path)
    segments = []
    current = None
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        match = re.fullmatch(r'(发言人.*?)\s+((?:\d+:)?\d{2}:\d{2})', text)
        if match:
            parts = list(map(int, match[2].split(':')))
            seconds = sum(n * 60 ** i for i, n in enumerate(reversed(parts)))
            if seconds > duration + 5 or (segments and seconds < segments[-1]['start']):
                raise ValueError('千问时间戳与音频时长不符，保留原媒体')
            if current is not None:
                current['end'] = seconds
            current = {'start': seconds, 'end': duration, 'speaker': match[1], 'text': ''}
            segments.append(current)
        elif current is not None and text:
            current['text'] += ('\n' if current['text'] else '') + text
    if doc.tables:
        raise ValueError('千问导出出现未支持的表格结构，保留媒体，需更新导入器')
    if not segments or any(not s['text'] for s in segments):
        raise ValueError('千问导出缺少完整原文、发言人或时间戳，保留媒体')
    return {'model': MODEL, 'language': '中英文自由说', 'segments': segments,
            'speaker_method': '发言人由千问网页识别；结束时间取下一段起点，末段取音频总长。'}


class LoginRequired(RuntimeError):
    pass


def upload_failure_message(state, message):
    """Suggest login only for unconfirmed uploads; never claim expiry without evidence."""
    if state in ('cloud_connecting', 'cloud_uploading', 'cloud_confirming_upload'):
        if not re.search('存储已满|超限|不足|限制|不翻译|500MB|6小时|登录', message):
            return message + '\n可能千问未登录或登录已失效，请点击“登录或打开千问”，确认登录后重试。若已登录，请检查上方具体错误原因。'
    return message


def auth_state(status, error=None):
    from reader import save_json
    path=ROOT/'work/qianwen-auth.json'
    previous=__import__('json').loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    previous.update(status=status,checked_at=time.time())
    previous.pop('check_error',None)
    if error:previous['check_error']=str(error)
    if status=='valid':previous['last_success']=time.time()
    save_json(path,previous)


def require_login_if_visible(page):
    prompts=page.get_by_role('dialog').filter(has_text=re.compile('登录|验证码|手机号'))
    for prompt in prompts.all():
        if prompt.is_visible():
            auth_state('required')
            raise LoginRequired('千问需要重新登录或完成验证。请点击页面上的“登录或打开千问”，完成后重试任务。')
    buttons=[button for name in ('登录','登录/注册','立即登录')
             for button in page.get_by_role('button',name=name,exact=True).all()]
    if any(button.is_visible() for button in buttons):
        auth_state('required')
        raise LoginRequired('千问未登录或登录已失效，请点击“登录或打开千问”完成登录后重试。')


def require_cloud_available(page):
    """Surface explicit visible errors, without interpreting transcript text as errors."""
    messages=[]
    for alert in page.get_by_role('alert').all():
        if alert.is_visible():
            text=alert.inner_text().strip()
            if re.search('失败|出错|错误|异常|已满|超限|不足|重试|限制|不可用',text):
                messages.append(text)
    if messages:
        raise RuntimeError('千问页面提示：'+'；'.join(messages)+'。本机文件已保留，请处理后重试。')


def save_export_download(download,page,destination):
    """CDP clients can cancel browser downloads; recover through the same page session."""
    import base64
    try:
        download.save_as(str(destination))
        return
    except Exception as error:
        if 'canceled' not in str(error).lower():raise
    # Use the exact URL emitted by this export, including session-local blob URLs.
    encoded=page.evaluate("""async url => {
        const response=await fetch(url,{credentials:'include'});
        if(!response.ok)throw new Error('Word导出请求失败：HTTP '+response.status);
        const bytes=new Uint8Array(await response.arrayBuffer());
        if(bytes.length>50*1024*1024)throw new Error('Word导出文件超过50MB');
        let binary='';for(let i=0;i<bytes.length;i+=8192)binary+=String.fromCharCode(...bytes.subarray(i,i+8192));
        return btoa(binary);
    }""",download.url)
    data=base64.b64decode(encoded,validate=True)
    if not data.startswith(b'PK'):raise RuntimeError('千问导出未返回有效Word文件，原媒体已保留')
    from zipfile import ZipFile
    import io
    with ZipFile(io.BytesIO(data)) as archive:
        if 'word/document.xml' not in archive.namelist():raise RuntimeError('千问导出缺少Word正文，原媒体已保留')
    partial=destination.with_suffix('.partial.docx');partial.write_bytes(data);partial.replace(destination)

class TaskContext:
    def __init__(self,context):
        self.page=context.new_page()
        self.pages=[self.page]
        session=context.new_cdp_session(self.page)
        target=session.send("Target.getTargetInfo")["targetInfo"]["targetId"]
        session.detach()
        self.owner=ROOT/"work/browser-page-owners"/target
        self.owner.parent.mkdir(exist_ok=True)
        self.owner.write_text(str(os.getpid()))

@contextmanager
def browser_context(playwright, headed=False):
    from browser_service import endpoint
    from runtime_compat import venv_python,file_lock as fcntl
    PROFILE.mkdir(parents=True, exist_ok=True)
    if not headed:
        if not endpoint():
            with (ROOT/'work/browser-service.log').open('ab') as log:
                subprocess.Popen([str(venv_python(ROOT)),str(ROOT/'browser_service.py')],stdout=log,stderr=log,start_new_session=True)
            for _ in range(40):
                if endpoint():break
                time.sleep(.25)
        address=endpoint()
        if not address:raise RuntimeError('千问浏览器正在使用中，请关闭登录窗口或稍后重试。')
        browser=playwright.chromium.connect_over_cdp(address)
        task=TaskContext(browser.contexts[0])
        try:yield task
        finally:
            try:
                task.page.close()
                task.owner.unlink(missing_ok=True)
            finally:browser.close() # CDP disconnect; shared browser stays alive.
        return
    address=endpoint()
    if address:
        browser=playwright.chromium.connect_over_cdp(address)
        if len(browser.contexts[0].pages)>1:
            browser.close()
            raise RuntimeError('后台任务仍在使用千问，请等待当前操作完成后登录。')
        browser.new_browser_cdp_session().send('Browser.close')
        browser.close()
        time.sleep(1)
    with (ROOT/'work/qianwen-browser.lock').open('a') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise RuntimeError('千问浏览器正在使用中，请关闭登录窗口或等待任务完成后再试。')
        context=playwright.chromium.launch_persistent_context(str(PROFILE),headless=False,accept_downloads=True,viewport={'width':1920,'height':1600})
        try:yield context
        finally:context.close()

def check_auth():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        with browser_context(p) as context:
            page=context.pages[0];page.goto(URL,wait_until='domcontentloaded')
            page.wait_for_timeout(1500)
            require_login_if_visible(page)
            page.get_by_text('中英文自由说',exact=True).wait_for(timeout=30000)
            require_login_if_visible(page)
            auth_state('valid')


def export_with_retry(audio, job, meta, save):
    """Retry browser timeouts only; saved submission and document URL prevent reupload."""
    from playwright.sync_api import TimeoutError as BrowserTimeout
    for attempt in range(3):
        try:
            return export_audio(audio,job,meta,save)
        except BrowserTimeout:
            if attempt==2:raise
            meta.update(state='retry_waiting',retry_attempt=attempt+1)
            save(job/'job.json',meta)
            time.sleep(5*(attempt+1))


def export_panel(page,job):
    from playwright.sync_api import expect
    panel=page.get_by_role('tooltip').filter(visible=True).first
    panel.wait_for(state='visible',timeout=30000)
    checks=panel.get_by_role('checkbox')
    try:
        expect(checks).to_have_count(5,timeout=30000)
    except AssertionError as error:
        from playwright.sync_api import TimeoutError
        page.screenshot(path=str(job/'browser-diagnostic.png'),full_page=True)
        (job/'browser-diagnostic.txt').write_text(page.locator('body').inner_text(), encoding="utf-8")
        raise TimeoutError('千问导出选项尚未加载完整，已保留任务和媒体') from error
    return panel,checks


def confirm_submission(page,title,job,meta,save,timeout=120000):
    from playwright.sync_api import TimeoutError as BrowserTimeout
    meta['state']='cloud_confirming_upload';save(job/'job.json',meta)
    deadline=time.monotonic()+timeout/1000
    while time.monotonic()<deadline:
        require_login_if_visible(page)
        try:
            page.get_by_text(title,exact=True).filter(visible=True).first.wait_for(timeout=1000)
            meta.update(qianwen_submitted=True,qianwen_upload_confirmed=True,state='cloud_transcribing')
            save(job/'job.json',meta)
            return
        except BrowserTimeout:
            body=page.locator('body').inner_text()
            (job/'browser-diagnostic.txt').write_text(body, encoding="utf-8")
            events=job/'upload-events.txt'
            previous=events.read_text(encoding="utf-8") if events.exists() else ''
            if not previous.endswith(body+'\n'):
                events.write_text((previous+'\n'+str(time.time())+'\n'+body+'\n')[-64000:], encoding="utf-8")
            if '存储已满' in body and '删除不用的记录' in body:
                meta.update(qianwen_submission_attempted=False,qianwen_submitted=False,qianwen_upload_confirmed=False)
                save(job/'job.json',meta)
                raise RuntimeError('千问账号云端存储已满，请在千问中自行删除不需要的记录后重试。本机音频已保留；本次未删除云端记录。')
            require_cloud_available(page)
            meta['last_browser_check']=time.time();save(job/'job.json',meta)
    raise RuntimeError('千问页面未出现本次上传记录，尚未确认上传成功。已保留音频，请诊断后重试；不会重复自动上传。')


def export_audio(audio, job, meta, save):
    from playwright.sync_api import sync_playwright
    from reader import ffmpeg, filename
    meta['state']='cloud_preparing';save(job/'job.json',meta)
    upload = job/'media'/(filename(meta['title'])+'-'+job.name+'.mp3')
    if not upload.exists():
        subprocess.run([ffmpeg(), '-nostdin', '-v', 'error', '-y', '-i', str(audio),
                        '-c:a', 'libmp3lame', '-b:a', '64k', str(upload)], check=True)
    if meta['audio_duration'] > 6*3600 or upload.stat().st_size > 500*1024*1024:
        raise ValueError('超过千问网页单文件6小时或音频500MB限制，保留媒体')
    with sync_playwright() as p:
        with browser_context(p) as context:
            page = context.pages[0] if context.pages else context.new_page()
            meta['state']='cloud_connecting';save(job/'job.json',meta)
            page.goto(meta.get('qianwen_url') or URL)
            page.screenshot(path=str(job/'browser-diagnostic.png'), full_page=True)
            (job/'browser-diagnostic.txt').write_text(page.locator('body').inner_text(), encoding="utf-8")
            require_login_if_visible(page)
            if not meta.get('qianwen_url'):
                try:
                    page.get_by_text('中英文自由说', exact=True).wait_for(timeout=30000)
                except Exception as error:
                    require_login_if_visible(page)
                    raise RuntimeError('千问上传页面未加载完成，可能千问未登录或页面无法访问。请点击“登录或打开千问”，确认登录后重试。') from error
                page.get_by_text('中英文自由说', exact=True).click()
                page.get_by_text('多人讨论', exact=True).click()
                if not page.get_by_text('不翻译', exact=True).is_visible():
                    raise RuntimeError('未确认不翻译设置，停止上传')
                if not meta.get('qianwen_submitted') and not meta.get('qianwen_submission_attempted'):
                    meta['state']='cloud_uploading';save(job/'job.json',meta)
                    with page.expect_file_chooser() as chooser:
                        page.get_by_role('button', name=re.compile('点击或将')).click()
                    chooser.value.set_files(str(upload))
                    page.screenshot(path=str(job/'upload-selected.png'),full_page=True)
                    (job/'upload-selected.txt').write_text(page.locator('body').inner_text(), encoding="utf-8")
                    from playwright.sync_api import expect
                    expect(page.get_by_role('button',name='确 认',exact=True)).to_be_enabled(timeout=120000)
                    meta['qianwen_upload_title']=upload.stem
                    meta['qianwen_submission_attempted']=True;save(job/'job.json',meta)
                    page.get_by_role('button', name='确 认', exact=True).click()
                    page.screenshot(path=str(job/'upload-confirmed.png'),full_page=True)
                    (job/'upload-confirmed.txt').write_text(page.locator('body').inner_text(), encoding="utf-8")
                    require_login_if_visible(page)
                title = upload.stem
                confirm_submission(page,title,job,meta,save)
                deadline = time.monotonic() + 6 * 3600
                while time.monotonic() < deadline:
                    require_login_if_visible(page)
                    require_cloud_available(page)
                    from playwright.sync_api import TimeoutError as BrowserTimeout
                    try:
                        if '/efficiency/doc/transcripts/' not in page.url:
                            page.get_by_text(title, exact=True).filter(visible=True).first.click(timeout=10000)
                        if '/efficiency/doc/transcripts/' in page.url:
                            meta['qianwen_url']=page.url;save(job/'job.json',meta)
                        page.get_by_role('button', name='导出', exact=True).wait_for(timeout=10000)
                    except BrowserTimeout:
                        page.screenshot(path=str(job/'browser-diagnostic.png'),full_page=True)
                        (job/'browser-diagnostic.txt').write_text(page.locator('body').inner_text(), encoding="utf-8")
                        meta['last_browser_check']=time.time();save(job/'job.json',meta)
                        time.sleep(5)
                        continue
                    meta['qianwen_url'] = page.url; save(job/'job.json', meta)
                    break
                else:
                    raise RuntimeError('千问处理超过等待上限，保留媒体以便检查')
            meta['state']='cloud_exporting';save(job/'job.json',meta)
            page.get_by_role('button', name='导出', exact=True).wait_for(timeout=60000)
            page.screenshot(path=str(job/'browser-diagnostic.png'), full_page=True)
            (job/'browser-diagnostic.txt').write_text(page.locator('body').inner_text(), encoding="utf-8")
            require_cloud_available(page)
            page.get_by_role('button', name='导出', exact=True).click()
            panel,checks=export_panel(page,job)
            checks.nth(0).check()
            for i in range(1, 5): checks.nth(i).uncheck()
            if not panel.get_by_text('.docx', exact=True).first.is_visible():
                raise RuntimeError('导出格式不是 Word')
            for text in ('发言人', '时间戳'):
                if not panel.get_by_text(text, exact=True).is_visible():
                    raise RuntimeError('千问导出未包含'+text+'，请在千问导出设置中勾选')
            meta['state'] = 'cloud_exporting'; save(job/'job.json', meta)
            destination = job/'qianwen-original.docx'
            with page.expect_download(timeout=120000) as download:
                panel.get_by_role('button', name='导出', exact=True).click()
            save_export_download(download.value,page,destination)
    raw = read_export(destination, meta['audio_duration'])
    auth_state('valid')
    upload.unlink(missing_ok=True)
    return raw


def delete_cloud_record(page, job, meta, save):
    """Delete only the exact tool-uploaded title containing this task's identifier."""
    from playwright.sync_api import expect
    from reader import filename
    if meta.get('qianwen_cloud_deleted') or meta.get('qianwen_delete_resolved'):return
    if not any(meta.get(key) for key in ('qianwen_submitted','qianwen_submission_attempted','qianwen_url','qianwen_upload_confirmed')):
        meta.update(qianwen_delete_resolved=True,qianwen_delete_result='not_uploaded');save(job/'job.json',meta);return
    title=meta.get('qianwen_upload_title') or filename(meta['title'])+'-'+job.name
    if not title.endswith('-'+job.name):raise RuntimeError('无法确认千问记录归属，未执行删除')
    require_login_if_visible(page)
    page.get_by_text('最近记录',exact=False).first.wait_for(timeout=30000)
    rows=page.locator('[data-e2e-test-id="folders_item_div"]').filter(has=page.get_by_text(title,exact=True))
    try:expect(rows).to_have_count(1,timeout=15000)
    except AssertionError as error:
        require_login_if_visible(page)
        require_cloud_available(page)
        if rows.count()==0:
            meta.update(qianwen_delete_resolved=True,qianwen_delete_result='not_found')
            save(job/'job.json',meta)
            return
        raise RuntimeError('存在多个匹配的千问记录，无法唯一定位，未执行云端删除') from error
    rows.locator('[data-name="action"] .ant-dropdown-trigger').click()
    page.get_by_role('menuitem',name='删除',exact=True).click()
    dialog=page.get_by_role('dialog').filter(has_text='确定删除本记录吗？')
    dialog.wait_for(state='visible',timeout=10000)
    dialog.get_by_role('button',name='确定删除',exact=True).click()
    expect(rows).to_have_count(0,timeout=30000)
    require_cloud_available(page)
    meta.update(qianwen_cloud_deleted=True,qianwen_delete_resolved=True,qianwen_delete_result='deleted');save(job/'job.json',meta)


def delete_cloud(job):
    import json
    from reader import save_json
    from playwright.sync_api import sync_playwright
    meta=json.loads((job/'job.json').read_text(encoding="utf-8"))
    if meta.get('qianwen_cloud_deleted') or meta.get('qianwen_delete_resolved'):return
    if not any(meta.get(key) for key in ('qianwen_submitted','qianwen_submission_attempted','qianwen_url','qianwen_upload_confirmed')):
        meta.update(qianwen_delete_resolved=True,qianwen_delete_result='not_uploaded');save_json(job/'job.json',meta);return
    with sync_playwright() as p:
        with browser_context(p) as context:
            page=context.pages[0] if context.pages else context.new_page()
            page.goto(URL,wait_until='domcontentloaded')
            delete_cloud_record(page,job,meta,save_json)


def login(ui=False):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        with browser_context(p, headed=True) as context:
            page = context.pages[0] if context.pages else context.new_page()
            page.goto(URL)
            if ui:
                while not page.is_closed():
                    try:
                        require_login_if_visible(page)
                        if page.get_by_text('中英文自由说',exact=True).is_visible():auth_state('valid')
                        page.wait_for_timeout(500)
                    except LoginRequired:page.wait_for_timeout(500)
                    except Exception:break
            else:
                input('请在专用浏览器中登录千问，确认音视频速读页面可用后，在此按回车保存登录。')
    print('登录环境已保存在本机。后台任务不会打开此浏览器窗口。')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('command', choices=['login','login-ui','delete','check-auth'])
    parser.add_argument('--job')
    args=parser.parse_args()
    if args.command=='check-auth':
        try:check_auth()
        except LoginRequired:pass
        except Exception as error:
            auth_state('unknown',error)
    elif args.command=='delete':
        if not args.job or not re.fullmatch('[0-9a-f]{12}',args.job):parser.error('任务编号不合法')
        delete_cloud(ROOT/'work/jobs'/args.job)
    else:
        from reader import save_json
        result=ROOT/'work/qianwen-login-result.json'
        save_json(result,{'status':'opening','at':time.time()})
        try:
            login(ui=args.command=='login-ui')
            save_json(result,{'status':'closed','at':time.time()})
        except Exception as error:
            message=str(error)
            if '浏览器正在使用中' in message:
                message='千问浏览器被更新前启动的任务或登录窗口占用，请等待该任务结束或关闭登录窗口后再试。'
            save_json(result,{'status':'failed','error':message,'at':time.time()})
            raise
```

### FILE: reader.py
```text
#!/usr/bin/env python3
"""Background download, Qianwen cloud speech recognition and verified Word export."""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata
import wave
import time
from pathlib import Path
from runtime_compat import IS_WINDOWS

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work'
LEGACY_OUTPUT = Path.home() / 'Downloads' / '音视频文稿'
OUTPUT = Path.home() / 'Downloads' / '网页视频转语音识别文字稿（由千问提供支持）'
NOTICE = '本文稿内容为语音模型识别结果，需要注意：可能有错别字和识别不准确之处。'


def save_json(path, value):
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    tmp.replace(path)


def filename(title):
    title = unicodedata.normalize('NFC', title)
    title = re.sub(r'[\x00-\x1f/\\:*?"<>|]', '_', title).strip(' .')
    # macOS filenames have a byte limit, rather than a character limit.
    while len(title.encode('utf-8')) > 190:
        title = title[:-1]
    if re.fullmatch(r'(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?', title, re.I):
        title = '_' + title
    return title or '未命名音视频'


def ffmpeg():
    import imageio_ffmpeg
    folder = WORK / 'bin'
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / ('ffmpeg.exe' if IS_WINDOWS else 'ffmpeg')
    if not target.exists():
        if IS_WINDOWS:
            __import__('shutil').copy2(imageio_ffmpeg.get_ffmpeg_exe(), target)
        else:
            target.symlink_to(imageio_ffmpeg.get_ffmpeg_exe())
    os.environ['PATH'] = str(folder) + os.pathsep + os.environ.get('PATH', '')
    return str(target)


def stamp(seconds):
    seconds = int(seconds)
    return f'{seconds // 3600:02}:{seconds // 60 % 60:02}:{seconds % 60:02}'


def load_job(job):
    path = Path(job).resolve()
    if path.parent != (WORK / 'jobs').resolve() or not path.is_dir():
        raise ValueError('任务必须位于本项目 work/jobs 下')
    return path, json.loads((path / 'job.json').read_text(encoding="utf-8"))


def make_blocks(segments, limit=2200):
    # Keep each audio interval and each speaker turn visible, rather than merging timestamps.
    return [dict(seg, id=i + 1, text=seg['text'].strip())
            for i, seg in enumerate(segments) if seg.get('text', '').strip()]


def download_url(url):
    """Normalize Douyin modal pages without changing the source link in the document."""
    from urllib.parse import urlparse,parse_qs
    parts=urlparse(url)
    if parts.hostname in ('douyin.com','www.douyin.com'):
        ident=parse_qs(parts.query).get('modal_id',[''])[0]
        if re.fullmatch(r'[0-9]+',ident):return 'https://www.douyin.com/video/'+ident
    return url


def extract_audio(executable,media,destination):
    result=subprocess.run([executable,'-nostdin','-v','error','-y','-i',str(media),
                           '-vn','-ac','1','-ar','16000','-c:a','pcm_s16le',str(destination)],
                          capture_output=True,text=True)
    if result.returncode:
        destination.unlink(missing_ok=True)
        if 'does not contain any stream' in result.stderr:
            raise ValueError('下载的视频没有音轨，无法生成语音文字稿。原视频已保留；如果原网页播放时有声音，请提供其他有声音的视频版本。')
        raise ValueError('音频提取失败，原视频已保留。转换器提示：'+result.stderr.strip()[-600:])


def prepare(args):
    import certifi
    os.environ['SSL_CERT_FILE'] = certifi.where()
    from yt_dlp import YoutubeDL
    from urllib.parse import urlparse
    if urlparse(args.url).scheme not in ('http', 'https', 'local'):
        raise ValueError('请输入 HTTP 或 HTTPS 网页链接')
    try:
        os.nice(10)
    except (PermissionError, AttributeError):
        print('当前执行环境不允许调整进程优先级，继续单任务处理。', flush=True)
    ff = ffmpeg()
    ident = hashlib.sha256(args.url.encode()).hexdigest()[:12]
    job = WORK / 'jobs' / ident
    job.mkdir(parents=True, exist_ok=True)
    lock = job / '.prepare.lock'
    # OS file locks release automatically after an interrupted process.
    from runtime_compat import file_lock as fcntl
    with lock.open('a') as handle:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        meta = {'url': args.url, 'state': 'downloading'}
        if (job / 'job.json').exists():
            meta = json.loads((job / 'job.json').read_text(encoding="utf-8"))
            if meta.get('state') == 'completed' and Path(meta.get('document', '/nonexistent')).is_file():
                print(f'已有任务，无需重复处理：{job}', flush=True)
                return
            if meta.get('state') == 'completed' and (job / 'raw-transcript.json').exists():
                build_document(job)
                return
        meta.setdefault('created_at', getattr(job.stat(), 'st_birthtime', job.stat().st_mtime))
        meta.pop('error', None)
        meta['state'] = 'downloading'
        save_json(job / 'job.json', meta)
        try:
            media_folder = job / 'media'
            options = {'noplaylist': True, 'ffmpeg_location': str(Path(ff).parent),
                       'format': 'bestvideo[height<=480]+bestaudio/best/bestaudio',
                       'outtmpl': str(media_folder / '%(title).60s.%(ext)s'),
                       'merge_output_format': 'mkv', 'retries': 5,
                       'socket_timeout': 30, 'overwrites': False}
            node = Path('~/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node')
            if node.exists():
                options['js_runtimes'] = {'node': {'path': str(node)}}
            if args.cookies_browser:
                options['cookiesfrombrowser'] = (args.cookies_browser,)
            if meta.get('source_kind') == 'local' and (not meta.get('media') or not Path(meta['media']).is_file()):
                raise ValueError('本地上传文件已不存在，请重新上传')
            if not meta.get('media') or not Path(meta['media']).exists():
                media_folder.mkdir(parents=True, exist_ok=True)
                with YoutubeDL(options) as downloader:
                    from bilibili_download import register
                    register(downloader)
                    try:
                        info = downloader.extract_info(download_url(args.url), download=True)
                    except Exception as error:
                        if 'No video formats found' in str(error) and 'bilibili.com' in args.url:
                            raise ValueError('B站未提供可下载的音视频地址，可能需要B站访问验证或登录；尚未上传千问。重复重试不一定有效，可使用本地文件入口。') from error
                        raise
                    if not info or info.get('_type') in ('playlist', 'multi_video'):
                        raise ValueError('此页面包含多个媒体，请提供具体视频链接')
                    name = filename(info.get('title', '未命名音视频'))
                    merged = media_folder / (Path(downloader.prepare_filename(info)).stem + '.mkv')
                    source = merged if merged.exists() else Path(downloader.prepare_filename(info))
                    if not source.is_file():
                        raise ValueError('下载结束后未找到媒体文件')
                    target = media_folder / (name + source.suffix)
                    if source != target:
                        source.replace(target)
                    meta.update(title=info.get('title', name), name=name,
                                duration=info.get('duration'), media=str(target),
                                source_id=info.get('id'), state='downloaded')
                    save_json(job / 'job.json', meta)
            wav = Path(meta.get('audio', str(Path(meta['media']).parent / 'transcription-audio.wav')))
            meta['audio'] = str(wav)
            if not wav.exists():
                meta['state']='extracting_audio';save_json(job/'job.json',meta)
                partial = wav.with_name('transcription-audio.partial.wav')
                extract_audio(ff,Path(meta['media']),partial)
                partial.replace(wav)
            with wave.open(str(wav)) as audio:
                duration = audio.getnframes() / audio.getframerate()
            if not duration:
                raise ValueError('音轨为空')
            meta['audio_duration'] = duration
            if meta.get('duration') and abs(duration - meta['duration']) > max(5, duration * .01):
                raise ValueError('下载音轨时长与网页时长不符，需要检查')
            meta['state'] = 'cloud_preparing'
            meta['model'] = 'qianwen-web'
            save_json(job / 'job.json', meta)
            os.environ.setdefault('SSL_CERT_FILE', '/etc/ssl/cert.pem')
            raw_path = job / 'raw-transcript.json'
            raw = json.loads(raw_path.read_text(encoding="utf-8")) if raw_path.exists() else {}
            if raw.get('model') != 'qianwen-web':
                from qianwen_browser import export_with_retry
                raw = export_with_retry(wav, job, meta, save_json)
                save_json(raw_path, raw)
            meta['state']='generating_document';save_json(job/'job.json',meta)
            build_document(job, raw)
            print(f'Word 已生成：{job}', flush=True)
        except Exception as error:
            from qianwen_browser import LoginRequired, upload_failure_message
            message=upload_failure_message(meta.get('state'),str(error))
            if 'Fresh cookies' in message and 'Douyin' in message:
                message='抖音限制了自动下载，需要有效的抖音浏览器 Cookie。精选页链接已转换成单视频地址，但尚未下载成功；千问转写尚未开始。'
            meta.update(state='login_required' if isinstance(error,LoginRequired) else 'failed', error=message)
            save_json(job / 'job.json', meta)
            raise


def hyperlink(paragraph, url):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    link = OxmlElement('w:hyperlink')
    link.set(qn('r:id'), paragraph.part.relate_to(url, RT.HYPERLINK, is_external=True))
    run = OxmlElement('w:r')
    props = OxmlElement('w:rPr')
    color = OxmlElement('w:color')
    color.set(qn('w:val'), '0563C1')
    props.append(color)
    run.append(props)
    text = OxmlElement('w:t')
    text.text = url
    run.append(text)
    link.append(run)
    paragraph._p.append(link)


def verify_document(path, meta, blocks):
    from docx import Document
    from zipfile import ZipFile
    with ZipFile(path) as archive:
        if archive.testzip():
            raise ValueError('Word 文件损坏')
    doc = Document(path)
    texts = [p.text for p in doc.paragraphs]
    if not texts or texts[0] != (meta.get('source_label') if meta.get('source_kind') == 'local' else meta['url']):
        raise ValueError('Word 缺少来源信息')
    if NOTICE not in texts:
        raise ValueError('Word 缺少识别准确性提示')
    for block in blocks:
        caption = f'[{stamp(block["start"])}–{stamp(block["end"])}] {block.get("speaker", "")}'
        if caption not in texts:
            raise ValueError('Word 缺少时间戳或发言人标注')
        if block['text'] not in texts:
            raise ValueError('Word 未完整保存语音识别结果')
    return {'zip_valid': True, 'first_line_url': meta.get('source_kind') != 'local', 'first_line_source': True, 'notice_present': True,
            'all_blocks_present': len(blocks), 'accuracy': '未经人工校对的语音模型识别结果'}


def clear_intermediate(job, meta):
    import shutil
    report = json.loads((job / 'validation.json').read_text(encoding="utf-8"))
    path = Path(meta['document'])
    if hashlib.sha256(path.read_bytes()).hexdigest() != report['document_sha256']:
        raise ValueError('Word 已改动，拒绝清理原媒体')
    raw = json.loads((job / 'raw-transcript.json').read_text(encoding="utf-8"))
    verify_document(path, meta, make_blocks(raw['segments']))
    for key in ('media', 'audio'):
        if not meta.get(key):
            continue
        media = Path(meta[key])
        if media.is_symlink() or media.parent.resolve() not in (job.resolve(), (job / 'media').resolve(), (LEGACY_OUTPUT / job.name).resolve()):
            raise ValueError('媒体不在本工具的任务目录内，拒绝清理')
        if media.exists():
            from send2trash import send2trash
            if key == 'media':
                send2trash(str(media.resolve()))
                meta['media_trashed'] = True
            else:
                media.unlink()
    for name in ('transcription-audio.wav', 'transcription-audio.partial.wav'):
        for folder in (job, job / 'media', LEGACY_OUTPUT / job.name):
            (folder / name).unlink(missing_ok=True)
    for checkpoint in job.glob('checkpoints-*'):
        if checkpoint.is_dir() and not checkpoint.is_symlink():
            shutil.rmtree(checkpoint)
    for name in ('blocks.json', '原始转写.txt', 'ChatGPT校对任务.txt', 'chatgpt-result.json',
                 '网页校对结果.json', 'submitted-result.json', 'result.json', 'speaker-turns.json',
                 'qianwen-original.docx', 'browser-diagnostic.png', 'browser-diagnostic.txt', 'upload-selected.png', 'upload-selected.txt', 'upload-confirmed.png', 'upload-confirmed.txt', 'upload-events.txt', 'upload-recovery.png', 'upload-recovery.txt',
                 'browser-elements.json', 'browser-rows.json', 'browser-structure.json'):
        (job / name).unlink(missing_ok=True)
    meta['temporary_files_removed'] = True
    save_json(job / 'job.json', meta)


def configure_folder_sort(folder):
    """Persist Finder list-view settings for this output folder only."""
    if IS_WINDOWS:
        return
    from ds_store import DSStore
    settings = folder / '.DS_Store'
    with DSStore.open(str(settings), 'r+' if settings.exists() and settings.stat().st_size else 'w+') as store:
        preferences = {
            'viewOptionsVersion': 1, 'iconSize': 16.0, 'showIconPreview': True,
            'sortColumn': 'name', 'textSize': 13.0, 'useRelativeDates': True,
            'calculateAllSizes': False, 'columns': {
                'name': {'index': 0, 'width': 450, 'visible': True, 'ascending': False},
                'dateAdded': {'index': 1, 'width': 180, 'visible': True, 'ascending': False},
                'dateModified': {'index': 2, 'width': 180, 'visible': False, 'ascending': False},
                'size': {'index': 3, 'width': 90, 'visible': True, 'ascending': False},
                'kind': {'index': 4, 'width': 130, 'visible': True, 'ascending': True}}}
        store['.']['vstl'] = ('type', b'Nlsv')
        store['.']['lsvp'] = preferences


def build_document(job, raw=None):
    from docx import Document
    from docx.shared import Pt, RGBColor
    from docx.enum.text import WD_COLOR_INDEX
    from docx.oxml.ns import qn
    job, meta = load_job(job)
    raw = raw if raw is not None else json.loads((job / 'raw-transcript.json').read_text(encoding="utf-8"))
    blocks = make_blocks(raw.get('segments', []))
    if not blocks:
        raise ValueError('识别结果为空，保留媒体，不生成 Word')
    from task_numbering import numbers,document_name
    numbered_name=document_name(numbers(job.parent.parent)[job.name],meta['name'])
    folder = OUTPUT
    folder.mkdir(parents=True, exist_ok=True)
    path = Path(meta['document']) if meta.get('document') and Path(meta['document']).parent == folder else folder / (numbered_name + '.docx')
    if path.exists() and str(path) != meta.get('document'):
        path = folder / (numbered_name + ' (' + job.name + ').docx')
    doc = Document()
    normal = doc.styles['Normal']
    normal.font.name = 'Arial'
    normal.font.size = Pt(11)
    normal.element.rPr.rFonts.set(qn('w:eastAsia'), 'PingFang SC')
    if meta.get('source_kind') == 'local':
        doc.add_paragraph(meta['source_label'])
    else:
        hyperlink(doc.add_paragraph(), meta['url'])
    doc.add_heading(meta['title'], 0)
    notice = doc.add_paragraph().add_run(NOTICE)
    notice.bold = True
    notice.font.color.rgb = RGBColor.from_string('9C0006')
    notice.font.highlight_color = WD_COLOR_INDEX.YELLOW
    doc.add_paragraph('时间戳为原音视频片段的起止范围，并非逐字对齐。' + raw.get('speaker_method', '历史识别结果未区分发言人。'))
    doc.add_heading('语音识别文稿', 1)
    for block in blocks:
        doc.add_paragraph(f'[{stamp(block["start"])}–{stamp(block["end"])}] {block.get("speaker", "")}', 'Caption')
        doc.add_paragraph(block['text'])
    save_json(job/'export-target.json', {'path': str(path), 'url': meta['url']})
    partial = path.with_suffix('.partial.docx')
    doc.save(partial)
    report = verify_document(partial, meta, blocks)
    partial.replace(path)
    # Page order uses the first successful export time; Finder uses the system's added date.
    meta.setdefault('added_at', time.time())
    configure_folder_sort(folder)
    report['document_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    save_json(job / 'validation.json', report)
    meta.update(state='cleaning', document=str(path), blocks=len(blocks),
                language=raw.get('language'), model=raw.get('model', meta.get('model')),
                document_type='raw_asr')
    for key in ('review_flags', 'import_error', 'error', 'cleanup_error'):
        meta.pop(key, None)
    save_json(job / 'job.json', meta)
    try:
        clear_intermediate(job, meta)
    except (OSError, ValueError) as error:
        meta['cleanup_error'] = str(error)
        save_json(job / 'job.json', meta)
    meta['state']='completed'
    save_json(job/'job.json',meta)
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    prep = sub.add_parser('prepare')
    prep.add_argument('url')
    prep.add_argument('--engine', choices=['qianwen'], default='qianwen')
    prep.add_argument('--cookies-browser', choices=['chrome', 'safari', 'firefox', 'edge'])
    export = sub.add_parser('export', help='从已有识别结果生成 Word')
    export.add_argument('job')
    args = parser.parse_args()
    if args.command == 'prepare':
        prepare(args)
    else:
        print(build_document(args.job))


if __name__ == '__main__':
    main()
```

### FILE: requirements.txt
```text
yt-dlp[default]
python-docx
imageio-ffmpeg
send2trash
ds-store
playwright
certifi

portalocker>=3,<4; sys_platform == "win32"
psutil>=6,<8; sys_platform == "win32"
```

### FILE: runtime_compat.py
```text
"""Small platform boundary for Windows 11 x64 and native Apple Silicon Mac."""
import os
from pathlib import Path

IS_WINDOWS = os.name == "nt"


def venv_python(root):
    return Path(root) / '.venv' / ('Scripts/python.exe' if IS_WINDOWS else 'bin/python')


class FileLock:
    LOCK_EX, LOCK_NB, LOCK_UN = 1, 2, 4

    @staticmethod
    def flock(handle, flags):
        import portalocker
        if flags & FileLock.LOCK_UN:
            portalocker.unlock(handle)
            return
        mode = portalocker.LOCK_EX
        if flags & FileLock.LOCK_NB:
            mode |= portalocker.LOCK_NB
        try:
            portalocker.lock(handle, mode)
        except portalocker.exceptions.LockException as error:
            raise BlockingIOError('文件正在被其他进程使用') from error


# Preserve existing Mac flock behavior and interoperability with running versions.
if IS_WINDOWS:
    file_lock = FileLock
else:
    import fcntl as file_lock
```

### FILE: runtime_status.py
```text
"""Read-only runtime inspection. Viewing never stops or changes a task."""
import json,subprocess,time
from pathlib import Path
from runtime_compat import file_lock as fcntl

def snapshot(root,jobs,login):
    from browser_service import endpoint
    work=Path(root)/'work';shared=bool(endpoint());busy=False
    with (work/'qianwen-browser.lock').open('a') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);fcntl.flock(lock,fcntl.LOCK_UN)
        except BlockingIOError:busy=True
    owners=[]
    if busy and not shared:
        result=subprocess.run(['lsof','-t',str(work/'qianwen-browser.lock')],capture_output=True,text=True)
        pids=set(result.stdout.split())
        for job in jobs:
            r=subprocess.run(['lsof','-t',str(work/'jobs'/job['id']/'.prepare.lock')],capture_output=True,text=True)
            if pids.intersection(r.stdout.split()):owners.append(job.get('title') or job['id'])
    items=[]
    for job in jobs:
        record=work/'jobs'/job['id']/'job.json'
        items.append({'id':job['id'],'title':job.get('title') or job['id'],'state':job['state'],'error':job.get('error'),
            'seconds_since_record_update':round(time.time()-record.stat().st_mtime) if record.exists() else None,
            'last_browser_check':job.get('last_browser_check'),
            'uploaded':bool(job.get('qianwen_upload_confirmed'))})
    pages=[];path=work/'browser-live/status.json'
    if path.exists():
        try:
            data=json.loads(path.read_text())
            if time.time()-data['at']<15:pages=data['pages']
        except (ValueError,KeyError):pass
    browser='共享后台浏览器已连接' if shared else ('旧任务占用浏览器：'+'、'.join(owners) if owners else '浏览器被其他进程占用，未确认是登录窗口') if busy else '后台浏览器尚未启动'
    return {'at':time.time(),'browser':browser,'login':login,'tasks':items,'pages':pages}
```

### FILE: smoke_qianwen.py
```text
"""Run the independent cloud workflow from the normal Mac environment."""
import hashlib
import json
import subprocess
import time
from pathlib import Path
import reader
from qianwen_browser import export_audio


def main():
    result={'passed':False,'started_at':time.time()}
    ident=hashlib.sha256(b'qianwen-smoke-test-20-seconds-v2').hexdigest()[:12]
    job=reader.WORK/'jobs'/ident
    (job/'media').mkdir(parents=True,exist_ok=True)
    meta={'url':'',
          'title':'千问独立后台完整测试（仅20秒片段）','name':'千问独立后台完整测试（仅20秒片段）',
          'audio_duration':20,'engine':'qianwen','state':'cloud_transcribing',
          'created_at':time.time()}
    existing=job/'job.json'
    if existing.exists():
        previous=json.loads(existing.read_text())
        for key in ('qianwen_submitted','qianwen_url'): 
            if key in previous:meta[key]=previous[key]
    try:
        candidates=[]
        for other in (reader.WORK/'jobs').glob('*/job.json'):
            data=json.loads(other.read_text())
            audio=Path(data.get('audio','/nonexistent'))
            if other.parent!=job and audio.is_file():candidates.append((other.stat().st_mtime,audio,data))
        if not candidates:
            raise ValueError('测试用的已下载音轨不存在，请让 Codex 选择其他测试音轨。')
        _,source,source_meta=max(candidates,key=lambda item:item[0])
        meta['url']=source_meta['url']
        clip=job/'media'/'test-20-seconds.wav'
        subprocess.run([reader.ffmpeg(),'-nostdin','-v','error','-y','-i',str(source),
                        '-t','20',str(clip)],check=True)
        meta.update(audio=str(clip),media=str(clip))
        reader.save_json(existing,meta)
        print('正在无窗口浏览器中上传20秒测试片段、等待千问转写并导出Word……',flush=True)
        raw=export_audio(clip,job,meta,reader.save_json)
        reader.save_json(job/'raw-transcript.json',raw)
        reader.save_json(existing,meta)
        document=reader.build_document(job,raw)
        result.update(passed=True,document=str(document),elapsed_seconds=round(time.time()-result['started_at'],2),segments=len(raw['segments']))
        print('独立后台完整流程测试通过。Word：'+str(document),flush=True)
    except Exception as error:
        result['error']=str(error)
        # Retain current cloud task identity for a safe retry.
        current=json.loads(existing.read_text()) if existing.exists() else meta
        current.update(state='failed',error=str(error))
        reader.save_json(existing,current)
        print('测试未通过：'+str(error),flush=True)
    finally:
        reader.save_json(reader.WORK/'qianwen-smoke-test.json',result)
    return 0 if result['passed'] else 1


if __name__=='__main__':raise SystemExit(main())
```

### FILE: smoke_qianwen_runner.py
```text
"""A bounded local test runner; retry only on an explicit file request."""
import subprocess
import sys
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
request=ROOT/'work/qianwen-test-request.txt'
last=None
end=time.monotonic()+600
first=True
while time.monotonic()<end:
    current=request.read_text() if request.exists() else ''
    if first or current!=last:
        first=False;last=current
        subprocess.run([sys.executable,str(ROOT/'smoke_qianwen.py')])
        print('测试结果已保存。保留此窗口即可，接下来十分钟内可后台重试；按Ctrl+C结束。',flush=True)
    time.sleep(1)
```

### FILE: start-windows.cmd
```text
@echo off
cd /d "%~dp0"
powershell.exe -NoProfile -File "%~dp0install-windows.ps1" -StartOnly -Open %*
set "install_result=%errorlevel%"
if not "%install_result%"=="0" pause
exit /b %install_result%
```

### FILE: task_controls.py
```text
"""Stop one verified reader and move its local artifacts to the Trash."""
import json
import os
import re
import shlex
import signal
import subprocess
import time
from pathlib import Path


def reader_pids(root, folder):
    if os.name == 'nt':
        import psutil
        verified = []
        for process in psutil.process_iter(['pid', 'cmdline']):
            try:
                args = process.info['cmdline'] or []
                if len(args) >= 4 and Path(args[1]).resolve() == (root/'reader.py').resolve() and args[2] == 'prepare' and args[3] == json.loads((folder/'job.json').read_text(encoding='utf-8'))['url']:
                    verified.append(process.pid)
            except (psutil.NoSuchProcess, psutil.AccessDenied, OSError, ValueError):
                continue
        return verified
    result=subprocess.run(['/usr/sbin/lsof','-t',str(folder/'.prepare.lock')],capture_output=True,text=True)
    verified=[]
    for value in result.stdout.split():
        pid=int(value)
        command=subprocess.run(['/bin/ps','-p',str(pid),'-o','command='],capture_output=True,text=True)
        args=shlex.split(command.stdout.strip())
        if len(args)>=3 and args[1]==str(root/'reader.py') and args[2]=='prepare':verified.append(pid)
    return verified


def stop_reader(pid):
    if os.name == 'nt':
        import psutil
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            for process in reversed(children):
                try: process.terminate()
                except psutil.NoSuchProcess: pass
            parent.terminate()
            psutil.wait_procs(children + [parent], timeout=10)
        except psutil.NoSuchProcess:
            pass
        return
    children=subprocess.run(['/usr/bin/pgrep','-P',str(pid)],capture_output=True,text=True)
    for child in children.stdout.split():stop_reader(int(child))
    try:os.kill(pid,signal.SIGTERM)
    except ProcessLookupError:pass


def trash_task(root, work, output_roots, ident):
    from send2trash import send2trash
    from docx import Document
    from runtime_compat import file_lock as fcntl
    if not re.fullmatch('[0-9a-f]{12}',ident):raise ValueError('任务编号不合法')
    folder=work/'jobs'/ident
    if folder.is_symlink() or not folder.exists():raise ValueError('任务不存在')
    meta=json.loads((folder/'job.json').read_text(encoding="utf-8"))
    (folder/'.deleting').touch()
    for pid in reader_pids(root,folder):stop_reader(pid)
    # Do not remove files until the reader has actually relinquished ownership.
    with (folder/'.prepare.lock').open('a') as lock:
        deadline=time.monotonic()+15
        while True:
            try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);break
            except BlockingIOError:
                if time.monotonic()>deadline:
                    (folder/'.deleting').unlink(missing_ok=True)
                    raise ValueError('任务尚未停止，未删除文件。请稍后重试。')
                time.sleep(.2)
        meta=json.loads((folder/'job.json').read_text(encoding="utf-8"))
        candidates=set()
        owned=set()
        reservation=folder/'export-target.json'
        if reservation.exists():
            record=json.loads(reservation.read_text(encoding="utf-8"))
            if record.get('url')==meta.get('url'):
                target=Path(record['path'])
                owned.update([target,target.with_suffix('.partial.docx')])
                candidates.update(owned)
        if meta.get('document'):
            candidates.add(Path(meta['document']));owned.add(Path(meta['document']))
        name=meta.get('name')
        if name:
            for base in output_roots:
                for suffix in ('.docx','.partial.docx'):
                    candidates.add(base/(name+suffix))
                    candidates.add(base/(name+' ('+ident+')'+suffix))
        for path in candidates:
            if path.exists() and (path.is_symlink() or not any(base.resolve() in path.resolve().parents for base in output_roots)):
                raise ValueError('文稿路径不属于工具输出目录，未删除任务')
        for path in candidates:
            if not path.exists():continue
            if path.is_symlink() or not any(base.resolve() in path.resolve().parents for base in output_roots):
                raise ValueError('文稿路径不属于工具输出目录，未删除任务')
            try:
                paragraphs=Document(path).paragraphs
                belongs=path in owned or bool(paragraphs and paragraphs[0].text==meta.get('url'))
            except Exception:
                # An incomplete file is owned only if it was explicitly recorded.
                belongs=str(path)==meta.get('document') or path in owned
                if not belongs and path.suffix=='.docx' and '.partial' in path.name:
                    raise ValueError('无法确认未完成文稿的归属，已保留文件，请检查')
            if belongs:send2trash(str(path.resolve()))
        for base in output_roots[1:]:
            legacy=base/ident
            if legacy.is_dir() and not legacy.is_symlink():send2trash(str(legacy.resolve()))
        # Windows cannot recycle a directory containing an open lock handle.
        if os.name == 'nt':
            fcntl.flock(lock, fcntl.LOCK_UN)
            lock.close()
        send2trash(str(folder.resolve()))
    return {'ok':True,'message':'本机任务与相关文件已移入废纸篓。千问云端记录需在千问网页中管理。'}
```

### FILE: task_numbering.py
```text
"""Persistent task IDs: deletion never releases a sequence number."""
import json,time
from pathlib import Path
from runtime_compat import file_lock as fcntl

def numbers(work):
    work=Path(work);work.mkdir(parents=True,exist_ok=True)
    with (work/'task-numbers.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        path=work/'task-numbers.json'
        ledger=json.loads(path.read_text()) if path.exists() else {'next':1,'tasks':{}}
        ledger.setdefault('created',{})
        pending=[]
        for record in (work/'jobs').glob('*/job.json'):
            meta=json.loads(record.read_text());stat=record.parent.stat()
            created=meta.get('created_at',getattr(stat,'st_birthtime',stat.st_mtime))
            ident=record.parent.name
            if ident in ledger['tasks'] and ledger['created'].get(ident,created)==created:
                ledger['created'][ident]=created;continue
            pending.append((created,ident))
        for created,ident in sorted(pending):
            ledger['created'][ident]=created
            ledger['tasks'][ident]=ledger['next'];ledger['next']+=1
        from reader import save_json
        save_json(path,ledger)
        return dict(ledger['tasks'])

def document_name(number,name):return f'{number} - {name}'

def migrate_documents(work,output):
    """Rename only recorded completed documents; never touch a running reader."""
    from reader import save_json,configure_folder_sort
    mapping=numbers(work);output=Path(output);renamed=[]
    for record in (Path(work)/'jobs').glob('*/job.json'):
        with (record.parent/'.prepare.lock').open('a') as lock:
            try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError:continue
            meta=json.loads(record.read_text())
            if meta.get('state')!='completed' or not meta.get('document'):continue
            old=Path(meta['document'])
            if old.parent.resolve()!=output.resolve() or not old.is_file() or old.is_symlink():continue
            new=output/(document_name(mapping[record.parent.name],meta['name'])+'.docx')
            if new!=old:
                if new.exists():raise ValueError('编号文稿名称已存在，未覆盖：'+new.name)
                old.rename(new);meta['document']=str(new);save_json(record,meta)
                save_json(record.parent/'export-target.json',{'path':str(new),'url':meta['url']})
                renamed.append(new.name)
    if output.exists():configure_folder_sort(output)
    return renamed
```

### FILE: test_app.py
```text
import json
import tempfile
import queue
import unittest
from pathlib import Path
from unittest.mock import patch
from docx import Document
import app


class PageTests(unittest.TestCase):
    def fixture(self, root):
        job = root / 'work/jobs/123456abcdef'
        job.mkdir(parents=True)
        output = root / 'downloads'
        output.mkdir()
        path = output / '文稿.docx'
        doc = Document()
        doc.add_paragraph('https://example.com/video')
        doc.add_heading('测试标题', 0)
        doc.add_paragraph(app.NOTICE)
        doc.add_paragraph('全文末尾 <script>不能执行</script>')
        doc.save(path)
        (job / 'job.json').write_text(json.dumps({'document': str(path)}), encoding="utf-8")
        return job, output, path

    def test_preview_contains_saved_text_and_notice(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            job, output, path = self.fixture(root)
            with patch.object(app, 'WORK', root / 'work'), patch.object(app, 'OUTPUT', output):
                page = app.preview_document(job.name).decode()
            self.assertIn('全文末尾 &lt;script&gt;不能执行&lt;/script&gt;', page)
            self.assertIn(app.NOTICE, page)
            self.assertIn('class=notice', page)
            self.assertNotIn('<script>', page)

    def test_reveal_exact_document_without_shell(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            job, output, path = self.fixture(root)
            with patch.object(app, 'WORK', root / 'work'), patch.object(app, 'OUTPUT', output), patch('app.subprocess.run') as run, patch('app.os.startfile', create=True) as startfile:
                run.return_value.returncode = 0
                app.reveal_document(job.name)
                if app.os.name == 'nt':
                    startfile.assert_called_once_with(str(path.resolve().parent))
                    run.assert_not_called()
                else:
                    run.assert_called_once_with(['/usr/bin/open', '-a', 'Finder', str(path.resolve().parent)], capture_output=True, text=True, timeout=15)
                path.unlink()
                with self.assertRaises(ValueError):
                    app.reveal_document(job.name)

    def test_queued_title_is_read_from_separate_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            job = root / 'jobs/123456abcdef'
            job.mkdir(parents=True)
            (job / 'job.json').write_text(json.dumps({'url': 'https://example.com/v', 'state': 'queued'}), encoding="utf-8")
            (job / 'page-title.json').write_text(json.dumps({'title': '对话视频'}), encoding="utf-8")
            with patch.object(app, 'WORK', root):
                items = app.list_jobs()
            self.assertEqual(items[0]['title'], '对话视频')
            self.assertEqual(items[0]['state'], 'queued')

    def test_title_lookup_does_not_overwrite_active_progress(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            job = root / 'jobs/123456abcdef'
            job.mkdir(parents=True)
            meta = {'url': 'https://example.com/v', 'state': 'transcribing', 'transcribed_seconds': 123}
            (job / 'job.json').write_text(json.dumps(meta), encoding="utf-8")
            with patch.object(app, 'WORK', root), patch('app.subprocess.run') as run:
                run.return_value.returncode = 0
                run.return_value.stdout = '对话标题\n'
                app.fetch_title(job.name, meta['url'])
            self.assertEqual(json.loads((job / 'job.json').read_text(encoding="utf-8")), meta)
            self.assertEqual(json.loads((job / 'page-title.json').read_text(encoding="utf-8"))['title'], '对话标题')

    def test_restart_recovers_only_unfinished_in_original_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for ident, state, created in [('000000000001','queued',3), ('000000000002','transcribing',1),
                                           ('000000000003','completed',2), ('000000000004','failed',4)]:
                folder = root / 'jobs' / ident
                folder.mkdir(parents=True)
                (folder/'job.json').write_text(json.dumps({'state':state,'created_at':created,'url':'https://example.com/'+ident}), encoding="utf-8")
            restored = queue.Queue()
            with patch.object(app,'WORK',root), patch.object(app,'tasks',restored), patch.object(app,'pending',set()), patch('app.start_title_lookup'):
                app.resume_jobs()
                self.assertEqual(restored.get_nowait()[0], '000000000002')
                self.assertEqual(restored.get_nowait()[0], '000000000001')
                self.assertTrue(restored.empty())


class WorkerFailureTests(unittest.TestCase):
    def test_launch_failure_is_visible_and_next_job_runs(self):
        from unittest.mock import MagicMock
        with tempfile.TemporaryDirectory() as tmp:
            work=Path(tmp)
            identifiers=['000000000001','000000000002']
            for ident in identifiers:
                folder=work/'jobs'/ident;folder.mkdir(parents=True)
                (folder/'job.json').write_text(json.dumps({'url':'https://example.com/'+ident,'state':'queued','engine':'qianwen'}), encoding="utf-8")
            fakequeue=MagicMock()
            fakequeue.get.side_effect=[(ident,'https://example.com/'+ident,ident) for ident in identifiers]+[StopIteration()]
            process=MagicMock();process.wait.return_value=0
            with patch.object(app,'WORK',work),patch.object(app,'tasks',fakequeue),patch.object(app,'pending',set(identifiers)),patch.object(app,'generations',{}),patch.object(app,'cancelled',set()),patch.object(app,'active_readers',{}),patch('app.subprocess.Popen',side_effect=[OSError('launch failed'),process]) as run:
                with self.assertRaises(StopIteration):app.worker()
            first=json.loads((work/'jobs'/identifiers[0]/'job.json').read_text(encoding="utf-8"))
            self.assertEqual(first['state'],'failed');self.assertIn('launch failed',first['error'])
            self.assertEqual(run.call_count,2)
            self.assertEqual(fakequeue.task_done.call_count,2)

class LocalUploadTests(unittest.TestCase):
    def test_rejects_incomplete_upload_without_queuing_or_residue(self):
        import io
        with tempfile.TemporaryDirectory() as tmp,patch.object(app,'WORK',Path(tmp)),patch.object(app,'enqueue') as enqueue:
            with self.assertRaisesRegex(ValueError,'上传中断'):
                app.receive_upload(io.BytesIO(b'abc'),10,'test.mp3')
            enqueue.assert_not_called()
            self.assertFalse(list((Path(tmp)/'jobs').glob('*/job.json')))

    def test_http_upload_streams_file_and_preserves_chinese_name(self):
        import http.client, threading
        from urllib.parse import quote
        from http.server import ThreadingHTTPServer
        server=ThreadingHTTPServer(('127.0.0.1',0),app.Handler)
        port=server.server_port
        with tempfile.TemporaryDirectory() as tmp,patch.object(app,'WORK',Path(tmp)),patch.object(app,'PORT',port),patch.object(app,'enqueue',return_value='123456abcdef') as enqueue:
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            try:
                conn=http.client.HTTPConnection('127.0.0.1',port)
                conn.request('POST','/upload',body=b'example-audio',headers={'Origin':f'http://127.0.0.1:{port}','X-File-Name':quote('采访.mp3'),'Content-Type':'application/octet-stream'})
                response=conn.getresponse();result=json.loads(response.read());conn.close()
                self.assertEqual(response.status,200);self.assertEqual(result['id'],'123456abcdef')
                enqueue.assert_called_once()
                meta=json.loads(next((Path(tmp)/'jobs').glob('*/job.json')).read_text(encoding="utf-8"))
                self.assertEqual(meta['source_label'],'本地上传文件：采访.mp3')
                self.assertEqual(Path(meta['media']).read_bytes(),b'example-audio')
            finally:server.shutdown();server.server_close();thread.join()

    def test_unsupported_file_rejected_before_writing(self):
        import io
        with tempfile.TemporaryDirectory() as tmp,patch.object(app,'WORK',Path(tmp)):
            with self.assertRaises(ValueError):app.receive_upload(io.BytesIO(b'abc'),3,'a.command')
            self.assertFalse((Path(tmp)/'jobs').exists())

class SynchronizedDeleteTests(unittest.TestCase):
    def test_missing_cloud_record_success_reports_all_three_elements(self):
        report=app.deletion_report(True,'not_found')
        self.assertEqual(report['status'],'success')
        self.assertEqual(len(report['elements']),3)
        self.assertIn('未找到对应千问记录',report['elements'][2]['detail'])
        self.assertIn('删除成功',report['elements'][0]['detail'])

    def test_partial_failure_keeps_cloud_success_in_report(self):
        report=app.deletion_report(False,'deleted','文件被占用')
        self.assertEqual(report['elements'][2]['detail'],'删除成功')
        self.assertEqual([e['status'] for e in report['elements']],['failed','failed','success'])
        self.assertIn('未全部删除成功',report['elements'][1]['detail'])
        self.assertIn('文件被占用',report['message'])

    def test_failed_deletion_result_survives_task_list_refresh(self):
        with tempfile.TemporaryDirectory() as tmp:
            work=Path(tmp);folder=work/'jobs/123456abcdef';folder.mkdir(parents=True)
            (folder/'job.json').write_text(json.dumps({'state':'completed','created_at':1}), encoding="utf-8")
            (folder/'delete-result.json').write_text(json.dumps({'status':'failed','message':'删除失败：登录失效'}), encoding="utf-8")
            with patch.object(app,'WORK',work):
                self.assertEqual(app.list_jobs()[0]['deletion_result']['message'],'删除失败：登录失效')

    def test_successful_delete_removes_task_from_list(self):
        import shutil
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory() as tmp:
            work=Path(tmp);folder=work/'jobs/123456abcdef';folder.mkdir(parents=True)
            (folder/'job.json').write_text(json.dumps({'state':'completed','created_at':1}), encoding="utf-8")
            def trash(root,work,outputs,ident):
                shutil.rmtree(work/'jobs'/ident)
                return {'ok':True}
            with patch.object(app,'WORK',work),patch('task_controls.reader_pids',return_value=[]),patch('task_controls.trash_task',side_effect=trash),patch('app.subprocess.run',return_value=SimpleNamespace(returncode=0)):
                self.assertEqual(len(app.list_jobs()),1)
                self.assertTrue(app.delete_task('123456abcdef')['ok'])
                self.assertEqual(app.list_jobs(),[])

    def test_cloud_failure_preserves_local_document_and_task(self):
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory() as tmp:
            work=Path(tmp);folder=work/'jobs/123456abcdef';folder.mkdir(parents=True)
            doc=work/'keep.docx';doc.write_bytes(b'keep')
            (folder/'job.json').write_text(json.dumps({'state':'completed','document':str(doc)}), encoding="utf-8")
            with patch.object(app,'WORK',work),patch('task_controls.reader_pids',return_value=[]),patch('task_controls.trash_task') as trash,patch('app.subprocess.run',return_value=SimpleNamespace(returncode=1,stderr='登录失效')):
                with self.assertRaisesRegex(ValueError,'登录失效'):app.delete_task('123456abcdef')
                trash.assert_not_called()
            self.assertTrue(doc.exists());self.assertTrue((folder/'job.json').exists())
            self.assertFalse((folder/'.deleting').exists())

if __name__ == '__main__':
    unittest.main()
```

### FILE: test_bilibili_download.py
```text
import unittest
from unittest.mock import patch
from bilibili_download import BiliBiliPageFallbackIE
class FallbackTests(unittest.TestCase):
 def test_optional_voucher_does_not_override_page(self):
  ie=BiliBiliPageFallbackIE()
  with patch('yt_dlp.extractor.bilibili.BiliBiliIE._download_playinfo',return_value={'v_voucher':'test'}),patch.object(ie,'extract_formats',return_value=[]),patch.object(ie,'report_warning'),patch.object(ie,'_download_webpage',return_value=None):
   self.assertIsNone(ie._download_playinfo('video','cid',fatal=False))
 def test_playable_api_kept(self):
  ie=BiliBiliPageFallbackIE();info={'dash':{'audio':[]}}
  with patch('yt_dlp.extractor.bilibili.BiliBiliIE._download_playinfo',return_value=info):self.assertIs(ie._download_playinfo('video','cid',fatal=False),info)
 def test_required_api_not_suppressed(self):
  ie=BiliBiliPageFallbackIE();info={'v_voucher':'test'}
  with patch('yt_dlp.extractor.bilibili.BiliBiliIE._download_playinfo',return_value=info):self.assertIs(ie._download_playinfo('video','cid'),info)

 def test_matching_page_streams_used(self):
  ie=BiliBiliPageFallbackIE();api={'v_voucher':'test'};play={'dash':{'audio':[{'id':1}]}}
  with patch('yt_dlp.extractor.bilibili.BiliBiliIE._download_playinfo',return_value=api),patch.object(ie,'extract_formats',side_effect=lambda data: [] if data==api else [{'url':'media'}]),patch.object(ie,'report_warning'),patch.object(ie,'_download_webpage',return_value='page'),patch.object(ie,'_search_json',side_effect=[{'videoData':{'cid':123}},{'data':play}]):
   self.assertIs(ie._download_playinfo('BVtest',123,fatal=False),play)
 def test_other_episode_not_used(self):
  ie=BiliBiliPageFallbackIE()
  with patch('yt_dlp.extractor.bilibili.BiliBiliIE._download_playinfo',return_value={'v_voucher':'test'}),patch.object(ie,'extract_formats',return_value=[]),patch.object(ie,'report_warning'),patch.object(ie,'_download_webpage',return_value='page'),patch.object(ie,'_search_json',return_value={'videoData':{'cid':999}}):
   self.assertIsNone(ie._download_playinfo('BVtest',123,fatal=False))
```

### FILE: test_browser_service.py
```text
import unittest
from unittest.mock import Mock,patch
from qianwen_browser import browser_context
class SharedPagesTests(unittest.TestCase):
 def test_each_client_owns_only_its_page(self):
  p=Mock();browser=p.chromium.connect_over_cdp.return_value;context=Mock();browser.contexts=[context]
  first,second=Mock(),Mock();context.new_page.side_effect=[first,second]
  with patch('browser_service.endpoint',return_value='ws://127.0.0.1:18769/devtools/browser/test'), patch('qianwen_browser.TaskContext',side_effect=lambda ctx: Mock(page=ctx.new_page(),pages=[])):
   # Exercise close ownership using independent page wrappers.
   from qianwen_browser import TaskContext
   TaskContext.side_effect=lambda ctx: type('Owned',(),{'page':(page:=ctx.new_page()),'pages':[page],'owner':Mock()})()
   with browser_context(p) as one:
    with browser_context(p) as two:
     self.assertIs(one.pages[0],first);self.assertIs(two.pages[0],second)
    second.close.assert_called_once();first.close.assert_not_called()
   first.close.assert_called_once();context.close.assert_not_called()
 def test_shared_browser_is_not_busy_for_deletion(self):
  from deletion_queue import browser_busy
  with patch('browser_service.endpoint',return_value='ws://localhost/test'):
   self.assertFalse(browser_busy('/unused'))

class LoginDiagnosticsTests(unittest.TestCase):
 def test_endpoint_explicitly_bypasses_proxy(self):
  from browser_service import endpoint
  import json
  response=Mock();response.__enter__=Mock(return_value=response);response.__exit__=Mock(return_value=False)
  response.read.return_value=json.dumps({'webSocketDebuggerUrl':'ws://127.0.0.1/test'}).encode()
  with patch('urllib.request.ProxyHandler') as proxy,patch('urllib.request.build_opener') as opener:
   opener.return_value.open.return_value=response
   self.assertEqual(endpoint(),'ws://127.0.0.1/test');proxy.assert_called_once_with({})
 def test_login_failure_surfaces_actual_busy_reason(self):
  import app,tempfile,json,time
  from pathlib import Path
  with tempfile.TemporaryDirectory() as tmp:
   work=Path(tmp);(work/'qianwen-auth.json').write_text('{}')
   (work/'qianwen-login-result.json').write_text(json.dumps({'error':'旧任务占用浏览器'}))
   process=Mock();process.poll.return_value=1
   with patch.object(app,'WORK',work),patch.object(app,'login_process',process),patch.object(app,'auth_check_started',time.time()),patch.object(app,'list_jobs',return_value=[]):
    self.assertEqual(app.login_status()['error'],'旧任务占用浏览器')
```

### FILE: test_deletion_queue.py
```text
import tempfile,json,unittest
from pathlib import Path
from unittest.mock import Mock,patch
from deletion_queue import DeletionQueue
class QueueTests(unittest.TestCase):
 def setup_queue(self):
  tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);work=Path(tmp.name);job=work/'jobs/123456abcdef';job.mkdir(parents=True);(job/'job.json').write_text('{}')
  delete=Mock(return_value={'deletion_result':{'status':'success','at':1}});failed=Mock(return_value={'status':'failed','at':1});q=DeletionQueue(work,delete,failed)
  return q,delete,failed,job
 def test_busy_waits_and_free_executes(self):
  q,delete,failed,job=self.setup_queue();self.assertEqual(q.submit(job.name)['status'],'pending')
  with patch('deletion_queue.browser_busy',return_value=True):q.run_once()
  delete.assert_not_called();failed.assert_not_called();self.assertTrue(q.has_pending())
  with patch('deletion_queue.browser_busy',return_value=False):q.run_once()
  delete.assert_called_once_with(job.name);self.assertFalse(q.has_pending())
 def test_restart_and_duplicate_submit(self):
  q,delete,failed,job=self.setup_queue();q.submit(job.name);q.submit(job.name)
  self.assertEqual(len(list(q.folder.glob('*.json'))),1)
  restored=DeletionQueue(q.work,delete,failed)
  with patch('deletion_queue.browser_busy',return_value=False):restored.run_once()
  delete.assert_called_once()
 def test_nonbusy_failure_is_reported(self):
  q,delete,failed,job=self.setup_queue();q.submit(job.name);delete.side_effect=ValueError('登录失效')
  with patch('deletion_queue.browser_busy',return_value=False):q.run_once()
  failed.assert_called_once_with(job.name,'登录失效');self.assertFalse(q.has_pending())
 def test_lock_race_stays_pending(self):
  q,delete,failed,job=self.setup_queue();q.submit(job.name);delete.side_effect=ValueError('千问浏览器正在使用中')
  with patch('deletion_queue.browser_busy',return_value=False):q.run_once()
  failed.assert_not_called();self.assertTrue(q.has_pending())
 def test_expired_queue_has_clear_failure(self):
  q,delete,failed,job=self.setup_queue();q.submit(job.name);p=q.folder/(job.name+'.json');d=json.loads(p.read_text());d['created_at']=0;p.write_text(json.dumps(d));q.run_once()
  delete.assert_not_called();self.assertIn('超过6小时',failed.call_args.args[1]);self.assertFalse(q.has_pending())

class QueueHTTPTests(unittest.TestCase):
 def test_delete_returns_pending_without_claiming_success(self):
  import app,http.client,threading
  from http.server import ThreadingHTTPServer
  fake=Mock();fake.submit.return_value= {'status':'pending','message':'等待千问浏览器空闲'}
  server=ThreadingHTTPServer(('127.0.0.1',0),app.Handler)
  with patch.object(app,'PORT',server.server_port),patch.object(app,'get_deletion_queue',return_value=fake):
   thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
   try:
    conn=http.client.HTTPConnection('127.0.0.1',server.server_port)
    conn.request('POST','/delete/123456abcdef',body='{}',headers={'Content-Type':'application/json','Origin':f'http://127.0.0.1:{server.server_port}'})
    response=conn.getresponse();data=json.loads(response.read())
    self.assertEqual(response.status,202);self.assertEqual(data['deletion_result']['status'],'pending')
    fake.submit.assert_called_once_with('123456abcdef');conn.close()
   finally:server.shutdown();server.server_close();thread.join()
```

### FILE: test_export_download.py
```text
import unittest,tempfile,base64,io,zipfile
from pathlib import Path
from unittest.mock import Mock
from qianwen_browser import save_export_download
class ExportTests(unittest.TestCase):
 def test_cancelled_download_uses_same_page_and_validates_word(self):
  stream=io.BytesIO()
  with zipfile.ZipFile(stream,'w') as z:z.writestr('word/document.xml','<document/>')
  download=Mock();download.save_as.side_effect=RuntimeError('Download.save_as: canceled');download.url='blob:export'
  page=Mock();page.evaluate.return_value=base64.b64encode(stream.getvalue()).decode()
  with tempfile.TemporaryDirectory() as tmp:
   target=Path(tmp)/'original.docx';save_export_download(download,page,target);self.assertEqual(target.read_bytes(),stream.getvalue())
  self.assertEqual(page.evaluate.call_args.args[1],'blob:export')
 def test_invalid_download_not_saved(self):
  download=Mock();download.save_as.side_effect=RuntimeError('canceled');page=Mock();page.evaluate.return_value=base64.b64encode(b'<html>login</html>').decode()
  with tempfile.TemporaryDirectory() as tmp:
   target=Path(tmp)/'original.docx'
   with self.assertRaises(RuntimeError):save_export_download(download,page,target)
   self.assertFalse(target.exists())
```

### FILE: test_install.py
```text
"""Installer safety and recovery regressions; no network/login in unit tests."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import install


class InstallerTests(unittest.TestCase):
    def test_platform_rejected_before_commands(self):
        with patch.object(install.platform, 'system', return_value='Linux'), patch.object(install, 'run') as run:
            with self.assertRaisesRegex(RuntimeError, 'Windows'):
                install.main([])
            run.assert_not_called()

    def test_wrong_node_version_or_arch_rejected(self):
        for version, arch in [('20.0.0', 'arm64'), ('22.0.0', 'x64')]:
            with self.subTest(version=version, arch=arch), patch.object(install.platform, 'system', return_value='Darwin'), patch.object(install.platform, 'machine', return_value='arm64'), patch.object(install.sys, 'version_info', (3,12)), patch.object(install.shutil, 'which', return_value='/node'), patch.object(install.subprocess, 'check_output', return_value=json.dumps(dict(version=version, arch=arch))):
                with self.assertRaisesRegex(RuntimeError, 'Node.js 22'):
                    install.check_environment()

    def test_broken_venv_preserved_and_rebuilt(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(install, 'ROOT', Path(tmp)), patch.object(install, 'run') as run:
            folder = Path(tmp) / '.venv'
            folder.mkdir()
            (folder / 'marker').write_text('preserve', encoding="utf-8")
            install.ensure_venv()
            backups = list(Path(tmp).glob('.venv.backup-*'))
            self.assertEqual(len(backups), 1)
            self.assertEqual((backups[0] / 'marker').read_text(encoding="utf-8"), 'preserve')
            self.assertEqual(run.call_args.args[0][-2:], ['venv', folder])

    def test_healthy_venv_reused(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(install, 'ROOT', Path(tmp)), patch.object(install, 'run') as run:
            python = install.venv_python(Path(tmp))
            python.parent.mkdir(parents=True)
            python.touch()
            info = [[3,12], install.platform.machine(), str(Path(tmp)/'.venv'), '/base']
            with patch.object(install.subprocess, 'check_output', return_value=json.dumps(info)):
                self.assertEqual(install.ensure_venv(), python)
            run.assert_not_called()

    def test_symlink_environment_not_modified(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(install, 'ROOT', Path(tmp)), patch.object(install, 'run') as run:
            try:
                (Path(tmp)/'.venv').symlink_to(Path(tmp)/'other')
            except OSError:
                self.skipTest('Windows symlink privilege unavailable')
            with self.assertRaisesRegex(RuntimeError, '符号链接'):
                install.ensure_venv()
            run.assert_not_called()

    def test_foreign_service_never_started_or_stopped(self):
        with patch.object(install, 'health', return_value={'ok':True,'project':'/other','engines':['qianwen']}), patch.object(install.subprocess, 'Popen') as popen:
            with self.assertRaisesRegex(RuntimeError, '不是本目录'):
                install.start_service(Path('/python'), 8767)
            popen.assert_not_called()

    def test_same_service_reused(self):
        with patch.object(install, 'health', return_value={'ok':True,'project':str(install.ROOT),'engines':['qianwen']}), patch.object(install.subprocess, 'Popen') as popen:
            install.start_service(Path('/python'), 8767)
            popen.assert_not_called()

    def test_health_requires_cloud_only(self):
        for data in ([], {'ok':False,'project':str(install.ROOT),'engines':['qianwen']}, {'ok':True,'project':str(install.ROOT),'engines':['local']}):
            with self.assertRaises(RuntimeError):
                install.validate_health(data)

    def test_failed_dependency_stops_before_start(self):
        with patch.object(install, 'check_environment'), patch.object(install, 'ensure_venv', return_value=Path('/python')), patch.object(install, 'run', side_effect=subprocess.CalledProcessError(1, 'pip')), patch.object(install, 'start_service') as start:
            with self.assertRaises(subprocess.CalledProcessError):
                install.main([])
            start.assert_not_called()

    def test_no_start_runs_all_acceptance_steps(self):
        with patch.object(install, 'check_environment'), patch.object(install, 'ensure_venv', return_value=Path('/python')), patch.object(install, 'run') as run, patch.object(install, 'start_service') as start:
            install.main(['--no-start'])
            commands = [list(map(str,c.args[0])) for c in run.call_args_list]
            self.assertTrue(any(c[1:]==['-m','pip','check'] for c in commands))
            self.assertTrue(any(c[1:]==['-m','playwright','install','chromium'] for c in commands))
            self.assertTrue(any('unittest' in c and all(t in c for t in install.TESTS) for c in commands))
            start.assert_not_called()

if __name__ == '__main__':
    unittest.main()
```

### FILE: test_qianwen.py
```text
import tempfile
import unittest
from pathlib import Path
from docx import Document
from qianwen_browser import read_export

class QianwenExportTests(unittest.TestCase):
    def test_unconfirmed_upload_suggests_login_and_preserves_cause(self):
        from qianwen_browser import upload_failure_message
        for state in ('cloud_connecting','cloud_uploading','cloud_confirming_upload'):
            message=upload_failure_message(state,'上传按钮等待超时')
            self.assertIn('上传按钮等待超时',message)
            self.assertIn('可能千问未登录',message)
            self.assertIn('登录或打开千问',message)

    def test_explicit_other_failures_do_not_suggest_login(self):
        from qianwen_browser import upload_failure_message
        for message in ('千问账号云端存储已满','超过500MB限制','千问需要登录'):
            self.assertEqual(upload_failure_message('cloud_uploading',message),message)
        for state in ('downloading','cloud_preparing','cloud_transcribing','generating_document'):
            self.assertEqual(upload_failure_message(state,'失败'),'失败')

    def export(self, lines):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        path=Path(temp.name)/'export.docx';doc=Document()
        for line in lines:doc.add_paragraph(line)
        doc.save(path);return path
    def test_preserves_all_paragraphs_and_speakers(self):
        p=self.export(['标题','2026年10月07日','发言人1   00:00','第一段。','继续讲话。','发言人2   00:12','第二段。'])
        result=read_export(p,20)
        self.assertEqual(result['segments'],[{'start':0,'end':12,'speaker':'发言人1','text':'第一段。\n继续讲话。'},{'start':12,'end':20,'speaker':'发言人2','text':'第二段。'}])
    def test_rejects_missing_timestamps(self):
        with self.assertRaises(ValueError):read_export(self.export(['只有正文']),20)
    def test_rejects_wrong_duration(self):
        with self.assertRaises(ValueError):read_export(self.export(['发言人1   01:00','正文']),20)
    def test_rejects_empty_segment(self):
        with self.assertRaises(ValueError):read_export(self.export(['发言人1   00:00']),20)

class RecoveryTests(unittest.TestCase):
    def test_download_certificate_bundle_loads_trusted_roots(self):
        import certifi,ssl
        context=ssl.create_default_context(cafile=certifi.where())
        self.assertGreater(context.cert_store_stats()['x509_ca'],0)
        self.assertEqual(context.verify_mode,ssl.CERT_REQUIRED)

    def test_timeout_reuses_saved_cloud_document(self):
        from unittest.mock import patch
        from playwright.sync_api import TimeoutError
        import qianwen_browser as browser
        meta={};calls=[]
        def export(audio,job,record,save):
            calls.append(record.get('qianwen_url'))
            if len(calls)==1:
                record.update(qianwen_submitted=True,qianwen_url='https://www.qianwen.com/efficiency/doc/transcripts/test')
                raise TimeoutError('loading')
            return {'model':'qianwen-web'}
        with patch.object(browser,'export_audio',side_effect=export),patch.object(browser.time,'sleep'):
            result=browser.export_with_retry(None,Path('/tmp/test'),meta,lambda *args:None)
        self.assertEqual(result['model'],'qianwen-web')
        self.assertEqual(calls,[None,meta['qianwen_url']])

    def test_login_error_is_not_retried(self):
        from unittest.mock import patch
        import qianwen_browser as browser
        with patch.object(browser,'export_audio',side_effect=browser.LoginRequired('login')) as run:
            with self.assertRaises(browser.LoginRequired):browser.export_with_retry(None,Path('/tmp/test'),{},lambda *args:None)
        self.assertEqual(run.call_count,1)

    def test_timeout_retry_is_bounded(self):
        from unittest.mock import patch
        from playwright.sync_api import TimeoutError
        import qianwen_browser as browser
        with patch.object(browser,'export_audio',side_effect=TimeoutError('loading')) as run,patch.object(browser.time,'sleep'):
            with self.assertRaises(TimeoutError):browser.export_with_retry(None,Path('/tmp/test'),{},lambda *args:None)
        self.assertEqual(run.call_count,3)

    def test_export_options_wait_before_selection(self):
        from unittest.mock import MagicMock,patch
        import qianwen_browser as browser
        page=MagicMock();panel=page.get_by_role.return_value.filter.return_value.first
        checks=panel.get_by_role.return_value
        with patch('playwright.sync_api.expect') as expect:
            browser.export_panel(page,Path('/tmp/test'))
            panel.wait_for.assert_called_once_with(state='visible',timeout=30000)
            expect.assert_called_once_with(checks)
            expect.return_value.to_have_count.assert_called_once_with(5,timeout=30000)
        checks.count.assert_not_called()

class UploadConfirmationTests(unittest.TestCase):
    def page(self):
        from unittest.mock import MagicMock
        page=MagicMock()
        page.get_by_role.return_value.filter.return_value.all.return_value=[]
        page.get_by_role.return_value.all.return_value=[]
        page.locator.return_value.inner_text.return_value='最近记录'
        return page

    def test_submission_requires_visible_record(self):
        import qianwen_browser as browser
        page=self.page();meta={'qianwen_submission_attempted':True}
        with tempfile.TemporaryDirectory() as tmp:
            browser.confirm_submission(page,'test-task',Path(tmp),meta,lambda *args:None)
        page.get_by_text.return_value.filter.return_value.first.wait_for.assert_called_once_with(timeout=1000)
        self.assertTrue(meta['qianwen_upload_confirmed'])
        self.assertEqual(meta['state'],'cloud_transcribing')

    def test_absent_record_does_not_claim_submission_success(self):
        from unittest.mock import patch
        from playwright.sync_api import TimeoutError
        import qianwen_browser as browser
        page=self.page();page.get_by_text.return_value.filter.return_value.first.wait_for.side_effect=TimeoutError('absent')
        meta={'qianwen_submission_attempted':True}
        with tempfile.TemporaryDirectory() as tmp,patch.object(browser.time,'monotonic',side_effect=[0,0,130]):
            with self.assertRaisesRegex(RuntimeError,'未出现本次上传记录'):
                browser.confirm_submission(page,'test-task',Path(tmp),meta,lambda *args:None)
        self.assertFalse(meta.get('qianwen_upload_confirmed',False))
        self.assertEqual(meta['state'],'cloud_confirming_upload')
        page.locator.assert_called()

    def test_cloud_storage_full_stops_without_claiming_upload(self):
        from playwright.sync_api import TimeoutError
        import qianwen_browser as browser
        page=self.page()
        page.get_by_text.return_value.filter.return_value.first.wait_for.side_effect=TimeoutError('absent')
        page.locator.return_value.inner_text.return_value='任务添加成功，请在「我的记录」查看进展\n存储已满\n请删除不用的记录后重试'
        meta={'qianwen_submission_attempted':True}
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(RuntimeError,'云端存储已满'):
                browser.confirm_submission(page,'test-task',Path(tmp),meta,lambda *args:None)
        self.assertFalse(meta['qianwen_upload_confirmed'])
        self.assertFalse(meta['qianwen_submission_attempted'])
        page.get_by_text.return_value.filter.return_value.first.wait_for.assert_called_once()

class CloudErrorTests(unittest.TestCase):
    def test_visible_cloud_error_is_preserved(self):
        from unittest.mock import MagicMock
        from qianwen_browser import require_cloud_available
        page=MagicMock();alert=MagicMock()
        alert.is_visible.return_value=True;alert.inner_text.return_value='上传失败，请稍后重试'
        page.get_by_role.return_value.all.return_value=[alert]
        with self.assertRaisesRegex(RuntimeError,'上传失败，请稍后重试'):
            require_cloud_available(page)

    def test_success_or_hidden_alert_does_not_fail_task(self):
        from unittest.mock import MagicMock
        from qianwen_browser import require_cloud_available
        page=MagicMock();success=MagicMock();hidden=MagicMock()
        success.is_visible.return_value=True;success.inner_text.return_value='任务添加成功'
        hidden.is_visible.return_value=False;hidden.inner_text.return_value='上传失败'
        page.get_by_role.return_value.all.return_value=[success,hidden]
        require_cloud_available(page)

class CloudDeleteSafetyTests(unittest.TestCase):
    def test_rejects_record_title_without_task_identifier(self):
        from unittest.mock import MagicMock
        import qianwen_browser as browser
        page=MagicMock()
        with self.assertRaisesRegex(RuntimeError,'归属'):
            browser.delete_cloud_record(page,Path('/tmp/123456abcdef'),{'qianwen_submitted':True,'qianwen_upload_title':'同名视频'},lambda *args:None)
        page.get_by_role.assert_not_called()

    def test_recent_records_counter_does_not_block_deletion(self):
        from unittest.mock import MagicMock,patch
        import qianwen_browser as browser
        page=UploadConfirmationTests().page();meta={'title':'测试','qianwen_submitted':True}
        # The actual header is “最近记录 + 4”; exact matching must not be used.
        def text_locator(text,exact=False):
            if text=='最近记录' and exact:raise AssertionError('header includes counter')
            return MagicMock()
        page.get_by_text.side_effect=text_locator
        with patch('playwright.sync_api.expect'):
            browser.delete_cloud_record(page,Path('/tmp/123456abcdef'),meta,lambda *args:None)
        self.assertTrue(meta['qianwen_cloud_deleted'])
        page.get_by_text.assert_any_call('最近记录',exact=False)

    def test_missing_cloud_record_allows_local_cleanup_without_claiming_deleted(self):
        from unittest.mock import patch
        import qianwen_browser as browser
        page=UploadConfirmationTests().page();meta={'title':'测试','qianwen_submitted':True}
        page.locator.return_value.filter.return_value.count.return_value=0
        with patch('playwright.sync_api.expect') as expect:
            expect.return_value.to_have_count.side_effect=AssertionError('record absent')
            browser.delete_cloud_record(page,Path('/tmp/123456abcdef'),meta,lambda *args:None)
        self.assertEqual(meta['qianwen_delete_result'],'not_found')
        self.assertTrue(meta['qianwen_delete_resolved'])
        self.assertFalse(meta.get('qianwen_cloud_deleted',False))
        page.locator.return_value.filter.return_value.locator.assert_not_called()

    def test_ambiguous_record_never_clicks_delete(self):
        from unittest.mock import MagicMock,patch
        import qianwen_browser as browser
        page=UploadConfirmationTests().page();meta={'title':'测试','qianwen_submitted':True}
        with patch('playwright.sync_api.expect') as expect:
            expect.return_value.to_have_count.side_effect=AssertionError('two records')
            with self.assertRaisesRegex(RuntimeError,'唯一定位'):
                browser.delete_cloud_record(page,Path('/tmp/123456abcdef'),meta,lambda *args:None)
        page.locator.return_value.filter.return_value.locator.assert_not_called()
        self.assertFalse(meta.get('qianwen_cloud_deleted',False))

if __name__=='__main__':unittest.main()
```

### FILE: test_reader.py
```text
import argparse
import hashlib
import json
import tempfile
import unittest
import wave
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from docx import Document
import reader


def reader_audio_duration(wav):
    with wave.open(str(wav)) as audio:
        return audio.getnframes() / audio.getframerate()


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.work = root / 'work'
        self.output = root / 'Downloads'
        (self.work / 'jobs').mkdir(parents=True)
        for name, value in [('WORK', self.work), ('OUTPUT', self.output)]:
            p = patch.object(reader, name, value)
            p.start()
            self.addCleanup(p.stop)
        self.addCleanup(self.temp.cleanup)
        self.trash = Path(self.temp.name) / 'trash'; self.trash.mkdir()
        p = patch('send2trash.send2trash', side_effect=lambda name: Path(name).rename(self.trash / Path(name).name))
        self.trash_mock = p.start(); self.addCleanup(p.stop)

    def fixture(self, seconds=1):
        url = 'https://example.com/video'
        job = self.work / 'jobs' / hashlib.sha256(url.encode()).hexdigest()[:12]
        job.mkdir(exist_ok=True)
        audio = job / 'transcription-audio.wav'
        with wave.open(str(audio), 'wb') as a:
            a.setnchannels(1); a.setsampwidth(2); a.setframerate(16000)
            a.writeframes(b'\0' * (seconds * 16000 * 2))
        meta = {'url': url, 'title': '测试标题', 'name': '测试标题', 'media': str(audio),
                'audio': str(audio), 'duration': seconds, 'state': 'downloaded'}
        reader.save_json(job / 'job.json', meta)
        return job, meta, audio

    def test_automatic_word_generation_and_cleanup(self):
        job, meta, audio = self.fixture()
        raw={'model':'qianwen-web','segments':[{'start':0,'end':1,'speaker':'发言人 1','text':'完整识别文字 80%。'}]}
        with patch('qianwen_browser.export_audio',return_value=raw), patch.object(reader,'ffmpeg',return_value='/unused'):
            reader.prepare(argparse.Namespace(url=meta['url'],cookies_browser=None,engine='qianwen'))
        saved = json.loads((job / 'job.json').read_text(encoding="utf-8"))
        self.assertEqual(saved['state'], 'completed')
        doc = Document(saved['document'])
        texts = [p.text for p in doc.paragraphs]
        self.assertEqual(texts[0], meta['url'])
        self.assertIn(reader.NOTICE, texts)
        self.assertIn('完整识别文字 80%。', texts)
        warning = next(p for p in doc.paragraphs if p.text == reader.NOTICE)
        self.assertTrue(warning.runs[0].bold)
        self.assertIsNotNone(warning.runs[0].font.highlight_color)
        self.assertNotIn('ChatGPT 总结', texts)
        self.assertEqual(Path(saved['document']).name, '1 - 测试标题.docx')
        self.assertFalse(audio.exists())
        self.assertTrue((self.trash / audio.name).exists())
        self.assertEqual(Path(saved['document']).parent, self.output)
        self.assertIn('[00:00:00–00:00:01] 发言人 1', texts)
        self.assertFalse(list(job.glob('checkpoints-*')))
        self.assertFalse((job / 'ChatGPT校对任务.txt').exists())
        self.assertTrue(saved['temporary_files_removed'])

    def test_local_upload_pipeline_preserves_user_original(self):
        import io, app, shutil
        original=Path(self.temp.name)/'我的录音.wav'
        with wave.open(str(original),'wb') as a:
            a.setnchannels(1);a.setsampwidth(2);a.setframerate(16000);a.writeframes(b'\0'*32000)
        with patch.object(app,'WORK',self.work),patch.object(app,'enqueue',side_effect=lambda url: __import__('hashlib').sha256(url.encode()).hexdigest()[:12]):
            ident=app.receive_upload(io.BytesIO(original.read_bytes()),original.stat().st_size,original.name)
        job=self.work/'jobs'/ident;meta=json.loads((job/'job.json').read_text(encoding="utf-8"))
        raw={'model':'qianwen-web','segments':[{'start':0,'end':1,'speaker':'发言人 1','text':'本地文件全部原文'}]}
        with patch('qianwen_browser.export_audio',return_value=raw),patch.object(reader,'ffmpeg',return_value='/unused'),patch.object(reader,'extract_audio',side_effect=lambda ff,src,dst:shutil.copy2(src,dst)):
            reader.prepare(argparse.Namespace(url=meta['url'],cookies_browser=None,engine='qianwen'))
        saved=json.loads((job/'job.json').read_text(encoding="utf-8"));texts=[p.text for p in Document(saved['document']).paragraphs]
        self.assertEqual(saved['state'],'completed')
        self.assertEqual(texts[0],'本地上传文件：我的录音.wav')
        self.assertEqual(Path(saved['document']).name,'1 - 我的录音.docx')
        self.assertIn('[00:00:00–00:00:01] 发言人 1',texts)
        self.assertTrue(original.exists());self.assertFalse(Path(meta['media']).exists())

    def test_speaker_changes_keep_separate_timestamps(self):
        job, meta, audio = self.fixture(4)
        raw = {'segments': [
            {'start': 0, 'end': 2, 'speaker': '发言人 1', 'text': '第一人发言'},
            {'start': 2, 'end': 4, 'speaker': '发言人 2', 'text': '第二人发言'}]}
        reader.save_json(job / 'raw-transcript.json', raw)
        path = reader.build_document(job, raw)
        texts = [p.text for p in Document(path).paragraphs]
        self.assertIn('[00:00:00–00:00:02] 发言人 1', texts)
        self.assertIn('[00:00:02–00:00:04] 发言人 2', texts)
        self.assertIn('第一人发言', texts)
        self.assertIn('第二人发言', texts)

    def test_empty_result_preserves_media(self):
        job, meta, audio = self.fixture()
        with self.assertRaises(ValueError):
            reader.build_document(job, {'segments': []})
        self.assertTrue(audio.exists())

    def test_modified_word_blocks_cleanup(self):
        job, meta, audio = self.fixture()
        raw = {'segments': [{'start': 0, 'end': 1, 'text': '原文'}]}
        reader.save_json(job / 'raw-transcript.json', raw)
        path = reader.build_document(job, raw)
        audio.write_bytes(b'retained')
        path.write_bytes(path.read_bytes() + b'changed')
        meta = json.loads((job / 'job.json').read_text(encoding="utf-8"))
        with self.assertRaises(ValueError):
            reader.clear_intermediate(job, meta)
        self.assertTrue(audio.exists())


if __name__ == '__main__':
    unittest.main()

class AudioExtractionTests(unittest.TestCase):
    def test_real_silent_video_gives_readable_error_and_preserves_source(self):
        import subprocess,imageio_ffmpeg
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);source=folder/'silent.mp4';target=folder/'temporary.wav'
            executable=imageio_ffmpeg.get_ffmpeg_exe()
            subprocess.run([executable,'-v','error','-f','lavfi','-i','color=size=16x16:rate=1','-t','1','-an',str(source)],check=True)
            with self.assertRaisesRegex(ValueError,'没有音轨'):
                reader.extract_audio(executable,source,target)
            self.assertTrue(source.exists());self.assertFalse(target.exists())

    def test_real_audio_extracts_readable_wave(self):
        import subprocess,imageio_ffmpeg
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);source=folder/'sound.wav';target=folder/'temporary.wav'
            executable=imageio_ffmpeg.get_ffmpeg_exe()
            subprocess.run([executable,'-v','error','-f','lavfi','-i','sine=frequency=440:duration=1',str(source)],check=True)
            reader.extract_audio(executable,source,target)
            with wave.open(str(target)) as audio:
                self.assertEqual(audio.getframerate(),16000)
                self.assertEqual(audio.getnchannels(),1)
                self.assertGreater(audio.getnframes(),0)

class DownloadLinkTests(unittest.TestCase):
    def test_douyin_selected_video_is_normalized(self):
        source='https://www.douyin.com/jingxuan?modal_id=7689068026368380196'
        self.assertEqual(reader.download_url(source),'https://www.douyin.com/video/7689068026368380196')
    def test_other_site_modal_parameter_is_untouched(self):
        source='https://example.com/jingxuan?modal_id=123'
        self.assertEqual(reader.download_url(source),source)
    def test_invalid_douyin_id_is_untouched(self):
        source='https://www.douyin.com/jingxuan?modal_id=invalid'
        self.assertEqual(reader.download_url(source),source)
```

### FILE: test_runtime_compat.py
```text
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import install
import reader
import runtime_compat


class CompatibilityTests(unittest.TestCase):
    def test_venv_layout(self):
        with patch.object(runtime_compat, 'IS_WINDOWS', True):
            self.assertTrue(runtime_compat.venv_python('/tmp').parts[-2:] == ('Scripts','python.exe'))
        with patch.object(runtime_compat, 'IS_WINDOWS', False):
            self.assertTrue(runtime_compat.venv_python('/tmp').parts[-2:] == ('bin','python'))

    def test_lock_excludes_another_process(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'lock'
            with path.open('a') as handle:
                runtime_compat.file_lock.flock(handle, runtime_compat.file_lock.LOCK_EX | runtime_compat.file_lock.LOCK_NB)
                code = "from runtime_compat import file_lock as f; import sys\nh=open(sys.argv[1],'a')\ntry: f.flock(h,f.LOCK_EX|f.LOCK_NB)\nexcept BlockingIOError: sys.exit(0)\nsys.exit(1)"
                result=subprocess.run([sys.executable,'-c',code,str(path)],capture_output=True,text=True)
                self.assertEqual(result.returncode,0,result.stderr)

    def test_windows_environment(self):
        with patch.object(install.platform,'system',return_value='Windows'), patch.object(install.platform,'machine',return_value='AMD64'), patch.object(install.sys,'version_info',(3,12)), patch.object(install.sys,'getwindowsversion',create=True,return_value=MagicMock(build=22631,product_type=1)), patch.object(install.shutil,'which',return_value='node.exe'), patch.object(install.subprocess,'check_output',return_value=json.dumps({'version':'24.0.0','arch':'x64'})):
            install.check_environment()

    def test_windows_service_redirector_identity(self):
        fake = MagicMock()
        process = fake.Process.return_value
        process.parents.return_value = [MagicMock(pid=123)]
        process.cmdline.return_value = ['python.exe', str(install.ROOT/'app.py')]
        process.cwd.return_value = str(install.ROOT)
        with patch.object(install.platform,'system',return_value='Windows'), patch.dict(sys.modules, {'psutil':fake}):
            self.assertTrue(install.started_service_matches(456,123))
            process.cmdline.return_value = ['python.exe', str(install.ROOT/'other.py')]
            self.assertFalse(install.started_service_matches(456,123))
            process.cmdline.return_value = ['python.exe', str(install.ROOT/'app.py')]
            process.parents.return_value = [MagicMock(pid=999)]
            self.assertFalse(install.started_service_matches(456,123))

    def test_windows_10_rejected_before_dependency_install(self):
        with patch.object(install.platform,'system',return_value='Windows'), patch.object(install.platform,'machine',return_value='AMD64'), patch.object(install.sys,'getwindowsversion',create=True,return_value=MagicMock(build=19045,product_type=1)), patch.object(install,'run') as run:
            with self.assertRaisesRegex(RuntimeError,'Windows 11'):
                install.check_environment()
            run.assert_not_called()

    def test_windows_arm_rejected(self):
        with patch.object(install.platform,'system',return_value='Windows'), patch.object(install.platform,'machine',return_value='ARM64'):
            with self.assertRaises(RuntimeError):install.check_environment()

    def test_reserved_filename(self):
        for name in ['CON','nul.txt','COM1','LPT9.docx']:
            self.assertTrue(reader.filename(name).startswith('_'))
        self.assertEqual(reader.filename('普通标题'),'普通标题')

    def test_windows_ffmpeg_uses_copy_not_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); source=root/'original.exe';source.write_bytes(b'ffmpeg')
            with patch.object(reader,'WORK',root), patch.object(reader,'IS_WINDOWS',True), patch('imageio_ffmpeg.get_ffmpeg_exe',return_value=str(source)):
                target=Path(reader.ffmpeg())
                self.assertEqual(target.name,'ffmpeg.exe')
                self.assertFalse(target.is_symlink())
                self.assertEqual(target.read_bytes(),b'ffmpeg')

if __name__ == '__main__':unittest.main()
```

### FILE: test_runtime_status.py
```text
import unittest,tempfile,json
from pathlib import Path
from unittest.mock import patch
class StatusTests(unittest.TestCase):
 def test_readonly_status_does_not_mutate_job(self):
  from runtime_status import snapshot
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);job=root/'work/jobs/123456abcdef';job.mkdir(parents=True)
   record=job/'job.json';record.write_text('{"state":"failed"}');before=record.read_bytes()
   with patch('browser_service.endpoint',return_value='ws://localhost/test'):
    data=snapshot(root,[{'id':job.name,'state':'failed','title':'任务','error':'失败'}],{'status':'unknown'})
   self.assertEqual(record.read_bytes(),before);self.assertEqual(data['tasks'][0]['error'],'失败');self.assertIn('已连接',data['browser']);self.assertEqual(data['pages'],[])
```

### FILE: test_task_controls.py
```text
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from docx import Document
import task_controls
import qianwen_browser


class TaskControlTests(unittest.TestCase):
    def setup_files(self, root):
        folder=root/'work/jobs/123456abcdef';folder.mkdir(parents=True)
        output=root/'output';output.mkdir()
        path=output/'测试.docx';doc=Document();doc.add_paragraph('https://example.com/test');doc.add_paragraph('正文');doc.save(path)
        meta={'name':'测试','url':'https://example.com/test','document':str(path)}
        (folder/'job.json').write_text(json.dumps(meta), encoding="utf-8")
        (folder/'media').mkdir();(folder/'media/video.mp4').write_bytes(b'test')
        return folder,output,path

    def run_delete(self, root, output):
        trash=root/'trash';trash.mkdir()
        def move(path):shutil.move(path,trash/Path(path).name)
        with patch('send2trash.send2trash',side_effect=move),patch('task_controls.reader_pids',return_value=[]):
            task_controls.trash_task(root,root/'work',[output],'123456abcdef')
        return trash

    def test_removes_task_media_document_and_reserved_partial(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);folder,output,path=self.setup_files(root)
            partial=path.with_suffix('.partial.docx');partial.write_bytes(b'incomplete zip')
            (folder/'export-target.json').write_text(json.dumps({'url':'https://example.com/test','path':str(path)}), encoding="utf-8")
            trash=self.run_delete(root,output)
            self.assertFalse(folder.exists());self.assertFalse(path.exists());self.assertFalse(partial.exists())
            self.assertTrue((trash/'123456abcdef/media/video.mp4').exists())
            self.assertTrue((trash/'测试.docx').exists());self.assertTrue((trash/'测试.partial.docx').exists())

    def test_preserves_unrelated_document_with_same_title(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);folder,output,path=self.setup_files(root)
            meta=json.loads((folder/'job.json').read_text(encoding="utf-8"));meta.pop('document');(folder/'job.json').write_text(json.dumps(meta), encoding="utf-8")
            doc=Document();doc.add_paragraph('https://other.example/video');doc.save(path)
            self.run_delete(root,output);self.assertTrue(path.exists())

    def test_rejects_document_outside_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);folder,output,path=self.setup_files(root)
            outside=root/'private.docx';shutil.copy2(path,outside)
            meta=json.loads((folder/'job.json').read_text(encoding="utf-8"));meta['document']=str(outside);(folder/'job.json').write_text(json.dumps(meta), encoding="utf-8")
            with patch('task_controls.reader_pids',return_value=[]),patch('send2trash.send2trash'),self.assertRaises(ValueError):
                task_controls.trash_task(root,root/'work',[output],'123456abcdef')
            self.assertTrue(outside.exists());self.assertTrue(folder.exists())

    def test_invalid_identifier_cannot_escape_job_folder(self):
        with self.assertRaises(ValueError):task_controls.trash_task(Path('/tmp'),Path('/tmp'),[], '../escape')

    def test_login_prompt_becomes_explicit_login_required(self):
        from unittest.mock import MagicMock
        page=MagicMock();prompt=MagicMock();prompt.is_visible.return_value=True
        page.get_by_role.return_value.filter.return_value.all.return_value=[prompt]
        with patch('qianwen_browser.auth_state') as state,self.assertRaises(qianwen_browser.LoginRequired):
            qianwen_browser.require_login_if_visible(page)
        state.assert_called_once_with('required')

    def test_login_buttons_use_exact_names(self):
        from unittest.mock import MagicMock
        page=MagicMock()
        page.get_by_role.return_value.filter.return_value.all.return_value=[]
        page.get_by_role.return_value.all.return_value=[]
        qianwen_browser.require_login_if_visible(page)
        for name in ('登录','登录/注册','立即登录'):
            page.get_by_role.assert_any_call('button',name=name,exact=True)

if __name__=='__main__':unittest.main()
```

### FILE: test_task_numbering.py
```text
import unittest,tempfile,json,shutil
from pathlib import Path
from task_numbering import numbers,migrate_documents
class NumberTests(unittest.TestCase):
 def test_delete_leaves_gap_and_retry_keeps_number(self):
  with tempfile.TemporaryDirectory() as tmp:
   work=Path(tmp)
   for ident,t in [('first',1),('second',2)]:
    job=work/'jobs'/ident;job.mkdir(parents=True);(job/'job.json').write_text(json.dumps({'created_at':t}))
   self.assertEqual(numbers(work),{'first':1,'second':2})
   shutil.rmtree(work/'jobs/first');job=work/'jobs/third';job.mkdir();(job/'job.json').write_text('{"created_at":3}')
   self.assertEqual(numbers(work)['third'],3);self.assertEqual(numbers(work)['second'],2)
 def test_document_rename_updates_owned_paths(self):
  with tempfile.TemporaryDirectory() as tmp:
   work=Path(tmp)/'work';job=work/'jobs/one';job.mkdir(parents=True);output=Path(tmp)/'output';output.mkdir();old=output/'title.docx';old.write_bytes(b'example')
   meta={'created_at':1,'state':'completed','name':'title','url':'source','document':str(old)};(job/'job.json').write_text(json.dumps(meta))
   from unittest.mock import patch
   with patch('reader.configure_folder_sort'):migrate_documents(work,output)
   self.assertEqual((output/'1 - title.docx').read_bytes(),b'example');self.assertFalse(old.exists());self.assertEqual(json.loads((job/'job.json').read_text())['document'],str(output/'1 - title.docx'))
```

### FILE: tools/build_guides.py
```text
"""Rebuild public self-contained guides from tracked source; never read work/."""
import hashlib
import json
import subprocess
from pathlib import Path
from docx import Document

ROOT = Path(__file__).resolve().parents[1]
files = sorted(subprocess.check_output(['git','ls-files','-z'], cwd=ROOT).decode().split('\0')[:-1])
files = sorted(set(files + ['install.sh', 'test_install.py', 'tools/build_guides.py', 'runtime_compat.py', 'test_runtime_compat.py', 'install-windows.ps1', 'install-windows.cmd', 'start-windows.cmd', 'deletion_queue.py', 'test_deletion_queue.py', 'browser_service.py', 'test_browser_service.py', 'runtime_status.py', 'test_runtime_status.py', 'bilibili_download.py', 'test_bilibili_download.py', 'test_export_download.py', 'task_numbering.py', 'test_task_numbering.py', '修复浏览器占用并加载更新.command']))
files = [f for f in files if f.endswith(('.py','.sh','.command','.html','.ps1','.cmd')) or f in ('requirements.txt','.gitignore')]
checks = {f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}
(ROOT/'文件校验.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n', encoding="utf-8")
text = (ROOT/'README.md').read_text(encoding="utf-8") + '\n## 仅收到本文档：完整源码\n\nAI Agent 可按 FILE 标记逐个提取文件，再核对文件校验.json；运行 `bash install.sh`。仅提取这里列出的公开源码，不迁移他人的登录资料。\n\n'
for f in files + ['文件校验.json']:
    text += f'### FILE: {f}\n```text\n' + (ROOT/f).read_text(encoding="utf-8").rstrip() + '\n```\n\n'
(ROOT/'INSTALL_GUIDE.md').write_text(text, encoding="utf-8")
doc = Document()
in_code = False
for line in text.splitlines():
    if line == '```text':
        in_code = True
        doc.add_paragraph(line)
    elif line == '```' and in_code:
        in_code = False
        doc.add_paragraph(line)
    elif not in_code and line.startswith('# '): doc.add_heading(line[2:],level=0)
    elif not in_code and line.startswith('## '): doc.add_heading(line[3:],level=1)
    elif not in_code and line.startswith('### '): doc.add_heading(line[4:],level=2)
    else: doc.add_paragraph(line)
doc.save(ROOT/'安装与使用指南.docx')
print(f'Rebuilt guides with {len(files)} public source files.')
```

### FILE: 修复浏览器占用并加载更新.command
```text
#!/bin/zsh
cd -- "${0:A:h}" || exit 1
.venv/bin/python - <<'PY'
import json,subprocess,time,os,plistlib
from pathlib import Path
from task_controls import reader_pids,stop_reader
from reader import save_json
from launch_service import LABEL
from browser_service import endpoint
root=Path.cwd();work=root/'work'
plist=Path.home()/'Library/LaunchAgents'/(LABEL+'.plist')
if not plist.exists() or plistlib.loads(plist.read_bytes()).get('WorkingDirectory')!=str(root):raise SystemExit('未找到属于当前项目的自动启动服务，未执行切换。')
if not endpoint():
    owners=set(subprocess.run(['lsof','-t',str(work/'qianwen-browser.lock')],capture_output=True,text=True).stdout.split())
    for record in (work/'jobs').glob('*/job.json'):
        verified=reader_pids(root,record.parent)
        if not owners.intersection(str(pid) for pid in verified):continue
        for pid in verified:stop_reader(pid)
        from runtime_compat import file_lock as f
        with (record.parent/'.prepare.lock').open('a') as lock:
            deadline=time.monotonic()+20
            while True:
                try:f.flock(lock,f.LOCK_EX|f.LOCK_NB);break
                except BlockingIOError:
                    if time.monotonic()>deadline:raise SystemExit('旧进程仍未退出，文件和任务已保留。')
                    time.sleep(.25)
            meta=json.loads(record.read_text());meta.update(state='queued');meta.pop('error',None);save_json(record,meta)
            print('已保留媒体和千问提交记录，切换任务：'+meta.get('title',record.parent.name))
for record in (work/'jobs').glob('*/job.json'):
    meta=json.loads(record.read_text())
    if meta.get('state')=='failed' and '千问浏览器正在使用中' in meta.get('error',''):
        meta.update(state='queued');meta.pop('error',None);save_json(record,meta)
subprocess.run(['/bin/launchctl','kill','SIGTERM',f'gui/{os.getuid()}/{LABEL}'],check=True)
print('切换完成。请刷新工具页面，并点击“显示任务状态”查看后台进展。')
PY
result=$?
read '?按回车关闭窗口。'
exit "$result"
```

### FILE: 停用自动启动.command
```text
#!/bin/zsh
cd "${0:A:h}" || exit 1
.venv/bin/python launch_service.py uninstall --port 8767
result=$?
read 'reply?按回车关闭窗口。'
exit $result
```

### FILE: 切换千问并清理本地模型.command
```text
#!/bin/zsh
cd -- "${0:A:h}" || exit 1
uid_value=$(id -u)
service="gui/$uid_value/com.zhangjp.web-video-to-word"
plist="$HOME/Library/LaunchAgents/com.zhangjp.web-video-to-word.plist"
# Temporarily unload to prevent an old worker restarting during migration.
/bin/launchctl bootout "$service" 2>/dev/null || true
.venv/bin/python cloud_migration.py
result=$?
/bin/launchctl bootstrap "gui/$uid_value" "$plist" 2>/dev/null || /bin/launchctl kickstart "$service"
if (( result != 0 )); then
 print '迁移未完成，请把以上错误发给 Codex。'
else
 print '已完成千问专用版切换。刷新工具页面即可。'
fi
read '?按回车关闭窗口。'
```

### FILE: 加载本次更新.command
```text
#!/bin/zsh
cd -- "${0:A:h}" || exit 1
.venv/bin/python - <<'PY'
import os, plistlib, subprocess
from pathlib import Path
from launch_service import LABEL
root=Path.cwd()
path=Path.home()/'Library/LaunchAgents'/(LABEL+'.plist')
if not path.exists():
    raise SystemExit('尚未启用自动启动。请先关闭手动网页服务，再运行启动工具.command。')
config=plistlib.loads(path.read_bytes())
if config.get('WorkingDirectory')!=str(root):
    raise SystemExit('自动启动项属于另一个项目副本，未停止服务。')
subprocess.run(['/bin/launchctl','kill','SIGTERM',f'gui/{os.getuid()}/{LABEL}'],check=True)
print('网页服务正在自动恢复。请稍后刷新工具页面。正在识别的任务会保留。')
PY
result=$?
read '?按回车关闭窗口。'
exit "$result"
```

### FILE: 启动工具.command
```text
#!/bin/zsh
cd "${0:A:h}" || exit 1
/bin/bash install.sh --start-only --open
result=$?
if (( result != 0 )); then read 'reply?请按上方提示处理；按回车关闭窗口。'; fi
exit $result
```

### FILE: 启用自动启动.command
```text
#!/bin/zsh
cd "${0:A:h}" || exit 1
.venv/bin/python launch_service.py install --port 8767
result=$?
read 'reply?按回车关闭窗口。'
exit $result
```

### FILE: 测试千问后台流程.command
```text
#!/bin/zsh
cd -- "${0:A:h}" || exit 1
export SSL_CERT_FILE=/etc/ssl/cert.pem
export NODE_EXTRA_CA_CERTS=/etc/ssl/cert.pem
.venv/bin/python smoke_qianwen_runner.py
result=$?
read '?测试结束，按回车关闭窗口。'
exit "$result"
```

### FILE: 自动恢复测试.command
```text
#!/bin/zsh
cd "${0:A:h}" || exit 1
.venv/bin/python check_recovery.py --port 8767
result=$?
read 'reply?按回车关闭窗口。'
exit $result
```

### FILE: 配置千问登录.command
```text
#!/bin/zsh
cd -- "${0:A:h}" || exit 1
export SSL_CERT_FILE=/etc/ssl/cert.pem
export PIP_CERT=/etc/ssl/cert.pem
export NODE_EXTRA_CA_CERTS=/etc/ssl/cert.pem
export PLAYWRIGHT_BROWSERS_PATH="$PWD/work/browser-bin"
.venv/bin/python -m pip install playwright || exit 1
.venv/bin/python -m playwright install chromium || exit 1
.venv/bin/python qianwen_browser.py login || exit 1
/bin/launchctl kill SIGTERM "gui/$(id -u)/com.zhangjp.web-video-to-word" 2>/dev/null || true
echo "登录配置完成。如已启用自动启动，服务将自动加载新版。"
read '?按回车关闭窗口。'
```

### FILE: 首次安装.command
```text
#!/bin/zsh
cd "${0:A:h}" || exit 1
/bin/bash install.sh --open
result=$?
if (( result != 0 )); then print '安装未完成，请按上方“下一步”操作后重试。'; fi
read 'reply?按回车关闭窗口。'
exit $result
```

### FILE: 文件校验.json
```text
{
  ".gitignore": "3e1cfc92af2c00c9dede00b674647a334c4cd068d8d8d743780802025013e291",
  "app.py": "de5aa99204ed5c0c0091be3a045c157968d9fa3758ba8833ee7543b23721221c",
  "bilibili_download.py": "286ed2197bb0763f3f060aea40075d0cb4a46c1252ef19a0343358e00dd40f5d",
  "browser_service.py": "4bb4e16ac5b1f0ba53a46e3df01a55b5072f4d1dcbd3c48e745aaf55d8e5136a",
  "check_recovery.py": "7fb929eabc113b13551764fe57caa4f72e7f37f6cded04a75c590fe54e1a3d2d",
  "cloud_migration.py": "cc5c02b953f404a280f0230e836ff9a5fe04f3e7002361ef9b8b8cdc244c07a0",
  "deletion_queue.py": "f9fef20b033ab62baa5fd40b4e1ce383d4bed3c8dde54f80a468417c03dc3cad",
  "index.html": "9d3e810574065f1a50bfb22b197c253cc83bdb81686a0327b8b5e4bcce569741",
  "install-windows.cmd": "181344afef4643cc95c8098d5839cdf8df98963e8d05a13991deb41c8a38c2ed",
  "install-windows.ps1": "727a49a50e928b435c2863aff20dd8b20be4b0c5662d971c71ac8a4554dbaedd",
  "install.py": "8fb062e855fb41616c65923dc4ca43808d4c710fc8919d1cb62c039a1fb2144c",
  "install.sh": "abead2c9d17bc14579905cab745be4220776c7d954a96042028c7b4855164826",
  "launch_service.py": "2cadb70ee153b678af24a6eb9e911d7e6e2ae4906ca8d3115ff8bb723d516dba",
  "qianwen_browser.py": "7988161230d63faf0a86da6a6b5a2bc10c49a91edb92d7095873bb8a3c3b9cdd",
  "reader.py": "c5ca5add9980f167b3566ae4fc1f536f4cd6055da666990fe418640572027566",
  "requirements.txt": "ca2ed115c7d5ef1c7d63e54519aa39795e35d48d74ac5e8b7be278ccc8e7f083",
  "runtime_compat.py": "88356cfde1ee32b4a9100f48ee374ed7e5ac0ba558f6a8626dde430c10b1191f",
  "runtime_status.py": "53e0df100829fd59b385b1fbdddb8bb0da17ff0a5ba88d91c2fb4b29ba2d5c3a",
  "smoke_qianwen.py": "5a41ae58b74a8f2edaaadeb36c60235646989c5bdb2aa49e17d72dfd8778f71e",
  "smoke_qianwen_runner.py": "10c6047ad2b7ae20cac3945b41f8afdc047975fd2da3ef0dc576f3753a512409",
  "start-windows.cmd": "c7337ce90691fcda24e0bf19b584ff342288322681552433921f92ef399ed9b8",
  "task_controls.py": "e452af89723c6a0506012cb48a931bb7286132925ed33d56db0069ef6e29fba4",
  "task_numbering.py": "fb2249ca9dc6d7c8fb7ac28cf9e23e15d6796f544e8dc2faed6d67ca8dcbb34e",
  "test_app.py": "c7ffaebeb5c1ea329f86b5e1047860f080b1a7b46604250782d0cad6fc96d233",
  "test_bilibili_download.py": "7d880288610b8e78afb0927f074275b737b143b5b81750c4caf51d99ebe7dae1",
  "test_browser_service.py": "fa30cf65671ef804c0fee82b0cecced1a3748bbc9f2209cde584ceb8aa49a2c3",
  "test_deletion_queue.py": "172f0a40974d00804f6d7e0d0fbcdf72acc7178c1d301c7cfec678d88985db71",
  "test_export_download.py": "d7d2c3fd4ac63f3fc513a74ef9a296a707066cb2912c5a97443071dfb2255b01",
  "test_install.py": "5ecdd4f27fc1761c89a27fd5d623377f05315a318cbb622bbd615686798b4941",
  "test_qianwen.py": "9fb2902cabfbb02f36b5ce3bed5c96205ba05b6b390833cae97e10ecafd78473",
  "test_reader.py": "0320926db03be6d0726c88092cdd5cb7d88b3cc7fcfb9d341bc3e0cf740a6b02",
  "test_runtime_compat.py": "e7e4d7ddc223a5586ab803f7969a4a6eb69861f64d1257b48f02ade15a939188",
  "test_runtime_status.py": "4b255845c0a0fdb89f76f0fbd04d43d0162c35428ebef9ff3724470abbe6baca",
  "test_task_controls.py": "4c7ef80bd87e091c6140d660cacd406f932048ba89809b4a9236e1b327d3b9b5",
  "test_task_numbering.py": "0c1223029045edc6ff1210b2376505722b4e30f62ba4ab33c7d340042925afc8",
  "tools/build_guides.py": "a39ba11ad1b2496aee4ef424db8acfadaf8af35c687abd45adebfb7f1ff3329c",
  "修复浏览器占用并加载更新.command": "518dadc5853e369bd88d24645d55c42ef7af42595edd8f88defe62c3bb5a32d6",
  "停用自动启动.command": "0c2353cd41fd56b737864d09d6fe83f8b7d62cc1c51757e86fe0bc6bbd76b682",
  "切换千问并清理本地模型.command": "39ae5c718d5854f9fec85e13cd2c6fc683cb3c07844dffdd29697f97cfeeaaf4",
  "加载本次更新.command": "ceabb97ebf2b3d7df5568844de02733bc9e09f9c877621985bdaf801a182b978",
  "启动工具.command": "d04ece1eecd95cc76065918bac7b07bc9d6cd9988e853fc93a15bb185602e218",
  "启用自动启动.command": "3475ec88b5c035f49adc0a13b3a14a09255ca19aa600a750051f6a8f1d8a07b6",
  "测试千问后台流程.command": "365ea7c455b38238341c79e3f2db6531de8053c34a909c4a210a19248a680c8c",
  "自动恢复测试.command": "e5f7e855d99cd648d6ae2e1382da651e8afb7597f184e08d1661d6daef5cc7f6",
  "配置千问登录.command": "3bc9b14516ab4c169b0cd7a9c595778965167f7f7ce533eab5ad7b3abd835fac",
  "首次安装.command": "79eb3d678dd13a8115cfba58933713a6557929264a79b7e5143ee65c35987fb0"
}
```

