# M2.3 preparation — the first monster raid, AI/runtime side

Branch `feat/re-ai-runtime`, main `8564ca7`. Intact `RISING.EXE` `6c556520…43fb`. Original first: the capture was committed before the translation.

## Native capture

[capturar_incursao_ia.py](capturar_incursao_ia.py) → [evidencias/captura-incursao-ia.json](evidencias/captura-incursao-ia.json): one 40 s run under the lease, original only.
- **Input:** the same forced input as Combat's `1e9f28e`. Missions' committed frame path (v1) is rerun with their read-only `Isolamento`. At frame 1, AvanceMonstre runs an extra case with u32 `0x508f7c` = 9000; every other byte is the exact frame-1 input.
- **Reproduction:** all phase states, the boundaries and the code reproduce.
- **Recorded inside the forced case:**
  - every **top-level call into another owner's routine** (14), with its arguments, exit registers and net bytes written;
  - every byte this front's routines write themselves (86 outside the stack, 27 of them changing).

  Isolamento also provides the whole call's read-before-write footprint (65,739 bytes) and its changed bytes.
- **Discarded run:** a first run without the own-write records is kept in `.local/`; it is not evidence.

## Translation ([incursao_ia.py](incursao_ia.py))

| Routine | Status |
|---|---|
| AvanceMonstre `0x47b283` | whole routine: first-call stamps, spawn branch `0x47b349` (cyclic group bit, re-stamp, ConstruitGroupeMonstre), ambush-action countdown, pending-attack branch `0x47b44c` (target player with the HumanOnly retry, Random % 100 against the cave/ambush thresholds, cave → ambush → field fallbacks, 20 tries each) |
| ConstruitGroupeMonstre `0x47a81d` | whole routine: guards (50 monsters, 16 pending), iaGroupNew(4, 0x10), per unit type: GetFreeCell, CreerEngin, EnginSetPlayer, PlaceEngin, Random parity → ProjectileInit 0x20/0x1f, iagUnitAddToGroup; pending-group push |
| StockeAction `0x47a99a` | new action (0x31 ambush timer, or iaProbPost and the action-table entry); the merge into an existing action stops at `0x47aa07` |
| iaGroupNew `0x483bd8`, iagUnitAddToGroup `0x482939`, iagUnitGetFirstUnitInGroup `0x4837f0` | whole routines |
| iagUnitSendMessage `0x4829c8` | message 0x49 dispatch only, **from the code, no native capture yet**. Owner type 2 → the group's behaviour handler `+8` → `iabDetection_AjouteEnnemiOuAlerteConflit 0x489b5a` for monster groups, a named stop. EnginNextEtape's scan hit now calls it with the target. |

**Other named stops:**
- the mission-0x17 pending post (`0x47b2d3`);
- an expired ambush action (`0x47b3d1`);
- an empty pending group, which calls iaGroupDelete (`0x47b4a3`).

**Differential** (`testes/test_incursao_ia.py`, no native run; the capture is the native side). My routines run on a memory holding only the bytes the original read before writing them, and any other read fails.
- Each of the 14 outside calls must come in the original order with the original arguments. It returns the original exit EAX and applies its native net writes.
- **Result:** equal. The calls, their order and arguments match; all 86 own-written bytes match, as do all non-stack bytes the call changed. Nothing else changed.
- Mutating the group cursor or the spawn effect type makes the test fail.

**Composition wiring:**
- iaProbPost runs on Core's `MaquinaTarefasViva.postar`, whose effect matches the captured one: free list, context list, active count and a 0x2f record with (group, cell, origin).
- ProjectileInit runs on Combat's `PoolProjeteis.iniciar`.
- Random and EnginGetType are Core's; PlayerGetType and MissionGetNum are as before.
- The strict 128-frame probe is unchanged: 128/128 frames equal Core's survey, with no stop.

## Checkpoint start

- `ComposicaoQuadros(..., inicio=k, alocacoes=…, regs_inicio=…)` starts from a full state after frame(k).
- `comparar_quadros_ia.py --a-partir-de K` takes that state from the capture. Either the capture's phases are replayed through frame K with integrity checks, or the capture begins at between_frames(K+1) and its `state_s0` holds a full state.
- **Declared inputs:**
  - the between_frames(K+1) entry registers;
  - the allocation records, from `checkpoint_allocations[frameK]`, from `allocations_at_start`, or from the final list when no later phase allocates or releases;
  - frame words (0, 0, 0).
- **Consistency check (Python only):** a chain started from the native `-v2` state after frame 1 runs frames 2–4 identically to the full chain. Exit registers and events are equal. The state differs only by the native display bytes in 79 blocks, which are present at the start and never touched.

## Provider requests (through the coordinator)

| Owner | Routines (contract in `incursao_ia.py`) |
|---|---|
| **Core** | GetFreeCell `0x479f20`, CreerEngin `0x457e6c`, EnginSetPlayer `0x443108`, PlaceEngin `0x456fa6`, EnginGetCase `0x44113e`, GetRandCaseChamps `0x489147`, GetRandCaseTypeBatPlayer `0x489300`, Chemin_Accessible `0x42d4f8`. The capture holds each call's native arguments, exit registers and net writes at the raid input. |
| Core/Combat | SetDeplaceEngin `0x4457d3` (ambush expiry, StockeAction merge) |
| Combat | SetAttaqueEngin `0x445a36` (EnginNextEtape scan hit in state 7; StockeAction 0x30 merge) |
| Mac mini (through you) | the first native `iagUnitSendMessage(0x49)` call in M2.3b, to validate the dispatch and to capture `iabDetection_AjouteEnnemiOuAlerteConflit` before I translate it |

Until Core's providers land, the composition at frame 9000 stops at GetFreeCell (`0x47a8ec`).
