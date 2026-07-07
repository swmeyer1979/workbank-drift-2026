# Threshold sensitivity

Counts use `capability_2026_median` and `desire_2025`. For sensitivity only, the cutoff is moved on both axes so the table reflects how the full 2x2 framework behaves at nearby thresholds. The registered headline remains the original 3.0 cutoff.

## Zone population by cutoff

| zone | 2025, c=2.75 | 2025, c=3.0 | 2025, c=3.25 | 2026, c=2.75 | 2026, c=3.0 | 2026, c=3.25 |
|---|---:|---:|---:|---:|---:|---:|
| Green Light | 446 | 364 | 211 | 553 | 455 | 207 |
| Red Light | 190 | 267 | 284 | 268 | 366 | 276 |
| R&D Opportunity | 123 | 107 | 102 | 16 | 16 | 106 |
| Low Priority | 85 | 106 | 247 | 7 | 7 | 255 |

## Migration count by threshold

| | c=2.75 | c=3.0 | c=3.25 |
|---|---:|---:|---:|
| Tasks with zone change | 195 (23%) | 200 (24%) | 298 (35%) |

## Bootstrap CIs on headline statistics (cutoff = 3.0)

| metric | point estimate | 95% bootstrap CI |
|---|---:|---|
| Tasks with zone change | 200 | [177, 225] |
| Share with capability >= 3 in 2026 | 97.3% | [96.1%, 98.3%] |

## Reading guide

- At c=2.75, most tasks are above threshold in both years; zones merge.
- At c=3.25, R&D Opportunity and Low Priority repopulate, but the 2026 capability axis is no longer saturated.
- The headline above-threshold share is sensitive to the cutoff.
- Migration count stays near 200 at c=2.75 and c=3.0, then rises at c=3.25.

## Near-threshold population

345/844 = 40.9% of tasks are near-threshold under the CSV flag, which uses median or mean capability in [2.5, 3.5]. Median-only count is 338/844 = 40.0%.
