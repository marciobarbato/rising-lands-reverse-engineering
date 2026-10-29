# Combat research contract

Owner: combat. Source and tests live in `pesquisas-paralelas/combate/`. Shared damage, reload, movement, and task primitives remain in `ferramentas/`; changes there belong to core and require a contract handoff.

## Supported pipeline

| Module | Responsibility |
|---|---|
| `alvos_alcance.py` | Alliances/enemies, scan/grid target selection, adjacency, range, line of fire, weapon readiness, local order/maintenance effects |
| `mira_angular.py` | Target-cell resolution, `AngleCalcul`, `EnginViseCible`, and 8/32-sector quantization |
| `animacao_disparo.py` | Attack substates 0/1/2/3, animation advance, orientation, firing requests |
| `inicializacao_ataque.py` | Type characteristics, mission/game post-load attack fields, persistence audit |
| `projeteis.py` | 100-record pool, initialization, integer line preparation/calculation |
| `reinicio_projeteis.py` | `ProjectileReset` entry for the mission reset prefixes and the other three original callers |
| `ataque_vivo.py` | `SetAttaqueEngin`, the dispatcher's state-1/24 branch and the shared-world chain into pool, `ProjectileCalcul`, impact, damage and physical death |
| `avanco_projeteis.py` | Linear advance, logical animation, arrival, RNG, damage requests and secondary effects |
| `maquina_projeteis.py` | Supported full advancement/expiration dispatcher, types 30/33, and live-pool `Calcul` passes |
| `cadencia_projeteis.py` | Original caller gates, accumulated-counter input, and impact presentation preparation |
| `consumo_dano.py` | Initialized mode-1/3/4/8/9 unit damage with explicit loaded inputs and death boundaries |
| `fonte_batiment.py` | Read-only mode-3 building-source queries over Core's public structure pool and explicit loaded damage rows |
| `impacto_unidades.py` | Mode-1/3/4 unit impact wrapper: lookup, mode-specific source/reaction/diplomacy, consumer and hit allocation |
| `bonus_combate.py` | Argument-order adapter from damage's modifier queries to economy's committed loaded-table provider |
| `morte_dano.py` | Optional mode-1 lethal tail: local experience/life writes, child allocation and explicit level/lifecycle/sympathy requests |
| `consumo_fisico.py` | Opt-in shared-pool connection from damage/death sequencing to Core's committed physical dying provider |
| `alvos_impacto.py` | Read-only impact-victim selection with original ground/elevated tie rules, reusable as a unit-wrapper query |
| `grade_impacto.py` | Read-only building-ID selection from the loaded region grid, preserving building-before-unit priority |
| `proximidade_ataque.py` | Read-only radius-10 owner proximity query for the damage consumer, with explicit loaded grid inputs |

Input units use raw 276-byte records. Callbacks must describe external world effects explicitly; receiving a resolved query or stopping at a dependency is a narrower claim than executing the complete caller. Whole-record/grid comparisons distinguish local copies from mutations of the live world.

## Targeting and aiming

`TypeEnginPeutAttaquer` is at `0x453D7D`, `EnginTrouveCibleScan` at `0x453DA2`, and `EnginTrouveCible` at `0x453F74`. Scan returns the first eligible ID; grid selection uses its original spatial traversal and distance/tie order, including special handling of types 2/8. Do not replace both with an unconstrained nearest-enemy search.

Owner alliances are directional (`PlayerEstAllie`, `0x46D838`). Adjacency uses type-specific occupied cells (`0x44246E`, `0x4468E4`, `0x446B0C`). `EnginAPortee` (`0x446CB5`) includes modes 1/3/5 and explicit building/magic geometry callbacks; the minimum range excludes squared distance ≤4 for type 16. Line-of-fire reconstruction is tied to `0x4517A2` and its sign-step traversal.

Aiming resolves target cells and quantizes the original angular result. Body, type-3 behavior, and turret paths are distinct. A query for required orientation does not itself rotate a live unit. The tests compare original x87 calls in the supported input domain; they do not claim bitwise equivalence of every x87 intermediate.

## Attack states and projectile effects

Attack substate 0 prepares, aims, and waits for readiness; 1 animates and emits at its marked frame; 2 waits/revalidates; 3 ends the local order. Retain exact original sequencing, counter widths, and dependency calls. Do not infer transitions from an attractive animation sequence.

`+0x8A=2/3` has no producer in the executable. Every unit writer stores 0 or 1. The only register-valued one, `0x452A3A mov [esi+0x8a],ah`, is reached solely by `je` at `0x452469` after `mov ah,[esi+0x8b]; test ah,ah`, so it stores 0. The earlier by-byte dword hits in hangar/turret/structure code are `66`-prefixed word stores to structure records at `0x49A0C8`, and the `iagRessReset` hit is an AI resource record. No unit routine contains `rep movs/stos`, and the table `memset` callers fill with zero. 2/3 can therefore enter only through `FileRead` loaders of external bytes (mission ETA, saved games); none of the 2,604 ETA records holds them. Native runs of the Stage 18 chain observed only 0/1 writes, from `0x445AB3`, `0x445AD1`, `0x451E08` and `0x452A3A`. Network receive buffers and arbitrary pointer aliasing are not covered by this static trace ([evidence](../pesquisas-paralelas/combate/evidencias/ataque-vivo.json)). The audit also tracks `+0x79`, `+0x7A`, and `+0x8B`.

Type-4 initialization has an important provider boundary: `caracterizar_tipo` calls modifier 12 before writing `+0x7A=5`, then stores `+0xDA=(modifier+10)&255`. Original call `0x457845`, frame store `0x45784C`, amount store `0x457850` establish that order. A failed modifier leaves the inherited frame intact and the earlier common `+0xDA=1` intact. The corrected order also applies through `definir_tipo` and mission postload, including writable memoryviews of the live table. Owners 4/200 bypass the Python modifier callback as before. The [focused reference report](../pesquisas-paralelas/combate/validacao-ordem-tipo4-emulada.json) records 108 expected modifier-entry stops and 18 successful original returns; no phase transitions or other type behavior were added.

The projectile pool and dispatcher preserve fixed-width arithmetic, allocation behavior, line increments, creation/arrival order, expiration, and RNG consumption. Type 30's circular effects and type 33's old-target child/new-target damage behavior require their own paths. `Calcul` processes the live pool in 30 passes; a snapshot iteration can change newly allocated record behavior.

Damage distribution produces requests and invokes declared callbacks. Building, unit, magic, sound, message, and navigation effects must remain explicit. Original effect-edge conditions are not automatically interchangeable with linear-motion bounds. Tests using synthetic 1×1/3×3 building geometry do not establish all real building footprints.

## Live attack chain from the unit dispatcher

`ataque_vivo.py` holds the three combat entries that ai-runtime's dispatcher skeleton calls (contract recorded in [AI and runtime](AI_RUNTIME.md)):

