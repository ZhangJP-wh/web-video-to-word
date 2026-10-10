#!/bin/zsh
cd "${0:A:h}" || exit 1
.venv/bin/python launch_service.py uninstall --port 8767
result=$?
read 'reply?按回车关闭窗口。'
exit $result
