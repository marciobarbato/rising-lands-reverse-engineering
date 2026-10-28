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
| `producao.py` | Unit/spell increments, colonist counts, x87 rounding, and `CalculTroupe` caller branches 1/2/13/16 |
| `saida_tropa.py` | `SortieTroupe` economic preparation: detach an existing colonist, unload stone/food, return pending world handoff |
| `aprendizagem.py` | Library option tables/lists, costs, learning initiation, completion |
| `mercado.py` | Totals, global prices, directional sympathy/alliance, proposal evaluation |
| `transferencias_mercado.py` | `VideMatiere` transfer arithmetic and ordered side effects |
| `ordem_mercado.py` | Resource-only `MarcheOrdreEchange` handshake and consuming `MarcheEchangePrend`/`Donne` callers |
| `bonus_unidades.py` | `BonusGetValEngin`/`EnginTypeGetCapacite` queries, selective `BonusReset`, and `BonusSetEngin` table producer |
| `bonus_compartilhados.py` | Actual bonus setter → committed core refresh composition on live unit/bonus buffers |

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

## Resource-only market exchange caller

`OrdemMercado(mercado, mundo, aceites=...)` shares the exact same `Economia` object between both providers. It copies four approval bytes from original base `0x4E2968`. `ordenar(jogador, proponente)` reconstructs all of `MarcheOrdreEchange` `[0x461BEA,0x461C4F)` for resource-only proposals, executing the real zero-unit branches of `MarcheEchangePrend` (`0x461621`) and `MarcheEchangeDonne` (`0x46189A`). Both player arguments truncate to u8 and must be 0–3 in the protected API. Invalid players are rejected before mutations, unlike the original unchecked memory accesses.

The **second argument owns the consumed proposal row**. Contacts, price indicators, alliance/sympathy, and sufficiency are not queried by this entry point. It toggles the first player's approval from zero to 1 or any nonzero byte to zero. If the second player's current approval is nonzero, or the first player's type byte is 2, it executes `Prend`, then `Donne`, then clears both approvals. It can execute even when the first player's newly toggled approval is zero. When both indices alias, the condition sees the newly toggled byte. The new Python bool return diagnoses whether both calls ran; it does not claim an original AL success flag.

| Stage | Units checked first | Resource movement | Mutation order for each nonzero resource |
|---|---|---|---|
| `receber(jogador, proponente)` / `Prend` | Offered-unit row of `proponente`, 26 × u16 | Offered-resource row of `proponente` to `jogador` | Conditional donor debit; destination total u16; consumed proposal entry = 0; destination RMI u16 |
| `entregar(jogador, proponente)` / `Donne` | Requested-unit row of `proponente`, 26 × u16 | `jogador` to requested-resource row owner `proponente` | Same order |

Resource IDs iterate 0=`Peças`, 1=`Comida`, 2=`Pedra`; quantities are u16. Zero entries are skipped completely, including player-type query and recalculation. Type-1 donors use `BatimentEnleveMatiere`; other type bytes do not debit. Destination credits wrap u16 without capacity checks or the 9,999 clamp, increasing total and RMI. Same-player transfers re-read the balance after debit. Resource row consumption distinguishes these callers from `VideMatiere`, which leaves its row intact and calls debit/recalculation even for zero quantities. The fourth resource record remains untouched.

Direct `receber`/`entregar` calls preserve approvals. In `ordenar`, only completion of both calls clears both approval bytes. A division failure during donor recalculation propagates after the donor debit and before destination credit/row consumption; already-completed entries and legs remain committed. No rollback is added. Nonzero unit rows raise `TrocaUnidadesMercadoPendente` at the first nonzero type in ascending 0–25 order: offered checkpoint `0x46166B`, requested checkpoint `0x4618DF`. The exception includes phase, both players, type, quantity, and address. It preserves the initial toggle and, for requested-unit stops, any completed offered-resource leg. These are genuine original checkpoints before the unsupported unit body, not successful unit transfers. Repeating the full order after a partial stop can retoggle approval and repeat unconsumed work; continuation requires the missing unit-transfer provider and original-order resumption.

Original EXE/SBL hashes are the same as above. [The additive market-caller evidence](../pesquisas-paralelas/economia/evidencias/ordem-mercado.json) includes exact bytes and hashes for all three caller bodies and shared epilogues. Unit branches are captured for provenance but not implemented. Fresh validation commands:

