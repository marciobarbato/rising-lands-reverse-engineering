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

### Seventh-stage selection before implementation

Stage 6 is integrated at `15e49e8dfe7c77f60ec0c468e5546bc891384f42`, final feature `e07dc41562af96e7bc909146cbf81e7653f0e4a7`; common gate 827 tests/357 optional skips. The next stage resumed the same clean helper-managed tree and merged updated main before new implementation.

The remaining market lifecycle gap is now selected: complete `MarcheResetAll` `[0x46027C,0x4602CD)`, `ResetMarche` `[0x46634E,0x4663D6)`, and `MarcheQuitte` `[0x4663D6,0x4663EB)`. Inspected original bytes reset seven per-player fields but leave proposals, approval bytes, global difference, balances and sympathy intact. Pair reset mutates its first row before using the second index; quit captures the contact before that mutation. Exact supported u8 indices, ordered writes and protected invalid-contact partial state will be recovered without assuming a transactional or whole-market reset. Core's remaining production physical helpers and live-mission dispatch remain separate dependencies.

## Selective market lifecycle

After the human resumed research, the worktree incorporated committed main `5e2bf0831d3aaa776481a6ab023be262ef0df1bd`. The current core production continuation still stops before healing; the exact remaining shared-world calls were requested from core. This independently bounded market slice follows the inventory above while those providers are unavailable.

`CicloMercado(mercado, **buffers)` in `ciclo_mercado.py` shares the supplied `Mercado` object, including its live `contatos` and `indicadores`. It copies five additional loaded buffers: raw u8 arrays `bytes_2e7c`, `bytes_292c`, `bytes_2928` (four bytes each), and u16 arrays `words_2938`, `words_2940` (eight bytes each). Unknown names or wrong sizes raise before use. Omitted data are synthetic zeros, not a recovered loader. These raw names make no unverified gameplay interpretation.

The three methods return `None`, invoke no callbacks, and reproduce complete original bodies in the protected player domain 0–3 after u8 truncation:

- `resetar_todos()` (`MarcheResetAll`, `[0x46027c,0x4602cd)`) visits players 0–3. Each row writes `2e7c=0`, indicator word=0, contact=255, `292c=1`, `2928=0`, `2940` word=0, `2938` word=0, in that order.
- `resetar(j,k)` (`ResetMarche`, `[0x46634e,0x4663d6)`) first writes row j in order `2e7c`, `292c`, `2928`, contact, indicator, `2940`, `2938`, with the same values. **Only after these writes** is k protected/validated. The second row order is `2e7c`, contact, `292c`, `2928`, `2938`, `2940`, indicator. Aliased rows still receive both write sequences. Invalid j raises before mutation; invalid k raises after j's writes, which remain committed. These Python guards are not original executable branches.
- `sair(j)` (`MarcheQuitte`, `[0x4663d6,0x4663eb)`) captures the live contact byte before calling pair reset. An invalid contact, including 255 after a prior quit/reset, therefore raises after the first row's reset. Repeating quit is not an automatically harmless operation in this protected model.

Proposals, prices, approvals at `0x4e2968`, global difference, balances, player records, sympathy and neighboring bytes are preserved. This is not whole-market clearing or exchange execution. The [additive original manifest](../pesquisas-paralelas/economia/evidencias/ciclo-mercado.json) records three byte/hash intervals under the unchanged EXE/SBL identities. The actual original pair caller executes unchanged for quit; no call return is substituted. Protected invalid-second comparisons stop at original `0x466395`, after the complete first row and before the original second-index use. They do not claim original native exceptions for unchecked indices.

[Complementary REA evidence](../pesquisas-paralelas/economia/evidencias/ciclo-mercado-rea.json) records pinned source `b9a8f8e9f25feb9cc97bf4960748f2bdf8c898bc`, original and normalized-analysis hashes, provider/profile, retained dossier hash, and the reviewed quit instructions/call edge. Ghidra's inferred ECX `__fastcall` parameter is explicitly rejected against the Watcom AL/DL instructions and native comparisons. The restricted first startup failed Java `spawn EPERM`; the authorized context succeeded and the session closed/exported cleanly. No shared tool or original project was changed.

```sh
python3 -B pesquisas-paralelas/economia/capturar_ciclo_mercado.py
python3 -B pesquisas-paralelas/economia/validar_ciclo_mercado.py
python3 -B pesquisas-paralelas/economia/validar_ciclo_mercado.py --emular
python3 -B scripts/check.py --domain economy
```

[Fresh native report](../pesquisas-paralelas/economia/validacao-ciclo-mercado-emulada.json): 14 tests passed, zero skips/errors/failures; **1,275 executions = 259 complete returns + 1,016 deliberate first-row checkpoints**, zero native faults or limits. Coverage includes all player pairs/aliases, poisoned high register bits, all 252 invalid second bytes × four first players, quit contact boundaries, persistent reset/quit sequences, exact native/model write order (including duplicate alias writes), complete market/economy/player buffers, and seeded neighboring gaps/guards. Local stage executes seven tests and skips seven optional native tests. Historical and earlier-stage reports remain unchanged. The required economy gate passes 303 discovered tests with 136 optional skips and valid documentation links.

Global gap closed: original selective market reset/quit lifecycle, shared with the existing proposal/approval model and preserving its transaction state. Implemented and independently original-x86 validated; required integration result follows separately. Real-mission market dispatch, unit exchange, complete production and mission loading remain open. Overall project estimate remains coordinator-owned, approximately 50% with 40–60% uncertainty, independently of test totals.

### Stage 7 integration and eighth-stage selection

Implementation `c10dff75af2495946a8f0fb204eb71ada35941e2`, final feature `5eafc1eff6235536a243716ec7253ee5992537c6`, main merge `874167ede98bdb08980d7d071683945ec25785ff` are pushed. The required helper passed core 280/134 optional skips, combat 163/102, economy 303/136, graphics 115/0, workflow 3/0: 864 discovered/372 optional skips in total. Subsequent fetch plus ancestry checks confirmed all three commits reachable from remote main. The clean tree then resumed with the helper and fast-forwarded to that merge.

Stage 8 selects actual `CalculTroupe` → economic preparation → committed core position/conversion/healing/fatigue composition on identical shared unit/structure buffers, stopping at original `0x420f81` before experience setup. Core has reported 2,020 independent executions for its healing/fatigue stage; implementation here waits for that provider's committed integration/API rather than reading another live worktree. Whole original caller execution from `0x4259e6` will verify progress occurs once, low-byte bonus queries consume the loaded shared table, deposits retain their order, and later import/query failures retain preceding progress/removal effects. Building cleanup audited at `0x420fb7` also depends on unit-type Bag predicates, terrain/color changes, and unit/building AI messages; no completion or retry is inferred from resetting the progress field. This selection precedes implementation.

## Production update joined through live recovery

`producao_compartilhada.calcular_tropa_no_mundo(producao, mundo, bonus, indice)` joins the existing production caller and economic preparation to actual committed core position/conversion/recovery. Core recovery implementation `3b7f71697095ab12e960bf4cbdf0952d20d554d8` was consumed from inspected main `62b9d76941dbcf90a2dc5d45b71317136c8b5d28`; [its contract](core/RECOVERY.md) remains authoritative. No world helper or bonus algorithm is copied.

The supplied `Producao`/`Recrutamento` must use the exact same 800 × 276-byte unit object and 1,000 × 276-byte structure object as core `mundo`. A mismatch raises `ValueError` before progress. The wrapper does not copy or silently reconnect buffers. Existing protected input widths/domains remain in effect: AX building index u16, supported production types 1/2/13/16, existing colonist/reference and terminating Bag domains, loaded 1,300-byte unit types, and an explicitly supplied loaded bonus object. Bonus queries must be read-only; synthetic zeros do not establish mission initialization.

The wrapper calls `Producao.calcular_tropa` once. Its exit callback calls `SaidaTropa.preparar` once, including the below-threshold path; only a prepared result loads the committed core providers. It then reads u16 runtime width/height from `producao.tipos_construcoes[type*52]` and passes them to the existing position query. Conversion reloads live requested type `+7b`, uses actual `capacidade_tipo`/`bonus.consultar`, and retains its original unit/search partial effects. Recovery heals by 1000 with u16 wrap/strict clamp, then clears fatigue and copies the live `+76` word. The wrapper returns the existing frozen `RecuperacaoSaidaTropa` at **`0x420f81` before experience**. Inactive/below-threshold returns are `None`, with any already-applied progress retained. Do not separately advance production on that update.

Core imports are scoped to this checkout and occur after economic preparation. The lazy position dependency is resolved inside that scope; a clean-process test checks that no permanent core search path is needed. Foreign same-named provider modules raise `ImportError` at the import boundary. Import, dimension, conversion/bonus or recovery errors propagate with preceding progress, colonist/cargo removal, resource credits and any unit/search writes retained. This wrapper adds no rollback or retry. After a pending result or partial failure, the caller must suspend further updates until an explicit continuation resolves it. Replaying can repeat removals or healing; this API does not claim complete recruitment or physical placement.

[The new composition manifest](../pesquisas-paralelas/economia/evidencias/producao-compartilhada.json) records original caller continuation bytes, immutable provider revisions and hashes of the committed entry/preparation/position/conversion/recovery evidence, preserving the distinct original EXE/SBL identities. The benchmark begins at actual `CalculTroupe 0x4259e6` and executes all original nested calls unpatched, stopping at return or the declared pending point. Python query observers call the actual providers; no native callback result is substituted. Two import failures compare to native `CalculPosition` entry, and four Python query failures compare to native bonus entry, after the preceding effects. These six stops are deliberate dependency boundaries, not native faults.

```sh
python3 -B pesquisas-paralelas/economia/capturar_producao_compartilhada.py
python3 -B pesquisas-paralelas/economia/validar_producao_compartilhada.py
python3 -B pesquisas-paralelas/economia/validar_producao_compartilhada.py --emular
python3 -B scripts/check.py --domain economy
```

