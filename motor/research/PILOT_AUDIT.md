# Native engine pilot audit

Baseline: a7427fd0e416d212f08af7f0df3d36a224d12f2d (fetched main).
Only motor/ and docs/ENGINE.md are owned by this workstream.

The intact original is SHA-256
6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb.
No emulation is necessary or performed for this pilot. Existing committed
original-only captures are the oracle; original media is read-only.

| Capture | Selected routines | Calls |
| --- | --- | ---: |
| evidencias/fundacoes-quadro/captura-chamadas-quadro1.json | Random | 16 |
| evidencias/fundacoes-quadro/captura-exibicao-quadro1.json | Random / LongRand / rand | 8 / 12 / 12 |
| pesquisas-paralelas/economia/evidencias/captura-consultas-economia-exibicao-v2.json | IntToBCD / BCDToInt | 19 / 8 |

These are 75 captured call records. LongRand and rand include nested records
of the same original invocation, so counts are not 75 independent invocations.
References are chamadas_quadro_core (aleatorio_mundo_memoria and
aleatorio_crt_memoria) and provedores_economia_quadro (IntToBCD/BCDToInt).
The harness will import these unchanged from this clone, never another checkout.

World RNG uses unsigned division with explicit wrapping intermediate arithmetic.
CRT RNG accepts the proved single-thread getter only, preserving the original
(thread pointer +12) wrapping/null behavior. Unsupported getters are named stops.
BCD is four unpacked bytes, units first; the thousands byte is not clamped to9.
BCDToInt must preserve destination/source overlap: zero the word first, then
read each source digit against the updated value. Captures include caller-stack
changes and unchanged written bytes; do not zero-fill their unobserved neighbors.

Python's BCD providers model memory and return None, not scratch GPR values.
The static original review bcd-register-review.asm establishes their separate
register adapter: IntToBCD clobbers EAX=0, EDX=1; BCDToInt preserves EAX and
sets EDX=10000. Other seven data GPRs are preserved. All these values will be
checked against every captured return. EIP/ESP/flags are not a semantic C ABI;
this pilot does not execute x86 call/return or claim to model flags.
The review used Capstone5.0.7 over hash-verified original bytes, through Core's
unchanged PE interval reader; it executed no original instructions.

The state will have semantic RNG/value types, not a native packed-memory world.
A checked sparse projection retains uninterpreted declared bytes and binds the
few modeled fields explicitly. Per-call BCD buffers are typed scratch values,
with aliasing handled in their load/project boundary. No projectile pool,
frame engine, rendering, assets, orders or live Swift integration is claimed.
The clock foundation uses integer tick arithmetic only. A configurable20Hz
pilot default is pacing policy, not an inferred historical MONDE01 fixed FPS;
Core's cadencia explicitly does not establish a fixed FPS.
