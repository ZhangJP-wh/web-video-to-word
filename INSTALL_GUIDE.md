# 网页视频转语音文稿：安装、使用与验收指南

版本：2026-10-07。适用对象：电脑初学者，以及具备本地文件、终端和网络权限的 AI Agent。

这是一份可独立交给 Agent 的指南：附录包含本分享版的完整源码和校验值。本项目的 GitHub 地址为 https://github.com/ZhangJP-wh/web-video-to-word- 。可点击 Code → Download ZIP 下载源码。拿到配套源码 ZIP 时可以直接解压；只有本文时，Agent 可以按第 11 节提取附录源码。普通读者只需读第 1～8 节，代码附录不必逐行阅读。

## 1. 这个工具做什么

操作流程：粘贴音视频网页链接 → 后台下载 → 本地声纹区分 → Qwen3-ASR-1.7B 语音识别 → 自动生成 Word → 验证写入完整 → 下载的原音视频移入废纸篓。

Word 第一行是原网页链接，随后是视频标题、醒目提示、带音频时间范围和发言人编号的识别文字。所有 Word 直接放在自己的“下载/网页视频转语音文稿”文件夹里，不创建任务二级文件夹。同标题的不同视频可能追加任务编号，避免覆盖。任务页面按添加任务的时间倒序，最新在最上方；Finder 可按文档添加日期倒序排列。

提示原文：本文稿内容为语音模型识别结果，需要注意：可能有错别字和识别不准确之处。

识别全文不会交给 ChatGPT 校对，也不生成总结。不需要 ChatGPT、Codex 账号或付费 API。安装时下载软件和模型；使用时视频网站仍需联网。本地模型推理不把音轨上传到云端识别服务。

时间戳对应音频片段的起止范围，不是逐字对齐。发言人 1、2 等是声纹估计编号，不是真实姓名；短句、重叠讲话、口音、噪声、相似声音可能导致分错或识别错误。Word 完整性检查只证明程序把识别结果写入了文档，不证明听写准确。

## 2. 先确认电脑能否安装

本分享版范围：Apple 芯片 Mac，原生 arm64 Python 3.12，CPU 单任务运行。原工具在 Apple M2、8GB 内存、macOS 27.0.1、Python 3.12.8 的环境中验证过；分享版的便携安装脚本还没有在另一台全新 Mac 上完成全流程验收。不要把它描述为已覆盖所有 Mac 或 Windows。

查看方法：点左上角苹果图标 → 关于本机。如果“芯片”显示 Apple M1、M2、M3 等，属于本指南的目标类型。如果写 Intel，或是 Windows/Linux，先让 Agent 适配，不要照搬 .command、Finder、废纸篓相关步骤。

资源准备：8GB 的原电脑可运行，但处理可能很慢；16GB 或以上通常更宽裕，这不是性能保证。建议安装前至少预留 15GB 空间；长视频还要额外预留视频和解压 WAV 的空间。Qwen 权重在原环境约 4.4GB，Python 运行依赖约 1.7GB，这只是实测参考。废纸篓里的视频仍占磁盘，移入废纸篓并不等于释放空间。

工具后台不会控制鼠标、切换桌面或占用屏幕操作，但会占用 CPU、内存和磁盘。电脑休眠、关闭盖子或断网会影响运行；长任务请接电源、让电脑保持唤醒，必要时由本人设置系统的睡眠选项。

## 3. 下载入口与组件说明

以下均为官方或项目上游链接，核对日期为 2026-10-07；将来下载页面和版本要求可能改变。

| 项目 | 下载或说明链接 | 用途及备注 |
| --- | --- | --- |
| Python macOS 下载 | https://www.python.org/downloads/macos/ | 运行本工具的 Python 环境。本指南选 3.12 系列，避免直接用最新 3.14 替代。 |
| Python 3.12.10 发布页 | https://www.python.org/downloads/release/python-31210/ | 兼容性安装路径，页面 Files 中选 macOS 64-bit universal2 installer。3.12.10 不是截至本文日期的最新 Python 安全补丁；长期部署请让 Agent 评估更新的 3.12 补丁版本及其官方安装方式。 |
| Python 3.12.10 macOS 安装包 | https://www.python.org/ftp/python/3.12.10/python-3.12.10-macos11.pkg | 官方 .pkg 链接，适用于本指南的手动兼容性安装路线。 |
| Node.js 下载 | https://nodejs.org/en/download | 选 macOS 的 LTS 安装包；Apple 芯片选 ARM64（若页面需要选择架构）。本分享版要求主版本至少 22。 |
| yt-dlp | https://github.com/yt-dlp/yt-dlp | 网页音视频下载组件，通过 pip 自动安装。 |
| yt-dlp 的 JavaScript 运行时说明 | https://github.com/yt-dlp/yt-dlp/wiki/EJS | YouTube 完整支持需要相应 JavaScript 运行时和 EJS；上游当前列 Node 最低 22。源码会自动寻找 PATH 中的 Node。 |
| Qwen3-ASR 官方项目 | https://github.com/QwenLM/Qwen3-ASR | 语音识别引擎，使用 transformers 后端；不用 CUDA/vLLM。 |
| Qwen3-ASR-1.7B 模型 | https://huggingface.co/Qwen/Qwen3-ASR-1.7B | 首次安装自动下载，之后缓存于项目 work/model-cache；模型页面标示 Apache-2.0。 |
| 声纹区分组件 | https://github.com/resemble-ai/Resemblyzer | 免费本地声纹特征模型，通过 pip 安装，权重随该组件提供。 |
| FFmpeg Python 包 | https://pypi.org/project/imageio-ffmpeg/ | 自动取得此包提供的 FFmpeg 可执行文件；无需为本版另装 Homebrew FFmpeg。 |
| Python 软件包索引 | https://pypi.org/ | 安装依赖时连接；不需要手动一个个下载 .whl。 |

软件本身没有按分钟收费。网络、电脑电力、存储或视频网站会员不属于本工具提供的免费资源。不要把下载失败视为应当绕过网站访问限制。

## 4. 小白安装路线：一步一步做

### 4.1 获取工具文件

优先使用分享者发来的“网页视频转语音文稿-源码包.zip”。下载后双击解压，得到 source 文件夹。把这个文件夹改名为 VideoTranscript，移到自己的个人目录中，最终位置建议为 ~/VideoTranscript。

Finder 中打开个人目录的方法：菜单“前往”→“个人”。~/ 是你自己的个人目录，不要输入分享者的用户名。不要把程序长期放在 ZIP 内运行，也不要在首次安装后搬动已建立 .venv 的整个文件夹。

如果只收到 Word 或 Markdown 指南：把文档交给有本地文件权限的 Agent，明确说“按第 11 节提取完整源码，并按本指南安装和验收”；不要让普通聊天机器人假装操作你的电脑。没有本地执行权限的聊天 AI 只能提供指导。

文件夹至少应有 reader.py、app.py、index.html、requirements.txt、install.py、prefetch_model.py、首次安装.command、启动工具.command、test_reader.py、test_app.py，以及 文件校验.json。

### 4.2 安装 Python

打开第 3 节的 Python 下载入口，找到 Python 3.12 系列的 macOS 安装包；本文提供的明确 .pkg 是 3.12.10。不要下载源码 tar 包，也不要选择 Windows 安装器。双击 .pkg，按安装器完成操作；管理员密码由电脑本人输入。若本人或 Agent 选择较新 3.12 安全补丁路线，记录实际版本并重新验收。

