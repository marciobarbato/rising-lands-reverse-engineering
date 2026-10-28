# Research status — 2026-10-28

The organization baseline is remote revision `1231ebff9463871b124d736c9e0333a6f8b5c87a`. It already contains all three completed feature branches: economy/market, graphics/animation, and core/structures. Combat developments were already on main. Completed worktrees have been preserved in the workspace archive.

## Recorded differential results at that revision

| Domain | Tests | Bounded original-x86 executions | Meaning |
|---|---:|---:|---|
| Core | 226 | 49,305 | Includes placement and gate simulation; no skipped cases in the saved emulated run |
| Combat | 113 | 234,245 | Targeting, attack state, projectile pool/advance, cadence, and impact preparation |
| Economy | 214 | 54,871 | Includes 176 expected x86 exceptions and 3 expected execution limits |
| Graphics | Per-stage reports | Per-stage reports | Six research stages plus a corrected composition release; keep stage counts separate |

These are **historical, independent runs**, recorded in the versioned JSON reports. They are not an aggregate integrated-game test and are not claims that organization reran those x86 calls. Current local check results are recorded separately in [the organization check record](ORGANIZATION_CHECKS.md).

## Implemented research scope

Core includes 38 ETA maps, eight CMP banks, 26 unit types, damage primitives, movement and occupancy, independent Python pathfinding for occupancy classes 1–3, task operations and messages, structure footprints/terrain, placement, walls, and physical gate transitions. The original SBL supplies 1,995 records; the decoded AI program contains 1,157 instructions, 42 registered types, and 140 resolved operation names.

Combat includes target selection and persistence, range and line-of-fire tests, angular aiming, attack animation/emission, a 100-record projectile pool, full supported projectile advancement/expiration, caller gating, and visual impact preparation. Damage delivery and other world callbacks remain explicit integration boundaries. The producer of attack field `+0x8A` values 2/3 is still unproven.

Economy includes resource queries and mutations, capacity/excess handling, deposits/withdrawals, warehouse counts and ownership effects, terrain resource extraction/regeneration, recruitment initiation/progress, production increments, library learning completion and initiation, market proposal evaluation, and market transfers. Complete unit production/spawn and transport remain open.

Graphics includes verified bodies for five unit types, indexed composition and shadows, Sanctuary facade layers, terrain objects, trees, and codes 54/66/67/68. The v6 reader maps all 486 nonzero serialized objects in mission 1; this does not establish complete mission loading or a final rendered game scene.

The macOS preview is a separate consumer of older pinned snapshots. New research files do not become preview features automatically. Its movement lab, manual economy operations, and targeting queries have narrower scope than the current research modules.

## Next independent slices

| Owner | Next slice | Excluded responsibilities |
|---|---|---|
| Core | Structure allocation/initialization and lifecycle callers; trace real-mission load/remapping and gate dispatch | Economy charging, projectile behavior, sprite mapping |
| Combat | Trace impact/damage and missing attack-phase producers; join supported combat steps through explicit callbacks | Navigation implementation, resource rules, renderer |
| Economy | Unit production completion/spawn handoff and transport/market callers; preserve partial-failure semantics | World allocator implementation, movement algorithm, rendering |
| Graphics | Remaining structure/gate sprite mapping and render ordering, with indexed-buffer comparisons | Physical gate state/collision, economic meaning inferred from appearance |

Each slice must stop at its declared boundary, publish an English contract and tests, and state what remains unsupported. A complete playable mission still needs coordinated world loading, dispatch, dynamic rendering, combat/economy integration, events, save/load, audio integration, and reference-game comparison.
