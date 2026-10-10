"""Installer safety and recovery regressions; no network/login in unit tests."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import install


class InstallerTests(unittest.TestCase):
    def test_platform_rejected_before_commands(self):
        with patch.object(install.platform, 'system', return_value='Linux'), patch.object(install, 'run') as run:
            with self.assertRaisesRegex(RuntimeError, 'macOS'):
                install.main([])
            run.assert_not_called()

    def test_wrong_node_version_or_arch_rejected(self):
        for version, arch in [('20.0.0', 'arm64'), ('22.0.0', 'x64')]:
            with self.subTest(version=version, arch=arch), patch.object(install.platform, 'system', return_value='Darwin'), patch.object(install.platform, 'machine', return_value='arm64'), patch.object(install.sys, 'version_info', (3,12)), patch.object(install.shutil, 'which', return_value='/node'), patch.object(install.subprocess, 'check_output', return_value=json.dumps(dict(version=version, arch=arch))):
                with self.assertRaisesRegex(RuntimeError, 'Node.js 22'):
                    install.check_environment()

    def test_broken_venv_preserved_and_rebuilt(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(install, 'ROOT', Path(tmp)), patch.object(install, 'run') as run:
            folder = Path(tmp) / '.venv'
            folder.mkdir()
            (folder / 'marker').write_text('preserve')
            install.ensure_venv()
            backups = list(Path(tmp).glob('.venv.backup-*'))
            self.assertEqual(len(backups), 1)
            self.assertEqual((backups[0] / 'marker').read_text(), 'preserve')
            self.assertEqual(run.call_args.args[0][-2:], ['venv', folder])

    def test_healthy_venv_reused(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(install, 'ROOT', Path(tmp)), patch.object(install, 'run') as run:
            python = Path(tmp) / '.venv/bin/python'
            python.parent.mkdir(parents=True)
            python.touch()
            info = [[3,12], 'arm64', str(Path(tmp)/'.venv'), '/base']
            with patch.object(install.subprocess, 'check_output', return_value=json.dumps(info)):
                self.assertEqual(install.ensure_venv(), python)
            run.assert_not_called()

    def test_symlink_environment_not_modified(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(install, 'ROOT', Path(tmp)), patch.object(install, 'run') as run:
            (Path(tmp)/'.venv').symlink_to(Path(tmp)/'other')
            with self.assertRaisesRegex(RuntimeError, '符号链接'):
                install.ensure_venv()
            run.assert_not_called()

    def test_foreign_service_never_started_or_stopped(self):
        with patch.object(install, 'health', return_value={'ok':True,'project':'/other','engines':['qianwen']}), patch.object(install.subprocess, 'Popen') as popen:
            with self.assertRaisesRegex(RuntimeError, '不是本目录'):
                install.start_service(Path('/python'), 8767)
            popen.assert_not_called()

    def test_same_service_reused(self):
        with patch.object(install, 'health', return_value={'ok':True,'project':str(install.ROOT),'engines':['qianwen']}), patch.object(install.subprocess, 'Popen') as popen:
            install.start_service(Path('/python'), 8767)
            popen.assert_not_called()

    def test_health_requires_cloud_only(self):
        for data in ([], {'ok':False,'project':str(install.ROOT),'engines':['qianwen']}, {'ok':True,'project':str(install.ROOT),'engines':['local']}):
            with self.assertRaises(RuntimeError):
                install.validate_health(data)

    def test_failed_dependency_stops_before_start(self):
        with patch.object(install, 'check_environment'), patch.object(install, 'ensure_venv', return_value=Path('/python')), patch.object(install, 'run', side_effect=subprocess.CalledProcessError(1, 'pip')), patch.object(install, 'start_service') as start:
            with self.assertRaises(subprocess.CalledProcessError):
                install.main([])
            start.assert_not_called()

    def test_no_start_runs_all_acceptance_steps(self):
        with patch.object(install, 'check_environment'), patch.object(install, 'ensure_venv', return_value=Path('/python')), patch.object(install, 'run') as run, patch.object(install, 'start_service') as start:
            install.main(['--no-start'])
            commands = [list(map(str,c.args[0])) for c in run.call_args_list]
            self.assertTrue(any(c[1:]==['-m','pip','check'] for c in commands))
            self.assertTrue(any(c[1:]==['-m','playwright','install','chromium'] for c in commands))
            self.assertTrue(any('unittest' in c and all(t in c for t in install.TESTS) for c in commands))
            start.assert_not_called()

if __name__ == '__main__':
    unittest.main()
