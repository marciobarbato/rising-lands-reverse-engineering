# Graphics recovery — 2026-10-30

The worktree merged `origin/main` at `ad0a4a9` before recovering the coordinator-preserved
`2add6fc` (`wip/re-graphics-codex-0430`). Delivery is feature-branch push only.

## Native view inventory, before translation

The preserved final batches at offsets 1240, 1480 and 1720 complete the original-only matrix.
`validar_grade_vistas19.py --output validacao/grade-vistas19-native-audit.json` checks
**3840/3840 calls**, 1920 exact origins per routine (`AffGame 0x417698`, `RestoreAll 0x474B08`).
The finite matrix is `(x,y)` with x=0..39, y=0..47 on the original 64×64 MONDE01 map,
25×17 viewport, camera 0, native frame-128 state. Only the two explicitly declared
origin words are changed before each restored native call.

Every call returns to `0x03000000`; there are zero additional logic writes, CRT changes
or display RNG writer hits. DGROUP before/after hashes and each changed byte are checked
against the existing cumulative display mask without modifying it. Changed heap objects
are restricted to the previously identified display-bank/cache allocations. The validator
checks both original producer source identities, the complete case order, uniqueness,
executable/code hashes, and the native input bytes. It pins only Graphics-owned evidence
and source files. The saved report records each capture's actual duration.

The intact executable is SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`;
observed native code is `02985de5c6218c3968a45fa5b5cdc4bf4be850a8d87d92520c6e184098518af4`.
These are bounded prepared-call proofs of logic effects, not full-frame pixel reconstruction
at every view. The provider has not yet been extended by this evidence commit. Existing
structure/projectile/shake restrictions remain separate. No callbacks or new default
behavior are introduced.

The interrupted batch log remains preserved. The recovered native files are immutable;
fresh reruns use separate output files. Recovery of the CAVE guard, glyph-enabled calls,
real P7 origins and S1 result/objectives composition proceeds in subsequent validated steps.
