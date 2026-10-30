# Hunger entry, food search and light removal (S1 path)

Status: original-first on `feat/re-core`. Economy's hunger body (state 19, `alimentacao.py`) and SortieTroupe's abandonment (`caverna_recrutamento._abandonar`) name these Core routines. The Mac mini's S1 run enters EnginSetFatigue and its ChercheVegetLibre at frame 7958.

Module: `ferramentas/fadiga_vegetacao.py`. Validator and capture: `ferramentas/validar_fadiga_vegetacao.py`. Original SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

## Routines

| Routine | Original bytes | Inputs | Exit registers |
|---|---|---|---|
| EnginSetFatigue | `0x453b84..0x453d56`, tails `0x44b334..0x44b34a`, `0x44f29d`, `0x440d58` | AX unit (0..799) | EAX by path (below); EBX..EBP preserved |
| ChercheVegetLibre | `0x477b74..0x477e91` | AX cell, DX radius word, BL/CL object byte bounds, pushed unit (RET 4) | EAX cell or 0xffff; EBX/ECX/EDX exact by path; ESI/EDI/EBP preserved |
| ChercheTypeBatimentProximite | `0x4538fa..0x4539f3` | AX cell, DX radius word, BL type, CL owner | EAX index or 0xffff; EDX 1000; EBX/ECX the scan's last values; ESI/EDI/EBP preserved |
| EteintTerrain | `0x476e82..0x477042`, epilogue `0x476e7b` | AX cell, DX radius, BL owner (0..3) | EAX = sign-extended word DX+1; EDX = DX; EBX = −EDX + 2·DX + 1; ECX/ESI/EDI/EBP preserved |

**EnginSetFatigue.**
- If word +4 is 4, or the state is 19, nothing happens and EAX is that value.
- Otherwise it stores +0xa0 := the state byte and +0xa2 := +0x7e, then calls ChercheVegetLibre(+8, 20, 0x43, 0x43, push unit).
- **Sack found:** +0xc2 := 0xffff, state 19, +0x7e := the cell. If the unit owns the path search (0x496304), it is released (0x4e0f36/37 := 0, 0x4e0f3c := 0, 0x496304 := 0xffff). Then +0x88 := 0, and EAX is the entry EAX.
- **No sack:** it calls Economy's TestRessource(food 3, 0, 0, push owner). If that fails, EAX is TestRessource's EAX.
  - Otherwise ChercheTypeBatimentProximite(+8, 40, type 3, owner). If a cave is found: state 19, +0xc2 := the cave, +0x7e := BatimentGetCase(cave), search release, +0x88 := 0, and EAX is the entry EAX.
  - With no cave, the chain stops at the first exit that applies:
    - owner ≠ local player: EAX = 0xff00 | owner;
    - +0x74 ≠ 1: EAX = +0x74;
    - cell not discovered by the local player: EAX = TerrainEstDecouvert's EAX;
    - otherwise EnginGetVolume runs and +0xf9 := 0. If the handle +0x104 ≠ −1, EAX is the volume. Else Audio's PlaySnd_PostSound(0x50, type<<16 | 0xc00, rec+0x104, 0, push volume), and EAX is what it returns.

**ChercheVegetLibre.**
- It checks the cell itself first, then rings k = 1..DX. On ring k, for i = −k..k it tests (y+i, x−k) and (y+i, x+k). Only for −k < i < k does it also test (y−k, x+i) and (y+k, x+i).
- A cell qualifies when it is in the map, its object byte is in [BL, CL] (unsigned), and EnginPeutPasser(unit, cell, 1) passes.
- EnginPeutPasser is evaluated inline, with its exact registers, for the types that reach its 0x4426c7 path: 0..2 and 4..10. That is every fatigable type except 3 and 25.
  - The unit's own cell (+8 or +0x7c, unless +0xab, the mask or state 14 excludes it) passes with EBX 0x101 and EDX = the cell.
  - Otherwise a clear attribute bit passes and a set bit fails, both with EDX 1 and EBX 0x100. EBX is 0x101 instead when an early exclusion left EnginOccupeCase's BL at 1.
