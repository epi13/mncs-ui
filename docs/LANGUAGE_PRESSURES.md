# MNCS language pressure ledger

Record workload, current behavior, desired behavior, reproducer, owner, workaround and closure verification for each finding.

## Initial pressure targets

- concise declarative/component syntax
- closures capturing mutable/reactive state
- ownership and references across component lifetimes
- typed heterogeneous child collections
- named/default arguments and ergonomic constructors
- pattern matching and event dispatch
- async tasks scoped to component lifetime
- cancellation and cleanup
- Unicode text/input handling
- trait/interface composition for widgets and render backends
- deterministic update scheduling
- diagnostics for cycles, stale references and invalid state access
- reflection/metadata sufficient for inspection and tooling

The pressure ledger should distinguish framework design problems from language limitations.

## Discovered pressures (foundation campaign, 2026-09-26)

### P-UI-TREE — recursive computation over nested values rejected (non-blocking)

Workload: depth-general queries over nested view values
(`count_nodes` over `Row { kids: [Node; 2] }`).
Current behavior: recursive VALUES elaborate, but any function
recursing through array-element children is rejected (MNE130:
only direct self-calls consuming a match-bound structural
descendant are admitted).
Likely owner: mncs-language. Workaround (canonical): the arena —
flat tables, u64 identity, bounded `iterate` scans. The workaround
is arguably the better architecture (stable identity, no unstable
reconciliation), but the restriction should be explicit.
Verification to close: admitted structural recursion over
fixed-arity children, or a `map_tree` combinator.

### P-UI-CLOSURE — no capturing closures for handlers (non-blocking)

Workload: callbacks capturing state/context for reusable components.
Current behavior: inexpressible; there is no closure syntax to reach for.
Likely owner: mncs-language. Architecture (not a workaround):
intents-as-data — nodes carry `(op, arg)` references to canonical
operations owned elsewhere. Verification to close: a safe-capture
story that preserves the data-first routing (intents must survive
as inspectable values, not disappear into opaque callbacks).

### P-UI-TEXT — no string type; Nat-generic nominals unusable (non-blocking)

Workload: `Label<N>` text with dynamic widths.
Current behavior: no string literals or String type; `record
Label<N: Nat>` elaborates but can never be named in a binding
(MNP053 on `Label<4>`, MNP051 without annotation — annotations are
mandatory). Prior campaigns hit the same wall (per-size concrete
outcomes).
Likely owner: mncs-language. Workaround (canonical): one concrete
`Label32` with byte length; UTF-8 opaque; >32 bytes is `Truncated`
data. Verification to close: nameable generic nominal types with
inference.

### P-UI-SHADOW — match bindings silently shadow parameters (diagnostics gap, non-blocking)

Workload: `table_push_child(t, n)` with arm `Value { n, idx }`.
Current behavior: the arm binding silently shadows the parameter;
the wrong node pushed with zero diagnostics. This cost the
campaign its longest debugging detour (~30 probes, including a
false backend-stride theory) before the values identified it.
The values were decisive: stored id/parent/intent matched the
PARENT row exactly.
Likely owner: mncs-language diagnostics. No workaround needed
(rename the parameter), but a shadow warning would have caught it
instantly. Verification to close: shadowing diagnostics for match
bindings over parameters.

### P-UI-PARSE — chained field-index access needs binding first (non-blocking)

Workload: `a.t.nodes[a.idx]`.
Current behavior: parse error (MNP054); must bind the array first.
Likely owner: mncs-language. Workaround: one `let` per chain link
(used throughout). Verification to close: accept chained
projection/indexing.

### P-UI-MATCH — patterns must bind every payload field (non-blocking, closed)

Workload: `FindOut.Value { idx }` omitting `n`.
Current behavior: MNE179 rejects; MNE140 follows. The rule is
explicit and the fix trivial (bind all fields). Recorded for the
ledger; no owner action needed beyond the existing diagnostic,
which is clear.

### Deferred UI pressures (not language blockers)

- P-UI-STYLE: no cascade/themes (style records only).
- P-UI-VIRTUAL: 64-node bound, no virtualization.
- P-UI-ASYNC: no async/lifecycle semantics.
- P-UI-REMOTE: no remote/render-protocol support.
- P-UI-PERF: no allocation/memory telemetry; suite times are
  toolchain-dominated.

### Boundary closed: Signal

mncs-signal owns DSP kernels (filters/FFT/ring buffers), nothing
resembling UI reactivity. UI updates are pull-based recompute;
no subscription registry, no Signal dependency. Not a pressure —
an ownership answer with evidence.

## Observed language facts (pinned by this campaign)

- MNE130 admits only match-bound structural-descendant self-calls.
- MNE179/MNE140: bind every payload field; diagnostics are clear.
- MNP051/052/053: Nat-generic nominals unnameable; `let` needs annotations.
- Reserved words encountered: `next`, `fail` (also `over`, `up_to`
  from prior work); `throw` avoided preemptively.
- `..` record-update syntax works (`Node { ..n, text: t }`).
- u64 param indexing and `replace` work; `[0; N]` repeat works.
- `==` on enums has no precedent; use discriminant/code functions.
- Match arms on bool are lazy per arm (unlike `select`); guards
  stay safe behind `match`/`if`.
