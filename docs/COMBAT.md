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
| `avanco_projeteis.py` | Linear advance, logical animation, arrival, RNG, damage requests and secondary effects |
| `maquina_projeteis.py` | Supported full advancement/expiration dispatcher, types 30/33, and live-pool `Calcul` passes |
| `cadencia_projeteis.py` | Original caller gates, accumulated-counter input, and impact presentation preparation |
| `consumo_dano.py` | Initialized mode-1/4/8/9 unit damage with explicit loaded inputs and death boundaries |
| `impacto_unidades.py` | Mode-1 unit impact wrapper: lookup, reaction requests, consumer, hit allocation, diplomacy and alert requests |
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

The origin of `+0x8A=2/3` remains unproven: direct writes found by the audit use 0/1, and none of the 2,604 records in 38 ETA maps contain 2/3. Loaders can preserve externally supplied values; this neither proves those phases impossible nor licenses inventing their producer. The audit also tracks `+0x79`, `+0x7A`, and `+0x8B`.

Type-4 initialization has an important provider boundary: `caracterizar_tipo` calls modifier 12 before writing `+0x7A=5`, then stores `+0xDA=(modifier+10)&255`. Original call `0x457845`, frame store `0x45784C`, amount store `0x457850` establish that order. A failed modifier leaves the inherited frame intact and the earlier common `+0xDA=1` intact. The corrected order also applies through `definir_tipo` and mission postload, including writable memoryviews of the live table. Owners 4/200 bypass the Python modifier callback as before. The [focused reference report](../pesquisas-paralelas/combate/validacao-ordem-tipo4-emulada.json) records 108 expected modifier-entry stops and 18 successful original returns; no phase transitions or other type behavior were added.

The projectile pool and dispatcher preserve fixed-width arithmetic, allocation behavior, line increments, creation/arrival order, expiration, and RNG consumption. Type 30's circular effects and type 33's old-target child/new-target damage behavior require their own paths. `Calcul` processes the live pool in 30 passes; a snapshot iteration can change newly allocated record behavior.

Damage distribution produces requests and invokes declared callbacks. Building, unit, magic, sound, message, and navigation effects must remain explicit. Original effect-edge conditions are not automatically interchangeable with linear-motion bounds. Tests using synthetic 1×1/3×3 building geometry do not establish all real building footprints.

## Occupied-unit damage consumer

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

Missing row 26 fails before callbacks/writes. Every mode-8 lethal result raises `LimiteMorte` at `0x4506A1`, preserving life and prior audio effects; `exception.modo` is 8. A configured mode-1 `morte` handler is never called for this mode, including through `criar_consumidor_fisico`. Its original prefix does not initialize the saved owner byte at stack `+0x28` later read for sympathy, so the mode-1 death tail cannot be substituted. General mode-8 lethal/caller semantics and the loaded row's game meaning remain open. The additional supported modes 9 and 4 are described below; other modes fail explicitly, and `ImpactoUnidades` still accepts only mode 1.

The [mode-8 reference report](../pesquisas-paralelas/combate/validacao-dano-modo8-emulada.json) records **27 tests / 2,110 original-x86 executions** with no failures/errors/skips: 1,101 complete mode-8 returns, 139 expected mode-8 death stops, four expected mode-8 audio stops, and 866 rerun mode-1 consumer/physical-composition calls. Tests cover all 26×26 source/victim types, real loaded economy modifier-6 results, signed-byte boundaries, life/protection wrap, ID edges/aliasing and visible handles. Whole unit buffers match; the loaded bonus table is unchanged. Original mode-1 reports and evidence were preserved.

## Life-derived damage mode 9

`infligir(victim,9,source,direction=0)` implements original `[0x450494,0x4504C6)`: raw damage is `((entry_life_u16//2)&255) or 1`, followed by the same reduction/visibility/life tail as mode 8. Byte truncation precedes the zero test and common signed clamp. For example, life 255 loses 127 with zero reductions, but life 256 loses 1 because raw byte 128 is negative at the common clamp; life 512 also loses 1 because its raw byte is zero before replacement. The constructor still requires the ordinary 26-row input domain (or 27 rows), although mode 9 does not read a damage row. IDs/types and common query widths remain unchanged. There is no mode-1 F7/modifier-5/proximity/message prefix, and direction is unused.

