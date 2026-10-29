# Audio handoff

Owner: the Audio front. Branch `feat/re-audio`, worktree `worktrees/re-audio`. Owned paths: `pesquisas-paralelas/audio/` and `docs/AUDIO.md`. The macOS chat executes this front while it waits for the M1 trigger, as approved by the human on 2026-10-28.

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
branch calls DSB_IsThisSoundPlaying 0x48beb9; the new COM status/position,
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
