# S1 M3.2 render windows — Graphics 1.10

The original S1 input/capture is revision `82ec5eaa98d4f212b650c2c8ce2b293a30fb50ef`.
The census includes every gameplay input record and 200 following frames. The result
confirmation is a separate screen proof. No foreign implementation-file hash is pinned.

| Window | Inclusive gameplay frames | Required full 800×600 surfaces |
|---|---|---:|
| 1 | 130–403 | 274 |
| 2 | 1820–2383 | 564 |
| 3 | 2400–2878 | 479 |
| 4 | 3110–3508 | 399 |
| 5 | 3730–4080 | 351 |
| 6 | 4170–4623 | 454 |
| 7 | 4820–5090 | 271 |
| Total | Seven windows | 2,792 |

The final current-source report passes **2,792/2,792** required surfaces and all
**3,906/3,906** captured frame instances, **319,948** raster calls and **2,019**
strict text boundaries, with no mismatch or render/logic stop. The domain gate
passes **298 tests**, zero failures or skips (192.738 s). P3/P6/P7 regression passes
3,001/3,001, 2,272/2,272 and 3,572/3,572 on the same Graphics 1.10 source.

`evidencias/s1-render-window-inventory.json` records all 19 S1 view origins, structure
modes and the explicitly partial tracked-unit metadata. All 19 origins are already
proved for AffGame and RestoreAll. The native render captures, rather than that partial
metadata, supply the full 800-unit/1,000-structure census.

The declared original probe boundary is retained: AffText/TextGetMessage do not execute
their bodies. Python supplies the strict recorded adapter only after checking every
argument and the full incoming surface. A glyph-enabled trajectory is not claimed.
Each native invocation verifies its opening checkpoint, every subsequent complete
state and both phase surfaces against the published original S1 record. Each Python
capture starts from its actual native surface/cache and carries Python outputs through
consecutive rows/transport parts. Independent or overlapping native prefixes remain
explicit; this is not a reconstructed whole-state simulation or full-mission acceptance.

## Replaying the committed Graphics proof

Run from this Graphics worktree. This is Python-only; it does not execute the oracle.
The capture set keeps the required ordering across transport partitions.

```sh
python3 -B - <<'PY'
import json, sys
from pathlib import Path
sys.path.insert(0, 'pesquisas-paralelas/graficos-animacao')
from validar_janelas_s1_graficos import validar, AQUI
names = json.loads((AQUI/'validacao/s1-render-capture-set.json').read_text())['captures']
result = validar([AQUI/'evidencias'/name for name in names])
Path('.local/s1-render-reproduction.json').write_text(json.dumps(result, indent=1) + '\n')
print([(w['frames'], w['equal'], w['expected']) for w in result['windows']])
assert result['equal_surfaces'] == result['expected_surfaces'] == 2792
assert all(c['first_difference'] is None for c in result['captures'])
PY
python3 -B scripts/check.py --domain graphics
```

The original new native archives are unchanged in `.local/s1-native-archives/`; transport
parts copy rows and encoded pixel payloads verbatim. `*.partitions.json` ledgers retain
parent hashes/manifests and verify every part. No historical evidence was replaced.

## Exact Mac-mini original reproduction commands

Run **after delivery**, in a prepared Graphics worktree at the delivered revision, with
read-only original inputs and `.local/python` linked as in the repository workflow.
Do not switch the mini's Missions checkout or write its snapshots. Its documented
canonical checkout is `$HOME/git/Rising Lands`; the input paths below are its existing
M3 frame-128 and S1 pass-2 snapshots. Fetch the public repository over HTTPS when setting
up that separate worktree. The coordinator owns dispatch and any `runs/graphics/*` push.

These seven original runs are sequential and individually bounded below 20 minutes.
Each has its own leased process and the observer's whole-invocation 19-minute alarm.
The first snapshot directory/output directory must be new, preventing old results or
checkpoints from being overwritten. Full pass-2 capture/proof jobs longer than these
bounded windows remain on the mini, through Missions/AI-runtime; this command does not
create or change their policy, masks or acceptance records.

