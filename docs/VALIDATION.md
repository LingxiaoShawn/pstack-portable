# Validation

Checked in the build environment on 2026-09-09:

- Both generated packages contain 51 valid skill directories with matching names.
- Local Markdown resource links and skill-map paths stay inside the package and resolve.
- Codex plugin manifest passes the plugin-creator validator; all Codex skill
  frontmatter files pass the skill-creator validator.
- Rebuilding produces the same file contents.
- Twelve executable tests cover real installation/update/uninstall behavior,
  preserving unrelated skills and local edits, partial-update rollback, rejecting
  incomplete source bundles, configuration precedence and validation, HTML content
  escaping, evidence requirements and retention of long presentation content.
- The briefing helper also runs from an installed copy, without the source layout.

Not established by these checks:

- Authenticated Codex or Claude model sessions loading and following every workflow.
- Semantic equivalence of arbitrary agent refactors.
- Human comprehension speed or comparative model quality.
- Optional Bun PR watcher, cloud workers, durable scheduling or external services.
- Browser layout verification unless recorded separately below.

The native Claude CLI validator could not be installed in this environment
because its network approval was cancelled. No authenticated client session was
run. The local package/skill validators and executable helper tests above did run.
Playwright is present, but its Chromium binary is not installed, so HTML layout
was not visually verified here. The content/escaping tests are not a substitute
for the browser checks in the smoke test.

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
