import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gen_pages import build, cats, pr, install_js, nos

SKILLS = []

SKILLS.append({
 "name": "findable-polish",
 "title": "findable-polish — Audit Discoverability, Then Generate the Fix",
 "desc": "An open agent skill that runs the Findable audit on a README, skill page or landing copy, then hands every finding to Wordsmith for 2-3 polished alternatives. Diagnosis plus concrete rewrites in one pass.",
 "ogdesc": "An open agent skill that chains Findable (what people actually search for, and where your surfaces fall short) into Wordsmith (two or three alternatives per finding that fix it without touching your meaning or facts). Audit first, rewrite second, copy-paste ready. Proven on its own repo: seven searches returned nothing, six metadata gaps named, fixes applied and verified the same day.",
 "nav_mid": "The workflow",
 "h1": "It isn't being found. First learn <em>why</em>, then rewrite the surfaces.",
 "hsub": "One install chains two skills: <b>Findable</b> audits the surfaces people actually search \u2014 README opening, GitHub About text, topics, site page \u2014 against the task queries a stranger would type, and <b>Wordsmith</b> writes two or three alternatives per finding that fix it without inventing a fact. You get the diagnosis and the cure in one pass.",
 "stats": '''
          <span><b>2</b> chained skills</span>
          <span><b>5-10</b> target queries</span>
          <span><b>2-3</b> options per issue</span>
          <span><b>0</b> facts invented</span>''',
 "ms": '''
          <p class="ms-label">findable-polish run against its own repo, measured 2026-10-19</p>
          <p><span class="ms-before"><s>"nobody finds it \u2014 time to write punchier copy."</s></span></p>
          <ul class="ms-findings">
            <li><span class="sev high">0 hits</span><span>Seven live searches ran first \u2014 four by name, three by task \u2014 and the repo appeared in <b>none</b> of them. The gap was indexing and listing, not wording.</span></li>
            <li><span class="sev med">6 gaps</span><span>The metadata read named six fixable surfaces: zero topics, no homepage, no release, no install line, a 60-character description with no audience, and a README opening naming neither agent nor task.</span></li>
            <li><span class="sev ok">applied</span><span>Alternatives were drafted per gap, then applied and verified: 15 topics, a task-first About and a rewritten README landed on the repo the same day.</span></li>
          </ul>
          <div class="ms-after">
            <p class="ms-label">what the run shows</p>
            <p class="hl">A rewrite that doesn't start from what people type is decoration. Audit first, alternatives second.</p>
          </div>
          <div class="ms-foot"><span>searches measured live, not assumed</span><span>indexing lags \u2014 re-check in two to three weeks</span>''',
 "install_h2": "Copy one line. Audit the surface, then rewrite it.",
 "cmd_note": 'The install line from the repo README. This skill is a chain: <b>findable</b> and <b>wordsmith</b> must be installed too \u2014 if either is missing it says so and stops.',
 "audit": '''
    <p class="kicker">the workflow</p>
    <h2>Three phases. The audit output arrives verbatim.</h2>
    <p class="lede">Phase one runs the Findable audit and hands its full report on, untouched \u2014 no summarising the evidence away. Phase two turns each finding into alternatives. Phase three returns everything in one copy-paste-ready block.</p>
    '''
      + cats([
      ("Audit", "1", "Findable reads the target content and derives the queries a stranger types, task-based, never name-based.", ["5-10 target queries","missing keywords","vague or audience-less description","weak opening line","absent About text or topics","same-name collisions"], False),
      ("Alternatives", "2", "Wordsmith treats each audit finding as its own rewrite task, in the author's voice and facts.", ["2-3 labelled options per issue","keywords woven in naturally","GitHub About and topic drafts","opening lines matched to queries","best option chosen with a reason"], False),
      ("Presentation", "3", "One three-part response: audit summary by severity, alternatives grouped by issue, and a merge recommendation.", ["severity-ordered findings","copy-paste-ready blocks","a 2-3 sentence overall recommendation","unchanged facts stay untouched"], False),
      ("Outside its boundary", "2 siblings", "The chain stops where its parts begin. Tuning the SKILL.md description that carries agent triggering is <a href=\"https://github.com/arm-pz/tune-skill\" target=\"_blank\" rel=\"noopener\" class=\"mono\">tune-skill</a>. Setting up a repo's discovery from scratch, with distribution targets, is <a href=\"https://github.com/arm-pz/findable\" target=\"_blank\" rel=\"noopener\" class=\"mono\">findable</a>. This skill writes human-facing copy from a real audit; it does not execute gh commands or push changes \u2014 it hands over the commands.", ["audits + drafts, never publishes","no trigger tuning","no resume work (recruiter-lens)","no code review"], True),
    ]),
 "principles": '''
    <p class="kicker">ground rules</p>
    <h2>What it refuses to do.</h2>
    '''
      + pr([
      ("Queries before copy", "Every rewrite is written from a search query a real stranger would type, derived and shown before any prose. Copy written from vibes gets audited again by the search engine, not by you."),
      ("Describe only what is real", "Alternatives may not claim features, install counts or compatibility the content doesn't support. A rewrite that adds a false capability is a worse audit result, not a better one."),
      ("Hand the audit over whole", "Phase two receives the full phase-one report verbatim. Summarising findings before rewriting them drops the awkward ones, and the awkward ones are the point."),
    ]),
 "cta": '''
  <div class="wrap">
    <h2>Both the diagnosis and the cure, in one pass.</h2>
    <p>Free, open, and every alternative traces back to a finding the audit named.</p>
    <a class="big-btn" href="#install">Install findable-polish</a>
    <a class="big-btn alt" href="https://github.com/arm-pz/findable-polish" target="_blank" rel="noopener">Read the source</a>
  </div>
''',
 "footer": '''
    <span>findable-polish — an open agent skill · <a href="../">all skills</a></span>
    <span><a href="https://github.com/arm-pz/findable-polish" target="_blank" rel="noopener">github.com/arm-pz/findable-polish</a></span>
  ''',
 "noscript": nos("findable-polish", "Requires the <span class=\"mono\">findable</span> and <span class=\"mono\">wordsmith</span> skills; the chain names and stops on a missing dependency."),
 "cmds_js": install_js("findable-polish", "Requires the findable and wordsmith skills installed alongside."),
})

