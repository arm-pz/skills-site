"""Write out/llms.txt, a plain-text catalog for agents, from the manifest."""

import argparse
import sys
from pathlib import Path

import skilllib

INTRO = ("Open, plain-markdown agent skills for Claude Code, Cursor, Qoder and other "
         "coding agents.")
SUMMARY = ("Verification-first agent skills for shipping, auditing and writing: pre-launch "
           "security and performance checks, SEO, editorial work, careers, skill authoring "
           "and outbound.")


def visible(manifest):
    group_order = {group["id"]: group["order"] for group in manifest["groups"]}
    skills = [s for s in manifest["skills"] if s["page"] != "none"]
    return sorted(skills, key=lambda s: (group_order[s["group"]], s["order"]))


def one_line(value):
    return " ".join(str(value).split())


def install_command(skill):
    return skill.get("install") or f"npx skills add {skill['repo']}"


def source_url(skill):
    repo = skill.get("repo")
    if not repo:
        return None
    path = (skill.get("path") or ".").strip("/")
    prefix = "" if path in ("", ".") else f"{path}/"
    return f"https://raw.githubusercontent.com/{repo}/HEAD/{prefix}SKILL.md"


def render(manifest):
    groups = sorted(manifest["groups"], key=lambda group: group["order"])
    skills = visible(manifest)
    lines = [
        "# Caffeinity Skills",
        "",
        f"> {SUMMARY}",
        "",
        f"{INTRO} {len(skills)} published skills in {len(groups)} groups.",
        "",
        f"- Site: {skilllib.SITE}/",
        "- Marketplace: `/plugin marketplace add arm-pz/caffeinity-skills`",
        "- One skill: `npx skills add arm-pz/<name>`",
        f"- Machine index: {skilllib.SITE}/.well-known/agent-skills/index.json",
        f"- Sitemap: {skilllib.SITE}/sitemap.xml",
    ]
    for group in groups:
        members = [skill for skill in skills if skill["group"] == group["id"]]
        if not members:
            continue
        lines.extend(["", f"## {one_line(group['title'])}", ""])
        for skill in members:
            line = (f"- [{one_line(skill['title'])}]({skilllib.SITE}/{skill['name']}/): "
                    f"{one_line(skill['blurb'])} Install: `{one_line(install_command(skill))}`.")
            source = source_url(skill)
            if source:
                line += f" SKILL.md: {source}"
            lines.append(line)
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", required=True)
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    root = Path(args.root)
    manifest = skilllib.load_manifest(root)
    skilllib.validate_manifest(manifest)
    text = render(manifest)
    out = root / "out"
    out.mkdir(exist_ok=True)
    with open(out / "llms.txt", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print(f"out/llms.txt: {len(visible(manifest))} skills, {len(text.splitlines())} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
