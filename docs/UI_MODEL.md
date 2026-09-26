# UI model

## What mncs-ui means

The typed, accessible, testable meaning of a human interface:
what is shown (semantic nodes with roles and names), what state
it represents (projection of canonical state), what interaction
occurred (typed semantic events), what intent that expresses
(operation references), and how the interface changes (bounded
reconciliation). This repository is explicitly NOT:

- a terminal renderer (TUI owns cells, escape codes, key quirks);
- a DOM/desktop renderer (host-owned behind the slot boundary);
- application state (boards own checks; UI projects them);
- operation execution (Control/Test/Forge own operations);
- reactive DSP (Signal owns filters/FFTs, not UI updates);
- a state database (Store owns persistence; UI state is ephemeral).

## Ownership boundary

| Concept | Owner | UI's use |
|---|---|---|
| Terminal cells, escape codes, key normalization | TUI | Consumed as semantic events; never embedded |
| Operation routing/execution | Control | Referenced by id in intents; never imported |
| Test execution/semantics | Test | Fixture shaped like results; never imported |
| DSP/reactivity primitives | Signal | Not used (DSP, not UI reactivity) |
| Persistence | Store | Not used; UI state is ephemeral |
| Structured values | Data | Not needed; nodes are nominal types |
| Test execution, assertions | mncs-test | Consumed |
| Drawing, widgets, a11y APIs, input capture | Renderers | Consume slots; host-owned |

UI owns: the node arena, text labels, focus ownership, typed
events with intent routing, cell layout, the semantic projection,
reconciliation, style records, accessibility validation, and the
status-board fixture proving the loop.

## The loop

canonical state → build_board → table → layout → project (+focus)
→ slots → renderer/agent → semantic event → dispatch → intent →
owner applies → rebuild → diff → rerender.

Build, layout, projection, and diff are pure value functions. The
only mutations are push-time (table assembly) and the explicit
`table_set_text` boundary write. Host effects (HTML emit,
terminal IO) live outside MNCS.

## Identity

Stable u64 ids, never array position. Reorder without id changes
produces zero diff ops (pinned). Focus names one id or is
explicitly empty.

## State kinds

- Board (checks, selection, filter): canonical fixture state.
- Focus (one id): UI-owned.
- Field text: table-resident until an Edit commits it.
- Derived rows (filtered lists): recomputed every build, never stored.

## Events vs intents

Device input never reaches UI. `Activate/Edit/Select/Focus`
arrive semantic; dispatch validates (exists, enabled, right kind,
names an operation) and emits `Intent { op, arg }` data. No
closures exist in MNCS (pressure P-UI-CLOSURE); intents-as-data
are the architecture.

## Enforcement

Static: nominal node kinds/roles/statuses; no function adds a
button to a displacement (no such function exists). Runtime:
`BadParent/DupId/Full/BadDepth`, `DisabledTarget/WrongKind/
UnknownTarget/NotFocusable/NoIntent`, `BadWidth` — all data.

## What is NOT claimed

No real renderer in MNCS (HTML proof is host-owned), no themes/
cascade, no async/lifecycle, no virtualization, no Store/Lineage
integration, no cross-renderer pixel claims, no performance
optimization beyond bounded tables.
