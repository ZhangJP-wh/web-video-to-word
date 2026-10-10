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
