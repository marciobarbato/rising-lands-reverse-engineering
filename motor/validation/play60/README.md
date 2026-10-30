# Sustained native play proof

All native jobs were individually run through the shared `heavy_lease.py`, with
1,140-second child timeouts. Benchmark jobs additionally used `--exclusive`.
The per-job `*-run.json` files give the exact child commands and elapsed time
after lease grant. Queue time is excluded. Source/library hashes and execution
policies are in each proof. The source revision in a benchmark identifies its
harness; `before-final` loads the preserved ABI1.5 baseline library, SHA-256
7070b80561c84bc36cb3b4543f2a25d2e20bc8c6dc4318b754f1a73e159c38b2,
from bbf1638. It can be rebuilt from that revision with `cargo build --manifest-path motor/Cargo.toml --release --locked`.
No native binary or asset payload is part of this report.

Reproduction (from the feature checkout; wrap each command in the lease):

```sh
sh motor/validate.sh
python3 -B scripts/check.py
RL_EXECUTION_MODE=2 python3 -B motor/testes/frame_differential.py --frames 128 --m22 --library motor/target/release/librising_engine.dylib --output .local/m22-new.json
python3 -B motor/testes/frame_long_differential.py verify --output .local/m23-new-plan.json
# Run i=0..9 as separate bounded jobs, then aggregate the ten reports.
RL_EXECUTION_MODE=2 RL_COMPARE_PLAY=1 python3 -B motor/testes/frame_long_differential.py part --part 0 --library motor/target/release/librising_engine.dylib --output .local/m23-new-part0.json.xz
RL_EXECUTION_MODE=2 RL_COMPARE_PLAY=1 python3 -B motor/testes/player_proof.py --probe P1 --python --whole-state --library motor/target/release/librising_engine.dylib --output .local/P1-new.json
# Repeat P2/P6 with --whole-state; P3/P7/K1 without that option.
RL_EXECUTION_MODE=2 python3 -B motor/testes/render_proof.py --frames 128 --library motor/target/release/librising_engine.dylib --output .local/render128-new.json
RL_EXECUTION_MODE=1 python3 -B motor/testes/render_proof.py --frames 9200 --no-python --library motor/target/release/librising_engine.dylib --output .local/render9200-new.json
python3 -B motor/testes/player_leaf_proof.py --output .local/leaf-new.json
python3 -B motor/testes/play_benchmark.py --library motor/target/release/librising_engine.dylib --mode 1 --frames 9200 --output .local/play-new.json
```

Timing excludes initialization, proof/export/hash work and app presentation.
Graphics remains the pinned 1.7 contract. Production glyph stops and the old
input composition dependencies remain; see `summary.json` for exact coverage.
The first merged-tree gate failure is retained as `validate-final.log.gz`;
`validate-final2.log.gz` is the passing frozen-phase-proof run after the initial fixes.
`final-main-validate.log.gz` and `final-main-common.log.gz` are the final gates
after merging main `54d148d` and adopting its coordinator input-pin verifier.
Native source/header/library bytes and every frozen evidence digest are identical;
`post-merge-identity.json` records this check. Preview and interrupted jobs are not proof claims.
