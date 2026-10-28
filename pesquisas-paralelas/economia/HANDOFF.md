# Economy handoff — 2026-10-28

Chat: `01a18262-c6d5-7cd3-80fa-8431bf5f2657` (Economy and Production). Worktree: `/Users/marcio/git/Rising Lands/worktrees/re-economy`. Branch: `feat/re-economy`. Organization base: `6634be3af2d255846a847d8aa21ad4edf1cdb589`. Implementation commit: `f5a5e9b` (`Reconstruct troop completion preparation and cargo credits`); the following handoff commit and serialized integration result are identified in the completion chat. Only economy-owned paths changed.

## Delivered boundary

`saida_tropa.SaidaTropa(recrutamento).preparar(indice, direcao)` reconstructs the economic prefix of original `SortieTroupe` (`0x420E4C`) through the real dependency stop at `CalculPosition` (`0x420698`, call `0x420F5A`). It detaches an existing type-9 colonist and unloads its carried stone and food. It returns `None` below the unsigned completion threshold, otherwise an immutable `PreparacaoSaidaTropa` pending record. This is not a completed spawn or a world allocator.

Read [the complete maintained contract](../../docs/ECONOMY.md) for offsets, order, and validation scope. Inputs are low-u16 building index and low-u8 direction. Protected data consists of 1–1,000 building records of 276 bytes, 800 unit records of 276 bytes, requested types 0–25 in 50-byte type records, Bag count/capacity 0–30, and deposit owners 0–3. All direction bytes are passed through. Progress is u32; recruitment time is u16 multiplied by 100. Activity `+0x74` and building state `+5` are not tested by this entry point. Time zero/progress zero prepares a unit if the Bag contains one.

## Mutations and failure order

1. Below threshold: no mutations and no world request.
2. At threshold: `BagRetire` mode 1 removes the first live tag-1 reference with type byte 9 from the building Bag at `+0x0C`. It decrements Bag `+0x66` modulo 65,536, compacts values/tags, clears the former last slot, and decrements live count. Other units and opaque bytes remain.
3. `EnginGetBag` resolves that existing unit's Bag at unit `+0x0A`. `BagContient` mode 2 scans capacity, whereas removal scans live count. Remove every carried entry tagged 2/value 2, crediting **2 stone per removed entry** through `BatimentAjouteMatiere`, then tagged 2/value 1, crediting **1 food per entry**. The returned entry value becomes the credit quantity. Resource ID 0 and other tags remain. Bag `+0x66` also decrements for resource removals, preserving u16 wrap.
4. Each cargo removal precedes its deposit. Existing capacity/excess/RNG semantics remain in effect. `ZeroDivisionError` preserves the removed colonist, removed cargo, and already-applied credit; `RetiradaColonoPendente` preserves removals before its dependency. Neither produces a successful pending-position result, and neither rolls back.
5. Successful preparation returns building index, direction, existing unit index, current requested type snapshot, and dependency address `0x420698`. No world callback executes; type, progress/activity, exit fields, and post-conversion cleanup/messages remain untouched.

Protected `ValueError` cases are API domain limits, not observed original returns: missing colonist, invalid referenced unit, out-of-buffer building/type, count/capacity above 30, or a matching resource tag beyond live count when removal fails. Invalid unit Bag state is checked after building removal. Malformed original state can instead read outside the modeled pool or fail to terminate. Do not retry preparation after a pending handoff or failure: it has already consumed entries.

## Requested core continuation

The smallest next core operation is `CalculPosition(AX=building u16, BL=direction u8) -> AX=position u16`. At the original call boundary EAX is the zero-extended building index, EBX the zero-extended direction, ECX zero, ESI the zero-extended existing unit index, and EDI the building pointer. The test harness checks the first four values and compares all protected buffers. No guessed geometry is supplied.

Captured original context then performs these calls in order:

| Caller | Callee | Visible arguments |
|---|---|---|
| `0x420F69` | `EnginSetType`, `0x457B87` | EAX=existing unit, EDX=zero-extended position, CL=building `+0x7B` reloaded after position callback |
| `0x420F75` | `EnginAddVie`, `0x457122` | EAX=unit, EDX=1,000 |
| `0x420F7C` | `EnginResetFatigue`, `0x4530FD` | EAX=unit |
| `0x420F85` | `EnginSetExperimente`, `0x44FE42` | EAX=unit, EDX=position |
| `0x420F8C` | `SetSortEngin`, `0x445FBC` | EAX=unit |
| `0x420F99` | `SetDeplaceEngin`, `0x4457D3` | EAX=unit, DX=building `+0x7C` |
| `0x420FB2` | `EnginAsk`, `0x440D5E` | Only when building owner equals byte `0x508041`; EAX=unit, EDX=6, EBX=0 |

These are observed caller arguments, not newly verified callee behavior. All are outside this implementation. In particular, the pending record's type is only a boundary snapshot: an eventual continuation must preserve the original reload after a callback that could mutate the building. Economy communicated this contract directly to Core and the coordinator under the research-round authorization. Core's selected structure-pool slice is independent and does not provide this unit continuation this round.

## Original evidence

