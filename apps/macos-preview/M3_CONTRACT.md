# macOS accepted-state consumption contract v4

Identifier: `rising-lands/macos-state-consumer/4`. This version explicitly accepts Graphics
render API **1.3** and its full128-frame reference while preserving the existing
read-only playback and pixel/cache chaining. No live
frame delivery, orders, game input protocol or milestone acceptance is added.

## Evidence and memory

The M1 loader retains `MONDE01/original-v2/M1-accepted-inspection` (881 blocks,
2,659,375 bytes). M2.2 is separately labeled
`MONDE01/display-v2/M2.2-accepted-evidence`. Its initial state is the accepted
**display-v2** MissionLoad result; the original-v2 M1 image is never substituted.

`MacOSM22Playback.open(source_root=None)` verifies the acceptance, compression
manifest, xz and raw-JSON hashes, display entry and MissionLoad artifacts. Pins
remain in `macos_m22_playback.PINS`. Every one of the 257 ordered phase summaries
and 11 full checkpoints is verified before opening. Missions' unchanged memory
loader/delta applier and the runtime comparator's pure reader definitions are
loaded by path. Only those unchanged AST definitions are compiled; simulation
imports, constructors and emulator dependencies are not executed or stubbed.

The xz identity is
`4c8f5c14a9623131dd019eafcdc49ea63054ee358f9defde58c12cb949f59ff3`;
raw JSON is
`1ad031b96300e5c632fd5b6b7857ae30792f78e86531e4f17d1bf7124c6dd930`.
The intact original executable is
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

Source roots are explicit or resolved from the adjacent bundle snapshot.json
relative archive. Traversal, absolute archive paths and escaping symlinks are
refused; no deployed consumer guesses an external repository. Images contain
immutable bytes at original addresses, ordered by numeric base then name.
Identity includes contract, source hash, phase and state summary. There is no
pointer rebasing or fabricated state in gaps. Reads must fit one captured block.

Existing navigation is preserved: `step_to_phase` takes exact names or indices
0..256; `step_to_frame` takes 0..128 or frame names; reset returns to state_s0.
Failed validation leaves the current image unchanged, and repeat navigation
returns identical state. Observed words include the counter, viewport, both
RNG words, shared permutation cursor and HUD flag. LIVE `apply_frame` remains
reserved and always raises RuntimeContractPending.

`fork()` makes an independent cursor over verified evidence. `drawing_input()`
returns the preceding captured image for an AffGame phase: load_tail before
between_frames, and frame(k-1) before between_frames(k). This is essential:
between_frames ends at the **next CalculGame entry**, after the window loop has
incremented the counter. That ending image is not AffGame's entry memory. No
bytes are patched to manufacture an entry image.

## Graphics 1.3 chain

The renderer is loaded in an isolated worker to keep Graphics and Economy's
flat `construcoes` names separate. Exactly `(1, 3)` is accepted, on module load
and returned result; every other version is refused clearly. The original
service-test KeyError was secondary: a refused version returned `ok:false`
without `playback`, and the test indexed that key. Tests now assert success
before inspecting data, cover the explicit error response, and the client
validates successful response shape.

Four Graphics artifacts are file-SHA pinned in `RENDER_PINS`:

- superficie-inicial-m22-v2.json
- cache-terreno-inicial-m22-v2.json
- verificacao-cadeia-m22-v2-api13-128.json (128 reference renders)
- superficies-fase-m22-v2.json (257 native phase-end surface hashes)

The initial surface/cache are loaded only through Graphics'
`carregar_superficie_inicial` and `carregar_cache_inicial`, which verify their
payloads and bank base. The surface matches the accepted load_tail hash. It
represents original RestoreAll/MenuInit output before the first AffGame.
No cold/empty cache, blank surface or independent mid-sequence start is used.

For every between_frames(k), call Graphics `renderizar_quadro` with its captured
entry memory, previous **pixels and cache**, and the hash-checked catalog.
Carry both returned objects to the next drawing phase. frame(k) is **undrawn**
and retains the surface/cache. load_tail publishes the initial original artifact
without reimplementing RestoreAll. A cadence return, if observed, is also
reported undrawn. Backward navigation resets/replays from the initial artifacts;
forward navigation processes every intervening phase. No phase is skipped to
start rendering with an invented cache.

