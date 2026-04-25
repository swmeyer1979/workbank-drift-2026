# WORKBank Drift 2026

**Which jobs crossed the AI-capability threshold since Stanford SALT's WORKBank audit?**

Stanford SALT Lab's [WORKBank](https://futureofwork.saltlab.stanford.edu) (Shao et al., 2025) surveyed 1,500 workers and 53 AI experts between January and May 2025, classifying **844 tasks across 104 U.S. occupations** into four zones by worker-desire × AI-capability:

- 🟢 **Green Light** — high desire + high capability
- 🔴 **Red Light** — high capability + low desire
- 🟠 **R&D Opportunity** — high desire + low capability
- ⚪ **Low Priority** — low / low

This repo recomputes the **capability** axis against the **April-2026 frontier** (Claude Opus 4.7, Kimi K2.6, GPT-5.5), holds worker desire fixed at its 2025 value, and publishes the tasks that migrated zones.

> This is a drift study using fixed 2025 worker preferences. The capability axis here is a frontier-model **self-assessment** with human calibration, **not** a deployment claim. A task scoring "capability ≥ 3" means an ensemble of 2026 frontier models judges the task achievable with supervision, not that any organization has deployed an agent doing it. The 2025 framework's discriminative power degenerates at frontier — when ~98% of in-scope tasks score ≥ 3, the four-zone framework has effectively collapsed to two zones, which is itself a finding about the framework, not just about capability.

**Live dashboard:** _TBD_
**Findings (1-page):** [`findings.md`](./findings.md) — _populated after scoring run_

---

## Methodology

Full protocol in [`METHODOLOGY.md`](./METHODOLOGY.md). Summary:

- Zone boundary from the original paper: fixed cutoff at **3.0** on 1–5 Likert, mean across raters. Unchanged.
- 2026 capability scored by an ensemble of three frontier models, temperature 0, one call per model per task.
- Each rater receives the task statement, occupation, WORKBank-derived requirement priors, a pinned rubric, and a set of April-2026 benchmark anchors (SWE-bench Verified, GAIA, WebArena, OSWorld, MMLU-Pro, etc.).
- Raters return a 1–5 Likert score plus a one-sentence justification plus cited benchmark anchors.
- **Both median and mean** of the three model scores are reported. `zone_2026` is provided under both aggregations.
- **Human calibration:** the author hand-scores a stratified 50-task sample before the full pipeline runs. κ gate at ≥ 0.4.
- **Agentic spot-check:** ~20 sampled tasks are attempted end-to-end by Claude Opus 4.7 + tool-use, and actual completion quality is compared to the predicted score.

### Limitations (read before citing)

- **n=3 model raters per task vs. upstream's ~2.4 expert raters per task** — coverage is comparable per task, but the three model raters are correlated by training-data overlap in ways the upstream human panel was not.
- **Self-grading prior:** raters score tasks that members of their own model family perform. Family caps (physical → ≤2, sustained interpersonal → ≤3, safety-critical unsupervised → ≤3) mitigate the upper tail; the score-3-vs-4 boundary, where most drift sits, is not externally validated. Agentic spot-check is the recommended next step and is not yet implemented.
- **Calibration is underpowered** as a publication-grade gate: n=50 stratified tasks, 2 human raters, bootstrap 95% CI on κ overlaps both the pre-registered 0.4 gate and the 0.833 inter-human ceiling. Treat reported κ values as point estimates with wide error bands.
- **Pre-registration was iterated:** prompt v1 failed the κ ≥ 0.4 gate; prompt v2 with explicit edge anchors and ordered cap hierarchy passed. The calibration set saw both prompts; a fresh confirmatory set (proposed n=30) is required for publication-grade claims.
- **Benchmark anchors are decorative in places:** ~50% of cells in `benchmarks.yaml` are null; all populated cells are flagged `status: unverified` (extracted from third-party aggregators, not vendor model cards). Audit of full_844 outputs shows Kimi K2.6 cited an empty anchor list on ~71% of calls, indicating one of three raters is essentially unanchored — a silent failure mode flagged in [`reports/anchor_audit.md`](./reports/anchor_audit.md).
- **Hard 3.0 threshold creates classification cliffs.** 40% of 844 tasks have ensemble capability in [2.5, 3.5]. Sensitivity at thresholds 2.75 / 3.0 / 3.25 is reported in [`reports/threshold_sensitivity.md`](./reports/threshold_sensitivity.md).
- **No demographic robustness.** ACS/SOC join is recommended but not yet performed.
- **Median aggregation diverges from upstream mean.** Both are reported per task in `capability_2026.csv` so readers can reproduce either rule.
- **Reproducibility under model drift:** the headline percentage is a snapshot timestamped 2026-04-25. Models released after this date will produce different numbers under the same protocol.

---

## Data

