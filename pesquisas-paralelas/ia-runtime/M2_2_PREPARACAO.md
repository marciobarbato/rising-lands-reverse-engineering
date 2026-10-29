# M2.2 preparation — N-frame composition (AI/runtime)

Branch `feat/re-ai-runtime`, merged main `5c0dac2`. **Preparation only:** no native run beyond frame 1 was made on this machine. The Mac mini's per-frame captures and the cumulative 128-frame mask have not landed yet, so the formal per-frame comparison has not run.

## What is ready

| Piece | File | Status |
|---|---|---|
| N-frame chain: load_tail, then between_frames(k)/frame(k), on one map, mode `prova`, zero crossings | [composicao_quadros_ia.py](composicao_quadros_ia.py) | runs 128 frames in about 2 s, plus 20 s to build the map |
| AffGame's HUD flag `0x4e05a2` and its leftover EAX | [affgame_hud_ia.py](affgame_hud_ia.py) | translated from the code; checked against Core's native survey (below) |
| EnginNextEtape 32-frame target scan (`0x4546aa..0x4547e0`) | [proxima_etapa_quadro.py](proxima_etapa_quadro.py) | translated; first reached at frame 17 |
| UpdateChamp tile-grid read (ScanNouvellePatate) | [composicao_encadeada_ia.py](composicao_encadeada_ia.py) | per-call immutable bytes snapshot of Core's u16 list; first reached at frame 45 |
| Per-frame comparator against the Mac mini capture and the cumulative mask | [comparar_quadros_ia.py](comparar_quadros_ia.py) | self-test on the committed frame-1 `-v2` data reproduces the M2.1 proof |
| Static display context of reference events | [contexto_exibicao_ia.py](contexto_exibicao_ia.py) | reproduces M2.1's natively tracked counts: 19/2 in (a), 8 in (b), 0 in (c) |
| Coverage probe against Core's survey | [percorrer_quadros_ia.py](percorrer_quadros_ia.py) | below |

## Registers and frame words across frames

- **between_frames(k), k ≥ 2:** starts from frame(k−1)'s entry registers. ESP gets +4 (CalculGame preserves EBX..EBP). Its leftover EAX is overwritten by AffGame's before any event.
- **ProgIteration's saved (EDX, ECX, EBX):** declared (0, 0, 0) for frame 1, as in M2.1 and the capture's `caller_registers`. For k ≥ 2 they are the values the previous between-frames phase pushed. Bindings write EAX only, and the boundaries are skipped, so they stay (0, 0, 0).
- **Comparator checks:** the 8 exit registers of every between-frames phase, and the carried entry registers for k ≥ 2.

## AffGame and the HUD flag `0x4e05a2`

From the mode-0x12 body, with no event in progress:
1. If the flag is 0 and `counter mod [0x497284] ≠ 0`, AffGame returns at `+0x28d`. It stores nothing, and EAX is the quotient.
2. Otherwise it draws. `+0x7f2` stores 0. When `counter mod 5 = 0`, `+0x815` calls Cyclage, which keeps CL = 1, and `+0x81c` stores 1. The `+0x3ef` store is always overwritten.
3. EAX = `DD_OK` after Cyclage, or `counter div 5` otherwise, with AL replaced by `[0x4e1b0e]`. That EAX is the PlaySnd_Manage/MCICD_Manage boundary EAX.

Named stops: mode ≠ 0x12, an event in progress, divisor 0, `[0x508f92]` set, the marker animation (`[0x496204]` ≠ 0xffff), and no palette object.

**Missions vs Graphics:** AffGame does change the flag. It is 0 after between_frames(k) unless the AffGame counter k−1 is a multiple of 5. In frame 1 the net change is zero (0 then 1, at counter 0), which is what Graphics observed. In frame 2 it becomes 0, which is what Missions observed.

