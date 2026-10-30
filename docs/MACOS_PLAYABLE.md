# Local macOS playable consumer

`compilar-jogável` builds **RisingLands-ptbr.app** for this Apple Silicon Mac.
The primary game path is the native **Rust e Metal** window: MONDE01 from the
accepted S0, Rust engine logic and rendering through the C ABI, Metal
presentation, and live player orders. The Swift/AppKit/WebKit shell, the M2.2
evidence inspector and the older synthetic **Treino livre** exercise (described
in the historical sections below) remain available. It is a bounded
reconstruction, not a complete original mission or campaign.

## Play-mode sound effects (2026-10-30)

**Jogar** now plays the original sound effects exactly when the engine requests
them. **Validar** is unchanged: it never enables the transport, so no audio
call touches game state, audits or proofs.

**How requests reach the app (no ABI change).** ABI 1.6 already copies every
`PlaySnd_PostSound`/`PlaySnd_StopSound` call as `RlPlayerInputEvent` kind 10
(`post, EAX, EDX, EBX, ECX, has_volume, volume`), and keeps those events in
play policy 1. After each successful play phase the C driver
(`macos_live_driver.c`, `macos_live_sound_capture/_events`) copies them, in
order, into a 4,096-entry transport. The WinMain loop calls `PlaySnd_Manage`
before every `PeekMessage`, so the driver adds one Manage tick at the start of
phase 2 and, when phase 2 dispatched requests, the loop's final tick after
them. `rl_eventos_entrada` is a pure query, so state is unchanged.

**What plays.** The engine's game state is the original's *unopened* sound
library (Audio's validated domain): caller handles stay -1 and nothing is
played. `macos_audio_mapper.c` is a line-by-line C port of Audio's validated
initialized queue (`fila_audio.AudioQueue` plus `carregar_info_som`), running
over its own private image at the original addresses (globals `0x498f14`,
BSS `0x521358`, the HED bodies, and a shadow map of caller handle words).
It never reads or writes game memory. It keeps:

- the 20 playing records and the waiting records 20..70;
- ten physical and ten logical (`DuplicateSoundBuffer`) slots;
- the entry-word-256 dictator, a single voice channel that keeps later voices
  waiting;
- the `GetDataHeader` variant cursor;
- repost semantics: the same ID on a busy handle only updates its volume, and
  volume 0 cancels;
- the original volume lookup
  `((volume*byte13|256)*game_volume)>>20` into the initialized table at `0x498f14`
  (-10000..0 hundredths of dB);
- looping when the flags byte (ECX low byte) is 1.

There is no pan: the original issues no `SetPan`, and every sample is mono.

`NativeAudio.swift` runs the mapper's commands (create, duplicate, play,
volume, stop, release) on its own queue, using an AVAudioEngine pool of player
nodes. The only device answer fed back is "buffer stopped" (DSB_IsStopped),
taken from the player's played-back completion. Samples are the pinned asset
release's decoded WAVs (`rising-lands-assets` v1-4eb88f2): PCM16, mono,
22,050 Hz, played without resampling or normalization. Playback gain is
`10^(dB/2000)`.

**Build.** `playable_audio.py` copies the original `A/B/P.HED` from the CD,
hash-checked against Audio's catalogue, into `Resources/preview/audio`. When
`<inputs-root>/rising-lands-assets` (or `RISING_ASSETS_ROOT`) exists, the build
also copies all 551 WAVs (48,945,219 sample bytes, about 49 MB). That checkout
must be exactly the ORIGIN release commit, clean, with the manifest hash
matching, and every WAV must match its manifest hash. Any mismatch stops the
build. A missing checkout produces an explicit soundless bundle (`som: ausente`
in the window caption and `audio.status=absent` in the build manifest); no
replacement audio is ever used. The bundle verifier re-hashes every audio file.

**Tests** (`testes/test_macos_audio.py`, no sound card needed):

- The complete original S1 MONDE01 boundary log (177 PostSound, 3 StopSound,
  17,167 Manage calls) and P6 (59 PostSound) are replayed in order through
  the C mapper and through Audio's own `fila_audio.AudioQueue`. Both use the
  same private image and device model. Two device models are run: samples end
  after their catalogued length at 60 frames/s, or never end, which exercises
  saturation.
