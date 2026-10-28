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
