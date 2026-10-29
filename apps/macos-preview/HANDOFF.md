# Playable macOS consumer handoff

Owned paths: root `compilar-jogável`, this app directory, and
[`docs/MACOS_PLAYABLE.md`](../../docs/MACOS_PLAYABLE.md). Implementation base:
`5e2bf0831d3aaa776481a6ab023be262ef0df1bd`. No other owner's implementation or
shared workstream helper is changed.

The existing shell, engine, UI and portable runtime packager are extended.
Normal builds pin fetched main once and archive Git blobs, including current
domain providers and the app itself. Development builds are separate. See the
manual for exact provider inputs, callback ordering, unsupported inventory,
source manifests, controls and build/run commands.

The live synthetic exercise integrates navigation, resource extraction/deposit
and bounded direct type-0 attacks on one world and shared balances. It does
not claim native transport dispatch, full InfligeDegat, production/spawn,
visible death, audio, mission loading or campaign fidelity. The default lethal
consumer stop is retained, with no retry or invented completion. Graphics use
only verified base bodies and explicit unsupported-state markers.

## Actual validation before integration

Development build `43a016c062e2a3384d4acc4da95b665888b9a77a` passed **29 consumer
tests**, including six new integration checks over shared state, repeated
combat, the lethal boundary, interrupting attack, rejected inputs, the bounded
message guard and same-revision imports. One obsolete preview test expected a
missing structure grid; it now checks the current provider's successful route
while retaining the historical expectation for historical preview snapshots.
The new exercise suite is explicitly skipped by historical preview builds.

The actual ARM64 bundle and bundled CPython 3.12.14 passed source/asset hashes,
isolated runtime/import paths, source binding, signature and architecture
checks. Native LaunchServices/WKWebView validation passed **25 checks**. The
new tests use actual DOM unit buttons, destination form submission, speed and
play/pause buttons, with the real interval pump enabled. The constructor
collects at `(4,9)`, deposits at `(2,12)`, food changes 30→31; the soldier
contours the wall to `(9,4)` and two direct hits change enemy health 100→60.
The screenshot records tick 464, one delivery, seven remaining supply units,
two hits and an empty Python stderr. The window is visible, not a headless
browser or captured-command replay.

Exact development outputs:

* Bundle: `/Users/marcio/git/Rising Lands/local-data/macos-playable/dist/development/RisingLands-ptbr.app`.
* Evidence directory: `/Users/marcio/git/Rising Lands/local-data/macos-playable/build/development/43a016c062e2a3384d4acc4da95b665888b9a77a/build/logs/`.
* Reports: `consumer-tests.log`, `native-smoke.json`, `native-process.log`,
  `architecture.log`, `codesign-verify.log`; native images `native-smoke.png`,
  `native-smoke.before.png`, `native-smoke.after.png`.
* Before/after PNG SHA-256:
  `9964cac5f9d41b2ad7066fa83c93e889bbe1088ca9c52ecdb05d84f289a775c4` /
  `cde6859e73d27414fecd0b324840c25cdff15176fbb3bb3b6987441dfe9d38ee`.

Failed candidates are preserved. Initial direct sandbox app launch produced no
smoke report; LaunchServices in a graphical execution context opened the
window. The next check exposed file-URL canvas readback taint. Native WK
snapshots replaced that readback without changing WebKit security settings.
The corrected build then completed all UI interactions and checks above.

## Merged-main timer regression and correction

The coordinator preserved failed merge candidate
`67f97a6408498929ede841bd07f2a6f511e91d79` without pushing app main. Common
checks, 29 consumer checks and package verification passed, but the native
soldier movement wait expired. Its screenshot proves running 8× at tick 384,
soldier `(9,5)` with progress 20/32 toward `(9,4)`, no blocked state, worker
delivery complete and empty Python stderr. The fixed update quantum depended
on timely WebView interval callbacks; the failure was not a pathfinding result
or a completed movement falsely reported as success.

Corrective implementation `12e0223e973acc92f65841d72a7dc619a20a204f`, based on
the coordinator-updated feature `6194c849a693f7799b816ce5be40c73c3f52b401`,
uses monotonic elapsed time only for the live exercise. It retains the old lab
quantum, bounds one-response catch-up to one second and resets the time anchor
on pause/play/speed changes. Native failures now include live clock, unit,
pause, focus and visibility diagnostics. No timeout or security setting was
relaxed and no research provider changed.

