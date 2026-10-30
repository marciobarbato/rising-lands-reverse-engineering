# S1 recruit continuation: Core binding and city message

Implementation source: `bf8ec61c28062da151e74613613a6ec9e9a76686`, after merging
main `6cdbc5a`. Only AI/runtime-owned paths were changed; feature commits were
pushed, with no main merge or acceptance operation.

## S1 reach and first stop

Both fresh indicator runs compare **2,418 frames equal, 129–2546**, with no
first difference. Both stop inside **frame2547** at:

```text
SetSortEngin called at 0x420f8c without its argument register(s) EDX
```

| Mode | Equal frames | First stop | Graphics planning bypasses |
|---|---:|---|---:|
| Strict (default) | 2418 | frame2547, SetSortEngin | Not enabled |
| `--diagnostico-planejamento` | 2418 | frame2547, SetSortEngin | 0 |

Strict report: [s1-recrutamento-strict.json](validacao/s1-recrutamento-strict.json).
Planning diagnostic: `.local/m3-1/s1-recrutamento-planejamento.json` (never acceptance
evidence), SHA-256
`eb9686de089904487297d09312e767e81ead7b4faa5086d6107571613f1165db`. Both use Missions' replay-checked S1 at `bab6c7c`, request the full
16,922-frame post-128 probe, and stop at the first missing dependency. They
compare inputs, orders, counters, RNGs, view, selection, objectives and unit
11–15 whole-record hashes. This is indicator equality through 2546, not a
whole-state proof or a completed frame 2547.

**Next owner: Economy. Exact contract:** `SetSortEngin`, entry **`0x445fbc`**,
CALL **`0x420f8c`**, consumes **AX = u16 unit and DX = u16 exit cell**. Its
`caverna_recrutamento.ARGUMENTOS['SetSortEngin']` still lists only AX, and
`_SortieTroupe` supplies only `EAX=unidade`. Add `EDX: 0xffff` to the argument
mask and pass the actual local `celula`, returned by CalculPosition and
preserved through EnginSetExperimente. Core's committed original S1 case
(`evidencias/recrutamento-core/original.json.xz`, frame 2547, caller return
`0x420f91`) observes **AX = 4, DX = `0x0e0f` (3599)**. These are observations,
not constants to inject. AI/runtime preserves `ArgumentoNaoPassado`; it neither
recovers DX from callback history nor substitutes a default.

Earlier producer effects remain: Bag retirement, conversion, healing, fatigue
reset and experience have already run when placement rejects the missing DX.
There is no retry or rollback. After Economy forwards DX, rerun this same chain;
later movement/sound/messages have not been reached by the current Python S1 run.

## Bound providers and original-first city behavior

`DonosM3` binds Core's `RecrutamentoCore` / `provedor_recrutamento` over the same
live memory. It consumes Economy's updated BL at EnginSetType unchanged and
routes all five recruit calls. A supplied live bonus query is reused; otherwise
Core's `bonus_recrutamento(memory)` resolves the live Economy tables on demand.
Every caller register/mask reaches the adapter unchanged. The seven result
registers and explicit unknown preserved bits are retained. Missing or uncertain
behavior inputs fail before that callee touches memory. Core owns the actual
conversion/healing/fatigue/experience/placement bodies and their bounded domain;
see [the Core contract](../../docs/core/RECRUITMENT_ADAPTERS.md).

City evidence was committed before translation: `14d1cb1` (v1), then `018687a`
(v2 correcting missing cached-block read hooks). V1 remains unchanged and is
superseded for read fixtures. The v2 recorder flushes Unicorn translation blocks
after installing memory hooks and checks owner/player read completeness.

`mensagem_cidade_ia.mensagem_cidade(memory, regs, chamada)` implements
`iagVilleSendMessage 0x484808`, including CALL **`0x4211e5`**, **AX structure,
DL 3, EBX 0**. Structure indices are protected to 0..999. It reads the real
structure owner and Economy's live PlayerGetType query:

- Owner >=4 returns that owner byte; owner 0..3 with player type !=2 returns
  the type byte. EAX is the result, EBX the zero-extended structure, EDX the
  original full EBX. ECX/ESI/EDI/EBP and their unknown masks are preserved;
  optional entry ESP returns ESP+4. These original branches make no non-stack
  stores. The actual S1 call returns EAX=1, EBX=0, EDX=0.
