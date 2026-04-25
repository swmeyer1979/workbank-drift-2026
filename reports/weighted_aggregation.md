# Importance-weighted zone aggregation

Tasks weighted by `Importance × Frequency × Relevance` from upstream task metadata. This adjusts for the fact that not all tasks are equally central to an occupation.

**Coverage:** 844/844 tasks have all three weight components (others dropped).

## Zone share — unweighted vs importance-weighted

| zone | unweighted % | weighted % (Imp×Freq×Rel) |
|---|---:|---:|
| Green Light | 54.4% | 53.0% |
| Red Light | 43.2% | 44.3% |
| R&D Opportunity | 1.4% | 1.5% |
| Low Priority | 0.9% | 1.2% |

## Migration share — unweighted vs weighted

| migration | unweighted count | unweighted % | weighted % |
|---|---:|---:|---:|
| Green->Green | 361 | 42.8% | 42.7% |
| Red->Red | 264 | 31.3% | 32.6% |
| Low->Red | 101 | 12.0% | 11.6% |
| R&D->Green | 98 | 11.6% | 10.3% |
| R&D->R&D | 9 | 1.1% | 1.1% |
| Low->Low | 5 | 0.6% | 0.7% |
| Green->R&D | 3 | 0.4% | 0.4% |
| Red->Low | 3 | 0.4% | 0.5% |

## Reading guide

- If a migration class has weighted % > unweighted %, those tasks are more central/frequent than average — reweighting amplifies their importance.
- Conversely, if weighted < unweighted, tasks are peripheral.