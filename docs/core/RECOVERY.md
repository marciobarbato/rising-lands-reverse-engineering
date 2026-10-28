# Live unit healing and fatigue reset

Stage 6 contract, inventoried before implementation on 2026-10-28. Original executable SHA-256: `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`. All ranges below are end exclusive.

| Original body | Range | Public entry |
|---|---|---|
| `EnginAddVie` | `0x457122..0x45718a` | `adicionar_vida_unidade(mundo, indice, acrescimo, tipos_unidades)` |
| `EnginResetFatigue` | `0x4530fd..0x453129` | `resetar_fadiga_unidade(mundo, indice)` |
| `SortieTroupe` continuation | `0x420f6e..0x420f81` | `retomar_recuperacao_saida(mundo, pedido, tipos_unidades)` |

These APIs operate on the existing writable 800 × 276-byte `mundo.unidades` pool. AX index truncates to u16, then the protected model requires 0–799. Healing requires the preloaded 26 × 50-byte type table and current live unit type 0–25; invalid pool/index/table/type fails before mutation. This protection does not claim original behavior for unchecked out-of-table accesses. Neither helper filters activity, owner or life.

Healing adds the low word of EDX to u16 life `+0x9a`, truncates the sum to u16, then compares it to the u16 maximum at `0x4965b6 + type*50` (type record `+8`). The original stores the sum before reading type/maximum and clamps only if the sum is strictly greater. The adapter reuses `unidades.curar_com_limite` first with maximum 65535 for the sum store, then with increment zero for clamping. It returns the caller-visible AL flag as a Python boolean and changes only life. Equality returns false; overflow can produce a lower life. No callbacks are invoked.

Fatigue reset writes u16 `+0x74=0`, then reads u16 `+0x76` and writes it to `+0x04`. It leaves `+0x76` and all other bytes intact. The original has no type-table read or callbacks; unknown type is supported for this helper.

The continuation accepts the conversion handoff with `endereco_dependencia=0x420f6e`, heals the existing unit by literal 1000, then resets fatigue. It returns a new `RecuperacaoSaidaTropa` at `0x420f81`, before `EnginSetExperimente`. The current live unit type supplies the healing maximum; the old conversion type snapshot is diagnostic. The result preserves the building index and exit cell as u16 metadata. This is an explicit one-shot continuation: replay repeats healing. It does not rerun economy or conversion. A failure retains any earlier completed effects; input protection is performed before the first effect.

Remaining original calls are experience `0x44fe42`, placement `0x445fbc`, movement `0x4457d3` (existing core order provider), and conditional sound/request `0x440d5e`, followed by economy-owned cleanup. No complete production, new allocator, occupancy, mission loading, Windows runtime or original-game runtime is claimed by this stage.

REA source revision `b9a8f8e9f25feb9cc97bf4960748f2bdf8c898bc`, Ghidra 12.2 private copy, analyzed normalized PE SHA-256 `26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0`. It supplied focused dossiers and direct call references at `0x420f75`/`0x420f7c`. Its inferred `__fastcall`/`__stdcall` signatures are not authoritative: the original Watcom register inputs and intact-byte/native comparisons define this contract. No POC implementation is imported. [Reviewed REA excerpts](../../evidencias/recuperacao-unidades/rea-reviewed.json) preserve source Evidence IDs, source-record hashes and the distinct analysis/oracle identities. The session was closed after exporting its local bundle.

Implementation: [recuperacao_unidades.py](../../ferramentas/recuperacao_unidades.py), with matching healing/fatigue methods on `MundoUnidades` and subclasses. `RecuperacaoSaidaTropa(indice, unidade, celula, tipo_unidade, endereco_dependencia=0x420f81)` carries the next boundary. Its `tipo_unidade` is the current live type, not the prior snapshot.

Fresh validation: `python3 -B ferramentas/validar_recuperacao_unidades.py --emular` passes ten tests and 2,020 bounded original executions: 624 complete healing returns, 512 complete fatigue returns, 312 recovery caller checkpoints and 572 joined position/conversion/recovery caller checkpoints. Whole unit/structure pools and search state match; native nested calls are unpatched. Healing covers all 26 supported types, both edge indices, strict equality/clamp, u16 overflow and high increment bits; fatigue covers all 256 type bytes, including inactive/unknown-type records. Native faults, limits, failures, errors and skips are zero. The initial Python-only run had one incorrect demonstration expectation: conversion updates `+0x76` before recovery. Correcting that fixture made its expected copied value 4; no implementation change was needed.

Local validation discovers ten tests, executes six, skips four optional x86 tests and runs zero x86. `demonstrar_recuperacao_saida.py` joins the committed economy preparation/query providers, conversion and recovery on shared live buffers: life 50→100, fatigue zero, live `+0x76` copied as 4, pending `0x420f81`. It is synthetic, runs no x86 and does not complete production. Reports are [native](../../relatorios/recuperacao-unidades-emulada.json), [local](../../relatorios/recuperacao-unidades-local.json) and [demonstration](../../relatorios/recuperacao-saida-python.json).

Reproduction also includes `python3 -B ferramentas/extrair_recuperacao_unidades.py` and `python3 -B scripts/check.py --domain core`. The exporter verifies the intact original SHA-256 and records three complete intervals with bytes and interval hashes in [the manifest](../../evidencias/recuperacao-unidades/manifesto.json). Current domain/integration check results are recorded in the handoff after they run.
