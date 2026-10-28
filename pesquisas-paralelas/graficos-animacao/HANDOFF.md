# Graphics handoff

Research round: 2026-10-28. Chat `01a18262-cdd5-7b13-84af-0d6eca1a43eb`.
Worktree: `/Users/marcio/git/Rising Lands/worktrees/re-graphics`.
Feature branch: `feat/re-graphics`, based on organization revision `6634be3af2d255846a847d8aa21ad4edf1cdb589`. The feature commit is the commit carrying this handoff; final commit and remote-main merge identities are reported to the coordinator after the authorized integration helper finishes.

## Delivered slice

`portoes_graficos.py` reconstructs the type-12 `HERSE` gate facade before the common `AffBatiments` tail. It exposes a pure query and indexed compositor, 64 hash-identified frame associations, an original-buffer contact sheet, exact original-byte extracts and a separately run original-x86 validator. Previous releases, stage reports, manifests, inputs, and predecessor hashes are unchanged.

The exact supported API and formulas are in [the graphics manual](../../docs/GRAPHICS.md#gate-facade-contract--2026-10-28). `consultar_portao` requires keyword inputs: counter u8 restricted to 0–31; full orientation u16; raw `+0x0A` u16; owner 0–4 and camera 0–3; mode u8; record visibility u8; separate cell discovery u8; projected x/y i16; window width/height u16 in cells restricted to 1–1024. The caller supplies an already resolved object-253/type-12 runtime record. There are no defaults for missing state and no disk-to-runtime conversion.

## Original contract and ordering

1. Reject a foreign-owner record when mode is not 3 and its visibility byte at `+0x110+camera` is zero.
2. Query discovery at the per-camera cell map; bit 16 suppresses the facade.
3. Save the current global clip; resolve the gate occupancy label (the public caller must do this).
4. Query `BatimentGetEtat`, consume its low u16, and replace the clip with the state-dependent inclusive rectangle. The incoming clip is not intersected.
5. Copy one sprite with clipping enabled. Orientation zero selects `7576+counter` at `(x,y)`; any nonzero u16 selects `7608+counter` at `(i16(x+5),i16(y+4))`.
6. Stop at `0x40F342`, before the common workshop/restore/selection/gauge tail. Early rejection stops at `0x40F491` before the epilogue. Missing original occupancy saves the clip then rejects; it does not yield a public prepared-record plan.

The facade makes no player-color or shadow call. The pure compositor returns new bytes and preserves destination opacity semantics. The original captures compare the complete 276-byte runtime record before/after, and verify the selected occupancy/object/discovery cells are preserved. There are no allocator, physical-gate, damage, economic, or simulation callbacks. The new APIs do not import another owner's implementation or a live worktree.

Invalid widths/ranges, booleans, and incompatible nonempty-plan surface dimensions raise `ValueError`; missing required arguments raise `TypeError`. Counters 32–255 raise `NotImplementedError`. The original accepts the complete byte and runs into later strips; 896 such captures are recorded separately without widening the public domain. Hidden-cell plans have no layers and preserve the background without accessing a catalog. Camera 4 would access beyond this record's four visibility slots and is unsupported.

## Evidence

- `RISING.EXE`: SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
- `AffBatiments` gate branch `0x407FA7..0x4080E8`: SHA-256 `f52190772fa3b3abf70197f451bab4fe9887b56edf436b2d1abc574ff0cce20d`.
- Gate copy join `0x408412..0x408422`; raw-state query `0x41A8E5..0x41A940`; clip helpers `0x40F4B7..0x40F535`. Input convention: `AX=x`, `DX=y`, `BX=cell`; runtime base `0x49A0C8`, stride 276; viewport `0x508724/+2`; object constant at `0x495BF9` equals 253.
- Type-12 table `0x495FFC..0x496030` contains `HERSE` and denominator 70. `BatimentGetEtat` returns `floor(raw_u16*200/70)`; this renderer consumes the low word without economic interpretation.
- `BUILDING.CMP`: SHA-256 `af4f94ea996a65d36592bb6cefc407dc628b3d488c9c335b8f6015bbfcb6a3ae`; IDs 7576–7639 correspond to local indices 547–610. Zero-orientation frames are 34×30; nonzero-orientation frames are 21×47.
- [Exact bytes and appended predecessor provenance](evidencias/portoes-graficos.json), [frame and opacity hashes](artefatos/associacoes-portoes.json), [original reference captures](validacao/x86-portoes-graficos.json), [contact sheet](artefatos/portoes-contato.png). The sheet contains 64 independently compared original 64×64 surfaces, with the original palette applied afterward. Its patterned background is an indexed test fixture.

## Actual validation

Commands run in this feature worktree:

```sh
python3 -B pesquisas-paralelas/graficos-animacao/validar_portoes_graficos.py
python3 -B -m unittest discover -s pesquisas-paralelas/graficos-animacao -p 'test_portoes_graficos.py' -v
python3 -B scripts/check.py --domain graphics
```

The completed x86 run uses the authorized execution context supporting Unicorn JIT memory: **2,792 bounded executions / 1,651,749 observed instructions**. It records 1,700 supported call/clip captures (all 32 counters, full-word orientation boundaries, four modes, owner/camera/visibility/discovery combinations, signed coordinates, raw-state low-word boundaries, and structure index 999), 896 raw counter-overrun captures, two missing-occupancy captures, two bank initialization calls, and **192 exact indexed-buffer comparisons**. No skipped cases, expected x86 exceptions, or instruction/time limits occurred. The supported draw cases stop deliberately before the common tail; they do not claim full function or game execution.

Nine new regression tests pass; `scripts/check.py --domain graphics` passes **82 tests**, with no skips and valid documentation links. Legacy x86 validators were not rerun; their saved reports are only replayed by existing Python tests. A sandbox JIT smoke probe produced no usable reference result, and an initial permitted development run found a camera-4 fixture indexing error; the public camera range and fixture were corrected to the four in-record camera slots before producing the final saved run.

Integration is to be performed from the clean committed feature worktree using `python3 scripts/workstream.py integrate graphics`. The coordinator receives the actual common-suite counts and remote-main merge identity after it completes; this file does not claim a future push already succeeded.

## Remaining dependencies

Core supplies an existing prepared runtime record and occupancy mapping, including the current gate counter; the renderer neither resets nor increments it. The raw state word is consumed exactly, without deriving resource costs, construction progress, or physical collision rules. Scene projection, global draw order, workshop callback, clip restoration in a stateful consumer, selection/gauges, complete mission loading, other buildings, and preview integration remain open. No claim of a complete playable game is made.
