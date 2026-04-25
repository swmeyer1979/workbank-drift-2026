# WORKBank Drift 2026: Recomputing AI Task Capability Against the April-2026 Frontier

**Sam Meyer**
2026-04-25

---

## Abstract

Stanford SALT Lab's WORKBank dataset (Shao et al., 2025) classifies 844 occupational tasks across 104 U.S. occupations into four zones by worker-desire and AI-capability. The capability axis was scored by 53 expert raters between January and May 2025, predating Claude Opus 4.7, Kimi K2.6, GPT-5.5, and the broader April-2026 frontier. We recompute the capability axis with a three-model LLM-as-judge ensemble under a published rubric with explicit edge anchors and family caps, hold worker desire fixed at its 2025 value, and report zone migrations.

The headline drift is large. In 2025, 75% of in-scope tasks scored ≥ 3 on the 1–5 capability Likert. In 2026, **97.6% [96.6%, 98.6%]** scored ≥ 3. The original framework collapses under this saturation: R&D Opportunity falls from 107 to 12 tasks (−89%), Low Priority from 106 to 8 (−92%). 24% of tasks (205/844, [180, 230]) migrate zones. Two flows dominate: 98 tasks move from R&D Opportunity to Green Light (workers wanted the help, capability now arrived) and 102 move from Low Priority to Red Light (workers did not want the help, capability arrived anyway).

Calibration on a stratified 50-task sample with two human raters yields inter-human κ_linear = 0.834 and ensemble-vs-consensus κ_linear = 0.526 (95% bootstrap CI [0.321, 0.703]). The ensemble lower-bound CI overlaps the pre-registered 0.4 gate. A 20-task agentic spot-check using Perplexity Comet K2.6 returns Spearman ρ = 0.488 (p = 0.029) between predicted capability and realized agent grade. Migration counts pass a permutation test against random-delta reassignment at p < 0.001.

We treat the capability axis as a frontier-model self-assessment with calibrated human anchors, not a deployment claim. The original four-zone framework's discriminative power degenerates at this capability tier and is itself a finding.

---

## 1. Introduction

In May 2025, Shao et al. surveyed 1,500 U.S. workers and 53 AI experts to construct WORKBank, a database of 844 O*NET-derived occupational tasks rated for both worker-desire and AI-capability. The published framework classifies each task into one of four zones (Green Light, Red Light, R&D Opportunity, Low Priority) by a hard 3.0 cutoff on the 1–5 Likert mean of each axis. The paper's headline finding — that 41% of YC startup task targeting fell in the Red Light + Low Priority zones — has been cited as evidence of misalignment between AI productization and worker preferences.

The capability column was scored against the December 2024 to May 2025 frontier. The April-2026 frontier includes Claude Opus 4.7, Kimi K2.6, GPT-5.5, and Grok 4.20, all released or substantially upgraded after the upstream rating window. The intuition that drove this study: if frontier capability moved enough between mid-2025 and mid-2026, the WORKBank zones — defined relative to a particular capability snapshot — should shift in measurable ways.

We recompute the capability axis only. Worker desire is held at its 2025 value. This is by construction a study of capability drift under fixed preferences, not a re-audit. The substantive question is which tasks crossed the 3.0 capability threshold, not whether worker preferences also moved.

Three contributions. First, we publish a 844-task drift table with per-rater scores, ensemble median and mean, zone classifications under both aggregations, near-threshold flags, and inter-rater dispersion. Second, we report calibration against two independent human raters with full bootstrap confidence intervals and a separate agentic spot-check that anchors the LLM-as-judge in actual agent behavior on a stratified subsample. Third, we document several robustness checks — threshold sensitivity, importance-weighted aggregation, family-stratified agreement, permutation tests against null migration counts — that situate the headline drift within explicit uncertainty bands.

The headline finding is not subtle. Frontier models in April 2026 self-assess as capable on virtually all in-scope tasks that do not require physical embodiment or sustained empathic interaction. The two-axis framework collapses to one populated diagonal. We discuss what survives and what does not.

