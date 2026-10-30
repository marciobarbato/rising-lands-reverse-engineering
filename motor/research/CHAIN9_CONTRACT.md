# Recruitment owner and S1 continuation contract

Original oracle: intact RISING.EXE SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
The five Core adapters were captured before their Python translation in
`evidencias/recrutamento-core/original.json.xz` (capture commit `8e5e2a5`).
New reference profile `chain9` initially selects logic `6cdbc5a` and Graphics
`92fab50`, independently of all earlier immutable profiles. Each transitive
source and fixture is checked against its Git object; explicit additional pins
include Core recruitment and Economy's actual BL/DX forwarding source.

## Native owner entries

These Rust fixture entries are selected by `chain_stage5::entry`, not new C ABI
functions or routine IDs. C ABI 1.6 and Graphics contract 1.9 are unchanged.

| Original entry | SortieTroupe call | Input widths | Changed outputs |
| --- | --- | --- | --- |
| EnginSetType 0x457b87 | 0x420f69 | AX unit, DX cell, BL direction, CL type | EAX capacity + live bonus, EBX=0x1d, ECX=record+10, EDX=0x1e |
| EnginAddVie 0x457122 | 0x420f75 | AX unit, DX increment | EAX maximum-life high byte + AL clamp flag; EDX record |
| EnginResetFatigue 0x4530fd | 0x420f7c | AX unit | EAX record |
| EnginSetExperimente 0x44fe42 | 0x420f85 | AX unit; DX continuation cell preserved | EAX owner*10 on empty/mismatch, owner*5 after consuming |
| SetSortEngin 0x445fbc | 0x420f8c | AX unit, DX cell | EAX rows and EDX scratch from final mode4 SetMiniMap |

Every other data GPR is preserved; fixture ESP advances by4. Production calls
reuse the same healing, fatigue, experience and placement bodies. Conversion
continues to use the native frame_spawn type/characteristic/capacity provider,
including live Economy bonus queries; no missing bonus becomes zero.
The direction is the actual BL preserved by CalculPosition. The exit cell is
carried through experience and consumed by placement, without reconstruction
from a default register tuple.

Unit indices are0..799, types0..25, owners0..4 or200; experience owners0..3.
The placement register entry protects in-map cells, loaded map dimensions1..256,
local player0..3 and128x128 minimap. Normal-owner BB+F5 vision sums above11 stop
at0x446146 after the preceding position/collision/visibility effects and before
sight discovery. No fallback success or widened radius domain is introduced.

Mutation/callback order remains the original provider order: conversion's cell
and search release, unit fields, characterization, live bonus and Bag reset;
healing's wrapped u16 sum store, live maximum read and conditional clamp;
fatigue +74 clear then +76→+04; experience AF store and F5–F8 effects before
queue shifts (experience byte before type byte, then tail0/255); placement's
+7e/+7c/+08/+7e, search release, active state7, orders and animation clear,
collision, visibility, discovery, illumination and mode4 minimap. SortieTroupe
then issues movement, local voice, habitation/abandonment, recruitment reset,
unit message and city message. Unsupported AI message handlers retain named
original-address stops. Fixture calls compare effects retained before a stop;
the public frame ABI retains its existing transactional publication semantics.

## S1 surface oracle

`motor/testes/s1_render_capture.py` runs only original x86 routines and the
pinned observer on the mini, from original checkpoints. Each segment is at most
750 frames, bounded to1,140 seconds after its shared lease grant. Every complete
frame must reproduce the previously committed original S1 whole-state hash and
both phase surface hashes before its raster/text attestation is retained.
Only hashes and original arguments are saved; no commercial asset bytes or
writable emulator database is shared. A late segment is evidence, never a new
Rust opening.

`motor/testes/s1_surface_proof.py` advances one Rust world from frame128. A
separate Graphics worker carries Rust pixels/cache/background from the same
original frame128 opening, verifies the original raster order and full surface
hash, and compares pinned Python pixels/cache/effects. AffText nonexecution
remains the exact recorded boundary: text, font, rectangle, flags and complete
pre-text surface hash must agree. No empty text callback is installed in the
production ABI, whose glyph stop remains unchanged. These qualified surfaces
are not proof of glyph reconstruction or production-default text completion.

## Validation and gaps

The owner reader reexecutes all277 committed original cases: three real Economy
producer entries, the five in-situ S1 frame2547 calls, and declared variants.
It compares every mapped input byte plus original changes and all seven data
GPRs/ESP, with no comparison masks, skips or invented memory. Native capture
reproduction is checked independently of native Rust equality. Stack writes
remain excluded by the original capture policy.

Measured reports, first stops, timings and prior exact regression scopes are
recorded in `motor/HANDOFF.md` as each bounded piece finishes. Neither this
contract nor a successful prefix establishes S1 victory, Test B, integration
acceptance, or a main merge. Those remain coordinator-owned decisions.
