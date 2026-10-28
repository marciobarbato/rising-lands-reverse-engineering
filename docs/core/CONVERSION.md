# Shared-world existing-unit conversion

This stage joins the committed combat-owned local `EnginSetType` provider to core's live unit pool and navigation-search state. It also resumes economy's prepared handoff through the two original calls at `0x420f5a..0x420f6e`: `CalculPosition`, live building type reload, then `EnginSetType`. It stops before healing and does not establish complete production or world occupancy.

Implementation: [conversao_unidades.py](../../ferramentas/conversao_unidades.py). Original executable SHA-256: `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`. The [new manifest](../../evidencias/conversao-saida/manifesto.json) records caller and modifier-order intervals and references existing committed combat evidence for `EnginSetType` (`0x457b87..0x457e0c`), `EnginSetTypeCaract` (`0x457350..0x457b87`), `EnginTypeGetCapacite` (`0x4475ac`), and original SBL symbol `BonusGetValEngin` (`0x428cc0`, established implementation alias `Modificateur`). End addresses are exclusive.

## Public API and supported inputs

```python
converter_unidade(mundo, indice, celula, direcao, tipo, tipos_unidades,
                 *, capacidade_tipo=None, modificador=None)

retomar_conversao_saida(mundo, pedido, tipos_unidades,
                       *, capacidade_tipo=None, modificador=None,
                       dimensoes=None)
```

`mundo` is a core world exposing a writable 800 × 276-byte `bytearray` at `.unidades`, the live `.busca` object, and `_liberar_busca(indice)`. For the resumed caller it also exposes the 1,000-record `.estruturas` pool. `MundoUnidades` provides a direct `converter_unidade` method. Integer unit index and cell truncate to u16; direction and type truncate to u8. Supported index/type ranges are 0–799 and 0–25. The preloaded type table has exactly 1,300 bytes (26 × 50). Fields read are u16 vision `+2a`, squared range `+2c`, and recharge `+30`; the underlying original provider consumes their low bytes here. No INI parsing or extra squaring occurs.

The direct conversion returns `None`. Its read-only queries are `capacidade_tipo(tipo) -> u16` and `modificador(owner, tipo, selector) -> u8`, with selectors 1 and 12. Query results are narrowed to those widths. Capacity is always queried; selector 12 is queried only for type 4; owner bytes 4 and 200 bypass both modifier queries. The committed economy module `bonus_unidades.py` supplies both providers: `capacidade_tipo` and `BonusUnidades(loaded_1872_bytes).consultar`. Core implements neither query. That bonus provider supports owner lookups 0–3 plus the neutral bypasses; other owners can raise at the query point after prior conversion mutations, and adjacent-table native memory is not modeled.

The source provider is imported from the committed combat folder of this same checkout with a scoped import path. An already loaded same-named provider/dependency from another snapshot or checkout is rejected with `ImportError`, before unit mutations. There is no import from another worker's live worktree and no copy of the combat implementation.

The resumed caller accepts economy's `PreparacaoSaidaTropa` or an equivalent object exposing `indice`, `direcao`, `unidade`, and `endereco_dependencia == 0x420698`. It calculates the cell first, then reloads u8 `mundo.estruturas[indice*276+0x7b]`; it deliberately ignores `pedido.tipo_unidade`, which is only an earlier diagnostic snapshot. It performs conversion of that existing unit and returns frozen `ConversaoSaidaTropa(indice, unidade, celula, tipo_unidade, endereco_dependencia=0x420f6e)`. Its `dimensoes` argument has the [position query's contract](EXIT_POSITION.md).

## Live mutations, ordering, and failures

Conversion passes a writable 276-byte `memoryview` into the shared unit pool. A temporary bytearray followed by writeback would discard partial changes if a query raises, so that pattern is intentionally avoided. All unlisted fields remain the committed provider's responsibility; the core adapter does not normalize them.

The original order, as reused here, is:

