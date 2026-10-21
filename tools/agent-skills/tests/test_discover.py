import hashlib
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import discover


class AssignmentTest(unittest.TestCase):
    def test_group_table(self):
        cases = {
            "resume-screener": "career",
            "seo-helper": "writing-growth",
            "study-coach": "thinking-learning",
            "deploy-audit": "ship-checks",
            "widget-maker": "skill-authoring",
        }
        for name, group in cases.items():
            self.assertEqual(discover.assign_group(name, ""), group, name)

    def test_tag_follows_group(self):
        self.assertEqual(discover.assign_tag("writing-growth", "seo-x", ""), "seo")
        self.assertEqual(discover.assign_tag("writing-growth", "findable-x", ""), "discovery")
        self.assertEqual(discover.assign_tag("ship-checks", "perf-x", ""), "release")
        self.assertEqual(discover.assign_tag("thinking-learning", "arena-x", ""), "arena")
        self.assertEqual(discover.assign_tag("skill-authoring", "x", ""), "authoring")

    def test_blurb_is_one_sentence_and_capped(self):
        text = "First sentence here. Second sentence."
        self.assertEqual(discover.draft_blurb(text), "First sentence here.")
        self.assertLessEqual(len(discover.draft_blurb("x " * 400)), 241)

    def test_measure_reads_repo_license_and_commit(self):
        files = {
            "SKILL.md": b"---\nname: demo\ndescription: A demo.\n---\n",
            "LICENSE": b"MIT License\n",
            "extra.txt": b"x\n",
        }
        original = discover.gh
        discover.gh = lambda *args, **kwargs: '{"sha": "' + "a" * 40 + '"}'
        try:
            source, blob = discover.measure("demo", files, ".")
        finally:
            discover.gh = original
        self.assertEqual(source["license"], "MIT")
        self.assertEqual(source["fileCount"], 2)
        self.assertEqual(source["commit"], "a" * 40)
        self.assertEqual(source["sha256"], hashlib.sha256(blob).hexdigest())


if __name__ == "__main__":
    unittest.main()
