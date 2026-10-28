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

Next: remaining building render mappings, the shared gate/building tail and original scene render-order callers. The gate facade is a bounded indexed composition scenario; it does not implement physical gate effects, establish economic semantics, or integrate the older macOS preview.