- Every request and every ordered device command must be equal between the
  two: S1 schedules 138 plays (finishing model) or 57 (holding model); P6
  schedules 56 or 7. The run must have zero domain faults, unknown IDs or
  overflows.
- Every created sample must be a catalogued, `GetDataHeader`-reachable
  original variant of an ID the log posted at or before that frame. The test
  also checks the original volume table bytes.
- A transport test runs the real engine through the production C phase entry
  on P2's scripted input. Its copied requests equal P2's original
  PostSound log (frames 133, 133, 143: registers, volume, return site) and
  carry one Manage tick per frame.
- S1's single `PlaySnd_StopAllSound` at victory is not translated by Audio
  and is excluded explicitly.

**Gates and speed (build `5e182f4`).** APP_BUILD passes: **122 consumer
tests, zero skips**, including the five audio tests with the engine transport,
plus both native smokes. The build manifest records `audio.status=bundled`
(551 samples). `sh motor/validate.sh` passes unchanged: 75 original-x86
comparisons, 0 mismatches; 63 Python tests and 10 renderer children. A
75-second real-window run at the 60 cap, with the selected-actor order
workload (`--orders-selected`), gives:

- **60.009 game frames/s** and **59.943 displayed fps**, minimum full second
  **57**. The no-audio baseline was 60.009 / 59.942 / 58.
- audits off and no stop.
- 4,376 transported requests: 3 PostSound and 4,373 Manage ticks.
- 2 sounds actually started on the output device, 0 missing samples and 0
  domain faults.

Evidence: [benchmark](../apps/macos-preview/validation/m3-audio-play60-selected.json),
[consumer tests](../apps/macos-preview/validation/m3-audio-consumer-tests.log),
[engine gate](../apps/macos-preview/validation/m3-audio-engine-validate.log.gz).
The app's Python inspection gate now consumes main's additive Graphics render
API **1.10**. The Rust renderer contract stays 1.9.

**Known limits (named requests).**

- *Audio:* translate `PlaySnd_StopAllSound` (0x48aac5), `PostVolume`
  (0x48aacf) and `SetGameVolume`.
- *Engine/Audio:* the engine models the unopened library. An initialized
  original would store the returned queue index in caller handles (unit
  `+0x104`), so busy handles would take `PostVolume` and the `+0xf9` branch
  instead of `PostSound`. Exact busy-handle audio therefore needs an
  initialized-audio engine domain validated original-first. Until then the
  mapper's shadow handles reproduce queue behavior for the requests the engine
  actually makes.
- Waiting index 70's aliasing of `0x521f84` and volume lookups
  outside 0..16 are counted as `audioDomainFaults` rather than raised. The
  replayed logs reach neither.
- P/0221-v00's one-byte incomplete PCM tail (FORMAT.md) is not played.

**CD music: not played yet; extraction plan.** `RISING_LANDS_BR_.CUE`
describes track 01 (MODE2/2352 data) plus two CD-DA tracks in the BIN (raw
2,352-byte sectors, 44.1 kHz, 16-bit little-endian stereo):

| Track | BIN sectors (index 01 → next index 01 / end) | Bytes | Length | SHA-256 |
|---|---|---:|---:|---|
| 02 | 227,283 → 269,653 | 99,654,240 | 564.93 s | `b6bb0739cc569e28347145699724b541ad64d7419447b55cbe99a493ff690710` |
| 03 | 269,653 → 299,923 | 71,195,040 | 403.60 s | `1005fda1b49a8174e8032734ed022effe214e3e79c6aabab5d898ba6e2f02b45` |

The track-02 pregap (227,133..227,283) is digital silence. Static reading of the
intact MCICD routines:

- `MCICD_Init` 0x467af6 opens `"%c: type cdaudio alias cdrud"`, sets byte
  `0x4e2f29`=1 and `0x4e2f28`=0.
- `MCICD_Play(track, loop)` 0x467a8c sets the stop time to `timeGetTime()` plus
  `status cdrud length track N`, sends `play cdrud from N`, and stores
  `0x496fdc`=track, `0x4e2f2a`=loop and `0x4e2f28`=1.
- `MCICD_Manage` stops at the stop time (`stop cdrud wait`, `0x4e2f28`=0) and
  replays only when the loop flag is set.