| Entry | Original | Inputs |
|---|---|---|
| `definir_ataque(unidades, indice, modo, referencia, redefinir_ordem)` / `AtaqueVivo.definir_ataque` | `SetAttaqueEngin 0x445A36`: AX unit, DL mode, BX reference | u16/u8/u16; `redefinir_ordem` is Core `ResetOrdre 0x44357C` |
| `ramo_estado_ataque(ctx, indice, consultar, efetuar)` / `AtaqueVivo.ramo(indice)` | `EnginNextEtape` states 1/24, `0x456886..0x4568AD`, exit `0x454CCD`: ESI record, DI index | u16 unit; return ignored |
| `AtaqueVivo.calcular_projeteis()` | `ProjectileCalcul 0x46FC0F`, no register input | low byte of `AtaqueVivo.contador` (u32 `0x508F7C`) |

`SetAttaqueEngin` returns before `ResetOrdre` when the same order is active (state 1, same `+0xB7`, same `+0xB8`). Every other call resets the order first. Only then does it refuse types 5/6/7/9/10/13, modes other than 1/3/5 and a mode-1 self target, so refused calls still reset. Accepted orders store `+2=1`, `+0x8A=0`, `+0xB7=mode` and u16 `+0xB8=reference`.

The branch switches on target mode `+0xB7` (1 unit, 3 structure, 5 cell); `+0x8A` is the separate attack substate.
- **Mode 1:** valid when the reference is not `0xFFFF`, the target state is not 0/4, the target owner is not 200 and target `+0x72` is nonzero.
- **Mode 3:** asks `BatimentEnDestruction` (structure `+5 == 3`) and then `BatimentGetPlayer` (≠200).
- **Mode 5:** needs no check.
- **Valid order:** runs one `CalculAttaqueEngin` step.
- **Invalid order:** queries `PlayerGetType(owner)`. An AI owner (2; every owner ≥4) gets `iagUnitSendMessage(unit, 0x4A, 0)`. Otherwise it requests `SetDeplaceEngin(unit, u16 +0x7E)` and then stores `+0xB8=0xFFFF`.
- **Other modes:** they reach `CalculAttaqueEngin` untranslated and raise before any effect.
- **Mode-1 references ≥800:** they raise `IndexError` (the original would read past the 800-record table).

The branch reads nothing from the prelude's stack frame.

`AtaqueVivo(mundo, pool, danos, tipos, bonus, mascaras, *, bonus_4965ac, ultimo_alerta, celula_alerta, consulta=None, efeito=None)` shares, by reference:
- Core's world and the live `PoolProjeteis`.
- 26 loaded DEGAT rows and the loaded 26×50 type table (reload at `+0x30`).
- Economy's loaded bonus provider (`BonusUnidades.consultar` for `Modificateur` 3/4/5/6).
- Five alliance mask bytes (players 0..4, byte `+6`).
- The u8 global `0x4965AC` and the inherited alert globals `0x4E19C0`/`0x496ACC` (Stage 17: these persist across loads).

Internally it routes:

| Request | Destination |
|---|---|
| `ProjectileInit` | `pool.iniciar` |
| `InfligeDegat` (melee and projectile arrival) | `ImpactoUnidades` |
| Wrapper retaliation `SetAttaqueEngin` | `definir_ataque` |
| `SetDeplaceEngin` / `ResetOrdre` | Core `definir_movimento` / `redefinir_ordem` |
| The damage consumer | `criar_consumidor_fisico` with both lethal tails |
| `SetDyingEngin` | Core physical death |

Read-only bridges cover:
- `PlayerGetType 0x46D817`: the control byte for owners 0..3, otherwise 2.
- `BatimentEnDestruction 0x41A70B` and `BatimentGetPlayer 0x41A08C` over the 1000-record structure pool.
- `PlayerEstAllie`, the computed building/unit lookups, proximity and visibility, all over the live grids.

Every other request goes to `consulta`/`efeito`, or raises `DependenciaAtaqueVivo(nome, argumentos)` with the original entry address: AI messages, `EnginGetVolume`/`PlaySnd_PostSound`, `MAJSympathie`/`PlayerResetAllie`/`PlayerAAttaqueSet`, `EnginSetLevelExperience 0x44FB20`, `DeplaceEngin`, `Random`, building geometry, spells and terrain effects. Earlier effects are retained. The object takes over the pool's `efeito_externo`/`raio_magia`.

The reload advance `0x454530..0x454591` belongs to the dispatcher prelude (ai-runtime places it; Core supplies `avancar_recarga`). The validation chain runs the prelude head `0x45442C..0x454591` natively only as a declared fragment.

[Original-only captures](../pesquisas-paralelas/combate/evidencias/captura-ataque-vivo-original.json) preceded the Python composition: 25 scenarios, 1,208 native segments, every one ending at its declared return or stop with zero writes outside the modeled areas.
- **Inputs:** real loaded type and DEGAT tables rebuilt by Core's `regras` from the original `RISING.EXE`/`RISING.INI`; units created with the committed `EnginSetType` translation. The map, positions, owners, life, zero bonus table, players and discovery bytes, order fields and the frame counter are declared synthetic. Core's MONDE01 placement is not yet a composed loaded world, and MONDE01's 16 serialized units all belong to owner 0.
- **Frame driver:** each frame sets the counter, runs `ProjectileCalcul`, then the prelude head and branch for every unit in state 1/24 in live index order.
- **Complete chains:** neutral monsters (owner 200; types 18–24 skip the mode-1 experience award) fight a human SOLDADO under a non-participating local player.
  - ESMAGADOR melee: 220 frames.
  - ARAIGNEE ranged (projectile 17): 114 frames.
  - Both cover emission, flight, impact, damage, retaliation, the victim's own invalid branch, physical death and the attacker's final invalid-target branch, ending at the named AI-message stop `0x4567A9`.
- **Named stops in the same chain:** `PlayerAAttaqueSet` (AI attacker owner 1), `EnginGetVolume` (visible attacker) and `EnginSetLevelExperience` (SOLDADO killer).
- **Single entries:** eleven branch cases (every validity outcome, the mode-3 `CalculAttaqueEngin` checkpoint, a mode-5 `DeplaceEngin` stop) and nine `SetAttaqueEngin` cases.

## Mission reset prefix: projectile pool

`reinicio_projeteis.resetar_projeteis(pool)` reconstructs complete `ProjectileReset` `[0x46E00A,0x46E02C)` (34 bytes, SHA-256 `9941723e…1e71`, no CALL). Pass the live 5,600-byte allocation that the original reaches through dword `0x5080F0`: a `bytearray`, or a writable C-contiguous one-dimensional `B`/`b` memoryview (for example a slice of a larger arena); `PoolProjeteis.resetar()` delegates to it with `.memoria`. Shape is validated before the first store, so a rejected buffer keeps every byte. The original would fault on an unmapped pointer; it never allocates, frees or reinitializes the pool (`ProjectileAlloc 0x46DFA0` allocates `0x15E0` bytes once from `ProgInit 0x474ED7`).

| Order | Effect | Width |
|---|---|---|
| 1..100 | Reread pointer `[0x5080F0]`, then store zero at `pool + 56*i + 2` for `i = 0..99` | u8 |
| return | `EAX = 0x64`; EBX/EDX pushed and restored; ECX/ESI/EDI/EBP untouched; flags from `cmp 0x64,0x64` (ZF/PF set, CF/AF/SF/OF clear, DF kept) | — |

