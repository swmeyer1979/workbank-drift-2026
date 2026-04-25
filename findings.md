# WORKBank Drift 2026 — One-page findings

Stanford SALT Lab's WORKBank (Shao et al., 2025) classified 844 occupational tasks across 104 U.S. occupations into four zones by worker-desire × AI-capability, scored against the early-2025 frontier. We recompute the capability axis against an April-2026 ensemble (Claude Opus 4.7, Kimi K2.6, GPT-5.5), hold worker desire fixed at its 2025 value, and report the migrations.

## Headline

- **97.6% of 844 tasks score capability ≥ 3 in 2026** [bootstrap 95% CI: 96.6%, 98.6%], up from 75% in 2025.
- **24% of tasks (205/844) migrate zones** [CI: 180, 230]. R&D Opportunity collapses 107 → 12; Low Priority 106 → 8.
- Two flows account for 199 of the 205 migrations: **98 tasks R&D → Green Light** (workers wanted help, capability arrived), **102 tasks Low Priority → Red Light** (workers did not want help, capability arrived anyway).
- Both cross-zone flows are 2.6× higher than a permutation null (p < 0.001).
- The four-zone framework collapses to two populated zones at the original 3.0 cutoff. At c = 3.25, R&D and Low Priority repopulate; the framework is threshold-sensitive.
- Inter-human κ_linear = 0.834; ensemble-vs-consensus κ_linear = 0.526 [0.321, 0.703]. Agentic spot-check: ρ = 0.488 (p = 0.029) between predicted capability and realized agent grade on n = 20.

## Top 10 tasks: R&D Opportunity → Green Light

Tasks workers wanted automated in 2025 where 2025 capability was insufficient. 2026 capability now clears the 3.0 threshold.

| Δ | occupation | task |
|---:|---|---|
| +2.7 | Video Game Designers | Create and manage documentation, production schedules, prototyping goals, and co |
| +2.5 | Clinical Data Managers | Track the flow of work forms, including in-house data flow or electronic forms t |
| +2.5 | Judicial Law Clerks | Verify that all files, complaints, or other papers are available and in the prop |
| +2.5 | Appraisers and Assessors of Real Es | Search public records for transactions such as sales, leases, and assessments. |
| +2.5 | Sales Representatives, Wholesale an | Prepare sales presentations or proposals to explain product specifications or ap |
| +2.5 | Regulatory Affairs Managers | Maintain current knowledge of relevant regulations, including proposed and final |
| +2.3 | Medical Secretaries and Administrat | Perform various clerical or administrative functions, such as ordering and maint |
| +2.2 | Production, Planning, and Expeditin | Calculate figures, such as required amounts of labor or materials, manufacturing |
| +2.2 | Production, Planning, and Expeditin | Distribute production schedules or work orders to departments. |
| +2.0 | Computer and Information Systems Ma | Stay abreast of advances in technology. |

## Top 10 tasks: Low Priority → Red Light

Tasks where worker desire was below threshold and 2025 capability was below threshold. 2026 capability has crossed; desire has not.

| Δ | occupation | task |
|---:|---|---|
| +3.0 | Secretaries and Administrative Assi | Complete forms in accordance with company procedures. |
| +3.0 | Reservation and Transportation Tick | Assemble and issue required documentation, such as tickets, travel insurance pol |
| +2.2 | Secretaries and Administrative Assi | Use computers for various applications, such as database management or word proc |
| +2.0 | Medical Secretaries and Administrat | Schedule and confirm patient diagnostic appointments, surgeries, or medical cons |
| +2.0 | Sales Representatives, Wholesale an | Quote prices, credit terms, or other bid specifications. |
| +2.0 | Production, Planning, and Expeditin | Requisition and maintain inventories of materials or supplies necessary to meet  |
| +2.0 | Production, Planning, and Expeditin | Establish and prepare product construction directions and locations and informat |
| +2.0 | Information Technology Project Mana | Develop and manage work breakdown structure (WBS) of information technology proj |
| +2.0 | Human Resources Specialists | Schedule or administer skill, intelligence, psychological, or drug tests for cur |
| +2.0 | Computer Network Support Specialist | Configure wide area network (WAN) or local area network (LAN) routers or related |

## Net zone-population shift

| zone | 2025 | 2026 | change |
|---|---:|---:|---:|
| Green Light | 364 | 459 | +95 |
| Red Light | 267 | 367 | +100 |
| R&D Opportunity | 107 | 12 | -95 |
| Low Priority | 106 | 6 | -100 |

## Wage and demographic exposure

- Low → Red: 52 occupations, 9.4M U.S. workers, ~$850B annual wage bill. **65.5% female-weighted** vs 47% workforce baseline.
- R&D → Green: 48 occupations, 5.8M workers, ~$580B wage bill. 51.4% female-weighted.
- Concentration in the Low → Red bucket: clerical, secretarial, scheduling, network/IT support — the routine-cognitive task families.

## YC startup mapping recompute

The upstream paper found 41% of YC company-task targeting in Red+Low zones in 2025. Under 2026 capability, the share is **unchanged at 41.2%** but the composition flipped: Low Priority dropped 11.8% → 0.5%, Red Light grew 29.4% → 40.7%. The original Red+Low composite metric no longer distinguishes "misaligned" from "feasible-but-unwanted" startup targeting.

## Limitations to read before citing

- Two-rater calibration with n = 50; lower bootstrap CI of ensemble κ overlaps the pre-registered 0.4 gate.
- Rubric was iterated against the calibration set; a fresh confirmatory n ≥ 30 sample is documented as a required next step.
- LLM-as-judge self-grading prior; agentic spot-check is the partial mitigation but is itself author-graded.
- Capability ≠ deployment. The Low → Red headline is a feasibility claim, not a displacement estimate.
- Worker desire is held at its 2025 value by design; 2026 preferences may have shifted.