# M2 frame inventory — Economy (Step 1, static)

Scope: the economy routines that the original `CalculGame 0x42c868` frame body reaches, and which branches the frozen M1 MONDE01 post-load state can reach in the first frames. Static reading of the intact executable only; nothing in this file was executed. Step 2 captures and implementations are recorded separately.

- Intact `RISING.EXE` SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`. Interval hashes below are SHA-256 of the exact bytes `[start, end)` of the mapped image.
- Post-load input: `pesquisas-paralelas/missoes/evidencias/captura-carga-missao-original-v2.json`, `oracle.final_state.blocks` (881 blocks, state SHA-256 `58a5020e79f812e741991410bde0ebc847c927ce141176975a82c0a51a7a1114`), read-only. It is the accepted M1 snapshot at `MissionLoad`'s return to `0x42d22d`, **not** a frame-1 input.
- Main at inventory time: `81ebbf9`.

## Frame order and frame counter

The economy calls sit in the in-game path of `CalculGame` (`0x42d3e1..0x42d46c`):

```
0x42d3f5 CalculEnginNextEtape      (ai-runtime loop → EnginNextEtape state bodies)
0x42d3fa CalculBatimentNextEtape   (ai-runtime loop → BatimentNextEtape type bodies)
0x42d3ff RechercheCalcul()
0x42d404 PlayerInitAllianceCompteur()
0x42d409 SetUpdateChamp()
0x42d40e UpdateChamp()
0x42d413 CalculMatiere()
0x42d41f CalculCompteurMarche(EAX = u8 [0x508041])
0x42d42d CalculCompteurProposition(EAX = u8 [0x508041], EDX = 0)
   ... NextAnim* (graphics) ...
