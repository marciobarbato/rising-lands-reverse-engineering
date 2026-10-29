# Core routines of the first monster raid (M2.3)

Date: 2026-10-29. Owner: Core. This contract applies to AI/runtime (`avancar_monstros`, the AvanceMonstre composition), Combat (raid capture and projectiles) and Missions (frame sequence).

## Trigger and scope

Combat's static analysis sets the trigger (`pesquisas-paralelas/combate/HANDOFF.md`, M2.3). AvanceMonstre `0x47b283` spawns MONDE01's first monster group when the cycle counter u32 `0x508f7c` reaches 9000, and then posts the group's first order. The Core routines that frame reaches are:

- **Spawn:**
  - `GetFreeCell`;
  - `CreerEngin`, which calls `EnginSetType` → `EnginSetTypeCaract` / `EnginTypeGetCapacite` (with Economy's `BonusGetValEngin`) and then `EnginEnArret`;
  - `EnginSetPlayer`;
  - `PlaceEngin`, which calls `SetEnginCollision` → `SetCollision` / `Chemin_ModifieZone` and then `SetMiniMap` mode 4 → `PlayerGetColor` / `TerrainEstIllumine`;
  - `Random`.
- **Order:**
  - `Random`, `EnginGetCase`, `EnginGetType`;
  - the target pick: `GetRandCaseChamps` (field) or `GetRandCaseTypeBatPlayer` (cave), the latter through `GetNumIndiceTypeBatiment` / `GetCaseIndiceBatiment`;
  - `Chemin_Accessible`;
  - the task list: `iaProbPost` → `iaProbNew` → `listNewElem`, then `listLinkElemToTail`.

## Capture (original-first)

[`ferramentas/capturar_incursao_core.py`](../../ferramentas/capturar_incursao_core.py) reruns Missions' committed frame path with their read-only `Isolamento` on AvanceMonstre, as Combat's raid capture does. At frame 1's AvanceMonstre entry it adds 21 declared forced cases. Every other byte is the exact frame-1 input:

| Cases | Writes |
|---|---|
| `counter9000` | u32 `0x508f7c` = 9000 (Combat's case) |
| `counter9000_seed*` (16) | the counter, plus the world RNG u32 `0x497164` set to a declared seed |
| `counter10800` | u32 `0x508f7c` = 10800 (records 0 and 1 both fire: two spawns) |
| `counter9000_cell*` (4) | the counter, plus record 0's cell u16 `0x50a9d0` set to `0x3e3e`, `0x8080`, `0x2e03` or `0x4a20` |

A nested recorder is armed only inside those cases. For every call to a Core routine above, in one native pass, it records:
- entry and exit registers;
- the six stack words after the return address;
- the enclosing call;
- bytes read before written, stack residue included;
- changed bytes, stack excluded.

The output uses the lossless run encoding of `compactar_captura_isolada`.

- **v1 scenario** (Combat's): [`captura-incursao-core-v1.json`](../../evidencias/fundacoes-quadro/captura-incursao-core-v1.json), 689 calls, all returned. The phase states and code integrity reproduce. It took 78.7 s.
- **Display scenario** (the M2 reference): `captura-incursao-core-exibicao.json` is requested from the Mac mini, because the display bench takes about 91 s per forced case.

**Branches captured:**
- GetFreeCell: a free cell found in ring 1, and 0xffff for centres off the 64×64 map.
- Three field cells: `0x2e03`, `0x2416`, `0x3b22`.
- One cave attempt: MONDE01 has no cave, so it finds none and falls back to a field.
- Two spawns in one frame.

## API

All functions are in [`ferramentas/incursao_core.py`](../../ferramentas/incursao_core.py). They take the flat memory interface of `chamadas_quadro_core` (`u8/u16/u32(addr, value=None)` and `ler`), and return the exact output registers. `ROTINAS[name] = (entry, f(memoria, registers, stack_words, bonus))`. `traducao_core(name)` also covers the frame-1 Core routines the raid reaches. `bonus(owner, type, selector)` is Economy's BonusGetValEngin (`BonusUnidades.consultar`).

| Original | Function | Inputs → result |
|---|---|---|
| GetFreeCell `0x479f20` | `celula_livre(m, eax, edx, esp)` | AX centre, DX type → EAX free cell or `0xffff` |
| CreerEngin `0x457e6c` | `criar_unidade(m, eax, edx, ebx, ecx, bonus)` | AX cell, DL direction, BL type, CL owner → EAX unit or `0xffff` |
| EnginSetType `0x457b87` | `definir_tipo_unidade(...)` | Combat's `definir_tipo` over the record. Flat search release: `0x496304`, `0x4e0f36/37/3c` |
| EnginSetTypeCaract `0x457350` | `caracterizar_unidade(m, eax, bonus)` | Combat's `caracterizar_tipo` |
| EnginTypeGetCapacite `0x4475ac` | `capacidade_tipo_engin(eax)` | table `0x447544` |
| EnginEnArret `0x448194` | `unidade_em_arret(m, eax)` | stop animation +0xa4 |
| EnginSetPlayer `0x443108` | `definir_dono_unidade(m, eax, edx)` | owner, also given to the members of group types 11..17 |
| PlaceEngin `0x456fa6` | `colocar_unidade(m, eax)` | owners 4/200 |
| SetMiniMap `0x46a388` | `definir_minimapa(m, eax, edx, ebx)` | mode 4 |
| EnginGetCase `0x44113e`, PlayerGetColor `0x46003b` | `caso_unidade`, `cor_jogador` | queries |
| GetRandCaseChamps `0x489147` | `caso_campo_aleatoria(m)` | random cell with object type `0x1c` |
| GetRandCaseTypeBatPlayer `0x489300` | `caso_estrutura_tipo_jogador(m, eax, edx)` | random cell of a structure with +4 = AL and +8 = DL |
| GetNumIndiceTypeBatiment `0x41db24`, GetCaseIndiceBatiment `0x41aab2` | `indice_tipo_estrutura`, `caso_indice_estrutura` | structure queries |
| Chemin_Accessible `0x42d4f8` | `acessivel(m, eax, edx)` | AL = same region |
| iaProbPost `0x47d920` | `postar_tarefa(m, eax, edx, ebx, ecx, pilha)` | player, type, args EBX/ECX/4 stack words → EAX task |
| iaProbNew `0x47d7ec`, listNewElem `0x47d012`, listLinkElemToTail `0x47d07a` | `tarefa_nova`, `lista_novo_elemento`, `lista_ligar_ao_fim` | the live lists at `0x5148a0`/`0x5148b0` |

## Original details kept

- **GetFreeCell** searches rings 1..29. In each ring it tests the row y−k, then the row y+k, then the columns x−k and x+k.
  - A column may equal the map width.
  - The column sides compare an x-based counter with the map height, and their first cell lags the row check by one.
  - Its 32-bit cell values add 16-bit locals whose upper words are never written. That stack residue (at ESP−0x32, −0x1a, −0x3a and −0x2e) is read as an input and reaches EAX's upper word.
  - Type classes (`0x4962c8`): 0 or above 3 take the first candidate; 1 tests the attribute mask (2 for types 0x10/0x11, else 1); 2..3 test a 2×2 footprint up-left and reject x = 0 or y = 0.
- **GetRandCaseChamps** keeps at most 201 matches. The 201st lands on the scan's own column bound, so drawing it returns that cell + 1.
- **CreerEngin** gives group types 11..17 other than 16/17 to owner 200. Type 4 sets +0xda = BonusGetValEngin(owner, 4, 12) + 10; types 14 and 16 clear it.
- **Exit registers:** EnginSetType's EBX is 0x1d and its EDX 0x1e, from its closing loop. EnginSetPlayer's and CreerEngin's EDX are 69·index (or the pool pointer). SetMiniMap's EBX is its pixel cursor.

## Not translated

These raise `DependenciaRamoCore` at their original address, after the original's earlier effects:
- **PlaceEngin** for owners other than 4/200 needs terrain discovery/illumination: it raises at `0x457019`. The world-model provider `colocacao_missao` covers those owners over `MundoFisico`.
- **SetMiniMap** modes other than 4 raise at their handlers (`0x46a49f`, `0x46a4d9`, `0x46a528`, `0x46a5a6`, `0x46a647`, `0x46a69d`). A zero map size raises at `0x46a3dc`.
- **GetRandCaseTypeBatPlayer** with more than 200 matches would overwrite its saved registers; it raises at `0x48933f`.

GetCaseIndiceBatiment is translated but no capture reaches it, because MONDE01 has no cave.

## Validation

- **Without a CPU:** [`testes/test_incursao_core.py`](../../testes/test_incursao_core.py) replays every captured call of every scenario from its read-before-write bytes, with registers EAX..EBP and changed bytes exact. That includes the frame-1 Core routines the raid reaches.
- **Native differential:** [`ferramentas/validar_incursao_core.py`](../../ferramentas/validar_incursao_core.py) reruns the forced cases. At every nested Core call it runs the translation over a copy-on-write view of the live memory at that entry, and compares its registers and changed bytes with the original's at the return. The results are in `relatorios/incursao-core-<scenario>-emulada.json`. For v1: **689 comparisons, 0 mismatches and 0 dependency stops**, every captured call of the 26 routines reached, with the phases and code reproduced (114 s). The display differential follows its capture.
