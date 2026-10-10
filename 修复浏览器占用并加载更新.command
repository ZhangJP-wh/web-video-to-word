#!/bin/zsh
cd -- "${0:A:h}" || exit 1
.venv/bin/python - <<'PY'
import json,subprocess,time,os,plistlib
from pathlib import Path
from task_controls import reader_pids,stop_reader
from reader import save_json
from launch_service import LABEL
from browser_service import endpoint
root=Path.cwd();work=root/'work'
plist=Path.home()/'Library/LaunchAgents'/(LABEL+'.plist')
if not plist.exists() or plistlib.loads(plist.read_bytes()).get('WorkingDirectory')!=str(root):raise SystemExit('未找到属于当前项目的自动启动服务，未执行切换。')
if not endpoint():
    owners=set(subprocess.run(['lsof','-t',str(work/'qianwen-browser.lock')],capture_output=True,text=True).stdout.split())
    for record in (work/'jobs').glob('*/job.json'):
        verified=reader_pids(root,record.parent)
        if not owners.intersection(str(pid) for pid in verified):continue
        for pid in verified:stop_reader(pid)
        from runtime_compat import file_lock as f
        with (record.parent/'.prepare.lock').open('a') as lock:
            deadline=time.monotonic()+20
            while True:
                try:f.flock(lock,f.LOCK_EX|f.LOCK_NB);break
                except BlockingIOError:
                    if time.monotonic()>deadline:raise SystemExit('旧进程仍未退出，文件和任务已保留。')
                    time.sleep(.25)
            meta=json.loads(record.read_text());meta.update(state='queued');meta.pop('error',None);save_json(record,meta)
            print('已保留媒体和千问提交记录，切换任务：'+meta.get('title',record.parent.name))
for record in (work/'jobs').glob('*/job.json'):
    meta=json.loads(record.read_text())
    if meta.get('state')=='failed' and '千问浏览器正在使用中' in meta.get('error',''):
        meta.update(state='queued');meta.pop('error',None);save_json(record,meta)
subprocess.run(['/bin/launchctl','kill','SIGTERM',f'gui/{os.getuid()}/{LABEL}'],check=True)
print('切换完成。请刷新工具页面，并点击“显示任务状态”查看后台进展。')
PY
result=$?
read '?按回车关闭窗口。'
exit "$result"
