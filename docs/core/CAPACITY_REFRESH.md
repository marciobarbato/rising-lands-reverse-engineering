# Existing-unit Bag-capacity refresh

`atualizar_capacidades_unidades(mundo, jogador, *, capacidade_tipo=None, modificador=None)` in [capacidades_unidades.py](../../ferramentas/capacidades_unidades.py) translates complete `EnginResetCapacite` at `0x4475ef..0x447676` with shared epilogue `0x440d55..0x440d5e` (end exclusive). `MundoUnidades` exposes the same method. The [evidence manifest](../../evidencias/capacidades-unidades/manifesto.json) records code hashes/bytes from original executable SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

This closes the world-unit refresh dependency requested by economy's `BonusSetEngin` selector-1 setter. Core owns scanning and modifying live units; economy owns the bonus table, setters, and the query providers. This API does not perform the setter's earlier table writes or claim the whole setter is integrated.

## Exact interface, order and effects

`mundo.unidades` is a writable `bytearray` of exactly 220,800 bytes: 800 records, stride 276, addressed by the original global pointer at `0x4e19a0`. A wrong buffer type/length raises `ValueError` before callbacks or mutation. Integer `jogador` truncates to its low byte, matching original AL. The function returns `None`; it does not expose incidental final x86 registers.

The original and Python implementations visit indices 0–799 in ascending order. For each record:

1. Read u8 state `+02`; skip exactly states 0 and 4. Every other byte value is eligible for the next test.
2. Compare u8 owner `+00` to the saved input owner. Skip mismatches.
3. Read u8 type `+01`, then query `capacidade_tipo(type)` (`EnginTypeGetCapacite`, original call `0x44762a`).
4. Query `modificador(owner, type, 1)` (`BonusGetValEngin`, original call `0x44763a`).
5. Write the sum's low u16 at unit `+0c`, the Bag capacity word. Only after this store does the scan proceed.

Read-only query results are consumed as u16 capacity and u8 selector-1 bonus; the final sum wraps to u16. The routine calls the bonus query even for owners 4 and 200, whose native query returns zero. This differs from the local conversion adapter's provider-level callback bypass and must not be silently substituted.

Bag count at `+0a`, contents, tags, other unit fields, navigation search, structures, terrain, occupancy and resource balances are unchanged. No count clamp or item removal occurs when the new capacity is below the existing count. The original does not inspect whether that Bag is otherwise internally valid.

The actual committed economy providers are `bonus_unidades.capacidade_tipo` and `BonusUnidades(loaded_1872_bytes).consultar`. Capacity supports every u8 type. Bonus-table lookups support ordinary owners 0–3 and types 0–25, with owner-4/200 bypass before lookup/type validation. Therefore all raw u8 types also work for matching neutral owners. Unknown ordinary table indices remain outside the exact provider's protected lookup domain; an error from that provider propagates at the query, after any earlier scan stores.

## Missing providers and partial failure

No query provider is needed when the scan finds no eligible matching unit. At a matching unit, a missing capacity callback raises `NotImplementedError` before the capacity query; a missing modifier raises it after capacity resolves and before the bonus query. Exceptions from either supplied query propagate. Queries must not mutate or resize shared world/bonus state; mutating or reentrant query callbacks are unsupported.

No rollback or speculative whole-pool validation occurs. All earlier matching unit capacity writes survive; the failing unit's capacity and all later units remain unchanged. This matters when the caller has already changed the bonus table. Retrying a whole mutating caller is not automatically safe; callers must preserve their original continuation semantics.

An economy-owned caller can wire the callback without copying state:

```python
def refresh(owner):
    mundo.atualizar_capacidades_unidades(
        owner, capacidade_tipo=capacidade_tipo,
        modificador=bonus.consultar)
```

The same `mundo.unidades` must be the caller's live pool, and `bonus` must expose the table after the setter's prior writes. This stage provides no ownership transfer or unit allocator.

## Actual validation

```sh
python3 -B ferramentas/extrair_capacidades_unidades.py
python3 -B ferramentas/validar_capacidades_unidades.py --emular
python3 -B ferramentas/validar_capacidades_unidades.py
python3 -B scripts/check.py --domain core
```

The [new native report](../../relatorios/capacidades-unidades-emulada.json) passes 10 tests and 284 bounded x86 executions: 278 complete 800-slot scans and six conditional pre-query checkpoints at indices 0/7/799. Of those six, three stop at capacity call `0x44762a`, three at bonus call `0x44763a`; the Python side deliberately raises six `NotImplementedError`s. There are no native exceptions, instruction/time limits, skips, failures or errors. Native subcalls are unpatched: 5,016 capacity queries and 5,013 bonus queries execute inside those bounded calls, not as additional top-level execution counts.

Comparisons cover whole 220,800-byte unit pools, unchanged bonus-table bytes, exact query order, all 256 state bytes, six owner filters, all 256 input-owner low bytes, all 256 raw unit types for neutral owners, poisoned Bags, the last slot, and partial writes when later queries stop. Python comparisons use the actual committed economy capacity/bonus providers.

The [local report](../../relatorios/capacidades-unidades-local.json) discovers 10 tests, executes six Python tests, explicitly skips four optional-x86 tests and executes zero x86. The owning core check passes 270 discovered tests with 130 optional-x86 skips. No historical x86 aggregate is rerun. The global gap closed is the original live-world capacity callback for a bonus-table mutation, independently validated before integration. Full bonus setters/loading, production continuation, navigation/death callbacks, and real-mission runtime operation remain separate.
