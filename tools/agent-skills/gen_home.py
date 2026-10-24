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
FLOWS_START = "    <!-- gen:workflows:start -->"
FLOWS_END = "    <!-- gen:workflows:end -->"
STATS_START = "<!-- gen:stats:start -->"
STATS_END = "<!-- gen:stats:end -->"
WALL_START = "<!-- gen:wall:start -->"
WALL_END = "<!-- gen:wall:end -->"
JSONLD_START = "<!-- gen:jsonld:start -->"
JSONLD_END = "<!-- gen:jsonld:end -->"
HUB_DESCRIPTION = ("Open agent skills for Claude Code, Cursor, Codex and Qoder, mapped into eleven "
                   "workflows: build a skill, get found, ship safely, rank, get hired, decide.")


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
    chips = [esc(skill["tag"])]
    if skill.get("chain"):
        chips.append("chain")
    if skill.get("kind") == "mod":
        chips.append("Claude Code mod")
    chip_html = "".join(f'<span class="chip{" chip-hot" if c != chips[0] else ""}">{c}</span>'
                        for c in chips)
    return [
        f'      <article class="skill" id="{name}" data-search="{search}">',
        f'        <p class="chips">{chip_html}</p>',
        f'        <h3><a href="{name}/">{esc(skill["title"])}</a></h3>',
        f'        <p class="sk-blurb">{esc(skill["blurb"])}</p>',
        f'        <p class="sk-stats">{esc(skill["stats"])}</p>',
        f'        <code class="sk-install">{install}</code>',
        '        <p class="sk-links">',
        f'          <a href="{name}/">Install page</a>',
        f'          <a href="{repo}" target="_blank" rel="noopener">Source</a>',
        '        </p>',
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
        if not cards:
            continue
        lines.append(f'    <section class="sk-group" id="{esc(group["id"])}" '
                     f'aria-labelledby="{esc(group["id"])}-h">')
        lines.append('      <div class="sk-head">')
        lines.append(f'        <h2 id="{esc(group["id"])}-h">{esc(group["title"])}</h2>')
        lines.append(f'        <p>{count_label(cards)} · {esc(group["descriptor"])}</p>')
        lines.append('      </div>')
        lines.append('      <div class="sk-grid">')
        for skill in cards:
            lines.extend("  " + line for line in card(skill))
        lines.append('      </div>')
        lines.append('    </section>')
        lines.append('')
    return "\n".join(lines)


def render_wall(manifest):
    """Two drifting rows of small cards: every skill and mod at a glance, linking to its page.

    Each row holds its cards twice so the CSS loop is seamless; the copy is hidden from
    assistive tech and the tab order.
    """
    cards = visible(manifest)
    rows = [cards[0::2], cards[1::2]]
    lines = ['<div class="wall" aria-label="Every skill and mod">']
    for i, row in enumerate(rows):
        lines.append(f'  <div class="wall-row{" wall-rev" if i else ""}"><div class="wall-track">')
        for copy in (False, True):
            hide = ' aria-hidden="true" tabindex="-1"' if copy else ""
            for s in row:
                lines.append(f'    <a class="wcard" href="{esc(s["name"])}/"{hide}><b>{esc(s["name"])}</b>'
                             f'<code>{esc(s["repo"])}</code></a>')
        lines.append('  </div></div>')
    lines.append('</div>')
    return "\n".join(lines)


def render_workflows(manifest):
    lines = []
    for flow in manifest.get("workflows", []):
        lines.append(f'    <article class="flow" id="{esc(flow["id"].lower())}">')
        lines.append(f'      <p class="flow-id">{esc(flow["id"])}</p>')
        lines.append(f'      <h3>{esc(flow["title"])}</h3>')
        lines.append('      <ol class="flow-steps">')
        for step in flow["steps"]:
            links = " <span class=\"or\">or</span> ".join(
                f'<a href="{esc(n)}/">{esc(n)}</a>' for n in step["skills"])
            opt = ' <span class="opt">optional</span>' if step.get("optional") else ""
            lines.append(f'        <li>{links}{opt}</li>')
        lines.append('      </ol>')
        if flow.get("note"):
            lines.append(f'      <p class="flow-note">{esc(flow["note"])}</p>')
        lines.append('    </article>')
    return "\n".join(lines)


def render_stats(manifest):
    cards = visible(manifest)
    groups = sum(1 for g in manifest["groups"] if any(s["group"] == g["id"] for s in cards))
    flows = len(manifest.get("workflows", []))
    return (f'<p class="stats">{count_label(cards)} · {flows} workflow{"" if flows == 1 else "s"} · '
            f'{groups} {"category" if groups == 1 else "categories"} · 0 API keys</p>')


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
    if FLOWS_START in text:
        flows = render_workflows(manifest).replace("\n", nl)
        text = replace_region(text, FLOWS_START, FLOWS_END, nl + flows + nl)
    if WALL_START in text:
        wall = render_wall(manifest).replace("\n", nl)
        text = replace_region(text, WALL_START, WALL_END, nl + wall + nl)
    if STATS_START in text:
        text = replace_region(text, STATS_START, STATS_END, render_stats(manifest))
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