- CalculGame (0x42d2f0) calls `MCICD_Play(2 + perm[cursor] % 2, 0)` whenever
  `0x4e2f28`=0. In-mission music is therefore tracks 2/3, chosen per track
  from the shared permutation table, played once each.

Extraction is straightforward. The proposed assets release adds
`data/music/TRACK02.cdda.part-0000..0002.bin` and `TRACK03.cdda.part-0000..0002.bin`:
byte-exact BIN slices of at most 32 MiB, raw CD-DA without a header, with BIN
offset, length and SHA-256 in the manifest and the BIN identity recorded as the
source. That release needs the maintenance-owned extractor, a new tag and an
ORIGIN repin. The app would stream the parts through an `AVAudioPlayerNode`.

The blocker is game state, not extraction. In the accepted domain no CD is
initialized, so every frame draws one permutation-cursor byte (`0x4e1d18`),
which NextAnim* and rendering also consume. A playing CD skips that draw, so
"the original's" track choice changes the world. Exact music needs an engine
"CD present" declared domain. MCICD_Play/Manage would become declared boundary
answers (track started, track ended from the app clock), validated against
original captures with `0x4e2f28`=1 (Audio with Missions). Until that domain
exists, music stays off rather than diverging from the validated state.

## Current state — main 6cdbc5a rerun (2026-10-30)

This feature delivery consumes the new engine from main **6cdbc5a** and updates
the native consumer's explicit renderer gate to **Graphics 1.9**. Runtime/build:
**afbc0f075a3d57cc04a1a3bbfe6d32e939cd3fe0**. Engine ABI **1.6** and execution
policies 0/1/2 are unchanged. The following historical sections preserve earlier
validation; this summary supersedes their pending CAVE/fatigue results.

The fresh app **Test A state half**, from S0 through the real 128-frame prefix,
uses the same mapper/C phase entry as play and no later oracle-state reload:

| Probe | Frame hashes equal / compared | Whole-state phases equal / compared | First engine stop |
|---|---:|---:|---|
| [P1](../apps/macos-preview/validation/m3-chain8-state-P1.json.xz) | 501/501 | 1,002/1,002 | None in published window |
| [P2](../apps/macos-preview/validation/m3-chain8-state-P2.json.xz) | 601/601 | 1,202/1,202 | None in published window |
| [P3](../apps/macos-preview/validation/m3-chain8-state-P3.json.xz) | 3,001/3,001 | No published window | None in published window |
| [P6](../apps/macos-preview/validation/m3-chain8-state-P6.json.xz) | 2,272/2,272 | 4,544/4,544 | None in published window |
| [P7](../apps/macos-preview/validation/m3-chain8-state-P7.json.xz) | 3,572/3,572 | No published window | None in published window |
| [K1](../apps/macos-preview/validation/m3-chain8-state-K1.json.xz) | 501/501 | No published window | None in published window |

Every first difference and engine stop is null in these requested windows.
K1 now completes all 501 frames through 629, resolving the old viewport stop.
Frame rows require equal indicator hashes plus separately equal inputs/orders
and WndProc output flags; whole-state phases are separately compared under the
published masks. Test A omits rendering after the prefix. P3/P7 have no published
whole-state window in this proof.

The former **frame 2,952 fatigue stop is resolved for the selected builder**.
A bounded advancing-world diagnostic retains unit 12/type 7 selected with
`u16(+4)=3`, `u16(+0x76)=4` and passes frame 2,952 through frame 4,500. The new
Rust renderer explicitly supports that type-5/7 pair, matching Graphics 1.9;
other unsupported pairs still stop. The app adds no renderer provider or state
patch. The actual **75-second selected-actor AppKit/Metal run** reaches **4,501
frames**, tags **1/5**, no stop, **60.009 game frames/s**, **59.942 displayed fps**
(minimum full second **58**) on the current **60 Hz** monitor. It keeps the actor
selected, with zero audits/time and publication drops. A separate 65-second
no-order run sustains **60.013 game / 59.936 displayed fps**, minimum **57**.

