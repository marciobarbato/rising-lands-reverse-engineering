# Raw-memory recruitment owner adapters

Task scope: the five Core calls in Economy's complete `SortieTroupe`, reached by
AI/runtime's S1 producer at frame 2547. Original oracle: intact `RISING.EXE`,
SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
This delivery supplies owner callbacks; consumer wiring and whole-state S1 proof
remain AI/runtime's responsibility.

| Routine | Entry | SortieTroupe CALL | Required behaviour registers |
|---|---|---|---|
| EnginSetType | `0x457b87` | `0x420f69` | AX unit, DX cell, BL direction, CL type |
| EnginAddVie | `0x457122` | `0x420f75` | AX unit, DX increment (1000 here) |
| EnginResetFatigue | `0x4530fd` | `0x420f7c` | AX unit |
| EnginSetExperimente | `0x44fe42` | `0x420f85` | AX unit, DX exit cell (preserved) |
| SetSortEngin | `0x445fbc` | `0x420f8c` | AX unit, DX cell |

## Consumer protocol

The public entry is `recrutamento_core.RecrutamentoCore(memory, bonus=...)`
and `provedor_recrutamento(owner, outros=None)`, returning
`externo(nome, chamada, regs)`. Memory supplies `u8/u16/u32`, `ler` and writable
live `vista` (or the existing `segmentos` interface). No mission initialization,
synthetic bonus table, rollback or retry occurs.

Every omitted required argument raises `entrada_estruturas.ArgumentoNaoPassado`
before any reads or writes. Complete register inputs yield exact seven-register
outputs. The partial-register protocol also returns EAX/EBX/ECX/EDX/ESI/EDI/EBP;
missing preserved registers retain explicit `_incertos` masks. Known outputs
clear those masks even when their numerical value happens to equal the input.
Unknown bits in behaviour arguments are rejected; they cannot select game
behaviour. No pushed arguments are accepted. Optional ESP is entry ESP; direct
calls report ESP+4, while the callback protocol returns the seven data registers.

`bonus_recrutamento(memory)` exposes Economy's committed live
`BonusUnidades.consultar` as `(owner, type, selector) -> value`; every query
reads the current buffers. The conversion owner requires this callback and
never supplies zero as a missing bonus. Conversion's selectors are 12 (type 4)
and 1 (capacity). Economy/Combat remain the owners of their underlying bodies.

## Consumer dependencies

Economy currently omits EBX from `ARGUMENTOS['EnginSetType']`; forward the actual
BL preserved by CalculPosition. It also omits EDX from `ARGUMENTOS['SetSortEngin']`;
the intact routine consumes the exit cell in DX, preserved by EnginSetExperimente.
Forward that actual cell at `0x420f8c`. Core must not fabricate either input.
The city-message callback at `0x4211e5` remains an AI/runtime dependency after
these five calls; it is outside this delivery.

## Original-first validation

`ferramentas/validar_recrutamento_core.py --capturar`, through the heavy lease,
replays the three complete Economy CalculTroupe fixtures (297, 869, 1363),
checks each owner's argument registers against the immutable capture, and
executes the unpatched calls at their actual SortieTroupe sites. It then
replays S1 from snapshot 2500 through frame 2547, verifying every frame against
the committed original trajectory, observes the same five sites, and runs
declared original leaves from those entry states with the trajectory restored.
The capture was committed as `8e5e2a5` before the new adapter was implemented or compared.
The subsequent native differential reexecutes those cases, compares exact
capture reproduction, all seven exits/ESP and every changed non-stack byte,
and checks both complete and partial-register provider routes. Native faults,
instruction limits and unexpected dependencies fail the run. Three Python
routes do not multiply the native case count. No test pins foreign source bytes.

## Implementation and supported domain

`RecrutamentoCore.chamar(nome, regs, pilha=())` requires all seven input
registers; the external adapter accepts the partial protocol described above.
`EnginSetExperimente` additionally requires DX in the external adapter: although
the routine preserves it, it is the live continuation cell, so it must be
available for the next owner call. Its full EDX is returned unchanged; omitted
upper bits can remain marked unknown in `_incertos`.

Inputs truncate to the widths in `ARGUMENTOS`. Unit indices are protected to
0..799; conversion types 0..25; conversion/placement owners 0..3, 4 and 200;
experience owners 0..3. Healing requires live type 0..25. Placement requires
loaded width/height 1..256, an in-map cell, local player 0..3, 128×128 minimap,
and normal-owner vision sum BB+F5 ≤ 11. A larger sum stops at `0x446146` after
collision and visibility stores, before discovery. These are protected loaded
memory domains, not a mission loader or a claim for arbitrary malformed state.
Full EAX outputs depend only on known low-width inputs and loaded memory:

