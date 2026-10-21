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


def render_page(entry):
    source = entry["pageSource"]
    name = entry["name"]
    license_id = source["license"]
    osi = license_id in OSI
    repo_url = f"https://github.com/{entry['repo']}"
    commit = source["commit"]
    canonical = f"{skilllib.SITE}/{name}/"
    files = source["files"]
    kb = max(1, round(source["bytes"] / 1024))
    page_title = entry.get("pageTitle") or f"{entry['title']} — agent skill"
    manuscript_rows = "\n".join(
        f'            <li><span class="mono">{esc(f["path"])}</span>'
        f'<span>{f["lines"]:,} lines · {f["bytes"]:,} B</span></li>'
        for f in files)
    table_rows = "\n".join(
        f'        <tr><td class="mono">{esc(f["path"])}</td>'
        f'<td class="n">{f["lines"]:,}</td><td class="n">{f["bytes"]:,} B</td></tr>'
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
        "DESCRIPTION": esc(source["description"]),
        "INSTALL": esc(entry.get("install") or f"npx skills add {entry['repo']}"),
        "REPO_URL": esc(repo_url),
        "REPO_SLUG": esc(entry["repo"]),
        "FILE_COUNT": str(source["fileCount"]),
        "LINES": f'{source["lines"]:,}',
        "KB": str(kb),
        "LICENSE": esc(license_id if osi else "see LICENSE"),
        "LICENSE_META": esc(f"free, open, {license_id}" if osi else "see LICENSE"),
        "LICENSE_CLAUSE": esc(f", {license_id}" if osi else ""),
        "MANUSCRIPT_LABEL": esc(f'what ships · {source["fileCount"]} files, '
                                f'{source["lines"]:,} lines, {kb} KB'),
        "MANUSCRIPT_FILES": manuscript_rows,
        "FILES_TABLE": table_rows,
        "SOURCE_PATH": esc(entry["path"]),
        "COMMIT": esc(commit[:7]),
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
            fh.write(render_page(entry))
        written.append(str(path.relative_to(root)))
    return written


def check_pages(root, manifest):
    stale = []
    for entry in generated(manifest):
        path = page_path(root, entry)
        expected = render_page(entry)
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
