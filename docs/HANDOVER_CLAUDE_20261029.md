# Coordinator handover — 2026-10-29

This handover is for a fresh Claude coordinator session. Read it first, then `docs/PROGRESS.md` (the top sections) and `docs/M3_PLAN.md`. The coordinator's auto-memory, which loads automatically, holds the same standing decisions in short form.

## State at handover (main `3579c40` or later)

- **Accepted:**
  - M1, the MONDE01 load (`927c7e5`);
  - M2.1, the first frame (`32bb391`, [record](../integracao/validacao/cxr-20261029-m2r5-m2-1-acceptance.json));
  - M2.2, 128 frames (`b9f4b5d`, [record](../integracao/validacao/cxr-20261029-m2r6-m2-2-acceptance.json)).
- **In progress: M2.3, the first scripted raid.**
  - The window is frames 0–9,200: the raid spawns at frame 9000 and the first path search runs at 9177–9179.
  - The Mac mini is producing the original evidence: 1,000-frame xz parts, a cumulative policy and docs on `feat/re-missions`. The expected push is about 17:15–17:45 BRT on 2026-10-29.
  - The Python side is ready on main:
    - Core: live movement, path search with byte-exact scratch, the grid sharing fix;
    - AI/runtime: raid rules and the segmented comparator (`comparar_quadros_ia.py`; `provar_quadros_ia.py` is the M2.2 proof pattern);
    - Economy: timers.
  - The composition runs counters 9000–11999 with no stop.
- **M2 is accepted only when M2.3 is.**

## Next steps (M2.3 closure)

1. When the Mac mini reports the M2.3 SHAs, integrate `feat/re-missions`. The local worktree is `worktrees/re-missions`: fast-forward it to origin, then run `python3 scripts/workstream.py integrate missions` from it.
2. Spawn a fresh agent (AI/runtime front, `worktrees/re-ai-runtime`) to run the FORMAL M2.3 comparison of all parts with the segmented comparator against the published parts and cumulative policy. It is Python-only. Deliverable: `validacao/m2-3-prova-9200-quadros.json` in the M2.2 proof shape: per-phase equality of every compared byte, allocation records, RNGs, bindings and boundaries outside display, registers, and zero crossings writing compared bytes.
3. Reproduce the proof on main on both machines: the MacBook directly, the Mac mini through its Remote Control session or SSH.
4. Record the acceptance like M2.2: an `integracao/validacao/` record, PROGRESS with a dated snapshot and the index entry, the ROADMAP update. M2 is then accepted.
5. Start M3 per `docs/M3_PLAN.md`.

## Known open item for the macOS front

main carries Graphics render API 1.3, but the macOS consumer still pins 1.2, so the app build fails until Codex workstream A accepts 1.3. The task is already sent.

## Machines and execution

