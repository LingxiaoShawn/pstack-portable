---
name: interrogate
description: "Review a diff adversarially against its intent, correctness and maintainability, without automatically editing it."
---

# Interrogate

Establish the intended behavior and scope. Include relevant working-tree changes
and surrounding code, using the appropriate base branch rather than assuming main.
Read references/rubric.md, references/code-quality-review.md and
references/reviewer-prompt.md as needed to construct the review.

When independent reviewers are available and permitted, give them the same intent,
artifact and rubric without the author's rationale. Respect max_workers. Use
different model families only when the host actually provides them.
Without independent reviewers, perform and label a single-agent review.

For each finding, verify the mechanism or reproduction against the code. Group
actionable defects, meaningful tradeoffs, and dismissed findings. Prefer evidence
over reviewer vote counts. Lead with issues that change the shipping decision,
not an exhaustive report of the reviewing process. Do not fix code unless the
request includes fixes.
