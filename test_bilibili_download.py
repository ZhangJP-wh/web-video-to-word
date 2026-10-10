import unittest
from unittest.mock import patch
from bilibili_download import BiliBiliPageFallbackIE
class FallbackTests(unittest.TestCase):
 def test_optional_voucher_does_not_override_page(self):
  ie=BiliBiliPageFallbackIE()
  with patch('yt_dlp.extractor.bilibili.BiliBiliIE._download_playinfo',return_value={'v_voucher':'test'}),patch.object(ie,'extract_formats',return_value=[]),patch.object(ie,'report_warning'):
   self.assertIsNone(ie._download_playinfo('video','cid',fatal=False))
 def test_playable_api_kept(self):
  ie=BiliBiliPageFallbackIE();info={'dash':{'audio':[]}}
  with patch('yt_dlp.extractor.bilibili.BiliBiliIE._download_playinfo',return_value=info):self.assertIs(ie._download_playinfo('video','cid',fatal=False),info)
 def test_required_api_not_suppressed(self):
  ie=BiliBiliPageFallbackIE();info={'v_voucher':'test'}
  with patch('yt_dlp.extractor.bilibili.BiliBiliIE._download_playinfo',return_value=info):self.assertIs(ie._download_playinfo('video','cid'),info)