- **MacBook Pro** (the user's workstation, user `marcio`):
  - heavy lease `local-data/coordination/heavy_lease.py` with 3 slots Mon–Fri 08:00–17:00 and 6 otherwise;
  - native runs of at most about 20 min here;
  - non-native gates run outside the lease.
- **Mac mini** (M4, 4P+6E, 16 GB, user `marciobarbato`):
  - `ssh marciobarbato@marcios-Mac-mini.local` works; the checkout is at `~/git/Rising Lands/`;
  - Remote Control session "Rising Lands M2.2 Mac mini setup". This coordinator needs Remote Control ON to see and message it;
  - it is the sole writer of `feat/re-missions` and the runner for long jobs, publishing `runs/<front>/<tag>` branches parented on the requesting SHA;
  - its lease has 5 slots by default; about 7 heavy jobs saturate the CPU;
  - the user delegated milestone go-aheads for the mini to the coordinator ("sem minha interação"). Quote that if the mini asks.
- **Cross-machine paths:** the MacBook has `/Users/marciobarbato -> /Users/marcio`, and RISING.EXE and the `source/python` hash match the mini. Cross-machine segment runs are possible from M3 on.
- **Native C pass-2 hooks** (Core `5580c2d`, `docs/core/NATIVE_POLICY_HOOKS.md`) are 6.45× faster with byte-identical policies. Use them for all future long policy runs, after an equality check on each machine.

## Working mode (user preferences)

- **One chat.** New work goes to fresh Agent subagents with concise, complete briefs (goal, worktree and branch, owned paths, the front's HANDOFF.md, the original-first rule, gates, what to return). Do not open new sidebar sessions. The five front sessions are archived; their worktrees remain under `worktrees/re-*`.
- **Reports to the user** in Brazilian Portuguese, brief.
- **Integration:**
  - always `scripts/workstream.py integrate <front>` from a clean feature worktree;
  - never force-push;
  - verify ancestry;
  - reproduce acceptance evidence on main before recording it.
- **Commits** end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## External Codex workstreams

They report through pushed branches plus the user, and the coordinator reviews and integrates. The record is in `local-data/coordination/claude-20261028/external-workstreams.md`.

| Workstream | Branch | How it integrates |
|---|---|---|
| A. macOS layer | `feat/codex-macos-m3-preparation` | merge into `feat/macos-playable`, then `integrate macos`. The native build and UI smoke run in the gate with explicit `--inputs-root`/`--data-root`. A first-try UI-smoke timeout under load happened once, and the retry passed. |
| B. Audio | `feat/re-audio` | `integrate audio` |
| C. Player-action map | — | integrated |
| D. Rust engine pilot | `feat/codex-rust-engine`, path `motor/` | integrated (`33842de`): C ABI 1.0, 75/75 equal. Validate with `./motor/validate.sh` (rustc 1.99.1 on both Macs). TODO: add it to the maintenance gate |
| E. Asset extraction | data goes to `rising-lands-assets` with a release tag; tooling goes to `feat/codex-assets-tooling` | integrate only the tooling branch, through maintenance; never `feat/codex-assets` |
| F. Hidden-difficulty scan | `feat/codex-difficulty-scan` | integrated (`33842de`): four hidden MONSTRE.INI targeting keys, no selectable difficulty |

New paths that no front owns (`motor/`, `assets/`, `pesquisas-paralelas/mapa-acoes-jogador/`, `pesquisas-paralelas/dificuldade/`) come in through `coordinator/maintenance`. Declare owners in `scripts/workstream.py` when a workstream becomes long-lived.

## Architecture decisions (user, 2026-10-29)

- **Engine language:** the playable engine is a native **Rust** port. **Python** stays the validated reference and test harness, **C** is only for small tooling, and **Swift** is the macOS shell, calling Rust through a C ABI. The Python research tooling (emulator, captures, masks, comparators) stays in Python.
- **1. State:** idiomatic Rust structures, plus a tested **projection** to the original memory layout for byte-exact comparison.
- **2. Pace:** fixed-step deterministic ticks decoupled from host speed. Ticks/second is configurable, with a period-like default; logic wall-clock reads come from a virtual tick clock.
- **3. Presentation:** the original 800×600 8-bit frame, scaled. The renderer is separable for a future HD version.
- **4. Assets:** extracted assets live in the SEPARATE public repo `marciobarbato/rising-lands-assets`, with a local clone at `/Users/marcio/git/Rising Lands/rising-lands-assets` and an HTTPS remote (SSH to GitHub is not configured on the MacBook). They are bundled with the app. The code repo keeps only the extractor and the pin `assets/ORIGIN.json`. Never merge `feat/codex-assets`, the ~630 MB payload branch. Delete it from the code remote only after confirming the assets repo holds byte-identical content.
- **Repository:** it is PUBLIC and already contains game-derived evidence. The user accepts this and will make it private only if someone complains. Do not re-raise it or hold pushes over it.
- **Future, after M4:** a per-mission difficulty selector (no original setting is known; a hidden-parameter scan is in workstream F), an HD renderer, adjustable speed.
- **Scope** stops at MONDE01 (M4). No other missions without authorization.