[Final native report](../pesquisas-paralelas/economia/validacao-producao-compartilhada-emulada.json): 13 tests pass/no skips/errors/failures; **782 native calls = 136 returns + 636 experience stops + four bonus-query stops + two import stops + four expected deposit divide exceptions at `0x423501`**, zero limits. Whole economy/capacity/terrain/recruitment/production/unit/structure/search buffers and guards match. All four production building types × 26 output types × owners 0/1/2/3/4/200, live inactive/converting states, edge indices/high bits, loaded dimension/bonus/health boundaries, exact query/deposit order and twelve persistent update sequences are covered. Local stage executes seven tests/skips six optional methods. Required economy gate: 316 discovered tests, 142 optional skips; documentation links pass. The [initial failed report](../pesquisas-paralelas/economia/validacao-producao-compartilhada-primeira.json) is retained: 53 calls, four trace assertions failed because inherited economy and core observers shared one list; separate observation routing fixed the harness without changing reconstructed behavior. Earlier-stage reports remain untouched.

Global gap closed: the real production update now composes through economic removal/credit and actual shared-world positioning, conversion, healing and fatigue, with independently verified partial failures. Required integration is reported separately. No experience, occupancy/placement, spell/movement/conditional request, building cleanup, mission loading or real-mission operation is claimed. The overall estimate remains the coordinator's approximately 50% (40–60% uncertainty).

### Stage 8 integration and ninth-stage selection

Stage 8 implementation `3c2fc2c3d3227e89cec76bff357ab3ce5395dd47`, final feature `4f0cd24126b68e1812437915f1b05e6ce16bd679`, main merge `089919c926bfdcddd94152fe3abcf40c8001e81f` are pushed. Required common checks passed core290/138 optional skips, combat178/111, economy316/142, graphics115/0, workflow3/0 (902/391 total). Fresh fetch and ancestry checks verified all three on remote main, which subsequently advanced. Exact stable contract was published to core, app and mission owners. The clean feature resumed with the helper before the next selection.

Stage 9 selects the economy-owned cleanup prefix at `0x420fb7`, only after the still-pending experience/placement/movement/request caller has completed. Protected building types remain 1/2/13/16. Original type2 first runs `BagContientTroupe` (`0x44724a..0x4472d3`), a capacity-scanning unit-type predicate; a false result falls through to the existing type9 `BagContient`. Other supported types query type9 directly. A retained unit sends control to the common selective reset, then the unit-message call at `0x4211d3`. Without one, types1/2 reset first; all four then reach terrain query call `0x42110c`, with raw parameter10 for type2 and8 otherwise. Reuse the actual committed core `resetar_estrutura` for the identical inline reset sequence. New validation must be labeled an **isolated cleanup continuation** with explicit original frame/register inputs, not a whole production run or a bypass of the missing preceding calls. No terrain/AI-message effects are skipped or guessed. This inventory precedes implementation.

## Isolated production cleanup continuation

`limpeza_saida.retomar_limpeza_saida(producao,mundo,pedido)` consumes only an explicit handoff at **`0x420fb7`**, after the original experience/placement/movement/conditional request calls. The current complete production provider does not reach this address; this is an isolated continuation contract, not permission to bypass those dependencies. It accepts u16 building/output indices (protected 0–999/0–799), supported building types1/2/13/16, identical live economy/core structure and unit objects, and the existing loaded recruitment model. Wrong handoff, indices, type or shared identity fail before mutation.

Complete `bag_vide(recrutamento,indice)` (alias `bag_contient_troupe`) reconstructs original SBL `BagContientTroupe [0x44724a,0x4472d3)`; Stage 9–14 prose mislabelled it `BagVide`, which is `0x4470b9` (Stage 15 erratum). It scans the Bag's u16 **capacity**, restricted to0–30, and only tag1 entries. It returns at the first referenced unit whose u8 type is **not** in `{3,11,12,13,14,15,16,17,25}`; all other bytes, including26–255, pass. A live count of zero does not prevent a tagged capacity entry from being read. References are protected0–799 only when encountered; a successful early return does not read/reject later references. This query checks no unit state/owner and mutates nothing.

Cleanup type2 first runs that predicate; on false it falls through to the existing `Producao.contar_unidades(indice,9)` capacity query. Other supported types query type9 directly. A true retention result invokes the actual committed core `ciclo_estruturas.resetar_estrutura`, then returns frozen `LimpezaSaidaTropa(indice,unidade,0x4211d3,0x4829c8,70)`, before the unit AI message. On false, types1/2 invoke the same core reset first; types13/16 have no reset yet. All four return at `0x42110c`, before `BatimentGetCase 0x41aee2`, with raw EDX parameter10 for type2 and8 otherwise. The subsequent original `0x476e82` terrain call and AI messages remain pending. Type/owner/state, unit Bags, balances and unlisted structure bytes retain the original effects; resetting progress is not a completion event.

The reused core reset implementation is `7a24e974384782e66d6c7454fe1343035e1178db`, integrated since the first core stage. It supplies the identical inline store sequence here: fields `+78/+86=ffff`, `+7b=ff`, `+7c/+7e=0`, payload words`+80/+82=0` for this supported type domain, `+74=0`, progress`+8c=0`, state3 preserved/otherwise5. No reset algorithm is duplicated. The provider loads only at the original first reset boundary, using a scoped same-checkout import; a foreign provider raises there, with no fabricated later effects. Errors propagate, and a pending/error result must not be replayed as completion.

[Additive cleanup evidence](../pesquisas-paralelas/economia/evidencias/limpeza-saida.json) records the original cleanup context, complete predicate bytes/hashes, jump table and committed reset manifest identity under unchanged EXE/SBL hashes. The native harness declares the isolated original frame (`[ESP]` building word, `[ESP+4]` output unit word, EDI live building address), executes actual original Bag calls and inline reset, and stops before the unresolved terrain/message call. It does not execute or claim the preceding unit caller. The direct Bag query alone runs to its original return.

```sh
python3 -B pesquisas-paralelas/economia/capturar_limpeza_saida.py
python3 -B pesquisas-paralelas/economia/validar_limpeza_saida.py
python3 -B pesquisas-paralelas/economia/validar_limpeza_saida.py --emular
python3 -B scripts/check.py --domain economy
```

[Fresh native result](../pesquisas-paralelas/economia/validacao-limpeza-saida-emulada.json):10 tests pass/no skips, **1,184 executions =512 complete predicate returns +555 unit-message stops +117 terrain-query stops**, zero faults/limits/errors/failures. Whole economic/capacity/terrain/recruitment/unit/structure buffers and guards match. All256 predicate type bytes with count0/1, both edge structure slots/high bits, state3 retention versus other states, all four supported building types, mixed tags/duplicate references and seeded reset fields are covered. Local stage: six executed/four optional skipped. Required economy gate passes326 discovered tests/146 optional skips and documentation links. Prior reports remain unchanged; the aggregate runner counts this bench only when explicitly run.

Global gap closed: verified local cleanup decisions and selective reset ordering after production, with actual shared core reset reuse. Independently validated as an isolated continuation; mandatory integration follows. Preceding unit placement/request calls, pending terrain/AI messages, other building types, mission initialization and real-mission execution remain explicit gaps. The coordinator's overall estimate remains approximately50% (40–60%), separate from test totals.

### Stage 9 integration and tenth-stage selection

Cleanup implementation `3a7ac12a4906553b73b84037a17f51c0c552cf88`, final feature `c191342066b8484cab929f285c02a6669da36327`, main merge `29f90a27a522ad13d732ec821ecf73729042e2e4` are pushed and ancestry-verified after fresh fetch. Required common gate passed core302/143 optional skips, combat185/115, economy326/146, graphics115/0, workflow3/0:931 discovered/404 optional skips. The exact pending terrain/unit/building AI calls were published to core. Clean feature then resumed via helper before selection.

Stage 10 selects the actual production-update composition through the now-committed core experience provider from main `dae42125f45c348c10dff7e727e803138be7670f` (implementation `f67898b75423adcfaf90a7b6e6c710c409e6f9ee`). A new explicit entry will delegate once to the Stage8 recovery composition and then consume its handoff using `retomar_experiencia_saida`, stopping at `0x420f8a` before placement. Existing Stage8 API/endpoint remains stable. The raw40-byte owner queue must be supplied as loaded/inherited state; synthetic zeros do not establish initialization. Whole original `CalculTroupe` execution must compare queue/AF/F5–F8 and all preceding shared effects, including failures after recovery. This inventory precedes implementation; cleanup's420fb7 entry remains unavailable until the intervening real calls are implemented.

## Production update joined through experience

`producao_experiente.calcular_tropa_com_experiencia_no_mundo(producao,mundo,bonus,indice)` calls the Stage8 shared production/recovery entry exactly once, then only on a prepared recovery result loads and invokes actual committed core `retomar_experiencia_saida(mundo,pedido,recrutamento.tipos_unidades)`. It returns `None` for inactive/incomplete updates, otherwise the existing frozen `ExperienciaSaidaTropa` at **`0x420f8a` before placement**. The original Stage8 `calcular_tropa_no_mundo` still returns before experience at `0x420f81`; its contract and reports are unchanged. No queue, level, conversion, healing or progress algorithm is copied.

All earlier shared-object/loaded-table/protected-domain contracts apply. Experience additionally consumes the supplied live raw40-byte `mundo.experiencias_unidades`, supporting owner0–3. Core's constructor zeros are synthetic, not a recovered mission default. The actual core provider tests the first experience byte then first type; it never searches later pairs. A match writes AF, applies the original selected F5–F8 effect through `EnginSetNewExperience`, then shifts that owner's five pairs in the original order. Runtime unit-type `+2e` is supplied from the same recruitment table. The distinction from combat's separate lethal-experience routine remains explicit in [core's queue contract](core/EXPERIENCE_QUEUE.md).

The experience provider is imported from this checkout only after recovery. Wrong queue type/length/owner and foreign/missing provider errors therefore preserve economic progress/removal/credit, conversion/search changes, healing and fatigue; later queue effects do not occur. This is still a one-shot production handoff: no repeated tick/replay, allocation, placement, movement/request or building cleanup is implied. The isolated cleanup entry at420fb7 cannot consume this earlier checkpoint.

[New composition evidence](../pesquisas-paralelas/economia/evidencias/producao-experiente.json) records exact original experience-caller bytes and immutable prior-composition/core-queue evidence identities. Core implementation `f67898b75423adcfaf90a7b6e6c710c409e6f9ee` was inspected from integrated main `dae42125f45c348c10dff7e727e803138be7670f`. The fresh native harness begins actual `CalculTroupe 0x4259e6` and runs all nested calls unpatched, comparing the entire queue and existing shared buffers. Twelve protected queue errors and two import failures are compared to actual post-recovery checkpoint420f81, before native queue use; they are not native faults or claims about unchecked neutral-owner memory.

