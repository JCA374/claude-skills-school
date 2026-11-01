"""The Skills School explainer videos: narration and visuals defined together, scene by scene.

    python3 video/build_videos.py scripts          # write video/<id>/script.md (one ## scene per scene)
    # then, per video:  voice.sh new video/<id>/script.md --kind voiceover --slug film-<id>; prep; narrate; listen; export
    python3 video/build_videos.py render [ids...]  # needs voice/film-<id>/audio/voiceover/ (per-scene MP3s + timings.json)

Output: docs/video/<id>.mp4 (1280x720, 25 fps) + docs/video/<id>.jpg poster + docs/data/videos.json.
Rules (from ml-project-site): never loop, never repeat footage, hold the last frame while narration runs on.
Every number drawn comes from a file on this machine (the skill files, the studio's training cases).
"""
import glob
import json
import os
import re
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SK = os.path.expanduser('~/.claude/skills')
STUDIO = os.path.expanduser('~/code/other/fantasy-audiobook-studio')
SW, SH, FPS, GAP = 1280, 720, 25, 0.6
BG, PANEL, LINE = (17, 19, 24), (28, 31, 39), (52, 56, 68)
INK, MUTED = (236, 236, 240), (150, 153, 164)
BLUE, ORANGE, GREEN, YELLOW, PINK, PURPLE, RED = (90, 150, 245), (240, 130, 70), (60, 200, 140), (240, 185, 50), (235, 130, 170), (150, 130, 240), (240, 100, 100)
FD = '/usr/share/fonts/truetype/dejavu/'


def font(size, bold=False, mono=False):
    name = 'DejaVuSansMono' + ('-Bold' if bold else '') if mono else 'DejaVuSans' + ('-Bold' if bold else '')
    return ImageFont.truetype(FD + name + '.ttf', size)


# ---------------- real data ----------------

def skill_stats():
    rows = []
    for f in sorted(glob.glob(SK + '/*/SKILL.md')):
        name = f.split('/')[-2]
        txt = open(f).read()
        desc = re.search(r'^description:\s*(.*)$', txt, re.M).group(1).strip('"')
        code = sum(sum(1 for _ in open(p, errors='ignore')) for p in glob.glob(os.path.dirname(f) + '/scripts/*')
                   if os.path.isfile(p))
        rows.append(dict(name=name, lines=txt.count('\n'), desc_words=len(desc.split()), script_lines=code, desc=desc))
    return rows


def training_cases():
    out = []
    for line in open(STUDIO + '/training/cases.md'):
        m = re.match(r'\|\s*(\d\d)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|', line)
        if m:
            out.append(dict(n=m.group(1), problem=m.group(2), rule=m.group(3), status=m.group(4)))
    return out


def short(t, n):
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0].rstrip(',;:') + ' …'


STATS = skill_stats()
CASES = training_cases()
PS = next(s for s in STATS if s['name'] == 'ml-project-site')

# ---------------- the videos ----------------
# Each scene: title, say (narration, written for the ear), show = (kind, data). Steps of a visual are revealed
# evenly across the scene's narration.