| Routine | Changed exit registers | Preserved data registers |
|---|---|---|
| EnginSetType | EAX capacity+bonus, EBX `0x1d`, ECX record+10, EDX `0x1e` | ESI, EDI, EBP |
| EnginAddVie | EAX maximum-life word with AL clamp flag; EDX record | EBX, ECX, ESI, EDI, EBP |
| EnginResetFatigue | EAX record | EBX, ECX, EDX, ESI, EDI, EBP |
| EnginSetExperimente | EAX owner×10 on no match/empty, owner×5 after consumption | EBX, ECX, EDX, ESI, EDI, EBP |
| SetSortEngin | EAX/EDX from the final native-equivalent SetMiniMap | EBX, ECX, ESI, EDI, EBP |

Conversion reuses the same committed Combat `definir_tipo` body as
`incursao_core.definir_tipo_unidade`, with a writable live record instead of
the older raid adapter's copy. Therefore a live bonus query observes prior
conversion stores, and a callback exception retains them. The capacity query
is `incursao_core.capacidade_tipo_engin`; neutral-owner bonus uses the live
Economy bypass. Bonus providers are read-only queries; they must not mutate
shared state. Characteristic bytes retain the original low-byte reads.
Healing reuses `curar_com_limite`: store the wrapped sum, read the live maximum,
then store the clamp only if strictly exceeded. Fatigue clears +74 then copies
+76 to +04. Experience stores AF, applies the existing F5–F8 rules using
`experiencia_unidades.TIPOS_F7`, then shifts each experience byte before its
type byte and finally stores queue tail 0/255. A failed characteristic read
retains AF and leaves the queue unshifted.

Placement stores +7e/+7c/+08/+7e, releases a matching search, clears +88,
sets active (not state 0/4) units to state 7, clears orders/animation, runs
`definir_colisao_unidade`, stores visibility +72, then discovery, light and
mode-4 minimap. It does not remove previous occupancy. The discovery/light
body is the existing `VisaoMovimento`, bound through the lazy flat-memory
`visao_grupos._MinimapaPlano` plus live light counts; it does not require
unrelated path solver/Bag/selection allocations to be present. Final minimap
uses `incursao_core.definir_minimapa`, including its exact EAX/EDX. None of the
five adapters calls movement, sound or messages; the producer owns that order.

For AI/runtime's `DonosM3`, construct once on the same live memory:

```python
from recrutamento_core import RecrutamentoCore, bonus_recrutamento, provedor_recrutamento
recruit_owner = RecrutamentoCore(m, bonus=bonus_recrutamento(m))
recruit_callback = provedor_recrutamento(recruit_owner, outros=existing_owner_route)
# Route these five original names through recruit_callback(nome, chamada, regs).
# Use the caller's owned ambiente_* bootstrap / integracao.providers as usual.
```

A supplied live `(owner, type, selector)` bonus callback may be used instead.
No foreign file or consumer is edited in this delivery. DX must be forwarded
into SetSortEngin by Economy before the complete chain can use this provider.

## Final validation

Fresh leased native differential: **277 comparisons, zero mismatches**, 154.25 s;
exact committed original capture reproduced, all seven registers/ESP and every
changed non-stack byte equal. Counts: EnginSetType **57/0**, EnginAddVie **83/0**,
EnginResetFatigue **11/0**, EnginSetExperimente **103/0**, SetSortEngin **23/0**
(cases/mismatches). Full and partial provider routes agree on all known bits;
the original cases are counted once. All native cases returned, with no native
faults, instruction limits, boundary requests, skips or dependency stops. The
protected radius stop is exercised separately by the focused Python tests.

Reproduce with:

```sh
python3 '/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py' core-recruit-differential -- python3 -B ferramentas/validar_recrutamento_core.py
python3 -B scripts/check.py --domain core
```

Evidence: [original-only capture](../../evidencias/recrutamento-core/original.json.xz),
[native differential](../../relatorios/recrutamento-core-emulada.json).
Tests bind this report to Core sources and the owned capture only. The report's
foreign capture hash is provenance, not a foreign source/version requirement.
These isolated owner proofs do not establish a completed S1 producer, input
chain, M3/M4 acceptance or whole-state Python S1 equality.

Final Core gate: **608 discovered tests, 215 optional skips, zero failures**,
32.396 s, documentation links passed. `git diff --check` and module-basename
uniqueness checks passed.
