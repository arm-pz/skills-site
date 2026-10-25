"""Shared manifest, frontmatter, shape-test and packing helpers."""

import gzip
import io
import json
import re
import tarfile
from pathlib import Path

SCHEMA = 1
SITE = "https://skills.caffeinity.com"
# Hand-written pages served at /<name>/, beside the hub and the skill pages.
STATIC_PAGES = ["work"]
INDEX_SCHEMA = "https://schemas.agentskills.io/discovery/0.2.0/schema.json"
NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
GROUP_IDS = ("start-here", "writing-growth", "career", "thinking-learning", "skill-authoring",
             "publish-discover", "ship-checks", "seo-search", "outbound")
TAGS = ("editorial", "seo", "discovery", "career", "learning", "arena",
        "decisions", "authoring", "release", "performance", "outbound",
        "routing", "build", "content", "research", "publishing")
PAGE_KINDS = ("bespoke", "generated", "none")
# A mod is a Claude Code plugin with no SKILL.md: it gets a page but no archive.
KINDS = ("skill", "mod")
REPO_META = {"README.md", "LICENSE", "LICENSE.md", "CHANGELOG.md", "CONTRIBUTING.md"}
REPO_META_DIRS = {".claude-plugin", ".github", ".git", "tests"}


class ManifestError(ValueError):
    pass


def _req(cond, message):
    if not cond:
        raise ManifestError(message)


def valid_name(name):
    return (isinstance(name, str) and bool(NAME_RE.match(name))
            and not name.startswith("-") and not name.endswith("-") and "--" not in name)


def archived(manifest):
    """Entries packed as skill archives and listed in the discovery index."""
    return [s for s in manifest["skills"] if s.get("kind", "skill") == "skill"]


def load_manifest(root):
    return json.loads((Path(root) / "site" / "skills.json").read_text(encoding="utf-8"))


