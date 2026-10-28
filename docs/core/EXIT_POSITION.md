# Building exit-position query

`calcular_posicao_saida(mundo, indice, direcao=0, dimensoes=None)` in [posicao_saida.py](../../ferramentas/posicao_saida.py) translates the complete original `CalculPosition` body at `0x420698..0x420ba5`, including shared epilogues at `0x41dbe5..0x41dbed` and `0x41db1e..0x41db24` (end exclusive). `MundoUnidades` and descendants expose an adapter. The free function also accepts another world object exposing the same structure-buffer layout; it imports no economy implementation.

Original executable SHA-256 is `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`. The [evidence manifest](../../evidencias/posicao-saida/manifesto.json) records hashes and bytes for all three code intervals, the 11 jump tables at `0x4202d0..0x420698`, and the 22 initial geometry pairs at `0x495d8c + type*52`. The [original-only captures](../../evidencias/posicao-saida/captura-original.json) were generated before the Python translation and retain complete input-record bytes, AX results, and whole-pool output hashes.

## Exact supported interface

`mundo.estruturas` has exactly 276,000 bytes, interpreted as 1,000 records with stride 276. Integer `indice` truncates to u16 (original AX) and must be 0–999. The query reads u8 type at `+08` and u16 origin at `+02`. Supported types are 0–21. Invalid pool length, out-of-domain index, type ≥22, or an override with a length other than two raises `ValueError`, without mutation. Original types ≥22 take the zero-return dispatch only after reading outside the declared geometry table; those adjacent-memory reads are outside this protected API.

Integer `direcao` accepts the original u8 BL width but is unused in the result. At entry the original saves EBX, then overwrites it at `0x4206ba`; no later instruction reads the saved argument except to restore EBX. All 256 values were compared independently for all 22 supported types. A caller must not interpret the parameter name as proof of directional exit selection.

By default, dimensions are the original initial width/height pairs already published in `pegadas_estruturas.py`. An optional two-integer `dimensoes=(width,height)` supplies the current runtime words for this query; both truncate to u16. This supports mutated runtime geometry without silently assuming initial geometry remains live. The full geometry table is not mutated by the API.

The returned integer is the low 16 bits AX consumed by the original caller, not a model of the full scratch EAX register. No callback executes. The original body writes only its private stack; structures, units, terrain, occupancy, regions, flags, resources, tasks and RNG are unchanged. No origin or result is clipped to playable-map dimensions, and no collision/buildability test is performed.

## Dispatch arithmetic

For the types with an arithmetic branch, the result is:

```text
(origin + ((height - dy) << 8) + width - dx - correction + addback) modulo 65536
```

The original performs 32-bit intermediate arithmetic and eventually exposes only AX. The expression preserves that low word even when dimensions underflow or overflow. The code's `AJUSTES` tuple publishes each dispatch's `dx`, `dy`, immediate correction, and addback; these are derived from the original main and subordinate jump tables, rather than selected by visual appearance.

With the original initial geometry, the observed offsets are:

| Type | Result relative to u16 origin |
|---|---|
| 0 | +257 |
| 1, 2 | +771 |
| 3, 4, 10, 11, 19, 21 | +513 |
| 5 | +1285 |
| 6 | +772 |
| 7, 13, 16 | +770 |
| 8 | +256 |
| 9, 12, 17 | literal cell 0, regardless of origin/dimensions |
| 14 | +0 |
| 15, 20 | +1026 |
| 18 | +515 |

## Caller integration and next dependency

Economy's committed `PreparacaoSaidaTropa` is a pending handoff after colonist and cargo removal. Its `indice` and `direcao` can be passed to this function using the shared structure buffer. The returned cell is available for the next original call to `EnginSetType` at `0x420f69`. The original reloads the building's requested unit type from u8 `+7b` after `CalculPosition` returns. This positioning implementation has no callbacks or mutations, but a future composed adapter must preserve that order instead of substituting a stale diagnostic snapshot.

This stage closes the position-query dependency only. It neither consumes/retries the economic prefix nor converts the existing colonist, reserves occupancy, heals, resets fatigue, issues movement, updates vision/minimap, or proves a unit was produced. `EnginSetType` and the remaining production continuation are the next core investigation.

## Actual validation

```sh
python3 -B ferramentas/extrair_posicao_saida.py
python3 -B ferramentas/capturar_posicao_saida.py
python3 -B ferramentas/validar_posicao_saida.py --emular
python3 -B ferramentas/validar_posicao_saida.py
python3 -B scripts/check.py --domain core
```

The original-only capture executes 22 complete x86 calls, one per type. The [differential report](../../relatorios/posicao-saida-emulada.json) records 10 tests and 7,546 additional bounded complete x86 calls: 5,632 direction/type combinations, 1,518 modified-dimension cases, 308 origin/index-width cases, and 88 poisoned-record cases. All return normally to the benchmark sentinel. There are zero dependency stops, expected exceptions, instruction/time limits, failures, errors or skips. Whole structure pools remain unchanged. The dimension cases include zero, `ffff`, 16-bit sign boundaries, underflow and deterministic random values.

The [local report](../../relatorios/posicao-saida-local.json) has 10 discovered tests: six executed Python/capture tests and four explicitly skipped optional-x86 tests, with zero x86 calls. The core check passed 248 discovered tests with 122 optional-x86 skips. These are this stage's runs, not a rerun or aggregation of historical differential totals. No real mission or original game runtime was executed.
