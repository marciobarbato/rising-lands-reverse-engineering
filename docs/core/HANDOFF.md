# Core handoff

Status: sequential core research in the authorized continued research round on 2026-10-28. Stages 1–10 are remotely integrated. Stage 11 global unit/raw Bag reset is independently validated, awaiting required integration. Its original body/dependency contract was inventoried before implementation.

The human authorized continued sequential research after that first slice. See the [remaining dependency inventory](REMAINING.md), published before the next implementation. The clean feature worktree resumed through the helper and incorporated remote main `ff4bc269c6d8534f4683bd0429072286ea8eaaf1`. Each stage must be committed and remotely integrated before the following implementation begins.

Stage 2 implements complete `CalculPosition` (`0x420698`) and both shared epilogues, closing economy's position-query dependency for all 22 structure types. See the [precise exit-position contract](EXIT_POSITION.md). `calcular_posicao_saida(mundo, indice, direcao=0, dimensoes=None)` reads the shared 1,000-record pool, truncates index/direction to u16/u8, accepts explicit u16 width/height overrides, and returns the caller-consumed u16 cell. Direction is unused; types 9/12/17 return zero. There are no callbacks, mutations, passage checks or conversion effects. Protected invalid inputs raise `ValueError`. Original code/hash/table addresses and arithmetic are fully recorded in the contract.

Stage 2 actual validation: `extrair_posicao_saida.py` exports three original code intervals, 11 jump tables and 22 geometry pairs. `capturar_posicao_saida.py` produced 22 independent original-only calls before translation. `validar_posicao_saida.py --emular` passed 10 tests and 7,546 additional complete x86 calls, zero skips/errors/failures/dependency stops/exceptions/limits. Local mode discovered 10 tests, executed six, skipped four optional x86 tests, and ran zero x86. `scripts/check.py --domain core` passed 248 discovered tests with 122 optional skips. No historical x86 aggregate or real mission was rerun. Integration outcome is reported to the coordinator after the required helper completes.

The next dependency after Stage 2 is remotely integrated is existing-colonist conversion through `EnginSetType` (`0x457b87`), followed by the rest of production's world effects. The caller must reload building `+7b` after the position call. Combat's new unit-only wrapper also requests exact resolver/navigation callbacks; they remain recorded in the inventory rather than implemented by analogy.

Completed Stage 2: implementation `61e2a2e1201b7e0e020906bb67963a17e5364a8c`, final feature `08fbf98fdef813f33053d242cd1056e87f4b27b7`, remote-main merge `82122a2c790c835c455253b7cb701558ffcbfcca`. Required integration checks passed: core 248 (122 skips), combat 124 (76), economy 229 (101), graphics 82 (0), workflow 3 (0). The clean feature worktree resumed through the helper again before Stage 3. Detailed provider inspection found the existing `EnginSetType` implementation under combat; the next stage reuses it instead of duplicating it. A type-4 modifier-callback partial-order correction has been requested from that owner before claiming its exceptional path matches native memory.

Stage 3: [shared conversion contract](CONVERSION.md). Public `converter_unidade` takes live core state, u16 index/cell, u8 direction/type, a preloaded 1,300-byte type table and explicit read-only capacity/modifier callbacks; `retomar_conversao_saida` resumes economy's pending handoff through original `0x420f5a..0x420f6e`, returning a new pending result before healing. Live memoryviews and `_liberar_busca` preserve earlier mutations on callback failure and retain `busca.concluida`. No occupancy, healing, production cleanup or allocation is claimed. It reuses committed combat local conversion and economy `BonusUnidades`/`capacidade_tipo`; no sibling implementation is duplicated.

Stage 3 consumed owner commits: combat callback-order fix `fbb5c7067b67f8a70190b0c5d7adebd119a61ceb` at main `aee255d6669285e77f8b528c34836c6500bba6f4`; economic queries at main `7325cd0a3cb54d80d10a0c62c7d61bd25b0f8c49`. Initial run 11 tests/1,985 native calls exposed one type-4 frame discrepancy; that was not a pass. Final `validar_conversao_saida.py --emular` passes 12 tests/1,986 native executions, zero skips/failures/errors/native exceptions/limits: 832 returns, 1,144 caller checkpoints before healing, four capacity stops, four selector-1 stops, two selector-12 stops. Ten Python `NotImplementedError` cases are intentional comparisons to native pre-query boundaries. Local mode executes eight tests and skips four x86 tests (12 discovered). Core check passes 260 discovered tests, 126 optional skips. Shared-buffer Python demo joins actual economic preparation and query providers to core conversion; zero x86, no real mission. Required integration result will be reported to coordinator before the next stage starts.

Global gap addressed by Stage 3 is the shared-state connection across production preparation, positioning and local conversion; it is independently validated and ready for integration, with no loaded-mission runtime claim. Next selected core dependency after integration is `EnginResetCapacite` (`0x4475ef`), requested by economy's bonus setter. Remaining production world effects, lookup/navigation callbacks and real-mission dispatch stay open; the coordinator's coarse global estimate is not inferred from these test totals.

Completed Stage 3: implementation `90fdfa51ab2bb2243d1e81fbd6bc7ab9548c89fa`, final feature `1f666a86da87ce0295f3d1c00504f63cd6f397c5`, remote-main merge `08790abc0cc2286436e1fe1fbe2d43e64a377789`. Required helper passed core 260 (126 optional skips), combat 141 (88), economy 257 (113), graphics 94 (0), workflow 3 (0). Feature worktree was clean and resumed through the helper before Stage 4. The global gap is integrated and independently validated, with a joined synthetic exercise; real-mission operation remains unsupported. Coordinator estimate remains approximately 50%, uncertainty 40–60%, independently of the test totals.

Stage 4: complete `EnginResetCapacite` (`0x4475ef..0x447676`, shared epilogue `0x440d55..0x440d5e`) implemented as `atualizar_capacidades_unidades(mundo, jogador, *, capacidade_tipo=None, modificador=None)` and a matching world method. See the [exact contract](CAPACITY_REFRESH.md). Input owner truncates to u8; 800-slot order, states other than 0/4, matching owner, capacity query then selector-1 query, and u16 unit `+0c` store follow the original. Bonus is queried even for neutral owners. No Bag clearing/count clamp, unit allocation, ownership transfer or navigation effect occurs. Missing/raising read-only providers retain earlier stores; invalid pool is rejected before mutation.

Stage 4 actual checks: exporter records two original-byte intervals with the original EXE hash. `validar_capacidades_unidades.py --emular` passes 10 tests/284 bounded executions: 278 complete scans and six expected conditional query stops (indices 0/7/799, capacity/bonus call positions). Native nested queries total 5,016 capacity and 5,013 bonus calls; these are not additional top-level execution counts. Six Python dependency exceptions are intentional; native exceptions, limits, errors, failures and skips are zero. Local mode discovers 10 tests, executes six and skips four x86 tests. Core check passes 270 discovered tests with 130 optional skips. The actual committed economy providers are used; no historical totals or real mission are rerun.

Global gap addressed by Stage 4 is the live-world capacity refresh required after an economy bonus mutation; implemented and independently validated, integration pending. Full setters/bonus loading, production world effects, physical death/navigation and mission runtime remain open. After this stage is committed and integrated, the next high-value investigation is original `SetDyingEngin` (`0x444938`) requested by combat; its exact body/dependencies must be inspected before selecting an implementation boundary. No death behavior is inferred from the name.

Completed Stage 4: implementation `d458ea71838ff3dc0e30dbc5ec027996e2976420`, final feature `09e3fd8e94ae6b08a580e5cca672fed56585824e`, remote-main merge `8126f1aed299e19337e2b1ac4f95cfa85c068214`. Required helper passed core 270 (130 optional skips), combat 146 (91), economy 268 (119), graphics 101 (0), workflow 3 (0). Clean feature worktree resumed through the helper before Stage 5. The global gap closed is an integrated and independently validated capacity-refresh provider; loaded-mission operation remains open, and the coordinator's approximately 50% estimate (40–60%) is unchanged by test counts.

Stage 5: [physical dying contract](PHYSICAL_DYING.md), API `iniciar_morte_unidade(mundo, indice)`/world method, original `SetDyingEngin` `0x444938..0x444dad` and shared epilogues. AX index truncates to u16 then requires 0–799. Complete ordinary type domain is 0–10/18–25, with hidden cell, no AI group effect, inactive sound, empty Bag and unselected record. It writes state 4, releases matching navigation search while retaining completion flag, clears `+a4`/u16 `+c2`, and removes current/reserved collision. It preserves life; combat's caller owns life zeroing. Inactive state 0/4 with special bit clear is a no-op, even with unknown type/unresolved fields. Other branches raise `DependenciaMorteUnidade` at original checkpoints, preserving prior effects; entry retry is not a continuation.

Stage 5 actual checks: exporter records 14 original-byte intervals and the seven-entry effect table. Final `validar_morte_unidades.py --emular` passes 10 tests/283 native executions: 264 complete original returns and 19 intentional dependency stops (special flag/group/active sound/visible-cell sound/Bag/selection/effects). Whole physical, unit/structure/group/search, routes, discovery/light and minimap buffers match. Native subcalls are unpatched. Nineteen Python dependency exceptions are expected; native faults, limits, failures, errors and skips are zero. Local mode executes six tests and skips four x86 tests (10 discovered). Core check passes 280 discovered tests/134 optional skips. No old aggregate or actual mission is rerun.

Stage 5 global gap is a concrete physical dying provider for the declared common-unit subdomain, ready for integration, without complete lifecycle or mission-runtime claims. Combat must share live record views with core rather than copy its preceding life writes. Remaining AI group/sound/Bag/selection/projectile/special-flag/level/final-removal effects stay explicit. Integration hashes and the next selected dependency will be reported before new implementation begins.

Chat: `01a18262-b95b-7bd2-b73f-1fc0429cf009`. Worktree: `/Users/marcio/git/Rising Lands/worktrees/re-core`. Branch: `feat/re-core`, based on organization commit `6634be3af2d255846a847d8aa21ad4edf1cdb589`. The final feature/integration hashes are reported in the coordinator response after the clean-tree helper completes; this file does not embed its own future commit hash.

Completed Stage 1: feature `7a24e974384782e66d6c7454fe1343035e1178db`, successful remote-main merge `ff9b32f77023e8909c8c517a9e894babc66ce2f0` through the required helper. The feature was clean before Stage 2 resumed.

