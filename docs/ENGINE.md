# Native Rust engine

The pilot foundations and bounded frame-logic port are documented below.
This is not a playable engine, M2.3 work or M3 acceptance. The game engine and
rendering will be Rust; Swift owns the macOS shell, C only small tooling, and Python remains the original-validated reference
and test harness. This work owns only `motor/` and this document. The existing
app, references, captures and other fronts are unchanged.

## Reproduce

Install [rustup stable](https://rust-lang.org/tools/install/) for
`aarch64-apple-darwin`. Add the rustfmt and clippy components:

```sh
rustup toolchain install stable --profile minimal
rustup component add rustfmt clippy --toolchain stable
./motor/validate.sh
```

The workspace pins the stable channel and has no external Cargo dependencies.
`Cargo.lock` is committed. The validation script runs formatting, strict Clippy,
`cargo test`, `cargo build`, Python unittest discovery, the ctypes capture
harness, C header layout checks and a Swift CLI client. Python3 standard-library
modules suffice; no original media, emulator, assets, pip packages or app bundle
are needed to reproduce. Capstone was used only for the separate static audit.

The essential engine validation can also be run manually:

```sh
cd motor
cargo test --workspace --locked
cargo build --workspace --locked
python3 -B -m unittest discover -s testes -v
python3 -B testes/differential.py \
  --library target/debug/librising_engine.dylib \
  --output ../.local/engine-validation-new.json
```

The optional output path must not already exist: the harness refuses to replace
evidence. All generated libraries, executables and caches stay in ignored
`motor/target/`; choose clone-local `.local/` for local reports. `RL_LIBRARY`
selects another built library (for example release) for Python tests. The
supported native delivery host is 64-bit aarch64 macOS; no Linux/Windows or
cross-compilation validation is claimed. See [handoff](../motor/HANDOFF.md) for
actual toolchain, baseline, SHAs and results.

## State and original-memory projection

`rl-core` has no FFI or host APIs. `GameState` owns optional semantic `WorldRng`
and `CrtRng` values. A missing capture field stays absent, never a default seed.
`BcdDigits` is four unpacked bytes, units first; its thousands byte is allowed
to exceed 9. It is loaded/projected per call because BCD buffers are caller-owned
scratch objects rather than a fixed game-global pool. No projectile state is
ported in this pilot; the optional ProjectileInit/Set scope is deferred.

`MemoriaJogo` is an explicit sparse `BTreeMap<u32, Vec<u8>>` of owned declared
regions. Addresses are original 32-bit addresses, never host pointers. Regions
are nonempty, nonoverlapping, ordered numerically and cannot extend past 2^32.
Accessors read/write u8/u16/u32 little-endian only when the entire access fits
one declared region. Adjacent regions are not implicitly coalesced. Missing
access names its address/width; no gap is zero-filled. Partly captured modeled
u32 fields raise IncompleteField instead of appearing absent.

`GameState::load(memory)` returns semantic state and a `Projection` layout.
The layout retains all uninterpreted declared bytes and explicit original
address bindings. `GameState::project(layout)` clones that declared template
and writes semantic fields into their bound addresses. Tests prove identity
for memory→state→memory and for modified typed state→memory→state, while opaque
bytes remain unchanged. Modeled-field presence must match the captured layout;
adding an unbound value or removing a bound value raises ProjectionFieldMismatch
instead of silently retaining stale template bytes. This is an incremental port: uninterpreted bytes do
not acquire invented Rust game semantics. The state is not a packed original
struct or an address-indexed simulation.

`World::step` projects current state to a private transaction, executes the
selected typed operation and reloads semantic bindings after the result. This
also preserves BCD buffers aliasing an RNG/global. Only successful calls publish
new world state and output registers. A failed call publishes no prefix. The
pilot's transactional error semantics are not a claim that arbitrary failing
original routines roll back their earlier writes.

BCDToInt reproduces aliasing explicitly: zero the destination word, then each
digit read overlapping that word sees the current typed accumulator bytes.
The final word is projected back. The register adapter preserves the original
scratch effects established by the [static review](../motor/research/bcd-register-review.asm).
Unknown later engine paths must receive named dependency errors, never empty
callbacks or fallback success.

## Pilot C ABI 1.0

`rl-ffi` builds `librising_engine.dylib` as a `cdylib`; the contract is
[motor/include/rising_engine.h](../motor/include/rising_engine.h).
A Clang module map supports `import RisingEngine` in Swift. The
[Swift CLI test](../motor/testes/abi_smoke.swift) calls the actual dylib; it does
not integrate live simulation into the macOS app.

`rl_versao()` returns `0x00010000` (major in high 16, minor in low 16). Creation
requires that exact version, and Python/Swift clients gate it explicitly.
Changes to layouts, widths, semantics or existing signatures require a major
bump. Additive functions require an explicit minor bump, documentation and
client tests; consumers do not silently accept a new version. Crate version
0.1.0 describes pilot maturity and is distinct from ABI 1.0.

| Function | Contract |
| --- | --- |
| rl_criar_mundo | Version, explicit ticks/second, epoch_ms → opaque u64 handle; zero rate refused |
| rl_liberar_mundo | Releases the handle; stale/zero/double-free refused; tokens are never reused |
| rl_carregar_blocos | Copies all input blocks atomically; replaces the whole projection; preserves virtual clock |
| rl_executar_rotina | Isolated routine identifier and seven data GPRs → updated registers/world; **not a frame step** |
| rl_quantidade_blocos | Number of projected blocks |
| rl_projetar_bloco | Indexed block in numeric-address order; size query, then copy into caller buffer |
| rl_avancar_ticks | Advances virtual clock only; executes no game logic |
| rl_relogio | Tick u64 and virtual milliseconds u32 |
| rl_erro_mensagem | Thread-local UTF8+NUL error text, query/copy; querying does not clear it |

`RlBloco` has u32 address/length and a host pointer to readable input bytes.
`RlRegisters` has u32 EAX, EBX, ECX, EDX, ESI, EDI, EBP, in that order.
No x86 EIP/ESP/EFLAGS or stack execution is exposed. All seven data registers
are compared to original returns. Python's BCD providers return None and model
memory only; the harness explicitly adds their statically proved scratch
register effects, rather than claiming Python returns them. IntToBCD returns
EAX=0, EDX=1; BCDToInt preserves EAX, sets EDX=10000. Other data GPRs are kept.

No Rust-owned pointers escape. Input storage may be released after the call;
projected buffers belong to the caller. Nonnull foreign pointers must be valid,
aligned, sized as declared and disjoint from output storage. Arbitrary dangling
pointers cannot be validated by Rust and violate the C caller preconditions.
The ABI supports 64-bit hosts. Load limits are 65,536 blocks and 64MiB total;
zero blocks are allowed, zero-length individual blocks are refused. The pilot
copies data for correctness and makes no real-time throughput claim.

All calls use an internal registry mutex, with per-thread error messages. Use
one caller/serialization discipline per world, including free and a complete
multi-call projection enumeration: different calls are atomic individually,
not one combined snapshot under concurrent mutation. Independent worlds are
isolated and tested under concurrent callers. No callback crosses the ABI.
Rust panics in stateful entry points are caught and returned; a poisoned mutex
fails explicitly. Process-level allocation aborts/foreign-pointer violations
are not recoverable status errors.

| Status | Name |
| ---: | --- |
|0|OK|
|1|InvalidArgument|
|2|InvalidHandle|
|3|MemoryError (including undeclared, incomplete, projection mismatch, overlap, overflow)|
|4|UnknownRoutine|
|5|UnsupportedPath (including thread getter at 0x48c513)|
|6|BufferTooSmall|
|7|Panic|
|8|Poisoned|
|9|ResourceLimit|
|10|VersionMismatch|

Success clears the calling thread's previous error. Errors leave the world and
register outputs unchanged. The explicit projection-query exception writes
address/required-size metadata on BufferTooSmall and leaves the byte buffer
untouched. Null/zero is the size-query form. Output storage on other failures
must not be consumed. The header documents exact pointer preconditions.

## Deterministic ticks and clock

One future simulation tick is one logic frame. Host pacing and speed controls
schedule ticks; they never change per-tick arithmetic or supply wall-clock
deltas. This pilot introduces the integer `TickClock`, not a frame dispatcher.
Its tick is wrapping u64; `rl_avancar_ticks` explicitly advances that counter.
A routine call does not implicitly tick. A future frame orchestration must
advance once per validated logic frame in its published contract.

Virtual time is `epoch_ms + floor(tick *1000 /ticks_per_second)`, reduced to
u32 with explicit wrapping for Win32 timer width. The intermediate is u128, so
u64 ticks times1000 cannot overflow. There are no wall-clock reads or sleeps in
Rust logic. A future GetTickCount/timeGetTime consumer must use this virtual
clock; timer/seed initialization is not ported here. Tests cover batching,
rate fractions, u32 clock wrap, u64 tick wrap and identical RNG results under
different pacing/rates. Rate is fixed at world creation, nonzero and explicit.
`TickClock::DEFAULT_RATE` is 20Hz (50ms nominal period), a configurable pilot
pacing policy, **not proof of an original fixed MONDE01 FPS**: Core's cadencia
module explicitly establishes no fixed FPS. Historical timing calibration
remains a coordinator decision.

## Arithmetic and rendering boundaries

All original-width overflow uses wrapping_add/sub/mul/shifts. Narrowing casts
are documented at their width boundary (DX→u16, a digit→u8, virtual time→u32).
Host lengths/indices use checked conversions/addition or bounded structural
invariants; projection address validation rejects ranges beyond2^32. Debug
and release both keep overflow checks enabled, so forgotten unchecked arithmetic
fails tests instead of inheriting build-mode-dependent behavior. No floating
point, host RNG or nondeterministic collection iteration enters pilot logic.

Rendering remains separable from logic. The future output contract must carry
the original 800×600 8-bit indexed surface and palette, scaled by the app. A
separate renderer can later be replaced by an HD implementation. This pilot
contains no renderer, palette, frame output function, asset extraction or blank
placeholder frame. Original assets will be committed/bundled by their later
owner; the projection/oracle harness requires none.

## Ported routine semantics

| Routine / ABI id | Original address | Semantic effect |
| --- | --- | --- |
| Random /1 |0x4704dc|World seed at0x497164: unsigned `(q,r)=divmod(seed,127773)`, wrapped32-bit `n=r*16807-q*2836`; if zero or high bit set, wrapped add0x7fffffff; write seed and return EAX=n|
| LongRand /2, CRT rand /3 |0x45841b /0x48c51d|Getter at0x4990cc must equal0x48e7c7. Seed address is wrapped `u32[0x522244]+12`; address zero returns EAX0 without stores. Otherwise wrapped seed*0x41c64e6d+0x3039, return `(seed>>16)&0x7fff`; EDX preserved|
| IntToBCD /4 |0x467cd1|Low16 DX to four unpacked bytes at EAX, units first, stores thousands→units; no thousands clamp|
| BCDToInt /5 |0x467d3a|Read digits at EDX with destination-alias semantics and project wrapped u16 at EAX|

The32-bit world and CRT seeds are independent. Getter/seed declarations are
required for the selected path; absent bytes and unproved getters are named
errors. The world RNG uses the unsigned full32-bit input path, not an assumed
positive-only seed. The audit and code give exact clobbers and widths.

## Original-first porting and validation procedure

1. Select a fully proved Python routine and original-only capture from its
   owner's HANDOFF. Pin capture and relevant reference identities. Keep both
   read-only. Record original executable identity and coverage limits first.
2. Audit addresses, widths, aliases, mutation order, register effects and
   dependency exits. Commit original research separately from implementation.
3. Define semantic Rust types, then explicit load/project bindings. Unknown
   fields remain opaque; absent bytes are errors, not invented initial state.
4. Port wrapping arithmetic and pure logic. Keep renderer and host effects
   outside logic. Unsupported paths get named errors before publication.
5. Through ctypes, load each captured input into Rust, run the routine, project
   every declared byte and compare with both the original and unchanged Python.
   Compare changed-byte triples, seven data GPRs and captured RNG seeds. Include
   caller-stack writes and unchanged writes when reconstructing input regions.
6. Prove load/project identity, aliasing, errors, atomic publication and repeat
   behavior. Mutate an actual Rust return and actual projected byte in the
   harness and require the oracle to detect each. Test deterministic timing
   separately from original captures, clearly labeling reference-only cases.
7. Fetch/merge latest main into the feature, rerun validation, record toolchain,
   case counts, errors/skips/dependencies and SHAs, then push the feature only.

The frozen pilot corpus is 75 selected records: Random 24, LongRand 12, rand 12,
IntToBCD 19, BCDToInt 8. LongRand/rand include nested captures of the same original
call and are counted separately. This is not 75 independent game scenarios.
All are required; no optional oracle skips. The corpus has only 19 captured
BCD encodes and 8 decodes; exhaustive u16 encoding/round-trip and overlap tests
extend comparison with Python, not the claim of original-native coverage.
See [audit](../motor/research/PILOT_AUDIT.md), [pins](../motor/testes/reference-pins.json)
and [differential harness](../motor/testes/differential.py).

## Open contracts for macOS/M3

The pilot ABI is available for isolated interoperability. Before live app
integration the coordinator still needs to publish:

- full world initialization, complete deterministic frame-step and input/order
  semantics, dependency stops and lifetime/reset rules;
- immutable memory/render snapshots with generation identity and buffer
  ownership/lifetime, including whether multi-call copies remain acceptable;
- indexed 800×600 surface stride/orientation, palette format/updates and explicit
  full/partial/stop status, while keeping rendering replaceable;
- native library location, architecture/version gate, loading/linking and
  signing/bundling policy for Swift, and thread/error-reporting policy;
- tick rate/epoch calibration and exact virtual-clock use at original timer
  calls, plus the later asset packaging contract;
- whether a shipped app retains Python. It remains the reference/harness and
  present evidence inspector; this pilot changes no app runtime.

The macOS consumer's LIVE apply_frame stays RuntimeContractPending. The
additive bounded frame ABI below does not establish an app input/render contract.

## Stage 2 frame logic — ABI 1.1

The current library adds the accepted M2 phase chain: `load_tail` (frame 0),
`between_frames`, and `frame` (`CalculGame 0x42c868`). Stage 2a's three phases
are compared against the intact-original display-scenario evidence, under its
unchanged published mask. This is a bounded native logic port, with pixels and
human orders outside its contract. It does not declare project acceptance.
The preceding ABI 1.0 section describes the preserved pilot interface;
`rl_versao` now returns `0x00010001`. Creation accepts explicitly requested
1.0 or 1.1; existing signatures, layouts, status values and semantics remain.

`GameState` now owns an optional semantic `FrameState`: 800 `UnitState` values,
1,000 `StructureState` values and `FrameGlobals` (counters, AI seed, permutation
cursor, viewport, mission/mode, input and owner/kind counts). Named fields are
loaded/projected with explicit widths and original bindings; unmodeled bytes
remain opaque in `Projection`. A complete frame state is modeled only when
both pools and every declared frame-global field are present. Sparse isolated
routine fixtures retain absent frame state rather than inventing a mission.
Removing a bound state, rebinding a pool or changing pool cardinality fails.
Tests prove every-byte identity, semantic mutation/reload and opaque-byte
preservation. This remains incremental: provider translations operate on a
private original-layout projection transaction to preserve original alias and
read/write order, then reload the semantic state after success. Moving each
provider's internal access to typed fields is further refactoring, not a
claim that every original field already has Rust semantics.

The [C header](../motor/include/rising_engine.h) defines these additive calls:

| Call | Contract |
| --- | --- |
| `rl_passo_quadro` | Phase 1/2/3, copied 72-byte `RlFrameInput`; named unsupported branches fail atomically |
| `rl_eventos_quadro` | Last successful phase's ordered bindings, boundaries and frees; copied 72-byte records |
| `rl_projetar_tudo` | Bulk copied memory projection, LE count then address/length/data records |
| `rl_projetar_liberados` | Same format, actual bytes retained at each free in the last phase |
| `rl_executar_rotina_quadro` | Versioned isolated provider IDs/argument counts for differential testing; no tick |

`RlFrameInput` explicitly carries cursor coordinates, the offscreen address,
eight phase-entry registers, three saved ProgIteration words and four MSG
words. Supported host answers are the accepted no-input scenario: no key,
PeekMessageA=0, ShowCursor=0, SetCursorPos/GetCursorPos=1, and fixed allocations
with handle equal to address. Inputs and all outputs remain unchanged on a
failed phase, including clock and previous events. Each successful CalculGame
body (phase 1's frame 0 or phase 3) ticks once; phase 2 does not tick. No host
clock is read. Phase 2 produces all eight next-entry registers; phase 3 preserves
the six saved data registers and returns ESP+4. Its EAX remains unmodeled,
matching the accepted proof. No renderer or blank frame is supplied.

The port includes the player loop, empty/inactive task paths, monster timers,
input/menu, messages/icons, unit/structure dispatch and their reached state
branches, research/resources/alliances/market/field providers, terrain and
vegetation animation, original RNGs, end conditions and influence queries.
The original display-effect domain guards are retained. Display-only pixels
are excluded, while HUD refresh, CRT draws, shared cursor and shake effects
are modeled. DeleteBank frees its sub-buffers, entries, table and header in
original order; freed bytes and host bindings are exposed for independent
allocation-record validation. Active AI kernels/tasks, raid spawn, movement,
combat, transport, completed troop production and other unsupported branches
stop with a callee name and original address; no empty callback substitutes
for those routines. Projectile animation is implemented across its type
branches; effect-only lifetime branches are supported, while reached damage,
movement and spell calls stop explicitly.

Reproduce the separate full phase proof under the shared heavy lease (read-only
intact executable supplies static tables/issuer classification):

```sh
python3 -B motor/testes/frame_differential.py \
  --executable '/path/to/cd/INSTALHD/RISING.EXE' \
  --output .local/engine-frame1-new.json
```

The executable is hash-checked. The proof pins the original M1 display input,
frame evidence and exact mask, independently verifies all replay checkpoints,
and chains one Rust world from S0 without importing later expected states.
Four immutable original jump tables are explicit additional inputs and must
remain byte-identical. The comparer checks every unmasked byte, RNGs, bindings,
boundary arguments/registers/guards, between-frame registers and complete final
allocation records with actual freed-buffer hashes. Actual projected-byte,
binding-result and boundary-register corruptions must be rejected. Reports
record source/library hashes and source stability. The 128-frame extension
uses `--m22 --frames 128`, with its separate cumulative mask.

`sh motor/validate.sh` includes Rust projection tests, 923 selected original
frame-provider records (773 Core, 132 Economy, 8 AI, 10 Input/Missions), randomized/perturbed
Python comparisons, ABI failure tests, the unchanged 75-record pilot proof,
C layout and an actual Swift client calling the frame ABI. The sparse isolated
captures omit unobserved/same-value bytes in places; the Core/Economy replay
uses explicitly synthetic surrounding pages, checks every captured changed
byte and defined return, and compares the entire fixture against Python.
Only the full-phase proof establishes whole original mission-state equality.
See [frame audit](../motor/research/FRAME_AUDIT.md) and the current stage
[handoff](../motor/HANDOFF.md) for actual results, limits and evidence.

### Proven migration window and performance

[Stage 2a](../motor/validation/stage2a-frame-proof.json) proves frame 0/1 in all
three phases: 16,097,242 compared bytes each, zero mismatches.
[Stage 2b](../motor/validation/stage2b-128-frame-proof.json) extends the same
engine code to 128 frames and **257/257 equal phases**, each comparing
**16,022,275 bytes with zero mismatches** under the unchanged cumulative mask
(153,060 display bytes). RNGs, external observations, registers and all 25,482
allocation records are equal. These are native-port evidence results; project
acceptance remains the coordinator's decision.

The release phase chain runs at **119.83 frames/s** on this Apple M4 Pro
MacBook (24 GiB), under an exclusive heavy lease: 1.0682 seconds of Rust
execution for 128 frames. This includes private state projection/reload and
between-frame effects; it excludes exported snapshots, Python comparison and
rendering. The task's ~0.5 s/frame Python baseline was not freshly rerun.
Full validation and remaining common-check prerequisites are in the
[stage handoff](../motor/HANDOFF.md) and
[summary](../motor/validation/stage2b-summary.json). App/rendering contracts and
support beyond the bounded window remain open.

## Stage 2c — raid-window extension, ABI 1.2

The raid-window implementation extends the same fixed-step engine with the
resolved original task VM, monster group/action rules, spawn and orders, live
movement, class 1–3 path search and contour/optimization scratch, and the
reached projectile creation/lifetime calls. `GetMeteo` and `MAJSympathie`
retain their complete bounded timer implementations and now have additional
perturbed-state comparisons. Python providers remain read-only references.
The full comparison window is frames 0–9,200: 18,401 phases under Missions'
unchanged cumulative mask (153,060 display bytes; 1,560 observed changing
logic bytes). Implementation and proof status are separate; the committed
stage report records actual complete results.

`rl_versao` returns `0x00010002`. Creation accepts explicit ABI 1.0, 1.1 or
1.2. All existing C signatures/layouts/status values remain unchanged; new
isolated provider IDs add raid/tasks (400–409), movement/path/spawn (450–487)
and projectile initialization/set/line preparation (550–552). Existing frame
inputs/events remain 72 bytes. Unknown rules and unsupported original branches
still return a named address error, atomically. No host callback, Python
runtime, wall clock, fabricated task program or captured-effect replay enters
Rust execution. Instructions come from the loaded original resolved RULE table
at `0x514910`, with entries at `0x51a720`.

The canonical semantic state adds fourteen movement/order/animation fields per
unit, plus 100 task values, 100 group values, list heads, counters, iterators
and pending group state. Explicit load/project tests retain opaque padding,
original list bindings and sentinel meanings. Action-record bytes remain
opaque because the original indexed action span overlaps other globals;
independent duplicate semantic bindings would lose alias behavior. Shared
terrain/region/route grids use the same declared original-address bindings;
movement and path search never create a separate grid copy as live state.

[Long-window audit](../motor/research/FRAME_LONG_AUDIT.md) distinguishes complete
proof from declared package openings, an actual-Rust serial continuation chain,
and a serial endpoint/throughput supplement. Each package validates its full
opening, all delta/full checkpoints and policy hashes before comparing Rust.
Independent proofs can run under separate bounded heavy leases. `--serial`
carries actual Rust state between jobs, without loading later original states.
The serial benchmark runs S0 through frame 9,200 in one world, exports only
outside timed execution and checks the complete masked endpoint; it does not
replace the full phase proof.

The completed [Stage 2c proof](../motor/validation/stage2c/proof.json) is
**18,401/18,401 phases equal**, comparing **16,022,275 bytes per phase with
zero mismatches**. It uses all ten declared original package openings and
chains every subsequent phase within each package. RNGs, allocations,
bindings, boundaries and compared registers all agree; there is no first
divergence. The exact mask remains 153,060 display bytes, with all 1,560
observed changing logic bytes compared. The separate uninterrupted S0-to-9,200
run matches the complete masked endpoint and measures **101.87 frames/s**
(90.3068 seconds, excluding exports/comparison/rendering). It supplements the
phase proof with serial endpoint and timing evidence.

The [delivery summary](../motor/validation/stage2c/summary.json) and
[handoff](../motor/HANDOFF.md) record source/library hashes, reproduction
commands and the precise proof scopes. Main's formal Python M2.3 proof was
merged into this feature branch and reviewed; its diagnostics-only comparer
update changes no native runtime sources. Both refreshed gates pass:
`sh motor/validate.sh` (25 Rust tests, 56 Python tests, C/Swift ABI 1.2 smoke)
and prepared `python3 -B scripts/check.py` (1,881 tests, 610 optional skips).
The previous missing-input common-check stop is resolved. No Mac mini run is
needed for the completed native evidence proof. Unreached branches retain
named failures; project acceptance and integration remain with the coordinator.

## Stage 3 — native Graphics 1.5 renderer, ABI 1.3

The renderer binds directly to a Rust world and retains owned, hash-verified
original CMP banks, the PLATGAME palette and the original shadow/lighting
tables. Asset bytes come from Graphics' catalog sources; no asset payload is
committed in motor/. Creation requires the explicit original initial indexed
surface and complete terrain cache. Terrain cache keys, raw 32×33 payloads and
replacement cursor carry between draws. Generic CMP drawing preserves opaque
literal zero, transparent skips, signed clipping, destination remaps and player
colors. Tables and layer plans keep the bounded renderer extensible without
adding Graphics 1.6 construction behavior to this port.

The additive C interface is `rl_render_criar`, `rl_render_geracao`,
`rl_render_quadro`, `rl_render_reset`, `rl_render_liberar`,
`rl_render_observacoes` and `rl_render_cache`. See the versioned
[header](../motor/include/rising_engine.h) for field layouts. Creation copies
all inputs. Rendering copies 480,000 top-down indexed8 pixels (800×600, stride
800) plus 768 RGB24 palette bytes into caller-owned reusable buffers. Palette
generation is explicitly 1; Cyclage is outside Graphics 1.5's surface contract.
No Rust pointer escapes. No filesystem access or Python projection is needed
per frame. Full projection remains an optional proof/debug interface.

A world generation changes on every successful state load, isolated routine or
frame phase. The renderer requires the exact AffGame-entry generation after
phase 1 or phase 3 and rejects phase 2. Repeating the same generation and HUD
flag returns the same committed result. Capacity queries update only required
sizes/metadata; neither output buffer nor cache advances. ABI failures publish
nothing. Full, undrawn and partial are distinct successful outcomes; partial
publishes only the actual drawn prefix/cache and names the first original
callee/address. Reset copies explicit surface/cache inputs and clears the
previous-generation result. Freeing the world invalidates its renderer calls;
renderer release remains available. All native calls share one registry lock.

Phase 2 remains the sole owner of display-related logic effects. Rendering
reads the entry world, uses local overrides in original write order, and
exports ordered changed-byte and raster observations without applying them to
the world. BatimentEstHabiter reads the actual structure bag and live unit
kinds internally. The default display tick follows the published Python read
contract, not a host wall clock. Native renderer validation and throughput
results are recorded in the stage handoff after the measured runs.

The completed [Stage 3 proof](../motor/validation/stage3/summary.json) establishes
**128/128** chained own-world surfaces equal to Python and the original full
surface hashes, with carried cache, palette and effect equality and no world
mutation. The input-time matrix has **113/113** complete native surfaces equal;
the damaged-sanctuary case retains its expected **0x4085CB** stop. All 26
perturbed stop/prefix cases match Python. The uninterrupted M2.3 run renders
**9,200/9,200** complete surfaces with hashes equal to the original, with no
stop or first difference. The ABI 1.3 logic regression stays 257/257 equal.

The exclusive release [Swift/Metal client](../motor/validation/stage3/swift-metal.json)
measures **248.64 render fps** and **61.22 engine+render+Metal fps** (16.33 ms
per frame), including copied output buffers, GPU upload/conversion and GPU
completion, excluding initialization, proof work and app UI/display pacing.
It verifies 128 native indexed hashes and complete first/last RGBA readbacks.
The supplied native path exceeds the 25 fps target; app UI integration remains
with the macOS owner. No app source or acceptance record is changed.

Both gates pass: engine fmt/strict Clippy, 27 Rust tests, 57 Python discovery
tests plus seven isolated renderer checks, C/Swift/Metal interoperability;
prepared common check 1,881 tests with 610 optional skips. Detailed proof scopes,
unchanged native source identities, exact commands and remaining 1.5 boundaries
are in the [handoff](../motor/HANDOFF.md).

## Reference isolation and Graphics 1.7 — ABI 1.4

Engine tests consume exact Git revisions, independently of the integrated
working-tree Python. `motor/testes/pinned_reference.py` materializes a read-only,
ignored reference tree from logic revision `7ceeff9` (the version ported) with
only Graphics overlaid from `ce441852bcada750a8f91da8ed3302f1668c4405` (1.7).
Both sources and fixtures come from Git objects, including transitive imports;
every cached tracked file is checked against its immutable Git blob identity.
The frozen catalog still verifies the linked original asset payloads. Python
source pins and copied-definition AST tests read this revision tree. Original
capture/policy pins continue checking the actual immutable checkout evidence.
A legitimate upstream Python update therefore needs no engine pin refresh.
Tests demonstrate live-source independence and rejection of evidence/snapshot
corruption. Missing pinned commits require fetching them; no cache, reference
payload or commercial media is committed in motor/.

The renderer now ports Graphics 1.7 construction progress/full/gray facades,
selected builder construction bodies, order markers, CAVE placement shading,
tooltip measurement/frame/background save and next-frame restoration. ABI 1.4
keeps all 1.3 signatures and layouts; explicit creation at 1.0–1.3 remains valid.
`rl_render_contrato()` identifies Graphics 1.7 separately. The additive
`rl_render_fundo_salvo()` copies actual saved background bytes; observation
kinds 3/4 describe write-only background output and the exact text request.
Reset clears carried background; creation/restoration can read an explicitly
declared original background buffer. Rendering still leaves world state
unchanged and never applies display effects on top of phase 2.

Graphics 1.7 does not reconstruct glyphs: default rendering retains the named
`AffText 0x459454` stop after drawing the native tooltip background. The P1/P2/P3
full-window evidence declares that original routine non-executed. The offline
Rust fixture runner supports only that explicitly recorded contract, verifying
every text/font/rectangle/flags argument and the entire pre-text surface hash.
The production C ABI cannot install this adapter. Qualified full-window results
and normal production-prefix results are reported separately. Graphics 1.8
windows and glyph reconstruction remain outside this port.
