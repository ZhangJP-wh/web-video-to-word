import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from docx import Document
import app


class PageTests(unittest.TestCase):
    def fixture(self, root):
        job = root / 'work/jobs/123456abcdef'
        job.mkdir(parents=True)
        output = root / 'downloads'
        output.mkdir()
        path = output / '文稿.docx'
        doc = Document()
        doc.add_paragraph('https://example.com/video')
        doc.add_heading('测试标题', 0)
        doc.add_paragraph(app.NOTICE)
        doc.add_paragraph('全文末尾 <script>不能执行</script>')
        doc.save(path)
        (job / 'job.json').write_text(json.dumps({'document': str(path)}))
        return job, output, path

    def test_preview_contains_saved_text_and_notice(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            job, output, path = self.fixture(root)
            with patch.object(app, 'WORK', root / 'work'), patch.object(app, 'OUTPUT', output):
                page = app.preview_document(job.name).decode()
            self.assertIn('全文末尾 &lt;script&gt;不能执行&lt;/script&gt;', page)
            self.assertIn(app.NOTICE, page)
            self.assertIn('class=notice', page)
            self.assertNotIn('<script>', page)

    def test_reveal_exact_document_without_shell(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            job, output, path = self.fixture(root)
            with patch.object(app, 'WORK', root / 'work'), patch.object(app, 'OUTPUT', output), patch('app.subprocess.run') as run:
                run.return_value.returncode = 0
                app.reveal_document(job.name)
                run.assert_called_once_with(['/usr/bin/open', '-a', 'Finder', str(path.resolve().parent)], capture_output=True, text=True, timeout=15)
                path.unlink()
                with self.assertRaises(ValueError):
                    app.reveal_document(job.name)

    def test_queued_title_is_read_from_separate_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            job = root / 'jobs/123456abcdef'
            job.mkdir(parents=True)
            (job / 'job.json').write_text(json.dumps({'url': 'https://example.com/v', 'state': 'queued'}))
            (job / 'page-title.json').write_text(json.dumps({'title': '对话视频'}))
            with patch.object(app, 'WORK', root):
                items = app.list_jobs()
            self.assertEqual(items[0]['title'], '对话视频')
            self.assertEqual(items[0]['state'], 'queued')

    def test_title_lookup_does_not_overwrite_active_progress(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            job = root / 'jobs/123456abcdef'
            job.mkdir(parents=True)
            meta = {'url': 'https://example.com/v', 'state': 'transcribing', 'transcribed_seconds': 123}
            (job / 'job.json').write_text(json.dumps(meta))
            with patch.object(app, 'WORK', root), patch('app.subprocess.run') as run:
                run.return_value.returncode = 0
                run.return_value.stdout = '对话标题\n'
                app.fetch_title(job.name, meta['url'])
            self.assertEqual(json.loads((job / 'job.json').read_text()), meta)
            self.assertEqual(json.loads((job / 'page-title.json').read_text())['title'], '对话标题')


if __name__ == '__main__':
    unittest.main()
