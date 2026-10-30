# Local macOS playable consumer

`compilar-jogável` builds **RisingLands-ptbr.app** for this Apple Silicon Mac.
The existing Swift/AppKit/WebKit shell and JSON-lines Python engine are reused.
The new exercise consumes current committed core, combat, economy and graphics
providers from one revision. It is a bounded interactive reconstruction, not a
complete original mission or campaign.

## Build and run

From the repository, run:

```sh
export RISING_PYTHON_RUNTIME=/absolute/path/to/relocatable-python-3.12-arm64
./compilar-jogável --inputs-root /absolute/path/to/inputs
open .local/macos-playable/dist/RisingLands-ptbr.app
```

From the workspace, use `./engenharia-reversa/compilar-jogável`. The normal build
fetches `origin/main`, resolves it once to a commit, and uses only that commit's
Git archive, including the app sources and build implementation. Uncommitted
files and other worktrees are never runtime inputs. Fetch failure stops the
build. `--offline` explicitly permits the already fetched `origin/main` object.

Before feature integration, a separate check is available:

```sh
./compilar-jogável --development-ref HEAD
```

It requires a committed revision and writes under `dist/development/`, preserving
the normal delivery. The build prints the absolute bundle path. Generated
sources, assets, runtime, compiler caches, logs and prior bundles remain under
clone-local `.local/macos-playable/`, outside tracked research folders.
Existing preview distributions and historical manifests are untouched.

Prerequisites: macOS 13+ on ARM64, Apple Swift command-line tools, Git, Python
3.9+ for the launcher, the existing extracted Brazilian CD at workspace
`source/cd`, and the existing relocatable CPython 3.12 runtime under
`local-data/macos-preview/dependencies/python`. `RISING_PYTHON_RUNTIME` may select
another compatible existing runtime. No download, Rosetta, Unicorn, system
package installation, notarization or external distribution is performed.

## Player controls and supported exercise

The app opens **Treino livre** paused. Select a friendly unit on the map or in
the left list, click an empty destination, then press **Continuar** (Space).
The destination form also issues movement orders. Drag pans, the wheel zooms,
`.` advances one update, and `R` resets. Speed controls the exercise clock.

* Move the constructor to the yellow supply cell `(4, 9)` and press **Coletar
  sacola**. Move to the cyan depot `(2, 12)` and press **Depositar carga**.
  The supply shrinks and the shared food balance increases on deposit.
* Move the soldier around the wall to `(9, 4)`. Press **Atacar adversário**
  (or right-click the adjacent adversary with the soldier selected), then
  continue. Facing, attack frames, recharge and repeated direct unit damage
  advance on the live clock. A move order interrupts attack.
* The final lethal hit pauses at the explicit missing death continuation.
  Earlier nonlethal damage remains visible; reset starts a new exercise.
* Existing obstacle/wall/free movement labs, manual resource operations and
  targeting queries remain accessible. Mission 1 shows original ETA terrain
  and positions in inspection mode, with simulation controls disabled.

All player-visible text remains Brazilian Portuguese. No replacement audio is
introduced; the original audio files are unchanged, and audio playback is not
integrated in this consumer.

## Provider and input contracts

The 16×16 exercise, wall, initial units, eight food units, one-item exercise
cargo, depot location, objective and 20-update/second clock are **synthetic app
policy**. They are not recovered transport, AI, mission or dispatch rules.
The WebView requests an update every 100 ms; the exercise engine uses monotonic
elapsed time ×20×speed, so coalesced background timers still advance the live
clock. A single response catches up at most one second (160 updates at 8×);
pause/play and speed changes reset the time anchor, preventing an unbounded
sleep/wake replay. Rendering follows current responses. Historical movement
labs retain their explicit 2×speed update quantum. Neither mode reconstructs
the original global timing loop.

