"""M2.3 provider readiness matrix over every routine MONDE01 enters in frames 0..9,200.

Source: Core's coverage of the display reference to frame 9200 (run branch
``runs/core/coverage-9200``, commit 7193999, ``relatorios/cobertura-quadros-
exibicao-9200.json``; 215 routines with first/last frame and entry counts).
The per-routine owner, provider, validation and M2.3 exposure below are a
read-only reading of the committed fronts at main 99c0e4e (the chained
composition ``ia-runtime/composicao_encadeada_ia.provedores`` and the modules
it reaches) plus Combat's raid captures; nothing is executed or translated.
The script checks that the curated set equals the coverage set and writes
``M2_3_PRONTIDAO.json`` (and the routine table of ``M2_3_PRONTIDAO.md``).

    python3 -B pesquisas-paralelas/combate/prontidao_m2_3.py [--resumo <summary.json>]
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

AQUI = Path(__file__).resolve().parent
REPO = AQUI.parents[1]
COBERTURA = ('7193999', 'relatorios/cobertura-quadros-exibicao-9200.json')
JANELA_M22 = 128

# ------------------------------------------------------------------ validation references
M22 = 'M2.2 chained proof (ia-runtime validacao/m2-2-prova-128-quadros.json): display reference frames 0-128'
CORE_Q1 = 'Core frame-0/1 isolated calls (ferramentas/validar_chamadas_quadro_core.py, display v2 frames 0/1)'
CORE_RAID = 'Core evidencias/fundacoes-quadro/captura-incursao-core-v1.json (v1, counter forced to 9000, frame 9000 only)'
IA_RAID = 'AI-runtime evidencias/captura-incursao-ia.json (v1, counter forced to 9000, frame 9000 only)'
IA_Q1 = 'AI-runtime frame-0/1 entry captures (evidencias/captura-entradas-quadro1-ia-v2.json, captura-isolada-ia-quadro1.json)'
ECO_Q1 = 'Economy frame-0/1 captures (captura-quadro1-economia-exibicao.json, captura-consultas-economia-exibicao-v2.json)'
CMB_Q1 = 'Combat captura-isolada-combate-quadro1.json (frames 0/1)'
CMB_RAID = 'Combat captura-incursao-m2-3-original.json (v1, forced 9000, frame 9000)'
CMB_VIDA = 'Combat captura-vida-incursao-m2-3-original.json (v1, forced 9000-9100, every call isolated)'
CMB_SET = 'Combat captura-projectile-set-m2-3-original.json (v1, forced 9000, isolated; types 0x20 and 0x1f)'
CMB_NAT = 'Combat native suites on synthetic pools/records (RISING_EMULAR)'
GFX_RAID = 'Graphics evidencias/dominio-exibicao-incursao*.json (AffGame at a raid display state)'
MIS_Q1 = 'Missions frame-0/1 differentials (fim_missao, influencia_missao)'
CURSO = 'Combat percurso-incursao-m2-3-original.json (v1, forced 9000-12000, entries only)'

# ------------------------------------------------------------------ per-routine rows
# name: (owner, provider in the chained composition, chain status, validations, M2.3 exposure, gap or None)
# chain status: direct (key of provedores), nested (runs inside a direct provider's Python),
# display (inside AffGame/RestoreAll/MenuInit display roots: Graphics' logic-effect model, drawing not executed),
# boundary (declared, not executed), not-wired (a validated translation exists but the chain does not call it),
# none (no Python provider; the chain stops).
GRAFICOS = 'graficos efeitos_logicos_exibicao.desenhar_jogo + ia-runtime affgame_hud_ia (AffGame root)'
NADA = 'no new state: same calls as frames 0-128'
L = {}


def linha(nomes, dono, provedor, cadeia, validacao, exposicao, lacuna=None):
    for n in nomes.split():
        if n in L:
            raise ValueError(f'duplicate row {n}')
        L[n] = dict(owner=dono, provider=provedor, chain=cadeia, validated=list(validacao), m23_exposure=exposicao,
                    gap=lacuna)


# --- Graphics: display roots and everything drawn inside them
linha('AffGame', 'graphics', GRAFICOS, 'direct', [M22, GFX_RAID],
      'draws the monster unit and a live type-31/32 effect from 9000 on; Graphics raid-domain capture exists, '
      'its comparison with desenhar_jogo is Graphics\' to confirm',
      dict(kind='confirm', detail='desenhar_jogo/affgame_hud over the raid display state (monster unit, live effect '
                                  'projectile, minimap dot) and the display mask beyond frame 128'))
linha('RestoreAll', 'graphics', 'graficos efeitos_logicos_exibicao.restaurar_tudo', 'direct', [M22],
      'load_tail only', None)
for n in ('DDLockSurface DDUnlockSurface DDFlipPage FilledBox DeleteBank').split():
    linha(n, 'graphics', f'graficos efeitos_logicos_exibicao.{n.lower()} (MenuInit display calls)', 'direct', [M22],
          'load_tail and AffGame only', None)
linha('AffBatimentOmbre AffBatiments AffBloc AffChrono AffCompteurMatiere AffCorpsEngin AffCorpsEnginDecalage '
      'AffDrapeauAlliance AffEngin AffInfoAide AffMarche AffMiniMap AffSprite AffTerrain AffTrame AffVeget '
      'AffVegetTerrain AffVehiculeAtelier AffZoneIconeAction AffZoneInfo Box CopyBitmap32x32 OmbreBitmap32x32 '
      'PasteBitmap32x32 PasteBobCmp PasteOmbreCmp PastePlayerCmp MemOmbreCopy MemPlayerCopy GetNumBob '
      'MessageBoxAffiche RestaureClipping SaveCurrentClipping Cyclage CalculFrame DDSetPalette itoa utoa '
      'EstConstructionTerrain BatimentGetEtat BatimentGetModeEtat MemClose MemFree',
      'graphics', 'inside ' + GRAFICOS, 'display', [M22],
      'display only; AffEngin/AffSprite/AffMiniMap draw the raid unit from 9000', None)
linha('AffDeplaceEngin', 'graphics', 'inside ' + GRAFICOS, 'display', [M22, GFX_RAID],
      'first moving unit drawn: the raid unit walks from 9000 (frames 0-128 have no moving unit)',
      dict(kind='confirm', detail='moving-unit sprite path (AffDeplaceEngin) is display-only; confirm mask/logic '
                                  'effects with the raid display capture'))
linha('ProjectileTrierAffichage', 'graphics', 'inside ' + GRAFICOS, 'display', [M22, GFX_RAID],
      'sorts a live projectile for the first time (slot 0, type 31/32, 9000-9031)',
      dict(kind='confirm', detail='projectile display ordering with a live pool slot'))
linha('LoadPie', 'graphics', 'declared boundary (RestoreAll pictures)', 'boundary', [M22], 'load_tail only', None)

# --- Audio boundaries
linha('MCICD_Play MCICD_Manage PlaySnd_Manage', 'audio', 'declared boundary (CalculGame/ProgIteration)', 'boundary',
      [M22], NADA, None)

# --- AI-runtime: frame skeleton, dispatchers, input and the raid
linha('CalculGame', 'ai-runtime', 'quadro_calcul_game.calcular_quadro', 'direct', [M22], NADA, None)
linha('ProgIteration', 'ai-runtime', 'composicao_encadeada_ia.fase_entre_quadros_exibicao + Core '
      'fundacoes_quadro.avancar_contadores_iteracao', 'direct', [M22], NADA, None)
linha('CalculNextReflect iaCalculPlayer', 'ai-runtime', 'quadro_calcul_game.calcul_next_reflect', 'direct', [M22, IA_Q1],
      NADA, None)
linha('MessageBoxCalcul', 'ai-runtime', 'rotinas_quadro_ia.calcular_caixa_mensagens', 'direct', [M22, IA_Q1], NADA,
      None)
linha('ProcessInputGame', 'ai-runtime', 'rotinas_quadro_ia.processar_entrada', 'direct', [M22, IA_Q1], NADA, None)
linha('InputGame', 'ai-runtime', 'entrada_quadro_ia.entrada_jogo', 'direct', [M22, IA_Q1],
      'map hover sees the raid unit only if it enters the hovered cell (cursor stays at (0,0))', None)
linha('InputSend ReseauActif', 'ai-runtime', 'entrada_quadro_ia.enviar_entrada', 'direct', [M22],
      NADA, None)
linha('CalculIconeAction EnginGetNbSelection DesTroupesSelectionnes BatimentGetSelection', 'ai-runtime',
      'entrada_quadro_ia.calcular_icone_acao', 'direct', [M22, IA_Q1], NADA, None)
linha('MenuInit', 'ai-runtime', 'entrada_quadro_ia.iniciar_menu', 'direct', [M22], 'load_tail only', None)
linha('MouseZone ScrollTerrain NextGouttes TerrainEstGc TerrainEstMine TerrainEstPiege TerrainEstSac', 'ai-runtime',
      'entrada_quadro_ia (zona_mouse, rolar_terreno, proximas_gotas, pairar_mapa)', 'nested', [M22, IA_Q1], NADA,
      None)
linha('CalculEnginNextEtape IATestUtilite iabTestEngin iagMessTestSendMessageEngin', 'ai-runtime',
      'laco_despachantes.calcular_proxima_etapa_unidades', 'direct', [M22, IA_Q1],
      'the loop now includes units 16 (and 17 from 10800), owner 4', None)
linha('CalculBatimentNextEtape', 'ai-runtime', 'laco_despachantes.calcular_proxima_etapa_estruturas', 'direct',
      [M22, IA_Q1], 'structure step gate counter % 1000 fires at 1000..9000 (inside frames 0-128 only at 0)',
      dict(kind='confirm', detail='periodic counter-%1000 branch beyond frame 128 (M2.3a states, not raid)'))
linha('EnginNextEtape', 'ai-runtime', 'proxima_etapa_quadro.proxima_etapa_unidade', 'direct', [M22, IA_Q1],
      'the raid unit is in state 2 (moving) from 9000: the state switch target for state 2 is not translated '
      '(_trocar_estado raises "EnginNextEtape state 2"), and its reload/fatigue gates run for owner 4 type 0',
      dict(kind='missing-branch', detail='EnginNextEtape state-2 movement branch (0x456c1c table) calling DeplaceEngin '
                                         '@EnginNextEtape+0x1185; owner-4 type-0 prelude (reload gate, fatigue)'))
linha('BatimentNextEtape', 'ai-runtime', 'proxima_etapa_quadro.proxima_etapa_estrutura', 'direct', [M22, IA_Q1],
      'per-structure %50 gate and production branch beyond frame 128', None)
linha('AvanceMonstre', 'ai-runtime', 'incursao_ia.avancar_monstros (via rotinas_quadro_ia)', 'direct',
      [M22, IA_RAID, CMB_RAID],
      'raid frame 9000 validated (forced v1); 9001-9200 run the action loop over one 0x2f action and return '
      '(not captured, same code path)', None)
linha('ConstruitGroupeMonstre iaGroupNew iagUnitAddToGroup StockeAction', 'ai-runtime',
      'incursao_ia (construir_grupo_monstros, novo_grupo, adicionar_ao_grupo, guardar_acao)', 'nested',
      [IA_RAID, CURSO], 'frame 9000 only', None)
linha('iagUnitGetFirstUnitInGroup', 'ai-runtime', 'incursao_ia.primeira_unidade (AvanceMonstre path only)', 'nested',
      [IA_RAID], 'also called by the iaSolver kernels I_DetermineTempsTrajet and V_DeplaceGroupe at 9000, '
      'which have no provider', dict(kind='missing-provider', detail='kernel-side callers have no provider (see '
                                                                       'V_DeplaceGroupe, I_DetermineTempsTrajet)'))
linha('iagUnitGetNextUnitInGroup', 'ai-runtime', 'none', 'none', [CURSO],
      'iaSolver kernels I_DetermineTempsTrajet and V_DeplaceGroupe at 9000',
      dict(kind='missing-provider', detail='iagUnitGetNextUnitInGroup (group iterator, pairs with incursao_ia.'
                                           'primeira_unidade)'))
linha('B_TestGroupeVide B_AttenteConflit B_NewConflit I_DetermineTempsTrajet V_DeplaceGroupe iagWarNewBattleToPos '
      'iagWarSearchBattleFromPos iagWarSetWait', 'ai-runtime',
      'none: Core\'s MaquinaTarefasViva is built without operacoes/mundo, so executar_operacao raises '
      '"Operação de mundo ainda não reconstruída" (V_DeplaceGroupe: "Estado das unidades não fornecido")', 'none',
      [CURSO], 'iaSolver runs the posted 0x2f task for player 4 at 9000 (and re-plans at 9500, 9700, ...)',
      dict(kind='missing-provider', detail='iaSolver rule kernels of the monster battle task, wired as VM operations '
                                           'over the live memory'))
linha('B_Superieur', 'ai-runtime', 'ferramentas/tarefas_ia.MaquinaTarefas.executar_operacao (inline)', 'nested',
      [CURSO], 'first use at 9000 inside the battle task', dict(kind='unvalidated', detail='inline VM operation '
                                                                 'never compared at a raid state'))
linha('iaProbSleep', 'core', 'ferramentas/tarefas_ia.MaquinaTarefas.suspender', 'nested', [CURSO],
      'called by iagWarSetWait at 9000 (whose kernel has no provider)',
      dict(kind='unvalidated', detail='reached only through a missing kernel; compare once iagWarSetWait exists'))
linha('iaSolver', 'core', 'ferramentas/tarefas_ia.MaquinaTarefasViva.atualizar', 'direct', [M22],
      'frames 0-128 validate only empty/idle contexts; from 9000 player 4 has a live battle task',
      dict(kind='missing-branch', detail='live task execution with world operations (operacoes/mundo not supplied)'))
linha('iaProbPost', 'core', 'chain: tarefas_ia.MaquinaTarefasViva.postar; validated translation: '
      'incursao_core.postar_tarefa (not the one wired)', 'direct', [CORE_RAID],
      'frame 9000 (StockeAction 0x2f), 10800, 11101',
      dict(kind='not-wired', detail='the chain posts through the VM method, while the raid-validated provider is '
                                    'incursao_core.postar_tarefa; one of them must be wired and compared'))
linha('iaProbNew listNewElem listLinkElemToTail', 'core', 'nested in the iaProbPost provider '
      '(incursao_core.tarefa_nova / lista_novo_elemento / lista_ligar_ao_fim validated)', 'nested', [CORE_RAID],
      'frame 9000', dict(kind='not-wired', detail='follows iaProbPost'))

# --- Core: frame foundations and world queries (frames 0-128)
linha('GameNextFrame', 'core', 'quadro_calcul_game (inc [0x496d40]) / fundacoes_quadro.avancar_quadro_jogo', 'direct',
      [M22, CORE_Q1], NADA, None)
linha('SetClipping InitGameZone NextAnimTerrain NextAnimVeget', 'core',
      'chamadas_quadro_core (definir_recorte, iniciar_zonas_jogo, animar_terreno, animar_vegetacao)', 'direct',
      [M22, CORE_Q1], NADA, None)
linha('ChercheContacteur MouseSetZone MouseTestZone MiniMapGetPos MiniMapGetTaille MessageBoxExiste '
      'PlayerEstContacterPourAlliance', 'core', 'chamadas_quadro_core (nested in InitGameZone/InputGame)', 'nested',
      [M22, CORE_Q1], NADA, None)
linha('Random rand LongRand', 'core', 'chamadas_quadro_core (aleatorio_mundo_memoria, aleatorio_crt_memoria)',
      'direct', [M22, CORE_Q1, CORE_RAID, IA_RAID], 'raid draws at 9000 (effect type, target player, %100, field)',
      None)
linha('GetBit SetBit TerrainEstDecouvert TerrainEstIllumine ExisteEngin EnginGetPlayer EnginEstTerreur '
      'EnginEstMiroir EnginEstArmure TypeEnginSeFatigue CaseEstDecouverte CaseEstIlluminee BatimentGetCase '
      'BatimentEstDecouvert BatimentContourEstIllumine BatimentCollision SetCollision', 'core',
      'chamadas_quadro_core.provedores_core', 'direct', [M22, CORE_Q1], NADA, None)
linha('EnginGetType', 'core', 'chamadas_quadro_core.tipo_da_unidade', 'direct', [M22, CORE_Q1, IA_RAID],
      'new logic caller AvanceMonstre (pending branch) at 9000, monster unit type 0', None)
linha('SetEnginCollision Chemin_ModifieZone', 'core', 'chamadas_quadro_core (definir_colisao_unidade, '
      'modificar_zona_caminho)', 'direct', [M22, CORE_Q1, CORE_RAID],
      'raid unit placed (PlaceEngin, validated) and re-collided every frame while it moves (state-2 path, no '
      'provider upstream)', None)
linha('CalculFatigue', 'core', 'chamadas_quadro_core.calcular_fadiga', 'direct', [M22, CORE_Q1],
      'first owner-4 type-0 unit (the raid unit) from 9000',
      dict(kind='unvalidated', detail='fatigue for the monster unit; compare on the raid states'))
linha('memset __STOSB __STOSD', 'core', 'CRT helpers inline in their callers (reset_terreno/minimap in load_tail)',
      'nested', [M22], 'also inside CheminCalcul at 9177 (pathfinding scratch clear)',
      dict(kind='follows', detail='covered once CheminCalcul has a provider'))
linha('MissionGetNum', 'core', 'composicao_encadeada_ia (u8 0x496fe4) / chamadas_quadro_core.numero_missao', 'direct',
      [M22, IA_RAID], NADA, None)

# --- Core: raid spawn (translated and validated, not wired)
linha('GetFreeCell CreerEngin EnginSetType EnginSetTypeCaract EnginTypeGetCapacite EnginEnArret EnginSetPlayer '
      'PlaceEngin PlayerGetColor SetMiniMap EnginGetCase GetRandCaseChamps Chemin_Accessible', 'core',
      'incursao_core.ROTINAS (validated) - not in provedores_core, so the chain raises DependenciaIA at the '
      'incursao_ia call site', 'not-wired', [CORE_RAID, IA_RAID],
      'spawn and first order at 9000 (10800 for the second raid; Chemin_Accessible again at 11101 and inside '
      'Chemin_Verouille at 9177)',
      dict(kind='not-wired', detail='export incursao_core routines as chain providers (original-name signatures '
                                    'used by incursao_ia)'))
linha('EnginEstVivant', 'core', 'none in the chain (ordens_unidades.viva exists on Core\'s object world)', 'none',
      [CURSO], 'frame 9000 (raid order path)', dict(kind='missing-provider', detail='EnginEstVivant over the live '
                                                                                   'unit table'))

# --- Core: movement and pathfinding (state 2), all first entered in the raid
linha('SetDeplaceEngin ResetOrdre', 'core', 'none in the chain (ordens_unidades.definir_movimento / redefinir_ordem '
      'exist on Core\'s object world; Combat alvos_alcance.ordem_apos_reset covers ResetOrdre inside SetAttaqueEngin '
      'only)', 'none', [CURSO], 'V_DeplaceGroupe orders the raid unit at 9000 (re-orders at 9500, 9700, 10200, ...)',
      dict(kind='missing-provider', detail='SetDeplaceEngin/ResetOrdre over the live unit table'))
linha('DeplaceEngin AvanceEngin CalculNextCase CalculDirCase CalculDirection RotateEngin EnginNextCase '
      'EnginPeutPasser ResetCollision ResetEnginCollision TerrainEnCollision', 'core',
      'none in the chain (avanco_unidades / navegacao_unidades / movimento exist on Core\'s object world)', 'none',
      [CURSO], 'every frame the raid unit moves (9000 on)',
      dict(kind='missing-provider', detail='unit movement over the live memory, called from the EnginNextEtape '
                                           'state-2 branch'))
linha('ChercheIndiceEngin', 'core', 'entrada_quadro_ia.procurar_unidade (map hover only)', 'nested', [M22, IA_Q1],
      'new caller at 9176: the first path search (DeplaceEngin/pathfinding)', dict(
          kind='missing-provider', detail='pathfinding-side ChercheIndiceEngin use is not provided'))
linha('CheminCalcul Chemin_Verouille OptimiseChemin TestLigneOptimise EnginNextCaseChemin', 'core',
      'none in the chain (preparacao_destino / navegacao_unidades.escolher_da_rota exist on Core\'s object world)',
      'none', [CURSO], 'first path search at 9177, route following from 9179',
      dict(kind='missing-provider', detail='pathfinding (CheminCalcul and the route follower) over the live memory'))

# --- Economy
linha('BonusGetValEngin', 'economy', 'bonus_unidades.BonusUnidades.consultar', 'direct', [M22, ECO_Q1, CORE_RAID],
      'owner-4 type-0 unit (CreerEngin path validated by Core with this provider; EnginNextEtape reload gate for the '
      'raid unit is not)', None)
linha('CalculMatiere BCDToInt IntToBCD CalculCompteurMarche CalculCompteurProposition RechercheCalcul '
      'PlayerInitAllianceCompteur ResetTableauHangar', 'economy', 'quadro_economia', 'direct', [M22, ECO_Q1],
      'periodic gates beyond 128 (market %100, propositions %800, research) - M2.3a states, not raid', None)
linha('SetUpdateChamp UpdateChamp ScanNouvellePatate', 'economy',
      'quadro_economia.agendar_campos / atualizar_campos (extracao.propagar_planta)', 'direct', [M22, ECO_Q1],
      'second and later field sweeps (frames 256+) - M2.3a states, not raid', None)
linha('PlayerAttaqueCalculSympa MAJSympathie', 'economy',
      'quadro_economia.calcular_simpatia_ataques / atualizar_simpatia', 'direct', [M22, ECO_Q1, CMB_VIDA],
      'counter % 2000 fires at 2000..8000 (MAJSympathie x12 each); frames 0-128 cover only counter 0',
      dict(kind='confirm', detail='same inactive branch expected at counters 2000k; not compared beyond frame 0'))
linha('CalculTroupe BagContientTroupe BagVide BatimentEstHabiter BatimentExiste BatimentGetType BatimentGetPlayer '
      'TestRessource', 'economy', 'quadro_economia / producao / construcoes_habitaveis (production branch, '
      'TestFinDeMission queries; display callers inside AffGame)', 'nested', [M22, ECO_Q1], NADA, None)
linha('PlayerGetType', 'economy', 'mercado.tipo_jogador', 'direct', [M22, ECO_Q1, IA_RAID],
      'player 4 (constant 2) at the raid', None)

# --- Missions
linha('EvenementEnCours TestFinDeMission', 'missions', 'fim_missao (evento_em_curso, testar_fim_missao)', 'direct',
      [M22, MIS_Q1], NADA, None)

# --- Combat
linha('PlayerAttaqueReset', 'combat', 'quadro_calcul_game (one-byte RET, no effect)', 'direct',
      [M22, CMB_Q1, CMB_VIDA], NADA, None)
linha('ProjectileCalcul ProjectileAnim', 'combat', 'maquina_projeteis.MaquinaProjeteis.calcular (avanco_projeteis.'
      'animar_projetil)', 'direct', [M22, CMB_Q1, CMB_RAID, CMB_VIDA, CMB_NAT],
      'live type-32 effect 9000-9031, validated every frame 9000-9100 (forced v1)', None)
linha('ProjectileAvance', 'combat', 'maquina_projeteis.MaquinaProjeteis.avancar', 'nested',
      [CMB_RAID, CMB_VIDA, CMB_NAT], 'live effect 9000-9031 (slot order validated)', None)
linha('ProjectileInit', 'combat', 'projeteis.PoolProjeteis.iniciar', 'direct', [CMB_RAID, CMB_NAT],
      'spawn effect at 9000 (10800)', None)
linha('ProjectileSet', 'combat', 'projeteis.PoolProjeteis.definir (inside iniciar)', 'nested',
      [CMB_SET, CMB_RAID, CMB_NAT], 'spawn effect at 9000, types 0x20 and 0x1f validated at the raid entry', None)
linha('EnginTrouveCible EnginTrouveCibleScan Distance2d', 'combat', 'alvos_alcance.encontrar_alvo '
      '(encontrar_alvo_scan, distancia2)', 'direct', [M22, CMB_Q1, CMB_VIDA],
      'raid unit (owner 4, type 0) queries at 9008+32k and unit 15 scans at 9009+32k, all validated 9000-9100; no '
      'target through 12000', None)
linha('PlayerEstAllie', 'combat', 'alvos_alcance.aliados (+ register contract)', 'nested', [M22, CMB_Q1, CMB_VIDA],
      'owner-4 queries inside the raid unit\'s target query, validated 9000-9100', None)
linha('EnginOccupeCase', 'combat', 'alvos_alcance.ocupa_celula', 'direct', [M22, IA_Q1],
      'called by EnginNextCase/pathfinding for the moving raid unit (9000 on), whose callers have no provider',
      dict(kind='follows', detail='Combat provider exists; raid-state comparison needs the movement callers'))


def construir(d):
    rotinas = d['routines']
    if set(rotinas) != set(L):
        raise SystemExit(f'Curated rows differ from coverage: missing {sorted(set(rotinas) - set(L))}, '
                         f'extra {sorted(set(L) - set(rotinas))}')
    saida = []
    for nome in sorted(rotinas, key=lambda n: (rotinas[n]['first_frame'], n)):
        r = dict(routine=nome, **rotinas[nome], **L[nome])
        r['beyond_m22_window'] = r['last_frame'] > JANELA_M22
        r['new_in_raid'] = r['first_frame'] > JANELA_M22
        saida.append(r)
    lacunas = {}
    for r in saida:
        if r['gap']:
            lacunas.setdefault(r['owner'], []).append(dict(routine=r['routine'], first_frame=r['first_frame'], **r['gap']))
    return saida, lacunas


CABECALHO = """# M2.3 provider readiness (Combat, read-only)

