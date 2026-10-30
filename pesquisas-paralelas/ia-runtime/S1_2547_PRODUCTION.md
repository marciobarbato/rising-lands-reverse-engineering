# S1 frame 2547: missing recruit continuation

## Finding and ownership

The first planning-mode indicator difference is structure 0 (type 2, `SANCTUAIRE`, cell 2828):
`objective.structures[0][4]` is byte **`0x49a0cd`**, structure offset **+5**. The original changes 4 → 5;
Python retained 4. Structure 1 (type 3, `CAVE`, cell 2579) remains 5 on both sides.

The writer is **Economy's `SortieTroupe 0x420e4c`, instruction `0x4211c1`**:
`c6 42 05 05` (`mov byte ptr [edx+5], 5`). It follows the occupied-structure cleanup at `0x421153`,
including request fields +0x74/+0x7b/+0x7c/+0x7e/+0x80/+0x82/+0x86/+0x8c; state 3 is preserved.
Then it sends unit message 0x46 at CALL `0x4211d3` and city message 3 at CALL `0x4211e5`.
The intact execution oracle is SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

This writer is directly observed in Economy's committed original capture at completion frames 297, 869
and 1363 (`evidencias/caverna-recrutamento/captura-caverna-recrutamento-exibicao.json.xz`), both inside
`CalculTroupe` and as `SortieTroupe`. Its S1 attribution combines that original instruction/capture with
S1's native frame-2547 trace: BagRetire, CalculPosition, EnginSetType, healing/fatigue, experience,
SetSortEngin, movement, sound and both messages execute exactly there. It is not a new S1 instruction trace
or a pass-2 equality claim. Economy's full `CavernaRecrutamento._SortieTroupe` already has the correct store.

**The immediate defect was AI/runtime composition.** The pinned M2 route in
`composicao_encadeada_ia.provedores` passed `Producao.calcular_tropa` directly to
`quadro_economia.ramo_producao_estrutura`. That producer returns an explicit preparation handoff, before
world conversion. The dispatcher discarded the handoff. A fresh planning rerun on clean `5568c00`
reproduced the frame-2547 difference and exposed the discarded value:

```text
PreparacaoSaidaTropa(indice=0, direcao=4, unidade=4, tipo_unidade=7, endereco_dependencia=4327064)
```

4327064 = `0x420698` (CalculPosition). Thus this was more than a missing final status store: conversion,
placement and completion callbacks were missing too. Writing +5 alone would hide the defect.

## Bounded fix

Only the input composition is changed; the historical M2 implementation/evidence stays intact.
`ComposicaoEntrada._donos_quadro` retains Economy's inhabited predicate and one-call ordering, and sends
types 1/2 to `DonosM3.calcular_tropa_entrada(structure)` → the committed full
`caverna_recrutamento.provedor_caverna`, `CalculTroupe` at CALL `0x426983`.
AX is the u16 structure; exit registers are discarded by the structure dispatcher at `0x426988`.
The full provider advances once, then runs `SortieTroupe`, using the existing live owner routes. An absent
provider raises at its real call, retaining earlier progress/Bag changes; there is no retry, rollback or
invented callback. Other production types retain their existing producer, but an unfinished handoff is now
a named dependency at CALL `0x420f5a`, rather than discarded success.

The rerun is equal on the published indicators for frames **129–2546 (2,418 frames)**. At `frame2547`
it now stops on **`EnginSetType required at 0x00420f69; earlier stores retained`**, before conversion;
there is no first difference before that stop. This is a corrected dependency boundary, **not completed
recruitment or whole-state S1 equality**. Planning runs remain diagnostic and stay under `.local/`.

## Exact remaining owner contracts

1. **Economy ABI prerequisite:** `caverna_recrutamento.ARGUMENTOS['EnginSetType']` currently omits **BL**,
   which Core's `incursao_core.definir_tipo_unidade` consumes as direction. Add `EBX: 0xff` and forward the
   actual BL preserved by CalculPosition (`c['EBX']` in `_SortieTroupe`) into the call at `0x420f69`.
   Do not fabricate it in AI/runtime. The six-case bounded native comparison finds BL = 4 at each of its
   three conversion stops, while the emitted callback currently carries AX/DX/CL only. Economy must extend
   its argument comparison/native differential to include BL.
2. **Core conversion adapter / AI/runtime consumption:** the first missing live callback is
   `EnginSetType 0x457b87`, CALL `0x420f69`: AX unit, DX cell, BL direction, CL requested type. Core's
   `incursao_core.definir_tipo_unidade(memory, eax, edx, ebx, ecx, bonus)` already implements the body;
   its exact callback adapter needs the complete arguments above and the live bonus provider. The API
   returns EAX/EBX/ECX/EDX; preserved/unknown register bits must follow the existing explicit protocol.
   After this callback is available, the full producer reaches Core `EnginAddVie` (`0x420f75`, AX unit,
   DX = 1000), `EnginResetFatigue` (`0x420f7c`, AX), `EnginSetExperimente` (`0x420f85`, AX and DX exit cell),
   `SetSortEngin` (`0x420f8c`, AX), then existing movement/voice routes. Those bodies exist in Core's
   production continuations; the raw-memory owner adapter is not bound in `DonosM3` here.
3. **AI/runtime callback prerequisite:** `iagVilleSendMessage` at `0x4211e5` needs a real provider (AX
   structure, DL 3, EBX 0). `mensagem_unidade` already handles the unit message for a non-AI owner;
   city-message handling remains unbound. Keep a named stop if it is reached. Neither callback may be
   replaced with an empty function to obtain a passing frame.

No foreign research file was edited. These are dependency requests, not claims that the later calls have
been reached in the corrected S1 run.

## Validation and reproduction

Fresh leased native prefix comparison: [producao-entrada-prefixo-native.json](validacao/producao-entrada-prefixo-native.json),
**6/6 equal prefixes**, zero byte differences. It executes original `CalculTroupe` directly from six
committed native read-before-write fixtures (296/297, 868/869, 1362/1363), without stubs or crossings:
three return below threshold; three reach the actual `EnginSetType` entry. All touched non-stack bytes
and the provided AX/DX/CL agree. Missing BL is explicitly recorded, so these are not full ABI or completed
recruit comparisons. Native instruction limits remain failures, not success.

```sh
python3 '/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py' ai-runtime-production-prefix -- python3 -B pesquisas-paralelas/ia-runtime/validar_producao_entrada_ia.py --saida .local/m3-1/producao-prefixo-rerun.json
python3 '/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py' ai-runtime-s1-2547 -- python3 -B pesquisas-paralelas/ia-runtime/provar_entrada_ia.py --sonda S1 --ref bab6c7c --quadros 2419 --diagnostico-planejamento --saida .local/m3-1/s1-2547-rerun.json
```

Local diagnostic outputs: `.local/m3-1/s1-2547-baseline-5568c00.json` and
`.local/m3-1/s1-2547-routed.json`; logs `.local/s1-2547-*-20261030.log`. Baseline first difference and corrected
stop are diagnostic observations, never acceptance evidence. The P6 proof at clean source `01c4319`
precedes this bounded fix and retains that source identity; it is not silently relabelled as a proof of the
new source. No new S1 pass-2 pin or unrelated task is started.
