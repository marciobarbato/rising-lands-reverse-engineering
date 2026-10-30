# Late-S1 original render windows

Input and phase references: native S1 revision
`82ec5eaa98d4f212b650c2c8ce2b293a30fb50ef`. The complete 800-unit pool is
required; S1's objective summary tracks only a few friendly units. Original
first entries include AffAttaqueEngin at 11,846, AffDyingEngin at 11,858 and
AffFlamme at 12,179. The native snapshots also show two owner-4 soldier raiders
and state 19 on the starting army. These are explicit inputs, not inferred logic.

`capturar_s1_tardio_graficos.py` preserves the published S1 display-v2 text
boundaries, checks the opening checkpoint, every complete native frame state and
both phase surfaces, and audits every captured world block before/after AffGame.
It also records all changing DGROUP bytes. It has a 19-minute whole-invocation
alarm and accepts at most 750 frames; transport/serialization are inside that
budget. Use independent native checkpoints for disjoint segments.

## Exact Mac-mini commands

Run in a separate Graphics worktree at the delivered feature commit, with read-only
original inputs and `.local/python` linked. The mini's Missions session remains
the sole writer of its worktree and snapshots. Fetch the public repository over
HTTPS when preparing this Graphics worktree. No main merge is performed.

The following covers the full late window 11,001–12,500 in six independent,
bounded original invocations. `RL_START` and `RL_OUT` must be new directories.
Each command obtains and releases its own native lease.

```sh
RL_CANONICAL="$HOME/git/Rising Lands"
RL_LEASE="$RL_CANONICAL/local-data/coordination/heavy_lease.py"
RL_F0="$RL_CANONICAL/.local/m3/quadro128"
RL_S1="$RL_CANONICAL/.local/m3/passo2/S1"
RL_GFX="pesquisas-paralelas/graficos-animacao"
RL_START=".local/s1-late-mini-start"
RL_OUT=".local/s1-late-mini-original"
mkdir "$RL_START" "$RL_OUT"
cp "$RL_F0/manifesto.json" "$RL_START/manifesto.json"
cp "$RL_F0/instantaneo-00128.pickle" "$RL_START/instantaneo-00128.pickle"
for RL_RANGE in 11000:11250 11250:11500 11500:11750 11750:12000 12000:12250 12250:12500; do
    RL_FROM="${RL_RANGE%:*}"
    RL_TO="${RL_RANGE#*:}"
    python3 -B "$RL_LEASE" "graphics-s1-late-$RL_RANGE" -- \
      python3 -B "$RL_GFX/capturar_s1_tardio_graficos.py" \
      --start "$RL_START" --resume "$RL_S1/instantaneo-$RL_FROM.pickle" \
      --to "$RL_TO" --output "$RL_OUT/S1-$RL_FROM-$RL_TO.json.xz" || break
done
```

To extend the complete survey through the last gameplay frame, use the same
command with ranges `12500:13250 13250:14000 14000:14750 14750:15500
15500:16250 16250:17000 17000:17031`. Every range remains at most 750 frames.
Frame 17,032 begins the separate result/menu contract. The user-facing bitmap
provider and glyph-enabled original display evidence are specified separately in
[AFFTEXT_RENDER_CONTRACT.md](AFFTEXT_RENDER_CONTRACT.md).

Do not compare glyph-enabled pixels to the old text-skipped S1 phase hash. For
those historical S1 windows, pass the strict recorded text adapter; the separately
captured AffText-enabled full surfaces prove the production glyph path. No
TextGetMessage pointer is fabricated and no missing glyph becomes a no-op.

## Glyph-enabled native calls and CPU comparison

The delivered proof covers natural entries11251–12500, **1250/1250** complete
normal glyph surfaces and1649 real AffText calls. Its separate historical chain
also passes1250/1250; there is no glyph-enabled simulated whole-state trajectory.
Prepared native cases pass179/179:141 fire/level cases,2 friendly soldier cases,
3 larger raid cases,32 message-marker phases and1 visible farmer hunger case.
The initial11001–11250 interval and entries after12500 remain unrun here.

After each250-frame capture in the first loop, run the following with its
`RL_FROM` and `RL_TO` still set. Every glyph call first checks the historical
surface against that capture, then executes original AffText and retains the
complete native indexed buffer. Keep glyph batches at250: the existing native
bench has a cumulative600-second limit, independently of the19-minute outer alarm.
For a750-frame survey file, use three separate250-frame selections of that file.
All Python comparisons below run outside the native lease.

```sh
RL_NATIVE="$(pwd)/$RL_OUT/S1-$RL_FROM-$RL_TO.json.xz"
RL_FIRST=$((RL_FROM+1))
python3 -B "$RL_LEASE" "graphics-s1-glyphs-$RL_RANGE" -- \
  python3 -B "$RL_GFX/capturar_alerta_s1_graficos.py" \
  --start "$RL_START" --capture "$RL_NATIVE:$RL_FIRST-$RL_TO" \
  --output "$RL_OUT/S1-$RL_FROM-$RL_TO-glyphs.json.xz"
python3 -B "$RL_GFX/validar_affgame_glifos.py" \
  --capture "$RL_OUT/S1-$RL_FROM-$RL_TO-glyphs.json.xz" \
  --output "$RL_OUT/S1-$RL_FROM-$RL_TO-glyph-comparison.json"
```

For the historical text-boundary full-surface comparison of any newly captured
window, use this CPU-only command. Supply consecutive files in chronological
order to carry cache, pixels and saved background across capture boundaries.
The command prints actual N/N and writes all mismatch/stop details. It makes no
whole-state reconstructed mission acceptance claim.

```sh
PYTHONPATH="$RL_GFX${PYTHONPATH:+:$PYTHONPATH}" python3 -B - \
  "$RL_OUT/S1-$RL_FROM-$RL_TO.json.xz" <<'PY'
import json,sys
from pathlib import Path
from validar_janelas_s1_graficos import comparar,registros
refs=registros();previous=None
for filename in sys.argv[1:]:
    result=comparar(Path(filename),refs,previous)
    previous=result.pop('_exit')
    print(filename,result['equal'],'/',result['compared'])
    Path(filename+'.comparison.json').write_text(json.dumps(result,indent=1)+'\n')
    if result['first_difference'] is not None:raise SystemExit(1)
PY
```

The original probes retain named failures for unsupported states. Preserve the
native output and its failing comparison; do not change inputs or skip a draw to
produce N/N. Consumer contracts are in HANDOFF.md and AFFTEXT_RENDER_CONTRACT.md.