打开 Finder 的“应用程序”文件夹，找到 Python 3.12 文件夹。如有 Install Certificates.command，双击运行一次，用来配置该 Python 的 HTTPS 证书。安装结束后重新打开终端窗口，避免沿用旧 PATH。

### 4.3 安装 Node.js

打开 https://nodejs.org/en/download，选 macOS LTS 安装包，Apple 芯片选 ARM64（如需选择），主版本至少 22。双击安装包并按页面完成操作。你不需要理解 JavaScript；这个组件帮助 yt-dlp 处理 YouTube 的下载挑战。

### 4.4 检查环境

按 Command+空格，输入“终端”并回车。把下面三行分别复制进去，每行按回车。代码框里的内容不包括提示符，不要手工修改版本号。

```sh
python3.12 --version
python3.12 -c "import platform; print(platform.machine())"
node --version
```

成功标志：Python 显示 3.12.x，架构显示 arm64，Node 显示 v22 或更高。如果显示 command not found，请转到第 8 节排查，不要先开始模型下载。

### 4.5 首次安装

在 VideoTranscript 文件夹双击“首次安装.command”。它会自动建立本工具专用的 .venv，安装组件、检查依赖、运行测试、下载 Qwen 模型，并检查声纹与 FFmpeg。

第一次运行可能被系统要求确认打开、申请文件访问或安装器权限。先核对来源是朋友给你的清洁源码；遇到安全或权限提示，由电脑本人按系统允许的方式处理。不要为了省事关闭 Gatekeeper、修改全局安全设置或运行全盘删除隔离标记的命令。

若系统提示没有执行权限，可在终端运行以下命令（前提是确实按 4.1 放在这个位置）：

```sh
cd "$HOME/VideoTranscript"
chmod u+x 首次安装.command 启动工具.command
./首次安装.command
```

安装过程中窗口会显示下载文字。不要关闭窗口，也不要以短时间没有新文字判断卡死。模型约 4.4GB，速度取决于网络。看到“安装完成。请双击：启动工具.command。”，才表示安装脚本通过；只有网页能打开还不算模型已装好。

下载中断后可再次运行首次安装，已存在的组件和模型缓存通常能复用。不要删除正在下载的缓存文件。

## 5. 日常使用

1. 双击“启动工具.command”。按提示打开 http://127.0.0.1:8767/。
2. 127.0.0.1 代表自己的电脑。朋友打开同样地址，使用的是朋友自己的工具，不会连接分享者的 Mac。
3. 在视频网站复制具体音视频播放页面的链接，贴进输入框，点“开始生成文稿”。B 站多分 P、合集或播放列表请尽量选具体的一集。
4. 页面出现排队、下载、区分发言人、语音识别等状态。可切到其他应用做自己的事；浏览器标签页可以关闭，电脑和后台服务仍须运行。
5. 最新添加任务在最上方，完成时仍按任务添加顺序排列，不按文档完成时间重新排队。
6. 出现“Word 已生成，可以查看”后，点“查看 Word 文稿”在页面阅读，或点“打开文档所在位置”在 Finder 中找到文件。
7. Word 第一行有原链接，正文有提示和时间戳。多人对话还应有不同发言人编号，但编号可能分错。
8. 默认 Word 已在自己的“下载/网页视频转语音文稿”内；“下载 Word”按钮用于另存副本，可能由浏览器再次生成重名副本，不是必须点击。
9. 本工具下载的原音视频在文档写入检查通过后移入废纸篓。它不会删除自己原本存在的其他视频，也不自动清空废纸篓。只有自己决定不再需要恢复原视频时，才手动清空。

相同链接会复用原任务，已经完成且 Word 存在时不会重复生成。没有结果或任务失败时先阅读错误。不要在任务正在运行时反复启动多个工具副本、移动项目文件夹或改写任务 JSON。

Finder 排序：打开输出文件夹，在列表视图中右键表头 → 勾选“添加日期” → 点击该列直到较新的在前。Mac 可能继承旧视图偏好，必要时按这个方法手动确认一次。

## 6. 安装验收：每一项都应有证据

### 6.1 依赖及程序测试

```sh
cd "$HOME/VideoTranscript"
.venv/bin/python -m pip check
.venv/bin/python -m unittest test_reader test_app -q
```

pip check 应显示 No broken requirements found；单元测试应显示 OK。当前分享版有 9 项测试，其中 ASR 使用模拟结果，验证文档生成、时间戳与发言人写入、失败保护和页面功能。它们不是模型听写准确率测试，也不是真实网站下载测试。

### 6.2 不依赖视频网站登录的短音频实测

官方短英语样例链接：https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-ASR-Repo/asr_en.wav 。它是 Qwen 官方示例中使用的公开音频，不是个人文件。

在工具输入框提交这条链接。如果该 yt-dlp 版本不能识别直接音频链接，请由 Agent 使用下述本地分步验证；这一步只测试本地声纹、真实 Qwen 推理及 Word 导出，不能冒充网站下载已验收。

```sh
cd "$HOME/VideoTranscript"
curl --fail --location 'https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-ASR-Repo/asr_en.wav' --output work/official-sample.wav
```

随后让 Agent 按附录 reader.py 的接口建立独立的 work/jobs/<12位测试ID>/ 测试任务，将官方样例转换为 16kHz 单声道 WAV，调用 transcribe_qwen，写入 raw-transcript.json 后调用 build_document；meta 必须包含 url、title、name、media、audio，且媒体文件要放在本工具该测试任务的 media 子目录中。不得借测试任务删除用户其他文件。

成功证据：真实模型给出非空可读文字，Word 可打开，原链接存在，警示语完全匹配，有时间范围；删除行为只有本工具的测试源音频移入废纸篓。听写质量要对照样例试听，不能因为非空就判断准确。

### 6.3 真实视频测试

用自己能访问的公开短视频，先测试 1～3 分钟的单人音视频，再测试一个 1～3 分钟的双人对话。对话里最好有轮流发言，先避开大量同时讲话。

可以使用自己常看的 YouTube 或 B 站具体视频链接。分享者的示例链接：https://www.youtube.com/watch?v=40JP_fal3xA 。它约 17.5 分钟，不是最快的首次测试样例；访问权限与可用性可能随时变化。没有一个能保证永久可用且适合所有地区的测试链接。

记录：网页 URL、标题、网页时长、下载音轨时长、生成的 Word 路径、可读文字、不同发言人编号、原媒体是否在废纸篓、页面任务排序是否正确。比较发言人前后是否被错误合并或切成多个人。长视频建议在短测试完成后再试。

## 7. 更新、停止、备份与卸载

更新下载器：先等待当前任务结束，再在项目目录运行以下命令；重新启动服务后新任务才加载更新。

```sh
.venv/bin/python -m pip install --upgrade 'yt-dlp[default]'
```

不要一次盲目升级所有模型依赖；qwen-asr 0.0.6 与 transformers 4.57.6 是本指南的兼容组合。要升级，先保留现有环境，单独测试新版。

停止后台服务：先确认没有下载或识别任务在运行。Agent 可运行 lsof -nP -iTCP:8767 -sTCP:LISTEN，确认该 PID 的命令路径确实是自己的 VideoTranscript/app.py，再只停止该进程。不要使用 killall Python；它会影响其他程序。电脑重启后默认需重新双击启动工具。