```sh
python3 -B pesquisas-paralelas/economia/capturar_ordem_mercado.py
python3 -B pesquisas-paralelas/economia/validar_ordem_mercado.py
python3 -B pesquisas-paralelas/economia/validar_ordem_mercado.py --emular
python3 -B scripts/check.py --domain economy
```

The new [original-x86 report](../pesquisas-paralelas/economia/validacao-ordem-mercado-emulada.json) records 18 passed tests, no skips/failures/errors, and 2,357 bounded executions: 2,241 routine returns (including approval waits), 104 explicit unit dependency stops, and 12 expected divide exceptions at `0x423635`. There are 2,345 declared stops and zero execution limits. The local stage suite passes 10 and skips 8 optional differential methods. Checks cover all 256 approval-byte values, aliased/all player pairs, direct calls, zero-resource skips, random protected buffers, first/second-leg unit stops and division failures, exact original total/row-clear/RMI write order, donor-debit argument order, and repeated calls. Evidence uses synthetic state and unmodified original instructions. The domain local gate passes 247 tests with 109 optional methods skipped. No prior full-x86 suite was rerun; complete market UI/AI/unit logistics or live missions are not established by these results.

## Remaining-component inventory after the first integrated slice

The first slice is integrated at main merge `1394669620a2d256b1abb9a9f0741f29728ee7eb`. These entries distinguish recovered local behavior from remaining live-world work. Symbol ranges alone identify investigation targets; they do not establish callee semantics.

| Subcomponent | Evidence and current status | Next dependency |
|---|---|---|
| Resource arithmetic, deposits, extraction, learning, progress | Existing modules and saved differential reports; new prefix adds fresh 426-execution validation | Correct real-mission dispatch and shared loaded state |
| Unit completion preparation | `SortieTroupe` prefix `[0x420E4C,0x420F5F)` implemented and integrated | Core `CalculPosition` and `EnginSetType`, then remaining caller cleanup `[0x420FB7,0x421250)` |
| Exit/balloon and unit market transfer | Prior explicit dependency classes; original `MarcheEchangePrend`/`Donne` unit loops at `0x461642`/`0x4618B6` | Original geometry/unit transfer/allocation contracts from core |
| General transport credit | SBL `EnginCalculTransporte` `0x44EA78`, `CalculTransporteEngin` `0x44F2D4`; earlier direct-call evidence includes deposits | Trace complete arrival/task gates without replacing navigation |
| Higher market exchange caller | `MarcheOrdreEchange` `[0x461BEA,0x461C4F)` resource-only path implemented and independently validated in the second slice | Integrated at `ac26806908d3d631c5f5910a9e0e379d39a1fb69`; nonzero unit bodies still require world providers |
| Market proposal/UI lifecycle | `CalculMarcheProposition` `[0x4670A8,0x467557)`, reset callers `[0x46634E,0x4663EB)`, persistence symbols | UI/input dispatch and world-presenter callbacks remain unimplemented |

The next selected slice is the resource-only `MarcheOrdreEchange` path. Original bytes show an approval-byte toggle, conditional ordered calls, resource rows cleared as each transfer commits, and no indicator test in this entry point. Both unit loops can execute their original zero-quantity branches without world callbacks when the corresponding unit proposal rows are zero. This closes more of the market execution chain independently of the missing core provider. Nonzero unit rows remain explicit pending stops with earlier mutations retained. The second slice is independently validated and integrated at `ac26806908d3d631c5f5910a9e0e379d39a1fb69`.

### Third-stage selection before implementation

The market stage is integrated; the worktree was clean before helper resume and updated-main merge. Core's committed `CalculPosition` provider is available at main merge `82122a2c790c835c455253b7cb701558ffcbfcca`; existing combat `EnginSetType` is being adapted by core rather than duplicated. The highest-value remaining economic dependency is now the exact capacity/bonus callback pair used by that converter.

