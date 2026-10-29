# Audio state soundness over accepted M2.2

This bounded original-only audit keeps the accepted M2.2 evidence and exclusion
policy unchanged. It does not accept a milestone, enable audio playback, or prove
anything about M2.3, initialized DirectSound or a playing CD track.

## Identities and setup

The only executable oracle is intact RISING.EXE SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
The normalized analysis PE is not executed. The accepted compressed M2.2 capture
is pinned at `4c8f5c14a9623131dd019eafcdc49ea63054ee358f9defde58c12cb949f59ff3`
(raw JSON `1ad031b96300e5c632fd5b6b7857ae30792f78e86531e4f17d1bf7124c6dd930`).
The accepted policy is pinned at
`bf36e6e8f6a38202fa3248256d3de9f768497caa835a563a3ef119be994127f0`.

The [static inventory](evidencias/m22-sound-original-inventory.json) exports
101 sound/MCI symbol intervals and their byte hashes. Its
[disassembly](evidencias/m22-sound-original-inventory.asm) contains no Python
translation. Native inputs reuse the exact accepted named Windows answers via
Missions' existing input dataclasses. The convenience factory's ISO PVD file
is unavailable in the authorized CD-only tree; no ISO label was guessed.
The [run history](validacao/m22-sound-run-history.json) preserves that first
pre-startup failure instead of counting it as a native success.

## What the intact pumps actually do

The [isolated original captures](evidencias/m22-sound-original-pumps.json)
check all 258 state boundaries (initial state plus 257 phases). The private
sound/MCI ranges have one identical input image across that accepted sequence.
Three original routines run to their actual return, with no sound translation:

| Routine | Entry | Instructions | Non-stack stores |
|---|---|---:|---|
| PlaySnd_Manage | 0x48aaca | 352 | 0x521f88 u32: 0→0; 0x498f5c u32: 1→0 |
| MCICD_Play | 0x467a8c | 13 | none; guard read at 0x467a97 of byte 0x4e2f29 |
| MCICD_Manage | 0x467bf0 | 11 | none; guard read at 0x467bf6 of byte 0x4e2f29 |

PlaySnd_Manage is therefore **not a no-op**. The real reset at 0x498f5c must
remain visible even though no game instruction consumes it in this window.

## Native whole-window observation and temporal check

The [first native access replay](evidencias/m22-sound-original-accesses.json)
keeps the accepted sound/CD boundaries: **257/257 phase summaries equal** in
186.752 s. No native read/write reaches the private ranges below. This first
probe used a three-byte backward hook prefix; it alone would not justify
completeness for wider memory operands.

The [second original-only replay](evidencias/m22-sound-original-chained-pumps.json)
starts from the identical accepted MissionLoad state, then removes just the
three pump boundaries and executes their intact bodies throughout 128 frames.
It completes 257 phases in 189.970 s, with original entry counts:
MCICD_Play **130**, PlaySnd_Manage **128**, MCICD_Manage **128**.
The code SHA-256 is unchanged before/after.

For this second run, hooks begin 15 bytes before each watched range and filter
actual intersections. The explicit original-text disassembly reports a maximum
memory operand of 10 bytes (legacy x87 included); REP strings are hooked per
element. The audit records the text hash and 18 skip-data bytes, so it is not
presented as a universal x86 operand-width theorem. Diagnostics and actual
phase differences are written before a failure exits.

Watched intervals are half-open:

| Range | Classification |
|---|---|
| 0x498f14..0x498f6c | Initialized private sound scalars/table |
| 0x521358..0x522234 | Static request/waiting/logical/physical/bank neighborhood |
| 0x496fdc..0x496fe0 | Shared MCI clock copy |
| 0x4e2f28..0x4e2f34 | Shared CD-playing/init and MCI fields |
| 0x4e1d18..0x4e1d1c | Shared random permutation cursor |

In the chained run, the private ranges have **zero game/display readers**;
all observed private readers are sound-library instructions. Every captured
byte outside 0x498f5c equals the accepted reference at every phase. The load
-tail is strictly equal; the remaining **256 phases differ in exactly one
byte**, 0x498f5c: accepted 1, actual 0, after the first real manager call.
The store at 0x521f88 keeps an already-zero word.

This is **not strict whole-state equality**. No accepted mask or reference was
edited to make it pass. The [summary report](validacao/m22-soundness.json)
retains the discrepancy, original entry counts, read counts, start/end hashes,
watch ranges, source hashes and artifact identities.

## Shared CD state is not private sound state

The declared input is **no CD track playing**, byte 0x4e2f28 stays zero, and
MCICD_Init never executes (byte 0x4e2f29 is zero). The positive native reads
include CalculGame's shared CD flag test and shared cursor accesses by
CalculGame, MenuInit and NextAnimVeget. CalculGame's original branch at
0x42d2f0 tests 0x4e2f28, reads the permutation cursor at 0x42d2f9, writes it
at 0x42d322 and calls MCICD_Play at 0x42d328. This branch occurs even when
the guarded MCI routine itself returns without a store.

A playing-CD scenario changes the consumption of cursor 0x4e1d18 and therefore
can change game logic over long runs. Neither those flags nor the cursor are
classified as isolated private audio state. The result does not extrapolate
to nonzero MCI init, initialized request queues, arbitrary dynamic sound heaps,
other windows or later raids.

## Reproduction

Run from the independent Audio repository. All native jobs use the unchanged
shared lease; `audio_m22_soundness.py` installs an 18-minute SIGALRM after the
lease grants execution, with a 180 s per-phase original bench limit.

```sh
python3 '/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py' \
  codex-audio-m22-pumps -- \
  /Users/marcio/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B \
  pesquisas-paralelas/audio/audio_m22_soundness.py pumps \
  --output .local/audio/repeat-pumps.json

python3 '/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py' \
  codex-audio-m22-accesses -- \
  /Users/marcio/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B \
  pesquisas-paralelas/audio/audio_m22_soundness.py logic --frames 128 \
  --output .local/audio/repeat-accesses.json

python3 '/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py' \
  codex-audio-m22-chained-pumps -- \
  /Users/marcio/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B \
  pesquisas-paralelas/audio/audio_m22_soundness.py logic --frames 128 --execute-pumps \
  --output .local/audio/repeat-chained-pumps.json
```

Use fresh output paths; the scripts refuse evidence overwrite. A rerun using
the current script widens hooks to 15 bytes in either mode. Original media and
runtime are read-only. No long Mac mini job is requested by this bounded audit.
