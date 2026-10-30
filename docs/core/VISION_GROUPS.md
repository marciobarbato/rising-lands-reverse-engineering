# Structure vision, group selection, minimap view and exit position (M3.1 round 2)

Status: captured natively, translated and validated natively on `feat/re-core`, not yet integrated. These are the Core routines that ai-runtime's M3 probe chain names as stops (docs/AI_RUNTIME.md "M3.1 round 2": P3/P6/P7 stop right after the CAVE body at frame 220, K1's tag 12 at frame 200, the minimap presses), and the exit position Economy's recruitment needs. Addresses apply only to the intact `RISING.EXE` (SHA-256 `6c556520…8543fb`).

## Method (original first)

1. **Bench**: `bancada_entrada_estruturas` (the selection-orders pause: Missions' accepted MONDE01 display path, frame 1's first `ProcessInputGame` entry, with native preparations and multi-step windows). The prepared CAVE is STRUCTURE_ENTRY's (built natively by `CreerBatiment`, the progress word, `BatimentConstruction`, `BatimentRetireColon`); `illumine/decouvre_cave_created_*` use only `CreerBatiment`, the P3 state at frame 220.
2. **Cases** (`ferramentas/casos_visao_grupos.py`): 320 declared cases, 329 measured steps (windows: light on/on/off/off, discovery twice, group save → deselect → restore, minimap press → drag → recentre). The pause facts they rely on are checked by `verificar_pausa`.
3. **Capture** (`capturar_visao_grupos.py` → `evidencias/visao-grupos/captura-visao-grupos-exibicao.json.xz`), committed before any translation (`f708b15`); 329/329 steps return; the run reproduces load_tail, between_frames and frame1 and leaves the code section unchanged (175 s). `extrair_visao_grupos.py` exports 21 original intervals and 13 jump tables.
4. **Translation** (`ferramentas/visao_grupos.py`, class `VisaoGrupos`) over live flat memory.
5. **Native differential** (`validar_visao_grupos.py` → `relatorios/visao-grupos-emulada.json`): **329 comparisons, 0 mismatches**, 8,433 changed bytes compared, 19 sound requests compared, the native rerun equal to the capture step for step. Registers EAX..EBP compared except one declared uncertainty (RechercheDecalageSortie's EAX bits 16+ when a free neighbour is found, 32 steps). The same run wrote `leituras-visao-grupos-exibicao.json.xz`; **all 329 steps replay without a CPU** (`testes/test_visao_grupos.py`), and the translation reads no byte the original did not read.

```sh
python3 "…/heavy_lease.py" core -- python3 -B ferramentas/capturar_visao_grupos.py --saida <new>.json.xz   # ~3 min
python3 "…/heavy_lease.py" core -- python3 -B ferramentas/validar_visao_grupos.py                           # ~3.5 min
RISING_EMULAR=1 PYTHONPATH=ferramentas:testes python3 -B -m unittest testes.test_emulacao_visao_grupos
```

| Routine | Steps | Mismatches |
|---|---|---|
| BatimentIllumine 0x419233 (AX structure, DL player, BL on/off) | 56 | 0 |
| BatimentDecouvre 0x419d54 (AX structure, DL player) | 47 | 0 |
| IllumineCase 0x476968, EteintCase 0x476adc, DecouvreCase 0x47670a (AX cell, DL player) | 22, 22, 17 | 0 |
| SauveSelectionGroupe 0x4726f7, RestaureSelectionGroupe 0x472769 (AL player, DL group) | 14, 22 | 0 |
| EnginGetCentreGroupe 0x442139 (AL player, EDX/EBX result addresses, CL group) | 14 | 0 |
| MiniMapRecentre 0x46a01b, MiniMapSetPos 0x46a19e (AX x, DX y) | 19, 11 | 0 |
| CalculPosition 0x420698 (every register), RechercheDecalageSortie 0x41d1d0 | 50, 33 | 0 |
| BatimentDeselectionner, DeSelectionGroupe (inside the group window; `selecao_ordens`) | 1, 1 | 0 |

## What the routines do (the original's facts the cases pinned)

- **BatimentIllumine**: IllumineCase (BL nonzero) or EteintCase (BL zero) over the footprint rectangle (type width × height from the origin `+2`), rows then columns, skipping cells whose column or row is outside 0..255 (not the map). It uses DL, not the owner. EAX = height; EBX = width once a row was in range (else the origin word); EDX = the last cell routine's EDX (or the last index tested).
- **BatimentDecouvre**: player 0xc8 returns at once (EAX = 0xc8, EDX = the structure word). Otherwise DecouvreCase over rows −1..height and columns −1..width (a dimension of 0x100 or more is not grown). EAX = EDX = the grown height; every other register preserved.
- **Per-cell**: DecouvreCase clears the four neighbour border bits, calls SetMiniMap mode 1 when the discovery byte was nonzero, then clears bit 4. IllumineCase at count 0 clears the borders and the light bit 4 and calls SetMiniMap mode 2; the count grows unless 0xff (EDX = old | new << 8). EteintCase at count 1 sets them and calls mode 3; a nonzero count drops (EAX = the count byte's address). A footprint touching row 255 writes past the 64 KiB grid exactly as the original does (the grids are reached through their live pointers). SetMiniMap is M2.3's `visao_movimento.minimapa` over flat-memory views (a minimap index past the 128×128 buffer reaches the memory after it, as in the original).
- **SauveSelectionGroupe**: for every live unit of the player, a member of the group leaves it (`+0xbc = 0`, not 0xff), then a selected one (`+0xbd`) joins it. Group 0xff is the "no group" value every unit has at the start, so saving group 0xff clears it on all of them.
- **RestaureSelectionGroupe**: unselects every selected unit of the player (RetireSelectionEngin), then appends each live group member not in state 14 to the player's list (count < 0xff) with `+0xbd = 1`. The first member that is not type 10, belongs to the local player and is not of types 0xb..0x10 speaks: a type-7 unit in state 0xb/0xf stops its sound (PlaySnd_StopSound(`+0x104`, 0x16, 0)) and EnginAsk(unit, 0x16); any other EnginAsk(unit, 8, 0).
- **EnginGetCentreGroupe**: only the **first** live member of the player's group counts (the original leaves its loop after the first match), so the result is that unit's cell; with no member, the centre of the view rectangle from the current words at EDX/EBX and the view size. EAX/ECX/EDX are the halving's, EBX = that unit (else the view height word).
- **MiniMapRecentre**: clamps the minimap scroll words 0x507d68/6a to [margin × 32, view × 32 − margin × 32 − display − 2] (margin: the signed byte 0x508f90; display: 0x496fe0/2), then pulls the view origin 0x508720/22 back inside the map. Only EAX changes; it comes from the last computation and reads the upper halves of EBX/ECX/ESI/EDI.
- **MiniMapSetPos**: 0x507d68 = AX + 0x507d6c and 0x507d6a = DX + 0x507d6e (each 0 when negative as a signed word), then MiniMapRecentre. EDX = DX + the lock word (32-bit).
- **CalculPosition**: AX as `posicao_saida` (unchanged); EAX bits 16+ come from the 32-bit arithmetic over the origin word loaded into a 16-bit register that keeps its upper half: the caller's ESI (types 0, 10, 11), the caller's EDI (type 1), height − 4 (type 8), width − 1 (type 18), else 0. Types 9, 12, 17 and above 0x15 give 0. Every other register preserved.
- **RechercheDecalageSortie**: the first of the 8 cells around CalculPosition's AX (rows then columns; row and column 0..255) whose attribute bit 0 is clear, else CalculPosition's full EAX. Only EAX changes.

## API

`VisaoGrupos(memoria, *, som=None)`; `chamar(nome, regs)` takes EAX..EBP and returns EAX..EBP as the original leaves them, optionally with `_incertos = {register: mask}` (masked bits never guessed). It also forwards BatimentDeselectionner and DeSelectionGroupe to `selecao_ordens`, so ProcessInputGame's tag 0xc sequence runs through one object.

**Named dependency** (never defaulted): Audio's PlaySnd_PostSound/PlaySnd_StopSound through `som(nome, regs, pilha) -> EAX` (RestaureSelectionGroupe's voice, as in SELECTION_ORDERS). **Outside the domain** (`ForaDoDominioVisao`, before any store): players other than 0..3 in the per-cell routines (player 4's grid pointers alias other grids, 0xc8's lie beyond the table; BatimentDecouvre's 0xc8 early return is translated); RechercheDecalageSortie for structure types 9, 12, 17 and above 0x15 (they read uninitialized locals).

## Adapters

- **ai-runtime** (`laco_despachantes`, `entrada_ordens_ia`): `provedores_visao(memoria, som=None)` gives the keyword-shaped providers `BatimentIllumine(sitio, estrutura, jogador, ebx)`, `BatimentDecouvre(sitio, estrutura, jogador)`, `MiniMapSetPos(sitio, x, y)` (EBX = 0, ECX = 1 as at 0x42bb45) and `MiniMapRecentre(sitio)`. The register-shaped ones (SauveSelectionGroupe, RestaureSelectionGroupe, EnginGetCentreGroupe, and any of the above) are `VisaoGrupos(m, som=som).chamar(nome, regs)`, the same shape as `SelecaoOrdens.chamar` that `provedores_entrada_ia.nucleo` already binds. With these, CalculBatimentNextEtape's vision loop (CaseEstDecouverte, BatimentEstDecouvert, BatimentContourEstIllumine from `chamadas_quadro_core.provedores_core`) has every Core callee.
- **Economy** (recruitment): `provedor_saida(visao, outros=None)` is the `externo(nome, chamada, regs)` for CalculPosition and RechercheDecalageSortie, in the shape of `provedor_entrada` (a register Economy does not pass enters as 0 with a full uncertain mask; a missing ESI/EDI also marks EAX bits 16+). `escolher_saida(memoria)` is the `Recrutamento.iniciar(escolher_saida=...)` callback: structure index → RechercheDecalageSortie's u16 cell, which the suffix 0x428640 stores in `+0x7c`. SortieTroupe's call at 0x420f5a passes AX = structure, BL = direction (unused); AX is the caller-consumed cell, the next original call is EnginSetType at 0x420f69 (CONVERSION).

## Not covered here

- The scripted-input captures (Missions' probes on the Mac mini) that reach these routines from real frames: P3/P6/P7 past frame 220, K1's tag 12 at frame 200, the minimap zone press/drag, WndProc VK_SUBTRACT.
- SetMiniMap modes other than 1/2/3 are not reached by these routines.
