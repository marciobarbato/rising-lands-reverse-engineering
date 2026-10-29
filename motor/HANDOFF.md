# Rust engine pilot handoff

Workstream D owns motor/ and docs/ENGINE.md on feat/codex-rust-engine in the
independent Rising-Lands-Codex-Engine clone. No other front was edited; no
merge into or push to main is performed. This is a pilot, not a frame engine or milestone.

The original-first audit was committed separately as b7dfcdd. The five routines
are Random 0x4704dc, LongRand 0x45841b/CRT rand 0x48c51d, IntToBCD 0x467cd1,
and BCDToInt 0x467d3a. Original executable identity is
6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb.
Existing captures and Python references are read-only, SHA pinned; no original
emulation or asset copy is required. See the [audit](research/PILOT_AUDIT.md).

The core uses semantic RNG/BCD values, a checked sparse original-address
projection with explicit load/project and opaque uninterpreted bytes, integer
virtual ticks and explicit wrapping arithmetic. The registry-based C ABI 1.0
uses copied caller buffers, typed seven-data-GPR calls, opaque u64 handles,
transactional publication and named failures. The C header and Swift CLI smoke
are in include/ and testes/. The full API/limits/versioning and reproduction
commands are in [ENGINE](../docs/ENGINE.md).

The differential requires every selected captured call: Random 24, LongRand 12,
rand 12, IntToBCD 19, BCDToInt 8, total 75 records. Nested LongRand/rand observations
are counted separately. It compares every declared byte, changed-byte triples,
seven data GPRs and 48 captured RNG transitions against original and unchanged
Python. Python BCD providers are void; their separate scratch-register adapter
is grounded in the static original review, not a Python return value. Caller
stack writes are included without filling unobserved bytes. Synthetic aliasing,
u16 round-trip, wrapping and ABI error tests do not extend native-capture claims.

Remaining work: full world/frame initialization and orchestration, actual
frame-step/input ABI, generation-stable memory/render snapshots and lifetimes,
indexed 800x600 output/palette convention, native library loading/signing and
bundling, timing calibration, later original-asset packaging, and whether a
shipped app keeps Python. The pilot default 20Hz is pacing policy only. The
current macOS live apply_frame remains reserved; the app was not changed.
Projectiles and Rust rendering are deliberately outside this pilot.

## Validated delivery

Latest fetched/merged main is `a7427fd0e416d212f08af7f0df3d36a224d12f2d`;
ancestry was checked before and after validation. Original-first research:
`b7dfcdd1ad9a72cd6816c3c4ac34efd981028d0e`. Initial implementation:
`347383f22ad27709476c1ea5c29063eaaf8351eb`. The final projection-invariant
fix and tested code is `550b4f26d3c087e10d8258ed00ec95ec96cf982e`. The subsequent documentation/
evidence commit adds these results without changing executable code.

`./motor/validate.sh` passes: rustfmt; Clippy with -D warnings; **16 Rust tests,
16 Python tests, zero failures/ignores/skips**; **75 captured records with zero
mismatches**, including 48 explicit RNG checks. The C11 header layout check
and an actual Swift 6.4→C ABI→Rust CLI run pass. The latter creates/frees a
world, copies a seed, draws 16807, checks projected bytes and advances the
virtual clock to 1000ms. No app files or runtime were modified.

Toolchain: **rustc 1.99.1 (58cf8f9c3,2026-10-13), cargo 1.99.1**, target
**aarch64-apple-darwin**, LLVM 23.1.1, Apple Swift 6.4. Rustup stable and
format/lint components were installed only into clone-local ignored .local/;
no shared runtime or shell configuration was changed. To repeat with a normal
rustup installation, run the manual's commands. For this isolated installation:

```sh
export CARGO_HOME="$PWD/.local/cargo"
export RUSTUP_HOME="$PWD/.local/rustup"
export PATH="$CARGO_HOME/bin:$PATH"
./motor/validate.sh
```

[Structured summary](validation/pilot-v2-summary.json),
[all 75 call records](validation/pilot-v2-differential.json),
[full validation log](validation/pilot-v2-validation.log) and
[toolchain](validation/toolchain.log) preserve exact results and identities.
Generated dylib/CLI remain under ignored motor/target; their sizes/hashes are
recorded in the summary. The crate workspace has no external dependencies.
Reference source/capture hashes must still match; an upstream change requires
an explicit audit and pin update rather than silent acceptance.

