"""One-time migration: seed site/skills.json and site/deny.json from live files.

Not part of the recurring build. Refuses to read a working tree whose seed
inputs differ from HEAD, so the manifest records committed bytes.
"""

import argparse
import ast
import hashlib
import html
import json
import re
import shutil
import subprocess
from pathlib import Path

import skilllib

ROOT_LAYOUT = {"draft-skill", "tune-skill", "prompts-to-skill", "prompts-to-skill-release"}
LEGACY = {"release-gate", "publish-release-gate"}
NONE_META = {
    "upstream-check": ("skill-authoring", "authoring"),
    "release-gate": ("ship-checks", "release"),
    "publish-release-gate": ("ship-checks", "release"),
}
DENY = [{
    "repo": "arm-pz/job-application-agent",
    "reason": "Third-party skill that fills and submits applications and transmits candidate data by default.",
}]
SEED_INPUTS = ["index.html", "agent-skills/index.json", "tools/agent-skills/build.py"]

GROUP_RE = re.compile(
    r'<div class="sk-group" id="([^"]+)">\s*<h2>(.*?)</h2>\s*'
    r'<span>\d+ skills · (.*?)</span>\s*</div>', re.S)
CARD_RE = re.compile(
    r'<div class="skill" id="([^"]+)">\s*<div class="sk-id">\s*'
    r'<a class="sk-name" href="[^"]+">[^<]+</a>\s*'
    r'<span class="sk-tag">(.*?)</span>\s*</div>\s*<div class="sk-body">\s*'
    r'<p>(.*?)</p>\s*<p class="sk-stats">(.*?)</p>\s*'
    r'<p class="sk-install mono">(.*?)</p>', re.S)


def parse_build_paths(text):
    tree = ast.parse(text)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "REPOS" for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit("build.py has no REPOS map")


def parse_hub(text):
    groups, cards = [], []
    starts = list(GROUP_RE.finditer(text))
    foot = text.index('<p class="foot-note">')
    for index, match in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else foot
        block = text[match.end():end]
        groups.append({
            "id": match.group(1),
            "title": html.unescape(match.group(2)),
            "descriptor": html.unescape(match.group(3)).strip(),
        })
        for card in CARD_RE.finditer(block):
            cards.append({
                "name": card.group(1),
                "group": match.group(1),
                "tag": card.group(2),
                "blurb": html.unescape(card.group(3)),
                "stats": html.unescape(card.group(4)),
                "install": html.unescape(card.group(5)),
            })
    return groups, cards


def build_seed(root):
    root = Path(root)
    index = json.loads((root / "agent-skills" / "index.json").read_text(encoding="utf-8"))
    hub = (root / "index.html").read_text(encoding="utf-8")
    build_paths = parse_build_paths(
        (root / "tools" / "agent-skills" / "build.py").read_text(encoding="utf-8"))
    groups, cards = parse_hub(hub)
    for order, group in enumerate(groups, 1):
        group["order"] = order

    descriptions = {entry["name"]: entry["description"] for entry in index["skills"]}
    carded = {card["name"] for card in cards}
    skills, order = [], 0

    def base(name, group, tag):
        entry = {
            "name": name,
            "repo": None if name in LEGACY else f"arm-pz/{name}",
            "path": None if name in LEGACY else build_paths.get(name, "."),
            "group": group,
            "tag": tag,
            "title": skilllib.title_case(name),
            "page": "bespoke" if (root / name / "index.html").is_file() else "none",
            "order": order,
        }
        if name in LEGACY:
            source = root / "agent-skills" / f"{name}.tar.gz"
            blob = source.read_bytes()
            target = root / "site" / "legacy" / f"{name}.tar.gz"
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            entry["legacy"] = {
                "archive": f"{name}.tar.gz",
                "sha256": hashlib.sha256(blob).hexdigest(),
                "description": descriptions[name],
            }
        return entry

    for card in cards:
        order += 1
        entry = base(card["name"], card["group"], card["tag"])
        entry["order"] = order
        entry["blurb"] = card["blurb"]
        entry["stats"] = card["stats"]
        entry["install"] = card["install"]
        skills.append(entry)

    for entry in index["skills"]:
        if entry["name"] in carded:
            continue
        order += 1
        group, tag = NONE_META.get(entry["name"], ("skill-authoring", "authoring"))
        item = base(entry["name"], group, tag)
        item["order"] = order
        skills.append(item)

    manifest = {"schema": skilllib.SCHEMA, "site": skilllib.SITE,
                "groups": groups, "skills": skills}
    return manifest, DENY


def assert_clean_inputs(root):
    result = subprocess.run(
        ["git", "status", "--porcelain", "--", *SEED_INPUTS],
        cwd=root, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"git status failed: {result.stderr.strip()}")
    if result.stdout.strip():
        raise SystemExit("seed inputs are modified in the working tree; commit or stash first:\n"
                         + result.stdout)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    assert_clean_inputs(root)
    manifest, deny = build_seed(root)
    skilllib.validate_manifest(manifest)
    (root / "site").mkdir(exist_ok=True)
    with open(root / "site" / "skills.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    with open(root / "site" / "deny.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump(deny, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"site/skills.json: {len(manifest['skills'])} skills, "
          f"{len(manifest['groups'])} groups")
    print(f"site/deny.json: {len(deny)} repos")


if __name__ == "__main__":
    main()
