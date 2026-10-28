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
| Unit action handlers | `AffEngin` dispatches to attack `0x41374C`, construction `0x414495`, work `0x414A8A`, death `0x41559A` | Map each supported type/action input and coordinate simulation phase producers |
| Projectile display inputs/rendering | The 100-record selection/sort, cell queries and public `AffProjectile` mapper/compositor are reconstructed; eight bounded complete sprite scenes use the public renderer | Integrate the consumer and physical producers; preserve explicit catalog limits and raw phase semantics |
| Projectile/effect lighting | `CalculEclairage`, clipping-enabled mask remap and public projectile consumers are independently validated | Recover remaining palette effects and their lifecycle separately |
| Scene traversal/projection | Complete interior `AffSprite` planning/execution and relative projection are reconstructed; native complete-pass traces and bounded indexed scenes match | Recover margin wraparound/negative origins, `AffGame` projection/cadence and a real-mission consumer |
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
