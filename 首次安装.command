#!/bin/zsh
cd "${0:A:h}" || exit 1
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
if ! command -v python3.12 >/dev/null 2>&1; then
  print '请先安装 Python 3.12： https://www.python.org/downloads/macos/'
  read 'reply?按回车退出。'; exit 1
fi
python3.12 install.py
result=$?
if (( result != 0 )); then print '安装未完成，请保留报错文字供 AI 排查。'; fi
read 'reply?按回车关闭窗口。'
exit $result
