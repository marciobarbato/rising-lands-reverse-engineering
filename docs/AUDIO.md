# Audio contract

Owner: the Audio front (`feat/re-audio`, `worktrees/re-audio`). Owned paths are `pesquisas-paralelas/audio/` and this manual. Audio is a second-wave domain of the [MONDE01 roadmap](ROADMAP_MONDE01.md#second-wave). On 2026-10-28 the human approved anticipating it in the macOS chat while that chat waits for its M1 trigger. No eighth executor was created. When the coordinator triggers M1, the chat returns to the `macos` front and audio pauses at its last integrated stage.

Addresses apply to executable SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`. The normalized analysis PE (`26c4534b…64d0`) is analysis-only. The original sound banks are `INSTALHD/SOUND/{A,B,P}.HED` and `.SND` on the read-only CD copy (`../source/cd`), plus `TICKONE.WAV`. Their sizes and hashes are in `relatorios/fontes.json`. PT-BR voices and music are preserved byte-exactly. They are never re-recorded, translated or normalized.

This manual starts as a coordinator skeleton. Each stage replaces its planned section with original-byte evidence.

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

## Stages

1. **Bank format and sample decoding.**
   - Inventory the original bytes of the `BanqSon_*` and `LoadSoundBuffer_*` routines and the HED header/index layout. Run original-only captures over the real A/B/P banks first.
   - Python readers must reproduce the original header validation, index and decompressed sample buffers byte for byte. Compare them natively over every sound in the three banks, with file and allocation bindings declared.
   - Inventory the sound identity (`PlaySnd_MakeID`, `PlaySnd_CreateSoundPath`, `SoundFile`) that maps a request ID to a bank entry. Publish a PT-BR sample catalogue with hashes, recording sound IDs, not invented labels.
2. **Request queue state.** `PlaySnd_PostSound`/`PlaySnd_Manage` with the `HandlSnd_*`, `LSB_*`, `PSB_*` and `WaitSnd_*` tables, compared natively as whole-table state. DirectSound buffer creation, playback and position queries are declared stops. Afterwards, the emitting owners can consume it in place of their pending descriptors.
3. **Game-side emitters** (`TryLanceAttaqueSound`, `VoixOffAsk`) and the volume/visibility rules, coordinated with combat and economy.

## Validation

```sh
python3 -B scripts/check.py --domain audio
RISING_EMULAR=1 python3 -B -m unittest discover -s pesquisas-paralelas/audio/testes -p 'test_*.py' -v
```

Integration runs the common checks plus this native suite in the merge candidate. Earlier extraction utilities in `legacy-prototype` are context only. They are not evidence until the original routines confirm them.

Status and results live in `pesquisas-paralelas/audio/HANDOFF.md`.
