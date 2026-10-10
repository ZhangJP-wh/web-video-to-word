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
