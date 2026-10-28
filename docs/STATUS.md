# Research status — 2026-10-28, seven-front round

Main `2da89cd7655998f3b3f240be192b4b2badf94b63` closed the previous round: core stage 13, combat stage 16, economy stage 14, graphics stage 15, missions stage 8 and the playable macOS consumer are all integrated, pushed and ancestry-verified. The organization baseline of the earlier four-chat round was `1231ebff9463871b124d736c9e0333a6f8b5c87a`. This round reorganizes the work into seven fronts aimed at [a running original mission](ROADMAP_MONDE01.md); the roadmap holds the dependency map, milestones, per-front stage sequences, the validation oracle strategy and the completion inventory.

## Current local check results at the round baseline

| Suite | Discovered | Explicit optional skips |
|---|---:|---:|
| Core | 357 | 169 |
| Combat | 227 | 143 |
| Economy | 393 | 180 |
| Graphics, including comparison with captured original buffers | 176 | 0 |
| Missions | 56 | 21 |
| AI/runtime (namespace guard only; no research stage yet) | 3 | 0 |
| Workflow and provider-import tests | 8 | 0 |

These are local runs of `python3 -B scripts/check.py`; the fresh native counts of each integrated stage are recorded in the owners' manuals and handoffs. They are not an aggregate integrated-game test.

## Implemented research scope

Core includes 38 ETA maps, eight CMP banks, 26 unit types, damage primitives, movement and occupancy, independent Python pathfinding for occupancy classes 1–3, task operations and messages, structure footprints/terrain, placement, walls, physical gate transitions, structure pool lifecycle, exit position, conversion, recovery, experience queue, physical exit, unit request/volume, selection initialization, global unit/Bag reset, mission placement predicates and the pre-allocation remap reset. The original SBL supplies 1,995 records; the decoded AI program contains 1,157 instructions, 42 registered types, and 140 resolved operation names; the VM control flow and five unit operations are reconstructed.

Missions includes the indexed unit loader with selection initialization, the header prelude, end-condition/objective table loaders, the indexed structure copy, the mission filename selection, the mine/attack auxiliary loaders and the `MissionPlaceTerrain` unit scan with capacity refresh through committed core/economy providers. Actual MONDE01 stops at unit 15 (vision radius 10) inside core's discovery boundary.

Combat includes targeting, aiming, attack states, the projectile pool and dispatcher, caller gating, damage modes 1/3/4/8/9, the unit impact wrapper, optional lethal sequencing and the shared-world physical death connection. Natural emission/runtime and the building-target branch remain open.

Economy includes resource queries and mutations, capacity/excess handling, deposits/withdrawals, warehouse counts, extraction/regeneration, recruitment, production increments, learning, market proposals/transfers, bonus producers, read-only transport status queries and the prepared production pipeline through position, conversion, recovery, experience, physical exit, movement order, conditional request and selective cleanup. Natural startup and the transport cycle remain open.

Graphics includes verified bodies for several unit types and states, indexed composition and shadows, facades, gate facade/tail, selection sorting, projectile display and lighting, the complete interior sprite pass order, the terrain block cache and the bounded terrain pass. Frame orchestration and cache initialization remain open.

The macOS playable consumer runs a synthetic exercise over committed providers from one pinned revision. Audio and save/load have no reconstruction yet; they are inventoried for the second wave.

## Next stages

The per-front wave-1 sequences and the cross-front contracts are in [the roadmap](ROADMAP_MONDE01.md#wave-1-stage-sequence-per-front). Each stage must stop at its declared boundary, publish an English contract and tests, state what remains unsupported, and be integrated before the next begins. A complete playable mission still needs coordinated world loading, dispatch, dynamic rendering, combat/economy integration, events, save/load, audio integration, and reference-game comparison.
