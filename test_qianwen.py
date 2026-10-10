import tempfile
import unittest
from pathlib import Path
from docx import Document
from qianwen_browser import read_export

class QianwenExportTests(unittest.TestCase):
    def test_unconfirmed_upload_suggests_login_and_preserves_cause(self):
        from qianwen_browser import upload_failure_message
        for state in ('cloud_connecting','cloud_uploading','cloud_confirming_upload'):
            message=upload_failure_message(state,'上传按钮等待超时')
            self.assertIn('上传按钮等待超时',message)
            self.assertIn('可能千问未登录',message)
            self.assertIn('登录或打开千问',message)

    def test_explicit_other_failures_do_not_suggest_login(self):
        from qianwen_browser import upload_failure_message
        for message in ('千问账号云端存储已满','超过500MB限制','千问需要登录'):
            self.assertEqual(upload_failure_message('cloud_uploading',message),message)
        for state in ('downloading','cloud_preparing','cloud_transcribing','generating_document'):
            self.assertEqual(upload_failure_message(state,'失败'),'失败')

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

class UploadConfirmationTests(unittest.TestCase):
    def page(self):
        from unittest.mock import MagicMock
        page=MagicMock()
        page.get_by_role.return_value.filter.return_value.all.return_value=[]
        page.get_by_role.return_value.all.return_value=[]
        page.locator.return_value.inner_text.return_value='最近记录'
        return page

    def test_submission_requires_visible_record(self):
        import qianwen_browser as browser
        page=self.page();meta={'qianwen_submission_attempted':True}
        with tempfile.TemporaryDirectory() as tmp:
            browser.confirm_submission(page,'test-task',Path(tmp),meta,lambda *args:None)
        page.get_by_text.return_value.filter.return_value.first.wait_for.assert_called_once_with(timeout=1000)
        self.assertTrue(meta['qianwen_upload_confirmed'])
        self.assertEqual(meta['state'],'cloud_transcribing')

    def test_absent_record_does_not_claim_submission_success(self):
        from unittest.mock import patch
        from playwright.sync_api import TimeoutError
        import qianwen_browser as browser
        page=self.page();page.get_by_text.return_value.filter.return_value.first.wait_for.side_effect=TimeoutError('absent')
        meta={'qianwen_submission_attempted':True}
        with tempfile.TemporaryDirectory() as tmp,patch.object(browser.time,'monotonic',side_effect=[0,0,130]):
            with self.assertRaisesRegex(RuntimeError,'未出现本次上传记录'):
                browser.confirm_submission(page,'test-task',Path(tmp),meta,lambda *args:None)
        self.assertFalse(meta.get('qianwen_upload_confirmed',False))
        self.assertEqual(meta['state'],'cloud_confirming_upload')
        page.locator.assert_called()

    def test_cloud_storage_full_stops_without_claiming_upload(self):
        from playwright.sync_api import TimeoutError
        import qianwen_browser as browser
        page=self.page()
        page.get_by_text.return_value.filter.return_value.first.wait_for.side_effect=TimeoutError('absent')
        page.locator.return_value.inner_text.return_value='任务添加成功，请在「我的记录」查看进展\n存储已满\n请删除不用的记录后重试'
        meta={'qianwen_submission_attempted':True}
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(RuntimeError,'云端存储已满'):
                browser.confirm_submission(page,'test-task',Path(tmp),meta,lambda *args:None)
        self.assertFalse(meta['qianwen_upload_confirmed'])
        self.assertFalse(meta['qianwen_submission_attempted'])
        page.get_by_text.return_value.filter.return_value.first.wait_for.assert_called_once()

class CloudErrorTests(unittest.TestCase):
    def test_visible_cloud_error_is_preserved(self):
        from unittest.mock import MagicMock
        from qianwen_browser import require_cloud_available
        page=MagicMock();alert=MagicMock()
        alert.is_visible.return_value=True;alert.inner_text.return_value='上传失败，请稍后重试'
        page.get_by_role.return_value.all.return_value=[alert]
        with self.assertRaisesRegex(RuntimeError,'上传失败，请稍后重试'):
            require_cloud_available(page)

    def test_success_or_hidden_alert_does_not_fail_task(self):
        from unittest.mock import MagicMock
        from qianwen_browser import require_cloud_available
        page=MagicMock();success=MagicMock();hidden=MagicMock()
        success.is_visible.return_value=True;success.inner_text.return_value='任务添加成功'
        hidden.is_visible.return_value=False;hidden.inner_text.return_value='上传失败'
        page.get_by_role.return_value.all.return_value=[success,hidden]
        require_cloud_available(page)

class CloudDeleteSafetyTests(unittest.TestCase):
    def test_rejects_record_title_without_task_identifier(self):
        from unittest.mock import MagicMock
        import qianwen_browser as browser
        page=MagicMock()
        with self.assertRaisesRegex(RuntimeError,'归属'):
            browser.delete_cloud_record(page,Path('/tmp/123456abcdef'),{'qianwen_submitted':True,'qianwen_upload_title':'同名视频'},lambda *args:None)
        page.get_by_role.assert_not_called()

    def test_recent_records_counter_does_not_block_deletion(self):
        from unittest.mock import MagicMock,patch
        import qianwen_browser as browser
        page=UploadConfirmationTests().page();meta={'title':'测试','qianwen_submitted':True}
        # The actual header is “最近记录 + 4”; exact matching must not be used.
        def text_locator(text,exact=False):
            if text=='最近记录' and exact:raise AssertionError('header includes counter')
            return MagicMock()
        page.get_by_text.side_effect=text_locator
        with patch('playwright.sync_api.expect'):
            browser.delete_cloud_record(page,Path('/tmp/123456abcdef'),meta,lambda *args:None)
        self.assertTrue(meta['qianwen_cloud_deleted'])
        page.get_by_text.assert_any_call('最近记录',exact=False)

    def test_missing_cloud_record_allows_local_cleanup_without_claiming_deleted(self):
        from unittest.mock import patch
        import qianwen_browser as browser
        page=UploadConfirmationTests().page();meta={'title':'测试','qianwen_submitted':True}
        page.locator.return_value.filter.return_value.count.return_value=0
        with patch('playwright.sync_api.expect') as expect:
            expect.return_value.to_have_count.side_effect=AssertionError('record absent')
            browser.delete_cloud_record(page,Path('/tmp/123456abcdef'),meta,lambda *args:None)
        self.assertEqual(meta['qianwen_delete_result'],'not_found')
        self.assertTrue(meta['qianwen_delete_resolved'])
        self.assertFalse(meta.get('qianwen_cloud_deleted',False))
        page.locator.return_value.filter.return_value.locator.assert_not_called()

    def test_ambiguous_record_never_clicks_delete(self):
        from unittest.mock import MagicMock,patch
        import qianwen_browser as browser
        page=UploadConfirmationTests().page();meta={'title':'测试','qianwen_submitted':True}
        with patch('playwright.sync_api.expect') as expect:
            expect.return_value.to_have_count.side_effect=AssertionError('two records')
            with self.assertRaisesRegex(RuntimeError,'唯一定位'):
                browser.delete_cloud_record(page,Path('/tmp/123456abcdef'),meta,lambda *args:None)
        page.locator.return_value.filter.return_value.locator.assert_not_called()
        self.assertFalse(meta.get('qianwen_cloud_deleted',False))

if __name__=='__main__':unittest.main()
