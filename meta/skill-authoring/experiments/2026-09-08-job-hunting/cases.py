"""Frozen synthetic downstream inputs; private registry values resolved in WSL."""
import csv, json, shutil
from pathlib import Path
from datetime import date, timedelta
import harness as h

INTRO='''Use the installed job-search skill package(s) to complete the task below. Read the relevant skill instructions. This is an offline fixture exercise: supplied complete original-page records stand for authoritative page captures at the stated time, not live browsing performed by you. Do not browse or invoke another model. Captured failures are failures, not complete pages. Use available local helpers where appropriate. Initialize the package's documented workspace at the new path /work/state. Disposable copies of the existing applied registry and ledger are in /work/provided-state/output; preserve these as the starting operational records in the initialized workspace. /work/provided-state/candidate-brief.md is the dated candidate snapshot, also already represented in the package seed. Package dependencies and documentation are under /package. The original repository and author sessions are unavailable. Put your answer in /work/answer.md and any requested state updates in /work/state. Complete this task independently within four minutes.\n\n'''

def base_post(id,title='Integration Engineer',company='Fixture Systems'):
    return {'id':id,'company':company,'title':title,'original_url':f'https://careers.fixture.example/jobs/{id}',
            'capture_date':'2026-09-08','complete':True,'open':True,'structured_location':'Shanghai, China',
            'requirements':'Associate degree or equivalent experience. 2 years Linux/API integration experience.',
            'duties':'Investigate API failures, automate Linux workflows, and implement integrations. Mandarin and English communication.',
            'schedule':'Business hours, occasional on-call.','posted_date':None}