```sh
python3 -B pesquisas-paralelas/economia/capturar_producao_experiente.py
python3 -B pesquisas-paralelas/economia/validar_producao_experiente.py
python3 -B pesquisas-paralelas/economia/validar_producao_experiente.py --emular
python3 -B scripts/check.py --domain economy
```

[Fresh native report](../pesquisas-paralelas/economia/validacao-producao-experiente-emulada.json):11 tests pass/no skips/errors/failures; **610 calls=136 returns+460 placement checkpoints+14 deliberate post-recovery stops**, zero faults/limits. Coverage includes four building×26 output type×four owner combinations, all eight encoded experience levels, 32 first-pair guard cases with later matches, queue/raw data boundaries, full queue/unit/structure/search/economic/capacity/terrain/production buffers and guards, edge indices/high bits, and twelve persistent update sequences ending at a single handoff. Local stage executes six tests/skips five optional methods. Required economy gate passes337tests/151optional skips and documentation links. Historical and predecessor reports remain untouched.

Global gap closed: the actual production update now consumes the committed recruitment experience queue after live recovery on the same state, independently original-x86 validated. Required integration follows. Physical output placement, conditional request, full cleanup/terrain/AI messages and real-mission operation remain open; overall estimate stays coordinator-owned at approximately50% (40–60%).

### Stage 10 integration and eleventh-stage selection

Experience composition implementation `38375594123849fb6607cd9ec8749202166e5e8f`, final feature `ff9dcf7b49f5bde6e030a2bb745c8420658b9e9f`, main merge `12b97ff3f2b1a1f242a0d5430ff0a0f914791d10` are pushed. Required gate passed core302/143 optional skips, combat191/119, economy337/151, graphics122/0, workflow3/0 (955/413 total). Fresh fetch/ancestry verified all three on main. Exact producer/queue contract shared with app and mission owners. Clean feature helper-resumed to current committed main before selection; core placement is still being validated and has no committed provider to consume.

Stage11 selects complete read-only transport status queries `EnginRentreMatiere [0x456cd9,0x456d35)` and `EnginApporteMatiere [0x456d35,0x456d92)`. Original unit state must be5/17/18. The first requires byte+82=2, reads u16 building reference+80, calls actual `BatimentGetType [0x41a4f4,0x41a513)`, and compares the building **type+8** to requestedDL byte. This is not a player-owner query. The second compares full u16+84 to requestedDL u8, then treats BL=0 as wildcard or requires BL==byte+82. Names do not prove further semantics for raw+84/+82. Queries mutate nothing and do not execute cargo transfer, orders or movement. Protected unit indices0..799 and building indices0..999 only when that conditional read is reached; false early branches must ignore unused invalid building references. Original register widths/guards and both complete native returns will be checked before integration. This inventory precedes implementation; no existing committed core provider duplicates these addresses.

## Read-only transport status queries

`ConsultasTransporte(recrutamento)` in `consultas_transporte.py` shares the supplied recruitment/unit/structure state. Omitted recruitment constructs synthetic data; it does not initialize a mission or transport order. Both complete original queries truncate AX unit index to u16 (protected0–799, 800-record pool), compare literal unit state5/17/18 and return a Python boolean corresponding to AL0/1. They mutate nothing.

`retorna(indice,tipo_construcao)` reconstructs `EnginRentreMatiere [0x456cd9,0x456d35)`. After the state gate, byte+82 must equal2; only then is target building word+80 read. Protected target must be0–999 and fit the supplied structure pool. Actual original `BatimentGetType [0x41a4f4,0x41a513)` reads building byte+8, compared to requestedDL u8. Building owner+4 and unit owner do not participate. Invalid targets on earlier false branches are never read/rejected. An invalid target on the conditional lookup raises at that query boundary; no native index guard is claimed.

`aporta(indice,valor84,modo82=0)` reconstructs `EnginApporteMatiere [0x456d35,0x456d92)`. It compares the full u16 unit+84 against requestedDL u8; a stored257 does not match requested1 or257 (DL=1). Only after matching does BL0 act as wildcard; otherwise lowBL must equal byte+82. No building, owner or Bag read occurs. Raw parameter/field names preserve the unproven wider meaning of+84/+82; these functions do not execute cargo transfer, movement, orders or a transport state machine.

[New original evidence](../pesquisas-paralelas/economia/evidencias/consultas-transporte.json) records all three complete byte/hash intervals under unchanged EXE/SBL identities. The benchmark executes both original queries and actual conditional building-type getter unchanged. Six protected Python target errors compare to original getter entry0x41a4f4 before unsafe lookup; native exceptions are not invented for those indices.

[Complementary REA coverage record](../pesquisas-paralelas/economia/evidencias/consultas-transporte-rea.json) preserves pinned source revision, separate intact/normalized-analysis identities, provider/profile and retained observation hashes. Existing read-only Ghidra has no procedure at456d35 and its instruction Listing reports undecodable there. This is an **existing analysis coverage limitation**, not a finding that the intact CPU bytes are invalid. No project repair or auto-analysis was attempted; original SBL/Capstone bytes and actual native execution establish this contract. The private session exported/closed. No shared adapter change or substantive reasoning stall occurred.

```sh
python3 -B pesquisas-paralelas/economia/capturar_consultas_transporte.py
python3 -B pesquisas-paralelas/economia/validar_consultas_transporte.py
python3 -B pesquisas-paralelas/economia/validar_consultas_transporte.py --emular
python3 -B scripts/check.py --domain economy
```

[Fresh native result](../pesquisas-paralelas/economia/validacao-consultas-transporte-emulada.json):12 tests pass/no skips, **4,934 calls=4,928 complete returns+six conditional pre-lookup stops**, zero faults/limits/errors/failures. Covers all256 state bytes, both edge unit slots, building0/999, mode/comparison byte domains, full word nonmatches, early unused-reference guards, poisoned high register bits, original preserved registers, and seeded complete unit/structure/economic buffers with guard preservation. Local stage:six executed/six optional skipped. Required economy gate:349discovered/157optional skips, documentation links pass. Historical and earlier native reports remain untouched; aggregate counts the new bench only for future explicit runs.

Global gap closed: exact complete economic transport-status predicates with conditional target lookup and original integer widths, independently native-validated. Required integration follows. This does not close transport actions/state machines or production placement/request/cleanup. Core's placement provider is now integrated ataa9cba47af34aef3b0b4b67faded0b884bb1e428; after this bounded stage integrates, the priority is actual producer composition to420f9e using that committed provider. No real mission is claimed; coordinator's overall estimate remains approximately50% (40–60%).

### Stage 11 integration and twelfth-stage selection

Transport implementation `bf2de88a49444f16a6f01a677fd6cdbb4c2f7a0f`, final feature `5d84ded24667400997492131ce814c4b0db77009`, main merge `477bc3a682fc0bb8a2a26781eef76123718341ed` are pushed and ancestry-verified after fresh fetch. Required common checks:core319/151 optional skips, combat198/123, economy349/157, graphics134/0, workflow3/0 (1003/431 total). Clean feature resumed through helper and incorporated current main before selection.

Stage12 selects actual production composition through committed `colocacao_saida.retomar_colocacao_saida` (implementation `6b3882b5b4a3a0c99dddcaccbd4d1c08a765f8ce`, main `aa9cba47af34aef3b0b4b67faded0b884bb1e428`), ending420f9e after physical exit and original movement order. Existing recovery/experience endpoints stay stable. In addition to identical unit/structure buffers, the new entry must require economic terrain types **identical to physical objects** (shared original pointer507d74), and economic quantities **identical to physical object-owner bytes** (507dac). These raw aliases are established by the original pointer consumers; no universal meaning for every cell byte is inferred. Reject mismatched aliases before progress, without silently reconnecting copies.

Native tests will begin actualCalculTroupe, use the actual core physical world/harness/intervals/effect observers and preserved-state native segmentation, then compare economy plus full physical/search/queue/routes/discovery/light/minimap buffers. Count original entries and additional bounded resumes separately. Core's normal-owner vision sumBB+F5 domain0–8 and pre-discovery partial failure must remain exact, after economic/experience effects. Conditional owner/EnginAsk420f9e..420fb7 and all later cleanup/AI effects remain pending; no jump to the isolated cleanup API. This inventory precedes implementation.

## Production update joined through physical exit and movement order

`producao_colocada.calcular_tropa_com_colocacao_no_mundo(producao,mundo,bonus,indice)` calls the existing experience producer once, then only on its prepared result loads actual committed core `colocacao_saida.retomar_colocacao_saida`. It returns `None` for inactive/incomplete updates or the existing frozen `ColocacaoSaidaTropa` at **`0x420f9e` before conditional owner/request handling**. Existing recovery/experience public APIs and endpoints remain stable. Core implementation `6b3882b5b4a3a0c99dddcaccbd4d1c08a765f8ce` was consumed from integrated main `aa9cba47af34aef3b0b4b67faded0b884bb1e428`; [its physical-exit contract](core/UNIT_EXIT.md) owns every collision/vision/light/minimap/movement algorithm.

Before progress, this entry requires two additional original raw-buffer aliases: `r.mundo.terreno.tipos is mundo.objetos` at507d74, and `r.mundo.terreno.quantidades is mundo.donos_objetos` at507dac. Prior unit/structure identity guards still apply. A mismatch raises without reconnecting or copying data. Names describe existing domain views of the same byte arrays; they do not assign one universal meaning to every cell. The remaining physical world, loaded type/bonus tables and writable experience queue are explicit supplied state. Full producer ownership is restricted by the experience queue's supported owners0–3; this does not widen to the physical helper's neutral-owner subdomain.

After economic progress/removal/credit, conversion/search release, recovery and experience, actual core placement writes current/step/destination, releases search, inserts new collision while preserving old occupancy, enables+72, and performs discovery/light/minimap in its original order. It then reloads live building+7c and calls actual `definir_movimento`; destination objects read the same raw object array as the economic view. This issues the original order without advancing a path or arrival. Normal-owner vision sumBB+F5 must be0–8; larger sums raise at the original pre-discovery boundary after preceding economic/experience/record/collision effects. Late import errors preserve all previous recovery/experience effects. No rollback, implicit replay or extra progress tick is supplied. Pending/error buildings must remain suspended until explicit continuation; economic cleanup has not cleared their active/progress fields.