No projectile port, rendering, full-frame delivery, performance claim or new
original emulation is included. The existing macOS apply_frame remains
RuntimeContractPending. The coordinator reviews/integrates the feature branch;
no merge into or push to main was performed.

The final review also tests the Rust projection boundary against adding or
removing typed fields without corresponding captured bindings. Such changes
now raise ProjectionFieldMismatch instead of silently publishing stale template
bytes. All 16 Rust and 16 Python tests, 75 original-call comparisons, formatting,
strict lint, header layout and Swift client pass again from latest main plus
that committed fix. Earlier v1 reports remain historical and unchanged.

## Final latest-main refresh

The coordinator advanced main to `3579c40ad455564f2a9b32c9a01b815b24d68f87`
with Core native-hook tooling. It was merged cleanly into the engine feature
at `668571f9b065ac4fa579ef53ed0384261e89a723`. Engine sources remain exactly
`550b4f26d3c087e10d8258ed00ec95ec96cf982e`; the eight reference/capture pins
and generated dylib hash are unchanged. This carries upstream Core commits
without editing any Core file in this workstream.

The full `./motor/validate.sh` was rerun from that committed merged checkout:
**16 Rust tests, 16 Python tests, 75 original captured records, zero failures/
skips/mismatches**, plus rustfmt, strict Clippy, C header layout and the actual
Swift client. The clock/projection/source scopes remain unchanged. Current
[summary](validation/pilot-latest-main-summary.json),
[75-record comparison](validation/pilot-latest-main-differential.json) and
[full log](validation/pilot-latest-main-validation.log) supersede the earlier
reports only for delivery-baseline identification; historical results remain
preserved. The final metadata commit does not modify executable code.

## Stage 2a — native frame logic (2026-10-29)

Branch `feat/codex-rust-engine`, fetched/merged baseline
`d9f70bab2506fea55f6cb0ad926290fed3803595`. Ownership remains motor/ and
`docs/ENGINE.md`; Python references, original evidence and published policies
are unchanged. This delivery is a proof for coordinator review, not acceptance
or a merge into main. Stage 2b starts only after this stage is pushed.

### API, state and supported domain

ABI **1.1** preserves all 1.0 entry points and adds frame phases, ordered event
observations, bulk copied projection, actual freed-byte projection and isolated
provider comparisons. The complete pointer/size/version/input contract is in
`include/rising_engine.h`. Frame input is 72 bytes: cursor, offscreen address,
eight entry registers, saved EDX/ECX/EBX and MSG words. No Rust pointer escapes.
Inputs and outputs are transactional on error. Phase1 (load_tail, including
frame0) and phase3 each advance one virtual tick; phase2 does not. Host pacing
never changes arithmetic. Frame3 return EAX is intentionally unspecified, as in
the accepted evidence; its preserved registers and ESP+4 carry forward.

GameState owns semantic unit/structure vectors and named frame globals when
the complete declared mission pools/globals are present. Explicit bindings
project these values onto the retained original layout. Unmodeled bytes stay
opaque. Mechanical providers execute on a private projection transaction and
reload semantic state only after success. This is an incremental semantic port;
terrain, Bags and every AI table do not yet have complete semantic Rust models.
Sparse isolated fixtures remain sparse; absence is never a fabricated mission.

Supported proof domain is the accepted no-human-input MONDE01 display scenario,
from display-v2 MissionLoad S0 through the load tail, window loop and frame1.
Four intact original jump tables are explicit immutable inputs. The library
executes native Rust; no Python callback, emulator or expected-state replay is
used to produce its state. Read-only expected deltas are replayed separately
by the comparator, which checks all reference checkpoints before comparison.

Routine families: CalculGame and player loop/CalculNextReflect; inactive
players and empty task VM; monster timing; InputGame/no key, InputSend,
MouseZone/scroll/rain, MenuInit/load path, message/icon timers; unit and
structure dispatch and reached idle/inhabited production branches; collision,
fatigue, visibility queries; research, resource presentation, alliances,
sympathy, market counters and field growth; NextAnimTerrain/NextAnimVeget,
world/CRT RNG and shared permutation cursor; TestFinDeMission/influence;
ProjectileAnim and effect lifetimes; guarded display logic effects/HUD.

