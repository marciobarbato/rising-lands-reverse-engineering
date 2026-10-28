# Selective structure-record lifecycle

This slice implements pool initialization and reset, plus the first-free query used by `CreerBatiment`. It does not reserve, create, place, charge for, or demolish a structure. The Python entries are in [ciclo_estruturas.py](../../ferramentas/ciclo_estruturas.py); `MundoUnidades` and its descendants expose the same operations as methods. Construction of a synthetic world still starts with zero-filled buffers; invoking the original startup prefix is explicit.

## Original evidence and calling convention

Original `RISING.EXE` SHA-256: `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`. The [manifest](../../evidencias/ciclo-estruturas/manifesto.json) records independent interval hashes; adjacent disassemblies include every original byte.

| Original interval, end exclusive | Boundary | Python entry |
|---|---|---|
| `0x418e95..0x419004` | `BatimentAlloc` startup prefix, stop before economic initialization | `inicializar_registros_estruturas(registros, realizaveis)` |
| `0x41a75c..0x41a860` | complete `BatimentResetAll` body and return | `resetar_todas_estruturas(registros, realizaveis, selecoes)` |
| `0x41b9d6..0x41ba49` | complete `ResetBatiment`; index in low 16 bits of EAX | `resetar_estrutura(registros, indice)` |
| `0x41fea2..0x41ff04` | `CreerBatiment` prologue and first-free scan; success stop before any cost reads | `buscar_estrutura_livre(registros)` |
| `0x4202c1..0x4202ce` | original failure epilogue used when the scan finds no slot | same query, returns `0xffff` |

The original structure pool begins at `0x49a0c8`, has 1,000 records, and has stride 276 (`0x114`). Raw flag bytes occupy `0x49a070..0x49a0c8` (4 × 22). The four selection words begin at `0x495be0`. Their game-level producers and meanings are not expanded here. All numeric stores are little endian and preserve their original widths.

The two pool routines take no arguments in the original machine code and mutate globals. `ResetBatiment` consumes AX without checking bounds; this Python model supports only indices 0–999 after truncation to u16. The original `CreerBatiment` prologue saves EAX, DL, and BL for later creation, but the isolated scan uses none of them. Its successful checkpoint contains the index in AX; its failure epilogue returns `0xffff` in EAX. The remaining original creator body is unsupported.

## Buffers, mutation order, and failures

`registros`, `realizaveis`, and `selecoes` must be writable `bytearray` objects of exactly 276,000, 88, and 8 bytes respectively, including for the read-only query. Wrong buffer types/sizes and an integer reset index whose low 16 bits are ≥1,000 raise `ValueError` before any mutation. Arbitrary original out-of-pool memory access is not supported. The three mutating operations return `None`; the query returns an integer. No callback is invoked by these supported intervals, and no deferred callback is silently skipped inside them.

Startup first zeroes the 88 flag bytes, then visits records 0–999. Within each record the ordered stores are below; offsets and sentinel values are hexadecimal, while the value 200 is decimal:

```text
u8 +05=0; u16 +0a=0; u16 +78=ffff; u16 +86=ffff; u16 +88=ffff;
u16 +06=0; u8 +90=1; u8 +00=ff; u8 +74=0; u8 +75=0; u8 +76=0;
u8 +7b=ff; u16 +82=0; u16 +7c=0; u8 +7a=0; u16 +80=0;
u16 +7e=0; u16 +c4=0; u16 +c6=0; u16 +c2=0; u16 +84=200;
u16 +c8=ffff; u16 +02=ffff; u8 +104=0; u8 +8a=1; u8 +8b=1;
u32 +100=ffffffff; u8 +04=ff; u8 +08=ff; u32 +8c=0; u32 +108=0;
u8 +110=0; u8 +111=0; u8 +112=0; u8 +113=0.
```

The original stops at `0x419004` with the startup stack frame still present. The benchmark deliberately stops there; it does not pretend this is a completed `BatimentAlloc` call. The remaining routine resets 88 economic Bags through `BagReset`, initializes player tables, and calls `BatimentLoadCaract`. These effects remain dependencies rather than callbacks offered by this prefix API.

Global reset writes the four selection words to `0xffff`, zeroes the 88 flag bytes, then visits records 0–999 with these stores:

