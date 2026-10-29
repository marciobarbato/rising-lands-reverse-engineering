# Graphics and animation contract

Owner: graphics. Active implementation, synthetic/reference tests, indexed-buffer artifacts, and original-byte extracts live in `pesquisas-paralelas/graficos-animacao/`. Historical frozen releases are immutable records in the workspace archive and in the pre-organization Git history. Never edit a frozen release's text or inputs to modernize it: its manifest hashes identify the exact original record.

## Banks, pixels, and palette

The concatenated bank order is `BLOCS`, `TROOPS`, `VEHICULE`, `CREATURE`, `BUILDING`, `OTHERS`, with counts 1,345 / 2,848 / 915 / 1,920 / 611 / 4,517. Engine graphic IDs start at **1**; local/global API indices start at **0**. `INVENTE` and `MENU` are separate banks. Use `localizar`, not a guessed equality between an engine ID and a file index.

`graficos.py` reads CMPs with a separate opacity mask: a literal palette index zero stays opaque. A transparent skip is not the same as literal zero. Preserve clipping, source anchors, indexed pixels, and destination state before converting to RGBA. `Catalogo` verifies copied input files against `fontes/manifesto.json`.

The current graphics reader's palette behavior is authoritative for graphics tests. Earlier prototype palette expansion was a preliminary implementation; do not silently use it as the current original-renderer oracle. `composicao.py` reconstructs palette/shadow tables and composition. Shadows remap the destination through a 256-byte table under a CMP mask; they are not a black alpha overlay or a second dark sprite.

## Unit and building coverage

The verified unit bodies cover type 0 `SOLDADO`, 5 `FAZENDEIRO`, 6 `MECÂNICO`, 7 `CONSTRUTOR`, and 9 `COLONO`, including recovered stop/movement frames, anchors, direction, and bag-related branches where supported. Keep original French INI keys and recovered offsets. Do not generalize a soldier's frame groups to every unit type or infer a complete action from a visual strip.

`construcoes.py` provides verified Sanctuary facade layers, player tables/clocks, and structure ETA reading. A disk record, a prepared runtime structure, its physical gate counter, and a render plan are different data contracts. Graphics consumes explicit simulation state; core owns collisions and gate progression. New gate sprite associations require byte/address evidence and indexed-buffer comparison, not the apparent shape of a frame.

## Gate facade contract — 2026-10-28

`portoes_graficos.py` adds `consultar_portao` and `compor_portao`, independently of physical gate progression. The caller must resolve an existing structure occupancy label to a prepared **type-12 `HERSE` runtime record** and an object-code **253** cell. The API does not read an ETA record, allocate a structure, or derive state from an image.

All inputs are required keyword arguments. Integers exclude Python booleans.

| Input | Width and supported values | Original source |
|---|---|---|
| `contador_u8` | u8, public domain 0–31 | Runtime record `+0x76` |
| `orientacao_u16` | u16, 0–65535; zero versus any nonzero | Runtime record `+0x7C` |
| `valor_0a_u16` | u16, 0–65535; raw value without economic interpretation | Runtime record `+0x0A` |
| `jogador`, `camera` | Owner 0–4; camera 0–3 | Record `+0x04`; global `0x508041` |
| `modo_u8` | u8, 0–255 | Record `+0x05` |
| `visibilidade_u8` | u8, 0–255 | Record `+0x110+camera`, four in-record camera slots |
| `descoberta_u8` | u8, 0–255 | Separate per-camera cell map, pointer array `0x507D78` |
| `x`, `y` | i16, −32768–32767 | Projected cell origin, original `AX` / `DX` |
| `janela_celulas` | Pair of u16 values, each restricted to 1–1024 | Window width/height in cells at `0x508724` / `0x508726` |

The original first rejects a foreign-owner record when mode is not 3 and its camera visibility byte is zero. It next rejects a map cell with discovery bit 16 set; other bits do not independently suppress this branch. Accepted records save the incoming clip, replace it, then issue **one `PasteBobCmp` with clipping enabled**:

| Orientation | Engine IDs for counters 0–31 | `BUILDING.CMP` local indices | Draw position |
|---|---|---|---|
| Zero | 7576–7607 (`0x1D98 + counter`) | 547–578 | `(x, y)` |
| Any nonzero u16 | 7608–7639 (`0x1DB8 + counter`) | 579–610 | `(i16(x+5), i16(y+4))` |

There is no recoloring or shadow call in this facade branch. `compor_portao` preserves transparent skips, opaque palette indices, and the supplied destination; it returns new indexed bytes. No original gate frame contains an opaque literal zero, so that behavior is additionally covered by a synthetic opacity fixture. Converting to RGBA occurs only after indexed comparison, using the hash-checked original `PLATGAME.PIE` palette.

`BatimentGetEtat` calculates `floor(200 * valor_0a_u16 / 70)`. The renderer consumes its low u16 word as `estado`. Its temporary inclusive clip is:

```text
left   = max(0, x)
top    = max(0, i16(y + trunc_toward_zero((100 - estado) * 32 / 100)))
right  = window_width_cells * 32 - 1
bottom = window_height_cells * 32 - 1
```

The incoming clip is replaced, not intersected. `compor_portao` requires the destination dimensions to equal the planned window when a layer exists. No-layer plans return a copy without catalog access. Missing required arguments raise `TypeError`; invalid scalar widths/ranges or surface sizes raise `ValueError`; counters 32–255 raise `NotImplementedError` even if visibility would hide them. Original raw byte access into subsequent strips is evidence only.

The x86 comparison stops at `0x40F342`, before `AffVehiculeAtelier`, restoration of the saved clip, selection, and gauges; early rejection stops at `0x40F491`. These are deliberate checkpoints, not complete `AffBatiments` returns. The pure compositor has no global clip to restore and no callbacks. Whole-scene render order, the common tail, occupancy lookup, simulation updates, and world loading remain external dependencies.

Evidence: original `RISING.EXE` SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`; facade range `0x407FA7..0x4080E8` byte SHA-256 `f52190772fa3b3abf70197f451bab4fe9887b56edf436b2d1abc574ff0cce20d`; shared copy join `0x408412..0x408422`; raw-state query `0x41A8E5..0x41A940`; clip helpers `0x40F4B7..0x40F535`. [New byte provenance](../pesquisas-paralelas/graficos-animacao/evidencias/portoes-graficos.json) records exact bytes, interval hashes, the original type table and object constants, and unchanged predecessor hashes. `BUILDING.CMP` SHA-256 is `af4f94ea996a65d36592bb6cefc407dc628b3d488c9c335b8f6015bbfcb6a3ae`.

Fresh validation: **2,792 bounded original-x86 executions**, comprising 1,700 supported call/clip captures, 896 out-of-contract raw counter captures, two missing-occupancy captures, two original bank setup calls, and **192 exact indexed-buffer comparisons**. Completed run: zero skipped cases, expected exceptions, or instruction/time limits. Nine new Python regression tests replay the independent captures; the full graphics domain check passes **82 tests**. Earlier graphics x86 stages were not rerun. See the [saved report](../pesquisas-paralelas/graficos-animacao/validacao/x86-portoes-graficos.json), [64 frame associations](../pesquisas-paralelas/graficos-animacao/artefatos/associacoes-portoes.json), and [original-buffer contact sheet](../pesquisas-paralelas/graficos-animacao/artefatos/portoes-contato.png) (eight columns, zero orientation first, counters increasing across each row).

```sh
python3 -B pesquisas-paralelas/graficos-animacao/validar_portoes_graficos.py
python3 -B scripts/check.py --domain graphics
```

## Gate return and clip restoration — second continuation stage

`portoes_completos.py` adds `consultar_portao_completo` and `compor_portao_completo` on top of the unchanged facade API. It validates the original call through its **actual return at `0x3000000` in the harness**, rather than stopping at the shared-tail checkpoint. It uses the same prepared type-12/object-253 contract and all facade arguments, with two required additions:

- `terreno_u16`: the original cell's terrain word, 0–65535, excluding **`0x356`**. That tile can invoke `ChercheCaseBatiment` over other world records before the workshop type check; it remains unsupported by this independent renderer.
- `recorte_entrada`: four u16 values in left/top/right/bottom order. Inverted rectangles are permitted because the original saves and restores their words verbatim.

The pure compositor returns `(indexed_bytes, restored_clip_tuple)`. For an accepted facade the original order is save clip → set temporary clip → one indexed copy → workshop guard → restore clip → habitation query → conditional selection-frame/gauge guards → return. The workshop guard returns immediately for every terrain word in the supported domain. The selection-frame and gauge routines themselves return before drawing when the structure type is 12, including when selection/hover conditions invoke them. Empty and populated valid bags were exercised through the original habitation query; the renderer does not implement bag rules or require their result as an input because they cannot add pixels for this type. An early-hidden gate preserves the incoming clip without calling any of these helpers.

This stage has no delegated callbacks, no world mutation, no extra sprite, and no new player-color/shadow behavior. It returns the clip explicitly instead of writing a global. Invalid terrain/clip widths raise `ValueError`, tile `0x356` raises `NotImplementedError`, and the facade API retains its existing failures. Other structure types, invalid runtime bag records, workshop-trigger lookup, whole-scene order, and runtime mission integration remain outside the contract.

Original evidence: shared tail `0x40F342..0x40F49C`, SHA-256 `ce3dabcebaebfb6d4ba718445b5d854bcfd10b184bdf6c2883354c7b837e3264`; `AffVehiculeAtelier` guard `0x402864..0x40288B` and epilogue `0x402C7A..0x402C82`; type-12 guards in `BatimentPoseCadre` `0x4022C8..0x4022F9` and `AffJaugeBatiment` `0x4020EC..0x402122`. [Exact bytes and prior-stage hashes](../pesquisas-paralelas/graficos-animacao/evidencias/portoes-completos.json) retain the original executable identity above and include the read-only habitation dependency intervals.

Fresh validation: **882 bounded original-x86 executions / 1,077,090 instructions**, consisting of 768 full-return call/guard captures, 112 exact indexed buffers and two bank setup calls. Zero skips, expected exceptions or time/instruction limits; no guard, habitation or pixel routine is substituted in the pixel comparisons. Six new Python regressions pass; the graphics domain now contains **88 tests**. The original facade report and its 2,792-call result are unchanged historical records for the preceding stage. [Saved full-return report](../pesquisas-paralelas/graficos-animacao/validacao/x86-portoes-completos.json).

```sh
python3 -B pesquisas-paralelas/graficos-animacao/validar_portoes_completos.py
python3 -B scripts/check.py --domain graphics
```

## Unit selection and exact sorting — third continuation stage

`ordem_unidades.py:selecionar_ordem_unidades` reconstructs the read-only prefix of `AffSprite`, before projectile sorting or drawing. It requires exactly **220,800 runtime unit bytes** (800 records × 276), two separately selected camera byte maps of 65,536 bytes each, a required `origem` pair in 0–255, and `janela_celulas` width/height in 1–256. It reads only record state u8 `+0x02`, cell u16 `+0x08`, and priority u8 `+0xAB`. It does not infer unit type, owner, life, or economic state.

The original scans pool indices 0–799 and accepts a record exactly when its state byte is nonzero, its discovery map byte has `(flag & 31) == 0`, its separate illumination map has `(flag & 16) == 0`, and its cell coordinates satisfy:

```text
origin_x <= cell_x < origin_x + window_width_cells + 2
origin_y <= cell_y < origin_y + window_height_cells + 10
```

The result contains `selecionadas` in initial pool-index order and `ordenadas` in the exact original swap order. The primary key is the full cell word, then the priority byte. The original selection sort is **unstable for equal keys**: initial indices `[0,1,2]` with cells `[A,A,B]`, `B < A`, and equal priorities produce `[2,1,0]`. A stable sort would produce `[2,0,1]`. State 4 is included as a nonzero state; no independent death precedence was observed in this prefix.

No input buffer is mutated and there are no callbacks or rendering effects in this API. Incorrect buffer lengths or origin/window pairs raise `ValueError`; missing required keyword arguments raise `TypeError`. The sorted buffer is an intermediate caller input, not the final draw order: subsequent code divides units into two priority passes and interleaves other renderers/projectiles. The overlapping-unit demonstration separately invokes the original supported unit renderer using the captured order at a declared common projected position; it is not a full `AffSprite` scene.

Original evidence: `AffSprite 0x416864..0x416A6C`, byte SHA-256 `9c1d0287c39058b803a9f23c0080354ab769c5127132919bd03d1a82768bad0e`; original `ExisteEngin 0x441FFF..0x442025`, discovery `0x4766F0..0x47670A`, illumination `0x47693A..0x476951`. [Exact bytes and predecessor provenance](../pesquisas-paralelas/graficos-animacao/evidencias/ordem-unidades.json) use the same original executable identity recorded above.

Fresh validation: **2,354 bounded x86 segments / 15,600,001 observed instructions**, covering 327 selection/sort fixtures, all state and camera-flag byte values, index 799, window margins, deterministic mixed pools, the full 800-selected pool, and eight separately captured overlap buffers. The large sort preserves CPU/stack at outer-loop checkpoints to stay within each execution limit. There are zero skipped cases, expected exceptions or limit failures. Eight original indexed overlap buffers match; a hypothetical stable-sort composition differs by **44–127 pixels** per buffer. Forty original type initialization calls, forty original complete supported body draws, and two bank setup calls are included in this stage's segment count, not added as historical totals. Six new capture regressions pass; the full graphics domain passes **94 tests** without skips. [Saved ordering report](../pesquisas-paralelas/graficos-animacao/validacao/x86-ordem-unidades.json).

```sh
python3 -B pesquisas-paralelas/graficos-animacao/validar_ordem_unidades.py
python3 -B scripts/check.py --domain graphics
```

## Projectile display list and cell query — fourth continuation stage

`ordem_projeteis.py` reconstructs two read-only display inputs required by `AffSprite`. These functions consume the existing **100×56-byte projectile pool**; they do not advance, allocate, expire or damage anything.

- `consultar_celula_projetil(pool, indice_u16)` accepts indices 0–99 and reads unsigned pixel words `+0x0C/+0x0E`, regardless of the activity byte. It returns `x_celula=x//32`, `y_celula=y//32`, `chave_u32=y_celula*256+x_celula`, and `celula_u16=chave_u32 & 65535`. The full dword matters: raw maximum coordinates yield **526079**, while the scene commonly compares its low word. Origin/target fields `+0x14/+0x16` are not read.
- `selecionar_ordem_projeteis(pool, descoberta, iluminacao, indices_entrada, *, origem, janela_celulas)` requires two camera maps of 65,536 bytes, a **200-byte caller index array**, origin coordinates 0–255, and window dimensions 1–256 cells. It returns selected/ordered indices, count 0–100 and a new output index array whose unused tail remains identical to the caller input.

