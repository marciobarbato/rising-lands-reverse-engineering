# Scripted probe windows — render API 1.8 research

Source main is pinned to `ce441852bcada750a8f91da8ed3302f1668c4405`. The published 1.7 version is retained as history;
the coordinator confirmed that its dispatch version typo requires no renumbering. No main integration or acceptance
is authorized by this dispatch. Owned changes remain Graphics-only.

## Original-first case matrix

| Window | Required evidence | Native acquisition |
|---|---|---|
| P3 129–3129 | All construction stages, completion at 1812, finished uninhabited CAVE | Existing 129–300 evidence, then <=750-frame restored continuations |
| P6 2001–2400 | Sanctuary selection/release, colonist walk/order/lodging, inhabited CAVE from 2178 | Restore verified shared P3 frame-2000 state, run P6's original input |
| P7 2401–3700 | View movement, carrier work, Ctrl/depot order, delivery/credit at 3604 | Restore verified shared P6 frame-2400 state, run P7 in bounded chunks |
| K1 129–629 | Arrow-key scrolling and subsequent key states | Native input replay from accepted frame 128 |

Published whole-state hashes establish that P3/P6/P7 are identical at frame 2000, and P6/P7 at frame 2400. Every
restored opening checkpoint is checked against the destination probe, then both phase surfaces and the complete
end-frame state are checked at every frame. This is native continuation, not injection of reconstructed state.
The recorder has an 18-minute internal checkpoint budget; every native invocation uses the heavy lease.

`evidencias/janelas-api18-proveniencia.json` pins all four published probe directories and the intact-executable
intervals before translation. Executable SHA-256 is unchanged:
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
`capturar_janelas_graficas_m3.py` imports the pinned original-only capture helper and adds observation of
TextGetMessage entry and native accesses to `[0x5099A4..0x5099A7]`; it never reads that pointer to fabricate a message.

## Boundary contract

The display oracle declares TextGetMessage EAX 0, with its body not executed. A glyph path depending on an unavailable
pointer remains a named dependency. AffText is also a declared non-executed display boundary in the inherited bench;
the existing fixture-only adapter may verify that exact recorded boundary, never act as a default glyph renderer.
Actual observed boundary counts and pointer reads are recorded separately. The checked-in `fronteiras.jsonl.xz`
files at the pinned revision contain audio/CD boundary rows; no TextGetMessage row was found in P3/P6/P7/K1 during
initial inventory. This is recorded as an observation, not used to synthesize an unobserved text call.

## Portability

New sprite families, anchors, clock sources, masks and conditions will be expressed as explicit layer plans/tables.
The Python frame compositor consumes those plans; the engine workstream can port the data and arithmetic to the Rust
renderer without deriving IDs from image pixels or importing emulator code. Unsupported state remains an addressed stop.

## Native evidence ledger

All files below are under `evidencias/`, with `.manifest.json` siblings pinning compressed/raw SHA-256, executable,
producer sources, probe input/records, checkpoint and native code hash. The elapsed column excludes xz packaging.
Every invocation used the MacBook heavy lease; the longest replay was 434.390 seconds. Native windows total
2,781.405 seconds; the additional inhabited matrix took 73.026 seconds. The fresh native 128-frame HUD regression
took approximately 531 seconds including startup. No >20-minute native run or Mac mini continuation is required.

| Commit | Capture basename | Frames/cases | Native seconds |
|---|---|---:|---:|
| `38cd3ee` | `janelas-api18-proveniencia.json` | Four published probe directories and raw x86 intervals | — |
| `111ac04` | `janela-K1-129-629-api18.json.xz` | 501 | 192.038 |
| `6794493` | `janela-P3-301-1050-api18.json.xz` | 750 | 434.390 |
| `cbe2604` | `camadas-habitadas-api18.json.xz` | 515 | 73.026 |
| `fd019f5` | `janela-P3-1051-1800-api18.json.xz` | 750 | 430.282 |
| `7ad141d` | `janela-P6-2001-2400-api18.json.xz` | 400 | 226.544 |
| `7f157fc` | `janela-P3-1801-2550-api18.json.xz` | 750 | 432.971 |
| `4befc76` | `janela-P7-2401-2850-api18.json.xz` | 450 | 238.969 |
| `30ce7b7` | `janela-P3-2551-3129-api18.json.xz` | 579 | 350.310 |
| `ae13da0` | `janela-P7-2851-3275-api18.json.xz` | 425 | 224.757 |
| `e3ab05b` | `janela-P7-3276-3700-api18.json.xz` | 425 | 251.144 |
| `b9ec299` | `fronteira-texto-api18.json` | P7 frame 2851 return/body/read observation | One frame |

The inhabited leaf matrix is 512 combinations (16 variants × busy 0/1 × full 0/1 × 8 clock phases) and three selection
cases: sanctuary eight/seven troops, CAVE one resident. The original habitation routine must return true before
recording each inhabited facade. Unit IDs in structure slots begin at +0x12, paired with +0x4E slot codes.
This is a declared-write leaf domain; the full P6/P7 continuations separately prove natural entry and transitions.

