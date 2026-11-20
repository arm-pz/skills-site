#!/usr/bin/env python3
"""Flag mechanical AI-writing patterns in a text or Markdown file.

Usage:
  python slop_scan.py FILE [--plain-text] [--strict]
  python slop_scan.py - < draft.txt

Prints one line per hit: line number, rule, matched text. Fenced code blocks, inline code and YAML
frontmatter are skipped. --plain-text also flags curly quotes. --strict exits 1 when there is any
hit; otherwise the exit code is 0, because a hit is something to look at and may be fine in context.

The scan cannot see forced groups of three, inflated claims in unlisted words, a change of voice,
or an empty sentence. A clean result does not mean the text is free of them.
"""
import argparse
import re
import sys

VOCAB = (r"delv(e|es|ed|ing)|deep dives?|crucial|pivotal|intricate|intricacies|tapestry|vibrant|"
         r"landscape|enduring|testament|underscor(e|es|ed|ing)|showcas(e|es|ed|ing)|foster(s|ed|ing)?|"
         r"garner(s|ed|ing)?|robust|interplay|meticulous(ly)?|aligns? with|resonates? with|"
         r"bolster(s|ed|ing)?|utili[sz](e|es|ed|ing)|serves? as|boasts?")
PROMO = (r"renowned|groundbreaking|breathtaking|nestled|world-class|stunning|diverse array|"
         r"commitment to excellence|remarkable|profound|innovative|impressive")
SIGNIFICANCE = (r"marks? a (major |significant )?(shift|turning point)|turning point|broader trend|"
                r"enduring legacy|plays? a (pivotal|crucial|key|vital) role|sets? the stage|"
                r"broader landscape|stands as a")
ATTRIBUTION = (r"experts (say|believe|agree)|observers have noted|critics argue|"
               r"industry reports suggest|sources indicate|many believe|studies show")
CHATBOT = (r"of course!|certainly!|absolutely!|you're absolutely right|great question|"
           r"i hope this helps|here is a detailed breakdown|here's a comprehensive overview|"
           r"would you like me to|let me know if you'd like|is there anything else|"
           r"i'm happy to|feel free to")
PARALLEL = (r"not only\b[^.\n]{0,80}\bbut|not just\b[^.\n]{0,80}\bbut|"
            r"\bnot (just|only|merely)\b[^.\n]{0,60}[,;\u2014] ?(it|this|that|they)(['’]s|['’]re| is| are)\b|"
            r"\b(it|this|that)(['’]s| is) not\b[^.\n]{0,60}[,;.] (it|this|that)(['’]s| is)\b|"
            r"\b(is|are|was)n['’]t\b[^.\n]{0,60}\. (It|They|This)(['’]s|['’]re| is| are)\b|"
            r"\bnot\b[^.\n]{0,40}, but rather\b|\bno \w+, no \w+, just\b|\brather than\b")
ING_TAIL = (r", (highlighting|underscoring|reflecting|ensuring|fostering|enhancing|symboli[sz]ing|"
            r"demonstrating|showcasing|contributing to)\b")
CANNED = r"^(in conclusion|in summary|overall|additionally)\b,?"
PLACEHOLDER = (r"\[(your|insert|specific|add|name|company|date)\b[^\]\n]*\]|XX/XX/XXXX|INSERT_URL|"
               r"SOURCE_PUBLISHER|lorem ipsum")
MARKUP = r"【[^】]*】|oaicite|contentReference|turn\d+(search|view|news)\d+|\butm_[a-z]+="
RELATION = r"associated with|connected to|linked with|in connection with"

