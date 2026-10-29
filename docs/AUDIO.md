# Audio contract

Owner: the Audio front (`feat/re-audio`, `worktrees/re-audio`). Owned paths are `pesquisas-paralelas/audio/` and this manual. Audio is a second-wave domain of the [MONDE01 roadmap](ROADMAP_MONDE01.md#second-wave). On 2026-10-28 the human approved anticipating it in the macOS chat while that chat waits for its M1 trigger. No eighth executor was created. When the coordinator triggers M1, the chat returns to the `macos` front and audio pauses at its last integrated stage.

Addresses apply to executable SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`. The normalized analysis PE (`26c4534b…64d0`) is analysis-only. The original sound banks are `INSTALHD/SOUND/{A,B,P}.HED` and `.SND` on the read-only CD copy (`../source/cd`); `TICKONE.WAV` sits at the CD root and is not part of the banks. `relatorios/fontes.json` does not list the sound files, so their sizes and SHA-256 are recorded in [`ambiente_audio.py`](../pesquisas-paralelas/audio/ambiente_audio.py) and the [audio manifest](../pesquisas-paralelas/audio/evidencias/som-manifesto.json). PT-BR voices and music are preserved byte-exactly. They are never re-recorded, translated or normalized, and no decoded audio is committed.

Stage 1 is the integrated baseline. The independent 2026-10-29 continuation adds a bounded M2.2 soundness audit and the first original-first queue-index slice; full stages 2 and 3 remain incomplete.

## Original subsystem inventory (symbols from the original SBL)

| Group | Routines |
|---|---|
| Bank files | `BanqSon_OpenDataFile 0x48b3ec`, `BanqSon_CloseDataFile 0x48b446`, `BanqSon_ControleValiditeHeader 0x48b44e`, `BanqSon_LoadHeader 0x48b496`, `BanqSon_FreeHeader 0x48b596`, `BanqSon_Open 0x48b5a6`, `BanqSon_FreeDataInMemory 0x48b650`, `BanqSon_Close 0x48b687`, `BanqSon_LoadAllData 0x48b6e7`, `BanqSon_LoadDataInMemory 0x48b733` |
| Sample decoding | `LoadSoundBuffer_LoadDataFromFileInSoundBuffer 0x48c070`, `LoadSoundBuffer_DecompactInSoundBuffer 0x48c0bc`, `LoadSoundBuffer_PlaceOnSample 0x48c137`, `LoadSoundBuffer_LoadCompactedData 0x48c141`, `LoadSoundBuffer_InitCompressedBuffer 0x48c16c`, `LoadSoundBuffer_FreeCompressedBuffer 0x48c18d`, `LoadSoundBuffer_LoadDataFromMemoryInSoundBuffer 0x48c1a8` |
| Sound identity and paths | `PlaySnd_CreateSoundPath 0x48a834`, `SoundFile 0x48a87f`, `PlaySnd_MakeID 0x48a894`, `HndSound_LoadDataInfo 0x48a0f4` |
| Library lifecycle | `PlaySnd_InitSoundLib 0x48a89f`, `PlaySnd_FreeSoundLib 0x48aa04`, `HandleSnd_InitDictator 0x489f39`, `HandleSnd_FreeDictator 0x489f76`, `HandleSnd_DestroyDictator 0x489f04` |
| Game requests | `PlaySnd_PostSound 0x48aa79`, `PlaySnd_StopSound 0x48aac0`, `PlaySnd_StopAllSound 0x48aac5`, `PlaySnd_Manage 0x48aaca`, `PlaySnd_PostVolume 0x48aacf`, `PlaySnd_SetGameVolume 0x48aa45` |
| Handle and queue logic | `HandlSnd_Insert 0x48a218`, `HandlSnd_SetVolume 0x48a14a`, `HandlSnd_AffectVolumeOut 0x48a517`, `HandlSnd_GetAverageVolume 0x489dac`, `HandlSnd_ClearListe 0x489f96`, `HandlSnd_TriWaitingHandle 0x48a664`, `HandlSnd_ValidateListe 0x48a7f9`, `HandlSnd_LaunchWaitingSound 0x48a803`, `HandleSnd_StopHandle 0x48a438`, `HandleSnd_StopAllHandle 0x48a4a8`, `DestroyOnlySound 0x489e35` |
| Logical/physical/waiting tables | `LSB_*` (`0x48ad3c`..`0x48aeb3`), `PSB_*` (`0x48aad4`..`0x48ad0c`), `WaitSnd_*` (`0x48aef8`..`0x48b38f`) |
| DirectSound boundary | `InitDirectSound 0x48bdf7`, `FreeDirectSound 0x48be56`, `IsInitDirectSound 0x48be80`, `SetPrimaryFormatDirectSound 0x48bd14`, `DSB_CreateEmptySoundBuffer 0x48b7b1` |
| Game-side emitters | `TryLanceAttaqueSound 0x440ac0`, `VoixOffAsk 0x41a1ac`, and the pending `PlaySnd_PostSound` descriptors already published by core, economy and combat (for example `PlaySnd_PostSound(0x50, (type<<16)|0x100, 0, volume, unit)` in [combat](COMBAT.md)) |

## Ownership boundary

- Audio implements the bank readers, sample decoding, sound identity, and the logical/physical/waiting queue state reached by `PlaySnd_PostSound`/`PlaySnd_Manage`.
- DirectSound and Windows file/allocation calls are **declared bindings**. They record exact arguments and fixture results, and they stop when the fixture cannot honor the semantics. Audio does not reconstruct the DirectSound mixer.
- Core, economy and combat keep their emitting call sites. They replace a pending descriptor with the audio provider only after the audio contract for that request is integrated.
- The macos front plays decoded samples at M2/M3. It consumes committed audio APIs only.

## Stage 1: bank format and sample decoding (complete)

### Evidence

[`extrair_som.py`](../pesquisas-paralelas/audio/extrair_som.py) exports 47 intact intervals with SHA-256 into the [manifest](../pesquisas-paralelas/audio/evidencias/som-manifesto.json) and [disassembly](../pesquisas-paralelas/audio/evidencias/som-rotinas.asm). Each interval runs from its SBL symbol to the next one, minus zero padding. The manifest also holds the IMA tables, the strings, the globals, the import slots and the bank identities. Watcom CRT intervals that run natively (`sprintf` and its character sink, `__prtf`, `memset`, `__STOSB`, `__STOSD`) are hashed; `__prtf` is listed by hash only.

The original-only captures were produced by [`capturar_som.py`](../pesquisas-paralelas/audio/capturar_som.py) and committed before the Python translation:

- [`captura-som-estrutura.json`](../pesquisas-paralelas/audio/evidencias/captura-som-estrutura.json): open and validation branches, index lookup over every ID, path building, direct decoder calls and synthetic surfaces.
- `captura-som-banco-{A,B,P}.json`: every data header of every bank decoded natively, plus the dead-code in-memory path.

Commercial bytes appear only as SHA-256.

### Bank file layout (HED/SND)

| Bytes | Content |
|---|---|
| HED 0..15 | `ABCD` magic, u32 header body size, u32 SND size, u32 entry count (stored as u16 in the bank record) |
| HED body, 12 bytes per entry | u32 sound ID, u16 word (100 or 256 in the corpus), u16 variant count, u32 offset of the first data header in the body |
| HED body, 16 bytes per data header | u32 SND offset, u32 SND bytes, u8 channels, u8 bits, u16 sample rate, u8 format (0 PCM, 4 IMA ADPCM), u8 byte13 (200 in six P headers, read by nothing in stage 1), u16 ADPCM block alignment |

| Bank | Entries | Data headers | Formats |
|---|---|---|---|
| A (selector `0x41`, record `0x521fc8`) | 11 | 14 | IMA ADPCM mono, 16-bit, 22,050 Hz, 512-byte blocks |
| B (selector `0x42`, record `0x521fe4`) | 102 | 102 | Same |
| P (selector `0x50`, record `0x522000`) | 278 | 435 | 434 ADPCM as above, one 16-bit PCM |

### Python API

All APIs take explicit inherited buffers and a `sistema` provider for the Windows and CRT calls. Nothing is opened, allocated or defaulted implicitly.

- [`bancos_som.py`](../pesquisas-paralelas/audio/bancos_som.py):
  - `GlobaisSom` holds every inherited global: the 104-byte bank file name at `0x5221c0`, the 256-byte sound directory at `0x52201c`, the u32 variant counter at `0x5221bc` and allocation counter at `0x522230`, the window handle at `0x4e27e8`, the compressed-buffer pointer at `0x52222c` and the IDirectSound pointer at `0x522228`.
  - `BancoSom(registro28, endereco)` is the original 28-byte bank record: +0 open, +4 u16 count, +8 handle, +0xc header pointer, +0x10 in-memory flag, +0x14 data pointer, +0x18 data size.
  - The routine functions are `criar_caminho_sons`, `arquivo_som`, `criar_id_som`, `validar_cabecalho_banco`, `carregar_cabecalho_banco`, `abrir_banco`, `carregar_todos_dados`, `carregar_dados_em_memoria`, `procurar_som`, `cabecalho_dados_som`, `carregar_info_som` and `entradas_banco`.
- [`adpcm_som.py`](../pesquisas-paralelas/audio/adpcm_som.py): `decodificar_ima_mono16`, `decodificar_ima_estereo16`, `iniciar_buffer_comprimido`, `criar_buffer_vazio`, `criar_superficie_som` (`PSB_CreateMySurfaceWithSound`) and `carregar_dados_comprimidos`.
- The `sistema` provider has these parts:
  - `arquivos.abrir/ler/posicionar/fechar`, standing for `_lopen`/`_hread`/`_llseek`/`_lclose`;
  - `alocador.alocar/liberar`, standing for `GlobalAlloc`/`GlobalFree`;
  - `directsound.criar/travar/destravar` with numbered `buffers`, standing for `CreateSoundBuffer`/`Lock`/`Unlock`;
  - `getcwd`, `free` and `mensagem` (MessageBoxA).
  [`provedores_som.SistemaFixo`](../pesquisas-paralelas/audio/provedores_som.py) is the deterministic fixture used on both sides of every comparison.

### Original behavior reproduced

- **Path.** `getcwd(NULL,1000)`. A trailing backslash gives `<cwd>SOUND`, otherwise `<cwd>\SOUND`. Then `free`. `SoundFile` appends `\<letter>`; `BanqSon_LoadHeader`/`Open` append `.HED`/`.SND` into the 104-byte global and open with mode 0.
- **Header.** Reads 16 bytes and checks the magic. On a bad magic it closes the file and returns 0, writing nothing to the bank record. On success it stores the count (u16) and the data size before allocating. Then OurAlloc and a body read; a short body read closes, frees and returns 0, keeping the count and size it already stored. `Open` stores the header pointer (0 on failure), opens `.SND` and stores the handle, even `0xffffffff`. A failed `.SND` open frees the header and zeroes +0xc. Success clears +0x14 and +0x10, then sets +0 = 1. An already-open record (+0 == 1) returns 0 untouched.
- **Index.** `FindIdInBanque` scans the entries in order and matches the first equal u32 ID. `GetDataHeader` increments the u32 counter, then picks `(n-1) & counter` when n-1 > 0. A 3-variant entry never selects variant 1, and a 5-variant entry selects only 0 or 4. `HndSound_LoadDataInfo` store order: +0x18, +0, +4, (counter), +0x1c, +0xc, +0x10 (0x100 when the entry word is 256, else the stack argument), +0x14 = 0.
- **`PlaySnd_MakeID`.** `(a<<16)|(b<<8)|c` on full u32 inputs, without masking.
- **Buffer creation and decoding.** A file-backed bank seeks the data file to 0 for every sound. The buffer is created as PCM, flags `0xe0`, block alignment `(channels*bits)>>3`.
  - Format 0: seek, then lock/read/unlock; the in-memory path copies instead.
  - Format 4: the buffer is 4× the compressed size. Seek and read into the 160,000-byte compressed buffer, then lock **only the compressed size** and decode about 4× as many bytes through the same pointer, then unlock. A 512-byte block yields 1,017 samples, so 14 bytes per block at the end of the buffer stay unwritten.
  - Other formats create nothing.
- **Decoders.** The mono decoder takes min(remaining, alignment) bytes per block while at least 4 bytes remain. A step index above 88 stops with EAX 0 and keeps the output written so far. The stereo decoder interleaves L/R nibbles from paired dwords.
- **Dead code.** `BanqSon_OpenDataFile`, `CloseDataFile`, `ControleValiditeHeader`, `LoadAllData`, `LoadDataInMemory`, `PlaySnd_CreateSoundPath`, `SoundFile` and `PlaySnd_MakeID` have no CALL/JMP and no absolute reference. `LoadDataInMemory` does not seek, and it sets the in-memory flag even after a failed allocation or read, leaving a NULL data pointer.

### Supported domain and stops

- Paths:
  - a non-empty working directory;
  - a sound directory of at most 256 bytes and bank file names of at most 104 bytes, NUL included.
- Header prefixes must be complete 16-byte reads.
- ADPCM:
  - the mono block alignment must be at least 4;
  - stereo needs whole blocks with `(alignment-8) % 8 == 0`;
  - the compressed buffer must exist and the read must be complete, with no sample above 160,000 bytes;
  - a resident path needs a non-NULL data pointer.

Outside this domain the original would read stack garbage, wrap a counter or dereference NULL. Python raises `DependenciaSom` with the original address after earlier effects. In the fixture, `MessageBoxA` and every unbound import or COM slot are declared stops.

### Validation

- **Captures.** Every data header in the three banks was decoded by the intact code: 14 + 102 + 435 sounds, 43,281,606 / 137,098,639 / 823,182,052 instructions for the file path.
- **Python vs captures.** The Python replays in [`reproduzir_som.py`](../pesquisas-paralelas/audio/reproduzir_som.py) equal the captures record for record. That covers bank records, globals, call logs with exact arguments and results, and the whole DirectSound buffer SHA-256 (fixture `0xcd` in the unwritten tail).
- **Fresh native comparison.** [`validar_som.py`](../pesquisas-paralelas/audio/validar_som.py) repeats the three-way comparison (fresh native, Python, committed) and writes `validacao/x86-som.json`.
- **Catalogue.** [`catalogo-amostras.json`](../pesquisas-paralelas/audio/catalogo-amostras.json) lists 551 sounds keyed by bank, selector, ID and variant. Each entry records header fields, SND slice SHA-256, decoded length and SHA-256, and whether `GetDataHeader` can reach the variant. No labels are assigned.

```sh
python3 -B pesquisas-paralelas/audio/extrair_som.py
python3 -B pesquisas-paralelas/audio/capturar_som.py        # original-only, ~9 min
python3 -B pesquisas-paralelas/audio/validar_som.py         # fresh three-way comparison, ~10 min
python3 -B pesquisas-paralelas/audio/catalogo_som.py
```

### Remaining gaps

- **Queue and lifecycle not reconstructed.** `PlaySnd_InitSoundLib` beyond the path/open order, `PlaySnd_PostSound` dispatch into `HandlSnd_Insert`, all queue tables, `BanqSon_Close`/`Free*` and `DSB_Destroy`.
- **DirectSound is modeled only as fixture semantics.** The fixture treats the lock pointer as direct buffer memory and fills new buffers with `0xcd`. Real buffer content after creation, hardware-buffer lock copies and playback are not reconstructed. The decoder's writes past the locked length depend on that lock-pointer behavior.
- **Pending binding migration.** The bindings live in `bancada_som.py` and will migrate to core's generic binding facility when Stage 15 commits it.

## Stages

1. **Bank format and sample decoding.** Complete; see above.
2. **Request queue state.** Original-first inventory is in progress; see the [stage-2 plan](#stage-2-requestqueue-original-first-inventory). `PlaySnd_PostSound`/`PlaySnd_Manage` with the `HandlSnd_*`, `LSB_*`, `PSB_*` and `WaitSnd_*` tables must be compared natively as whole-table state. DirectSound buffer creation, playback and position queries remain explicit boundaries. Afterwards, the emitting owners can consume it in place of their pending descriptors.
3. **Game-side emitters** (`TryLanceAttaqueSound`, `VoixOffAsk`) and the volume/visibility rules, coordinated with combat and economy.

## Validation

```sh
python3 -B scripts/check.py --domain audio
RISING_EMULAR=1 python3 -B -m unittest discover -s pesquisas-paralelas/audio/testes -p 'test_*.py' -v
```

Integration runs the common checks plus this native suite in the merge candidate. Earlier extraction utilities in `legacy-prototype` are context only. They are not evidence until the original routines confirm them.

Status and results live in `pesquisas-paralelas/audio/HANDOFF.md`.

## Stage 2: request/queue original-first inventory

Resumed from integrated main `8810b3730a0fb788af3eac2b447dea65372f597f`.
This section is **static original-byte evidence and a capture plan**, not a
queue implementation or native validation result. The stage-1 captures,
catalogue and `9a0c171` three-way report remain unchanged; the 551-sound corpus
has not been rerun in this light analysis window.

[`extrair_filas_som.py`](../pesquisas-paralelas/audio/extrair_filas_som.py)
exports 53 intact SBL intervals in `0x489dac..0x48b390`, with individual hashes
and original initialized bytes, to a separate
[manifest](../pesquisas-paralelas/audio/evidencias/filas-som-manifesto.json) and
[disassembly](../pesquisas-paralelas/audio/evidencias/filas-som-rotinas.asm).
It imports no emulator and executes no original code. Existing stage-1
evidence is not regenerated by this exporter.

### Observed layout and control-flow facts requiring captures

| Original bytes | Static observation | Required comparison |
|---|---|---|
| `PlaySnd_PostSound 0x48aa79..0x48aac0` | Full-u32 bank selector EAX accepts only `0x41/0x42/0x50`; ID enters EDX, caller-owned handle pointer EBX, low byte of ECX reaches Insert, stack dword is forwarded. Invalid selector returns without entering Insert; it does not manufacture EAX=0 | Capture all selectors/boundaries, complete registers, caller handle and all tables |
| `PlaySnd_Manage 0x48aaca` | Tail-jumps to ValidateListe; ValidateListe calls ClearListe then AffectVolumeOut and falls through to LaunchWaitingSound | Run the original chain through real shared tails; no empty callback for Manage |
| Handle array `0x52137c`, stride `0x2c` | Initialization clears 70 records, selectively: byte+8, dwords+0x14/+0x20/+0x28. Playing scans cover indices 0..19; waiting scans descend from the last index to 20 | Patterned inherited whole-table capture, preserving fields not cleared |
| PSB `0x52211c`, LSB `0x52216c` | Ten 8-byte slots each, with DirectSound pointer and handle-record pointer; signed last-index counters at `0x498f60/+4` start at -1 in the executable image | Swap-with-last/last-slot branches, counter widths, moved handle back-pointers and stale-slot retention |
| Waiting counter `0x498f68` | Original initialized value 19. GetFirstFreePlace rejects only equality 70, otherwise increments and returns. Thus 69→70 is permitted by this routine | Preserve the actual edge; index 70 starts at `0x521f84` and aliases queue/dictator globals. Do not replace equality with a capacity clamp or model those bytes as independent buffers |
| `WaitSnd_Compact 0x48af1b` | May clear the external caller handle before a 44-byte move; saves/reuses the old handle word; the empty 19 case returns before the clear | Capture external references, alias cases and exact partial mutation order |
| `WaitSnd_Permute 0x48b317` | Copies three 44-byte regions, updates caller handle words, then exchanges the two +0x20 slot pointers again | Whole-table/reference comparison, including overlapping or equal inputs in an explicitly protected domain |
| `WaitSnd_Trier 0x48b38f` | Literal RET. TriWaitingHandle clears its dirty flag after calling it only when that flag equals1 | No invented sorting policy; capture dirty 0/1/other values |
| `HandlSnd_TriWaitingHandle` SBL span | Contains a RET and the shared block entered backwards by LaunchWaitingSound at `0x48a67d` | SBL symbol boundaries are not callable-body boundaries; permit the actual shared code intervals |

The static handle fields read by this stage include ID+0, bank pointer+4,
state byte+8, flags+0x0c, volume+0x10, dirty field+0x14, bank-entry pointer+0x18,
sample-header pointer+0x1c, PSB/LSB slot pointer+0x20, slot-kind+0x24 and
caller-handle pointer+0x28. These descriptions are read/store observations;
they do not establish a safe initialized domain or the complete lifecycle.
The separate dictator uses the same record shape at `0x521f94` and must not
be detached from the aliasing image. Volume uses wrapping multiplication,
arithmetic shift and lookup at `0x498f14`; it is not a guessed linear gain.

### Capture-first bounded work plan

After the coordinator grants the serialized heavy slot:

1. Capture the intact leaf queries/reservations/compactions/transfers and their
   complete inherited tables, globals and caller-owned reference words.
   Include waiting 69→70 aliasing, full signed counters, selective writes,
   same-slot and moved-last branches. Commit these original-only captures
   before adding the queue translation.
2. Capture natural PostSound sequences using checked stage-1 bank metadata,
   valid explicit pointer maps and patterned inherited state: new request,
   absent sound, repeated identity, volume-zero cancellation, entry-word256,
   replacement, full queue and invalid selector. No real sample corpus decode
   is needed merely to exercise queue admission.
3. Capture Manage's exact chain. Empty/inactive and queued states may complete
   without DirectSound; active states need declared status/duplicate/create/
   volume/play/stop/position provider results or named original stops. Provider
   failures retain earlier mutations. No callback is treated as success solely
   to make a frame advance.
4. Only then implement the bounded provider, replay every saved original
   capture, perform fresh native whole-table comparisons and relevant domain
   checks, and integrate with the current helper under the common lock.

The original DirectSound helpers reached by these paths include addresses
`0x48be90`, `0x48beb9`, `0x48bef4`, `0x48bf74`, `0x48bfb9` and indirect COM
slot+0x3c. Their exact fixture/stop contracts still require inventory and
captures; Windows playback, timing and buffer position are not inferred from
the queue bytes. The existing bank/sample APIs remain the provider for sample
data. Generic native bindings will consume core's committed facility when
available; audio will not create a competing shared binding mechanism.

Current status: static export and inspection only; **queue translation not
implemented, new original execution not run, stage2 not integrated, real
mission/complete audio flow not tested**. The macOS front remains idle until
the coordinator's M1 trigger. No synthetic training build is relabeled as a
running original mission.


## Independent M2.2 soundness and queue foundation — 2026-10-29

The independent `feat/re-audio` workstream merged origin/main before research;
its clone is `/Users/marcio/git/Rising-Lands-Codex-Audio/repository`. Maintained
changes remain inside Audio ownership. It never integrates or pushes main.

[Audio/M2.2 soundness](../pesquisas-paralelas/audio/M22_SOUNDNESS.md) gives the
original-byte inventory, native commands, all watch ranges and limitations.
The accepted declared-boundary replay equals all 257 phase summaries. A second
128-frame original replay executes PlaySnd_Manage/MCICD_Play/MCICD_Manage and
observes zero game/display readers of the watched private sound neighborhoods.
It is **not whole-state equal**: 256 phases have the private byte 0x498f5c
changed from accepted 1 to actual 0. All other captured bytes equal. The
manager also writes an already-zero u32 at 0x521f88. Accepted evidence and
masks remain unchanged. The no-playing-CD input and shared cursor 0x4e1d18
remain explicit game-state dependencies; initialized audio and M2.3 are outside.

### Waiting-slot index API (first stage-2 slice)

`indices_fila_audio.WaitingSlotIndex(index_word, playing_table)` requires an
inherited writable contiguous 4-byte index at 0x498f68 and the inherited first
20×44-byte playing records at 0x52137c. It retains both caller objects by
identity and writes in place. It creates no defaults, records or callbacks.

| Method | Original | Domain and effect |
|---|---|---|
| maximum | WaitSnd_GetMaxIndice 0x48afe9 | Raw u32 read; no mutation |
| reserve | WaitSnd_GetFirstFreePlace 0x48aef8 | Inherited index 19..70; 70 returns u32 0xffffffff unchanged, otherwise increments the word and returns it |
| give_back | WaitSnd_SorryGiveBackOnePlace 0x48afd0 | Index 19..70; 19 unchanged, otherwise decrements the word; no API result (original EAX preserved) |
| find_place | WaitSnd_FindPlace 0x48afef | Reads +8 status bytes in slots 0..19; returns the first zero slot or u32 0xffffffff; no mutation |

Malformed/readonly/noncontiguous buffers raise ValueError before any store.
Unsupported reserve/give_back index values raise DependenciaSom at original
0x48aefa/0x48afd2 before mutation. A maximum index is not a general queue count;
no full-table capacity or unexamined record meaning is inferred from it.

Original-only capture commit `679bd00` precedes the provider translation.
[133 native cases](../pesquisas-paralelas/audio/evidencias/captura-indices-fila-audio-original.json)
cover every reserve/give-back index 19..70, getter bounds and all 20 first-free
positions/full tables. The fresh native/Python/committed comparison passes
[133/133](../pesquisas-paralelas/audio/validacao/indices-fila-audio-native.json).
The native helper capture/comparison installs a five-minute SIGALRM and runs
through the shared lease. No DirectSound callback is involved.

**Next validated boundary:** PlaySnd_PostSound selects a bank and reaches
HandlSnd_Insert 0x48a218 (call 0x48aa9e). That routine reads the inherited handle
at [EBX] (0x48a225), creates/updates 44-byte records and calls the reservation
helper, for example at 0x48a351. Manage consumes GetMaxIndice at 0x48a80c.
The new provider covers those index helpers only. Record population/compaction,
transfer/sorting, logical/physical ownership and the DirectSound status/position,
volume, play/stop lifecycle remain unimplemented. Initialized ClearListe reaches
DSB_IsThisSoundPlaying 0x48beb9 (call 0x489fd9), requiring an explicit COM status
fixture. This is a declared dependency boundary, not a completed queue or a
successful sound request. Stage-3 emitters remain with their game-side owners
until that request contract is integrated; original bank/decoder work is baseline,
not new validation claimed by this round.
