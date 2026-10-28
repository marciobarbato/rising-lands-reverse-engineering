# Bounded physical dying transition

`iniciar_morte_unidade(mundo, indice)` in [morte_unidades.py](../../ferramentas/morte_unidades.py) recovers ordinary-unit physical returns of original `SetDyingEngin` (`0x444938..0x444dad`, end exclusive). `MundoFisico`/`MundoNavegacao` expose the same method. It supplies a bounded physical provider for combat's lethal caller; it is not complete death, corpse removal, or mission simulation.

The [original evidence](../../evidencias/morte-unidades/manifesto.json) records 14 code intervals and the seven-entry effect table at `0x44491c`. Original executable SHA-256: `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`. Evidence includes the complete caller body, `GetBit`, no-effect AI/audio guards, discovery query, deselection, collision removal and shared epilogues. The native benchmark executes these supported nested calls unchanged; it does not replace them with mocks.

## Inputs and complete supported returns

`mundo` is a core physical/navigation world with the live writable 800 × 276-byte unit pool, occupancy/regions, discovery grids, owner-control bytes and navigation search. Integer `indice` truncates to u16, matching original AX, then must be 0–799. Invalid pool/index raises `ValueError` before mutation. A participating transition requires known type 0–25 and local camera 0–3; unsupported type/camera inputs are protected `ValueError`s before effects, not original eligibility checks.

The original branches on bit 2 of u8 unit `+dc`. With that bit clear, state bytes 0 and 4 return immediately and leave all world state unchanged, including malformed/unresolved fields that are never consulted. This guard also accepts inactive records with unknown type bytes. If the bit is set, a distinct state-0/vision/minimap/effect path is required and remains explicitly unsupported.

For an active ordinary path (state neither 0 nor 4), the currently complete domain is:

- AI message `0x44` has no group effect: owner control is not 2, or unit u32 group `+10c` is `ffffffff`. Original `PlayerGetControle` treats owners ≥4 as control 2.
- Sound handle u32 `+104` is `ffffffff`, so actual `PlaySnd_StopSound`/`HandleSnd_StopHandle` returns without effects.
- Current cell u16 `+08` is hidden for the local camera: its discovered-map byte has a nonzero `0x1f` mask. The original `TerrainEstDecouvert` query then skips death sound generation.
- Embedded Bag count u16 `+0a` is zero, unit selected byte `+bd` is zero, and type is outside 11–17.

Thus complete participating types are 0–10 and 18–25 under the stated guards. No building, alliance, life threshold, requested destination or already-dead collision repair is invented. The function returns `None`; incidental x86 register values are not modeled.

## Exact effects and original order

1. Apply the original activity/bit guards, no-group message bypass, inactive sound guard and discovery query in that order. These supported nested calls mutate nothing.
2. Write u8 state `+02=4`. If this is the current navigation-search unit, clear the search unit reference, occupied/success bytes and route pointer; preserve `busca.concluida`.
3. Inspect the Bag count. The original would repeatedly call `EnginRetire` while nonzero; the unsupported branch stops here after the preceding state/search effects.
4. With an empty Bag, the repeated active-state assignment in the original is now a no-op because the record is already state 4. Clear u8 animation frame `+a4` and u16 `+c2`.
5. Call the original deselection behavior. For `+bd=0` this is a no-op. For nonzero selection, clear `+bd` before stopping at the still-unimplemented selection-counter helper.
6. Remove collision at current u16 cell `+08`, then at reserved/step u16 `+7c` only if it differs. The implementation reuses core's already reconstructed occupancy primitive. Attribute masks, compact natural-region slots and unit labels follow that primitive; planned routes are not cleared or replayed.
7. Types outside 11–17 reach the actual original shared return. Types 11–17 require a following Random/projectile effect and stop explicitly after physical cleanup.

