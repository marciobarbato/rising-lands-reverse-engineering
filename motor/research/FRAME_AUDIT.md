# Frame migration audit and evidence contract

Workstream D stage 2 translates the accepted Python frame composition. The
only original oracle is intact RISING.EXE SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Python routines, original captures and published masks remain read-only. No
acceptance decision is made by this port.

## Starting state and comparison domain

The production proof starts from the display-scenario `-v2` MissionLoad final
state, expanded against its declared entry artifact. This is the accepted M1
state with the backend required by the accepted M2 display scenario. It has
25,343 live blocks before the load tail. MenuInit frees 146 bank blocks, leaving
25,197. The record set retains all 25,482 historical allocation records.

The chain is one Rust world: load_tail (including frame 0), between_frames(1),
frame(1), and optionally successive pairs through frame 128. Expected states
are independently replayed from committed original deltas. They are never
loaded into the Rust world after its initial state. The harness verifies replay
summaries and full-state checkpoints before comparison.

The M2.1 policy excludes exactly 78,093 display-only bytes in 8,780 ranges.
The M2.2 cumulative policy excludes exactly 153,060 display-only bytes in 4,948
ranges. The harness uses their unchanged address masks and compares every
remaining byte, including untouched state. The 776 and 999 logic-byte figures
refer to the policies' observed changed-byte classification; the phase proof
compares approximately 16 MB, not only those changed bytes.

Surfaces and pixels are outside this port. Shared permutation cursor
`0x4e1d18`, world RNG `0x497164`, AI RNG `0x498db4`, CRT seed reached through
`[0x522244]+12`, and the HUD flag `0x4e05a2` remain logic-visible. A display-only
routine may be omitted only under the accepted provider's guarded contract.
Unknown logic paths must produce the original routine name/address error.

## ABI observation and ownership

The additive frame ABI uses copied 72-byte input/event structures. Explicit
inputs are cursor coordinates, offscreen surface address, eight entry registers,
three saved ProgIteration words and four MSG words. The no-input scenario uses
cursor `(0,0)`, saved `(0,0,0)`, MSG `(0x3000000,0,0,0)`, no async key and no
queued Windows message. These are declared scenario answers, not game defaults.
A completed load-tail frame 0 and each later frame body advance one virtual
tick; the between-frames phase does not.

The bulk projection is a count followed by repeated little-endian
`(u32 address,u32 length,bytes)` records. The same format exposes actual bytes
at each free, before release. The harness reconstructs the adopted allocator's
record transitions from Rust's ordered GlobalHandle/GlobalUnlock/GlobalFree
observations, hashes the actual freed Rust bytes, and compares complete final
records excluding only the accepted call-site metadata fields. Missing or
unmatched free records fail the proof.

Bindings and boundaries are compared outside the accepted static display
context classification. Shared issuers must match in order. MCICD caller stack
locals remain unknown exactly as the accepted proof declares; known stack words,
guards, argument widths, return sites, boundary registers and between-frames
registers are compared. The frame-body return EAX remains unmodeled as in M2.2.

## Harness provenance and rejection checks

`frame_evidence.py` mechanically copies only pure replay/mask/comparison helper
definitions from the accepted Python comparison scripts. This avoids importing
the x86 bench into an offline comparison. A test compares their complete ASTs
with the unchanged originals. It does not copy or emulate game behavior.
`frame_differential.py` pins the original input artifacts, masks and helper
sources by full SHA-256 and refuses to overwrite reports. `OriginalImage`
checks the intact executable identity before its static issuer graph is used.
No original execution is needed to replay the committed evidence.

Fast harness tests validate C layout, strict bulk decoding, exact helper
identity, reference pins and rejection of an altered actual compared byte. Every compared phase also mutates
an actual returned binding result and boundary register and requires rejection.
Reports preserve the library hash and engine source hashes before/after the run.
A malformed or unknown observation fails explicitly. State-only diagnostic
runs are marked incomplete and cannot return a complete-proof verdict.

Commands (wrap game runs in the machine's heavy lease):

```sh
python3 -B motor/testes/test_frame_evidence.py
python3 -B motor/testes/frame_differential.py --output .local/engine-frame1-new.json
python3 -B motor/testes/frame_differential.py --m22 --frames 128 \
  --output .local/engine-frames128-new.json
```

Timing reports include only synchronous Rust phase execution, excluding corpus
replay, projection copies and Python comparison. They cover load tail and the
between-frame logic effects along with frame bodies. They are not renderer or
end-to-end app throughput measurements. Actual proof results and remaining
routine boundaries belong in the stage handoff after execution.
