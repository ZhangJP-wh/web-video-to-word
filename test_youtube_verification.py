import unittest
from youtube_verification import needs_verification
class VerificationTests(unittest.TestCase):
 def test_youtube_challenge(self):self.assertTrue(needs_verification("ERROR: [youtube] abc: Sign in to confirm you’re not a bot"))
 def test_other_failure_does_not_open_window(self):
  for error in ["HTTP Error 403", "千问未登录", "[youtube] Video unavailable"]:self.assertFalse(needs_verification(error))
