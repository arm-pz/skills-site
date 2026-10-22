"""Build the discovery artifacts from site/skills.json.

Repo-backed entries are fetched from GitHub at their current HEAD and packed
deterministically. Legacy entries are copied from site/legacy and checked
against their pinned digest. Nothing is written unless every entry succeeds.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import skilllib

GH = os.environ.get("GH", "gh")
OUT = os.environ.get("OUT", "out")


def gh(*args):
    result = subprocess.run([GH, "api", *args], capture_output=True)
    if result.returncode != 0:
        raise SystemExit(f"gh api {' '.join(args)} failed: "
                         f"{result.stderr.decode('utf-8', 'replace').strip()}")
    return result.stdout


def repo_about(repo):
    data = json.loads(gh(f"repos/{repo}").decode("utf-8"))
    return data.get("description")


def check_about(repo, description):
    if not isinstance(description, str) or not description.strip():
        raise SystemExit(f"{repo}: the repository About is empty; set it before building")
    description = " ".join(description.split())
    if len(description) > 1024:
        raise SystemExit(f"{repo}: repo About is {len(description)} characters (max 1024)")
    return description


def build(manifest, out_dir, tarball_fetch, about_fetch, legacy_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    entries = []
    for skill in skilllib.archived(manifest):
        name = skill["name"]
        if skill["repo"] is None:
            archive = Path(legacy_dir) / skill["legacy"]["archive"]
            if not archive.is_file():
                raise SystemExit(f"{name}: legacy archive {archive} is missing")
            blob = archive.read_bytes()
            digest = skilllib.sha256_hex(blob)
            if digest != skill["legacy"]["sha256"]:
                raise SystemExit(f"{name}: legacy digest mismatch: "
                                 f"{digest} != {skill['legacy']['sha256']}")
            description = skill["legacy"]["description"]
        else:
            full = skilllib.expand_tarball(tarball_fetch(skill["repo"]))
            files = skilllib.select_skill_files(full, skill["path"])
            if "SKILL.md" not in files:
                raise SystemExit(f"{name}: no SKILL.md under {skill['path']!r}")
            try:
                fm = skilllib.parse_frontmatter(files["SKILL.md"].decode("utf-8", "replace"))
            except skilllib.ManifestError as exc:
                raise SystemExit(f"{name}: {exc}") from exc
            if not (fm.get("description") or "").strip():
                raise SystemExit(f"{name}: SKILL.md description is empty")
            blob = skilllib.pack(files)
            digest = skilllib.sha256_hex(blob)
            description = check_about(skill["repo"], about_fetch(skill["repo"]))
        with open(out_dir / f"{name}.tar.gz", "wb") as fh:
            fh.write(blob)
        entries.append({
            "name": name,
            "description": description,
            "type": "archive",
            "url": f"{skilllib.SITE}/agent-skills/{name}.tar.gz",
            "digest": f"sha256:{digest}",
        })
        print(f"{name:<32} {len(blob):>7} B  {digest[:12]}...")

    if len(entries) != len(skilllib.archived(manifest)):
        raise SystemExit("shrink guard: built entries do not match the manifest")
    entries.sort(key=lambda entry: entry["name"])
    index = {"$schema": skilllib.INDEX_SCHEMA, "skills": entries}
    with open(out_dir / "index.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump(index, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"index.json: {len(entries)} skills")
    return entries


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    root = Path(args.root)
    manifest = skilllib.load_manifest(root)
    skilllib.validate_manifest(manifest)
    build(manifest, root / OUT,
          tarball_fetch=lambda repo: gh(f"repos/{repo}/tarball"),
          about_fetch=repo_about,
          legacy_dir=root / "site" / "legacy")
    return 0


if __name__ == "__main__":
    sys.exit(main())