The original mode-9 prefix does not initialize the saved sympathy owner either. Every lethal result raises `LimiteMorte` with `modo=9` before life zero, preserving prior effects and ignoring any mode-1 lethal handler. No mode-9 cell-wrapper/projectile caller, death completion or game meaning is claimed. The [dedicated reference report](../pesquisas-paralelas/combate/validacao-dano-modo9-emulada.json) records **33 tests / 4,506 original-x86 calls**: 2,359 complete mode-9 returns, 33 expected mode-9 death stops, four expected mode-9 audio stops, and 2,110 mode-8/mode-1 regressions. Every raw byte value and its even/odd life input is checked in four life bands; reduction/protection edges, source types, ID aliases and visible handles also match whole unit/loaded-bonus buffers. Historical reports remain unchanged.

## Loaded-byte damage mode 4

`infligir(victim,4,source,direction)` supports only direction bytes 29 and 30. Supply `danos_modo4=(loaded_u8_at_49716C,loaded_u8_at_49716E)` when constructing the consumer, or set that field to the same explicit two-byte loaded state before calling. The pair remains live; it is not copied or defaulted. Constructor values must be two u8 entries. Missing values or another direction fail before callbacks/writes. Direction truncates to u8 as in the original.

The original prefix `[0x4504C6,0x450588)` selects the appropriate loaded byte. Its [26-entry table](../pesquisas-paralelas/combate/evidencias/dano-modo4-tabela.json) assigns class 2 to victim types 3/11/12/13/14/15/16/25 and class 1 otherwise. Class 2 replaces the selected signed byte by division by four, truncating toward zero, then stores the resulting low byte. Common F6/modifier-6 reduction, negative clamp, visibility/audio and life/protection logic follow. Thus raw 255 in class 2 becomes zero before reduction; raw 128 becomes signed -32 and later follows the common clamp. No F7/modifier-5/proximity/message prefix is added. The original saves source owner before common reduction, but mode-4 lethal handling remains an explicit `LimiteMorte(modo=4)` before life zero; the mode-1 handler is not invoked.

The [dedicated reference report](../pesquisas-paralelas/combate/validacao-dano-modo4-emulada.json) records **40 tests / 6,354 original-x86 calls**: 1,580 complete mode-4 consumers, 264 expected mode-4 death stops, four expected mode-4 audio stops, and 4,506 mode-9/8/1 regressions. All 26 victim classes, both loaded bytes, every raw byte in both classes, signed division/reduction/protection/life edges, ID aliases and visible handles match whole unit/loaded-bonus buffers. The new original-hash-grounded table extract preserves previous evidence. Other directions can consume uninitialized raw damage and remain unsupported; no world caller, game meaning or complete mode-4 lethal path is claimed.

## Optional lethal sequencing

The default `LimiteMorte` is unchanged. To opt in, set `consumer.morte = MorteDanoUnidade(units, pool, efeito)`. The internal handoff is `(victim:u16, attacker:u16, signed_damage:s8, saved_entry_step_cell:u16, saved_source_owner:u8)`. The cell is captured at consumer entry (`0x45033F`), and the source owner after the AI message (`0x45046C`), before reduction/visibility callbacks. The handler does not subtract damage again and supports this mode-1 handoff only.

The original tail at `0x4506A1..0x45084F` reads the live source type. For source types 0..10 or 25 it clears the low five bits of `+0xAF`, then requests `EnginSetLevelExperience(attacker:u16, (old_AF>>5)+1:u8)` before zeroing victim life. All 256 AF bytes select that request in this domain; any level clamp belongs to its provider. If it fails, AF is already masked and victim life remains unchanged. After success or for other source types, victim `+0x9A` is set to u16 zero. Live victim type 1 attempts a type-6 child in the live pool at the saved entry cell (origin=destination, all other arguments zero). `SetDyingEngin(victim:u16)` follows. Core owns that physical state/lifecycle body; a missing provider leaves life zero and any child allocated, without retiring the calling projectile.

After the physical provider returns, the handler rereads victim owner/type and requests `MAJSympathie(live_victim_owner:u8, saved_source_owner:u8, flag:u32)`, with flag 1 for type 3 or 11..17, otherwise 0. These effect callbacks use `(name,args_tuple)` and may mutate records in place; no level, physical lifecycle or sympathy body is silently implemented by this handler. A successful callback chain returns `None`. The first sequencing validation stopped at those external bodies; the opt-in shared-world adapter below now composes the committed Core physical provider in its supported domain.

