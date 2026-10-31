import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import discover
import skilllib
import sync

LICENSE = b"MIT License\nPermission is hereby granted, free of charge\n"


def skill_files(name, desc="Does a thing. Use when asked.", folder=""):
    prefix = f"{folder}/" if folder else ""
    return {f"{prefix}SKILL.md": f"---\nname: {name}\ndescription: {desc}\n---\n# {name}\n".encode(),
            "LICENSE": LICENSE, "README.md": b"# r\n"}


def entry(name, page="bespoke", order=1, **extra):
    e = {"name": name, "repo": f"arm-pz/{name}", "path": ".", "group": "writing-growth",
         "tag": "editorial", "title": name.title(), "blurb": "Hand-written.", "stats": "1",
         "install": f"npx skills add arm-pz/{name}", "page": page, "order": order}
    e.update(extra)
    return e


class FakeGitHub:
    """Stands in for gh: public repos, renames, HEAD shas and tarballs."""

    def __init__(self, repos, files, renamed=None, heads=None):
        self.repos, self.files = repos, files
        self.renamed, self.heads = renamed or {}, heads or {}

    def gh_json(self, *args):
        if args[:2] == ("repo", "list"):
            return [{"name": n, "isFork": False, "visibility": "PUBLIC", "isArchived": False,
                     "description": d} for n, d in self.repos.items()], None
        path = args[1]
        repo = path.split("/")[2]
        if path.endswith("/commits/HEAD"):
            return {"sha": self.heads.get(repo, "a" * 40),
                    "commit": {"committer": {"date": "2026-10-24T09:00:00Z"}}}, None
        if "/git/trees/" in path:
            return {"tree": [{"path": p} for p in self.files.get(repo, {})]}, None
        if repo in self.repos:
            return {"full_name": f"arm-pz/{repo}", "private": False}, None
        if repo in self.renamed:
            new = self.renamed[repo]
            return {"full_name": new if "/" in new else f"arm-pz/{new}", "private": False}, None
        return None, "gh: Not Found (HTTP 404)"

    def install(self, test):
        originals = (sync.gh_json, discover.fetch_files, discover.gh)
        sync.gh_json = self.gh_json
        discover.fetch_files = lambda name: self.files[name]
        discover.gh = lambda *a, **k: json.dumps({"sha": self.heads.get(a[1].split("/")[2], "a" * 40)})
        test.addCleanup(lambda: setattr(sync, "gh_json", originals[0]))
        test.addCleanup(lambda: setattr(discover, "fetch_files", originals[1]))
        test.addCleanup(lambda: setattr(discover, "gh", originals[2]))


class SyncTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.manifest = {
            "schema": 1, "site": skilllib.SITE,
            "groups": [{"id": g, "title": g, "descriptor": "x", "order": i}
                       for i, g in enumerate(skilllib.GROUP_IDS, 1)],
            "skills": [entry("keeper", quality={"version": None, "commit": "aaaaaaa",
                                                "updated": "2026-10-24", "notFor": []})],
            "workflows": [{"id": "pour-over", "number": 1, "name": "Pour-over", "title": "Flow",
                           "slug": "flow", "summary": "Does it.", "steps": [{"skills": ["keeper"]}]}],
        }

    def run_sync(self, gh, deny=()):
        gh.install(self)
        actions = sync.plan(self.root, self.manifest, list(deny))
        notes = sync.apply(self.root, self.manifest, actions)
        return {(k, n) for k, n, _ in actions}, notes

    def names(self):
        return [s["name"] for s in self.manifest["skills"]]

    def test_in_sync_does_nothing(self):
        before = copy.deepcopy(self.manifest)
        actions, _ = self.run_sync(FakeGitHub({"keeper": "About."}, {"keeper": skill_files("keeper")}))
        self.assertEqual(actions, set())
        self.assertEqual(self.manifest, before)

    def test_new_skill_repo_is_added_with_a_generated_page(self):
        gh = FakeGitHub({"keeper": "About.", "fresh-seo": "About.", "notes-app": "About."},
                        {"keeper": skill_files("keeper"), "fresh-seo": skill_files("fresh-seo"),
                         "notes-app": {"README.md": b"x"}})
        actions, _ = self.run_sync(gh)
        self.assertEqual(actions, {("add", "fresh-seo")})
        added = self.manifest["skills"][-1]
        self.assertEqual((added["name"], added["page"], added["group"]), ("fresh-seo", "generated", "seo-search"))

    def test_empty_about_and_bad_shape_are_held_not_published(self):
        gh = FakeGitHub({"keeper": "About.", "no-about": "", "two-skills": "About."},
                        {"keeper": skill_files("keeper"), "no-about": skill_files("no-about"),
                         "two-skills": {**skill_files("a", folder="a"), **skill_files("b", folder="b")}})
        actions, notes = self.run_sync(gh)
        self.assertEqual(actions, {("hold", "no-about"), ("hold", "two-skills")})
        self.assertEqual(self.names(), ["keeper"])
        self.assertTrue(any("About is empty" in n for n in notes))

    def test_denied_repo_never_publishes(self):
        gh = FakeGitHub({"keeper": "About.", "bad-agent": "About."},
                        {"keeper": skill_files("keeper"), "bad-agent": skill_files("bad-agent")})
        actions, _ = self.run_sync(gh, deny=[{"repo": "arm-pz/bad-agent", "reason": "x"}])
        self.assertEqual(actions, set())

    def test_renamed_repo_moves_page_keeps_copy_and_redirects(self):
        (self.root / "keeper").mkdir()
        (self.root / "keeper/index.html").write_text("<title>keeper</title>")
        gh = FakeGitHub({"new-keeper": "About."}, {"new-keeper": skill_files("new-keeper")},
                        renamed={"keeper": "new-keeper"})
        actions, notes = self.run_sync(gh)
        self.assertEqual(actions, {("rename", "keeper")})
        e = self.manifest["skills"][0]
        self.assertEqual((e["name"], e["repo"], e["aliases"], e["blurb"]),
                         ("new-keeper", "arm-pz/new-keeper", ["keeper"], "Hand-written."))
        self.assertEqual(e["install"], "npx skills add arm-pz/new-keeper")
        self.assertTrue((self.root / "new-keeper/index.html").is_file())
        self.assertEqual(self.manifest["workflows"][0]["steps"][0]["skills"], ["new-keeper"])
        self.assertIn("/keeper/ /new-keeper/ 301", skilllib.redirects(self.manifest))
        self.assertTrue(any("copy may still say 'keeper'" in n for n in notes))

    def test_move_to_another_owner_is_held_and_the_rest_still_syncs(self):
        gh = FakeGitHub({"fresh": "About."}, {"fresh": skill_files("fresh")},
                        renamed={"keeper": "someone-else/keeper"})
        actions, notes = self.run_sync(gh)
        self.assertEqual(actions, {("hold", "keeper"), ("add", "fresh")})
        keeper = next(s for s in self.manifest["skills"] if s["name"] == "keeper")
        self.assertEqual(keeper["repo"], "arm-pz/keeper")
        self.assertTrue(any("moved to someone-else/keeper" in n for n in notes))

    def test_rename_keeps_entry_name_when_skill_folder_kept_it(self):
        self.manifest["skills"][0]["path"] = "skills/keeper"
        gh = FakeGitHub({"keeper-kit": "About."}, {"keeper-kit": skill_files("keeper", folder="skills/keeper")},
                        renamed={"keeper": "keeper-kit"})
        self.run_sync(gh)
        e = self.manifest["skills"][0]
        self.assertEqual((e["name"], e["repo"], e["path"]), ("keeper", "arm-pz/keeper-kit", "skills/keeper"))
        self.assertNotIn("aliases", e)

    def test_gone_repo_is_removed_from_entries_and_workflows(self):
        self.manifest["skills"].append(entry("other", order=2,
                                             quality=self.manifest["skills"][0]["quality"]))
        self.manifest["workflows"][0]["steps"].append({"skills": ["other"]})
        gh = FakeGitHub({"other": "About."}, {"other": skill_files("other")})
        actions, _ = self.run_sync(gh)
        self.assertEqual(actions, {("remove", "keeper")})
        self.assertEqual(self.names(), ["other"])
        self.assertEqual(self.manifest["workflows"][0]["steps"], [{"skills": ["other"]}])

    def test_unreadable_repo_stops_instead_of_removing(self):
        gh = FakeGitHub({}, {})
        gh.gh_json = (lambda *a: (None, "HTTP 502 Bad Gateway")
                      if a[0] == "api" else FakeGitHub({}, {}).gh_json(*a))
        gh.install(self)
        with self.assertRaises(SystemExit):
            sync.plan(self.root, self.manifest, [])

    def test_generated_page_is_refreshed_when_head_moves(self):
        files = skill_files("gen-skill", desc="New description. Use when asked.")
        gh = FakeGitHub({"keeper": "About.", "gen-skill": "About."},
                        {"keeper": skill_files("keeper"), "gen-skill": files}, heads={"gen-skill": "b" * 40})
        gh.install(self)
        source, _ = discover.measure("gen-skill", skill_files("gen-skill"), ".")
        self.manifest["skills"].append(entry("gen-skill", page="generated", order=2,
                                             pageSource=dict(source, commit="0" * 40)))
        actions, _ = self.run_sync(gh)
        self.assertEqual(actions, {("refresh", "gen-skill"), ("quality", "gen-skill")})
        e = self.manifest["skills"][1]
        self.assertEqual(e["quality"]["commit"], "bbbbbbb")
        self.assertEqual((e["pageSource"]["commit"], e["blurb"]), ("b" * 40, "Hand-written."))
        self.assertTrue(e["pageSource"]["description"].startswith("New description."))

    def test_quality_record_follows_head(self):
        files = {"SKILL.md": b"---\nname: keeper\nversion: 1.4.0\ndescription: Does a thing. "
                             b"Not for poems; or essays.\n---\n", "LICENSE": LICENSE}
        gh = FakeGitHub({"keeper": "About."}, {"keeper": files}, heads={"keeper": "c" * 40})
        actions, _ = self.run_sync(gh)
        self.assertEqual(actions, {("quality", "keeper")})
        self.assertEqual(self.manifest["skills"][0]["quality"],
                         {"version": "1.4.0", "commit": "ccccccc", "updated": "2026-10-24",
                          "notFor": ["poems", "essays"]})
        self.assertEqual(self.run_sync(gh)[0], set())


if __name__ == "__main__":
    unittest.main()
