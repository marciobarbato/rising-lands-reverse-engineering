# Workstream F handoff — static hidden-difficulty check

Branch: feat/codex-difficulty-scan. Independent clone:
`/Users/marcio/git/Rising-Lands-Codex-Difficulty`.
Baseline main: a7427fd0e416d212f08af7f0df3d36a224d12f2d.
Original research commit:4af3abc4176848e5e7e15056ece524b5efd8330b.
Only pesquisas-paralelas/dificuldade/** changes. No main merge/push, game
behavior changes, original-media writes or emulated/native-game calls.

Review [DIFFICULTY_SCAN.md](DIFFICULTY_SCAN.md) for the concise finding and
confidence labels; [static-scan-v1.json](evidence/static-scan-v1.json) contains
all input hashes, file offsets, reader commits and instruction references.
[Reviewed instructions](evidence/reviewed-routines.asm) are from the intact
original, never the normalized PE. Existing owner native proofs are cited,
not represented as fresh execution by this front.

The strongest positive finding is four absent shipped MONSTRE.INI keys with
live monster-targeting consumers: HumanOnly0 and ProbaCaveJoueur5/ProbaCaveIA2/
ProbaEmbuscade2. These are hidden configuration knobs, not an established
player difficulty level. iaConfigGetValue0x47fc54 returns its EBX default
(bytes89d8c3), so named AI tuning hooks do not read an external configuration.
All38 ETA missions parse through the unchanged reader;436 nonempty-cell monster
records and380 condition records show per-mission tuning. MONDE01's two timed
entry periods are300/360 on disk→9000/10800 logic-counter units; zero-period
ambush cells are not counted as raids.

No menu writer appears in the bounded absolute/direct-reference scan. It does
not prove global UI absence, indirect call reachability or lack of alias writes.
ReadConfigMonstre has no direct CALL/JMP found, not a proven globally dead body.
The editor meaning of the discarded16 bytes and unconsumed ETA suffix remains
open. No user-facing difficulty option was added, and no claim is made that
the whole game has no hidden parameter.

Reproduction requires the original CD at the explicit --cd root and
Capstone5.0.7 (local tooling dependency only), plus Python3 standard library:

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