The [lethal reference report](../pesquisas-paralelas/combate/validacao-morte-dano-emulada.json) records 268 level-entry stops, 24 dying-entry stops, 104 separately executed original suffix fragments with synthetic post-provider inputs, and one occupied projectile reaching the physical dying request. The suffix starts at `0x4507AF` as a declared separate fragment; no lifecycle CALL or return is patched/skipped. Whole unit/pool buffers match at the connected boundaries, including full pools and a message callback changing the victim step after the old step was saved. These checks validate local sequencing and requests, not world removal, dying animation, AI effects or audio.

## Shared-world physical lethal composition

`criar_consumidor_fisico(mundo,pool,danos,consulta=None,efeito=None,bonus_4965ac=0)` returns an opt-in `ConsumidorDanoUnidade`. The Core world must expose a writable 220,800-byte `unidades` bytearray, `jogador_local` and `iniciar_morte_unidade(index)`. The factory makes 800 writable 276-byte memoryviews over that exact buffer; `consumer.unidades` can also be passed to `ImpactoUnidades` or the read-only query adapters. Damage rows, projectile pool and callbacks retain their existing contracts. The consumer initially copies the world's local camera ID; callers changing camera between calls must also update `consumer.jogador_local`. Replacing/resizing the world/pool or record objects during callbacks is unsupported.

Only the lethal `SetDyingEngin(victim:u16)` request is routed to `mundo.iniciar_morte_unidade`. Other effects still use the supplied callback or fail explicitly. Core provider commit `913a4ada5bb931e276d57f606b12c5858efc36da` owns [physical death](core/PHYSICAL_DYING.md): state/search release, local reset and current/reserved collision removal, with explicit unresolved branches. Combat writes life zero and attempts the victim-type-1 child before invoking that provider. A `DependenciaMorteUnidade` propagates unchanged, retaining all prior combat and physical writes. Retrying the entry after a partial failure is not continuation.

The [new reference report](../pesquisas-paralelas/combate/validacao-consumo-fisico-emulada.json) records **103 original-x86 executions**: 46 complete consumers, four complete type-9 projectile arrivals, 42 sympathy-entry stops and 11 physical dependency stops. Every call executes the original consumer and actual `SetDyingEngin` in one native world; no separate suffix or skipped CALL is used. Complete fixtures choose source type 12 (no level request), ordinary hidden victims, empty Bag, no selection, null sound/group handles, and original inactive sympathy flags at `0x51A990+16*owner`. The fixture external sympathy callback represents only that declared original early return. General diplomacy/message/audio/level bodies remain unresolved. Projectile wrapper queries beyond computed victim lookup are observed fixture inputs; diplomacy/statistic effects remain compared requests rather than new production providers.

Comparisons include all 220,800 unit bytes, all 5,600 projectile bytes, Core structures/groups/objects, collision/region/terrain grids, search fields, vision/light/minimap/shadow buffers and routes. They cover all 19 ordinary victim types, equal/different current/reserved cells, pool saturation and unit IDs 0/799. Expected physical stops cover special bit 2, active sound, nonempty Bag, selection counters and all vehicle types 11..17, preserving prior life/child/cleanup effects. The [focused REA record](../pesquisas-paralelas/combate/evidencias/rea-consumo-fisico.json) retains pinned-source metadata and reviewed entry assembly for the analysis image; its inferred signatures are not authoritative. Execution uses the intact original EXE hash stated above. This is a bounded synthetic-world composition; mission loading, complete lifecycle animation and runtime are still open.

## Unit impact wrapper

`encontrar_estrutura_impacto(grid,cell)` supplies original `ChercheIndiceBatiment` at `[0x41B54A,0x41B579)`. The explicit grid contains 65,536 little-endian u16 words (131,072 bytes), and cell truncates to u16. Bit 15 set returns `(word & 0x7FE0)>>5`; otherwise the full result is `0xFFFF`. No structure record, footprint, owner or activity is consulted. IDs 1000..1023 remain valid query outputs even though they exceed Core's 1000-record allocation. This query does not dereference them. Low five bits are ignored, and grid memory is unchanged.

