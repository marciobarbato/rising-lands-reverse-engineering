# macOS accepted-state consumption contract v6

Identifier: `rising-lands/macos-state-consumer/6`. This version explicitly accepts Graphics
render API **1.5**, enables its HUD/cursor option, and checks the original full
800×600 phase-end surface while preserving read-only playback and cache chaining. Live ABI 1.1 is a separate session described below. Orders remain record-only; no milestone acceptance is added.

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
RNG words, shared permutation cursor and HUD flag. The immutable playback API refuses `apply_frame`; live execution uses the separate `MacOSLiveSession.apply_frame` boundary below.

`fork()` makes an independent cursor over verified evidence. `drawing_input()`
returns the preceding captured image for an AffGame phase: load_tail before
between_frames, and frame(k-1) before between_frames(k). This is essential:
between_frames ends at the **next CalculGame entry**, after the window loop has
incremented the counter. That ending image is not AffGame's entry memory. No
bytes are patched to manufacture an entry image.

## Graphics 1.5 chain

The renderer is loaded in an isolated worker to keep Graphics and Economy's
flat `construcoes` names separate. Exactly `(1, 5)` is accepted, on module load
and returned result; every other version is refused clearly. The original
service-test KeyError was secondary: a refused version returned `ok:false`
without `playback`, and the test indexed that key. Tests now assert success
before inspecting data, cover the explicit error response, and the client
validates successful response shape.

Four Graphics artifacts are file-SHA pinned in `RENDER_PINS`:

- superficie-inicial-m22-v2.json
- cache-terreno-inicial-m22-v2.json
- verificacao-cadeia-m22-v2-api15-128.json (128 reference renders)
- superficies-fase-m22-v2.json (257 native phase-end surface hashes)

The initial surface/cache are loaded only through Graphics'
`carregar_superficie_inicial` and `carregar_cache_inicial`, which verify their
payloads and bank base. The surface matches the accepted load_tail hash. It
represents original RestoreAll/MenuInit output before the first AffGame.
No cold/empty cache, blank surface or independent mid-sequence start is used.

For every between_frames(k), call Graphics `renderizar_quadro` with its captured
entry memory, previous **pixels and cache**, the hash-checked catalog and
`hud=True`. Before calling it, read every region returned by
`regioes_necessarias(memory, hud=True)` through the immutable captured image.
This includes minimap `[0x507D5C]` (width×height at `0x496FE0/E2`) and player
table `[0x5080A8]` (5×20 bytes). Missing/short regions fail before rendering,
without allocation, defaults or state publication.
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
publication. With HUD enabled, the returned surface must also equal the
original phase-end hash before publication when no stop is returned. Undrawn
phases retain that same verified full surface. The reference is no longer a
pre-HUD checkpoint.

The render record includes `hud:true` and `required_regions` for drawing
phases. Their `native_full_surface_sha256` / `equals_native_full_surface`
fields refer to the full post-HUD surface. Every phase also reports
`native_phase_end_sha256` / `equals_native_phase_end`; no-stop mismatches are
refused before publication, including undrawn phases. The former pre-HUD
`native_checkpoint_sha256` fields are replaced in consumer contract v6.

## Full-surface Graphics 1.5 evidence and limits

The consumer pins `verificacao-cadeia-m22-v2-api15-128.json`, SHA-256
`d95618beff805b5e47c7be6ec922cdf9cda75c4063b0cd52c254a1a116e19c10`.
All 128 chained/native full-surface hashes equal the predecessor 1.4 report;
a consumer regression checks every pair. The fresh owner proof used `--hud`.
The only additional external region is `[0x4e24bc]`, 256 grayscale bytes,
preflighted through Graphics' own declarations. New input-time overlays/action
panels, drag box, target and second cursor are accepted within Graphics' stated
1.5 domain; see the owner contract in `docs/GRAPHICS.md` and `M3_INPUT_RENDER.md`.
Selection order markers, nontrivial bags, other owners/bodies, damage/fire,
placement, recruitment, tooltips, market/events/messages and other unsupported
branches retain named stops. No input-time gameplay equivalence is claimed.
Palette cycling remains outside this static-palette renderer.

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
Inputs remain read-only and outputs stay under the explicitly declared data root.
Bundle name and identity are unchanged. See [manual](../../docs/MACOS_PLAYABLE.md)
and [handoff](HANDOFF.md) for actual commands and results. Orders and branches beyond the published Rust/Graphics domains remain dependency stops; live no-input execution is specified below.


