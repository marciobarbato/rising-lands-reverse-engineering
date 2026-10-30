# Coordinator handover — 2026-10-30 07:00 (MacBook paused)

Read this first, then the top of `docs/PROGRESS.md` (round M3R2). [HANDOVER_CLAUDE_20261030](HANDOVER_CLAUDE_20261030.md) and [HANDOVER_CLAUDE_20261029](HANDOVER_CLAUDE_20261029.md) still describe the machines, leases and working mode, except where this file says otherwise. The coordinator's auto-memory holds the standing decisions.

The user paused development on the MacBook at 07:00 on 2026-10-30. The Mac mini keeps its long native runs.

## Milestones

| Milestone | State | Record |
|---|---|---|
| M1, M2 | accepted (`927c7e5`, `ea62eb4`) | `integracao/validacao/` |
| **M3.1, P1/P2 part** | **accepted at `c9c85eb`**: P1 1,002/1,002 and P2 1,202/1,202 phases whole-state, 0 crossings; reproduced on main on the MacBook and the Mac mini with identical chain hashes | `cxr-20261030-m3r1-m3-1-p1-p2-acceptance.json` |
| M3.1 rest | open: P6 strict proof (Graphics guards now on main), S1 order windows (pass-2 S1 still being captured) | — |
| M3.2–M3.5, M4 | open | — |

## What happened overnight (main `71335aa` at 06:00)

- **S1 wins MONDE01 on the original**, replay-equal over two independent runs from F0 (`82ec5ea`): AL = 1 at 16,933, MenuInit(0x13) at 17,032, MissionNext at 17,043, no MissionLoad.
- **D1 defeat on the original** (`bab6c7c`): the player unit count `0x4e1a3a` reaches 0 at 15,555, PartieGetResultat returns 0 at 15,655 and the failure branch runs. The trigger is pinned statically: only combat deaths lower the count. A replay check from F0 is running on the mini.
- **Rust engine:** stage 4 (orders, ABI 1.5) and the play-mode optimisation (ABI 1.6) are on main (`2eadf69`, `240ea87`). Logic now takes 0.26 ms/frame and logic plus render 0.65 ms (it was 13.4 ms). The coordinator reproduced the final hashes, M2.2 257/257 and P1/P2.
- **macOS app** (main `51715e2`): play mode without audits runs at 60 game frames/s with the display at ~120 fps. Orders work (ABI 1.5). Test A state-hash half: P1 501/501, P2 601/601, P3/P6/P7 91/91, K1 12/12, up to the engine's stops. ABI 1.6 adoption is in progress.
- **Core:** the frame-125 minimap divergence was explained: Economy omitted EDX=1. Also landed: hunger dependencies, `TerrainEstGc`, `SetMiniMap` mode 4, and all 16 S1 coverage gaps (1,956 native cases). The S1 coverage survey (495 routines, gaps per owner) is `docs/core/S1_COVERAGE.md`.
- **Economy:** exit position, hunger (state 19), sanctuary abandonment, `EnginRestaureEtat`, `BatimentEnleveMatiere`, the cave meal and tag 19, all with 0 mismatches. Transport states 18/20 are in progress; WIP is on `wip/re-economy-transporte`.
- **Combat:** turret `BatimentPeutAttaquer`, tag 14, the fatal fight path through death and recount, and the fatal-window runner for the mini (`--intervals`).
- **Graphics:** render 1.9 (K1 501/501, P4/P5 3,001/3,001), S1 end screens and the P6 guard fixes (`ad0a4a9`). Unvalidated WIP is preserved on `wip/re-graphics-codex-0430`.
- **AI/runtime:** hunger, restoration, turret and Core providers are wired. The P6 planning-mode diagnostic gives 4,544/4,544 phases. K1 and P5 are complete. The S1 proof driver is ready (`provar_entrada_janelas_ia.py fixar/tudo/reproduzir`).

## In flight at the pause

**Mac mini** (Claude session "Mini-task M3 harness", SSH `marciobarbato@192.168.68.63`):
- Pass-2 S1 policy segments. The MacBook ran 9,750–12,500; all others are the mini's. ETA about midday. Then `relatorio`/`empacotar` and a push to feat/re-missions.
- D1 replay check from F0, two runs, ETA about 07:40, then packaging `sondas/D1`.
- Then Combat's fatal windows:
  - `executar_janelas_fatais_combate.py S1 --intervals 11000-12250`
  - `... D1 --intervals 11250-11750 15250-15700`
  - push to `runs/combat/fatal-{s1,d1}`.

**Codex** sessions still running at 06:15. They are stopped at the pause, and their unpushed work stays in their worktrees:
- `rust-engine-chain`: port of the chain past frame 220 to Rust (Rising-Lands-Codex-Engine).
- `economy-transport`: states 18/20 capture and translation (re-economy).
- `macos-abi16`: ABI 1.6 play mode and the original's game speed (macos-playable).
- `graphics-retry`: WIP recovery, glyphs, view origins (re-graphics).
- `ai-runtime-s1-proof`: strict P6 proof with Core/Graphics on main (re-ai-runtime).

Codex quota: 65% of the weekly window at 03:45; it resets 2026-11-04 05:10. Many runs failed overnight with "Selected model is at capacity"; resuming the same session later usually worked. Very long threads also failed during compaction. Start a fresh session with a handover brief instead.

## Next steps (in order)

1. Check each Codex worktree for unpushed work. Integrate what passes, and park the rest on `wip/*` branches.
2. When pass-2 S1 lands:
   - AI/runtime runs `fixar S1` and `tudo --janelas S1` (strict and planning);
   - reproduce on both machines;
   - M3.1 S1 windows.
3. Strict P6 proof on main, then reproduce it and record M3.1 (P6 part).
4. D1 packaged, then M4.2 groundwork. Use Combat's fatal windows for the death chain.
5. Rust engine past 220, then the app's Test A beyond 220, then Test B (recorded human session replayed on the original, Mac mini).

## Rules learned tonight

- **No foreign byte pins in tests.** A test that pins the exact bytes of another front's file deadlocks integrations. It happened Core↔Economy twice, and once in the engine's player pins. Accept any foreign version that has a committed native run, and bind only the front's own files.
- **Clean tree for `integrate`.** `workstream.py integrate` merges main into the feature worktree, so it needs a clean tree. Don't integrate while a Codex session is editing that worktree. Park leftover WIP on a `wip/*` branch first.
- **Mini over plain SSH.** `git fetch` over SSH hangs; fetch the public repo by HTTPS. Symlink `.local/python` into new worktrees.
- **Cross-machine pass-2 segments work.** Rsync the snapshots and pass-1 set to the MacBook, run `passo2_sondas.py politica --de --ate`, and rsync each pickle back (no `--delete`).
