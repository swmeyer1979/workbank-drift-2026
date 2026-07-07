# Zone-migration significance - permutation test

Null: 2026 capability deltas randomly reassigned across tasks, preserving the marginal delta distribution but breaking task-level pairing. 5000 permutations, two-sided empirical p-values.

## Per-cell migration counts vs null

| migration | observed | null mean | null 95% range | two-sided p |
|---|---:|---:|---|---:|
| R&D->Green | 94 | 36.3 | [27, 46] | <0.001 *** |
| Low->Red | 101 | 36.7 | [28, 45] | <0.001 *** |
| Green->R&D | 3 | 44.3 | [34, 55] | <0.001 *** |
| Red->Low | 2 | 43.5 | [34, 54] | <0.001 *** |
| Green->Green | 361 | 319.7 | [309, 330] | <0.001 *** |
| Red->Red | 265 | 223.5 | [213, 233] | <0.001 *** |
| R&D->R&D | 13 | 70.7 | [61, 80] | <0.001 *** |
| Low->Low | 5 | 69.3 | [61, 78] | <0.001 *** |

## Reading guide

- Small p tests whether the observed migration count is unusual given random delta reassignment.
- The cross-zone cells R&D->Green and Low->Red are the policy-relevant cells.
- Reverse flows are also far from the null, in the opposite direction: capability rarely moved down enough to repopulate the old below-threshold zones.
