"""Human verification in an isolated visible browser; never reads everyday browser cookies."""
import os,time
from pathlib import Path
from http.cookiejar import MozillaCookieJar,Cookie

def needs_verification(message):
    return '[youtube]' in str(message) and 'Sign in to confirm' in str(message)

def verify(url,job,meta,save,timeout=900):
    from playwright.sync_api import sync_playwright
    os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH',str(Path(__file__).resolve().parent/'work/browser-bin'))
    cookiefile=job/'youtube-session.cookies'
    meta.update(state='youtube_verifying',error='请在弹出的YouTube专用窗口登录或完成人机验证，完成后关闭该窗口；工具将自动重试下载。')
    save(job/'job.json',meta)
    try:
        with sync_playwright() as p:
            context=p.chromium.launch_persistent_context(str(job/'youtube-browser-profile'),headless=False)
            try:
                page=context.pages[0] if context.pages else context.new_page()
                page.goto(url,wait_until='domcontentloaded',timeout=60000)
                deadline=time.monotonic()+timeout
                jar=MozillaCookieJar(str(cookiefile))
                while context.pages:
                    if time.monotonic()>deadline:raise RuntimeError('YouTube人工验证等待超过15分钟，请重试后完成验证')
                    try:
                        for c in context.cookies():
                            if not any((c['domain'].lstrip('.')==d or c['domain'].lstrip('.').endswith('.'+d)) for d in ('youtube.com','google.com')):continue
                            expires=int(c['expires']) if c.get('expires',-1)>0 else None
                            jar.set_cookie(Cookie(0,c['name'],c['value'],None,False,c['domain'],True,c['domain'].startswith('.'),c['path'],True,c['secure'],expires,expires is None,None,None,{},False))
                        jar.save(ignore_discard=True,ignore_expires=True);cookiefile.chmod(0o600)
                        context.pages[-1].wait_for_timeout(1000)
                    except Exception:
                        if not context.pages:break
                        raise
                if not cookiefile.exists():raise RuntimeError('未获得YouTube验证会话，请重新打开验证窗口')
                return cookiefile
            finally:
                context.close()
    except Exception as error:
        raise RuntimeError('YouTube验证窗口未能完成：'+str(error)) from error
