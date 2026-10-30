# Structure entry, lodging and Bag routines (M3/M4 groundwork)

Status: captured natively, translated and validated natively on `feat/re-core`, not yet integrated. These are the Core routines Economy's work cycle and lodging credit (`pesquisas-paralelas/economia/ciclo_trabalho.py`, feat/re-economy `612d67a`) and the M3 victory path name as dependencies. Addresses apply only to the intact `RISING.EXE` (SHA-256 `6c556520…8543fb`).

## Method (original first)

1. **Bench** (`ferramentas/bancada_entrada_estruturas.py`): the selection-orders pause (Missions' accepted MONDE01 display path, frame 1's first `ProcessInputGame` entry), extended with native preparation steps, mid-routine body entries with declared stops, and multi-step windows whose state carries from step to step.
2. **Prepared state `CAVERNA`**: original routines called natively from the pause, as Economy's capture does at frame 2: `CreerBatiment((23,14), 3, 0)` → structure 1; progress := target − 2; `BatimentConstruction(1)` completes it (owner stays 0xc8, origin (19,10), Bag capacity 2); `BatimentRetireColon(0)` releases colonist 3 to (15,14).
3. **Cases** (`ferramentas/casos_entrada_estruturas.py`): 384 declared cases, 505 measured steps, including two windows: the colonist's whole walk into the 0xc8 cave (order + 87 state-13 bodies, lodges at the last one, cave owner → 0) and worker 13 into the sanctuary (order + 34 bodies; it lodges and becomes a colonist through `EnginResetType`).
4. **Capture** (`capturar_entrada_estruturas.py` → `evidencias/entrada-estruturas/captura-entrada-estruturas-exibicao.json.xz`), committed before any translation (`ebea7e6`); 505/505 steps return or reach their stop; the run reproduces load_tail, between_frames and frame1 and leaves the code section unchanged (181 s). `extrair_entrada_estruturas.py` exports 49 original intervals and 7 jump tables.
5. **Translation** (`ferramentas/entrada_estruturas.py`, class `EntradaEstruturas`) over live flat memory.
6. **Native differential** (`validar_entrada_estruturas.py` → `relatorios/entrada-estruturas-emulada.json`): **505 comparisons, 0 mismatches**, 5,043 changed bytes compared, the native rerun equal to the capture step for step. Registers EAX..EBP compared except declared `_incertos` bits (19 steps, listed in the report). One declared domain stop (`entre_unit_type_out_of_branch`, type-16 entry at 0x449c56). Other fronts' callees (BatimentLogeEngin, iagUnitSendMessage, InitBatimentNeutre, PlayerInitPropositionAlliance) are the original's own nested call replayed (arguments checked, its stores applied, exit registers returned; 7 replays), as Economy's validators do. Bonus: Economy's committed `BonusUnidades`; sound: the bench's PlaySnd declaration (EAX unchanged), each request compared. The same run wrote `leituras-entrada-estruturas-exibicao.json.xz` (bytes read before written per step) for a future CPU-free replay test.

```sh
python3 "…/heavy_lease.py" core -- python3 -B ferramentas/capturar_entrada_estruturas.py --saida <new>.json.xz   # ~3 min
python3 "…/heavy_lease.py" core -- python3 -B ferramentas/validar_entrada_estruturas.py                           # ~4 min
RISING_EMULAR=1 PYTHONPATH=ferramentas:testes python3 -B -m unittest testes.test_emulacao_entrada_estruturas
```

| Routine | Steps | Mismatches |
|---|---|---|
| EnginNextEtape state-13 body 0x4558e4 (incl. the two windows) | 130 | 0 |
| EnginSelectPeutEntrer 0x472b6c (modes 1, 3, others) | 111 | 0 |
| SetEnginSelectRentreBatiment 0x473f4b | 30 | 0 |
| BagContient 0x4471b8 (every tag) | 28 | 0 |
| BatimentAdjacent 0x42381f, BatimentGetCaseEntrer 0x41d057 | 25 + 25 | 0 |
| PlaceLibre 0x41f552 | 19 | 0 |
| AnimWorkEngin 0x447f58, SetEnginRentreBatiment 0x445b10 | 18 + 18 | 0 |
| BagRetire, GetCaseCentrale, CalculEntreBatiment, BagContientTroupe, BagAccepte, RetireEngin | 12, 12, 11, 10, 9, 9 | 0 |
| BagPrend, EnginGetBag, EnginPeutPasser, BatimentRetireColon, EnginGetVolume, BatimentGetVolume | 5, 4, 4, 3, 3, 3 | 0 |
| BatimentGetCase, BatimentModifyMap, DecouvreTerrain, IllumineTerrain, SetEnginCollision, SetDeplaceEngin, TerrainEstDecouvert | 2 each | 0 |
| EnginGetType, EnginGetPlayer | 1 each | 0 |

## API