---

## 2. Related work

The methodological lineage is short and concentrated. Eloundou et al. (2024) score occupational task exposure to GPT-class models using LLM-as-judge against O*NET tasks; we inherit the protocol shape. Felten, Raj, and Seamans (2021, 2024) construct the AI Occupational Exposure (AIOE) index from a different annotation route. Webb (2020) uses patent text. Brynjolfsson, Li, and Raymond (2025) measure within-job productivity gains from generative AI deployment.

The upstream paper, Shao et al. (2025), introduces the desire-capability framework this work re-runs. Brynjolfsson is a co-author there. Acemoglu and Restrepo (2022) and Autor et al. (2024) provide the broader task-displacement framework underlying any zone-based exposure mapping. Acemoglu (2024) supplies a counterweight: capability is not impact, and aggregate effects depend on adoption costs the technical frontier does not predict.

LLM-as-judge methodology is documented in Zheng et al. (2023) and the literature that follows. The self-preference and self-evaluation biases in this paradigm are documented by Panickssery, Bowman, and Feng (2024) and are directly relevant: when judges rate tasks that members of their own model family perform, the prior is not neutral. Berkeley RDI (2026) demonstrates that several agent-family benchmarks (SWE-bench Verified, WebArena, GAIA, Terminal-Bench) are exploitable to near-perfect scores without solving the underlying tasks. We treat agent-family benchmark anchors in our prompt as upper bounds and report them with that caveat.

Tamkin et al. (2024) measure observed Claude usage by occupation. Where this drift study estimates capability, Tamkin et al. observe deployment. The two are distinct constructs and we keep them so.

---

## 3. Methodology

### 3.1 Data

WORKBank (Shao et al., 2025) is fetched at build time from Hugging Face. The dataset declares no license at the point of fetch (verified 2026-04-24); this repository ships derivative tables and code under MIT but does not redistribute the upstream files.

Three CSVs anchor the analysis: 2,131 task statements with O*NET-SOC code, occupation, wage, and employment metadata; 2,057 expert capability ratings across 846 unique tasks; 5,731 worker desire ratings across 844 unique tasks. Joining on `Task ID` yields 844 tasks with both axes scored. Two tasks (IDs 1252, 21448) appear in expert ratings only and are dropped.

### 3.2 Zone definition

Lifted unchanged from `analysis/automation_viability.ipynb` in the upstream repository. Per task:

* `automation_capacity` = mean of `Automation Capacity Rating` across expert raters.
* `automation_desire` = mean of `Automation Desire Rating` across worker raters.
* Cutoff at **3.0 on 1–5 Likert** for both axes, inclusive on the high side.

| zone | capability | desire |
|---|---|---|
| Green Light | ≥ 3 | ≥ 3 |
| Red Light | ≥ 3 | < 3 |
| R&D Opportunity | < 3 | ≥ 3 |
| Low Priority | < 3 | < 3 |

In 2026, capability is recomputed from the LLM ensemble; desire is held at its 2025 worker-mean value.

### 3.3 Ensemble

Three frontier models, called once per task, temperature zero where the API permits it:

| model | API | role |
|---|---|---|
| Claude Opus 4.7 | Anthropic | rater A |
| Moonshot Kimi K2.6 | OpenRouter | rater B |
| OpenAI GPT-5.5 | OpenAI | rater C |

Gemini 3 Pro was the original third rater, replaced after the gemini-3-pro-preview free-tier daily quota (250 requests/day) exhausted before the 844-task run completed. The swap is documented; calibration metrics for both ensembles are reported in `reports/calibration_full.md`. Headline numbers reported here use the Opus-Kimi-GPT triple. A subsequent 844-task run added Grok 4.20 as a fourth rater for sensitivity. Adding it shifts the headline 98%-above-threshold by 0%; zone counts move by 1–2 tasks.

