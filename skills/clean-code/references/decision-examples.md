# Decision Examples

Use these examples to distinguish a useful simplification from a superficially similar regression. Apply the consuming language's idioms and the actual project contracts; the examples do not prescribe a framework or coding style.

## Forwarding code and useful boundaries

Suppose `submit -> prepare -> dispatch -> send` merely forwards the same arguments and return value. If tracing those names adds navigation without explaining decisions, inlining or consolidating the forwarding functions may help.

Before removing a wrapper, inspect what it owns. A single implementation that supplies transaction scope, authorization, resource lifetime, a stable public contract, or isolation from an external effect can be useful. Preserve that boundary or explicitly relocate its duty. A concise caller is not an improvement if it must now know how to manage an internal connection or lock.

## Duplication and independent policy

Two callers lowercase a string. One normalizes login identifiers; another exports a value for display. Their identical expression does not establish a shared rule: a display change may require retaining case while login normalization remains unchanged.

Keep independently changing policies separate. Conversely, when several paths implement the same current business rule, consolidating its owner can prevent divergent fixes. Trace inputs, null/empty behavior, errors, callers, and required differences before merging. If an existing shared helper has accumulated caller-specific switches, inspect whether specializing its callers removes accidental coupling; do not declare every parameterized function a wrong abstraction.

## Apparent duplicate checks across effects

Consider this language-neutral sequence:

```text
if stopping or clock.now() >= deadline:
    return
await write(payload)
if stopping or clock.now() >= deadline:
    return
mark_complete()
```

The second guard observes a later state. The write can take time or yield to a stop request, so the checks are not interchangeable. Preserve the exact deadline boundary, whether the write may still occur, what completion means, and how write failures propagate. A test in which the write changes the stop flag or advances time distinguishes removal from preservation. When a value is immutable and no intervening effect can invalidate the earlier guarantee, elimination may instead be justified by the actual contract.

## Long code and mixed responsibility

A sequential parser or explicit state machine may be easier to understand together than through many tiny helpers. A long dispatch statement with simple independent cases is not automatically a problem.

By contrast, a function that decides retry policy, serializes requests, owns a connection, and writes recovery records may force unrelated knowledge on each change. Separate the responsibilities that have a current reason to change independently, while retaining the required connection identity, transaction, ordering, and recovery semantics. Do not split solely at each chronological step or move all branches into a generic engine that is harder to understand.

## Unused locally and reachable at runtime

A handler with no ordinary call sites may be loaded by a configuration string, decorator, reflection, command entry point, dependency injection, or an external consumer. Search the applicable registration and export paths before deletion. A public extension point is not unused merely because this checkout contains no consumer.

If the usage boundary cannot be established, retain the uncertain code and describe the gap; continue with independently supported cleanup.

## Reuse and lifecycle compatibility

A framework scheduler may replace custom startup, worker, and shutdown machinery. Compare startup timing, overlap/concurrency, cancellation, failures, shutdown behavior, and required performance before substitution. The existence of a similarly named facility is not evidence of semantic equivalence. Verify the installed version's official contract when uncertain; no particular documentation tool is required.

## Local cleanup and structural completion

For a one-line fallback bug, fix the specified condition and its affected uses without reorganizing unrelated packages. For an authorized responsibility or package cleanup, a one-line fix is insufficient if the requested ownership boundary remains mixed. The relevant unit is the requested outcome and its impact paths, not a fixed number of files.

A cleanup request can also end unchanged: explain which reading or change task the existing design already serves. If only one path was inspected, qualify that conclusion rather than declaring the whole module clean.

## Design sources and limits

These sources inform the paired examples; they are not runtime dependencies or evidence that this skill improves every language or project:

- [Google code review guidance](https://google.github.io/eng-practices/review/reviewer/looking-for.html): concrete complexity, present requirements, and useful tests, names, comments, and documentation.
- [Parnas on modular decomposition](https://john.cs.olemiss.edu/~hcc/csci555/notes/localcopy/Parnas_Criteria_Decomposing.pdf): responsibility and information hiding rather than division by execution stages alone.
- [The Wrong Abstraction](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction): re-examine shared abstractions that accumulate distinct caller policies.
- [Preparatory refactoring](https://martinfowler.com/articles/preparatory-refactoring-example.html): small behavior-preserving transformations can prepare a necessary structural change.
- [Linux 6.12 coding style](https://docs.kernel.org/6.12/process/coding-style.html#functions): project-specific exceptions to length and control-flow heuristics; these are not portable syntax rules.
- [Ponytail at the inspected revision](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/skills/ponytail/SKILL.md): inspect impact and reuse existing capabilities. This skill does not adopt smallest-diff or deletion-first rules as universal objectives.
