# Logic-state effects of RestoreAll and AffGame (M2 round 4)

Original-only. Input: Missions' `exibicao` scenario (intact `RISING.EXE`), phases (a) `load_tail`, (b) `between_frames`, (c) `frame1`. Capture: [capturar_efeitos_logicos_exibicao.py](capturar_efeitos_logicos_exibicao.py) → [evidencias/efeitos-logicos-exibicao.json](evidencias/efeitos-logicos-exibicao.json). Both passes reproduce Missions' three phase states.

Method: pass 1 records every **value-changing** write inside the dynamic extent of RestoreAll (`0x474b08`) / AffGame (`0x417698`) (entry hook, return hooks matched on ESP). Pass 2 hooks reads of exactly those bytes and keeps reads by code outside both extents.

## Result

In the three phases RestoreAll runs once (a, view origin (4,6)) and AffGame once (b, mode `[0x4e2f78]`=0x12). Value-changing written bytes: 453,300 declared-surface pixels, 1,619 bench-stack bytes, 80,256 + 25 + 245 bank/cache/palette heap bytes, and **33 DGROUP bytes**. Logic readers of those bytes: **none**. The only reads of the DGROUP bytes (`0x4e17a4..ab`, the nested-lock bookkeeping) are DDLockSurface/DDUnlockSurface themselves.

| DGROUP bytes written | Writer | Verdict |
|---|---|---|
| `0x4e17a4..ab` | DDLockSurface/DDUnlockSurface (RestoreAll) | display bookkeeping, restored to 0 |
| `0x496394..96`, `0x4963b5` | CalculFrame, utoa (AffGame) | fps text |
| `0x4e17ae`, `0x4e17b0..b7` | CalculFrame | frame ticks / flag |
| `0x49a02e/32`, `0x49a042..45` | Save/RestaureClipping, AffGame | clip words |
| `0x49a04e/4f` | GetNumBob (RestoreAll) | bob cache counter |
| `0x4e05a2` | AffGame `0x417a87`.. | set 0 then 1 in the same extent, net zero |

Not written by either routine in the captured domain (zero value-changing writes): `0x4e1d18`, the CRT rand seed (thread block +0xc), `0x508f72/73` (same-value stores), `0x508720/22`, `0x5099xx`.

**Correction of the attribution in `QUADRO1_EXIBICAO.md`:** `NextAnimTerrain` and `NextAnimVeget` are called by **CalculGame** (direct callers `CalculGame+0xbd9` and `CalculGame+0xbff`, the only ones), not by RestoreAll/AffGame. The CRT `rand` stream and `0x4e1d18` advance there, and the dependence on display is through DDInit's inputs: viewport `0x508724/26` = 25×17 and screen `0x49a018/1a` = 800×600 (4 stores, `DDInit+0x1d/0x24/0x2a/0x7b`). `inicializar_dimensoes` provides exactly these four stores.

## Provider ([efeitos_logicos_exibicao.py](efeitos_logicos_exibicao.py))

| Function | Original | Effects | Stops (`DependenciaExibicao(rotina, sitio, motivo)`) |
|---|---|---|---|
| `restaurar_tudo(memoria)` | RestoreAll | `()` | below |
| `desenhar_jogo(memoria)` | AffGame (mode 0x12) | `()` | below |
| `inicializar_dimensoes(memoria, alta_resolucao=True)` | DDInit | four u16 stores | low-res path |

`memoria` needs `u8/u16/u32` reads (`MemoriaDeclarada` fits); the providers never write. Domain proved natively (guards read at every extent entry, listed in the evidence): `[0x4dfb44]`=0, viewport 25×17, view origin (4,6), structure pool states ⊆ {0,5}. Any other state raises a named stop: `0x43f191` (DDFlipPage shake path), `0x415b77/0x415c19` (vegetation/terrain handlers, `0x411147`, `0x412392`: guards not decoded, native proof only at (4,6)), `0x407dd3` (AffBatiments, state 3, 69 `0x4e1d18` sites). The stops are conservative supersets, not proofs those branches are reached.

## Validation

`test_efeitos_logicos_exibicao.py`: the evidence has no logic-reader of any display write; the provider accepts every captured entry guard and returns no writes; the three stop sites are exercised. The native differential is the capture itself: the enumerated write set of the intact code is empty for logic-read bytes. A full pre/post image diff per extent was not built.

## Open dependencies

- Other view origins, structures in state 3, vegetation guards, `[0x4dfb44]≠0`, other modes of AffGame and low-res DDInit: no native evidence, so they stop.
- Frame 1's `AffGame` is not entered inside the three phases (only the between-frames one), so a second frame is not covered.
- `MenuInit` (writes `0x4e1d18`, `0x508f72/73` in (a)) is outside this task's routines.

# Round 5

