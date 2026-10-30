# Register queries and S1 provider completion

Status: **546 original-only query calls captured**, no game mutations or boundary calls, code unchanged; wrappers and differential pending. The completed S1 a/b/c comparisons are in [S1_GAPS](S1_GAPS.md).

## Query contract

Oracle: intact RISING.EXE SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

| Routine | Original range | Input | Result |
|---|---|---|---|
| EnginEstVivant | `0x443dad..0x443ddd` | AX unit index, protected domain 0..799; every state byte supported | Full EAX = 0 for state 0/4, otherwise 1; every other register preserved |
| BatimentGetDecalageConstruction | `0x41aea4..0x41aee2` | AL structure type, all 256 bytes supported | Full EAX = the construction offset for types 0..21, otherwise 0; every other register preserved |

Ranges are end exclusive. `0x4731d3` is EnginEstVivant's call instruction inside SetDechargeCaveEnginSelect, not its entry. The construction jump table is `0x41ae4c..0x41aea4`. Both helpers are read-only, have no callbacks, and return with ESP advanced by four. No life, owner, selection or activity guard is added beyond the original state test. Upper input bits are ignored exactly according to AX/AL.

The wrappers will reuse `SelecaoOrdens._vivo` and `selecao_ordens.DECALAGEM`, already used by the order setters and Economy. No second implementation of either rule is needed.

## Original-first fixtures

`validar_consultas_estado_core.py --capturar` opens S1's verified frame-11250 snapshot and runs 546 declared original leaf calls without advancing a frame. These are declared query fixtures, not new in-situ observations of the S1 callers. Each leaf records every exit register and ESP, its explicit state writes, every changed game byte, and non-stack native reads. Unread bytes remain unmapped during CPU-free replay; no artificial memory defaults are supplied.

- EnginEstVivant: 256 state bytes on slot 15, four state values each on slots 0/799, and four upper-word cases: **268**.
- BatimentGetDecalageConstruction: 256 AL values with high EAX bits plus every valid type with zero high bits: **278**.

The capture must be committed before the comparison; the driver enforces that its bytes equal the committed HEAD blob. Every native command uses `heavy_lease.py`. Original code intervals and the jump-table hash are recorded separately from the loaded-state fixture.

## Reuse across owners

- Economy `restauracao.Restauracao` / `provedor_restauracao`, implementation `f7ead23`, already covers all EnginRestaureEtat switch targets and forwards Core callees. Its published native counts are 58 restore calls within 92 isolated calls, and 804 composed comparisons (712 bodies plus the 92 isolated calls), zero mismatches. No additional Core restore body is owed.
- Combat `refugio_luta_combate.refugio_registradores`, exposed by `luta_fatal_viva_combate.LutaFatalViva.chamar` and `.provedores()`, implementation `072481d`, already covers ChercheBatimentProximiteCaveOuSanctuaire. Its published supplement compares two refuge calls with zero mismatches. It prefers any own CAVE, otherwise the nearest sanctuary; no maximum distance. Reuse that owner provider rather than copying it.

These owner counts are published evidence, not fresh Core executions. Consumers bootstrap through their owned `ambiente_*` module and inject the committed owner providers into the Core routing adapter. Owner source files and their current hashes are not pinned by Core tests.
