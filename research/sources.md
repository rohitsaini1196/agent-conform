# Sources

Collected 2026-09-20. Grouped by what they were used for.

## Vendor bug reports (the incident catalogue)

Claude Code:
- #31925 Managed settings deny rules from Console not enforced — https://github.com/anthropics/claude-code/issues/31925
- #86253 managed-settings disableBypassPermissionsMode does not block --dangerously-skip-permissions — https://github.com/anthropics/claude-code/issues/86253
- #70181 Empty server-managed settings (304 cached) zero out local managed-settings.json — https://github.com/anthropics/claude-code/issues/70181
- #95233 managed-settings sandbox.network.deniedDomains not enforced for Bash in VS Code extension — https://github.com/anthropics/claude-code/issues/95233
- #88795 Read tool ignores permissions.deny Read(/Users/**) — https://github.com/anthropics/claude-code/issues/88795
- #89346 Managed settings defaultMode no longer respected — https://github.com/anthropics/claude-code/issues/89346
- #88590 Local managed-settings allowedChannelPlugins silently discarded — https://github.com/anthropics/claude-code/issues/88590
- #91816 Regression in 2.1.259: managed-settings discovery on WSL fails fatally — https://github.com/anthropics/claude-code/issues/91816
- #40495 Cowork sessions ignore user hooks and managed settings — https://github.com/anthropics/claude-code/issues/40495
- #86478 bypassPermissions defaultMode and --permission-mode flag ignored — https://github.com/anthropics/claude-code/issues/86478
- #84231 Managed-settings policy key to suppress session-scoped bulk permission grants — https://github.com/anthropics/claude-code/issues/84231
- #88564 Settings schema validation failures should be more fault-tolerant — https://github.com/anthropics/claude-code/issues/88564
- #27040 Deny permissions in .claude/settings.json ignored (2.1.49, WSL) — https://github.com/anthropics/claude-code/issues/27040
- #26334 / #25621 Permission deny rules not enforced for Bash — https://github.com/anthropics/claude-code/issues/26334
- #24846 Read deny permissions not enforced for .env — https://github.com/anthropics/claude-code/issues/24846
- #6699 deny permissions in settings.json are not enforced (1.0.93) — https://github.com/anthropics/claude-code/issues/6699
- #6631 Permission deny not enforced for Read/Write (1.0.93, RHEL) — https://github.com/anthropics/claude-code/issues/6631

Codex:
- #44964 Managed requirements.toml rules do not fire for nested shell scripts — https://github.com/openai/codex/issues/44964
- #14068 app-server runs tools in read-only sandbox despite --dangerously-bypass-approvals-and-sandbox — https://github.com/openai/codex/issues/14068
- #13095 Unicode confusable characters can bypass exec policy matching — https://github.com/openai/codex/issues/13095
- #5038 VS Code extension ignores approval_policy="never" — https://github.com/openai/codex/issues/5038
- codex-plugin-cc #75 Codex plugin bypasses project-level Claude Code deny rules — https://github.com/openai/codex-plugin-cc/issues/75

## Adjacent tooling in this space
- OWASP Agent Security Regression Harness — https://github.com/OWASP/Agent-Security-Regression-Harness
- Clauditor (security configuration scanner for Claude Code) — https://github.com/gabrielsoltz/clauditor
- OpenACA (Open Agent Composition Analysis) — https://github.com/open-agent-security/openaca
- HOL Guard — https://hol.org/guard/features , Claude Code guide: https://hol.org/guard/security/harnesses/claude-code
- HOL Guard coverage — https://www.helpnetsecurity.com/2026/08/25/hol-guard-open-source-antivirus-ai-agents/
- AgentCheck (devlyai) — https://github.com/devlyai/AgentCheck
- Anthropic claude-code-security-review — https://github.com/anthropics/claude-code-security-review
- Zenity, coding & personal agents — https://zenity.io/use-cases/agent-type/coding-personal-agents
- Endor Labs, security for AI coding agents and workstations — https://www.endorlabs.com/learn/introducing-security-for-ai-coding-agents-and-workstations
- Zenity vs Noma comparisons — https://langguard.ai/alternatives/zenity-vs-noma/ , https://www.kosmoy.com/resources/blog/zenity-vs-noma-security/
- awesome-ai-security-tools — https://github.com/scadastrangelove/awesome-ai-security-tools

