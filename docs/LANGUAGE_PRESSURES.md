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
