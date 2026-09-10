"""Private WSL paired study. Host data lives outside the public source repository."""
import argparse, hashlib, json, os, re, shutil, signal, subprocess, time
from pathlib import Path

BASE = Path('/home/<user>/skill-authoring-study-20260908')
SOURCE = Path('/home/<user>/me/Job_hunting')
SKILL = Path('/mnt/c/Users/<user>/Documents/Projects/prompts-skills/skills/skill-authoring')
VENDOR = Path('/home/<user>/.bun/install/global/node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl')
MODEL = 'gpt-6-astra'

COMMON = '''Convert /source's job-search materials into reusable private agent skill package(s). Decide whether one package or separate search-tool and job-search packages best serve future use, taking existing skills into account. Preserve the established behavior and necessary resources. The result should work from another workspace with its documented dependencies. Write complete candidate packages under /work/deliverable/skills/ and a concise explanation under /work/deliverable/README.md. You may include additional supporting files under deliverable. Do not modify the source snapshot, install globally, or conduct a live job search.

The source includes current uncommitted work. Its AGENTS.md is source context for the search workflow, not an instruction to perform a search now. Dated authoritative career references are available read-only at /context/career-source; original host paths are unavailable in this isolated environment. Credential literals in source were replaced with ${EXA_API_KEY}; never embed a credential. Search programs/network services are not supplied for live searches; ordinary Python, shell, and file tools are available for local checks. No other user is available during this run: resolve ordinary design choices yourself and document material assumptions. Use the existing source as the task specification. Finish within 15 minutes. Do not invoke another language model or another Codex process. Skill files need name and description frontmatter and a SKILL.md entrypoint; supporting resources may be bundled as needed.
'''

def manifest(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink()}

def setup():
    BASE.mkdir(mode=0o700, exist_ok=False)
    snap=BASE/'snapshot'; snap.mkdir()
    omitted=[]
    for p in SOURCE.rglob('*'):
        rel=p.relative_to(SOURCE)
        if any(x in rel.parts for x in ['.git','.claude','.codebuddy','__pycache__']): continue
        if p.is_symlink(): omitted.append(str(rel)); continue
        if not p.is_file(): continue
        if p.name.startswith('.env') or p.suffix in ['.pyc']: continue
        dst=snap/rel; dst.parent.mkdir(parents=True,exist_ok=True)
        data=p.read_bytes()
        try:
            txt=data.decode('utf-8')
            # Replace the known Exa credential only in credential-bearing syntax.
            txt=re.sub(r'(?i)(exaApiKey=)[0-9a-f-]{36}',r'\1${EXA_API_KEY}',txt)
            txt=re.sub(r'(?i)(x-api-key:\s*)[0-9a-f-]{36}',r'\1${EXA_API_KEY}',txt)
            txt=re.sub(r'(?i)(API key:\s*`)[0-9a-f-]{36}',r'\1${EXA_API_KEY}',txt)
            data=txt.encode()
        except UnicodeDecodeError: pass
        dst.write_bytes(data)
    shutil.copytree(SKILL,BASE/'treatment-skill')
    shutil.copytree('/mnt/c/Users/<user>/.agents/skills/ray-resume-workflow/references',BASE/'career-source')
    (BASE/'source-before.json').write_text(json.dumps(manifest(SOURCE),indent=2))
    (BASE/'snapshot-manifest.json').write_text(json.dumps(manifest(snap),indent=2))
    (BASE/'setup.json').write_text(json.dumps({'model':MODEL,'effort':'low','source':str(SOURCE),'omitted_symlinks':omitted,'skill_manifest':manifest(BASE/'treatment-skill')},indent=2))
    (BASE/'common-prompt.txt').write_text(COMMON)
    print(BASE)

def prepare(name, treatment=False, source=True, model=MODEL):
    run=BASE/'runs'/name; run.mkdir(parents=True,exist_ok=False)
    for d in ['home/.codex','home/.agents/skills','work','logs']: (run/d).mkdir(parents=True,exist_ok=True)
    shutil.copyfile('/home/<user>/.codex/auth.json',run/'home/.codex/auth.json')
    (run/'home/.codex/auth.json').chmod(0o600)
    if source:
        shutil.copytree(BASE/'snapshot/.agents/skills/searching-the-web',run/'home/.agents/skills/searching-the-web')
    if treatment:
        shutil.copytree(BASE/'treatment-skill',run/'home/.agents/skills/skill-authoring')
    cfg='model = "'+model+'"\nmodel_reasoning_effort = "low"\napproval_policy = "never"\nweb_search = "disabled"\n[memories]\nuse_memories = false\ngenerate_memories = false\n'
    for name2 in ['skill-creator','plugin-creator','skill-installer','openai-docs','imagegen','review-agent','plan']:
        cfg+='\n[[skills.config]]\npath = "/home/agent/.codex/skills/.system/'+name2+'/SKILL.md"\nenabled = false\n'
    (run/'home/.codex/config.toml').write_text(cfg)
    return run

