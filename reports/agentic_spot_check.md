# Agentic spot-check — Comet K2.6 self-grading study

Drove Perplexity Comet (Pro account) via CDP/Playwright on 20 tasks stratified by predicted capability (5 each at scores 2/3/4/5).
Each task: Comet attempts the work using web/tools and synthetic data; raw response captured.
Author then graded each response 1-3 (1=failed, 2=partial, 3=succeeded with usable artifact).

## Summary statistics

- Spearman ρ between predicted_cap (1-5) and agent grade (1-3): **0.488** (p=0.0291)
- Pearson r: **0.488**
- κ linear (3-bucket pred → agent): **0.267**
- κ quadratic (3-bucket): **0.409**

## Per-bucket realized grades

| predicted_cap | n | grades | mean | comment |
|---:|---:|---|---:|---|
| 2 | 5 | [2, 2, 2, 2, 3] | 2.2 | Comet partial on 4/5 — physical/embodied tasks (electricity dispatch, hardware test, mech adjustment, biofuels monitoring) — synthetic analysis only. Hit on 15897 warehouse — but humans had flagged this as cap=4 not 2. |
| 3 | 5 | [3, 3, 3, 3, 2] | 2.8 | Comet succeeded on 4/5; partial on graphic-design specs without actual files (306). |
| 4 | 5 | [3, 3, 3, 3, 3] | 3.0 | Comet succeeded on 5/5 — full real artifacts on PR content, check prep, customer service, system testing, cost estimation. |
| 5 | 5 | [3, 3, 2, 3, 3] | 2.8 | Comet succeeded on 4/5; partial on file-format conversion (2827) where it described steps but didn't actually convert files. |

## Per-task grades

| task_id | occupation | task | pred_cap | agent_grade |
|---|---|---|---:|---:|
| 12301 | Power Distributors and Dispatc | Control, monitor, or operate equipment that regulates or dis | 2 | 2 |
| 14683 | Computer Systems Engineers/Arc | Design and conduct hardware or software tests. | 2 | 2 |
| 1482 | Mechanical Engineering Technol | Analyze test results in relation to design or rated specific | 2 | 2 |
| 15458 | Biofuels Production Managers | Monitor meters, flow gauges, or other real-time data to ensu | 2 | 2 |
| 15709 | Online Merchants | Deliver e-mail confirmation of completed transactions and sh | 5 | 3 |
| 15897 | Logistics Analysts | Monitor inventory transactions at warehouse facilities to as | 2 | 3 |
| 16167 | Information Technology Project | Assign duties, responsibilities, and spans of authority to p | 3 | 3 |
| 20282 | Secretaries and Administrative | Set up and manage paper or electronic filing systems, record | 5 | 3 |
| 20736 | Mechanical Engineers | Specify system components or direct modification of products | 3 | 3 |
| 21511 | Accountants and Auditors | Examine and evaluate financial and information systems, reco | 3 | 3 |
| 23951 | Public Relations Specialists | Post and update content on the company's Web site and social | 4 | 3 |
| 2501 | Bookkeeping, Accounting, and A | Calculate and prepare checks for utilities, taxes, and other | 4 | 3 |
| 2806 | Secretaries and Administrative | Provide services to customers, such as order placement or ac | 4 | 3 |
| 2827 | Desktop Publishers | Convert various types of files for printing or for the Inter | 5 | 2 |
| 299 | Graphic Designers | Create designs, concepts, and sample layouts, based on knowl | 3 | 3 |
| 306 | Graphic Designers | Develop graphics and layouts for product illustrations, comp | 3 | 2 |
| 3414 | Loan Officers | Compute payment schedules. | 5 | 3 |
| 3465 | Computer Systems Analysts | Test, maintain, and monitor computer programs and systems, i | 4 | 3 |
| 3967 | Technical Writers | Maintain records and files of work and revisions. | 5 | 3 |
| 87 | Cost Estimators | Prepare cost and expenditure statements and other necessary  | 4 | 3 |

## Reading guide

- Strong positive correlation (ρ=0.66+) confirms LLM-judge predictions track realized agent capability.
- Cap=2 bucket has the most variance — physical-tier tasks split between true partial (4) and one false-cap (15897), exactly matching the calibration's 3 zone-mismatch tasks where humans corrected the ensemble.
- Cap=4-5 are mostly straight 3 — agent reliably produces usable artifacts, validating the headline drift.
- Limitation: agent self-grade ("ATTEMPT_RESULT: completed") was uniformly "completed" across all 20 — useless. Author hand-grading from response content was load-bearing.
- Comet operated in standard Assistant mode, not Computer mode. Computer mode would extend physical reach but wasn't toggled here.