[New composition evidence](../pesquisas-paralelas/economia/evidencias/producao-colocada.json) records actual caller bytes, raw pointer-consumer context and immutable prior/core manifest identities under unchanged EXE/SBL hashes. The original starts at actual `CalculTroupe 0x4259e6`, executes every nested call unpatched, and uses the committed core physical harness/observers. Its established preserved-state segmentation stops before genuine `SetMiniMap` entry after the instruction threshold and resumes that same instruction with all registers/flags/stack intact. No CALL/RET, original instruction, or callback result is replaced; the per-segment cap/timeout is unchanged. Economic data loaders run through a separate adapter so they cannot replace core's physical loader or redirect the shared raw pointers. Core fixture/effect observers are reused as committed code, not copied world implementations.

```sh
python3 -B pesquisas-paralelas/economia/capturar_producao_colocada.py
python3 -B pesquisas-paralelas/economia/validar_producao_colocada.py
python3 -B pesquisas-paralelas/economia/validar_producao_colocada.py --emular
python3 -B scripts/check.py --domain economy
```

[Final native report](../pesquisas-paralelas/economia/validacao-producao-colocada-emulada.json):13 tests pass/no skips/errors/failures; **192 original entries in552 bounded segments**, including360 native minimap resumptions. Entry outcomes:64 complete returns,118 request checkpoints420f9e, eight pre-discovery stops446146, two post-experience import stops420f8a. Native faults/limits are zero. The [earlier four-building calibration](../pesquisas-paralelas/economia/validacao-producao-colocada-quatro.json) independently records four joined entries/20segments; it is not an additional original-only capture. Broad coverage includes all four building×26 output types, ordinary owner/edge index samples, loaded nonzero bonus tables, live movement object branches, vision 0/8 thresholds and unsaturated light counts, inactive and late-error branches, and four persistent progress sequences. Full physical/unit/structure/group/search/route/queue/discovery/light/minimap, economic/capacity/recruitment/production buffers, input guards and complete deposit→physical→movement effect traces match. Core's earlier original-only captures remain separate upstream evidence.

Local mode executes six tests and skips seven optional native methods. The required economy gate passes 362 discovered tests with 164 optional skips and valid documentation links. The initial local command failed before discovery because the committed core test fixture needed its tools import path; the new test's setup was corrected. Both new native runs passed. Prior/historical reports are untouched; the aggregate runner includes the new bounded-segment counter only for future explicit runs.

Global gap closed: the actual economic producer now reaches verified physical unit placement and original movement order on one shared loaded world. Independently native-validated before mandatory integration. Conditional owner/EnginAsk420f9e..420fb7, full cleanup/terrain/AI messages and real-mission operation remain open; the isolated cleanup API cannot bypass that gap. Coordinator's overall approximate50% estimate (40–60%) remains separate from test totals.

### Stage 12 integration and thirteenth-stage selection

Placement composition implementation `e1ff67fc0eb729dae87505721170b266831f4af6`, final feature `2b159f81129b50c6366df52b14fd2a9a999d136a`, main merge `62f0a1c86c35a5bb883d156423bcd1efe71f0772` are pushed and fresh-fetch ancestry-verified. Required checks passed core319/151 optional skips, combat211/131, economy362/164, graphics148/0, workflow3/0 (1,043/446 total). Producer/raw-alias contracts were published to app and missions. This chat did not modify the canonical checkout; its ref advanced externally during coordinated project work. The clean feature resumed via the helper before selection.

Stage 13 selects actual producer composition through committed `voz_unidades.retomar_solicitacao_saida`, implementation `b1585b4bd8a64c92aa28455fc39b13c87993a067` at main `66e83062f1dd821b04a59b820fcc7e2712839f60`. It consumes placement420f9e and reaches cleanup420fb7 only after the supported original owner/EnginAsk branch returns. Four explicit loaded u16 viewport words are required when volume is reached. Hidden/foreign-owner paths may not need them; visible active handles still query volume and write F9. Visible inactive handles retain F9 and raise the exact pending PostSound request instead of fabricating playback or a handle. Missing viewport stops before volume. Reuse the core caller and request logic, preserving earlier APIs and partial effects. Whole original CalculTroupe execution must compare physical/economic/queue state and exact pending sound arguments, with entry/segment counts separate. Existing cleanup is not invoked before this handoff. This selection precedes implementation.

## Production update joined through the conditional request

`producao_solicitada.calcular_tropa_com_solicitacao_no_mundo(producao,mundo,bonus,indice,*,janela=None)` delegates once to the physical producer, then invokes actual committed core `voz_unidades.retomar_solicitacao_saida`. It returns `None` for inactive/incomplete updates or actual `SolicitacaoSaidaTropa` at **`0x420fb7`, ready for the separate cleanup**. Core implementation `b1585b4bd8a64c92aa28455fc39b13c87993a067` was consumed from main `66e83062f1dd821b04a59b820fcc7e2712839f60`; [the request contract](core/UNIT_REQUEST.md) remains authoritative. No owner comparison, visibility, volume, selection or sound algorithm is copied. Prior recovery/experience/placement APIs and endpoints remain stable.

All prior loaded-state/identity/domain/one-shot requirements apply. The caller supplies `janela=(x,y,width,height)` as four loaded u16 viewport words when volume is reached. The actual core caller compares the live building owner with local camera, skipping the request for a foreign owner. A hidden request returns without volume data. A visible request still queries volume for a non-FFFFFFFF handle, then writes F9 and returns. A visible FFFFFFFF handle writes F9 and raises the exact pending PostSound descriptor, including opcode/code/flag/full volume and relative handle offset. Missing viewport data stops before the volume query. Zero volume does not silently discard a requested sound. The wrapper creates no backend, handle, queue insertion or playback result.

Core voice and its selection/movement dependencies load only after successful placement, through a scoped same-checkout import. Import, volume or PostSound dependencies retain all earlier economic/removal/credit, unit/search/recovery/experience, physical/vision/minimap/movement effects. Pending data/requests must be explicitly resolved; replay is not a continuation. Cleanup is not invoked by this entry, and building activity/progress remain set until that later step. Only a returned420fb7 handoff can enter the existing economic cleanup API.

[Composition evidence](../pesquisas-paralelas/economia/evidencias/producao-solicitada.json) records exact original conditional-caller bytes, immutable prior/core manifest identities and declared viewport/sound boundaries under unchanged EXE/SBL hashes. Native tests begin actual `CalculTroupe`, execute the original nested request and volume routines, and stop before missing volume/PostSound calls without replacing any original instruction or return. Core's preserved-state minimap resumptions remain unchanged. Pending sound arguments are decoded with the actual committed native decoder and compared to the core's Python descriptor.

```sh
python3 -B pesquisas-paralelas/economia/capturar_producao_solicitada.py
python3 -B pesquisas-paralelas/economia/validar_producao_solicitada.py
python3 -B pesquisas-paralelas/economia/validar_producao_solicitada.py --emular
python3 -B scripts/check.py --domain economy
```

[Fresh native report](../pesquisas-paralelas/economia/validacao-producao-solicitada-emulada.json):15 tests pass without skips/errors/failures; **266 original entries in796 bounded segments, including530 minimap resumes**. Entry outcomes:64 original returns,144 cleanup checkpoints,52 pending PostSound checkpoints, four missing-viewport checkpoints and two post-placement import checkpoints. Native faults/limits are zero. Coverage includes four building×26 output types, all ordinary building-owner/camera pairs, explicit inherited handle branches, hidden/local/foreign paths, full viewport words/selection/zero-volume packing, inactive updates and four persistent sequences. Full physical/economic/unit/structure/group/search/routes/queue/vision/minimap/recruitment/production buffers and checked input guards match, together with complete deposit→physical→movement traces and exact pending sound arguments.

The [first four-building calibration](../pesquisas-paralelas/economia/validacao-producao-solicitada-quatro.json) passes four original entries/20segments and remains separate from the expanded result. The [initial local report](../pesquisas-paralelas/economia/validacao-producao-solicitada-local-primeira.json) retains one fixture error: raw discovery0 was incorrectly assumed hidden, while core's established rule treats low five zero bits as visible. Using0x1f corrected the fixture; no reconstructed implementation changed. Final local mode executes seven tests/skips eight optional native methods. Required economy gate:377 discovered/172 optional skips and valid documentation links. Historical and predecessor reports remain untouched; future explicit aggregate runs count the new bounded segments.

Global gap closed: the actual producer reaches the original economic cleanup boundary after the supported conditional request, while genuine missing viewport/audio insertion stays explicit. Independently native-validated before mandatory integration. Full cleanup/terrain/AI messages, sound insertion and real-mission operation remain open; no playback or complete mission is claimed. The coordinator's approximate50% overall estimate (40–60%) remains independent of test totals.

### Stage 13 integration and fourteenth-stage selection

Request composition implementation `7fe62277516d4ebac77f1e862cb4a9b8f36f3b2b`, final feature `7a43a7c9587074a34379315b4296fa8b68ce3335`, main merge `9e0efeaa8032cbef76f58236ebe2d34fff9501ae` are pushed and fresh-fetch ancestry-verified. Required gate passed core341/161 optional skips, combat219/137, economy377/172, graphics162/0, workflow3/0:1,102 discovered/470 optional skips. The feature was clean and helper-resumed before selection.

Stage 14 selects the actual producer→supported request→existing economic cleanup connection, using `limpeza_saida.retomar_limpeza_saida` exactly once after the genuine420fb7 handoff. It must stop at the original first terrain query or unit AI message, preserving all earlier economic/world/voice effects. Natural remaining-colonist fixtures must use a distinct existing unit record; duplicate references to the converted output are not evidence of another colonist. Native checks will begin actual CalculTroupe and compare prefix, Bag predicates and selective-reset timing on the same world, including count/capacity differences and late import failures. No terrain/AI call or sound insertion will be skipped. Earlier pending producer endpoints remain stable.

A maintained-name correction accompanies this inventory: original SBL identifies41aee2 as `BatimentGetCase`. Earlier Stage9 prose/manifest used the informal label `BatimentGetPosition`; the original address, bytes, checkpoint and behavior did not change. Maintained prose now uses the original symbol. A new erratum will retain the predecessor manifest's identity and correction; old evidence will not be rewritten. This inventory precedes implementation.

## Production update joined through economic cleanup