The [precise contract](STRUCTURE_LIFECYCLE.md) specifies input sizes, widths, ordered mutations, retained bytes, failure behavior, original hashes/addresses, and reproduction commands. Public raw-buffer entries in `ferramentas/ciclo_estruturas.py` are `inicializar_registros_estruturas`, `resetar_todas_estruturas`, `resetar_estrutura`, and `buscar_estrutura_livre`. `MundoUnidades` exposes matching methods using its 276,000-byte structure pool, 88 raw flag bytes and eight selection bytes. Calls are explicit and invoke no callbacks. Invalid model inputs fail before mutation; valid reset indices are truncated to u16 then checked against 1,000. The query returns the first state-zero slot or `0xffff` without reserving it.

Original executable SHA-256: `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`. Newly exported evidence covers `BatimentAlloc` prefix `0x418e95..0x419004`, full `BatimentResetAll` `0x41a75c..0x41a860`, full `ResetBatiment` `0x41b9d6..0x41ba49`, `CreerBatiment` scan `0x41fea2..0x41ff04`, and its failure epilogue `0x4202c1..0x4202ce`. Ranges are end exclusive. Startup stops before economic Bags/player tables/characteristic loading; the free query stops before costs and all remaining creator effects.

Actual checks: new evidence exporter emitted five hash-checked intervals. `python3 -B ferramentas/validar_ciclo_estruturas.py --emular` passed 12 tests and 648 bounded original-x86 executions, with zero skips/failures/errors, zero expected exceptions and zero limits. Reached stops: seven startup boundaries at `0x419004`, six free-scan success boundaries at `0x41ff04`, 635 normal returns. `python3 -B ferramentas/validar_ciclo_estruturas.py` passed seven executed Python tests and explicitly skipped five x86 tests (12 discovered, zero x86). `python3 -B scripts/check.py --domain core` passed 238 discovered tests with 118 optional-x86 skips. The first sandbox x86 attempt exited 132/SIGILL before results; an authorized JIT-capable rerun passed. Historical aggregate x86 totals were not rerun. `demonstrar_ciclo_estruturas.py` records the synthetic world integration, including unchanged terrain after resets; it runs no x86.

Graphics contract: gate u8 `+76` and full u16 `+7c` remain the inputs. Startup/global reset clear the counter; single reset retains it and clears orientation. Rendering remains graphics-owned. Economy's `SortieTroupe` uses an existing colonist; Stage 2 closes its `CalculPosition` query and Stage 3 connects local conversion, while remaining production world effects stay open. No fresh allocator is provided for that path. Combat's lethal-unit/world-impact callbacks remain unsupported and unchanged.

Remaining gaps: full `BatimentAlloc`, `CreerBatiment` cost/reservation/creation pipeline, complete teardown/destruction, unit conversion/production, real mission loading/remapping, global dispatch/cursor gate selection, vision/minimap lifecycle, and cross-domain game integration. Existing terrain APIs remain separate; a pool reset does not remove physical occupancy or prove a playable mission. No original media, immutable report, predecessor evidence, shared script, app, or sibling-owned file was modified.

Integration procedure: commit only owned paths, run `python3 scripts/workstream.py integrate core` from this clean feature worktree, and report its actual remote-main result to the coordinator. Authorization includes commit, feature push, and non-force main integration; no additional approval is needed from the human.


Completed Stage 5: implementation `913a4ada5bb931e276d57f606b12c5858efc36da`, final feature `c1bda16661201942b61653b805e66c06f5c82255`, remote-main merge `5e2bf0831d3aaa776481a6ab023be262ef0df1bd`. Required integration checks passed: core 280 (134 optional skips), combat 163 (102), economy 289 (129), graphics 108 (0), workflow 3 (0). The clean worktree resumed from that committed main before Stage 6.

Stage 6: [live recovery contract](RECOVERY.md). Complete `EnginAddVie` `0x457122..0x45718a` and `EnginResetFatigue` `0x4530fd..0x453129` are exposed as `adicionar_vida_unidade(mundo, indice, acrescimo, tipos_unidades)` and `resetar_fadiga_unidade(mundo, indice)` with matching world methods. Index truncates to u16, then requires 0–799. Healing requires bytes/bytearray type table length 1300 and live type 0–25. Protected invalid inputs fail before mutation. There are no activity/owner guards or callbacks. Healing reuses existing u16 arithmetic, stores the sum before the live type/maximum read, then strictly clamps; returns AL as bool. Fatigue clears u16 +74 then copies +76 to +04. All other unit/search/world bytes remain intact.

`retomar_recuperacao_saida(mundo, pedido, tipos_unidades)` consumes conversion's pending `0x420f6e`, heals the existing unit by literal 1000, resets fatigue and returns `RecuperacaoSaidaTropa(indice, unidade, celula, tipo_unidade, endereco_dependencia=0x420f81)`. Its metadata truncates to u16; live type supplies the maximum and new diagnostic type. It is one-shot: replay repeats healing. It neither reruns economy/conversion nor completes recruitment. Experience/placement/movement/conditional audio and economic cleanup remain pending. Future failures must preserve completed effects.

Stage 6 actual checks: original-byte exporter and independent audit verify three complete code intervals and hashes. REA revision `b9a8f8e9f25feb9cc97bf4960748f2bdf8c898bc`, Ghidra 12.2 private session supplied focused function/caller observations from normalized analysis SHA `26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0`; reviewed Evidence excerpts preserve that identity separately from intact-original oracle SHA `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`. Inferred signatures were checked against original register behavior. No POC implementation was imported; the private session exported and closed.

Final `validar_recuperacao_unidades.py --emular` passes ten tests/2,020 native executions: 1,136 complete helper returns (624 healing, 512 fatigue), 312 recovery-only caller checkpoints and 572 joined position/conversion/recovery checkpoints at `0x420f81`. Native subcalls are unpatched. Whole unit/structure/search state matches; native faults, limits, failures, errors, dependency exceptions and skips are zero. Initial local run had one stale fixture expectation for +76 already changed by conversion; correcting it required no implementation change. Final local run discovers ten tests, executes six and skips four optional x86 tests. Core check passes 290 tests with 138 optional skips. Synthetic shared-buffer economy/conversion/recovery demo reaches life 100 from 50, fatigue zero and copied live word 4, then stops before experience; zero x86 and no actual mission.

Stage 6 concrete gap addressed is the live healing/fatigue connection after recruitment conversion, independently validated and ready for required integration. This advances the production dependency without claiming complete output placement or runtime. After integration, the next bounded investigation is the original experience queue `EnginSetExperimente` and nested `EnginSetLevel`, followed by physical placement; signatures/names alone will not establish equivalent behavior. Coordinator's global estimate is independent of these test totals. Core continues within owned paths and uses the shared helper for feature/main pushes.


Completed Stage 6: implementation `3b7f71697095ab12e960bf4cbdf0952d20d554d8`, final feature `68fd0b8388cf11ac8175405ac995d4e486af2ee6`, remote-main merge `62b9d76941dbcf90a2dc5d45b71317136c8b5d28`. The required helper passed all common local suites; core 290 (138 optional skips), graphics 115 (0), workflow 3 (0). Combat/economy also passed; their detailed counts were not retained in the terminal summary. No all-domain native rerun is implied. Clean feature worktree resumed through the helper and fast-forwarded to that main before Stage 7.

Stage 7: [experience queue contract](EXPERIENCE_QUEUE.md), complete original `EnginSetExperimente` `0x44fe42` and its nested original SBL `EnginSetNewExperience` `0x44f9e0`. This corrects the earlier informal EnginSetLevel name; it does not supply combat's `EnginSetLevelExperience` `0x44fb20`. APIs are `aplicar_nova_experiencia(mundo, indice, nivel, tipos_unidades=None)`, `consumir_experiencia_unidade(mundo, indice, tipos_unidades=None)` and `retomar_experiencia_saida(mundo, pedido, tipos_unidades=None)` in `experiencia_unidades.py`. The world owns a raw mutable `experiencias_unidades` table of 40 bytes for four owners, initialized synthetically to zero. Actual mission initialization/loading remains the missions owner's responsibility.

Index truncates to u16 then requires 0–799; level truncates to u8. Local effects write only the selected F5–F8 field; levels 0/5–255 are no-ops, with no activity guard or AF mutation. Type data is needed only on its original table-read branches, with exact u32 doubling/division/u8 truncation. Queue guards read first experience then type, with no search of later entries. A match writes AF, applies local effects, then shifts four pairs (experience then type) and clears final value before writing FF type. Missing type data raises `DependenciaExperienciaUnidade` at `0x44fa71`/`0x44fafa`, retaining AF and the unshifted queue. Protected invalid owner/table/pool inputs are documented separately from native unchecked behavior. No physical callbacks run.

The production handoff consumes `0x420f81` and returns `ExperienciaSaidaTropa` at `0x420f8a`, before placement. Its saved cell is still the original EDX consumed by SetSortEngin because the experience helper preserves EDX; the native caller comparison verifies this directly. It does not rerun healing/economy/conversion or finish recruitment.

Stage 7 actual validation: five intact-original code intervals and one jump table exported and independently audited. Focused REA dossiers from the pinned revision/private Ghidra 12.2 copy were reviewed with separate normalized analysis/original hashes; original symbol names/registers/bytes remain authoritative and the session is closed. Final `validar_experiencia_unidades.py --emular` passes 12 tests/3,785 original executions: 3,201 returns, 572 full joined-prefix checkpoints at `0x420f8a`, and 12 intentional pre-read dependency stops. Whole unit/structure/search/owner-queue buffers match. Twelve differential Python dependency exceptions are intentional; native faults, limits, failures, errors and skips are zero. Local mode executes seven tests, skips five optional native tests and runs zero x86. Synthetic queue demonstration reaches AF=129/F8=30 and the exact shifted queue before placement; no real mission or complete production claim.

Stage 7 closes the local queued-experience dependency after live recovery. It is independently validated and ready for integration. Remaining shared production calls are physical placement `0x445fbc`, the existing movement-order body, conditional request/audio and economic cleanup. Following successful integration Core will investigate placement using existing occupancy/discovery/light/minimap primitives. Complete mission loader/remapping/orchestration work now belongs to the authorized missions chat; Core retains lower world/navigation/pool/task/VM primitives and supplies committed contracts. The coordinator owns the global estimate; these native counts do not measure project completion.

Stage 7 core domain check passed 302 discovered tests with 143 optional x86 skips and documentation links valid. Required clean-tree integration follows the owned commit; final hashes are reported separately without amending a commit to insert its own future merge hash.


