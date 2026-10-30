# Missions handoff

Owner:missions, sixth authorized project chat. Branch:`feat/re-missions`. Worktree:`/Users/marcio/git/Rising Lands/worktrees/re-missions`. Inspected/fetched main base:`1f9019d8027f59e0fa304df29961b9c13ea5f4be`. Only this module and `docs/MISSIONS.md` are owned. No additional workers were created.

Stage1 implements the indexed `LoadEngin` continuation from `0x46acca` after `SelectionInit` to original return. [Full contract](../../docs/MISSIONS.md), [original ranges](evidencias/manifesto.json), [asset inventory](evidencias/inventario.json), [independent pre-implementation captures](evidencias/captura-original.json), [fresh native report](validacao/carga-unidades-x86.json).

`continuar_carga_unidades(Leitor, writable_unit_pool220800, writable_loader_bytes4, loaded_type_table1300, *, modificador12=None)` preserves live pool views, file order, sparse/repeated u16 indices, copy140/skip512/copy132, all four inherited tail bytes until active postload and the original ordinal+bd clear. It reuses committed combat `preparar_apos_carga_missao`; it does not duplicate that helper or core readers. Return:`CargaUnidades(quantidade,indices,fim,rotina_seguinte=0x47534a)`; this describes a checkpoint, not mission readiness. Optional modifier12 uses explicit loaded economy `BonusUnidades` when supplied. No synthetic zero world/bonuses are installed by the API.

Mutation order:four bytes50→header→ID→first copy→skip→second copy→ordinal+bd zero→indexed state predicate→combat provider→next record. Missing/raising modifier leaves earlier stores/copies intact. Unsupported/truncated input handling and narrower successful-I/O scope are documented precisely in the manual. Active type≥26 is a named boundary. SelectionInit remains a core-owned prerequisite; the original native helper executes in reference runs but its effects are not translated here. Original entry asks for four selection-count u16 zeros at508728/508928/508b28/508d28; the other bytes of those lists are preserved.

Original oracle SHA256:`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`; normalized static PE:`26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0`. REA private read-only session used pinned revision`b9a8f8e9f25feb9cc97bf4960748f2bdf8c898bc`, exported and closed; Ghidra summaries/signatures did not override assembly. Original `MissionLoad`, `MissionLoadName`, inline structure copy, auxiliary calls and postload caller inventory were inspected before implementation.

Actual validation:two original-only captures/88 bounded segments preceded implementation. Fresh differential:12 tests,469 native fixtures/14,056 segments;457 returns,12 expected modifier-entry checkpoints;zero skips/faults/failures/errors. All38 original ETA unit blocks included; inherited pools and loaded bonus patterns explicitly synthetic. Local mission run:12 discovered,eight executed,four optional skips. Common local checks at base:core290/138 skips,combat172/107,economy303/136,graphics115/0,workflow3/0. Sandbox capture SIGILL and REA Java EPERM were resolved by permitted ordinary execution; no OS protections or shared toolchain changed.

App consumer:do not expose this as a prepared `MundoNavegacao`. It supplies only the unit-load continuation into an inherited pool, with explicit selection prerequisite. No structure/terrain/region/discovery initialization, mission dispatcher, objective/event rules, victory condition, cadence or audio is established. All38 maps passing this unit slice does not prove38 running missions. The precise next investigation is terrain/header/resource/view preparation before `Chemin_Remap`, after Stage1 integrates.

Integration:the four-domain workstream helper cannot start/integrate missions. Stage1 must be reviewed/committed only in owned paths and pushed to`feat/re-missions`; coordinator must perform the isolated merge candidate under the same common `.git/rising-integration.lock`, holding it throughout fetch/ownership review/merge/common+mission checks/non-force main push. Failed candidates are preserved. No later implementation begins before this stage is integrated, and its result must be reproduced on integrated main. Final feature/main SHAs are reported in coordination messages, without editing a completed commit to embed its own future SHA.

Final review corrected an owned bootstrap module-name collision with core `caminhos.py` before integration; `ambiente_missoes.py` and a real `MundoNavegacao` import regression preserve consumer composition. No loader behavior or native fixture count changed.

Stage 1 integrated:implementation+fix `9f0d32481560e49a21258a269cd22b44a1827263`, final feature `551e1fb19e8bf529d0074a960d6507a87e2ee248`, main merge `c64d32b859046468e2f9085f90f96eb5002d567c`. Coordinator's locked candidate passed fresh mission12/zero skips and common core302/143 optional,combat185/115,economy326/146,graphics115/0,workflow3/0. Worker fetched clean main `8fd9c41ce6e3b8709cc0d7235e8c31d9b6a68b8d`, verified ancestry and reproduced mission12/469 fixtures/14,056 segments before Stage 2 implementation.

