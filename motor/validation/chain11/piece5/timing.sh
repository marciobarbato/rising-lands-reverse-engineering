#!/bin/sh
set -eu
for probe in K1 P3 P6 P7 S1; do
 case "$probe" in K1) frames=501;; P3) frames=3001;; P6) frames=2272;; P7) frames=3572;; S1) frames=3722;; esac
 RL_REFERENCE_PROFILE=chain11 python3 -B motor/testes/probe_benchmark.py --probe "$probe" --frames "$frames" --output ".local/chain11/timing-$probe.json"
done
RL_REFERENCE_PROFILE=chain11 python3 -B - <<'PY'
import json,sys
from pathlib import Path
sys.path.insert(0,'motor/testes')
from probe_benchmark import run
native=json.load(open('.local/chain11/S1-native.json'));frames=native['frames_equal']
assert native['first_difference']is None and frames>=3722
result=run('S1',frames,'motor/target/release/librising_engine.dylib')
Path('.local/chain11/timing-S1-extended.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print({k:result[k]for k in ('frames','logic_mean_ms','max_ms','stop')})
assert result['stop']is None and result['max_ms']<=4
PY
RL_REFERENCE_PROFILE=logic python3 -B motor/testes/play_benchmark.py --library motor/target/release/librising_engine.dylib --frames 9200 --mode 1 --output .local/chain11/timing-M2.json
