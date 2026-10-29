# Rust engine pilot handoff

Workstream D owns motor/ and docs/ENGINE.md on feat/codex-rust-engine in the
independent Rising-Lands-Codex-Engine clone. No other front was edited; no
merge into or push to main is performed. This is a pilot, not a frame engine or milestone.

The original-first audit was committed separately as b7dfcdd. The five routines
are Random 0x4704dc, LongRand 0x45841b/CRT rand 0x48c51d, IntToBCD 0x467cd1,
and BCDToInt 0x467d3a. Original executable identity is
6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb.
Existing captures and Python references are read-only, SHA pinned; no original
emulation or asset copy is required. See the [audit](research/PILOT_AUDIT.md).

The core uses semantic RNG/BCD values, a checked sparse original-address
projection with explicit load/project and opaque uninterpreted bytes, integer
virtual ticks and explicit wrapping arithmetic. The registry-based C ABI 1.0
uses copied caller buffers, typed seven-data-GPR calls, opaque u64 handles,
transactional publication and named failures. The C header and Swift CLI smoke
are in include/ and testes/. The full API/limits/versioning and reproduction
commands are in [ENGINE](../docs/ENGINE.md).

The differential requires every selected captured call: Random 24, LongRand 12,
rand 12, IntToBCD 19, BCDToInt 8, total 75 records. Nested LongRand/rand observations
are counted separately. It compares every declared byte, changed-byte triples,
seven data GPRs and 48 captured RNG transitions against original and unchanged
Python. Python BCD providers are void; their separate scratch-register adapter
is grounded in the static original review, not a Python return value. Caller
stack writes are included without filling unobserved bytes. Synthetic aliasing,
u16 round-trip, wrapping and ABI error tests do not extend native-capture claims.

Remaining work: full world/frame initialization and orchestration, actual
frame-step/input ABI, generation-stable memory/render snapshots and lifetimes,
indexed 800x600 output/palette convention, native library loading/signing and
bundling, timing calibration, later original-asset packaging, and whether a
shipped app keeps Python. The pilot default 20Hz is pacing policy only. The
current macOS live apply_frame remains reserved; the app was not changed.
Projectiles and Rust rendering are deliberately outside this pilot.

## Validated delivery

Latest fetched/merged main is `a7427fd0e416d212f08af7f0df3d36a224d12f2d`;
ancestry was checked before and after validation. Original-first research:
`b7dfcdd1ad9a72cd6816c3c4ac34efd981028d0e`. Implementation and tested code:
`347383f22ad27709476c1ea5c29063eaaf8351eb`. The subsequent documentation/
evidence commit adds these results without changing executable code.

`./motor/validate.sh` passes: rustfmt; Clippy with -D warnings; **15 Rust tests,
16 Python tests, zero failures/ignores/skips**; **75 captured records with zero
mismatches**, including 48 explicit RNG checks. The C11 header layout check
and an actual Swift 6.4→C ABI→Rust CLI run pass. The latter creates/frees a
world, copies a seed, draws 16807, checks projected bytes and advances the
virtual clock to 1000ms. No app files or runtime were modified.

Toolchain: **rustc 1.99.1 (58cf8f9c3,2026-10-13), cargo 1.99.1**, target
**aarch64-apple-darwin**, LLVM 23.1.1, Apple Swift 6.4. Rustup stable and
format/lint components were installed only into clone-local ignored .local/;
no shared runtime or shell configuration was changed. To repeat with a normal
rustup installation, run the manual's commands. For this isolated installation:

```sh
export CARGO_HOME="$PWD/.local/cargo"
export RUSTUP_HOME="$PWD/.local/rustup"
export PATH="$CARGO_HOME/bin:$PATH"
./motor/validate.sh
```

[Structured summary](validation/pilot-summary.json),
[all 75 call records](validation/pilot-differential.json),
[full validation log](validation/pilot-validation.log) and
[toolchain](validation/toolchain.log) preserve exact results and identities.
Generated dylib/CLI remain under ignored motor/target; their sizes/hashes are
recorded in the summary. The crate workspace has no external dependencies.
Reference source/capture hashes must still match; an upstream change requires
an explicit audit and pin update rather than silent acceptance.

No projectile port, rendering, full-frame delivery, performance claim or new
original emulation is included. The existing macOS apply_frame remains
RuntimeContractPending. The coordinator reviews/integrates the feature branch;
no merge into or push to main was performed.
