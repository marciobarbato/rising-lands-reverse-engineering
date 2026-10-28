# M1 oracle architecture review — 28 October 2026

Coordinator review of the Missions Stage12 whole-`MissionLoad 0x46c2cf` original oracle, written at main `3d782ca76ee29a782eea5de9c763278c7674db65`. It covers the uncommitted Missions WIP in `worktrees/re-missions`: `oraculo_carga_missao.py`, `fronteiras_carga_missao.py` and `capturar_carga_missao_original.py`, source SHA-256 `708d2477…`, `056f66cc…` and `82f32ee4…`. It also covers the two local calibration captures `.local/stage12-calibration-1.json` (allocation fill 0xA7) and `.local/stage12-calibration-fill5a.json` (fill 0x5A). Those captures are calibrations, not committed evidence. Intact executable SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

**Follow-up.** Missions implemented the four checks below in `14b56a9`/`81815eb`/`3990b7c`, and all four passed. Capture v2 `eb7d2303…` and entry snapshot `0692dea1…` are integrated at main `14c01228218b51d2e7d42a3c35cbd4119efa6b5b`, and the coordinator reproduced them byte-identically there. See the [round evidence](../integracao/validacao/cxr-20261028-07-claude-round.json).

**Verdict.** Keep the current design and do not rewrite it. The original oracle already reaches the real return. M1 now depends on four things: freezing that capture with four added checks, composing the Python whole load from the frozen *entry* snapshot, comparing every byte at return, and running the standard gates.

## Design under review

The bench executes the intact program in two phases.

1. **Startup phase.** It executes the original new-campaign path: the CRT thread-data and file-handle initializers, then `AppInit`/`ProgInit`, then the `CalculGame` frames that drive the main menu, campaign menu and research screen through declared `GetAsyncKeyState` answers. It ends at the real `CALL MissionLoad` at `0x42d228`. Display, CD-audio, text-resource and bitmap-bank routines are not executed. The bench stops at their entry, applies a declared EAX and the routine's own callee stack cleanup, and returns to the caller.
2. **Oracle phase.** It runs from the `MissionLoad` entry to the real return `0x42d22d`. Any skip boundary, undeclared import, fault or budget exhaustion stops the run with the state retained. The only answers come from the declared external boundaries: the CRT `fopen`/`fread`/`fclose` and the inventoried `FileSeek` wrapper, `GlobalAlloc`/`Lock`/`Handle`/`Unlock`/`Free`, and the two private-profile reads. Their inputs are the read-only original media.

Instrumentation replaces Core's per-instruction Python address check with two native mechanisms. Code hooks are scoped to individual stop addresses, and data, stack and arena pages are non-executable. Long runs are cut into `count`-limited segments and resumed at the same EIP with the CPU context intact.

## Proven behavior

| Claim | Evidence |
|---|---|
| Original `MissionLoad` returns for MONDE01 | Both calibrations reach `0x42d22d` with AL=1. The oracle phase used 1,425 segments, about 2.5 s, 0 skips and 0 watched reads. There were 1,400 binding events: 1 fopen/fclose, 1,019 fread, 17 FileSeek, 57 each of GlobalAlloc/Lock/Unlock/Free, 114 GlobalHandle and 20 profile reads. |
| Uninitialized allocation memory does not influence the load | Between fills 0xA7 and 0x5A, the entry DGROUP and final DGROUP (585,728 bytes) are byte-identical. Every one of the 552,340 differing final bytes is untouched fill (entry byte = fill, final byte = entry byte). No computed byte differs. |
| Skips respect the calling conventions | There were 47 startup skips across 16 routines, none in the oracle phase. Declared callee cleanup equals each routine's exit: plain `RET`, `ret 0x10` (AffText), or a shared epilogue. `0x43f316` pops EDI/ESI/EDX/ECX/EBX then does a plain `RET`, matching the DDLockSurface/DDSetPalette prologues. `0x45cac7` pops EBP/EDI/ESI then does `ret 8`, matching FilledBox/Box. No caller reads a skipped routine's EAX: the instruction after every return either overwrites EAX or calls again. |
| Shared epilogues inside the load run natively | MissionLoad ends `add esp,0x12c; jmp 0x46bc30`, and Engin_RetrieveExperimente exits through `0x440d59`. Both execute as original code, not as skips, so no cleanup is synthesized there. |
| Startup-derived inherited controls | At MissionLoad entry the live player types are `[1,2,2,2]`, the same controls used by the AI adapter's two complete MONDE01 fixtures. The saved experience queue is `ff00`×20, which matches Core's static provenance (MenuInit→Engin_ResetExperience). After the return the current queue is `ff00`×20, which matches the integrated `recuperar_experiencia_missao`. |

## Assumptions and architectural risks