Mutation and host-effect order is the Python chain's original order:
load-tail restore/clipping/counter reset/menu/bank frees/zones/frame0;
between-frame display effects/flags/boundaries/message poll/counter advance/
cursor; frame player loop/input/messages/game counter/icons/projectiles/units/
structures/research/alliances/fields/material/market/animations/sympathy/end
condition. DeleteBank frees each sub-buffer before its entry, clears the header
count, then frees table and header. Every MemFree emits Handle/Unlock/Handle/Free.
Actual bytes at free are retained for independent freed_sha256 validation.
No callbacks cross the ABI; unported paths fail by name and original address.

Original executable SHA-256:
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Principal addresses: CalculGame0x42c868, unit dispatcher0x456db5,
structure dispatcher0x4281c7, iaCalculPlayer0x47f927, iaSolver 0x47d314,
MenuInit0x4682bb, AffGame0x417698, DeleteBank0x418a12, TestFinDeMission0x458606.
Capture/mask/source identities are pinned in `testes/frame_differential.py` and
provider tests. See `research/FRAME_AUDIT.md` for exclusion and observation scope.

### Validation scope and results

The full stage2a report records **3/3 phases equal**, **16,097,242 compared bytes
in each phase**, **zero mismatched bytes**, unchanged exact display mask
(78,093 bytes/8,780 ranges), equal RNGs and all 597/2/13 bindings and3/2/1
boundaries outside display. All25,482 final allocation records are equal,
including146 freed buffers hashed from actual Rust output. Eight between-frame
registers are equal. The report also checks immutable input tables, virtual
ticks and rejection of actual projected-byte/binding-result/boundary-register
corruptions. Exact source/library identities and timing are in the committed
report; committed-revision reproduction is recorded below after execution.

The native engine gate covers fmt, Clippy-Dwarnings, Rust semantic projection
and pilot tests, Python provider/ABI/harness tests, all75 pilot captures,
C layout and a real Swift1.1 client exercising a successful frame phase.
Selected isolated frame-provider capture records are not independent missions:
Core773, Economy132, AI8 and Input/Missions10; historical sparse captures use explicitly synthetic
surrounding bytes, compare all captured changes/defined returns and compare
whole fixtures with unchanged Python. Perturbed cases exercise animation/RNG,
resource presentation, field growth, message timers, command clearing, monster
timing and target/occupancy scans. Whole-mission equality comes from the full
phase report, not these synthetic fixtures.

The requested `python3 -B scripts/check.py` was run under the heavy lease in
this clone. It failed on local prerequisites, not a Rust assertion: missing
`../source/cd` (mission media/intact executable), linked Graphics `fontes/cd`,
and Unicorn. Core, Combat, Economy, Graphics, Missions, AI/runtime and Audio
reported errors/dependency failures; workflow passed. The unmodified checker
and references were not patched to hide these missing inputs. The preserved
common-check log records the actual errors/skips. Coordinator reproduction in
a prepared checkout is needed for the common gate. Fresh x86 emulation and
the long128-frame Python composition are not rerun here; committed intact
original evidence is the oracle for this port.

### Remaining boundaries

Active AI kernels/task instructions, monster spawning/raids, moving/combat/
transport unit branches, completed production SortieTroupe, invention effects,
alliance expiry, nontrivial market contacts, and other unported branches stop
explicitly. No fallback is installed. Rendering/pixels, player orders, sound
playback, app integration and historical tick-rate calibration remain separate.
The display-effect provider is restricted to the original sampled-origin/type2
structure domain. Native frame throughput measures phase execution only,
including projection transactions, excluding Python corpus parsing/comparison,
rendering and app pacing. Stage2b full128-phase evidence/timing follows in its
own delivery. No Mac mini run is needed for the offline Rust corpus; any fresh
original emulation or long Python re-composition remains coordinator work.

### Committed stage 2a reproduction

Implementation commit `8a46430` was reproduced from a clean committed tree.
[Full proof](validation/stage2a-frame-proof.json) records3/3 equal phases,
16,097,242 bytes/phase,0 mismatches and no source changes during execution.
[Summary](validation/stage2a-summary.json) links exact hashes and counts.
The debug phase-only rate was4.23frames/s including initial load-tail overhead;
release128-frame throughput is measured in stage2b.

