# Stage 11 readiness: structure traversal of MissionPlaceTerrain

Status: **static inventory and capture plan only**. Resumed under the new human authorization on 2026-10-28. Inspected committed main `8810b3730a0fb788af3eac2b447dea65372f597f`; the clean existing Missions worktree was resumed and fast-forwarded without resetting or replacing any work. Stages 9/10 and all predecessor evidence remain intact. The old STOP and unit-15 radius limitation are historical, superseded respectively by the new authorization and committed Core Stage 14.

The coordinator granted light work only. No native capture, Ghidra session, heavy test, integration or engine implementation has been started for this stage. The static exporter [extrair_terreno_estruturas_missao.py](extrair_terreno_estruturas_missao.py) reads only the intact executable and committed provider sources. [Inventory](evidencias/terreno-estruturas-missao-inventario.json).

## Exact caller contract

Continue at `0x46c16d` after Stage 8's unit scan and four capacity calls. For index 0..999 in ascending order:

1. `BatimentExiste 0x41a735`, CALL `0x46c185`: consume lowAL. It zero-extends AX, reads byte +5 of the 276-byte structure record at `0x49a0c8`, and returns AL 1 iff nonzero. The original pool is 276,000 bytes. Missions owns this leaf according to economy's committed handoff.
2. On nonzero existence, `PlaceBatiment 0x41c4ac`, CALL `0x46c190`.
3. `BatimentEstHabiter 0x41a5b8`, CALL `0x46c197`: consume lowAL.
4. On nonzero habitation, `BatimentHabitable 0x41cc70`, CALL `0x46c1a2`.
5. `BatimentModifyMap 0x419e97(index, EDX=1)`, CALL `0x46c1b1`, for every existing structure, whether inhabited or not.

The loop exits via `0x46c17d` to the shared `pop edx; pop ebx; ret` at `0x46b6f5..0x46b6f8`. A native continuation must preserve or explicitly construct the two saved-register stack words. No native instruction or internal engine call may be replaced with a Python result.

Every callback reads live state at its call position. Habitation is queried after placement; map modification runs after any habitation effects. A failure retains earlier placements, Bags, grids and stores. Replaying the scan is not a continuation and can repeat vision counts. A missing callback must name its original callee and CALL site when reached; no silent defaults.

## Providers to compose

- Core `colocacao_estruturas.colocar_estrutura(world,index,mascara_tipo20=...)` is committed. Keep its supported type/geometry/wall/gate domain and the explicit 20-byte runtime mask for type 20.
- Economy `HabitacaoConstrucoes.estrutura_habitada(index)` and `.tornar_habitavel(world,index)` are committed. Preserve identity of the shared unit/structure pools, technology Bags at `0x4dd6e8` (9,152 bytes), spells `0x508f30`/`0x508f44` (20 bytes each), realizability tables `0x4e1934` (104) and `0x4dfad4` (88), capacities `0x4dfb2c` (24) and resources `0x4e2ea8` (128). Do not copy those providers or accept constructor state as loaded state.
- Core's Stage 15 `BatimentModifyMap`, TerrainReset and MiniMapReset are pending integrated-SHA notification. Consume their published main revision and public contract only after that notification; do not import from the live Core worktree.
- Existing namespace adapters/bootstrap must keep economy's `construcoes` distinct from graphics. New module basenames must be unique across all research/core/app folders.

## Capture and validation plan after the heavy grant

1. Inspect the integrated Core Stage 15 contract and adopt the smallest matching harness/provider interface. Reproduce only the relevant changed dependency before relying on it.
2. Make original-only observations **before translating this traversal**: real MONDE01 input records in a declared inherited world; an empty pool; sparse/repeated positions and edge slots 0/999; absent and present habitation; early callback/dependency checkpoints. Any synthetic region/color/allocation state is labeled as inherited fixture input, never natural remap output.
3. Compare the entire DGROUP+.bss image `0x494000..0x523000`, the full unit and structure pools, and every declared physical/economic/selection/Bag/search/route allocation that the native path can reach. Include ordered original call/effect traces. Compare all bytes, including retained bytes; no selected-field-only acceptance.
4. Cover literal state/existence and post-placement habitation gates, map mode 1, the original return epilogue, owner/type boundaries and partial-effect timing. Reuse committed lower-provider tests rather than duplicating their whole matrices.
5. Compare both the bounded structure continuation and the joined original `MissionPlaceTerrain` entry over a declared MONDE01 fixture. The latter establishes L8 only, not M1.
6. Under coordinator serialization, run changed native checks and the required missions/domain/integration gate. Keep new results separate from original-only captures and prior stage reports. Use `scripts/workstream.py integrate missions` from the clean feature worktree; the helper now supports Missions.

## Remaining M1 contracts

The [planned M1 snapshot contract](M1_SNAPSHOT_CONTRACT.md) is an acceptance/interface proposal, not an exported loaded mission. Whole MissionLoad still needs complete natural `Chemin_Remap`, generic declared bindings, Core `Engin_RetrieveExperimente 0x441623`, and the integrated AI `IaReset` provider. Full-load composition follows only after this stage is integrated and the coordinator schedules it. MONDE01's existing type-2 structure is a Santuário; type 3 is Armazém/CAVE. Objective evaluation remains separate.
