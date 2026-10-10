#!/bin/zsh
cd "${0:A:h}" || exit 1
/bin/bash install.sh --start-only --open
result=$?
if (( result != 0 )); then read 'reply?请按上方提示处理；按回车关闭窗口。'; fi
exit $result
