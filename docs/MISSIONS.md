# Mission loading and execution contract

Mission orchestration belongs to `pesquisas-paralelas/missoes/`. The first stage implements an indexed unit-load continuation, independently compared against intact original instructions. It does **not** return an initialized mission or establish mission execution. The inspected main base is `1f9019d8027f59e0fa304df29961b9c13ea5f4be`.

## Original assets and caller inventory

The [hash-only inventory](../pesquisas-paralelas/missoes/evidencias/inventario.json) covers **38 ETA maps, 25 PT-BR TXT briefings, and five NET files** under the original CD's `WORLD` directories. It records sizes, SHA-256, every existing reader's ETA block boundary and the untouched suffix. No commercial file is copied. The 38 maps contain 2,604 disk unit records. Text remains CP1252 source material; mission names, stories and objectives have not been invented or translated.

Original executable SHA-256 is `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`. The analysis-only PE is `26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0`. The [original instruction manifest](../pesquisas-paralelas/missoes/evidencias/manifesto.json) exports seven exact intervals. SBL names below identify original routines, not inferred completed capabilities.

| Original entry | Ordered calls and boundary |
|---|---|
| `MissionLoad 0x46c2cf` | Build mission filename; reset handles/global state, terrain, minimap, structures, units, projectiles, messages and balloon state; open original file; skip four version bytes; read attribute/terrain/object/aux layers; normalize object 54→66/aux1; resources 1,2,0; dimensions and selected-player view; `Chemin_Remap`; indexed structures; `LoadEngin`; eight auxiliary readers; close; postload calls below |
| `MissionLoadName 0x46c5e3..0x46c9a5` | Second direct caller of the same `LoadEngin`; extra technology/network setup and filename selection; separate postload differences. Its code ends before the following SBL symbol at `0x46c9a8` |
| `LoadEngin 0x46acbf` | `SelectionInit`, four loader bytes=50, indexed header/records, ordinal selection-byte clear, per-index existence/type/postload; shared return at `0x46b112` |
| Inline structure loader `0x46c517..0x46c578` | u16 count/size and indexed bytes into static `0x49a0c8`, stride276; this is not `LoadBatiment 0x46b1fb` and does not prepare complete structures |
| `MissionPlaceTerrain 0x46c122` | Scan 800 units: existence then `EnginVisible` then `PlaceEngin 0x456fa6`; capacity refresh for players0..3; scan1,000 structures: existence, `PlaceBatiment`, conditional `BatimentHabitable`, `BatimentModifyMap(...,1)` |
| `MissionLoad` tail | After placement: `EnginInitTechnologie 0x441459`, `BatimentInitCave 0x419112`, `Engin_RetrieveExperimente 0x441623`, `PlayerRetrieve 0x46df41`, `IaReset 0x47f36e`, `0x46027c`; none is silently skipped |

The auxiliary readers are `0x47534a`, `0x47c24d`, `0x47bcc7`, `0x47c04a`, `0x458b05`, `0x47c30f`, `0x47c404`, `0x47ac30`, in that order. The existing [format manual](FORMATS.md) describes their disk blocks; decoding blocks does not prove their runtime meanings, reference remaps or AI operation semantics. Shared VM primitives remain core-owned.

## Stage 1: indexed unit-load continuation

Public API: `continuar_carga_unidades(leitor, unidades, valores_jogador, tipos_unidades, *, modificador12=None)` in [carregador_unidades.py](../pesquisas-paralelas/missoes/carregador_unidades.py). It begins at **`0x46acca`, after `SelectionInit`**, and ends at the original `LoadEngin` return. The caller must already have performed selection initialization; the API does not provide that prerequisite.

| Input | Exact contract |
|---|---|
| `leitor` | Committed `formatos.Leitor` positioned at the indexed unit block's u16 count,size header, with complete successful-I/O input bytes |
| `unidades` | Writable contiguous u8 buffer, exactly220,800 bytes:800×276 inherited live records; a memoryview retains object identity |
| `valores_jogador` | Writable contiguous four bytes corresponding to original `0x4e19bc`; no interpretation beyond the observed stores is assigned |
| `tipos_unidades` | Readable contiguous1,300 bytes:26×50 already-loaded type records; offsets42/44/48 supply vision/range²/reload |
| `modificador12` | Optional read-only `(owner_u8,type_u8)->integer` query. Required only for active type4 with owner other than4/200. Can adapt committed `BonusUnidades.consultar(owner,type,12)` using an explicitly supplied loaded1,872-byte table |

Buffers must be separate, stable allocations throughout the call. The function does not allocate/zero a world or load default bonuses. Provider callbacks may not mutate loader inputs or replace buffers. Types are values already processed by the core reader; range is not squared a second time. The fixture input helper consumes committed `regras.extrair_regras` and the original INI; it is not a new INI loader.

Effects occur in this order:

1. Store50 into all four loader bytes. Read u16 count then size. Protect the supported domain:count0..800,size784.
2. For each ordinal in file order, read u16 disk index0..799. Copy140 disk bytes into **that indexed record** at+0. Consume512 skipped disk bytes without writing RAM, then copy132 bytes into+140..271. The four bytes+272..275 are untouched by copying.
3. Clear byte+`0xbd` of the **ordinal record**, even when the disk index differs. Preserve repetitions and sparse IDs; this is not a compacting remap. An indexed record may later overwrite a previous ordinal clear.
4. For indexed state byte+2 equal0, skip postload. Every other byte, including4 and14, reaches the committed combat `preparar_apos_carga_missao` provider. That provider owns type characteristics, modifier12 order, life100, vision/range/reload, group255, handles and other stores, owner0 for type16 and owner4 for types20..24. Active postload explicitly zeros+272..275; inactive units retain those inherited bytes. Disk health, owner and type fields therefore remain distinct from postload outputs.
5. Return `CargaUnidades(quantidade, indices, fim, rotina_seguinte=0x47534a)`. `indices` preserves the exact encountered file indices, not a newly allocated ID mapping. The next routine is metadata for the original caller; it is not executed.

Structural buffer/callback errors fail before effects. Unsupported header/count or index fails after the preceding header/ID reads and four stores. Strict-reader truncation preserves preceding copies; Win32 short-read/failure behavior is outside this successful-I/O slice. Active type≥26 raises a named dependency at the original type-helper entry. Missing modifier12 raises `DependenciaCargaUnidades(endereco=0x428cc0)` at its query, retaining raw copies, ordinal clear and earlier provider stores. An arbitrary provider exception propagates with the same earlier effects. Retrying entry after failure repeats effects; no general continuation token is claimed.

## Independent evidence and checks

The [original-only captures](../pesquisas-paralelas/missoes/evidencias/captura-original.json) were generated **before** the Python continuation was implemented. They cover actual MONDE01 bytes and a synthetic sparse/repeated-index block, with inherited pool `0xa5` and explicit patterned loaded bonuses. Two original loader calls returned through88 bounded execution segments. Capture regressions compare independently retained whole-pool hashes and changed records.

Fresh [differential report](../pesquisas-paralelas/missoes/validacao/carga-unidades-x86.json): **469 loader fixtures /14,056 bounded segments**, comprising457 native returns and12 expected modifier-entry checkpoints. Whole220,800-byte pools, four loader bytes, cursors and successful read/seek sizes match. The fixtures include every unit block in all38 original ETA maps, all26 supported types, states0/4/7/14, owners0/3/4/200, IDs0/7/799, repeated/sparse indices and empty blocks. Native selection/type/bonus helpers execute unpatched. Only successful file I/O is supplied in memory; no Windows process is run.

All12 mission tests pass with native mode:zero skips/failures/errors/native faults. Local mode runs eight tests and explicitly skips four optional x86 tests. The two capture calls are separate from the469 differential fixtures; segment totals are not counts of full missions. First sandbox capture exited132/SIGILL; the authorized ordinary-context JIT run succeeded. REA's first Java spawn was sandbox-blocked; its private read-only ordinary-context session succeeded, exported and closed. [Reviewed REA observations](../pesquisas-paralelas/missoes/evidencias/rea-review.json) use pinned revision `b9a8f8e9f25feb9cc97bf4960748f2bdf8c898bc` and the normalized PE, separately from the intact-original oracle.

```sh
python3 -B pesquisas-paralelas/missoes/extrair_evidencias.py
python3 -B pesquisas-paralelas/missoes/capturar_original.py
python3 -B pesquisas-paralelas/missoes/validar.py
python3 -B pesquisas-paralelas/missoes/validar.py --emular
python3 -B scripts/check.py
```

The common runner currently has no missions domain. It must be run alongside the owned mission entrypoint. At the inspected base, actual common suites pass:core290(138 optional skips),combat172(107),economy303(136),graphics115(0),workflow3(0). Those local checks are not native verification of other domains.

## Remaining mission coverage

This stage closes the indexed-unit stream/postload connection, including an ordinal/index distinction missing from raw record reconstruction. MONDE01 has16 indexed units and one structure; neither this result nor a terrain screenshot establishes a correctly running mission.

Missing prerequisites are explicit:shared `SelectionInit`, original terrain/unit global reset state, `Chemin_Remap`, runtime auxiliary tables/reference relations, structure postload/physical insertion, unit `PlaceEngin` and complete discovery/occupancy setup, loaded bonuses/player economy state, technology/experience/cave/player retrieval tails, mission selection/briefing semantics, mission-specific rule/objective/event wiring and a supported dispatcher. Core capacity refresh/structure placement providers exist but are not invoked by Stage1. Mission2+ runtime, unsupported AI operations, victory/loss, global timing, save/load and audio remain unsupported. Rendering, economic effects, combat effects and app/native build retain their owners.

Stage 1 was integrated at main `c64d32b859046468e2f9085f90f96eb5002d567c`, from final feature `551e1fb19e8bf529d0074a960d6507a87e2ee248` containing implementation and import correction `9f0d32481560e49a21258a269cd22b44a1827263`. The clean worktree fetched main `8fd9c41ce6e3b8709cc0d7235e8c31d9b6a68b8d`, verified ancestry and reproduced all 12 Stage 1 tests / 469 native fixtures / 14,056 segments before Stage 2 implementation.

Final consumer review renamed the owned bootstrap to `ambiente_missoes.py`, avoiding collision with core `caminhos.py`. A committed-provider navigation import regression now passes; this correction changes no loader bytes or native fixture counts.

## Stage 2: successful-open terrain, resource and view prelude

`continuar_cabecalho` in [carregador_cabecalho.py](../pesquisas-paralelas/missoes/carregador_cabecalho.py) reconstructs `MissionLoad 0x46c396..0x46c512`, **after successful open and before `Chemin_Remap 0x42ee1c` executes**. It consumes the committed `Leitor`, graphics `normalizar_inicio` and economy `Economia.atribuir`; it does not copy those providers' implementations. [Appended original evidence](../pesquisas-paralelas/missoes/evidencias/cabecalho-manifesto.json) preserves the original executable hash, two intervals, consumed provider hashes and original INI/SBL/RUL dependency identities, without regenerating Stage 1 evidence.

Call `continuar_cabecalho(leitor, atributos, terreno, objetos, auxiliares, economia, dimensoes, visualizacao, jogador_visualizacao)` with these explicit inherited inputs:

| Input | Width/layout |
|---|---|
| `leitor` | Existing `Leitor` at file position 0, after the caller's successful open |
| Four raw layers | Separate writable contiguous u8 buffers of 65,536 / 131,072 / 65,536 / 65,536 bytes; the second is raw little-endian u16 terrain, with cell stride 256 |
| `economia` | Already-supplied `Economia` object with its inherited 128-byte table; no default construction or balance/bonus initialization |
| `dimensoes` | Writable four bytes: u16 width, u16 height |
| `visualizacao` | Writable four bytes: u16 X, u16 Y; inherited bytes remain relevant when the selected-player byte is outside 0..3 |
| `jogador_visualizacao` | Integer truncated to u8, corresponding to original `0x508041` |

All buffers/provider memory must be separate and remain stable. Shape/provider/reader-position checks fail before reads or effects. The prelude skips four bytes without validating `V0.3`, matching original absolute seek 4. The inventory/full ETA reader independently enforces its studied version. It then copies the four entire layers in original order, normalizes every object cell 54→66/auxiliary 1 through the committed graphics provider, reads resources in order 1,2,0 for players 0..3, and invokes the actual setter immediately after each u16 read. The setter updates RMI/total, clears display/flags, preserves byte +7 and the fourth resource slot, and applies no 9,999 cap. A resource provider failure propagates with earlier copies/normalization/setter effects retained.

Width and height are read into their two halves in order. The prelude consumes all four players' X/Y pairs, writing only the pair matching the selected-player u8. Values 4..255 preserve the inherited view, while still consuming all 16 bytes. It returns `CabecalhoCarregado(largura, altura, jogador_visualizacao, fim=0x50030, rotina_seguinte=0x42ee1c)`. These are raw u16 dimensions; even out-of-range raw values can reach this safe checkpoint. This API does not validate a playable rectangle, project a camera, infer walkability/discovery or enter remapping.

