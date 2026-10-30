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

## Additive 1.9 contract

`VERSAO_RENDER_QUADRO = (1,9)`. Function arguments, required regions, result fields, palette/cache format and the
existing optional text/habitation/clock callbacks remain unchanged. The consumer must update its explicit pin.
`camadas_colheita_m3.json` contains the exact added AffGame origins and the builder work family; it is data the
engine workstream can port alongside the existing 1.8 layer plans.

The AffGame logic-effect provider accepts the 35 new origins only after the corresponding isolated native calls
are committed. `ORIGENS_RESTOREALL_PROVADAS` retains the previous 108-origin domain; the new calls do not establish
RestoreAll behavior. `ORIGENS_PROVADAS` is the 143-origin AffGame domain. Other origins still stop at `0x415B77`,
and the previous structure/shake/projectile guards remain in force. The HUD flag `0x4E05A2` remains game logic,
handled by the existing AI `affgame_hud_ia` provider. Validation compares its flag stores and leftover EAX against
the original, rather than adding that byte to a display exclusion mask. No additional logic write is assumed empty.

P5's selected owner-0/camera-0 builder (type 7, state 5) adds the actual mining routes at `0x414A8A`: task 0 draws
the selected frame, order markers, shadow, body and existing information tail; tasks 1/2 return before that entire
prefix, so the builder has no selection frame, body or information gauge while mining. Native frame 594
proves the approach route, frame 610 mining, and frame 760 the one-frame exit. The body uses anchor (26,26), raw count 8, fixed stride 8, and bases
1338/1466 for empty/nonempty bag. ID = base + floor((direction+1)/2)*8 + raw phase, with no count-derived stride or
phase masking. Shadow 10784 remains at shifted cell origin+(2,26). Owner, camera, effects, oscillation, raw count,
direction and phase are bounded; other work tasks remain `0x414A8A`. Existing health/bag/fatigue/experience guards
apply when the information tail is reached. No simulation, resource or task update is performed by rendering.
The body bases, fixed stride, anchors and bag choice retain the unchanged prepared-worker proof in
[x86-trabalho-grafico.json](validacao/x86-trabalho-grafico.json): 18,516 original command cases and 1,179 indexed-buffer
cases, replayed by the graphics gate. The new P5 evidence proves the selected prefix/tail and early-return integration.

The original-only capture producer remains independent of reconstructed code. Its first K1 attempt completed all
33 isolated calls but failed when saving the observer in the resumable checkpoint. The trace and native observations
are preserved; detaching the observer before snapshot serialization fixed it. The bounded 61-frame retry completed,
reproduced every published state/surface hash and saved its checkpoint. This was a host capture-tool error, not an
oracle mismatch. Historical evidence and predecessor source pins remain unchanged.

## Bounded reproduction

Run from this Graphics worktree with the intact media/input links present. A new start folder can be prepared with
the preceding original-only `capturar_sondas_graficos_m3.py --prepare --start <folder>` command under its own lease;
it verifies the accepted M2.2 frame 128 summary. The existing local start folder is `.local/graficos-api17-start`.
Never overwrite a frozen capture or an existing checkpoint while regenerating evidence.

```sh
python3 "/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py" graphics-harvest-reproduce -- \
  python3 -B pesquisas-paralelas/graficos-animacao/capturar_sondas_colheita_graficos.py \
  --start .local/graficos-api17-start --probe P4 --to 728 \
  --output .local/recaptured-P4-129-728.json.xz
```

For P4 and P5 separately, continue targets 1328, 1928, 2528, 3129 with `--resume <start>/<probe>-<previous:05d>.pickle`.
Each invocation must acquire its own lease. K1's new origin calls use the same producer with `--probe K1 --to 189`;
the existing 1.8 recording supplies the complete 129–629 full-surface comparison. Each xz file has separate manifest
and `.origins.json` files; the manifest records compressed/raw hashes, input/ref/producer/code identities, actual
frame interval, elapsed native seconds and checkpoint hash. The isolated cases apply no declared state writes.

Pure-Python pixel/argument/effect replay can wait for each completed native segment while carrying its own outputs:

```sh
python3 -B pesquisas-paralelas/graficos-animacao/validar_colheita_graficos.py \
  --probe P4 --probe P5 --probe K1 --wait-captures \
  --output pesquisas-paralelas/graficos-animacao/validacao/colheita-graficos-final.json
python3 -B pesquisas-paralelas/graficos-animacao/validar_origens_colheita.py \
  --output pesquisas-paralelas/graficos-animacao/validacao/origens-colheita-final.json
```

