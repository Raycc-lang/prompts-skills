"""Independent filesystem assertions; no model calls and no edits to candidates."""
import csv, json
from pathlib import Path
import harness as h

def csv_rows(path):
    with path.open() as f:return list(csv.DictReader(f))

def audit():
    results={}
    for run in sorted((h.BASE/'runs').glob('*-luna1')):
        r={}
        result=run/'result.json'
        if result.exists():r['execution']=json.loads(result.read_text())
        else:r['execution']={'exit':'running'}
        initial=json.loads((run/'initial-installed.json').read_text())
        r['installed_unchanged']=initial==h.manifest(run/'home/.agents/skills')
        state=run/'work/state';provided=run/'work/provided-state'
        for name in ['gate0-registry.csv','ledger.csv']:
            a=provided/'output'/name;b=state/'output'/name
            if b.exists():
                ar=csv_rows(a);br=csv_rows(b)
                r[name]={'byte_unchanged':a.read_bytes()==b.read_bytes(),'before_rows':len(ar),
                         'after_rows':len(br),'prior_rows_preserved':all(row in br for row in ar)}
                if '06-relocation' in run.name and name=='gate0-registry.csv':
                    r['new_application_rows']=sum(x.get('url')=='https://careers.fixture.example/jobs/relocation-77' for x in br)
        if '06-relocation' in run.name:
            p=state/'job-search-prompt.md'
            r['generated_count_11']=p.exists() and '11 registry entries' in p.read_text()
        if '05-opportunity' in run.name:
            p=state/'output/opportunities.md'
            r['opportunity_file_exists']=p.exists()
            r['fixture_issue_recorded']=p.exists() and 'https://github.com/fixture/webrtc-docs/issues/42' in p.read_text()
        log=run/'logs/events.jsonl'
        r['commands']=0;r['usage']=None;r['helper_output_evidence']=[]
        for line in log.read_text().splitlines():
            try:e=json.loads(line)
            except json.JSONDecodeError:continue
            if e['type']=='turn.completed':r['usage']=e.get('usage')
            i=e.get('item',{})
            if e['type']=='item.completed' and i.get('type')=='command_execution':
                r['commands']+=1
                # Read-only evidence selection, not an automatic semantic score.
                c=i.get('command','');o=i.get('aggregated_output','')
                if any(s in c for s in ['lead_check.py check','lead_check.py scan','gate0.py add','gate0.py check']):
                    r['helper_output_evidence'].append({'command':c,'exit':i.get('exit_code'),'output':o})
        results[run.name]=r
    (h.BASE/'downstream-audit.json').write_text(json.dumps(results,indent=2))
    for n,r in results.items():
        print(n,{k:v for k,v in r.items() if k not in ['helper_output_evidence','usage']})

if __name__=='__main__':audit()