**30 consumer tests pass**, including a new independent scheduling regression
for 100 ms and 1 s callback spacing, pause/sleep and the catch-up bound. **27 native
checks pass** after a real 900 ms interval without engine pump requests, then
the original DOM movement/delivery/combat flow. The initial corrected run
records tick 577, two hits, enemy life 60, one delivery and a measured maximum
pump interval 0.992624333 s, with empty Python stderr. Source, assets, signature,
architecture and relocated runtime paths pass again. Evidence directory:
`/Users/marcio/git/Rising Lands/local-data/macos-playable/build/development/12e0223e973acc92f65841d72a7dc619a20a204f/build/logs/`.
The failed candidate's logs remain under its separate 67f97a6 directory.
Two additional actual native launches also passed all27 checks:
`native-repeat-2.json` records tick579 and maximum interval1.007242709s;
`native-repeat-3.json` records tick575 and interval1.016723542s. Both retain
paired native captures and process logs, complete the same delivery/two-hit
flow and have empty Python stderr. These are repeat checks of the corrective
timing concern, not extra native reverse-engineering executions.

The new native test includes the delay to reproduce the scheduling condition;
it still uses actual wall time, DOM controls and the running interval, rather
than replaying an expected fixed number of pump commands. Its native before/
after PNG captures continue to verify real rendering without canvas readback.

No new recovered native algorithm or domain x86 execution is claimed. Original
executable identity/interval evidence remains in each committed provider's
handoff. Research totals are not aggregated into a game-fidelity percentage.

The coordinator must review/integrate this clean feature under the common Git
lock with an isolated merge candidate and full checks. The four-domain helper
must not be called with an invented app domain. Final delivery requires a new
normal build from verified fetched `origin/main`, recording its actual revision
in the local build/source manifests. Integration/main-output evidence is sent
after that build rather than predicting a future merge SHA here.

## Independent M3 preparation (2026-10-29)

The independent clone and dedicated `feat/codex-macos-m3-preparation` branch
add an immutable M1 consumer and command-line inspector. See the
[contract and runtime/Graphics dependency requests](M3_CONTRACT.md) and
[audit](M3_AUDIT.md). This is a validated inspection boundary, with future
frame application explicitly stopped before mutation. It introduces no
recovered behavior, renderer, input protocol or formal milestone acceptance.
The existing native shell continues to expose the synthetic exercise.

The accepted capture is read in place using the existing Missions decoder;
all 881 original-name/address blocks (2,659,375 bytes) match that decoder.
Consumer tests cover deterministic ordering, immutable bytes, rejection of
malformed payloads/metadata/hashes/ranges, atomic failure, idempotent load,
reset/reload identity and the M2 dependency stop. No original-x86 run is
needed or claimed for this read-only adapter.

Actual independent validation on Apple Silicon, Python 3.9.6:

* New consumer suite: **11/11 passed, zero skips**. Inspector CLI succeeds.
* `git diff --check` and documentation link validation: passed.
* Full app test discovery: 14 tests, 3 import errors (missing generated
  `apps/macos-preview/snapshot.json`); the 11 new tests passed.
* Common `scripts/check.py`: failed. Core 490 tests / 7 errors / 226 skips;
  Combat 260 / 1 error / 147 skips; Economy 487 / 1 failure / 7 errors /
  205 skips; Missions 104 / 1 failure / 22 errors / 31 skips; AI/runtime
  82 / 7 errors / 23 skips; Audio 20 / 8 errors / 3 skips. Graphics did not
  run (missing hash-checked CD files). Workflow **8/8 passed**.
* Observed missing inputs include MONDE01.ETA, RISING.EXE, capstone, unicorn,
  pefile and audio media. The two assertions also depend on missing media
  (38-map inventory and opening the original CRT stream). These failures
  are recorded, not changed or suppressed by this delivery.
* No native bundle build/UI smoke was run. The existing launcher derives
  shared `/Users/marcio/git/local-data` from the independent clone parent,
  outside this task's isolation scope, and required local runtime/CD inputs
  are absent from the clone. No existing bundle or Claude local data was used.

Detailed results and log hashes: [M3 validation](validation/m3-preparation.json).
This boundary is implemented and tested as an inspection consumer; common
checks and native application delivery remain incomplete. Runtime/Graphics
contracts remain the stop for further state/frame integration. The coordinator
reviews and integrates the remote feature; this task never merges/pushes main.


