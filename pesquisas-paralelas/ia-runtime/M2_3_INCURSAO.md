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

## Raid task rules at counter 9000 (round 2)

**Capture:** [capturar_regras_incursao_ia.py](capturar_regras_incursao_ia.py) → [evidencias/captura-regras-incursao-9000-ia.json](evidencias/captura-regras-incursao-9000-ia.json), a native run of 38 s under the lease.
- **Input:** Missions' v1 bench, with the counter written to 9000 at frame 1's CalculGame entry (Combat's course input); three frames.
- **Recorded:** each rule call returning to iaSolver's `0x47d4ec`/`0x47d73c`, with its argument block, exit EAX, read-before-write footprint, every written byte and its outside calls.
- **Calls at 9000:** B_TestGroupeVide, B_NewConflit (→ iagWarSearchBattleFromPos, iagWarNewBattleToPos), I_DetermineTempsTrajet, B_Superieur, V_DeplaceGroupe (→ EnginEstVivant, SetDeplaceEngin) and B_AttenteConflit (→ iagWarSetWait → iaProbSleep).
- **Earlier attempt:** it added the memory hooks during the run, and Unicorn did not apply them to blocks translated earlier, so it missed reads. It is kept in `.local/`; the committed run installs the hooks before the frame and flushes the translation cache.
- **Order of work:** the translations were drafted from the code and the first attempt's call list, before this capture. The differential below ran only after the committed capture.

**Translation:** [regras_incursao_ia.py](regras_incursao_ia.py) has the five rules plus the war kernels, iaProbSleep and iagUnitGetNextUnitInGroup. B_Superieur is Core's (`MaquinaTarefas`).
- **Composition:** the rules run as `MaquinaTarefas` `operacoes`. V_DeplaceGroupe is reached through the VM's unit-operation hook (`MundoRegras`); the other unit operations are named stops.

**Differential:** `test_regras_incursao_ia`.
- **Result:** all six calls equal. Every rule's EAX and every written byte match, and the outside calls come in the native order with the native arguments.
- **Mutation check:** three mutations on exercised paths fail. The walking-unit skip is not reached at 9000.

**Core's raid providers** (`ferramentas/incursao_core.py`, `3a81e66`) are wired into the composition: CreerEngin, EnginSetPlayer, PlaceEngin, EnginGetCase, GetRandCaseChamps, GetRandCaseTypeBatPlayer, Chemin_Accessible and iaProbPost.
- **Cross-check:** a second raid differential runs six of them in place of the replayed native effects (CreerEngin keeps its effect, because it nests Economy's BonusGetValEngin). Every changed byte equals the native one.
- **GetFreeCell** stays a named stop in the composition. Core's translation reads native stack residue, the upper words of 16-bit locals at ESP−0x32/−0x1a/−0x3a/−0x2e, and the composition has no native stack.

**Still needed for frame 9000 in Python:**
- Core: GetFreeCell's residue contract, EnginEstVivant and SetDeplaceEngin.
- Economy: BonusGetValEngin inside CreerEngin, already in the composition through `prov.bonus`.

## Segmented M2.3 comparison

`comparar_quadros_ia.py --parte <part.json.xz> --sha256 <raw> --politica <policy>` compares one part of Missions' `pacotes_quadros_missao` format (`eb08940`). It was coded against the real writer.
- **Opening state:** its full state must match its summary, `compared_summary` and `masked_sha256` (`resumos_mascarados` uses Missions' definitions).
- **Replay:** every phase is checked on all three hashes, and every full state (8999, 9000, 9176 in the window part) is checked.
- **Python run:** Python starts from the opening state. Part 0 starts from the `-v2` MissionLoad state with load_tail; a later part starts as a checkpoint with the first phase's entry registers.
- **Per phase:** the compared-summary hash and the masked bytes are compared, plus RNGs, events, registers and the HUD flag.
- **Independence:** parts run independently, so they can run in parallel.
- **Self-test:** synthetic parts were cut from the M2.2 capture (load_tail–frame 64, and frames 65–128 with full states at 100 and 128). Run in parallel, both are equal: 129/129 and 128/128 phases.

**Requests to Missions:**
- `opening_state.allocations` in every part. Until then, a later part uses the `-v2` records, but only when it keeps the count and allocates or releases nothing.
- Optionally `named_inputs` in every part. A later part uses the `-v2` frame inputs, which are the same declared answers.

The writer's parts carry complete deltas, so the logic-only delta form in the brief is not needed.

**Against the real writer (`eb08940`):**
- **Writer check:** a synthetic two-part pack, cut from the M2.2 capture in the writer's exact format (`seconds` removed, `frames`/`last_phase`/`policy` fields), passes the writer's own `verificar()`. It was extracted read-only from `eb08940` and gave `equal`, 257/257 phases equal to the M2.2 capture, with the chain checked.
- **Comparator:** `--parte` finds both parts equal (129/129 and 128/128), run in parallel.
- **Policy:** the aggregated schema (`5a14cea`) keeps `cumulative.exclusion_mask`, `display_roots` and the per-byte `writers`/`readers`, so the comparator reads it unchanged.

**Manifest workflow** ([partes_quadros_ia.py](partes_quadros_ia.py)):
1. `verificar --manifesto … --plano …`
   - checks every part's compressed and raw hash and the policy pin;
   - checks the chain from hashes alone: `previous_part_raw_sha256`, each opening's summary, compared_summary and masked_sha256 against the previous part's last phase, and contiguous frames;
   - writes one independent `--parte` command per part.
2. The parts run in any order or in parallel.
3. `agregar --plano … --saida …`
   - requires every report to be equal, made from a clean tree, for the planned part, with the same policy and covering the whole part;
   - requires the final allocation records to be equal in the last part.

On the synthetic pack the result is `equal`, 257/257.

## Combat's readiness matrix: AI/runtime gaps (round 3)

Combat's matrix (`e3f0f8b`) reads main `99c0e4e`, which predates `ffa62fd`…`5b71905` on this branch.

| Gap | Status on `feat/re-ai-runtime` |
|---|---|
| Battle-task kernels: B_TestGroupeVide, B_AttenteConflit, B_NewConflit, I_DetermineTempsTrajet, V_DeplaceGroupe, the three iagWar* kernels, iagUnitGet{First,Next}UnitInGroup | translated, validated against the native 9000 capture (6/6 calls), wired as `MaquinaTarefas` `operacoes` |
| B_Superieur | Core's VM operation, checked against the captured call in `test_regras_incursao_ia` |
| Task poster (interface a) | StockeAction posts through Core's raid-validated `incursao_core.postar_tarefa`; iaSolver's own child tasks stay in Core's VM |
| iaSolver world operations (interface b) | the VM gets `operacoes=operacoes_regras(mm, p)`, `mundo=MundoRegras(mm, p)` (V_DeplaceGroupe; other unit operations are named stops) and `missao` from `0x496fe4` |
| **EnginNextEtape state 2 and the owner-4 prelude** | capture `6fe01d2`: the raid unit's 12 calls at counters 9000–9011. Translation `26ecd4a`: short of its target cell (`+0x7e` ≠ `+8`) it calls DeplaceEngin (Core) and exits; arrival stops at `0x4563e8`. `test_proxima_etapa_incursao_ia` finds all 12 equal: prelude (reload gate, GetBit gates, CalculFatigue, SetEnginCollision), the 9008 scan, and state 2 |
| CalculBatimentNextEtape at counter % 1000 | confirmed: the branch (`0x4281e5`) stores 0 to `0x4dfb9b` and does nothing else. Frame 0 runs it at counter 0, inside the proven M2.2 window |

**Still Core's:**
- DeplaceEngin and the movement routines;
- SetDeplaceEngin and EnginEstVivant (V_DeplaceGroupe);
- GetFreeCell's native stack-residue contract.

## Later raid rules and the unit's arrival (round 4)

These two captures ran on the MacBook under the new lease (3 work-hour slots; native runs up to 20 minutes). Both are original only, with the forced counter-9000 input, run sequentially in parallel.

| Capture | Content | Time |
|---|---|---|
| `evidencias/captura-regras-incursao-ia.json` | 19 rule calls at counters 9500, 9700, 10200, 11100 and 11101 | 208 s |
| `evidencias/captura-proxima-etapa-chegada-ia.json` | 9 EnginNextEtape calls of unit 16 at 10523–10531 | 164 s |

**Rule calls by counter:**

| Counter | Rule calls |
|---|---|
| 9500, 10200 | I_DonnePositionGroupe (→ EnginGetCase), V_DeplaceGroupe, B_AttenteConflit (re-post) |
| 9700 | I_Soustraction, B_Egalite (Core's VM), V_DeplaceGroupe, B_AttenteConflit |
| 11100 | I_Soustraction, B_Egalite, B_TestGroupeVide, V_FreeConflit (→ iagWarDeleteBattle), V_iaMonstreAttendLaReponse… (mode 1: the group is re-queued and its action entry removed) |
| 11101 | B_TestGroupeVide, B_NewConflit at ambush cell `0x320e`, V_DeplaceGroupe, B_AttenteConflit |

**New translations** in `regras_incursao_ia`:
- I_DonnePositionGroupe;
- V_FreeConflit and iagWarDeleteBattle;
- V_iaMonstreAttendLaReponse…, with mode 1 re-queuing, mode 0 subtracting the monster count, and the action-table compaction.

**Arrival** (`proxima_etapa_quadro`): at its target cell, with facing `+0x91` equal to `+0x90`, the unit calls EnginEnArret (Core). When that is nonzero and the state is neither 0 nor 4, the state becomes 7. Named stops:
- facing change (`0x455a6f`);
- EnginEnArret returning 0 (`0x456408`);
- the path-search unit (`0x4564c8`).

**Differentials:**
- **Rules:** `test_regras_incursao_ia` finds all 25 captured rule calls equal (9000 through 11101).
- **Raid unit:** `test_proxima_etapa_incursao_ia` finds all 21 calls equal: 9000–9011, moving 10523–10527, arrival at 10528, and state 7 at 10529–10531 through Economy's `estado_parado_unidade`, whose own Random draw matches the native one.
- **Mutation check:** three mutations of the new rules fail the test.

**Ambush re-post:** `evidencias/captura-avance-monstre-emboscada-ia.json` (AvanceMonstre at 11100 and 11101, 208 s). `test_incursao_ia.AmbushRepost` finds both equal.
- At 11101 the translation takes the ambush branch: the Random % 100 threshold, the cyclic ambush cursor walk, `Chemin_Accessible`, then `StockeAction(0x2e, 0x12, 0x320e)` with Core's `postar_tarefa`.
- It writes only bytes the original writes, and reproduces every changed byte.

## Readiness probe after Core's live movement (main `34ebf44`, round 5)

[sondar_incursao_ia.py](sondar_incursao_ia.py) is Python only, writes to `.local/`, and is not evidence. It starts from the `-v2` state after frame 1 with the counter forced to 8999, so the next frame runs at 9000. It runs the composition through the raid frames and reports the first stop.
- **Wiring:** with Core's exported providers in place (GetFreeCell, EnginEnArret, SetDeplaceEngin, DeplaceEngin, EnginEstVivant), the 128-frame probe and every owned test are unchanged.
- **First stop:** frame 9000, the first EnginEstVivant call from V_DeplaceGroupe. Core's `provedores_core` builds `mundo_vivo` over memory, and its `vincular_grades` needs byte views of the tile and region grids (`GradeU16`). The chain's map binds those grids as the Core world's u16 lists (Missions' `ligacao_provedores_m1.py:177`), so they have no byte view.
- **Owner:** Core (with Missions for the map binding). Sent to Core with two options: reuse the chain's own world, or bind the grids as bytes with `vincular_grades`, which means rerunning the M1/M2 proofs.

**After Core's `6e12550`** (`feat/re-core`, not yet on main): the probe ran in a throwaway worktree, my head plus that branch, not committed. Outputs are in `.local/m2-3-sonda-*-core-6e12550.json`.
- **Run length:** 1,880 Python frames, from counter 9000 to about 10879.
- **Comparison:** raid unit 16 against Combat's native course (`percurso-incursao-m2-3-original.json`), on head, cell `+8`, target `+0x7e`, `+0xb7` and `+0xb8`.
  - Counters 9000–9716: equal at every counter, including Core's first path search at 9177.
  - From 9717: Python is one 16-frame step ahead (32 differing counters up to 10878).
- **Where it starts:** entering 9700, the unit's bytes that SetDeplaceEngin writes equal the native ones. In that frame, Core's DeplaceEngin takes the first step and turn of the re-ordered unit, which was idle in state 7, one step earlier than the original. Sent to Core with the data.
- **Next stop:** at about 10880, Core's CalculFatigue fatigue-threshold branch `0x452d61`, which is not translated.