Strict Python reads require complete supplied data. Truncation preserves preceding complete buffer/setter stores; this does not model partial Win32 reads. The successful path does not include filename selection, global/terrain/minimap/pool/projectile/message resets, open failure, region/color/search initialization or allocation. Those prerequisites must not be inferred from a constructor. In particular, the original remap clears search/color/region buffers before allocation and can fail with those effects retained; `MundoNavegacao.refazer_regioes` is not declared equivalent to that full routine.

Four [original-only prelude captures](../pesquisas-paralelas/missoes/evidencias/captura-cabecalho-original.json), generated before translation, cover MONDE01 with selected-player values 0/3/4/255. All reach `0x42ee1c` in 160 bounded segments. The inherited resource pattern and initial view are explicitly synthetic. Native object normalization and `SetMatiere` execute unpatched; only successful file I/O is supplied. Regressions compare all seven output-buffer hashes independently of the reconstruction. The Stage 1 capture/report files remain historical records.

Stage 2's [combined report](../pesquisas-paralelas/missoes/validacao/stage2-suite-x86.json) keeps unit and prelude counts separate. The fresh native test covers the 38 original headers for cameras 0/1/2/3/4/255, plus synthetic all-grid normalization, version skipping, dimension/resource width boundaries and u8 camera truncation. The initial boundary-fixture run failed in the harness because Unicorn `mem_write` received a Python bytearray; converting that adapter input to bytes fixed the host error without a reconstruction change. The failed attempt is not counted as successful coverage.

```sh
python3 -B pesquisas-paralelas/missoes/extrair_cabecalho.py
python3 -B pesquisas-paralelas/missoes/capturar_cabecalho.py
python3 -B pesquisas-paralelas/missoes/validar.py --emular
```

No unit records, structures or auxiliary mission tables are loaded by this prelude. Stage 1 is a later independent continuation separated by `Chemin_Remap` and structure loading. Their passing tests do not join those missing operations. Selection initialization, complete world insertion, mission-specific objective/event execution and runtime comparison remain open. After Stage 2 integrates and is reproduced, the next independently supported slice is the mission auxiliary-table load path, beginning with exact original `LoadFinMission`/`LoadObjectif` input and retention rules; no end-condition semantics will be inferred from names or disk values alone.

Final Stage 2 checks:18 mission tests pass in native mode, zero skips/failures/errors/native faults. New prelude coverage is237 calls/9,480 bounded segments, all stopped before remap. Unit revalidation separately repeats469 fixtures/14,056 segments (457 returns,12 expected query checkpoints); these are not new aggregate mission coverage. Local mode executes12 tests and skips six optional native tests. Common suites at inspected main pass core302/143 optional skips,combat191/119,economy326/146,graphics122/0,workflow3/0.

Stage 2 integrated at main `b8f424dde0bc12d829b8653bdd9deb4906093397`, final feature `0c7d825fe008b2c8ecc24a9e54bd0af8efb546d0`, reviewed implementation `5361b496e61265275cc129de8efc018d267d266f`. The clean worker fetched main `6a9168e42f917096af88fc6c510b3f25b7230516`, verified ancestry and reproduced all 18 native tests / exact per-slice counts before Stage 3 implementation.

## Stage 3: end-condition and objective table initialization

[carregador_condicoes.py](../pesquisas-paralelas/missoes/carregador_condicoes.py) adds two exact original table loaders. These are initialization APIs; **`TestFinDeMission`, objective consumption, victory/loss and events remain unsupported**. The [original-byte manifest](../pesquisas-paralelas/missoes/evidencias/condicoes-manifesto.json) includes both loader bodies and the still-unimplemented consumer/query bodies. [Reviewed private REA evidence](../pesquisas-paralelas/missoes/evidencias/rea-condicoes-review.json) inventories the consumer's caller and 11 resolved native queries without adopting its fallible Watcom pseudocode as semantics.

`carregar_condicoes_fim(leitor, memoria)` consumes a committed `Leitor` positioned at the format manual's `tabela_458b05` block, and a separate writable contiguous **114-byte** inherited buffer corresponding to `0x4e1d20..0x4e1d92`:

| Relative bytes | Original loading effects |
|---|---|
| 0..99 | Ten 10-byte records. Before reading the header, set **only the first byte of every record to255**, retaining the other nine bytes |
| 100..103 | Four adjacent result/global bytes; retain all of them |
| 104..113 | Ten status bytes. Clear a status only **after** its corresponding record read completes; statuses beyond the supplied count retain inherited values |

The protected header domain is u16 count0..10 and size10. Read count then size, then copy each entire record in order and clear its one status byte. Count0 still marks the ten record codes, but preserves all statuses and other record bytes. Unsupported count/size raises after code marking and header reads. A strict read failure retains previous copies/status stores and the initial marking. Return `TabelaMissaoCarregada(count, fim, rotina_seguinte=0x47c30f)`; the next original call is not executed. Raw record codes are opaque inputs to this loader, including codes outside the observed corpus.

`carregar_objetivos(leitor, memoria)` takes a committed `Leitor` at `listas_por_jogador` and **804 inherited writable bytes** at `0x511ffc`: four players ×100 u16 ID words (800 bytes), followed by four retained player cursor bytes at `0x51231c`. It first fills the800 ID bytes with `0xff`. In player/ordinal order it reads and stores each u16 ID, then consumes one disk flag byte into discarded scratch. The flag is not copied into runtime objective memory. A failure before the flag read retains the preceding stored word. Cursor bytes are never reset by this routine. Return `TabelaMissaoCarregada(400, fim, rotina_seguinte=0x47ac30)`; no monster-entry load, cursor query or text load is executed.

Both APIs validate input shape/writability before reads or effects. These strict in-memory adapters do not model Win32 partial reads or malformed native buffer overruns. They neither initialize unrelated world state nor infer objective rules from raw IDs. The original `LoadObjectif`/`LoadFinMission` callers occur after intervening auxiliary loaders; APIs may only be joined when those operations are explicitly supplied.

Across all38 original maps, serialized objective words are `0xffff`; this is a disk observation, **not evidence that missions lack objectives**. Separate end-condition records contain first-byte values0/1/3/4/5/255. MONDE01's PT-BR briefing is an independent player-facing source; its wording is preserved in the original file and is not substituted for executing the condition evaluator. The original consumer `TestFinDeMission 0x458606` is called by `CalculGame 0x42c868` and queries resources, structures, ownership, influence, alliances, invention count, mission number and illumination. Its mission-specific branches and callback order need independent traces before implementation.

Four [original-only table captures](../pesquisas-paralelas/missoes/evidencias/captura-condicoes-original.json), created before translation, cover real MONDE01, zero-record condition input and synthetic nonempty objective words/flags. They returned in1,618 bounded segments with explicit inherited patterns, retaining adjacent globals/cursors. Native table-loader instructions execute unchanged; only successful FileRead data is supplied. Earlier evidence and reports remain untouched.

```sh
python3 -B pesquisas-paralelas/missoes/extrair_condicoes.py
python3 -B pesquisas-paralelas/missoes/capturar_condicoes.py
RISING_EMULAR=1 python3 -B -m unittest discover -s pesquisas-paralelas/missoes/testes -p test_condicoes.py -v
python3 -B pesquisas-paralelas/missoes/validar.py --emular
```

The next supported dependency now available is core's explicit selection-list initializer, integrated at main `140cc1a2ff38811fcbc02a1bda583e45f5f72462`; its four u16 stores preserve unit+bd flags and the rest of the2,048-byte allocation. A subsequent bounded mission wrapper can consume it before Stage1's continuation. It has not been silently replaced by constructor zeros, and no larger world/mission readiness follows from its existence. Remapping, structure/unit insertion, auxiliary AI tables, complete initialization tails, event/condition execution, dispatch and reference-game runtime remain open.

Fresh Stage 3 results:all26 mission tests pass with native mode, zero skips/failures/errors/native faults. The new table slice completes71 native FinMission calls and41 native Objectif calls in33,599 segments. Prior unit and prelude counts are separate repeats in the [Stage 3 report](../pesquisas-paralelas/missoes/validacao/stage3-suite-x86.json). Local mode executes17 tests and skips nine optional native tests. Common checks at inspected main pass core314/149 optional skips,combat198/123,economy337/151,graphics134/0,workflow3/0.

Stage 3 integrated at main `d079aa902a3e094385db2fe69c60f91e3f86f673`, final feature `fa317bf002fd8eb6809667fbb01b7817648ce999`, reviewed implementation `582de22e88ec019ba3c696a804886e78a0ec11cd`. The worker fetched that clean main, verified both feature and selection-provider ancestry, reproduced the changed table slice's eight native tests /112 calls /33,599 segments, and ran the complete local26-test suite with nine declared native skips before Stage 4. This narrower reproduction does not claim another full prelude-native run.

## Stage 4: complete unit-loader entry with selection initialization

`carregar_unidades_missao(leitor, unidades, valores_jogador, tipos_unidades, selecoes_unidades, *, modificador12=None)` in [carregador_unidades.py](../pesquisas-paralelas/missoes/carregador_unidades.py) now composes the **actual committed core** `inicializar_selecoes_unidades` provider before Stage1's unchanged continuation. It covers the original `LoadEngin 0x46acbf` entry, `0x46acc5 -> SelectionInit 0x472555`, continuation `0x46acca` and the original return. [Provider/call-position manifest](../pesquisas-paralelas/missoes/evidencias/selecao-carga-manifesto.json).

The additional input is an explicit inherited **bytearray of exactly2,048 bytes**, corresponding to `0x508728`. No default selection allocation or constructor state is supplied. The core initializer writes four u16 zeros, in order, at offsets0/512/1024/1536, preserving every other selection byte and every unit flag. The wrapper then calls the existing continuation with the same live buffers/type/modifier inputs. Its return is the existing `CargaUnidades` metadata, not CPU-register preservation or world readiness.

An invalid selection allocation is rejected by the core provider before loader reads/effects. Valid selection initialization occurs **before** the continuation's other input validation, four loader-byte stores, header reads or unit copies. Consequently a later protected input error, strict read failure or missing/raising modifier retains those four word stores. The unit pool's +bd bytes are not globally cleared; only the subsequent original ordinal writes act on them. No core selection logic or combat postload body is copied.

Four [independent original-only complete-entry captures](../pesquisas-paralelas/missoes/evidencias/captura-selecao-carga-original.json) preceded wrapper implementation:MONDE01, sparse/repeated units, empty block and a modifier-entry checkpoint. They use an explicit patterned selection allocation and inherited `0xa5` unit pool. Native `SelectionInit`, postload/type/bonus helpers run unpatched; successful file I/O remains supplied by the bounded adapter. Three original returns and one expected modifier stop span100 segments. Regressions compare all2,048 selection bytes and complete unit-pool hashes, loader bytes and cursors.

The previous continuation remains public for callers already at its checkpoint; its documented selection prerequisite has not been retroactively hidden. The new entry closes that prerequisite for callers of this one routine. It does **not** execute `MissionLoad`'s resets/open/remap/structure load, auxiliary tables, physical insertion or later AI/economic/graphics initialization. Complete mission selection, objective/event evaluation, cadence and reference-game runtime remain outside this API.

Fresh Stage 4 checks:31 mission tests pass in native mode with zero skips/failures/errors/native faults. New full-entry coverage is41 fixtures/10,600 segments:40 native returns and one expected modifier-entry stop, including every unit block in all38 original maps and explicit inherited selection bytes. Earlier unit-continuation, prelude and table counts remain separate repeats in the [Stage 4 report](../pesquisas-paralelas/missoes/validacao/stage4-suite-x86.json); no whole-mission coverage is inferred. Local mode executes20 tests and skips11 optional native tests. Common checks pass core319/151 optional skips,combat205/127,economy349/157,graphics141/0,workflow3/0. After integration/reproduction, the next independent slice is the original indexed structure-copy continuation after remap, preserving all72 uncopied bytes and stopping before unit loading.

Stage 4 integrated at main `37629edc282367702811f9b7060d2026b6ba9b47`, final feature `74834368edf19bb26e2413053cb653eef075f3be`, reviewed implementation `892244a19ed7b426059679736cc6afaf2812e75c`. The clean worker fetched that main, verified ancestry and reproduced all five changed native composition tests /41 fixtures /10,600 segments, plus the complete local31-test suite with11 declared native skips before Stage 5.

## Stage 5: indexed structure-copy continuations

`carregar_estruturas_missao(leitor, estruturas)` in [carregador_estruturas.py](../pesquisas-paralelas/missoes/carregador_estruturas.py) implements the identical buffer effects of two original inline paths: `MissionLoad 0x46c517..0x46c578` and `MissionLoadName 0x46c8e0..0x46c941`. Both stop **before** the call to `LoadEngin`; neither is `LoadBatiment 0x46b1fb`. [Exact original intervals and consumed reader identities](../pesquisas-paralelas/missoes/evidencias/estruturas-manifesto.json).

Supply the committed `Leitor` at the u16 count,size header, and a separate inherited writable contiguous u8 pool of **276,000 bytes**, corresponding to1,000 ×276-byte records at original `0x49a0c8`. The studied size is204. For each record, read its u16 index0..999, then copy exactly204 bytes into that indexed slot. Preserve the remaining72 bytes of **every** slot, all unloaded records, file order and repeated IDs. Count is an independent u16, not an allocation count limited to1,000: a valid1,001-record file can overwrite the same valid slot repeatedly. No compacting index remap, allocation, reset, active-state/type/owner initialization, terrain placement, region label or discovery flag is invented.

