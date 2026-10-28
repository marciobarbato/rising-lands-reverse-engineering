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
