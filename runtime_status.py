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
