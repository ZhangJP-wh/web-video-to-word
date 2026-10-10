#!/bin/zsh
cd -- "${0:A:h}" || exit 1
export SSL_CERT_FILE=/etc/ssl/cert.pem
export PIP_CERT=/etc/ssl/cert.pem
export NODE_EXTRA_CA_CERTS=/etc/ssl/cert.pem
export PLAYWRIGHT_BROWSERS_PATH="$PWD/work/browser-bin"
.venv/bin/python -m pip install playwright || exit 1
.venv/bin/python -m playwright install chromium || exit 1
.venv/bin/python qianwen_browser.py login || exit 1
/bin/launchctl kill SIGTERM "gui/$(id -u)/com.zhangjp.web-video-to-word" 2>/dev/null || true
echo "登录配置完成。如已启用自动启动，服务将自动加载新版。"
read '?按回车关闭窗口。'
