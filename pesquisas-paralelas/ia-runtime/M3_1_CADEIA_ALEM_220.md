# M3.1 — the input chain past frame 220 (AI/runtime)

Status of the second M3.1 step: the committed M3 owners are wired into the chain, and the P6 window (129–2400) is compared whole-state. The proof does **not** pass yet: it stops at a Graphics named stop at `between_frames221`. Everything here is Python against Missions' committed native captures; the leaf changes are validated natively (below).

## Wiring (commits `656ac96`, `17bb6e9`, `7cc733e`)

`provedores_entrada_ia.DonosM3` builds one instance each of the owners' committed translations over the chain's live memory and routes every named dependency one of them raises to its owner:

| Owner module | Used for |
|---|---|
| Core `entrada_estruturas.EntradaEstruturas` | unit state 13 (`estado_entrada`, ESI = record, EDI = unit), SetEnginSelectRentreBatiment (tag 0x10 sub 3), BatimentRetireColon (tag 0x21), EnginSelectPeutEntrer, and the Core routines Economy calls (`provedor_entrada`) |
| Core `visao_grupos.VisaoGrupos` | BatimentIllumine/BatimentDecouvre (structure loop), Sauve/RestaureSelectionGroupe (tags 0xb/0xc), EnginGetCentreGroupe (group key with Shift), MiniMapSetPos, CalculPosition/RechercheDecalageSortie |
| Economy `caverna_recrutamento.CavernaRecrutamento` | BatimentNextEtape's type-3 body (`corpo_caverna`, at the switch target 0x426aff), BatimentHabitable, InitBatimentPlayer/Neutre |
| Economy `ciclo_trabalho.CicloTrabalho` | CalculWorkEngin (unit state 5), BatimentLogeEngin, BatimentAjouteMatiere and its leaves |
| Economy `recrutamento.Recrutamento` | GetStatusRecrute (read-only snapshots) |

