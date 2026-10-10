#!/usr/bin/env python3
import os, platform, shutil, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
if platform.system() != "Darwin" or platform.machine() != "arm64":
    raise SystemExit("本安装版仅验证 Apple 芯片 Mac；请使用原生 arm64 终端。")
if sys.version_info[:2] != (3, 12):
    raise SystemExit("请先安装 Python 3.12，再运行首次安装。")
node = shutil.which("node")
if not node or int(subprocess.check_output([node, "--version"], text=True).strip().lstrip("v").split(".")[0]) < 22:
    raise SystemExit("请先从 nodejs.org 安装 Node.js 22 或以上的 LTS 版本。")
folder = ROOT / ".venv"
if not folder.exists():
    subprocess.run([sys.executable, "-m", "venv", str(folder)], check=True)
python = str(folder / "bin/python")
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(ROOT / "work/browser-bin")
subprocess.run([python, "-m", "pip", "install", "--upgrade", "pip"], check=True)
subprocess.run([python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
subprocess.run([python, "-m", "pip", "check"], check=True)
subprocess.run([python, "-m", "unittest", "test_reader", "test_app", "-q"], check=True)
print("正在安装千问后台浏览器，可以等待，不要关闭窗口。", flush=True)
subprocess.run([python, "-m", "playwright", "install", "chromium"], check=True)
print("安装完成。请双击：启动工具.command。", flush=True)
