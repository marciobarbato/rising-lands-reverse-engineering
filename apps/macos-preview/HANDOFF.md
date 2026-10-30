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


## Graphics 1.4 full HUD/cursor adoption

Latest main `ccbdcf0b1e6c35881fdd150ac7d3cc4ddc57fc38` was merged into this
feature after checking ownership and the clean tree. Graphics 1.4 is additive:
default hud=False keeps 1.3 pixels; this consumer explicitly opts into hud=True.
No Graphics implementation or other front is edited. Consumer contract v5
updates the render verification reference from pre-HUD to full 800×600 phase-end.

Before rendering, the adapter reads every region from Graphics' own
regioes_necessarias(memory,hud=True), including minimap and five-player table.
It refuses missing/short regions, incompatible module/result versions and
chain/full-phase-end mismatches before publishing state. Unsupported HUD states
retain their named stops and can remain explicitly partial. Both pixels and
cache are carried in phase order; no independent start or fallback is added.

The 1.4 full 128 reference is hash-pinned. Tests cover HUD opt-in, both additional
regions, failed preflight without render/publication, full phase-end mismatch
even if the chain hash matches, future/older version refusal and HUD partial
stop inheritance. The real worker confirms the complete native frame 1 surface
and original minimap/player regions. No original snapshot is patched or copied
to invent state. Full playback/native build results follow after validation.

The real full-sequence check passed on implementation cf8c15a: 257/257 phase
summaries, 11/11 memory checkpoints, 128/128 chained/full-native surface hashes,
and 257/257 phase-end surface hashes. Results are 128 full and 129 undrawn, zero
partial/named stops in accepted M2.2. HUD/cursor pixels are included. Every
drawing record declares the required minimap/player buffers from captured
state. See [per-phase v5 proof](validation/m3-m22-render-v5.json); old 1.3
reports are retained as historical. The exact committed native build follows.


### Graphics 1.4 delivery validation

The exact coordinator build passed on committed checkout
`b4e3b6266e21d64ce3a9c87961cae0702ce0e85c`, containing latest fetched main
`b3ebdfb93200cc8ac3563eb10128cf98dd07fa6b`. The latest-main merge added
Core selection/orders and the small separate-assets tooling only; Graphics
providers, reference hashes and this consumer did not change after the full
sequence proof. Implementation is cf8c15a; final evidence/docs commits change
no executable code.

```sh
RISING_PYTHON_RUNTIME='/Users/marcio/.cache/codex-runtimes/codex-primary-runtime/dependencies/python' \
  ./compilar-jogável --development-ref HEAD \
  --inputs-root '/Users/marcio/git/Rising Lands' \
  --data-root '/Users/marcio/git/Rising-Lands-Codex/.local/macos-playable'
```

First attempt exit 0. **82/82 app tests, zero skips**, 46.108 seconds; ARM64
app/bundled CPython 3.12.14, strict deep signature and relocated source/runtime
verification passed. Exercise smoke **27/27** (checks 11.907 seconds); native
inspection **9/9** (checks 6.597 seconds), including the full native phase-end
surface and enabled HUD/cursor. Both windows were visible, readiness signals
were validated, stderr was empty, and before/after/final PNGs remain preserved
with hashes. Existing smoke deadlines/assertions were not relaxed.

Saved [full discovery](validation/m3-graphics14-consumer-tests.log),
[exercise](validation/m3-graphics14-native-smoke.json),
[inspection](validation/m3-graphics14-native-inspection-smoke.json),
[exact build](validation/m3-graphics14-build.log) and
[structured results](validation/m3-preparation.json) identify the actual run.
The [complete phase proof](validation/m3-m22-render-v5.json) shows 128 native
full 800×600 matches and 257 phase-end matches. All 17 required Graphics regions
per draw are read from captured blocks, including 16384 minimap bytes and 100
player-table bytes. No live inputs or game state are synthesized.

The former HUD/cursor absence is removed; remaining limits are the published
HUD/body domain, static palette (not live palette cycling), and no independent
mid-sequence cache. Named unsupported stops remain visible. The reserved live
apply_frame/native Rust frame ABI is unchanged. This is accepted-evidence
inspection, not M3 acceptance. Review/integrate only this feature; no merge
into or push to main was performed.

## M3.3 groundwork — Rust live phases and Graphics 1.5 (2026-10-29)

Feature `feat/macos-playable`, integrated base `c08e1fb96bf06392aec13ddde2bac29eb29a4ee0`.
No `motor/`, owner evidence, frozen hash, shared helper or main branch is edited.
Current consumer contract is v6; historical reports above remain unchanged.

`MacOSLiveSession.apply_frame()` now executes ABI 1.1 phases from accepted
**display-v2 S0**, using the Stage 2 initialization registers, cursor (0,0),
no keys/messages and four immutable original jump tables. Inputs, exact hashes,
copy ownership, mutation/publication order, reset/free and stop semantics are
in [M3_CONTRACT.md](M3_CONTRACT.md). ctypes bridges the real signed Rust dylib
in the isolated worker; no Python logic simulation is used. Swift owns the
native shell and save panel. The accepted original-v2 M1 inspector stays
separate. Legacy immutable playback guards still reject frame mutation.

Graphics 1.5 is explicitly gated on module and result. The full-HUD 128 proof
is pinned to SHA `d95618beff805b5e47c7be6ec922cdf9cda75c4063b0cd52c254a1a116e19c10`.
A regression compares every 1.5/1.4 reference surface hash. Preflight also
requires the new `[0x4e24bc]` 256-byte grayscale lookup. Rendering retains the
preceding live AffGame-entry image, previous pixels/cache, real habitation
callback and `hud=True`; no display effects are patched into engine memory.
Original executable identity remains
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Frame entry `CalculGame 0x42c868`, WndProc `0x4181a1` and the published phase
contracts are unchanged. This is consumer wiring of already-proved behavior;
no new reconstructed routine or x86 execution is claimed.

The actual [live proof](validation/m3-live-graphics15.json) reports **257/257
masked states, 11/11 checkpoints, 128/128 full native surfaces and 257/257
phase-end surfaces equal**, zero stops. Raw memory hashes are not claimed equal
inside the unchanged 153,060-byte display mask. Shared-host Python 3.9 timing:
Rust 1.140 s (112.26 frames/s), projection/hash/oracle 65.875 s, Graphics 25.622 s
(4.996 frames/s), PNG presentation 43.709 s, complete validated pipeline
**0.939 frames/s**. Initialization, IPC and native scaling are excluded; this
is not an exclusive-host peak or an M3.5 playable-speed pass. Per-phase timings
are retained in the report.

The [engine-only horizon](validation/m3-live-horizon.json) continues that S0
chain beyond 128 without new loads: frame 8999 and between_frames9000 return;
frame9000 stops honestly at **ABI status 5: ConstruitGroupeMonstre at
0x0047a81d**. Beyond 128 this diagnostic uses ABI calls only, without
snapshots/rendering/equality claims. It takes 85.474 s for the 8,871 additional
completed frame bodies. Live UI rendering has no fabricated reference past
128: verification fields become null, and either provider's named stop latches.

The record-only mapper covers messages 0x200–0x205 and all requested vkeys.
It preserves signed coordinates, scaled image position, message/modifier order,
held/release timing, poll addresses and per-poll answers. Raw journal replay
reconstructs the exact event/poll interleaving and rejects changed answers.
No event or order enters Rust. The native save panel exports the distinctly
named raw journal. At this stage Missions' scripted-input module has not landed
on fetched `origin/feat/re-missions`; the interchange exporter returns
`InputContractPending`, rather than inventing its schema. Test A/B original
replay remains dependent on that schema, captures and engine order support.

### Proposed next engine stage (proposal only)

Port Graphics' separable renderer into Rust behind a versioned C ABI that
accepts the engine's same-generation projected state and explicit asset catalog,
previous indexed 800×600 surface and terrain cache. Preserve clipping, signed
coordinates, wrapping widths, draw order, palette indices, real habitation
queries, cache payloads/cursor and ordered display effects. Return copied
indexed pixels/palette plus full/partial/named-stop metadata; define ownership,
stride, lifetime and reset. Validate every 1.5 native leaf case, then all 128
chained full surfaces and caches; preserve older no-input hashes. The engine
already models display effects: give one side ownership to prevent double
application. A native texture upload/palette conversion should replace per-frame
Python RGBA/PNG encoding and base64 WebView transfer. Avoid the current bulk
Python block/hash work on the production render path while retaining an
optional diagnostic projection/comparison API. A Rust draw loop alone would
leave two larger measured bridge/encoding costs. No renderer port is implemented
by this front.

Final committed build/common-check/native results will be appended below.

### Final committed native build and gates

Implementation `1ca070a7b3b096839a24a86da1eb16dca85d9e86` is followed by
`054f29a` (live memory reads retain the active Rust projection) and
`901b95cdae284a01d35752bc58dc288fa081a2fa` (validation resolves bundle source
identity from its adjacent manifest). The exact coordinator command passed at
**901b95c**, with `RISING_PYTHON_RUNTIME` declaring the existing relocatable
CPython root `/Users/marcio/git/Rising Lands/local-data/macos-preview/dependencies/python`:

```sh
python3 -B compilar-jogável --development-ref HEAD \
  --inputs-root '/Users/marcio/git/Rising Lands' \
  --data-root '/Users/marcio/git/Rising Lands/local-data/macos-playable'
```

The command ran through the required shared heavy lease. **93/93 consumer
tests pass, zero skips** (60.106 s). Native exercise **27/27** and inspection/
live **11/11** pass, with visible ARM64 windows, verified readiness, empty
Python stderr and unchanged budgets. The live smoke opens S0 and actually
runs the signed dylib through frame 1, verifying three masked states and the
full native surface. Native checks take 5.165 s and 9.698 s respectively.
Paired before/after/final images remain in the build logs; the final live
screenshot was visually inspected. Source binding, relocated Python/library
loading, architecture and strict deep signing all pass.

