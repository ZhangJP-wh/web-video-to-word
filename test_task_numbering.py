import unittest,tempfile,json,shutil
from pathlib import Path
from task_numbering import numbers,migrate_documents
class NumberTests(unittest.TestCase):
 def test_delete_leaves_gap_and_retry_keeps_number(self):
  with tempfile.TemporaryDirectory() as tmp:
   work=Path(tmp)
   for ident,t in [('first',1),('second',2)]:
    job=work/'jobs'/ident;job.mkdir(parents=True);(job/'job.json').write_text(json.dumps({'created_at':t}))
   self.assertEqual(numbers(work),{'first':1,'second':2})
   shutil.rmtree(work/'jobs/first');job=work/'jobs/third';job.mkdir();(job/'job.json').write_text('{"created_at":3}')
   self.assertEqual(numbers(work)['third'],3);self.assertEqual(numbers(work)['second'],2)
 def test_document_rename_updates_owned_paths(self):
  with tempfile.TemporaryDirectory() as tmp:
   work=Path(tmp)/'work';job=work/'jobs/one';job.mkdir(parents=True);output=Path(tmp)/'output';output.mkdir();old=output/'title.docx';old.write_bytes(b'example')
   meta={'created_at':1,'state':'completed','name':'title','url':'source','document':str(old)};(job/'job.json').write_text(json.dumps(meta))
   from unittest.mock import patch
   with patch('reader.configure_folder_sort'):migrate_documents(work,output)
   self.assertEqual((output/'1 - title.docx').read_bytes(),b'example');self.assertFalse(old.exists());self.assertEqual(json.loads((job/'job.json').read_text())['document'],str(output/'1 - title.docx'))
