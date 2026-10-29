# Workstream F handoff — static hidden-difficulty check

Branch: feat/codex-difficulty-scan. Independent clone:
`/Users/marcio/git/Rising-Lands-Codex-Difficulty`.
Baseline main: a7427fd0e416d212f08af7f0df3d36a224d12f2d.
Original research commit: 4af3abc4176848e5e7e15056ece524b5efd8330b.
Only pesquisas-paralelas/dificuldade/** changes. No merge into main or push to main, game
behavior changes, original-media writes or emulated/native-game calls.

Review [DIFFICULTY_SCAN.md](DIFFICULTY_SCAN.md) for the concise finding and
confidence labels; [static-scan-v1.json](evidence/static-scan-v1.json) contains
all input hashes, file offsets, reader commits and instruction references.
[Reviewed instructions](evidence/reviewed-routines.asm) are from the intact
original, never the normalized PE. Existing owner native proofs are cited,
not represented as fresh execution by this front.

The strongest positive finding is four absent shipped MONSTRE.INI keys with
live monster-targeting consumers: HumanOnly=0 and ProbaCaveJoueur=5/ProbaCaveIA=2/
ProbaEmbuscade=2. These are hidden configuration knobs, not an established
player difficulty level. iaConfigGetValue 0x47fc54 returns its EBX default
(bytes 89d8c3), so named AI tuning hooks do not read an external configuration.
All 38 ETA missions parse through the unchanged reader; 436 nonempty-cell monster
records and 380 condition records show per-mission tuning. MONDE01's two timed
entry periods are 300/360 on disk→9000/10800 logic-counter units; zero-period
ambush cells are not counted as raids.

No menu writer appears in the bounded absolute/direct-reference scan. It does
not prove global UI absence, indirect call reachability or lack of alias writes.
ReadConfigMonstre has no direct CALL/JMP found, not a proven globally dead body.
The editor meaning of the discarded 16 bytes and unconsumed ETA suffix remains
open. No user-facing difficulty option was added, and no claim is made that
the whole game has no hidden parameter.

Reproduction requires the original CD at the explicit --cd root and
Capstone 5.0.7 (local tooling dependency only), plus Python 3 standard library:

```sh
python3 -m pip install --target .local/python capstone==5.0.7
PYTHONPATH=.local/python python3 -B pesquisas-paralelas/dificuldade/difficulty_scan.py \
  --cd '/Users/marcio/git/Rising Lands/source/cd'
PYTHONPATH=.local/python python3 -B -m unittest discover \
  -s pesquisas-paralelas/dificuldade/testes -v
```

Set RISING_CD_ROOT for the tests if CD location differs. Default verification
never rewrites artifacts; --write creates the initial artifacts exclusively
and refuses existing files. The tests compare exact artifacts, reject wrong
original identity and incomplete mission corpora, and validate the distinctions
between absolute/indexed profile operands and timed/untimed monster entries.

Five static tests passed with zero skips. Final latest-main verification,
logs/output sizes and the validated implementation SHA are recorded below.
There is no registered common --domain difficulty; shared scripts are unchanged.
The coordinator reviews/integrates; this writer pushes only its feature branch.


## Final validated delivery

Research: `4af3abc4176848e5e7e15056ece524b5efd8330b`.
Report/tool/tests: `33adea370a114cc6b7b24383b2ddf89a6ee2802f`.
Validated code/formatter: `ec004fe77bb252910ba46222f2afe3c021cb9c8b`.
Latest fetched main `a7427fd0e416d212f08af7f0df3d36a224d12f2d` was already
an ancestor; the merge reported already up to date. No main integration ran.
The final metadata commit changes documentation/logs only.

The static verifier reproduces both artifacts exactly. Five tests pass,
zero skips/failures, 1.683 seconds. Documentation links, full-branch whitespace
and owned-path checks pass. Six trailing spaces on displayed RET rows were
normalized; original address/opcode/interval identities remain unchanged.
The prior research commit preserves the initial formatting.

The two original-research artifacts total **307,770 bytes**:
JSON 268,191 bytes and assembly 39,579 bytes. All files are below 50MB. Final
validation records output hashes/sizes in [results.json](validation/results.json),
with [verifier output](validation/final-static-verify.log) and
[test log](validation/final-tests.log). No emulation, heavy lease or Mac mini
job was used/required. Previous preliminary local validation remains under
this clone's ignored .local/preliminary-static-validation.

Only the dedicated remote feature branch is pushed. The final full remote
SHA and exact tracked-delivery byte total are reported with the delivery,
without amending a completed commit to insert its own future identity.


## Latest-main bounded refresh

Fetched/merged current main
`3579c40ad455564f2a9b32c9a01b815b24d68f87` (Core native hooks).
Merge and validated revision: `5eb91e29217bd8f647ec123f25aa8da4a564db19`.
No selected reader changed. Both static artifacts reproduce exactly; all five
tests pass, zero skips/failures, 1.631 seconds. Documentation links, latest-main
ancestry, full-branch whitespace and owned-path checks pass. This refresh adds
no new research or native execution. Original evidence remains 307,770 bytes.

Current results: [latest-main-results.json](validation/latest-main-results.json),
[verifier output](validation/latest-main-static-verify.log),
[test log](validation/latest-main-tests.log). Earlier validation is retained
as historical evidence for its recorded source revision.

Final tracked delivery: 13 files, 343,447 bytes, largest
file 268,191 bytes; every output remains below 50MB. The metadata commit following
this tested merge adds only this bounded refresh handoff and its new logs.
