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
| `saida_tropa.py` | `SortieTroupe` economic preparation: detach an existing colonist, unload stone/food, return pending world handoff |
| `aprendizagem.py` | Library option tables/lists, costs, learning initiation, completion |
| `mercado.py` | Totals, global prices, directional sympathy/alliance, proposal evaluation |
| `transferencias_mercado.py` | `VideMatiere` transfer arithmetic and ordered side effects |

Deposit capacity and excess generation do not imply completed unit transport. `BatimentEnleveMatiere` and `BatimentCalculResource` preserve debit/recalculation order, including division-by-zero after earlier mutations. `BatimentInitCave` reconstructs per-type counts and warehouse numbers without redefining per-warehouse capacity.

Ownership effects distinguish gaining a building and neutralizing it. They update warehouse/indicator state, resource removal, library permissions/lists, heliport state, and pending balloon effects only within their verified domains. The caller owns the record's owner assignment and original sequencing. `RetiradaColonoPendente`, `DependenciaBalaoPendente`, and `SaidaRecrutamentoPendente` identify unsupported external dependencies; do not swallow them as successful completion.

Terrain resource extraction/regeneration follows original buffers, wrap behavior, and random-draw order. It does not automatically transport or credit final player resources. Recruitment initiation and progress do not implement full spawn/exit selection or allocation. The unit completion preparation below is independently supported; world conversion and final cleanup remain open.

Library initiation uses recovered costs and option tables; completion mutates lists and permissions in the observed order. Advance each supported production/learning step once at its correct caller boundary. A UI request and a simulation update are not interchangeable entry points.

Market proposal evaluation preserves signed32 arithmetic, global prices, directional sympathy, and alliance queries. `VideMatiere` has two stages using the first player's row; direct credit updates total/RMI and debits preserve partial effects if recalculation later fails. Avoid transactional rollback unless the original caller actually does it.

## Unit completion preparation: `SortieTroupe`

`SaidaTropa(recrutamento).preparar(indice, direcao)` reconstructs the prefix at `0x420E4C` through the call at `0x420F5A`, stopping **before** `CalculPosition` (`0x420698`). It returns `None` below the completion threshold or an immutable `PreparacaoSaidaTropa` describing a pending dependency. This result does not mean a unit has spawned. The original prefix removes an existing type-9 colonist and later calls `EnginSetType`; it does not allocate a new unit.

| Input/state | Width and supported domain |
|---|---|
| `indice` / original AX | Low u16; must address one of the provided 1–1,000 building records, each 276 bytes |
| `direcao` / original DL | Low u8; all 256 values are retained without interpreting geometry |
| Building `+0x7B` | Requested type u8, protected range 0–25; time comes from the type table word `+0` |
| Building `+0x8C` | Progress u32, compared unsigned against time u16 × 100 |
| Building Bag | Base `+0x0C`; first live tag-1 reference whose unit type byte `+1` equals 9 |
| Unit Bag | Base unit `+0x0A`; count/capacity words must be 0–30; referenced units must be 0–799 |
| Deposit owner | Building `+4` u8; protected range 0–3 when a deposit is reached |

The prefix does not test building activity `+0x74`, state `+5`, ownership eligibility, or recruiting-building type. Time zero with progress zero reaches preparation. Callers own those eligibility checks. The existing x87 progress increment is unchanged; this prefix uses only integer threshold and Bag/deposit operations.

Effects occur in this order:

1. Below threshold, return without changing any buffer. At or above it, use `BagRetire` mode 1 to remove the first matching colonist from the building Bag.
2. `BagRetire` decrements its word `+0x66` with u16 wrapping, shifts the remaining values/tags left, clears the old last slot, and decrements the live-count word. The colonist record is not reset or converted.
3. Obtain its Bag via `EnginGetBag` (`0x4474A6`). Repeatedly count resource ID 2 with `BagContient` mode 2 over **capacity**, then remove one matching entry over **live count**. Removal decrements `+0x66` even for resource entries. Call `BatimentAjouteMatiere(owner, resource=2, quantity=2, building)` after each removal. The quantity is the returned entry value 2, not one per slot.
4. Repeat for resource ID 1, crediting quantity 1 per removed entry. Other tags and resource ID 0 remain. Stone always precedes food, regardless of slot order.
5. Return `PreparacaoSaidaTropa(indice, direcao, unidade, tipo_unidade, endereco_dependencia=0x420698)` with the existing unit index. No world callback executes in this API.