Original `EnginTypeGetCapacite` `[0x4475AC,0x4475EF)` dispatches through the 26-entry table at `0x447544`; all larger AL bytes return zero. Original `BonusGetValEngin` `[0x428CC0,0x428E71)` reads player/type records at `0x4DFBA0`, player stride 468 and type stride 18, with selector dispatch at `0x428C8C`. Owners 4/200 return zero first. Conversion uses selector 1 (u8 `+0x0B`) and selector 12 (u8 `+0x10`). Selector 8 or selector bytes above 12 return incoming ECX without a table lookup; this must remain explicit rather than assuming a default zero. The next slice will implement/validate these original query providers and publish their callable contract to core; it will not rebuild the shared-world converter. Loaded bonus-state production remains a separate dependency.

## Unit capacity and bonus query providers

`capacidade_tipo(tipo)` reconstructs complete `EnginTypeGetCapacite` (`0x4475AC..0x4475EF`, shared return `0x4474C5..0x4474C7`). It truncates AL to u8 and returns zero for all bytes outside 0–25. Nonzero base capacities are types 5/6/7/11/14/16 = 1, type 12 = 2, 13 = 5, 15 = 3, and 17 = 6. These values come from the original jump table at `0x447544`, not inferred crew semantics or loaded unit costs.

`BonusUnidades(memoria=None).consultar(jogador, tipo, seletor, ecx=0)` reconstructs complete `BonusGetValEngin` (`0x428CC0..0x428E71`), the routine used by established `Modificateur` callbacks. Its state is 1,872 already-loaded bytes at original `0x4DFBA0`, with four players × 26 records × 18 bytes. The constructor copies the supplied table; omitted zero bytes are a synthetic fixture, not execution of a loader/reset. Player, type, and selector truncate independently to original AL/BL/DL u8.

For a table lookup, record address is `0x4DFBA0 + player*468 + type*18`. The provider returns unsigned fields with these original widths:

| Selector | Record offset | Return width |
|---|---|---|
| 0 | `+0x00` | u16 |
| 1 | `+0x0B` | u8 |
| 2 | `+0x02` | u8 |
| 3 | `+0x04` | u16 |
| 4 | `+0x06` | u8 |
| 5 | `+0x08` | u16 |
| 6 | `+0x0A` | u8 |
| 7 | `+0x0C` | u8 |
| 8 | No lookup | Incoming ECX u32 |
| 9 | `+0x0E` | u8 |
| 10 | `+0x11` | u8 |
| 11 | `+0x0F` | u8 |
| 12 | `+0x10` | u8 |
| 13–255 | No lookup | Incoming ECX u32 |

Mutation/callback order: none; both queries are read-only and call no provider. Owners 4 and 200 return zero **before** selector dispatch or index validation. For other owners, selector 8 or above 12 returns the explicitly supplied `ecx & 0xFFFFFFFF` before any table/index access. Only the remaining branches require protected player 0–3/type 0–25; otherwise the API raises `ValueError` without mutation. Those guards are not original executable checks. `ecx=0` is an explicit convenience input; the original does not supply a default and must not be described as always returning zero for unsupported selectors. No sign extension or clamp is applied to u16 fields.

Core conversion consumes `capacidade_tipo(tipo)` and `bonus.consultar(owner, type, id)` with selectors 1/12. Combat's established `Modificateur(owner, selector, type)` callback can use `lambda owner, selector, type: bonus.consultar(owner, type, selector)` for selectors 5/6. Combat consumes the low byte of these results at its caller boundary; selector 5 remains a full u16 return from this provider. No existing `Modificateur` identifier is renamed and no conversion/damage algorithm is duplicated. Both owners received this exact contract.

[Original query evidence](../pesquisas-paralelas/economia/evidencias/bonus-unidades.json) records exact bytes/hashes for three code intervals and both dispatch tables, under the same original EXE/SBL hashes above. Fresh commands:

```sh
python3 -B pesquisas-paralelas/economia/capturar_bonus_unidades.py
python3 -B pesquisas-paralelas/economia/validar_bonus_unidades.py
python3 -B pesquisas-paralelas/economia/validar_bonus_unidades.py --emular
python3 -B scripts/check.py --domain economy
```

