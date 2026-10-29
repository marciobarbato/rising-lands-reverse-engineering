# Graphics handoff

Latest dispatch: render API **1.7**, scripted CAVE display, 2026-10-29. The explicit 1.7 goal supersedes the dispatch's
1.6 heading/report label. See the final section below and [M3_CAVE_RENDER.md](M3_CAVE_RENDER.md).
Delivery is feature-branch push only; the coordinator owns review, main integration and acceptance.

Research round: 2026-10-28. Chat `01a18262-cdd5-7b13-84af-0d6eca1a43eb`.
Worktree: `/Users/marcio/git/Rising Lands/worktrees/re-graphics`.
Feature branch: `feat/re-graphics`, based on organization revision `6634be3af2d255846a847d8aa21ad4edf1cdb589`. The feature commit is the commit carrying this handoff; final commit and remote-main merge identities are reported to the coordinator after the authorized integration helper finishes.

## Delivered slice

`portoes_graficos.py` reconstructs the type-12 `HERSE` gate facade before the common `AffBatiments` tail. It exposes a pure query and indexed compositor, 64 hash-identified frame associations, an original-buffer contact sheet, exact original-byte extracts and a separately run original-x86 validator. Previous releases, stage reports, manifests, inputs, and predecessor hashes are unchanged.

