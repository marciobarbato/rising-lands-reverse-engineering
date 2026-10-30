# Coordinator handover — 2026-10-29 night (for the next session)

Read this first, then the top of `docs/PROGRESS.md` (round M3R1) and `docs/M3_PLAN.md`. The coordinator's auto-memory holds the standing decisions in short form: Mac mini, Codex as subordinate executor, Rust, assets and public repo. The previous handover, [HANDOVER_CLAUDE_20261029](HANDOVER_CLAUDE_20261029.md), still describes the machines, the leases and the working mode, and remains valid except where this file says otherwise.

## Milestones

| Milestone | State | Where |
|---|---|---|
| M1 load | accepted `927c7e5` | `integracao/validacao/cxr-20261028-08-m1-acceptance.json` |
| M2.1 / M2.2 | accepted `32bb391` / `b9f4b5d` | `cxr-20261029-m2r5-…`, `cxr-20261029-m2r6-…` |
| **M2.3 / M2** | **accepted `ea62eb4`**: 18,401/18,401 phases, 0 crossings, reproduced on MacBook and Mac mini with identical part chain hashes | `integracao/validacao/cxr-20261029-m2r7-m2-3-acceptance.json` |
| M3 | in progress, no criterion accepted yet | this file, PROGRESS "M3 status" |

## Rules learned today

- **Integration.** `scripts/workstream.py integrate` holds a blocking `flock`, so integrations serialize on their own. Never write `pgrep` wait loops: their own command lines match the pattern and they deadlock.
- **Rust engine gate.** `sh motor/validate.sh` runs on every integration (`scripts/workstream.py run_validation`). Since `71c60ce` the engine reads its Python and Graphics references from **fixed git commits** (`motor/testes/pinned_reference.py`), so legitimate upstream Python changes no longer break the gate. If the gate does fail, fix the pin in `motor/` through maintenance; never edit a research front's file from maintenance.
- **Codex bridge.** The `codex` CLI is not on the default PATH. Prefix runs with `export PATH="/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin:$PATH"`. Bridge sessions are `codex exec` runs and do not appear in the Codex app. The user follows them with `python3 local-data/coordination/codex-bridge/codex_watch.py --follow`. Briefs live in `local-data/coordination/codex-bridge/briefs/`.
- **Mac mini.**
  - The session now in use is **"Mini-task M3 harness"** (Remote Control). It has standing permission to push `feat/re-missions` and `runs/*`.
  - The older session "Rising Lands M2.2 Mac mini setup" is idle and must not write.
  - The Claude app on the mini auto-updated at 16:46. That reset the bridge address, so call `ListAgents` again if a send fails.
  - The mini's CLI is not logged in, so headless `claude -p` over SSH does not work. SSH itself works and is the way to run reproductions there.
- **Disk.** Keep ≥ 20 GB free on both machines. The MacBook was at 96% today; the user cleaned it.

## Front state at handover

All of these are pushed. "On main" is as of the end of this session; check `git merge-base --is-ancestor` before acting.

| Front | Executor | Latest delivery | Status |
|---|---|---|---|
| Core | Claude agents | `62575a4` (vision/groups/minimap/recruit exit, 329/0) | on main |
| Economy | Claude | `e5f2cca` (CAVE body `0x426aff`, recruitment, work-cycle composition 402/407) | integration attempted at handover; see PROGRESS |
| AI/runtime | Claude | `6e05fc8` (input path rounds 1–3: InputGame/ProcessInputGame, state 11, keys, Ctrl depot, help pages; 417 native cases, 0 mismatches) | integration attempted at handover |
| Missions | Mac mini | `1191e4c` (probes P1–P7/K1, pass-2 windows P1/P2/P6, S1 input builder stages 1–6) | integration attempted at handover |
| Graphics | Codex | `85dd278` (render API 1.8: P3 3001/3001, P6 2272/2272, P7 3572/3572, K1 501/501 full surfaces under the AffText boundary) | integration attempted at handover |
| macOS | Codex | `c951c76` (Rust renderer in the app, 40.9 fps real UI; Test A answer-stream half 155,597/155,597) | built on ABI 1.3; adopt main's ABI 1.4 before it can pass APP_BUILD |
| Rust engine D | Codex | main has stage 2c (M2.3 logic, 102 fps) and stage 3.1 (renderer 1.7, ABI 1.4, commit-pinned refs) | **stage 4 (player input and orders, ABI 1.5) was in progress in `/Users/marcio/git/Rising-Lands-Codex-Engine` when the MacBook was updated**. It has 33 uncommitted files plus a local merge `367a09b`. Resume with `codex_task.py resume --name rust-engine-frame-logic --brief <short "continue stage 4" brief> --full-access` |
| Combat, Audio | Codex | on main | idle |