`ConsultaGradeImpacto(grid,outras=None)` handles only `ChercheIndiceBatiment(cell)` and delegates other queries unchanged, or raises without a provider. Compose `ConsultaAlvosImpacto(units, ConsultaGradeImpacto(grid, remaining_queries))` to compute both impact lookups. Grid views are read on each call without copying; callers construct/update the loaded grid. A flag-zero impact still takes the building stop before consulting any unit, including when both representations name an occupant. This provider does not implement the building damage branch.

The [focused grid-lookup report](../pesquisas-paralelas/combate/validacao-grade-impacto-emulada.json) records **4,120 original-x86 executions**: 4,110 complete queries, five expected building stops, and five complete nonlethal projectile arrivals using computed building and unit lookups. Query coverage includes all 1024 encoded IDs with four low-bit patterns, nonbuilding tags and cell-width edges; full result EAX, preserved EDX and unchanged grid/unit bytes match. Connected impacts preserve building priority and last-ground-victim selection. Their other world queries/effects remain declared observed fixture inputs/requests.

`ImpactoUnidades.infligir(cell, mode, attacker, direction, flag)` now reconstructs the **mode-1 unit branch** of `InfligeDegat` (`0x450874..0x4510DD`). Cell/attacker truncate to u16; mode/direction/flag to u8. Mode must be 1, attacker 0..799, the live table must have 800 records, and resolved unit types must be 0..25. `receber(name, args)` connects directly to `PoolProjeteis.efeito_externo` for `InfligeDegat`; other effect names stop explicitly. Supply the same live unit table, projectile pool and callable unit consumer, normally `ConsumidorDanoUnidade.infligir`.

Queries/effects use `(name, arguments_tuple)`. Lookup is external: flag zero first queries `ChercheIndiceBatiment(cell:u16)` and a non-FFFF result raises `LimiteImpactoBatiment` at `0x4508AF`; nonzero flag skips that query. The unit query is `ChercheIndiceEnginCible(cell:u16, excluded:u16=FFFF, flag:u8)`. FFFF is an empty impact. Unit IDs outside 0..799 fail before record access. Queries may already have had effects when such a returned ID is rejected.

The wrapper snapshots victim owner/type before reacting. Owner 200 bypasses reaction. Other owners query `PlayerGetType(owner:u8)`. Human states 5/18 query `ChercheBatimentProximiteCaveOuSanctuaire(current_cell:u16, owner:u8)`, then optionally `BatimentGetCase(building:u16)` and effect `SetDeplaceEngin(victim:u16, cell:u16)`. Eligible retaliation checks type, protection bit 1, source type and owner, then repeats the original player-type queries. Human retaliation requests `SetAttaqueEngin(victim:u16, mode:u8=1, attacker:u16)` for state 7 or unsigned wrapped elapsed counter **>250**. AI retaliation requests it only in state 7. Other reactions query `CalculDirection(source_step:u16, victim_step:u16)`, then `CalculDirCase(reread_victim_step:u16, direction:u8)` and request movement if the cell is not FFFF. Navigation implementation belongs to core.

The unit consumer runs next with `(victim:u16, mode:u8=1, attacker:u16, direction:u8)`. Its exception propagates; later effects do not run. After return, the wrapper uses the **saved** victim type to allocate hit projectiles in the live pool. Types 0/1/2, 4..10 and 18..24 allocate type 14. Types 11..17 query `Random(marker:u32=0x22)` even when the pool is full, then allocate type `15+(result&1)`; only victim type 16 sets height flag 1. Types 3/25 allocate none. Hit origin and destination both use the original impact cell; mode, attacker, direction and offsets are zero. The [original seven-entry hit table](../pesquisas-paralelas/combate/evidencias/impacto-unidades.json) sends all types 11..17 to this RNG path.

After hit allocation, source owner is captured again. Query `PlayerEstAllie(source_owner:u8, live_victim_owner:u8)` conditionally emits, in order, `MAJSympathie(live_victim_owner, saved_source_owner, 10)`, the same with 6, `PlayerResetAllie(saved_source_owner, live_victim_owner)` and its reverse. Each owner argument is reread at its original call site. `PlayerAAttaqueSet(saved_source_owner, live_victim_owner)` always follows. These are effect requests, not implementations of their world bodies.

For a different-owner victim owned by the local player, alert throttling uses u32 `contador` and `ultimo_alerta`: a counter reset/wrap (`previous>now`) or elapsed **>=200** updates `ultimo_alerta` and u16 `celula_alerta` before emitting `PlaySnd_PostSound(0x50, (live_victim_type<<16)|0x700, 0, 0x100, '0x496ac8')`. The string token represents the original alert-context pointer, distinct from a unit's sound handle. Missing providers preserve all earlier life, pool, alert and callback effects. This wrapper never moves units itself.

