"""The pinned rubric and prompt template. Edit here; raters see exactly this.

v2 (2026-04-24): added edge anchors (score 2, 5), cap hierarchy with worked
examples, and explicit "default to 3 is wrong" language to combat central-
tendency bias. Worked examples are hypothetical, not drawn from the
calibration set, to avoid calibration laundering.
"""

from __future__ import annotations

RUBRIC = """You are rating the 2026 frontier AI-agent capability for an occupational task on a 1-5 Likert scale.

The point of this rubric is NOT to pick a safe middle. Use the full scale. If you are tempted to score a 3 because you are uncertain, reconsider — "3" means "a domain expert must review every output before use," which is a STRONG operational claim, not a neutral default.

=== SCORE DEFINITIONS ===

1 = Cannot be done at all.
    Requires physical embodiment, real-time sensor access to the physical world, or continuous empathic judgment that current agents cannot deliver. Even with tools, an agent produces garbage.

2 = Demo-level only.
    The core task involves physical-world execution, hardware/equipment validation, live negotiation, or real-time safety decisions. An agent can draft analysis or summaries but cannot execute the task. Reliability in an agentic loop is < 50%. A human must do the actual task.

3 = Works with supervision.
    An agent can complete the core task when scaffolded (tool access, retry, verification step), but a domain expert must review every output before use. Cognitive work with high stakes, compliance requirements, or novel judgment.

4 = Works reliably end-to-end.
    An off-the-shelf agent (Claude Opus 4.7, Gemini 3 Pro, GPT-5.5 + standard tools) completes the task for the typical case. A human sees only edge-case escalations. Routine digital work with structured I/O.

5 = Fully automated, matches or exceeds typical human.
    Pure data operations: filing, routing, verification against a list, spreadsheet calculation, record lookup, format conversion. Low ambiguity, no judgment required beyond the rule set. Human involvement adds no value beyond periodic governance.

=== CAP HIERARCHY (applied in order — first rule that fires wins) ===

Rule 1 — Physical / embodied execution: MAX 2.
  If the task requires interacting with, testing, fabricating, or validating physical equipment, materials, hardware, vehicles, lab apparatus, or biological subjects — cap at 2 regardless of how analytical the task sounds.
  Examples: "test equipment for failure modes" → 2. "evaluate pilot plant runs" → 2. "conduct hardware validation" → 2.
  NOT capped: "document equipment specifications" → not physical execution, score by other rules.

Rule 2 — Continuous interpersonal / sustained empathic work: MAX 3.
  If the task requires multi-turn human interaction where tone, empathy, trust, or de-escalation matter over time — cap at 3.
  Examples: "provide grief counseling" → 3. "negotiate a contract face-to-face" → 3. "conduct a performance review" → 3.
  NOT capped: "answer product FAQ" → transactional, not sustained empathy.

Rule 3 — Safety-critical unsupervised operation: MAX 3.
  If the task produces an output that takes legal, medical, fiduciary, or life-safety effect without human review — cap at 3.
  Examples: "authorize disbursement of funds" → 3. "file a legal brief" → 3. "diagnose a patient" → 3.
  NOT capped: "draft a brief for attorney review" → human review is built in.

Rule 4 — Novel research / creative direction: MAX 3 for novel, MAX 4 for applied.
  Genuinely novel theorem / algorithm / artistic direction: cap 3.
  Applied routine work within an established framework: no cap.

=== WHEN TO SCORE 5 (override central-tendency bias) ===

Score 5 IF the task is:
- Pure data operations (filing, routing, lookup, verification against existing data)
- Format conversion, summarization of structured inputs
- Spreadsheet calculation with defined formulas
- No ambiguity, no judgment, no external-world dependency beyond provided data

Do NOT score 5 if: the task requires domain judgment about what's "correct," interpretation of ambiguous inputs, or any real-world action beyond digital recording.

=== HUMAN AGENCY SCALE (has_score, 1-5) ===

Separate from capability. How much human involvement does this task require in an ideal 2026 deployment?

1 = Full auto. Agent does the entire task alone. Human touches it only for periodic governance.
2 = Agent leads, human rubber-stamps. Final approval is a formality.
3 = Equal partnership. Agent and human split the work; both contribute material judgment.
4 = Human leads, agent assists. Agent drafts, researches, or summarizes; human does the actual task.
5 = Human essential. Agent has no meaningful role beyond trivial support.

IMPORTANT: has_score measures HUMAN involvement need. Higher = more human needed. This is the OPPOSITE of capability.

A task can be cap=5 (fully automatable) and has=1 (human not needed). A task can be cap=2 (agent can't do it) and has=5 (human does everything). These should correlate negatively in general, but not always (a cap=4 task may still be has=2 if humans must approve).

=== ANCHORING TO APRIL-2026 BENCHMARKS ===

Ground your rating in the April-2026 benchmark anchors provided. Cite which anchors you used. If no anchor applies to this task family, set `llm_inferred: true` and `confidence: low`.

=== OUTPUT ===

Return ONE JSON object:

{
  "capability_score": <int 1..5>,
  "has_score": <int 1..5>,
  "justification": "<one sentence, <=200 chars>",
  "cap_rule_fired": "none|physical|interpersonal|safety_critical|novel_research",
  "benchmark_anchors": ["<anchor_id>", ...],
  "llm_inferred": <bool>,
  "confidence": "<low|medium|high>"
}

No extra text. No chain-of-thought. Valid JSON only.
"""

PROMPT_TEMPLATE = """{rubric}

---

TASK TO RATE:

Occupation (O*NET-SOC): {occupation}
Task statement: {task}

Worker-reported requirement priors (1-5 means across workers):
- Physical Action Requirement:          {physical}
- Interpersonal Communication:          {interpersonal}
- Involved Uncertainty:                 {uncertainty}
- Domain Expertise Requirement:         {domain}

Pay attention to the priors. A high Physical Action Requirement (>= 3.5) is a STRONG signal that Rule 1 applies. A high Interpersonal Communication Requirement (>= 3.5) is a signal for Rule 2.

Relevant 2026 benchmark anchors (cite only those that apply to this task family):
{anchors}

---

Return the JSON now.
"""


def build_prompt(
    *,
    occupation: str,
    task: str,
    physical: float,
    interpersonal: float,
    uncertainty: float,
    domain: float,
    anchors_text: str,
) -> str:
    return PROMPT_TEMPLATE.format(
        rubric=RUBRIC,
        occupation=occupation,
        task=task,
        physical=round(physical, 2),
        interpersonal=round(interpersonal, 2),
        uncertainty=round(uncertainty, 2),
        domain=round(domain, 2),
        anchors=anchors_text,
    )
