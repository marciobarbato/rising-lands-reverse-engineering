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
| EnginSetExperimente | `0x44fe42` | `0x420f85` | AX unit; EDX is preserved (exit cell here) |
| SetSortEngin | `0x445fbc` | `0x420f8c` | AX unit, DX cell |

## Consumer protocol

The planned public entry is `recrutamento_core.RecrutamentoCore(memory, bonus=...)`
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

`bonus_recrutamento(memory)` will expose Economy's committed live
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
The capture is committed before the new adapter is implemented or compared.
The subsequent native differential reexecutes those cases, compares exact
capture reproduction, all seven exits/ESP and every changed non-stack byte,
and checks both complete and partial-register provider routes. Native faults,
instruction limits and unexpected dependencies fail the run. Three Python
routes do not multiply the native case count. No test pins foreign source bytes.
