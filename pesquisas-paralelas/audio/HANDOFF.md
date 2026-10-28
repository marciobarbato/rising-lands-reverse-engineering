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