- An AI owner is an explicit **AI/runtime** dependency at **`0x48484c`**, before
  the unbound message dispatch, with owner/message/argument in the error. There
  is no empty callback. Missing EAX/DL/full EBX or uncertain consumed bits raise
  `ArgumentoNaoPassado` before memory access.

The live city route is bound in DonosM3 and validated independently, but the
current Python S1 producer stops earlier at placement. Its caller stores and
later callbacks are not claimed complete by this delivery.

## Native comparisons

Intact execution oracle: RISING.EXE SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
No normalized PE, foreign source hash pins, original evidence replacement,
artificial callbacks or suppressed errors were used.

| Comparison | Native cases | Result |
|---|---:|---|
| Recruit binding | 6 | 6 equal prefixes, 0 mismatches; 3 returns / 3 missing-DX stops |
| City message | 27 | 23 exact returns / 4 named AI-prefix stops, 0 mismatches |
| Input orders | 124 | 118 complete / 6 named stops, 0 mismatches |
| Deposit pages | 203 | 203 complete, 0 mismatches |
| Construction/keys | 90 | 85 complete / 5 named stops, 0 mismatches |

[Recruit report](validacao/producao-entrada-recrutamento-native.json): original
CalculTroupe from the six committed Economy fixtures (296/297, 868/869,
1362/1363), without stubs, through return or before SetSortEngin. Every provided
owner argument (including BL), every changed non-stack byte and the original
native store sequence agree. The three conversion cases execute the four
preceding Core owner calls before the named placement ABI stop.

[City report](validacao/mensagem-cidade-native.json): three real Economy calls,
S1's real frame-2547 call and 23 declared owner/type variants. All 27 native
cases reproduce v2, including complete read fixtures. The S1 trajectory replays
snapshot 2500 through 2547, checks all 48 states against the committed original,
and preserves executable code. Compare all seven result registers (also S1 ESP),
all effects and named stops. Unknown preserved registers and omitted/uncertain
arguments also have focused consumer tests. The four AI prefixes are not
claimed as implemented message handlers.

Fresh native regression reports are [input orders](validacao/entrada-ordens-native.json),
[deposit pages](validacao/paginas-deposito-native.json) and
[construction/keys](validacao/construcao-teclas-native.json). All native load-tail,
between-frames, frame-1, pause and unchanged-code reproductions pass. The six
unloaded-text and five construction/key dependencies remain named; none was
suppressed to increase the passing count. The full differential set is 450 cases:
432 complete returns/comparisons and 18 named boundaries (including the bounded
recruit/city prefixes), with zero mismatches. This total excludes duplicate
full/partial adapter checks and CPU-free replays of the same native cases.

## Reproduction

All native runs and gates use
`/Users/marcio/git/Rising Lands/local-data/coordination/heavy_lease.py`:

```sh
python3 /Users/marcio/git/Rising\ Lands/local-data/coordination/heavy_lease.py ai-runtime-recruit -- python3 -B pesquisas-paralelas/ia-runtime/validar_producao_entrada_ia.py --saida .local/m3-1/recruit-rerun.json
python3 /Users/marcio/git/Rising\ Lands/local-data/coordination/heavy_lease.py ai-runtime-city -- python3 -B pesquisas-paralelas/ia-runtime/capturar_mensagem_cidade_ia.py --comparar --saida .local/m3-1/city-rerun.json
python3 /Users/marcio/git/Rising\ Lands/local-data/coordination/heavy_lease.py ai-runtime-s1 -- python3 -B pesquisas-paralelas/ia-runtime/provar_entrada_ia.py --sonda S1 --ref bab6c7c --saida .local/m3-1/s1-strict-rerun.json
python3 /Users/marcio/git/Rising\ Lands/local-data/coordination/heavy_lease.py ai-runtime-s1-plan -- python3 -B pesquisas-paralelas/ia-runtime/provar_entrada_ia.py --sonda S1 --ref bab6c7c --diagnostico-planejamento --saida .local/m3-1/s1-plan-rerun.json
```

Native city recapture requires the existing frame-128 inputs and S1 snapshot
2500 under ignored `.local/m3/`, as Core's `bancada_s1` documents. Initial
harness setup attempts exposed a missing repository bootstrap, write-only native
fixture pages and absent local snapshot inputs; each was corrected and rerun.
The incomplete v1 read-hook capture is preserved, marked superseded, and not
used by the translation or tests. No failed setup attempt is counted as a pass.
