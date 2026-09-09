# Porting decisions

This is a maintained adaptation, not an assertion of identical runtime behavior.
The pinned upstream source remains under upstream/pstack, including its license.
The generated distributions include all 47 primary upstream skills, three new
workflows (refactor, deslop, brief), and one runtime integration skill.

| Capability | Status |
| --- | --- |
| Code reasoning, architecture, refactoring, principles | Packaged for both hosts, with portable execution rules |
| Teach, plain language, decision trail | Adapted; follows the user's language and available evidence |
| HTML presentation | Added local deterministic renderer; generation of claims remains agent work |
| Native parallel workers | Conditional on actual host tools, permission and concurrency |
| Cross-vendor model panels | Only when those models are actually exposed; not supplied by this package |
| PR watcher, orchestration ledger | Upstream scripts included; optional Bun and gh dependencies |
| Durable cloud workers and scheduled wakes | Host integration required; not implemented by the ledger |
| Grok Bot / Cursor routine provisioning | Not provided; make-bot-ui now uses a real explicitly configured service |
| Benny hosted automations | Upstream reference retained, not advertised or installed as native workflows |
| Historical chat mining | Uses only exposed or supplied current-project records; no guessed account-wide paths |

The shared runtime resolves logical workflow names through a generated skill map.
Codex standalone skills have pstack-prefixed names to avoid collisions. Claude's
plugin uses its own pstack namespace and keeps upstream workflow names.
Both distributions contain their own complete resources; neither relies on a
symlink outside its installed plugin root or on the source checkout.

The main router and platform-sensitive workflows are explicitly rewritten in
overrides/. Portable principle/reference material is retained, with host paths
and model defaults normalized during the build. The runtime contract defines
how to interpret historical task descriptors in retained references; those are
not literal cross-client tool calls. The report must distinguish real independent
review from self-review and actual execution from an unexercised capability.

The new refactor/deslop workflow prioritizes lower reading burden. It does not
use deletion count as the goal and does not discard uncertain comments. Existing
tests and verification thresholds must not be weakened to bless a rewrite.

The build preserves original explicit-only invocation policies. It removes
Cursor-only UI metadata rather than asking a different loader to interpret it.
New user-facing workflows use ordinary skill discovery. The main mode is a
conversation preference, not a new persistent client mode or permission grant.

Upstream helper scripts are preserved and may require Bun plus pinned package
dependencies. The doctor only reports dependencies; it does not install them.
The optional upstream bootstrap can install pinned dependencies when its helper
is explicitly executed. Core workflows and HTML rendering do not need Bun.

To update upstream, fetch a specific new revision into a separate checkout,
inspect its changes, replace the snapshot deliberately, update upstream.lock.json,
and reconcile overrides. Then rebuild and rerun checks. Merely changing the lock
file does not update the snapshot, and the build never fetches moving main.

Official format references checked on 2026-09-09:

- [Codex skill locations and invocation](https://learn.chatgpt.com/docs/build-skills)
- [Codex plugin packaging and compatibility manifest](https://developers.openai.com/plugins/build/plugins)
- [Claude plugin layout and path rules](https://code.claude.com/docs/en/plugins-reference)
- [Claude skills and invocation policy](https://code.claude.com/docs/en/skills)

Readiness here means package structure and helper behavior have been checked.
It does not mean the full workflow has been evaluated across every client version,
model, codebase, optional service or unattended execution configuration.