0x42d46c PlayerAttaqueCalculSympa()
```

The frame counter u32 `0x508f7c` is 0 in the M1 snapshot. `CalculGame` stores 0 again at `0x42d2be` (with `0x508f80`/`0x508f84`) after `MissionLoad`, and `ProgIteration 0x47500e` increments it at `0x475014` before each frame. So the frame-k counter is expected to be k; Missions' frame-1 capture must confirm this. Every modulo gate below depends on it.

MONDE01 values read from the M1 snapshot: local player `0x508041` = 0; network byte `0x4e0730` = 0; mission number `0x496fe4` = 1; RNG state `0x497164` = `0x4926732e`; player records at `[0x5080a8]` = `0x41896000`, type byte `+1`: player 0 = 1 (human), players 1–3 = 2 (AI).

## Direct frame callees

| Routine | Interval (exclusive end) | Bytes SHA-256 | ABI | Reads | Writes | Callees |
|---|---|---|---|---|---|---|
| `RechercheCalcul` | `0x47125c..0x47149d` + shared epilogue `0x4709f3..0x4709f9` | `19f9e5a6…af4e0f` | no inputs; preserves EBX/ECX/EDX/ESI/EDI; x87 | u8 `0x50871c[p]`, 16-byte players `0x5080f4+16p` (`+0..+3` item per branch, `+4` branch, `+8` f64 accumulator), u16 `0x508174[p]` (scientists), research table `0x50817c + branch·0x168 + item·12` (`+0` u32 cost, `+4` u8, `+5` u8 minimum mission, `+6` u8 `0xff` end marker), f64 `0x494cbb` (= 2.0), `MissionGetNum` | f64 `+8`, u16 `0x508174[p]`=0, branch `+4`, item byte, `0x50871c[p]` | `MissionGetNum 0x46c11a`, `InventionSetEffet 0x470f98` (AL=p, DL=item, BL=branch, ECX=1) |
| `PlayerInitAllianceCompteur` | `0x46da3b..0x46dadb` | `01c5b67c…ed4a674` | no inputs; preserves all GPRs | u32 counters `0x5080b0 + 16p + 4q`, `0x508041` | counter −1 when nonzero | `InitGameZone 0x471830(EAX=1, EDX=EBX=ECX=0)` then `MAJSympathie 0x475118(AL=q, DL=p, EBX=9)` only when a local-player counter reaches 0 |
| `SetUpdateChamp` | `0x475328..0x47534a` | `4125ba37…8e1a1a5` | no inputs | `0x508f7c`, u16 period `0x4973ea` (= 128) | u8 `0x509952` = 1 when counter % period = 0 | — |
| `UpdateChamp` | `0x478806..0x478a01` | `f2c9eb78…a4c63` | no inputs | `0x509952`, u16 row `0x4973e8` (= 1), terrain, RNG `0x497164` | terrain types, row, flag, RNG | `Random`, field helpers |
| `CalculMatiere` | `0x467718..0x4678f2` | `747a6f4a…c2013` | no inputs; preserves all GPRs | local player's four 8-byte records `0x4e2ea8 + 32·local + 8r`: `+2` total, `+4` presentation, `+6` digit bits | `+4` presentation (via `BCDToInt`), `+6` bits, u8 `0x4e05a2` = 1 | `IntToBCD 0x467cd1`, `BCDToInt 0x467d3a`, `GetBit 0x467d97`, `SetBit 0x467d71` (all leaves) |
| `CalculCompteurMarche` | `0x466dd1..0x466e9b` | `55e6d6f4…a38cb2` | AL = player | `0x4e2928[p]`, partner `0x496f8c[p]`, state `0x4e2e7c[x]`, `0x4e292c[x]`, `0x508f7c`, u16 `0x496f90` (= 100), u16 `0x4e2938`/`0x4e2930` | state, u16 `0x4e2938` | `EvalueCoutProposition 0x466bac`, `ResetMarche 0x46634e`, `MessageBoxSet 0x46994b` |
| `CalculCompteurProposition` | `0x466e9b..0x466fef` | `587728a4…c93b21` | AL = player, EDX = 0 (unused) | as above plus u16 `0x496f92` (= 100), u16 `0x4e2940` | u16 `0x4e2940` | `MessageBoxSet`, `CalculValeur 0x466533`, `ForgetMarche 0x4610a4`, `ResetMarche`, `PlayerGetType 0x46d817`, `MAJSympathie` |
| `PlayerAttaqueCalculSympa` | `0x46d629..0x46d6a3` | `db0e0592…485e6f` | no inputs | `0x508f7c`, u32 attack flags `0x508044 + 20p + 4q` | the 16 flags = 0 | `MAJSympathie(AL=p, DL=q, EBX=0x13)` for p ≠ q whose flag was 0 |

Leaf helpers of `CalculMatiere`: `IntToBCD 0x467cd1..0x467d3a` (`8a21d598…`), `BCDToInt 0x467d3a..0x467d71` (`70017bfc…`), `SetBit 0x467d71..0x467d97` (`a89cba60…`), `GetBit 0x467d97..0x467da6` (`5ad94644…`). `MissionGetNum 0x46c11a..0x46c122` returns AL = `0x496fe4`, AH = 0.

**Ownership of `PlayerInitAllianceCompteur`.** From the bytes it is the per-frame countdown of the alliance-proposal counters `0x5080b0`. Their other writers are `SetPropositionAlliance`, `PlayerInitPropositionAlliance`, `InitPlayer`, `LoadPlayer` (all in the player/diplomacy block that Economy already owns through `PlayerRetrieve 0x46df41`). It is economy-owned. Its two callees are not: `InitGameZone` is UI (it also reads the market state `0x4e2e7c`), and `MAJSympathie` is the shared sympathy update (also called by `PlayerAttaqueCalculSympa`, `CalculCompteurProposition` and unit state 23). Both become named dependencies until an owner is agreed.

## Dispatcher branches the MONDE01 state reaches

### Structures (`CalculBatimentNextEtape` → `BatimentNextEtape`)

Only structure 0 is live (state byte `+5` ≠ 0): owner 0, state 5, type 2 (`SANCTUAIRE`). Its Bag at `+0x0c` has capacity 16 and eight tag-1 references to units 3..10, all type 9. The type-2 branch `0x426918..0x42698d` (`52b41c56…`) runs:

1. `BagContientTroupe 0x44724a(EAX=bag)` (`1da9b4ca…`): the first tag-1 slot references unit 3, type 9, which is not in the excluded set {3, 11–17, 25}. It returns 1 at once.
2. Because AL ≠ 0, `BagContient` is **not** called, and `CalculTroupe 0x4259e6(EAX=0)` runs.
3. `CalculTroupe` for type 2 dispatches through `0x426401` to the shared type-16 body. Progress u32 `+0x8c` = 0 and activity `+0x74` = 0, so the call is inactive: no time query, no progress, no `SortieTroupe`.

Production can only start through `InitRecruteTroupe 0x4283e2`, whose callers are `ProcessInputGame 0x45f1a9` (human input) and `V_BatimentRecruteUnite 0x480749` (AI). Player 0 is human, and AI players 1–3 own no structures. **With no human input, MONDE01 structure production stays inactive in M2.** `RechercheAddScientifique 0x470bf7`, the only writer of `0x508174` besides `RechercheCalcul`/`RechercheEndTechnologie`, is reached only from the type-7 branch (`0x426e39`). MONDE01 has no type-7 structure.

### Units (`CalculEnginNextEtape` → `EnginNextEtape`)

Live units: 0, 1, 2 (type 0), 11 (type 1), 12 (type 7), 13, 14 (type 5) and 15 (type 8), all owner 0 in state 7; 3..10 are type 9 in state 14. State 14 exits directly. State 7, owned by Economy under the ai-runtime agreement, is `0x456966..0x4569f0` (`f5f7c10b…`), exiting at `0x454ccd`:

- Unit types 0–10 and 18–25 take the `Random` path. Type 17 calls `AnimBallonStatic 0x447b2f` (`0x456957..0x456966`, `73ec1a7e…`). Types 11–16 and ≥ 26 exit. All MONDE01 state-7 types (0, 1, 5, 7, 8) take the `Random` path.
- `Random 0x4704dc` (Park–Miller/Schrage on `0x497164`; EAX = 0x24 is ignored) is called once per such unit per frame. When the result % 200 = 0, it stores `(byte +0x91 % 16) + 1` into `+0x90` and `+0x91`.

So **every frame consumes eight RNG draws in unit order** (0, 1, 2, 11, 12, 13, 14, 15), interleaved with whatever the shared prelude draws. Work (state 5, `CalculWorkEngin 0x44bc74`), transport (18, `CalculTransporteEngin 0x44f2d4`), harvest (19), unload (20) and market/technology (23) need an order. Orders come only from human input or AI messages, and owner 0 is human. **None of those branches is reachable from the MONDE01 state without input.** They are not part of this slice. The shared prelude also queries `BonusGetValEngin 0x428cc0(AL=owner, DL=3)` for the reload advance. That is already reconstructed as `bonus_unidades.BonusUnidades.consultar` and natively validated.

## MONDE01 first-frame reachability per routine

| Routine | M1 inputs | First-frame effect | Later frames |
|---|---|---|---|
| `RechercheCalcul` | `0x50871c` all 0 → all four players enter. Current items: p0 branch 0 item 2 (cost 7500), p1 branch 1 item 2 (15000), p2 branch 2 item 4 (200), p3 branch 0 item 2 (7500). Every `+6` ≠ 0xff and `+5` = 1 ≤ mission 1. Scientists `0x508174` = 0, accumulators 0.0 | Adds +0.0 (the zero-scientist path stores the zero dword pair), stores u16 0, cost > accumulator → no invention. Bytes unchanged | Unchanged while no type-7 structure adds scientists. `InventionSetEffet` unreachable |
| `PlayerInitAllianceCompteur` | all 16 counters 0 | Read-only | Unchanged without diplomacy input. `InitGameZone`/`MAJSympathie` unreachable |
| `SetUpdateChamp` | period 128, flag 0 | None (1 % 128 ≠ 0) | Sets the flag at counter 128 |
| `UpdateChamp` | flag 0, row 1 | Returns at `0x47881e` | Rows 1..255 from frame 128, one row per frame, drawing RNG |
| `CalculMatiere` | local 0: food (id 1) and stone (id 2) total 30, presentation 0, bits 0; parts and fourth record all 0 | **Mutates**: the tens digit of each nonzero record alternates set-bit / increment-and-clear; presentation reaches 10/20/30 at frames 2/4/6; `0x4e05a2` = 1 (already 1) | Idle once presentation equals total |
| `CalculCompteurMarche(0)` | `0x4e2928[0]` = 0 → partner `0x496f8c[0]` = 0xff → reads `0x4e2e7c[0xff]` = byte `0x4e2f7b` = 0 | Read-only return (≠ 3). Note the out-of-table index 255: the read lands 3 bytes after the `CalculGame` state byte `0x4e2f78` | Only market state 3 enters the counter branch |
| `CalculCompteurProposition(0, 0)` | same partner and `0x4e2f7b` = 0 | Read-only return (≠ 4, ≠ 5) | — |
| `PlayerAttaqueCalculSympa` | flags `0x508044` all 0 | None (1 % 2000 ≠ 0) | At counter 2000: twelve `MAJSympathie(p, q, 0x13)` calls for p ≠ q, then flags cleared |
| Type-2 branch + `CalculTroupe(0)` | see above | `BagContientTroupe` → 1; inactive `CalculTroupe` return | Inactive while no recruitment is started |
| Unit state 7 | 8 units, facing `+0x90`/`+0x91` = 1 | 8 `Random` draws. Facing changes only on a draw % 200 = 0 | Same every frame |

## Existing Economy implementations versus need

| Routine | Status before M2 |
|---|---|
| `SetUpdateChamp`, `UpdateChamp` | Implemented: `extracao.RecursosTerreno.agendar_campos` / `atualizar_campos`, native-validated (`bancada_extracao.py`). They take copies of the period, row and flag through constructor fields, not the live DGROUP addresses. Frame composition must bind them to `0x4973ea`/`0x4973e8`/`0x509952` and to the shared RNG `0x497164` by identity |
| `BagContientTroupe`, `BagContient`, `CalculTroupe` (types 1/2/13/16) | Implemented and native-validated (`limpeza_saida.bag_contient_troupe`, `Producao.contar_unidades`, `Producao.calcular_tropa`) |
| `BonusGetValEngin` | Implemented and native-validated (`bonus_unidades.BonusUnidades.consultar`) |
| `EvalueCoutProposition`, `ResetMarche` | Implemented (`mercado.Mercado`, `ciclo_mercado.CicloMercado`); not reached in MONDE01's first frames |
| `CalculMatiere` (+ `IntToBCD`/`BCDToInt`/`GetBit`/`SetBit`) | **Missing**; reached with real mutations |
| `RechercheCalcul` | **Missing**; reached each frame (no-op effect in MONDE01) |
| `PlayerInitAllianceCompteur` | **Missing**; reached each frame (read-only in MONDE01) |
| `CalculCompteurMarche`, `CalculCompteurProposition` | **Missing**; reached each frame (gate only in MONDE01) |
| `PlayerAttaqueCalculSympa` | **Missing**; reached each frame (gate only until counter 2000) |
| Unit state 7 body | **Missing**; reached each frame for 8 units, consumes RNG |
| `CalculWorkEngin`, `CalculTransporteEngin`, states 19/20/21/23 | Missing; **not reachable** from the MONDE01 state without orders. Out of this slice |

## Step 2 selection (no speculative features)

1. Original-only captures at the M1 snapshot, labelled "M1 post-load state, not frame-1 input": each reached routine entered natively over the whole mapped M1 memory, with the frame counter set to declared values (1, 2, …; 128 and 2000 for the gates). Includes a multi-call `CalculMatiere` sequence until the presentation converges, and the state-7 body for the 8 MONDE01 units over successive RNG states. Commit captures before translation.
2. Python over live shared buffers: `CalculMatiere` (whole routine), `RechercheCalcul` (stopping with a named dependency at the `InventionSetEffet` call `0x47132c`), `PlayerInitAllianceCompteur` (dependency at `InitGameZone` `0x46dab8`), `CalculCompteurMarche`/`CalculCompteurProposition` (gate; dependencies at the first unreached branch call), `PlayerAttaqueCalculSympa` (dependency at `MAJSympathie` `0x46d696`), and the state-7 body (dependency at `AnimBallonStatic` `0x45695c` for type 17). The RNG is the same 4-byte DGROUP memory, never a copy.
3. Native differential against the captures, then re-validation at the exact frame-1 inputs when Missions publishes them.

## Cross-front contracts

- **Missions / coordinator:** confirm the frame-1 counter value and the frame-1 entry state (this inventory assumes counter k at frame k).
- **ai-runtime:** the dispatcher calls the economy state-7 body with EAX = u16 unit, EDI = the same unit as the original register (the body uses DI), and returns through `0x454ccd`. The type-2 branch is unchanged (`Producao.calcular_tropa`).
- **Owner needed:** `MAJSympathie 0x475118` (sympathy; Economy proposes to own it with the player block), `InitGameZone 0x471830` (UI; graphics/macOS), `MessageBoxSet 0x46994b` (UI), `AnimBallonStatic 0x447b2f` (graphics), `InventionSetEffet 0x470f98` (Economy research, later stage). None is reached in MONDE01's first frames.

## Erratum after Missions' first-frame capture (M2.1 round 2)

Missions' original capture (`pesquisas-paralelas/missoes/QUADRO1_MONDE01.md`) shows that `CalculGame`'s load-state invocation already runs one frame body ("frame 0"), with counter 0, and that frame 1 runs with counter 1. The assumption above (counter k at frame k ≥ 1) is replaced by frame k at counter k for k ≥ 0. Consequences, confirmed by the isolated exact-frame capture:

- `SetUpdateChamp` sets the flag in frame 0 (0 % 128 = 0). `UpdateChamp` then processes row 1 in frame 0 and row 2 in frame 1, with no RNG draw in these rows.
- `PlayerAttaqueCalculSympa` runs its loop in frame 0. It calls `MAJSympathie(p, q, 0x13)` twelve times, and every call returns at the AI-context gate (`0x51a990 + 16p` = 1 for players 1–3). `MAJSympathie` is therefore reached, and Economy owns it (it writes only the player block, through `PlayerSetSympathie`).
- `CalculMatiere` sets the digit bits in frame 0, and the presentation reaches 10 in frame 1.
- `ResetTableauHangar 0x461e33` (market block, `0x4e296c`) runs at the start of `CalculBatimentNextEtape` every frame. In frame 0 it changes the 40 words from 0 to `0xffff`.
- The unit prelude calls `BonusGetValEngin` 24 times per frame. The type-2 branch calls `BagContientTroupe`, then `CalculTroupe` (inactive), and the structure loop calls `BatimentGetCase` (= `0x0c0e`).
