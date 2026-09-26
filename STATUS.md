# Status

This project is an experimental research harness. The current implementation
focuses on Claude Code runtime policy behavior. It is useful for
experimentation and reproducibility, and it should not be treated as a
production security certification tool.

## Scope

- **Agent:** Claude Code only. The Codex adapter is a stub that exists to show
  where agent-specific code lives.
- **Platform:** macOS 26.6 / Darwin 25.6.0, arm64. Never run on Linux or
  Windows; no results exist for those platforms.
- **Versions exercised:** `2.1.140`, `2.1.143`, `2.1.219` (full suite),
  `2.1.278` (the INC-019 control set), and `2.1.52`, `2.1.53`, `2.1.89`,
  `2.1.90` (individual controls).
- **Controls:** 30, as data in `tests/`.

## What is settled

- A deny rule using the `//<absolute-directory>/**` pattern form was not
  applied to `cat` through the Bash tool on 2.1.219, while the same rule was
  applied to the built-in `Read` tool. This does not reproduce on 2.1.278.
  Write-up: [research/INC-019-disclosure.md](research/INC-019-disclosure.md).
- Single-run version-to-version diffs are unreliable. Model variance produces
  apparent behavior changes that repetition does not support. Method and data:
  [docs/experiments-round2.md](docs/experiments-round2.md).
- The harness produced two classes of false finding of its own, both
  documented. See [docs/test-model.md](docs/test-model.md).

## What is open

- The managed-settings layer is untested. `--settings` is a user-level source,
  and `CLAUDE_CODE_MANAGED_SETTINGS_PATH` does not redirect the managed layer
  on 2.1.219. Testing it properly needs a root-owned file in a disposable VM.
- `FS-009` is marked `UNVERIFIED` and must not be cited: we could not confirm
  the setting it exercises is recognized.
- Which release between 2.1.220 and 2.1.278 changed the INC-019 behavior was
  not bisected.
- No Linux or Windows coverage.

## Maintenance

Archived research. Bug fixes and additional control specs are welcome; the
implementation is deliberately small and is not being expanded.
