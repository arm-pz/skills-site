# Example: Wordsmith in action

## User request

```text
/wordsmith audit

Our new AI platform is the most advanced solution on the market. It uses cutting-edge machine learning to help businesses optimize their workflows. Early adopters have seen incredible results. The system integrates seamlessly with existing tools and requires minimal training. We believe this will revolutionize how teams work together. Contact us today for a demo.
```

## Expected output

```text
Scorecard:
- Purpose clarity: 3/5
- Audience fit: 2/5
- Structure: 3/5
- Opening strength: 2/5
- Specificity: 1/5
- Evidence: 1/5
- Tone: 2/5
- Voice consistency: 3/5
- Readability: 4/5
- Concision: 4/5
- Accessibility: 4/5
- Factual risk: 1/5
- Call to action: 3/5

Findings:

Severity: P1
Location: Sentence 1 ("most advanced solution on the market")
Problem: Unsubstantiated superlative with no comparison criteria.
Why it matters: Triggers immediate skepticism; readers expect proof or specific differentiators.
Recommended action: Replace with concrete capability (e.g., "reduces workflow setup time by 60% compared to manual tools").

Severity: P1
Location: Sentence 3 ("incredible results")
Problem: Vague, unverifiable claim.
Why it matters: Reads as marketing fluff; provides no basis for evaluation.
Recommended action: Specify metric and timeframe (e.g., "beta users averaged 23% ROI increase within 6 weeks").

Severity: P2
Location: Sentence 4 ("integrates seamlessly", "minimal training")
Problem: Absolute language without qualification.
Why it matters: Sets unrealistic expectations; may not hold for all integration scenarios.
Recommended action: Add scope or conditions (e.g., "integrates with Slack, Teams, and Jira; most teams are productive within 2 hours").

Severity: P2
Location: Sentence 5 ("revolutionize how teams work together")
Problem: Overstated impact claim.
Why it matters: Dilutes credibility when paired with vague evidence.
Recommended action: Ground in specific outcome (e.g., "eliminates 4 hours of weekly coordination meetings per team").
```

## Why this is a good response

- Returns scorecard before findings (highest-priority info first)
- Uses consistent severity levels (P1 for credibility-breaking claims, P2 for overstatement)
- Each finding has location, problem, why it matters, and actionable recommendation
- Doesn't rewrite the entire piece — focuses on diagnosis
- Flags unsupported claims without inventing verification results
- Maintains professional tone while being direct about weaknesses
