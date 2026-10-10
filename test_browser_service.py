import unittest
from unittest.mock import Mock,patch
from qianwen_browser import browser_context
class SharedPagesTests(unittest.TestCase):
 def test_each_client_owns_only_its_page(self):
  p=Mock();browser=p.chromium.connect_over_cdp.return_value;context=Mock();browser.contexts=[context]
  first,second=Mock(),Mock();context.new_page.side_effect=[first,second]
  with patch('browser_service.endpoint',return_value='ws://127.0.0.1:18769/devtools/browser/test'), patch('qianwen_browser.TaskContext',side_effect=lambda ctx: Mock(page=ctx.new_page(),pages=[])):
   # Exercise close ownership using independent page wrappers.
   from qianwen_browser import TaskContext
   TaskContext.side_effect=lambda ctx: type('Owned',(),{'page':(page:=ctx.new_page()),'pages':[page],'owner':Mock()})()
   with browser_context(p) as one:
    with browser_context(p) as two:
     self.assertIs(one.pages[0],first);self.assertIs(two.pages[0],second)
    second.close.assert_called_once();first.close.assert_not_called()
   first.close.assert_called_once();context.close.assert_not_called()
 def test_shared_browser_is_not_busy_for_deletion(self):
  from deletion_queue import browser_busy
  with patch('browser_service.endpoint',return_value='ws://localhost/test'):
   self.assertFalse(browser_busy('/unused'))

class LoginDiagnosticsTests(unittest.TestCase):
 def test_endpoint_explicitly_bypasses_proxy(self):
  from browser_service import endpoint
  import json
  response=Mock();response.__enter__=Mock(return_value=response);response.__exit__=Mock(return_value=False)
  response.read.return_value=json.dumps({'webSocketDebuggerUrl':'ws://127.0.0.1/test'}).encode()
  with patch('urllib.request.ProxyHandler') as proxy,patch('urllib.request.build_opener') as opener:
   opener.return_value.open.return_value=response
   self.assertEqual(endpoint(),'ws://127.0.0.1/test');proxy.assert_called_once_with({})
 def test_login_failure_surfaces_actual_busy_reason(self):
  import app,tempfile,json,time
  from pathlib import Path
  with tempfile.TemporaryDirectory() as tmp:
   work=Path(tmp);(work/'qianwen-auth.json').write_text('{}')
   (work/'qianwen-login-result.json').write_text(json.dumps({'error':'旧任务占用浏览器'}))
   process=Mock();process.poll.return_value=1
   with patch.object(app,'WORK',work),patch.object(app,'login_process',process),patch.object(app,'auth_check_started',time.time()),patch.object(app,'list_jobs',return_value=[]):
    self.assertEqual(app.login_status()['error'],'旧任务占用浏览器')