- Original Brazilian `RISING.EXE` SHA-256: `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
- Original `RISING.SBL` SHA-256: `c3a5411255847d36161aea1aeef06ab280265c55fa5a6626cfeb7bab523cc627`.
- Prefix `[0x420E4C,0x420F5F)` SHA-256: `708fbdb1555a8562c5248924e749e537e4fdafa6f13ba98968612c9ffbf285ad`.
- Additive [evidence manifest](evidencias/saida-tropa.json) records exact bytes and hashes for prefix, return path, `EnginGetBag`, and unimplemented world-call context; it also records `BagContient` jump-table bytes at `0x44719C` and supporting routine hashes. The original prefix/support instructions run unpatched. No callbacks are mocked as successful original calls.
- `capturar_saida_tropa.py` checks the original hashes and only writes these new owned captures. It leaves predecessor evidence, frozen releases, source media, and PT-BR content unchanged. Other-owner code was consumed from the committed organization baseline, never another live worktree.

## Actual validation

All commands ran from the feature worktree above:

```sh
python3 -B pesquisas-paralelas/economia/capturar_saida_tropa.py
python3 -B pesquisas-paralelas/economia/validar_saida_tropa.py
python3 -B pesquisas-paralelas/economia/validar_saida_tropa.py --emular
python3 -B scripts/check.py --domain economy
```

- Capture: 4 new intervals and 5 support hashes; deterministic regeneration produced no evidence changes.
- New local suite: 15 discovered tests, 9 passed and 6 optional differential methods skipped; zero x86 executions.
- New original-x86 suite: 15 passed, no skips/failures/errors; **426 bounded executions**, consisting of **390 position dependency stops**, **24 early returns**, **4 deposit dependency stops** at `BatimentRetireColon`, and **8 expected division exceptions** at `0x423501` after mutation. There are 418 declared stops, zero expected limits, and no complete spawn executions. See [fresh x86 report](validacao-saida-tropa-emulada.json) and [local report](validacao-saida-tropa-local.json).
- Differential scope: full economic/capacity/building/unit/terrain/recruitment buffers and guards; observed deposit calls and order; all 26 requested types and 256 directions; unsigned progress boundaries, type-time zero, first matching/duplicate units, capacity versus live count, compaction, counter underflow, partial exceptions, excess deposits, and untouched seeded bytes. Fixtures are synthetic memory states, not a live mission capture.
- The first sandbox x86 invocation exited with code 132/SIGILL before finishing a test. The approved execution context with Unicorn JIT available passed; no OS protections or original bytes were changed.
- Domain gate: **229 tests**, **101 optional differential methods skipped**, zero failures/errors; documentation links passed. The 214-test/54,871-execution predecessor report remains historical and was not rerun.
- The complete owned diff and whitespace check were reviewed before committing. Integration must run `python3 scripts/workstream.py integrate economy` from this clean feature worktree; its common-lock candidate checks and non-force main push are reported in the completion chat. Do not amend this branch merely to embed its own resulting merge hash.

## Remaining gaps

World position, unit type conversion, life/fatigue/experience/task effects, the remainder of `SortieTroupe` cleanup/messages, full spawn/exit/balloon flows, other production paths, general transport credit, and higher-level market callers remain open. This slice does not add navigation, structure allocation, rendering, a live mission dispatcher, or a complete playable game. Existing progress, resource IDs, signed/fixed-width behavior, x87 rounding, and previous explicit dependencies remain unchanged.

## Sequential continuation inventory and selection

Slice 1 is integrated at main merge `1394669620a2d256b1abb9a9f0741f29728ee7eb`; pushed feature merge `d990121881db46eeddd348d44fc19b9bf77f19e5`. The common candidate gate passed 656 tests with 289 optional methods skipped. The worktree was clean before resuming it through `workstream.py start economy` and merging updated `origin/main`.

The maintained manual now inventories remaining component evidence and dependencies. Highest-value next independent closure: resource-only `MarcheOrdreEchange` (`0x461BEA`) through original `MarcheEchangePrend` (`0x461621`) and `MarcheEchangeDonne` (`0x46189A`). Zero unit rows permit original loop execution without inventing world effects. Unlike `VideMatiere`, these callers skip zero resources and consume the proposal row after each successful nonzero credit. Nonzero unit paths and original partial failures must remain explicit. Implementation and original comparisons of this slice are complete as recorded below; serialized integration remains the final step.

## Stage 2: consuming resource-only market exchange

`OrdemMercado(mercado, mundo, aceites=...)` adds the complete resource-only `MarcheOrdreEchange` body `[0x461BEA,0x461C4F)` and its original `MarcheEchangePrend`/`MarcheEchangeDonne` caller paths. Inputs are low-u8 players 0–3; four approval bytes at `0x4E2968`; quantity rows are u16, stride 6 for three resources or 52 for 26 unit types. Economic memory/provider identity is enforced. See the maintained manual for the full contract.

The first player's approval toggles `0 -> 1`, any nonzero `-> 0`. A nonzero second-player approval OR first-player type 2 triggers Prend, then Donne, then clears both approvals. No indicator, contact, alliance, price, sufficiency or new-own-approval check occurs. Aliased indices observe the newly toggled byte. The new bool return is a Python diagnostic, not a recovered original success flag.

Both calls consume the SECOND argument's proposal row. Prend checks offered units, then transfers nonzero offered resources from second player to first. Donne checks requested units, then transfers nonzero requested resources from first to second. IDs iterate 0/1/2. Zero entries skip type/debit/recalculation. Type-1 donors debit through the existing building routine; other types skip debit. Each direct destination credit writes total u16, clears the consumed row entry, then writes RMI u16; credits wrap with no capacity/clamp. Same-player aliasing reads balances after debit. Direct Prend/Donne APIs leave approvals untouched.

Nonzero units raise `TrocaUnidadesMercadoPendente` at the first positive type: `0x46166B` for Prend, `0x4618DF` for Donne. That records both players/type/u16 quantity/phase/address while preserving prior mutations. These world-unit paths are explicitly unsupported. A requested-unit stop retains the completed offered-resource leg. Division exceptions retain debit and prior consumed rows/legs while leaving the failed row entry unconsumed and approvals uncleared. No caller rollback or fake unit callback is added.

Additive `evidencias/ordem-mercado.json` and five instruction listings contain original bytes, exclusive intervals, SHA-256 values, and provenance; original EXE/SBL hashes remain those recorded above. Capture includes unit bodies for evidence, not an implementation claim. Original zero-unit branches and real debit/recalculation instructions run unpatched to shared returns/checkpoints.

Actual new commands and outcomes:

```sh
python3 -B pesquisas-paralelas/economia/capturar_ordem_mercado.py
python3 -B pesquisas-paralelas/economia/validar_ordem_mercado.py
python3 -B pesquisas-paralelas/economia/validar_ordem_mercado.py --emular
python3 -B scripts/check.py --domain economy
```

- Capture: five original intervals; no predecessor evidence changed.
- Stage local suite: 18 discovered, 10 passed, 8 optional differential methods skipped; no x86 executions.
- Stage original suite: 18 passed, no skips/errors/failures; **2,357 bounded executions** = **2,241 returns** (including non-executing approval gates), **104 unit dependency stops**, **12 expected division exceptions at `0x423635`** after mutation. There are 2,345 declared stops and zero expected limits. See `validacao-ordem-mercado-emulada.json`.
- Differential buffers: complete economic/capacity/building/terrain/market/player memory plus guards and a continuous `0x4E2900..0x4E3000` neighbor window. Captured original write order proves total, row clear, RMI; debit call arguments/order are checked. Fixtures cover all approval-byte values, player pairs/aliasing, types, resource zeros, wrapping, direct/repeated calls, offered/requested unit stops, and both-leg divide failures. Synthetic memory fixtures are not live-mission validation.
- Domain local check: 247 tests, 109 optional methods skipped, zero failures/errors; documentation links passed. Stage-1 and historical x86 reports were not regenerated.
- The current stage will use the authorized serialized `workstream.py integrate economy` from a clean committed tree; resulting feature/main hashes and actual common-gate counts will be sent to the coordinator before further implementation.

Remaining next dependencies: core's committed `CalculPosition` provider, then existing-unit type conversion and the rest of the production caller; market nonzero-unit bodies; general arrival/transport credit; market reset/input/persistence and real-mission dispatch. No live-world unit provider has been invented.

## Stage 2 integration and third-stage selection

Stage 2 successfully integrated: implementation `9801898fe79b74c2e2a84132f6135ed32e092245`, final pushed feature `a86311134b64ef4a5d875476bcd26b5194a47a48`, main merge `ac26806908d3d631c5f5910a9e0e379d39a1fb69`. Required helper passed core 248/122 optional skips, combat 124/76, economy 247/109, graphics 88/0, workflow 3/0: 710 discovered tests, 307 optional skips, no failures. Only after reporting this result did the next stage start from a clean helper-resumed worktree and updated-main merge.

Before new implementation, the remaining-component inventory selects the economic providers required by core's reuse of committed combat conversion: complete `EnginTypeGetCapacite` AL-byte query and complete `BonusGetValEngin` owner/type/selector query. Original addresses/tables and the incoming-ECX default-return quirk are published in the maintained manual. Core has been informed and owns the shared-world converter; this economy stage will not duplicate it. Runtime bonus table initialization/mutation and complete production continuation remain later dependencies.

## Stage 3: capacity and unit-bonus query providers

`bonus_unidades.capacidade_tipo(tipo)` is the complete AL-byte `EnginTypeGetCapacite` query at `0x4475AC`, with shared return `0x4474C5` and original dispatch at `0x447544`. It supports all 256 byte values and returns base capacity 0–6. `BonusUnidades(memoria).consultar(jogador,tipo,seletor,ecx=0)` is complete `BonusGetValEngin` at `[0x428CC0,0x428E71)`, using the original 13-entry dispatch at `0x428C8C`. It reads 1,872 already-loaded bytes at `0x4DFBA0`: player stride 468, type stride 18. Constructor zeros are synthetic, not a loader/reset.

Original input widths are AL owner, BL type, DL selector. Owners 4/200 return zero before dispatch/validation. Other owners with selector 8 or above 12 return incoming ECX u32 without lookup or index validation; the optional `ecx=0` argument is caller input, not an original default. Remaining lookups protect owner 0–3 and type 0–25 with `ValueError` on invalid indices; original out-of-table behavior remains unsupported. No mutations/callbacks occur. Selector offsets/widths are fully published in the maintained manual, including u16 fields and untouched opaque bytes.

Core's callbacks use `(owner,type,id)`: selector 1 is u8 `+0x0B`, selector 12 u8 `+0x10`. Combat's existing `Modificateur(owner,selector,type)` contract adapts via argument permutation, preserving original callback identifiers: selector 5 is u16 `+8`, selector 6 is u8 `+0x0A`; low-byte consumption remains combat's caller behavior. Both owners were notified, and no other-owner converter/damage implementation was duplicated.

Original EXE/SBL hashes remain those above. Additive `evidencias/bonus-unidades.json` and three listings publish exact code bytes/hashes plus the two dispatch tables. The original bodies run unpatched to return with no substituted queries.

Fresh commands:

```sh
python3 -B pesquisas-paralelas/economia/capturar_bonus_unidades.py
python3 -B pesquisas-paralelas/economia/validar_bonus_unidades.py
python3 -B pesquisas-paralelas/economia/validar_bonus_unidades.py --emular
python3 -B scripts/check.py --domain economy
```

Actual new results: 10 tests pass with no x86 skips/failures/errors; **4,060 complete original calls**, zero dependency stops/expected exceptions/limits. Coverage is 1,352 valid combinations, 1,524 selector-byte/neutral/default cases, 768 capacity-width/register-preservation cases, and 416 poisoned byte/word cases. Full query-state buffers/guards remain unchanged. Local stage: six passed/four optional skipped. Domain gate: 257 discovered/113 optional skips, zero failures; documentation links passed. No historical or prior-stage x86 totals are presented as rerun.

Global gap closed: exact read-only capacity/bonus providers needed for existing-unit conversion and attacker modifier queries. Status before integration: implemented and independently original-x86 validated; not yet wired into live mission/core/combat consumers. Loaded bonus initialization/setters, production continuation, and runtime dispatch remain. The coordinator's current overall estimate is approximately 50% (uncertainty 40–60%); this bounded provider delivery does not independently justify changing that coarse estimate. Required clean-tree serialized integration and actual feature/main hashes will be reported before another stage begins.

## Stage 3 integration and fourth-stage selection

Stage 3 is integrated: implementation `b1eb0c06e3b016f9abc2d27f3a836f6c20abf2f9`; final feature `d10c4e6af843b1af4e00286f212663fd777fd680`; main merge `7325cd0a3cb54d80d10a0c62c7d61bd25b0f8c49`. Required helper passed 731 tests/319 optional skips. Stable read-only providers were sent to Core/Combat. Only after reporting these results did the clean worktree resume through the helper and merge updated main.

Before implementation, selected next dependency: original `BonusSetEngin` table producer and selective `BonusReset`. Exact inspected addresses/selector widths/sentinels and preserved reset offsets are published in the maintained inventory. Selector 1's post-write `EnginResetCapacite` call is a requested core provider; its absence must preserve writes and remain pending. This closes the source of bonus-state mutations without moving world-unit mutation into economy.

## Stage 4: bonus table mutation and selective reset

`BonusUnidades.reiniciar()` is complete `BonusReset` at `[0x428E71,0x428EEE)` plus shared return `[0x428716,0x42871A)`. It performs ten ordered writes per record over 4 × 26 records and preserves record offsets 3/7/15/16/17. `definir(owner,type,selector,value, recalcular_capacidades=None)` supplies protected `BonusSetEngin` `[0x428878,0x428C8A)`: AL/BL/DL u8 and CX u16. Selector >12 is no-op before guard checks; active owner range is 0–3 with no neutral bypass. Normal types 0–25; BL=30 only for selectors 0/1/3/4/5/6 with branch-specific filtering. Exact offsets/formulas/filter set are published in the maintained manual.

Selector 0 uses runtime type word +46, a signed32-wrapped multiply and signed IDIV 10 before low-u16 storage. Selector 3 uses word +48 minus ten-times-word divided by CX; zero divisor raises before first write. Selector 12 stores CX-10 in u8. Other fields copy CL/CX at their original widths. Setter selector 8 writes opaque +13 although query selector 8 returns incoming ECX. No field meaning is invented. Constructor runtime types are 26 × 50 bytes, synthetic zero if omitted.

Selector 1 mutates capacity byte +11 (BL=30 affects only types 12/13/15), then calls original `EnginResetCapacite` at `0x428C60 -> 0x4475EF`, AL owner. Missing callback raises `CapacidadeUnidadesPendente` after table writes; callback errors preserve them. Core owns live-unit Bag capacity refresh and received this request. The original tests stop at the dependency, never stub it as success. Other setter/reset branches execute completely to return.

Original EXE/SBL hashes are unchanged. New `evidencias/mutacoes-bonus.json` and four listings contain exact original code/table bytes/hashes and supported interfaces. Fresh commands:

```sh
python3 -B pesquisas-paralelas/economia/capturar_mutacoes_bonus.py
python3 -B pesquisas-paralelas/economia/validar_mutacoes_bonus.py
python3 -B pesquisas-paralelas/economia/validar_mutacoes_bonus.py --emular
python3 -B scripts/check.py --domain economy
```

Actual stage results: 11 tests pass/no skips in x86 mode; **2,094 bounded calls = 1,946 returns + 124 capacity-refresh stops + 24 expected divide exceptions** at `0x428A67`/`0x428ACE`; 2,070 declared stops, zero limits/failures/errors. Protected table/runtime-type buffers and guards match; all 1,040 reset writes are checked in original order. Local producer suite: five pass/six optional skips. Domain gate: 268 discovered/119 optional skips, no failures; documentation links passed. The owned aggregate validator now counts all new benchmark groups in a future explicit full run; predecessor reports remain unchanged.

Global gap closed: original producers for the bonus table consumed by integrated read-only providers. Status before required integration: implemented and independently original-x86 validated; actual live-unit capacity refresh, mission/event loading and production/runtime composition remain providers/dispatch gaps. Overall coordinator estimate stays approximately 50% (40–60% uncertainty) for now; neither reset fixtures nor native call totals measure full-game completion. Feature/main hashes and common integration gate will be reported before another stage begins.

The updated aggregate-report runner was also exercised locally: 268 tests/119 skips, zero failures/errors/x86 calls, with its JSON write redirected only to a temporary file. All 16 benchmark groups, including the four new stages, appear in the counts; original versioned predecessor reports were left untouched.

## Stage 4 integration and fifth-stage selection

Stage 4 implementation `de6d6361aebcdb95e93ce60ee27e8e19e8fb8f5f`, final feature `e99d2316f715312cc7f97cf6a9b196f42ce08959`, main merge `25f5feabed2ce8828bd514f4a960f8cab9c3669e` are pushed. Required common gate passed 778 tests/336 optional skips. Only then did the next stage resume the clean helper-managed worktree and merge updated main.

Before implementation, selected highest-value economic caller gap: `CalculTroupe` type-1/2/13/16 simulation branches, including exactly one progress advance and the original `SortieTroupe` directions/call order. This composes existing economy routines and may hand off to the already committed core converter without reimplementing it. Original full-entry/dispatch/prefix validation will distinguish complete below-threshold returns from position dependency stops; other dispatch branches and later production world effects remain open.

## Stage 5: original production simulation caller

`Producao.calcular_tropa(indice, saida_tropa=None)` reconstructs `CalculTroupe` (`0x4259E6`) for the shared building-type family 1/2/13/16, including the real low-type dispatch at `0x426401`, inline x87 progress bodies and original `SortieTroupe` call. Index is AX u16 within the provided record pool. Other building types are protected `ValueError` cases before writes, not original return claims. All state/table/Bag domains remain the existing production/preparation contracts.

Active means nonzero u32 progress +8C and byte +74. Inactive calls do not query time or call exit. Active below-threshold calls advance once with the already proven binary64/x87 increment and runtime building capacity, then call `SortieTroupe` even below completion. At/above threshold they skip progress arithmetic. Directions: 4 for types 1/2/16, 14 for type13. Default composes the actual owned economic preparation, returning None below completion or a pending position record after colonist/cargo removal. Optional exact exit callback receives index/direction after the increment; failures preserve progress and earlier callback effects.

Do not add a separate `avancar_unidade` call for the same update. Do not process this building again after a pending or failed exit until the original continuation resolves it: economic removal may be committed while progress/activity remain set. Core's committed converter is reused at its own boundary; it is not duplicated by this caller. Healing/exit/cleanup and unsupported dispatches remain explicit gaps.

Additive `evidencias/ciclo-producao.json` plus three listings record original bytes/hash/entry/dispatch/epilogues and coefficient data under unchanged EXE/SBL hashes. The benchmark starts at the real function entry and executes actual progress and exit-prefix instructions without native callback mocks. Fresh commands:

```sh
python3 -B pesquisas-paralelas/economia/capturar_ciclo_producao.py
python3 -B pesquisas-paralelas/economia/validar_ciclo_producao.py
python3 -B pesquisas-paralelas/economia/validar_ciclo_producao.py --emular
python3 -B scripts/check.py --domain economy
```

Actual new report: 10 tests pass/no skips; **1,432 bounded calls = 1,268 returns + 160 position stops + 4 expected division exceptions at `0x423501`** after prior increment/removals. There are 1,428 declared stops, zero limits/failures/errors. Whole protected buffers and guards, observed exit arguments, register preservation on return, x87 control/tags, count/capacity samples, time/activity/unsigned/index boundaries, 16 update sequences, and partial post-increment errors are checked. Local stage: six passed/four optional skipped; domain gate: 278 tests/123 optional skips. Aggregate runner includes the new caller bench for future explicit runs. Predecessor reports were preserved.

Global gap closed: original simulation-update caller sequencing for four production building types, connecting progress to exit preparation exactly once per active tick. Status before mandatory integration: implemented and original-x86 validated; no complete unit production or real-mission runtime claim. Core refresh is now committed at `8126f1aed299e19337e2b1ac4f95cfa85c068214`; per coordinator direction, the next stage after this integration will wire BonusSetEngin to that provider using shared bonus/unit buffers and exact failure order. Overall coarse estimate remains coordinator's approximately 50% (40–60%).

## Stage 5 integration and sixth-stage selection

Stage 5 implementation `a9f055ca4fbf30327f5e83b4211ef1e4ad8a7802`, final feature `9e07845bff79820d7cdd3d39f3b77d136c309ca8`, main merge `342063d0303d6a31587851ecb5af4898f3457601` are pushed. Required gate passed 804 tests/348 optional skips. The next stage resumed the clean worktree with the helper and merged updated main before implementation.

Per the coordinator's priority, selected gap: connect the committed bonus setter to core's actual committed 800-slot capacity refresh, preserving shared bonus/unit identity and post-write failures. Complete native original setter/refresh/query comparisons must distinguish real returns from intentional pre-query stops. The owning wrapper will not duplicate core scan or economic query algorithms. Full world production, mission/event dispatch and other provider gaps remain explicit.

## Stage 6: bonus producer joined to committed live-world refresh

`bonus_compartilhados.definir_bonus_no_mundo(bonus,mundo,owner,type,selector,value)` calls the existing setter once, then for selector1 invokes the actual committed core `atualizar_capacidades_unidades` with this same post-write bonus object, live unit pool, and original capacity/bonus query providers. It imports only this checkout's core module at the callback boundary; a foreign same-named snapshot module raises there. Other selectors never load the core provider. No scan/query implementation is copied and no buffers are copied or written back later. Input domains remain the established setter/core contracts.

Ordering: bonus table writes first; core pool validation next; then ascending eligible owner-matching units, capacity query, selector1 query, low-u16 capacity store. All matching units refresh regardless of which type's table entry changed. Bag counts/contents remain intact. Import/guard/query errors retain the table update and earlier unit stores; this/later units remain unchanged on a later query failure. The wrapper never replays the setter or rolls back. Read-only/reentrancy restrictions remain the core provider's contract.

Additive `evidencias/bonus-compartilhados.json` records six exact original setter/refresh/query intervals and immutable provider revisions under unchanged EXE/SBL hashes. Native tests execute the full original chain; no native callback returns are substituted. Three deliberate Python callback failures plus three protected invalid-type errors are compared to conditional native pre-query stops at `0x44763A`, units0/7/799. They are dependency/domain stops, not native exceptions.

```sh
python3 -B pesquisas-paralelas/economia/capturar_bonus_compartilhados.py
python3 -B pesquisas-paralelas/economia/validar_bonus_compartilhados.py
python3 -B pesquisas-paralelas/economia/validar_bonus_compartilhados.py --emular
python3 -B scripts/check.py --domain economy
```

Actual stage results: 11 tests pass/no skips, **454 bounded native executions = 448 complete returns + six pre-query stops**, zero native exceptions/limits/errors/failures. Nested queries are reported separately. Full unit/bonus/runtime-type buffers and guards, actual query/write order, owner/type pairs, all-type sentinel and byte boundaries, untouched Bags/unrelated selectors, and exact partial failures match. Local stage: five passed/six optional skipped. Domain gate: 289 discovered/129 optional skips, zero failures; documentation links passed. Earlier reports were not regenerated.

Global gap closed: actual producer→world-capacity callback composition on identical shared loaded buffers, no longer merely a declared pending callback in this entry point. Status before required integration: implemented and independently native-validated, not real-mission-tested. Mission/event loading, other production dispatches, healing/exit/cleanup and runtime ownership remain gaps. Overall estimate remains coordinator's approximately 50% (40–60%). Required feature/main hashes and actual integration counts will be reported before another stage begins.

## Stage 6 integration and seventh-stage selection

Stage 6 implementation `68c59811fbe8cd5a0c0eccc4b9d04a1c4a1fa640`, final feature `e07dc41562af96e7bc909146cbf81e7653f0e4a7`, main merge `15e49e8dfe7c77f60ec0c468e5546bc891384f42` are pushed. Required gate passed 827 tests/357 optional skips. Only then did the next stage helper-resume the clean tree and merge updated main.

Before implementation, selected original market lifecycle callers: `MarcheResetAll`, `ResetMarche`, and `MarcheQuitte`, with exact inspected ranges and selective-versus-preserved fields published in the maintained inventory. Pair/quit partial effects before an invalid second index must be explicit and native-checked at a real checkpoint. This is independent of missing production healing/exit/cleanup providers and does not duplicate world effects.

## Stage 7: selective market reset and quit

Resumed through the helper and incorporated committed main `5e2bf0831d3aaa776481a6ab023be262ef0df1bd`, preserving the prior two planning notes. Production integration remains first priority, but the current committed conversion stops at `0x420f6e`; exact remaining core calls were published to core before proceeding with this inventoried fallback. Core has acknowledged work on healing/fatigue through `0x420f81`.

`ciclo_mercado.CicloMercado(mercado, **buffers)` shares the actual `Mercado` (contact/indicator/economy/player/proposal identity), copies five raw additional buffers, and performs complete `MarcheResetAll` `[0x46027c,0x4602cd)`, `ResetMarche` `[0x46634e,0x4663d6)`, `MarcheQuitte` `[0x4663d6,0x4663eb)` within protected u8 players 0–3. Methods `resetar_todos()`, `resetar(j,k)`, `sair(j)` return `None`, no callbacks. Defaults are synthetic zeros; raw names do not assert gameplay meaning.

Only seven per-player fields reset: byte `2e7c=0`, byte `292c=1`, byte `2928=0`, contact `496f8c=255`, words `2930/2938/2940=0`. All proposal/price/approval/difference/balance/player/sympathy data and gaps remain. Full reset order per row: `2e7c,2930,contact,292c,2928,2940,2938`. Pair first order: `2e7c,292c,2928,contact,2930,2940,2938`; second: `2e7c,contact,292c,2928,2938,2940,2930`. Aliases write twice. Invalid first index raises before mutation; second is guarded only after first row effects. Quit captures contact before pair mutation; invalid contact 255 is a partial-effect error, not an invented original return. No rollback/retry is supplied.

New byte evidence/manifest `evidencias/ciclo-mercado.json` preserves original EXE `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb` and SBL `c3a5411255847d36161aea1aeef06ab280265c55fa5a6626cfeb7bab523cc627`. Native quit executes the real ResetMarche call. Invalid second comparisons use first-row checkpoint `0x466395`, before unchecked native second-index use. Native does not implement Python's guards.

REA complementary reviewed excerpt `evidencias/ciclo-mercado-rea.json` retains source revision, both executable identities, provider/profile/dossier identity and original quit assembly/call edge. Recovered ECX fastcall signature is unreliable; AL/DL are established from original instructions and execution. Restricted startup's Java EPERM was resolved using authorized context; session exported/closed cleanly, no OS or shared infrastructure change. This was an adapter restriction, not a substantive reasoning stall.

Fresh commands: `capturar_ciclo_mercado.py`; `validar_ciclo_mercado.py`; `validar_ciclo_mercado.py --emular` (all with `python3 -B` under this folder); then `python3 -B scripts/check.py --domain economy`.

Actual new validation: 14 tests pass/no skips, **1,275 bounded executions = 259 complete returns + 1,016 intentional first-row stops**, zero faults/limits/failures/errors. Whole buffers/seeded gaps/guards, all pairs and aliases, u8 register widths, all 252 invalid second bytes × four first players, contact/quit boundaries, persistent sequences, original register preservation and exact write order match. Local stage: seven executed/seven optional skipped. Earlier/historical native reports preserved. The required economy gate passes 303 discovered tests with 136 optional skips and valid documentation links. Aggregate runner now counts the new bench when explicitly invoked; it was not rerun.

Global gap closed: precise market reset/quit lifecycle integrated with the shared market state without erasing proposals or approvals. Status before mandatory helper: implemented and independently native-validated; no real mission or complete runtime claim. Unit exchange, mission/event dispatch, complete production healing/exit/building cleanup and world loading remain gaps. Required feature/main hashes and common-check counts will be reported before the next stage. The coordinator's approximate overall estimate stays 50% (40–60%).

## Stage 7 integration and Stage 8 inventory

Pushed implementation `c10dff75af2495946a8f0fb204eb71ada35941e2`, feature `5eafc1eff6235536a243716ec7253ee5992537c6`, main merge `874167ede98bdb08980d7d071683945ec25785ff`. Required common gate: core280/134 optional skips, combat163/102, economy303/136, graphics115/0, workflow3/0 (864/372 overall). Subsequent fetch and ancestry checks verify all three commits on fetched main. Clean feature resumed through helper and fast-forwarded to874167e before selection.

Next selected boundary: economy-owned composition of original production caller `0x4259e6` with its once-per-active-update increment, existing economic preparation, and actual committed core position/conversion/healing/fatigue, ending at `0x420f81` before experience setup. Consume core's new provider only after its integration and published API; never read sibling live state or duplicate world helpers. Require identical live unit/structure objects and loaded bonus/type inputs. Original full-chain execution must compare whole buffers, query/deposit ordering and partial failures after preparation. Core currently reports its own 2,020 validated calls for healing/fatigue; those are not economy's executions. Original post-unit cleanup `0x420fb7` branches on Bag unit types, has terrain/color and AI message dependencies, and remains outside this slice. No complete production or real mission claim. This inventory is published before implementation.

## Stage 8: actual production caller through shared recovery

Consumed inspected core main `62b9d76941dbcf90a2dc5d45b71317136c8b5d28`, recovery implementation `3b7f71697095ab12e960bf4cbdf0952d20d554d8`; exact upstream API/contract is `ferramentas/recuperacao_unidades.py` / `docs/core/RECOVERY.md`. `producao_compartilhada.calcular_tropa_no_mundo(producao,mundo,bonus,indice)` enforces identical live unit/structure objects before any progress, then calls the existing production update once. Its actual exit callback runs existing economic preparation once; only prepared output resolves this checkout's core providers and runtime type-table dimensions. Existing protected AX/index/building/Bag/type/owner domains apply at their own stage, no copied scans/world implementation.

Actual order: progress→economic colonist removal→stone entries then food deposits→core position→live requested-type reload/conversion (real capacity/bonus queries and search release)→healing1000→fatigue clear/copy. Runtime dimensions are the same production table's u16 fields. Returns `None` for inactive/below threshold, otherwise actual `RecuperacaoSaidaTropa(...,endereco_dependencia=0x420f81)`, before experience. Shared buffers are never copied/reconnected. Loaded bonus object is required and read-only; zero fixture data do not model loading. Lazy core dependencies are resolved with scoped imports, and foreign same-named checkout modules raise after preparation. A fresh subprocess regression proves no permanent core search path is needed.

Import/dimension/query/recovery errors preserve earlier progress, removals, credits and unit/search changes. Do not advance separately on the same tick or replay/reprocess pending or failed output. This one-shot handoff has no automatic completion or retry; experience/placement/movement/conditional request and building cleanup remain open.

Additive `evidencias/producao-compartilhada.json` records exact original caller continuation and immutable provider/evidence identities under unchanged original EXE/SBL hashes. Native entry is actual `CalculTroupe 0x4259e6`; all nested original calls remain unpatched. Explicit dependency comparisons use original position entry (two Python import errors) and bonus entry (four Python query errors), retaining earlier effects; they are not native faults. Full new commands: `python3 -B pesquisas-paralelas/economia/capturar_producao_compartilhada.py`, `validar_producao_compartilhada.py` locally and `--emular`, then required `python3 -B scripts/check.py --domain economy`.

Final native result: **13 tests, 782 calls = 136 returns + 636 experience checkpoints + four bonus stops + two import stops + four expected deposit division exceptions at0x423501**; zero skips/failures/errors/limits. Full protected buffers/guards, shared search, actual query/deposit order, four building×26 type×six owner combinations, widths/edge slots/dimensions/health/bonus boundaries, inactive states and twelve persistent sequences match. Local: seven executed/six optional skipped. Required economy gate: 316 discovered tests, 142 optional skips; documentation links pass. The first report (53 calls/four failed trace assertions) is preserved separately; inherited observation lists collided, fixed by routing the core observer to its own list. No reconstructed behavior changed for that correction, and no substantive reasoning stall occurred. Aggregate runner counts this bench for future explicit runs; historical/earlier native reports were not regenerated.

Global gap closed: original simulation caller sequencing now has an actual shared-state connection through economic preparation, position/conversion and healing/fatigue, independently native-validated. Mandatory integration follows before new implementation. Real-mission operation, experience/physical output/AI calls and economic cleanup stay explicit. Overall project estimate remains coordinator-owned at approximately50% (40–60%).

## Stage 8 integration and Stage 9 selection

Stage8 implementation `3c2fc2c3d3227e89cec76bff357ab3ce5395dd47`, feature `4f0cd24126b68e1812437915f1b05e6ce16bd679`, main `089919c926bfdcddd94152fe3abcf40c8001e81f` are integrated. Required gate: core290/138 optional skips, combat178/111, economy316/142, graphics115/0, workflow3/0, total902/391. Fresh fetch/ancestry verify all three; current main later advanced. Exact provider contract shared with core/app/missions, canonical unchanged. Clean tree helper-resumed before selection.

Stage9 inventory: isolated economic cleanup continuation beginning original0x420fb7, requiring the actual preceding world caller to have reached that boundary (currently no complete provider through it). Supported building types1/2/13/16. Type2 uses BagVide0x44724a..4472d3 (unit-type predicate over capacity, not count); if false it falls through to type9 BagContient. Others use existing type9 query. True retention branch reuses committed core selective reset then stops before unit-message70 at0x4211d3. False branch resets types1/2 first, then all four stop before terrain query0x42110c with raw parameter10 for type2/8 otherwise. Core reset implementation must be reused, never copied. Native evidence/testing will declare isolated frame/index/unit/EDI inputs and actual original helper calls. It will not claim the missing experience/placement/request prefix or complete cleanup/messages/mission runtime. Selection is published before implementation.

## Stage 9: isolated cleanup decisions and selective reset

`limpeza_saida.retomar_limpeza_saida(producao,mundo,pedido)` requires explicit pending address0x420fb7, u16 protected building0..999/outputunit0..799, type1/2/13/16 and identical live economy/core unit/structure objects. Those guards precede mutation. The missing experience/placement/movement/request prefix is not executed by this entry and cannot be skipped by passing recovery's0x420f81 handoff.

Complete `bag_vide(r,indice)` is original0x44724a..4472d3: capacity0..30 scan, tag1 only, referenced unit0..799 only when read, early return for all u8 types except3/11/12/13/14/15/16/17/25. Count, activity and owner are ignored; unknown type26..255 passes. Type2 cleanup runs this first, then only on false uses existing type9 `Producao.contar_unidades`. Other supported building types query type9 directly. True retention→actual core selective reset→pendingunitmessage70 at0x4211d3 (callee4829c8). False→types1/2 reset now (13/16 preserve pending progress)→terrainquery checkpoint0x42110c (callee41aee2), rawparameter10for2/8otherwise. Following476e82 terrain and unit/building AI messages remain unresolved.

The identical inline reset uses actual committed `ciclo_estruturas.resetar_estrutura` implementation7a24e974384782e66d6c7454fe1343035e1178db; no stores are copied into economy. Same-checkout import happens only where reset is needed; foreign provider errors propagate at that boundary. Existing Bag query guards preserve original read/early-return order. No rollback, implicit replay, ownership transfer, terrain change or completion message occurs.

New evidence `evidencias/limpeza-saida.json` captures cleanup context/complete BagVide, original bytes/hash/jump table and immutable core reset evidence. Original EXE/SBL hashes unchanged. Native harness is **explicitly isolated** at0x420fb7 with frame[ESP]building/[ESP+4]outputunit and EDI live record; actual original helper calls/inline stores run to the genuine pending call. No whole-caller/real-mission assertion.

Commands: `python3 -B pesquisas-paralelas/economia/capturar_limpeza_saida.py`; `validar_limpeza_saida.py` locally/`--emular`; required `python3 -B scripts/check.py --domain economy`. Actual fresh result:10tests/no skips, **1184native=512completeBagreturns+555unitmessagestops+117terrainquerystops**; zero faults/limits/errors/failures. Full protected buffers/guards, all256typebytes×count0/1, indexwidths/edges, state3retention, types1/2/13/16, duplicate/mixedcapacityentries and seededfields match. Local6executed/4optional skipped. Required economy gate326discovered/146optional skips, documentation links pass. Historical/earlier native reports unchanged; no substantive reasoning stall.

Global gap closed: exact local cleanup decisions and reset timing with actual committed shared reset. Independently native-validated isolated continuation, mandatory integration next. Full preceding unit caller, terrain/AI messages, other building types and real mission remain open. Overall approximate50% (40–60%) remains coordinator-owned. Publish exact hashes/checkcounts after integration before another implementation.

## Stage 9 integration and Stage 10 selection

Stage9 implementation3a7ac12a4906553b73b84037a17f51c0c552cf88, featurec191342066b8484cab929f285c02a6669da36327, main29f90a27a522ad13d732ec821ecf73729042e2e4 are pushed and fresh-fetch ancestry-verified. Required gate core302/143optional,combat185/115,economy326/146,graphics115/0,workflow3/0=931/404. Cleanup remains explicitly isolated. Exact terrainquery→476e82 and unitmsg70/buildingmsg3 requests sent to core. Clean feature helper-resumed before next selection.

Stage10 selected gap: actual production update→existing Stage8 shared recovery→core committed retomar_experiencia_saida, stop420f8a beforeplacement. Consume inspected core implementationf67898b75423adcfaf90a7b6e6c710c409e6f9ee atmaindae42125f45c348c10dff7e727e803138be7670f, never copy queue/level logic. New explicit producer entry preserves existing420f81 API. Raw40-byte queue must remain explicit loaded/inherited input, not claimed zero default. Native tests start actualCalculTroupe and compare whole buffers/queue, AF/F5–F8, firstpair/no-search behavior and partial failures after recovery. No placement/cleanup/realmission claim. Inventory precedes implementation.

## Stage 10: production update through committed experience

New explicit `producao_experiente.calcular_tropa_com_experiencia_no_mundo(producao,mundo,bonus,indice)` delegates once to Stage8's actual update/preparation/position/conversion/recovery, then only for its prepared handoff loads actual committed core `retomar_experiencia_saida` with the same loaded type table. Returns None before completion, otherwise actual ExperienciaSaidaTropa at420f8a beforeplacement. Existing Stage8 public endpoint420f81 remains stable; no earlier report/algorithm changed.

Core implementationf67898b75423adcfaf90a7b6e6c710c409e6f9ee was inspected from integratedmaindae42125f45c348c10dff7e727e803138be7670f. Raw writable40-byte `mundo.experiencias_unidades` supportsowner0..3 and must be supplied as live inherited/loaded state; defaultzero is synthetic. Actual core firstpair guards, AF/F5–F8 effects (same runtime+2e), then ordered shift are reused without copies. No later-pair search, retries or duplicate progress. The original local queue/level provider differs from combat's lethal-experience dependency.

Import/queue/type/owner errors occur after prior recovery and preserve all economic/unit/search/healing/fatigue effects. Same-checkout provider import is scoped; foreign module rejects at that late boundary. Output is one-shot and still requires real placement/movement/request and economic cleanup. The isolated420fb7 cleanup contract cannot accept420f8a.

New `evidencias/producao-experiente.json` records original caller bytes, immutable prior/core evidence identities and provider commit. Fresh native entry actualCalculTroupe4259e6 executes all nested calls unpatched. Twelve Python queue guards and two import failures compare to420f81 afterrecovery/beforequeueuse; native does not implement those protected guards. Commands: capturar_producao_experiente.py; validar_producao_experiente.py local/--emular (python3-B under this folder); required scripts/check.py --domain economy.

Actual new validation:11tests pass/no skips, **610calls=136returns+460placementcheckpoints+14postrecoverystops**, zero faults/limits/errors/failures. Full queue/sharedbuffers/guards, all4building×26type×4owner combinations, eight levels,32firstpair/no-searchcases, rawqueue failures, edgeindices/highbits and12persistentupdate sequences match. Local6executed/5optional skipped. Required economy gate337discovered/151optional skips, documentation links pass. Historical/earlier native reports unchanged; aggregate includes this bench only on future explicit run. No substantive reasoning stall.

Global gapclosed: actual economic producer→sharedworldrecovery→recruitmentexperience consumption, independently native-validated, integrationnext. Full placement/request/cleanup/terrain/AI effects and realmission remain open. Coordinator's coarse overall approximate50% (40–60%) remains independent of test counts.

## Stage 10 integration and Stage11 inventory

Pushed implementation38375594123849fb6607cd9ec8749202166e5e8f, featureff9dcf7b49f5bde6e030a2bb745c8420658b9e9f, main12b97ff3f2b1a1f242a0d5430ff0a0f914791d10. Required gate core302/143optional,combat191/119,economy337/151,graphics122/0,workflow3/0=955/413. Freshfetch ancestry confirmedallthree. App/missions received exact stablequeueproducercontract; treeclean/helperresumed beforeselection. Core placement still in nativevalidation, no committedprovider available yet.

Stage11 selection beforeimplementation: full read-only EnginRentreMatiere456cd9..456d35 and EnginApporteMatiere456d35..456d92, plus actual BatimentGetType41a4f4..41a513. Both gate literal unitstate5/17/18. Rentre requires+82byte2, then+80u16building reference and compares buildingtype+8 to requestedDLu8 (not owner). Apporte compares full+84u16 to requestedDLu8 and usesBL0wildcard/otherwise exact+82byte. Furtherrawfield meanings remainunproved. Protected unit0..799; building0..999 guardedonlyafterstate/mode branches reachread; unusedinvalidrefs must beignored. Nativefullreturns/conditionalprelookupguardstops and wholebuffer preservation required. No movement, cargo action or transport state machine claimed. No existing committedcore implementation found attheseaddresses. REA complementarycallerinspection will preserve separateanalysis/originalidentities and reject inferredsignatures asneeded.

## Stage11: complete read-only transport status

`consultas_transporte.ConsultasTransporte(recrutamento)` shares supplied state (defaultsynthetic). `retorna(indice,tipo_construcao)` fully reconstructs456cd9..456d35 and actualconditionalBatimentGetType41a4f4..41a513: state5/17/18, byte+82=2, then+80u16buildingref, comparebuildingtype+8 toDLu8. Owner+4 isunused. Target0..999/suppliedpool guard occurs onlywhenread; falseprefix ignoresunusedinvalidrefs. `aporta(indice,valor84,modo82=0)` fully reconstructs456d35..456d92: same literalstate gate, full+84u16equalsDLu8, thenBL0wildcard/otherwiseexactbyte+82. Rawfield wider meanings unproved. Both AXunitu16/protected0..799/full800pool, ALbool, no mutation/Bag/order/movement/cargo/state-machine effect.

Additive three-interval original evidence/manifest `evidencias/consultas-transporte.json` preserves originalEXE/SBL identities and recordsinputwidths/conditionalguard. Nativeoriginalgetter executesunchanged onvalid targets; sixPythonprotected errors comparetoprelookup41a4f4, notnativefaults. Nativepreservedregisters andwhole economic/capacity/terrain/recruitment/unit/structurebuffers/guards checked.

REA `analyze_function456d35` found no procedure inexistingreadonlyproject; exactinstruction Listingalso reportsundecodable. New reviewed `evidencias/consultas-transporte-rea.json` records sourceb9a8f8e9f25feb9cc97bf4960748f2bdf8c898bc, separateoriginal/analysisSHA, provider/profile, sourceobservationhashes andcoverage limitation. IntactoriginalSBL/Capstone/nativeexecution remainauthoritative; this is notCPU-byte invalidity, adapterfix orsemanticstall. Sessionexported/closed, noprojectrepair attempted.

Commands: capturar_consultas_transporte.py; validar_consultas_transporte.py local/--emular (python3-B inownedfolder); requiredscripts/check.py --domain economy. Actualfreshresult:12tests/no skips, **4934calls=4928completeRET+6prelookupstops**, faults/limits/errors/failures0. Allstatebytes, allcomparison/modebytes, fullwordboundaries, earlyignoredrefs, edges/highbits, originalpreservedregisters andseededfullbuffers match. Local6executed/6optional skipped. Requiredeconomygate349discovered/157optional skips, links pass. Historical/earliernative reports untouched; aggregate includesnewbench onfutureexplicitruns.

Global gapclosed: complete transport-status predicates andconditionaltypequery, independentlynativevalidated; mandatoryintegrationnext. Actions/transportstate machines, production placement/request/cleanup andrealmission remainopen. Coreplacementnowcommittedaa9cba47af34aef3b0b4b67faded0b884bb1e428; priorityafterthisintegration isactualproducercompositionto420f9e withthatprovider, nojumpoverrequest420f9e..420fb7. Coarseoverallapproximately50% (40–60%) remainscoordinator-owned.

## Stage11 integration and Stage12 selection

Implementationbf2de88a49444f16a6f01a677fd6cdbb4c2f7a0f, feature5d84ded24667400997492131ce814c4b0db77009, main477bc3a682fc0bb8a2a26781eef76123718341ed integrated/fresh-fetch ancestryverified. Requiredgate core319/151optional,combat198/123,economy349/157,graphics134/0,workflow3/0=1003/431. Cleanfeature helper-resumed/currentmain incorporated beforeselection.

Stage12 selected actualproducer→committedcorephysicalplacement/movementorder to420f9e. Provider colocacao_saida.retomar_colocacao_saida implementation6b3882b5b4a3a0c99dddcaccbd4d1c08a765f8ce atmainaa9cba47af34aef3b0b4b67faded0b884bb1e428. Newentry retains oldrecovery/experienceAPIs. Nativepointer audit adds requiredidentityaliases: r.mundo.terreno.tipos IS mundo.objetos (507d74), r.mundo.terreno.quantidades IS mundo.donos_objetos (507dac), alongside unit/structureidentity. No silentcopy/reconnection or speculativeuniversalrawbyte semantics. Guardsbeforeprogress.

OriginalfullCalculTroupe comparison willreusecore'sphysicalworld/harness/allowedintervals/effecttrace andnative preserved-state resumptions, not duplicateworldlogic. Matchallphysical/search/queue/routes/discovery/light/minimap andowned economic/productionloadedstate; reportoriginalentries versusboundedsegments/resumes separately. SupportedvisionBB+F5<=8; larger normal-owner vision stopsbeforediscovery afterpriorcollision/+72 andalleconomic/experienceeffects. Actualmovementorderuseslivebuilding+7c. Requestgap420f9e..420fb7 andcleanupterrain/AI remainsopen; no bypass/realmissionclaim. Inventoryprecedesimplementation.

## Stage 12: actual producer through physical exit and order

`producao_colocada.calcular_tropa_com_colocacao_no_mundo(producao, mundo, bonus, indice)` delegates once to the existing experience producer, then invokes committed core `colocacao_saida.retomar_colocacao_saida` (implementation `6b3882b5b4a3a0c99dddcaccbd4d1c08a765f8ce`, main `aa9cba47af34aef3b0b4b67faded0b884bb1e428`). It returns `None` if inactive/incomplete, otherwise actual `ColocacaoSaidaTropa` at `0x420f9e` before the conditional request. Recovery/experience endpoints remain stable. No world algorithm is copied.

Before progress, require the original raw aliases: economic `terreno.tipos is mundo.objetos` at `0x507d74`, and `terreno.quantidades is mundo.donos_objetos` at `0x507dac`, alongside the earlier unit/structure identity guards. The entry never reconnects copies. Cell interpretation depends on context. The complete producer supports queue owners 0–3 and explicitly supplied physical world/type/bonus/queue state. Core places the existing unit, retains old occupancy, releases search, sets `+72`, performs discovery/light/minimap, reloads live building `+7c`, and issues the actual movement order. Normal vision sum BB+F5 must be at most eight; larger sums stop before discovery, preserving preceding record/collision and economic/experience effects. Import errors after experience retain earlier stores. Do not replay, add another advance, or process the pending building again; activity/progress still await cleanup.

Additive `evidencias/producao-colocada.json` records original caller/raw pointer context and immutable provider/evidence identities under unchanged EXE/SBL hashes. Native tests start actual `CalculTroupe`, with every nested call unpatched. They reuse core's physical harness, fixture, effect observers, and minimap pauses with preserved CPU registers/flags/stack. Per-segment caps/timeouts remain unchanged; no CALL, RET or callback result is replaced. A separate economic data-loading adapter preserves core's raw pointer bindings. Complete deposit→collision/discovery/light/minimap→movement traces match.

Commands: `python3 -B pesquisas-paralelas/economia/capturar_producao_colocada.py`; `validar_producao_colocada.py` locally and with `--emular`; then `python3 -B scripts/check.py --domain economy`.

Fresh native result: 13 tests pass without skips; **192 original entries in 552 bounded segments, including 360 minimap resumes**. Entry outcomes are 64 returns, 118 request stops at `0x420f9e`, eight pre-discovery stops at `0x446146`, and two post-experience import stops at `0x420f8a`. Faults, limits, failures and errors are zero. Earlier four-building calibration (four entries/20 segments) remains separate and is not an original-only capture. Coverage includes all four building × 26 type pairs, owner/edge samples, loaded bonus/object branches, vision boundaries and partial failures, unsaturated light, and four persistent sequences. Full physical/unit/structure/group/search/routes/queue/vision/light/minimap and owned economic/capacity/recruitment/production buffers plus checked input guards match. Core's original-only captures remain separate upstream evidence.

Local mode executes six tests and skips seven optional methods. The required economy gate passes 362 discovered tests with 164 optional skips and valid documentation links. The initial local command failed before tests because the core fixture required its tools import path; test setup was corrected. Both native runs passed. Earlier/historical reports remain unchanged. Future explicit aggregate runs count bounded segments. No substantive reasoning stall occurred.

Global gap closed: the actual economic producer now reaches shared physical placement and the original movement order, independently native-validated before required integration. Request handling at `0x420f9e..0x420fb7`, full cleanup/terrain/AI effects and real-mission operation remain open; the isolated cleanup entry cannot bypass that gap. Overall approximate 50% (40–60%) remains coordinator-owned. Publish exact feature/main hashes and common-check counts after integration before another implementation.

## Stage 12 integration and Stage 13 selection

Integrated implementation `e1ff67fc0eb729dae87505721170b266831f4af6`, feature `2b159f81129b50c6366df52b14fd2a9a999d136a`, main `62f0a1c86c35a5bb883d156423bcd1efe71f0772`; fresh fetch confirms all three ancestors of main. Required gate: core319/151 optional skips, combat211/131, economy362/164, graphics148/0, workflow3/0, total1,043/446. App/missions received stable producer and raw-alias contracts. Canonical was not modified by this chat; its ref advanced externally. Clean feature helper-resumed before the next selection.

Stage 13 will compose the actual producer with core `voz_unidades.retomar_solicitacao_saida`, implementation `b1585b4bd8a64c92aa28455fc39b13c87993a067` at main `66e83062f1dd821b04a59b820fcc7e2712839f60`. No duplicate owner/EnginAsk caller will be written. It advances420f9e→420fb7 only for supported foreign/hidden/active-handle returns. Explicit four-u16 viewport words are needed at the volume call, including visible active handles. Missing data stops before volume; visible inactive handle stores F9 then raises the exact pending PostSound descriptor, with no fake backend/handle. Original full producer tests will compare all shared physical/economic/experience state and pending native arguments, count entries/resumes separately, and preserve earlier endpoints. Cleanup remains separate until this real handoff returns. Inventory precedes implementation.

## Stage 13: actual producer through conditional request

`producao_solicitada.calcular_tropa_com_solicitacao_no_mundo(producao,mundo,bonus,indice,*,janela=None)` calls the existing physical producer once, then actual core `voz_unidades.retomar_solicitacao_saida`. It returns `None` before completion or actual `SolicitacaoSaidaTropa` at `0x420fb7`, ready for separate cleanup. Provider implementation `b1585b4bd8a64c92aa28455fc39b13c87993a067` was inspected from integrated main `66e83062f1dd821b04a59b820fcc7e2712839f60`. Earlier API endpoints remain stable. No conditional caller or sound/volume/selection algorithm is duplicated.

Prior shared-state/loaded-table/one-shot contracts apply. Supply four loaded u16 viewport words when volume is reached. Actual foreign-owner/hidden branches can return without them; visible non-FFFFFFFF handles still query volume and store F9. Visible FFFFFFFF handles store F9, then raise exact pending PostSound data instead of inventing a backend/handle. Zero volume still leaves the request pending. Missing viewport stops before volume. Same-checkout voice/selection/movement imports happen only after placement, so import/volume/sound errors preserve earlier economic/unit/search/recovery/experience/physical/vision/minimap/order effects. Do not replay or process that building again. Cleanup remains separate and accepts only a returned420fb7 handoff.

Additive `evidencias/producao-solicitada.json` records exact original caller bytes, prior/core manifest identities and dependency checkpoints under unchanged EXE/SBL hashes. Native starts actual CalculTroupe and executes all original request/volume calls unpatched. Pending sound arguments use core's actual native decoder; CPU/flags/stack minimap resumptions and caps/timeouts are unchanged. No CALL/RET or callback result is replaced.

Commands: `python3 -B pesquisas-paralelas/economia/capturar_producao_solicitada.py`; `validar_producao_solicitada.py` locally and with `--emular`; required `python3 -B scripts/check.py --domain economy`.

Fresh result: 15 tests pass/no skips, **266 original entries in796 bounded segments with530 minimap resumes**. Outcomes:64 returns,144 cleanup stops,52 pending PostSound stops, four viewport stops and two late import stops. Native faults/limits/failures/errors are zero. All four building×26 output type combinations, ordinary owner/camera pairs, inherited handle values, hidden/foreign/local branches, viewport/selection/zero-volume arguments, inactive updates and four persistent sequences are covered. Full shared physical/economic/queue/search/routes/vision/minimap and owned recruitment/production state plus checked guards match; pending native arguments exactly match Python descriptors.

Four-building calibration (four entries/20segments) remains separate. Initial local report preserves one incorrect hidden fixture: byte0 is visible under core's low-five-bit rule; byte1f correctly represents hidden input. Fixture corrected without implementation change. Final local mode executes seven tests/skips eight optional methods; required economy gate passes377 discovered/172 optional skips and valid documentation links. Historical/earlier reports are unchanged; future explicit aggregate counts bounded segments. No substantive reasoning stall.

Global gap closed: actual producer→supported original conditional request→economic cleanup boundary, independently native-validated before integration. Sound insertion, full cleanup/terrain/AI messages and real mission remain open. No audio playback/mission completion claim. Overall approximate50% (40–60%) remains coordinator-owned. Publish exact feature/main hashes and common-check counts after the mandatory helper before another implementation.

## Stage 13 integration and Stage 14 selection

Integrated implementation `7fe62277516d4ebac77f1e862cb4a9b8f36f3b2b`, feature `7a43a7c9587074a34379315b4296fa8b68ce3335`, main `9e0efeaa8032cbef76f58236ebe2d34fff9501ae`; fresh fetch verifies all three on main. Required gate: core341/161 optional skips, combat219/137, economy377/172, graphics162/0, workflow3/0, total1,102/470. Clean feature resumed through helper before selection.

Stage 14 will join the actual producer/request result at420fb7 to existing `limpeza_saida.retomar_limpeza_saida`, without copying its predicates or core reset. Native starts real CalculTroupe and ends at the genuine terrain-query or unit-message boundary, preserving earlier effects and pending sound behavior. Retained-colonist fixtures use a distinct existing record, not duplicate references to the converted output. Cover count/capacity discrepancies, full shared state, exact reset order and late import failures. No sound/terrain/AI effect or complete production/mission claim is supplied. Earlier producer endpoints remain stable.

Naming correction: the original SBL name at41aee2 is `BatimentGetCase`; my Stage9 informal label `BatimentGetPosition` was inaccurate. Maintained prose is corrected. Original address/bytes/checkpoint/behavior remain unchanged, and the old manifest stays intact; add a separate identity-linked erratum. Core was notified. Inventory precedes implementation.

## Stage 14: actual producer through selective economic cleanup

`producao_limpa.calcular_tropa_com_limpeza_no_mundo(producao, mundo, bonus, indice, *, janela=None)` calls the existing actual producer/request exactly once, then the existing cleanup exactly once only after its real 0x420fb7 handoff. Return `None` for inactive/incomplete calls, otherwise frozen `LimpezaSaidaTropa` at the first terrain-query or unit-message boundary. Prior loaded-table, ordinary owner, shared unit/structure/terrain identity, viewport and one-shot contracts remain. No predicate, progress, request or core reset algorithm is duplicated; older API endpoints remain stable.

Capacity predicates ignore live count. Type 2 uses complete BagVide, falling back to type 9; types 1/13/16 use type 9. Retention resets with actual core, then stops at 0x4211d3 before iagUnitSendMessage0x4829c8, AX output unit/EDX70/EBX0. Empty types 1/2 reset now; empty 13/16 retain progress/activity until later. All empty paths stop at 0x42110c before original BatimentGetCase0x41aee2, AX building/EDX10 for type2 and8 otherwise. EteintTerrain0x476e82 and subsequent messages remain pending. Core reset import errors occur before the first inline store (0x421097 or0x42116e), preserving all prior economic/unit/search/recovery/experience/physical/vision/minimap/movement/request effects. Earlier viewport/PostSound dependencies propagate before cleanup. Never replay/tick pending or failed work.

New evidence binds original EXE/SBL identities, exact cleanup bytes and predecessor/core manifests. `evidencias/limpeza-saida-symbol-erratum.json` adds the original SBL record correcting the informal Stage9 label BatimentGetPosition to BatimentGetCase. Predecessor manifest hash is retained; original code/address/checkpoint/behavior and frozen evidence are unchanged.

Commands: `python3 -B pesquisas-paralelas/economia/capturar_producao_limpa.py`; `validar_producao_limpa.py` locally, with `--emular --quatro`, and with `--emular`; required `python3 -B scripts/check.py --domain economy`.

Fresh native result: 16 tests pass without skips/errors/failures, **332 original entries /1,504 bounded segments /1,172 minimap resumptions**. Outcomes:66 returns,125 unit-message stops,131 terrain-query stops,6 pending PostSound,2 missing viewport,2 late reset-import stops. Native faults/limits are zero. Independent earlier four-building calibration is four entries/20 segments and remains separate. All four building ×26 output types ×retention, eight remaining-type samples per building, ordinary owners/edge indices, states3/255, count/capacity differences, inactive cases, four persistent sequences and dependency timing are covered. Full shared physical/economic/queue/search/routes/vision/minimap state and owned recruitment/production/tables/guards match, with complete ordered effects and exact pending sound arguments. Local mode executes eight tests/skips eight optional methods. No historical report was rerun or rewritten.

Remaining colonists use distinct existing records, not duplicate output references. Stale count/capacity tests are raw-state cases, not coherent mission examples. Expanded native run completed during a turn interruption and its successful preserved report was inspected on resume. Helper resumed this same inspected dirty feature without discarding changes; current main will be merged by the clean-tree integration helper. No substantive mismatch/stall occurred. Canonical checkout was not modified by this chat.

Concrete gap closed: prepared actual producer → supported request → selective economic reset → first genuine terrain/AI dependency on shared loaded state. Natural recruitment startup/exit geometry, terrain cleanup, unit/building messages, sound insertion and coordinated real-mission dispatch remain open. No full production/mission claim or competing global estimate. Commit, integrate and publish exact feature/main ancestry and common gate counts before the next implementation.

Stage 14 required economy gate: 393 discovered tests pass, with 180 declared optional native skips; documentation links pass.

Final review corrected the new distinct remaining unit fixture: its owner belongs at byte +0, not +3. The earlier successful native report is preserved separately as `validacao-producao-limpa-emulada-primeira.json`; the final expanded native run uses the corrected fixture. No reconstructed algorithm changed.

### Stage 14 local integration preparation

Implementation `e1bbc3d5cc9f0441e56e96a203170b0341f09d2e` is committed. After automatic approval rejected the required feature/main integration helper for lack of accepted direct user authorization, the clean feature locally merged fetched main `6b15be1c96348d51dac7a46208126e6974290eca` as `778e2af653369f9d09a45a6c5b46ffa2d1cad822`. This is a local feature preparation, not a feature push or main integration. No failed candidate or native report was discarded.

Main brought core placement refactor `c84556f`. A fresh full Stage 14 native run against that merged provider passes all 16 tests, with the same 332 entries /1,504 segments /1,172 resumptions and declared outcomes, without skips, mismatches, faults or limits. The pre-main successful report is separately retained as `validacao-producao-limpa-emulada-antes-main.json`. Full common local preflight passes core350/166 optional skips, combat227/143, economy393/180, graphics169/0, workflow6/0: **1,145 discovered /489 optional skips**; documentation links pass. This preflight does not replace the required locked integration helper's final gate.

The human explicitly approved coordination messages after their initial automatic-review rejection; coordinator/core received the exact status and dependency requests. Feature/main push and merge remain subject to the separate final authorization requested in this chat. The stage must not be called integrated until the required helper and fresh ancestry checks succeed. No next implementation has started.

## Stage 14 integration

Integrated implementation `e1bbc3d5cc9f0441e56e96a203170b0341f09d2e`, feature commits `e64e29471243e44f0584635beb5c628ad41f204e` (validation against current core providers) and `94276dc0335f9d9e9430ba5321589a75cce31601` (main merge), main merge `aa873df6e930155fa3eae4c022249ab0c6fa2242`; all are ancestors of fetched `origin/main` (verified 2026-10-28 before Stage 15 began). The earlier "local integration preparation" note above is superseded: the locked helper integrated the stage after the human's durable authorization for this round.

## Compatibility with core's discovery extension (before Stage 15)

Core Stage 14 moves the normal-owner insertion vision boundary of `SetSortEngin` from a sum of 8 to 11 and publishes `insercao_unidades.SOMA_VISAO_MAXIMA_INSERCAO`. At core's request, `testes/test_producao_colocada.py` now derives its dependency-stop fixtures from that symbol (`LIMITE_VISAO`, falling back to 8 while the symbol is absent from main): the local stop uses vision `LIMITE_VISAO+1`, and the native `erro='visao'` matrix uses `(LIMITE_VISAO+1, level 0)` and `(LIMITE_VISAO, level 3)`, both sum `LIMITE_VISAO+1`. Before core lands the values are exactly the old 9/0 and 8/3. No reconstructed behavior or report changed. Verified on this branch: the local test file passes (13 discovered, 7 optional skips) and the native vision test reaches all eight original stops at `0x446146`. The unsaturated boundary matrix `(0,0),(7,3),(8,0)` remains inside both the old and the new domain.

## Stage 15: structure habitation for `MissionPlaceTerrain`

Delivered in `construcoes_habitaveis.py`; the full contract is in [ECONOMY.md](../../docs/ECONOMY.md#structure-habitation-for-missionplaceterrain-stage-15). Original-byte inventory: `evidencias/habitaveis.json` (20 intervals, 3 jump tables, 22 type records; EXE `6c5565…43fb`, SBL `c3a541…c627`; analysis PE `26c4534b…64d0` named, never executed). Original-only captures: `evidencias/captura-habitaveis-original.json`, 22 entries in 79 segments, committed as `7081ac9` before any translation.

**API for missions' structure scan** (`MissionPlaceTerrain 0x46c16d..0x46c1b8`). Missions keeps the loop, `BatimentExiste`, core `PlaceBatiment 0x41c4ac` and core `BatimentModifyMap 0x419e97(AX, EDX=1)`. Economy supplies:
- `HabitacaoConstrucoes(aprendizagem, *, unidades_realizaveis, estruturas_realizaveis)`.
  - Buffers are used by identity: `0x4dd6e8` technology Bags 9,152 bytes, `0x508f30`/`0x508f44` spells 20+20, `0x4e1934` unit realizability 104, `0x4dfad4` structure realizability 88, plus `0x4dfb2c` capacities and `0x4e2ea8` resources of the economy world.
  - The economy structure/unit pools must be the same objects as core's world.
  - All of these are inherited load state; the whole-load oracle supplies them. None is defaulted.
- `.estrutura_habitada(indice)` → AL 1/0 (`0x41a5b8`).
- `.tornar_habitavel(mundo, indice)` → `HabitacaoAplicada` (`0x41cc70`), called only when AL ≠ 0.
- AX inputs are u16 with protected index 0..999; structure type byte 0..21 for `BatimentHabitable`.

**Effects, in order:**
1. Technology Bag (complete `BatimentSetTechnologie`).
2. Types 17/9/12: `+0x84 = 200`, done.
3. Type 4: `+0x78 = 0`. Type 3 with owner < 4: warehouse level.
4. `BatimentGetCase`.
5. Core `descobrir_area(cell, R+3, owner)`.
6. Core `iluminar_area(cell, R, owner)`.
7. `+0x84 = 200`.

**Named dependencies and boundaries:**
- `DependenciaHabitacao` at `0x476851`/`0x476cb3` when R exceeds core's `RAIO_DESCOBERTA_MAXIMO_VALIDADO`/`RAIO_LUZ_MAXIMO_VALIDADO` (core will publish 23/20 in `visao_movimento`, re-exported by `insercao_unidades`/`colocacao_missao`; fallback 10/8 today).
- The same `DependenciaHabitacao` at `0x476851` for owner bytes ≥ 4 (the original aliases core's grid pointers).
- `ValueError` before any effect for type bytes > 21 (inherited EDI).
- `ZeroDivisionError` for the original type-3 `#DE`.
- Earlier effects are retained. Never replay.