Every routine MONDE01 enters in frames 0–9,200, with its owner, the Python provider the chained composition would call, the captures that validate it, and whether the M2.3 raid path takes it outside those captures. Generated by [`prontidao_m2_3.py`](prontidao_m2_3.py) (data: [`M2_3_PRONTIDAO.json`](M2_3_PRONTIDAO.json)).

**Sources**
- Coverage: Core's display-reference run to frame 9200, from branch `runs/core/coverage-9200` at commit `7193999` (`relatorios/cobertura-quadros-exibicao-9200.json`, SHA-256 `{sha}`). It lists {n} routines, {novas} of them first entered at 9000–9179, during the raid.
- Code: main `99c0e4e`. The chain is `ia-runtime/composicao_encadeada_ia.provedores`, plus the modules it reaches. This is a static reading; nothing was executed for the matrix.
- Combat's raid captures, all on the v1 bench with the counter forced to 9000: `captura-incursao-m2-3-original.json`, `captura-vida-incursao-m2-3-original.json` (frames 9000–9100, every call isolated), `percurso-incursao-m2-3-original.json` (entries through 12000) and `captura-projectile-set-m2-3-original.json`.

**Chain status:** {contagem}.
- **direct:** a key of `provedores`.
- **nested:** runs inside a direct provider's Python.
- **display:** runs inside a display root, which Python models only by its logic effects.
- **boundary:** a declared, non-executed boundary.
- **not-wired:** a validated translation exists, but the chain does not call it.
- **none:** no provider; the chain stops at the original call site.

