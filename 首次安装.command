#!/bin/zsh
cd "${0:A:h}" || exit 1
/bin/bash install.sh --open
result=$?
if (( result != 0 )); then print '安装未完成，请按上方“下一步”操作后重试。'; fi
read 'reply?按回车关闭窗口。'
exit $result
