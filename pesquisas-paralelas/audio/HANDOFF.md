# Audio handoff

Owner: the independent Audio front, branch `feat/re-audio`, clone `/Users/marcio/git/Rising-Lands-Codex-Audio/repository`. Owned paths: `pesquisas-paralelas/audio/` and `docs/AUDIO.md`. Historical sections below preserve earlier scopes; the current delivery is the final request/record and PCM section.

## Stage 1: bank format and sample decoding (complete)

The full contract (layout, API, effect order, domain, gaps) is in [docs/AUDIO.md](../../docs/AUDIO.md#stage-1-bank-format-and-sample-decoding-complete). This handoff records identities, ordering and validation.

### Identities and addresses

- Intact executable SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb` (the only execution oracle). The analysis PE `26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0` was not used. REA was not needed: every claim rests on the exported intact bytes and native runs.
- 47 exported intervals with SHA-256 in [evidencias/som-manifesto.json](evidencias/som-manifesto.json). The main entries are:
  - bank routines `UseBank_FindIdInBanque 0x48b390`, `UseBank_GetDataHeader 0x48b3b3`, `BanqSon_OpenDataFile 0x48b3ec` .. `BanqSon_LoadDataInMemory 0x48b733`;
  - buffer and decoding `PSB_CreateMySurfaceWithSound 0x48aad4`, `DSB_CreateEmptySoundBuffer 0x48b7b1`, `imaadpcm* 0x48b844..0x48bd12`, `LoadSoundBuffer_* 0x48c070..0x48c202`;
  - file and allocation wrappers `0x48c008..0x48c2d7`;
  - identity `HndSound_LoadDataInfo 0x48a0f4`, `PlaySnd_CreateSoundPath 0x48a834`, `SoundFile 0x48a87f`, `PlaySnd_MakeID 0x48a894`.
- IMA tables: index words at `0x498f6c`, step words at `0x498f8c`. The decoder reads them through `dword [n*2 + base-2] >> 16`.
- Sound bank identities are in [ambiente_audio.py](ambiente_audio.py). `relatorios/fontes.json` (core-owned) does not list `INSTALHD/SOUND`; that is reported to the coordinator, not edited here.

### API inputs and widths

- `BancoSom(registro: writable bytearray 28, endereco: u32)`.
- `GlobaisSom` takes:
  - `nome_arquivo`: writable 104 bytes;
  - `diretorio`: writable 256 bytes;
  - u32 values `contador_variantes`, `contador_alocacoes`, `janela`, `comprimido` and `directsound`.
- `carregar_info_som(globais, registro >= 32 writable bytes, id u32, banco, ecx u32, argumento u32)`.
- `criar_superficie_som(sistema, globais, banco, cabecalho_dados 16 bytes)` returns `(buffer object or 0, [decoder EAX])`.
- Decoders take raw bytes and a u32 block alignment, and return `(bytes written, EAX)`.

### Mutation and callback order

- **Open.** The call order is path (getcwd, free), `.HED` open, 16-byte read, then the count/size stores, alloc, body read and close. Then come the header-pointer store, the `.SND` open and handle store, and finally +0x14, +0x10, +0. Failure branches keep earlier stores, as listed in AUDIO.md.
- **Surface, ADPCM file path.** `_llseek(h,0,0)`, `CreateSoundBuffer(size*4)`, `_llseek(h,offset,0)`, `_hread(size)` into the compressed buffer, `Lock(0,size)`, decode, `Unlock(p,size)`.
- **Surface, PCM file path.** `_llseek(h,0,0)`, `CreateSoundBuffer(size)`, `_llseek`, `Lock`, `_hread` straight into the buffer, `Unlock`.
- **In-memory path.** No seeks, a memory copy or decode from the resident data.
- **Errors.** Provider exceptions propagate after earlier effects, with no rollback. Unsupported original behavior raises `DependenciaSom(endereco)`.

### Validation (this stage)

- **Original-only captures.** Committed before the translation, in their own commit. The native runs covered:
  - 551 sounds: A 14, B 102, P 435;
  - 43,281,606 / 137,098,639 / 823,182,052 file-path instructions;
  - every ID lookup;
  - 5 counter values per entry;
  - all `LoadDataInfo` IDs plus 2 absent IDs;
  - 6 `MakeID` inputs and 3 working directories;
  - 17 open/validation/dead-code cases plus the in-memory-after-reads case;
  - 11 direct decoder calls (mono, stereo, saturation, invalid index, short tails);
  - 8 synthetic surfaces: stereo, PCM, unsupported format, byte13=200, in file and memory paths.
- **Local suite** (`python3 -B scripts/check.py --domain audio`). It checks the interval and table hashes against the intact EXE and the bank identities. It replays every capture record in Python, including all 551 buffers, regenerates the catalogue, and runs domain and dependency tests. Native tests are skipped in this mode.
- **Native suite** (`RISING_EMULAR=1`). It runs the structure scenarios, every sound of bank A and a P subset (PCM, byte13=200, five-variant entry, largest sample), each compared fresh, native against Python.
- **Full fresh comparison.** `validar_som.py` covers all three banks; its report is `validacao/x86-som.json`.

Actual counts, SHAs and push results for this stage are reported to the coordinator in the stage report.

### Remaining gaps

Queue state (`HandlSnd_*`, `LSB_*`, `PSB_*` beyond buffer creation, `WaitSnd_*`), `PlaySnd_PostSound`/`Manage`, emitters, `BanqSon_Close`/`Free*`, `DSB_Destroy`, DirectSound initialization and playback, and real DirectSound buffer content and lock semantics. The bindings will migrate to core's Stage 15 generic facility when it is committed.

### Requested contracts

- **core:** the generic binding facility (Stage 15). The audio bench will migrate its `_lopen`/`_hread`/`_llseek`/`_lclose`/`GlobalAlloc`/`GlobalFree`/`MessageBoxA` slot bindings and its COM stubs onto it.
- **core:** `relatorios/fontes.json` should list `INSTALHD/SOUND/{A,B,P}.{HED,SND}` (sizes and SHA-256 in `ambiente_audio.py`).
- **macos (M2/M3):** consume `criar_superficie_som` and `catalogo-amostras.json`. Play the written region (`decoded_bytes`) at the header's rate and channels. The unwritten tail is fixture fill, not audio.

## Codex resumption: light Stage 2 inventory

The new human request of 2026-10-28 supersedes the historical stop. The current
coordinator is `01a183e4-456e-77d0-9c6a-81b1c72ae887`; historical `local_`
identities remain historical. This chat owns only the audio worktree while M1
is unavailable. The macOS worktree has not been rebuilt or modified.

Before helper start, `feat/re-audio` was clean at
`85d54ac651eb578afa528d167b229619258995e6`, with no local commits outside main.
The intact capture commit `fa4a759d13107f84e24bd1f2af9d01d0b72403c3`, decoder
implementation `0fc99df90ebcadb69f8e6fa5f6603ceae89e79fd` and report commit
`9a0c171` were each verified as ancestors of fetched main
`8810b3730a0fb788af3eac2b447dea65372f597f`. The prescribed start helper resumed
the same checkout; a clean fast-forward moved it to that main. No worktree,
failed candidate, earlier capture, manifest or original media was removed or
rewritten.

The new static exporter [extrair_filas_som.py](extrair_filas_som.py) and separate
[53-interval manifest](evidencias/filas-som-manifesto.json) preserve the intact
request/queue bytes for Stage 2. The [current capture-first plan](../../docs/AUDIO.md#stage-2-requestqueue-original-first-inventory)
records exact field widths, partial writes, PostSound register inputs,
Manage's shared/fall-through bodies, PSB/LSB tables, literal-RET waiting sorter,
and the critical waiting 69→70 alias into queue/dictator globals. These are
static observations, not a reconstructed queue or fresh execution result.

Validation separation for this light window:

| Item | Status |
|---|---|
| Existing bank/sample implementation and original captures | Preserved; already integrated on main |
| Existing 551-sound three-way report 9a0c171 | Inspected as prior evidence; not rerun |
| New request/queue original bytes | Static export from the intact verified EXE; 53 intervals |
| New queue Python behavior | Not implemented; captures must precede translation |
| New original-x86 comparisons/Ghidra | Not run; no heavy slot granted |
| Full audio/domain/integration gate | Not run in this light window |
| Stage 2 main integration | Not performed |
| Complete audio playback or real-mission flow | Not tested; remains unsupported |

Light checks performed here: two namespace/contract-presence unit tests passed;
all 53 newly exported interval hashes and 88 initialized-data bytes matched the
intact image; exporter syntax, maintained documentation links and diff
whitespace passed. These checks ran no emulator and decoded no sound corpus.

No heavy job has started, so no heavy lease is held. The next required action
is coordinator scheduling of an original-first capture window. Light notes
remain within this one current stage; no subsequent implementation is started.


## Independent continuation — M2.2 soundness and stage-2 foundation

Dedicated clone `/Users/marcio/git/Rising-Lands-Codex-Audio/repository`, branch
`feat/re-audio`. The remote Audio base c464dcd was 397 commits behind main;
origin/main was merged into the feature at b837d8943ad5d23cb0e3d43540325253587d86c2.
No main push, integration helper, force-push or other-front edit is performed.
The read-only CD is linked inside the dedicated Audio workspace. Analysis
requirements live only in ignored `.local/python` (Unicorn 2.1.4, Capstone
5.0.7, pefile 2024.8.26). Original media and runtime were not modified.

### Bounded result

See [M22_SOUNDNESS.md](M22_SOUNDNESS.md) and
[validacao/m22-soundness.json](validacao/m22-soundness.json) for exact hashes,
addresses, input provenance, watched ranges, source identity and limitations.

* Original-byte inventory: 101 sound/MCI intervals, intact executable only.
* Original pump input audit: 258 accepted state boundaries, one distinct
  private sound/MCI image; 3 isolated calls return in 4.370 s total preparation.
* Native declared-boundary replay: 128 frames, **257/257 summaries equal**,
  186.752 s. The initial three-byte hook prefix is superseded for width coverage
  by the chained probe's 15-byte prefix (static original text maximum 10 bytes).
* Native chained original pumps: 257 phases, 189.970 s, MCICD_Play 130,
  PlaySnd_Manage 128, MCICD_Manage 128. Code unchanged. **Not strict whole-state
  equality:** the private 0x498f5c byte is accepted 1 / actual 0 in 256 phases;
  every other captured byte equals. 0x521f88 receives an already-zero u32.
* Private watched ranges have zero game/display readers, while sound-library
  readers and shared CD flag/cursor accesses are recorded positively.
* The first native-watch attempt failed before startup because the convenience
  factory required a BIN ISO. The probe now reuses the exact accepted named
  Windows answers through committed dataclasses; no ISO label is guessed.
  [Run history](validacao/m22-sound-run-history.json) retains this failure.

All native jobs use the unchanged shared lease. M2 probes set an 18-minute
SIGALRM after lease acquisition; each phase has a 180 s bench limit. Diagnostics
and actual differences are saved before a phase failure exits. Exact reproduction
commands are in M22_SOUNDNESS.md. No native job exceeded four minutes, and no
Mac mini run is requested for this completed slice.

### Stage-2 index helpers and validation

Original capture `679bd00` precedes translation. `WaitingSlotIndex` implements
only WaitSnd_GetFirstFreePlace/GetMaxIndice/SorryGiveBackOnePlace/FindPlace over
explicit inherited 4-byte and 880-byte buffers. Objects retain identity, no
initialization/defaults/callbacks occur, and effects are in original order.
Supported reservation domain 19..70; unknown values stop by original address
before mutation. Widths and exact API are in docs/AUDIO.md.

The original-only fixture covers 133 cases; fresh native/Python/committed
comparison passes **133/133**, 0.014 s, with a five-minute SIGALRM. Full playing
records are compared byte-exactly, not only return values. No DirectSound
provider is supplied. The implementation hash is in
[indices-fila-audio-native.json](validacao/indices-fila-audio-native.json).

Exact fresh differential command (from the clone):

```sh
python3 '/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py' \
  codex-audio-waiting-slot-differential -- \
  /Users/marcio/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B \
  pesquisas-paralelas/audio/validar_indices_fila_audio.py \
  --output .local/audio/waiting-slot-repeat-001.json
```

The validator requires an explicit --output path and refuses existing files
(including symlinks) before any native capture starts. Relative paths use the
current working directory; choose another fresh .local/audio/... name for each
rerun. Final report creation is exclusive too, protecting against a later race.
The committed original report remains untouched. The original-only capture command is the
same lease wrapper with `capturar_indices_fila_audio.py` (also exclusive output).

`python3 -B scripts/check.py --domain audio`: **30 discovered, 27 passed,
0 failures, 3 explicit optional native skips** (the unchanged Stage-1 native
bank/structure tests). Ten new replay/API tests pass with zero skips. The
fresh 133/133 native helper differential and the two original frame replays
are separate actual native results, not those optional skips. Earlier 551-sound
bank/decoder achievements remain integrated baseline and were not rerun to
inflate this round's counts.

### Remaining dependencies and ownership requests

The no-playing-CD input is essential: game byte 0x4e2f28 is shared, and the
zero branch consumes shared cursor 0x4e1d18. Playing-CD, initialized MCI/sound,
arbitrary dynamic sound heaps and M2.3 are not covered. No accepted policy or
milestone record changes are requested by this audit.

Next Audio capture boundary is HandlSnd_Insert 0x48a218, including [EBX] at
0x48a225 and 44-byte record population/compaction. ClearListe's initialized
branch calls DSB_IsStopped 0x48beb9; the new COM status/position,
volume, play/stop fixture contract remains required. The index helper alone
must not replace PostSound/Manage with a successful request or playback.
Stage-3 game emitters and owners' pending descriptors remain unchanged until
the complete request contract is validated and integrated by Claude.

No new engine, rendering, mixer, audio device output, artificial callback or
empty success stub is introduced. Full queue reconstruction and M3 sound
remain incomplete; this delivery supplies a bounded soundness proof plus a
small tested queue foundation.


### Reproducibility follow-up

The fresh helper validator now accepts required `--output` and checks refusal
to overwrite before importing/starting native capture. The exact rerun command
above uses a fresh ignored output. CLI regression tests cover help/required
arguments, pre-capture overwrite refusal and report creation with a mocked
capture; they do not rerun unchanged original algorithms or claim a new native
result. The original 133/133 report and implementation hash remain unchanged.

Latest non-native gate after this follow-up: **34 discovered, 31 passed,
0 failures, 3 unchanged optional native skips**. The four new CLI tests pass
without executing original instructions. The original native report is
byte-identical; no unchanged native algorithm was rerun. See
[validator-reproducibility.json](validacao/validator-reproducibility.json) and
[the gate log](validacao/validator-reproducibility-check.log).


## Current delivery: request records and declared-platform PCM queue slice

The human authorized this independent continuation after the prior Audio
`e06e787` delivery was integrated. The clone was inspected clean, remote feature
history was fast-forwarded, and latest main was merged by fast-forward to
`a7405668e630650f67f6ff792bd07348ae7697f7`. Main was not checked out, pushed or
integrated. All new changes belong to Audio only; no milestone is established.
Read-only CD input is `/Users/marcio/git/Rising Lands/source/cd`, linked as
`../source/cd` inside the dedicated Audio workspace. Analysis packages remain
in ignored `.local/python`; original media, runtime and other checkouts are
unchanged. The only external local coordination access is execution of the
unchanged human-mandated shared lease.

### API, domain and original-first provenance

Current API and original addresses are in
[docs/AUDIO.md](../../docs/AUDIO.md#current-requestrecord-api-and-declared-pcm-bridge--2026-10-29).
[QUEUE_COM_CONTRACT.md](QUEUE_COM_CONTRACT.md) specifies each scalar width,
protected memory range, original call order, COM answer and dependency address.
The provider is [fila_audio.py](fila_audio.py), with frozen-input replay in
[reproduzir_fila_audio.py](reproduzir_fila_audio.py). Its constructor retains
caller objects and creates no initialized audio state or backend defaults.

The original-only research sequence is `0af28b0`, `7e29ac1`, `3806164`,
`ba251fa`; its first request/record implementation is `6bd1ca9`.
Original-only creation descriptors/output evidence is `d0bfdd7`; PCM
creation/fill/start and error evidence is `fd8642c`. The subsequent bridge
implementation reuses Stage-1 `criar_superficie_som` rather than reimplementing
sample decoding. The 551-bank/sample baseline was preserved and not rerun as
new native work. Full commit SHAs accompany the delivery message.

Preserved diagnostics include the v1 incomplete fixture answers, v2 missing
seek binding, the v3/v4 CRT interval stop (earlier premature Create attribution
corrected), v5's actual creation stop, and all v6 replacement effects. A rejected
first v9 _hread declaration used wrong IAT 0x523200; original instruction
0x48c042 and the existing Stage-1 map prove 0x5231e8. The corrected run is
separate; [queue-create-run-history.json](validacao/queue-create-run-history.json)
retains the setup failure. No frozen evidence or accepted policy was edited.
The maintained legacy symbol at 0x48beb9 is corrected to `DSB_IsStopped`.

### What passed

[v9 original-only capture](evidencias/captura-fila-audio-original-v9.json):
**244 actual intact-original calls / 238 scenarios**. The seven-call persistent
PostSound sequence retains every intermediate image. All 235 returned scenarios
and three intentionally unbound cases match Python: full inherited memory,
reference and slot back-pointers, aliasing index 70, partial writes, ordered COM
calls/arguments/results and meaningful EAX values. The three expected stops
are missing CreateSoundBuffer at caller 0x48b834 and two missing Lock bindings
at caller 0x48c097; earlier PSB reservation -1→0, dirty resets and seek calls
remain visible. They are dependency tests, not successful device creation.

The new defined PCM path additionally reaches CreateSoundBuffer, Lock, explicit
_hread bytes, Unlock, GetStatus, SetPosition, SetVolume and Play in that order.
The declared matrix covers null/non-null output independently of HRESULT,
Lock/Unlock error results, 64/32/0 returned bytes, already-playing status and
position/volume/Play failures. A start failure still moves the request into a
playing record exactly as the original does. No actual sound is emitted and no
real DirectSound allocation, initialization or timing is inferred.

[fila-audio-three-way-v2.json](validacao/fila-audio-three-way-v2.json): fresh
native/frozen/Python comparison **passed**, 244 calls, 238 scenarios, three
expected stops, zero unexpected failures, 0.965 seconds. Earlier v7 fresh
report remains [v1](validacao/fila-audio-three-way-v1.json): 230 calls, 224
scenarios, one expected stop, 0.871 seconds. These reports are separate, not
summed as independent unique scenario coverage. The provider hash is recorded
in each corresponding report.

### Exact bounded reproduction

Run from the independent clone. Choose a fresh output path; existing files or
symlinks are refused before importing/starting native capture. Output creation
is exclusive as well. Do not overwrite committed reports.

```sh
python3 '/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py' \
  codex-audio-queue-repeat-001 -- \
  /Users/marcio/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B \
  pesquisas-paralelas/audio/validar_fila_audio.py \
  --output .local/audio/queue-repeat-001.json
```

The same wrapper with `capturar_fila_audio.py --output <fresh-path>` performs
an original-only run. Each call permits at most 20,000 original instructions;
the capture installs SIGALRM 600 seconds after acquiring the lease. No new
native queue job exceeded two seconds, and no Mac mini time is requested for
this slice. The native runtime is read-only and must see the clone's ignored
analysis packages. Non-native checks run outside the lease:

```sh
python3 -B scripts/check.py --domain audio
```

### Remaining validated boundary

Manage supports the captured empty/one-active-logical states and exactly one
new file-backed PCM request with no loaded physical slots. Multiple pending
requests stop at 0x48a80c; loaded physical lookup/reuse at 0x48acd3,
physical transfer at 0x48ac53, promotion at 0x489e6d, dictator lifecycle at
0x48a0a1 and dictator creation at 0x48a702 remain outside. Queue bridging for
resident/compressed data stops at 0x48aad4 (their separate Stage-1 sample APIs
remain baseline). Wrapped/short Lock outputs, unwritten output/status words,
real buffer ownership and asynchronous/device initialization remain undeclared.
These are explicit caller/provider boundaries, not fabricated successful
callbacks. Future original-first captures may extend them.

No emitter/game-side code, M2.3, renderer, native application, acceptance record
or formal milestone is changed. This is a tested queue foundation plus a
bounded declared-platform PCM path; complete audio stages 2/3 and M3 audio
acceptance remain incomplete.


Final non-native gate: **49 discovered, 46 passed, zero failures, three unchanged
optional Stage-1 native skips**, 11.052 seconds. All **15 new queue replay/API
tests pass with zero skips**. Three additional CLI checks confirm help, required
--output and refusal to overwrite the committed report before native capture.
The exact gate log is [audio-queue-check.log](validacao/audio-queue-check.log);
[audio-queue-validation.json](validacao/audio-queue-validation.json) records
source hashes, command, actual skips, CLI results and the fresh native report.
The 244-call fresh comparison ran under the lease despite the optional baseline
native skips; those are separate results. No unchanged 551-sound native corpus
was rerun or claimed anew.


## Current continuation: reuse, promotion, concurrency and sample-data bridge

This independent round resumes the clean Audio clone and fast-forwards
`feat/re-audio` to fetched main `8e90beb412a63d5f00965c381d21bc9a800257bc`.
Both remote Audio history and `73196fc` ancestry were verified. No other-front
checkout, main branch, accepted capture or milestone file is modified. The
preceding delivery sections remain historical; this section and
[QUEUE_CONTINUATION.md](QUEUE_CONTINUATION.md) define the new current scope.

Original-only leaves (`0a28d14`) precede their translation (`01dd333`). Original
concurrency/data research (`e410c3e`) precedes composition (`c1e54a2`). Original
persistent-sequence evidence (`67f3bdb`) precedes its multi-operation replay.
All earlier original queue v1–v9 diagnostics remain unchanged.

The provider covers captured physical/logical ID+bank lookups, slot replacement,
physical destruction/promotion, explicit duplication, logical reservation,
physical playing→waiting transfer and ClearListe's real IsStopped guards.
Manage composes two/three simultaneous same-bank or distinct-bank requests,
with explicit capacity guards. Stage-1 handles resident/file PCM and mono ADPCM;
no competing decoder or device model was written. The 256-created/64-Locked
ADPCM write extent, inherited tail and all status/HRESULT differences match the
original. The complete API, widths, callback order and protected domains are in
[docs/AUDIO.md](../../docs/AUDIO.md#current-buffer-reuse-and-concurrent-data-bridge--continuation).

Original v3: **139 intact calls / 132 scenarios, zero stops**, 0.685 seconds.
The eight-call persistent sequence begins from one declared input, then uses
only earlier original outputs: three PostSound calls, Manage, physical-owner
cancellation/logical promotion, a different-bank repost, Manage and logical
volume-zero cancellation. Every intermediate memory image and EAX is captured;
no state is rewritten between calls. Physical/duplicate object identities and
external-reference words are preserved. These are declared platform fixtures,
not real initialized audio or audible playback.

Fresh [native/frozen/Python differential](validacao/continuacao-audio-three-way-v1.json):
**139 calls / 132 scenarios equal, zero stops/failures**, 0.681 seconds. Ten new
continuation replay/API tests pass without skips. Prior baseline queue evidence
and the full 551-sound bank/decoder achievements are preserved, not rerun or
added to these native totals.

Fresh native reproduction, from the independent clone (choose a new filename):

```sh
python3 '/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py' \
  codex-audio-continuation-repeat-001 -- \
  /Users/marcio/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B \
  pesquisas-paralelas/audio/validar_continuacao_audio.py \
  --output .local/audio/continuation-repeat-001.json
```

Existing outputs/symlinks are refused before importing native capture; creation
is exclusive too. Fresh original differences and comparison errors are saved
before failure exits. `capturar_continuacao_audio.py` under the same wrapper
performs original-only capture. Each call has a 50,000-instruction limit; the
job has a 600-second alarm/deadline after acquiring the unchanged shared lease.
All continuation native jobs took under one second; no Mac mini run is needed.

Remaining work is original-first dictator lifecycle/creation, broader saturation
and unsupported fault continuations, device initialization, wrapped/short Lock
regions, unwritten output/status words and asynchronous buffer lifetime. The
new queue data proof is mono ADPCM/full read; stereo remains separately decoded
in Stage-1. Missing scratch/short compressed reads stop at 0x48c14f/0x48c15f
with earlier effects retained, rather than returning fake success. No broad
mission playback, M2.3 or M3 milestone acceptance is claimed.


The required Audio gate passes: **59 discovered, 56 passed, zero failures,
three unchanged optional Stage-1 native skips**, 11.300 seconds. All **10 new
continuation tests pass with zero skips**. CLI checks confirm help, required
output and refusal before native capture for an existing report. See
[audio-continuation-validation.json](validacao/audio-continuation-validation.json)
and [the exact gate log](validacao/audio-continuation-check.log). The fresh
139-call native differential is separate actual leased execution, despite the
optional baseline skips. The coordinator's exact committed native bundle build
is performed next; its actual outcome is recorded separately.


### Required committed native bundle build — first attempt preserved

The exact coordinator command was executed from committed Audio
`588a7942e6a0923574e1a56047bda8213a2f8ed6` merged with main `8e90beb`:

```sh
RISING_PYTHON_RUNTIME='/Users/marcio/.cache/codex-runtimes/codex-primary-runtime/dependencies/python' \
  ./compilar-jogável --development-ref HEAD \
  --inputs-root '/Users/marcio/git/Rising Lands' \
  --data-root '/Users/marcio/git/Rising-Lands-Codex-Audio/repository/.local/macos-playable'
```

**Overall exit 1; native UI smoke failed.** The build compiled the ARM64 app,
verified ARM64 Python and the local signature, and passed **71/71 consumer
tests, zero skips**, 41.051 seconds. The first native window smoke then
reported original player-visible error `Tempo limite de 45 segundos na abertura`,
with nativeWindowVisible=true and empty Python stderr. Inspection smoke was
not reached. Compilation/signing and consumer success do not imply UI success.
No timeout was increased, app file modified or native build repeated.

The first JSON is preserved byte-for-byte in
[audio-continuation-native-smoke-first.json](validacao/audio-continuation-native-smoke-first.json).
[The build report](validacao/audio-continuation-native-build.json) records the
exact command, commit, original PNG paths/hashes and disposition. All three
first-attempt PNGs remain under the clone-local build/logs directory. The
[full launcher log](validacao/audio-continuation-native-build.log),
[consumer log](validacao/audio-continuation-consumer-tests.log),
[architecture](validacao/audio-continuation-architecture.log) and
[codesign verification](validacao/audio-continuation-codesign-verify.log) are
committed. Original inputs remain read-only; every output is inside this clone.

The failure was reported immediately to the parent coordinator, after AppKit
finished, allowing its independent macOS readiness fix/smoke to proceed without
concurrent UI runs. The remaining UI-startup issue belongs to that front; this
Audio delivery does not repair or suppress it. The successful Audio gate and
139-call native differential remain separate results. Final build validation
must be rerun by the coordinator with its integrated readiness fix.


## Current independent round: entry-word256 lifecycle

The clone was clean and latest main was fetched/merged by fast-forward to
`a7427fd0e416d212f08af7f0df3d36a224d12f2d`. Prior Audio `a711ff9`, remote feature
history and latest-main ancestry were verified. Work remains in this independent
clone on `feat/re-audio`, with only Audio-owned writes and no main push or merge.
Read-only CD/runtime paths and clone-local outputs remain unchanged. Python is
the validated reference/harness for the coordinator's future Rust+C ABI engine;
this round introduces no live device implementation or new ABI/protocol.

[DICTATOR_CONTRACT.md](DICTATOR_CONTRACT.md) defines the original hashes,
addresses, allocation/COM declarations, API widths, supported domain and gaps.
Original research `69d57aa` precedes its translation. The new API is
`init_dictator()`, `clear_dictator()`, `set_game_volume(u32)` and
`create_sound(record_address)`, composed by Manage/ClearListe. Entry-word256
admission now reaches the captured separate record/slot lifecycle. Initial
allocation contents, object/reference identity, forced flags0, partial stores,
status/HRESULT branches and exact callback order are preserved.

Original-only v3 has **140 actual original entries /35 scenarios**,0.432 seconds:
34 returned scenarios and one expected NULL-allocation MessageBoxA dependency.
The fresh [original/frozen/Python comparison](validacao/dictador-audio-three-way-v1.json)
passes those 140 entries/35 scenarios with **zero failures**,0.423 seconds.
Ten new tests pass without skips, including an eight-call persistent
pending/clear/relaunch sequence. Every completed step's memory and meaningful
API results match. Void EAX remains raw native observation metadata: it is
compared fresh-native to frozen-native, not invented as a Python API result.
Earlier 139-call and 244-call queue corpora and 551-sound decoder results remain
historical baseline; none is counted as fresh native coverage in this round.

Preserved diagnostic v1 allowed OurAlloc only through 0x48c23f, missing its intact
RET 0x48c240. Its field native_calls 140 counted planned steps, although35 were
attempted. This report is retained as diagnostic and is not claimed as 140
executed calls. V2 fixes the interval/count accounting and records128 actual /
140 planned:12 explicit Play mismatches reveal that the dictator clears the
requested loop flag, plus the NULL-allocation boundary. V3 changes only the
declared answer list and executes all 140 entries. No original instruction or
predecessor evidence was patched.

Exact fresh reproduction (choose a new ignored output name):

```sh
python3 '/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py' \
  codex-audio-dictator-repeat-001 -- \
  /Users/marcio/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B \
  pesquisas-paralelas/audio/validar_dictador_audio.py \
  --output .local/audio/dictator-repeat-001.json
```

Existing files/symlinks are refused before native capture; final report creation
is exclusive. Fresh differences are retained before failure exits. The same
wrapper with `capturar_dictador_audio.py --output <fresh-path>` runs original-only
capture. All native jobs use unchanged shared heavy_lease.py, SIGALRM 600 plus a
monotonic 600-second deadline and 50,000 instructions/call. Each took under one
second; no Mac mini request is needed. Original media/runtime remain read-only.

Remaining boundaries are MessageBoxA allocation failure 0x48c227, actual device
initialization, unwritten outputs/status, wrapped/short Lock, asynchronous
lifetime and broader saturation/fault/stereo queue composition. No game emitter,
M2.3, rendering, milestone or app implementation is changed. The preceding
45-second B smoke is historical unknown timeout evidence; it did not prove slow
initialization. The coordinator later diagnosed an occluded final animation
barrier in its own reproductions. This round uses the integrated readiness fix;
Graphics1.3/macOS1.2 compatibility is separately coordinator-owned.


The required Audio gate passes **69 discovered,66 passed,zero failures,three
unchanged optional Stage-1 native skips**,12.011 seconds. All **ten new tests
pass without skips**. CLI checks pass for help,required output and refusal of
an existing report before native capture. Exact gate/source identities and
new evidence file/byte sizes are in
[audio-dictator-validation.json](validacao/audio-dictator-validation.json) and
[the gate log](validacao/audio-dictator-check.log). The required exact application
build is run from the committed implementation next and recorded separately.
