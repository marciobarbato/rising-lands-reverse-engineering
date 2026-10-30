# S1 result and objectives: original-only screen evidence

Native evidence is committed in `24f0ec8`, before any screen translation. The producer restored the real S1
frame17000 checkpoint found read-only in `worktrees/p2-s1-macbook/.local/m3/passo2/S1`, whose sequential-capture
metadata and immutable probe ledger belong to revision `54d148d931cc3420fe256e6fec71462087597293`. Its input hash
`622a882d5439afc88431102fb98df60dcc44a59714742c9278ba4d7d8413c18c` exactly matches the S1 input at `fd56f69`.
The opening whole-state hash also matches the published frame17000. A byte-identical private checkpoint copy is
retained at `.local/graficos-api17-start/S1-17000.pickle`; no other front's file was modified.

`evidencias/s1-telas-finais-nativas.json.xz` covers frames17001–17050. **100/100 phase surfaces and all50 end-frame
whole states match the original S1 ledger.** At real call entries it saves CPU/context, stack, state blocks,
DirectDraw pixels and declared host state, executes the intact call to its real caller return, restores the exact
entry, then requires ordinary execution to reproduce its surface, whole native state, raster arguments and text
arguments. Declared game-state writes are empty; no victory or menu mode is injected.

| Screen | Original calls isolated | Equal / total |
|---|---|---:|
| Result | MenuInit(0x13) at17032 + PartieGetResultat at17033–17043 | 12 / 12 |
| Objectives | MenuInit(0x11) at17043 + AffObjectif at17044–17050 | 8 / 8 |

Zero surface/state/raster/text-argument mismatches. The leased native recording takes **71.216s**. It requires no
multi-thousand-frame MacBook run or new Mac mini continuation. Both real MenuInit transitions are asserted.
The record contains full800x600 indexed surfaces, complete-phase raster/text traces, bounded render-state inputs,
allocation metadata/hashes and original input/code/checkpoint provenance. Complete asset banks are not copied into
tracked evidence. Some optional input regions are explicitly unavailable; notably the requested4096-byte CRT span
exceeds the captured thread-data block. Its whole-state metadata/hash is retained. Unavailable data is never filled
with zeros. A future translation requiring further bytes must export them from the retained native checkpoint.

AffText remains the declared non-execution boundary. Text arguments retain their full terminated bytes when
readable, bounded to65536 bytes; an opaque pointer is an explicit text-read stop, never an invented empty string.
The surfaces are precisely what the original drew under the benchmark's declared boundaries. A new glyph-enabled
renderer has not been proved here.

Reproduction from the Graphics worktree, using only the retained private checkpoint and read-only Git data:

```sh
git show 54d148d931cc3420fe256e6fec71462087597293:pesquisas-paralelas/missoes/m3/sondas/S1/quadros.jsonl.xz > .local/graficos-api17-start/S1-ledger.jsonl.xz
python3 "/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py" graphics-s1-final-screens -- \
  python3 -B pesquisas-paralelas/graficos-animacao/capturar_telas_finais_s1.py \
  --start .local/graficos-api17-start --snapshot .local/graficos-api17-start/S1-17000.pickle \
  --probe-records .local/graficos-api17-start/S1-ledger.jsonl.xz \
  --to 17050 --ref fd56f69 --output .local/graficos-api17-start/S1-screens-reproduction.json.xz
```

The gameplay renderer remains contract1.9. Python composition for menu modes0x13/0x11 is **not implemented** and
continues to stop at `0x4176A8`; this is native screen preparation, not a claim of reconstructed screen equality.
`evidencias/inventario-estruturas-S1-ledger.json` separately inventories all16922 native S1 frame records: only
sanctuary type2 modes4/5 and CAVE type3 modes2/5, with owners0/0xC8, occur. Free pool records are not active CAVEs
in mode0. All19 native S1 view origins are enumerated for the view-effect follow-up.
