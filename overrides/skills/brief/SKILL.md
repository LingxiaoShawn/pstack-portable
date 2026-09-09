---
name: brief
description: "Create a concise, evidence-backed HTML presentation explaining a completed change or subsystem."
---

# Brief

Read the final code, relevant diff and actual verification outputs. Choose the
few things the reader needs to understand. Use the user's language, common words,
one consistent name per concept and a real input/output example.

Write a JSON brief following assets/example.json. It contains title, summary,
problem, before, after, example, verification and sources. These are planning
fields, not jargon to show to the audience. Sources must point to files or links
actually inspected. A test result must include what ran and its observed outcome.
Unverified claims belong in uncertainties; do not invent a successful check.

For a change, explain the earlier problem, the new structure and the effect on a
real example. For an unchanged subsystem, use before/after for the input and
result and say this is a walkthrough, not a change report.

Render with:
```sh
python3 <this-skill-directory>/scripts/render.py --input <brief.json> --output <brief.html>
```
The renderer is local and uses only Python's standard library. It produces five
readable sections with previous/next navigation, a show-all option and print
support. Sections can scroll; long content must not be silently clipped.

Recheck the rendered text against the final code and sources. Open the page and
inspect layout if a browser capability is available. If none is available, state
that fact rather than claiming visual inspection. Keep technical evidence in the
last section so the main explanation stays clear. Return the artifact and a
short summary, not a duplicate transcript of the presentation.