Stage 2 implements `continuar_cabecalho(Leitor_at_0,attrs65536,terrainLE131072,objects65536,aux65536,Economia128,dimensions4,view4,selected_player_u8)` after successful file open. Exact original interval `0x46c396..0x46c512`; checkpoint `0x42ee1c` before every remap effect. Shape/provider failures precede reads; strict read/provider failures preserve prior complete stores. Order:skip4→copy four layers→committed graphics normalization54→66/aux1 across65,536 cells→12 committed economy setters in resources1,2,0/player0..3 read order→width/height words→consume all four view pairs, store matching selected-player only. Selected values4..255 preserve inherited view. Raw dimensions remain raw; no playable-world claim. Full [Stage 2 contract](../../docs/MISSIONS.md#stage-2-successful-open-terrain-resource-and-view-prelude), [new instruction/provider manifest](evidencias/cabecalho-manifesto.json), [pre-translation original captures](evidencias/captura-cabecalho-original.json).

No other owner's implementation is duplicated. Prior reset/open/selection effects remain prerequisites, not fabricated defaults. Region/color/search/allocator effects and natural remap remain core dependencies. The original remap mutates several buffers before possible allocation failure; existing region reconstruction is not silently used as a full original loader. App must still treat this as explicit raw preparation, not a loaded mission. Stage 1 and Stage 2 are separate continuations with missing operations between them.

Four original-only prelude calls/160 segments preceded translation. The first combined native attempt completed all228 original-map/camera fixtures but then hit a host adapter TypeError on a synthetic bytearray; its failure is retained in ignored `.local/stage2-initial-adapter-failure.json`, not reported as a pass. The adapter now supplies bytes to Unicorn; no reconstructed behavior was changed. Stage 2 suite/report preserves Stage 1 evidence and reports its repeated unit-fixture counts separately. Next implementation begins only after Stage 2 is integrated/reproduced; planned original-only investigation is auxiliary-table initialization and exact FinMission/Objectif load/retention boundaries, not inferred victory rules.

Final Stage 2 validation:18 tests pass --emular,zero skips/errors/failures/native faults;237 new prelude calls/9,480 segments all stop before remap. Repeated Stage 1 coverage remains separately469 fixtures/14,056 segments,457 returns+12 expected modifier checkpoints. Local18 discovered/12 executed/six optional skips. Common local checks at8fd9c41:core302/143 optional,combat191/119,economy326/146,graphics122/0,workflow3/0. The reporter writes new validacao/stage2-suite-x86.json and leaves Stage 1 report unchanged.

Stage 2 integrated:implementation `5361b496e61265275cc129de8efc018d267d266f`, final feature `0c7d825fe008b2c8ecc24a9e54bd0af8efb546d0`, main `b8f424dde0bc12d829b8653bdd9deb4906093397`. Worker fetched/verified clean committed main `6a9168e42f917096af88fc6c510b3f25b7230516` and reproduced all18 native tests and exact unit/prelude counts before new implementation. Coordinator independently reran18 tests with zero skips/errors/failures under the shared lock and completed non-force main push/ancestry verification.

Stage 3 adds exact `LoadFinMission0x458b05` and `LoadObjectif0x47c404` APIs in `carregador_condicoes.py`. `carregar_condicoes_fim(Leitor, writable114)` marks only each10-byte record's code255 before header, copies count0..10/size10 sequentially, then clears only the copied statuses at+104; preserves four adjacent result bytes and unloaded record/status bytes. `carregar_objetivos(Leitor, writable804)` fills800 ID bytesffff, then reads400(word,flag) pairs in player/ordinal order, stores each word before discarding its flag, and preserves the four following cursor bytes. Both retain preceding effects on strict-reader failure. Shape checks precede effects; protected invalid header fails after initial marking/header consumption. Return metadata names the next original routine, never executes it.

Original-only four captures/1,618 segments precede translation; actual MONDE01, zero-record conditions and nonempty synthetic objectives use explicit inherited patterns. Complete original loader bytes and unsupported consumer/query bodies are newly exported; prior evidence is unchanged. Eight new table tests pass with native execution. The combined owned entrypoint additionally repeats the two integrated prior slices; no historical totals are added as fresh coverage. All38 original objective lists containffff, while the separate FinMission block has other raw codes. This does not establish an empty objective system or any victory rule.

Remaining condition execution is explicit:TestFinDeMission458606 has11 resolved native queries and is called by CalculGame42c868. Its Watcom decompiler artifacts were reviewed in a private pinned REA session, exported and closed; original assembly/captures remain the authority. No callback, unknown event, evaluator, cursor/text loader or mission dispatch is treated as a successful no-op. Core SelectionInit now exists at committed main140cc1a2ff38811fcbc02a1bda583e45f5f72462 and can be composed in the next bounded stage after this stage integrates/reproduces; no constructor defaults are consumed as original state.

Final Stage 3 checks:26 native-mode tests pass,zero skips/errors/failures/native faults. New112 table calls (71 FinMission,41 Objectif) all return through33,599 bounded segments. Separate repeats remain469 unit fixtures/14,056 segments and237 prelude checkpoints/9,480 segments. Local26 discovered/17 executed/nine optional skips. Common checks:core314/149 optional,combat198/123,economy337/151,graphics134/0,workflow3/0. Full owned report is validacao/stage3-suite-x86.json; Stage 1/2 reports unchanged.

Stage 3 integrated:implementation `582de22e88ec019ba3c696a804886e78a0ec11cd`, final feature `fa317bf002fd8eb6809667fbb01b7817648ce999`, main `d079aa902a3e094385db2fe69c60f91e3f86f673`. Worker fetched that clean main, verified ancestry and reproduced the changed eight native table tests/112 complete calls/33,599 segments plus the complete local26 tests/nine optional skips before Stage 4 implementation. Coordinator independently passed full native26 and common checks under the shared integration lock.

Stage 4 public `carregar_unidades_missao(Leitor,units220800,loader_bytes4,loaded_types1300,explicit_selections_bytearray2048,*,modificador12=None)` composes the actual committed core SelectionInit at its original call position before the existing continuation. Core writes four count words at selection offsets0/512/1024/1536; every other selection byte and unit flag is preserved until the loader's own ordinal writes. Selection guard errors precede effects; a later continuation validation/read/modifier failure retains completed selection effects. No copied core logic, zero-default list or callback no-op is used. [Call/provider manifest](evidencias/selecao-carga-manifesto.json), [original-only complete-entry captures](evidencias/captura-selecao-carga-original.json).

Four original-only fixtures/100 segments precede the wrapper:three returns and one expected modifier stop, with actual MONDE01 plus sparse/empty inputs. All five new composition tests pass, comparing full2,048-byte selections and220,800-byte unit pools. The continuation API remains unchanged and explicitly requires already-initialized selection; the new entry covers only full LoadEngin, not MissionLoad or world/mission readiness. Remap, original global/pool startup, structure copy/insertion, unit placement, auxiliary AI data, initializer tails, objective/event execution and dispatch remain named gaps.

Final Stage 4 native suite:31 tests pass,zero skips/errors/failures/native faults. New41 complete-entry fixtures/10,600 segments yield40 returns+one expected modifier-entry stop. Prior continuation469/14,056,prelude237/9,480,and table112/33,599 counts are separately repeated, not added as mission coverage. Local31 discovered/20 executed/11 optional skips. Common checks:core319/151 optional,combat205/127,economy349/157,graphics141/0,workflow3/0. New report validacao/stage4-suite-x86.json leaves all predecessor reports intact. Next independent slice after integration/reproduction is the original inline structure copy after remap, with72 inherited bytes retained; no core lifecycle body will be duplicated.

Stage 4 integrated:implementation `892244a19ed7b426059679736cc6afaf2812e75c`, final feature `74834368edf19bb26e2413053cb653eef075f3be`, main `37629edc282367702811f9b7060d2026b6ba9b47`. Worker verified the clean fetched main and reproduced five native composition tests/41 fixtures/10,600 segments, plus complete local31/11 optional skips before Stage 5. Coordinator independently passed fresh full native31 and common suites under the shared lock.

Stage 5 `carregar_estruturas_missao(Leitor,writable_pool276000)` covers inline MissionLoad46c517..46c578 and MissionLoadName46c8e0..46c941, stopping before unit loading. Read u16 count/size204, then each u16 ID0..999 and204-byte payload into indexed276-byte slot; preserve72-byte tails, unloaded records and sparse/repeated order. Count is not limited to slot capacity:1,001 repeated records are supported and natively compared. Return count/encountered IDs/end cursor/next46acbf, not world readiness. Buffer guard precedes effects; bad size fails after header, invalid ID after its read, truncation after earlier complete copies. No reset, allocation, owner/state fixup, region or placement operation is silently applied.

All38 original maps contain1,111 structures with204-byte records and IDs0..631. Four original-only fixtures/22 segments preceded translation and cover both caller paths, sparse duplicates and empty input with explicit inherited0xa5 memory/synthetic caller stack scratch. Complete pool snapshots/hashes govern regressions; committed core and graphics raw readers remain intact. All six focused structure tests pass, including both native paths across the entire corpus. Original-byte exporter/manifest are owned and preserve prior evidence. Remaining core startup/remap/placement, auxiliary tables, initialization tails, mission selection, condition/event execution and runtime are named boundaries. Next implementation waits for integration/reproduction; read-only mission filename branch inventory can proceed independently.

Final Stage 5 suite:37 tests pass --emular,zero skips/errors/failures/native faults. New82 structure-copy checkpoints (41 per caller)/8,706 segments compare all276,000 bytes. Earlier unit/prelude/table/full-entry counts are separately repeated in validacao/stage5-suite-x86.json, not added as mission coverage. Local37 discovered/24 executed/13 optional skips. Common checks:core319/151 optional,combat211/131,economy349/157,graphics148/0,workflow3/0.

Stage 5 integrated:implementation `694051af7f4b29e607f7a75c0ca554bc6a2e4c44`, final feature `653d38a15869ed6d6fc478a365f6cc56ba9a2c30`, main `82a0468f5482ef00357bc077a75947c01b44aec4`. Worker verified that clean committed main and reproduced six changed native tests/82 checkpoints/8,706 segments plus all local37/13 optional skips before Stage 6. Coordinator independently passed full native37/common suites under the shared integration lock.

Stage 6 `nome_arquivo_missao(number,destination>=20bytes,*,variante_u8=None,simpatia=None)` covers complete MakeMissionName46c1b8..46c2cf, preserving original filename case/backslashes/lowercase suffixes. Number truncates to u8, prefix/digits precede dependencies. Number9 requires explicit raw4e1d85 byte protected0..3; numbers10/12/17 require actual read-only query(1,0),(2,0),(3,0), consumed signed low8 with initial90/choice1 and strict replacement/tie retention. Committed Mercado.simpatia is reused; its copied player inputs do not auto-follow a separate later-mutated buffer. No default variant/sympathy is supplied. Missing/raising query retains numeric prefix and terminator; extension/suffix are appended only after queries complete. Return bytes is not a file-open/progression/title/runtime result.

Eight original-only captures preceded implementation:seven returns and one query checkpoint, eight segments, explicit inherited64-byte destination/80-byte loaded player fixture. Complete original filename/query code and string/pointer table are newly exported. Seven focused tests pass with native comparison, including all raw number bytes/upper-register poison, signed-low-byte boundaries, threshold/ties, explicit variants and failures at each query. Unknown campaign/initializer state remains a dependency rather than a successful no-op.

Next world-orchestration inventory:MissionPlaceTerrain requires ExisteEngin(state+2!=0,including4), EnginVisible(raw+72) and distinct PlaceEngin456fa6, followed by four capacity refreshes and structure work. Exact lower getters/placement/startup/remap contracts are requested from core; no generic alive predicate, copied lower routine or synthetic constructor state will stand in for them. Independent supported loaders may continue while those providers are unavailable, after Stage 6 integration/reproduction.

Final Stage 6 validation:44 tests pass --emular,zero skips/errors/failures/native faults. New3,268 filename calls/segments produce3,265 returns+three expected query checkpoints; original number width, raw variants, signed-word/low-byte differences, initial90 threshold/ties and query order match. Earlier counts remain separate repeats in validacao/stage6-suite-x86.json; predecessors unchanged. Local44 discovered/28 executed/16 optional skips. Common checks:core332/157 optional,combat211/131,economy362/164,graphics155/0,workflow3/0.

Stage 6 integrated:implementation `7c4c4e12d36e5c2a47ae1b2503c7bdadcc94521f`, final feature `61c9d9402a7724b77baca0ca33db4a545fcef2ab`, main `eb0ecb3622142812392a6d0c73dce7002040717f`. Worker fetched clean main `189c94eac6700c5d0fb24dc547d5da015734b06d`, verified ancestry and reproduced seven filename-native tests/3,268 calls plus complete local44/16 optional skips before Stage 7. Coordinator independently passed fresh full native44/common checks under the shared lock. Exact placement was not yet available, so the original immediate post-unit auxiliary prefix was selected independently.

Stage 7 original LoadMine47534a→IALoadAttaqueIni47c24d prefix is implemented for both MissionLoad and MissionLoadName, stopping before Ghost47bcc7. `carregar_minas_e_ataques(Leitor,writable_mines80,writable_attacks1004)` composes those exact readers. Mine u16 N0..20 then N×4 records; only afterward clear trailing origin words, retaining reserve words. Actual `RecursosTerreno.minas` can be supplied in place; extraction behavior remains economic-owned. Attack allocation is100×10+u32counter:counter0, reset exact bytes+0..8, preserve+9, then read count0..100/size8 and copy each payload into its10-byte slot. No shared AI semantics, economic credit/extraction or unknown next operation is executed.

Four original-only prefixes/140 segments precede translation, with actual MONDE01 in both callers and synthetic empty/maximal tables/inherited patterns. Six focused tests pass, including original whole-buffer comparisons over all38 maps and every supported count in both caller prefixes. Reader/format failures retain previous complete effects, including earlier mine loading before attack validation. Shape/header guard positions and fixed widths are in the manual. Owned source exporter appends evidence without modifying predecessor files.

Observed integration boundary:the initial actual-economic-object test failed because economy and graphics both expose flat `construcoes` modules. No provider source or sys.modules binding was changed. That genuine provider-object regression now runs in an isolated ordinary Python test process with normal economic imports; production APIs accept the actual raw buffer. General simultaneous consumer namespace coexistence remains coordinator-maintenance work and was reported immediately. This is a test isolation boundary, not an extra agent or a complete consumer claim.

Core EnginResetAll is integrated at main b9b6f726895a2e0f800bb8f986f28a767104a882 with explicit inherited four2704-byte Bag pools; constructor zeros remain synthetic. Exact PlaceEngin/ExisteEngin/EnginVisible are following it. After this stage integrates/reproduces, prioritize their real MissionPlaceTerrain call order as committed providers arrive; otherwise supported raw auxiliary/initializer slices can continue without waiting or duplicating lower primitives.

Final Stage 7:50 native-mode tests pass,zero skips/errors/failures/native faults. New320 pre-Ghost checkpoints (160 per caller)/14,270 segments compare whole80/1,004-byte arrays, every supported count and all38 maps. Prior counts are separately repeated in validacao/stage7-suite-x86.json; no complete mission/runtime claim follows. Local50 discovered/32 executed/18 optional skips. Common checks:core332/157 optional,combat219/137,economy362/164,graphics162/0,workflow3/0.

Stage 7 integrated:implementation `aa89188b48d2f98c9a1cfe0c3d7cc33e7cb35ab8`, final feature `b7f49785fdcc2a72fd5e11b308b7aa79689ae016`, main `9e60bcea5ce57d986a617c13c274c75da18c6c08`. Worker verified fetched clean ancestry and reproduced the six changed native tests/320 checkpoints/14,270 segments plus local50/18 optional skips before Stage 8.

Stage 8 is the final current slice under the human cutoff. Inspected main `6b15be1c96348d51dac7a46208126e6974290eca` includes core placement main `92d8c1e93062b97f1872ce65b2dd5b8a3e98499e` and coordinator adapter main `167615ecf5ef972dcc808156d11c71a3e3814165`. `preparar_unidades_no_terreno(ProvedoresTerrenoUnidades)` covers MissionPlaceTerrain46c122..46c16d only:ascending800-slot existence lowAL, then visibility lowAL, then actual placement when both nonzero; capacity calls owner0..3 after the complete scan. Return lists completed placements and names the pre-structure checkpoint. Missing reached callbacks raise named original dependencies; prior effects remain.

`provedores_terreno_core(explicit_world,*,bonus_unidades=None)` composes actual committed core existence/visibility/mission placement/capacity helpers and actual economy capacity/query providers. State4 is existent although excluded by generic alive/capacity predicates; raw+72 visibility is not normalized before the lowAL test. No constructor world, zero bonus, lower-body copy, reset/remap or successful no-op is installed. Missing bonus stops at the first actual428cc0 selector1 query after earlier physical effects. The core placement supported domain remains authoritative; no owner/type/camera/map/minimap/vision restriction is widened by this caller.

Four original full-prefix observations were captured before production orchestration. V1's input parent-call trace accidentally retained a live list and later serialized output calls; buffer hashes and all output dictionaries were unaffected. V1 remains intact. The frozen-trace original-only v2 exporter asserts those old outputs unchanged. Two synthetic query/vision boundary captures and matching caller-aligned supplements distinguish callee-entry attempted discovery logging from core's pre-CALL457019 boundary. No evidence is edited to fit Python.

Actual MONDE01 reaches the existing radius10 limit at unit15. Seven earlier placements complete; collision/+72 stores for15 precede the named discovery dependency476851/checkpoint457019. A supplementary original capture validates that exact partial state over all buffers/traces. The full original-prefix observation is retained, but the Python test deliberately stops at the provider boundary. All regions/colors/search and surrounding physical initialization in these fixtures are explicitly synthetic; only the mission's raw layers/unit stream and their documented preprocessing are real inputs. No complete startup, intervening auxiliary effects or running mission is established. Entry replay can repeat earlier vision counts; it is not continuation.

Owned namespace adoption closes the earlier isolated-test limitation for the specific providers:Stage5 uses `load_graphics_structures`, and Stage7 uses actual `load_economy_resources().RecursosTerreno` in the same process with the graphics reader. Bootstrap adds repository root before legacy graphics imports. The coordinator adapter preserves economy's flat `construcoes`, uses a distinct graphics identity and rejects polluted bindings without source/path/sys.modules rewrites. No sibling file or shared adapter is edited. Previous stage manifests remain historical evidence.

The final focused suite covers three declared physical fixtures, actual MONDE01 partial placement,96 combinations of indices0/799 ×states0/4/7/14 ×owners0/3/4/200 ×flags0/1/255, and two deliberate dependencies. The first native matrix attempt hit Unicorn's bytearray host-interface TypeError before executing that case; the adapter now supplies bytes to the existing native file loader. Failed and final logs are retained under ignored `.local`. Production effects were not changed to resolve this host error.

Human cutoff:finish only this existing Stage8, validate/commit/push it, request the coordinator's locked tested integration, verify the resulting remote ancestry, then STOP. No next research, speculative implementation, app rebuild or autonomous follow-up. Natural remap remains stopped at its allocator dependency despite core's separate pre-allocation reset provider; structures and later startup/condition/event/runtime gaps remain. Integration hashes belong in the final coordination/chat report, without amending a completed commit to embed its own future hash.

Final Stage 8 validation:56 native-mode tests pass,zero skips/errors/failures/native faults. New102 placement prefixes produce99 pre-structure checkpoints plus three expected dependencies in139 prefix segments/37 preserved-state minimap resumptions. Their102 preparatory unit-loader entries use876 segments, separate from prefix execution. Previous slice counts remain separate repeats in validacao/stage8-suite-x86.json; predecessor reports unchanged. Local56 discovered/35 executed/21 optional skips. Common checks at inspected6b15be1:core350/166 optional,combat227/143,economy377/172,graphics169/0,workflow6/0. Documentation links/diff whitespace pass. No real mission runtime was tested.

Stage 9a (seven-front round, base main `8a499a91`) changes no reconstructed behavior. Core proposed the discovery-domain symbol and missions agreed it by message: `getattr(colocacao_missao,'SOMA_VISAO_MAXIMA_INSERCAO',8)`. It is the inclusive maximum normal-owner vision sum u8+0xbb + u8+0xf5 completing DecouvreTerrain 0x476851; an absent symbol means the committed limit 8, and 510 means no reachable discovery stop.
- MONDE01: the test asserts unit 15's sum is 10 from the loaded pool. While 10 exceeds the maximum, it expects the unit-15 dependency against the boundary capture. Otherwise it compares the complete scan against the original v2 full-prefix capture through 0x46c16d, every buffer and trace included, and the native differential runs the unstopped prefix.
- Forced stop: the differential uses maximum+1 on the ordinary unit 7, through the type word up to 255, or type word 255 plus a post-load +0xf5 write applied to both sides. At 510 it compares the native vision9 continuation instead.
- Static caller-aligned vision9: inside the domain it compares the new original-only `captura-terreno-unidades-visao9-continuacao.json` (same fixture, native discovery/light/minimap unpatched to 0x46c16d, one load, one prefix, 39 segments, 30 minimap resumes). Predecessor evidence is unchanged.

Validation: the six placement tests pass natively at limit 8. A scratch-only simulated core limit of 9, 10, 300 or 510 (in-process patch, no core file edited) also passed all six natively; that is branch coverage of these tests, not provider validation.

Stage 9 (base main `f18b5a00a27e716fd3662d56f9482b67b110ef16`) completes L7. `carregar_cadeia_auxiliar(Leitor, BuffersCadeiaAuxiliar, *, tipos_grupo8, perfil)` follows the original order confirmed in both callers' bytes: LoadMine → IALoadAttaqueIni → LoadBatimentGhost 47bcc7 → LoadCadreInfluence 47c04a → LoadFinMission → LoadCalculMissionDivers 47c30f → LoadObjectif → LoadEntrerMonstre 47ac30. It stops before FileClose 45844c, which is next. Stage 3 and Stage 7 readers are composed unchanged.

Inputs and widths: writable views of mines 509954/80, attacks 50d5b4/1004, ghosts 50b18c/5254, influence 50c614/4000, end conditions 4e1d20/114, objectives 511ffc/804, monsters 50a9bc/1220, groups 50af84/432, the live Random state 497164/4, and the explicit group type table 498400/8 (original image `0001081415161718`, single direct reader 47a7c9).
- Every shape guard precedes the first effect. Later failures keep all earlier effects, including Random advances.
- Unsupported domains raise `ForaDoDominioAuxiliar(endereco)` before the first out-of-table write or unsupported CRT form: ghost flag 750 at 47bce1, influence beyond 4000 bytes at 47c0b1, monster record beyond 100×12 at 47ac9b, `%i` octal/hex/overflow at 48c41c, group index outside 0..7 at 47a7c9.
- `perfil=None` raises `DependenciaEntradaMonstros(0x47a665)` after the record initialization.

`LoadEntrerMonstre` calls `InitEntrerMonstre 47a601`, which runs, in order:
1. A 100-record fill. Each record makes one Random 4704dc call through core's `candidatos_rota.aleatorio_caminhos`, never a copy.
2. The HumanOnly zero store.
3. Four `GetPrivateProfileIntA` calls (HumanOnly 0, ProbaCaveJoueur 5, ProbaCaveIA 2, ProbaEmbuscade 2).
4. memset of the 432 group bytes.
5. 16 `GetPrivateProfileStringA` GROUPE%02i calls with comma/`%i` parsing and counter increments.

The loader then reads the count and size, and for each record: ×30 on +4, +8=0, a cyclic next-mask-bit search for +6, and finally the backward word0-only compaction. Details are in docs/MISSIONS.md.

`PerfilPrivado({b'./monstre.ini': bytes|None})` is the declared KERNEL32 binding: strict INI subset, an undeclared file raises `DependenciaPerfil`, and a declared-absent file returns the Windows defaults. No runtime meaning of ghosts, influence frames, divers bytes or monster entries is claimed.

Bench `bancada_cadeia_auxiliar.py` runs every engine body unpatched (loaders, InitEntrerMonstre, Random, complete Watcom memset/sprintf/sscanf/__prtf/__scnf bounds from SBL). Only the read wrapper 458461 and the five profile CALL sites (IAT 5231ac/5231b0, stdcall pop) are bound. This stays a mission-local binding until core publishes its generic facility. Comparisons cover the entire DGROUP+.bss image 494000..523000, the read sequence and the profile-call log; predicate stops compare native state at each unsupported boundary. Original-only captures came before translation: 38 maps × 2 callers with the shipped MONSTRE.INI, plus 10 synthetic × 2, giving 96 returns, 167,950 segments, 165,934 read and 1,920 profile bindings.

Agreed contracts:
- **AI/runtime** (message of 2026-10-28). Missions keeps the MissionLoad/MissionLoadName composition and calls ai-runtime's `reiniciar_ia` (IaReset 47f36e) as a provider at 46c5cc/46c98e. The AL load is not passed; IaReset ignores it. Missions also keeps EvenementInit/EnCours/Affiche/End, TestFinDeMission 458606 and the MissionGetNum/attack-table inputs.
  - ai-runtime provides IaAlloc 47fb15 (program-start state that the oracle inherits as declared input), IaReset with its tail through InitMissionMonstre 47af90 (which consumes this stage's monster tables), and the CalculGame in-game path: the state 0/15 load entry calling `carregar_missao`, state 0x12 and the network gate. Menus are second wave.
  - The M1 snapshot point is MissionLoad's return to 42d22d. Neither reset prefix contains an AI message table; L2's "message" call is UI MessageBoxInit 469908.
- **Core** (Stage 14, not yet integrated): `SOMA_VISAO_MAXIMA_INSERCAO=11` for units, plus `RAIO_DESCOBERTA_MAXIMO_VALIDADO=23` and `RAIO_LUZ_MAXIMO_VALIDADO=20` for BatimentHabitable 41cc70 structure discovery/light. MONDE01's type-2 structure uses 13/10. For Stage 11 these are consumed through `colocacao_missao`.
- **Economy finding, relayed by the coordinator, recorded as a hypothesis:** MONDE01's only structure is type 2 SANCTUAIRE, the cave is type 3, and MONDE01 loads with no cave. Whether the objective requires building one must come from the objective/end-condition trace.
- **macOS:** the requested `carregar_missao` M1 snapshot field list has not been received. It is a planned contract to record when sent.

Reset-prefix inventory for Stage 10, read from the original bytes:
- **MissionLoad 46c2cf..46c396:** MakeMissionName 46c1b8 → words 4e1a38/4e1a3a=ffff → IconeReset 45e88f → TerrainReset 46b315 → MiniMapReset 469f00 → BatimentResetAll 41a75c → EnginResetAll 441659 → ProjectileReset 46e00a → MessageBoxInit 469908 → BallonInit 441b6c → FileOpen 458420.
- **MissionLoadName 46c5e3:** the same reset calls through MessageBoxInit, without the filename and BallonInit.
- **Tails:** MissionLoad 441459, 419112, 441623, 46df41, 47f36e, 46027c. MissionLoadName 441459, 419112, 47150f, 47f36e, 46027c.

Final Stage 9 validation: 65 native-mode tests pass, with zero skips, errors, failures or faults. Fresh chain coverage is 270 caller entries resolving to 227 returns, 18 declared boundary stops and 25 strict-input failure stops, over 324,811 segments with 318,287 read and 4,744 profile bindings. Every comparison is whole-image equality over DGROUP+.bss plus the read sequence and the profile log. The new report is validacao/stage9-suite-x86.json; predecessor reports are unchanged. Local runs execute 65 tests with 24 optional skips. Common checks at f18b5a0 pass: core 357/169, combat 227/143, economy 393/180, graphics 176/0, missions 65/24, ai-runtime 3/0, workflow 8/0. No real mission runtime was tested.

Stage 10 (authorized by the coordinator, base main `7b7b96960cee0ec7868914e811f51b851fc27dba`, which includes core Stage 14 and combat ProjectileReset main `9e579b4`) composes both reset prefixes up to FileOpen. Module `reinicio_missao.py`:
- `resetar_para_missao(MemoriaReinicio, diretorio_0x509594, ProvedoresReinicio, *, variante_u8, simpatia)` returns `PedidoAbertura(caminho, b'rb', nome, 0x458420)`.
- `resetar_para_missao_nome(memoria, MemoriaReinicioNome, nome, {0x509494, 0x509594}, provedores)`.
- Continuations `continuar_reinicio_missao` / `continuar_reinicio_missao_nome` from `0x46c369` / `0x46c619`.
- Missions-owned leaves, assigned by the coordinator: `resetar_icones` (IconeReset 45e88f), `inicializar_caixas_mensagem` (MessageBoxInit 469908) and `inicializar_baloes` (BallonInit 441b6c), plus the u16 ffff words 4e1a38/4e1a3a. Exact orders are in docs/MISSIONS.md Stage 10.
- Committed providers are called at their CALLs: core `resetar_todas_estruturas` and `resetar_todas_unidades`, combat `resetar_projeteis`, and, for MissionLoadName, economy `Aprendizagem.zerar_tecnologia`.
- Named `DependenciaReinicio` stops at their CALL sites, with earlier effects kept:
  - TerrainReset 46b315 (46c35f / 46c60f) and MiniMapReset 469f00 (46c364 / 46c614), from core's next stage;
  - RechercheReset 470b46 (46c68c), RechercheCheat 4716fe (46c6a6) and RechercheStore 4714f0 (46c6ab), requested from economy;
  - Engin_ResetExperience 441470 (46c691), requested from core.
- ReseauActif 42c3b0 = AL=[0x4e0730], taken as an explicit inherited byte; ai-runtime was told.
- Domain limits:
  - MissionLoad: a path ≥ 0x100 raises `ForaDoDominioReinicio` at 46c333.
  - MissionLoadName: a name shorter than 4 bytes raises at 46c6c5; a path ≥ 0x114 raises at 46c742.

Boundaries agreed or recorded:
- Economy's balloon table `PropriedadeConstrucoes.baloes` (0x4e1a14) gets only the store-only BallonInit reset, by identity. The habitation tables 0x4e1934/0x4dfad4 are zeroed inline by MissionLoadName, also by identity.
- BatimentResetAll writes 0x49a070 (4×22), not economy's 0x4dfad4; both tables exist.
- My earlier summary "MissionLoadName without BallonInit" was wrong; BallonInit is at 46c6b0. I sent corrections to ai-runtime and combat; COMBAT.md has the same wording.
- The Stage 10 call list was sent to core, combat, economy and ai-runtime.

Other contracts received:
- **Economy habitation** (main 7a60f54, for Stage 11). Caller order 46c16d..46c1b8: BatimentExiste 41a735 → PlaceBatiment 41c4ac → BatimentEstHabiter 41a5b8 → BatimentHabitable 41cc70 only if AL≠0 → BatimentModifyMap 419e97(index, 1) for every existing structure. API `construcoes_habitaveis.HabitacaoConstrucoes(aprendizagem, unidades_realizaveis, estruturas_realizaveis)` with identity wiring, `estrutura_habitada(index)`, `tornar_habitavel(world, index)`, and `DependenciaHabitacao` at 0x476851 / 0x476cb3. MONDE01 structure 0 completes with core's 23/20 radii.
- **Core Stage 14** at main 7b7b969: `SOMA_VISAO_MAXIMA_INSERCAO=11`. Missions reproduced 6/6 placement tests natively; MONDE01 now completes the unit scan against the v2 capture.
- **macOS M1 contract**: recorded as planned in docs/MISSIONS.md, with the Divers and iaInit corrections sent to macOS.

Stage 10 validation:
- 170 original-only captures came before translation and all match Python.
- Fresh native run: 71/71 mission tests, with zero skips, errors or faults. Reset coverage is 459 entries/segments, all at their declared stops: 176 leaf returns, 259 + 5 TerrainReset CALL stops, 4 FileOpen stops and 15 RechercheReset CALL stops. Each comparison covers the whole DGROUP+.bss image plus the units, Bags, projectiles, players and frame strings.
- The first full run failed one Stage 2 header segment (MONDE17, camera 4) on the harness's 1-second wall-clock timeout under load average 11. It is logged in .local/stage10-validar-timeout-failure.log and not counted. The test passed in isolation and the clean full rerun passed.
- Local: 71 tests with 27 optional skips. Common checks at 7b7b969: core 368/175, combat 236/145, economy 413/190, graphics 184/0, missions 71/27, ai-runtime 25/1, audio 2/0, workflow 8/0. No real mission was run.

## Codex resumption: Stage 11 light readiness (2026-10-28)

Read the new original human request and current AGENTS/roadmap/workflow/status/manuals; the old STOP is superseded. Preserved the existing clean `feat/re-missions` worktree, prior Claude work and all integration candidates. Before `scripts/workstream.py start missions`, verified no owned uncommitted changes or commits outside current main. The helper resumed the same checkout; it was fast-forwarded to the coordinator's declared main `8810b3730a0fb788af3eac2b447dea65372f597f`. The current helper supports Missions, so obsolete manual-integration instructions are not used. No new chats or subagents were created.

Stages9/10 remain integrated. Core Stage14 has already resolved the old unit15 radius10 stop; no discovery reimplementation is planned. The current bounded stage is the original L8 structure traversal. [STAGE11_READINESS.md](STAGE11_READINESS.md) records its byte-derived order, original state+5 predicate, lowAL gates, mode1 map call and shared return epilogue. [Static inventory](evidencias/terreno-estruturas-missao-inventario.json) pins three original intervals and existing provider hashes; the exporter performs no emulation. Economy's handoff assigns BatimentExiste and the caller to Missions. PlaceBatiment and habitation are consumed from committed main; Core15 map/reset provider consumption waits for the coordinator's integrated SHA.

The [M1 snapshot proposal](M1_SNAPSHOT_CONTRACT.md) now records source identity, acceptance/checkpoint, whole-state registry and exact known layouts/provenance. All static AI/runtime bytes stay covered by the complete DGROUP+.bss image; unknown logical extents must come from the integrated AI provider and are not inferred from example write traces. Dynamic allocations, pointer/alias identity and all retained bytes are included. Type2 Santuário/type3 Armazém identity and separate CP1252 briefing provenance are preserved. This is a proposal, not an exported/accepted full mission.

**Scheduling:** coordinator granted light work only. No native capture, Ghidra, heavy check, integration or engine translation was run in this readiness turn. Fresh execution is limited to static disassembly/export and whitespace/link consistency. Readiness is reported to coordinator `01a183e4-456e-77d0-9c6a-81b1c72ae887`; native work awaits its explicit heavy grant. Historical native totals above are not rerun results. After this stage integrates, only lightweight next-stage inventory may proceed until another scheduled grant.

### Stage11 committed-provider/capture scaffold follow-up

Within the same Stage11, merged verified Core15 main `b610bfad77ffadaa0ee5f6af02160d786ccfdc7b` into the clean feature as `5c417bfca30b08bbbe83794d99c922f0b443eedc`. Read RESET_MINIMAP and its actual committed source/harness: `modificar_minimapa_estrutura(world,index,ativo)` updates the minimap footprint only, with this caller's1 selecting mode6. It writes no structure bytes. Reset APIs preserve the live mines/RNG aliases but are not silently executed in an L8 fixture.

Prepared the native harness, eight declared fixture inputs and an original-only exporter without executing x86. It uses actual committed Core native harness inheritance, original caller/callee bytes, whole DGROUP+.bss and all non-stack/non-code mapped arenas, explicit economic buffers and mask/bonus aliasing. The continuation frame supplies original saved EDX/EBX and a real RET target. Import/MRO and one MONDE01 input fixture were checked in ordinary Python; no Unicorn instance, traversal or current-stage getter was executed. There is no Stage11 engine translation yet.

Coordinator approved four tiny MissionGetNum observations with the eight scan captures, in this same stage. Exact static bytes confirm a one-byte live field at496fe4, AX0..255 and retained highEAX16. Planned `consultas_missao.numero_missao(missao_u8)` accepts the actual explicit one-byte view and has no default or neighbor read; AI/runtime received that planned contract and keeps the dependency until tested integration. Its recovered raw reset provider is reported at main5d24c91; the production adapter remains separate work. No live sibling import is used.

Still LIGHT-only while coordinator owns maintenance integration. Suggested grant: original-only eight scans plus four query observations, inspect/commit captures before translation, release while implementing, then a separate serialized validation/integration window. Original capture script is not run and refuses to overwrite existing evidence. New human cutoff: development until18:25BRT on2026-10-28,18:25–18:40 handover only. At the first follow-up boundary the clock was16:35BRT; subsequent boundaries must be checked before accepting a heavy window. No extra session or subagent.

### Stage11 original-only capture boundary

The coordinator explicitly granted only the8scan+4query original-only window after Core released its process. At17:05BRT the first attempt exited0; heavy lease was released immediately, before light inspection/commit. No current-stage Python traversal or getter existed or was run. `evidencias/captura-terreno-estruturas-missao-original.json` SHA-256 `52232213ef3585a8523a04d24d5bcc9d472c90ff137769fb0cea48f9a41b777e`, source `24ca5a794ff4c6979a8f5ed7c23621d75adcdf32`; predecessor evidence unchanged. Ignored log `.local/stage11-capture-attempt1.log` is retained.

Observed8scan entries (7tails/1joined):6actual returns and2exact declared pre-CALL checkpoints46c1b1/41cdb9. Scan execution56segments,18minimap+30pixel-loop resumes, max156130instructions. Every input/output records all6blocks (whole585728-byte DGROUP plus every mapped non-stack/code fixture arena,5263360bytes total) and complete ordered parent/physical traces. Actual MONDE01 structures-only has1004parent calls, joined1832; no original engine call is replaced. Four separately counted MissionGetNum entries return AX0/1/127/255, preserve highEAX16, ignore neighbor poison and keep whole DGROUP byte-identical. These are independent original observations, not Python comparisons.

The capture is committed before engine translation. Next authorized work is light traversal/getter implementation and replay against this frozen capture while Core owns fresh heavy validation/integration. Required changed-native/domain/helper gates await a later explicit heavy grant. No native process remains, no full MissionLoad/M1/runtime acceptance, and no second research stage started.

### Stage11 light translation after independent capture commit

Capture commitment is `ed0172a364310b28584824b3e49dc63db371ed93`; only afterward added the traversal and two queries. Coordinator resolved a brief ownership ambiguity from economy's committed HANDOFFline412: Missions keeps BatimentExiste; Economy will not duplicate it. Public `consultas_missao.existe_estrutura(estruturas276000,indice)` returns AL0/1 from live state+5 after low16/protected0..999. Public `consultas_missao.numero_missao(missao_u8)` reads exactly the supplied live one-byte B/b view and returns AX0..255. Both are read-only, accept read-only views, copy/cache nothing and have no state/mission default. AI receives them through coordinator after tested integration, without waking its idle slot now.

`terreno_estruturas_missao.preparar_estruturas_no_terreno(ProvedoresTerrenoEstruturas)` preserves all original lowAL gates/call positions across1000slots. `provedores_terreno_estruturas_core(world,*,habitacao=None,mascara_tipo20=None)` composes actual Missions/Core/Economy functions over identical live pools. `preparar_terreno_missao(unit_providers,structure_providers)` joins existing Stage8 unit/capacity entry and the structure continuation. Results name completed indices/shared RET46b6f7, never world/M1 readiness. Missing callbacks carry original callee/CALL/arguments; exceptions preserve prior effects. No unsupported provider is a successful no-op and no lower body is copied.

Light frozen replay passes every one of the8cases across all6mapped-state hashes plus full parent/physical traces. Getters pass original4query capture values, live-view/neighbor/signed-byte/shape checks and all256structure state bytes at slots0/999. Local focused9discovered/5executed/4optional native skips. A memory-only Unicorn fixture initialization initially SIGILLed inside the sandbox; ordinary replay passed, then replaced that local allocation backend with a pure byte ledger so no JIT/CPU instance is needed for future local replays. Execution/resumption is explicitly forbidden there; fresh native tests still use real Unicorn. Logs preserved, frozen capture SHA unchanged.

Prepared later native matrix (not executed):8original scan inputs,48slot/state/habitation/type combinations,2type20alias cases,5missing-callback CALL stops,512read-only structure query entries and256mission query entries. Expected counts remain plans until the scheduled run. `validar_terreno_estruturas_missao.py --emular` will record new focused results; the full owned reporter writes a new Stage11 path rather than overwriting Stage10. Required domain/helper gates await coordinator heavy grant; no other native/check/Ghidra process was started during Core's lease.

### Stage11 new native/domain verification, integration preparation

Coordinator granted exclusive validation/integration. At17:26BRT fetched and merged verified Core16 main `b4c5a1072a2b2e494b3a6bf374bd978fc6e67b9a` as feature merge `13619b6e36deda8cbb7f289b8404d8371e57fe96`, before relying on its no-binding harness path. First `validar_terreno_estruturas_missao.py --emular` passes9tests/zero skips/errors/failures/native faults. Actual scan counts:63entries (62tail/1joined),56returns+7expected dependencies,161segments,49minimap+49pixel-loop preserved resumes,max156130instructions. All6mapped blocks are compared as raw bytes, plus exact parent/physical trace. Actual MONDE01 joined places8visible units and the inhabited sanctuary identically to the intact caller, over declared inherited fixture state.

Separately512original existence queries cover all256states at0/999 with poisoned high index bits and preservedEDX;256mission queries cover all byte values/neighbor poison/highEAX16. All768query segments match the exact scalar APIs and leave the whole global image unchanged. This is new differential validation; independent original8+4capture/hash remains frozen, and local byte-ledger replay is not counted as native evidence. Report `validacao/stage11-focused-x86.json`; first-success log `.local/stage11-native-attempt1.log` retained.

Required `python3 -B scripts/check.py --domain missions` passes80discovered/31optional skips, documentation links valid; log `.local/stage11-domain.log`. No source mismatch or native fault occurred. Commit this owned validation/handoff, then run the current shared-lock `integrate missions` helper and reproduce the changed9test slice on verified committed main. Remote delivery/finalfeature/merge hashes belong in the subsequent coordination/chat report, without amending a commit to embed its own future merge. Full M1 still needs complete remap, experience retrieval, real-world AI adapter and whole-load comparison; no extra implementation stage began.

## Stage11 integration and Stage12 light preparation

Stage11 delivered: original capture `ed0172a364310b28584824b3e49dc63db371ed93`, implementation `2f6d96b89039590c598f312752d4fe0e3c5b3607`, pushed feature `c0f0a873c3657e72a3e478cf6fd7ea73c84dd58a`, main merge `7f617fab29ce382f96b690ea70da25a33fab8bae`. Current helper held the shared lock through all common gates, full80native mission tests/zero skips, nonforce push and fresh ancestry. Worker fast-forwarded to fetched main, verified all four ancestors and unchanged original captureSHA, then reproduced9focused native tests with exact versioned report equality. Common local:Core401/186optional,Combat246/149,Economy424/196,Graphics192/0,Missions80/31,AI36/4,Audio20/3,Workflow8/0. Logs `.local/stage11-integration.log`, `.local/stage11-integrated-focused.log/.json`; tracked state clean. Heavy lease released to coordinator. No completeMissionLoad/M1 claim.

Coordinator then scheduled LIGHT Stage12 only, while Core17/Economy own native windows. [STAGE12_ORACLE_PLAN.md](STAGE12_ORACLE_PLAN.md), `estado_herdado_missao.py` and `bancada_mission_load_original.py` prepare a closed raw inherited registry and an original native-only oracle class using committed Core16 bindings. No class instance or whole-load instruction was executed. All native state blocks must be overwritten from explicit caller bytes/provenance; stored/live player types are separate, and no all-human constructor fixture is manufactured. Eleven external handlers and external arena bytes/identities are mandatory, without defaults. FileOpen/Read/Close wrappers remain native through CRT bindings; the permitted FileSeekI/O wrapper is explicitly disclosed. GlobalHandle takes actual locked pointers, matching pending Core17's live-buffer identity counterpart.

This is **not yet a runnable self-contained fixture**: complete raw input closure, concrete finite file/profile/resource handlers and segmentation/budget native calibration remain. Stage11's hashes cannot supply missing raw memory. Full Core17remap, Engin_RetrieveExperimente441623 and production AI/Economy adapter adoption remain explicit Python-composition dependencies. No whole-load translation begins before original-only capture. Proposed≤60second single-entry calibration/≤300second later return attempt are finite bounds only, not measured estimates or grants. Development ends18:25BRT/handovers18:25–18:40; preserve this scaffold if no safe window remains.

Light checks on this scaffold pass two CPU-free registry tests (live view identity, absent-pool rejection without mutation, overlap/duplicate-ID guards), AST syntax, import with native CPU construction forbidden, documentation links and diff whitespace. They do not validate native ABI/segmentation, external handlers or whole-load state. No whole-MissionLoad experiment, fixture-default shortcut, original engine substitution or broad heavy run took place in Stage12 preparation. The coordinator receives the exact pending checkpoint rather than an invented runtime estimate.

### Final late-provider note,18:19BRT

Core full remap is now published at main `09d3953c6dda02ba6e4f6ca9ac61e51ca48782e6`, with realMONDE01RET/AL1 reproduced by its owner. Read that immutable commit's RESET completion contract and verified its ancestry in local origin/main; did not import the live worktree or merge/validate this provider into the unexecuted Stage12 scaffold. Its resource identity API matches the plan. The original-only MONDE01 remap measured31.157seconds/56components/731segments; do not call that a whole-load estimate. Exact compressed raw capture blocks can inform inherited-state assembly with original bases/provenance, but cannot silently stand in for all program allocations/players.

This supersedes the earlier statement that full remap is unavailable. Remaining actual composition gap includes Core Engin_RetrieveExperimente441623 (canceled this window), real AI/Economy adapter adoption, complete explicit inherited inputs/external fixtures and the whole-load original oracle itself. No new implementation or native run was started at this boundary. Stage11 main7f617fa remains the delivered result; Stage12 local prototypee7ea60f plus this handover note remains pending, not main-integrated or acceptedM1.

## Stage12 runnable oracle and original-only whole-MissionLoad capture (Claude, 2026-10-28)

Resumed after the Codex handover in the same worktree; merged `origin/main` 9bf217d (f08f255 after 3d782ca). Full details, tables and limits: [STAGE12_ORACLE_PLAN.md — Stage12 result](STAGE12_ORACLE_PLAN.md#stage12-result-runnable-program-start-oracle-and-original-only-missionload-capture-2026-10-28-claude).

- **API/source.** `oraculo_carga_missao.BancadaCargaMissaoOriginal(entradas, *, segundos, instrucoes_segmento, …)`: `iniciar_relogio()`, `executar_inicio()` (CRT thread data, `AppInit`, native `CalculGame` frames to the real `CALL MissionLoad`), `snapshot_entrada()`, `iniciar_pegada()`/`pegada()`, `executar_mission_load(segundos, instrucoes_segmento=None)`, `imagem()`. Handlers in `fronteiras_carga_missao.py`; named inputs `EntradasNomeadas`. Scripts `capturar_carga_missao_original.py`, `validar_carga_missao_original.py`.
- **Result.** Intact MissionLoad 0x46c2cf ran from the real CalculGame frame to its **real return 0x42d22d, AL=1**, in 2.49 s / 1,425 segments / 1,400 declared binding calls, with no skip, trap, fault or limit. Startup 31.0 s. Captures: v1 `evidencias/captura-carga-missao-original.json` (61847e5, SHA `e0b7ca47…`), hardened v2 `…-v2.json` (81815eb, SHA `eb7d2303…`, byte-identical state/log), entry artifact `evidencias/entrada-carga-missao-original.json` (SHA `0692dea1…`). All committed before any translation.
- **Startup controls.** Live player types at entry are **(1,2,2,2)**, written by original `InitPlayer` and by the new-campaign `SetPlayerType` calls at 0x42c479..0x42c4b2; stored types are never initialized and `PlayerRetrieve` does not copy them. Saved XP `ff00`×20 from `Engin_ResetExperience`.
- **Checks** (`validacao/stage12-missionload-original-x86.json`, passed): replay, code-section SHA unchanged, segmentation invariance (77,777 vs 1,000,000), fill independence (0 computed bytes depend on fill), input footprint 1,757 read-before-write bytes: 0 skip-derived, 0 skipped-store, 4 declared inputs (clock RNG, CD letter), 4 entry return slot, 48 fill bytes read only by `__STOSD`/`__STOSB` cache touches before overwrite.
- **Tests.** Light `test_carga_missao_original.py` 10 passed (+1 native skipped in local mode); native replay `RISING_EMULAR=1` 11/11 passed; `scripts/check.py --domain missions` 93 tests/32 optional skips passed. Not run: full native missions suite, common gates, integration, committed-main reproduction.
- **Gaps / next.** No Python whole-load composition (deliberately not started). It must start from the entry artifact bytes and compare final image, AL and ordered binding log, using Core resets/remap/placement + `Engin_RetrieveExperimente` (main 3d782ca), the AI adapter for IaReset (main 977c890), Economy MarcheResetAll/initializers and Missions loaders. Startup limits: ProgIteration/AffGame/WndProc not executed, TEXTES.TXT not loaded, no research click, declared Windows subsets. M1 is **not** accepted.

## Stage13 M1 composition: whole MissionLoad in Python vs the original capture (Claude, 2026-10-28)

Merged `origin/main` 14c0122 (fast-forward). Source commit `b114fa7`; report [validacao/stage13-m1-composition.json](validacao/stage13-m1-composition.json) generated from that clean tree, CPU-free (no native run). Full method and limits: [STAGE12_ORACLE_PLAN.md — Stage13](STAGE12_ORACLE_PLAN.md#stage13-m1-composition-and-comparison-2026-10-28-claude).

- **Verdict: NOT M1.** The strict composition stops at **EnginInitTechnologie 0x441459, MissionLoad CALL 0x46c5af (owner Economy)**: `PropriedadeConstrucoes.ordens` is one copied 10,816-byte buffer, while the original and Core keep four distinct 2,704-byte Bag allocations behind `[0x4e19b8]` (0x41781000..0x41784000). Every earlier step (MakeMissionName … MissionPlaceTerrain, 26 steps) completed; effects are retained.
- **Bindings.** The 1,400 ordered requests equal the original log at every position: 1 fopen `D:\World\Monde01.ETA` "rb" → 0x7f000800, 1,019 fread (size/count/cursor/bytes SHA), 17 FileSeek (4,SET and 16×(0x200,CUR)), 20 profile reads, 57 GlobalAlloc/Lock/Unlock/Free and 114 GlobalHandle with identical pointers, 1 fclose. The 16 `GROUPE%02d` key strings live in an uncaptured native stack frame; at those positions all other fields are compared.
- **State.** All 938 allocation records (881 entry + 57 remap, freed bytes SHA-256 included) equal. The strict partial state differs from the original final image in 3,966 bytes: the four Bag allocations (26 each), live players +6 (4) and 3,858 DGROUP bytes, i.e. exactly what the six unexecuted tails write.
- **Diagnostic only (not M1 evidence).** With one declared copy-in/copy-out bridge for `ordens` around EnginInitTechnologie, the composition reaches **AL=1** and the **whole state is byte-identical**: 881 blocks / 2,659,375 bytes, 938 allocation records, AL and all 1,400 bindings. IaReset ran through the integrated adapter over live controls (1,2,2,2) without `DependenciaIA`.
- **Needed contract change (Economy, not edited):** `proprietarios.PropriedadeConstrucoes` (and consumers `cauda_carga.definir_tecnologia_unidades`, `aprendizagem.atualizar_ordens`) must accept the four live per-owner Bag pools by identity (Core's `bolsas_tipos_unidades`) and address owner j as `ordens[j] + type*104`. Non-blocking Core recommendations: accept the exact 16,384-byte minimap allocations; optional u16 views instead of Python lists for tiles/regions/color stack.
- **New modules:** `mapa_memoria_m1.py` (one memory map, in-place fill, list/scalar codecs, serializer), `arena_composicao_m1.py` (entry next-free page bump, handle==pointer, fill 0xA7), `ligacao_provedores_m1.py` (provider binding and guards), `composicao_carga_missao.py` (call order, named stops, `PONTES` diagnostic bridges), `comparacao_carga_missao.py`, `validar_composicao_carga_missao.py`. `carregador_cabecalho`/`carregador_unidades` forward FileSeek requests to a reader exposing `buscar`; plain readers are unchanged.
- **Tests.** `test_composicao_carga_missao.py` 10 run / 0 skipped / passed (strict-vs-capture main test, bridged diagnostic, closure, no constructor defaults on a randomized snapshot, guards, cache divergence, alias identity incl. the AI adapter, arena policy). `scripts/check.py --domain missions` under the lease: 103 tests, 32 optional native skips, passed. Not run: native suites, common gates, integration, committed-main reproduction.
- **Next blocker:** the Economy `ordens` contract above. After it lands, rerun `validar_composicao_carga_missao.py`; the strict run is expected to reach the return, and only then can M1 be claimed.

### Stage13 compatibility step for the Economy per-owner Bag contract (2026-10-28)

Merged `origin/main` eb2f1c2 (fast-forward; Stage13 integrated). To let Economy's per-owner `[0x4e19b8]` contract (feat/re-economy `31b5232`, not yet on main) integrate after Missions, `ligacao_provedores_m1.ORDENS_POR_DONO = hasattr(proprietarios, 'validar_ordens')` selects the contract on the import path. Per-owner: `PropriedadeConstrucoes(construcoes, ordens=w.bolsas_tipos_unidades)` (identity verified, `ordens` permitted by the guard, rebinding still raises), and the `ordens` diagnostic bridge is skipped (`bridges_not_needed`), so the diagnostic run equals the strict run. Legacy: unchanged (strict stop at EnginInitTechnologie 0x46c5af plus the bridged diagnostic). Strict semantics are unchanged; the committed Stage13 report is not regenerated.

- Tests assert the outcome for the contract in use: legacy = strict stop + bridged equality; per-owner = strict AL=1 with whole-state, record and binding equality, no bridge.
- Legacy (this checkout): `test_composicao_carga_missao.py` 10/10 passed.
- Per-owner, scratch only: Economy `31b5232` files were extracted read-only to `.local/economy-31b5232/`; the eight differing non-test modules were placed in `.local/economy-31b5232-overlay/`, first on `sys.path` after the economy bootstrap, through a scratchpad runner that asserts the overlay modules are imported. Nothing foreign is committed. Results: `test_composicao_carga_missao` 10/10 passed (strict reaches AL=1, whole state equal, no bridge). Also `test_terreno_estruturas_missao` 9 run/4 skipped, `test_auxiliares` 6/2, `test_carga_missao_original` 11/1 and `test_estado_herdado_missao` 2/0, all passed. Log: `.local/stage13-compat-per-owner-overlay-tests.log`. This is NOT M1 evidence; Step 2 writes the strict report on integrated code.

## Stage14 strict M1 composition on integrated code (Claude, 2026-10-28)

Merged `origin/main` ff2f5cf (Economy per-owner `[0x4e19b8]` Bag contract integrated). Source `ea1aac5` makes that contract mandatory (`ligacao_provedores_m1` raises ImportError without `proprietarios.validar_ordens`) and removes the `ordens` bridge, `PONTES` and the legacy test branch. Report [validacao/stage14-m1-composition-strict.json](validacao/stage14-m1-composition-strict.json) was generated CPU-free from that clean tree. The Stage13 report is unchanged.

- **Strict result: M1 candidate (not accepted).** All 32 steps ran with no bridge and the run reached the 0x42d22d return semantics with **AL=1**. **Whole state equal: 881/881 blocks, 2,659,375 bytes, 0 differing.** **938/938 allocation records** and **1,400/1,400 binding requests** are equal. The poisoned provider excess is unchanged. IaReset returned EAX 0 over live controls (1,2,2,2).
- **Determinism.** A second run gave the identical state SHA-256 `da9ce107…` (also equal to the Stage13 bridged run), the identical binding-request SHA-256 and the identical AL.
- **Explicit exclusions** (listed in the report):
  - the 16 `GROUPE%02d` key strings live in an uncaptured native stack frame; every other field at those positions is compared;
  - the allocation-record caller-return and stack-dword metadata is native observation, not state;
  - the native stack block is absent from the original final capture.
- **Tests.** `test_composicao_carga_missao.py`: 11 run, 0 skipped, all passed. This includes the strict whole-state test, determinism and the mandatory-contract guard. `scripts/check.py --domain missions` under the lease: 104 tests, 32 optional native skips, passed (log `.local/stage14-domain.log`). Native suites, common gates, integration and committed-main reproduction are left to the coordinator.
- **Acceptance.** M1 is accepted only after the coordinator's integration and committed-main reproduction.

## Stage15 (M2.1): MONDE01 first frame, original first (Claude, 2026-10-28)

Merged `origin/main` 81ebbf9; M1 was accepted at 927c7e5. Full contract: [docs/MISSIONS.md — Stage15](../../docs/MISSIONS.md#stage15-m21-monde01-first-frame-original-first). Readable summary: [QUADRO1_MONDE01.md](QUADRO1_MONDE01.md).

### Commits

| Commit | Content |
|---|---|
| `e6aa305` | bench source |
| `ca35221` | original capture and trace, before any translation |
| `51381b1` | validation and summary |
| `6516b41`, `e15465b`, `46dc93d` | isolation bench and fixes |
| `d619787` | isolated captures and the M1 footprint re-validation |
| `b25e8d6` | translation |
| `0a7da75` | native differential |

### API inputs

**Bench** (`oraculo_quadro_missao`):

`BancadaQuadroMissaoOriginal(EntradasQuadro(base=EntradasNomeadas, cursor, registradores_chamador))` exposes `executar_cauda_carga`, `executar_entre_quadros` and `executar_quadro`, plus `rastro_json()`.

`Isolamento(bancada, rotinas, perturbacoes, observador)` pauses at routine entries.

The scripts are `capturar_quadro_missao_original`, `validar_quadro_missao_original`, `capturar_isolados_quadro1` and `diferencial_fim_missao`.

**Translation** (`fim_missao`):
- `evento_em_curso(view 0x4e1b0e)`
- `testar_fim_missao(jogador, condicoes 0x4e1d20/100, estado 0x4e1d84/14, contagem_inicial 0x4e1a3a/2, exercitos 0x4e1928/8, exercitos_ia 0x4dfaa8/16, ConsultasFimMissao)`
- `consultas_publicadas(estruturas 0x49a0c8/276000, Economia over 0x4e2ea8, missao_u8 0x496fe4, **optional providers)`

### Supported domain

The frame-1 capture covers the accepted M1 path, then three phases:
- **(a)** the load-state CalculGame tail;
- **(b)** the window loop;
- **(c)** frame 1, which ends at its real return `0x475063`.

TestFinDeMission supports every record type. Callees that are not supplied stop as named dependencies.

### Order of mutations and callbacks

- **Frame phases:** see the trace. The boundaries are not executed and are recorded in call order.
- **TestFinDeMission:**
  1. Process records 0..9 in order, setting or clearing each record's mark.
  2. Apply the mission-6 override.
  3. Set the latch, then the `0x4e1a3a`==0 override.
  4. For missions 8/13, run the owner-count scan into `0x4e1d85`.
  5. Return AL.

### Original addresses and hashes

The intact executable SHA-256 is `6c556520…43fb`, with code-section SHA `02985de5…` unchanged after every run. Main addresses:
- CalculGame `0x42c868`
- ProgIteration `0x47500e`
- `_WinMain@16` loop `0x4601c0`
- EvenementEnCours `0x4581b6`
- TestFinDeMission `0x458606`

Evidence files:

| File | SHA-256 |
|---|---|
| captura-quadro1 | `c06f78ea…` |
| rastro | `45859330…` |
| captura-isolada | `d0365055…` |

### Validation

| Report | Result |
|---|---|
| `validacao/m2-frame1-original-x86.json` | passed (see QUADRO1_MONDE01.md) |
| `validacao/stage12-missionload-original-x86-tbflush.json` | passed |
| `validacao/m2-fim-missao-differential-x86.json` | passed: 38/38 compared equal, 10 named dependency stops |

Light tests: `test_quadro_missao_original.py` and `test_fim_missao.py`.

### Gaps and dependencies

**Graphics.** Does AffGame, running over the (b) state, store into:
- `0x4e2f78`
- `0x4e1b0e`
- `0x4e060c` / `0x4e0610`
- `0x507d54`
- `0x50a9b4` / `0x50a9b6`
- `0x4e1d18`

Frame 1 reads these. AffGame cannot run on this bench because its sprite banks were never loaded.

**Audio.** The sound library is a boundary because PlaySnd_InitSoundLib never runs. MCICD_* return early while `[0x4e2f29]`=0.

**Core / Economy / Combat / AI.** TestFinDeMission still needs these providers:

| Provider | Address |
|---|---|
| BatimentGetCase | `0x41aee2` |
| CaseGetZoneInfluence | `0x47bf66` |
| RechercheGetNbInvention | `0x470554` |
| PlayerEstAllie | `0x46d838` (combat `alvos_alcance.aliados` exists; its register mapping is not verified here) |
| GetTopLeftCaseZoneInfluence | `0x47c114` |
| CaseEstIlluminee | `0x47693a` |

MONDE01 needs BatimentGetCase and CaseGetZoneInfluence as soon as a type-3 cave exists.

**AI/runtime.** The frame pipeline consumes `fim_missao` and the trace. No whole-frame composition was built here.

**Inputs.**
- The cursor (0,0) is a declared input, and it causes an edge scroll in frame 1.
- The M1 startup still does not execute WndProc or AppWindowInit; their static UI stores are read and classified in the footprint.
- The `[esp+8]` stale local of the mission 8/13 scan is not modeled.

### Not run

- The full native missions suite
- The common gates
- Integration
- Committed-main reproduction

## Stage16 (M2): influence queries and register trace view (Claude, 2026-10-28)

Merged `origin/main` ec931d2, which contains M2.1. Contract: [docs/MISSIONS.md — Stage16](../../docs/MISSIONS.md#stage16-m2-influence-zone-queries-and-the-register-trace-view).

### Commits

| Commit | Content |
|---|---|
| `c1bb6b2` | injection source |
| `60f00c2` | original influence capture |
| `72dd272` | translation and `fim_missao` wiring |
| `3cb9173` | register-view source |
| `0002794` | both differential reports |
| `1594ae7` | register view |

### API inputs

- `influencia_missao.zona_influencia(table 0x50c614/4000, AX cell)`
- `influencia_missao.canto_zona_influencia(table, AX zone 0..399)`
- `fim_missao.consultas_publicadas(..., influencia)`: the table argument is now required.
- `Isolamento(..., injecoes={routine: f(iso, phase, regs)})`, with `chamar_folha` and `verificar_puro`, for native leaf calls injected at a pause.

### Domain

- The two influence queries cover the complete original domain, except that GetTopLeftCaseZoneInfluence is protected for AX ≥ 400, where the original reads beyond the table.
- CaseInZoneInfluence `0x47bfdd` is not translated. It is not reached.

### Mutation and callback order

Neither query performs a store. Both preserve EBX/ECX/EDX, which the native capture and the differential checked.

### Validation

| Check | Result |
|---|---|
| Influence native differential | 5 tables × 66,192 calls, all equal |
| `fim_missao` native differential v2 | 38/38 equal |
| CPU-free tests | full sweep replay |

### Gaps and dependencies

- **Economy:** BatimentGetCase is the next stop of the MONDE01 cave condition. RechercheGetNbInvention is also Economy's.
- **Core:** CaseEstIlluminee.
- **Combat:** PlayerEstAllie register mapping still needs confirmation.
- **Graphics:** the AffGame inter-frame write set is pending, and the boundary policy may change when it arrives.
- **AI/runtime:** no extension of `mapa_memoria_m1` / `ligacao_provedores_m1` has been requested yet; I will implement one if asked. The register trace view it requested is published.
- **Frame limit:** the original oracle is held at frame 1 until the frame-1 comparison passes.

## Stage17 (M2 round 3): display path executed (Claude, 2026-10-29)

Merged `origin/main` 67fb81f. Contract: [docs/MISSIONS.md — Stage17](../../docs/MISSIONS.md#stage17-m2-round-3-oracle-with-the-display-path-executed). Summary: [QUADRO1_EXIBICAO.md](QUADRO1_EXIBICAO.md).

### Commits

| Commit | Content |
|---|---|
| `3ff4b21` | scenario source |
| `46a4d46` | display M1 entry and capture |
| `8c7c47a` | display frames 0/1 capture and trace |
| `9017f11` | comparison script |
| `6934a0c` and later | validator fix and writer attribution |
| `1980950` | reports |

### API inputs

- `cenarios_oraculo.bancada(cenario, fill, clock, ...)`
- `oraculo_exibicao_missao.BancadaExibicaoOriginal(EntradasExibicao(quadro, ticks, preenchimento_superficie))`, with the same phase methods as the frame bench.
- `exibicao_declarada.DirectDrawDeclarado(bench)`: declared DirectDraw COM objects.

### Supported domain

The display scenario covers MONDE01 startup, MissionLoad and frames 0/1.

### Order of mutations and callbacks

The real loop runs in the original's order. Every DirectDraw call is recorded in order (`directdraw_calls` per phase).

### Validation

All passed:

| Check | Report |
|---|---|
| Composition regression | `m2r3-m1-composition-strict-exibicao.json` |
| MissionLoad validation | `m2r3-missionload-exibicao-x86.json` |
| Frame validation | `m2r3-frame1-exibicao-x86.json` |
| Comparison and attribution | `m2r3-frame1-v1-vs-exibicao.json`, `m2r3-v1-vs-exibicao-writers.json` (both scenarios reproduced) |

### Attempts preserved under `.local/`

- **M1 validation** crashed on the 4-field footprint tuples (`m2r3-m1-validation-attempt1-unpack.log`).
- **Writer attribution** missed unaligned stores and host binding writes (`m2r3-writers-attempt1-missed-unaligned.json`).
- **Exploration logs:** `m2r3-explore-*.log`.

### Gaps and dependencies

| Owner | Gap |
|---|---|
| Graphics | final display backend, still to wire in when it lands |
| Core | inventory CRT `fgets` `0x48ce96` (TEXTES.TXT via FileReadLine) and `fseek` `0x48cda2` (ReadLZSImage), so text and LoadPie can run |
| AI/runtime | the frame composition should use the display artifacts and model viewport NextAnimTerrain/NextAnimVeget (CRT rand, `0x4e1d18`), MouseInit/MouseSetZone geometry and the startup ProgIteration counters |
| Missions | the oracle is still held at frame 1 |

**Size.** The display entry and captures total about 60 MB (25k bank allocation records and per-block hashes).

## Stage18 (M2 round 4): frozen display reference, Graphics' backend, comparison policy (Claude, 2026-10-29)

Merged `origin/main` 81e0a26. Contract: [docs/MISSIONS.md — Stage18](../../docs/MISSIONS.md#stage18-m2-round-4-frozen-display-reference-and-comparison-policy). Policy: [POLITICA_COMPARACAO_M2_1.md](POLITICA_COMPARACAO_M2_1.md).

### Commits

| Commit | Content |
|---|---|
| `af1ccbe` | backend wiring and policy script |
| `5b5256f` | backend comparison script |
| `ac6b5f3` | M1 v2 reference (generated from `af1ccbe`) |
| `73badbe` | frames v2 reference (generated from `ac6b5f3`) |
| `c40999e` | backend equivalence |
| `8525e0d` | policy tracker fix and tests |
| `24ae9e1` | policy and validation reports |

### API inputs

- **`cenarios_oraculo`:**
  - `bancada('exibicao', ...)`: Graphics' backend, `-v2` artifacts.
  - `caminho('exibicao_interino', ...)`: the Stage17 artifacts, historical.
- **`politica_comparacao_quadro1`:** produces `exclusion_mask`, per-range writers and readers with context, and the surface proof.

### Mutation order

Unchanged: the real loop, with every DirectDraw call recorded in order by the backend.

### Original hashes

The intact executable is unchanged (code-section SHA `02985de5…`). The artifact hashes are in each report.

### Validation

All passed: backend equivalence (except the 10 backend-pointer bytes), the Stage14 regression, both original-only validations, and the policy (with phase states reproduced).

### Discarded and failed attempts (preserved under `.local/`)

- **Dirty-provenance capture.** A first M1 v2 capture recorded an uncommitted bench. Its local commit was never pushed; I soft-reset it, and the files are under `m2r4-dirty-provenance/`.
- **Policy tracker.** The first tracker kept display roots open across sibling calls (`m2r4-policy-attempt1-stale-root-context.json`).

### Gaps and dependencies

| Owner | Gap |
|---|---|
| Core | inventory CRT fgets `0x48ce96` and fseek `0x48cda2`. Text and LoadPie then run, and I recapture as a new version. |
| Coordinator | decide how to treat the allocation records of the 146 freed menu banks |
| AI/runtime | compare against the v2 reference with the `exclusion_mask` |
| Missions | the oracle is held at frame 1 |

The policy proof covers only the declared phases and must be re-derived for M2.2.

## Stage19 (M2 round 5): N-frame tooling, M2.2 plan, v3 preparation (Claude, 2026-10-29)

Merged `origin/main` d94a59e. The coordinator decided the 146 freed menu-bank allocation records stay **compared**. The `-v2` reference is unchanged and no capture beyond frame 1 is evidence. Plan: [PLANO_M2_2.md](PLANO_M2_2.md).

### Commits

| Commit | Content |
|---|---|
| `7962e46` | N-frame bench and policy |
| `9af33f9` | v3 fixtures and scenario |
| `628e473` | event probe |
| later | budgets, summary fix, docs and tests |

### API inputs

- `oraculo_quadro_missao.eh_fase_quadro(fase)` and `nomes_fases(k)`
- `BancadaExibicaoOriginal.executar_quadros(n, segundos)`
- `politica_comparacao_quadros.py --quadros N --relatorio …`
- `varrer_eventos_quadros.py --quadros N [--cenario exibicao_v3]`
- `ArquivosCRT.fseek_crt` / `fgets_crt` (Core inventory ABI)
- `BancadaExibicaoOriginal(..., v3=True)`, scenario `exibicao_v3`

### Validation

| Check | Where | Result |
|---|---|---|
| N=1 policy | `.local/m2r5-policy-n1.json` | identical mask and totals to the committed M2.1 policy |
| N=3 policy | `.local/m2r5-policy-n3.json` | passed, 7/7 phases reproduced |
| 130-frame probe | `.local/m2r5-eventos-130.json` | see the plan |
| v3 probe (2 frames) | `.local/m2r5-eventos-v3-2.json` | LoadPie executed; the per-phase logic indicators equal `-v2`. Two earlier attempts stopped at budget guards; their logs are preserved. |
| Light tests | `test_preparacao_m2_2.py` | 4 tests |

### Not run

- The full N-frame policy over 128 or more frames: it costs about 3 s per frame per pass with hooks.
- Any v3 capture.
- Integration.

### Dependencies

| Owner | Needed |
|---|---|
| Core | `ftell` `0x48cf11`, which text needs |
| Audio and coordinator | the CD-audio availability input. It drives `0x4e1d18` every frame. |
| Audio | confirm that sound-library state is never read by logic |
| AI/runtime | model AffGame's store to `0x4e05a2` from frame 2 on |
| Missions | extend the display-clock named input beyond 4,096 answers before M2.3 |

## Stage20 (M2.2): 128-frame original capture and comparison policy (Claude, Mac mini, 2026-10-29)

Executed on the Mac mini (Apple M4, 16 GB, macOS 27.2, python 3.9.6, unicorn 2.1.4) from `feat/re-missions` merged with main `8564ca7`. Reference: the frozen `-v2` display scenario. Text/LoadPie (v3) is out of scope. Every artifact is original-only; no Python translation was imported.

### Coordinator decisions recorded in the scenario

- **CD audio:** no CD track plays. This is a declared input (`named_inputs.cd_audio`), and every phase checks `[0x4e2f28] == 0`. CalculGame therefore advances the shared cursor `0x4e1d18` every frame; a CD-playing run would be a different scenario.
- **HUD flag `0x4e05a2`:** compared. The policy confirms a logic writer (`CalculMatiere+0x12c`).
- **The 146 MenuInit bank records freed in load_tail:** compared.

### Commits

| Commit | Content |
|---|---|
| `e8bcec5` | delta-form N-frame capture tool and replay check |
| `717bd46` | workspace-relative provenance path; shared per-phase record builder |
| `ad50ab2` | original-only 128-frame capture (`evidencias/captura-quadros128-monde01-exibicao-v2.json.xz` + manifest) |
| `1a01591` | 128-frame comparison policy (`validacao/m2-2-politica-comparacao-128-quadros.json`) |
| later | segment-parallel tool (M2.3a), policy refactor, docs |

### Capture (API inputs for AI/runtime)

[capturar_quadros_exibicao_missao.py](capturar_quadros_exibicao_missao.py) writes 257 phases: `load_tail`, then `between_frames`/`frame1` and `between_frames{k}`/`frame{k}` up to 128. Each phase has the following fields:
- the M2.1 fields: entry/exit registers, RNGs, counts, bindings, boundaries, Windows/clock answers, DirectDraw calls and display state;
- `observed`: the CD flag, cursor `0x4e1d18`, HUD flag, cycle counter and view origin;
- `state_delta`: `released`, then `allocated`, then `ranges`, applied in that order ([delta_estado_missao.py](delta_estado_missao.py));
- `state_after.summary`;
- `state_after.full_state` at frames 1, 31, 32, 45, 50–52, 64, 100, 101 and 128.

The top level also has `state_s0` (the `-v2` MissionLoad final state), `named_inputs`, `decisions`, the final `allocations` and the `entry_trace`. Events carry no display-context flag.

- xz SHA-256 `4c8f5c14a9623131dd019eafcdc49ea63054ee358f9defde58c12cb949f59ff3` (8,650,900 bytes).
- Raw JSON SHA-256 `1ad031b96300e5c632fd5b6b7857ae30792f78e86531e4f17d1bf7124c6dd930` (165,916,863 bytes), kept in `.local/m2-2/`.

### Validation

| Check | Result |
|---|---|
| MissionLoad final state vs the `-v2` MissionLoad capture | equal |
| load_tail / between_frames / frame1 vs the `-v2` frame-1 capture | equal: summary, bindings, boundaries, Windows/clock answers, DirectDraw, registers, RNGs |
| Replay of s0 + deltas, read back from the written xz | 257/257 summaries and 11/11 checkpoint full states equal |
| Determinism | two full runs (tools `e8bcec5`, `717bd46`) are identical apart from wall-clock fields, `source_revision` and the provenance path |
| Policy `--quadros 128` | passed in 1,753 s; every phase state reproduced; pass-1 summaries equal the capture's |
| Policy totals | 154,059 changed bytes; cumulative mask 153,060 display-only bytes, **999 compared logic bytes**, 0 without an observed writer, 0 logic-context surface accesses |

223 logic bytes first change after frame 1:

| Writer | Bytes |
|---|---|
| NextGouttes (rain-drop slots) | 197 |
| UpdateChamp | 9 |
| EnginNextEtape | 8 |
| NextAnimVeget | 6 |
| ScanNouvellePatate | 2 |
| HUD flag (AffGame and CalculMatiere) | 1 |

### Observed facts AI/runtime predicted

- **View origin:** (3,5), (2,4), (1,3), (0,2) after frames 1–4, then (0,1) after frame 5 and (0,0) from frame 6 on.
- **HUD flag:** 0 after `between_frames2`, and after every between-frames phase whose AffGame counter is not a multiple of 5.
- **Cursor `0x4e1d18`:** 0x25 after frame 128.

### Segment-parallel execution for M2.3a ([segmentos_quadros_missao.py](segmentos_quadros_missao.py), not evidence)

**Pass A** runs the frames sequentially and saves exact snapshots: at the MissionLoad return and after every K-th frame.
- **Memory:** every Unicorn region, with its bytes and protection.
- **CPU:** the `context_save` CPU state.
- **Python state:** the bench's Python state, pickled. The arena, DirectDraw backend and binding registry are saved without their Unicorn handles.

**Pass B** resumes a segment from a snapshot:
1. It builds a fresh bench (constructor only).
2. It restores the snapshot in place, so the objects that bindings hold keep their identity.
3. It reinstalls the frame hooks and runs.

Proof on M2.2 (K = 32, segments on separate lease slots):

| Check | Result |
|---|---|
| Pass A records vs the committed capture | 257/257 equal (wall-clock `seconds` excluded) |
| Segments 32–64, 64–96, 96–128 vs pass A and the capture | 192/192 phase records byte-equal, about 40 s each |
| Policy pass 2 by segment (0–32, 32–64, 64–96, 96–128, about 4–5 min each), merged | every report field equal to the sequential `--quadros 128` report (pass-1 data taken from the capture's exact deltas) |

Measured costs: pass 2 runs at about 8–9 s per frame per slot; peak RSS is 1.0–1.3 GB per segment and 2.6 GB for the sequential capture.

### Not run / gaps

- **M2.3:** not started; it needs a new authorization.
- **Display clock beyond 4,096 answers:** M2.3 needs it. The agreed definition is Core's: the same rule `0x123456 + 40·k`, extended.
- **v3 (text/LoadPie):** still waits for Core's `ftell`.
- **Python per-frame comparison:** AI/runtime runs it against these artifacts.

## Stage21 (M2.3): 9,200-frame original capture and long-run comparison policy (Claude, Mac mini, 2026-10-29)

Executed on the Mac mini (Apple M4, 16 GB, macOS 27.2, python 3.9.6, unicorn 2.1.4) with the tools at `eb08940`. Reference: the frozen `-v2` display scenario, the same declared inputs and decisions as Stage20. Window: frames 0–9,200; the coordinator dropped the extension to 10,800. Every artifact is original-only; no Python translation was imported.

### Commits

| Commit | Content |
|---|---|
| `5e5c746` | binding-event log compaction (`EventosCompactos`) and a light pass A; fixes `passo-a` on int snapshot keys |
| `45aa285` | display clock extended to 200,000 answers by Core's rule `0x123456 + 40·k` |
| `5a14cea` | aggregated pass-2 access keys, validated exactly on M2.2 |
| `192f000` | segment-end records (allocations, entry trace, answers, code integrity) |
| `eb08940` | part packager with re-read verification ([pacotes_quadros_missao.py](pacotes_quadros_missao.py)) |
| `6d5c27d` | original-only capture in 10 parts (`evidencias/m2-3/`) + manifest |
| `ab99eab` | long-run comparison policy (`validacao/m2-3-politica-comparacao-9200-quadros.json`) |

### Capture (API inputs for AI/runtime)

[evidencias/m2-3/](evidencias/m2-3/) holds `captura-quadros9200-monde01-exibicao-v2.parteNN.json.xz` (NN = 00–09) and the manifest `captura-quadros9200-monde01-exibicao-v2.manifest.json` (schema `compressed-evidence-manifest/2`).

| Part | Frames | Phases | xz bytes | Raw bytes |
|---|---|---|---|---|
| 00 | 0–1000 (`load_tail` … `frame1000`) | 2,001 | 9,708,140 | 123,523,842 |
| 01–07 | 1001–2000 … 7001–8000 | 2,000 each | 9,298,748–9,312,468 | about 122.4 MB each |
| 08 | 8001–8990 | 1,980 | 9,300,020 | 121,268,819 |
| 09 | 8991–9200 | 420 | 8,862,004 | 297,283,210 |
| total | 0–9200 | 18,401 | 93,012,400 | |

The raw JSON of each part is kept under `.local/m2-3/partes/`; the manifest pins both hashes per part.

- **Every part** opens with `opening_state` (`full_state`, `summary`, `compared_summary`, `masked_sha256`) and carries complete deltas, display bytes included.
- **Every phase** keeps the Stage20 record fields; `state_after` adds `compared_summary` and `masked_sha256`.
- **Full states** also follow frames 8999, 9000 and 9176 (part 09).
- **Run-level records:** named inputs and decisions in part 00, with the display clock declared by its rule, N = 200,000 and the SHA-256 of the answer list (its first 4,096 answers equal the Stage20 ones); final allocations, entry trace, declared Windows answers, import resolutions and code integrity in part 09.

Definitions (also in the manifest). The mask is the policy's `cumulative.exclusion_mask`, sorted `[start, end)` ranges; `native_stack` is never a block.
- **`compared_summary`:** `resumo_imagem` of the state with every masked byte set to 0 (blocks sorted by name, each hashed as `<II base, size>` + bytes).
- **`masked_sha256`:** SHA-256 over, for each block sorted by name and each mask range intersecting it in address order, `<II start, length>` + the bytes of that intersection.

A Python run that matches the original reproduces `compared_summary` in every phase. `masked_sha256` hashes only the excluded display bytes, so a mismatch there alone is display-only.

### Execution

| Step | Result |
|---|---|
| Pass A (sequential, light, snapshots at frame 0 and every 250 frames) | 7,861 s, peak RSS 1.87 GB, 37 snapshots |
| Records (37 segments from the snapshots, lease slots) | 218–307 s each |
| Pass 1 (from the records, CPU only) | 18,401 phases, 154,620 changed bytes, about 6 min |
| Pass 2 (37 segments, aggregated keys, 5 then 7–8 lease slots) | 1,817–2,783 s each; 11:22–15:54 wall clock |
| Long report | `passed: true` |
| Packaging and re-read verification | 1,696 s, peak RSS 3.6 GB |

### Validation

| Check | Result |
|---|---|
| Segment 0–250 records vs the M2.2 capture | 257/257 phases equal |
| Pass-2 summaries vs pass-1 record summaries | 18,401/18,401 equal |
| Re-read of the written parts | raw hashes; chain of opening states (part 00 opens with s0); every replayed summary, compared summary and masked hash; every full state |
| First 128 frames vs the committed M2.2 capture | 257/257 phases equal |
| Policy totals | 154,620 changed bytes; cumulative mask 153,060 display-only bytes, **1,560 compared logic bytes**, 0 without an observed writer, 0 logic-context surface accesses (display 1,282,055,899, backend 5,109,920) |

The 1,560 logic bytes are the 999 of M2.2 (the same addresses) plus 561 that first change after frame 128. 413 of those first change in the 9,000-frame window, the first raid. Their main writers there are CheminCalcul (108), SetMiniMap (52), EnginSetType (46), ProjectileSet (32), CreerEngin (31) and Chemin_ModifieZone (30). The remaining 148 spread over frames 129–8,999; their writers are UpdateChamp (116), ScanNouvellePatate (31), CalculFatigue (16), EnginNextEtape (8), ProgIteration, CalculGame and GameNextFrame.

### Not run / gaps

- **Python per-frame comparison over 9,200 frames:** AI/runtime runs it against these parts.
- **Native pass-2 hooks** (Core `5580c2d`, about 6.45× faster): not used for M2.3. Before any later long policy run (M3), check on the mini that they reproduce the M2.2 128-frame policy.
- **v3 (text/LoadPie):** still waits for Core's `ftell`.

## Stage22 (M3): scripted-input harness, probes, S1 victory, D1 defeat, window captures (Claude, Mac mini, 2026-10-29/30)

Executed on the Mac mini, original only (no translation imported). Full details, rules and timelines: [m3/SONDAS_M3.md](m3/SONDAS_M3.md).

### Commits

| Commit | Content |
|---|---|
| `d79f68a`, `e17dbf0` | Step 0 static targets ([m3/M3_ALVOS.md](m3/M3_ALVOS.md)) and their tests in the missions suite |
| `3befc83` | scripted-input harness ([m3/entrada_roteirizada.py](m3/entrada_roteirizada.py), schema `rising-lands/monde01-scripted-input/1`), frame-128 checkpoint, inputs P1–P3 |
| `f058844`, `55db1d5`, `085fe35`, `01fa7d8` | probes P1–P7 and K1, each replay-checked on two runs ([m3/sondas/](m3/sondas/)) |
| `01745da`, `d18add9`, `5f6f155` | pass-2 whole-state captures of the P1, P2 and P6 windows |
| `1191e4c`, `fef8e02` | S1 input builder; snapshots kept at state size |
| `0ebfe70`, `82ec5ea` | S1 reaches victory; replay-checked capture `m3/sondas/S1` |
| `bab6c7c`, `93f3b61` | D1 defeat input and its replay-checked capture `m3/sondas/D1` |
| `8c7a2a0` | pass-2 whole-state capture of the S1 window, plus two pass-2 tool fixes |

### Captures (API inputs for AI/runtime)

| Capture | Frames | Result | Files |
|---|---|---|---|
| S1 (victory) | 129–17050 | AL = 1 at 16933; `MenuInit(0x13)` 17032; confirmation click → `MissionNext` 17043 | `m3/entradas/S1.json`, `m3/sondas/S1/{replay,relatorio,resumo}.json`, `*.jsonl.xz` |
| D1 (defeat) | 129–15700 | unit count 0 at 15555 (AL = 1, latch 0); `MenuInit(0x13)` 15654; `PartieGetResultat` 0 and failure branch 0x42c9d5 at 15655 | `m3/entradas/D1.json`, `m3/sondas/D1/...` |
| S1 window, pass 2 | 129–17050 | policy passed: 33,844/33,844 phases, 920,200 changed bytes, 654,586 logic bytes, 0 without writer | `m3/sondas/S1/captura-janela.parte00..16.json.xz` + manifest, `mascara-janela.json`, `politica-janela.json.xz` |
| P1, P2, P6 windows, pass 2 | to 629, 729, 2400 | policies passed | `m3/sondas/{P1,P2,P6}/captura-janela.*` |

The two S1 and the two D1 runs from F0 give equal record files (quadros, entradas, comandos, fronteiras). D1's published `resumo.json` lists a snapshot every 250 frames.

### Defeat trigger [B]

`TestFinDeMission 0x458735` is the only store of AL = 1 with latch 0x4e1d84 = 0, when the player unit count 0x4e1a3a is 0 (`CalculEnginNextEtape` counts pool slots whose state is neither 0 nor 4). `MenuInit 0x4684d4` (menus 0x11 and 0x17) only resets the latch. MONDE01 has no trap cells, so every unit must fall to the raiders.

### Pass-2 tool fixes (`8c7a2a0`)

- `relatorio_longo`/`comparar_politica` globbed `politica-0*.pickle`, which skips segments from frame 10000. M2.3 and P1/P2/P6 never reach 10000.
- The policy credits `KERNEL32.GlobalAlloc`'s declared fill to that binding. It runs only at frame 17043 in the S1 window, and in none of P1/P2/P6.

### Not run / pending

- **Combat's fatal-window captures**: requested and then cancelled on 2026-10-30 before starting (rest day; nothing new to start).
  - Commands: `pesquisas-paralelas/combate/executar_janelas_fatais_combate.py S1 --intervals 11000-12250` and `D1 --intervals 11250-11750 15250-15700`, from a checkout of `main` ≥ `89575fa`.
  - Start snapshots, kept on the Mac mini: S1 from `.local/m3/passo2/S1/instantaneo-11000.pickle` (DGROUP equal to the S1 record at 11000; Combat's tool checks the whole state); D1 from `.local/m3/d1final/D1-b/instantaneo-*.pickle`.
- **Python comparison** of the S1 and D1 windows: AI/runtime runs it against these captures.
