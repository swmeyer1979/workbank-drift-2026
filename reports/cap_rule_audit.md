# Cap-rule audit (primary 844-task rerun)

Rubric v2 added an ordered cap hierarchy. Raters return a `cap_rule_fired` field. This report audits how often each rule fires and how load-bearing it is for the headline drift.

## Rule-fire frequency per rater

| rater | none | physical | interpersonal | safety_critical | novel_research |
|---|---:|---:|---:|---:|---:|
| codex_gpt_5_5_xhigh | 604 | 27 | 43 | 143 | 27 |
| kimi_k2_6 | 621 | 18 | 71 | 113 | 21 |
| gpt_5_5 | 608 | 24 | 45 | 135 | 32 |

## Cap-binding tasks

- >=1 rater fired any cap: **339/844 tasks (40%)**
- All 3 raters fired some cap: **133/844 tasks (16%)**

## Distribution of `capability_2026_median` by cap status

| group | n | mean cap | share >=3 |
|---|---:|---:|---:|
| cap-rule fired (>=1 rater) | 339 | 3.12 | 93% |
| no cap rule fired | 505 | 3.99 | 100% |

## Headline-impact: zone counts with/without cap-rule binding

| zone | cap-fired | no cap |
|---|---:|---:|
| Green Light | 163 | 292 |
| Red Light | 153 | 213 |
| R&D Opportunity | 16 | 0 |
| Low Priority | 7 | 0 |

## Caveat

A true leave-one-out re-score with each cap rule disabled requires a new full ensemble run with a modified rubric. Current report is observational: it relates cap-fire status to final scores, then flags where the surviving below-threshold tasks sit.
