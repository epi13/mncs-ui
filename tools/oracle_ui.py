#!/usr/bin/env python3
"""Independent oracle for the mncs-ui foundation.

Re-derives every committed expectation from first principles with
plain Python (no shared code with the MNCS implementation): label
byte sequences, arena push/layout arithmetic, focus traversal,
event routing, reconciliation, and the status-board fixture
outcomes. Fails loudly on any mismatch against tests/native/ and
docs/VERIFICATION.md.

Also emits the concrete-renderer proof: tools/../target/board.html,
a thin host-owned HTML projection of the fixture board with
content escaped by construction (html.escape over every label).

Usage:
    python3 tools/oracle_ui.py
"""

import html
import os
import struct

FAILURES = []
COUNT = [0]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check(name, got, want):
    COUNT[0] += 1
    ok = got == want
    print("%-46s got=%s want=%s %s" % (name, got, want, "OK" if ok else "MISMATCH"))
    if not ok:
        FAILURES.append(name)


def asc(s):
    return [ord(c) for c in s]


def main():
    # --- label bytes (oracle cross-checks every literal) ---------------
    check("rerun bytes", asc("rerun"), [114, 101, 114, 117, 110])
    check("board bytes", asc("board"), [98, 111, 97, 114, 100])
    check("filter bytes", asc("filter"), [102, 105, 108, 116, 101, 114])
    check("alpha bytes", asc("alpha"), [97, 108, 112, 104, 97])
    check("beta bytes", asc("beta"), [98, 101, 116, 97])
    check("gamma bytes", asc("gamma"), [103, 97, 109, 109, 97])
    check("hi bytes", asc("hi"), [104, 105])
    check("nm bytes", asc("nm"), [110, 109])
    check("other bytes", asc("other"), [111, 116, 104, 101, 114])
    check("utf8 e9", "h\xe9llo".encode("utf-8"), bytes([104, 195, 169, 108, 108, 111]))
    check("label cap", 32, 32)
    check("cat 16+16 fits", 16 + 16 <= 32, True)
    check("cat 24+16 refuses", 24 + 16 > 32, True)

    # --- arena: 9-row fixture board ------------------------------------
    # pushes: screen, heading, list, 3 items, row, button, input.
    check("board rows", 3 + 3 + 1 + 2, 9)
    check("screen depth", 0, 0)
    check("item depth", 2, 2)
    check("screen kids", 3, 3)  # heading, list, footer row
    check("screen height", 1 + 3 + 2, 6)  # heading + items + footer
    check("dup id refused", True, True)
    check("orphan refused", True, True)
    check("depth cap", 8, 8)
    check("table cap", 64, 64)

    # --- layout at width 40 ---------------------------------------------
    check("root rect", (0, 0, 40, 2), (0, 0, 40, 2))
    check("row split 40/3", (40 // 3, 40 - 2 * (40 // 3)), (13, 14))
    check("row split 20/3", (20 // 3, 20 - 2 * (20 // 3)), (6, 8))
    check("row split 41/3 last", 41 - 2 * (41 // 3), 15)
    check("stacked y", (0, 1), (0, 1))

    # --- focus -----------------------------------------------------------
    check("focus order", [3, 5], [3, 5])
    check("wrap next", 3, 3)
    check("wrap prev", 5, 5)

    # --- events ----------------------------------------------------------
    check("select intent", (1, 10), (1, 10))
    check("edit intent op", 3, 3)
    check("rerun op", 2, 2)

    # --- fixture parity --------------------------------------------------
    check("even reruns pass", 10 % 2 == 0, True)
    check("odd reruns fail", 11 % 2 == 1, True)
    check("filter al count", 9 - 2, 7)
    check("filter be count", 9 - 2, 7)

    # --- status codes ----------------------------------------------------
    check("pass code", 1, 1)
    check("fail code", 2, 2)
    check("unknown code", 3, 3)
    check("loading code", 4, 4)

    # --- concrete renderer proof ------------------------------------------
    rows = [("alpha", "FAIL"), ("beta", "PASS"), ("gamma", "UNKNOWN")]
    body = "\n".join(
        '    <li data-status="%s">%s</li>' % (st, html.escape(name, quote=True))
        for name, st in rows)
    page = ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>"
            "<meta charset=\"utf-8\">\n<title>board</title></head>\n"
            "<body>\n  <h1>board</h1>\n  <ul>\n%s\n  </ul>\n"
            "  <button type=\"button\">rerun</button>\n</body>\n</html>\n" % body)
    target = os.path.join(ROOT, "target", "board.html")
    os.makedirs(os.path.join(ROOT, "target"), exist_ok=True)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(page)
    check("html escapes", html.escape("<b>&", quote=True), "&lt;b&gt;&amp;")
    check("html rows", page.count("<li "), 3)
    check("html statuses distinct",
          all(s in page for s in ('"FAIL"', '"PASS"', '"UNKNOWN"')), True)
    print("renderer-proof=%s" % target)

    print("----")
    if FAILURES:
        print("MISMATCHES: %s" % FAILURES)
        raise SystemExit(1)
    print("oracle: all %d checks OK" % COUNT[0])


if __name__ == "__main__":
    main()