## Findings

1. **The raid unit cannot move in Python.** From 9000 the unit is in state 2 (moving). `proxima_etapa_quadro._trocar_estado` stops at the state-2 branch, and nothing in the chain provides the movement and pathfinding it calls: `DeplaceEngin`, `AvanceEngin`, `CalculNextCase`, the collision reset, and `CheminCalcul`/`OptimiseChemin`/`EnginNextCaseChemin`. Core has movement and pathfinding modules on its own world object (`avanco_unidades`, `navegacao_unidades`, `ordens_unidades`), but none of them runs over the live memory the chain uses.
2. **The monster battle task cannot run.** `MaquinaTarefasViva` is built without `operacoes`/`mundo`. The kernels the posted 0x2f task runs at 9000 therefore raise inside iaSolver: `B_TestGroupeVide`, `B_AttenteConflit`, `B_NewConflit`, `I_DetermineTempsTrajet`, `V_DeplaceGroupe` → `SetDeplaceEngin`/`ResetOrdre`, `iagWarNewBattleToPos`/`SearchBattleFromPos`/`SetWait`, and `iagUnitGetNextUnitInGroup`.
3. **The spawn's Core providers are validated but not wired.** `incursao_core.ROTINAS` (`GetFreeCell`, `CreerEngin` and its `EnginSetType*` helpers, `EnginSetPlayer`, `PlaceEngin`, `SetMiniMap`, `PlayerGetColor`, `EnginGetCase`, `GetRandCaseChamps`, `Chemin_Accessible`) is not exported by `provedores_core`, so `incursao_ia` would raise `DependenciaIA` at its call sites. The chain's `iaProbPost` is the VM's `postar`, not the raid-validated `incursao_core.postar_tarefa`.
4. **Combat's providers are ready for the reached states.** `ProjectileInit`/`ProjectileSet` (both effect types at the raid entry), `ProjectileCalcul`/`Anim`/`Avance` over the live effect, `EnginTrouveCible`/`Scan`/`Distance2d` and `PlayerEstAllie` are equal on every isolated call from 9000 to 9100. Neither raid reaches attack, damage or death before 12000. Combat's only open row is `EnginOccupeCase`: the provider exists, but its raid-time callers are the missing movement routines.
5. **To confirm outside the raid (M2.3a states, frames 129–8999):** the periodic gates the 128-frame proof never fired. These are the structure step at counter % 1000, sympathy at % 2000 (`MAJSympathie` ×12), propositions at % 800, and the later field sweeps. On the display side, Graphics should confirm the raid display state: a moving monster, a live effect projectile and the display mask beyond frame 128.

