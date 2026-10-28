# Economy research contract

Owner: economy. All implementations, tests, original-byte evidence, and validation reports live in `pesquisas-paralelas/economia/`. The API retains Portuguese identifiers and original French symbol names. Player-facing resource names stay PT-BR.

## Resource layout and arithmetic

`LoadGameRessource` (`0x46AB21`) and `SauveRessource` (`0x46AB33`) read/write the same 128 bytes without conversion. Base address is `0x4E2EA8`, with four players, four resource records per player, and eight bytes per record:

```text
address = 0x4E2EA8 + player * 32 + resource_id * 8
```

| Record offset | Type | Verified role |
|---|---|---|
| `+0` | u16 | RMI portion read, assigned, and debited by original routines |
| `+2` | u16 | Total returned by `GetRessource`; receives credits/debits |
| `+4` | u16 | Presentation value converted through `IntToBCD`/`BCDToInt` |
| `+6` | u8 | Digit bits used by `CalculMatiere` animation |
| `+7` | u8 | Preserved; economic meaning unconfirmed |

Mutation IDs are 0=`Peças`, 1=`Comida`, 2=`Pedra`. AI query order differs: food/stone/parts. The fourth record exists and is traversed by `CalculMatiere`, but high-level queries return zero in their fourth output instead of exposing that record's balance. Do not assign it a speculative resource name.

Preserve u16 wrapping, signed32 interpretation, original division, x87 rounding, exact debit/credit order, and partial mutations before exceptions. A resource credit is not production; a debit is not a complete purchase authorization. Costs are separate queries tied to the recovered unit/building tables.

## Modules and world boundaries

| Module | Confirmed responsibilities |
|---|---|
| `economia.py` | Resource queries, mutations, balances, unit/building costs, AI cost order |
| `construcoes.py` | Capacity, deposits, excess bags, withdrawals, indicator recalculation, warehouse initialization |
| `proprietarios.py` | Incremental ownership/neutralization effects, warehouse/library/heliport state |
| `extracao.py` | 15 mine, bag/field collection, and resource-regeneration routines |
| `recrutamento.py` | Recruitment initiation, eligibility/query/progress, explicit exit dependency |
| `producao.py` | Unit/spell production increments, colonist counts, original x87 rounding |
| `aprendizagem.py` | Library option tables/lists, costs, learning initiation, completion |
| `mercado.py` | Totals, global prices, directional sympathy/alliance, proposal evaluation |
| `transferencias_mercado.py` | `VideMatiere` transfer arithmetic and ordered side effects |

Deposit capacity and excess generation do not imply completed unit transport. `BatimentEnleveMatiere` and `BatimentCalculResource` preserve debit/recalculation order, including division-by-zero after earlier mutations. `BatimentInitCave` reconstructs per-type counts and warehouse numbers without redefining per-warehouse capacity.

Ownership effects distinguish gaining a building and neutralizing it. They update warehouse/indicator state, resource removal, library permissions/lists, heliport state, and pending balloon effects only within their verified domains. The caller owns the record's owner assignment and original sequencing. `RetiradaColonoPendente`, `DependenciaBalaoPendente`, and `SaidaRecrutamentoPendente` identify unsupported external dependencies; do not swallow them as successful completion.

Terrain resource extraction/regeneration follows original buffers, wrap behavior, and random-draw order. It does not automatically transport or credit final player resources. Recruitment initiation and progress do not implement full spawn/exit selection or allocation. The completion of unit production remains a next investigation.

Library initiation uses recovered costs and option tables; completion mutates lists and permissions in the observed order. Advance each supported production/learning step once at its correct caller boundary. A UI request and a simulation update are not interchangeable entry points.

Market proposal evaluation preserves signed32 arithmetic, global prices, directional sympathy, and alliance queries. `VideMatiere` has two stages using the first player's row; direct credit updates total/RMI and debits preserve partial effects if recalculation later fails. Avoid transactional rollback unless the original caller actually does it.

## Validation and next work

```sh
python3 -B pesquisas-paralelas/economia/validar.py
python3 -B pesquisas-paralelas/economia/validar.py --emular
```

The saved differential report records 214 tests and 54,871 bounded executions: 54,692 declared stops, 176 expected division-by-zero exceptions, and three expected limits. No optional tests were skipped in that historical run. Expected errors and dependency stops are declared coverage boundaries, not proof that a whole economic cycle completed.

Unit production completion, world allocation/spawn handoff, exit/balloon dependencies, transport credit, and higher-level market callers need further tracing. Economy should implement its own verified arithmetic/caller slices and publish callback requests to core. Do not rewrite pathfinding, physical structure placement, or graphic mappings in this domain. Read `validacao-emulada.json` and the module tests for exact current supported domains and reference buffers.
