# Scripted-input render research (API 1.7 target)

The dispatch title/report call this 1.6, but its explicit goal names 1.7. This front follows the explicit 1.7 target.
No M3 acceptance or main integration is claimed.

The source probe ref is pinned read-only to `f0588447b6cea3cc10701233a55bbcd16551e5e5` on `origin/feat/re-missions`.
It was not merged. `sondas-api17-proveniencia.json` pins P1/P2/P3/K1 reports, input/output streams, all initial native
artifacts and intact-executable intervals (SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`).

Before translation, a native checkpoint was regenerated after the accepted frame 128. Its whole-state summary is
`eb714f7d5a694ad91bab9b41c37a28860006c89be03f9170e3b312064a4b04b2`, matching the accepted M2.2 capture. Snapshots remain
local task data under `.local/graficos-api17-start`, not tracked research evidence. The native recorder imports only
Missions' pinned scripted-input module using git-show, then executes WndProc and the original game/display paths.

Initial original-only recordings (before translation):

| Probe | Native frames | Surface and whole-state reproduction |
|---|---|---|
| P1 | 129–629 (501) | 501/501 match the published probe |
| P2 | 129–729 (601) | 601/601 match |
| P3 | 129–300 (172) | 172/172 match |

The JSON records are delivered in xz containers; decompressed byte hashes are unchanged. These files preserve every render entry buffer, native terrain cache, before/after surface and drawing arguments.
The frozen V1 producer source has exactly the SHA-256 recorded in each initial capture. V1's shaded rectangle records
include one surplus observed stack word; only the first pushed word is an argument. Text entry code hooks were
preempted by the bench's boundary stop, so their V1 `text_boundaries` arrays are empty; this is not evidence that no
text boundary occurred. The follow-up recorder uses a block hook and additionally records saved-background/grayscale
buffers before any translation of those paths.

A native AffBatiments matrix restored from P3's reproduced frame-220 CAVE-creation checkpoint adds 160 calls: types
2/3; modes 0/1/2/6/7 across 13 progress thresholds; uninhabited modes 3/4/5 with permutation cursors 0/1/254 and mode-3
construction height offsets 0/35/255. Every native call returned. Declared writes and their exact inputs are in the
matrix; the initial state, CPU and surfaces are restored for every call. This extends progress/branch evidence without
running thousands of frames on the MacBook.

**Native boundary limitation.** Missions' display-v2 oracle declares AffText (0x459454) non-executed. The published
probes therefore validate native tooltip layout/backgrounds but do not validate glyph drawing. Normal rendering must
retain a visible dependency for missing text rendering; no empty text callback or fabricated glyph output is allowed.

All native runs use `heavy_lease.py`. Initial measured run times: P1 266.802 s, P2 312.900 s, P3 94.014 s, matrix
20.978 s. Additional recording of the missing inputs is kept distinct. The full P3 probe is 3,001 frames and its
published native run took about 31 minutes, so full native continuation is routed to the coordinator's Mac mini.