SKILLS.append({
 "name": "keyword-resolver",
 "title": "keyword-resolver — One Query, One Owner, Then the Rewrite",
 "desc": "An open agent skill that resolves keyword cannibalization with Keyword-Guard, then generates alternative titles, H1s and meta descriptions with Wordsmith. Ownership map first, copy second.",
 "ogdesc": "An open agent skill for the moment two of your pages rank for the same query. It chains Keyword-Guard (who competes, who should own, from Search Console or a sitemap fallback) into Wordsmith (alternative titles, H1s and metas that de-conflict the loser without losing its traffic). One query, one owner, every time.",
 "nav_mid": "The workflow",
 "h1": "Two pages, one query. Decide the winner, <em>then</em> write for it.",
 "hsub": "One install chains two skills: <b>Keyword-Guard</b> audits the cannibalization \u2014 which pages compete for which query, who should own it, from Search Console or straight from the sitemap when you have no access \u2014 and <b>Wordsmith</b> writes the alternative titles, H1s and meta descriptions that de-conflict the non-owner. The audit is a blocker: nothing gets rewritten before the map is clean.",
 "stats": '''
          <span><b>1</b> owner per query</span>
          <span><b>2</b> audit paths</span>
          <span><b>2-3</b> options per conflict</span>
          <span><b>0</b> cross-canonicals</span>''',
 "ms": '''
          <p class="ms-label">design contract \u00b7 no live site audit was run in this pass</p>
          <p><span class="ms-before"><s>"both pages read well, so both may keep targeting the same phrase."</s></span></p>
          <ul class="ms-findings">
            <li><span class="sev high">blocker</span><span>The ownership audit must finish before any content change. Two pages sharing a primary keyword in title <b>and</b> H1 is guaranteed internal competition, whoever writes nicer copy.</span></li>
            <li><span class="sev med">fallback</span><span>No Search Console? The method falls back to sitemap plus a title/H1 grep, and the report <b>names it as a fallback</b> rather than passing off a guess as measured data.</span></li>
          </ul>
          <div class="ms-after">
            <p class="ms-label">the rule it enforces</p>
            <p class="hl">Assign ownership before touching a title. The homepage anchor is the #1 silent cannibal: raw authority makes it win and starves the dedicated page.</p>
          </div>
          <div class="ms-foot"><span>method documented, live run not performed</span><span>check the map, then the copy</span>''',
 "install_h2": "Copy one line. Settle the map, then settle the copy.",
 "cmd_note": 'The install line from the repo README. This skill is a chain: <b>keyword-guard</b> and <b>wordsmith</b> must be installed too \u2014 if either is missing it says so and stops.',
 "audit": '''
    <p class="kicker">the workflow</p>
    <h2>Audit, ownership, rewrite. In that order.</h2>
    <p class="lede">Phase one runs Keyword-Guard and blocks until the ownership map is signed off. Phase two hands each conflict to Wordsmith for alternatives that keep the loser's secondary traffic instead of gutting it.</p>
    '''
      + cats([
      ("Cannibalization audit", "blocker", "Every page ranking for a target query is listed, from GSC (page+query dimension) or the sitemap fallback.", ["GSC cross-page query map","sitemap + title/H1 grep","homepage anchor flagged","mixed-language pairs checked","one owner assigned per query"], False),
      ("De-optimization plan", "per loser", "Non-owners lose the competing primary keyword and gain a distinct long-tail modifier, plus links toward the owner.", ["strip primary keyword","self-referencing canonicals kept","internal links point to the owner","merge only when pages truly duplicate"], False),
      ("Alternatives", "2-3 each", "Wordsmith rewrites title, H1 and meta per conflict; hreflang sets for mixed-language sites are drafted with reciprocity checked.", ["owner keeps the primary phrase","loser gets a long-tail modifier","A points to B and B back to A","copy-paste ready"], False),
      ("Outside its boundary", "2 siblings", "Technical crawl, index and performance diagnosis is the <span class=\"mono\" style=\"color:var(--paper)\">seo-audit</span> skill's job; pages generated at scale belong to programmatic-seo. This skill settles who wins which query and rewrites accordingly. It does not touch your CMS \u2014 it hands back copy and a map.", ["no crawl diagnosis","no page generation","no direct site edits"], True),
    ]),
 "principles": '''
    <p class="kicker">ground rules</p>
    <h2>What it refuses to do.</h2>
    '''
      + pr([
      ("One query, one owner", "The page with the most clicks and impressions, the closest semantic match, or the designated pillar owns the query. Proposals without an owner assignment are not proposals, they are a second cannibal."),
      ("No cross-canonicals as a shortcut", "Canonicaling one competing page to another hides the fight instead of settling it \u2014 it suppresses the non-canonical page. Ownership first; canonicals stay self-referencing unless pages genuinely merge."),
      ("Say which path was taken", "GSC-measured and sitemap-inferred findings are labelled differently. A fallback audit is honest about being a fallback, because its blind spots are the traffic you cannot see."),
    ]),
 "cta": '''
  <div class="wrap">
    <h2>Exactly one page wins each query \u2014 then the copy follows.</h2>
    <p>Free, open, and every rewrite traces back to an ownership decision.</p>
    <a class="big-btn" href="#install">Install keyword-resolver</a>
    <a class="big-btn alt" href="https://github.com/arm-pz/keyword-resolver" target="_blank" rel="noopener">Read the source</a>
  </div>
''',
 "footer": '''
    <span>keyword-resolver — an open agent skill · <a href="../">all skills</a></span>
    <span><a href="https://github.com/arm-pz/keyword-resolver" target="_blank" rel="noopener">github.com/arm-pz/keyword-resolver</a></span>
  ''',
 "noscript": nos("keyword-resolver", "Requires the <span class=\"mono\">keyword-guard</span> and <span class=\"mono\">wordsmith</span> skills; the chain names and stops on a missing dependency."),
 "cmds_js": install_js("keyword-resolver", "Requires the keyword-guard and wordsmith skills installed alongside."),
})

