# M3.1 — whole-state proof of the input chain over P1 and P2 (AI/runtime)

Proof file: [validacao/m3-1-prova-p1-p2.json](validacao/m3-1-prova-p1-p2.json), produced by [provar_entrada_janelas_ia.py](provar_entrada_janelas_ia.py) from clean revision `21bbb37`. Python only; the native side is Missions' committed pass-2 window captures (`m3/sondas/P1`, `m3/sondas/P2`, main `01745da`). Intact `RISING.EXE` `6c556520…43fb`. Acceptance is the coordinator's decision.

## Reproduction

One command, on a clean tree (about 24 min wall on the MacBook under a busy heavy lease; 289 s and 364 s of compute):

```
python3 -B pesquisas-paralelas/ia-runtime/provar_entrada_janelas_ia.py tudo --janelas P1 P2 \
    --lease <path>/heavy_lease.py \
    --saida pesquisas-paralelas/ia-runtime/validacao/m3-1-prova-p1-p2.json
```

Step by step: `provar_entrada_janelas_ia.py janela P1` and `janela P2` (reports under `.local/m3-1/prova-<revision>/`), then `agregar --janelas P1 P2 --saida <proof.json>`. `agregar` accepts only reports from the current clean revision, equal over the whole window, with zero crossings and no M3.1 field byte under the mask.

Phase chains to match on a second machine (`phase_chain_sha256`, the M2.3 definition: each phase's Python compared summary, both RNGs and the allocation count):

| Window | Frames | Phases | Chain |
|---|---|---|---|
| P1 (selection) | 129–629 | 1,002 | `7220a6312b573670eb3206d8ba11771ac24c4ca0238bd8c3e832f53a4e7fe2e6` |
| P2 (selection + move) | 129–729 | 1,202 | `208aef46776a260bca0bbf0cd25bce5f675ad9a895129b0f77e4a054a85e0fbb` |

## Method

The M2.3 method, imported unchanged (`comparar_quadros_ia.comparar_sequencia`, `fases_referencia`, `MascaraEnderecos`, `ContextoExibicao`):
- **Reference.** The window manifest (SHA-256 pinned in the script) pins the part's xz and raw JSON and the mask; the mask file pins the window policy (display roots); the part pins the scripted-input file. Every phase is replayed from its complete deltas and checked against its summary, compared summary and masked hash (1,002/1,002 and 1,202/1,202), plus the full states at frames 250, 500 and the last frame.
- **Start.** The opening full state matches its own hashes and equals the accepted M2.2 frame-128 full state. Declared inputs: the frame-128 allocation records (no phase allocates or releases; the count stays 25,482) and the between_frames129 entry registers.
- **Chain.** `ComposicaoEntrada` (the pinned M2.2/M2.3 composition plus this front's WndProc, InputGame, SetPlayerOrdre, ProcessInputGame and CalculIconeAction, with Core's selection/order setters and Economy's queries) fed the probe's input file through the original poll sites. Mode 'prova': no crossing data, so any crossing would stop the run.
- **Mask.** The window's `cumulative.exclusion_mask`: the published M2.3 mask plus the display-only bytes proven in the window (P1 155,587 bytes in 4,950 ranges; P2 160,721 in 5,115). No game-logic conflict was removed.

## Result: every phase equal, zero crossings

| Check (every phase) | P1 | P2 |
|---|---|---|
| Compared state bytes (outside the mask) | 16,019,748 equal per phase | 16,014,614 equal per phase |
| Python compared summary = the reference's | 1,002/1,002 | 1,202/1,202 |
| RNGs `0x497164`/`0x498db4` | 1,002/1,002 | 1,202/1,202 |
| Bindings / boundaries outside display context | 1,002/1,002 (8,023 / 1,511 events) | 1,202/1,202 (9,635 / 1,818) |
| Allocation count | 1,002/1,002 | 1,202/1,202 |
| Between-frames exit registers; carried entry registers | 501/501; 500/500 | 601/601; 600/600 |
| HUD flag `0x4e05a2` | 501/501 | 601/601 |
| Consumed scripted inputs (peek/get/translate/dispatch, cursor, keys) and WndProc flag bytes | 1,002/1,002 | 1,202/1,202 |
| SetPlayerOrdre packets and ProcessInputGame dispatches (`comandos.jsonl`) | 501/501 frame phases | 601/601 |
| M3.1 fields (below) | 1,002/1,002 | 1,202/1,202 |

**Crossings: 0; crossings writing compared bytes: 0; Core provider stops: 0.**

Orders reproduced: P1 tag 1 (select unit 12) at frame 133; P2 tag 1 at 133 and tag 5 (move) at 143, each SetPlayerOrdre packet and its ProcessInputGame dispatch (jump target from table `0x45ed20`).

**M3.1 fields**, compared explicitly at every phase end and not masked anywhere (0 of their bytes are in the mask):
- each player's packet pointer `[0x4e2458+4p]` and its 10-byte packet, p = 0..3;
- the per-player selection areas `0x508728+512p` (512 bytes each), p = 0..3;
- the order fields `+2`, `+0xb2`, `+0xb7`, `+0xb8`, `+0xbe`, `+0x110` of all 800 unit slots of the pool `[0x4e19a0]`.

## Chain changes made for this proof (commit `21bbb37`)

The first runs of the comparator found three differences, all in what the chain recorded, none in state:
- the input chain did not log `USER32.GetAsyncKeyState` as the original's import binding (12 polls per frame phase); it now does, with the poll's return address and the declared answer;
- `PeekMessageA` (PM_NOREMOVE) fills the MSG with the head message as `GetMessageA` does; the binding now records that write;
- the PlaySnd_PostSound boundary raised from Core's EnginAsk now carries its call site (`EnginAsk+0x8e`), the pushed volume word (the three stale caller words after it are not modeled, as for MCICD_Play) and the `ret 4` cleanup. Core's `som(nome, regs, pilha)` API passes no call site, so it is read from Core's own declared `_fronteira(nome, endereco, ...)` argument. Requested from Core: pass the call address to `som`.

## Not compared, stated explicitly

- **`top_callee` of boundaries.** The window harness (`entrada_roteirizada`) records `null` on every boundary of both windows (the M2.3 oracle recorded the issuing top-level callee). It is not compared; Python's values are counted in each report (`boundary_top_callee`). Every other boundary field is compared. Owner of the field: Missions.
- **WndProc flag bytes.** The window parts do not carry them; they are compared against the probe's committed `entradas.jsonl` (pass 1, same input, replay-equal).
- As in M2.3: the MCICD_Play stack words in the frame bodies, EFLAGS and EIP; bindings and boundaries inside policy display roots (counted per phase); the masked display-only state and the surfaces; allocation-record call-site metadata.
- TextGetMessage stays Missions' declared display-scenario boundary; neither window reaches it.

The proof file holds per-window equality counts, the run-length phase table, the full records of the order frames and their neighbours, the code SHA-256 of every imported source file, and the evidence SHA-256 (manifests, parts, masks, policies, inputs, command logs, the M2.2 capture, EXE and SBL).
