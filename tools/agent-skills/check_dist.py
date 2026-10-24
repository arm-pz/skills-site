"""Assert that dist/ is complete, self-consistent and matches out/."""

import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import indexnow
import skilllib
import twins

REF_RE = re.compile(r'(?:href|src)="(/[^"#?]*)"')
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
LD_RE = re.compile(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', re.S)
STATIC = ["404.html", "_headers", "_routes.json"]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(root="."):
    root = Path(root)
    dist = root / "dist"
    manifest = skilllib.load_manifest(root)
    skilllib.validate_manifest(manifest)
    errors = []

    def need(condition, message):
        if not condition:
            errors.append(message)

    for name in STATIC:
        need((dist / name).is_file(), f"missing dist/{name}")
    need((dist / ".well-known/skills.json").is_file(),
         "missing dist/.well-known/skills.json")

    out_index = root / "out" / "index.json"
    dist_index = dist / "agent-skills" / "index.json"
    well_index = dist / ".well-known/agent-skills/index.json"
    for path in (out_index, dist_index, well_index):
        need(path.is_file(), f"missing {path.relative_to(root)}")
    if all(p.is_file() for p in (out_index, dist_index, well_index)):
        out_bytes = out_index.read_bytes()
        need(dist_index.read_bytes() == out_bytes, "dist index differs from out/index.json")
        need(well_index.read_bytes() == out_bytes,
             ".well-known discovery index differs from out/index.json")
        index = json.loads(out_bytes)
        names = [s["name"] for s in skilllib.archived(manifest)]
        indexed = [entry["name"] for entry in index["skills"]]
        need(indexed == sorted(names),
             f"index names {indexed} do not equal the manifest names {sorted(names)}")
        for entry in index["skills"]:
            artifact = dist / "agent-skills" / f"{entry['name']}.tar.gz"
            need(artifact.is_file(), f"missing archive for {entry['name']}")
            if artifact.is_file():
                need("sha256:" + sha256(artifact) == entry["digest"],
                     f"{entry['name']}: archive digest does not match the index")

    pages = [s for s in manifest["skills"] if s["page"] != "none"]
    for skill in pages:
        page = dist / skill["name"] / "index.html"
        need(page.is_file(), f"missing dist/{skill['name']}/index.html")
        if page.is_file():
            title = TITLE_RE.search(page.read_text(encoding="utf-8"))
            need(bool(title and title.group(1).strip()),
                 f"{skill['name']}: page has no <title>")

    # Every page carries its dates and author and has a Markdown twin (twins.py).
    for rel in ["index.html"] + [f"{s['name']}/index.html" for s in pages]:
        page = dist / rel
        if not page.is_file():
            continue
        text = page.read_text(encoding="utf-8")
        twin = Path(rel).with_suffix(".md")
        need((dist / twin).is_file(), f"missing Markdown twin dist/{twin.as_posix()}")
        need(f'<link rel="alternate" type="text/markdown" href="/{twin.as_posix()}">' in text,
             f"{rel}: no alternate link to its Markdown twin")
        need('class="page-stamp"' in text, f"{rel}: no visible author and date line")
        nodes = [twins.dated_node(json.loads(m)) for m in LD_RE.findall(text)]
        need(any(n and {"datePublished", "dateModified", "author"} <= n.keys() for n in nodes),
             f"{rel}: JSON-LD has no dates or author")

    try:
        key = indexnow.key_file(root).name
    except SystemExit as exc:
        errors.append(str(exc))
    else:
        need((dist / key).is_file(), f"missing IndexNow key file dist/{key}")
        routes = dist / "_routes.json"
        need(routes.is_file() and
             json.loads(routes.read_text(encoding="utf-8")) == skilllib.routes(manifest, key),
             "dist/_routes.json is missing or differs from the manifest aliases")

    sitemap_path = dist / "sitemap.xml"
    need(sitemap_path.is_file(), "missing dist/sitemap.xml")
    if sitemap_path.is_file():
        ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        locs = {el.text for el in ET.parse(sitemap_path).getroot().iter(ns + "loc")}
        expected = {f"{skilllib.SITE}/"} | {f"{skilllib.SITE}/{s['name']}/" for s in pages}
        need(locs == expected, f"sitemap URLs differ: missing {expected - locs}, "
                               f"extra {locs - expected}")

    llms = dist / "llms.txt"
    need(llms.is_file() and llms.read_text(encoding="utf-8") == skilllib.llms_txt(manifest),
         "dist/llms.txt is missing or differs from the manifest")

    redirects = dist / "_redirects"
    need(redirects.is_file(), "missing dist/_redirects")
    if redirects.is_file():
        need(redirects.read_text(encoding="utf-8") == skilllib.redirects(manifest),
             "dist/_redirects differs from the manifest aliases")
        for line in redirects.read_text(encoding="utf-8").splitlines():
            target = line.split()[1]
            path = dist / target.lstrip("/")
            need((path / "index.html").is_file() if target.endswith("/") else path.is_file(),
                 f"redirect target {target} does not exist")

    hub_path = dist / "index.html"
    need(hub_path.is_file(), "missing dist/index.html")
    if hub_path.is_file():
        hub = hub_path.read_text(encoding="utf-8")
        cards = hub.count('class="skill"')
        need(cards == len(pages), f"hub has {cards} cards, expected {len(pages)}")
        ld = LD_RE.search(hub)
        need(ld is not None, "hub has no ItemList JSON-LD")
        if ld:
            data = json.loads(ld.group(1))
            need(data.get("numberOfItems") == len(pages),
                 f"JSON-LD numberOfItems is {data.get('numberOfItems')}, "
                 f"expected {len(pages)}")
        for ref in REF_RE.findall(hub):
            target = dist / ref.lstrip("/")
            if ref.endswith("/") or target.is_dir():
                target = target / "index.html"
            need(target.is_file(), f"hub reference {ref} does not resolve")

    for skill in pages:
        page = dist / skill["name"] / "index.html"
        if page.is_file():
            for ref in REF_RE.findall(page.read_text(encoding="utf-8")):
                target = dist / ref.lstrip("/")
                if ref.endswith("/") or target.is_dir():
                    target = target / "index.html"
                need(target.is_file(), f"{skill['name']}: reference {ref} does not resolve")

    return errors


def main(argv=None):
    errors = check((argv or sys.argv[1:] or ["."])[0])
    if errors:
        for error in errors:
            print(f"FAIL {error}", file=sys.stderr)
        return 1
    print("check_dist: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
