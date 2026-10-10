"""Persistent pending deletions; busy browser is waiting, never a false failure."""
import json,re,threading,time
from pathlib import Path
from reader import save_json
from runtime_compat import file_lock as fcntl

def browser_busy(work):
    with (Path(work)/'qianwen-browser.lock').open('a') as handle:
        try:
            fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
            fcntl.flock(handle,fcntl.LOCK_UN)
            return False
        except BlockingIOError:return True

def waiting_report():
    elements=[{'label':label,'status':'pending','detail':detail} for label,detail in [
        ('工具任务列表记录','等待同步删除，暂时保留'),('本机文稿及任务文件','等待同步删除，文件已保留'),
        ('对应的千问记录','等待千问浏览器空闲，将自动重试；若登录窗口开着，请关闭该窗口')]]
    return {'status':'pending','message':'删除已加入后台队列，等待千问浏览器空闲后自动执行。','elements':elements,'at':time.time()}

class DeletionQueue:
    def __init__(self,work,delete,failed,on_submit=lambda ident:None):
        self.work=Path(work);self.folder=self.work/'deletion-queue';self.folder.mkdir(parents=True,exist_ok=True)
        self.delete=delete;self.failed=failed;self.on_submit=on_submit
        self.lock=threading.RLock();self.finished={};self.started=False
    def submit(self,ident):
        if not re.fullmatch('[0-9a-f]{12}',ident):raise ValueError('无效任务编号')
        with self.lock:
            job=self.work/'jobs'/ident
            if not (job/'job.json').exists():raise ValueError('任务已不存在，请刷新列表')
            record=self.folder/(ident+'.json')
            if record.exists():return json.loads(record.read_text())['report']
            self.on_submit(ident)
            (job/'.deleting').touch()
            report=waiting_report();save_json(record,{'id':ident,'created_at':time.time(),'report':report})
            save_json(job/'delete-result.json',report);self.finished.pop(ident,None)
            return report
    def has_pending(self):return any(self.folder.glob('*.json'))
    def results(self):
        with self.lock:
            now=time.time();self.finished={k:v for k,v in self.finished.items() if now-v['at']<600}
            result=dict(self.finished)
            for p in self.folder.glob('*.json'):
                try:result[p.stem]=json.loads(p.read_text())['report']
                except (OSError,ValueError):continue
            return result
    def run_once(self):
        for path in sorted(self.folder.glob('*.json'),key=lambda p:p.stat().st_mtime):
            try:
                record=json.loads(path.read_text());ident=record['id']
                if time.time()-record['created_at']>6*3600:raise ValueError('等待千问浏览器空闲超过6小时，请关闭登录窗口后重试删除')
                if browser_busy(self.work):return
                try:report=self.delete(ident)['deletion_result']
                except Exception as error:
                    if '千问浏览器正在使用中' in str(error):
                        (self.work/'jobs'/ident/'.deleting').touch();return
                    raise
            except Exception as error:
                report=self.failed(path.stem,str(error))
            with self.lock:
                self.finished[path.stem]=report;path.unlink(missing_ok=True)
    def start(self):
        with self.lock:
            if self.started:return
            self.started=True
        def loop():
            while True:
                try:self.run_once()
                except Exception:pass # Records persist for the next pass/restart.
                time.sleep(2)
        threading.Thread(target=loop,daemon=True).start()