- EAX's upper half on hits from the first two ring checks comes from the never-written upper words of the 16-bit locals `[esp+0x10]` and `[esp+0xc]`.

**EteintTerrain.** This is the routine RetireEngin and BatimentRetireColon already reach through `visao_movimento.apagar_area`.
- It visits rows i = −DX..DX, then columns j = −DX..DX. On each map cell where (i²+j²) mod 65536 ≤ (DX² + [DX ≥ 2]) mod 65536, EteintCase removes one light count for the owner.
- A second identical pass only reads.
- When no row of the disc is inside the map (a centre below the map rows), EBX is instead the first pass's `[esp+8]` + 1. Its upper word is a never-written stack word.

## Stack residue and `_incertos`

The registers that come from uninitialized stack words are exact when the call passes `ESP`, the routine's entry ESP, and that stack is readable in the memory given to `FadigaVegetacao`. Otherwise they come back as 0 and are named in `_incertos`:
- ChercheVegetLibre's EAX bits 16..31 on ring checks 1 and 2;
- EteintTerrain's EBX bits 16..31 in the no-row case.

Callers use only AX of ChercheVegetLibre (EnginSetFatigue, state 19). SortieTroupe's EteintTerrain centre is always inside the map.

## Providers

`provedor_fadiga(FadigaVegetacao(memoria, externo=..., som=...), outros=None)` has the shape of `provedor_entrada`.
- **Required:** the registers in `ARGUMENTOS_EXIGIDOS` must be present, or the call raises `ArgumentoNaoPassado` before anything runs:
  - EnginSetFatigue: AX;
  - ChercheVegetLibre: AX, DX, BL, CL, plus `_pilha` = [unit];
  - ChercheTypeBatimentProximite: AX, DX, BL, CL;
  - EteintTerrain: AX, DX, BL.
- **Optional:** `ESP`.
- **Missing other registers** enter as 0. They come back in `_incertos` when the routine leaves them unchanged.
- **Named dependencies:**
  - `externo('TestRessource', 0x453c5f, {EAX, EDX, EBX, ECX, _pilha: [owner]})`: Economy's `ordens_economia`;
  - `som('PlaySnd_PostSound', regs, [volume]) -> EAX`: Audio, in the shape of `selecao_ordens`.

**Owed by Economy:**
- `alimentacao.ARGUMENTOS['ChercheVegetLibre']` lacks ECX. `_procurar` sets ECX = 0x43, but `_ext` drops it, so the provider raises `ArgumentoNaoPassado(ECX)`. Add `'ECX': 0xff`.
- Pass the pushed unit as `_pilha`. This already happens through `PILHA_EXTERNA`.
- `caverna_recrutamento._abandonar` should call `EteintTerrain` through `provedor_fadiga` with EAX = BatimentGetCase's cell, EDX = the radius from table 0x420df4 (sanctuary 10, cave 8), and EBX = the owner.

## Out of the translated domain (`ForaDoDominioFadiga`, no store by the branch)

- a unit index above 799;
- EnginPeutPasser inside ChercheVegetLibre for unit types 3 and 11..25 (raised at the first passage test; the search stores nothing);
- ChercheVegetLibre radius words 0x7fff and above;
- EteintTerrain owners other than 0..3 (owner 0xc8 indexes past the light-grid pointers and faults in the original) and radii above 0x7ffe.

## Capture first, then native differential

`validar_fadiga_vegetacao.py` reruns Economy's own scenarios on `bancada_ciclo_trabalho.Ciclo` (frames 0/1 reproduced, code unchanged), imported read-only. Until Economy's `bfef1ce` reaches main, its two scenario files were taken with `git show` into a scratch directory (`--fontes-economia`). Each report records the Economy versions it ran; only Core's files bind it.

**Scenarios:**
- **`fome`** (`capturar_alimentacao.ordens`, to frame 1200): declared hunger of unit 12 at frame 1100 and unit 14 later. EnginNextEtape's own call at `0x45498f` enters EnginSetFatigue natively: 14 in-situ calls. Unit 12 at 1100 and unit 14 at 1163 find a sack. The repeats return at state 19.
- **`abandono`** (`capturar_abandono_santuario.ordens`, to frame 470): SortieTroupe's EteintTerrain at `0x421116`, frame 455, sanctuary centre 0xc0e, radius 10, owner 0, 958 bytes changed.

