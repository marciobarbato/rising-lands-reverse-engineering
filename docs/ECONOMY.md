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

Stage 9 selects the economy-owned cleanup prefix at `0x420fb7`, only after the still-pending experience/placement/movement/request caller has completed. Protected building types remain 1/2/13/16. Original type2 first runs `BagVide` (`0x44724a..0x4472d3`), a capacity-scanning unit-type predicate despite its symbol; a false result falls through to the existing type9 `BagContient`. Other supported types query type9 directly. A retained unit sends control to the common selective reset, then the unit-message call at `0x4211d3`. Without one, types1/2 reset first; all four then reach terrain query call `0x42110c`, with raw parameter10 for type2 and8 otherwise. Reuse the actual committed core `resetar_estrutura` for the identical inline reset sequence. New validation must be labeled an **isolated cleanup continuation** with explicit original frame/register inputs, not a whole production run or a bypass of the missing preceding calls. No terrain/AI-message effects are skipped or guessed. This inventory precedes implementation.

## Isolated production cleanup continuation

`limpeza_saida.retomar_limpeza_saida(producao,mundo,pedido)` consumes only an explicit handoff at **`0x420fb7`**, after the original experience/placement/movement/conditional request calls. The current complete production provider does not reach this address; this is an isolated continuation contract, not permission to bypass those dependencies. It accepts u16 building/output indices (protected 0–999/0–799), supported building types1/2/13/16, identical live economy/core structure and unit objects, and the existing loaded recruitment model. Wrong handoff, indices, type or shared identity fail before mutation.

Complete `bag_vide(recrutamento,indice)` reconstructs `BagVide [0x44724a,0x4472d3)`. It scans the Bag's u16 **capacity**, restricted to0–30, and only tag1 entries. It returns at the first referenced unit whose u8 type is **not** in `{3,11,12,13,14,15,16,17,25}`; all other bytes, including26–255, pass. A live count of zero does not prevent a tagged capacity entry from being read. References are protected0–799 only when encountered; a successful early return does not read/reject later references. This query checks no unit state/owner and mutates nothing.

Cleanup type2 first runs that predicate; on false it falls through to the existing `Producao.contar_unidades(indice,9)` capacity query. Other supported types query type9 directly. A true retention result invokes the actual committed core `ciclo_estruturas.resetar_estrutura`, then returns frozen `LimpezaSaidaTropa(indice,unidade,0x4211d3,0x4829c8,70)`, before the unit AI message. On false, types1/2 invoke the same core reset first; types13/16 have no reset yet. All four return at `0x42110c`, before `BatimentGetPosition 0x41aee2`, with raw EDX parameter10 for type2 and8 otherwise. The subsequent original `0x476e82` terrain call and AI messages remain pending. Type/owner/state, unit Bags, balances and unlisted structure bytes retain the original effects; resetting progress is not a completion event.

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