| Area | Actual provider and supported inputs | Deliberate boundary |
|---|---|---|
| World | `MundoNavegacao`/`SolucionadorCaminhosPython`, 800×276 writable bytes, 256-stride cells, prepared region/occupancy arrays; three active units on a 16×16 synthetic map | No full ETA world loader or global dispatcher |
| Unit setup | `definir_tipo`, loaded 26×50 original type records, `BonusUnidades` with explicitly zero 1,872-byte fixture state, `capacidade_tipo`; inactive handles and null AI groups | No claim that original mission initialization ran |
| Orders | Committed movement/reset APIs; `ordem_ja_definida` before reset then `ordem_apos_reset` for a stationary, adjacent type-0 attacker, unit-target mode 1 | Pursuit callback is not supplied; out-of-range attacks are rejected before mutation |
| Attack | `ContextoAtaque`/`calcular_ataque`, original type recharge and animation parameters, `avancar_recarga` once per exercise update | No invented phase-2/3 producer, projectiles, magic, full combat dispatch or attack-body artwork |
| Direct damage | `encontrar_vitima_impacto` then `ConsumidorDanoUnidade.infligir`, mode 1; original 26 damage rows and explicitly zero proximity-bonus global `bonus_4965ac`; `ConsultaBonusCombate` and live packed region-grid `ConsultaProximidadeAtaque` | Intentionally excludes `InfligeDegat` reaction/diplomacy/presentation wrapper; default `LimiteMorte` stops before life-zero/death effects |
| Message callback | Only the non-AI-control or null-group no-effect guard is accepted; all other branches raise | No general AI message provider or new native differential claim |
| Audio visibility | Observer camera 3 remains hidden (`descoberto[3][cell] & 31 != 0`); the exercise UI observes the prepared scene independently | Volume/sound callbacks remain unsupported; they raise if reached |
| Economy | `RecursosTerreno.retirar_sacola` and `EconomiaConstrucoes.adicionar` mutate shared supply/balances; exercise cargo is separate UI state | No reconstructed transport caller, automatic harvesting, production completion or spawned units |
| Graphics | `graficos.Catalogo/consultar/rgba`, current original palette and explicit opacity, generated cached body frames for 0/7/9, owner 0, states 2/7, direction 1–16, raw frame 0–7, bag variant 0/1 | Other owners/states/types use labeled markers. No shadow remap, complete indexed scene ordering, lighting cycle or complete game frame |

Missing callbacks raise at their boundary; partial effects remain visible and
are not retried as though they were a continuation. The exercise locks further
actions after its death boundary. Production's partial preparation/conversion/
recovery providers are available in the source revision but are not exposed as
successful recruitment. Save/load, original event scripts, campaigns, audio,
visible death, general structure actions and full-game fidelity remain open.

## Provenance and validation

`Contents/Resources/preview/snapshot.json` records the immutable commit/tree,
requested ref, main/development mode, per-file SHA-256 and last path-changing
feature commits. `assets/fontes.json` binds generated media to the same source
revision and verified original CD hashes. `Info.plist` repeats the revision and
display name. `dist/build-manifest.json` records actual output hashes, logs and
whether the native smoke ran. Prior bundles are preserved under `previous/`.

Every build runs the app-owned consumer suite, verifies every archived source
file and mirrored app source, generated asset hashes, ARM64 executables, local
ad hoc signature, bundled isolated Python imports and a real navigation loop.
It then opens the actual AppKit/WKWebView app and exercises DOM selection,
destination submission, play/pause/speed, movement around the wall, collection,
deposit and two live-clock hits. `native-smoke.json` records the interaction,
positions, health, revision and changed native PNG hashes; `native-smoke.png`
captures the rendered window; paired `.before.png`/`.after.png` files preserve the visual interaction evidence without reading a tainted file-URL canvas. `--skip-ui-smoke` is explicitly an incomplete
headless check and records that fact.

Initial implementation baseline: `5e2bf0831d3aaa776481a6ab023be262ef0df1bd`.
Actual validation results and integration identity are recorded in the
[app handoff](../apps/macos-preview/HANDOFF.md). Historical x86 totals are not
substitutes for these consumer/runtime checks. This app adds no recovered
native algorithm and does not aggregate domain totals into a game-fidelity claim.

## Independent M3 preparation boundary

The original preparation added an app-owned read-only M1 inspector with a
pending-M2 update boundary. That evidence interface remains immutable; the
[current contract](../apps/macos-preview/M3_CONTRACT.md) separately defines M2.2 playback and live Rust execution.
It loads the exact acceptance-pinned evidence with the existing Python block
decoder. It does not switch the native app to MONDE01 or establish M3 acceptance.
The [independent audit](../apps/macos-preview/M3_AUDIT.md) records isolation and
provider dependencies.


## Independent accepted-evidence playback (contract v6)

The app offers **Inspeção M2.2 · evidência aceita** separately from the synthetic
training exercise. It loads the accepted display-v2 MissionLoad state and all
257 phases / 11 checkpoints using committed Missions/runtime readers. Choose a
phase or frame, inspect original-address memory/observed words, or reset. This
is read-only playback, not a running Python mission or M3 acceptance. M1
original-v2 inspection remains a separately labeled API.

The shell pins Graphics API **1.5** and calls it with `hud=True`. HUD and
captured cursor are included within the published domain. Every required region
is checked against captured memory before rendering, including the minimap and
player table. Other versions are refused until explicitly reviewed and tested.
All rendering continues to come exclusively from Graphics.

All 128 drawing phases are checked against the pinned 1.5 full 800×600 native
phase-end reference before publication. Undrawn phases preserve the same
verified surface. Generic named HUD/body stops remain visible outside the
provider's supported domain. The palette is static; palette cycling is not
applied. Memory playback verifies 257 phases and 11 checkpoints. The inspector
uses phase/frame navigation, original-address reads, filter and reset, without
live orders. See the [v6 contract](../apps/macos-preview/M3_CONTRACT.md) and
[handoff](../apps/macos-preview/HANDOFF.md) for exact evidence and test results.

