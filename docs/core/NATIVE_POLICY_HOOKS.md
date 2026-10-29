# Native pass-2 hooks for the comparison policy

Tooling only. It changes how pass 2 of Missions' comparison policy observes accesses, not what it records. Missions' files are not edited: `politica_comparacao_quadros.py`, `segmentos_quadros_missao.py` and `politica_comparacao_quadro1.py` are reused read-only.

## Files

| File | Role |
|---|---|
| [`ferramentas/nativo/ganchos_memoria.c`](../../ferramentas/nativo/ganchos_memoria.c) | C library: display-root tracker, target/surface access callbacks, insertion-ordered aggregates |
| [`ferramentas/compilar_ganchos_nativos.py`](../../ferramentas/compilar_ganchos_nativos.py) | Deterministic build with `/usr/bin/clang` into `.local/nativo/libganchos_memoria.dylib` (ignored, never committed) |
| [`ferramentas/ganchos_nativos.py`](../../ferramentas/ganchos_nativos.py) | Loader, tracker wrapper, `ganchos_politica(b, alvos)` drop-in |
| [`ferramentas/politica_ganchos_nativos.py`](../../ferramentas/politica_ganchos_nativos.py) | Runtime injection into the Missions policy, sequential and segmented validation |
| [`testes/test_ganchos_nativos.py`](../../testes/test_ganchos_nativos.py) | Build identity, loud failure, no fallback (no library needed) |
| [`testes/test_emulacao_ganchos_nativos.py`](../../testes/test_emulacao_ganchos_nativos.py) | Opt-in (`RISING_EMULAR=1`): tracker vs Missions' closures, engine registration, stale library, short window vs Python hooks |

Build: `python3 -B ferramentas/compilar_ganchos_nativos.py`. Two builds give the same bytes.

## Interface

- **Registration.** `uc_hook_add(engine, &h, type, callback, user_data, begin, end)` is called through ctypes on the binding's own `libunicorn` (`unicorn.unicorn_py3.unicorn.uclib`), with `Uc._uch` as the engine and a C function pointer from the library. The library calls `uc_reg_read`, `uc_mem_read` and `uc_emu_stop` through pointers taken from that same `libunicorn`; it links nothing.
- **Loading.** `ganchos_nativos.carregar()` raises `BibliotecaNativaIndisponivel` when the library is missing, when its embedded identity (sha256 of the C source and the exact flag list) differs from the current source and flags, or when Unicorn is not 2.1.4. There is no fallback to Python hooks. `--metodo python` must be asked for explicitly.
- **Drop-in.** `ganchos_politica(b, alvos, modo='agrupado')` has the contract of `politica_comparacao_quadros.ganchos(b, alvos)`: it returns `(acessos, superficie, coletar)`, with the same keys `(kind, context, phase, routine)`, counts and key insertion order. `coletar(fase)` drains the native aggregates once per phase, then adds the binding writes exactly as the Python `coletar` does.
- **Phase.** The Python closures read `b.fase` at each access. `espelhar_fase` swaps the bench's class for a subclass whose `fase` property forwards every assignment to the tracker. The value stays in `b.__dict__`, so `vars(b)` and segment snapshots are unchanged.
- **Injection.** `politica_ganchos_nativos.injetar('nativo')` replaces `politica_comparacao_quadros.ganchos` in the running process. Missions' `passo2` and `segmentos_quadros_missao.politica_segmento` both look that name up at call time. No Missions adapter is needed.

## Equivalence with the Python tracker

- **Root stack.** At each block in `0x401000..0x493bff`, entries are popped while ESP > entry ESP, or while the block is the top entry's return address with ESP = entry + 4. A root block pushes `(ESP, [ESP])` unless that pair is already on top. The same-depth follow-on call after a root's RET is therefore logic.
- **Context of an access.** Pops while ESP > entry ESP. A target hook evaluates it, and so pops, only at the first watched byte of the access. A surface hook always evaluates it. EIP is read once per access.
- **Overlapping ranges.** Python registers one read and one write hook per run of watched bytes, widened to `[start-3, end-1]`. Runs separated by 1 or 2 bytes therefore overlap, and Unicorn fires every hook whose range contains the access address. `modo='agrupado'` registers one hook spanning all ranges and replays those firings from a per-address multiplicity table. `modo='por_faixa'` registers the Python layout hook for hook. Both are tested equal to Python.

