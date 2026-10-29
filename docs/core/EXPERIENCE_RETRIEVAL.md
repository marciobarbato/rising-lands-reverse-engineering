# Mission-load experience retrieval (`Engin_RetrieveExperimente`)

Core P2 / M1 blocker #1, 2026-10-28. Intact executable SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb` is the only execution oracle. The normalized analysis PE (`26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0`) was not used; no REA/Ghidra session was opened. All ranges are end exclusive.

## Original bytes and ABI

`Engin_RetrieveExperimente` is the `MissionLoad+0x2ea` tail call at `0x46c5b9`, between `BatimentInitCave 0x419112` and `PlayerRetrieve 0x46df41`. It is the only direct caller. The routine bytes are `0x441623..0x441659` (54 bytes), SHA-256 `9e9298121bdb5c12a6d8912f5430b3cdcbcb5cb7831c466a672b320f8c7d4522`. This matches the coordinator's static lead. The routine exits through the shared epilogue `0x440d59..0x440d5e`, which pops ESI, EDX, ECX and EBX and then returns with RET. The [byte manifest](../../evidencias/recuperacao-experiencia/manifesto.json) records the hash of each interval and has `.asm` files next to it.

- **Inputs:** no register is consumed. EAX is overwritten by `IMUL EAX,ECX,10` before it is read. EBX, ECX and ESI are initialized locally. Only DX is loaded, and EDX is restored afterwards. There are no stack arguments. The only memory input is the 40-byte saved queue at `0x4e19ec..0x4e1a14`.
- **Effect:** for owner 0..3 and word 0..4, ascending, the u16 at `0x4e19ec+10*owner+2*word` is stored to `0x4e19c4+10*owner+2*word`. The loop compares the biased index with an owner limit of 10, 20, 30 and 40. It has no guard, no data-dependent branch and no call. The destination ends exactly where the source begins, so the two never overlap. The only other writes are the four pushed dwords (EBX, ECX, EDX, ESI) at ESP-4..ESP-16.
- **Exit:** EAX is `0x28`. EBX, ECX, EDX, ESI, EDI and EBP equal their entry values. ESP is the entry ESP + 4 (near RET with no immediate). The final `CMP ECX,4` sets ZF=PF=1 and CF=AF=SF=OF=0. DF and the non-arithmetic bits are kept. Every run takes 152 instructions. MissionLoad ignores both EAX and the flags: `PlayerRetrieve` starts with `XOR EAX,EAX`.

## Public API (`ferramentas/recuperacao_experiencia.py`)

- `recuperar_experiencias(atuais, guardadas) -> RetornoRecuperacaoExperiencia` copies the queue in place. `atuais` must be the live writable 40-byte `bytearray` for `0x4e19c4`, and it keeps its identity. `guardadas` must be the distinct live 40-byte `bytes`/`bytearray` for `0x4e19ec`; it is only read.
- `recuperar_experiencia_missao(mundo, guardadas)` is the same call over `mundo.experiencias_unidades`, the queue that `EnginSetExperimente` consumes (see [experience queue](EXPERIENCE_QUEUE.md)). **Missions should call this one** at the `0x46c5b9` tail slot.
- `RetornoRecuperacaoExperiencia.eax` is `0x28`. `RetornoRecuperacaoExperiencia.eflags(entry_eflags)` returns the exit EFLAGS.
- **Domain and protection:** every check happens before the first store.
  - If `guardadas is None`, `DependenciaExperienciaGuardada` (a `NotImplementedError`) is raised with `endereco=0x441645`, the first saved-queue read.
  - A wrong length or type, a memoryview, or the same object passed as both queues raises `ValueError`.
  - Any 40-byte content is supported, because the original has no data guard.
- No buffer is created, reset or defaulted. The world constructor's zero queue is synthetic and is not a mission-load value.

## Saved-buffer provenance (static; not implemented by Core)

The saved queue sits in `.bss` (`0x49a000..0x522400`), so it is not file-backed at process start. A scan of every BEGTEXT instruction that addresses `0x4e19c2..0x4e1a14` finds 23 references. Apart from the two in `Engin_RetrieveExperimente` itself, all of them are in these routines:

