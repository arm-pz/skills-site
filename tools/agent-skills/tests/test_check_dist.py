import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_dist
import skilllib


def entry(name, digest):
    return {"name": name, "description": "x", "type": "archive",
            "url": f"https://skills.caffeinity.com/agent-skills/{name}.tar.gz",
            "digest": f"sha256:{digest}"}


class CheckDistTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "site").mkdir()
        (self.root / "out").mkdir()
        (self.root / "dist/agent-skills").mkdir(parents=True)
        (self.root / "dist/.well-known/agent-skills").mkdir(parents=True)
        blobs = {n: skilllib.pack({"SKILL.md": f"---\nname: {n}\ndescription: x\n---\n".encode()})
                 for n in ("alpha", "beta")}
        for name, blob in blobs.items():
            (self.root / "out" / f"{name}.tar.gz").write_bytes(blob)
            shutil.copyfile(self.root / "out" / f"{name}.tar.gz",
                            self.root / "dist/agent-skills" / f"{name}.tar.gz")
        index = {"$schema": skilllib.INDEX_SCHEMA,
                 "skills": [entry(n, skilllib.sha256_hex(b)) for n, b in blobs.items()]}
        text = json.dumps(index)
        (self.root / "out/index.json").write_text(text)
        (self.root / "dist/agent-skills/index.json").write_text(text)
        (self.root / "dist/.well-known/agent-skills/index.json").write_text(text)
        manifest = {
            "schema": 1, "site": skilllib.SITE,
            "groups": [{"id": "writing-growth", "title": "Writing", "descriptor": "x", "order": 1}],
            "skills": [
                {"name": "alpha", "repo": "arm-pz/alpha", "path": ".", "group": "writing-growth",
                 "tag": "editorial", "title": "Alpha", "blurb": "A.", "stats": "1",
                 "install": "npx skills add arm-pz/alpha", "page": "bespoke", "order": 1},
                {"name": "beta", "repo": "arm-pz/beta", "path": ".", "group": "writing-growth",
                 "tag": "editorial", "title": "Beta", "blurb": "B.", "stats": "1",
                 "install": "npx skills add arm-pz/beta", "page": "bespoke", "order": 2},
            ],
        }
        (self.root / "site/skills.json").write_text(json.dumps(manifest))
        (self.root / "out/sitemap.xml").write_text(
            '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            '<url><loc>https://skills.caffeinity.com/</loc></url>'
            '<url><loc>https://skills.caffeinity.com/alpha/</loc></url>'
            '<url><loc>https://skills.caffeinity.com/beta/</loc></url>'
            "</urlset>")
        shutil.copyfile(self.root / "out/sitemap.xml", self.root / "dist/sitemap.xml")
        llms = ("# Skills\n\n"
                "- [Alpha](https://skills.caffeinity.com/alpha/)\n"
                "- [Beta](https://skills.caffeinity.com/beta/)\n")
        (self.root / "out/llms.txt").write_text(llms)
        shutil.copyfile(self.root / "out/llms.txt", self.root / "dist/llms.txt")
        for name in ("alpha", "beta"):
            (self.root / "dist" / name).mkdir()
            (self.root / "dist" / name / "index.html").write_text(
                f"<title>{name}</title>")
        (self.root / "dist/index.html").write_text(
            '<a href="/alpha/">a</a><a href="/beta/">b</a>'
            '<div class="skill"></div><div class="skill"></div>'
            '<script type="application/ld+json">{"numberOfItems": 2}</script>')
        for name in ("404.html", "_headers"):
            (self.root / "dist" / name).write_text("x")
        (self.root / "dist/.well-known/skills.json").write_text("{}")
        (self.root / "dist/fonts").mkdir()
        (self.root / "dist/fonts/fonts.css").write_text("x")

    def tearDown(self):
        self.tmp.cleanup()

    def test_valid_tree_passes(self):
        self.assertEqual(check_dist.check(self.root), [])

    def test_missing_404_fails(self):
        (self.root / "dist/404.html").unlink()
        self.assertTrue(check_dist.check(self.root))

    def test_digest_mismatch_fails(self):
        (self.root / "dist/agent-skills/alpha.tar.gz").write_bytes(b"changed")
        self.assertTrue(check_dist.check(self.root))

    def test_missing_page_fails(self):
        shutil.rmtree(self.root / "dist/beta")
        self.assertTrue(check_dist.check(self.root))

    def test_missing_llms_fails(self):
        (self.root / "dist/llms.txt").unlink()
        self.assertTrue(check_dist.check(self.root))

    def test_stale_jsonld_count_fails(self):
        html = (self.root / "dist/index.html").read_text().replace(
            '"numberOfItems": 2', '"numberOfItems": 1')
        (self.root / "dist/index.html").write_text(html)
        self.assertTrue(check_dist.check(self.root))


if __name__ == "__main__":
    unittest.main()