[Engine gate](validation/stage2a-engine-gates.log):21 Rust tests,39 Python tests,
75/75 pilot records,923 selected frame-provider records and592 perturbed
comparisons,0 engine failures/skips; fmt, strict Clippy, C layout and Swift1.1
frame smoke pass. The requested common checker log is preserved losslessly as
`validation/stage2a-common.log.gz`:1,574 tests run,64 errors,2 dependency-related
fixture failures,651 optional skips; Graphics not run for missing linked
inputs. A prepared coordinator checkout must rerun that gate. No main merge
or acceptance was recorded.

## Stage 2b — 128-frame release proof (2026-10-29)

Stage 2a was pushed at `9ff8aef` before this run began. No engine code changed
for stage 2b: implementation remains `8a46430`. From clean committed `9ff8aef`,
the release library passes [all 257 phases](validation/stage2b-128-frame-proof.json)
(load_tail plus 128 between/frame pairs), with **16,022,275 compared bytes per
phase and zero mismatches**. The exact cumulative policy masks 153,060 display
bytes in 4,948 ranges; its 999 observed logic-changing bytes stay compared.
There is no first divergence, dependency stop or crossing. All 257 replay
summaries and recorded full-state checkpoints, immutable original tables,
RNGs, bindings/boundaries outside display, eight between-frame registers,
carried registers, virtual clock increments and event corruption rejection
checks pass. All 25,482 allocation records equal the accepted reference,
including 146 actual freed-byte hashes. Original identities are unchanged.

**Performance:** Apple M4 Pro, 24 GiB, 12 logical CPUs, macOS 27.0.1; aarch64
Rust release with overflow checks, exclusive heavy lease over slots 0–5.
Native phase execution totals **1.068210955 seconds for 128 frames:
119.83 frames/s**, about 8.35 ms/frame. This includes startup/frame 0,
between-frame effects, private projection transactions and semantic reload.
It excludes exported snapshots, Python replay/comparison, rendering and app
pacing. The full proof takes 36.71 seconds including oracle checks. The task's
Python baseline (~0.5 s/frame, ~2 fps) was not rerun; the native phase rate is
approximately 60 times that reported baseline, with different measurement scope.

[Release validation log](validation/stage2b-release-validation.log) records
39/39 Python tests against the release dylib and
[75/75 pilot capture records](validation/stage2b-release-pilot.json), with zero
mismatches/skips. The earlier 21 Rust tests, fmt/strict Clippy, C layouts and
Swift 1.1 frame smoke remain valid because engine sources are unchanged.
[Stage 2b summary](validation/stage2b-summary.json) records source/library/report
hashes and timing scope.

The common checker still requires the prepared media/Graphics/Unicorn setup
described in stage 2a. No fresh original emulation or full 128-frame Python
composition was run. No Mac mini run is needed to finish the Rust evidence
proof; coordinator common-gate reproduction in a prepared checkout remains,
and any fresh long Python/original run should use the Mac mini. All named
unported branches listed above remain explicit stops. This is logic-only
workstream delivery; project acceptance and playable-app integration are separate.

Reproduce under the heavy lease (use exclusive mode for comparable timing):

```sh
cargo build --manifest-path motor/Cargo.toml --workspace --locked --release
python3 -B motor/testes/frame_differential.py --m22 --frames 128 \
  --library motor/target/release/librising_engine.dylib \
  --executable '/path/to/cd/INSTALHD/RISING.EXE' \
  --output .local/engine-128-new.json
```

## Stage 2c — implementation and proof contract

Baseline main `406823a` was merged into this feature branch. This stage owns
only motor/ and docs/ENGINE.md. No merge into main or acceptance decision is
performed. Original executable identity remains
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

ABI 1.2 is additive: explicit creation at 1.0/1.1/1.2 is supported, previous
signatures/layouts/status values and the 72-byte phase/event structures remain.
New isolated testing IDs cover task/rules, Core movement/spawn/path, and
Combat projectile creation. The frame entry, clock, register and transactional
publication contracts are unchanged. Existing no-human-input host answers
remain explicit inputs from the same display scenario. No renderer is added.

