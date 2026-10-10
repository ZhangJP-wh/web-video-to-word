#!/bin/zsh
cd -- "${0:A:h}" || exit 1
.venv/bin/python - <<'PY'
import os, plistlib, subprocess
from pathlib import Path
from launch_service import LABEL
root=Path.cwd()
path=Path.home()/'Library/LaunchAgents'/(LABEL+'.plist')
if not path.exists():
    raise SystemExit('尚未启用自动启动。请先关闭手动网页服务，再运行启动工具.command。')
config=plistlib.loads(path.read_bytes())
if config.get('WorkingDirectory')!=str(root):
    raise SystemExit('自动启动项属于另一个项目副本，未停止服务。')
subprocess.run(['/bin/launchctl','kill','SIGTERM',f'gui/{os.getuid()}/{LABEL}'],check=True)
print('网页服务正在自动恢复。请稍后刷新工具页面。正在识别的任务会保留。')
PY
result=$?
read '?按回车关闭窗口。'
exit "$result"
