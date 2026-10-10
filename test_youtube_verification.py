import unittest
from youtube_verification import needs_verification
class VerificationTests(unittest.TestCase):
 def test_youtube_challenge(self):self.assertTrue(needs_verification("ERROR: [youtube] abc: Sign in to confirm you’re not a bot"))
 def test_other_failure_does_not_open_window(self):
  for error in ["HTTP Error 403", "千问未登录", "[youtube] Video unavailable"]:self.assertFalse(needs_verification(error))

 def test_normal_chrome_has_no_automation_connection(self):
  import tempfile
  from pathlib import Path
  from unittest.mock import patch,Mock
  from youtube_verification import verify
  with tempfile.TemporaryDirectory() as tmp:
   job=Path(tmp)/'work/jobs/task';job.mkdir(parents=True);cookies=job.parent.parent/'youtube-verification/youtube-manual-chrome/Default/Cookies';cookies.parent.mkdir(parents=True);cookies.touch()
   with patch('youtube_verification.chrome_path',return_value=Path('/chrome')),patch('youtube_verification.subprocess.Popen') as launch:
    verify('https://www.youtube.com/watch?v=test',job,{},Mock())
    args=launch.call_args.args[0]
    self.assertFalse(any('remote-debugging' in arg or 'enable-automation' in arg for arg in args))
    self.assertTrue(any('youtube-manual-chrome' in arg for arg in args))

 def test_confirmation_only_for_waiting_task(self):
  import tempfile,json
  from pathlib import Path
  from youtube_verification import confirm
  with tempfile.TemporaryDirectory() as tmp:
   job=Path(tmp);(job/'job.json').write_text(json.dumps({'state':'youtube_verifying'}));self.assertTrue(confirm(job)['ok']);self.assertTrue((job/'youtube-verification-confirmed').exists())
   (job/'job.json').write_text(json.dumps({'state':'completed'}))
   with self.assertRaises(ValueError):confirm(job)

 def test_two_tasks_reuse_one_window(self):
  import tempfile
  from pathlib import Path
  from unittest.mock import patch,Mock
  from youtube_verification import verify,shared_root
  with tempfile.TemporaryDirectory() as tmp:
   jobs=[Path(tmp)/'work/jobs'/str(i) for i in range(2)]
   for job in jobs:job.mkdir(parents=True)
   cookies=shared_root(jobs[0])/'youtube-manual-chrome/Default/Cookies';cookies.parent.mkdir(parents=True);cookies.touch()
   with patch('youtube_verification.chrome_path',return_value=Path('/chrome')),patch('youtube_verification.subprocess.Popen') as launch:
    first=verify('https://youtube.com/watch?v=one',jobs[0],{},Mock())
    second=verify('https://youtube.com/watch?v=two',jobs[1],{},Mock())
    self.assertEqual(first,second);self.assertEqual(launch.call_count,1)

 def test_any_waiting_task_can_confirm_shared_window(self):
  import tempfile,json
  from pathlib import Path
  from youtube_verification import confirm,shared_root
  with tempfile.TemporaryDirectory() as tmp:
   job=Path(tmp)/'work/jobs/task';job.mkdir(parents=True)
   (job/'job.json').write_text(json.dumps({'state':'youtube_verifying','youtube_shared_verification':True}))
   confirm(job);self.assertTrue((shared_root(job)/'confirmed').exists())

 def test_concurrent_tasks_wait_for_one_window(self):
  import tempfile,time,threading
  from concurrent.futures import ThreadPoolExecutor
  from pathlib import Path
  from unittest.mock import patch,Mock
  from youtube_verification import verify,shared_root
  with tempfile.TemporaryDirectory() as tmp:
   jobs=[Path(tmp)/'work/jobs'/str(i) for i in range(2)]
   for job in jobs:job.mkdir(parents=True)
   cookies=shared_root(jobs[0])/'youtube-manual-chrome/Default/Cookies';cookies.parent.mkdir(parents=True);cookies.touch()
   opened=threading.Event();release=threading.Event()
   process=Mock();process.poll.side_effect=lambda:0 if release.is_set() else None
   def launch(*args,**kwargs):opened.set();return process
   with patch('youtube_verification.chrome_path',return_value=Path('/chrome')),patch('youtube_verification.subprocess.Popen',side_effect=launch) as popen:
    with ThreadPoolExecutor(max_workers=2) as pool:
     a=pool.submit(verify,'https://youtube.com/a',jobs[0],{},Mock())
     self.assertTrue(opened.wait(2))
     b=pool.submit(verify,'https://youtube.com/b',jobs[1],{},Mock())
     time.sleep(.1);self.assertFalse(b.done());release.set()
     self.assertEqual(a.result(timeout=3),b.result(timeout=3));self.assertEqual(popen.call_count,1)