Completed Stage 7: implementation `f67898b75423adcfaf90a7b6e6c710c409e6f9ee`, final feature `fa5e970ea5d1abf7b03b6dc3bf4d17016f9914a4`, remote-main merge `dae42125f45c348c10dff7e727e803138be7670f`. Required helper passed core 302 (143 optional skips), combat 178 (111), economy 316 (142), graphics 115 (0), workflow 3 (0). Clean worktree resumed through the helper and fast-forwarded to that committed main before Stage 8.

Stage 8 inventory: [physical exit contract](UNIT_EXIT.md), original `SetSortEngin` `0x445fbc..0x446189` and shared epilogue `0x4431fb..0x443203`. `colocar_unidade_saida(mundo, indice, celula)` uses the same live physical world and existing `ocupar`, discovery/light and minimap bodies, without duplicating them. U16 index/cell inputs, known type/owner, in-map cell, local camera and 128×128 minimap are protected before stores. Original ordered record stores, matching search release, inactive-state preservation, collision insertion then +72=1 and owner-specific vision/minimap order are retained. It does not remove previous occupancy. Initial supported vision sum BB+F5 is 0–8; larger sums stop at original discovery call, with prior effects retained.

`retomar_colocacao_saida(mundo, pedido)` consumes experience handoff `0x420f8a`, runs placement, reloads live building +7c and delegates to committed `definir_movimento`, then returns `ColocacaoSaidaTropa` at `0x420f9e`. It is one-shot because replay can duplicate light counts. Conditional owner/request/audio and economy cleanup remain pending, along with actual movement advancement. Loader/orchestration remains missions-owned.

Stage 8 evidence before translation: three original code intervals exported and independently audited; focused pinned REA dossiers reviewed for original collision/exit calls, with separate normalized/original identities and closed private session. Four original-only full-record/full-pool/physical-buffer-hash/effect-trace captures completed before translation and all match local Python. Initial capture attempt did not reach its stop under harness cap: the observer read three registers at every instruction. Filtering it to relevant call entries allowed all four captures with intact instructions and unchanged limits. That unsuccessful attempt is recorded separately, not called a pass. Six local tests pass and five optional native tests skip; core check passes 313 discovered tests with 148 optional skips. Broader original differential validation is still running; integration awaits its outcome and full owned diff review.


Final Stage 8 validation: the full native matrix passes 12 tests, 846 original entries in 1,038 bounded segments. Ordinary matrix: 666 actual returns, 156 caller checkpoints at 0x420f9e (52 placement/order and 104 joined prefixes), six pre-discovery stops. Expanded empty-light radius edges: 18 original entries complete through 192 preserved-state SetMiniMap entry resumptions. Every resume counts separately; original code/subcalls remain unpatched and limits are unchanged. Full unit/structure/group/search/routes/physical/vision/minimap/queue buffers and native effect traces match. Six Python dependency exceptions match the original pre-discovery boundaries. Final native faults/limits/failures/errors/skips are zero. Four independent pre-translation original captures are a separate earlier run.

The initial broad run (819 segments, one cap error) is preserved; a faster equivalent byte-interval guard then passed the same 828-entry monolithic matrix. A separate empty-light radius-8 diagnostic reached exactly one million instructions at 0x46a505; final segmented validation closes that gap through actual 0x46a388 entries with CPU state preserved, maximum 55,454 instructions per resumed segment. No failed run is relabeled as successful. Final local mode executes six tests and skips six optional x86 tests (12 discovered). Core check passes 314 discovered tests with 149 optional skips. Synthetic demo reaches current/step0x808, requested destination0x909, state2/+72=1, preserving search completion77 and previous occupancy. No movement arrival, audio, production cleanup or loaded mission is claimed.

Stage 8 closes live physical production output and the movement-order connection through 0x420f9e, ready for integration. Conditional owner/EnginAsk to 0x420fb7 remains open before economy cleanup; bigger vision/minimap/input domains remain explicit. Following integration, Core will close missions' small SelectionInit 0x472555 prerequisite before the next larger investigation. Missions also records distinct PlaceEngin 0x456fa6 and Chemin_Remap 0x42ee1c (including clear-before-allocation failure semantics) as lower dependencies; they are not inferred equivalents of the production body. Coordinator retains the global estimate independently of these counts.


Completed Stage 8: implementation `6b3882b5b4a3a0c99dddcaccbd4d1c08a765f8ce`, final feature `3b0a43596f63548e88cac0edee98876130beaba5`, remote-main merge `aa9cba47af34aef3b0b4b67faded0b884bb1e428`. Required helper passed core 314 (149 optional skips), combat 198 (123), economy 337 (151), graphics 129 (0), workflow 3 (0). Clean feature worktree resumed through the helper and fast-forwarded to that main before Stage 9.

Stage 9: missions requested exact original `SelectionInit` `0x472555..0x472576`, 0x21/33 decimal bytes. [Selection contract](SELECTION_INIT.md) was inventoried before implementation. Public `selecao_unidades.inicializar_selecoes_unidades(selecoes)` takes a writable bytearray of exactly 2048 bytes and writes u16 zero in order at offsets 0/512/1024/1536. World raw `selecoes_unidades` and matching method expose the same allocation. Every list-tail byte and every unit +bd flag remains untouched, with no unit reads, callbacks or dependencies. Malformed/read-only buffers fail before mutation. Constructor zeros are synthetic, not proof of mission loading; missions owns the caller/orchestration.

Stage 9 actual validation: one original interval exported and all 33 bytes independently audited against intact executable SHA 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb. `validar_selecao_unidades.py --emular` passes five tests / 262 actual original returns, whole 2048-byte selection allocation and 220800-byte unit pool match, and EAX/EDX preservation is verified. Native faults/limits/dependency stops/failures/errors/skips zero. Local mode executes three tests and skips two optional x86 tests (five discovered). Core check 319 tests / 151 optional skips passes. World-method tests demonstrate shared-state retention without mission or Windows runtime. This closes the selection prerequisite independently; loaded-unit stream and later mission providers remain separately owned and bounded.

Stage 9 is ready for required integration. Afterwards production's conditional owner/request fragment 0x420f9e→0x420fb7 remains a useful next bounded dependency for economy; physical mission PlaceEngin 0x456fa6 and Chemin_Remap 0x42ee1c remain explicit lower-world requests. No overall completion fraction is inferred from the new test counts.


Completed Stage 9: implementation `d57d430f809161bb4ffddb67ae7cd1179ca0e53a`, final feature `8d74a074b428e53379334bce877bce38eea44cb9`, remote-main merge `140cc1a2ff38811fcbc02a1bda583e45f5f72462`. Required helper passed core 319 (151 optional skips), combat 198 (123), economy 337 (151), graphics 134 (0), workflow 3 (0). Clean feature worktree resumed through the helper and incorporated committed main `fe85cadcb07edcffbea365988aeacfc44f7a52c0` before Stage 10. Missions received the stable initializer and independently composed it in its owned loader.

Stage 10: [unit request contract](UNIT_REQUEST.md). Complete readonly `EnginEstSelectionne` 0x472174 and `EnginGetVolume` 0x440c5d, plus bounded `EnginAsk` 0x440d5e and original conditional production fragment 0x420f9e..0x420fb7. APIs: `unidade_selecionada(mundo,jogador,indice)`, `consultar_volume_unidade(mundo,indice,janela)`, `solicitar_voz_unidade(mundo,indice,modo,flag,*,janela=None)`, `retomar_solicitacao_saida(mundo,pedido,*,janela=None)`. Unit index u16 requires 0–799, owner/flag u8 and mode u16; camera 0–3, explicit four loaded viewport words. Distance reuses established u16/u32 arithmetic and signed-i32 comparison; volume is full EAX 0..256 and selection checks exact owner/+bd rather than list counts. No activity/type filter is added.

Hidden requests return without writes or viewport. Visible requests compute volume before mode 16 override and active-handle guard, then store +f9. Active handles return; FFFFFFFF handles raise `DependenciaVozUnidade` at the original pre-PostSound boundary, carrying exact opcode/code/flag/volume/live relative handle offset. No fake backend/post success is provided. Missing viewport stops before the volume call. Conditional production reaches `SolicitacaoSaidaTropa` at 0x420fb7 only for a foreign building owner or an actually supported request return. Pending dependencies retain prior placement/order/flag effects; earlier stages are not rerun.

Stage 10 actual checks: six original intervals and focused closed REA dossiers with distinct normalized/original identities reviewed/audited. Final 13 tests pass 5,196 original entries/5,532 bounded segments: 4,452 returns, 560 cleanup checkpoints, 176 pending-post and eight pending-volume stops. 336 preserved-state minimap resumptions in 64 joined prefixes are counted separately, not substituted calls. 184 differential Python dependency exceptions are intentional. Whole world buffers and exact native call arguments match, maximum 53,345 instructions/segment; final faults/limits/failures/errors/skips zero. Initial fixture-assumption failure (active sound handle preserved by conversion) and later monolithic prefix-cap failure remain saved; final harness reuses Stage 8's verified checkpoint mode with unchanged instructions/limits. Local seven executed / six optional skips; core 332 / 157 optional skips passes. Synthetic two-handoff demonstration performs no audio or cleanup.

Stage 10 closes readonly volume/selection and conditional recruitment request through cleanup boundary for its declared common return domain, ready for integration. Sound handle allocation/replacement/resource/backend effects at PlaySnd_PostSound/HandlSnd_Insert remain explicit. After integration, inspect missions' required EnginResetAll 0x441659 and distinct PlaceEngin 0x456fa6, reusing existing world effects without implementing its loader. Chemin_Remap and combat's level-experience/remaining death branches remain recorded. No real mission, full recruitment/audio or global completion percentage is inferred.


Completed Stage 10: implementation `b1585b4bd8a64c92aa28455fc39b13c87993a067`, final feature `68f218d4b0df8078f7e6611ad496b42c46591c7c`, remote-main merge `66e83062f1dd821b04a59b820fcc7e2712839f60`. Required helper passed core 332 (157 optional skips), combat 211 (131), economy 362 (164), graphics 155 (0), workflow 3 (0). Clean feature worktree resumed through the helper and incorporated committed main `82a0468f5482ef00357bc077a75947c01b44aec4` before Stage 11. Economy is consuming the actual request/caller through its own production composition.

