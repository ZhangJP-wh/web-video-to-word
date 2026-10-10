import unittest,tempfile,json
from pathlib import Path
from unittest.mock import patch
class StatusTests(unittest.TestCase):
 def test_readonly_status_does_not_mutate_job(self):
  from runtime_status import snapshot
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);job=root/'work/jobs/123456abcdef';job.mkdir(parents=True)
   record=job/'job.json';record.write_text('{"state":"failed"}');before=record.read_bytes()
   with patch('browser_service.endpoint',return_value='ws://localhost/test'):
    data=snapshot(root,[{'id':job.name,'state':'failed','title':'任务','error':'失败'}],{'status':'unknown'})
   self.assertEqual(record.read_bytes(),before);self.assertEqual(data['tasks'][0]['error'],'失败');self.assertIn('已连接',data['browser']);self.assertEqual(data['pages'],[])
