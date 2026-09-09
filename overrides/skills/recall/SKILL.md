---
name: recall
description: "Reconstruct current project context from available conversation history, checkpoints and git state."
---

# Recall

Pin the topic, time window and active project. Use a supplied state capsule
directly if it already answers the request.

Read the relevant visible conversation, explicit checkpoint files and git state.
Use host-exposed or user-supplied current-project transcripts if available. Do not
guess a client-specific transcript path or scan unrelated workspaces.
Use why for necessary historical sources that the current tools can access.
Absence of a transcript or service is a coverage limit, not evidence of no activity.

Verify cited branches, PRs and artifacts against live state. Return a short capsule,
the status of each relevant thread, unresolved problems and the next concrete
action. Distinguish completed, in-progress, reverted and planned work. Do not
silently truncate a user request for all activity into a recent sample.