`EntradaEstruturas(memoria, *, externo=None, som=None, bonus=None)`; `chamar(nome, regs)` takes EAX..EBP and returns EAX..EBP as the original leaves them (flags not modeled), optionally with `_incertos = {register: mask}` (masked bits 0, never guessed). The module docstring lists every routine, its arguments, effects and register exits. The state-13 body is `chamar('EnginNextEtape:state13', regs)` with ESI = unit record, DI = unit (ai-runtime's state switch calls it; registers returned are those at the continuation 0x454ccd).

Reused single implementations: `selecao_ordens` (DeselectionEngin, SetDeplaceEngin, EnginAsk, volumes), `construcao_core` (DeplaceEngin, BatimentCollision), `chamadas_quadro_core` (BatimentGetCase, SetEnginCollision, TerrainEstDecouvert, EnginGetType/Player, EnginEstMiroir), `posicao_saida` (CalculPosition), M2.3's live world (`ocupar`, `minimapa`, `apagar_area`, `descobrir_area`, `iluminar_area`, `modificar_minimapa_estrutura`, `consultar_passagem`). SetSortEngin (inside BatimentEnleveUnColon) follows `colocacao_saida.colocar_unidade_saida`'s body order over live memory, because that function's protected-input check requires a `bytearray` pool a live view cannot pass.

**Uncertain bits** (world effects whose loops' registers are not reconstructed): DecouvreTerrain's and IllumineTerrain's EBX high word (a 16-bit local's never-written upper half); BatimentModifyMap's EAX/EDX; EnginPeutPasser's EAX bits 8+, EBX, ECX, EDX; DeplaceEngin's deep-callee EAX (as in CONSTRUCTION). Derived from loop bounds since the first delivery (M3.1 round 2, revalidated natively): IllumineTerrain's EAX = DX + 1 (sign-extended), EDX = DX, EBX low word = DX + 1 (0x476df9); RetireEngin's EAX for owners other than 4/0xc8 = EteintTerrain's last row index, radius + 1 sign-extended (0x476fba).

**Named dependencies** (`externo(nome, chamada, regs) -> regs`, never defaulted): Economy BatimentLogeEngin (0x449976), InitBatimentNeutre (0x41e0d7), BonusGetValEngin (`bonus`); ai-runtime iagUnitSendMessage (0x449bb8 msg 0x47, 0x4499ee/0x449af8 msg 0x44, 0x41da48 msg 0x42); diplomacy PlayerInitPropositionAlliance (0x449ad7); Audio PlaySnd_PostSound (`som`).

**Outside the translated domain** (`ForaDoDominioEntrada`, before any store of that branch): CalculEntreBatiment for unit types 11..24 (vehicles 0x44a12f, type 16 0x449c56); state 13's vehicle entry (+0xb8 set, 0x4559c6); BatimentRetireColon for types 0x13/0x15 and the last colonist of types 5/8/0xe; RechercheDecalageSortie for types 9/12/17; AnimWorkEngin with divisor 0 (the original faults). The original itself faults on BatimentRetireColon of an empty 0xc8 cave (EteintTerrain indexes player 0xc8's light grid), so that is not a case.

## Economy adapter

`provedor_entrada(entrada, outros=None)` is Economy's `externo(nome, chamada, registradores)` for `ROTINAS_ECONOMIA` (DeplaceEngin, SetDeplaceEngin, BatimentGetCase, GetCaseCentrale, BatimentAdjacent, EnginPeutPasser, SetEnginCollision, RetireEngin, AnimWorkEngin, EnginGetVolume, EnginGetType, EnginGetPlayer, EnginGetBag, PlaceLibre, BatimentModifyMap, BatimentGetVolume, BagContient, BagContientTroupe, BagRetire, BagPrend, DecouvreTerrain, IllumineTerrain, TerrainEstDecouvert). Same shape as `provedor_construcao`, plus: Economy passes only argument registers (its `ARGUMENTOS` widths), so a missing register enters as 0 with a full uncertain mask, carried to the output when the callee leaves it unchanged. Other names go to `outros` (e.g. `provedor_construcao(...)`, then `provedor_core(SelecaoOrdens(...))`) or raise `DependenciaRamoCore`.

**CPU-free replay** (`testes/test_entrada_estruturas.py`): the 340 steps whose routine does not run on M2.3's live world replay exactly from `leituras-entrada-estruturas-exibicao.json.xz` (registers and every changed byte; the translation reads no byte the original did not read). The world-backed routines (RetireEngin, SetDeplaceEngin, EnginPeutPasser, DecouvreTerrain, IllumineTerrain, BatimentModifyMap, CalculEntreBatiment, the state-13 body, BatimentRetireColon) stay native: the world is built from pointers the original never reads.

Not yet done: replaying Economy's own ciclo-trabalho capture through `CicloTrabalho(externo=provedor_entrada(...))` (their module is not on main yet).
