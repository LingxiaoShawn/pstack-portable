---
name: principle-test-behavior-not-implementation
description: "Choose tests that detect a meaningful behavior regression, using observable results and effects rather than mirroring implementation."
---

# Test behavior, not implementation

Identify the behavior that could regress and exercise the public surface that
owns it. Assert the result, error, state transition or external effect the caller
depends on. Expected values should come from the contract, an independent oracle,
or a meaningful property, not a second call to the same implementation.

Ask which plausible defect would make the test fail. Returning undefined is one
possible mutation, not a universal test-quality rule: `toBeDefined()`,
`toBeTruthy()` and `toEqual([])` can all reject undefined. Their usefulness
depends on the contract and the input, not the assertion's name.

Absence can be important behavior: no write for an invalid request, no message
without authorization, or an empty result for no matches. Assert that absence
on a realistic path. Add a contrasting case when it would detect a missed
implementation, without requiring both cases in the same test.

Use mocks to observe effects at real boundaries, checking meaningful arguments
and outcomes. Do not freeze incidental internal call order. Property tests,
compile-time checks, table consistency checks and exact external-contract
constants can all provide useful evidence.

Keep useful existing coverage. Strengthen a weak assertion when possible; remove
a test only after understanding its purpose and establishing it is redundant,
obsolete or tests no required behavior. Avoid adding tests that merely repeat
instruction wording or a hand-maintained implementation value.
