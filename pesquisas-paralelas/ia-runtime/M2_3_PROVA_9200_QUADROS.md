# M2.3 — 9,200-frame equality proof (AI/runtime)

Main `5f4052c` (Missions' M2.3 evidence, `de154b5`). Proof file: [validacao/m2-3-prova-9200-quadros.json](validacao/m2-3-prova-9200-quadros.json), produced by [provar_quadros_9200_ia.py](provar_quadros_9200_ia.py) from clean revision `8a5787d`. Python only; the native side is Missions' committed capture. Intact `RISING.EXE` `6c556520…43fb`. M2.3 acceptance is the coordinator's decision.

The window is frames 0–9,200 (18,401 phases). It covers the first scripted raid: the spawn at frame 9000 and the first path search at 9176–9179.

## Reproduction

One command, on a clean tree:

```
python3 -B pesquisas-paralelas/ia-runtime/provar_quadros_9200_ia.py tudo --paralelo 4 \
    --lease <path>/heavy_lease.py \
    --saida pesquisas-paralelas/ia-runtime/validacao/m2-3-prova-9200-quadros.json
```

- `--lease` is optional; with it, each part takes one heavy-lease slot.
- Step by step (the parts can run in any order, in parallel):
  - `provar_quadros_9200_ia.py parte N` for N = 0..9; each writes `.local/m2-3/prova-<revision>/parteNN.json`;
  - `provar_quadros_9200_ia.py agregar --saida <proof.json>`.
- `agregar` accepts only reports from the current clean revision, each equal and covering its whole part. A proof that is not accepted goes under `.local/`.
- Each part report carries `phase_chain_sha256`: a hash over every phase's Python compared summary, both RNGs and the allocation count. Two machines that run the same part must produce the same chain.

## Reference and policy

| Input | File | SHA-256 |
|---|---|---|
| Manifest (pinned in the script) | `pesquisas-paralelas/missoes/evidencias/m2-3/captura-quadros9200-monde01-exibicao-v2.manifest.json` | `e88dc3fc…0b09` |
| Parts 00–09 (xz) | `…/m2-3/captura-quadros9200-monde01-exibicao-v2.parteNN.json.xz` | pinned in the manifest (xz and raw JSON) |
| Policy | `pesquisas-paralelas/missoes/validacao/m2-3-politica-comparacao-9200-quadros.json` (cumulative mask: 153,060 display-only bytes; 1,560 logic bytes) | `384f985b…fc21e` |
| `-v2` scenario | MissionLoad input and capture, frame-1 capture | in the proof file |

**Capture checks before and during the comparison:**
- `agregar` re-checks the manifest: each part's xz and raw hashes, and the hash chain between parts (`partes_quadros_ia.verificar`).
- Each part's opening full state matches its own summary, compared summary and masked hash. Part 00 opens with the `-v2` MissionLoad final state.
- Every phase is replayed from its deltas. Its summary, compared summary and masked hash all match (18,401/18,401).
- The full states after frames 8999, 9000 and 9176 equal the replay.

## Result: equal in all 18,401 phases, with zero crossings

Each part runs from its opening state on ONE map, in mode 'prova'. Part 00 starts at load_tail; the others start from their checkpoint.

| Check (every phase) | Result |
|---|---|
| Compared state bytes (outside the cumulative mask) | **16,022,275 equal** in every phase (294,825,882,275 byte comparisons) |
| Python compared summary = the reference's | 18,401/18,401 |
| RNGs `0x497164`/`0x498db4` | 18,401/18,401 |
| Bindings outside display context | 18,401/18,401 phases (138,597 events) |
| Boundaries outside display context | 18,401/18,401 phases (27,603 events) |
| Allocation-record count | 25,482, 18,401/18,401 |
| Between-frames exit registers (8) | 9,200/9,200 |
| Carried entry registers | 9,191/9,191 (each part's first between-frames phase starts from declared registers) |
| HUD flag `0x4e05a2` | 9,200/9,200 |
| Final allocation records (part 09) | 25,482 equal |

**Crossings: 0. Crossings writing compared bytes: 0.** These are measured per part, not assumed. Mode 'prova' carries no crossing data, so any crossing would stop the part. There were no Core provider stops either.

**At frame 9200:** counter 9200, world RNG `0x128b8024`, AI RNG `0x3212b7ce`. The proof file keeps the full records for frames 8999–9000 and 9176–9179, and for frame 9200.

## Allocation records

No phase in the run allocates or releases a block, and the count is 25,482 in every phase.
- **Part 00:** starts from the `-v2` MissionLoad records.
- **Parts 01–09:** open with the `-v2` final records, a declared input.
- **Check:** part 09's final records are compared in full and are equal. The opening input is therefore the original's at the end of the run.

## Per-part timing

This MacBook (arm64, Python 3.9.6), `--paralelo 4` under the heavy lease, with other agents running:

| Part | Frames | Phases | Seconds | Peak RSS |
|---|---|---|---|---|
| 00 | 0–1000 | 2,001 | 481.7 | 1.2 GB |
| 01 | 1001–2000 | 2,000 | 482.1 | 1.1 GB |
| 02 | 2001–3000 | 2,000 | 482.4 | 1.1 GB |
| 03 | 3001–4000 | 2,000 | 484.9 | 1.1 GB |
| 04 | 4001–5000 | 2,000 | 486.8 | 1.1 GB |
| 05 | 5001–6000 | 2,000 | 487.4 | 1.0 GB |
| 06 | 6001–7000 | 2,000 | 484.3 | 1.1 GB |
| 07 | 7001–8000 | 2,000 | 478.6 | 1.1 GB |
| 08 | 8001–8990 | 1,980 | 462.1 | 1.1 GB |
| 09 | 8991–9200 | 420 | 121.5 | 2.2 GB |

Total wall clock: 1,432.5 s (sum of the parts 4,451.8 s).

**Phase chains** (`phase_chain_sha256`, the values to match on a second machine). An earlier diagnostic run of all ten parts gave the same ten chains; it ran on the uncommitted driver, so it is not evidence.

| Part | Chain |
|---|---|
| 00 | `9903ccd49ed9e4170098ed5cc29b1dcd35f8fefc3317401bd9bedc386675d2eb` |
| 01 | `a4f633206ab300324e2281202f46bcd0d12779d99523b8d28433766559882649` |
| 02 | `5660d4038a5a139dac18d78f55037f29c6f34f819cd23c351aad86733dfb2f0b` |
| 03 | `1fe202a1b49cde49f68b0f21f185540d50447af776fddba2fdcafead94a007fe` |
| 04 | `c518c4da4330fc3ecc131c94b733b8728e85d8b217d9d5ad00ecd4e0b9ad5ff8` |
| 05 | `bd938e40f1ef251718b72d8b1527ba12f23fba534f9c5a9a3aae49f90e850c5c` |
| 06 | `3b8418826cc81e824d111e56606d287c181d8868e60f5f73ae2159280e883e28` |
| 07 | `71b5139e7af171d5df771731faf86226ab0506d7f325d6a9085d269cd63f383b` |
| 08 | `34d69394bb5f8e9b3d5b16ab1313499deff037f08b8a391d9c1658b6dca31206` |
| 09 | `eb171e7d8b6e0c9385ceccba8bc789be49d9e4cef7b81bf46e021f76aeafa164` |

## Compared bytes with a display writer

The same five bytes as in M2.2:
- the HUD flag `0x4e05a2` (AffGame modeled; CalculMatiere is Economy's provider);
- the clip words `0x49a01e/1f` and `0x49a022/23`. RestaureClipping restores them, and SetClipping is Core's provider.

All five are equal at every phase end.

## Unmodeled, stated explicitly

Same as M2.2, plus the part openings:
- The MCICD_Play stack words in the frame bodies, EFLAGS and EIP.
- Bindings and boundaries inside policy display roots. They are counted per phase in `phase_table`: 58,904 display-context bindings and 2 boundaries in all.
- The masked display-only state and the surfaces.
- ProgIteration's saved words and the MSG buffer: declared, and checked through the exit registers.
- Allocation-record call-site metadata, and CalculGame's return EAX.
- **At each part opening after part 00:** the opening full state, the allocation records and the between-frames entry registers are declared inputs from the capture. The state is proven against the previous part's end hashes, and the records against part 09's final list.

## Proof file layout

- `equality`: per-check counts.
- `phase_table`: run-length encoded by frame. Each run is `[first_frame, last_frame, frames, between_frames_row, frame_row]` over `columns`, and `load_tail` has its own row.
- `phases`: full records for the raid frames.
- `parts`: per part, the result, opening checks, crossings, phase chain, timing and the SHA-256 of its report.
- `code_sha256`: every repository source file the parts imported.
- `evidence_sha256`: the manifest, parts, policy, `-v2` scenario, EXE and SBL.
