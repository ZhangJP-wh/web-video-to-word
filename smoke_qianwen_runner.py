"""A bounded local test runner; retry only on an explicit file request."""
import subprocess
import sys
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
request=ROOT/'work/qianwen-test-request.txt'
last=None
end=time.monotonic()+600
first=True
while time.monotonic()<end:
    current=request.read_text() if request.exists() else ''
    if first or current!=last:
        first=False;last=current
        subprocess.run([sys.executable,str(ROOT/'smoke_qianwen.py')])
        print('测试结果已保存。保留此窗口即可，接下来十分钟内可后台重试；按Ctrl+C结束。',flush=True)
    time.sleep(1)
