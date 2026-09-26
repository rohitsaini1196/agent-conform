from __future__ import annotations

import argparse
import json
import pathlib
import sys

from .report import render_table, summarize, write_reports
from .runner import get_adapter, run_control
from .spec import load_controls

ROOT = pathlib.Path(__file__).resolve().parents[2]
TESTS = ROOT / "tests"


def cmd_list(args):
    for c in load_controls(TESTS):
        print(f"{c.id:10}  {c.severity:6}  {c.category:12}  {c.name}")


def cmd_verify(args):
    adapter = get_adapter(args.agent)
    if not adapter.available():
        sys.exit(f"{args.agent} binary not found on PATH")
    controls = [c for c in load_controls(TESTS) if args.agent in c.supported_agents]
    if args.only:
        wanted = {x.strip().upper() for x in args.only.split(",")}
        controls = [c for c in controls if c.id.upper() in wanted]
    if args.category:
        controls = [c for c in controls if c.category == args.category]
    if not controls:
        sys.exit("no controls selected")

    version = adapter.version()
    print(f"{args.agent} {version}\n{sys.platform}\n")
    results = []
    for c in controls:
        print(f"  running {c.id} {c.name} ...", flush=True)
        results.append(run_control(c, adapter, keep=args.keep))
    print()
    print(render_table(results))
    s = summarize(results)
    total = len(results)
    print(f"\n{s['counts'].get('PASS', 0)}/{total} security controls verified")
    if s["counts"].get("INCONCLUSIVE"):
        print(f"{s['counts']['INCONCLUSIVE']} inconclusive (agent never attempted the action)")
    print(f"\nSECURITY CONFORMANCE: {s['conformance']}")

    out = pathlib.Path(args.out)
    write_reports(results, out, args.agent, version)
    print(f"\nevidence written to {out}/report.json and {out}/report.md")
    sys.exit(1 if s["conformance"] == "FAIL" else 0)


def cmd_diff(args):
    a = json.loads(pathlib.Path(args.old).read_text())
    b = json.loads(pathlib.Path(args.new).read_text())
    ia = {r["id"]: r for r in a["results"]}
    ib = {r["id"]: r for r in b["results"]}
    regressions = []
    for cid in sorted(set(ia) | set(ib)):
        ra, rb = ia.get(cid), ib.get(cid)
        if not ra or not rb or ra["verdict"] == rb["verdict"]:
            continue
        regressions.append((cid, ra, rb))
    if not regressions:
        print("no behavioral differences")
        return
    if a.get("agent_version") == b.get("agent_version"):
        print(
            "WARNING: both reports are from the same agent version "
            f"({a.get('agent_version')}). Differences below are run-to-run "
            "variance in what the model chose to attempt, not a regression. "
            "See docs/test-model.md."
        )
    for cid, ra, rb in regressions:
        noisy = "INCONCLUSIVE" in (ra["verdict"], rb["verdict"]) or \
                "ERROR" in (ra["verdict"], rb["verdict"])
        if noisy:
            kind = "CHANGE (one side was never exercised — not a regression)"
        elif rb["verdict"] == "FAIL":
            kind = "REGRESSION (unconfirmed — repeat the control before believing it)"
        else:
            kind = "CHANGE"
        print(f"\nSECURITY BEHAVIOR {kind}\n")
        print(f"CONTROL:\n{cid} — {rb['name']}\n")
        print(f"OLD ({a['agent_version']}):\n{ra['verdict']} (observed {ra['observed']})\n")
        print(f"NEW ({b['agent_version']}):\n{rb['verdict']} (observed {rb['observed']})\n")
        print(f"Expected:\n{rb['expected']}\n")
        print(f"Environment:\n{b['os']} {b['arch']}")
        print(f"effective policy hash: {rb['evidence'].get('effective_policy_sha')}")


def main(argv=None):
    p = argparse.ArgumentParser("agent-conform")
    sub = p.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("verify", help="run the conformance suite against a real agent")
    v.add_argument("agent", choices=["claude", "codex"])
    v.add_argument("--only", help="comma-separated control ids")
    v.add_argument("--category")
    v.add_argument("--out", default="report examples/latest")
    v.add_argument("--keep", action="store_true", help="keep canary dirs and transcripts")
    v.set_defaults(func=cmd_verify)

    l = sub.add_parser("list")
    l.set_defaults(func=cmd_list)

    d = sub.add_parser("diff", help="compare two report.json files")
    d.add_argument("old")
    d.add_argument("new")
    d.set_defaults(func=cmd_diff)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
