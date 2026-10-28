# Audio research

Owned by the Audio front, a second-wave front run by the macOS chat until its M1 trigger. The contract, ownership boundary and stage sequence are in [docs/AUDIO.md](../../docs/AUDIO.md). Results and requested contracts are in [HANDOFF.md](HANDOFF.md).

Original sound banks are read from the read-only CD copy (`../source/cd/INSTALHD/SOUND/`). Decoded PT-BR samples, caches and bundles are never committed here. Commit only evidence (exported intact intervals, original-only captures, reviewed REA excerpts) under `evidencias/`, fresh native reports under `validacao/`, and tests under `testes/`. Every new module basename must be unique across the flat research namespace (`testes/test_namespace_audio.py`).

## Modules (stage 1)

| Module | Role |
|---|---|
| `ambiente_audio.py` | Bootstrap, CD paths and bank identities |
| `extrair_som.py` | Exports intact intervals, tables and the manifest |
| `provedores_som.py` | Declared Windows/DirectSound binding fixtures shared by both sides |
| `cenarios_som.py` | Scenario constants and synthetic inputs |
| `bancada_som.py`, `capturar_som.py` | Native bench (Unicorn) and original-only captures |
| `bancos_som.py`, `adpcm_som.py` | Python reconstruction: bank paths/header/index, buffer creation and IMA ADPCM |
| `reproduzir_som.py` | Python replays of the capture scenarios |
| `validar_som.py` | Fresh native vs Python vs committed comparison |
| `catalogo_som.py` | Sample catalogue (`catalogo-amostras.json`), hashes only |
