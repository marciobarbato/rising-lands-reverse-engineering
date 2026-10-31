# Roadmap to a playable Rising Lands for Mac

Written 2026-10-31 at main `559f148`. **This document supersedes [ROADMAP_MONDE01](ROADMAP_MONDE01.md) and [M3_PLAN](M3_PLAN.md) as the plan of record.** Those two documents, the acceptance records in `integracao/validacao/` and every proof already on main stay valid as history. Nothing accepted is reopened.

## 1. Goal

The user wants the experience of playing Rising Lands in 1997, on a modern Mac, with modern conveniences. The deliverable is a game, not an equivalence proof.

**Definition of done (the "human release"):**
- The macOS app opens into the original PT-BR main menu and plays the whole campaign: 25 stages, briefings, victory and defeat screens, stage progression with the original carry-over (experience, research, players).
- Gameplay feels like the original: same units, buildings, economy, AI raids, mission objectives, sprites, sound effects and music.
- Modern tools: game speed (0.5x–4x and pause), difficulty presets, save and load anywhere, scalable window and fullscreen, at least 60 fps.
- A human can play any mission for an hour without a freeze, crash or engine stop.

**Fidelity target: behaviourally faithful, not byte-exact.** The rules, numbers and AI decisions come from the original code, so the game plays the same. Differences invisible to a player (RNG call order inside a frame, scratch memory, display-only bytes, timing of an animation by one frame) are acceptable and are not investigated.

## 2. Diagnosis of the previous plan

In five days (26–30 October) the project produced 1,441 commits, ~115,000 lines of Python reference, ~25,000 lines of Rust and ~35,600 lines of Markdown. It accepted 4 of 12 criteria and proved the S1 victory script through frame 10,800 of 17,050. That is real, reusable progress: load, 9,200 autonomous frames with the first raid, player orders, rendering, sound and a 60 fps app.

But a human still plays only 5–15 seconds before the engine stops. The reasons:
- **Validation was path-based.** Everything the scripted probes touched is proven; everything else is a named stop (242 stop sites in `motor/`). Free play leaves the scripted path almost immediately.
- **Each routine was translated twice** (x86 → Python → Rust) and proven by whole-state equality per phase (~16 MB compared per phase, masks with writer/reader proofs, two-machine reproduction, a JSON acceptance record per sub-criterion). That rigor buys preservation-grade fidelity the goal does not need.
- **Coordination overhead.** Seven fronts, rounds, handovers every few hours, lease scheduling and integration locks cost a large share of both quotas.
- **The Rust engine cannot load a mission.** It starts from the captured MONDE01 post-load state (S0). No other stage can start.

## 3. New rules (replace the original-first rules where they conflict)

| Topic | Before | Now |
|---|---|---|
| Acceptance | Whole-state equality per phase against a native capture, two machines | The game runs without stops and behaves like the original in automated and human play (section 5) |
| Translation path | Capture → Python → prove → Rust → prove | **Ghidra/asm → Rust directly.** No new Python. Existing Python stays frozen as a reference |
| Primary metric | Frames of a scripted run proven equal | **Stop-free play time** under the play bot, then stages completable |
| Work order | Depth: finish one scripted path exactly | **Breadth:** port the stops actually hit in play, most frequent first |
| Unknown behaviour | Named stop, never a default | Same in tests. In play mode a stop must never freeze the game (section 4, P1) |
| Divergence | Every byte investigated | Investigate only divergences a player could notice: unit positions, resources, health, deaths, objectives, AI decisions, pixels of sprites and terrain |
| Proof artefacts | Acceptance JSON per sub-criterion, two-machine reproduction | One line in `docs/PROGRESS.md` per phase exit, with the command that shows it |
| Documentation | Domain manuals, handoffs, progress, status, roadmap, M3 plan, handovers | This roadmap, `docs/PROGRESS.md` (short), `motor/HANDOFF.md`, and one handover per session |

Kept unchanged: the intact `RISING.EXE` (SHA-256 `6c556520…8543fb`) is the only oracle; no invented game rules (when the behaviour is unknown, read the asm); explicit wrapping arithmetic; Rust engine, Swift shell, C only for small tooling; the public repository and bundled assets decisions; PT-BR game content.

