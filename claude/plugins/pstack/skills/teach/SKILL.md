---
name: teach
description: Explain a change or subsystem plainly, at the reader's pace, grounded
  in code and known design reasons.
disable-model-invocation: true
---

Read [the pstack runtime](../pstack-runtime/runtime.md) before acting; it defines host tools, model fallback, skill lookup and scope.

# Teach

Explain what the thing is, how it works and why it is shaped that way.
Use the conversation to infer what the reader knows; do not quiz them.

Use how for mechanisms and why for historical reasons when necessary. Scope the
investigation to the question. Distinguish source-backed intent from inference,
and preserve that distinction when simplifying the wording.

Start with a small complete answer. Use a concrete input and trace its journey.
Use common names consistently; explain a necessary term once. Respond in the
user's language. Do not substitute playful metaphors for the actual mechanism.
Expand the relevant layer when the reader asks instead of repeating the full
architecture.

Use a compact diagram when relationships are easier to see than read. Use the
host's rendering support or a local HTML/SVG diagram. Image generation is optional,
never a dependency for an accurate engineering explanation. For a requested
presentation or a substantial handoff, invoke brief to create the HTML artifact.

Apply unslop to remove vague language, filler and compressed fragments.
The response is the explanation itself, not a report about the teaching process.