The original resolved RULE instructions at 0x514910 and entry table 0x51a720
are read from captured state. The native VM implements task/free/context lists,
child/wait/result control flow and reached rule operations. Monster groups,
battle/arrival rules, creation/placement/type/owner initialization, minimap,
orders, physical step/turn/animation, occupancy/region changes, route selection,
contour candidates, optimization and exact shared search scratch are ported.
Primary addresses: AvanceMonstre 0x47b283, ConstruitGroupeMonstre 0x47a81d,
iaSolver 0x47d314, DeplaceEngin 0x44930c, CheminCalcul 0x42f214,
Chemin_Verouille 0x43b30b, ProjectileInit 0x46e44c and ProjectileSet 0x46e208.
The owned audit/source pins and tests distinguish defined semantic returns
from unmodeled caller GPR leftovers.

Order remains the accepted phase chain: player AI executes before the game
counter and unit dispatcher; the first raid posts real tasks, creates its
unit/group and projectile, gives real orders, then the unit/projectile frame
families observe that state. Movement shares terrain/region grids and route
storage; path preparation, contours, candidate selection, optimization and
scratch stores follow the reference order. Buffers are original bindings,
not independently cached world copies. Every unsupported world callback or
rule raises a named original-address error; no no-op fallback is installed.

Semantic state now contains 46 unit fields, typed task/group pools, list heads,
counters, iterators and pending groups. Action records retain opaque backing
because their indexed span overlaps other globals. Sparse fixtures never gain
an invented runtime; bound presence/cardinality/list bindings are tested.

Missions Stage21 supplies ten original-only xz packages. Manifest SHA-256:
`e88dc3fcaca11d03a774dad8bd9c768345f13c884cc2d8df493107ec9d180b09`.
Policy SHA-256:
`384f985bea05137197ea22b3439f96db2f1e6b9a6d8b1a6c986f4955697fc21e`.
The cumulative mask has 153,060 display-only bytes; all unmasked bytes are
compared in each of 18,401 phases (1,560 observed changing logic bytes).
Each part starts from a declared full original opening and chains all its
phases. The aggregate rejects gaps, partial diagnostics, changed sources,
different libraries/policies or dirty source trees. Serial mode instead loads
hashed actual-Rust continuation checkpoints, never later reference openings.
The separate serial benchmark checks the final complete masked state and
records after an uninterrupted S0-to-9,200 native run; it is not a phase proof.

New isolated comparisons include 155 selected original Core records across
37 families (all available 9175–9180 records, plus the first four per family),
25 original raid-rule calls, three original Combat call records, and 942
additional perturbed/reference checks (176 movement/path, 320 groups/tasks,
446 projectile/timer cases). These counts are selected records,
not independent missions. Original callback effects are never replayed to
produce the Rust results. Final gate/proof results follow after committed runs.

Common-check preparation now uses workstream.py's ignored-link logic from the
prepared maintenance checkout to link media/Graphics inputs and missing local
Python packages, including Unicorn 2.1.4. Original inputs are read-only and no
tracked reference was patched. The prepared `python3 -B scripts/check.py`
passes all requested suites (1,860 tests run, 609 optional skips). This
supersedes the stage 2a/2b environment stop; the earlier log stays preserved.

## Stage 2c — completed evidence proof and delivery

Engine implementation commit `e87b943f45e5744b873424294a323bce77552b26`
proves **18,401/18,401 phases equal**, with **16,022,275 bytes compared per
phase and zero mismatches** (294,825,882,275 byte comparisons). The exact
153,060-byte display mask is unchanged; the 1,560 observed changing logic
bytes are included. There is no first divergence or dependency stop.
The [aggregate](validation/stage2c/proof.json), ten compressed per-phase
reports and [delivery summary](validation/stage2c/summary.json) preserve the
actual outputs. Every part ran from the same clean implementation commit and
release library SHA-256
`aa268176a7448fcae0f2f8de060ac8b0e6857a66bf2930a7327d971589ab3615`.

The completed phase proof uses the ten declared full original openings,
chaining every phase within each package. State/summary, RNG, bindings,
boundaries and allocation counts match in all 18,401 phases; between-frame
registers match 9,200 times and carried entry registers 9,191 times. There are
138,597 compared bindings, 27,603 compared boundaries and 587 matched shared
issuers. Display-context exclusions remain exactly the published policy.
All 25,482 final allocation records match, including actual retained bytes
for the 146 load-tail bank releases. Final world/AI RNG values are
`0x128b8024` / `0x3212b7ce`.

