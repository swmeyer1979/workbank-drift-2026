# Calibration — full metric report (50-task v2)

Generated: 2026-04-25.
Calibration set: 50 tasks, stratified 10 per 2025 zone + 10 random.
Two human raters: Sam Meyer (rater 1), independent (rater 2). Consensus = (sam+r2)/2 rounded half-up.
Ensemble: median of Claude Opus 4.7, Moonshot Kimi K2.6, OpenAI GPT-5.5 under rubric v2.

## Capability — agreement vs consensus

| comparison | κ_linear (95% boot CI) | κ_quadratic (95% CI) | binary ≥3 (Wilson 95%) |
|---|---|---|---|
| **Inter-human (sam vs r2)** | 0.834 [0.699, 0.937] | 0.886 [0.776, 0.959] | 100% [93%, 100%] |
| **Ensemble vs consensus** | 0.526 [0.321, 0.703] | 0.590 [0.356, 0.770] | 94% [84%, 98%] |

The ensemble κ_linear 95% CI is [0.321, 0.703]. This **overlaps the pre-registered 0.4 gate** (lower bound is below 0.4) and **does not overlap the inter-human ceiling** (upper bound below the human-human point estimate). The point estimate is acceptable; the uncertainty is wide because n=50.

## Per-pair κ across model raters (capability)

| pair | κ_linear | κ_quadratic |
|---|---|---|
| kimi_k2_6 vs opus_4_7 | 0.353 | 0.424 |
| gpt_5_5 vs opus_4_7 | 0.631 | 0.714 |
| gpt_5_5 vs kimi_k2_6 | 0.708 | 0.791 |

**Interpretation:** if one pair has dramatically higher κ than the others, the ensemble is dominated by that pair and the third rater is contributing little. The Kimi K2.6 standalone κ vs consensus was 0.360 (linear) — the weakest. This is consistent with Kimi being the single "outside" voice (the other two share the rubric's named-rater bias).

## Family-stratified agreement (capability)

| subset | n | κ_linear |
|---|---:|---|
| Tasks where any rater fired a cap rule | 31 | 0.266 |
| Tasks where no cap rule fired | 19 | 0.638 |
| Tasks with consensus in [2.5, 3.5] (near-threshold) | 22 | -0.193 |

## Pre-registration note (transparency)

Prompt v1 produced ensemble-vs-consensus κ_linear = 0.327 (failed the 0.4 gate).
Prompt v2 with explicit edge anchors and ordered cap hierarchy was developed and tested **on the same 50 tasks**, producing the metrics above.
The calibration set is therefore not held-out for v2; a fresh confirmatory n ≥ 30 is required for publication-grade claims.

## Reading guide

- The 0.4 κ_linear pre-registration target was set before any LLM rater scored a task.
- The inter-human κ_linear of 0.834 is the empirical ceiling for this task domain at this rubric maturity.
- Reports `reports/threshold_sensitivity.md` and `reports/anchor_audit.md` cover other dimensions.
