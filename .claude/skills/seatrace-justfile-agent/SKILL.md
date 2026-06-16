---
name: seatrace-justfile-agent
description: SeaTrace MSC-v007 demo repo lane skill. Load before any write to this repo. Enforces lane split (Codex = hero/UI, Claude = docs/bootstrap), boundary rules, and harness proof gate.
metadata:
  type: skill
  version: "1.0"
  project: SeaTrace MSC-v007 Demo
  repo: seatrace-msc-v007
  last_updated: 2026-06-15
---

# SeaTrace MSC-v007 — Agent Lane Skill

## Gate state

```
GO-PREVIEW-BRANCH-PROOF-ONLY
NO-GO-PRODUCTION-DEPLOY
NO-GO-LIVE-PO-PARTNER-MSC-CLAIMS
```

---

## Lane split (hard boundary — no exceptions)

| Lane | Agent | Files | Rule |
|---|---|---|---|
| Hero / UI | **Codex** | `index.html`, `seo/peterpan_publix_sockeye.html`, `assets/css/msc-v007-demo.css`, `assets/js/` | Codex owns. Claude does NOT touch. |
| Docs / Bootstrap | **Claude Code** | `README.md`, `.netlifyignore`, `docs/AGENT_LEDGER.md`, `.claude/skills/` | Claude owns. Codex does NOT touch. |
| Deploy | **Owner** | `netlify.toml`, Netlify CLI commands | Owner GO #7 minimum. No agent may deploy unilaterally. |
| Harness proof | **Codex / CI** | `src/seatrace_4p3l/`, `tests/`, `justfile` | Proven at commit `4fe4264`. Do not regress. |

---

## Boundary gate (run before every commit or PR)

```bash
grep -RInE 'C:\\\\|OneDrive|\$CHECK|\$BOOK|invoice|margin|COGS|GPS|settlement|advance_amount|real-time vessel|exact coordinates|SeaTrace003|SeaTrace002|SeaTrace-ODOO|Roberto002|worldseafood@gmail' \
  README.md index.html seo/ assets/ 2>/dev/null
```

Expected: no output. Any match = NO-GO.

---

## Harness proof gate

```bash
cd C:\WSP001\seatrace-msc-v007
just install
just verify
```

Both must PASS before any PR merge or Netlify deploy.

---

## Commit rule

1. Open a ledger claim in `docs/AGENT_LEDGER.md` before any write
2. No `git commit` without Owner GO
3. No `netlify deploy` without campaign GO #7 minimum
4. Co-Authored-By trailer required on every commit

---

## QA recheck scope (post Codex patch)

After Codex closes the `seo/` asset path fix, QA runs a narrow check on:

- `index.html` — step 08 renders correctly; hero wording public-safe; no brand names in public hero
- `seo/peterpan_publix_sockeye.html` — assets load correctly on preview URL
- `assets/css/msc-v007-demo.css` — no private values or raw numbers in CSS variables

Expected: all three pass boundary gate AND visual load check before Preview GO.

---

## Unresolved at bootstrap (2026-06-15)

| Item | Blocker |
|---|---|
| `README.md` fixes not committed | Owner GO required for `git add README.md .netlifyignore && git commit` |
| `.netlifyignore` untracked | Same commit |
| Campaign `settings.json` hook fix | Owner must apply 2-line PowerShell fix natively (unblocks campaign SKILL.md v1.4 write) |
| `seo/` asset paths broken on preview | Codex patch lane — not Claude |

---

*For the Commons Good — WSP001*
