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

## Translation and qualification

The evidence commits are `9a05e69`, `9a1f846` and `51fc02e`; no production translation was included in them.
The final recorder reruns took P1 277.140 s, P2 330.936 s, P3 92.017 s and the 160-case matrix 21.657 s.
The expanded matrix restored that same checkpoint and executed 600 calls in 82.035 s: all CAVE health words 0..100
in modes 0/1/2/6/7, plus the original sanctuary and uninhabited/RNG cases. Python matches all 600 surfaces, argument
lists and DGROUP projections exactly. The initial recordings are retained in separate immutable xz containers;
they are not silently replaced by the richer recordings.

API 1.7 adds uninhabited CAVE/sanctuary construction facades, selected builder construction bodies, selected cell-order
markers, CAVE placement grid, tooltip frame/shadow/background save and restoration. The original placement ghost is
a gray rectangle with invalid-cell outlines, not the CAVE sprite. Existing inhabited sanctuary and other predecessor
providers remain byte-identical. The frame globals schema is unchanged. Glyphs remain a named `0x459454` dependency.

The fixture-only `FronteiraTextoGravada` implements the probe's declared non-execution after verifying text, font,
rectangle, flags and the entire native pre-text surface. It rejects unrecorded calls or a single wrong pixel. It is
not a production fallback. With this explicit probe boundary, P1 is 501/501, P2 601/601 and P3 172/172 full surfaces,
arguments and projected effects equal; the chain carries Python surface/cache/saved-background bytes. Normal default
rendering stops at frame 170/219/141 respectively, with 41/90/12 complete prefix frames and exact native partial
pixels/arguments at the first glyph dependency. See `validacao/prefixos-sondas-api17.json` and the per-probe reports.

The fresh 128-frame `--hud` regression is 128/128, no stop or differing frame, matching all old 1.4/1.5 hashes. Its log
birth-to-finish interval was 482 s initially, then 450 s after callback-order review (including lease startup), with
byte-identical reports. The native replay uses the intact executable, never the
static-analysis PE. A temporary PE with normalized directory/section headers was used only for objdump inspection;
no byte from that analysis file was executed or used as an execution oracle.

## Exact Mac mini continuation commands

Run from a checkout of the pushed `feat/re-graphics`. These commands regenerate the accepted frame-128 start and
capture all 3,001 P3 frames in four bounded native jobs. The recorder imports Missions' pinned source with git-show;
do not merge the Missions branch. Every invocation saves a resumable checkpoint and has an 18-minute internal budget.
If a budget stop occurs, resume from the actual checkpoint printed in its report before attempting the next target.

```sh
python3 "/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py" graphics17-P3-start -- \
  python3 -B pesquisas-paralelas/graficos-animacao/capturar_sondas_graficos_m3.py \
  --prepare --start .local/graficos-api17-start
python3 "/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py" graphics17-P3-a -- \
  python3 -B pesquisas-paralelas/graficos-animacao/capturar_sondas_graficos_m3.py \
  --start .local/graficos-api17-start --probe P3 --to 878 \
  --output pesquisas-paralelas/graficos-animacao/evidencias/sonda-render-P3-129-878-api17.json
python3 "/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py" graphics17-P3-b -- \
  python3 -B pesquisas-paralelas/graficos-animacao/capturar_sondas_graficos_m3.py \
  --start .local/graficos-api17-start --probe P3 --to 1628 \
  --resume .local/graficos-api17-start/P3-00878.pickle \
  --output pesquisas-paralelas/graficos-animacao/evidencias/sonda-render-P3-879-1628-api17.json
python3 "/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py" graphics17-P3-c -- \
  python3 -B pesquisas-paralelas/graficos-animacao/capturar_sondas_graficos_m3.py \
  --start .local/graficos-api17-start --probe P3 --to 2378 \
  --resume .local/graficos-api17-start/P3-01628.pickle \
  --output pesquisas-paralelas/graficos-animacao/evidencias/sonda-render-P3-1629-2378-api17.json
python3 "/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py" graphics17-P3-d -- \
  python3 -B pesquisas-paralelas/graficos-animacao/capturar_sondas_graficos_m3.py \
  --start .local/graficos-api17-start --probe P3 --to 3129 \
  --resume .local/graficos-api17-start/P3-02378.pickle \
  --output pesquisas-paralelas/graficos-animacao/evidencias/sonda-render-P3-2379-3129-api17.json
```

For a smaller continuation using this MacBook's local frame-300 checkpoint (copy it separately; it is not tracked),
the first target can instead be 1050 with `--resume .local/graficos-api17-start/P3-00300.pickle`, then 1800/2550/3129.
Preserve decompressed SHA-256 when placing large JSON captures into xz containers before Git delivery.
Validate each returned capture with `validar_sondas_graficos_m3.py --capture <file> --probe-text-boundary --output
<comparison.json>` and report the first stop. Contiguous chunks whose endpoints match the native surfaces/cache/
background compose the same chain; the current delivered chain stops at 300. The complete P3 chain, P4/P5, and a
native text-enabled glyph capture remain external follow-up work.
