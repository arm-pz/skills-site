import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import twins

PAGE = """<!DOCTYPE html><html><head><title>Alpha &amp; co</title>
<meta name="description" content="Alpha does a thing.">
<script type="application/ld+json">
{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "alpha"}
</script>
</head><body>
<nav><a href="/">All skills</a></nav>
<header><h1>Alpha <em>edits</em></h1><p class="lead">One line.</p>
<button>Copy</button><span class="sr-only">status</span></header>
<section><h2>Steps</h2><ul><li>First</li><li>Second <a href="/beta/">beta</a></li></ul>
<ol><li>One</li><li>Two</li></ol>
<p>Run <code>npx skills add arm-pz/alpha</code>.<svg><text>icon</text></svg></p>
<table><thead class="sr-only"><tr><th>File</th><th>Lines</th></tr></thead>
<tbody><tr><td>SKILL.md</td><td>12</td></tr></tbody></table>
<p><span>44</span><span>commands</span> <a href="#top">top</a></p>
<pre>line one
  line two</pre>
</section>
<footer>
  <div class="wrap">Alpha is open.</div>
</footer>
<script>var x = "<p>not text</p>";</script>
</body></html>"""

CANON = "https://skills.caffeinity.com/alpha/"


class StampTest(unittest.TestCase):
    def setUp(self):
        self.html = twins.stamp(PAGE, "2026-10-14", "2026-10-24", "/alpha/index.md")

    def test_jsonld_gets_dates_and_author(self):
        ld = json.loads(twins.LD_RE.search(self.html).group(2))
        self.assertEqual(ld["datePublished"], "2026-10-14")
        self.assertEqual(ld["dateModified"], "2026-10-24")
        self.assertEqual(ld["author"]["name"], twins.AUTHOR["name"])

    def test_visible_line_and_alternate_link(self):
        self.assertIn('<link rel="alternate" type="text/markdown" href="/alpha/index.md">\n</head>',
                      self.html)
        self.assertIn('<footer>\n  <p class="page-stamp"', self.html)
        self.assertIn('Published <time datetime="2026-10-14">Oct 14, 2026</time>', self.html)
        self.assertIn('Updated <time datetime="2026-10-24">Oct 24, 2026</time>', self.html)

    def test_same_day_has_no_updated(self):
        html = twins.stamp(PAGE, "2026-10-24", "2026-10-24", "/alpha/index.md")
        self.assertNotIn("Updated", html)

    def test_stamping_twice_fails(self):
        with self.assertRaises(SystemExit):
            twins.stamp(self.html, "2026-10-14", "2026-10-24", "/alpha/index.md")

    def test_graph_node_is_found(self):
        data = {"@graph": [{"@type": "Organization"}, {"@type": "WebSite", "name": "x"}]}
        self.assertEqual(twins.dated_node(data)["@type"], "WebSite")
        self.assertIsNone(twins.dated_node({"@type": "ItemList"}))


class MarkdownTest(unittest.TestCase):
    def setUp(self):
        self.md = twins.to_markdown(PAGE, CANON, "2026-10-14", "2026-10-24")

    def test_front_matter(self):
        self.assertTrue(self.md.startswith('---\ntitle: "Alpha & co"\n'
                                           'description: "Alpha does a thing."\n'
                                           f"canonical: {CANON}\n"))
        self.assertIn("published: 2026-10-14\nmodified: 2026-10-24\n---\n", self.md)

    def test_content(self):
        self.assertIn("# Alpha *edits*\n\nOne line.", self.md)
        self.assertIn("- First\n- Second [beta](https://skills.caffeinity.com/beta/)", self.md)
        self.assertIn("1. One\n2. Two", self.md)
        self.assertIn("Run `npx skills add arm-pz/alpha`.", self.md)
        self.assertIn("| File | Lines |\n| --- | --- |\n| SKILL.md | 12 |", self.md)
        self.assertIn("44 commands top", self.md)
        self.assertIn("```\nline one\n  line two\n```", self.md)
        self.assertIn("Alpha is open.", self.md)

    def test_chrome_is_dropped(self):
        for text in ("All skills", "Copy", "status", "icon", "not text", "page-stamp"):
            self.assertNotIn(text, self.md.split("---", 2)[2])


class RunTest(unittest.TestCase):
    def test_writes_twins_beside_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp)
            (dist / "alpha").mkdir()
            (dist / "index.html").write_text(PAGE)
            (dist / "alpha/index.html").write_text(PAGE)
            manifest = {"skills": [{"name": "alpha", "page": "bespoke", "order": 1},
                                   {"name": "beta", "page": "none", "order": 2}]}
            written = twins.run(dist, dist, manifest, lambda path: ("2026-10-14", "2026-10-24"))
            self.assertEqual(written, ["index.md", "alpha/index.md"])
            self.assertIn("canonical: https://skills.caffeinity.com/\n",
                          (dist / "index.md").read_text())
            self.assertIn('href="/alpha/index.md"', (dist / "alpha/index.html").read_text())


if __name__ == "__main__":
    unittest.main()
