# Unicorn teardown and capture-script exit

Date: 2026-10-29. Owner: Core. This applies to every front whose scripts build a `BancadaX86` (`ferramentas/emulador.py`) or any other `unicorn.Uc`.

## Symptom

On 2026-10-29, Economy's display-state field-growth capture (`capturar_campos_exibicao_original.py`, `feat/re-economy` 9703754) wrote its evidence and printed its last line at 05:17:38. It then ran at 100% CPU for more than 75 minutes, while holding the heavy lease, until it was stopped with SIGTERM. A `sample` of the process showed this stack:

`Py_FinalizeEx → ctypes → uc_close → x86_release → release_common → memory_free_x86_64 → memory_region_transaction_commit_x86_64`

## Cause

Unicorn 2.1.4's `uc_close` frees the mapped regions one at a time. Each free commits a QEMU memory transaction that rebuilds the address-space view over every region still mapped, so teardown time grows superlinearly with the number of regions. The Python binding runs `uc_close` from a `weakref.finalize` during interpreter shutdown, after the script's last line. Unmapping the regions explicitly costs the same, in either order.

The region count is what matters, not the byte count:
- **Missions' display bench** has 16 regions after MissionLoad (273 MB). It builds in 71 s and its `uc_close` takes 2 ms.
- **Economy's capture bench** (`capturar_quadro_m2_original.Captura`, reused by the field-growth capture) maps every 4 KiB page of the display post-load blocks as its own region. The 25,343 display blocks (DGROUP excluded) give 26,262 single-page regions, which form only 5 contiguous runs.

`relatorios/encerramento-unicorn.json` has the full measurement. It was run on the Mac mini with `ferramentas/medir_encerramento_unicorn.py` at `ca761bb`, under the exclusive lease, with Unicorn 2.1.4, Python 3.9.6 on arm64, taking 232.5 s. Each case runs in its own child process with a 120 s bound. `close` is the binding finalizer that interpreter shutdown calls:

| 4 KiB regions, one per `mem_map` | 250 | 500 | 1,000 | 2,000 | 3,000 | 4,000 | 8,000 |
|---|---|---|---|---|---|---|---|
| Disjoint pages: `mem_map` total (s) | 0.004 | 0.02 | 0.117 | 0.81 | 2.9 | 7.7 | — |
| Disjoint pages: `uc_close` (s) | 0.004 | 0.018 | 0.113 | 0.79 | 2.9 | 7.7 | — |
| Display-state pages, contiguous: `mem_map` total (s) | — | — | 0.117 | 0.80 | — | 7.8 | over 120 s for map and close |
| Display-state pages, contiguous: `uc_close` (s) | — | — | 0.113 | 0.79 | — | 7.6 | (same run) |

- Each doubling of the region count multiplies both costs by 7 to 10.
- Contiguous single-page regions cost exactly as much as disjoint ones: Unicorn does not merge adjacent regions.
- Mapping and closing the 26,262 display-state pages coalesced into 5 regions both take 0.000 s.
- Mapping and closing the display bench's 16-region layout replayed in a bare engine also take 0.000 s.

## Fixes in Core tooling

1. **Map pages as contiguous runs.** `emulador.mapear_paginas(cpu, paginas, permissoes=None)` maps a set of page addresses as one region per contiguous run and returns the runs. `paginas_em_execucoes` gives the runs without mapping. Bytes, addresses, access rights and faults outside the runs are identical to one-region-per-page mapping (`testes/test_encerramento_captura.py::PaginasCoalescidas`). For Economy's layout, 26,262 regions become 5.
2. **Durable fast exit.** `encerramento_captura.encerrar_captura(codigo, *saidas)` does the following, in order:
   - it fsyncs each written output file and its directory;
   - it flushes stdout and stderr, fsyncing them when they are redirected to a file;
   - it leaves with `os._exit(codigo)`, so no `uc_close` runs, whatever the region count.

   A missing output raises instead of exiting. The heavy-lease wrapper runs the command as a child process, so it still records the exit status and releases the lease. `testes/test_encerramento_captura.py` bounds the exit of a process holding 3,000 regions to under 1 s after its output is written. A normal shutdown with that many regions takes 2.9 s.

Core's display-bench scripts now end with the fast exit: `capturar_quadros_seguintes.py`, `capturar_exibicao_quadro1.py`, `levantar_quadros_exibicao.py` and `validar_chamadas_quadro_core.py`.

## Guidance for capture scripts (all fronts)

- **Map coalesced.** Never call `mem_map` once per page or once per allocation block when the blocks are adjacent. Collect the pages and call `emulador.mapear_paginas(cpu, paginas)`. Economy's `capturar_quadro_m2_original.Captura.__init__` and `capturar_campos_exibicao_original.CapturaExibicao.__init__` are the known instances. Combat's `capturar_quadro_m1.py` maps per page as well.
- **End a capture with the fast exit.** Write and close the evidence, then call `encerrar_captura(status, path, ...)`, for example:

  ```python
  if __name__ == '__main__':
      from encerramento_captura import encerrar_captura   # ferramentas/ on sys.path
      encerrar_captura(*main())                           # main() -> (status, written path)
  ```

  Keep failure outputs under `.local/` as before, and pass whichever path was actually written.
- **Never call it from a test runner, a library function or the gate.** It ends the whole process and skips `atexit` and pending `finally` blocks. Tests that build benches release them by garbage collection: keep their region counts small, or coalesce.
- **Check the count while developing:** `len(list(cpu.mem_regions()))`. Up to a few hundred regions costs milliseconds. Thousands cost seconds, and tens of thousands cost hours. Mapping costs as much as teardown, whether the pages are contiguous or not.
