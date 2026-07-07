# YC mapping recompute under 2026 zones

Upstream finding (Shao et al. 2025): **41% of YC startup company-task mappings sat in Red Light + Low Priority zones in 2025**.

Recomputed here with 2026 capability and fixed 2025 desire. Matched 841/2076 YC mapping rows by task and occupation join. Unmatched rows had no capability score in the 844-task table.

**Total YC company-task pairs in matched data:** 106,947

## Zone share, 2025 vs 2026 (weighted by company-task count)

| zone | 2025 | 2026 |
|---|---:|---:|
| Green Light | 45.6% | 57.3% |
| Red Light | 29.4% | 40.7% |
| R&D Opportunity | 13.2% | 1.6% |
| Low Priority | 11.8% | 0.4% |

## Misalignment (Red Light + Low Priority share)

| year | share |
|---|---:|
| 2025 (recomputed from mapping data) | 41.2% |
| 2026 (under 2026 capability) | 41.2% |
| Upstream paper claim, 2025 | 41% |

## Interpretation

The upstream 41% misalignment claim holds numerically under 2026 capability. The composition flipped: Low Priority dropped from 11.8% to 0.4%, while Red Light grew from 29.4% to 40.7%. Low->Red migration consumed nearly the entire Low Priority sub-bucket of YC targeting.

The Red+Low composite metric now hides the distinction between infeasible low-desire work and feasible low-desire work. Splitting Red and Low is now load-bearing.

## Caveats

- The 41% upstream figure is computed over a different denominator. This recompute uses the published `company_to_workflow_aggregation.csv` and matches on task and occupation. Direct comparability is approximate.
- Results hold worker desire fixed at its 2025 value.
