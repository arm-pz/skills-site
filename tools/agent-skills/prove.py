"""Post-deploy proof: fetch the live site with a cache-buster and compare it
with the files this run produced."""

import argparse
import html
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import skilllib

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)


def fetch(url, bust):
    separator = "&" if "?" in url else "?"
    request = urllib.request.Request(f"{url}{separator}v={bust}",
                                     headers={"Cache-Control": "no-cache"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True)
    parser.add_argument("--bust", required=True)
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    root = Path(args.root)
    site = args.site.rstrip("/")
    manifest = skilllib.load_manifest(root)
    pages = [s for s in manifest["skills"] if s["page"] != "none"]
    problems = []

    try:
        hub = fetch(f"{site}/", args.bust).decode("utf-8")
        cards = hub.count('class="skill"')
        if cards != len(pages):
            problems.append(f"hub: {cards} cards, expected {len(pages)}")
    except Exception as err:
        problems.append(f"hub: {err}")

    for skill in pages:
        try:
            text = fetch(f"{site}/{skill['name']}/", args.bust).decode("utf-8")
            match = TITLE_RE.search(text)
            title = html.unescape(match.group(1)).strip() if match else ""
            if not title:
                problems.append(f"{skill['name']}: live page has no title")
        except Exception as err:
            problems.append(f"{skill['name']}: {err}")

    try:
        xml = fetch(f"{site}/sitemap.xml", args.bust)
        ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        locs = {el.text for el in ET.fromstring(xml).iter(ns + "loc")}
        expected = {f"{skilllib.SITE}/"} | {f"{skilllib.SITE}/{s['name']}/" for s in pages}
        if locs != expected:
            problems.append(f"sitemap: missing {expected - locs}, extra {locs - expected}")
    except Exception as err:
        problems.append(f"sitemap: {err}")

    local = (root / "out" / "index.json").read_bytes()
    for path in ("/.well-known/agent-skills/index.json", "/agent-skills/index.json"):
        try:
            live = fetch(site + path, args.bust)
            if live != local:
                problems.append(f"{path}: bytes differ from out/index.json")
        except Exception as err:
            problems.append(f"{path}: {err}")

    if problems:
        for problem in problems:
            print(f"FAIL {problem}", file=sys.stderr)
        print("deployed but live verification failed (cache or propagation)",
              file=sys.stderr)
        return 1
    print(f"prove: live site matches this run ({len(pages)} pages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
