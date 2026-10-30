# S1 coverage: every routine the victory capture reaches, by owner

Data: [`relatorios/cobertura-s1.json`](../../relatorios/cobertura-s1.json). Generator: `python3 -B ferramentas/cobertura_s1.py` (read-only; about 30 s, no Unicorn). It is a coverage survey, not evidence.

## Sources

- **Capture.** Missions' replay-checked S1 (feat/re-missions `82ec5ea`, `pesquisas-paralelas/missoes/m3/sondas/S1/`), frames 129–17050. `quadros.jsonl` holds per-frame entry counts for every symbol. They come from one block hook over the code section, the same method as `cobrir_quadros_exibicao.py`. The file also holds every routine's first entry with its caller. The tool reads the files from the git object and checks them against `replay.json`, after the same normalisation: sorted keys, `seconds` dropped.
- **No new native run was needed.** The block-hook counts are complete at routine level. Caller sets come from a static scan instead: every `call`/`jmp rel32` in the code section whose target is a symbol start, restricted to routines S1 reaches. A routine whose reached callers all sit under `AffGame` is marked *display-only*.
- **Owner.** Owners come from three sources, in this order:
  1. a curated table in the tool, built from who translated the routine on main, or whose call sites it serves;
  2. Combat's `M2_3_PRONTIDAO.json`;
  3. Graphics, for display-only routines.

  `WndProc` goes to AI/runtime, following M3_PLAN.
- **Status.** Status is read from main `5422338` (merged `47b8386`). It is per routine, not per branch:

| Status | Meaning |
|---|---|
| `validated` | An isolated native differential on main compares the routine and reports no mismatch. Evidence is extracted from every front's `*emulad*`/`*nativ*`/`*x86*` reports, plus one curated row: Missions' influence differential for `CaseGetZoneInfluence`. |
| `nested-validated` | A native capture records the routine as entered inside a root whose differential is clean. |
| `chain-only` / `display-chain` | Reached inside an equal chain-proof window on main, with no isolated differential: M2.3 frames 0–9200 (no input), M3.1 P1 129–629 or P2 129–729. |
| `boundary` | A declared audio, MCI or picture-load boundary. |
| `display` | Display-only and never inside a proven window. |
| `gap` | None of the above. Gap rows carry `mentioned_in_native_reports`: unverified pointers, often dependency stops, for the owner to confirm. |

## Totals

495 routines and 241,383,466 entries in total. The status counts are:
- 193 validated, 57 nested-validated;
- 63 chain-only, 51 display-chain;
- 7 boundary, 22 display;
- **102 gap**.

| Owner | Routines | validated | nested | chain | boundary | display | **gap** |
|---|---|---|---|---|---|---|---|
| Core | 186 | 137 | 30 | 3 | 0 | 0 | **16** |
| Economy | 84 | 28 | 11 | 16 | 0 | 1 | **28** |
| AI/runtime | 72 | 11 | 11 | 28 | 0 | 0 | **22** |
| Combat | 40 | 14 | 2 | 4 | 0 | 0 | **20** |
| Graphics | 87 | 0 | 0 | 63 | 1 | 21 | **2** |
| Missions | 20 | 3 | 3 | 0 | 0 | 0 | **14** |
| Audio | 6 | 0 | 0 | 0 | 6 | 0 | 0 |

## Gap list per owner

Each entry is the routine, then its first S1 frame and its total entries.

**Core (16).**
- ChercheGc (2352, 56), ChercheVeget (2352, 56), ChercheGcLibre (3116, 40): the work-cycle searches. Economy's `ciclo_trabalho` calls them as externals.
- TypeEnginPeutEcraser (2604, 486), IsIndirectlyBlocking (2604, 355), IsDirectlyBlocking (2709, 131): path-search blocking by other units. `caminhos.classificar_passagem` translates them and the synthetic native test checks it, but S1's live states are not compared.
- EnginRestaureEtat (8057, 15).
- listDeleteElem, listUnlinkElem (11500, 3) and iaProbReturnTo (11663, 4): task-VM lists.
- TerrainEstMontagne (11741, 315).
- ChercheBatimentProximiteCaveOuSanctuaire (11753, 1), VoixOffAsk (12178, 1): Combat names both as external dependencies.
- BatimentGetCaseAdjacent (11860, 170), ChercheCaseBatiment (11860, 1).
- GetCaseIndiceBatiment (11860, 1): already translated in `incursao_core`, but first reached by S1.

