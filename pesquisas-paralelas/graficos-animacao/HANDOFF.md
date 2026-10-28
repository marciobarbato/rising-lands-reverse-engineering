# Graphics handoff

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