**Cave identity.** Established from original tables: type 2 = `SANCTUAIRE`, type 3 = `CAVE` (`0x495d8c+0x13`, accessor `BatimentGetTypeName 0x418af7`; `BatimentInitCave` counts type 3 into `0x4dfb2c`). MONDE01's serialized structure is the sanctuary; centre cell `0x0c0e`. The coordinator was told and forwarded it to missions.

**Erratum.** `0x44724a` is SBL `BagContientTroupe`, not `BagVide` (`0x4470b9`). Maintained prose and docstrings are corrected; alias `bag_contient_troupe` was added, with no behaviour change.

**Validation.** Fresh native run on current main gates (10/8): 20 tests, 1,509 original entries / 1,571 segments / 62 minimap resumptions. Outcomes: 53 full returns, 101 discovery-gate stops (including MONDE01), 2 light stops, 1 expected `#DE`, 0 mismatches/limits/skips. A labelled diagnostic with core's announced 23/20 gives the same entries in 1,967 segments / 458 resumptions, and all 12 actual-MONDE01 caller configurations complete with whole-buffer equality. Local: 10 run / 10 optional skips. Required economy gate: 413 discovered / 190 optional skips; documentation links pass.

**Gaps.**
- Resolved after core Stage 14 (see below): actual MONDE01 now completes on main.
- `BatimentHabitable` callers `BatimentConstruction 0x41d000` and `BatimentLogeEngin 0x41fa81` are not composed.
- Stage 16 proposal: the `EnginInitTechnologie 0x441459` → `BatimentInitCave 0x419112` tail pair (InitCave is already reconstructed; its mission-world composition remains), then `PlayerRetrieve 0x46df41`.

