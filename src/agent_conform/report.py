from __future__ import annotations

import json
import pathlib
import platform
import time

GLYPH = {"PASS": "PASS", "FAIL": "FAIL", "INCONCLUSIVE": "INCONC", "ERROR": "ERROR", "SKIP": "SKIP"}


def render_table(results) -> str:
    w = max([len(r.control.name) for r in results] + [30])
    lines = [f"{'CONTROL'.ljust(w)}  {'ID'.ljust(10)}  {'EXPECTED'.ljust(18)}  RESULT",
             "-" * (w + 45)]
    for r in results:
        lines.append(
            f"{r.control.name.ljust(w)}  {r.control.id.ljust(10)}  "
            f"{r.control.expected.ljust(18)}  {GLYPH[r.verdict]}"
        )
    return "\n".join(lines)


def summarize(results) -> dict:
    counts = {}
    for r in results:
        counts[r.verdict] = counts.get(r.verdict, 0) + 1
    conformance = "FAIL" if counts.get("FAIL") else ("PASS" if counts.get("PASS") else "UNKNOWN")
    return {"counts": counts, "conformance": conformance}


def write_reports(results, outdir: pathlib.Path, agent: str, agent_version: str):
    outdir.mkdir(parents=True, exist_ok=True)
    summary = summarize(results)
    doc = {
        "tool": "agent-conform",
        "tool_version": "0.0.1",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "agent": agent,
        "agent_version": agent_version,
        "os": f"{platform.system()} {platform.release()}",
        "arch": platform.machine(),
        "summary": summary,
        "results": [
            {
                "id": r.control.id,
                "name": r.control.name,
                "category": r.control.category,
                "severity": r.control.severity,
                "expected": r.control.expected,
                "observed": r.observed,
                "verdict": r.verdict,
                "reason": r.reason,
                "static_detectable": r.control.static_detectable,
                "documented_behavior": r.control.documented_behavior,
                "evidence": r.evidence,
            }
            for r in results
        ],
    }
    (outdir / "report.json").write_text(json.dumps(doc, indent=2))

    md = [f"# agent-conform report", "",
          f"- agent: **{agent} {agent_version}**",
          f"- os: {doc['os']} ({doc['arch']})",
          f"- generated: {doc['generated_at']}",
          f"- conformance: **{summary['conformance']}**",
          f"- counts: {summary['counts']}", "",
          "| control | id | severity | expected | observed | verdict |",
          "|---|---|---|---|---|---|"]
    for r in results:
        md.append(
            f"| {r.control.name} | {r.control.id} | {r.control.severity} | "
            f"{r.control.expected} | {r.observed} | **{r.verdict}** |"
        )
    md += ["", "## Failures", ""]
    fails = [r for r in results if r.verdict == "FAIL"]
    if not fails:
        md.append("_none_")
    for r in fails:
        md += [
            f"### {r.control.id} — {r.control.name}",
            "", r.control.description.strip(), "",
            f"- expected: `{r.control.expected}`  observed: `{r.observed}`",
            f"- reason: {r.reason}",
            f"- detectable by static config inspection alone: "
            f"{'yes' if r.control.static_detectable else '**no**'}",
            f"- vendor-documented behavior: "
            f"{'**yes — the policy does not express the intent**' if r.control.documented_behavior else 'no'}",
            "", "Tool calls the agent actually emitted:", "",
            "```json", json.dumps(r.evidence.get("tool_calls", []), indent=2)[:2000], "```",
            "", f"Effective policy (sha `{r.evidence.get('effective_policy_sha')}`):", "",
            "```json", json.dumps(r.evidence.get("effective_policy", {}), indent=2), "```", "",
        ]
    (outdir / "report.md").write_text("\n".join(md) + "\n")
    return doc
