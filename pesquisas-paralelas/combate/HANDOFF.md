# Combat handoff — 2026-10-28

Chat: `01a18262-bf98-7530-a8d2-ea4fe025dad8` (local). Worktree: `/Users/marcio/git/Rising Lands/worktrees/re-combat`. Branch: `feat/re-combat`. First slice starts at organization revision `6634be3af2d255846a847d8aa21ad4edf1cdb589`.

## Completed slice: mode-1 unit damage consumer

`consumo_dano.ConsumidorDanoUnidade.infligir(victim, mode, attacker, direction=0)` consumes the original `EnginInfligeDegat` mode-1 path. Supply 800 live writable 276-byte records and 26 damage rows containing at least 26 u8 entries. IDs truncate to u16 then require 0..799, mode truncates to u8 then requires 1, and both unit types require 0..25. Direction has no effect in mode 1. Unsupported inputs fail before callbacks/writes. `None` means a nonlethal consumer return.

Exact query/effect signatures, field widths and ordering are published in [COMBAT.md](../../docs/COMBAT.md#occupied-unit-damage-consumer). Callbacks take `(name, arguments_tuple)` and may mutate records in place/context, without replacing world/row pointers or record objects. Source matrix and `+0xF7` are saved before modifier 5. The proximity predicate conditionally adds the global u8 bonus. The AI message precedes reduction and life loss. Modifier 6 uses the attacker's reread owner/type, whereas reduction `+0xF6` belongs to the victim. Visibility precedes volume, the `+0xF9` reset and optional sound. Protection bit 3 decrements the byte after its negative clamp. Life subtraction uses signed damage and u16 storage, including zero-protected healing/wrap.

Missing query/effect providers raise at the call boundary with prior effects retained. `LimiteMorte` identifies original address `0x4506A1`, victim, attacker and signed damage, before the death branch executes or writes life zero. Lethal life is unchanged by this adapter; earlier message/audio effects remain.

The callback-connected type-9 impact scenario stops at the consumer return (`0x450DA5`) inside the world wrapper. Native `ProjectileAvance`/`ProjectileInfligeDegat`/`InfligeDegat` choose the victim; the Python fixture receives that independently captured ID. Four direction bytes produce the same whole unit/projectile buffers at that checkpoint and life 100→80. Parent retirement, cell-wrapper aftereffects and RNG are beyond this checkpoint. This is not a full battle or completed world wrapper.

## Original evidence

Original Brazilian `RISING.EXE` SHA-256: `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`. Consumer: `[0x4502F0,0x450856)`, mode-1 body `0x4503B8`, nonlethal return `0x45084F`, death boundary `0x4506A1`. Existing projectile/wrapper ranges remain unchanged. [New range manifest](evidencias/consumo-dano.json) records nine newly extracted ranges and their individual hashes, including proximity, unit lookup, visibility, volume, selection, player type and the message's non-AI return. `rastrear_consumo_dano.py` verifies the original hash before extraction and writes only the new evidence files.

No evidence, immutable manifests, original media, predecessor reports or other owner's source was edited. The core arithmetic is reused from committed `ferramentas/combate.py`. The proximity symbol's name does not establish a captain/type filter; queries retain original identifiers and argument order.

## Actual validation for this slice

- `python3 -B pesquisas-paralelas/combate/rastrear_consumo_dano.py`: nine hash-grounded extracts.
- `python3 -B pesquisas-paralelas/combate/validar_consumo_dano.py --emular`: **11 tests, 763 bounded original-x86 executions, zero failures/errors/skips**. Includes all 26×26 source/victim type pairs, fixed-width life/protection boundaries, ID edges/self-alias, native query results and whole 220,800-byte unit buffers. Eight of those executions are the four projectile/consumer entry-and-resume pairs, also comparing all 5,600 projectile bytes.
- Expected stops: **257** death entries at `0x4506A1`, **4** audio entries at `0x48AA79`, and **4** pipeline checkpoints at consumer return. No unexpected exceptions or execution limits in the final run. Original message no-op, modifiers, proximity, visibility, volume and selection execute without instruction/register replacement. An explicitly synthetic mutation injected at the message callback boundary tests rereading; it does not claim that the original non-AI message body makes those changes.
- `python3 -B pesquisas-paralelas/combate/validar_consumo_dano.py`: **11 tests, 6 optional x86 skips, 0 x86 executions**, no failures/errors.
- `python3 -B scripts/check.py --domain combat`: **124 tests, 76 optional x86 skips**, no failures/errors; documentation links passed. The prior 234,245-execution suite was not rerun or relabeled as fresh coverage.
- Restricted-sandbox reference attempts exited **132/SIGILL** during Unicorn initialization, after local cases but before x86 coverage. The approved ordinary execution context ran the final successful reference suite. During fixture development, 0xFFFF was caught as a building and `+0xAB=1` was caught as incompatible with flag-0 unit lookup; corrected fixtures use natural-zero cells and the original stratum filter. Original bytes were unchanged.

Reports: [reference](validacao-consumo-dano-emulada.json), [local](validacao-consumo-dano-local.json). Integration is performed from the clean feature tree by `python3 scripts/workstream.py integrate combat`; exact feature/main merge hashes are reported in the coordinator chat after success, without amending a commit to contain its own hash.

## Evidence-backed remaining inventory and next priority

| Subcomponent | Evidence / implemented state | Remaining work |
|---|---|---|
| Cell impact wrapper | `InfligeDegat`, `0x450874..0x4510DD`; now natively captured through an occupied consumer return | Reconstruct unit lookup/reaction/aftereffects around the consumer using explicit callbacks; building branch remains separate |
| Unit damage modes | Complete original extract at `0x4502F0..0x450856`; only mode 1 translated here | Building/magic/mine/other mode preparation; determine initialized versus undefined input domains |
| Lethal effects | Stop at `0x4506A1`; original zero-life/death calls occur later | Preserve experience, world lifecycle, messages and effect order with core-owned deletion callbacks |
| Attack phase producers | Existing field audit found direct writes 0/1; no 2/3 in 2,604 serialized ETA records | Trace indirect writes/callers without inventing `+0x8A=2/3` transitions |
| World providers | Existing combat calls remain explicit | Core world lookup/navigation/lifecycle, message bodies, modifiers and sound providers; real building geometry |
| Runtime/mission integration | No game/runtime is started by these harnesses; preview uses old pinned snapshots | Coordinate committed mission state/caller dispatch and runtime operation in a maintenance-owned consumer |

Highest-value next slice: the mode-1 **unit branch of `InfligeDegat`** around the now validated consumer, prioritizing exact cell lookup → optional reaction/navigation requests → consumer → hit/diplomacy callbacks. It will not implement navigation, building allocation or audio. The next slice starts only after this clean candidate integrates; the same inspected feature worktree/branch is resumed with the helper as directed by the continued research authorization.
