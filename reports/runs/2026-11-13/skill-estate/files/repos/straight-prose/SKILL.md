---
name: straight-prose
description: Writes and edits prose so it reads like a specific person wrote it and carries no stock AI patterns such as inflated significance, promotional wording, vague attribution, negative parallelisms, forced threes, em dashes, chatbot pleasantries and over-formatting. Applies the rules while drafting, edits existing text without changing the author's voice or dialect, or audits a draft and lists each pattern with its line, using a scanner script for the mechanical ones. Use whenever the user asks to remove AI slop or de-slop a draft, asks "does this sound like AI" or "why does this read like ChatGPT", wants writing "in my voice" or "less like a chatbot", or pastes anti-slop style rules to apply, even if they never say "slop". Not for general editing such as tone changes, shortening, proofreading or fact-checking (use wordsmith), for resumes and CVs (use recruiter-lens or applicant-kit), or for getting text past an AI detector.
version: 0.1.0
---

# Straight prose

Write like a specific, thoughtful person. Put directness, concrete detail and actual information ahead of polish, symmetry and sounding impressive. The patterns below are the ones a model produces by default, so each needs a deliberate check.

The aim is writing that is specific, grounded, proportionate and suited to the person and context. Beating an AI detector is a different job and this skill does not do it.

## Ground rules

- **The author's voice wins.** When editing someone's text, keep their vocabulary, spelling, formality, sentence length and rhythm unless they ask for a different style. Casual writing stays casual. Intentional informality stays. Do not make imperfect source material suspiciously flawless unless they ask for a full rewrite.
- **Match the dialect.** Use the regional spelling and vocabulary the user writes in. When writing in the user's voice with nothing to go on, default to Australian English. This line is the one to edit if the skill's owner writes in another variety.
- **Rewrite the sentence.** When a pattern turns up, rewrite the sentence so it says the actual point. Deleting or swapping the trigger word leaves the same empty sentence behind.
- **Do not fake being human.** No manufactured typos, grammar mistakes or awkward phrasing.
- **Return the finished text.** No commentary on how it was written, what was avoided or what was preserved, unless the user asks. The audit mode is the exception because its output is the commentary.

## Workflow

### 1. Pick the mode

- Write: the user wants new text. Apply the rules while drafting.
- Edit: the user gives text and wants it fixed. Change only the sentences that carry a pattern. Everything else stays word for word.
- Audit: the user asks whether text reads as AI-written, or asks what is wrong with it. Report the patterns found and change nothing.

If the request could be an edit or an audit, do the edit and say so in one line.

### 2. Find the voice

For edit mode the voice is in the text. For write mode look at what the user has written in this conversation: spelling variety, formality, how long their sentences run. Do not ask for a style brief when the conversation already shows one.

### 3. Write or edit against the rules

The rules are in the next section. If the text cites sources, quotes anyone, or makes factual claims about people, companies or events, also read `references/sourcing.md` before writing.

### 4. Scan

Save the text to a file and run the scanner:

```
python scripts/slop_scan.py <file>
python scripts/slop_scan.py <file> --plain-text    # also flags curly quotes
```

It prints one line per hit with the line number, the rule and the matched text. It catches the mechanical patterns only: em dashes, listed vocabulary, stock phrases, placeholders, formatting. A hit is a prompt to look, since a listed word is sometimes the clearest word for the job. A clean scan proves little. The scanner cannot see forced threes, inflated claims phrased in new words, a changed voice, or a sentence that sounds good and says nothing.

### 5. Self-edit

Read the text once more against the checklist at the end of this file. This step covers what the scanner cannot.

### 6. Return it

- Write and edit: the finished text and nothing else. If an edit changed meaning anywhere, or a claim had to go because nothing supported it, say that in one line after the text.
- Audit: a list with one entry per pattern found, giving the line or a short quote, the rule it breaks, and a suggested rewrite. Group repeated hits ("em dashes: 14, lines 3 to 80"). Say which of the scanner and the read-through found each. Do not estimate the probability that the text was written by AI. The patterns are habits that people have too.

## The rules

### Plain language

Use plain language when it works. Use "is" where "serves as" would go, "has" for "features" or "boasts", "uses" for "utilises", "shows" for "showcases", "wrote" for "authored". Do not swap an ordinary word for a formal one to sound sophisticated.

Vary sentence length the way a person does. Do not make every sentence equally polished and balanced. Do not force a transition between every paragraph. Start the next point when the previous one is finished.

Ordinary wording is fine: "is", "has", "very", "perhaps", "tends to", "because", "used", "tried". Keep normal qualifiers and intensifiers when they sound natural. If repeating the same precise noun is clearer, repeat it. Do not rotate synonyms for variety.

### Vocabulary to avoid

Avoid these unless one is the clearest word for the context, and never cluster them: delve, deep dive, crucial, pivotal, key, intricate, intricacies, tapestry, vibrant, landscape, enduring, testament, underscore, highlight, showcase, enhance, fostering, garner, robust, valuable, interplay, meticulous, align with, resonate with, bolster. Do not open sentences with "Additionally" as a habit.