VIDEOS = [
 dict(id='v1-anatomy', title='Anatomy of a skill', lesson='lesson-1', scenes=[
  dict(title='A skill is a folder', show=('tree', ['ml-project-site/', '├── SKILL.md          ← the instructions', '├── scripts/', '│   └── init.sh       ← code Claude runs', '└── template/         ← files to copy']),
       say="A skill is a folder. Here is one of yours, the project site skill. The important file is the skill file, written in markdown. Next to it sit scripts that I can run, and templates that I copy into a new project."),
  dict(title='The header: name and description', show=('code', ['---', 'name: ml-project-site', 'description: Standard live website for ML /', '  training projects on GitHub Pages ... Use it whenever', '  an ML, RL, evolution or training project starts or', '  needs a homepage, a progress page, a log site,', '  replays, "watch the model play" ...', '---']),
       say="The file starts with a short header. It has two fields. The name, and the description. The description says what the skill does, and, just as important, when to use it."),
  dict(title='The body: a briefing for a colleague', show=('bullets', ['Set-up, step by step', 'The data conventions it reads', 'Rules for videos and replays', 'Rules learned the hard way', 'When deployment counts as done']),
       say="Below the header comes the body. It is plain language, written like a briefing for a new colleague. Steps to follow, conventions, and the rules you learned the hard way."),
  dict(title='Your nine skills, measured', show=('bars', [(s['name'], s['lines']) for s in STATS], 'lines in SKILL.md'),
       say="Here are your nine skills, measured. Every skill file is short. Between fifty and ninety lines. The heavy work lives in the scripts, not in the instructions."),
  dict(title='Scripts do the heavy lifting', show=('bars', [(s['name'], s['script_lines']) for s in STATS if s['script_lines']], 'lines of script code'),
       say="And this is the code behind them. About fourteen hundred lines in total. When I run a script, only its output comes back to me. So a big script costs me almost nothing to use."),
 ]),
 dict(id='v2-loading', title='How Claude picks and loads a skill', lesson='lesson-2', scenes=[
  dict(title='At the start: only a list', show=('stack', [('Level 1 · always loaded', 'name + description of every skill  (~100 words each)', BLUE)]),
       say="When a session starts, I do not read your skills. I only see a list. One line per skill, the name and the description. That is all."),
  dict(title='Your request meets the descriptions', show=('match', ['"make a homepage for the bipedal run"', 'ml-project-site', 'project-podcast', 'failure-analysis-report']),
       say="When you ask for something, I compare your words with every description. Here you ask for a homepage for a training run. One description fits: the project site skill."),
  dict(title='Three levels of loading', show=('stack', [('Level 1 · always', 'name + description', BLUE), ('Level 2 · when chosen', 'the body of SKILL.md', ORANGE), ('Level 3 · when a step needs it', 'scripts run, references read', GREEN)]),
       say="Now the skill loads in layers. First the body of the skill file. Then, only when a step needs it, a reference file or a script. This is called progressive disclosure."),
  dict(title='Or call it yourself', show=('code', ['> /code-review high', '', '> /loop 5m check the training run', '', 'A slash + the name loads the skill directly.']),
       say="You can also skip the matching. Type a slash and the skill's name, and it loads straight away. That is handy for commands you run on purpose, like a deploy or a review."),
  dict(title='Why the description matters most', show=('compare', ('Weak', ['"Website helper."', 'no "when"', 'never fires'], RED), ('Strong', ['what it builds', 'the words you say:', 'homepage, replays, film', 'fires at the right time'], GREEN)),
       say="So the description is the trigger. A weak one says what the skill is. A strong one also lists the words you actually say when you need it. Yours for the project site is a strong one."),
 ]),
 dict(id='v3-pipeline', title='Skills that work together', lesson='lesson-5', scenes=[
  dict(title='One job, five skills', show=('flow', [('speech-flow', 'fix for the ear'), ('narration-prep', 'text → script'), ('kokoro-narrate', 'script → audio'), ('listen-check', 'Whisper listens'), ('audiobook-assemble', 'MP3 + m4b')]),
       say="Some jobs are too big for one skill. Your audiobook studio splits narration into five. Speech flow fixes the text for the ear. Narration prep makes the script. Kokoro narrate renders it. Listen check has Whisper listen back. And audiobook assemble packages it."),
  dict(title='voice-text: one door into the pipeline', show=('code', ['V=~/.claude/skills/voice-text/scripts/voice.sh', '$V new notes.md --kind prose', '$V scan    voice/notes', '$V prep    voice/notes', '$V narrate voice/notes', '$V listen  voice/notes', '$V export  voice/notes']),
       say="Voice text is the front door. From any project, one launcher calls each stage in order. It reuses the studio's scripts instead of copying them, so a fix in the studio helps everyone."),
  dict(title='Skills that point to skills', show=('flow', [('ml-project-site', 'the website'), ('project-podcast', 'Podcast tab'), ('voice-text', 'the narration'), ('listen-check', 'the check')]),
       say="Your project site skill works the same way. It hands the podcast tab to the podcast skill. The podcast skill hands the audio to voice text. And voice text hands the checking to listen check."),
  dict(title='This video was made by them', show=('bullets', ['Script written scene by scene', 'speech-flow scan: phrasing fixed', 'Kokoro (af_heart) voiced each scene', 'Whisper listened back for errors', 'Scenes drawn from real files, then joined']),
       say="This very video is an example. The script was scanned for phrasing. Kokoro voiced each scene, Whisper checked it, and each picture was drawn from real files on your machine."),
 ]),
 dict(id='v4-learning', title='How a skill learns', lesson='lesson-6', scenes=[
  dict(title='The training loop', show=('flow', [('report', '"sounds wrong"'), ('case', 'before / after'), ('you pick', 'by ear'), ('rule', 'in the skill'), ('test', 'never undone')]),
       say="A skill gets better when a lesson is written into it. Your studio has a fixed loop. A problem is reported. It becomes a case with a before and an after. You pick the better one. It becomes a rule, and a test keeps it from being undone."),
  dict(title=f'{len(CASES)} cases so far', show=('table', [(c['n'], short(re.sub(r'[`*]', '', c['problem']), 64)) for c in CASES]),
       say="Here are the studio's real cases. Short questions that end flat. Commas that break the rhythm. Two word lines that feel lazy. Each one is now a rule."),
  dict(title='Rules learned the hard way', show=('bullets', ['publish.py never runs  git pull --rebase --autostash', '  (it once silently reverted an hour of code)', 'Deployment counts only when Pages says "built <sha>"', 'A replay that fails must never stop the publisher']),
       say="Your project site skill learns the same way. It has a list of rules learned the hard way. One of them exists because a rebase once threw away an hour of work."),
  dict(title='Measure, then improve', show=('compare', ('without skill', ['same task', 'baseline output'], MUTED), ('with skill', ['same task', 'compared side by side', 'keep what wins'], GREEN)),
       say="To know that a skill helps, measure it. The skill creator runs the same task with the skill and without it, and you compare. If the skill does not win, change it and run again."),
 ]),
 dict(id='v5-reviewer', title='A skill that reviews papers', lesson='example', scenes=[
  dict(title='The idea', show=('bullets', ['Review a paper or report like a careful referee', 'Same path every time', 'Every finding points to a page', 'Never invents a number or a citation']),
       say="Here is a skill you could build next. It reviews academic papers and reports, the way a careful referee would. It follows the same path every time, and every finding points to a page."),
  dict(title='The review path', show=('flow', [('claim', '3-sentence summary'), ('evidence', 'tables, n, baselines'), ('method', 'luck, leaks'), ('sources', 'cited right?'), ('verdict', '+ confidence')]),
       say="The path has five steps. Summarize the claim. Check it against the evidence. Look for luck or leaks in the method. Check the sources. Then give a verdict with a confidence level."),
  dict(title='The folder', show=('tree', ['paper-review/', '├── SKILL.md', '├── references/', '│   ├── ml-papers.md', '│   ├── statistics.md', '│   └── business-reports.md', '├── scripts/', '│   ├── extract.py        ← text, tables, refs', '│   └── check_quotes.py   ← every quote is real', '└── tests/papers/         ← known flaws']),
       say="The checklists go in a references folder, one per kind of paper. A script pulls out the text and tables. Another script checks that every quote in the review really appears in the paper."),
  dict(title='Make it learn', show=('flow', [('test paper', 'known flaw'), ('review', 'with skill'), ('missed?', 'new case'), ('rule', 'in a reference'), ('rerun all', 'no regressions')]),
       say="Then make it learn, like the studio. Keep test papers with known flaws. When a review misses one, that becomes a case and a rule. Run every test paper again after each change."),
 ]),
]