The sorter scans indices 0–99; nonzero u8 `+0x02` is active. It derives the pixel-coordinate cell, applies **mask 31 to both discovery and illumination** at the low-word key, and applies the same +2-column/+10-row window margins as the unit selector. Raw coordinate words can derive coordinates beyond 255; the query preserves that arithmetic rather than silently clamping to a physical map.

It selection-sorts the output by the **unsigned low 16-bit key**, choosing the **last equal candidate** at each swap. Four equal keys initially `[0,1,2,3]` produce `[3,0,1,2]`. This is a different tie rule from the unit sort. Only the first `count*2` output bytes are replaced; no pool, camera map, or input index bytes mutate. Invalid lengths, scalar indices, or origin/window ranges raise `ValueError`; missing required keywords raise `TypeError`. Negative camera origins and raw indices outside the 100-record pool are unsupported.

Evidence: original `ProjectileTrierAffichage 0x46FC8B..0x46FE9A` SHA-256 `3b26fd5f75330b32f114f8546c332e9fb13e3740af97519a8c6283cbf74e5dc5`; `ProjectileGetCase 0x46FE9A..0x46FEE5` SHA-256 `5cf91836f9b460da243a56f8f62400d840dff7b8a5014a223ceb13c89c97ccc1`; shared epilogue `0x46FC08..0x46FC0F`; terrain illumination `0x476951..0x476968`. Sort input `EAX` points to the output array, returns `EAX=count`; globals supply the pool at `0x5080F0`, selected camera at `0x508041`, origin words `0x508720/+2` and window words `0x508724/+2`. GetCase takes the record index in `AX` and returns the full key in `EAX`. [Exact original bytes](../pesquisas-paralelas/graficos-animacao/evidencias/ordem-projeteis.json).

Fresh validation: **1,310 bounded x86 segments / 1,736,567 instructions**: 581 full index-buffer fixtures, 98 cell queries (including pixel/u16 boundaries and indices 0/99), eight original type-1 projectile overlap captures, 32 complete original draw calls, and two bank setup calls. Sort capture deliberately pauses at `0x46FD9C` before sorting, preserves CPU/stack, then reaches the actual return; GetCase and demo draws also return normally. Zero skips, expected exceptions or limit failures. Seven new capture regressions pass. The eight indexed demos replay independently captured sprite IDs/positions in the reconstructed index order; **they do not establish a public `AffProjectile` sprite mapping**. [Saved display report](../pesquisas-paralelas/graficos-animacao/validacao/x86-ordem-projeteis.json).

```sh
python3 -B pesquisas-paralelas/graficos-animacao/validar_ordem_projeteis.py
python3 -B scripts/check.py --domain graphics
```

## Complete interior sprite-pass order — fifth continuation stage

`passe_sprites.py` adds `planejar_passe_sprites` and `executar_passe_sprites`. Planning consumes the complete 800×276 unit pool, 100×56 projectile pool, object-code map and the two selected-camera maps (65,536 bytes each). Origin is a pair 0–255 used for both native `AffSprite` arguments and projectile viewport globals. Window dimensions are restricted to **1–32 cells**, with `origin_x+width+8 <= 256` and `origin_y+height+10 <= 256`. Negative origins, margin wraparound and larger viewports are excluded from this stage.

Inputs form a stable frame snapshot: renderers must not change its activity, selection, cell, priority, object or visibility inputs during traversal. Planning runs the independently verified selectors first, then emits exact French renderer identifiers and argument values:

1. Traverse `(width+8) × (height+5)` cells row by row. If the object byte is nonzero and discovery mask 31 is clear, emit `AffVeget(x,y,cell)`. Always emit `AffBatiments(x,y,cell)` and `AffBatimentOmbre(x,y,cell)`, then zero-`+0xAB` units via `AffEngin(x,y,index)` at that cell.
2. Reset the unit cursor and traverse `(width+8) × (height+10)` cells. Emit `AffProjectile(index)` for every matching low-word projectile cell, then nonzero-`+0xAB` units via `AffEngin(x,y,index)`.

Relative projected cell origins are `x=32*column`, `y=32*row`. The first pass's smaller row extent is preserved: a selected zero-priority unit in the additional lower five rows is not forcibly flushed into a draw call. These relative coordinates do not establish `AffGame`'s full window/scrolling projection.

`executar_passe_sprites` requires four keyword callbacks: `vegetacao(x,y,cell)`, `construcao(x,y,cell)`, `unidade(x,y,index)`, and `projetil(index)`. Return values are ignored; the Python executor returns the number of callbacks invoked. `AffBatimentOmbre` is a literal original RET at `0x40F49B` and is retained in the plan for exact traces without invoking a callback. Missing required callbacks raise `TypeError`; non-callable callbacks raise `ValueError` before any effect. A callback exception propagates immediately, preserving earlier callback effects; there is no rollback. Actual renderer effects, including cosmetic RNG where applicable, remain those callbacks' responsibility.

Planning does not mutate input buffers or run renderer callbacks. Invalid lengths/origin/window values raise `ValueError`; a viewport whose margins cross the map boundary raises `NotImplementedError`. The event plan supports raw byte states and object codes as caller inputs; it does not claim that every emitted renderer handler is reconstructed.

Original evidence: complete `AffSprite 0x416864..0x416E41`, SHA-256 `e3a5445a1ef8b30dbdcb1b41612ff2ebfb612070d49f8673b252af7f1fd8bd51`, with shared return epilogue `0x410878..0x41087E`. [Exact caller bytes and committed-provider hashes](../pesquisas-paralelas/graficos-animacao/evidencias/passe-sprites.json).

Fresh validation: **105 bounded native calls / 3,578,331 instructions**, comprising 55 complete-caller trace fixtures, eight complete native sprite-pass pixel scenes, 40 original unit-type initializations and two bank setup calls. Every scene/trace reaches the actual return with a balanced stack; zero skipped cases, expected exceptions, limit failures or dependency checkpoints. Trace fixtures capture renderer callbacks; the eight indexed comparisons run the original tree, gate, unit and type-1 projectile handlers **without renderer stubs**. Reconstructed composition matches all eight exact indexed buffers. The supplied patterned background is synthetic and the terrain pass is not executed. Projectile layers in the demonstration are independently captured native commands, so public projectile sprite mapping remains a separate gap. Seven new saved-capture regressions pass. [Saved complete-pass report](../pesquisas-paralelas/graficos-animacao/validacao/x86-passe-sprites.json), [indexed scene preview](../pesquisas-paralelas/graficos-animacao/artefatos/cena-passe-sprites.png).

```sh
python3 -B pesquisas-paralelas/graficos-animacao/validar_passe_sprites.py
python3 -B scripts/check.py --domain graphics
```

## Lighting table and masked destination remap — sixth continuation stage

`eclairage.py` adds `tabela_eclairage(paleta, *, percentual, ciclos)` and `compor_eclairage`. The table constructor requires 768 RGB bytes, percentage u8 restricted to **1–255**, and up to 255 inclusive ordered u8 cycle ranges. For each palette component it calculates `q=floor(component*100/percentage)`, then uses target component **30 if q is zero**, otherwise `min(q,255)`. It selects the closest palette color by squared RGB distance, keeping the smaller eligible index on a tie. Palette index 0 is the initial candidate and remains eligible even when a cycle covers it; candidates 1–255 inside any cycle are excluded. There are no per-index exceptions inherited from `CalculOmbrage`.

The original writes its destination table sequentially at indices 0–255. The pure API returns 256 new bytes and preserves palette/cycle inputs. Invalid percentage/width/range inputs raise `ValueError`. Percentage zero is outside the public domain: original `IDIV` faults at `0x45FB46` before writing any output entry, independently captured as one expected exception. The API rejects it before effects.

`compor_eclairage(destino, largura, altura, quadro, x, y, tabela, recorte=None)` supports the original clipping-enabled `PasteEclairCmp` path, with i16 positions and an explicit 256-byte remap table. Only the CMP opacity mask matters: for each opaque source pixel, including literal palette zero, map the **existing destination index** through the table. Transparent skips leave the destination intact. Literal source colors are ignored. This is the same mask geometry as the verified shadow primitive with a distinct table, not RGB/alpha blending. Input buffers remain unchanged; new indexed bytes are returned. `CL=0`, full palette initialization/cycling and projectile simulation remain outside this contract.

Original evidence: `CalculEclairage 0x45FAFC..0x45FCA5`, SHA-256 `9a9709bd01200af21f1848f13901ab946e11b1449ddaaf052ceae98a90ddb156`; `PasteEclairCmp 0x45BA23..0x45BCB0`, SHA-256 `81371fcc66cb61a61031de5c4c841b844f124754909f7246ec51c3e867969407`; `MemEclairCopy 0x45F7D8..0x45F7F6`; original setup call `0x474F04..0x474F13` explicitly loads percentage 60. Table input is `EAX=palette pointer`, `DL=percentage`, with destination pointer `0x4E24B8` and cycle metadata `0x4E24E1/0x4E24E4`. [Exact bytes and predecessor hashes](../pesquisas-paralelas/graficos-animacao/evidencias/eclairage.json).

Fresh validation: **4,412 bounded segments / 35,074,931 instructions**, eight complete table fixtures (real palette, parameter boundaries, cycles, synthetic ties/all candidate exclusions), **297 exact indexed buffers** (all 256 destination indices, five real masks with clipping boundaries, one synthetic literal-zero fixture), two bank setup calls and **one expected zero-divisor exception**. Table generation uses original CPU/stack checkpoints before/after each sequential output write, then returns normally. Zero skipped cases, unexpected exceptions or execution-limit failures. Seven new capture regressions pass. [Saved original lighting report](../pesquisas-paralelas/graficos-animacao/validacao/x86-eclairage.json).

