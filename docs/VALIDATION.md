# Validation

Checked on macOS on 2026-09-09, including the 0.1.1 compatibility fixes:

- Both generated packages contain 51 valid skill directories with matching names.
- Local Markdown resource links and skill-map paths stay inside the package and resolve.
- Codex plugin manifest passes the plugin-creator validator; all Codex skill
  frontmatter files pass the skill-creator validator.
- Rebuilding produces the same file contents.
- Twenty-four executable tests cover real installation/update/uninstall behavior,
  preserving unrelated skills and local edits, partial-update rollback, rejecting
  incomplete source bundles, configuration precedence and validation, HTML content
  escaping, evidence requirements, retention of long presentation content, worktree
  audit decisions, marketplace generation, invocation namespace validation and
  release version changes. Invalid
  release versions are rejected before existing distributions are modified.
- The briefing helper also runs from an installed copy, without the source layout.

Native checks used Codex CLI 0.153.4 and Claude Code 2.1.236:

- Codex's app-server discovered all 51 project-installed skills with no errors.
  Its native plugin reader accepted the marketplace and all 51 plugin skills.
  Every generated `invoke` and `invoke_standalone` was compared with the names
  returned by the native loaders; plugin and standalone namespaces matched.
- Both clients completed a small read-only code explanation in disposable
  projects, reading the runtime, skill map and relevant workflows. These sessions
  used the clients' configured models, not a matrix of model families.
- Claude's native marketplace and plugin validation passed. A real isolated Git
  marketplace installation upgraded the 0.1.0 package from commit `f76938f` to
  0.1.1 after refreshing the marketplace. All 137 installed package files matched
  the new generated source. The Git server was temporary and bound to loopback.
- The upgraded Claude `pstack:poteto-agent` ran with only Read, Glob and Grep.
  Host expansion of `${CLAUDE_PLUGIN_ROOT}` led it directly to its own cached
  workflow and runtime. It did not read the Codex skill copy deliberately present
  in the same project. No Skill tool was needed to discover the plugin root.

These checks used disposable projects and a separate `CLAUDE_CONFIG_DIR`, not
installation into the user's daily plugin configuration. Release versions come
from `overrides/version.txt`; maintainers must raise that version before
distributing changed contents, as documented in README.

Not established by these checks:

- Authenticated Codex or Claude model sessions loading and following every workflow.
- Semantic equivalence of arbitrary agent refactors.
- Human comprehension speed or comparative model quality.
- Optional Bun PR watcher, cloud workers, durable scheduling or external services.
- Browser layout verification unless recorded separately below.

HTML layout was not visually verified in this pass. Content/escaping tests are
not a substitute for the browser checks in the smoke test below. Native loading
and a small successful task do not establish productivity improvements or full
coverage of all workflows, operating systems and client versions.

**Client smoke test**

Use a disposable checkout of a small real project with an existing passing test.
Record the client version and active model. Keep the plugin's default inherited
model settings for the first run.

1. Install using README instructions and open a fresh client session. Confirm the
   documented pstack entry points are discoverable.
2. Ask how a small function works. Verify the response references actual files,
   uses the requested language and does not claim a nonexistent reviewer.
3. Request a scoped refactor. Compare behavior and tests before/after, including
   a relevant error path. Check that unrelated files and useful comments remain.
4. Request brief on the completed change. Open the HTML, check a narrow and wide
   viewport, use navigation and show-all, and verify that every behavior or test
   claim agrees with the final files and actual outputs.
5. If native workers are unavailable, check that the agent explains the sequential
   fallback. A request to compare unavailable model families must not be reported
   as a successful model comparison.

For a new upstream revision, repeat the smoke test on the workflows affected by
the update rather than treating package validation as behavioral equivalence.
