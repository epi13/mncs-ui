# Architecture

## Layers

1. **Core model** — component identity, tree structure, properties, state and lifecycle.
2. **Reactivity** — dependency tracking, derived state, update scheduling and transaction semantics.
3. **Interaction** — pointer, keyboard, text input, focus, commands and accessibility actions.
4. **Layout/style** — constraints, measurement, styling, themes and animation.
5. **Rendering** — backend-neutral scene representation plus native/GPU adapters.
6. **Tooling** — inspection, deterministic event replay, snapshots, accessibility checks and performance evidence.

## First milestones

1. Minimal component/state/event model.
2. Deterministic layout and simple renderer.
3. Input/focus and accessibility tree.
4. Async/lifecycle semantics.
5. Styling/animation foundations.
6. Examples that test whether simple UI remains genuinely simple in MNCS.
