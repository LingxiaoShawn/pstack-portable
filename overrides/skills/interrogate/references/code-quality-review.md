# Code quality review

Review the change against its intended behavior, project conventions and
maintenance consequences. Trace callers and ownership when needed to understand
a structural concern. Use the rubric's correctness and verification lenses first.

Look for complexity introduced by the change: duplicated mutable state, hidden
ordering constraints, unclear ownership, leaky interfaces, silent fallbacks, or
unnecessary indirection. Explain a concrete consequence and a proportionate fix.
Useful simplifications can be suggested without making them merge conditions.

File length, a crossed function boundary, a cast or a one-caller helper is a
signal to inspect, not a defect by itself. A file passing 1000 lines does not
automatically require extraction. Consider whether the proposed split actually
reduces what the reader must track.

Distinguish blocking defects or project-contract violations from meaningful
tradeoffs and optional improvements. A maintainability concern warrants blocking
when evidence shows material risk in the changed design, not merely a preferred
style or an opportunity for a larger rewrite. Keep unrelated restructuring out
of a focused fix unless it is needed to make the fix correct.

Return a few actionable findings with location, mechanism, impact and evidence.
State remaining verification gaps. No findings is a valid result; correctness is
not established by reviewer agreement alone.