**Economy (28).**
- Recruitment and troops from frame 2013: EnginGetTimeRecrute (5104), `__CHP` (2467), BatimentGetCapacite (2115), BatimentGetColons (2115), GetStatusRecrute (437), EnginSetExperimente (2547, 5).
- TuyauEstSortie (1977, 14927).
- MineEstSurTerrain (2685, 44), AjouteMatiere (2728, 97), SacGetCapacite (3851, 2), TerrainRetireMatiere (8057, 15).
- 17 research/technology routines at the result screen (17043): RechercheCalculNew, InventionSetEffet, TypeBatimentEstRealisable (352), Technologie*, Set*Recrutable, Recherche*, BonusReset and IaRechercheAjuste.
- Also CalculStatusRecrute (2013), which is display-only.

**AI/runtime (22).**
- iagVilleSendMessage (2547, 13).
- The raid's later solver kernels from 11300: I_DonnePositionGroupe, V_FreeConflit, V_iaMonstreAttend…, B_Egalite, I_Soustraction, V_AttaquerBatiment, I_DonneBatimentSurCase, B_EtatBatiment, V_LibereGroupeVide.
- The war, battle and messaging routines from 11663: iagWarAddEnnemyToBattle, iagWarProbReturnTo, iagWarNewTargetForUnit, iagWarRemoveEnnemyFromBattle, iagWarDeleteBattle, iagWarUnlockTargetAfterDeath, iagUnitRemoveFromGroup, iaGroupDelete.
- The three `iab*` reactions.
- MessageBoxSet (11753).

**Combat (20), the first fight from frame 11663.**
- EnginAPortee (422), EnginAdjacent (32).
- EnginLigneDeTir and AngleCalcul (351), with the CRT `IF@DACOS`, `IF@DATAN2` and `__@DSQRT` (347).
- AnimAttaqueEngin (362).
- InfligeDegat's helpers: PlayerAAttaqueSet, ChercheIndiceEnginCible, ChercheTypeEnginProximite, PlayerResetAllie, EnginSetLevelExperience and EnginEstEnnemi.
- The linear projectile: ProjectileLineaire, ProjectileCalculLineaire (8075), ProjectileInfligeDegat, TypeEnginGetSortieProjectile.
- EnginGetDegat, EnginAddVie (2547).

**Missions (14).**
- CaseGetZoneInfluence is validated. The influence differential compares it, but its rows do not name it, so it is a curated row.
- The gaps are PartieGetResultat (17033), then the result-screen and next-mission path at 17043:
  - MissionNext, MakeMissionName, ObjectifLoadText;
  - File*, `fopen`, `fread`, `fclose`;
  - PlayerStore, RechercheStore, Engin_StoreExperimente.

**Graphics (2 logic + 21 display).**
- The logic gaps are LoadBank and MemAlloc at the result screen.
- The display-only routines with no proven window:
  - AffWorkEngin (2085), AffConstruireBatiment (154);
  - AffJaugeBatiment, AffContenanceBatiment, BatimentGetBag, BatimentGetDegat (1831);
  - BatimentPoseCadre;
  - PasteGrisCmp, MemGrisCopy, FilledBoxGris;
  - AffCompteurCoutMatiere;
  - AffProjectile, ProjectileGetCase;
  - AffAttaqueEngin, AffDyingEngin, EnginGetSpriteMort, AffFlamme;
  - the result screen's AffObjectif, AffString, SetBank and AffEnginProjectile.

**Audio.** No gaps. PlaySnd_PostSound/StopSound/StopAllSound and MCICD are boundaries, and S1's boundary log holds 177 post requests.

## Caveats

- Routine-level only. EnginNextEtape, CalculWorkEngin and similar routines are `validated` or `chain-only`, but S1 drives them through states no proof has covered. The per-segment chain proofs will find those branches.
- `chain-only` for M2.3 covers no-input states. Routines first reached only in P1/P2 are covered for those windows only.
- The extractor reads report shapes (`by_routine`, `counts`, `cases[]` with `routine`) and nested-entry maps. A front whose report names a routine differently is a missed `validated`, not a real gap. The report's `mentioned_in_native_reports` pointers exist to catch exactly that.
