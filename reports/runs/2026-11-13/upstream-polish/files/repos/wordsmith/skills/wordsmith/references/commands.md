# Wordsmith command reference

This file defines the behavior of the supported commands.

## `brief`

Turn a vague idea into a structured writing brief.

Return:

```text
Purpose:
Audience:
Core message:
Desired action:
Format:
Tone:
Length:
Required points:
Things to avoid:
Open questions:
```

Do not draft the full piece unless the user asks for it.

## `outline`

Create the structure for a piece of writing.

Consider:

- the reader's likely questions;
- logical order;
- the most important point;
- supporting evidence;
- transitions;
- the desired conclusion or call to action.

For longer pieces, include headings and bullets explaining the purpose of each section.

## `draft`

Create new content from the user's brief, notes, or request.

Before drafting, infer:

- who is speaking;
- who is reading;
- what the reader should understand;
- what the reader should do next;
- what tone is appropriate;
- what length and format are required.

Do not invent product capabilities, statistics, events, or personal experiences. If essential information is missing, either use clearly marked placeholders like [launch date] or ask one focused question — do both only if the gap blocks the entire draft.

## `develop`

Expand a short idea or rough paragraph into a complete piece.

Add useful explanation, examples, transitions, and structure. Do not add unsupported factual claims.

## `compose`

Combine notes, fragments, or multiple sections into a coherent draft.

Remove duplication and resolve inconsistent wording where possible. Flag contradictions instead of silently choosing between conflicting facts.

## `continue`

Continue an existing piece while matching its voice, tense, perspective, structure, and level of detail.

Do not introduce a new theme unless requested.

## `finish`

Complete an unfinished draft.

Preserve the existing direction and voice. If the intended ending is unclear, provide the most reasonable ending and mention the assumption.

## `critique`

Evaluate the writing without automatically rewriting the entire piece.

Return:

```text
Overall assessment:
What works:
Main weaknesses:
Highest-value improvements:
Example revision:
```

Prioritize major problems over minor stylistic preferences.

## `audit`

Perform a systematic review.

Return a scorecard followed by findings. Use the format in `references/output-formats.md`.

Assess:

- purpose clarity;
- audience fit;
- structure;
- opening strength;
- specificity;
- evidence;
- tone;
- voice consistency;
- readability;
- concision;
- accessibility;
- factual risk;
- call to action.

Use this finding format:

```text
Severity: P0/P1/P2/P3
Location:
Problem:
Why it matters:
Recommended action:
```

Severity levels:

- `P0` — serious issue that makes the writing misleading, unusable, or unsafe;
- `P1` — important issue that significantly weakens the piece;
- `P2` — worthwhile improvement;
- `P3` — minor refinement.

## `diagnose`

Identify the main reason the writing is not working.

Focus on root causes such as:

- unclear purpose;
- wrong audience;
- weak structure;
- buried main point;
- insufficient evidence;
- excessive abstraction;
- inconsistent tone;
- unnecessary length.

Return the top three causes and the highest-value fix for each.

## `clarity`

Find and improve:

- vague wording;
- ambiguous references;
- unexplained jargon;
- indirect phrasing;
- overloaded sentences;
- unclear pronouns;
- missing context;
- confusing transitions.

Show revised examples where helpful.

## `voice`

Analyze or preserve the author's voice.

Consider:

- sentence length;
- vocabulary;
- formality;
- warmth;
- confidence;
- rhythm;
- use of humor;
- use of contractions;
- degree of specificity;
- emotional distance.

Do not replace an individual voice with generic professional language.

## `structure`

Review or improve organization.

Check:

- whether the main point appears early enough;
- whether sections are in a logical order;
- whether headings describe the content;
- whether paragraphs have clear purposes;
- whether transitions are sufficient;
- whether the ending follows naturally.

For significant structural changes, provide the proposed outline before the full rewrite.

## `audience`

Check whether the writing fits its intended audience.

Consider:

- knowledge level;
- expectations;
- vocabulary;
- cultural context;
- likely objections;
- desired action;
- amount of explanation required.

If the audience is not specified, infer it from context and state the assumption briefly.

## `accuracy`

Identify statements that may require verification.

Separate:

- factual claims;
- opinions;
- interpretations;
- predictions;
- generalizations;
- marketing claims.

Do not claim that a statement is true merely because it sounds plausible.

## `readability`

Review:

- sentence length;
- paragraph length;
- jargon;
- abstraction;
- passive constructions;
- unnecessary nominalizations;
- headings;
- lists;
- accessibility.

Recommend changes that improve comprehension without making the content simplistic.

## `edit`

Make careful improvements while preserving the author's meaning and voice.

Correct:

- grammar;
- spelling;
- punctuation;
- awkward phrasing;
- inconsistent terminology;
- obvious repetition.

Do not restructure the entire piece unless necessary.

## `rewrite`

Make a substantial improvement to the writing.

You may change:

- sentence order;
- paragraph order;
- structure;
- transitions;
- wording;
- level of detail;
- tone.

Preserve factual content and intended meaning.

Use the output format in `references/output-formats.md`.

## `polish`

Perform a final refinement pass.

Check:

- rhythm;
- repetition;
- transitions;
- word economy;
- sentence variety;
- punctuation;
- consistency;
- opening and closing strength.

Do not make major changes unless a serious problem remains.

## `tighten`

Make the writing more concise.

Remove:

