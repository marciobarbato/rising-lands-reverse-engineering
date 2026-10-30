# CalculWorkEngin's TerrainEstGc and SetMiniMap (AI/runtime M3.1 stops)

Status: original-first on `feat/re-core`. AI/runtime's M3.1 chain (feat/re-ai-runtime `2083a37`, `M3_1_CADEIA_ALEM_220.md`) stops at two Core names inside CalculWorkEngin:
- TerrainEstGc at `0x44d8cd` for an object byte ≥ 0x1d (P7 2801, P4 460; unassigned before, Core took it as terrain);
- SetMiniMap at `0x44c437` (P5 760).

Validator and capture: `ferramentas/validar_consultas_trabalho.py`. It uses `validar_fadiga_vegetacao`'s bench method on Economy's committed work-cycle scenario `capturar_ciclo_trabalho.ordens`, run to frame 600. Original SHA-256 `6c556520…43fb`.

## What the original does

**TerrainEstGc `0x4762b9..0x4762de`.**
- The input is AX, a cell. EAX = 1 when the object byte `[[0x507d74] + AX]` is in 0x1d..0x34, else 0. The byte is zero-extended into EAX before AL is set, so bits 8..31 are 0.
- EDX is pushed and restored. Nothing else is touched.
- CalculWorkEngin phase 0 (`0x44d8cd`) asks it on the field cell. In the scenario, unit 13 asks at frame 261 on (26,32), object ≥ 0x1d, and unit 14 at 293 on (27,32). Both return 1.

**SetMiniMap at `0x44c437`.**
- This is **mode 4**: `0x44c427 mov edx, 4`. AL is the unit owner and BX is the cell, called right after the mine exit's DecouvreTerrain/IllumineTerrain (`0x44c3f5`/`0x44c422`). The twin call at `0x44c243` is also mode 4.
- In the scenario the builder (unit 12, owner 0) leaves its mine at frame 572, cell 0x92b. The call writes 8 bytes: the unit layer, and the view where the cell is lit.

## Translations and providers

- `incursao_core.terreno_esta_gc(m, eax) -> {EAX}` (new), registered in `incursao_core.ROTINAS` / `traducao_core('TerrainEstGc')` and in `chamadas_quadro_core.provedores_core` as `'TerrainEstGc': provider(sitio, caso) -> EAX`.
- SetMiniMap mode 4 is the existing `incursao_core.definir_minimapa`, already served as `provedores_core['SetMiniMap'] (keywords sitio, jogador, modo, caso)`. It matches natively for player owners 0..3, owner 4, 0xc8, lit and unlit cells, map corners and upper register bits.
  - **No Core change was needed.** If AI/runtime's chain stops there, the call reached it without DL = 4 or through another provider.
  - Economy's `ciclo_trabalho` already passes `EDX=4` at `0x44c437`.
  - Modes other than 4 still raise at their handlers in the flat translation (the world model's `minimapa` has them all).
- `som` call address (AI/runtime's request): `selecao_ordens.chamar_som(som, nome, regs, pilha, chamada)` passes the original `call PlaySnd_*` address as keyword `chamada` when the provider declares that parameter or `**kwargs`. Existing three-argument providers are unchanged. The addresses come from Core's call sites:
  - EnginAsk `0x440de7`;
  - BatimentSelection `0x41b785`;
  - RetireSelectionEngin's stop `0x474582`;
  - RestaureSelectionGroupe's stop `0x4728e4`;
  - EnginSetFatigue `0x44b33d`.

## Native differential

| Routine | In situ | Declared variants | Mismatches |
|---|---|---|---|
| TerrainEstGc | 2 (`0x44d8cd`, frames 261/293) | 16: object bytes 0x00, 0x01, 0x1c..0x1e, 0x28, 0x33..0x36, 0x42, 0x43, 0x46, 0x80, 0xff; upper register bits | 0 |
| SetMiniMap | 3 (`0x44c437` frame 572; AvanceEngin mode 4 frames 18/20) | 11: owners 0..3/4/0xc8, cell lit/unlit, corners, upper bits | 0 |

The capture is `evidencias/consultas-trabalho/captura-trabalho.json.xz` (original only, 272 s). The report is `relatorios/consultas-trabalho-emulada.json`: 32 comparisons, 0 mismatches. Each comparison covers EAX..EBP, ESP and every byte of every block; paths reproduced, code unchanged.

Tests:
- `testes/test_consultas_trabalho.py` (CPU-free): capture facts, report bound to Core sources, TerrainEstGc over all 256 object bytes and its provider, and `chamar_som`.
- `testes/test_incursao_core.py` lists TerrainEstGc as not reached by the raid replay.

Because `selecao_ordens.py`, `visao_grupos.py`, `chamadas_quadro_core.py` and `fadiga_vegetacao.py` changed, every native differential bound to them was rerun: selection orders, vision groups, both hunger scenarios, and these queries.

```sh
python3 "…/heavy_lease.py" core -- python3 -B ferramentas/validar_consultas_trabalho.py    # ~5 min
```