备份：Word 在下载目录，工作记录与可恢复识别 JSON 在项目 work/jobs，模型在 work/model-cache。备份前等待任务完成。如果仅分享工具，不分享这些工作记录和模型缓存。

卸载：确认没有运行任务并停止本工具后，把 VideoTranscript 文件夹移入废纸篓。输出 Word 文件夹是独立的，想保留就不要删除。Python 和 Node 可能被其他软件使用，不要因为卸载本工具就自动卸载它们。

## 8. 常见问题及排查

| 现象 | 先做什么 | 不应该做什么 |
| --- | --- | --- |
| command not found: python3.12 | 确认装的是 3.12，重新开终端；检查 /Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 | 不要用系统 Python 做全局 pip 安装 |
| 架构显示 x86_64 | 关闭以 Rosetta 运行的终端，使用原生终端与 arm64 Python | 不要强行混装 arm64/x86_64 依赖 |
| Node 找不到或版本低 | 安装官方 LTS，重新开终端，执行 node --version | 不要复制分享者电脑上的 Node 路径 |
| HTTPS 证书错误 | 运行 Python 的 Install Certificates.command；检查时间、网络；Agent 核查证书配置 | 不关闭 TLS 验证，不用 --trusted-host 掩盖证书错误 |
| 模型下载失败 | 核查 Hugging Face 模型页能否访问，保留缓存后重试；记录域名与错误 | 不输入付费 API 密钥，不擅自换成未知来源权重 |
| 安装提示缺编译器 | 先核查包是否有本机 wheel；确实需要时按 macOS 官方提示安装 Command Line Tools | 不随意安装不明工具链 |
| Address already in use / 页面不是本工具 | 用 lsof 核查 8767 的进程身份；等待任务结束后处理重复服务 | 不杀掉身份不明的进程，不直接暴露公网端口 |
| 页面能打开但没有进展 | 看 work/app.log、对应 work/jobs/任务ID/run.log 以及 job.json；核查磁盘、睡眠和进程 | 不因界面无变化就删除正在运行的任务 |
| 视频要求登录、验证或不可用 | 先在自己的浏览器验证访问；必要时本人登录，再由 Agent 讨论本地 cookies 参数 | 不分享 Cookie、不绕过验证码或受保护媒体 |
| 页面不支持粘贴登录 Cookie | 当前页面没有这个选项；CLI 有 prepare URL --cookies-browser chrome/safari/firefox/edge 参数，由 Agent 按本机授权使用 | 不把 Cookie 上传给分享者或写进指南 |
| Word 没有真实姓名 | 发言人编号只是声纹估计；可自己阅读后改名 | 不把模型编号当作已验证身份 |
| 同时说话时识别乱 | 对照原音频验收，记录未区分或分错；高级分离需另外适配与评测 | 不把基础区分宣传为专业会议级准确率 |
| Finder 排序不是最新在前 | 在文件夹列表表头显示“添加日期”，点击切为倒序 | 不按文件名解释成添加时间 |
| 原视频没进废纸篓 | 读取 cleanup_error；核查输出 Word 的完整性与文件访问权限 | 不在 Word 未写入完整时强行删除源音频 |
| 长文件处理慢、电脑变热 | 接电源，预留内存与磁盘；继续后台等待，先用短样例验收 | 不保证 1 小时视频必定几分钟完成 |

反馈给 AI 的信息：macOS 版本、芯片、内存、Python/Node 版本、安装路径、出错阶段、最近相关错误日志。不必发送全部文稿、个人视频或登录凭据。日志也可能含 URL 和标题，先检查再分享。

## 9. 给 AI Agent 的执行任务书

用户可复制这段话给自己的本地 Agent：

“请阅读这份《网页视频转语音文稿-安装与使用指南》，先确认我的电脑是否属于适用范围；从配套源码或第 11 节完整源码附录建立 ~/VideoTranscript。按第 10 节阶段表完成环境检测、依赖安装、模型下载、启动与第 6 节验收。保留我的个人文件，使用本地免费模型和本机回环地址。请在你的权限范围内执行；遇到必须由我输入的管理员密码、登录、验证码或安全许可时说明具体步骤。不要仅因测试脚本 OK 就声称真实识别成功，最后给出安装路径、模型路径、Word 路径和逐项验收结果。”

指南是用户的操作说明，不是对 Agent 平台安全规则或权限的豁免。平台允许时可以自动完成下载安装和文件操作；必须人工完成的系统安装器、授权、登录、验证码等应交给用户。没有网络、文件或终端权限时，要具体报告限制。

## 10. Agent 分阶段操作清单

### A0：建立任务与边界

目标目录固定为当前用户的 ~/VideoTranscript，输出固定为 ~/Downloads/网页视频转语音文稿。若已有同名项目，先读取、核查是否为本工具；不覆盖不明文件，不删除已有模型。只绑定 127.0.0.1:8767，不部署公网。执行前记录自己拥有的文件、网络和进程权限。

### A1：环境检测

```sh
uname -m
sw_vers
python3.12 --version
python3.12 -c "import platform; print(platform.machine())"
node --version
df -h "$HOME"
```

期望 arm64 和 Python 3.12。macOS 版本没有验证过时如实记录，不能伪造兼容结论。缺少组件时优先使用第 3 节官方入口。现有 Python/Node 可复用；不要把本文当作允许卸载用户环境的授权。

### A2：源码准备

有源码 ZIP 就解压至目标目录；只有本文则运行第 11 节提取程序。先验证 文件校验.json；源码应不包含 分享者个人目录 的专用路径、个人历史任务 ID、个人 job.json、Cookie、.venv 或 work/model-cache。附录源码仅用于建立朋友电脑上的副本，不修改分享者正在运行的工具。

### A3：安装与下载

```sh
cd "$HOME/VideoTranscript"
python3.12 install.py
```

成功条件：pip check 通过，9 项单元测试 OK，prefetch_model.py 完成、模型路径存在、声纹模型可加载、FFmpeg 路径可执行。安装中不要自动清空共享 Hugging Face 缓存，也不要同时下载其他 ASR 大模型。下载失败与真实推理失败分别记录。

模型主要约 4.4GB，断点下载与解压期间可能需要额外空间。当前安装脚本是幂等的基本安装流程，不是已签名的 macOS App 安装器。重复安装不会自动删除工作记录，但也不保证跨依赖大版本更新完全可复现。

### A4：启动与健康检查

```sh
cd "$HOME/VideoTranscript"
chmod u+x 首次安装.command 启动工具.command
./启动工具.command
curl --fail http://127.0.0.1:8767/jobs
```

检查返回是本工具任务 JSON，浏览器页是“音视频文稿”。若端口有不明服务，先确认进程身份，不把其他服务响应误认为本工具健康。POST /jobs 需要 Origin: http://127.0.0.1:8767 与 JSON Content-Type，URL 字段是 url；接口返回 id 只代表入队，不代表完成。

```sh
curl --fail --request POST 'http://127.0.0.1:8767/jobs' --header 'Origin: http://127.0.0.1:8767' --header 'Content-Type: application/json' --data '{"url":"https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-ASR-Repo/asr_en.wav"}'
```

### A5：真实识别与验收

按第 6 节检查短音频和视频。等待 completed 前不得宣称成功；轮询可读 /jobs 和任务 JSON，但不每秒刷屏。任务过慢时读日志和进程状态，持续告知用户实际进度，不擅自终止下载或识别。真实对话验收要实际试听至少两人各一段，写入两个编号不等于模型分对。

