# Zone-migration significance — permutation test (revised)

Null: 2026 capability deltas randomly reassigned across tasks (preserves the marginal delta distribution but breaks task-level pairing). 5000 permutations, two-sided p-values.

## Per-cell migration counts vs null

| migration | observed | null mean | null 95% range | two-sided p |
|---|---:|---:|---|---:|
| R&D->Green | 98 | 37 | [29, 47] | 0.0000 *** |
| Low->Red | 101 | 38 | [29, 47] | 0.0000 *** |
| Green->R&D | 3 | 42 | [32, 52] | 0.0000 *** |
| Red->Low | 3 | 41 | [32, 51] | 0.0000 *** |
| Green->Green | 361 | 322 | [312, 332] | 0.0000 *** |
| Red->Red | 264 | 226 | [216, 235] | 0.0000 *** |
| R&D->R&D | 9 | 70 | [60, 78] | 0.0000 *** |
| Low->Low | 5 | 68 | [59, 77] | 0.0000 *** |

## Reading guide

- Small p tests whether the observed migration count is unusual given random delta reassignment, in either direction.
- Big stable cells (Green→Green, Red→Red) usually show no significance — they're anchored by the desire axis and small capability deltas.
- The cross-zone cells (R&D→Green, Low→Red) are the policy-relevant ones; their significance vs null is the substantive question.