Deposits preserve existing capacity, excess-bag, RNG, and failure semantics. Division failure can occur after the building colonist and one carried resource entry have been removed and the credit has changed a balance. `RetiradaColonoPendente` can interrupt a type-4 deposit after the cargo removal. Neither failure is rolled back or turned into a successful handoff. Do not retry this prefix after a failure or pending handoff: prior removals have already happened.

Missing colonists, out-of-buffer references, and Bag count/capacity above 30 are protected `ValueError` cases; they are not claimed original error returns. A matching resource tag beyond live count is outside the terminating supported domain and raises when removal fails, retaining earlier mutations. Invalid unit Bag state is checked after the colonist removal. The original can instead read outside the modeled pool or loop on malformed Bags.

The smallest requested core continuation is `CalculPosition(AX=building u16, BL=direction u8) -> AX=position u16`, followed by `EnginSetType(EAX=existing unit index, DX=position, CL=requested type)` at `0x420F69 -> 0x457B87`. Captured context then calls life/fatigue/experience, exit/task, and optional `EnginAsk` operations. Those calls, subsequent structure cleanup/messages, balloon paths, other production branches, and navigation remain unsupported here. The handoff snapshots the requested type at this boundary; a future original-order continuation must account for callbacks that mutate the shared building record before the original reload of `+0x7B`.

Evidence is additive in [the prefix manifest](../pesquisas-paralelas/economia/evidencias/saida-tropa.json), with exact bytes, interval hashes, original SBL names, and jump-table targets. Original EXE SHA-256: `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`; SBL SHA-256: `c3a5411255847d36161aea1aeef06ab280265c55fa5a6626cfeb7bab523cc627`. Prefix interval `[0x420E4C,0x420F5F)` SHA-256: `708fbdb1555a8562c5248924e749e537e4fdafa6f13ba98968612c9ffbf285ad`. Existing predecessor evidence/manifests are unchanged.

Fresh validation on 2026-10-28:

```sh
python3 -B pesquisas-paralelas/economia/capturar_saida_tropa.py
python3 -B pesquisas-paralelas/economia/validar_saida_tropa.py
python3 -B pesquisas-paralelas/economia/validar_saida_tropa.py --emular
python3 -B scripts/check.py --domain economy
```

The new suite has 15 tests: the local run passes 9 and skips 6 optional differential methods; the emulated run passes all 15 with no skips. Its [fresh report](../pesquisas-paralelas/economia/validacao-saida-tropa-emulada.json) records 426 original executions: 390 position dependency stops, 24 early returns, 4 `BatimentRetireColon` dependency stops, and 8 expected divide exceptions at `0x423501` after mutation. Thus 418 reach declared stops; there are no expected execution limits. Comparisons include all economy, capacity, building, unit, terrain, recruitment table/selection buffers, guards, deposit call order/arguments, mixed/duplicate Bags, u16 counter wrap, unsigned thresholds, all 26 requested types, and all 256 directions. Inputs are synthetic states, not captured live-mission states. The first sandbox x86 attempt exited with SIGILL before completing a test; approved execution with Unicorn JIT available passed. The domain local gate passes 229 tests with 101 optional differential methods skipped. Historical differential suites were not rerun by this slice.

## Validation and next work

```sh
python3 -B pesquisas-paralelas/economia/validar.py
python3 -B pesquisas-paralelas/economia/validar.py --emular
```

The saved differential report records 214 tests and 54,871 bounded executions: 54,692 declared stops, 176 expected division-by-zero exceptions, and three expected limits. No optional tests were skipped in that historical run. Expected errors and dependency stops are declared coverage boundaries, not proof that a whole economic cycle completed.

After the supported `SortieTroupe` preparation, world conversion/spawn completion, exit/balloon dependencies, general transport credit, and higher-level market callers still need further tracing. Economy should implement its own verified arithmetic/caller slices and publish callback requests to core. Do not rewrite pathfinding, physical structure placement, or graphic mappings in this domain. Read `validacao-emulada.json` and the module tests for exact current supported domains and reference buffers.