### A6：交付与报告

交付：启动文件路径、本机网页地址、Word 所在目录、实际生成的示例 Word，以及每项通过/失败/未执行的结果。说明只在本机生成文稿，不用 API；说明样例音视频已进入废纸篓或未清理的原因。没有完成的网站测试、其他 Mac 测试和准确率评测要明确标未验证。

### A7：文件与版本说明

reader.py：下载、声纹区分、Qwen 转写、Word 生成和清理。app.py：本机后台服务和任务队列。index.html：页面。requirements.txt：依赖。install.py：首次安装流程。prefetch_model.py：提前下载模型及组件检查。两份 .command：小白入口。test_reader.py/test_app.py：程序单元测试。

模型源码与权重、下载器、声纹组件、FFmpeg 具有各自许可；本包没有重新分发这些权重或二进制运行环境，安装时从上游获取。需要商业分发或改名发布时，自己核查各上游许可与声明，不把这份私人分享指南当作法律许可意见。

## 11. 仅收到文档时：提取完整源码

Markdown 版能直接提取。如果收到的是 Word 版，先把本文附录代码准确导出为文本或让 Agent 读取 DOCX 段落。优先使用配套 Markdown，避免 Word 复制时引入智能引号、缩进或换行错误。

以下提取程序只接受清单中的固定文件名，验证附录中的 SHA-256 校验值，不调用网络、不执行提取出的代码、不覆盖已有目录。用户先将 Markdown 放在下载目录并保留文件名，再在终端运行。已有 VideoTranscript 时它会停止，让 Agent 核查后选择新目录。

```sh
python3.12 - <<'PY'
from pathlib import Path
import re, json, hashlib
source = Path.home() / 'Downloads/网页视频转语音文稿-安装与使用指南.md'
text = source.read_text(encoding='utf-8')
files = dict(re.findall(r'(?ms)^### FILE: ([^\n]+)\n```[^\n]*\n(.*?)\n```(?=\n|$)', text))
manifest = json.loads(files['文件校验.json'])
assert set(files) == set(manifest) | {'文件校验.json'}, '文件清单不完整或有额外文件'
for name, expected in manifest.items():
    assert Path(name).name == name and name not in ('.', '..'), '不安全的文件名'
    assert hashlib.sha256(files[name].encode('utf-8')).hexdigest() == expected, '校验失败：' + name
folder = Path.home() / 'VideoTranscript'
assert not folder.exists(), '目标目录已存在，先让 Agent 核查，禁止直接覆盖'
folder.mkdir()
for name, data in files.items():
    path = folder / name
    path.write_text(data, encoding='utf-8')
    if path.suffix == '.command':
        path.chmod(0o755)
print('源码提取并校验完成：', folder)
PY
```

校验值用于发现传输和复制损坏，不是第三方签名，也不能证明未知来源文档安全。请核对分享者身份。附录的每个 FILE 块对应一个 UTF-8 文件，保留全部内容与缩进，不能用省略号替代。

## 12. 本版验证记录

原版工具：曾在分享者 Mac 上完成真实 Qwen 短音频识别、单声纹分析、拼接双声音频分析、Word 生成和界面检查。多人分析属于基础声纹聚类，不是会议语料准确率评测。

本分享文档与便携源码：去除分享者的固定 Node 路径和个人排序记录；另外提供首次安装和模型预下载入口。本文交付时验证范围以随包“验证记录.json”为准：源码语法、脚本语法、文件校验、源码提取一致性、文档内容完整性和现有运行环境中的单元测试。不会宣称在朋友的全新 Mac 上已经安装成功，也不在制作指南时替用户再下载一次 4.4GB 模型。

## 附录：本分享版完整源码

以下为可供 Agent 重建的源码。普通读者可结束阅读。

### FILE: app.py
```python
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
from urllib.parse import urlparse

from reader import ROOT, WORK, OUTPUT, LEGACY_OUTPUT, NOTICE, save_json

HOST = '127.0.0.1'
PORT = int(os.environ.get('VIDEO_READER_PORT', '8767'))
tasks = queue.Queue()
pending = set()
mutex = threading.Lock()


def document_path(ident):
    job = WORK / 'jobs' / ident
    meta = json.loads((job / 'job.json').read_text())
    path = Path(meta.get('document', '/nonexistent')).resolve()
    if not any(root.resolve() in path.parents for root in (OUTPUT, LEGACY_OUTPUT, ROOT / 'outputs')) or not path.is_file():
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
    result = subprocess.run(['/usr/bin/open', '-a', 'Finder', str(path.parent)],
                            capture_output=True, text=True, timeout=15)
    if result.returncode:
        raise ValueError('Mac 未能打开 Finder。请从 Finder 双击启动文件，在正常环境中重启网页服务后再试。')



def fetch_title(ident, url):
    """Resolve metadata independently of the sequential transcription queue."""
    try:
        result = subprocess.run(
            [str(ROOT / '.venv/bin/python'), '-m', 'yt_dlp', '--skip-download',
             '--no-playlist', '--ignore-no-formats-error', '--no-warnings',
             '--socket-timeout', '8', '--retries', '0', '--print', 'title', url],
            capture_output=True, text=True, timeout=40)
        title = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else ''
        if result.returncode or not title or title == 'NA':
            return
        with mutex:
            path = WORK / 'jobs' / ident / 'job.json'
            meta = json.loads(path.read_text())
            # Active reader owns job.json. Separate metadata avoids competing writes.
            save_json(path.parent / 'page-title.json', {'title': title, 'url': url})
    except (OSError, ValueError, subprocess.SubprocessError):
        pass


def start_title_lookup(ident, url):
    threading.Thread(target=fetch_title, args=(ident, url), daemon=True).start()


def resume_jobs():
    # After restarting the web service, leave an existing reader process running.
    for item in sorted(list_jobs(), key=lambda item: item['created_at']):
        if item.get('state') not in ('completed', 'failed'):
            pending.add(item['id'])
            tasks.put((item['id'], item['url']))
            if not item.get('title'):
                start_title_lookup(item['id'], item['url'])

def task_created_at(folder):
    marker = folder / '.prepare.lock'
    path = marker if marker.exists() else folder
    stat = path.stat()
    return getattr(stat, 'st_birthtime', stat.st_mtime)


def list_jobs():
    items = []
    for path in (WORK / 'jobs').glob('*/job.json'):
        try:
            item = json.loads(path.read_text())
            item['id'] = path.parent.name
            title_path = path.parent / 'page-title.json'
            if not item.get('title') and title_path.exists():
                item['title'] = json.loads(title_path.read_text()).get('title')
            item['created_at'] = item.get('created_at', task_created_at(path.parent))
            item['has_document'] = bool(item.get('document') and Path(item['document']).is_file())
            items.append(item)
        except (ValueError, OSError):
            pass
    return sorted(items, key=lambda item: (item['created_at'], item['id']), reverse=True)


def worker():
    while True:
        ident, url = tasks.get()
        try:
            folder = WORK / 'jobs' / ident
            import fcntl
            with (folder / '.prepare.lock').open('a') as lock:
                while True:
                    try:
                        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        fcntl.flock(lock, fcntl.LOCK_UN)
                        break
                    except BlockingIOError:
                        time.sleep(2)
            with (folder / 'run.log').open('ab') as log:
                result = subprocess.run([str(ROOT / '.venv/bin/python'), str(ROOT / 'reader.py'),
                                        'prepare', url], stdout=log, stderr=log)
            if result.returncode == 0:
                (folder / 'run.log').unlink(missing_ok=True)
        finally:
            with mutex:
                pending.discard(ident)
            tasks.task_done()


def enqueue(url):
    if urlparse(url).scheme not in ('http', 'https') or not urlparse(url).hostname:
        raise ValueError('请输入完整的 HTTP/HTTPS 视频页面链接')
    ident = hashlib.sha256(url.encode()).hexdigest()[:12]
    folder = WORK / 'jobs' / ident
    folder.mkdir(parents=True, exist_ok=True)
    with mutex:
        if ident in pending:
            return ident
        meta = json.loads((folder / 'job.json').read_text()) if (folder / 'job.json').exists() else {}
        if meta.get('state') == 'completed' and Path(meta.get('document', '/nonexistent')).is_file():
            return ident
        import fcntl
        with (folder / '.prepare.lock').open('a') as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                return ident
            meta.setdefault('created_at', task_created_at(folder))
            meta.update(url=url, state='queued')
            meta.pop('error', None)
            save_json(folder / 'job.json', meta)
        pending.add(ident)
        tasks.put((ident, url))
        if not meta.get('title'):
            start_title_lookup(ident, url)
    return ident


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
        if self.path == '/jobs':
            return self.reply(200, list_jobs())
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
            if not 0 < length <= 5_000_000:
                raise ValueError('提交内容为空或过大')
            data = json.loads(self.rfile.read(length))
            if self.path == '/jobs':
                return self.reply(200, {'id': enqueue(data['url'].strip())})
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
    resume_jobs()
    threading.Thread(target=worker, daemon=True).start()
    print(f'音视频文稿队列：http://{HOST}:{PORT}', flush=True)
    server.serve_forever()

```