Stage 11: [global unit reset contract](UNIT_RESET.md), complete original EnginResetAll 0x441659..0x441775 (284 bytes, no subcalls). Economy confirmed there is no matching generic raw Bag helper and agreed that core should own the common raw lifecycle primitive. API `bolsas_inicializacao.resetar_bolsa(memoria,offset=0,*,ordem='tabela')` accepts writable bytearray or contiguous B/b byte memoryview, validates before stores, preserves +60..+65 and uses the exact original table/unit header order, followed by 30 interleaved word/tag stores. `ciclo_unidades.resetar_todas_unidades(mundo)` and world method first reset four distinct 2704-byte owner/type pools, then scan 800 units: state 0 fully retained; all nonzero states, including 4, write life 0/state 0/AF 0 then reset local Bag in unit order. Every other field/selection/search/physical state stays intact.

World raw `bolsas_tipos_unidades` explicitly models four pointer-table pointees at 0x4e19b8; constructor bytes are synthetic, not loaded initialization. All allocations are protected before effects, while original unchecked invalid/alias pointers remain outside scope. No owner/type/capacity eligibility guard, economic balance change, allocator, navigation release or collision teardown is added. Actual mission orchestration remains with missions.

Stage 11 actual checks: full body plus four inline ranges exported and independently audited; focused REA dossier reviewed with separate hashes and closed session. Nine tests / 46 fresh original executions pass: 16 whole returns, 15 table-fragment exits, 15 unit-fragment exits. Whole 220800-byte units and 4×2704-byte type Bags match; exact 6,857 whole-driver native store events plus all 30 fragment traces match, including differing headers and interleaved word/tag writes. Final faults/limits/failures/errors/skips zero, no dependencies/callbacks. Local five executed / four optional skips; core 341 / 161 optional skips passes. Synthetic world demo preserves inherited collision/search/selection while resetting nonzero records and retaining six reserved bytes; no actual mission/runtime.

Stage 11 closes the exact preallocated unit/global-Bag reset prerequisite, independently validated and ready for integration. Next original lower provider is PlaceEngin 0x456fa6, accompanied by exact ExisteEngin 0x441fff (state!=0) and raw EnginVisible 0x4465bf (+0x72 byte) predicates requested by missions. They must remain distinct from production SetSortEngin, Mundo.viva and terrain discovery. Chemin_Remap clear-before-allocation semantics and full mission call order remain separately open; no synthetic constructor/default remap is substituted. Coordinator retains the overall estimate independently of these counts.

Completed Stage 11: implementation `2b3d502f1e0ec21127f15d8e3604f14ccf4918b7`, final feature `e8dfe61dba9994bdf25976c70cbf49012a71a963`, remote-main merge `b9b6f726895a2e0f800bb8f986f28a767104a882`. Required helper passed core 341 (161 optional skips), combat 219 (137), economy 362 (164), graphics 162 (0), workflow 3 (0). The clean feature worktree resumed through the helper and merged committed main `9e0efeaa8032cbef76f58236ebe2d34fff9501ae` before Stage 12.

Stage 12: [physical mission placement contract](MISSION_PLACEMENT.md), exact `ExisteEngin` 0x441fff, raw `EnginVisible` 0x4465bf and bounded `PlaceEngin` 0x456fa6. Public functions are `consultas_unidades.existe_unidade(mundo,indice)`, `visibilidade_unidade(mundo,indice)` and `colocacao_missao.colocar_unidade_missao(mundo,indice)`, with matching world methods. U16 index is protected to 0–799. Existence returns state != 0 including state 4; visibility returns raw +72 without state/type/owner filtering and promises consumed AL only. Both retain all unit bytes. Physical placement protects the existing type/owner/camera/map/minimap domain before effects; reads prepared current +8, calls collision, sets +72, then normal-owner discovery/light and all-owner minimap. State, step/destination/order/search/life/experience/sound are retained; collision may update existing FA backups. It does not release search or remove old occupancy.

The shared physical tail uses the established providers once, while production retains its preceding record/search prefix. Larger normal-owner vision sums above 8 raise `DependenciaColocacaoMissao` at 0x457019→0x476851, preserving collision/+72; production retains its own dependency class/checkpoint 0x446146. No callback, mission scan or loader is invented. Four intact-original exported ranges and manifest hashes were independently audited against PE offsets. A reviewed excerpt reuses the already closed REA session and keeps normalized analysis and original oracle identities separate; its incorrect inferred void signature is not used as an API.

Stage 12 actual validation: 15 tests pass 2,014 original entries / 3,938 bounded segments: 672 mission entries, 318 production entries and 1,024 readonly queries. Native returns total 2,002; 12 intentional discovery stops match Python dependency exceptions and complete partial state. The 1,924 other segments resume the same original minimap instruction with CPU/flags/stack preserved; no subcalls are substituted. Whole loaded world buffers and native effect order match, including all types/owners/edge indices, all state bytes, geometry/vision boundaries and all raw-query bytes. Maximum segment is 54,778 instructions; final native faults/limits/failures/errors/skips zero. Existing four production captures replay unchanged. Local ten executed / five optional skips; core 350 / 166 optional skips passes. Synthetic prepared state-4 demo preserves distinct orders and matching search while inserting current collision and setting +72; no actual mission/runtime claim.

Stage 12 closes the lower mission insertion and predicate request, independently validated and ready for required integration. Missions retains original scan/predicate order and coordinated load readiness. After integration Core will inspect Chemin_Remap 0x42ee1c, particularly clears before allocation, resource cleanup, obstacle input and region labeling; existing natural-region rebuilding is not silently substituted. Combat's level-experience/remaining death branches and real audio remain open. Coordinator retains global completion assessment independently of these stage counts.

Completed Stage 12: implementation `c84556f9f101b766306074fc37bd33a30d02e970`, final feature `9f1687a697f486a9d119d29fc8f3a6e448fa2192`, remote-main merge `92d8c1e93062b97f1872ce65b2dd5b8a3e98499e`. Required helper passed core 350 (166 optional skips), combat 219 (137), economy 377 (172), graphics 169 (0), workflow 3 (0). An initial remote-operation review required explicit human approval; the human approved the exact helper operation and it completed without a workaround. The clean feature tree then resumed and fast-forwarded to this committed main before Stage 13.

Stage 13: [remapping lifecycle contract](MAP_REMAP.md). API `remapeamento_mundo.iniciar_remapeamento(mundo)` / navigation-world method translates only 0x42ee1c..0x42eebd, before the first external allocation. It mutates live allocations in exact order: search occupied/success/pointer/unit, auxiliary color fill, release-status fill, free count and entries, region-word fill. Search completion, units/structures/routes, terrain attributes/tiles/objects, vision/minimap, owner Bags and selection remain unchanged. Protected data requires mutable ContextoBusca, 65,536-entry region list, exact-size bytearray color pools and distinct free/status buffers; all checks precede effects. It adds no dimension or active-unit filter and no occupant reinsertion.

The frozen `RemapeamentoPendente(flags=0,tamanho=65536,endereco_dependencia=0x42eebd,importacao=0x5231c0)` is the first GlobalAlloc request, not a successful remap result. Repeating the prefix repeats its clears. Original `CMP AX,AX` makes search reset unconditional, including FFFF unit input. Full GlobalAlloc/GlobalLock effects, temporary classification, per-component stack resources, map-edge stores, cleanup and final AL success remain the next continuation. Missions keeps orchestration and actual load readiness; the existing convenience region rebuild is not substituted for the original lifecycle.

Stage 13 evidence/checks: four audited intact-original intervals cover complete 965-byte body, 161-byte prefix, 24-byte memset wrapper and 163-byte fill leaf. Focused REA dossiers from the pinned private provider keep normalized/original identities distinct; session exported and closed. Four independent original captures preceded translation. Final seven tests pass 29 fresh original entries, all at 0x42eebd, with full loaded world buffers, exact stack arguments and 263 ordered events matching. Three native memset/fill calls execute unchanged; zero Windows imports reached/substituted. Maximum segment 88,073 instructions; final faults/limits/failures/errors/skips/dependency exceptions zero. Two observer-only failure reports are preserved (callback signature, then byte-value normalization). The source audit caught and corrected overlapping export filenames before completion. Local four executed / three optional skips; core 357 / 169 optional skips passes. Synthetic demo clears regions/colors in place and retains units/attributes/search completion, with no allocator or real mission.

Stage 13 closes the precise pre-allocation reset prerequisite and is ready for required integration. Continue next with the original first allocation/lock return and terrain classification, using explicit resource effects and raw obstacle-marker input. Normal components and their allocation/cleanup/failure behavior remain open until independently compared. No mission/runtime or global completion claim follows from these counts.

Completed Stage 13: implementation `dac71c04900fcac6f7a67bb07e24c52a30dbd69e`, final feature `6754df4052637a3c2de2a73ff9506c520b3a803a`, remote-main merge `8fcf1d35e9945d98eac07da8975ff933e4b9fe0b`. The seven-front round then resumed this worktree at main `8a499a9`, committed the untracked remap inventory [REMAP_CLASSIFICATION.md](REMAP_CLASSIFICATION.md) (then labeled Stage 15, Stage 16 after the reorder) (inventory only, `a4a67efd52faefdddd173719faf732df35a62c22`) and merged main `f18b5a0` before Stage 14 implementation.

Stage 14: [discovery domain contract](DISCOVERY_DOMAIN.md).

Published symbols:
- `insercao_unidades.SOMA_VISAO_MAXIMA_INSERCAO = 11`, re-exported unchanged by `colocacao_missao` and `colocacao_saida`. It is the inclusive normal-owner u8 +0xbb + u8 +0xf5 sum for which `PlaceEngin`/`SetSortEngin` run `DecouvreTerrain` (sum+2), `IllumineTerrain` (sum) and `SetMiniMap`.
- `visao_movimento.RAIO_DESCOBERTA_MAXIMO_VALIDADO = 23` and `RAIO_LUZ_MAXIMO_VALIDADO = 20`, the natively validated direct-call DX radii for owners 0..3, re-exported by the same three modules.
- Agreed by message: missions reads the symbol through `colocacao_missao` (9a, main `dbff65199a8e2d81620a3abec6a7e49713194ec2`); economy reads it through `insercao_unidades` (main `f18b5a00a27e716fd3662d56f9482b67b110ef16`). Economy gates its `BatimentHabitable` on the two radius symbols.
- The coordinator asked for the structure caller to be covered with separate symbols, without widening the unit symbol.

