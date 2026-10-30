# S1/D1 death windows for the Mac mini

These runs are **requested, not run on the MacBook**. They require Missions'
committed `m3/sondas/<scenario>/resumo.json` and `quadros.jsonl.xz`, the
original scenario input file, `.local/m3/quadro128/manifesto.json`, and trusted
native snapshot files. D1's published artifacts must be present before its
command runs; its summary is expected to list snapshots every 250 frames.
Run from the feature checkout containing this delivery and those artifacts:

```sh
python3 -B pesquisas-paralelas/combate/executar_janelas_fatais_combate.py S1 --intervals 11000-12250
python3 -B pesquisas-paralelas/combate/executar_janelas_fatais_combate.py D1 --intervals 11250-11750 15250-15700
```

The optional middle D1 death window is a separate invocation:

```sh
python3 -B pesquisas-paralelas/combate/executar_janelas_fatais_combate.py D1 --intervals 12250-13750
```

`--intervals START-END [START-END ...]` overrides defaults. Intervals must be
ordered, nonoverlapping, within the manifest's `last_frame`, and start at a
listed snapshot with a committed frame record. The complete plan is checked
before the first job. Omitting the option selects the S1 and required D1
windows above. Each interval is split into **separate heavy-lease jobs** of
at most 250 frames, each retaining the 1,100-second native-window alarm:

| Scenario | Starting snapshot frame | Leased jobs |
|---|---|---|
| S1 | 11000 | 11000–11250, 11250–11500, 11500–11750, 11750–12000, 12000–12250 |
| D1 | 11250 | 11250–11500, 11500–11750 |
| D1 | 15250 | 15250–15500, 15500–15700 |
| D1 (optional) | 12250 | six 250-frame jobs through 13750 |

## Snapshot identity and provenance

Pickle file hashes are provenance, not reproducible game-state identity.
The mini reports S1-a's frame-11000 pickle as `42d60722…`, S1-b's as
`eca79f8a…`, and the pass-2 records snapshot as `6570ff47…`. The runner can
restore any of these trusted serializations **only if both** restored
`dgroup_sha256` and `state_sha256` equal the committed scenario's
`quadros.jsonl.xz` record at the requested frame. S1/frame11000's DGROUP is
`d6bcbd2e5e75d24677926e8adf8ce0ff1d0c180f627bb721342e5d1cebb16761`;
its whole-state digest is
`3e1c2b531052721d622880f14306759fc3b670dfe1500409d1385e7782fa85ea`.
No DGROUP-only fallback is used if the whole state differs.

Set `--snapshot-root /path/to/trusted/snapshots` to narrow discovery to the
mini's pass-2 records directory; the default is `.local`. The tool searches
`instantaneo-<frame padded to five digits>.pickle`, restores candidates with
Missions' existing binding/layout checks, and checks frame and both digests
before changing sound boundaries or executing any phase. Restore errors stop
visibly. No order is injected or game byte patched.

The existing `--manifest /path/to/pass-2/resumo.json` remains supported for an
alternate run's snapshot availability, end frame and scenario input hash.
It does **not** replace the committed `m3/sondas/<scenario>/quadros.jsonl.xz`
identity anchor, and its pickle SHA is not an acceptance requirement. The
scenario's full input hash and the entire restored input prefix must match.
This lets the mini keep its existing pass-2 `--manifest` invocation.

Only each interval's first snapshot is checked against the published record.
Later jobs restore the exact end snapshot produced by the preceding capture,
using that job's path and file SHA. Their sound-body execution intentionally
differs from the inherited display-boundary scenario. Each output manifest
records the actual opening pickle SHA, verification method, published record
file hash, expected state digests, source manifest hash and input hash.
No following job starts after failure, incomplete leaves or a short segment.

The first S1 command expanded is:

```sh
python3 "/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py" combat-s1-11000-11250 -- python3 -B pesquisas-paralelas/combate/capturar_janela_fatal_combate.py --inicio .local/m3/quadro128 --snapshot-root .local --snapshot-frame 11000 --snapshot-manifest pesquisas-paralelas/missoes/m3/sondas/S1/resumo.json --snapshot-records pesquisas-paralelas/missoes/m3/sondas/S1/quadros.jsonl.xz --entrada pesquisas-paralelas/missoes/m3/entradas/S1.json --ate 11250 --saida .local/combat-fatal-20261030/S1/11000-11250 --execute-sound-bodies
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
steps through removal/recount. The Mac mini reports these events on the
**actual D1.json path**: deaths at 11429 and 11561; twelve further deaths
between 12456 and 13687; deaths at 15344 and 15555; population count 0 and
AL=1 at 15555; MenuInit(0x13) at 15654; PartieGetResultat returning 0 and the
failure branch at 15655. D1.json stops at 15700. The earlier raider-17 kill
near 11500 was a development chain, and 17000–17500 is not a D1 window.
These are the mini's reported landmarks, not fresh captures on this MacBook.
Mission end-condition/latch translation remains Missions' responsibility.
Return the compressed outputs/manifests for exact phase and raw-leaf reproduction.