SKILLS.append({
 "name": "seo-polish",
 "title": "seo-polish — Full SEO Audit, Then the Optimized Rewrite",
 "desc": "An open agent skill that diagnoses technical and on-page SEO with Seo-Audit, then generates optimized titles, meta descriptions, headings and content fixes with Wordsmith. Evidence first, prose second.",
 "ogdesc": "An open agent skill that chains Seo-Audit (crawlability, indexation, Core Web Vitals, titles, metas, headings, content gaps, internal linking) into Wordsmith (optimized alternatives for every High and Medium finding, priority-ranked). One pass gets you the diagnosis and the paste-ready fix \u2014 and says which checks were inconclusive because a source was unreadable.",
 "nav_mid": "The workflow",
 "h1": "The audit says what's broken. <em>Then write the fix.</em>",
 "hsub": "One install chains two skills: <b>Seo-Audit</b> works the priority order \u2014 crawlability and indexation, technical foundations, on-page optimization, content quality, authority \u2014 and <b>Wordsmith</b> turns every High and Medium finding into optimized alternatives: titles, meta descriptions, headings, internal-link anchors. Report plus rewrite in one pass, and every finding carries its evidence and impact rating.",
 "stats": '''
          <span><b>5</b> audit layers</span>
          <span><b>2-3</b> options per finding</span>
          <span><b>1</b> prioritized plan</span>
          <span><b>0</b> rankings promised</span>''',
 "ms": '''
          <p class="ms-label">design contract \u00b7 a full pass needs GSC or PageSpeed data; missing sources are named, not guessed</p>
          <p><span class="ms-before"><s>"fetched the page, saw no schema \u2014 must be missing schema."</s></span></p>
          <ul class="ms-findings">
            <li><span class="sev ok">honest</span><span>The audit records its own blind spot: static fetches strip <span class="mono">&lt;script&gt;</span>, so JS-injected JSON-LD is invisible to them. \u201cNo schema found\u201d is never reported from a static fetch alone \u2014 a rendering check decides.</span></li>
            <li><span class="sev med">scope</span><span>Findings without access to Search Console or Core Web Vitals data come back <b>inconclusive</b>, listed as what was not verified, instead of a confident zero.</span></li>
          </ul>
          <div class="ms-after">
            <p class="ms-label">the rule it enforces</p>
            <p class="hl">Diagnosis and rewrite, but only over what was actually measured. Unreadable is inconclusive, never counted as empty.</p>
          </div>
          <div class="ms-foot"><span>method documented, live site run not part of this pass</span><span>name the tool each finding came from</span>''',
 "install_h2": "Copy one line. Diagnose the site, then write the fixes.",
 "cmd_note": 'The install line from the repo README. This skill is a chain: <b>seo-audit</b> and <b>wordsmith</b> must be installed too \u2014 if either is missing it says so and stops.',
 "audit": '''
    <p class="kicker">the workflow</p>
    <h2>Five layers audited. Every finding gets a fix drafted.</h2>
    <p class="lede">Each finding is recorded as issue, impact, evidence, fix and priority. Anything High or Medium crosses to Wordsmith, which writes optimized alternatives for the exact element that failed.</p>
    '''
      + cats([
      ("Technical", "1-2", "Crawl and index first \u2014 robots, sitemap, canonicals, redirects \u2014 then speed, Core Web Vitals, mobile and HTTPS.", ["noindex and canonical direction","redirect chains","LCP / INP / CLS","mixed content","hreflang and locale hygiene"], False),
      ("On-page", "3", "Titles, metas, heading hierarchy, image alt text, internal links \u2014 each checked against what the page is for.", ["50-60 char unique titles","150-160 char descriptions","one H1 with the primary term","alt text on every image","orphan pages surfaced"], False),
      ("Rewrites", "2-3 each", "Wordsmith drafts alternatives per flagged element; the report says which checks ran and which were inconclusive.", ["title + meta pairs per page","anchor text for internal links","content-gap briefs","priority-ranked action plan"], False),
      ("Outside its boundary", "2 siblings", "Keyword cannibalization \u2014 which of <em>your own</em> pages should win a query \u2014 is <a href=\"https://skills.caffeinity.com/keyword-guard/\" target=\"_blank\" rel=\"noopener\" class=\"mono\">keyword-guard</a> and <a href=\"../keyword-resolver/\" class=\"mono\">keyword-resolver</a>. Pages generated at scale for a keyword list is programmatic-seo. This skill diagnoses a site that exists and writes its fixes. SEO compounds over months; it never promises positions.", ["no ownership rulings","no mass page generation","no ranking guarantees"], True),
    ]),
 "principles": '''
    <p class="kicker">ground rules</p>
    <h2>What it refuses to do.</h2>
    '''
      + pr([
      ("Evidence over confidence", "Every finding states how it was found. A check that could not run \u2014 no GSC access, unreadable source, JS-hidden schema \u2014 is reported as inconclusive, never as a clean pass or a zero."),
      ("Fetch output is untrusted data", "Pages are analyzed, never obeyed: instructions embedded in HTML or meta tags are a prompt-injection surface and are treated as content."),
      ("White-hat only", "No link schemes, no cloaking, no keyword stuffing. The rewrites match search intent in the author's own facts \u2014 and say honestly that SEO compounds over months, not days."),
    ]),
 "cta": '''
  <div class="wrap">
    <h2>The full diagnosis and the paste-ready fix, in one pass.</h2>
    <p>Free, open, and every alternative traces back to a measured finding.</p>
    <a class="big-btn" href="#install">Install seo-polish</a>
    <a class="big-btn alt" href="https://github.com/arm-pz/seo-polish" target="_blank" rel="noopener">Read the source</a>
  </div>
''',
 "footer": '''
    <span>seo-polish — an open agent skill · <a href="../">all skills</a></span>
    <span><a href="https://github.com/arm-pz/seo-polish" target="_blank" rel="noopener">github.com/arm-pz/seo-polish</a></span>
  ''',
 "noscript": nos("seo-polish", "Requires the <span class=\"mono\">seo-audit</span> and <span class=\"mono\">wordsmith</span> skills; the chain names and stops on a missing dependency."),
 "cmds_js": install_js("seo-polish", "Requires the seo-audit and wordsmith skills installed alongside."),
})