def command(run, source=True):
    cmd=['bwrap','--die-with-parent','--new-session','--unshare-pid','--unshare-ipc','--unshare-uts',
         '--ro-bind','/usr','/usr','--symlink','usr/bin','/bin','--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64',
         '--proc','/proc','--dev','/dev','--tmpfs','/tmp','--dir','/etc','--dir','/opt',
         '--ro-bind',str(VENDOR),'/opt/codex','--bind',str(run/'home'),'/home/agent','--bind',str(run/'work'),'/work']
    for p in ['/etc/ssl','/etc/resolv.conf','/etc/hosts','/etc/nsswitch.conf','/etc/passwd','/etc/group','/etc/localtime']:
        if Path(p).exists(): cmd+=['--ro-bind',p,p]
    if source:
        cmd+=['--ro-bind',str(BASE/'snapshot'),'/source','--ro-bind',str(BASE/'career-source'),'/context/career-source']
    if (run/'package').exists():
        cmd+=['--ro-bind',str(run/'package'),'/package','--ro-bind',str(run/'home/.agents'),'/home/agent/.agents']
    cmd+=['--chdir','/work','--clearenv','--setenv','HOME','/home/agent','--setenv','CODEX_HOME','/home/agent/.codex',
          '--setenv','PATH','/opt/codex/bin:/usr/local/bin:/usr/bin:/bin','--setenv','LANG','C.UTF-8','--setenv','PYTHONDONTWRITEBYTECODE','1']
    return cmd

def execute(name, prompt, treatment=False, source=True, timeout=1000):
    run=prepare(name,treatment,source)
    return execute_prepared(run,prompt,source,timeout)

def execute_prepared(run,prompt,source=True,timeout=1000):
    (run/'prompt.txt').write_text(prompt)
    cmd=command(run,source)+['/opt/codex/bin/codex','exec','--strict-config','--ephemeral','--skip-git-repo-check',
                            '-s','workspace-write','--json','--color','never','-o','/work/final.md','-']
    (run/'command.json').write_text(json.dumps(cmd,indent=2))
    # Independent OS-level read/write probes, outside model context.
    probe='import os,json; p=["/home/<user>","/mnt/c","/source","/context/career-source","/home/agent/.agents/skills/skill-authoring","/work"]; print(json.dumps({x:os.path.exists(x) for x in p})); print(open("/proc/self/mountinfo").read())'
    pr=subprocess.run(command(run,source)+['python3','-c',probe],capture_output=True,text=True)
    (run/'logs/isolation.txt').write_text(pr.stdout+pr.stderr)
    start=time.time()
    with (run/'logs/events.jsonl').open('w') as out,(run/'logs/stderr.txt').open('w') as err:
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=out,stderr=err,text=True,start_new_session=True)
        try: p.communicate(prompt,timeout=timeout); status=p.returncode
        except subprocess.TimeoutExpired:
            os.killpg(p.pid,signal.SIGTERM)
            try:p.wait(timeout=10)
            except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
            status='timeout'
    (run/'result.json').write_text(json.dumps({'exit':status,'elapsed_seconds':round(time.time()-start,2)},indent=2))
    print(run.name,status,round(time.time()-start,2),flush=True)
    return status

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('action');ap.add_argument('--name');ap.add_argument('--treatment',action='store_true');args=ap.parse_args()
    if args.action=='setup':setup()
    elif args.action=='probe':execute(args.name or 'preflight','List the names of the available skills in this session. Run python3 to print whether /home/<user>, /mnt/c, /source and /home/agent/.agents/skills/skill-authoring exist. Do not read source contents or modify anything. Finish briefly.',args.treatment,timeout=120)
    elif args.action=='author':execute(args.name,COMMON+('\nUse the available skill-authoring skill to carry out this task.\n' if args.treatment else ''),args.treatment)
