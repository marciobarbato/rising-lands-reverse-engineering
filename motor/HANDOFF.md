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
structure dispatcher0x4281c7, iaCalculPlayer0x47f927, iaSolver0x47d314,
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
