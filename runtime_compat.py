"""Small platform boundary for Windows 11 x64 and native Apple Silicon Mac."""
import os
from pathlib import Path

IS_WINDOWS = os.name == "nt"


def venv_python(root):
    return Path(root) / '.venv' / ('Scripts/python.exe' if IS_WINDOWS else 'bin/python')


class FileLock:
    LOCK_EX, LOCK_NB, LOCK_UN = 1, 2, 4

    @staticmethod
    def flock(handle, flags):
        import portalocker
        if flags & FileLock.LOCK_UN:
            portalocker.unlock(handle)
            return
        mode = portalocker.LOCK_EX
        if flags & FileLock.LOCK_NB:
            mode |= portalocker.LOCK_NB
        try:
            portalocker.lock(handle, mode)
        except portalocker.exceptions.LockException as error:
            raise BlockingIOError('文件正在被其他进程使用') from error


# Preserve existing Mac flock behavior and interoperability with running versions.
if IS_WINDOWS:
    file_lock = FileLock
else:
    import fcntl as file_lock
