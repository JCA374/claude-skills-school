#!/usr/bin/env bash
# Narrate + Whisper-check + export each episode (publish.sh's audio half; pushing happens later).
cd "$(dirname "$0")/.."; V=~/.claude/skills/voice-text/scripts/voice.sh
for NN in "$@"; do D=voice/podcast-$NN
  echo "[$(date +%T)] $NN prep"; $V prep $D > /dev/null 2>&1 || { echo "FAILED prep $NN"; continue; }
  echo "[$(date +%T)] $NN narrate"; nice -n 5 $V narrate $D > $D/narrate.log 2>&1 || { echo "FAILED narrate $NN"; continue; }
  echo "[$(date +%T)] $NN listen"; $V listen $D > $D/listen.txt 2>&1
  $V export $D > $D/export.log 2>&1 || { echo "FAILED export $NN"; continue; }
  cp $D/audio/ch01.mp3 docs/podcast/episode-$NN.mp3
  echo "[$(date +%T)] $NN done $(ffprobe -v error -show_entries format=duration -of csv=p=0 docs/podcast/episode-$NN.mp3)s"
done
python3 ~/.claude/skills/project-podcast/scripts/make_feed.py