The [fresh x86 report](../pesquisas-paralelas/economia/validacao-bonus-unidades-emulada.json) has 10 passed tests, no skips/errors/failures, and **4,060 complete original returns**: 1,352 valid player/type/selector combinations, 1,524 selector-byte/neutral/default cases, 768 capacity/register-width cases, and 416 poisoned byte/word cases. There are no dependency stops, expected exceptions, or limits. Full bonus buffers/guards remain unchanged; caller ECX and EBX preservation and capacity-query EDX preservation are checked. The local stage suite passes six and skips four optional methods. The domain gate passes 257 tests with 113 optional methods skipped. Historical and prior-stage x86 reports were not rerun.

This stage closes the read-only economic query contracts, independently validated and ready for serialized integration. Runtime table initialization and setters, provider wiring in core/combat, complete production continuation, and real-mission dispatch remain separate gaps. It supplies no invented bonus meaning for unproven selectors. Overall progress estimates remain the coordinator's coarse project estimate; query/test totals do not measure game completion.

### Fourth-stage selection before implementation

Stage 3 is integrated at main merge `7325CD0A3CB54D80D10A0C62C7D61BD25B0F8C49`, final pushed feature `d10c4e6af843b1af4e00286f212663fd777fd680`. Its common candidate gate passed 731 tests/319 optional skips. The next stage started only after clean helper resume and updated-main merge. Read-only query providers now exist; the highest-value remaining economic state gap is their exact mutation/reset producer.

Original `BonusSetEngin` `[0x428878,0x428C8A)` uses selector table `0x428844`, AL owner/BL type/DL selector/CX value, with BL=30 sentinels only in selected branches. Some all-type branches filter through original `TypeEnginEstArmee` (`0x44230C`). Selector 1 writes bonus `+0x0B`, then calls core-owned `EnginResetCapacite` (`0x4475EF`) after mutation; that dependency will remain explicit. Original `BonusReset` `[0x428E71,0x428EEE)` and shared return `0x428716` selectively clear all four unit-bonus rows, preserving offsets 3/7/15/16/17. The next slice will recover those table producers with fixed-width arithmetic, exact ordered writes and explicit refresh failure behavior; it will not duplicate world-unit mutation.

## Bonus-state producers: setter and selective reset

`BonusUnidades.reiniciar()` reconstructs complete `BonusReset` (`0x428E71..0x428EEE`, shared return `0x428716..0x42871A`). For players 0–3 and types 0–25, it writes zero in this order: u16 `+0`, u8 `+2`, u16 `+4`, u8 `+12`, u8 `+6`, u8 `+11`, u16 `+8`, u8 `+10`, u8 `+13`, u8 `+14`. Record bytes 3, 7, 15, 16, 17 survive. It does not refresh live-unit capacity or reset another table.

`bonus.definir(jogador, tipo, seletor, valor, recalcular_capacidades=None)` reconstructs the protected `BonusSetEngin` table producer (`0x428878..0x428C8A`). Inputs truncate to AL owner u8, BL type u8, DL selector u8, CX value u16. Selector above 12 is a no-op before any index validation. Active branches require protected owner 0–3; **setters do not use the read-query neutral-owner bypass** for 4/200. Normal types are 0–25. Runtime `tipos_unidades` is a copied 26 × 50-byte table supplied to the constructor; omitted bytes are synthetic zeros.

| Selector | Record write | Calculation / BL=30 scope |
|---|---|---|
| 0 | u16 `+0` | Signed32-wrapped product of runtime type word `+46` and CX, IDIV 10 toward zero, low u16; BL=30 applies to all 26 |
| 1 | u8 `+11` | CL; BL=30 updates types 12/13/15 only; then calls capacity refresh |
| 2 | u8 `+2` | CL; single type |
| 3 | u16 `+4` | Runtime type word `+48` minus `(word*10)//CX`; BL=30 only original `TypeEnginEstArmee` matches |
| 4 | u8 `+6` | CL; BL=30 only original `TypeEnginEstArmee` matches |
| 5 | u16 `+8` | CX; same BL=30 filter |
| 6 | u8 `+10` | CL; BL=30 all 26 |
| 7 | u8 `+11` | CL, single type, no capacity refresh |
| 8 | u8 `+13` | CL; this field is not returned by query selector 8 |
| 9 | u8 `+14` | CL |
| 10 | u8 `+17` | CL |
| 11 | u8 `+15` | CL |
| 12 | u8 `+16` | `(CX-10) & 255` |

