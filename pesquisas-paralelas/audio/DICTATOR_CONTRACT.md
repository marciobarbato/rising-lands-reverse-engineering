# Entry-word256 Audio queue reference contract

Base main: `a7427fd0e416d212f08af7f0df3d36a224d12f2d`; independent Audio
clone/branch and write ownership unchanged. Prior 139-call reuse/concurrency
corpus is integrated baseline, not new coverage. Python remains the byte-exact
reference/harness for a future Rust port; this adds no live device model or ABI.

## Original-first scope and inputs

Original executable SHA-256:
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Existing sound byte inventories include all reached bodies. New original-only
v3 has **140 actual original entries / 35 scenarios**, 0.432 seconds: 34
returned scenarios and one explicit unresolved allocation-error/UI boundary.
Every memory image, ordered external answer, raw COM ABI argument and completed
sequence step is frozen before translation. Synthetic input memory is the same
88-byte global, 3804-byte BSS and 65536-byte caller region of the queue fixtures.
No mission state, audio sample corpus or initialized device is fabricated.

The allocator is declared at original IAT `0x5231c0`: GlobalAlloc(flags=0,
size=8) returns an explicitly supplied u32 pointer `0x7009000` or NULL. Flags0
means the fixture retains its patterned inherited allocation bytes; it does
not guess a zero fill. The intact InitDictator `0x489f39` runs OurAlloc, then
writes both pointer globals `0x521fc0/0x521fb4`, slot+4=`0x521f94`, active=0
and enabled=1. It does not initialize slot+0. The allocation-count increment at
`0x522230` is preserved. A NULL result reaches unresolved MessageBoxA at
original caller `0x48c227` / IAT `0x5232b0`; the failed attempt's original fetch
fault is retained, with no substituted UI answer or later initialization.

All other COM/file inputs reuse the prior declared contract: explicit Create,
Lock/read/Unlock, status, position, volume, Play, Stop and Release answers.
Output pointer writes and HRESULT remain independent; there are no default
callbacks. The new sound fixture is entry-word256, PCM mono/16bit/22050Hz,
64 explicit synthetic bytes, with three header variants. No sound is emitted.

## Proven caller behavior

- PostSound/HandlSnd_Insert admits entry-word256 and retains the caller's handle
  reference. Manage's `0x48a702` branch uses the separate 44-byte dictator record
  at `0x521f94` and the actual InitDictator slot; it does not allocate a PSB slot.
- The branch writes flags=0 even if the caller requested flags=1. The original
  Play therefore receives flags0. It copies ID/bank/entry/header/caller reference,
  sets volume256 and dirty1, creates/fills the declared buffer, calls the real
  start chain, removes the waiting record, then sets active=1. Start failures
  still retain those mutations and return the aggregate failure result.
- A pending entry-word256 request remains queued while active=1. The persistent
  eight-call case initializes, posts, manages, posts another caller, manages
  while occupied, explicitly clears, relaunches and clears through IsStopped.
  No fixture memory is rewritten between original calls.
- ClearListe uses the actual DSB_IsStopped `0x48beb9` semantics with statuses
  0/1/5 and success/error HRESULT. Stop/Release and caller invalidation occur
  only in their original branches. Explicit DestroyDictator `0x489f04` clears
  active before Stop/Release and invalidates its inherited caller reference.
- PlaySnd_SetGameVolume `0x48aa45` uses signed clamp0..256 and writes dirty=1.
  The active dictator uses original volume-table words; the volume update's
  error HRESULT is ignored. Declared inputs cover0/128/256/257/0xffffffff.

Protected domain is these exact inherited region layouts, nonnull allocated
8-byte slot, declared sound metadata and explicit platform answers. Queue
identity/aliasing, all earlier partial effects and untouched words are retained.
No actual DirectSound initialization, memory allocator/hardware ownership,
unwritten output/status, asynchronous state, arbitrary unobserved saturation,
long mission flow or acceptance milestone is established.

## Preserved diagnostic history and bounds

v1 stops at the missing RET interval endpoint `0x48c240`; its native_calls140
field counted planned sequence entries, while only35 entries were attempted.
That frozen diagnostic is not counted as140 executed calls. v2 includes that
intact RET and records actual128/planned140 entries:12 declared Play mismatches
exposed the original flags reset, plus the NULL allocation stop. v3 corrects
only the declared Play inputs and executes all140 entries with one expected
NULL-allocation boundary. Original code and earlier reports are unchanged.

Every native job uses unchanged shared heavy_lease.py, SIGALRM600 after lease
acquisition, a monotonic600-second deadline and50,000 instructions per call.
Each new job took under one second. No Mac mini time is required. Original
research commits precede implementation; current fresh differential, API tests
and exact native app build are reported in the handoff after they run.