This body does **not** zero u16 life `+9a`; combat's preceding caller owns that write. Life is preserved even if a caller invokes this transition on a unit with positive life. The supported path also preserves attack phase/wait bytes `+8a/+8b`, direction, type, owner, current/reserved coordinates, route buffers, task-group memory, vision counts and minimap content. Physical collision is removed without pretending corpse animation or its final removal is complete.

## Explicit dependency stops

`DependenciaMorteUnidade` subclasses `NotImplementedError` and exposes `unidade`, `efeito`, `endereco` (missing body/branch) and `checkpoint` (native comparison stop). There is no automatic dependency success, rollback or entry retry. In particular, after state 4 is written, calling this entry again can return immediately without finishing collision cleanup. A caller must propagate/record the pending continuation rather than replay combat or this whole entry.

| Dependency | Native comparison checkpoint | Earlier effects retained |
|---|---|---|
| `+dc` bit-2 branch | `0x444c7e` | none |
| `iagUnitSendMessage` group handling | `0x482c58` | none |
| `PlaySnd_StopSound` active-handle handling | `0x48a446` | preceding no-group bypass only; no mutations |
| `EnginGetVolume`/death sound for discovered cell | `0x440c5d` | no prior record/world mutation |
| `EnginRetire` for nonempty Bag | `0x443dfc` | state 4 and matching-search release; collision/frame remain |
| `RetireSelectionEngin` counters | `0x472683` | state/search reset, `+a4=0`, `+c2=0`, `+bd=0`; collision remains |
| `Random(0x41)` and effect for types 11–15/17 | `0x4704dc` | all supported local/physical cleanup; RNG has not executed |
| `ProjectileInit` type 34 effect for type 16 | `0x46e44c` | all supported local/physical cleanup; effect has not executed |

The complete `SetDyingEngin` body also contains the distinct bit-2 state-0 branch, lighting/minimap teardown and other effects; none is inferred from its name. The native type-11–17 dispatch table, rather than visual interpretation, establishes the effect boundary.

Combat integration must share the same unit storage: if its API uses 800 records, writable `memoryview` records over `mundo.unidades` preserve that identity. Copying records into another list would disconnect its preceding life write and this physical transition. A callback can invoke `mundo.iniciar_morte_unidade(victim)` for the supported domain; it must retain the explicit exception behavior for other branches. This stage does not change combat's lethal caller or its level/projectile/sympathy logic.

## Actual validation

```sh
python3 -B ferramentas/extrair_morte_unidades.py
python3 -B ferramentas/validar_morte_unidades.py --emular
python3 -B ferramentas/validar_morte_unidades.py
python3 -B scripts/check.py --domain core
```

The [new native report](../../relatorios/morte-unidades-emulada.json) passes 10 tests and 283 bounded executions: 264 complete original returns and 19 explicit dependency stops. Complete participating cases cover all 19 ordinary supported types, indices 0/799 with poisoned upper EAX bits, states 1/7/14, and equal/distinct current/reserved cells. Additional inactive/control tests include states 0/4 with type 255, owners 0/3/4/200 and control bytes 0/2/255. Six guard/local dependency kinds are tested at indices 0/799; all seven effect-producing types reach their exact post-cleanup dependency. Entire unit/structure/group/search, terrain/occupancy/region, route, visibility/light and minimap buffers are compared. No native subcall is patched or skipped to claim a successful return.

The 19 Python dependency exceptions are intentional matches to the reported native checkpoints. Native exceptions, instruction/time limits, failures, errors and skips are zero. The [local report](../../relatorios/morte-unidades-local.json) discovers 10 tests, executes six Python tests, skips four optional x86 tests and runs zero x86. The core check passes 280 discovered tests with 134 optional-x86 skips. Historical x86 aggregates and an original game/real mission were not rerun.

The global gap addressed is a concrete shared-world physical dying provider for the declared ordinary-unit domain, independently validated before integration. AI group effects, sound, carried-unit/resource removal, selection counters, vehicle effects, special-flag teardown, level changes, final corpse removal and coordinated real-mission runtime remain open dependencies.
