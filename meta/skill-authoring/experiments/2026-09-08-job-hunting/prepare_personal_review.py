"""Run with WSL Python; copy frozen private packages for Ray's personal trial."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

SOURCE = Path('/home/<user>/skill-authoring-study-20260908/runs')
TARGET = Path('/mnt/c/Users/<user>/Documents/skill-authoring-personal-review-20260909')
WINDOWS = 'C:/Users/<user>/Documents/skill-authoring-personal-review-20260909'

def hashes(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()}

def main():
    if TARGET.exists():
        raise SystemExit('Destination exists; refusing to overwrite personal trial state.')
    TARGET.mkdir()
    (TARGET / '.gitignore').write_text('*\n')
    checks = {}
    for arm in ('p', 'q'):
        source = SOURCE / f'candidate-{arm}/work/deliverable/skills'
        dest = TARGET / arm / 'skills'
        before = hashes(source)
        shutil.copytree(source, dest)
        subprocess.run([sys.executable, str(dest / 'ray-job-search/scripts/init_workspace.py'),
                        str(TARGET / arm / 'workspace')], check=True)
        checks[arm] = {'source_unchanged': before == hashes(source),
                       'copy_identical': before == hashes(dest), 'files': len(before)}
        if not all(checks[arm][k] for k in ('source_unchanged', 'copy_identical')):
            raise RuntimeError('Copy verification failed')
        base = f'{WINDOWS}/{arm}'
        prompt = f'''Use the skill at {base}/skills/ray-job-search/SKILL.md and its sibling searching-the-web skill. Read their required resources. Use the already initialized private workspace at {base}/workspace; do not initialize it again. These are dated experimental snapshots, not my current application registry.

Review the job postings I supply below using the full job-search policy. Do not discover extra jobs. Verify the supplied originals using available authorized tools; report inaccessible evidence as unresolved. Save the assessment in this trial workspace. Do not submit applications or contact anyone. At the end, list any setup obstacles or missing inputs that affected the result.

Postings: [paste the same 2–3 original posting URLs or complete captured postings in each trial; say whether this is live verification or an offline comparison].
'''
        (TARGET / arm / 'TRY-JOB-SEARCH.txt').write_text(prompt, encoding='utf-8')
        (TARGET / arm / 'TRY-WEB-SEARCH.txt').write_text(f'''Use {base}/skills/searching-the-web/SKILL.md and the references it calls for. Research the question below using available authorized tools. Give a concise answer with original-source links and unresolved gaps. Use only free tools or already authorized credit. Do not use the private job-search skill for this task.

Question: [paste the same concrete research question in both trials].
''', encoding='utf-8')
    (TARGET / 'copy-verification.json').write_text(json.dumps(checks, indent=2))
    (TARGET / 'START-HERE.md').write_text('''# Personal skill trial

Four unchanged skill folders, arranged as two pairs:

| Pair | Job search | Web search |
|---|---|---|
| P: authored without skill-authoring | [Read](p/skills/ray-job-search/SKILL.md) | [Read](p/skills/searching-the-web/SKILL.md) |
| Q: authored with skill-authoring | [Read](q/skills/ray-job-search/SKILL.md) | [Read](q/skills/searching-the-web/SKILL.md) |

Read the two job-search entrypoints first. Follow their resource links, especially the complete job-search-prompt.md in each workspace: much of the policy lives there. The web-search entrypoints are byte-identical; compare their references if interested.

## Try them

1. Use a fresh agent session with local file access for each pair, with the same model and tools. Copy that pair's TRY-JOB-SEARCH.txt, replacing the bracketed posting input. Explicit file loading avoids installing two skills with the same name. If the agent cannot access these files, supply the entire selected skills folder, including resources, through that host's supported file mechanism.
2. Start with the same 2–3 postings. Captured full postings make an offline comparison reproducible; live URLs additionally test current extraction but can change between runs. The working folders are already initialized and independent. They contain the September 8 seed, not current application state.
3. Try TRY-WEB-SEARCH.txt in separate fresh sessions for a general research question. This exercises the web skill independently of the job workflow.
4. Record your first impression before reading the earlier experiment report. Then save the actual answers and your feedback here. Keep model, inputs, tools and budget comparable; note differences in tool availability. This manual trial does not enforce the prior experiment's filesystem isolation or test automatic skill selection.

## Feedback worth keeping

For each pair, record: task and model; answer file; what you would actually use; a specific error or omitted detail; any unnecessary question or setup step; one passage you found confusing; your preferred result and why. Separate readability preference from an error in execution. An example with a desired correction is more useful than a numerical score alone.

No live searches were run during preparation. No global skills were installed. Copies are byte-verified against the frozen packages; maintenance outside the original skills folders was not copied. Private career and application data stay in this private review directory, outside the prompts-skills repository. Keep trial state separate from real application records.
''', encoding='utf-8')
    print(json.dumps({'folder': WINDOWS, 'verification': checks}, indent=2))

if __name__ == '__main__':
    main()
