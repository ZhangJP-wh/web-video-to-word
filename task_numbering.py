"""Persistent task IDs: deletion never releases a sequence number."""
import json,time
from pathlib import Path
from runtime_compat import file_lock as fcntl

def numbers(work):
    work=Path(work);work.mkdir(parents=True,exist_ok=True)
    with (work/'task-numbers.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        path=work/'task-numbers.json'
        ledger=json.loads(path.read_text()) if path.exists() else {'next':1,'tasks':{}}
        ledger.setdefault('created',{})
        pending=[]
        for record in (work/'jobs').glob('*/job.json'):
            meta=json.loads(record.read_text());stat=record.parent.stat()
            created=meta.get('created_at',getattr(stat,'st_birthtime',stat.st_mtime))
            ident=record.parent.name
            if ident in ledger['tasks'] and ledger['created'].get(ident,created)==created:
                ledger['created'][ident]=created;continue
            pending.append((created,ident))
        for created,ident in sorted(pending):
            ledger['created'][ident]=created
            ledger['tasks'][ident]=ledger['next'];ledger['next']+=1
        from reader import save_json
        save_json(path,ledger)
        return dict(ledger['tasks'])

def document_name(number,name):return f'{number} - {name}'

def migrate_documents(work,output):
    """Rename only recorded completed documents; never touch a running reader."""
    from reader import save_json,configure_folder_sort
    mapping=numbers(work);output=Path(output);renamed=[]
    for record in (Path(work)/'jobs').glob('*/job.json'):
        with (record.parent/'.prepare.lock').open('a') as lock:
            try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError:continue
            meta=json.loads(record.read_text())
            if meta.get('state')!='completed' or not meta.get('document'):continue
            old=Path(meta['document'])
            if old.parent.resolve()!=output.resolve() or not old.is_file() or old.is_symlink():continue
            new=output/(document_name(mapping[record.parent.name],meta['name'])+'.docx')
            if new!=old:
                if new.exists():raise ValueError('编号文稿名称已存在，未覆盖：'+new.name)
                old.rename(new);meta['document']=str(new);save_json(record,meta)
                save_json(record.parent/'export-target.json',{'path':str(new),'url':meta['url']})
                renamed.append(new.name)
    if output.exists():configure_folder_sort(output)
    return renamed
