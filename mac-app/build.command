#!/bin/zsh
set -e
cd -- "${0:A:h}"
app='网页视频转语音识别文字稿.app'
mkdir -p "$app/Contents/MacOS" "$app/Contents/Resources"
cp app.icns "$app/Contents/Resources/app-current.icns"
cp Info.plist "$app/Contents/Info.plist"
cache_dir=$(mktemp -d "${TMPDIR:-/tmp}/web-video-swift.XXXXXX")
trap 'rm -rf "$cache_dir"' EXIT
swiftc -module-cache-path "$cache_dir" Main.swift -o "$app/Contents/MacOS/WebVideoToWord" -framework Cocoa -framework WebKit
codesign --force --sign - "$app"
printf '已生成独立浅色窗口应用：%s\n' "$app"
