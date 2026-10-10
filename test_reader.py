import argparse
import hashlib
import json
import tempfile
import unittest
import wave
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from docx import Document
import reader


def reader_audio_duration(wav):
    with wave.open(str(wav)) as audio:
        return audio.getnframes() / audio.getframerate()


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.work = root / 'work'
        self.output = root / 'Downloads'
        (self.work / 'jobs').mkdir(parents=True)
        for name, value in [('WORK', self.work), ('OUTPUT', self.output)]:
            p = patch.object(reader, name, value)
            p.start()
            self.addCleanup(p.stop)
        self.addCleanup(self.temp.cleanup)
        self.trash = Path(self.temp.name) / 'trash'; self.trash.mkdir()
        p = patch('send2trash.send2trash', side_effect=lambda name: Path(name).rename(self.trash / Path(name).name))
        self.trash_mock = p.start(); self.addCleanup(p.stop)

    def fixture(self, seconds=1):
        url = 'https://example.com/video'
        job = self.work / 'jobs' / hashlib.sha256(url.encode()).hexdigest()[:12]
        job.mkdir(exist_ok=True)
        audio = job / 'transcription-audio.wav'
        with wave.open(str(audio), 'wb') as a:
            a.setnchannels(1); a.setsampwidth(2); a.setframerate(16000)
            a.writeframes(b'\0' * (seconds * 16000 * 2))
        meta = {'url': url, 'title': '测试标题', 'name': '测试标题', 'media': str(audio),
                'audio': str(audio), 'duration': seconds, 'state': 'downloaded'}
        reader.save_json(job / 'job.json', meta)
        return job, meta, audio

    def test_automatic_word_generation_and_cleanup(self):
        job, meta, audio = self.fixture()
        raw={'model':'qianwen-web','segments':[{'start':0,'end':1,'speaker':'发言人 1','text':'完整识别文字 80%。'}]}
        with patch('qianwen_browser.export_audio',return_value=raw), patch.object(reader,'ffmpeg',return_value='/unused'):
            reader.prepare(argparse.Namespace(url=meta['url'],cookies_browser=None,engine='qianwen'))
        saved = json.loads((job / 'job.json').read_text(encoding="utf-8"))
        self.assertEqual(saved['state'], 'completed')
        doc = Document(saved['document'])
        texts = [p.text for p in doc.paragraphs]
        self.assertEqual(texts[0], meta['url'])
        self.assertIn(reader.NOTICE, texts)
        self.assertIn('完整识别文字 80%。', texts)
        warning = next(p for p in doc.paragraphs if p.text == reader.NOTICE)
        self.assertTrue(warning.runs[0].bold)
        self.assertIsNotNone(warning.runs[0].font.highlight_color)
        self.assertNotIn('ChatGPT 总结', texts)
        self.assertEqual(Path(saved['document']).name, '1 - 测试标题.docx')
        self.assertFalse(audio.exists())
        self.assertTrue((self.trash / audio.name).exists())
        self.assertEqual(Path(saved['document']).parent, self.output)
        self.assertIn('[00:00:00–00:00:01] 发言人 1', texts)
        self.assertFalse(list(job.glob('checkpoints-*')))
        self.assertFalse((job / 'ChatGPT校对任务.txt').exists())
        self.assertTrue(saved['temporary_files_removed'])

    def test_local_upload_pipeline_preserves_user_original(self):
        import io, app, shutil
        original=Path(self.temp.name)/'我的录音.wav'
        with wave.open(str(original),'wb') as a:
            a.setnchannels(1);a.setsampwidth(2);a.setframerate(16000);a.writeframes(b'\0'*32000)
        with patch.object(app,'WORK',self.work),patch.object(app,'enqueue',side_effect=lambda url: __import__('hashlib').sha256(url.encode()).hexdigest()[:12]):
            ident=app.receive_upload(io.BytesIO(original.read_bytes()),original.stat().st_size,original.name)
        job=self.work/'jobs'/ident;meta=json.loads((job/'job.json').read_text(encoding="utf-8"))
        raw={'model':'qianwen-web','segments':[{'start':0,'end':1,'speaker':'发言人 1','text':'本地文件全部原文'}]}
        with patch('qianwen_browser.export_audio',return_value=raw),patch.object(reader,'ffmpeg',return_value='/unused'),patch.object(reader,'extract_audio',side_effect=lambda ff,src,dst:shutil.copy2(src,dst)):
            reader.prepare(argparse.Namespace(url=meta['url'],cookies_browser=None,engine='qianwen'))
        saved=json.loads((job/'job.json').read_text(encoding="utf-8"));texts=[p.text for p in Document(saved['document']).paragraphs]
        self.assertEqual(saved['state'],'completed')
        self.assertEqual(texts[0],'本地上传文件：我的录音.wav')
        self.assertEqual(Path(saved['document']).name,'1 - 我的录音.docx')
        self.assertIn('[00:00:00–00:00:01] 发言人 1',texts)
        self.assertTrue(original.exists());self.assertFalse(Path(meta['media']).exists())

    def test_speaker_changes_keep_separate_timestamps(self):
        job, meta, audio = self.fixture(4)
        raw = {'segments': [
            {'start': 0, 'end': 2, 'speaker': '发言人 1', 'text': '第一人发言'},
            {'start': 2, 'end': 4, 'speaker': '发言人 2', 'text': '第二人发言'}]}
        reader.save_json(job / 'raw-transcript.json', raw)
        path = reader.build_document(job, raw)
        texts = [p.text for p in Document(path).paragraphs]
        self.assertIn('[00:00:00–00:00:02] 发言人 1', texts)
        self.assertIn('[00:00:02–00:00:04] 发言人 2', texts)
        self.assertIn('第一人发言', texts)
        self.assertIn('第二人发言', texts)

    def test_empty_result_preserves_media(self):
        job, meta, audio = self.fixture()
        with self.assertRaises(ValueError):
            reader.build_document(job, {'segments': []})
        self.assertTrue(audio.exists())

    def test_modified_word_blocks_cleanup(self):
        job, meta, audio = self.fixture()
        raw = {'segments': [{'start': 0, 'end': 1, 'text': '原文'}]}
        reader.save_json(job / 'raw-transcript.json', raw)
        path = reader.build_document(job, raw)
        audio.write_bytes(b'retained')
        path.write_bytes(path.read_bytes() + b'changed')
        meta = json.loads((job / 'job.json').read_text(encoding="utf-8"))
        with self.assertRaises(ValueError):
            reader.clear_intermediate(job, meta)
        self.assertTrue(audio.exists())