def load_deny(root):
    path = Path(root) / "site" / "deny.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def validate_manifest(data):
    _req(isinstance(data, dict), "manifest must be an object")
    _req(data.get("schema") == SCHEMA, f"schema must be {SCHEMA}")
    _req(data.get("site") == SITE, f"site must be {SITE}")
    groups = data.get("groups")
    _req(isinstance(groups, list) and groups, "groups must be a non-empty list")
    gids, gorders = set(), set()
    for g in groups:
        _req(isinstance(g, dict), "group must be an object")
        _req(g.get("id") in GROUP_IDS, f"unknown group id {g.get('id')!r}")
        _req(g["id"] not in gids, f"duplicate group id {g['id']!r}")
        gids.add(g["id"])
        _req(isinstance(g.get("title"), str) and g["title"].strip(), f"group {g['id']} needs a title")
        _req(isinstance(g.get("descriptor"), str) and g["descriptor"].strip(),
             f"group {g['id']} needs a descriptor")
        _req(isinstance(g.get("order"), int) and g["order"] not in gorders,
             f"group {g['id']} needs a unique integer order")
        gorders.add(g["order"])

    skills = data.get("skills")
    _req(isinstance(skills, list) and skills, "skills must be a non-empty list")
    names, orders = set(), set()
    for s in skills:
        _req(isinstance(s, dict), "skill must be an object")
        name = s.get("name")
        _req(valid_name(name), f"bad skill name {name!r}")
        _req(name not in names, f"duplicate skill name {name!r}")
        _req(name not in STATIC_PAGES, f"skill name {name!r} is taken by a static page")
        names.add(name)
        _req(s.get("group") in gids, f"{name}: unknown group {s.get('group')!r}")
        _req(s.get("tag") in TAGS, f"{name}: unknown tag {s.get('tag')!r}")
        _req(isinstance(s.get("title"), str) and s["title"].strip(), f"{name}: title required")
        _req(isinstance(s.get("order"), int) and s["order"] not in orders,
             f"{name}: order must be a unique integer")
        orders.add(s["order"])
        page = s.get("page")
        _req(page in PAGE_KINDS, f"{name}: page must be one of {PAGE_KINDS}")
        kind = s.get("kind", "skill")
        _req(kind in KINDS, f"{name}: kind must be one of {KINDS}")
        if kind == "mod":
            _req(s.get("repo") is not None, f"{name}: a mod needs a repo")
            _req(page in ("bespoke", "generated"), f"{name}: a mod page must be bespoke or generated")
        if page != "none":
            _req(isinstance(s.get("blurb"), str) and s["blurb"].strip(),
                 f"{name}: blurb required when page is not none")
            _req(isinstance(s.get("stats"), str) and s["stats"].strip(),
                 f"{name}: stats required when page is not none")

        repo = s.get("repo")
        if repo is None:
            _req(page != "generated", f"{name}: legacy entries cannot be generated")
            legacy = s.get("legacy")
            _req(isinstance(legacy, dict), f"{name}: legacy entries need legacy")
            _req(isinstance(legacy.get("archive"), str) and legacy["archive"],
                 f"{name}: legacy.archive required")
            _req(isinstance(legacy.get("sha256"), str)
                 and re.fullmatch(r"[a-f0-9]{64}", legacy["sha256"]),
                 f"{name}: legacy.sha256 must be 64 lowercase hex")
            _req(isinstance(legacy.get("description"), str) and legacy["description"].strip(),
                 f"{name}: legacy.description required")
            _req(s.get("path") is None, f"{name}: legacy entries must have path null")
        elif repo == f"arm-pz/{name}":
            _req(s.get("path") in (".", name, f"skills/{name}"),
                 f"{name}: path must be '.', '{name}' or 'skills/{name}'")
        else:
            # A skill or mod bundled inside another repo, such as a marketplace plugin.
            _req(re.fullmatch(r"arm-pz/[A-Za-z0-9._-]+", str(repo)),
                 f"{name}: repo must be arm-pz/{name} or another arm-pz repo")
            if kind == "mod":
                _req(str(s.get("path", "")).rstrip("/").split("/")[-1] == name,
                     f"{name}: a mod in another repo needs a path ending in '/{name}'")
            else:
                _req(str(s.get("path", "")).endswith(f"skills/{name}"),
                     f"{name}: a skill in another repo needs a path ending in 'skills/{name}'")

        if page == "generated":
            src = s.get("pageSource")
            _req(isinstance(src, dict), f"{name}: generated pages need pageSource")
            _req(isinstance(src.get("description"), str) and src["description"].strip(),
                 f"{name}: pageSource.description required")
            files = src.get("files")
            _req(isinstance(files, list) and files, f"{name}: pageSource.files must be non-empty")
            for f in files:
                _req(isinstance(f, dict) and isinstance(f.get("path"), str)
                     and isinstance(f.get("lines"), int) and isinstance(f.get("bytes"), int),
                     f"{name}: each pageSource file needs path, lines, bytes")
            _req(src.get("fileCount") == len(files),
                 f"{name}: pageSource.fileCount must equal len(files)")
            _req(src.get("lines") == sum(f["lines"] for f in files),
                 f"{name}: pageSource.lines must equal the sum of file lines")
            _req(isinstance(src.get("bytes"), int) and src["bytes"] > 0,
                 f"{name}: pageSource.bytes must be the archive size")
            _req(isinstance(src.get("license"), str) and src["license"],
                 f"{name}: pageSource.license required")
            _req(isinstance(src.get("commit"), str) and re.fullmatch(r"[0-9a-f]{40}", src["commit"]),
                 f"{name}: pageSource.commit must be 40 lowercase hex")
            _req(isinstance(src.get("sha256"), str) and re.fullmatch(r"[a-f0-9]{64}", src["sha256"]),
                 f"{name}: pageSource.sha256 must be 64 lowercase hex")
        else:
            _req("pageSource" not in s, f"{name}: pageSource is only for generated pages")

    for s in skills:
        aliases = s.get("aliases", [])
        _req(isinstance(aliases, list) and all(valid_name(a) for a in aliases),
             f"{s['name']}: aliases must be a list of skill names")
        for alias in aliases:
            _req(alias not in names, f"{s['name']}: alias {alias!r} is also a live skill name")

    paged = {s["name"] for s in skills if s.get("page") != "none"}
    flows = data.get("workflows", [])
    _req(isinstance(flows, list), "workflows must be a list")
    seen = set()
    numbers = set()
    for f in flows:
        # A workflow is a brew: an id slug ("cold-brew"), its number and name ("Brew 4 · Cold brew").
        _req(isinstance(f, dict) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(f.get("id"))),
             "workflow id must be a lowercase slug such as cold-brew")
        _req(f["id"] not in seen, f"duplicate workflow {f['id']}")
        seen.add(f["id"])
        _req(isinstance(f.get("number"), int) and f["number"] > 0 and f["number"] not in numbers,
             f"{f['id']}: number must be a unique positive integer")
        numbers.add(f["number"])
        _req(isinstance(f.get("name"), str) and f["name"].strip(), f"{f['id']}: name required")
        _req(isinstance(f.get("title"), str) and f["title"].strip(), f"{f['id']}: title required")
        steps = f.get("steps")
        _req(isinstance(steps, list) and steps, f"{f['id']}: steps must be a non-empty list")
        for st in steps:
            names = st.get("skills") if isinstance(st, dict) else None
            _req(isinstance(names, list) and names, f"{f['id']}: each step needs skills")
            for n in names:
                _req(n in paged, f"{f['id']}: step skill {n!r} has no page on the site")
    return data