On resumption, the complete lighting validator was rerun against the intact original and reproduced the same observations/counts; only report elapsed seconds changed. The graphics domain passed **115 tests** with no skips. A [focused read-only REA review](../pesquisas-paralelas/graficos-animacao/evidencias/rea-eclairage-review.json), pinned to source revision `b9a8f8e9f25feb9cc97bf4960748f2bdf8c898bc`, corroborates the arithmetic using normalized analysis PE SHA-256 `26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0`. Its Watcom signature/register artifacts are documented; original SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb` remains the execution oracle. These are repeat runs of one fixture set, not additive coverage.

```sh
python3 -B pesquisas-paralelas/graficos-animacao/validar_eclairage.py
python3 -B scripts/check.py --domain graphics
```

## Remaining component inventory — continuation after the gate facade

This inventory distinguishes reconstructed behavior, captured original behavior, and runtime integration. The integrated gate facade at `ff4bc269c6d8534f4683bd0429072286ea8eaaf1` has exact indexed comparisons; it is not yet exercised by the macOS consumer or a complete loaded mission.

| Component | Evidence and current boundary | Next dependency |
|---|---|---|
| Gate shared tail | The full-return API now reconstructs `AffBatiments 0x40F342..0x40F49C` for terrain other than `0x356`; 882 fresh x86 calls validate return/clip/guards | Close the workshop-trigger lookup with a committed world-provider contract; integrate the consumer |
| Other building facades and overlays | `AffBatiments 0x407DD3..0x40F49C`; only the Sanctuary subset and gate facade are reconstructed | Recover per-type/mode layers, clipping and anchors against original buffers |
| Unit action handlers | Prepared type-0/type-2 attacks, six-type corpse copy/fade, type-6/type-7 construction and type-5/type-6/type-7 work display are reconstructed | Extend other types/effects and coordinate simulation task/phase/corpse-counter producers |
| Type-2 normal body | Separate raw-record mapper/compositor reconstructs branch `0x412ECE`, raw frame stride and exact anchor; full native calls and indexed buffers match | Consume the committed provider in the app; recover other players/effects/actions independently |
| Projectile display inputs/rendering | The 100-record selection/sort, cell queries and public `AffProjectile` mapper/compositor are reconstructed; eight bounded complete sprite scenes use the public renderer | Integrate the consumer and physical producers; preserve explicit catalog limits and raw phase semantics |
| Projectile/effect lighting | `CalculEclairage`, clipping-enabled mask remap and public projectile consumers are independently validated | Recover remaining palette effects and their lifecycle separately |
| Scene traversal/projection | Complete interior `AffSprite` planning/execution and relative projection are reconstructed; native complete-pass traces and bounded indexed scenes match | Recover margin wraparound/negative origins, `AffGame` projection/cadence and a real-mission consumer |
| Terrain pass/cache | Bounded nonwrapping `AffTerrain` traversal, opaque blocks, terrain objects, the `GetNumBob` cache and its verified CacheAlloc/InitCache/CacheFree lifecycle over real bank payloads match full native buffers | Recover negative/wrapped viewports |
| Frame orchestration | `AffGame` mode 0x12 through the HUD checkpoint `0x417B1C`: CalculFrame, draw gate, surface lock, terrain and sprite passes with committed renderers, every write returned; whole-frame native equality and named stops over the MONDE01 checkpoint | Building facades (MONDE01's type-2 trigger `0x2ED` first), unit overlays/types 1 and 8, HUD tail, palette cycling, 640×480 mode |
| Visibility, palette and clocks | Indexed composition/shadow helpers and clock prefix are reconstructed; visibility bytes are explicit runtime inputs | Connect validated world providers and original frame cadence |
| Real-mission consumer | V6 reads all serialized mission-1 object codes; the preview uses older pinned snapshots | Coordinate complete world loading/remapping, dynamic render state, input, effects and original-reference runtime scenes |

The gate-tail stage proves the explicit type-12 returns in `BatimentPoseCadre 0x4022C8` and `AffJaugeBatiment 0x4020EC`, plus the supported terrain guard in `AffVehiculeAtelier 0x402864`. This does not establish that the shared tail is visually inert for other buildings.

Original direct-call sites are `0x416B8A -> AffVeget`, `0x416BBD -> AffBatiments`, and `0x416C5D/0x416E2F -> AffEngin`. Recovering the prefix does not by itself reconstruct those passes or projectile integration.

The projectile-display slice is read-only with respect to combat state. Both visibility predicates use mask 31; the query uses pixel-coordinate-derived keys and the swap sort chooses the last equal candidate. These independently validated differences must remain distinct from the unit selector and physical projectile targeting.

The complete interior scene stage closes the two caller passes and projectile/unit interleaving. It preserves the asymmetric margins and relative projection while keeping callbacks and their supported sprite domains explicit. The terrain pass, global frame caller, boundary viewports and full mission/runtime operation remain independent missing components.

Lighting remap is available as an explicit independently validated provider consumed by the seventh-stage public projectile renderer. Its original setup literal 60 does not establish whole initialization or temporal palette behavior. Physical advancement stays combat-owned.

Selected next after stage-six integration: reconstruct the read-only `AffProjectile 0x46FF70..0x4704D9` dispatcher and the original 34-entry table at `0x46FEE8..0x46FF70`. Inputs are one 56-byte runtime record, explicit viewport-origin words and the caller-selected illumination byte at the derived pixel cell. The original dispatches copy, shadow, or lighting-mask layers; types 28/33 have no visible handler. Preserve u8 phase/direction, u32 presentation displacement, signed-i16 draw coordinates, layer order and catalog boundaries. Replace the prior captured-only projectile layers with the new public mapper only after original captures and complete indexed comparisons agree. No simulation update, target inference or phase advancement is included.

## Public projectile renderer — seventh continuation stage

`projeteis_graficos.py:consultar_projetil_grafico` consumes one prepared 56-byte runtime record, required `origem` containing two raw u16 viewport words, and required `iluminacao_u8`. The record fields read are type u8 `+0`, activity u8 `+2`, pixel x/y u16 `+0x0C/+0x0E`, phase u8 `+0x18`, direction u8 `+0x22` and presentation displacement u32 `+0x24`. The selected-camera illumination byte comes from the low word of `(pixel_y//32)*256+pixel_x//32`. `AffProjectile` itself does not query discovery; the display selector does so separately. Activity zero, illumination mask 31 nonzero, types 0/28/33 and types above 34 produce no layers or asset lookup.

The result exposes exact ordered `camadas` with engine/file/local IDs, signed-i16 x/y and operation `copiar`, `sombra` or `eclairage`. Origin words are multiplied by 32 and subtracted from unsigned pixel words before each final i16 coordinate wrap. All phase/direction bytes are consumed raw; they do not establish legal simulation phases, animation cadence or natural asset sequences. Types 9–13 ignore phase and draw shadow before the displaced copy. Types 24/25 use signed division of `(direction-1)/2`, truncated toward zero (including direction zero). Type 27 uses `(direction-1)*8`. Types 29/30 issue three lighting layers in increasing ID steps of 32; types 31/32 issue two shadow/lighting layers in original order. The remaining visible branches issue one copy, with vertical displacement applied only where the original reads it.

`compor_projetil` returns `(new_indexed_bytes, plan)` and requires explicit 256-byte `tabela_sombra` and `tabela_eclairage`, even on a no-draw path. It fetches and composes each layer in plan order with the existing indexed blitters and inclusive clip. Input record, surface and tables remain unchanged; no simulation callback, RNG, clock or physical effect occurs. Invalid scalar widths/buffer sizes raise `ValueError`; missing required keywords raise `TypeError`. Raw states selecting an engine ID outside the verified 12,156-entry catalog raise `NotImplementedError` before composition. Raw spills that remain within the catalog are reproduced without assigning gameplay meaning.

Evidence: the unchanged original executable SHA-256 above; `AffProjectile 0x46FF70..0x4704D9` hash `0fe33194fc2edde7f73e94a1d103b9a017f0213ed84dd2d3cf770bd2a32b3cf7`, jump table `0x46FEE8..0x46FF70` hash `24baa7752b2cac6f99cf92b36b4e5dabe38c72d5e7e001a1ab3025c48ad7de87`, shared epilogue `0x46FC08..0x46FC0F` and selected-camera query `0x476951..0x476968`. Native input is the pool index in low EAX, pool pointer `0x5080F0`, origin words `0x508720/+2` and camera byte `0x508041`; every renderer call uses CL=1. [Exact bytes and predecessor hashes](../pesquisas-paralelas/graficos-animacao/evidencias/projeteis-graficos.json) retain the source identities.

Fresh `validar_projeteis_graficos.py`: **12,148 bounded native calls / 7,447,454 instructions** = 11,728 complete dispatch captures, 410 exact indexed buffers, eight complete sprite-pass scenes and two bank setup calls. All calls return to `0x3000000` with stack `0x2008004`; pool and selected illumination byte are preserved. Zero skips, expected exceptions or limits. The capture matrix covers every type/phase byte, every direction byte for directional types, activity/illumination bytes and displacement/coordinate boundaries. It contains **172 explicitly unsupported raw out-of-catalog captures**: their blitters are intercepted, so those calls establish selected commands rather than valid native asset dereferences. Pixel and scene comparisons execute the original rendering instructions without renderer substitutions; bank setup substitutes only file IO/allocation.

The eight scenes combine trees, a supported gate, five supported unit bodies and projectile pairs through the public mapper, replacing the previous captured-projectile-command replay. Their background is synthetic; `AffTerrain`, `AffGame` and real-mission operation are not tested. The shadow table is a declared input from the unchanged historical composition report; the lighting table is the stage-six native percentage-60 table. [Saved native report](../pesquisas-paralelas/graficos-animacao/validacao/x86-projeteis-graficos.json), [32-type contact sheet](../pesquisas-paralelas/graficos-animacao/artefatos/projeteis-contato.png) (eight columns, visible types in increasing order; phase 0/direction 1).

The [focused REA review](../pesquisas-paralelas/graficos-animacao/evidencias/rea-projeteis-review.json) retains pinned REA source `b9a8f8e9f25feb9cc97bf4960748f2bdf8c898bc` and normalized analysis PE SHA-256 `26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0`, separately from the intact execution original. At `0x46FFE7`, exact bytes `e91cfcffff` decode as JMP to `0x46FC08` although existing Ghidra flow metadata classifies it as a call. That annotation and the absence of modeled parameters do not override the original opcode, recovered register input or native return observation. The private read-only session exported and closed; no database/cache is published.

Seven new saved-capture regressions pass; `python3 -B scripts/check.py --domain graphics` passes **122 tests**, with zero skips. This closes the public projectile render dependency for the declared raw-record/catalog domain. Physical phase producers, temporal animation, wider unit/building handlers, terrain/global-frame rendering and real-mission runtime integration remain open.

```sh
python3 -B pesquisas-paralelas/graficos-animacao/validar_projeteis_graficos.py
python3 -B scripts/check.py --domain graphics
```

## Type-2 normal body — eighth continuation stage

The app's type-2 body gap is reconstructed in a separate `unidade_tipo2.py`, preserving the existing five-type modules and their frozen provenance. Its historical stage-eight signature was `consultar_corpo_tipo2(registro276, *, x, y)`; **the required selection inputs added in stage nine below supersede that signature**. It requires one 276-byte prepared runtime record and signed-i16 projected cell origins. Supported inputs: owner byte `+0=0`, type `+1=2`, state `+2` in 2/7, oscillation `+0x99=0`, effects byte `+0xDC=0`, auxiliary indicator `+0xBA=0` and unsigned word `+0x74>=100`. These are explicit conditions, not defaults inferred from a loaded mission. The bag word at `+0x0A` does not affect this branch.

It reads signed-i8 displacement `+0x86/+0x87`, raw direction u8 `+0x91`, phase u8 `+0xA4` and count u8 `+0xA5`. Body ID is low-u16 `3202 + (floor((direction+1)/2)-1)*count + phase`; direction zero therefore uses group -1, rather than being silently clamped. Native type initialization sets count=8 and oscillation=0, but this renderer consumes every count/phase byte raw. It does not reset state-7 phase to the separate stop-phase value, infer animation cadence or advance simulation.

Exact order is shadow ID10784 at `(x+dx+2,y+dy+26)`, then body at `(x+dx-32,y+dy-16)`, with every final coordinate wrapped to signed i16. The plan contains engine/file/local IDs and operations. `compor_corpo_tipo2(catalogo,destino,largura,altura,registro276,*,x,y,tabela_sombra,recorte=None)` requires an explicit 256-byte shadow table and returns `(new_indexed_bytes,plan)` through the existing indexed blitters/inclusive clip. Record, surface and table remain unchanged; no callbacks or world mutations occur. Invalid widths/lengths raise `ValueError`, missing keywords `TypeError`, unsupported guards/types/states and out-of-catalog raw IDs `NotImplementedError` before composition. Other owners, oscillation, effects, indicators and action handlers remain unsupported by this API.

Original evidence: unchanged executable SHA-256 above; type-2 branch `0x412ECE..0x412F1C` hash `2861dce18904b697f56ffba18973c8f0707d9dd8f8b9ea5b51140e764afb6c57`, anchor `0x410F6C -> 0x410FF8..0x411001` hash `6463df6bf40d3200669072267440eb994d87cc54b1086ec86a052805abf44670`, body table slot `0x412330`, join `0x412CB8`, type initialization `0x4576CA..0x457727`, caller `AffEngin 0x41591F..0x415A57`. Native input is signed-i16 x/y in EAX/EDX and pool index in low EBX; unit pool pointer is `0x4E19A0`. Type table `0x496612` identifies French `CAPITAINE`; no new translated player label is introduced. [Exact-byte evidence](../pesquisas-paralelas/graficos-animacao/evidencias/unidade-tipo2.json).

Fresh validator: **12,851 bounded original-x86 calls / 8,553,649 instructions** = 12,564 layer captures, 21 unsigned guard/bag captures, **263 exact indexed buffers**, one original type initialization and two bank setup calls. Both states exercise all 256 phase bytes at directions1–16/count8; additional matrices cover all count/direction bytes, pool slots0/799, signed displacements and coordinate boundaries. Every caller reaches `0x3000000`, ESP `0x2008004`, with the entire 220,800-byte pool unchanged. Zero skips, expected faults or limits. **555 raw out-of-catalog captures** are explicitly unsupported; intercepted capture blitters prove selected commands, not valid native asset dereferences. Pixel calls execute the full original renderer without substitutions. Only bank setup file IO/allocation is substituted. The supplied background/table are explicit fixtures; no scene caller, loaded mission or natural animation is established. [Native report](../pesquisas-paralelas/graficos-animacao/validacao/x86-unidade-tipo2.json), [contact sheet](../pesquisas-paralelas/graficos-animacao/artefatos/unidade-tipo2-contato.png) (eight odd directions, phase0 above phase7).

The [focused REA review](../pesquisas-paralelas/graficos-animacao/evidencias/rea-unidade-tipo2-review.json) retains the raw-count MOV at `0x412F06`, pinned source revision and separate original/normalized PE hashes. Exact instruction bytes corroborate the runtime stride; Listing operand tokens do not establish effective-address roles or a Watcom signature. The private read-only session exported and closed. Seven new saved-capture regressions pass; the graphics domain passes **129 tests**, zero skips and valid documentation links.

```sh
python3 -B pesquisas-paralelas/graficos-animacao/validar_unidade_tipo2.py
python3 -B scripts/check.py --domain graphics
```

## Explicit type-2 selection guards — ninth continuation stage

Caller review found an omitted boundary in the stage-eight raw-record wrapper: `AffDeplaceEngin` can draw a selection marker before the body and invoke `AffInfoSelection` after it, using record `+0xBD` and globals outside that record. The old native fixtures used original image defaults camera0, selected indexFFFF, mode0, and +BD0. Their results remain valid for that narrow environment; the wrapper needed explicit inputs to avoid accepting an unimplemented overlay path.

Both `consultar_corpo_tipo2` and `compor_corpo_tipo2` now require four additional keywords: `indice_u16` in0–799, `camera_u8` in0–255, `indice_selecionado_u16` in0–65535, and `modo_selecao_u8` in0–255. They are the actual pool index, current camera, original selected-index word and selection-mode byte. No mission defaults are supplied. The API rejects `NotImplementedError` before composition if `(record[0xBD]!=0 and camera==owner)` or selected index equals pool index or mode is nonzero. A nonzero +BD can still use the normal-body API under another camera when the other two overlay triggers are absent. The existing body/effect guards, ordered layers, fixed-width arithmetic and input preservation remain as above. Other five-type APIs keep their existing contracts.

Original selection-prefix range `0x4124A9..0x4124C4`, tail `0x412A53..0x412A9F`; globals camera `0x508041`, selected-index word `0x496AC2` and mode byte `0x508F8F`. [New exact-byte evidence](../pesquisas-paralelas/graficos-animacao/evidencias/selecao-tipo2.json) pins unchanged stage-eight report/evidence hashes and original executable identity. The original-byte review is sufficient for these simple guards; REA was not needed for a new semantic inference.

Fresh validator: **5,155 bounded original calls / 2,360,401 instructions**, comprising 5,136 selection captures, 16 exact indexed buffers, one type initialization and two bank calls. Captures contain **3,596 full returns**, **514 declared stops at `0x4124C4` before selection-marker work**, and **1,026 declared stops at `AffInfoSelection 0x410BE4`** after the normal body. The stops are explicit unimplemented dependencies, not full original returns. Every supported capture/pixel call returns normally with ESP`0x2008004`; pools and selection globals are preserved. Zero unexpected exceptions, limits or skips. Capture blitters are intercepted; pixel calls execute original rendering without substitutions. All mode/camera/selection-flag bytes, pool slots0/1/799 and selected-word boundaries are covered. [Saved report](../pesquisas-paralelas/graficos-animacao/validacao/x86-selecao-tipo2.json).

Five new capture regressions and all preceding graphics checks pass (**134 tests**, zero skips). Stage-eight capture files are not regenerated; maintained replay/validator call sites now pass their historical explicit selection values. This fixes the wrapper boundary; selection markers/gauges, broader action rendering and real-mission operation remain unsupported.

```sh
python3 -B pesquisas-paralelas/graficos-animacao/validar_selecao_tipo2.py
python3 -B scripts/check.py --domain graphics
```

## Prepared attack bodies — tenth continuation stage

`ataque_grafico.py:consultar_ataque_grafico(registro276, *, x, y, indice_u16, camera_u8, indice_selecionado_u16, modo_selecao_u8)` implements the type-0/type-2 attack-display paths. x/y are projected signed-i16 cell origins; indices/camera/mode have the exact widths and domains of the type-2 selection contract above. Supported record: owner0, type0/2, state1/24 with `1<=+0x8A<=3`, or state22 with `+0x8A=1`; effects byte `+0xDC=0`, auxiliary `+0xBA=0`, unsigned `+0x74>=100`. It rejects the same selection-overlay triggers before composition. Normal-body routes, no-draw routes and other actions remain outside this attack API; the pure function raises `NotImplementedError` for them. Display selection/visibility belongs to the existing scene selector, not this body mapper.

The body ID is low-u16 `base + (floor((direction+1)/2)-1)*attack_count + phase`, using raw direction u8 `+0x91`, phase u8 `+0xA4` and **attack count u8 `+0xA6`**, independently of normal count `+0xA5`. Type0 base2146/anchor40,22; type2 base3266/anchor32,16. Native initialization writes attack count10 for both tested types, but every raw count/phase byte is consumed as supplied. Direction zero preserves group -1. Signed-i8 displacement `+0x86/+0x87` shifts both layers. Shadow10784 at `(x+dx+2,y+dy+26)` precedes the body at the type anchor; final positions wrap i16. Catalog-overflow IDs raise `NotImplementedError` before composition.

`compor_ataque_grafico` takes the same record/keywords plus catalog, indexed destination/dimensions, explicit 256-byte `tabela_sombra` and optional inclusive `recorte`; returns `(new_bytes,plan)`. Inputs remain unchanged, no callbacks or world updates occur. Invalid widths/ranges/lengths raise `ValueError`; missing required inputs `TypeError`. There is no phase advancement, projectile emission, damage, RNG or timing behavior. Combat's producer of `+0x8A=2/3` remains unproven; these accepted prepared display bytes do not establish a simulation transition or a legal animation lifecycle.

Evidence uses the unchanged original executable identity: type0 branch `0x413A04..0x413A58` hash `d35e6a88aeb0d5632eebf29764c92d07aaea57a9e49773f63944bc9d0998d782`; type2 `0x413BC7..0x413C14` hash `cf56e6f0b2a1a728d3bf4c5bf73961b0cbb98b6bf105c90042c5c6d9703761c3`; dispatch table `0x4136E4`, join `0x413971`, prefix `0x41374C`, tail `0x414320..0x414495`, full `AffEngin` caller `0x41591F..0x415A57`. Native input x/y in EAX/EDX, pool index low EBX, unit pointer `0x4E19A0`; selection globals as above. [Exact-byte evidence and unchanged predecessor hashes](../pesquisas-paralelas/graficos-animacao/evidencias/ataque-grafico.json).

Fresh validator: **18,938 bounded native calls / 20,771,171 instructions**, 17,960 route/layer captures, **974 exact indexed buffers**, two original type initializations and two bank calls. Capture outcomes are separate: **15,341 supported full returns**, **6 normal-handler entry checkpoints**, **2 selection-prefix checkpoints**, **6 selection-info checkpoints**, **1,516 native no-draw route returns outside the public attack scope**, and **1,089 raw out-of-catalog command captures**. These outcomes sum to the capture matrix; the checkpoints are declared dependencies, not complete returns. Every full call has balanced ESP`0x2008004`, with the 220,800-byte pool and selection globals unchanged. No unexpected faults, skips or limits. Capture blitters are intercepted; pixel calls execute the original rendering instructions without substitutions. Out-of-catalog captures prove command selection only. Bank setup substitutes file IO/allocation. [Native report](../pesquisas-paralelas/graficos-animacao/validacao/x86-ataque-grafico.json), [type0/type2 eight-direction contact sheet](../pesquisas-paralelas/graficos-animacao/artefatos/ataque-tipos0-2.png).

Matrix coverage includes every phase byte at directions1–16, every attack-count/direction byte in additional raw fixtures, every +8A byte for each supported state, pool0/799 and signed coordinate/shift/clipping boundaries. Pixel fixtures cover all ten initialized attack phases for both types, all directions and all three supported states, plus clipping edges. A [focused read-only REA review](../pesquisas-paralelas/graficos-animacao/evidencias/rea-ataque-grafico-review.json) corroborates the `MOV DL,[ESI+0xA6]` at`0x413BFF`, preserving pinned source and distinct analysis/original hashes; operand/signature limitations remain explicit. Session exported/closed. Seven new regressions pass; the graphics domain passes **141 tests**, zero skips and valid links. Background/table are explicit fixtures; this is not a full scene, mission or natural attack/emission run.

```sh
python3 -B pesquisas-paralelas/graficos-animacao/validar_ataque_grafico.py
python3 -B scripts/check.py --domain graphics
```

## Prepared corpse display — eleventh continuation stage

`morte_grafica.py:consultar_morte_grafica(registro276, *, x, y)` takes one prepared record, projected signed-i16 x/y, owner0, state4, effects byte `+0xDC=0` and type0/2/5/6/7/9. It reads raw direction u8`+0x91`, phase u8`+0xA4`, corpse stride u8`+0xDB`, counter u16`+0xC2` and signed-i8 shifts`+0x86/+0x87`. It does not advance the counter/phase or remove the record. Unlike normal/attack handlers, the original death handler does not read selection globals, +BD/+BA, fatigue word+74, bag word+0A or walking/attack stride+A5/+A6. Twelve additional native cases explicitly exercise those differing conditions; no selection-default inputs are invented for this API.

Death base/anchor pairs are type0:2226/(40,22), type2:3346/(32,16), type5:1762/(11,11), type6:3106/(16,20), type7:1538/(26,26), type9:1890/(19,14). Engine ID is low-u16`base+(floor((direction+1)/2)-1)*corpse_stride+phase`; direction0 keeps group-1. Every layer shares that ID and the signed-i16 wrapped position `(x+dx-anchor_x,y+dy-anchor_y)`. There is **no walking footprint shadow10784**. The source corpse's opacity mask controls each repeated destination shadow remap.

| Counter+0xC2 | Ordered operations |
|---|---|
| 0–304 | One body copy |
| 305–309 | Copy, then one shadow |
| 310–314 | Copy, then two shadows |
| 315 | Copy, then three shadows |
| 316–319 | Three shadows, no copy |
| 320–324 | Two shadows |
| 325–329 | One shadow |
| 330–65535 | No layers or asset lookup |

`compor_morte_grafica(catalog,dest,w,h,record276,*,x,y,tabela_sombra,recorte=None)` requires an explicit256-byte shadow table and returns `(new_indexed_bytes,plan)` with inclusive clipping and unchanged inputs. Repeated shadows operate on the evolving destination in order. Out-of-catalog IDs raise `NotImplementedError` only when layers are required; a finished counter returns no layers even if other raw bytes would select an invalid ID. Unsupported owner/type/state/effects raise `NotImplementedError`; invalid widths/lengths raise `ValueError`, absent keywords `TypeError`. No callbacks/RNG/clock/world changes occur. Visibility selection remains the caller's responsibility.

Evidence: unchanged original executable SHA-256; `EnginGetSpriteMort 0x415496..0x41559A` hash `11d597526321a257beb04660b948a08b889fb2c8e5721fcdc33ed7269e6eac96`; complete `AffDyingEngin 0x41559A..0x41591F` hash `e0862d1dd4d638bfe1e834e28e0f6cfa1e608202da6ebf9fa7d3afc1f62208fe`; full `AffEngin` caller preserved. Native x/y in EAX/EDX, pool index lowEBX, pool pointer`0x4E19A0`. [Exact-byte evidence and unchanged predecessors](../pesquisas-paralelas/graficos-animacao/evidencias/morte-grafica.json). Core's [physical dying contract](core/PHYSICAL_DYING.md) separately sets state4/A4=0/C2=0 in its declared domain and leaves DB unchanged; it does not establish corpse progression or visible-mission execution.

Fresh validator: **18,732 bounded original calls / 29,307,746 instructions**, 17,502 complete command captures, 12 ignored-field captures, **1,210 exact indexed buffers**, six type initializations and two bank calls. Every caller reaches`0x3000000`, ESP`0x2008004`, with the full220,800-byte pool unchanged. Zero dependency checkpoints, expected/unexpected exceptions, limits or skips. There are **1,068 raw out-of-catalog command captures**: blitters are intercepted for those, so native asset dereference is not claimed; public API rejects them. Pixel calls execute original rendering without substitutions, with bank IO/allocation substituted only during setup. [Native report](../pesquisas-paralelas/graficos-animacao/validacao/x86-morte-grafica.json), [six-type counter contact sheet](../pesquisas-paralelas/graficos-animacao/artefatos/morte-contadores.png) (rows0/2/5/6/7/9, columns counters0/304/305/314/315/316/325/330).

Matrix covers counters0–340 and large-u16 boundaries, all phase/direction/stride bytes in focused raw cases, pool0/799 and signed positions/shifts. Indexed comparisons cover every initialized corpse phase at eight directions plus fade/copy/clipping boundaries. Original initialized stride is8 for five types and10 for type2; this is a field observation, not a proven animation lifecycle. [Focused REA review](../pesquisas-paralelas/graficos-animacao/evidencias/rea-morte-grafica-review.json) corroborates the u16 load at`0x415639`, retains pinned source/distinct PE identities and notes the corrected preliminary interior-byte query. Private session exported/closed. Seven new capture regressions pass; graphics domain **148 tests**, zero skips and valid links. Synthetic background/table fixtures do not establish a scene or mission; corpse timing, removal, other types/owners/effects and consumer activation remain open.

```sh
python3 -B pesquisas-paralelas/graficos-animacao/validar_morte_grafica.py
python3 -B scripts/check.py --domain graphics
```

## Prepared construction display — twelfth continuation stage

`construcao_grafica.py:consultar_construcao_grafica(record276, *, x, y, indice_u16, indice_selecionado_u16, modo_selecao_u8)` consumes one prepared runtime record, projected signed-i16 cell origins, actual pool index 0–799, raw selected index u16 and raw selection-mode u8. Supported record: owner 0, type 6/7, state 11/15, +BD/+DC/+BA zero, unsigned fatigue word +74 at least 100. Nonzero +BD invokes the original construction selection prefix **regardless of camera**; the API rejects it before composition. It also rejects selected-index equality or nonzero selection mode. With +BD zero, camera cannot change the supported branch, so no camera default/input is needed; all camera bytes were independently captured.

The renderer reads raw task byte +89, phase +A4, direction +91, Bag count word +0A and signed-i8 shifts +86/+87. Task 0 chooses by count zero versus nonzero; task 1 ignores the Bag; tasks 2–255 produce no body layers under the required guards. This describes display branching, not task production or transport semantics. The branch uses fixed strides, independently of +A5/+A6/+A8:

| Type | Task +89 | Bag word | Branch constant | Fixed stride |
|---|---|---|---:|---:|
| 6 | 0 | 0 | 2970 | 8 |
| 6 | 0 | nonzero | 3034 | 8 |
| 6 | 1 | ignored | 3166 | 4 |
| 7 | 0 | 0 | 1338 | 8 |
| 7 | 0 | nonzero | 1466 | 8 |
| 7 | 1 | ignored | 1402 | 8 |

Engine ID = low-u16 `constant + floor((direction+1)/2)*stride + phase`. Direction 0 and all phase bytes retain their raw behavior; they can cross semantic sprite ranges without establishing a legal animation sequence. Shadow 10784 at `(x+dx+2,y+dy+26)` precedes the body at `(x+dx-16,y+dy-20)` for type 6 or `(x+dx-26,y+dy-26)` for type 7, with final signed-i16 wrap. Tasks above 1 do not fetch assets. `compor_construcao_grafica` takes catalog/destination/dimensions, the same required inputs, explicit 256-byte `tabela_sombra` and optional inclusive `recorte`; returns `(new_indexed_bytes,plan)`. All inputs stay intact; no callback, RNG/clock, task, building-progress or economic effect occurs. Invalid widths/lengths raise `ValueError`, missing keywords `TypeError`, unsupported guards/types/states `NotImplementedError` before composition.

Evidence: unchanged original executable identity; complete `AffConstruireBatiment 0x414495..0x414A8A` hash `22d386a7b6ac4af35f190e4293d06a64dd489c4746f0db31c2cd618e8d8d3c9a`, `BagVide 0x4470B9..0x4470C5` hash `a4b23a2dfd610b631864b3ffd40674fc62f9bc18fec11a6d3b824a770aa937af`, full `AffEngin` caller. Native x/y enter EAX/EDX, actual index low EBX; unit pointer `0x4E19A0`, selected-index/mode at `0x496AC2/0x508F8F`. [Exact-byte evidence and unchanged predecessors](../pesquisas-paralelas/graficos-animacao/evidencias/construcao-grafica.json). Direct original-byte review and independent native execution establish this small branch mapping; no new REA interpretation is needed.

Fresh validator: **32,338 bounded original calls / 33,469,945 instructions**, 30,780 route/layer captures, **1,554 exact indexed buffers**, two type initializations and two bank calls. Capture outcomes: **29,246 complete returns** (including 1,016 empty-body returns), **1,020 declared selection-prefix stops at `0x41451D`**, **514 declared selection-info stops at `0x410BE4`**. Stops are unimplemented overlay boundaries, not complete returns. Every complete call has ESP `0x2008004`; full pool and selection globals remain unchanged. Zero expected/unexpected exceptions, limits or skips. Capture blitters are intercepted; pixel renderers and Bag query execute unchanged. Bank setup substitutes file IO/allocation. [Native report](../pesquisas-paralelas/graficos-animacao/validacao/x86-construcao-grafica.json), [six-variant direction sheet](../pesquisas-paralelas/graficos-animacao/artefatos/construcao-tipos6-7.png) (type 6 then 7, empty/filled task-0 then task-1 rows, eight odd directions, phase 0).

Matrix covers all task/phase/direction/camera/mode/+BD bytes in focused combinations, Bag-word boundaries, pool 0/799, shifts and signed coordinate edges. Pixels cover both states, all 16 directions, phases 0–7 and each body variant plus no-body/clipping cases. These phases are raw fixtures, not a recovered task cadence. Seven new regressions pass; graphics domain **155 tests**, no skips and valid links. Background/table remain synthetic inputs; other types/owners/effects, selection rendering, work/task producers and real-mission operation are separate gaps.

```sh
python3 -B pesquisas-paralelas/graficos-animacao/validar_construcao_grafica.py
python3 -B scripts/check.py --domain graphics
```

## Prepared worker work display — thirteenth continuation stage

`trabalho_grafico.py:consultar_trabalho_grafico(record276, *, x, y, indice_u16, camera_u8, indice_selecionado_u16, modo_selecao_u8)` consumes projected signed-i16 origins, actual pool index 0–799, raw camera/mode u8 and selected-index u16. Supported record: owner 0, state 5, type 5/6/7, effects byte +DC zero. The selected-target prefix is unsupported when +BD is nonzero and camera matches owner. The API reads raw task +89, phase +A4, direction +91, Bag count word +0A and i8 shifts +86/+87. It does not produce or advance those values.

| Type | Task +89 | Body choice | Branch constant / fixed stride |
|---|---|---|---|
| 5 | 0, 2, 3 | Bag count zero / nonzero | 1594 / 8 or 1690 / 8 |
| 5 | 1 | Bag ignored | 1662 / 4 |
| 6 | 0, 1 | Bag count zero / nonzero | 2970 / 8 or 3034 / 8 |
| 6 | 2 | Bag ignored | 3034 / 8 |
| 7 | 0, 3, 4, 5 | Bag count zero / nonzero | 1338 / 8 or 1466 / 8 |
| 7 | 12 | Bag ignored | 1402 / 8 |
| All three | Other task values | No body | No asset lookup |

Engine ID = low-u16 `constant + floor((direction+1)/2)*stride + phase`, independently of +A5/+A6/+A8. Raw phase/direction spill is reproduced without a natural animation claim. Shadow 10784 at `(x+dx+2,y+dy+26)` precedes body at the existing type anchor (5:11,11; 6:16,20; 7:26,26), final positions wrapped i16. Mechanic task 2 deliberately differs from its construction action sprite.

Two kinds of no-body return must remain distinct. Type 6 task 3 and type 7 tasks 1/2 clear an original local flag and **skip all later selection/fatigue/experience overlays**. Once the initial selected-target guard is absent, those tasks accept selected-index equality, nonzero selection mode, any fatigue word and any +BA byte. Other no-body/body tasks still require selected index different from pool index, selection mode 0, unsigned +74 at least 100 and +BA zero; otherwise the API raises `NotImplementedError` before composition. These narrower supported guards do not claim every rejected original input necessarily paints an indicator.

`compor_trabalho_grafico` takes catalog, indexed destination/dimensions, the same required inputs, explicit 256-byte `tabela_sombra` and optional inclusive clip; returns `(new_bytes,plan)`. No-body tasks avoid catalog access. Inputs remain unchanged, with no callbacks, RNG/clock, economic/world effects or rollback behavior. Unsupported record/overlay domains raise `NotImplementedError`; invalid widths/lengths raise `ValueError`, missing keywords `TypeError`. Type 13 work, selected-target/structure markers, player colors/effects, resource semantics and task/phase producers remain unsupported.

Original executable identity unchanged. Complete `AffWorkEngin 0x414A8A..0x415496` hash `4aae4288bd307f9de5b93ce32772b04ab3d7ef6803f42de3ecd412c22704694f`, full `AffEngin` caller `0x41591F..0x415A57`; EAX/EDX projected origins, low EBX actual index, pool pointer `0x4E19A0`, selection globals `0x508041/0x496AC2/0x508F8F`. [Exact-byte evidence and unchanged predecessors](../pesquisas-paralelas/graficos-animacao/evidencias/trabalho-grafico.json). Original instruction review directly establishes the task-local flag; independent native runs corroborate it, without needing new REA interpretation.

Fresh validator: **19,700 original calls / 23,007,614 observed instruction hooks**, comprising 18,516 command captures, **1,179 exact indexed buffers**, three initializations and two bank calls. Captures: **16,971 complete returns** (including 1,530 empty-body returns), **768 declared selected-target prefix stops**, **765 declared selection-info stops**, **12 declared indicator-boundary stops**. Supported calls reaching `0x41531C` resume from that checkpoint with the same CPU/stack through the real return; some calls use two bounded segments, each limited to 300,000 instructions/2 seconds. Call count is not a segment count. Unsupported boundary stops retain earlier native body effects; public preflight rejects before composition. Every complete call has ESP `0x2008004`; pool/selection globals are unchanged. Zero expected/unexpected faults, limits or skips. Capture blitters intercepted; pixel renderers and Bag query intact; only bank IO/allocation substituted. [Native report](../pesquisas-paralelas/graficos-animacao/validacao/x86-trabalho-grafico.json).

Focused matrices cover all task/phase/direction/camera/mode/+BD bytes, Bag boundaries, pool 0/799 and signed coordinate/shift edges. Each bypass task has all 256 selection-mode bytes with active selected index/BD under another camera, fatigue 0 and +BA 255, plus a native indexed empty result. Pixels exercise all 16 directions, phases 0–7 and nine body variants plus no-body/clipping cases; this does not prove phase cadence. Seven new regressions pass; graphics domain **162 tests**, zero skips and valid links. Background/table are synthetic fixtures, not mission/runtime operation.

```sh
python3 -B pesquisas-paralelas/graficos-animacao/validar_trabalho_grafico.py
python3 -B scripts/check.py --domain graphics
```

## Terrain block cache — fourteenth continuation stage

`cache_terreno.py:CacheTerreno(registros, blocos_crus, *, proximo_u16)` owns mutable copies of an explicit **1,024-byte key table**, **270,336 raw block bytes** (256×1056) and a replacement cursor in 0–255. There are no startup defaults. Each key is source u16, lighting-mask u8, discovery-mask u8; each block has 32 rows of one header plus 32 indexed pixels. `pixels(slot_u8)` reads the 1,024 pixel bytes, matching the raw block consumer's row layout. Arbitrary initial payload/header bytes remain unchanged until replacement; their contents are supplied snapshots, not original mission initialization.

`resolver_bloco_terreno(catalog, cache, *, id_terreno_u16, descoberta_u8, iluminacao_u8, tabela_sombra)` returns engine ID/branch/slot metadata and mutates only the explicit graphics cache on a miss. The two flag bytes must already be selected for the current camera/cell. Discovery **mask `0x10`** set returns blank ID1081 immediately; this differs from the sprite selector's mask31 predicate. Otherwise discovery mask is the low nibble; lighting mask is15 when `(lighting & 0x10)!=0`, else its low nibble. If both effective masks are0, return the raw source word without lookup/mutation. This direct query path can return0/FFFF; it does not prove a drawable asset exists.

Other paths search all256 keys in increasing slot order. The first exact match returns1090+slot without changing cursor, keys or pixels; duplicate precedence and reuse across cells/camera-flag high bits are preserved. On a miss, the supported copy-source domain is static IDs1–1081, each independently verified as a32×32,1056-byte full-literal block. Preflight rejects unsupported miss sources before effects; it does not emulate arbitrary native overreads/partial failures outside that domain. Hits can reuse an explicit key for other raw words without source lookup, as the original does. Invalid scalar widths/buffer sizes raise `ValueError`, missing required inputs `TypeError`, unsupported miss sources/shapes `NotImplementedError`.

Visible miss order is key source word → lighting byte → discovery byte → cursor advance modulo256 → copy all1056 source bytes → shadow-mask remap of destination indices → literal fog-mask copy. Both masks use original IDs1081–1089: nibble0 means no mask;1/2/3/4/6/8/9/12 map to1085/1084/1088/1083/1087/1082/1089/1086; other nonzero nibbles use1081. Lighting uses opacity only; fog copies literal colors, including the full blank block's palette index2. Row headers are preserved. No cache key includes the shadow table: changing that table does **not** invalidate a hit or recompute its existing pixels. No palette lifecycle rule is invented.

Original evidence: unchanged executable identity; `GetNumBob 0x40FD95..0x410085` hash `e23998884a96474e07358cacba6c6aeb2afc618b39620068504deb32c4e4a76b`; block copy/mask helpers `0x45C779..0x45C8DF` hash `31ba5b7b0943018d64fb2dda515ab99eb9cec233d8d8ffe1070c2aacb4037bca`. Capacity word `0x495BC4` is256; key pointer/cursor at`0x49A050/0x49A04E`; native EAX source word, EDX cell word, camera byte`0x508041`, discovery/lighting pointer arrays`0x507D78/0x507D88`. Cached engine IDs1090–1345. [Exact bytes and unchanged predecessors](../pesquisas-paralelas/graficos-animacao/evidencias/cache-terreno.json).

Fresh validator: **8,524 complete original calls / 104,519,504 observed instructions**, including two bank-loading calls and **8,522 full key-table/raw-block/pixel comparisons**. Native branch counts:770 undiscovered,40 direct,711 hits,7,001 misses. Every query reaches`0x3000000`, ESP`0x2008004`, preserving callee-saved registers, all visibility maps, pointer table, capacity and cache-buffer guards. Zero stops, expected/unexpected faults, limits or skips. No query or rendering primitive is substituted. Bank IO/allocation is substituted; cached payload pointers are bound in emulated RAM to a guarded, explicitly synthetic contiguous snapshot, retaining the original32×32/1056 descriptors. This is a fixture binding, not cache initialization recovered from the game. [Native report](../pesquisas-paralelas/graficos-animacao/validacao/x86-cache-terreno.json).

Coverage includes all low-five-bit flag pairs, every flag byte in additional combinations, all1081 verified sources, all256 mask pairs for seven sources under real60%/identity/synthetic shadow tables, cursor255 wrap, duplicate/raw-word hits, and eviction/recompute after table changes. Cell0/FFFF/8000/1234 and cameras0/3 exercise selected maps. [Native mask grid](../pesquisas-paralelas/graficos-animacao/artefatos/cache-terreno-mascaras.png) shows source300, discovery nibble across columns and lighting nibble down rows, with the explicit real shadow table.

The [focused REA review](../pesquisas-paralelas/graficos-animacao/evidencias/rea-cache-terreno-review.json) retains the existing French symbol/summary and cursor-division instruction at`0x40FF39`, pinned source and separate normalized/intact PE identities. Inferred Watcom signatures and existing annotations remain fallible; original instructions and independent state comparisons are authoritative. Session exported/closed. Seven new regressions pass; graphics domain **169 tests**, zero skips and valid links. Complete terrain traversal, cache startup/invalidation, world remapping, palette lifecycle and real-mission rendering remain open. No callbacks/RNG/clock or world terrain changes occur here.

```sh
python3 -B pesquisas-paralelas/graficos-animacao/validar_cache_terreno.py
python3 -B scripts/check.py --domain graphics
```

## Complete bounded terrain pass — fifteenth continuation stage

`passe_terreno.py:planejar_passe_terreno(terreno, iluminacao, *, origem, janela_celulas, margem_i8)` takes 131,072 terrain-word bytes, a selected-camera 65,536-byte lighting map, origin coordinates 0–255 and window dimensions 1–32 cells. The full viewport must remain within the256×256 map. Inset is an explicit signed-i8 field, supported only from0 through half the smaller window dimension. Negative/excessive insets and wrapped views raise `NotImplementedError`; bad widths/lengths raise `ValueError`. Maps are snapshotted, and the relevant world/visibility state must stay fixed while callbacks draw. Native initial-width word `0x49A018` and pitch dword `0x4E17A0` are both required to equal window width×32 in this domain.

Cells are row-major, rows`inset..height-inset-1`, columns`inset..width-inset-1`, with relative pixel origins32×column/row. Native `EstConstructionTerrain` classifies the raw word **702–1081 inclusive**. When that predicate is true and lighting has mask`0x10` set, the source passed to GetNumBob becomes `349+(absolute_x%8)+8*(absolute_y%8)`; otherwise it remains the raw terrain word. This is visual source selection, without changing the world word or inferring construction progress. `terreno_de_construcao(word_u16)` publishes the exact read-only predicate.

`executar_passe_terreno(plan, *, bloco, vegetacao)` calls `bloco(x,y,cell,source_word)` then `vegetacao(x,y,cell)` for **every** visited cell, including empty/hidden objects. The block callback owns GetNumBob/cache resolution and painting; vegetation owns the existing terrain-object provider. Both callbacks are required and preflighted as callable before any call; missing inputs raise `TypeError`, non-callables `ValueError`. Returns are ignored, completed calls counted, and exceptions propagate with earlier callback effects retained. No rollback or world mutation is supplied by the planner/executor.

`pixels_bloco_terreno(catalog,cache,id)` reads full-literal static blocks1–1081 or cache IDs1090–1345. Cached raw row headers are skipped without interpreting their value, matching AffBloc. Other IDs raise `NotImplementedError`; a raw query's direct ID is not automatically a drawable block. `compor_bloco_terreno(dest,w,h,pixels1024,x,y)` returns new bytes, copying32 opaque pixels per row with native pitch and **no clip rectangle**. A block must fit entirely inside the surface; otherwise it rejects before effects. Object blitters still use their explicit incoming inclusive clip, so a narrow object clip does not limit ground blocks.

Original evidence: `AffTerrain 0x41068E..0x41087E` hash `4e0b75233c42cb4e1d60daaa14b7473f19b5546507421e3520deb68e935abd0b`; `EstConstructionTerrain 0x42302D..0x423355` hash `b1992759ba7638da4f2e19ff1ecd6af250697dfd6a1e2ccd7bcf615087a790c5`; `AffBloc 0x45C72A..0x45C779` hash `99fbfda70e2038110ef2f75b657f7880296e512fc6a547bb8f0a690c8ed73c2e`. Same intact executable identity; terrain origin in EAX/EDX, map pointer`0x507D70`, window`0x508724/+2`, inset byte`0x508F90`, surface pointer`0x508F70`. [New exact bytes and unchanged providers](../pesquisas-paralelas/graficos-animacao/evidencias/passe-terreno.json).

Fresh validator: **65,536 complete predicate calls**, **80 complete terrain calls** (72 traces plus8 indexed scenes), **20 standalone block calls**, two bank calls, **72,258 bounded segments / 15,599,587 observed instruction hooks**. Terrain executes original retained-stack segments alternating before/after each cell, then reaches its actual return`0x3000000` with ESP`0x2008004`; segment count is distinct from routine-call count. No expected/unexpected faults, limits or skips. Trace-only cases intercept GetNumBob with valid returnID1 and intercept block/vegetation callbacks; predicate and lighting tests are original. Pixel cases execute terrain, GetNumBob, AffBloc and supported terrain-object renderers unchanged, comparing the complete surface, resolved IDs and final cache keys/raw blocks/cursor. Bank IO/allocation and explicit synthetic cache-payload binding remain declared fixture substitutions. World maps, attributes, clip and bank pointer inputs stay intact. [Native report](../pesquisas-paralelas/graficos-animacao/validacao/x86-passe-terreno.json). The figures in this paragraph are the stage-15 run; stage 16 below replaced the synthetic payload binding in this validator and records its own counts.

Coverage includes every u16 predicate value, every window width/height1–32 in focused traces, map corners, inset/no-cell paths, source substitution, hidden invalid words, narrow object clipping, unaligned standalone blocks and a full1024×1024 buffer. The [128×128 native terrain fixture](../pesquisas-paralelas/graficos-animacao/artefatos/cena-passe-terreno.png) uses synthetic world/cache inputs and original assets. The chosen ground assets produced the same pixels when deferred; **ordering is established by exact callback traces**, not a claimed pixel counterexample. Seven new regressions pass; graphics domain **176 tests**, no skips and valid links. Complete frame/AffSprite orchestration, negative/wrapped views, cache initialization, mission/runtime loading and consumer activation remain open.

```sh
python3 -B pesquisas-paralelas/graficos-animacao/validar_passe_terreno.py
python3 -B scripts/check.py --domain graphics
```

## Terrain cache lifecycle — sixteenth continuation stage

The original lifecycle, from exact bytes and a static caller scan: `ProgInit` runs `MemInit` (zeroes the MemAlloc byte counter `0x4E2F3C`), later `LoadSTRATBank 0x41877A`, `SetBank 0x418590`, then `CacheAlloc 0x40FA18`. `InitCache 0x40FA38` has exactly two callers: the game-start branch of `CalculGame` at `0x42D1EF`, before `MissionLoad`/`MissionLoadName`, and `MenuNewSelect` at `0x42C6A8`, before `GameLoad`. `GetNumBob 0x40FD95` (only caller `AffTerrain+0x1D1`) fills and replaces slots. `ProgExit` calls `CacheFree 0x40FA2E` before `DeleteBank`. `SetCacheBloc`, `SearchCacheBloc` and `ConstruitCache` have no direct callers or absolute references and are not part of the live lifecycle. Capacity word `0x495BC4` is 256 in DGROUP and only read. Key pointer `0x49A050` and cursor `0x49A04E` are in `.bss` (`PointerToRawData` 0, uninitialized-data flag), so both are zero at process load; only GetNumBob misses (and the uncalled siblings) reference the cursor. The scan covers direct rel32 calls/jumps and absolute 4-byte references, not computed addresses.

`ciclo_cache_terreno.py` publishes the lifecycle:

- `MemoriaMotor(*, contador_u32, vinculos)` reconstructs `MemAlloc 0x467EA6` and `MemFree 0x467ECB`. MemAlloc adds the u32 request to the counter **before** calling `GlobalAlloc(0 /*GMEM_FIXED*/, n)` at `0x467EB9`, then `GlobalLock(handle)` at `0x467EC1`, returning the lock result. MemFree calls `GlobalHandle(p)`, `GlobalUnlock(h)` (result ignored), `GlobalHandle(p)`, `GlobalFree(h)` at `0x467ED1/0x467ED9/0x467EE1/0x467EE9` and returns the GlobalFree result; it never subtracts from the counter. MemFree has no RET of its own and falls into `MemClose`'s lone RET at `0x467EF3`. `vinculos` supplies the five KERNEL32 bindings as callables returning u32. A missing binding raises `DependenciaCicloCache` at its original call site after the earlier counter/binding effects.
- `CicloCacheTerreno(blocos_crus, *, proximo_u16)` is the state after LoadSTRATBank/SetBank and before CacheAlloc: pointer 0, keys absent, 256×1,056 bank payload bytes and an inherited cursor 0–255. `CicloCacheTerreno.apos_carregar_banco(catalog)` gives the first-ProgInit state: the real BLOCS.CMP frames 1090–1345 (each its own LoadSTRATBank allocation; 254 identical, IDs 1163 and 1291 distinct) and the `.bss` cursor 0.
- `alocar(memoria)` is CacheAlloc: `MemAlloc(256<<2)`, then the pointer is stored. A second CacheAlloc is refused. The key table content of a `GMEM_FIXED` block is undefined, so `registros` stays `None` and `cache` raises until InitCache.
- `iniciar()` is InitCache: every key word/light/fog byte becomes zero (original order per entry: word +0, byte +2, byte +3) and EAX returns 256. **The cursor and all payload bytes are kept.** A zero key can never hit, because GetNumBob returns the raw word before lookup when both masks are zero. A null or freed table raises at `0x40FA49`, where the original writes through the pointer.
- `cache` returns the live `CacheTerreno` for `resolver_bloco_terreno` and `pixels_bloco_terreno`, only between InitCache and CacheFree. Restart behaviour follows: after a second InitCache, earlier keys miss again and the next miss lands at the inherited cursor over stale payload bytes.
- `liberar(memoria)` is CacheFree → MemFree. The `0x49A050` global keeps the stale pointer; the counter, cursor and payloads stay unchanged; further InitCache/cache/CacheFree/CacheAlloc calls are refused.

Saved games do not save or restore cache state: only cache routines reference its globals. Payloads are bank-owned bytes that the lifecycle never restores.

**Declared bindings.** The native bench (`bancada_ciclo_cache.py`) resolves the five KERNEL32 IAT slots `0x5231C0/C8/CC/D0/D8` to binding trampolines, as the loader would, and binds the statically linked C-runtime `fopen 0x48C71F`, `fread 0x48C97B` and `fclose 0x48C80B`. LoadSTRATBank, SetBank, MemAlloc/MemFree and the game's `FileOpen/FileRead/FileClose` wrappers, including the `0x4E1D1C` handle global, execute unchanged. `vinculos_graficos.py` holds the fixtures. `ArenaGlobalFixa` honors only `GMEM_FIXED` allocations of live blocks inside a deterministic 32 MiB arena. Handle equals pointer, `GlobalUnlock` returns 0, `GlobalFree` returns NULL, and new blocks are filled with the declared undefined-content byte `0xA5`. `ArquivosDeclarados` honors only `"rb"` opens of declared names and complete reads. Other flags, zero sizes, exhaustion, stale handles, unknown names, other modes and short reads raise `ParadaVinculo`: a reported stop, not a pass. Every call logs exact arguments and the returned value. Bank path prefix `0x509494` is a declared empty string, so names are exactly `\Graphics\Blocs.cmp` and the other five. Visibility maps, the shadow table pointer and the camera byte remain explicit harness-owned inputs. These bindings stay local until core publishes its generic facility in `ferramentas/emulador.py`; graphics will then migrate.

Original evidence ([inventory](../pesquisas-paralelas/graficos-animacao/evidencias/ciclo-cache.json), unchanged intact executable, normalized analysis PE `26c4534b…64d0` named but not executed): `CacheAlloc/CacheFree/InitCache 0x40FA18..0x40FA72` hash `29e4373d6d4dcb98bf4b5dd7feedffb24418155871a83a0e86a96b8ba601c3dc`; `MemInit/MemAlloc/MemFree..MemClose RET 0x467E34..0x467EF4` hash `b1c0ba63078aa94826d0121eb402eae066c3a916110166fc9036e86046d9c0dd`; `LoadSTRATBank 0x41877A..0x4189C2` hash `2682bf21e849d9d06d1a3a335bafb5912207c75ab2770ff3ec5a508a2e83e9da`; file wrappers `0x458420..0x458476` hash `ad54bf31c0b1fce6772da8d532fd3a0f91024b80ae83be1af57bdeade1d267b7`; ProgInit `0x474E9B..0x474ECD` hash `144952e50ac0ac4434678ef9027ade67c6a517b9bfda85410707deff30322889`; CalculGame start `0x42D1DA..0x42D239` hash `4c0bf171cb34b320c5c14948d32d8c398dfd7a96be319f8c738e5a6dfd76c636`; MenuNewSelect `0x42C693..0x42C710` hash `d3f806190ea5edfa0ab94adb5c3fbf2484c3f52bded68d81a937aff5a3bc4503`; GetNumBob is unchanged.

**Original-only captures** ([record](../pesquisas-paralelas/graficos-animacao/evidencias/captura-ciclo-cache-original.json)) were committed before the translation. Native LoadSTRATBank takes 1,229,883 instructions and 97,288 bound calls: 24,314 GlobalAlloc, 24,314 GlobalLock, 12 fopen, 48,636 fread and 12 fclose. Its counter ends at 13,508,936 = 8 + 4N + 12N + payload bytes for N = 12,156 frames. CacheAlloc binds `GlobalAlloc(0,1024)` plus `GlobalLock`, adding 1,024. InitCache returns EAX 0x100 and preserves EBX/EDX. 547 GetNumBob calls run over the real payloads: 539 after the first InitCache, eight after a restart, with the cursor wrapping and cursor 18 surviving the restart. CacheFree binds `GlobalHandle, GlobalUnlock→0, GlobalHandle, GlobalFree→NULL` and returns 0. Bank payloads for IDs 1–1089 and the 12,156 descriptors are unchanged. InitCache before CacheAlloc faults natively writing address 0 at `0x40FA49`, an explicitly expected fault.

Fresh validator `validar_ciclo_cache.py`: **554 native entries / 9,364,346 observed instructions / 97,294 bound calls**. It makes **552 whole-state comparisons**, after the bank, CacheAlloc, both InitCache calls, every GetNumBob call and CacheFree. Each compares the key pointer, all 1,024 key bytes, cursor, all 256 bank payloads, the MemAlloc counter and the exact binding log against Python. Branches: 3 undiscovered, 3 direct, 7 hits, 534 misses. The fresh run also reproduces every original-only capture row. There are no limits, skips or unexpected faults; the only expected fault is the null-table InitCache, which the model reports as a named dependency at the same address. The [report](../pesquisas-paralelas/graficos-animacao/validacao/x86-ciclo-cache.json) has no synthetic payload binding.

**Terrain-pass consumer.** `validar_passe_terreno.py` now consumes the real lifecycle instead of the synthetic payload binding. It loads the bank natively through the declared bindings, runs CacheAlloc right after it (ProgInit order), and runs native InitCache before the first pixel scene and again before the fifth (`large`, a restart). The eight pixel scenes chain over one cache like consecutive frames. The Python side composes over `CicloCacheTerreno.cache` from the same fixture position. The restart is observable: `narrow` misses into IDs 1112+ because the cursor survived. Fresh run: 65,536 predicate calls, 80 complete terrain calls, 20 standalone blocks, two bank calls, three lifecycle calls, **72,261 bounded segments / 16,013,021 observed instructions**, zero limits/skips. Surfaces, resolved IDs and final keys/payloads/cursor match natively. The 128×128 fixture image and `evidencias/passe-terreno.json` are byte-identical to stage 15. Trace-only cases still intercept GetNumBob/AffBloc/AffVegetTerrain to record callback order.

Supported limits: first-ProgInit payloads and cursor, or explicit inherited ones; capacity 256. GetNumBob before InitCache, after CacheFree or with a null table is refused rather than emulating undefined memory. GlobalAlloc failure, movable memory and short reads are fixture stops. MemInit itself, DeleteBank and the bank loader's own reconstruction are outside this stage. `validar_cache_terreno.py` keeps its stage-14 synthetic snapshot binding to cover arbitrary key/payload states that the lifecycle never produces.

```sh
python3 -B pesquisas-paralelas/graficos-animacao/capturar_ciclo_cache.py   # original-only; rewrites the two evidence files
python3 -B pesquisas-paralelas/graficos-animacao/validar_ciclo_cache.py
python3 -B pesquisas-paralelas/graficos-animacao/validar_passe_terreno.py
```

## In-game frame orchestration (`AffGame`) — seventeenth continuation stage

`AffGame 0x417698` (only caller `ProgIteration 0x475063`) switches on the game-mode byte `0x4E2F78`. Mode `0x12`, the running mission, is the branch reconstructed here, from its entry to the **HUD checkpoint `0x417B1C`**. The original order is:

1. `CalculFrame 0x43F710` runs on every call.
2. `EvenementEnCours 0x4581B6` reads byte `0x4E1B0E` into a local flag that only the HUD tail consumes.
3. The draw-cadence gate: unless `0x4E05A2` is set, the frame is drawn only when `frame 0x508F7C mod divisor 0x497284` is 0; otherwise AffGame returns.
4. The video-surface clear path (`0x508F92` with screen width 800).
5. `DDLockSurface`, storing the surface pointer at `0x508F70`.
6. The saved-background restore path (`0x49A041`).
7. `AffTerrain(0x508720, 0x508722)`, then `AffSprite` with the same origin.
8. The selection drag box (`0x4E19B0` → `Box`).
9. HUD panels, the destination-marker animation (`0x4E05AC`/`0x496204`), minimap, info texts, cursor save/draw, unlock, page flips, cursor-visibility toggle, the reset of `0x4E05A2`, `Cyclage` palette cycling every fifth frame, and the switch to mode `0x16` while an event runs. **Stage 17 does not compose this step.**

Configuration from the original bytes:
- `DDInit` sets either 800×600 with a **25×17-cell window**, or 640×480 with 20×13 cells (`0x49A018/1A`, `0x508724/26`). The pitch global `0x4E17A0` is always 800.
- `ResetMode` derives the clip `0x49A01C..22` (top, bottom, left, right) from the window and inset `0x508F90`.
- The draw divisor `0x497284` starts at 1, and `WndProc` keys set it to 1–4.
- Which frames reach AffGame is frame-loop cadence owned by ai-runtime.

**API** (`quadro_jogo.py`, the planned graphics → macOS frame contract):

`compor_quadro(mundo, tela, *, ciclo_cache, catalogo, tabela_sombra, tabela_eclairage, superficie, relogio, directdraw) -> dict`

| Input | Meaning |
|---|---|
| `mundo` | `MundoQuadro`, read-only. Terrain words (131,072 bytes), objects, auxiliaries, region/occupancy words `0x4E0F38` (131,072), units 800×276, projectiles 100×56, and four 65,536-byte discovery (`0x507D78`) and lighting (`0x507D88`) maps. These are the buffers of core's world (`tiles`, `objetos`, `donos_objetos`, `regioes`, `descoberto`, `luz_bordas`). |
| `tela` | `EstadoTela`: the 30 frame globals listed in `GLOBAIS_QUADRO`, as raw little-endian bytes. The requested `jogador_camera`, `origem`, `janela_celulas` and `margem_i8` are its `camera_u8` `0x508041`, `origem` `0x508720`, `janela` `0x508724` and `margem_i8` `0x508F90`. |
| `ciclo_cache` | The persistent `CicloCacheTerreno` after `InitCache`, threaded through every frame. It is never rebuilt per frame (see stage 16). |
| `tabela_sombra`, `tabela_eclairage` | The 256-byte tables in PaletteAlloc's buffers. |
| `superficie` | The locked surface's previous bytes, pitch × screen height (800×600). |
| `relogio` | `GetTickCount` binding (u32). |
| `directdraw` | Surface binding: `is_lost()`, `restore()`, `lock() -> (hresult, pointer)`. |

| Output field | Meaning |
|---|---|
| `superficie` | Indexed bytes at native pitch. |
| `desenhado` | `False` when the gate skips drawing. |
| `parada` | `0x417B1C`, or `'retorno'` when the gate skipped the frame. |
| `chamadas` | Ordered renderer trace with French IDs and arguments: `CalculFrame`, `DDLockSurface`, `AffTerrain(x,y)`, per cell `GetNumBob(source,cell)`/`AffBloc`/`AffVegetTerrain(x,y,cell)`, `AffSprite(x,y)`, then `AffVeget`/`AffBatiments`/`AffBatimentOmbre(x,y,cell)`, `AffEngin(x,y,index)`, `AffProjectile(index)`. |
| `efeitos` | Ordered `(name, address, old, new)` for every global write. |
| `evento` | The `EvenementEnCours` flag. |

The palette is not changed before the checkpoint; the PIE palette stays valid, and `Cyclage` comes later.

An unsupported branch raises `DependenciaQuadro(endereco, detalhe)`. It carries the **partial surface**, the trace up to and including the refused call, and the effects so far. Placeholder art is never substituted.

**Every write made while drawing** is returned, established by a whole writable-memory diff of every native frame. A frame writes nothing else, and there are no unit, world, structure or RNG writes in the supported domain.

| Routine | Effects |
|---|---|
| `CalculFrame` | Counter `0x4E17AE` += 1 (u16). Tick `0x4E17B4`. When `(tick − 0x4E17B0) mod 2³² ≥ 1000`: last tick, counter clamped to 99, ASCII digits `0x496394..96`, counter 0. Page-count text `0x4963B4` via the statically linked `itoa` of byte `0x49A05B`. |
| `DDLockSurface` | When unlocked (count `0x4E17A8` = 0 or pointer `0x4E17A4` = 0): `IsLost`, `Restore` if `DDERR_SURFACELOST`, then `Lock`. On success: pitch `0x4E17A0` = 800 and the pointer. Count += 1 on both the fresh and the already-locked path. A failed lock returns 0 without writes. |
| AffGame | `0x508F70` = surface pointer. |
| AffBatiments | On each discovered cell, `SaveCurrentClipping` copies (left, right, top, bottom) to `0x49A02C..32`, and `RestaureClipping` writes the clip back unchanged. |
| GetNumBob | Mutates `ciclo_cache` (cursor `0x49A04E`, keys, cached blocks). |

**Renderer dispatch** (domains from the original bytes; outside them the frame stops at the named address):

| Renderer | Draws in this domain | Named stop |
|---|---|---|
| `AffVegetTerrain` | Objects 0 and 253, and cells with `discovery & 31`, skip. Other codes use V6 `consultar_objeto_v6`. | `0x410085` |
| `AffVeget` | Codes outside the 23-entry table at `0x415A58` return at `0x410B38`. Trees 1–11 use V5 `consultar_objeto`. | Codes 27 and 55–65: `0x415ACF` |
| `AffBatiments` | Undiscovered cells (`CaseEstDecouverte`: `discovery & 0x10`) return. Discovered cells save the clip, check objects 254/253, check the 19 facade-trigger terrain words (`0x2CB..0x436`) and workshop word `0x356`, then restore the clip. | Building occupancy bit 15 of `0x4E0F38`: `0x407DEF`. Objects 254/253 (ChercheIndiceBatiment): `0x407EA7`/`0x407FB8`. Facade triggers: `0x40F23B`. Workshop: `0x40288B`. |
| `AffBatimentOmbre` | A literal RET. | — |
| `AffEngin` | Routing by `encaminhamento` for types 0/5/6/7/9; the `sem_desenho` route draws nothing (for example MONDE01's type-9 state 14). Bodies use `compor_unidade` only with all of: states 2/7, owner 0 = camera 0, `u16 +0x74 ≥ 100`, `+0xBA = 0`, `+0xBD = 0`, not the selected unit (`0x496AC2`), selection mode `0x508F8F` = 0, direction 1–16, phase 0–7. | Everything else: `0x41591F` |
| `AffProjectile` | The public projectile renderer with the selected camera's lighting. | `0x46FF70` |
| Selection box | — | `0x417AC8` |

**Stops before drawing:** mode ≠ `0x12` (`0x4176A8`); divisor 0 (`0x417921`); the clear path (`0x41794B`); a NULL lock (`0x4179D4`); the background restore (`0x4179E1`); and an `AffTerrain` or `AffSprite` viewport outside the reconstructed domain (`0x41068E`/`0x416864`). The terrain domain requires window width × 32 = pitch = screen-width word, so the 640×480 mode stops. The sprite domain requires `origin + window + 8/10 ≤ 256`.

**Bindings.** On top of the stage-16 bank and memory bindings:
- KERNEL32 `GetTickCount` (IAT `0x5231B8`).
- The `IDirectDrawSurface` methods reached through the COM object at `0x4E1790` (vtable `+0x60` IsLost, `+0x64` Lock, `+0x6C` Restore, `+0x80` Unlock). The fixture is never lost. Lock honors only a whole-surface `DDLOCK_WAIT` with a 0x6C-byte descriptor, writing `lpSurface`/`lPitch`; Restore and Unlock stop.

The bench follows ProgInit's order:
1. `PaletteAlloc` runs natively through the allocation bindings.
2. LoadSTRATBank, SetBank and CacheAlloc run.
3. Native `CalculTabPlayer` builds the player tables, which equal the committed `construcoes.tabelas_jogador()`.

The shadow and lighting contents are the real 60% tables from earlier native captures. All renderers execute unchanged inside the whole code section; only the bindings are replaced.

**MONDE01 checkpoint.** The frame consumes missions' committed MONDE01 checkpoint. With core's discovery domain integrated, the `MissionPlaceTerrain` unit scan completes all 16 units to the pre-structure checkpoint `0x46C16D`. The buffers are pinned as [a hashed snapshot](../pesquisas-paralelas/graficos-animacao/evidencias/monde01-checkpoint-quadro.json) (9 KB zlib), recording the checkout revision, so later upstream progress cannot silently change the validated input; the capture script re-pins from the live pipeline. Declared synthetic inputs:
- From missions: the unit-pool pre-fill, regions, selections, search context and bonus table.
- From this stage: the camera/viewport (origin (0,0), camera 0), the zero projectile and structure pools, and the background surface.

The native frame completes to `0x417B1C` (2,201,940 instructions; 16 AffEngin calls). The model draws the whole terrain pass and sprite rows 0–13, then stops at **`0x40F23B` for facade trigger `0x2ED` at cell 3345 = (17,13)**. That is the trigger cell of MONDE01's single type-2 structure, whose origin is cell 2828; its facade is drawn from terrain words even before the mission places the structure. The next blockers are MONDE01's units: `+0x74 = 0` enables an overlay; types 1 and 8. [Partial frame preview](../pesquisas-paralelas/graficos-animacao/artefatos/quadro-monde01-parcial.png).

Original evidence ([inventory](../pesquisas-paralelas/graficos-animacao/evidencias/quadro-jogo.json), unchanged intact executable, normalized PE named but not executed):

| Region | SHA-256 |
|---|---|
| `AffGame 0x417698..0x417F38` | `0eeac1cee741e147e5c1979a320bbb280fea3d5151c7cf662de6c514cbd6583a` |
| `CalculFrame` | `ec7f8002…a592` |
| `DDLockSurface` | `3b685f16…4b34` |
| AffBatiments prefix | `616969e1…1be9` |
| AffBatiments switch/tail | `d8fa5152…4fa7` |
| AffVeget table/prefix | `4f9c9cad…b526` |

Unchanged `AffSprite`/`AffTerrain`. The inventory also holds DDInit, WndProc and ResetMode evidence and a static absolute-write scan.

**Validation:**
- **Original-only capture** ([record](../pesquisas-paralelas/graficos-animacao/evidencias/captura-quadro-original.json)): 21 native entries / 23,908,934 instructions / 97,331 bound calls over seven frames. It was first committed before translation (`077a05b`), then regenerated by the same native-only script after main advanced the MONDE01 checkpoint.
- **Fresh run `validar_quadro.py`**: 26 native entries / 44,585,739 instructions / 97,346 bound calls over **nine frames**.
  - Six are complete: terrain and objects; units and projectiles; inset 1 at origin (2,3); a gate-skipped frame; a forced frame with an event and FPS clamp; and a cache restart. Each has whole-frame equality of the 800×600 surface, canonical trace, all 30 globals, cache keys/blocks/cursor, and the full memory diff restricted to those globals.
  - Three are named stops: the MONDE01 facade, the selection box, and real MONDE01 terrain over synthetic visibility. Native memory is restored and rerun to the same original address after the same trace event, then compared.
- Every fresh native frame reproduces its original-only capture. There are no limits or skips.
- [Report](../pesquisas-paralelas/graficos-animacao/validacao/x86-quadro-jogo.json).

**Not composed:** the HUD and everything after `0x417B1C`, palette cycling, the 640×480 mode, wrapped or negative viewports, building facades and structure lookup, the selection box, the clear and restore paths, unit bodies outside the guard, and AffVeget handlers 27/55–65.

```sh
python3 -B pesquisas-paralelas/graficos-animacao/capturar_quadro.py   # original-only; rewrites the two evidence files
python3 -B pesquisas-paralelas/graficos-animacao/validar_quadro.py
```

## Terrain objects and sequential codes

`objetos.py` reconstructs visibility predicates, terrain/sprite passes, tree progression, and the v5 catalog. Discovery requires `(flag & 31) == 0`; lighting requires `(flag & 16) == 0`. These per-player flags are external runtime inputs, not automatically the ETA disk attribute byte.

`sequenciais.py` adds codes 54/66/67/68 through `consultar_sequencial`, `consultar_objeto_v6`, `ler_objetos_eta_v6`, and `normalizar_inicio`. The relevant `AffVegetTerrain` range is `0x410085` onward; 66 enters `0x4104AF`, 67/68 enter `0x4104B1`. For auxiliary byte 0–31:

```text
visual_phase = floor(auxiliary / 2)
engine_id = 0x2A47 + 16 * (code - 66) + visual_phase
```

| Code | Engine IDs | OTHERS local indices | Draw offset |
|---|---|---|---|
| 66 | 10823–10838 | 3183–3198 | −4, 0 |
| 67 | 10839–10854 | 3199–3214 | 0, 0 |
| 68 | 10855–10870 | 3215–3230 | 0, 0 |
| 54 | 10823, fixed | 3183 | −4, 0 |

The runtime original accepts the whole auxiliary byte and can cross into subsequent sequences. The public contract only exposes 0–31 for 66–68. This is an indexed visual phase, not proven temporal animation. Code 54 ignores the auxiliary. Without discovery there is no layer; lit cells copy once; unlit cells copy then shadow with the same ID/position. These codes do not draw through the `AffVeget` sprite pass.

The mission-load loop `0x46C3DE..0x46C40A` visits all 65,536 cells and changes code 54 into 66 with auxiliary 1. `normalizar_inicio` reproduces only that loop on new layer copies. It does not implement full `MissionLoad`, terrain placement, or later simulation updates.

V6 maps 51 codes and all **486/486 nonzero serialized mission-1 objects**. Sixteen records are the newly mapped sequences: seven code 66 and nine code 67, auxiliaries 1–14. The stage records 147 associations and 48 distinct sequence frames, 6,144 domain captures, 142 indexed pixel-buffer comparisons, two complete normalization fixtures, and 4,096 no-change `NextAnim` checks. Appearance descriptions do not identify economic resource meaning or consumption rules.

## Reproduction and provenance

```sh
python3 -B pesquisas-paralelas/graficos-animacao/validar_python.py
python3 -B -m unittest discover -s pesquisas-paralelas/graficos-animacao -p 'test_*.py' -v
```

Individual `validar_x86.py`, `validar_trabalhadores.py`, `validar_composicao.py`, `validar_construcoes.py`, `validar_objetos.py`, and `validar_sequenciais.py` scripts reproduce original-x86 comparisons. They require the hash-identified local input copies, dependencies, and reference snapshot. Generated reports/artifacts belong only to this domain.

The original private reference snapshot is commit `1c8ebdd43b0a820652b7cb852ae1fe218d4dea5e`. Keep that snapshot and its manifest immutable. Predecessor-source hashes in `evidencias/proveniencia-v6.json` deliberately refer to historical implementations. Current research must append provenance instead of rewriting old claims.

Next: remaining building render mappings, workshop-trigger gate terrain, general building tails and original scene render-order callers. The gate facade and supported full-return path are bounded indexed composition scenarios; they do not implement physical gate effects, establish economic semantics, or integrate the older macOS preview.

## Static M1 render (optional)

See `pesquisas-paralelas/graficos-animacao/RENDER_M1_ESTATICO.md`: terrain/vegetation render of the accepted MONDE01 M1 state; the Santuario facade stops at `0x407DEF` (structure occupancy, not reconstructed).

## AffGame write set between frames (M2 dependency)

See `pesquisas-paralelas/graficos-animacao/ESCRITAS_AFFGAME_ENTRE_QUADROS.md`: static closure plus native M1 capture; verdict per address (the shared RNG cursor `0x4e1d18` is the only one with state-dependent writes).

## Declared display backend (M2 round 3)

See `pesquisas-paralelas/graficos-animacao/FRONTEIRAS_EXIBICAO.md`: `fronteiras_exibicao.py` (Core16 DirectDraw COM backend; original wrappers run natively), boundary table, bank/file inventory and RestoreAll's static DGROUP effects.

- [Logic-state effects of RestoreAll/AffGame](../pesquisas-paralelas/graficos-animacao/EFEITOS_LOGICOS_EXIBICAO.md): native capture shows no logic-read byte written in the captured domain; `efeitos_logicos_exibicao.py` provider with named stops.

## M3 preparation: native pixel reference, structure facade in the frame, render API

**Reference.** [capturar_quadro_original_pixels.py](../pesquisas-paralelas/graficos-animacao/capturar_quadro_original_pixels.py) runs Missions' display scenario to the real entry of AffGame in `between_frames` (frame 1), saves the entry state, and runs the intact AffGame natively to the HUD checkpoint `0x417B1C`. [quadro-original-pixels-m1.json](../pesquisas-paralelas/graficos-animacao/evidencias/quadro-original-pixels-m1.json) (199 KB, every block hash-verified on load) holds the entry state the composition needs, the 1000×276 structure pool, BatimentEstHabiter's native result per occupied record, and the 800×600 offscreen surface before and at the checkpoint. [quadro-original-pixels-m1-modos.json](../pesquisas-paralelas/graficos-animacao/evidencias/quadro-original-pixels-m1-modos.json) holds the same run with the Santuário's mode byte `+5` set to 0..7 (surface hash and a crop of the facade box). Requires `RISING_EMULAR` only to regenerate; the tests read the fixtures.

**What the Python frame now reproduces.** `quadro_jogo.batiments` follows AffBatiments for structure cells: occupancy lookup (`0x407DEF..0x407E56`), the foreign-owner visibility byte, the type-2 facade through the committed seven-layer `construcoes` provider (terrain word `0x2ED`, modes 3/4/5 share the same layers at `0x40873A`), and the `0x40F342` tail (AffVehiculeAtelier only for terrain `0x356`, selection frame and gauge only for a selected structure). Against the native surface at `0x417B1C`, every pixel above row 279 is equal: terrain, vegetation and the full Santuário facade; modes 3, 4 and 5 equal the original's facade crop pixel for pixel (the original draws the identical image for the three).

**Named stops (visible, not guessed).** `0x41591F`: the 16 M1 units have life word `+0x74` = 1 (< 100), which enables the tired/overlay branch of the unit body (`0x414320..0x414409`, `TypeEnginSeFatigue`) that no committed unit module covers; this is the first stop and all later sprite cells are absent. `0x408AC8`: modes 0, 1, 2, 6, 7, for which the original draws one common image different from the facade (identical across those five modes; captured natively, not reconstructed). `0x40892D`: uninhabited facade (gray effect). `0x40863E`: mode 3 uninhabited (advances the RNG cursor). `0x4022C8` / `0x4020EC`: selection frame / gauge of a selected structure. The raid unit (unit 16) on screen and the effect projectiles 31/32 were captured as logic-state-clean (see EFEITOS_LOGICOS_EXIBICAO.md) but their **pixel** composition is not reconstructed; the composition stops at the unit overlay before reaching them.

**Render API, contract version 1.2** ([render_quadro.py](../pesquisas-paralelas/graficos-animacao/render_quadro.py)). This is the contract the macOS integration layer consumes. A change of any input, output field, format or stop semantics bumps `VERSAO_RENDER_QUADRO` (major for breaking changes, minor for additions); the version is returned in every result.

```python
VERSAO_RENDER_QUADRO = (1, 2)
renderizar_quadro(memoria, *, superficie_anterior, catalogo=None, paleta=None, habitado=None, relogio=None, cache=None) -> QuadroRenderizado
regioes_necessarias(memoria) -> [(start, end_exclusive, name)]
QuadroRenderizado(versao, largura, altura, pixels, rgba, parada, chamadas, efeitos, cache)
EstadoCache(registros, blocos_crus, proximo)
carregar_superficie_inicial(caminho) -> bytes
carregar_cache_inicial(caminho, catalogo=None) -> EstadoCache
```

*Inputs.*
- `memoria` (required): the `MemoriaDeclarada` read contract, `u8/u16/u32(address)` and `ler_mundo(address, n) -> bytes`, over the live game memory (original addresses). It is never written. Declare the regions of `regioes_necessarias(memoria)`: DGROUP+.bss `0x494000..0x523000` (includes the 1000×276 structure pool at `0x49A0C8` and the frame globals) and the buffers addressed by the slots `0x507D70, 0x507D74, 0x507DAC, 0x4E0F38, 0x4E19A0, 0x5080F0, 0x507D78+4c, 0x507D88+4c` (c = 0..3). An undeclared read raises the memory's own error.
- `superficie_anterior` (required): exactly 800×600 bytes of palette indices, row-major, the surface the game draws over (AffGame does not clear it); anything else raises `ValueError`.
- `habitado(indice) -> bool` (optional, required once a structure is occupied): BatimentEstHabiter, economy's result for structure `indice`. Without it the frame stops at `0x40F378`.
- `relogio() -> int` (optional): GetTickCount; default the tick copy at `0x4E17B4`. `catalogo`/`paleta` (optional): asset catalog and a 768-byte palette; defaults are the local PLATGAME assets.

*Outputs* (`QuadroRenderizado`, frozen).
- `versao`: `(1, 2)`. `largura`, `altura`: 800, 600.
- `pixels`: 480,000 bytes, palette indices, row-major, origin top-left, pitch 800. The surface after the composed passes; pixels the composition did not reach keep `superficie_anterior`.
- `rgba`: 1,920,000 bytes, 4 bytes per pixel (R, G, B, 255), same order as `pixels`; `rgba[4i:4i+3] = palette[3*pixels[i]:3*pixels[i]+3]`.
- `parada`: `None` for a complete composition, otherwise `{'endereco': '0x........', 'detalhe': str}`: the first original branch the reconstruction does not cover. The frame is then **partial** (everything drawn before the stop is exact, everything after is absent); the consumer must show or log it, never treat it as complete.
- `chamadas`: ordered tuple of the original calls the composition made (`('AffTerrain', ...)`, `('AffBatiments', x, y, cell)`, ...). `efeitos`: tuple of `(name, address, old_hex, new_hex)` writes the original would make to the frame globals (informational; the memory is not modified).

*Palette.* PLATGAME.PIE: 256 entries × 3 bytes, 8-bit RGB (the 6-bit VGA values expanded ×4, so the maximum component is 252), no gamma. It is the static palette: the live palette cycling (`Cyclage`) and any palette change after load are not applied. Pass `paleta` to override.

*Supported domain.* Mode `[0x4E2F78] = 0x12` (in-game), 800×600 session (`[0x49A018] = 800`, window 25×17 cells), camera 0..3, terrain/vegetation/structure passes as captured. Frame cadence gates (`[0x4E05A2]`, divisor) can return an undrawn frame (`pixels == superficie_anterior`, stop at the cadence return). The HUD (from `0x417B1C`), the selection drag box, other game modes and the video-surface clear path are outside; they stop at their original address.

*Named stops* (address → meaning). `0x4176A8` mode ≠ 0x12; `0x41794B` video-surface clear; `0x4179D4` lock returned NULL; `0x4179E1` saved-background restore; `0x41068E`/`0x416864` viewport outside the reconstructed terrain/sprite domain; `0x417AC8` selection drag box; `0x41591F` unit body outside its validated domain (type without a committed body: 1 and 8 in MONDE01; owner/overlay conditions of the validated body); `0x46FF70` projectile outside its domain; `0x40863E`/`0x40892D`/`0x408AC8` structure mode 3 uninhabited / uninhabited facade / modes 0, 1, 2, 6, 7; `0x4087AA`/`0x40F378` habitation provider missing; `0x4022C8`/`0x4020EC` selection frame / gauge; `0x407EA7`/`0x407FB8`/`0x40288B`/`0x40F23B` wall, gate, workshop and other structure facades; `0x410085`/`0x415ACF`/`0x40FD95`/`0x45C72A` terrain object, vegetation, block and engine-ID outside the committed domain. The full list grows only by reconstructing a pass, never silently.

*Properties.* Pure function, no files after the catalog loads, no emulation, about 0.3 s per frame, deterministic. Verified against the original: [fixture and native pixels](../pesquisas-paralelas/graficos-animacao/evidencias/quadro-original-pixels-m1.json); all pixels above row 279 equal at the M1 post-load frame (terrain, vegetation, Santuário facade), first stop `0x41591F`.

*Changelog.* **1.1** (additive, not breaking): the low-life tired icon of units is composed (tail `0x413568..0x413655` of the body routine: word `+4` = word `+0x76`, life `< 100`, `(life/5)` even, `TypeEnginSeFatigue` true → bob `word(+4) + 0x1E2B` drawn with the owner's player table at cell origin − (8, 11)), so the M1 frame no longer stops at unit 0: types 0, 5, 7 and 9 now match the original pixel for pixel. The first stop moves to `0x41591F` for unit 15 (type 8 has no committed body); type 1 (unit 11) is the next. Experience icon (`+0xBA ≠ 0`), a nonzero body shift with the icon, and owner ≥ 5 stop. **1.0**: initial contract.

Native evidence for 1.1: [captura-cauda-engin-m1.json](../pesquisas-paralelas/graficos-animacao/evidencias/captura-cauda-engin-m1.json) (hooks on the tail inside the real AffGame run: per unit the gate values, TypeEnginSeFatigue's answer and the PastePlayerCmp arguments). With types 1 and 8 skipped, the Python frame differs from the original only inside those two units' footprints (2,080 pixels); every other pixel at the HUD checkpoint is equal.

### Playback sequences (contract 1.2, additive)

**What persists between frames.** Two things outside the live game state feed a frame: the surface AffGame draws over, and GetNumBob's terrain cache (a cache hit reuses its stored pixels even when lighting or discovery changed, so a sequence is exact only if the cache is carried). `renderizar_quadro` therefore takes `cache` (an `EstadoCache`, `None` = the cold cache) and returns the state after the frame in `QuadroRenderizado.cache`.

**Chaining rule.** Render frame k over the `pixels` of frame k−1 and with the `cache` of frame k−1:

```python
pixels, cache = carregar_superficie_inicial(SUPERFICIE), carregar_cache_inicial(CACHE)
for k, memoria_k in enumerate(memorias, 1):      # one live-memory view per drawing phase
    q = renderizar_quadro(memoria_k, superficie_anterior=pixels, cache=cache, habitado=...)
    pixels, cache = q.pixels, q.cache
```

Which phases draw: **AffGame in `between_frames(k)`** (the ProgIteration tail after CalculGame(k−1); `between_frames` is k = 1) and the `RestoreAll` of the load tail (before the sequence). `frame(k)` (CalculGame) and the window-loop remainder leave the surface unchanged: the original's surface hash is equal at the end of `between_frames(k)` and `frame(k)`. The memory view for AffGame(k) is the state at the entry of AffGame in `between_frames(k)`; the display-only bytes AffGame itself writes (fps, ticks, clip words) do not change the pixels. Not reproduced: everything AffGame draws after the HUD checkpoint `0x417B1C` (the bottom strip from row 544 and the cursor), so in a chain those pixels keep the initial surface's values, and a stop (`parada`) leaves the later sprite cells as they were.

**Initial artifacts (M2.2 sequence start, -v2 display scenario).**
- [superficie-inicial-m22-v2.json](../pesquisas-paralelas/graficos-animacao/evidencias/superficie-inicial-m22-v2.json): the original's 800×600 offscreen surface at the entry of AffGame in `between_frames`, after the load tail (RestoreAll and the MenuInit tail). SHA-256 `e8cb862d…2db76`, **equal to the surface hash Missions' capture records for the `load_tail` phase**; provenance (producing revision, source capture and its hash, command) inside. Load with `carregar_superficie_inicial`.
- [cache-terreno-inicial-m22-v2.json](../pesquisas-paralelas/graficos-animacao/evidencias/cache-terreno-inicial-m22-v2.json): the terrain cache at the same instant (256 keys, cursor 76, the 76 payloads GetNumBob rewrote; the others are the bank's original payloads, hash-pinned). Load with `carregar_cache_inicial`.
- Captured natively by [capturar_serie_quadros.py](../pesquisas-paralelas/graficos-animacao/capturar_serie_quadros.py) (about 2 min), committed before use.

**Are the M2.2 capture's surface hashes usable?** [superficies-fase-m22-v2.json](../pesquisas-paralelas/graficos-animacao/evidencias/superficies-fase-m22-v2.json) extracts them (257 phases; pinned to the xz capture's SHA-256). They are SHA-256 of the **complete** surface at the end of each phase (primary equals offscreen after DDFlipPage). They witness the native run (my native phase-end surfaces equal them in all 12 frames checked) and are the right check for a *complete* render. They **cannot** validate the Python frame today: the render stops at the HUD checkpoint and has the type 1/8 stop, so its surface cannot equal a post-HUD hash. For the Python comparison use the native checkpoint surfaces in the verification below.

**Verification** ([verificacao-cadeia-m22-v2.json](../pesquisas-paralelas/graficos-animacao/evidencias/verificacao-cadeia-m22-v2.json), frames 1..12, native run plus the chain above):
- The native phase-end surface hash equals Missions' recorded hash in 12/12 frames; the cache carried by the chain equals the native cache at every frame entry (keys, cursor and payloads).
- **First stop and first differing frame: frame 1**, `0x41591F` (unit 15, type 8, then type 1: no committed body). Frames 1–5 differ in the rows below the sprite cut (the view scrolls one cell per frame toward origin (0,0), so those units move down 32 pixels per frame).
- From **frame 6** on (view origin (0,0), the two unreconstructed units are below the visible window) the composed rows 0..543 equal the original's checkpoint surface exactly when drawn over the native previous surface, and the chained render differs only in the bottom strip (rows ≥ 547: HUD, not composed).
- So the chain is a faithful playfield render from frame 6 of this sequence; before that it is partial by the named stop.
