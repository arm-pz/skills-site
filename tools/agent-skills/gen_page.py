"""Render generated skill pages from site/skills.json and the shared template."""

import argparse
import difflib
import html
import json
import re
import sys
from pathlib import Path

import skilllib

TEMPLATE = Path(__file__).resolve().parent / "templates" / "skill-page.html"
OSI = {"MIT", "Apache-2.0", "AGPL-3.0", "GPL-3.0", "MPL-2.0",
       "BSD-3-Clause", "BSD-2-Clause", "ISC", "Unlicense"}


def esc(value):
    return html.escape(str(value), quote=True)


def meta_description(text, limit=155):
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    cut = text[:limit]
    cut = cut[:cut.rfind(" ")].rstrip(" ,;:-")
    return cut + "…"


def detect_license(text):
    upper = text.upper()
    if "MIT LICENSE" in upper or "PERMISSION IS HEREBY GRANTED, FREE OF CHARGE" in upper:
        return "MIT"
    if "APACHE LICENSE" in upper and "VERSION 2.0" in upper:
        return "Apache-2.0"
    if "GNU AFFERO GENERAL PUBLIC LICENSE" in upper:
        return "AGPL-3.0"
    if "GNU GENERAL PUBLIC LICENSE" in upper and "VERSION 3" in upper:
        return "GPL-3.0"
    if "MOZILLA PUBLIC LICENSE" in upper and "2.0" in upper:
        return "MPL-2.0"
    if "BSD 3-CLAUSE" in upper:
        return "BSD-3-Clause"
    if "BSD 2-CLAUSE" in upper:
        return "BSD-2-Clause"
    if "ISC LICENSE" in upper:
        return "ISC"
    if "UNLICENSE" in upper:
        return "Unlicense"
    return "NOASSERTION"


def split_description(text):
    """Split a SKILL.md description into purpose, when, trigger phrases and not-for.

    Descriptions follow the house pattern loosely, so each part is optional and
    anything unrecognised stays in the purpose.
    """
    purpose, when, says, nots = [], "", [], []
    for sentence in re.split(r"(?<=\.)\s+(?=[A-Z])", " ".join(text.split())):
        if sentence.startswith("Use when "):
            when = sentence[len("Use when "):].rstrip(".")
        elif sentence.startswith("Trigger phrases include"):
            says = re.findall(r'"([^"]+)"', sentence)
        elif sentence.startswith("Not for "):
            body = sentence[len("Not for "):].rstrip(".")
            parts = body.split(";") if ";" in body else re.split(r"(?<=\)),\s+", body)
            nots = [re.sub(r"^(or|and)\s+", "", p.strip()) for p in parts if p.strip()]
        else:
            purpose.append(sentence)
    return " ".join(purpose), when, says, nots


def uses_html(when, says, nots):
    def block(cls, title, inner):
        return (f'    <div class="uses-col {cls}">\n      <h3>{title}</h3>\n'
                f'{inner}\n    </div>')

    def items(values):
        rows = "".join(f"<li>{esc(v[:1].upper() + v[1:])}</li>" for v in values)
        return f"      <ul>{rows}</ul>"

    cols = []
    if when:
        cols.append(block("when", "Reach for it when",
                          f'      <ul><li>{esc(when[:1].upper() + when[1:])}.</li></ul>'))
    if says:
        cols.append(block("say", "Say it like this", items(says)))
    if nots:
        cols.append(block("not", "Not for", items(nots)))
    if not cols:
        return ""
    return '    <div class="uses">\n' + "\n".join(cols) + "\n    </div>"


def related_html(entry, manifest):
    if not manifest:
        return ""
    siblings = sorted((s for s in manifest["skills"]
                       if s["group"] == entry["group"] and s["page"] != "none"
                       and s["name"] != entry["name"]),
                      key=lambda s: s["order"])[:3]
    if not siblings:
        return ""
    group = next(g["title"] for g in manifest["groups"] if g["id"] == entry["group"])
    rows = "\n".join(
        f'      <li><a href="/{esc(s["name"])}/"><strong>{esc(s["title"])}</strong>'
        f'<span>{esc(s["blurb"])}</span></a></li>' for s in siblings)
    return (f'    <h2 id="more-h">More in {esc(group)}</h2>\n'
            f'    <ul class="related">\n{rows}\n    </ul>')


