# Agent and contributor contract

- Prefer `mncs-language` for implementation and examples.
- Treat ergonomics and diagnostics as core acceptance criteria, not polish added later.
- Keep state ownership, mutation, effects and lifecycle semantics explicit enough for tools to reason about them.
- Avoid framework magic that depends on hidden global state or undocumented ordering.
- Record every significant language/compiler/runtime pressure in `docs/LANGUAGE_PRESSURES.md` with a reproducer when possible.
- Accessibility, deterministic tests and event/lifecycle correctness are required design dimensions.
- Do not permanently mask missing MNCS capabilities with another-language implementation.