`producao_limpa.calcular_tropa_com_limpeza_no_mundo(producao, mundo, bonus, indice, *, janela=None)` delegates once to the actual producer/request composition and, only after its genuine `0x420fb7` handoff, invokes the existing `limpeza_saida.retomar_limpeza_saida`. It returns `None` for an inactive/incomplete update or the existing frozen `LimpezaSaidaTropa` before the first unsupported terrain query or unit AI message. No progress, request, Bag predicate or reset algorithm is copied. Earlier producer APIs/endpoints are unchanged.

All prior loaded tables, shared unit/structure/terrain identities, ordinary owner domains, explicit viewport and one-shot rules still apply. The cleanup uses capacity scans, including tagged entries beyond live count. Type 2 first uses the complete `BagContientTroupe` type predicate, then the type-9 query on false; the other three types use type 9. A retained unit causes the actual committed core reset, then stops before `iagUnitSendMessage` at `0x4211d3`, callee `0x4829c8`, AX output unit/EDX 70/EBX 0. On an empty predicate, types 1/2 reset before the first terrain query, while types 13/16 preserve activity/progress at that boundary. The pending query is `BatimentGetCase` at `0x42110c`, callee `0x41aee2`, AX building/EDX 10 for type 2 and 8 otherwise. `EteintTerrain` at `0x421116` and later messages remain unsupported.

The reset provider loads only when the original reaches its first reset store (`0x421097` empty 1/2; `0x42116e` retained). A missing provider preserves all prior producer/removal/credit, conversion/recovery/experience, physical/vision/minimap/movement and voice effects, with no reset store. Earlier viewport/PostSound dependencies propagate before cleanup. Do not replay or tick a pending/failed building. This remains a prepared-state production pipeline, not natural recruitment initialization, complete production or a running mission.

The [additive composition manifest](../pesquisas-paralelas/economia/evidencias/producao-limpa.json) binds the predecessor request/cleanup and core reset evidence under unchanged original EXE/SBL hashes. Its [symbol erratum](../pesquisas-paralelas/economia/evidencias/limpeza-saida-symbol-erratum.json) records the original SBL name `BatimentGetCase`, correcting Stage 9's informal `BatimentGetPosition` label. The old manifest identity and original catalog record are included; predecessor evidence is byte-identical. Address, captured code, checkpoint and behavior are unchanged.

```sh
python3 -B pesquisas-paralelas/economia/capturar_producao_limpa.py
python3 -B pesquisas-paralelas/economia/validar_producao_limpa.py
python3 -B pesquisas-paralelas/economia/validar_producao_limpa.py --emular --quatro
python3 -B pesquisas-paralelas/economia/validar_producao_limpa.py --emular
python3 -B scripts/check.py --domain economy
```

The [fresh native report](../pesquisas-paralelas/economia/validacao-producao-limpa-emulada.json) passes all 16 tests without skips, failures or errors: **332 original entries in 1,504 bounded segments, including 1,172 preserved-state minimap resumptions**. Entry outcomes are 66 complete returns, 125 unit-message stops, 131 terrain-query stops, six pending PostSound stops, two missing-viewport stops and two pre-reset import stops. Native faults and execution limits are zero. The earlier [four-building calibration](../pesquisas-paralelas/economia/validacao-producao-limpa-quatro.json) independently passes four entries/20 segments and is separate from the expanded report.

Coverage includes all four building × 26 output types × two retention branches, eight remaining-type predicate samples per building, ordinary owners and edge building/unit indices, state 3/255, eight stale capacity cases, inactive/incomplete calls, four persistent sequences and explicit earlier/late dependencies. Remaining-colonist fixtures reference a distinct existing record; duplicate references to the converted output do not establish retention. Stale count/capacity fixtures are explicit raw-state tests, not mission-coherence claims. Full physical/unit/structure/group/search/routes/queue/vision/light/minimap and economic/capacity/recruitment/production buffers, input guards, bonus/realizable tables, complete deposit→physical→movement traces and pending sound arguments match. Local mode executes eight tests and skips eight optional native methods. Historical reports remain untouched; the aggregate runner counts this new bench only on future explicit runs.

The expanded native run completed during an interrupted turn; its preserved successful output was inspected on resume, without replacing or duplicating it. No substantive differential mismatch occurred in this stage. The feature was helper-resumed with owned changes preserved; newer main changes are left to the required clean-tree integration helper. This chat did not modify the canonical checkout.

Global gap closed: the actual prepared producer reaches selective economic reset and the genuine terrain/AI boundaries on the same loaded world. Remaining dependencies include natural startup/exit geometry, terrain cleanup, unit/building AI messages, sound insertion and real-mission dispatch. The coordinator owns the coarse overall estimate; native checkpoint counts do not measure full-game completion. Publish final implementation/feature/main hashes and required gate counts after integration.

Stage 14 required economy gate: 393 discovered tests pass, with 180 declared optional native skips; documentation links pass.

Final review corrected the new distinct remaining unit fixture: its owner belongs at byte +0, not +3. The earlier successful native report is preserved separately as `validacao-producao-limpa-emulada-primeira.json`; the final expanded native run uses the corrected fixture. No reconstructed algorithm changed.

### Stage 14 local integration preparation

Implementation `e1bbc3d5cc9f0441e56e96a203170b0341f09d2e` is committed. After automatic approval rejected the required feature/main integration helper for lack of accepted direct user authorization, the clean feature locally merged fetched main `6b15be1c96348d51dac7a46208126e6974290eca` as `778e2af653369f9d09a45a6c5b46ffa2d1cad822`. This is a local feature preparation, not a feature push or main integration. No failed candidate or native report was discarded.

Main brought core placement refactor `c84556f`. A fresh full Stage 14 native run against that merged provider passes all 16 tests, with the same 332 entries /1,504 segments /1,172 resumptions and declared outcomes, without skips, mismatches, faults or limits. The pre-main successful report is separately retained as `validacao-producao-limpa-emulada-antes-main.json`. Full common local preflight passes core350/166 optional skips, combat227/143, economy393/180, graphics169/0, workflow6/0: **1,145 discovered /489 optional skips**; documentation links pass. This preflight does not replace the required locked integration helper's final gate.

The human explicitly approved coordination messages after their initial automatic-review rejection; coordinator/core received the exact status and dependency requests. Feature/main push and merge remain subject to the separate final authorization requested in this chat. The stage must not be called integrated until the required helper and fresh ancestry checks succeed. No next implementation has started.

### Stage 14 integration

The locked helper integrated Stage 14: implementation `e1bbc3d5cc9f0441e56e96a203170b0341f09d2e`, feature commits `e64e29471243e44f0584635beb5c628ad41f204e`/`94276dc0335f9d9e9430ba5321589a75cce31601`, main merge `aa873df6e930155fa3eae4c022249ab0c6fa2242`, all ancestors of fetched `origin/main`. The preparation note above is superseded. Before Stage 15, `test_producao_colocada.py` began deriving its vision-stop fixtures from core's `insercao_unidades.SOMA_VISAO_MAXIMA_INSERCAO` (fallback 8; implementation `db77da6`, main `f18b5a00a27e716fd3662d56f9482b67b110ef16`). If no vision sum above that limit is representable (u8 `+0xBB` at most 255), those cases compare the original continuation instead of a stop.

## Structure habitation for `MissionPlaceTerrain` (Stage 15)

[construcoes_habitaveis.py](../pesquisas-paralelas/economia/construcoes_habitaveis.py) provides the two economic calls of the original structure scan. The [original-byte inventory](../pesquisas-paralelas/economia/evidencias/habitaveis.json) exports 20 intact intervals, three jump tables and the 22-record structure-type table with hashes (EXE `6c556520…43fb`; the normalized analysis PE `26c4534b…64d0` is named but never executed). The [original-only captures](../pesquisas-paralelas/economia/evidencias/captura-habitaveis-original.json) were recorded and committed (`7081ac9`) before any translation.

**Caller order** (`MissionPlaceTerrain 0x46c16d..0x46c1b8`, after the unit scan and capacity refresh): for AX index 0..999 ascending, `BatimentExiste 0x41a735`; if AL, `PlaceBatiment 0x41c4ac` (core), `BatimentEstHabiter 0x41a5b8`, and only if that AL is nonzero `BatimentHabitable 0x41cc70`; then `BatimentModifyMap 0x419e97` with AX index and EDX 1 (core) for every existing structure. The loop exits at `0x46c17d` into the shared `pop edx/pop ebx/ret` at `0x46b6f5`. Missions composes this loop; economy supplies only the two calls below.

| API | Original | Inputs and result |
|---|---|---|
| `estrutura_habitada(producao, indice)` or `HabitacaoConstrucoes.estrutura_habitada(indice)` | `BatimentEstHabiter 0x41a5b8` | AX u16 building, protected 0..999 in the supplied pool; returns AL 1/0. Type 21: `BagContientTroupe 0x44724a` only. Type 2: `BagContientTroupe`, then on false `BagContient(tag 1, unit type 9)`. Other types: `BagContient` only. Scans Bag capacity (0..30) at `+0x0e`, not live count; unit references 0..799 are checked only when read. No mutation |
| `HabitacaoConstrucoes(aprendizagem, *, unidades_realizaveis, estruturas_realizaveis)` | state of `0x41cc70` | Uses by identity: structure/unit pools of `aprendizagem.producao.recrutamento`, technology Bags `propriedade.pendencias` (`0x4dd6e8`, 4 owners × 22 types × 104 bytes), spells `propriedade.sortilegios` (`0x508f30`) and `aprendizagem.inventados` (`0x508f44`), unit realizability (`0x4e1934`, 4 × 26 bytes), structure realizability (`0x4dfad4`, 4 × 22 bytes), capacities `0x4dfb2c` and resources `0x4e2ea8`. Only lengths are checked; nothing is copied or defaulted |
| `definir_tecnologia(jogador, tipo)` | complete `BatimentSetTechnologie 0x41c76c` | AL owner u8, DL type u8. Owner ≥ 4 and types without a branch return unchanged. Each branch runs `BagInit` on that owner/type Bag, then `BagPrend` (`0x447483`, unchecked append) in original order: type 1 cap 4 + units 0,1,2,8; type 2 cap 4 + 5,6,7; type 3 cap 3; type 5 cap 5 + 11..15; type 6 existing library list; type 13 cap 2 + 3,25; type 15 cap 2 + 4, then tag 3 value 20 if `0x4dfad4+22*owner+20` (after `ReseauActif 0x42c3b0`, whose AL is discarded); type 16 cap 1 + 10; type 18 cap 1 + 16; type 20 cap 2 + 4, then tag 4 value 5 always. Units use tag 6 and need `TypeEnginEstRealisable 0x44228e` (byte `0x4e1934+26*owner+type`) nonzero |
| `celula_central_estrutura(estruturas, indice)` | `BatimentGetCase 0x41aee2` | AX u16 index (0..999), type `+8` 0..21. EDX/EBX are not inputs and are preserved. Result: u16 origin `+2` + (minrow + (maxrow−minrow)/2)·256 + mincol + (maxcol−mincol)/2 over the collision mask. Masks come from core's committed `pegadas_estruturas` (from this checkout), not a copy. Core agreed that economy owns this query |
| `HabitacaoConstrucoes.tornar_habitavel(mundo, indice)` | `BatimentHabitable 0x41cc70` | AX u16 index 0..999. `mundo` is core's physical world, whose `estruturas`/`unidades` must be the same objects. Returns `HabitacaoAplicada(indice, tipo, dono, celula, raio)`; `celula`/`raio` are `None` for types 17/9/12 |

