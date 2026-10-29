# MONDE01 facade readiness inventory — 2026-10-28

Light static review only, under the resumed Codex authorization. Baseline:
`b610bfad77ffadaa0ee5f6af02160d786ccfdc7b`. No implementation, native capture,
Ghidra session, domain gate or integration was started in this inventory.
The coordinator subsequently limited this recovery round to preserving these
notes; further graphics work needs another scheduled round.

## Four distinct states

| Scope | Implementation | Original validation | Main integration | Complete-flow test |
|---|---|---|---|---|
| Stage 16 cache lifecycle | Existing provider | Historical original captures and differential validation; not rerun here | Already integrated | No complete mission |
| Stage 17 AffGame prefix to HUD checkpoint | Existing bounded provider | Historical six complete synthetic frames and three named stops; not rerun here | `7eff798b77cc694a6def54a4d5311883651005c9`, pinned-input correction `d483dec37b62b570867a4777ca1763ad7c1aa93c`, merge `07560625beb22daafd338937482f2694bc2e39ad`; all freshly checked ancestors of fetched main | Pinned pre-structure checkpoint only; M1/M2/M3 unaccepted |
| Next facade/lookup extension | Not implemented | Fresh static byte/hash review only; no new x86 comparison | This inventory is local documentation only | Not run |

The historical graphics domain result is 192 tests, zero skips. It is not a
fresh result from this recovery. No test was skipped in place of new validation:
native validation and domain checks were **not run** because no heavy slot was
granted. Fresh checks here cover original identity, exact interval hashes,
every pinned checkpoint buffer hash, Git ancestry and documentation whitespace.

## The first pinned stop has no structure lookup result

The unchanged `monde01-checkpoint-quadro.json` records checkout
`7e18ad00cdc39788726880b16422b13405ff3e6e` and compressed-file SHA-256
`540470d253b74ecc9131c64045ebe21e4df79fc1bf39f88d68f4979fce2a0f2f`.
Fresh read-only decompression verified every manifest buffer hash. At cell
3345 `(17,13)`: terrain is `0x2ED`, region/occupancy word is `0x0001`, discovery
camera 0 is zero and light camera 0 is zero. The checkpoint precedes the
structure placement scan. `cena_monde01` separately declares a synthetic zero
276,000-byte structure pool, absent from `MundoQuadro`'s current inputs.

The model currently stops on the terrain trigger at `0x40F23B`. Static original
flow sends `0x2ED` to `0x408577`. That branch checks occupancy bit 15 and computes
`(word & 0x7FE0) >> 5` only when set; otherwise its result is `0xFFFF`. At
`0x4085BF..0x4085C5`, a missing result jumps directly to `0x40F491`, without
entering the facade, workshop or later indicators. Thus this pinned trigger is
not evidence of a drawn Santuário. A future extension must distinguish this
missing-structure path from the real placed structure. Do not fabricate
occupancy, install a record to satisfy the trigger, or overwrite the old pin.

## Smallest future slice, pending scheduling

1. Capture original-only missing/present lookup and occupied-prefix behavior
   before translation. `ChercheIndiceBatiment 0x41B54A` consumes AX (u16 cell),
   preserves EDX, and returns the same bit-15/index rule. It can decode indices
   0..1023; records 1000..1023 exceed the actual pool and need an explicit
   protected boundary rather than an invented normalization.
2. Add explicit inherited structure input (1000 records of **276** bytes), not
   the 204-byte serialized record size. The prefix `0x407DEF..0x407E56` checks
   mode `+5`, owner `+4` and the per-camera visibility byte at `+0x110+camera`
   before discovery/SaveCurrentClipping. Preserve that ordering and early exit.
3. Reuse the committed seven-layer `construcoes.consultar_santuario` /
   `compor_fachada` only within its proven type-2, mode-5, inhabited, auxiliary
   `+6 == 0` domain. It is a facade provider, not a complete AffBatiments caller.
   The original caller also invokes `BatimentGetEtat 0x41A8E5` before mode/body
   selection and may execute later workshop/selection/gauge paths. Do not erase
   that query or its failure boundary because the mode-5 body ignores its value.
4. Consume economy's committed `construcoes_habitaveis.estrutura_habitada`
   contract for `BatimentEstHabiter`; no duplicated Bag logic or unconditional
   inhabited flag. Selection index `0x496AC4`, per-owner structure selection
   words `0x495BE0`, camera and all three drawing clocks must be inherited.
   Uncovered overlays, owners, effects and gray rendering remain named stops.
5. Compare standalone caller effects, clip save/restore and actual return, then
   new whole-frame buffers over explicitly declared snapshots. Reproduce the
   old checkpoint unchanged. A later complete-M1 snapshot is a new capture with
   its own provenance. Unit `+0x74 == 0` overlays and types 1/8 remain subsequent
   stops, with no implementation in this round. Broader viewport work is lower
   priority unless an actual checkpoint needs it.

The facade branch does its own inline lookup, so a ChercheIndiceBatiment call
trace alone cannot establish that branch's behavior. Observe both paths.

## Fresh static original identities

The intact execution oracle remains
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
`imagem_pe()` verified that identity before the following reads. The normalized
analysis PE `26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0`
was not used in this review. Intervals are half-open; static evidence is not a
new native capture.

| Interval | SHA-256 |
|---|---|
| Prefix `0x407DD3..0x407E85` | `2f0cff11144db2c4384bbb7109387fc2ad2c5d2ff2867405a2713a6b22485b09` |
| Inline lookup `0x408577..0x408619` | `e46dd6ef7a10153b1c85d9e018ac19fe35430d58c2cf50dcb00ea86bd20b9533` |
| Habitation/layers `0x40873A..0x40892D` | `a50ee64368de70b195c5651226d18250dfcfee2f79c6ec5856a5a24853b805c6` |
| Auxiliary guard `0x408AB3..0x408AC8` | `00949d6e165b7241f5bb3237f7fc1e49f3011a4fe58f7ead8c807adfd9b5f632` |
| Switch/tail `0x40F23B..0x40F49C` | `d8fa5152f721bb2508f0ca9d72351045d1b040d9ab9bd4738aa78e3b9e4d4fa7` |
| Lookup function `0x41B54A..0x41B579` | `9d9a454a4a9684e367f7904d815e18ce500499edbcd43bf850fbcd3fc8f4b9cb` |
| Habitation predicate `0x41A5B8..0x41A61C` | `8db6619013ef9a6ed8f6b8bb53cac82fb4752b1ff95e62d2b61531dfe28a67b1` |
| State query `0x41A8E5..0x41A940` | `3adb65e8bedb386247012b8f14d02553aff01a2be629841aaf65a83856047968` |

Existing [AffBatiments assembly](evidencias/00407dd3.asm),
[lookup assembly](evidencias/0041b54a.asm),
[pinned manifest](evidencias/monde01-checkpoint-quadro.json) and
[stage-17 frame contract](../../docs/GRAPHICS.md#in-game-frame-orchestration-affgame--seventeenth-continuation-stage)
remain unchanged. Main integration, new native proof and real-mission acceptance
are not claimed by this inventory. The overall estimate remains coordinator-owned.
