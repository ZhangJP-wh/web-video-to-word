"""Manage a per-user launchd service; no administrator privileges required."""
import argparse
import json
import os
import plistlib
import signal
import subprocess
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LABEL = 'com.zhangjp.web-video-to-word'


def configuration(root, port):
    root = Path(root).resolve()
    return {'Label': LABEL, 'ProgramArguments': [str(root / '.venv/bin/python'), str(root / 'app.py')],
            'WorkingDirectory': str(root), 'RunAtLoad': True, 'KeepAlive': True,
            'ThrottleInterval': 10, 'AbandonProcessGroup': True,
            'EnvironmentVariables': {'VIDEO_READER_PORT': str(port),
                'PATH': '/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin',
                'PYTHONUNBUFFERED': '1'},
            'StandardOutPath': str(root / 'work/service.log'),
            'StandardErrorPath': str(root / 'work/service.log')}


def launchctl(*args, check=True):
    result = subprocess.run(['/bin/launchctl', *args], capture_output=True, text=True)
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or 'launchctl 操作失败')
    return result


def stop_standalone(port):
    """Only stop a listener whose executable arguments and cwd match this project."""
    result = subprocess.run(['/usr/sbin/lsof', '-t', f'-iTCP:{port}', '-sTCP:LISTEN'], capture_output=True, text=True)
    for pid in set(result.stdout.split()):
        cwd = subprocess.run(['/usr/sbin/lsof', '-a', '-p', pid, '-d', 'cwd', '-Fn'], capture_output=True, text=True).stdout
        try:
            command = subprocess.run(['/bin/ps', '-p', pid, '-o', 'command='], capture_output=True, text=True).stdout
            matching = str(ROOT / 'app.py') in command
        except OSError:
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/', timeout=2) as response:
                matching = response.read() == (ROOT / 'index.html').read_bytes()
        if 'n' + str(ROOT) + '\n' not in cwd or not matching:
            raise RuntimeError(f'端口 {port} 的进程身份无法确认为本工具，未关闭该进程。')
        os.kill(int(pid), signal.SIGTERM)
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        r = subprocess.run(['/usr/sbin/lsof', '-t', f'-iTCP:{port}', '-sTCP:LISTEN'], capture_output=True, text=True)
        if not r.stdout.strip():
            return
        time.sleep(.25)
    raise RuntimeError('旧网页服务尚未退出，未继续安装。')


def install(port):
    if not (ROOT / '.venv/bin/python').is_file():
        raise RuntimeError('请先完成首次安装。')
    folder = Path.home() / 'Library/LaunchAgents'
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / (LABEL + '.plist')
    config = configuration(ROOT, port)
    if path.exists():
        previous = plistlib.loads(path.read_bytes())
        if previous.get('WorkingDirectory') != str(ROOT):
            raise RuntimeError('已有另一份工具的同名启动项，请先核查，不自动覆盖。')
    domain = f'gui/{os.getuid()}'
    target = domain + '/' + LABEL
    (ROOT / 'work').mkdir(exist_ok=True)
    if launchctl('print', target, check=False).returncode == 0:
        if path.exists() and plistlib.loads(path.read_bytes()) == config:
            launchctl('kickstart', target)
            print(f'自动启动服务已配置：http://127.0.0.1:{port}/')
            return
        launchctl('bootout', target)
    stop_standalone(port)
    path.write_bytes(plistlib.dumps(config))
    path.chmod(0o644)
    launchctl('enable', target)
    try:
        launchctl('bootstrap', domain, str(path))
    except RuntimeError:
        env = os.environ.copy()
        env['VIDEO_READER_PORT'] = str(port)
        with (ROOT / 'work/service.log').open('ab') as log:
            subprocess.Popen(config['ProgramArguments'], cwd=ROOT, env=env,
                             stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True)
        raise
    deadline = time.monotonic() + 25
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/health', timeout=2) as response:
                health = json.load(response)
            if health.get('project') == str(ROOT):
                print(f'自动启动与自动恢复已启用：http://127.0.0.1:{port}/')
                return
        except (OSError, ValueError):
            pass
        time.sleep(.5)
    raise RuntimeError('启动项已安装，但服务未通过健康检查；请查看 work/service.log。')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['install', 'status', 'uninstall'])
    parser.add_argument('--port', type=int, default=8767)
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error('端口应在 1024～65535 之间')
    target = f'gui/{os.getuid()}/{LABEL}'
    if args.action == 'install':
        install(args.port)
    elif args.action == 'status':
        result = launchctl('print', target, check=False)
        print(result.stdout or '本工具自动启动项未加载。')
    else:
        path = Path.home() / 'Library/LaunchAgents' / (LABEL + '.plist')
        if path.exists():
            config = plistlib.loads(path.read_bytes())
            if config.get('WorkingDirectory') != str(ROOT):
                raise RuntimeError('启动项属于其他副本，未删除。')
            launchctl('bootout', target, check=False)
            path.unlink()
        print('已停用本工具的自动启动；Word 和任务记录均保留。')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        raise SystemExit(f'未完成：{error}。若系统限制操作，请从 Finder 双击自动启动设置文件。')
