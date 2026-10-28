# AI and runtime handoff

Owner: AI and Runtime front. Branch `feat/re-ai-runtime`, worktree `worktrees/re-ai-runtime`. Owned paths: `pesquisas-paralelas/ia-runtime/` and `docs/AI_RUNTIME.md`. The contract itself is [docs/AI_RUNTIME.md](../../docs/AI_RUNTIME.md); this file records status, counts, agreements and requested contracts.

## Stage 1 — contract (original-byte inventory, captures, ownership)

**Gap closed:** every "to be inventoried" item of the skeleton now has original-byte evidence:
- the `0x47500e` cycle;
- `CalculGame 0x42c868` call order with gates `0x42d14c`, `0x42d2e3` and `0x42d3c0`, and `GameNextFrame`;
- the `EnginNextEtape 0x45442c` state table (reached from `CalculEnginNextEtape 0x456db5`) and the routines each state reaches, including MONDE01's states 0, 7 and 14;
- the `BatimentNextEtape 0x4268d4` type table (reached from `CalculBatimentNextEtape 0x4281c7`);
- the `iaCalculPlayer 0x47f927` callbacks;
- the AI tables touched by `IaAlloc`/`iaInit`/`IaReset` and the initializers;
- the 140 operation names by address and provider family;
- both message routines.

No behavior is implemented in this stage.

Identities: intact executable `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb` (execution and every interval); normalized analysis PE `26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0` (not used). Base: main `8a499a9`.

### Files

| Path | Role |
|---|---|
| `ambiente_ia_runtime.py` | Paths and identities (bootstrap; adds `ferramentas` and the read-only Python inputs) |
| `inventario_ia_runtime.py` | `OriginalImage`: section-mapped intact image, SBL names via core `simbolos_ia`, static walker (jump tables bounded by their `cmp`/`ja`, shared Watcom tails, tail calls, import thunks), global-operand inventory, `ret N` stack cleanup |
| `extrair_contrato_ia.py` | Writes `evidencias/manifesto.json`, `inventario.json` and the 35 `.asm` listings (no emulation) |
| `captura_chamadas_ia.py` | `CallCapture` on core's `BancadaX86`: declared callee stops, Watcom `ret N` cleanup, IAT-slot thunks for Win32 imports, store trace |
| `capturar_contrato_ia.py` | The 57 declared scenarios → `evidencias/capturas-originais.json` |
| `testes/test_evidencias_contrato.py`, `testes/test_capturas_contrato.py`, `testes/test_namespace.py` | Local checks, core consistency, and the native replay (requires `RISING_EMULAR=1`) |

Core inputs consumed without modification, with their hashes recorded in `evidencias/manifesto.json`: `ferramentas/ia.py`, `tarefas_ia.py`, `simbolos_ia.py`, `ordens_unidades.py`, `mensagens_chegada.py`, `cadencia.py`, `emulador.py`, `analisar.py`, `relatorios/regras-ia.json`, `relatorios/simbolos-originais.tsv`, and `relatorios/missao01-unidades.json` (the MONDE01 owner/type/state bytes used by one fixture).

### Counts

- Exported intervals: 171, all SHA-256-checked against the intact bytes. They are 35 routines with 9 shared tails, plus 136 operation bodies, plus 9 data tables.
- Static inventory: 25 unit states, 21 structure types, 12 unit messages, 4 city messages, 12 behavior records, and 140 operation names at 136 addresses (none unresolved).
- Original-only captures: 57 scenarios, 4,054 declared stops, 4,111 bench segments, 0 faults. All scenarios return to the bench's return address; there are no unexpected stops and no instruction-limit hits.
- Local run (`python3 -B -m unittest discover -s pesquisas-paralelas/ia-runtime/testes`): 25 tests discovered, 24 passed, 1 explicit skip (native replay, `RISING_EMULAR` unset).
- Native run (`RISING_EMULAR=1`): 25 tests, 25 passed, 0 skipped. The fresh replay of the 57 scenarios equals the committed captures as a whole document.

### Key findings

- **First frame and the M1 snapshot point.** `CalculGame` state 0 runs `MissionLoad` and then falls through into the first frame in the same call. The M1 snapshot point is `MissionLoad`'s return to `0x42d22d`.
- **AI sees counters one frame late.** AI players run in `CalculGame`'s player loop (via `CalculNextReflect 0x47fbea`) before the unit/structure dispatchers rebuild the counters `0x4e1928`/`0x4dfaa8`.
- **Real per-state dispatcher.** `CalculEnginNextEtape` is only the loop and its counters; the per-state dispatcher is `EnginNextEtape 0x45442c`. MONDE01 state 14 has no branch body (prelude only). State 7 reaches `AnimBallonStatic`/`Random`. State 0 is never dispatched.
- **Routines with no caller or pointer anywhere in the image:** `CalculEnginStatic 0x453062`, `iaInit 0x47f328` and `IAResetAttaque 0x47c162`.
- **Program-start AI state.** It is `IaAlloc 0x47fb15` (`ProgInit`). The RNG seed `0x498db4` comes from `timeGetTime`, so M1/M2 oracles need a clock binding.
- **IaReset research thresholds persist across missions.** IaReset rebuilds them only when bytes `+5..+8` of the player context are all zero.
- **Core's `ia.atualizar_ia` is confirmed.** It reproduces the six iaCalculPlayer captures exactly.

