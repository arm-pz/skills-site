"""Shape-test public arm-pz repos and open one reviewed proposal PR per batch."""

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import gen_page
import skilllib

GH = os.environ.get("GH", "gh")
OWNER = "arm-pz"
KEYWORDS = {
    # First because agent skills often mention SEO or writing only in their
    # "not for" clause, which would otherwise claim them for another group.
    "outbound": ["cold", "outbound", "deliverability", "inbox", "prospect",
                 "mailbox"],
    "career": ["resume", "cv", "linkedin", "recruiter", "applicant", "job",
               "interview", "career", "promotion"],
    "skill-authoring": ["frontmatter", "authoring", "triggering"],
    "publish-discover": ["discover", "findable", "listing", "publish", "marketplace",
                         "stars", "installs"],
    "seo-search": ["seo", "keyword", "crawl", "cannibalization", "serp"],
    "ship-checks": ["release", "ship", "deploy", "security", "red-team", "preflight",
                    "audit", "performance", "verify", "code", "website"],
    "writing-growth": ["content", "copy", "edit", "write", "wordsmith", "newsletter",
                       "thread", "post"],
    "thinking-learning": ["teach", "learn", "study", "tutor", "explain", "decision",
                          "debate", "brainstorm", "research", "strategy", "data"],
}


def words(*parts):
    return set(re.findall(r"[a-z0-9]+", " ".join(parts).lower()))


def assign_group(name, description):
    tokens = words(name, description)
    text = f"{name} {description}".lower()
    for group, keywords in KEYWORDS.items():
        if tokens & set(keywords) or any(k in text for k in keywords if "-" in k):
            return group
    return "skill-authoring"


def assign_tag(group, name, description):
    tokens = words(name, description)
    if group in ("career", "outbound"):
        return group
    if group == "seo-search":
        return "seo"
    if group == "publish-discover":
        return "discovery" if tokens & {"discover", "findable", "listing"} else "publishing"
    if group == "writing-growth":
        return "editorial" if tokens & {"edit", "proofread", "wordsmith"} else "content"
    if group == "thinking-learning":
        if tokens & {"decisions", "decision", "strategy"}:
            return "decisions"
        if "arena" in tokens:
            return "arena"
        if tokens & {"research", "data", "sources"}:
            return "research"
        return "learning"
    if group == "ship-checks":
        if "performance" in tokens:
            return "performance"
        return "build" if tokens & {"code", "website", "prompt"} else "release"
    return "authoring"


def draft_blurb(description):
    text = " ".join(description.split())
    match = re.match(r"(.+?[.!?])(?:\s|$)", text)
    sentence = match.group(1) if match else text
    if len(sentence) > 240:
        sentence = sentence[:240].rsplit(" ", 1)[0].rstrip(" ,;:-") + "…"
    return sentence


