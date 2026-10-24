"""Stamp every page in dist/ with its dates and author, and write its Markdown twin.

Runs after make_dist.sh copies the pages. The committed pages stay as they are: the dates come
from git (first and last commit of the page's source file, or today for a page this run changed),
so they can only be known at build time. Each page gets

  - datePublished, dateModified and author in its main JSON-LD node,
  - a visible "By ... · Published ... · Updated ..." line at the top of its footer,
  - <link rel="alternate" type="text/markdown"> pointing at its twin, and
  - the twin itself at <page>/index.md: the same content as Markdown, front matter first.

The twin's canonical is the HTML page (a Link header in _headers and in functions/_middleware.js),
so search engines do not count the two as duplicates.
"""

import argparse
import datetime
import json
import re
import subprocess
import sys
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

import skilllib

AUTHOR = {"@type": "Person", "name": "Abdul Rahman P Z", "url": "https://github.com/arm-pz"}
STAMP_MARK = 'class="page-stamp"'
LD_RE = re.compile(r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)', re.S)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
DESC_RE = re.compile(r'<meta name="description" content="([^"]*)"')
DATED = ("SoftwareApplication", "WebPage", "WebSite", "Article", "CreativeWork")


def pages(manifest):
    """(dist-relative html path, source path, canonical URL) for the hub and every page."""
    result = [("index.html", "index.html", f"{skilllib.SITE}/")]
    for s in sorted((s for s in manifest["skills"] if s["page"] != "none"),
                    key=lambda s: s["order"]):
        path = f"{s['name']}/index.html"
        result.append((path, path, f"{skilllib.SITE}/{s['name']}/"))
    return result


def git_dates(root, path, today):
    """(published, modified) as YYYY-MM-DD; today for a file this run created or changed."""
    def log(*args):
        return subprocess.run(["git", "log", *args, "--format=%cs", "--", path], cwd=root,
                              capture_output=True, text=True).stdout.split()

    changed = subprocess.run(["git", "status", "--porcelain", "--", path], cwd=root,
                             capture_output=True, text=True).stdout.strip()
    history = log("--follow")
    modified = today if changed or not history else history[0]
    published = history[-1] if history else today
    return published, modified


def human(date):
    day = datetime.date.fromisoformat(date)
    return f"{day:%b} {day.day}, {day.year}"


def dated_node(data):
    """The JSON-LD node that should carry the page's dates: the first CreativeWork-like one."""
    nodes = data.get("@graph", [data]) if isinstance(data, dict) else []
    for kind in DATED:
        for node in nodes:
            if isinstance(node, dict) and node.get("@type") == kind:
                return node
    return None


def stamp_jsonld(html, published, modified):
    def place(match):
        data = json.loads(match.group(2))
        node = dated_node(data)
        if node is None or state["done"]:
            return match.group(0)
        node.setdefault("datePublished", published)
        node["dateModified"] = modified
        node.setdefault("author", AUTHOR)
        state["done"] = True
        body = json.dumps(data, indent=2, ensure_ascii=False).replace("</", "<\\/")
        return match.group(1) + body + match.group(3)

    state = {"done": False}
    html = LD_RE.sub(place, html)
    if not state["done"]:
        raise SystemExit("no JSON-LD node to carry the page dates")
    return html


def stamp_line(published, modified, twin):
    updated = "" if modified == published else (
        f' · Updated <time datetime="{modified}">{human(modified)}</time>')
    return (f'  <p {STAMP_MARK} style="max-width:1180px;margin:0 auto;'
            f'padding:24px clamp(16px,5vw,56px) 0;font-size:14px;opacity:.8">'
            f'By <a href="{escape(AUTHOR["url"])}" rel="author">{escape(AUTHOR["name"])}</a>'
            f' · Published <time datetime="{published}">{human(published)}</time>{updated}'
            f' · <a href="{twin}" type="text/markdown">Markdown</a></p>\n')


