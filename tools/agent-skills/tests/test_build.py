import io
import json
import sys
import tarfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build
import skilllib


def tarball(files):
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w:gz") as tf:
        for name, data in files.items():
            info = tarfile.TarInfo(f"arm-pz-demo-deadbeef/{name}")
            info.size = len(data)
            tf.addfile(info, io.BytesIO(data))
    return raw.getvalue()


FILES = {
    "SKILL.md": b"---\nname: demo\ndescription: A demo skill.\n---\n# Demo\n",
    "scripts/run.py": b"print(1)\n",
    ".claude-plugin/plugin.json": b"{}",
}

MANIFEST = {
    "schema": 1,
    "site": skilllib.SITE,
    "groups": [{"id": "skill-authoring", "title": "Authoring", "descriptor": "drafts", "order": 1}],
    "skills": [
        {"name": "demo", "repo": "arm-pz/demo", "path": "skills/demo",
         "group": "skill-authoring", "tag": "authoring", "title": "Demo",
         "blurb": "A demo.", "stats": "2 files", "install": "npx skills add arm-pz/demo",
         "page": "bespoke", "order": 1},
        {"name": "legacy", "repo": None, "path": None, "group": "skill-authoring",
         "tag": "authoring", "title": "Legacy", "page": "none", "order": 2,
         "legacy": {"archive": "legacy.tar.gz", "sha256": "", "description": "Pinned."}},
    ],
}


def build_fixture(tmp):
    files = {f"skills/demo/{k}": v for k, v in FILES.items()}
    files["README.md"] = b"# demo\n"
    blob = tarball(files)
    legacy_files = skilllib.pack({"SKILL.md": FILES["SKILL.md"]})
    legacy_dir = Path(tmp) / "legacy"
    legacy_dir.mkdir()
    (legacy_dir / "legacy.tar.gz").write_bytes(legacy_files)
    manifest = json.loads(json.dumps(MANIFEST))
    manifest["skills"][1]["legacy"]["sha256"] = skilllib.sha256_hex(legacy_files)
    return manifest, legacy_dir


class BuildTest(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmp = tempfile.TemporaryDirectory()
        self.manifest, self.legacy = build_fixture(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_build(self, about=lambda repo: "A demo skill.", blob=None):
        root = Path(self.tmp.name)
        return build.build(
            self.manifest, root / "out",
            tarball_fetch=lambda repo: blob or tarball(
                {f"skills/demo/{k}": v for k, v in FILES.items()} | {"README.md": b"# demo\n"}),
            about_fetch=about, legacy_dir=self.legacy)

    def test_entries_sorted_and_index_written(self):
        entries = self.run_build()
        self.assertEqual([e["name"] for e in entries], ["demo", "legacy"])
        index = json.loads((Path(self.tmp.name) / "out" / "index.json").read_text())
        self.assertEqual(len(index["skills"]), 2)
        self.assertEqual(index["skills"][1]["description"], "Pinned.")

    def test_empty_about_fails(self):
        with self.assertRaises(SystemExit):
            self.run_build(about=lambda repo: "")

    def test_legacy_digest_mismatch_fails(self):
        self.manifest["skills"][1]["legacy"]["sha256"] = "0" * 64
        with self.assertRaises(SystemExit):
            self.run_build()

    def test_same_inputs_produce_identical_bytes(self):
        self.run_build()
        first = (Path(self.tmp.name) / "out" / "demo.tar.gz").read_bytes()
        self.run_build()
        self.assertEqual(first, (Path(self.tmp.name) / "out" / "demo.tar.gz").read_bytes())


if __name__ == "__main__":
    unittest.main()