### Ownership agreement

| Front | Status | Recorded where |
|---|---|---|
| Core | **Confirmed** (message of 2026-10-28). Clarifications: sound, the bonus query (`BonusGetValEngin`, economy), targeting (`EnginTrouveCible`/`SetAttaqueEngin`, combat) and `CreerSac` (economy) stay with their owners as named dependencies; ai-runtime sequences the 32-frame scan, spell timer and fatigue branches; `CalculFatigue`/`EnginSetFatigue` are core. Planned core entries for the state bodies are `executar_estado_movimento` (2), `executar_estado_rotacao` (3), `executar_estado_retirada` (4) and `executar_estado_saco` (16/17), each `(mundo, indice)` returning None. They are not scheduled yet; the coordinator must schedule them. The declared-binding facility is core Stage 15. In a second message core also accepted unit state 13 (physical entry body; economy queries and message 0x47 as named dependencies) and `DemonteBatiment 0x41effd` (physical removal; economy refund query). Neither is scheduled yet | `docs/core/HANDOFF.md`, core Stage 14 commit |
| Economy | **Confirmed** (message of 2026-10-28). The call shape is eax = zero-extended u16 index, return ignored. Unit states 5 (`ciclo_trabalho.calcular_trabalho_unidade`, provisional), 7, 11, 15, 18 (`ciclo_transporte.calcular_transporte_unidade`, provisional), 19, 20, 21 (economic body; physical lodging is core) and 23. Structure types 1–8 and 13–20 (`producao_limpa.calcular_tropa_com_limpeza_no_mundo` committed for types 1/2/13/16, plus 6 via `aprendizagem.Aprendizagem.calcular_biblioteca`). Frame calls `RechercheCalcul`, `PlayerInitAllianceCompteur`, `PlayerAttaqueCalculSympa`, `SetUpdateChamp` (`extracao.RecursosTerreno.agendar_campos`), `UpdateChamp` (`atualizar_campos`), `CalculMatiere`, `CalculCompteurMarche`, `CalculCompteurProposition`. `BagContientTroupe` is `0x44724a`. `DemonteBatiment` as core physical removal with an economy refund query (core accepted) | economy `HANDOFF.md`, Stage 15 commit |
| Missions | **Confirmed** (messages of 2026-10-28). Missions keeps the `MissionLoad`/`MissionLoadName` composition and calls `reiniciar_ia` at `0x46c5cc`/`0x46c98e` without the unused AL. It keeps the event bodies, `TestFinDeMission 0x458606`, `MissionGetNum` and the attack/monster tables. The oracle inherits IaAlloc as declared input, and the M1 snapshot is at `0x42d22d`. The reset prefix has no AI call and stores 0xffff in `0x4e1a38`/`0x4e1a3a`. Missions' monster-table API is `carregador_cadeia_auxiliar.carregar_entrada_monstros_missao(leitor, monstros1220@0x50a9bc, grupos432@0x50af84, aleatorio4@0x497164, *, tipos_grupo8, perfil)` | `pesquisas-paralelas/missoes/HANDOFF.md`, Stage 9 (main `bb8c6d0`) |
| Combat | **Confirmed** (messages of 2026-10-28). Combat owns the whole state-1/24 branch body `0x456886`..exit through one entry (provisional `ataque_vivo.ramo_estado_ataque(contexto, indice)`, u16 unit, no return). `+0xb7` is the target mode (1 unit, 3 structure, 5 cell), not a substate; the inline blocks are validity checks. Combat also owns `EnginTrouveCible` (`alvos_alcance.encontrar_alvo`), `SetAttaqueEngin(eax=unit, dl=mode, bx=ref)` (Stage 18 `ataque_vivo.definir_ataque`), and `ProjectileCalcul` (`maquina_projeteis.MaquinaProjeteis(...).calcular(low byte of u32 0x508f7c at 0x42d3f0)`). Turret types 10/11 and state 22 are accepted in principle but not yet scheduled. Combat identified the prelude step `0x454530..0x454591` as the reload advance | combat `HANDOFF.md`, Stage 18 commit |

