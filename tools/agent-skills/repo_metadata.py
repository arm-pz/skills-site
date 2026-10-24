#!/usr/bin/env python3
"""Give every published repo the GitHub metadata directories crawl: topics and a homepage.

    python tools/agent-skills/repo_metadata.py            # show what would change (needs `gh auth login`)
    python tools/agent-skills/repo_metadata.py --apply    # apply it
    python tools/agent-skills/repo_metadata.py --apply --about   # also set About text findable wrote

Additive only: a topic is added when missing (never removed, GitHub's cap of 20 respected) and the
homepage is set to the skill's page only when it is empty. The About text changes only with --about,
and only for entries whose `githubAbout` (written by findable, in site/skills.json) differs from it. Run it from your own machine: Claude Code cloud sessions cannot write repo
settings. Safe to re-run whenever a skill is added.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import skilllib

SKILL_TOPICS = ["agent-skills", "claude-code", "claude-skills", "skill-md", "codex", "cursor"]
MOD_TOPICS = ["claude-code", "claude-code-plugin", "claude-code-mod", "agent-skills"]
MARKETPLACE = "arm-pz/caffeinity-skills"
MARKETPLACE_TOPICS = ["claude-code-plugin", "plugin-marketplace", "codex-plugin", "agent-skills", "claude-skills"]


def wanted(manifest):
    """{repo: (topics, homepage, about or None)} for every repo the site publishes."""
    out = {MARKETPLACE: (MARKETPLACE_TOPICS, f"{skilllib.SITE}/", None)}
    for s in manifest["skills"]:
        repo = s.get("repo")
        if not repo or repo in out:
            continue
        topics = list(MOD_TOPICS if s.get("kind") == "mod" else SKILL_TOPICS) + s.get("githubTopics", [])
        out[repo] = (topics, f"{skilllib.SITE}/{s['name']}/", s.get("githubAbout"))
    return out


def plan(current, topics, homepage):
    have = list(current.get("topics") or [])
    add = [t for t in topics if t not in have][: max(0, 20 - len(have))]
    home = homepage if not (current.get("homepage") or "").strip() else None
    return have, add, home


def gh(*args, data=None):
    p = subprocess.run(["gh", *args], input=data, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(p.stderr.strip() or p.stdout.strip())
    return p.stdout


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--about", action="store_true", help="also replace About text with githubAbout")
    ap.add_argument("--root", default=".")
    a = ap.parse_args(argv)
    manifest = json.loads((Path(a.root) / "site" / "skills.json").read_text(encoding="utf-8"))
    changes = failures = 0
    for repo, (topics, homepage, about) in sorted(wanted(manifest).items()):
        try:
            current = json.loads(gh("api", f"repos/{repo}"))
        except RuntimeError as e:
            print(f"skip   {repo}: {e}")
            failures += 1
            continue
        have, add, home = plan(current, topics, homepage)
        new_about = about if a.about and about and about != (current.get("description") or "") else None
        if not add and not home and not new_about:
            continue
        changes += 1
        print(f"{'apply' if a.apply else 'would'}  {repo}: "
              + ", ".join(filter(None, [f"+topics {' '.join(add)}" if add else "",
                                        f"homepage {home}" if home else "",
                                        f"about {new_about!r}" if new_about else ""])))
        if not a.apply:
            continue
        try:
            if add:
                gh("api", "-X", "PUT", f"repos/{repo}/topics", "--input", "-",
                   data=json.dumps({"names": have + add}))
            if home:
                gh("api", "-X", "PATCH", f"repos/{repo}", "-f", f"homepage={home}")
            if new_about:
                gh("api", "-X", "PATCH", f"repos/{repo}", "-f", f"description={new_about}")
        except RuntimeError as e:
            print(f"failed {repo}: {e}")
            failures += 1
    print(f"\n{changes} repos {'changed' if a.apply else 'to change'}"
          + ("" if a.apply or not changes else "; rerun with --apply") + (f", {failures} failed" if failures else ""))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
