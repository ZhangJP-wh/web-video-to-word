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
            raise LoginRequired('千问需要重新登录或完成验证。请点击页面上的“千问登录”，完成后重试任务。')
    buttons=[button for name in ('登录','登录/注册','立即登录')
             for button in page.get_by_role('button',name=name,exact=True).all()]
    if any(button.is_visible() for button in buttons):
        auth_state('required')
        raise LoginRequired('千问登录已失效，请点击“千问登录”重新登录后重试。')


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
            page.get_by_text(title,exact=True).filter(visible=True).first.wait_for(timeout=10000)
            meta.update(qianwen_submitted=True,qianwen_upload_confirmed=True,state='cloud_transcribing')
            save(job/'job.json',meta)
            return
        except BrowserTimeout:
            page.screenshot(path=str(job/'browser-diagnostic.png'),full_page=True)
            (job/'browser-diagnostic.txt').write_text(page.locator('body').inner_text())
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
                    from playwright.sync_api import expect
                    expect(page.get_by_role('button',name='确 认',exact=True)).to_be_enabled(timeout=120000)
                    meta['qianwen_submission_attempted']=True;save(job/'job.json',meta)
                    page.get_by_role('button', name='确 认', exact=True).click()
                    require_login_if_visible(page)
                title = upload.stem
                confirm_submission(page,title,job,meta,save)
                deadline = time.monotonic() + 6 * 3600
                while time.monotonic() < deadline:
                    require_login_if_visible(page)
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
    parser = argparse.ArgumentParser(); parser.add_argument('command', choices=['login','login-ui'])
    args=parser.parse_args(); login(ui=args.command=='login-ui')