For each task the rater receives the task statement, occupation title, worker-reported requirement priors (physical action, interpersonal communication, uncertainty, domain expertise), the rubric below, and a set of April-2026 benchmark anchors. Output is a structured JSON object containing capability and human-agency scores, a one-sentence justification, the cap rule that fired (if any), the benchmark anchors cited, and a self-reported confidence.

### 3.4 Rubric

Iterated once. The first version produced ensemble-vs-consensus κ_linear = 0.327 with a compressed score distribution: models avoided 2 and 5, collapsing to 3 and 4. The second version, used for all reported results, adds explicit edge anchors and an ordered cap hierarchy:

* **Rule 1, physical/embodied execution → max 2.** Tasks requiring interaction with physical equipment, materials, hardware, vehicles, lab apparatus, or biological subjects.
* **Rule 2, sustained interpersonal/empathic work → max 3.** Multi-turn human interaction where tone, empathy, or trust matter over time.
* **Rule 3, safety-critical unsupervised operation → max 3.** Outputs that take legal, medical, fiduciary, or life-safety effect without human review.
* **Rule 4, novel research or creative direction → max 3 for novel, max 4 for applied-routine.**

The rubric also includes anti-central-tendency language ("3 means a domain expert must review every output, which is a strong operational claim, not a neutral default") and worked examples of score 5 (pure data operations: filing, format conversion, lookup, defined-formula calculation). Worked examples are hypothetical, not drawn from the calibration set.

The rubric was iterated against the calibration sample. The calibration set is therefore not a held-out validator for v2; a fresh confirmatory n ≥ 30 sample is documented as a required next step.

### 3.5 Aggregation

Ensemble median across the three raters, rounded half-up to integer for zone classification. Mean is also reported per task in the output table for readers who prefer the upstream aggregation. All zone counts in this paper use the median.

### 3.6 Calibration

A 50-task stratified sample (10 per 2025 zone + 10 uniform random, seed 424) was drawn before any LLM scored a task. Two human raters scored independently:

* Rater 1: the author. Drafted scores under rubric v2, reviewed twice; eight substantive edits to capability scores between draft and final, all directionally net-zero.
* Rater 2: an independent reviewer not involved in pipeline design. Scored from a blank CSV with the same rubric.

Consensus is `(rater1 + rater2) / 2` rounded half-up. Inter-human metrics on capability:

* κ_linear = 0.834 [0.699, 0.937]
* κ_quadratic = 0.886 [0.776, 0.959]
* Krippendorff's α (ordinal) = 0.880
* Binary ≥ 3 agreement = 100%
* Zone agreement on the 50-task sample = 100%

Human-human zone agreement is exact. Capability disagreements occur at adjacent levels only (max |diff| = 1 across all 50 tasks). Ensemble-vs-consensus, capability:

* κ_linear = 0.526 [0.321, 0.703]
* κ_quadratic = 0.590 [0.356, 0.770]
* Binary ≥ 3 agreement = 94% [84%, 98%]

The ensemble κ_linear 95% bootstrap CI overlaps the pre-registered 0.4 gate at the lower bound and falls below the inter-human ceiling. The point estimate is acceptable; the uncertainty is wide because n = 50 with two raters is underpowered.

### 3.7 Agentic spot-check

LLM-as-judge has a self-grading prior: judges score tasks members of their own model family perform. Family caps mitigate the upper tail; the score-3-vs-4 boundary, where most drift sits, has no rubric-based external check. We add an agentic validation.

A stratified 20-task sample (5 each at predicted capability 2/3/4/5) was generated. Each task was attempted by Perplexity Comet (K2.6, Pro account) under remote-debugging Chromium control. Comet was prompted to actually attempt the task using web tools and synthetic data, then label its own outcome. The author then graded each captured response on a 1–3 scale (1 = failed, 2 = partial, 3 = succeeded with a usable artifact), reading the response content directly. Comet's self-label was uniformly "completed" across all 20 and was not used.

