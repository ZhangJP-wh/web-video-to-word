"""Controlled launchd recovery check. Run from the normal Mac user environment."""
import argparse
import json
import os
import plistlib
import subprocess
import time
import urllib.request
from pathlib import Path
from launch_service import LABEL
ROOT=Path(__file__).resolve().parent

def health(port):
    with urllib.request.urlopen(f'http://127.0.0.1:{port}/health',timeout=2) as response:
        data=json.load(response)
    if data.get('project')!=str(ROOT):raise ValueError('页面不属于当前项目，停止测试。')
    return data

def reader_pids():
    pids=set()
    for lock in (ROOT/'work/jobs').glob('*/.prepare.lock'):
        result=subprocess.run(['/usr/sbin/lsof','-t',str(lock)],capture_output=True,text=True)
        pids.update(int(value) for value in result.stdout.split())
    return pids

def run(port):
    report={'passed':False,'tested_at':time.time(),'port':port}
    try:
        path=Path.home()/'Library/LaunchAgents'/(LABEL+'.plist')
        config=plistlib.loads(path.read_bytes())
        if config.get('WorkingDirectory')!=str(ROOT) or not config.get('KeepAlive') or not config.get('AbandonProcessGroup'):
            raise ValueError('启动项不匹配或缺少自动恢复设置，未停止服务。')
        before=health(port);report['before_pid']=before['pid']
        readers=reader_pids()-{before['pid']}
        started=time.monotonic()
        result=subprocess.run(['/bin/launchctl','kill','SIGTERM',f'gui/{os.getuid()}/{LABEL}'],capture_output=True,text=True)
        if result.returncode:raise RuntimeError(result.stderr.strip())
        while time.monotonic()-started<45:
            try:
                after=health(port)
                if after['pid']!=before['pid']:
                    report.update(after_pid=after['pid'],recovery_seconds=round(time.monotonic()-started,2))
                    with urllib.request.urlopen(f'http://127.0.0.1:{port}/jobs') as response:
                        report['task_count']=len(json.load(response))
                    for pid in readers:
                        try:os.kill(pid,0)
                        except ProcessLookupError:raise RuntimeError('原识别进程已退出，需要检查是否正常完成。')
                    report.update(passed=True,preserved_reader_pids=sorted(readers));break
            except OSError:pass
            time.sleep(.5)
        if not report['passed']:raise RuntimeError('45 秒内未观察到网页服务恢复。')
    except (OSError,ValueError,RuntimeError) as error:report['error']=str(error)
    finally:
        (ROOT/'work').mkdir(exist_ok=True)
        (ROOT/'work/recovery-test.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not report['passed']:raise SystemExit('测试未通过或未能执行，请保留以上报错。')
    print('自动恢复实测通过，原识别进程保留。')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8767)
    run(parser.parse_args().port)