def parse_frontmatter(text):
    match = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    return _parse_mapping(match.group(1)) if match else {}


def _parse_mapping(block):
    fields = {}
    lines = block.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].rstrip("\r")
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if line.startswith((" ", "\t")):
            i += 1
            continue
        kv = re.match(r"^([A-Za-z0-9_-]+):(?:[ \t]*(.*))?$", line)
        if not kv:
            raise ManifestError(f"unparseable frontmatter line: {line!r}")
        key, rest = kv.group(1), (kv.group(2) or "")
        if rest in (">", ">-", "|", "|-", ">+", "|+"):
            style, chomp = rest[0], rest[1:]
            body = []
            i += 1
            while i < len(lines):
                nxt = lines[i].rstrip("\r")
                if nxt.strip() and not nxt.startswith((" ", "\t")):
                    break
                body.append(nxt)
                i += 1
            fields[key] = _block_scalar(body, style, chomp)
            continue
        value = rest.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key] = value
        i += 1
    return fields


def _block_scalar(body, style, chomp):
    indents = [len(b) - len(b.lstrip(" ")) for b in body if b.strip()]
    indent = min(indents) if indents else 0
    body = [b[indent:] if b.strip() else "" for b in body]
    if style == "|":
        value = "\n".join(body)
    else:
        parts = []
        for b in body:
            if not b:
                parts.append("\n")
            elif parts and not parts[-1].endswith("\n"):
                parts.append(" " + b)
            else:
                parts.append(b)
        value = "".join(parts)
    return value.strip("\n") if chomp == "-" else value.rstrip("\n")


