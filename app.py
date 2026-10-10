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
    migrated = OUTPUT / path.name
    if path.parent == OUTPUT.parent / '网页视频转语音文稿' and migrated.is_file():
        path = migrated.resolve()
    if not any(root.resolve() in path.parents for root in (OUTPUT, LEGACY_OUTPUT, ROOT / 'outputs', OUTPUT.parent / '网页视频转语音文稿')) or not path.is_file():
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
                                        'prepare', url, '--engine',
                                        json.loads((folder/'job.json').read_text()).get('engine', 'local')], stdout=log, stderr=log)
            if result.returncode == 0:
                (folder / 'run.log').unlink(missing_ok=True)
        finally:
            with mutex:
                pending.discard(ident)
            tasks.task_done()


def enqueue(url, engine="local"):
    if engine not in ("local", "qianwen"):
        raise ValueError("不支持的语音识别方式")
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
            meta.update(url=url, state='queued', engine=engine)
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
        if self.path == '/health':
            return self.reply(200, {'ok': True, 'project': str(ROOT), 'pid': os.getpid(), 'engines': ['local', 'qianwen']})
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
                return self.reply(200, {'id': enqueue(data['url'].strip(), data.get('engine', 'local'))})
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
    print(f'网页视频转语音识别文字稿：http://{HOST}:{PORT}', flush=True)
    server.serve_forever()
