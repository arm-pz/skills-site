"""Write out/sitemap.xml from the manifest with per-path git dates."""

import argparse
import subprocess
import sys
from pathlib import Path

import skilllib


def urls(manifest):
    pages = sorted((s for s in manifest["skills"] if s["page"] != "none"),
                   key=lambda s: s["order"])
    result = [(f"{skilllib.SITE}/", "index.html")]
    result.extend((f"{skilllib.SITE}/{s['name']}/", f"{s['name']}/index.html") for s in pages)
    return result


def git_date(root, path, fallback):
    result = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path],
                            cwd=root, capture_output=True, text=True)
    value = result.stdout.strip()
    return value or fallback


def render(manifest, date_for):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, path in urls(manifest):
        lines.append(f"  <url><loc>{url}</loc><lastmod>{date_for(path)}</lastmod></url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", required=True)
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    root = Path(args.root)
    manifest = skilllib.load_manifest(root)
    skilllib.validate_manifest(manifest)
    head = subprocess.run(["git", "log", "-1", "--format=%cs"], cwd=root,
                          capture_output=True, text=True).stdout.strip() or "2026-10-21"
    xml = render(manifest, lambda path: git_date(root, path, head))
    out = root / "out"
    out.mkdir(exist_ok=True)
    with open(out / "sitemap.xml", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(xml)
    print(f"out/sitemap.xml: {len(urls(manifest))} urls")
    with open(out / "llms.txt", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(skilllib.llms_txt(manifest))
    print("out/llms.txt written")
    rules = skilllib.redirects(manifest)
    with open(out / "_redirects", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(rules)
    print(f"out/_redirects: {rules.count(chr(10))} rules")
    return 0


if __name__ == "__main__":
    sys.exit(main())
