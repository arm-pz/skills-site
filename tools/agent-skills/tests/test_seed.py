import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import seed_manifest
import skilllib

ROOT = Path(__file__).resolve().parents[3]


class SeedTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest, cls.deny = seed_manifest.build_seed(ROOT)

    def test_counts_match_the_live_site(self):
        skills = self.manifest["skills"]
        self.assertEqual(len(skills), 25)
        self.assertEqual(sum(s["page"] == "bespoke" for s in skills), 22)
        self.assertEqual(sum(s["page"] == "none" for s in skills), 3)
        self.assertEqual(len(self.manifest["groups"]), 5)

    def test_group_card_counts(self):
        counts = {}
        for s in self.manifest["skills"]:
            if s["page"] != "none":
                counts[s["group"]] = counts.get(s["group"], 0) + 1
        self.assertEqual(counts, {"writing-growth": 6, "career": 3,
                                  "thinking-learning": 3, "skill-authoring": 7,
                                  "ship-checks": 3})

    def test_paths_include_the_four_omitted_root_repos(self):
        paths = {s["name"]: s["path"] for s in self.manifest["skills"] if s["repo"]}
        self.assertEqual(paths["tune-skill"], ".")
        self.assertEqual(paths["draft-skill"], ".")
        self.assertEqual(paths["wordsmith"], "skills/wordsmith")
        self.assertEqual(paths["keyword-guard"], ".")

    def test_legacy_entries_are_pinned(self):
        by_name = {s["name"]: s for s in self.manifest["skills"]}
        for name in ("release-gate", "publish-release-gate"):
            entry = by_name[name]
            self.assertIsNone(entry["repo"])
            self.assertEqual(len(entry["legacy"]["sha256"]), 64)
            self.assertTrue((ROOT / "site" / "legacy" / entry["legacy"]["archive"]).is_file())

    def test_manifest_validates(self):
        skilllib.validate_manifest(self.manifest)

    def test_deny_lists_only_the_third_party_skill(self):
        self.assertEqual([d["repo"] for d in self.deny], ["arm-pz/job-application-agent"])


if __name__ == "__main__":
    unittest.main()
