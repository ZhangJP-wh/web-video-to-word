import tempfile
import unittest
from pathlib import Path
from docx import Document
from qianwen_browser import read_export

class QianwenExportTests(unittest.TestCase):
    def export(self, lines):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        path=Path(temp.name)/'export.docx';doc=Document()
        for line in lines:doc.add_paragraph(line)
        doc.save(path);return path
    def test_preserves_all_paragraphs_and_speakers(self):
        p=self.export(['标题','2026年10月07日','发言人1   00:00','第一段。','继续讲话。','发言人2   00:12','第二段。'])
        result=read_export(p,20)
        self.assertEqual(result['segments'],[{'start':0,'end':12,'speaker':'发言人1','text':'第一段。\n继续讲话。'},{'start':12,'end':20,'speaker':'发言人2','text':'第二段。'}])
    def test_rejects_missing_timestamps(self):
        with self.assertRaises(ValueError):read_export(self.export(['只有正文']),20)
    def test_rejects_wrong_duration(self):
        with self.assertRaises(ValueError):read_export(self.export(['发言人1   01:00','正文']),20)
    def test_rejects_empty_segment(self):
        with self.assertRaises(ValueError):read_export(self.export(['发言人1   00:00']),20)

class RecoveryTests(unittest.TestCase):
    def test_download_certificate_bundle_loads_trusted_roots(self):
        import certifi,ssl
        context=ssl.create_default_context(cafile=certifi.where())
        self.assertGreater(context.cert_store_stats()['x509_ca'],0)
        self.assertEqual(context.verify_mode,ssl.CERT_REQUIRED)

    def test_timeout_reuses_saved_cloud_document(self):
        from unittest.mock import patch
        from playwright.sync_api import TimeoutError
        import qianwen_browser as browser
        meta={};calls=[]
        def export(audio,job,record,save):
            calls.append(record.get('qianwen_url'))
            if len(calls)==1:
                record.update(qianwen_submitted=True,qianwen_url='https://www.qianwen.com/efficiency/doc/transcripts/test')
                raise TimeoutError('loading')
            return {'model':'qianwen-web'}
        with patch.object(browser,'export_audio',side_effect=export),patch.object(browser.time,'sleep'):
            result=browser.export_with_retry(None,Path('/tmp/test'),meta,lambda *args:None)
        self.assertEqual(result['model'],'qianwen-web')
        self.assertEqual(calls,[None,meta['qianwen_url']])

    def test_login_error_is_not_retried(self):
        from unittest.mock import patch
        import qianwen_browser as browser
        with patch.object(browser,'export_audio',side_effect=browser.LoginRequired('login')) as run:
            with self.assertRaises(browser.LoginRequired):browser.export_with_retry(None,Path('/tmp/test'),{},lambda *args:None)
        self.assertEqual(run.call_count,1)

    def test_timeout_retry_is_bounded(self):
        from unittest.mock import patch
        from playwright.sync_api import TimeoutError
        import qianwen_browser as browser
        with patch.object(browser,'export_audio',side_effect=TimeoutError('loading')) as run,patch.object(browser.time,'sleep'):
            with self.assertRaises(TimeoutError):browser.export_with_retry(None,Path('/tmp/test'),{},lambda *args:None)
        self.assertEqual(run.call_count,3)

    def test_export_options_wait_before_selection(self):
        from unittest.mock import MagicMock,patch
        import qianwen_browser as browser
        page=MagicMock();panel=page.get_by_role.return_value.filter.return_value.first
        checks=panel.get_by_role.return_value
        with patch('playwright.sync_api.expect') as expect:
            browser.export_panel(page,Path('/tmp/test'))
            panel.wait_for.assert_called_once_with(state='visible',timeout=30000)
            expect.assert_called_once_with(checks)
            expect.return_value.to_have_count.assert_called_once_with(5,timeout=30000)
        checks.count.assert_not_called()

if __name__=='__main__':unittest.main()
