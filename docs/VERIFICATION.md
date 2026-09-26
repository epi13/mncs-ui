# Verification

Canonical fixture: status board with checks 10/11/12
(alpha/Fail, beta/Pass, gamma/Unknown), 9-row table
(screen, heading, list, 3 items, footer row, rerun button,
filter input), 40-cell layout.
39 native `mncs test` declarations across 8 suites, all PASS,
plus a 44-check independent oracle (`tools/oracle_ui.py`), all
PASS, plus the host-owned HTML proof (`target/board.html`).

## Text (6 tests)

- Empty/push/drop; no underflow; full label refuses.
- Concatenation with truncation refusal (16+16 fits, 24+16 refuses).
- Byte-exact equality ignoring padding; length mismatch differs.
- Prefix matching with empty/self prefixes; overlong prefix fails.
- UTF-8 opaque: 6-byte sequence preserved, counted as bytes.

## Nodes (6 tests)

- Root/child push with depth, intent, parent index.
- Duplicate ids, orphan parents, and second roots refused;
  missing lookup is `Missing` data.
- Heights bubble (leaf 1, containers summed); sibling anchors
  captured (sx 0, sy 0 for first children).
- Depth cap: depth 8 allowed, depth 9 is `BadDepth`.
- Table fills at 64 with `Full` on the 65th push.
- `table_set_text` writes input text; wrong kinds and missing
  ids refused.

## Focus (4 tests)

- Requests route to focusable rows; unknown/text/disabled rows
  report `UnknownTarget`/`NotFocusable`.
- Traversal order 3 → 5 with wrap both directions; empty focus
  starts at first/last.
- Removal: live focus kept, gone focus moves to nearest live
  row, empty stays empty.

## Events (4 tests)

- Select/Activate/Edit emit `(op, arg)` intents.
- Disabled → `DisabledTarget`; missing → `UnknownTarget`;
  wrong kind → `WrongKind`; unfocusable focus → `NotFocusable`.
- Zero-intent buttons are `NoIntent`, never silent no-ops.

## Layout (4 tests)

- Column stacks full-width; root height sums children.
- Row splits 40 across 3 as 13/13/14 (remainder last).
- Resize redistributes purely (20 → 6/6/8; 41 → 13/13/15).
- Zero width is `BadWidth`.

## Render (4 tests)

- Slots carry id/role/name/status/enabled/focus/rect.
- Focus marks exactly the focused row; empty focus marks none.
- `find_by_role`/`find_by_name` in table order; missing names miss.
- Style storage bounded (16 entries); projection takes no style
  input — separation by construction.

## Reconcile (4 tests)

- Identical tables diff empty.
- Insert/Remove/Update detected with exact counts.
- Reorder with stable ids produces zero ops.

## App (7 tests)

- Board builds 9 rows; accessibility validates `Ok`.
- Select dispatches intent and updates board selection.
- Rerun resolves by parity (even → Pass, odd → Fail),
  verified on rebuilt projections.
- Prefix filters derive rows (9 → 7).
- Edit emits intent, commits through `table_set_text`, and the
  rebuilt board shows the filtered rows.
- Full loop: select 12 → rerun → rebuild → exactly one
  `Update` for id 12; projection flips Unknown → Pass.
- PASS/FAIL/UNKNOWN project distinctly with codes 1/2/3.

## Reproduction

`python3 scripts/run_tests.py` (native suites + oracle + evidence
JSON under `target/`). Full run takes minutes (toolchain
invocations dominate; UI arithmetic is negligible).
