# YC mapping recompute under 2026 zones

Upstream finding (Shao et al. 2025): **41% of YC startup company-task mappings sat in Red Light + Low Priority zones in 2025** — i.e., startups were targeting tasks where worker desire was low or capability was insufficient.
Recomputed here with 2026 capability and **fixed 2025 desire**.

Matched 841/2076 YC mapping rows by (task, occupation) join. Unmatched rows had no capability score in our 844-task table.

**Total YC company-task pairs in matched data:** 106,947

## Zone share, 2025 vs 2026 (weighted by company-task count)

| zone | 2025 | 2026 |
|---|---:|---:|
| Green Light | 45.6% | 57.6% |
| Red Light | 29.4% | 40.7% |
| R&D Opportunity | 13.2% | 1.2% |
| Low Priority | 11.8% | 0.5% |

## Misalignment (Red Light + Low Priority share)

| year | share |
|---|---:|
| 2025 (recomputed from mapping data) | 41.2% |
| 2026 (under 2026 capability) | 41.2% |
| Upstream paper claim, 2025 | 41% |

## Interpretation

**Headline:** the upstream paper's 41% misalignment claim *holds* under 2026 capability — the headline number is unchanged. But the composition flipped: Low Priority dropped 11.8% → 0.5% (-95%); Red Light grew 29.4% → 40.7% (+39%). Low→Red migration consumed the entire Low Priority sub-bucket of YC targeting.

**Implication:** under 2025 capability, "41% of YC mappings are in Red+Low" was a statement about a heterogeneous population — startups targeting both impossible tasks (Low) and unwanted-but-feasible tasks (Red). Under 2026 capability, it's a homogeneous claim — startups are predominantly targeting feasible-but-low-desire tasks (Red Light, 40.7%). The ratio held, but the meaning changed.
- The change is concentrated in the **Low Priority → Red Light** flow: capability rose into low-desire task space without changing alignment.
- The original Red+Low composite metric **no longer distinguishes "misaligned" from "well-aligned"** under 2026 capability — it conflates the (high-cap, low-desire) Red Light bucket with the (low-cap, low-desire) Low Priority bucket. Splitting the two is now informative.

## Caveats

- The 41% upstream figure is computed over a different denominator (YC company → workflow → task chain). Our recompute uses the published `company_to_workflow_aggregation.csv` and matches on (task, occupation). Direct comparability is approximate.
- Results held under fixed 2025 worker desire — actual 2026 worker desire may differ.