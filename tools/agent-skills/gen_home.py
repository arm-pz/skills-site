"""Rewrite only the marked hub regions of index.html from site/skills.json."""

import argparse
import difflib
import html
import json
import sys
from pathlib import Path

import skilllib

SKILLS_START = "    <!-- gen:skills:start -->"
SKILLS_END = "    <!-- gen:skills:end -->"
JSONLD_START = "<!-- gen:jsonld:start -->"
JSONLD_END = "<!-- gen:jsonld:end -->"
HUB_DESCRIPTION = ("Plain-markdown skills for AI coding agents: wordsmith edits, topic-primer "
                   "teaches, keyword-guard ranks, web-preflight ships, findable gets found.")


def esc(value):
    return html.escape(str(value), quote=False)


def visible(manifest):
    ids = {group["id"]: group["order"] for group in manifest["groups"]}
    skills = [s for s in manifest["skills"] if s["page"] != "none"]
    return sorted(skills, key=lambda s: (ids[s["group"]], s["order"]))


def card(skill):
    name = esc(skill["name"])
    repo = html.escape(f"https://github.com/{skill['repo']}", quote=True)
    install = esc(skill.get("install") or f"npx skills add {skill['repo']}")
    search = html.escape(" ".join([skill["name"], skill["title"], skill["tag"],
                                   skill["blurb"]]).lower(), quote=True)
    kind = ' <span class="sk-kind">Claude Code mod</span>' if skill.get("kind") == "mod" else ""
    return [
        f'      <article class="skill" id="{name}" data-search="{search}">',
        f'        <h3><a href="{name}/">{esc(skill["title"])}</a>{kind}</h3>',
        '        <div class="sk-body">',
        f'          <p>{esc(skill["blurb"])}</p>',
        f'          <p class="sk-stats">{esc(skill["stats"])}</p>',
        f'          <code class="sk-install">{install}</code>',
        '          <p class="sk-links">',
        f'            <a href="{name}/">Install page</a>',
        f'            <a href="{repo}" target="_blank" rel="noopener">Source</a>',
        '          </p>',
        '        </div>',
        '      </article>',
    ]


def count_label(cards):
    mods = sum(1 for s in cards if s.get("kind") == "mod")
    skills = len(cards) - mods
    parts = [f"{skills} skill" + ("" if skills == 1 else "s")] if skills else []
    if mods:
        parts.append(f"{mods} mod" + ("" if mods == 1 else "s"))
    return " and ".join(parts)


def render_skills(manifest):
    lines = []
    for group in sorted(manifest["groups"], key=lambda g: g["order"]):
        cards = [s for s in visible(manifest) if s["group"] == group["id"]]
        lines.append(f'    <section class="sk-group" id="{esc(group["id"])}" '
                     f'aria-labelledby="{esc(group["id"])}-h">')
        lines.append('      <div class="sk-head">')
        lines.append(f'        <h2 id="{esc(group["id"])}-h">{esc(group["title"])}</h2>')
        lines.append(f'        <p>{count_label(cards)} · {esc(group["descriptor"])}</p>')
        lines.append('      </div>')
        for skill in cards:
            lines.extend(card(skill))
        lines.append('    </section>')
        lines.append('')
    return "\n".join(lines)


def render_jsonld(manifest):
    items = [
        {"@type": "ListItem", "position": position, "name": skill["name"],
         "url": f"{skilllib.SITE}/{skill['name']}/"}
        for position, skill in enumerate(visible(manifest), 1)
    ]
    data = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Caffeinity Skills",
        "url": f"{skilllib.SITE}/",
        "description": HUB_DESCRIPTION,
        "numberOfItems": len(items),
        "itemListElement": items,
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def replace_region(text, start, end, replacement):
    left = text.index(start) + len(start)
    right = text.index(end, left)
    return text[:left] + replacement + text[right:]


def render(text, manifest):
    nl = "\r\n" if "\r\n" in text else "\n"
    skills_body = render_skills(manifest).replace("\n", nl)
    text = replace_region(text, SKILLS_START, SKILLS_END, nl + skills_body)
    ld = render_jsonld(manifest).replace("\n", nl)
    block = (nl + '<script type="application/ld+json">' + nl + ld + nl
             + "</script>" + nl)
    return replace_region(text, JSONLD_START, JSONLD_END, block)


def main(argv=None):
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    root = Path(args.root)
    manifest = skilllib.load_manifest(root)
    skilllib.validate_manifest(manifest)
    path = root / "index.html"
    with open(path, encoding="utf-8", newline="") as fh:
        original = fh.read()
    updated = render(original, manifest)
    if args.check:
        if updated != original:
            diff = difflib.unified_diff(
                original.splitlines(), updated.splitlines(),
                fromfile="index.html (committed)", tofile="index.html (generated)", lineterm="")
            print("\n".join(list(diff)[:80]))
            print("index.html is stale; run gen_home.py --write", file=sys.stderr)
            return 1
        print("index.html is current")
        return 0
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(updated)
    print(f"index.html rewritten: {len(visible(manifest))} cards")
    return 0


if __name__ == "__main__":
    sys.exit(main())