This repository does **not** redistribute WORKBank. The upstream dataset has no declared license as of 2026-04-24. The pipeline fetches it at build time from
[`huggingface.co/datasets/SALT-NLP/WORKBank`](https://huggingface.co/datasets/SALT-NLP/WORKBank)
and only our derivative tables ship here:

- [`data/capability_2026.csv`](./data/capability_2026.csv) — one row per task, 2025 → 2026 capability, zone migration
- [`data/has_drift_2026.csv`](./data/has_drift_2026.csv) — Human Agency Scale drift (bonus axis)
- [`data/drift_summary.csv`](./data/drift_summary.csv) — aggregate zone-population shifts
- [`data/calibration_sample.csv`](./data/calibration_sample.csv) — 50-task human-scored validation set
- [`data/benchmarks.yaml`](./data/benchmarks.yaml) — pinned April-2026 benchmark results with citations

---

## Reproducing

```bash
uv sync
uv run fetch-workbank         # fetch upstream at build time; no raw commit
uv run sample-calibration     # draw stratified 50-task sample for human scoring
uv run score-capability       # ensemble scoring pipeline (requires API keys / OAuth)
uv run build-drift-table      # join, aggregate, classify zones, emit derivative CSVs
```

Credentials: see [`.env.example`](./.env.example). Claude Opus 4.7 uses OAuth subscription billing when available; falls back to `ANTHROPIC_API_KEY`. GPT-5.5 requires `OPENAI_API_KEY`. Kimi K2.6 routed via OpenRouter (`OPENROUTER_API_KEY`).

> **Ensemble note (2026-04-25):** This study originally specified Gemini 3 Pro as the third rater. Mid-pipeline the gemini-3-pro-preview free-tier daily quota (250 req/day) was exhausted before the 844-task run completed. Gemini 3 Pro is replaced with **Moonshot Kimi K2.6** for production scoring. Calibration metrics for both ensembles are reported side-by-side in [`reports/calibration.md`](./reports/calibration.md).

---

## Related work

- **Shao, Zope, Jiang, Pei, Nguyen, Brynjolfsson, Yang, 2025** — *Future of Work with AI Agents: Auditing Automation and Augmentation Potential across the U.S. Workforce.* arXiv:2506.06576. The upstream WORKBank paper.
- **Eloundou, Manning, Mishkin, Rock, 2024** — *GPTs are GPTs: Labor market impact potential of LLMs.* Science. The canonical occupational-exposure benchmark; this work is methodologically downstream of it.
- **Felten, Raj, Seamans, 2021/2024** — *AI Occupational Exposure (AIOE) index.* O*NET-anchored capability scoring. Recommended cross-validation: correlate `capability_2026_median` per occupation with AIOE.
- **Webb, 2020** — *The Impact of Artificial Intelligence on the Labor Market.* Patent-text-based occupational exposure; methodological cousin.
- **Acemoglu & Restrepo, 2022** — *Tasks, Automation, and the Rise in U.S. Wage Inequality.* Econometrica. Provides the task-displacement framework underlying the upstream zones.
- **Acemoglu, 2024** — *The Simple Macroeconomics of AI.* NBER WP 32487. Counterweight to capability-equals-impact framing.
- **Autor, Chin, Salomons, Seegmiller, 2024** — *New Frontiers: The Origins and Content of New Work, 1940-2018.* QJE. Task emergence/disappearance over time.
- **Brynjolfsson, Li, Raymond, 2025** — *Generative AI at Work.* QJE. Within-job productivity at the task level — the augmentation evidence missing from a pure capability-score frame.
- **Tamkin et al., 2024** — *Clio: Privacy-Preserving Insights into Real-World AI Use* (Anthropic Economic Index). Vendor-side measurement of where agents are actually used.
- **Panickssery, Bowman, Feng, 2024** — *LLM Evaluators Recognize and Favor Their Own Generations.* Direct prior on the self-grading bias this study is exposed to.
- **Zheng et al., 2023** — *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* The LLM-as-judge methodology this work inherits and the biases it documents.
- **Berkeley RDI, 2026** — *Benchmark Gaming in Frontier Agent Evaluations.* Documents how SWE-bench Verified, WebArena, GAIA, and Terminal-Bench are exploitable to near-perfect scores without solving tasks. Treat agent-family anchors in `benchmarks.yaml` as upper bounds.

## Citation

If you use this drift study, please cite both the original work and this repo.

```bibtex
@misc{shao2025futureworkaiagents,
  title = {Future of Work with {AI} Agents: Auditing Automation and Augmentation
           Potential across the {U.S.} Workforce},
  author = {Shao, Yijia and Zope, Humishka and Jiang, Yucheng and Pei, Jiaxin
            and Nguyen, David and Brynjolfsson, Erik and Yang, Diyi},
  year = {2025},
  eprint = {2506.06576},
  archivePrefix = {arXiv},
  primaryClass = {cs.CY},
  url = {https://arxiv.org/abs/2506.06576}
}

@misc{meyer2026workbankdrift,
  title  = {{WORKBank} Drift 2026: Recomputing {AI} Capability against the
            April-2026 Frontier},
  author = {Meyer, Sam},
  year   = {2026},
  url    = {https://github.com/<user>/workbank-drift-2026}
}
```

---

## License

Code and derivative data: [MIT](./LICENSE).
Upstream WORKBank data: unlicensed as of 2026-04-24 — fetched at build time, not redistributed.