def render_page(entry, manifest=None):
    source = entry["pageSource"]
    name = entry["name"]
    license_id = source["license"]
    osi = license_id in OSI
    repo_url = f"https://github.com/{entry['repo']}"
    commit = source["commit"]
    canonical = f"{skilllib.SITE}/{name}/"
    files = source["files"]
    kb = max(1, round(source["bytes"] / 1024))
    mod = entry.get("kind") == "mod"
    noun = "Claude Code mod" if mod else "agent skill"
    page_title = entry.get("pageTitle") or f"{entry['title']} — {noun}"
    purpose, when, says, nots = split_description(source["description"])
    related = related_html(entry, manifest)
    if not related:
        related = '    <h2 id="more-h" class="sr-only">Source</h2>'
    table_rows = "\n".join(
        f'        <tr><td>{esc(f["path"])}</td>'
        f'<td class="n">{f["lines"]:,}</td><td class="n bytes">{f["bytes"]:,} B</td></tr>'
        for f in files)
    ld = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": name,
        "alternateName": entry["title"],
        "applicationCategory": "DeveloperApplication",
        "operatingSystem": "Any",
        "url": canonical,
        "description": source["description"],
        "codeRepository": repo_url,
        "license": (f"https://spdx.org/licenses/{license_id}.html" if osi
                    else f"{repo_url}/blob/{commit}/LICENSE"),
        "publisher": {"@type": "Organization", "name": "Caffeinity",
                      "url": "https://caffeinity.com/"},
    }
    if osi:
        ld["offers"] = {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    json_ld = json.dumps(ld, indent=2, ensure_ascii=False).replace("</", "<\\/")
    tokens = {
        "PAGE_TITLE": esc(page_title),
        "META_DESCRIPTION": esc(meta_description(source["description"])),
        "OG_DESCRIPTION": esc(source["description"]),
        "CANONICAL": esc(canonical),
        "JSON_LD": json_ld,
        "NAME": esc(name),
        "TITLE": esc(entry["title"]),
        "BLURB": esc(entry.get("blurb") or meta_description(source["description"])),
        "PURPOSE": esc(purpose or source["description"]),
        "USES": uses_html(when, says, nots),
        "RELATED": related,
        "INSTALL": esc(entry.get("install") or f"npx skills add {entry['repo']}"),
        "REPO_URL": esc(repo_url),
        "REPO_SLUG": esc(entry["repo"]),
        "FILE_COUNT": str(source["fileCount"]),
        "LINES": f'{source["lines"]:,}',
        "KB": str(kb),
        "LICENSE_FACT": esc(f"free under {license_id}" if osi else "see LICENSE for terms"),
        "FILES_TABLE": table_rows,
        "SOURCE_PATH": esc(entry["path"]),
        "COMMIT": esc(commit[:7]),
        "NOUN": noun,
        "NOUN_SHORT": "mod" if mod else "skill",
        "FILES_INTRO": ("A mod is code that runs inside Claude Code with your permissions, so read "
                        "its hooks before you install it." if mod else
                        "A skill is plain text your agent reads, so this list is all of it."),
    }
    template = TEMPLATE.read_text(encoding="utf-8")
    for key, value in tokens.items():
        template = template.replace("{{" + key + "}}", value)
    leftover = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", template)))
    if leftover:
        raise SystemExit(f"template tokens left unreplaced: {leftover}")
    return template

def generated(manifest):
    return [s for s in manifest["skills"] if s["page"] == "generated"]


def visible(manifest):
    return [s for s in manifest["skills"] if s["page"] != "none"]


def page_path(root, entry):
    return Path(root) / entry["name"] / "index.html"


def write_pages(root, manifest):
    written = []
    for entry in generated(manifest):
        path = page_path(root, entry)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(render_page(entry, manifest))
        written.append(str(path.relative_to(root)))
    return written


def check_pages(root, manifest):
    stale = []
    for entry in generated(manifest):
        path = page_path(root, entry)
        expected = render_page(entry, manifest)
        actual = path.read_text(encoding="utf-8") if path.exists() else None
        if actual != expected:
            stale.append(entry["name"])
            if actual is not None:
                diff = difflib.unified_diff(
                    actual.splitlines(), expected.splitlines(),
                    fromfile=f"{entry['name']} (committed)",
                    tofile=f"{entry['name']} (generated)", lineterm="")
                print("\n".join(list(diff)[:40]))
    return stale


def main(argv=None):
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--list", action="store_true")
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    root = Path(args.root)
    manifest = skilllib.load_manifest(root)
    skilllib.validate_manifest(manifest)
    if args.list:
        for entry in visible(manifest):
            print(entry["name"])
        return 0
    if args.check:
        stale = check_pages(root, manifest)
        if stale:
            print(f"generated pages are stale: {', '.join(stale)}", file=sys.stderr)
            return 1
        print(f"{len(generated(manifest))} generated pages are current")
        return 0
    written = write_pages(root, manifest)
    print(f"generated pages written: {len(written)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
