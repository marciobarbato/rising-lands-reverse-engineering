# Coordinator handover — 2026-10-30 19:10 (paused until the Codex quota reset)

Read this first, then the indicators table at the top of `docs/PROGRESS.md`, `docs/M3_PLAN.md` (status table) and the "After MONDE01" section of `docs/ROADMAP_MONDE01.md`.
- The earlier handovers ([0700](HANDOVER_CLAUDE_20261030_0700.md), [20261030](HANDOVER_CLAUDE_20261030.md), [20261029](HANDOVER_CLAUDE_20261029.md)) still describe machines, leases and working mode. Where they differ, this file wins.
- The coordinator's auto-memory holds the standing decisions (see "User decisions" below).

**Pause.** The user paused new work until the Codex weekly quota resets (88% used at 19:07; reset 2026-11-04 05:10 BRT, possibly earlier if Codex grants a bonus reset). The agreed stop line is 95% used. At the stop line, running tasks finish, results are integrated and docs updated, and nothing new starts.

## State at the pause

**Main:** `631d76b`. Everything below is integrated and gate-checked unless marked otherwise.

| Item | State |
|---|---|
| M1, M2 | accepted |
| **M3.1** | **P1/P2 accepted** at `c9c85eb`; **P6 accepted** at `92fab50` (4,544/4,544 phases, both machines). The S1 window is open. |
| S1 chain reach (Python, strict) | **10,800 / 17,050 frames** on main (11,752 in planning mode). Stops are in `pesquisas-paralelas/ia-runtime/S1_NEXT_STOPS.md`. |
| M3.2 render | Graphics API 1.10: S1 order windows 130–5,090 give 2,792/2,792 full surfaces |
| M3.3 app | Test A state half 6/6 probes. Test B pipeline ready: synthetic prefix 222/222 on the original. Human Test B is blocked by the text glyphs (`0x459454`). |
| M3.5 | 60 game fps with orders; Rust logic ~0.3 ms/frame. The app plays the original **sound effects** (`e4be826`). |
| M4.1 / M4.2 | Original S1 victory and D1 defeat captures are replay-equal on main; no chain proof yet |
| Campaign inventory | 38 maps/25 stages on main (`pesquisas-paralelas/inventario-campanha/`). Most content: MONDE23 (tied with MONDE17A); +MONDE25 covers 56/62 static selectors |

**Not on main yet** (pushed branches; integrate first after the pause):
1. `feat/re-missions` `86c27f0`: **pass-2 S1 whole-state capture**, parts 00–16 (246 MB), mask and policy (passed, 33,844 phases), plus the Stage 22 docs.
   - The local `worktrees/re-missions` holds an unpushed merge of main from an interrupted integration. `scripts/workstream.py integrate missions` will push it; don't `reset --hard` it.
2. `feat/codex-rust-engine` `aaf7705`: Rust S1 to frame 10,800 (state) and 2,013 (surfaces), plus K1 complete.
   - Integrate through maintenance after a short reproduction (K1 501/501 and M2.2 257/257 were reproduced on `1f7590a`).
   - Use the pin profile that the branch's `motor/testes/pinned_reference.py` names.
3. `feat/re-graphics` `bc38477`: native bitmap tooltips (glyph work). **The Codex session `graphics-s1-render` may still be running** (glyphs `0x459454`, then late-S1 combat/fire/death rendering).
   - Let it finish. Integrate its pushed head.
   - If it left WIP, park it on a `wip/*` branch first.

## Next steps (in order)

1. Integrate Missions (pass-2 S1). Then run AI/runtime's formal S1 proof.
   - Brief: `local-data/coordination/codex-bridge/briefs/ai-runtime-s1-proof-run.md`.
   - Commands: `provar_entrada_janelas_ia.py fixar S1 --ref origin/main`, then `tudo --janelas S1`.
   - Expected: strict reach ~10,800; any first *difference* matters most.
   - Reproduce on both machines and record the M3.1 S1 partial result.
2. Integrate the Rust engine `aaf7705` and Graphics.
3. Push the S1 chain past 10,801. Owners and contracts are in `S1_NEXT_STOPS.md`.
   - Graphics: AffGame with 2 monsters, guard `0x41591f`.
   - Then the frame-11,753 sound stop, already fixed by Combat in `631d76b`.
   - Then the raid AI and combat to the victory (frame 16,933 → MissionNext 17,043).
   - Loop: AI/runtime runs the indicator check, the owner fixes original-first, integrate, rerun.
4. M3.3 human Test B once the glyphs land.
   - The user records a session in the app; docs/MACOS_PLAYABLE.md has "Recording the real human session".
   - Replay it on the mini with `apps/macos-preview/scripts/test_b_pipeline.py original …`.
5. M4.1/M4.2 chain proofs over S1 and D1. Combat's fatal windows on the mini are pending (commands in `pesquisas-paralelas/combate/FATAL_MAC_MINI_RUNS.md`; start snapshots kept in the mini's `.local/m3/passo2/S1` and `.local/m3/d1final`).

## User decisions (also in auto-memory)

- **After MONDE01:**
  - Reduced rigor for **all** missions, MONDE23 included: Rust-direct, automatic validation by routine and by checkpoint, no frame-by-frame replay, no hand scripts.
  - Go back to full rigor if something looks wrong.
- **Release-only (human version):** the speed selector and opening straight into the game.
- **Progress reporting:** lead with the measured indicators (above all the S1 frame reach) and revise the % on every acceptance. Estimate now ~60% (50–70%).
- **Pause means let finish:** never force-kill running work unless the user says so explicitly.
- **Claude vs Codex usage:** prefer Codex when Claude usage is high; the Codex stop line is 95%.

## Machines and housekeeping

- **MacBook:**
  - 126 GB free after cleanup: old app builds `local-data/macos-playable/previous`, 51 stale build-source copies, stale integration candidates and scratch worktrees.
  - Two build-source dirs could not be removed: `1486c82…`, `709b606…`.
- **Mac mini** (`marciobarbato@192.168.68.63`, Wi-Fi only):
  - Idle, 85 GB free. It **rebooted unexpectedly at 15:26**.
  - Ask the user to turn off automatic macOS updates. Neither the coordinator nor the mini session changes system settings.
  - Optional cleanup is awaiting the user: about 8 GB of old verification worktrees, `.local/m3/s1dev` and `.local/m3/d1`.
- **Safety checks:** recursive deletes need literal absolute paths or `${VAR:?}` guards. Remote deletions over SSH and `git reset --hard` were refused by the safety checks; ask the user.
- **Unvalidated parked work:** `origin/wip/*` (rust 0715/chain-0700, economy transporte/0700/0715, graphics codex-0430/0700/0715, macos abi16-0700/abi16-runs-0715/0715). Diff each before reuse.

## Lessons from today (also in PARALLEL_WORK/AGENTS)

- **Integration:**
  - Never commit into a worktree while `workstream.py integrate` runs from it. The post-push ancestry check fails even though main was pushed.
  - A branch the mini pushes to while an integration merges main into it diverges. Merge, don't reset.
- **Pass-2 segment runs:**
  - Verify `relatorio` on a small set that includes segments ≥ 10000 before the long run. The glob bug `politica-0*` cost a day.
  - Never let two dispatch queues share a skip list.
- **Codex:**
  - "Selected model is at capacity" errors are transient; resume the same session.
  - Very long threads fail at compaction; start a fresh session with a handover brief.
- **Rust reproductions:** use the branch's own reference pin profile (`RL_REFERENCE_PROFILE`). The default profile compares against old Python and stops at frame 220.
