# Harvest probe graphics and exact view-origin evidence

Dispatch base: integrated render API 1.8, main `ef52cb0` (merged before research). Delivery is feature-branch push
only. No main integration or acceptance is authorized. Original executable SHA-256 remains
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

## Declared native matrix, before translation

`evidencias/origens-colheita-proveniencia.json` pins the source ref, input files, published frame records, baseline
logic-effect provider and every new view origin. The three reported stops are the first occurrences: K1 subsequently
traverses 32 additional unproved origins. The full new origin set therefore contains 35, not just three.

| Probe | Full drawn window | New origin evidence |
|---|---|---|
| K1 | 129–629 (501 phases) | First actual AffGame entry at each of 33 unproved arrow-scroll origins |
| P4 | 129–3129 (3001 phases) | First actual AffGame entry at (10,16), after native minimap input |
| P5 | 129–3129 (3001 phases) | First actual AffGame entry at (31,0), after native minimap input |

`capturar_sondas_colheita_graficos.py` consumes the pinned original-only display recorder and native input bench.
Each invocation contains at most 750 frames and an 18-minute internal checkpoint budget. The planned P4/P5 chunks
are 129–728, 729–1328, 1329–1928, 1929–2528 and 2529–3129; checkpoints remain local scratch data. Both native phase
surfaces and the complete end-frame state must match the published probe at every frame.

`isolar_origens_sondas_graficas.py` pauses at the real AffGame entry, saves CPU context, DGROUP, CRT, every allocation,
native stack, declared host state and DirectDraw surfaces, and executes the intact routine to its native caller
return. No record, camera, cursor or input write is applied. Hooks only observe. It records all changed DGROUP/CRT
bytes and heap-block differences, entry/exit registers, original code hash and the full offscreen surface hash.
The exact saved entry is restored, then the ordinary phase runs and must still match its published whole-state and
surface hashes. This distinguishes origin sampling from native proof of the actual selected/work probe state.

The AffGame logic-effect domain and RestoreAll domain will remain distinct unless both have native evidence.
Unproved origins and other existing guards remain named stops; no general map-bounds fallback is introduced.

## Text and surfaces

The existing strict `FronteiraTextoGravada` adapter validates every AffText argument and the complete pre-text
surface before accepting the probe's declared non-execution. It remains a validation fixture, never a default
glyph provider. Every comparison uses the entire 800×600 indexed surface and exact raster argument sequence.
The chained Python result must supply its own next surface, terrain cache and saved tooltip background.
TextGetMessage's declared zero return remains unchanged; the renderer never substitutes an unavailable pointer.