LINE_RULES = [
    ("em-dash", re.compile("—")),
    ("vocabulary", re.compile(rf"\b({VOCAB})\b", re.I)),
    ("promotional", re.compile(rf"\b({PROMO})\b", re.I)),
    ("significance", re.compile(rf"\b({SIGNIFICANCE})\b", re.I)),
    ("vague-attribution", re.compile(rf"\b({ATTRIBUTION})\b", re.I)),
    ("chatbot-phrase", re.compile(rf"({CHATBOT})", re.I)),
    ("negative-parallelism", re.compile(PARALLEL, re.I)),
    ("ing-tail", re.compile(ING_TAIL, re.I)),
    ("canned-opener", re.compile(CANNED, re.I)),
    ("vague-relationship", re.compile(rf"\b({RELATION})\b", re.I)),
    ("placeholder", re.compile(PLACEHOLDER, re.I)),
    ("tool-markup", re.compile(MARKUP)),
]
CURLY = re.compile("[‘’“”]")
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐⬆✅❌]")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*$")
BOLD_LABEL = re.compile(r"^\s*([-*+]|\d+[.)])\s+\*\*[^*\n]+\*\*\s*[:–-]|^\s*([-*+]|\d+[.)])\s+\*\*[^*\n]+:\*\*")
RULE_LINE = re.compile(r"^\s*([-*_])(\s*\1){2,}\s*$")
SMALL = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "of", "on", "or", "the", "to", "vs", "with"}


def title_case(heading):
    """True when a heading of three or more words capitalises every word that is not a small one."""
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z'-]*", heading)]
    if len(words) < 3:
        return False
    rest = [w for w in words[1:] if w.lower() not in SMALL]
    # All-caps words are acronyms and say nothing about the casing style.
    rest = [w for w in rest if not w.isupper()]
    return len(rest) >= 2 and all(w[0].isupper() for w in rest)


def scan(text, plain_text=False):
    """Return a list of (line_number, rule, matched_text)."""
    hits = []
    lines = text.replace("\r\n", "\n").split("\n")
    in_fence = False
    in_front = bool(lines) and lines[0].strip() == "---"
    bold_run = []
    for n, raw in enumerate(lines, 1):
        if in_front:
            if n > 1 and raw.strip() == "---":
                in_front = False
            continue
        if raw.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line = re.sub(r"`[^`\n]*`", "", raw)

        for rule, rx in LINE_RULES:
            for m in rx.finditer(line.strip() if rule == "canned-opener" else line):
                hits.append((n, rule, m.group(0)))
        if plain_text:
            for m in CURLY.finditer(line):
                hits.append((n, "curly-quote", m.group(0)))

        h = HEADING.match(line)
        if h:
            if title_case(h.group(2)):
                hits.append((n, "title-case-heading", h.group(2)))
            if EMOJI.search(h.group(2)):
                hits.append((n, "emoji-decoration", h.group(2)))
        elif re.match(r"^\s*([-*+]|\d+[.)])\s+", line) and EMOJI.match(re.sub(r"^\s*([-*+]|\d+[.)])\s+", "", line)):
            hits.append((n, "emoji-decoration", line.strip()[:40]))
        if RULE_LINE.match(line):
            hits.append((n, "horizontal-rule", line.strip()))

        # One bold-label bullet is ordinary; three in a row is the stock list format.
        if BOLD_LABEL.match(line):
            bold_run.append(n)
        elif line.strip() and not line.startswith((" ", "\t")):
            if len(bold_run) >= 3:
                hits.append((bold_run[0], "bold-label-list", f"{len(bold_run)} bullets"))
            bold_run = []
    if len(bold_run) >= 3:
        hits.append((bold_run[0], "bold-label-list", f"{len(bold_run)} bullets"))
    return sorted(hits)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file", help="path to a text or Markdown file, or - for stdin")
    ap.add_argument("--plain-text", action="store_true", help="also flag curly quotes")
    ap.add_argument("--strict", action="store_true", help="exit 1 when there is any hit")
    a = ap.parse_args(argv)

    if a.file == "-":
        text = sys.stdin.read()
    else:
        with open(a.file, encoding="utf-8-sig") as fh:
            text = fh.read()
    hits = scan(text, a.plain_text)
    counts = {}
    for n, rule, found in hits:
        counts[rule] = counts.get(rule, 0) + 1
        print(f"{n:>5}  {rule:<22}{found}")
    summary = ", ".join(f"{rule} {c}" for rule, c in sorted(counts.items())) or "none"
    print(f"\n{len(hits)} hits: {summary}")
    print("Not checked: groups of three, unlisted inflated wording, voice changes, empty sentences.")
    return 1 if hits and a.strict else 0


if __name__ == "__main__":
    sys.exit(main())
