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
| `consumo_dano.py` | Mode-1 occupied-unit damage consumer, live callbacks and explicit death boundary |
| `impacto_unidades.py` | Mode-1 unit impact wrapper: lookup, reaction requests, consumer, hit allocation, diplomacy and alert requests |
| `bonus_combate.py` | Argument-order adapter from damage's modifier queries to economy's committed loaded-table provider |

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

Callbacks take `(name, arguments_tuple)`. Queries return native integer results; modifiers and predicates are consumed at their original widths. Effects return no value. Callbacks may mutate records **in place** and context fields; replacing record objects, the world base pointer or the damage-row pointer table during a call is outside this adapter's contract. Missing providers raise `NotImplementedError` at their call site; earlier effects are retained.

| Order | Callback or mutation | Width and original site |
|---|---|---|
| 1 | Snapshot source damage row indexed by victim type, add source `+0xF7` | u8 arithmetic, `0x4503B8..0x4503EA` |
| 2 | Query `Modificateur(source_owner, 5, source_type)` | u8 arguments; low result byte added, `0x4503F4` |
| 3 | Query `ChercheTypeEnginProximite(2, source_owner, source_step_cell, 10)`; if AL is nonzero add `bonus_4965ac` | u8/u8/u16/u16; bonus u8, `0x450427..0x45043B` |
| 4 | Effect `iagUnitSendMessage(victim, 0x48, attacker)` | u16/u8/u16, `0x450452`; life is unchanged here |
| 5 | Read victim `+0xF6`, then query `Modificateur(source_owner, 6, source_type)` and reduce damage | u8 arithmetic with signed-negative clamp; **source** fields reread after message, `0x45059C..0x4505D8` |
| 6 | Query `TerrainEstDecouvert(victim_current_cell, local_player)` | u16/u8; AL predicate, `0x450604` |
| 7 | If visible, query `EnginGetVolume(victim)`, snapshot u32 `+0x104`, then clear victim byte `+0xF9` | u16 ID / u32 volume, `0x45060F..0x450624` |
| 8 | If saved handle is `0xFFFFFFFF`, effect `PlaySnd_PostSound(0x50, (victim_type<<16)\|0x100, 0, volume, victim)` | u32 values; final ID represents native `&victim[0x104]`, `0x45063F` |
| 9 | Decrement damage byte when victim `+0xDC` bit 3 is set; compare life u16 with signed damage byte | `0x450644..0x45068B` |
| 10 | Nonlethal: subtract signed damage and store life u16. Death: raise `LimiteMorte` at `0x4506A1` before its first instruction | `0x45068D..0x45069C`; no invented zero-life/death effects |

The proximity callback retains the original French identifier; its name does not establish a captain/type filter. The native path used by these tests checks owner and geometry. Zero damage protected by bit 3 becomes -1 and raises life by one with u16 wrap. The death exception exposes `endereco`, `vitima`, `atacante`, and signed `dano`; message/audio effects already reached remain visible. `None` indicates only the consumer's nonlethal return, not completion of the world impact wrapper.

The connected scenario uses original `ProjectileAvance` → `ProjectileInfligeDegat` → `InfligeDegat` → `EnginInfligeDegat`, with a type-9 arrival, mode 1, an occupied target, and four direction bytes. The harness captures the original selected victim and consumer arguments, resumes to `0x450DA5` immediately after the consumer returns, and compares all 220,800 unit bytes plus all 5,600 projectile bytes with the callback-connected Python path at that same checkpoint. The fixture's world callback supplies that captured victim; Python does **not** implement the cell wrapper's lookup, retaliation/evasion, diplomacy, visual hit effects or continuation. The parent is still active and no RNG has been consumed at this checkpoint. This is a supported impact-to-life-loss slice, not a complete impact/battle.