**`BatimentHabitable` order:**
1. `definir_tecnologia(owner +4, type +8)`.
2. Types 17/9/12 store word `+0x84 = 200` and return.
3. Type 4 clears word `+0x78`. Type 3 with owner < 4 runs the existing `recalcular_recursos(owner)`; its inline body (`0x41cce2..0x41cd57`) is byte-equivalent to `BatimentCalculResource 0x423355`.
4. Radius R from jump table `0x41cc18`: 0→20, 2→10, 4→5, 10/11→7, 17/19/21→4, every other placed type 8.
5. `BatimentGetCase`.
6. `DecouvreTerrain 0x476851(cell, (R+3)&0xffff, owner)`.
7. `IllumineTerrain 0x476cb3(cell, R, owner)`, with owner re-read from `+4`.
8. Word `+0x84 = 200`.

Discovery and light are core's existing `descobrir_area`/`iluminar_area`, called directly.

**Gates and partial failures.**
- **Vision gates.** The call requires `R+3 <= visao_movimento.RAIO_DESCOBERTA_MAXIMO_VALIDADO` and `R <= RAIO_LUZ_MAXIMO_VALIDADO`, read from core at call time (fallback 10/8 until core publishes them; core's Stage 14 announces 23/20). Otherwise it raises `DependenciaHabitacao` at `0x476851` (call site `0x41cdb9`) or `0x476cb3` (call site `0x41cdca`). The light stop happens after discovery effects.
- **Owner bytes ≥ 4.** The original indexes core's per-owner grid pointers out of range (`0x507d78+4*owner` aliases the light grids). These raise at `0x476851`, after the technology no-op and any type-4 store.
- **Type bytes above 21.** These reach `BatimentGetCase` with an inherited EDI, so they are rejected with `ValueError` before any effect. So are an index ≥ 1000 and a world whose pools are not the same objects.
- **Division fault.** Type 3 with warehouses > 0 and per-warehouse capacity 0 raises `ZeroDivisionError` (the original `#DE` at `0x41cd55`) after the Bag reset.
- **No replay.** Effects are not transactional; never replay an entry after a stop.

**Cave identity (original tables only).** `BatimentGetTypeName 0x418af7` returns `0x495d8c + type*52 + 0x13`. InputGame calls it at `0x429ad1`/`0x42c141`. The table names type 2 `SANCTUAIRE` and type 3 `CAVE`. `BatimentInitCave 0x419112` copies each owner's type-3 count into the warehouse word `0x4dfb2c`, which the capacity code consumes. MONDE01's only serialized structure (owner 0, state 5, type 2, origin `0x0b0c`, Bag of the eight type-9 colonists units 3..10) is therefore the sanctuary, not the cave; its centre cell is `0x0c0e` (3086). The PT-BR `TEXTES.TXT` building list (Santuário/Armazém) agrees by position, but no code path adding 70 to a structure type was found, so it is only corroborating. The briefing text and the objective evaluator were not used.

**Erratum.** Original SBL names `0x44724a` `BagContientTroupe`. Stage 9–14 prose called it `BagVide`, which is `0x4470b9`. The API name `bag_vide` stays, with alias `bag_contient_troupe`; bytes, behaviour and earlier evidence are unchanged, and the identity-linked correction is in the Stage 15 manifest.

```sh
python3 -B pesquisas-paralelas/economia/capturar_habitaveis.py
python3 -B pesquisas-paralelas/economia/capturar_habitaveis_original.py   # original-only, before translation
python3 -B pesquisas-paralelas/economia/validar_habitaveis.py
python3 -B pesquisas-paralelas/economia/validar_habitaveis.py --emular
python3 -B scripts/check.py --domain economy
```

**Validation.** Both native runs compare whole structure, unit, technology-Bag, realizability, spell, capacity and resource buffers, core's full physical state (grids, minimap, objects, search, routes, experience queue), guard bytes beside every economy table, and the ordered discovery/light/minimap effect trace. Expected stops come from the declared gates, not from the Python exception.
- [Fresh native run on the current main gates](../pesquisas-paralelas/economia/validacao-habitaveis-emulada.json) (10/8): 20 tests pass without skips, mismatches or limits. **1,509 original entries** (192 predicate, 144 `BatimentHabitable`, 17 caller fragments `0x46c195..0x46c1a7`, 1,024 direct `BatimentSetTechnologie` for AL 0/3/4/255 × every DL, 132 direct `BatimentGetCase`) in 1,571 bounded segments with 62 preserved-CPU minimap resumptions. Outcomes: 53 full returns, 101 discovery-gate stops at `0x476851` (including actual MONDE01), 2 light-gate stops with lowered limits, 1 expected original `#DE` at `0x41cd55`.
- [Labelled diagnostic run with core's announced gates](../pesquisas-paralelas/economia/validacao-habitaveis-emulada-diagnostico-limites-23-20.json) (23/20, over core's current committed primitives): the same 1,509 entries in 1,967 segments (458 resumptions). All 17 caller fragments, including 12 actual-MONDE01 configurations (zero/one/random tables × fresh/seeded grids × cameras 0/1), complete to `0x46c1a7` with discovery 13 and light 10. 126 full returns, 15 owner-byte ≥ 4 stops, 2 lowered-limit light stops, 1 `#DE`. This run shows equality but does not replace the run after core publishes the constants.
- [Local mode](../pesquisas-paralelas/economia/validacao-habitaveis-local.json) replays every original-only capture: completed cases match all hashes, and gated cases keep the captured physical inputs and match the captured Bag/capacity/resource outputs.

**After core Stage 14 (main `7b7b96960cee0ec7868914e811f51b851fc27dba`).** Core now publishes `RAIO_DESCOBERTA_MAXIMO_VALIDADO=23`/`RAIO_LUZ_MAXIMO_VALIDADO=20` and `SOMA_VISAO_MAXIMA_INSERCAO=11`. The [fresh native run on these published gates](../pesquisas-paralelas/economia/validacao-habitaveis-emulada.json) passes 20 tests without skips or mismatches: 1,509 original entries in 1,967 segments (458 resumptions). All 17 caller fragments, including the 12 actual-MONDE01 configurations, complete to `0x46c1a7` with discovery 13 / light 10 and whole-buffer equality; there are 126 full returns, 15 owner-byte ≥ 4 stops, 2 lowered-limit light stops and 1 `#DE`. The pre-core run is preserved as `validacao-habitaveis-emulada-antes-core.json`. Local replay now reaches full hash equality for 21 of 22 original-only captures; the remaining one is the deliberate owner-4 boundary. The re-run [producer placement suite](../pesquisas-paralelas/economia/validacao-producao-colocada-emulada.json) has the same counts as Stage 12 (13 tests, 192 entries / 552 segments / 360 resumptions; 64 returns, 118 request stops, 8 pre-discovery stops, now at sum 12, and 2 import stops). Its fresh report is byte-identical to the committed one.

**Remaining limits.** Owner bytes ≥ 4 remain a named dependency at `0x476851`. Inherited technology/realizability tables at load time are explicit inputs: `TechnologieReset` zeroes them, but it is reached from `RechercheCalculNew`, not `MissionLoad`, so the whole-load oracle must supply the real values. `PlaceBatiment`/`BatimentModifyMap` (core) and the loop itself (missions) are not part of this provider. Other callers of `BatimentHabitable` (`BatimentConstruction 0x41d000`, `BatimentLogeEngin 0x41fa81`) are not composed. `BatimentInitCave` is already reconstructed (`EconomiaConstrucoes.inicializar_armazens`) and validated over all 38 ETA prefixes. Its composition into the mission tail after `EnginInitTechnologie 0x441459` is the proposed Stage 16.

## Economy load tails of `MissionLoad` (Stage 16)

[cauda_carga.py](../pesquisas-paralelas/economia/cauda_carga.py) provides the economy-owned initializer calls of the load tails. The [original-byte inventory](../pesquisas-paralelas/economia/evidencias/cauda-carga.json) exports 14 intervals with hashes. The [original-only captures](../pesquisas-paralelas/economia/evidencias/captura-cauda-carga-original.json) were committed (`8d0f2a9`) before translation.

**Tail order from original bytes.**

| Loader | Tail after `FileClose` |
|---|---|
| `MissionLoad 0x46c5aa..0x46c5d6` | `MissionPlaceTerrain` (missions), `EnginInitTechnologie 0x441459`, `BatimentInitCave 0x419112`, core `Engin_RetrieveExperimente 0x441623`, `PlayerRetrieve 0x46df41`, ai-runtime `iaReset 0x47f36e` (AL = byte `[esp+0x128]`), `MarcheResetAll 0x46027c`, AL = 1 |
| `MissionLoadName 0x46c973..0x46c998` | `MissionPlaceTerrain`, `EnginInitTechnologie`, `BatimentInitCave`, `RechercheCalculNew 0x47150f`, `iaReset` (AL = byte `0x496fe4`), `MarcheResetAll`, AL = 1 |

Missions composes the tail; economy supplies the calls below.

**`RechercheCalculNew 0x47150f..0x4716fe` is economy-owned and not reconstructed here.** It calls `TechnologieReset`, `BonusReset`, `InventionSetEffet 0x470f98` and missions' `MissionGetNum`, and copies 16 bytes per owner `0x508134 → 0x5080f4`. It is reached only from `MissionLoadName`, not from MONDE01's `MissionLoad`.

| API (`CaudaCargaEconomia(habitacao, ciclo_mercado, *, rede, jogadores_guardados)`) | Original | Contract |
|---|---|---|
| `inicializar_tecnologia_unidades()` | `EnginInitTechnologie 0x441459` | `definir_tecnologia_unidades(owner)` for owners 0..3 ascending |
| `definir_tecnologia_unidades(jogador)` | `EnginSetTechnologie 0x4411e1` | AL owner u8, protected 0..3 (the original indexes the pointer table without a check). It rebuilds three of that owner's unit-order Bags (`propriedade.ordens`, the `[0x4e19b8]` arrays of 26 × 104 bytes); each inline reset equals `BagInit` and keeps bytes `+0x60..+0x65`: the unit-7 Bag gets capacity 22 and tag 3 for each structure type 0..21 except 20 that is realizable; the unit-14 Bag gets capacity 1 and tag 7 value 6; the unit-8 Bag gets capacity 4 and tag 2 values 0..3 |
| `estrutura_realizavel(tabela, rede, jogador, tipo)` | `TypeBatimentEstRealisable 0x418a93` | AL owner, DL type (protected 0..3/0..21). A nonzero `ReseauActif` byte (`0x4e0730`) makes types 8/12 return 0; otherwise the result is byte `0x4dfad4 + 22*owner + type`. EBX is preserved |
| `inicializar_cavernas(mundo)` | `BatimentInitCave 0x419112` in tail position | Delegates to the existing `EconomiaConstrucoes.inicializar_armazens`. Its 88-byte count table must be the same object as core's world table at `0x49a070` (core's raw name `realizaveis_estruturas`; `BatimentResetAll` zeroes it, `BatimentInitCave` fills it with per-owner, per-type counts of structures whose state `+5` is nonzero), and the structure pool must be the same object. The type-3 (CAVE) count goes to the warehouse word `0x4dfb2c+6*owner` and the type-18 count to `0x4dfb4c+owner`; byte counts wrap |
| `recuperar_jogadores()` | `PlayerRetrieve 0x46df41` | For each of the four 20-byte players, first byte `+6` (alliance mask), then bytes `+0x0c..+0x13` (four signed-16 sympathies), copied from the 80-byte source table `[0x5080ac]` (written by `InitPlayer`/`LoadPlayer`/`PlayerStore`) into the live table `[0x5080a8]` (`Mercado.jogadores`). Nothing else changes |
| `resetar_mercado()` | `MarcheResetAll 0x46027c` | Exactly the committed `CicloMercado.resetar_todos`: for each player in ascending order, the seven stores `0x4e2e7c=0`, word `0x4e2930=0`, `0x496f8c=255`, `0x4e292c=1`, `0x4e2928=0`, word `0x4e2940=0`, word `0x4e2938=0`. No difference was found; it now also passes in tail position |

