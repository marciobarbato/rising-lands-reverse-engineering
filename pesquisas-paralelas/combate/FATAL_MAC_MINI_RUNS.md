# Exact S1/D1 death windows for the Mac mini

These runs are **requested, not run on the MacBook**. They require Missions'
committed `m3/sondas/S1/resumo.json` or the forthcoming D1 equivalent, its
original input file, `.local/m3/quadro128/manifesto.json`, and the already
produced exact native snapshot files. Run from a checkout containing this
Combat delivery and those Missions artifacts. Set `--snapshot-root` if the
immutable snapshots are stored elsewhere; the tool finds the exact SHA,
never a merely similar frame.

```sh
python3 -B pesquisas-paralelas/combate/executar_janelas_fatais_combate.py S1
python3 -B pesquisas-paralelas/combate/executar_janelas_fatais_combate.py D1
```

The runner executes these **separate heavy-lease jobs**, each at most 250
frames and with a 1,100-second native-window alarm:

| Scenario | Existing starting snapshot | Windows |
|---|---|---|
| S1 | frame 11000, SHA `42d60722886b9e5775f1cf218412afa49fbc101a411468bed7de8c03e72e34aa` | 11000–11250, 11250–11500, 11500–11750, 11750–12000, 12000–12250 |
| D1 | frame 11000, exact SHA from `D1/resumo.json` | 11000–11250, 11250–11500, 11500–11750, 11750–12000 |
| D1 | frame17000, exact SHA from `D1/resumo.json` | 17000–17250, 17250–17500 |

Only each interval's first snapshot comes from Missions. Later jobs restore
the exact end snapshot saved by the preceding job; both path and SHA come
from that job's manifest. All jobs verify the scenario input hash and its
entire prefix up to the restored frame. No order is injected or byte patched.
D1's commands stop visibly if its eventual manifest has different available
frames; no snapshot or digest is invented.

The first S1 command expanded is:

```sh
python3 "/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py" combat-S1-11000-11250 -- python3 -B pesquisas-paralelas/combate/capturar_janela_fatal_combate.py --inicio .local/m3/quadro128 --snapshot-root .local --snapshot-frame 11000 --snapshot-sha256 42d60722886b9e5775f1cf218412afa49fbc101a411468bed7de8c03e72e34aa --entrada pesquisas-paralelas/missoes/m3/entradas/S1.json --ate 11250 --saida .local/combat-fatal-20261030/S1/11000-11250 --execute-sound-bodies
```

The batch runner locates this machine's `heavy_lease.py` by walking the
checkout's parent directories, or takes `--lease /exact/path/heavy_lease.py`.
It prints the complete command before each job. Use `--saida-root` for a new
output root on a rerun; existing evidence directories are never overwritten.

## Hooks and output

Observational entry/return hooks record InfligeDegat 0x450874,
EnginInfligeDegat 0x4502f0, iagUnitSendMessage 0x4829c8,
MAJSympathie 0x475118, PlayerResetAllie 0x46d8cb,
MessageBoxSet 0x46994b, EnginSetLevelExperience 0x44fb20,
SetDyingEngin 0x444938, RetireEngin 0x457058 and
CalculEnginNextEtape 0x456db5. EnginNextEtape 0x45442c is sampled for dying
units at corpse timers 0 and 329. Full registers, actual caller return and
stack flag, entry delta from that phase's opening, and full leaf delta at
the actual native return are recorded. Sampling has an explicit limit plus
a reserved death/removal budget; every entry is counted even when not sampled.

Whole game memory and registers are recorded before/after **every**
between-frames and frame phase. The last successful frame has a full exact
Missions continuation snapshot. The outputs are `abertura.json.xz`,
`fases.jsonl.xz`, `folhas.json.xz`, `manifest.json` and the end `.pickle`.

The original unopened sound-library bodies execute: the tool removes their
inherited display-scenario skip boundaries, while retaining the established
external Windows/input/display bindings. This is explicit in each manifest.
It yields real sound-call register clobbers for the Combat leaf comparison;
it is not a fresh F0 replay-equality claim for the old display-boundary log.
No translated Combat/AI/game callee executes inside the capture.

S1's window spans the frame 11858 harvester death and 330 subsequent corpse
steps through removal/recount. D1's windows cover the reported raider 17 kill
near 11500 and the last population rebuild/defeat interval near 17500. Mission
end-condition/latch translation remains Missions' responsibility. Return the
compressed outputs/manifests for exact phase and raw-leaf reproduction.
