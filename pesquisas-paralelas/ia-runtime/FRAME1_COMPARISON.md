# M2.1 comparison — Python composition of MONDE01 phases (a)/(b)/(c) versus the original

Intact `RISING.EXE` SHA-256 `6c556520…43fb`. Original reference: Missions' first-frame capture `pesquisas-paralelas/missoes/evidencias/captura-quadro1-monde01-original.json` (SHA-256 `c06f78ea…fed8`, source `e6aa305`), at main `ec931d2`. Report: [validacao/m2-quadro1-composicao-ia.json](validacao/m2-quadro1-composicao-ia.json), produced by [comparar_quadro1_ia.py](comparar_quadro1_ia.py) from a clean source revision. M2 is **not** accepted by this report.

## Method

- **Memory.** The memory is Missions' `MapaMemoriaM1` plus `montar_provedores`, used by import. It is built from the original state at each phase entry:
  - S0, the accepted M1 post-load state `58a5020e…`, for (a). Its bytes equal the Stage14 strict composition output.
  - The captured state after the previous phase, reconstructed from the capture's per-phase changed blocks and checked against all 881 block hashes, for (b) and (c).
- **Providers.** The composition ([composicao_quadro1_ia.py](composicao_quadro1_ia.py)) calls only integrated providers, in original order:
  - this front's skeleton and loops, CalculNextReflect, AvanceMonstre, MessageBoxCalcul and ProcessInputGame;
  - Core `fundacoes_quadro` and `tarefas_ia`;
  - Economy `Mercado.tipo_jogador`;
  - Missions `fim_missao.evento_em_curso`.

  Any other routine raises `DependenciaIA` at its original CALL, after every earlier effect.
- **Boundaries.** The original capture's declared non-executed boundaries (AffGame, PlaySnd_Manage, MCICD_Manage, MCICD_Play) are recorded with the same fields and stepped over. **AffGame remains a declared open item**: graphics is proving its write set.
- **Windows answers.** They are the capture's named inputs: PeekMessageA 0, GetCursorPos (0, 0), SetCursorPos 1.
- **Comparison when a phase completes.** The whole state (881 blocks), both RNGs, the modeled registers, the ordered bindings (name, arguments, caller return, results, memory writes) and the boundary events (all recorded fields).
- **Comparison when a phase stops.** The same native replay of Missions' committed path pauses at the stopping routine's entry ([bancada_quadro1_ia.py](bancada_quadro1_ia.py)). The Python state and the binding/boundary prefix are compared with the original at that exact point. The replay itself reproduces every committed phase state, the entry trace and the boundaries.

## Result per phase

| Phase | Start | Result | Comparison |
|---|---|---|---|
| (a) `load_tail` | S0 | **stops at `RestoreAll`, CALL `0x42d27f`** (the first call after `jmp 0x42d27f`) | At the stop, the Python state equals the original state at RestoreAll's entry (all blocks). Bindings 0 = 0, boundaries 0 = 0 |
| (b) `between_frames` | captured state after (a), the capture's declared caller frame | **complete: full equality** | State: all 881 blocks equal (only `0x508f7c` changes). RNG `0x497164` = `0x1c019f87`, `0x498db4` = `0x3212b7ce`. Registers at the CalculGame entry equal for EAX/EBX/ECX/EDX/ESI/EDI/EBP/ESP (0, 3, 0, `0x2008004`, 0, 0, 0, `0x2008000`). Bindings PeekMessageA and GetCursorPos equal, including the POINT memory write. Boundaries AffGame, PlaySnd_Manage and MCICD_Manage equal in every field, including stack words and guards. EFLAGS/EIP are not modeled |
| (c) `frame1` | captured state after (b) | **stops at `InputGame`, CALL `0x42d33b`** (player 0, type 1, local) | At the stop, the Python state equals the original state at InputGame's entry (all blocks), after the prologue stores (`0x49a010`), the MCICD track index `0x4e1d18`, PlayerAttaqueReset, EvenementEnCours and PlayerGetType(0). The SetCursorPos(0, 0) binding is equal. The MCICD_Play boundary is equal in routine, caller, registers EAX/EDX/EBX/ECX = 3/0/3/2, cleanup and guards. Its four stack words are CalculGame locals (bench stack bytes) and are reported as not modeled |

Chained mode (b) after Python (a) is not applicable, because (a) stops. (b) and (c) were therefore composed from the original entry states.

## First stops and their owners

1. **(a) `RestoreAll 0x474b08`** (CALL `0x42d27f`): display/UI. It runs `AffTerrain` natively between DDLockSurface/LoadPie/DDUnlockSurface/DDFlipPage/DDSetPalette boundaries. **No owner or provider yet.** The rest of (a) needs, in order: `SetClipping 0x40f519` (UI), `MenuInit 0x4682bb` (UI, with the ShowCursor binding and display boundaries), and `InitGameZone 0x471830` (UI: MouseSetZone, MiniMapGetPos/Taille, ChercheContacteur, MessageBoxExiste, PlayerEstContacterPourAlliance, MouseTestZone). Then frame 0 follows: the same body as frame 1, plus EnginTrouveCible, PlayerEstAllie and MAJSympathie.
2. **(c) `InputGame 0x429278`** (CALL `0x42d33b`): input. It reads 12 GetAsyncKeyState bindings and runs MouseZone, ScrollTerrain and NextGouttes. With the declared cursor (0, 0) it **edge-scrolls the view `0x508720/22`**, which NextAnimTerrain/NextAnimVeget then consume. Stage 1 labelled input "ai-runtime (second wave)". **The coordinator must confirm that this front owns InputGame for M2.1.** If it does, it is the next original-first piece. `InputSend 0x45ec9f` (→ ReseauActif) follows.

