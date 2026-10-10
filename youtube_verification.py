"""Human login in normal installed Chrome, with a dedicated private profile."""
import os,time,subprocess,sys
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

def verify(url,job,meta,save,timeout=900):
    # A separate profile: never launches or reads the user's everyday Chrome profile.
    profile=job/'youtube-manual-chrome'
    profile.mkdir(parents=True,exist_ok=True)
    meta.update(state='youtube_verifying',error='请在弹出的Chrome专用窗口完成YouTube登录或验证，然后关闭该专用窗口；工具自动重试下载。')
    save(job/'job.json',meta)
    process=subprocess.Popen([str(chrome_path()),'--user-data-dir='+str(profile.resolve()),'--no-first-run','--no-default-browser-check','--disable-background-mode','--new-window',url],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired as error:
        raise RuntimeError('YouTube验证窗口仍未关闭；请完成登录并关闭专用窗口后重试。') from error
    if not (profile/'Default'/'Network'/'Cookies').is_file() and not (profile/'Default'/'Cookies').is_file():
        raise RuntimeError('Chrome未保存验证会话，请在专用窗口完成登录后再重试')
    return profile