### FILE: index.html
```html
<!doctype html>
<html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>音视频文稿</title>
<style>
body{font:16px/1.7 -apple-system,BlinkMacSystemFont,sans-serif;color:#24322d;background:#f4f6f3;max-width:920px;margin:48px auto;padding:0 24px}h1{font-size:32px}input,button,.action{font:inherit;padding:10px 14px;border:1px solid #c6d1ca;border-radius:8px}input[type=url]{flex:1;min-width:180px}button,.action{background:#245441;color:white;cursor:pointer;text-decoration:none;display:inline-block}form,.actions{display:flex;gap:12px;flex-wrap:wrap}article{background:white;padding:24px;border:1px solid #e0e7e1;border-radius:12px;margin:20px 0}small{color:#62736b}a{color:#245441}#message{color:#8b4520}.notice{background:#fff3cd;color:#9c0006;padding:14px 18px;border-left:4px solid #b07800;font-weight:bold}.secondary{background:white;color:#245441}
</style>
<h1>音视频文稿</h1>
<p>粘贴网页链接，后台下载并用 Qwen3-ASR-1.7B 识别语音，自动区分发言人，生成带时间戳、以视频标题命名的 Word。</p>
<form id="form"><input id="url" aria-label="音视频网页链接" type="url" required placeholder="粘贴 YouTube、哔哩哔哩等音视频网页链接"><button>开始生成文稿</button></form>
<p id="message" role="status"></p>
<p class="notice">本文稿内容为语音模型识别结果，需要注意：可能有错别字和识别不准确之处。</p>
<p><small>Word 保存到“下载/网页视频转语音文稿”。无需提交给其他 AI；完成后直接查看或打开所在位置。Word 完整性检查通过后自动将原音视频移入废纸篓并清理临时音轨。</small></p>
<div id="jobs"></div>
<script>
const historicalTaskTimes={};
const stages={queued:'排队中',downloading:'正在下载',downloaded:'下载完成',diarizing:'本地模型正在区分发言人',transcribing:'本地模型正在识别语音',completed:'Word 已生成，可以查看',failed:'处理失败，进度已保留'};
const msg=document.querySelector('#message');
async function post(url,data){let r=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});let j=await r.json();if(!r.ok)throw Error(j.error);return j}
document.querySelector('#form').onsubmit=async e=>{e.preventDefault();try{await post('/jobs',{url:document.querySelector('#url').value});msg.textContent='已加入后台队列。你可以继续做其他事情，稍后回来查看文稿。';await refresh()}catch(e){msg.textContent=e.message}};
function taskHeading(j){let title=j.title;if(j.state==='queued')return '待处理 · '+(title||'正在获取标题（'+new URL(j.url).hostname+' / '+(new URL(j.url).searchParams.get('v')||new URL(j.url).pathname.split('/').filter(Boolean).pop()||j.id)+'）');return title||'正在获取标题 · '+j.id}
function link(text,url,style){let a=document.createElement('a');a.textContent=text;a.href=url;if(style)a.className=style;return a}
async function refresh(){try{let jobs=await(await fetch('/jobs')).json();jobs.sort((a,b)=>(b.created_at??historicalTaskTimes[b.id]??b.added_at??Infinity)-(a.created_at??historicalTaskTimes[a.id]??a.added_at??Infinity));let host=document.querySelector('#jobs');host.replaceChildren();for(let j of jobs){let card=document.createElement('article');let h=document.createElement('h2');h.textContent=taskHeading(j);card.append(h);let p=document.createElement('p');p.textContent=(j.document&&!j.has_document)?'Word 文件已不在原保存位置，重新提交链接可生成':(stages[j.state]||'准备生成文稿');if(j.state==='transcribing'&&j.transcribed_seconds)p.textContent+=' · '+Math.floor(j.transcribed_seconds/60)+' / '+Math.ceil(j.audio_duration/60)+' 分钟';card.append(p);card.append(link('原网页',j.url));if(j.error){let err=document.createElement('p');err.textContent=j.error;card.append(err)}if(j.cleanup_error){let note=document.createElement('p');note.textContent='Word 已生成，但部分临时文件未清理：'+j.cleanup_error;card.append(note)}if(j.has_document){let actions=document.createElement('p');actions.className='actions';actions.append(link('查看 Word 文稿','/preview/'+j.id,'action'));let reveal=document.createElement('button');reveal.type='button';reveal.className='secondary';reveal.textContent='打开文档所在位置';let revealStatus=document.createElement('small');revealStatus.setAttribute('role','status');reveal.onclick=async()=>{reveal.disabled=true;revealStatus.textContent='正在打开文件夹…';try{await post('/reveal/'+j.id,{});revealStatus.textContent='已打开 Finder 文件夹。';msg.textContent='已打开文档所在的 Finder 文件夹。'}catch(e){revealStatus.textContent='打开失败：'+e.message;msg.textContent='打开失败：'+e.message}finally{reveal.disabled=false}};actions.append(reveal);actions.append(revealStatus);let download=link('下载 Word','/document/'+j.id,'action secondary');download.download=j.name+'.docx';actions.append(download);card.append(actions);let note=document.createElement('small');note.textContent=j.temporary_files_removed?(j.media_trashed?'原音视频已移入废纸篓，临时音轨已清理。':'原音视频与临时音轨已清理。'):'Word 内容未经人工校对。';card.append(note)}host.append(card)}}catch(e){msg.textContent='后台连接中断，请重新启动工具。'}}
refresh();setInterval(refresh,6000);
</script></html>

```

