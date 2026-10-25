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

    def test_nested_mapping_is_ignored(self):
        fields = fm("name: demo\ndescription: one line\nmetadata:\n  version: \"1.0.0\"")
        self.assertEqual(fields["name"], "demo")
        self.assertEqual(fields["description"], "one line")


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

    def test_quality_and_tested_shapes(self):
        data = self.manifest()
        data["skills"][0]["quality"] = {"version": None, "commit": "abcdef1",
                                        "updated": "2026-10-24", "notFor": []}
        data["skills"][0]["tested"] = {"date": "2026-10-24", "target": "t", "result": "r",
                                       "evidence": "/#proof"}
        skilllib.validate_manifest(data)
        for key, bad in (("quality", {"commit": "abc"}),
                         ("tested", {"date": "24 Oct", "target": "t", "result": "r", "evidence": "/"}),
                         ("tested", {"date": "2026-10-24", "target": "t", "result": "r",
                                     "evidence": "javascript:alert(1)"})):
            broken = self.manifest()
            broken["skills"][0][key] = bad
            with self.assertRaises(skilllib.ManifestError):
                skilllib.validate_manifest(broken)

    def test_frontmatter_version(self):
        self.assertEqual(skilllib.frontmatter_version("---\nname: a\nversion: 1.0.0\n---\n"), "1.0.0")
        self.assertEqual(skilllib.frontmatter_version(
            '---\nname: a\nmetadata:\n  author: x\n  version: "2.1.0"\n---\n'), "2.1.0")
        self.assertIsNone(skilllib.frontmatter_version("---\nname: a\n---\nversion: 9\n"))
        self.assertIsNone(skilllib.frontmatter_version("no frontmatter"))

    def test_static_page_name_fails(self):
        data = self.manifest()
        data["skills"][0]["name"] = "work"
        with self.assertRaises(skilllib.ManifestError):
            skilllib.validate_manifest(data)

    def test_generated_needs_page_source(self):
        data = self.manifest()
        data["skills"][0]["page"] = "generated"
        with self.assertRaises(skilllib.ManifestError):
            skilllib.validate_manifest(data)

    def test_mod_passes_and_is_not_archived(self):
        data = self.manifest()
        data["skills"].append(dict(data["skills"][0], name="watch", repo="arm-pz/watch",
                                   path=".", kind="mod", order=2))
        skilllib.validate_manifest(data)
        self.assertEqual([s["name"] for s in skilllib.archived(data)], ["demo"])

    def test_mod_inside_another_repo_can_be_generated(self):
        data = self.manifest()
        data["skills"].append(dict(data["skills"][0], name="gate-mod", repo="arm-pz/market",
                                   path="mods/gate-mod", kind="mod", order=2))
        skilllib.validate_manifest(data)
        data["skills"][1]["path"] = "mods/other-mod"
        with self.assertRaises(skilllib.ManifestError):
            skilllib.validate_manifest(data)

    def test_mod_must_have_a_page_and_kind_known(self):
        data = self.manifest()
        data["skills"][0]["kind"] = "mod"
        data["skills"][0]["page"] = "none"
        with self.assertRaises(skilllib.ManifestError):
            skilllib.validate_manifest(data)
        data["skills"][0]["kind"] = "agent"
        with self.assertRaises(skilllib.ManifestError):
            skilllib.validate_manifest(data)

    def test_skill_inside_another_repo(self):
        data = self.manifest()
        data["skills"][0].update(repo="arm-pz/market", path="plugins/demo/skills/demo")
        skilllib.validate_manifest(data)
        data["skills"][0]["path"] = "plugins/demo"
        with self.assertRaises(skilllib.ManifestError):
            skilllib.validate_manifest(data)
        data["skills"][0].update(repo="someone/market", path="plugins/demo/skills/demo")
        with self.assertRaises(skilllib.ManifestError):
            skilllib.validate_manifest(data)

    def test_workflow_needs_a_unique_slug_and_a_summary(self):
        flow = {"id": "pour-over", "number": 1, "name": "Pour-over", "title": "Demo",
                "slug": "demo-flow", "summary": "Does it.", "steps": [{"skills": ["demo"]}]}
        for bad in ({"slug": "Demo Flow"}, {"summary": " "}):
            data = self.manifest()
            data["workflows"] = [dict(flow, **bad)]
            with self.assertRaises(skilllib.ManifestError):
                skilllib.validate_manifest(data)
        data = self.manifest()
        data["workflows"] = [flow, dict(flow, id="bloom", number=2)]
        with self.assertRaises(skilllib.ManifestError):
            skilllib.validate_manifest(data)

    def test_featured_needs_a_tested_run_and_its_own_spot(self):
        data = self.manifest()
        data["skills"][0]["featured"] = 1
        with self.assertRaises(skilllib.ManifestError):
            skilllib.validate_manifest(data)
        data["skills"][0]["tested"] = {"date": "2026-10-24", "target": "t", "result": "r",
                                       "evidence": "/#proof"}
        skilllib.validate_manifest(data)
        data["skills"][0]["featured"] = 4
        with self.assertRaises(skilllib.ManifestError):
            skilllib.validate_manifest(data)

    def test_section_names_are_reserved(self):
        for name in ("skills", "subagents", "harnesses"):
            data = self.manifest()
            data["skills"][0]["name"] = name
            with self.assertRaises(skilllib.ManifestError):
                skilllib.validate_manifest(data)

    def test_workflow_steps_must_have_pages(self):
        data = self.manifest()
        data["workflows"] = [{"id": "pour-over", "number": 1, "name": "Pour-over", "title": "Demo",
                              "slug": "demo-flow", "summary": "Does it.", "steps": [{"skills": ["demo"]}]}]
        skilllib.validate_manifest(data)
        data["workflows"][0]["steps"].append({"skills": ["ghost"]})
        with self.assertRaises(skilllib.ManifestError):
            skilllib.validate_manifest(data)


if __name__ == "__main__":
    unittest.main()
