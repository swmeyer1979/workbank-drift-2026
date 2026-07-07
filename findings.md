# WORKBank Drift 2026 - One-page findings

Stanford SALT Lab's WORKBank (Shao et al., 2025) classified 844 occupational tasks across 104 U.S. occupations into four zones by worker-desire × AI-capability, scored against the early-2025 frontier. We recompute the capability axis against the 2026 primary ensemble (Codex OAuth GPT-5.5 xhigh, Kimi K2.6, OpenAI GPT-5.5), hold worker desire fixed at its 2025 value, and report the migrations.

## Headline

- **97.3% of 844 tasks score capability >= 3 in 2026** [bootstrap 95% CI: 96.1%, 98.3%], up from 75% in 2025.
- **24% of tasks (200/844) migrate zones** [CI: 177, 225]. R&D Opportunity moves 107 → 16; Low Priority moves 106 → 7.
- Two flows account for 195 of the 200 migrations: **94 tasks R&D → Green Light** (workers wanted help, capability arrived), **101 tasks Low Priority → Red Light** (workers did not want help, capability arrived anyway).
- Both cross-zone flows are far above a permutation null (p < 0.001).
- The four-zone framework mostly collapses to two populated zones at the original 3.0 cutoff. At c = 3.25, R&D and Low Priority repopulate; the framework is threshold-sensitive.
- Inter-human κ_linear = 0.833; ensemble-vs-consensus κ_linear = 0.554 [0.338, 0.734]. Refreshed agentic spot-check correlation: ρ = 0.469 (p = 0.0368) between predicted capability and preserved agent grade on n = 20.

## Top 10 tasks: R&D Opportunity → Green Light

Tasks workers wanted automated in 2025 where 2025 capability was insufficient. 2026 capability now clears the 3.0 threshold.

| Δ | occupation | task |
|---:|---|---|
| +2.7 | Video Game Designers | Create and manage documentation, production schedules, prototyping goals |
| +2.5 | Network and Computer Systems Administr | Perform data backups and disaster recovery operations. |
| +2.5 | Sales Representatives, Wholesale and M | Prepare sales presentations or proposals to explain product specificatio |
| +2.5 | Clinical Research Coordinators | Schedule subjects for appointments, procedures, or inpatient stays as re |
| +2.5 | Clinical Data Managers | Track the flow of work forms, including in-house data flow or electronic |
| +2.5 | Regulatory Affairs Managers | Maintain current knowledge of relevant regulations, including proposed a |
| +2.5 | Judicial Law Clerks | Verify that all files, complaints, or other papers are available and in  |
| +2.2 | Production, Planning, and Expediting C | Calculate figures, such as required amounts of labor or materials, manuf |
| +2.2 | Production, Planning, and Expediting C | Distribute production schedules or work orders to departments. |
| +2.0 | Art Directors | Mark up, paste, and complete layouts and write typography instructions t |

## Top 10 tasks: Low Priority → Red Light

Tasks where worker desire was below threshold and 2025 capability was below threshold. 2026 capability has crossed; desire has not.

| Δ | occupation | task |
|---:|---|---|
| +3.0 | Secretaries and Administrative Assista | Complete forms in accordance with company procedures. |
| +2.3 | Secretaries and Administrative Assista | Locate and attach appropriate files to incoming correspondence requiring |
| +2.0 | Medical Secretaries and Administrative | Schedule and confirm patient diagnostic appointments, surgeries, or medi |
| +2.0 | Computer Systems Analysts | Expand or modify system to serve new purposes or improve work flow. |
| +2.0 | Reservation and Transportation Ticket  | Assemble and issue required documentation, such as tickets, travel insur |
| +2.0 | Sales Representatives, Wholesale and M | Quote prices, credit terms, or other bid specifications. |
| +2.0 | Production, Planning, and Expediting C | Requisition and maintain inventories of materials or supplies necessary  |
| +2.0 | Production, Planning, and Expediting C | Establish and prepare product construction directions and locations and  |
| +2.0 | Information Technology Project Manager | Develop and manage work breakdown structure (WBS) of information technol |
| +2.0 | Secretaries and Administrative Assista | Compose, type, and distribute meeting notes, routine correspondence, or  |

## Net zone-population shift

| zone | 2025 | 2026 | change |
|---|---:|---:|---:|
| Green Light | 364 | 455 | +91 |
| Red Light | 267 | 366 | +99 |
| R&D Opportunity | 107 | 16 | -91 |
| Low Priority | 106 | 7 | -99 |

## Wage and demographic exposure

- Low → Red: 52 occupations, 9.4M U.S. workers, ~$850B annual wage bill. **65.5% female-weighted** vs 47% workforce baseline.
- R&D → Green: 46 occupations, 5.7M workers, ~$571B wage bill. 51.0% female-weighted across the matched CPS subset.
- Concentration in the Low → Red bucket: clerical, secretarial, scheduling, network/IT support, and routine-cognitive task families.

## YC startup mapping recompute

The upstream paper found 41% of YC company-task targeting in Red+Low zones in 2025. Under 2026 capability, the share is **unchanged at 41.2%**, but the composition flipped: Low Priority dropped 11.8% → 0.4%, Red Light grew 29.4% → 40.7%. The original Red+Low composite metric no longer distinguishes low-desire feasible work from low-desire infeasible work.

## Limitations to read before citing

- Two-rater calibration with n = 50; lower bootstrap CI of ensemble κ overlaps the pre-registered 0.4 gate.
- Rubric was iterated against the calibration set; a fresh confirmatory n >= 30 sample remains the publication-grade next step.
- LLM-as-judge self-grading prior; agentic spot-check is a partial mitigation and is author-graded.
- Capability is not deployment. The Low → Red headline is a feasibility claim, not a displacement estimate.
- Worker desire is held at its 2025 value by design; 2026 preferences may have shifted.
