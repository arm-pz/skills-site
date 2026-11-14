# Trigger cases for straight-prose

Written to the format in tune-skill's `references/test-cases.md`. Each case is judged from the `description` frontmatter only, as an agent choosing what to load would. Competing descriptions read from their SKILL.md files: `wordsmith`, `recruiter-lens`, `tune-skill`, `findable`. `applicant-kit` and `findable-polish` were not read.

Run: by hand on 2026-11-10, against the descriptions. No automated triggering loop was run. Each result is a routing judgement. The pass conditions describe behaviour that was not executed.

## Cases

| # | Message | Expected skill | Expected mode | Pass condition | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | "Take the AI slop out of this blog post." | straight-prose | edit | changes only sentences that carry a pattern | PASS ("remove AI slop") |
| 2 | "Does this sound like AI wrote it?" with a draft pasted | straight-prose | audit | lists patterns, changes nothing, gives no AI probability | PASS (quoted trigger) |
| 3 | "Here are my anti-slop writing rules. Apply them to what you write for me." | straight-prose | write | follows the pasted rules and these ones, and says where they conflict | PASS ("pastes anti-slop style rules to apply") |
| 4 | "My manager said my status update reads like ChatGPT. Fix it but keep it sounding like me." | straight-prose | edit | keeps the user's spelling and register | PASS ("why does this read like ChatGPT", voice) |
| 5 | "Write the launch post in my voice. No em dashes and none of that 'not just X but Y' stuff." | straight-prose | write | returns the post with no process commentary | PASS ("in my voice", em dashes and negative parallelisms named) |
| 6 | "Make this email warmer and a bit shorter." | wordsmith | n/a | straight-prose does not load | PASS ("Not for general editing such as tone changes, shortening") |
| 7 | "/wordsmith humanize" on a paragraph | wordsmith | n/a | straight-prose does not load | PASS (explicit command; the body's hand-off says the same) |
| 8 | "Make this essay undetectable by GPTZero." | none | n/a | straight-prose declines the detector job | PASS on the "Not for" clause. The message shares "AI" wording with the triggers, so a load followed by the stated refusal is also acceptable |
| 9 | "Rewrite my resume bullets so they don't sound AI-generated." | applicant-kit | n/a | straight-prose does not load | PASS on the "Not for" clause, with a caveat: `applicant-kit`'s description was not read |
| 10 | "Humanize this paragraph." with no command and no mention of AI | unclear | n/a | one skill loads | FAIL: `wordsmith` has a `humanize` command and its description claims "rewrite, edit, polish and improve text". A user who says "humanize" often means removing AI patterns. Both can load. `wordsmith`'s description does not name straight-prose, so the boundary holds from this side only |
| 11 | "Tighten my skill's description so it triggers." | tune-skill | n/a | straight-prose does not load | PASS |
| 12 | "Polish the README so the repo gets found." | findable | n/a | straight-prose does not load | PASS |

11 of 12 pass by review. Case 10 fails and needs a change in `wordsmith`, which this skill cannot make.

## Boundary pairs

| Message | Should trigger | Why |
| --- | --- | --- |
| "This reads like a chatbot wrote it, fix that" | straight-prose | the complaint is AI patterns |
| "Make this more formal" | wordsmith | a tone change with no complaint about AI patterns |
| "Which sentences here sound generated?" | straight-prose | audit of patterns |
| "Fact-check this article" | wordsmith | `factcheck` is its command |
| "Is my resume too obviously AI?" | recruiter-lens | job-search material is reviewed there |
| "Get this past Turnitin's AI check" | none | detector evasion is not offered |

Spans both: "clean the AI-speak out of this and then cut it to 200 words" starts with straight-prose for the pattern edit, then hands the text and the voice notes to wordsmith for the `shorten`.

## Original prompt

The skill was built from one long style prompt, not from a set of requests, so there are no original prompts to replay as triggers. Case 3 stands in for a user pasting that prompt.

## Not verified

- No case was run in a live session.
- The edit and audit behaviour in `evals/evals.json` has not been executed against the skill by a fresh agent.
- The collision in case 10 is open until `wordsmith` names this skill in its "Not for" clause or drops `humanize`.
