#!/usr/bin/env python3
"""Idempotent installation and verified local startup; stdlib only at entry."""
import argparse
import json
import os
import platform
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from runtime_compat import venv_python

ROOT = Path(__file__).resolve().parent
TESTS = ['test_reader', 'test_app', 'test_qianwen', 'test_task_controls', 'test_install', 'test_runtime_compat']


def run(args, **kwargs):
    print('执行：' + ' '.join(map(str, args)), flush=True)
    return subprocess.run(list(map(str, args)), check=True, cwd=ROOT, **kwargs)


def check_environment():
    system, machine = platform.system(), platform.machine().lower()
    if not ((system == 'Darwin' and machine == 'arm64') or (system == 'Windows' and machine in ('amd64', 'x86_64'))):
        raise RuntimeError('支持原生 Apple Silicon Mac 或 Windows 10/11 x64；不支持 Rosetta、Intel Mac、Windows ARM/32位和 Linux。')
    if system == 'Windows' and sys.maxsize <= 2**32:
        raise RuntimeError('Windows 需要64位 Python 3.12，请安装官方 x64 安装包。')
    if system == 'Windows' and sys.getwindowsversion().build < 17763:
        raise RuntimeError('需要 Windows 10 1809 或更新版本。')
    if sys.version_info[:2] != (3, 12):
        raise RuntimeError('需要 Python 3.12。请运行系统对应的安装入口。')
    node = shutil.which('node')
    if not node:
        raise RuntimeError('缺少 Node.js。请运行系统对应的安装入口。')
    info = json.loads(subprocess.check_output(
        [node, '-p', 'JSON.stringify({version:process.versions.node,arch:process.arch})'], text=True))
    expected_arch = 'x64' if system == 'Windows' else 'arm64'
    if int(info['version'].split('.')[0]) < 22 or info['arch'] != expected_arch:
        raise RuntimeError('需要与系统架构一致的 Node.js 22+。请运行对应系统的安装入口。')


def ensure_venv():
    folder = ROOT / '.venv'
    python = venv_python(ROOT)
    if folder.is_symlink():
        raise RuntimeError('.venv 是符号链接，请先人工核查其目标；安装器不会修改。')
    healthy = False
    if python.exists():
        try:
            info = json.loads(subprocess.check_output([str(python), '-c',
                'import sys,platform,json;print(json.dumps([list(sys.version_info[:2]),platform.machine(),sys.prefix,sys.base_prefix]))'], text=True, timeout=10))
            healthy = info[0] == [3, 12] and info[1].lower() == platform.machine().lower() and Path(info[2]).resolve() == folder.resolve() and info[2] != info[3]
        except (OSError, ValueError, subprocess.SubprocessError):
            pass
    if not healthy:
        if folder.exists():
            # Preserve rather than delete a potentially non-standard environment.
            backup = ROOT / ('.venv.backup-' + str(time.time_ns()))
            folder.rename(backup)
            print(f'旧环境保留在 {backup.name}；任务和登录资料不受影响。', flush=True)
        run([sys.executable, '-m', 'venv', folder])
    return python


def health(port):
    # Bypass ambient HTTP proxies for local checks.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(f'http://127.0.0.1:{port}/health', timeout=2) as response:
        return json.load(response)


def validate_health(data):
    if not (isinstance(data, dict) and data.get('ok') is True and data.get('project') == str(ROOT) and data.get('engines') == ['qianwen']):
        raise RuntimeError('端口上的服务不是本目录的千问工具。请关闭对应旧服务，或使用 --port 选择空闲端口；未停止任何进程。')


def started_service_matches(pid, launcher_pid):
    if pid == launcher_pid:
        return True
    if platform.system() != 'Windows':
        return False
    # Windows venv python.exe redirects to a child interpreter. Verify ancestry,
    # script and working directory rather than accepting an arbitrary PID.
    import psutil
    try:
        process = psutil.Process(pid)
        args = process.cmdline()
        return (any(p.pid == launcher_pid for p in process.parents()) and
                len(args) >= 2 and Path(args[1]).resolve() == ROOT / 'app.py' and
                Path(process.cwd()).resolve() == ROOT)
    except (psutil.NoSuchProcess, psutil.AccessDenied, OSError, ValueError):
        return False


