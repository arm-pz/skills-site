import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gen_page

SOURCE = {
    "description": "Edits <script>alert(1)</script> & proofs, with 'quotes' and </script>.",
    "files": [{"path": "SKILL.md", "lines": 12, "bytes": 340},
              {"path": "scripts/check.py", "lines": 40, "bytes": 900}],
    "fileCount": 2,
    "lines": 52,
    "bytes": 2048,
    "license": "MIT",
    "commit": "a" * 40,
    "sha256": "b" * 64,
}
ENTRY = {
    "name": "demo", "repo": "arm-pz/demo", "path": "skills/demo",
    "group": "writing-growth", "tag": "editorial", "title": "Demo Skill",
    "blurb": "A demo.", "stats": "2 files",
    "install": "npx skills add arm-pz/demo", "page": "generated", "order": 1,
    "pageSource": SOURCE,
}


class GenPageTest(unittest.TestCase):
    def test_title_default_and_description_escaping(self):
        out = gen_page.render_page(ENTRY)
        self.assertIn("<title>Demo Skill — AI Agent Skill for Claude Code and Codex</title>", out)
        self.assertNotIn("<script>alert(1)</script>", out)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", out)
        self.assertIn("&amp;", out)

    def test_mod_page_says_mod_not_skill(self):
        out = gen_page.render_page(dict(ENTRY, kind="mod", install="/plugin install demo"))
        self.assertIn("<title>Demo Skill — Claude Code mod</title>", out)
        self.assertIn("is an open Claude Code mod", out)
        self.assertIn("read its hooks before you install it", out)
        self.assertNotIn("plain text your agent reads", out)

    def test_jsonld_is_valid_and_escapes_script_close(self):
        out = gen_page.render_page(ENTRY)
        self.assertIn("<\\/script>", out)
        self.assertNotIn("</script>\n</script>", out)
        self.assertIn('"price": "0"', out)

    def test_non_osi_license_omits_offer(self):
        entry = dict(ENTRY, pageSource=dict(SOURCE, license="NOASSERTION"))
        out = gen_page.render_page(entry)
        self.assertNotIn('"offers"', out)
        self.assertIn("see LICENSE", out)

    def test_meta_description_is_155_or_less(self):
        self.assertLessEqual(len(gen_page.meta_description(SOURCE["description"])), 156)

    def test_split_description_parts(self):
        text = ('Use when you need a crawl. Runs a bounded crawl. Trigger phrases include '
                '"crawl the site" and "audit links". Not for rankings; Core Web Vitals.')
        purpose, when, says, nots = gen_page.split_description(text)
        self.assertEqual(purpose, "Runs a bounded crawl.")
        self.assertEqual(when, "you need a crawl")
        self.assertEqual(says, ["crawl the site", "audit links"])
        self.assertEqual(nots, ["rankings", "Core Web Vitals"])
        _, _, _, nots = gen_page.split_description(
            "Does X. Not for writing copy (wordsmith), or finding the ICP.")
        self.assertEqual(nots, ["writing copy (wordsmith)", "finding the ICP"])

    def test_related_lists_group_siblings(self):
        other = dict(ENTRY, name="other", title="Other", blurb="Sibling.", order=2)
        hidden = dict(ENTRY, name="gone", page="none", order=3)
        manifest = {"groups": [{"id": "writing-growth", "title": "Writing & Growth"}],
                    "skills": [ENTRY, other, hidden]}
        out = gen_page.render_page(ENTRY, manifest)
        self.assertIn("More in Writing &amp; Growth", out)
        self.assertIn('href="/other/"', out)
        self.assertNotIn('href="/gone/"', out)

    def test_license_detection(self):
        self.assertEqual(gen_page.detect_license("MIT License\n\nPermission is hereby granted"),
                         "MIT")
        self.assertEqual(gen_page.detect_license("Apache License\nVersion 2.0"), "Apache-2.0")
        self.assertEqual(gen_page.detect_license("something else"), "NOASSERTION")


if __name__ == "__main__":
    unittest.main()
