import unittest,tempfile,base64,io,zipfile
from pathlib import Path
from unittest.mock import Mock
from qianwen_browser import save_export_download
class ExportTests(unittest.TestCase):
 def test_cancelled_download_uses_same_page_and_validates_word(self):
  stream=io.BytesIO()
  with zipfile.ZipFile(stream,'w') as z:z.writestr('word/document.xml','<document/>')
  download=Mock();download.save_as.side_effect=RuntimeError('Download.save_as: canceled');download.url='blob:export'
  page=Mock();page.evaluate.return_value=base64.b64encode(stream.getvalue()).decode()
  with tempfile.TemporaryDirectory() as tmp:
   target=Path(tmp)/'original.docx';save_export_download(download,page,target);self.assertEqual(target.read_bytes(),stream.getvalue())
  self.assertEqual(page.evaluate.call_args.args[1],'blob:export')
 def test_invalid_download_not_saved(self):
  download=Mock();download.save_as.side_effect=RuntimeError('canceled');page=Mock();page.evaluate.return_value=base64.b64encode(b'<html>login</html>').decode()
  with tempfile.TemporaryDirectory() as tmp:
   target=Path(tmp)/'original.docx'
   with self.assertRaises(RuntimeError):save_export_download(download,page,target)
   self.assertFalse(target.exists())
