# Wordsmith

A portable Agent Skill for drafting, rewriting, editing, proofreading, and polishing text.

Wordsmith helps AI coding agents produce clearer, more concise, natural, and publication-ready writing while preserving the author's meaning and voice.

## Use when

Use Wordsmith when you need to:

- draft content from an idea or brief;
- rewrite or polish existing text;
- proofread grammar and spelling;
- improve clarity, flow, and concision;
- change tone or reading level;
- create headlines, titles, emails, or website copy;
- critique structure and audience fit;
- review accessibility and readability;
- prepare content for publication.

## Installation

Copy the following directory into the skills directory supported by your AI agent:

```text
skills/wordsmith/
```

Depending on the agent platform, that may be one of:

```text
.claude/skills/wordsmith/
.agents/skills/wordsmith/
.cursor/skills/wordsmith/
.qoder/skills/wordsmith/
```

Consult the documentation for the agent platform you use to determine the correct location.

Or install via the Skills CLI:

```bash
npx skills add arm-pz/wordsmith --skill wordsmith
```

For Claude Code specifically:

```bash
npx skills add arm-pz/wordsmith --skill wordsmith --agent claude-code
```

## Usage

Invoke with a command:

```text
/wordsmith draft
/wordsmith rewrite
/wordsmith critique
/wordsmith audit
/wordsmith tighten
/wordsmith polish
/wordsmith final
```

Or describe the task naturally:

```text
Rewrite this paragraph for a professional website while preserving its meaning.
Make this email warmer without sounding corporate.
Check this article for unsupported claims and unclear sections.
```

### Command quick reference

| Command | When to use |
|---------|-------------|
| `brief` | Turn an idea into a structured writing brief |
| `outline` | Plan structure before drafting |
| `draft` | Write new content from notes or prompt |
| `edit` | Fix grammar/spelling, preserve voice |
| `rewrite` | Substantial transformation |
| `critique` | Diagnose problems without auto-rewriting |
| `audit` | Systematic quality review with scorecard |
| `tighten` | Reduce length, remove filler |
| `simplify` | Make technical text accessible |
| `tone` | Change emotional/professional register |
| `polish` | Final refinement pass |
| `final` | Pre-publication check + placeholder flagging |

## Commands

### Build

- `brief` — turn an idea into a clear writing brief;
- `outline` — create a logical structure;
- `draft` — write new content;
- `develop` — expand notes into a complete piece;
- `compose` — combine fragments into one coherent draft;
- `continue` — continue an existing piece;
- `finish` — complete an unfinished draft.

### Evaluate

- `critique` — explain what works and what needs improvement;
- `audit` — perform a structured quality review;
- `diagnose` — identify the main reason a piece is weak;
- `clarity` — identify confusing or ambiguous language;
- `voice` — analyze voice and style;
- `structure` — review organization and flow;
- `audience` — check audience fit;
- `accuracy` — identify claims that require verification;
- `readability` — review complexity and accessibility.

### Refine

- `edit` — improve grammar and wording while preserving the voice;
- `rewrite` — substantially transform the writing;
- `polish` — perform a final refinement pass;
- `tighten` — make the writing shorter and more direct;
- `simplify` — make difficult writing easier to understand;
- `smooth` — improve flow and transitions;
- `strengthen` — improve weak arguments or wording;
- `proof` — correct mechanical errors.

### Adapt

- `tone` — change the emotional or professional tone;
- `formalize` — make writing more formal;
- `humanize` — make writing warmer and less mechanical;
- `shorten` — reduce the length;
- `expand` — add useful detail;
- `summarize` — produce a concise version;
- `headline` — create titles and headings;
- `subject` — create email subject lines;
- `repurpose` — adapt content for multiple channels;
- `translate` — translate while preserving intent;
- `localize` — adapt language and cultural references.

### Prepare

- `factcheck` — identify factual claims that need verification;
- `evidence` — identify where sources or citations are needed;
- `inclusive` — review language for unnecessary exclusion or stereotyping;
- `accessibility` — improve readability and accessibility;
- `consistency` — check names, terms, dates, and formatting;
- `compare` — compare two versions;
- `diff` — explain what changed;
- `final` — prepare content for publication or sending;
- `release` — return only the final copy.

## Common aliases

These aliases map to the main commands:

| Alias | Main command |
|---|---|
| `proofread` | `proof` |
| `grammar` | `proof` |
| `review` | `critique` |
| `feedback` | `critique` |
| `check` | `audit` |
| `quality-check` | `audit` |
| `condense` | `tighten` |
| `make-clear` | `clarity` |
| `make-simple` | `simplify` |
| `ready-to-send` | `final` |
| `publication` | `final` |

Note: `shorten` is a command in its own right (hit a length target), not an alias for `tighten` (remove filler).

## Typical workflows

### Write something new

```text
/wordsmith brief
/wordsmith outline
/wordsmith draft
/wordsmith critique
/wordsmith polish
```

### Improve existing writing

```text
/wordsmith critique
/wordsmith rewrite
/wordsmith polish
```

### Prepare an email

```text
/wordsmith rewrite
/wordsmith tone warm and direct
/wordsmith tighten
/wordsmith final
```

### Prepare important content

```text
/wordsmith audit
/wordsmith factcheck
/wordsmith accessibility
/wordsmith final
```

## Design principles

Wordsmith should:

- preserve the author's intended meaning;
- preserve important facts, names, numbers, and quotations;
- avoid inventing facts, sources, statistics, or experiences;
- match the requested audience and tone;
- use clear and direct language;
- preserve the author's voice unless asked to change it;
- explain substantial changes;
- identify uncertainty instead of pretending to know;
- return the requested writing before lengthy commentary.

Wordsmith should not:

- silently change dates, numbers, names, or commitments;
- make unsupported claims sound certain;
- replace a personal voice with generic corporate language;
- rewrite everything when the user only requested proofreading;
- claim that content is factually correct without verification;
- add fake citations or sources.

## Development

The source repository is a Copier template.

Generate a new project:

```bash
copier copy https://github.com/arm-pz/agent-skill-template.git wordsmith
```

Update a previously generated project:

```bash
cd wordsmith
copier update
```

Copier stores the original answers in:

```text
.copier-answers.yml
```

## License

MIT — see [LICENSE](LICENSE).
