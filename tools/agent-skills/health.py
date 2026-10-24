"""Nightly skill health: run tune-skill's regress.py over every published skill.

    python tools/agent-skills/health.py                 # compare with site/health.json, exit 1 on regression
    python tools/agent-skills/health.py --accept        # also record improvements when nothing regressed
    python tools/agent-skills/health.py --report FILE   # write the regress output as markdown

Each repo-backed entry in site/skills.json is fetched at its default-branch HEAD and the skill
folder is unpacked under its name, so the family checked here is exactly what the site publishes.
tune-skill's own scripts come from arm-pz/tune-skill at HEAD, so a fix to the checker reaches this
job without a copy. Skills that the family hands off to but that live elsewhere are listed in
EXTERNAL; anything else a description sends work to must exist.
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

import skilllib
from build import gh

EXTERNAL = [
    "seo-audit", "programmatic-seo",          # coreyhaines31/marketingskills
    "skill-creator", "plugin-authoring",      # built into the agents
    "job-application-agent",                  # third-party, denied in site/deny.json
]


def unpack(files, dest):
    for rel, data in files.items():
        path = dest / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def stage(manifest, family, tools, fetch):
    tune = skilllib.expand_tarball(fetch("arm-pz/tune-skill"))
    unpack({k: v for k, v in tune.items() if k.startswith("scripts/")}, tools)
    for skill in manifest["skills"]:
        if skill.get("repo") is None or skill.get("kind") == "mod":
            continue
        files = skilllib.select_skill_files(skilllib.expand_tarball(fetch(skill["repo"])), skill["path"])
        unpack(files, family / skill["name"])
    legacy = [s["name"] for s in manifest["skills"] if s.get("repo") is None]
    return EXTERNAL + legacy


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--accept", action="store_true",
                        help="record improvements when nothing regressed")
    parser.add_argument("--accept-all", action="store_true",
                        help="record the current state even with regressions (after review)")
    parser.add_argument("--report")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    manifest = skilllib.load_manifest(root)
    baseline = root / "site" / "health.json"

    with tempfile.TemporaryDirectory() as tmp:
        family, tools = Path(tmp) / "family", Path(tmp) / "tune-skill"
        external = stage(manifest, family, tools, lambda repo: gh(f"repos/{repo}/tarball"))
        if not (tools / "scripts" / "regress.py").is_file():
            print("arm-pz/tune-skill has no scripts/regress.py on its default branch yet; skipped")
            return 0
        cmd = [sys.executable, "-I", str(tools / "scripts" / "regress.py"), str(family),
               "--baseline", str(baseline), "--external", ",".join(external)]
        run = subprocess.run(cmd, capture_output=True, text=True)
        print(run.stdout, end="")
        print(run.stderr, end="", file=sys.stderr)
        regressed = run.returncode != 0
        if args.report:
            with open(args.report, "w", encoding="utf-8") as fh:
                fh.write("Nightly `regress.py` over every skill published on skills.caffeinity.com.\n\n")
                fh.write("```\n" + run.stdout + "```\n\n")
                fh.write("Fix each regression in its repo with tune-skill; the next nightly run "
                         "records the fix. If a regression is intended, accept it with "
                         "`python tools/agent-skills/health.py --accept-all` and commit "
                         "`site/health.json`.\n")
        if args.accept_all or (args.accept and not regressed and "0 improvements" not in run.stdout):
            subprocess.run(cmd + ["--write"], check=True, capture_output=True)
            print(f"baseline updated: {baseline.relative_to(root)}")
            return 0
    return 1 if regressed else 0


if __name__ == "__main__":
    sys.exit(main())
