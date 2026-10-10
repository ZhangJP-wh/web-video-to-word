"""Human login in normal installed Chrome, with a dedicated private profile."""
import os,time,subprocess,sys,json
from runtime_compat import file_lock
from pathlib import Path

def needs_verification(message):
    return '[youtube]' in str(message) and 'Sign in to confirm' in str(message)

def chrome_path():
    candidates=[Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'),Path.home()/'Applications/Google Chrome.app/Contents/MacOS/Google Chrome']
    if sys.platform=='win32':
        candidates=[Path(os.environ.get(k,''))/'Google/Chrome/Application/chrome.exe' for k in ('PROGRAMFILES','PROGRAMFILES(X86)','LOCALAPPDATA')]
    for path in candidates:
        if path.is_file():return path
    raise RuntimeError('未找到正式版Google Chrome，请安装后再重试YouTube验证')

REUSE_SECONDS = 600

def shared_root(job):
    return job.parent.parent / 'youtube-verification'

def saved_profile(job):
    profile = shared_root(job) / 'youtube-manual-chrome'
    return profile if any((profile / 'Default' / p).is_file() for p in ('Network/Cookies', 'Cookies')) else None

def recently_verified(root):
    try:
        age = time.time() - float((root / 'verified-at').read_text())
        return 0 <= age < REUSE_SECONDS
    except (OSError, ValueError):
        return False

def verify(url,job,meta,save,timeout=900):
    root = shared_root(job)
    root.mkdir(parents=True,exist_ok=True)
    profile = root / 'youtube-manual-chrome'
    marker = root / 'confirmed'
    meta.update(state='youtube_verifying',youtube_shared_verification=True,
        error='等待共享YouTube验证：只需在一个专用窗口完成登录或验证并关闭窗口，所有等待任务将继续。')
    save(job/'job.json',meta)
    deadline = time.monotonic()+timeout
    with (root / 'session.lock').open('a') as lock:
        while True:
            try:
                file_lock.flock(lock,file_lock.LOCK_EX | file_lock.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise RuntimeError('等待共享YouTube验证超时，请完成专用窗口验证后重试')
                time.sleep(.5)
        try:
            if recently_verified(root) and saved_profile(job):
                return profile
            profile.mkdir(parents=True,exist_ok=True)
            marker.unlink(missing_ok=True)
            process=subprocess.Popen([str(chrome_path()),'--user-data-dir='+str(profile.resolve()),'--no-first-run','--no-default-browser-check','--disable-background-mode','--new-window',url],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            while process.poll() is None and not marker.exists():
                if time.monotonic()>deadline:
                    raise RuntimeError('YouTube验证窗口仍未关闭；请完成登录并关闭专用窗口后手动确认。')
                time.sleep(.5)
            marker.unlink(missing_ok=True)
            if not saved_profile(job):
                raise RuntimeError('Chrome未保存验证会话，请在专用窗口完成登录后再重试')
            (root / 'verified-at').write_text(str(time.time()))
            return profile
        finally:
            file_lock.flock(lock,file_lock.LOCK_UN)

def confirm(job):
    import json
    record=job/'job.json'
    if not record.is_file():raise ValueError('任务不存在')
    meta=json.loads(record.read_text())
    if meta.get('state')!='youtube_verifying':raise ValueError('任务当前不在等待YouTube验证，请刷新页面')
    if meta.get('youtube_shared_verification'):
        root=shared_root(job);root.mkdir(parents=True,exist_ok=True)
        (root/'confirmed').touch()
    else:
        (job/'youtube-verification-confirmed').touch()
    return {'ok':True,'message':'已确认关闭验证窗口，正在继续原任务，请稍候。'}
