import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gen_llms

MANIFEST = {
    "groups": [
        {"id": "ship-checks", "title": "Ship Checks", "descriptor": "pre-launch audits",
         "order": 2},
        {"id": "writing-growth", "title": "Writing & Growth", "descriptor": "editorial",
         "order": 1},
    ],
    "skills": [
        {"name": "alpha", "title": "Alpha", "repo": "arm-pz/alpha", "path": "skills/alpha",
         "group": "writing-growth", "page": "bespoke", "order": 2, "blurb": "Does alpha.",
         "stats": "1 file", "install": "npx skills add arm-pz/alpha"},
        {"name": "hidden", "title": "Hidden", "repo": None, "legacy": {},
         "group": "writing-growth", "page": "none", "order": 3, "path": None},
        {"name": "gamma", "title": "Gamma", "repo": "arm-pz/gamma", "path": ".",
         "group": "ship-checks", "page": "generated", "order": 1, "blurb": "Does gamma.",
         "stats": "2 files", "install": None},
    ],
}


class LlmsTest(unittest.TestCase):
    def test_visible_skills_follow_group_then_skill_order(self):
        names = [skill["name"] for skill in gen_llms.visible(MANIFEST)]
        self.assertEqual(names, ["alpha", "gamma"])

    def test_render_lists_groups_and_skips_unpublished(self):
        text = gen_llms.render(MANIFEST)
        self.assertIn("2 published skills in 2 groups", text)
        self.assertLess(text.index("## Writing & Growth"), text.index("## Ship Checks"))
        self.assertIn("- [Alpha](https://skills.caffeinity.com/alpha/)", text)
        self.assertNotIn("Hidden", text)
        self.assertNotIn("hidden", text)

    def test_source_url_follows_the_manifest_path(self):
        self.assertEqual(
            gen_llms.source_url(MANIFEST["skills"][0]),
            "https://raw.githubusercontent.com/arm-pz/alpha/HEAD/skills/alpha/SKILL.md")
        self.assertEqual(
            gen_llms.source_url(MANIFEST["skills"][2]),
            "https://raw.githubusercontent.com/arm-pz/gamma/HEAD/SKILL.md")
        self.assertIsNone(gen_llms.source_url(MANIFEST["skills"][1]))

    def test_install_falls_back_to_the_repo(self):
        self.assertEqual(gen_llms.install_command(MANIFEST["skills"][2]),
                         "npx skills add arm-pz/gamma")


if __name__ == "__main__":
    unittest.main()
