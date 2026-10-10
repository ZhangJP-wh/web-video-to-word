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
    if path.parent in (OUTPUT.parent / '网页视频转语音识别文字稿（由千问提供支持）', OUTPUT.parent / '网页视频转语音文稿', OUTPUT.parent / '网页视频转语音识别文字稿') and migrated.is_file():
        path = migrated.resolve()
    if not any(root.resolve() in path.parents for root in (OUTPUT, LEGACY_OUTPUT, ROOT / 'outputs', OUTPUT.parent / '网页视频转语音识别文字稿（由千问提供支持）', OUTPUT.parent / '网页视频转语音文稿', OUTPUT.parent / '网页视频转语音识别文字稿')) or not path.is_file():
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
    # Classify orphaned work for explicit restart; keep live readers untouched.
    list_jobs()


def classify_interrupted(folder, item):
    if item.get('state') in ('completed','failed','login_required','interrupted') or (folder/'.deleting').exists():
        return item
    from runtime_compat import file_lock
    with mutex:
        if folder.name in pending:
            return item
        with (folder/'.prepare.lock').open('a') as lock:
            try:
                file_lock.flock(lock,file_lock.LOCK_EX | file_lock.LOCK_NB)
            except BlockingIOError:
                return item
            try:
                fresh=json.loads((folder/'job.json').read_text())
                if fresh.get('state') not in ('completed','failed','login_required','interrupted'):
                    fresh.update(state='interrupted',error='任务已中断，已保留处理进度。请点击“重新开始任务”。')
                    save_json(folder/'job.json',fresh)
                return fresh
            finally:
                file_lock.flock(lock,file_lock.LOCK_UN)

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
            item = classify_interrupted(path.parent,json.loads(path.read_text(encoding="utf-8")))
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
        result=trash_task(ROOT,WORK,[OUTPUT,OUTPUT.parent/'网页视频转语音识别文字稿（由千问提供支持）',LEGACY_OUTPUT,ROOT/'outputs',OUTPUT.parent/'网页视频转语音文稿'],ident)
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
            verification=re.fullmatch(r'/youtube/confirm/([0-9a-f]{12})',self.path)
            if verification:
                from youtube_verification import confirm
                return self.reply(200,confirm(WORK/'jobs'/verification.group(1)))
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