## Gaps by owner
"""


def markdown(r):
    contagem = ', '.join(f'{k} {v}' for k, v in r['chain_status_counts'].items())
    texto = [CABECALHO.format(sha=r['coverage']['sha256'], n=r['coverage']['routines'], novas=r['new_in_raid'],
                              contagem=contagem)]
    for dono, itens in r['gaps_by_owner'].items():
        texto.append(f'\n### {dono} ({len(itens)})\n')
        for g in itens:
            texto.append(f"- `{g['routine']}` (first frame {g['first_frame']}): **{g['kind']}**. {g['detail']}")
    texto.append('\n## All routines\n')
    texto.append('| Routine | First | Last | Entries | Owner | Chain | Provider | Validated by | M2.3 exposure |')
    texto.append('|---|---|---|---|---|---|---|---|---|')
    for x in r['routines']:
        valid = '; '.join(v.split(' (')[0] for v in x['validated']) or '-'
        celulas = [f"`{x['routine']}`", str(x['first_frame']), str(x['last_frame']), str(x['entries']), x['owner'],
                   x['chain'] + (' ⚠' if x['gap'] else ''), x['provider'], valid, x['m23_exposure']]
        texto.append('| ' + ' | '.join(c.replace('|', '/') for c in celulas) + ' |')
    return '\n'.join(texto) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--resumo', help='coverage summary JSON (default: git show of the coverage commit)')
    args = ap.parse_args()
    bruto = Path(args.resumo).read_bytes() if args.resumo else subprocess.check_output(
        ['git', 'show', f'{COBERTURA[0]}:{COBERTURA[1]}'], cwd=REPO)
    d = json.loads(bruto)
    linhas, lacunas = construir(d)
    contagem = {}
    for r in linhas:
        contagem[r['chain']] = contagem.get(r['chain'], 0) + 1
    relatorio = dict(
        schema='rising-lands/m2-3-provider-readiness/1', main='99c0e4e',
        coverage=dict(commit=COBERTURA[0], path=COBERTURA[1], sha256=hashlib.sha256(bruto).hexdigest(),
                      frames_run=d['frames_run'], routines=len(d['routines']), scenario=d['scenario']),
        m22_window=[0, JANELA_M22], chain_status_counts=dict(sorted(contagem.items())),
        new_in_raid=sum(r['new_in_raid'] for r in linhas),
        gaps_by_owner={k: v for k, v in sorted(lacunas.items())}, routines=linhas)
    (AQUI / 'M2_3_PRONTIDAO.json').write_text(json.dumps(relatorio, indent=1, ensure_ascii=False) + '\n')
    (AQUI / 'M2_3_PRONTIDAO.md').write_text(markdown(relatorio))
    print(json.dumps(dict(chain=relatorio['chain_status_counts'], new_in_raid=relatorio['new_in_raid'],
                          gaps={k: len(v) for k, v in lacunas.items()})))


if __name__ == '__main__':
    main()
