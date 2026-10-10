# 网页视频转语音识别文字稿（由千问提供支持）

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

页面上有标题旁蓝色“登录或打开千问”按钮。识别任务检测到登录失效后显示需要重新登录；点击按钮登录、关闭登录窗口，再点击重试。空闲时不保证实时发现过期，也不会主动抢占屏幕。

已完成任务的“删除任务并同步到千问”与“查看 Word 文稿”“打开文档所在位置”同排，不再提供重复下载按钮。每条任务的“删除任务并同步到千问”会停止该任务，将相关本机文件、已完成和未完成 Word、任务记录移入废纸篓；点击“删除任务并同步到千问”会删除对应千问记录，云端删除后无法恢复。删除结果逐项列出工具任务记录、本机文稿及任务文件、对应千问记录，每项成功显示绿色、失败显示红色；千问记录未找到而按成功处理时显示绿色并注明情况。绿色成功提示在卡片消失后显示3秒自动清空；红色失败提示保留；失败原因保留在任务卡片并随刷新显示。成功删除后任务卡片立即从工具列表消失，旧的刷新结果不会把卡片重新显示。云端删除失败则保留本机任务和文稿，提示原因后可重试；未上传的任务只清理本机。仅删除含本工具任务编号且唯一匹配的记录，千问未找到对应记录时仍清理本机，整体按成功处理，并明确注明未找到、未执行云端删除；多个匹配记录或页面/登录异常仍视为失败。模型和登录信息不会上传 GitHub。

## 新电脑安装

仅在 Apple 芯片 Mac / Python 3.12 环境验证。Windows、Intel Mac 暂未验证。

1. 在本仓库点击绿色 **Code → Download ZIP**，解压到固定位置，不要只运行压缩包内的文件。
2. 安装 [Python 3.12](https://www.python.org/downloads/release/python-31210/) 的 macOS universal2 安装包。安装后运行 Applications/Python 3.12/Install Certificates.command。
3. 安装 [Node.js](https://nodejs.org/en/download) 22 或更高 LTS 的 macOS 安装包。
4. 双击“首次安装.command”。下载 Python 依赖及 Chromium 浏览器，首次需要网络。
5. 双击“配置千问登录.command”登录，然后启动工具。
6. 如 macOS 阻止打开 command 文件，在 Finder 右键打开；仅对自己信任的源码操作，不关闭系统安全保护。
7. 可双击“启用自动启动.command”，实现登录 Mac 后启动、服务停止后自动重启。恢复未完成任务可能重新处理部分步骤。

更新时停止服务，备份 work 中的任务记录与浏览器登录资料，替换源码和重新安装 requirements 后启动；不要用别人的登录资料覆盖自己的。朋友电脑不会因 GitHub 更新自动升级。

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

## 给 AI Agent 的安装与验收步骤

- 读取 README 和 INSTALL_GUIDE，确认 macOS arm64、Python 3.12、Node.js 22+。
- 执行 `python3.12 install.py`。依赖只来自 requirements；不得下载本地 ASR 模型。
- 执行 `.venv/bin/python -m unittest test_reader test_app test_qianwen test_task_controls` 和 pip check。
- 让用户在专用浏览器中完成登录。验证码和账号密码由用户处理，不提交凭据。
- 启动服务，检查 /health 返回 engines 为仅 qianwen。
- 用获授权的短音频验证下载、千问原文导出、最终 Word、链接、提示、发言人、时间戳、媒体移入废纸篓。
- 检查登录失效提示和删除按钮；测试删除只使用临时测试文件。
- 不把任务记录、个人文稿、音视频、日志、work、.venv、Cookie 或缓存提交仓库。

## 验证说明

本次 48 项测试通过，其中云端识别返回结果在单元测试中模拟；旧本地推理断点测试已移除。此前本机20秒音频的千问后台完整流程约46秒，不能推断长视频速度或识别准确率。未在另一台全新 Mac 完成安装实测。

## 主要文件

`app.py` 网页服务；`reader.py` 下载与 Word；`qianwen_browser.py` 千问后台浏览器；`task_controls.py` 删除任务；`install.py` 安装；`requirements.txt` 依赖；`INSTALL_GUIDE.md` 含完整源码的安装指南。

本项目采用 MIT 许可证，第三方组件遵循各自许可证。

## 仅收到本文档：完整源码

AI Agent 可按 FILE 标记逐个提取文件，核对文件校验.json 后执行安装。保存 command 文件后运行 chmod +x *.command。切换旧版本仅需双击“切换千问并清理本地模型.command”，完成后刷新网页。该迁移会保留文稿和任务，永久清除本工具模型缓存与旧推理依赖。

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


def document_path(ident):
    job = WORK / 'jobs' / ident
    meta = json.loads((job / 'job.json').read_text())
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
             '--socket-timeout', '8', '--retries', '0', '--print', 'title', download_url(url)],
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
        if item.get('state') not in ('completed', 'failed', 'login_required'):
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
    items = []
    for path in (WORK / 'jobs').glob('*/job.json'):
        try:
            item = json.loads(path.read_text())
            item['id'] = path.parent.name
            deletion=path.parent/'delete-result.json'
            if deletion.exists():item['deletion_result']=json.loads(deletion.read_text())
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
        ident, url, generation = tasks.get()
        log=None
        try:
            folder = WORK / 'jobs' / ident
            import fcntl
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
                process=subprocess.Popen([str(ROOT/'.venv/bin/python'),str(ROOT/'reader.py'),
                     'prepare',url,'--engine',json.loads((folder/'job.json').read_text()).get('engine','qianwen')],
                     stdout=log,stderr=log,start_new_session=True)
                active_readers[ident]=(process,generation)
            result=process.wait();log.close()
            if result==0:(folder/'run.log').unlink(missing_ok=True)
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            record=WORK/'jobs'/ident/'job.json'
            if record.exists() and (ident,generation) not in cancelled:
                try:
                    meta=json.loads(record.read_text())
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
            import fcntl
            with (folder/'.prepare.lock').open('a') as lock:
                deadline=time.monotonic()+15
                while True:
                    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);break
                    except BlockingIOError:
                        if time.monotonic()>deadline:raise ValueError('任务尚未停止，请稍后重试删除')
                        time.sleep(.2)
                result=subprocess.run([str(ROOT/'.venv/bin/python'),str(ROOT/'qianwen_browser.py'),'delete','--job',ident],capture_output=True,text=True,timeout=120)
                if result.returncode:raise ValueError('千问同步删除失败，本机任务和文稿已保留：'+(result.stderr.strip().splitlines()[-1] if result.stderr.strip() else '后台浏览器未能完成删除'))
        except Exception as error:
            (folder/'.deleting').unlink(missing_ok=True)
            meta=json.loads((folder/'job.json').read_text())
            if meta.get('state') not in ('completed','failed','login_required'):
                meta.update(state='failed',error='任务已停止，千问同步删除未完成：'+str(error))
                save_json(folder/'job.json',meta)
            raise
        cloud_meta=json.loads((folder/'job.json').read_text())
        cloud_status=cloud_meta.get('qianwen_delete_result','deleted' if cloud_meta.get('qianwen_cloud_deleted') else 'failed')
        result=trash_task(ROOT,WORK,[OUTPUT,LEGACY_OUTPUT,ROOT/'outputs',OUTPUT.parent/'网页视频转语音文稿'],ident)
        pending.discard(ident);generations.pop(ident,None)
        result['deletion_result']=deletion_report(True,cloud_status)
        result['message']=result['deletion_result']['message']
        return result


