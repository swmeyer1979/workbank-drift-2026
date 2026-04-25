# Cap-rule audit (full 844-task run)

Rubric v2 added an ordered cap hierarchy. Raters return a `cap_rule_fired` field. This report audits how often each rule fires and how load-bearing it is for the headline drift.

## Rule-fire frequency per rater

| rater | none | physical | interpersonal | safety_critical | novel_research |
|---|---:|---:|---:|---:|---:|
| opus_4_7 | 591 | 26 | 78 | 127 | 22 |
| kimi_k2_6 | 628 | 16 | 75 | 99 | 26 |
| gpt_5_5 | 596 | 24 | 46 | 145 | 33 |

## Cap-binding tasks

- ≥1 rater fired any cap: **360/844 tasks (43%)**
- All 3 raters fired some cap: **119/844 tasks (14%)**

## Distribution of `capability_2026_median` by cap status

| group | n | mean cap | share ≥3 |
|---|---:|---:|---:|
| cap-rule fired (≥1 rater) | 360 | 3.12 | 94% |
| no cap rule fired | 484 | 4.07 | 100% |

## Headline-impact: zone counts with/without cap-rule binding

| zone | cap-fired | no cap |
|---|---:|---:|
| Green Light | 174 | 285 |
| Red Light | 166 | 199 |
| R&D Opportunity | 12 | 0 |
| Low Priority | 8 | 0 |

## Caveat

- A true leave-one-out (re-score with each cap rule disabled) requires a new full ensemble run with a modified rubric. Estimated cost: ~$30 per cap-rule ablation × 4 rules = ~$120. Deferred. Current report is *observational* — relating cap-fire status to final scores, not counterfactually re-scoring.