## Where the time went

Unicorn 2.1.4 walks the whole hook list of a type on every memory access. The M2.2 policy has 154,059 watched bytes in 5,300 runs, so Python registers 5,300 read hooks and 5,300 write hooks. Most of pass 2's cost was that walk, paid on every access of the game, not the Python callbacks themselves. In a micro-benchmark with 5,000 range read hooks, each read cost about 7.5 µs whether the callbacks were Python or native. That is why `agrupado` is the default: a single hook spans `0x496391..0x47982009`, and an access outside every watched range costs one native table lookup. `por_faixa` is kept only as an equivalence check.

## Validation

All runs were on the MacBook (work hours, shared lease slots), at the commit that adds this tooling. Outputs are under `.local/nativo-politica/` and are not evidence. The reference is the committed [M2.2 128-frame policy](../../pesquisas-paralelas/missoes/validacao/m2-2-politica-comparacao-128-quadros.json), sha256 `bf36e6e8f6a38202fa3248256d3de9f768497caa835a563a3ef119be994127f0`. The comparison ignores only `schema`, `source_revision`, `translation_executed`, `evidence` and `seconds`.

**Sequential run.** `politica_ganchos_nativos.py sequencial --quadros 128` ran live pass 1, then native pass 2 through Missions' own `passo2` and `relatorio`. The policy body is JSON-identical to the committed report:
- cumulative `exclusion_mask` equal;
- all 999 `game_logic_bytes` equal, writers and readers included;
- totals 153,060 masked and 999 logic;
- every window equal;
- surfaces equal (0 logic-context accesses, `excluded_with_proof` true);
- every phase state reproduced, `passed` true.

**Segmented runs.** Missions' `segmentos_quadros_missao.py passo-a --cada 32` produced the snapshots, then `preparar-politica` ran from the committed capture. Python and native policy segments 0–32, 32–64, 64–96 and 96–128 ran in pairs on the same windows at the same time. `politica_ganchos_nativos.py comparar` joined each method's four segments. The native join is JSON-identical to the committed report, with the same fields as above. The Python join, made from the same snapshots, is JSON-identical too. This also confirms that the segment tool reproduces the sequential policy.

| Pass 2, phase loop only (seconds per frame) | Python hooks | Native hooks |
|---|---|---|
| Segment 0–32 (includes load_tail) | 8.931 | 1.358 |
| Segment 32–64 | 8.166 | 1.250 |
| Segment 64–96 | 8.026 | 1.254 |
| Segment 96–128 | 8.044 | 1.278 |
| **All 128 frames** | **8.291** (1,061.3 s) | **1.285** (164.5 s) |

- **Speedup:** 6.45× for the pass-2 phase loop.
- **Sequential native run, same machine:** pass 2 took 1.313 s/frame. Pass 1, which has no hooks, took 1.154 s/frame. Each bench start (program start + MissionLoad) took about 75 s and is excluded from both figures.
- **What remains:** native pass 2 costs about 0.13–0.16 s/frame more than an unhooked run. Most of that is the per-phase image summary and the aggregate drain.

**Tests.**
- `test_emulacao_ganchos_nativos` (`RISING_EMULAR=1`): 9 tests.
- The short-window test hooks one live run of load_tail and frames 1–2 three ways at once: Missions' Python closures, `agrupado` and `por_faixa`. After every phase all three give equal `acessos` and `superficie`, key order included. It took 134 s under the lease.

**Missions note.** At `cf08d32` (its latest change), `segmentos_quadros_missao.py passo-a` crashes after it has written every snapshot. The crash is at `dict({0: zero}, **inst)`, because `inst` has int keys, so `passo-a.json` is never written. `segmento` and `comparar` need that manifest; `preparar-politica`, `politica` and `comparar-politica` do not. The policy validation above did not depend on it. The Missions-side fix is `inst = {0: zero, **inst}`.
