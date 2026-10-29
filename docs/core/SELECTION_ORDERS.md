# Player selection and order setters (M3 groundwork)

Status: captured natively, translated and validated natively on `feat/re-core`, not yet integrated. These routines are what player input reaches through `ProcessInputGame` in M3 ([M3 plan](../M3_PLAN.md) §3, Core row). None of them runs in the no-input coverage run to frame 9200, so this is the first execution evidence for them. Addresses apply only to the intact `RISING.EXE` (SHA-256 `6c556520…8543fb`).

## Method (original first)

1. **Bench** (`ferramentas/bancada_selecao_ordens.py`). It reruns Missions' accepted MONDE01 display path (startup, MissionLoad, load_tail, between_frames) and pauses frame 1 at its first `ProcessInputGame` entry (called from `CalculGame+0xb4d`). There each declared case runs one routine natively as a leaf call:
   - the exact paused state is restored (CPU context, DGROUP+.bss, CRT thread page, every active allocation, native stack);
   - the case's declared byte writes and argument registers are applied;
   - the routine runs to a sentinel return under the bench's own frame-boundary handling: `PlaySnd_*` is not executed, EAX is unchanged and the call is logged with its registers and pushed words.

   After the cases, the paused state is restored and frame 1 continues. The run reproduces the committed `load_tail`, `between_frames` and `frame1` state summaries, and the code section is unchanged.
2. **Cases** (`ferramentas/casos_selecao_ordens.py`): 130 cases. They cover:
   - unit indices: builder 12, types 5/1/8, soldiers, colonists in state 14, a free record;
   - owners and player arguments 0–3;
   - selection counts 0, 1, 2, 3, 4, 8 and a full list (0xff);
   - the visibility, type-16/state-13 and already-selected rules;
   - rectangles: single cell, all field units, reversed corners, empty, the sanctuary;
   - builder states 11/15, sound handles busy or free, an undiscovered cell, view distances for every volume tier;
   - structure types 0, 1, 2, 3, 4, 9, 12, 13, 17, 21, the gate queue, the search-context owner and the origin cell.
