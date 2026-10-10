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
swift -module-cache-path "$cache_dir" -e 'import AppKit; let image=NSImage(contentsOfFile:CommandLine.arguments[2])!; guard NSWorkspace.shared.setIcon(image,forFile:CommandLine.arguments[1],options:[]) else { fatalError("无法设置持久应用图标") }' "$PWD/$app" "$PWD/app.icns"
printf '已生成独立浅色窗口应用：%s\n' "$app"
