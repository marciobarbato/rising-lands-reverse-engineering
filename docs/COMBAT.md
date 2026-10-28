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

Input units use raw 276-byte records. Callbacks must describe external world effects explicitly; receiving a resolved query or stopping at a dependency is a narrower claim than executing the complete caller. Whole-record/grid comparisons distinguish local copies from mutations of the live world.

## Targeting and aiming

`TypeEnginPeutAttaquer` is at `0x453D7D`, `EnginTrouveCibleScan` at `0x453DA2`, and `EnginTrouveCible` at `0x453F74`. Scan returns the first eligible ID; grid selection uses its original spatial traversal and distance/tie order, including special handling of types 2/8. Do not replace both with an unconstrained nearest-enemy search.

Owner alliances are directional (`PlayerEstAllie`, `0x46D838`). Adjacency uses type-specific occupied cells (`0x44246E`, `0x4468E4`, `0x446B0C`). `EnginAPortee` (`0x446CB5`) includes modes 1/3/5 and explicit building/magic geometry callbacks; the minimum range excludes squared distance ≤4 for type 16. Line-of-fire reconstruction is tied to `0x4517A2` and its sign-step traversal.

Aiming resolves target cells and quantizes the original angular result. Body, type-3 behavior, and turret paths are distinct. A query for required orientation does not itself rotate a live unit. The tests compare original x87 calls in the supported input domain; they do not claim bitwise equivalence of every x87 intermediate.

## Attack states and projectile effects

Attack substate 0 prepares, aims, and waits for readiness; 1 animates and emits at its marked frame; 2 waits/revalidates; 3 ends the local order. Retain exact original sequencing, counter widths, and dependency calls. Do not infer transitions from an attractive animation sequence.

The origin of `+0x8A=2/3` remains unproven: direct writes found by the audit use 0/1, and none of the 2,604 records in 38 ETA maps contain 2/3. Loaders can preserve externally supplied values; this neither proves those phases impossible nor licenses inventing their producer. The audit also tracks `+0x79`, `+0x7A`, and `+0x8B`.

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
python3 -B scripts/check.py --domain combat
```

The current slice's actual results and expected dependency stops are recorded in [the combat handoff](../pesquisas-paralelas/combate/HANDOFF.md) and its `validacao-consumo-dano-*.json` reports. Reference calls execute original modifiers, proximity, visibility, volume, and the original non-AI message return without replacing instructions or return registers. AI message bodies and audio/death backends remain external. Further work can reconstruct the cell wrapper around this consumer, add other damage modes and lethal effects, and trace `+0x8A=2/3` producers.