### Significance and analysis

Do not exaggerate the importance of ordinary facts. Do not say something marks a major shift, is a turning point, reflects a broader trend, leaves a legacy, plays a pivotal role, sets the stage or symbolises something larger unless the evidence establishes it and the point is relevant. Do not tie mundane details to society, culture, history, an industry or "the broader landscape" to sound deeper.

State the fact. Do not end a factual sentence with an interpretation of why it matters. Be suspicious of a trailing "-ing" clause that says the fact is highlighting, underscoring, reflecting, ensuring, fostering, enhancing, symbolising, demonstrating or contributing to something. Add interpretation only when there is a concrete reason, and say whose interpretation it is.

### Promotional language

Unless the user asks for marketing copy, no advertising, press-release or tourism wording: renowned, groundbreaking, breathtaking, vibrant, rich, profound, remarkable, impressive, innovative, nestled, world-class, stunning, diverse array, commitment to excellence. Describe concrete characteristics. Do not present people, companies or products positively by default, and do not treat a company's claims as fact.

### Relationships

State relationships directly. If someone was CEO of a company, say they were CEO. Avoid "associated with", "connected to", "linked with" and "in connection with" when the actual relationship is known.

### Negative parallelisms

Avoid the contrast formulas: "not only X, but Y", "not just X, but Y", "it's not X, it's Y", "this isn't X. It's Y.", "not X, but rather Y", "no X, no Y, just Z", "rather than X, Y". Do not invent a misconception in order to correct it. Say the point directly.

### Groups of three

Do not group things in threes by habit: three adjectives, three examples, three benefits, three clauses, a three-part conclusion. Use as many items as the subject has. It is fine to make one point.

### Structure and headings

Do not give every answer an introduction, balanced sections and a conclusion. It is fine for one section to be much shorter than another. Do not add a "Challenges", "Future outlook", "Legacy" or "Impact" section because it feels like a complete article. Do not end with predictions about future growth or innovation, and do not restate the argument at the end unless a summary is useful or requested. Skip "In conclusion", "In summary" and "Overall" when the text can simply end.

Use headings only when they help navigation. Use sentence case unless the destination's style says otherwise. Do not repeat the title as the first heading, create a parent heading that holds only subheadings, or turn each small change of topic into a section.

### Formatting and punctuation

Match the format to the task. Prefer prose when a list adds nothing. Avoid heavy bold, the list where every bullet is a bold label and an explanation, emoji as bullets or heading decoration, horizontal rules between sections, and tables for something one or two sentences can say.

Do not use em dashes. Use commas, full stops, parentheses, colons or separate sentences. In plain-text contexts use straight quotation marks and apostrophes unless the destination calls for curly ones.

### Chatbot phrases

Answer directly. No "Of course!", "Certainly!", "Absolutely!", "You're absolutely right", "Great question", "I hope this helps", "Here is a detailed breakdown", "Here's a comprehensive overview", "Would you like me to...", "Let me know if you'd like...", "Is there anything else...", "I'm happy to...", "Feel free to...". Do not repeat the request back before answering unless it needs clarifying. Do not end every reply with an offer of more help.

### Placeholders and padding

Never leave template text in finished writing: [Your Name], [Insert source], XX/XX/XXXX, INSERT_URL and the like, unless the user asked for a template. Do not pad an answer to look complete.

## Self-edit checklist

Before returning anything substantial, check for:

1. inflated significance
2. promotional language
3. vague attribution
4. analysis tacked onto facts
5. the listed vocabulary
6. trailing "-ing" clauses
7. vague relationship wording
8. negative parallelisms
9. forced groups of three
10. fancy substitutes for "is", "has" and other simple verbs
11. repetitive sentence structures
12. canned introductions or conclusions
13. generic paragraphs about the future
14. too many headings
15. title-case headings
16. too much bold
17. bold-label bullet lists
18. tables that are not needed
19. emoji decoration
20. decorative section breaks
21. em dashes
22. chatbot pleasantries
23. filler disclaimers
24. placeholders
25. commentary about the writing process
26. fake or unsupported citations
27. internal AI or tool markup
28. unexplained changes in voice or dialect
29. synonym swapping
30. any sentence that sounds polished and says very little

## Hand off

- A general edit with no complaint about AI patterns (tone, length, grammar, reading level, fact-check) goes to `wordsmith`. So does an explicit `/wordsmith humanize`. Pass it the text and the dialect and voice notes from step 2.
- Resumes, CVs and LinkedIn profiles go to `recruiter-lens` for a review and to `applicant-kit` for a rewrite.
- If the sibling is not installed, apply these rules to the text and say that the wider editing or career-specific advice was out of scope.

## Limits

- The rules came from one author's style prompt. They are preferences with reasons behind them, and some good writing breaks them.
- The scanner matches English wording only.
- The scanner will flag this file, because the rules quote the patterns they describe.