Fresh gates: **APP_BUILD 112 consumer tests / zero skips, 27 exercise checks,
21 inspection/live checks**; `sh motor/validate.sh` passes (30 Rust/63 Python
plus 10 renderer children, 75 fresh x86 comparisons / zero mismatches/skips,
128/128 Swift/Metal surfaces; input leaves 666/666 with two declared adapter
skips). The supported complete common suite passes **2,108 tests / 624 optional
skips**. `scripts/check.py` has no macos domain selector; APP_BUILD supplies the
app gate. Prefix **257/257 states, 11/11 checkpoints, 128/128 original and Python
surfaces**; uninterrupted no-input chain **18,401/18,401 states / 9,200/9,200
original surfaces**; answers **155,597/155,597**, six canonical round trips.
Every prior reached frame/whole-state result and all 21 prepared native binary
inputs remain unchanged.

See the [handoff](../apps/macos-preview/HANDOFF.md#main-6cdbc5a-consumer-rerun-and-selected-actor-fatigue-2026-10-30)
and [delivery manifest](../apps/macos-preview/validation/m3-chain8-delivery.json)
for exact domains, raw timings, original identities, proof commands and skips.
Only the feature branch is pushed; the coordinator owns integration/acceptance.
Broader renderer/mission support remains bounded by the engine contracts;
Test B/human original replay, full mission/campaign and audio remain open.

## Historical state (2026-10-30 07:15)

This summary supersedes older "pending" or "not implemented" remarks in the
chronological sections below, which are kept as the validation record.

**Native smoke repair validated on this branch (2026-10-30; runtime `c5f1734`):**
The inspection smoke previously dispatched clicks while the visible app was
inactive, yielding an empty export and `down.frame` TypeError. It now waits for
actual application/key-window/Metal-responder focus before dispatch. The original
checks and budgets remain; a new focus assertion raises inspection checks to
**21**. Exact APP_BUILD passes **112 consumer tests / zero skips**, **27 exercise
checks**, and **21 inspection/live checks**; `sh motor/validate.sh` also passes.
Fresh proofs retain **155,597/155,597 answers**, all six state-probe results below,
**257/257 states**, **128/128 original and Python surfaces**, and **18,401/18,401
states / 9,200/9,200 original surfaces**, with every prior hash unchanged.

A fresh 65-second no-order play run at the 60 cap gives **60.013 game
frames/s**, audits off. The current monitor reports **60 Hz**: displayed rate is
**59.751 fps**, minimum full second **56**; an unchanged pre-fix bundle gives
**60.013 game / 59.936 displayed fps**, minimum **57**, and the same final
GPU image. These are current 60 Hz measurements, separate from the historical
120 Hz results below. The three 75-second ordered ABI 1.6 runs remain pending.
See the [repair handoff](../apps/macos-preview/HANDOFF.md#native-recording-smoke-focus-regression-2026-10-30)
and [fresh delivery evidence](../apps/macos-preview/validation/m3-smoke-focus-delivery.json).

**On main** (app last integrated at `51715e2`; validated executable `04dea39`):

- Consumer of engine **ABI 1.5** (`rl_passo_quadro_entrada`) with Rust Graphics
  **1.7**; Python inspection and proof oracles pin Graphics **1.9**. Jogar
  applies native mouse and keyboard orders after the real 128-frame prefix; the
  recorder observes the same events. Validar keeps the no-input equality proofs.
- Play mode runs without audits: no-input **69.2 game frames/s uncapped**
  (60.001 at the 60 cap) with **~120 displayed fps**, minimum full second 117
  (build `55cddc5`). With live orders at the 20 Hz cap: 20.010 game frames/s,
  118.752 displayed fps average, minimum 111.
- Gates: APP_BUILD 112 consumer tests / 0 skips, 27 native exercise checks,
  20 inspection/live checks. Prefix proof 257/257 states, 11/11 checkpoints,
  128/128 original and 128/128 Python surfaces. Long no-input chain 18,401/18,401
  states and 9,200/9,200 original surfaces. Test A answer stream
  **155,597/155,597**, six canonical round trips.
- Test A state half, every first difference null (0 mismatches):

  | Probe | Frame hashes | Whole-state phases | First engine stop |
  |---|---:|---:|---|
  | P1 | 501/501 | 1,002/1,002 | none |
  | P2 | 601/601 | 1,202/1,202 | none |
  | P3, P7 | 91/91 each | no published window | frame 220 phase 3, CAVE `0x426aff` |
  | P6 | 91/91 | 183/183 reached | frame 220 phase 3, CAVE `0x426aff` |
  | K1 | 12/12 | no published window | frame 141 phase 2, viewport `0x415b77` |

  The P1/P2 whole-state results match the engine's M3.1 P1/P2 acceptance
  (`c9c85eb`).

**On `feat/macos-playable`, awaiting integration** (commits `4dad27e`,
`8de9b7e`, `b44fe80`, `40c6295`; frozen build `b44fe80`):

- ABI **1.6** consumer: requires major 1 / minor >=6; Jogar selects persistent
  play policy 1 after S0 and before phase 1, Validar keeps policy 0, the Test A
  state proof uses audited policy 2.
- Static pacing audit of the intact RISING.EXE: the active loop is uncapped, so
  the default speed is **Original (sem limite)**, with 15/20/30/60 caps optional.
  The engine's virtual 20 Hz TickClock is unchanged.
- Gates at `b44fe80`: APP_BUILD 112/0 skips, 27, 20; engine validation 30 Rust
  tests, 63 Python tests plus 10 renderer children, 75 original-x86 comparisons
  with 0 mismatches; prefix and long chain unchanged; Test A answers and all six
  state probes reproduce every prior hash; 21 prepared native inputs
  byte-identical to ABI 1.5; common checks 2,039 tests, 624 optional skips,
  0 failures.
- Not yet done: the three 75-second ordered UI runs under ABI 1.6. No ABI 1.6
  sustained ordered UI result is claimed.

**Parked, unvalidated WIP** (not integrated, not reviewed):

- `origin/wip/macos-abi16-0700` (`874a079`, on top of the four branch commits):
  the first ABI 1.6 ordered UI attempts, which all failed at AffText `0x459454`
  (frame 386 capped, 395 uncapped). The diagnosis is that the benchmark's right
  click arrived as another left-click move (order tags 1,5,5), because
  `NSEvent.mouseEvent` can build a right event with buttonNumber 0. The commit
  derives right-button messages from `event.type` and extends the recorder and
  mapper regressions. No APP_BUILD or gate was rerun after the fix.
- `origin/wip/macos-playable-0715` (`d774d14`): adds only an empty
  `m3-abi16-right-orders20.log`. The corrected 20 Hz ordered run was starting
  when Codex was stopped at about 07:15.

**Open stops and owners**

| Stop | Owner |
|---|---|
| CAVE body `BatimentNextEtape` type 3 `0x426aff` at frame 220 (P3/P6/P7) | Rust engine (chain port past 220, `feat/codex-rust-engine`) |
| AffGame viewport `0x415b77` at frame 141 (K1) | Rust engine / renderer port |
| Renderer fatigue domain `AffInfoSelection 0x410be4` (orders at 60 game frames/s stop at frame 2,952) | Rust renderer port, from Graphics' validated domain |
| Production glyphs `AffText 0x459454` | Rust renderer port, from Graphics' validated domain |
| Test A state half beyond frame 220 (and K1 beyond 141) | macOS, once the engine passes those stops |
| Test B: a recorded human session of at least 3,000 frames replayed on the original | macOS (recording and export); replay on the original on the Mac mini |
| Historical elapsed-speed calibration (optional) | AI/runtime or coordinator, who must publish a real Windows timing contract |
| Audio playback (not integrated) | Audio |

**Next steps**

1. Review `874a079`, rerun APP_BUILD and the three 75-second ordered UI runs
   with the corrected right click, then integrate the ABI 1.6 branch.
2. When the Rust engine passes frame 220, extend the Test A state half for
   P3/P6/P7 (and K1 past 141) and record any per-frame divergence here.
3. Record Test B and replay it on the original on the Mac mini.
4. Adopt the renderer fatigue and glyph domains as the engine publishes them,
   then remeasure ordered play at 60 game frames/s and uncapped.

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
human orders. At this ABI 1.4 stage the recorder/export scaffolding was an
independent inspection feature; native orders arrived with ABI 1.5 (see
[ABI 1.5 live orders](#abi-15-live-orders)).

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
ABI 1.3 horizon below is historical. At that stage orders, Test A's game-state
half, Test B, continuous human drags and glyph rendering were separate
dependencies; orders and the reached state half have since landed (see
[Current state](#current-state-2026-10-30-0715)).

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
continuous drags. Reset is disabled while recording. When this recorder first
shipped, orders were unavailable and no recorded answer entered the Rust world;
since ABI 1.5 Jogar applies the same events as orders. Record/export failures are visible
and block exporting an incomplete session as success.

The [input contract](../apps/macos-preview/M3_CONTRACT.md#m33-test-a--frame-input-interchange-and-answer-stream)
describes `ScriptedInput`, `FrameAnswerMapper` and `MacOSSessionRecorder`.
The [Test A answer report](../apps/macos-preview/validation/m3-test-a-answers.json)
compares every declared answer against P1/P2/P3/P6/P7/K1, using the native logs
only as poll requests. All **155,597 answers** match, with no first difference;
all six export/import/export byte round trips match. Native WndProc flag stores
and whole-state hashes belong to Test A's state half, recorded under
[Test A state results](#test-a-state-results) up to the engine's stops. The
3,000-frame human original replay (Test B) is still pending; no M3 acceptance is
claimed.

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
`sh motor/validate.sh` passes unchanged. At this build, engine/order support, the
original timing probe and the state-hash half of Test A were still dependencies
(all since addressed, see the later sections). No 9,200-frame
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

## M3.3 Test B recording and replay pipeline (2026-10-30)

`apps/macos-preview/scripts/test_b_pipeline.py` consumes the canonical JSON
export from `MacOSSessionRecorder`. Normal human play currently stops at the
CAVE tooltip; see [the renderer dependency](#current-normal-ui-dependency). `validate` imports the complete Missions
module and calls its unchanged `carregar_entrada` on the actual saved bytes.
`app` runs the production app C input entry in audited validation policy 2,
starting at accepted S0 and executing the real 128-frame prefix. As in Test A,
this validation tool omits rendering after that prefix. The window's existing
**Validar** button still runs its no-input visual proof; use this command for
recorded-input validation.

`original` calls Missions' unchanged `correr` with the exact exported file.
A read-only observer adds `states.jsonl` alongside the standard
`quadros.jsonl`, `entradas.jsonl`, `comandos.jsonl`, `fronteiras.jsonl` and
`resumo.json`. The child retains Missions' durable native fast-exit behavior;
the parent closes the companion stream and writes its manifest. Neither the
scripted bindings nor WndProc/game bytes are patched by this consumer.

The frame hash covers all mapped game blocks, in original name order with
base/length headers, under the **unchanged published P6 cumulative mask** in
`m3/sondas/P6/mascara-janela.json`. Its source policy is integrity-checked and
its SHA-256 is in both manifests. No exclusions are added for a new session.
Original static executable tables and native stack follow Test A's separate
contract. Indicator hashes (including unit-record hashes, objective/resources,
selection, RNG and UI bytes) are reported separately. Raw original DGROUP,
unmasked mapped-state and display hashes are not substituted for this masked
state hash. A mask mismatch, changed input identity or missing/duplicate frame
cannot pass. Every differing or missing frame goes into the JSON and Markdown
comparison reports. The reused P6 mask does not claim a new session-specific
Missions policy acceptance.

### Recording the real human session

1. Build/open the app, open **Rust ao vivo**, choose **Jogar** and
   **60 quadros/s** (or 20 for a slower recording), and start from
   **Reiniciar**. Advance/run to frame 128 or later without touching the game
   surface or issuing orders. Pause. There must be no earlier unrecorded input;
   otherwise reset and start again.
2. Choose **Nova gravação** and confirm **● Gravando entrada**. Run the session,
   using the map/HUD to select, move, build a CAVE, lodge a colonist, issue a
   depot order while holding **Control**, and recruit. These must be actual
   engine orders; the validation replay's `order_coverage` reports their tags
   (1, 5, 4/type 3, 16, 7/depot argument, 17). Continuous dragging remains outside
   this recorder's supported domain. Keep focus while holding a key; losing
   focus records its release.
3. Continue at least 3,000 frames after recording starts (if its first frame
   is R, stop at R+3,000 or later, and never before frame 3,129).
   Pause, choose **Parar gravação**, then **Exportar entrada** and save, for
   example, `.local/test-b/entradas/human.json`. Preserve that file unchanged.
   Reset is disabled while recording. An engine/recorder stop must be reported;
   it does not count as a complete Test B session.
4. Run `validate`, `app`, then the original replay on the Mac mini, and
   `compare` below. A synthetic session proves plumbing only. Human Test B
   acceptance requires the real recording, all six actual order kinds,
   at least 3,000 replayed frames, and an empty divergence list.

### Commands

Run from this feature worktree (use an unused output directory for each run):

```sh
PIPE=apps/macos-preview/scripts/test_b_pipeline.py
APP="/Users/marcio/git/Rising Lands/local-data/macos-playable/dist/development/RisingLands-ptbr.app"
INPUT=.local/test-b/entradas/human.json
python3 -B "$PIPE" validate --input "$INPUT"
python3 -B "$PIPE" app --input "$INPUT" --bundle "$APP/Contents/Resources/preview" --output .local/test-b/human-app
```

The repeatable synthetic proof drives the actual AppKit window, Metal view,
recording controls, serial event queue and `MacOSSessionRecorder`; it saves the
same canonical export as the native save action:

```sh
python3 -B "$PIPE" record --record-only --app "$APP" --output .local/test-b/validation-ui.json
python3 -B "$PIPE" validate --input .local/test-b/validation-ui.input.json
python3 -B "$PIPE" app --input .local/test-b/validation-ui.input.json --bundle "$APP/Contents/Resources/preview" --output .local/test-b/validation-app
```

On the Mac mini, use a checkout of this feature commit, fetch over HTTPS, and
copy the input byte-for-byte into that checkout. Create the standard checkpoint
once if it is absent:

```sh
python3 -B pesquisas-paralelas/missoes/m3/checkpoint_quadro128.py --saida .local/test-b/quadro128
python3 -B apps/macos-preview/scripts/test_b_pipeline.py original --input apps/macos-preview/validation/test-b/entradas/synthetic.json --inicio .local/test-b/quadro128 --output .local/test-b/original-full
```

Copy the original output directory back without changing its files, then:

```sh
python3 -B "$PIPE" compare --app .local/test-b/validation-app --original .local/test-b/original-full --output .local/test-b/comparison-full.json
```

`--ate FRAME` bounds either replay or the comparison. On the MacBook every
original prefix must use `heavy_lease.py` and `original --minutes 19` (a hard
wall-clock limit below 20 minutes). The full original run belongs on the mini.
Synthetic proof results and the measured runtime estimate are recorded below.


### Current normal-UI dependency

The fresh normal **Jogar** synthetic attempt at runtime `600c41a` stops before
frame **141**, after 140 completed frames, when the CAVE icon's tooltip enters
**AffText `0x459454`**: the production Rust ABI supplies no glyph renderer. This
is an explicit renderer dependency, not a state-hash mismatch. Its actual
recording and stop are preserved in this delivery. No app callback, state edit,
substitute pixels or skipped production draw is installed to hide it. Current
`origin/main` `65d9d50` retains that C ABI boundary.

The synthetic plumbing proof therefore has a separate, explicit command:

```sh
python3 -B "$PIPE" record --record-only --app "$APP" --output .local/test-b/validation-ui.json
```

This uses the app's existing **Validar** UI: real AppKit events and the normal
recorder/save path, while its live world runs the no-input validation chain.
Its report says `capture_policy: record-only` and
`orders_applied_in_capture: false`. The separate audited `app` replay must
actually emit all six order kinds with the required CAVE/depot arguments.
This proves recording/interchange/replay/comparison plumbing; it is **not a
human-play acceptance**. The normal human recording procedure above requires
the engine/Graphics owner to supply the glyph contract before a player can
continue past this tooltip. An actual human Test B remains pending that
provider and the complete original replay on the mini.

### Fresh synthetic pipeline result and per-frame divergence list

Runtime/build **c9bc5d79b048f579a2ee9323db955e7a3cf05086**;
[delivery manifest](../apps/macos-preview/validation/test-b/delivery.json).
This is **synthetic Validar capture**, not human Test B acceptance.

- Real AppKit/Metal Validar recording: **3,572 completed frames after 128**,
  ending at frame **3,700**, **80.6 seconds**; 3,700 accepted no-input surfaces,
  257 prefix states and 11 checkpoints equal. Events traverse NSWindow, the
  Metal responder, serial frame stamping and `MacOSSessionRecorder`.
- Canonical [saved input](../apps/macos-preview/validation/test-b/entradas/synthetic.json)
  passes the complete unchanged Missions validator; SHA256
  `394364c4e57737cf35abd858aebc85809e125a6622661d944b7e2406c6636fe0`.
  The existing stop barrier exports the next frame, **3,701**; the app replay
  validates that extra quiescent frame, and the pending full original command
  includes it. It is not counted among the 3,572
  actually completed captured UI frames.
- Audited app replay: **3,573 frames (129–3,701), no stop**, 254.1 seconds after
  initialization. All six actual order checks pass: select at 133; CAVE
  tag4/type3 at 153; lodge tag16 at 2,073; move tag5 at 2,421–2,423;
  Ctrl depot tag7/word4=2 at 3,228; recruit tag17 at 3,700. Recruitment completion
  is outside this bounded UI recording. Post-prefix rendering is omitted only
  in this explicit replay tool, as in Test A.
- Fresh original replay **129–350**, under `heavy_lease.py`, completes in
  **171.5 seconds** with original code unchanged. **222/222 full mapped-state
  hashes under the unchanged published P6 mask equal**, and all 222 separate
  indicator hashes equal. The [per-frame report](../apps/macos-preview/validation/test-b/comparison-prefix.md)
  and [complete hash rows](../apps/macos-preview/validation/test-b/comparison-prefix.json.xz)
  preserve every comparison.

**State-hash divergences per frame, compared interval 129–350: `[]`.**
Original frames 351–3,701 have not been executed for this input and are not
reported equal. The separate normal-UI renderer stop is **frame141,
AffText `0x459454`**, after frame140; it is preserved in the
[failed normal-UI recording](../apps/macos-preview/validation/test-b/normal-ui-stopped.json.xz).
No normal human session or complete original Test B acceptance is claimed.

Fresh **APP_BUILD passes 116 consumer tests / zero skips, 27 exercise checks,
21 inspection/live checks**. `sh motor/validate.sh` passes, including 75 original
x86 comparisons / zero mismatches / zero skips and 128 Swift/Metal surfaces.
The engine tree is unchanged through this app delivery. The six-frame corrected
original-wrapper preflight also passes all six state/indicator hashes. Initial
runtime-variable and wrapper-pickling setup failures are preserved separately.

Reproduce the bounded original comparison on the MacBook with the committed
input and a fresh app replay output, after preparing the checkpoint above:

```sh
python3 -B "$PIPE" app --input apps/macos-preview/validation/test-b/entradas/synthetic.json --bundle "$APP/Contents/Resources/preview" --output .local/test-b/replayed-app
python3 "/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py" macos-test-b-prefix -- python3 -B "$PIPE" original --input apps/macos-preview/validation/test-b/entradas/synthetic.json --inicio .local/test-b/quadro128 --ate 350 --minutes 19 --output .local/test-b/replayed-original-prefix
python3 -B "$PIPE" compare --app .local/test-b/replayed-app --original .local/test-b/replayed-original-prefix --output .local/test-b/replayed-comparison.json
```

**Exact Mac-mini command**, from a checkout of this feature delivery with the
frame128 checkpoint prepared:

```sh
python3 -B apps/macos-preview/scripts/test_b_pipeline.py original --input apps/macos-preview/validation/test-b/entradas/synthetic.json --inicio .local/test-b/quadro128 --output .local/test-b/original-full
```

The measured prefix rate is **0.773 seconds/frame**. Linear projection gives
**46 minutes for one full 3,573-frame original replay**; allow **45–60 minutes**
for machine/contention and later-frame variation. A fresh checkpoint took
**196 seconds**, separately; reuse an existing verified one. The entire local
final validation sequence held one normal lease, and the original prefix was
well below its explicit 19-minute hard limit. Lease events, commands, source/
artifact hashes, raw logs and all report scopes are in the delivery package.
After a full replay, run `compare` against `.local/test-b/original-full` and
copy every row from its Markdown divergence report into this section; missing
frames or nonempty differences cannot establish acceptance.