def gh(*args, check=True):
    result = subprocess.run([GH, *args], capture_output=True, text=True)
    if check and result.returncode != 0:
        raise SystemExit(f"gh {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def list_repos():
    data = json.loads(gh("repo", "list", OWNER, "--limit", "1000",
                         "--json", "name,isFork,visibility"))
    return [r for r in data if r["visibility"].lower() == "public"]


def proposal_open():
    out = gh("pr", "list", "--state", "open", "--json", "headRefName",
             "--jq", ".[].headRefName")
    return any(line.startswith("proposal/") for line in out.split())


def fetch_files(repo):
    return skilllib.expand_tarball(gh_bytes(["api", f"repos/{OWNER}/{repo}/tarball"]))


def gh_bytes(args):
    result = subprocess.run([GH, *args], capture_output=True)
    if result.returncode != 0:
        raise SystemExit(f"gh {' '.join(args)} failed: "
                         f"{result.stderr.decode('utf-8', 'replace').strip()}")
    return result.stdout


def entry_point(files, path):
    """The file that describes what lives at path: a SKILL.md, or a mod's plugin.json."""
    prefix = "" if path == "." else path + "/"
    for rel in ("SKILL.md", ".claude-plugin/plugin.json"):
        if prefix + rel in files:
            return prefix + rel
    return None


def measure(repo, files, path):
    point = entry_point(files, path)
    if point is None:
        raise KeyError(f"no SKILL.md or .claude-plugin/plugin.json at {path}")
    text = files[point].decode("utf-8", "replace")
    fm = (skilllib.parse_frontmatter(text) if point.endswith("SKILL.md")
          else {"description": json.loads(text)["description"]})
    selected = skilllib.select_skill_files(files, path)
    blob = skilllib.pack(selected)
    commit = json.loads(gh("api", f"repos/{OWNER}/{repo}/commits/HEAD"))["sha"]
    license_id = gen_page.detect_license(
        files.get("LICENSE", b"").decode("utf-8", "replace"))
    return {
        "description": " ".join(fm["description"].split()),
        "files": [{"path": name,
                   "lines": data.count(b"\n"),
                   "bytes": len(data)}
                  for name, data in sorted(selected.items())],
        "fileCount": len(selected),
        "lines": sum(data.count(b"\n") for data in selected.values()),
        "bytes": len(blob),
        "license": license_id,
        "commit": commit,
        "sha256": skilllib.sha256_hex(blob),
    }, blob


def quality(files, path, sha, date):
    """What a page's quality block shows, read from the files at one commit."""
    point = entry_point(files, path)
    text = files[point].decode("utf-8", "replace") if point else ""
    if point and point.endswith("plugin.json"):
        data = json.loads(text)
        version, description = data.get("version"), data.get("description", "")
    else:
        version = skilllib.frontmatter_version(text)
        description = skilllib.parse_frontmatter(text).get("description", "") if text else ""
    _, _, _, nots = gen_page.split_description(description)
    return {"version": str(version) if version else None, "commit": sha[:7],
            "updated": date, "notFor": nots}


def candidate_entry(name, path, group, tag, source, order):
    title = skilllib.title_case(name)
    return {
        "name": name,
        "repo": f"{OWNER}/{name}",
        "path": path,
        "group": group,
        "tag": tag,
        "title": title,
        "pageTitle": skilllib.skill_page_title(title),
        "blurb": draft_blurb(source["description"]),
        "stats": (f'{source["fileCount"]} files · {source["lines"]:,} lines · '
                  f'{max(1, round(source["bytes"] / 1024))} KB'),
        "install": f"npx skills add {OWNER}/{name}",
        "page": "generated",
        "order": order,
        "pageSource": source,
    }


def bash_command():
    # Windows resolves bare "bash" to the WSL stub, which fails in a subprocess.
    if os.name == "nt":
        candidate = Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Git" / "bin" / "bash.exe"
        if candidate.is_file():
            return str(candidate)
    return "bash"


def run_gate(root):
    env = dict(os.environ, GH=GH)
    for cmd in (
        [sys.executable, "-m", "unittest", "discover",
         "-s", "tools/agent-skills/tests", "-v"],
        [sys.executable, "tools/agent-skills/build.py"],
        [sys.executable, "tools/agent-skills/gen_home.py", "--check"],
        [sys.executable, "tools/agent-skills/gen_page.py", "--check"],
        [sys.executable, "tools/agent-skills/gen_sitemap.py", "--write"],
        [bash_command(), "tools/agent-skills/make_dist.sh"],
        [sys.executable, "tools/agent-skills/check_dist.py"],
        ["node", "tools/agent-skills/verify.mjs", "local"],
    ):
        subprocess.run(cmd, cwd=root, check=True, env=env)


def main(argv=None):
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--report", action="store_true")
    mode.add_argument("--propose", action="store_true")
    parser.add_argument("--root", default=".")
    parser.add_argument("--only", metavar="NAMES",
                        help="propose only these comma-separated repos; the report lists all")
    parser.add_argument("--dry-run", action="store_true",
                        help="propose: write files locally, do not commit, push or open a PR")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    manifest = skilllib.load_manifest(root)
    deny = skilllib.load_deny(root)
    denied = {item["repo"] for item in deny}
    existing = {s["name"] for s in manifest["skills"]}
    only = ({n.strip() for n in args.only.split(",") if n.strip()}
            if args.only else None)

    repos = list_repos()
    report = []
    eligible = []
    seen = set()
    for repo in sorted(repos, key=lambda r: r["name"]):
        name = repo["name"]
        seen.add(name)
        if only is not None and name not in only:
            report.append((name, "skip", "not selected by --only"))
            continue
        if name in existing or repo["isFork"] or f"{OWNER}/{name}" in denied:
            report.append((name, "skip", "already published, fork, or denied"))
            continue
        try:
            files = fetch_files(name)
        except SystemExit as err:
            report.append((name, "error", str(err)))
            continue
        fails = skilllib.shape_failures(name, files,
                                        denied=denied, is_fork=repo["isFork"])
        report.append((name, "eligible" if not fails else "ineligible",
                       "; ".join(fails)))
        if not fails:
            eligible.append((name, files))

    if only is not None:
        missing = sorted(only - seen)
        if missing:
            raise SystemExit(f"--only names not found among public repos: {', '.join(missing)}")

    for name, status, reason in report:
        print(f"{name:<40} {status:<10} {reason}")
    if args.report:
        return 0

    if proposal_open():
        print("proposal already open; nothing to do")
        return 0
    if not eligible:
        print("no eligible repos")
        return 0
    if not args.dry_run and subprocess.run(
            ["git", "status", "--porcelain"], cwd=root, capture_output=True,
            text=True).stdout.strip():
        raise SystemExit("working tree is dirty; discovery must run from a clean checkout")

    deferred = []
    for name, files in eligible:
        try:
            sk = next(p for p in (f"{name}/SKILL.md", "SKILL.md", f"skills/{name}/SKILL.md")
                      if p in files)
            layout = "." if sk == "SKILL.md" else (
                "skills/" + name if sk.startswith("skills/") else name)
            source, _ = measure(name, files, layout)
            group = assign_group(name, source["description"])
            tag = assign_tag(group, name, source["description"])
            deferred.append((name, layout, group, tag, source))
        except SystemExit as err:
            print(f"DROPPED {name}: {err}", file=sys.stderr)

    if not deferred:
        print("no candidate survived measurement")
        return 1

    order = max(s["order"] for s in manifest["skills"])
    entries = []
    for name, layout, group, tag, source in deferred:
        order += 1
        entries.append(candidate_entry(name, layout, group, tag, source, order))
    manifest["skills"].extend(entries)
    skilllib.validate_manifest(manifest)
    with open(root / "site" / "skills.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    written = gen_page.write_pages(root, manifest)
    subprocess.run([sys.executable, str(root / "tools/agent-skills/gen_home.py"),
                    "--write", "--root", str(root)], check=True)
    run_gate(root)

    if args.dry_run:
        print(f"dry run: {len(written)} pages written, manifest updated, nothing committed")
        return 0

    branch = f"proposal/{dt.date.today().isoformat()}"
    names = [e["name"] for e in entries]
    subprocess.run(["git", "switch", "-c", branch], cwd=root, check=True)
    paths = ["site/skills.json", "index.html", *written]
    subprocess.run(["git", "add", *paths], cwd=root, check=True)
    subprocess.run(["git", "commit", "-m",
                    f"propose {len(names)} skill(s): {', '.join(names)}"],
                   cwd=root, check=True)
    subprocess.run(["git", "push", "-u", "origin", branch], cwd=root, check=True)
    body = "\n\n".join(
        f"### {e['title']} (`{e['repo']}`)\n"
        f"- group/tag: `{e['group']}` / `{e['tag']}`\n"
        f"- install: `{e['install']}`\n"
        f"- digest: `sha256:{e['pageSource']['sha256']}`\n"
        f"- measured: {e['pageSource']['fileCount']} files, "
        f"{e['pageSource']['lines']} lines, {e['pageSource']['bytes']} bytes\n"
        f"- [ ] correct group/tag/copy if needed, then regenerate with "
        f"`gen_page.py --write && gen_home.py --write`"
        for e in entries)
    subprocess.run([GH, "pr", "create", "--title",
                    f"Propose {len(names)} new skill(s)", "--body",
                    "Discovery found eligible repos. Merging publishes them.\n\n" + body,
                    "--head", branch], cwd=root, check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