### Requested contracts (provider, original address, consumed widths)

- **Core.**
  - State bodies 2/3/4/16/17 with the u16 unit index (`0x4563da`, `0x455a61`, `0x456ae5`, `0x455e32`).
  - Prelude primitives `SetDeplaceEngin 0x4457d3(eax=u16 unit, edx=u16 cell)`, `SetDyingEngin 0x444938(eax=u16)`, `RetireEngin 0x457058(eax=u16)`, `CalculFatigue 0x452cc8(eax=u16)`, `EnginSetFatigue 0x453b84(eax=u16)`, `GetBit 0x467d97(al=byte, edx=bit)`.
  - Discovery `BatimentDecouvre(eax=u16 structure, edx=player)`, `BatimentIllumine(eax=u16, edx=player, ebx=0/1)` and the gate branch body `0x427bb7`.
  - The declared-binding facility (Stage 15) for the frame oracle.
  - Unit state 13 body (`0x4558e4`: `CalculEntreBatiment`/`CalculEntreEngin`) and `DemonteBatiment 0x41effd(eax=u16 structure)`. Both accepted; the coordinator schedules them.
- **Economy.** The bodies above, each `(eax=u16 index)`. Queries `BonusGetValEngin 0x428cc0(al=owner, edx=3)`, `PlayerGetType 0x46d817(al=player)` (reads byte +1 of the 20-byte records at `[0x5080a8]`; players ≥ 4 return 2), `GetRessource 0x467670` (four u16 output pointers plus a pushed player, `ret 4`), `RechercheGetNiveau 0x4717c2(al=player, dx=branch)`, `RechercheSetBranche 0x470b37(al=player, dl=branch)`.
- **Combat.** The state-1/24 branch entry (u16 unit), `EnginTrouveCible 0x453f74(eax=u16 unit) → ax target or 0xffff`, `SetAttaqueEngin 0x445a36(eax=u16 unit, dl=mode, bx=ref)`, `ProjectileCalcul 0x46fc0f()`, turret branches `0x426e43`/`0x427549`, `CalculPiege` (state 22).
- **Missions.**
  - Owners of the ghost-table queries used by four placement operations: `GetCaseOfGhost`, `GetCaseCentraleOfGhost`, `GetNumIndiceTypeGhost(FullFree)`, `OccupationIndiceGhost`, `ImplantePlayerInGhost`, `LiberePlayerInGhost`.
  - `MissionGetNum 0x46c11a` (returns u16), `EvenementEnCours 0x4581b6` (AL), `TestFinDeMission 0x458606(al=local)` (AL stored in `0x4e05a0`).
  - The monster tables consumed by `InitMissionMonstre 0x47af90` (committed in Stage 9):
    - `0x50a9bc`: HumanOnly u8; Proba dwords at +4/+8/+12; u16 count at +18; 100 × 12-byte records at +20.
    - `0x50af84`: 16 × 26 type counts, then 16 group counts at +416.
    - The `Random` state `0x497164`.
- **Graphics.** `NextAnimTerrain(ax=u16 0x508720, dx=u16 0x508722)`, `NextAnimVeget` (same arguments), `NextAnimVegetFullMap()`.

### Supported limits and gaps

- Erratum: the first draft of this stage called the prelude step `0x454530..0x454591` an HP regeneration and `+0xb7` a substate. The bytes are unchanged; combat identified them as the reload advance and the attack target mode.

- The captures fix the caller's own order, gates and stores under declared fixtures; stubbed callees are not executed. Captures are not whole-state oracles and do not validate any callee.
- Menu, video and briefing states of `CalculGame` and the input routines are inventoried only by target address (second wave).
- The `EnginNextEtape` prelude conditions are inventoried at the level stated in the manual; its full branch-by-branch translation is Stage 4. The type-17 branch (`0x4549c2`) and inline state 6 (`0x4568ad`) are not described beyond their callees.
- Behavior record 0 of the table `0x498e94` points to `0x521368`, outside initialized data, so it is resolved only at run time.
- `iaProbLoadBinaryRules`, `debugSymLoad` and `debugSymUnload` are file I/O stops in the IaAlloc capture. Stage 2 needs the rule-file binding; core's `ler_rul` parses the same format.
- The `core_status` field of the inventory is a snapshot of core's `MaquinaTarefas` at `8a499a9`. It is excluded from the regeneration test so that later core work does not break this suite.

### Statuses

- Implemented: no behavior (contract stage); evidence tooling only.
- Validated against the original: the inventory is regenerated from intact bytes, and the captures are freshly replayed natively.
- Integrated on main: through `workstream.py integrate ai-runtime`. Implementation commit `87f3567`; the feature and merge SHAs are in the stage report, not amended here.
- Tested in a real mission: no.
