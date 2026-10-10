"""One-time migration from local ASR to Qianwen; preserves jobs and documents."""
import json,shutil,subprocess,time
from pathlib import Path
from reader import ROOT,WORK,OUTPUT,save_json
from task_controls import reader_pids,stop_reader
OLD=OUTPUT.parent/'网页视频转语音识别文字稿'
def main():
    for folder in (WORK/'jobs').glob('*'):
        record=folder/'job.json'
        if not record.exists():continue
        meta=json.loads(record.read_text())
        if meta.get('engine')!='qianwen' and meta.get('state')!='completed':
            for pid in reader_pids(ROOT,folder):stop_reader(pid)
            meta.update(engine='qianwen',state='queued');meta.pop('error',None)
        if meta.get('document') and Path(meta['document']).parent==OLD:
            meta['document']=str(OUTPUT/Path(meta['document']).name)
        save_json(record,meta)
        reservation=folder/'export-target.json'
        if reservation.exists():
            value=json.loads(reservation.read_text())
            if Path(value['path']).parent==OLD:value['path']=str(OUTPUT/Path(value['path']).name);save_json(reservation,value)
        for item in folder.iterdir():
            if item.name.startswith('checkpoints-') or item.name=='speaker-turns.json':
                if item.is_dir():shutil.rmtree(item)
                else:item.unlink()
    if OLD.exists():
        if not OUTPUT.exists():OLD.rename(OUTPUT)
        else:
            for item in OLD.iterdir():
                dest=OUTPUT/item.name
                if dest.exists():raise RuntimeError('新旧目录有同名文件，已保留，请检查：'+item.name)
                item.rename(dest)
            OLD.rmdir()
    cache=WORK/'model-cache'
    size=sum(p.stat().st_size for p in cache.rglob('*') if p.is_file() and not p.is_symlink()) if cache.exists() else 0
    shutil.rmtree(cache,ignore_errors=True)
    from importlib.metadata import distributions
    from packaging.requirements import Requirement
    normalize=lambda value:value.lower().replace('_','-').replace('.','-')
    installed={normalize(d.metadata['Name']):d for d in distributions()}
    keep=set(); pending=['yt-dlp','python-docx','imageio-ffmpeg','send2trash','ds-store','playwright','pip','setuptools','packaging']
    while pending:
        name=normalize(pending.pop())
        if name in keep:continue
        keep.add(name)
        if name not in installed:continue
        for spec in installed[name].requires or []:
            requirement=Requirement(spec)
            if requirement.marker is None or any(requirement.marker.evaluate({'extra':extra}) for extra in ('','default')):pending.append(requirement.name)
    packages=sorted(set(installed)-keep)
    subprocess.run([str(ROOT/'.venv/bin/python'),'-m','pip','uninstall','-y',*packages],check=True)
    subprocess.run([str(ROOT/'.venv/bin/python'),'-m','pip','check'],check=True)
    save_json(WORK/'cloud-migration.json',{'ok':True,'removed_model_cache_bytes':size,'output':str(OUTPUT)})
    print('已移除本地模型及推理组件，文稿文件夹已更新。')
if __name__=='__main__':main()
