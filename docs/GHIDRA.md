# Ghidra, executable identity, and original symbols

The local installation records Ghidra 12.2 and Temurin JDK 25.0.5+8 ARM64 under `.local/`. Verified distribution URLs and hashes live in `ghidra/instalacao.json`. The macOS ARM64 decompiler was compiled from the distribution sources using Apple's existing development tools. Projects, downloads, configuration, logs, and caches remain local.

```sh
python3 ghidra/instalar.py
python3 ghidra/analisar.py
python3 ghidra/executar.py gui ghidra/projetos/RisingLands.gpr
```

The original Watcom PE has six sections with `VirtualSize=0`. `ghidra/preparar_entrada.py` creates an **analysis-only copy**, filling those fields with `SizeOfRawData`; eight bytes differ within the six four-byte fields. `ghidra/entrada.json` lists changed offsets.

| Input | SHA-256 |
|---|---|
| Original | `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb` |
| Normalized analysis copy | `26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0` |

Never overwrite the original or use the normalized copy as the differential execution oracle. Code/data addresses and file length are preserved by the normalization, but it is not a patch intended to run the game.

Analysis uses `x86:LE:32:default` and the available Windows profile. This is not evidence of Visual C++ compilation; the original runtime string identifies `WATCOM C/C++32`. Watcom register arguments and shared epilogues can confuse inferred signatures. Seven accessors have explicit AX arguments/AL or AX returns. Assembly and original-byte behavior take precedence over decompiled C. An export marked OK means text was produced, not that semantics were established.

`RISING.SBL` provides 1,995 original symbol records, retained in French. `ferramentas/extrair_ia.py` extracts symbols and the rule-program evidence into `relatorios/`. `ImportarSimbolosOriginais.java` imports the records into namespace `OriginaisSBL` after checking the analysis-copy hash:

```sh
python3 ferramentas/extrair_ia.py
python3 ghidra/executar.py headless ghidra/projetos RisingLands   -process RISING-analise.exe -noanalysis -scriptPath ghidra/scripts   -postScript ImportarSimbolosOriginais.java relatorios/simbolos-originais.tsv evidencias/simbolos-importados.tsv
```

Symbol names, duplicate entries, type layouts, table indices, and recovered register conventions are evidence with distinct confidence levels. Original naming does not fix an incorrectly inferred calling convention. The rule-program inventory has 1,157 instructions, 42 active registered types, and 140 operation names; decoding those names does not implement the whole AI machine.

Parallel workers read the central project/exported evidence. New Ghidra work uses a domain-local ignored project/log directory and publishes exports only under its owned evidence path. Do not concurrently write one shared Ghidra database. Avoid reinstalling or changing the shared toolchain during a research round.
