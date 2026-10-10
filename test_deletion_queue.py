import tempfile,json,unittest
from pathlib import Path
from unittest.mock import Mock,patch
from deletion_queue import DeletionQueue
class QueueTests(unittest.TestCase):
 def setup_queue(self):
  tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);work=Path(tmp.name);job=work/'jobs/123456abcdef';job.mkdir(parents=True);(job/'job.json').write_text('{}')
  delete=Mock(return_value={'deletion_result':{'status':'success','at':1}});failed=Mock(return_value={'status':'failed','at':1});q=DeletionQueue(work,delete,failed)
  return q,delete,failed,job
 def test_busy_waits_and_free_executes(self):
  q,delete,failed,job=self.setup_queue();self.assertEqual(q.submit(job.name)['status'],'pending')
  with patch('deletion_queue.browser_busy',return_value=True):q.run_once()
  delete.assert_not_called();failed.assert_not_called();self.assertTrue(q.has_pending())
  with patch('deletion_queue.browser_busy',return_value=False):q.run_once()
  delete.assert_called_once_with(job.name);self.assertFalse(q.has_pending())
 def test_restart_and_duplicate_submit(self):
  q,delete,failed,job=self.setup_queue();q.submit(job.name);q.submit(job.name)
  self.assertEqual(len(list(q.folder.glob('*.json'))),1)
  restored=DeletionQueue(q.work,delete,failed)
  with patch('deletion_queue.browser_busy',return_value=False):restored.run_once()
  delete.assert_called_once()
 def test_nonbusy_failure_is_reported(self):
  q,delete,failed,job=self.setup_queue();q.submit(job.name);delete.side_effect=ValueError('登录失效')
  with patch('deletion_queue.browser_busy',return_value=False):q.run_once()
  failed.assert_called_once_with(job.name,'登录失效');self.assertFalse(q.has_pending())
 def test_lock_race_stays_pending(self):
  q,delete,failed,job=self.setup_queue();q.submit(job.name);delete.side_effect=ValueError('千问浏览器正在使用中')
  with patch('deletion_queue.browser_busy',return_value=False):q.run_once()
  failed.assert_not_called();self.assertTrue(q.has_pending())
 def test_expired_queue_has_clear_failure(self):
  q,delete,failed,job=self.setup_queue();q.submit(job.name);p=q.folder/(job.name+'.json');d=json.loads(p.read_text());d['created_at']=0;p.write_text(json.dumps(d));q.run_once()
  delete.assert_not_called();self.assertIn('超过6小时',failed.call_args.args[1]);self.assertFalse(q.has_pending())

class QueueHTTPTests(unittest.TestCase):
 def test_delete_returns_pending_without_claiming_success(self):
  import app,http.client,threading
  from http.server import ThreadingHTTPServer
  fake=Mock();fake.submit.return_value= {'status':'pending','message':'等待千问浏览器空闲'}
  server=ThreadingHTTPServer(('127.0.0.1',0),app.Handler)
  with patch.object(app,'PORT',server.server_port),patch.object(app,'get_deletion_queue',return_value=fake):
   thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
   try:
    conn=http.client.HTTPConnection('127.0.0.1',server.server_port)
    conn.request('POST','/delete/123456abcdef',body='{}',headers={'Content-Type':'application/json','Origin':f'http://127.0.0.1:{server.server_port}'})
    response=conn.getresponse();data=json.loads(response.read())
    self.assertEqual(response.status,202);self.assertEqual(data['deletion_result']['status'],'pending')
    fake.submit.assert_called_once_with('123456abcdef');conn.close()
   finally:server.shutdown();server.server_close();thread.join()