The recorded AffText adapter is explicit. There is no glyph fallback, surface patching or cache repair. Full DGROUP
effects retain only the two established DirectDraw binding-pointer exclusions, while every pixel is compared.
The final reports pin their exact implementation/table/comparison sources. Parallel per-probe replay reports may be
combined only when all source pins are identical and still match the working source bytes.

## Final evidence ledger and results

The evidence commits precede the translation commit: `5d0e736` declares the matrix; `2e24188` captures P5 approach
and mining, `99c5952` the completed K1 retry, `42aef49` P4 approach/harvest, `fbf6200` P4 continuation, `8a35073` P5
mine exit, `5593df2` both probes through 1928, `7ecb551` both through 2528, and `f5c89bc` both through 3129.
All output files below are in `evidencias/`, with compressed/raw SHA manifests and isolated-call sidecars.

| Evidence commit | Native frames | Native seconds | Capture basename |
|---|---|---:|---|
| `42aef49` | P4 129–728 | 335.117 | `sonda-colheita-P4-129-728.json.xz` |
| `fbf6200` | P4 729–1328 | 317.297 | `sonda-colheita-P4-729-1328.json.xz` |
| `5593df2` | P4 1329–1928 | 329.979 | `sonda-colheita-P4-1329-1928.json.xz` |
| `7ecb551` | P4 1929–2528 | 377.142 | `sonda-colheita-P4-1929-2528.json.xz` |
| `f5c89bc` | P4 2529–3129 | 307.639 | `sonda-colheita-P4-2529-3129.json.xz` |
| `2e24188` | P5 129–728 | 334.501 | `sonda-colheita-P5-129-728.json.xz` |
| `8a35073` | P5 729–1328 | 286.287 | `sonda-colheita-P5-729-1328.json.xz` |
| `5593df2` | P5 1329–1928 | 320.071 | `sonda-colheita-P5-1329-1928.json.xz` |
| `7ecb551` | P5 1929–2528 | 317.009 | `sonda-colheita-P5-1929-2528.json.xz` |
| `f5c89bc` | P5 2529–3129 | 270.091 | `sonda-colheita-P5-2529-3129.json.xz` |

The ten P4/P5 native loops cover 6,002 frames in 3,195.133 seconds, maximum 377.142 seconds per loop, excluding xz
packaging. The complete K1 origin retry covers 61 frames in 87.765 seconds. Every native invocation uses the lease
and stays below 20 minutes; no Mac mini continuation is required. The fresh native 128-frame HUD regression plus
both renderer comparisons takes 525.101 seconds between lease grant/release, and passes 128/128 with all prior
1.4/1.5/1.7/1.8 phase hashes unchanged.

`validacao/origens-colheita-final.json`: **43/43** isolated calls, **35** unique added origins, **0** mismatches.
This includes the first K1 calls and each P4/P5 segment's exact opening state. The separately preserved first K1
attempt is diagnostic history, not counted again. No additional logic/CRT store is accepted; the existing AI flag
and EAX contract is checked explicitly. Current provider, data, comparison source and recording hashes are pinned.

`validacao/colheita-graficos-final.json` combines independent full probe replays only after verifying identical
source pins against current source bytes:

| Probe | Drawn frames | Full surfaces equal / total | First difference / stop |
|---|---|---:|---|
| K1 | 129–629 | 501 / 501 | None |
| P4 | 129–3129 | 3001 / 3001 | None |
| P5 | 129–3129 | 3001 / 3001 | None |

All 6,503 full 800×600 indexed surfaces, 346,644 raster calls and projected display effects match, with 2,646 strictly
attested AffText boundaries (all in P4). Active replay wall times excluding capture waits are 66.241s K1, 467.933s P4,
445.201s P5. The final P4 replay is paused during the macOS exclusive timing lease, then resumed under its own lease.
No native surface or cache is used to repair a Python output.

Default P4 rendering without a text provider stops at frame 484, `0x459454`, after 355 complete phases. K1/P5 have no
AffText calls in these windows. Glyph-enabled execution and unproved origins remain outside the evidence; the new
35 positions are still not proved for RestoreAll. Other builder work tasks and previous named stops remain.

Final leased `python3 -B scripts/check.py --domain graphics`: **267 tests, zero skips, PASS**, 143.534 seconds.
Log: `validacao/api19-graphics-tests-final.log`. Prior native matrices are replayed unchanged; the new comparisons
and full source-pinned reports run alongside them. No M3 acceptance or main integration is recorded by this front.