Buffer/reader validation precedes effects. Unsupported record size raises after header reads with the pool intact. A protected out-of-range ID raises after its read, preserving earlier completed copies. Strict input truncation preserves earlier complete copies; native Win32 short-read behavior is outside scope. Return `CargaEstruturas(quantidade, indices, fim, rotina_seguinte=0x46acbf)`, retaining all encountered IDs in order. The following unit call is metadata only. Existing raw reader `ler_estruturas_eta` is consumed in a contract regression; the stateful copy uses core's `Leitor` to preserve original read/failure ordering.

The original corpus contains **1,111 structure records** across38 maps, all size204, with disk indices0..631. This does not identify those disk records as fully initialized live structures. Earlier original global reset and remap must already have occurred; their effects are not recreated by filling the pool with zeros or by calling this copy routine. Core owns structure startup/reset and physical placement. Saved region slots, discovery bytes and other unpopulated fields remain inherited inputs until those actual providers establish them.

Four [original-only copy captures](../pesquisas-paralelas/missoes/evidencias/captura-estruturas-original.json) preceded implementation:actual MONDE01 through both original callers, sparse/repeated IDs and an empty block. They reach the pre-unit checkpoints in22 bounded segments, using a declared `0xa5` pool and synthetic caller stack scratch. Native instructions are unchanged and only successful FileRead input is supplied. Capture regressions compare complete276,000-byte pool hashes and changed records; all72 inherited bytes remain visible in the expected record buffers.

```sh
python3 -B pesquisas-paralelas/missoes/extrair_estruturas.py
python3 -B pesquisas-paralelas/missoes/capturar_estruturas.py
RISING_EMULAR=1 python3 -B -m unittest discover -s pesquisas-paralelas/missoes/testes -p test_carga_estruturas.py -v
```

This closes the original disk-index-to-structure-pool copy contract, not `MissionPlaceTerrain` or a prepared-world API. Remap/global startup, physical unit/structure insertion, remaining auxiliary loaders, initializer tails, mission selection/metadata, condition/event evaluation and runtime remain explicit. The next independent inventory is original mission filename selection and its branch/query inputs; mission1 is the primary runtime target and no later mission operation is inferred from additional raw-file coverage.

Fresh Stage 5 checks:37 mission tests pass in native mode, zero skips/failures/errors/native faults. New structure coverage reaches82 pre-unit checkpoints (41 per original caller) in8,706 bounded segments, with whole276,000-byte pool equality. Prior counts remain separate repeats in the [Stage 5 report](../pesquisas-paralelas/missoes/validacao/stage5-suite-x86.json). Local mode executes24 tests and skips13 optional native tests. Common checks pass core319/151 optional skips,combat211/131,economy349/157,graphics148/0,workflow3/0.

Stage 5 integrated at main `82a0468f5482ef00357bc077a75947c01b44aec4`, final feature `653d38a15869ed6d6fc478a365f6cc56ba9a2c30`, reviewed implementation `694051af7f4b29e607f7a75c0ca554bc6a2e4c44`. The clean worker fetched that main, verified ancestry and reproduced all six changed native structure tests /82 checkpoints /8,706 segments plus the complete local37-test suite with13 declared native skips before Stage 6.

## Stage 6: original mission filename selection

`nome_arquivo_missao(numero, destino, *, variante_u8=None, simpatia=None)` in [nome_missao.py](../pesquisas-paralelas/missoes/nome_missao.py) reconstructs complete `MakeMissionName 0x46c1b8..0x46c2cf`, using explicit query inputs. It writes the caller's inherited writable contiguous u8 buffer (at least20 bytes) and returns the filename bytes before NUL. [Original routine/query/string/pointer-table evidence](../pesquisas-paralelas/missoes/evidencias/nome-manifesto.json).

`numero` truncates to u8. The original copies its `\World\Monde00` prefix and NUL, then writes the two decimal-character bytes at offsets12/13. It accepts raw numbers0..255; values above99 yield the original nondecimal first byte. This is a byte-formatting contract, not evidence that every generated name identifies a mission asset. Original casing, backslashes and lowercase suffix letters remain unchanged; this is not a PT-BR mission title or a translated player label.

For number9 only, provide the inherited raw byte originally at `0x4e1d85` as `variante_u8`. Its low u8 must be0..3 and selects literal suffix `a`/`b`/`c`/`d` from the original pointer table at `0x497154`. Missing input raises `DependenciaNomeMissao` at `0x46c23e` after the numeric prefix was written. An unsupported suffix index is protected after that same prefix effect; no default previous-result value or guessed campaign outcome is installed.

For numbers10/12/17 only, provide read-only `simpatia(owner, other)`. The routine always queries `(1,0)`, `(2,0)`, `(3,0)` in order. It consumes **signed low8**, not the provider's full signed16 result. Initial comparison value is90 and initial choice is1. Replace the choice only when the current signed value is strictly greater than the newly queried signed byte, preserving initial/earlier choices on a tie. Consequently values100/90/127 still select suffix `a`, rather than replacing the initial choice on the later90. This follows original byte `CMP CL,AL` / signed `JLE`, not a generic minimum over the full words.

Use the committed bound `Mercado.simpatia` query with an explicitly supplied intended player table. Its source uses4×20 bytes and signed i16 at+12+2×other; the mission caller narrows its return. Negative i16 `0xff01` becomes low-byte+1; positive128 becomes low-byte−128. The query is directional and adds no alliance/type adjustment. `Mercado` **copies** constructor inputs; a bound query does not automatically follow later mutations of a separate player buffer. No constructor-generated zero table is treated as mission state.

Other raw numbers query neither input. After any required queries, append the selected suffix if present, then `.ETA` and NUL, preserving all destination bytes beyond the last store. Missing sympathy raises a named `0x46dc6c` dependency after prefix/digits. A callback exception at any query propagates with that same partial buffer; no suffix/extension is written yet. Shape validation precedes effects. No file-exists/open operation, mission number progression, formal-name/title load or campaign transition is executed.

Eight [original-only filename captures](../pesquisas-paralelas/missoes/evidencias/captura-nome-original.json) preceded translation:ordinary and variant paths, signed-byte boundaries, upper-register poison, raw255 and a stop before the second native query. Seven return and one deliberately stops, in eight bounded segments. Native `MakeMissionName` and `PlayerGetSympathie` execute unpatched against an explicit synthetic80-byte player table and inherited destination. Regressions compare all64 destination bytes, ordered query arguments and retained player bytes.

```sh
python3 -B pesquisas-paralelas/missoes/extrair_nome.py
python3 -B pesquisas-paralelas/missoes/capturar_nome.py
RISING_EMULAR=1 python3 -B -m unittest discover -s pesquisas-paralelas/missoes/testes -p test_nome_missao.py -v
```

This closes the original filename branch/width/query-order contract and does not establish campaign routing, selected mission loading or execution. Core is preparing exact world startup/placement providers. The next meaningful world join will preserve `MissionPlaceTerrain`'s original predicates:unit state+2 nonzero (including4), then raw+72 nonzero, before `PlaceEngin`. These differ from a generic alive-unit filter. The committed exact lower predicates/placement/remap must be consumed rather than inferred or duplicated.

Fresh Stage 6 checks:44 mission tests pass in native mode, zero skips/failures/errors/native faults. New filename coverage is3,268 calls/segments:3,265 returns and three expected sympathy-query stops. It covers all256 raw number bytes with poisoned upper bits, all three query branches over signed-byte/word boundary triples, explicit variants and each partial query checkpoint. Earlier slice counts remain separate repeats in the [Stage 6 report](../pesquisas-paralelas/missoes/validacao/stage6-suite-x86.json). Local mode executes28 tests and skips16 optional native tests. Common checks pass core332/157 optional skips,combat211/131,economy362/164,graphics155/0,workflow3/0.

Stage 6 integrated at main `eb0ecb3622142812392a6d0c73dce7002040717f`, final feature `61c9d9402a7724b77baca0ca33db4a545fcef2ab`, reviewed implementation `7c4c4e12d36e5c2a47ae1b2503c7bdadcc94521f`. The clean worker fetched main `189c94eac6700c5d0fb24dc547d5da015734b06d`, verified ancestry and reproduced all seven changed filename-native tests /3,268 calls plus the full local44-test suite with16 declared native skips before Stage 7. Core placement was not yet available; the independently supported immediate post-unit prefix was selected while waiting for that exact contract.

## Stage 7: first auxiliary loaders in original caller order

[carregador_auxiliares.py](../pesquisas-paralelas/missoes/carregador_auxiliares.py) adds `carregar_minas_missao`, `carregar_ataques_missao` and their ordered composition `carregar_minas_e_ataques(leitor, minas, ataques)`. This reproduces `MissionLoad 0x46c57d..0x46c587` and `MissionLoadName 0x46c946..0x46c950`:complete `LoadMine 0x47534a`, then complete `IALoadAttaqueIni 0x47c24d`, **stop before `LoadBatimentGhost 0x47bcc7`**. [Original bodies/caller intervals and input identity](../pesquisas-paralelas/missoes/evidencias/auxiliares-manifesto.json).

`minas` is an inherited writable contiguous **80-byte** table at original `0x509954`, twenty little-endian `(origin_u16,reserve_u16)` records. Read u16 count0..20, then count4-byte records into ordinal slots. Only after all supplied records are read, clear the origin word of each trailing slot. Preserve its reserve word. No fixed-size header, allocation, extraction, economic credit or zero-filled reserve default is inserted. A count outside the protected table fails after its header read; a strict record failure retains earlier copies and does not prematurely clear trailing origins.

The caller may pass the actual `RecursosTerreno.minas` bytearray. The economic constructor copies input bytes, and its zero default is synthetic. Loading in place preserves the object's table identity; the existing `capacidade_mina` query can observe a retained reserve even when origin is zero. Existing economic extraction/arithmetic/terrain aliases remain owner-provided; this module only loads the raw mission table.

`ataques` is an inherited writable contiguous **1,004-byte** allocation at `0x50d5b4`:100 runtime records of10 bytes, followed by the u32 at `0x50d99c`. Before header reads, clear the counter, then initialize each record in order:u8+0=200,+1=255,u16+2=ffff,u8+4=255,+5=255,u16+6=ffff,u8+8=0. **Byte+9 is preserved** in every record. Read u16 count,size, protected to count0..100,size8; copy each eight-byte disk record into the beginning of its ten-byte runtime slot. Byte+8 retains its explicit reset and byte+9 remains inherited. These are raw configuration values, not an implementation of attack AI or an inferred owner/state model.

Each individual reader checks buffer shape before its own effects. The combined entry deliberately finishes the mine reader before entering attack-buffer validation/initialization, preserving original call position and partial effects. Unsupported attack header raises after its complete initial reset/header reads. Strict input/callback failures do not roll back earlier work; Win32 partial-read behavior is excluded. Return `AuxiliaresIniciais(minas, ataques, fim, rotina_seguinte=0x47bcc7)` is checkpoint metadata; it does not invoke an unsupported next loader, VM operation or event.

Four [original-only prefix captures](../pesquisas-paralelas/missoes/evidencias/captura-auxiliares-original.json) preceded translation:MONDE01 through both callers, empty tables and maximal20/100 records, with explicit inherited mine0x63 and attack0xa5 bytes. All reach the pre-Ghost checkpoint in140 segments. Native loader bodies and caller order are unpatched; successful FileRead input and caller stack scratch are bounded fixture inputs. Whole80/1,004-byte snapshots validate retained reserve/+9 bytes independently of the reconstruction.

The initial actual-economy-object regression exposed an existing flat-module collision:both economy and graphics publish `construcoes`, while economy `extracao` imports its own unqualified name. The production mission API therefore remains an in-place raw-buffer interface. The actual `RecursosTerreno.minas`/capacity regression runs in an **isolated ordinary Python test process**, with normal economic imports before the mission reader. No provider source is copied, rewritten or globally rebound; no extra AI worker/chat is created. General economic+graphic module coexistence remains a coordinator/consumer namespace dependency. A passing isolated regression does not establish that combined application import path.

```sh
python3 -B pesquisas-paralelas/missoes/extrair_auxiliares.py
python3 -B pesquisas-paralelas/missoes/capturar_auxiliares.py
RISING_EMULAR=1 python3 -B -m unittest discover -s pesquisas-paralelas/missoes/testes -p test_auxiliares.py -v
```

The corpus-supported bounds are mine counts0..20 and attack counts0..100,size8 across all38 maps. The next loader/initializer, physical world insertion, natural remap, shared VM semantics, event/objective evaluation and runtime remain unsupported boundaries. Core's exact unit reset is now available separately at main `b9b6f726895a2e0f800bb8f986f28a767104a882`; constructor bytes are still synthetic. Actual `PlaceEngin`/predicate providers will be consumed for the next meaningful world join when committed, rather than replaced with copied logic or generic live-unit filtering.

