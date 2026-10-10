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

 def test_large_file_uses_local_cdp_path(self):
  from qianwen_browser import set_local_upload_file
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'large.mp3'
   with path.open('wb') as f:f.truncate(51*1024*1024)
   chooser=Mock();page=Mock();session=page.context.new_cdp_session.return_value
   session.send.side_effect=[{'root':{'nodeId':1}},{'nodeId':2},{}]
   set_local_upload_file(page,chooser,path)
   chooser.set_files.assert_not_called();session.send.assert_any_call('DOM.setFileInputFiles',{'nodeId':2,'files':[str(path.resolve())]});session.detach.assert_called_once()
 def test_file_size_error_does_not_suggest_login(self):
  from qianwen_browser import upload_failure_message
  error='Cannot transfer files larger than 50Mb'
  self.assertEqual(upload_failure_message('cloud_uploading',error),error)
