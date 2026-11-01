#!/usr/bin/env bash
# Voice every video script (voice-text, kind voiceover), then render the films.
cd "$(dirname "$0")/.."; V=~/.claude/skills/voice-text/scripts/voice.sh
for s in video/v*/script.md; do id=$(basename $(dirname $s)); D=voice/film-$id
  [ -d $D ] && F=--force || F=""
  $V new $s --kind voiceover --slug film-$id $F > /dev/null
  $V prep $D > /dev/null 2>&1
  echo "[$(date +%T)] $id narrate"; nice -n 5 $V narrate $D > $D/narrate.log 2>&1 || { echo "FAILED narrate $id"; continue; }
  $V listen $D > $D/listen.txt 2>&1
  $V export $D > $D/export.log 2>&1 || { echo "FAILED export $id"; continue; }
  echo "[$(date +%T)] $id voiced"
done
python3 video/build_videos.py render