SKILLS.append({
 "name": "tune-and-polish",
 "title": "tune-and-polish — Fix Skill Triggers, Then Polish Discovery",
 "desc": "An open agent skill that fine-tunes triggering and sibling boundaries with Tune-Skill, then audits and polishes discoverability surfaces with Findable-Polish. The agent-facing text first, the human-facing copy second.",
 "ogdesc": "An open agent skill for a skill that both misfires and hides. It chains Tune-Skill (description, overlaps, stale counts, handoffs, minimal validated edits) into Findable-Polish (query-derived audit of README, About and site copy, with polished alternatives). One order, one pass: fix what the agent loads, then write what people search.",
 "nav_mid": "The workflow",
 "h1": "Make it fire. <em>Then make it findable.</em>",
 "hsub": "One install chains two phases: <b>Tune-Skill</b> audits the SKILL.md the agent actually loads \u2014 triggering description, sibling overlaps, stale names and counts, broken handoffs \u2014 and makes minimal edits validated by <span class=\"mono\" style=\"font-size:15px\">check_skill.py</span>. Then <b>Findable-Polish</b> audits the human-facing surfaces against real queries and polishes the README, About text and site copy. The file gets fixed first because the listing is written from the final description.",
 "stats": '''
          <span><b>2</b> chained phases</span>
          <span><b>16</b> validator checks</span>
          <span><b>0</b> FAILs to pass</span>
          <span><b>5-10</b> target queries</span>''',
 "ms": '''
          <p class="ms-label">order contract \u00b7 both halves documented; tune-skill's own validator ran on its repo 2026-10-19</p>
          <p><span class="ms-before"><s>"fix the description and the README in one breath \u2014 they're the same text."</s></span></p>
          <ul class="ms-findings">
            <li><span class="sev high">order</span><span>Tuning edits the <span class="mono">SKILL.md</span> description that carries the triggering; polish writes listing copy <b>from the final description</b>. Polish first and you re-audit prose you were about to change \u2014 twice the work, contradictory copy.</span></li>
            <li><span class="sev ok">gate</span><span>Phase one is not done until <span class="mono">check_skill.py</span> reports no FAIL. A tuned skill that fails shape validation is not tuned; the chain refuses to polish on top of it.</span></li>
            <li><span class="sev med">chain</span><span>Four skills must be installed (tune-skill, findable-polish, findable, wordsmith). A missing one is named and the run stops \u2014 no half-workflow with silently skipped phases.</span></li>
          </ul>
          <div class="ms-after">
            <p class="ms-label">the rule it enforces</p>
            <p class="hl">Triggering text and listing text are two jobs for two audiences. Same story, run in that order.</p>
          </div>
          <div class="ms-foot"><span>validator proven on tune-skill itself</span><span>end-to-end runs recorded per skill</span>''',
 "install_h2": "Copy one line. Tune what fires, then polish what's found.",
 "cmd_note": 'The install line from the repo README. The chain needs <b>tune-skill</b>, <b>findable-polish</b>, <b>findable</b> and <b>wordsmith</b>; a missing dependency is named and the run stops.',
 "audit": '''
    <p class="kicker">the workflow</p>
    <h2>Two phases, one gate between them.</h2>
    <p class="lede">Phase one is tune-skill's eight-step audit and edit loop, gated on the validator. Only a passing skill enters phase two, the findable-polish query audit and copy alternatives. The final report names what changed, what was polished, and what was never seen.</p>
    '''
      + cats([
      ("Tune", "phase 1", "Read the real SKILL.md and references, check overlaps with siblings, settle boundaries, make the smallest evidenced edit.", ["description and trigger check","sibling overlap resolution","stale names and counts","handoff contracts","check_skill.py: no FAILs"], False),
      ("Polish", "phase 2", "Run the discoverability audit on README, About and site copy; write alternatives from real queries.", ["5-10 target queries","2-3 options per gap","About text and topics drafted","sibling cross-links added"], False),
      ("Handover", "1 report", "Changes per skill with a one-line reason, the polished copy, and an honest note on which checks ran.", ["what changed and why","what was only drafted","commands for the user to run","never a silent push"], False),
      ("Outside its boundary", "2 siblings", "A brand-new skill is <a href=\"../draft-skill/\" class=\"mono\">draft-skill</a> territory, or the full pipeline in <a href=\"../skill-launch/\" class=\"mono\">skill-launch</a>. Nothing to tune, just better listing copy? Run <a href=\"../findable-polish/\" class=\"mono\">findable-polish</a> alone. This chain exists for the both-at-once case.", ["no authoring from scratch","no publishing"], True),
    ]),
 "principles": '''
    <p class="kicker">ground rules</p>
    <h2>What it refuses to do.</h2>
    '''
      + pr([
      ("Read the file, not the listing", "Every claim about a skill comes from its SKILL.md or references \u2014 READMEs and listings drift. An edit to prose that contradicts the file is the bug this order prevents."),
      ("The validator decides done", "\u201cLooks tighter\u201d is not a pass. Phase one ends when check_skill.py exits clean, and the report says which test cases were run versus only written."),
      ("Minimal edits, author's voice", "Change what the audit found and nothing else. Honesty, safety and privacy rules never get weakened to make a description scan better."),
    ]),
 "cta": '''
  <div class="wrap">
    <h2>A skill that fires correctly and is easy to find.</h2>
    <p>Free, open, and every edit traces back to a quoted line or a measured query.</p>
    <a class="big-btn" href="#install">Install tune-and-polish</a>
    <a class="big-btn alt" href="https://github.com/arm-pz/tune-and-polish" target="_blank" rel="noopener">Read the source</a>
  </div>
''',
 "footer": '''
    <span>tune-and-polish — an open agent skill · <a href="../">all skills</a></span>
    <span><a href="https://github.com/arm-pz/tune-and-polish" target="_blank" rel="noopener">github.com/arm-pz/tune-and-polish</a></span>
  ''',
 "noscript": nos("tune-and-polish", "Requires <span class=\"mono\">tune-skill</span>, <span class=\"mono\">findable-polish</span>, <span class=\"mono\">findable</span> and <span class=\"mono\">wordsmith</span>."),
 "cmds_js": install_js("tune-and-polish", "Requires tune-skill and findable-polish (with findable and wordsmith) installed alongside."),
})

