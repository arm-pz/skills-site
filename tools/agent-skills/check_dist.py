"""Assert that dist/ is complete, self-consistent and matches out/."""

import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import gen_home
import skilllib

REF_RE = re.compile(r'(?:href|src)="(/[^"#?]*)"')
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
LD_RE = re.compile(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', re.S)
STATIC = ["404.html", "_headers"]


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
    for name in skilllib.STATIC_PAGES:
        need((dist / name / "index.html").is_file(), f"missing dist/{name}/index.html")
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

    sitemap_path = dist / "sitemap.xml"
    need(sitemap_path.is_file(), "missing dist/sitemap.xml")
    if sitemap_path.is_file():
        ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        locs = {el.text for el in ET.parse(sitemap_path).getroot().iter(ns + "loc")}
        expected = ({f"{skilllib.SITE}/"} | {f"{skilllib.SITE}/{s['name']}/" for s in pages}
                    | {f"{skilllib.SITE}/{name}/" for name in skilllib.STATIC_PAGES}
                    | {f"{skilllib.SITE}/workflows/{f['slug']}/" for f in manifest.get("workflows", [])})
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

    for rel, cards in (("skills/index.html", gen_home.skills_only(manifest)),
                       ("mods/index.html", gen_home.mods_only(manifest))):
        path = dist / rel
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            count = text.count('class="skill"')
            need(count == len(cards), f"{rel} has {count} cards, expected {len(cards)}")
            ld = LD_RE.search(text)
            need(ld is not None, f"{rel} has no ItemList JSON-LD")
            if ld:
                data = json.loads(ld.group(1))
                need(data.get("numberOfItems") == len(cards),
                     f"{rel}: JSON-LD numberOfItems is {data.get('numberOfItems')}, "
                     f"expected {len(cards)}")
    for flow in manifest.get("workflows", []):
        need((dist / "workflows" / flow["slug"] / "index.html").is_file(),
             f"missing dist/workflows/{flow['slug']}/index.html")

    need((dist / "index.html").is_file(), "missing dist/index.html")
    for page in sorted(dist.rglob("*.html")):
        for ref in REF_RE.findall(page.read_text(encoding="utf-8")):
            target = dist / ref.lstrip("/")
            if ref.endswith("/") or target.is_dir():
                target = target / "index.html"
            need(target.is_file(), f"{page.relative_to(dist).as_posix()}: reference {ref} does not resolve")

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
