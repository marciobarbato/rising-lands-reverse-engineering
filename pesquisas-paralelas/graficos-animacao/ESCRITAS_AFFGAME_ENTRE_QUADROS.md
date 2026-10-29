# Does AffGame write game state between frames? (M2 acceptance dependency)

Original-first evidence over the intact `RISING.EXE` (SHA-256 `6c556520…43fb`). No renderer was added. Frame bench inputs: the
accepted M1 capture `captura-carga-missao-original-v2.json` (SHA-256 `eb7d2303e13e62d4f5692c9cb6ef302b573d138df6a8b51183a6d9b0bd703afc`).

- Static: `fechamento_escritas_affgame.py` (capstone recursive descent of the intact image, no execution) →
  [evidencias/fechamento-escritas-affgame-modo12.json](evidencias/fechamento-escritas-affgame-modo12.json).
- Native: `capturar_escritas_m1.py` runs the existing `BancadaQuadro` (original AffGame x86, unchanged) over the M1 world under the heavy lease →
  [evidencias/captura-escritas-affgame-m1.json](evidencias/captura-escritas-affgame-m1.json).

## Scope of each method (read before trusting a verdict)

**Static closure.** AffGame dispatches on `[0x4e2f78]` (`0x4176a8..0x4176af`). The **mode 0x12** body starts at `0x4178f7`; closure = that body
(394 instructions, jump table `0x417b2a` resolved) plus all direct callees: **221 routines**. Other modes (`0x16` at `0x4178b3`, `0x13..0x15`, `0x0a`
at `0x417ed0`, …) are excluded: they are not the in-game path.
- 65 distinct absolute DGROUP store addresses. 207 stores go through a non-stack pointer; 19 of those carry a DGROUP displacement and none
  can reach the eight addresses except the `0x5099b4+16*i` table (below). The rest write surfaces/caches/stack and are not individually resolved.
- 910 unresolved indirect transfers: 806 blit-table calls `[eax*4+0x496cdc/0x496d04]`, 39 COM/register, 37 Windows IAT, 15 `0x4990cc..e4`
  hook tables (image values `0x48e7cc` `ret` stub and CRT jmp thunks), 13 other single pointers. The blit tables are zero in M1; the bench's own video/bank setup
  fills only entries 6 and 9 (`0x47cd76/0x47cebe`, `0x47cd5a/0x47cea2`). The closure of those four targets has **no absolute DGROUP store** (recorded in the capture).
  The other pointer cells (COM, IAT, `0x49932x`/`0x5233xx`) are display/OS entry points, not resolved by this closure.

**Native capture.** One AffGame call, M1 world buffers + structure pool `0x49a0c8` + M1 view origin (4,6) with the Santuário (cell 2828) in the 25×17 window,
declared: `[0x4e2f78]=0x12` (CalculGame sets it in the load-state frame, Missions QUADRO1), 800×600 geometry, tick 1500, the bench's DirectDraw IsLost/Lock fixture.
It runs **to the HUD checkpoint `0x417B1C`** (2,320,149 instructions: 425 terrain blocks, 726 AffBatiments/AffBatimentOmbre, 49 AffVeget, **16 AffEngin**).
Everything after the checkpoint (HUD, `0x417f38`, `0x416f29`, `0x41721f`, `0x46677d`, `0x469c44`, `0x4581bc`, the `0x43f14f` page loop and the tail stores
`0x417e0f..0x417ec7`) is **static only**: it needs fonts/bobs/DirectDraw state this bench does not provide (open dependency). The frame-0 state is M1 plus the declared
mode byte, **not** Missions' recorded post-(a) state.

## Guard values in the M1 state

`[0x4e2f78]=0` (0x12 after the load-state frame), `[0x4e1b0e]=0`, `[0x4e2e7c+cam0]=0`, `[0x507d54]=[0x507d56]=0`, `[0x4dfb44]=0`, `[0x4e05a2]=1`, `[0x4e1d18]=0`,
`[0x50a9b4]=1`, `[0x50a9b6]=8`, viewer 0, origin (4,6).

## Verdict per address (mode 0x12 path)