## Mask check against `m2-politica-comparacao-quadro1.json`

- The 33 DGROUP bytes of round 4: 19 of them are `display_only` in the mask (fps text `0x496394..96/0x4963b5`, clip words `0x49a02e/2f/32/33`, `0x49a042..45`, `0x49a04e`, ticks `0x4e17b0..b2/b4..b6`). The other 14 are not in the phase-diff set (net unchanged at every phase boundary), so the mask neither excludes nor needs them.
- **`0x4e17a4..ab` (DD lock state): not covered by the mask and not compared as a difference.** DDLockSurface writes the pointer `0x4e17a4..a7` and count `0x4e17a8` (1); DDUnlockSurface restores 0. They are equal at every phase boundary. AI's `0x4e17a6..a8` are inside this set; they are non-zero only between MenuInit's Lock and Unlock inside one phase.
- One disagreement to check on Missions' side: the mask has the clip words `0x49a01e/1f/22/23` as `game_logic`. RestoreAll/AffGame leave them unchanged inside their extents; their writers are SetClipping/RestaureClipping from callers outside those two routines (MenuInit among them), consistent with `game_logic` under the policy's writer rule.

## MenuInit's display calls in (a) ([chamadas-menuinit-exibicao.json](evidencias/chamadas-menuinit-exibicao.json), [script](capturar_chamadas_menuinit_exibicao.py))

Native, original only; the three phase states reproduce. In `load_tail` MenuInit calls, in order (caller offsets in the evidence): DDLockSurface, DeleteBank, FilledBox, DDUnlockSurface, DDFlipPage(1).

| Call | DGROUP effect | Other | Provider |
|---|---|---|---|
| DDLockSurface | `0x4e17a4..a7`=surface pointer, `0x4e17a8`=1 (unchanged across the phase) | none; EAX = pointer | `ddlocksurface(memoria, ponteiro_superficie)`: count must be 0 |
| DeleteBank (bank `0x47ac6000`, 72 entries) | none | 146 MemFree = 72 × (sub-block + entry) + table + bank, matching the policy's 146 `freed_blocks`; count word zeroed (2 heap bytes) | `deletebank(memoria, banco)` returns the exact free order and the count store; the native `GlobalHandle` sequence equals the walk |
| FilledBox | none | 455,972 surface pixels only | `filledbox(memoria)`: no effect; EAX is a leftover register, not modelled |
| DDUnlockSurface | pointer and count back to 0 | none; EAX = 1 | `ddunlocksurface(memoria)`: count must be 1 |
| DDFlipPage(1) | none while `[0x4dfb44]`=0 | two BltFast | `ddflippage(memoria)`: EAX = 0; `[0x4dfb44]≠0` stops |

Writes by MouseSetZone, MenuInit's own stores (`0x4e1d18`, `0x4e2f78`, ...) belong to MenuInit and its other callees, not to these five calls.

## Domain extension from isolated captures ([dominio-exibicao-isolado.json](evidencias/dominio-exibicao-isolado.json), [dominio-exibicao-visivel.json](evidencias/dominio-exibicao-visivel.json), [script](capturar_dominio_exibicao_isolado.py))

At the real entry of RestoreAll (load tail) and AffGame (between frames) the saved state is perturbed, the intact routine runs natively to its return, and the exact state is restored. RestoreAll keeps its declared LoadPie skip; its LoadPie effects stay an open dependency.

- **View origin:** 103 origins (a 7×7 grid plus a 9×6 grid, map 64×64 per `[0x497168]`) for both routines: no DGROUP or CRT byte outside the display set changes; only display caches (bank bitmaps, GetNumBob cache) and the palette block change. `ORIGENS_PROVADAS` is exactly this set; other origins still stop (sampling, not a proof of every origin).
- **Vegetation:** AffVeget runs at these origins; the cursor `0x4e1d18` never changes.
- **Later frames:** three consecutive AffGame calls on one logic state: no logic-state write in any. The logic between frames is not simulated, so this covers AffGame's own state only.
- **`[0x4dfb44]=1`:** AffGame advances the cursor by 1 (4→5) and decrements `0x4dfb44`; RestoreAll advances the cursor by 2 (0→2). Recorded, not modelled: it stops.
- **Structures in state 3: not proved.** Setting the Santuário's state byte (record 0, cell (12, 11) in the record) to 1..7 at 4 visible-origin candidates and then 54 origins never reaches the AffBatiments state read (`0x40816b` hook: 0 hits in every case), and the results are identical for every state. The perturbation was therefore vacuous; the state-{0,5} guard and the `0x407dd3` stop stay.

## Open dependencies
- Structure state 3 (and 1/2/4/6/7), which needs a captured state where AffBatiments actually reads the state.
- DDFlipPage shake path; LoadPie inside RestoreAll; nested locks; low-resolution DDInit.
