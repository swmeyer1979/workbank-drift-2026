# Benchmark anchor audit (full 844-task run)

Each rater is asked to cite the benchmark anchors used to ground its score. An empty list means the rater used no anchor — score is essentially a zero-shot judgment unmoored from published benchmarks.

## Empty-anchor rate per rater

| rater | n | empty list | empty % | llm_inferred=true |
|---|---:|---:|---:|---:|
| opus_4_7 | 844 | 19 | 2.3% | 57.7% |
| kimi_k2_6 | 844 | 600 | 71.1% | 73.5% |
| gpt_5_5 | 844 | 31 | 3.7% | 8.2% |

## Top anchors cited per rater

### opus_4_7

- osworld_verified: 401
- mmlu_pro: 392
- webarena: 239
- swe_bench_verified: 186
- gaia: 160
- gpqa_diamond: 133
- mmmlu: 74
- swe_bench_pro: 56

### kimi_k2_6

- osworld_verified: 152
- webarena: 92
- swe_bench_verified: 87
- swe_bench_pro: 51
- gaia: 38
- gpqa_diamond: 24
- mmmlu: 8
- livecodebench_pro: 2

### gpt_5_5

- osworld_verified: 634
- webarena: 454
- gaia: 371
- mmmlu: 277
- mmlu_pro: 266
- gpqa_diamond: 122
- swe_bench_verified: 115
- swe_bench_pro: 90

## Confidence distribution

| rater | low | medium | high |
|---|---:|---:|---:|
| opus_4_7 | 9 | 628 | 207 |
| kimi_k2_6 | 619 | 157 | 68 |
| gpt_5_5 | 30 | 631 | 183 |

## Reading guide

- A rater with high empty-anchor % is functionally unanchored — it scored from priors not from benchmark evidence.
- High `llm_inferred=true` rate is the rater self-flagging that no benchmark applied to the task family.
- The Berkeley RDI 2026 caveat applies: agent-family anchors (SWE-bench, OSWorld, WebArena, GAIA) are upper bounds, not validated capability proofs.