No register or stack argument is read. The other 55 bytes of each record, every global and every unit field stay inherited. The function returns `0x64` (`EAX_RETORNO`). Stack scratch (`[esp-4]=EBX`, `[esp-8]=EDX`, below the CALL return address) is native-only and not modeled.

The four direct callers (`CHAMADAS`) are `MissionReStart 0x46B5AC`, `GameLoad 0x46B8C1`, `MissionLoad 0x46C373` and `MissionLoadName 0x46C623`; no absolute pointer to the routine exists. In every one, the call follows `EnginResetAll 0x441659` and precedes `MessageBoxInit 0x469908`, after the u16 `0xFFFF` stores to `0x4E1A38/0x4E1A3A` and `IconeReset`, `TerrainReset`, `MiniMapReset`, `BatimentResetAll`. Only `MissionLoad` adds `BallonInit 0x441B6C` before `FileOpen`. EAX=0x64 is dead at all four sites: `MessageBoxInit` zeroes AL/AH and indexes by AX. Missions owns that composition order; this entry supplies only the combat step.

**No other combat state is reset in the prefix.** `EnginResetAll` writes Bag words, `+2`, `+0x9A` and `+0xAF` of nonzero-state units; attack fields `+0x79`, `+0x7A`, `+0x8A`, `+0x8B`, `+0xDA` and the target fields stay inherited until `LoadEngin` and the committed postload. An executable-wide displacement scan finds the alert counter `0x4E19C0` and alert cell `0x496ACC` written only by `InfligeDegat` and `TryLanceAttaqueSound`, the presentation byte `0x4DFB44` only by building/projectile/flip routines, and the pool pointer only by `ProjectileAlloc`. These values persist across mission loads. The [inventory](../pesquisas-paralelas/combate/evidencias/reinicio-projeteis.json) records bytes, hashes, caller contexts and those references. The other prefix routines also store through runtime pointers (terrain layers at `0x507D74..0x507DAC`, minimap buffers from `0x507D5C`); their reach is established only by missions' whole-prefix native equality, which this stage does not run.

[Original-only captures](../pesquisas-paralelas/combate/evidencias/captura-reinicio-projeteis-original.json), taken before the Python entry, run 16 seeded dirty states: random pools at region start/end/unaligned/high addresses, `+2` values covering 0..255, all-`0xFF`, already clear, all-zero, and one entry through each original CALL. The [reference report](../pesquisas-paralelas/combate/validacao-reinicio-projeteis-emulada.json) adds 60 fresh dirty states. All 76 compare the complete 2 MiB image with poisoned DGROUP/.bss (`0x494000..0x523000`), the unit area, stack, both pool regions, registers and EFLAGS against the Python prediction; 52 enter through original CALL instructions.


`ConsumidorDanoUnidade.infligir(victim, mode, attacker, direction=0)` reconstructs the mode-1 path of `EnginInfligeDegat` at `0x4502F0`, returning through `0x45084F..0x450855` for nonlethal results. It reuses core's committed `dano_bruto_unidade`, `reduzir_dano`, and `aplicar_dano_parcial` arithmetic. Provide 800 live mutable 276-byte records and 26 damage rows with at least 26 u8 entries each. IDs truncate to u16 and must then be 0..799; mode truncates to u8 and must be 1; source and victim types must be 0..25. Direction is unused by this mode. Unsupported modes, IDs or types fail before callbacks or local writes.

The constructor also accepts 27 explicit damage rows for mode 8 below. Mode 1 still uses only the first 26 rows; supplying the optional row does not change its callbacks or arithmetic.

Callbacks take `(name, arguments_tuple)`. Queries return native integer results; modifiers and predicates are consumed at their original widths. Effects return no value. Callbacks may mutate records **in place** and context fields; replacing record objects, the world base pointer or the damage-row pointer table during a call is outside this adapter's contract. Missing providers raise `NotImplementedError` at their call site; earlier effects are retained.

| Order | Callback or mutation | Width and original site |
|---|---|---|
| 1 | Snapshot source damage row indexed by victim type, add source `+0xF7` | u8 arithmetic, `0x4503B8..0x4503EA` |
| 2 | Query `Modificateur(source_owner, 5, source_type)` | u8 arguments; low result byte added, `0x4503F4` |
| 3 | Query `ChercheTypeEnginProximite(2, source_owner, source_step_cell, 10)`; if AL is nonzero add `bonus_4965ac` | ignored type/u8/u16/u32 constant 10; bonus u8, `0x450427..0x45043B` |
| 4 | Effect `iagUnitSendMessage(victim, 0x48, attacker)` | u16/u8/u16, `0x450452`; life is unchanged here |
| 5 | Read victim `+0xF6`, then query `Modificateur(source_owner, 6, source_type)` and reduce damage | u8 arithmetic with signed-negative clamp; **source** fields reread after message, `0x45059C..0x4505D8` |
| 6 | Query `TerrainEstDecouvert(victim_current_cell, local_player)` | u16/u8; AL predicate, `0x450604` |
| 7 | If visible, query `EnginGetVolume(victim)`, snapshot u32 `+0x104`, then clear victim byte `+0xF9` | u16 ID / u32 volume, `0x45060F..0x450624` |
| 8 | If saved handle is `0xFFFFFFFF`, effect `PlaySnd_PostSound(0x50, (victim_type<<16)\|0x100, 0, volume, victim)` | u32 values; final ID represents native `&victim[0x104]`, `0x45063F` |
| 9 | Decrement damage byte when victim `+0xDC` bit 3 is set; compare life u16 with signed damage byte | `0x450644..0x45068B` |
| 10 | Nonlethal: subtract signed damage and store life u16. Death: default `LimiteMorte` at `0x4506A1`, or explicit optional handler below | `0x45068D..0x45069C`; the default does not invent death effects |

The proximity callback retains the original French identifier; its name does not establish a captain/type filter. The native path used by these tests checks owner and geometry. Zero damage protected by bit 3 becomes -1 and raises life by one with u16 wrap. The death exception exposes `endereco`, `vitima`, `atacante`, and signed `dano`; message/audio effects already reached remain visible. `None` indicates only the consumer's nonlethal return, not completion of the world impact wrapper.

The connected scenario uses original `ProjectileAvance` → `ProjectileInfligeDegat` → `InfligeDegat` → `EnginInfligeDegat`, with a type-9 arrival, mode 1, an occupied target, and four direction bytes. The harness captures the original selected victim and consumer arguments, resumes to `0x450DA5` immediately after the consumer returns, and compares all 220,800 unit bytes plus all 5,600 projectile bytes with the callback-connected Python path at that same checkpoint. The fixture's world callback supplies that captured victim; Python does **not** implement the cell wrapper's lookup, retaliation/evasion, diplomacy, visual hit effects or continuation. The parent is still active and no RNG has been consumed at this checkpoint. This is a supported impact-to-life-loss slice, not a complete impact/battle.