if __name__ == '__main__':
    unittest.main()

class AudioExtractionTests(unittest.TestCase):
    def test_real_silent_video_gives_readable_error_and_preserves_source(self):
        import subprocess,imageio_ffmpeg
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);source=folder/'silent.mp4';target=folder/'temporary.wav'
            executable=imageio_ffmpeg.get_ffmpeg_exe()
            subprocess.run([executable,'-v','error','-f','lavfi','-i','color=size=16x16:rate=1','-t','1','-an',str(source)],check=True)
            with self.assertRaisesRegex(ValueError,'没有音轨'):
                reader.extract_audio(executable,source,target)
            self.assertTrue(source.exists());self.assertFalse(target.exists())

    def test_real_audio_extracts_readable_wave(self):
        import subprocess,imageio_ffmpeg
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);source=folder/'sound.wav';target=folder/'temporary.wav'
            executable=imageio_ffmpeg.get_ffmpeg_exe()
            subprocess.run([executable,'-v','error','-f','lavfi','-i','sine=frequency=440:duration=1',str(source)],check=True)
            reader.extract_audio(executable,source,target)
            with wave.open(str(target)) as audio:
                self.assertEqual(audio.getframerate(),16000)
                self.assertEqual(audio.getnchannels(),1)
                self.assertGreater(audio.getnframes(),0)

class DownloadLinkTests(unittest.TestCase):
    def test_douyin_selected_video_is_normalized(self):
        source='https://www.douyin.com/jingxuan?modal_id=7689068026368380196'
        self.assertEqual(reader.download_url(source),'https://www.douyin.com/video/7689068026368380196')
    def test_other_site_modal_parameter_is_untouched(self):
        source='https://example.com/jingxuan?modal_id=123'
        self.assertEqual(reader.download_url(source),source)
    def test_invalid_douyin_id_is_untouched(self):
        source='https://www.douyin.com/jingxuan?modal_id=invalid'
        self.assertEqual(reader.download_url(source),source)

class CloudCleanupTests(PipelineTests):
    def exported(self):
        job,meta,audio=self.fixture()
        meta['qianwen_url']='https://www.qianwen.com/test'
        reader.save_json(job/'job.json',meta)
        raw={'segments':[{'start':0,'end':1,'speaker':'发言人 1','text':'完整文字'}]}
        reader.save_json(job/'raw-transcript.json',raw)
        return job,meta,raw

    def test_delete_only_after_word_is_saved_and_validated(self):
        job,meta,raw=self.exported()
        def deleted(folder):
            saved=json.loads((folder/'job.json').read_text())
            self.assertTrue(Path(saved['document']).is_file())
            self.assertTrue((folder/'validation.json').is_file())
            saved.update(qianwen_cloud_deleted=True,qianwen_delete_resolved=True)
            reader.save_json(folder/'job.json',saved)
        with patch('qianwen_browser.delete_cloud',side_effect=deleted) as delete:
            path=reader.build_document(job,raw)
        delete.assert_called_once_with(job.resolve())
        saved=json.loads((job/'job.json').read_text())
        self.assertEqual(saved['cloud_cleanup_state'],'completed');self.assertTrue(path.exists())

    def test_cloud_failure_keeps_completed_word(self):
        job,meta,raw=self.exported()
        with patch('qianwen_browser.delete_cloud',side_effect=RuntimeError('登录失效')):
            path=reader.build_document(job,raw)
        saved=json.loads((job/'job.json').read_text())
        self.assertEqual(saved['state'],'completed');self.assertEqual(saved['cloud_cleanup_state'],'failed');self.assertTrue(path.exists())

    def test_invalid_word_never_deletes_cloud(self):
        job,meta,raw=self.exported()
        with patch.object(reader,'verify_document',side_effect=ValueError('损坏')),patch('qianwen_browser.delete_cloud') as delete:
            with self.assertRaises(ValueError):reader.build_document(job,raw)
        delete.assert_not_called()