`macos_habitation_view` binds read-only captured structure/unit buffers to the
unchanged Economy `estrutura_habitada`, `bag_contient_troupe`, `contar_unidades`
and offset/word readers, compiled by path to avoid constructor defaults and
module collisions. This supplies the real habitation query, never a constant
true callback or synthetic economy. Its result is checked against the existing
native Graphics habitation reference. Neither game state nor owner code changes.

Only Graphics supplies rendering, palette expansion and PNG encoding. The
shell displays its image with an image element. Cache keys, payload hashes,
cursor, entry-state identity, stop address and verification status are recorded.
Applicable chained hashes must equal Graphics' frame 1..128 reference before
publication. Native post-HUD surface hashes are reported as **different** where
appropriate, never mislabeled as a complete-render success.

## Visible limitations and Graphics 1.3 evidence

Graphics 1.3 is additive over 1.2: the inputs, outputs, indexed format and
cache/surface chaining stay unchanged. Its validated normal bodies for unit
types 1/8 remove the prior 0x41591F stop from accepted M2.2 playback. Other
records outside Graphics' published domain retain their named stops; generic
partial/stop handling and version refusal tests remain required.

The consumer pins Graphics' full 128-frame reference, SHA-256
`4f2d536fec21cde39f885f1e6cccbbda83c5130b8ba60cc557f38c27fc508407`.
Every drawing phase must match the applicable chained-pixel hash before
publication. This replaces the old 12-frame 1.2 reference for current validation;
the historical reports remain unchanged. There are still 257 memory phase
summaries and 11 full memory checkpoints.

HUD rows >=544 and cursor remain **not drawn**. `full` means the supported
playfield composition returned without a named stop, not a post-HUD full-frame
equality claim. Graphics' chain differs from its native checkpoint only below
the supported playfield (first differing row 547, from frame 2). Native phase-end
hashes remain recorded honestly and are not substituted for checkpoint hashes.
The initial cache/surface are still required; no independent mid-sequence
start, fallback drawing, live delivery or game input is added. The current
[per-phase report](validation/m3-m22-render-v4.json) records actual results.

## Native shell and builds

Inspection remains separate from synthetic training; opening it pauses training.
It exposes phase/frame navigation, reset, original-address reads, block filter,
observed words, image/stops and verification. Requests may require replay from
the start; the UI allows a bounded 180-second inspection response window. The
native smoke uses actual controls through frame 12, reads memory, filters blocks,
checks the image/stop/limitations and resets. Full 128-frame rendering is verified
separately by the per-phase report, not by relaxing the window-open smoke.

`compilar-jogável --development-ref HEAD` accepts explicit `--inputs-root` and
`--data-root`, with RISING_PYTHON_RUNTIME for relocatable CPython 3.12 ARM64.
All inputs remain read-only and outputs stay inside this independent clone.
Bundle name and identity are unchanged. See [manual](../../docs/MACOS_PLAYABLE.md)
and [handoff](HANDOFF.md) for actual commands and results. Live runtime delivery,
orders, remaining Graphics passes and M2.3 stay outside this consumer's scope.


## Native engine dependency — architecture decision, 2026-10-29

The future playable engine and rendering are a native Rust library exposed
through a C ABI. Swift remains the macOS shell. Python remains the original-
validated reference and test harness, including this accepted-evidence
inspection/playback path. The bundled runtime remains for those uses for now;
its inclusion in a later shipped game is undecided. No live-simulation delivery
is to be built on the embedded Python worker. `apply_frame` remains reserved
and raises RuntimeContractPending; contract v4 and its evidence APIs are unchanged.

The eventual Swift native-library adapter is a separate dependency from the
read-only evidence worker. Before any loading or calling implementation, the
coordinator must publish the C ABI for engine lifetime, frame stepping, memory
views and render output, together with version/compatibility checks, ownership
and buffer lifetimes, thread requirements and failure semantics. Library
location and loading policy also require that contract. This document defines
no speculative symbols, layouts, signatures or executable stubs. No simulation
or fallback behavior is provided while that dependency is pending. Existing
Graphics 1.3 evidence rendering remains pinned independently.

The published Rust pilot ABI handles isolated routines, not full live frames.
This inspector does not bind it; production frame-step/memory/render output
and native loading policy remain coordinator dependencies.
