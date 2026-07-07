# WORKBank postmortem rerun spec

Date: 2026-07-07
Scope: L

## Objective

Rerun the WORKBank drift analysis as a reproducible audit while preserving existing outputs before any overwrite.

## Approach

- Use the replacement primary triple approved 2026-07-07: `codex_gpt_5_5_xhigh,kimi_k2_6,gpt_5_5`.
- Run `grok_4_20` as sensitivity only.
- Keep archived Gemini and failed Opus smoke output out of all refreshed primary aggregation.
- Default scorer raters resolve to the approved primary triple; Opus and Grok remain explicit opt-in raters.
- Snapshot current outputs outside the repo before any generated output overwrite.
- Build only from clean run directories that contain the selected rater JSONL files.
- Restore primary triple outputs after sensitivity build so committed data reflects the publication baseline.

## Files and artifacts

Repo files expected to change:

- `src/drift/score.py`
- `data/capability_2026.csv`
- `data/has_drift_2026.csv`
- `data/drift_summary.csv`
- `data/calibrators/*`
- `reports/*.md`
- `paper.md`
- `findings.md`
- `dashboard/public/data.json`
- `article-assets/*`

Generated run directories:

- `runs/raters/smoke_20260707_codex_triple`
- `runs/raters/rerun_20260707_triple`
- `runs/raters/rerun_20260707_grok_only`
- `runs/raters/rerun_20260707_triple_plus_grok`

External audit archive:

- `/Users/sam/.codex/tmp/workbank-rerun-20260707/baseline/`
- `/Users/sam/.codex/tmp/workbank-rerun-20260707/primary/`
- `/Users/sam/.codex/tmp/workbank-rerun-20260707/sensitivity/`

## Acceptance criteria

- Baseline files copied outside repo before generated output overwrite.
- Codex OAuth auth exists in `/Users/sam/.codex/auth.json` without printing secret values.
- `.env` contains `OPENAI_API_KEY` and `OPENROUTER_API_KEY` without printing secret values.
- Raw WORKBank files have expected row counts: metadata 2131, expert ratings 2057, worker desires 5731.
- Smoke run produces 3 valid rows for each primary rater with no JSON parse errors.
- Primary run produces 844 valid rows for each primary rater.
- Resume logic treats error rows as incomplete, matching aggregation behavior.
- Primary `data/capability_2026.csv` has 844 rows and no `gemini_3_pro` rater column.
- `data/drift_summary.csv` counts sum to 844.
- Sensitivity output is copied outside repo, then primary outputs are restored to `data/`.
- Claim files match primary CSV-derived statistics.
- Runtime checks pass:
  - `python3 scripts/verify_streamlit_proof.py`
  - `python3 -m py_compile streamlit_app.py`

## Risks and mitigations

- API model ID failure: stop after smoke run, update this spec before model substitution.
- Codex CLI overhead: use an isolated `CODEX_HOME` copied from `/Users/sam/.codex/auth.json`, low concurrency, batch 8 tasks per `codex_gpt_5_5_xhigh` invocation, and hard-kill timed-out child processes.
- OpenRouter latency: keep default concurrency at 8, allow `OPENROUTER_RATER_CONCURRENCY` during rerun resume if Kimi becomes the bottleneck, and use explicit API timeouts.
- Anthropic auth mismatch: Opus is no longer in the refreshed primary triple because Sam approved Codex OAuth GPT-5.5 xhigh replacement.
- API billing or rate limits: use explicit run IDs and resumable append mode.
- Archived rater contamination: build from clean run directories only.
- Dirty worktree collision: preserve baseline outside repo and avoid touching unrelated dirty files.
- Thesis drift: flag any headline swing over 2 percentage points, any migration bucket swing over 10 tasks, or calibration gate failure before publishing.
