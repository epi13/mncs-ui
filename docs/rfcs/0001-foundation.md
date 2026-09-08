# RFC 0001: Declarative UI foundation

Status: Draft

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
