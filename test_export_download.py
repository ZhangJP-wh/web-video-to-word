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

 def test_empty_saved_download_uses_recovery(self):
  stream=io.BytesIO()
  with zipfile.ZipFile(stream,'w') as z:z.writestr('word/document.xml','<document/>')
  download=Mock();download.url='blob:export';download.save_as.side_effect=lambda path:Path(path).write_bytes(b'')
  page=Mock();page.evaluate.return_value=base64.b64encode(stream.getvalue()).decode()
  with tempfile.TemporaryDirectory() as tmp:
   target=Path(tmp)/'original.docx';save_export_download(download,page,target);self.assertEqual(target.read_bytes(),stream.getvalue())
 def test_network_failure_leaves_no_partial_file(self):
  download=Mock();download.save_as.side_effect=RuntimeError('canceled');page=Mock();page.evaluate.side_effect=RuntimeError('Failed to fetch')
  with tempfile.TemporaryDirectory() as tmp:
   target=Path(tmp)/'original.docx'
   with self.assertRaisesRegex(RuntimeError,'无需重新上传'):save_export_download(download,page,target)
   self.assertFalse(target.exists());self.assertFalse(target.with_suffix('.partial.docx').exists())