Inventory from intact bytes (`extrair_descoberta_terreno.py`; 16 hashed intervals, 9 writer sites, 52 call sites):
- BB comes only from the type table low byte (`LoadEngin` 0x46adeb, `EnginSetType` 0x457d55) or a literal 5. F5 is only ever 0 or 1.
- The shipped `RAYON` values are {5,7,8,10} and the 38 ETA maps place {5,7,8,10}, so the reachable maximum is 11.
- `BatimentHabitable` 0x41cc70 passes R+3 / R from jump table 0x41cc18 (maxima 23/20, type 0); `BatimentGetCase` preserves EDX.

Implementation: `_aplicar_insercao` compares the sum with the symbol instead of literal 8; order and partial effects are unchanged. The native bench gains a per-cell `DecouvreCase`/`IllumineCase` trace, direct entries under the exact routine and leaf intervals, and an opt-in preserved-state resume at `SetMiniMap`'s pixel-loop head 0x46a623.

Validation:
- Seven original-only captures (80 segments) preceded the change and match Python.
- The initial full native run failed because the direct-entry guard omitted `SetMiniMap`'s leaf queries; it is preserved. A 1×1 segment-budget diagnostic is also preserved.
- Final `validar_descoberta_terreno.py --emular` passes 32 tests over 10,503 segments with zero failures, errors, skips, native faults or limits.
- New entries: 1,433, with 1,423 returns and 10 declared pre-discovery stops. Maximum segment: 164,737 instructions.
- The unchanged 0–8 regressions reproduce Stage 8/12 counts: 2,014 and 846 entries.
- `conferir_monde01_descoberta.py --emular` shows missions' committed scan on actual MONDE01 placing units 0, 1, 2 and 11–15, reaching 0x46c16d and equalling their original v2 capture. A fresh native prefix equals both.
- Missions and economy suites pass natively on this branch (6/6 and 13/13). Locally: missions 56/21 skips, economy 393/180, core 368/175.

Remaining:
- sums 12..510;
- direct radii above 23/20 and owners of 4 or more;
- radius domains of the other 46 call sites (including AvanceEngin and the BatimentDecouvre/BatimentIllumine loops);
- loaded-mission readiness.

Completed Stage 14: implementation `f8d93718625eb8eaae954d4426651cac4506324d`, final feature `5ba1190ad547594458996126a6aa11b3742ed1a9`, remote-main merge `7b7b96960cee0ec7868914e811f51b851fc27dba`.
- The helper's candidate passed core 368/175 optional skips, combat 236/145, economy 413/190, graphics 184/0, missions 65/24, ai-runtime 25/1, audio 2/0 and workflow 8/0.
- Reproduced on that main: the full 32-test native suite (10,503 segments, reports byte-identical) and the MONDE01 check.
- Missions independently reproduced 6/6 natively.

The coordinator then pre-authorized a reorder:
- Stage 15: BatimentModifyMap, TerrainReset and MiniMapReset.
- Stage 16: remap allocation/classification plus the declared-binding facility, per [REMAP_CLASSIFICATION.md](REMAP_CLASSIFICATION.md).
- Stage 17: region labeling, cleanup and the final Chemin_Remap return.
- Stage 18: Engin_RetrieveExperimente, then unit state 13 and DemonteBatiment.

Stage 15: [reset and structure-minimap contract](RESET_MINIMAP.md).
- APIs: `reset_terreno.resetar_terreno(mundo, minas, aleatorio)`, `reset_terreno.resetar_minimapa(mundo)` and `minimapa_estruturas.modificar_minimapa_estrutura(mundo, indice, ativo)`, plus `MundoFisico` methods. `SetMiniMap` modes 6/7 were added to `minimapa`.
- Validation: eight original-only captures (303 segments) preceded translation and match. Native: 11 tests, 755 entries / 1,939 segments, every entry at its real return, zero failures.
- Historical interruption status: committed locally, NOT yet integrated. The Stage 14 regression rerun after the `minimapa` change was still running when the session's usage limit was reached. The recovery below completes that validation without replacing its earlier reports.

### Stage 15 recovery — 2026-10-28

The new human request superseded the old stop. Preserved implementation `a572e8c0320ff929a6c3dd2e75907bc121f7dea6` was inspected on its clean existing worktree, then current main `8810b3730a0fb788af3eac2b447dea65372f597f` was merged as `cc95c0af6bb785f8e448e59b6d5c3f82073b5e39`. The original eight captures / 303 segments and historical 755 entries / 1,939 segments are unchanged. No REA session, source regeneration or extra worker was used. The coordinator granted this stage the exclusive heavy lease through integration and committed-main reproduction; native runs and checks are serialized.

The audit independently matched eight full exported byte intervals, seven minimap jump targets and seven caller/DL instructions to the intact oracle, in `relatorios/recuperacao-stage15-source-audit.json`. A local input audit found two real protected-buffer defects: signed byte views could fail at bulk assignment after the aux writes; multidimensional views could fail after the first minimap layer had changed. The reproduction is retained in `relatorios/recuperacao-stage15-initial-buffer-audit.json`. The recovery requires one-dimensional contiguous byte views, normalizes admitted B/b access without copying/replacing caller views, and adds local/native view checks. Existing bytearray behavior, original instructions, captures and native limits remain unchanged. `--relatorio` was added to the two validators solely to retain separate fresh reports.

Actual fresh commands, each run to completion before the next heavy command:

```sh
python3 -B ferramentas/validar_reset_terreno.py --relatorio relatorios/recuperacao-stage15-reset-local.json
python3 -B ferramentas/validar_reset_terreno.py --emular --relatorio relatorios/recuperacao-stage15-reset-emulada.json
python3 -B ferramentas/validar_descoberta_terreno.py --emular --relatorio relatorios/recuperacao-stage15-descoberta-emulada.json
python3 -B scripts/check.py --domain core
```

Fresh outcomes:
- **Reset/map PASS:** 14 tests / 759 original returns (13 terrain, 12 minimap, 734 structure), 2,139 bounded segments and 1,380 preserved loop resumptions. Maximum segment 86,186 instructions. Whole mapped world buffers, mine reserves, seed/draw count, minimap fill/call order and B/b views match. Zero failures, errors, skips, native faults or limits. Report above; full log `.local/recuperacao-stage15-reset.log` (187.147 seconds).
- **Required discovery regression PASS:** 32 tests / 4,293 original entries / 10,503 bounded segments. Direct radii 0..23/0..20, insertion sums 0..11, domain stops, all mission-placement predicates and production-exit regressions pass with unchanged real subcalls and limits. Declared pre-discovery/caller stops remain explicit; zero failures, errors, skips, native faults or limits. Report above; log `.local/recuperacao-stage15-descoberta.log` (530.032 seconds).
- **Local reset PASS:** eight executed tests / six explicit optional native skips; no x86. **Core check PASS:** 382 discovered / 181 optional skips, documentation links valid; log `.local/recuperacao-stage15-core-check.log`.
- **Full flow NOT RUN:** this stage does not validate end-to-end `MissionLoad` or `MissionPlaceTerrain`, a whole post-load mission image, frames, AI/events or a playable mission. Its MONDE01 case is a standalone fixture using the actual dimensions and type-2 sanctuary record. Synthetic constructors or zero marker tables are not loaded-state evidence.

The recovered stage is ready for the required owned commit and locked integration. Consumer contracts are in [RESET_MINIMAP.md](RESET_MINIMAP.md); mines/RNG must be the same live allocations used by the later mission loaders. Full remap allocation/classification, labeling, cleanup/final return and `Engin_RetrieveExperimente` remain open. After integration, only lightweight next-stage inventory is authorized until the coordinator schedules another implementation/heavy lease. Final feature/main hashes and committed-main reproduction are reported to the coordinator without amending a commit merely to add its own future merge hash.

## Agreed ownership with ai-runtime (seven-front round, 2026-10-28)

Proposed by ai-runtime from intact bytes and confirmed by core by message:
- **ai-runtime implements** the `CalculGame` 0x42c868 frame skeleton; the `CalculEnginNextEtape` 0x456db5 loop and its counters (0x4e1a38/0x4e1a3a, the 4×26 table at 0x4e1a3c, per-owner totals 0x4e1928); the `EnginNextEtape` 0x45442c prelude order and its 25-entry state switch at 0x4543c8; the `CalculBatimentNextEtape` 0x4281c7 loop/counters (0x4dfaa8) and the `BatimentNextEtape` 0x4268d4 type switch at 0x426880; `IATestUtilite` 0x47fbfd; AI kernels, rule-VM world operations, `iagUnit`/`iagVille` messages, iab* behaviors and the `IaAlloc`/`IaReset` tables.
- **core keeps** the bodies of unit states 2, 3, 4, 16 and 17; the prelude primitives `SetDeplaceEngin` 0x4457d3, `SetDyingEngin` 0x444938, `SetEnginCollision`/`ResetEnginCollision`, `RetireEngin` 0x457058, `CalculFatigue` 0x452cc8/`EnginSetFatigue`; `DecouvreTerrain`/`IllumineTerrain`/`SetMiniMap` and `BatimentDecouvre`/`BatimentIllumine`; the type-12 gate branch body 0x427bb7; and, unchanged, `ia.atualizar_ia`, `MaquinaTarefas`, `OPERACOES`, `mensagens_chegada` and `cadencia`, which ai-runtime consumes without copying.
- **Owned elsewhere:** the prelude's sound, HP regeneration through `BonusGetValEngin` (economy query), `EnginTrouveCible`/`SetAttaqueEngin` (combat) and state-4 `CreerSac` (economy). Core bodies raise named dependencies at those call sites. ai-runtime sequences the 32-frame target scan, spell timer and fatigue branches; core supplies primitives only. The fatigue bonus read at 0x4dfba0 and the provisions/Bag consumption are economy dependencies.
- **Requested core API (not yet scheduled):** the committed `MundoNavegacao.atualizar_movimento(indice, maquina=None)` is a coordination over `girar` (RotateEngin 0x448599), `avancar_passo` (AvanceEngin prefix 0x448704) and `concluir_movimento` (state-2 tail 0x4563da), not the exact branch bodies. Proposed exact entries, each `(mundo, indice)` with a u16 index, returning None (the dispatcher ignores the value) and raising named dependencies at original call sites: `executar_estado_movimento` (state 2), `executar_estado_rotacao` (state 3), `executar_estado_retirada` (state 4) and `executar_estado_saco` (states 16/17). The coordinator schedules them; they are outside Stages 15–17.
- **Also accepted by core, not yet scheduled:** `DemonteBatiment` 0x41effd, called by `CalculBatimentNextEtape` with a u16 structure index when state byte +5 is 3. It is the physical structure removal; economy supplies refund arithmetic as a callable query. Unit state 13 (0x4558e4, entering a structure or vehicle) is the physical entry body. `BatimentGetPlayer`/`BatimentGetType`/`BatimentEnDestruction` (economy queries) and `CalculEntreBatiment`'s `iagUnitSendMessage` 0x47 (ai-runtime) remain named dependencies at their call sites.
- The declared-binding facility in `ferramentas/emulador.py` is Stage 16 after the coordinator's reorder. A binding declared at an import thunk or game wrapper stops before entry, records the exact stack/register arguments, obtains the fixture result, applies the stdcall return and resumes at the caller. A fixture that cannot honor Windows semantics raises, and the run is reported as a stop.