def stamp(html, published, modified, twin):
    if STAMP_MARK in html:
        raise SystemExit("page is already stamped")
    html = stamp_jsonld(html, published, modified)
    if "</head>" not in html or "<footer" not in html:
        raise SystemExit("page has no </head> or <footer>")
    html = html.replace(
        "</head>", f'<link rel="alternate" type="text/markdown" href="{twin}">\n</head>', 1)
    at = html.index(">", html.index("<footer")) + 1
    return html[:at] + "\n" + stamp_line(published, modified, twin) + html[at:].lstrip("\n")


class Markdown(HTMLParser):
    """A small HTML-to-Markdown converter for these pages: headings, paragraphs, lists, links,
    code, tables and emphasis. Navigation, scripts, styles, icons, buttons and anything hidden
    from screen readers are dropped, so the twin reads like the page without its chrome."""

    SKIP = {"script", "style", "svg", "nav", "button", "template", "head", "title"}
    VOID = {"br", "hr", "img", "input", "meta", "link", "source", "wbr"}
    BLOCK = {"p", "div", "section", "article", "header", "footer", "main", "aside", "figure",
             "figcaption", "noscript", "ul", "ol", "table", "blockquote", "dl", "dd", "dt",
             "form", "fieldset", "details", "summary"}
    INLINE = {"span", "a", "strong", "b", "em", "i", "code", "small", "time", "s", "del"}

    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base = base
        self.out = []          # finished blocks
        self.line = []         # inline text of the current block
        self.stack = []        # open tags with whether they are skipped
        self.skip = 0
        self.lists = []        # "ul" or ["ol", n]
        self.links = []        # open <a> hrefs
        self.pre = 0
        self.row = None
        self.rows = None
        self.cell = None
        self.after_inline = False  # an inline element just closed with no text since

    # -- helpers
    def flush(self):
        text = "".join(self.line)
        self.line = []
        if self.pre:
            return
        text = re.sub(r"[ \t\r\n]+", " ", text).strip()
        if text:
            self.out.append(text)

    def emit(self, text):
        if self.cell is not None:
            self.cell.append(text)
        else:
            self.line.append(text)

    @staticmethod
    def hidden(tag, attrs):
        a = dict(attrs)
        classes = (a.get("class") or "").split()
        if tag == "thead":  # a visually hidden table header still names the columns
            return False
        return (tag in Markdown.SKIP or a.get("aria-hidden") == "true" or "hidden" in a
                or "sr-only" in classes or "page-stamp" in classes)

    # -- parser hooks
    def handle_starttag(self, tag, attrs):
        if tag in self.VOID:
            if not self.skip and tag == "br":
                self.emit("\n" if self.pre else " ")
            return
        hide = self.hidden(tag, attrs)
        self.stack.append((tag, hide))
        if hide:
            self.skip += 1
        if self.skip:
            return
        a = dict(attrs)
        if self.after_inline and tag in self.INLINE:
            self.emit(" ")  # <span>44</span><span>commands</span> reads as two words
        self.after_inline = False
        if re.fullmatch(r"h[1-6]", tag):
            self.flush()
            self.line.append("#" * int(tag[1]) + " ")
        elif tag == "li":
            self.flush()
            depth = "  " * (len(self.lists) - 1)
            top = self.lists[-1] if self.lists else "ul"
            if isinstance(top, list):
                top[1] += 1
                self.line.append(f"{depth}{top[1]}. ")
            else:
                self.line.append(f"{depth}- ")
        elif tag in ("ul", "ol"):
            self.flush()
            self.lists.append("ul" if tag == "ul" else ["ol", 0])
        elif tag == "pre":
            self.flush()
            self.pre += 1
        elif tag == "table":
            self.flush()
            self.rows = []
        elif tag == "tr" and self.rows is not None:
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = []
        elif tag in self.BLOCK:
            self.flush()
        elif tag in ("strong", "b"):
            self.emit("**")
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag in ("s", "del"):
            self.emit("~~")
        elif tag == "code" and not self.pre:
            self.emit("`")
        elif tag == "a":
            href = a.get("href") or ""
            if href.startswith("#") or not href:
                self.links.append(None)
            else:
                self.links.append(urljoin(self.base, href))
                self.emit("[")

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        while self.stack:
            open_tag, hide = self.stack.pop()
            self._close(open_tag, hide)
            if open_tag == tag:
                break

    def _close(self, tag, hide):
        if hide:
            self.skip -= 1
            return
        if self.skip:
            return
        self.after_inline = tag in self.INLINE
        if re.fullmatch(r"h[1-6]", tag) or tag in ("li", "p"):
            self.flush()
        elif tag in ("ul", "ol"):
            self.flush()
            if self.lists:
                self.lists.pop()
        elif tag == "pre":
            code = "".join(self.line).strip("\n")
            self.line = []
            self.pre -= 1
            self.out.append(f"```\n{code}\n```")
        elif tag in ("td", "th") and self.cell is not None:
            text = re.sub(r"\s+", " ", "".join(self.cell)).strip().replace("|", "\\|")
            self.row.append(text)
            self.cell = None
        elif tag == "tr" and self.row is not None:
            if any(self.row):
                self.rows.append(self.row)
            self.row = None
        elif tag == "table" and self.rows is not None:
            if self.rows:
                width = max(len(r) for r in self.rows)
                rows = [r + [""] * (width - len(r)) for r in self.rows]
                lines = ["| " + " | ".join(rows[0]) + " |",
                         "| " + " | ".join(["---"] * width) + " |"]
                lines += ["| " + " | ".join(r) + " |" for r in rows[1:]]
                self.out.append("\n".join(lines))
            self.rows = None
        elif tag in self.BLOCK:
            self.flush()
        elif tag in ("strong", "b"):
            self.emit("**")
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag in ("s", "del"):
            self.emit("~~")
        elif tag == "code" and not self.pre:
            self.emit("`")
        elif tag == "a" and self.links:
            href = self.links.pop()
            if href:
                self.emit(f"]({href})")

    def handle_data(self, data):
        if not self.skip:
            self.emit(data)
            self.after_inline = False

    def result(self):
        self.flush()
        text = "\n\n".join(self.out)
        text = re.sub(r"\*\*\s*\*\*|(?<!`)` *`(?!`)|\[\]\([^)]*\)", "", text)
        return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def list_tight(text):
    """Join consecutive list items into one list instead of one paragraph each."""
    def kind(line):
        match = re.match(r"\s*(- |\d+\. )", line)
        return match and ("-" if match.group(1) == "- " else "1")

    out = []
    for block in text.split("\n\n"):
        if out and kind(block) and kind(block) == kind(out[-1].split("\n")[-1]):
            out[-1] += "\n" + block
        else:
            out.append(block)
    return "\n\n".join(out)


