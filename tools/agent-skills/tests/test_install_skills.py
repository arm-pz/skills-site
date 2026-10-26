import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import install_skills

MANIFEST = {"skills": [
    {"name": "alpha", "repo": "arm-pz/alpha", "path": ".", "page": "bespoke"},
    {"name": "beta", "repo": "arm-pz/market", "path": "plugins/beta/skills/beta", "page": "generated"},
    {"name": "gamma", "repo": "arm-pz/market", "path": "plugins/gamma/skills/gamma", "page": "generated"},
    {"name": "watch-mod", "repo": "arm-pz/market", "path": "mods/watch-mod", "kind": "mod", "page": "generated"},
    {"name": "old", "repo": None, "path": None, "page": "bespoke"},
]}


def fake_clone(repo, dest):
    """A checkout holding a root skill for alpha and two plugin skills for the market repo."""
    dest.mkdir(parents=True)
    (dest / ".git").mkdir()
    if repo == "arm-pz/alpha":
        (dest / "SKILL.md").write_text("---\nname: alpha\n---\n")
        (dest / "notes.md").write_text("n")
    elif repo == "arm-pz/market":
        (dest / "plugins/beta/skills/beta").mkdir(parents=True)
        (dest / "plugins/beta/skills/beta/SKILL.md").write_text("---\nname: beta\n---\n")
    else:
        raise RuntimeError("repository not found")


class InstallSkillsTest(unittest.TestCase):
    def test_plan_selects_named_skills_and_reports_the_rest(self):
        chosen, unknown = install_skills.plan(MANIFEST, ["beta", "watch-mod", "old", "nope"])
        self.assertEqual([e["name"] for e in chosen], ["beta"])
        self.assertEqual(unknown, ["watch-mod", "old", "nope"])

    def test_all_leaves_out_mods_and_legacy(self):
        chosen, unknown = install_skills.plan(MANIFEST, [], everything=True)
        self.assertEqual([e["name"] for e in chosen], ["alpha", "beta", "gamma"])
        self.assertEqual(unknown, [])

    def test_install_copies_each_skill_folder_without_git(self):
        chosen, _ = install_skills.plan(MANIFEST, ["alpha", "beta"])
        with tempfile.TemporaryDirectory() as tmp:
            done, failed = install_skills.install(chosen, tmp, clone=fake_clone)
            self.assertEqual((done, failed), (["alpha", "beta"], {}))
            self.assertTrue((Path(tmp) / "alpha/SKILL.md").is_file())
            self.assertTrue((Path(tmp) / "alpha/notes.md").is_file())
            self.assertFalse((Path(tmp) / "alpha/.git").exists())
            self.assertTrue((Path(tmp) / "beta/SKILL.md").is_file())

    def test_a_failure_is_reported_and_the_rest_still_install(self):
        chosen, _ = install_skills.plan(MANIFEST, ["beta", "gamma"])
        with tempfile.TemporaryDirectory() as tmp:
            done, failed = install_skills.install(chosen, tmp, clone=fake_clone)
            self.assertEqual(done, ["beta"])
            self.assertIn("no SKILL.md", failed["gamma"])

    def test_clone_error_is_a_failure_not_a_crash(self):
        chosen, _ = install_skills.plan({"skills": [dict(MANIFEST["skills"][0], repo="arm-pz/missing")]}, ["alpha"])
        with tempfile.TemporaryDirectory() as tmp:
            done, failed = install_skills.install(chosen, tmp, clone=fake_clone)
            self.assertEqual((done, list(failed)), ([], ["alpha"]))

    def test_reinstall_replaces_the_old_copy(self):
        chosen, _ = install_skills.plan(MANIFEST, ["alpha"])
        with tempfile.TemporaryDirectory() as tmp:
            install_skills.install(chosen, tmp, clone=fake_clone)
            (Path(tmp) / "alpha/stale.md").write_text("old")
            install_skills.install(chosen, tmp, clone=fake_clone)
            self.assertFalse((Path(tmp) / "alpha/stale.md").exists())


if __name__ == "__main__":
    unittest.main()
