# Streamlit Data Product Proof Spec

## Objective

Add a recruiter-visible Streamlit app over existing WORKBank drift outputs to demonstrate web/data-product depth.

## Files

- `README.md`
- `streamlit_app.py`
- `scripts/verify_streamlit_proof.py`
- `specs/2026-05-21-streamlit-proof.md`

## Acceptance Criteria

- App reads existing derivative CSV files.
- App exposes occupation, migration, and near-threshold filters.
- Verification script imports helper functions without requiring Streamlit.
- No existing dirty dependency files are modified.
- Claims remain limited to the study data already present in this repo.

## Risks

- Streamlit dependency may be absent locally.
- Dashboard could be mistaken for deployment evidence.
- Dirty repo already has unrelated edits.

## Verification

- `python3 scripts/verify_streamlit_proof.py`
- `python3 -m py_compile streamlit_app.py`
- Optional runtime: `streamlit run streamlit_app.py`
