# WORKBank Drift 2026 — Methodology

**Goal:** recompute the `Automation Capacity Rating` column of Stanford SALT Lab's WORKBank (data collected Jan–May 2025) against the April-2026 frontier (Claude Opus 4.7, Kimi K2.6, GPT-5.5), hold `Automation Desire Rating` constant, and publish the zone migrations.

This is a drift study, not a re-audit. Worker desire is treated as a fixed prior.

---

## 0. Licensing status (blocker — flag before writing derivative data)

Upstream WORKBank declares **no license** on either GitHub ([SALT-NLP/workbank](https://github.com/SALT-NLP/workbank)) or the HF dataset ([SALT-NLP/WORKBank](https://huggingface.co/datasets/SALT-NLP/WORKBank)). Confirmed 2026-04-24.

Implications:
- Cannot redistribute the raw `expert_rated_technological_capability.csv`, `domain_worker_desires.csv`, `task_statement_with_metadata.csv` under MIT.
- **Proposed resolution:** this repo does not mirror raw WORKBank files. Pipeline fetches them at build time via `datasets.load_dataset("SALT-NLP/WORKBank", ...)`. Only the *derivative* tables (`capability_2026.csv`, `drift_table.csv`) and our code ship under MIT. Raw data stays upstream.
- Parallel action: email first author (Yijia Shao) requesting explicit license clarification, cite the reply in README.

---

## 1. Data

Three upstream CSVs (HF, fetched at build time):

| File | Rows | Unique tasks | Key columns used |
|---|---:|---:|---|
| `task_data/task_statement_with_metadata.csv` | 2,131 | 2,131 | Task ID, O*NET-SOC Code, Occupation, Task, Task Type, Occupation Mean Annual Wage, Employment |
| `expert_ratings/expert_rated_technological_capability.csv` | 2,057 | 846 | Task ID, **Automation Capacity Rating** (1–5), Human Agency Scale (1–5) |
| `worker_data/domain_worker_desires.csv` | 5,731 | 844 | Task ID, **Automation Desire Rating** (1–5), Human Agency Scale (1–5) |

**Join key:** `Task ID`. Intersection = 844 tasks. Two tasks (IDs 1252, 21448) are expert-only, dropped.

---

## 2. Zone definition (locked to upstream paper)

Lifted verbatim from `analysis/automation_viability.ipynb`:

- `automation_capacity = mean(Automation Capacity Rating)` per Task ID, across all expert raters.
- `automation_desire   = mean(Automation Desire Rating)` per Task ID, across all worker raters.
- **Fixed cutoff at 3.0 on 1–5 Likert.** Not median split.

| Zone | Capacity | Desire |
|---|---|---|
| **Green Light** | ≥ 3 | ≥ 3 |
| **Red Light** | ≥ 3 | < 3 |
| **R&D Opportunity** | < 3 | ≥ 3 |
| **Low Priority** | < 3 | < 3 |

**2026 drift recomputes `automation_capacity` only.** `automation_desire` is held at its 2025 value. A task's zone changes iff its capability mean crosses 3.0.

---

## 3. 2026 capability scoring pipeline

### 3.1 Ensemble

Three independent frontier models, called in parallel per task:

| Model | Role |
|---|---|
| Claude Opus 4.7 | rater A |
| Moonshot Kimi K2.6 | rater B (replaced Gemini 3 Pro mid-pipeline due to API quota) |
| GPT-5.5 | rater C |

Rationale for n=3: the upstream dataset averages 2.4 expert ratings per task (range 1–5). Three uniform ratings per task gives *tighter* coverage than the upstream mean and is cheap enough for 844 tasks × 3 = 2,532 calls.

### 3.2 Per-task prompt

Each rater receives:
1. **Task statement** (verbatim from WORKBank)
2. **Occupation title** (O*NET-SOC)
3. **Requirement priors** (from WORKBank worker self-report means): Physical Action, Interpersonal Communication, Uncertainty, Domain Expertise — so model knows what the task *demands*, not just its surface description.
4. **Rubric** (§3.3).
5. **Benchmark anchors** (§3.4).
6. Instruction: return a single integer 1–5 plus one-sentence justification plus a list of the benchmark anchors it relied on.

Temperature = 0. Structured output (JSON schema). No chain-of-thought visible in output (to prevent anchoring on another rater's reasoning if we later do cross-model critique).

### 3.3 Rubric (Likert 1–5, matching upstream)

Mirrors the codebook's `Automation Capacity Rating` definition ("how capable current AI agents are of completing this task reliably without human intervention"):

| Score | Meaning (2026 frontier) |
|---|---|
| **1** | Cannot be done at all. Task requires physical embodiment, real-time sensor access, or continuous interpersonal judgment that current agents cannot deliver. |
| **2** | Demo-level only. Single model may produce a passable artifact with heavy prompting, but reliability < 50% in an agentic loop. Needs a human to finish. |
| **3** | Works with supervision. An agent can complete the core task when scaffolded (tool access, retry, verification step), but a domain expert must review outputs before use. |
| **4** | Works reliably. Off-the-shelf agent (e.g., Claude Opus 4.7 + standard tools) completes the task end-to-end for the typical case; a human only sees edge-case escalations. |
| **5** | Fully automated. Agent matches or exceeds typical human performance on the full distribution of cases. Human involvement adds no value beyond governance. |

### 3.4 Benchmark anchors (ground the rating)

Every task-type is mapped to ≥1 published April-2026 benchmark result. Raters must cite which anchor(s) they used. If a task has no relevant anchor, rater flags `LLM-inferred: true` and rating is treated as lower-confidence.

| Task family | Anchor benchmark(s) | Frontier score (2026-04, to pin in `benchmarks.yaml`) |
|---|---|---|
| Software engineering | SWE-bench Verified | Claude Opus 4.7 — verified score TBD at build time |
| Multi-step web agent | WebArena, GAIA | TBD |
| Desktop / OS control | OSWorld | TBD |
| General knowledge / reasoning | MMLU-Pro, GPQA Diamond | TBD |
| Code authoring | HumanEval+, LiveCodeBench | TBD |
| Math | MATH-500, AIME 2025 | TBD |
| Long-context synthesis | BABILong, RULER | TBD |
| Physical / embodied | *none — auto-score ≤ 2* | n/a |
| Continuous interpersonal | *none — rubric caps at 3 unless voice+turn-taking proves out* | n/a |

`benchmarks.yaml` is committed; numbers are pulled from each vendor's April-2026 model card or leaderboard screenshots stored in `data/benchmark_snapshots/` with retrieval date. **No fabricated scores. Empty cell > guessed cell.**

### 3.5 Aggregation

Upstream uses arithmetic mean across raters. We use **median of the 3 model scores** per task.

Reason for divergence from upstream: 3 raters is small; median is robust to a single-rater outlier, mean is not. This asymmetry is itself a methodology limitation and is documented in README.

We also report mean alongside median to let readers reproduce the upstream cutoff rule unchanged if they prefer.

### 3.6 Human calibration set

Author (Sam Meyer) hand-scores a **stratified sample of 50 tasks** before the ensemble runs:

- 10 tasks/zone from 2025 WORKBank (40 tasks) — so each zone is equally represented.
- 10 additional tasks sampled uniformly at random from the 844.

Calibration metrics reported:
- Spearman ρ between author scores and each model, pairwise.
- Cohen's weighted κ (linear weights, 5 ordinal levels) between author and ensemble median.
- Disagreement table for tasks where |author − ensemble| ≥ 2.

**Gate:** if ensemble-vs-author κ < 0.4 on the 50-task set, pipeline is paused and rubric is revised before full run.

---

## 4. Output tables

### 4.1 `data/capability_2026.csv`

One row per task (n ≈ 844):

| column | source |
|---|---|
| `task_id` | WORKBank |
| `occupation` | WORKBank |
| `task` | WORKBank |
| `desire_2025` | WORKBank worker-mean |
| `capability_2025` | WORKBank expert-mean |
| `zone_2025` | derived (§2) |
| `capability_opus_4_7` | rater A |
| `capability_kimi_k2_6` | rater B |
| `capability_gpt_5_5` | rater C |
| `capability_2026_median` | median of A/B/C |
| `capability_2026_mean` | mean of A/B/C |
| `zone_2026` | derived from median |
| `delta_capability` | median − `capability_2025` |
| `migration` | e.g. `Red→Green`, `Green→Green` (no-move) |
| `benchmark_anchors` | JSON list cited by raters |
| `llm_inferred_flag` | bool |
| `model_disagreement_std` | stddev of A/B/C |

### 4.2 `data/drift_summary.csv`

Aggregate zone population shifts (16-cell transition matrix) + per-occupation deltas.

### 4.3 Secondary axis (bonus)

Human Agency Scale is present in both upstream tables. We recompute it in parallel under the same protocol (expert-feasible HAS on 2026 frontier) and ship `data/has_drift_2026.csv`. HAS drift (H3→H1, etc.) is arguably the stronger story and costs little extra. Flagged in README, not front-paged.

---

## 5. Validation & release artifacts

1. **Inter-model agreement stats** — Krippendorff's α across the three models, full 844 tasks.
2. **Calibration report** — `reports/calibration.md`, 50-task human validation.
3. **Limitations section** in README — explicit:
   - n=3 raters is small vs. upstream's 53.
   - LLMs grading LLM-completable work is a self-serving prior; authors' rating was based on watching an agent attempt each task, which we do not replicate.
   - Benchmark anchors cover a subset of task families; long-tail knowledge work relies on model judgment with no anchor.
   - Median aggregation diverges from upstream (mean). Mean column shipped for apples-to-apples.
4. **Attribution block** in README + dashboard footer citing Shao et al. 2025 (arXiv:2506.06576).

---

## 6. Open decisions requiring your sign-off

1. **License strategy** — §0. Ship derivative-only + email authors? Or wait for explicit permission before publishing anything?
2. **Aggregation rule** — median (our proposal) vs mean (matches upstream exactly). We can ship both columns either way; the question is which drives `zone_2026`.
3. **Author calibration set size** — 50 feels like the floor. Willing to do 100 if you want tighter κ CIs, but it's ~2 hrs of your time.
4. **HAS drift** — ship alongside capability drift, or save for a second post?
5. **Agentic-execution validation** — upstream's rubric implicitly assumes an expert watched an agent try the task. We don't. Do we spot-check 20 tasks by actually running an agent (Claude Opus 4.7 + Anthropic computer-use or equivalent) and comparing its completion to our predicted score? Adds ~1 day, materially strengthens defensibility.
6. **Scoring budget** — 844 tasks × 3 models × ~3k tokens ≈ $60–120 total. Approve.

Once these are resolved, scoring pipeline runs against the approved rubric.