SKILLS.append({
 "name": "skill-launch",
 "title": "skill-launch — Draft, Validate and Publish a Skill End to End",
 "desc": "An open agent skill that takes a skill idea through the full pipeline: draft-skill writes it, tune-skill makes the description fire and validates it, findable-polish audits and polishes the discovery surfaces. One session, three gated phases.",
 "ogdesc": "An open agent skill that turns \u201cI want a skill that does X\u201d into a validated, discoverable folder: Draft-Skill confirms intent and writes the structure, Tune-Skill gates it through check_skill.py with zero FAILs, Findable-Polish polishes README, About and site copy against real queries. Publishing commands are handed over, never run behind your back. Proven on six chain skills in one day.",
 "nav_mid": "The pipeline",
 "h1": "An idea in, a launched skill out \u2014 <em>three gates deep</em>.",
 "hsub": "One install runs three skills in order: <b>Draft-Skill</b> confirms intent, checks siblings and writes the SKILL.md; <b>Tune-Skill</b> makes the description fire, resolves overlaps and validates with <span class=\"mono\" style=\"font-size:15px\">check_skill.py</span>; <b>Findable-Polish</b> audits the discovery surfaces and polishes the copy. Each phase gates the next \u2014 nothing advances on \u201clooks fine\u201d, and no public change runs without your go-ahead.",
 "stats": '''
          <span><b>3</b> gated phases</span>
          <span><b>16</b> validator checks</span>
          <span><b>0</b> FAILs to advance</span>
          <span><b>6</b> skills launched</span>''',
 "ms": '''
          <p class="ms-label">the pipeline run for real \u00b7 six chain skills drafted, tuned and published 2026-10-19</p>
          <p><span class="ms-before"><s>"draft it, push it, write the description last."</s></span></p>
          <ul class="ms-findings">
            <li><span class="sev ok">proven</span><span>Six skills went the full loop in one day \u2014 draft, tune, publish \u2014 each landing with <span class="mono">SKILL.md</span>, README, MIT license and a v0.1.0 release on GitHub.</span></li>
            <li><span class="sev high">caught</span><span>The same run caught a shipped bug: a description whose YAML colon broke frontmatter parsing reached a repo before the validator gate tightened. A gate that runs beats a review that meant well.</span></li>
            <li><span class="sev med">handoff</span><span>Publication is a <b>handover, not a step it takes alone</b>: gh commands and releases are drafted and shown, then run only on explicit confirmation.</span></li>
          </ul>
          <div class="ms-after">
            <p class="ms-label">the rule it enforces</p>
            <p class="hl">A skill is launched when it fires, passes the validator, and says what people search for \u2014 in that order.</p>
          </div>
          <div class="ms-foot"><span>six repos, releases and indexes updated</span><span>public changes always need a go-ahead</span>''',
 "install_h2": "Copy one line. Idea in, launched skill out.",
 "cmd_note": 'The install line from the repo README. The pipeline needs <b>draft-skill</b>, <b>tune-skill</b> and <b>findable-polish</b> installed; a missing one is named and the run stops.',
 "audit": '''
    <p class="kicker">the pipeline</p>
    <h2>Three phases, two gates, one handover.</h2>
    <p class="lede">Each phase ends in an artifact the next one consumes: a drafted folder, a validated skill with zero FAILs, a polished set of discovery surfaces. The final report states which checks ran and which publication commands are waiting on you.</p>
    '''
      + cats([
      ("Draft", "phase 1", "Intent confirmed before anything is written; siblings checked so the new skill has one clear owner of its request.", ["purpose + trigger sketch","sibling overlap screen","scripts vs references decided","description written to trigger"], False),
      ("Validate", "gate 1", "Tune-Skill audits and edits, and the folder must pass check_skill.py with zero FAILs to move on.", ["16 checks, exit clean","overlap edits minimal","near-miss test cases written","no FAIL, no advance"], False),
      ("Polish + launch", "gate 2", "Findable-Polish derives the queries and polishes README, About and site copy; the launch kit hands over copy-paste commands.", ["5-10 target queries","About + topics drafted","install line verified","gh commands handed over"], False),
      ("Outside its boundary", "2 siblings", "An existing skill that needs work runs through <a href=\"../tune-and-polish/\" class=\"mono\">tune-and-polish</a>, not this pipeline. A prompt list rather than an idea is <span class=\"mono\">prompts-to-skill</span> territory. Nothing public changes without confirmation \u2014 that rule outlives every convenience.", ["no edits to existing skills","no unapproved publishing"], True),
    ]),
 "principles": '''
    <p class="kicker">ground rules</p>
    <h2>What it refuses to do.</h2>
    '''
      + pr([
      ("Confirm intent before writing", "A skill written from a misread idea is a repo you have to delete later. Phase one asks what it is for and who should never trigger it, then writes."),
      ("Gates, not vibes", "The validator decides when phase one is done. Descriptions are measured against the checklist, and a FAIL sends the skill back to tuning instead of forward to polish."),
      ("Public changes need a go-ahead", "Repos, releases and listing edits are drafted with exact commands and run only after confirmation. The pipeline prepares the launch; you pull the trigger."),
    ]),
 "cta": '''
  <div class="wrap">
    <h2>From idea to launched, with a gate between every phase.</h2>
    <p>Free, open, and every launch traces back to a validated file.</p>
    <a class="big-btn" href="#install">Install skill-launch</a>
    <a class="big-btn alt" href="https://github.com/arm-pz/skill-launch" target="_blank" rel="noopener">Read the source</a>
  </div>
''',
 "footer": '''
    <span>skill-launch — an open agent skill · <a href="../">all skills</a></span>
    <span><a href="https://github.com/arm-pz/skill-launch" target="_blank" rel="noopener">github.com/arm-pz/skill-launch</a></span>
  ''',
 "noscript": nos("skill-launch", "Requires <span class=\"mono\">draft-skill</span>, <span class=\"mono\">tune-skill</span> and <span class=\"mono\">findable-polish</span> (which needs <span class=\"mono\">findable</span> and <span class=\"mono\">wordsmith</span>)."),
 "cmds_js": install_js("skill-launch", "Requires draft-skill, tune-skill and findable-polish installed alongside."),
})