**What each case runs:**
- **In-situ cases** are the bench's isolated calls. AvanceEngin's and RetireEngin's EteintTerrain (vision sum 5) are capped at their first calls.
- **Nested snapshots:** at each EnginSetFatigue, the whole state is snapshotted at the entry of its ChercheVegetLibre and ChercheTypeBatimentProximite.
- **Declared variants** run the original routine as a leaf from a snapshot, with stack words pushed as the callers push them:
  - EnginSetFatigue: 12 per call (guards, search release, no sack → cave, no food, no cave with +0x74 = 0/1, a busy voice handle, an undiscovered cell, another local player, upper EAX bits);
  - ChercheVegetLibre: radii 0–40, object bounds, the eight map edges, the own cell with occupancy passing or excluded (+0xab, state 14), upper register bits, units 13/14;
  - ChercheTypeBatimentProximite: 8 per call;
  - EteintTerrain: radii 0–23 including 8 and 10, owners 0–3, EDX upper bits, map corners and edges, and a centre below the map with and without rows inside.
- **ChercheVegetLibre outside EnginSetFatigue** ends with RET 4, which the bench's isolation cannot model. Such calls are snapshotted by a code hook and run as leaves at the next frame start. These scenarios have none.

**Comparison:** each case is compared with `fadiga_vegetacao` over a copy of its exact entry state, stack included, at the case's ESP. The comparison covers EAX..EBP, ESP, every byte of every block, and the sound request. Every native case also equals the committed capture.

| Scenario | Capture | Report | Cases (per routine) | Mismatches |
|---|---|---|---|---|
| fome | `evidencias/fadiga-vegetacao/captura-fome.json.xz` | `relatorios/fadiga-vegetacao-fome-emulada.json` (513 s) | EnginSetFatigue 182, ChercheVegetLibre 58, ChercheTypeBatimentProximite 112, EteintTerrain 47 | 0 |
| abandono | `evidencias/fadiga-vegetacao/captura-abandono.json.xz` | `relatorios/fadiga-vegetacao-abandono-emulada.json` (223 s) | EteintTerrain 45 | 0 |

Totals are 444 comparisons and 30,179 changed bytes. No case has uncertain bits, because every comparison passes the real ESP. The exact residue matters natively: unit 14's in-situ ChercheVegetLibre returns EAX 0x441f18, whose upper word comes from the stack.

**Preserved first run:** the first full hunger differential had 8 mismatches. It is kept in `.local/fadiga-vegetacao/falha-fome-20261030T005324.json`.
- Six were EBX 0x100 vs 0x101: EnginOccupeCase's early exclusions keep BL = 1.
- Two were the validator's sound stub: a boundary with `declared_eax` None leaves EAX as passed.
- Both are fixed in the translation and the validator. The original captures are unchanged.

**Tests:**
- `testes/test_fadiga_vegetacao.py` (CPU-free) checks the capture facts, the real call sites, the reports bound to Core sources with 0 mismatches, and the provider shapes.
- `testes/test_emulacao_fadiga_vegetacao.py` (`RISING_EMULAR=1`) reruns the abandonment scenario.

```sh
python3 "…/heavy_lease.py" core -- python3 -B ferramentas/validar_fadiga_vegetacao.py --cenario fome      # ~9 min
python3 "…/heavy_lease.py" core -- python3 -B ferramentas/validar_fadiga_vegetacao.py --cenario abandono  # ~4 min
```

## Not run / open

- ChercheVegetLibre from the state-19 body (`0x455756`) and from the transport routines: their calls were never reached in these scenarios. The translation is the same body.
- ChercheTypeBatimentProximite reached nested in situ: the scenarios always find a sack. It is covered by direct leaves and by EnginSetFatigue's "no sack" variants.
- EnginPeutPasser for types 3 and 11..25.
- The S1 snapshots themselves (Mac mini).
