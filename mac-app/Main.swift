import Cocoa
import WebKit
final class AppDelegate: NSObject, NSApplicationDelegate, WKUIDelegate, WKNavigationDelegate, WKDownloadDelegate {
 var window: NSWindow!
 var web: WKWebView!
 func applicationDidFinishLaunching(_ notification: Notification) {
  if let icon=Bundle.main.url(forResource:"app-current",withExtension:"icns") {NSApp.applicationIconImage=NSImage(contentsOf:icon)}
  NSApp.appearance = NSAppearance(named: .aqua)
  let config = WKWebViewConfiguration()
  web = WKWebView(frame: .zero, configuration: config)
  web.appearance = NSAppearance(named: .aqua)
  web.uiDelegate = self
  web.navigationDelegate = self
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
  view.addItem(withTitle:"返回任务列表",action:#selector(home),keyEquivalent:"0").target=self
  view.addItem(withTitle:"返回上一页",action:#selector(back),keyEquivalent:"[").target=self
  NSApp.mainMenu=menu
  web.load(URLRequest(url: URL(string:"http://127.0.0.1:8767/")!))
  NSApp.activate(ignoringOtherApps:true)
 }
 @objc func reload(){web.reload()}
 @objc func home(){web.load(URLRequest(url:URL(string:"http://127.0.0.1:8767/")!))}
 @objc func back(){if web.canGoBack {web.goBack()} else {home()}}
 func showError(_ message:String){
  let alert=NSAlert();alert.messageText="工具窗口提示";alert.informativeText=message
  alert.addButton(withTitle:"好");alert.beginSheetModal(for:window){_ in}
 }
 func webView(_ webView:WKWebView,decidePolicyFor navigationAction:WKNavigationAction,decisionHandler:@escaping (WKNavigationActionPolicy)->Void){
  if let url=navigationAction.request.url,let host=url.host,
     !(host == "127.0.0.1" && url.port == 8767) {
   if navigationAction.navigationType == .linkActivated {NSWorkspace.shared.open(url)}
   decisionHandler(.cancel);return
  }
  decisionHandler(navigationAction.shouldPerformDownload ? .download : .allow)
 }
 func webView(_ webView:WKWebView,decidePolicyFor navigationResponse:WKNavigationResponse,decisionHandler:@escaping (WKNavigationResponsePolicy)->Void){
  decisionHandler(navigationResponse.canShowMIMEType ? .allow : .download)
 }
 func webView(_ webView:WKWebView,navigationAction:WKNavigationAction,didBecome download:WKDownload){download.delegate=self}
 func webView(_ webView:WKWebView,navigationResponse:WKNavigationResponse,didBecome download:WKDownload){download.delegate=self}
 func download(_ download:WKDownload,decideDestinationUsing response:URLResponse,suggestedFilename:String,completionHandler:@escaping (URL?)->Void){
  let panel=NSSavePanel();panel.nameFieldStringValue=suggestedFilename
  panel.directoryURL=FileManager.default.urls(for:.downloadsDirectory,in:.userDomainMask).first
  panel.beginSheetModal(for:window){response in completionHandler(response == .OK ? panel.url:nil)}
 }
 func download(_ download:WKDownload,didFailWithError error:Error,resumeData:Data?){
  if (error as NSError).code != NSURLErrorCancelled {showError("文件保存失败："+error.localizedDescription)}
 }
 func webView(_ webView:WKWebView,didFailProvisionalNavigation navigation:WKNavigation!,withError error:Error){
  if (error as NSError).code != NSURLErrorCancelled {showError("无法连接工具后台："+error.localizedDescription+"。请确认后台服务已启动，再按 Command-R 刷新。")}
 }
 func webView(_ webView:WKWebView,didFail navigation:WKNavigation!,withError error:Error){
  if (error as NSError).code != NSURLErrorCancelled {showError("页面加载失败："+error.localizedDescription+"。可按 Command-R 重试。")}
 }
 func webViewWebContentProcessDidTerminate(_ webView:WKWebView){
  showError("页面进程已停止，后台任务不会因此停止。请按 Command-R 重新加载。")
 }
 func applicationShouldTerminateAfterLastWindowClosed(_ sender:NSApplication)->Bool {true}
 func webView(_ webView:WKWebView,runJavaScriptConfirmPanelWithMessage message:String,initiatedByFrame frame:WKFrameInfo,completionHandler:@escaping (Bool)->Void) {
  let alert=NSAlert();alert.alertStyle = .warning
  alert.messageText="请确认操作";alert.informativeText=message
  alert.addButton(withTitle:"确认");alert.addButton(withTitle:"取消")
  alert.buttons[1].keyEquivalent="\u{1b}"
  alert.beginSheetModal(for:window){response in completionHandler(response == .alertFirstButtonReturn)}
 }
 func webView(_ webView:WKWebView,runJavaScriptAlertPanelWithMessage message:String,initiatedByFrame frame:WKFrameInfo,completionHandler:@escaping ()->Void) {
  let alert=NSAlert();alert.messageText="工具提示";alert.informativeText=message
  alert.addButton(withTitle:"好")
  alert.beginSheetModal(for:window){_ in completionHandler()}
 }
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