Fresh Stage 7 checks:50 mission tests pass in native mode, zero skips/failures/errors/native faults. New auxiliary coverage reaches320 pre-Ghost checkpoints (160 per caller) in14,270 bounded segments, covering both callers/all38 maps and every supported mine/attack count. Earlier slice counts are separate repeats in the [Stage 7 report](../pesquisas-paralelas/missoes/validacao/stage7-suite-x86.json). Local mode executes32 tests and skips18 optional native tests. Common checks pass core332/157 optional skips,combat219/137,economy362/164,graphics162/0,workflow3/0.

Stage 7 integrated at main `9e60bcea5ce57d986a617c13c274c75da18c6c08`, final feature `b7f49785fdcc2a72fd5e11b308b7aa79689ae016`, implementation `aa89188b48d2f98c9a1cfe0c3d7cc33e7cb35ab8`. The clean worker verified fetched ancestry and reproduced the six changed auxiliary tests /320 native checkpoints /14,270 segments, plus the complete local50-test suite with18 optional skips before Stage 8.

## Stage 8: unit placement and capacity caller prefix

[terreno_unidades.py](../pesquisas-paralelas/missoes/terreno_unidades.py) adds `preparar_unidades_no_terreno(provedores)` for **`MissionPlaceTerrain 0x46c122..0x46c16d` only**, stopping before structure traversal. The [original-byte/provider manifest](../pesquisas-paralelas/missoes/evidencias/terreno-unidades-manifesto.json) pins inspected main `6b15be1c96348d51dac7a46208126e6974290eca`; actual core placement arrived at main `92d8c1e93062b97f1872ce65b2dd5b8a3e98499e`. No lower primitive is copied.

Supply `ProvedoresTerrenoUnidades(existe, visibilidade, colocar, capacidades)` with four actual callbacks. The caller scans all800 pool indices in ascending order, querying `existe(index)` and consuming lowAL. Only a nonzero result reaches `visibilidade(index)`; only nonzero lowAL visibility reaches `colocar(index)`. After the entire scan, call `capacidades(owner)` for0,1,2,3 in that order. The result contains the indices whose placement callbacks completed and the next checkpoint `0x46c16d`. Missing callbacks raise `DependenciaTerrenoUnidades` when first reached, naming their original targets. Later failures preserve prior effects; there is no rollback or implicit retry.

`provedores_terreno_core(mundo, *, bonus_unidades=None)` binds the actual committed `existe_unidade`, `visibilidade_unidade`, `colocar_unidade_missao` and `atualizar_capacidades_unidades` functions to an **explicit inherited world**. Existence means state+2 !=0, including state4; visibility returns raw+72. These are not the world's generic alive predicate. Placement retains current position/order/search state, inserts collision, sets+72=1, then performs the supported discovery/light/minimap operations. Core's supported type/owner/map/camera/minimap and vision domains still apply. Selection bytes and active search state remain live and are checked unchanged.

Capacity refresh uses the actual economy `capacidade_tipo` and supplied `BonusUnidades.consultar(owner,type,1)` query. Core skips states0/4 and nonmatching owners, queries base capacity then the modifier, and stores the low16 result at unit+0x0c. An absent bonus object is **not** replaced with zeros:the first reached selector1 query raises at `0x428cc0`, after all earlier placement effects. If no active normal-owner query is reached, no bonus input is required or manufactured. Input tables and world buffers must be the intended loaded/inherited state; constructors are not an original startup substitute.

Four [original-only full-prefix captures](../pesquisas-paralelas/missoes/evidencias/captura-terreno-unidades-original-v2.json) originated before the orchestration:ordinary, state4/owner200, state14/hidden and the actual MONDE01 unit stream. The surrounding region/color/physical/search inputs are explicitly synthetic; MONDE01's four raw layers and committed graphics normalization are preparation for this bounded fixture. Intervening auxiliary effects, natural reset/remap and complete startup are not claimed. Native lower routines execute unchanged, with preserved CPU/stack state across minimap segmentation.

The first export had an **input trace alias bug**:its `parent_calls` list later acquired the output calls. Buffer hashes and complete output dictionaries were unaffected. The [first export is retained](../pesquisas-paralelas/missoes/evidencias/captura-terreno-unidades-original.json); v2 freezes the list and the original-only recapture asserts every prior output dictionary unchanged. This correction does not alter expected original effects to fit Python.

MONDE01 exposes a genuine provider boundary:unit15 has radius10. Seven earlier insertions complete; unit15's collision/+72 effects occur before core raises `DependenciaColocacaoMissao` at target `0x476851`, caller checkpoint `0x457019`, before discovery. A [supplementary original capture at that exact caller checkpoint](../pesquisas-paralelas/missoes/evidencias/captura-terreno-unidades-monde01-limite.json) validates all partial effects. The retained full original observation does not imply the Python provider completes that input. Re-entering from the beginning can repeat earlier discovery/light counts and is not a continuation API.

Two additional deliberate [caller-aligned captures](../pesquisas-paralelas/missoes/evidencias/captura-terreno-unidades-limites-chamador.json) cover missing bonus and synthetic radius9. The [initial callee-entry captures](../pesquisas-paralelas/missoes/evidencias/captura-terreno-unidades-limites.json) remain retained:their diagnostic trace includes attempted discovery entry, whereas core's explicit dependency stops before the CALL. Tests compare the matching caller checkpoints, including all unit/physical/selection buffers, search state and callback order.

Owned regressions now consume coordinator maintenance main `167615ecf5ef972dcc808156d11c71a3e3814165` through `integracao.providers.load_graphics_structures()` and `load_economy_resources()`. The Stage5 graphics reader and Stage7 actual economic-buffer test coexist in the **same Python process**, replacing the earlier subprocess isolation. The bootstrap exposes the repository root before legacy flat graphics imports. The adapter preserves the economic `construcoes` binding and loads graphics under its distinct module identity; polluted/foreign bindings are rejected rather than rewritten. Its supported provider namespaces do not imply arbitrary application import compatibility. [Adapter contract](PROVIDER_IMPORTS.md).

```sh
python3 -B pesquisas-paralelas/missoes/extrair_terreno_unidades.py
RISING_EMULAR=1 python3 -B -m unittest discover -s pesquisas-paralelas/missoes/testes -p test_terreno_unidades.py -v
python3 -B pesquisas-paralelas/missoes/validar.py --emular
```

This is the final current research stage under the human cutoff:finish validation, commit, checked integration and remote push, then **stop without another slice or rebuild**. Structure traversal, remaining loaders/initializers, natural remap after its first allocation boundary, mission dispatch, condition/event execution and real mission runtime remain explicit gaps. Core's pre-allocation remap reset at main `8fcf1d35e9945d98eac07da8975ff933e4b9fe0b` is a separate bounded provider; it is not a completed remap and is not silently inserted here.

Fresh Stage 8 checks:all56 mission tests pass in native mode with zero skips/errors/failures/native faults. New placement coverage is102 prefixes:99 reach the pre-structure boundary and three intentionally stop at dependencies, spanning139 prefix segments including37 preserved-state minimap resumptions. Their102 preparatory original unit-loader entries use876 separate segments. Earlier slices are reported separately in the [Stage 8 report](../pesquisas-paralelas/missoes/validacao/stage8-suite-x86.json); these counts are not combined into game coverage. Local mode executes35 tests and skips21 optional native tests. Common checks pass core350/166 optional skips,combat227/143,economy377/172,graphics169/0,workflow6/0. Documentation links and `git diff --check` pass.

## Stage 9a: placement tests keyed to core's published discovery domain

No reconstructed behavior changes. The placement tests read core's agreed symbol `getattr(colocacao_missao, 'SOMA_VISAO_MAXIMA_INSERCAO', 8)`: the inclusive maximum normal-owner vision sum `u8 unit+0xbb + u8 unit+0xf5` for which `PlaceEngin 0x456fa6` completes `DecouvreTerrain 0x476851` (radius sum+2), `IllumineTerrain 0x476cb3` and `SetMiniMap`. An absent symbol means the committed limit 8; 510 is the whole u8+u8 range and leaves no reachable discovery stop. A larger sum still raises `DependenciaColocacaoMissao` at target `0x476851`, caller checkpoint `0x457019`, with collision/+72 retained.

- **MONDE01.** The test asserts from the loaded pool that unit 15's sum is 10. While 10 exceeds the published maximum, it expects the unit-15 dependency and compares the boundary capture. Otherwise it compares the complete scan against the retained [original full-prefix capture](../pesquisas-paralelas/missoes/evidencias/captura-terreno-unidades-original-v2.json) through `0x46c16d`, every buffer, trace and callback included; reaching the end without an exception is not the criterion. The native differential compares the unstopped original prefix in the same way.
- **Forced stop.** The differential uses the first sum outside the domain, maximum+1, on the ordinary fixture's unit 7. Up to 255 it goes through the type word at +42; from 256 to 510 it sets +0xbb=255 through the type word and writes the remainder to +0xf5 after both loads, on the native and Python sides. When the maximum is 510, the same fixture with sum 9 is compared against the native continuation instead.
- **Static caller-aligned vision9.** While 9 is outside the domain, it compares the retained stop capture. Inside the domain, it compares a new [original-only vision9 continuation capture](../pesquisas-paralelas/missoes/evidencias/captura-terreno-unidades-visao9-continuacao.json): the same fixture with the native discovery, light and minimap bodies unpatched, run to `0x46c16d` (one unit-load entry, one prefix, 39 segments, 30 preserved minimap resumptions). Predecessor captures are unchanged.

At the current committed limit 8, the six placement tests pass in native mode. A scratch-only simulation of core limits 9, 10, 300 and 510, which raised the core check inside the test process without editing core files, also passed all six natively; that run is branch coverage for these tests, not provider validation.

## Stage 9: complete L7 auxiliary chain in both callers

[carregador_cadeia_auxiliar.py](../pesquisas-paralelas/missoes/carregador_cadeia_auxiliar.py) adds the four remaining raw readers and `carregar_cadeia_auxiliar(leitor, buffers, *, tipos_grupo8, perfil)`. That function reproduces `MissionLoad 0x46c57d..0x46c5a5` and `MissionLoadName 0x46c946..0x46c96e` and stops before `FileClose 0x45844c`. The original bytes of both callers, in the [exported caller intervals](../pesquisas-paralelas/missoes/evidencias/cadeia-auxiliar-manifesto.json), give the same order:

`LoadMine 0x47534a` → `IALoadAttaqueIni 0x47c24d` → `LoadBatimentGhost 0x47bcc7` → `LoadCadreInfluence 0x47c04a` → `LoadFinMission 0x458b05` → `LoadCalculMissionDivers 0x47c30f` → `LoadObjectif 0x47c404` → `LoadEntrerMonstre 0x47ac30`

The Stage 3 and Stage 7 readers are composed unchanged. `BuffersCadeiaAuxiliar` holds writable contiguous views in original widths: mines `0x509954`/80, attacks `0x50d5b4`/1,004, ghosts `0x50b18c`/5,254, influence `0x50c614`/4,000, end conditions `0x4e1d20`/114, objectives `0x511ffc`/804, monsters `0x50a9bc`/1,220, groups `0x50af84`/432, and the live `Random` state `0x497164`/4. Every shape guard, plus the explicit 8-byte group type table `0x498400`, is checked before the first effect. After that point a failure keeps every earlier effect, including the advanced `Random` state; nothing rolls back.

| Reader | Original effect order | Supported domain (named `ForaDoDominioAuxiliar` beyond it) |
|---|---|---|
| `LoadBatimentGhost 0x47bcc7..0x47bd40` | The u16 count is read into +0. Flags +4504+i become `0xff` for i < count. Count pairs are then read: u16 → +2+2i, u32 → +1504+4i. Bytes +1502/+1503 are kept. AL = 0 for an empty table, else 1; callers ignore it | count ≤ 750 (stop before flag 750 at `0x47bce1`); corpus max 747 |
| `LoadCadreInfluence 0x47c04a..0x47c0c3` | Words +0/+2/+4/+6 of all 400 ten-byte slots become `0xffff`, with +8/+9 kept. The u16 count and u16 size are read into stack locals; the size is read even when count = 0. Count records of `size` bytes are then read at slot×10. A size above 10 overlaps the next slot, as in the original | last write ≤ 4,000 bytes (stop before the record read at `0x47c0b1`); the original would reach the attack table. Corpus: size 10, count ≤ 399 |
| `LoadCalculMissionDivers 0x47c30f..0x47c359` | 16 one-byte reads into a stack scratch byte; no global store. The bytes are returned for diagnosis only | any; five distinct corpus patterns |
| `LoadEntrerMonstre 0x47ac30..0x47ad6a` | Detailed below | count ≤ 100 and last write ≤ 1,200 bytes (stop before the read at `0x47ac9b`). Corpus: count 100, size 6 |

