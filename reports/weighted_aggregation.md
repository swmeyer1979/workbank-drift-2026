# Importance-weighted zone aggregation

Tasks weighted by `Importance × Frequency × Relevance` from upstream task metadata. This adjusts for the fact that not all tasks are equally central to an occupation.

**Coverage:** 844/844 tasks have all three weight components.

## Zone share - unweighted vs importance-weighted

| zone | unweighted % | weighted % (Imp×Freq×Rel) |
|---|---:|---:|
| Green Light | 53.9% | 52.6% |
| Red Light | 43.4% | 44.4% |
| R&D Opportunity | 1.9% | 1.9% |
| Low Priority | 0.8% | 1.1% |

## Migration share - unweighted vs weighted

| migration | unweighted count | unweighted % | weighted % |
|---|---:|---:|---:|
| Green->Green | 361 | 42.8% | 42.7% |
| Red->Red | 265 | 31.4% | 32.7% |
| Low->Red | 101 | 12.0% | 11.7% |
| R&D->Green | 94 | 11.1% | 9.9% |
| R&D->R&D | 13 | 1.5% | 1.6% |
| Low->Low | 5 | 0.6% | 0.7% |
| Green->R&D | 3 | 0.4% | 0.4% |
| Red->Low | 2 | 0.2% | 0.4% |

## Reading guide

- If a migration class has weighted % above unweighted %, those tasks are more central or frequent than average.
- If weighted % is lower, the tasks are comparatively peripheral under the upstream task metadata.