## Frame-body providers after InputGame (static status, not yet reachable in the composition)

| Callee (CALL) | Owner | Integrated Python | In this composition |
|---|---|---|---|
| MissionGetNum `0x42d354`, CalculNextReflect `0x42d35d` | missions, ai-runtime | byte `0x496fe4`; this front + Core `ia.atualizar_ia` | wired; natively equal in isolation (below) |
| ProcessInputGame `0x42d3b0`, MessageBoxCalcul `0x42d3e1`, GameNextFrame `0x42d3e6` | ai-runtime | this front | wired; natively equal in isolation |
| CalculIconeAction `0x42d3eb` | interface | — | named stop |
| ProjectileCalcul `0x42d3f0` | combat | `maquina_projeteis.MaquinaProjeteis.calcular` | not wired yet (pool adapter over `[0x5080f0]`) |
| CalculEnginNextEtape `0x42d3f5` | ai-runtime | loop: this front | wired; the per-unit `EnginNextEtape 0x45442c` is a named stop at `0x456ead` (prelude: this front; state 7: Economy `estado_parado_unidade`; leaves: Core GetBit, CalculFatigue, SetEnginCollision, Random; Economy BonusGetValEngin; Combat EnginTrouveCible in frame 0) |
| CalculBatimentNextEtape `0x42d3fa` | ai-runtime | loop: this front | wired; stops at `ResetTableauHangar` `0x4281d0` (Economy, in progress), then BatimentNextEtape type 2 (Economy), BatimentGetCase, CaseEstDecouverte, BatimentEstDecouvert, BatimentContourEstIllumine (Core/Economy) |
| RechercheCalcul … CalculCompteurProposition `0x42d3ff..0x42d42d`, PlayerAttaqueCalculSympa `0x42d46c` | economy | `quadro_economia` (calcular_pesquisa, contar_aliancas, agendar_campos/atualizar_campos, calcular_materia, calcular_contador_mercado/proposicao, calcular_simpatia_ataques) | not wired yet |
| NextAnimTerrain `0x42d441`, NextAnimVeget `0x42d467` | graphics (per Core's inventory) | — | named stop |
| TestFinDeMission `0x42d481` | missions | `fim_missao.testar_fim_missao` | not wired yet |

"Not wired yet" means the provider exists but cannot be reached and compared while the composition stops at InputGame. It is wired when the composition reaches it, so that the first execution is already compared.

## This front's routines at the exact frame-0/1 inputs (original-first)

1. **Capture first.** Committed before any translation (`3b4d227`): [evidencias/captura-isolada-ia-quadro1.json](evidencias/captura-isolada-ia-quadro1.json), produced by [capturar_isolados_ia_quadro1.py](capturar_isolados_ia_quadro1.py). It holds 24 isolated native calls on Missions' committed path, which is reproduced exactly: CalculNextReflect ×4, ProcessInputGame ×4, MessageBoxCalcul, GameNextFrame and both dispatcher loops, in frame 0 and frame 1. It also holds snapshot pauses at RestoreAll and InputGame.
2. **Translation.** [rotinas_quadro_ia.py](rotinas_quadro_ia.py):
   - MessageBoxCalcul, the whole routine;
   - ProcessInputGame, the no-command path (command word 0 or above 0x27 → `0x45f2de`);
   - AvanceMonstre, the reached branches. Unreached branches raise at `0x47b2d3`, `0x47b349`, `0x47b3ad` and `0x47b44c`;
   - iaSolver, through Core `MaquinaTarefas.atualizar` with a live-memory load/store bridge (`PonteTarefas`). Only the empty-context path is validated.
3. **Native differential.** Python runs on a copy of each exact entry state. **22/24 equal** in changed bytes and returns:
   - CalculNextReflect ×8, including player 4: AvanceMonstre stores `0x50a9cc` = 1 in frame 0, and iaSolver returns `0x1a1a000e`.
   - ProcessInputGame ×8 (10 bytes cleared per player in frame 0, zeros rewritten in frame 1).
   - MessageBoxCalcul ×2 and GameNextFrame ×2.
   - The CalculEnginNextEtape loop-owned bytes ×2: counters and unit `+0x10a/+0x10b`, 27 bytes in frame 0, with EnginNextEtape as a declared recording stub.
   - The two CalculBatimentNextEtape cases stop at the Economy/Core per-structure providers.
4. **Local regression.** [testes/test_rotinas_quadro_ia.py](testes/test_rotinas_quadro_ia.py) replays the isolated captures on a sparse memory that holds only the bytes the original read. That exposed eager AI-counter reads in CalculNextReflect, which now reads only where the original does.

## Requests

- **Coordinator:** confirm the owner of InputGame/InputSend (input) and of RestoreAll/SetClipping/MenuInit/InitGameZone (UI). Until then they are named stops.
- **Missions:** nothing is required from the Missions-owned files. `MapaMemoriaM1`/`montar_provedores` worked unchanged by import, and `memoria_declarada` was enough.
- **Core:** `tarefas_ia.MaquinaTarefas` keeps a private copy of the task pool and list headers. A native live-memory binding of `0x512320..0x514908` would let this front drop `PonteTarefas`.
- **Graphics:** the AffGame write set (open item), and NextAnimTerrain/NextAnimVeget.