| Routine | Calls | Effect on saved `0x4e19ec` |
|---|---|---|
| `Engin_ResetExperience 0x441470..0x4414ad` (exit `0x440d5a`) | `MenuInit+0xb77` `0x468e32`; `MissionLoadName+0xae` `0x46c691` | Every one of the 20 pairs gets type `0xFF`, experience `0`; the current queue is untouched. Native exit EAX=4. |
| `Engin_StoreExperimente 0x4414f8..0x441623` (exit `0x440d55`) | `CalculGame+0x21a` `0x42ca82`, only when `MissionNext 0x46c08c` returns AL=1, after `IaRechercheAjuste` and before `RechercheStore`/`PlayerStore` | First resets all pairs to (`0xFF`,0). Then, for each of the 800 units whose state byte +2 is not 0 or 4, it finds the slot with the strictly lowest experience among the owner's (+0) five slots, taking the first one on ties. If unit AF (+0xaf) is larger, it stores (type +1, AF) there. It has no owner guard: an owner ≥4 would write beyond `0x4e1a14`. |
| `Engin_LoadExperimente 0x4414ad..0x4414d7` | `GameLoad+0x263` `0x46baf0` when the save version is ≥2 | `FileRead 0x458461` reads 40 bytes into current, then 40 bytes into saved only when the version is ≥4 |
| `Engin_SaveExperimente 0x4414d7..0x4414f8` | `GameSave+0x32b` `0x46c070` | `FileWrite 0x458476` writes current, then saved (read-only) |
| `EnginSetExperimente 0x44fe42` | production exit | Addresses current owner records. Its unguarded owner 4 would alias exactly the saved bytes; Core's protected domain is owners 0..3. |

In a fresh campaign, MenuInit's reset leaves the saved queue as `ff00` × 20, so the first `MissionLoad` copies that pattern into current. This was observed with the original producer, not assumed. After a won mission, the saved queue holds the stored top five per owner. After a loaded save with version ≥4, it holds the file bytes. Missions must supply the actual live buffer for the session it composes. No MONDE01 memory snapshot of either queue exists in committed evidence.

## Original-first evidence and validation

1. **Static export and original-only capture before translation.** The static export, bench and capture script were committed as `ff92691` before any Python translation existed.
   - The [capture](../../evidencias/recuperacao-experiencia/captura-original.json) has SHA-256 `5c734542db10337117b8167f15fe7bd49c47a4e4c5553fd6ea750949c2c220d3`. It covers 20 cases in 22 bounded segments: 20 retrieve entries, one native `ResetExperience` chain and one native `StoreExperimente` chain over a synthetic pool. The largest segment took 58,813 instructions (Store).
   - The cases cover distinct per-word values, single-owner differences for each of the four owners, all-`FF`/all-zero and boundary words, a reset-shaped saved queue, identical queues, register/flag probes and random queues.
   - Each case records sentinel registers and flags, the ordered write log, the complete 2 MiB image difference, stack words and a neighbourhood `0x4e19a4..0x4e1a40` of distinct bytes.
   - In every case the image changes only inside `0x4e19c4..0x4e19ec`, and the writes are exactly 20 ascending u16 stores plus four pushes.
2. **CPU-free replay.** `testes/test_recuperacao_experiencia.py` replays all 20 frozen cases through Python. It checks the queues, EAX, EFLAGS, preserved registers, ESP, the exact image difference and the write order. It also covers input protection and live-buffer identity.
3. **Fresh native differential.** `testes/test_emulacao_recuperacao_experiencia.py` (`RISING_EMULAR=1`) passes 10 tests in 5.55 s, with 74 Python/native comparisons in 78 bounded segments. Those segments are 74 retrieve entries plus 2 Reset and 2 Store producer runs. The comparisons are:
   - all 20 captured inputs, with the regenerated saved bytes equal to the capture;
   - 32 random queue/register/flag cases;
   - 20 single-word differences, one at each word position;
   - two fresh producer chains.

   The run had zero failures, errors, skips, faults or limits, and used no binding or patch. Report: [native](../../relatorios/recuperacao-experiencia-emulada.json); [local](../../relatorios/recuperacao-experiencia-local.json) runs 10 tests, 6 executed and 4 optional skips.

Reproduce:

```sh
python3 -B ferramentas/extrair_recuperacao_experiencia.py
python3 -B ferramentas/capturar_recuperacao_experiencia.py   # rewrites the capture; must stay byte-identical
python3 -B ferramentas/validar_recuperacao_experiencia.py --emular
python3 -B scripts/check.py --domain core
```

Run native commands under the exclusive heavy lease.

**NOT RUN:** a complete `MissionLoad` with the six-tail composition; a real MONDE01 snapshot of either queue; translation of the Reset, Store, Load or Save producers. Those are provenance only and belong to Missions/Core follow-up scheduling.