Bundle: `/Users/marcio/git/Rising Lands/local-data/macos-playable/dist/development/RisingLands-ptbr.app`.
Logs: `/Users/marcio/git/Rising Lands/local-data/macos-playable/build/development/901b95cdae284a01d35752bc58dc288fa081a2fa/build/logs/`.
Committed copies: [build](validation/m3-live-final-build.log),
[consumers](validation/m3-live-final-consumer-tests.log),
[exercise](validation/m3-live-final-native-smoke.json),
[live inspection](validation/m3-live-final-native-inspection-smoke.json),
[architecture](validation/m3-live-final-architecture.log),
[signing](validation/m3-live-final-codesign-verify.log), and
[Rust release build](validation/m3-live-final-rust-engine-build.log).

Common `python3 -B scripts/check.py` **fails prerequisites**, retained in
[full compressed log](validation/m3-live-common.log.gz): Core 532 tests /
5 errors / 214 skips; Combat 271 / 0 errors / 151 skips; Economy 503 / 2 errors /
207 skips; Missions 113 / 6 errors / 30 skips; AI/runtime 95 / 7 errors / 5 skips;
Audio 69 / 0 errors / 3 skips; workflow 9 / 0 errors / 0 skips. All 20 errors
are missing Unicorn imports; Graphics does not start because its worktree
`fontes/cd` copies are absent. Documentation links pass. No other front's paths
are changed to conceal these stops. Optional original-x86 recaptures remain
skipped; this consumer changes no reconstructed routine and uses the immutable
owner proofs instead. A preliminary targeted run also failed for missing
`RISING_INPUTS_ROOT`; declaring the actual input root then passed 61 tests.

The first bundled 130-frame diagnostic reached its final metadata step but
failed by querying Git in an archive; no result JSON was published. Its
[failure log](validation/m3-live-initial-bundled-validation-failure.log) is
preserved. The manifest-based source-identity correction above replaces that
assumption. The final bundled proof is recorded separately, never by editing
the failed run or a frozen reference. No original evidence is regenerated.

Remaining delivery gaps: Missions scripted-input schema/export adapter and
original Test A/B replay, engine order support/raid branch, Graphics' other
named stops, palette cycling and real-time performance. The 1.5 provider's
114 input-time display cases are accepted as its published domain, not claimed
as newly replayed M3 gameplay by this app. No main merge/push or milestone
acceptance is authorized or performed by this front.

Missions dependency request: publish the scripted-input module's exact field
names, frame/poll-site ordering, cursor coordinate convention, vkey result
width/sign rules and validation/import/export entry points. The last fetched
`origin/feat/re-missions` is `de154b5f22b7d30f7b1610e2c54cf684751e214b`;
`m3/entrada_roteirizada.py` is absent. The app must review that contract before
exporting a file labeled `rising-lands/monde01-scripted-input/1`. It currently
exports and deterministically replays its distinct raw journal only.

### Bundled runtime continuation and final rate

The final [bundled proof](validation/m3-live-bundled-130.json) uses the exact
901b95c archive, signed dylib SHA
`839ce4b7978a0fc0ab1aaed6752ed079e84805374e97339e3f0facaf93b2de53`,
and bundled **CPython 3.12.14**. It reaches **frame130**, with no stop:
257 accepted masked phases, 11 checkpoints, 128 full native surfaces and all
257 native phase-end surfaces remain equal. Frames 129–130 render completely
but have **null** state/surface equality fields because no reference is pinned
there. This validates actual continuation without fabricating verification.
The separate engine-only horizon remains the frame9000 dependency result above.

Measured 130-frame pipeline: **1.155 frames/s** (112.559 s), split into Rust
**1.180 s / 110.15 frames/s**, projection/hash/oracle **51.170 s**, Graphics
**15.816 s / 8.22 frames/s**, and PNG presentation **44.378 s**. Initialization,
IPC and native scaling remain excluded; the machine was shared under the heavy
lease. The earlier Python 3.9 measurement remains preserved as a separate run.
The production renderer port must address projection and image transfer as well
as draw speed; the measured rate still fails the M3.5 playability target.

The final evidence/docs commit changes no executable app code after the 901b95c
build. Its [structured delivery](validation/m3-live-delivery.json) records
artifact and screenshot hashes. Feature push only; no main integration or
formal acceptance is recorded.

## Live pipeline performance follow-up (macOS-owned paths)