1. **Count-based segmentation is assumed transparent, not yet proven.** Unicorn keeps the CPU context between `emu_start` calls, and the fill-invariance result is consistent with that. A direct test is still cheap: rerun the oracle phase from the same entry state with a different per-segment instruction count and require identical image, event log and AL.
2. **The code section is writable in this bench.** `BancadaX86` maps `0x400000..0x600000` with `UC_PROT_ALL`. The oracle only re-protects data as RW. A stray native store into `0x401000..0x493c00` would self-modify silently. `0x523000..0x600000` is mapped RW although it lies outside the PE image. Protect code as R+X, make the tail inaccessible, and hash the code section after the run.
3. **The static watched-write set is incomplete.** It only covers absolute stores made by non-executed routines. It does not cover values that *executed* code stores after a skip returns, for example `ProgInit` storing the declared DDLockSurface result 0 at `0x508f70`. The general fix is dynamic: record every inherited byte MissionLoad reads before writing it, then classify each range by provenance.
4. **Startup provenance and M1 equality are separate claims.** M1 compares Python and original over the *same* inherited input. Imperfections in the startup phase change how representative that input is, not whether the comparison is valid. The entry snapshot must therefore be a frozen first-class artifact. The startup emulation provides that snapshot's provenance; Python does not reproduce it.
5. **Python world objects own their buffers.** `MundoUnidades.__init__` creates its own bytearrays, and the AI adapter rejects whole-DGROUP shadows that overlap the actual pools. The composition needs one memory-map assembler. It loads entry-snapshot bytes into the providers' live buffers *in place*, splits DGROUP into non-overlapping segments around those pools, and serializes back to DGROUP plus allocations for comparison. This is the largest remaining piece of engineering.
6. **Allocation pointer values are part of the state.** Native remap allocations come from a page-aligned bump arena (handle = pointer, GMEM_FIXED). The Python `alocar` callback must hand out the same addresses from the same next-free position recorded in the entry snapshot. Otherwise stored pointers differ for representational reasons only.
7. **Declared Windows inputs are legitimate state.** These are the clock seed consumed by `iaRandom(0)`, the install directory, the CD label and the key script. They are recorded inputs, not defaults. The final state legitimately depends on the clock through the RNG, and both sides consume the same entry snapshot.

## Simpler alternatives considered

- **Constructing inherited state in Python or from fixture constructors.** Rejected. It reintroduces the synthetic defaults the methodology forbids, and the original startup already provides byte provenance.
- **Calling individual original initializers directly instead of driving the menus.** Not simpler. It requires asserting the order and completeness of initialization, which the menu path gives for free, and the startup phase already runs in about 30 s.
- **Dumping memory from a real Windows/Wine process.** This would be an independent cross-check, but it needs new tooling and debugger fidelity. It is not needed for M1 now that the emulated original returns. It remains optional later evidence.

## Remaining operations genuinely required for M1

1. **Freeze the original capture.** Missions, original-only, before translation, with four added checks:
   - Code-section protection and post-run integrity hash.
   - Segmentation invariance.
   - The read-before-write input footprint with per-range provenance classes.
   - The entry snapshot as an artifact: all blocks, registers, arena policy and next-free pointer.
2. **Compose `carregar_missao` from the entry snapshot.** Missions, consuming integrated providers, with the memory-map assembler, the deterministic arena and the original call order from `0x46c2cf`:
   - MakeMissionName and the filename build
   - the `0x4e1a38`/`0x4e1a3a` stores
   - the reset prefix: `0x45e88f`, TerrainReset, MiniMapReset, BatimentResetAll, EnginResetAll, ProjectileReset, `0x469908`, BallonInit
   - FileOpen and the header prelude
   - Chemin_Remap
   - the structure copy
   - LoadEngin
   - the eight auxiliary loaders
   - FileClose
   - MissionPlaceTerrain
   - the six tails: EnginInitTechnologie, BatimentInitCave, Engin_RetrieveExperimente, PlayerRetrieve, IaReset through the integrated adapter, MarcheResetAll
   - AL=1

   Any provider that is still missing must raise its named dependency at the original CALL.
3. **Compare the whole state at return.** The comparison covers the full DGROUP and every allocation (active and freed, with its records), the ordered binding log and the return value. The only exclusion is untouched allocation fill, and it is handled by consuming identical entry bytes, not by masking.
4. **Gate and integrate.** Run the Missions native suite, common gates, locked integration and committed-main reproduction.

The AI providers `EnginGetEtat 0x440e11` and `EnginSetPlayer 0x443108` are *not* expected on this path. The actual controls are `[1,2,2,2]`, which is inside the adapter's complete domain. Step 2 proves or refutes this. If the IaReset adapter raises `DependenciaIA`, that stop becomes the next real blocker. Graphics, audio, combat building-damage and runtime dispatchers are not M1 requirements.