Original input remains `RISING.EXE` SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`. New immutable-byte extracts and individual range hashes are in [the consumer evidence manifest](../pesquisas-paralelas/combate/evidencias/consumo-dano.json). Predecessor extracts and saved historical reports were not regenerated.

`ConsultaBonusCombate(bonus, outras=None)` now connects this consumer to economy's committed `BonusUnidades` provider (implementation `b1eb0c06e3b016f9abc2d27f3a836f6c20abf2f9`). Pass it as the consumer's query callable. It maps `Modificateur(owner, selector, type)` to `bonus.consultar(owner, type, selector)`, preserves the provider's full return width, and forwards other queries unchanged to `outras(name,args)`. Only damage selectors 5/6 are supported; absent providers, other selectors and absent forwarded queries raise at the call site. No zero table, bonus, or inherited-ECX default is manufactured. Selector 5 reads u16 at loaded record `+0x08`; selector 6 reads u8 at `+0x0A`; the damage caller consumes their low bytes. Economy owns the loaded 1,872-byte table and its initialization remains separate.

The corrected native fixture now writes those exact fields, with explicit requested-value assertions. A separate [provider-composition report](../pesquisas-paralelas/combate/validacao-bonus-combate-emulada.json) records 450 complete original consumers against the **actual committed economy query results**, including word/high-byte boundaries and all 4×26 loaded owner/type combinations. Other native query results remain explicit inputs. The same run also reruns consumer/wrapper tests under corrected bonus inputs; predecessor reports remain unchanged as historical records of their earlier fixture values.

The fixed consumer proximity query can now use `ConsultaProximidadeAtaque(units, grid, outras=None)`, supporting exactly `(2, owner, cell, 10)` and forwarding other query names. `proximidade_dono_ataque(units, grid, owner, cell)` takes 800 readable 276-byte records and exactly 131,072 loaded little-endian grid bytes; owner/cell truncate to u8/u16. It scans the clipped ±10 square in original row-major order, recognizes only grid words with `(word & C000)==4000`, decodes `(word & 3FF8)>>3`, checks owner equality, then accepts squared distance ≤100. It reads no type, activity, enabled or alliance field. The original EAX desired-type argument is unused; radius ECX is consumed as u32 and only the caller's constant 10 is reconstructed here. Unit IDs outside 0..799 in an inspected unit-tagged cell are explicitly unsupported and raise before access. All other radii/caller domains remain unsupported; no default grid is created.

The [proximity report](../pesquisas-paralelas/combate/validacao-proximidade-ataque-emulada.json) contains 636 complete original AL-return comparisons and five complete damage consumers using computed proximity and the real economy provider. Grid/unit buffers remain unchanged by the query. The type/state independence, boundary circle and owner equality are directly exercised against original instructions; this does not reconstruct grid placement or mission loading.

## Special-row damage mode 8

The same `infligir(victim,8,source,direction=0)` API supports the initialized mode-8 nonlethal path. Supply **27** explicit rows, each with at least 26 u8 entries. The original prefix `[0x450475,0x450494)` reads damage-pointer table entry 26 (`+0x68`) indexed by victim type. This path adds no source `+0xF7`, requests no modifier 5/proximity, and sends no mode-1 AI message. It then performs the shared victim-F6/source-modifier-6 reduction, visibility/volume/optional sound, protection-bit decrement and signed-damage/u16-life rules. Source ID/type are still required because the original computes its record pointer and common modifier 6 reads it. Input widths and live callback restrictions are unchanged.

Missing row 26 fails before callbacks/writes. Every mode-8 lethal result raises `LimiteMorte` at `0x4506A1`, preserving life and prior audio effects; `exception.modo` is 8. A configured mode-1 `morte` handler is never called for this mode, including through `criar_consumidor_fisico`. Its original prefix does not initialize the saved owner byte at stack `+0x28` later read for sympathy, so the mode-1 death tail cannot be substituted. General mode-8 lethal/caller semantics and the loaded row's game meaning remain open. The additional supported modes 9, 4 and 3 are described below; modes 0/2/5/6/7 and other values still fail explicitly. The cell wrapper supports modes 1/3/4, with mode 4 restricted to directions 29/30 and mode 3 requiring its separate source-cell/owner callbacks.

The [mode-8 reference report](../pesquisas-paralelas/combate/validacao-dano-modo8-emulada.json) records **27 tests / 2,110 original-x86 executions** with no failures/errors/skips: 1,101 complete mode-8 returns, 139 expected mode-8 death stops, four expected mode-8 audio stops, and 866 rerun mode-1 consumer/physical-composition calls. Tests cover all 26×26 source/victim types, real loaded economy modifier-6 results, signed-byte boundaries, life/protection wrap, ID edges/aliasing and visible handles. Whole unit buffers match; the loaded bonus table is unchanged. Original mode-1 reports and evidence were preserved.

## Life-derived damage mode 9

`infligir(victim,9,source,direction=0)` implements original `[0x450494,0x4504C6)`: raw damage is `((entry_life_u16//2)&255) or 1`, followed by the same reduction/visibility/life tail as mode 8. Byte truncation precedes the zero test and common signed clamp. For example, life 255 loses 127 with zero reductions, but life 256 loses 1 because raw byte 128 is negative at the common clamp; life 512 also loses 1 because its raw byte is zero before replacement. The constructor still requires the ordinary 26-row input domain (or 27 rows), although mode 9 does not read a damage row. IDs/types and common query widths remain unchanged. There is no mode-1 F7/modifier-5/proximity/message prefix, and direction is unused.

The original mode-9 prefix does not initialize the saved sympathy owner either. Every lethal result raises `LimiteMorte` with `modo=9` before life zero, preserving prior effects and ignoring any mode-1 lethal handler. No mode-9 cell-wrapper/projectile caller, death completion or game meaning is claimed. The [dedicated reference report](../pesquisas-paralelas/combate/validacao-dano-modo9-emulada.json) records **33 tests / 4,506 original-x86 calls**: 2,359 complete mode-9 returns, 33 expected mode-9 death stops, four expected mode-9 audio stops, and 2,110 mode-8/mode-1 regressions. Every raw byte value and its even/odd life input is checked in four life bands; reduction/protection edges, source types, ID aliases and visible handles also match whole unit/loaded-bonus buffers. Historical reports remain unchanged.

## Loaded-byte damage mode 4

`infligir(victim,4,source,direction)` supports only direction bytes 29 and 30. Supply `danos_modo4=(loaded_u8_at_49716C,loaded_u8_at_49716E)` when constructing the consumer, or set that field to the same explicit two-byte loaded state before calling. The pair remains live; it is not copied or defaulted. Constructor values must be two u8 entries. Missing values or another direction fail before callbacks/writes. Direction truncates to u8 as in the original.

The original prefix `[0x4504C6,0x450588)` selects the appropriate loaded byte. Its [26-entry table](../pesquisas-paralelas/combate/evidencias/dano-modo4-tabela.json) assigns class 2 to victim types 3/11/12/13/14/15/16/25 and class 1 otherwise. Class 2 replaces the selected signed byte by division by four, truncating toward zero, then stores the resulting low byte. Common F6/modifier-6 reduction, negative clamp, visibility/audio and life/protection logic follow. Thus raw 255 in class 2 becomes zero before reduction; raw 128 becomes signed -32 and later follows the common clamp. No F7/modifier-5/proximity/message prefix is added. The original saves source owner before common reduction. By default lethal damage stops at `LimiteMorte(modo=4)` before life zero; the separate opt-in tail below skips mode-1 experience awards.

The [initial reference report](../pesquisas-paralelas/combate/validacao-dano-modo4-emulada.json) records **40 tests / 6,354 original-x86 calls**: 1,580 complete mode-4 consumers, 264 expected mode-4 death stops, four expected mode-4 audio stops, and 4,506 mode-9/8/1 regressions. All 26 victim classes, both loaded bytes, every raw byte in both classes, signed division/reduction/protection/life edges, ID aliases and visible handles match whole unit/loaded-bonus buffers. The new original-hash-grounded table extract preserves previous evidence. Other directions can consume uninitialized raw damage and remain unsupported. This initial report covered the nonlethal path and boundaries; later physical composition is described below. No world caller or game meaning is inferred.

## Building-source damage mode 3

`infligir(victim,3,source,direction=0)` implements `[0x450377,0x4503B8)`: save victim type; query `BatimentGetType(source:u16)`; query `TypeBatimentGetDegat(type:u8,1,saved_victim_type:u8)`; query `BatimentGetPlayer(source:u16)`; emit `iagUnitSendMessage(victim:u16,0x4C,source:u16)`; then enter common reduction/visibility/life logic. Type, raw damage and saved building owner consume only the low result byte. No source F7, modifier 5 or proximity bonus is added. Direction is unused. The shared consumer requires source/victim IDs 0..799 and unit types 0..25 even though a building ID is also supplied: the original common modifier 6 still reads **unit[source]** owner/type. It must not substitute building owner/type. By default lethal damage stops at `LimiteMorte(modo=3)` before life zero; the separate opt-in tail below skips mode-1 experience awards.

`ConsultaFonteBatiment(structures,damage_type10,damage_type11,outras=None)` supplies the three source queries. Core's public flat pool has 1000×276 bytes; record type is byte +8, owner byte +4. Getter IDs truncate to u16 and require 0..999. The bridge returns the AL values consumed by this caller; full EAX in original record getters retains address bits and is deliberately not emulated. Source queries read live supplied buffers without copying/mutating them. Both damage rows must contain at least 26 explicitly loaded u8 entries: selector 1/type 10 reads original row `0x4DFB80`, type 11 row `0x4DFB64`, every other source type returns zero. Victim type requires 0..25. Other selectors fail explicitly; other query names delegate unchanged or fail. Both owning chats confirmed no existing generic public provider and approved reading these committed public inputs.

The [dedicated reference report](../pesquisas-paralelas/combate/validacao-dano-modo3-emulada.json) records **47 tests / 8,010 original-x86 calls**: 606 complete source-query calls, 889 complete mode-3 consumers, 157 expected mode-3 death stops, four mode-3 audio stops, and 6,354 mode-4/9/8/1 regressions. All 22 building types and 26 victim types, loaded rows, source-ID overlap, reduction/life/protection and visible handles are covered. Full unit/structure buffers and unchanged bonus/damage rows match. Original message executes its human-control early return; general AI/audio/lifecycle/world-caller bodies remain external. [New focused source evidence](../pesquisas-paralelas/combate/evidencias/dano-modo3.json) preserves original bytes/hash and prior reports. This is a unit damage target with a building source, distinct from `InfligeDegat`'s building target branch.

## Optional lethal sequencing

The default `LimiteMorte` is unchanged. To opt in, set `consumer.morte = MorteDanoUnidade(units, pool, efeito)`. The internal handoff is `(victim:u16, attacker:u16, signed_damage:s8, saved_entry_step_cell:u16, saved_source_owner:u8)`. The cell is captured at consumer entry (`0x45033F`), and the source owner after the AI message (`0x45046C`), before reduction/visibility callbacks. The handler does not subtract damage again and supports this mode-1 handoff only.

The original tail at `0x4506A1..0x45084F` reads the live source type. For source types 0..10 or 25 it clears the low five bits of `+0xAF`, then requests `EnginSetLevelExperience(attacker:u16, (old_AF>>5)+1:u8)` before zeroing victim life. All 256 AF bytes select that request in this domain; any level clamp belongs to its provider. If it fails, AF is already masked and victim life remains unchanged. After success or for other source types, victim `+0x9A` is set to u16 zero. Live victim type 1 attempts a type-6 child in the live pool at the saved entry cell (origin=destination, all other arguments zero). `SetDyingEngin(victim:u16)` follows. Core owns that physical state/lifecycle body; a missing provider leaves life zero and any child allocated, without retiring the calling projectile.

After the physical provider returns, the handler rereads victim owner/type and requests `MAJSympathie(live_victim_owner:u8, saved_source_owner:u8, flag:u32)`, with flag 1 for type 3 or 11..17, otherwise 0. These effect callbacks use `(name,args_tuple)` and may mutate records in place; no level, physical lifecycle or sympathy body is silently implemented by this handler. A successful callback chain returns `None`. The first sequencing validation stopped at those external bodies; the opt-in shared-world adapter below now composes the committed Core physical provider in its supported domain.

The [lethal reference report](../pesquisas-paralelas/combate/validacao-morte-dano-emulada.json) records 268 level-entry stops, 24 dying-entry stops, 104 separately executed original suffix fragments with synthetic post-provider inputs, and one occupied projectile reaching the physical dying request. The suffix starts at `0x4507AF` as a declared separate fragment; no lifecycle CALL or return is patched/skipped. Whole unit/pool buffers match at the connected boundaries, including full pools and a message callback changing the victim step after the old step was saved. These checks validate local sequencing and requests, not world removal, dying animation, AI effects or audio.

Modes 3/4 can separately opt into `consumer.morte_sem_experiencia = handler.sem_experiencia`. This callback has the same five handoff arguments: victim/source u16, signed damage, entry-saved step cell u16, saved source owner u8. Original dispatch at `0x4506A1` skips the award branch when mode is not 1. `sem_experiencia` therefore performs life zero, optional type-6 child, physical request and live-field sympathy in the same order, without reading/writing source AF or requesting a level. Mode 3 uses building owner saved before its message; mode 4 uses unit owner saved before modifier 6. Modes 8/9 never invoke this callback because their saved owner is undefined. The existing mode-1 `morte` field retains its domain, and both opt-ins default to `None` in the plain consumer.

## Shared-world physical lethal composition

`criar_consumidor_fisico(mundo,pool,danos,consulta=None,efeito=None,bonus_4965ac=0,mortes_sem_experiencia=False)` returns an opt-in `ConsumidorDanoUnidade`. The Core world must expose a writable 220,800-byte `unidades` bytearray, `jogador_local` and `iniciar_morte_unidade(index)`. The factory makes 800 writable 276-byte memoryviews over that exact buffer; `consumer.unidades` can also be passed to `ImpactoUnidades` or the read-only query adapters. Damage rows, projectile pool and callbacks retain their existing contracts. The consumer initially copies the world's local camera ID; callers changing camera between calls must also update `consumer.jogador_local`. Replacing/resizing the world/pool or record objects during callbacks is unsupported. The new flag explicitly enables the separate mode-3/4 tail; its default preserves earlier stops. Mode-4 loaded values still require the consumer's `danos_modo4` input, and mode-3 source queries still require their explicit bridge.

Only the lethal `SetDyingEngin(victim:u16)` request is routed to `mundo.iniciar_morte_unidade`. Other effects still use the supplied callback or fail explicitly. Core provider commit `913a4ada5bb931e276d57f606b12c5858efc36da` owns [physical death](core/PHYSICAL_DYING.md): state/search release, local reset and current/reserved collision removal, with explicit unresolved branches. Combat writes life zero and attempts the victim-type-1 child before invoking that provider. A `DependenciaMorteUnidade` propagates unchanged, retaining all prior combat and physical writes. Retrying the entry after a partial failure is not continuation.

The [new reference report](../pesquisas-paralelas/combate/validacao-consumo-fisico-emulada.json) records **103 original-x86 executions**: 46 complete consumers, four complete type-9 projectile arrivals, 42 sympathy-entry stops and 11 physical dependency stops. Every call executes the original consumer and actual `SetDyingEngin` in one native world; no separate suffix or skipped CALL is used. Complete fixtures choose source type 12 (no level request), ordinary hidden victims, empty Bag, no selection, null sound/group handles, and original inactive sympathy flags at `0x51A990+16*owner`. The fixture external sympathy callback represents only that declared original early return. General diplomacy/message/audio/level bodies remain unresolved. Projectile wrapper queries beyond computed victim lookup are observed fixture inputs; diplomacy/statistic effects remain compared requests rather than new production providers.

Comparisons include all 220,800 unit bytes, all 5,600 projectile bytes, Core structures/groups/objects, collision/region/terrain grids, search fields, vision/light/minimap/shadow buffers and routes. They cover all 19 ordinary victim types, equal/different current/reserved cells, pool saturation and unit IDs 0/799. Expected physical stops cover special bit 2, active sound, nonempty Bag, selection counters and all vehicle types 11..17, preserving prior life/child/cleanup effects. The [focused REA record](../pesquisas-paralelas/combate/evidencias/rea-consumo-fisico.json) retains pinned-source metadata and reviewed entry assembly for the analysis image; its inferred signatures are not authoritative. Execution uses the intact original EXE hash stated above. This is a bounded synthetic-world composition; mission loading, complete lifecycle animation and runtime are still open.

The [mode-3/4 physical reference report](../pesquisas-paralelas/combate/validacao-morte-sem-experiencia-emulada.json) records **59 tests / 8,609 original-x86 calls**: 98 complete mode-3/4 lethal consumers, 82 expected sympathy-entry stops, 22 physical dependency stops, and 8,407 regressions (including the original mode-1 award/lifecycle prefixes and separately declared suffix fragments). Each of the 202 new mode-3/4 cases uses one original native call through actual physical death, with complete world/child-pool comparisons and computed loaded source/bonus queries. Source unit type 0 and unchanged AF prove that modes 3/4 skip awards. Coverage includes all ordinary victims, both mode-4 directions, both building damage types, ID/pool/cell/inactive boundaries and all earlier physical stops. Complete fixtures execute original inactive sympathy returns; Python's external callback represents only that declared fixture guard. Defaults and mode-8/9 stops also have explicit local checks. This initial composition covered direct consumers; the mode-4 wrapper below adds its separate prepared caller domain. General sympathy/audio/AI/special death remains external.

## Unit impact wrapper

`encontrar_estrutura_impacto(grid,cell)` supplies original `ChercheIndiceBatiment` at `[0x41B54A,0x41B579)`. The explicit grid contains 65,536 little-endian u16 words (131,072 bytes), and cell truncates to u16. Bit 15 set returns `(word & 0x7FE0)>>5`; otherwise the full result is `0xFFFF`. No structure record, footprint, owner or activity is consulted. IDs 1000..1023 remain valid query outputs even though they exceed Core's 1000-record allocation. This query does not dereference them. Low five bits are ignored, and grid memory is unchanged.

`ConsultaGradeImpacto(grid,outras=None)` handles only `ChercheIndiceBatiment(cell)` and delegates other queries unchanged, or raises without a provider. Compose `ConsultaAlvosImpacto(units, ConsultaGradeImpacto(grid, remaining_queries))` to compute both impact lookups. Grid views are read on each call without copying; callers construct/update the loaded grid. A flag-zero impact still takes the building stop before consulting any unit, including when both representations name an occupant. This provider does not implement the building damage branch.

The [focused grid-lookup report](../pesquisas-paralelas/combate/validacao-grade-impacto-emulada.json) records **4,120 original-x86 executions**: 4,110 complete queries, five expected building stops, and five complete nonlethal projectile arrivals using computed building and unit lookups. Query coverage includes all 1024 encoded IDs with four low-bit patterns, nonbuilding tags and cell-width edges; full result EAX, preserved EDX and unchanged grid/unit bytes match. Connected impacts preserve building priority and last-ground-victim selection. Their other world queries/effects remain declared observed fixture inputs/requests.

`ImpactoUnidades.infligir(cell, mode, attacker, direction, flag)` reconstructs the **mode-1/3/4 unit branches** of `InfligeDegat` (`0x450874..0x4510DD`). Cell/attacker truncate to u16; mode/direction/flag to u8. Mode must be 1, 3 or 4, with direction 29/30 required for 4; attacker is 0..799, the live table has 800 records, and resolved unit types are 0..25. `receber(name, args)` connects directly to `PoolProjeteis.efeito_externo` for `InfligeDegat`; other effect names stop explicitly. Supply the same live unit table, projectile pool and callable unit consumer, normally `ConsumidorDanoUnidade.infligir`.

Queries/effects use `(name, arguments_tuple)`. Lookup is external: flag zero first queries `ChercheIndiceBatiment(cell:u16)` and a non-FFFF result raises `LimiteImpactoBatiment` at `0x4508AF`; nonzero flag skips that query. The unit query is `ChercheIndiceEnginCible(cell:u16, excluded:u16=FFFF, flag:u8)`. FFFF is an empty impact. Unit IDs outside 0..799 fail before record access. Queries may already have had effects when such a returned ID is rejected.

The wrapper snapshots victim owner/type before reacting. Owner 200 bypasses reaction. Other owners query `PlayerGetType(owner:u8)`. Human states 5/18 query `ChercheBatimentProximiteCaveOuSanctuaire(current_cell:u16, owner:u8)`, then optionally `BatimentGetCase(building:u16)` and effect `SetDeplaceEngin(victim:u16, cell:u16)`. Eligible retaliation requires mode 1, type, protection bit 1, source type and owner, then repeats the original player-type queries. Human retaliation requests `SetAttaqueEngin(victim:u16, mode:u8=1, attacker:u16)` for state 7 or unsigned wrapped elapsed counter **>250**. AI retaliation requests it only in state 7. Remaining mode-1 reactions query `CalculDirection(source_step:u16, victim_step:u16)`, then `CalculDirCase(reread_victim_step:u16, direction:u8)` and request movement if the cell is not FFFF. Mode 4 instead uses literal origin cell **zero**; mode 3 requests `BatimentGetCase(attacker:u16)` and consumes its low u16 for evasion origin. Neither uses mode-1 retaliation. The earlier refuge/neutral bypass still applies. `BatimentGetCase` and navigation bodies remain external unless supplied by their owners.

The unit consumer runs next with `(victim:u16, mode:u8=1, attacker:u16, direction:u8)`. Its exception propagates; later effects do not run. After return, the wrapper uses the **saved** victim type to allocate hit projectiles in the live pool. Types 0/1/2, 4..10 and 18..24 allocate type 14. Types 11..17 query `Random(marker:u32=0x22)` even when the pool is full, then allocate type `15+(result&1)`; only victim type 16 sets height flag 1. Types 3/25 allocate none. Hit origin and destination both use the original impact cell; mode, attacker, direction and offsets are zero. The [original seven-entry hit table](../pesquisas-paralelas/combate/evidencias/impacto-unidades.json) sends all types 11..17 to this RNG path.

After hit allocation, source owner is captured again: from the live unit record in modes 1/4, or query `BatimentGetPlayer(attacker:u16)` in mode 3. Query `PlayerEstAllie(source_owner:u8, live_victim_owner:u8)` conditionally emits, in order, `MAJSympathie(live_victim_owner, saved_source_owner, 10)`, the same with 6, `PlayerResetAllie(saved_source_owner, live_victim_owner)` and its reverse. Each target-owner argument is reread at its original call site. `PlayerAAttaqueSet(saved_source_owner, live_victim_owner)` always follows. Mode 3 returns there and has no unit alert block. These are effect requests, not implementations of their general world bodies.

For modes 1/4 with a different-owner victim owned by the local player, alert throttling uses u32 `contador` and `ultimo_alerta`: a counter reset/wrap (`previous>now`) or elapsed **>=200** updates `ultimo_alerta` and u16 `celula_alerta` before emitting `PlaySnd_PostSound(0x50, (live_victim_type<<16)|0x700, 0, 0x100, '0x496ac8')`. The string token represents the original alert-context pointer, distinct from a unit's sound handle. Missing providers preserve all earlier life, pool, alert and callback effects. This wrapper never moves units itself.

The reference suite finishes five type-9 occupied impacts, including consumer life loss, hit allocation/RNG, diplomacy requests and parent retirement; all 220,800 unit bytes and 5,600 pool bytes match. Its world queries execute original code. Navigation/refuge/audio entries are explicit native stops. The full allied-order fixture executes original inactive `MAJSympathie` returns and `PlayerResetAllie` with a nonparticipating local player; Python still delegates those bodies. No real mission, AI message body, lethal effect, building damage, other damage mode or whole battle is established by those fixtures.

The unit lookup is now available as `encontrar_vitima_impacto(units, cell, excluded=FFFF, flag=0)`, reconstructing `ChercheIndiceEnginCible` (`0x4465DF..0x446693`, range hash `f3a9bd57f2fd9dfe18e7db9a992250068e0cd3754c14af65a62a940b262b81b3`). It requires exactly 800 readable 276-byte records; cell/excluded truncate to u16 and flag to u8. IDs scan 0..799, skipping the excluded ID, state 0/4 and `+0x72=0`. Combat's existing `ocupa_celula` handles state 14, current/step cells, type-specific geometry and stratum filtering: flag zero uses filter 1, every nonzero byte uses filter 2. Interpreted live types require the established 0..25 domain; inactive bytes need not describe a valid type.

Each matching ground record (`+0xAB=0`) replaces the candidate, so the **last** matching ID is returned; a matching elevated record (`+0xAB!=0`) returns immediately, so the **first** matching ID is returned. FFFF means no victim. The full EAX result contains that u16 ID with high bits zero. No owner, alliance, life, distance, navigation or grid filter is added. The function writes no state and must receive a stable view for the duration of its callback-free scan. `ConsultaAlvosImpacto(units, outras=None)` answers `ChercheIndiceEnginCible` and delegates every other query; a missing delegate raises explicitly. Building lookup and all world effects remain separate.

The [selection report](../pesquisas-paralelas/combate/validacao-alvos-impacto-emulada.json) contains 376 complete original lookup returns and five complete occupied projectile impacts using **computed** selection, not a replayed native victim ID. Overlapping ground candidates prove unit 799 receives damage while unit 1 remains unchanged. Whole unit/pool buffers match, and standalone lookup leaves all 220,800 unit bytes unchanged. These remain synthetic world fixtures, not mission/runtime tests.

The [mode-4 caller report](../pesquisas-paralelas/combate/validacao-impacto-modo4-emulada.json) records **78 tests / 8,818 original-x86 calls**. New coverage includes 104 complete neutral-victim wrappers across every type, both strata and initialized directions; five expected building/death/evasion/refuge stops; two complete shared-world cell impacts; four complete prepared type-29 arrivals; a later building stop after central physical death; and two shared-world navigation/refuge stops. The remaining 8,700 calls rerun initialized consumer, lethal, shared-world and mode-1 wrapper scopes. Native calls are unpatched. Computed building/unit lookup follows the live world after each impact, and all Core physical buffers plus all 5,600 projectile bytes match.

The type-29 fixtures start with explicit phase 12 and zero remaining line length. Original `ProjectileAvance`/`ProjectileInfligeDegat` deliver mode 4 with direction 29, then create arrival effects and retire the parent. The full/partial fixtures compare **38 ordered impact requests and 36 original RNG returns**, including failed child allocation in a full pool. RNG values remain explicit observed external inputs to the Python caller, not a new generator implementation. Neutral owner 200, null AI group, hidden ordinary units and original owner-range sympathy/statistic guards define the complete fixture domain; other world queries/effects remain declared inputs/requests. A building at the first neighbor stops before building damage while retaining the central zero-life/physical cleanup/hit allocation and active parent, before arrival RNG. Mode 3's separate source-cell/owner requests are validated below. Mode 8/9 evasion may consume an undefined origin and remains unsupported. No natural mission dispatch, general navigation/diplomacy/audio/AI or complete battle is established.

The [mode-3 caller report](../pesquisas-paralelas/combate/validacao-impacto-modo3-emulada.json) records **86 tests / 8,936 original-x86 calls**: 104 complete neutral-victim wrappers across all types/strata and both source building types, five wrapper stops (building target, default death, source-cell and two refuge), three complete shared-world cell impacts, four complete prepared type-1 arrivals, two shared-world source-cell/refuge stops, and 8,818 prior caller/consumer regressions. Full physical/unit/structure/projectile buffers match. The four projectile arrivals compare four original impact requests and four observed RNG returns, including full child-pool allocation failure and parent retirement. `BatimentGetCase` still stops at its original entry when no provider is supplied.

Mode-3 neutral fixtures execute the exact original message-`0x4C` null-group guard `[0x482DB6,0x482DBE)` and existing epilogue. [Focused guard evidence](../pesquisas-paralelas/combate/evidencias/impacto-modo3.json) records original bytes/hash and dispatch-table target; the common prefix through `0x482A51` alone is not a null-group return. Active group/message bodies remain external. One explicitly synthetic data mutation at the message boundary changes building owner 3→2. Original execution and Python both retain saved owner 3 for consumer sympathy, re-query owner 2 for wrapper diplomacy, and use unit owner 0 for modifier 6. This proves read timing for mutable callback state; it does not claim the original null-group message performs that mutation. General world effects and natural mission dispatch remain open.

## Caller cadence and rendering boundary

Three distinct gates occur after menu return (`0x42D14C`), event handling (`0x42D2E3`), and players/commands with a reread state (`0x42D3C0`). Projectile calculation precedes units in the traced caller. Preserve the low byte of the accumulated counter passed into logical animation; do not replace it with an arbitrary frame number or wall-clock delta.

The consumer of `0x4DFB44` prepares a vertical presentation displacement and draw rectangle. A simulation counter, impact geometry, and graphical presentation are separate contracts. Graphics owns sprite/palette mapping; combat owns the observed state/caller arithmetic.

## Validation and next work

```sh
python3 -B pesquisas-paralelas/combate/validar.py
python3 -B pesquisas-paralelas/combate/validar.py --emular
```

The saved emulated result records 113 tests and 234,245 bounded original-x86 executions. Local-only execution explicitly skips optional differential cases. Harnesses, original-byte extracts, dispatch tables, field/cadence audits, and data tables stay in this domain's `evidencias/`. Use a worktree because the validation entry point writes its own report.

The current Stage 19 [building-target inventory](../pesquisas-paralelas/combate/CONTRACT_BUILDING_DAMAGE.md) is static readiness only: original damage arithmetic, destruction stores and explicit dependency boundaries, plus the future type-10/11 turret contract. Its new byte exports are not runtime validation or a public provider. The bounded Stage 18 attack chain is already integrated. The human's later steering ends this recovery turn after the light inventory; native captures, translation, heavy gates and integration were not run. Unknown AI/audio/diplomacy effects and real mission behavior remain open.

The occupied-unit consumer has its own bounded validator, so it does not overwrite the historical 234,245-execution report:

```sh
python3 -B pesquisas-paralelas/combate/rastrear_consumo_dano.py
python3 -B pesquisas-paralelas/combate/validar_consumo_dano.py
python3 -B pesquisas-paralelas/combate/validar_consumo_dano.py --emular
python3 -B pesquisas-paralelas/combate/validar_impacto_unidades.py --emular
python3 -B pesquisas-paralelas/combate/validar_ordem_tipo4.py --emular
python3 -B pesquisas-paralelas/combate/validar_bonus_combate.py --emular
python3 -B pesquisas-paralelas/combate/validar_morte_dano.py --emular
python3 -B pesquisas-paralelas/combate/validar_alvos_impacto.py --emular
python3 -B pesquisas-paralelas/combate/validar_proximidade_ataque.py --emular
python3 -B pesquisas-paralelas/combate/validar_consumo_fisico.py --emular
python3 -B pesquisas-paralelas/combate/validar_grade_impacto.py --emular
python3 -B pesquisas-paralelas/combate/validar_dano_modo8.py --emular
python3 -B pesquisas-paralelas/combate/validar_dano_modo9.py --emular
python3 -B pesquisas-paralelas/combate/rastrear_dano_modo4.py
python3 -B pesquisas-paralelas/combate/validar_dano_modo4.py --emular
python3 -B pesquisas-paralelas/combate/rastrear_dano_modo3.py
python3 -B pesquisas-paralelas/combate/validar_dano_modo3.py --emular
python3 -B pesquisas-paralelas/combate/validar_morte_sem_experiencia.py --emular
python3 -B pesquisas-paralelas/combate/validar_impacto_modo4.py --emular
python3 -B pesquisas-paralelas/combate/rastrear_impacto_modo3.py
python3 -B pesquisas-paralelas/combate/validar_impacto_modo3.py --emular
python3 -B pesquisas-paralelas/combate/rastrear_reinicio_projeteis.py
python3 -B pesquisas-paralelas/combate/validar_reinicio_projeteis.py --emular
python3 -B pesquisas-paralelas/combate/rastrear_ataque_vivo.py
python3 -B pesquisas-paralelas/combate/capturar_ataque_vivo.py
python3 -B pesquisas-paralelas/combate/validar_ataque_vivo.py --emular
python3 -B scripts/check.py --domain combat
```

The slices' actual results and expected dependency stops are recorded in [the combat handoff](../pesquisas-paralelas/combate/HANDOFF.md) and their dedicated reports. General AI message, audio, level and diplomacy bodies remain external. The shared-world adapter delegates supported physical death to Core; special/vehicle effects remain explicit stops. The Stage 18 field audit above supersedes the older open producer inventory. Building-target behavior and natural MONDE01 runtime remain separate unimplemented work.

M2 slice 1 captures the frame body's combat-relevant calls natively from the accepted M1 post-load state. `PlayerAttaqueReset 0x46d628` is a single `ret`. `PlayerAttaqueCalculSympa 0x46d629` is diplomacy, a periodic (`counter % 2000`) attack-matrix consumer owned outside Combat. `ProjectileCalcul` over the empty M1 pool clears the 100 stale `+1` fill bytes in its first pass; `MaquinaProjeteis.calcular` now matches that store trace. Run:

```bash
python3 -B pesquisas-paralelas/combate/capturar_quadro_m1.py
RISING_EMULAR=1 python3 -B -m unittest discover -s pesquisas-paralelas/combate -p test_quadro_m1.py
```

M2.1 round 2 revalidates those calls at the exact frame-0 and frame-1 inputs of Missions' first-frame path. It uses isolated native calls, `captura-isolada-combate-quadro1.json`. Frame 0 (the load-state pass) reaches `ProjectileCalcul` (the 100 `+1` clears), `EnginTrouveCible` for unit 0 (no target) and 7 `PlayerEstAllie` calls. Frame 1 reaches only an empty projectile pass. `PlayerEstAllie 0x46d838` is `alvos_alcance.aliados(AL origin, DL target, masks)`, where `masks[p]` is byte `[[0x5080a8] + 20·p + 6]`. Its native register contract (ECX preserved, DL = `1 << target` on the in-range path) is in `test_quadro1_combate.py`.

M2.3 preparation locates MONDE01's first scripted raid statically. `AvanceMonstre 0x47b283`'s EntrerMonstre record 0 (cell `0x3f3f`, group 0, period 9000) fires at counter 9000 and calls `ConstruitGroupeMonstre`. A forced-counter native capture (`captura-incursao-m2-3-original.json`) shows that the raid frame's Combat calls are only the spawn effect (`ProjectileInit` type 31/32) and the following projectile pass. Both match the existing Python (`test_incursao_m2_3.py`). The order is a posted AI task, so no attack or damage is reached in that frame. Details and cross-front contracts are in the combat handoff.