Spearman ρ between predicted capability (1–5) and author-graded agent outcome (1–3) is **0.488 (p = 0.029)**. Per-bucket means: cap = 2 → 2.2; cap = 3 → 2.8; cap = 4 → 3.0; cap = 5 → 2.8. Agent outcomes saturate at 3 because the grading scale tops out there; this is a method limitation. Cap-2 tasks were partial on 4/5 (physical-tier work: SCADA monitoring, hardware tests, biofuels production monitoring, mechanical equipment adjustment) and succeeded on the fifth (warehouse inventory monitoring, task ID 15897). Task 15897 is one of the three calibration-set tasks where humans had over-ridden the ensemble's cap-2 prediction to 4. The agent confirms the human direction.

---

## 4. Results

### 4.1 Capability shift

Mean capability across 844 tasks rises from 3.46 (2025 expert mean) to 3.67 (2026 ensemble median). The aggregate change is small. The threshold-crossing change is large: tasks scoring ≥ 3 rise from 75% to 97.6% [96.6%, 98.6%]. Concentration above threshold is the salient story; the integer-Likert distribution shifts from {1: 38, 2: 385, 3: 683, 4: 615, 5: 336} (2025 expert ratings, raw) to {2: 20, 3: 226, 4: 410, 5: 188} after ensemble median rounding (2026, in-scope 844).

### 4.2 Zone migration

Two-axis classification under fixed 2025 desire and 2026 capability:

| zone | 2025 | 2026 | Δ |
|---|---:|---:|---:|
| Green Light | 364 | 459 | +95 |
| Red Light | 267 | 365 | +98 |
| R&D Opportunity | 107 | 12 | −95 |
| Low Priority | 106 | 8 | −98 |

205 tasks (24.3%, [180, 230] bootstrap 95% CI) migrate zones. The 4×4 transition matrix is dominated by four cells:

| from \ to | Green | Red | R&D | Low |
|---|---:|---:|---:|---:|
| Green | 361 | 0 | 3 | 0 |
| Red | 0 | 264 | 0 | 3 |
| R&D | 98 | 0 | 9 | 0 |
| Low | 0 | 101 | 0 | 5 |

Two flows account for 199 of 205 migrations:

* **R&D Opportunity → Green Light: 98 tasks.** Tasks workers reported wanting AI assistance with in 2025, where 2025 capability was insufficient. 2026 capability now clears the threshold. Examples include video game documentation, sales presentation prep, clinical data flow tracking, regulatory knowledge maintenance, judicial law clerk file verification, logistics tracking.
* **Low Priority → Red Light: 101 tasks.** Tasks where 2025 worker desire was below threshold and 2025 capability was below threshold. 2026 capability has crossed; desire has not. Examples include ticket and document issuance, secretarial correspondence, network configuration, HR test scheduling, medical appointment scheduling.

Both cells are large compared to the permutation null. Under random reassignment of capability deltas across tasks (5,000 permutations, preserving the marginal delta distribution), the null mean is 37 for R&D → Green and 38 for Low → Red, with 95% null ranges of [29, 47]. Both observed counts produce two-sided p-values below 0.0001. The reverse flows (Green → R&D and Red → Low) have observed counts of 3 each against a null mean of 41–42; capability did not move down for the existing populated zones.

### 4.3 Threshold sensitivity

The 3.0 cutoff creates classification cliffs. 39% of 844 tasks have ensemble median capability in [2.5, 3.5]; these are the most cutoff-sensitive. Migration count is robust to threshold choice in the [2.75, 3.0] range and grows substantially at 3.25:

| | c = 2.75 | c = 3.0 | c = 3.25 |
|---|---:|---:|---:|
| Tasks with zone change | 200 (24%) | 205 (24%) | 296 (35%) |
| Share with capability ≥ c (2026) | — | 97.6% | — |

