# Scripted probe windows — render API 1.8 research

Source main is pinned to `ce441852bcada750a8f91da8ed3302f1668c4405`. The published 1.7 version is retained as history;
the coordinator confirmed that its dispatch version typo requires no renumbering. No main integration or acceptance
is authorized by this dispatch. Owned changes remain Graphics-only.

## Original-first case matrix

| Window | Required evidence | Native acquisition |
|---|---|---|
| P3 129–3129 | All construction stages, completion at 1812, finished uninhabited CAVE | Existing 129–300 evidence, then <=750-frame restored continuations |
| P6 2001–2400 | Sanctuary selection/release, colonist walk/order/lodging, inhabited CAVE from 2178 | Restore verified shared P3 frame-2000 state, run P6's original input |
| P7 2401–3700 | View movement, carrier work, Ctrl/depot order, delivery/credit at 3604 | Restore verified shared P6 frame-2400 state, run P7 in bounded chunks |
| K1 129–629 | Arrow-key scrolling and subsequent key states | Native input replay from accepted frame 128 |

Published whole-state hashes establish that P3/P6/P7 are identical at frame 2000, and P6/P7 at frame 2400. Every
restored opening checkpoint is checked against the destination probe, then both phase surfaces and the complete
end-frame state are checked at every frame. This is native continuation, not injection of reconstructed state.
The recorder has an 18-minute internal checkpoint budget; every native invocation uses the heavy lease.

`evidencias/janelas-api18-proveniencia.json` pins all four published probe directories and the intact-executable
intervals before translation. Executable SHA-256 is unchanged:
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
`capturar_janelas_graficas_m3.py` imports the pinned original-only capture helper and adds observation of
TextGetMessage entry and native accesses to `[0x5099A4..0x5099A7]`; it never reads that pointer to fabricate a message.

## Boundary contract

The display oracle declares TextGetMessage EAX 0, with its body not executed. A glyph path depending on an unavailable
pointer remains a named dependency. AffText is also a declared non-executed display boundary in the inherited bench;
the existing fixture-only adapter may verify that exact recorded boundary, never act as a default glyph renderer.
Actual observed boundary counts and pointer reads are recorded separately. The checked-in `fronteiras.jsonl.xz`
files at the pinned revision contain audio/CD boundary rows; no TextGetMessage row was found in P3/P6/P7/K1 during
initial inventory. This is recorded as an observation, not used to synthesize an unobserved text call.

## Portability

New sprite families, anchors, clock sources, masks and conditions will be expressed as explicit layer plans/tables.
The Python frame compositor consumes those plans; the engine workstream can port the data and arithmetic to the Rust
renderer without deriving IDs from image pixels or importing emulator code. Unsupported state remains an addressed stop.
