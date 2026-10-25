#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."

# Windows editors can hold the dist directory handle; clearing contents is enough.
if [ -d dist ]; then
  rm -rf dist 2>/dev/null || true
  if [ -d dist ]; then
    find dist -mindepth 1 -delete 2>/dev/null || true
  fi
  if [ -n "$(find dist -mindepth 1 -print -quit 2>/dev/null)" ]; then
    sleep 1
    find dist -mindepth 1 -delete 2>/dev/null || true
  fi
  if [ -n "$(find dist -mindepth 1 -print -quit 2>/dev/null)" ]; then
    echo "make_dist: dist/ is held by another process; close it and retry" >&2
    exit 1
  fi
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
cp out/_redirects dist/_redirects
cp out/llms.txt dist/llms.txt

for name in $(cd tools/agent-skills && python -c "import skilllib; print(*skilllib.STATIC_PAGES)" | tr -d '\r'); do
  mkdir -p "dist/$name"
  cp "$name/index.html" "dist/$name/index.html"
done

python tools/agent-skills/gen_page.py --list | tr -d '\r' | while read -r name; do
  [ -n "$name" ] || continue
  mkdir -p "dist/$name"
  cp "$name/index.html" "dist/$name/index.html"
done

# One hash over every file, so CI can tell whether the live site already matches this build.
python - <<'PY'
import hashlib, json, pathlib
root = pathlib.Path("dist")
digest = hashlib.sha256()
for path in sorted(p for p in root.rglob("*") if p.is_file() and p.name != "version.json"):
    digest.update(path.relative_to(root).as_posix().encode() + b"\0" + path.read_bytes() + b"\0")
(root / "version.json").write_text(json.dumps({"tree": digest.hexdigest()}) + "\n")
PY

echo "dist: $(find dist -type f | wc -l) files"
