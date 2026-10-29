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

A real committed-revision launcher attempt and its prerequisite result will be
recorded separately; these source/package regressions do not constitute a
native application build or UI smoke pass.
