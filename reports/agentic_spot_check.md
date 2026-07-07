# Agentic spot-check - Comet K2.6 self-grading study

Status: browser run preserved from the prior analysis; agent outcomes were not rerun on 2026-07-07. Predicted capability buckets below are refreshed from the Codex OAuth GPT-5.5 xhigh primary CSV.

Drove Perplexity Comet (Pro account) via CDP/Playwright on 20 tasks stratified by predicted capability. Each task: Comet attempted the work using web/tools and synthetic data; raw response captured. Author then graded each response 1-3 (1=failed, 2=partial, 3=succeeded with usable artifact).

## Summary statistics

- Spearman ρ between refreshed predicted_cap (1-5) and agent grade (1-3): **0.469** (p=0.0368)
- Pearson r: **0.450** (p=0.0467)
- κ linear (3-bucket pred -> agent): **0.221**
- κ quadratic (3-bucket): **0.375**

## Per-bucket realized grades

| predicted_cap | n | grades | mean | comment |
|---:|---:|---|---:|---|
| 2 | 5 | [2, 2, 2, 2, 3] | 2.2 | Physical/embodied tasks mostly partial; one warehouse inventory task succeeded. |
| 3 | 6 | [3, 3, 3, 3, 3, 2] | 2.8 | Preserved agent outcomes; refreshed predicted capability. |
| 4 | 5 | [3, 3, 3, 3, 3] | 3.0 | All tasks succeeded with usable artifacts. |
| 5 | 4 | [3, 2, 3, 3] | 2.8 | Preserved agent outcomes; refreshed predicted capability. |

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
| 20282 | Secretaries and Administrative | Set up and manage paper or electronic filing systems, record | 4 | 3 |
| 20736 | Mechanical Engineers | Specify system components or direct modification of products | 3 | 3 |
| 21511 | Accountants and Auditors | Examine and evaluate financial and information systems, reco | 3 | 3 |
| 23951 | Public Relations Specialists | Post and update content on the company's Web site and social | 4 | 3 |
| 2501 | Bookkeeping, Accounting, and A | Calculate and prepare checks for utilities, taxes, and other | 3 | 3 |
| 2806 | Secretaries and Administrative | Provide services to customers, such as order placement or ac | 4 | 3 |
| 2827 | Desktop Publishers | Convert various types of files for printing or for the Inter | 5 | 2 |
| 299 | Graphic Designers | Create designs, concepts, and sample layouts, based on knowl | 3 | 3 |
| 306 | Graphic Designers | Develop graphics and layouts for product illustrations, comp | 3 | 2 |
| 3414 | Loan Officers | Compute payment schedules. | 5 | 3 |
| 3465 | Computer Systems Analysts | Test, maintain, and monitor computer programs and systems, i | 4 | 3 |
| 3967 | Technical Writers | Maintain records and files of work and revisions. | 5 | 3 |
| 87 | Cost Estimators | Prepare cost and expenditure statements and other necessary | 4 | 3 |

## Reading guide

- The preserved spot-check still shows a moderate positive relationship between predicted capability and realized agent grade.
- Two sampled tasks changed predicted capability under the refreshed primary CSV, so the correlation moved slightly.
- Comet's self-label was uniformly "completed" across all 20 tasks and was not used. Author grading from captured response content remains load-bearing.
- Comet operated in standard Assistant mode, not Computer mode.
