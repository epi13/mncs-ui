#!/usr/bin/env python3
"""Run mncs-ui native contract suites through `mncs test`.

Usage:
    python3 scripts/run_tests.py [--suites text,node] [--evidence-dir DIR]

Each suite is a Profile 0.18 test module under tests/native/ exercised
through the canonical mncs-test entrypoint (`mncs test`) using the
compiler-owned declaration inventory. Every expectation is an
in-language assertion; the result envelope carries stable test-case
identities, inventory identity, and run identity.

The library is dependency-free beyond mncs-test and the language
core: it deliberately does not depend on Signal (DSP, not reactive
UI), Control (operations referenced by id, never imported), TUI
(a renderer, not the model), or Data/Store (no persistence here).
See docs/UI_MODEL.md for the boundary.

After the native suites, the independent oracle
(`tools/oracle_ui.py`, no shared code with the MNCS implementation)
re-derives every committed expectation and emits the sample HTML
proof; its verdict joins the evidence.

Exit code is 0 unless some suite or the oracle fails to verify.
"""

import argparse
import datetime
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NATIVE = os.path.join(ROOT, "tests", "native")

SUITES = [
    {"name": "text", "source": os.path.join(NATIVE, "text_tests.mncs")},
    {"name": "node", "source": os.path.join(NATIVE, "node_tests.mncs")},
    {"name": "focus", "source": os.path.join(NATIVE, "focus_tests.mncs")},
    {"name": "event", "source": os.path.join(NATIVE, "event_tests.mncs")},
    {"name": "layout", "source": os.path.join(NATIVE, "layout_tests.mncs")},
    {"name": "render", "source": os.path.join(NATIVE, "render_tests.mncs")},
    {"name": "reconcile", "source": os.path.join(NATIVE, "reconcile_tests.mncs")},
    {"name": "app", "source": os.path.join(NATIVE, "app_tests.mncs")},
]


def resolve_mncs_bin():
    override = os.environ.get("MNCS_BIN")
    if override and os.path.isfile(override):
        return [override]
    lang_dir = os.environ.get("MNCS_LANGUAGE_DIR")
    if not lang_dir:
        lang_dir = os.path.join(os.path.dirname(ROOT), "mncs-language")
    prebuilt = os.path.join(lang_dir, "target", "debug", "mncs")
    if os.path.isfile(prebuilt):
        return [prebuilt]
    return ["cargo", "run", "-q", "-p", "mncs-cli", "--"]


def library_path():
    roots = [os.path.join(ROOT, "src")]
    test_dir = os.environ.get("MNCS_TEST_DIR")
    if not test_dir:
        test_dir = os.path.join(os.path.dirname(ROOT), "mncs-test")
    roots.append(os.path.join(test_dir, "native"))
    lang_dir = os.environ.get("MNCS_LANGUAGE_DIR")
    if not lang_dir:
        lang_dir = os.path.join(os.path.dirname(ROOT), "mncs-language")
    roots.append(os.path.join(lang_dir, "library"))
    return ":".join(roots)


def git_rev(path):
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], capture_output=True,
            text=True, cwd=path).stdout.strip()
    except OSError:
        return "unknown"


def run_suite(suite):
    cmd = resolve_mncs_bin() + ["test", suite["source"], "--format", "json"]
    env = dict(os.environ)
    env["MNCS_LIBRARY_PATH"] = library_path()
    lang_dir = os.environ.get("MNCS_LANGUAGE_DIR")
    if not lang_dir:
        lang_dir = os.path.join(os.path.dirname(ROOT), "mncs-language")
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=lang_dir, env=env)
    try:
        result = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"suite": suite["name"], "status": "ERROR",
                "detail": (proc.stdout[-1500:] + proc.stderr[-1500:])}
    summary = result.get("summary") or {}
    verdict = summary.get("verdict", result.get("classification", "unknown"))
    return {"suite": suite["name"], "status": verdict,
            "passed": summary.get("passed"), "failed": summary.get("failed"),
            "total": summary.get("total"),
            "run_id": result.get("run_id"),
            "test_identities": (result.get("selection") or {}).get(
                "selected_test_identities", [])}


def run_oracle():
    oracle = os.path.join(ROOT, "tools", "oracle_ui.py")
    proc = subprocess.run([sys.executable, oracle], capture_output=True,
                          text=True, cwd=ROOT)
    lines = (proc.stdout or "").strip().split("\n")
    checks = [ln for ln in lines if ln.strip().endswith("OK") or "MISMATCH" in ln]
    mismatches = [ln for ln in checks if "MISMATCH" in ln]
    return {"status": "PASS" if proc.returncode == 0 else "FAIL",
            "checks": len(checks), "mismatches": len(mismatches),
            "tail": lines[-3:] if lines else []}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--suites", default=",".join(s["name"] for s in SUITES))
    parser.add_argument("--evidence-dir", default=None)
    parser.add_argument("--skip-oracle", action="store_true")
    args = parser.parse_args()

    wanted = set(args.suites.split(","))
    outcomes = [run_suite(s) for s in SUITES if s["name"] in wanted]
    oracle_outcome = None if args.skip_oracle else run_oracle()

    failed = [o for o in outcomes if o["status"] != "PASS"]
    if oracle_outcome is not None and oracle_outcome["status"] != "PASS":
        failed.append({"suite": "oracle_ui", "status": oracle_outcome["status"]})
    for outcome in outcomes:
        print("%-16s %-6s passed=%s failed=%s total=%s run=%s" % (
            outcome["suite"], outcome["status"], outcome.get("passed"),
            outcome.get("failed"), outcome.get("total"),
            (outcome.get("run_id") or "-")[:8]))
    if oracle_outcome is not None:
        print("%-16s %-6s checks=%s mismatches=%s" % (
            "oracle_ui", oracle_outcome["status"],
            oracle_outcome.get("checks"), oracle_outcome.get("mismatches")))

    evidence = {
        "schema_version": "mncs-ui.test-evidence/1",
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "ui_rev": git_rev(ROOT),
        "language_rev": git_rev(os.path.join(os.path.dirname(ROOT), "mncs-language")),
        "test_rev": git_rev(os.path.join(os.path.dirname(ROOT), "mncs-test")),
        "suites": outcomes,
        "oracle": oracle_outcome,
    }
    evidence_dir = args.evidence_dir or os.path.join(ROOT, "target")
    os.makedirs(evidence_dir, exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = os.path.join(evidence_dir, "test-evidence-%s.json" % stamp)
    with open(path, "w") as handle:
        json.dump(evidence, handle, indent=1)
        handle.write("\n")
    print("evidence=%s" % path)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
