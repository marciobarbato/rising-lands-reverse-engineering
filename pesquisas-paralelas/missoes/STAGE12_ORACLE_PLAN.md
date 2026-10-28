# Stage12: whole-MissionLoad original oracle preparation

Status: **light scaffold only; no whole-load execution or Python composition**. Stage11 is integrated at main `7f617fab29ce382f96b690ea70da25a33fab8bae` (pushed feature `c0f0a873c3657e72a3e478cf6fd7ea73c84dd58a`, implementation `2f6d96b89039590c598f312752d4fe0e3c5b3607`, original captures `ed0172a364310b28584824b3e49dc63db371ed93`). All four commits are ancestors of fetched main. Its locked candidate passed80native tests, common local gates, then9focused native tests reproduced on main with unchanged counts/state/trace. The heavy lease was released; no prior work or evidence is replaced here.

## Scaffold and inherited-state closure

[estado_herdado_missao.py](estado_herdado_missao.py) defines `BlocoHerdadoMissao` and `EstadoHerdadoMissao`. The caller must supply every byte, address, source revision and provenance. There is no world/player/rule constructor or zero-fill fallback. Aliases are views into one declared backing block; overlapping independent blocks are rejected. The registry validates all known physical grids, units, live/stored80-byte players, projectiles, four2704-byte type Bags,800route buffers and complete585728-byte DGROUP+.bss.

The live player types and stored player types are recorded independently. No all-human/disabled-AI table is synthesized to avoid research branches. A complete original input source or an explicitly identified nontrivial inherited fixture must be assembled and reviewed; **the Stage11 hash-only captures do not supply missing raw bytes**. Engine state produced by earlier constructor defaults cannot silently fill gaps. The M1 schema/alias/provenance requirements remain in [M1_SNAPSHOT_CONTRACT.md](M1_SNAPSHOT_CONTRACT.md).

[bancada_mission_load_original.py](bancada_mission_load_original.py) defines a native scaffold on the committed Stage11/Core harness. It overwrites every game-state arena from the inherited registry before use and requires explicit additional arena pages and external handlers. The class is not instantiated by import and has not been run. All original executable-section intervals come from the intact PE's protected-code metadata, so reached engine bodies execute as original instructions rather than Python replacements. Original loop heads may resume through Core's existing preserved-stack/register mechanism. Unknown imports/unsupported state remain errors/stops, never successful no-ops.

Finite limits are mandatory: total wall time≤300seconds, segment count≤10000, binding count≤10000 and≤1000000instructions per segment. These are upper guards, **not an estimated runtime or evidence of completion**. Binding and segment exhaustion must retain/report the partial original frame and memory. A caller-specified checkpoint is distinct from the real return. Reported `m1_accepted` and `whole_load_python_composed` remain false.

## Explicit external boundaries

Core16's validated generic binding API is consumed from committed main `b4c5a1072a2b2e494b3a6bf374bd978fc6e67b9a`. No live sibling import, OS emulation or engine provider stub is introduced. `FronteirasExternasCargaMissao` requires eleven named handlers and their provenance; none has a default return.

