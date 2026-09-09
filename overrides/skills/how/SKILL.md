---
name: how
description: "Trace how a function or subsystem works from actual code and explain its data and control flow."
---

# How

Trace the user's question through the current code. For a narrow function or
module, investigate and explain directly. For a broad subsystem, separate the
question into a few meaningful slices. Use independent readers if available and
permitted; otherwise trace the slices sequentially.

Use references/explorer-prompt.md and references/explainer-prompt.md for the
relevant investigation criteria. Follow runtime tool mapping, not historical
tool-call fields in a reference.

Identify entry points, inputs, ownership, state changes, outputs, and failure
paths. Cite the actual files inspected. A file list alone is not an explanation.
Present the smallest complete account first, using a real example when useful.
Keep the full evidence for follow-up questions. The parent synthesizes a coherent
answer rather than forwarding raw worker summaries.