## Round-1 packaging correction

Coordinator integration found that the playable verifier correctly required
`src/macos_state_consumer.py` in the bundle, but both builders had fixed copy
lists that omitted it. Both now use `build.copy_preview_sources` to mirror
Python modules and UI assets, including the consumer and playable session.
Source verification remains strict. The playable runtime check also imports
the bundled consumer and loads all 881 accepted M1 blocks from its declared
archive. The shell's behavior and bundle identity are unchanged.

The deployed consumer resolves its default source root from its adjacent
`snapshot.json` relative archive; it refuses missing/invalid declarations and
paths escaping the payload. Explicit roots and checkout loading remain
supported. Consumer errors and CLI help are now English. Contract version 1
and the evidence identity are unchanged.

18 consumer/packaging tests pass with zero skips. The seven new regressions
exercise the actual source-copy helper and source verifier, reproduce the
original omitted-module failure, retain tamper detection, and run a relocated
consumer in isolated Python against the real M1 evidence. They cover valid
bundle defaults, missing archives/declarations, malformed manifests, traversal,
absolute paths, escaping symlinks and explicit roots.

Real launcher attempt: `./compilar-jogável --development-ref HEAD` at
`38ed65b2565c15f031b59660d7271dcd59d30097`, exit 1. To preserve isolation,
a local validation clone of that commit was created under the independent
clone's ignored `.local/bundle-validation/workspace/checkout`; its launcher
writes only under that temporary workspace, not shared host local-data.
No launcher or other domain files were modified.

The first stop is missing relocatable CPython 3.12 ARM64 at
`.local/bundle-validation/workspace/local-data/macos-preview/dependencies/python/bin/python3`
(and `lib/python3.12`). `RISING_PYTHON_RUNTIME` can declare a compatible runtime.
The temporary workspace also lacks the entire `source/cd` tree, including
`INSTALHD/PLATGAME.PIE`, `INSTALHD/GRAPHICS/BLOCS.CMP`,
`INSTALHD/GRAPHICS/TROOPS.CMP` and `WORLD/MONDE01.ETA`.
Native compilation, signing, full bundle runtime verification and UI smoke
were not reached. No existing Claude runtime, media, bundle or local data
was read or modified. Integration must rerun the real build with these inputs.

The full app discovery was rerun: 21 tests, 3 import errors due to missing
generated snapshot.json; all 18 independent consumer/package tests passed.
Documentation links and git diff --check pass. Unchanged cross-domain common
checks were not repeated; their previous failed prerequisite results remain
recorded above.

Preserved logs: [targeted tests](validation/m3-packaging-fix-tests.log),
[real build attempt](validation/m3-packaging-fix-build.log),
[full app discovery](validation/m3-packaging-fix-full-tests.log).
These regressions verify the packaging omission and bundled source resolution;
they do not constitute a native application build or UI smoke pass.

## Round 2 — accepted M2.2 playback and independent native inspection

Started only after fetched `origin/main` contained packaging correction
`fac29d6d0be7ee9e0aed41c2e8f3dc339adaab19`; verified base:
`c59781cdffafbd0f7120fd801293f9f7d589f39f`. The existing dedicated feature
was advanced by fast-forward. Only app-owned paths, the launcher and the
macOS manual are changed. No formal milestone is established.

Contract v2 retains M1 original-v2 inspection and adds separately labeled,
read-only M2.2 display-v2 playback. Inputs, widths, ordering, provenance pins,
atomic publication and identity are specified in [M3_CONTRACT.md](M3_CONTRACT.md).
No simulation provider is called or stubbed. The runtime comparator's unchanged
pure reader definitions are loaded by path without its simulation imports;
Missions' unchanged delta applier handles navigation. Images retain original
names, addresses and immutable bytes. LIVE apply_frame remains reserved.

The real capture verifies **257/257 summaries and 11/11 full checkpoints**.
[Per-phase report](validation/m3-m22-playback.json) includes observed words,
state identity and render status for every phase. All 257 render attempts stop
before calling Graphics at `missing_previous_surface`. The coordinator confirmed
that no previous-surface pixels exist in this capture and instructed this stop.
Thus this report records **zero actual Graphics calls, zero full/partial images**;
it must not be interpreted as rendered-phase validation.