The constructor uses its buffers by identity. It requires the market and the structures to share one resource table, and checks lengths: unit-order Bags 10,816, `rede` 1, source and live player tables 80 each, counts 88 and 4. All of these, including the realizability tables, are inherited load state for the whole-load oracle; none is defaulted. A `ValueError` from a protected domain is raised before that call's stores. The calls are independent single entries; missions must not replay them.

```sh
python3 -B pesquisas-paralelas/economia/capturar_cauda_carga.py
python3 -B pesquisas-paralelas/economia/capturar_cauda_carga_original.py   # original-only, before translation
python3 -B pesquisas-paralelas/economia/validar_cauda_carga.py
python3 -B pesquisas-paralelas/economia/validar_cauda_carga.py --emular
python3 -B scripts/check.py --domain economy
```

**Validation.** The [fresh native run](../pesquisas-paralelas/economia/validacao-cauda-carga-emulada.json) passes 11 tests without skips, mismatches, faults or limits. **435 original entries** in 451 bounded segments, 16 of them minimap resumptions:
- MissionLoad tail fragments: 16 runs of `0x46c5af..0x46c5b9`, 19 of `0x46c5be..0x46c5c3`, 19 of `0x46c5d1..0x46c5d6`.
- MissionLoadName pair `0x46c978..0x46c982`: 3 runs.
- 2 Stage 15 caller fragments, chaining habitation into the tail.
- Direct entries: 24 `EnginSetTechnologie` (owners with garbage high register bits) and 352 `TypeBatimentEstRealisable` (4 owners × 22 types × 4 network bytes).

Fixtures include actual MONDE01: its loaded structure, header and units; zero, one and random realizability tables; network bytes 0/1/0x80; and two runs after its Stage 15 habitation. Also covered: random 1,000-record pools with owners 0..3/4/200/255 and states 0..255, and wraps of 300 caves and 257 heliports. Each run compares whole structures, units, technology and unit-order Bags, realizability, counts, capacities, resources, both player tables, the seven market buffers, core's physical state and guard bytes. The [local mode](../pesquisas-paralelas/economia/validacao-cauda-carga-local.json) replays all seven original-only captures to full hash equality.

On MONDE01 the tail counts one owner-0 type-2 sanctuary and no cave. All four owners' warehouse words become 0 and the type-18 counts become 0.

**Remaining.** `RechercheCalculNew` (MissionLoadName only) is not reconstructed. Core's `Engin_RetrieveExperimente 0x441623` and ai-runtime's `iaReset 0x47f36e` are not part of this provider.

## Stage 17 recovery audit: natural production inventory only

Recovered local commit `3868ce5d6f3cfd82c577595e528d8e803fe81e19` remains the original-byte inventory. It is not reachable from the observed fetched main `8810b3730a0fb788af3eac2b447dea65372f597f`. Stages 15/16 habitation and economy load tails are already integrated; they must not be reimplemented. The resumed worktree was clean, its prior history was preserved, and `scripts/workstream.py start economy` resumed that same branch without resetting or merging over it.

The [additive static audit](../pesquisas-paralelas/economia/evidencias/producao-natural-auditoria-retomada.json) checks the intact EXE, SBL and INI identities, all ten code intervals (2,048 bytes, 588 decoded instructions), all three jump tables (65 entries), the static structure-type table and all five predecessor hashes. Every byte, decoded listing and table entry matches. Existing evidence/exporters are unchanged. This is new static verification, **not** an original execution capture, differential run or complete natural-production implementation. No x86, Ghidra, domain gate or integration ran during this light audit.

Contract clarifications from original instructions and committed providers:

- `InitRecruteTroupe` accepts structure types 1/2/5/13/15/16/18/20. The selected `BatimentNextEtape` branch advances only 1/2/13/16, after its habitation predicate. Starting a request and advancing the selected structure branch are separate entry points. The two inventoried input/AI fragments prove those direct calls; no complete indirect-call graph is claimed.
- `RechercheDecalageSortie` reuses actual core `CalculPosition`, then searches dy before dx, skips the centre, and tests raw `[0x507da8][cell] & 0x01`. Bounds are global 0..255 coordinates, independent of playable map width/height. Types 9/12/17 take uninitialized-local paths and stay outside this protected recruitment domain.
- The search writes a word at local `+8`, later reads a dword at `0x41d2a6`, and may carry inherited high stack bits into full EAX. The actual caller at `0x428640` consumes AX only. Capture low-word behavior and the original registers; do not invent a stable full-EAX value.
- Reuse the already integrated `construcoes_habitaveis.celula_central_estrutura` and `estrutura_habitada`; no duplicate footprint or Bag algorithm is required. Existing core light removal is a candidate for exact radius-8/10 caller validation. Core commit `a572e8c` contains the separately pending `BatimentModifyMap` provider; it was inspected through immutable Git objects and must reach main before consumption. The pending initializer audit does not depend on that provider to integrate its inventory.
- Structure selections at `0x495be0` must be explicitly shared between the economic recruitment object and physical world. Raw attributes at `0x507da8` are a different pointer from economy/core objects at `0x507d74`. Use explicit loaded tables and buffers by identity.
- Existing MONDE01-derived fixtures use its real header/serialized records together with declared synthetic inherited grids/tables. They are not a fully initialized post-`MissionLoad` state. A true whole-load image remains M1 work; missing state is never silently zeroed. The known FFFFFFFF sound handle keeps genuine `PostSound` pending.

Before any later translation, the proposed original-only capture batch has **28 scenarios /29 top-level original entry calls**: fourteen exit-search cases (all eight accepted start types plus blocked-first, all-blocked fallback, two global corners, playable-map/global-bound distinction and an alternate upper-stack seed); four complete initializer cases (accepted MONDE01-derived request, insufficient balances, busy building, ineligible building type); six dispatcher cases (four supported inhabited types and empty type-1/type-2 branches); four empty cleanup fragments (types 1/2/13/16) ending before `BatimentModifyMap` at `0x42114e`. The accepted initializer scenario also executes one original dispatcher update on the same live buffers, accounting for the extra entry. Preserve exact registers, whole loaded world/economic/selection/queue/tables, guards and ordered effects. No engine subcall is replaced. These captures are planned, not executed; reject undeclared stops/limits rather than increasing budgets or filling in unknown effects. Broader implementation comparisons follow only after this evidence is committed and the coordinator schedules translation.

The current reviewable stage is inventory recovery/audit only. Its scheduled completion is the economy domain gate, owned diff review/commit, the locked `scripts/workstream.py integrate economy`, fresh delivered/feature/merge ancestry verification and a static byte replay on committed main. Those domain/integration operations await the coordinator's serialized heavy slot. AI message 0x46/town message 3, natural request dispatch, sound insertion, whole mission runtime, transport and work remain separate gaps. No next game implementation has begun.

## Light M1 audit: economy delegates required by `IaReset`

This audit is against committed main `e9f5dbd33972344e37db3a93be1aec9c115a88bf` and AI's feature-only adapter inventory `428f54cc075cb94ab0ffba5595dfed42f09f7d38`. Its [additive static record](../pesquisas-paralelas/economia/evidencias/contratos-economia-iareset-auditoria.json) contains five complete intact-original getter/setter bodies and hashes of the five inspected committed source files. No provider implementation, native execution, domain/common gate, Ghidra or integration was performed in this light wave. The prior Stage 17 inventory and recovery notes remain preserved and unintegrated. Natural production and transport are deferred; their earlier capture plan is not active work in this M1 callback audit.

