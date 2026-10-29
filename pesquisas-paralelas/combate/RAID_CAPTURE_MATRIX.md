# Real raid original-first capture matrix

Base: `c08e1fb`, branch `feat/re-combat`. The only execution oracle is intact
RISING.EXE SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
No milestone acceptance or main integration is authorized by this task.

Inputs are the full states after frames 9000 and 9176 in Missions' committed
M2.3 part 09. The reader checks compressed/raw manifest pins and the complete
checkpoint summary, using AI/runtime's compressed reader and Missions' decoder.
All blocks, including graphics bytes, remain present. Native hooks only record
or halt before an explicit dependency; no game body is bridged, patched or skipped.
A zeroed 64-KiB stack, sentinel return, argument registers and stack words are
explicit leaf-call inputs. Checkpoint stacks were not serialized by Missions.

| Case family | Checkpoints | Declared input | Scope |
|---|---|---|---|
| Player attack order/step | 9000, 9176 | SetAttaqueEngin units 0,1,2, mode 1, target 16; then CalculAttaqueEngin | Real positions, occupancy, navigation and tables |
| Raid attack order/step | 9000, 9176 | Unit 16, mode 1 target 0; mode 3 structure 0 | Sanctuary footprint and real navigation |
| Reacquisition | 9000, 9176 | EnginTrouveCible units 0,1,2,15,16 | Original grid traversal, no relocated enemies |
| Repeated hits | 9000, 9176 | InfligeDegat at actual target +7c; source 0 to 16 and source 16 to 0 | Full original damage/retaliation until first named stop |
| Lethal/overkill leaves | 9000, 9176 | EnginInfligeDegat, explicit victim +9a = 1/0 | Health variations are declared; geometry stays original |
| Death/removal | 9000, 9176 | SetDyingEngin on 0/16; RetireEngin only after successful dying return | Core-owned; capture does not transfer ownership |
| Sanctuary consumer | 9000, 9176 | BatimentInfligeDegat, direct u32 damage boundaries | Original local-player sound boundary retains accumulated damage |
| Sanctuary threshold variant | 9000, 9176 | Same direct damage; explicitly set local camera to 1 | Separate declared input, not the player-0 path; original audio guards run |
| Native unit windows | 9000, 9176 | Three order sets, counter = checkpoint+tick; native EnginNextEtape active units ascending, then ProjectileCalcul | Bounded unit/projectile driver; excludes other CalculGame phases and is not a full-frame equivalence proof |

## Initial probe (before translation)

[evidence](evidencias/probe-combate-raid-original-v1.json): 30 calls, 22 returns,
8 named audio stops, zero faults and instruction/time limits. Ten calls each
cover SetAttaqueEngin and CalculAttaqueEngin, four SetDyingEngin, four InfligeDegat,
two BatimentInfligeDegat. This probe's exact source versions are retained under
[evidencias/fontes-probe-raid-v1](evidencias/fontes-probe-raid-v1/bancada_combate_raid.py.txt),
matching its source hashes. Later harness revisions add execute permissions and
supplemental cases; the probe artifact is immutable.

Native SetDyingEngin reaches AI group/task updates for raid unit 16. A real player
hit reaches PlaySnd_PostSound before damage subtraction. This probe halts at
PlaySnd_StopSound even for its original no-effect handle guard; the later capture
must distinguish that deliberate stop from actual physical death completion.

The maintained contract and final validation report will separate full original
returns, translated whole-state comparisons and named dependency stops. A native
case or native window alone is not a translated-chain proof.
