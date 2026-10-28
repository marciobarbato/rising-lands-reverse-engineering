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