At c = 3.25, R&D Opportunity refills to 99 tasks and Low Priority to 242, recovering populated quadrants. The framework's degeneracy at c = 3.0 is partly an artifact of the fixed cutoff being calibrated to 2025 capability levels. A drift-aware framework would recalibrate the cutoff to preserve four populated zones; we do not recalibrate here in order to preserve direct comparability with the upstream paper.

### 4.4 Importance-weighted aggregation

WORKBank metadata provides per-task `Importance`, `Frequency`, and `Relevance` ratings. Reweighting tasks by `Importance × Frequency × Relevance` shifts the headline zone shares by less than 1.5 percentage points in any cell. Migration shares:

| migration | unweighted | weighted |
|---|---:|---:|
| Green → Green | 42.8% | 42.7% |
| Red → Red | 31.3% | 32.6% |
| Low → Red | 12.0% | 11.6% |
| R&D → Green | 11.6% | 10.3% |

The drift result is not concentrated in peripheral tasks; central tasks migrate at similar rates.

### 4.5 Wage and employment exposure

Joining the upstream BLS 2024 occupation mean annual wage and employment to the 76 in-scope occupations:

| migration class | n occupations | workers (M) | wage bill ($B) | mean wage ($) |
|---|---:|---:|---:|---:|
| R&D → Green | 48 | 5.82 | 578.6 | 99,600 |
| Low → Red | 52 | 9.39 | 849.6 | 90,400 |
| Green → Green | 94 | 21.45 | 1,900.4 | 88,600 |
| Red → Red | 79 | 19.42 | 1,558.2 | 80,200 |

The Low → Red bucket touches 52 occupations totaling 9.4M U.S. workers and approximately $850B in annual wage bill. R&D → Green touches 48 occupations, 5.8M workers, $580B in wage bill. These are upper-bound exposure figures — full occupational employment, not the share of an occupation's wage bill apportioned to migrating tasks. A finer-grained estimate weighting each occupation's wage bill by the share of its tasks that migrated is left to follow-on work.

### 4.6 Demographic exposure

Cross-walking BLS Current Population Survey 2024 occupation-level demographic shares to 50 of 104 in-scope occupations (matched on cleaned occupation title), employment-weighted demographic share by migration class:

| migration | n occs | workers (M) | Women % | White % | Black/AA % | Asian % | Hispanic % |
|---|---:|---:|---:|---:|---:|---:|---:|
| R&D → Green | 17 | 4.4 | 51.4% | 79.3% | 9.2% | 7.9% | 13.3% |
| Low → Red | 23 | 7.4 | **65.5%** | 78.6% | 10.5% | 7.4% | 13.7% |
| Green → Green | 45 | 18.2 | 60.4% | 77.3% | 11.4% | 7.8% | 14.1% |
| Red → Red | 42 | 16.4 | 62.4% | 77.6% | 11.5% | 7.3% | 14.6% |

Baseline BLS workforce: women 47.1%. The Low → Red bucket is 65.5% female-weighted, 18.4 percentage points above baseline. Clerical, secretarial, and scheduling tasks dominate this migration class; these occupations remain disproportionately female. The R&D → Green bucket is closer to baseline at 51.4% female. Capability arrival is not demographically uniform across the two cross-zone migrations.

The match rate (50/104 occupations) is a coverage caveat. A publication-grade analysis would use IPUMS USA ACS PUMS with explicit SOC codes; a stub procedure is documented in `reports/external_joins.md`.

### 4.7 YC mapping recompute

The upstream paper's most-cited derivative is that 41% of YC startup company-task mappings sit in Red + Low zones in 2025. Recomputing with 2026 capability and fixed 2025 desire, on 841 of 2,076 published YC mapping rows that match our 844-task table by (task, occupation):

| zone | 2025 share of YC pairs | 2026 share |
|---|---:|---:|
| Green Light | 45.6% | 57.6% |
| Red Light | 29.4% | 40.7% |
| R&D Opportunity | 13.2% | 1.2% |
| Low Priority | 11.8% | 0.5% |