The full asset pack is being published in the separate rising-lands-assets
repository. This app update continues to use an explicit read-only CD inputs
root and does not add that pack or its commits to the code repository.

## Bounded native smoke readiness

The shell waits for an explicit, source-commit/mode-validated readiness message
from the UI after its worker and assets finish loading. Merely showing a window
or finishing document navigation is not readiness. The original interaction
assertions and per-action waits remain unchanged.

Monotonic budgets are separate: window visibility within 45 seconds;
initialization/readiness within 90 seconds total from launch (including the
window); then at most 45 seconds for checks. Progress does not reset any budget.
A before snapshot must finish before checks begin. A final screenshot has a
10-second exit guard; LaunchServices has a 165-second outer process guard
(90 + 45 + 10 + 20 launch allowance). This does not turn an unready window into
success or extend the 45-second check budget.

Failure JSON includes phase, document/window/ready signals, elapsed times,
readiness payload and Python stderr. It is written before screenshots, so a
stuck WebView cannot erase the reason. Both UI smokes preserve paired before/
after images plus the final snapshot; missing captures fail the delivery.
Retries archive prior JSON, images and process logs under `previous-smoke/`.
An outer-process failure preserves any more specific app failure JSON.

`--smoke-ready-delay-ms 50000` is a smoke-only diagnostic: it holds the readiness
signal after real initialization to reproduce a slow startup without inventing
worker/asset success or generating CPU load. It is ignored outside smoke mode
and bounded to 0..80000 ms. Native state-machine tests exercise missing ready,
late window, out-of-order document/ready events and an unchanged check deadline.
Graphics stays pinned to its explicitly accepted 1.5 contract; other versions
still fail. That robustness delivery preserved the inspection boundary. Current live no-input work follows the published M3 plan and is described below.

An occluded WebView can report a hidden document while its native window is
visible. Native smoke repaint barriers therefore wait for a completed WebView
snapshot through the existing 15-second request deadline, rather than waiting
for animation callbacks that WebKit suspends while hidden. This preserves
paint verification and every interaction assertion. Timeout JSON also records
the last assertion/stage and game/visibility diagnostics.


The 2026-10-29 architecture decision targets a Rust engine/render library with
a C ABI called by Swift. Python stays as the validated reference and current
inspection/playback runtime; whether it ships later remains undecided. Live logic and rendering now use Rust ABI 1.4 with native Metal presentation. See the live session below.


## Live no-input Rust session and input recording

Open the inspection page and select **Abrir Rust ao vivo**. The app opens a
native **Rust e Metal** window. **Executar**, **Pausar**, **Avançar quadro** and
**Reiniciar** control one serial ABI 1.4 world and renderer, initialized from
accepted display-v2 S0 and original static tables. The native driver renders
at the exact phase-1/3 generation before phase 2. Phase 2 alone applies display
logic effects. Swift uploads original indexed pixels and RGB palette to
reusable Metal resources and presents every completed frame. Python supplies
only evidence inspection, asset/input preparation and proof oracles.

The live driver checks all 257 M2.2 masked state hashes and 11 checkpoints,
plus original full-surface hashes through frame 9200. The full 18,401-state
M2.3 audit uses the same stepping/render path in proof mode. Beyond the pinned
window, surface verification is explicitly unavailable; execution continues
to its first named engine/render stop. The driver latches the reason without
replaying captured frames or inventing state. Reset creates valid replacement
handles before releasing the previous world/renderer. Original-address reads
are explicit diagnostics. The normal native no-input scenario injects no
human orders. The prior recorder/export scaffolding remains an independent
inspection feature; native gameplay input/orders are not implemented here.

The Swift executable statically links the unchanged Rust C ABI and app driver,
so existing hardened ad-hoc signing remains enabled without a library-validation
exception. The shared library remains available to proof tooling and is hash-
recorded separately. The builder compiles integrated `motor/` into its ignored
target from the same immutable Git archive as the app. The app requires ABI
**1.4** and checks `rl_render_contrato()==0x00010007` (Rust Graphics **1.7**)
before creating the renderer. The temporary external-engine override has been
retired; a set `RISING_MACOS_ENGINE_SOURCE` fails explicitly. Builds use main's
integrated `motor/`, with no implicit library or source fallback.

Python evidence inspection explicitly accepts Graphics **1.8** and pins its
native 128-frame HUD report SHA-256
`613ec2348b7fe0d597690ca4601af7f825c0d227133cdddc6b10e822e8eee845`.
The predecessor 1.7 and current 1.8 hashes match for all 128 no-input frames.
The existing habitation reader consumes the actual CAVE bag as well as the
sanctuary. No new callback or external region is required by Graphics 1.8.
Rust exposes its separately published Graphics **1.7** domain. Saved-background
and text-boundary exports are additive in ABI 1.4; glyphs retain their named
stop and no text substitution is installed. Native orders, continuous drag
recording and later Graphics 1.8 worker/lodging branches remain outside this
no-input live session. The UI remains Brazilian Portuguese.

