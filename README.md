# mncs-ui

<!-- MNCS:generated:begin -->
## Project entry

Declarative, machine-native user-interface infrastructure for MNCS: expressive application code with inspectable UI graphs, state dependencies, effects, and accessibility semantics.

```bash
python3 scripts/run_tests.py
```

Declared capabilities (declarations do not establish execution health):

- `ui-framework/0.1` — mncs-library (experimental)

Semantic sources and ownership: `.mncs/projections.json`.
<!-- MNCS:generated:end -->

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

## Status

First canonical implementation operational (Profile 0.18):
semantic node arena, intents-as-data events, focus ownership,
cell layout, renderer-neutral projection, reconciliation, and a
status-board fixture proving the full loop — 39 native tests
plus a 44-check independent oracle, all passing, with a thin
host-owned HTML proof. Details in `docs/VERIFICATION.md`;
ownership boundary in `docs/UI_MODEL.md`.

## Repository layout

- `src/ui/` — native library (`text`, `node`, `build`, `focus`,
  `event`, `layout`, `render`, `reconcile`, `style`, `a11y`, `app`)
- `tests/native/` — eight `mncs-test` contract suites
- `tools/oracle_ui.py` — independent oracle + HTML proof emitter
- `scripts/run_tests.py` — canonical verification entrypoint
- `docs/UI_MODEL.md` — what UI owns (and does not)
- `docs/VERIFICATION.md` — what the foundation proves
- `docs/ARCHITECTURE.md`
- `docs/rfcs/0001-foundation.md`
- `docs/LANGUAGE_PRESSURES.md`
- `AGENTS.md`

## Verification

`python3 scripts/run_tests.py`
