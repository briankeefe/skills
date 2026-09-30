#!/bin/sh
# Link this checkout into OMP; never replace another skill or local edits.
set -eu
SOURCE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SKILLS_DIR=${SKILLS_DIR:-"$HOME/.omp/agent/skills"}

# Check all collisions before creating any links.
for source in "$SOURCE_DIR"/skills/*; do
  [ -f "$source/SKILL.md" ] || continue
  target="$SKILLS_DIR/${source##*/}"
  if [ -e "$target" ] || [ -L "$target" ]; then
    if [ -L "$target" ] && [ "$(readlink "$target")" = "$source" ]; then
      continue
    fi
    printf 'Refusing to replace %s; preserve local edits and move it aside first.\n' "$target" >&2
    exit 1
  fi
done

mkdir -p "$SKILLS_DIR"
for source in "$SOURCE_DIR"/skills/*; do
  [ -f "$source/SKILL.md" ] || continue
  target="$SKILLS_DIR/${source##*/}"
  if [ ! -L "$target" ]; then ln -s "$source" "$target"; fi
  printf 'Installed %s -> %s\n' "$target" "$source"
done