### FILE: install.py
```python
#!/usr/bin/env python3
import os, platform, shutil, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
if platform.system() != "Darwin" or platform.machine() != "arm64":
    raise SystemExit("本安装版仅验证 Apple 芯片 Mac；请使用原生 arm64 终端。")
if sys.version_info[:2] != (3, 12):
    raise SystemExit("请先安装 Python 3.12，再运行首次安装。")
node = shutil.which("node")
if not node or int(subprocess.check_output([node, "--version"], text=True).strip().lstrip("v").split(".")[0]) < 22:
    raise SystemExit("请先从 nodejs.org 安装 Node.js 22 或以上的 LTS 版本。")
folder = ROOT / ".venv"
if not folder.exists():
    subprocess.run([sys.executable, "-m", "venv", str(folder)], check=True)
python = str(folder / "bin/python")
subprocess.run([python, "-m", "pip", "install", "--upgrade", "pip"], check=True)
subprocess.run([python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
subprocess.run([python, "-m", "pip", "check"], check=True)
subprocess.run([python, "-m", "unittest", "test_reader", "test_app", "-q"], check=True)
print("正在下载 Qwen3-ASR-1.7B 模型（约 4.4GB），可以等待，不要关闭窗口。", flush=True)
subprocess.run([python, "prefetch_model.py"], check=True)
print("安装完成。请双击：启动工具.command。", flush=True)

```

### FILE: prefetch_model.py
```python
from pathlib import Path
from huggingface_hub import snapshot_download
from resemblyzer import VoiceEncoder
from reader import ffmpeg
root = Path(__file__).resolve().parent
path = snapshot_download("Qwen/Qwen3-ASR-1.7B", cache_dir=str(root / "work/model-cache"),
                         allow_patterns=["*.json", "*.safetensors", "*.txt", "*.model"])
print("Qwen 模型下载完成：", path)
VoiceEncoder(device="cpu", verbose=False)
print("声纹模型可加载；FFmpeg 路径：", ffmpeg())

```