```sh
RL_CANONICAL="$HOME/git/Rising Lands"
RL_LEASE="$RL_CANONICAL/local-data/coordination/heavy_lease.py"
RL_F0="$RL_CANONICAL/.local/m3/quadro128"
RL_S1="$RL_CANONICAL/.local/m3/passo2/S1"
RL_GFX="pesquisas-paralelas/graficos-animacao"
RL_START=".local/s1-render-mini-start"
RL_OUT=".local/s1-render-mini-original"
mkdir "$RL_START" "$RL_OUT"
cp "$RL_F0/manifesto.json" "$RL_START/manifesto.json"
cp "$RL_F0/instantaneo-00128.pickle" "$RL_START/instantaneo-00128.pickle"

python3 "$RL_LEASE" graphics-s1-mini-w1 -- python3 -B "$RL_GFX/capturar_janelas_s1_graficos.py" \
  --start "$RL_START" --to 403 --output "$RL_OUT/w1.json.xz"
python3 "$RL_LEASE" graphics-s1-mini-w2 -- python3 -B "$RL_GFX/capturar_janelas_s1_graficos.py" \
  --start "$RL_START" --resume "$RL_S1/instantaneo-01750.pickle" --to 2383 --output "$RL_OUT/w2.json.xz"
python3 "$RL_LEASE" graphics-s1-mini-w3 -- python3 -B "$RL_GFX/capturar_janelas_s1_graficos.py" \
  --start "$RL_START" --resume "$RL_S1/instantaneo-02250.pickle" --to 2878 --output "$RL_OUT/w3.json.xz"
python3 "$RL_LEASE" graphics-s1-mini-w4 -- python3 -B "$RL_GFX/capturar_janelas_s1_graficos.py" \
  --start "$RL_START" --resume "$RL_S1/instantaneo-03000.pickle" --to 3508 --output "$RL_OUT/w4.json.xz"
python3 "$RL_LEASE" graphics-s1-mini-w5 -- python3 -B "$RL_GFX/capturar_janelas_s1_graficos.py" \
  --start "$RL_START" --resume "$RL_S1/instantaneo-03500.pickle" --to 4080 --output "$RL_OUT/w5.json.xz"
python3 "$RL_LEASE" graphics-s1-mini-w6 -- python3 -B "$RL_GFX/capturar_janelas_s1_graficos.py" \
  --start "$RL_START" --resume "$RL_S1/instantaneo-04000.pickle" --to 4623 --output "$RL_OUT/w6.json.xz"
python3 "$RL_LEASE" graphics-s1-mini-w7 -- python3 -B "$RL_GFX/capturar_janelas_s1_graficos.py" \
  --start "$RL_START" --resume "$RL_S1/instantaneo-04750.pickle" --to 5090 --output "$RL_OUT/w7.json.xz"

python3 -B "$RL_GFX/validar_janelas_s1_graficos.py" \
  --capture "$RL_OUT/w1.json.xz" --capture "$RL_OUT/w2.json.xz" \
  --capture "$RL_OUT/w3.json.xz" --capture "$RL_OUT/w4.json.xz" \
  --capture "$RL_OUT/w5.json.xz" --capture "$RL_OUT/w6.json.xz" \
  --capture "$RL_OUT/w7.json.xz" \
  --output "$RL_GFX/validacao/mini-s1-render-windows.json"
```

If an invocation reports `budget_stop`, it is not complete coverage: its manifest gives
the exact last frame and resumable `snapshot.path`. Continue that native checkpoint in
a fresh leased invocation ending at the originally requested frame, with a new output
name, and include both files in the comparison. Never count missing frames, a named
stop, or an absent pass-2 package as equal surfaces. The MacBook's seven recorded native
invocations all completed without that stop (actual maximum about eight minutes).

## Remaining boundaries

Graphics 1.10 covers these gameplay windows. The default API still stops at `0x459454`
when a required text callback is omitted. The optional bounded native bitmap provider
is separately available; the S1/P4 probe comparison uses the explicitly recorded boundary.
General game modes other than 0x12 remain `0x4176A8`; actual MenuInit/LoadPie
`0x4799C4`, opaque victory text, the full late S1 combat/fire/death trajectory, other maps,
owners/cameras and unproved unit/task variants retain their named stops. Separate S1
result/objectives APIs and historical 100/100 native screen surfaces retain their own
scope. No whole-state M3.1/M4 proof or mission acceptance is asserted by this document.