# ---------------- drawing ----------------

def wrap(d, s, f, width):
    words, lines, cur = s.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) > width and cur:
            lines.append(cur); cur = w
        else:
            cur = t
    return lines + ([cur] if cur else [])


def base(video, scene, k, n):
    im = Image.new('RGB', (SW, SH), BG)
    d = ImageDraw.Draw(im)
    d.text((60, 40), video['title'].upper(), fill=BLUE, font=font(18, True))
    d.text((60, 70), scene['title'], fill=INK, font=font(42, True))
    d.text((60, SH - 44), 'Skills School', fill=MUTED, font=font(16))
    d.text((SW - 60, SH - 44), f'scene {k} / {n}', fill=MUTED, font=font(16), anchor='ra')
    return im, d


def n_steps(show):
    kind, data = show[0], show[1]
    return {'tree': len(data), 'code': 1, 'bullets': len(data), 'bars': len(data), 'stack': len(data), 'match': 3,
            'compare': 2, 'flow': len(data), 'table': len(data)}[kind]


def draw(d, show, step):
    kind, data = show[0], show[1]
    top = 160
    if kind in ('tree', 'code'):
        lines = data if kind == 'tree' else data
        shown = lines[:step] if kind == 'tree' else lines
        h = 46 * len(lines) + 40
        d.rounded_rectangle((60, top, SW - 60, top + h), 14, fill=PANEL, outline=LINE)
        for i, l in enumerate(shown):
            col = ORANGE if l.startswith('>') or l.startswith('$') else (MUTED if l.startswith('---') else INK)
            if '←' in l:
                a, b = l.split('←')
                d.text((90, top + 24 + 46 * i), a, fill=INK, font=font(26, mono=True))
                d.text((90 + d.textlength(a, font=font(26, mono=True)), top + 24 + 46 * i), '← ' + b.strip(), fill=GREEN, font=font(24, mono=True))
            else:
                d.text((90, top + 24 + 46 * i), l, fill=col, font=font(26, mono=True))
    elif kind == 'bullets':
        y = top + 10
        for i, b in enumerate(data[:step]):
            sub = b.startswith('  ')
            if not sub:
                d.ellipse((72, y + 12, 86, y + 26), fill=[BLUE, ORANGE, GREEN, YELLOW, PINK][i % 5])
            d.text((110 if not sub else 110, y), b.strip(), fill=MUTED if sub else INK, font=font(26 if sub else 32))
            y += 70 if not sub else 56
    elif kind == 'bars':
        label = show[2]
        mx = max(v for _, v in data)
        bh = min(48, (SH - top - 110) // len(data))
        for i, (name, v) in enumerate(data[:step]):
            y = top + i * bh
            d.text((60, y + bh / 2), name, fill=INK, font=font(22), anchor='lm')
            w = int((SW - 470) * v / mx)
            d.rectangle((340, y + 8, 340 + w, y + bh - 8), fill=BLUE)
            d.text((350 + w, y + bh / 2), str(v), fill=INK, font=font(22, True), anchor='lm')
        d.text((340, top + len(data) * bh + 10), label + ' · counted from ~/.claude/skills', fill=MUTED, font=font(18))
    elif kind == 'stack':
        for i, (h1, h2, col) in enumerate(data[:step]):
            y = top + 20 + i * 150
            d.rounded_rectangle((60 + i * 40, y, SW - 60, y + 120), 14, fill=PANEL, outline=col, width=3)
            d.text((90 + i * 40, y + 22), h1, fill=col, font=font(30, True))
            d.text((90 + i * 40, y + 70), h2, fill=INK, font=font(26))
    elif kind == 'match':
        req, hit, *others = data
        d.rounded_rectangle((60, top + 10, SW - 60, top + 90), 14, fill=PANEL, outline=LINE)
        d.text((90, top + 50), 'You: ' + req, fill=INK, font=font(28), anchor='lm')
        if step >= 2:
            for i, nm in enumerate(others + [hit]):
                y = top + 150 + i * 80
                ok = nm == hit and step >= 3
                d.rounded_rectangle((300, y, 980, y + 62), 12, fill=PANEL, outline=GREEN if ok else LINE, width=3 if ok else 1)
                d.text((330, y + 31), nm, fill=INK if ok or step < 3 else MUTED, font=font(28, ok), anchor='lm')
                if ok:
                    d.text((1000, y + 31), '✓ loads', fill=GREEN, font=font(28, True), anchor='lm')
    elif kind == 'compare':
        for i, (h, items, col) in enumerate(show[1:][:step]):
            x = 60 + i * 590
            d.rounded_rectangle((x, top + 10, x + 570, SH - 90), 16, fill=PANEL, outline=col, width=3)
            d.text((x + 30, top + 40), h, fill=col, font=font(34, True))
            for j, it in enumerate(items):
                d.text((x + 30, top + 110 + j * 56), it, fill=INK, font=font(28))
    elif kind == 'flow':
        n = len(data)
        bw = (SW - 120 - (n - 1) * 30) // n
        y = top + 120
        for i, (h1, h2) in enumerate(data[:step]):
            x = 60 + i * (bw + 30)
            col = [BLUE, ORANGE, GREEN, YELLOW, PINK][i % 5]
            d.rounded_rectangle((x, y, x + bw, y + 170), 14, fill=PANEL, outline=col, width=3)
            fs = 22 if n > 4 else 26
            while fs > 14 and d.textlength(h1, font=font(fs, True)) > bw - 16:
                fs -= 1
            d.text((x + bw / 2, y + 40), h1, fill=col, font=font(fs, True), anchor='mm')
            for j, l in enumerate(wrap(d, h2, font(20), bw - 24)):
                d.text((x + bw / 2, y + 110 + j * 26), l, fill=INK, font=font(20), anchor='mm')
            if i:
                d.text((x - 15, y + 85), '→', fill=MUTED, font=font(30, True), anchor='mm')
            d.text((x + bw / 2, y - 30), str(i + 1), fill=MUTED, font=font(22, True), anchor='mm')
    elif kind == 'table':
        rh = min(46, (SH - top - 80) // len(data))
        for i, (a, b) in enumerate(data[:step]):
            y = top + i * rh
            d.rectangle((60, y, SW - 60, y + rh - 4), fill=PANEL)
            d.text((80, y + rh / 2 - 2), a, fill=ORANGE, font=font(22, True, mono=True), anchor='lm')
            d.text((140, y + rh / 2 - 2), b, fill=INK, font=font(21), anchor='lm')


def frames_for_scene(video, k, n, dur, outdir):
    """Reveal steps evenly over the narration; the last step holds to the end (no loops, no repeats)."""
    scene = video['scenes'][k - 1]
    steps = n_steps(scene['show'])
    span = dur * 0.8                               # finish revealing by 80 % of the narration
    times = [span * i / steps for i in range(steps)] + [dur + GAP]
    lst = []
    for s in range(1, steps + 1):
        im, d = base(video, scene, k, n)
        draw(d, scene['show'], s)
        p = f'{outdir}/s{k:02d}_{s:02d}.png'
        im.save(p)
        lst.append((p, times[s] - times[s - 1]))
    return lst


def render(vid):
    v = next(x for x in VIDEOS if x['id'] == vid)
    vo = f'voice/film-{vid}/audio/voiceover'
    timings = json.load(open(vo + '/timings.json'))
    durs = [t['seconds'] if isinstance(t, dict) else t for t in (timings['scenes'] if isinstance(timings, dict) and 'scenes' in timings else timings)]
    tmp = f'video/build/{vid}'
    os.makedirs(tmp, exist_ok=True)
    segs = []
    for k, dur in enumerate(durs, 1):
        lst = frames_for_scene(v, k, len(durs), dur, tmp)
        with open(f'{tmp}/s{k:02d}.txt', 'w') as f:
            for p, t in lst:
                f.write(f"file '{os.path.abspath(p)}'\nduration {t:.3f}\n")
            f.write(f"file '{os.path.abspath(lst[-1][0])}'\n")
        seg = f'{tmp}/seg{k:02d}.mp4'
        subprocess.run(['nice', '-n', '10', 'ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/s{k:02d}.txt',
                        '-i', f'{vo}/ch{k:02d}.mp3', '-af', f'apad=pad_dur={GAP}', '-t', f'{dur + GAP:.3f}',
                        '-vf', f'fps={FPS},format=yuv420p', '-c:v', 'libx264', '-crf', '24', '-preset', 'medium',
                        '-c:a', 'aac', '-b:a', '128k', '-ar', '44100', '-ac', '1', seg], check=True)
        segs.append(seg)
    with open(f'{tmp}/all.txt', 'w') as f:
        f.writelines(f"file '{os.path.abspath(s)}'\n" for s in segs)
    os.makedirs('docs/video', exist_ok=True)
    out = f'docs/video/{vid}.mp4'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/all.txt', '-c', 'copy',
                    '-movflags', '+faststart', out], check=True)
    # poster = the first scene fully revealed
    im, d = base(v, v['scenes'][0], 1, len(durs)); draw(d, v['scenes'][0]['show'], n_steps(v['scenes'][0]['show']))
    im.convert('RGB').save(f'docs/video/{vid}.jpg', quality=85)
    total = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out],
                                 capture_output=True, text=True).stdout)
    print(f'{out}: {total:.1f} s, {len(durs)} scenes')
    return total


