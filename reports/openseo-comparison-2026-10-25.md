# OpenSEO's skills next to ours: what to adopt

Read on 2026-10-25 from `every-app/open-seo` at `236761a` (MIT, Ben Senescu): the 12 public skills
in `plugins/openseo/skills/`, with `seo-audit`, `ai-visibility-audit`, `ai-prompt-research` and
`keyword-clustering` read in full. Compared with `seo-crawl`, `keyword-guard` and `findable` at their
current HEADs. Nothing below copies their text; each proposal is an idea to write in our own words.

## How the two families differ

| | OpenSEO | Ours |
| --- | --- | --- |
| Data | Paid search data through its MCP server: volumes, rankings, backlinks, SERPs, AI answers, Search Console | None from outside. `seo-crawl` measures the site itself; `keyword-guard` reads Search Console when the user has it |
| Without the service | Every skill stops ("ask the user to connect it") | Every skill runs, with no API keys |
| Evidence | Live checks with query, country, date and listing count behind every ranking claim | Deterministic crawl JSON with stable finding IDs, INCONCLUSIVE checks and a fix lifecycle (`fixed-verified`) |
| Deciding what to do | Built in: shortlist, choose one to three, size the benefit, review, report | Not ours: `seo-crawl` hands diagnosis to the third-party `seo-audit` (coreyhaines31) |
| Memory | Shared project context: business overview, key pages, a research log reused for 30 days | Each run starts fresh |

They complement each other: OpenSEO supplies the data our skills declare out of scope, and ours
work offline, with no account and no spend. That is why the site now pairs them on `seo-crawl`,
`keyword-guard` and the "Grow organic search traffic" workflow, labelled third-party.

## Proposals, most useful first

1. **Give Brew 4 a deciding step of its own** (`keyword-guard`, or a new skill). Today the chain goes
   crawl, ownership, rewrite, and nothing of ours picks the few changes that matter. Adopt OpenSEO's
   discipline: write a shortlist of five to ten candidates drawn from at least three kinds (an
   underperforming page, missing demand, a winner to protect, an access defect, the visitor's next
   step); choose one to three; and end every other row in a "What else we checked" table with a real
   reason. It fits `keyword-guard`'s existing Phase 3 blocker and would let Brew 4 stop depending on a
   third-party audit skill for the decision.
2. **Size benefit honestly in `keyword-guard`'s plans.** Search volume is not visits; a page that
   already ranks already gets part of the volume; label any position-one scenario hypothetical; never
   invent a conversion rate. Short rules, and they stop the most common overclaim in SEO plans.
3. **One convention for ranking claims** in every skill that makes them (`keyword-guard` today, any
   OpenSEO-fed step later): the exact query, country, language and date, and positions written as
   "#10 (page 1)" or "not in the first 20 results". A failed lookup is unknown, never "not ranking".
   This is the same idea as `seo-crawl`'s INCONCLUSIVE, applied to rankings.
4. **Add an AI-crawler rule to `seo-crawl`.** It already reads `robots.txt`. Report, at info level,
   which AI crawlers are blocked and what each rule controls: blocking `OAI-SearchBot` keeps a site out
   of ChatGPT search answers, while blocking `GPTBot` or `Google-Extended` affects model training, not
   live answers. Deterministic, cheap, and nothing in our family checks it today. (skillsmith.tech
   allows everything, so it passes.)
5. **Name the reviewer step.** OpenSEO's audit hands its draft and shortlist to a second reviewer who
   must argue for the strongest rejected option. We already have the tools for this in `crash-test`
   and `do-better`; Brew 4 could name one as the review step before the report.
6. **Consider shared context, carefully.** A small per-project file (what the business does, its key
   pages, a dated log of past findings) that our SEO skills read first and append to would stop each
   run re-asking the same questions. Worth a design note before code: it adds state to skills that are
   currently stateless, and stateless is part of why they are easy to trust.

## What not to adopt

- **Their skill names.** OpenSEO ships its own `seo-audit`, `keyword-research` and
  `keyword-clustering`. `seo-crawl` already hands off to a different `seo-audit` (coreyhaines31). A user
  with both installed gets two skills claiming one trigger. Keep our names distinct, and say which
  `seo-audit` a handoff means.
- **A hard dependency on a paid service.** Pairing is right; requiring it would end "0 API keys".
- **Their report HTML.** Their `seo-report` skill builds one house-styled HTML page. Our skills return
  markdown and JSON that other skills consume; keep it that way.

## Doing this

Proposals 1 to 5 are edits to `arm-pz/keyword-guard` and `arm-pz/seo-crawl` (and the Brew 4 entry in
`caffeinity-routing`). They go through Brew 10 · Descale like any other change: tune-skill, then a
release, with each repo's own tests. None of them needs OpenSEO to run.