The original all-type filter accepts types 0/1/2/3/8/11/12/15/16/18/19/20/21/22/23/24/25, as proven from `TypeEnginEstArmee` `0x44230C..0x442347`. BL=30 for other selectors and types 26–29/31–255 are outside the protected write domain, raising `ValueError` before writes. Neither percentage-style formula is replaced by speculative bonus meaning. Selector 0 preserves signed32 product overflow before division; selector 3 with CX zero raises before its first write. Other stored results wrap to their declared width.

Selector 1 writes the table first, then invokes `recalcular_capacidades(owner)` at original call `0x428C60 -> EnginResetCapacite 0x4475EF`. Without the callback it raises `CapacidadeUnidadesPendente` containing owner/address after those writes. Callback errors propagate with table writes retained. The callback belongs to core and must refresh existing live-unit Bag capacities in original order; this module does not rewrite unit/world state. Repeating the setter after a pending/error result repeats table writes and can repeat refresh effects; the caller owns resumption.

[Additive producer evidence](../pesquisas-paralelas/economia/evidencias/mutacoes-bonus.json) records four original code intervals, the selector table at `0x428844`, source hashes, input widths, preserved reset offsets and the dependency call. Fresh commands:

```sh
python3 -B pesquisas-paralelas/economia/capturar_mutacoes_bonus.py
python3 -B pesquisas-paralelas/economia/validar_mutacoes_bonus.py
python3 -B pesquisas-paralelas/economia/validar_mutacoes_bonus.py --emular
python3 -B scripts/check.py --domain economy
```

The [fresh producer report](../pesquisas-paralelas/economia/validacao-mutacoes-bonus-emulada.json) passes 11 tests with no skips/failures/errors: 2,094 bounded x86 calls, including 1,946 returns, 124 explicit capacity-refresh stops, and 24 expected divide exceptions at `0x428A67`/`0x428ACE`. There are 2,070 declared stops and zero expected limits. Coverage includes all owner/type/selector combinations in the protected single-type domain, sentinel filters, unsupported-selector no-ops, signed product/width boundaries, post-write dependency state, all 1,040 ordered writes per reset, and untouched runtime types/bonus neighbors. The local producer suite passes five/skips six optional methods; the domain gate passes 268 tests with 119 optional skips. The owning full-suite report runner now includes the new benchmark groups when explicitly run; a local reporting smoke run passed 268 tests/119 skips with its report redirected to a temporary file, leaving predecessor and prior-stage reports unchanged.

This stage closes table reset/mutation producers, independently validated before integration. Live-unit refresh remains core's explicit provider, as do mission event/loading dispatch and complete production/runtime composition. It does not by itself establish a live mission or justify a new global completion percentage.

### Fifth-stage selection before implementation

The bonus producer stage is integrated at `25f5feabed2ce8828bd514f4a960f8cab9c3669e`, feature `e99d2316f715312cc7f97cf6a9b196f42ce08959`. The next stage started only after clean helper resume and updated-main merge. Core's committed shared conversion adapter was inspected from this checkout; its logic remains core/combat-owned.

The remaining inventory now selects the real economic simulation caller: `CalculTroupe` (`0x4259E6`) for the shared building-type branches 1, 2, 13, and 16 only. Original dispatch suffix `0x426401` also routes types 1/2 into the same type-16 body. Original branches `[0x425A4B,0x425C4E)` advance progress once using colonist/capacity x87 arithmetic, then active type 16 calls `SortieTroupe` with direction 4 and type 13 with direction 14. The call happens even below completion, relying on the callee's threshold early return. Recovering that caller composes existing validated economy behavior and closes a genuine update boundary without duplicating core conversion. Other building dispatches, healing/exit/cleanup, and live-mission dispatch remain unsupported.

## Production simulation caller: `CalculTroupe` branches 1/2/13/16

`Producao.calcular_tropa(indice, saida_tropa=None)` recovers the original `CalculTroupe` (`0x4259E6`) shared branches for building types 1, 2, 13, and 16. Original dispatch sends 1/2 through `0x426401` to the type-16 body `0x425A4B`; type 13 uses `0x425B5E`. Other dispatches are protected `ValueError` cases before mutation, not claimed original failures. Index truncates to AX u16 and must address a provided 276-byte record in the protected 1–1,000-record pool.

