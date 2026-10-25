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
QUALITY_START = "<!-- gen:quality:start -->"
QUALITY_END = "<!-- gen:quality:end -->"
QUALITY_CSS_START = "<!-- gen:quality-css:start -->"
QUALITY_CSS_END = "<!-- gen:quality-css:end -->"
HEALTH_URL = "https://github.com/arm-pz/skills-site/blob/main/.github/workflows/health.yml"
AGENTS = "Claude Code, Codex, Cursor, Qoder and any agent that loads a SKILL.md"
# Hand-written pages come in a dark and a light palette; the fallbacks cover both.
QUALITY_CSS = """<style>
  .qb{--qb-line:var(--rule,var(--line,color-mix(in srgb,currentColor 14%,transparent)));padding:clamp(48px,6vw,80px) 0;border-top:1px solid var(--qb-line)}
  .qb-kicker{font-family:var(--mono);font-size:12.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--dim,var(--muted))}
  .qb h2{font-family:var(--serif);font-weight:400;font-size:clamp(30px,3.6vw,44px);line-height:1.08;letter-spacing:-.015em;margin-top:10px}
  .qb-lead{color:var(--dim,var(--muted));max-width:62ch;margin-top:12px;font-size:16px}
  .qb a{color:inherit;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:.22em}
  .qb-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:0 36px;margin-top:28px}
  .qb-grid>div{border-top:1px solid var(--qb-line);padding:16px 0 18px}
  .qb dt{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--dim,var(--muted))}
  .qb dd{margin:6px 0 0;font-size:16px;line-height:1.5}
  .qb dd small{display:block;color:var(--dim,var(--muted));font-size:14px;margin-top:2px}
  .qb .qb-wide{grid-column:1/-1}
  .qb ul{margin:6px 0 0;padding-left:20px;display:grid;gap:4px}
  .qb .qb-flag{font-weight:600}
  .qb .qb-flag.fail{color:var(--ember,var(--accent))}
</style>"""
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


def human_date(iso):
    year, month, day = iso.split("-")
    months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    return f"{int(day)} {months[int(month) - 1]} {year}"


def health_html(entry, health):
    if entry.get("kind") == "mod":
        return ("Not covered", "The nightly check reads SKILL.md files, and a mod has none.")
    result = health.get(entry["name"])
    if result is None:
        return ("Not checked yet", "It joins the nightly check after its first run.")
    fails, warns = len(result.get("fail", [])), len(result.get("warn", []))
    if fails:
        return (f'<span class="qb-flag fail">{fails} failing</span>',
                "Fails at least one structural check; the fix is tracked in the health issue.")
    if warns:
        return ("Passing", f"{warns} warning{'s' if warns != 1 else ''}, no failures.")
    return ("Passing", "No failures or warnings.")