## Stage 16 binding requests received (inputs, not implemented)

- **ai-runtime:** a frame oracle on the declared-binding facility (shape agreed above).
- **missions:** a whole-`MissionLoad` oracle; real ETA bytes through the file wrappers and a deterministic allocation arena.
- **graphics** (Stage 16 on main `21ebbee` uses local bindings it will migrate):
  - KERNEL32 IAT slots, all stdcall with the callee popping and the result in EAX: 0x5231C0 GlobalAlloc (2 arguments), 0x5231C8 GlobalFree (1), 0x5231CC GlobalHandle (1), 0x5231D0 GlobalLock (1), 0x5231D8 GlobalUnlock (1).
  - Statically linked Watcom-register C runtime, so the game's FileOpen/FileRead/FileClose wrappers and handle global 0x4E1D1C run natively: fopen 0x48C71F (EAX name, EDX mode), fread 0x48C97B (EAX buf, EDX size, EBX n, ECX FILE*), fclose 0x48C80B (EAX FILE*).
  - Each call is logged as [name, exact arguments, return].
  - These requests become stops: non-GMEM_FIXED flags, zero sizes, exhaustion, stale handles, non-"rb" modes and short reads.
  - Graphics offers its natively validated `ciclo_cache_terreno.MemoriaMotor` model of MemAlloc 0x467EA6 / MemFree 0x467ECB as a shared provider. MemAlloc adds to counter 0x4E2F3C before GlobalAlloc; MemFree never subtracts and falls into MemClose's RET at 0x467EF3.


### Stage15 completed boundary and Stage16 continuation — 2026-10-28

The Stage15 recovery above was delivered as `2f9d0df8a9f894673a1ce5737bb2f3bbbe4644ac`, merged/pushed to main as `b610bfad77ffadaa0ee5f6af02160d786ccfdc7b`, and reproduced there: four focused tests, 16 original returns / 212 segments, eight historical captures replayed, no failures/errors/skips. Tested provider trees matched main. This closes its earlier integration-pending wording without rewriting the historical records.

Stage16 provides the opt-in [declared-boundary API](DECLARED_BINDINGS.md) in `emulador.py` / `vinculos_declarados.py` and [remap allocation/classification](REMAP_CLASSIFICATION.md) in `classificacao_remapeamento.py`. No consumer may replace unknown engine bodies with this transport. Imports must be actual PE IAT slots; original-image direct bindings are restricted to the inventoried I/O allowlist. Handlers consume explicit register/stack widths, return explicit EAX/optional GPRs, and log writes/results/stops. Native code sections are write-protected by the protocol; data/DGROUP/stack/arena writes are supported. Finite per-top-level binding budgets retain partial effects and report failure. No Windows/file/allocation/clock defaults are supplied.

`retomar_classificacao_remapeamento(world,pending,alocar=...,fixar=...)` consumes Stage13's exact pre-GlobalAlloc handoff without resetting again. It calls allocation(0,65536), then lock(handle), including handle0. A missing provider stops at its exact original call with earlier effects retained; a null lock returns False before terrain reads or cleanup. Supported live class memory receives the complete ascending attrs-bit0 pass, then the complete ascending natural-obstacle pass using explicit 702-byte markers. Returned `ClassificacaoRemapeamento` retains live memory/u32 handle at 0x42ef8b. Tiles are 65536 explicit u16 values; class/read sources are exact contiguous byte buffers, with protected overlap checks. No unit insertion, component labels, edge correction, second allocation, cleanup or final remap success is implied.

Coordinator-approved tiny readonly delegates: `consultas_unidades.tipo_unidade(world,index)` / world method reads raw +1 (u16 index0..799, consumed AL); `tipo_unidade_monstro(type)` masks to u8 and returns 20..24 inclusive. They add no activity/type filter, VM object or rule-domain behavior. EnginGetEtat/EnginSetPlayer remain dependencies.

Original-first observations were made under the exclusive lease before translation: eight remap calls /299segments (five classification checkpoints, two null returns, one declared unsupported lock) plus 768 query entries. Actual MONDE01 normalized disk layers with shipped TABLEAU.COL produce 506 temporary class-one cells, not labeled loaded regions. Fresh validation: 19tests/1073segments, zero failures/errors/skips/native faults/limits; one unsupported-lock fixture and one binding-budget failure are intentional and distinct. Focused no-binding legacy: seven tests /45 original entries /241segments, all passing. A first temporary report-export AttributeError after passing tests is preserved; the repeat succeeds. Static audit independently matches eight original intervals and actual import metadata. See the contract for all report paths and order/input limits. Original EXE SHA remains6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb; normalized-analysis SHA remains26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0. No REA/Ghidra session was used.

Core gate passes 401 discovered tests /186 explicit optional native skips, with documentation links valid. The owned commit and locked integration follow this validation; final delivery/main/reproduction hashes are reported separately, without amending solely for a future merge hash. Full MissionLoad/MissionPlaceTerrain and whole loaded mission comparison remain NOT RUN by this Core stage. Stage17 region labeling/cleanup/final Chemin_Remap return remains the next scheduled bounded slice; Engin_RetrieveExperimente follows. The coordinator owns global progress and the18:25 development/18:40absolute cutoff. Do not begin a further round without its scheduling grant.


### Stage17 complete natural remap lifecycle — preparation and original-first evidence

The original-only harness was committed asf0365f5, adopted Missions Stage11 main, and captured seven cases in immutable commit `2d541308c6652eeeb39867fd80d7252491afd465` before translation. [Whole-remap contract](REMAP_COMPLETION.md) records all byte ranges, resource ABI, image/store acceptance, file hashes and actual outcomes. The batch took148.947seconds /2,263segments: four real returns including actual MONDE01 (AL1,56components), two exact declared resource stops, and the original unchecked-null write fault at0x42efd9. All eight mapped blocks /5,246,976bytes per case, live/freed resources and temporary-memory tails are retained. No prior artifact/media or original instruction was modified.

`conclusao_remapeamento.remapear_mundo` now composes reset→classification→component LIFO labels→edge correction→class cleanup→final AL. The continuation accepts the Stage16 live class handoff or an explicit retained phase. Missing providers name the original CALL/IAT and preserve a resumable state; buffer-identity GlobalHandle queries avoid conflating locked pointers and allocation handles. Callbacks remain owner-supplied. Python replay matches every captured mapped byte and ordered stack/region/edge/resource effect; fresh native differential and required gates/publication are pending. Full MissionLoad/MissionPlaceTerrain and the loaded-mission comparison remain NOT RUN by this Core stage. Engin_RetrieveExperimente remains the next Core P2 dependency, without claiming it was implemented here.


Stage16's completed boundary is main `b4c5a1072a2b2e494b3a6bf374bd978fc6e67b9a`, implementation `9bf13ae01364b9b12c0b90b3debfabfddcc6eedd`, feature `830e6390b57e62155a1c433041e871f62f61a79a`. Normal pushes and fetched ancestry were verified. Exact-main19test/1,073segment reproduction matches the tested report; the seven-test no-binding Core regression passes. The coordinator-requested focused AI initialization module then passed11tests with19fresh original captures and19fresh translation comparisons; all48shared binding registries remained empty. Those post-main reports are preserved in `.local/stage16-repro-main.json` and `.local/stage16-ai-legacy-main.json`. This closes earlier publication-pending wording; whole MissionLoad remained untested.


Stage17 fresh native comparison now PASSES seven tests /2,267segments in157.394seconds, zero failures/errors/skips. This includes all seven complete original entries and four separate final-tail entries; complete mapped bytes, exact resource generations/call results, ordered LIFO/label/edge stores and returns equal frozen observations and Python. Two declared resource stops and one original unchecked-null write fault remain explicit; no unexpected fault or limit. The first attempt's key-format/assertion-rendering failure before full-remap execution is preserved in `relatorios/stage17-native-first-attempt.json`; only test diagnostics/key normalization changed. Native instruction limits, game code and captures were unchanged. Focused legacy regression, Core/common gates and exact-main reproduction follow this result; final hashes are reported without amending solely for a future merge hash.

Focused Stage16 regression also passes19tests /1,073segments with zero failures/errors/skips; `relatorios/stage17-classificacao-regressao.json` preserves its separate fresh result. The legacy report scope describes its own checkpoint-only tests; Stage17's separate report above establishes full remap returns.

Required Core gate PASS:408discovered /188explicit optional native skips, documentation links valid,10.350seconds; `relatorios/stage17-core-check.json`. Stage17 and focused legacy original comparisons above ran without skips. The owned commit is ready for the unchanged locked integration helper and focused committed-main reproduction.


### Stage17 delivered boundary and cutoff handover

Implementation `93620d34a7a1cf722764a690fb3b945920d9531e`, final feature `e5f0b69573688418430524171058e3df124a4904`, main merge `09d3953c6dda02ba6e4f6ca9ac61e51ca48782e6`. The unchanged helper held the common lock through fetch, semantic merge, common checks and normal feature/main pushes; all delivery/capture/feature/merge ancestry was verified on fetched main. Common suites all pass: Core408/188optional skips, combat246/149, economy424/196, graphics192/0, missions80/31, AI36/4, audio20/3 and workflow8/0. Fresh Stage17 and focused legacy native comparisons have no optional skips.

Focused reproduction on that exact main passes: all seven frozen whole-state/Python cases, four native final-tail entries, and a fresh complete original MONDE01 return AL1 with56components. All5,246,976mapped bytes, resource generations/results, ordered LIFO/label/edge writes and registers equal immutable evidence. Total735native segments (731whole MONDE01 plus four tail),342binding resumptions,388preserved loop resumptions, maximum88,074instructions; no unexpected fault or limit. Relevant Core/mission-fixture source identities match the tested implementation; captures remain unchanged. Reports/logs: `.local/stage17-main-repro.json`, `.local/stage17-main-repro.log`, `.local/stage17-integration.log`. Main reproduction was complete and the exclusive heavy lease explicitly released at approximately18:19 BRT on2026-10-28. No child remains. Full MissionLoad and a whole loaded-mission snapshot remain NOT RUN by this Core stage.

