# RFC 0001: Declarative UI foundation

Status: Partially implemented (foundation 2026-09-26)

## Purpose

Define a UI model that is pleasant for application developers while retaining machine-visible structure.

## Principles

- Simple components should require little ceremony.
- State mutation and ownership have defined semantics.
- Reactive updates are deterministic within a declared scheduling model.
- Effects and async work have structured lifetimes tied to UI ownership.
- Accessibility semantics exist alongside visual semantics from the beginning.
- Rendering backends are replaceable without changing application meaning.
- The runtime may optimize the graph, but must preserve observable contracts.

## Pressure objectives

Closures, ownership/reference ergonomics, reactive dependencies, mutation, async lifetimes, event handlers, heterogeneous trees, generics, declarative syntax, optional values, strings/Unicode, property defaults, named arguments, diagnostics and hot-reload/tooling hooks.

## Implementation record (foundation 2026-09-26)

Retained: machine-visible structure (arena tables, intents as
data, semantic roles); defined state ownership (board vs focus
vs field text vs derived rows); deterministic updates
(pure build/layout/project/diff); accessibility from the start
(structural validation); replaceable backends (slot boundary +
HTML proof).

Redesigned: nested declarative trees → flat arena with stable
ids (MNE130 rules out depth-general recursive computation);
closure handlers → intents-as-data; string labels → Label32
byte buffers; reactive subscriptions → pull-based recompute;
universal component model → 9 concrete kinds.

Delegated: terminal semantics to TUI; operation execution to
Control/Test/Forge (by id reference); DSP to Signal (no UI
reactivity there); test execution to mncs-test.

Excluded: async/lifecycle, themes/cascade, virtualization,
remote protocol, Store/Lineage integration — each with a
pressure or boundary note.