**Native check (Core's survey, frames 2–128):** in 127 of 127 between-frames phases, Cyclage is entered exactly when the model stores 1 (counters 5, 10, 15, …). AffTerrain is entered every time, because the body is drawn (divisor 1). Frame 1 has no survey entries. The per-frame comparator also tables the flag against the capture.

## Coverage probe (Python only, against Core's native 0–128 survey)

`percorrer_quadros_ia.py --quadros 128`, output under `.local/` (not evidence).

| Run | Result |
|---|---|
| Strict | frame 1 equal; **first stop at between_frames2**: Graphics' `desenhar_jogo` guard `0x415b77`, view origin (3, 5) not in the proved set |
| Planning (`--planejamento`: Graphics stops recorded, drawing taken as display-only) | **128/128 frames**. Counter, game frame, world RNG, AI RNG, CRT seed, cursor `0x4e1d18` and view origin equal the survey at every frame end. Per-frame call counts of the 20 checkpoint routines equal the survey. 127/127 HUD checks agree. The only stops are Graphics' guard, at origins (3,5), (2,4), (1,3), (0,2) and (0,1); the view then stays at (0,0) |

The cursor `0x4e1d18` agrees at every frame, so the original's AffGame did not advance it at those five origins. That is empirical support for Graphics' extension, not a proof.

## Provider requests (through the coordinator)

| Owner | Needed for M2.2 |
|---|---|
| **Graphics** | Extend `efeitos_logicos_exibicao.desenhar_jogo`'s proved domain to view origins (3,5), (2,4), (1,3), (0,2) and (0,1), in mode 0x12 with the 25×17 viewport. It is the only blocker in the 128 frames. |
| Core, Economy, Combat | Nothing for frames 1–128. |
| Economy/Core (FYI) | UpdateChamp now reads the tile grid through a per-call immutable snapshot. A shared u16-list accessor in `RecursosTerreno` would remove the copy. |
| Combat (M2.3) | `SetAttaqueEngin` (EnginNextEtape scan hit, state 7). |
| AI/runtime (M2.3, mine) | `iagUnitSendMessage` (scan hit, player type 2). |

## Contract for the Mac mini capture

`comparar_quadros_ia.py --captura <file[.xz]> --sha256 <raw JSON hash> --politica <N-frame report> --saida …`. It reads the xz file and checks the pinned hash of the raw JSON.

**Top level**, as in `captura-quadro1-monde01-exibicao-v2.json`:
- `state_s0` with `summary.sha256` equal to the `-v2` MissionLoad final state;
- `named_inputs`;
- `phases`, named `load_tail, between_frames, frame1, between_frames2, frame2, …`;
- the final `allocations` list.

**Per phase:** `entry`/`exit` (`registers`, `rng`, `allocations` count), `bindings` and `boundaries`. The state comes in one of two forms.

| Form | Fields |
|---|---|
| `-v2` | `state_after.blocks_changed_since_previous` and `state_after.block_hashes` |
| M2.2 delta | `state_delta`, against the previous phase's state |

The M2.2 delta form, applied in this order:

| Field | Content |
|---|---|
| `state_delta.released` | `[block name, …]` |
| `state_delta.allocated` | `{name: {base, zlib_base64}}` |
| `state_delta.ranges` | `[{address, zlib_base64 or hex}]`, each range inside one live block |
| `state_after.summary` | `{blocks, bytes, sha256}`, computed like Missions' `resumo_imagem`: SHA-256 over the name-sorted blocks, each as `<II base, size>` then its bytes, `native_stack` excluded. Required for every delta phase |
| `state_after.full_state` | `{name: {base, zlib_base64}}`, at the checkpoint frames only. It must equal the replayed state exactly |

**Failures:** a replay, summary or checkpoint mismatch stops the run as `capture_integrity_failure_<phase>` before Python is compared. Each phase in the report records `reference_integrity`.

**Self-test:** the committed `-v2` capture was converted to the delta form, xz-compressed and given a pinned raw hash. It has 3,059/18/359 ranges, 146 releases in load_tail, and a full state at frame1. Both forms reproduce the M2.1 proof: 16,097,242 compared bytes per phase, 597/2/13 bindings, 25,482 records, every summary replayed, and the frame1 checkpoint equal. A wrong pinned hash is refused.

**Policy:** the `politica_comparacao_quadros.py --quadros N` report; only its cumulative mask is used. Display context is derived statically. When display roots and logic share an issuer (MenuInit, MemFree), the comparator matches it in order against Python's events and reports it as a difference if it stays unmatched. A per-event context field in the capture would make this exact.

## Not done

- The formal per-frame comparison: it waits for the captures and the mask.
- Locating the writer of a divergent byte: it needs a native watch rerun, on the Mac mini.
- The display-context bindings and boundaries, EFLAGS/EIP, and the MCICD_Play stale-local stack words are not modelled, as in M2.1.