Graphics API (1, 0) is pinned on import and result. Only Graphics supplies image
pixels and PNG encoding; its partial frame and named stop remain explicit.
The adapter has an unset surface-source extension point. No alternate surface
artifact, zero-filled fallback, habitation result or drawing code is invented.
Graphics' original-first initial surface, chaining rule and per-phase surface
hash verification (planned API 1.1) remain required. Version 1.1 is refused until
an explicit tested consumer change. Other Graphics scene gaps and live runtime
input/frame delivery remain external dependencies.

The AppKit/WebView shell now exposes a separate inspection page and isolated
worker, preserving the synthetic exercise. It supports phase/frame navigation,
reset, memory reads, block filtering, observed words and verification status.
Inspection pauses training. The existing game input commands are unchanged.
Both views have native smoke paths; no engine or renderer is added.

Build inputs are now explicit (`--inputs-root` / RISING_INPUTS_ROOT and
RISING_PYTHON_RUNTIME), with clone-local default outputs `.local/macos-playable`
and optional `--data-root`. CD/runtime inputs are read-only. The renderer's
catalog assets are copied and hash-checked into the bundle. Source mirroring
and the original bundle identity are preserved. See the manual for invocation.

Independent checks before the native build: 34 targeted tests passed, zero
skips, plus the separate real worker/bridge test passed (35 total). Tests cover
all API paths, corrupt/missing pinned inputs, order/checkpoint failures, atomic
failure, repeat/reset identity, reserved live delivery, Graphics API mismatch,
explicit surface stop and launcher preflight. These tests use real M2.2 evidence;
synthetic Graphics test outputs validate adapter branching only.
Native build and UI results are recorded after the committed-revision run.


### Round-2 committed native delivery

Implementation: `b4444f8e3e3031f0fb97aef1cec785305f38d680`.
Final native smoke/manifest change:
`2314804cbfe30f3866338284cc8141abf6493a86`.
The latter revision was built with the documented explicit input root and
RISING_PYTHON_RUNTIME; every generated file stayed inside the independent clone.
Original media and the source runtime were read-only.

**65/65 packaged consumer tests pass, zero skips** under bundled CPython 3.12.14.
Swift compilation, ARM64 checks, source/asset binding, relocated bundled runtime
verification and strict ad hoc signature verification pass. Native LaunchServices
runs passed **27 exercise checks and 8 inspection checks**, with visible windows
and empty Python stderr. The inspection smoke uses actual phase/frame buttons,
selector, memory form, block filter and reset; it checks the captured counter,
initial identity and explicit missing-surface state with no image fallback.
An earlier b4444f8 build also passed; the final smoke specifically strengthened
DOM coverage and native window visibility checks.

Bundle (local):
`/Users/marcio/git/Rising-Lands-Codex/.local/macos-playable/dist/development/RisingLands-ptbr.app`.
Full source/runtime/build manifests and prior bundles remain under this clone's
`.local/macos-playable/`. No native emulation was run by the macOS workstream.
No Mac mini execution is requested for this consumer.

Common checks were rerun and remain **FAILED**, independently of the successful
app build: Core 490 / 7 errors / 226 skips; Combat 262 / 1 error / 147 skips;
Economy 487 / 1 failure / 7 errors / 205 skips; Missions 104 / 1 failure /
22 errors / 31 skips; AI/runtime 90 / 11 errors / 23 skips; Audio 20 /
8 errors / 3 skips. Graphics was not run (its hash-checked fontes/cd absent).
Workflow passed 8/8, and documentation links/diff whitespace checks pass.
Those research suites use their own expected source/cd and optional
capstone/unicorn/pefile inputs, not the app's explicit inputs-root; no other
front was modified to suppress or repair those environment failures.

Preserved round-2 evidence: [consumer tests](validation/m3-round2-consumer-tests.log),
[exercise UI smoke](validation/m3-round2-native-smoke.json),
[inspection UI smoke](validation/m3-round2-native-inspection-smoke.json),
[build log](validation/m3-round2-build.log),
[common checks](validation/m3-round2-common.log), and
[structured validation](validation/m3-preparation.json).
Graphics 1.1 remains the render dependency. Runtime live delivery/input remains
reserved. The remote feature is delivered for Claude coordinator review;
this work establishes no milestone and never merges or pushes main.

