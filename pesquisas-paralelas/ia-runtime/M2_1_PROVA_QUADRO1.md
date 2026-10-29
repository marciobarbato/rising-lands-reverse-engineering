# M2.1 — first-frame equality proof (AI/runtime, round 5)

Main `d94a59e`. Proof file: [validacao/m2-1-prova-quadro1.json](validacao/m2-1-prova-quadro1.json), produced by [provar_quadro1_ia.py](provar_quadro1_ia.py) from a clean tree with a fresh native run under the heavy lease. Intact `RISING.EXE` `6c556520…43fb`. M2 acceptance is the coordinator's decision.

## Reference and policy

The SHA-256 of each file is in the proof file and checked by `testes/test_prova_quadro1.py`.

| Input | File |
|---|---|
| MissionLoad entry | `pesquisas-paralelas/missoes/evidencias/entrada-carga-missao-exibicao-v2.json` |
| MissionLoad reference | `…/captura-carga-missao-exibicao-v2.json` |
| Frames 0/1 reference (Graphics backend) | `…/captura-quadro1-monde01-exibicao-v2.json` |
| Entry trace | `…/rastro-quadro1-monde01-exibicao-v2.json` |
| Policy | `pesquisas-paralelas/missoes/validacao/m2-politica-comparacao-quadro1.json` (8,780 mask ranges, 78,093 display-only bytes) |

The script refuses to run if the policy's reference SHAs differ from the committed -v2 files.

## Result: equal in every phase, with zero crossings

One map is built from the -v2 MissionLoad final state and chained (a)→(b)→(c) in Python.

| Phase | Compared state bytes (25,197 blocks) | RNG `0x497164` / `0x498db4` | Bindings | Boundaries | Allocation records | Registers | Checkpoints |
|---|---|---|---|---|---|---|---|
| (a) load_tail | **16,097,242 equal** | equal | 597/597 equal | 3/3 equal | 25,482 equal (146 freed in Python) | — | 48/48 |
| (b) between_frames | equal | equal | 2/2 equal | 2/2 equal | equal | 8/8 equal | 1/1 |
| (c) frame1 | equal | `0x78fe3b37` equal | 13/13 equal | 1/1 equal | equal | — | 38/38 |

"Compared" means every byte of every reference state block outside the policy's `exclusion_mask`. The surfaces lie outside the state.

**Crossings: 0. Crossings writing compared bytes: 0.**

| Routine | Python provider |
|---|---|
| NextAnimTerrain/NextAnimVeget | Core's 25×17 providers |
| RestoreAll/AffGame | Graphics' `efeitos_logicos_exibicao` (guards checked; no logic write) |
| DeleteBank → MemFree | this front's `bancos_quadro_ia` on Missions' `ArenaComposicaoM1`: the 146 bank records (`alloc lock handle unlock handle free`, freed SHA-256) and 584 GlobalHandle/GlobalUnlock/GlobalFree bindings |
| SetClipping, InitGameZone, the task VM and the other leaves | Core, Economy, Combat and Missions providers, as in round 4 |

## Display roots not executed by Python (MenuInit), with proof

These are policy display roots. Python does not execute them. The native write set of each top-level call is in the proof file:

| Call (phase a) | Bytes written natively | Proof |
|---|---|---|
| DDLockSurface (MenuInit `0x46837a`) | `0x4e17a5..a8` (lock bookkeeping) | compared bytes, **restored by DDUnlockSurface before the phase ends** (first value = phase-end value). Graphics' evidence: only DDLockSurface/DDUnlockSurface read them. EAX = the offscreen pixels `0x60076000`, a declared input from the reference backend state; MenuInit stores it at `0x508f70` (same value) |
| FilledBox (`0x468400`) | none in the state (surface pixels only) | outside the compared state |
| DDUnlockSurface (`0x468c91`) | `0x4e17a5..a8` back to their values | restored (above) |
| DDFlipPage (`0x468ca2`) | none in the state | outside the compared state |
| RestoreAll (`0x42d27f`) | 78,050 bytes, all masked | inside the mask |
| AffGame (`0x475063`, phase b) | 43 bytes, all masked | inside the mask |

## Round-4 classification versus the policy

| Routine | Round 4 | Policy | Agreement |
|---|---|---|---|
| RestoreAll, AffGame | display | display-only (masked) | yes |
| FilledBox, DDFlipPage | display | no state write | yes |
| NextAnimTerrain (CRT seed), NextAnimVeget (`0x4e1d18`) | logic | compared | yes |
| **DDLockSurface/DDUnlockSurface** `0x4e17a6..a8` | display | **compared** (no net change at the phase ends, so not in the mask) | **no**. The proof shows the bytes restored, and Python leaves them untouched, so the end states are equal |
| **DeleteBank** | display (bank memory) | its 146 freed allocation records are **compared** (coordinator decision) | **no**. Now modeled exactly (above) |

## Unmodeled, stated explicitly

- The four stack words of MCICD_Play in the two CalculGame frame bodies (uninitialized caller locals).
- EFLAGS and EIP.
- Bindings and boundaries issued inside policy display roots: DirectDraw COM calls, display ticks and palette entries, and LoadPie inside RestoreAll. Graphics' provider produces none of them. Counts: 19 bindings and 2 boundaries in (a), 8 bindings in (b), 0 in (c).
- Masked display-only state and the surfaces.
- Phase (b)'s ProgIteration frame words (saved EDX/ECX/EBX = 0, as the boundary registers show) and the MSG buffer `[0x3000000, 0, 0, 0]` (bench loop frame), which are declared.
- The allocation-record metadata `caller_return`, `stack` and `freed_caller_return` (bench call-site metadata, excluded as in M1).

## Process note

During development, one trial rerun executed the native collection **outside the heavy lease**. A missing cache file triggered it; it ran briefly and crashed in my collector code, and no evidence came from it. Every run that produced evidence, including the committed proof, ran under the lease.
