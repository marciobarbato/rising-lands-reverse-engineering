# Original-first static difficulty audit

Baseline main: a7427fd0e416d212f08af7f0df3d36a224d12f2d, independent clone
and feat/codex-difficulty-scan. Scope is static research only; no native
emulation, original instructions executed, gameplay changes or UI implementation.

The original executable identity is
6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb.
The CD, existing decoders and other-front implementations remain read-only.

The frozen static-scan-v1.json records hashes and offsets for all 38 MONDE*.ETA
files, 436 nonempty-cell monster records, 380 condition records, two INI inputs,
reader identities and selected code references. The unchanged formatos.ler_eta
reader supplies file layout; this scan adds only explicit field observations.

The strongest hidden settings are four MONSTRE.INI keys absent from the shipped
233-byte file: HumanOnly and ProbaCaveJoueur/ProbaCaveIA/ProbaEmbuscade. Their
original defaults are 0/5/2/2, and AvanceMonstre reads their globals. This is a
monster-targeting configuration mechanism, not proof of a general difficulty
selector. A separate original iaConfigGetValue is exactly 89d8c3 (mov eax,ebx;
ret), so named AI initialization knobs currently return their defaults.

A linear original-text disassembly finds 19 absolute field operands (15 stores
in InitEntrerMonstre/ReadConfigMonstre/ChargeMonstre, four AvanceMonstre reads),
plus two indexed operands separately labeled because they address record state.
It finds 78 direct call sites to iaConfigGetValue and no direct call/jump to
ReadConfigMonstre. Indirect calls, computed/alias writes and global UI absence
are not proved by this scan. Original SBL symbols label containing regions;
that labeling is not a recovered complete call graph.

reviewed-routines.asm preserves small byte-hashed intervals. The interval
named AvanceMonstre_and_wait_response_prefix intentionally ends at 0x47b6f1;
AvanceMonstre itself ends at 0x47b6db, and the following 16 bytes are the next
routine's prefix. No extra bytes are presented as part of AvanceMonstre.

The research artifacts precede the validator/report commit. The reproducer
will compare artifacts without rewriting them; no bytes or hashes are adjusted
to make a game implementation pass, because none is implemented here.
