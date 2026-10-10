"""Run the independent cloud workflow from the normal Mac environment."""
import hashlib
import json
import subprocess
import time
from pathlib import Path
import reader
from qianwen_browser import export_audio


def main():
    result={'passed':False,'started_at':time.time()}
    ident=hashlib.sha256(b'qianwen-smoke-test-20-seconds-v2').hexdigest()[:12]
    job=reader.WORK/'jobs'/ident
    (job/'media').mkdir(parents=True,exist_ok=True)
    meta={'url':'',
          'title':'千问独立后台完整测试（仅20秒片段）','name':'千问独立后台完整测试（仅20秒片段）',
          'audio_duration':20,'engine':'qianwen','state':'cloud_transcribing',
          'created_at':time.time()}
    existing=job/'job.json'
    if existing.exists():
        previous=json.loads(existing.read_text())
        for key in ('qianwen_submitted','qianwen_url'): 
            if key in previous:meta[key]=previous[key]
    try:
        candidates=[]
        for other in (reader.WORK/'jobs').glob('*/job.json'):
            data=json.loads(other.read_text())
            audio=Path(data.get('audio','/nonexistent'))
            if other.parent!=job and audio.is_file():candidates.append((other.stat().st_mtime,audio,data))
        if not candidates:
            raise ValueError('测试用的已下载音轨不存在，请让 Codex 选择其他测试音轨。')
        _,source,source_meta=max(candidates,key=lambda item:item[0])
        meta['url']=source_meta['url']
        clip=job/'media'/'test-20-seconds.wav'
        subprocess.run([reader.ffmpeg(),'-nostdin','-v','error','-y','-i',str(source),
                        '-t','20',str(clip)],check=True)
        meta.update(audio=str(clip),media=str(clip))
        reader.save_json(existing,meta)
        print('正在无窗口浏览器中上传20秒测试片段、等待千问转写并导出Word……',flush=True)
        raw=export_audio(clip,job,meta,reader.save_json)
        reader.save_json(job/'raw-transcript.json',raw)
        reader.save_json(existing,meta)
        document=reader.build_document(job,raw)
        result.update(passed=True,document=str(document),elapsed_seconds=round(time.time()-result['started_at'],2),segments=len(raw['segments']))
        print('独立后台完整流程测试通过。Word：'+str(document),flush=True)
    except Exception as error:
        result['error']=str(error)
        # Retain current cloud task identity for a safe retry.
        current=json.loads(existing.read_text()) if existing.exists() else meta
        current.update(state='failed',error=str(error))
        reader.save_json(existing,current)
        print('测试未通过：'+str(error),flush=True)
    finally:
        reader.save_json(reader.WORK/'qianwen-smoke-test.json',result)
    return 0 if result['passed'] else 1


if __name__=='__main__':raise SystemExit(main())
