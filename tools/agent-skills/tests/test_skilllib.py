import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import skilllib


def fm(text):
    return skilllib.parse_frontmatter(f"---\n{text}\n---\n")


def repo_files(root=True, name="demo", plugin=None):
    base = "" if root else f"{name}/"
    files = {
        f"{base}SKILL.md": (
            "---\n"
            f"name: {name}\n"
            "description: A demo skill that does one measurable thing.\n"
            "---\n# Demo\n"
        ).encode(),
        "LICENSE": b"MIT License\n",
        "README.md": b"# demo\n",
    }
    if plugin is not None:
        files[".claude-plugin/plugin.json"] = plugin
    return files


class FrontmatterTest(unittest.TestCase):
    def test_plain_scalar(self):
        self.assertEqual(fm("name: demo\ndescription: one line")["description"], "one line")

    def test_folded_scalar_is_one_line(self):
        fields = fm("description: >-\n  first part\n  second part")
        self.assertEqual(fields["description"], "first part second part")

    def test_literal_single_line_passes(self):
        self.assertEqual(fm("description: |-\n  one line")["description"], "one line")

    def test_literal_multiline_keeps_break(self):
        self.assertIn("\n", fm("description: |\n  line one\n  line two")["description"])

    def test_folded_paragraph_keeps_blank_line(self):
        self.assertIn("\n", fm("description: >-\n  para one\n\n  para two")["description"])


class ShapeTest(unittest.TestCase):
    def test_root_layout_passes(self):
        self.assertEqual(skilllib.shape_failures("demo", repo_files()), [])

    def test_plugin_layout_passes(self):
        files = repo_files(root=False)
        files[".claude-plugin/plugin.json"] = b'{"skills": ["skills/demo"]}'
        files = {("skills/demo/SKILL.md" if k.endswith("SKILL.md") else k): v for k, v in files.items()}
        self.assertEqual(skilllib.shape_failures("demo", files), [])

    def test_two_skill_md_files_fail_clause_one(self):
        files = repo_files()
        files["skills/demo/SKILL.md"] = files["SKILL.md"]
        fails = skilllib.shape_failures("demo", files)
        self.assertTrue(any(f.startswith("clause 1") for f in fails))

    def test_wrong_depth_fails(self):
        files = repo_files()
        files["nested/demo/SKILL.md"] = files.pop("SKILL.md")
        self.assertTrue(any(f.startswith("clause 1") for f in skilllib.shape_failures("demo", files)))

    def test_broken_plugin_key_fails(self):
        files = repo_files()
        files[".claude-plugin/plugin.json"] = b'{"skills": ["skills/missing"]}'
        self.assertTrue(any(f.startswith("clause 4") for f in skilllib.shape_failures("demo", files)))

    def test_absent_plugin_key_passes(self):
        files = repo_files()
        files[".claude-plugin/plugin.json"] = b'{"name": "demo"}'
        self.assertEqual(skilllib.shape_failures("demo", files), [])

    def test_name_mismatch_fails(self):
        files = repo_files()
        files["SKILL.md"] = b"---\nname: other\ndescription: x\n---\n"
        self.assertTrue(any(f.startswith("clause 5") for f in skilllib.shape_failures("demo", files)))

    def test_denied_repo_fails(self):
        fails = skilllib.shape_failures("demo", repo_files(), denied={"arm-pz/demo"})
        self.assertTrue(any(f.startswith("clause 8") for f in fails))


class PackTest(unittest.TestCase):
    def test_pack_is_deterministic_and_has_root_skill(self):
        files = {"SKILL.md": b"---\nname: demo\ndescription: x\n---\n", "a/b.txt": b"x"}
        one, two = skilllib.pack(files), skilllib.pack(dict(reversed(list(files.items()))))
        self.assertEqual(one, two)
        self.assertEqual(skilllib.expand_tarball(one)["SKILL.md"], files["SKILL.md"])


class ManifestTest(unittest.TestCase):
    def manifest(self):
        return {
            "schema": 1,
            "site": skilllib.SITE,
            "groups": [{"id": "writing-growth", "title": "Writing", "descriptor": "editorial", "order": 1}],
            "skills": [{
                "name": "demo", "repo": "arm-pz/demo", "path": "skills/demo",
                "group": "writing-growth", "tag": "editorial", "title": "Demo",
                "blurb": "A demo.", "stats": "1 file · 1 line · 1 KB",
                "install": "npx skills add arm-pz/demo", "page": "bespoke", "order": 1,
            }],
        }

    def test_valid_manifest_passes(self):
        skilllib.validate_manifest(self.manifest())

    def test_duplicate_order_fails(self):
        data = self.manifest()
        data["skills"].append(dict(data["skills"][0], name="other", repo="arm-pz/other"))
        with self.assertRaises(skilllib.ManifestError):
            skilllib.validate_manifest(data)

    def test_generated_needs_page_source(self):
        data = self.manifest()
        data["skills"][0]["page"] = "generated"
        with self.assertRaises(skilllib.ManifestError):
            skilllib.validate_manifest(data)


if __name__ == "__main__":
    unittest.main()