**LoadEntrerMonstre.** The routine first calls `InitEntrerMonstre 0x47a601`. That call:
1. Initializes the 100 twelve-byte records at monsters+20, in order: u16+0 = `ffff`, u16+2 = `ffff`, u16+4 = 0, u32+8 = 0. Each record then calls `Random 0x4704dc`, through core's committed `candidatos_rota.aleatorio_caminhos` with the state written back after every call, and stores the low four bits of the result at +6.
2. Stores 0 at the HumanOnly byte +0.
3. Makes four `GetPrivateProfileIntA` calls on `./monstre.ini [GENERAL]`: `HumanOnly` with default 0 (nonzero stores 1), then `ProbaCaveJoueur` 5, `ProbaCaveIA` 2 and `ProbaEmbuscade` 2, as dwords at +4/+8/+12.
4. Clears the 432 group bytes with the engine `memset`.
5. For `GROUPE00..GROUPE15`, calls `GetPrivateProfileStringA` (default "", size 256). A nonzero result is split on commas. Each token parsed by `sscanf("%i")` maps through `0x498400[value]` to a unit type, and the routine increments the group count byte at +416+g and the type count at g×26+type.

The loader then:
1. Reads the u16 count into +18 and the u16 size into a local.
2. Reads each record into its slot, then sets u16+4 ×= 30 (low 16 bits) and u32+8 = 0. Starting after the old +6 value, it searches cyclically for the next set bit of the u16+2 mask and stores that bit index (or `0xff` if no bit is set) at +6. With the corpus size 6, the +6 starting point is the Random-initialized value.
3. Walks backward from the last record. An empty word0 (`ffff`) decrements the count. A used record copies **only its word0** into the highest lower empty slot and decrements the count. If no empty slot lies below a used record, the pass ends.

No monster spawning, AI, cave-probability or ambush semantics is interpreted. `InitMissionMonstre 0x47af90` (an IaReset tail, owned by AI/runtime) consumes these tables later.

**Declared binding.** [perfil_privado_missao.py](../pesquisas-paralelas/missoes/perfil_privado_missao.py) `PerfilPrivado({b'./monstre.ini': bytes_or_None})` answers both KERNEL32 profile functions from files the caller declares.
- An undeclared file raises `DependenciaPerfil`. A file declared as `None` is absent, and every query then returns the documented Windows default.
- Only a strict INI subset is accepted: case-insensitive section and key names, no padding, no quotes, no duplicates, decimal integers. Values are truncated to nSize−1.
- `perfil=None` raises `DependenciaEntradaMonstros` at CALL `0x47a665`, after the record initialization and the HumanOnly zero store.
- The shipped `INSTALHD/MONSTRE.INI` (233 bytes) has only `GROUPE00..14`, so the four integers take their defaults.

The `sscanf("%i")` translation supports blanks, a sign and decimal digits. Octal or hex forms and overflow raise at `0x48c41c`, and group indices outside 0..7 raise at `0x47a7c9`. This is a Python translation of engine CRT behavior, validated against the native Watcom bodies.

**Native harness.** [bancada_cadeia_auxiliar.py](../pesquisas-paralelas/missoes/bancada_cadeia_auxiliar.py) runs every engine body unpatched: the loaders, `InitEntrerMonstre`, `Random`, and the complete Watcom `memset`/`sprintf`/`sscanf`/`__prtf`/`__scnf` bodies with their SBL bounds. It replaces only two things:
- the game read wrapper `0x458461`, with fixture bytes;
- the five profile CALL sites `0x47a665/0x47a688/0x47a6a5/0x47a6c7` (IAT `0x5231ac`) and `0x47a74d` (IAT `0x5231b0`). The bench reads the stdcall arguments, writes the declared result, pops the arguments and resumes after the CALL. This is a mission-local binding until core publishes the generic binding facility.

Comparisons cover the complete DGROUP+.bss image `0x494000..0x523000`, not only the tables. They also cover the read sequence, which shows the 16 single-byte Divers reads, and the exact profile-call log. A predicate stop compares the native state just before the first unsupported write or call with the Python state after its named exception.

The [original-only captures](../pesquisas-paralelas/missoes/evidencias/captura-cadeia-auxiliar-original.json) were made before translation. They cover all 38 maps in both callers with the shipped profile, plus 10 synthetic streams × 2 callers: an absent profile, synthetic tokens with seed 0, 750 ghosts / 400 influence records, influence sizes 0/6/12 and overlap, and monster compaction plus counts and sizes. All 96 entries return, in 167,950 bounded segments with 165,934 read bindings and 1,920 profile bindings. Inherited tables, gaps and `Random` state are explicit synthetic patterns.

```sh
python3 -B pesquisas-paralelas/missoes/extrair_cadeia_auxiliar.py
python3 -B pesquisas-paralelas/missoes/capturar_cadeia_auxiliar.py
RISING_EMULAR=1 python3 -B -m unittest discover -s pesquisas-paralelas/missoes/testes -p test_cadeia_auxiliar.py -v
python3 -B pesquisas-paralelas/missoes/validar.py --emular
```

Fresh Stage 9 checks: all 65 mission tests pass in native mode, with zero skips, errors, failures or native faults.

The new chain coverage is 270 caller entries (124 MissionLoad, 146 MissionLoadName). They resolve to 227 returns, 18 declared boundary stops and 25 strict-input failure stops, over 324,811 bounded segments with 318,287 read and 4,744 profile bindings:
- **Map comparisons.** All 38 maps in both callers, with fresh inherited images and seeds.
- **Domain sweeps.** Ghost counts 0/1/2/374/749/750. Every influence size 0..12 × counts 0/1/2/399/400 inside the table. Monster counts 0..100 × sizes 0..24 inside the table, including overlap. 12 random compaction patterns, 7 Random edge states, and the absent and synthetic-token profiles.
- **Boundary and failure stops.**
  - A missing binding, an undeclared file, and each unsupported-domain site in both callers.
  - Truncations at 13 sampled MONDE04 reads, each cut at the read start and at its last byte.

Earlier slice counts are repeated separately in the [Stage 9 report](../pesquisas-paralelas/missoes/validacao/stage9-suite-x86.json); the Stage 1–8 reports are unchanged. Local mode runs 65 tests with 24 optional native skips. Common local checks at base `f18b5a0` pass: core 357/169 optional skips, combat 227/143, economy 393/180, graphics 176/0, missions 65/24, ai-runtime 3/0, workflow 8/0.

Remaining boundaries:
- FileClose and the rest of MissionLoad (Stage 10 reset prefix, remap, structure placement scan, tails) are not composed here.
- Ghost, influence and monster-entry runtime meaning is not established.
- MONSTRE.INI integer keys other than the defaults, and profile syntax outside the strict subset, are unsupported.
- No mission was run.

## Stage 10: reset prefixes of both callers to FileOpen

[reinicio_missao.py](../pesquisas-paralelas/missoes/reinicio_missao.py) composes the reset prefix of each caller from the [original call lists](../pesquisas-paralelas/missoes/evidencias/reinicio-manifesto.json), whose bytes, interval hashes and callee hashes are exported. The coordinator assigned three UI leaf resets and the two ffff words to missions. No other front models them, except that the balloon table is economy's `PropriedadeConstrucoes.baloes`; BallonInit is a store-only reset over that buffer, applied by identity, and economy's balloon semantics stay economy's.

**MissionLoad 0x46c2cf..0x46c389.**
1. Read the inherited mission byte `0x496fe4`. Call Stage 6 `MakeMissionName` into the stack local at +0x100.
2. strcpy the inherited C string `0x509594` into the 0x100-byte local, then strcat the name. A path ≥ 0x100 bytes is outside the domain and raises at `0x46c333`.
3. Store u16 `0x4e1a38` = `0x4e1a3a` = `0xffff`.
4. Call, in order: IconeReset, **TerrainReset `0x46b315` (CALL `0x46c35f`)**, **MiniMapReset `0x469f00` (`0x46c364`)**, core `resetar_todas_estruturas` (`0x46c369`), core `resetar_todas_unidades` (`0x46c36e`), combat `resetar_projeteis` (`0x46c373`), MessageBoxInit (`0x46c378`), BallonInit (`0x46c37d`).
5. Stop at `FileOpen 0x458420(path, "rb")` with `PedidoAbertura(caminho, modo, nome)`. The open is the caller's file binding.

