"""Preserve public page formats when the optional API returns only a voucher."""
from yt_dlp.extractor.bilibili import BiliBiliIE
class BiliBiliPageFallbackIE(BiliBiliIE):
    @classmethod
    def ie_key(cls):return 'BiliBili'
    def _download_playinfo(self,*args,**kwargs):
        info=super()._download_playinfo(*args,**kwargs)
        if kwargs.get('fatal') is False and info and 'v_voucher' in info and not self.extract_formats(info):
            self.report_warning('B站接口要求访问验证，尝试保留公开网页中已有的播放地址。')
            return None
        return info

def register(downloader):
    downloader.add_info_extractor(BiliBiliPageFallbackIE())