**Cross-front records:**
- Core changed its discovery domain: `test_producao_colocada.py` follows `SOMA_VISAO_MAXIMA_INSERCAO` (`db77da6`, main `f18b5a0`). If no vision sum above the limit is representable (u8 255), the stop cases compare the original continuation instead.
- Core agreed that economy owns `BatimentGetCase`.
- Answer sent to AI/runtime (dispatcher branches; call shape: `eax` = zero-extended u16 index, return ignored):
  - Economy owns unit states 5 (`CalculWorkEngin`), 18 (`CalculTransporteEngin`), 7, 11, 15, 19, 20, 21 and 23.
  - Economy owns structure `CalculTroupe` (committed entry `producao_limpa.calcular_tropa_com_limpeza_no_mundo` for types 1/2/13/16; library via `aprendizagem`) and structure types 3/4, 7, 8, 17, 18, 19 and 20. Inside them, `CreerEngin` and physical lodging stay core, and `iagUnitSendMessage` stays AI/runtime.
  - Frame calls owned by economy: `RechercheCalcul`, `PlayerInitAllianceCompteur`, `PlayerAttaqueCalculSympa`, `SetUpdateChamp`/`UpdateChamp` (committed: `extracao.RecursosTerreno.agendar_campos`/`atualizar_campos`), `CalculMatiere`, `CalculCompteurMarche` and `CalculCompteurProposition`.
  - Graphics owns `NextAnim*`.
  - I proposed core for `DemonteBatiment 0x41effd`.
  - Unimplemented bodies must raise at their call sites.
