# Graphics and animation contract

Owner: graphics. Active implementation, synthetic/reference tests, indexed-buffer artifacts, and original-byte extracts live in `pesquisas-paralelas/graficos-animacao/`. Historical frozen releases are immutable records in the workspace archive and in the pre-organization Git history. Never edit a frozen release's text or inputs to modernize it: its manifest hashes identify the exact original record.

## Banks, pixels, and palette

The concatenated bank order is `BLOCS`, `TROOPS`, `VEHICULE`, `CREATURE`, `BUILDING`, `OTHERS`, with counts 1,345 / 2,848 / 915 / 1,920 / 611 / 4,517. Engine graphic IDs start at **1**; local/global API indices start at **0**. `INVENTE` and `MENU` are separate banks. Use `localizar`, not a guessed equality between an engine ID and a file index.

`graficos.py` reads CMPs with a separate opacity mask: a literal palette index zero stays opaque. A transparent skip is not the same as literal zero. Preserve clipping, source anchors, indexed pixels, and destination state before converting to RGBA. `Catalogo` verifies copied input files against `fontes/manifesto.json`.

The current graphics reader's palette behavior is authoritative for graphics tests. Earlier prototype palette expansion was a preliminary implementation; do not silently use it as the current original-renderer oracle. `composicao.py` reconstructs palette/shadow tables and composition. Shadows remap the destination through a 256-byte table under a CMP mask; they are not a black alpha overlay or a second dark sprite.

## Unit and building coverage

The verified unit bodies cover type 0 `SOLDADO`, 5 `FAZENDEIRO`, 6 `MECÂNICO`, 7 `CONSTRUTOR`, and 9 `COLONO`, including recovered stop/movement frames, anchors, direction, and bag-related branches where supported. Keep original French INI keys and recovered offsets. Do not generalize a soldier's frame groups to every unit type or infer a complete action from a visual strip.

`construcoes.py` provides verified Sanctuary facade layers, player tables/clocks, and structure ETA reading. A disk record, a prepared runtime structure, its physical gate counter, and a render plan are different data contracts. Graphics consumes explicit simulation state; core owns collisions and gate progression. New gate sprite associations require byte/address evidence and indexed-buffer comparison, not the apparent shape of a frame.

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

Next: remaining building/gate render mappings, original render-order callers, and one bounded composition scenario with exact indexed output. Publish required input fields and supported values to core; do not implement physical gate effects, infer economic semantics from pixels, or silently integrate the older macOS preview.