## Research
- Distributing Security Controls Through Harness Engineering (SHarD) — https://arxiv.org/html/2607.25890v1
- VeriGrey: Greybox Agent Validation — https://arxiv.org/pdf/2603.17639
- MalSkillBench: Runtime-Verified Benchmark of Malicious Agent Skills — https://arxiv.org/pdf/2606.07131
- Formal Policy Enforcement for Real-World Agentic Systems — https://arxiv.org/pdf/2602.16708
- Clawed and Dangerous: Can We Trust Open Agentic Systems? — https://arxiv.org/pdf/2603.26221

## Enterprise deployment practice and managed configuration
- Claude Code permissions docs — https://code.claude.com/docs/en/permissions
- Claude Code enterprise rollout playbook for 50+ developers — https://systemprompt.io/guides/claude-code-organisation-rollout
- Enterprise Claude Code with managed settings — https://systemprompt.io/guides/enterprise-claude-code-managed-settings
- General Analysis, Claude Code enterprise security deployment — https://generalanalysis.com/guides/claude-code-enterprise-security-deployment
- General Analysis, how to secure Claude Code — https://generalanalysis.com/guides/how-to-secure-claude-code
- General Analysis, settings/permissions/Bash tool security — https://generalanalysis.com/guides/claude-code-settings-permissions-bash-tool-security
- TrueFoundry, Claude enterprise security — https://www.truefoundry.com/blog/claude-enterprise-security
- PlatformSecurity, securing a Claude Enterprise tenant — https://platformsecurity.com/blog/how-to-secure-your-claude-enterprise-tenant
- VerityAI, Claude Code enterprise governance CISO playbook — https://verityai.co/blog/claude-code-enterprise-ai-development-governance-guide
- Repello AI, Claude Cowork security deployment guide — https://repello.ai/blog/claude-cowork-security
- OWASP AI Agent Security Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html
- OWASP Top 10 for Agentic Applications 2026 — https://goteleport.com/blog/owasp-top-10-agentic-applications/

## Local
- `claude --help`, Claude Code 2.1.219, macOS 25.6.0 arm64
- `report examples/` in this repository — runs performed 2026-09-20

## Added during the version-differencing experiments (2026-09-20)

CVEs and disclosures:
- CVE-2026-33068 (CVSS 8.8, trust-dialog bypass, fixed 2.1.53) — https://nvd.nist.gov/vuln/detail/CVE-2026-33068
- CVE-2026-25723 (piped sed/echo file-write sandbox escape, fixed 2.0.55) — https://github.com/advisories/GHSA-mhg7-666j-cqg4
- CVE-2025-59536 (8.7, pre-trust hook RCE / MCP consent bypass, fixed 1.0.111) and CVE-2026-21852 (5.3, API key exfil, fixed 2.0.65) — https://www.mintmcp.com/blog/claude-code-cve
- Six-exploit roundup incl. the Adversa 50-subcommand deny-rule bypass (fixed 2.1.90) — https://venturebeat.com/security/six-exploits-broke-ai-coding-agents-iam-never-saw-them
- Claude Code CVE list — https://vulners.com/search/vendors/anthropic/products/claude%20code

Version pinning and rollout practice:
- requiredMinimumVersion / requiredMaximumVersion, managed-only, added CLI 2.1.163 (June 2026) — https://code.claude.com/docs/en/setup
- Update and pinning guide — https://continuumcode.ai/guides/claude-code-update/
- Enterprise rollout playbook (pilot 5–10 devs, staged expansion) — https://systemprompt.io/guides/claude-code-organisation-rollout
- Managed settings enterprise policy guide — https://localskills.sh/blog/claude-code-managed-settings
- Claude Code governance / usage policy — https://www.truefoundry.com/blog/claude-code-governance-building-an-enterprise-usage-policy-from-scratch
- Auto-update bricking incident (March 2025) — https://techcrunch.com/2025/03/06/anthropics-claude-code-tool-had-a-bug-that-bricked-some-systems

Local experiments: `docs/experiments-round2.md`, `report examples/` (v-*, chain-*, chain2-*, cve-*, cve33068-*, rep-*)