SKILLS.append({
 "name": "upstream-polish",
 "title": "upstream-polish — Find the Drift, Then Rewrite What's Stale",
 "desc": "An open agent skill that audits push state and listing drift with Upstream-Check, then generates polished fixes with Wordsmith. Fast-forward-only pushes; corrected descriptions, topics and README rows.",
 "ogdesc": "An open agent skill for the gap between your repos and your listings. It chains Upstream-Check (fetch-based verdicts per repo \u2014 push-ready, level, behind, diverged \u2014 plus a drift report comparing every published listing against repos that ship a SKILL.md, screened for credential-shaped lines) into Wordsmith, which rewrites the drifted descriptions, topics and README rows. Never force, never push a diverged repo, never count an unreadable source as empty.",
 "nav_mid": "The workflow",
 "h1": "You pushed. The listings still say last week. <em>Sync them.</em>",
 "hsub": "One install chains two skills: <b>Upstream-Check</b> fetches every clone and returns a verdict per repo \u2014 fast-forward-only pushes, screened for secrets \u2014 plus a drift report measuring each published listing against the ground truth of repos that actually ship a <span class=\"mono\">SKILL.md</span>. <b>Wordsmith</b> then writes the corrected descriptions, topics and README rows. Two failures, one pass: work that never left the machine, and numbers that quietly disagreed.",
 "stats": '''
          <span><b>7</b> verdicts</span>
          <span><b>1</b> secret screen</span>
          <span><b>0</b> forced pushes</span>
          <span><b>2-3</b> options per drift</span>''',
 "ms": '''
          <p class="ms-label">design contract \u00b7 the upstream-check run of 2026-10-19 reported push verdicts per repo</p>
          <p><span class="ms-before"><s>"everything's pushed, so the site must be current."</s></span></p>
          <ul class="ms-findings">
            <li><span class="sev high">truth</span><span>Ground truth is a <span class="mono">SKILL.md</span> in a repo. A description, a badge or a listing is <b>never</b> evidence a skill exists \u2014 and an unreadable source is reported inconclusive, never counted as empty.</span></li>
            <li><span class="sev ok">safe</span><span>Read-only by default: without <span class="mono">--push</span> nothing is written anywhere. Pushes are fast-forwards only, screened for credential-shaped lines; a diverged repo is explained before it is touched.</span></li>
            <li><span class="sev med">scope</span><span>Counts move while you read. If a fetch fails, the remote side may be stale rather than level \u2014 the report names what it did not verify.</span></li>
          </ul>
          <div class="ms-after">
            <p class="ms-label">the rule it enforces</p>
            <p class="hl">Push status is git arithmetic; listing truth is a count against repos. Read both, then rewrite only the drift.</p>
          </div>
          <div class="ms-foot"><span>verdict logic lives in upstream-check's tests</span><span>this chain hands over listings copy, not commits</span>''',
 "install_h2": "Copy one line. Audit the drift, then rewrite what moved.",
 "cmd_note": 'The install line from the repo README. The chain needs <b>upstream-check</b> and <b>wordsmith</b>; the audit half ships its own behavior tests, the polish half writes the fixes.',
 "audit": '''
    <p class="kicker">the workflow</p>
    <h2>Verdicts first. Copy second. Nothing forced.</h2>
    <p class="lede">Phase one fetches every clone in the root, classifies each repo, and \u2014 only with <span class="mono" style="font-size:15px">--push</span> and only after a secret screen \u2014 fast-forwards the clean ones. The drift register then compares every published surface against repos shipping a SKILL.md, and Wordsmith rewrites what disagreed.</p>
    '''
      + cats([
      ("Push audit", "7 verdicts", "push-ready, level, behind, diverged, no-upstream, no-remote, unreadable \u2014 each with a defined action.", ["read-only without --push","fast-forward only","credential-shaped lines block a push","diverged is explained, never touched"], False),
      ("Drift report", "vs ground truth", "Site index, homepage, marketplace manifest and READMEs measured against every owned repo that ships a SKILL.md.", ["absent listings named","phantom entries checked","both site indexes compared","offline means inconclusive"], False),
      ("Polished fixes", "2-3 each", "Wordsmith rewrites drifted descriptions, topics and README rows so every surface tells the same story as the repos.", ["one line per fix","numbers from the same run","handover kit for listings","boundary prose stays with tune-skill"], False),
      ("Outside its boundary", "2 siblings", "The verdict engine itself is <a href=\"https://github.com/arm-pz/upstream-check\" target=\"_blank\" rel=\"noopener\" class=\"mono\">upstream-check</a>; making a fresh repo discoverable at all is <a href=\"../findable/\" class=\"mono\">findable</a>. This chain runs when state and listings disagree after work exists. It does not commit loose work to make a number look tidy.", ["no force-push ever","no commits of other people's WIP"], True),
    ]),
 "principles": '''
    <p class="kicker">ground rules</p>
    <h2>What it refuses to do.</h2>
    '''
      + pr([
      ("Read before inferring", "git status compares against a remote-tracking ref nobody refreshed; it lies about \u201cup to date\u201d until something is fetched. Every verdict comes from a fetch, or is labelled possibly stale."),
      ("Unreadable is INCONCLUSIVE", "A failed fetch or an unparseable listing is reported as inconclusive \u2014 never counted as an empty one. A silent zero is how drift gets blessed."),
      ("A dirty tree is context, not a blocker", "Pushes send commits, so uncommitted files stay local and are named as such. Nobody's loose work gets committed to make an audit pass."),
    ]),
 "cta": '''
  <div class="wrap">
    <h2>Repos and listings, telling the same story again.</h2>
    <p>Free, open, and every fix traces back to a fetch or a counted listing.</p>
    <a class="big-btn" href="#install">Install upstream-polish</a>
    <a class="big-btn alt" href="https://github.com/arm-pz/upstream-polish" target="_blank" rel="noopener">Read the source</a>
  </div>
''',
 "footer": '''
    <span>upstream-polish — an open agent skill · <a href="../">all skills</a></span>
    <span><a href="https://github.com/arm-pz/upstream-polish" target="_blank" rel="noopener">github.com/arm-pz/upstream-polish</a></span>
  ''',
 "noscript": nos("upstream-polish", "Requires <span class=\"mono\">upstream-check</span> and <span class=\"mono\">wordsmith</span>."),
 "cmds_js": install_js("upstream-polish", "Requires upstream-check and wordsmith installed alongside."),
})

for c in SKILLS:
    build(c)
