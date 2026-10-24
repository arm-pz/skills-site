import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import repo_metadata


class RepoMetadataTest(unittest.TestCase):
    def test_wanted_covers_skills_mods_and_marketplace(self):
        manifest = {"skills": [
            {"name": "demo", "repo": "arm-pz/demo"},
            {"name": "found", "repo": "arm-pz/found", "githubAbout": "AI agent skill.", "githubTopics": ["skill-md"]},
            {"name": "gate-mod", "repo": "arm-pz/caffeinity-skills", "kind": "mod"},
            {"name": "watch", "repo": "arm-pz/watch", "kind": "mod"},
            {"name": "old", "repo": None},
        ]}
        w = repo_metadata.wanted(manifest)
        self.assertEqual(w["arm-pz/demo"][1], "https://skills.caffeinity.com/demo/")
        self.assertIsNone(w["arm-pz/demo"][2])
        self.assertIn("claude-code-mod", w["arm-pz/watch"][0])
        self.assertEqual(w["arm-pz/caffeinity-skills"][1], "https://skills.caffeinity.com/")
        self.assertNotIn(None, w)
        self.assertEqual(w["arm-pz/found"][2], "AI agent skill.")
        self.assertIn("skill-md", w["arm-pz/found"][0])

    def test_plan_is_additive_and_respects_the_cap(self):
        have, add, home = repo_metadata.plan({"topics": ["agent-skills", "x"], "homepage": ""},
                                             ["agent-skills", "codex"], "https://h/")
        self.assertEqual((add, home), (["codex"], "https://h/"))
        _, add, home = repo_metadata.plan({"topics": [f"t{i}" for i in range(19)], "homepage": "https://mine/"},
                                          ["a", "b"], "https://h/")
        self.assertEqual((add, home), (["a"], None))


if __name__ == "__main__":
    unittest.main()