- For missions' reset prefix: economy owns `MarcheResetAll 0x46027c` (selective reset exists: `ciclo_mercado.CicloMercado.resetar_todos`) and `BallonInit 0x441b6c` (not implemented; a named dependency until then). Pending missions' published call list.

## Stage 15 follow-up after core Stage 14

Stage 15 integrated as implementation `5aed3dfe94a16a94e03c9bceb4dd8437be9c710c` (evidence `7081ac94c5f36e96d7ef4ab29203ab776a072a24`), feature `c5237347d8eae9ce02108dc144fa5debcd0f4a9d`, main `7a60f54937fb1e7351a76dd85c8974627db06be4`. Ancestry was verified and the merge tree reproduced natively. Integration gate: core 357/169, combat 236/145, economy 413/190, graphics 184/0, missions 65/24, ai-runtime 3/0, audio 2/0, workflow 8/0.

Core Stage 14 landed at main `7b7b96960cee0ec7868914e811f51b851fc27dba`, publishing radii 23/20 and insertion sum 11. After merging it, results with no diagnostic override:
- **Structure habitation:** 20 tests, 1,509 entries / 1,967 segments / 458 resumptions. All 12 actual-MONDE01 caller configurations complete to `0x46c1a7`: `DecouvreTerrain(3086, 13, 0)`, `IllumineTerrain(3086, 10, 0)`, whole-buffer equality. 0 mismatches/limits/skips.
- **Captures:** local replay matches 21 of 22 original-only captures in full; the owner-4 boundary is the remaining one.
- **Producer placement:** same counts as Stage 12, with the vision stops now at sum 12.

