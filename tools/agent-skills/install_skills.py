"""Install skills from site/skills.json into ~/.claude/skills, for a fresh workspace.

    python tools/agent-skills/install_skills.py tune-skill seo-crawl   # these skills
    python tools/agent-skills/install_skills.py --all                  # every skill (mods and legacy archives excluded)
    python tools/agent-skills/install_skills.py --list                 # what could be installed

A cloud session starts with an empty workspace, so a skill that is public on GitHub is still not
callable until something installs it. Put this in the environment's setup script and every new
session has them. A skill that fails to install is reported and skipped; the exit code stays 0 so a
GitHub hiccup never stops a session from starting.
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import skilllib

DEFAULT = ["caffeinity-routing", "draft-skill", "tune-skill", "prompts-to-skill-release",
           "findable", "upstream-check", "seo-crawl", "keyword-guard", "web-preflight"]


def installable(manifest):
    """Entries that are a plain skill in a public repo: not a mod, not a pinned legacy archive."""
    return {s["name"]: s for s in manifest["skills"]
            if s.get("repo") and s.get("kind", "skill") == "skill" and s.get("path") is not None}


def plan(manifest, names, everything=False):
    """(entries to install, names that are not installable skills)."""
    available = installable(manifest)
    if everything:
        names = list(available)
    chosen = [available[n] for n in names if n in available]
    return chosen, [n for n in names if n not in available]


def git_clone(repo, dest):
    result = subprocess.run(["git", "clone", "--depth", "1", "--quiet",
                             f"https://github.com/{repo}", str(dest)],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git clone {repo} failed")


def install(entries, target, clone=git_clone):
    """Copy each skill folder into target/<name>. Returns (installed names, {name: reason})."""
    target = Path(target)
    target.mkdir(parents=True, exist_ok=True)
    done, failed = [], {}
    with tempfile.TemporaryDirectory() as tmp:
        checkouts = {}
        for entry in entries:
            name, repo = entry["name"], entry["repo"]
            try:
                if repo not in checkouts:
                    checkouts[repo] = Path(tmp) / repo.replace("/", "__")
                    clone(repo, checkouts[repo])
                source = checkouts[repo] / (entry["path"] if entry["path"] != "." else "")
                if not (source / "SKILL.md").is_file():
                    raise RuntimeError(f"no SKILL.md at {entry['path']}")
                dest = target / name
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(source, dest, ignore=shutil.ignore_patterns(".git"))
                done.append(name)
            except (RuntimeError, OSError) as exc:
                failed[name] = str(exc)
    return done, failed


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("names", nargs="*", help=f"skills to install (default: {' '.join(DEFAULT)})")
    parser.add_argument("--all", action="store_true", help="every plain skill in the manifest")
    parser.add_argument("--list", action="store_true", help="print the installable skills and stop")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--target", default=str(Path.home() / ".claude" / "skills"))
    args = parser.parse_args(argv)
    manifest = skilllib.load_manifest(Path(args.root))
    if args.list:
        print("\n".join(sorted(installable(manifest))))
        return 0
    entries, unknown = plan(manifest, args.names or DEFAULT, everything=args.all)
    for name in unknown:
        print(f"skip {name}: not a plain skill in site/skills.json (mods and legacy archives are not installed)",
              file=sys.stderr)
    done, failed = install(entries, args.target)
    for name, reason in failed.items():
        print(f"FAILED {name}: {reason}", file=sys.stderr)
    print(f"installed {len(done)} skill{'' if len(done) == 1 else 's'} into {args.target}: {' '.join(done) or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
