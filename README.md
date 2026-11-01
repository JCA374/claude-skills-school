# Skills School

**🌐 Live site: https://jca374.github.io/claude-skills-school/**

A small course on how Claude Code skills work, built from the skills installed on Jonas's laptop:
lessons, short narrated videos, a podcast, an audit of the existing skills, project ideas and a
ready-to-install `paper-review` skill. Served by GitHub Pages from `main:/docs`.

## Rebuild

```bash
python3 build_site_data.py                 # docs/data/skills.json from ~/.claude/skills (+ studio, synced, plugins)
podcast/render_all.sh 01 02 03             # narrate + Whisper-check + export episodes (voice-text), rebuild feed
video/voice_all.sh                         # voice every video script (kind voiceover), then render the films
python3 video/build_videos.py preview      # one PNG per scene, to check layouts
```

- Episodes: `podcast/episode-NN.md` (+ `.notes.json`); `~/.claude/skills/project-podcast/scripts/prepare.sh NN`
  runs the speech-flow scan, and `publish.sh NN` narrates, commits, pushes and verifies.
- Videos: narration and visuals are defined together in `video/build_videos.py` (`VIDEOS`). Clips never loop;
  the last frame holds while the narration finishes.
- `docs/examples/paper-review/` is a complete skill: `cp -r docs/examples/paper-review ~/.claude/skills/`.
