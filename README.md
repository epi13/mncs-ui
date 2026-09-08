# mncs-ui

Declarative, machine-native user-interface infrastructure for MNCS.

`mncs-ui` is intended to pressure `mncs-language` on the opposite end of scientific computing: expressive application code, reactive state, events, accessibility, composition, animation, native rendering, and developer ergonomics.

## Initial scope

- declarative component trees and layout
- local/shared reactive state
- events, commands, focus and input
- styling and theming boundaries
- accessibility semantics
- animation and time-dependent state
- async work and lifecycle management
- rendering/backend abstraction
- inspection, debugging and testability

## Machine-native direction

The UI graph, state dependencies, effects and accessibility semantics should remain inspectable by MNCS tooling rather than disappearing into opaque runtime callbacks.

## Repository layout

- `docs/ARCHITECTURE.md`
- `docs/rfcs/0001-foundation.md`
- `docs/LANGUAGE_PRESSURES.md`
- `AGENTS.md`
