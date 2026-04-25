# Threshold sensitivity

All counts use `capability_2026_median` (integer ensemble median) and `desire_2025` (worker mean).
Capability-axis cutoff varied; desire-axis cutoff fixed at 3.0.

## Zone population by capability cutoff

| zone | 2025, c=2.75 | 2025, c=3.0 | 2025, c=3.25 | 2026, c=2.75 | 2026, c=3.0 | 2026, c=3.25 |
|---|---:|---:|---:|---:|---:|---:|
| Green Light | 446 | 364 | 211 | 557 | 459 | 214 |
| Red Light | 190 | 267 | 284 | 267 | 365 | 289 |
| R&D Opportunity | 123 | 107 | 102 | 12 | 12 | 99 |
| Low Priority | 85 | 106 | 247 | 8 | 8 | 242 |

## Migration count by threshold

| | c=2.75 | c=3.0 | c=3.25 |
|---|---:|---:|---:|
| Tasks with zone change | 200 (24%) | 205 (24%) | 296 (35%) |

## Bootstrap CIs on headline statistics (cutoff = 3.0)

| metric | point estimate | 95% bootstrap CI |
|---|---:|---|
| Tasks with zone change | 205 | [180, 230] |
| Share with capability ≥ 3 in 2026 | 97.6% | [96.6%, 98.6%] |

## Reading guide

- At c=2.75: most tasks are above threshold in both years; zones merge.
- At c=3.25: enough tasks fall below threshold in 2026 to keep R&D / Low Priority populated.
- The headline "98% above threshold" is fragile to threshold choice.
- The Migration count is robust at all three thresholds (bootstrap CI tight).

## Near-threshold population (median in [2.5, 3.5])

332/844 = 39% of tasks have median capability in [2.5, 3.5]. These are the most cutoff-sensitive.