The remaining note is LIGHT handover documentation, added after that verified main boundary. The coordinator canceled queued P2 development at18:16 to preserve the remaining validation window for Economy. No P2 capture, implementation, native comparison or integration was started.

### Next window: static Engin_RetrieveExperimente lead only

Coordinator's independent intact-EXE static read:54bytes at0x441623..0x441659, SHA256 `9e9298121bdb5c12a6d8912f5430b3cdcbcb5cb7831c466a672b320f8c7d4522`. The observed shape appears to copy20u16 words in ascending order, grouped as five words per owner across four owners. Actual source40bytes are0x4e19ec..0x4e1a14 exclusive; destination40bytes are0x4e19c4..0x4e19ec exclusive. The source must be the live saved experience buffer, and destination the existing live current queue; neither zero state nor a copied/default queue is justified. The shared epilogue at0x440d59 still needs its own byte/ABI audit. This paragraph preserves the coordinator's static finding; Core has not independently executed or validated the routine.

Future bounded work starts with an independent original-only copy/guard/word-order capture and committed immutable evidence before translation, then focused fresh comparisons, required gates, locked integration and committed-main reproduction. Schedule it under a new coordinator grant. Unit-state13, DemonteBatiment, other dispatch primitives, full MissionLoad, frames and loaded gameplay remain separate gaps. Development stops at18:25 BRT;18:25–18:40 is handover only. No new development round is authorized by this note.


### Engin_RetrieveExperimente 0x441623 — original-first delivery on `feat/re-core`

This entry follows the static lead above, under a new coordinator grant. The branch first merged `origin/main` `9bf217d` normally (merge `f291638`). The [retrieval contract](EXPERIENCE_RETRIEVAL.md) holds the ABI, the API, the domain and the saved-buffer provenance.

**Static findings.** An independent byte audit confirms the coordinator's static lead: 54 bytes, SHA `9e9298…4522`.
- The routine is an unguarded ascending copy of 20 u16 words from `0x4e19ec..0x4e1a14` to `0x4e19c4..0x4e19ec`.
- It consumes no register. EBX, ECX, EDX and ESI are pushed and popped; EDI and EBP are untouched.
- The shared epilogue `0x440d59..0x440d5e` is POP ESI, EDX, ECX, EBX and then RET, with no stack arguments.
- On exit EAX=`0x28`, ZF=PF=1 and CF=AF=SF=OF=0, with DF kept. The caller ignores all of these: `PlayerRetrieve` begins with XOR EAX,EAX.

**Saved-buffer provenance.** The buffer is in `.bss`, and 23 code references cover it.
- `Engin_ResetExperience 0x441470`, called from MenuInit and MissionLoadName, fills it with (`FF`,0) pairs.
- `Engin_StoreExperimente 0x4414f8`, called from `CalculGame+0x21a` after `MissionNext`=1, stores the top five AF values per owner.
- `Engin_LoadExperimente 0x4414ad`, called from GameLoad, reads it when the save version is ≥4. `Engin_SaveExperimente` writes it out.

These producers are recorded and run natively as provenance only; they are not translated.

**Evidence and validation.**
1. Static export, bench and capture were committed in `ff92691` before translation. Capture SHA `5c734542…20d3`: 20 cases, 22 segments, including native Reset and Store chains. The image changes only in the current queue. The capture regenerated byte-identically later in the same session.
2. Implementation commit `5b82b99` adds `recuperacao_experiencia.recuperar_experiencias(atuais, guardadas)` and `recuperar_experiencia_missao(mundo, guardadas)`. Both work on the live buffers, raise `DependenciaExperienciaGuardada` at `0x441645` for a missing saved queue, and fail protected inputs before any store.
3. The CPU-free replay of all 20 frozen cases passes.
4. The fresh native differential PASSES: 10 tests, 74 Python/native comparisons, 78 segments, with zero failures, errors, skips, faults or limits, and no binding or patch.
5. Local mode runs 10 tests, 6 executed and 4 optional skips.
6. The Core gate result is recorded in `relatorios/recuperacao-experiencia-core-check.json`.

No failed attempt occurred in this slice. Logs are in `.local/xp/`.

**NOT RUN:** complete MissionLoad or six-tail composition; a real MONDE01 queue snapshot; translation of the producers; locked integration and exact-main reproduction, which the coordinator performs. Missions should call `recuperar_experiencia_missao(mundo, guardadas)` with the session's actual live saved buffer, and never with a constructed default.


### M2 frame foundations — original-first delivery on `feat/re-core`

The branch merged `origin/main` `81ebbf9` (fast-forward). The [frame-foundations contract](FRAME_FOUNDATIONS.md) holds the inventory, ownership, API and validation.

**Inventory.** `extrair_fundacoes_quadro.py` exports 29 hash-checked intervals into `evidencias/fundacoes-quadro/` (commit `a5830f6`, static only). For each it records the operand-derived reads and writes, the grids, the callees and whole-code reference lists.
- **Core-owned:** the `ProgIteration` counters, the load counter reset, `GameNextFrame`, the `Random` family, `iaRandom`, `LongRand`/CRT `rand` and the permutation draw.
- **Other owners:** `SetUpdateChamp`/`UpdateChamp`/`ScanNouvellePatate` belong to Economy, which has committed them. `NextAnim*` belongs to Graphics under the agreed contract. `CalculNextReflect` and `PlayerAttaqueReset` (a single RET) belong to ai-runtime, `SetClipping` to Graphics, and `InitGameZone` (mouse zones) to UI.

**Cross-front findings** (requested contracts, not edits):
1. The permutation cursor `0x4e1d18` is advanced by rendering (`AffBatiments`, `AffCorpsEngin`, `AffDeplaceEngin`, `AffVeget`, `DDFlipPage`) and also consumed by the world stores of `NextAnim*`. The frame oracle therefore needs AffGame's cursor consumption, which depends on the draw divisor.
2. Single-player `NextAnimTerrain`/`NextAnimVeget` visit only the viewport. The viewport size `0x508724`/`0x508726` is **0×0 in the frozen M1 state**, so the frame oracle must declare its source.
3. The load case zeroes the counters and falls through into a frame body in the same CalculGame call, provided `MenuInit` leaves state `0x12`. Missions' trace decides this.
4. `iaRandom(0)` needs a declared clock.

**Evidence and validation.** These are M1 post-load inputs, not yet frame-1 inputs.
1. The capture is committed before translation (`9a80499`): 62 cases, 195 steps, 202 segments, with the code hash unchanged and timeGetTime as the only binding.
2. Implementation commit `06ed6d9`: `fundacoes_quadro.py` plus the CPU-free M1 loader `estado_m1_quadro.py`. The loader reuses `cadencia.avancar_contadores` and `candidatos_rota.aleatorio_caminhos`.
3. The CPU-free replay of all 195 steps matches the whole state, the ordered writes and the registers.
4. The fresh native differential PASSES: 11 tests, 659 comparisons and 677 segments, with zero failures, errors, skips, faults or limits.
5. Local mode runs 11 tests: 8 executed and 3 optional skips.

Logs are in `.local/frame/`. No failed attempt occurred.

**NOT RUN:** re-validation at frame-1 inputs, which waits for Missions' capture and entry trace; any frame-oracle composition; locked integration and exact-main reproduction, which the coordinator performs.


### M2.1 frame 0/frame 1 — re-validation and reached Core callees on `feat/re-core`

The branch merged `origin/main` `ec931d2`, which includes Missions' first-frame capture and entry trace. The [frame-foundations contract](FRAME_FOUNDATIONS.md#frame-0frame-1-re-validation-and-the-reached-core-callees-m21) holds the details. All inputs are the exact frame inputs: frame 0 is the load-state CalculGame body, and frame 1 is the second pass.

**Foundations re-validated** against the Missions phase snapshots, with no CPU:
- the load counter reset;
- the `ProgIteration` prefix, which is the only DGROUP change between frames;
- `GameNextFrame` (1 per frame);
- `Random` (8 per frame, one per state-7 unit), with `iaRandom` untouched;
- the permutation draw: MenuInit plus the CD branch in frame 0, the CD branch only in frame 1, with the MCICD_Play EAX/EDX/BL matched.

The viewport size stays 0×0, so NextAnim* visit no cell. The per-frame cursor step is Core's CD-branch draw.

**Reached Core callees.** The capture was committed before translation (`2e5cc6d`): 678 isolated native calls with Missions' `Isolamento`, the translation cache flushed after each hook_add, and the path reproduction passed. `chamadas_quadro_core.py` translates them over `memoria_quadro_core.MemoriaQuadro`, whose interface matches ai-runtime's `MemoriaDeclarada`:
- GetBit and SetBit;
- CaseEstDecouverte and CaseEstIlluminee;
- BatimentCollision, BatimentGetCase, BatimentEstDecouvert and BatimentContourEstIllumine;
- SetCollision, SetEnginCollision and Chemin_ModifieZone mode 2;
- CalculFatigue, up to its threshold;
- Random and GameNextFrame over memory.

**Inputs and order.** Inputs are register values plus live memory. Chemin's pushed `sub` and CalculFatigue's `bonus(jogador, tipo, seletor)` are explicit arguments. The bonus is Economy's BonusGetValEngin and is called with AL=owner, BL=type, DL=0. Mutation order equals the original: SetEnginCollision runs SetCollision and then Chemin for each cell in footprint order, and Chemin writes the slot word before the region word. Callbacks happen only through `bonus`.

**Validation.**
1. The static manifest has 16 intervals, 4 jump tables and 4 data tables. It records that all 20 captured call sites overwrite flags before reading them.
2. The CPU-free replay of all 678 calls from exactly the original's read-before-write bytes matches every store and all seven GPRs: 15 tests, which also cover the snapshot re-validation and the static regeneration.
3. The fresh native differential, under the lease, made **1,918 comparisons with 0 mismatches and 0 stops**. These are the 678 exact calls plus perturbations of registers, types and origins, owners 0–7, a discovered cell, free region cells, counter wrap, owner bonus and seed edges. The positive visibility exits and the Chemin insert were reached.
4. Three failed validator attempts (perturbation domain or a base computation) are kept in `.local/frame/`.

