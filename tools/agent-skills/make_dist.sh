#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."

# Windows editors can hold the dist directory handle; clearing contents is enough.
if [ -d dist ]; then
  rm -rf dist 2>/dev/null || find dist -mindepth 1 -delete
fi
mkdir -p dist/agent-skills dist/.well-known/agent-skills dist/fonts

for f in 404.html _headers favicon.ico favicon.svg robots.txt index.html; do
  cp "$f" dist/
done
cp -r fonts/. dist/fonts/
cp .well-known/skills.json dist/.well-known/skills.json

cp out/*.tar.gz dist/agent-skills/
cp out/index.json dist/agent-skills/index.json
cp out/index.json dist/.well-known/agent-skills/index.json
cp out/sitemap.xml dist/sitemap.xml

python tools/agent-skills/gen_page.py --list | tr -d '\r' | while read -r name; do
  [ -n "$name" ] || continue
  mkdir -p "dist/$name"
  cp "$name/index.html" "dist/$name/index.html"
done

echo "dist: $(find dist -type f | wc -l) files"
