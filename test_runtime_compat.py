import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import install
import reader
import runtime_compat


class CompatibilityTests(unittest.TestCase):
    def test_venv_layout(self):
        with patch.object(runtime_compat, 'IS_WINDOWS', True):
            self.assertTrue(runtime_compat.venv_python('/tmp').parts[-2:] == ('Scripts','python.exe'))
        with patch.object(runtime_compat, 'IS_WINDOWS', False):
            self.assertTrue(runtime_compat.venv_python('/tmp').parts[-2:] == ('bin','python'))

    def test_lock_excludes_another_process(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'lock'
            with path.open('a') as handle:
                runtime_compat.file_lock.flock(handle, runtime_compat.file_lock.LOCK_EX | runtime_compat.file_lock.LOCK_NB)
                code = "from runtime_compat import file_lock as f; import sys\nh=open(sys.argv[1],'a')\ntry: f.flock(h,f.LOCK_EX|f.LOCK_NB)\nexcept BlockingIOError: sys.exit(0)\nsys.exit(1)"
                result=subprocess.run([sys.executable,'-c',code,str(path)],capture_output=True,text=True)
                self.assertEqual(result.returncode,0,result.stderr)

    def test_windows_environment(self):
        with patch.object(install.platform,'system',return_value='Windows'), patch.object(install.platform,'machine',return_value='AMD64'), patch.object(install.sys,'version_info',(3,12)), patch.object(install.sys,'getwindowsversion',create=True,return_value=MagicMock(build=22631,product_type=1)), patch.object(install.shutil,'which',return_value='node.exe'), patch.object(install.subprocess,'check_output',return_value=json.dumps({'version':'24.0.0','arch':'x64'})):
            install.check_environment()

    def test_windows_service_redirector_identity(self):
        fake = MagicMock()
        process = fake.Process.return_value
        process.parents.return_value = [MagicMock(pid=123)]
        process.cmdline.return_value = ['python.exe', str(install.ROOT/'app.py')]
        process.cwd.return_value = str(install.ROOT)
        with patch.object(install.platform,'system',return_value='Windows'), patch.dict(sys.modules, {'psutil':fake}):
            self.assertTrue(install.started_service_matches(456,123))
            process.cmdline.return_value = ['python.exe', str(install.ROOT/'other.py')]
            self.assertFalse(install.started_service_matches(456,123))
            process.cmdline.return_value = ['python.exe', str(install.ROOT/'app.py')]
            process.parents.return_value = [MagicMock(pid=999)]
            self.assertFalse(install.started_service_matches(456,123))

    def test_windows_10_rejected_before_dependency_install(self):
        with patch.object(install.platform,'system',return_value='Windows'), patch.object(install.platform,'machine',return_value='AMD64'), patch.object(install.sys,'getwindowsversion',create=True,return_value=MagicMock(build=19045,product_type=1)), patch.object(install,'run') as run:
            with self.assertRaisesRegex(RuntimeError,'Windows 11'):
                install.check_environment()
            run.assert_not_called()

    def test_windows_arm_rejected(self):
        with patch.object(install.platform,'system',return_value='Windows'), patch.object(install.platform,'machine',return_value='ARM64'):
            with self.assertRaises(RuntimeError):install.check_environment()

    def test_reserved_filename(self):
        for name in ['CON','nul.txt','COM1','LPT9.docx']:
            self.assertTrue(reader.filename(name).startswith('_'))
        self.assertEqual(reader.filename('普通标题'),'普通标题')

    def test_windows_ffmpeg_uses_copy_not_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); source=root/'original.exe';source.write_bytes(b'ffmpeg')
            with patch.object(reader,'WORK',root), patch.object(reader,'IS_WINDOWS',True), patch('imageio_ffmpeg.get_ffmpeg_exe',return_value=str(source)):
                target=Path(reader.ffmpeg())
                self.assertEqual(target.name,'ffmpeg.exe')
                self.assertFalse(target.is_symlink())
                self.assertEqual(target.read_bytes(),b'ffmpeg')

if __name__ == '__main__':unittest.main()
