# M2.2 — 128-frame equality proof (AI/runtime)

Main `c7ed947`. Proof file: [validacao/m2-2-prova-128-quadros.json](validacao/m2-2-prova-128-quadros.json), produced by [provar_quadros_ia.py](provar_quadros_ia.py) from clean revision `8beb95a`. Python only; the native side is Missions' committed capture. Intact `RISING.EXE` `6c556520…43fb`. M2.2 acceptance is the coordinator's decision.

## Reference and policy

| Input | File | SHA-256 |
|---|---|---|
| Capture (xz) | `pesquisas-paralelas/missoes/evidencias/captura-quadros128-monde01-exibicao-v2.json.xz` | `4c8f5c14…9ff3` |
| Capture, raw JSON (pinned) | — | `1ad031b9…d930` |
| Policy | `pesquisas-paralelas/missoes/validacao/m2-2-politica-comparacao-128-quadros.json` (cumulative mask: 4,948 ranges, 153,060 display-only bytes; 999 logic bytes) | in the proof file |

**Capture checks before the comparison:**
- the capture's `state_s0` equals the `-v2` MissionLoad final state;
- all 257 phases replay from it, and every phase summary matches;
- the full states at frames 1, 31, 32, 45, 50–52, 64, 100, 101 and 128 equal the replay.

## Result: equal in all 257 phases, with zero crossings

One map, built from the `-v2` MissionLoad final state, is carried through load_tail and frames 1–128.

| Check (every phase) | Result |
|---|---|
| Compared state bytes (outside the cumulative mask) | **16,022,275 equal** in every phase |
| RNGs `0x497164`/`0x498db4` | equal |
| Bindings outside display context | equal |
| Boundaries outside display context | equal |
| Allocation-record count | 25,482, equal |
| Between-frames exit registers (8) and the registers carried into each frame | equal |
| HUD flag `0x4e05a2` (compared; modeled by `affgame_hud_ia`) | 128/128 equal |
| Final allocation records | 25,482 equal |

**Crossings: 0. Crossings writing compared bytes: 0.**

## Compared bytes with a display writer

The policy compares five bytes that display code also writes:

| Bytes | Writers | How Python matches them |
|---|---|---|
| `0x4e05a2` | AffGame `+0x7f2`/`+0x81c` (display), CalculMatiere `+0x12c` (logic) | AffGame's store modeled from the code; CalculMatiere is Economy's provider |
| `0x49a01e/1f`, `0x49a022/23` (clip words) | RestaureClipping (display), SetClipping (logic) | RestaureClipping writes back what SaveClipping saved, and SetClipping is Core's provider; equal at every phase end |

## Display context

**Static issuer classification:** display-context events are identified by issuer (`contexto_exibicao_ia`), which reproduces M2.1's native counts.

**Not modeled:**
- 19 bindings and the 2 RestoreAll LoadPie boundaries in load_tail;
- 6–8 bindings per between-frames phase: display ticks and the DirectDraw calls, plus palette updates when Cyclage runs;
- 0 in the frame phases.

**Shared issuers:** in load_tail, 587 MenuInit/MemFree events were matched in order against Python's events. None was left unmatched in any phase.

## Unmodeled, stated explicitly

- The MCICD_Play stack words in the frame bodies (uninitialized caller locals).
- EFLAGS and EIP.
- Bindings and boundaries issued inside policy display roots (counted per phase in `phase_table`).
- Masked display-only state and the surfaces. The policy proves that no logic code accesses the surfaces.
- ProgIteration's saved words (0, 0, 0) and the MSG buffer: declared, and checked through the exit registers.
- Allocation-record call-site metadata.
- CalculGame's return EAX, which AffGame overwrites before any use.

## Note on `alloc24329` (`0x474a7000`)

It is the terrain bob-cache index. Its pointer is `[0x49a050]`, its entry count `[0x495bc4]`, and its counter `0x49a04e`.
- **Writers in this window:** GetNumBob only, through AffTerrain inside AffGame.
- **Logic writer outside it:** InitCache (CalculGame `+0x987`, MenuNewSelect) zeroes the index, but it is never entered in frames 0–128.
- **Result:** the 128-frame policy masks the block as display-only.
- **Later windows:** if a longer window reaches InitCache, these bytes become mixed and need a display-effect provider for GetNumBob.
