# cold-email-ops: real-world run, 2026-11-13

**Verdict: PARTIAL** (7/10). The run hand-computed 275 inboxes and 93 domains for 60k sends/month (10/inbox/day, 3 inboxes/domain, 22 days) with a correct per-client split, a 1% domain reply floor and shadow-ban and automation checks, but its burn-replacement plan is not sized to the 6 burned domains and it gets today's date wrong.

Target: a 60,000-sends-a-month cold-email plan across 4 clients. Run headless on the CLI default model in a clean project with only this skill installed (6 turns, 4 tool calls, 29 s, $0.2).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
I run outbound for 4 B2B clients. Next month I want to send 60,000 cold emails total (clients get 25k, 15k, 12k, 8k). Last month: 41 domains, 120 inboxes, reply rate fell from 2.1% to 1.2% across the board, and 6 domains got burned. Plan the infrastructure for next month and tell me what to watch.
```

## Rubric

- Computes inboxes and domains needed from the send target with stated per-inbox/day and per-domain assumptions, and the arithmetic is right
- Sets per-domain reply-rate floors and what happens when a domain falls below
- Gives a burn-replacement cadence sized to last month's 6 burned domains (warm spares)
- Includes a shadow-ban or inbox-placement test and an automation error budget
- Splits capacity per client and states which assumptions are its own rather than facts

## Hard checks


## Met

- Inboxes and domains computed from the target with stated assumptions (10 sends/inbox/day, 3 inboxes/domain, 22 days). The arithmetic checks out: 2,727/day, 273 inboxes and 91 domains pooled, 275 and 93 summed per client.
- Per-client capacity table (25k: 114 inboxes/38 domains, 15k: 69/23, 12k: 55/19, 8k: 37/13) with a reasoned choice to keep domains separate per client at a cost of about 2 extra domains.
- Per-domain reply floor of 1%, with an explicit action when a domain falls below it (schedule for replacement, not just monitor), plus a two-week declining-slope watch rule.
- Shadow-ban check: 0% bounce with zero replies triggers one copy rewrite, then retirement after 48 hours if nothing changes.
- Automation reliability math (0.8^4 ≈ 41% vs 0.99^4 ≈ 96%, about 2,400 misses at 60k) with an owner, check and blast-radius per step. This works as an error budget.
- Marks its own assumptions (warm-up of 2–4 weeks is 'my rule of thumb', hand-computed math, skill defaults) and flags unknown inputs, rather than presenting them as facts.

## Missed

- The burn-replacement cadence is not sized to last month's 6 burned domains out of 41 (about 15%). It uses a generic '6–9 month burn' rate to get 30–46 inboxes/month and says only 'keep spare inboxes warming', with no stated warm-spare pool size or per-week domain cadence.
- No true inbox-placement or seed test (e.g. seed inboxes or placement tooling per provider). The shadow-ban check is only a symptom heuristic on reply data.
- The automation error budget is a reliability illustration with no numeric tolerance, such as an acceptable failure rate or max emails per failure.
- States 'Today is Nov 13' when the date is Nov 14. It also speculates that overloaded inboxes caused the 6 burns, which is hedged but unsupported without last month's send count.
- Says the script could not be run because Bash was denied, so the numbers were never machine-verified, though they are correct.

## Defects to fix in the skill

- The skill gives no guidance on sizing a warm-spare pool from the observed burn count (burned domains ÷ active domains) or on a weekly replacement cadence derived from it, so the agent fell back on a generic burn-lifetime rule.
- The skill does not require a concrete inbox-placement or seed-test procedure, only symptom-based shadow-ban detection.
- The skill does not give a numeric automation error budget (e.g. max tolerated failed sends per step), only a compounding-reliability illustration.
- The skill relies on a script that failed to run here, with no instruction to show the formulas or a fallback computation, so the output is less verifiable.

## What it did

1. `Skill: cold-email-ops`
1. `Bash: cd /tmp/run-cold-email-ops-lh3odlh6/project/.claude/skills/cold-email-ops && python scripts/cold_email_math.py capacity --monthly 60000; for m in 25000 15000 12`
1. `Read: /tmp/run-cold-email-ops-lh3odlh6/project/.claude/skills/cold-email-ops/references/report-format.md`
1. `Read: /tmp/run-cold-email-ops-lh3odlh6/project/.claude/skills/cold-email-ops/scripts/cold_email_math.py`

## Final output

**Verdict:** you need about 275 inboxes and 93 domains to send 60k a month. You have 120 inboxes and 41 domains, and 6 of those domains are burned. Order the new domains this week, because warm-up has to finish before December volume.

I couldn't run `cold_email_math.py` because Bash was denied here. I did the arithmetic by hand with the script's formulas, so re-run it if you want to confirm. Skill defaults are 10 sends per inbox per day, 3 inboxes per domain and 22 sending days.

## 1. Inputs and assumptions

| Input | Value | Source |
|---|---|---|
| Monthly target | 60,000 (25k / 15k / 12k / 8k) | You |
| Current infrastructure | 41 domains, 120 inboxes, 6 domains burned | You |
| Reply rate last month | 2.1% → 1.2%, all clients | You |
| Sends last month | **Unknown** | Missing |
| Reply and bounce split by domain, receiving provider, client | **Unknown** | Missing |
| Sending tool, data provider, who answers replies | **Unknown** | Missing |

## 2. Capacity (hand-computed)

| Client | Sends/day | Inboxes | Domains |
|---|---|---|---|
| A (25k) | 1,136 | 114 | 38 |
| B (15k) | 682 | 69 | 23 |
| C (12k) | 546 | 55 | 19 |
| D (8k) | 364 | 37 | 13 |
| **Total** | **2,727** | **275** | **93** |

- **Pooled versus separate:** pooling all clients would need 273 inboxes and 91 domains. I'd keep domains separate per client, so a burned domain or a spam complaint never crosses clients. That costs about 2 extra domains.
- **Gap against what you have:** 275 − 120 = about 155 more inboxes. Once the 6 burned domains are retired you have about 35 healthy domains, so you need about 58 new ones.
- **Replacement:** at a 6–9 month burn, expect 30–46 inboxes a month (7–10 a week). Replace weekly, and on the same day when one fails.
- **Last month's load:** 120 inboxes at 10 a day is about 26,400 sends a month. If you sent much more than that, you were running inboxes hot. That is the most likely cause of the 6 burns and the reply decline. I can't confirm it without last month's send count.

## 3. Timeline

Today is Nov 13, so there are about 2–3 weeks before the month starts.

1. **Now:** buy about 58 domains and create the inboxes. SPF, DKIM and DMARC must be clean before any sending.
2. **Now to late November:** warm the new inboxes. I'm assuming 2–4 weeks, which is my rule of thumb and not from the skill.
3. **Month start:** only warmed inboxes carry the full 10 a day. If some aren't ready, the temptation is to push 15–20 a day through the healthy ones. Don't. The skill allows up to 20 only while an inbox is healthy, and that is how you get the next burn.
4. **Weeks 1–2:** ramp volume rather than going to 60k at once. Put about 70% of the load on your best-performing proven inboxes. Keep spare inboxes warming for swaps.

## 4. What to watch

- **Domain floor:** at least 1% reply rate, counting automated replies. A domain below that gets scheduled for replacement. Don't just keep monitoring it.
- **Two-week slope:** two consecutive weeks of falling reply rate puts a domain on watch, even if it is still above 1%. One bad week is not a burn.
- **Daily per inbox:** alert on a reply dip or a bounce rise, and swap the same day. Low per-inbox volume means one dead inbox barely moves the total.
- **Shadow-ban test:** if an inbox shows 0% bounce, healthy placement and zero replies, rewrite the copy once. If nothing changes in 48 hours, retire the inboxes.
- **Provider split:** report sends, replies and reply rate for Google, Outlook and other separately. The source benchmark saw about 6.5× more replies from Google recipients than Microsoft ones. That is directional, so check it in your own data. If a client's list is Microsoft-heavy, match the sending provider to it.
- **List quality:** watch bounce rate and valid-contact rate by client. If the reply drop was across all four clients, check whether they share a data provider.
- **Prospects-to-lead (contacts sent ÷ leads):** under 500 is strong. Use it alongside reply rate, and track each client against your four-client average. A client below average is an early warning, not a verdict.
- **Reply speed:** source benchmark says answering within 5 minutes lifts positive-reply-to-meeting from about 20% to about 80%. Name who is on replies and their hours before you scale.

## 5. Automation checks

Reliability multiplies across steps. Four steps at 0.8 each leave about 41% end to end, and four at 0.99 each leave about 96%. At 60k sends, 4% is about 2,400 misses. For each automated step (list pull, enrichment, copy merge, send), write down an owner, a check, and how many emails a failure reaches before you'd notice.

Before any bulk load, sample 10 rows per list and approve them. Keep volume quotas as reporting only.

## 6. Verdicts so far

| Area | Verdict | Evidence |
|---|---|---|
| Capacity | **FAIL** | 120 of 275 inboxes needed, with 6 domains burned |
| Deliverability | **WATCH** | Reply rate fell 2.1% → 1.2% and domains burned. Cause not yet shown. |
| List | **INCONCLUSIVE** | No bounce or valid-contact data |
| Replies | **INCONCLUSIVE** | No owner or response-time data |
| Measurement | **INCONCLUSIVE** | No provider or per-domain split |

The 1.2% average is only slightly above the 1% floor, so many individual domains are probably under it now.

## What I need from you

Please send these exports. I can turn the INCONCLUSIVE rows into real verdicts and trace the cause of last month's drop:

1. Last month's sends, replies and bounces by domain, by receiving provider, and by client.
2. Your sending tool and data provider.
3. Who handles replies and in what hours.
4. Whether the 6 burned domains shared a client, a list or a provider.

Suggested next check: Nov 27, to confirm warm-up status and that the replacement batch is ordered. The owner for each item is whoever runs deliverability for you, and I can't name them yet.
