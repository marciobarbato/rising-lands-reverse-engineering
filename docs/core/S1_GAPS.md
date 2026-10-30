# S1's Core gaps: work-cycle searches, path-search blocking, first-fight queries

[S1_COVERAGE](S1_COVERAGE.md) lists 16 Core routines that S1 reaches with no native differential on main. This stage targets 14 of them, original-first, on the S1 trajectory itself.

**Status (resumed under Codex, 2026-10-30):**
- Captures `a` and `b` are committed.
- Capture `c` was committed as `c162e68` before comparison. Its native differential passes **652 comparisons, 0 mismatches**; 1,251 S1 frame states reproduced, original code unchanged.
- Window `a` is natively validated: **638 comparisons, 0 mismatches**, all seven registers, ESP, changed bytes and boundary requests; 951 S1 frame states reproduced, original code unchanged. Report: `relatorios/lacunas-s1-a-emulada.json`.
- Window `b` is natively validated: **120 comparisons, 0 mismatches**; 1,201 S1 frame states reproduced, original code unchanged. Report: `relatorios/lacunas-s1-b-emulada.json`.
- All three windows total **1,410 comparisons, 0 mismatches**. The strict S1 routing provider and two requested query wrappers add **546 fresh native comparisons, 0 mismatches** (EnginEstVivant 268, BatimentGetDecalageConstruction 278), also replayed without a CPU. Total fresh comparisons: **1,956**. See [STATE_QUERIES](STATE_QUERIES.md).
- Integrated on main at `71335aa` (Core `3f3913f`). AI/runtime's consumer wiring (`d2777b1`) is on `feat/re-ai-runtime`. "Resume" below now only reproduces the windows; open stops and next steps are in [CORE.md](../CORE.md#current-state-2026-10-30-0715).

## Bench: S1 resumed from its own snapshots

`ferramentas/bancada_s1.py` opens Missions' scripted-input oracle (`entrada_roteirizada.abrir`) from an S1 pass-2 snapshot, with the S1 input installed. Those snapshots come from the Mac mini's `.local/m3/passo2/S1`, one every 250 frames; local copies live in the ignored `.local/m3/passo2/S1/`, and the F0 checkpoint in `.local/m3/quadro128/`.

- **Frame loop.** Frames run exactly as `entrada_roteirizada.correr` runs them.
- **Frame check.** Every frame is checked against the replay-checked S1 record (`quadros.jsonl` at feat/re-missions `82ec5ea`): counter, the three RNGs, DGROUP SHA-256 and whole-state SHA-256. A capture taken here is therefore a capture of S1.
- **In-situ observation.** It is passive:
  - a code hook at each routine's entry snapshots the registers and the whole mapped state, stack page included;
  - hooks at the routine's static return sites (every `call rel32` + 5) close the case;
  - the case then records the exit registers, the changed bytes and the boundary calls.
- **Variants.** Declared variants run the original as leaf calls between frames, from saved in-situ entry states. The state is restored afterwards.

`ferramentas/validar_lacunas_s1.py` is the capture and native-differential script. It runs one window at a time:

| Window | Frames | Routines |
|---|---|---|
| `a` | 2250–3200 | ChercheVeget and ChercheGc (CalculWorkEngin, 2352/2407), ChercheGcLibre (3116), TypeEnginPeutEcraser, IsIndirectlyBlocking and IsDirectlyBlocking (CheminCalcul/Chemin_Verouille, from 2604) |
| `b` | 3250–4450 | ChercheVeget/ChercheGc (3384, 3424, 4396, 4423, 4441), ChercheGcLibre (4129, 4174) |
| `c` | 11250–12500 | TerrainEstMontagne, BatimentGetCaseAdjacent, ChercheCaseBatiment, GetCaseIndiceBatiment, listDeleteElem, listUnlinkElem, iaProbReturnTo, VoixOffAsk |

```sh
python3 "…/heavy_lease.py" core -- python3 -B ferramentas/validar_lacunas_s1.py --janela a --capturar
python3 "…/heavy_lease.py" core -- python3 -B ferramentas/validar_lacunas_s1.py --janela a
```

## Translations

### Completed native comparisons

| Window | Routine | Cases | Mismatches |
|---|---|---:|---:|
| a | ChercheVeget | 42 | 0 |
| a | ChercheGc | 32 | 0 |
| a | ChercheGcLibre | 20 | 0 |
| a | TypeEnginPeutEcraser | 198 | 0 |
| a | IsIndirectlyBlocking | 294 | 0 |
| a | IsDirectlyBlocking | 52 | 0 |
| b | ChercheVeget | 45 | 0 |
| b | ChercheGc | 35 | 0 |
| b | ChercheGcLibre | 40 | 0 |
| c | TerrainEstMontagne | 325 | 0 |
| c | BatimentGetCaseAdjacent | 284 | 0 |
| c | ChercheCaseBatiment | 16 | 0 |
| c | GetCaseIndiceBatiment | 6 | 0 |
| c | listDeleteElem | 3 | 0 |
| c | listUnlinkElem | 3 | 0 |
| c | iaProbReturnTo | 4 | 0 |
| c | VoixOffAsk | 11 | 0 |

These are fresh native comparisons under `heavy_lease.py`, not historical smoke totals. The committed original-only captures were reproduced exactly in every case. No translation correction was needed for windows `a` or `b`.