Order and effects:

1. Read building type and apply the supported-branch guard. Original activity requires nonzero u32 progress `+0x8C` and nonzero byte `+0x74`. Inactive calls return `None`, do not query recruitment time, and do not call exit. State `+5`, owner eligibility and UI selection are not checked here.
2. Active calls query time from requested-type byte `+0x7B` and compare unsigned progress against the u16 time multiplied by 100. If below, count colonists with `BatimentGetColons`/`BagContient` mode 1 over Bag capacity, read the building-type capacity byte via `BatimentGetCapacite`, and add the existing x87-accurate increment `100 + low16(trunc((count/capacity)*100))`. Runtime type tables, protected Bag count/reference domains, masked divisor-zero behavior, binary64 intermediate rounding, and control word `0x127F` retain the existing production contract. The final addition is u32. At/above threshold there is no increment or colonist/capacity query.
3. **Every active call then invokes `SortieTroupe`, even below completion.** Types 1/2/16 pass direction 4; type 13 passes 14. Default behavior executes `SaidaTropa.preparar`, whose own threshold returns early or detaches/unloads an existing colonist before returning its position dependency. The crossing update can both increment and prepare the unit in the same call. No world allocation/conversion/healing or cleanup is invented.
4. An explicit `saida_tropa(index_u16, direction_u8)` callback replaces the whole original exit call boundary after the increment. Its diagnostic return is forwarded. Exceptions preserve progress and any callback-side effects. The callback must preserve the actual original exit behavior; it is not automatically called a successful production.

This is the simulation-update boundary. Do not invoke `avancar_unidade` and then `calcular_tropa` for the same update: the latter already contains the progress step. After a pending handoff or partial failure, do not process the same building again until the original continuation resolves it; the prefix may already have removed its colonist/cargo while progress and activity still remain set. The committed core converter can consume the pending record, but later healing/exit/cleanup are still required and owned at their declared boundaries.

[New caller evidence](../pesquisas-paralelas/economia/evidencias/ciclo-producao.json) contains exact entry/branch/dispatch/epilogue bytes and hashes plus the original coefficient bytes. The harness runs from the **real function entry**, then actual inline progress instructions and the original exit prefix, with no native callback substitution. It stops at the original return or before `CalculPosition`; the prefix's existing deposit dependency/error domains still apply. Fresh commands:

```sh
python3 -B pesquisas-paralelas/economia/capturar_ciclo_producao.py
python3 -B pesquisas-paralelas/economia/validar_ciclo_producao.py
python3 -B pesquisas-paralelas/economia/validar_ciclo_producao.py --emular
python3 -B scripts/check.py --domain economy
```

[Fresh validation](../pesquisas-paralelas/economia/validacao-ciclo-producao-emulada.json): 10 tests pass with no skips/errors/failures; 1,432 native calls = 1,268 returns + 160 position dependency stops + 4 expected post-increment deposit division exceptions at `0x423501`. There are 1,428 declared stops and zero limits. Comparisons include complete economic/capacity/building/unit/terrain/recruitment/production buffers and guards, observed exit-call arguments, original register preservation on returns, x87 control/tag state, masked divisor-zero and binary64 samples, activity/time/unsigned boundaries, indices 0/999 with high-word poison, sequential updates to preparation, and partial failure after progress. The local suite passes six/skips four optional methods; the domain gate passes 278 tests/123 optional skips. Prior-stage and historical x86 reports were not rerun.

Global gap closed: recovered simulation caller sequencing for four supported production building types, connecting progress and economic completion preparation at the proper update boundary. Independently validated before integration; complete world production and loaded-mission runtime remain unsupported. The coordinator's coarse overall estimate remains approximately 50% (40–60% uncertainty).

### Sixth-stage selection before implementation

Stage 5 is integrated at `342063d0303d6a31587851ecb5af4898f3457601`, final feature `9e07845bff79820d7cdd3d39f3b77d136c309ca8`; its common gate passed 804 tests/348 optional skips. Only then did the clean feature worktree resume through the helper and merge updated main.

