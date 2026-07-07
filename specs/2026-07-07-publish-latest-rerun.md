# Publish latest WORKBank rerun spec

Date: 2026-07-07
Scope: L

## Objective

Publish the refreshed WORKBank rerun outputs and Codex OAuth scorer changes to the GitHub repository.

## Approach

- Commit the current rerun artifacts produced by `specs/2026-07-07-rerun-postmortem-analysis.md`.
- Include the local proof app files already referenced by the updated README.
- Keep `runs/` and external audit archives out of git.
- Push the current branch to `origin` because Sam requested the repo be updated with the latest.

## Files

- `src/drift/score.py`: Codex OAuth GPT-5.5 xhigh rater and default primary triple.
- `data/*.csv`, `data/calibrators/*`: refreshed primary outputs.
- `reports/*.md`, `paper.md`, `findings.md`, `README.md`, `METHODOLOGY.md`: refreshed claims and protocol text.
- `dashboard/index.html`, `dashboard/public/data.json`: refreshed dashboard payload and copy.
- `article-assets/*`, `marketing/*`: refreshed publication assets.
- `streamlit_app.py`, `scripts/verify_streamlit_proof.py`, `pyproject.toml`, `uv.lock`: proof app surface and dependency lockfile.
- `specs/*`: audit and publish specs.

## Acceptance criteria

- No API secrets are staged.
- `git diff --check` passes.
- `data/capability_2026.csv` has 844 data rows.
- `data/drift_summary.csv` counts sum to 844.
- Primary CSV has no `gemini_3_pro`, `grok_4_20`, or `opus_4_7` rater columns.
- `python3 scripts/verify_streamlit_proof.py` passes.
- `python3 -m py_compile streamlit_app.py src/drift/score.py` passes.
- Commit uses Conventional Commits.
- Push to `origin/master` succeeds.

## Risks

- Unrelated dirty files could be swept into the commit. Mitigation: inspect status and only stage the rerun, proof app, and documentation surfaces listed above.
- Secrets could leak through auth or environment files. Mitigation: scan staged paths for known key and token patterns before commit.
- Generated JSON formatting could create noisy diffs. Mitigation: compact dashboard JSON before staging.
- Pushing to `master` updates the public repository. Mitigation: Sam explicitly requested updating the repo with the latest.