P7 native recordings observe 287 TextGetMessage entries (81 in 2401–2850,206 in 2851–3275). The dedicated micro-probe
also observes its actual EAX 0 return and zero body instructions. No new display message pointer is supplied.
Every overlapping read begins at 0x5099A6, the packed cursor-coordinate load at 0x417CE2, rather than 0x5099A4.
All phase surfaces and complete end-frame state hashes remain equal with the observation hooks installed.

## Bounded reproduction

Use a fresh scratch directory for regeneration: checkpoint/output paths are never overwritten. The existing 1.7
producer's `--prepare` path regenerates the accepted frame 128; its P3 `--to 300` path regenerates frame 300. See
[the preceding capture instructions](M3_CAVE_RENDER.md#exact-mac-mini-continuation-commands). For this integrated
probe revision, use `capturar_janelas_graficas_m3.py` for subsequent continuations. The command template is:

```sh
python3 "/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py" graphics18-window -- \
  python3 -B pesquisas-paralelas/graficos-animacao/capturar_janelas_graficas_m3.py \
  --start .local/graficos-api17-start --resume .local/graficos-api17-start/P3-00300.pickle \
  --probe P3 --to 1050 \
  --output .local/graficos-api17-start/recaptured-P3-301-1050.json.xz
```

Apply these rows sequentially, using distinct output names. A dash means omit `--resume` and restore accepted frame 128.
The optional `--checkpoint 2000` on the third P3 continuation is required for P6/P7 prefix reuse.

| Probe | Resume checkpoint | Target | Additional checkpoint |
|---|---|---:|---:|
| K1 | — | 629 | — |
| P3 | P3-00300.pickle | 1050 | — |
| P3 | P3-01050.pickle | 1800 | — |
| P3 | P3-01800.pickle | 2550 | 2000 |
| P3 | P3-02550.pickle | 3129 | — |
| P6 | P3-02000.pickle | 2400 | — |
| P7 | P6-02400.pickle | 2850 | — |
| P7 | P7-02850.pickle | 3275 | — |
| P7 | P7-03275.pickle | 3700 | — |

The inhabited matrix producer takes `--start`, `--snapshot` (native P3 frame 220), and `--output`; run it under a
separate lease. `capturar_fronteira_texto18.py` takes the same arguments with the native P7 frame 2850 snapshot.
No single native command is expected to replay a multi-thousand-frame window. A budget stop must be resumed from
its actual saved checkpoint, and never relabelled as a complete capture.

The pure-Python comparison reuses all committed recordings and requires no executable execution:

```sh
python3 -B pesquisas-paralelas/graficos-animacao/validar_janelas_api18.py \
  --probe P3 --probe P6 --probe P7 --probe K1 \
  --output pesquisas-paralelas/graficos-animacao/validacao/janelas-api18-final.json
python3 -B pesquisas-paralelas/graficos-animacao/validar_camadas_api18.py
```

The chained renderer receives only its own preceding pixels/cache/background. Each native entry is checked before
the next call; no native pixel repair is applied. Full 480,000-byte surfaces, all raster arguments and projected
DGROUP effects are compared. The two established DirectDraw binding-pointer exclusions apply only to effects.
All frame-phase surface hashes equal the preceding between-frame hash, so each frame contributes one drawn phase.

## Results and remaining evidence

`validacao/janelas-api18-final.json`: P3 **3001/3001** (129–3129), P6 **2272/2272** (129–2400), P7 **3572/3572**
(129–3700), K1 **501/501** (129–629). No differing frame or stop occurs under the declared recorded AffText boundary.
All pixels, raster arguments and exported display effects match. The replay took 769.391 seconds and checks 5,202
unique render entries/9,346 expanded phase rows, including 1,030,208 drawing calls and 7,865 attested text boundaries.
The final source hashes are part of the report; earlier exploration reports are not substituted for this proof.

Without the explicit recorded-boundary adapter, P3/P6/P7 first stop at frame 141, `0x459454`, after 12 complete phases;
K1 has no missing text. `validacao/camadas-api18.json` reports 515/515 native leaf cases, zero mismatches.
The fresh leased 128-frame `--hud` regression reports 128/128 and direct equality to all 1.4/1.5/1.7 surface hashes.
P3 completion changes logic at 1812 and pixels at 1813; P6 lodging changes owner at 2178 and pixels at 2179. P7 credit
lands in frame 3604; the HUD flash follows, and the second displayed counter becomes 21 at between_frames(3606).

The complete requested windows are captured and compared on the MacBook in bounded jobs; no Mac mini job remains.
Unexecuted glyph paths still need a text-enabled native oracle capture. P4/P5, unknown CAVE owners/levels/fire,
additional new bag configurations, other unit effects/tasks/experience and prior unrelated named stops remain outside
this 1.8 evidence domain. Every original capture was committed before the delivered translation.

Final leased gate: `python3 -B scripts/check.py --domain graphics` passes **261 tests, zero skips**, in 131.111 seconds.
Log: `validacao/api18-graphics-tests-final.log`. All prior graphics suites run alongside the new six tests.
Historical native matrices are replayed unchanged; they are not recaptured. Documentation links and the flat import
namespace check pass. No main integration or M3 acceptance is performed by this front.