| Boundary | Original ABI / fixture obligation |
|---|---|
| CRT `fopen 0x48c71f` | EAX=path, EDX=mode; explicit known-file mapping and nonzero stream identity or declared failure. Native FileOpen stores that stream at0x4e1d1c and computes AL |
| CRT `fread 0x48c97b` | EAX=destination, EDX=item size, EBX=item count, ECX=stream. Supply actual declared bytes/cursor, preserve typed writes and return actual item count. Never confuse byte count with item count or fabricate EOF success |
| CRT `fclose 0x48c80b` | EAX=stream, explicit result. Native FileClose performs its global clear; the external handler must not duplicate engine stores |
| Inventoried I/O wrapper `FileSeek 0x45848b` | EAX=offset, DL=origin; handler reads the actual stream at0x4e1d1c. Wrapper bytes only save EBX/ECX, reorder arguments and call CRT fseek0x48cda2; no global stores. This one wrapper is an explicitly declared external I/O boundary permitted by Core's FRONTEIRAS_IO; it must be disclosed in reports. A future owner-reviewed CRT fseek registration could retain this wrapper too |
| IAT `GlobalAlloc 0x5231c0` | two stdcall dwords flags,size; choose only an explicit finite planned allocation, with retained initial bytes and no automatic zero allocation |
| IAT `GlobalLock 0x5231d0` | handle→locked pointer; do not assume opaque handle equals pointer |
| IAT `GlobalHandle 0x5231cc` | actual locked **pointer**→opaque handle. Python counterpart resolves the identity of the actual live buffer, not equal bytes or a copied allocation |
| IAT `GlobalUnlock 0x5231d8` / `GlobalFree 0x5231c8` | exact handle and explicitly declared results/lifetime, retaining all resource bytes and ordered cleanup events |
| IAT `GetPrivateProfileIntA 0x5231ac` / `StringA 0x5231b0` | four/six stdcall arguments, actual shipped MONSTRE.INI input and original default arguments. Reuse the committed profile protocol; do not install implicit absence or return empty strings for unknown files |

The file input is actual `WORLD/MONDE01.ETA` SHA-256 `19237b8c3f3c0c76022276da229bec727b17603440823c43561aba159dd47015`. The profile is actual `INSTALHD/MONSTRE.INI` SHA-256 `6be59feea11e20eda101ee1e528b3306be447da9e9c3a3807bc2c1bf9e071046`. They remain read-only. Briefing TXT is not read by MissionLoad.

## Resource ownership proposal for Core17 compatibility

Prepare a finite explicit resource registry carrying `(opaque handle, native pointer, actual Python buffer identity, size, initial bytes, active lifetime, declared results)`. Core reports a64KiB classification allocation and a1MiB component LIFO. A freed temporary remains in the state/binding report; reusing an address/buffer and its tail bytes requires an explicit lifetime plan. No new bytes are zeroed merely because a system allocation was requested.

The proposed Core17 Python shape is compatible: `alocar(flags,size)->handle`, `fixar(handle)->live mutable buffer`, `obter_handle(the_same_buffer)->handle`, `desfixar(handle)->explicit u32`, `liberar(handle)->explicit u32`. Native GlobalHandle receives the locked pointer. This is still a pending provider contract until its validated main commit is supplied. Do not import its live implementation or substitute the first lock's handle for the second lock's pointer. Native second-lock NULL is reported as the original fault at0x42efd9, never converted into a clean return.

## Remaining work before a measured original run

1. Assemble the complete raw inherited registry, including exact stored/live player provenance and program-start AI allocations/rules. The scaffold deliberately rejects missing references; it does not create substitute players, Bags or runtime tables.
2. Implement/review the explicit finite file/profile/resource fixtures against the above ABI and preserve all aliases. Eleven callable slots alone are an interface, **not implemented Windows semantics or a runnable fixture**.
3. Audit oracle segmentation/budget behavior and whole-memory capture under Core's committed opt-in dispatcher. No new native execution was performed in this light turn, so the new scaffold has no validation claim.
4. Ask the coordinator for one measured calibration window only when input/handler closure is complete. Suggested first bounded experiment: one actual MONDE01 original entry with a≤60second total cap and explicit partial checkpoints; retain a fault/stop exactly. A later≤300second whole-return attempt needs its own justified grant and enough time before18:25BRT. These are proposed bounds, not measured estimates; do not launch a broad matrix on that basis.
5. Freeze/commit the complete original-only result before writing a Python whole-load composition.

Core17 full remap/cleanup/final AL is not adopted yet; current committed class reset/allocation/classification stops at0x42ef8b. Core `Engin_RetrieveExperimente 0x441623` and the production AI/Economy adapters remain explicit composition dependencies. The original oracle may execute original engine bodies once inputs are declared, but Python M1 acceptance requires the actual committed providers and full post-load byte equality at return to0x42d22d. No whole-load, real mission or objective result is claimed here.
