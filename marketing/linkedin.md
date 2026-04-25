# LinkedIn post — 300 words

**WORKBank Drift 2026: what one year did to AI capability on real jobs**

Stanford SALT Lab published WORKBank in mid-2025 — a database of 844 occupational tasks across 104 U.S. occupations, scored on two axes: how much workers want AI to help with each task, and how capable AI agents are at doing it. Their headline framework split tasks into four zones: Green Light (workers want it, AI can do it), Red Light (AI can do it, workers don't want it), R&D Opportunity (workers want it, AI can't yet), and Low Priority (neither).

I recomputed the capability axis against the April-2026 frontier — Claude Opus 4.7, Kimi K2.6, GPT-5.5 — held worker desire fixed at its 2025 value, and looked at what migrated.

**The framework collapsed.**

In 2025, 75% of tasks scored above the capability threshold. In April 2026, **97.6%** do. The R&D Opportunity zone dropped from 107 tasks to 12. Low Priority dropped from 106 to 8.

24% of tasks moved zones. Two flows dominate: 98 tasks moved from R&D Opportunity to Green Light (workers wanted help, capability now arrived), and 102 moved from Low Priority to Red Light (workers didn't want help, capability arrived anyway).

The Low → Red bucket touches 9.4 million U.S. workers and roughly $850B in annual wage bill. It's 65.5% female-weighted, mostly clerical and scheduling work.

The original paper's "41% of YC startups target misaligned tasks" finding still holds numerically — but the composition flipped. In 2026 it's almost entirely Red Light targeting (feasible but undesired), not Low Priority (infeasible). The Red+Low composite metric no longer distinguishes those two cases.

Capability is not deployment. This is a feasibility claim, not a displacement estimate.

Repo + paper + dashboard: [link]