## Live Rust ABI 1.1 session

`MacOSLiveSession(root, library, executable, renderer=None)` owns one serial
world. `reset()` frees/recreates it at 20 configurable-policy ticks/s, epoch 0,
and loads accepted **display-v2 S0** plus only the four original immutable jump
tables declared by Stage 2: `0x45ed20`/160 bytes, `0x454344`/104,
`0x4543c8`/100 and `0x426880`/84. Captured overlaps must agree byte-for-byte;
only missing subranges are added. The intact PE is hash-checked to the identity above;
no later state becomes an engine input. The ABI is exactly `0x00010001`.
The app builder compiles integrated `motor/` release sources into its ignored
build target, copies/signs the dylib beside the worker and copies the hash-checked
PE solely as the table input. No external library search/fallback occurs.

`apply_frame()` advances **one phase**: 1 at load_tail, then alternating 2/3.
The UI first requests the load tail, then one 2/3 pair per frame. Cursor (0,0),
o messages/keys, original offscreen address, phase-1 registers and the initial
phase-2 registers are explicit accepted inputs. Later registers are carried
from actual ABI outputs. The four MSG words and three saved words follow the
Stage 2 proof; fixed-step time comes only from Rust. No wall-clock delta enters
logic. State, events and buffers are copied through the C ABI, never pointers
into Rust-owned memory. Free, reset, phase calls, event reads and complete bulk
projection are serialized in the isolated worker. ctypes is the temporary ABI
bridge while Python supplies Graphics; Swift owns the native shell.

Every phase through 128 is compared to accepted playback under the unchanged
M2.2 cumulative mask (file SHA `bf36e6e8f6a38202fa3248256d3de9f768497caa835a563a3ef119be994127f0`).
Both **masked state hashes** are equal, including all 11 full checkpoints.
Raw full-memory hashes can differ in excluded display bytes and are never
reported as equal. Original addresses/names and immutable bytes form the
Graphics memory view. AffGame gets the **preceding live image**, and previous
pixels/cache chain from the original initial artifacts. `hud=True` and the
same required-region, version, chain and original-surface gates apply. Display
effects are already part of Rust's phase-2 logic contract; the consumer does
not patch them back or apply them twice.

Beyond 128 the renderer keeps chaining but has no accepted surface reference;
verification fields are null, never true by default. Rust or Graphics errors
latch the first named stop with phase/type/detail, shown in PT-BR UI context.
A failed ABI call publishes no phase. If projection/render validation fails
after a successful private ABI call, no new image is published and the session
cannot step again until reset. Partial Graphics results remain explicitly
partial and stop the live runner. `close()` releases exactly once.

The legacy immutable M1/M2 playback `apply_frame` guard remains for callers
that try to mutate evidence; it is not the live runtime interface.

## Record-only event mapper

The UI maps scaled image coordinates to original 800×600 coordinates and
records WM_MOUSEMOVE/left down/up/double-click/right down/up (0x200..0x205),
with signed 16-bit lParam coordinates and mouse/modifier wParam. Enter, Shift,
Control, Alt, Escape, Space, arrows, Delete and X map to the prescribed vkeys.
Focus loss releases held keys in the journal. UI recording is scheduled at
frame 129 or the next live frame, whichever is later; the accepted no-input
prefix remains unchanged. This is a future-input journal, not a claim that
Rust has consumed those events.

`MacOSInputRecorder.poll(frame, original_site, api, ...)` scaffolds ordered
GetCursorPos, PeekMessageA (peek/remove), and GetAsyncKeyState (held high bit,
pressed-since-last-poll low bit) answers. Actual poll addresses must be supplied;
arrival events alone invent no poll sites. Messages are destined for the
original WndProc 0x4181a1; no game flag stores are made here. Neither mouse
messages nor keys enter ABI 1.1. The raw schema is separately named
`rising-lands/macos-input-journal/1`; deep-copy export uses a native save panel.
Missions' `rising-lands/monde01-scripted-input/1` interchange remains a named
export dependency until its owner module lands and is reviewed. Raw journals
must not be relabeled as that schema. Test A/B original replay and order
injection remain pending the engine/input providers and Missions capture.

## Live performance path — `rising-lands/macos-live/2`

