import io
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import health


def tarball(files):
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for name, data in files.items():
            info = tarfile.TarInfo(f"repo-abc/{name}")
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
    return buf.getvalue()


class StageTest(unittest.TestCase):
    def test_stages_published_skills_and_tune_skill_scripts(self):
        repos = {
            "arm-pz/tune-skill": tarball({"scripts/regress.py": b"#", "SKILL.md": b"x"}),
            "arm-pz/alpha": tarball({"skills/alpha/SKILL.md": b"a", "README.md": b"r"}),
            "arm-pz/market": tarball({"plugins/p/skills/beta/SKILL.md": b"b"}),
        }
        manifest = {"skills": [
            {"name": "alpha", "repo": "arm-pz/alpha", "path": "skills/alpha"},
            {"name": "beta", "repo": "arm-pz/market", "path": "plugins/p/skills/beta"},
            {"name": "watch", "repo": "arm-pz/watch", "path": ".", "kind": "mod"},
            {"name": "old-gate", "repo": None, "path": None},
        ]}
        with tempfile.TemporaryDirectory() as tmp:
            family, tools = Path(tmp) / "family", Path(tmp) / "tools"
            external = health.stage(manifest, family, tools, repos.__getitem__)
            self.assertEqual(sorted(p.name for p in family.iterdir()), ["alpha", "beta"])
            self.assertEqual((family / "beta" / "SKILL.md").read_bytes(), b"b")
            self.assertFalse((family / "alpha" / "README.md").exists())
            self.assertTrue((tools / "scripts" / "regress.py").is_file())
            self.assertIn("old-gate", external)
            self.assertIn("seo-audit", external)


if __name__ == "__main__":
    unittest.main()
