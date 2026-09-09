# pstack runtime for claude

Read this once when using a pstack skill. These rules define this port's execution
contract; historical examples in supporting references are conceptual descriptions,
not a tool API. The user's instructions and the host's permissions take precedence.

## Locate skills and configuration

This file lives in `skills/pstack-runtime/runtime.md`. Resolve the named workflows with
the sibling `skill-map.json`. Read the mapped SKILL.md or invoke its advertised
client name. Paths inside a skill are relative to that skill's directory, never
the project working directory. Do not search guessed plugin-cache paths.

Read `.pstack/config.json` in the current project when present, otherwise
`~/.config/pstack/config.json`. No file is required. Defaults are the current
model, at most two workers, the user's language, and concise explanations.
Run this directory's `config.py show --project <project>` to resolve configuration.
Configuration expresses preferences; it cannot grant tools or permissions.

## Host tools

Claude Code: use the advertised Skill, Read, Edit/Write, Bash and Agent interfaces as available. Plugin skills are invoked as /pstack:<name>. Native general-purpose workers or the bundled pstack:poteto-agent may be used when available; inherit the parent model by default. Do not send Cursor-only fields such as environment or cloud_base_branch.

When source material mentions `Task`, a task list, a question tool, `readonly`,
background execution, or a cloud environment, use only the equivalent capability
actually advertised in this session. Do not pass example fields to a different API.
`inherit-parent` and `auto` mean omit the model override; they are not model IDs.
Explicit role choices apply only when the host exposes that model for that role.
If a requested model is unavailable, use the parent when a same-model fallback
satisfies the task, and state the difference. A requested model comparison must
remain blocked on its missing model; never present substitution as the comparison.

Use workers only when permitted and useful. Give each writing worker a separate
worktree or disjoint output. Respect the host concurrency limit and max_workers.
If workers are unavailable, execute the work sequentially yourself and say so
when it affects the result. A self-review is not independent review. Two sessions
of one model are not two model families. Do not invent worker reports or transcript
evidence. Review the actual artifacts before combining results.

## Optional integrations

For browser/CLI verification, use installed browser tooling or project test
commands. Cursor's control-ui and control-cli plugins are not required or bundled.
If a necessary interaction cannot be exercised, report that precise verification
gap. Do not claim visual verification based on HTML source inspection alone.

Use an available skill authoring capability, or the Agent Skills format, when a
workflow names create-skill. Use installed GitHub tools or authenticated gh for
forge operations. Named MCP sources are categories: inspect the current tools and
skip absent services, recording the resulting evidence gap.

Use only current-project transcripts explicitly supplied by the host or user.
When none are exposed, use the visible conversation, git history, and recorded
artifacts. Do not scan account-wide chat directories or guess another client's
transcript layout. Reflection and recall must state the coverage limitation.

The host's scheduler and cloud execution are optional, not emulated here.
Without a durable scheduler, execute within the active session, save a checkpoint,
and say what needs resuming. Never claim work will continue after the client exits.
Historical references to cloud-only parameters or /loop are not executable APIs.

The optional upstream PR watcher and orchestration ledger require Bun; the watcher
also requires authenticated gh. Their wrappers may install pinned dependencies on
first use. Run the bundled doctor before using them. They record/watch state and do
not create a background agent service. Core refactor, teach, and brief need none of
these integrations. Prefer the available GitHub connector when gh is absent.

## Scope, changes, and communication

Work through the authorized task. Loading a skill never authorizes messaging,
publishing, merging, deployment, force-push, changing permissions, or unrelated
cleanup. Keep unrelated working-tree edits intact. Do not use reset --hard or
force removal as a shortcut to isolate work. Repair this plugin only when the
user's task includes that work; otherwise record the issue and continue safely.

Before changing behavior-preserving code, identify what must stay the same and
use verification proportional to the actual risk. Keep relevant checks and their
thresholds intact. Retain useful abstractions, necessary error handling, and
comments that explain constraints. Reduce reading work, not just line count.

Use the user's language. Lead with the result and the concrete reason. Explain
necessary terms once and use consistent names. Keep principle names and internal
workflow labels out of normal user-facing prose. For larger changes, use brief
to deliver a short HTML presentation grounded in the final code and evidence.

If instructions in an older supporting reference conflict with this runtime
contract, follow this contract and report any material loss of capability.