| Original callback | Genuine existing delegate or minimal missing contract |
|---|---|
| `PlayerGetType 0x46d817` | Existing `Mercado.tipo_jogador(player)`: player low u8; 0..3 returns raw live player byte `20*player+1`; 4..255 returns 2. Returns the consumed AL value, no stores. Do not reject player 4 or substitute human control bytes. |
| `GetRessource 0x467670` | Existing `Economia.consultar(player)`: player low u8, protected 0..3; returns `(food, stone, parts, 0)` with unsigned u16 totals from record `+2` at resource IDs 1/2/0. No RMI or stock substitution, no mutation. Native writes four word outputs; the AI delegate consumes the tuple rather than a general aliasing-output-pointer emulation. |
| `BatimentGetPlayer 0x41a08c` | Existing committed bridge `ataque_vivo.batiment_get_player(structures, index)`: index low u16, protected 0..999, exact flat 276,000-byte live pool; returns raw byte `index*276+4`, including owner 200/255. No state/owner filtering, mutation or full-EAX guarantee. Its code matches the consumed-AL original contract, so a duplicate getter is unnecessary. The adapter still needs fresh joined validation. |
| `RechercheGetNiveau 0x4717c2` | Missing standalone economy delegate. Player AL u8; branch DX u16. Reads **one unsigned byte** at `0x5080f4+16*player+branch`, returns it zero-extended in AX, preserves EBX and EDX, writes nothing. Proposed protected M1 scope: player 0..3 and branch 0..3, exactly the four IaReset queries. Original has no such index guards. The RET ends at `0x4717de`; the following two zero bytes before the next SBL symbol are padding. |
| `RechercheSetBranche 0x470b37` | Missing standalone economy delegate. Player AL u8, branch value DL u8 (all 0..255 values). Writes only byte `0x5080f8+16*player`; every other research byte remains. No progress reset, technology/bonus update or balance effect. Proposed protected player 0..3. The adapter ignores its result; native EAX becomes `(player & 255)*16`. |
| `BatimentExiste 0x41a735` | Missing standalone owner delegate: AX index u16, protected 0..999; read byte `+5`, return EAX 1 if nonzero, else 0. States 3/4/5 remain true. Habitation or destruction predicates are not substitutes. No stores. |
| `BatimentGetType 0x41a4f4` | Missing standalone owner delegate: AX index u16, protected 0..999; return raw byte `+8`, no normalization by state/type range and no stores. The current transport query only compares that type internally and cannot serve as this standalone getter. Upper native EAX bits contain address-derived data; only consumed AL is the delegate contract. |

All three structure queries address the same original pool `0x49a0c8..0x4dd6e8` and preserve EDX. Their protected pool bounds are owner API guards, not native failure returns. Use the actual live pool, not a list of copied records.

**Backing-buffer requirements.** `Mercado` copies the supplied 80-byte player table and `Economia` copies the supplied 128-byte resource table in their constructors. Construction is not alias binding. Use the existing mission-owned provider objects and map their actual backing buffers into AI `MemoriaDeclarada`: the live `[0x5080a8]` pointee must be the same range as `mercado.jogadores`, and `0x4e2ea8..0x4e2f28` must be exactly `economia.memoria`; the market must retain that same `Economia` instance. Mounting a memoryview preserves its backing allocation; byte equality alone does not prove aliasing. The separate inherited research table is 64 bytes at `0x5080f4..0x508134`, not the spell availability/invention tables at `0x508f30`/`0x508f44`. Its actual load provenance must be supplied; no constructor-zero table is a mission initialization claim. A real branch-setter store must be visible to AI through that same range immediately, without a second copy/write-back.

The AI adapter accepts `sitio=call_address` for tracing and delegates actual argument values to owner methods. Existing `tipo_jogador`/`consultar`/combat getter do not accept this keyword directly. This metadata wrapper must not copy their rules. Type-2 player research is a real required path: original `IaReset` calls the getter at `0x47f43f` and setter at `0x47f4ca`. All-human fixtures cannot replace it.

**Minimal scheduled follow-up.** First integrate the reviewed pending inventory/audit stage under the coordinator's exclusive heavy grant: economy domain gate, complete owned diff/commit, shared-lock `integrate economy`, fresh ancestry and relevant committed-main replay. Only then schedule four missing leaf providers (research query/setter and structure existence/type), reusing the three existing delegates. Before translating them, capture 14 original-only scenarios /26 leaf entries: four research reads (owners and branches distributed across 0..3 with values 0/1/128/255 and dirty upper register bits), four research writes (owners 0..3 with DL 0/3/128/255), six structure cases (edge indices 0/999 with state 0/3/5 and deliberately varied raw owner/type bytes), each executing all three real structure getters. Subsequent bounded differentials should cover all 4×4 research indices, all 4×256 setter bytes, states 0/1/3/4/5/255 and whole-buffer preservation/aliasing. AI owns the fresh full `IaReset` adapter comparison with actual type-2 controls, genuine callbacks and declared remaining stops. No heavy run or next implementation starts without scheduling.

### Ownership correction after coordinator review

The preserved original-byte audit remains unchanged. The earlier phrase "four missing owner leaves" was a dependency list, not authority to implement all four in economy. The existing Stage 15 contract in this handoff (structure habitation) explicitly leaves `BatimentExiste` with **Missions**. Coordinator confirmed that Missions will expose its single validated reusable getter in Stage 11, based on original scan captures committed as `ed0172a`; wait for its integrated callable contract. Economy must not implement or duplicate it.

The separate next economy stage therefore contains only **three new leaves**: `RechercheGetNiveau`, `RechercheSetBranche` and `BatimentGetType`. It reuses the committed combat `BatimentGetPlayer`, while AI consumes the Missions existence getter after publication. The ignored scratch was adjusted without running x86: its 14 scenarios now contain **20 original calls** (four research reads, four writes, six structure cases executing only GetPlayer/GetType). Original byte provenance for all five inspected functions stays frozen; there is no new or altered runtime behavior.

This correction and the prior checkpoint remain subject to the pending economy domain/common integration gate. No capture, domain test, integration or new game implementation has run in this light slot. Coordination goes through the coordinator while the active executor slots are full; no idle AI executor is awakened for this correction.

### Original-only observations for the three M1 economy leaves

After the inventory integrated at main `2456848e57c1fbb63f3590023e424012c0916d3e`, capture source `ff02f8accddff16934155d5c65dd3bdd8814e42e` was committed before any translation. The [original-only capture](../pesquisas-paralelas/economia/evidencias/captura-consultas-reinicio-economia-original.json) records14 scenarios/20 real returns:4 research reads,4 single-byte branch writes,6 existing owner queries and6 structure-type queries. Complete registers, research bytes, whole structure-pool hashes, guards and observed stores are retained. No engine call/result is replaced. This is new original evidence, not a reconstructed-query comparison or whole-mission proof. The three new leaves remain unimplemented at this capture checkpoint; native checks and integration of their later implementation require a new serialized grant. The source/evidence remain pending that next stage's final integration.

### Three live-buffer economy queries for the IaReset adapter (implementation)

`consultas_reinicio_economia.py` now implements only the three missing economy leaves, after source commit `ff02f8a` and original-capture commitment `85525e8`. It imports no game provider and copies no input. Missions' existence getter and combat's existing owner getter remain separate reusable delegates; neither is duplicated.

| Callable | Input and result |
|---|---|
| `nivel_pesquisa(pesquisa, jogador, ramo)` | Exact live 64-byte research view at `0x5080f4`; player truncates AL u8, branch DX u16, protected 0..3 each. Return the unsigned byte at `16*player+branch` as semantic AX. Read-only views are accepted. No mutation. |
| `definir_ramo_pesquisa(pesquisa, jogador, ramo)` | Same exact writable research view; player AL u8 protected 0..3; all DL bytes retained. Store exactly `view[16*player+4] = ramo & 255`, preserving every other byte. Return None; no progress, technology, bonus or balance effect. |
| `tipo_estrutura(estruturas, indice)` | Exact live 276,000-byte flat pool; index AX u16 protected 0..999. Return raw unsigned byte `276*index+8`, including state-0 structures and unknown type values. Read-only views are accepted; no mutation or upper-EAX contract. |

Views must be one-dimensional contiguous B/b byte buffers of the exact size. Signed-byte views are cast to unsigned without copying. The setter rejects read-only memory before storing; all protected-domain checks precede its sole write. There are no constructors, cached values, default buffers or copy-back. Mutations through a caller's sliced arena are immediately visible in that same underlying allocation. These owner functions do not accept the AI adapter's `sitio` tracing keyword; the adapter supplies only actual arguments and preserves its own tracing metadata.

Local targeted replay (`python3 -B pesquisas-paralelas/economia/validar_consultas_reinicio_economia.py`) passes seven executed tests with one optional native method skipped. All 14 new-leaf Python calls match the frozen observations' consumed values and whole research/structure/guard state; six preexisting GetPlayer observations remain provenance for the genuine reused bridge. Other tests cover source-before-translation identity, high input bits, protected invalid indices, signed/read-only/strided/multidimensional/incorrect-size buffers, single-byte write-through and later external mutation. No new x86 run, domain/common gate or integration occurred after the heavy release. The dedicated fresh native test is bounded to the same 20 original returns, with exact registers/stores/buffers, and requires a separate grant. The older aggregate runner only gains the real native bench counter for a future explicit run; no historical aggregate was rerun.

The module is implemented and locally replayed, but not yet freshly validated against native or integrated. Whole-IaReset binding, actual mission research-state provenance and full M1 behavior remain outside this leaf stage. Completion must fit the 18:25 development cutoff and use a separately granted narrow native/domain/integration window.

### Stage 18 fresh narrow native result

On the renewed final exclusive lease, [fresh native validation](../pesquisas-paralelas/economia/validacao-consultas-reinicio-economia-emulada.json) passes8 tests with no skips/errors/failures:20 original calls return normally and exactly match the preserved capture's complete registers/stores/buffers/guards, with14 translated leaf results checked. No broad matrix, limit or unknown-effect substitution occurred. The earlier immutable original-only capture remains unchanged. The required economy check passes432 tests/197 optional skips. Frozen runtime4181758 is unchanged; locked integration and committed-main focused replay are the remaining delivery steps at this result checkpoint. This closes these three leaf-provider dependencies only; it does not establish a fully bound IaReset or M1 load.