## Key M3 facts (native, from the Mac mini probes)

- **CAVE** (type 3): costs 10 food / 6 stone (30/30 → 20/24 at frame 220); complete at 1812; owner stays 0xc8.
- **Cave ownership:** only a **colonist** can enter it. Double-click the sanctuary (tag 33, BatimentRetireColon), select the colonist, click the cave (tag 16/3). It lodges at frame 2178: owner becomes 0, cave count 1, objective mark `0x4e1d88` = 1.
- **Crediting:** only `BatimentAjouteMatiere` credits `0x4e2ea8`, and only while a cave is owned. Delivery is a Ctrl depot order (Ctrl held from the source press to the depot press) or an idle carrier lodging. First credit at frame 3604. Rates are about 1 food per 880–1000 frames per worker and about 1 stone per 1000 frames per builder; only type 7 mines.
- **Recruits:** type 5 costs 4 food (≈270 frames), type 7 costs 6 food (≈570 frames). One pending request per sanctuary; each recruit consumes a colonist.
- **Victory does not fit before the frame-9000 raid.** Plan S1-b recruits 2 builders and 4 workers; victory is estimated near frame 13–14k, through both raids (9000, 10800).
  - At handover the mini was running the continuation from 5300; at frame 9347 food was 21 and stone 43.
  - It will push the result (the victory frame, if reached) and then stay idle.
- **Text:** TextGetMessage is a declared boundary (EAX 0) in the -v2 scenario. TEXTES.TXT is never loaded, and a v3 scenario with text would invalidate the accepted references.

## Next steps (in order)

1. **Reconcile:**
   - Check which of economy/ai-runtime/graphics/missions/macos landed (PROGRESS lists the results), and integrate the rest.
   - macOS needs ABI 1.4 adoption first: resume Codex `macos-live-rust`.
   - Read the mini's S1 result on `origin/feat/re-missions`.
2. **M3.1, first criterion:** AI/runtime proves the whole state over the P1 (129–629) and P2 (129–729) windows with the pass-2 captures. The deliverable is `pesquisas-paralelas/ia-runtime/validacao/m3-1-prova-p1-p2.json`. Then reproduce it on main on both machines and record acceptance of M3.1 (P1/P2 part).
3. **Chain past frame 220:** AI/runtime wires
   - Economy `caverna_recrutamento.corpo_caverna` (provider `BatimentNextEtape:cave`);
   - Core `visao_grupos` (`provedores_visao`, `VisaoGrupos`);
   - Core `entrada_estruturas` (state 13, tags 0x10/0x21);
   - Economy `ciclo_trabalho` (state 5).

   Then rerun P3/P6/P7/K1 and prove P6 (129–2400) whole-state.
4. **Open divergence for Core:** at frame 125, Economy's composition gives DecouvreTerrain → SetMiniMap 196 minimap bytes (from `0x47933a26`; the original goes 32 → 162). See Economy HANDOFF "Cave body, habitation and recruitment".
5. **Graphics stops:** K1/P4/P5 AffGame view origins outside `ORIGENS_PROVADAS`: (1,0), (10,16), (31,0). The P4/P5 screens are not run yet.
6. **Rust stage 4** (orders), then the app's Test A state-hash half, then Test B (a recorded human session replayed on the original; Mac mini).
7. **S1 final:** two full native S1 runs from F0 on the mini, then pass 2, then the M4.1 victory proof. Defeat D1 is still unplanned.

## Quotas and machines at handover

- **Codex:** 57% of the weekly window used; resets 2026-11-04 05:10 BRT. The user wants both quotas used fully by their resets; ask the user for Claude's usage when balancing.
- **Machines:** after-hours MacBook lease has 6 slots, weekdays 08–17 have 3. The mini lease has 5 slots, and about 7 heavy jobs saturate it.

## Reconciliation at handover (21:52, interrupted by the MacBook restart)

- Economy `e5f2cca` integrated: main `3d73142`.
- AI/runtime was in its integration gate when the MacBook restarted. Graphics, missions and macOS were not yet attempted. Rerun `scripts/workstream.py integrate <front>` for each; a killed run leaves main unchanged.
- The Rust engine had committed stage 4 locally (`f4e5abe`, "Port declared player input and orders behind additive Rust ABI 1.5") in `/Users/marcio/git/Rising-Lands-Codex-Engine`. It was unpushed and its final validation was still running. Resume the Codex session to finish and push it, then review it.
- This handover, the PROGRESS M3R1 checkpoint and the ROADMAP note are committed on coordinator/maintenance but not yet integrated. Integrate maintenance last.