Misalignment share (Red + Low) is unchanged: 41.2% in 2025, 41.2% in 2026. The composition flipped. In 2025 the 41% comprised both startups targeting unwanted-but-feasible work (Red, 29.4%) and startups targeting infeasible work (Low, 11.8%). In 2026 it is essentially all Red Light: capability arrived into the entire Low Priority sub-bucket of YC targeting. The Red + Low composite metric no longer distinguishes "misaligned" from "well-aligned" under 2026 capability and should be split into its constituents in any updated analysis.

### 4.8 Cap rule audit and anchor coverage

The rubric's cap hierarchy fired on 360 of 844 tasks (43%) for at least one rater; 119 tasks (14%) had all three raters fire some cap. Rule frequencies across all three raters in the production run:

| rule | total fires (across raters) |
|---|---:|
| safety_critical | 371 |
| interpersonal | 199 |
| novel_research | 81 |
| physical | 66 |

Tasks with no cap fired have higher mean ensemble capability (4.07) than capped tasks (3.12), and 100% of uncapped tasks score ≥ 3 versus 94% of capped tasks. The cap hierarchy is doing meaningful work at the boundary; both R&D Opportunity (12 tasks) and Low Priority (8 tasks) survive in 2026 only among cap-fired tasks. A counterfactual leave-one-out, re-scoring with each rule disabled, is deferred (~$120 in API spend).

Benchmark anchor coverage is uneven across raters. Empty-anchor rates: Opus 4.7 = 2.3%, Kimi K2.6 = 71.1%, GPT-5.5 = 3.7%. Kimi is functionally unanchored on most tasks and self-flags `llm_inferred = true` on 73.5% of calls. The ensemble effectively has two anchored raters and one judge-from-priors rater. Pairwise inter-rater κ (capability) supports this: Opus–GPT = 0.631, Kimi–GPT = 0.708, Kimi–Opus = 0.353. Kimi diverges from Opus more than from GPT.

---

## 5. Discussion

### 5.1 The framework collapsed

A two-axis 2x2 framework communicates by separating tasks across both axes. When 97.6% of tasks score above the capability threshold, the framework communicates only on the desire axis. Two of four zones effectively empty out. The R&D Opportunity finding from the upstream paper — "tasks workers want AI to help with that AI can't yet do" — survives in 2026 only as a residual of 12 tasks, dominated by physical-tier work.

This is not a failure of the original framework. It is a direct consequence of holding the threshold fixed across a year of capability movement. A drift-aware framework would recalibrate. The c = 3.25 sensitivity result demonstrates this: at a quarter-point higher cutoff, 99 R&D Opportunity tasks and 242 Low Priority tasks repopulate, and the migration count grows to 35%. Whether to recalibrate the threshold is itself a research-design decision; we report both the unchanged-threshold result (for direct comparability) and the threshold-shift sensitivity.

### 5.2 Capability is not deployment

The 102 Low → Red migrations are politically combustible if framed as "AI ate jobs workers did not want eaten." The frame is wrong on two grounds.

First, capability arrival precedes and does not entail deployment. None of the agents whose self-assessments populate the 2026 capability axis is deployed against most of these tasks at scale. Tamkin et al. (2024) provide a separate occupational-usage measurement that should be cross-referenced before any displacement claim is made.

Second, the Low Priority zone's defining feature is that workers reported low desire to delegate. Many of these tasks are intra-occupation activities workers had already deprioritized in their own time allocation; "did not want AI to do this" can mean both "this is mine and important" and "nobody should have to do this and it might as well be automated when feasible." The aggregate worker-level data in WORKBank does not separate these.

The honest framing is narrower: capability has arrived in the Low Priority zone faster than worker preferences have updated. The reallocation that follows depends on adoption costs and labor demand effects this study does not estimate.

### 5.3 The female-exposed Low → Red flow