The reference suite finishes five type-9 occupied impacts, including consumer life loss, hit allocation/RNG, diplomacy requests and parent retirement; all 220,800 unit bytes and 5,600 pool bytes match. Its world queries execute original code. Navigation/refuge/audio entries are explicit native stops. The full allied-order fixture executes original inactive `MAJSympathie` returns and `PlayerResetAllie` with a nonparticipating local player; Python still delegates those bodies. No real mission, AI message body, lethal effect, building damage, other damage mode or whole battle is established by those fixtures.

The unit lookup is now available as `encontrar_vitima_impacto(units, cell, excluded=FFFF, flag=0)`, reconstructing `ChercheIndiceEnginCible` (`0x4465DF..0x446693`, range hash `f3a9bd57f2fd9dfe18e7db9a992250068e0cd3754c14af65a62a940b262b81b3`). It requires exactly 800 readable 276-byte records; cell/excluded truncate to u16 and flag to u8. IDs scan 0..799, skipping the excluded ID, state 0/4 and `+0x72=0`. Combat's existing `ocupa_celula` handles state 14, current/step cells, type-specific geometry and stratum filtering: flag zero uses filter 1, every nonzero byte uses filter 2. Interpreted live types require the established 0..25 domain; inactive bytes need not describe a valid type.

Each matching ground record (`+0xAB=0`) replaces the candidate, so the **last** matching ID is returned; a matching elevated record (`+0xAB!=0`) returns immediately, so the **first** matching ID is returned. FFFF means no victim. The full EAX result contains that u16 ID with high bits zero. No owner, alliance, life, distance, navigation or grid filter is added. The function writes no state and must receive a stable view for the duration of its callback-free scan. `ConsultaAlvosImpacto(units, outras=None)` answers `ChercheIndiceEnginCible` and delegates every other query; a missing delegate raises explicitly. Building lookup and all world effects remain separate.

The [selection report](../pesquisas-paralelas/combate/validacao-alvos-impacto-emulada.json) contains 376 complete original lookup returns and five complete occupied projectile impacts using **computed** selection, not a replayed native victim ID. Overlapping ground candidates prove unit 799 receives damage while unit 1 remains unchanged. Whole unit/pool buffers match, and standalone lookup leaves all 220,800 unit bytes unchanged. These remain synthetic world fixtures, not mission/runtime tests.

## Caller cadence and rendering boundary

Three distinct gates occur after menu return (`0x42D14C`), event handling (`0x42D2E3`), and players/commands with a reread state (`0x42D3C0`). Projectile calculation precedes units in the traced caller. Preserve the low byte of the accumulated counter passed into logical animation; do not replace it with an arbitrary frame number or wall-clock delta.

The consumer of `0x4DFB44` prepares a vertical presentation displacement and draw rectangle. A simulation counter, impact geometry, and graphical presentation are separate contracts. Graphics owns sprite/palette mapping; combat owns the observed state/caller arithmetic.

## Validation and next work

```sh
python3 -B pesquisas-paralelas/combate/validar.py
python3 -B pesquisas-paralelas/combate/validar.py --emular
```

The saved emulated result records 113 tests and 234,245 bounded original-x86 executions. Local-only execution explicitly skips optional differential cases. Harnesses, original-byte extracts, dispatch tables, field/cadence audits, and data tables stay in this domain's `evidencias/`. Use a worktree because the validation entry point writes its own report.

The next slice traces missing attack-phase producers and original damage/world consumers, then publishes adapters with explicit effects and one bounded end-to-end supported scenario. It does not silently replace callbacks, import the preview as an oracle, or claim a complete battle from independent routine tests. Publish outstanding core/economy/graphics requests in the combat handoff before integration.

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
python3 -B scripts/check.py --domain combat
```

The slices' actual results and expected dependency stops are recorded in [the combat handoff](../pesquisas-paralelas/combate/HANDOFF.md) and their dedicated reports. General AI message, audio, level and diplomacy bodies remain external. The shared-world adapter delegates supported physical death to Core; special/vehicle effects remain explicit stops. Further work can add other damage modes and lethal effects, and trace `+0x8A=2/3` producers.
