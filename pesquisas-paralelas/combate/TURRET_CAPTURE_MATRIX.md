# Turret orders: original-first capture, 2026-10-30

Initial main sync: `3e0de77`. Only intact RISING.EXE
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`
executes. No translated game routine runs in either capture. Native hooks
record entries/stores or halt; they never replace a game body.

`bancada_ordens_torres_combate.py` reconstructs pinned Missions P1/frame250
and P6/frame2020 using the existing compressed-part reader and delta decoder.
P6 has the genuinely selected sanctuary and completed cave. Every changed
type, owner, bonus, target step-cell or selected ID is declared per case;
these are leaf variations on real memory, not physical turret construction.

| Original routine | Cases | Native returns | Faults / limits / outside writes |
|---|---:|---:|---:|
| BatimentPeutAttaquer, 0x42436c | 148 | 148 | 0 / 0 / 0 |
| BatimentInitAttaqueSelect, 0x4242cc | 40 | 40 | 0 / 0 / 0 |

The query covers both turret types 10/11, non-turret prefixes, ground/flying
units, neutral owner 200, structure targets, owners 0..4/200, bonus 255,
inclusive radius 7 and outside radius 8, and mode 5. The setter covers four
players, selected IDs 0/1/999, modes 0/1/3/5/255, self and FFFF references.
Dirty high register halves are explicit. Every general register, EFLAGS,
whole checkpoint delta, stores and nested native entries are recorded in
`evidencias/captura-ordens-torres-original-v1.json`. No Python comparison has
been made at this evidence-first stage. The JSON pins source/code/state hashes.
The query has 68 true and 80 false results (testing AL); the setter has 36
ordered two-store returns and four self-target returns without stores.

## Raid target contact: bounded inventory

`capturar_contato_alvo_incursao.py` restores real M2.3/frame9000. Original
SetDeplaceEngin moves soldiers 0..2 toward 0x2e03 while raid unit 16 waits;
then only these four units and projectiles advance. At counter 10671 the
native window reaches distance squared 4 and issues reciprocal native
SetAttaqueEngin orders. No positions, life or occupancy are patched.

The original enters CalculAttaqueEngin and InfligeDegat. The former isolated
call returns. The latter reaches diplomacy and MessageBoxSet, then faults
fetching unresolved KERNEL32!GetPrivateProfileStringA (IAT0x5231b0,
target0x1235f0). This is an honest harness stop,
not evidence of completed damage/death. SetDyingEngin, RetireEngin,
EnginInfligeDegat and EnginSetLevelExperience were not reached before it.
The complete partial capture is stored losslessly as
`evidencias/captura-contato-alvo-incursao-original-v1.json.xz`; decompression
recovers the original JSON bytes. The original source/log are preserved.
This staged unit window is separate from Missions' complete D1 search.

Supplement `aa82d33` (`capturar_fronteira_contato_combate.py`) restores the
exact two captured entry states and halts at iagUnitSendMessage 0x4829c8.
CalculAttaqueEngin returns; InfligeDegat stops before that callback, with
zero faults, limits or outside writes. No state variation or game substitution
is introduced. `evidencias/captura-fronteira-contato-original-v1.json` pins the
source capture and records full deltas/registers/stores. The first unrestricted
import fault remains historical evidence and is not counted as a completed
damage return. Subsequent translation results live separately under
`validacao/`; the original evidence is unchanged.