1. Write current/step/destination cells at u16 `+08`, `+7c`, `+7e`, then release the matching navigation search.
2. Reset the local movement/animation/selection fields, set direction, and write the new type. Change existing state to 7 only when prior state was neither 0 nor 4; then attempt the same search release again.
3. Set local supplies/fatigue fields and low-byte vision/range, then execute the committed type-characterization body. Type 4 queries bonus selector 12 before writing its final frame and modifier-dependent direction byte.
4. Query native type capacity, then bonus selector 1 for ordinary owners. Only after these queries return, clear the embedded unit Bag and store its u16 capacity sum.

The search bridge calls core's `_liberar_busca` directly. It clears only the matching unit reference, occupied/success bytes and route pointer; `busca.concluida` survives, as it does in the original. No copied `BuscaAtaque` is written back later.

Missing query providers raise `NotImplementedError` at the matching point, and exceptions from supplied queries propagate. All earlier unit/search mutations remain visible, while later Bag clearing does not occur. Query providers must be read-only with respect to shared records, tables, and search state; mutating/reentrant providers are outside this adapter's domain. Protected invalid index/type/pool/type-table inputs raise `ValueError` before conversion mutation. A wrong pending address is also rejected before positioning. None of these errors authorizes rerunning the economic prefix or retrying a partially converted unit.

The type-4 exceptional path uses the combat-owned correction discovered during this stage: native call `0x457845` precedes frame store `0x45784c`, whereas the earlier provider stored that frame before invoking its callback. The first new differential run exposed exactly that byte discrepancy at the native query boundary. The owner fixed it in implementation `fbb5c7067b67f8a70190b0c5d7adebd119a61ceb`, integrated at main `aee255d6669285e77f8b528c34836c6500bba6f4`. Core merged that committed revision and reran the failing cases successfully. The economic query providers were also consumed from integrated main `7325cd0a3cb54d80d10a0c62c7d61bd25b0f8c49`.

This stage does not remove an old physical reservation, add a new reservation, update terrain/regions/colors, handle unit death, heal, issue movement, change economic balances, reset building progress, or send a production-complete message. Those are separate original caller effects. Life and attack phase `+8a` survive; wait byte `+8b` is cleared by the original local provider.

## Reproduction and validation status

```sh
python3 -B ferramentas/extrair_conversao_saida.py
python3 -B ferramentas/validar_conversao_saida.py --emular
python3 -B ferramentas/validar_conversao_saida.py
python3 -B ferramentas/demonstrar_saida_tropa.py
python3 -B scripts/check.py --domain core
```

The benchmark executes full original bodies and their internal capacity/bonus calls without replacing them. It compares entire 220,800-byte unit pools, 276,000-byte structure pools, and all five modeled navigation-search fields. Original caller tests execute both real native calls and stop at `0x420f6e`; missing Python queries are compared to deliberate native pre-query stops, not to native exceptions.

The first x86 attempt ran 11 tests and 1,985 calls, with one failure at the type-4 selector-12 boundary. This was an identified provider-order defect, not a passing validation result. After consuming its committed fix and the economy providers, the [final report](../../relatorios/conversao-saida-emulada.json) passes 12 tests and 1,986 native executions: 832 complete conversion returns, 1,144 original caller checkpoints before healing, four native capacity stops, four selector-1 stops, and two selector-12 stops. The ten pre-query cases deliberately raise Python `NotImplementedError`; none is a native exception. Native exceptions, instruction/time limits, failures, errors and skips are zero. Successful paths use actual committed economy query providers against the original unpatched x86 calls. No historical aggregate was rerun.

The [local report](../../relatorios/conversao-saida-local.json) discovers 12 tests, executes eight Python/integration tests and explicitly skips four optional x86 tests. It executes zero x86. The core check passes 260 discovered tests with 126 optional-x86 skips. These figures refer to this stage's final runs, separately from the earlier failing attempt and earlier stages.

The [shared-buffer demonstration](../../relatorios/saida-tropa-compartilhada-python.json) runs committed economic preparation, capacity/bonus queries, and core conversion on identical underlying unit/structure buffers, using an explicitly synthetic loaded zero bonus table. It removes an existing colonist/cargo, credits stone before food, converts that colonist, releases the navigation search, and leaves healing/occupancy/production cleanup pending. It executes zero x86 and is not a loaded-mission runtime test. The global gap addressed is a composed shared-state connection between already bounded economy/core/combat routines, with the remaining production and real-mission dispatch gaps still explicit.
