#!/bin/zsh
cd "${0:A:h}" || exit 1
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
if [[ ! -x .venv/bin/python ]]; then print '请先运行 首次安装.command'; read 'reply?按回车退出。'; exit 1; fi
mkdir -p work
if curl --silent --fail --max-time 2 http://127.0.0.1:8767/jobs >/dev/null; then
  print '端口 8767 已有服务，请先确认浏览器中的页面确实是本工具。'
else
  nohup .venv/bin/python app.py >> work/app.log 2>&1 < /dev/null &
  print '已请求后台启动；请稍后打开 http://127.0.0.1:8767'
fi
print '确认页面能打开后，这个终端窗口可以关闭。'
