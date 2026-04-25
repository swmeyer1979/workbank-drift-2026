# Second-rater calibration — instructions

Thanks for doing this. You're the second independent human rater on a 50-task calibration set for a drift study of Stanford SALT Lab's WORKBank dataset. Your scores will be used to measure inter-human agreement.

**Do not look at the first rater's scores** (they're in a separate file you don't need to open). Score independently.

---

## What you're doing

For each of 50 occupational tasks, assign two integer scores on a 1–5 scale:

1. **Capability 2026** (`rater2_capability_2026`) — How capable is a current (April 2026) frontier AI agent (Claude Opus 4.7, Gemini 3 Pro, or GPT-5.5) at completing this task reliably?
2. **Human Agency Scale** (`rater2_has_2026`) — How much human involvement does the task need?

Optional: `rater2_notes` — brief note only if a task was ambiguous or required a judgment call.

**Time estimate:** ~25–40 min. 30 sec per row is fine; don't overthink.

---

## Capability rubric (1–5)

Use the **full scale**. Don't default to 3.

| Score | Meaning |
|---|---|
| **1** | Cannot be done at all. Physical embodiment, real-time sensors, or sustained empathic judgment beyond agent reach. |
| **2** | Demo-level only. Task involves physical-world execution, hardware/equipment validation, live negotiation. Agent can draft but not execute. |
| **3** | Works with supervision. Agent can complete core task when scaffolded; domain expert reviews every output before use. High-stakes cognitive work. |
| **4** | Works reliably end-to-end. Off-the-shelf agent completes typical case; human only handles edge cases. Routine digital work. |
| **5** | Fully automated. Pure data operations — filing, routing, verification against a list, format conversion. No judgment required. |

### Hard caps (applied in order — first rule wins)

1. **Physical / embodied execution → MAX 2.** Tasks that require interacting with, testing, fabricating, or validating physical equipment, materials, hardware, vehicles, lab apparatus, or biological subjects. Documenting or analyzing from afar = not capped.
2. **Continuous interpersonal / sustained empathic work → MAX 3.** Multi-turn human interaction where tone, empathy, trust, or de-escalation matter over time. Transactional Q&A = not capped.
3. **Safety-critical unsupervised operation → MAX 3.** Output takes legal, medical, fiduciary, or life-safety effect without human review. If human review is built into the workflow, not capped.
4. **Novel research / creative direction → MAX 3** for novel, **MAX 4** for applied-routine.

### Score 5 specifically

Use 5 only for: pure data operations, filing/routing, lookup, verification against existing data, spreadsheet calculation with defined formulas. No ambiguity, no judgment, no real-world dependency beyond provided data.

---

## Human Agency Scale (1–5)

How much human involvement does the task need?

| Score | Meaning |
|---|---|
| **1** | Full auto. Agent does entire task alone. |
| **2** | Agent leads, human rubber-stamps. |
| **3** | Equal partnership. Agent + human split the work. |
| **4** | Human leads, agent assists. |
| **5** | Human essential. Agent has no meaningful role. |

---

## What to do

1. Open [`calibration_rater2.csv`](./calibration_rater2.csv) in a spreadsheet tool (Numbers, Excel, VS Code CSV editor — anything).
2. For each row, read `occupation` + `task`. Use the priors (physical / interpersonal / uncertainty / domain requirement means) as additional signal — high physical ≥ 3.5 = almost certainly Rule 1 applies.
3. Fill `rater2_capability_2026`, `rater2_has_2026`. Optional note only if you had to make a tough call.
4. Save to the same file name, same location.
5. Tell Sam you're done.

## Worked examples (hypothetical — not in the CSV)

- "Test equipment for failure modes" → cap **2** (physical execution), HAS **4** (human leads).
- "Document equipment specifications" → cap **4** (routine digital), HAS **2** (agent leads).
- "Provide grief counseling" → cap **3** (sustained empathy), HAS **5** (human essential).
- "Answer product FAQ" → cap **4** (transactional), HAS **2**.
- "Authorize disbursement of funds" → cap **3** (safety-critical), HAS **3**.
- "Store completed documents in appropriate locations" → cap **5** (pure data ops), HAS **1**.

---

## Questions

If a task is genuinely ambiguous, pick the more conservative score (lower capability, higher HAS) and put the reason in `rater2_notes`. Don't agonize — your rating is a reference point, not ground truth.
