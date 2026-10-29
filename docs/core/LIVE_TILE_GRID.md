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

## Consumers

- **Economy:** pass `mundo.tiles.buffer`, or the same live view, as the `mosaicos` bytes that `quadro_economia.atualizar_campos` / `extracao.RecursosTerreno` expect. Do not copy it.
- **Missions:** replace the list bridge `vincular_lista(P(TILES), w.tiles, 'H', …)` with `w.vincular_tiles(mapa.vista(P(TILES), 131072))`, so the world and the memory map share the allocation.
- The region grid `[0x4e0f38]` is also a u16 list in `MundoFisico`. `GradeU16` can carry it the same way when a consumer needs it live. That is not bound yet.

## Validation

`testes/test_grade_u16.py` checks:
- identity and little-endian access;
- the list operations and the refusals;
- that the following give identical results with a live grid and with the list, and that the live buffer equals the packed list:
  - structure terrain placement;
  - region reconstruction;
  - the eight original-first remap classification captures (`relatorios/capturas-classificacao-remapeamento-original.json`).

The existing terrain, placement, reset and classification suites are unchanged.
