"""Retry public page playback data when optional Bilibili API has no streams."""
from urllib.parse import urlsplit,parse_qs,urlencode
from yt_dlp.extractor.bilibili import BiliBiliIE
class BiliBiliPageFallbackIE(BiliBiliIE):
    @classmethod
    def ie_key(cls):return 'BiliBili'
    def _real_extract(self,url):
        self.source_url=url
        return super()._real_extract(url)
    def _download_playinfo(self,*args,**kwargs):
        info=super()._download_playinfo(*args,**kwargs)
        if kwargs.get('fatal') is False and info and 'v_voucher' in info and not self.extract_formats(info):
            self.report_warning('B站播放接口没有返回媒体地址，重新读取公开网页中的播放器数据。')
            bvid,cid=args[:2]
            source=getattr(self,'source_url','https://www.bilibili.com/video/'+bvid+'/')
            part=parse_qs(urlsplit(source).query).get('p',['1'])[0]
            for extra in ({'p':part,'t':'0'},{'p':part}):
                page=self._download_webpage('https://www.bilibili.com/video/'+bvid+'/?'+urlencode(extra),bvid,fatal=False)
                if not page:continue
                state=self._search_json(r'window\.__INITIAL_STATE__\s*=',page,'page state',bvid,default={})
                selected=state.get('videoData',{}).get('cid')
                if str(selected)!=str(cid):continue # Never substitute a different episode.
                play=self._search_json(r'window\.__playinfo__\s*=',page,'page playback',bvid,default={}).get('data',{})
                if self.extract_formats(play):return play
            return None # Preserve initial-page data if these pages also lack streams.
        return info

def register(downloader):
    downloader.add_info_extractor(BiliBiliPageFallbackIE())
