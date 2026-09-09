---
name: make-bot-ui
description: "Build a UI for an explicitly configured webhook service; requires a real service endpoint and supported authentication."
---

# Make a bot UI

This port does not provision Cursor or Grok Bot routines. Begin with the webhook
service the user actually wants to use and its documented API. If none is
available, build only the requested local UI and contract, and identify the
missing service integration. Do not invent a routine creation tool.

Keep credentials on the server using the host's supported secret storage.
Use a small explicit request schema and treat webhook payloads as data. Bind a
local development server to localhost by default; expose it more widely only
when required and authorized. Do not install a VPN or alter networking implicitly.

Verify a harmless request against the actual service before calling the
integration live. State whether only the UI, the local adapter, or the complete
webhook path was exercised.