The pre-core habitation report is preserved as `validacao-habitaveis-emulada-antes-core.json`; the producer report was byte-identical, so no copy was kept.

Further records:
- From AI/runtime: core owns `DemonteBatiment 0x41effd` (physical removal) and unit state 13. Economy owes the `DemonteBatiment` refund arithmetic as a callable query; until published it is a named dependency. `BatimentGetPlayer`/`BatimentGetType`/`BatimentEnDestruction` stay economy queries.
- Missions will consume the habitation contract in its Stage 11, after its reset-prefix Stage 10.
- Next, pending coordinator confirmation: Stage 16, the `EnginInitTechnologie 0x441459` → `BatimentInitCave 0x419112` tail, then `PlayerRetrieve 0x46df41`.

## Stage 16: economy MissionLoad initializer tails

Delivered in `cauda_carga.py`; the full contract is in [ECONOMY.md](../../docs/ECONOMY.md#economy-load-tails-of-missionload-stage-16). Inventory: `evidencias/cauda-carga.json` (14 intervals). Original-only captures: `evidencias/captura-cauda-carga-original.json` (22 fragment entries / 30 segments), committed as `8d0f2a9` before translation.

**API for missions' tail composition.**
- `CaudaCargaEconomia(habitacao, ciclo_mercado, *, rede, jogadores_guardados)`:
  - `habitacao` is the Stage 15 `HabitacaoConstrucoes`. Its economy world's `contagens_por_tipo` must be the same object as core's `mundo.realizaveis_estruturas` (`0x49a070`), and its `propriedade.ordens` is the `[0x4e19b8]` unit-order Bags (10,816 bytes).
  - `ciclo_mercado` is a `CicloMercado` over the loaded market buffers and the live player table `Mercado.jogadores` (`[0x5080a8]`); it must share the `Economia`.
  - `rede` is the byte at `0x4e0730`.
  - `jogadores_guardados` is the 80-byte source table `[0x5080ac]`.
  - `casos_cauda_carga.montar_cauda` shows the identity wiring.
- Calls in MissionLoad order: `.inicializar_tecnologia_unidades()` (`0x441459`), `.inicializar_cavernas(mundo)` (`0x419112`), [core `0x441623`], `.recuperar_jogadores()` (`0x46df41`), [ai-runtime `iaReset`], `.resetar_mercado()` (`0x46027c`).
- MissionLoadName replaces core and `PlayerRetrieve` with economy's `RechercheCalculNew 0x47150f`. It is not implemented, so it must raise a named dependency at `0x46c982`.
- Protected-domain `ValueError`s come before the call's stores. No call is replayed.

**Answers to the coordinator.**
- `MarcheResetAll 0x46027c` is exactly the committed `CicloMercado.resetar_todos`: same seven stores per player, same order, no difference. It is now also validated in tail position.
- `0x47150f` is `RechercheCalculNew`, owned by economy (research/technology); it is on the MissionLoadName path only, and was proposed as a separate later stage.

**Validation.**
- Fresh native: 11 tests, 435 original entries / 451 segments / 16 resumptions, every entry at its declared checkpoint, 0 mismatches/faults/limits/skips.
- Actual MONDE01 (four table/network configurations plus two chained after Stage 15 habitation) matches whole state. MONDE01 counts one sanctuary and no cave, so all warehouse words are 0.
- Local: 5 run / 6 optional skips; all 7 captures replay to full equality. Economy gate: 424 discovered / 196 optional skips.

**Stage 15 on core's main.** The actual-MONDE01 result is recorded in the Stage 15 follow-up above: main `04c7bfb`, 12/12 caller configurations complete through discovery 13 / light 10.

**Gaps.**
- `RechercheCalculNew` and its `InventionSetEffet 0x470f98`.
- `DemonteBatiment` refund query.
- Natural production start (next sequence item 2) and the transport/work cycle (item 3).
- Note for core: `0x49a070` holds per-owner, per-type counts of active structures (`BatimentInitCave`), not realizability flags. Only the name is misleading; no change is requested.