Original input remains `RISING.EXE` SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`. New immutable-byte extracts and individual range hashes are in [the consumer evidence manifest](../pesquisas-paralelas/combate/evidencias/consumo-dano.json). Predecessor extracts and saved historical reports were not regenerated.

`ConsultaBonusCombate(bonus, outras=None)` now connects this consumer to economy's committed `BonusUnidades` provider (implementation `b1eb0c06e3b016f9abc2d27f3a836f6c20abf2f9`). Pass it as the consumer's query callable. It maps `Modificateur(owner, selector, type)` to `bonus.consultar(owner, type, selector)`, preserves the provider's full return width, and forwards other queries unchanged to `outras(name,args)`. Only damage selectors 5/6 are supported; absent providers, other selectors and absent forwarded queries raise at the call site. No zero table, bonus, or inherited-ECX default is manufactured. Selector 5 reads u16 at loaded record `+0x08`; selector 6 reads u8 at `+0x0A`; the damage caller consumes their low bytes. Economy owns the loaded 1,872-byte table and its initialization remains separate.

The corrected native fixture now writes those exact fields, with explicit requested-value assertions. A separate [provider-composition report](../pesquisas-paralelas/combate/validacao-bonus-combate-emulada.json) records 450 complete original consumers against the **actual committed economy query results**, including word/high-byte boundaries and all 4×26 loaded owner/type combinations. Other native query results remain explicit inputs. The same run also reruns consumer/wrapper tests under corrected bonus inputs; predecessor reports remain unchanged as historical records of their earlier fixture values.

## Unit impact wrapper

`ImpactoUnidades.infligir(cell, mode, attacker, direction, flag)` now reconstructs the **mode-1 unit branch** of `InfligeDegat` (`0x450874..0x4510DD`). Cell/attacker truncate to u16; mode/direction/flag to u8. Mode must be 1, attacker 0..799, the live table must have 800 records, and resolved unit types must be 0..25. `receber(name, args)` connects directly to `PoolProjeteis.efeito_externo` for `InfligeDegat`; other effect names stop explicitly. Supply the same live unit table, projectile pool and callable unit consumer, normally `ConsumidorDanoUnidade.infligir`.

Queries/effects use `(name, arguments_tuple)`. Lookup is external: flag zero first queries `ChercheIndiceBatiment(cell:u16)` and a non-FFFF result raises `LimiteImpactoBatiment` at `0x4508AF`; nonzero flag skips that query. The unit query is `ChercheIndiceEnginCible(cell:u16, excluded:u16=FFFF, flag:u8)`. FFFF is an empty impact. Unit IDs outside 0..799 fail before record access. Queries may already have had effects when such a returned ID is rejected.

The wrapper snapshots victim owner/type before reacting. Owner 200 bypasses reaction. Other owners query `PlayerGetType(owner:u8)`. Human states 5/18 query `ChercheBatimentProximiteCaveOuSanctuaire(current_cell:u16, owner:u8)`, then optionally `BatimentGetCase(building:u16)` and effect `SetDeplaceEngin(victim:u16, cell:u16)`. Eligible retaliation checks type, protection bit 1, source type and owner, then repeats the original player-type queries. Human retaliation requests `SetAttaqueEngin(victim:u16, mode:u8=1, attacker:u16)` for state 7 or unsigned wrapped elapsed counter **>250**. AI retaliation requests it only in state 7. Other reactions query `CalculDirection(source_step:u16, victim_step:u16)`, then `CalculDirCase(reread_victim_step:u16, direction:u8)` and request movement if the cell is not FFFF. Navigation implementation belongs to core.

The unit consumer runs next with `(victim:u16, mode:u8=1, attacker:u16, direction:u8)`. Its exception propagates; later effects do not run. After return, the wrapper uses the **saved** victim type to allocate hit projectiles in the live pool. Types 0/1/2, 4..10 and 18..24 allocate type 14. Types 11..17 query `Random(marker:u32=0x22)` even when the pool is full, then allocate type `15+(result&1)`; only victim type 16 sets height flag 1. Types 3/25 allocate none. Hit origin and destination both use the original impact cell; mode, attacker, direction and offsets are zero. The [original seven-entry hit table](../pesquisas-paralelas/combate/evidencias/impacto-unidades.json) sends all types 11..17 to this RNG path.

After hit allocation, source owner is captured again. Query `PlayerEstAllie(source_owner:u8, live_victim_owner:u8)` conditionally emits, in order, `MAJSympathie(live_victim_owner, saved_source_owner, 10)`, the same with 6, `PlayerResetAllie(saved_source_owner, live_victim_owner)` and its reverse. Each owner argument is reread at its original call site. `PlayerAAttaqueSet(saved_source_owner, live_victim_owner)` always follows. These are effect requests, not implementations of their world bodies.

For a different-owner victim owned by the local player, alert throttling uses u32 `contador` and `ultimo_alerta`: a counter reset/wrap (`previous>now`) or elapsed **>=200** updates `ultimo_alerta` and u16 `celula_alerta` before emitting `PlaySnd_PostSound(0x50, (live_victim_type<<16)|0x700, 0, 0x100, '0x496ac8')`. The string token represents the original alert-context pointer, distinct from a unit's sound handle. Missing providers preserve all earlier life, pool, alert and callback effects. This wrapper never moves units itself.

The reference suite finishes five type-9 occupied impacts, including consumer life loss, hit allocation/RNG, diplomacy requests and parent retirement; all 220,800 unit bytes and 5,600 pool bytes match. Its world queries execute original code. Navigation/refuge/audio entries are explicit native stops. The full allied-order fixture executes original inactive `MAJSympathie` returns and `PlayerResetAllie` with a nonparticipating local player; Python still delegates those bodies. No real mission, AI message body, lethal effect, building damage, other damage mode or whole battle is established by those fixtures.

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
python3 -B scripts/check.py --domain combat
```

The slices' actual results and expected dependency stops are recorded in [the combat handoff](../pesquisas-paralelas/combate/HANDOFF.md) and their `validacao-consumo-dano-*.json` / `validacao-impacto-unidades-*.json` reports. AI message bodies and audio/death backends remain external. Further work can add other damage modes and lethal effects, and trace `+0x8A=2/3` producers.