3. **Capture** (`ferramentas/capturar_selecao_ordens.py` → `evidencias/selecao-ordens/captura-selecao-ordens-exibicao.json`). It was committed before any translation (`75ed19b`). Per case it holds the entry/exit registers, every non-stack store in order, the changed bytes of the whole mapped state, every nested routine entry (depth, name, argument registers, exit EAX) and the boundary events. `extrair_selecao_ordens.py` exports the bodies, shared epilogues and jump tables (`evidencias/selecao-ordens/*.asm`, `manifesto.json`).
4. **Translation** (`ferramentas/selecao_ordens.py`, class `SelecaoOrdens`) over live flat memory.
5. **Native differential** (`ferramentas/validar_selecao_ordens.py` → `relatorios/selecao-ordens-emulada.json`). It reruns the same native cases. After each one, the translation runs over a copy of the exact case-entry state.
   - Result: **130 comparisons, 0 mismatches.**
   - Compared per case: registers EAX..EBP, every changed byte of the whole mapped state (481 in total), and the 58 sound requests (routine, EAX/EDX/EBX/ECX, pushed volume) against the native boundary events.
   - The native run also equals the committed capture in every case: registers, stores, changed bytes, calls and boundaries.
   - The same run records the bytes each case read before writing (`leituras-selecao-ordens-exibicao.json`). With them, 94 cases replay without a CPU in `testes/test_selecao_ordens.py`. These are all cases whose path avoids ResetOrdre/SetDeplaceEngin (Core's live navigation world) and SetAttaqueEngin (Combat). The test also binds the committed report to the current sources.

```sh
python3 "…/heavy_lease.py" core -- python3 -B ferramentas/capturar_selecao_ordens.py --saida .local/selecao/x.json   # ~110 s
python3 "…/heavy_lease.py" core -- python3 -B ferramentas/validar_selecao_ordens.py                                  # ~120 s
RISING_EMULAR=1 PYTHONPATH=testes python3 -B -m unittest testes.test_emulacao_selecao_ordens
```

## API

`SelecaoOrdens(memoria, *, som=None, definir_ataque=None)`.

- **`memoria`**: `u8/u16/u32(addr, value=None)` plus `vista(addr, n)` (`memoria_quadro_core.MemoriaQuadro` over the live buffers). ResetOrdre and SetDeplaceEngin use Core's navigation world bound live to it (`mundo_vivo`, validated in M2.3).
- **`chamar(nome, regs, pilha=())`**: runs routine `nome` with entry registers `regs` (EAX..EBP; missing keys are an error). It returns all seven registers as the original leaves them, callee-saved ones included. `pilha` holds the pushed words (only `EnginInZone` takes one). Each routine is also a method (`selection_engin`, `set_deplace_engin_select`, …) with the same register dicts.
- Arithmetic flags are not modeled.

Argument widths are what the original reads. Other bits are ignored, except where noted.

| Routine | Entry | Arguments | Effects | Registers changed (others preserved) |
|---|---|---|---|---|
| SelectionEngin | 0x4742dc | AL player, DX corner A, BX corner B (cells) | For every live selectable unit of the player: clear +0xbd and remove it from the list (RetireSelectionEngin), then re-add it when EnginInZone holds. Corners are ordered per axis (SwapWORD). Voice: see below | EAX, EBX, EDX (EDX = 0x320) |
| EnginAddSelection | 0x4741cd | AX unit, DL player | Appends a live selectable unit of that owner whose +0xbd is 0 when count < 0xff; +0xbd = 1 | EAX, EDX |
| EnginSelectionnable | 0x474169 | AX unit | AL = state ≠ 14, not (type 16, state 13, +0xab ≠ 0x32), and +0x72 visible | EAX |
| SelectionAddEngin | 0x4725ee | AX unit, DL player | Unconditional append when count < 0xff; +0xbd = 1; AL = appended | EAX, EDX |
| RetireSelectionEngin | 0x472576 | AX unit, DL player | Removes the first matching slot by shifting the tail and decrements the count. It clears the unit's +0xbd once per slot visited before the match (also when absent). EAX = count+1 | EAX, EDX |
| DeselectionEngin | 0x472648 | AX unit | If +0xbd is set: clears it and removes the unit from its owner's list | EAX |
| DeSelectionGroupe | 0x47268b | AL player | Every live unit of that owner with +0xbd set is cleared and removed | EAX |
| Deselection | 0x429180 | AL player | DeSelectionGroupe + BatimentDeselectionner. Then: action mode `0x496207` = 0xff, `0x4e19b0` = 0, u16 `0x4e05ae` = 0, `0x4e05ab` = 0, redraw `0x496d48` = 1 | EAX |
| EnginInZone | 0x4461f4 | AX unit, DX x1, BX y1, CX x2, pushed y2 (RET 4) | AL = the unit cell lies in [x1..x2]×[y1..y2]. Types 3, 11–16 and 25 also test cell−1, cell−0x101 and cell−0x100. Coordinates come from a signed idiv by 256; compares are unsigned 16-bit | EAX, EBX, ECX, EDX |
| BatimentSelection | 0x41b673 | AX structure | Type 12: `0x495be0[owner]` = structure. Otherwise, when +5 ≠ 0, the structure is selected if its Bag holds a troop (types 2/21, BagContientTroupe) or, for types other than 21, a type-9 unit (BagContient mode 1). A local-player selection with handle +0x100 = −1 posts sound 0x42 | EAX |
| BatimentDeselectionner | 0x41b663 | AL player | `0x495be0[player]` = 0xffff | EAX = AL |
| SetDeplaceEnginSelect | 0x473e6e | AL player, DX cell | Each live selected unit of that owner gets SetDeplaceEngin, then +0x110 = the cycle counter `0x508f7c`. Voice mode 0xb (first non-vehicle, non-aerial unit) | EAX, EDX |
| SetAttaqueEnginSelect | 0x473dbf | AL player, DL mode, BX reference | Each live selected unit of that owner gets +0x110 = the counter, then SetAttaqueEngin (Combat). Voice mode 0x17 | EAX (= player<<9), EBX, EDX |
| SetConstruitBatimentSelect | 0x473a07 | AL player, DL structure type, BX cell | Only live selected **type-7** units of that owner: SetEnginConstruitBatiment. Voice mode 0x11 | EAX, EBX, EDX (= player<<9) |
| SetEnginConstruitBatiment | 0x4454ce | AX unit, DL structure type, BX cell | See below | EAX (= type, or the record on the queue path), EBX, EDX |
| SetRecolteEnginSelect | 0x473290 | AL player, DX cell | Each live selected unit of that owner: SetRecolteEngin. Voice mode 0xf | EAX, EDX |
| SetRecolteEngin | 0x444ebd | AX unit, DX cell | ResetOrdre; +0x7e = cell; search context released if owned; +0x88 = +0x89 = 0; state 5; +0x82 = 0; +0xb2 = cell | EAX = EDX = record |
| SetTransporteEnginSelect | 0x473212 | AL player, DX value | Each live selected unit, **with no owner test**: SetTransporteEngin. Voice mode 0xf | EAX, EDX |
| SetTransporteEngin | 0x444e7f | AX unit, DX value | **No ResetOrdre.** State 0x12; +0x89 = 0; +0xb2 = +0x7e = value; search released if owned; +0x88 = 0 | EAX = record, EDX = unit·276 or 0 |
| SetDeplaceEngin, ResetOrdre | 0x4457d3, 0x44357c | as M2.3 | Core's translations, reconfirmed on this state | EAX(=EDX) = record / EAX = record |
| EnginAsk | 0x440d5e | AX unit, DX mode, BL flag | If the unit cell is discovered for the local player: +0xf9 = flag. When the handle +0x104 = −1, it posts the voice request | EAX, EBX, EDX |

Rules shared by the `*Select` setters:
- The selection list of player p is at `0x508728 + 0x200·p`: u16 count, then u16 units at +2. The count is re-read every iteration.
- A unit is skipped unless EnginEstVivant (state not 0/4). Every setter except transport also requires owner = player.
- Only the first eligible unit speaks, and only when player = local player `0x508041`. The voice counter still advances for a non-local player.

SetEnginConstruitBatiment details:
- **Gate queue.** A unit already in state 11 with +0xbe = 9 appends the cell at +0xc4 + 2·n with n = +0xd8 (< 10) and returns. There is no ResetOrdre.
- **Otherwise** ResetOrdre runs first. For types other than 9 and 12, the cell becomes cell + ((h − h/2) << 8) − 0x100 + (w − w/2) − 1 − BatimentGetDecalageConstruction(type):
  - w/h come from `0x495d8c + 52·type`;
  - the offsets per type come from table `0x41ae4c`: 0x201, 0x300, 0x101, 0x202, 0x100, 0x202, 0x100, 0x300, 0x202, 0x100, 0, 0, 0x100, 0x200, 0x300, 0x100, 0x100, 1, 0x201, 0x100, 0x100, 0x100; types above 21 give 0.
- **Stores, in order:** +0x7e = cell; search released; +0x88 = +0x89 = 0; +0xc0 = 0xffff; +0xbe = type; state 11; +0xb2 = cell. A gate (type 9) also clears +0xd8.

SelectionEngin voice:
- Only the first unit selected in the rectangle can speak, and only if its type is not 10, not 11–16 (TypeEnginEstEnLoop), and the player is local.
- A type-7 unit in state 11 or 15 first calls `PlaySnd_StopSound(EAX = record+0x104, EDX = 0x16)` and then EnginAsk mode 0x16. Every other unit asks mode 8.

EnginAsk volume (EnginGetVolume 0x440c5d):
- The distance is Distance2d from the view centre (x + w/2, y + h/2) of the u16 view at `0x508720`. The volume is 256 if the distance ≤ 0x91, 180 if ≤ 0x12c, 100 if < 0x258, otherwise 0. It is halved unless the unit is selected by the local player.
- Mode 0x10 forces 256.
- The request is `PlaySnd_PostSound(EAX = 0x50, EDX = type<<16 | mode<<8, EBX = record+0x104, ECX = flag, push volume)`.
- BatimentGetVolume (0x41a0ab) uses the same tiers from the structure cell, without halving. The structure request is `(EAX = 0x42, EDX = type<<16 | 0x800, EBX = structure+0x100, ECX = 0, push volume)`.

## Callees and dependencies

Callees reached in the capture:
- **Translated here** (all Core or unowned in the player-action map): EnginEstVivant, EnginGetPlayer, EnginGetType, EnginGetEtat, EnginVisible, EnginInZone, SwapWORD, TypeEnginEstEnLoop, TypeEnginEstVehicule, TypeEnginEstAerien, RetireSelectionEngin, BatimentTailleGet, BatimentGetDecalageConstruction, BagContientTroupe, BagContient (mode 1 only; other modes raise), BatimentGetVolume, EnginAsk, EnginGetVolume, EnginEstSelectionne, TerrainEstDecouvert and Distance2d.
- **From M2.3:** ResetOrdre and SetDeplaceEngin.

Named dependencies (no defaults; a path that reaches one without its provider raises `DependenciaRamoCore` at the original call, after the stores the original made before it):
- **Audio — `som(nome, registradores, pilha) -> EAX`** for `PlaySnd_PostSound 0x48aa79` and `PlaySnd_StopSound 0x48aac0`. The registers and the pushed volume are listed above. The returned EAX is what the caller then holds: the setters' and EnginAsk's exit EAX after a post is the library's return. The accepted frame bench declares it unchanged (the library is never initialized), and the comparison uses that declaration.
- **Combat — `definir_ataque(unidade, modo, referencia) -> {'EAX', 'EDX'}`** for `SetAttaqueEngin 0x445a36`. It performs the order stores, including its own ResetOrdre. EBX, ECX, ESI, EDI and EBP are preserved by the original.
  - The validator wires Combat's committed `ataque_vivo.definir_ataque` over live records with Core's ResetOrdre.
  - Register rule from the bytes: EAX = 1 when the same order is already active (it returns before ResetOrdre), otherwise the unit type; EDX = the record.

## What needs real input (deferred to the scripted-input captures)

- Which `ProcessInputGame` tag and packet reaches each setter, and with which arguments. The leaf calls declare the arguments; they do not show that the UI produces them. This is AI/runtime's ProcessInputGame cases, to be confirmed by S1/P1–P5.
- The CAVE icon / action mode `0x496207` (Deselection writes 0xff), and the HUD rectangles.
- The sound library's real return values after PlaySnd_* (Audio). The bench declares EAX unchanged.
- Paths MONDE01's state cannot reach without forcing:
  - the type-6 (crate) branch of SetDeplaceEngin;
  - BagContient modes other than 1;
  - selection lists of other players holding their own units (MONDE01 starts with player-0 units only);
  - SetAttaqueEngin on targets the raid creates.

Economy-owned setters `SetMineEnginSelect`, `SetDepotEnginSelect` and `SetRamasseEnginSelect` are not part of this Core slice.
