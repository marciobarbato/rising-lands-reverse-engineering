# S1 result and objectives capture request

The local original-only S1 checkpoints stop at frame 1728. Two native prefix passes also agree through frame 2020.
There is no local late S1 checkpoint, and `origin/feat/re-missions` has no S1 probe package at this writing.
Replaying the entire 17,050-frame prefix exceeds the MacBook's 20-minute native-run allowance. Do not fabricate a
victory state or change the menu-mode byte to create a screen.

`capturar_telas_finais_s1.py` is a prepared, syntax-checked native producer; its late-screen execution is not yet
validated. It restores an actual scripted S1 checkpoint at frame 17000, isolates each real MenuInit(0x13),
PartieGetResultat, MenuInit(0x11) and AffObjectif call, records entry/exit memory metadata, bounded render inputs,
full surfaces and raster/text arguments, restores
the exact entry, then requires the ordinary call's surface to equal the isolated result. Declared writes are empty.
No glyph provider is substituted. Every ordinary phase also retains its complete surface, raster arguments and whole-state hash. Complete native
asset banks are hashed as memory metadata and are not copied into tracked evidence. Text arguments are read through
the terminator (bounded to65536 bytes); an unreadable argument is an explicit text-read stop, never a fabricated
empty string or glyph result.

Run on the Mac mini from the Graphics worktree after fetching this feature branch. Substitute the existing native
S1 snapshot path if the capture directory differs; the checkpoint must be the real scripted frame 17000.

```sh
python3 "/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py" graphics-s1-final-screens -- \
  python3 -B pesquisas-paralelas/graficos-animacao/capturar_telas_finais_s1.py \
  --start .local/m3/quadro128 \
  --snapshot .local/m3/S1/instantaneo-17000.pickle \
  --to 17050 --ref fd56f69 \
  --output pesquisas-paralelas/graficos-animacao/evidencias/s1-telas-finais-nativas.json.xz
```

The checkpoint carries the original scripted bindings. The producer reads the immutable S1 input from `fd56f69`;
that input must match the native run. This is only 50 frames after the supplied late checkpoint, with an internal
18-minute budget. If there is no late checkpoint, Missions must produce it on the Mac mini from its accepted native
S1 run. No multi-thousand-frame MacBook command is authorized by this request.

After the capture, commit the evidence before translating screen composition. Compare the ordinary phase hashes
with the eventual published S1 probe and replay all raster arguments and complete 800x600 surfaces in Python.
Until that evidence exists, result/objectives equality is **not run (0 captured screens)**, and the gameplay renderer's
unsupported menu modes remain named stops. Render API remains 1.9.