The accepted f508a52 delivery is preserved. This stage starts from integrated
`23dfd6e` and changes only the macOS front; the engine/Graphics reconstruction
is unchanged. The proposed C renderer interface is in
[Renderer port input](../../docs/MACOS_PLAYABLE.md#renderer-port-input).

ABI 1.1 `rl_projetar_tudo` has no region filter and always packs the entire
world. The adapter now calls it once per phase into alternating reusable caller
buffers (the second buffer preserves the last published state if later
projection/verification/rendering fails). Only Graphics' 18 declared regions,
1,746,372 bytes, are copied into two reusable read-only views. The 25,197 full
memory blocks are not copied into Python objects or rehashed individually.
Full masked state verification streams directly over the bulk projection;
expected hashes are prepared once from accepted evidence before stepping.
Views are serial leases until reuse, not immutable snapshots retained forever;
accepted M1/M2 playback remains immutable. Arbitrary current-address inspection
reads the last successfully published full bulk buffer. Layout/pointer changes
are revalidated, and missing ranges fail before render publication.

The same fast path runs in the UI and rendered proof. Raw presentation carries
800×600 indexed bytes and the original RGB24 palette in a versioned packet;
JavaScript reuses ImageData/palette/index buffers and calls putImageData.
PNG compression is absent from live transfer. It remains available through
explicit `validate_live_macos.py --png-output PATH` evidence export and the
unchanged immutable playback inspector. Economy's unchanged read definitions
and the hash-checked palette are cached per archive, not reparsed/reread for
every frame. No drawing algorithm or engine behavior is replaced here.

The initial 128-frame fast-path run passed 257 states, 11 checkpoints, 128 full
surfaces and 128 decoded raw-transfer surfaces. Every masked state hash also
exactly equals the preceding f508a52 proof. Preliminary rate: 7.623 fps vs
1.155 fps (bundled CPython 3.12, shared heavy lease). Final committed build,
raw native-canvas checks, phase/transfer timings and common maintenance gate
will be recorded below. This preliminary run used one bulk buffer; the final
implementation deliberately uses two to preserve failed-publication isolation.

A further app-owned C byte codec validates stable bulk descriptors and streams
SHA-256 over the same original-name ordering and mask spans using system
CommonCrypto. It has no game state, drawing, allocations or retained foreign
pointers. The reference Python codec remains the unit-test oracle; production
rendered sessions require the explicitly versioned helper, with a visible load
failure rather than an automatic fallback. The builder compiles and signs it
inside the normal app packaging path. Native smoke exercises the actual live
play/pause loop through at least frame 33, raw canvas readback and generation
matching, without changing the existing readiness/check deadlines.

### Final performance validation

Executable app implementation: `6e2f1a5` (persistent/raw path), `481407f`
(native byte codec) and `604046b2b6602cc73d6acea3fd78661465bf39c5` (failed
publication regression). The exact coordinator build passed on **604046b**:

```sh
RISING_PYTHON_RUNTIME='/Users/marcio/git/Rising Lands/local-data/macos-preview/dependencies/python' \
python3 -B compilar-jogável --development-ref HEAD \
  --inputs-root '/Users/marcio/git/Rising Lands' \
  --data-root '/Users/marcio/git/Rising Lands/local-data/macos-playable'
```

The existing heavy-lease wrapper covered the whole build. **99/99 consumer
tests pass, zero skips**, including the native codec against the independent
Python digest, raw roundtrip, malformed layout/spans, immutable view reads,
buffer reuse and failed-publication isolation. Compilation/signing/relocation
and source binding pass for Swift, CPython 3.12.14, Rust and the app-owned C
helper. The helper performs byte validation/SHA-256 only, not game logic or
rendering. No `motor/` source or Graphics owner source changed.

Native exercise **27/27** and inspection/live **14/14** pass. The latter uses
the actual play/pause loop from frame 1 to frame 33, checks every canvas RGBA
byte, confirms raw indexed transfer with no PNG and verifies phase generations.
It measures **8.470 fps including worker IPC, WebKit and UI updates** over 32
frames. Canvas decode/palette expansion/upload averages **1.176 ms**, maximum
3 ms over 34 presentations. Both visible windows have empty Python stderr;
existing readiness and 45-second check budgets are unchanged. The inspection
checks take 24.464 s, including one-time expected-hash preparation. Before,
after and final screenshots remain under the build logs; final PNG and native
canvas screenshots were visually inspected.

The final [128-frame proof](validation/m3-speed-fast-128.json) runs the archived
604046b sources with the signed bundled helpers and CPython, under the shared
heavy lease. A shared build-directory lock protects the bundle from replacement
during the run. **257/257 masked states, 11/11 checkpoints, 128/128 complete
surfaces, 257/257 phase-end surfaces and 128/128 decoded raw-transfer surfaces
match**, with no stop. All 257 actual masked state hashes also match the
preceding f508a52 proof exactly; no mask or historical artifact was altered.
Two ABI buffers and 36 region buffers are allocated once and reused across all
257 phase calls. Each view retains only **18 regions / 1,746,372 bytes**.
ABI 1.1 still exports the complete 16,175,335-byte world; server-side filtering
requires an engine API change and is explicitly requested by the renderer spec.

| Component | Previous bundled run, ms/frame | Fast bundled run, ms/frame |
| --- | ---: | ---: |
| Rust phase execution | 9.078 | 8.871 |
| Projection, full-state proof and region views | 393.614 | 25.520 |
| Graphics rendering | 121.661 | 64.422 |
| Transfer preparation/roundtrip (PNG → raw indexed) | 341.366 | 2.124 |

Worker pipeline throughput is **1.155 → 9.898 fps (8.57×)**. The preceding
bundled run has 130 frames, the new run 128; table values are normalized per
frame. Both use CPython 3.12.14 on the shared machine and exclude initialization,
IPC and native canvas presentation. The new transfer timer includes raw JSON
encoding/decoding and SHA-256 verification; the actual UI result above includes
the complete transport. The unchanged Python renderer now dominates; this is
below 25 fps, not a claimed real-time completion. PNG compression remains an
explicit evidence export outside the measured live transfer.

Common checks now **pass**: `/usr/bin/python3 -B scripts/check.py`, run read-only
from `/Users/marcio/git/Rising Lands/worktrees/maintenance`, using that repo's
`.local/python`. Maintenance revision observed before/after was
`4279ad8fe237a679253e4dfde976b4694b4fd1ee`. Suites: Core 532/210 skips,
Combat 271/151, Economy 503/207, Graphics 248/0, Missions 137/33,
AI/runtime 95/5, Audio 79/4, workflow 9/0: **1,874 tests, 610 optional skips,
zero errors/failures**. Documentation links pass. No new original-x86 capture
is needed or claimed: only consumer transport/byte-codec behavior changes.

Saved [build](validation/m3-speed-build.log),
[consumer tests](validation/m3-speed-consumer-tests.log),
[native exercise](validation/m3-speed-native-smoke.json),
[native raw live loop](validation/m3-speed-native-inspection-smoke.json),
[common maintenance log](validation/m3-speed-common-maintenance.log.gz),
[architecture](validation/m3-speed-architecture.log),
[signing](validation/m3-speed-codesign-verify.log),
[byte-codec compilation](validation/m3-speed-macos-projection-build.log), and
[structured delivery](validation/m3-speed-delivery.json) pin actual outputs.
The [renderer spec](../../docs/MACOS_PLAYABLE.md#renderer-port-input) requests a
native, generation-checked indexed-buffer call with explicit palette/HUD/stop
semantics and a 40-ms total budget. Input/order support is unchanged by this
performance follow-up. Final evidence/docs commits change no executable app
code after the validated 604046b build. Only the feature branch is pushed;
main integration and acceptance remain with the coordinator.

## Rust renderer integration — ABI 1.3

This stage replaces live Python drawing and per-frame JSON pixels with an
app-owned native frame driver and a Swift/Metal game window. The same C driver
is called by the production window and by the proof harness. It owns the Rust
world and renderer, copies accepted S0 plus the four original jump tables once,
and invokes phase 1, then render at the exact entry generation, phase 2 and
phase 3. Rendering never applies display effects; phase 2 remains their sole
owner. Initial surface/cache and nine assets are explicit, hash-verified inputs.
Caller-owned indexed/palette buffers and Metal textures persist across frames.
No captured state after S0 is ever loaded into the world.

The driver audits all 257 M2.2 states and 11 checkpoints on live startup and
all reached surfaces through frame 9200. Full M2.3 state auditing is a proof
mode over the identical stepping/render calls, without a different simulation
path. It exports the actual engine world/renderer handles only to proof tools;
Python rendering, cache and observation comparisons are test oracles, never
part of live drawing. ABI/status/generation and host buffer layouts are gated
explicitly. Missing ABI 1.3 or Metal produces a named visible error. Reset
creates a new valid world/renderer before replacing the old one. Errors latch
the first named stop; the app never fills unknown state or synthesizes frames.

Development is explicitly authorized against read-only engine revision
`363faa9c252ffb00d62c81db0da2ee5d4a3d7615`. Its release library was built into
this front's ignored target directory, not the engine worktree. Tested library
SHA-256: `fe1aa558cbb1d597a8ba79cce40ee1cbb576a3b6b40139076e1b5b79a8b1c5e1`.
The [development serial proof](validation/m3-abi13-development-proof.json)
passes **18,401/18,401 masked states, 11/11 M2.2 checkpoints, 9,200/9,200
surfaces and 128/128 Python surfaces**. It carries one actual world from S0
through frame 10,800. Its first stop is phase 2 of frame **10,801**:
`ABI 5: Display monster count at 0x0041591f`. Total leased execution is 406.969 s,
including full-state exports/comparison. No state reset or package opening is
used during that run. The native UI displays the same latched driver error.

Main's concurrent Graphics integration is **API 1.7**, not 1.6. Its reviewed
additive contract changes optional text and construction/tooltip branches;
normal rendering retains named glyph stops without installing the probe-only
text adapter. The evidence inspector/oracle now explicitly accepts 1.7 and
pins its native 128-frame report SHA
`4448aeb44920d89b271e9af276477ee545fe797164b5b654e26c18a545d1a16c`.
A regression compares all 1.7/1.5 no-input chained/full-surface hashes. New
required gray/tooltip/background regions are preflighted through the published
API. This **does not expand Rust's Graphics 1.5 domain** or claim CAVE/glyph
support in the native renderer. No Graphics owner file is edited.

The builder defaults to integrated `motor/`. While ABI 1.3 is pending main,
`RISING_MACOS_ENGINE_SOURCE` may explicitly select the approved engine repository
for a development build only. The builder archives the immutable 363faa9 Git
object into its own build directory; the external checkout may advance without
changing that input. Native binaries and all
prepared inputs remain inside the declared ignored data root. No implicit
library fallback or uncommitted source snapshot is accepted. Final integrated
builds, GPU readbacks, real-window throughput and common gates follow below.

### Final native validation and delivery

Exact coordinator development build **869ffaa22db49105c39c31444790b4648551a886**
passes with the explicitly approved engine-source override. Both the builder
and all native/proof runs use the shared heavy lease; each execution is below
20 minutes. The builder archives 363faa9 from the external engine repository
read-only. The external checkout and both `motor/` trees are unmodified.
The linked Rust static archive SHA-256 is
`8b089afc9d1a92330c376dbdd62f155a6603377f01b796a11a56e393858faf7d`;
the signed bundled shared library used by proof tools is
`3b98ff15054128b2ced4dee51ed3fb60402ae5affeb289b4d618146e286de713`.
The [structured delivery](validation/m3-abi13-delivery.json) also pins the live
Swift executable, native driver, input manifest, build manifest and logs.

The [final bundled Python comparison](validation/m3-abi13-final-prefix.json)
passes **257/257 states, 11/11 checkpoints and 128/128 full surfaces**, plus
128 Python surface/palette/cache/ordered-effect comparisons. Python is only
the test oracle. The [final actual native-window horizon](validation/m3-abi13-native-horizon.json)
passes **18,401/18,401 states and 9,200/9,200 surfaces** using the same statically
linked production driver and visible Metal view. It completes frame **10,800**,
then displays the first named stop at frame **10,801**:
`between_frames · quadro 10801 · ABI 5: Display monster count at 0x0041591f`.
No reset, evidence-state loading or surface substitution occurs in that chain.
The entire full-state audit takes **420.244 s, 25.699 fps**; the preceding
1486c82 run also passes in 409.110 s at 26.399 fps. Both final GPU readbacks
check every one of 1,920,000 displayed pixels; the horizon PNG SHA-256 is
`62de37f3e04ed53174dc64f6ae6fe65cb1dc82e95a1bb4a1f1d9cb6bdf7f860c`.

The [normal native live smoke](validation/m3-abi13-native-inspection-smoke.json)
measures **40.914 fps**, 406 frames / 9.923 s, including the required startup
proofs and all reached surface comparisons. Per frame: Rust logic **11.042 ms**,
Rust renderer/generation **4.451 ms**, proof export/hash **8.000 ms**, Metal
upload/presentation/GPU completion **0.921 ms**, other loop/notification work
**0.027 ms**, total **24.441 ms**. Host projection belongs only to proof/debug;
native rendering has no Python pixels, per-frame JSON/PNG or Python IPC. The
previous real Python/raw-canvas UI measured 8.470 fps; its 9.898-fps worker
measurement excluded IPC/native presentation. Frame counts differ and the
machine is shared. GPU PNG evidence is exported after pausing, outside timing.

The [build](validation/m3-abi13-build.log) passes **102 consumer tests, zero
skips**, **27 native exercise checks** and **16 inspection/live checks**.
Source/asset binding, portable isolated Python imports, relocated runtime,
ARM64 architecture and strict deep signing pass. Existing 90-second readiness
and 45-second check budgets remain unchanged. The initial dynamic-link build
passed signing verification but failed LaunchServices startup because hardened
DYLD library validation rejected the ad-hoc dylib's Team ID. Its
[failed log](validation/m3-abi13-initial-dynamic-build.log) is preserved. Static
linkage fixes that failure while retaining hardened signing and adding no
library-validation exception. Another failed source-revision guard is recorded
in the delivery; immutable Git-object extraction fixes the advancing-checkout
race without editing or resetting the engine repository.

[Common checks](validation/m3-abi13-common-maintenance.log.gz) pass with
`/usr/bin/python3 -B scripts/check.py`, read-only in the maintenance worktree,
using its `.local/python`; observed revision
`b896665b39696bf3bc5ff90b3c6bf6446d06581c`. Core 545/211 optional skips,
Combat 279/153, Economy 513/208, Graphics 255/0, Missions 154/33, AI/runtime
109/7, Audio 79/4 and workflow 9/0: **1,943 tests, 616 optional skips, zero
failures/errors**. Owned commit paths/trailers, documentation links and
`git diff --check` also pass. No new original-x86 capture is claimed: these
app proofs compare unchanged original evidence and the Python oracle.

Final fetch still exposes main **c5988c4** with **ABI 1.2**. Consequently a
default integrated-main ABI 1.3 build remains **pending**, not passed. The
builder defaults to archived integrated `motor/`, with the visible named
`RustRendererABI1.3NotIntegrated` guard until its renderer lands; the temporary
external override is development-only and never an implicit fallback. Native
input/orders and M3.3 Test A remain unsupported; the prior inspection recorder
remains separate and injects no orders. Rust's Graphics 1.5 domain, later text/
input branches, Cyclage and the frame-10801 engine branch remain explicit gaps.
Only the feature branch is pushed; main integration and acceptance are left
to the coordinator. Final evidence/documentation commits change no executable
code after the validated 869ffaa build.

## M3.3 Test A — answer-stream half and native input recording

Implementation **96303fc**, focus/responder correction **ebacca2** (full validated
build `ebacca229f5fa72cdb3ab26d368e434c9c8e5979`), based on approved **1d29d81**.
No merge was performed for this task. The [input API contract](M3_CONTRACT.md#m33-test-a--frame-input-interchange-and-answer-stream)
specifies inputs, normalization, mutation/order and explicit failures.

`ScriptedInput(root, dict_or_json)` imports the actual Missions schema through
its unchanged pure validator and exports canonical JSON bytes.
`FrameAnswerMapper(script, hwnd=...)` takes explicit frame/phase/poll-site
requests and returns the declared cursor/key/message/translate/dispatch rows.
`MacOSSessionRecorder(root).event(frame, event)` records monotonic game-frame
mouse/key events; `export_script(stop_frame=...)` returns that validated script.
No wall-clock timestamps, Rust input calls, game-memory writes or WndProc flag
patches occur. Messages dispatch in order; cursor holds; keys reset per frame
and repeat their literal signed answer at every poll. Human key transitions
export held `-32768` values throughout Control/depot holds. Imported key/message
values remain literal, including K1's digit-1 WndProc message and the native
unlisted-vkey-0x45 zero polls. Legacy per-poll journals remain distinct.

The [six-probe proof](validation/m3-test-a-answers.json) uses the unchanged
original references for intact `RISING.EXE` SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
It records every source input/log hash and the owner module SHA-256
`57cb30f1fd6f947107de38ccc2de09874bdd94c4b465af7ea84b2704dbddf609`.
All 19 schema/input/summary/log Git blobs used here equal fetched main's blobs.

| Probe | Frames after 128 | Declared answers | First difference | Canonical byte round trip |
| --- | ---: | ---: | --- | --- |
| P1 | 501 | 7,522 / 7,522 | none | equal |
| P2 | 601 | 9,034 / 9,034 | none | equal |
| P3 | 3,001 | 45,032 / 45,032 | none | equal |
| P6 | 2,272 | 33,873 / 33,873 | none | equal |
| P7 | 3,572 | 53,099 / 53,099 | none | equal |
| K1 | 501 | 7,037 / 7,037 | none | equal |

All **155,597** answers match per frame, phase and original poll return site.
Native logs supply only requests, never expected answer bytes. HWND=0 is an
explicit scenario declaration, checked against all native dispatch records.
The sole omitted field is `wndproc_flags_after` (102 original-game outputs),
which belongs to Test A's deferred state half. No game-state equivalence under
orders is claimed. Each canonical export/import/export is byte-identical;
original files are read-only. The CLI `scripts/validate_macos_input.py` refuses
to overwrite its report and lists the first difference if any.

Native NSEvents are stamped on the engine's serial queue for its next frame.
Recording begins only after frame128. Starting recording focuses the Metal
view, observes initially held modifiers and records focus-loss releases.
**● Gravando entrada**, **Parar gravação** and **Exportar entrada** are visible
in PT-BR. Reset is disabled during capture. Stop/export drains native work and
the isolated worker chain. Errors latch visibly and prohibit successful export
of incomplete data. **Ordens ao vivo indisponíveis** stays visible; host events
never alter the no-input Rust structure. Fixed clicks use k/k+1/k+3, with cursor
holding and deferred subsequent moves; continuous human drags remain outside
this recorder's supported domain and are labeled unavailable.

The [exact coordinator build](validation/m3-test-a-build.log), using the allowed
read-only **363faa9 ABI 1.3** source override, passes **109 consumer tests, zero
skips**, **27 native exercise checks** and **20 inspection/live checks**.
Signatures, ARM64 architecture, asset/source binding, isolated portable runtime
and relocation pass. The native smoke now sends constructed NSEvents through
the actual AppKit window/responder chain, rather than calling view handlers
directly. It proves the visible native indicator, key focus, Ctrl hold, click
cadence and native atomic export. Rust remains on its no-input chain with
257 states, 11 checkpoints and all 410 reached surfaces equal. Real UI rate
is **39.097 fps**; no 9,200-frame engine rerun was needed for this input-only
change. The prior full-window result above remains historical evidence.

The [actual saved-file proof](validation/m3-test-a-native-export.json) imports
the complete actual Missions harness and accepts the exported bytes unchanged.
Move=407, down=408, up=410, Ctrl release=411; cursor=(400,272). SHA-256:
`39e9e1cce2c0455d12a0c637f24ff77053f4967ecf64ded9e2ab072c3bef4820`.
Its canonical byte round trip and all 283 input-schedule frames equal Missions'
own scheduler. These are **input schedules**, not game-state hashes. Production
uses NSSavePanel; automated smoke selects the explicit CLI evidence destination
and tests the same atomic save action. Human destination selection is not
automated. The earlier pre-focus build's passing artifacts are preserved.

[Common checks](validation/m3-test-a-common-maintenance.log.gz) pass read-only
from maintenance with `/usr/bin/python3 -B scripts/check.py` and its
`.local/python`; observed revision `c203400a833f44593a66d5fd5546532e746a19c7`.
Core 546/212 optional skips, Combat 279/153, Economy 513/208, Graphics 255/0,
Missions 154/33, AI/runtime 109/7, Audio 79/4, workflow 9/0: **1,944 tests,
617 optional skips, zero failures/errors**. An initial targeted worker test
failed before asset loading because RISING_INPUTS_ROOT was unset; the declared-
input rerun and both complete builds pass. The failed setup log is preserved.

The [delivery manifest](validation/m3-test-a-delivery.json) pins library,
artifact and source hashes. Main advanced to **d1ff3e0 / ABI 1.4** while this
task ran; this delivery deliberately keeps testing the explicitly authorized
363faa9 library, with no new ABI acceptance or main merge. Adopting ABI 1.4
remains separate. Test A's WndProc effects/whole-state half requires engine
order support; no orders were injected. Test B's 3,000-frame human original
replay and new original-x86 captures were not run. No M3 acceptance is recorded.
Final evidence/documentation commits change no executable code after ebacca2;
only `feat/macos-playable` is pushed non-forcibly.

## Integrated ABI 1.4 and Graphics 1.8 adoption

Merged fetched main **ef52cb0** into the front at **091aee2**. Implementation
and validated APP_BUILD commit: **e760756c44f79950cedc146ac17654b19c2d18c0**.
Only owned app sources/manuals are changed; `motor/`, pinned references,
provider implementations and original evidence are unmodified. The standard
workstream preparation helper creates only ignored read-only input links.
Build/test caches remain ignored. No main integration or acceptance occurs.

Both ctypes and native consumers now require **ABI 1.4 / 0x00010004**. Native
creation also checks `rl_render_contrato()==0x00010007`, the Rust Graphics 1.7
domain. The checked C layouts and caller-buffer lifetimes are unchanged;
generation query → read-only render → phase2 → phase3 ordering is preserved.
Phase2 alone owns game display effects. The Swift binary statically links the
same reviewed ABI and app driver, keeping hardened signing. The temporary
363faa9 override is retired explicitly; APP_BUILD uses integrated `motor/`
from the identical immutable source archive as the app, not another checkout.
ABI/capability errors and render stops remain visible and named.

The isolated Python inspector/oracle explicitly accepts **Graphics 1.8** and
pins its 128-frame HUD report SHA-256
`613ec2348b7fe0d597690ca4601af7f825c0d227133cdddc6b10e822e8eee845`.
The consumer regression checks all 128 chained/full-surface hashes against
1.7. The owner declares no new callback or heap region; the existing actual
Economy habitation reader covers CAVE bags. Native labels/metadata accurately
retain Rust Graphics 1.7 rather than claiming the Python 1.8 extensions.
No glyph/text substitute, default habitation answer or order injection is added.
The [current contract](M3_CONTRACT.md#current-integrated-backend--abi-14--python-graphics-18)
supersedes the earlier development-backend notes.

The exact [APP_BUILD](validation/m3-abi14-app-build.log) command is unchanged:
`python3 -B compilar-jogável --development-ref HEAD --inputs-root
"/Users/marcio/git/Rising Lands" --data-root
"/Users/marcio/git/Rising Lands/local-data/macos-playable"`, with the existing
relocatable Python runtime declared and no external-engine override. It passes
**109 consumer tests, zero skips**, **27 native exercise checks** and **20
inspection/live checks**. Source/assets, isolated relocated runtime, ARM64 and
strict deep signing pass. Existing readiness/check budgets are unchanged.

The [fresh bundled live proof](validation/m3-abi14-live-prefix.json) passes
**257/257 masked states, 11/11 checkpoints, 128/128 original full surfaces and
128/128 Python 1.8 surfaces**, with palette/cache/ordered-effect comparisons
and zero observer failures. The production frame driver is the one under test.
The [fresh Test A proof](validation/m3-abi14-test-a-answers.json) retains all
**155,597/155,597 answers**, no first difference, and six byte-identical canonical
round trips: P1 7,522; P2 9,034; P3 45,032; P6 33,873; P7 53,099; K1 7,037.
Native poll logs supply requests only; WndProc output flags/state remain outside
the answer half. Original input/evidence bytes and masks are unchanged.

The [real native UI smoke](validation/m3-abi14-native-inspection-smoke.json)
measures **41.386 fps** (401 frames, 9.689 s), with a visible Metal window,
required startup proofs and actual presentation. GPU readback matches all
1,920,000 displayed pixels. All 406 reached original surfaces are equal. The
input recorder still receives constructed NSEvents through the AppKit responder
chain, exports the literal frame file, and injects nothing into Rust.

[`sh motor/validate.sh`](validation/m3-abi14-engine-validate.log) passes:
fmt, clippy, **28 Rust tests**, **61 Python tests** plus **10 renderer child
tests**, **75 original-x86 differential comparisons / zero mismatches / zero
skips**, C header checks, Swift ABI interoperability and **128/128** Swift render
surfaces. The engine gate's library is debug; the measured application is
release. Its unchanged `pinned_reference.py` uses logic revision
`7ceeff909b52b7d4f59723f35dfe43a9deda41ff` and Graphics revision
`ce441852bcada750a8f91da8ed3302f1668c4405`, materialized/checked from Git objects.
Current Graphics 1.8 source never replaces that engine reference tree.

[Common checks](validation/m3-abi14-common.log.gz) also pass in this prepared
feature worktree using `/usr/bin/python3 -B scripts/check.py` and `.local/python`:
Core 561/213 optional skips, Combat 279/153, Economy 521/209, Graphics 261/0,
Missions 154/33, AI/runtime 112/8, Audio 79/4, workflow 9/0 — **1,976 tests,
620 optional skips, zero failures/errors**. All native/heavy runs used the
coordination lease and stayed below 20 minutes. No new original capture is
created or altered. The [delivery manifest](validation/m3-abi14-delivery.json)
pins libraries, inputs and result artifacts, including tested shared library
SHA-256 `7079b58383dba56bfd885883161a300650c697dd0053e38bb5dbb6c0364d556f`.

Remaining scope: Test A game-state/WndProc-effect half, Test B and order support;
continuous human drag capture; glyphs; Rust ports of the added Python 1.8
families. The 9,200-frame/first-stop horizon was **not rerun on ABI 1.4**; prior
ABI 1.3 results remain historical. Requested APP_BUILD, engine gate and bounded
live/Test A proofs pass. Final evidence/docs commits change no executable code
after e760756. Only the feature branch is pushed without force.

## Play mode and independent display scheduling

Work resumed after fast-forwarding the front and merging fetched main 8138e6e.
The integrated ABI1.4 / Rust Graphics1.7 / Python Graphics1.8 pins are unchanged.
Only macOS-owned paths are changed; no engine optimization is included.

The native driver defaults to validation for existing proof consumers. New
`macos_live_validation(driver,0)` must be selected before phase1, and removes
projection/hash/equality/observer work while retaining the real phase ordering,
caller buffers, renderer metadata checks and named stops. Input files, masks,
original hashes/addresses and evidence are unchanged. A new actual-driver
regression compares all 128 play-mode output surfaces/palettes and the final
whole projection to validation mode, while asserting zero callbacks/proof time
and rejecting mode changes after phase1.

The UI's Jogar mode uses a fixed host game cadence (20 Hz nominal default,
configurable independently) and asynchronous Metal presentation of the latest
complete frame. See the [manual](../../docs/MACOS_PLAYABLE.md#native-play-mode-and-independent-clocks)
for buffer ownership, scheduling and the original-rate dependency. A three-slot
pool releases textures only after GPU completion. Main thread handles AppKit
and resizing; engine initialization, frame work and display acquisition run on
background queues. Validar and APP_BUILD's validation smoke keep their audits.
Sustained real-UI measurements and gate outputs will be appended after validation.

### Validated results for play mode

The final executable source/build is **55cddc571ec75bf6b305aabd75c33d5697fa7471**;
subsequent evidence/docs commits do not change executable behavior. Exact
[APP_BUILD](validation/m3-play-app-build.log) passes **110 consumer tests / zero
skips**, **27 native exercise checks** and **20 inspection/live checks**. ARM64,
isolated relocated runtime/source/assets, static ABI1.4 binding and strict deep
signing pass. The app still uses integrated main's motor from its immutable Git
archive. Shared library SHA256:
`792edc2e0812b6a2636e1033f2235c5f89ce8b7336ccb825a1c45902d48fa6a1`;
static engine archive:
`8827032dfe15a6df294884ad2b63f8e4317db7818630237ed80ebff9f288a4a0`.
No other engine checkout or override is used.

Fresh [prefix proof](validation/m3-play-live-prefix.json) retains **257 states,
11 checkpoints, 128 original surfaces and 128 Python Graphics1.8 surfaces**, with
palette/cache/ordered-observation checks and zero observer failures. The new
consumer regression also checks 128 play-mode pixels/palettes and the final whole
projection against validation, while confirming zero proof work/callbacks. Fresh
[Test A](validation/m3-play-test-a-answers.json) retains **155,597/155,597** declared
answers: P1 7,522; P2 9,034; P3 45,032; P6 33,873; P7 53,099; K1 7,037. All six
canonical byte round trips match; no first difference and no orders injected.
An initial proof command used the builder's staging bundle path, which is moved
at delivery; its [setup failure](validation/m3-play-prefix-staging-path.log) is
preserved. The corrected proof uses the actual delivered bundle under the shared
build lock and checks its source commit before loading any library.

The [four 65-second UI runs](validation/m3-play-timing.log) use the actual
unoccluded native window and CAMetalDrawable presentation timestamps. Jogar gives
**119.920 fps average / 117 minimum one-second fps** at nominal 20 game frames/s;
**119.878 / 117** at 60.001 game frames/s; **119.919 / 117** at unlimited
**69.226 game frames/s**. No warmup bin is discarded, no proof work or publication
drop occurs, and final readback through the asynchronous texture pool verifies
all 1,920,000 pixels. Maximum excess main-thread timer delay is below 2 ms in
all play runs. No interpolation or synthetic game frame is generated.

Validar gives **63.210 displayed fps average / 25 minimum**, with the retained
startup prefix, 257 states, 11 checkpoints and **4,117/4,117 reached surfaces**.
Its first five full-second bins are 25,27,25,26,26; later bins 63–70. The short
APP_BUILD audit run is 44.252 displayed / 44.362 game fps; historical 41.386 fps
was also a short startup-audited sample. The manual separates those scopes.

Uncapped per game frame: Rust logic **10.313 ms**, Rust render **4.059 ms**, app
upload **0.059 ms**. Per display: CPU encoding **0.030 ms**, GPU **0.141 ms**.
Drawable wait is separate; asynchronous stages overlap. The app removes proof
and synchronous presentation costs. The engine remains the throughput limit;
state-reload cost is an engine-owner profiling candidate, not individually timed
here. The default is the documented 20 Hz nominal TickClock rate; the original's
actual timing remains unmeasured. Current no-input performance does not establish
raid/order or full-mission headroom, Test A state-half fidelity, or Test B.

[Engine gate](validation/m3-play-engine-validate.log) passes **28 Rust tests,
61 Python tests plus 10 renderer child tests, 75 original-x86 comparisons / zero
mismatches / zero skips**, C layouts, Swift ABI1.4 interoperability and **128/128**
Swift render surfaces with Metal. Its library is debug, so its throughput is not
an application release measurement. Logic/Graphics reference commits and original
hashes/masks are unchanged. All heavy runs use the lease; build+four timing runs
use an exclusive lease. Feature push only; no main integration or acceptance.

[Common checks](validation/m3-play-common.log.gz) pass from this prepared feature
worktree using `/usr/bin/python3 -B scripts/check.py` and its read-only linked
`.local/python`: Core 561/213 optional skips, Combat 279/153, Economy 521/209,
Graphics 261/0, Missions 154/33, AI/runtime 112/8, Audio 79/4, workflow 9/0 —
**1,976 tests, 620 optional skips, zero failures/errors**. Documentation links and
`git diff --check` pass. Every actual leased execution stays below 20 minutes.
The [delivery manifest](validation/m3-play-delivery.json) pins source, library,
benchmark and validation artifacts. Only `feat/macos-playable` is pushed without
force; no main merge or milestone acceptance is performed.

## Stage 4 consumer — ABI 1.5 input and orders

Resumed by fast-forwarding the feature and merging fetched main **2eadf69**.
Only app-owned sources/manuals change. The consumer accepts ABI1.5 explicitly;
Python Graphics1.9 acceptance is separately pinned, while Rust retains its own
Graphics1.7 domain. Original evidence, window policies and engine reference pins
remain unchanged.

Play now routes native mouse and keyboard events to the worker's bounded,
frame-addressed mapper and then `rl_passo_quadro_entrada`, after the real 128-frame
startup prefix. The existing recorder observes those events without applying a
second order. Input/file replay expands literal per-frame declarations through
`FrameAnswerMapper.declared_answers`; consumed engine poll sites check those
answers independently. Validation mode and old no-input tools retain their
previous hashes/observer/callback ordering. The new native mapper regression
compares human-event and scripted-descriptor worlds and frame registers after
every phase, including Ctrl hold/release and k/k+1/k+3 click scheduling.

The Test A state tool starts each world from S0, runs the real prefix and compares
P1/P2/P6 whole-state phases with the owner's pinned window reader and exact mask.
All six probes also compare the owner's declared indicator fields/unit-record
hashes, input answers including WndProc flag bytes, and order packets. It does
not claim whole-state coverage where no full-state window exists. Simulation
proof deliberately omits rendering so that an earlier Graphics dependency cannot
masquerade as the engine's frame-220/frame-141 stop.

Rendering, CAVE body execution, initialized audio and glyph dependencies retain
explicit named stops; wiring an order does not claim those providers are ported.
Human Test B and complete-mission playability remain outside this bounded proof.
Measured results and artifacts are recorded below.

### Integrated player-input build and preserved regressions

Validated executable/build **04dea3927ab4b9846f60a3d9a86c0b72cd2b59a0** uses
integrated main's ABI1.5 motor, Rust Graphics1.7 and Python Graphics1.9. Only
owned app paths change. Shared library SHA256:
`5fa0292dc7485957baf8106be007b6292b9c64578d4b9e574a3357d14911b477`;
native driver:
`bff17d09b48dd53437ea9fec5ef70224cac69804f4dc32f2c38f720a9113c9e1`;
static engine archive:
`d060b19918747fc1ba874b2de9eb865e9fbed73f817796e89ead25da19a22b6c`.
No external engine checkout, pin rewrite or later captured-state load is used.

Exact [APP_BUILD](validation/m3-input-app-build.log) passes **112 consumer tests,
zero skips**, **27 native exercise checks** and **20 inspection/live checks**;
ARM64, isolated relocated runtime/source/assets, source binding and strict deep
signing pass. The new tests compare native event mapping against independent
script mapping after every phase, including context registers, click timing,
cursor hold and Ctrl release. Digit 0–9 hotkeys produce WndProc messages without
expanding the twelve polled human key bindings. The native recorder smoke now
obtains Ctrl from a mouse event's physical modifier flags, without first sending
a synthetic flags-change event. Losing game focus releases held keys.

Two rejected build attempts remain preserved: an immutable tuple/list expectation
in the new digit test ([log](validation/m3-input-initial-consumer-failure.log)),
then a recording-policy label that failed the existing validation-mode UI check
([log](validation/m3-input-initial-ui-policy-failure.log)). The tuple expectation
and actual mode-specific label were corrected; no proof/assertion was weakened.
Initial queued proof invocations refused a stale ABI1.4 bundle before any game
phase ran. Delivery proofs use the published ABI1.5 bundle under the build lock
and verify its source revision and mapper/driver bytes before loading a world.

Fresh [answer proof](validation/m3-input-answers.json): **155,597/155,597**, six
canonical byte round trips, zero first differences. The [128-frame native proof](validation/m3-input-live-prefix.json)
retains **257/257 states, 11/11 checkpoints, 128/128 original surfaces and 128/128
Python1.9 oracle surfaces**, including palette/cache/ordered-observation checks.
The [full no-input chain](validation/m3-input-live-long.json) also retains
**18,401/18,401 states and 9,200/9,200 original surfaces** with no stop inside that
window. It takes 347.104 seconds; all per-phase/surface comparisons use the
production frame driver. No new reference state or exclusion mask is introduced.

[Engine gate](validation/m3-input-engine-gate.log) passes **28 Rust tests,
63 Python tests plus 10 renderer child tests**, **75 original-x86 comparisons /
zero mismatches / zero skips**, C layout, Swift ABI1.5 interoperability and
**128/128** Swift/Metal render surfaces. Its debug timing is not release UI fps.
[Common checks](validation/m3-input-common.log.gz) pass with
`/usr/bin/python3 -B scripts/check.py` in this feature worktree and `.local/python`:
Core576/215 optional skips, Combat279/153, Economy533/209, Graphics267/0,
Missions154/33, AI/runtime112/8, Audio79/4, workflow9/0 — **2,009 tests,
622 optional skips, zero failures/errors**. Native/emulated runs use the lease;
all actual executions stay below 20 minutes. Source/docs links are checked again
before delivery. No acceptance or main integration is performed.

### Test A state half — reached prefixes

All six [state proofs](validation/m3-input-delivery.json) replay imported/canonical
files through the mapper into the same native phase entry used by play. Each
world starts once at S0, executes 128 real prefix frames and carries state/context
forward without reloading any original checkpoint. Every actual consumed poll
request is answered by the script mapper and compared to the engine. Completed
frames also compare the original input stream (including WndProc flag stores),
order packets and canonical hashes of the owner's exact indicator fields.

| Probe | Complete frame hashes equal / compared | Whole-state phases equal / compared | First engine stop |
|---|---:|---:|---|
| [P1](validation/m3-input-state-P1.json) | 501/501 | 1,002/1,002 | None in requested window |
| [P2](validation/m3-input-state-P2.json) | 601/601 | 1,202/1,202 | None in requested window |
| [P3](validation/m3-input-state-P3.json) | 91/91 | No published window in this proof | Frame220, phase3, BatimentNextEtape type3 `0x426aff` |
| [P6](validation/m3-input-state-P6.json) | 91/91 | 183/183 reached, of 4,544 requested | Same frame220/phase3 CAVE body |
| [P7](validation/m3-input-state-P7.json) | 91/91 | No published window in this proof | Same frame220/phase3 CAVE body |
| [K1](validation/m3-input-state-K1.json) | 12/12 | No published window in this proof | Frame141, phase2, AffGame view `0x415b77` |

Every first difference is null. P6's 183rd successful phase is
`between_frames220`; failed phase3 is not counted equal. Frame hashes cover the
owner's indicator comparator (including unit-record hashes, objective/UI bytes,
selection and RNGs); they are not whole-memory hashes for P3/P7/K1. Full-state
checks use the published exact masks/block identities/register policy through
the unchanged engine-owned reader. The entire requested original window is not
claimed where the engine stops. No renderer ran after the prefix in these state
proofs, and no later input/order was injected after a stop.

### Actual UI performance with live orders

The [default-rate 65-second run](validation/m3-input-orders20.json) dispatches
AppKit mouse events through the actual window/responder path, observes engine
SetPlayerOrdre tags **1 and 5** and verifies the asynchronous texture readback.
It sustains **118.752 displayed fps average / 111 minimum one-second fps** while
the game runs at **20.010 frames/s**, with zero audit work/publication drops and
1,920,000 pixels checked. The pointer moves to empty ground after the orders;
this is a declared input gesture, not a glyph/tooltip bypass. Production code has
no fixture text callback. The displayed actor's moved position and selection/menu
are present in the committed GPU image.

The [60-game-fps attempt](validation/m3-input-orders60.json) reaches frame2,951,
then the production renderer stops at frame2,952: **AffInfoSelection 0x410be4**,
`fatigue words outside captured +4 = +0x76 = 4`. Its `passed` field is false.
The paused tail's zero-fps bins are retained and are not claimed as sustained
performance. The actual partial buffer is retained/exported, with the visible
named stop. No coercion of fatigue words, fallback renderer, skipped draw or
later captured surface is used. This is an additional engine-renderer dependency
beyond the requested CAVE/viewport simulation stops and known AffText glyph stop.

The short APP_BUILD validation UI sample is **46.489 displayed / 46.718 game fps**
over 8.712 seconds, including 257-state startup proofs (minimum full-second27).
An additional 65-second validation timing repeat was cancelled before execution
after prolonged shared-lease contention; native validation UI checks and the
9,200-frame complete equality chain passed. Uncapped orders timing was not run
because the fatigue domain already prevents a comparable full window. Those are
explicit skips, not successful measurements.

The [delivery manifest](validation/m3-input-delivery.json) pins source, libraries,
reports, logs and images. No executable code changes after validated build
04dea39. Build/recruitment/help dispatch is enabled through the generic engine
input path; full execution/visual continuation still needs CAVE body, viewport,
fatigue and glyph ports. The original timing probe, broader workload performance,
continuous drag and human Test B remain gaps. Only the feature branch is pushed;
no main merge or milestone acceptance is recorded.

## ABI 1.6 consumer and original pacing audit

Fetched main `240ea87` contains the persistent ABI 1.6 contract; the feature
fast-forward adopts it without modifying `motor/`. The C consumer requires major
1/minor >=6, loads complete S0 once, and selects `rl_execucao_definir(world,1)`
when Jogar is selected before phase 1. Validar retains execution policy 0 and
its unchanged projection/hash/observer path. Mode changes after phase 1 remain
rejected. Failure of policy selection is a named stop, never a silent fallback.
The engine selector takes an opaque uint64 world and uint32 mode 0/1/2 and
returns int32 status; it does not advance generation or virtual ticks.
`macos_live_validation` accepts uint32 0/1 only before phase 1. Complete MONDE01
S0 and the committed renderer/input domains remain the supported domain.
Order is S0 load → policy selection → phase 1 → repeated render → phase 2 →
phase 3, with proof observers after successful phases only in validation.
Caller buffers, carried cache and error atomicity remain unchanged. Test A state proofs
select persistent audited policy 2 explicitly to preserve consumed-poll records.
Production play policy 1 retains real order/text/sound requests.

The read-only [pacing audit](validation/m3-abi16-original-pacing.json) and
[original instructions](validation/m3-abi16-original-pacing.asm) identify intact
RISING.EXE SHA256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
`WinMain 0x460205..0x46021b` calls `0x47500e` when active and the message queue
is empty; inactive uses WaitMessage. `0x47505e` calls CalculGame, then
`0x475063` calls rendering. `GameNextFrame 0x45d015` just increments the counter.
`CalculFrame 0x43f710` calls GetTickCount to count frames per >=1,000 ms and
formats a two-digit display, without throttling simulation. The render divisor
at `0x417909` runs after simulation. `DDFlipPage 0x43f220..0x43f26b` calls
BltFast with DDBLTFAST_WAIT and retries still-drawing; this is blitter readiness,
not a fixed game timer or a WaitForVerticalBlank cadence.

All executable-section timer-import and thunk references are recorded. The other
timeGetTime references are FLI playback elapsed time, network input, CD audio
deadlines and RNG seeding; WaitForSingleObject references are CRT semaphore/join
paths. No fixed-Hz active-loop timer gate or named WaitFrame is established.
The default now follows the original's uncapped idle-loop policy, with optional
15/20/30/60 host caps. TickClock remains at its audited nominal 20 and recorded
frame numbers are unchanged. This reproduces scheduling policy, not the speed
of a particular historical computer. Historical Windows CPU/driver/refresh FPS
is unmeasured. A historical elapsed-speed calibration, if wanted, requires the
AI/runtime/coordinator owner to publish a real Windows hardware/session timing
contract; no single fixed FPS can be inferred from this executable path.
Requested calibration contract: intact hash above; original Windows CPU/OS,
DirectDraw driver and refresh; active/unoccluded MONDE01; default draw divisor
byte `0x497284 = 1`; >=65 seconds of real native GetTickCount start/end uint32
values paired with game counter `0x496d40` start/end uint32 values and declared
pause/input policy. Distinguish counter wraps, simulation iterations and actual
presentations. Emulator execution time or a stubbed timer cannot supply the
historical elapsed-speed measurement.

Benchmark orders are real AppKit selection/movement clicks after the real
128-frame prefix, followed by a real right-click on empty ground to deselect,
then a pointer move to empty ground. Input remains enabled every frame. This is
a declared narrower workload than keeping a fatigued actor selected. It changes
no world bytes, renderer domain or stop handling. The production selected-actor
fatigue stop at `0x410be4` remains. Gestures are anchored to observed game frames
rather than an eight-second timer, allowing uncapped play to receive orders
before the first-raid dependency horizon. Failed sustained runs retain every
second, the named stop and the separate first-stop active-window snapshot.

The frozen runtime/build is **b44fe804a696413f79904b9d36b01f30138cfac5**.
[APP_BUILD](validation/m3-abi16-delivery-app-build.log) passes **112 consumer
tests / zero skips**, **27 native exercise checks** and **20 inspection checks**;
ARM64, relocated runtime/source/assets and strict deep signing pass. The app
uses its immutable archive's integrated motor with static ABI 1.6 binding.
No external engine override is used. [Engine validation](validation/m3-abi16-engine-gate.log)
passes **30 Rust tests, 63 Python tests plus 10 renderer child tests, 75
original-x86 comparisons / zero mismatches / zero skips**, C layouts, Swift
ABI 1.6 and 128/128 Swift/Metal surfaces. Its debug timings are not UI throughput.

Fresh [prefix](validation/m3-abi16-live-prefix.json) and
[uninterrupted long proof](validation/m3-abi16-live-long.json) retain
**257/257 states, 11 checkpoints, 128/128 original and Python surfaces**, and
**18,401/18,401 states / 9,200/9,200 original surfaces**, respectively. There is
no stop or observer failure in the 9,200-frame window. All prior prefix hashes
match. All [21 prepared native binary inputs](validation/m3-abi16-input-regression.json)
remain byte-identical to the ABI 1.5 build, including S0, masks, original expected
state/surface hashes, assets and initial cache.

Fresh [Test A answers](validation/m3-abi16-answers.json) retain **155,597/155,597**
and six canonical byte round trips. All prior input, canonical, native log,
expected-answer and actual-answer hashes are [unchanged](validation/m3-abi16-answer-regression.json).
The six [state probes](validation/m3-abi16-correctness.json) also retain every
prior frame hash: P1 501 frames / 1,002 whole-state phases; P2 601 / 1,202;
P6 91 / 183; P3/P7 91 indicator-hash frames each; K1 12. P3/P6/P7 retain
frame 220 phase 3 CAVE `0x426aff`; K1 retains frame 141 phase 2 viewport
`0x415b77`. No requested phase beyond those stops is claimed.

[Common checks](validation/m3-abi16-common.log.gz) pass **2,039 tests, 624
optional skips, zero failures/errors**. `check.py` does not offer a macos domain
selector; APP_BUILD supplies the consumer gate and the supported complete common
suite was run. Only own queued correctness jobs were requeued before grant with
50 ms polling to avoid starvation, using the unchanged shared helper/locks/slot
limits; the [restart record](validation/m3-abi16-lease-poll-restart.json) preserves
that distinction. Every executed macOS job remains below 20 minutes after grant.
No original capture, pin or mask is changed. No main merge/push or acceptance.

The three 75-second ordered UI runs are still queued for the unmodified exclusive
heavy lease. This duration allows >=65 seconds with input enabled after the real
128-frame prefix at nominal 20 Hz. No sustained UI result is claimed yet.

## State at 2026-10-30 07:15

Docs-only reconciliation at the MacBook pause; no build, gate or native run.

- **Main** (app last integrated at `51715e2`, validated executable `04dea39`):
  ABI 1.5 orders consumer, Rust Graphics 1.7, Python Graphics 1.9 oracles.
  Play mode reaches 60 game frames/s and above in the no-input window (69.2
  uncapped) with ~120 displayed fps; ordered play at 20 Hz gives 118.752
  displayed fps. Test A answers 155,597/155,597; state half P1 501/501 frames
  and 1,002/1,002 phases, P2 601/601 and 1,202/1,202, P3/P6/P7 91/91 (P6
  183/183 phases reached), K1 12/12, all first differences null.
- **This branch, awaiting integration:** `4dad27e`, `8de9b7e`, `b44fe80`,
  `40c6295` (ABI 1.6 policies 0/1/2, original uncapped pacing default, gates
  in the section above). The three 75-second ordered UI runs have not run.
- **Parked, unvalidated:** `origin/wip/macos-abi16-0700` (`874a079`, the failed
  first ordered attempts at AffText `0x459454` and the right-click
  `event.type` fix; no gate rerun) and `origin/wip/macos-playable-0715`
  (`d774d14`, only an empty corrected-run log). Neither is reviewed.
  Uncommitted outputs of the corrected runs on a development build of
  `874a079` were left untracked in this worktree
  (`validation/m3-abi16-right-orders{20,60,-unlimited}*`, 06:57–06:59). As
  written by the benchmark: 60 Hz passed (75 s, 60.01 game frames/s, 117.9
  displayed fps, minimum 110, no stop); 20 Hz ran 75 s without a stop but is
  marked failed (minimum one-second display 79); uncapped stopped at frame
  10,801 on `Display monster count 0x0041591f` after ~141 game frames/s. They
  are not committed, not gated and not claimed.
- **Open stops:** engine CAVE `0x426aff` at frame 220 and viewport `0x415b77`
  at frame 141 (Rust engine); renderer fatigue `0x410be4` and glyphs `0x459454`
  (Rust renderer port); Test A beyond 220 and Test B (macOS, with the replay
  on the original on the Mac mini).
- **Next:** review `874a079`, rerun APP_BUILD and the ordered UI runs, then
  integrate ABI 1.6; extend Test A when the engine passes 220; record Test B.

The manual's [current state](../../docs/MACOS_PLAYABLE.md#current-state-2026-10-30-0715)
holds the owner table and next steps.


## Native recording smoke focus regression (2026-10-30)

Implementation: `c5f1734f6a0fb517fd997862746c65c99f958f24`, on feature base
`e553010` (merged main `00afd4b`). The coordinator's failing `8808d54` bundle
reproduces `TypeError: undefined is not an object (evaluating 'down.frame')`.
Its exported Missions script has no frames. A separate diagnostic build adds
only native view receipt counters and reports **recording=true, hidden=false,
appActive=false, windowKey=false, mouseCalls=0**. The visible-window and recording
indicator checks did not establish input readiness: AppKit discarded the
synthetic clicks while the application was inactive. Diagnostic logging or extra
UI work changed timing and could conceal the failure. Timestamp-only and
application-dispatch-only experiments still failed; neither is adopted.

The smoke-only `recordNativeSmoke(body, live, deadline)` accepts the existing
playback request dictionary and press/release stages. It runs on the AppKit main
queue, requests activation and a key native window, then waits asynchronously
for actual application/window focus. Its monotonic Double deadline is two
seconds inside the unchanged 45-second checks budget. It requires the real
Metal view as first responder before dispatching the unchanged NSEvents through
NSWindow. Failure returns a named PT-BR error without dispatch. The native worker
still stamps events with the next game frame; no wall-clock value enters a
recording or the engine. Native input-barrier and WebView recording/export
ordering are unchanged. An additional smoke assertion checks the actual active
application, key window and Metal responder; every original click cadence,
Ctrl-hold, state, surface, readback and timeout assertion remains.

This is an AppKit smoke-fixture repair, with no new reconstructed behavior.
Engine ABI 1.6, policies 0/1/2, original tables, references and masks are unchanged.
Original identity remains RISING.EXE SHA256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`;
recorded Windows messages still target WndProc `0x4181a1`. Supported engine and
renderer domains and their named stops are unchanged. No parked WIP is adopted.

The exact [APP_BUILD](validation/m3-smoke-focus-app-build.log) passes **112
consumer tests / zero skips**, **27 native exercise checks** and **21
inspection/live checks**. Architecture, relocated runtime/source/assets, source
binding and strict deep signing pass. [Engine gate](validation/m3-smoke-focus-engine-gate.log.gz)
passes **30 Rust tests, 63 Python tests plus 10 renderer children**, **75
original-x86 comparisons / zero mismatches / zero skips**, C/Swift ABI layout and
**128/128 Swift/Metal surfaces**. The engine source tree is unchanged from the
pre-fix gate (`835d527e765fc0ebe6515016e1d7318bbebeff36`).

Fresh [answer proof](validation/m3-smoke-focus-answers.json) reproduces every
prior answer/provenance hash: **155,597/155,597**, six canonical round trips.
The [prefix](validation/m3-smoke-focus-prefix.json) retains **257/257 states,
11/11 checkpoints, 128/128 original and 128/128 Python surfaces**. The
[uninterrupted long chain](validation/m3-smoke-focus-long.json) retains
**18,401/18,401 states / 9,200/9,200 original surfaces**, no stop or observer
failure. All prefix hashes and all [21 prepared native files](validation/m3-smoke-focus-input-regression.json)
are unchanged.

Every prior per-frame indicator hash and whole-state report is reproduced:

| Probe | Frame hashes | Whole-state phases | First engine stop |
|---|---:|---:|---|
| [P1](validation/m3-smoke-focus-state-P1.json) | 501/501 | 1,002/1,002 | None |
| [P2](validation/m3-smoke-focus-state-P2.json) | 601/601 | 1,202/1,202 | None |
| [P3](validation/m3-smoke-focus-state-P3.json) | 91/91 | No published window | Frame220 phase3 CAVE `0x426aff` |
| [P6](validation/m3-smoke-focus-state-P6.json) | 91/91 | 183/183 reached | Same CAVE stop |
| [P7](validation/m3-smoke-focus-state-P7.json) | 91/91 | No published window | Same CAVE stop |
| [K1](validation/m3-smoke-focus-state-K1.json) | 12/12 | No published window | Frame141 phase2 viewport `0x415b77` |

Every first difference is null. These state proofs omit rendering after the real
prefix; no requested continuation beyond the known stops is claimed.

The [65-second no-order play run](validation/m3-smoke-focus-play60.json), at the
60 game-fps cap under an exclusive lease, sustains **60.013 game frames/s**,
zero audit counters/time, zero publication drops and 1,920,000 GPU pixels checked.
This session's monitor reports **60 Hz**, so its **59.751 displayed fps /
56 minimum full-second fps** is recorded separately from historical 120 Hz runs.
An [unchanged pre-fix bundle](validation/m3-smoke-focus-baseline-app-play60.json)
measures **60.013 game / 59.936 displayed fps**, minimum **57**, on the same
60 Hz display, with the identical final GPU image. All bins, startup seconds,
raw timings and both presentation rates are retained. The archived bundle's
first launch was rejected before execution from its preserved directory without
an `.app` suffix; an unchanged copy with that suffix passed strict deep codesign
verification and supplied the comparison. No refresh setting or frame path was
changed to obtain the measurements.

The [delivery manifest](validation/m3-smoke-focus-delivery.json) binds current
sources, runtime libraries, reports, real commands/lease events and diagnostics.
The [diagnostic patch](validation/m3-smoke-focus-diagnostic.patch) is evidence-only,
against `8808d54`; it is not applied to the delivered app. The
[baseline failure](validation/m3-smoke-focus-baseline-failure.json) and
[inactive-window diagnosis](validation/m3-smoke-focus-inactive-diagnosis.json)
remain preserved. No parked run output is reused. Docs/evidence after `c5f1734`
change no executable input. Only `feat/macos-playable` is pushed; no main merge,
acceptance, new engine domain, ordered-UI claim or Test B work.

## Main 6cdbc5a consumer rerun and selected-actor fatigue (2026-10-30)

Runtime implementation/build: **afbc0f075a3d57cc04a1a3bbfe6d32e939cd3fe0**,
after a fast-forward merge of `origin/main` **6cdbc5a**. The app-owned C driver
now explicitly accepts Rust Graphics **1.9** (`0x00010009`); ABI 1.6, copied
buffers, generations, serial phase order, masks, inputs and failure publication
remain unchanged. Swift/inspection version labels and the native ABI assertion
follow that reviewed contract. No engine or research-front file is edited.

Original identity remains intact RISING.EXE SHA256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Test A still starts every world at S0 with the four immutable original tables,
runs the real 128-frame prefix, and uses the app mapper and production C phase
entry with audited persistent policy 2. Phase 2 consumes declared messages,
cursor and signed key answers; phase 3 receives the same keys and no messages.
The carried state/context is never replaced by a later oracle state. Frames require equal hashes of the owner's exact indicator fields and separately
equal consumed inputs, orders and WndProc output flags; whole-state phases use
the owner's published cumulative
mask/block/register policy. Rendering after the prefix is excluded from Test A.
A failed engine phase is a named dependency stop, not an equal phase.

### Former frame 2,952 fatigue stop

The new app-driver [bounded diagnostic](validation/m3-chain8-fatigue-diagnostic.json)
reaches **4,500 completed frames**, including attempted render 2,952, without a
stop. Its exact declared mouse events occur at 481/493/511; this is not a replay
claim about the historical UI arrival times. It uses play policy 1 and the real
advancing renderer, with no per-frame projection, proof observer or equality
counter. Only boundary/stop projections are read for diagnosis.

At completed frame 2,951, unit **12**, type **7**, owner **0**, state **7** stays
selected (`+0xbd=1`) at original record address **0x474a8cf0**. The boundary has
`u16(+4)=3`, `u16(+0x76)=4`, `u16(+0x74)=0`; frame 2,952 completes and the last
word becomes 1. Both original-address 276-byte records and their SHA256 values
are retained in the diagnostic. No consumer word is coerced, no draw is skipped,
and no deselection or substitute image hides the boundary.

This is the new renderer's explicit **type 5/7, word pair 3/4** extension in
`motor/crates/rl-core/src/render_units.rs`, matching Graphics 1.9's committed
`camadas_m3_api18.json` / `sobreposicoes_entrada_m3.validar_unidade`. It resolves
this selected-builder boundary; it does not establish every fatigue pair or unit
type. Other unsupported pairs keep the actual `AffInfoSelection 0x410be4` stop.
The supported domain is owned by the engine/Graphics fronts, not broadened here.

The app adds the separate `--orders-selected` benchmark option: the historical
real AppKit selection/movement clicks at 8/8.2 seconds and pointer motion at
8.5 seconds, keeping the actor selected. This workload does not use the newer
benchmark's right-click/deselection gesture. The existing right-event fixture
issue and other workloads are outside this task. Production input is unchanged.

### Gates and preserved evidence

Exact [APP_BUILD](validation/m3-chain8-app-build.log), run with
`--development-ref HEAD --inputs-root "/Users/marcio/git/Rising Lands"
--data-root "/Users/marcio/git/Rising Lands/local-data/macos-playable"`, passes
**112 consumer tests / zero skips**, **27 native exercise checks**, and **21
inspection/live checks**. The source/runtime/assets checks, ARM64 binaries and
strict deep signing pass. Static Swift and the dynamically bound proof driver
consume the same archived engine sources. No external engine override is used.

The fresh [engine gate](validation/m3-chain8-engine-gate.log.gz) passes **30 Rust
tests, 63 Python tests plus 10 renderer children**, **75 original-x86 comparisons /
zero mismatches / zero skips**, C/Swift ABI checks and **128/128 Swift/Metal
surfaces**. The player leaf subtest asserts **666/666 completed state comparisons**,
zero mismatches/stops and **two declared adapter skips** (KeyTestRelease with a changing key stream and
InitInputPlayer allocator setup, outside the fixed-key/already-loaded contract;
separate from the
75 fresh x86 comparisons, which have zero skips). The complete common gate
passes **2,108 tests / 624 optional skips / zero failures or errors**. There is
no `macos` selector in `scripts/check.py`; the requested selector's explicit
usage error is preserved, and the supported complete suite supplies that gate.
APP_BUILD separately supplies the app consumer/native UI gate.

Fresh [prefix](validation/m3-chain8-prefix.json) and
[uninterrupted long-chain](validation/m3-chain8-long.json) proofs retain
**257/257 states, 11/11 checkpoints, 128/128 original and Python surfaces**, and
**18,401/18,401 states / 9,200/9,200 original surfaces**, respectively. Both have
null first stops and no observer failures. Proof wall times include auditing
and are not play throughput.

The first queued proof launch referenced the staging `.app`, which the successful
builder moves into `dist/development/`. Those launch failures executed no state
comparison; their logs and commands are preserved separately. The reruns use the
delivered bundle. Two queued exclusive timing wrappers were stopped before grant
so the remaining deterministic jobs could start, then requeued unchanged; the
queue record distinguishes waiting from execution. All executed jobs use the
unchanged shared lease helper and locks, with bounded native proof entry points.
No other front's process or lease is modified.

### Selected-actor UI result

The actual [75-second ordered UI run](validation/m3-chain8-selected60.json)
passes **4,501 completed frames**, with tags **1 and 5**, **five native human
events**, observed next-frame gestures **482/494/512**, and null live/first stops.
It sustains **60.009 game frames/s**, **59.942 displayed fps**, minimum full-second
**58**, on the current **60 Hz** display. The actor stays selected; the
[actual GPU readback](validation/m3-chain8-selected60.png) retains that visible
selection. Play policy 1 has zero audit counts/time and zero publication drops;
1,920,000 RGBA channel bytes are checked. This directly resolves the earlier
2,952 failure for the historical selected-builder workload on the new engine.
It does not claim a broader fatigue domain or fidelity beyond published original
windows. All second bins and raw rates remain in the report.

The separate [65-second no-order run](validation/m3-chain8-play60.json) also
passes: **3,901 frames**, **60.013 game / 59.936 displayed fps**, minimum full
second **57**, on the same 60 Hz monitor. Audits/time and publication drops are
zero; GPU readback checks the same complete RGBA extent. This preserves the
previous no-order play target. Neither display measurement is labeled 120 Hz.

### Test A state half — new engine results

| Probe | Frame hashes equal / compared | Whole-state phases equal / compared | First engine stop |
|---|---:|---:|---|
| [P1](validation/m3-chain8-state-P1.json.xz) | 501/501 | 1,002/1,002 | None in published window |
| [P2](validation/m3-chain8-state-P2.json.xz) | 601/601 | 1,202/1,202 | None in published window |
| [P3](validation/m3-chain8-state-P3.json.xz) | 3,001/3,001 | No published window | None in published window |
| [P6](validation/m3-chain8-state-P6.json.xz) | 2,272/2,272 | 4,544/4,544 | None in published window |
| [P7](validation/m3-chain8-state-P7.json.xz) | 3,572/3,572 | No published window | None in published window |
| [K1](validation/m3-chain8-state-K1.json.xz) | 501/501 | No published window | None in published window |

Every first difference and first engine stop is null. P3/P6/P7 now complete
the original windows 129–3,129 / 129–2,400 / 129–3,700. K1 also completes all
501 frames through 629; the former frame-141 viewport stop is resolved. No
whole-state claim is added for P3/P7/K1 without a published window.

Fresh [answers](validation/m3-chain8-answers.json) retain **155,597/155,597**
with six canonical round trips. The [regression record](validation/m3-chain8-regression.json)
checks every prior reached indicator hash and whole-state phase, both prefix
row sequences, every answer/provenance field, and all **21 native binary inputs**:
all are unchanged. The [correctness summary](validation/m3-chain8-correctness.json)
keeps original evidence identities, requested/reached counts and actual stops.

The [delivery manifest](validation/m3-chain8-delivery.json) binds the runtime,
engine tree, reports, compressed raw hashes, commands and lease journal. Final
docs/evidence/diagnostic-tool additions change no production runtime input after
the validated build afbc0f0. Only `feat/macos-playable` is committed/pushed.
No merge to main, acceptance, Test B or unrelated work is performed. Remaining
dependencies include the broader renderer domain and human Test B replay on
the original; full mission/campaign/audio are not claimed.