**MissionLoadName 0x46c5e3..0x46c75f.**
1. The same words and calls through MessageBoxInit, with the CALLs at `0x46c60a..0x46c628`.
2. Inline zeroing of 4×26 bytes at `0x4e1934` and 4×22 at `0x4dfad4`. These are economy's habitation realizability tables, applied by identity.
3. SortilegeResetTechnologie `0x4749f2` (economy `Aprendizagem.zerar_tecnologia`, `0x46c687`).
4. **RechercheReset `0x470b46` (`0x46c68c`)**.
5. **Engin_ResetExperience `0x441470` (`0x46c691`)**.
6. u8 `0x496fe4` = `0x32`.
7. ReseauActif `0x42c3b0`, which is only `AL=[0x4e0730]`. The byte is an explicit inherited input. If it is nonzero: **RechercheCheat `0x4716fe` (`0x46c6a6`)**, then **RechercheStore `0x4714f0` (`0x46c6ab`)**.
8. BallonInit (`0x46c6b0`).
9. Path: `0x509494` if `stricmp(name+len-4,".NET")==0`, else `0x509594`; then `\WORLD\`, then the name. A name shorter than 4 bytes reads before the buffer and raises at `0x46c6c5`; a path ≥ 0x114 bytes raises at `0x46c742`.
10. Stop at FileOpen `0x46c75f`.

Bold callees have no committed provider. They are `ProvedoresReinicio` callables; when one is `None`, `DependenciaReinicio(rotina, endereco, chamada, chamador, caminho)` is raised at its CALL and every earlier store is kept. Today the full compositions therefore stop at TerrainReset, after the words and IconeReset. The continuations `continuar_reinicio_missao` and `continuar_reinicio_missao_nome` enter at the original instruction after MiniMapReset (`0x46c369` / `0x46c619`), in the established Stage 1/2 continuation pattern. Every buffer, directory and name guard precedes the first effect.

| Leaf (missions) | Original effect order |
|---|---|
| `IconeReset 0x45e88f..0x45e90b` | For each of the 10 six-byte records at `0x4e2410`, in order: if the record ≠ (u16 `0x29b1`, u16 1, u16 0), store u8 1 at `0x4e05a2`, which is never cleared. Then rewrite the record |
| `MessageBoxInit 0x469908..0x46994b` | u16 `0x507d54` = `0x507d56` = 0, u8 `0x507d58` = `0x507d59` = 0, then byte +0 of each of the 256 records of 518 bytes at `0x4e7754`. The table ends exactly at `0x507d54` |
| `BallonInit 0x441b6c..0x441baa` | For each of the 4 eight-byte records at `0x4e1a14`: u16 +4 = u16 +6 = `ffff`, u16 +0 = 0, u8 +2 = 0. +3 is kept |

`MemoriaReinicio` holds these widths: words `0x4e1a38`/4, icons/60, flag/1, message boxes `0x4e7754`/132,614, balloons/32, structures `0x49a0c8`/276,000, structure flags `0x49a070`/88, structure selections `0x495be0`/8, a core world exposing `.unidades` and `.bolsas_tipos_unidades`, the projectile pool reached through `0x5080f0`/5,600, and the mission byte. The core-consumed pools must be `bytearray`s, as core requires.

**Validation.** [bancada_reinicio_missao.py](../pesquisas-paralelas/missoes/bancada_reinicio_missao.py) runs all engine bodies unpatched, including MakeMissionName with PlayerGetSympathie and the committed provider routines. Entries cover the three leaves, both caller prologues stopping before the TerrainReset CALL, and both continuations with the caller frame. The MissionLoad continuation stops at FileOpen; the MissionLoadName continuation stops before the RechercheReset CALL. Each comparison covers the whole DGROUP+.bss image, the unit pool, the four type Bags, the projectile pool, the player table and the strings in the frame.

The [original-only captures](../pesquisas-paralelas/missoes/evidencias/captura-reinicio-original.json) were taken before translation: 170 entries, each reaching its declared stop (105 leaf returns, 50 + 4 TerrainReset stops, 3 FileOpen stops, 8 RechercheReset stops).

```sh
python3 -B pesquisas-paralelas/missoes/extrair_reinicio_missao.py
python3 -B pesquisas-paralelas/missoes/capturar_reinicio_missao.py
RISING_EMULAR=1 python3 -B -m unittest discover -s pesquisas-paralelas/missoes/testes -p test_reinicio_missao.py -v
```

Fresh Stage 10 checks: all 71 mission tests pass in native mode, with zero skips, errors, failures or native faults. The new reset coverage is 459 native entries in 459 bounded segments, and each reaches its declared stop:
- 176 leaf returns: every IconeReset field/record mismatch, plus random records with flags 0/1/2/255, and the MessageBoxInit and BallonInit patterns.
- 259 MissionLoad prologues stopping before the TerrainReset CALL: all 256 mission bytes, number 9 with variants 0..3, and the 10/12/17 sympathy branches, with empty, ordinary and long directories.
- 4 MissionLoad continuations stopping at FileOpen.
- 5 MissionLoadName prologues stopping before TerrainReset.
- 15 MissionLoadName continuations stopping before RechercheReset: `.NET` case variants, short names, and network bytes 0/1/7.

The first full native run failed one Stage 2 header case, MONDE17 with camera 4. Under a machine load average of 11, the core harness's 1-second wall-clock segment timeout expired. That failure is logged in ignored `.local/` and not counted as a pass. The test passed in isolation, and the complete rerun passed. The [Stage 10 report](../pesquisas-paralelas/missoes/validacao/stage10-suite-x86.json) records the clean run; predecessor reports are unchanged.

Local mode runs 71 tests with 27 optional skips. Common local checks at `7b7b969` pass: core 368/175, combat 236/145, economy 413/190, graphics 184/0, missions 71/27, ai-runtime 25/1, audio 2/0, workflow 8/0.

Remaining boundaries:
- TerrainReset and MiniMapReset (core's next stage) stop both full prefixes today. The tails are validated as continuations from their original post-MiniMapReset instructions.
- RechercheReset, RechercheCheat, RechercheStore and Engin_ResetExperience stop the MissionLoadName tail.
- FileOpen and everything after it belong to Stage 12. No mission was run.

### Planned contract: `carregar_missao` M1 result (requested by macOS)

Recorded as planned; not implemented. The result of `carregar_missao(numero, ...)` will carry:
- **Identity and status.** The mission number, the generated MakeMissionName bytes and the opened path, and the ETA SHA-256 and size. The ordered list of completed original calls (address, SBL name). Either the complete `0x46c2cf` return or the named dependency (callee, CALL site, detail) with the partial state attached. The whole-MissionLoad oracle status with its report path and SHA-256, or explicitly absent.
- **Raw buffers**, each with exact length and original address. Read-only copies are fine, and the set stays stable into M2:
  - terrain layers, dimensions, camera view, viewer byte `0x508041`, per-player discovery/light maps and minimap state;
  - remap outputs, as core publishes them;
  - the unit pool, loader bytes `0x4e19bc` and placed indices;
  - the structure pool `0x49a0c8`, ghosts `0x50b18c` and influence `0x50c614`;
  - selections;
  - Economia, players, technology, cave, market and experience;
  - mines, attacks, conditions, objectives and EntrerMonstre/groups. Divers is not a table: its 16 discarded bytes are exposed as diagnostics.
  - the projectile pool, AI tables after IaReset (no iaInit, which has no caller), message-box/balloon/icon state, and the unit-type and bonus rule inputs with provenance.
- **A field-layout table, or a read-only `descrever_missao(resultado)`**, for every displayed field. Conditions and objectives are shown raw only, and TestFinDeMission is not evaluated.
- **Briefing.** MissionLoad does not read `WORLD/MONDE01.TXT`, and the routine that selects or displays it has not been traced. Until it is, the app shows the raw CP1252→UTF-8 CD text with its SHA-256, labeled as source text.

The resumed Codex round refines this proposal in [M1_SNAPSHOT_CONTRACT.md](../pesquisas-paralelas/missoes/M1_SNAPSHOT_CONTRACT.md): identity/source revision, acceptance gates, exact block layouts/aliasing and per-range inherited-versus-loaded provenance. It includes the whole static image and a closed declared-allocation registry so unnamed AI/runtime bytes are not dropped. It remains a planned interface; no accepted M1 snapshot or running mission is claimed.

## Stage 11 readiness: original structure traversal

The new human authorization of 2026-10-28 supersedes the historical Stage8 STOP. The existing worktree and Stages9/10 were preserved and fast-forwarded to the coordinator's inspected main `8810b3730a0fb788af3eac2b447dea65372f597f`. Core Stage14 already resolves MONDE01 unit15; the earlier Stage8 dependency descriptions remain historical evidence, not a current blocker.

[Readiness and capture plan](../pesquisas-paralelas/missoes/STAGE11_READINESS.md) and [static original inventory](../pesquisas-paralelas/missoes/evidencias/terreno-estruturas-missao-inventario.json) cover `MissionPlaceTerrain 0x46c16d..0x46c1b8`, `BatimentExiste 0x41a735..0x41a75c`, and shared epilogue `0x46b6f5..0x46b6f8`. The loop visits1000 indices in ascending order: existence lowAL → actual placement → habitation lowAL → conditional habitation effects → actual map modification(index,1). The predicate reads state byte+5; the final map call applies to every existing structure.

This is light original-byte/contract work only. No native observations, heavy checks or reconstructed traversal have been added yet. Core15 main `b610bfad77ffadaa0ee5f6af02160d786ccfdc7b` is now merged and its [reset/minimap contract](core/RESET_MINIMAP.md) audited. The prepared capture harness composes committed native harnesses and preserves all state/aliases; it has not executed. Await the coordinator's heavy grant before original whole-state capture, caller translation and the required Missions integration helper. Original-only observations precede translation; prior captures/manifests remain unchanged. Whole MissionLoad, natural remap completion, Core experience retrieval, production adoption of AI reset, objectives/events and real runtime remain separate dependencies.

The coordinator also approved four tiny original-only `MissionGetNum 0x46c11a` observations inside this same Stage11 to unblock the M1 identity query. Its [exact bytes](../pesquisas-paralelas/missoes/evidencias/mission-get-num-inventario.json) read only byte `0x496fe4`, clear AH, retain highEAX16 and return. Planned API `consultas_missao.numero_missao(missao_u8)` reads an explicit live one-byte buffer/view and returns semantic AX0..255, with no neighbor read, replacement state or literal mission default. No query translation exists yet; AI/runtime retains its named dependency until original-backed integration.

The first [original-only Stage11 capture](../pesquisas-paralelas/missoes/evidencias/captura-terreno-estruturas-missao-original.json) now completes the approved eight scans plus four query observations, before either Python translation. Capture SHA-256:`52232213ef3585a8523a04d24d5bcc9d472c90ff137769fb0cea48f9a41b777e`, source `24ca5a794ff4c6979a8f5ed7c23621d75adcdf32`. Seven tail entries and one joined entry yield six returns and two exact pre-CALL stops (`0x46c1b1`, `0x41cdb9`) in56 scan segments (18 minimap/30 pixel-loop resumes, max156,130 instructions). Six full mapped-state blocks cover5,263,360 bytes per snapshot, plus ordered call/effect traces. Four separately counted getter entries confirm one-byte AX semantics and unchanged whole global image. The short heavy lease was released immediately; no Python equality, heavy domain gate, integration or full-load acceptance is claimed by these observations.

### Stage11 translation and light capture replay

The original observations were independently committed at `ed0172a364310b28584824b3e49dc63db371ed93` **before** the following source was written. Fresh native validation/integration remain pending at this checkpoint.

[consultas_missao.py](../pesquisas-paralelas/missoes/consultas_missao.py) publishes two read-only explicit-buffer queries:

- `numero_missao(missao_u8)` consumes exactly one contiguous B/b byte, accepting read-only views. It reads the actual live field on every call, returns semantic AX0..255 and never reads the adjacent byte. Native highEAX16 preservation is a CPU-register fact, outside this scalar API.
- `existe_estrutura(estruturas, indice)` consumes the actual276,000-byte pool/view, truncates the index to low16 then protects0..999, and returns AL1 iff state byte+5 is nonzero. It includes raw states1/4/5/255. No copy, constructor defaults or generic alive filter is supplied.

The coordinator resolved existence-query ownership from economy's existing Stage15 handoff: **Missions provides the single BatimentExiste implementation**, reusable by AI/economy. The temporary proposal to wait for an economic duplicate was canceled before adding either body elsewhere.

[terreno_estruturas_missao.py](../pesquisas-paralelas/missoes/terreno_estruturas_missao.py) supplies `ProvedoresTerrenoEstruturas(existe,colocar,habitada,habitar,modificar_mapa)` and `preparar_estruturas_no_terreno(provedores)`. It performs the exact live1000-slot ascending scan, consuming lowAL from both queries. For each existing structure, place first, query habitation, conditionally make habitable, then call map modification(index,1). Return completed placed/habitable index tuples and the shared original RET address `0x46b6f7`; this describes L8, not a loaded world.

`provedores_terreno_estruturas_core(world, *, habitacao=None, mascara_tipo20=None)` binds the actual Missions existence query, Core placement/minimap provider and supplied Economy habitation methods. Habitation and Core must share the identical live unit/structure pools. A missing habitation provider raises only when its query is reached, after completed placement; no successful fallback is installed. Type20 retains Core's explicit mutable20-byte mask requirement. The combined `preparar_terreno_missao(unit_providers,structure_providers)` composes unchanged Stage8 unit/capacity orchestration followed by this scan, matching the whole MissionPlaceTerrain caller. Failures retain every previous effect; entry replay is not continuation.

Missing callbacks raise `DependenciaTerrenoEstruturas` with callee, CALL site and exact arguments. Actual lower-provider errors propagate unchanged. Local checks cover lowAL poison, live post-placement queries, selective callback order, alias rejection, query widths/protection and all eight frozen observations. Every replay matches all six full mapped-state hashes and complete ordered traces; actual MONDE01's joined fixture completes8unit placements and its one sanctuary placement. Inherited grids/allocations remain explicitly synthetic, so **this does not establish whole MissionLoad or M1**.

The first memory-only replay attempt hit sandbox SIGILL during Unicorn initialization, before any original instruction. The ordinary-context replay passed; local replay now uses a pure byte-ledger backend solely for fixture serialization, with execution/resume forbidden. It hashes the same frozen memory blocks and does not model any engine operation. Nine focused tests are discovered: five light tests pass and four optional fresh-native methods are skipped. Failure/success logs remain in ignored `.local`; no capture or expected byte was altered.

```sh
python3 -B pesquisas-paralelas/missoes/validar_terreno_estruturas_missao.py
# Only after the coordinator grants the serialized validation window:
python3 -B pesquisas-paralelas/missoes/validar_terreno_estruturas_missao.py --emular
python3 -B scripts/check.py --domain missions
python3 scripts/workstream.py integrate missions
```

### Stage11 fresh validation before integration

After merging verified Core16 main `b4c5a1072a2b2e494b3a6bf374bd978fc6e67b9a` into the feature as `13619b6e36deda8cbb7f289b8404d8371e57fe96`, the first [focused native run](../pesquisas-paralelas/missoes/validacao/stage11-focused-x86.json) passes all9tests with zero skips/errors/failures/native faults. Actual new scan coverage is63entries (62structure continuations,1joined MissionPlaceTerrain):56returns and7expected pre-CALL dependencies in161segments,49minimap-entry plus49pixel-loop resumes, maximum156,130instructions per segment. Every scan compares all six mapped blocks byte for byte and the full call/physical trace; this includes the actual MONDE01 joined input.

Separately,512original BatimentExiste entries cover all256state bytes at indices0/999 with poisoned high index bits and preserved EDX;256MissionGetNum entries cover every byte with poisoned neighbors/highEAX16. All768query segments match the public APIs and preserve the entire global image. The independent8+4pretranslation captures remain unchanged and are not counted as this new differential run. The CPU-free local capture replay is separate evidence, not native execution.

The required domain command passes80tests with31declared optional native skips and valid documentation links. Logs `.local/stage11-native-attempt1.log` and `.local/stage11-domain.log` are preserved. Integration and committed-main reproduction are still pending at this source checkpoint; no whole MissionLoad, natural remap completion, objective execution or real mission is claimed. No additional stage starts before the checked helper merge and remote ancestry verification.

Stage11 is now integrated/pushed at main `7f617fab29ce382f96b690ea70da25a33fab8bae`, feature `c0f0a873c3657e72a3e478cf6fd7ea73c84dd58a`. The complete locked candidate passed all80native mission tests and the common gates; fetched ancestry of capture/implementation/feature/merge was verified. The changed9native tests reproduced on committed main with exactly the versioned focused report's results; worktree clean and heavy lease released. This supersedes the pending status at the preceding source checkpoint.

## Stage12 light preparation: original whole-load oracle

[STAGE12_ORACLE_PLAN.md](../pesquisas-paralelas/missoes/STAGE12_ORACLE_PLAN.md) records the explicit inherited memory/alias registry, committed Core16 external-boundary ABI and finite resource identity/budget plan. The new source is an **unexecuted native scaffold**, with two CPU-free registry guard tests; it supplies no default game state, player controls, file results, profile absence or allocator success. Raw inherited input closure and actual external handlers are still required. No whole-MissionLoad capture, Python load composition, new native validation or M1 acceptance has occurred.

### Stage12 result: original-only whole MissionLoad from the program start

The Stage12 oracle is now runnable ([result section](../pesquisas-paralelas/missoes/STAGE12_ORACLE_PLAN.md#stage12-result-runnable-program-start-oracle-and-original-only-missionload-capture-2026-10-28-claude)). The original new-campaign path (CRT thread data, `AppInit`/`ProgInit`, five native `CalculGame` frames driven by a declared Enter-key script) produces the inherited state; display/text/bitmap-bank startup calls are skipped and shown not to be read. The intact `MissionLoad 0x46c2cf` then ran for MONDE01 to its **real return 0x42d22d with AL=1** through declared CRT/KERNEL32 boundaries only. Live player controls at entry are (1,2,2,2) from original `InitPlayer`/`SetPlayerType`. Captures, the frozen entry state and the validation report (replay, code integrity, segmentation invariance, fill independence, classified read-before-write footprint) are committed before any translation. No Python composition or M1 acceptance exists yet.

## Stage13: whole MissionLoad composed in Python vs the original capture

The composition starts from the frozen entry snapshot and runs `MissionLoad 0x46c2cf` for MONDE01 over the integrated providers. It uses one non-overlapping memory map in which provider buffers are filled in place, plus a deterministic arena and the original call order. It then compares the result with the frozen original capture: the whole state, the allocation records, AL and the ordered binding requests. Details are in [STAGE12_ORACLE_PLAN.md — Stage13](../pesquisas-paralelas/missoes/STAGE12_ORACLE_PLAN.md#stage13-m1-composition-and-comparison-2026-10-28-claude) and the report is [stage13-m1-composition.json](../pesquisas-paralelas/missoes/validacao/stage13-m1-composition.json).

- **NOT M1.** The strict run stops at `EnginInitTechnologie 0x441459`, CALL `0x46c5af`. The cause is Economy: `PropriedadeConstrucoes.ordens` is one 10,816-byte copy, but the original keeps four separate Bag allocations behind `[0x4e19b8]`.
- **Up to the stop:**
  - all 1,400 binding requests match the original;
  - all 938 allocation records match, including the native remap pointers and the SHA-256 of freed bytes;
  - the only state differences are the 3,966 bytes that the six tails write.
- **Diagnostic bridge (not M1 evidence).** A declared copy-in/copy-out of `ordens` gets past the stop. With it, the run reaches AL=1 and the whole 2,659,375-byte final state matches byte for byte.
- **Needed:** Economy must accept the four live Bag pools by identity. After that, rerun `validar_composicao_carga_missao.py`.

## Stage14: strict whole-MissionLoad composition — M1 candidate

Economy's per-owner `[0x4e19b8]` Bag contract is now on main, and the composition requires it. No bridge remains. The strict Python `MissionLoad` for MONDE01, starting from the frozen entry snapshot, reaches **AL=1**, and the full comparison with the original capture is equal:
- 881 blocks, 2,659,375 bytes;
- 938 allocation records;
- 1,400 ordered binding requests.

Two runs are identical. The exclusions are listed in the report: 16 profile key strings that exist only on the native stack, plus native call-site and stack metadata. Details: [STAGE12_ORACLE_PLAN.md — Stage14](../pesquisas-paralelas/missoes/STAGE12_ORACLE_PLAN.md#stage14-strict-m1-composition-on-integrated-code-2026-10-28-claude) and [stage14-m1-composition-strict.json](../pesquisas-paralelas/missoes/validacao/stage14-m1-composition-strict.json). This is an M1 **candidate**. Acceptance follows integration and committed-main reproduction.

**Update:** M1 was accepted at main `927c7e5` (CXR-20261028-08).

## Stage15 (M2.1): MONDE01 first frame, original first

### Original-only capture (Deliverable 1)

[oraculo_quadro_missao.py](../pesquisas-paralelas/missoes/oraculo_quadro_missao.py) extends the accepted M1 bench; it does not rewrite it. After the original MissionLoad returns at `0x42d22d`, the intact executable runs three phases:
- **(a)** the rest of the load-state CalculGame invocation, to its RET;
- **(b)** the window-loop bytes between two frames: ProgIteration `0x475063`, `_WinMain@16` `0x460212..0x460225`, PeekMessageA, a new ProgIteration with its frame counters and GetCursorPos, up to the CalculGame entry `0x42c868`;
- **(c)** the first game-state CalculGame frame, to its real return `0x475063`.

Readable result: [QUADRO1_MONDE01.md](../pesquisas-paralelas/missoes/QUADRO1_MONDE01.md), with the per-routine entry trace in [rastro-quadro1-monde01.json](../pesquisas-paralelas/missoes/evidencias/rastro-quadro1-monde01.json). The capture is [captura-quadro1-monde01-original.json](../pesquisas-paralelas/missoes/evidencias/captura-quadro1-monde01-original.json) (SHA-256 `c06f78ea…`, source `e6aa305`, commit `ca35221`), and it was committed before any translation.

**Key facts:**
- The load-state invocation already runs one complete frame body ("frame 0"), because MenuInit(…, 0x12) passes the `0x42d3c0` gate.
- Frame 1 reaches the end-condition test but none of the AI kernels.
- No phase performs file I/O, allocates memory or reads the clock.
- RNG `0x497164` advances in (a) and (c); `0x498db4` does not change.

**Declared boundary policy:**
- Display, sound-library and MCI CD routines are not executed. Each call is recorded with its registers, stack words and guard bytes.
- Each declared stack cleanup equals the RET immediates reachable in the intact bytes, found by following shared epilogues, thunks and switch tables.

**Named inputs:** GetAsyncKeyState answers 0, PeekMessageA reports no message, the cursor is (0,0), and the caller frame is declared.

**Validation:** [m2-frame1-original-x86.json](../pesquisas-paralelas/missoes/validacao/m2-frame1-original-x86.json) passed:
- replay, code integrity and segmentation invariance;
- fills 0x5A and 0x00 are state-independent;
- boundary-EAX markers propagate 0 bytes;
- the M1 Windows inputs propagate 0 bytes;
- the cursor matters: (0,0) edge-scrolls the view in frame 1.

The footprint holds 4,932 read-before-write bytes, classified by provenance.

**Open graphics dependency:** frame 1 reads AffGame's possible stores, listed in QUADRO1_MONDE01.md.

**Bench fix with M1 impact:**
- Unicorn instruments hooks at translation time, so hooks added after startup missed reads from code translated earlier.
- The bench now flushes the translation cache after adding hooks.
- Rerunning the M1 original-only validation with the fix ([stage12-missionload-original-x86-tbflush.json](../pesquisas-paralelas/missoes/validacao/stage12-missionload-original-x86-tbflush.json)) passes again: 9,585 read-before-write bytes instead of 1,757, still with 0 skip-derived and 0 skipped-store bytes. The extra bytes are memset touches on allocation fill.

### EvenementEnCours and TestFinDeMission (Deliverable 2)

**Isolated captures (original only).** [captura-isolada-missoes-quadro1.json](../pesquisas-paralelas/missoes/evidencias/captura-isolada-missoes-quadro1.json), source `46dc93d`, records each routine at its exact frame-0 and frame-1 entry: AL, registers, changed bytes, and the bytes read before written. Both calls of each routine return AL=0 and change nothing. TestFinDeMission reads 1,031 bytes. After every isolation the paused path still reproduces the committed phase states and trace.

**API** ([fim_missao.py](../pesquisas-paralelas/missoes/fim_missao.py)):

`evento_em_curso(evenement_u8)` returns AL = byte `0x4e1b0e`.

`testar_fim_missao(jogador, condicoes, estado, contagem_inicial, exercitos, exercitos_ia, consultas)` takes these live views:

| Argument | Address | Size | Access |
|---|---|---|---|
| `condicoes` | `0x4e1d20` | 100 | read |
| `estado` | `0x4e1d84` | 14: latch +0, owner count +1, marks +4..+13 | written |
| `contagem_inicial` | `0x4e1a3a` | 2 | read |
| `exercitos` | `0x4e1928` | 8 | read |
| `exercitos_ia` | `0x4dfaa8` | 16 | read |

`ConsultasFimMissao` supplies the callees. `consultas_publicadas(estruturas, recursos, missao_u8)` binds the committed ones:

| Callee | Address | Owner |
|---|---|---|
| BatimentExiste | `0x41a735` | Missions |
| BatimentGetPlayer | `0x41a08c` | Combat |
| BatimentGetType | `0x41a4f4` | Economy |
| TestRessource | `0x4676e5` | Economy (`Economia.suficiente`) |
| MissionGetNum | `0x46c11a` | Missions |

**Mutation order**, as in the original:
1. Records 0–9 are processed in order. Each record's mark is set or cleared as its test runs.
2. The result accumulates across records.
3. The MissionGetNum==6 override runs.
4. Latch: set to 1 if the result is non-zero, then cleared and the result forced to 1 when `[0x4e1a3a]`==0.
5. When the result and the latch are both non-zero and the mission is 8 or 13, the owner count at `[0x4e1d85]` is written.

**Supported domain:**

| Record type | Test |
|---|---|
| 0, 1, 2 | resource |
| 3 | inventions |
| 4 | structure of a type in up to three influence zones (`0x00ff` = wildcard) |
| 5 | no non-allied opponent forces |
| `0xff` | blocks only when it is the first record |
| any other | ignored |

**Named dependencies** (`DependenciaFimMissao`, raised at the original CALL):

| Missing callee or state | CALL |
|---|---|
| BatimentGetCase | `0x45883f` / `0x458a44` |
| CaseGetZoneInfluence | `0x45884b` / `0x458a50` |
| RechercheGetNbInvention | `0x45879c` |
| PlayerEstAllie | `0x458903` |
| GetTopLeftCaseZoneInfluence | `0x45870e` |
| CaseEstIlluminee | `0x45871c` |
| uninitialized stack local `[esp+8]` in the mission 8/13 scan when no type-4 match stored it | `0x4589dc` |
| a structure owner ≥4 in that scan (the original writes the caller stack) | `0x458aa8` |

**MONDE01 conditions:**
- record 0 is type 4: a **type-3 CAVE structure** of the player in influence zone 0;
- records 1 and 2 require 50 food and 50 stone;
- record 9 repeats the 50-stone test;
- records 3–8 are `0xff`.

So **the objective requires building a cave**, which answers the roadmap's open question.

**Validation:**
- CPU-free ([test_fim_missao.py](../pesquisas-paralelas/missoes/testes/test_fim_missao.py)): each captured call is rebuilt from only the bytes the original read, under two poisons.
- Native differential ([m2-fim-missao-differential-x86.json](../pesquisas-paralelas/missoes/validacao/m2-fim-missao-differential-x86.json), source `b25e8d6`): of 48 native cases at both frame entries, 38 compared cases are equal in AL and every changed byte. The other 10 stop at the named dependencies above.

No whole-frame composition is built. The AI/runtime front owns the frame pipeline.

## Stage16 (M2): influence-zone queries and the register trace view

M2.1 was integrated at main `ec931d2`.

### Ownership

Every reference in the intact code to the influence table `0x50c614` (400 records × 10 bytes: x0 at +0, y0 at +2, x1 at +4, y1 at +6) lies in the cluster `0x47bf2c..0x47c138`:
- InfluenceReset;
- CaseGetZoneInfluence `0x47bf66`;
- CaseInZoneInfluence `0x47bfdd`;
- LoadCadreInfluence `0x47c04a`, the Missions loader already composed in M1;
- SaveCadreInfluence;
- GetTopLeftCaseZoneInfluence `0x47c114`.

The cluster is therefore Missions-owned. MONDE01 has a single zone: zone 0 covers cells (0,0)–(28,25).

### Original-only capture

[captura-influencia-quadro1.json](../pesquisas-paralelas/missoes/evidencias/captura-influencia-quadro1.json) was generated from source `c1bb6b2` and committed in `60f00c2`.

MONDE01 frames 0–1 never enter either query. Instead, `Isolamento` pauses at the frame-1 TestFinDeMission entry and injects native leaf calls from that exact state:

| Query | Arguments | Result |
|---|---|---|
| CaseGetZoneInfluence | all 65,536 cells | 754 cells in zone 0, all others `0xff` |
| CaseGetZoneInfluence | 256 calls with non-zero upper EAX bits | results unaffected |
| GetTopLeftCaseZoneInfluence | zones 0..399 | — |

Sampled footprints show that each call reads only zone-record words and writes nothing. Registers are preserved, and the whole state equals the paused state afterwards. The phases then continue and reproduce every committed state.

### API ([influencia_missao.py](../pesquisas-paralelas/missoes/influencia_missao.py))

Both functions take the live 4,000-byte table view.

**`zona_influencia(influencia, celula)`** reads AX only: x = AX & 0xff, y = AX >> 8. It returns the first zone 0..399 whose inclusive unsigned-16 rectangle contains the cell, skipping record 255. If no zone matches, it returns `0xff`.

**`canto_zona_influencia(influencia, zona)`** returns EAX = x0 + (y0 << 8) as a u32 including the carry, so an empty record gives `0x0100feff`. The zone index is protected to 0..399.

**Wiring.** `fim_missao.consultas_publicadas(estruturas, recursos, missao_u8, influencia)` now requires the table view and binds both queries.

### MONDE01 consequences

- **Cave condition (type 4):** it now passes the zone test. It still stops at BatimentGetCase `0x41aee2`, which is Economy's to publish.
- **Mission-6 path:** it now stops at CaseEstIlluminee `0x47693a`, which is Core's to publish.

### Validation

- **CPU-free** ([test_influencia_missao.py](../pesquisas-paralelas/missoes/testes/test_influencia_missao.py)): replaying the captured table reproduces every native EAX.
- **Native differential** ([m2-influencia-differential-x86.json](../pesquisas-paralelas/missoes/validacao/m2-influencia-differential-x86.json)): Python equals the native result on 5 tables × 66,192 calls. The tables are the captured table, overlaps with record 255 skipped and an inverted rectangle and a point, the whole map, upper-word bounds, and 400 seeded random records.
- **Re-wired `fim_missao`** ([m2-fim-missao-differential-x86-v2.json](../pesquisas-paralelas/missoes/validacao/m2-fim-missao-differential-x86-v2.json)): 38/38 compared cases are equal.

### Register trace view

[rastro-registradores-quadro1-monde01.json](../pesquisas-paralelas/missoes/evidencias/rastro-registradores-quadro1-monde01.json) was generated from source `0002794`. It lists every routine entry of the three phases in order (1,718 / 5 / 1,605), one line each in the AI/runtime format `callee@caller+off EAX EDX EBX ECX`.

The rerun's phase states equal the committed capture, and its per-routine counts equal the committed trace. The original oracle was **not** extended beyond frame 1.

## Stage17 (M2 round 3): oracle with the display path executed

Stage16 was integrated at main `67fb81f`. Graphics' report [ESCRITAS_AFFGAME_ENTRE_QUADROS.md](../pesquisas-paralelas/graficos-animacao/ESCRITAS_AFFGAME_ENTRE_QUADROS.md) motivated executing the display path. Full summary: [QUADRO1_EXIBICAO.md](../pesquisas-paralelas/missoes/QUADRO1_EXIBICAO.md).

**Scenario.** The new scenario `exibicao` ([oraculo_exibicao_missao.py](../pesquisas-paralelas/missoes/oraculo_exibicao_missao.py), [cenarios_oraculo.py](../pesquisas-paralelas/missoes/cenarios_oraculo.py)) runs AppInit and then the real `_WinMain@16` loop up to the original `CALL MissionLoad`. Along the way it executes:
- AffInit/DDInit, LoadPalette and the bank loaders;
- RestoreAll, DDFlipPage, and menu and game AffGame.

The declared interim DirectDraw backend (`exibicao_declarada.py` (retired in Stage18; source at commit `3ff4b21`)) stands in for Graphics' backend until it lands.

**Remaining boundaries:**
- Text needs CRT `fgets` `0x48ce96` and LoadPie needs CRT `fseek` `0x48cda2`, which Core has not inventoried.
- Video and credits.
- Audio.

**Scenario switch.** The M1 and frame capture and validation scripts take `--cenario`, and v1 behavior is unchanged. The composition validator takes `--entrada`/`--captura`. Display M1 captures are delta-encoded against their entry artifact (`mapa_memoria_m1.expandir_captura`).

**Evidence.** The new entry snapshot, the whole MissionLoad capture (AL=1, the same 1,400 binding requests as v1) and the frames 0/1 capture with its trace were all committed before any translation. v1, v2, Stage14 and the frame-1 v1 evidence are untouched.

**Checks (all passed):**
- **Stage14 strict composition regression:** whole state equal over 25,343 blocks and 25,482 records.
- **MissionLoad validation:** replay, integrity, segmentation, fill, markers, inputs and the flushed footprint.
- **Frame validation:** the same checks, plus display-input sensitivity.

**Logic-state comparison with v1.** The comparison ([m2r3-frame1-v1-vs-exibicao.json](../pesquisas-paralelas/missoes/validacao/m2r3-frame1-v1-vs-exibicao.json)) has native writer attribution ([m2r3-v1-vs-exibicao-writers.json](../pesquisas-paralelas/missoes/validacao/m2r3-v1-vs-exibicao-writers.json)). No unit, structure, player, resource, AI, condition or market byte differs, and RNG `0x497164` is equal throughout.

Three real logic differences come from display **initialization**:
- the CRT rand seed, because NextAnimTerrain now calls LongRand 425 times per frame over the 25×17 viewport DDInit sets;
- the permutation cursor `0x4e1d18`, advanced by NextAnimVeget;
- the view origin, because MouseInit centres the cursor variables on the real screen and frame 0 no longer edge-scrolls.

AffGame between frames writes only display state for frame 1.

## Stage18 (M2 round 4): frozen display reference and comparison policy

Stage17 is integrated at main `81e0a26`. The display scenario is the M2 reference; v1 is historical evidence. Full write-up: [POLITICA_COMPARACAO_M2_1.md](../pesquisas-paralelas/missoes/POLITICA_COMPARACAO_M2_1.md).

**Backend.** Graphics' declared backend `fronteiras_exibicao.ExibicaoDeclarada` (d8b1af9) replaces the retired interim `exibicao_declarada`. It is installed after the bench's own imports, and its surfaces live at `0x60000000`.

**New reference artifacts** (`*-exibicao-v2.json`, all original-only and committed before any translation): the entry snapshot, the MissionLoad capture (from `af1ccbe`) and the frames 0/1 capture with its trace (from `ac6b5f3`).

**Equivalence with Stage17** ([report](../pesquisas-paralelas/missoes/validacao/m2-exibicao-v2-vs-interino.json)). The v2 artifacts are not byte-for-byte equal to the Stage17 ones. In every state the same 10 DGROUP bytes differ: the program stores four backend object pointers (`0x4e1788`, `0x4e178c`, `0x4e1790`, `0x4e179c`) and the offscreen pixel pointer (`0x508f70`), and each backend chooses different addresses. Everything else is identical.

**Checks on v2, all passed:**
- the Stage14 strict composition regression, whole state equal;
- the MissionLoad and frame original-only validations.

**Comparison policy** ([m2-politica-comparacao-quadro1.json](../pesquisas-paralelas/missoes/validacao/m2-politica-comparacao-quadro1.json)). The policy assigns every one of the 78,869 bytes that change in (a)–(c) to its native writers and readers, then classifies it by call context:
- **Masked, 78,093 display-only bytes:** 19 DGROUP bytes and 78 terrain-cache/palette blocks.
- **Surfaces:** proven untouched by logic.
- **Compared, 776 game-logic bytes:** these include `0x4e1d18`, the CRT rand seed and the view origin.

**Open points:**
- The record lifecycle of the 146 menu banks freed in (a) is an open coordinator decision.
- Text (`fgets`) and LoadPie (`fseek`) stay boundaries until Core inventories those CRT entries.

## Stage19 (M2 round 5): N-frame tooling, M2.2 plan, v3 preparation

Stage18 is integrated at main `d94a59e`. The `-v2` reference stays fixed, nothing beyond frame 1 is committed as evidence, and MissionLoad was not recaptured. Plan and findings: [PLANO_M2_2.md](../pesquisas-paralelas/missoes/PLANO_M2_2.md).

**N-frame oracle.** `BancadaExibicaoOriginal.executar_quadros(n)` runs load_tail and then `between_frames{k}`/`frame{k}`. Frame 1 keeps its committed phase names.

**N-frame policy.** [politica_comparacao_quadros.py](../pesquisas-paralelas/missoes/politica_comparacao_quadros.py) makes two native passes. The rule is unchanged: a byte is masked only when every writer and every reader is display. It produces masks per frame window and a cumulative mask.
- With N=1 it reproduces the committed M2.1 policy exactly.
- An N=3 trial (in `.local/`) passed. It found the first **mixed byte**, `0x4e05a2`, written by AffGame and by CalculMatiere and compared from frame 2 on.

**Static timeline for MONDE01:**

| Event | Frame(s) | Notes |
|---|---|---|
| Field sweep starts | 0 | the load-state frame resets the counter, and SetUpdateChamp runs at counter 0 |
| Candidate field rows | 31–51 | |
| First field event | 45 | confirmed by the probe |
| Second sweep reaches candidate rows | 287–307 | |
| First monster raid | **9000** | AvanceMonstre entry record 0 |
| Second monster raid | **10800** | entry record 1 |

The attack table is empty and the AI players are inactive, so there is no other scripted attack.

**Proposed sequence:**
- **M2.2:** 128 frames with checkpoints at frames 1, 31–32, 50–52, 64, 100–101 and 128.
- **M2.3a:** up to frame 8,999, with per-frame hashes and full checkpoints.
- **M2.3b:** frames 9,000–9,100 and frame 10,800.

**New owner decisions:**
- **Core:** CRT `ftell` `0x48cf11`. Text needs it through FileSize.
- **Audio and coordinator:** the CD-availability input. While no CD track plays, CalculGame advances the shared cursor `0x4e1d18` every frame.
- **Audio:** sound-library state.

**v3 preparation (not committed as reference).** The CRT `fseek`/`fgets` fixtures and the `exibicao_v3` scenario run LoadPie natively, with explicit budgets of 3M segments and 1M bindings (the Core bench cap).

## Stage20 (M2.2): 128-frame original capture and comparison policy

The M2.2 reference extends the frozen `-v2` display scenario from frame 1 to frame 128, original only.

- **Capture:** [captura-quadros128-monde01-exibicao-v2.json.xz](../pesquisas-paralelas/missoes/evidencias/captura-quadros128-monde01-exibicao-v2.json.xz), with its [manifest](../pesquisas-paralelas/missoes/evidencias/captura-quadros128-monde01-exibicao-v2.manifest.json). It has 257 phases in delta form, a state summary in every phase and full states at frames 1, 31, 32, 45, 50–52, 64, 100, 101 and 128. The raw JSON SHA-256 is pinned in the manifest.
- **Policy:** [m2-2-politica-comparacao-128-quadros.json](../pesquisas-paralelas/missoes/validacao/m2-2-politica-comparacao-128-quadros.json). Its cumulative mask has 153,060 display-only bytes; 999 logic bytes are compared. Only the cumulative mask may exclude bytes from a whole-run comparison.
- **Declared inputs and decisions:**
  - No CD track plays: `[0x4e2f28] = 0` is checked in every phase.
  - The HUD flag `0x4e05a2` is compared.
  - The 146 freed MenuInit bank records are compared.
- **Checks:**
  - The first three phases equal the M2.1 frame-1 capture.
  - Replaying s0 plus the deltas reproduces every summary and checkpoint.
  - Two full runs are identical apart from wall-clock fields.

**Segment-parallel execution** ([segmentos_quadros_missao.py](../pesquisas-paralelas/missoes/segmentos_quadros_missao.py)) restores exact snapshots (memory, CPU context, bench state) in fresh benches. On M2.2, its segmented capture records and its segmented policy both equal the sequential results byte for byte. It is the planned tool for M2.3a.

Details: [missions handoff](../pesquisas-paralelas/missoes/HANDOFF.md), Stage20.

## Stage21 (M2.3): 9,200-frame original capture and long-run comparison policy

M2.3 extends the frozen `-v2` display reference to frame 9,200, original only, with the same declared inputs and decisions as M2.2.

- **Capture:** 10 xz parts in [evidencias/m2-3/](../pesquisas-paralelas/missoes/evidencias/m2-3/), 93,012,400 bytes in all, with a manifest that pins each part's raw and compressed SHA-256. There are 18,401 phases in complete delta form. Every part opens with a full state, and full states also follow frames 8999, 9000 and 9176.
- **Per-phase hashes:** `summary` covers the full state. `compared_summary` covers the state with the cumulative mask zeroed. `masked_sha256` covers only the masked bytes. The manifest defines all three.
- **Policy:** [m2-3-politica-comparacao-9200-quadros.json](../pesquisas-paralelas/missoes/validacao/m2-3-politica-comparacao-9200-quadros.json). 154,620 bytes change. The cumulative mask has 153,060 display-only bytes, and 1,560 logic bytes are compared: the 999 of M2.2 plus 561 later ones, 413 of them in the first raid window from frame 9,000.
- **Checks:**
  - Every phase state is reproduced.
  - The written parts replay to every summary, compared summary, masked hash and full state.
  - The first 128 frames equal the M2.2 capture.

Details: [missions handoff](../pesquisas-paralelas/missoes/HANDOFF.md), Stage21.

## Stage22 (M3): scripted-input harness, S1 victory, D1 defeat and window captures

M3 drives the intact executable with a scripted input file from the M2.2 frame-128 state, original only.

- **Harness:** [entrada_roteirizada.py](../pesquisas-paralelas/missoes/m3/entrada_roteirizada.py) answers `GetCursorPos`, `PeekMessageA` and `GetAsyncKeyState` per frame from the input file and dispatches messages to WndProc 0x4181a1 natively.
- **Probes:** P1–P7 and K1 settle selection, moves, the CAVE build, food and stone orders, cave lodging, the depot route and the keys. Each is replay-checked on two runs.
- **S1, victory:** frames 129–17050. AL = 1 at 16933. The result screen opens at 17032, and a click confirms it into `MissionNext` at 17043.
- **D1, defeat:** frames 129–15700. The unit count reaches 0 at 15555. `PartieGetResultat` returns 0 at 15655 and the failure branch runs. The only defeat trigger is `TestFinDeMission` with unit count 0.
- **Window captures:** pass-2 whole-state captures with comparison policies for P1, P2, P6 and the whole S1 window. All four pass; S1 has 33,844 phases and 654,586 logic bytes, most of them from the next screen's bank load at 17043.
- **Checks:** two independent runs from F0 give equal records for every probe, for S1 and for D1. Each window's written parts replay to every phase state.
- **Pending:** Combat's fatal-window captures over S1 and D1 (cancelled before starting).

Details: [SONDAS_M3.md](../pesquisas-paralelas/missoes/m3/SONDAS_M3.md) and the [missions handoff](../pesquisas-paralelas/missoes/HANDOFF.md), Stage22.
