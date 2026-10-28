# Stage 11 readiness: structure traversal of MissionPlaceTerrain

Current status: **independent original captures committed, translation and light frozen replays pass; fresh native/domain/integration gate pending**. Initial inventory/plan below is historical. Resumed under the new human authorization on 2026-10-28. Inspected committed main `8810b3730a0fb788af3eac2b447dea65372f597f`; the clean existing Missions worktree was resumed and fast-forwarded without resetting or replacing any work. Stages9/10 and all predecessor evidence remain intact. The old STOP and unit-15 radius limitation are historical, superseded respectively by the new authorization and committed Core Stage14.

The coordinator granted light work only. No native capture, Ghidra session, heavy test, integration or engine implementation has been started for this stage. The static exporter [extrair_terreno_estruturas_missao.py](extrair_terreno_estruturas_missao.py) reads only the intact executable and committed provider sources. [Inventory](evidencias/terreno-estruturas-missao-inventario.json). A later light turn merged verified Core Stage15 main `b610bfad77ffadaa0ee5f6af02160d786ccfdc7b` into this same stage; its contract is now audited below. The first static inventory remains unchanged as historical provenance.

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
- Core's Stage15 is now integrated at `b610bfad77ffadaa0ee5f6af02160d786ccfdc7b`. [RESET_MINIMAP.md](../../docs/core/RESET_MINIMAP.md) supplies `minimapa_estruturas.modificar_minimapa_estrutura(world,index,ativo)` and the bound world method. Mode1 of this caller becomes SetMiniMap mode6 across the footprint; no structure-record store occurs. Terrain/minimap resets are also integrated but are not inserted into this L8 traversal. The current stage imports only these committed sources, never the live Core worktree.
- Existing namespace adapters/bootstrap must keep economy's `construcoes` distinct from graphics. New module basenames must be unique across all research/core/app folders.

## Capture and validation plan after the heavy grant

1. The integrated Core15 contract has been inspected. [bancada_terreno_estruturas_missao.py](bancada_terreno_estruturas_missao.py) combines the committed reset/discovery and placement harnesses; its import/MRO was checked without instantiating Unicorn. It adds only caller intervals, trace/stop hooks, explicit inherited Bags, whole-memory serialization and the saved-register continuation frame. No engine body is substituted.
2. Make original-only observations **before translating this traversal**: real MONDE01 input records in a declared inherited world; an empty pool; sparse/repeated positions and edge slots 0/999; absent and present habitation; early callback/dependency checkpoints. Any synthetic region/color/allocation state is labeled as inherited fixture input, never natural remap output.
3. Compare the entire DGROUP+.bss image `0x494000..0x523000`, the full unit and structure pools, and every declared physical/economic/selection/Bag/search/route allocation that the native path can reach. Include ordered original call/effect traces. Compare all bytes, including retained bytes; no selected-field-only acceptance.
4. Cover literal state/existence and post-placement habitation gates, map mode 1, the original return epilogue, owner/type boundaries and partial-effect timing. Reuse committed lower-provider tests rather than duplicating their whole matrices.
5. Compare both the bounded structure continuation and the joined original `MissionPlaceTerrain` entry over a declared MONDE01 fixture. The latter establishes L8 only, not M1.
6. Under coordinator serialization, run changed native checks and the required missions/domain/integration gate. Keep new results separate from original-only captures and prior stage reports. Use `scripts/workstream.py integrate missions` from the clean feature worktree; the helper now supports Missions.

Prepared capture script: [capturar_terreno_estruturas_missao.py](capturar_terreno_estruturas_missao.py). It refuses to overwrite an existing result. Eight declared scan inputs cover real MONDE01 structure-only and joined entry, empty state, uninhabited edge999, inhabited state1 at0, sparse0/999, a missing-map CALL stop and owner4's pre-discovery CALL stop. Six complete returns and two declared stops are the plan, not observed results. Whole static image and every mapped non-stack/non-code arena are compared/hashed, with ordered call and physical traces. A light pure-Python input audit confirms MONDE01 type2/state5 and shared mask/bonus backing; that is fixture consistency, not native validation.

