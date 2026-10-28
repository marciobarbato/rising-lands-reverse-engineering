# AI and runtime contract

Owner: the AI and Runtime front (`feat/re-ai-runtime`, `worktrees/re-ai-runtime`). Owned paths are `pesquisas-paralelas/ia-runtime/` and this manual. The front composes the committed Core VM/task primitives and the other owners' simulation APIs into the original frame, unit and structure dispatchers and the AI player kernels. It does not copy, fork or silently alter a sibling implementation; a needed change in a core primitive is requested as a contract in the handoffs. Addresses apply to executable SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

This manual starts as a coordinator skeleton. Its first owned stage is to replace every "to be inventoried" item below with original-byte evidence and agreed ownership before any implementation.

## Ownership boundary with Core and Missions

| Area | Core keeps (`ferramentas/`) | AI/runtime implements (`pesquisas-paralelas/ia-runtime/`) | Missions keeps |
|---|---|---|---|
| AI orchestration | `ia.atualizar_ia` order/returns for `iaCalculPlayer 0x47f927`, the `chamar(address, *args)` callback protocol, `EstadoIA` | The five callback bodies: `iagUnitNoyau 0x482936`, `iagVilleNoyau 0x48453c`, `iagRessNoyau 0x485183`, `iagWarNoyau 0x4866d7`, `AvanceMonstre 0x47b283`; `iagUnitDeleteAllGroups 0x483d95` | Mission number/attack table inputs loaded from disk |
| Rule VM | `tarefas_ia.MaquinaTarefas` (task memory, lists, waiting, control flow, arithmetic operations), `simbolos_ia` (SBL/RUL decoding), `ordens_unidades.OPERACOES` (the five unit operations already reconstructed), `mensagens_chegada` profiles | The remaining world operations registered through the `operacoes` dictionary of `MaquinaTarefas`, grouped by original address (140 names, 1,157 instructions, 64 entries in `relatorios/regras-ia.json`) | Objective/end-condition tables their callers consume |
| Messages | Arrival/state-change profiles | `iagUnitSendMessage 0x4829c8`, `iagVilleSendMessage 0x484808`, `I_AttenteMessageBatiment 0x482697`, group/city mailbox tables | — |
| AI tables | — | `iaInit 0x47f328`, `IaReset 0x47f36e`, `listInit 0x47cfd0`, `iagUnitInit 0x4826a4`/`Reset 0x48270b`, `iagVilleInit 0x484214`/`Reset 0x484310`, `iagRessInit 0x484bc4`/`Reset 0x485002`, `iagWarInit 0x48614c`/`Reset 0x4864c1`, `iaProbInit 0x47d1a4`/`Reset 0x47d220`, `IAResetAttaque 0x47c162` | `IALoadAttaqueIni 0x47c24d` disk loader (done) |
| Frame loop | `cadencia` counters/draw predicate/RNG step | `0x47500e` outer cycle order, `CalculGame 0x42c868` with its three gates (`0x42d14c`, `0x42d2e3`, `0x42d3c0`), `GameNextFrame 0x45d015` | `EvenementInit/EnCours/Affiche/End` bodies, `TestFinDeMission 0x458606` |
| Unit dispatcher | Movement, arrival, orders, tasks, physical death bodies | `CalculEnginNextEtape 0x456db5` state dispatch and per-state call order, delegating to core (movement/dying), combat (`CalculAttaqueEngin 0x451914`), economy (`CalculWorkEngin 0x44bc74`, `CalculTransporteEngin 0x44f2d4`), `CalculEnginStatic 0x453062` | — |
| Structure dispatcher | Gate branch (type 12) | `CalculBatimentNextEtape 0x4281c7` skeleton and branch order, delegating production (`CalculTroupe`), construction, repair, market and nova branches to economy and the gate branch to core | — |
| Input | — | `InputGame 0x429278`/`ProcessInputGame 0x45edc0` dispatch (second wave; not needed for an input-free mission comparison) | — |

Anything not in this table is decided in the contract stage and recorded in the three handoffs (`pesquisas-paralelas/ia-runtime/HANDOFF.md`, `docs/core/HANDOFF.md`, `pesquisas-paralelas/missoes/HANDOFF.md`).

## Public API shape

APIs are published only after original comparison. The intended shapes follow the repository conventions: explicit inherited buffers with exact widths, read-only query callbacks, effect callbacks named after original routines, named dependency exceptions carrying the original call address, partial effects retained, no replay guard disguised as a continuation.

| Planned entry | Original | Inputs | Result |
|---|---|---|---|
| `reiniciar_ia(tabelas)` | `IaReset 0x47f36e` → `iaInit` and the table initializers | Explicit AI table allocations with original widths (to be inventoried) | Ordered store trace; no mission or player semantics |
| `quadro_jogo(mundo, provedores, *, entrada=None)` | `CalculGame 0x42c868` | Live world (core/missions buffers), provider bundle per branch, optional scripted input | Per-frame checkpoint metadata and the list of reached dependencies |
| `proxima_etapa_unidade(mundo, indice, provedores)` | `CalculEnginNextEtape 0x456db5` | Unit index, provider bundle | Branch taken and provider result |
| `proxima_etapa_estrutura(mundo, indice, provedores)` | `CalculBatimentNextEtape 0x4281c7` | Structure index, provider bundle | Branch taken and provider result |
| `operacoes_mundo(mundo, provedores)` | `iaSolver` world operations | Returns the `operacoes` dictionary for `MaquinaTarefas` | Each operation stops explicitly when its world provider is missing |

## Validation

Every stage keeps the repository rules: exported intact intervals, original-only captures before translation, fresh bounded native comparisons on core's harness with whole-state equality, local tests that skip native cases explicitly. The frame oracle described in [the roadmap](ROADMAP_MONDE01.md) runs `CalculGame` natively from a loaded MONDE01 snapshot with declared clock/sound/import bindings and compares the whole state after each frame with the Python driver.

```sh
python3 -B scripts/check.py --domain ai-runtime
RISING_EMULAR=1 python3 -B -m unittest discover -s pesquisas-paralelas/ia-runtime/testes -p 'test_*.py' -v
```

`pesquisas-paralelas/ia-runtime/testes/test_namespace.py` enforces unique module basenames across the flat research namespace and rejects copies of core primitives.

## Stages

1. **Contract stage (no implementation).** Inventory from original bytes: the `0x47500e` cycle and `CalculGame` call order with its gates; `CalculEnginNextEtape` state table and the routine reached by each state; `CalculBatimentNextEtape` branch table; `iaCalculPlayer` callbacks; AI table addresses/widths touched by `iaInit`/`IaReset`; the 140 operation addresses grouped by the world provider they need. Publish ownership and the requested contracts; integrate.
2. **AI table initializers** for `MissionLoad`'s `IaReset` tail (M1).
3. **Frame skeleton** `CalculGame` with committed providers and named stops; frame oracle (M2 entry).
4. **Unit dispatcher** for the states present in MONDE01 (0, 7, 14 at load; movement/work/transport/attack as they arise), then the structure dispatcher skeleton.
5. **AI kernels and operations** required by the first MONDE01 raid (`iagWarNoyau`, group movement, `V_AttaquerBatiment`, `B_TestUniteDanger`, `I_DonneForce*`), then the remaining operations by frequency in the rule program.

Status and results live in `pesquisas-paralelas/ia-runtime/HANDOFF.md`.
