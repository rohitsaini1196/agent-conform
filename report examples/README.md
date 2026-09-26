# Report examples

Real runs against installed Claude Code binaries on macOS 25.6.0 arm64.

| directory | what it is |
|---|---|
| `claude-2.1.219-macos-arm64/` | headline full-suite run, 25 controls |
| `version-matrix.md` | round-2 version comparison, the main artifact |
| `v-2.1.140/`, `v-2.1.143/`, `v-2.1.219/` | full suite, one run per version |
| `rep-<ver>-<n>/` | EXEC-002 repeated 5× per version to measure variance |
| `chain-<ver>-r<n>/`, `chain2-<ver>/` | Adversa 50-subcommand deny bypass attempts at the 2.1.89/2.1.90 boundary |
| `cve-<ver>-r<n>/` | EXEC-006, the destructive-payload version the model refused |
| `cve33068-<ver>/` | CVE-2026-33068 attempts at the 2.1.52/2.1.53 boundary |
| `trial-1/`, `trial-3/`, `rerun/`, `mech-1/`, `mech2-1/` | round-1 runs, incl. the FS-005/006/007/008 differential behind INC-019 |

Each `report.json` carries, per control: agent version and binary, OS and arch,
effective policy plus its SHA, the tool calls the agent actually emitted,
recorded permission denials, observed effects, exit code and a transcript
excerpt. No secrets: canary values are random per-run tokens in fabricated files.

**Paths are redacted.** Absolute paths in these reports have had the operating
user's home directory replaced with `/Users/REDACTED`. Nothing else is altered.
Canary values are random per-run tokens in fabricated files; no real credential,
key or host appears anywhere in this directory.
