# Wordsmith test prompts

These prompts can be used to evaluate the generated skill. Each test includes realistic input and expected behavior.

## Draft

### Input

```text
/wordsmith draft
Write a friendly welcome email for a new customer who has just created an account.
```

### Expected behavior

- creates a complete email with subject line, greeting, body, and sign-off;
- uses a friendly and clear tone;
- includes 2–3 useful next steps (not generic "explore our platform");
- does not invent product features or capabilities;
- uses placeholders like [Product Name] where specifics are unknown.

---

## Edit

### Input

```text
/wordsmith edit
Fix the grammar and punctuation in the following text, but preserve my voice:

"I wanted to reach out because we have made some changes that I think will be really useful for you and your team."
```

### Expected behavior

- makes only necessary corrections (e.g., contraction for conversational tone);
- does not substantially rewrite the sentence structure;
- preserves the author's casual, personal tone;
- returns edited text before any explanation.

---

## Rewrite

### Input

```text
/wordsmith rewrite
Rewrite this announcement so that it sounds confident, direct, and helpful without sounding aggressive:

"We wanted to let you know that there might be some updates coming soon to the platform. We're not entirely sure when they'll be ready, but we think they could potentially help with workflow efficiency. Please feel free to reach out if you have any questions about this."
```

### Expected behavior

- removes hedging language ("might", "not entirely sure", "could potentially");
- adds concrete timeframe or flags it as needing confirmation;
- preserves the core facts (updates coming, workflow focus);
- improves clarity and directness without adding invented details;
- includes brief notes explaining significant changes.

---

## Tighten

### Input

```text
/wordsmith tighten
Shorten the following text by approximately 30 percent while preserving the argument, evidence, and qualifications:

"Our team has been working really hard over the past several months to develop a brand-new feature that we think will be incredibly useful for you and your entire organization. We have spent a lot of time researching what our customers need most, and we believe that this new capability addresses one of the most common pain points that teams like yours face on a daily basis. The feature allows you to automatically sync data between multiple platforms without having to manually export and import files, which saves a tremendous amount of time and reduces the risk of errors significantly. We are very excited about this launch and hope that you will find it as valuable as we do."
```

### Expected behavior

- removes repetition, filler phrases, and redundant qualifiers;
- preserves the main claim (new feature, research-backed, sync capability);
- preserves evidence (research, time savings, error reduction);
- aims for ~30% word count reduction (original ~95 words → target ~67);
- states actual reduction achieved if significantly different from target.

---

## Simplify

### Input

```text
/wordsmith simplify
Rewrite this technical explanation for a general audience with no technical background:

"The API leverages OAuth 2.0 bearer token authentication with JWT payloads containing scoped claims that enforce RBAC policies at the middleware layer, ensuring granular access control without compromising throughput latency."
```

### Expected behavior

- explains OAuth, JWT, RBAC in plain language or replaces with conceptual equivalents;
- uses short sentences and concrete analogies;
- retains technical accuracy (authentication + authorization + performance);
- does not make the explanation childish or condescending;
- states assumptions about reader knowledge level.

---

## Tone

### Input

```text
/wordsmith tone warm
Make this customer message warm, calm, and professional. Avoid sounding corporate or overly enthusiastic:

"Per our records, your subscription renewal is due on 2026-10-15. Please ensure payment is processed prior to this date to avoid service interruption. Contact billing@company.com for assistance."
```

### Expected behavior

- uses direct address and contractions naturally;
- acknowledges the reader's situation without excessive enthusiasm;
- preserves all factual information (date, action needed, contact);
- avoids corporate filler and forced warmth;
- translates "warm" into concrete writing decisions (not just adjective swaps).

---

## Critique

### Input

```text
/wordsmith critique
Review this article and identify the three most important weaknesses:

"Our new product is revolutionary. It changes everything about how teams collaborate. Early users love it. The interface is intuitive and the features are powerful. We believe this will transform the industry. Competitors should be worried."
```

### Expected behavior

- prioritizes major issues over minor stylistic preferences;
- explains why each weakness matters to the reader;
- points to specific sentences or phrases;
- provides example revision for at least one finding;
- does not rewrite the entire article automatically.

---

## Audit

### Input

```text
/wordsmith audit
Audit this proposal for clarity, structure, repetition, unsupported claims, audience fit, and tone:

"Most companies struggle with their marketing strategy. Our solution is the best in the industry. We have helped thousands of businesses grow faster than ever before. The platform uses advanced AI to optimize campaigns. You should switch to us immediately because competitors are already doing it. Our pricing is competitive and flexible. Many clients have seen amazing results within weeks."
```

### Expected behavior

- provides scorecard with all 13 dimensions rated /5;
- identifies findings with P0/P1/P2/P3 severity levels;
- each finding includes location, problem, why it matters, recommended action;
- distinguishes problems from recommendations;
- flags unsupported claims ("most", "best", "thousands", "amazing") without inventing verification.

---

## Voice

### Input

```text
/wordsmith voice
Analyze these three writing samples and produce a practical style guide for the author:

Sample 1: "Hey team — quick update on the Q3 roadmap. We're pushing the analytics dashboard to October because the data pipeline needs more testing. Better to ship it right than fast."

Sample 2: "Just wrapped up the client demo. They loved the new export feature but flagged the loading time as a concern. Let's prioritize performance optimization next sprint."

Sample 3: "Heads up: the compliance review came back clean. No blockers for the November release. Great work everyone — this was a team effort."
```

### Expected behavior

- identifies recurring patterns across all three samples;
- discusses sentence length, vocabulary, tone, rhythm, and formality;
- produces usable style rules (not vague labels like "professional");
- includes "avoid" list with specific examples;
- captures the author's peer-to-peer communication style.

---

## Factcheck

### Input

```text
/wordsmith factcheck
List every factual claim in this draft that should be verified before publication:

"Launched in 2024, our platform serves over 10,000 teams across 50 countries. Users report 3x faster project completion and 40% cost reduction. Featured in TechCrunch and Forbes as 'the future of remote work.' Backed by $50M in Series B funding led by Sequoia Capital."
```

### Expected behavior

- separates factual claims from opinions/interpretations;
- identifies statistics, dates, counts, and specific assertions;
- does not pretend to have verified anything;
- does not invent sources or verification results;
- lists each claim with why verification may be needed.

---

## Final

### Input

```text
/wordsmith final
Prepare this announcement for publication:

"Hi [Customer Name], we're excited to announce our new backup feature! It launched on [DATE] and helps you protect your data. Check it out at [LINK]. Let us know what you think! Best, The Team"
```

### Expected behavior

- fixes mechanics and improves flow;
- checks names, numbers, dates, and placeholders;
- returns clean final copy first (before commentary);
- lists unresolved issues separately under "Needs confirmation";
- flags all placeholders ([Customer Name], [DATE], [LINK]) and missing brand name.