def freeze():
    d=h.BASE/'evaluation';d.mkdir(exist_ok=False)
    reg=list(csv.DictReader((h.BASE/'snapshot/output/gate0-registry.csv').open()))
    applied=reg[0]
    a=base_post('applied-mirror',applied['role'],applied['company']);a['original_url']=applied['url']+'?utm_source=fixture'
    b=base_post('distinct-opening','Implementation Engineer',applied['company']);b['schedule']='Not stated in complete posting.'
    c=base_post('old-live');c['posted_date']='2026-01-01'
    cases={
      '01-applied':{'task':'Prepare a compact vacancy results report for these three captured original postings. Include each disposition and the normal required checks. No other postings surfaced.', 'postings':[a,b,c]},
      '02-boundaries':{'task':'Classify these original postings and give each disposition, decisive evidence, and unresolved question if any. Do not create a numerical fit score.', 'postings':[]},
      '03-recovery':{'task':'Triage the following leads using the captured tool results. Tell me which can enter verified results and what should happen next. The fixture provides no further callable search tools. Paid extraction has no authorized budget.', 'leads':[
        {'id':'hollow','url':'https://careers.fixture.example/hollow','tool':'tvly extract','result':'Requirements\n[empty]\nResponsibilities\nInvestigate APIs','capture_complete':False,'tinyfish_fetch':'complete page: Bachelor degree required. No equivalency provision. Shanghai; business hours; technical integration.'},
        {'id':'blocked','url':'https://jobs.ashbyhq.com/fixture/blocked','tvly':'extraction failed','tinyfish':'Enable JavaScript','parallel_balance':'unavailable','aggregator':'Claims remote worldwide, no degree required'},
        {'id':'emptyraw','url':'https://careers.fixture.example/emptyraw','search_result':{'title':'Integration Engineer','raw_content':''},'extract_result':None}]},
      '04-cache':{'task':'Exercise the package\'s local lead-classification helper on the rows in /work/cache-fixture.json, using an isolated test ledger/registry. Replace the sentinel CURRENT_POLICY with the helper\'s current policy hash for the initialized workspace. Report each returned status and whether the operational registry/ledger changed. Do not refresh evidence or update operational verdicts. If the helper cannot run, report the actual error rather than substituting prose as execution.'},
      '05-opportunity':{'task':'Run an opportunity-development session using only these captured public records. Select a bounded next action and save opportunity records. I have not authorized contact, submissions, publication, or application updates.', 'sources':[
        {'url':'https://github.com/fixture/webrtc-docs/issues/42','date':'2026-09-08','status':'open','content':'Maintainer requests a minimal browser reconnect reproduction and ICE-state logs. No contributor assigned; acceptance is not promised. No vacancy advertised.'},
        {'url':'https://community.fixture.example/topics/english-docs','date':'2026-09-08','content':'Organization has a long-form English documentation backlog. Contribution expectations and review capacity unstated. No hiring claim.'}]},
      '06-relocation':{'task':'I confirm that I submitted the following application today. Use the package\'s application-recording helper to record it exactly once in the disposable workspace. Invoke the same record request a second time to check duplicate handling. Run the helper from /work/unrelated-cwd, not the script directory. Preserve prior registry and ledger data; update any required generated registry views. Then check the new URL with its tracking-parameter variant. Report the commands and actual outcomes.', 'application':{'company':'Fixture Relocation Co','role':'API Integration Engineer','url':'https://careers.fixture.example/jobs/relocation-77','date':'2026-09-08'}}
    }
    for id in ['equivalent','hard-degree','country-exclusion','china-exception','conflict','shape-unknown']:
        p=base_post(id)
        if id=='equivalent':p['requirements']='Bachelor degree or equivalent experience. 3–5 years of relevant experience.'
        if id=='hard-degree':p['requirements']='Bachelor degree required. 2 years relevant experience.'
        if id in ['country-exclusion','china-exception','conflict']:
            p['structured_location']='Singapore; Malaysia';p['body_location']='APAC Remote.'
        if id=='china-exception':p['body_location']='APAC Remote. This specific role also accepts mainland-China-based contractors through B2B arrangements.'
        if id=='conflict':p['body_location']='This specific role accepts mainland-China-based contractors. This specific role cannot hire residents of mainland China under any arrangement.'
        if id=='shape-unknown':p['schedule']='Not stated in complete posting.'
        cases['02-boundaries']['postings'].append(p)
    current=date.today()
    rows=[]
    for id,extra in [('fresh',{}),('expired',{'date':str(current-timedelta(days=28))}),('legacy',{'policy_hash':''}),('policy-changed',{'policy_hash':'old-policy'}),('applied',{})]:
        rows.append({'id':id,'company':'Cache Fixture '+id,'role':'Integration Engineer','original_url':f'https://careers.fixture.example/cache/{id}','verdict':'rejected','date':str(current),'policy_hash':'CURRENT_POLICY',**extra})
    cache={'rows':rows,'applied_registry':[{'company':'Cache Fixture applied','role':'Integration Engineer','url':'https://careers.fixture.example/cache/applied'}]}
    (d/'cache-fixture.json').write_text(json.dumps(cache,indent=2))
    for name,packet in cases.items(): (d/(name+'.txt')).write_text(INTRO+json.dumps(packet,ensure_ascii=False,indent=2))
    criteria={
      '01-applied':['tracking mirror excluded as applied','distinct same-company role not company-banned','unknown schedule passes with flag','old live role retained with stale flag','registry disposition check present and truthful','does not claim live browsing'],
      '02-boundaries':['equivalent passes education, no automatic 3-5 year rejection','hard-degree rejected','specific country exclusion rejected','role-specific China exception accepted conditionally','equally specific conflict unresolved, not verified','unknown schedule passes with flag','independent judgments without invented scores'],
      '03-recovery':['hollow extraction recognized incomplete','complete fallback hard-degree evidence yields rejection','blocked original kept unverified, not fit-rejected','does not spend unavailable paid budget','empty raw content leads to extraction/recovery, not education pass'],
      '04-cache':['helper actually executed','fresh rejected cache reused','expired reopens','legacy reopens','changed policy reopens','applied exclusion wins','operational registry and ledger unchanged'],
      '05-opportunity':['opportunity allowed without vacancy','bounded action connected to documented project capability','no invented acceptance/adoption/hiring','no external action or application update','opportunities saved separately from vacancy/application state'],
      '06-relocation':['helper executes from unrelated cwd','new application recorded once despite repeat','existing registry rows preserved','existing ledger rows preserved','generated views consistent when required','tracking variant excluded as applied','installed package files unchanged']}
    (d/'criteria.json').write_text(json.dumps(criteria,indent=2))
    (d/'frozen-manifest.json').write_text(json.dumps(h.manifest(d),indent=2))
    print('Frozen six cases and',sum(map(len,criteria.values())),'criteria')

def runner(candidate,case,suffix=''):
    run=h.prepare(candidate+'-'+case+suffix,source=False,model='gpt-5.6-luna')
    deliver=h.BASE/'runs'/candidate/'work/deliverable'
    # Copy the complete install unit, not the author's context or maintenance files.
    shutil.copytree(deliver/'skills',run/'home/.agents/skills',dirs_exist_ok=True)
    # README and declared supporting dependencies are visible as a read-only package.
    shutil.copytree(deliver,run/'package')
    state=run/'work/provided-state';(state/'output').mkdir(parents=True)
    for name in ['gate0-registry.csv','ledger.csv']:
        shutil.copyfile(h.BASE/'snapshot/output'/name,state/'output'/name)
    shutil.copyfile(h.BASE/'snapshot/candidate-brief.md',state/'candidate-brief.md')
    (run/'work/unrelated-cwd').mkdir()
    if case=='04-cache':shutil.copyfile(h.BASE/'evaluation/cache-fixture.json',run/'work/cache-fixture.json')
    (run/'initial-state.json').write_text(json.dumps(h.manifest(state),indent=2))
    (run/'initial-installed.json').write_text(json.dumps(h.manifest(run/'home/.agents/skills'),indent=2))
    prompt=(h.BASE/'evaluation'/(case+'.txt')).read_text()
    return h.execute_prepared(run,prompt,source=False,timeout=330)

if __name__=='__main__':
    import sys
    if sys.argv[1]=='freeze':freeze()
    else:runner(sys.argv[1],sys.argv[2])