AI/runtime requested the smallest MissionGetNum provider for L9. The coordinator approved four tiny original-only query cases as the M1 identity portion of the **same** stage, followed by translation only after capture. [Static query bytes](evidencias/mission-get-num-inventario.json) are `xor ah,ah; mov al,[0x496fe4]; ret`: exactly one live byte; AX is0..255 while highEAX16 is retained. Planned API `consultas_missao.numero_missao(missao_u8)` reads the same explicit one-byte buffer/view, with no default, copy or neighbor read. The native capture varies the field, adjacent poison and high register bits; no getter implementation exists yet.

Suggested serialized windows: first run only the eight scans plus four getter observations and inspect/commit the original-only results; release the lease while translating. Then request a window for the changed native differential, required domain gate and complete integration helper. These are bounded plans; no estimated runtime is counted as validation. Check BRT at each stage boundary. The new human development cutoff is18:25 on2026-10-28;18:25–18:40 is handover only, and no new development round begins after the cutoff.

## Remaining M1 contracts

The [planned M1 snapshot contract](M1_SNAPSHOT_CONTRACT.md) is an acceptance/interface proposal, not an exported loaded mission. Whole MissionLoad still needs complete natural `Chemin_Remap`, generic declared bindings and Core `Engin_RetrieveExperimente 0x441623`. Coordinator reports the raw AI reset provider integrated at main `5d24c91104e8b7f66b774e5b46969508708cc01f`; its real-world adapter and the exact remaining query dependencies still require committed adoption, not literal fixture values. Full-load composition follows only after this stage is integrated and the coordinator schedules it. MONDE01's existing type-2 structure is a Santuário; type3 is Armazém/CAVE. Objective evaluation remains separate.

## Original-only observations completed before translation

Under the coordinator's exclusive eight-scan/four-query grant, the first capture attempt succeeded on2026-10-28 at approximately17:05BRT. [Capture](evidencias/captura-terreno-estruturas-missao-original.json) SHA-256 `52232213ef3585a8523a04d24d5bcc9d472c90ff137769fb0cea48f9a41b777e`; capture source commit `24ca5a794ff4c6979a8f5ed7c23621d75adcdf32`, original EXE and ETA identities recorded inside. No current-stage Python scan/getter existed or executed. The capture is preserved unchanged.

- Seven structure-tail entries plus one joined MissionPlaceTerrain entry: six returns to the real sentinel and two stops at the declared CALLs `0x46c1b1` / `0x41cdb9`, all exactly as planned.
-56 scan segments,18 minimap-entry and30 pixel-loop preserved-state resumes; maximum156,130 native instructions per segment. Four additional MissionGetNum entries are reported separately from scan segments.
- Six complete state blocks (5,263,360 bytes per snapshot): DGROUP+.bss plus unit, object/argument, physical, navigation/color and explicit Bag arenas. Input/output hashes and complete ordered parent/physical traces are retained for every case.
- Original query returns AX0/1/127/255, ignores poisoned neighbors, retains input highEAX16 and writes no global byte; the exporter checks whole-image read-only equality.

The native child exited0 and the heavy lease was explicitly released immediately. No domain/full-native/integration gate ran under this short grant. Log: ignored `.local/stage11-capture-attempt1.log`. Independent capture commitment precedes the next translation. This proves original observations only; Python equality and full MissionLoad/M1 acceptance remain unclaimed.

Following capture commit `ed0172a364310b28584824b3e49dc63db371ed93`, the same stage translated the caller and its Missions-owned two queries. All8frozen cases now match every mapped-state hash and ordered trace, without native execution. The exact API/current status is in [MISSIONS.md](../../docs/MISSIONS.md#stage11-translation-and-light-capture-replay). Coordinator confirmed Missions owns BatimentExiste from the existing economic handoff, canceling the proposed duplicate-query wait. Five local focused tests pass with four native methods skipped. `validar_terreno_estruturas_missao.py --emular`, the required domain gate and integration await the next exclusive lease; no second stage began.
