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


Stage 2b actual adapter preparation, 18:10 BRT (same bounded slice): committed Core/Missions getter main `2456848e57c1fbb63f3590023e424012c0916d3e` was merged into this feature tree without importing live sibling files. New owned `reinicio_ia_compartilhado.py` provides a small callable `ReinicioIACompartilhado` over actual Core/economy/mission objects and exact host ranges; no callback return/store replay is used. Public arguments, alias and scalar behavior, missing owner calls and input/control limits are in [the adapter section](../../docs/AI_RUNTIME.md#stage-2b--production-delegate-adapter-preparation-native-gate-pending). Controls remain explicit live inherited bytes.

`validar_adaptador_reinicio_ia.py` consumes all 11 preserved original IaReset inputs. Current light local replay completes the declared `(1,0,0,0)` MONDE01 fixture with identical full final images/EAX/provider sequence and reaches named dependencies on ten other fixtures; it never changes a type-2 player into a human. Four focused host-alias/control tests pass; one opt-in native test is not run. The existing frozen original observations precede this adapter and are expectations only, never its production providers. The validator's opt-in native mode is prepared to compare complete or stopped original image state and exact provider order on every fixture, retaining partial effects. Its local report `validacao/stage2b-adapter-local.json` records inherited controls, source identities, completed vs stopped cases and explicit no-native status.

**Readiness:** useful owned source and local proof are prepared; native comparison, owning domain gate, commit delivery, helper integration and committed-main reproduction remain **not run/pending explicit coordinator grant**. Economy's three actual committed leaves are still absent in this checkout; missing EnginGetEtat/SetPlayer remain outside the evidenced complete domain. No whole MissionLoad or original/current startup-control claim. Development ends at 18:25 BRT; if validation cannot finish within the authorized window, preserve this source as a WIP handover rather than claim closure.


Stage 2b readiness at 18:13:48 BRT: coordinator permitted extraction of only the clean immutable Economy source blob from commit `41817582430d327b20754bb768a28f559cc0e8ed` to ignored read-only scratch. Its SHA-256 `c81239ae0b7527c01242ef3f95b0c11cfa35cbae6333e7c0068ef6a67e1ec268` was checked before loading under unique `_rising_stage2b_economy_4181758`; no live sibling import or sys.modules replacement occurred. A **test-only** subclass forwards the adapter's three owner-query calls to that module's actual stateless function bodies. The production adapter source is unchanged and continues to require the real same-checkout owner module when integrated. This local commit is not yet claimed natively validated or integrated.

The separate `validacao/stage2b-adapter-immutable-provider-local.json` shows both historical declared-control MONDE01 inputs complete with full original final hashes, EAX and provider-call order, including the `(1,2,2,2)` AI-player fixture. The other nine inputs retain exact named stops: eight at `EnginGetEtat` CALL `0x4843ea`, one at `EnginSetPlayer` CALL `0x47b01f`. Production delegates read/mutate the shared inherited raw buffers; original observations are expectations only. Fresh original partial-state comparison is still pending; those nine stopped-image hashes are local observations, not upgraded to original equality. Four alias/control tests pass; one native adapter test is not run. The nearest complete **fixture** domain is now explicit; actual startup controls, full MissionLoad and real M1 remain unproven. Economy-provider validation/integration must precede any adapter integration.


### Stage 2b final focused native checkpoint — handover, not main delivery

The coordinator granted **only** the focused native attempt at 18:23:50 BRT, after Economy released its lease and integrated validated provider main `85dc8130cf45966f8cde6001b6ccb860d32d4db1`. The clean feature merged fetched main as `a5316d4b8b22265eaeb29afd4909c39314f52044`. Its same-checkout Economy runtime SHA-256 is `c81239ae0b7527c01242ef3f95b0c11cfa35cbae6333e7c0068ef6a67e1ec268`; no scratch/provider override is used by this native run.

The ignored finite-budget wrapper ran exactly:

```sh
python3 -B pesquisas-paralelas/ia-runtime/validar_adaptador_reinicio_ia.py --emular --relatorio pesquisas-paralelas/ia-runtime/validacao/stage2b-adapter-native.json
```

Fresh [native report](validacao/stage2b-adapter-native.json), SHA-256 `19db7ddeab0b5f660022c2f1683b05f4abc8d3a31f571a6fe7a1bc256e050e64`: **all 11 complete/stopped original comparisons pass** over 75,967 native segments. Two complete historical MONDE01 fixtures (including declared AI controls) return with matching full DGROUP+.bss/unit/player images, consumed EAX and actual-provider call order; 19,028 segments. Nine deliberate dependencies retain the exact original partial image and call-prefix order; 56,939 segments: eight `EnginGetEtat` CALL `0x4843ea` / entry `0x440e11`, one `EnginSetPlayer` CALL `0x47b01f` / entry `0x443108`. All Core group/scalar aliases remain coherent. No original callback return/store replay supplies production effects. Historical captures remain unchanged.

[Attempt journal](validacao/stage2b-focused-attempt.json) records start 18:23:52.459 BRT, exit 18:23:56.763 BRT, exit code 0, a 60-second hard budget and the before-18:25 deadline. No timeout/failure/skip occurred in this focused validator. The heavy lease was explicitly released immediately on child exit. Four local guard tests had passed earlier; the **full AI suite, owning domain gate, helper integration and targeted committed-main adapter reproduction were not run** under this final grant. Do not infer their success from the focused proof.

**Four statuses:** implementation prepared **yes** (bounded actual-delegate adapter); original-validated **yes for these 11 declared complete/stopped fixtures**; integrated on main **no**; tested in a real mission **no**. L9/complete MissionLoad remains open: actual original/current startup-control state, full load-tail composition and whole mission oracle are not established. Missing Core state/ownership bodies remain named, not substituted. The source WIP `1a455b037a3af8a290d988753e52c72d0deec2e2`, source merge `a5316d4` and this evidence checkpoint are preserved for Claude. Next authorized maintainer action is the pending full suite/domain/helper integration from the clean feature branch, preserving every prior report and the unchanged common integration lock; do not start dispatcher/kernels or a new stage before that gate. All new development stops at 18:25 BRT; handover operations alone may continue to 18:40.


## M2 slice 1 — frame inventory, M1 post-load captures, skeleton and dispatcher loops (2026-10-28)

Branch `feat/re-ai-runtime`, merged with main `81ebbf9` (fast-forward). The intact executable is SHA-256 `6c556520…43fb`. Input label: **"M1 post-load input"**, the frozen accepted final state `58a5020e…` of `captura-carga-missao-original-v2.json` (read-only), replayed natively and hash-checked each run.

### Commits
- `32dfb4a` static frame inventory: `inventario_quadro_m2.py` and `evidencias/inventario-quadro-m2.json`, plus the M2 section of `docs/AI_RUNTIME.md`.
- `a2a4aad` CalculGame frame-body skeleton (`quadro_calcul_game.py`) with its replay test against the 8 Stage 1 frame captures.
- `678c42c` capture script `capturar_quadro_m2.py`.
- `66db4e4` **native captures, committed before any translation**: `evidencias/captura-quadro-m2-pos-carga.json`, 46/46 returned, 0 bindings, 0 skips, 0 faults.
- `e24b0e1` dispatcher loops `laco_despachantes.py`, hybrid validator `validar_despachantes_m2.py` and local tests.
- `1b8e2fb` native hybrid report `validacao/m2-despachantes-native.json`: **23/23 equal** (whole image SHA and provider order).

### API (inputs, domain, mutation and callback order)
- `calcular_quadro(memoria, provedores)`, CalculGame `0x42d2de..0x42d4f5`. `memoria` is a `MemoriaDeclarada` covering `REGIOES_QUADRO`; `provedores` maps original names to `f(sitio=…, **args)`. It returns `{saida, chamadas}`. Exits are `0x42d4e2` (clears `0x5099b0`), `0x42d4ea` and `0x42c92c` (the MenuInit tail). Call order and stores are as in the original body (doc table). It is single-player and network aware.
- `Quadro.calcul_next_reflect(jogador, missao)`, CalculNextReflect/iaCalculPlayer through Core `ia.atualizar_ia`. It stores the counter `0x51a995+16p` for active players and the inactive byte only on the tenth empty cycle. Kernel sites are `0x47f939/45/9ad/9df/9ea/9f5/a02/a12`.
- `calcular_proxima_etapa_unidades`, `calcular_proxima_etapa_estruturas`, `testar_utilidade` and `testar_mensagem_unidade` in `laco_despachantes.py`: domain and providers as documented in `docs/AI_RUNTIME.md` (M2 step 2).
- Missing providers raise `DependenciaIA(name, original call site)`; partial stores are retained. The unreached iagMessTestSendMessageEngin group path raises at `0x483f5d`.

### Native counts and validation
- Capture run: about 34 s for the startup and MissionLoad replay; 46 captures in under 1 s. Trace sizes: unit loop 188 entries, structure loop 23, monster AI 5.
- Hybrid validation: 23 cases in 36 s, all equal.
- Local suite: 50 tests, 5 native opt-in skips (pre-existing).
- Gate: see the report.

### Gaps and next
1. **AvanceMonstre `0x47b283` (player 4) and iaSolver** for frame 1. It stores `0x50a9cc` = 1, and the solver finds an empty task list. Next ai-runtime slice.
2. ProcessInputGame (clear-only at frame 1) and MessageBoxCalcul (read-only), then the EnginNextEtape prelude for states 7/14.
3. Re-validation at Missions' exact frame-1 input once it is published (the load-entry tail and the earlier frame steps differ from this input).

### Cross-front contracts requested
- **Missions**: the frame-1 oracle must bind `MCICD_Play` (byte `0x4e2f28` = 0 at MONDE01) or stop there under the audio owner. Please publish the per-routine entry trace with return sites, so this front can align its traces (same format: `callee@caller-site EAX EDX EBX ECX`).
- **Economy**: PlayerGetType ≥ 4 → 2 is consumed by the frame; `Mercado.tipo_jogador` already provides it. BonusGetValEngin, state 7 (AnimBallonStatic/Random), BatimentNextEtape type 2 (BagContientTroupe, CalculTroupe) and ResetTableauHangar are reached at frame 1.
- **Core**: GetBit, CalculFatigue, SetEnginCollision/SetCollision/Chemin_ModifieZone and Random are reached by every MONDE01 state-7 unit; BatimentGetCase, CaseEstDecouverte, BatimentEstDecouvert and BatimentContourEstIllumine by the structure loop. iaSolver over the actual task pool (`tarefas_ia`) is needed for player 4.
- **Combat**: EnginTrouveCible (→ PlayerEstAllie) is reached for unit 0 at frame counter 0, and ProjectileCalcul is reached every frame.

**Statuses:** implemented: loops, IATestUtilite and the frame skeleton. Original-validated: yes, at the M1 post-load input (23/23 hybrid, 17/17 local IATestUtilite, 8/8 Stage 1 frame captures). Integrated: no (the coordinator integrates). Tested at the exact frame-1 input: no (waits for Missions).


## M2.1 round 2 — first-frame composition (2026-10-28)

Merged main `ec931d2`. The report is [FRAME1_COMPARISON.md](FRAME1_COMPARISON.md).

- **Commits:**
  - `3b4d227`: isolated original captures at the exact frame-0/1 inputs (before translation).
  - The composition, translations and comparator commit, followed by the report/docs commits (see git log).
- **API:**
  - `composicao_quadro1_ia.fase_cauda_carga`, `fase_entre_quadros` and `fase_quadro`. Inputs: a `MapaMemoriaM1` and its providers, a `ContextoQuadro` (Core task machine + original jump tables), a `Registro` for bindings/boundaries, and the declared Windows answers.
  - `rotinas_quadro_ia.calcular_caixa_mensagens`, `processar_entrada`, `avancar_monstros` and `resolver_ia`, over a `MemoriaDeclarada`. `REGIOES_ROTINAS` plus the dynamic regions (unit pool, input records) must be declared.
- **Validation:** native composition compare: (a) stop equal at RestoreAll, (b) full equality, (c) stop equal at InputGame. The isolated differential is 22/24 equal; 2 are structure-loop provider stops. Missions' path reproduction passed in both native runs. The local suite has a sparse-read regression on the isolated captures.
- **Gaps:**
  - The owners of InputGame/InputSend and of RestoreAll/SetClipping/MenuInit/InitGameZone (coordinator).
  - The EnginNextEtape prelude (this front, next).
  - iaSolver beyond the empty context, which goes through a bridge into Core's private machine (a Core contract is requested).
  - The AffGame write set (graphics, open item).
- `validacao/m2-despachantes-native.json` (slice 1) predates the lazy-read change in CalculNextReflect. The behavior is unchanged, and the change is re-checked by the new native differential.


## M2.1 round 3 — chained frame-0/1 composition (2026-10-29)

Merged main `67fb81f`. The report is [FRAME1_CHAINED_COMPARISON.md](FRAME1_CHAINED_COMPARISON.md).

- **Result:** (a), (b) and (c) are all equal to the original, chained from Python. Eight declared-stop crossings, each with the state equal at entry: RestoreAll (graphics), SetClipping, InitGameZone ×2 and NextAnim* ×4 (core, pending).
- **Commits:**
  - `f60137a`/`4e10cdd`: captures before translation.
  - The translation + composition commit, then the report/docs commit (see git log).
- **API:**
  - `entrada_quadro_ia.entrada_jogo(m, jogador, registro, janelas)`.
  - `enviar_entrada(m, jogador)`.
  - `calcular_icone_acao(m)`.
  - `iniciar_menu(m, jogador, estado, ecx, registro, janelas, provedores, ebx, esp)`.
  - `proxima_etapa_quadro.proxima_etapa_unidade(m, provedores, unidade, tabelas)`.
  - `proxima_etapa_estrutura(m, provedores, estrutura, tabelas)`.
  - `composicao_encadeada_ia.fase_cauda_carga` and `fase_quadro`, with `Travessias` (crossings and checkpoints).
  - `memoria_composicao_ia.MemoriaMapaM1`.
- **Mutation and callback order:** original order throughout. The providers receive `sitio` and original-width arguments. Untaken branches raise `DependenciaIA` at their addresses.
- **Gaps:** the stack words of stale locals in four boundaries; the tile-grid list/bytes contract between Economy and Core; iaSolver beyond the empty context; the crossings, until Graphics/Core land their routines.


## M2.1 round 4 — display reference (2026-10-29)

Merged main `81e0a26`. The report is [FRAME1_DISPLAY_COMPARISON.md](FRAME1_DISPLAY_COMPARISON.md).

- **Result:** display (a)/(b)/(c) all equal, chained from Python, with 96/96 checkpoints. The v1 regression is equal.
- **Crossings:** Graphics' display routines (no logic bytes), and Core's NextAnim* provider stops at `0x477737`/`0x47731b` (logic: the CRT seed and `0x4e1d18`).
- **Commits:** `ad27649` (display captures, before translation), `fc864d4` (translations + composition), then the report commit.
- **API changes:**
  - `entrada_jogo(..., provedores)` serves the zone-0 hover; it needs CaseEstDecouverte, CaseEstIlluminee and EnginOccupeCase.
  - `iniciar_menu` takes display-call providers (`provider(sitio, registros, palavras, limpeza)`) and uses the register dict returned by InitGameZone.
  - The composition is scenario-aware (`ContextoEncadeado(imagem, cenario)`). `Travessias` keys are (phase, routine, call-return site, occurrence), and crossings carry allocated/released blocks.
- **Gaps:**
  - Core's NextAnim* cell loops.
  - Graphics' display routines.
  - The Missions mask.
  - Unmodeled stale-local stack words in the frame-body MCICD_Play boundary.


## M2.1 round 5 — first-frame equality proof (2026-10-29)

Merged main `d94a59e`. The report is [M2_1_PROVA_QUADRO1.md](M2_1_PROVA_QUADRO1.md); the data is in `validacao/m2-1-prova-quadro1.json` (fresh native run from a clean tree, under the lease).

- **Result:** all three phases equal, with zero crossings.
- **New code:**
  - `bancos_quadro_ia` (DeleteBank/MemFree on `ArenaQuadro`).
  - Mode `prova` in `composicao_encadeada_ia`.
  - `provar_quadro1_ia`.
- **Disagreements with my round-4 classification:**
  - DDLock/DDUnlock bookkeeping `0x4e17a6..a8` is compared by the policy; the proof shows it restored.
  - The DeleteBank records are compared; they are now modeled.
- **Process:** one development trial executed the native collection outside the lease. It crashed and produced no evidence.


## M2.2 preparation — N-frame composition (2026-10-29)

Merged main `5c0dac2`. The report is [M2_2_PREPARACAO.md](M2_2_PREPARACAO.md). No native run beyond frame 1 was made; the Mac mini captures and the cumulative mask are pending.

- **API inputs:**
  - `composicao_quadros_ia.ComposicaoQuadros(estado_s0, captura_quadro, entrada, captura_m1, planejamento=False).executar(n)` yields `dict(phase, registro, entry, exit)`.
  - `affgame_hud_ia.affgame_hud(m, desenhar)` returns `EfeitoHud(desenhou, escritas, eax, leituras)`.
  - `contexto_exibicao_ia.ContextoExibicao(imagem, raizes).vinculo(e)` and `.fronteira(e)`.
  - `comparar_quadros_ia.py --captura --politica [--quadros] --saida`.
  - `percorrer_quadros_ia.py --quadros N --saida [--planejamento]` (planning writes under `.local/` only).
  - `fase_entre_quadros_exibicao(..., fase=)` and `fase_quadro(..., fase=)` take the phase name. In mode `prova`, AffGame's leftover EAX becomes the boundary EAX.
- **Supported domain:**
  - display scenario `-v2`, mode 0x12, no input, no event;
  - AffGame within Graphics' proved domain;
  - EnginNextEtape scan hits stop at `iagUnitSendMessage`/`SetAttaqueEngin` (not reached in 128 frames).
- **Mutation order:** original order. AffGame stores the flag after Graphics' guards. UpdateChamp reads an immutable tile-grid snapshot taken at the call.
- **Validation:**
  - The comparator self-test on the `-v2` frame-1 data equals the M2.1 proof (16,097,242 bytes per phase, 597/2/13 bindings, registers, 25,482 records).
  - The 128-frame planning probe equals Core's survey on every indicator and checkpoint call count; the HUD agrees 127/127.
  - `testes/test_quadros_ia.py` has 10 tests.
- **Gaps:**
  - Graphics' origin domain: (3,5), (2,4), (1,3), (0,2), (0,1).
  - The formal per-frame comparison.
  - The display-context events, EFLAGS/EIP, and the MCICD_Play stale locals.


## M2.2 — delta-form capture reader (2026-10-29)

`comparar_quadros_ia.py` reads the Mac mini capture format (contract in [M2_2_PREPARACAO.md](M2_2_PREPARACAO.md)).
- It rebuilds each phase from `state_s0` plus `state_delta` (`released`, `allocated`, `ranges`).
- It checks every `state_after.summary` (Missions' `resumo_imagem`) and the checkpoint `full_state`s.
- It accepts `.xz` with a pinned raw-JSON SHA-256 (`--sha256`).
- An inconsistent replay stops the run as a capture-integrity failure before any comparison.
- The `-v2` path is unchanged and now also checks the summaries.

**Validation:** the `-v2` frame-1 data and its delta-form conversion (in `.local/`) both reproduce the M2.1 proof. `test_quadros_ia.py` now has 12 tests, including replay, checkpoint and named-failure cases.


## M2.3 preparation — first raid, checkpoint start (2026-10-29)

Main `8564ca7`. The report is [M2_3_INCURSAO.md](M2_3_INCURSAO.md).

- **Capture first:** `capturar_incursao_ia.py` → `evidencias/captura-incursao-ia.json`. It is Combat's forced counter-9000 input, with each outside call's arguments, exit registers and net writes, plus the own-routine writes; native, 40 s, under the lease.
- **API inputs** (all in `incursao_ia`):
  - `avancar_monstros(m, p)`, with `rotinas_quadro_ia.avancar_monstros` delegating to it;
  - `construir_grupo_monstros(m, p, celula, grupo)`;
  - `guardar_acao(m, p, acao, grupo, celula, origem)`;
  - `novo_grupo(m, jogador, tipo)`, `adicionar_ao_grupo(m, grupo, unidade)`, `primeira_unidade(m, grupo)`;
  - `enviar_mensagem_unidade(m, p, unidade, mensagem, alvo)`.

  Provider contract: the table in the module docstring.
- **Composition:** iaProbPost runs on `MaquinaTarefasViva.postar` and ProjectileInit on `PoolProjeteis.iniciar`. The EnginNextEtape scan hit passes `alvo`.
- **Checkpoint start:**
  - `ComposicaoQuadros(..., inicio, alocacoes, regs_inicio)`;
  - `fases_quadros(n, inicio)`;
  - `comparar_quadros_ia.py --a-partir-de K`, with `alocacoes_no_ponto`.
- **Validation:**
  - `test_incursao_ia` reproduces the forced AvanceMonstre call byte for byte, call for call.
  - The checkpoint chain equals the full chain over frames 2–4.
  - The strict 128-frame probe is unchanged (128/128).
  - Both comparator self-tests are equal.
- **Gaps:**
  - Core providers (GetFreeCell, CreerEngin, EnginSetPlayer, PlaceEngin, EnginGetCase, GetRandCaseChamps, GetRandCaseTypeBatPlayer, Chemin_Accessible).
  - SetDeplaceEngin and SetAttaqueEngin.
  - The 0x49 behaviour handler; iagUnitSendMessage's dispatch is static and has no native capture.


## M2.2 — 128-frame equality proof (2026-10-29)

Main `c7ed947`. The report is [M2_2_PROVA_128_QUADROS.md](M2_2_PROVA_128_QUADROS.md); the data is in `validacao/m2-2-prova-128-quadros.json`. It is Python only, from clean revision `8beb95a`.
- **Reference:** Missions' 128-frame capture (raw SHA pinned, replay and 11 checkpoints checked).
- **Policy:** cumulative 128-frame mask.
- **Result:** all 257 phases equal, with zero crossings.
  - Every phase has 16,022,275 compared bytes, and RNGs, bindings/boundaries outside display, allocation counts and registers equal.
  - The final 25,482 records are equal, and the HUD flag matches 128/128.
- **Mixed bytes:** the HUD flag (modeled) and the clip words (restored by display, equal).
- **In progress, not pushed:** the M2.3 raid rules at counter 9000 sit on the local branch `wip/ai-raid-rules`. Their capture is waiting for the lease.


## M2.3 — raid rules at 9000, Core providers, segmented comparison (2026-10-29)

Main `99c0e4e`. Details are in [M2_3_INCURSAO.md](M2_3_INCURSAO.md), round 2.
- **Capture first:** `9fbc2bc` (rule calls at counter 9000, native, 38 s under the lease).
- **Translations:** `regras_incursao_ia` with `REGRAS`, `operacoes_regras(m, p)` and `MundoRegras(m, p)`. Rule signature: `regra(m, p, argumentos, jogador, indice) -> EAX`.
- **Validation:** `test_regras_incursao_ia` (6/6 calls equal) and `test_incursao_ia.RaidFrameWithCoreProviders`.
- **Composition:** it uses Core's `incursao_core`; GetFreeCell is a named stop (native stack residue).
- **Segments:** `comparar_quadros_ia.comparar_parte(caminho, politica, sha256_bruto, alocacoes_caminho)` and `resumos_mascarados(mascara, blocos)`. The CLI is `--parte`/`--alocacoes`.
- **Gaps:** Core's GetFreeCell residue contract, EnginEstVivant and SetDeplaceEngin; the 9500/9700/11100 rules (their capture needs about 2,100 sequential frames, which goes to the Mac mini); `opening_state.allocations` in Missions' parts.


## M2.3 — raid probe beyond the window (2026-10-29)

- **No known divergence.** The "one step ahead after counter 9716" report came from the probe's start point (after frame 1 with counter 8999, one extra frame of draws). It is withdrawn.
- **Equivalent start:** the native forcing is counter 9000 at frame 1's CalculGame entry. From that start, with Core's `6e12550`, Python equals the original:
  - world RNG, and unit 16's state, facing and cell: every counter 8999–9705, native probe;
  - unit 16's cell: every counter 9000–10878, Combat's course.
- **Call order:** the composition's order is the original's. At 9700 the native dispatcher runs DeplaceEngin in the same frame as the re-order.
- **Next stop, beyond the M2.3 window:** Core's CalculFatigue fatigue-threshold branch `0x452d61`, around counter 10880.
- **Tool:** `sondar_incursao_ia.py N` (Python only, `.local/` output) runs the composition with the forcing-equivalent start.


## M2.3 — 9,200-frame equality proof (2026-10-29)

Main `5f4052c` (Missions' evidence `de154b5`). The report is [M2_3_PROVA_9200_QUADROS.md](M2_3_PROVA_9200_QUADROS.md); the data is in `validacao/m2-3-prova-9200-quadros.json`. It is Python only, from clean revision `8a5787d`.
- **Reference:** Missions' 10 M2.3 parts (manifest SHA pinned; hash chain, every replayed summary/compared summary/masked hash, and the full states at 8999, 9000 and 9176 checked) and the cumulative 9,200-frame policy.
- **Result:** all 18,401 phases equal, frames 0–9,200, through the raid spawn at 9000 and the first path search at 9176–9179.
  - 16,022,275 compared bytes per phase; both RNGs; bindings and boundaries outside display; allocation counts; the 9,200 between-frames exit registers and 9,191 carried entry registers; HUD flag 9,200/9,200.
  - Part 09's final 25,482 allocation records are equal.
  - Zero crossings, measured per part (`comparar_parte` now reports them instead of a constant), and no Core provider stop.
- **Tool:** `provar_quadros_9200_ia.py` — `parte N`, `agregar`, or `tudo --paralelo 4 --lease <heavy_lease.py>` (one command, about 24 min on the MacBook with four parts at a time).
- **Next:** the coordinator's second-machine reproduction must match the ten `phase_chain_sha256` values listed in the report.


## M3.1 groundwork — input path, declared-input chain (2026-10-29)

Main `ea62eb4` (after the M2.3 proof `ecaf853` was integrated). The details are in [docs/AI_RUNTIME.md](../../docs/AI_RUNTIME.md#m31-groundwork--the-input-path-inputgame--setplayerordre--processinputgame--setters).

- **Capture first:**
  - `9f08979`: the case matrix and capture script.
  - `887b6c7`: `evidencias/captura-entrada-ordens-ia.json`, 124 native leaf calls at Core's frame-1 ProcessInputGame pause, all returned, with path and code reproduced.
- **Translation:**
  - `277891c`: `entrada_ordens_ia`, `provedores_entrada_ia`, `composicao_entrada_ia`, `provar_entrada_ia` and `validar_entrada_ordens_ia`.
  - The follow-up commit records the orders of a stopped probe frame.
- **Native differential:** 124 cases, 113 equal, **0 mismatches**, 11 named-dependency stops. Compared: registers, whole changed state, sound requests and key answers.
- **Declared-input API:** `RoteiroEntrada(scripted-input file)` and `ComposicaoEntrada(..., roteiro, inicio=128, ...)`. `executar(n)` yields phases with `ordens` and `eventos`.
- **Probe chain check** (Python, from the M2.2 frame-128 state, indicator level; reports `validacao/m3-1-sonda-*.json`):
  - P1: 501/501 frames equal.
  - P2: 601/601 frames equal.
  - P3: 24 frames equal, then tag 4 equal at 153 and a stop at EnginNextEtape state 11.
  - K1: 11 frames equal, then a stop at WM_KEYDOWN.
- **Named dependencies:**
  - Core: `construcao_core` (BatimentPosable) is on `feat/re-core` `63200b5`, not on main. The proofs used a read-only extraction (`--nucleo-ref .local/entrada/nucleo-ref`); without it, every page-3 hover stops there.
  - Economy or the owner to decide: SetDechargeCaveEnginSelect (tag 19), InitRecruteTroupe (tag 17).
  - Combat: BatimentInitAttaqueSelect (tag 14 with a structure selected).
  - MiniMapSetPos/MiniMapRecentre.
  - Missions: the text table `[0x5099a4]` is 0 in the display bench, so TextGetMessage over a field, mine or sack is a named stop. This blocks P4/P5 hovers.
- **Next for this front:** EnginNextEtape state 11 (0x4564ef: the `+0x89`/BatimentEnDestruction test, then CalculConstruireBatiment and the tail 0x454ccd). Then WndProc key messages 0x100/0x101 and the help pages 2/7/8/9/0xb/0xc (Ctrl deposit tags 8/19).
- **Captures needed:** pass-2 delta captures of the P1/P2/P3 windows (M2.2 form, with per-phase states) for the whole-state proof under the published mask. Also P4/P5 runs, and a text-loaded scenario or the text-table owner's answer.

**Statuses:**
- Implemented: the input path above and the declared-input chain.
- Validated against the original: the leaf cases natively (0 mismatches), and P1/P2 at indicator level over every frame.
- Integrated: no.
- Tested in a real mission: no.

## M3.1 round 2 — state 11, construction progress, keys, text boundary (2026-10-29)

Branch `feat/re-ai-runtime` after `298095b` (round 1, not yet on main). Details: [docs/AI_RUNTIME.md](../../docs/AI_RUNTIME.md#m31-round-2--state-11-builder-construction-progress-structure-entry-dispatch-keys).

- **Capture first:** `51a7f46` adds `evidencias/captura-construcao-teclas-ia.json`. It holds 90 native leaf calls, all returned, with path and code reproduced.
- **Translation:** `58bdd81`.
  - `construcao_entrada_ia`: state 11, the progress branch and completion, and six structure/animation leaves.
  - The state-13 dispatch.
  - WndProc 0x100/0x101, the group-number and GoLastAttaque keys, and ProcessInputGame tags 0xb/0xc/0x10/0x21.
- **Native differential:** 90 cases, 79 equal, **0 mismatches**, 11 named stops. Round 1 was rerun: 124 cases, 113 equal, 0 mismatches.
- **Text:** `c23352a` binds TextGetMessage in the chain as Missions' declared boundary (EAX 0, logged).
- **Chain check** (probes `b1cd5bd`):
  - P1: 501/501.
  - P2: 601/601.
  - P3/P6/P7: 91 frames equal, then a stop in frame 220 at the type-3 cave body.
  - P4: 293 frames equal, then a Graphics view-origin stop at 422.
  - P5: 443 frames equal, then a Graphics view-origin stop at 572.
  - K1: 12 frames equal, then a Graphics view-origin stop at 141.
- **Read-only extraction:** Core's `construcao_core` is on main `2ad381a` but not yet on this branch. The runs used `--nucleo-ref .local/entrada/nucleo-ref`; the file is identical to main's (SHA-256 `7ccf640c…`).
- **Named dependencies:**
  - Economy: the type-3 body `0x426aff`, BatimentRetireColon, BatimentHabitable.
  - Core: BatimentIllumine/BatimentDecouvre, the state-13 body (CalculEntreBatiment), Sauve/RestaureSelectionGroupe, SetEnginSelectRentreBatiment/Engin, EnginGetCentreGroupe, MiniMapRecentre.
  - SetMurAllentour.
  - Graphics: AffGame vegetation/terrain handlers at unsampled view origins. This blocks K1, P4 and P5.
- **Not done (next for this front):**
  - InputGame help pages 9/0xc/0xb/2/7 and the Ctrl deposit mode: `0x429601`, page 9 at `0x429b90` with the depot table `0x42923c` → tags 6/7/8/0x13, and pages 8 over a field or mine at `0x42b393`/`0x42b525`.
  - The tag-16 producer: the structure under the cursor with troops selected, `0x42ac32`.
  - P7's depot press at 3228 needs these.
- **Captures needed:**
  - Graphics: native samples of the AffGame view origins that K1 (1..19, 0..), P4 (10, 16) and P5 (31, 0) reach.
  - The probes' pass-2 delta windows, for the whole-state proof.

**Statuses:**
- Implemented: the above.
- Validated against the original: the leaf differential, and the chains at indicator level.
- Integrated: no.
- Tested in a real mission: no.

## M3.1 round 3: Ctrl deposit mode, help pages 9/0xc/0xb/2/7, structure under the cursor with troops (2026-10-29)

Branch `feat/re-ai-runtime`, pushed at `9409355`. Not integrated. Details are in [docs/AI_RUNTIME.md](../../docs/AI_RUNTIME.md#m31-round-3--ctrl-deposit-mode-help-pages-90xc0xb27-structure-under-the-cursor-with-troops).

- **Capture first:**
  - `d0bc84d` adds the matrix `casos_paginas_deposito_ia.py` and the capture script `capturar_paginas_deposito_ia.py`.
  - `c4ff87d` adds `evidencias/captura-paginas-deposito-ia.json`: 203 native leaf calls, all returned, path and code reproduced.
  - Page 0xb over a cell with no structure is not a case. BatimentGetType(0xffff) at `0x429ea2` reads `0x15d9fbc`, and the native smoke run faulted there. The translation stops there by name.
- **Translation** (`9409355`, `entrada_ordens_ia.py`):
  - Ctrl `0x429601`.
  - Page 9 `0x429b90` with the table `0x42923c` → tags 6/7/8/0x13.
  - Page 0xc (tag 0x24), page 0xb (tag 0x22), page 2 (tag 0xe), page 7 (tag 0xa + BatimentDeselectionner).
  - Page 8 over a field or mine (`0x42b393`/`0x42b525`).
  - `0x42ac32` complete:
    - page 8 over a cave (deposit mode 3);
    - enemy structures (tag 0x10 for type-10 units, tag 0xe);
    - builder repair (tag 0x14);
    - wounded units to a type-0x13/0xe structure (tag 0x15);
    - entry (tag 0x10, through Core's EnginSelectPeutEntrer);
    - unbuilt (tag 5).
  - The no-troops path with a structure selected (`0x42b289`) now calls Combat's BatimentPeutAttaquer by name.
  - Thirteen leaves: EnginSelectPeutAttaquer, EstTroupe, EstEngin, ContientMiroir, PeuventTransporter, EstBlesse and PeutDeposer; BatimentEstDepot, EstNeutre, EstEnnemi and PeutSeVendre; PlayerEstAllie; ChercheIndiceBatiment.
  - Fixed: `_armee` (TypeEnginEstArmee) was wrong for types 0x11..0x13.
  - Fixed: the TextGetMessage provider keyword collided with `sitio`, so the chain binding would have raised TypeError on first use. The keyword is now `local`.
  - Economy's `extracao` is imported with its own siblings, because Graphics has a `construcoes` with the same name.
- **Native differential** (`validar_paginas_deposito_ia.py --nucleo-ref .local/entrada/nucleo-ref-r3`): 203 cases, 201 equal, **0 mismatches**, 2 named stops (Combat's BatimentPeutAttaquer).
  - The `--nucleo-ref` directory holds `git show 90fd831:ferramentas/entrada_estruturas.py` (SHA-256 `5221608b…`).
  - TextGetMessage is the bench's display boundary (EAX 0, never executed). The differential binds it as the chain does and compares the message number.
  - Rounds 1 and 2 were rerun (output in `.local`): 124/113/0 and 90/79/0.
  - CPU-free replay: `testes/test_paginas_deposito_ia.py`. `RISING_NUCLEO_REF` optionally adds Core's extraction; without it, the EnginSelectPeutEntrer cases must stop by name.
- **Gate:** `scripts/check.py --domain ai-runtime` passes (112 tests).
- **Provider wiring done:**
  - Core's EnginSelectionnable (`selecao_ordens`).
  - Core's EnginSelectPeutEntrer (`provedores_entrada_ia.entrada_estruturas`, used when importable).

### Paused here: resumable next steps, in priority order

1. **Whole-state proof of the input chain over P1 (129–629) and P2 (129–729).** This is the coordinator's top priority. The deliverable is `validacao/m3-1-prova-p1-p2.json` plus an `.md`.
   - **Inputs.** The Mac mini windows are at `origin/feat/re-missions` `01745da`/`f56ed1d`. When they reach main (check `git merge-base --is-ancestor f56ed1d origin/main`), merge main. Until then, `.local/m3-1/ref/P1|P2/` holds `git show` copies.
   - **Window format** (`rising-lands/m3-probe-window-part/1`):
     - `opening_state.full_state` is the frame-128 state, with its summary, compared_summary and masked_sha256.
     - The phases run `between_frames129..frame629`, as complete deltas (`state_delta`) with `bindings`, `boundaries`, entry/exit `registers` and `rng`, and an `allocations` count.
     - The mask is `mascara-janela.json` `cumulative.exclusion_mask` (the M2.3 mask plus display-only bytes proven in the window). Note that the manifest's `definitions.mask` names "policy cumulative.exclusion_mask".
   - **Plan.** Write `provar_entrada_janelas_ia.py`, modeled on `provar_quadros_9200_ia.py` (per-part reports, an `agregar` step, a one-command run, phase-chain hashes).
     - Reuse the pinned `comparar_quadros_ia.comparar_sequencia` / `fases_referencia` / `MascaraEnderecos` / `ContextoExibicao`. Import them; do not modify them.
     - Use `comp = ComposicaoEntrada(s0, dict(named_inputs=cap_v2['named_inputs'], phases=parte['phases']), entrada, m1, RoteiroEntrada(entradas/P1.json), inicio=128, alocacoes=<from the M2.2 capture: cap['allocations']>, regs_inicio=parte['phases'][0]['entry']['registers'])`.
     - Check that the opening state equals the M2.2 frame-128 full state.
     - Crossings: measured with `travessias_medidas`.
   - **Failure rule.** Stop at the first divergence and report it precisely.
2. **The P6 window (129–2400, 4,544 phases, 3 parts):** the same tool. Report how far it goes with today's providers and its first divergence or named stop. The cave body `0x426aff` at frame 220 is expected.
3. **Wire Core's vision/groups** (`feat/re-core` `d07ed89`, `ferramentas/visao_grupos.py`; contract in `docs/core/VISION_GROUPS.md`). Check first that `d07ed89` is on main.
   - `provedores_visao(m, som)` provides BatimentIllumine/BatimentDecouvre as keyword providers in the `laco_despachantes` shape, plus MiniMapSetPos(x, y) and MiniMapRecentre.
   - `VisaoGrupos(m, som).chamar(nome, regs)` covers SauveSelectionGroupe, RestaureSelectionGroupe and EnginGetCentreGroupe (tags 0xb/0xc, the Shift group key).
   - Bind them in `provedores_entrada_ia.provedores_vivos` (and the chain's `p` dict for the frame-phase Illumine/Decouvre).
   - Rerun the round-1/2 differentials. This should clear `process_tag11/12`, `input_group2_shift_centre` and `p2_minimap_right_held`.
4. **Wire Core's `entrada_estruturas`** (still only on `feat/re-core` at last check):
   - `chamar('EnginNextEtape:state13', ESI=record, EDI=unit, ...)` for state 13. Adapt `construcao_entrada_ia.proxima_etapa_entrada`: it currently calls the provider with only the call site and the unit, so it must build REG7 with ESI = the record and EDI = the unit.
   - `SetEnginSelectRentreBatiment` for tag 0x10 sub 3, and `BatimentRetireColon` for tag 0x21 (Core raises `ForaDoDominioEntrada` outside its domain).
   - Its named dependencies: Economy's BatimentLogeEngin (now `ciclo_trabalho.CicloTrabalho.batiment_loge_engin`, on main), iagUnitSendMessage messages 0x44/0x47/0x42 (this front; only 0x49 is translated, in `incursao_ia`) and PlayerInitPropositionAlliance.
5. **Economy's `ciclo_trabalho`** (on main): CalculWorkEngin for unit state 5. Find EnginNextEtape's state-5 target in `proxima_etapa_quadro`'s table and dispatch it like state 11. Also its BatimentLogeEngin (above).
6. **Audio:** `pesquisas-paralelas/audio/provedor_pedidos_m3_audio.py` on main (`M3_REQUEST_CONTRACT.md`). Not checked yet against this front's `som(nome, regs, pilha) -> EAX` boundary.
7. **Rerun `provar_entrada_ia.py`** on P1..P7 and K1 after 3–5. Main now carries Economy's CAVE body (0x426aff) and recruitment, so check main for them first. Since round 2, P3/P6/P7 stop at frame 220 (the cave body); P4, P5 and K1 stop at Graphics view origins. The probe reports in `validacao/` were not rerun this round.
- **Named dependencies still open:**
  - Combat: BatimentPeutAttaquer, BatimentInitAttaqueSelect.
  - Economy: SetDechargeCaveEnginSelect, InitRecruteTroupe, BatimentHabitable, the 0x426aff body.
  - SetMurAllentour.
  - SacGetCapacite.
  - Graphics: AffGame at unsampled view origins.

**Statuses:**
- Implemented: round 3 above.
- Validated against the original: the leaf differential (0 mismatches).
- Integrated: no.
- Tested in a real mission: no.

## M3.1 — P1/P2 whole-state proof (2026-10-29)

Merged main `ef52cb0`. The report is [M3_1_PROVA_P1_P2.md](M3_1_PROVA_P1_P2.md); the data is in `validacao/m3-1-prova-p1-p2.json` (Python only, clean revision `21bbb37`, one command under the heavy lease).

- **Result:** P1 1,002/1,002 and P2 1,202/1,202 phases equal under each window's cumulative mask, zero crossings, by the M2.3 method, plus the consumed scripted inputs, WndProc flag bytes, SetPlayerOrdre/ProcessInputGame records and the M3.1 fields (packets `[0x4e2458+4p]`, selection areas `0x508728+512p`, unit order fields of all 800 slots; none masked).
- **Tool:** `provar_entrada_janelas_ia.py` — `janela <P>`, `agregar --janelas ...`, `tudo --janelas ... --lease <heavy_lease.py>`.
- **Chain fixes** (`21bbb37`): GetAsyncKeyState binding, the PeekMessageA MSG write, the PlaySnd boundary's call site and pushed words.
- **Requested:** Core — pass the call address to `som` (today read from `_fronteira`'s `endereco` argument). Missions — the window harness records `top_callee = null` on every boundary (not compared; counted).

## M3.1 — chain past frame 220, P6 window (2026-10-30)

Merged main `8138e6e` (P6 window `d18add9` on main). The report is [M3_1_CADEIA_ALEM_220.md](M3_1_CADEIA_ALEM_220.md). Commits `656ac96`, `17bb6e9`, `7cc733e`.

- **API:** `provedores_entrada_ia.DonosM3(m, *, som, bonus=None, mensagem_unidade=None)` — one instance each of Core `entrada_estruturas`/`visao_grupos` and Economy `caverna_recrutamento`/`ciclo_trabalho` over one memory, `externo(nome, chamada, regs)` routing every named dependency to its owner (all of EAX..EBP passed), `registros(nome)`; `provedores_vivos(..., donos=)` binds group selection, MiniMapSetPos, tag 0x10 sub 3, tag 0x21, tag 17, EnginSelectPeutEntrer; `construcao_entrada_ia.instalar_donos(m, p, donos, tabelas)` installs the cave body (0x426aff), BatimentIllumine/Decouvre and unit states 5/13; `estado_trabalho` (state 5, 0x456600); `composicao_entrada_ia.mensagem_unidade` (iagUnitSendMessage, non-AI owner).
- **Translated:** CalculIconeAction with a structure selected, IconeFillContenu code 6, the unit hover with a structure selected, BatimentPeutAttaquer's type prefix, unit state 5's dispatch.
- **Native differentials:** 124/116/0 mismatches, 203/203, 90/85/0 mismatches. Domain gate passes.
- **P6 whole state (prova):** part 0 equal through frame 220 (184 phases), then Graphics' AffBatiments logic-effects guard at `between_frames221`. Planning diagnostics (never evidence) reach 2400 at indicator level, P3 to 3129, K1 to 629; whole state (planning) equal 129–2177 in all 4,098 phases, then Economy/Core's minimap divergence at 2178.
- **Stops and owners:** Graphics (AffBatiments for structures other than the Santuario; view origins for K1/P4/P5); Economy/Core (minimap bytes after BatimentHabitable); unassigned (TerrainEstGc object ≥ 0x1d, P7 2801/P4 460); Core (SetMiniMap mode from CalculWorkEngin, P5 760); Combat (turret BatimentPeutAttaquer, BatimentInitAttaqueSelect); Economy (SetDechargeCaveEnginSelect).

## M3.1 — hunger wiring, reach after the minimap fix, S1 by parts (2026-10-30)

Merged main `3e0de77` then `fcc0ba8`. The report is [M3_1_FOME_E_S1.md](M3_1_FOME_E_S1.md). Commit `8b8c984` plus the follow-up.

- **P6 (planning diagnostic, whole state):** 4,544/4,544 phases equal from 129 to 2400; frame 2178 now passes. Chains: `a3f35dfc…`, `5da71fab…`, `c557167f…`. Strict P6/P3/P7 stop at `between_frames221` (Graphics' AffBatiments guard). K1 is equal in strict mode to 629. P4 stops at 460 and P7 (planning) at 2801, both on TerrainEstGc ≥ 0x1d (Core); P5 stops at 760 on SetMiniMap 0x44c437 (Core).
- **API:**
  - `construcao_entrada_ia.ESTADO_19` and `EnginNextEtape:state19` (Economy's `alimentacao.estado_fome`);
  - `instalar_donos` installs `EnginSetFatigue` from `DonosM3.rotina_core`;
  - `DonosM3.fome` / `.fadiga` / `.ordens()`, `_externo_fome`, `rotina_core(nome) -> f(regs, chamada=0)`;
  - `entrada_quadro_ia.terrain_get_sac_type(m, regs)`;
  - `provar_entrada_janelas_ia.py fixar | tudo --partes --diagnostico-planejamento | reproduzir`;
  - `provar_entrada_ia.py --diagnostico-planejamento`.
- **S1:** run `fixar S1 --ref origin/feat/re-missions` once the pass-2 capture lands, commit, then `tudo --janelas S1 --lease …`. The expected first stop is EnginRestaureEtat 0x45315f (Economy, at the end of the first meal, about frame 8057), unless Economy lands it first.
- **Open stops and owners:**
  - Graphics: the AffBatiments guard;
  - Core: TerrainEstGc ≥ 0x1d and the SetMiniMap mode at 0x44c437;
  - Economy: EnginRestaureEtat, BatimentEnleveMatiere and SetDechargeCaveEnginSelect;
  - Combat: the turret BatimentPeutAttaquer and BatimentInitAttaqueSelect.
