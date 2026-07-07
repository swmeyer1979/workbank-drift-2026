# Benchmark anchor audit (primary 844-task rerun)

Each rater is asked to cite benchmark anchors used to ground its score. An empty list means the rater used no anchor and the score is a zero-shot judgment from priors.

## Empty-anchor rate per rater

| rater | n | empty list | empty % | llm_inferred=true |
|---|---:|---:|---:|---:|
| codex_gpt_5_5_xhigh | 844 | 29 | 3.4% | 5.6% |
| kimi_k2_6 | 844 | 610 | 72.3% | 73.2% |
| gpt_5_5 | 844 | 35 | 4.1% | 8.2% |

## Top anchors cited per rater

### codex_gpt_5_5_xhigh

- osworld_verified: 471
- gaia: 419
- webarena: 413
- mmmlu: 184
- mmlu_pro: 130
- gpqa_diamond: 88
- swe_bench_verified: 76
- swe_bench_pro: 48
- humaneval_plus: 14
- livecodebench_pro: 13

### kimi_k2_6

- osworld_verified: 142
- webarena: 108
- swe_bench_verified: 84
- swe_bench_pro: 47
- gaia: 44
- gpqa_diamond: 19
- aime_2025: 3
- humanitys_last_exam: 2
- mmmlu: 2
- livecodebench_pro: 1

### gpt_5_5

- osworld_verified: 618
- webarena: 459
- gaia: 387
- mmmlu: 256
- mmlu_pro: 242
- gpqa_diamond: 124
- swe_bench_verified: 114
- swe_bench_pro: 90
- livecodebench_pro: 25
- aime_2025: 10

## Confidence distribution

| rater | low | medium | high |
|---|---:|---:|---:|
| codex_gpt_5_5_xhigh | 24 | 540 | 280 |
| kimi_k2_6 | 622 | 160 | 62 |
| gpt_5_5 | 33 | 620 | 191 |

## Reading guide

- A high empty-anchor rate means the rater is judging from priors instead of benchmark evidence.
- High `llm_inferred=true` means the rater self-flagged that no benchmark applied to the task family.
- The Berkeley RDI 2026 caveat applies: agent-family anchors are upper bounds, not validated capability proofs.
