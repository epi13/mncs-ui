# Architecture

## Layers

1. **Core model** — component identity, tree structure, properties, state and lifecycle.
2. **Reactivity** — dependency tracking, derived state, update scheduling and transaction semantics.
3. **Interaction** — pointer, keyboard, text input, focus, commands and accessibility actions.
4. **Layout/style** — constraints, measurement, styling, themes and animation.
5. **Rendering** — backend-neutral scene representation plus native/GPU adapters.
6. **Tooling** — inspection, deterministic event replay, snapshots, accessibility checks and performance evidence.

## First milestones

1. Minimal component/state/event model — DONE (foundation
   2026-09-26: node arena, intents-as-data events, status-board
   fixture proving the full loop).
2. Deterministic layout and simple renderer — HALF DONE (cell
   layout verified; headless projection verified; one thin
   host-owned HTML proof; no in-MNCS renderer).
3. Input/focus and accessibility tree — DONE (focus ownership,
   semantic events, structural a11y validation; platform mapping
   stays renderer-owned).
4. Async/lifecycle semantics — DEFERRED (no workload).
5. Styling/animation foundations — DEFERRED (style records only).
6. Examples that test whether simple UI remains genuinely simple
   in MNCS — STARTED (the board fixture is small but honest about
   ceremony: byte-literal labels and explicit pushes are verbose).

See `docs/UI_MODEL.md` for the ownership boundary and
`docs/VERIFICATION.md` for what the foundation proves.