def shape_failures(repo, files, denied=frozenset(), is_fork=False):
    fails = []
    paths = set(files)
    layouts = (f"{repo}/SKILL.md", "SKILL.md", f"skills/{repo}/SKILL.md")
    all_skill_md = [p for p in paths if p == "SKILL.md" or p.endswith("/SKILL.md")]
    sk = next((p for p in layouts if p in paths), None)
    if len(all_skill_md) != 1 or sk is None:
        fails.append("clause 1: expected exactly one SKILL.md at SKILL.md, "
                     "<repo>/SKILL.md or skills/<repo>/SKILL.md")
    if "LICENSE" not in paths:
        fails.append("clause 2: no LICENSE at root")
    if "README.md" not in paths:
        fails.append("clause 3: no README.md at root")

    plugin = files.get(".claude-plugin/plugin.json")
    if plugin is not None:
        try:
            data = json.loads(plugin.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            fails.append("clause 4: .claude-plugin/plugin.json is not JSON")
        else:
            skills = data.get("skills") if isinstance(data, dict) else None
            if skills is not None:
                if isinstance(skills, str):
                    skills = [skills]
                if not isinstance(skills, list) or not all(isinstance(x, str) for x in skills):
                    fails.append("clause 4: plugin.json skills must be a string or list of strings")
                else:
                    for raw in skills:
                        target = raw[2:] if raw.startswith("./") else raw
                        target = target.rstrip("/")
                        if not any(p == target or p.startswith(target + "/") for p in paths):
                            fails.append(f"clause 4: plugin.json path {raw!r} does not resolve")
                        elif sk and not (sk == target or sk.startswith(target + "/")):
                            fails.append(f"clause 4: plugin.json path {raw!r} does not contain the SKILL.md")

    if sk:
        try:
            fm = parse_frontmatter(files[sk].decode("utf-8", errors="replace"))
        except ManifestError as err:
            fails.append(f"clause 5/6: {err}")
            fm = {}
        folder = repo if sk == "SKILL.md" else sk.split("/")[-2]
        name = (fm.get("name") or "").strip()
        if name != folder or name != repo:
            fails.append(f"clause 5: frontmatter name {name!r} must equal folder "
                         f"{folder!r} and repo {repo!r}")
        desc = fm.get("description")
        if not isinstance(desc, str) or not desc.strip():
            fails.append("clause 6: frontmatter description is empty")
        elif "\n" in desc or "\r" in desc:
            fails.append("clause 6: frontmatter description has a line break")
        elif len(desc) > 1024:
            fails.append(f"clause 6: description is {len(desc)} characters (max 1024)")

    if is_fork:
        fails.append("clause 7: repository is a fork")
    if repo in denied or f"arm-pz/{repo}" in denied:
        fails.append("clause 8: repository is denied")
    return fails


def expand_tarball(blob):
    with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as tf:
        members = [m for m in tf.getmembers() if m.isfile()]
        tops = {m.name.split("/")[0] for m in members}
        prefix = ""
        if len(tops) == 1 and all("/" in m.name for m in members):
            prefix = tops.pop() + "/"
        files = {}
        for m in members:
            name = m.name[len(prefix):] if prefix else m.name
            files[name] = tf.extractfile(m).read()
    return files


def select_skill_files(files, path):
    if path == ".":
        selected = {}
        for rel, data in files.items():
            top = rel.split("/")[0]
            if top in REPO_META or top in REPO_META_DIRS:
                continue
            selected[rel] = data
        return selected
    prefix = path + "/"
    return {rel[len(prefix):]: data for rel, data in files.items() if rel.startswith(prefix)}


def pack(files):
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w") as tf:
        for name in sorted(files):
            info = tarfile.TarInfo(name)
            info.size = len(files[name])
            info.mode = 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.mtime = 0
            tf.addfile(info, io.BytesIO(files[name]))
    gz = io.BytesIO()
    with gzip.GzipFile(fileobj=gz, mode="wb", mtime=0, compresslevel=9) as g:
        g.write(raw.getvalue())
    return gz.getvalue()


def redirects(manifest):
    """Cloudflare Pages _redirects lines sending a renamed skill's old URLs to the new ones."""
    lines = []
    for s in sorted(manifest["skills"], key=lambda s: s["name"]):
        for old in s.get("aliases", []):
            if s["page"] != "none":
                lines.append(f"/{old}/ /{s['name']}/ 301")
                lines.append(f"/{old} /{s['name']}/ 301")
            if s.get("kind", "skill") == "skill":
                lines.append(f"/agent-skills/{old}.tar.gz /agent-skills/{s['name']}.tar.gz 301")
    return "".join(line + "\n" for line in lines)


INSTALL = {
    "claude": ["/plugin marketplace add arm-pz/caffeinity-skills",
               "/plugin install caffeinity@caffeinity-skills"],
    "codex": ["codex plugin marketplace add arm-pz/caffeinity-skills"],
    "any": ["npx skills add arm-pz/<skill>"],
}


def llms_txt(manifest):
    """/llms.txt: what the site offers, for agents and AI search, rendered from the manifest."""
    order = {g["id"]: g["order"] for g in manifest["groups"]}
    pages = sorted((s for s in manifest["skills"] if s["page"] != "none"),
                   key=lambda s: (order[s["group"]], s["order"]))
    out = ["# Caffeinity Skills", "",
           "> Open agent skills for Claude Code, Codex, Cursor and any agent that reads a SKILL.md: "
           f"{len(pages)} skills mapped into {len(manifest.get('workflows', []))} workflows "
           "(build a skill, get found, gate a release, grow search traffic, land a job, decide, "
           "learn, run outbound, launch a product). Plain markdown, no API keys.", "",
           "## Install", "",
           "- Claude Code, every skill plus eleven workflow agents: "
           + " then ".join(f"`{c}`" for c in INSTALL["claude"]),
           "- Codex: " + " ".join(f"`{c}`" for c in INSTALL["codex"])
           + ", then install caffeinity from the Plugins directory",
           "- Any agent, one skill: " + " ".join(f"`{c}`" for c in INSTALL["any"]),
           f"- Discovery index: {SITE}/.well-known/agent-skills/index.json", ""]
    for g in sorted(manifest["groups"], key=lambda g: g["order"]):
        rows = [s for s in pages if s["group"] == g["id"]]
        if not rows:
            continue
        out += [f"## {g['title']}", ""]
        for s in rows:
            parts = re.findall(r".+?[.!?](?=\s|$)", " ".join(s["blurb"].split())) or [s["blurb"]]
            lead = parts[0] if len(parts[0]) >= 40 or len(parts) == 1 else f"{parts[0]} {parts[1].strip()}"
            out.append(f"- [{s['name']}]({SITE}/{s['name']}/): {lead.strip()}")
        out.append("")
    flows = manifest.get("workflows", [])
    if flows:
        out += ["## Brews (workflows)", ""]
        for f in flows:
            steps = " -> ".join(" or ".join(st["skills"]) for st in f["steps"])
            out.append(f"- {brew_label(f)}: {f['title']}: {steps}")
        out.append("")
    return "\n".join(out)


def brew_label(flow):
    return f"Brew {flow['number']} · {flow['name']}"


def sha256_hex(blob):
    import hashlib
    return hashlib.sha256(blob).hexdigest()


def title_case(name):
    return " ".join(word.capitalize() for word in name.split("-"))