The separate [uninterrupted serial run](validation/stage2c/serial-benchmark.json)
starts at accepted M1 S0 and reaches frame 9,200 without importing a later
reference state. Its complete masked endpoint, RNGs, allocations and virtual
clock match (tick 9,201; 460,050 ms). Under an exclusive heavy lease it measures
**101.87 frames/s**, 90.3068 seconds of phase execution for 9,200 frames on the
Apple M4 Pro MacBook, including C ABI/Python call overhead and private state
projection/reload, excluding exported snapshots, comparison and rendering.
This is an endpoint/timing supplement, not a serial per-phase proof. The
task's Python timing baseline was not rerun. Each complete proof package ran
under a heavy lease with a 19-minute inner cap; the longest took 397.35 seconds.
No Mac mini run is needed for this native proof.

Main `ea62eb4`, containing the formal Python M2.3 proof, was subsequently
merged into the feature branch as `b3e72e0`. Its comparer change only adds
measured crossing diagnostics; the comparison helper ASTs remain identical.
The corresponding reference pin was refreshed. All native Rust/header hashes
and the release library remain identical to the completed proof. The
[formal-reference review](validation/stage2c/formal-reference-review.json)
checks matching evidence/policy identities, phase counts, event counts and
byte totals against the landed formal report. Original part reports retain
their original clean source provenance rather than being relabeled.

The refreshed [engine gate](validation/stage2c/engine-gate.log.gz) passes fmt,
Clippy with warnings denied, 25 Rust tests, 56 Python tests, 75/75 pilot records,
C layouts and Swift ABI 1.2 smoke, with no new engine skips. The frame-provider
tests cover 1,106 selected original records and 1,534 perturbed reference cases
in total. A new frame 0/1 regression remains 3/3 equal. The refreshed
[common check](validation/stage2c/common-check.log.gz) passes all eight suites:
1,881 tests run, 610 optional skips. Media, Graphics and Unicorn are available
through ignored links prepared with the repository helper; no reference input
was patched. Fresh original emulation and another full Python composition
were not run by this workstream; the coordinator's formal Python report was
reviewed instead.

Outside this proven no-input window, normal-player AI, normal-owner sight,
trap/crush/hunger/sound callbacks, further path continuation/unblocking,
player-4 alliance-mask resolution and damage/spell effects retain bounded
implementations or named original-address failures. Rendering, human input and
playable-app integration remain separate work. No acceptance is recorded and
no merge into main is performed.

Reproduce from a clean committed checkout. Each native command below is a
separate bounded job; package commands may run concurrently if the lease
permits it. Outputs must be fresh paths.

```sh
lease='/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py'
python3 "$lease" engine-stage2c-build -- \
  cargo build --manifest-path motor/Cargo.toml --workspace --locked --release
python3 -B motor/testes/frame_long_differential.py verify \
  --output .local/engine-9200-plan-new.json
for n in 0 1 2 3 4 5 6 7 8 9; do
  python3 "$lease" "engine-stage2c-part-$n" -- \
    python3 -B motor/testes/frame_long_differential.py part --part "$n" \
    --library motor/target/release/librising_engine.dylib \
    --output ".local/engine-9200-part-$n-new.json.xz" || break
done
python3 -B motor/testes/frame_long_differential.py aggregate \
  --plan .local/engine-9200-plan-new.json \
  --reports .local/engine-9200-part-{0,1,2,3,4,5,6,7,8,9}-new.json.xz \
  --output .local/engine-9200-proof-new.json
python3 "$lease" --exclusive engine-stage2c-serial-benchmark -- \
  python3 -B motor/testes/frame_long_benchmark.py \
  --library motor/target/release/librising_engine.dylib \
  --output .local/engine-9200-benchmark-new.json
```

For a serial phase proof, add `--serial --checkpoint-out` with a fresh
checkpoint path to each `part` command, and `--resume` with the preceding
actual Rust checkpoint for parts 1–9; aggregate with `--serial`. This mode
requires every continuation hash to match. It is implemented and covered by
harness tests but was not the completed 18,401-phase run's scope. The serial
benchmark above is the completed uninterrupted S0 endpoint run.


