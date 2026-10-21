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
        self.assertIn("<h2>Writing &amp; Growth</h2>", out)
        self.assertIn("1 skills · editorial", out)

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


if __name__ == "__main__":
    unittest.main()