def login_status():
    path=WORK/'qianwen-auth.json'
    state=json.loads(path.read_text()) if path.exists() else {'status':'unknown'}
    if not state.get('last_success'):
        successes=[item.get('added_at',0) for item in list_jobs() if item.get('state')=='completed' and item.get('model')=='qianwen-web']
        if successes:state['last_success']=max(successes)
    state['window_open']=bool(login_process and login_process.poll() is None)
    if login_process and login_process.poll() not in (None,0):state['error']='登录窗口未能正常打开，请运行配置千问登录.command检查浏览器环境。'
    return state


def open_login():
    global login_process
    with mutex:
        if login_process and login_process.poll() is None:return {'ok':True,'message':'登录窗口已经打开。'}
        lock=WORK/'qianwen-browser.lock'
        import fcntl
        with lock.open('a') as handle:
            try:fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError:raise ValueError('千问浏览器正在处理任务，请稍后再登录。')
        with (WORK/'qianwen-login.log').open('ab') as log:
            login_process=subprocess.Popen([str(ROOT/'.venv/bin/python'),str(ROOT/'qianwen_browser.py'),'login-ui'],
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
        meta = json.loads((folder / 'job.json').read_text()) if (folder / 'job.json').exists() else {}
        if meta.get('state') == 'completed' and Path(meta.get('document', '/nonexistent')).is_file():
            return ident
        import fcntl
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
        if self.path == '/health':
            return self.reply(200, {'ok': True, 'project': str(ROOT), 'pid': os.getpid(), 'engines': ['qianwen'], 'task_controls': True, 'local_upload': True, 'cloud_delete': True})
        if self.path == '/qianwen/status':
            return self.reply(200, login_status())
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
                    result=delete_task(ident)
                except (ValueError,OSError,subprocess.SubprocessError) as error:
                    folder=WORK/'jobs'/ident
                    meta=json.loads((folder/'job.json').read_text()) if (folder/'job.json').exists() else {}
                    cloud_status=meta.get('qianwen_delete_result','deleted' if meta.get('qianwen_cloud_deleted') else 'failed')
                    report=deletion_report(False,cloud_status,str(error))
                    if folder.exists():save_json(folder/'delete-result.json',report)
                    return self.reply(400,{'error':str(error),'deletion_result':report})
                return self.reply(200,result)
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
    print(f'网页视频转语音识别文字稿（由千问提供支持）：http://{HOST}:{PORT}', flush=True)
    server.serve_forever()

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

### FILE: index.html
```text
<!doctype html>
<html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>网页视频转语音识别文字稿（由千问提供支持）</title>
<style>
body{font:16px/1.7 -apple-system,BlinkMacSystemFont,sans-serif;color:#24322d;background:#f4f6f3;max-width:920px;margin:48px auto;padding:0 24px}h1{font-size:32px}h1 button{font-size:14px;padding:6px 10px;font-weight:normal;vertical-align:middle;white-space:nowrap}input,button,.action{font:inherit;padding:10px 14px;border:1px solid #c6d1ca;border-radius:8px}input[type=url]{flex:1;min-width:180px}button,.action{background:#245441;color:white;cursor:pointer;text-decoration:none;display:inline-block}form,.actions{display:flex;gap:12px;flex-wrap:wrap}article{background:white;padding:24px;border:1px solid #e0e7e1;border-radius:12px;margin:20px 0}small{color:#62736b}a{color:#245441}#message{color:#8b4520;white-space:pre-line}#message.success{color:#176538;background:#eaf7ee;padding:12px;border-radius:8px}#message.failure{color:#a52222;background:#fff0f0;padding:12px;border-radius:8px}.delete-result{font-weight:bold;white-space:pre-wrap}.notice{background:#fff3cd;color:#9c0006;padding:14px 18px;border-left:4px solid #b07800;font-weight:bold}.secondary{background:white;color:#245441}
#url::placeholder{color:#757575;opacity:1}#upload-zone{background:#fff;color:#757575;font:inherit;text-align:center;border:1px dashed #c6d1ca;border-radius:8px;padding:12px 14px;cursor:pointer;flex-basis:100%;box-sizing:border-box}#file-name{display:block;font-size:14px;color:#000}#form input[type=url]{order:0}#form button{order:1}#upload-zone{order:2}#qianwen-login{background:#004B93;border-color:#004B93}#qianwen-login:hover{background:#003B75}#form button{background:#D65A00;border-color:#D65A00}#form button:hover{background:#B94D00}</style>
<h1>网页视频转语音识别文字稿（由千问提供支持） <button type="button" id="qianwen-login">登录或打开千问</button></h1>
<p>粘贴网页链接，后台下载并默认交给千问识别语音、区分发言人，生成带时间戳、以视频标题命名的 Word。</p>
<form id="form" autocomplete="off"><input id="url" autocomplete="off" aria-label="音视频网页链接" type="url" placeholder="粘贴YouTube、B站、小宇宙等音视频网页链接"><label id="upload-zone" tabindex="0">点击或将音视频文件拖拽到此处上传<input id="media-file" type="file" accept="audio/*,video/*,.mkv,.flac,.opus" hidden><span id="file-name"></span></label><button>开始生成文稿</button></form>
<p class="actions"><span id="login-status" role="status">正在读取登录千问状态…</span></p><p id="message" role="status"></p>
<p class="notice">本文稿内容为语音模型识别结果，需要注意：可能有错别字和识别不准确之处。</p>
<p><small>Word 保存到“下载/网页视频转语音识别文字稿（由千问提供支持）”。音频将上传千问服务器；需要登录时点击上方“登录或打开千问”。完成后直接查看或打开所在位置。Word 完整性检查通过后自动将原音视频移入废纸篓并清理临时音轨。</small></p>
<div id="jobs"></div>
<script>

const historicalTaskTimes={};
const stages={queued:'排队中',downloading:'正在下载',downloaded:'下载完成',diarizing:'正在准备千问识别',transcribing:'正在准备千问识别',cloud_preparing:'正在准备上传音频',cloud_transcribing:'等待千问处理结果或加载文稿页面',extracting_audio:'正在提取音频',cloud_connecting:'正在连接千问并检查登录',cloud_uploading:'正在向千问上传音频',cloud_confirming_upload:'等待千问页面确认上传记录（尚未确认成功）',retry_waiting:'页面加载超时，稍后自动重试',generating_document:'正在生成并检查 Word 文稿',cleaning:'Word 已生成，正在清理原音视频和临时文件',cloud_exporting:'正在导出千问原文 Word',completed:'Word 已生成，可以查看',login_required:'需要重新登录千问',failed:'处理失败，进度已保留'};
const msg=document.querySelector('#message');
let deleteNoticeTimer;
function renderDeletionResult(target,result){target.replaceChildren();let heading=document.createElement('div');heading.textContent=result.status==='success'?'删除成功':result.status==='pending'?'正在同步删除…':'删除失败';heading.style.color=result.status==='success'?'#176538':'#a52222';target.append(heading);if(result.elements){for(let element of result.elements){let row=document.createElement('div');row.textContent=element.label+'：'+element.detail;row.style.color=(element.status==='success'||(!element.status&&/^(删除成功|无需删除|未找到对应千问记录)/.test(element.detail)))?'#176538':'#a52222';target.append(row)}}else{let row=document.createElement('div');row.textContent=result.message;row.style.color=result.status==='success'?'#176538':'#a52222';target.append(row)}}
function showDeletionResult(result,success){clearTimeout(deleteNoticeTimer);msg.className=success?'success':'failure';renderDeletionResult(msg,result);let displayed=msg.textContent;if(success){deleteNoticeTimer=setTimeout(()=>{if(msg.className==='success'&&msg.textContent===displayed){msg.replaceChildren();msg.className=''}},3000)}}
const deletedTaskIds=new Set();const deletionResults=new Map();let refreshSequence=0;
async function requireControls(){let h=await(await fetch('/health')).json();if(!h.task_controls)throw Error('请双击“加载本次更新.command”，让网页服务加载登录和删除功能。')}
document.querySelector('#qianwen-login').onclick=async()=>{try{await requireControls();let r=await post('/qianwen/login',{});msg.textContent=r.message}catch(e){msg.textContent=e.message}};
async function refreshLogin(){try{let h=await(await fetch('/health')).json();if(!h.task_controls){document.querySelector('#login-status').textContent='新功能需要加载本次更新';return}let s=await(await fetch('/qianwen/status')).json();let text=s.window_open?'请在千问窗口中完成登录，完成后关闭窗口':s.status==='required'?'千问需要重新登录，请点击标题旁的“登录或打开千问”按钮':s.last_success?'最近成功转写：'+new Date(s.last_success*1000).toLocaleString()+'；任务中会继续验证登录':'登录状态待验证；首次使用请点击“登录或打开千问”';document.querySelector('#login-status').textContent=s.error||text}catch(e){document.querySelector('#login-status').textContent='暂时无法读取登录状态'}}
async function post(url,data){let r=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});let j=await r.json();if(!r.ok){let error=Error(j.error);error.deletionResult=j.deletion_result;throw error}return j}
let selectedFile=null;
const zone=document.querySelector('#upload-zone'),picker=document.querySelector('#media-file'),urlInput=document.querySelector('#url');
function selectFile(file){if(!file)return;selectedFile=file;urlInput.value='';document.querySelector('#file-name').textContent=file.name}
picker.onchange=()=>selectFile(picker.files[0]);
zone.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();picker.click()}};
zone.ondragover=e=>{e.preventDefault()};zone.ondrop=e=>{e.preventDefault();if(e.dataTransfer.files.length!==1){msg.textContent='每次请选择一个音视频文件';return}selectFile(e.dataTransfer.files[0])};
urlInput.oninput=()=>{if(urlInput.value){selectedFile=null;picker.value='';document.querySelector('#file-name').textContent=''}};
document.querySelector('#form').onsubmit=async e=>{e.preventDefault();try{if('qianwen'==='qianwen'){let health=await(await fetch('/health')).json();if(!health.engines?.includes('qianwen'))throw Error('网页服务需要加载新版。请完成登录千问配置后再试。')}if(selectedFile){let h=await(await fetch('/health')).json();if(!h.local_upload)throw Error('请双击“加载本次更新.command”启用本地文件入口。');let button=document.querySelector('#form button');button.disabled=true;msg.textContent='正在将文件交给本机后台，请稍候…';try{let r=await fetch('/upload',{method:'POST',headers:{'Content-Type':'application/octet-stream','X-File-Name':encodeURIComponent(selectedFile.name)},body:selectedFile});let j=await r.json();if(!r.ok)throw Error(j.error)}finally{button.disabled=false}}else{if(!urlInput.value.trim())throw Error('请粘贴链接或选择音视频文件');await post('/jobs',{url:urlInput.value,engine:'qianwen'})}deletedTaskIds.clear();selectedFile=null;picker.value='';document.querySelector('#file-name').textContent='';document.querySelector('#url').value='';msg.textContent='已加入后台队列。你可以继续做其他事情，稍后回来查看文稿。';await refresh()}catch(e){msg.textContent=e.message}};
function taskHeading(j){let title=j.title;if(j.state==='queued')return '待处理 · '+(title||'正在获取标题（'+new URL(j.url).hostname+' / '+(new URL(j.url).searchParams.get('v')||new URL(j.url).pathname.split('/').filter(Boolean).pop()||j.id)+'）');return title||'正在获取标题 · '+j.id}
function link(text,url,style){let a=document.createElement('a');a.textContent=text;a.href=url;if(style)a.className=style;return a}
async function refresh(){const sequence=++refreshSequence;try{let jobs=await(await fetch('/jobs')).json();if(sequence!==refreshSequence)return;jobs=jobs.filter(j=>!deletedTaskIds.has(j.id));jobs.sort((a,b)=>(b.created_at??historicalTaskTimes[b.id]??b.added_at??Infinity)-(a.created_at??historicalTaskTimes[a.id]??a.added_at??Infinity));let host=document.querySelector('#jobs');host.replaceChildren();for(let j of jobs){let card=document.createElement('article');card.dataset.taskId=j.id;let h=document.createElement('h2');h.textContent=taskHeading(j);card.append(h);let p=document.createElement('p');p.textContent=(j.document&&!j.has_document)?'Word 文件已不在原保存位置，重新提交链接可生成':(stages[j.state]||'状态暂未识别：'+String(j.state));card.append(p);if(j.source_kind==='local'){let source=document.createElement('p');source.textContent=j.source_label;card.append(source)}else card.append(link('原网页',j.url));let deletion=deletionResults.get(j.id)||j.deletion_result;if(deletion){let status=document.createElement('p');status.className='delete-result';status.setAttribute('role','alert');status.style.color=deletion.status==='failed'?'#a52222':'#8b4520';renderDeletionResult(status,deletion);card.append(status)}if(j.error){let err=document.createElement('p');err.textContent=j.error;card.append(err)}if(j.cleanup_error){let note=document.createElement('p');note.textContent='Word 已生成，但部分临时文件未清理：'+j.cleanup_error;card.append(note)}if(j.has_document){let actions=document.createElement('p');actions.className='actions';actions.append(link('查看 Word 文稿','/preview/'+j.id,'action'));let reveal=document.createElement('button');reveal.type='button';reveal.className='secondary';reveal.textContent='打开文档所在位置';let revealStatus=document.createElement('small');revealStatus.setAttribute('role','status');reveal.onclick=async()=>{reveal.disabled=true;revealStatus.textContent='正在打开文件夹…';try{await post('/reveal/'+j.id,{});revealStatus.textContent='已打开 Finder 文件夹。';msg.textContent='已打开文档所在的 Finder 文件夹。'}catch(e){revealStatus.textContent='打开失败：'+e.message;msg.textContent='打开失败：'+e.message}finally{reveal.disabled=false}};actions.append(reveal);actions.append(revealStatus);card.append(actions);let note=document.createElement('small');note.textContent=j.temporary_files_removed?(j.media_trashed?'原音视频已移入废纸篓，临时音轨已清理。':'原音视频与临时音轨已清理。'):'Word 内容未经人工校对。';card.append(note)}let controls=document.createElement('p');controls.className='actions';if(j.state==='failed'||j.state==='login_required'){let retry=document.createElement('button');retry.textContent='重试任务';retry.onclick=async()=>{try{await post('/jobs',{url:j.url,engine:'qianwen'});await refresh()}catch(e){msg.textContent=e.message}};controls.append(retry)}let remove=document.createElement('button');remove.type='button';remove.className='secondary';remove.style.color='#a52222';remove.textContent='删除任务并同步到千问';if(deletion?.status==='pending'){remove.disabled=true;remove.textContent='正在同步删除…'}remove.onclick=async()=>{if(!confirm('删除“'+(j.title||j.id)+'”？将停止该任务，把本机任务文件和相关文稿移入废纸篓。同时删除对应的千问云端记录，云端删除后无法恢复。'))return;deletionResults.set(j.id,{status:'pending',message:'正在删除并同步到千问，请稍候…'});msg.className='';msg.textContent='正在删除并同步到千问，请稍候…';remove.disabled=true;remove.textContent='正在同步删除…';try{let health=await(await fetch('/health')).json();if(!health.cloud_delete)throw Error('请先双击加载本次更新.command启用千问同步删除');await requireControls();let r=await post('/delete/'+j.id,{});deletedTaskIds.add(j.id);++refreshSequence;document.querySelectorAll('article[data-task-id="'+j.id+'"]').forEach(node=>node.remove());deletionResults.delete(j.id);showDeletionResult(r.deletion_result||{status:'success',message:r.message},true);await refresh()}catch(e){let message=e.deletionResult?.message||('删除失败\n工具任务列表记录：未删除成功\n本机文稿及任务文件：未确认删除成功\n对应的千问记录：未确认删除成功\n原因：'+e.message);let report=e.deletionResult||{status:'failed',message};deletionResults.set(j.id,report);showDeletionResult(report,false);let status=card.querySelector('.delete-result');if(!status){status=document.createElement('p');status.className='delete-result';status.setAttribute('role','alert');card.append(status)}status.style.color='#a52222';renderDeletionResult(status,report);remove.disabled=false;remove.textContent='删除任务并同步到千问'}};if(j.has_document){card.querySelector('.actions').append(remove)}else{controls.append(remove)}if(controls.children.length)card.append(controls);host.append(card)}await refreshLogin()}catch(e){msg.textContent='后台连接中断，请重新启动工具。'}}
refresh();setInterval(refresh,6000);
</script></html>

```

### FILE: install.py
```text
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
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(ROOT / "work/browser-bin")
subprocess.run([python, "-m", "pip", "install", "--upgrade", "pip"], check=True)
subprocess.run([python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
subprocess.run([python, "-m", "pip", "check"], check=True)
subprocess.run([python, "-m", "unittest", "test_reader", "test_app", "-q"], check=True)
print("正在安装千问后台浏览器，可以等待，不要关闭窗口。", flush=True)
subprocess.run([python, "-m", "playwright", "install", "chromium"], check=True)
print("安装完成。请双击：启动工具.command。", flush=True)

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


def auth_state(status):
    from reader import save_json
    path=ROOT/'work/qianwen-auth.json'
    previous=__import__('json').loads(path.read_text()) if path.exists() else {}
    previous.update(status=status,checked_at=time.time())
    if status=='valid':previous['last_success']=time.time()
    save_json(path,previous)


def require_login_if_visible(page):
    prompts=page.get_by_role('dialog').filter(has_text=re.compile('登录|验证码|手机号'))
    for prompt in prompts.all():
        if prompt.is_visible():
            auth_state('required')
            raise LoginRequired('千问需要重新登录或完成验证。请点击页面上的“登录千问”，完成后重试任务。')
    buttons=[button for name in ('登录','登录/注册','立即登录')
             for button in page.get_by_role('button',name=name,exact=True).all()]
    if any(button.is_visible() for button in buttons):
        auth_state('required')
        raise LoginRequired('千问登录已失效，请点击“登录千问”重新登录后重试。')


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


@contextmanager
def browser_context(playwright, headed=False):
    import fcntl
    PROFILE.mkdir(parents=True, exist_ok=True)
    with (ROOT/'work/qianwen-browser.lock').open('a') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise RuntimeError('千问浏览器正在使用中，请关闭登录窗口或等待任务完成后再试。')
        context=playwright.chromium.launch_persistent_context(str(PROFILE), headless=not headed,
                     accept_downloads=True,viewport={'width':1920,'height':1600})
        try:yield context
        finally:
            try:context.close()
            except Exception:pass


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
        (job/'browser-diagnostic.txt').write_text(page.locator('body').inner_text())
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
            (job/'browser-diagnostic.txt').write_text(body)
            events=job/'upload-events.txt'
            previous=events.read_text() if events.exists() else ''
            if not previous.endswith(body+'\n'):
                events.write_text((previous+'\n'+str(time.time())+'\n'+body+'\n')[-64000:])
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
            (job/'browser-diagnostic.txt').write_text(page.locator('body').inner_text())
            require_login_if_visible(page)
            if not meta.get('qianwen_url'):
                try:
                    page.get_by_text('中英文自由说', exact=True).wait_for(timeout=30000)
                except Exception as error:
                    raise RuntimeError('千问需要登录或页面无法访问。请运行“配置千问登录.command”。') from error
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
                    (job/'upload-selected.txt').write_text(page.locator('body').inner_text())
                    from playwright.sync_api import expect
                    expect(page.get_by_role('button',name='确 认',exact=True)).to_be_enabled(timeout=120000)
                    meta['qianwen_upload_title']=upload.stem
                    meta['qianwen_submission_attempted']=True;save(job/'job.json',meta)
                    page.get_by_role('button', name='确 认', exact=True).click()
                    page.screenshot(path=str(job/'upload-confirmed.png'),full_page=True)
                    (job/'upload-confirmed.txt').write_text(page.locator('body').inner_text())
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
                        (job/'browser-diagnostic.txt').write_text(page.locator('body').inner_text())
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
            (job/'browser-diagnostic.txt').write_text(page.locator('body').inner_text())
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
            download.value.save_as(str(destination))
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
    meta=json.loads((job/'job.json').read_text())
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
                    try:page.wait_for_timeout(500)
                    except Exception:break
                auth_state('unknown')
            else:
                input('请在专用浏览器中登录千问，确认音视频速读页面可用后，在此按回车保存登录。')
    print('登录环境已保存在本机。后台任务不会打开此浏览器窗口。')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('command', choices=['login','login-ui','delete'])
    parser.add_argument('--job')
    args=parser.parse_args()
    if args.command=='delete':
        if not args.job or not re.fullmatch('[0-9a-f]{12}',args.job):parser.error('任务编号不合法')
        delete_cloud(ROOT/'work/jobs'/args.job)
    else:login(ui=args.command=='login-ui')

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
            node = Path(__import__('shutil').which('node') or '/nonexistent')
            if node.exists():
                options['js_runtimes'] = {'node': {'path': str(node)}}
            if args.cookies_browser:
                options['cookiesfrombrowser'] = (args.cookies_browser,)
            if meta.get('source_kind') == 'local' and (not meta.get('media') or not Path(meta['media']).is_file()):
                raise ValueError('本地上传文件已不存在，请重新上传')
            if not meta.get('media') or not Path(meta['media']).exists():
                media_folder.mkdir(parents=True, exist_ok=True)
                with YoutubeDL(options) as downloader:
                    info = downloader.extract_info(download_url(args.url), download=True)
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
            raw = json.loads(raw_path.read_text()) if raw_path.exists() else {}
            if raw.get('model') != 'qianwen-web':
                from qianwen_browser import export_with_retry
                raw = export_with_retry(wav, job, meta, save_json)
                save_json(raw_path, raw)
            meta['state']='generating_document';save_json(job/'job.json',meta)
            build_document(job, raw)
            print(f'Word 已生成：{job}', flush=True)
        except Exception as error:
            from qianwen_browser import LoginRequired
            message=str(error)
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
                 '网页校对结果.json', 'submitted-result.json', 'result.json', 'speaker-turns.json',
                 'qianwen-original.docx', 'browser-diagnostic.png', 'browser-diagnostic.txt', 'upload-selected.png', 'upload-selected.txt', 'upload-confirmed.png', 'upload-confirmed.txt', 'upload-events.txt', 'upload-recovery.png', 'upload-recovery.txt',
                 'browser-elements.json', 'browser-rows.json', 'browser-structure.json'):
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
    result=subprocess.run(['/usr/sbin/lsof','-t',str(folder/'.prepare.lock')],capture_output=True,text=True)
    verified=[]
    for value in result.stdout.split():
        pid=int(value)
        command=subprocess.run(['/bin/ps','-p',str(pid),'-o','command='],capture_output=True,text=True)
        args=shlex.split(command.stdout.strip())
        if len(args)>=3 and args[1]==str(root/'reader.py') and args[2]=='prepare':verified.append(pid)
    return verified


def stop_reader(pid):
    children=subprocess.run(['/usr/bin/pgrep','-P',str(pid)],capture_output=True,text=True)
    for child in children.stdout.split():stop_reader(int(child))
    try:os.kill(pid,signal.SIGTERM)
    except ProcessLookupError:pass


def trash_task(root, work, output_roots, ident):
    from send2trash import send2trash
    from docx import Document
    import fcntl
    if not re.fullmatch('[0-9a-f]{12}',ident):raise ValueError('任务编号不合法')
    folder=work/'jobs'/ident
    if folder.is_symlink() or not folder.exists():raise ValueError('任务不存在')
    meta=json.loads((folder/'job.json').read_text())
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
        meta=json.loads((folder/'job.json').read_text())
        candidates=set()
        owned=set()
        reservation=folder/'export-target.json'
        if reservation.exists():
            record=json.loads(reservation.read_text())
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
        send2trash(str(folder.resolve()))
    return {'ok':True,'message':'本机任务与相关文件已移入废纸篓。千问云端记录需在千问网页中管理。'}

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

    def test_restart_recovers_only_unfinished_in_original_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for ident, state, created in [('000000000001','queued',3), ('000000000002','transcribing',1),
                                           ('000000000003','completed',2), ('000000000004','failed',4)]:
                folder = root / 'jobs' / ident
                folder.mkdir(parents=True)
                (folder/'job.json').write_text(json.dumps({'state':state,'created_at':created,'url':'https://example.com/'+ident}))
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
                (folder/'job.json').write_text(json.dumps({'url':'https://example.com/'+ident,'state':'queued','engine':'qianwen'}))
            fakequeue=MagicMock()
            fakequeue.get.side_effect=[(ident,'https://example.com/'+ident,ident) for ident in identifiers]+[StopIteration()]
            process=MagicMock();process.wait.return_value=0
            with patch.object(app,'WORK',work),patch.object(app,'tasks',fakequeue),patch.object(app,'pending',set(identifiers)),patch.object(app,'generations',{}),patch.object(app,'cancelled',set()),patch.object(app,'active_readers',{}),patch('app.subprocess.Popen',side_effect=[OSError('launch failed'),process]) as run:
                with self.assertRaises(StopIteration):app.worker()
            first=json.loads((work/'jobs'/identifiers[0]/'job.json').read_text())
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
                meta=json.loads(next((Path(tmp)/'jobs').glob('*/job.json')).read_text())
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
            (folder/'job.json').write_text(json.dumps({'state':'completed','created_at':1}))
            (folder/'delete-result.json').write_text(json.dumps({'status':'failed','message':'删除失败：登录失效'}))
            with patch.object(app,'WORK',work):
                self.assertEqual(app.list_jobs()[0]['deletion_result']['message'],'删除失败：登录失效')

    def test_successful_delete_removes_task_from_list(self):
        import shutil
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory() as tmp:
            work=Path(tmp);folder=work/'jobs/123456abcdef';folder.mkdir(parents=True)
            (folder/'job.json').write_text(json.dumps({'state':'completed','created_at':1}))
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
            (folder/'job.json').write_text(json.dumps({'state':'completed','document':str(doc)}))
            with patch.object(app,'WORK',work),patch('task_controls.reader_pids',return_value=[]),patch('task_controls.trash_task') as trash,patch('app.subprocess.run',return_value=SimpleNamespace(returncode=1,stderr='登录失效')):
                with self.assertRaisesRegex(ValueError,'登录失效'):app.delete_task('123456abcdef')
                trash.assert_not_called()
            self.assertTrue(doc.exists());self.assertTrue((folder/'job.json').exists())
            self.assertFalse((folder/'.deleting').exists())

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

    def test_local_upload_pipeline_preserves_user_original(self):
        import io, app, shutil
        original=Path(self.temp.name)/'我的录音.wav'
        with wave.open(str(original),'wb') as a:
            a.setnchannels(1);a.setsampwidth(2);a.setframerate(16000);a.writeframes(b'\0'*32000)
        with patch.object(app,'WORK',self.work),patch.object(app,'enqueue',side_effect=lambda url: __import__('hashlib').sha256(url.encode()).hexdigest()[:12]):
            ident=app.receive_upload(io.BytesIO(original.read_bytes()),original.stat().st_size,original.name)
        job=self.work/'jobs'/ident;meta=json.loads((job/'job.json').read_text())
        raw={'model':'qianwen-web','segments':[{'start':0,'end':1,'speaker':'发言人 1','text':'本地文件全部原文'}]}
        with patch('qianwen_browser.export_audio',return_value=raw),patch.object(reader,'ffmpeg',return_value='/unused'),patch.object(reader,'extract_audio',side_effect=lambda ff,src,dst:shutil.copy2(src,dst)):
            reader.prepare(argparse.Namespace(url=meta['url'],cookies_browser=None,engine='qianwen'))
        saved=json.loads((job/'job.json').read_text());texts=[p.text for p in Document(saved['document']).paragraphs]
        self.assertEqual(saved['state'],'completed')
        self.assertEqual(texts[0],'本地上传文件：我的录音.wav')
        self.assertEqual(Path(saved['document']).name,'我的录音.docx')
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
        meta = json.loads((job / 'job.json').read_text())
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
        (folder/'job.json').write_text(json.dumps(meta))
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
            (folder/'export-target.json').write_text(json.dumps({'url':'https://example.com/test','path':str(path)}))
            trash=self.run_delete(root,output)
            self.assertFalse(folder.exists());self.assertFalse(path.exists());self.assertFalse(partial.exists())
            self.assertTrue((trash/'123456abcdef/media/video.mp4').exists())
            self.assertTrue((trash/'测试.docx').exists());self.assertTrue((trash/'测试.partial.docx').exists())

    def test_preserves_unrelated_document_with_same_title(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);folder,output,path=self.setup_files(root)
            meta=json.loads((folder/'job.json').read_text());meta.pop('document');(folder/'job.json').write_text(json.dumps(meta))
            doc=Document();doc.add_paragraph('https://other.example/video');doc.save(path)
            self.run_delete(root,output);self.assertTrue(path.exists())

    def test_rejects_document_outside_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);folder,output,path=self.setup_files(root)
            outside=root/'private.docx';shutil.copy2(path,outside)
            meta=json.loads((folder/'job.json').read_text());meta['document']=str(outside);(folder/'job.json').write_text(json.dumps(meta))
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

### FILE: 启用自动启动.command
```text
#!/bin/zsh
cd "${0:A:h}" || exit 1
.venv/bin/python launch_service.py install --port 8767
result=$?
read 'reply?按回车关闭窗口。'
exit $result

```

### FILE: 文件校验.json
```text
{
  "test_reader.py": "dcbf181640b381f6d7ab81497b5fc8779ea88ae203dfb4181eb00861aaf044f5",
  "qianwen_browser.py": "4042b5e64acb95f87c8be2de002b46d52bc172a5b833877e23d397e06fd296f7",
  "测试千问后台流程.command": "365ea7c455b38238341c79e3f2db6531de8053c34a909c4a210a19248a680c8c",
  "smoke_qianwen.py": "5a41ae58b74a8f2edaaadeb36c60235646989c5bdb2aa49e17d72dfd8778f71e",
  "index.html": "a5ae1e8ce64032d6ee744fa81e4649a13041f0f281b911cf52db48cbb0c38add",
  "停用自动启动.command": "0c2353cd41fd56b737864d09d6fe83f8b7d62cc1c51757e86fe0bc6bbd76b682",
  "launch_service.py": "2cadb70ee153b678af24a6eb9e911d7e6e2ae4906ca8d3115ff8bb723d516dba",
  "requirements.txt": "8f1f858b32310780d785ef1d196205c8c85a0c44efbb9fe4124bf7e98c9a96d3",
  "启动工具.command": "f67940511e7be84f96ef4eadc60dee14b08668d185f06f94cd03a02ebd3d59ca",
  "首次安装.command": "3386934c6c62f0983f9d9ee8541bf0d73a4fa671be319201efa649bf71c28d32",
  "task_controls.py": "a420be2ff8a6b4fc833d126f235e8a249c521e2a8c30435b36ebdf7426579084",
  "test_task_controls.py": "2a0d1da5b7de5a52a5d3c0257dd989341bccf00ba3cda5fd57fe98db25842644",
  "reader.py": "1b32092e273dcf8847b30c1ab80fc5597d12ff5ca5c69e35172c9cdbe7be406f",
  "切换千问并清理本地模型.command": "39ae5c718d5854f9fec85e13cd2c6fc683cb3c07844dffdd29697f97cfeeaaf4",
  "smoke_qianwen_runner.py": "10c6047ad2b7ae20cac3945b41f8afdc047975fd2da3ef0dc576f3753a512409",
  "cloud_migration.py": "cc5c02b953f404a280f0230e836ff9a5fe04f3e7002361ef9b8b8cdc244c07a0",
  "自动恢复测试.command": "e5f7e855d99cd648d6ae2e1382da651e8afb7597f184e08d1661d6daef5cc7f6",
  "app.py": "42334fb8c21c2b74196f6377bd67516af9c5bb5b1a8541128d8592b3882f4391",
  "加载本次更新.command": "ceabb97ebf2b3d7df5568844de02733bc9e09f9c877621985bdaf801a182b978",
  "配置千问登录.command": "3bc9b14516ab4c169b0cd7a9c595778965167f7f7ce533eab5ad7b3abd835fac",
  "install.py": "837ca16dea4cc1b6c258f5effb2eea8953577857a00a4b9b927624aff8a146e8",
  "test_qianwen.py": "47ba77b258ba4fb918fdc390419931c05fa9da14a7483cdad91f83e812ffdcda",
  "check_recovery.py": "7fb929eabc113b13551764fe57caa4f72e7f37f6cded04a75c590fe54e1a3d2d",
  "启用自动启动.command": "3475ec88b5c035f49adc0a13b3a14a09255ca19aa600a750051f6a8f1d8a07b6",
  "test_app.py": "e850e10b4e8414ef683b73076e73d10e39b5837125edfd82f97af9a8cbb781ab"
}

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