## Stage 3 — native renderer implementation contract

This additive ABI 1.3 stage ports Graphics `renderizar_quadro` 1.5, including
HUD/cursor and input-time selection overlays, to Rust. Python providers,
original captures, assets and masks remain read-only. The original executable
identity is unchanged: `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
The app input contract reviewed is `docs/MACOS_PLAYABLE.md` on committed
`origin/feat/macos-playable` at `16918c0` (Renderer port input).

The C header defines create, generation query, render, reset, release, cache
export and observation export. Existing 1.0/1.1/1.2 creation remains supported;
old signatures/layouts and the 72-byte frame structures are unchanged.
`RlRenderResult` is 304 bytes; `RlRenderObservation` is 108 bytes on the
supported 64-bit host. Output is indexed8, top-down 800×600, stride 800, plus
256 RGB24 entries (768 bytes), copied to caller-owned reusable buffers.
`hud_flags=1` enables Graphics 1.5 HUD/cursor; zero ends at its playfield
checkpoint. The complete persistent cache is 1,024 key bytes, 270,336 raw
payload bytes and a cursor in 0..255. Creation/reset copy all inputs and never
invent a cold cache or blank prior surface. Callers provide initialization
with established provenance; proofs use Graphics' pinned original artifacts.

The renderer owns verified copies of six original CMP banks in catalog order,
PLATGAME.PIE and the original 256-byte shadow and lighting tables. All nine
SHA-256 identities are enforced at creation. It decodes original row RLE with
an explicit opacity mask: literal zero remains opaque. It draws opaque terrain
blocks and destination-remap masks, preserves cache-hit stale payloads and
replacement order, selects/sorts units/projectiles with the original unstable
tie rules, interleaves scene passes, draws terrain objects and tree layers,
inhabited sanctuary facades, supported normal unit bodies and fatigue icons,
projectiles, input overlays, HUD counters/icons/minimap/target/cursors in
reference order. BatimentEstHabiter reads the actual structure bag/live units.
AffBatimentOmbre is the original literal RET; no unknown callback is replaced.
No original-effect stream, Python callback or host wall clock enters rendering.

AffGame 0x417698 enters after phase 1/3 and before phase 2. World generation
increments on successful state writes, separately from virtual ticks; an exact
generation and eligible phase are required. Stale generation is additive
status 11. Repeated generation+HUD flags is idempotent. All calls use the same
registry mutex. Undrawn output preserves the previous surface/cache; partial
output retains the actual drawn prefix and first original-address stop.
Size queries change only required-size metadata. ABI errors publish no frame,
cache or world writes. World release invalidates its bound render operations;
renderer release remains available. Reset copies explicit initial data and
clears the last-result generation. Palette generation is static 1; Cyclage is
outside the 1.5 surface contract.

Phase 2 retains sole ownership of display effects that affect logic. Rendering
uses local overrides and exports ordered changed bytes/raster calls, without
writing the world or consuming RNGs a second time. Diagnostic DD lock/surface
pointers use the same explicit software binding as Python; only 0x4E17A4 and
0x508F70 retain the public reference's process-local pointer exclusions when
checking native DGROUP. Other effects, cache cursor and compared bytes are
checked. The default renderer tick follows Python's published copied-tick
contract; isolated native leaf fixtures bind their observed GetTickCount.

Renderer reference identities are pinned in
[test pins](testes/render-reference-pins.json). Graphics' ambiguous flat
`construcoes` import is isolated in a fresh test consumer process, so it cannot
replace Economy's provider during the engine gate. Only motor/ and
`docs/ENGINE.md` are edited. App integration/acceptance remain with the
coordinator. Final committed-run proof and timing results follow below.

The standalone `render_smoke.swift` client exercises the actual C structs,
generation/size errors and reusable Swift output arrays, uploads indexed pixels
and palette to Metal, converts to an opaque RGBA texture and waits for GPU
completion. It verifies all 128 indexed surface hashes and complete RGBA
readbacks for the first/last frames. Timing excludes initialization, proof
hashing/readback and app display pacing. This client does not modify the macOS
app. `motor/validate.sh` runs it against the debug library for correctness;
release throughput is measured separately under an exclusive heavy lease.