## Round 3 — explicit Graphics 1.2 chained playback

Round 2 was not integrated: its Graphics 1.0 gate correctly rejected 1.2 on the
coordinator's candidate. Fetched main for this continuation:
`a7405668e630650f67f6ff792bd07348ae7697f7`, merged safely into the existing
feature at `7e771c4e9f46a22536a86f7d3331d1de74d9151d`. New implementation
changes stay in app-owned paths and the macOS manual. Other-front changes
arrived only through the main merge; no owner implementation is edited.

Contract v3 explicitly accepts only Graphics (1,2), checks both module/result,
and SHA-pins its initial surface, initial terrain cache and verification files.
Both initial loaders are the unchanged Graphics APIs. The cache never starts
cold, and navigation never loads an independent mid-sequence state: forward
seeks process every phase; backward seeks reset and replay from the start.
AffGame reads the preceding captured frame/load-tail state, not the ending
between_frames counter. The surface AND cache are carried after each draw;
frame(k) is undrawn and preserves both. RestoreAll/MenuInit output is supplied
by the original initial-surface artifact, not reconstructed by this consumer.

Read-only habitation is now supplied by the unchanged Economy predicates,
loaded as pure AST definitions with their actual constants and read methods.
They bind captured structure/unit bytes without constructing a synthetic world,
adding defaults or replacing any Graphics/Economy module. The original native
habitation reference is checked by consumer tests.

The completed [per-phase render report](validation/m3-m22-render-v3.json) verifies
257/257 memory summaries, 11/11 complete memory checkpoints, 128 Graphics calls,
and **12/12 applicable chained surface hashes**. Actual provider statuses are
**128 partial, 129 undrawn, zero full**. Every drawing phase preserves the
0x41591F stop for type 8 (then type 1). Graphics' own frame 6..12 references
still carry this stop although their first pixel difference is row 547; no
consumer silently promotes them to full. The HUD (rows >=544) and cursor are
not drawn, and no native pixel checkpoints beyond frame 12 are claimed.
The initial load_tail surface equals its recorded full-surface hash. Later
native phase-end/post-HUD hashes are reported for comparison, not treated as
successful complete-render checks.

The playback-service KeyError was confirmed as a secondary test failure: the
worker returned a valid error without a playback key after rejecting Graphics.
The service now checks Graphics before opening/publishing playback, returns an
explicit error_type, and tests assert response success before indexing. A real
isolated worker test with API (1,3) confirms the refusal response. Successful
response shape is checked by the client. Renderer/version/reference errors do
not publish a new inspection image. The native page shows actual PNG output,
partial/inherited stops, undrawn phases and all limitations; its DOM smoke uses
frame 12 while the separate report covers all 128 frames.

Targeted version/cache/sequence/error tests pass. The full committed-revision
consumer discovery, bundle build and both native smokes follow below after
execution with the coordinator's explicit inputs-root/data-root/runtime flags.
No live delivery, game input protocol, renderer or M2.3 work is added.


### Round-3 native results and review identity

Implementation/native-tested revision:
`12e534b03241ff64c6cf65fa2ae9f7c1d0bbdbe8`.
The full committed app discovery passed **71/71 tests, zero skips**. Strict
source mirroring, source/asset binding, bundled CPython 3.12.14 isolation,
Swift compilation, ARM64 architecture and ad hoc signature checks passed.
Native LaunchServices passed **27 synthetic-exercise checks and 9 inspection
checks**, with visible windows and empty Python stderr. The inspection test
uses actual DOM controls, reaches frame 12, checks PNG presence and the explicit
inherited stop/HUD limitation, reads original counter memory, filters blocks
and resets to the same captured identity. It no longer expects a missing surface.

Exact build command (from the independent macOS clone):

```sh
RISING_PYTHON_RUNTIME='/Users/marcio/.cache/codex-runtimes/codex-primary-runtime/dependencies/python' \
./compilar-jogável --development-ref HEAD \
  --inputs-root '/Users/marcio/git/Rising Lands' \
  --data-root '/Users/marcio/git/Rising-Lands-Codex/.local/round3-workspace/local-data/macos-playable'
```

The CD and runtime inputs are read-only; generated source archives, manifests,
runtime copies, assets, bundles and logs stay inside this clone. Bundle name
and identity remain unchanged. The normal launcher and explicit development
arguments remain supported. The prior failed candidate was not touched.

