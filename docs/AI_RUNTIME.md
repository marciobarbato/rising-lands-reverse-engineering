# AI and runtime contract

Owner: the AI and Runtime front (`feat/re-ai-runtime`, `worktrees/re-ai-runtime`). Owned paths are `pesquisas-paralelas/ia-runtime/` and this manual. The front composes the committed Core VM/task primitives and the other owners' simulation APIs into the original frame, unit and structure dispatchers and the AI player kernels. It does not copy, fork or silently alter a sibling implementation; a needed change in a core primitive is requested as a contract in the handoffs.

Every address applies to the intact executable SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`, the only execution oracle. The normalized analysis PE `26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0` is a different identity and was not read for any interval below. Routine names are the original SBL names decoded by core's `simbolos_ia`.

**Current scope:** Stage 1 established the original-byte contract and Stage 2 the AI table providers (`IaReset`, `IaAlloc`, `IAResetAttaque`). M2 composed the whole frame (CalculGame, both dispatchers, the AI kernels reached by MONDE01) and proved it whole-state against the original through the first raid (M2.2, M2.3). M3.1 adds the input path (InputGame → SetPlayerOrdre → ProcessInputGame → setters) and the per-window input chain; its P1/P2 part is accepted. The current state, API and open stops are summarized in the next section; the later sections are the historical record, stage by stage.

## Current state (2026-10-30, resumed front)

**Milestones.** M2.2 (257/257 phases) and M2.3 (18,401/18,401 phases, frames 0–9,200 through the first raid) are accepted. **M3.1 P1/P2 is accepted at main `c9c85eb`**: P1 1,002/1,002 and P2 1,202/1,202 phases whole-state, zero crossings, reproduced on the MacBook and the Mac mini with identical chain hashes ([M3_1_PROVA_P1_P2.md](../pesquisas-paralelas/ia-runtime/M3_1_PROVA_P1_P2.md), `validacao/m3-1-prova-p1-p2.json`). The strict P6 proof is now recorded (4,544/4,544 phases, zero crossings, clean source `01c4319`); second-machine reproduction and coordinator acceptance remain pending. S1 windows are open.

**Resumed delivery.** Main `9ae3e4d` supplies Economy `dfb87bd` recruitment register forwarding. Fresh strict/planning S1 indicators pass recruitment and match through frame 3276, stopping in 3277 on the missing MineGetCapacite route. That AI/runtime binding now delegates to Economy's live query: 101 native comparisons, zero mismatches. The next chain rerun is pending; follow [S1_NEXT_STOPS.md](../pesquisas-paralelas/ia-runtime/S1_NEXT_STOPS.md). The earlier [recruit continuation](../pesquisas-paralelas/ia-runtime/S1_RECRUIT_CONTINUATION.md) retains its historical scope. Feature pushes only; main integration and acceptance remain coordinator-owned.

**API (input chain).**
- `provedores_entrada_ia.DonosM3(m, *, som, bonus=None, mensagem_unidade=None)`: one instance of each owner provider over one live memory (Core `entrada_estruturas`, `visao_grupos`, `recrutamento_core.provedor_recrutamento`, `buscas_bloqueios.provedor_buscas`, `consultas_estado_core.provedor_consultas_estado`, `provedores_lacunas_core.provedor_lacunas_s1`; Economy `caverna_recrutamento`, `ciclo_trabalho`, `alimentacao.estado_fome`, the restoration provider; Combat's turret providers and `refugio_registradores`). `externo(nome, chamada, regs)` routes every named dependency to its owner with the full register file; `rotina_core(nome)`, `.fome`, `.fadiga`, `.ordens()`, `registros(nome)`. Core's `_incertos` registers are carried, never invented; strict calls refuse an absent or nominal ESP.
- `provedores_entrada_ia.provedores_vivos(m, *, janelas, som, ..., donos=)` and `construcao_viva(...)` bind the live providers for the validators and the window proofs; `construcao_entrada_ia.instalar_donos(m, p, donos, tabelas)` installs the cave body, BatimentIllumine/Decouvre, unit states 5/13/19 and EnginSetFatigue.
- `mensagem_cidade_ia.mensagem_cidade(memory, regs, chamada)` binds iagVilleSendMessage's owner gate, exact register effects and named AI-dispatch stop in `DonosM3`.
- `composicao_entrada_ia.ComposicaoEntrada` runs a window's scripted inputs over the M2 frame composition; `mensagem_unidade` is iagUnitSendMessage.
- `provar_entrada_janelas_ia.py janela | agregar | tudo [--partes] [--diagnostico-planejamento] --lease <heavy_lease.py> | fixar <W> --ref <missions ref> | reproduzir`. Planning mode lets Graphics planning stops through; its output stays under `.local/` and is never acceptance evidence.

**Validated coverage (native, 0 mismatches).**

| Check | Cases / phases | Equal | Named stops | Mismatches |
|---|---:|---:|---:|---:|
| Input orders (`validar_entrada_ordens_ia.py`) | 124 | 118 | 6 | 0 |
| Deposit pages (`validar_paginas_deposito_ia.py`) | 203 | 203 | 0 | 0 |
| Construction/keys (`validar_construcao_teclas_ia.py`) | 90 | 85 | 5 | 0 |
| Recruit binding prefix | 6 | 6 equal prefixes | 3 missing-DX boundaries | 0 |
| City message | 27 | 23 returns | 4 AI-prefix stops | 0 |
| M3.1 P1 / P2 whole state | 1,002 / 1,202 phases | all | 0 | 0 |

All three leaf differentials were freshly rerun with the recruitment/city binding in `bf8ec61`: 417 cases, 406 complete comparisons, 11 explicit dependency stops, zero mismatches. All native load-tail, between-frames, frame-1, pause and unchanged-code reproductions pass; reports retain the current source/provider provenance. No foreign source bytes are pinned by new tests. Remaining leaf stops: six unloaded-text cases (`0x478a47`), `BatimentHabitable` (`0x41d000`), `SetMurAllentour` (`0x41d012`), `SetEnginSelectRentreEngin` (`0x45f17a`), `iagUnitSendMessage` (`0x41da48`) and VK_SUBTRACT/MiniMapRecentre (`0x41843e`).

**Window reach (indicators unless stated).** Fresh S1 strict/planning runs at `bf8ec61` are equal 129–2546, stop at SetSortEngin in frame 2547, and have no earlier difference (planning records zero Graphics bypasses). The following older observations retain their original source/scope: P6 planning whole-state 4,544/4,544 phases through frame 2400 (diagnostic). K1 strict complete through 629, P5 strict complete through 3129, P3 planning 3,001/3,001 through 3129. Uncommitted local runs at `d2777b1` (logs under `.local/`, not evidence) show P3 and P4 strict complete through 3129; P7 strict through 3216 and S1 strict (pass-1 indicators) through 2057, both stopping on Graphics' AffGame view origin at `0x415b77`; S1 planning through 2546 with a first difference at 2547 in `objective.structures`; strict P6 parts 1 and 2 equal (2,000 and 544 phases, chains `5da71fab…` and `c557167f…`) while part 0 was cut off at the pause.

**Open stops and owners.**
- P6 reproduction (Mac mini/coordinator): strict proof [m3-1-prova-p6.json](../pesquisas-paralelas/ia-runtime/validacao/m3-1-prova-p6.json) is equal in all three parts (2,000 + 2,000 + 544 phases, frames 129–2400), with zero crossings and matching checkpoints; reproduce its three part chains on the mini before acceptance.
- S1 windows (Missions → AI/runtime): wait for the pass-2 S1 capture from the Mac mini, then `fixar S1 --ref origin/feat/re-missions`, commit the pin, and run `tudo --janelas S1` in strict and planning modes.
- Graphics: AffGame vegetation/terrain handlers proved only on sampled view origins (`0x415b77`); `feat/re-graphics` carries the finite-origin validation not yet on main.
- S1 frame 2547: [recruit continuation](../pesquisas-paralelas/ia-runtime/S1_RECRUIT_CONTINUATION.md). Both strict and planning modes have 2,418 indicator frames equal, 129–2546, with no earlier difference. Core's conversion/healing/fatigue/experience callbacks run; Economy's SetSortEngin CALL `0x420f8c` omits DX and stops before placement. Required AX/DX are unit/exit cell; native S1 observes 4 / `0x0e0f`. Add EDX's mask and forward the actual preserved cell in Economy. The live city callback is independently proved: 23 exact native returns and four named AI-prefix stops, zero mismatches. Six production prefixes agree through the missing-DX boundary. This is not completed recruitment or pass-2 S1 equality.
- Core/Economy/Combat leaf stops listed above.

**Next dependencies.** Rerun S1 with the MineGetCapacite binding; the previous missing-DX stop is resolved by main. Coordinator review/integration and S1 whole-state validation remain separate. AI-owner city message bodies retain a named AI/runtime stop at `0x48484c`. No later task was started in this delivery.

## Evidence

| File (under `pesquisas-paralelas/ia-runtime/evidencias/`) | Contents |
|---|---|
| `manifesto.json` | 171 intact intervals with SHA-256: 35 routines with the shared Watcom tails they reach, plus the 136 rule-VM operation bodies. Also 9 jump/handler tables (data) with their values, the SBL hash and the hashes of the core inputs consumed |
| `*.asm` (35 files) | Disassembly of each routine interval and its shared tails. Each line carries the original bytes; bytes no static path reaches are listed as `.byte` rows |
| `inventario.json` | Static reachability over the intact bytes: the CalculGame state table and frame path, the unit state table, the structure type table, iaCalculPlayer callbacks, message tables and call sites with their codes, AI-table global operands, the 140 operations with callees/globals/provider families, and direct callers of the key routines |
| `capturas-originais.json` | 57 original-only captures on core's `BancadaX86`: call order, declared stops, registers at each call and store traces |

Regenerate with `python3 -B pesquisas-paralelas/ia-runtime/extrair_contrato_ia.py` (static, no emulation) and `python3 -B pesquisas-paralelas/ia-runtime/capturar_contrato_ia.py` (Unicorn).

The capture method (`captura_chamadas_ia.py`) works as follows:
- The intact routine executes; every declared callee entry is a stop.
- At a stop, the capture records the callee with EAX/EDX/EBX/ECX and the call site. It then applies the fixture's declared return and pops the callee's stack arguments exactly as the callee's own `ret N` would (read from its bytes), and resumes at the original return address.
- Stubbed callees are never executed, so a capture claims only the caller's own order, branches and stores.
- Win32 imports are bound by pointing their IAT slots at declared thunks, which is the loader's job. No Windows API is emulated.
- Every scenario lists its synthetic fixture (memory before entry, declared returns, declared callee side effects).

These captures fix call order and gates. They are not whole-state oracles.

## Agreed ownership

| Area | Core keeps (`ferramentas/`) | AI/runtime implements (`pesquisas-paralelas/ia-runtime/`) | Others |
|---|---|---|---|
| Frame loop | `cadencia` counters, draw predicate, RNG step | `ProgIteration 0x47500e` order; the in-game paths of `CalculGame 0x42c868` (load entry for states 0/15, frame state 0x12, the network gate for state 0x10, gates 1–3, end-condition tail); `GameNextFrame 0x45d015` | Missions: `EvenementEnCours`, `TestFinDeMission`, the `MissionLoad`/`MissionLoadName` composition. Economy: `RechercheCalcul`, `PlayerInitAllianceCompteur`, `PlayerAttaqueCalculSympa`, `SetUpdateChamp`, `UpdateChamp`, `CalculMatiere`, `CalculCompteurMarche`, `CalculCompteurProposition`. Graphics: `NextAnim*`. Combat: `ProjectileCalcul`. Menu states and input are second wave |
| Unit dispatcher | Bodies of states 2, 3, 4, 13, 16 and 17. Prelude primitives `SetDeplaceEngin 0x4457d3`, `SetDyingEngin 0x444938`, `Set/ResetEnginCollision`, `RetireEngin 0x457058`, `CalculFatigue 0x452cc8`/`EnginSetFatigue`, plus `DecouvreTerrain`/`IllumineTerrain`/`SetMiniMap` | The `CalculEnginNextEtape 0x456db5` loop and counters; `EnginNextEtape 0x45442c` prelude order (32-frame target scan, spell timer, fatigue branch) and the state switch at `0x4543c8`; inline state 6; `IATestUtilite 0x47fbfd` | Combat: the whole state-1/24 branch body `0x456886`..exit (target-mode switch, validity checks, `CalculAttaqueEngin 0x451914`), `EnginTrouveCible`, `SetAttaqueEngin`, state 22 `CalculPiege`. Economy: states 5, 7, 11, 15, 18, 19, 20, 21, 23, plus the prelude's bonus query `BonusGetValEngin` and `CreerSac` inside state 4 |
| Structure dispatcher | Body of the type-12 gate branch; `BatimentDecouvre`/`BatimentIllumine` | The `CalculBatimentNextEtape 0x4281c7` loop and counters; the `BatimentNextEtape 0x4268d4` type switch at `0x426880` | Core: `DemonteBatiment 0x41effd` (structure state 3), with the refund arithmetic as an economy query. Economy: types 1–8 and 13–20 (`CalculTroupe 0x4259e6` and the other production bodies). Combat: turret types 10/11 |
| AI players | `ia.atualizar_ia` (iaCalculPlayer order, verified below), the `chamar` protocol, `EstadoIA` | The callbacks `iagUnitNoyau 0x482936`, `iagVilleNoyau 0x48453c`, `iagRessNoyau 0x485183`, `iagWarNoyau 0x4866d7`, `AvanceMonstre 0x47b283`, `iagUnitDeleteAllGroups 0x483d95` | Missions: mission number and attack-table inputs |
| Rule VM | `tarefas_ia.MaquinaTarefas` (task memory, lists, waiting, control flow, arithmetic), `simbolos_ia`, `ordens_unidades.OPERACOES`, `mensagens_chegada` | The world operations, registered through `MaquinaTarefas(operacoes=...)` and grouped below | Each operation calls its providers' committed queries and raises a named dependency where none exists |
| Messages | Arrival/state-change profiles | `iagUnitSendMessage 0x4829c8`, `iagVilleSendMessage 0x484808`, the 12-entry behavior table `0x498e94` and the `iab*` handlers, `iagMessTestSendMessageEngin 0x483ed7` | Callers in other owners' bodies raise named dependencies until these are committed |
| AI tables | — | `IaAlloc 0x47fb15` (program start), `IaReset 0x47f36e`, `listInit 0x47cfd0`, `iaProbInit`/`iaProbReset`, `iagUnit/Ville/Ress/WarInit` and `Reset`, `iafRessourceReset`, `InitMissionMonstre 0x47af90` | Missions calls `IaReset` at `0x46c5cc`. Economy/missions supply the player table `[0x5080a8]` and the Recherche queries |

Agreement record:

| Front | Status |
|---|---|
| Core | Confirmed 2026-10-28, with two clarifications. Sound, the bonus query, targeting and `CreerSac` stay with their owners and raise named dependencies inside core bodies. The 32-frame scan, spell timer and fatigue branches are sequenced by ai-runtime. Core also accepted unit state 13 and `DemonteBatiment`. Core will record the table in `docs/core/HANDOFF.md` in its Stage 14 commit |
| Economy | Confirmed 2026-10-28 for every economy branch listed above, with the call shape eax = zero-extended u16 index and return ignored. Recorded in economy's Stage 15 commit |
| Missions | Confirmed 2026-10-28. Missions keeps the `MissionLoad`/`MissionLoadName` composition and calls `reiniciar_ia` (IaReset) at `0x46c5cc`/`0x46c98e` without the unused AL. It keeps the event bodies, `TestFinDeMission`, `MissionGetNum` and the attack/monster tables. The oracle inherits IaAlloc's program-start state as declared input, and the M1 snapshot is taken at `0x42d22d`. Recorded in `pesquisas-paralelas/missoes/HANDOFF.md` (Stage 9, main `bb8c6d0`) |
| Combat | Confirmed 2026-10-28. Combat owns the whole state-1/24 branch body (one entry with the u16 unit index), `EnginTrouveCible`, `SetAttaqueEngin`, `ProjectileCalcul`, and in principle turret types 10/11 and state 22. Recorded in combat's Stage 18 commit |

## Frame loop

### `ProgIteration 0x47500e..0x47509d`

Called by `_WinMain@16+0x9d` (`0x46020d`). Order (capture `prog_iteration`):
1. u32 `0x508f7c` += 1; when the new value is even, u32 `0x508f80` += 1; when it is a multiple of 3, u32 `0x508f84` += 1. This is the same arithmetic as `cadencia.avancar_contadores`.
2. `GetCursorPos(&point)` stores u16 `0x5099a8` = x and u16 `0x5099aa` = y.
3. `CalculGame`, then `AffGame 0x417698`.
4. If byte `0x5099af` ≠ 0, clear `0x5099af` and `0x5099ae`. If byte `0x5099b2` ≠ 0, clear `0x5099b1` and `0x5099b2`.

### `CalculGame 0x42c868..0x42d4f8` (shared epilogue `0x42c314`)

On entry it copies the state byte `0x4e2f78` into `[esp+0x104]`, sets u16 `0x49a010` = 0x1dd8 and calls `SetCursorPos(u16 0x5099a8, u16 0x5099aa)`. A state above 0x18 exits at `0x42d4e2`. Otherwise it jumps through the 25-entry table `0x42c804`:

| States | Target | Meaning in this contract |
|---|---|---|
| 0, 15 | `0x42d1da` | Load entry. It falls through into the frame body in the same call |
| 18 (0x12) | `0x42d2de` | In-game frame |
| 2–5, 12–14, 16 | `0x42cfe3` | Menu path. It ends at gate 1 (`0x42d14c`) |
| 8, 9, 11 | `0x42d4e2` | Exit |
| 1, 6, 7, 10, 17, 19, 20, 22, 23, 24 | `0x42c8bf`, `0x42cda4`, `0x42cd7d`, `0x42c979`, `0x42caa9`, `0x42c9c5`, `0x42cd5f`, `0x42d197`, `0x42cbfd`, `0x42c947` | Menus, video, briefing, end screens (second wave) |
| 21 | `0x42d4d9` | `PostQuitMessage(0)` |

**Load entry `0x42d1da`** (capture `load_state0_then_first_frame`), in order:
1. `MouseInit`; bytes `0x496d2c` = `0x497285` = 1, `0x496fd8` = 0, `0x5099ae` = `0x5099af` = 0.
2. `InitCache`, `InitGouttes`; u32 `0x4e061c` = 0.
3. State 0: `MissionLoad(eax=0)` when the network flag `0x4e0730` is 0, otherwise `MissionLoadName(0x4e3acc)`. State 15: `ShowCursor(1)`, then `OpenNewFile`. On failure: `RestoreAll`, `MenuInit(local, 2)`, `ShowCursor(0)`, exit `0x42d4ea`. On success: `ShowCursor(0)`.
4. `RestoreAll`; `SetClipping(0, 0, (u16 0x508724 << 5) − 1, (u16 0x508726 << 5) − 1)`.
5. u32 `0x508f7c`/`0x508f80`/`0x508f84` = 0.
6. `MenuInit(al=local player 0x508041, edx=0x12, ecx=1)`, `InitGameZone(1, 0)`.
7. Fall through to `0x42d2de`.

The capture declares `MenuInit`'s store of DL into `0x4e2f78` (original store `0x468c6d`); with it, the first frame runs in the same call. **The M1 snapshot point is therefore `MissionLoad`'s return to `0x42d22d`, and the first M2 frame is the remainder of that `CalculGame` call.**

**Frame `0x42d2de`** (capture `frame_single_player`):

1. `PlayerAttaqueReset 0x46d628`, a one-byte `ret`.
2. **Gate 2 `0x42d2e3`:** `EvenementEnCours 0x4581b6`. A nonzero AL exits at `0x42d4ea`, which skips the clear of `0x5099b0` (capture `gate2_event_in_progress`).
3. If byte `0x4e2f28` = 0: `MCICD_Play(2 + table[0x4e1c18 + idx] % 2, 0)` with u8 `idx` = `0x4e1d18`, then `idx` += 1.
4. Player loop for `cl` = 0..4 (0..3 in network games). It calls `PlayerGetType(cl)`:
   - Type 1: when `cl` is the local player 0x508041, `InputGame(cl)` and `InputSend(cl)`; otherwise `InputReceive(cl)`.
   - Type 2: `CalculNextReflect(cl, MissionGetNum())`, which calls `iaCalculPlayer`; then `InputGame(cl)` if `cl` is local.
   - Other types: nothing.
5. `0x4e2480` = local player; `ProcessInputGame(0..3)`.
6. **Gate 3 `0x42d3c0`:** state 0x12 continues. State 0x10 continues only in network games. Anything else exits at `0x42d4e2` (capture `gate3_state_left_during_input`).
7. In order: `MessageBoxCalcul`, `GameNextFrame`, `CalculIconeAction`, `ProjectileCalcul 0x46fc0f` (no register inputs; its Python entry takes the low byte of u32 `0x508f7c` as it stands here), `CalculEnginNextEtape 0x456db5`, `CalculBatimentNextEtape 0x4281c7`, `RechercheCalcul`, `PlayerInitAllianceCompteur`, `SetUpdateChamp`, `UpdateChamp`, `CalculMatiere`, `CalculCompteurMarche(local)`, `CalculCompteurProposition(local, 0)`, `NextAnimTerrain(u16 0x508720, u16 0x508722)`.
8. Network games: `NextAnimVegetFullMap`. Single player: `NextAnimVeget(u16 0x508720, u16 0x508722)`. Then `PlayerAttaqueCalculSympa`.
9. Network games exit here.
10. `TestFinDeMission(local)` stores AL in `0x4e05a0`; zero exits.
11. When `MissionGetNum` = 6 and u32 `0x4e061c` = 0: `MessageBoxSet(10, 500)`.
12. u32 `0x4e061c` += 1; below 100 exits. At 100: `PlaySnd_StopAllSound`, then `MenuInit(local, 0x13)` (`0x42c92c`), exit `0x42d4e2`.
13. Exit `0x42d4e2` clears byte `0x5099b0`; `0x42d4ea` is the epilogue.

**Gate 1 `0x42d14c`** ends the menu path. The frame runs only when the entry state copy is 0x10, the network flag is set and the current state is 0x10 or 0x12 (captures `gate1_single_player_state_0x10` and `gate1_network_state_0x10`).

**Cross-frame dependency:** `iaCalculPlayer` reads the structure counters `0x4dfaa8` and unit counters `0x4e1928`. These are rebuilt later in the same frame by `CalculBatimentNextEtape` and `CalculEnginNextEtape`, so the AI sees the previous frame's values.

### `GameNextFrame 0x45d015`

`inc dword [0x496d40]` (wraps; the image initializes it to 1), then `ret`.

## Unit dispatcher

### `CalculEnginNextEtape 0x456db5..0x456f0a` (shared tail `0x45179d`)

1. It zeroes:
   - u16 `0x4e1a38` and `0x4e1a3a`;
   - the u16 table `0x4e1a3c + owner·0x34 + type·2` (owners 0–3 × 26 types);
   - u16 `0x4e1928 + owner·2` for owners 0–3, and u16 `0x4e1930`.
2. For unit `i` = 0..799 with state byte `+2` ≠ 0 (pool `[0x4e19a0]`, stride 276):
   - If the state is not 0 or 4:
     - u16 `0x4e1a3c[owner][type]` += 1 when the owner is not 4 or 200.
     - `IATestUtilite(eax=1, edx=i)`.
     - For type ≠ 17: `0x4e1a3a` += 1 when the owner is the local player, else `0x4e1a38` += 1.
     - `0x4e1928[owner]` += 1 when the owner is not 200 and the type is not 5.
   - `EnginNextEtape(eax=i)`, in every case (state 4 included).

`MissionLoad`'s reset prefix stores 0xffff in `0x4e1a38`/`0x4e1a3a` (reported by missions), so their value before the first frame is not zero.

The capture `unit_loop_monde01` uses MONDE01's 16 serialized owner/type/state bytes plus five synthetic units. It confirms the order, that the state-0 unit is skipped, that state 4 is dispatched without `IATestUtilite`, and the counter values.

### `EnginNextEtape 0x45442c..0x456c34` (shared tail `0x44f29d`)

For a unit whose state is not 0 or 4, a common prelude runs first, in this order:
1. Sound volume and handle (`EnginGetVolume`, `PlaySnd_PostVolume`, `PlaySnd_StopSound`/`PostSound`).
2. Type-16 animation counter.
3. Reload advance (`0x454530..0x454591`, identified by combat): u16 `+0x102` grows by 1 up to the type value (u16 `0x4965de + type·50`) minus `BonusGetValEngin(owner, 3)`.
4. Target scan, when `([0x508f7c] + unit) & 0x1f` = 0, the state is not 14, 1 or 19, the owner is not 200, and the type is in {0–3, 8, 11, 12, 15, 16, 18–25} (types 14/16 also need byte `+0xda` ≠ 0). It calls `EnginTrouveCible 0x453f74`. With a target and an AI owner (`PlayerGetType` = 2) it sends `iagUnitSendMessage(unit, dl=0x49, ebx=target)`. With a target, a non-AI owner and state 7 it calls `SetAttaqueEngin(eax=unit, dl=1 (target mode: unit), bx=target)`.
5. Spell timer (`GetBit(+0xdc, 2)`, `SortilegeGetTempsFin(2)`, u16 `+0x9a` countdown). On expiry it calls `SetDyingEngin` and exits.
6. Fatigue branch for types 0–10 and 25: `CalculFatigue`, then message 0x4b for an AI owner or `EnginSetFatigue` otherwise.
7. The type-17 branch (`0x4549c2`).
8. The state switch `0x456c1c` (25-entry table `0x4543c8`). States 0 and 4 go straight to the switch.

Every branch call passes eax = the zero-extended u16 unit index and ignores the return value.

Static callees per state (`inventario.json` → `dispatch.engin_next_etape.states`):

| State | Target | Instructions | Callees reached (static) | Branch owner |
|---:|---|---:|---|---|
| 0, 8, 9, 10, 12, 14 | `454ccd` | 0 | direct exit | — |
| 1, 24 | `456886` | 106 | BatimentGetPlayer, BatimentEnDestruction, SetDeplaceEngin, CalculAttaqueEngin, PlayerGetType, iagUnitSendMessage. Target mode `+0xb7` (1 = unit, 3 = structure, 5 = cell) selects the inline validity checks `0x4567ce`/`0x45673b`, otherwise `CalculAttaqueEngin`. An invalid target sends message 0x4a for an AI owner, else `SetDeplaceEngin(unit, u16 +0x7e)`, then `+0xb8` = 0xffff | combat (whole body) |
| 2 | `4563da` | 88 | EnginEnArret, RotateEngin, DeplaceEngin | core |
| 3 | `455a61` | 58 | RotateEngin | core |
| 4 | `456ae5` | 165 | ResetEnginCollision, EnginRetire, RetireEngin, GetBit, DeselectionEngin, CreerSac | core (CreerSac: economy) |
| 5 | `456600` | 101 | BatimentGetPlayer, BatimentEnDestruction, SetEnginCollision, SetDeplaceEngin, CalculWorkEngin, SetMiniMap, MineEndWork, DecouvreTerrain, IllumineTerrain | economy |
| 6 | `4568ad` | 50 | — (inline) | ai-runtime |
| 7 | `456966` | 50 | AnimBallonStatic, Random | economy |
| 11 | `4564ef` | 18 | BatimentEnDestruction, SetDeplaceEngin, CalculConstruireBatiment | economy |
| 13 | `4558e4` | 117 | BatimentGetPlayer, BatimentGetType, BatimentEnDestruction, SetDeplaceEngin, CalculEntreBatiment, CalculEntreEngin | core (physical entry; economy queries and message 0x47 as named dependencies) |
| 15 | `45652f` | 72 | BatimentEnDestruction, SetDeplaceEngin, CalculReparer | economy |
| 16, 17 | `455e32` | 141 | EnginRetireType, SetDeplaceEngin, DeplaceEngin, TerrainGetSacType, TerrainRetireMatiere, TerrainEstSac | core |
| 18 | `455d26` | 86 | BatimentGetPlayer, BatimentEnDestruction, SetEnginCollision, SetDeplaceEngin, CalculTransporteEngin, SetMiniMap, DecouvreTerrain, IllumineTerrain | economy |
| 19 | `4554db` | 868 | harvest: BatimentGetPlayer/GetType/EnDestruction/EnleveMatiere/Adjacent, EnginGetVolume, SetEnginCollision, SetDeplaceEngin, DeplaceEngin, EnginRestaureEtat, TestRessource, SetMiniMap, PlayerGetType, MineEndWork, TerrainGetSacType, TerrainRetireMatiere, TerrainEstDecouvert, DecouvreTerrain, IllumineTerrain, ChercheVegetLibre, iagUnitSendMessage, PlaySnd_PostSound | economy |
| 20 | `455b28` | 158 | BatimentGetPlayer, BatimentEnDestruction, SetEnginCollision, SetDeplaceEngin, CalculDechargeCaveEngin, SetMiniMap, DecouvreTerrain, IllumineTerrain | economy |
| 21 | `4558b4` | 16 | BatimentEnDestruction, SetDeplaceEngin, CalculGareBatiment | economy (physical lodging: core) |
| 22 | `456520` | 4 | CalculPiege | combat (in principle) |
| 23 | `455fe2` | 297 | market/technology: BatimentGetPlayer/EnDestruction/GetCase/AjouteMatiere/EnleveMatiere/Adjacent, SetDeplaceEngin, DeplaceEngin, RetireEngin, RechercheTypeBatiment/EndTechnologie/GetBranche/GetNiveau, GetRessourceStock, MessageBoxSet, Random, MAJSympathie | economy |

`CalculEnginStatic 0x453062` has no direct caller and no pointer anywhere in the image; it is not part of the dispatcher.

**MONDE01 at load.** The serialized units are three type-0 units, one type 1, one type 7, two type 5 and one type 8 in state 7, plus eight type-9 units in state 14. The other 784 slots are state 0. The captures `unit_state_monde01_*` (all callees stubbed, scan frame forced) give the exact per-unit order:

| MONDE01 units | Captured calls, in order |
|---|---|
| Type 9, state 14 | `BonusGetValEngin`, `GetBit`, `GetBit`, `CalculFatigue`, `GetBit`, `GetBit`. The switch exits directly |
| Types 0, 1, 8, state 7 | Adds `PlayerGetType`, `EnginTrouveCible` after `BonusGetValEngin`, and `Random` from the state-7 branch at the end. A found target adds `SetAttaqueEngin` for a human owner or `iagUnitSendMessage(…, 0x49)` for an AI owner |
| Types 5, 7, state 7 | No scan; otherwise the same as types 0/1/8 |
| State 0 | Never dispatched by the loop. A direct entry makes no call |

## Structure dispatcher

### `CalculBatimentNextEtape 0x4281c7..0x4283e2` (shared tail `0x41db1a`)

1. `ResetTableauHangar`. When `[0x508f7c] % u16[0x495c02]` = 0, byte `0x4dfb9b` = 0.
2. u32 `0x4dfaa8[0..3]` = 0.
3. For structure `i` = 0..999 (`0x49a0c8 + i·276`) with state byte `+5` ≠ 0:
   - `0x4dfaa8[owner]` += 1 when owner `+4` < 4 and type `+8` is not 9, 12 or 17.
   - State 3: `DemonteBatiment(i)`, then the next structure.
   - Otherwise `IATestUtilite(3, i)`, `BatimentNextEtape(i)` and `cell = BatimentGetCase(i)`.
   - For each other player `p` < 4: `BatimentDecouvre(i, p)` when `!CaseEstDecouverte(cell, p) && BatimentEstDecouvert(i, p)`.
   - For each other player `p` < 4: when `BatimentContourEstIllumine(i, p)` disagrees with the flag byte `+0x110+p`, it calls `BatimentIllumine(i, p, ebx=1 or 0)` and updates the flag.
4. byte `0x4dfb50` = 0.

Capture: `structure_loop`.

### `BatimentNextEtape 0x4268d4..0x4281c7`

It switches on type byte `+8` − 1 through the 21-entry table `0x426880`. Types 0, 9, 21 and above exit at `0x4281c0`. Every branch call passes eax = u16 structure index and ignores the return value.

| Type | Target | Callees reached (static) | Owner |
|---:|---|---|---|
| 1, 2, 13, 16 | `426918` | BagContientTroupe, BagContient, CalculTroupe | economy |
| 3 | `426aff` | BagContient, BagContientTroupe | economy |
| 4 | `426c10` | BatimentLogeEngin, BonusGetValEngin, EnginSetEtat, BagAccepte, BagContient(Troupe), EnginNewPossible, CreerEngin, iagUnitSendMessage(0x43) | economy (CreerEngin: core, message: ai-runtime) |
| 5, 14 | `42698d` | AnimPorteBatiment, CalculTroupe, BagContient(Troupe) | economy |
| 6 | `428095` | CalculTroupe, BagContient(Troupe) | economy |
| 7 | `426d61` | BagContient(Troupe), RechercheAddScientifique | economy |
| 8 | `426a08` | AnimPorteBatiment, ControleArrivageHangar, CalculTroupe, BagContient(Troupe), SetTableauHangar | economy |
| 10, 11 | `426e43`, `427549` | turret: BatimentDecouvre, BatimentGetVolume, BatimentGetCase, TourelleTrouveEngin, TourelleTrouveBatiment, CibleTourelleValide, RechercheDecalageProjectile, EnginGetStart/GetCase/GetPlayer/EstVivant, Random, AngleCalcul, PlaySnd_PostSound | combat (in principle) |
| 12 | `427bb7` | BaisseTouteHerse, RemonteTouteHerse, HerseSousCurseur, Chemin_ModifieZone, SetCollision, ResetCollision | core (gate) |
| 15 | `427d5d` | CalculTroupe, BagContient(Troupe) | economy |
| 17 | `427ed9` | CristalCherchePretre | economy |
| 18 | `427eec` | CalculReparation, CalculTroupe, BagInit/Contient/ContientTroupe/Retire/Prend, TypeEnginGetNb | economy |
| 19 | `42803c` | BagContient(Troupe), BatimentSoignePerso | economy |
| 20 | `427da4` | CalculTroupe, InitNova, BagInit/Contient/ContientTroupe/Prend | economy |

For MONDE01's type-2 structure, the captures show `BagContientTroupe` → `BagContient` when both return 0, and `BagContientTroupe` → `CalculTroupe` when the first returns nonzero (`structure_type2_bag0/1`).

## AI players: `iaCalculPlayer 0x47f927`

`CalculNextReflect 0x47fbea(eax=player, edx=mission)` masks both registers to bytes, calls `iaCalculPlayer` and returns AL = 1, which `CalculGame` ignores.
- Player 4: `AvanceMonstre(4)` then `iaSolver(0x5148b0 + 4·16)`; the solver result is returned.
- Players 0–3, inactive byte `0x51a990 + p·16` set: return 0 without calls.
- Players 0–3 whose structure counter `0x4dfaa8[p]` and unit counter `0x4e1928[p]` are both 0: byte `0x51a995 + p·16` += 1. At 10 it calls `iagUnitDeleteAllGroups(p)`, sets the inactive byte and returns 0. Otherwise the counter is cleared.
- Kernels run in order `iagUnitNoyau(p)`, `iagVilleNoyau(p)`, `iagRessNoyau(p)`, `iagWarNoyau(p, mission)` and `iaSolver(0x5148b0 + p·16)`. The first nonzero result is returned.

The six `ia_calcul_player_*` captures are reproduced exactly by core's committed `ia.atualizar_ia`: call addresses, arguments, return values and `EstadoIA` updates (`test_core_orchestration_reproduces_ia_calcul_player`).

## AI tables

**`iaInit 0x47f328` has no caller and no pointer in the image.** Program start uses `IaAlloc 0x47fb15`, called from `ProgInit+0x2e7` (`0x474ed2`). Its order (capture `ia_alloc_program_start`):
1. `iaRandom(0)`, which seeds the RNG u32 `0x498db4` from `timeGetTime` (a declared binding; the M1/M2 oracles must bind the clock).
2. `debugSymLoad("RISING.SBL")`.
3. `iaProbInit` → `iaProbLoadBinaryRules("RISING.RUL", 1)`. This is file I/O; core's `simbolos_ia.ler_rul` parses the format.
4. `iagUnitInit` (returns 0, no store), `iagRessInit`, `iagVilleInit`, `iagWarInit`. Their constants come from `iaConfigGetValue 0x47fc54`, which returns its default argument. The first nonzero result aborts the sequence.
5. `debugSymUnload`, entered by tail jump.

IaAlloc writes the following u32 constants:

| Region | Writer | Values |
|---|---|---|
| `0x498c10..0x498c20` | iagVilleInit | 2000, 2500, 1000, 1000 |
| `0x498c38..0x498c94` (12 cells) | iagRessInit | |
| `0x51bcdc..0x51bcfc` | iagRessInit | 100, 100, 100, 5, 80, 5, 3, 2 |
| `0x498cb0..0x498cd4` (8 cells) | iagWarInit | |
| `0x498cf4..0x498d5c` (26 cells) | iagWarInit | |
| `0x521350..0x521368` | iagWarInit | 10, 10, 40, 10, 10, 6000 |

The cells without listed values carry them in `capturas-originais.json`. The whole-`MissionLoad` oracle inherits this program-start state; `MissionLoad` does not produce it.

**`IaReset 0x47f36e`** is called only from `MissionLoad+0x2fd` (`0x46c5cc`, between `PlayerRetrieve` and `MarcheResetAll`) and `MissionLoadName+0x3ab` (`0x46c98e`). The caller loads AL, but IaReset never reads EAX.
- For each player `p` = 0..3 whose type byte in the 20-byte player records at `[0x5080a8]` (via `PlayerGetType`) is 2, it sets up the context `0x51a98c + p·16`:
  - only when bytes `+5..+8` are all zero (first reset; the context persists across missions): cumulative research-branch thresholds in bytes `+5..+7`, and byte `+8` = 100. A favored branch (player 1 → 1, player 3 → 0, otherwise `iaRandom(4)`) receives r = `iaRandom(20)` + 30 points and each other branch (100 − r)/3;
  - byte `+5+k` = 0xff for each branch k whose `RechercheGetNiveau(p, k)` reaches `0x498464[k]`;
  - a branch drawn with `iaRandom(100)` against the thresholds (0xff branches skipped), redrawn while it is branch 3 and `MissionGetNum` < 7, then `RechercheSetBranche(p, branch)`;
  - `+4` = 1 when the player has no living unit (the inactive byte read by iaCalculPlayer). Otherwise `+4` = 0, `+0` = 0, `iagVilleSetMode`/`iagRessSetMode`/`iagWarSetMode(p, 0)`, and bytes `+1, +2, +3, +9` = 0, 1, 0, 0.
- Then, in order: `iaProbReset`, `iagUnitReset`, `iagVilleReset`, `iafRessourceReset`, `iagRessReset`, `iagWarReset`, `InitMissionMonstre`. Any nonzero result is returned and skips the rest.
- `iaProbReset` runs `listInit(0x5148a0, base 0x512320, 100, stride 0x60, chain=1)`, then the five contexts `listInit(0x5148b0 + 16k, 0x512320, 100, 0x60, 0)`. `listInit` takes eax=header, edx=base, ebx=count, ecx=stride and one pushed flag (`ret 4`). It writes header `[0]`=head, `+4`=count, `+8`=stride, `+12`=base, and with the flag set it chains the records' first dword. Core's `MaquinaTarefas` constructor models this memory without executing it.

The capture `ia_reset_empty_world` (player types 1, 2, 0, 0, 2; no live unit or structure; world queries stubbed) writes these regions:

| Region | Bytes | Widths | Writer |
|---|---:|---|---|
| `0x498db4` | 4 | 4 | iaRandom (RNG state) |
| `0x50a9cc`, `0x50ae80`, `0x50b134`, `0x50b178..0x50b184` | 1+4+1+12 | 1/4 | InitMissionMonstre |
| `0x512320..0x514900` | 9696 | 4 | listInit (100 task records × 0x60, free list `0x5148a0`, five contexts `0x5148b0`) |
| `0x51a9a0..0x51a9a5` | 5 | 1 | IaReset (AI context of player 1) |
| `0x51a9cc..0x51b664` | 3224 | 1/2/4 | iagUnitReset (100 groups × 32 at `0x51a9e0`), iafRessourceReset |
| `0x51b6c4..0x51b718`, `0x51b7e4..0x51b84a` | 84, 102 | 2/4 | iagUnitReset (unit pools at `0x51b664 + p·0x60`) |
| `0x51b8c8..0x51b938` | 112 | 2/4 | iagVilleReset (city table `0x51b84c + p·0x7c`) |
| `0x51bae4..0x51bb10`, `0x51bb28..0x51bb82` | 44, 90 | 1/2/4 | iagRessReset (`0x51ba3c + p·0xa8`) |
| `0x51ce44..0x51de68`, `0x520234..0x521234` | 4132, 4096 | 2/4 | iagWarReset |

Every cell with its first and last value and its writer is in the capture. Stage 2 turns these into exact providers; a different player or world fixture writes more cells.

`InitMissionMonstre 0x47af90` consumes the monster tables that missions loads (`carregar_entrada_monstros_missao`):
- `0x50a9bc`: HumanOnly u8; dwords +4/+8/+12 ProbaCaveJoueur/ProbaCaveIA/ProbaEmbuscade; u16 count at +18; 100 × 12-byte records at +20.
- `0x50af84`: 16 × 26 group type counts, then 16 group counts at +416.
- The live `Random` state `0x497164`.

**`IAResetAttaque 0x47c162` has no caller and no pointer in the image.** It is not part of `MissionLoad`.

## Rule-VM world operations

The rule program (`relatorios/regras-ia.json`, RUL SHA-256 recorded there) uses 140 operation names: 1,157 instructions resolved to 136 original addresses (aliases share bodies). Each body's interval and hash, callees, globals and provider families are in `inventario.json` → `operations.records`. Families are labelled by callee-name rules listed in `extrair_contrato_ia.py`; ownership follows the table above.

Committed core coverage (probe of `MaquinaTarefas.executar_operacao` at base `8a499a9`):
- 15 names are served without world state: `V_Attendre`, `B_Bidon`/`B_AccessibiliteChemin`/`B_AccessibiliteBatiment`, `B_GicleUniteAmieDeZone`/`B_TestUniteAmieSurZone`/`B_TestUniteEnnemieSurZone`, `B_Egalite`, `B_Superieur`, `I_Addition`, `I_Soustraction`, `I_PourcentageAB`, `I_Affecte`, `I_NumMission`, `I_Divise`.
- 4 need the unit world: `V_DeplacerUnite`, `V_DeplaceGroupe`, `I_DonneTypeUnite`, `I_AttenteMessageGroupe`.
- The other 121 are pending world operations.

| Provider families needed | Operations (original address) |
|---|---|
| ai-runtime AI state (31) | I_DonneForceEnnemieDansZone `47fe9b`, I_DonneForceGroupeDansZone `47fead`, B_InitConflit `47febf`, B_NewConflit `47fee0`, V_FreeConflit `47ff22`, I_CommandeForceDefense `47ff34`, B_AttenteConflit `47ff4d`, B_TestUniteDanger `47ff65`, V_AttacheConflitGroupe `47ffa4`, I_DonneChampAssocieGroupe `48181a`, I_DonneNoGroupe `481c28`, V_LibereGroupeVide `481c38`, B_TransfertUnite `481c4a`, B_CompleteGroupe `481c75`, B_AjusteNbUnitesGroupe `481c9b`, V_MiseADisposition `481cb8`, I_AttenteMessageGroupe `481f1a`, I_AiJeUniteDansGroupe `481f2e`, I_RecupereNoGroupe `481fb4`, V_AttendreDispatcher `481fc4`, I_DonneGroupeNonComplet `482000`, V_SetMaxUnites `482010`, I_DetermineTempsTrajet `482354`, B_TransfertUniteFastest `482433`, V_BatimentNestPlusEnConstructionWithAbort `482610`, V_MiseAJourBatimentConstruit `482630`, B_AiJeBatimentEnCoursConstruction `48264a`, V_MiseAJourBatimentEnCoursConstruction `482667`, I_AttenteBatimentConstruit `482679`, I_AttenteMessageBatiment `482697`, V_AttendreRessource `485d53` |
| no callee: arithmetic or direct table access (27) | B_EtatMarche `46030a` (market byte `0x4e2918`), V_iaMonstreAttendLaReponseVachementCoolMemeQueJeLaVeux `47b6db` (monster tables `0x50ae80`, `0x50b134`), V_Attendre `47da7a`, B_AccessibiliteBatiment/B_AccessibiliteChemin/B_Bidon `47f31c`, B_GicleUniteAmieDeZone/B_TestUniteAmieSurZone/B_TestUniteEnnemieSurZone `47f322`, B_Egalite `481280`, B_Superieur `481296`, I_Addition `4812ac`, I_Soustraction `4812b9`, I_PourcentageAB `4812d0`, I_Affecte `4812f4`, I_Divise `481302`, I_DonneMaxExploitantsDansChamp `481806`, B_TestGroupeVide `48232f`, V_SetChampExploite `485d7b`, V_SetChampNonExploite `485dfc`, V_SetProductionColonsOn `485e53`, V_SetProductionColonsOff `485e66`, B_TesteProductionColons `485e7c`, V_SetMineExploitee `485e98`, I_DonneMineAssocieeGroupe `485ec2`, B_TestMaxChampsExploites `485ef3`, V_AffecteComportement `4897a5` |
| ai-runtime AI state + core units (16) | I_DonneForceGroupe `47fc58`, V_EntreBatiment `481e07`, V_ActiveBatiment `481e4f`, V_VideEngin `481e88`, V_EntreDansEngin `481ece`, V_DeplaceGroupe `481f4c`, V_Recolter `482020`, V_CueillirChamp `482085`, V_SetNavetteCaveToCulture `4820e7`, V_ExploiteMine `48213c`, V_RienFaire `48219e`, V_ExploitePiece `4821f0`, V_DeposerPiece `482265`, V_PrendrePiece `4822ab`, V_TricheToutLeMondeMange `482501`, I_DonnePositionGroupe `482550` |
| structures (13) | I_DonneBatimentDansZone `4801d2`, I_AiJeBatiment `480644`, B_EtatBatiment `48068f`, I_DonneTypeBatiment `4806db`, B_OccupationColonMinBatiment `4806ed`, V_BatimentSortColon `480712`, I_DonnePositionBatiment `480803`, I_DonneBatimentOuEstUnite `48094a`, B_TestBatimentBesoinColon `480abd`, I_DonneBatimentSurCase `480ace`, I_DonneNationBatiment `480d56`, I_DeterminationEnnemi `480d68`, I_CombienCouteBatiment `481399` |
| economy players/diplomacy (10) | V_FixeAlliance `480d97`, B_Allie `480e4f`, V_DeclareGuerre `480e72`, I_DonneNationPlusHaute `480ea6`, I_DonneNationPlusBasse `480ee2`, I_CombienDAlliances `480f16`, B_ChoixPlaceLibre `480fc7`, I_RecupereSympathie `481034`, I_NombreAlliances `481075`, I_ChercheNationPasAllie `4810aa` |
| economy resources/production/technology (10) | B_AiJeConnaissanceBatiment `47ffd8`, B_AiJeConnaissanceFutureBatiment `48001e`, B_TestRessource `481400`, I_DonneValeurChamp `4817f2`, I_DonneValeurPiece `481b9e`, B_EncorePiece `481bb1`, I_DonneValeurMine `481bcf`, V_InterditCaseMine `481be8`, V_RestoreCaseMine `481c03`, B_TestMaxRocheDansStock `485f20` |
| core terrain/navigation + structures (7) | I_ChercheWayPoint `4802fb`, I_DonneBatimentProche `4808b4`, I_DonneBatimentMarchandage `480cee`, I_DonneCaveAssocieeChamp `481738`, I_DonneCaveAssocieeMine `48179e`, I_CherchePiece `4819d7`, I_DonneCaveProchePiece `481b46` |
| core units (7) | I_DonneForceNation `47fe4b`, B_AiJeConnaissanceUnitee `47fffb`, I_ChercheCivilProche `4804a1`, I_DonneCaseLibreProcheGhostBatiment `480617`, I_DonneTypeUnite `481133`, V_DeplacerUnite `481146`, I_CombienCouteUnite `481372` |
| structures + C runtime `memset` (2) | I_DonneBatimentOccupe `480760`, I_DonneBatimentPasPlein `480951` |
| ai-runtime + core units + economy (2) | V_ConstruireBatiment `481ce3`, V_ReparerBatiment `481d7e` |
| core terrain/navigation + structure ghosts + structures (2) | I_TrouvePlaceLibreProche `480064`, I_TrouvePlaceOccupeProche `4800f1` |
| structure ghosts (2) | B_ReserveGhostBatiment `480816`, V_LibereGhostBatiment `480842` |
| ai-runtime + combat + core units (1) | V_AttaquerBatiment `4822ed` (calls `SetAttaqueEngin`) |
| ai-runtime + core terrain/navigation + core units (1) | I_CompleteMilitairesDansGroupe `47fce9` |
| ai-runtime + core terrain/navigation + economy + structures (1) | I_ChercheChampNonExploite `481426` |
| ai-runtime + core units + economy + structures (1) | V_TricheColon `482579` |
| core RNG + core terrain/navigation + structures (1) | I_DonneBatimentAAttaquer `480aed` |
| core terrain/navigation (1) | I_DonneCaseLibreZoneProche `4801a2` |
| core terrain/navigation + economy + structures (1) | I_ChercheMine `481833` |
| economy + user interface (1) | V_BatimentRecruteUnite `480731` (`InitRecruteTroupe`, `BatimentSelection`) |
| missions (1) | I_NumMission `4812f7` |
| structure ghosts + structures (1) | I_DonnePositionMaVille `480859` |
| user interface (1) | V_RefuseAlliance `480e1f` (`MessageBoxSet`) |

The structure-ghost table is filled by missions' `LoadBatimentGhost 0x47bcc7`; its runtime queries (`GetCaseOfGhost`, `OccupationIndiceGhost`, `Implante/LiberePlayerInGhost`) have no owner yet. They are requested from missions/core in `HANDOFF.md`.

## Messages

**`iagUnitSendMessage 0x4829c8`**, called with eax = u16 unit, dl = message, ebx = payload:
- It returns immediately unless `PlayerGetType(owner)` = 2.
- The group is u32 unit `+0x10c` (0xffffffff = none; group records are 32 bytes at `0x51a9e0`).
- Messages 0x41–0x4c use the table `0x482998`; anything else returns. Captured branches:
  - 0x41: `iagUnitRemoveFromGroup`
  - 0x42: `RemoveFromGroup` → `iagUnitDispatch`
  - 0x43: `EnginGetPlayer` → `iaProbPost`
  - 0x44: `iagWarUnlockTargetAfterDeath` → `iagWarProbReturnTo` → `RemoveFromGroup`
  - 0x45: `iagUnitDispatch` → `EnginGetType` → `EnginGetPlayer` → `iaProbPost`
  - 0x46: `RemoveFromGroup` → `Dispatch` → `EnginGetType` → `EnginGetPlayer` → `iaProbPost`
  - 0x47: nothing
- Messages 0x48/0x4a/0x49/0x4c/0x4b call the behavior handler selected by group byte `+0x1b` (set by `V_AffecteComportement`) from the 12-entry table `0x498e94`. Each record holds 5 slots, in that message order. Message 0x4a also calls `iagWarProbReturnTo` when group `+0x0c` is a task. Message 0x4b calls `EnginSetFatigue` when the behavior byte is 0xff.
- Behavior 0's record pointer (`0x521368`) lies outside initialized data and is resolved only at run time.

Call sites with their codes (static):

| Code | Call sites |
|---|---|
| 0x42 | `BatimentEnleveUnColon` ×2, `EnginRetire` |
| 0x43 | `BatimentNextEtape` (type 4) |
| 0x44 | `BallonPrepareSortie`, `SetDyingEngin` |
| 0x45 | `EnleveTroupeHangar`, `SortTroupeHangar`, `CalculTrajectoire`, `BallonPrepareArrivee` |
| 0x46 | `SortieTroupe` |
| 0x47 | `CalculEntreBatiment` |
| 0x48 | `EnginInfligeDegat+0x162` |
| 0x49 | `EnginNextEtape` scan |
| 0x4a | `EnginNextEtape` ×2 |
| 0x4b | `EnginNextEtape` fatigue |
| computed | `CalculEntreBatiment` ×2, `EnginInfligeDegat+0xbe`, `iagMessTestSendMessageEngin` ×2 |

**`iagVilleSendMessage 0x484808`**, called with eax = u16 structure, dl = message, ebx = payload:
- It requires `BatimentGetPlayer` < 4 and `PlayerGetType` = 2. The city record is `0x51b84c + p·0x7c`.
- The table `0x4847f8` covers messages 1–4:
  - 1: per-type counter += 1, `iagRessAddToCaveList` for type 3, `0x48499d`
  - 2: per-type counter −= 1, `iagRessRemoveFromCaveList` for type 3, `0x48499d`
  - 3: `0x48499d`
  - 4: `EnginGetCase(payload unit)` → `iagWarSearchBattleFromPos`, then `iaProbPost(p, 0x13, …)` when no battle is found, else `iagWarAddEnnemyToBattle`
- Callers: `BatimentInfligeDegat` (2), `VendreBatiment` (2), `DetruireBatiment` (2), `SortieTroupe` (3), `CalculTrajectoire` (3), `InfligeDegat` (4), `iagMessTestSendMessageEngin` (computed).

`MissionLoad`'s reset prefix (`IconeReset`, `TerrainReset`, `MiniMapReset`, `BatimentResetAll`, `EnginResetAll`, `ProjectileReset`, `MessageBoxInit`, `BallonInit`) contains no AI message table. `MessageBoxInit` is the UI message box.

## Stage 2 — AI table reset and program initialization

Recovered from WIP `ad97e4228c67dac24ed8024c46183e8628cf7ef8`; its original capture is preserved unchanged as `evidencias/captura-reinicio-original.json`. Recovery validation for round `CXR-20261028-01` passes all 36 native tests (zero skips/failures/errors) and the local domain gate (36 discovered, four explicit native skips); results are separate from historical evidence in `validacao/recuperacao-stage2-native.json` and `recuperacao-stage2-local.json`. The recovered implementation is `reinicio_ia.py`; `memoria_ia_runtime.py` supplies explicit inherited memory views. All addresses retain the intact-executable identity stated above.

### Public providers and inherited memory

| Entry | Original | Inputs and return |
|---|---|---|
| `reiniciar_ia(memoria, mundo)` | `IaReset 0x47f36e` | `MemoriaDeclarada` and explicit world providers; returns original EAX (zero or the first nonzero reset-tail result). Missions ignores this value at `0x46c5cc` / `0x46c98e` |
| `iniciar_ia_programa(memoria, ligacoes)` | `IaAlloc 0x47fb15` | Explicit clock, SBL and rule-loader bindings; returns original EAX. A rule-loader error returns before constant-table initialization; successful completion returns `debugSymUnload`'s EAX |
| `resetar_ataques_ia(memoria)` | `IAResetAttaque 0x47c162` | Count and 100 ten-byte attack records; no promised register return. No caller or pointer exists in the intact image, so this is not inserted into MissionLoad |

`MemoriaDeclarada(segmentos, regioes)` takes `(absolute_base, writable_byte_buffer)` segments and `(start, end_exclusive, name)` regions. Reads/writes use the original little-endian widths and u32 address arithmetic; writes mask to their width. Every translated access must lie in both a mapped segment and a declared region, otherwise `AcessoNaoDeclarado` names the address and width. World-provider effects use `escrever_mundo`, which requires a mapped inherited buffer and retains the caller's region policy for translated accesses.

For `reiniciar_ia`, declare `REGIOES_REINICIO` and the actual 800×276-byte unit pool at `[0x4e19a0]` plus four 20-byte player records at `[0x5080a8]`. Declare `REGIOES_ALOCACAO` for program initialization and `REGIOES_ATAQUES` for the attack reset. These constants describe AI access regions; callers must map every inherited buffer used by their world providers as well. The validation addresses `0x1000000` / `0x1100000` are explicit fixture allocations, not production defaults. No whole-image constructor or zero-filled game state is installed by the public providers.

### Calls and mutation order

The `mundo` object supplies the following original-name methods. Each call receives `sitio=original_CALL_address`; narrow inputs are already masked to the width below. No adapter to a sibling world's object model is silently installed.

| Method | Inputs | Consumed result |
|---|---|---|
| `PlayerGetType` | u8 player | AL |
| `RechercheGetNiveau` | u8 player, u16 branch | AX |
| `RechercheSetBranche` | u8 player, u8 branch | effect only |
| `MissionGetNum` | none | AX |
| `EnginEstVivant`, `EnginGetType`, `EnginGetEtat` | u16 unit | AL |
| `TypeEnginEstMonstre` | u8 type | AL |
| `EnginSetPlayer` | u16 unit, u8 player | effect only |
| `BatimentExiste`, `BatimentGetPlayer`, `BatimentGetType` | u16 structure | AL |
| `GetRessource` | u8 player | four u16 output values; the reset stores outputs 0–2 and preserves the original fourth-field behavior |

IaReset first visits players 0–3. For AI players it retains nonzero inherited research thresholds, otherwise generates them using core's `cadencia.proximo_aleatorio`; it selects research and scans living units, then initializes modes only for a player with a living unit. It then runs `iaProbReset` → `iagUnitReset` → `iagVilleReset` → `iafRessourceReset` → `iagRessReset` → `iagWarReset` → `InitMissionMonstre`, in original order. Unit/group links, group hints, city/resource/war fields, monster ownership and list order mutate in place. Partial effects are retained on dependency failure. The task-pool free/context-list reset is the agreed AI-table initialization; VM execution, waiting, lists and task operations remain core-owned and are not forked. The core positive RNG path is imported rather than copied.

IaAlloc supplies `timeGetTime(sitio=0x489789)`, `debugSymLoad(0x494f84, sitio=0x47fb21)`, `iaProbLoadBinaryRules(0x494f28, 1, sitio=0x47d1af)` and `debugSymUnload(sitio=0x47fb67)`. A real binding must supply its actual mapped memory effects; validation's declared return-only bindings do not demonstrate those loaders. The original `iaConfigGetValue` body returns its EBX default. The original war initializer's `sprintf` builds only a stack-local key passed to that getter; Python emits the resulting ordered constant stores and retains all unit-weight defaults. The native oracle executes that formatting code unchanged.

A missing reached provider raises `DependenciaIA(rotina, sitio)` at its first original call. Providers' own errors propagate. Unsupported RNG states or nonpositive arguments raise a named dependency; no replacement RNG value is chosen. Research/context and group-list inputs must be well formed for the original path: arbitrary corrupt links, cyclic unit lists and arbitrary modes are not claimed as a safe public domain. An empty monster spec with a nonzero group count and its creation flag retained causes the original to create/delete the same empty group forever; Python raises `NaoTerminaNoOriginal` at `0x47b1f4` after the same stores. No timeout is accepted as evidence for that assertion.

### Original coverage and validation boundary

`auditar_reinicio_ia.py` writes the additive `evidencias/reinicio-byte-audit.json`: 32 game/RNG routines in the static transitive closure, exact reached-instruction intervals and SHA-256 values, and 18 explicit boundaries (13 world providers, three file/SBL bindings, the clock import thunk and stack-local `sprintf`). It includes helper intervals not exported by Stage 1. Static closure is not branch coverage. Stage 1's manifest, listings and captures are unchanged.

`oraculo_reinicio_ia.py` executes the intact routine and all reached game bodies on core's `BancadaX86`. World providers execute natively; entry arguments, return EAX and non-stack writes are observed, not substituted. Only IaAlloc's declared file/SBL bindings and clock are substituted. `MundoRepetido` checks original-name call order, call sites and arguments while applying the observed effects to Python's inherited images. The whole compared image is DGROUP+.bss `0x494000..0x523000` (585,728 bytes), units (220,800 bytes) and players (80 bytes); ordinary routine comparison excludes CPU scratch registers and stack locals. The separate intentional-cycle proof compares registers/flags/segments, the complete 65,536-byte stack and all three images at three consecutive visits to the same original checkpoint after one transient visit; all resumed segments must return to their declared stops, and any external call during the repeated cycle fails the proof.

The preserved WIP capture has 19 cases: 11 complete IaReset entries, three IaAlloc entries under declared bindings, one uncalled attack reset and four group helpers; 66,977 observed calls/bindings and 133,960 bench segments, plus nine separately captured partial-state checkpoints. These are historical captures; fresh results are recorded in the handoff and `validacao/`. MONDE01 supplies actual serialized structures/units/auxiliary tables through committed missions loaders, with explicit fixture player types and surrounding inherited state. This is not the complete MissionLoad sequence, terrain placement, frame progression or a mission-runtime test. All original media and predecessor captures remain unchanged.

## Public API shape

APIs are published only after original comparison. They follow the repository conventions: explicit inherited buffers with exact widths, read-only query callbacks, effect callbacks named after original routines, named dependency exceptions carrying the original call address, partial effects retained.

| Entry (Stage 2 delivered; others planned at the time — the current input-chain API is under "Current state") | Original | Inputs | Result |
|---|---|---|---|
| `iniciar_ia_programa(memoria, provedores)` | `IaAlloc 0x47fb15` | RNG clock binding, rule-file provider | Original EAX; ordered constant stores and RNG seed |
| `reiniciar_ia(memoria, provedores)` | `IaReset 0x47f36e` | Player table, Recherche, unit, structure and resource queries, mission number | Original EAX; ordered stores into inherited regions |
| `quadro_jogo(mundo, provedores, *, entrada=None)` | `CalculGame 0x42c868` | Live world, provider bundle per branch | Per-frame checkpoint metadata and the reached named dependencies |
| `proxima_etapa_unidade(mundo, indice, provedores)` | `EnginNextEtape 0x45442c` | u16 unit index | Branch taken and provider result |
| `proxima_etapa_estrutura(mundo, indice, provedores)` | `BatimentNextEtape 0x4268d4` | u16 structure index | Branch taken and provider result |
| `operacoes_mundo(mundo, provedores)` | rule-VM world operations | — | The `operacoes` dictionary for `MaquinaTarefas` |

## Validation

```sh
python3 -B scripts/check.py --domain ai-runtime
RISING_EMULAR=1 python3 -B -m unittest discover -s pesquisas-paralelas/ia-runtime/testes -p 'test_*.py' -v
```

- `test_evidencias_contrato.py` checks every exported interval's SHA-256 against the intact bytes. It also rebuilds every listing from its bytes, checks data-table values, regenerates the manifest/inventory/listings from the original and compares them with the committed files (except the core-status snapshot and core input hashes), and checks the contract facts stated here.
- `test_capturas_contrato.py` asserts the captured orders and gates, and runs core's `ia.atualizar_ia` against the six iaCalculPlayer captures. With `RISING_EMULAR=1` it replays all 57 scenarios natively and requires whole-document equality with the committed captures.
- `test_namespace.py` guards module basenames and core primitives.

## Stages

1. **Contract stage (this manual).** Inventory, captures and ownership; no implementation.
2. **AI table initializers (recovered Stage 2):** `IaAlloc` and `IaReset` with their callees as exact providers for `MissionLoad`'s `IaReset` tail (M1).
3. **Frame skeleton:** `CalculGame` with committed providers and named stops; frame oracle on core's declared-binding facility (core Stage 15).
4. **Unit dispatcher** for the MONDE01 states (prelude, states 7 and 14, then the states that arise), then the structure dispatcher skeleton.
5. **AI kernels and operations** for the first MONDE01 raid (`iagWarNoyau`, group movement, `V_AttaquerBatiment`, `B_TestUniteDanger`, `I_DonneForce*`), then the remaining operations by frequency.

The bounded raw-memory IaReset provider is implemented and compared against the original. L9 still needs production provider adapters, load-tail composition and complete MissionLoad state equality; this stage does not close that consumer/integration gap. Actual rule/SBL file effects, caller-owned frame/kernel bodies and all live mission behavior remain separate.

Status, counts and requested contracts live in `pesquisas-paralelas/ia-runtime/HANDOFF.md`.


## Stage 2b — production delegate adapter (preparation; native gate pending)

`reinicio_ia_compartilhado.ReinicioIACompartilhado(memoria, mundo, mercado, missao_u8, *, pesquisa64=None)` is the callable adapter under preparation. `memoria` is an explicit `MemoriaDeclarada`; `mundo` is the actual Core world and `mercado` is the actual economic Mercado with its shared Economia. No game state is allocated by the adapter. The constructor requires exact same host-buffer range (address **and** length) for the original unit/player pointees, inline structure pool, AI group pool, resource table and one-byte mission field; a supplied research view must alias all 64 bytes at `0x5080f4`. Equal copies, overlapping mappings and initially divergent iterator scalar slots are rejected before effects. It does not silently rebind a provider's buffer. Writable contiguous B views are the protected alias-verification domain.

The adapter delegates live reads to committed Core `tipo_unidade`, `tipo_unidade_monstro`, `MundoUnidades.viva`, Missions `numero_missao` / `existe_estrutura`, economy `Mercado.tipo_jogador` / `Economia.consultar` and combat `batiment_get_player`. The original `sitio` is wrapper trace metadata and is not passed to owner functions. On AI writes to `0x51b844`/`0x51b848`, its memory view updates the raw slots and existing Core scalar attributes together; it verifies their agreement on reads and preserves partial effects. All other memories retain their actual aliases.

The planned Economy leaves are consumed only from `consultas_reinicio_economia.py` in this same committed checkout: `nivel_pesquisa(pesquisa64,jogador,ramo)`, `definir_ramo_pesquisa(pesquisa64,jogador,ramo)` and `tipo_estrutura(pool,indice)`. Until their actual module is available, a reached call raises `DependenciaIA` at the original site. Missing research input likewise stops at its first reached research call. `EnginGetEtat` and `EnginSetPlayer` remain explicit dependencies; the latter is not approximated with an owner-byte store. A caller must continue from its actual checkpoint rather than replaying IaReset from entry after partial stores.

Player controls are inherited live bytes, read afresh. The adapter does not select human controls to skip research. The 11 frozen IaReset inputs predate this adapter; `validar_adaptador_reinicio_ia.py` builds declared fixture object graphs over those same bytes and uses **actual production delegates**, not `MundoRepetido` or recorded callback results/effects. It compares completed images/EAX/call order with historical originals; opt-in native mode additionally executes a complete or exactly stopped original run for each input. The fixture builder explicitly aliases only the provider buffers IaReset consumes; other synthetic constructor state is not a loaded mission.

Current light result before Economy leaves land: one declared-control MONDE01 input completes; ten other frozen inputs reach named dependencies. This does not determine actual program/menu initialization controls. Four host-alias/control guard tests pass, with the native test explicitly not run. No native/domain/integration gate has yet established this adapter as delivered; full MissionLoad, real M1 state and frame runtime remain outside this preparation.


At 18:13 BRT a separate preparation replay used the coordinator-authorized, hash-checked immutable Economy commit `4181758` through a test-only forwarding subclass and unique ignored-scratch module identity. Both declared-control MONDE01 fixtures then match their full historical original final images/EAX/call sequence, including the declared AI-player fixture. Eight other fixtures stop at missing `EnginGetEtat` (`0x4843ea`) and one at missing `EnginSetPlayer` (`0x47b01f`). This is actual-delegate local preparation, not fresh native partial-state validation, main integration or original/current startup-state evidence. The production adapter source remains unchanged; it must consume the actual validated Economy module after that provider integrates.


Final focused proof at 18:23:56 BRT uses the **actual same-checkout integrated Economy provider** from main `85dc813`, with no test-only override. The 11 frozen-input original full/stopped runs pass against the real adapter over 75,967 segments: two complete MONDE01 fixtures and nine exact dependency states (eight missing EnginGetEtat, one missing EnginSetPlayer). Iterator aliases, images, returns where consumed and provider order agree. Source revision `a5316d4`; native report `pesquisas-paralelas/ia-runtime/validacao/stage2b-adapter-native.json`. Full suite/domain/helper integration and real mission were **not run** under this final bounded grant. The adapter remains a feature-branch WIP with focused original evidence, not a main delivery or L9/full MissionLoad closure. Heavy lease released on child exit; no new development after 18:25.

## M2 — frame pipeline inventory at the M1 post-load state (step 1, static)

`inventario_quadro_m2.py` writes `evidencias/inventario-quadro-m2.json`. It reads only intact bytes, SBL names and the frozen accepted M1 capture `pesquisas-paralelas/missoes/evidencias/captura-carga-missao-original-v2.json` (file SHA-256 `eb7d2303…`, final state `58a5020e…`, read-only, every block hash verified). Nothing is executed. **Input label: "M1 post-load input"** — MissionLoad's real return `0x42d22d`. The load-entry tail `0x42d22d..0x42d2de` (RestoreAll, SetClipping, frame-counter reset, `MenuInit(local, 0x12, 1)`, `InitGameZone(1, 0)`) still runs before the frame body, so its writes are not yet in this state. The exact frame-1 input is Missions' first-frame oracle.

### Frame body `0x42d2de..0x42d4f5`: order, gates and owners

| Site | Callee | Owner | Reached at MONDE01 frame 1 |
|---|---|---|---|
| `42d2de` | PlayerAttaqueReset (`ret`) | economy | yes |
| `42d2e3` | EvenementEnCours (AL = byte `0x4e1b0e`) | missions | yes; post-load byte 0 → continue (gate 2 `jne 42d2ea`) |
| `42d328` | MCICD_Play | audio (second wave) | **yes**: byte `0x4e2f28` = 0 post-load. A frame oracle must bind MCI CD audio |
| `42d379` | PlayerGetType(cl), cl = 0..4 | economy | yes, five calls |
| `42d33b`, `42d342` | InputGame, InputSend | ai-runtime input/network (second wave) | player 0 (type 1, local) |
| `42d34b` | InputReceive | network (second wave) | no (no remote type-1 player) |
| `42d354`, `42d35d` | MissionGetNum, CalculNextReflect | missions, ai-runtime | players 1, 2, 3 and **4** |
| `42d36c` | InputGame after AI | ai-runtime | no (local player is human) |
| `42d3b0` | ProcessInputGame(0..3) | ai-runtime | yes, four calls |
| `42d3c9`/`42d3ce` | gate 3 | — | state `0x12` (stored by MenuInit before the body) continues |
| `42d3e1`…`42d441` | MessageBoxCalcul, GameNextFrame, CalculIconeAction, ProjectileCalcul, CalculEnginNextEtape, CalculBatimentNextEtape, RechercheCalcul, PlayerInitAllianceCompteur, SetUpdateChamp, UpdateChamp, CalculMatiere, CalculCompteurMarche(local), CalculCompteurProposition(local, 0), NextAnimTerrain | ai-runtime ×3 (CalculIconeAction: interface, second wave), combat, ai-runtime ×2, economy ×2, core ×2, economy ×3, core | yes |
| `42d467` | NextAnimVeget (`42d44f` NextAnimVegetFullMap is network only) | core | yes |
| `42d46c` | PlayerAttaqueCalculSympa | economy | yes |
| `42d481` | TestFinDeMission(local) → byte `0x4e05a0` | missions | yes; zero exits at `0x42d4e2` |
| `42d48f`, `42d4b1`, `42d4c8` | MissionGetNum, MessageBoxSet(10, 500) (mission 6 only), PlaySnd_StopAllSound | missions, interface, audio | only after a nonzero end result; MONDE01 is mission 1, so MessageBoxSet is unreachable |

The JSON lists all 33 call sites with targets and the 15 gate instructions verified as conditional jumps in the bytes.

**PlayerGetType 0x46d817 returns AL = 2 for any index ≥ 4** (`cmp edx, 4; jge 0x46d834; mov al, 2`). The single-player loop runs cl = 0..4, so player 4 (monsters) runs `CalculNextReflect(4, 1)` → `iaCalculPlayer(4)` → `AvanceMonstre(4)` → `iaSolver(0x5148f0)` **every frame**, in addition to the declared controls 1,2,2,2 of players 0–3.

### AI players at the M1 post-load state

| Player | Type | AI context `0x51a98c + 16p` | Frame-1 path |
|---:|---:|---|---|
| 0 | 1 (human, local) | — | InputGame, InputSend |
| 1 | 2 | `00000000 01 114253 64 …` | inactive byte `+4` = 1 → `iaCalculPlayer` returns 0, no call |
| 2 | 2 | `00000000 01 114152 64 …` | inactive → return 0 |
| 3 | 2 | `00000000 01 2e4052 64 …` | inactive → return 0 |
| 4 | 2 (constant) | — | AvanceMonstre(4), then iaSolver(context 4) |

IaReset set the inactive byte because players 1–3 own no living unit in MONDE01. Only player 0 owns units and the structure. The monster table holds 5 records (u16 `0x50a9ce`), HumanOnly = 0, and the 16 group counts at `0x50b124` are 1,1,1,1,1,1,1,1,2,2,2,2,3,4,7,0. **The only AI computation MONDE01 frame 1 can reach is the monster player's `AvanceMonstre` and its rule-VM solve.** `iagUnit/Ville/Ress/WarNoyau` are not reached while players 1–3 stay inactive. Static `AvanceMonstre` callees: MissionGetNum, iaProbPost, ConstruitGroupeMonstre, iagUnitGet{First,Next}UnitInGroup, V_iaMonstreAttendLaReponse…, iaGroupDelete, SetDeplaceEngin, Random, PlayerGetType, EnginGetCase, EnginGetType, GetRandCaseChamps, Chemin_Accessible, StockeAction, GetRandCaseTypeBatPlayer.

### Unit dispatcher at the M1 post-load state

All 16 live units are owned by player 0 (human, local). The other 784 slots are state 0 and are skipped.

| State (table `0x4543c8`) | Branch | Units | Types |
|---:|---|---|---|
| 7 | `0x456966` (economy: AnimBallonStatic, Random) | 0, 1, 2, 11, 12, 13, 14, 15 | 0, 0, 0, 1, 7, 5, 5, 8 |
| 14 | `0x454ccd` (direct exit) | 3–10 | 9 |

Every live unit is counted and calls `IATestUtilite(1, i)`, which is `iagMessTestSendMessageEngin(i)` followed by a tail jump to `iabTestEngin` (a one-byte `ret`). All of them increment `0x4e1a3a` (local). Type 5 is excluded from `0x4e1928`. With u32 `0x508f7c` = 0 in frame 1, the target scan runs only for unit 0 (`(0 + i) & 0x1f` = 0, type 0, state 7). Its owner is human, so a found target uses `SetAttaqueEngin`, not message 0x49. Fatigue branch: types 0–10 and 25, which covers all 16 units. Group dword `+0x10c` is 0xffffffff for every unit. Before the first frame the counters hold `0x4e1a38`/`0x4e1a3a` = 0xffff, and `0x4e1928` is all zero.

### Structure dispatcher at the M1 post-load state

One live structure: index 0, owner 0, state 5, type 2. Its branch is `0x426918` (economy: BagContientTroupe, BagContient, CalculTroupe). It is counted in `0x4dfaa8[0]`, and `IATestUtilite(3, 0)` returns immediately. Discover/illuminate loops run for players 1–3, with flags `+0x110..0x113` = 0. With `0x508f7c` = 0 and period u16 `0x495c02` = 1000, byte `0x4dfb9b` is cleared. No structure is in state 3, so DemonteBatiment is unreachable.

### Messages

`ProcessInputGame 0x45edc0` (390 static instructions) decodes the player command queue into selection/order setters: Set*Select, Marche*, BatimentSelection, MenuInit, VendreBatiment, InitRecruteTroupe and others. It has no import and no indirect call. `MessageBoxCalcul 0x469dce` is 32 instructions with no call. Which commands reach frame 1 is a native question (step 2).

### Cross-frame and cross-front facts recorded here

- Audio: frame 1 reaches `MCICD_Play` (`0x4e2f28` = 0). Missions' frame-1 oracle needs a declared MCI binding or an audio-owned stop.
- Missions: the frame-1 input differs from the M1 post-load state at least in `0x4e2f78` (0 → 0x12 by MenuInit) and in the writes of RestoreAll, SetClipping and InitGameZone. Re-validation at the exact frame-1 input waits for Missions' capture.
- Economy: PlayerGetType's constant 2 for player 4 is part of the economy-owned player API. The committed `mercado.Mercado.tipo_jogador` already returns 2 for an index ≥ 4. The frame skeleton consumes it.

## M2 — original captures at the M1 post-load input and the first reconstruction (step 2)

### Native captures (`capturar_quadro_m2.py` → `evidencias/captura-quadro-m2-pos-carga.json`)

The script replays the original new-campaign startup and MissionLoad on Missions' committed bench (`oraculo_carga_missao.BancadaCargaMissaoOriginal`, the same declared inputs as the accepted v2 capture: fill 0xA7, clock 0x123456). It requires the resulting image to equal the frozen accepted final state `58a5020e…` (881 blocks, AL = 1 at `0x42d22d`), and that replay takes about 34 s. For each capture it restores every block, enters one original routine with the registers of its CalculGame call site, and runs every callee natively; no callee is stubbed. Each capture records:
- the SBL entry trace: callee, return site, EAX/EDX/EBX/ECX;
- the read-before-write footprint over DGROUP+.bss and the arena;
- every changed byte;
- the registers out.

Every capture carries the label **"M1 post-load input"**. The capture was committed (`66db4e4`) before any translation. A trial run in `.local/` produced identical effects.

Result: **46/46 captures return; no declared binding, display skip, undeclared import or fault is reached.**

| Capture | Original behavior at the M1 post-load input |
|---|---|
| `calcul_next_reflect_p1..p3` | `iaCalculPlayer` reads only the inactive byte `0x51a990 + 16p` (= 1) and returns 0. No call, no store |
| `calcul_next_reflect_p4` | `AvanceMonstre(4)` → `MissionGetNum`; it reads the monster tables (`0x50a9cc`, count `0x50a9ce`, five 12-byte records, `0x50ae80`, `0x50b134`) and u32 `0x508f7c`, and **stores byte `0x50a9cc` = 1**. `iaSolver(0x5148f0)` reads `0x5148f0`/`0x514904` and finds no task. EAX = 0x1a1a0001 (CalculGame ignores it) |
| `process_input_game_p0..p3` | It reads the queue pointer `[0x4e2458 + 4p]` (queues at `0x418e4000 + 0x1000p`) and the command word, which still holds the 0xA7 allocation fill. 0xA7A7 > 0x27 takes the same path as command 0 (table `0x45ed20[0]` = `0x45f2de`): it clears the 10-byte record and dispatches nothing |
| `message_box_calcul` | Reads u32 `0x507d54`; no store |
| `game_next_frame` | u32 `0x496d40`: 1 → 2 |
| `calcul_engin_next_etape` | 188 entries. 16 × (IATestUtilite → iagMessTestSendMessageEngin → PlayerGetType, then EnginNextEtape). Units 0–2 and 11–15 (state 7) reach BonusGetValEngin, GetBit, CalculFatigue (→ BonusGetValEngin), SetEnginCollision (→ SetCollision, Chemin_ModifieZone), GetBit and Random. Unit 0 also reaches PlayerGetType, EnginTrouveCible (→ PlayerEstAllie) and the frame-0 scan. Units 3–10 (state 14) reach BonusGetValEngin, GetBit, CalculFatigue and GetBit. Stores: unit `+0x10a` = state for all 16 units; `+0x74` = 1 for the state-7 units; the Random state `0x497164` advances 8 times; `0x4e1a38`/`0x4e1a3a` = 0/16; `0x4e1928[0]` = 14; the owner-0 type counters |
| `calcul_batiment_next_etape` | ResetTableauHangar (stores 0xff over 80 bytes at `0x4e296c`), IATestUtilite(3, 0), BatimentNextEtape(0) → BagContientTroupe → CalculTroupe, BatimentGetCase (→ BatimentCollision), then players 1–3: CaseEstDecouverte, BatimentEstDecouvert (false, so no BatimentDecouvre), BatimentContourEstIllumine (false; the flags are already 0, so no BatimentIllumine). Stores `0x4dfaa8[0]` = 1 |
| `ia_test_utilite_unit*`, `engin_next_etape_unit*`, `ia_test_utilite_structure0`, `batiment_next_etape_structure0` | The same per-index effects, each from a fresh M1 state |

### Reconstruction (`laco_despachantes.py`, `quadro_calcul_game.py`)

| Entry | Original | Domain and gaps |
|---|---|---|
| `calcular_proxima_etapa_unidades(memoria, provedores)` | CalculEnginNextEtape `0x456db5` | Full loop and counters. `EnginNextEtape` is a provider (eax = u16 unit, site `0x456ead`) |
| `calcular_proxima_etapa_estruturas(memoria, provedores)` | CalculBatimentNextEtape `0x4281c7` | Full loop. Providers: ResetTableauHangar, DemonteBatiment, BatimentNextEtape, BatimentGetCase, CaseEstDecouverte(cell u16, player), BatimentEstDecouvert, BatimentDecouvre, BatimentContourEstIllumine and BatimentIllumine(structure, player, ebx = 1/0). A zero period u16 `0x495c02` raises, as the original `div` faults |
| `testar_utilidade(memoria, provedores, tipo, indice)` | IATestUtilite `0x47fbfd` | Only type 1 acts. `iabTestEngin 0x4897a4` is a `ret` |
| `testar_mensagem_unidade(memoria, provedores, unidade)` | iagMessTestSendMessageEngin `0x483ed7` | Stores `+0x10a/+0x10b` on change, then returns for owner ≥ 4, a non-AI owner or no group. **The group-descriptor path (`0x483f5d` onward: table `0x498b38`, iaProbReturnTo, iagUnit/VilleSendMessage) raises `DependenciaIA` at `0x483f5d`**; MONDE01 does not reach it |
| `calcular_quadro(memoria, provedores)` and `Quadro.calcul_next_reflect` | CalculGame frame body, CalculNextReflect | See the skeleton below |

Providers receive keyword arguments at original widths plus `sitio`. A missing provider raises `DependenciaIA(name, call site)`, and every earlier store is retained.

**Frame skeleton** (`quadro_calcul_game.calcular_quadro`, commit `a2a4aad`) runs `0x42d2de..0x42d4f5` in original order: gates 2/3, the MCICD_Play track arithmetic, the player loop (0..4, or 0..3 in network games), ProcessInputGame 0..3, and the end-condition counter (signed `jl`) with the `MenuInit(local, 0x13, ecx = counter)` tail at `0x42c931`. Three bodies are inline: PlayerAttaqueReset (`ret`), GameNextFrame (`inc dword [0x496d40]`) and CalculNextReflect (Core `ia.atualizar_ia`, with the counter/inactive stores in original order). Every other callee is a named provider. The skeleton reproduces the eight Stage 1 CalculGame captures: call order, sites, argument registers, exits, stores and state/counter/flag results (`test_quadro_calcul_game.py`).

### Validation

- **Native hybrid comparison** (`validar_despachantes_m2.py` → `validacao/m2-despachantes-native.json`, clean source revision). It replays the startup and MissionLoad, restores the M1 post-load state for each case, and runs the Python code over the bench memory through `MemoriaBancada`, which keeps the declared-region policy. Every provider executes the original natively on that memory. **23/23 cases are equal to the original native capture, both in the whole image (SHA-256) and in the provider call order:** CalculEnginNextEtape, CalculBatimentNextEtape, IATestUtilite for the 16 units and the structure, and CalculNextReflect for players 1–4.
- **Local, no emulation** (`test_laco_despachantes.py`). It uses the frozen M1 blocks, with Economy's `Mercado.tipo_jogador` as PlayerGetType. IATestUtilite matches all 17 captures byte for byte. The unit loop's owned bytes (`0x4e1928..`, `0x4e1a38..`, `+0x10a/+0x10b`) and its dispatch order match the loop capture, with EnginNextEtape as a declared recording stub. Inactive players 1–3 match. Player 4 stops at `DependenciaIA('AvanceMonstre', 0x47f939)`.

### Named dependency stops for a Python frame 1 at MONDE01

In frame order, the providers that do not exist yet in Python:
1. `EvenementEnCours` (missions; one byte read) and `MCICD_Play` (audio, second wave).
2. Player 0: `InputGame`, `InputSend` (input, second wave).
3. **`AvanceMonstre` `0x47f939` and `iaSolver` `0x47f945` for player 4: ai-runtime, next.** Core's `tarefas_ia` must supply iaSolver over the actual task lists.
4. `ProcessInputGame` (ai-runtime; for MONDE01 frame 1 it is clear-only, next), `MessageBoxCalcul` (ai-runtime; read-only, next), `CalculIconeAction` (interface).
5. `ProjectileCalcul` (combat).
6. `EnginNextEtape` prelude (ai-runtime) with BonusGetValEngin (economy), EnginTrouveCible/PlayerEstAllie (combat/economy), GetBit, CalculFatigue, SetEnginCollision, Random (core), and state 7 (economy) and state 14 (direct exit).
7. ResetTableauHangar, BatimentNextEtape type 2 (economy), BatimentGetCase, CaseEstDecouverte, BatimentEstDecouvert, BatimentContourEstIllumine (core/structures).
8. RechercheCalcul … PlayerAttaqueCalculSympa (economy/core), and `TestFinDeMission` (missions).

The exact frame-1 input differs from the M1 post-load state: the load-entry tail and the earlier frame steps run first. Everything above is re-validated at Missions' first-frame capture when it is published.

## M2.1 round 2 — whole first-frame composition compared with the original

The full report is [FRAME1_COMPARISON.md](../pesquisas-paralelas/ia-runtime/FRAME1_COMPARISON.md); the data is in `validacao/m2-quadro1-composicao-ia.json`. The composition (`composicao_quadro1_ia.py`) runs Missions' `MapaMemoriaM1`/`montar_provedores` by import and calls integrated providers in original order. It is compared phase by phase with Missions' first-frame capture.

- **(a) load_tail** stops at `RestoreAll`, CALL `0x42d27f` (UI/display, no owner yet). The Python state equals the original at that entry.
- **(b) between_frames** is in **full equality**: state, both RNGs, the 8 modeled registers, the bindings and the boundaries.
- **(c) frame1** stops at `InputGame`, CALL `0x42d33b` (input; ownership to be confirmed). The state and the event prefix equal the original at that entry.

This front's reached routines were captured natively at the exact frame-0/1 entries first (`evidencias/captura-isolada-ia-quadro1.json`) and then translated in `rotinas_quadro_ia.py`: MessageBoxCalcul, ProcessInputGame (no-command path), AvanceMonstre (reached branches) and iaSolver (via Core `MaquinaTarefas` with a live-memory bridge). In the native differential, 22 of 24 isolated cases are equal. The structure loop stops at the Economy/Core per-structure providers.

## M2.1 round 3 — chained composition: frames 0 and 1 equal to the original

[FRAME1_CHAINED_COMPARISON.md](../pesquisas-paralelas/ia-runtime/FRAME1_CHAINED_COMPARISON.md); the data is in `validacao/m2-quadro1-encadeado-ia.json`.

Running on one M1 map, chained from Python and wired to every integrated Core, Economy, Combat and Missions provider, the composition equals the original at the end of each phase:
- **(a) load tail**: all blocks, RNGs, bindings and boundaries.
- **(b) window loop**: also the modeled registers.
- **(c) frame 1**.

All 81 checkpoints are equal. Declared stops crossed (state equal at entry): RestoreAll (graphics), and SetClipping, InitGameZone ×2 and NextAnimTerrain/NextAnimVeget (core, pending).

New this round, translated from captured executed blocks: InputGame (MouseZone, ScrollTerrain edge scroll, NextGouttes), InputSend, CalculIconeAction, MenuInit, the EnginNextEtape prelude and switch, and the BatimentNextEtape switch.

## M2.1 round 4 — display reference

[FRAME1_DISPLAY_COMPARISON.md](../pesquisas-paralelas/ia-runtime/FRAME1_DISPLAY_COMPARISON.md): on Missions' display scenario, the chained composition (a)→(b)→(c) equals the original in every phase and at all 96 checkpoints. The v1 regression with the same code is also equal.
- **Core providers:** SetClipping, InitGameZone and the live task VM replace the earlier crossings and the bridge. Core's NextAnim* stop on the 25×17 viewport (`0x477737`/`0x47731b`) and are crossed. They are the only logic crossings: the CRT seed and `0x4e1d18`.
- **Graphics' display routines:** RestoreAll, AffGame, and DD*/FilledBox/DeleteBank inside MenuInit are crossed and write no logic byte.
- **New translations:** the MouseZone no-zone tail, the InputGame map hover, and MenuInit's DeleteBank branch.

## M2.1 round 5 — formal first-frame equality proof

[M2_1_PROVA_QUADRO1.md](../pesquisas-paralelas/ia-runtime/M2_1_PROVA_QUADRO1.md); the data is in `validacao/m2-1-prova-quadro1.json`. Against Missions' display -v2 reference and comparison policy, the chained composition is equal in phases (a), (b) and (c) on every compared byte (16,097,242 outside the exclusion mask), both RNGs, the bindings and boundaries outside display context, the modeled registers, and the 25,482 allocation records. It uses **zero crossings**: Core's 25×17 NextAnim*, Graphics' `efeitos_logicos_exibicao`, and DeleteBank/MemFree on Missions' arena. MenuInit's display roots are not executed, and the proof shows their write sets are masked, outside the state, or restored lock bookkeeping.

## M2.2 preparation — N-frame composition

[M2_2_PREPARACAO.md](../pesquisas-paralelas/ia-runtime/M2_2_PREPARACAO.md): the M2.1 chain generalizes to load_tail plus N frames on one map, with no crossing.
- **New translations:** AffGame's HUD flag `0x4e05a2` and leftover EAX, and EnginNextEtape's 32-frame target scan.
- **Python-only probe:** it runs 128 frames. Against Core's native survey, all indicators, the checkpoint call counts and the HUD agree, once Graphics' drawing-domain guard is bypassed for planning at five view origins.
- **Blocker:** that guard is the only one, and Graphics must extend it.
- **Comparator:** it is ready for the Mac mini captures and the cumulative mask; a self-test on the frame-1 data reproduces the M2.1 proof.

## M2.3 preparation — first monster raid

[M2_3_INCURSAO.md](../pesquisas-paralelas/ia-runtime/M2_3_INCURSAO.md).

**AvanceMonstre (whole routine), ConstruitGroupeMonstre, StockeAction and the group kernels** are translated after a native capture of the forced counter-9000 raid frame. The capture records each outside call and every own write.
- The differential reproduces the call exactly: 14 outside calls with their original arguments, and every written byte.
- iaProbPost runs on Core's task VM and ProjectileInit on Combat's pool.
- The remaining stops are Core's unit-creation and path routines.

**Checkpoint start:** the N-frame chain can start from a full state after frame K (`--a-partir-de K`) for M2.3b.

## M2.2 — 128-frame equality proof

[M2_2_PROVA_128_QUADROS.md](../pesquisas-paralelas/ia-runtime/M2_2_PROVA_128_QUADROS.md). Against Missions' original 128-frame capture and the cumulative policy, the Python chain from the `-v2` MissionLoad state is equal in all 257 phases, with zero crossings:
- every compared byte (16,022,275 per phase);
- both RNGs, the bindings and boundaries outside display context, and the registers;
- the allocation records and the HUD flag.

## M2.3 — 9,200-frame equality proof

[M2_3_PROVA_9200_QUADROS.md](../pesquisas-paralelas/ia-runtime/M2_3_PROVA_9200_QUADROS.md). Against Missions' original 9,200-frame capture (10 self-contained parts) and the cumulative 9,200-frame policy, the Python composition is equal in all 18,401 phases. The window runs through the first raid: the spawn at frame 9000 and the first path search at 9176–9179. It uses zero crossings, measured per part:
- every compared byte (16,022,275 per phase);
- both RNGs, the bindings and boundaries outside display context, and the registers;
- the allocation-record count in every phase, part 09's final records, and the HUD flag.

One command reproduces it (`provar_quadros_9200_ia.py tudo`), with a per-part mode so the parts run in parallel.

## M3.1 groundwork — the input path (InputGame → SetPlayerOrdre → ProcessInputGame → setters)

Original first: `capturar_entrada_ordens_ia.py` → `evidencias/captura-entrada-ordens-ia.json` (commit `887b6c7`, before any translation). It runs 124 native leaf calls at Core's accepted frame-1 ProcessInputGame pause (`bancada_selecao_ordens`). Each case declares its cursor, WndProc flags `0x5099ae..b2`, view, help page, action mode, drag state, selection, packet and GetAsyncKeyState answers. All 124 cases return, and the load_tail/between_frames/frame1 summaries and the code section reproduce. InitInputPlayer's allocations are rolled back on the bench arena after its case.

**Translation** (`entrada_ordens_ia.py`, class `Entrada(m, Provedores)`):
- InputGame 0x429278. Translated:
  - the key block (arrows through ScrollTerrain, space);
  - the zone selection, MouseZone and the right-button deselection;
  - zone 0: the cell mapping 0x429800..0x42984a, the margins and the undiscovered-cell rule 0x4298d9 (troops selected and page 0 give tag 5);
  - the information block (sack, field, mine, trap, structure and unit under the cursor);
  - page 3, construction placement through BatimentPosable (tag 4), and page 1 (tag 5);
  - drag start, the selection box and its release (tag 1; with no troops, the own structure, tag 2);
  - own-unit hover and double click (tag 9), enemy-unit attack (tag 14), own-structure hover;
  - terrain presses: field (tag 7 or 0x12), mine (tag 6 or 0x12), move (tag 5);
  - the edges, the minimap (recentre through MiniMapGetCenterSelect, or tag 5 through MiniMapGetCase), and the HUD action icons (IconeGetZone, the single unit's order Bag, BagGetCode codes 2, 3 and 7). Code 3 is the CAVE icon: TestRessource, then page 3 and `0x496207` = type.

  Every other branch is a named stop at its original address.
- SetPlayerOrdre 0x45ecd4.
- ProcessInputGame 0x45edc0: all 40 table targets of 0x45ed20, with the original argument registers, then the slot cleanup 0x45f2de.
- CalculIconeAction 0x45e944 with IconeFillContenu 0x45dbd0 for a single selected unit.
- WndProc mouse messages 0x200..0x205.
- Leaves: MouseEstDeplacer, KeyPressed, KeyUnPressed, KeyTestRelease, IconeGetZone, BagGetCode, BagGetType, EnginGetBagOrdre, GrabAllInput, InitInputPlayer with MemAlloc's counter `0x4e2f3c` (GlobalAlloc/GlobalLock are bindings), MiniMapGetCase, MiniMapGetCenterSelect, MiniMapSetLock.

**Owners consumed by import** (`provedores_entrada_ia.provedores_vivos`, never defaulted):
- Core `selecao_ordens.SelecaoOrdens`: selection and Set*Select, EnginAsk with the sound boundary. Its SetAttaqueEngin goes through Combat's `ataque_vivo.definir_ataque`.
- Core `construcao_core.ConstrucaoCore`: BatimentPosable, when importable.
- Core `chamadas_quadro_core.iniciar_zonas_jogo`.
- Economy `ordens_economia.OrdensEconomia`: EnginTravailSelectionne, TestRessource, SetMine/SetDepot/SetRamasseEnginSelect.
- Economy `extracao.RecursosTerreno`: MineGetIndice/MineGetCapacite.
- Combat `alvos_alcance.ocupa_celula`: EnginOccupeCase.
- This front's `proximas_gotas`: NextGouttes.

**Native differential** (`validar_entrada_ordens_ia.py`; report [validacao/entrada-ordens-native.json](../pesquisas-paralelas/ia-runtime/validacao/entrada-ordens-native.json)):
- 124 comparisons: **113 equal, 0 mismatches, 11 named-dependency stops**.
- Compared per case: registers EAX..EBP, the whole changed state (18,335 changed bytes), the sound requests and the key answers.
- Excluded registers: InputGame's EAX and the single-unit CalculIconeAction's EAX. They are leftovers that CalculGame discards (0x42d340 reloads EAX; 0x42d3f0 does not read it).
- The run used Core's `construcao_core` from `origin/feat/re-core` `63200b5` (read-only extraction, `--nucleo-ref`; its SHA-256 is in the report), because it is not on main yet.
- The named stops:
  - BatimentInitAttaqueSelect, InitRecruteTroupe and SetDechargeCaveEnginSelect (no owner translation yet);
  - CalculIconeAction with a structure selected;
  - MiniMapSetPos (MiniMapRecentre);
  - TextGetMessage with the text-table pointer `0x5099a4` = 0. In the MONDE01 display bench no text file is loaded, so the original reads unmapped low memory. This is a gap, not a guessed 0.

The CPU-free replay (`testes/test_entrada_ordens_ia.py`) reruns every case from `evidencias/leituras-entrada-ordens-ia.json.xz`.

**Declared-input API** (`composicao_entrada_ia.py`):
- `RoteiroEntrada(dados)` reads a `rising-lands/monde01-scripted-input/1` file:
  - the cursor is held from frame to frame;
  - the messages are queued per frame;
  - keys are answered by vkey, 0 when absent;
  - every consumed answer is logged in the harness's `entradas.jsonl` fields.
- `ComposicaoEntrada(estado, captura_quadro, entrada, captura_m1, roteiro, inicio=128, alocacoes, regs_inicio)` extends the pinned `ComposicaoQuadros` without modifying it:
  - `between_frames{k}` runs the `_WinMain@16` loop. Each message gets PeekMessageA = 1, GetMessageA, TranslateMessage = 0 and DispatchMessageA→WndProc, and then the PlaySnd_Manage/MCICD_Manage boundaries with the MSG words. AffGame's order-marker block 0x417b8f..0x417c3c (the `0x4e05ac`/`0x496204` stores) is added.
  - `frame{k}` uses this front's InputGame, ProcessInputGame and CalculIconeAction.
  - `executar(n)` yields per phase `phase, registro, entry, exit, ordens, eventos`.

**Chain check against the Mac mini probes** (`provar_entrada_ia.py`). It runs Python only, from the accepted M2.2 frame-128 full state, on Missions' probes at `f058844`, which are read with `git show` and never merged. Compared per frame:
- the consumed inputs;
- the SetPlayerOrdre/ProcessInputGame events;
- counter, game frame, both RNGs, the CRT seed and `0x4e1d18`;
- view, selection head and objective block;
- the whole 276-byte records of units 11..15.

| Probe | Frames equal | Orders | End |
|---|---|---|---|
| P1 | 501 (129–629) | tag 1 (4113, 4113) at 133 | end of probe |
| P2 | 601 (129–729) | tag 1 at 133, tag 5 (3347) at 143; the unit walks | end of probe |
| P3 | 24 (129–152) | tag 1 at 133; CAVE mode at 143; tag 4 (3, 3093) and its ProcessInputGame jump at 153, equal | stop at 153: EnginNextEtape state 11 (this front's next slice; Economy's CalculConstruireBatiment is ready) |
| K1 | 11 (129–139) | — | stop at 139: WndProc WM_KEYDOWN 0x100 (keys are coverage only) |

This is an indicator-level check. The per-phase whole-state proof under the published mask needs the probes' pass-2 delta captures (M3_PLAN §2), which do not exist yet.

## M3.1 round 2 — state 11 (builder), construction progress, structure entry dispatch, keys

Original first: `capturar_construcao_teclas_ia.py` → `evidencias/captura-construcao-teclas-ia.json` (commit `51a7f46`, before any translation). It runs 90 native leaf calls at the same frame-1 ProcessInputGame pause as round 1 (`casos_construcao_teclas_ia`). All 90 return, and the load_tail/between_frames/frame1 summaries and the code section reproduce. The builder cases start from the committed native result of `process_tag4_build_cave` (P3's cave order at 3093) and a declared structure record 1 (a cave under construction at P3's origin 2579); the type limits are read at the pause (type 3: 100, type 9: 15, type 0x11: 300).

**Translation** (`construcao_entrada_ia.py`, class `ConstrucaoEntrada`; owners wired by `provedores_entrada_ia.construcao_viva`):
- EnginNextEtape state 11 `0x4564ef`: with `+0x89` set and BatimentEnDestruction(`+0xc0`), SetDeplaceEngin(unit, `+0x7e`) (Core); otherwise CalculConstruireBatiment; both end at the epilogue `0x454ccd`. `proxima_etapa_entrada` runs the pinned prelude and switch (`proxima_etapa_quadro`, unchanged) and continues at the state's target, where the pinned switch stops before the body's first store. State 13 `0x4558e4` (Core's physical entry) goes to a provider `EnginNextEtape:state13` when bound; none exists yet.
- CalculConstruireBatiment `0x44ab60` is Economy's `ordens_economia` (walk, creation, abandonment) with Core's `selecao_ordens` and `construcao_core` callees (`provedor_core(..., provedor_construcao(...))`). Its out-of-domain stop at `0x44b1c1` (`+0x89 = 1`, no store made) continues in `progresso`: RotateEngin when the facing differs; AnimConstruireBatiment; the completion block `0x44b34a` when BatimentConstruit holds with no damage (wall queue `+0xd8` for order type 9, else the finish sound 0x50/0x12, `+0xbe = 0xff`, state 7, `+0x7e = +0x7c`, path-search release); otherwise the countdown `+0x8b` and, at 0 with animation frame `+0xa4 = 2`, the dust projectile (CalculDirCase, Random, ProjectileInit 0xf/0x10), BatimentRepare or BatimentConstruction, `+0x8b = 0x14` and the work sound 0x50/0x25 for the local player's builder on a discovered cell.
- Leaves: BatimentEnDestruction `0x41a70b`, BatimentConstruit `0x41c652`, BatimentGetDegatEffectif `0x41a976`, BatimentRepare `0x41cec4`, BatimentConstruction `0x41cf59` (at the type limit: `+5 = 5`, then BatimentModifyMap(structure, 1) through Core's `minimapa_estruturas` over the live world), AnimConstruireBatiment `0x447e12`.
- Input (`entrada_ordens_ia.py`): WndProc WM_KEYDOWN (digits 1–9 → `0x49a05a`, F1–F4 → `0x497284`; VK_ADD/VK_SUBTRACT zoom and F11 are named stops past their gates) and WM_KEYUP (F5 → ReseauActif and `0x49a05b` mod 4; Tab → `0x497285` and Core's InitGameZone); InputGame's group-number path `0x4293e0` (Ctrl: tag 0xb; else tag 0xc; Shift: EnginGetCentreGroupe, then the view clamp); GoLastAttaque `0x440b63` on Enter/X; ProcessInputGame tags 0xb (SauveSelectionGroupe), 0xc (BatimentDeselectionner, DeSelectionGroupe, RestaureSelectionGroupe), 0x10 sub 1/3 (SetEnginSelectRentreEngin/Batiment) and 0x21 (BatimentRetireColon).

**Native differential** (`validar_construcao_teclas_ia.py`, run with Core's `construcao_core` from `origin/main` `2ad381a` as a read-only extraction, SHA-256 in the report): see [validacao/construcao-teclas-native.json](../pesquisas-paralelas/ia-runtime/validacao/construcao-teclas-native.json). The CPU-free replay is `testes/test_construcao_teclas_ia.py` (`evidencias/leituras-construcao-teclas-ia.json.xz`). Round 1's differential was rerun after the `entrada_ordens_ia` changes ([validacao/entrada-ordens-native.json](../pesquisas-paralelas/ia-runtime/validacao/entrada-ordens-native.json)).

Excluded registers (a value left by a callee that is not reconstructed): EnginNextEtape's EAX (its only caller discards it at `0x456eb3`), InputGame's EAX (as in round 1), CalculConstruireBatiment's EAX after RotateEngin, and BatimentConstruction's EAX after BatimentModifyMap.

**Named dependencies** (stops at their original call):
- Core: the state-13 body (`CalculEntreBatiment`), SauveSelectionGroupe, RestaureSelectionGroupe, SetEnginSelectRentreBatiment/Engin, EnginGetCentreGroupe, MiniMapRecentre (VK_SUBTRACT), `BatimentIllumine`/`BatimentDecouvre`.
- Economy: the type-3 structure body `0x426aff` (cave: BagContient colonist test, smoke counter `+0x76`), BatimentRetireColon, BatimentHabitable (type 0x11 completion); SetMurAllentour (type 9 completion).
- Text: TextGetMessage. In the display scenario InitTextLangue never runs (TEXTES.TXT needs CRT fgets/ftell), so `[0x5099a4]` is 0. The chain binds it as Missions' declared boundary (`oraculo_exibicao_missao.FRONTEIRAS_EXIBICAO`: EAX 0, no cleanup), logged per call site. The leaf bench keeps the pointer-0 read as a named gap.
- Graphics: AffGame's vegetation/terrain handlers for view origins outside `efeitos_logicos_exibicao.ORIGENS_PROVADAS` (raised as `DependenciaExibicao`).
- Not yet translated here: InputGame's help pages 2/7/9/0xb/0xc and the Ctrl deposit mode (pages 8/9, tags 8 and 19 producers, `0x429601`, `0x429b90..0x429f46`), the structure-under-cursor path with troops selected (`0x42ac32`, the tag-16 producer).

**Chain check** (`provar_entrada_ia.py`, Python only, from the M2.2 frame-128 state; probes read from `origin/feat/re-missions` with `git show`):

| Probe | Frames equal | Orders | End |
|---|---|---|---|
| P1 | 501 (129–629) | tag 1 at 133 | end of probe |
| P2 | 601 (129–729) | tag 1 at 133, tag 5 at 143 | end of probe |
| P3 | 91 (129–219) | tag 4 (3, 3093) at 153; the builder walks (state 11, Economy's CalculConstruireBatiment through Core's DeplaceEngin) and creates structure 1 at 220 (CreerBatiment, PlaceBatiment) | stop in frame 220: BatimentNextEtape type 3 `0x426aff` (Economy's cave body); BatimentIllumine (Core) follows in the same frame |
| P4 | 293 (129–421) | tag 5 at 141–143 | stop in between_frames422: Graphics, AffGame view origin (10, 16) not proved |
| P5 | 443 (129–571) | tag 5 at 141–143 | stop in between_frames572: Graphics, view origin (31, 0) |
| P6 | 91 (129–219) | as P3 | stop in frame 220, as P3 |
| P7 | 91 (129–219) | as P3 | stop in frame 220, as P3 |
| K1 | 12 (129–140) | — (the arrows scroll the view in frame 140, equal) | stop in between_frames141: Graphics, view origin (1, 0) |

Probes at `origin/feat/re-missions` `b1cd5bd` (P7 from `01fa7d8`). The TextGetMessage binding is not exercised yet: P4's first call (frame 430) lies past its Graphics stop. The frame-phase count is reported per frame against the probe's entry count, which also counts display-phase calls.

The state-11 walk, the creation at 220 and the WndProc/key paths are now checked at indicator level against the probes. The construction-progress branch, the completion and the state-13/tag-16/tag-33 dispatches are checked by the native leaf differential only, because every probe stops at frame 220.


## M3.1 round 3 — Ctrl deposit mode, help pages 9/0xc/0xb/2/7, structure under the cursor with troops

**Original first.** `capturar_paginas_deposito_ia.py` → `evidencias/captura-paginas-deposito-ia.json` (commit `c4ff87d`, before any translation). It holds 203 native leaf calls at the frame-1 ProcessInputGame pause (`casos_paginas_deposito_ia`), all returned, with the path and code reproduced. Declared structure 1 is placed under the cursor at cell (19, 14) through its record and its structure-grid word `[0x4e0f38]`. The type limits, grid pointers and player table `[0x5080a8]` are read at the pause.

**Translation** (`entrada_ordens_ia.py`):
- **Ctrl `0x429601`.** Page 8 is set when every live selected unit can carry (EnginSelectPeuventTransporter: types 5/6/7/0xd). Page 9 is kept only while that holds.
- **Page 9 `0x429b90`.** The target is a depot (types 3/4) the selection may use (EnginSelectPeutDeposer) and the player owns, or no structure.
  - The click sends table `0x42923c[u16 0x4e05b0]` → tags 6/7/8/0x13. BX = u16 `0x4e05b2`. With a structure, CX = 2 and the structure is word 6; without one, CX = 1 and the cell is word 6. Word 8 = byte `0x4e05b4`.
  - The click then sets page 0, `0x496204` and `0x4e05ac`.
- **Page 0xc `0x429daa`** (Shift): a selectable unit (Core's EnginSelectionnable); AF sends tag 0x24.
- **Page 0xb `0x429e31`.** A type-8 selection; a type-3 structure for mode ≠ 3, or a type-7 structure for mode 3 (byte `0x496209`); tag 0x22. A cell with no structure is a named stop at `0x429ea2`: BatimentGetType(0xffff) reads outside the pool, and the native run faults there.
- **Page 2 `0x42a4a2`** (Alt). The object under the cursor is [ebp-0xc] = 1/3/5 with ECX = the unit, the structure or the cell.
  - A selected structure asks Combat's BatimentPeutAttaquer (named dependency).
  - Troops ask EnginSelectPeutAttaquer, or target a type-10 unit regardless.
  - The click sends tag 0xe and page 0.
- **Page 7 `0x42a600`** (Delete): ChercheIndiceBatiment; an own structure that BatimentPeutSeVendre allows; tag 0xa, then BatimentDeselectionner.
- **Page 8 over a field or mine** (`0x42b393`/`0x42b525`): the click sets page 9 with index 1/2 (field) or 0/2 (mine), the cell and cargo 1/2.
- **`0x42ac32`** (troops selected, structure under the cursor):
  - Page 8 over an own cave with carriers: deposit index 3, cargo 2 (builders) / 1 (colonists) / 0. Otherwise a move (tag 5).
  - A foreign structure that is not neutral: type 0x10/2 with type-10 units → tag 0x10 (BX 3); otherwise EnginSelectPeutAttaquer(mode 3) → tag 0xe.
  - The first selected unit is a builder on an unbuilt or damaged structure → tag 0x14.
  - Wounded troops at a built type-0x13 structure, or wounded engins at a type-0xe one, without mirrors → tag 0x15.
  - Core's EnginSelectPeutEntrer(mode 3) without mirrors: built → tag 0x10 (BX 3), unbuilt → tag 5. Otherwise the own-structure drag start.
- **Leaves:**
  - EnginSelectPeutAttaquer `0x472355`, complete: TypeEnginEstArmee, TypeEnginPeutAttaquer, TypeEnginLargueBombe/EnginGetNbBombe. TypeEnginEstArmee is corrected for types 0x11 (false) and 0x12/0x13 (true).
  - EnginSelectEstTroupe, EstEngin, ContientMiroir, PeuventTransporter, EstBlesse and PeutDeposer.
  - BatimentEstDepot, EstNeutre, EstEnnemi and PeutSeVendre; PlayerEstAllie; ChercheIndiceBatiment.
  - Every leaf returns EAX..EBP as the original leaves them (e.g. BatimentEstEnnemi's EDX, EnginSelectPeutAttaquer's EBX/EDX).

**Native differential:** `validar_paginas_deposito_ia.py --nucleo-ref <dir with Core's entrada_estruturas.py from feat/re-core 90fd831>` → [validacao/paginas-deposito-native.json](../pesquisas-paralelas/ia-runtime/validacao/paginas-deposito-native.json).
- Result: 203 cases, 201 equal, **0 mismatches**, 2 named stops (Combat's BatimentPeutAttaquer).
- TextGetMessage is the bench's display boundary (EAX 0, never executed). The differential binds it as the chain does and compares its message number.
- CPU-free replay: `testes/test_paginas_deposito_ia.py`.
- The round-1 and round-2 differentials were rerun after these changes: 0 mismatches.

**Next:** the whole-state proof over the P1/P2 pass-2 windows, then P6, and the Core vision/groups and structure-entry wiring (see the HANDOFF).

## M3.1 continuation — integrated baseline and provider regressions (2026-10-30)

The later M3.1 wiring, hunger path, accepted P1/P2 proof and current dependency sequence are recorded in the latest [AI/runtime handoff](../pesquisas-paralelas/ia-runtime/HANDOFF.md). Fresh native regressions on main `e70fda3` compare 417 cases: **405 equal, 12 explicit dependency stops, zero mismatches**. Input orders are 117/124 equal, deposit pages 203/203, and construction/keys 85/90; the reports under `validacao/` retain each stop and current source provenance. All native load/frame/code reproductions pass. The leased AI/runtime gate passes 120 tests with eight explicit native skips.

This continuation changed validation records only; APIs, supported domains and ordered effects were unchanged. At the time Core `5422338` and Graphics' CAVE/construction-projectile guards were not yet on main; both have since landed (main `71335aa`), so only Missions' S1 pass-2 window is still awaited. See "Current state" for the follow-up.


## S1 recruit owner binding (2026-10-30)

`DonosM3` constructs Core's `RecrutamentoCore` on its live memory and routes
`EnginSetType`, `EnginAddVie`, `EnginResetFatigue`, `EnginSetExperimente` and
`SetSortEngin` through `provedor_recrutamento`. The supplied live bonus callback
is reused; when absent, `bonus_recrutamento(memory)` is resolved on the first
query against Economy's live tables. No bonus value is invented. The caller's
partial register file, `_incertos` and pushed-word metadata reach Core unchanged;
the adapter returns all seven data registers and explicit preserved unknown bits.
`ArgumentoNaoPassado` propagates before that callee reads or writes memory,
retaining all earlier producer effects.

The behavior inputs are AX unit, DX cell, BL direction, CL type for
`EnginSetType` (CALL `0x420f69`); AX/DX increment for `EnginAddVie` (`0x420f75`);
AX for fatigue reset (`0x420f7c`); AX/DX preserved exit cell for experience
(`0x420f85`); AX/DX exit cell for placement (`0x420f8c`). Core's original entries,
supported domains and exact mutations remain its
[recruitment adapter contract](core/RECRUITMENT_ADAPTERS.md).

Economy's BL update is consumed directly. Its current `SetSortEngin` callback
still supplies only AX, so DX is an explicit Economy ABI dependency. AI/runtime
does not recover it from a previous callback or synthesize it. The S1 indicator
driver reports the missing register, caller, native entry, owner and required
masks as a structured stop. The six-case native prefix validator now runs
through conversion, healing, fatigue and experience, stopping before placement
if DX is missing; its original store sequence, callback arguments and every
non-stack changed byte must agree. No recruit-completion claim follows from
that bounded comparison.


`mensagem_cidade_ia.mensagem_cidade(memory, regs, chamada=0x4211e5)` is the
city-message provider bound directly in `DonosM3.externo`. Required inputs are
AX structure, DL message and full EBX argument; missing/uncertain consumed
bits raise `ArgumentoNaoPassado` before memory access. Structure indices are
protected to 0..999. It reads BatimentGetPlayer's owner byte and, for owners
0..3, imports Economy's live `quadro_economia.tipo_jogador` query. Owners
>=4 return their owner byte; player types other than 2 return their type byte.
EAX is that result, EBX the zero-extended structure, EDX the original full EBX.
ECX/ESI/EDI/EBP are preserved with their explicit unknown masks; optional
entry ESP returns ESP+4. There are no non-stack stores or external effects
on these branches. An AI player raises a named `DependenciaIA` at `0x48484c`,
before its unbound message dispatch, naming owner/message/argument.

Original-first evidence was committed before translation: the corrected
`evidencias/mensagem-cidade-original-v2.json.xz` supersedes v1's incomplete
read hooks; neither evidence file is replaced. Native differential
`validacao/mensagem-cidade-native.json`: **27 cases, zero mismatches**,
23 exact returns and four explicit AI-prefix stops. It freshly replays the
three Economy calls and the S1 frame-2547 call, verifies the 48 native S1
states, reproduces the capture, compares all seven registers (plus S1 ESP),
and rejects Python stores. CPU-free tests replay the same native reads and
verify omitted/uncertain arguments.

Recruitment binding differential `validacao/producao-entrada-recrutamento-native.json`:
**6/6 equal bounded prefixes**, three returning below threshold and three
stopping before placement on Economy's missing DX. Every provided owner
argument, all changed non-stack bytes and the original native store sequence
agree, including actual BL direction. These checks do not establish a complete
S1 producer or a whole-state input-chain proof.


Final S1 continuation validation: strict and planning indicators both compare
2,418 equal frames (129–2546), then report Economy's missing DX at SetSortEngin
in frame 2547; planning bypass count is zero. The three native regressions
compare 417 cases (406 complete, 11 named stops), zero mismatches. Combined
with six recruitment prefixes and 27 city cases, the bounded differentials
have 450 cases, 18 named boundaries and zero mismatches. Final leased domain
gate: 129 tests, eight explicit native skips, zero failures/errors, documentation
links passed. See [the continuation report](../pesquisas-paralelas/ia-runtime/S1_RECRUIT_CONTINUATION.md)
for the exact Economy request and reproduction commands.