- repetition;
- empty introductions;
- redundant qualifiers;
- unnecessary adverbs;
- inflated phrases;
- obvious statements;
- duplicate examples.

Preserve nuance, evidence, qualifications, and the central argument.

If a percentage or word count is supplied, aim for it.

## `simplify`

Make the writing easier to understand.

Use:

- plain language;
- shorter sentences;
- concrete examples;
- explained technical terms;
- direct relationships between ideas.

Do not remove necessary technical accuracy or nuance.

## `smooth`

Improve rhythm, flow, and transitions without substantially changing the content.

Focus on:

- sentence rhythm;
- repeated sentence openings;
- abrupt transitions;
- awkward paragraph endings;
- excessive fragments;
- uneven levels of formality.

## `strengthen`

Improve weak arguments or wording.

Look for:

- unsupported conclusions;
- vague benefits;
- weak verbs;
- missing evidence;
- unclear stakes;
- unaddressed objections;
- buried recommendations.

Do not make claims stronger than the evidence allows.

## `proof`

Correct mechanical errors only.

Fix:

- spelling;
- grammar;
- punctuation;
- capitalization;
- obvious formatting errors.

Do not substantially alter the voice, structure, or argument.

## `tone`

Change the tone according to the user's request.

Useful tone dimensions include:

- formal or casual;
- warm or distant;
- confident or cautious;
- serious or playful;
- direct or diplomatic;
- concise or conversational;
- authoritative or collaborative.

Translate labels into concrete writing decisions. Do not rely on vague adjectives alone.

For example, "warm" means: use direct human language, acknowledge the reader's situation, avoid excessive enthusiasm, use contractions where appropriate, do not use forced jokes.

## `formalize`

Make the writing more professional and formal without making it stiff or inflated.

Avoid:

- unnecessary jargon;
- excessive passive voice;
- corporate filler;
- exaggerated claims;
- artificial politeness.

## `humanize`

Make the writing warmer and more natural.

Prefer:

- direct language;
- concrete examples;
- natural transitions;
- appropriate contractions;
- acknowledgment of the reader.

Avoid forced enthusiasm, fake intimacy, and unnecessary jokes.

## `shorten`

Reduce the length while preserving the core message.

State what was removed or combined if the reduction is substantial.

## `expand`

Add useful detail, explanation, examples, or context.

Do not add unsupported facts. If examples are invented, make that clear.

## `summarize`

Produce a shorter version that preserves the most important information.

Match the requested format:

- one sentence;
- executive summary;
- bullet list;
- abstract;
- plain-language summary.

## `headline`

Create titles, headings, or article headlines.

Prioritize:

- accuracy;
- specificity;
- clarity;
- relevance to the audience;
- an appropriate level of interest.

Avoid clickbait and claims unsupported by the content.

## `subject`

Create email subject lines.

Consider:

- clarity;
- length;
- urgency;
- relevance;
- whether the important information appears early;
- whether the subject sounds misleading or spam-like.

## `repurpose`

Adapt one piece into multiple formats.

Adjust each version for its channel rather than merely shortening the original.

Possible outputs include:

- email;
- website copy;
- social post;
- internal announcement;
- presentation script;
- FAQ;
- executive summary.

## `translate`

Translate while preserving:

- meaning;
- tone;
- formatting;
- placeholders;
- product names;
- code;
- Markdown structure.

Ask or infer whether formal or informal language is appropriate.

## `localize`

Adapt writing for a region or culture.

Consider:

- spelling;
- punctuation;
- date formats;
- currency;
- units;
- idioms;
- references;
- formality.

Do not treat localization as legal or regulatory advice.

## `factcheck`

List claims that should be verified before publication.

For each claim, return:

```text
Claim:
Why verification may be needed:
Recommended verification:
```

Do not invent a verification result or citation.

## `evidence`

Identify where evidence, examples, sources, or citations would strengthen the writing.

Distinguish between:

- claims that require evidence;
- claims that are common knowledge;
- opinions;
- personal experiences;
- predictions;
- interpretations.

## `inclusive`

Review the text for unnecessary exclusion, stereotyping, demeaning language, or assumptions about the reader.

Explain meaningful changes. Do not make automatic substitutions without considering context.

## `accessibility`

Improve accessibility by reviewing:

- sentence complexity;
- jargon;
- headings;
- list structure;
- descriptive links;
- unexplained abbreviations;
- excessive reliance on tone or implication;
- long blocks of text.

## `consistency`

Check:

- names;
- terminology;
- capitalization;
- dates;
- numbers;
- units;
- headings;
- punctuation;
- tense;
- perspective;
- formatting.

## `compare`

Compare two versions.

Return:

```text
Recommendation:
Main advantages:
Main disadvantages:
Audience considerations:
Important differences:
```

Do not select a winner without explaining the criteria.

## `diff`

Explain what changed between an original and revised version.

Group changes into:

- meaning;
- structure;
- tone;
- clarity;
- concision;
- grammar;
- formatting.

## `final`

Prepare content for publication or sending.

Check:

- grammar and spelling;
- names and titles;
- dates and times;
- numbers and units;
- links;
- placeholders;
- contradictions;
- unsupported claims;
- tone;
- call to action;
- accidental draft language.

Return:

```text
Final copy:
[prepared content]

Needs confirmation:
- [unresolved issue, if any]
```

## `release`

Return only the final copy.

Do not include editorial commentary unless an unresolved issue makes publication unsafe or misleading.
