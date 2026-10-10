"""Stop one verified reader and move its local artifacts to the Trash."""
import json
import os
import re
import shlex
import signal
import subprocess
import time
from pathlib import Path


def reader_pids(root, folder):
    if os.name == 'nt':
        import psutil
        verified = []
        for process in psutil.process_iter(['pid', 'cmdline']):
            try:
                args = process.info['cmdline'] or []
                if len(args) >= 4 and Path(args[1]).resolve() == (root/'reader.py').resolve() and args[2] == 'prepare' and args[3] == json.loads((folder/'job.json').read_text(encoding='utf-8'))['url']:
                    verified.append(process.pid)
            except (psutil.NoSuchProcess, psutil.AccessDenied, OSError, ValueError):
                continue
        return verified
    result=subprocess.run(['/usr/sbin/lsof','-t',str(folder/'.prepare.lock')],capture_output=True,text=True)
    verified=[]
    for value in result.stdout.split():
        pid=int(value)
        command=subprocess.run(['/bin/ps','-p',str(pid),'-o','command='],capture_output=True,text=True)
        args=shlex.split(command.stdout.strip())
        if len(args)>=3 and args[1]==str(root/'reader.py') and args[2]=='prepare':verified.append(pid)
    return verified


def stop_reader(pid):
    if os.name == 'nt':
        import psutil
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            for process in reversed(children):
                try: process.terminate()
                except psutil.NoSuchProcess: pass
            parent.terminate()
            psutil.wait_procs(children + [parent], timeout=10)
        except psutil.NoSuchProcess:
            pass
        return
    children=subprocess.run(['/usr/bin/pgrep','-P',str(pid)],capture_output=True,text=True)
    for child in children.stdout.split():stop_reader(int(child))
    try:os.kill(pid,signal.SIGTERM)
    except ProcessLookupError:pass


def trash_task(root, work, output_roots, ident):
    from send2trash import send2trash
    from docx import Document
    from runtime_compat import file_lock as fcntl
    if not re.fullmatch('[0-9a-f]{12}',ident):raise ValueError('任务编号不合法')
    folder=work/'jobs'/ident
    if folder.is_symlink() or not folder.exists():raise ValueError('任务不存在')
    meta=json.loads((folder/'job.json').read_text(encoding="utf-8"))
    (folder/'.deleting').touch()
    for pid in reader_pids(root,folder):stop_reader(pid)
    # Do not remove files until the reader has actually relinquished ownership.
    with (folder/'.prepare.lock').open('a') as lock:
        deadline=time.monotonic()+15
        while True:
            try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);break
            except BlockingIOError:
                if time.monotonic()>deadline:
                    (folder/'.deleting').unlink(missing_ok=True)
                    raise ValueError('任务尚未停止，未删除文件。请稍后重试。')
                time.sleep(.2)
        meta=json.loads((folder/'job.json').read_text(encoding="utf-8"))
        candidates=set()
        owned=set()
        reservation=folder/'export-target.json'
        if reservation.exists():
            record=json.loads(reservation.read_text(encoding="utf-8"))
            if record.get('url')==meta.get('url'):
                target=Path(record['path'])
                owned.update([target,target.with_suffix('.partial.docx')])
                candidates.update(owned)
        if meta.get('document'):
            candidates.add(Path(meta['document']));owned.add(Path(meta['document']))
        name=meta.get('name')
        if name:
            for base in output_roots:
                for suffix in ('.docx','.partial.docx'):
                    candidates.add(base/(name+suffix))
                    candidates.add(base/(name+' ('+ident+')'+suffix))
        for path in candidates:
            if path.exists() and (path.is_symlink() or not any(base.resolve() in path.resolve().parents for base in output_roots)):
                raise ValueError('文稿路径不属于工具输出目录，未删除任务')
        for path in candidates:
            if not path.exists():continue
            if path.is_symlink() or not any(base.resolve() in path.resolve().parents for base in output_roots):
                raise ValueError('文稿路径不属于工具输出目录，未删除任务')
            try:
                paragraphs=Document(path).paragraphs
                belongs=path in owned or bool(paragraphs and paragraphs[0].text==meta.get('url'))
            except Exception:
                # An incomplete file is owned only if it was explicitly recorded.
                belongs=str(path)==meta.get('document') or path in owned
                if not belongs and path.suffix=='.docx' and '.partial' in path.name:
                    raise ValueError('无法确认未完成文稿的归属，已保留文件，请检查')
            if belongs:send2trash(str(path.resolve()))
        for base in output_roots[1:]:
            legacy=base/ident
            if legacy.is_dir() and not legacy.is_symlink():send2trash(str(legacy.resolve()))
        # Windows cannot recycle a directory containing an open lock handle.
        if os.name == 'nt':
            fcntl.flock(lock, fcntl.LOCK_UN)
            lock.close()
        send2trash(str(folder.resolve()))
    return {'ok':True,'message':'本机任务与相关文件已移入废纸篓。千问云端记录需在千问网页中管理。'}