Low → Red is 65.5% female-weighted versus a 47.1% workforce baseline. The migration class is concentrated in clerical, administrative, secretarial, and scheduling occupations — task-displacement targets identified by Autor and others in earlier waves of office automation. The drift result here is consistent with the pattern, not novel relative to it. What is new is that the threshold-crossing fraction is high enough that almost all cognitive-routine tasks in these occupations now fall in the capability-feasible space.

The R&D → Green flow (51.4% female) is closer to baseline. Where capability arrived for tasks workers explicitly wanted help with, the demographic profile is mixed.

### 5.4 What the calibration can and cannot claim

The inter-human ceiling for this rubric and task domain is κ_linear = 0.834 with binary ≥3 agreement at 100% and zone agreement at 100% on the 50-task sample. This is a strong ceiling. Two raters scoring under the same rubric agree exactly on every zone assignment.

The ensemble achieves κ_linear = 0.526, 63% of the human-human ceiling. The 95% bootstrap CI is wide because n = 50 with two raters is underpowered. The lower CI bound (0.321) does not exclude the pre-registered 0.4 gate. The point estimate is above the gate; the upper CI bound is well above it. We treat the gate as passed in expectation but acknowledge the noisiness.

Cap-fired tasks show much weaker agreement (κ_linear = 0.266 on 31 tasks) than uncapped tasks (κ_linear = 0.638 on 19 tasks). The cap rules introduce structured disagreement. The three calibration-set tasks where humans corrected the ensemble's cap-2 prediction to capability 4 are all physical-engineering tasks; the agentic spot-check confirms the human direction (the agent succeeded on warehouse inventory monitoring, which is digital despite being labeled "warehouse").

Calibration alternatives — linear shift+scale, isotonic regression, ordered-logit-via-rounded-linear — were tested. None improves leave-one-out MAE over the raw ensemble median. All four methods produce identical 94% binary ≥3 agreement on the calibration set. Calibration mapping is not load-bearing for the zone-classification task here. The threshold dominates.

### 5.5 What an external validity check would look like

The ideal external validity check is an actual frontier agent attempting each task with success graded by an independent human, against benchmarks the agent cannot game. The agentic spot-check approximates this on n = 20: ρ = 0.488, p = 0.029. The correlation is modest but significant; the agent grade saturates at 3 (a method limitation we should fix in v2 with a 1–5 grading scale and Comet operating in Computer mode rather than Assistant mode).

A second external check would be correlating per-occupation 2026 capability with the Felten-Raj-Seamans AIOE 2.0 index. We document the protocol in `reports/external_joins.md`; the dataset fetch is non-trivial and is left to follow-on work.

---

## 6. Limitations

* **Single-author with one second human rater.** Rater 2 was an independent reviewer; rater 3 was not recruited. The inter-human ceiling is from n = 2.
* **Calibration set was iterated.** Rubric v2 was tested on the same 50 tasks that rubric v1 failed. The set is contaminated for v2 evaluation. A fresh confirmatory n ≥ 30 sample is documented and not yet scored.
* **LLM-as-judge self-grading prior.** The rubric mentions the rater models by name in the score-4 anchor. The agentic spot-check is the partial mitigation; it correlates at ρ = 0.488 with predictions but is itself author-graded.
* **Hard threshold at 3.0.** 39% of tasks fall in [2.5, 3.5]. Migrations near the boundary are sensitive to ensemble noise. Bootstrap CIs and threshold sensitivity reports cover this.
* **Ensemble swap mid-pipeline.** Gemini 3 Pro was the originally specified third rater; its free-tier daily quota exhausted before the 844-task run completed. Kimi K2.6 replaced it. Both ensembles' calibration metrics are reported. The swap is not a selection-on-outcome — Kimi K2.6 had not been calibrated when the swap was made.
* **Benchmark anchor unevenness.** Kimi K2.6 cited an empty anchor list on 71% of calls. The ensemble effectively has two anchored raters and one judge-from-priors rater on most tasks.
* **Demographic match rate.** 50 of 104 occupations matched BLS CPS occupation strings. IPUMS USA ACS PUMS is the publication-grade upgrade.
* **Snapshot timestamp.** The headline 97.6% above threshold is dated 2026-04-25. Models released after this date will produce different numbers under the same protocol.
* **Worker desire fixed at 2025.** This is the design constraint that defines the study as drift-only. Worker preferences may have moved between 2025 and 2026; we do not measure that movement.

