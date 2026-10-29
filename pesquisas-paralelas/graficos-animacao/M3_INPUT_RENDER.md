# M3 input-time display: native evidence

The original-only capture `evidencias/captura-entrada-m3.json` contains 71 complete AffGame draws, captured before
translation. Its original executable identity is SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
The paired `entrada-m3-proveniencia.json` pins its hash, case names and original byte intervals.

`capturar_entrada_m3.py` uses Core's `percurso_quadro1._bancada('exibicao')` and `Isolamento` at the first
`ProcessInputGame` entry of frame 1, exactly the pause described in `docs/core/SELECTION_ORDERS.md`.
Every case restores CPU, DGROUP, active allocations, native stack, DirectDraw metadata and all surface memory.
Native `EnginAddSelection`, `BatimentSelection` and `CalculIconeAction` create the selected states and action records.
The case explicitly declares any additional writes. AffGame then executes natively to `0x417D30`, before unlocking.
Recording hooks observe blitter and Box/FilledBox arguments; none replaces a game routine. The accepted display
bench's existing Windows/DirectDraw bindings and sound boundaries remain in effect. This is leaf-call evidence,
not a WndProc/scripted-input capture and not milestone acceptance.

Each case preserves the consumer's entry buffers, native terrain cache, complete before/after indexed surfaces,
ordered drawing arguments and exit DGROUP. Shared compressed blobs are addressed by full SHA-256. Banks remain
read-only original inputs, not embedded media. The grayscale lookup buffer at `[0x4E24BC]` is included explicitly.

The matrix covers the baseline; native selection and hover of units 0/11/12/13/15; selection modes 1/2/3; builder
experience levels 1–7 and blink frames; builder action selection 0/2/8/9; all four cost-counter branches; three drag
rectangles including reversed and clipped coordinates; target parity and final marker; the second cursor at 1/4/16;
native sanctuary selection; health percentages 0/1/35/36/75/76/99/100; selected-builder cave costs; numeric action
values 0/7/10/99/100/999; disabled-icon percentages 0/1/50/99/100; both scroll buttons; cost values through 9999.

The final native run took 173.655 s through the MacBook heavy lease. All 71 calls reached the drawing endpoint.
After restoration the accepted load-tail, between-frame and frame-1 summaries all reproduce, and code is unchanged.
An initial 38-case smoke run took 129.439 s. An expanded attempt was interrupted during startup to add the grayscale
buffer to the recorded inputs; it supplies no result. No translated renderer was imported by the evidence producer.
