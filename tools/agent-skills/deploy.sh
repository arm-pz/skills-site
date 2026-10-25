#!/usr/bin/env bash
# Manual fallback. Normally the publish workflow commits the build to the `deploy` branch and the
# Git-connected Cloudflare Pages project serves it. This deploys main from your own machine. CI never holds Cloudflare
# credentials: wrangler uses your login (`npx wrangler login`, an OAuth session stored on this
# machine) or a CLOUDFLARE_API_TOKEN you export in this shell only. Nothing is written to the repo.
#
#   bash tools/agent-skills/deploy.sh            # build main, gate it, deploy if live differs, prove it
#   bash tools/agent-skills/deploy.sh --force    # deploy even when live already matches
#   bash tools/agent-skills/deploy.sh --dry-run  # build and gate only
#
# Needs: python3, node 20+, `gh auth login` (the build reads each skill repo), and wrangler access
# to the Cloudflare Pages project `skills`.
set -euo pipefail
cd "$(dirname "$0")/../.."

SITE=https://skillsmith.tech
PROJECT=skills
WRANGLER="npx --yes wrangler@4.151.1"
force=0 dry=0
for arg in "$@"; do
  case "$arg" in
    --force) force=1 ;;
    --dry-run) dry=1 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

say() { printf '\n== %s\n' "$*"; }

say "on main, level with origin"
git fetch -q origin main
if [ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ] || [ -n "$(git status --porcelain)" ]; then
  echo "This deploys exactly what is on origin/main. Run: git checkout main && git pull, with a clean tree." >&2
  exit 1
fi

say "gates (the same ones CI runs)"
python3 -m unittest discover -s tools/agent-skills/tests
python3 tools/agent-skills/gen_home.py --check
python3 tools/agent-skills/gen_page.py --check
python3 tools/agent-skills/build.py
python3 tools/agent-skills/gen_sitemap.py --write
bash tools/agent-skills/make_dist.sh
python3 tools/agent-skills/check_dist.py
node tools/agent-skills/verify.mjs local

live=$(curl -fsS "$SITE/version.json?v=$(date +%s)" || true)
if [ "$live" = "$(cat dist/version.json)" ] && [ "$force" = 0 ]; then
  say "live already matches main $(cat dist/version.json); nothing to deploy (--force to redeploy)"
  exit 0
fi
[ "$dry" = 1 ] && { say "dry run: built and gated, not deployed"; exit 0; }

say "cloudflare login"
if ! $WRANGLER whoami >/dev/null 2>&1; then
  echo "wrangler is not logged in. Run: npx wrangler login   (or export CLOUDFLARE_API_TOKEN in this shell)" >&2
  exit 1
fi

say "deploy dist/ to Pages project $PROJECT"
$WRANGLER pages deploy dist --project-name "$PROJECT" --branch main

say "prove the live site"
bust=$(git rev-parse --short HEAD)-$(date +%s)
CACHE_BUST="$bust" node tools/agent-skills/verify.mjs "$SITE"
python3 tools/agent-skills/prove.py --site "$SITE" --bust "$bust"
say "deployed main $(git rev-parse --short HEAD); the Deploy pending issue closes on the next hourly run"