## Renderer port input

This input spec is implemented by engine **ABI 1.4** and consumed by the native app.
The original requested interface follows for traceability. The app needs no
Python projection or PNG work per displayed frame. At 25 fps the frame budget
is 40 ms: target at most 12 ms logic, 22 ms rendering, 4 ms transfer/presentation
and 2 ms headroom on the declared Apple Silicon host. Measure the whole
fixed-step pipeline; these are budgets for implementation, not achieved rates.

Original requested call shape (the published ABI header defines final layouts):

```c
rl_render_criar(world, assets, initial_surface, initial_cache, &renderer);
rl_render_quadro(renderer, expected_generation, hud_flags,
                 indexed_buffer, indexed_capacity,
                 palette_rgb24, palette_capacity, &result);
rl_render_reset(renderer, initial_surface, initial_cache);
rl_render_liberar(renderer);
```

- `assets` names the bundled, hash-checked Graphics catalog/banks. Parse and
  retain them once. Creation copies/owns accepted input bytes; caller input
  storage can be released afterward. The M2.2 proof supplies the pinned original
  480,000-byte initial surface and terrain cache, never an invented blank/cold
  start. Other initialization states need their own established contract.
- Bind the renderer to one world and require the **AffGame-entry generation**
  immediately after load_tail or the preceding CalculGame body. Render that
  state before the next between_frames mutation. A generation must distinguish
  phases as well as ticks. Serialize world/render/reset/free calls. Return the
  exact generation and frame counter; reject stale/mismatched generations.
- Input `hud_flags=1` explicitly requests Graphics 1.5 HUD/cursor composition;
  zero retains its published pre-HUD behavior. Preserve draw/callback order,
  signed clipping, 16/32-bit arithmetic, indexed pixels and cache cursor/payloads.
  Query habitation from the actual world, without a host callback or default.
- Caller owns/reuses the two output buffers. A successful call copies a coherent
  **800×600, top-down, indexed8 surface, stride 800**, and **256 RGB24 entries,
  768 bytes**, as one result. Alpha is opaque for presentation. No Rust pointer
  escapes; no per-frame allocation or filesystem access is required by the
  caller. Size-query/BufferTooSmall returns required capacities without changing
  buffers or advancing the render cache. Reset/free lifetimes are explicit.
- `result` reports full / undrawn / partial, ABI status, generation, width,
  height, stride, palette generation, cache generation and optional first stop
  (original address, callee and UTF-8 reason). An undrawn phase preserves the
  preceding surface/cache. Partial output is the actual drawn prefix with its
  named stop; it must never masquerade as a complete frame. ABI errors publish
  neither an output frame nor a cache update. Palette changes are explicit;
  static palette equality must remain while Cyclage is unsupported.
- Display effects already modeled by ABI 1.1 phase 2 must have **one owner**.
  A read-only render call must not apply those RNG/counter/target effects twice.
  Export their ordered observations for diagnostic comparison. Define the
  composition boundary with the engine owner before moving effect ownership.
- Keep full `rl_projetar_tudo` as an optional proof/debug path. ABI 1.1 has no
  region selector: it always copies the complete world. If Python Graphics
  remains during migration, add a copied, generation-checked
  `rl_projetar_regioes(world, requests[], buffers[], &generation)` for precisely
  `regioes_necessarias(..., hud=True)`. A direct native render should read world
  state internally and need neither bulk nor selective host snapshots.

Acceptance inputs are the existing Graphics 1.5 native leaf matrix and the
128-frame chained full-surface/cache proof, plus 257 masked states and 11
checkpoints from the no-input world. Test the actual Swift output-buffer path,
wrong sizes/generations, resets, named stops and palette changes. Swift should
upload indexed pixels plus palette to a reusable Metal texture/shader (or a
native RGBA surface), scaling only at presentation. PNG remains an explicit
evidence export. The native live window now uses Rust indexed buffers and Metal. The indexed
WebKit canvas and Python renderer remain diagnostic/evidence tools only.

### Integrated ABI 1.4 validation

APP_BUILD at `e760756c44f79950cedc146ac17654b19c2d18c0`, after merging main
`ef52cb0`, builds the integrated engine without an override. The exact
`scripts/workstream.py` APP_BUILD command passes 109 consumer tests, 27 native
exercise checks and 20 inspection/live checks. `sh motor/validate.sh` passes
with its commit-pinned references: 28 Rust tests, 61 Python tests plus the
10 renderer child tests, 75 original-x86 comparisons and both Swift smokes.
The engine gate uses a debug library; the application ships a release library.

