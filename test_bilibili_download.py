import unittest
from unittest.mock import patch
from bilibili_download import BiliBiliPageFallbackIE
class FallbackTests(unittest.TestCase):
 def test_optional_voucher_does_not_override_page(self):
  ie=BiliBiliPageFallbackIE()
  with patch('yt_dlp.extractor.bilibili.BiliBiliIE._download_playinfo',return_value={'v_voucher':'test'}),patch.object(ie,'extract_formats',return_value=[]),patch.object(ie,'report_warning'),patch.object(ie,'_download_webpage',return_value=None):
   self.assertIsNone(ie._download_playinfo('video','cid',fatal=False))
 def test_playable_api_kept(self):
  ie=BiliBiliPageFallbackIE();info={'dash':{'audio':[]}}
  with patch('yt_dlp.extractor.bilibili.BiliBiliIE._download_playinfo',return_value=info):self.assertIs(ie._download_playinfo('video','cid',fatal=False),info)
 def test_required_api_not_suppressed(self):
  ie=BiliBiliPageFallbackIE();info={'v_voucher':'test'}
  with patch('yt_dlp.extractor.bilibili.BiliBiliIE._download_playinfo',return_value=info):self.assertIs(ie._download_playinfo('video','cid'),info)

 def test_matching_page_streams_used(self):
  ie=BiliBiliPageFallbackIE();api={'v_voucher':'test'};play={'dash':{'audio':[{'id':1}]}}
  with patch('yt_dlp.extractor.bilibili.BiliBiliIE._download_playinfo',return_value=api),patch.object(ie,'extract_formats',side_effect=lambda data: [] if data==api else [{'url':'media'}]),patch.object(ie,'report_warning'),patch.object(ie,'_download_webpage',return_value='page'),patch.object(ie,'_search_json',side_effect=[{'videoData':{'cid':123}},{'data':play}]):
   self.assertIs(ie._download_playinfo('BVtest',123,fatal=False),play)
 def test_other_episode_not_used(self):
  ie=BiliBiliPageFallbackIE()
  with patch('yt_dlp.extractor.bilibili.BiliBiliIE._download_playinfo',return_value={'v_voucher':'test'}),patch.object(ie,'extract_formats',return_value=[]),patch.object(ie,'report_warning'),patch.object(ie,'_download_webpage',return_value='page'),patch.object(ie,'_search_json',return_value={'videoData':{'cid':999}}):
   self.assertIsNone(ie._download_playinfo('BVtest',123,fatal=False))