The exact supported API and formulas are in [the graphics manual](../../docs/GRAPHICS.md#gate-facade-contract--2026-10-28). `consultar_portao` requires keyword inputs: counter u8 restricted to 0–31; full orientation u16; raw `+0x0A` u16; owner 0–4 and camera 0–3; mode u8; record visibility u8; separate cell discovery u8; projected x/y i16; window width/height u16 in cells restricted to 1–1024. The caller supplies an already resolved object-253/type-12 runtime record. There are no defaults for missing state and no disk-to-runtime conversion.

## Original contract and ordering

1. Reject a foreign-owner record when mode is not 3 and its visibility byte at `+0x110+camera` is zero.
2. Query discovery at the per-camera cell map; bit 16 suppresses the facade.
3. Save the current global clip; resolve the gate occupancy label (the public caller must do this).
4. Query `BatimentGetEtat`, consume its low u16, and replace the clip with the state-dependent inclusive rectangle. The incoming clip is not intersected.
5. Copy one sprite with clipping enabled. Orientation zero selects `7576+counter` at `(x,y)`; any nonzero u16 selects `7608+counter` at `(i16(x+5),i16(y+4))`.
6. Stop at `0x40F342`, before the common workshop/restore/selection/gauge tail. Early rejection stops at `0x40F491` before the epilogue. Missing original occupancy saves the clip then rejects; it does not yield a public prepared-record plan.

The facade makes no player-color or shadow call. The pure compositor returns new bytes and preserves destination opacity semantics. The original captures compare the complete 276-byte runtime record before/after, and verify the selected occupancy/object/discovery cells are preserved. There are no allocator, physical-gate, damage, economic, or simulation callbacks. The new APIs do not import another owner's implementation or a live worktree.

Invalid widths/ranges, booleans, and incompatible nonempty-plan surface dimensions raise `ValueError`; missing required arguments raise `TypeError`. Counters 32–255 raise `NotImplementedError`. The original accepts the complete byte and runs into later strips; 896 such captures are recorded separately without widening the public domain. Hidden-cell plans have no layers and preserve the background without accessing a catalog. Camera 4 would access beyond this record's four visibility slots and is unsupported.

## Evidence

- `RISING.EXE`: SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
- `AffBatiments` gate branch `0x407FA7..0x4080E8`: SHA-256 `f52190772fa3b3abf70197f451bab4fe9887b56edf436b2d1abc574ff0cce20d`.
- Gate copy join `0x408412..0x408422`; raw-state query `0x41A8E5..0x41A940`; clip helpers `0x40F4B7..0x40F535`. Input convention: `AX=x`, `DX=y`, `BX=cell`; runtime base `0x49A0C8`, stride 276; viewport `0x508724/+2`; object constant at `0x495BF9` equals 253.
- Type-12 table `0x495FFC..0x496030` contains `HERSE` and denominator 70. `BatimentGetEtat` returns `floor(raw_u16*200/70)`; this renderer consumes the low word without economic interpretation.
- `BUILDING.CMP`: SHA-256 `af4f94ea996a65d36592bb6cefc407dc628b3d488c9c335b8f6015bbfcb6a3ae`; IDs 7576–7639 correspond to local indices 547–610. Zero-orientation frames are 34×30; nonzero-orientation frames are 21×47.
- [Exact bytes and appended predecessor provenance](evidencias/portoes-graficos.json), [frame and opacity hashes](artefatos/associacoes-portoes.json), [original reference captures](validacao/x86-portoes-graficos.json), [contact sheet](artefatos/portoes-contato.png). The sheet contains 64 independently compared original 64×64 surfaces, with the original palette applied afterward. Its patterned background is an indexed test fixture.

## Actual validation

Commands run in this feature worktree:

```sh
python3 -B pesquisas-paralelas/graficos-animacao/validar_portoes_graficos.py
python3 -B -m unittest discover -s pesquisas-paralelas/graficos-animacao -p 'test_portoes_graficos.py' -v
python3 -B scripts/check.py --domain graphics
```

The completed x86 run uses the authorized execution context supporting Unicorn JIT memory: **2,792 bounded executions / 1,651,749 observed instructions**. It records 1,700 supported call/clip captures (all 32 counters, full-word orientation boundaries, four modes, owner/camera/visibility/discovery combinations, signed coordinates, raw-state low-word boundaries, and structure index 999), 896 raw counter-overrun captures, two missing-occupancy captures, two bank initialization calls, and **192 exact indexed-buffer comparisons**. No skipped cases, expected x86 exceptions, or instruction/time limits occurred. The supported draw cases stop deliberately before the common tail; they do not claim full function or game execution.

Nine new regression tests pass; `scripts/check.py --domain graphics` passes **82 tests**, with no skips and valid documentation links. Legacy x86 validators were not rerun; their saved reports are only replayed by existing Python tests. A sandbox JIT smoke probe produced no usable reference result, and an initial permitted development run found a camera-4 fixture indexing error; the public camera range and fixture were corrected to the four in-record camera slots before producing the final saved run.

Integration is to be performed from the clean committed feature worktree using `python3 scripts/workstream.py integrate graphics`. The coordinator receives the actual common-suite counts and remote-main merge identity after it completes; this file does not claim a future push already succeeded.

## Remaining dependencies

Core supplies an existing prepared runtime record and occupancy mapping, including the current gate counter; the renderer neither resets nor increments it. The raw state word is consumed exactly, without deriving resource costs, construction progress, or physical collision rules. Scene projection, global draw order, workshop callback, clip restoration in a stateful consumer, selection/gauges, complete mission loading, other buildings, and preview integration remain open. No claim of a complete playable game is made.

## Continuing research inventory and next dependency

The facade stage was integrated by the required helper: implementation `6dcd05564047589e85fac4ba525ac762fedcc24f`, final feature revision `f147ecea657154532efb1166103ffc0164d8b177`, remote-main merge `ff4bc269c6d8534f4683bd0429072286ea8eaaf1`. Common checks discovered 665 tests: 376 executed passed and 289 optional x86 tests skipped (core 238/118 skipped; combat 113/70; economy 229/101; graphics 82/0; workflow 3/0). These common checks do not replace the separate new gate x86 run.

The same authorized graphics chat resumed its clean worktree through the helper and fast-forwarded to that main revision. Before the next implementation, [the manual's inventory](../../docs/GRAPHICS.md#remaining-component-inventory--continuation-after-the-gate-facade) records the remaining original intervals and dependencies: the gate shared tail, other building facades/overlays, unit action handlers, scene traversal/projection, runtime visibility/palette/clocks, and a real-mission consumer. None is labeled complete merely because a callback or isolated fixture exists.

Selected next: close the type-12 shared `AffBatiments` tail `0x40F342..0x40F49C` through its actual return. Original frame/gauge functions contain type-12 early returns; the workshop function has terrain/type guards. Validate clip save/restore and the actual guard ordering without implementing another owner's physical or economic behavior. General buildings, unit action handlers, and full scenes remain separate later work.

## Second stage: gate tail through the actual return

Implemented `portoes_completos.py`, with `consultar_portao_completo` and `compor_portao_completo`. All first-stage input fields and failures remain unchanged. Additional required inputs: `terreno_u16` (0–65535, excluding `0x356`) and `recorte_entrada` (four u16 words in left/top/right/bottom order, including inverted rectangles). Terrain `0x356` raises `NotImplementedError` because its workshop guard scans external structure records; invalid terrain/clip widths raise `ValueError`. The prepared runtime bag must be valid for the original read-only habitation query. The pure API needs no habitation/selection/hover input because those branches cannot add pixels for type 12.

Effects and order: save incoming clip, apply the facade temporary clip, copy the gate, run the workshop terrain guard, restore the saved words, query habitation, optionally enter selection-frame and gauge functions, return. Both overlay functions explicitly return before drawing for type 12. The renderer returns `(new_indexed_bytes, restored_clip_tuple)` and has no global state or delegated callbacks. Early hidden-record/cell paths preserve the incoming clip without catalog access. The captured original preserves the 276-byte record and returns with the balanced stack at `0x2008004`.

Evidence: same original executable SHA-256 as stage one; shared tail `0x40F342..0x40F49C` hash `ce3dabcebaebfb6d4ba718445b5d854bcfd10b184bdf6c2883354c7b837e3264`; workshop guard `0x402864..0x40288B` / epilogue `0x402C7A..0x402C82`; selection guard `0x4022C8..0x4022F9`; gauge guard `0x4020EC..0x402122`. [New exact-byte evidence](evidencias/portoes-completos.json) includes the original habitation and bag-query intervals and hashes of the unmodified first-stage module/evidence/report.

Actual new command `python3 -B pesquisas-paralelas/graficos-animacao/validar_portoes_completos.py`: **882 bounded original-x86 executions / 1,077,090 observed instructions**, comprising 768 call/guard captures, 112 exact indexed-buffer comparisons and two bank setup calls. All executions reach the actual harness return `0x3000000`; no expected dependency checkpoints, x86 exceptions, limits or skipped cases. Pixel comparisons run original habitation, selection/gauge guards, clip helpers and blitter without substitutions. Only bank file IO/allocation is stubbed; call-only captures intercept the copy to record its arguments.

Six new regression tests pass via `python3 -B -m unittest discover -s pesquisas-paralelas/graficos-animacao -p 'test_portoes_completos.py' -v`. `python3 -B scripts/check.py --domain graphics` passed all **88 tests**, with zero skips and valid documentation links. Earlier validators/reports are unchanged and their totals are not newly rerun. The [full-return saved report](validacao/x86-portoes-completos.json) records this stage separately.

The first stage's shared-tail gap is closed only for this declared type-12/terrain domain. Tile `0x356`, other building tails/facades, scene traversal/projection, action handlers, mission operation and preview activation remain unsupported. The next slice is selected after this stage's required integration, with the inventory updated before implementation.

## Third stage selected after successful second-stage integration

Stage two implementation `6489f6127f787cdb08a72170ec3e3e779da4d9ea`, final feature `2ceb6bf9dfadcfbc38c097295bc4da102140677e`, merged/pushed main `8066d6cde161fb699a498a293039af612b62b6b3`. Required common checks discovered 692 tests: 393 executed passed, 299 optional x86 skips (core 248/122 skipped; combat 124/76; economy 229/101; graphics 88/0; workflow 3/0). The same clean worktree resumed through the helper and fast-forwarded to updated main before further research.

The next evidence-backed inventory update selects the unit-selection/sort prefix of original `AffSprite 0x416864..0x416A6C`. Direct calls later in that function establish its role ordering vegetation, buildings, and two unit passes. First close its 800-record existence/visibility/window filter and exact in-place swap order by cell and `+0xAB`; equal-key order must not be assumed stable. This is a prerequisite to the full scene plan, with projectiles and traversal kept as explicit later dependencies. Original bytes and an independently executed overlap composition will ground the ordering slice.

## Third stage implementation and validation

`selecionar_ordem_unidades` consumes 800×276 runtime bytes, separate discovery/illumination maps of 65,536 bytes, required map origin 0–255 per coordinate, and window dimensions 1–256 cells. It reads state u8 `+2`, cell u16 `+8`, and priority u8 `+0xAB`; it returns pool-order selected indices and exact swap-order sorted indices. The original nonzero-state, discovery-mask 31, illumination-mask 16, and asymmetric window margins (+2 columns/+10 rows) are preserved. Sorting uses the complete cell word then the priority byte, with original equal-key instability. No world/input bytes mutate; no callbacks run. Invalid buffer lengths/ranges raise `ValueError`; missing keyword inputs raise `TypeError`.

Evidence: original `AffSprite 0x416864..0x416A6C` hash `9c1d0287c39058b803a9f23c0080354ab769c5127132919bd03d1a82768bad0e`, `ExisteEngin 0x441FFF..0x442025`, discovery `0x4766F0..0x47670A`, illumination `0x47693A..0x476951`; original executable SHA-256 unchanged. [New exact-byte evidence](evidencias/ordem-unidades.json) preserves predecessor hashes; [new reference report](validacao/x86-ordem-unidades.json) stores original selected/sorted buffers and indexed overlap hashes.

Actual command `python3 -B pesquisas-paralelas/graficos-animacao/validar_ordem_unidades.py`: **2,354 bounded segments / 15,600,001 observed instructions**. There are 327 selection/sort fixtures, including every state/flag byte and all 800 selected, plus eight overlap fixtures. Checkpoints are `0x416946` before sort, `0x41697D` at outer-loop boundaries for large arrays (original CPU/stack retained), and `0x416A6C` before projectile sorting/drawing. No expected exceptions, limit failures or skips. The segment count includes 40 original type initializations, 40 original supported complete body draws and two bank setup calls. The overlap buffers use captured original order and native unit bodies at one explicit projected position; they do not emulate the whole scene. Stable sorting changes 44–127 pixels in each of the eight buffers.

Six new capture regression tests pass via `python3 -B -m unittest discover -s pesquisas-paralelas/graficos-animacao -p 'test_ordem_unidades.py' -v`. `python3 -B scripts/check.py --domain graphics` passed **94 tests**, with zero skips and valid documentation links. Prior stages' x86 reports/totals remain unchanged.

Global gap closed locally and independently validated: the real sprite caller's existence/visibility/window selection and exact pre-draw ordering. Full two-pass traversal, projection, projectile render-list provider, other building/action handlers and real-mission operation remain open. This bounded stage alone does not warrant changing the coordinator's coarse overall estimate of about 50% (40–60% uncertainty). Integration and any real-mission testing are distinct statuses; this stage has no real-mission runtime test.

## Fourth stage selected after successful third-stage integration

Stage three implementation `fffc0b41b5e03036c5bed5902e4669585408611e`, final feature `fa997845bbb4667e783d9650e56c74896fc04cfc`, merged/pushed main `2b18ceaacf36a1360709bbb68debffefc905e5e7`. Mandatory common checks discovered 743 tests: 420 executed passed and 323 optional x86 skips (core 248/122 skipped; combat 141/88; economy 257/113; graphics 94/0; workflow 3/0). The same clean feature worktree resumed through the helper and fast-forwarded to updated main.

Combat confirmed it has no translated display-list/GetCase contract and explicitly permitted graphics to recover those read-only display functions. The next inventory closes `ProjectileTrierAffichage 0x46FC8B..0x46FE9A` and `ProjectileGetCase 0x46FE9A..0x46FEE5`: pixel-word-derived cell keys, mask-31 discovery/illumination, and the exact last-equal swap order in the caller-supplied output array. Physical advancement, target cells, damage and projectile lifetime remain combat-owned. The full `AffProjectile` sprite dispatcher remains a separate renderer dependency; no target-field approximation is accepted.

## Fourth stage implementation and exact pool-view contract

`ordem_projeteis.py` consumes a 5,600-byte pool (100×56) without mutation. `consultar_celula_projetil(pool, indice_u16)` accepts 0–99 and reads u16 pixel words at `+0x0C/+0x0E` even when activity is zero; returns full `chave_u32=(y//32)*256+x//32` and its low word separately. Raw coordinates are not clamped; maximum words derive key 526079. Origin/target cell words never substitute for this query.

`selecionar_ordem_projeteis(pool, descoberta, iluminacao, indices_entrada, *, origem, janela_celulas)` requires two 65,536-byte selected-camera maps, a 200-byte input index array, origin pairs 0–255 and window pairs 1–256. Activity u8 `+2` must be nonzero. Both camera predicates mask 31 at the derived low-word key; window margins are +2/+10. It returns initial selected indices, exact last-equal swap order, count and new array bytes. Only the first count×2 array bytes are replaced; the unused tail is preserved. Invalid lengths/ranges/indices raise `ValueError`, missing required keyword arguments raise `TypeError`. Negative camera origins and indices outside the pool are excluded. No callbacks or physical simulation effects occur.

Evidence: sort `0x46FC8B..0x46FE9A` hash `3b26fd5f75330b32f114f8546c332e9fb13e3740af97519a8c6283cbf74e5dc5`, cell query `0x46FE9A..0x46FEE5` hash `5cf91836f9b460da243a56f8f62400d840dff7b8a5014a223ceb13c89c97ccc1`, same original executable SHA-256. Original output pointer enters in EAX, count returns in EAX; the cell query index enters AX and key returns EAX. Globals: pool `0x5080F0`, camera `0x508041`, origin `0x508720/+2`, window `0x508724/+2`. [New exact-byte evidence](evidencias/ordem-projeteis.json) and [new reference report](validacao/x86-ordem-projeteis.json) preserve predecessors.

Actual `python3 -B pesquisas-paralelas/graficos-animacao/validar_ordem_projeteis.py`: **1,310 bounded segments / 1,736,567 instructions**, 581 complete index-buffer fixtures, 98 full cell queries, eight indexed overlap fixtures, 32 original complete type-1 draw calls and two bank setup calls. The sorter pauses once before sorting (`0x46FD9C`) then resumes with the same CPU/stack through RET; no expected dependency stop remains. Zero skips, expected exceptions or limit failures. Native overlap IDs/positions are captured from `AffProjectile` type 1 and replayed by reconstructed order; this demonstrates indexed ordering but does not implement the public projectile sprite dispatcher.

Seven new saved-capture tests pass. `python3 -B scripts/check.py --domain graphics` passed **101 tests**, with zero skips and valid documentation links. Global gap closed locally/independently validated: the scene's projectile display-list and precise cell-query inputs. Real-mission/runtime integration, the two complete scene passes, public projectile drawing and remaining building/action mappings are still open. This stage does not justify changing the coordinator's approximately 50% overall estimate (40–60% uncertainty).

## Fifth stage selected after successful fourth-stage integration

Stage four implementation `8ea8c56653ec1779fd47303ff6be614f13486c75`, final feature `1b50221ca11b49860236c08de852005c9b7d07ff`, merged/pushed main `8cb672c17e13f062a7d80f68c5ec89723e3e3dfc`. Required common checks discovered 767 tests: 437 executed passed and 330 optional x86 skips (core 260/126 skipped; combat 146/91; economy 257/113; graphics 101/0; workflow 3/0). The same clean feature worktree resumed through the helper, inspected history, and fast-forwarded to updated main (including committed economy changes).

The next inventory selects both scene passes in `AffSprite 0x416A6C..0x416E41`, consuming the committed unit/projectile selectors. The first scan is width+8 by height+5, with vegetation/buildings before zero-priority units; the second is width+8 by height+10, with projectiles before nonzero-priority units. Validate exact callback order and relative 32-pixel projection on stable interior frame snapshots, then compare a bounded supported native indexed scene. Wraparound/negative-origin viewports, arbitrary handler side effects, general sprite mapping and real-mission loading remain separate boundaries.

## Fifth stage implementation and callback contract

`planejar_passe_sprites` consumes fixed pools (800×276 units, 100×56 projectiles) plus object/discovery/illumination maps of 65,536 bytes. Required origin 0–255 supplies both native arguments and projectile viewport globals; window dimensions are 1–32, with complete +8-column/+10-row margins inside the 256×256 map. It returns exact callback events for both passes and the verified selector results. Raw event inputs do not imply that every renderer handler is implemented.

First row-major pass: width+8 columns, height+5 rows; discovered nonzero objects emit `AffVeget`, then every cell emits `AffBatiments` and the literal-RET `AffBatimentOmbre`, then priority-byte-zero units emit `AffEngin`. Second pass: width+8 by height+10; matching projectiles emit `AffProjectile` before nonzero-priority units. Relative origins increment by 32 pixels. Selected zero-priority units in the additional lower five rows are not forced into a callback. Sorting is completed before callbacks, and the selection/cell/priority/object/visibility snapshot must remain fixed while rendering.

`executar_passe_sprites` requires `vegetacao(x,y,cell)`, `construcao(x,y,cell)`, `unidade(x,y,index)`, and `projetil(index)`. It skips only original `AffBatimentOmbre` (literal RET `0x40F49B`), ignores callback return values and returns callback count. Missing callbacks raise `TypeError`; non-callables raise `ValueError` before any call; callback exceptions propagate with earlier effects retained and no rollback. Planning is pure; invalid arrays/ranges raise `ValueError`, boundary-crossing margins raise `NotImplementedError`. Rendering side effects remain owned by the invoked handler.

Evidence: full original caller `0x416864..0x416E41` hash `e3a5445a1ef8b30dbdcb1b41612ff2ebfb612070d49f8673b252af7f1fd8bd51`, original shared epilogue `0x410878..0x41087E`, same executable identity. [Exact caller bytes/provenance](evidencias/passe-sprites.json) pins the unchanged committed unit/projectile selectors and gate return implementation.

Actual `python3 -B pesquisas-paralelas/graficos-animacao/validar_passe_sprites.py`: **105 bounded native calls / 3,578,331 instructions** (55 full callback traces, eight complete sprite-pass indexed scenes, 40 original unit initializations, two bank setup calls). Every caller execution reaches `0x3000000` with stack `0x2008004`. Zero skips, expected exceptions, execution limits or dependency checkpoints. Call-only fixtures capture renderer callbacks; pixel fixtures execute original trees, gate, five supported unit bodies and type-1 projectile handlers without renderer substitutions. Composition matches all eight native indexed surfaces. The supplied background is synthetic; `AffTerrain` and full `AffGame` are not invoked. Projectile commands are captured for the replay; public projectile sprite mapping is not silently added. [Reference report](validacao/x86-passe-sprites.json), [128×128 indexed scene preview](artefatos/cena-passe-sprites.png).

Seven new saved-capture regressions pass. `python3 -B scripts/check.py --domain graphics` passed **108 tests**, with zero skips and valid documentation links. Global gap closed locally and independently validated: complete interior sprite-pass ordering/projection and one coordinated bounded renderer scenario. Callback availability, broader handler coverage, terrain/global-frame behavior and real-mission runtime operation remain separate dependencies. Overall completion remains the coordinator's approximately 50% estimate (40–60% uncertainty), not a percentage inferred from these tests.

## Sixth stage selected after successful fifth-stage integration

Stage five implementation `cc21d00999b7887ba7036415fe43d166e830ac62`, final feature `1250f9c3250b21ef56f53589425a38da8a9184fd`, merged/pushed main `4d12341b803deda5fd1a995a32c1ec6c1b65d235`. Required common checks discovered 816 tests: 465 executed passed and 351 optional x86 skips (core 270/130 skipped; combat 157/98; economy 278/123; graphics 108/0; workflow 3/0). The clean feature worktree resumed through the helper and fast-forwarded to this main revision.

The public projectile renderer depends on original `PasteEclairCmp 0x45BA23..0x45BCB0`, `MemEclairCopy 0x45F7D8..0x45F7F6` and `CalculEclairage 0x45FAFC..0x45FCA5`. These map destination indices under opacity, and the table has a distinct zero-component target rule and inverse percentage arithmetic. The original setup call loads 60 at `0x474F04`. Select this palette/blitter dependency first; validate original tables, cycle exclusions, clipping and literal-zero opacity before using it in the public projectile mapper. Physical projectile advancement remains combat-owned.

## Sixth stage implementation and failure contract

`eclairage.py:tabela_eclairage` consumes exactly 768 RGB bytes, required percentage u8 1–255, and up to 255 inclusive u8 cycle intervals. Each component targets `q=component*100//percentage`, replacing q=0 with 30 and capping other q at 255. Nearest squared-RGB color wins, ties keep the smaller eligible index; initial candidate 0 remains eligible even inside a cycle. Nonzero candidates in cycle ranges are excluded. The original writes destination indices 0–255 in sequence; the Python API returns new table bytes without mutating inputs.

`compor_eclairage` consumes a valid decoded frame, explicit 256-byte table, indexed destination, inclusive clip and signed-i16 x/y. It reproduces the clipping-enabled `PasteEclairCmp` path by mapping destination bytes under opacity. Opaque literal zero remains a mask hit, literal source colors are ignored, skips preserve destination. It returns new bytes and has no callbacks. Invalid widths/ranges raise `ValueError`; percentage zero is rejected in Python before effects. The original zero divisor faults at `0x45FB46` before any table output byte is written; that expected failure was independently executed and recorded.

Evidence: same original executable identity; `CalculEclairage 0x45FAFC..0x45FCA5` hash `9a9709bd01200af21f1848f13901ab946e11b1449ddaaf052ceae98a90ddb156`; `PasteEclairCmp 0x45BA23..0x45BCB0` hash `81371fcc66cb61a61031de5c4c841b844f124754909f7246ec51c3e867969407`; `MemEclairCopy 0x45F7D8..0x45F7F6`; setup call `0x474F04..0x474F13` loads DL=60. Inputs: palette pointer EAX, percentage DL, output pointer at `0x4E24B8`, cycle count/table at `0x4E24E1/0x4E24E4`. [New exact-byte evidence](evidencias/eclairage.json), [native reference report](validacao/x86-eclairage.json).

Actual `python3 -B pesquisas-paralelas/graficos-animacao/validar_eclairage.py`: **4,412 bounded segments / 35,074,931 observed instructions**, eight complete native table fixtures, 297 exact indexed buffers, two bank setup calls, and **one expected original zero-divisor exception**. Table checkpoints at `0x45FB16/0x45FB23` preserve original CPU/stack across all 256 output writes and finish through RET. Native blits return normally. Zero skips, unexpected exceptions or limit failures. Only bank file IO/allocation is substituted; the synthetic frame replaces ID1's descriptor exclusively in emulated RAM, leaving original bytes untouched.

Seven new saved-capture tests pass. On explicit human resumption, `validar_eclairage.py` was rerun against the intact original: the same 4,412 segments, eight tables, 297 buffers and one expected exception were reproduced, with all observations unchanged and only elapsed seconds different. The pre-resume report is preserved in ignored local storage with SHA-256 `a9dab152bbe8f48f136486e230754fb9d12bae0e8add271ea3c2de66cdc5f640`. `python3 -B scripts/check.py --domain graphics` passed **115 tests**, zero skips and valid documentation links. These repeated runs do not create additive coverage.

The required helper resumed the existing dirty feature worktree without discarding pending files and fetched main `5e2bf0831d3aaa776481a6ab023be262ef0df1bd`. Stage six is completed before any next implementation. A private read-only REA session reviewed `CalculEclairage`, then exported and closed successfully. [Focused REA review](evidencias/rea-eclairage-review.json) records pinned source `b9a8f8e9f25feb9cc97bf4960748f2bdf8c898bc`, normalized analysis PE SHA-256 `26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0`, the unchanged intact-original execution identity, exact retained pseudocode Evidence and the Watcom signature/register limitations. REA corroborates the formula; original assembly and independent x86 captures remain authoritative.

Global gap closed locally/independently validated: the lighting table and opaque destination-remap effect required by the public projectile/effect renderer. `CL=0`, palette lifecycle/cycling, public projectile mapping and real-mission/runtime integration remain unsupported. Latest communicated overall estimate is coordinator-owned approximately 50% (40–60% uncertainty); one expected invalid-input x86 exception is not a model/reasoning blocker.

## Seventh stage selected after successful sixth-stage integration

Stage six implementation `1fa6824d0123cc11676e89c15644e725baed2eb9`, final feature `fd5f05afd02f9caf18a2e490ee6c97690b61d22e`, merged/pushed main `cd3981d54ccd2545818d15e61f3d553a32e35a1a`. A subsequent fetch verified all three are ancestors of `origin/main`. The mandatory helper discovered 850 common tests: 485 executed passed and 365 optional x86 skips (core 280/134 skipped; combat 163/102; economy 289/129; graphics 115/0; workflow 3/0). The clean worktree resumed through the helper and fast-forwarded to that main revision.

The highest-value next dependency is the public `AffProjectile` renderer, original `0x46FF70..0x4704D9` plus its 34-entry jump table `0x46FEE8..0x46FF70`. Recover a plan/compositor consuming a prepared 56-byte record, explicit origin words and the selected illumination byte. Preserve type/phase/activity u8, unsigned pixel-coordinate words, direction u8, presentation displacement u32, signed-i16 coordinate wrap, and exact copy/shadow/lighting order. Types 28/33 and unknown/inactive/hidden paths must remain no-draw. Raw states selecting IDs outside the verified bank catalog will remain explicitly unsupported; valid raw phases do not imply a new logical animation state. Physical advance, arrival, damage and phase producers remain combat-owned. A private read-only REA session complements the original-byte and native differential investigation.

## Seventh stage implementation and validation

`projeteis_graficos.py` provides `consultar_projetil_grafico(registro56, *, origem, iluminacao_u8)` and `compor_projetil(catalogo, destino, largura, altura, registro56, *, origem, iluminacao_u8, tabela_sombra, tabela_eclairage, recorte=None)`. Origin contains two raw u16 words. Read record fields: type/activity u8 +0/+2, pixel x/y u16 +0x0C/+0x0E, phase/direction u8 +0x18/+0x22 and presentation displacement u32 +0x24. The illumination byte is selected at low-word `(pixel_y//32)*256+pixel_x//32` for the current camera; this renderer does not read discovery. Activity zero, illumination mask 31 nonzero, types 0/28/33/>34 return no layers without catalog lookup.

The plan reports exact layer IDs, file/local indices, signed-i16 positions and copy/shadow/Eclair operations. It preserves raw phase/direction rather than inferring natural animation. Types 9–13 ignore phase and issue shadow then displaced copy. Types 24/25 truncate signed `(direction-1)/2` toward zero; type 27 uses `(direction-1)*8`. Types 29/30 draw three lighting layers, types 31/32 two shadow/lighting layers. The compositor requires two explicit 256-byte tables, composes in plan order and returns new bytes plus plan. All inputs stay unchanged; no callbacks, RNG, clock or physical projectile mutations occur. Invalid widths/lengths raise `ValueError`, missing required keywords `TypeError`, and IDs outside catalog 1–12156 `NotImplementedError` before composition. Raw spills within the catalog are reproduced without gameplay claims.

Evidence: original executable SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`; `AffProjectile 0x46FF70..0x4704D9` hash `0fe33194fc2edde7f73e94a1d103b9a017f0213ed84dd2d3cf770bd2a32b3cf7`; dispatch table `0x46FEE8..0x46FF70` hash `24baa7752b2cac6f99cf92b36b4e5dabe38c72d5e7e001a1ab3025c48ad7de87`; epilogue `0x46FC08..0x46FC0F`; illumination `0x476951..0x476968`. Original index enters low EAX, pool pointer at `0x5080F0`, camera at `0x508041`, viewport words at `0x508720/+2`; every blit has CL=1. [New exact-byte evidence](evidencias/projeteis-graficos.json) pins unchanged lighting/pass/selector predecessors.

Actual `python3 -B pesquisas-paralelas/graficos-animacao/validar_projeteis_graficos.py`: **12,148 native calls / 7,447,454 instructions**, comprising 11,728 full-return dispatch captures, 410 exact indexed buffers, eight complete sprite-pass scenes and two bank setup calls. All caller executions finish at `0x3000000`, ESP `0x2008004`; pool/illumination inputs remain intact. Zero skips, expected exceptions or limits. Matrix covers all type/phase bytes, directional bytes for types 24/25/27, activity/illumination bytes and displacement/coordinate/origin boundaries. **172 raw states select out-of-catalog IDs** and are explicitly unsupported publicly. Their captured blitters are intercepted; these do not establish valid native asset dereferences. Pixel/scenes execute original renderers without substitutions; bank loading substitutes only file IO/allocation. [New native report](validacao/x86-projeteis-graficos.json).

The eight native/public scenes replace the stage-five captured projectile commands with the public mapper, mixing trees, supported gate/unit bodies and 16 projectile types. The indexed background is synthetic; no terrain/global-frame/real-mission runtime claim follows. Explicit tables come from the unchanged historical shadow report and stage-six percentage-60 lighting report. [Contact sheet](artefatos/projeteis-contato.png) presents all 32 visible types in increasing order, phase 0/direction 1, eight columns. Seven new regressions pass; `python3 -B scripts/check.py --domain graphics` passes **122 tests**, zero skips and valid documentation links.

The private REA session `1793196524625-15935` reviewed the dispatcher and instruction `0x46FFE7`, exported and closed successfully. [Focused reviewed Evidence](evidencias/rea-projeteis-review.json) retains both executable identities and pinned REA revision. Exact bytes `e91cfcffff` are JMP to `0x46FC08`, despite existing Ghidra flow metadata claiming call; original instructions and independent native return remain authoritative. No modeled parameters in REA does not negate the recovered low-EAX index ABI. This is an annotation limitation, not a model/reasoning stall.

Global gap closed locally/independently validated: public copy/shadow/lighting projectile rendering and complete bounded scene composition without captured projectile commands. Physical updates/phase producers, temporal animation, broader unit/building mappings, terrain/global-frame behavior and real-mission runtime remain separate gaps. Coordinator owns the overall approximately 50% estimate (40–60% uncertainty); integration status must be reported separately after the required helper.

## Eighth stage selected after successful seventh-stage integration

Stage seven implementation `f9f18ba0e3c63138bde3277b026eadd65cbaa77e`, final feature `2fb5a6801ee61d077fdca417b23b6e5d662ae81d`, tested/pushed main merge `8fd9c41ce6e3b8709cc0d7235e8c31d9b6a68b8d`; all three were verified reachable after fetching `origin/main`. The helper discovered 944 tests: 536 executed passed, 408 optional x86 skips (core 302/143, combat 191/119, economy 326/146, graphics 122/0, workflow 3/0). The clean feature worktree resumed through the helper and fast-forwarded to this main.

The app requested normal body rendering for type 2 (`CAPITAINE` in the French type table). Select that bounded consumer gap: original body branch `0x412ECE`, anchor table slot `0x410F6C -> 0x410FF8`, and prepared runtime frame count/phase/direction bytes. Preserve the existing five-type public modules and frozen predecessors. Add a separate raw-record type-2 API, validate complete original `AffEngin` calls with effect/indicator conditions explicit, then compare indexed buffers. Attack/construction/work/death handlers, physical movement/phase producers and palette/player effects remain separate scopes. Static REA is complementary to original assembly and independent x86.

## Eighth stage implementation and exact consumer contract

`unidade_tipo2.py:consultar_corpo_tipo2(registro276, *, x, y)` takes one prepared 276-byte record and signed-i16 projected cell origins. It supports owner byte +0=0, type +1=2, states +2=2/7, oscillation +0x99=0, effects +0xDC=0, auxiliary indicator +0xBA=0 and unsigned +0x74 word >=100. These inputs are guards, not inferred mission defaults. The bag word +0x0A is irrelevant to this branch. Displacement +0x86/+0x87 is signed i8; direction +0x91, phase +0xA4 and count +0xA5 are raw u8. Body ID is low-u16 `3202 + (floor((direction+1)/2)-1)*count + phase`, including direction-zero group -1. Original initialization writes count8/oscillation0, but no natural phase/cadence is inferred and state7 keeps its supplied phase.

The plan emits shadow10784 at `(x+dx+2,y+dy+26)` then body at `(x+dx-32,y+dy-16)`, final positions wrapped i16. `compor_corpo_tipo2(catalogo,destino,largura,altura,registro276,*,x,y,tabela_sombra,recorte=None)` requires an explicit 256-byte table and returns `(new_indexed_bytes,plan)` using the existing blitters/inclusive clip. Inputs stay intact; no callbacks, RNG/clock or world effects occur. Invalid scalar widths/lengths raise `ValueError`, missing keywords `TypeError`; unsupported guard/type/state and raw out-of-catalog IDs raise `NotImplementedError` before composition. Existing `graficos.py`/`composicao.py` remain unchanged, including their five-type support contract.

Original executable SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`; body branch `0x412ECE..0x412F1C` hash `2861dce18904b697f56ffba18973c8f0707d9dd8f8b9ea5b51140e764afb6c57`; anchor `0x410FF8..0x411001` hash `6463df6bf40d3200669072267440eb994d87cc54b1086ec86a052805abf44670`; exact dispatch slots, join, initialization, full caller and French identity bytes retained in [new evidence](evidencias/unidade-tipo2.json), with unchanged predecessor hashes. Native signed-i16 x/y enter EAX/EDX, pool index enters low EBX, unit pool pointer at `0x4E19A0`. French `CAPITAINE` identity is not used to invent a new translated player label.

Actual `python3 -B pesquisas-paralelas/graficos-animacao/validar_unidade_tipo2.py`: **12,851 bounded native calls / 8,553,649 instructions**, 12,564 complete layer captures, 21 guard/bag captures, 263 exact indexed buffers, one type initialization and two bank setup calls. All calls reach `0x3000000` with ESP `0x2008004`; the full 800×276 pool is unchanged. Zero skips, expected exceptions or limits. Both states cover every phase byte at directions1–16/count8; additional matrices cover all direction/count bytes, pool0/799, displacement/coordinate boundaries. **555 raw states are out of catalog**: their intercepted-blitter captures establish selected commands only; public API refuses them. Indexed comparisons execute original rendering without substitutions; bank setup substitutes only IO/allocation. Tables/background are explicit synthetic inputs, without original mission/scene/cadence claims. [Native report](validacao/x86-unidade-tipo2.json), [eight-direction phase0/7 contact sheet](artefatos/unidade-tipo2-contato.png).

Seven new capture regressions pass; `python3 -B scripts/check.py --domain graphics` passes **129 tests**, zero skips and valid links. A read-only REA instruction observation at `0x412F06` corroborates the raw-count MOV; [focused review](evidencias/rea-unidade-tipo2-review.json) keeps pinned source `b9a8f8e9f25feb9cc97bf4960748f2bdf8c898bc` and normalized PE SHA-256 `26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0` distinct from the intact execution oracle. Listing operand limitations remain explicit. Private session `1793198091545-27075` exported/closed successfully; no runtime/database cache is published.

Concrete gap closed locally/independently validated: app-requested type-2 normal body, exact indexed shadow/body composition, runtime raw stride and fixed-width anchors. It is not integrated into the app by this graphics-owned stage. Other owners/effects/indicators/actions, remaining normal-body types, terrain/global-frame rendering and real-mission operation remain open. Overall percentage remains coordinator-owned; integration status follows the mandatory helper.

## Ninth stage selected: make selection globals explicit before action expansion

Stage eight implementation `80d053821c2cd8f34a49e597829831c1866f74b9`, feature `98820ebc34f85d717fa321a4b79b2e609f30f210`, main merge `6bc3564fbb615912a80fac1f681f8773505c7256` were fetched and verified reachable. Common checks: 969 discovered, 552 passed and 417 optional x86 skips (core302/143, combat198/123, economy337/151, graphics129/0, workflow3/0). The worktree resumed cleanly and fast-forwarded to that main.

Attack-caller review exposed a stage-eight wrapper omission: normal-body selection overlays depend on record +0xBD, camera byte `0x508041`, selected-index word `0x496AC2` and mode byte `0x508F8F`. Stage-eight native fixtures used the intact image defaults camera0/selectedFFFF/mode0 and +BD0; they remain valid captures for that narrower environment. The wrapper did not publish these globals and could accept a selected record. Prioritize this correction before implementing attack bodies. Require exact selection/index inputs and reject paths invoking unimplemented overlays before composition. Validate complete supported calls plus explicitly bounded original selection-entry stops; do not relabel those stops as full returns or silently update old evidence.

## Ninth stage correction and current type-2 signature

Both type-2 public functions now require `indice_u16` (actual pool slot0–799), `camera_u8` (raw current camera0–255), `indice_selecionado_u16` (raw selected/hover word0–65535) and `modo_selecao_u8` (raw mode0–255), in addition to all existing arguments. They reject before composition when `(record[0xBD]!=0 and camera==owner)` or selected index equals pool index or mode is nonzero. Nonzero +BD with a different camera is supported when the other triggers are absent. This supersedes the stage-eight signatures; no implicit selection defaults remain. Existing type/body/state/effect/width guards and layer order stay intact; no selection overlays are implemented. Maintained stage-eight tests/validator call sites pass their historical camera0/selectedFFFF/mode0/pool-index inputs explicitly. Its captured report and original-byte evidence are unchanged.

Evidence: original selection prefix `0x4124A9..0x4124C4`, tail `0x412A53..0x412A9F`; globals camera `0x508041`, selected-index word `0x496AC2`, mode byte `0x508F8F`; original executable SHA-256 unchanged. [New exact bytes](evidencias/selecao-tipo2.json) also pin unchanged stage-eight report/evidence hashes. Original-byte review directly establishes these guards; this slice does not need new REA interpretation.

Actual `python3 -B pesquisas-paralelas/graficos-animacao/validar_selecao_tipo2.py`: **5,155 calls / 2,360,401 instructions**, 5,136 branch captures, 16 exact indexed buffers, one type initialization and two bank calls. Captures: **3,596 complete returns**, **514 explicit selection-prefix stops at0x4124C4**, **1,026 explicit AffInfoSelection-entry stops at0x410BE4**. Unsupported overlay stops retain prior native body effects where applicable; they are not claimed complete returns. Public rejection intentionally occurs before any composition. Supported captures/pixels return with ESP0x2008004. Pool and all selection globals stay unchanged. Capture blitters intercepted, pixel renderers intact, bank IO/allocation substituted; no unexpected faults/limits/skips. Matrix covers every camera/mode/+BD byte, pool0/1/799 and selected-word boundaries. [Native report](validacao/x86-selecao-tipo2.json).

Five new saved-capture regressions pass; graphics domain **134 tests**, no skips and valid links. Concrete gap closed: explicit type-2 selection preflight and rejection of unimplemented overlay paths. This is a review correction to the wrapper, not repeated model/reasoning difficulty. Attack expansion remains next; simulation producers of +8A2/3 remain unproven per combat, so those bytes must only be prepared display inputs. Real-mission/selection rendering remain separate dependencies.

## Tenth stage selected after ninth-stage integration

Stage nine implementation `63655de6104b60b4ac71899a867dc522138ee8ff`, final feature `21fbbaeafbf8ebb0c909f71ab5d9babee8fc9a11`, merge `6a9168e42f917096af88fc6c510b3f25b7230516` were fetched and verified reachable on main. Common checks: 986 discovered, 563 passed, 423 optional skips (core314/149, combat198/123, economy337/151, graphics134/0, workflow3/0). Clean worktree resumed through the helper and fast-forwarded to that merge.

Select original `AffAttaqueEngin` types0/2 at dispatch slots `0x4136E4/+8`, branches `0x413A04/0x413BC7`, with the original `AffEngin` state/+8A route. Consume prepared runtime records, raw phase +A4/attack stride +A6/direction +91 and i8 shifts +86/+87. Keep owner/effects/indicators and all selection globals explicit. Type0 attack base2146/anchor40,22; type2 base3266/anchor32,16. Validate full supported calls/indexed pixels and separately record normal-handler route checkpoints or no-draw returns for rejected raw routes. Combat confirms +8A2/3 producers remain unproven: no display frame establishes emission or simulation transitions. Existing normal-body modules and capture reports remain unchanged.

## Tenth stage implementation and validation

`ataque_grafico.py` exposes `consultar_ataque_grafico(record276, *, x, y, indice_u16, camera_u8, indice_selecionado_u16, modo_selecao_u8)` and `compor_ataque_grafico(catalog,dest,w,h,record276,*,x,y,tabela_sombra,indice_u16,camera_u8,indice_selecionado_u16,modo_selecao_u8,recorte=None)->(bytes,plan)`. Projected x/y signed i16; actual index0–799, camera/mode u8, selected index raw u16. Owner0/types0or2; states1/24 require +8A1–3, state22 requires +8A1. DC/BA zero, unsigned74>=100 and explicit inactive selection conditions required. Normal/no-draw/other action routes reject `NotImplementedError`, as do effects/selection/catalog overflow. Invalid widths/lengths raise `ValueError`, missing keywords `TypeError`.

Body base2146/anchor40,22 for type0; base3266/anchor32,16 for type2. Low-u16 ID = `base+(floor((dir+1)/2)-1)*attack_count+phase`, reading raw91/A6/A4. Direction0 group -1 is preserved, A5 ignored. Original initialization sets A6=10 for both types; raw inputs do not establish legal lifecycle or cadence. Signed-i8 shifts86/87 move shadow10784 at(+2,+26), then body at negative anchor; final coordinates wrap i16. Explicit shadow table and inclusive clip, immutable inputs, no callbacks/RNG/clock/world/phase/emission effects. Combat confirms +8A2/3 producers still unproven; accepted prepared bytes do not create a simulation transition.

Original executable SHA-256 unchanged (`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`). Type0 branch0x413A04..0x413A58 hash `d35e6a88aeb0d5632eebf29764c92d07aaea57a9e49773f63944bc9d0998d782`; type2 branch0x413BC7..0x413C14 hash `cf56e6f0b2a1a728d3bf4c5bf73961b0cbb98b6bf105c90042c5c6d9703761c3`; dispatch0x4136E4, join0x413971, prefix/tail/full caller retained in [new byte evidence](evidencias/ataque-grafico.json). Native EAX/EDX projected x/y, lowEBX pool index, pool pointer0x4E19A0; selection globals0x508041/0x496AC2/0x508F8F. Existing graphics/composition/type2 sources are pinned unchanged.

Actual `python3 -B pesquisas-paralelas/graficos-animacao/validar_ataque_grafico.py`: **18,938 native calls / 20,771,171 instructions** = 17,960 captures, **974 exact indexed buffers**, two type initializations, two bank setup calls. Capture outcomes: **15,341 supported returns**, **6 normal-handler checkpoints**, **2 selection-prefix checkpoints**, **6 selection-info checkpoints**, **1,516 no-draw route returns outside this attack API**, **1,089 raw out-of-catalog captures**. Checkpoints are explicit dependencies, not returns; out-of-catalog blitter interception proves selected commands only. Every complete call returns with ESP0x2008004; pool and selection globals unchanged. No unexpected fault/skip/limit. Capture blitters substituted, native pixel renderers intact; bank fileIO/allocation substituted. [New native report](validacao/x86-ataque-grafico.json), [type0/type2 contact sheet](artefatos/ataque-tipos0-2.png).

All phase bytes/directions1–16, additional count/direction-byte matrices, all +8A bytes in each state, pool0/799 and signed coordinate/shift boundaries are captured. Indexed buffers cover initialized ten attack phases, both types/all directions/all three states and clipping edges. Seven new capture regressions pass; graphics domain **141 tests**, zero skips and valid links. [Focused REA Evidence](evidencias/rea-ataque-grafico-review.json) observes A6 MOV at0x413BFF with pinned source `b9a8f8e9f25feb9cc97bf4960748f2bdf8c898bc` and normalized-analysis SHA `26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0` distinct from the execution original. Private session `1793198944668-34524` exported/closed; operand/signature limitations explicit.

Concrete gap closed locally/independently validated: exact prepared attack-body mapping/composition for types0/2 through the real display caller. Selection/effects/other types/actions, simulation +8A2/3 producers, mission runtime and consumer activation remain separate boundaries. The background is synthetic; this stage is not a scene or natural combat pipeline. Overall estimate remains coordinator-owned; integration status follows the required helper.

## Eleventh stage selected after tenth-stage integration

Stage ten implementation `74f785fa4bd04c86a193c8875c400efaa706866a`, final feature `f90e7ef2e8b153bb841d1dd59bddfb70a2135416`, main merge `0c9faea29a65e81fcf5d1ab110110d68790924ff` were fetched and verified reachable. Common checks: 1,017 discovered, 582 passed, 435 optional skips (core319/151, combat205/127, economy349/157, graphics141/0, workflow3/0). The clean worktree resumed through the helper and fast-forwarded to that main.

Select `AffDyingEngin 0x41559A..0x41591F` and `EnginGetSpriteMort 0x415496..0x41559A` for types0/2/5/6/7/9, whose normal anchors are independently established. Consume prepared state4 owner0/effects0 records; read raw phase A4, direction91, corpse strideDB and unsigned counterC2, preserving copy/shadow-mask order around counters300/315/330. No walking footprint shadow is inferred. Core's committed `docs/core/PHYSICAL_DYING.md` establishes only the supported physical transition's A4=0/C2=0 writes and explicitly leaves corpse progression/removal open. Graphics will not invent those producers or advance the counter; original captures ground the read-only display. No new implementation in another owner's files is authorized by this slice.

## Eleventh stage implementation and validation

`morte_grafica.py:consultar_morte_grafica(record276,*,x,y)` and `compor_morte_grafica(catalog,dest,w,h,record276,*,x,y,tabela_sombra,recorte=None)->(bytes,plan)` consume projected signed-i16 x/y and prepared owner0/state4/effectsDC0 records of types0/2/5/6/7/9. Raw direction91, phaseA4, corpse-strideDB u8, unsignedC2 counter and i8 shifts86/87 drive the layers. No selection arguments are needed: the original handler ignores camera/selected-index/mode, BD/BA, fatigue74, bag0A and A5/A6. Twelve independent native cases exercise those otherwise-active fields, preserving selection globals and the full pool.

Base/anchor: type0=2226/(40,22),2=3346/(32,16),5=1762/(11,11),6=3106/(16,20),7=1538/(26,26),9=1890/(19,14). Low-u16 ID=`base+(floor((direction+1)/2)-1)*DB+A4`, including direction0 group-1. All layers share the corpse ID and wrapped-i16 anchored position; no footprint10784 shadow. Ordered operations by counter:0–304 copy;305–309 copy+1shadow;310–314 copy+2shadow;315 copy+3shadow;316–319 only3shadows;320–324 only2;325–329 only1;330–65535 no layers or asset lookup. Shadows repeatedly map the current destination under the corpse opacity mask. Counter/phase do not mutate. Finished counters avoid catalog lookup even for raw invalid would-be IDs.

Explicit shadow table256 and inclusive clip; all inputs preserved; no callbacks/RNG/clock/physical effects. Invalid input widths/lengths raise `ValueError`, missing keywords `TypeError`, unsupported owner/type/state/DC and required out-of-catalog IDs `NotImplementedError` before composition. Original init observed DB8 for five types/DB10 for type2, without a natural animation/lifecycle claim. Core confirmed its stable physical provider clears A4/C2 on the supported transition and leaves DB/life/8A unchanged; corpse progression/final removal remain unimplemented.

Original executable SHA-256 unchanged. `EnginGetSpriteMort 0x415496..0x41559A` hash `11d597526321a257beb04660b948a08b889fb2c8e5721fcdc33ed7269e6eac96`; `AffDyingEngin 0x41559A..0x41591F` hash `e0862d1dd4d638bfe1e834e28e0f6cfa1e608202da6ebf9fa7d3afc1f62208fe`; full caller retained in [new evidence](evidencias/morte-grafica.json). EAX/EDX projected x/y, lowEBX pool index, pointer0x4E19A0. All predecessor modules are pinned unchanged.

Actual `python3 -B pesquisas-paralelas/graficos-animacao/validar_morte_grafica.py`: **18,732 native calls / 29,307,746 instructions** =17,502 complete command captures,12 ignored-field captures,1,210 exact indexed buffers,6 initializations,2 bank calls. Every call reaches0x3000000 with ESP0x2008004, full pool unchanged. No dependency stops, expected/unexpected exceptions, limits or skips. **1,068 raw out-of-catalog captures** use intercepted blitters and prove command selection only, publicly rejected. Pixel renderers are original/unsubstituted; bank setup substitutes IO/allocation. Coverage: counters0–340/large-u16 boundaries, every phase/direction/stride byte in focused matrices, pool0/799, signed position/shift edges. Pixels cover initialized corpse phases/eight directions, fade thresholds and clipping. [Native report](validacao/x86-morte-grafica.json), [six-type counter sheet](artefatos/morte-contadores.png).

Seven new capture regressions pass; graphics domain **148 tests**, no skips and valid links. [Focused REA Evidence](evidencias/rea-morte-grafica-review.json) retains source `b9a8f8e9f25feb9cc97bf4960748f2bdf8c898bc`, normalized SHA `26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0` separate from intact oracle. Corrected boundary0x415639 decodes u16C2 MOV; preliminary interior-byte query was correctly unavailable, no semantic mismatch. Private session `1793199453797-37876` exported/closed. No runtime/cache published.

Concrete gap closed locally/independently validated: exact six-type prepared corpse display and destination-mask fade order. Synthetic buffers are not a full scene/mission. Counter progression/removal, other owners/types/effects, selection rendering, remaining work/construction/building handlers and consumer activation remain open. Overall estimate remains coordinator-owned; integration status follows the mandatory helper.

## Twelfth stage selected after eleventh-stage integration

Stage eleven implementation `7b3d9a7bf8ab8966eb5ac15d405628af59cf6891`, final feature `f896c637e9f72d9d335d99c670e7843b0e937301`, merge `3dd5cdcf99b945fefdd259546f85fdcf8cdd6c8d` were fetched and verified on main. Common checks:1,024 discovered,589 passed,435 optional skips (core319/151,combat205/127,economy349/157,graphics148/0,workflow3/0). Clean feature resumed through the helper and fast-forwarded to this main.

Select prepared type6/7 `AffConstruireBatiment 0x414495..0x414A8A` in states11/15. Read raw task byte89, phaseA4, direction91, shifts86/87 and Bag count0A; preserve fixed branch strides instead of reusing normal/attack counts. +89=0 chooses empty/nonempty Bag body, +89=1 chooses the action body, larger values draw no body under inactive auxiliary guards. Unlike normal/attack handlers, construction's selection prefix reacts to nonzeroBD without a camera test; require BD0 and explicit selected-index/mode guard inputs. Building progress/target semantics and phase/task producers remain other owners' inputs, not inferred from appearance. Validate complete original calls, pixel buffers, widths and selection-entry stops before integration.

## Twelfth stage implementation and validation

`construcao_grafica.py:consultar_construcao_grafica(record276,*,x,y,indice_u16,indice_selecionado_u16,modo_selecao_u8)` takes signed-i16 projected origins, actual pool index 0–799, raw u16 selected-index and u8 selection mode. Owner 0, type 6/7, state 11/15; BD/DC/BA zero, unsigned74>=100. It rejects any nonzero BD independently of camera, selected-index equality or nonzero mode before composition. Camera is irrelevant under the supported BD-zero guard, not silently defaulted; every camera byte was captured. Other invalid guards/types/states raise `NotImplementedError`, bad widths/lengths `ValueError`, missing required keywords `TypeError`.

Raw task89/phaseA4/direction91/Bag count0A/shifts86/87 drive the body. Task0 branches on Bag count zero/nonzero; task1 ignores it; task2–255 emits no body and fetches no assets. Type6 branch constants/strides: task0 empty2970/8, filled3034/8; task1 3166/4. Type7: empty1338/8, filled1466/8; task1 1402/8. Engine ID low-u16 `constant+floor((direction+1)/2)*stride+phase`, preserving direction0/raw phase spill. Counts A5/A6/A8 do not change these fixed strides. Shadow10784 at(+2,+26), then body at(-16,-20) for type6 or(-26,-26) for type7; i8 shifts and final-i16 wrap.

`compor_construcao_grafica(catalog,dest,w,h,record276,*,x,y,tabela_sombra,indice_u16,indice_selecionado_u16,modo_selecao_u8,recorte=None)->(bytes,plan)` uses explicit256 shadow table/inclusive clip. Inputs remain unchanged; no callbacks, RNG/clock, task/phase production, progress or economic/world mutation. No sprite appearance infers a building/resource/task meaning. The producer and lifecycle of raw89/A4 remain external.

Original SHA-256 unchanged. Complete `AffConstruireBatiment 0x414495..0x414A8A` hash `22d386a7b6ac4af35f190e4293d06a64dd489c4746f0db31c2cd618e8d8d3c9a`; Bag query0x4470B9..0x4470C5 hash `a4b23a2dfd610b631864b3ffd40674fc62f9bc18fec11a6d3b824a770aa937af`; full caller retained in [new evidence](evidencias/construcao-grafica.json). EAX/EDX projected x/y, lowEBX index, unit pointer0x4E19A0, selected-index/mode0x496AC2/0x508F8F. Existing modules remain pinned unchanged. Straight original-byte/native review is sufficient; no new REA semantic inference is required.

Actual `python3 -B pesquisas-paralelas/graficos-animacao/validar_construcao_grafica.py`: **32,338 calls / 33,469,945 instructions**,30,780 captures,1,554 exact buffers,2 initializations,2 bank setup calls. Captures: **29,246 full returns** including1,016 empty-body returns; **1,020 explicit selection-prefix stops** at0x41451D, **514 explicit info-entry stops** at0x410BE4. Unsupported stops are not returns. Every full caller has ESP0x2008004; full pool and selection globals unchanged. No expected/unexpected exceptions, limits or skips. Capture blitters intercepted; pixel renderer/Bag query original; bank IO/allocation substituted. [Native report](validacao/x86-construcao-grafica.json), [type6/type7 empty/filled/action direction sheet](artefatos/construcao-tipos6-7.png).

Coverage includes all task/phase/direction/camera/mode/BD bytes in focused combinations, raw Bag word boundaries, pool0/799, signed shifts/coordinates. Pixel cases exercise both states, all16 directions, phases0–7, all variants/no-body and clipping boundaries; no natural cadence is claimed. Seven new saved-capture regressions pass; graphics domain **155 tests**, zero skips and valid links. Concrete gap closed locally/independently validated: prepared mechanic/builder construction display and its distinct selection guard. Other types/owners/effects, selection overlays, work/task producers, building progress, runtime mission/consumer activation remain separate boundaries; overall estimate stays coordinator-owned, integration status follows the helper.

## Thirteenth stage selected after twelfth-stage integration

Stage twelve implementation `eb958483e744db44442f6e9e7c484326749f7603`, final feature `7fbeffc05c2c0a1f2c5d135cad3c3b4292669b6d`, main merge `7ddbbc6876539af8ffb9eb6ed9b74fd195c77702` were fetched and verified reachable. Common checks:1,050 discovered,604 passed,446 optional skips (core319/151,combat211/131,economy362/164,graphics155/0,workflow3/0). The clean helper resumed feature and fast-forwarded to current main `66e8306` including committed core voice changes before further research.

Select prepared state5 `AffWorkEngin 0x414A8A..0x415496` for worker types5/6/7. Original task89 dispatch differs by type; some no-body tasks clear a local flag and skip all post-body selection/fatigue/experience guards, while other no-body tasks retain them. Recover those exact read-only branches, fixed strides, Bag variants and camera-dependent selection prefix without reusing construction assumptions. Type13 work and selected-target/structure markers remain unsupported. No economic resource meaning, extraction/deposit mutation, phase/task producer or mission behavior will be inferred. Validate original full returns, explicit selection-entry stops and indexed buffers before integration.

## Thirteenth stage implementation and validation

`trabalho_grafico.py:consultar_trabalho_grafico(record276,*,x,y,indice_u16,camera_u8,indice_selecionado_u16,modo_selecao_u8)` consumes signed-i16 projected origins, actual pool0–799, camera/mode u8 and selected-index u16. Owner0/state5/types5/6/7/DC0. Prefix rejects nonzeroBD under owner-matching camera. Raw89 task/A4 phase/91 direction/Bag0A word/i8 shifts86/87 drive read-only body plans. No task/phase/world/resource/economic effects are produced.

Type5 tasks0/2/3 choose Bag-zero constant1594/stride8 versus nonzero1690/8; task1 constant1662/4. Type6 tasks0/1 choose2970/8 versus3034/8; task2 uses3034/8 regardless of Bag. Type7 tasks0/3/4/5 choose1338/8 versus1466/8; task12 uses1402/8. Other tasks no body. Low-u16 ID=`constant+floor((dir+1)/2)*stride+phase`, raw u8 spill preserved, A5/A6/A8 ignored. Shadow10784(+2,+26) precedes body at existing anchors5(11,11),6(16,20),7(26,26); final i16 wrap.

Type6 task3 and type7 tasks1/2 clear the native local flag and skip every later selection/fatigue/experience overlay. After the prefix guard, they accept selected-index equality, nonzero mode, any fatigue74 word and BA byte, returning no layers. Other tasks require selected-index inequality/mode0/unsigned74>=100/BA0 even on no-body paths; unsupported inputs reject before composition. This is a bounded supported guard, not proof that every excluded input necessarily paints an indicator. EffectsDC0 remains required throughout this API.

`compor_trabalho_grafico(catalog,dest,w,h,record276,*,x,y,tabela_sombra,indice_u16,camera_u8,indice_selecionado_u16,modo_selecao_u8,recorte=None)->(bytes,plan)` requires explicit shadow table256 and inclusive clip. No-body paths fetch no asset; all inputs unchanged, no callbacks/RNG/clock/world updates. Invalid widths/lengths raise `ValueError`, missing keywords `TypeError`, unsupported record/overlay inputs `NotImplementedError`. Type13 work, selected-target/structure markers, other owners/effects and task/resource producers remain separate scopes.

Original SHA-256 unchanged. Whole `AffWorkEngin 0x414A8A..0x415496` hash `4aae4288bd307f9de5b93ce32772b04ab3d7ef6803f42de3ecd412c22704694f`, whole caller retained in [new evidence](evidencias/trabalho-grafico.json). Native EAX/EDX projected origins, lowEBX actual index, unit pointer0x4E19A0, selection globals0x508041/0x496AC2/0x508F8F. Predecessor modules unchanged/pinned. Direct original-byte review and native comparisons establish the local flag without a new REA semantic inference.

Actual `python3 -B pesquisas-paralelas/graficos-animacao/validar_trabalho_grafico.py`: **19,700 calls / 23,007,614 observed instruction hooks**,18,516 captures,1,179 exact indexed buffers,3 initializations,2 bank calls. Captures: **16,971 full returns** (1,530 empty subset), **768 selected-target prefix stops**, **765 info-entry stops**, **12 indicator-boundary stops**. Supported calls pause at0x41531C then resume same CPU/stack through RET; maximum2 segments/call with300,000 instructions/2seconds each. Call count is not segment count. Unsupported stops preserve preceding native body effects; public preflight has no partial composition. Full calls finish with ESP0x2008004 and unchanged pool/selection globals. No expected/unexpected faults, limits or skips. Capture blitters intercepted; pixel renderers/Bag query intact; bank IO/allocation substituted. [Native report](validacao/x86-trabalho-grafico.json).

Matrices cover all task/phase/direction/camera/mode/BD bytes in focused combinations, raw Bag boundaries, pool0/799 and signed edges. Each bypass branch exercises all256 mode bytes with selected-index equality, nonzeroBD under another camera, fatigue0 andBA255; indexed comparisons prove empty results. Pixels exercise16 directions/phases0–7/nine body variants/no-body/clipping; no natural cadence inferred. Seven regressions pass; graphics domain **162 tests**, zero skips and valid links. Concrete gap closed locally/independently validated: three-worker prepared work sprites and task-dependent overlay bypass. Synthetic input surfaces are not scene/mission runtime; broader types/effects/markers, economic/task producers and consumer activation remain open. Overall estimate stays coordinator-owned; integration follows helper.

## Fourteenth stage selected after thirteenth-stage integration

Stage thirteen implementation `f2837231fca392078775a383b1a5bb29fdb59aeb`, final feature `a7fe998193174caab90be32eee20152159324d2e`, main merge `3151330b356d603515ff7a3057847c4421aea166` were fetched/verified reachable. Common checks:1,070 discovered,618 passed,452 optional skips (core332/157,combat211/131,economy362/164,graphics162/0,workflow3/0). Clean feature resumed through the helper and fast-forwarded to that main.

Prioritize actual terrain backgrounds. `AffTerrain 0x41068E` depends on `GetNumBob 0x40FD95..0x410085`, which is not a pure tile-ID lookup: it checks selected-camera discovery/lighting flags, searches a 256-entry `(source u16, lighting mask u8, discovery mask u8)` cache and on a miss writes a key, advances a u16 replacement cursor, copies a 32×33-byte raw block and applies shadow/fog masks. Original static capacity at0x495BC4 is256; entries/index pointers at0x49A050/0x49A04E; cached engine IDs1090–1345. Capture explicit caller-provided cache snapshots and shadow table; do not invent mission cache defaults or palette invalidation. Native source blocks1–1081 are all32×32,1056 bytes with32 literal row headers, verified read-only from hashed assets. Mask IDs1081–1089 have distinct opacity/literal-color behavior. Close this exact cache dependency before the complete terrain traversal; world terrain remapping and mission initialization remain other owners' scope.

## Fourteenth stage implementation and validation

`cache_terreno.py:CacheTerreno(registros,blocos_crus,*,proximo_u16)` owns copies of explicit1024-byte key table,270336 raw payload bytes and cursor0–255; no default initialization. Each key is sourceu16/lightmasku8/fogmasku8, each slot1056 bytes (32 rows×33). `pixels(slot)` reads the1024 literal pixel positions while retaining arbitrary supplied row headers. `resolver_bloco_terreno(catalog,cache,*,id_terreno_u16,descoberta_u8,iluminacao_u8,tabela_sombra)` returns ID/branch/slot metadata, mutating only owned graphical cache state on misses. Selected-camera bytes are explicit; discovery bit16 returns1081 blank, else low-nibble fog. Lighting bit16 forces mask15, else low nibble. Both masks0 return raw source ID with no lookup/mutation, including0/FFFF as query values without drawable-asset proof.

Cache search scans all256 keys, first exact match wins; hits preserve cursor/key/pixels and can reuse raw-source keys without fetching assets. Supported misses require verified static full-literal sources1–1081; bad miss source/shape raises `NotImplementedError` before effects, rather than emulating arbitrary native overreads/partial failures. Source/pixel/table snapshots remain unchanged; no source callback or world/RNG/clock behavior. Protected scalar/buffer errors raise `ValueError`, missing inputs `TypeError`.

Miss order: source-word key write, light byte, fog byte, next cursor modulo256,1056-byte copy, destination-shadow mask, then literal fog copy. Nibble0=no mask;1/2/3/4/6/8/9/12 map1085/1084/1088/1083/1087/1082/1089/1086; other nonzero values map1081. Cache IDs1090–1345; slot row headers preserved. Shadow uses opacity only; fog copies colored literals (full blank is index2). Table changes do not invalidate hits; stale pixels remain until replacement. No automatic palette invalidation or cache/mission startup is supplied.

Original exe SHA-256 unchanged. `GetNumBob 0x40FD95..0x410085` hash `e23998884a96474e07358cacba6c6aeb2afc618b39620068504deb32c4e4a76b`; helpers0x45C779..0x45C8DF hash `31ba5b7b0943018d64fb2dda515ab99eb9cec233d8d8ffe1070c2aacb4037bca`; discovery/lighting/capacity bytes retained in [new evidence](evidencias/cache-terreno.json). Static capacity0x495BC4=256, keys pointer0x49A050/cursor0x49A04E, nativeEAX source/EDX cell, current-camera0x508041, flag arrays0x507D78/0x507D88. Existing modules pinned unchanged.

Actual `python3 -B pesquisas-paralelas/graficos-animacao/validar_cache_terreno.py`: **8,524 complete native calls /104,519,504 observed instructions**, two bank-loading calls and **8,522 full cache-state/raw-block/pixel comparisons**. Branches770 undiscovered/40 direct/711 hits/7001 misses. All queries return0x3000000/ESP0x2008004 with callee-saved registers, visibility maps, pointer table, static capacity and buffer guards preserved. Zero dependency stops, expected/unexpected exceptions, limits or skips. Query/blit instructions intact; bank IO/allocation substituted. Dynamic payload pointers bind a guarded synthetic contiguous RAM snapshot, retaining original32×32/1056 descriptors; that fixture does not establish game initialization. [Native report](validacao/x86-cache-terreno.json), [source300 discovery/lighting mask grid](artefatos/cache-terreno-mascaras.png).

All low-five-bit flag pairs, allflag bytes in additional cases, all1081 source blocks, all256 masks for seven sources×three explicit tables, duplicate/raw-word hits, cursor255 wrap and stale-table eviction/recompute are covered. Cell0/FFFF/8000/1234 and cameras0/3 select actual native maps. Seven new regressions pass; graphics domain **169 tests**, no skips and valid links. [Focused REA Evidence](evidencias/rea-cache-terreno-review.json) retains French symbol/two-parameter summary and IDIV at0x40FF39, source revision `b9a8f8e9f25feb9cc97bf4960748f2bdf8c898bc`, normalized SHA `26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0` separately from intact execution original. Private session `1793201480425-45288` exported/closed; annotations/signatures are not fresh runtime proof.

Concrete gap closed locally/independently validated: original terrain visual cache, exact flag differences and raw block shader/fog combination. Complete AffTerrain/block drawing, cache lifecycle/initialization, world remapping, palette lifecycle, scene/mission runtime and consumer activation remain separate gaps. Overall percentage remains coordinator-owned; integration status follows the required helper.

## Fifteenth stage selected after fourteenth-stage integration

Stage fourteen implementation `15530f86c948a00d5f702a40b5fd2a00118defb7`, final feature `4eb7aab533f09c0df94fc4747872059d0a611fda`, merge `a2629e62807c2293284c1f6ec0efbfee17af5734` were fetched and verified reachable. Common checks:1,109 discovered,639 passed,470 optional skips (core341/161,combat219/137,economy377/172,graphics169/0,workflow3/0). The clean helper resumed and fast-forwarded to current main `9e60bce`, including committed mission auxiliary-layer changes.

Select complete bounded interior `AffTerrain 0x41068E..0x41087E`: row-major block-before-terrain-object callbacks, explicit nonnegative inset, viewport projection, construction-tile fallback and un-clipped opaque32×32 block drawing. `EstConstructionTerrain 0x42302D..0x423355` is a repeated range predicate covering702–1081; validate that over all u16 values. When that predicate holds and lighting mask0x10 is set, caller selects349+(cell_x mod8)+8*(cell_y mod8) before GetNumBob. Require matching native width-word/pitch and inside-map/inside-surface viewports; negative insets/wrap remain unsupported. Reuse committed cache and object providers, with full native terrain/block/object pixels over explicit snapshots, no mission cache/default inference. Callback exceptions retain earlier effects rather than claiming rollback. Complete sprite/terrain frame orchestration and real missions remain separate statuses.

## Fifteenth stage implementation and validation

`passe_terreno.py:planejar_passe_terreno(terrain131072,selected_light65536,*,origem,janela_celulas,margem_i8)` supports origin0–255, window1–32, full viewport inside256×256, inset0..floor(min(window)/2). Negative/excessive signed-i8 insets and wrapping raise `NotImplementedError`; invalid widths/lengths `ValueError`. Native width-word49A018 and pitch4E17A0 must both equal width×32. Input maps are snapshotted and relevant world/visibility bytes stay fixed while callbacks draw.

Row-major inner cells use relative32×column/row positions. The pure word predicate `terreno_de_construcao` is exactly702..1081 inclusive. When true and selected light&0x10, source word becomes349+(absolute_x%8)+8*(absolute_y%8), otherwise raw source; no world-word mutation or progress inference. `executar_passe_terreno(plan,*,bloco,vegetacao)` invokes block(x,y,cell,source) then vegetation(x,y,cell) for every cell, with required-callable preflight, ignored returns, completed callback count and exception propagation retaining earlier effects. Missing inputs `TypeError`, non-callable `ValueError`; no rollback.

`pixels_bloco_terreno(catalog,cache,id)` reads full-literal static1..1081 or cached1090..1345 payloads; other IDs unsupported. Cached row headers are skipped, matching AffBloc independent of RLE command values. `compor_bloco_terreno(dest,w,h,pixels1024,x,y)` returns new bytes:32 opaque pixels per row, pitch width, no clipping. Block must fit entirely; object callbacks retain their separate inclusive clip. Callback composition in the owned benchmark uses the committed GetNumBob cache and V6 ground-object providers; no terrain/camera/cache defaults are inferred from real missions.

Original executable SHA unchanged. AffTerrain41068E..41087E hash `4e0b75233c42cb4e1d60daaa14b7473f19b5546507421e3520deb68e935abd0b`; predicate42302D..423355 hash `b1992759ba7638da4f2e19ff1ecd6af250697dfd6a1e2ccd7bcf615087a790c5`; AffBloc45C72A..45C779 hash `99fbfda70e2038110ef2f75b657f7880296e512fc6a547bb8f0a690c8ed73c2e`. [New exact evidence](evidencias/passe-terreno.json) pins unchanged cache/object/catalog providers. Native originsEAX/EDX, terrain pointer507D70, window508724/+2, inset508F90, surface508F70.

Actual `python3 -B pesquisas-paralelas/graficos-animacao/validar_passe_terreno.py`: **65,536 predicate calls**, **80 full terrain calls** (72traces/8pixels), **20 standalone block calls**,2bank calls; **72,258 bounded segments /15,599,587 observed instruction hooks**. Original CPU/stack is retained between before/after-cell checkpoints through actual RET0x3000000/ESP0x2008004. Calls and segments are distinct counts. Zero expected/unexpected exceptions, limits or skips. Trace-only GetNumBob returns fixed validID1 and block/vegetation callbacks are intercepted; predicate/light logic is original. Pixel terrain/cache/block/object instructions are intact, comparing entire surfaces, IDs and all final cache state. Only bank IO/allocation/explicit synthetic cache-payload binding are fixture substitutions. World maps/attributes/clip/pointer table remain unchanged. [Native report](validacao/x86-passe-terreno.json), [bounded native terrain fixture](artefatos/cena-passe-terreno.png).

All predicate words, window dimensions1–32, corners/insets/empty views, substitution/hidden invalid sources, narrow object clip, unaligned opaque blocks and a full1024×1024 buffer are covered. Chosen ground assets commute under deferred ordering in these pixel fixtures; precise native callback traces establish block/object interleaving. Initial regression failures were unsupported Python3.9 `int.bit_count` and an invalid expectation of a pixel-order counterexample; neither required changing implementation or captured native evidence. Corrected regressions all pass: seven new tests, graphics domain **176 tests**, zero skips and valid links.

Concrete gap closed locally/independently validated: complete bounded nonwrapping terrain traversal, its exact fallback and opaque block/object composition over original assets. Synthetic world/cache inputs are not a mission or full frame. AffSprite/AffGame orchestration, negative/wrapped views, cache startup/lifecycle, real-mission initialization and consumer activation remain separate gaps. Overall estimate stays coordinator-owned; integration status follows helper.

## Sixteenth stage selected after fifteenth-stage integration

Stage fifteen implementation `9db0735a4f7a81a7b53993d84413420da7983d80`, final feature `506012c834d0994c3c6a02ae92a53cee8507aa17` and main merge `1c12c2fda0c36106e85178ba17f4237af2df5baa` were fetched and verified as ancestors of `origin/main`. The clean worktree then fast-forwarded to the seven-front organization `8a499a9`. The coordinator assigned `InitCache 0x40FA38` and the verified cache lifecycle (allocation, fill, replacement) through declared bindings only, replacing the terrain-pass validator's synthetic cache-payload binding.

## Sixteenth stage implementation and validation

Order kept: original-byte inventory, then original-only native captures committed alone as `e3152ea`, then translation, fresh native comparison, tests and docs.

**API** (`ciclo_cache_terreno.py`, full contract in [the manual](../../docs/GRAPHICS.md#terrain-cache-lifecycle--sixteenth-continuation-stage)):

- `MemoriaMotor(*, contador_u32, vinculos)` models MemAlloc/MemFree.
  - `mem_alloc(n_u32)`: counter 0x4E2F3C += n, then `global_alloc(0,n)` at 0x467EB9, then `global_lock(h)` at 0x467EC1.
  - `mem_free(p_u32)`: `global_handle` 0x467ED1 → `global_unlock` 0x467ED9 (ignored) → `global_handle` 0x467EE1 → `global_free` 0x467EE9, whose result is returned. It never subtracts.
  - The five bindings are callables returning u32. A missing binding raises `DependenciaCicloCache(address)` after earlier effects.
- `CicloCacheTerreno(blocos_crus_270336, *, proximo_u16)` is the post-LoadSTRATBank/SetBank state; `apos_carregar_banco(catalog)` gives the real BLOCS.CMP 1090–1345 payloads with cursor 0.
  - `alocar(memoria)`: CacheAlloc, `MemAlloc(1024)`; keys stay undefined (`registros is None`).
  - `iniciar()`: InitCache; zero keys, keep cursor and payloads, EAX 256.
  - `cache`: the live `CacheTerreno`, only while initialized.
  - `liberar(memoria)`: CacheFree; the stale pointer is kept.
- Refusals: a null or freed table raises at 0x40FA49; a second CacheAlloc at 0x40FA18; CacheFree out of order at 0x40FA2E; a key read outside the initialized state at 0x40FE50.
- Invalid widths and types raise `ValueError`.

**Inherited state and effects.**

- Inherited: payload bytes, the cursor and the MemAlloc counter. The pointer 0 comes from `.bss`.
- Effects, in order: counter, then bindings, then pointer store; then the key zeroing; then GetNumBob misses through the existing `resolver_bloco_terreno`; then MemFree bindings.
- No callbacks, RNG, clock or world state.
- Stale payloads and the cursor survive InitCache, so the next miss after a restart lands at the inherited cursor.

**Bindings.** `bancada_ciclo_cache.py` and `vinculos_graficos.py` bind only:

- the KERNEL32 IAT slots `0x5231C0/C8/CC/D0/D8` (GlobalAlloc/Free/Handle/Lock/Unlock), resolved to trampolines as the loader would;
- the C-runtime `fopen 0x48C71F`, `fread 0x48C97B` and `fclose 0x48C80B`.

The game wrappers, MemAlloc/MemFree, LoadSTRATBank, SetBank and the cache routines run unchanged. Every call logs exact arguments and the returned value. Requests the fixture cannot honor stop with `ParadaVinculo`: non-`GMEM_FIXED` flags, zero sizes, exhaustion, stale handles, non-`rb` modes, unknown names and short reads. The fixture declares GMEM_FIXED content as `0xA5`, and the bank path prefix as empty. **Migration note for core:** these stay local until core publishes the generic declared-binding facility in `ferramentas/emulador.py`. `MemoriaMotor` is the first Python MemAlloc/MemFree model; core may adopt it as a shared provider.

**Original identities.** Executable `6c556520…43fb` is the only oracle; normalized PE `26c4534b…64d0` is named and not executed. Region hashes:

| Region | SHA-256 |
|---|---|
| CacheAlloc..InitCache | `29e4373d…c3dc` |
| MemInit..MemClose RET | `b1c0ba63…c0dd` |
| LoadSTRATBank | `2682bf21…e9da` |
| File wrappers | `ad54bf31…67b7` |
| ProgInit window | `144952e5…2889` |
| CalculGame start | `4c0bf171…c636` |
| MenuNewSelect window | `d3f80619…4503` |

The full list and the static scan are in [evidencias/ciclo-cache.json](evidencias/ciclo-cache.json).

**Actual validation.**

- `capturar_ciclo_cache.py` (original-only): 554 native entries / 9,364,336 instructions / 97,294 bound calls, 547 GetNumBob calls, and the expected null-table fault at 0x40FA49.
- `validar_ciclo_cache.py` (fresh): 554 native entries / 9,364,346 observed instructions / 97,294 bound calls / **552 whole-state comparisons**. Each compares pointer, all 1,024 keys, cursor, all 256 payloads, the counter and the binding log. Branches: 3 undiscovered, 3 direct, 7 hits, 534 misses. Every original-only row is reproduced. There are 0 limits and 0 skips; the one expected fault matches the model's named dependency.
- `validar_passe_terreno.py` (migrated): real bank and lifecycle, InitCache before scenes `interior` and `large`, 72,261 segments / 16,013,021 instructions. All 8 surfaces, IDs and final cache states match; the PNG and `evidencias/passe-terreno.json` are byte-identical. The stage-15 report is superseded at this commit and recoverable from `9db0735`.
- Graphics domain: **184 tests**, 0 skips, links valid.

**Remaining synthetic bindings** (listed as the stage requires):

1. `bancada_x86.Bancada.carregar_banco_original` replaces `FileOpen 0x458420`, `FileRead 0x458461`, `FileClose 0x45844c` and `MemAlloc 0x467ea6` wholesale. It keeps no argument log, does not write the handle global 0x4E1D1C or the counter 0x4E2F3C, and allocates zero-filled memory from the harness heap. It is used by every graphics validator except `validar_ciclo_cache.py`, `validar_passe_terreno.py` and `validar_python.py`.
2. `validar_composicao.BancadaComposicao.carregar_paleta` stubs `FileOpen/FileRead/FileSeek 0x45848b/FileClose` around `LoadPalette 0x4798E9`.
3. `validar_objetos.py` (`0x46C3A2..0x46C3DE`) and `validar_construcoes.py` (`0x46C517..0x46C578`) stub `FileRead 0x458461` to feed mission bytes.
4. `validar_cache_terreno.BancadaCache` still has stage 14's synthetic cache-payload binding. Its 256 payload pointers point into one guarded RAM snapshot, and its explicit synthetic key/cursor states use keys FFFF/FF/FF, fill 82 and cursors 0/255, with the key table taken from the harness heap. It is kept deliberately for arbitrary-state coverage.

Bounded trace modes also intercept engine callees to record order; these are not external bindings, and the pixel modes run the callees unchanged.

- Blitters `PasteBobCmp 0x45B247` and `PasteOmbreCmp 0x45B796` are intercepted in the objects, construction, death, work, type-2, selection, attack and gate validators; `0x45BA23` additionally in projectiles.
- The structures validator intercepts `PastePlayerCmp 0x45C455` and `MurAjoute 0x43E616`.
- The sprite-pass validator intercepts its callees `0x415ACF`, `0x407DD3`, `0x40F49B`, `0x41591F` and `0x46FF70`.
- Terrain traces intercept `GetNumBob`, `AffBloc` and `AffVegetTerrain`.
- `capturar_desenho` intercepts shadow capture at `0x45B796`.

**Gaps.**

- Not covered: MemInit (`GlobalMemoryStatus`/`GlobalCompact`), DeleteBank, a Python LoadSTRATBank, GlobalAlloc failure, movable memory, palette lifecycle and wrapped/negative viewports.
- Not exercised here: AffGame orchestration (stage 17), and the mission/runtime consumer of the lifecycle. Nothing in this stage reached a real loaded mission.
- The first InitCache in a real session follows MissionLoad's caller branch; a mission snapshot must carry the cache state explicitly or start from `apos_carregar_banco` + `alocar` + `iniciar`.

Concrete gap closed: verified cache startup, restart and release over real bank payloads, with the terrain-pass validator consuming it. The overall estimate stays coordinator-owned.

## Seventeenth stage selected after sixteenth-stage integration

The coordinator accepted stage 16: implementation `c4bd7da`, captures `e3152ea`, feature `a4bb655` and main merge `21ebbee` are all ancestors of `origin/main`. It authorized `AffGame 0x417698` orchestration over the furthest committed MONDE01 checkpoint, with every world, clock, sort-list or palette write returned explicitly. The worktree merged main `9ae9071`, which opens the audio front in the macOS chat; audio is no longer proposed for graphics.

## Seventeenth stage implementation and validation

Order kept: original-byte inventory and native captures were committed alone (`077a05b`), then the translation, the fresh native comparison, tests and docs.

**Scope.** `quadro_jogo.compor_quadro` reproduces AffGame mode `0x12` from its entry to the HUD checkpoint `0x417B1C`. The full contract is in [the manual](../../docs/GRAPHICS.md#in-game-frame-orchestration-affgame--seventeenth-continuation-stage).

**Inputs.**
- `MundoQuadro` (read-only): terrain words, objects, auxiliaries, region words `0x4E0F38`, the unit pool, the projectile pool, and the four discovery and lighting maps.
- `EstadoTela`: 30 globals with exact widths, in `GLOBAIS_QUADRO`.
- The persistent `CicloCacheTerreno` (stage 16).
- The 256-byte shadow and lighting tables.
- The previous surface: pitch × screen height.
- `relogio`: the GetTickCount binding.
- `directdraw`: the `is_lost`/`restore`/`lock` binding.

**Order and effects.**
1. CalculFrame. Counter, ticks, FPS digits clamped to 99, and the `itoa` page text at `0x4963B4`.
2. EvenementEnCours. A flag only; it is returned.
3. The gate: frame `0x508F7C` mod divisor `0x497284`, unless forced by `0x4E05A2`.
4. DDLockSurface. Lock count, pointer, pitch 800, and `0x508F70`.
5. AffTerrain. GetNumBob cache writes and V6 terrain objects.
6. AffSprite, in the stage-5 order:
   - AffVeget uses the `0x415A58` code table.
   - AffBatiments' no-building path writes the saved clip `0x49A02C..32` and restores the clip.
   - AffEngin uses the routing plus the validated body guard.
   - AffProjectile uses the public renderer.
7. The checkpoint.

Every write is in the ordered `efeitos` list. A whole writable-memory diff of each native frame shows no other write: no unit, world, structure, RNG or palette write in the supported domain. The RNG cursor `0x4E1D18` and the palette cycling (`Cyclage`) sit only in unsupported branches or after the checkpoint.

**Partial failures.** `DependenciaQuadro(address)` keeps the partial surface, the trace and the effects. A missing binding stops at its call site:
- GetTickCount at `0x43F71A`, after the counter increment;
- IsLost at `0x43F3D7`, Restore at `0x43F3E4`, Lock at `0x43F40C`.

**Bindings.** On top of stage 16:
- KERNEL32 `GetTickCount` (IAT `0x5231B8`).
- The `IDirectDrawSurface` vtable methods on the COM object `0x4E1790`. The fixture is never lost; Lock fills `lpSurface`/`lPitch`; Restore and Unlock stop.

The native bench runs PaletteAlloc, LoadSTRATBank/SetBank, CacheAlloc and CalculTabPlayer in ProgInit order. The player tables equal `construcoes.tabelas_jogador()`; the shadow and lighting contents are the real 60% tables from earlier captures.

**Original identities.**
- Executable `6c556520…43fb`; normalized PE `26c4534b…64d0` is named only.
- `AffGame 0x417698..0x417F38` hash `0eeac1ce…583a`; `CalculFrame` `ec7f8002…a592`; `DDLockSurface` `3b685f16…4b34`; AffBatiments prefix `616969e1…1be9`; AffBatiments switch/tail `d8fa5152…4fa7`; AffVeget table/prefix `4f9c9cad…b526`.
- [Inventory](evidencias/quadro-jogo.json), including the DDInit, WndProc and ResetMode configuration and a static absolute-write scan.

**Actual validation.**
- `capturar_quadro.py`, original-only: 21 native entries / 23,908,934 instructions / 97,331 bound calls over seven frames. It was regenerated on the advanced checkpoint; the first capture is `077a05b`.
- `validar_quadro.py`, fresh: 26 native entries / 44,585,739 instructions / 97,346 bound calls.
  - **Six complete frames** with whole-frame equality: the 800×600 surface, the canonical trace, all 30 globals, the cache state, and a memory diff restricted to those globals.
  - **Three named stops**, compared at the same original address after the same trace event, with native memory restored first:
    - MONDE01 at facade trigger `0x2ED` (`0x40F23B`);
    - the selection box (`0x417AC8`);
    - real MONDE01 terrain with synthetic visibility (`0x40F23B`).
  - Every fresh frame reproduces its original-only capture. There are no limits and no skips.
- Graphics domain: **192 tests**, 0 skips.

**MONDE01 checkpoint (real mission state).** The input is missions' committed load plus the `MissionPlaceTerrain` unit scan.
- With core's integrated discovery domain, all 16 units are placed, up to the pre-structure checkpoint `0x46C16D`.
- The first integration attempt failed its common gate because main had advanced this checkpoint under the tests' live pipeline. The candidate is preserved at `worktrees/integration-graphics-a0f20f22`.
- The buffers are now pinned in `evidencias/monde01-checkpoint-quadro.{zlib,json}` with their checkout revision, and the capture was regenerated natively.

The native frame reaches `0x417B1C` (2,201,940 instructions). The model draws the whole terrain pass and sprite rows 0–13, then stops at the type-2 structure facade trigger, cell 3345 = (17,13). Next blockers, in drawing order:
1. that facade, with structure lookup;
2. the unit overlays: MONDE01 units have `+0x74 = 0`;
3. unit types 1 and 8.

[Preview](artefatos/quadro-monde01-parcial.png).

Declared synthetic inputs:
- From missions: the unit pool pre-fill, regions, selections, search context and bonus table.
- From this stage: viewport origin (0,0), camera 0, the frame counter, the 800×600 mode, zero projectile and structure pools, and the background surface.
- DirectDraw locks a single fixture buffer; page flips are not modelled.

**Planned graphics → macOS contract** (requested by macOS; answered in the shared notes and now recorded here). `compor_quadro` is the frame entry. The requested keywords `jogador_camera`, `origem`, `janela_celulas` and `margem_i8` are `EstadoTela` fields at `0x508041`, `0x508720`, `0x508724` and `0x508F90`. `Quadro` returns the surface, the renderer trace, the ordered effects, `desenhado` and `parada`; the cache is the caller's persistent object. The palette is the loaded PIE palette, since the prefix does not change it.

Corrections sent to macOS:
1. **InitCache is not per frame.** Create the cache once (`apos_carregar_banco` + `alocar`), call `iniciar()` at game start or restart, and thread the same object through every frame.
2. **A read-only world is now established only for the supported domain**, by whole-memory diffs. Effects are explicit.
3. **Default window.** 25×17 cells at 800×600 (`DDInit`), pitch 800. The 640×480 mode stops until the stride is validated.
4. **Draw cadence is ai-runtime's.** AffGame's own gate is `frame mod divisor`, with divisor 1 initially.
5. **HUD, minimap and cursor are out of scope.**

The app's clamp (`origin + window + 8/10 ≤ 256`) matches the sprite domain.

**Remaining synthetic bindings and limits.** The stage-16 list is unchanged: wrapper-level bank/palette/FileRead stubs in the older validators, and the stage-14 synthetic cache snapshot. Stage 17 adds no synthetic payload binding. Shadow and lighting contents enter as explicit tables because `LoadPalette`/`CalculOmbrage`/`CalculEclairage` are not run in the frame bench.

Not composed:
- the HUD tail after `0x417B1C`;
- the clear and background-restore paths;
- the selection box;
- facades, structure lookup and the workshop;
- AffVeget handlers 27 and 55–65;
- units outside the guard;
- the 640×480 mode;
- wrapped or negative viewports.

Stage 18 (wrapped and negative viewports, and the MONDE01 building facades) is next, after coordinator confirmation.

## Codex recovery — light facade inventory only, 2026-10-28

The new human authorization superseded the old STOP. Before writes, the existing
graphics branch was clean with no local commits outside fetched main. Resumed
through `python3 scripts/workstream.py start graphics`, then fast-forwarded
without resetting to `b610bfad77ffadaa0ee5f6af02160d786ccfdc7b`. Existing Claude
research and failed candidates were preserved. The coordinator later restricted
this recovery round to the already-started light inventory; no further graphics
implementation or heavy work is authorized in this round.

The [reviewable readiness inventory](INVENTORY_MONDE01_FACADE.md) records exact
original intervals, inherited inputs, order and failure boundaries. Fresh
read-only checks verified the intact executable identity, eight interval hashes,
all pinned MONDE01 buffer hashes, and stage-17 implementation/correction/merge
ancestry. At the first terrain trigger (cell3345, word0x2ED), the pinned occupancy
word is0x0001, so the original inline lookup returns0xFFFF and branches directly
to the caller epilogue. The pinned scene is not proof of a drawn structure.
A placed type-2 facade must use a new explicit snapshot; predecessors stay fixed.

| Scope | Implementation | Original validation | Main integration | Full flow |
|---|---|---|---|---|
| Existing stages16/17 | Bounded providers already exist | Historical native captures/comparisons; not rerun in this recovery | Already on main; stage17 merge0756062 freshly ancestry-checked | Pinned pre-structure checkpoint, no accepted complete M1/frame runtime |
| Facade/lookup continuation | No new code | Fresh static review only; no new x86 capture/comparison | Inventory only; no integration in this turn | Not run |

Historical graphics domain192/0skips remains historical. New native validation,
Ghidra, domain/common gates and integration were **not run**, rather than marked
passed or skipped. Only lightweight static/hash/Git/whitespace checks ran.
No app rebuild or follow-up dispatch was made. The next valuable slice is exact
missing/present structure lookup plus the proven Santuário body/caller boundary;
overlays for unit+74=0 and types1/8 follow only in a later scheduled round.
No model difficulty or unresolved auto-review rejection was observed. Stop after
preserving this inventory and reporting readiness; do not poll for another task.

## Render API 1.3: unit types 1 and 8 (2026-10-29)

Goal: move the render API past its first stop `0x41591F` ("unit body outside its validated domain"), which hit MONDE01's unit 15 (type 8, `VOLEUR`) and unit 11 (type 1, `GARDIEN DU FEU`) in every M2.2 frame. Worktree merged `origin/main` (`8e90beb`) first.

**Order kept (original first).**
1. Evidence commit `a5011bb`: `capturar_corpos_tipos1_8.py` and `evidencias/captura-corpos-tipos1-8-m22-v2.json`, original only, before any translation. Missions' -v2 display bench runs to the real AffGame entry of `between_frames(1..6)`; AffGame runs natively to `0x417B1C` with a stop at each AffEngin entry. Each type-1/8 call is rerun as a native leaf call from the paused state, with hooks that only record (blitter arguments, routine entries, body-routine block path, RNG cursor, ±96-pixel surface crops). A 592-call matrix rewrites record bytes from the same restored state: states 2/7 × directions 1–16 × all phases below the count, three shifts with life 100, five life words. 12 real-state calls and 592 matrix calls, all returned, record and RNG unchanged, surface difference inside the crop. Phase-end hashes of the six frames equal Missions' recorded hashes.
2. Translation: `corpo_tipos1_8.py` (shadow 10784 at `(x+dx+2, y+dy+26)`, then body `base + (floor((dir+1)/2)−1)·[+A5] + [+A4]` at `(x+dx−ax, y+dy−ay)`; type 1 base 2290, anchor (23, 9); type 8 base 2450, anchor (32, 30)), wired into `quadro_jogo._Composicao.engin` followed by the existing tired-icon tail. `render_quadro.VERSAO_RENDER_QUADRO = (1, 3)`.
3. Static byte provenance `evidencias/corpo-tipos1-8.json` (intervals and constants, pinned capture hash).

**API inputs and domain.** `consultar_corpo_tipos1_8(registro276, *, x, y, indice_u16, camera_u8, indice_selecionado_u16, modo_selecao_u8)`; `compor_corpo_tipos1_8(catalogo, destino, largura, altura, registro276, *, ..., tabela_sombra, recorte=None) -> (bytes, plan)`. The domain is only what the capture covers: owner 0 under camera 0, states 2/7, `+0x99 = +0xBA = +0xBD = +0xDC = 0`, not selected, selection mode 0, count 8 (type 1) or 10 (type 8), direction 1–16, phase < count, any i8 shift. Everything else is `NotImplementedError`, which the frame reports as the named stop `0x41591F`. No callbacks, no writes; inputs are unchanged.

**Validation.**
- `test_corpo_tipos1_8.py` (7 tests): the 12 real-state crops equal pixel for pixel; all 592 matrix crops equal the native SHA-256; layer arguments equal the native blitter arguments; out-of-domain bytes stop; the capture hash is pinned.
- M1 / M2.2 frame 1 fixture: no stop, all 480,000 pixels equal the native checkpoint (1.2: first stop at unit 15, differences below row 279).
- Fresh native sequence rerun, `capturar_serie_quadros.py --quadros 12` → `evidencias/verificacao-cadeia-m22-v2-api13.json`: no stop in frames 1–12; over the native previous surface every frame equals the original checkpoint (0 pixels); the chained render differs only in rows ≥ 547 (HUD after `0x417B1C`, out of contract); initial surface and cache artifacts reproduced byte for byte. The 1.2 report stays unchanged.

- Fresh native rerun over the whole accepted M2.2 playback, `--quadros 128` → `evidencias/verificacao-cadeia-m22-v2-api13-128.json`: no stop in 128 frames; 128/128 phase-end hashes equal the recorded ones, 128/128 carried caches equal the native cache, 128/128 frames equal the original checkpoint over the native previous surface; chained differences only from row 547 (HUD). No first stop remains in the M2.2 playback.

**Native runs (shared lease, this MacBook).** Smoke capture of one frame 98.6 s (scratch output, discarded); evidence capture of six frames 110.8 s; 12-frame verification 111.0 s; 128-frame verification 441.1 s.

**Gaps.** Types 1/8 outside the domain above (other owners/cameras, oscillation and its RNG, effects, overlays, attack/work/construction/death routes, other counts/directions/phases) still stop at `0x41591F`. Types other than 0, 1, 5, 6, 7, 8, 9 have no frame body. The HUD tail after `0x417B1C` is still not composed.

## Render API 1.4: HUD tail and cursor (2026-10-29)

Goal: let the frame render reproduce everything AffGame draws after the HUD checkpoint `0x417B1C` in the no-input M2.2 states, so the chained render equals the original's full 800×600 phase-end surface. Worktree merged `origin/main` (`5fbef82`) first.

**Order kept (original first).**
1. `4efa3ea`: the capture script `capturar_hud_m22.py` (original only).
2. `6f753ad`: the evidence `evidencias/captura-hud-m22-v2.json` (SHA-256 `94086e38…fed5`), committed before any translation. For every `between_frames(k)`, k = 1..128, AffGame runs natively to `0x417B1C` and on to `0x417D30` (the DDUnlockSurface call; AffGame writes the offscreen surface no more after it). Recording-only hooks log routine entries with registers and stack words, the surface hash at each tail call boundary, DGROUP and arena reads-before-write, DGROUP and arena writes, and every offscreen pixel written. The native end-of-drawing surface equals the end-of-phase surface and Missions' recorded hash in 128/128; no pixel changes outside the written set. Touched pixels (checkpoint and end values) are stored for the first frame of each distinct call sequence (frames 1–8); hashes for all. A frame-1 matrix of native leaf calls from the paused checkpoint state: 195 `AffCompteurMatiere` (3 resources × 13 values 0–9999 × 5 highlight bytes) and 5 `AffMiniMap` view origins; all returned, nothing changed outside the crop. Native run 325.5 s.
3. Translation `hud_quadro.py`, the opt-in `hud=True` of `render_quadro.renderizar_quadro`, `VERSAO_RENDER_QUADRO = (1, 4)`; static byte provenance `evidencias/hud-quadro.json` (22 intervals, `extrair_proveniencia_hud.py`).

**API.** `renderizar_quadro(..., hud=False)`: default is exactly 1.3. `hud=True`: after a complete playfield (no stop, frame drawn) `compor_hud(LeituraHud(memoria, prefix writes overlaid), pixels, catalogo, evento)` runs AffGame's tail. `regioes_necessarias(memoria, hud=True)` adds the minimap buffer (`[0x507D5C]`, `[0x496FE0]×[0x496FE2]`) and the player table (`[0x5080A8]`, 100 bytes). Output fields unchanged; HUD calls are appended to `chamadas`, the mouse-position copy `0x49A042/44` to `efeitos`.

**Order and domain** (`hud_quadro._Hud.compor`): three `AffCompteurMatiere` (x `0x1EC/0x21C/0x24C`, y `0x22D`; value ≤ 9999; thousands as up to four `0x2A3C` icons at y−9, leading blanks `0x2A21`, digits `0x2A22 + 2d + highlight bit`); `AffZoneIconeAction` only while `[0x4E05A2]` ≠ 0 and only with all slot words `0x29B1` (empty); `AffTrame` returning (mouse outside the view or `[0x4E05AE]` ≠ 3); marker `[0x496204]` = `0xFFFF`; `AffMarche` state 0 or > 4; `AffMiniMap` when `[0x497285]` ≠ 0 (frame box colour `0x14`, row copy with the constant stride 800, view box colour 1, both clipped to the clip words); `AffChrono` with no selected structure; `AffZoneInfo` panel bob `0x29B8` with zero cost counters; `AffInfoAide` with a NULL tooltip; no AffDebug, no event, empty message queue, no alliance/contact for players 0–3; then the mouse copy and the cursor bob `[0x49A010]+[0x49A014]` at the mouse position, clipped, when `[0x49A054]` = 0, with `[0x4E062C]` = 0. Each other branch raises `DependenciaQuadro` at its original address (`ENDERECOS_PARADA`, 17 stops). Observed in M2.2: counters 0/10/20/30, highlight bits 0/2, force flag on in 31 frames, cursor 7640 at (400, 300) in frame 1 and (0, 0) after, minimap 128×128 at (0, 0) over a 64×64 map.

**Validation.**
- `test_hud_quadro.py` (6 tests), each frame of the capture as a sparse memory holding only the bytes the original read: the blitter and Box arguments equal the native ones in all 128 frames; in the 8 representative frames the written pixels equal the native end values and no other pixel is written; all 200 matrix crops equal the native SHA-256; out-of-domain branches stop at their addresses.
- Fresh native chain rerun `capturar_serie_quadros.py --quadros 128 --hud` → `evidencias/verificacao-cadeia-m22-v2-api14-128.json` (441 s): no stop. The chained render equals the original's complete 800×600 end-of-phase surface, and its SHA-256 equals Missions' recorded hash, in **128/128**; the render over the native previous surface and the carried cache match in 128/128 as well. There is no first differing frame, and the initial artifacts are reproduced.
- Graphics domain gate: 244 tests, 0 skips; common gate `scripts/check.py` passes.

**Native runs (shared lease, this MacBook).** Smoke runs of 2, 6 and 2 frames (78, 89 and 86 s, scratch output, discarded); evidence capture of 128 frames 325.5 s; 128-frame chain verification 441 s (a first attempt failed after its native run on a report-key collision and was rerun).

**Gaps (named stops, waiting for the M3 scripted-input captures):** the selection drag box `0x417AC8`, structure selection frame/gauge `0x4022C8`/`0x4020EC`, non-empty action icons, the placement frame, the target marker, the market panel, AffChrono's recruitment gauge, cost counters, tooltips, message boxes (`AffText`), alliance flags, events, the second cursor bob, counters above 9999. After `0x417D30` AffGame unlocks and flips, runs `Cyclage` (palette only) and `ShowCursor`, and resets `0x4E05A2`; these change no offscreen pixel and are not part of the render result.

## Render API 1.5: M3 input-time display (2026-10-29)

Feature-only delivery for coordinator review; no main merge or milestone acceptance. Main was fast-forwarded to
`d9f70ba` before research. Original-only evidence was committed first: `5b05e41` (71 native full AffGame draws), then
`5405033` (43 fatigue/shift/sanctuary boundary cases). See [M3_INPUT_RENDER.md](M3_INPUT_RENDER.md), the two native
captures and `entrada-m3-proveniencia.json` for exact cases, original bytes/hashes and method.

**Original-first method and identity.** Intact RISING.EXE SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`. The display bench pauses at frame 1's first
ProcessInputGame, restores CPU/mapped state/stack/DirectDraw/surfaces for each case, runs native EnginAddSelection or
BatimentSelection and CalculIconeAction, applies declared writes, then runs original AffGame to `0x417D30`. Hooks
only record. All 114 calls reach the endpoint; both runs reproduce load_tail/between_frames/frame1 and unchanged
code after restoration. Native runtimes: 173.655 s and 135.315 s, MacBook heavy lease. Earlier 38-case smoke: 129.439 s;
one expanded attempt was interrupted at startup to add the grayscale lookup buffer, with no result claimed.

**Public API and inputs.** `render_quadro.VERSAO_RENDER_QUADRO = (1, 5)`; `renderizar_quadro` and its output fields are
unchanged. `hud=False` gains playfield overlays/drag; `hud=True` also gains action/cost/target/cursor branches.
`regioes_necessarias(memoria, hud=True)` additionally declares `[0x4E24BC]`, 256 grayscale lookup bytes. All other new
inputs are already in DGROUP or the unit pool. The memory view remains read-only; the terrain cache is still carried
explicitly. Economy's real `habitado(index)` callback is required in the same places. No new callback/default exists.

**Supported domain and order.**
- Normal owner-0/camera-0 units of types 0/1/5/7/8, states 2/7; initialized counts 8/8/8/8/10 and existing body
  direction/phase bounds; no oscillation/effects, fatigue words `+4 = +0x76 = 4`, health `+0x9A` 0..100 with type maximum
  100, unit bag capacity 0/1. Selection frame (`0x4124C4`, bob `0x2A1E`) precedes shadow/body. Selection `+0xBD`, hover
  `0x496AC2` or nonzero mode `0x508F8F` invokes AffInfoSelection `0x410BE4` after the body instead of the ordinary tired
  tail: background/fill health boxes, fatigue icon, builder experience, then the empty capacity-0/1 bag exit. Builder
  XP levels 0..7 and `+0xBA` modulo-5 blink are supported; unselected XP follows the existing tired tail. Signed shifts
  are retained. Selected `+0x82` order markers and non-builder nonzero XP remain named stops.
- `0x4022C8`/`0x4020EC` are structure frame/gauge helpers. The inhabited owner-0 mode-5 type-2 sanctuary is supported,
  with health 0..600/max600, `+6 = 0`, 16 bag slots (eight troops then eight empty), and zero recruitment word `+0x74`.
  Only its facade trigger emits the overlay: four player-colored corners using clock `0x508F80 & 7`, then gauge and
  contents. Hover invokes only the gauge. Nonzero `+6` reaches a visible stop at `0x4085CB` before the base facade;
  the pinned facade provider is unchanged and the field is not silently passed as zero.
- HUD: populated action slots of kind 1, disabled kind 0 percentage 0..100, numeric kind 2 value 0..999; both scroll
  buttons and selection frames; all cost-counter priority branches with values 0..9999, including selected builder
  and sanctuary. Native builder 12 shows structure types 1–4, CAVE in slot 2 (input rectangle (151,548)–(209,598)).
- Drag Box `0x417AC8` preserves reversed endpoints and native clipping. Target `0x417BA2` increments animation first
  on even counters, draws with the camera's player table, then resets after ID `0x1E0A`; effects preserve that order.
  Marker input IDs `0x1E03..0x1E09` are supported. Second cursor `0x417CFC`: count 1..16, ID=cursor_base+16−count.

**Proof.** `validar_entrada_m3.py` and `test_entrada_m3.py` replay the immutable native captures through the public
renderer. A validator-only observer records every Python raster call, including existing bodies/facades, without
changing the API's calls or pixels, and compares the entire blitter/Box/FilledBox sequence argument-for-argument.
Complete cases compare all 480,000 indexed pixels and all DGROUP bytes after projecting exported effects and the
returned cache cursor. GetTickCount uses the observed native answer per case. Only the two process-local DirectDraw
pointer fields (`0x4E17A4`, `0x508F70`) are excluded from DGROUP comparison. The damaged-sanctuary case verifies the
native argument prefix and dependency stop; no full-surface or final-state equality is claimed for it.

**Remaining stops/gaps.** Tooltips `0x40F8C0`; selected-unit order markers; non-builder experience; nontrivial unit bag
contents; other owners/types/effects/oscillation and work/build/attack/death bodies; sanctuary damage/fire input `0x4085CB` (native fire join `0x408AC1`); other
structure modes 0/1/2/6/7 `0x408AC8`, uninhabited states `0x40892D`/`0x40863E`; placement frame `0x41729B`; recruitment
`0x401D18`; market, events, messages, alliance/debug and out-of-domain values retain visible stops. No scripted-input
capture is available: these are native leaf-created display states, not replay of WndProc or accepted M3 gameplay.
No longer native run or Mac mini run is required for this bounded slice.

**M3 comparison result.** `validacao/entrada-m3-api15.json`: 114 cases, 113 complete surface/state comparisons,
1 declared fire dependency stop, 0 mismatches. All 54,240,000 complete-frame palette indices match, as do 12,417 raster
arguments (including the native prefix of the stopped case). Whole DGROUP projection has zero differences in all
113 complete cases after the documented DD pointer exclusions. Pure-Python replay runtime: 14.248 s. The report pins
the hashes of every changed production source and of the validator. `test_entrada_m3.py` replays it afresh and checks
unsupported-domain stops and read-only memory; it also binds the fresh 128-frame report to the unchanged 1.4 hashes.

**128-frame regression.** `evidencias/verificacao-cadeia-m22-v2-api15-128.json`, fresh original-x86
`capturar_serie_quadros.py --quadros 128 --hud`: 128/128 complete chained surfaces equal the original's full phase-end
hashes, 128/128 renders over the native previous surface equal, 128/128 carried caches equal, no stop and no first
difference. Lease execution runtime: 482.844 s (2026-10-29 19:58:09–20:06:12 UTC), below 20 minutes; queue time is
excluded. Fresh initial surface/cache artifacts are under `validacao/`, and their payloads match the unchanged 1.4
artifacts. The compatibility correction only preserves the old globals schema and pinned facade provider; the new
drag coordinates use the existing live read view.

**Validation history and dependencies.** A preliminary domain run (240 tests, 1 failure/2 errors, log preserved as
`validacao/api15-graphics-tests-precheck.log`) exposed the old exact-globals fixture, the immutable predecessor source
hash, and the not-yet-produced 128-frame report. The globals schema and pinned `construcoes.py` source were restored;
no fixture, original capture or predecessor manifest was changed. The M3 comparison was rerun after those fixes.
Historical unrelated x86 matrices were not rerun. Core/Missions must expose original initialized text/font state
without AffText substitution before tooltip pixels can be captured; Missions' scripted-input/WndProc scenario is
still needed for a chained M3 input proof. These gaps do not require a longer MacBook run for this delivered domain.

**Final gates.** `python3 -B scripts/check.py --domain graphics`: **248 tests, 0 skips, PASS**, 54.524 s under the heavy
lease; documentation links pass. The final replay is 14.248 s, 114 cases / 113 complete / 1 named dependency / 0
mismatches. A second compatibility run (248 tests, 2 failures, preserved in
`validacao/api15-graphics-tests-compatibility.log`) identified exact legacy stop expectations when the low-level
compositor has no live read view; those stops are preserved and the final gate passes. The public 1.5 renderer supplies
the read view explicitly. The legacy globals set, predecessor source hashes and every frozen native fixture remain
unchanged. No historical native suite was silently substituted for the new M3 or 128-frame proofs.

## Render API 1.7 — scripted CAVE display (2026-10-29)

**Original first.** Main was fetched/merged before research (`ea62eb4`, descendant of accepted 1.5). The Missions
probe ref `f0588447b6cea3cc10701233a55bbcd16551e5e5` was read with git-show and never merged. Native evidence commits
are `9a05e69` (initial recordings and declared 160-case matrix), `9a1f846` (recorded AffText boundaries, gray/shadow
tables and saved backgrounds), and `51fc02e` (600-case matrix including every CAVE construction health value).
The translation commit is the commit carrying this section. The executable identity is unchanged:
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Native WndProc replay independently reproduces 1,274 published phase surfaces and whole-state hashes; hooks only
record original display execution. AffText remains the Missions bench's explicit non-executed boundary.

**API and domain.** `VERSAO_RENDER_QUADRO = (1,7)`. Existing positional/result/cache contracts and 1.5 outputs remain
unchanged. `renderizar_quadro` gains optional `texto(request, indexed_surface) -> bytes`; without it, the native
tooltip frame is returned with a visible `0x459454` dependency. Request keys are original text bytes, x/y/right/bottom,
font and flags. `regioes_necessarias` adds the gray table `[0x4E24C4]`, the pending raw background `[0x49A03C]`
(width `[0x49A04A]` × height `[0x49A04C]`), and, with HUD, tooltip shadow `[0x4E24B4]`. No input memory is written.

`cave_scriptada_m3.py` handles uninhabited type-2/3 facade triggers (`0x2ED`/`0x30D`, `0x40F23B` family), modes
0/1/2/6/7 across full health 0..maximum, and uninhabited modes 3/4/5. Mode 3 consumes three permutation bytes and
exports each RNG-cursor write before drawing; clipping is restored by AffBatiments before its existing tail. Full
CAVE uses seven plain and seven destination-gray layers, including the native three-pixel difference on layer 7119.
Inhabited sanctuary continues through the frozen predecessor provider. Inhabited CAVE remains `0x40958E`.

Selected owner-0 builder construction uses the existing verified fixed-stride formula for tasks 0/1, states 11/15
and no queue/effects/oscillation, with selection frame then shadow/body then AffInfoSelection/fatigue/experience tail.
P3 contributes selected state-11 walk/work bodies. Selected cell orders (`+0x82=1`) add their viewport-clipped two
markers before the normal walk body; mode 2 remains `0x412923`. Existing input-overlay bag/health/fatigue/type guards
remain visible. Other body routes, owners, queued builder, damage/fire and structure-selection domains are unchanged.

`hud_scriptado_m3.py` composes the type-3 5×5 CAVE placement gray grid/invalid-cell outlines (`0x41729B`), expired
CONSTRUTOR/ARMAZÉM tooltip layout/frame/shadow, background save and following-frame PasteBob restore (`0x4179E1`).
Only the captured single-byte font mode, suffix 0xFFFF and screen coordinates are accepted. Unknown tooltip strings/
font/suffix remain `0x40F8C0`. Glyph rendering is a `0x459454` dependency. GetBob exports `saved_background_pixels`
as a write-only effect (empty old hex, complete new raw pixels); carry it with display globals, cache and surface.
Callback order is save background → Box → FilledBoxOmbre → text provider → cursor. Default absence never skips text.

**Comparison qualification and results.** The validation-only `FronteiraTextoGravada` accepts the declared native
AffText non-execution only after exact text/font/rectangle/flags and whole partial-surface verification. It is never
a production default. Under that explicit probe contract, full chained surface equality is P1 501/501, P2 601/601,
P3 172/172 (129–300), with zero drawing-argument and projected-DGROUP differences (only the two existing DD binding
pointer fields excluded). The chain carries the Python-produced background, surface and cache and checks them at
native entries. Normal rendering without text provider stops first at P1 170, P2 219, P3 141, after 41/90/12 complete
prefix frames. Native partial pixels and argument prefixes match exactly at all three stops.
The combined current-source report is `validacao/sondas-api17-final.json`: 139,876 drawing calls and 1,037 attested
text boundaries. The inhabited sanctuary retains the 1.5 habitation-provider call order; its already queried false
result is passed explicitly to the new uninhabited provider, without a repeated economy callback.

`validacao/matriz-cave-toda-vida-api17.json`: 600/600 original leaf cases, 0 pixel/argument/effect mismatches. This
includes all 101 CAVE health values in each construction mode plus sanctuary threshold and RNG cases. It does not
claim completion of the actual P3 chain through frame 1812. The native calls use exact restored frame-220 state and
declared writes; previous captures, hashes and predecessor sources are unchanged.

Fresh `capturar_serie_quadros.py --quadros 128 --hud`: **128/128** full surfaces equal the original and unchanged
1.4/1.5 phase hashes, both chained and over the native previous surface; all carried caches equal, no stop or first
difference. The final source rerun's log wall interval is 450 s including lease startup; its report is byte-identical
to the first 482-second 1.7 run. The same 114 API-1.5 cases remain in the graphics gate;
the historical source report is pinned to its actual `06ef8f1` source revision, rather than requiring new additions
to have old source hashes. Frozen report bytes remain untouched.

**Remaining work.** P3 301–3129 needs native capture on the Mac mini (exact bounded commands in M3_CAVE_RENDER.md),
including completed CAVE at 1812 and later builder behavior. P4/P5 were not consumed. Full glyph drawing needs a
native text-enabled oracle capture; current probes deliberately do not execute it. Other facades/fire, inhabited
CAVE, nontrivial contents, other unit body routes and prior market/recruitment/event/message/alliance/debug stops
remain. No M3 acceptance or integration is recorded by this front. All native runs used the MacBook heavy lease and
stayed below 20 minutes; no multi-thousand-frame run was started here.

**Validation history.** The preserved `validacao/api17-graphics-tests-precheck.log` reports 248 tests with one
failure/two errors: an obsolete uninhabited-stop test lacked the newly required gray buffer, a sparse invalid-tooltip
test attempted an undeclared read, and the inhabited construction stop address needed compatibility preservation.
The fixture remains unchanged; missing regions now remain explicit read errors, invalid pointers stop before use,
and the historical inhabited stop address is preserved. The first complete 1.7 gate passed 254 tests with zero skips
in 86.892 s. After callback-order review, the combined source-pinned probe comparison again passes in 296.810 s,
and the final leased domain gate passes **254 tests, zero skips**, in **87.702 s**; documentation links also pass.
The final gate log is `validacao/api17-graphics-tests-final.log`.
Historical native matrices were consumed by the graphics suite; they were not recaptured. Full P3, P4/P5 and glyph
execution are skipped for the concrete evidence/runtime gaps above.
