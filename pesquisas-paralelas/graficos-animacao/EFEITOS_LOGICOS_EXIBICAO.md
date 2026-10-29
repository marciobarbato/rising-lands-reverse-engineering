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
