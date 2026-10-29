# Live tile grid contract

M2 round 4, 2026-10-29. Owner: Core. This contract applies to Economy (field growth, `UpdateChamp`/`ScanNouvellePatate`), Missions (world binding) and AI/runtime (composition).

## The original grid

The terrain tile grid is the allocation that DGROUP pointer `[0x507d70]` points to. It holds 65,536 little-endian u16 words (131,072 bytes), one per cell, at `pointer + 2·cell`. The original routines read and write it in place:
- NextAnimTerrain;
- UpdateChamp's field growth from frame counter 128;
- structure terrain placement;
- the region and pathing classifiers.

## Core representation

By default, `MundoFisico` keeps `tiles` as a list of 65,536 ints. That stays unchanged for every existing fixture and test.

For live memory, call

```python
mundo.vincular_tiles(buffer)   # buffer: the live 131,072-byte allocation at [0x507d70]
```

`buffer` is the caller's writable `bytearray`, or a writable one-dimensional contiguous `memoryview`, for example `memoria.vista(ponteiro, 131072)`. After the call:
- `mundo.tiles` is a `grade_u16.GradeU16`, and `mundo.tiles.buffer is buffer` (identity, no copy).
- Every Core read and store of a tile is a live little-endian u16 access to that buffer. Stores made by any other consumer of the same buffer are therefore visible to Core immediately, and Core's stores are visible to them.
- `GradeU16` supports the list operations Core uses:
  - `t[i]` and `t[-1]`;
  - `t[i] = v`;
  - `t[a:b]`, which returns a new list;
  - `t[:] = values`, same length only;
  - `len`, iteration, `list(t)` and equality with any sequence.
- It refuses, before writing, any store outside 0..65535 or any slice store that would change the size. A list accepted such values, but the original u16 grid cannot hold them.

## All the grids field growth touches (round 5)

`mundo.vincular_grades(tiles=…, regioes=…, atributos=…, objetos=…, donos_objetos=…)` binds any subset of the world's terrain grids live, by identity:

| Grid | Original | Bytes | Core attribute after binding |
|---|---|---|---|
| tiles | `[0x507d70]` u16 | 131,072 | `mundo.tiles` (`GradeU16`, `.buffer` is the given object) |
| regions | `[0x4e0f38]` u16 | 131,072 | `mundo.regioes` (`GradeU16`) |
| attributes | `[0x507da8]` u8 | 65,536 | `mundo.atributos` (the given object) |
| objects | `[0x507d74]` u8 | 65,536 | `mundo.objetos` (the given object) |
| owners / quantities | `[0x507dac]` u8 | 65,536 | `mundo.donos_objetos` (the given object) |

All buffers are validated before any of them is bound. `vincular_tiles(buffer)` is the tiles-only form. Bound grids keep their identity through Core's region rebuild (`refazer_regioes` writes in place) and through the remap reset.

**What UpdateChamp/ScanNouvellePatate need** (Economy `extracao.RecursosTerreno`), and where Core supplies it:
- **tiles:** read-only LE u16 at `2·neighbour`, testing 0x84..0x86 / 0x9d..0xdc → `mundo.tiles.buffer`.
- **attribute bit 0:** read-only, blocks planting → `mundo.atributos`.
- **object grid:** read, and written with 0x1d/0x29 → `mundo.objetos`.
- **quantity grid** → `mundo.donos_objetos`. Core calls this allocation "owners"; Economy's growth uses it as quantities. It is one allocation.
- The RNG `0x497164` and the mines `0x509954` are not Core grids.

`RecursosTerreno`'s constructor copies its arguments. Until Economy adds a live constructor, consumers assign the live objects after construction:

```python
recursos.mosaicos, recursos.atributos = mundo.tiles.buffer, mundo.atributos
recursos.terreno.tipos, recursos.terreno.quantidades = mundo.objetos, mundo.donos_objetos
```

`testes/test_grade_u16.py::GradesVivasMundo` runs Economy's actual `propagar_planta` this way, and the plant lands in Core's live object grid. A live constructor `RecursosTerreno.vivo(...)` is requested from Economy, matching `BonusUnidades.vivo`.

## Consumers

- **Economy:** pass `mundo.tiles.buffer`, or the same live view, as the `mosaicos` bytes that `quadro_economia.atualizar_campos` / `extracao.RecursosTerreno` expect. Do not copy it.
- **Missions:** replace the list bridge `vincular_lista(P(TILES), w.tiles, 'H', …)` with `w.vincular_tiles(mapa.vista(P(TILES), 131072))`, so the world and the memory map share the allocation.
- **Missions:** the other `vincular`/`vincular_lista` grid bindings can likewise become `w.vincular_grades(...)` over `mapa.vista(...)` views, so the world and the map share every terrain allocation.

## Validation

`testes/test_grade_u16.py` checks:
- identity and little-endian access;
- the list operations and the refusals;
- that the following give identical results with a live grid and with the list, and that the live buffer equals the packed list:
  - structure terrain placement;
  - region reconstruction;
  - the eight original-first remap classification captures (`relatorios/capturas-classificacao-remapeamento-original.json`).

The existing terrain, placement, reset and classification suites are unchanged.
