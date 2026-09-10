"""Run fixed downstream cases in paired isolated environments, then summarize logs."""
import concurrent.futures, json, sys
from pathlib import Path
import cases, harness as h

def run_all(suffix=''):
    names=sorted(p.stem for p in (h.BASE/'evaluation').glob('0*.txt'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for case in names:
            futures={pool.submit(cases.runner,candidate,case,suffix):candidate for candidate in ['candidate-p','candidate-q']}
            for f in concurrent.futures.as_completed(futures):
                try:f.result()
                except Exception as e:print('HARNESS ERROR',futures[f],repr(e),flush=True)
            for candidate in ['candidate-p','candidate-q']:
                log=h.BASE/'runs'/(candidate+'-'+case+suffix)/'logs/events.jsonl'
                if log.exists() and 'hit your usage limit' in log.read_text():
                    print('Stopped remaining pairs: account quota interruption.',flush=True);return

def summarize():
    out={}
    for run in sorted((h.BASE/'runs').iterdir()):
        result=json.loads((run/'result.json').read_text()) if (run/'result.json').exists() else {'exit':'running'}
        result['commands']=0;result['usage']=[];result['errors']=[]
        log=run/'logs/events.jsonl'
        if log.exists():
            for line in log.read_text().splitlines():
                try:e=json.loads(line)
                except json.JSONDecodeError:continue
                if e['type']=='item.completed' and e.get('item',{}).get('type')=='command_execution':result['commands']+=1
                if e['type']=='turn.completed':result['usage'].append(e.get('usage'))
                if e['type'] in ['error','turn.failed']:result['errors'].append(e)
        for field,root in [('installed','home/.agents/skills'),('deliverable','work/deliverable')]:
            p=run/root
            if p.exists():
                files=[x for x in p.rglob('*') if x.is_file()]
                result[field]={'files':len(files),'bytes':sum(x.stat().st_size for x in files),
                               'entrypoints':[str(x.relative_to(p)) for x in files if x.name=='SKILL.md']}
        out[run.name]=result
    (h.BASE/'results-summary.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    if sys.argv[1]=='run':run_all(sys.argv[2] if len(sys.argv)>2 else '')
    else:summarize()