The bundled live path equals **257/257 states, 11/11 checkpoints and 128/128
full surfaces**, including Python 1.8 surface/palette/cache/effect comparisons.
Test A retains **155,597/155,597 answers** and all six canonical byte round
trips. The real visible native UI measures **41.386 fps**, 401 frames in 9.689 s,
including startup proofs and Metal presentation. Its GPU readback checks all
1,920,000 displayed pixels; the UI smoke verifies all 406 reached surfaces.
Common checks pass 1,976 tests with 620 optional skips. See the
[delivery evidence](../apps/macos-preview/validation/m3-abi14-delivery.json).

The ABI 1.4 9,200-frame horizon was not rerun in this adoption; the previous
ABI 1.3 horizon below is historical. Orders, Test A's game-state half, Test B,
continuous human drags and glyph rendering remain separate dependencies.

### Historical ABI 1.3 application measurements

Development build `869ffaa22db49105c39c31444790b4648551a886` uses the approved
ABI 1.3 engine source `363faa9c252ffb00d62c81db0da2ee5d4a3d7615`. The real
visible Swift/Metal window measures **40.914 fps** over 406 frames in 9.923 s,
including the required 257-state startup audit and all reached surface checks.
The previous Python/raw-canvas application measured 8.470 fps; its separate
worker-only rate was 9.898 fps. These are shared-machine measurements, not an
exclusive benchmark or a comparison of identical frame counts.

| Component | Native UI milliseconds/frame |
| --- | ---: |
| Rust logic | 11.042 |
| Rust renderer, including generation query | 4.451 |
| State export/hash and surface proofs | 8.000 |
| Metal upload, presentation and GPU completion | 0.921 |
| Loop/notification overhead | 0.027 |
| Total | 24.441 |