def start_service(python, port):
    try:
        data = health(port)
    except (OSError, ValueError):
        data = None
    if data is not None:
        validate_health(data)
        print('本目录服务已运行，健康检查通过。')
        return
    with socket.socket() as probe:
        try:
            probe.bind(('127.0.0.1', port))
        except OSError as error:
            raise RuntimeError(f'端口 {port} 被占用，请用 --port 选择空闲端口；未停止其他服务。') from error
    env = os.environ.copy()
    env['VIDEO_READER_PORT'] = str(port)
    work = ROOT / 'work'
    work.mkdir(exist_ok=True)
    with (work / 'app.log').open('ab') as log:
        child = subprocess.Popen([str(python), str(ROOT / 'app.py')], cwd=ROOT, env=env,
            stdin=subprocess.DEVNULL, stdout=log, stderr=log,
            **({'creationflags': subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == 'nt' else {'start_new_session': True}))
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        if child.poll() is not None:
            raise RuntimeError('服务启动失败，请查看本机 work/app.log（不要公开上传日志）。')
        try:
            data = health(port)
        except (OSError, ValueError):
            time.sleep(.5)
            continue
        try:
            validate_health(data)
            if not started_service_matches(data.get('pid'), child.pid):
                raise RuntimeError('健康检查的进程与本次启动不一致，请检查端口。')
        except RuntimeError:
            child.terminate()
            raise
        print('服务启动及 /health 检查通过。')
        return
    child.terminate()
    raise RuntimeError('服务健康检查超时，本次启动的进程已请求停止；请查看本机 work/app.log。')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--no-start', action='store_true', help='只安装和验收，不启动服务')
    parser.add_argument('--start-only', action='store_true', help='启动已安装环境并验证健康状态')
    parser.add_argument('--port', type=int, default=8767)
    parser.add_argument('--open', action='store_true', help='健康检查通过后打开工具网页')
    args = parser.parse_args(argv)
    if not 1024 <= args.port <= 65535:
        parser.error('端口应在 1024～65535 之间')
    if args.no_start and args.start_only:
        parser.error('--no-start 和 --start-only 不能同时使用')
    check_environment()
    os.environ['PLAYWRIGHT_BROWSERS_PATH'] = str(ROOT / 'work/browser-bin')
    # macOS system trust roots; never disable TLS verification.
    if Path('/etc/ssl/cert.pem').is_file():
        for key in ('PIP_CERT', 'SSL_CERT_FILE', 'NODE_EXTRA_CA_CERTS'):
            os.environ.setdefault(key, '/etc/ssl/cert.pem')
    if args.start_only:
        python = venv_python(ROOT)
        if not python.exists():
            raise RuntimeError('请先运行系统对应的安装入口完成安装。')
    else:
        python = ensure_venv()
        run([python, '-m', 'ensurepip', '--upgrade'])
        run([python, '-m', 'pip', 'install', '--upgrade', 'pip'])
        run([python, '-m', 'pip', 'install', '-r', ROOT / 'requirements.txt'])
        run([python, '-m', 'pip', 'check'])
        run([python, '-m', 'playwright', 'install', 'chromium'])
        run([python, '-c', 'from playwright.sync_api import sync_playwright\nwith sync_playwright() as p:\n b=p.chromium.launch(); b.close()'])
        run([python, '-m', 'unittest', *TESTS, '-q'])
    if not args.no_start:
        start_service(python, args.port)
        url = f'http://127.0.0.1:{args.port}/'
        print(f'工具地址：{url}\n请点击网页“登录或打开千问”，由本人完成账号登录/验证码。健康检查不代表已登录或云端转写成功。')
        if args.open:
            if os.name == 'nt':
                os.startfile(url)
            else:
                run(['/usr/bin/open', url])
    else:
        print('安装和本机验收完成。运行 bash install.sh --start-only 启动。')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        raise SystemExit(f'未完成：{error}\n修复上述问题后重新运行系统对应的安装入口；不要提交 work、日志或登录资料。')
