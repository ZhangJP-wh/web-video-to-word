#!/bin/zsh
cd -- "${0:A:h}" || exit 1
uid_value=$(id -u)
service="gui/$uid_value/com.zhangjp.web-video-to-word"
plist="$HOME/Library/LaunchAgents/com.zhangjp.web-video-to-word.plist"
# Temporarily unload to prevent an old worker restarting during migration.
/bin/launchctl bootout "$service" 2>/dev/null || true
.venv/bin/python cloud_migration.py
result=$?
/bin/launchctl bootstrap "gui/$uid_value" "$plist" 2>/dev/null || /bin/launchctl kickstart "$service"
if (( result != 0 )); then
 print '迁移未完成，请把以上错误发给 Codex。'
else
 print '已完成千问专用版切换。刷新工具页面即可。'
fi
read '?按回车关闭窗口。'
