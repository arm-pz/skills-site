"""Bring site/skills.json in line with what is live on GitHub, without a human merge.

    python tools/agent-skills/sync.py            # report what would change
    python tools/agent-skills/sync.py --write    # apply it, then regenerate the hub and pages

Ground truth is every public, non-fork arm-pz repo that ships one SKILL.md and passes the shape
test. For each manifest entry and each such repo, sync decides one of:

  add       an eligible repo with no entry gets a generated page
  refresh   a generated page whose repo HEAD moved is re-measured; hand-written copy is kept
  rename    the repo answers under a new name; the entry, its page folder and the workflows follow,
            and the old name becomes an alias that _redirects sends to the new page
  remove    the repo is gone or private (the API says Not Found); the entry and a generated page go
  hold      something needs a person: an empty About, a failed shape test, a bespoke page whose
            copy may still use the old name. Reported, never guessed at.

Bespoke pages are moved on a rename but never edited. Denied repos never publish.
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import discover
import gen_home
import gen_page
import skilllib

OWNER = discover.OWNER


def gh_json(*args):
    out = subprocess.run([discover.GH, *args], capture_output=True, text=True)
    if out.returncode != 0:
        return None, out.stderr.strip()
    return json.loads(out.stdout), None


def live_repos():
    data, err = gh_json("repo", "list", OWNER, "--limit", "1000", "--json",
                        "name,isFork,visibility,isArchived,description")
    if data is None:
        raise SystemExit(f"cannot list {OWNER} repos: {err}")
    return {r["name"]: r for r in data if r["visibility"].lower() == "public" and not r["isFork"]}


def resolve(repo):
    """('same'|'renamed'|'gone', current full name). Unreadable is an error, never 'gone'."""
    data, err = gh_json("api", f"repos/{repo}")
    if data is None:
        if "Not Found" in err or "HTTP 404" in err:
            return "gone", None
        raise SystemExit(f"cannot read {repo}: {err}")
    if data.get("private"):
        return "gone", None
    full = data["full_name"]
    return ("same" if full.lower() == repo.lower() else "renamed"), full


def has_skill_md(name):
    """Cheap pre-check from the git tree, so non-skill repos are never downloaded."""
    data, err = gh_json("api", f"repos/{OWNER}/{name}/git/trees/HEAD?recursive=1")
    if data is None:
        return "Git Repository is empty" not in err and "Not Found" not in err
    return any(i["path"] == "SKILL.md" or i["path"].endswith("/SKILL.md") for i in data.get("tree", []))


def head_sha(repo):
    data, err = gh_json("api", f"repos/{repo}/commits/HEAD")
    if data is None:
        raise SystemExit(f"cannot read HEAD of {repo}: {err}")
    return data["sha"]


def locate(name, files):
    sk = next((p for p in (f"{name}/SKILL.md", "SKILL.md", f"skills/{name}/SKILL.md") if p in files), None)
    if sk is None:
        found = [p for p in files if p.endswith("/SKILL.md")]
        sk = found[0] if len(found) == 1 else None
    if sk is None:
        return None
    return "." if sk == "SKILL.md" else sk[: -len("/SKILL.md")]


def drop_from_workflows(manifest, name):
    for flow in manifest.get("workflows", []):
        for step in flow["steps"]:
            step["skills"] = [n for n in step["skills"] if n != name]
        flow["steps"] = [s for s in flow["steps"] if s["skills"]]
    manifest["workflows"] = [f for f in manifest.get("workflows", []) if f["steps"]]


def rename_in_workflows(manifest, old, new):
    for flow in manifest.get("workflows", []):
        for step in flow["steps"]:
            step["skills"] = [new if n == old else n for n in step["skills"]]


def plan(root, manifest, deny):
    repos = live_repos()
    denied = {d["repo"] for d in deny}
    actions = []
    known = set()
    for entry in manifest["skills"]:
        repo = entry.get("repo")
        if repo is None:
            known.add(entry["name"])  # a pinned legacy archive owns its name
            continue
        short = repo.split("/", 1)[1]
        known.add(short)
        if short not in repos:
            state, full = resolve(repo)
            if state == "gone":
                actions.append(("remove", entry["name"], f"{repo} is gone or private"))
                continue
            if state == "renamed":
                known.add(full.split("/", 1)[1])
                actions.append(("rename", entry["name"], full))
                continue
        if entry["page"] == "generated":
            sha = head_sha(repo)
            if sha != entry["pageSource"]["commit"]:
                actions.append(("refresh", entry["name"], sha))
    for name, r in sorted(repos.items()):
        if name in known or f"{OWNER}/{name}" in denied:
            continue
        if not has_skill_md(name):
            continue
        files = discover.fetch_files(name)
        fails = skilllib.shape_failures(name, files, denied=frozenset(denied), is_fork=r["isFork"])
        if fails:
            if any(p.endswith("SKILL.md") for p in files):
                actions.append(("hold", name, "; ".join(fails)))
            continue
        if not (r.get("description") or "").strip():
            actions.append(("hold", name, "repository About is empty; the build needs it"))
            continue
        actions.append(("add", name, files))
    return actions


def apply(root, manifest, actions):
    by_name = {s["name"]: s for s in manifest["skills"]}
    notes = []
    for kind, name, detail in actions:
        if kind == "remove":
            entry = by_name.pop(name)
            drop_from_workflows(manifest, name)
            if entry["page"] == "generated" and (root / name).is_dir():
                shutil.rmtree(root / name)
            elif entry["page"] == "bespoke":
                notes.append(f"{name}: bespoke page folder kept in git but no longer published")
        elif kind == "rename":
            entry = by_name.pop(name)
            new_repo = detail.split("/", 1)[1]
            files = discover.fetch_files(new_repo)
            path = locate(new_repo, files)
            if path is None:
                by_name[name] = entry
                notes.append(f"{name}: renamed to {detail} but its SKILL.md could not be located; held")
                continue
            # Keep the old entry name when the skill folder inside the repo kept it.
            new_name = name if path.endswith(f"skills/{name}") or path == name else new_repo
            entry["repo"] = detail
            entry["path"] = path
            entry["install"] = entry.get("install", "").replace(f"{OWNER}/{name}", detail)
            if new_name != name:
                entry["name"] = new_name
                entry["aliases"] = sorted(set(entry.get("aliases", [])) | {name})
                rename_in_workflows(manifest, name, new_name)
                if (root / name).is_dir() and not (root / new_name).exists():
                    (root / name).rename(root / new_name)
                if entry["page"] == "bespoke":
                    notes.append(f"{new_name}: bespoke page moved from /{name}/; its copy may still say '{name}'")
            if entry["page"] == "generated":
                entry["pageSource"], _ = discover.measure(new_repo, files, path)
            by_name[entry["name"]] = entry
        elif kind == "refresh":
            entry = by_name[name]
            short = entry["repo"].split("/", 1)[1]
            files = discover.fetch_files(short)
            path = (locate(name, files) if short == name else None) or entry["path"]
            if path != "." and f"{path}/SKILL.md" not in files or path == "." and "SKILL.md" not in files:
                notes.append(f"{name}: SKILL.md is no longer at {path}; page not refreshed")
                continue
            entry["path"] = path
            entry["pageSource"], _ = discover.measure(short, files, path)
            entry["stats"] = (f'{entry["pageSource"]["fileCount"]} files · '
                              f'{entry["pageSource"]["lines"]:,} lines · '
                              f'{max(1, round(entry["pageSource"]["bytes"] / 1024))} KB')
        elif kind == "add":
            files = detail
            path = locate(name, files)
            source, _ = discover.measure(name, files, path)
            group = discover.assign_group(name, source["description"])
            tag = discover.assign_tag(group, name, source["description"])
            order = max([s["order"] for s in by_name.values()] + [0]) + 1
            by_name[name] = discover.candidate_entry(name, path, group, tag, source, order)
        elif kind == "hold":
            notes.append(f"{name}: held, {detail}")
    manifest["skills"] = sorted(by_name.values(), key=lambda s: s["order"])
    skilllib.validate_manifest(manifest)
    return notes


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--summary", help="append a markdown summary to this file")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    manifest = skilllib.load_manifest(root)
    skilllib.validate_manifest(manifest)
    actions = plan(root, manifest, skilllib.load_deny(root))

    lines = [f"{kind:<8} {name:<34} {detail if isinstance(detail, str) else ''}".rstrip()
             for kind, name, detail in actions]
    print("\n".join(lines) or "in sync: nothing to change")
    notes = []
    if args.write and any(kind != "hold" for kind, _, _ in actions):
        notes = apply(root, manifest, actions)
        with open(root / "site" / "skills.json", "w", encoding="utf-8", newline="\n") as fh:
            json.dump(manifest, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        gen_page.main(["--write", "--root", str(root)])
        gen_home.main(["--write", "--root", str(root)])
    elif args.write:
        notes = [f"{name}: held, {detail}" for kind, name, detail in actions if kind == "hold"]
    for note in notes:
        print(f"NOTE {note}")
    if args.summary:
        with open(args.summary, "a", encoding="utf-8") as fh:
            fh.write("## sync\n\n" + ("\n".join(f"- `{l}`" for l in lines) or "- in sync") + "\n")
            fh.writelines(f"- note: {n}\n" for n in notes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