---

## 7. Conclusion

The capability axis of WORKBank, recomputed under an April-2026 frontier ensemble with calibrated human anchors and an agentic spot-check, has crossed the published 3.0 threshold for 97.6% of in-scope tasks. The four-zone framework collapses to an effective two-zone framework. R&D Opportunity (107 → 12 tasks) and Low Priority (106 → 8) empty out. The two cross-zone flows that absorb the change — 98 R&D → Green and 102 Low → Red — are large compared to permutation nulls and concentrated in occupations totaling roughly $1.4T in U.S. annual wage bill across 15 million workers.

The honest framing is narrow: this is a frontier-model self-assessment of task feasibility under fixed 2025 worker preferences, calibrated against two human raters with bootstrap confidence intervals overlapping the pre-registered gate at the lower bound. It is not a deployment claim, not a labor-impact estimate, and not a re-audit of the upstream paper's worker-survey methodology.

The drift is large enough, and the framework's discriminative power degrades enough at this capability tier, that any updated version of the desire-capability map should either recalibrate the threshold or split the Red + Low composite into its constituents. The original paper's 41% misalignment finding holds numerically in 2026 but means something different — startups are predominantly targeting feasible-but-low-desire tasks rather than the heterogeneous 2025 mix. That compositional shift is the single most informative summary of what changed.

Replication artifacts, raw rater outputs, calibration scores, and twelve detailed report files are public at the project repository. A fresh confirmatory calibration sample, a Felten AIOE correlation, IPUMS demographic join, and an expanded agentic spot-check (n = 50, 1–5 grading scale, Computer mode) are documented as next steps.

---

## References

* Acemoglu, D. & Restrepo, P. (2022). *Tasks, Automation, and the Rise in U.S. Wage Inequality.* Econometrica.
* Acemoglu, D. (2024). *The Simple Macroeconomics of AI.* NBER Working Paper 32487.
* Autor, D., Chin, C., Salomons, A., & Seegmiller, B. (2024). *New Frontiers: The Origins and Content of New Work, 1940–2018.* Quarterly Journal of Economics.
* Berkeley RDI (2026). *Benchmark Gaming in Frontier Agent Evaluations.*
* Brynjolfsson, E., Li, D., & Raymond, L. (2025). *Generative AI at Work.* Quarterly Journal of Economics.
* Eloundou, T., Manning, S., Mishkin, P., & Rock, D. (2024). *GPTs are GPTs: Labor Market Impact Potential of LLMs.* Science.
* Felten, E., Raj, M., & Seamans, R. (2021, 2024). *Occupational, Industry, and Geographic Exposure to Artificial Intelligence.* Strategic Management Journal; AIOE 2.0 update.
* Panickssery, A., Bowman, S., & Feng, S. (2024). *LLM Evaluators Recognize and Favor Their Own Generations.*
* Shao, Y., Zope, H., Jiang, Y., Pei, J., Nguyen, D., Brynjolfsson, E., & Yang, D. (2025). *Future of Work with AI Agents: Auditing Automation and Augmentation Potential across the U.S. Workforce.* arXiv:2506.06576.
* Tamkin, A., et al. (2024). *Clio: Privacy-Preserving Insights into Real-World AI Use.* Anthropic Economic Index.
* Webb, M. (2020). *The Impact of Artificial Intelligence on the Labor Market.* Working paper.
* Zheng, L., et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* NeurIPS.
