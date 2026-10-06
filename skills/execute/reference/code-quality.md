# Thermo-Nuclear Quality Standard

Apply this standard during planning, implementation, pre-publication self-review and PR review.
Adapted from Cursor's [Thermo-Nuclear Code Quality Review](https://github.com/cursor/plugins/blob/main/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md).
This is the local quality bar, not a replacement for the post-PR Cursor review.

## Plan before adding complexity

Trace the changed behavior through its callers, state/data ownership, contracts and canonical
helpers before choosing the implementation. For each meaningful change, ask whether a different
framing could delete whole branches, modes, wrappers or layers rather than merely rearrange them.
Choose the simplest complete design grounded in the existing architecture; do not invent a
second convention or an abstraction just to satisfy a reviewer.

In the existing task plan, briefly record:

- the canonical owner/helper to reuse and which callers or contracts must change;
- the simpler framing considered, the complexity it removes, or why the direct change is best;
- material branching, type/boundary, file-growth and partial-update risks, with verification.

Inspect current sizes of affected files. A change taking a file from at most 1000 lines to over
1000 lines needs a cohesive decomposition plan or a compelling structural reason to retain it.
Already-large files are not exempt from scrutiny, but their size alone does not authorize an
unrelated rewrite. Split by responsibility, not arbitrary line counts or pass-through modules.
For project-level planning, record only evidenced ownership/dependency risks; leave speculative
implementation design to the task that can inspect the actual flow.

## Implement against the same bar

1. **Delete complexity.** Look for a behavior-preserving "code judo" move that removes concepts,
   conditionals, duplicate state or indirection. Moving the same complexity into more files is
   not a simplification. Do not accept a demonstrably worse design merely because it works.
2. **Prevent spaghetti growth.** Challenge ad-hoc feature checks, nullable modes, one-off booleans,
   scattered special cases and repeated condition chains in busy or unrelated flows. Prefer a
   simpler state model or canonical owner; extract a focused helper only when it earns its keep.
   A necessary, local guard is not automatically a design defect.
3. **Keep files cohesive.** Treat crossing 1000 lines as a presumptive blocker. Decompose first
   unless a compelling structural justification shows the retained file remains cohesive and
   legible. Review added responsibilities and coupling even when no threshold is crossed.
4. **Use direct, boring code.** Reject magical generic handling that hides a simple data shape,
   identity wrappers, thin pass-through helpers and speculative factories, policies or frameworks.
   Reuse existing utilities, the standard library or platform features before writing another layer.
5. **Make contracts explicit.** Challenge unnecessary optionality, `any`, `unknown`, casts and ad-hoc
   object shapes that obscure a real invariant. Validate genuinely unknown input at its trust
   boundary; do not remove legitimate uncertainty or hide invalid state behind silent fallbacks.
   Prefer the existing shared typed contract and migrate its affected callers cleanly.
6. **Respect canonical ownership.** Keep business/feature logic in the layer that owns the concept.
   Do not leak implementation details through APIs or scatter feature logic into general-purpose
   paths. Reuse canonical helpers instead of near-duplicates; remove obsolete cutover paths.
7. **Simplify orchestration without changing semantics.** Challenge unnecessary serial work when
   operations are truly independent; check ordering, shared state and error semantics before
   parallelizing. For related writes, prefer the existing transaction/atomic operation so failure
   cannot leave half-applied state. Do not mistake parallel writes for atomic writes or introduce
   infrastructure for a hypothetical risk.

Structural changes must preserve required behavior, permissions, failure handling and persistence.
Follow the shared red/green or characterization-check contract, then re-exercise affected acceptance
criteria after restructuring. Ambition means a simpler implementation, not a broader ticket.
Material scope/risk changes still require the user's decision; unrelated pre-existing debt stays
separate and does not become a blocker merely because it is nearby.

## Review the complete change before publication

Before the initial draft PR and before publishing each code revision, review the complete in-scope
base-to-head change, not only the latest fix. Check callers and surrounding code against all seven
standards above. Reuse current context/evidence; reopen only missing or changed portions. A green
build, passing tests or successful demo does not excuse a structural regression.

Prioritize substantive findings: structural regressions; obvious dramatic simplifications;
spaghetti growth; boundary/type/ownership problems; file growth; modularity; then legibility.
Keep a short quality record in the existing plan or review report: finding, exact location,
consequence, concrete simpler remedy and disposition (`fixed`, `justified`, or `unresolved`).
Record a structural waiver with its reason and supporting evidence, not just "works" or "too much
work". State calibrated confidence; distinguish static reasoning from exercised verification.
Do not invent findings to fill a checklist or flood the review with cosmetic nits.

Treat demonstrated structural regressions, an obvious behavior-preserving simplification that
would delete substantial incidental complexity, unjustified threshold crossings, tangled special
cases, unnecessary indirection/cast-heavy contracts, ownership leaks and canonical-helper
duplication as presumptive blockers. Fix them or substantiate why the simpler design does not
preserve the requirements before publishing or approving. A speculative alternative, personal
style preference or unrelated rewrite is not sufficient evidence to block. No approval merely
because behavior appears correct. Read-only reviews report remedies; they do not authorize edits.
For sanity checks, unresolved blocking quality findings mean **FAIL**, not **PASS**.

## Keep the independent post-PR gate

After authorized draft publication or revision, still run
`skill://execute/reference/review-loop.md`: post `/check`, inspect both Cursor actions for the
current head, address valid findings or push back with evidence, and follow its existing round cap
and approval gate. Local planning/self-review, local waivers and another reviewer's approval never
substitute for either the risk analysis or thermo-nuclear approval. Local passes do not consume
Cursor review rounds. If a required action is unavailable, preserve the draft and report the blocker;
do not silently replace it with this checklist or another project's automation.
