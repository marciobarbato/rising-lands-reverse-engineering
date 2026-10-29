# Rust frame migration: original 0–9,200 window

This stage extends workstream D's bounded Rust logic port. Project acceptance
belongs to the coordinator. The executable remains intact `RISING.EXE`, SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Original media, Python providers, captures, policies and the earlier engine
proof harness are read-only inputs to this stage.

## Evidence and package identities

Missions Stage21 captured frames 0–9,200 in ten compressed packages:
`pesquisas-paralelas/missoes/evidencias/m2-3/`. Their manifest SHA-256 is
`e88dc3fcaca11d03a774dad8bd9c768345f13c884cc2d8df493107ec9d180b09`.
It pins every package's compressed and raw identities, frame interval and phase
count. The comparison policy SHA-256 is
`384f985bea05137197ea22b3439f96db2f1e6b9a6d8b1a6c986f4955697fc21e`.
The cumulative mask excludes exactly 153,060 display-only bytes; 1,560 observed
changed bytes are logic-visible. The proof compares all unmasked state bytes,
including unchanged bytes, in **18,401 phases**.

Every package has a complete opening state with full, compared and masked
hashes; the next opening's three hashes must equal the previous package's
final three hashes. Each phase carries complete deltas plus the same hashes.
Full checkpoints also follow frames 8,999, 9,000 and 9,176. The final package
carries all 25,482 allocation records. Surface pixels remain out of scope.

`frame_long_evidence.py` independently pins this stage's reviewed reference
sources. It reuses the earlier pure offline comparison helpers without editing
them. Loading the original image is for immutable data tables and the accepted
static classification of event issuers; this harness never executes x86.
The runtime-resolved original RULE instructions already reside at DGROUP
`0x514910`, with task entries at `0x51a720`. No alternative RUL parser or
invented program is supplied. The four original jump-table inputs remain
explicit and immutable.

## Three distinct validation scopes

1. **Complete phase proof from declared openings.** Each package starts one
   Rust world from its explicit original opening state, then advances through
   every phase without another reference reload. The aggregate requires all
   ten whole packages and exactly 18,401 equal phases. Reports from a changed
   or dirty checkout, different libraries/sources, partial diagnostic windows,
   different policies or broken package chains cannot establish the aggregate.
2. **Serial phase proof.** `--serial` starts package 0 from accepted M1 S0 and
   carries actual Rust bytes, registers, saved words, host-input declarations,
   allocator records and virtual ticks through hashed continuation checkpoints.
   Each later invocation loads the previous Rust checkpoint, never the later
   original opening state. The serial aggregate additionally checks every
   actual continuation SHA-256 link. Splitting at package boundaries keeps each
   heavy-lease job below the machine's approximately twenty-minute limit.
3. **Serial throughput supplement.** `frame_long_benchmark.py` starts once at
   accepted M1 S0, runs load_tail plus all 9,200 phase pairs in that same world,
   and checks the final projected state/RNGs/clock/records against the independently
   replayed original frame 9,200. No snapshot export or Python comparison occurs
   during the timed phase-pair loop. This is an endpoint and performance check;
   it explicitly cannot claim the 18,401-phase proof.

`--start-frame 8999` and `--start-frame 9176` are separate bounded diagnostics.
The harness verifies the preceding original deltas, takes that explicit
checkpoint as input and compares only following phases. Such reports cannot
be aggregated as whole packages. Their purpose is locating unported raid and
path-search callees quickly while the full earlier window is validated.

## State, observations and allocation order

Per phase, the checker verifies the exact cumulative-mask state and
`compared_summary`, RNGs, immutable original tables, bindings and boundaries
outside display context, carried/returned registers, and virtual-tick behavior.
It mutates actual returned binding/boundary values and requires rejection.
Loading/projecting each opening must preserve every declared byte; altering
an actual projected compared byte must also fail comparison.

The 25,482 allocation records are adopted from the accepted M1/post-load
records. The package verifier proves that only load_tail has allocator binding
or allocation/release activity (146 releases and 584 bindings). Record count
stays 25,482 throughout. A later checkpoint uses the published post-load
records only under that checked invariant; the final package's complete
records must agree. Load-tail frees are updated from Rust's ordered binding
observations and its actual retained freed bytes, including the bank-header
count store before release. Call-site metadata exclusions remain exactly the
accepted `caller_return`, `stack` and `freed_caller_return` fields.

MCICD uninitialized frame-body stack words, EFLAGS/EIP and CalculGame return
EAX retain the earlier published exclusions. No empty callback or fabricated
answer replaces an unknown logic callee. The no-input host answers, MSG/saved
words, cursor and original offscreen address are declared scenario inputs.

## Reproduction

Wrap each `verify`, `part` or benchmark command in the shared heavy lease;
use an exclusive lease for the performance result. Set `RL_ORIGINAL_EXE` to the
read-only intact executable and `RL_LIBRARY` to the built release library.
All report/checkpoint paths below must be new. Compressed `.json.xz` reports
are supported; the harness refuses to overwrite any evidence.

```sh
python3 -B motor/testes/test_frame_long.py
python3 -B motor/testes/frame_long_differential.py verify \
  --output .local/engine-long-plan.json
python3 -B motor/testes/frame_long_differential.py part --part 0 \
  --output .local/engine-long-part00.json.xz
# Repeat part 1..9 as separate bounded lease jobs.
python3 -B motor/testes/frame_long_differential.py aggregate \
  --plan .local/engine-long-plan.json \
  --reports .local/engine-long-part{00,01,02,03,04,05,06,07,08,09}.json.xz \
  --output .local/engine-long-proof.json
```

For the independently serial phase proof, add `--serial` to each part. Package
0 writes `--checkpoint-out .local/engine-serial00.json.xz`; package 1 takes
`--resume .local/engine-serial00.json.xz` and writes its next checkpoint, and
so on. Add `--serial` to the final aggregate. These checkpoints are local
verification state, not game save files or a new app API. The same commands
can run on the Mac mini if exporting/comparing every phase is too slow here.

```sh
python3 -B motor/testes/frame_long_differential.py part --part 9 \
  --start-frame 8999 --max-phases 4 --output .local/engine-raid-diagnostic.json
python3 -B motor/testes/frame_long_benchmark.py \
  --output .local/engine-serial9200-benchmark.json
```

Reports include actual library/profile/source hashes, source stability and git
identity, exact first stop/divergence, compared byte counts and mismatches,
phase coverage and timed C ABI execution. Timing includes private projection
and semantic-state reload, but excludes rendering and exported-snapshot
comparison. Actual validation results belong in the delivery handoff after
these commands run; this document does not turn a prepared harness into a pass.