Saved [full discovery](validation/m3-round3-consumer-tests.log),
[exercise smoke](validation/m3-round3-native-smoke.json),
[inspection smoke](validation/m3-round3-native-inspection-smoke.json),
[build log](validation/m3-round3-build.log) and
[structured results](validation/m3-preparation.json) identify the real run.
Documentation links and git diff --check pass. Cross-front common gates were
not repeated in round 3; their prior environment failures remain historical,
not represented as a current pass. No native x86 emulation or Mac mini job was
needed by this consumer. Remaining dependencies are Graphics' unsupported
bodies/HUD/cursor and new reference/cache artifacts for independent starts,
plus the separately reserved live runtime/input contract. No milestone changes.


## Round 4 — native smoke readiness only

Fetched integrated base `8e90beb412a63d5f00965c381d21bc9a800257bc` includes
macOS f20d38a and Audio b4e8dae. The macOS feature advanced by fast-forward;
only app-owned robustness code/docs change. The Graphics gate remains (1,2),
with its existing refusal tests. No renderer/game/input feature is added.

The old native watchdog applied 45 seconds to window opening, asset/worker
initialization AND all interaction checks, and called tests immediately on
navigation completion. The new shell requires a validated explicit readiness
signal after actual dependencies load, plus native document/window readiness.
Window and checks each keep 45-second budgets; initialization has a distinct
90-second total-from-launch budget. Monotonic progress never renews a deadline.
Failure diagnostics distinguish window, initialization and check timeout. All
interaction assertions, local waits, before/after screenshots and failure JSON
are retained. Both UI modes now have paired native captures. Retries archive
previous evidence; the outer 165-second guard cannot replace a specific native
failure. Missing screenshots cannot result in a passing build.

The exact pure Swift lifecycle compiled into both native builders is tested
with a controlled monotonic clock, including readiness after the old 45-second
mixed deadline, missing ready/late ready, missing/late window and document/ready
ordering. Python tests cover retry preservation, outer failures and missing
captures. A smoke-only bounded delayed-ready flag permits an actual native
50-second initialization regression without stressing the workstation or
accepting an uninitialized app. Actual results for the committed revision follow below.

After this bounded robustness change, A waits for Claude's M2.3 publication and
M3 plan. C remains complete. No milestone or main integration is performed.

The legacy preview opener uses the same bounded runner and evidence archive;
its old outer 60-second guard no longer contradicts the shared shell's separate
readiness budget. This changes no legacy game behavior. The playable integration
build remains the authoritative native validation for this delivery.


The first readiness-aware run established actual readiness in 0.53 seconds,
then failed at the unchanged 45-second check limit. A diagnostic run retained
`lastProgress=final_animation_frames`, `visibility=hidden`, `paused=true`: all
interaction assertions and the after snapshot had completed. Occluded
WKWebViews suspend requestAnimationFrame even when NSWindow.isVisible is true.
The two smoke-only repaint barriers now await an actual native WebView
snapshot through the existing 15-second RPC deadline. Browser-only diagnostics
keep their animation-frame barrier. No assertion, real clock exercise or
check deadline changes. Both failed runs and their images remain preserved.


### Architecture handoff