The next highest-value integration gap is the bonus producer's actual world callback, now available in committed core main `8126f1aed299e19337e2b1ac4f95cfa85c068214`. The economy-owned entry point will wire `BonusSetEngin` selector 1 to `atualizar_capacidades_unidades` using the same post-write bonus object and live 800-record unit buffer, with actual committed capacity/modifier queries. No core scan will be copied. Complete original setter→refresh→query execution and whole shared-state comparisons will replace the earlier dependency-only coverage for this composed entry point. Deliberate later pre-query stops will verify partial effects without replaying a setter. Mission/event dispatch and complete production continuation remain separate gaps.

## Bonus mutation joined to the live unit refresh

`definir_bonus_no_mundo(bonus, mundo, jogador, tipo, seletor, valor)` in `bonus_compartilhados.py` supplies the actual core callback to the original bonus setter. It calls the existing setter exactly once; selector 1 then loads `ferramentas/capacidades_unidades.py` from this same checkout and calls `atualizar_capacidades_unidades(mundo, owner, capacidade_tipo=capacidade_tipo, modificador=bonus.consultar)`. No table, unit buffer, scan, or query algorithm is copied. A same-named provider already imported from another checkout/snapshot raises `ImportError` at the callback boundary. Other selectors do not load or invoke the core provider.

Input widths and protected setter domains remain AL/BL/DL u8, CX u16 as above. The bonus object is the same object **after** its mutation; `mundo.unidades` is the caller's writable 800 × 276-byte live pool. This wrapper adds no whole-pool validation before table writes. At the callback point core validates pool type/length, then scans indices 0–799, skips states 0/4 and mismatched owners, queries native base capacity then selector-1 bonus, and writes the sum's low u16 at unit `+0x0C`. All eligible units of that owner refresh, including types other than the specific type whose table entry changed. Existing Bag counts/tags/contents remain untouched even if capacity becomes smaller than count or exceeds the modeled 30-slot cargo domain.

A successful call returns `None` after the actual refresh. Import, core guard, and query errors propagate after table writes; earlier unit-capacity stores also remain committed if a later query fails. The failing unit and later units remain unchanged. No rollback or setter replay is performed. The optional lower-level `BonusUnidades.definir(..., recalcular_capacidades=...)` remains available for explicit integration boundaries; its prior dependency-only report stays unchanged. Read-only queries must not mutate/reenter bonus/world state.

The committed callback contract is [core capacity refresh](core/CAPACITY_REFRESH.md), originally integrated at `8126f1aed299e19337e2b1ac4f95cfa85c068214`. [The composed evidence manifest](../pesquisas-paralelas/economia/evidencias/bonus-compartilhados.json) records exact original setter, scan, query and epilogue bytes/hashes plus immutable provider revisions. The new benchmark begins at `BonusSetEngin 0x428878` and executes the **whole original setter→800-slot refresh→economic queries** unpatched to return. Later-error comparisons use genuine conditional pre-query checkpoints at `0x44763A` for unit indices 0/7/799; those are not original native faults. Three Python callback errors and three protected invalid-type errors are compared with these stops after earlier stores.

```sh
python3 -B pesquisas-paralelas/economia/capturar_bonus_compartilhados.py
python3 -B pesquisas-paralelas/economia/validar_bonus_compartilhados.py
python3 -B pesquisas-paralelas/economia/validar_bonus_compartilhados.py --emular
python3 -B scripts/check.py --domain economy
```

The [fresh composed report](../pesquisas-paralelas/economia/validacao-bonus-compartilhados-emulada.json) passes 11 tests with no skips/errors/failures: 454 native calls, 448 complete returns and six deliberate pre-query stops. There are zero native exceptions or execution limits. Nested capacity/bonus query counts are reported separately from top-level calls. Whole 220,800-byte unit pools, 1,872 bonus bytes, runtime-type buffers/guards, original nested-query order, table-write-before-unit-store order, all ordinary owner/type pairs, sentinel/byte boundaries, unrelated selectors, and later partial failures are covered. Local stage: five passed/six optional skipped. Domain gate: 289 tests/129 optional skips. Historical and earlier-stage reports were preserved.

Global gap closed: the previously pending economic capacity-table mutation now has a validated actual world-refresh connection using committed providers. This is shared synthetic loaded-state operation, not a real-mission run. Mission/event loading and complete production/exit/cleanup remain open. The coordinator's coarse project estimate remains approximately 50% (40–60% uncertainty).