def to_markdown(html, canonical, published, modified):
    body = html[html.find("<body"):] if "<body" in html else html
    parser = Markdown(canonical)
    parser.feed(body)
    parser.close()
    title = TITLE_RE.search(html)
    desc = DESC_RE.search(html)

    def yaml(value):
        return json.dumps(value, ensure_ascii=False)

    front = ["---",
             f"title: {yaml(unescape(title.group(1).strip()) if title else canonical)}"]
    if desc:
        front.append(f"description: {yaml(unescape(desc.group(1)))}")
    front += [f"canonical: {canonical}",
              f"author: {yaml(AUTHOR['name'])}",
              f"published: {published}",
              f"modified: {modified}",
              "---", ""]
    return "\n".join(front) + "\n" + list_tight(parser.result())


def run(root, dist, manifest, dates):
    written = []
    for rel, source, canonical in pages(manifest):
        page = dist / rel
        published, modified = dates(source)
        html = page.read_text(encoding="utf-8")
        twin_rel = Path(rel).with_suffix(".md")
        twin_href = "/" + twin_rel.as_posix()
        with open(page, "w", encoding="utf-8", newline="") as fh:
            fh.write(stamp(html, published, modified, twin_href))
        with open(dist / twin_rel, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(to_markdown(html, canonical, published, modified))
        written.append(twin_rel.as_posix())
    return written


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    root = Path(args.root)
    manifest = skilllib.load_manifest(root)
    skilllib.validate_manifest(manifest)
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    written = run(root, root / "dist", manifest, lambda path: git_dates(root, path, today))
    print(f"twins: {len(written)} pages stamped, {len(written)} Markdown twins written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