The user's 2026-10-29 decision assigns real-time engine logic/rendering to Rust
through a C ABI and keeps Swift as the shell. Python remains the validated
reference, test harness and present inspection/playback dependency. No live
Python simulation plumbing was added. `apply_frame` remains reserved. See
[the pending native-engine boundary](M3_CONTRACT.md#native-engine-dependency--architecture-decision-2026-10-29).
Until the coordinator publishes the C ABI with the M3 plan after M2.3, there
are design notes only: no speculative loading, signatures or calls. Audio's
Python reference and captures are intended to support a later validated Rust
port, with device behavior still a declared boundary.


### Round 4 validation and review instructions

Built code revision: `7980efc3d4bb4e8f4417bf61441b41d3594ebf28`.
It contains latest fetched main `8e90beb412a63d5f00965c381d21bc9a800257bc`;
ancestry was checked again after the build. Earlier commits are
`1f5929c75b3695201a16a22c1f803186f703d8c5` (readiness and evidence),
`9464ea1` (legacy runner) and `9b648daf772522b79f8c70ddb9d0dc5b53b74652`
(last-assertion diagnostics). The final documentation/evidence commit records
these results without changing executable code. Review/integrate the feature
branch only; the independent writer did not merge or push main.

The coordinator's exact command passed, exit 0:

```sh
RISING_PYTHON_RUNTIME='/Users/marcio/.cache/codex-runtimes/codex-primary-runtime/dependencies/python' \
  ./compilar-jogável --development-ref HEAD \
  --inputs-root '/Users/marcio/git/Rising Lands' \
  --data-root '/Users/marcio/git/Rising-Lands-Codex/.local/macos-playable'
```

Full app discovery: **80/80, zero skips**, 46.702 seconds, including 9 new
readiness/evidence tests and existing Graphics version refusals. ARM64 app and
CPython 3.12.14, strict deep signature and relocated bundle verification passed.
Native exercise: **27/27**, ready 0.472 seconds, checks 9.488 seconds. Native
inspection: **9/9**, ready 5.978 seconds, checks 9.331 seconds. The unchanged
M2.2 suite/inspection verifies 257/257 phases and 11/11 checkpoints. Both native
smokes have empty Python stderr and paired before/after plus final PNGs.

A separate real native exercise held the valid ready signal for 50 seconds:
**27/27 passed**, initialization 50.884 seconds, checks 22.846 seconds, total
73.730 seconds, with the document still `hidden`. Thus initialization beyond
the old global45-second limit passes without extending the 45-second check
budget or bypassing any assertion. Missing/hung/late readiness remains a
bounded failure in the controlled-clock tests.

The two earlier check-timeout attempts are preserved, not reclassified as
passes. The second identifies `final_animation_frames` while the document
was hidden. That stage label remains stable in diagnostics; it now uses the
native paint capture barrier. All first/final images remain in clone-local
logs, with paths/hashes recorded in
[structured validation](validation/m3-preparation.json). Committed
[full discovery](validation/m3-round4-consumer-tests.log),
[exercise](validation/m3-round4-native-smoke.json),
[inspection](validation/m3-round4-native-inspection-smoke.json),
[delayed-ready](validation/m3-round4-native-ready-delay50.json),
[first failure](validation/m3-round4-failure-1.json),
[diagnostic failure](validation/m3-round4-failure-2.json) and
[exact build](validation/m3-round4-build.log) make the result reviewable.
No x86 emulation job was needed by A. Documentation links/diff checks pass;
other-front research gates were not represented as new A results.

A now waits for the coordinator's M2.3 publication, M3 plan and Rust C ABI.
Graphics stays exactly 1.2 with all prior stops/HUD/cursor/cache limitations
preserved. The separate Audio branch supplies a Python reference; its first
old-watchdog native failure remains historical and the coordinator should
rerun its merged candidate with this robustness fix. C requires no work.
There is no milestone claim, live frame plumbing or new game feature.


## Graphics 1.3 adoption — separate assets repository

Base `cb3e3245d919eee47b9c05b07a296032fd19a3e9` was fetched and fast-forwarded
into this dedicated macOS branch with a clean tree. The published additive
Graphics 1.3 contract retains all 1.2 signatures/formats and cache/pixel chaining.
Its normal bodies for types 1/8 remove the previous M2.2 unit stop. The consumer
now accepts exactly (1,3), refuses 1.2/1.4/other versions, and pins the committed
128-frame 1.3 reference. Current consumer contract is v4; source snapshot bytes
and accepted M1/M2 identities remain hash-pinned and unchanged.

The native page labels 1.3 and tests no inherited unit stop, retaining the
explicit HUD/cursor limitation. Generic partial-result tests remain in place
for records outside the provider domain. No renderer or live delivery was
implemented. Python remains evidence inspection/reference; the native Rust C ABI
is the future engine path, with the current apply_frame still reserved.

The large asset payload branch is not merged here. Asset data moves to the
separate public rising-lands-assets repository; this small app update uses the
existing explicit read-only CD/runtime inputs. Current full playback and exact
coordinator native-build results will follow after committed validation.

The full real-capture validation passed on implementation `0e10276`: 257/257
phase summaries, 11/11 memory checkpoints, 128/128 Graphics 1.3 chained hashes,
128 supported-playfield full results, 129 undrawn phases, zero partial results
and no named unit stops. HUD/cursor remain absent. See the new
[per-phase v4 report](validation/m3-m22-render-v4.json); older 1.2 reports remain
historical and unchanged. The exact committed native build follows separately.


### Graphics 1.3 native validation and integration handoff

The exact coordinator build passed on committed revision
`6d03502ba7140ce0f01c0243b1b3e6900b0d445b`, containing latest fetched main
`ea3175b2e903413d8d8bcde796d0910ff524af9f`. Implementation is `0e10276`;
subsequent commits record evidence/docs without changing executable code.

```sh
RISING_PYTHON_RUNTIME='/Users/marcio/.cache/codex-runtimes/codex-primary-runtime/dependencies/python' \
  ./compilar-jogável --development-ref HEAD \
  --inputs-root '/Users/marcio/git/Rising Lands' \
  --data-root '/Users/marcio/git/Rising-Lands-Codex/.local/macos-playable'
```

First attempt exit 0: **80/80 app tests, zero skips**, 47.870 seconds; ARM64
compile, bundled CPython 3.12.14 and strict deep signature/relocation checks
passed. Exercise smoke **27/27**, checks 21.514 seconds; inspection **9/9**,
checks 9.639 seconds. Both have visible native windows, validated ready signals,
empty Python stderr and retained before/after/final screenshots. Existing
readiness/check budgets were not changed. No new original emulation was needed.

The current [structured validation](validation/m3-preparation.json) includes
artifact hashes and screenshot paths/hashes. Saved
[full discovery](validation/m3-graphics13-consumer-tests.log),
[exercise](validation/m3-graphics13-native-smoke.json),
[inspection](validation/m3-graphics13-native-inspection-smoke.json) and
[exact build](validation/m3-graphics13-build.log) make the result reproducible.
No older report/capture was regenerated to adopt the new API. Full Graphics 1.3
chain verification covers all 128 drawing phases; complete post-HUD surfaces,
cursor, unsupported provider states and independent mid-sequence cache remain
outside this inspection boundary. Live delivery still awaits the native Rust
frame ABI; the published pilot routine ABI is not a live-frame implementation.

Review/integrate only feat/codex-macos-m3-preparation. The separate assets DATA
release and clean tooling branch are delivered independently. This app branch
does not include the old asset payload commits and claims no milestone.


### Final latest-main native refresh

Main advanced to `5fbef8252f5f63afcdbdaba56425da479073cec8` with a coordinator
common Rust-validation hook only. It was merged into this feature and the exact
coordinator build ran again on `585684fef34ecedeb904b97681421a7b2e85c63a`.
Consumer, Graphics and reference sources did not change. **80/80 tests, zero
skips**, 47.279 seconds; ARM64 compile/signature/relocation and native exercise
**27/27** plus inspection **9/9** all passed. No readiness budget or assertion
was relaxed. Earlier passing results remain preserved. Current
[full discovery](validation/m3-graphics13-latest-consumer-tests.log),
[exercise](validation/m3-graphics13-latest-native-smoke.json),
[inspection](validation/m3-graphics13-latest-native-inspection-smoke.json) and
[exact build](validation/m3-graphics13-latest-build.log) identify this final
merged checkout. Structured validation records all hashes and screenshot paths.
The final report-only commit changes no executable code. No merge into or push
to the code repository's main was performed.


## Graphics1.4 full HUD/cursor adoption

Latest main `ccbdcf0b1e6c35881fdd150ac7d3cc4ddc57fc38` was merged into this
feature after checking ownership and the clean tree. Graphics1.4 is additive:
default hud=False keeps1.3 pixels; this consumer explicitly opts into hud=True.
No Graphics implementation or other front is edited. Consumer contract v5
updates the render verification reference from pre-HUD to full800×600 phase-end.

Before rendering, the adapter reads every region from Graphics' own
regioes_necessarias(memory,hud=True), including minimap and five-player table.
It refuses missing/short regions, incompatible module/result versions and
chain/full-phase-end mismatches before publishing state. Unsupported HUD states
retain their named stops and can remain explicitly partial. Both pixels and
cache are carried in phase order; no independent start or fallback is added.

The1.4 full128 reference is hash-pinned. Tests cover HUD opt-in, both additional
regions, failed preflight without render/publication, full phase-end mismatch
even if the chain hash matches, future/older version refusal and HUD partial
stop inheritance. The real worker confirms the complete native frame1 surface
and original minimap/player regions. No original snapshot is patched or copied
to invent state. Full playback/native build results follow after validation.
