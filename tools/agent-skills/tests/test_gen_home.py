import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gen_home

MANIFEST = {
    "schema": 1,
    "site": "https://skills.caffeinity.com",
    "groups": [
        {"id": "writing-growth", "title": "Writing & Growth", "descriptor": "editorial", "order": 1},
        {"id": "ship-checks", "title": "Ship Checks", "descriptor": "audits", "order": 2},
    ],
    "skills": [
        {"name": "alpha", "repo": "arm-pz/alpha", "path": "skills/alpha",
         "group": "writing-growth", "tag": "editorial", "title": "Alpha",
         "blurb": "Edits & proofs.", "stats": "1 file", "install": "npx skills add arm-pz/alpha",
         "page": "bespoke", "order": 1},
        {"name": "beta", "repo": "arm-pz/beta", "path": ".", "group": "ship-checks",
         "tag": "release", "title": "Beta", "blurb": "Ships.", "stats": "2 files",
         "install": "npx skills add arm-pz/beta", "page": "none", "order": 2},
    ],
}

TEXT = """<head>
<!-- gen:jsonld:start -->
old
<!-- gen:jsonld:end -->
</head>
<body>
    <div class="skills">
    <!-- gen:skills:start -->
old
    <!-- gen:skills:end -->
    </div>
</body>
"""


class GenHomeTest(unittest.TestCase):
    def rendered(self):
        return gen_home.render(TEXT, MANIFEST)

    def test_writes_one_card_and_the_group_count(self):
        out = self.rendered()
        self.assertEqual(out.count('class="skill"'), 1)
        self.assertIn(">Writing &amp; Growth</h2>", out)
        self.assertIn("1 skill · editorial", out)

    def test_mod_is_labelled_and_counted(self):
        mod = dict(MANIFEST["skills"][0], name="watch", title="Watch", kind="mod", order=3)
        out = gen_home.render(TEXT, {**MANIFEST, "skills": MANIFEST["skills"] + [mod]})
        self.assertIn("1 skill and 1 mod · editorial", out)
        self.assertIn('<span class="chip chip-hot">Claude Code mod</span>', out)
        self.assertEqual(out.count('class="skill"'), 2)

    def test_jsonld_counts_cards(self):
        self.assertIn('"numberOfItems": 1', self.rendered())

    def test_escaping(self):
        self.assertIn("Edits &amp; proofs.", self.rendered())

    def test_render_is_idempotent(self):
        once = self.rendered()
        self.assertEqual(gen_home.render(once, MANIFEST), once)

    def test_check_detects_a_blurb_change(self):
        changed = {**MANIFEST, "skills": [dict(MANIFEST["skills"][0], blurb="Changed.")]}
        self.assertNotEqual(gen_home.render(TEXT, changed), self.rendered())

    def test_empty_group_is_not_rendered(self):
        self.assertNotIn('id="ship-checks"', self.rendered())

    def test_chain_chip(self):
        chain = dict(MANIFEST["skills"][0], chain=True)
        out = gen_home.render(TEXT, {**MANIFEST, "skills": [chain]})
        self.assertIn('<span class="chip chip-hot">chain</span>', out)

    def test_workflows_and_stats_regions(self):
        text = TEXT.replace("<body>", "<body>\n<!-- gen:stats:start -->x<!-- gen:stats:end -->\n"
                            "    <!-- gen:workflows:start -->\nold\n    <!-- gen:workflows:end -->")
        flows = [{"id": "pour-over", "number": 1, "name": "Pour-over", "title": "Edit", "steps": [{"skills": ["alpha"]},
                  {"skills": ["alpha"], "optional": True}], "note": "One & done."}]
        out = gen_home.render(text, {**MANIFEST, "workflows": flows})
        self.assertIn('<a href="alpha/">alpha</a> <span class="opt">optional</span>', out)
        self.assertIn("One &amp; done.", out)
        self.assertIn("1 skill · 1 brew · 1 category · 0 API keys", out)
        self.assertIn('<p class="flow-id">Brew 1 · Pour-over</p>', out)
        self.assertEqual(gen_home.render(out, {**MANIFEST, "workflows": flows}), out)


if __name__ == "__main__":
    unittest.main()