Window c also compares all seven exit registers and ESP, every changed game byte and Audio's four request-argument registers plus pushed volume. Before that comparison, the register review corrected the sound callback's ESI to the native structure-record pointer, forwarded `chamada` to `**kwargs` sound providers, and protected GetCaseIndiceBatiment's out-of-pool inputs. The ESI/call-address callback details have focused static-instruction contract tests; c's sound-boundary records contain only EAX/EDX/EBX/ECX. Neither callback returns nor unknown memory are defaulted.

### Window c capture preparation

A predecessor's local capture attempt faulted at frame 11860 in GetCaseIndiceBatiment `0x41aac4` on the declared index `0x1234`. The structure pool has 1,000 records. The corrected c variants retain indexes 0/1/2/5/999 and exclude that unsupported read; the original code and existing evidence are unchanged. This is a case-table correction, not an emulated successful return for the faulting input.

Report tests distinguish current executed translation dependencies from versioned validation-driver provenance. Driver/bench hashes and the unused opposite-window module are checked against the report's immutable Core `source_revision`; executed translation sources must still match current bytes. Thus a c-only case-table correction does not invalidate unchanged a/b implementations or rewrite their reports. No foreign-front source hash is pinned.

All take `chamar(nome, regs, pilha=())` with EAX..EBP and an optional ESP, and return EAX..EBP and ESP, every register. The full contracts, with addresses, are in the module docstrings.

**`buscas_bloqueios.BuscasBloqueios`** (provider: `provedor_buscas`):
- **ChercheVeget** (0x47790d): square-ring search for an object byte in [BL, CL]. EAX keeps all 32 bits of the entry EAX plus the offset. EBX holds the grid address of the hit. CH holds the last byte read.
- **ChercheGc** (0x4781cc): ChercheVeget with bounds 0x1e..0x35, entered through ChercheDrapeau's call.
- **ChercheGcLibre** (0x477ead): rings k < DX, fields 0x1e..0x35, and EnginPeutPasser(BX, cell, 1) at each candidate. That test is `fadiga_vegetacao`'s inline translation, for types 0..2/4..10. On the first two ring checks, EAX's upper word is stack residue; it is exact when ESP is given.
- **TypeEnginPeutEcraser** (0x442409), **IsDirectlyBlocking** (0x42eba4) and **IsIndirectlyBlocking** (0x42ece0): this is `caminhos.classificar_passagem`'s rule over live memory. AH holds the moving flag. EDX is the last load. The 0x4423d5 table covers all 256 type bytes.

**`consultas_luta.ConsultasLuta`** (dependency `som` for PlaySnd_StopSound/PostSound):
- **TerrainEstMontagne** (0x47653c).
- **BatimentGetCaseAdjacent** (0x4239a0): the 3×3 block around DX, against the masked footprint of structure AX. EAX's upper bits come from stack residue.
- **ChercheCaseBatiment** (0x41b489).
- **GetCaseIndiceBatiment**: `incursao_core`, already translated.
- **listDeleteElem** (0x47d03a), **listUnlinkElem** (0x47d11a), **iaProbReturnTo** (0x47da54).
- **VoixOffAsk** (0x41a1ac): StopSound, then PostSound 0x41 with table 0x41a190.

## Resume

```sh
L="/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py"
python3 "$L" core -- python3 -B ferramentas/validar_lacunas_s1.py --janela a     # ~15 min
python3 "$L" core -- python3 -B ferramentas/validar_lacunas_s1.py --janela b     # ~15 min
python3 "$L" core -- python3 -B ferramentas/validar_lacunas_s1.py --janela c --capturar   # commit before comparing
python3 "$L" core -- python3 -B ferramentas/validar_lacunas_s1.py --janela c
```

These commands need the snapshots in `.local/m3/quadro128/` and `.local/m3/passo2/S1/` (`instantaneo-02250/03250/11250.pickle`). Copy them from the Mac mini:

```sh
scp 'marciobarbato@192.168.68.63:git/Rising\ Lands/worktrees/re-missions/.local/m3/passo2/S1/instantaneo-NNNNN.pickle' .local/m3/passo2/S1/
```

The quadro128 directory comes from the same location. A failing comparison writes its report to `.local/lacunas-s1/falha-*.json`. Commit the reports and update HANDOFF once they show 0 mismatches.

## Validation `testes/test_lacunas_s1.py` checks:
- that the captures are original-only and on the S1 trajectory;
- that the reports are bound to Core sources with 0 mismatches;
- the synthetic properties of the translations.

## Owner reuse and remaining scope

- **EnginRestaureEtat** (`0x45315f`, first S1 call 8057): Economy's `Restauracao` / `provedor_restauracao` already covers every switch target, with 58 published native restore comparisons and zero mismatches. Core's existing callees remain named dependencies; no further Core restore body is owed.
- **ChercheBatimentProximiteCaveOuSanctuaire** (`0x4539f3`, first S1 call 11753): reuse Combat's `refugio_registradores`, exposed through `LutaFatalViva`, with two published native refuge comparisons and zero mismatches. Do not duplicate it in Core.
- `provedor_lacunas_s1` forwards both owner callbacks with all seven registers and actual call addresses; [STATE_QUERIES](STATE_QUERIES.md) records the exact binding contract. No additional Core capture window is needed to repeat their existing proofs.
- Full reconstructed S1 phase/whole-state equality remains a coordinator/consumer proof. The original survey is historical; these isolated comparisons do not establish M3.1/M4.1 acceptance. Search type/radius limits, readable-stack requirements and missing Audio/owner providers remain explicit.