### FILE: reader.py
```python
#!/usr/bin/env python3
"""Background download, local speech recognition and verified Word export."""
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
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work'
LEGACY_OUTPUT = Path.home() / 'Downloads' / '音视频文稿'
OUTPUT = Path.home() / 'Downloads' / '网页视频转语音文稿'
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
    return title or '未命名音视频'


def ffmpeg():
    import imageio_ffmpeg
    folder = WORK / 'bin'
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / 'ffmpeg'
    if not target.exists():
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
    return path, json.loads((path / 'job.json').read_text())


def make_blocks(segments, limit=2200):
    # Keep each audio interval and each speaker turn visible, rather than merging timestamps.
    return [dict(seg, id=i + 1, text=seg['text'].strip())
            for i, seg in enumerate(segments) if seg.get('text', '').strip()]


def speaker_turns(wav, job):
    """Local voice embeddings + conservative clustering; labels are estimates, not identities."""
    import numpy as np
    import torch
    from resemblyzer import VoiceEncoder
    from sklearn.cluster import AgglomerativeClustering
    torch.set_num_threads(4)
    import webrtcvad
    detector = webrtcvad.Vad(2)
    encoder = VoiceEncoder(device='cpu', verbose=False)
    vectors, intervals = [], []
    with wave.open(str(wav)) as source:
        rate, frames = source.getframerate(), source.getnframes()
        if rate != 16000:
            raise ValueError('声纹区分需要 16kHz 音轨')
        for start in range(0, frames, rate):
            source.setpos(start)
            pcm = source.readframes(2 * rate)
            piece = np.frombuffer(pcm, dtype='<i2').astype(np.float32) / 32768
            speech = [detector.is_speech(pcm[i:i+960], rate) for i in range(0, len(pcm)-959, 960)]
            if len(piece) < rate * .5 or not speech or sum(speech) / len(speech) < .25:
                continue
            vectors.append(encoder.embed_utterance(piece))
            intervals.append((start / rate, (start + len(piece)) / rate))
    if not vectors:
        return [{'start': 0, 'end': frames / rate, 'speaker': '发言人未确定'}]
    embeddings = np.array(vectors)
    # Bound clustering RAM on many-hour recordings; classify the other windows by reference similarity.
    step = max(1, int(np.ceil(len(vectors) / 3000)))
    references = embeddings[::step]
    labels = ([0] if len(references) == 1 else AgglomerativeClustering(
        n_clusters=None, distance_threshold=.35, metric='cosine', linkage='average').fit_predict(references))
    if step > 1:
        centers = np.array([references[np.asarray(labels) == label].mean(axis=0) for label in sorted(set(labels))])
        centers /= np.maximum(np.linalg.norm(centers, axis=1, keepdims=True), 1e-8)
        labels = embeddings @ centers.T
        labels = labels.argmax(axis=1)
    names, turns = {}, []
    for (start, end), label in zip(intervals, labels):
        if int(label) not in names:
            names[int(label)] = f'发言人 {len(names) + 1}'
        speaker = names[int(label)]
        if turns and turns[-1]['speaker'] == speaker and start - turns[-1]['end'] < 2:
            turns[-1]['end'] = end
        else:
            if turns and start < turns[-1]['end']:
                boundary = (start + turns[-1]['end']) / 2
                turns[-1]['end'] = boundary
                start = boundary
            turns.append({'start': start, 'end': end, 'speaker': speaker})
    return turns


def transcribe_qwen(wav, job, meta, model_name):
    import numpy as np
    import torch
    from qwen_asr import Qwen3ASRModel
    from qwen_asr.inference.utils import split_audio_into_chunks
    from huggingface_hub import snapshot_download
    torch.set_num_threads(4)
    meta['state'] = 'diarizing'
    save_json(job / 'job.json', meta)
    turn_path = job / 'speaker-turns.json'
    if not turn_path.exists():
        save_json(turn_path, speaker_turns(wav, job))
    turns = json.loads(turn_path.read_text())
    meta['state'] = 'transcribing'
    save_json(job / 'job.json', meta)
    model_dir = snapshot_download(model_name, cache_dir=str(WORK / 'model-cache'),
                                  allow_patterns=['*.json', '*.safetensors', '*.txt', '*.model'])
    model = Qwen3ASRModel.from_pretrained(
        model_dir, device_map="cpu", dtype=torch.bfloat16,
        max_inference_batch_size=1, max_new_tokens=4096)
    checkpoint_dir = job / 'checkpoints-Qwen3-ASR-1.7B-speakers'
    checkpoint_dir.mkdir(exist_ok=True)
    items, language = [], None
    with wave.open(str(wav)) as audio:
        rate, frames = audio.getframerate(), audio.getnframes()
        # The SDK splits long inputs at silence; outer chunks bound RAM and enable resume.
        chunk_frames = rate * 300
        for index, start in enumerate(range(0, frames, chunk_frames)):
            checkpoint = checkpoint_dir / f'{index:05}.json'
            if checkpoint.exists():
                saved = json.loads(checkpoint.read_text())
            else:
                audio.setpos(start)
                samples = np.frombuffer(audio.readframes(chunk_frames), dtype='<i2').astype(np.float32) / 32768
                current, detected_language = [], None
                # Prefer quiet boundaries and keep each inference small enough for this Mac.
                pieces = []
                chunk_start, chunk_end = start / rate, (start + len(samples)) / rate
                for turn in turns:
                    left, right = max(chunk_start, turn['start']), min(chunk_end, turn['end'])
                    if right <= left:
                        continue
                    turn_audio = samples[round((left-chunk_start)*rate):round((right-chunk_start)*rate)]
                    for piece, offset in split_audio_into_chunks(turn_audio, rate, max_chunk_sec=30):
                        pieces.append((piece, left-chunk_start+offset, turn['speaker']))
                for piece, offset, speaker in pieces:
                    results = model.transcribe(audio=(piece, rate), language=None)
                    current.append({'start': start / rate + offset,
                                    'end': start / rate + offset + len(piece) / rate,
                                    'text': results[0].text.strip(), 'speaker': speaker})
                    detected_language = detected_language or results[0].language
                    meta['transcribed_seconds'] = current[-1]['end']
                    save_json(job / 'job.json', meta)
                saved = {'segments': current, 'language': detected_language}
                save_json(checkpoint, saved)
            items.extend(saved['segments'])
            language = language or saved['language']
            meta['transcribed_seconds'] = min(start + chunk_frames, frames) / rate
            save_json(job / 'job.json', meta)
            print(f'转写进度 {stamp(meta["transcribed_seconds"])} / {stamp(frames / rate)}', flush=True)
    return {'text': ' '.join(s['text'] for s in items), 'segments': items,
            'language': language, 'duration': frames / rate, 'model': model_name,
            'timestamp_precision': '音频片段起止范围，非逐字对齐',
            'speaker_method': '本地声纹聚类（估计）；发言人编号和切换位置为估计，重叠发言可能无法区分'}


def prepare(args):
    from yt_dlp import YoutubeDL
    from urllib.parse import urlparse
    if urlparse(args.url).scheme not in ('http', 'https'):
        raise ValueError('请输入 HTTP 或 HTTPS 网页链接')
    try:
        os.nice(10)
    except PermissionError:
        print('当前执行环境不允许调整进程优先级，继续单任务处理。', flush=True)
    ff = ffmpeg()
    ident = hashlib.sha256(args.url.encode()).hexdigest()[:12]
    job = WORK / 'jobs' / ident
    job.mkdir(parents=True, exist_ok=True)
    lock = job / '.prepare.lock'
    # OS file locks release automatically after an interrupted process.
    import fcntl
    with lock.open('w') as handle:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        meta = {'url': args.url, 'state': 'downloading'}
        if (job / 'job.json').exists():
            meta = json.loads((job / 'job.json').read_text())
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
            node = shutil.which('node')
            if node:
                options['js_runtimes'] = {'node': {'path': node}}
            if args.cookies_browser:
                options['cookiesfrombrowser'] = (args.cookies_browser,)
            if not meta.get('media') or not Path(meta['media']).exists():
                media_folder.mkdir(parents=True, exist_ok=True)
                with YoutubeDL(options) as downloader:
                    info = downloader.extract_info(args.url, download=True)
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
                partial = wav.with_name('transcription-audio.partial.wav')
                subprocess.run([ff, '-nostdin', '-v', 'error', '-y', '-i', meta['media'],
                                '-vn', '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le',
                                str(partial)], check=True)
                partial.replace(wav)
            with wave.open(str(wav)) as audio:
                duration = audio.getnframes() / audio.getframerate()
            if not duration:
                raise ValueError('音轨为空')
            meta['audio_duration'] = duration
            if meta.get('duration') and abs(duration - meta['duration']) > max(5, duration * .01):
                raise ValueError('下载音轨时长与网页时长不符，需要检查')
            meta['state'] = 'transcribing'
            meta['model'] = args.model
            save_json(job / 'job.json', meta)
            os.environ['HF_HOME'] = str(WORK / 'model-cache')
            os.environ.setdefault('SSL_CERT_FILE', '/etc/ssl/cert.pem')
            raw_path = job / 'raw-transcript.json'
            raw = json.loads(raw_path.read_text()) if raw_path.exists() else {}
            if raw.get('model') != args.model:
                raw = transcribe_qwen(wav, job, meta, args.model)
                save_json(raw_path, raw)
            build_document(job, raw)
            print(f'Word 已生成：{job}', flush=True)
        except Exception as error:
            meta.update(state='failed', error=str(error))
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
    if not texts or texts[0] != meta['url']:
        raise ValueError('Word 缺少原网页链接')
    if NOTICE not in texts:
        raise ValueError('Word 缺少识别准确性提示')
    for block in blocks:
        caption = f'[{stamp(block["start"])}–{stamp(block["end"])}] {block.get("speaker", "")}'
        if caption not in texts:
            raise ValueError('Word 缺少时间戳或发言人标注')
        if block['text'] not in texts:
            raise ValueError('Word 未完整保存语音识别结果')
    return {'zip_valid': True, 'first_line_url': True, 'notice_present': True,
            'all_blocks_present': len(blocks), 'accuracy': '未经人工校对的语音模型识别结果'}


def clear_intermediate(job, meta):
    import shutil
    report = json.loads((job / 'validation.json').read_text())
    path = Path(meta['document'])
    if hashlib.sha256(path.read_bytes()).hexdigest() != report['document_sha256']:
        raise ValueError('Word 已改动，拒绝清理原媒体')
    raw = json.loads((job / 'raw-transcript.json').read_text())
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
                 '网页校对结果.json', 'submitted-result.json', 'result.json', 'speaker-turns.json'):
        (job / name).unlink(missing_ok=True)
    meta['temporary_files_removed'] = True
    save_json(job / 'job.json', meta)


def configure_folder_sort(folder):
    """Persist Finder list-view settings for this output folder only."""
    from ds_store import DSStore
    settings = folder / '.DS_Store'
    with DSStore.open(str(settings), 'r+' if settings.exists() and settings.stat().st_size else 'w+') as store:
        preferences = {
            'viewOptionsVersion': 1, 'iconSize': 16.0, 'showIconPreview': True,
            'sortColumn': 'dateAdded', 'textSize': 13.0, 'useRelativeDates': True,
            'calculateAllSizes': False, 'columns': {
                'name': {'index': 0, 'width': 450, 'visible': True, 'ascending': True},
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
    raw = raw if raw is not None else json.loads((job / 'raw-transcript.json').read_text())
    blocks = make_blocks(raw.get('segments', []))
    if not blocks:
        raise ValueError('识别结果为空，保留媒体，不生成 Word')
    folder = OUTPUT
    folder.mkdir(parents=True, exist_ok=True)
    path = Path(meta['document']) if meta.get('document') and Path(meta['document']).parent == folder else folder / (meta['name'] + '.docx')
    if path.exists() and str(path) != meta.get('document'):
        path = folder / (meta['name'] + ' (' + job.name + ').docx')
    doc = Document()
    normal = doc.styles['Normal']
    normal.font.name = 'Arial'
    normal.font.size = Pt(11)
    normal.element.rPr.rFonts.set(qn('w:eastAsia'), 'PingFang SC')
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
    partial = path.with_suffix('.partial.docx')
    doc.save(partial)
    report = verify_document(partial, meta, blocks)
    partial.replace(path)
    # Page order uses the first successful export time; Finder uses the system's added date.
    meta.setdefault('added_at', time.time())
    configure_folder_sort(folder)
    report['document_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    save_json(job / 'validation.json', report)
    meta.update(state='completed', document=str(path), blocks=len(blocks),
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
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    prep = sub.add_parser('prepare')
    prep.add_argument('url')
    prep.add_argument('--cookies-browser', choices=['chrome', 'safari', 'firefox', 'edge'])
    prep.add_argument('--model', choices=['Qwen/Qwen3-ASR-1.7B'], default='Qwen/Qwen3-ASR-1.7B')
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
qwen-asr==0.0.6
av>=11,<17

resemblyzer==0.1.4
send2trash
scikit-learn
ds-store
setuptools<81

transformers==4.57.6
torch>=2.6,<3

```

