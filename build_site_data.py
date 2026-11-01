"""docs/data/skills.json: every skill Claude can use on this machine, read from the files themselves.

    python3 build_site_data.py
Groups: personal (~/.claude/skills), studio project skills, Anthropic (synced), plugins, built-in commands.
deploy.md's body is not published (it holds a server address); only what it is.
"""
import glob
import json
import os
import re

SK = os.path.expanduser('~/.claude/skills')
STUDIO = os.path.expanduser('~/code/other/fantasy-audiobook-studio/.claude/skills')

PLAIN = {  # one plain sentence per personal skill: what it gives you
    'failure-analysis-report': 'Records how a model fails and turns it into one HTML report: gallery, heatmaps, run-up curves, which signals predict failure.',
    'ml-project-site': 'A live GitHub Pages site for a training run: log, curriculum, replays, "watch it play", lessons, podcast; rebuilt every 15 min.',
    'project-podcast': 'Writes, voices, checks and publishes a short spoken progress episode to the project site.',
    'voice-text': 'The front door to the audio pipeline: turns any text (doc, notes, video script) into checked narration.',
    'speech-flow': 'Finds punctuation and sentence shapes that trip a listener or the TTS voice, and proposes ear-friendly rewrites.',
    'narration-prep': 'Turns a chapter into a Kokoro script: strips markdown, spells numbers, applies name pronunciations.',
    'kokoro-narrate': 'Renders the script to speech locally with Kokoro (CPU), cached per paragraph.',
    'listen-check': 'Whisper listens to the audio and flags skipped, swapped or misheard words, odd pace and flat questions.',
    'audiobook-assemble': 'Masters the WAVs into loudness-normalised MP3s and one .m4b with chapters and cover.',
}
PIPE = {'speech-flow': 1, 'narration-prep': 2, 'kokoro-narrate': 3, 'listen-check': 4, 'audiobook-assemble': 5}


def front(txt):
    m = re.match(r'---\n(.*?)\n---\n?(.*)', txt, re.S)
    head, body = (m.group(1), m.group(2)) if m else ('', txt)
    meta = {}
    for line in head.splitlines():
        k, _, v = line.partition(':')
        if v:
            meta[k.strip()] = v.strip().strip('"')
    return meta, body


def files_of(d):
    out = []
    for p in sorted(glob.glob(d + '/**/*', recursive=True)):
        if os.path.isfile(p) and '__pycache__' not in p:
            out.append(dict(path=os.path.relpath(p, d), lines=sum(1 for _ in open(p, errors='ignore'))))
    return out


skills = []
for f in sorted(glob.glob(SK + '/*/SKILL.md')):
    d = os.path.dirname(f)
    name = os.path.basename(d)
    meta, body = front(open(f).read())
    linked = os.path.islink(d)
    skills.append(dict(group='personal', name=name, description=meta.get('description', ''), plain=PLAIN.get(name, ''),
                       source='audiobook studio (symlink)' if linked else 'written for your projects',
                       pipeline=PIPE.get(name), lines=open(f).read().count('\n'), files=files_of(d),
                       skill_md=open(f).read()))

meta, _ = front(open(SK + '/deploy.md').read())
skills.append(dict(group='personal', name='deploy (deploy.md)', description=meta.get('description', ''),
                   plain='rsync + docker restart for the World Cup tips site. NOT loaded: it is a loose file, not deploy/SKILL.md.',
                   source='loose file: not loaded', broken=True, lines=23, files=[], skill_md=''))

for f in sorted(glob.glob(STUDIO + '/*/SKILL.md')):
    name = f.split('/')[-2]
    if os.path.exists(f'{SK}/{name}'):
        continue
    meta, _ = front(open(f).read())
    skills.append(dict(group='studio', name=name, description=meta.get('description', ''),
                       source='only inside fantasy-audiobook-studio (project skill)', lines=open(f).read().count('\n')))

man = glob.glob(SK + '/synced/*/manifest.json')
if man:
    for s in json.load(open(man[0]))['skills']:
        skills.append(dict(group='anthropic', name=s['name'], description=s['description'], source='Anthropic (synced from claude.ai)'))

PLUGINS = [
    ('data:analyze', 'Answer data questions, from a quick lookup to a full analysis.'),
    ('data:build-dashboard', 'Interactive HTML dashboard with charts, filters and tables.'),
    ('data:create-viz / data-visualization', 'Publication-quality charts in Python.'),
    ('data:explore-data', 'Profile a new dataset: shape, nulls, distributions, quality issues.'),
    ('data:statistical-analysis', 'Descriptive stats, trends, outliers, hypothesis tests.'),
    ('data:validate-data', 'QA an analysis before sharing: methodology, accuracy, bias.'),
    ('data:sql-queries / write-query', 'Correct, fast SQL for any warehouse dialect.'),
    ('data:data-context-extractor', 'Builds a company-specific data skill by interviewing analysts.'),
    ('pdf-viewer:*', 'Open, annotate, fill and sign PDFs in an interactive viewer.'),
]
for n, d in PLUGINS:
    skills.append(dict(group='plugin', name=n, description=d, source='plugin'))

BUILTIN = [
    ('/code-review', 'Review the current diff or a PR for bugs, at an effort level; ultra = multi-agent cloud review.'),
    ('/simplify', 'Clean up changed code: reuse, simplification, efficiency.'),
    ('/loop', 'Run a prompt or command on an interval, or let Claude self-pace.'),
    ('/schedule', 'Scheduled cloud agents (routines) on a cron schedule.'),
    ('/init', 'Write a CLAUDE.md for a codebase.'),
    ('/security-review', 'Security review of the pending changes.'),
    ('dataviz', 'Design rules for any chart: form, colour, marks, accessibility.'),
    ('update-config / keybindings-help', 'Edit settings.json (hooks, permissions) and keybindings.'),
]
for n, d in BUILTIN:
    skills.append(dict(group='builtin', name=n, description=d, source='built into Claude Code'))

os.makedirs('docs/data', exist_ok=True)
json.dump(dict(skills=skills), open('docs/data/skills.json', 'w'), indent=1, ensure_ascii=False)
print({g: sum(s['group'] == g for s in skills) for g in ('personal', 'studio', 'anthropic', 'plugin', 'builtin')})
