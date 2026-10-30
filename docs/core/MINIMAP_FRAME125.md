# Frame-125 lodging minimap: Economy's composition divergence

Status: settled original-first on `feat/re-core`. **The cause is in Economy's wiring, not in a Core translation.** Core hardened its provider so the same omission now raises at the call.

## The report

Economy's work-cycle composition (`compor_ciclo_trabalho.py` CPU-free and `compor_ciclo_trabalho_nativo.py`, see `pesquisas-paralelas/economia/HANDOFF.md` "Cave body, habitation and recruitment") had one mismatch. At frame 125, BatimentLogeEngin(cave 1, colonist 3) makes the 0xc8 cave the player's. 196 minimap bytes differed, starting at 0x47933a26 (original 32 → 162). The report put this on Core's DecouvreTerrain → SetMiniMap.

## What the original does (capture before any change)

`ferramentas/validar_minimapa_quadro125.py --capturar` reruns Economy's own work-cycle bench (`capturar_ciclo_trabalho`, read-only import) natively up to frame 125. At that frame it isolates only BatimentLogeEngin. The rerun's entry and exit registers and changed bytes equal Economy's committed record of the call. Code hooks snapshot the whole mapped state at the entry of each of the call's DecouvreTerrain, IllumineTerrain and BatimentModifyMap. From those snapshots, the original routines are run natively as leaf calls. The capture is `evidencias/minimapa-quadro125/captura-minimapa-quadro125.json.xz` (commit `cce7511`); it ran no translation and reproduced load_tail, between_frames and frame1 with the code unchanged.

| Case | Call (from its exact frame-125 entry state) | Changed bytes (view / structure layer) |
|---|---|---|
| decouvre_terrain_in_situ | DecouvreTerrain(AX 0xa14, DX 11, BL 0), as BatimentHabitable makes it | 120 (72 / 0) |
| illumine_terrain_in_situ | IllumineTerrain(0xa14, 8, 0) | 335 (76 / 0) |
| modify_map_in_situ | BatimentModifyMap(AX 1, **DL 1**) at 0x41fa88: SetMiniMap mode 6 | 196 (96 / 100) |
| modify_map_dl0_composition_input | BatimentModifyMap(1, **DL 0**): mode 7, what the composition handed Core | 196 (96 / 100) |
| modify_map_dl1_before_light / _dl0_before_light | the same, from DecouvreTerrain's entry state | 196 each |
| decouvre_terrain_radius3 | DecouvreTerrain(0xa14, 3, 0): Economy's earlier wiring bug | 0 |

The 196 bytes are written by **BatimentModifyMap's** 25 SetMiniMap mode-6 calls (cave footprint 0xa13..0xe17), not by DecouvreTerrain. 0x47933a26 is in the minimap view, at cell (19,10). Only BatimentModifyMap's SetMiniMap from cell 0xa13 writes it (0xa2, the player-0 colour + 2). The DL=0 run differs from the in-situ DL=1 run in exactly **196 bytes, the first at 0x47933a26**: the composition's mismatch, reproduced by the original alone.

Why DL is 1: `0x41fa7c mov edx, 1` precedes `call BatimentHabitable` (0x41cc70). BatimentHabitable pushes and pops EDX, so EDX is still 1 at `0x41fa88 call BatimentModifyMap`, and BatimentModifyMap stores DL at `0x419e9f`.

## Cause

Economy's `ciclo_trabalho.py` calls `self._ext('BatimentModifyMap', 0x41fa88, EAX=s)`, and its `ARGUMENTOS['BatimentModifyMap']` is `{'EAX': 0xffff}`. EDX is never passed. Core's `provedor_entrada` entered a missing register as 0 (its published contract), so DL = 0 selected mode 7. The composition's argument check compares only the bits in `ARGUMENTOS`, so it never flagged the missing DL. With EDX = 1 passed, the frame-125 call matches in the CPU-free composition (checked with and without `--base`).

**Owed by Economy** (`pesquisas-paralelas/economia/ciclo_trabalho.py`):
1. `ARGUMENTOS['BatimentModifyMap'] = {'EAX': 0xffff, 'EDX': 0xff}`.
2. At 0x41fa88: `self._ext('BatimentModifyMap', 0x41fa88, EAX=s, EDX=1)`. EDX is the literal 1 that 0x41fa7c loads for BatimentHabitable and BatimentHabitable preserves; passing its exit EDX is equivalent.
3. Rerun `compor_ciclo_trabalho.py --base …` and `compor_ciclo_trabalho_nativo.py`. Frame 125 then matches; the expected total is 403 match, 4 uncertain EAX, 0 mismatch.

## Core change

`entrada_estruturas.provedor_entrada` now refuses a call that omits an argument register the routine's behaviour depends on. `ARGUMENTOS_EXIGIDOS` lists them:
- DecouvreTerrain and IllumineTerrain: AX, DX, BL;
- BatimentModifyMap: AX, DL;
- TerrainEstDecouvert: AX, DL.

The refusal is `ArgumentoNaoPassado` (a `ValueError`), raised before anything runs. Every other register keeps the published contract: a missing register enters as 0 with a full uncertain mask. Until Economy passes DL, its composition reports frame 125 as an `error` naming the missing EDX instead of a silent minimap mismatch. No translation changed: Core's DecouvreTerrain, IllumineTerrain and BatimentModifyMap (both modes) match the original at this state.

## Native differential

`validar_minimapa_quadro125.py` (default mode) reruns the bench and checks the native rerun against the committed capture and Economy's record. It then compares each case with `EntradaEstruturas(m).chamar` over a copy of the case's entry state: EAX..EBP except the declared uncertain bits, and every byte of every block. It also runs `provedor_entrada` in Economy's two call shapes: `{'EAX': 1, 'EDX': 1}` must equal the in-situ native result, and `{'EAX': 1}` must raise with no store. Report: `relatorios/minimapa-quadro125-emulada.json`. Tests: `testes/test_minimapa_quadro125.py` (CPU-free: capture facts, the 196-byte cause, report bound to the sources, provider shapes) and `testes/test_emulacao_minimapa_quadro125.py` (RISING_EMULAR=1).

```sh
python3 "…/heavy_lease.py" core -- python3 -B ferramentas/validar_minimapa_quadro125.py   # ~3 min
```

## Binding to Economy's bench (gate fix)

The report used to pin the bytes of Economy's `bancada_ciclo_trabalho.py` and `capturar_ciclo_trabalho.py`, so Economy's legitimate bench change (pseudo entries for the hunger capture) failed Core's test and blocked both integrations. Now:
- `source_sha256` holds Core's own files only, and the CPU-free test binds every committed report to them strictly.
- `economy_source_sha256` records the hash of the Economy files the run actually imported. The test passes when the current Economy files equal those of one committed report in `RELATORIOS_VERIFICADOS`.
- A new Economy bench version therefore needs a native rerun here, never a re-pin: `validar_minimapa_quadro125.py --bancada-economia <copy of the file> --saida relatorios/minimapa-quadro125-emulada-bancada-economia-<hash8>.json`, then add the report to `RELATORIOS_VERIFICADOS`.

Verified versions (both 7 comparisons, 0 mismatches, paths reproduced, code unchanged, Economy's record equal):

| Economy bench `bancada_ciclo_trabalho.py` | Report |
|---|---|
| `d3340e20…` (main) | `relatorios/minimapa-quadro125-emulada.json` (124 s) |
| `7139f3e2…` (feat/re-economy `bfef1ce`, extracted with `git show`) | `relatorios/minimapa-quadro125-emulada-bancada-economia-7139f3e2.json` (128 s) |
