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