```text
u8 +05=0; u16 +06=0; u16 +0a=0; u8 +00=ff; u8 +74=0; u8 +75=0;
u8 +76=0; u8 +7b=ff; u16 +7c=0; u8 +90=0; u16 +7e=0;
u16 +80=0; u16 +82=0; u16 +84=200; u32 +8c=0; u16 +78=ffff;
u16 +86=ffff; u8 +8a=1; u8 +8b=1; u8 +04=ff.
```

Thus global reset preserves origin `+02`, type `+08`, `+88`, and all `+100..+113`. Startup overwrites origin, type, `+88`, and selected fields within that final range; `+105..+107` and `+10c..+10f` survive both operations. Neither routine clears the entire record or its embedded Bag at `+0c..+73`.

Single-record reset performs, in order: u16 `+78=ffff`, u8 `+7b=ff`, u16 `+7c=0`, u16 `+7e=0`; reads type `+08`; writes u16 `+86=ffff`; clears u16 `+80` and `+82` unless type is exactly 20; clears u8 `+74`; reads state `+05`; clears u32 `+8c`; and writes state 5 unless the prior state was 3. All other bytes survive, including gate counter `+76`, gate command `+75`, type, origin, owner, and flags at `+7a` and `+90`.

The first-free query scans indices 0–999 and checks only u8 state `+05 == 0`. Owner, type, origin, and contents of the rest of the record do not affect selection. It returns the first matching index or `0xffff`. It never reserves the index: consecutive queries return the same slot until a caller changes state. It neither proves a location is buildable nor validates available resources.

All supported calls leave terrain, objects, regions, auxiliary colors, units, tasks, and economic inventories untouched. Resetting records in an occupied world therefore does not establish a valid rebuilt world; teardown/remapping must be supplied separately.

## Cross-domain contracts

Graphics may continue reading raw u8 `+76` and full u16 `+7c` for gates. Startup and global reset clear the counter; single-record reset preserves it while clearing orientation. None of these effects chooses a sprite. A reset record alone must not be interpreted as a complete world-lifecycle transition.

Economy does not need to import this code for its independently bounded `SortieTroupe` completion: that path reuses an existing colonist and hands off to `CalculPosition`/`EnginSetType`. Subsequent [position-query](EXIT_POSITION.md) and [shared conversion](CONVERSION.md) stages recover that connection; later production world effects remain unsupported. No fresh-allocation callback is claimed for that path. `CreerBatiment` cost validation, charging, the subsequent state write/reservation, placement, and Bag initialization still require their own contract.

Combat's occupied-unit impact adapter remains independent. Lethal unit transitions and world impact resolution still require explicit future callbacks; this structure-record slice supplies neither.

## Actual validation

```sh
python3 -B ferramentas/extrair_ciclo_estruturas.py
python3 -B ferramentas/validar_ciclo_estruturas.py
python3 -B ferramentas/validar_ciclo_estruturas.py --emular
python3 -B ferramentas/demonstrar_ciclo_estruturas.py
python3 -B scripts/check.py --domain core
```

The [new x86 report](../../relatorios/ciclo-estruturas-emulado.json) records 12 tests, 648 bounded original-x86 executions, no failures/errors/skips, zero expected x86 exceptions and zero execution limits. Seven executions reach the deliberate startup dependency boundary `0x419004`; six successful scans reach `0x41ff04`; 635 complete calls reach the normal benchmark return. All comparisons use complete 276,000-byte pools plus both raw global tables, with zero, `ff`, `a5`, and deterministic random fixtures. Single reset covers all 22 known types plus raw types 22/127/254/255, eight state values, and indices 0/499/999 with poisoned upper EAX bits. The scan includes pool exhaustion and multiple free slots. A combined sequence checks initialization followed by single/global reset.

The [local-only report](../../relatorios/ciclo-estruturas-local.json) records 12 discovered tests, seven executed Python tests, five explicit x86 skips, and zero x86 executions. The domain check passed 238 discovered tests with 118 optional-x86 skips. Its historical 49,305-x86 aggregate was not rerun. The first attempted new x86 process exited 132/SIGILL in the sandbox before an x86 result; the authorized JIT-capable rerun produced the successful report above.

The [Python demonstration](../../relatorios/ciclo-estruturas-python.json) uses an explicitly caller-prepared gate after pool initialization. It shows free-query non-reservation, placement through the existing physical API, and terrain retention across the two reset operations. It is synthetic and executes no x86. Original mission loading/remapping, full building allocation/creation/destruction, all remaining `BatimentAlloc` effects, global dispatcher cadence, economics, unit production conversion, and rendering remain unsupported by this slice.
