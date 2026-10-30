# Fatal raid composition — original-first evidence, 2026-10-30

Baseline main `c7f86cd`; intact RISING.EXE SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
`capturar_folhas_luta_fatal_combate.py` restores the exact first-impact entry
from the previously committed original contact window (counter10683, from real
M2.3/frame9000). Source/bench/artifact hashes and input summaries are pinned.
Every native game body executes intact. Hooks only record or halt. Only the
external KERNEL32.GetPrivateProfileStringA import is bound through Core's
declared-stdcall transport to Missions' media-backed PerfilWindows. Actual
section/key/file/default/length/text answers and binding effects are recorded.
No translated game routine executes in this capture.

| Routine | Native cases | Native returns |
|---|---:|---:|
| iagUnitSendMessage (48/44/4a) | 13 | 12 |
| PlayerResetAllie | 7 | 7 |
| PlayerAAttaqueSet | 7 | 7 |
| MAJSympathie | 29 | 29 |
| MessageBoxSet | 10 | 10 |
| EnginSetLevelExperience | 12 | 12 |
| SetDyingEngin | 6 | 6 |
| EnginNextEtape, corpse state4 | 990 | 990 |
| CalculEnginNextEtape, following removal | 3 | 3 |
| EnginInfligeDegat | 9 | 9 |
| InfligeDegat | 3 | 3 |
| **Total** | **1,089** | **1,088** |

The remaining case passes FFFF as the damage-message target; the intact game
faults reading an invalid unit. This negative discovery is preserved, outside
the protected unit-ID domain, and will not be called a successful return.
All other calls return, with zero instruction/time limits or outside-state
writes. Sum of measured leaf-call times is 149.639 seconds; the whole leased
job is bounded by a 1,100-second alarm.

The matrix covers actual human units0/13 (types0/5) and grouped owner4 raider16,
reciprocal AI damage messages, group death44 and target-lost4a, both alliance
directions including owner4, sympathy action thresholds/clamps/global mode,
profile message IDs/queue-full/wrap, levels0..5, and 100/1/0-life inputs.
All byte/word/dword variations are explicit per case; no unit position,
occupancy or ownership is relocated. Direct damage leaves need no range test.

Each of the three corpse sequences starts from the actual output of original
SetDyingEngin. The next 330 original EnginNextEtape calls are sequential,
with declared clock increments, until original RetireEngin and state0. The
following original full 800-slot CalculEnginNextEtape is captured too. Counts
must be compared at their actual phase, not decremented when life reaches0.
These unit windows are bounded experiments, not S1/D1 full-mission evidence.

The committed S1 branch has summaries/boundary logs and snapshot digests but
no full memory snapshots. `capturar_janela_fatal_combate.py` prepares bounded,
observational 250-frame captures from the exact existing Missions snapshots,
including whole per-phase deltas and entry/return leaf snapshots. It accepts
only a matching snapshot SHA and scripted-input prefix, and saves an exact
continuation snapshot. Its Mac-mini runs remain a separate request.

At this evidence-first commit no translation comparison has been made for
these new inputs. Original evidence and later validation reports stay separate.

## Civil and late count-phase supplements

`capturar_civil_fatal_combate.py`: **16/16 native returns**, zero faults or
limits. Twelve unit impacts vary type0/5, entry state5/7/18, and life100/1 at
the original contact geometry. Two original refuge searches return a real
sanctuary; two count cases isolate all-inactive versus corpse-only slots.
The refuge search has no maximum distance: it prefers any nearest own CAVE,
then the nearest own sanctuary. Supplying FFFF as a default would be wrong.

`capturar_fase_contagem_fatal_combate.py`: **82/82 native full unit-loop
returns**, zero faults. Two sequential 41-phase windows set victim0 life1
and raider16 lifeFFFF (explicit durability variation), keeping every original
unit body active and every position/occupancy unchanged. The second window
declares victim0 type5/state7 to exercise the civilian reaction. In both,
the original kills victim0 in the later slot16 body on phase40. Local
population is still16 at that phase's return, then15 after phase41. The
type-specific counter similarly changes3 to2 only in the following phase.
The type5 unit is excluded from the military counter even before death.
These are direct native observations of the phase order at0x456dbd onward,
not a manual count decrement or a D1 defeat claim.