## 4. Phases

Estimates are agent-working days with both quotas in use, and they are uncertain: ±50%.

### P0 — Reset (½ day)

- Stop the running proof work: formal S1 proof, M4.1/M4.2 chain proofs, Test B, late-S1 render windows, Combat fatal windows. Let anything already running finish and integrate it if it is green; start nothing new of that kind.
- Archive the fronts structure: no more per-front ownership for new Rust work. `motor/` is the one place where game logic lives.
- Measure the baseline: run the play bot (P1, first item) once and record minutes until the first stop and the top stops.

### P1 — Stop-free MONDE01 (≈ 4–7 days)

Exit: the bot plays MONDE01 for 30 minutes on 20 seeds with zero stops, and the user wins MONDE01 by hand in the app.

1. **Play bot and stop census.** A headless Rust driver (no app) that plays MONDE01 with seeded random but plausible input: select units, move, gather, build each available building, recruit, attack, scroll, press hotkeys, idle. On a stop it records the stop name and address, frame and the input history, then restarts from the last checkpoint with another seed. Output: a ranked table of stops by frequency. This drives all P1 work.
2. **Port the top stops, breadth first.** For each routine: read the Ghidra decompile (255 exports in `evidencias/ghidra/`, plus the local project with the 1,995 original SBL names) and the asm, write the Rust, and run a **routine differential** (section 5, tier 1). Reuse the existing Python only where it already exists and helps.
3. **Text and HUD.** Adopt Graphics 1.12's native `AffText` glyphs in the Rust renderer, so the renderer stops at frame ~2,013 no longer. Port the remaining HUD and selection displays hit by the bot (for example `AffInfoSelection 0x410be4`).
4. **Optional experiment, time-boxed to one agent-day: x86 fallback.** Embed Unicorn (the `unicorn-engine` crate) in the engine. On a stop in play mode, run the original routine over the same original-address memory, with the existing declared bindings, and continue. Adopt it only if MONDE01 runs 30 minutes at ≥ 60 fps with fallback enabled; otherwise drop it and keep porting. If adopted, the fallback also gives exact behaviour for rare routines while they wait for a port, and it is a free differential oracle.
5. **App:** opens straight into MONDE01 play (this reverses the 2026-10-30 deferral, because the goal is now play); keep the inspection UI behind a menu item.

### P2 — Missions load and chain in Rust (≈ 3–5 days)

Exit: every one of the 38 ETA files loads in Rust with the same gameplay state as the original, and winning MONDE01 continues into MONDE02.

1. **Port `MissionLoad 0x46c2cf` to Rust** from the validated Python composition (M1). Here the Python reference pays for itself.
2. **Port the startup state** the load depends on (`RISING.INI`, type tables, AI tables, `MONSTRE.INI`), so the engine no longer needs the captured S0.
3. **Automatic load check** on all 38 ETA files: native `MissionLoad` vs Rust, compared on gameplay buffers (units, structures, terrain layers, players, resources, objectives, AI and raid tables). One script, one table of results.
4. **Campaign chain:** `MissionNext 0x46c08c` with its stores (`Engin_StoreExperimente`, `RechercheStore`, `PlayerStore`, `IaRechercheAjuste`) and the stage/variant selection of `MakeMissionName`.

### P3 — Whole campaign stop-free (≈ 7–14 days, the largest unknown)

Exit: the bot reaches 30 stop-free minutes on every stage, and an automated or human run wins at least MONDE02, MONDE06, MONDE07, MONDE08, MONDE17A, MONDE23 and MONDE25 (the minimum set that covers every static feature, from the [campaign inventory](../pesquisas-paralelas/inventario-campanha/README.md)).

- Same loop as P1, stage by stage, in the inventory's order of new features. MONDE01 covers 21 of 88 static features; the other 67 are new units, buildings, spells, research and AI branches.
- Checkpoint comparison (tier 2) on MONDE23 and two other large stages.

### P4 — Game shell (≈ 3–5 days, can overlap P3)

Exit: the app can be used by someone who has never seen the project.