def quality_html(entry, health=None):
    """The quality block every skill page carries, generated and hand-written alike."""
    quality = entry.get("quality") or {}
    source = entry.get("pageSource") or {}
    mod = entry.get("kind") == "mod"
    commit = quality.get("commit") or source.get("commit", "")[:7]
    version = quality.get("version")
    repo_url = f"https://github.com/{entry['repo']}"
    if version:
        version_dd = f"{esc(version)}<small>commit {esc(commit)}</small>" if commit else esc(version)
    elif commit:
        version_dd = f"Unversioned<small>commit {esc(commit)}</small>"
    else:
        version_dd = "Not recorded yet"
    updated = quality.get("updated")
    updated_dd = (f'<a href="{esc(repo_url)}/commits" target="_blank" rel="noopener">'
                  f"{esc(human_date(updated))}</a><small>last commit to the repo</small>"
                  if updated else "Not recorded yet")
    agents_dd = ("Claude Code<small>installed as a plugin; it runs hooks with your permissions</small>"
                 if mod else f"{esc(AGENTS)}<small>plain text; no API keys</small>")
    state, note = health_html(entry, health or {})
    check_dd = f'{state}<small>{esc(note)} <a href="{HEALTH_URL}" target="_blank" rel="noopener">How it is checked</a></small>'
    tested = entry.get("tested")
    if tested:
        evidence = tested["evidence"]
        external = ' target="_blank" rel="noopener"' if evidence.startswith("https://") else ""
        tested_dd = (f'{esc(human_date(tested["date"]))}, on {esc(tested["target"])}'
                     f'<small>{esc(tested["result"])} <a href="{esc(evidence)}"{external}>See the run</a></small>')
    else:
        tested_dd = "No public run yet<small>Runs are published only with their evidence.</small>"
    if "notFor" in quality:
        nots = quality["notFor"]
    else:
        nots = split_description(source.get("description", ""))[3]
    if nots:
        limits_dd = "Not built for:<ul>" + "".join(f"<li>{esc(n[:1].upper() + n[1:])}</li>" for n in nots) + "</ul>"
    else:
        limits_dd = "None stated in its description. Read the source before relying on it."
    rows = [("Version", version_dd), ("Updated", updated_dd), ("Works in", agents_dd),
            ("Nightly check", check_dd), ("Last real-world run", tested_dd)]
    cells = "\n".join(f"      <div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in rows)
    return (f'{QUALITY_START}\n<section class="qb" aria-labelledby="qb-h">\n  <div class="wrap">\n'
            f'    <p class="qb-kicker">Quality record</p>\n'
            f'    <h2 id="qb-h">Know what you are installing.</h2>\n'
            f'    <p class="qb-lead">Version, date and limits are read from the repo on every sync, and the '
            f'check runs every night. Real-world runs are listed only with their evidence.</p>\n'
            f'    <dl class="qb-grid">\n{cells}\n'
            f'      <div class="qb-wide"><dt>Known limits</dt><dd>{limits_dd}</dd></div>\n'
            f'    </dl>\n  </div>\n</section>\n{QUALITY_END}')


def quality_css():
    return f"{QUALITY_CSS_START}\n{QUALITY_CSS}\n{QUALITY_CSS_END}"


def replace_region(text, start, end, block, label):
    i, j = text.find(start), text.find(end)
    if i < 0 or j < i:
        raise SystemExit(f"{label}: missing {start} … {end}")
    return text[:i] + block + text[j + len(end):]


def render_bespoke(entry, text, health=None):
    """A hand-written page with only its generated regions rewritten."""
    text = replace_region(text, QUALITY_CSS_START, QUALITY_CSS_END, quality_css(), entry["name"])
    return replace_region(text, QUALITY_START, QUALITY_END, quality_html(entry, health), entry["name"])


def render_page(entry, manifest=None, health=None):
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
    page_title = entry.get("pageTitle") or (f"{entry['title']} — Claude Code mod" if mod else
                                            f"{entry['title']} — AI Agent Skill for Claude Code and Codex")
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
        "QUALITY": quality_html(entry, health),
        "QUALITY_CSS": quality_css(),
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


def bespoke(manifest):
    return [s for s in manifest["skills"] if s["page"] == "bespoke"]


def visible(manifest):
    return [s for s in manifest["skills"] if s["page"] != "none"]


def page_path(root, entry):
    return Path(root) / entry["name"] / "index.html"


def expected_pages(root, manifest):
    """(entry, path, expected text) for every page this script owns all or part of."""
    health = skilllib.load_health(root)
    for entry in generated(manifest):
        yield entry, page_path(root, entry), render_page(entry, manifest, health)
    for entry in bespoke(manifest):
        path = page_path(root, entry)
        if path.is_file():
            yield entry, path, render_bespoke(entry, path.read_text(encoding="utf-8"), health)


def write_pages(root, manifest):
    written = []
    for entry, path, text in list(expected_pages(root, manifest)):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        written.append(str(path.relative_to(root)))
    return written


def check_pages(root, manifest):
    stale = []
    for entry in bespoke(manifest):
        if not page_path(root, entry).is_file():
            stale.append(entry["name"])
            print(f"{entry['name']}: bespoke page is missing")
    for entry, path, expected in expected_pages(root, manifest):
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
        print(f"{len(generated(manifest))} generated pages and the quality blocks "
              f"on {len(bespoke(manifest))} bespoke pages are current")
        return 0
    written = write_pages(root, manifest)
    print(f"pages written: {len(written)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
