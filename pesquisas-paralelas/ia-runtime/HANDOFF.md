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


## Stage 2 — recovery of the AI initialization WIP (2026-10-28)

The current human authorization supersedes the older STOP. Recovered intact from clean WIP `ad97e4228c67dac24ed8024c46183e8628cf7ef8`; no existing worktree, candidate, original capture or media was replaced. Inspected fetched main `8810b3730a0fb788af3eac2b447dea65372f597f`, then merged the completed core recovery main `b610bfad77ffadaa0ee5f6af02160d786ccfdc7b` as feature merge `a62231635351a6f745b105154cfef137dce0fee4` before native validation, retaining the current missions/economy/combat/core agreements. Stage 1 statements above remain historical; the public initialization providers now exist.

**Slice:** `reinicio_ia.reiniciar_ia(memoria, mundo)` (`IaReset 0x47f36e`), `iniciar_ia_programa(memoria, ligacoes)` (`IaAlloc 0x47fb15`) and the independently uncalled `resetar_ataques_ia(memoria)` (`IAResetAttaque 0x47c162`). The full memory layout, original widths, callback arguments, consumed returns, mutation order and error boundaries are in [the Stage 2 manual](../../docs/AI_RUNTIME.md#stage-2--ai-table-reset-and-program-initialization). Missions calls the reset at `0x46c5cc` / `0x46c98e` and ignores EAX. Core's RNG positive path is consumed directly; VM/task execution and physical bodies stay core-owned. The task-pool reset here is the agreed AI initialization, not a fork of VM execution.

**Recovery audit:**
- `evidencias/captura-reinicio-original.json` from the WIP remains byte-identical, SHA-256 `f038dd159363940f894489a0c333805d0ff97d7be0458e67640ab2c757f0cd9d`. Its 19 cases are 11 complete resets, three program initializations with explicit bindings, one attack reset and four group helpers. They contain 66,977 observed calls/bindings and 133,960 bench segments; nine partial-state checkpoints are separate executions. No pre-translation chronological claim is inferred from a single WIP commit.
- The additive `auditar_reinicio_ia.py` / `evidencias/reinicio-byte-audit.json` checks a static closure of 32 game/RNG routines, 1,749 instructions and 5,899 original bytes, including 1,016 bytes absent from Stage 1's export. All 18 boundaries are named: 13 world providers, three file/SBL bindings, a clock import thunk and stack-local formatting. This is static closure, not full branch coverage.
- The oracle executes native world routines and records their arguments, returns and non-stack writes; `MundoRepetido` enforces the same call sites, order and arguments. IaAlloc's clock, SBL and rule-loader bindings have explicit fixture returns; actual rule-file/SBL memory effects are not established. No consumer adapter or automatic bindings are installed.
- Corrected a validation flaw: the WIP's intentional-loop test accepted a generic bench-limit RuntimeError. The recovered test requires three identical native checkpoint states at `0x47b1f4` after one transient visit, including all relevant integer registers/flags/segments, the full stack and all images/pools. Every jump executes, every segment must reach its exact stop, and world/file/clock entries cause failure if reached in the cycle. A timeout/instruction limit remains a failure. Python's retained image must equal the first original checkpoint.

**Fresh validation in recovery round `CXR-20261028-01`:**

```sh
python3 -B pesquisas-paralelas/ia-runtime/validar_reinicio_ia.py --emular --relatorio pesquisas-paralelas/ia-runtime/validacao/recuperacao-stage2-native.json
python3 -B scripts/check.py --domain ai-runtime
python3 -B pesquisas-paralelas/ia-runtime/validar_reinicio_ia.py --relatorio pesquisas-paralelas/ia-runtime/validacao/recuperacao-stage2-local.json
```

- Native: **36/36 tests pass**, zero failures/errors/skips. The 19 freshly recaptured cases reproduce the historical whole document, including nine partial-state checkpoints. A second set of 19 direct original/Python runs compares all three image buffers byte for byte, consumed EAX and every provider call/argument/site/order; 66,977 calls/bindings and 133,960 segments in each complete-case set. Counts of partial checkpoints and the intentional cycle are separate, not added to those whole-return counts. Stage 1's 57 caller captures also replay unchanged; its stubbed-callee scope remains historical and distinct.
- Intentional cycle: four checkpoint visits, six original resumed segments; visits 2/3/4 have identical integer registers/flags/segments, full 65,536-byte stack and all images/pools, with no external calls/bindings in the cycle. Its native prefix has 13,949 segments. Python's `NaoTerminaNoOriginal` retains the exact first original stopped image. No generic timeout/instruction limit is accepted as success.
- The first proof and diagnostic attempts failed because visit 1 had three transient stack bytes (offsets 32616, 32620, 32621); all registers/game images matched, as did later complete states. The final proof explicitly accounts for this observed transient while retaining complete-state equality. Both failed logs remain in `.local`; [the attempt journal](validacao/recuperacao-stage2-attempts.json) records their hashes and distinguishes them from passing runs.
- Local/domain: 36 discovered, 32 executed and four explicit native skips, zero failures/errors. Documentation links, syntax and diff whitespace pass. [Native report](validacao/recuperacao-stage2-native.json) and [local report](validacao/recuperacao-stage2-local.json) identify base revision plus exact source/provider hashes. No predecessor report was overwritten. Integration and targeted committed-main reproduction follow these checks.

**Supported boundary and gaps:** explicit mapped/declared inherited regions; four player records, 800 unit slots, well-formed group links and the tested positive RNG domain. Missing providers raise `DependenciaIA` with original call address and preserve prior effects. Unsupported memory access raises `AcessoNaoDeclarado`; provider errors propagate. The malformed empty monster-spec loop has an explicit `NaoTerminaNoOriginal` boundary, not a successful reset. The actual-MONDE01 fixture includes its serialized structures, units and auxiliary tables through committed loaders; the surrounding fixture is declared and does not represent complete MissionLoad. No dispatcher, kernel, rule-world operation, live frame, first raid or real mission is demonstrated here.

This delivers a bounded raw-memory IaReset implementation and original comparison; **L9 still needs production provider adapters, composed load tails and full MissionLoad equality**. The original-ABI callbacks are explicit and are not a production adapter. Rule/SBL I/O, complete mission load and mission-runtime testing are not run. Integrate and ancestry-verify this recovery, then perform targeted committed-main reproduction. End round `CXR-20261028-01` and release the heavy lease; no dispatcher/kernel or next research stage begins. The global estimate is coordinator-owned and is not advanced from these counts.


## Stage 2b — M1 production-adapter light inventory (pending owner queries)

New human authorization permits justified M1 rounds only until 18:25 BRT on 2026-10-28, then handover through the absolute 18:40 cutoff. The previous recovery is integrated at `5d24c91104e8b7f66b774e5b46969508708cc01f`; this is a separate bounded adapter task. No x86, Ghidra or heavy check ran during this light window.

[evidencias/reinicio-provider-inventory.json](evidencias/reinicio-provider-inventory.json) audits all 13 original-ABI callbacks and the exact original call sites. Existing real delegates: economy `Mercado.tipo_jogador` over the live player table, Core `MundoUnidades.viva` over the live unit pool and economy `Economia.consultar` over the actual resource table. Core's `I_DonneTypeUnite` operation is related evidence, not justification for a fabricated VM/world. The coordinator requested direct reusable `EnginGetType 0x442025` and `TypeEnginEstMonstre 0x4422dd` queries from Core's active M1 slice, and `MissionGetNum 0x46c11a` from Missions' active slice. No live sibling tree was imported.

`MissionGetNum` is independently confirmed as exactly `xor ah,ah; mov al,[0x496fe4]; ret` (eight original bytes, SHA-256 `d7f04a28a4d01d8fb09eefc005ed13df4c5762237660e759d06a45e6240aa92a`); the adjacent byte is not consumed. Missions confirmed its existing one-byte `MemoriaReinicio.missao` is the input. Until an actual committed getter lands it remains a named dependency, never a literal mission number.

The future adapter accepts explicit original-address memory segments and requires the same actual buffer range as the production objects: world units at `[0x4e19a0]`, player records at `[0x5080a8]`, world groups at `0x51a9e0`, world structures at `0x49a0c8`, and economy resources at `0x4e2ea8`. A whole-DGROUP shadow that hides a separate group's/resource table is invalid; independent constructor copies are not aliases. Core's scalar iterator attributes must agree with raw `0x51b844`/`0x51b848`; a documented bridge must update the raw slots and attributes together on AI writes, retaining partial effects. No silent rebind/copy is allowed.

Player controls are inherited inputs. Historical MONDE01 reset fixtures declare `(1,0,0,0)` or `(1,2,2,2)`; neither establishes original menu/program initialization. The former currently reaches missing `TypeEnginEstMonstre` at `0x47b006` and later missing `MissionGetNum` at `0x47b02c`. Any reached type-2 player may stop first at economy `RechercheGetNiveau 0x4717c2`, CALL `0x47f43f`; its companion `RechercheSetBranche 0x470b37` at `0x47f4ca` and `BatimentExiste/GetPlayer/GetType` remain actual provider gaps. The adapter will not select human-control defaults to skip them. Core's `EnginGetEtat` and full `EnginSetPlayer` (including passenger propagation) remain separate dependencies; no generic owner-byte store substitutes for the latter.

**Four statuses:** adapter implemented **no**; adapter validated against original **not run**; adapter integrated **no**; tested in real mission **no**. This light task stops at concrete missing committed owner queries. Inventory/ownership messages are preparation, not an apparent callback-container delivery. No generic production adapter was fabricated. The coordinator can reallocate this freed slot to Economy and resume the bounded adapter once its required providers are committed.


Economy-owner clarification (light audit against main `e9f5dbd33972344e37db3a93be1aec9c115a88bf`, source hashes rechecked): reuse actual `Mercado.tipo_jogador` and `Economia.consultar`; their methods do not accept the AI wrapper's `sitio` metadata. Mercado and the mapped resources must reference the same Economia object and actual buffer ranges. Economy also confirms combat's existing `ataque_vivo.batiment_get_player` is a genuine reusable owner query (lowAX0..999, raw+4 including 200/255, no state filter/stores), so no duplicate is needed. Four missing economy leaves remain: `RechercheGetNiveau` reads a **byte**, zero-extends AX and requires explicit inherited 64-byte research state at `0x5080f4`; proposed protected player/branch are 0..3. `RechercheSetBranche` accepts every DL value 0..255 and stores only one branch byte at `0x5080f8+16*player`, without technology effects. `BatimentExiste` returns state+5 !=0 (including3/4/5); `BatimentGetType` returns raw+8 without alive/type filtering. These are owner-confirmed contracts, not newly implemented or natively validated leaves. No heavy work is authorized by receipt of this message; adapter statuses remain unchanged.