The immutable accepted-state API remains consumer v6. The live image is now a
serial read-only **lease**, valid until its alternating slot is reused two
phases later. The UI receives independent JSON metadata and raw pixel bytes,
not a retained Python view. One reusable ABI bulk buffer and one Graphics view
slot are selected per phase; two of each isolate publication failures. Only the
18 regions returned by `regioes_necessarias(..., hud=True)` are copied into the
Graphics views. Pointer/extent changes are revalidated before any draw. Current
arbitrary-address reads use the last successfully published full ABI buffer.
A failed phase/render does not replace that buffer or the visible image.

Full masked state checks still cover every declared byte outside the unchanged
M2.2 mask, in original-name ordering. They stream over the bulk snapshot using
the macOS-owned native byte codec v1 and compare with accepted expected hashes
prepared before stepping. The same 257 states, 11 checkpoints and 128 surfaces
are required. The native helper verifies layout/offsets and mask spans before
reading and retains no pointers. Missing or incompatible helpers fail by name;
no automatic implementation switch occurs in production. The explicit
no-renderer diagnostic API and Python codec tests remain separately labeled.

ABI 1.1 exports the entire world even when a caller needs fewer regions; this
consumer does not claim server-side filtering. It avoids the former size-query
projection, per-block byte copies, 25,197 Python memory-block objects and
per-block SHA calls in each phase. The unchanged Economy read definitions and
original palette are cached once per immutable archive.

Live presentation is `indexed8-rgb24/1`: width 800, height 600, stride 800,
480,000 indexed bytes and 768 RGB palette bytes (base64 only as transport
framing), plus the exact phase generation and indexed SHA-256. The canvas
reuses its palette lookup, ImageData and index buffers, then calls putImageData.
Frame shape and palette length are checked before display. Native smoke reads
back every RGBA byte and runs the real live play/pause loop; the full proof
checks every decoded transferred surface against the native phase-end hash.
No PNG compression occurs on this path. `--png-output PATH` exports a final
Graphics PNG for evidence, refusing overwrite; the immutable evidence inspector
retains its PNG presentation for compatibility. Unsupported orders, display
effects, clock/RNG semantics and Graphics 1.5 pixels are unchanged.

## Current native live path — ABI 1.3 / app driver v1

This section supersedes the Python-rendered live/v2 path above. The production
UI intercepts live operations in Swift and never sends them to the Python
worker, which explicitly refuses `NativeLivePathRequired`. Python remains the
immutable evidence inspector and proof oracle. The inspector explicitly accepts
Graphics 1.7 (native 128-frame pin `4448aeb44920d89b271e9af276477ee545fe797164b5b654e26c18a545d1a16c`);
its optional `texto` callback stays absent. Rust retains Graphics 1.5 semantics.

`macos_live_create` owns one actual ABI1.3 world/renderer and caller buffers.
Only accepted S0 and four hash-checked original table inputs initialize world
state. Prepared native files include the original initial surface/cache, nine
verified assets, phase-entry inputs, layout/mask spans and original expected
hashes. Expected hashes are comparisons only and never become world bytes.
The runtime order is phase1; then repeatedly generation query → Rust render
with HUD=1 → phase2 → phase3. The read-only render does not apply effects;
phase2 owns them. Successful body phases increment the completed-frame count.

The driver checks the first 257 states/11 checkpoints in production and every
surface through 9200. Proof mode extends the identical full-state comparison
to 18,401 phases, without a separate frame implementation. Callback hooks are
proof observers only, not game providers. Cache/ordered-effect exports and
Python rendering are compared in tests. Unknown paths latch the actual callee/
address/reason; partial pixels remain actual prefixes. The native Metal view
copies indexed/palette outputs into reusable textures/buffers, waits for GPU
completion before reuse, and reports real presented-window throughput. No
JSON pixels, PNG encoding, full Python projection or Python simulation runs
in live play. GPU readback/PNG is an explicit evidence action only.

The hardened Swift executable links the same Rust ABI and app C driver
statically. This avoids loading an ad-hoc non-platform library into a hardened
process and needs no weakened library-validation entitlement. The shared Rust
library and dynamically bound driver remain in proof tooling; static and shared
artifacts are built from the same pinned sources and recorded separately.
All world/renderer/host-buffer access is serialized. Reset prepares a valid
replacement before freeing the old handles. Native-window input orders remain
unsupported; existing record/replay inspection scaffolding is separate.

## M3.3 Test A — frame input interchange and answer stream

