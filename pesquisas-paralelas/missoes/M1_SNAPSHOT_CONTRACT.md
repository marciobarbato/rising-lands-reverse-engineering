# Planned M1 loaded-mission snapshot contract

**Status: proposal, no exported M1 state and no M1 acceptance yet.** This refines the existing macOS request in [MISSIONS.md](../../docs/MISSIONS.md#planned-contract-carregar_missao-m1-result-requested-by-macos). Inspected source revision: `8810b3730a0fb788af3eac2b447dea65372f597f`. The contract is intentionally separate from the Stage 11 structure traversal implementation. That stage can prove L8; a whole-load oracle must prove M1 later.

## Identity and acceptance

The future result records:

- Schema/version and a stable snapshot identity; exact engine source commit, provider revision identities, fixture/allocation-registry identity and SHA-256, and intact executable SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
- Mission number, generated raw MakeMissionName bytes, opened raw path, ETA size/SHA-256 and all other read input/profile/rule identities. Original CP1252 text is not silently normalized into a filename.
- Exact snapshot checkpoint. M1 is the original `MissionLoad 0x46c2cf` return to `CalculGame 0x42d22d`, before that caller's clipping/menu/first-frame work. Include the ordered completed calls and external binding log. The unused AL load before IaReset is not an input to that provider.
- `acceptance`: `planned`, `partial` or `accepted_m1`. A partial result names original callee, CALL site, reason, last completed operation and the retained state. Success of individual slices cannot select `accepted_m1`.
- Whole-MissionLoad oracle report path/SHA-256, native and Python source/fixture identities, compared block list, exact mismatches and expected stops. Missing report or unresolved reachable operation prevents acceptance. `tested_in_real_mission` remains false until a separately recorded actual mission/runtime run.

The app must display the acceptance/checkpoint, and consume read-only snapshot bytes. It must not label a synthetic inherited world or partial load as a running original mission. Derived labels/counts point to documented layouts; objective/condition entries stay raw until TestFinDeMission is implemented and verified.

## Block registry and provenance

Every block has a unique logical ID, original static address or pointer slot, declared native fixture base, byte length, element width/count/stride, endianness, bytes/SHA-256, and aliases expressed as `(block_id, offset, length)`. Distinguish pointer-slot contents from pointed-to allocation bytes. Declare shared pool identity once; consumers' views must resolve to that same block. A copy for export is acceptable when its alias metadata is preserved.

For every byte range, record provenance and its writer: **inherited program-start allocation/image**, **explicit rule/profile input**, **reset**, **ETA-loaded**, **remap/placement/tail-derived**, or **retained**. Keep the input SHA-256 and pre-state identity alongside the post-state. Fixture zeros/patterns are explicit inherited inputs, never claims about natural startup. A block may contain several provenance ranges; for example structure payload204 is loaded while its trailing72 bytes remain inherited until later original writes.

The registry is closed over every reachable allocation in the declared oracle. Capture the full static data image `0x494000..0x523000` (**585,728 bytes**) as a backstop, including padding, counters, tables and globals without decoded field names. Add every pointed-to allocation separately, including retained/runtime-only bytes. Code, stack locals and declared external thunks are not mission-state blocks; any other comparison exclusion requires an explicit reason in the oracle report. Do not discard pointer differences or unknown writes to achieve equality; use the same deterministic allocation binding and declared addresses on both sides.

## Known layouts to expose

Addresses below come from the committed mission/core/economy contracts. `[...]` means dereference the named pointer slot. This table does not establish that every block has already been initialized by the original load composition.

| Logical state | Address / bytes / layout | Required provenance |
|---|---|---|
| Terrain attributes | `[0x507da8]`, 65,536 u8 | ETA layer, then actual reset/remap/placement effects |
| Terrain tiles | `[0x507d70]`, 131,072 bytes, 65,536 little-endian u16 | ETA layer, then placement effects |
| Terrain objects | `[0x507d74]`, 65,536 u8 | ETA layer plus committed 54→66 normalization and later effects |
| Object auxiliary/owners | `[0x507dac]`, 65,536 u8 | ETA layer plus normalization and later effects |
| Map dimensions / selected view | `0x497168`, two u16; `0x508720`, two u16; viewer `0x508041`, one u8 | Dimensions from ETA; view from the selected ETA player only; viewer inherited |
| UI clipping dimensions | `0x508724..0x508728`, two u16 | Retain separately; do not conflate with header dimensions or infer the caller's later clipping work |
| Region grid | `[0x4e0f38]`, 131,072 bytes, 65,536 u16 | Exact complete Chemin_Remap output and structure changes, not the convenience region rebuild |
| Structure-color grid and allocator | `[0x4e156c]`, 65,536 u8; `0x4e1570`/`0x4e1670`, 256 bytes each; `0x4e0732`, 1,024 u16 | Actual remap/placement stores; retain allocator state |
| Search / routes | Search globals including `0x496304` u16, `0x496302` u8, `0x4e0f36`/`37` u8, `0x4e0f3c` u32; route pointer table `[0x4e1924]` and its declared pointed-to buffers | Exact Core layout/whole allocation registry; retained completion/scratch bytes are included, not reset by convenience defaults |
| Discovery, light edges, light counts | Four pointer slots each at `0x507d78`, `0x507d88`, `0x507d98`; each target is 65,536 u8 | Inherited/reset state plus each actual discovery/light call, in order |
| Minimap | `[0x507d5c]`, `[0x507d60]`, `[0x507d64]`; each 65,536 u8; dimensions `0x496fe0`, two u16 | Exact reset and placement effects; colors/palette-related inherited inputs also registered |
| Units | `[0x4e19a0]`, 220,800 bytes = 800×276; loader bytes `0x4e19bc`, four u8 | Reset then indexed ETA load, postload, placement, capacities and tails. Retain every untouched slot/field |
| Unit selections | `0x508728`, 2,048 bytes = four 512-byte lists | SelectionInit's four count words and loader ordinal effects; other bytes retained |
| Unit technology/type Bags | Pointer table `[0x4e19b8]` to four distinct 2,704-byte pools = 26×104 each | Exact reset and EnginInitTechnologie; retain reserved Bag bytes |
| Structures | `0x49a0c8`, 276,000 bytes = 1,000×276 | Reset, indexed ETA copy204/retain72, then placement/habitation/map/tail effects |
| Structure counts / selections | `0x49a070`, 88 bytes = 4×22; `0x495be0`, eight bytes = four u16 | Actual core reset and BatimentInitCave identity; distinct from realizability below |
| Resources / warehouse capacities | `0x4e2ea8`, 128 bytes; `0x4dfb2c`, 24 bytes = four six-byte records | ETA resources and actual economy tail/warehouse effects; retained resource types remain included |
| Live / stored players | `[0x5080a8]` and `[0x5080ac]`, declared allocations including their 80-byte four-player tables, 20-byte stride | Explicit program-start/loaded input; PlayerRetrieve copies only its documented type/AI/sympathy fields |
| Technology / realizability | `0x4dd6e8`, 9,152 bytes = 4×22×104; `0x4e1934`, 104 u8; `0x4dfad4`, 88 u8; `0x508f30` and `0x508f44`, 20 bytes each | Explicit inherited tables and actual habitation/tail writes, with the economic object views aliased by identity |
| Mines / initial attacks | `0x509954`, 80 bytes = 20×4; `0x50d5b4`, 1,004 bytes = 100×10 plus u32 counter | Stage 7 loading/reset/retention. No extraction or attack execution inferred |
| Ghost structures | `0x50b18c`, 5,254 bytes: u16 count, 750 u16 IDs at+2, retained gap+1502..1503, 750 u32 at+1504, 750 flags at+4504 | Stage 9 reads and flag initialization; raw runtime meaning remains separate |
| Influence | `0x50c614`, 4,000 bytes = 400×10 | Stage 9 word reset and payload stores; retained+8/+9 bytes included |
| End conditions / objectives | `0x4e1d20`, 114 bytes; `0x511ffc`, 804 bytes | Stage 3 exact loaded/reset/retained fields, including adjacent status/result/cursor bytes. No evaluator implied |
| Monster entries / groups | `0x50a9bc`, 1,220 bytes; `0x50af84`, 432 bytes = 16×26 type counts plus16 group counts | Stage 9 ETA/profile/RNG effects, then the actual IaReset→InitMissionMonstre tail |
| Two RNG states | `0x497164` u32 and `0x498db4` u32 | Distinct live generators; inherited clock/profile/rule provenance and ordered advances |
| Projectile runtime pool | `[0x5080f0]`, 5,600 bytes = 100×56 | Actual ProjectileReset, with retained bytes included; no projectile frame pass |
| Icon/message/balloon runtime | `0x4e2410`/60, `0x4e05a2`/1, `0x4e7754`/132,614, `0x4e1a14`/32 | Stage 10 selective resets and retained fields; balloons alias economy's table |
| Frame/runtime counters and all market tables | Full static image, plus each owner's published named views; market reset cells include `0x4e2e7c`/4, `0x4e292c`/4, `0x4e2928`/4, `0x4e2938`/8, `0x4e2940`/8 | Retained state or actual MarcheResetAll stores, never fabricated first-frame counts |
| Market proposals / contact / prices | Contacts `0x496f8c`/4; unit prices `0x496fb0`/26; resource prices `0x496fcc`/3; indicators `0x4e2930`/8; difference `0x4e2948`/2; offered/requested units `0x4e29bc`/208 and `0x4e2a8c`/208; offered/requested resources `0x4e2cfc`/24 and `0x4e2d14`/24 | Explicit inherited market buffers, shared live players/resources, then actual selective reset; untouched proposals remain present |
| Unit type / bonus / masks / other rules | Unit type records `0x4965ae`/1,300 (26×50); bonus records `0x4dfba0`/1,872 (4×26×18); type-20 runtime mask `0x4dfb9c`/20 overlaps the first16 bonus bytes | Exact intended rule/INI/image identity and address aliasing, not a silent zero bonus or static-mask substitution |

The rule-row base is the committed `regras.BASE_TIPOS`; unit-type values come from `entradas.tipos_originais`, which combines the intact image and `RISING.INI`, separate provenance from ETA. Core's `terreno_estruturas` explicitly identifies the type-20 mask as mutable RAM. The registry must preserve its real overlap with the bonus storage, rather than manufacture an independent mask copy with different bytes. The full static image remains the byte-level source for those aliases.

## AI and runtime completeness

The full static image includes **all** AI global tables, decoded or not. Named views must be supplied from the integrated AI/runtime contract; a WIP commit is not an accepted provider. Currently documented anchor layouts are:

- Task records `0x512320`, 100×96 bytes; free-list header `0x5148a0`/16 and five context headers `0x5148b0`/80. The complete `0x512320..0x514900` span is 9,696 bytes and includes the headers.
- Player AI contexts `0x51a98c`, four16-byte records; group records start `0x51a9e0`, 100×32. The surrounding header/flags remain included in the static-image block.
- Unit/city/resource/war table anchors `0x51b664`, `0x51b84c`, `0x51ba3c`, `0x51ce44`, `0x520234`, with all exact owner counts, header extents and padding to be taken from the integrated initializer provider. The contract-stage examples describe writes for one fixture, not complete allocation extents; do not use those examples as lengths.
- Rule/configuration tables, list headers, probabilities and program-start constants are inherited from declared IaAlloc/RUL/image state. MissionLoad calls **IaReset**, not iaInit; IAResetAttaque has no original caller and is not inserted into the load.
- Every dynamic task/group/runtime allocation discovered by the generic binding registry is included even if it has no decoded display fields. Declared allocator records contain size, handle/base, lifetime and retained bytes. Released temporary remap buffers are reported in the binding log, distinct from surviving mission state.

This closes the schema's coverage rule without inventing the still-pending AI provider extents. M1 acceptance requires the resolved provider's full registry and the native whole-load byte comparison; an opaque static image alone does not establish whole-load correctness.

## Briefing and objective provenance

MissionLoad does **not** read `WORLD/MONDE01.TXT`. The app may expose the original CD text separately with source path, CP1252 decoding, size/SHA-256 and the label "source briefing" until its selector/display routine is traced. No mission state or objective predicate is derived from that text.

MONDE01 starts with one type-2 `SANCTUAIRE` (Santuário), not a type-3 `CAVE` (Armazém). TestFinDeMission must establish the actual objective and transitions. Snapshot acceptance, a rendered inspection view and a completed/playable mission are separate claims.