| Address | Verdict | Exact stores, path condition, value |
|---|---|---|
| `0x4e2f78` | **(b)** conditional | `0x417ec7 mov byte [0x4e2f78],0x16` at the tail: reached only after the draw-cadence gate (`0x417909..0x417925`) and when `[0x4e1b0e]≠0` (`call 0x4581b6; test al,al; je 0x417f2f` at `0x417eba..0x417ec1`). Value 0x16. Other stores are off-path: `0x4178e7` (=0x12) only for entry mode 0x16; `0x468c6d` is inside `0x4682bb`, called only from mode 0x0a (`0x417ee5`). With `[0x4e1b0e]=0` never written. Native: 0x12→0x12 to the checkpoint (the store is after it: static). |
| `0x4e1b0e` | **(b)** only clears | `0x45835f mov [0x4e1b0e],bl` with `bl=0` (`0x458358`) inside `0x4581bc` (called `0x417c8a` when the entry event flag `[ebp-4]` was set). Guard `cmp [0x4e1b0e],0; je ret` (`0x4581c5`) and counter `[0x4e1b0c] ≥ [obj+6]` (`0x458351`). With 0 the routine returns at `0x4581cc`. The same path also clears `[0x4e1b14]`, sets `[0x4e05a2]=1`, calls `0x469b85`. Never sets it non-zero. |
| `0x4e060c` / `0x4e0610` | **(b)** conditional | Only in `0x428ef1` (`0x428efe`: `[0x4e0610]=1`; `0x428f10`: `=[0x49620a]`; `0x428f2c`: `+1`; `0x428f33`: `[0x4e060c]=EAX`). Reachable only via `0x46677d` (`0x417c43`) → `0x465b8c` → `0x463abb` → `0x428ef1`: `0x46677d` returns at once unless `[0x4e2e7c+viewer]` ∈ {1..4} (`0x46678b..0x46689d`; state 3 → `0x465b8c`). `[0x4e2e7c]=0` in M1. Static only (past the checkpoint). |
| `0x507d54` | **(b)** conditional | `0x469b9f [0x507d54]=(old+1) mod 256` (also `[0x507d58]=0`, `0x469ba6`) in `0x469b85`, whose only caller in the path is `0x4581bc` at `0x458375` (event-end branch, needs `[0x4e1b0e]≠0` and counter ≥ `[obj+6]`). `0x469c44` (`0x417c8f`) only reads it. Static only. |
| `0x50a9b4` / `0x50a9b6` | **(b)**, idempotent with M1 | `0x479c9e` stores AX/DX; its only call site `0x471944` follows `mov edx,8 / mov eax,1`, so the values are the constants **1 and 8 = M1's values**. All four jump-table cases of `0x471830` reach it. Entries: `0x46677d` (state ≠0) and `0x469c44` (always called at `0x417c8f`; exits at `0x469c59` when `[0x507d56]==[0x507d54]`, true (0=0) in M1, or the message id is `0x18f`). Residual **(c)**: `0x479c50` writes `0x5099b4+16*idx`; immediate indices ≤27, but 6 call sites pass a non-immediate index (`0x464f9f`, `0x4650d8`, `0x471993`, `0x471ab1`, `0x471acf`, `0x471fea`); hitting `0x50a9b4` needs idx 0x100. |
| `0x4e1d18` | **(b)** state-dependent | Not a plain flag: the cursor into the permutation table `0x4e1c18` shared with game-logic Random (logic readers include `0x42d2f9`, `0x477533`). The display path advances it (`read table[c]; c+=1`): 69 sites in AffBatiments `0x407dd3` (e.g. `0x4081ac..0x4082a3`, structure mode `[rec+5]==3`), plus `0x411147`, `0x412390`, the AffVeget handler tail `0x415b77/0x415c19`, and `0x43f191` (`0x43f14f`, only if `[0x4dfb44]≠0`, called from the page loop `0x417d4d`). **Native over M1 (view origin (4,6), Santuário mode 5, 16 units): 0x00→0x00, no consumption** through the checkpoint. Any visible structure in mode 3, such vegetation, or `[0x4dfb44]≠0` would change the Random stream seen by logic: a divergence risk once those states occur. |

## Other game-state bytes the display path writes (found, not requested)

Absolute stores with an absolute read in game-logic routines (16 addresses in the JSON): `0x4e2f78`, `0x4e1b0e`, `0x4e060c/10`, `0x507d54`, `0x4e1d18` (above),
and `0x507d58` (`0x469ba6`, with `0x507d54`), `0x496ed4/ec/f04/f1c` (`0x465c27/0x465cbf`, market panel `0x465b8c`, same state-3 guard), `0x49a018/1a` (`0x417a0f..0x417a48`
mode switch under `[0x49a041]`; native wrote `0x49a02e/32/4e` clip bytes, not these), `0x49a054` (`0x417e0f=1`, `0x417e78=0`, per-frame from the cursor vs margin `[0x508f90]`; with margin 0 and cursor (0,0)
the `0x417e06` branch is not taken), `0x4e17a0`, `0x508f70` (surface pointer, display).
Display-only writes with no logic reader found: `0x4dfb44` (decrement at `0x43f1a0`, guarded by itself, M1 = 0), `0x4e05a2` (`0x417a87=1`, `0x417e8a=0`, `0x417eb4=1`), `0x4e05ac`.
Not individually path-resolved: `0x49a018/1a/54`, `0x4e17a0`, `0x496ed4..`.

**Native written bytes through the checkpoint (M1, 7 DGROUP runs):** `0x49a02e/0x49a032/0x49a04e` (clip), `0x4e17a7`, `0x4e17ae` (fps counter 7→8), `0x4e17b4` (tick), `0x508f73` (surface pointer byte).
None is game state; none of the eight addresses changed.

## What this proves, and what it does not

For the MONDE01 M1/frame-0 guard values above, the original AffGame write to any of the eight addresses is either guard-blocked ((b) with
`[0x4e1b0e]=0`, `[0x4e2e7c]=0`, equal message indices) or value-idempotent (`0x50a9b4/b6`), **except `0x4e1d18`**, whose writes depend on what is drawn:
natively unchanged for the M1 view, undecided for later views. Missions should check the guard values in **its own** frame-0/1 states and, if any differs, treat the matching row as written.
Not proven: the post-checkpoint code natively, Missions' recorded state, the 6 non-immediate `0x479c50` indices, pointer stores to surfaces/caches, and the 13 minor unresolved pointers.
Open dependencies for native post-checkpoint capture: fonts/bobs for HUD, the DirectDraw surface semantics beyond IsLost/Lock, message/event objects (`[0x4e1b10]`), sound/MCI.