Host projection is confined to proof/debug reads. Python rendering, per-frame
pixel JSON, PNG encoding and Python IPC are absent from native live drawing.
The native smoke also reads back all 1,920,000 actual displayed GPU pixels and
compares each against the indexed output and palette. PNG export runs only
after pausing, outside the rate measurement. The
[handoff](../apps/macos-preview/HANDOFF.md#rust-renderer-integration--abi-13)
records complete-window proofs, the first engine stop and build provenance.

## Frame input recording and Test A answers

After the native session completes frame128, choose **Nova gravação** in the
inspection page or native game window. **● Gravando entrada** is visible while
recording. The native view captures mouse events and the declared keys; macOS
Control maps to Windows Ctrl, Option to Alt. The next game-frame poll receives
each event's frame stamp. Wall-clock timestamps never enter the script.
**Parar gravação** ends capture; **Exportar entrada** writes a file accepted
unchanged by Missions' scripted-input harness. The save panel preserves the
canonical bytes. A new recording replaces the preceding recording explicitly.

Clicks use the declared k/k+1/k+3 cadence and hold the cursor through release.
Ctrl remains held per frame until release/focus loss, supporting recorded depot
mode. Moves during a click wait until its end; this first half does not record
continuous drags. Reset is disabled while recording. Orders remain unavailable
and no recorded answer enters the Rust world. Record/export failures are visible
and block exporting an incomplete session as success.

The [input contract](../apps/macos-preview/M3_CONTRACT.md#m33-test-a--frame-input-interchange-and-answer-stream)
describes `ScriptedInput`, `FrameAnswerMapper` and `MacOSSessionRecorder`.
The [Test A answer report](../apps/macos-preview/validation/m3-test-a-answers.json)
compares every declared answer against P1/P2/P3/P6/P7/K1, using the native logs
only as poll requests. All **155,597 answers** match, with no first difference;
all six export/import/export byte round trips match. Native WndProc flag stores
and whole-state hashes belong to Test A's deferred state half. It requires
engine order support. The 3,000-frame human original replay (Test B) is also
pending; no M3 acceptance is claimed.

## Native play mode and independent clocks

The native window defaults to **Jogar**. **Validar** resets to the accepted S0
and retains the original audited frame driver: 257 prefix states, 11 checkpoints
and every reached reference surface. APP_BUILD's native smoke explicitly selects
Validar. The proof tools still default to validation, including observer callbacks.
Switching modes resets the world; it cannot disable validation halfway through a
proof. Memory inspection is available only in Validar. Jogar applies orders through
the ABI 1.6 input path after frame 128; the recorder observes the same events.

Jogar calls the same Rust phase1/render/phase2/phase3 sequence, with no projection,
state/surface hashing, equality counters or observer callbacks. Contract checks,
partial render results and named engine stops remain active. ABI 1.6 play policy 1
is selected after loading S0 and before phase 1. Validar retains policy 0; input
proofs may explicitly use persistent audited policy 2 to retain poll records.
Game speed selects 15, 20, 30, 60 game frames/s or unlimited. The default now
follows the original's **uncapped active idle-loop policy**. This is a scheduling
policy match; historical hardware elapsed speed is not established. The static
pacing audit below replaces the earlier assumption that nominal TickClock 20
was an original host-frame limit. Host scheduling never changes the engine's virtual clock,
frame arithmetic, frame-indexed recording or order. Slow frames catch up without
skipping simulation steps; pause and resume reset the host deadline.

Engine work and initialization run on a serial worker. A separate display queue
presents the latest complete indexed frame at up to 120 Hz, with no interpolation.
A 20 Hz game frame can therefore be displayed several times; display fps and
completed game frames/s are reported separately. Three persistent shared Metal
textures and palette buffers prevent CPU writes from racing GPU readers. The
producer copies directly from the Rust caller buffer to a free texture slot;
there is no Swift pixel array, PNG, RGBA conversion or allocation of new pixel
storage per frame. GPU completion releases slots asynchronously. The display
queue owns drawable acquisition and command submission; steady play has no
main-thread synchronization or GPU wait. Pause/reset/evidence capture drain the
queue. Validation keeps its synchronous presentation/readback checks.

For an actual visible-window measurement of at least 60 seconds, run the owned
`apps/macos-preview/scripts/benchmark_native_macos.py` through the exclusive heavy
lease, specifying `--app`, a new `--output`, `--mode play|test`, `--seconds 65`
and `--game-fps 20|60|0`. The app counts actual CAMetalDrawable presentation
timestamps, emits complete one-second bins and their minimum, and separates Rust
logic, rendering, proof, upload, submission and GPU timings. Each run ends with
GPU readback against the latest real Rust surface. It never claims repeated
presentations are distinct simulated frames. See the sustained measurements below.

### Sustained play measurements

Validated implementation/build **55cddc571ec75bf6b305aabd75c33d5697fa7471**,
based on main **8138e6e**. All four runs used the actual unoccluded native window
on this MacBook's 120 Hz screen for at least **65 seconds**, under an exclusive
heavy lease. Actual presentation timestamps include the first second; none of the
startup or slow bins below is removed. Each final readback matches all **1,920,000
pixels**. Play readbacks use the asynchronous slot texture/upload/shader path.

| Mode | Game frames/s, observed | Display fps, average | Display fps, minimum full 1 s |
|---|---:|---:|---:|
| Jogar, nominal 20 | 20.010 | 119.920 | 117 |
| Jogar, requested 60 | 60.001 | 119.878 | 117 |
| Jogar, unlimited | 69.226 | 119.919 | 117 |
| Validar, unlimited | 63.241 | 63.210 | 25 |

Evidence: [nominal play](../apps/macos-preview/validation/m3-play-play20.json),
[60 game frames/s](../apps/macos-preview/validation/m3-play-play60.json),
[uncapped play](../apps/macos-preview/validation/m3-play-play-unlimited.json),
[validation](../apps/macos-preview/validation/m3-play-test.json).
The minimum play display rate is 95% above 60 Hz; uncapped average game throughput
is about 15% above 60 game frames/s **in this no-input window**. Displaying an
unchanged game frame several times is deliberate; these are actual presentations,
not interpolated or invented simulation states. All play runs have zero proof
seconds, equality counts and publication drops. Main-thread 50 ms timer maximum
excess delay is 1.92, 1.98 and 1.94 ms respectively.

The previous **41.386 fps** number was a roughly 10-second audited run including
the expensive 257-state startup prefix. The same short APP_BUILD smoke now gives
**44.252 displayed / 44.362 game fps**, still with startup proofs. The 65-second
Validar run retains those proofs: the first five one-second bins are
**25, 27, 25, 26, 26**, then 63–70 presentations/s. Its **257 states, 11 checkpoints
and all 4,117 reached full surfaces** equal the accepted evidence. The sustained
average must not be interpreted as removal of test-mode proof costs.

| Stage | Nominal play | Play at 60 | Uncapped play |
|---|---:|---:|---:|
| Rust frame logic, ms/game frame | 10.659 | 10.426 | 10.313 |
| Rust rendering, ms/game frame | 4.360 | 4.201 | 4.059 |
| Texture upload, ms/game frame | 0.061 | 0.058 | 0.059 |
| CPU command encoding, ms/display | 0.022 | 0.030 | 0.030 |
| GPU draw, ms/display | 0.132 | 0.176 | 0.141 |

Asynchronous stages overlap; their totals cannot be added to wall time. Drawable
wait is reported separately from CPU encoding. Rust logic is about 72% of the
uncapped logic+render cost; app upload and encoding are small. This instrumentation
measures whole engine calls, not individual Rust routines. Repeated state loading
in `frame_state.rs` / `frame_runtime_state.rs` remains a candidate for the engine
owner to profile; no per-routine reload timing or engine optimization is claimed.
The current backend still provides only modest game-throughput headroom beyond
60, so broader/raid workloads need engine-side measurement and optimization.

Fresh [prefix proof](../apps/macos-preview/validation/m3-play-live-prefix.json):
**257/257 states, 11/11 checkpoints, 128/128 original surfaces and 128/128 Python
oracle surfaces**, zero observer failures. Fresh [Test A answer proof](../apps/macos-preview/validation/m3-play-test-a-answers.json):
**155,597/155,597**, all six canonical byte round trips equal. APP_BUILD passes
**110 consumer tests, 27 native exercise checks and 20 inspection/live checks**;
`sh motor/validate.sh` passes unchanged. Engine/order support, the original timing
probe and the state-hash half of Test A remain dependencies. No 9,200-frame
performance/first-stop horizon was rerun for this change.

[Common checks](../apps/macos-preview/validation/m3-play-common.log.gz) pass from
this feature worktree with `/usr/bin/python3 -B scripts/check.py` and `.local/python`:
**1,976 tests, 620 optional skips, zero failures/errors**. The
[delivery manifest](../apps/macos-preview/validation/m3-play-delivery.json) pins
all evidence and the tested static/shared libraries. Final evidence/documentation
commits do not change the validated executable source.

## ABI 1.5 live orders

The native Jogar window applies mouse/keyboard input after its 128 real startup
frames. Select a unit, then click its target; clicks are declared as move/down/up
at k/k+1/k+3. Ctrl remains held until release or focus loss, including depot-mode
selection. Engine-supported construction/recruitment/help-page controls now reach
the same input/order path. Unsupported engine or renderer branches stop visibly
with the original name/address and actual partial surface. Rust Graphics remains
1.7; Python inspection/oracles now pin Graphics1.9. No glyph or audio substitute
is installed. Text/sound non-execution boundaries are explicitly declared as in
Missions' probe contract. Validar retains the no-input equality proofs.

The current engine completes P1/P2's order scenarios, but its CAVE body still
stops at frame220 in P3/P6/P7, and K1 at frame141. Those are simulation bounds;
Rust's independently bounded renderer may stop earlier on an input-time text or
panel state. The app does not hide that limit. Recording still exports the owner
schema unchanged; a recording begun after earlier unrecorded orders does not
establish a full-session replay from frame128. Test B remains pending.

### ABI1.5 orders-on performance and renderer boundary

Executable/build **04dea3927ab4b9846f60a3d9a86c0b72cd2b59a0**, based on main
**2eadf69**, passes APP_BUILD with **112 consumer tests, 27 native exercise
checks and 20 inspection/live checks**. `motor/validate.sh` passes unchanged.
The native recorder check explicitly exercises Ctrl received with a mouse event
before a flags-change event; normal play sends those same key/mouse declarations
to the engine. The UI now states the actual per-mode order policy.

The [65-second default-rate orders run](../apps/macos-preview/validation/m3-input-orders20.json)
uses actual AppKit selection/movement clicks. It records real engine
`SetPlayerOrdre` tags **1 and 5**, then moves the pointer to empty ground before
the known tooltip dwell boundary. With **20.010 game frames/s**, the visible,
unoccluded UI delivers **118.752 displayed fps average / 111 minimum full-second
fps**, zero proof work and zero publication drops. All **1,920,000** final GPU
readback pixels match the actual Rust indexed buffer through the asynchronous
texture/upload path. No warmup bin is discarded. Input is active for 1,173 of the
1,301 completed game frames after the protected 128-frame prefix.

The [accelerated 60-game-frames/s attempt](../apps/macos-preview/validation/m3-input-orders60.json)
issues the same real orders but stops at **frame2,952**, with the named Rust
renderer dependency **AffInfoSelection 0x410be4**:
`fatigue words outside captured +4 = +0x76 = 4`. Its result is explicitly **failed**;
the paused tail is not a sustained performance success. No fatigue value, surface
or callback is substituted to pass it. The uncapped orders variant was not run
because this new bounded-domain stop already prevents a comparable full window.
This limits broader/faster play even though default-rate UI throughput exceeds
60 fps. The separate engine workstream must extend the renderer's fatigue domain.

Production Rust also retains the **AffText 0x459454** glyph dependency. The
owner's longer Graphics1.7 probe proofs use an original attested text boundary
available only to offline fixtures; the production ABI cannot install it. The
app never uses that fixture switch. Therefore build/recruitment/help dispatch is
wired, while complete visual/simulation continuation still depends on the
engine's CAVE body, viewport domain and renderer/glyph ports. Test A state proofs
omit rendering explicitly and do not claim those UI surfaces are complete.

Fresh no-input proofs retain **257 states / 11 checkpoints / 128 original and
Python1.9 surfaces**, plus **18,401 states / 9,200 original surfaces** over the
long chain. The answer-stream proof remains **155,597/155,597**, with all six
canonical round trips equal. See the [handoff](../apps/macos-preview/HANDOFF.md)
for source/library provenance, rejected build attempts and gate counts.

### Test A state results

All first differences are null. Counts below cover reached original frames;
P1/P2/P6 also have independently pinned whole-state windows.

| Probe | Frame hashes equal | Whole-state phases equal | First engine stop |
|---|---:|---:|---|
| P1 | 501/501 | 1,002/1,002 | None |
| P2 | 601/601 | 1,202/1,202 | None |
| P3 | 91/91 | Not available in this proof | Frame220, CAVE body `0x426aff` |
| P6 | 91/91 | 183/183 reached | Frame220, CAVE body `0x426aff` |
| P7 | 91/91 | Not available in this proof | Frame220, CAVE body `0x426aff` |
| K1 | 12/12 | Not available in this proof | Frame141, AffGame view `0x415b77` |

P6 includes `between_frames220`; its failing frame phase is not counted equal.
The other frame hashes cover the engine owner's exact indicator/unit-record
hash scope, with original input answers and order packets also equal; they do
not imply whole-memory comparison where no full window exists. Each world starts
from S0 and runs its prefix without loading captured frame128 or later states.
State proofs explicitly omit rendering, so a renderer stop is reported separately.
Full requested windows beyond named stops remain pending engine support.

The [delivery manifest](../apps/macos-preview/validation/m3-input-delivery.json)
links the per-probe results, no-input regressions and native UI evidence. Current
APP_BUILD validation UI timing is **46.489 displayed fps average / 27 minimum**
over **8.712 seconds**, including startup audits. The optional new 65-second
validation timing repeat was cancelled before execution; validation UI tests and
9,200-frame equality passed. Common checks pass **2,009 tests / 622 optional
skips**, with zero failures/errors. No milestone acceptance is made.

## ABI 1.6 and original pacing

Fetched main **240ea87** supplies ABI 1.6. Jogar explicitly selects
`rl_execucao_definir(world,1)` after complete S0 loading, before phase 1.
Validar keeps policy 0 and all existing equality/observer work. The native
consumer accepts major 1, minor >=6; Graphics remains 1.7. The input-state proof
uses persistent audited policy 2 so actual poll answers remain observable.
Switching the UI mode recreates the world; a mode change after phase 1 is refused.

The [static pacing report](../apps/macos-preview/validation/m3-abi16-original-pacing.json)
and [instruction listing](../apps/macos-preview/validation/m3-abi16-original-pacing.asm)
are derived read-only from intact RISING.EXE SHA256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
They preserve original byte identities and record every executable-section
reference to timer imports and their thunks. Reproduce with existing repository
pefile/capstone dependencies on PYTHONPATH:

```sh
python3 -B apps/macos-preview/scripts/macos_original_pacing.py \
  --exe /absolute/path/to/source/cd/INSTALHD/RISING.EXE \
  --output .local/original-pacing-recheck.json
```

The active `WinMain` path at `0x460205..0x46021b` advances whenever the message
queue is empty. The iteration calls `CalculGame` at `0x47505e`, then rendering
at `0x475063`; `GameNextFrame 0x45d015` increments a counter. The single
GetTickCount call, in `CalculFrame 0x43f710`, measures iterations over >=1,000 ms
for the two-digit FPS display. It does not wait for a deadline. A separate
[timestamp dataflow scan](../apps/macos-preview/validation/m3-abi16-pacing-dataflow.json)
finds all eight decoded direct references to its counter/timestamp globals inside
CalculFrame, including no reader of the stored last-tick value at `0x4e17b4`. The draw divisor
at `0x417909` is applied after simulation. `DDFlipPage` uses surface vtable
`+0x1c` (BltFast), flags `0x10` (DDBLTFAST_WAIT), and retries a busy blitter;
the [Microsoft BltFast contract](https://learn.microsoft.com/en-us/windows/win32/api/ddraw/nf-ddraw-idirectdrawsurface7-bltfast)
describes waiting until a blit can be submitted. The [Microsoft DirectDraw header](https://raw.githubusercontent.com/microsoft/win32metadata/main/generation/WinSDK/RecompiledIdlHeaders/um/ddraw.h)
identifies flag 0x10 and vtable slot 7. This is not a fixed simulation timer or a
vertical-blank wait. The inactive
window path uses WaitMessage. Other timeGetTime sites concern FLI playback,
network input, CD audio deadlines and RNG seeding; WaitForSingleObject sites
are CRT semaphore/join paths. No active-loop fixed-Hz gate is established.

The native window therefore defaults to **Original (sem limite)**, reproducing
that uncapped scheduling policy. The 15/20/30/60 caps remain explicit alternatives.
A particular historical computer's elapsed game speed remains **unmeasured**:
CPU, driver, blitter and message workload affect it, and native Apple Silicon
throughput is not a historical calibration. The engine's 20 Hz virtual TickClock
is unchanged to retain all state/frame/clock equalities. No original capture,
mask, reference pin, engine source or graphics fallback is changed.
