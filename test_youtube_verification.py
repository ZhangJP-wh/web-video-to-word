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
   job=Path(tmp);cookies=job/'youtube-manual-chrome/Default/Cookies';cookies.parent.mkdir(parents=True);cookies.touch()
   with patch('youtube_verification.chrome_path',return_value=Path('/chrome')),patch('youtube_verification.subprocess.Popen') as launch:
    verify('https://www.youtube.com/watch?v=test',job,{},Mock())
    args=launch.call_args.args[0]
    self.assertFalse(any('remote-debugging' in arg or 'enable-automation' in arg for arg in args))
    self.assertTrue(any('youtube-manual-chrome' in arg for arg in args))
