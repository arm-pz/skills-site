import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gen_home

TESTED = {"date": "2026-10-24", "target": "example.com", "result": "Found 2 & fixed.",
          "evidence": "/#proof"}
MANIFEST = {
    "schema": 1,
    "site": "https://skillsmith.tech",
    "groups": [
        {"id": "writing-growth", "title": "Writing & Growth", "descriptor": "editorial", "order": 1},
        {"id": "ship-checks", "title": "Ship Checks", "descriptor": "audits", "order": 2},
    ],
    "skills": [
        {"name": "alpha", "repo": "arm-pz/alpha", "path": "skills/alpha",
         "group": "writing-growth", "tag": "editorial", "title": "Alpha",
         "blurb": "Edits & proofs.", "stats": "1 file", "install": "npx skills add arm-pz/alpha",
         "page": "bespoke", "order": 1},
        {"name": "beta", "repo": "arm-pz/beta", "path": ".", "group": "ship-checks",
         "tag": "release", "title": "Beta", "blurb": "Ships.", "stats": "2 files",
         "install": "npx skills add arm-pz/beta", "page": "none", "order": 2},
    ],
    "workflows": [{"id": "pour-over", "number": 1, "name": "Pour-over", "title": "Edit a page",
                   "slug": "edit-a-page", "summary": "Edit it & ship it.",
                   "steps": [{"skills": ["alpha"]}, {"skills": ["alpha"], "optional": True}],
                   "note": "One & done."}],
}
MOD = dict(MANIFEST["skills"][0], name="watch", title="Watch", kind="mod", order=3,
           install="/plugin install watch")


def region(name, indent="    "):
    return f"{indent}<!-- gen:{name}:start -->\nold\n{indent}<!-- gen:{name}:end -->\n"


TEXT = ("<head>\n" + region("jsonld-skills", "") + "</head>\n<body>\n"
        + region("jump") + region("skills") + region("mods")
        + "<!-- gen:stats:start -->x<!-- gen:stats:end -->\n"
        + region("workflows") + region("outcomes") + region("flagships") + "</body>\n")


def render(manifest=MANIFEST, text=TEXT):
    return gen_home.render(text, manifest)


class GenHomeTest(unittest.TestCase):
    def test_skills_region_writes_one_card_and_the_group_count(self):
        out = render()
        self.assertEqual(out.count('class="skill"'), 1)
        self.assertIn(">Writing &amp; Growth</h2>", out)
        self.assertIn("1 skill · editorial", out)
        self.assertIn('<a href="/alpha/">Alpha</a>', out)
        self.assertIn('<a href="#writing-growth">Writing &amp; Growth</a>', out)

    def test_mods_get_their_own_region(self):
        out = render({**MANIFEST, "skills": MANIFEST["skills"] + [MOD]})
        skills = out[out.index("gen:skills:start"):out.index("gen:skills:end")]
        mods = out[out.index("gen:mods:start"):out.index("gen:mods:end")]
        self.assertNotIn("watch", skills)
        self.assertIn('<span class="chip chip-hot">Claude Code mod</span>', mods)
        self.assertIn("1 skill and 1 mod · 1 workflow", out)

    def test_jsonld_counts_skills_only(self):
        out = render({**MANIFEST, "skills": MANIFEST["skills"] + [MOD]})
        self.assertIn('"numberOfItems": 1', out)
        self.assertIn('"url": "https://skillsmith.tech/skills/"', out)

    def test_escaping(self):
        self.assertIn("Edits &amp; proofs.", render())

    def test_render_is_idempotent(self):
        once = render()
        self.assertEqual(render(text=once), once)

    def test_check_detects_a_blurb_change(self):
        changed = {**MANIFEST, "skills": [dict(MANIFEST["skills"][0], blurb="Changed.")]}
        self.assertNotEqual(render(changed), render())

    def test_empty_group_is_not_rendered(self):
        self.assertNotIn('id="ship-checks"', render())

    def test_chain_and_tested_chips(self):
        alpha = dict(MANIFEST["skills"][0], chain=True, tested=TESTED)
        out = render({**MANIFEST, "skills": [alpha]})
        self.assertIn('<span class="chip chip-hot">chain</span>', out)
        self.assertIn('<span class="chip chip-hot">tested 24 Oct 2026</span>', out)

    def test_workflow_and_outcome_regions_link_the_workflow_page(self):
        out = render()
        self.assertIn('<a href="/alpha/">alpha</a> <span class="opt">optional</span>', out)
        self.assertIn("One &amp; done.", out)
        self.assertIn('<p class="flow-id">Brew 1 · Pour-over</p>', out)
        self.assertIn('<h3><a href="/workflows/edit-a-page/">Edit a page</a></h3>', out)
        self.assertIn('<a class="outcome" href="/workflows/edit-a-page/">', out)
        self.assertIn("1 skill · Brew 1 · Pour-over", out)

    def test_flagships_need_a_featured_skill_and_show_its_run(self):
        self.assertNotIn('class="flag"', render())
        alpha = dict(MANIFEST["skills"][0], featured=1, tested=TESTED)
        out = render({**MANIFEST, "skills": [alpha]})
        self.assertIn("Shown working, 24 Oct 2026, on example.com.", out)
        self.assertIn("Found 2 &amp; fixed.", out)
        self.assertIn('data-copy="npx skills add arm-pz/alpha"', out)

    def test_unknown_region_stops(self):
        with self.assertRaises(SystemExit):
            render(text="<!-- gen:nope:start --><!-- gen:nope:end -->")


class FlowPageTest(unittest.TestCase):
    def test_page_lists_steps_and_one_install_block(self):
        flow = MANIFEST["workflows"][0]
        out = gen_home.render_flow_page(flow, MANIFEST)
        self.assertIn("<h1>Edit a page</h1>", out)
        self.assertIn('<link rel="canonical" href="https://skillsmith.tech/workflows/edit-a-page/">', out)
        self.assertIn("Step 2 · optional", out)
        self.assertIn("npx skills add arm-pz/alpha  # step 1\n", out)
        self.assertIn("# step 2, optional", out)
        self.assertIn('"@type": "HowTo"', out)
        self.assertNotIn("{{", out)

    def test_write_removes_a_dropped_workflow_and_check_flags_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "site").mkdir()
            for rel in gen_home.HUB_PAGES:
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / rel).write_text("<p>shell</p>")
            old = root / "workflows" / "gone" / "index.html"
            old.parent.mkdir(parents=True)
            old.write_text(gen_home.FLOW_MARKER)
            kept = root / "workflows" / "hand-made" / "index.html"
            kept.parent.mkdir(parents=True)
            kept.write_text("<p>not generated</p>")
            self.assertEqual(gen_home.stale_flow_dirs(root, MANIFEST), [old.parent])


if __name__ == "__main__":
    unittest.main()
