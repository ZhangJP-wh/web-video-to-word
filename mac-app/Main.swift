import Cocoa
import WebKit
final class AppDelegate: NSObject, NSApplicationDelegate, WKUIDelegate {
 var window: NSWindow!
 var web: WKWebView!
 func applicationDidFinishLaunching(_ notification: Notification) {
  NSApp.appearance = NSAppearance(named: .aqua)
  let config = WKWebViewConfiguration()
  web = WKWebView(frame: .zero, configuration: config)
  web.appearance = NSAppearance(named: .aqua)
  web.uiDelegate = self
  window = NSWindow(contentRect: NSRect(x: 0,y: 0,width: 1100,height: 800),styleMask: [.titled,.closable,.miniaturizable,.resizable],backing: .buffered,defer: false)
  window.title = "网页视频转语音识别文字稿（由千问提供支持）"
  window.appearance = NSAppearance(named: .aqua)
  window.contentView = web
  window.center();window.makeKeyAndOrderFront(nil)
  let menu = NSMenu(); let item = NSMenuItem();menu.addItem(item)
  let appMenu = NSMenu();item.submenu = appMenu
  appMenu.addItem(withTitle: "退出工具", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "q")
  let editItem=NSMenuItem();menu.addItem(editItem);let edit=NSMenu(title:"编辑");editItem.submenu=edit
  for (title,selector,key) in [("剪切","cut:","x"),("复制","copy:","c"),("粘贴","paste:","v"),("全选","selectAll:","a")] {edit.addItem(withTitle:title,action:NSSelectorFromString(selector),keyEquivalent:key)}
  let viewItem=NSMenuItem();menu.addItem(viewItem);let view=NSMenu(title:"视图");viewItem.submenu=view
  view.addItem(withTitle:"刷新",action:#selector(reload),keyEquivalent:"r").target=self
  NSApp.mainMenu=menu
  web.load(URLRequest(url: URL(string:"http://127.0.0.1:8767/")!))
  NSApp.activate(ignoringOtherApps:true)
 }
 @objc func reload(){web.reload()}
 func applicationShouldTerminateAfterLastWindowClosed(_ sender:NSApplication)->Bool {true}
 func webView(_ webView:WKWebView,createWebViewWith configuration:WKWebViewConfiguration,for navigationAction:WKNavigationAction,windowFeatures:WKWindowFeatures)->WKWebView? {
  if let url=navigationAction.request.url {NSWorkspace.shared.open(url)}
  return nil
 }
 func webView(_ webView:WKWebView,runOpenPanelWith parameters:WKOpenPanelParameters,initiatedByFrame frame:WKFrameInfo,completionHandler:@escaping ([URL]?)->Void){
  let panel=NSOpenPanel();panel.allowsMultipleSelection=parameters.allowsMultipleSelection;panel.canChooseDirectories=parameters.allowsDirectories;panel.canChooseFiles=true
  panel.beginSheetModal(for:window){response in completionHandler(response == .OK ? panel.urls:nil)}
 }
}
let app=NSApplication.shared
app.setActivationPolicy(.regular)
let delegate=AppDelegate();app.delegate=delegate;app.run()