- Original main menu (`MenuInit 0x4682bb` family), briefing text and screens, victory/defeat result screens.
- Save and load: a modern format (serialise the Rust state), not `GameSave 0x46bd45`. Several slots, autosave at stage start.
- Music: the CD-DA tracks, extracted from the CD image and played by the app.
- Intro video if the original's `PlayVideo 0x47c82c` assets are practical to decode; otherwise skip.

### P5 — Modern tools and release (≈ 2–4 days)

- Speed selector 0.5x/1x/2x/4x and pause, on the existing virtual `TickClock` (one logic tick per original frame).
- Difficulty presets built from the original's own knobs, documented in [the difficulty scan](../pesquisas-paralelas/dificuldade/DIFFICULTY_SCAN.md): raid periods and group masks, the hidden `MONSTRE.INI` targeting weights, starting resources. "Normal" equals the original.
- Window scaling (integer and fit), fullscreen, optional smooth filter, rebindable hotkeys.
- Packaging: signed app bundle with assets, an About screen with provenance.

**Total: roughly 3–5 weeks** of both quotas, with P3 dominating the uncertainty.

## 5. Validation policy

Three cheap, automatic tiers replace whole-state proofs.

1. **Routine differential (every ported routine).** Run the original routine in the existing Unicorn harness (`ferramentas/emulador.py` and its declared bindings) and the Rust port on the same inputs: states taken from bot checkpoints plus generated variations. Compare return registers and the memory the routine writes. Hundreds of cases per routine, a few seconds each. This replaces capture-first per probe.
2. **Checkpoint comparison (per stage, a few runs).** Feed the same input stream to the original emulator and to Rust, compare gameplay state every ~500 frames, and bisect automatically to the first diverging frame only on mismatch. Long runs go to the Mac mini.
3. **Play checks (continuous).** The bot's stop-free minutes, outcome checks (stage loads, objectives reachable, victory and defeat trigger), ≥ 60 fps, and human play by the user at each phase exit.

`sh motor/validate.sh` stays the integration gate, trimmed to what runs in minutes. The existing whole-state proof suites remain in the repository and may be run on demand; they are not gates.

## 6. Working mode

- **One coordinator** (Claude) owns the plan, reviews and merges. It uses fresh subagents with short briefs, and Codex through `codex_task.py`, one executor per area of `motor/` at a time.
- **Few, larger tasks.** A task is "port these 10 routines from the stop census and make their differentials pass", not one routine per round.
- **One branch per task, merged when its gate is green.** `scripts/workstream.py` may still be used for the lock and the gate; no per-front ownership checks for `motor/`.
- **No rounds, no acceptance JSON, no status-only handovers.** One handover at the end of each session: what changed, the census table, next steps.
- **Machines:** the MacBook builds and runs the bot; the Mac mini runs long tier-2 comparisons and multi-seed bot runs.
- **Quotas:** spend on porting. Before a large dispatch, check `codex_task.py quota` and Claude's usage, as before.

## 7. Metrics reported at every merge

| Metric | How it is measured |
|---|---|
| Stop-free minutes (median over 20 seeds) per stage | Play bot |
| Distinct stops hit, and the top five | Play bot census |
| Stages that load in Rust (of 38 ETA files) | P2 load check |
| Stages won (bot or human) | Outcome checks |
| Play-mode fps | App measurement |

The old indicators (criteria accepted of 12, S1 chain reach) are frozen at their 2026-10-30 values.

## 8. Risks

- **The stop tail is long.** The 242 current stop sites are only those already met; the full game reaches more. The census makes the size visible after P1's first day; re-estimate then.
- **Reduced rigor lets a real divergence through.** Tier 2 and the user's play catch the visible ones; for a doubtful system, fall back to a capture-first proof of that system only.
- **The fallback experiment costs a day and may fail.** It is time-boxed and optional.
- **AI behaviour is the hardest to verify by play.** Prefer tier-1 differentials on AI kernels (`iagUnitNoyau`, `iagVilleNoyau`, `iagRessNoyau`, `iagWarNoyau`, `iaSolver`) over eyeballing.
