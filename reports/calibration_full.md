# Calibration - full metric report (50-task v2)

Generated: 2026-07-07.
Calibration set: 50 tasks, stratified 10 per 2025 zone plus 10 random.
Two human raters: Sam Meyer (rater 1), independent (rater 2). Consensus = (sam+r2)/2 rounded half-up.
Primary ensemble: median of Codex OAuth GPT-5.5 xhigh, Moonshot Kimi K2.6, and OpenAI GPT-5.5 under rubric v2.

## Capability - agreement vs consensus

| comparison | κ_linear (95% boot CI) | κ_quadratic (95% CI) | binary >=3 (Wilson 95%) |
|---|---|---|---|
| **Inter-human (sam vs r2)** | 0.833 [0.697, 0.935] | 0.887 [0.776, 0.957] | 100% [93%, 100%] |
| **Ensemble vs consensus** | 0.554 [0.338, 0.734] | 0.608 [0.359, 0.794] | 94% [84%, 98%] |

The ensemble κ_linear 95% CI overlaps the pre-registered 0.4 gate at the lower bound. The point estimate is acceptable; uncertainty remains wide because n=50.

## Per-pair κ across model raters (full 844 tasks)

| pair | κ_linear | κ_quadratic |
|---|---:|---:|
| codex_gpt_5_5_xhigh vs gpt_5_5 | 0.636 | 0.696 |
| codex_gpt_5_5_xhigh vs kimi_k2_6 | 0.489 | 0.569 |
| gpt_5_5 vs kimi_k2_6 | 0.645 | 0.708 |

## Family-stratified agreement (capability)

| subset | n | κ_linear |
|---|---:|---:|
| Tasks where any rater fired a cap rule | 26 | 0.364 |
| Tasks where no cap rule fired | 24 | 0.545 |
| Tasks with consensus in [2.5, 3.5] (near-threshold) | 22 | -0.158 |

## Pre-registration note (transparency)

Prompt v1 produced ensemble-vs-consensus κ_linear = 0.327 and failed the 0.4 gate. Prompt v2 with explicit edge anchors and ordered cap hierarchy was developed and tested on the same 50 tasks. The calibration set is therefore not held out for v2; a fresh confirmatory n >= 30 is required for publication-grade claims.

## Reading guide

- The 0.4 κ_linear pre-registration target was set before any LLM rater scored a task.
- The inter-human κ_linear of 0.833 is the empirical ceiling for this task domain at this rubric maturity.
- Reports `reports/threshold_sensitivity.md` and `reports/anchor_audit.md` cover other dimensions.