Every call passes all of EAX..EBP (Core's `ArgumentoNaoPassado` rule); registers a call site does not determine enter as 0 and are named in the docstrings.

`construcao_entrada_ia.instalar_donos` installs the frame-phase providers (cave body, vision, states 5 and 13) for the chain and for `validar_construcao_teclas_ia`; the pinned switches stop at a target before the first store of its body, so each dispatch continues exactly there.

## Translated from the intact bytes (this front)

- **Unit state 5** `0x456600..0x456736` (`estado_trabalho`): +0x82 == 2 checks the work structure (BatimentEnDestruction, BatimentGetPlayer vs the owner); destroyed/foreign → named stop at the release branch 0x456639; otherwise CalculWorkEngin(AX = unit), exit 0x454ccd.
- **CalculIconeAction with a structure selected** `0x45e9bf` and BatimentGetBagOrdre `0x41c734`.
- **IconeFillContenu code 6** (recruitable unit icons, `0x45e430..0x45e691`) with EnginEnRecrutement `0x420bdf` and BatimentEstOccupe `0x422fa5` (both ten-instruction reads), EnginGetRessource and Economy's TestRessource/GetStatusRecrute.
- **InputGame unit hover with a structure selected** `0x42a9d3`.
- **BatimentPeutAttaquer type prefix** `0x42436c..0x4243b9` (a non-turret structure returns AL = 0); the turret target checks 0x42443f stay Combat's named stop.
- **iagUnitSendMessage for a non-AI owner** (PlayerGetType != 2 → exit 0x482eb5, exact registers, no store); an AI owner stops at 0x482a14.
- The sound boundary also takes the call site Economy passes (`PlaySnd_PostSound` at 0x41faeb).

## Native leaf differentials (rerun, MacBook, under the heavy lease)

| Validator | Cases | Equal | Mismatches | Named stops |
|---|---|---|---|---|
| `validar_entrada_ordens_ia.py` | 124 | 116 (was 113) | 0 | 8 (Combat BatimentInitAttaqueSelect, SetDechargeCaveEnginSelect, 6 TextGetMessage) |
| `validar_paginas_deposito_ia.py` | 203 | 203 (was 201) | 0 | 0 |
| `validar_construcao_teclas_ia.py` | 90 | 85 (was 79) | 0 | 5 (BatimentHabitable in the construction tail, SetMurAllentour, SetEnginSelectRentreEngin, iagUnitSendMessage without a PlayerGetType provider in the bench, WndProc VK_SUBTRACT zoom) |

Newly equal against the native leaf captures: CalculIconeAction with a structure selected, the minimap press (MiniMapSetPos), both BatimentPeutAttaquer call sites, tag 17 (Economy's InitRecruteTroupe), the cave body, unit state 13, tags 0xb/0xc/0x10 (sub 3) and the Shift group-centre key. The replay suites read the regenerated reports and reads (`validacao/*-native.json`, `evidencias/leituras-*.json.xz`); `scripts/check.py --domain ai-runtime` passes (112 tests, 8 native skips). The paginas/construcao reruns predate the InitRecruteTroupe binding, which their cases do not reach.

## P6 window (129–2400, 3 parts, 4,544 phases)

**Whole state, mode 'prova':** part 0 equal in every phase through `frame220` (184 phases: the CAVE order, the builder's construction, the cave body at frame 220), then the stop at `between_frames221`:

> AffGame @0x407dd3: structure states [0, 2, 5], occupied records [0, 1]: captured only for one type-2 structure in modes 0..7

This is Graphics' `efeitos_logicos_exibicao` domain guard: the logic-state effects of AffBatiments are proved only for the type-2 Santuario. **Owner: Graphics** (extend the proved domain to the CAVE states 0/2/5 and later ones; mode 3 uninhabited advances 0x4e1d18, `0x408679`).

**Diagnostic, never evidence** (`--diagnostico-planejamento`, `.local` only: a Graphics display-path stop is recorded and the drawing taken as writing no logic byte):
- indicator level (`provar_entrada_ia` probes, every frame: inputs, orders, RNGs, CRT seed, 0x4e1d18, view, selection, objective block, units 11..15 whole records): P6 2,272/2,272 frames equal to 2400; P3 3,001/3,001 to its last frame 3129; K1 501/501 to 629;
- whole state per phase (`provar_entrada_janelas_ia.py janela P6 --parte N --diagnostico-planejamento`, revision `7cc733e`): **part 0 (129–1128) 2,000/2,000 and part 1 (1129–2128, checkpoint start) 2,000/2,000 phases equal**, zero crossings, with the Graphics guard recorded in 908 and 1,000 between-frames phases (CAVE states [0, 2, 5] and [0, 5]); part 2 (2129–2400, checkpoint start, revision `17bb6e9`) equal 2129–2177, then **196 minimap bytes** (`0x47933a26..`, `0x4793ba26..`, original 162, Python 30/0) at frame 2178 on the lodging path BatimentLogeEngin → BatimentHabitable → DecouvreTerrain/SetMiniMap: the frame-125 minimap divergence already known (Economy's ciclo_trabalho calls BatimentModifyMap without EDX = 1; Core e713bfa makes that an `ArgumentoNaoPassado`). **Owner: Economy/Core**, being fixed. Diagnostic chains: part 0 `a3f35dfc7701065f…`, part 1 `5da71fab9ac33cb3…` (505 s each).

So with today's providers the strict proof's only stop before 2178 is the Graphics guard: assuming that guard's drawing writes no logic byte, the chain equals the native run in the whole compared state through frame 2177 (4,098 phases), and the next divergence is Economy/Core's.

## Remaining stops, with owners

| Where | Stop | Owner |
|---|---|---|
| P6/P3/P7 `between_frames221` | AffBatiments logic-state effects for structures other than the type-2 Santuario | Graphics |
| K1 141, P4 422, P5 572 | AffGame vegetation/terrain handlers at unsampled view origins | Graphics |
| P7 2801, P4 460 (planning) | TerrainEstGc `0x44d8cd` (object ≥ 0x1d) called by CalculWorkEngin | unassigned (terrain query; Economy's work cycle calls it, this front has only the object < 0x1d leaf) |
| P5 760 (planning) | SetMiniMap from CalculWorkEngin `0x44c437` (a mode Core has not translated in `incursao_core`) | Core |
| leaf cases | BatimentInitAttaqueSelect (tag 14), turret BatimentPeutAttaquer | Combat |
| leaf cases | SetDechargeCaveEnginSelect (tag 19) | Economy |
| P6 2178 (planning) | minimap bytes after BatimentLogeEngin → BatimentHabitable (frame-125 divergence) | Economy (BatimentModifyMap EDX) / Core |
| — | Core `som` without the call site (read from `_fronteira`) | Core (request) |