### FILE: test_app.py
```python
import json
import tempfile
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
        (job / 'job.json').write_text(json.dumps({'document': str(path)}))
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
            with patch.object(app, 'WORK', root / 'work'), patch.object(app, 'OUTPUT', output), patch('app.subprocess.run') as run:
                run.return_value.returncode = 0
                app.reveal_document(job.name)
                run.assert_called_once_with(['/usr/bin/open', '-a', 'Finder', str(path.resolve().parent)], capture_output=True, text=True, timeout=15)
                path.unlink()
                with self.assertRaises(ValueError):
                    app.reveal_document(job.name)

    def test_queued_title_is_read_from_separate_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            job = root / 'jobs/123456abcdef'
            job.mkdir(parents=True)
            (job / 'job.json').write_text(json.dumps({'url': 'https://example.com/v', 'state': 'queued'}))
            (job / 'page-title.json').write_text(json.dumps({'title': '对话视频'}))
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
            (job / 'job.json').write_text(json.dumps(meta))
            with patch.object(app, 'WORK', root), patch('app.subprocess.run') as run:
                run.return_value.returncode = 0
                run.return_value.stdout = '对话标题\n'
                app.fetch_title(job.name, meta['url'])
            self.assertEqual(json.loads((job / 'job.json').read_text()), meta)
            self.assertEqual(json.loads((job / 'page-title.json').read_text())['title'], '对话标题')


if __name__ == '__main__':
    unittest.main()

```

### FILE: test_reader.py
```python
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
import numpy
import torch


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
        p = patch.object(reader, 'speaker_turns', side_effect=lambda wav, job: [{'start': 0, 'end': reader_audio_duration(wav), 'speaker': '发言人 1'}])
        p.start(); self.addCleanup(p.stop)
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

    def qwen_mock(self):
        factory = MagicMock()
        factory.return_value.transcribe.side_effect = lambda **kw: [SimpleNamespace(text='完整识别文字 80%。', language='Chinese')]
        return factory, {'qwen_asr': SimpleNamespace(Qwen3ASRModel=SimpleNamespace(from_pretrained=factory)),
            'qwen_asr.inference.utils': SimpleNamespace(split_audio_into_chunks=lambda samples, rate, **kw: [(samples, 0)])}

    def test_automatic_word_generation_and_cleanup(self):
        job, meta, audio = self.fixture()
        factory, modules = self.qwen_mock()
        with patch.dict('sys.modules', modules), patch('huggingface_hub.snapshot_download', return_value='test-model'), patch.object(reader, 'ffmpeg', return_value='/unused'):
            reader.prepare(argparse.Namespace(url=meta['url'], cookies_browser=None, model='Qwen/Qwen3-ASR-1.7B'))
        saved = json.loads((job / 'job.json').read_text())
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
        self.assertEqual(Path(saved['document']).name, '测试标题.docx')
        self.assertFalse(audio.exists())
        self.assertTrue((self.trash / audio.name).exists())
        self.assertEqual(Path(saved['document']).parent, self.output)
        self.assertIn('[00:00:00–00:00:01] 发言人 1', texts)
        self.assertFalse(list(job.glob('checkpoints-*')))
        self.assertFalse((job / 'ChatGPT校对任务.txt').exists())
        self.assertTrue(saved['temporary_files_removed'])

    def test_interrupted_transcription_checkpoint_resume(self):
        job, meta, audio = self.fixture(301)
        factory, modules = self.qwen_mock()
        with patch.dict('sys.modules', modules), patch('huggingface_hub.snapshot_download', return_value='test-model'):
            first = reader.transcribe_qwen(audio, job, meta, 'Qwen/Qwen3-ASR-1.7B')
            self.assertEqual(factory.return_value.transcribe.call_count, 2)
            factory.return_value.transcribe.reset_mock()
            second = reader.transcribe_qwen(audio, job, meta, 'Qwen/Qwen3-ASR-1.7B')
            self.assertEqual(factory.return_value.transcribe.call_count, 0)
            self.assertEqual(first, second)
            self.assertEqual(second['segments'][1]['start'], 300)

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
        meta = json.loads((job / 'job.json').read_text())
        with self.assertRaises(ValueError):
            reader.clear_intermediate(job, meta)
        self.assertTrue(audio.exists())


if __name__ == '__main__':
    unittest.main()

```

### FILE: 启动工具.command
```sh
#!/bin/zsh
cd "${0:A:h}" || exit 1
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
if [[ ! -x .venv/bin/python ]]; then print '请先运行 首次安装.command'; read 'reply?按回车退出。'; exit 1; fi
mkdir -p work
if curl --silent --fail --max-time 2 http://127.0.0.1:8767/jobs >/dev/null; then
  print '端口 8767 已有服务，请先确认浏览器中的页面确实是本工具。'
else
  nohup .venv/bin/python app.py >> work/app.log 2>&1 < /dev/null &
  print '已请求后台启动；请稍后打开 http://127.0.0.1:8767'
fi
print '确认页面能打开后，这个终端窗口可以关闭。'

```

### FILE: 文件校验.json
```json
{
  "app.py": "74db0bed1e6ad6af8963548c9d5a8d74f9f971a38cf1bbdcda551d40b850adf9",
  "index.html": "28153eca7502ca97f4d6c1667c6daae8344a7afb2e01820ee451383e627e0d7e",
  "install.py": "d423b71bfd29145b2b6616da4b6474ad86beec07813eb8c9c36330ed298f19bb",
  "prefetch_model.py": "1c7512114bdb7d49b6a2d8a4199452f5291ad4c04fc4effa4e329b4dab227df3",
  "reader.py": "90dceae00db3c5f91a0eadecb20a9e7347b709de33241bf3eff11d680e83f3a6",
  "requirements.txt": "aa237150a51d1f468ccab935e7ccd3235beddaf60afb9719676dc7f8fbf63e7c",
  "test_app.py": "3bb5c3f39a4d7c0782a0a7a970e5580bc69d8204c3170468a166a2d556f84737",
  "test_reader.py": "ea7af8f55bfe4c47023ee9f712b6b078cfc9dd0beedec2325134556970fdc059",
  "启动工具.command": "f67940511e7be84f96ef4eadc60dee14b08668d185f06f94cd03a02ebd3d59ca",
  "首次安装.command": "3386934c6c62f0983f9d9ee8541bf0d73a4fa671be319201efa649bf71c28d32"
}

```

### FILE: 首次安装.command
```sh
#!/bin/zsh
cd "${0:A:h}" || exit 1
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
if ! command -v python3.12 >/dev/null 2>&1; then
  print '请先安装 Python 3.12： https://www.python.org/downloads/macos/'
  read 'reply?按回车退出。'; exit 1
fi
python3.12 install.py
result=$?
if (( result != 0 )); then print '安装未完成，请保留报错文字供 AI 排查。'; fi
read 'reply?按回车关闭窗口。'
exit $result

```