def write_feed():
    eps = []
    for v in VIDEOS:
        mp4 = f'docs/video/{v["id"]}.mp4'
        if not os.path.exists(mp4):
            continue
        sec = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp4],
                                   capture_output=True, text=True).stdout)
        tj = f'voice/film-{v["id"]}/audio/voiceover/timings.json'
        starts, t = [], 0.0
        for x in (json.load(open(tj)) if os.path.exists(tj) else []):
            starts.append(round(t, 2)); t += x['seconds'] + GAP
        eps.append(dict(id=v['id'], title=v['title'], lesson=v['lesson'], seconds=round(sec), starts=starts,
                        scenes=[dict(title=s['title'], say=s['say']) for s in v['scenes']]))
    os.makedirs('docs/data', exist_ok=True)
    json.dump(dict(videos=eps), open('docs/data/videos.json', 'w'), indent=1, ensure_ascii=False)
    print(f'{len(eps)} video(s) in docs/data/videos.json')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'scripts'
    if cmd == 'scripts':
        for v in VIDEOS:
            os.makedirs(f'video/{v["id"]}', exist_ok=True)
            with open(f'video/{v["id"]}/script.md', 'w') as f:
                f.write(f'# {v["title"]}\n\n' + ''.join(f'## {s["title"]}\n\n{s["say"]}\n\n' for s in v['scenes']))
            print(f'video/{v["id"]}/script.md: {sum(len(s["say"].split()) for s in v["scenes"])} words')
    elif cmd == 'render':
        for vid in sys.argv[2:] or [v['id'] for v in VIDEOS]:
            render(vid)
        write_feed()
    elif cmd == 'preview':                       # one PNG per scene, fully revealed, for checking layouts
        os.makedirs('video/build/preview', exist_ok=True)
        for v in VIDEOS:
            for k, s in enumerate(v['scenes'], 1):
                im, d = base(v, s, k, len(v['scenes'])); draw(d, s['show'], n_steps(s['show']))
                im.save(f'video/build/preview/{v["id"]}_{k}.png')
        print('video/build/preview/')