The current recorder is `MacOSSessionRecorder` in `macos_scripted_input.py`.
The former `MacOSInputRecorder` remains a separately versioned legacy poll
journal; its pressed-since-last-poll model is not the Missions script contract.
A legacy journal containing polls cannot be silently exported as a frame file.

`ScriptedInput(root, dict_or_json)` imports Missions schema
`rising-lands/monde01-scripted-input/1`. The adapter executes only the owner's
unchanged pure validator AST (`carregar_entrada`, `_inteiro` and its constants),
avoiding emulator imports/provider namespace changes. Missing definitions or a
schema/start mismatch fail explicitly. Tests also import the complete actual
Missions harness in a separate process and validate a human export unchanged.
`export()` returns independent JSON data; `export_bytes()` emits canonical UTF-8
JSON with sorted keys, one-space indentation and one final newline. All frame
messages, literal signed key answers and metadata survive normalization.
Export → import → export is byte-identical; original evidence is never rewritten.

`FrameAnswerMapper(script, hwnd=explicit_u32)` consumes `begin_frame(k)` and
`poll(kind, phase=..., site=..., vk=...)`. It implements cursor, key, peek, get,
translate and dispatch answers. Sites are the original call return addresses,
not routine entry addresses: e.g. GetCursorPos at `0x475044` records `0x47504b`,
the loop PeekMessageA records `0x4601d8`, GetMessageA `0x4601eb`, TranslateMessage
`0x4601f9` and DispatchMessageA `0x460203`. A cursor holds its last declared
position, initially the owner's explicit `(0,0)`. Messages queue in file order;
peek does not remove, get removes, translate returns zero, and dispatch targets
WndProc `0x4181a1`. No WndProc/game flag is written or simulated by this layer.
Keys reset to zero on every new frame and each poll repeats the frame's literal
i16 value. This includes zero for native polls of unlisted vkey `0x45`.
Poll phase/site validation and unconsumed/skipped message frames fail by name.

`MacOSSessionRecorder(root).event(frame, event)` takes monotonic integer game
frames >=129. Mouse dictionaries contain `kind='mouse', msg, x, y, wParam`;
key dictionaries contain `kind='key', vkey, down`. Coordinates must fit 800×600.
The human key set is Enter, Shift, Control, Option/Alt, Escape, Space, arrows,
Delete and X (the prescribed 12 vkeys). Key messages use explicit normalized
Windows scan/extended/previous/transition bits; held keys export `-32768` on
every frame until release, including all of a depot-mode Control hold. Imported
scripts additionally preserve arbitrary owner-accepted key messages/answers,
including K1's digit-1 message, without inventing a human hotkey mapping.

A human press schedules mouse move at k, button down at k+1 and release at k+3.
The physical release remains in the raw journal but does not add a second
scripted release. Right and double clicks use 0x204/0x205 and 0x203 respectively.
Moves received during the gesture wait until k+4; consecutive clicks serialize.
This stage records fixed clicks, not continuous drag gestures. Cursor holding,
message ordering, signed key values and literal poll repetition are under test.
`export_script(stop_frame=...)` rejects truncation of scheduled events and
returns a validated `ScriptedInput`; `journal()` is separately named
`rising-lands/macos-frame-input-recording/1`. Invalid events leave it unchanged.

In the native window, NSEvents are assigned to the next frame on the same
serial queue that owns the engine. No wall clock enters the file. Recording
starts only after completed frame128; reset is disabled while recording.
Control/Shift/Option changes, initial observed held modifiers and focus-loss
releases are recorded. Native events never enter Rust's input structure.
The visible **Gravando entrada** indicator and **Exportar entrada** action use
the isolated worker for file preparation only. Stop/export drains native event
work and the worker request chain. Export preserves canonical bytes through a
native save panel; recording errors latch and prohibit partial-success export.
**Ordens ao vivo indisponíveis** remains visible.

Test A reads only request frame/phase/site/kind/vkey from each native poll log.
Every answer is computed from the imported/exported script. Scenario HWND=0 is
an explicit declaration, checked against every native dispatch. Comparisons
include all 155,597 records from P1/P2/P3/P6/P7/K1. The sole excluded field is
`wndproc_flags_after`, an original-game output: its 102 records belong to the
deferred state half. No expected message/key/cursor/flag answer feeds the mapper.
State hashes, WndProc effects and human Test B await engine order support;
this stage does not inject orders or claim their state equivalence.
