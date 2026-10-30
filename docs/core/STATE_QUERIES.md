# Register queries and S1 provider completion

Status: **546 original-only query calls, 546 CPU-free replays and 546 fresh native comparisons, zero mismatches**, no game mutations or boundary calls, code unchanged. Direct calls and both provider routes match every seven-register exit; direct calls also match ESP. The completed S1 a/b/c comparisons are in [S1_GAPS](S1_GAPS.md).

## Query contract

Oracle: intact RISING.EXE SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

| Routine | Original range | Input | Result |
|---|---|---|---|
| EnginEstVivant | `0x443dad..0x443ddd` | AX unit index, protected domain 0..799; every state byte supported | Full EAX = 0 for state 0/4, otherwise 1; every other register preserved |
| BatimentGetDecalageConstruction | `0x41aea4..0x41aee2` | AL structure type, all 256 bytes supported | Full EAX = the construction offset for types 0..21, otherwise 0; every other register preserved |

Ranges are end exclusive. `0x4731d3` is EnginEstVivant's call instruction inside SetDechargeCaveEnginSelect, not its entry. The construction jump table is `0x41ae4c..0x41aea4`. Both helpers are read-only, have no callbacks, and return with ESP advanced by four. No life, owner, selection or activity guard is added beyond the original state test. Upper input bits are ignored exactly according to AX/AL.

`consultas_estado_core.ConsultasEstadoCore(memoria).chamar(nome, regs, pilha=())` reuses `SelecaoOrdens._vivo` and `selecao_ordens.DECALAGEM`, already used by the order setters and Economy. No second implementation of either rule is introduced. `regs` must contain EAX/EBX/ECX/EDX/ESI/EDI/EBP; optional ESP is the entry return-slot address. The returned dictionary contains every input register and, when supplied, ESP+4. Nonempty pushed arguments are rejected. The wrapper protects unit indexes above 799 before memory reads.

`provedor_consultas_estado(consultas, outros=None)` exposes `externo(nome, chamada, regs) -> seven registers`. All seven are required, including preserved registers; omission raises `ArgumentoNaoPassado` with the original call address before reads/effects. Unknown names are forwarded unchanged to `outros`, or raise. Flags/control flow are outside this seven-register provider protocol.

## S1 routing provider

`provedores_lacunas_core.provedor_lacunas_s1(memoria, *, som=None, restauracao=None, refugio=None, outros=None)` returns the same `externo` protocol. It serves all 16 surveyed Core gaps plus the two queries above, on the caller's live buffers, without initialization/copying. It uses the validated `BuscasBloqueios` and `ConsultasLuta` bodies. All seven registers are mandatory. ChercheGcLibre, BatimentGetCaseAdjacent and EnginRestaureEtat also require entry ESP; unavailable stack residue raises a named dependency instead of publishing guessed zero bits. Outputs contain exactly the seven registers.

`restauracao` and `refugio` are injected callbacks with the same `externo(nome, chamada, regs)` signature. The adapter forwards the complete register file and the exact original call address once, preserving store/callback order. A callback exception propagates, retaining earlier stores; there is no retry/rollback. Missing owner providers, incomplete returned registers or `_incertos` bits raise `DependenciaLacunaS1`. No owner body is copied into Core. Unknown names go to `outros` unchanged or raise the same explicit dependency.

Bind Economy's `provedor_restauracao(restauracao_obj)` directly. For Combat, use `refugio=lambda nome, chamada, regs: fatal.chamar(nome, regs, chamada=chamada)` with its committed `LutaFatalViva` instance, or adapt the committed `refugio_registradores(memoria, regs, chamada=chamada)` directly. Use the consumer's owned `ambiente_*` bootstrap before importing these providers.

Read-only queries/searches/blocking tests store nothing. List/task mutation and StopSound-before-PostSound order remain as recorded in [S1_GAPS](S1_GAPS.md). Owner mutation order remains the owner's published contract.

## Original-first fixtures

`validar_consultas_estado_core.py --capturar` opens S1's verified frame-11250 snapshot and runs 546 declared original leaf calls without advancing a frame. These are declared query fixtures, not new in-situ observations of the S1 callers. Each leaf records every exit register and ESP, its explicit state writes, every changed game byte, and non-stack native reads. Unread bytes remain unmapped during CPU-free replay; no artificial memory defaults are supplied.

- EnginEstVivant: 256 state bytes on slot 15, four state values each on slots 0/799, and four upper-word cases: **268**.
- BatimentGetDecalageConstruction: 256 AL values with high EAX bits plus every valid type with zero high bits: **278**.

The capture must be committed before the comparison; the driver enforces that its bytes equal the committed HEAD blob. Every native command uses `heavy_lease.py`. Original code intervals and the jump-table hash are recorded separately from the loaded-state fixture.

Capture commit: `ab9bb7d`, before wrapper implementation. Capture time 111.32 seconds; fresh differential 104.26 seconds. Reports: `evidencias/lacunas-s1/consultas-estado-original.json.xz`, `relatorios/consultas-estado-core-emulada.json`. Both routines have zero mismatches (268 / 278 cases respectively). These are 546 native calls compared through three interfaces, not 1,638 native calls. The same 546 native read sets replay without Unicorn. Tests detect a changed state rule, construction table and preserved EDX; they also check every omitted register, complete owner forwarding and retained stores on callback failure. No native faults, dependency stops, skipped query cases or changed-code executions occurred.

Original code hashes: EnginEstVivant `86d5313b2dabe2b67b5019eb0dfbcd7600ada43f681f26186d0b6111408907f0`; construction-offset body `41eb0b671cabaff25da6c4c837a83e2f92584040fe7cbe7d4036719dd85b4756`; jump table `040e1af18b93888fe6e3ef7a274dc5f275edd724377af7f325686f36297876de`.

## Reuse across owners

- Economy `restauracao.Restauracao` / `provedor_restauracao`, implementation `f7ead23`, already covers all EnginRestaureEtat switch targets and forwards Core callees. Its published native counts are 58 restore calls within 92 isolated calls, and 804 composed comparisons (712 bodies plus the 92 isolated calls), zero mismatches. No additional Core restore body is owed.
- Combat `refugio_luta_combate.refugio_registradores`, exposed by `luta_fatal_viva_combate.LutaFatalViva.chamar` and `.provedores()`, implementation `072481d`, already covers ChercheBatimentProximiteCaveOuSanctuaire. Its published supplement compares two refuge calls with zero mismatches. It prefers any own CAVE, otherwise the nearest sanctuary; no maximum distance. Reuse that owner provider rather than copying it.

These owner counts are published evidence, not fresh Core executions. Consumers bootstrap through their owned `ambiente_*` module and inject the committed owner providers into the Core routing adapter. Owner source files and their current hashes are not pinned by Core tests.

Final Core gate: 598 discovered tests, 215 optional skips, zero failures; documentation links and whitespace checks passed. New module basenames are unique across the research and app namespaces. The unchanged historical optional native corpus was not rerun.

## Remaining scope

The 16 surveyed Core names now have validated bounded bodies or committed owner providers, with no duplicate restore/refuge implementation. The complete reconstructed S1 chain and M3.1/M4.1 acceptance remain consumer/coordinator work. Search radius/type limits from S1_GAPS, required readable stack state and Audio/owner dependencies remain explicit. Captured read-only queries protect AX indexes above 799; this is not an emulated successful native return for an invalid pool access. This delivery (`3f3913f`) was integrated on main at `71335aa` by the coordinator. AI/runtime routes all three providers through `DonosM3.externo` on `feat/re-ai-runtime` (`d2777b1`), not yet on main.