**Stops.** Each raises `DependenciaRamoCore` before any store:
- CalculFatigue: the threshold branch `0x452d61` and a missing bonus provider `0x452d48`;
- Chemin_ModifieZone: modes 0 `0x43e153`, 1 `0x43e1b4`, 3 `0x43e256` and BL>3 `0x43e29c`.

**Cross-front contracts** (requests, not edits):
- **ai-runtime:** bind `provedores_core(memoria, bonus)` at the original CALLs, with keywords `caso`, `jogador`, `estrutura`, `unidade` and `valor`/`bit`. The Core providers touch these regions, which `MemoriaDeclarada` must declare:
  - `0x4e19a0` and the unit pool;
  - the structure pool `0x49a0c8`;
  - the data tables `0x495c04..0x4962d4`, `0x4962c8` and `0x4965dc`;
  - the grid pointers `0x507d78..0x507d98` and `0x507da8`, plus the region pointer `0x4e0f38` and the grids they point to;
  - `0x497164`, `0x496d40` and the bonus table `0x4dfba0`.
- **Economy:** `BonusUnidades` copies its table at construction, so Core's differential builds a fresh one from the live bytes for each query. A live-view constructor is requested. CalculMatiere can bind Core's GetBit/SetBit.
- **Missions:** TestFinDeMission can bind `celula=lambda i: caso_estrutura(m, i)['EAX']` and `iluminada=lambda c, p: caso_esta_iluminada(m, c, p)['EAX']`. CaseGetZoneInfluence and GetTopLeftCaseZoneInfluence are not reached in frame 0/1 and are not implemented. BatimentExiste stays with Missions.
- **Coordinator:** Core loads Economy's `bonus_unidades` through the private `integracao.providers._load_providers`. A public loader is requested.
- **Graphics:** in frame 1 the cursor `0x4e1d18` moves only through Core's CD draw. AffGame's own cursor draws remain the open frame-oracle input.

**NOT RUN:** CalculFatigue's threshold branch and Chemin modes 0/1/3 natively in Python; AffGame; locked integration and exact-main reproduction, which the coordinator performs.


### M2.1 round 3: SetClipping, InitGameZone, NextAnim* and the live task VM on `feat/re-core`

The branch merged `origin/main` `738cc17`. Details are in [FRAME_FOUNDATIONS](FRAME_FOUNDATIONS.md#frame-0frame-1-round-3-clipping-mouse-zones-nextanim-and-the-live-task-memory).

**Capture before translation** (`58a0440`): 61 isolated native calls at the exact frame inputs, each with its executed native blocks, and the path reproduction passed. Reached: SetClipping, InitGameZone(1, 0) from MenuInit and from CalculGame with its nested queries and zone setters, and NextAnimTerrain/NextAnimVeget in both frames. Not reached: MarcheGetPos/Taille and NextAnimVegetFullMap.

**API** (`7f2005e`), in `chamadas_quadro_core.py` and through `provedores_core`. The provider calls are:
- `SetClipping(eax, edx, ebx, ecx)`;
- `InitGameZone(eax, edx)`;
- `NextAnimTerrain(x, y)` / `NextAnimVeget(x, y)`;
- `NextAnimVegetFullMap()`.

All of these are void and return None.

**Inputs and order.** Inputs are register values plus live memory. MouseSetZone's pushed word is an argument. Mutation order equals the original:
- SetClipping stores AX, BX, DX, CX.
- InitGameZone stores zones 1–9, 0xa, 0x1a, 0x1b, 0x1c–0x1f and 0xb in that order. Each zone stores four dwords and then the maximum index.
- MouseTestZone runs last.

There are no callbacks.

**Validation.** The CPU-free replay of all 61 calls passes. The fresh native differential over both captures (739 calls) made **2,034 comparisons with 0 mismatches**.

**Stops.**
- InitGameZone modes 2/3/4/other: `0x4719be`/`0x47194f`/`0x47184d`/`0x471949`;
- NextAnimTerrain/NextAnimVeget with viewport rows: `0x477737`/`0x47731b`;
- NextAnimVegetFullMap: `0x4774fa`.

**Task VM** (`4c486ba`). `tarefas_ia.MaquinaTarefasViva(programa, memoria)` and `.sobre_memoria(programa, flat_memory)` run the unchanged VM in place over `0x512320..0x514908`. This covers the records, the free list, the context headers (s32 head, u32 count) and the active count `0x514904`. ai-runtime can replace `PonteTarefas` with it. It equals the bridge at every frame state and for all 42 posted task types, and the writes land in the caller's buffer.

**Contracts.**
- **Coordinator:** Core now uses `integracao.providers.load_economy_bonus()`.
- **Economy:** the live-table BonusUnidades constructor is not on main yet. Core still builds a fresh instance from the live bytes for each query, and will switch when it lands.
- **ai-runtime:** bind the new providers at CALLs `0x42d2a6`, `0x42d2d9`, `0x42d441` and `0x42d467`, and replace the task bridge. MenuInit's own InitGameZone call (MenuInit+0x1ce) can use the same provider.

**NOT RUN:** the NextAnim* cell loops (they need a non-empty viewport); RestoreAll and MenuInit (unassigned); locked integration.


### M2 round 4: CRT I/O boundaries, display-scenario frames, live tile grid on `feat/re-core`

The branch merged `origin/main` `81e0a26`, which includes Economy's live bonus table and Missions' display-scenario captures.

1. **CRT `fseek` 0x48cda2 and `fgets` 0x48ce96** are inventoried I/O boundaries (`f02c930`). They are in `FRONTEIRAS_IO`, and [DECLARED_BINDINGS](DECLARED_BINDINGS.md) has the exact ABI and the byte-grounded owner review:
   - They are Watcom CRT stdio routines that touch only the FILE object, the lock hooks, lseek/fgetc, the buffer and errno.
   - Every call site's FILE* comes from the inventoried `fopen`.
   - No caller reads EDX before overwriting it or branching on AL/EAX.

   Tests cover the static bodies, call-site provenance and registration (CPU-free), plus the native FileReadLine/FileSeek over declared fgets/fseek fixtures. Under the lease, 18 native and protocol tests pass, including the existing remap/CRT-wrapper suite. `ftell` 0x48cf11, used by FileSize, still needs its own review.
2. **Display-scenario frames.**
   - **Capture before translation** (`80fd5ef`): 70 isolated calls; the path reproduction passed.
   - **Translation** (`0b8f1ea`): the NextAnimTerrain/NextAnimVeget viewport loops and CRT `rand`/LongRand.
   - **Validation:** the CPU-free replay of all 70 calls passes. The native differential in the display scenario made 194 comparisons with 0 mismatches. The v1 rerun made 2,034 with 0 mismatches.
   - **Economy:** Core now uses `load_economy_bonus()` together with `BonusUnidades.da_memoria` (native) and `.vivo` (replay) (`d1a81d5`).

   Details are in [FRAME_FOUNDATIONS](FRAME_FOUNDATIONS.md#round-4-the-display-scenario-is-the-m2-reference).
3. **Live tile grid** (`c0fc446`, contract in [LIVE_TILE_GRID](LIVE_TILE_GRID.md)). `MundoFisico.vincular_tiles(buffer)` binds `[0x507d70]`'s 131,072 bytes by identity through `grade_u16.GradeU16`; after it, `mundo.tiles.buffer is buffer`. The default list world is unchanged. Identical results with a live grid and with the list:
   - structure placement;
   - region reconstruction;
   - the eight original classification captures.
   - **Economy:** pass `mundo.tiles.buffer` as `mosaicos`.
   - **Missions:** replace `vincular_lista(P(TILES), …)` with `w.vincular_tiles(mapa.vista(P(TILES), 131072))`.

**NOT RUN:** `ftell`; NextAnimVegetFullMap and InitGameZone modes 2–4 (not reached); locked integration.


### M2 round 5: ftell, frames to counter 128, unreachable modes, field-growth grids on `feat/re-core`

The branch merged `origin/main` `d94a59e`. ai-runtime reported no open Core gap: EnginOccupeCase goes through Combat's `ocupa_celula`, and its NextAnim* gap was closed by round 4.

1. **CRT `ftell` 0x48cf11** (`01216d2`). It is in `FRONTEIRAS_IO`, and [DECLARED_BINDINGS](DECLARED_BINDINGS.md) has the ABI and review: EAX FILE* → EAX s32 position or −1, every other GPR preserved. Its callers are FileSize and `__doclose`, inside the bound fclose. The original FileSize runs natively over fseek/ftell fixtures. Under the lease, 19 native and protocol tests pass.
2. **Frames up to counter 128.**
   - **Survey** (`f426e30`): no new Core routine in frame logic, and no raid by counter 128. The first new entries are Combat's EnginTrouveCibleScan (frame 17) and Economy's ScanNouvellePatate (frame 45).
   - **Capture before translation** (`ca5a7f3`): later-frame NextAnim*, InitGameZone modes 2/3/4/invalid, FullMap as a foreign entry, and the display-path queries.
   - **Translations:** InitGameZone modes 2/3/4 and the invalid modes; NextAnimVegetFullMap; TerrainEstDecouvert/Illumine, ExisteEngin, EnginGetType/Player, EnginEstArmure/Miroir/Terreur, TypeEnginSeFatigue; and the getters MissionGetNum and MenuGetNbItem.
   - **Validation:** the CPU-free replay of every case is exact. Native differentials: display 484 comparisons and v1 2,048, all with 0 mismatches.
   - Details are in [FRAME_FOUNDATIONS](FRAME_FOUNDATIONS.md#round-5-frames-up-to-cycle-counter-128-unreachable-modes-display-path-queries).
3. **Field-growth grids** (`f5c788c`, [LIVE_TILE_GRID](LIVE_TILE_GRID.md)). `MundoFisico.vincular_grades(tiles, regioes, atributos, objetos, donos_objetos)` binds every grid UpdateChamp/ScanNouvellePatate touch, by identity. It validates everything before binding, and region rebuilds and the remap reset keep the identity. Economy's actual `propagar_planta` plants into Core's live object grid.
   - **Request to Economy:** `RecursosTerreno.vivo(...)`, since the constructor copies.

**For Missions:**
- The survey and the capture name frames by the cycle counter.
- If your frame-sequence mapping uses other inputs or reaches a raid, Core will capture at those states.

**NOT RUN:**
- frames beyond counter 128, so no first raid;
- CalculFatigue's threshold branch and Chemin modes 0/1/3;
- locked integration.
