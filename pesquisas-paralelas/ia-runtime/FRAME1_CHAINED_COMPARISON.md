# M2.1 round 3 — chained Python composition of MONDE01 frames 0 and 1 versus the original

Main `67fb81f`. Intact `RISING.EXE` SHA-256 `6c556520…43fb`. Original reference: Missions' first-frame capture `captura-quadro1-monde01-original.json` (`c06f78ea…`, source `e6aa305`). Report: [validacao/m2-quadro1-encadeado-ia.json](validacao/m2-quadro1-encadeado-ia.json), produced by [comparar_quadro1_encadeado_ia.py](comparar_quadro1_encadeado_ia.py) from a clean source revision with a fresh native collection. M2 acceptance is the coordinator's decision.

## Result: all three phases equal, chained from Python

| Phase | Python input | Result |
|---|---|---|
| (a) `load_tail` | the map built from the accepted M1 post-load state | **equal**: all 881 blocks, RNGs `0x497164` = `0x1c019f87` and `0x498db4` unchanged, 13/13 bindings, 16/16 boundaries; 43/43 checkpoints equal |
| (b) `between_frames` | Python's (a) output | **equal**: all blocks, RNGs, 2/2 bindings, 3/3 boundaries, and registers EAX/EBX/ECX/EDX/ESI/EDI/EBP/ESP |
| (c) `frame1` | Python's (b) output | **equal**: all blocks, RNG `0x497164` = `0x78fe3b37`, 13/13 bindings, 1/1 boundary; 38/38 checkpoints equal |

One `MapaMemoriaM1` carries the state through all three phases, and nothing restarts from an original state. The only original data applied is the effect of each declared stop below, and only after an exact entry-state match.

**Not modeled.** Boundary stack words that lie in uninitialized caller locals (bench stack bytes): DDLockSurface (4 words) and FilledBox (words 3–4) in MenuInit, and MCICD_Play in both CalculGame frame bodies (4 words). Every other recorded field matches. EFLAGS/EIP are not modeled. Phase (b)'s caller frame, cursor and PeekMessageA answer are the capture's declared inputs.

## Declared stops crossed (reported)

| Phase | Routine (owner) | Original effect applied |
|---|---|---|
| (a) | RestoreAll (graphics: the oracle is being extended to execute it) | state + 9 DirectDraw/LoadPie/DDSetPalette boundary events |
| (a) | SetClipping (core, pending) | state |
| (a) | InitGameZone ×2: inside MenuInit at `0x468484`, and from CalculGame at `0x42d2d9` (core, pending) | state (mouse zones `0x5099b4…`) |
| (a), (c) | NextAnimTerrain, NextAnimVeget (core, pending) | state |

Before each crossing the Python state equalled the original state at that call's entry, in all blocks. A divergence there would have stopped the phase instead.

## Providers composed (integrated)

- **This front** (new this round, original-first): InputGame with MouseZone, ScrollTerrain (the cursor-(0, 0) edge scroll of `0x508720/22`) and NextGouttes; InputSend; CalculIconeAction; MenuInit (load-tail path); the EnginNextEtape prelude and state switch; the BatimentNextEtape type switch. Also, from earlier rounds: the frame skeleton, the dispatcher loops, CalculNextReflect, AvanceMonstre, iaSolver (Core `MaquinaTarefas` via `PonteTarefas`), ProcessInputGame and MessageBoxCalcul.
- **Core** `chamadas_quadro_core`: GetBit, CalculFatigue, SetEnginCollision (SetCollision, Chemin_ModifieZone), BatimentGetCase, CaseEstDecouverte/Illuminee, BatimentEstDecouvert and BatimentContourEstIllumine. Also `fundacoes_quadro` (the load counter reset).
- **Economy:** `BonusUnidades.consultar`, the state-7 body, the type-2 production branch (`ramo_producao_estrutura` + `Producao.calcular_tropa`), ResetTableauHangar, RechercheCalcul, PlayerInitAllianceCompteur, SetUpdateChamp/UpdateChamp (`RecursosTerreno`), CalculMatiere, CalculCompteurMarche/Proposition, PlayerAttaqueCalculSympa with MAJSympathie, and `Mercado.tipo_jogador`.
- **Combat:** `MaquinaProjeteis.calcular` (ProjectileCalcul), and `alvos_alcance.encontrar_alvo`/`aliados` (EnginTrouveCible in frame 0, PlayerEstAllie).
- **Missions:** `fim_missao.testar_fim_missao` with `consultas_publicadas` and the influence queries; `evento_em_curso`.

## Original-first evidence for this round's routines

1. [evidencias/captura-entradas-quadro1-ia.json](evidencias/captura-entradas-quadro1-ia.json) (`f60137a`) and [-v2](evidencias/captura-entradas-quadro1-ia-v2.json) (`4e10cdd`, adds the nested executed blocks), both committed before translation. They pause at the entry and the return of every MenuInit, InputGame, InputSend, CalculIconeAction and EnginNextEtape call (32) on Missions' committed path, reproduced exactly. They record registers, changed bytes, bindings, boundaries and every executed basic block.
2. The translations ([entrada_quadro_ia.py](entrada_quadro_ia.py), [proxima_etapa_quadro.py](proxima_etapa_quadro.py)) follow exactly the executed blocks. Every untaken branch raises `DependenciaIA` at its original address.
3. Native differential: the chained comparison above, whose checkpoints sit at each of these calls.

## Composition notes and requests

- [memoria_composicao_ia.py](memoria_composicao_ia.py) serves u8/u16/u32 over the map, including Core's list-backed u16 grids (tiles, regions), which Core's providers address as memory.
- **Economy/Core:** `RecursosTerreno.mosaicos` expects the tile grid `[0x507d70]` as bytes, while the M1 map keeps it as Core's u16 list. UpdateChamp does not read it at frames 0/1, and any access is a named stop. A shared contract is needed before the first field-growth frame (counter 128).
- **Core:** a live-memory binding of the task pool `0x512320..0x514908` in `tarefas_ia` (requested by the coordinator) would retire `PonteTarefas`. SetClipping, InitGameZone and NextAnim* will replace their crossings when integrated.
- **Graphics/Missions:** when the oracle executes RestoreAll and AffGame natively, the RestoreAll crossing becomes a provider. AffGame then joins phase (b), which still records it as a boundary.
