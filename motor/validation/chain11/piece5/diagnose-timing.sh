#!/bin/sh
set -eu
python3 -B .local/chain11/diagnose-timing.py
RL_REFERENCE_PROFILE=chain11 python3 -B motor/testes/probe_benchmark.py --probe S1 --frames 10672 --library motor/target/release/librising_engine.dylib --output .local/chain11/timing-S1-clean.json
RL_REFERENCE_PROFILE=logic python3 -B motor/testes/play_benchmark.py --library motor/target/release/librising_engine.dylib --frames 9200 --mode 1 --output .local/chain11/timing-M2.json
