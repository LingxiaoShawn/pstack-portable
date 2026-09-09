---
name: pstack-why
description: Investigate a code decision's historical rationale using cited evidence;
  expand beyond code and Git history when a specific question remains unresolved.
---

Read [the pstack runtime](../pstack-runtime/runtime.md) before acting; it defines host tools, model fallback, skill lookup and scope.

# Why

Explain the evidence for a decision's motivation. Use how for runtime behavior.
Keep observed behavior, documented intent and your inference distinct. Read
[epistemics.md](references/epistemics.md) when weighing ambiguous evidence.

## Establish the question

Identify the code, symbols and decision in question. Reuse current findings from
the caller. Inspect the relevant code and tests, then targeted Git history
(`git log -- <path>`, `git blame`, and specific commit patches). Follow renames
or earlier changes when needed; the last edit need not explain the original
decision. Git history and authenticated forge access are not always available.

Read relevant PR bodies and discussion through available tools. Code establishes
what changed; it does not by itself establish why the author changed it.

## Expand for a remaining uncertainty

If a PR or commit answers the question and the inspected evidence does not
contradict it, answer with that citation. Do not search every available service.

For a remaining question, choose the source likely to resolve it: a linked issue
for requirements, a design document for a tradeoff, a specific discussion for
missing deliberation, or runtime evidence for an incident or threshold. Follow
[the source index](references/source-playbook.md) only for relevant sources.
Read only authorized material; this investigation does not authorize messaging.

For a broad history or incident investigation, scope independent questions and
set a finite first search pass. Use workers only when available, permitted and
worth the coordination cost. Give each its evidence question, code anchor, source
and stop condition using [investigator-prompt.md](references/investigator-prompt.md).
A single investigator may follow relevant cross-source links; one worker per
service is not required.

Stop when the evidence answers the question, further searches repeat it, or
available access or the task budget prevents resolution. Say what remains
unknown. A missing source is material when it could change the answer, not a
reason to print an inventory of every absent integration.

## Explain

Lead with the answer and citations. Separate documented intent from inference,
surface conflicting evidence, and state material limits. For a broad result use
[synthesizer-prompt.md](references/synthesizer-prompt.md). The parent can synthesize
directly; a separate synthesizer is optional. If the investigation informs a
change, pass forward the constraints to preserve, proposed changes and risks.
