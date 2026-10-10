#!/bin/bash
# No curl | sh, sudo, Gatekeeper changes, or access to browser credentials.
set -euo pipefail
trap 'echo "安装未完成（入口第 $LINENO 行）。请按上方错误处理后重新运行 bash install.sh；若 Homebrew 安装失败，可改用 README 中的官方安装包。" >&2' ERR
cd -- "$(dirname -- "$0")"
export PATH="/opt/homebrew/opt/python@3.12/bin:/opt/homebrew/opt/node@22/bin:/opt/homebrew/bin:/Library/Frameworks/Python.framework/Versions/3.12/bin:/usr/local/bin:$PATH"
if [[ "$(uname -s)" != Darwin || "$(uname -m)" != arm64 ]]; then
  echo '仅支持原生 Apple Silicon Mac。若正在用 Rosetta，请在终端的“显示简介”取消“使用 Rosetta 打开”后重试。' >&2
  exit 1
fi
python_ok() {
  command -v python3.12 >/dev/null && python3.12 -c 'import sys,platform;sys.exit(not (sys.version_info[:2]==(3,12) and platform.machine()=="arm64"))'
}
node_ok() {
  command -v node >/dev/null && node -e 'process.exit(process.arch === "arm64" && Number(process.versions.node.split(".")[0]) >= 22 ? 0 : 1)'
}
if ! python_ok || ! node_ok; then
  if [[ -x /opt/homebrew/bin/brew ]]; then
    echo '使用已有的 Apple Silicon Homebrew 安装缺失环境（不使用 sudo）。'
    if ! python_ok; then /opt/homebrew/bin/brew install python@3.12; fi
    if ! node_ok; then /opt/homebrew/bin/brew install node@22; fi
    hash -r
  fi
fi
if ! python_ok; then
  echo '下一步：打开 https://www.python.org/downloads/release/python-31210/ ，安装 macOS universal2 安装包，然后重新运行 bash install.sh。系统密码由你本人输入。' >&2
  exit 1
fi
if ! node_ok; then
  echo '下一步：打开 https://nodejs.org/en/download ，安装 Node.js 22 或以上 LTS 的 macOS ARM64 安装包，然后重新运行 bash install.sh。系统密码由你本人输入。' >&2
  exit 1
fi
exec python3.12 install.py "$@"
