"""S1 coverage survey: every original routine the S1 victory capture reaches, with owner and status.

Read-only. Nothing is executed under Unicorn and nothing is translated. Sources:

* **S1 capture** (Missions, feat/re-missions ``82ec5ea``, ``pesquisas-paralelas/missoes/m3/sondas/S1/``):
  ``quadros.jsonl.xz`` gives per-frame symbol entry counts (one block hook over the code section, the
  coverage method of ``cobrir_quadros_exibicao.py``) and every routine's first entry with its caller;
  ``fronteiras.jsonl.xz`` the declared boundary calls. The files are read from the git object (or from
  ``--captura DIR``) and the decompressed SHA-256 values are checked against ``replay.json``.
* **Static caller sets**: every ``call``/``jmp rel32`` in RISING.EXE's code section whose target is a
  symbol start, restricted to routines S1 also reaches. A routine whose reached callers all lie under
  ``AffGame`` is *display-only* (fixed point from ``AffGame``).
* **Chain proofs on main**: the M2.3 9,200-frame proof (no input; routines from Core's coverage run,
  ``runs/core/coverage-9200`` ``7193999``) and the M3.1 P1/P2 window proofs (routines from the P1/P2
  probe captures on main, inside the proven frame ranges).
* **Isolated native differentials on main**: per-routine comparisons extracted from every native report
  (file name with ``emulad``/``nativ``/``native``/``x86``, not ``local``) of every front.

Status is routine-level, not branch-level: a routine proven on one state may still take an unproven
branch in S1. Those branches are found by the per-segment chain proofs that follow S1.

    python3 -B ferramentas/cobertura_s1.py [--captura DIR] [--saida relatorios/cobertura-s1.json]
"""
import argparse
import bisect
import collections
import hashlib
import io
import json
import lzma
import re
import struct
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
EXE = RAIZ.parent.parent / 'source/cd/INSTALHD/RISING.EXE'
SIMBOLOS = RAIZ / 'relatorios/simbolos-originais.tsv'
CODIGO = (0x401000, 0x493c00)
S1_REV = '82ec5eaa98d4f212b650c2c8ce2b293a30fb50ef'
S1_DIR = 'pesquisas-paralelas/missoes/m3/sondas/S1'
COB9200 = ('71939991cb06e9d23c059e1d422830ba996d2f23', 'relatorios/cobertura-quadros-exibicao-9200.json')
PROVA_9200 = 'pesquisas-paralelas/ia-runtime/validacao/m2-3-prova-9200-quadros.json'
PROVA_M31 = 'pesquisas-paralelas/ia-runtime/validacao/m3-1-prova-p1-p2.json'
FRENTES = ('core', 'economy', 'ai-runtime', 'combat', 'graphics', 'missions', 'audio')

# ------------------------------------------------------------------ owners
# Owner = the front that owns the routine's translation. Rows are a reading of main (who translated it,
# or whose domain the call sites are in); see docs/core/S1_COVERAGE.md. Display-only routines not listed
# here go to Graphics automatically. Platform routines (WndProc) are AI/runtime's translation per M3_PLAN.
DONOS = {
    'core': '''
        SelectionEngin RetireSelectionEngin DeselectionEngin DeSelectionGroupe
        EnginInZone EnginVisible EnginGetEtat EnginEstSelectionne EnginGetSelection EnginSelectEstBlesse
        EnginSelectPeutDeposer EnginSelectPeutAttaquer EnginTypeSelectionne EnginTravailSelectionne
        EnginSelectEstTroupe EnginSelectEstEngin EnginSelectContientMiroir EnginSelectPeuventTransporter
        EnginSelectPeutEntrer BatimentSelection BatimentDeselectionner SetDeplaceEnginSelect SetConstruitBatimentSelect
        SetEnginConstruitBatiment SetRecolteEnginSelect SetRecolteEngin SetEnginRentreBatiment
        SetEnginSelectRentreBatiment SetSortEngin EnginRestaureEtat EnginAsk VoixOffAsk EnginGetVolume
        BatimentGetVolume TypeEnginEstEnLoop TypeEnginEstAerien TypeEnginEstArmee TypeEnginEstTroupe
        TypeEnginEstVehicule TypeEnginEstEngin TypeEnginPeutEcraser EnginEstBlesse EnginGetVieMax
        BagInit BagReset BagContient BagGetCode BagGetType BagRetire BagPrend BagAccepte BagGetNbContenu EnginGetBag
        EnginGetBagOrdre BatimentGetBagOrdre PlaceLibre BatimentAdjacent BatimentGetCaseAdjacent GetCaseCentrale
        CalculEntreBatiment RetireEngin AnimWorkEngin BatimentRetireColon BatimentEnleveUnColon
        RechercheDecalageSortie CalculPosition BatimentIllumine BatimentModifyMap BatimentModifyTerrain PlaceBatiment
        BatimentConstructible BatimentPosable BatimentTailleGet BatimentGetDecalageConstruction Remplit MurAjoute
        SetTerrain TerrainEstHerbe TerrainEstObstacleNaturel TerrainEstMontagne TerrainGetColor
        DecouvreCase DecouvreTerrain IllumineCase EteintCase IllumineTerrain EteintTerrain Distance
        ChercheVeget ChercheVegetLibre ChercheGc ChercheGcLibre ChercheBatimentProximiteCaveOuSanctuaire
        ChercheCaseBatiment ChercheIndiceBatiment EnginSetFatigue EnginResetFatigue IsDirectlyBlocking
        IsIndirectlyBlocking MiniMapGetCase MiniMapGetCenterSelect GetCaseIndiceBatiment GetNumIndiceTypeBatiment
        GetRandCaseTypeBatPlayer listDeleteElem listUnlinkElem iaProbReturnTo
    ''',
    'economy': '''
        BatimentGetColons BatimentGetCapacite BatimentGetDegatEffectif BatimentGetRessource BatimentEstOccupe
        BatimentEstDepot BatimentConstruit BatimentConstruction CreerBatiment InitBatimentPlayer BatimentHabitable
        BatimentLogeEngin BatimentSetTechnologie BatimentInitTechnologie BatimentAjouteMatiere TuyauEstSortie
        CalculConstruireBatiment AnimConstruireBatiment CalculWorkEngin TerrainRecolte TerrainRetireMatiere
        MineEstSurTerrain MineGetIndice MineSetWork MineEndWork MineGetCapacite MineRecolte SacGetCapacite
        TerrainGetSacType SetDepotEngin SetDepotEnginSelect SetMineEngin SetMineEnginSelect SortieTroupe
        EnginEnRecrutement GetStatusRecrute CalculStatusRecrute InitRecruteTroupe EnginGetTimeRecrute
        EnginGetRessource EnginSetExperimente GetRessourceStock AjouteMatiere EnleveMatiere __CHP
        TypeBatimentEstRealisable SetBatimentRecrutable TypeEnginEstRealisable SetTroupeRecrutable
        EnginSetTechnologie BonusReset TechnologieReset SortilegeResetTechnologie RechercheGetNbInvention
        InventionGetCout InventionSetEffet RechercheCalculNew RechercheGetEtat RechercheGetBranche
        RechercheGetNiveau IaRechercheAjuste
    ''',
    'combat': '''
        SetAttaqueEngin CalculAttaqueEngin AnimAttaqueEngin EnginLigneDeTir AngleCalcul IF@DACOS IF@DATAN2 __@DSQRT
        TypeEnginGetSortieProjectile InfligeDegat EnginInfligeDegat BatimentInfligeDegat SetDyingEngin
        EnginSetLevelExperience ChercheIndiceEnginCible ChercheTypeEnginProximite EnginAdjacent EnginAPortee
        EnginEstEnnemi BatimentEstEnnemi BatimentPeutAttaquer BatimentEnDestruction EnginGetDegat EnginAddVie
        PlayerAAttaqueSet PlayerResetAllie ProjectileLineaire ProjectileCalculLineaire ProjectileInfligeDegat
    ''',
    'ai-runtime': '''
        WndProc SetDebug SetPlayerOrdre IconeGetZone IconeFillContenu MessageBoxSet
        V_iaMonstreAttendLaReponseVachementCoolMemeQueJeLaVeux V_FreeConflit B_EtatBatiment I_DonneBatimentSurCase
        B_Egalite I_Soustraction V_LibereGroupeVide V_AttaquerBatiment I_DonnePositionGroupe iagUnitSendMessage
        iagUnitRemoveFromGroup iaGroupDelete iagVilleSendMessage iagWarDeleteBattle iagWarAddEnnemyToBattle
        iagWarRemoveEnnemyFromBattle iagWarNewTargetForUnit iagWarUnlockTargetAfterDeath iagWarProbReturnTo
        iabDetection_AjouteEnnemiOuAlerteConflit iabTouche_AjouteEnnemiOuNeChangePasDeCibleOuAlerteConflit
        iabPlusCible_ChangeDeCibleOuObjectifRealise
    ''',
    'missions': '''
        BatimentGetTypeName EnginGetTypeName CaseGetZoneInfluence PartieGetResultat MissionNext MakeMissionName
        ObjectifLoadText FileOpen FileExists FileClose FileRead fopen fclose fread PlayerStore RechercheStore
        Engin_StoreExperimente TextGetMessage
    ''',
    'graphics': '''
        LoadBank MemAlloc GetBob TextGetLargeur AffText BobGetTaille
    ''',
    'audio': 'PlaySnd_PostSound PlaySnd_StopSound PlaySnd_StopAllSound',
}
FRONTEIRAS = {'PlaySnd_PostSound', 'PlaySnd_StopSound', 'PlaySnd_StopAllSound', 'PlaySnd_Manage',
              'MCICD_Manage', 'MCICD_Play', 'LoadPie'}
MATRIZ = 'pesquisas-paralelas/combate/M2_3_PRONTIDAO.json'


def _donos_curados():
    d = {}
    for dono, nomes in DONOS.items():
        for n in nomes.split():
            if n in d:
                raise ValueError(f'duplicate owner row {n}')
            d[n] = dono
    return d


# ------------------------------------------------------------------ inputs
def _git(*args):
    return subprocess.run(['git', '-C', str(RAIZ), *args], check=True, capture_output=True).stdout


def ler_captura(diretorio=None):
    """Return {name: bytes} of the S1 files, xz files decompressed, checked against replay.json."""
    nomes = ('quadros.jsonl.xz', 'fronteiras.jsonl.xz', 'comandos.jsonl.xz', 'replay.json', 'resumo.json')
    brutos = {}
    for n in nomes:
        if diretorio:
            brutos[n] = (Path(diretorio) / n).read_bytes()
        else:
            brutos[n] = _git('show', f'{S1_REV}:{S1_DIR}/{n}')
    replay = json.loads(brutos['replay.json'])
    if not replay.get('equal'):
        raise SystemExit('S1 replay.json does not declare the two runs equal')
    out = {'replay.json': replay, 'resumo.json': json.loads(brutos['resumo.json'])}
    for n in ('quadros.jsonl.xz', 'fronteiras.jsonl.xz', 'comandos.jsonl.xz'):
        dados = lzma.decompress(brutos[n])
        base = n[:-3]
        esperado = replay[base]['sha256']
        # Missions' relatorio_sondas.replay: each line as sorted-key JSON without 'seconds', joined by '\n'.
        normal = '\n'.join(json.dumps({k: v for k, v in json.loads(l).items() if k != 'seconds'}, sort_keys=True)
                           for l in dados.decode().splitlines() if l.strip())
        if hashlib.sha256(normal.encode()).hexdigest() != esperado:
            raise SystemExit(f'{base}: SHA-256 differs from replay.json ({esperado})')
        out[base] = dados
    return out


def agregar(quadros):
    tot, frames, primeiro, ultimo, info = collections.Counter(), collections.Counter(), {}, {}, {}
    n = 0
    for linha in io.BytesIO(quadros):
        d = json.loads(linha)
        n += 1
        f = d['frame']
        for r, k in d['entries'].items():
            tot[r] += k
            frames[r] += 1
            primeiro.setdefault(r, f)
            ultimo[r] = f
        for nr in d.get('new_routines', ()):
            info.setdefault(nr['routine'], nr)
    if set(tot) != set(info):
        raise SystemExit('entries and new_routines disagree')
    return dict(quadros=n, total=tot, frames=frames, primeiro=primeiro, ultimo=ultimo, info=info)


def simbolos():
    t = {}
    for linha in SIMBOLOS.read_text().splitlines()[1:]:
        a, nome = linha.split('\t')[:2]
        t[int(a, 16)] = nome
    return t


def chamadores_estaticos(sym):
    """{callee: set(caller routines)} from every E8/E9 rel32 whose target is a symbol start in the code."""
    raw = EXE.read_bytes()
    codigo = raw[0x400:0x400 + CODIGO[1] - CODIGO[0]]
    ends = sorted(a for a in sym if CODIGO[0] <= a < CODIGO[1])
    out = collections.defaultdict(set)
    for i in range(len(codigo) - 5):
        op = codigo[i]
        if op not in (0xe8, 0xe9):
            continue
        alvo = CODIGO[0] + i + 5 + struct.unpack_from('<i', codigo, i + 1)[0]
        if alvo not in sym or not CODIGO[0] <= alvo < CODIGO[1]:
            continue
        sitio = CODIGO[0] + i
        chamador = sym[ends[bisect.bisect_right(ends, sitio) - 1]]
        if chamador != sym[alvo] or op == 0xe8:
            out[sym[alvo]].add(chamador)
    return out


def so_exibicao(alcancadas, estaticos, info):
    def chamadores(r):
        c = {x for x in estaticos.get(r, ()) if x in alcancadas and x != r}
        fc = info[r]['caller']
        if fc:
            c.add(fc.split('+')[0])
        return c
    d = {'AffGame'}
    mudou = True
    while mudou:
        mudou = False
        for r in sorted(alcancadas - d):
            c = chamadores(r)
            if c and c <= d:
                d.add(r)
                mudou = True
    return d, {r: sorted(chamadores(r)) for r in alcancadas}


# ------------------------------------------------------------------ evidence
def cobertura_provas():
    """{routine: [proof labels]} for the chain proofs on main and the routines each window reaches."""
    out = collections.defaultdict(list)
    p9200 = json.loads((RAIZ / PROVA_9200).read_text())
    if p9200['summary']['result'] == 'equal':
        cob = json.loads(_git('show', f'{COB9200[0]}:{COB9200[1]}'))
        for r in cob['routines']:
            out[r].append('M2.3 chain proof 0-9200 (no input, {} phases equal)'.format(p9200['summary']['phases']))
    m31 = json.loads((RAIZ / PROVA_M31).read_text())
    for w in m31['windows']:
        if w['result'] != 'equal':
            continue
        a, b = w['frames']
        caminho = RAIZ / f"pesquisas-paralelas/missoes/m3/sondas/{w['window']}/quadros.jsonl.xz"
        vistos = set()
        with lzma.open(caminho, 'rt') as f:
            for linha in f:
                d = json.loads(linha)
                if a <= d['frame'] <= b:
                    vistos.update(d['entries'])
        for r in vistos:
            out[r].append(f"M3.1 chain proof {w['window']} {a}-{b} ({w['phases_equal']} phases equal)")
    return out


CHAVES_MAPA = {'by_routine', 'counts', 'live_by_routine', 'flat_by_routine', 'por_rotina', 'rotinas', 'routines',
               'comparisons_by_routine'}
CHAVES_LISTA = {'cases', 'results', 'rows', 'casos', 'resultados', 'comparisons'}
N_COMP = ('cases', 'comparisons', 'steps', 'comparacoes', 'casos', 'total', 'calls')
N_DIV = ('mismatches', 'mismatch', 'divergencias', 'diferencas')
FALHAS = {'mismatch', 'different', 'differs', 'divergente', 'diverged', 'fail', 'failed'}


def _relatorios():
    padrao = re.compile(r'(emulad|nativ|native|x86)', re.I)
    raizes = [RAIZ / 'relatorios'] + [RAIZ / 'pesquisas-paralelas' / d for d in
                                     ('combate', 'economia', 'graficos-animacao', 'missoes', 'ia-runtime', 'audio')]
    for base in raizes:
        for p in sorted(base.rglob('*.json')):
            if padrao.search(p.name) and 'local' not in p.name and p.stat().st_size < 40e6:
                yield p


def _frente(p):
    rel = p.relative_to(RAIZ).parts
    if rel[0] == 'relatorios':
        return 'core'
    return {'combate': 'combat', 'economia': 'economy', 'graficos-animacao': 'graphics', 'missoes': 'missions',
            'ia-runtime': 'ai-runtime', 'audio': 'audio'}[rel[1]]


def evidencias_isoladas(nomes):
    """{routine: [{report, front, comparisons, mismatches}]} from the native reports on main."""
    out = collections.defaultdict(list)
    for p in _relatorios():
        try:
            o = json.loads(p.read_text())
        except (ValueError, UnicodeDecodeError):
            continue
        acc = collections.defaultdict(lambda: [0, 0, False])   # comparisons, mismatches, mismatches known

        def walk(x, chave):
            if isinstance(x, dict):
                for k, v in x.items():
                    if k in CHAVES_MAPA and isinstance(v, dict):
                        for r, val in v.items():
                            if r not in nomes:
                                continue
                            if isinstance(val, int) and not isinstance(val, bool):
                                acc[r][0] += val
                            elif isinstance(val, dict):
                                c = next((val[q] for q in N_COMP if isinstance(val.get(q), int)), None)
                                m = next((val[q] for q in N_DIV if isinstance(val.get(q), int)), None)
                                if c is None and isinstance(val.get('match'), int):
                                    c = val['match'] + (m or 0)
                                if c is None and isinstance(val.get('equal'), int):
                                    c = val['equal'] + (m or 0)
                                if c:
                                    acc[r][0] += c
                                if m is not None:
                                    acc[r][1] += m
                                    acc[r][2] = True
                    walk(v, k)
            elif isinstance(x, list):
                for v in x:
                    if chave in CHAVES_LISTA and isinstance(v, dict):
                        r = v.get('routine', v.get('rotina'))
                        if isinstance(r, str) and r in nomes:
                            ruim = any(v.get(q) is False for q in ('ok', 'equal', 'registers_equal', 'state_equal',
                                                                     'changed_equal'))
                            ruim |= str(v.get('result', v.get('outcome', ''))).lower() in FALHAS
                            acc[r][0] += 1
                            acc[r][1] += int(ruim)
                            acc[r][2] = True
                    walk(v, chave)
        walk(o, None)
        for r, (c, m, conhecido) in acc.items():
            if c:
                out[r].append(dict(report=str(p.relative_to(RAIZ)), front=_frente(p), comparisons=c,
                                   mismatches=m if conhecido else None))
    return out


# Reports whose subject is one routine but whose rows do not name it: (routine, report, count key, pass key).
EVIDENCIA_CURADA = (
    ('CaseGetZoneInfluence', 'pesquisas-paralelas/missoes/validacao/m2-influencia-differential-x86.json',
     'native_calls_per_table', 'passed'),
)


def evidencias_curadas(out):
    for r, rel, chave_n, chave_ok in EVIDENCIA_CURADA:
        o = json.loads((RAIZ / rel).read_text())
        if o.get(chave_ok) is True and o.get(chave_n):
            out[r].append(dict(report=rel, front=_frente(RAIZ / rel), comparisons=o[chave_n], mismatches=0))


def evidencias_aninhadas(nomes, raizes_validadas):
    """{routine: sorted [(root, capture)]}: routines a native capture records as entered inside a root whose
    translation the isolated differentials compare (maps root -> {nested routine: entries})."""
    out = collections.defaultdict(set)
    bases = [RAIZ / 'evidencias'] + sorted(p for p in (RAIZ / 'pesquisas-paralelas').glob('*/evidencias'))
    vistos = set()
    for base in bases:
        for p in sorted(base.rglob('*.json')):
            if p in vistos or p.stat().st_size >= 40e6:
                continue
            vistos.add(p)
            try:
                o = json.loads(p.read_text())
            except (ValueError, UnicodeDecodeError):
                continue

            def walk(x):
                if isinstance(x, dict):
                    for k, v in x.items():
                        if (k in raizes_validadas and isinstance(v, dict) and v
                                and all(isinstance(q, int) and not isinstance(q, bool) for q in v.values())):
                            for n in v:
                                if n in nomes and n != k and v[n] > 0:
                                    out[n].add((k, str(p.relative_to(RAIZ))))
                        walk(v)
                elif isinstance(x, list):
                    for v in x:
                        walk(v)
            walk(o)
    return {n: sorted(v) for n, v in out.items()}


def mencoes(linhas):
    """Unverified pointers for gap rows: native reports naming the routine or its address (often as a
    dependency stop or a served provider, not a comparison). For the owner to confirm."""
    textos = {p: p.read_text(errors='ignore') for p in _relatorios()}
    for l in linhas:
        if l['status'] != 'gap':
            continue
        a = l['address'][2:]
        chaves = ('0x' + a, '0x00' + a, '"' + l['routine'] + '"')
        l['mentioned_in_native_reports'] = sorted(str(p.relative_to(RAIZ)) for p, t in textos.items()
                                                  if any(k in t for k in chaves))[:6]


# ------------------------------------------------------------------ survey
def levantar(diretorio=None):
    cap = ler_captura(diretorio)
    ag = agregar(cap['quadros.jsonl'])
    alcancadas = set(ag['total'])
    sym = simbolos()
    porn = {n: a for a, n in sym.items()}
    estaticos = chamadores_estaticos(sym)
    exib, chamadores = so_exibicao(alcancadas, estaticos, ag['info'])
    fronteiras = collections.Counter(json.loads(l)['routine'] for l in io.BytesIO(cap['fronteiras.jsonl']))
    matriz = {r['routine']: r for r in json.loads((RAIZ / MATRIZ).read_text())['routines']}
    curados = _donos_curados()
    provas = cobertura_provas()
    isol = evidencias_isoladas(alcancadas)
    evidencias_curadas(isol)
    sobra = set(curados) - alcancadas
    if sobra:
        raise SystemExit(f'owner rows for routines S1 does not reach: {sorted(sobra)}')
    validadas = {r for r, ev in isol.items() if ev and not any(e['mismatches'] for e in ev)}
    aninh = evidencias_aninhadas(alcancadas, validadas)

    linhas = []
    for r in sorted(alcancadas, key=lambda n: (ag['primeiro'][n], n)):
        if r in curados:
            dono, fonte = curados[r], 'curated'
        elif r in matriz:
            dono, fonte = matriz[r]['owner'], 'M2_3_PRONTIDAO'
        elif r in exib:
            dono, fonte = 'graphics', 'display-only'
        else:
            raise SystemExit(f'no owner for {r}')
        ev = isol.get(r, [])
        nativas = sum(e['comparisons'] for e in ev)
        div = [e for e in ev if e['mismatches']]
        if r in FRONTEIRAS:
            status = 'boundary'
        elif ev and not div:
            status = 'validated'
        elif aninh.get(r) and not div:
            status = 'nested-validated'
        elif provas.get(r):
            status = 'chain-only' if r not in exib else 'display-chain'
        elif r in exib:
            status = 'display'
        elif ev:
            status = 'mismatch-reported'
        else:
            status = 'gap'
        i = ag['info'][r]
        linhas.append(dict(
            routine=r, address=i['address'] if 'address' in i else hex(porn[r]), owner=dono, owner_source=fonte,
            first_frame=ag['primeiro'][r], last_frame=ag['ultimo'][r], calls=ag['total'][r],
            frames_with_calls=ag['frames'][r], first_phase=i['phase'], first_caller=i['caller'],
            first_caller_return=i['caller_return'], s1_static_callers=chamadores[r], display_only=r in exib,
            boundary_calls=fronteiras.get(r), chain_proofs=provas.get(r, []), native_evidence=ev,
            nested_in_validated=[dict(root=a, capture=b) for a, b in aninh.get(r, [])][:6],
            native_comparisons=nativas, status=status,
            translated_validated_on_main=status in ('validated', 'nested-validated', 'chain-only', 'display-chain',
                                                     'boundary')))
    mencoes(linhas)
    lacunas = collections.defaultdict(list)
    for l in linhas:
        if l['status'] in ('gap', 'mismatch-reported', 'display'):
            lacunas[l['owner']].append(l)
    resumo = {f: dict(routines=sum(1 for l in linhas if l['owner'] == f),
                      gaps=len(lacunas[f]),
                      by_status=dict(collections.Counter(l['status'] for l in linhas if l['owner'] == f)))
              for f in FRENTES}
    return dict(
        schema='rising-lands/s1-coverage/1',
        evidence=False,
        note='coverage survey, not evidence: routine-level status read from main; branches inside a validated '
             'routine may still be unproven on S1 states',
        capture=dict(revision=S1_REV, path=S1_DIR, frames=[129, cap['resumo.json']['last_frame']],
                     frames_recorded=ag['quadros'], replay_equal=True,
                     sha256={k: cap['replay.json'][k]['sha256'] for k in ('quadros.jsonl', 'fronteiras.jsonl')},
                     original_sha256=cap['resumo.json']['original_sha256']),
        main=_git('rev-parse', 'HEAD').decode().strip(),
        sources=dict(chain_proofs=[PROVA_9200, PROVA_M31, f'{COB9200[0]}:{COB9200[1]}'], owner_matrix=MATRIZ,
                     static_callers='E8/E9 rel32 scan of RISING.EXE code section 0x401000-0x493c00'),
        status_meaning={
            'validated': 'isolated native differential(s) on main compare it, no mismatch reported',
            'nested-validated': 'a native capture records it entered inside a root that an isolated differential '
                                'compares with no mismatch (covered through that root\'s translation)',
            'chain-only': 'reached inside an equal chain proof window on main, no isolated differential',
            'display-chain': 'display-only, reached inside a proven window (Python models logic effects only)',
            'display': 'display-only, never inside a proven window: Graphics draws/models it',
            'boundary': 'declared boundary (audio/MCI/picture load); Audio owns the request log',
            'mismatch-reported': 'a native report lists mismatches for it',
            'gap': 'no chain proof window reaches it and no native differential compares it'},
        totals=dict(routines=len(linhas), calls=sum(l['calls'] for l in linhas),
                    by_status=dict(collections.Counter(l['status'] for l in linhas))),
        by_owner=resumo,
        gaps_by_owner={f: [dict(routine=l['routine'], first_frame=l['first_frame'], calls=l['calls'],
                                status=l['status'], first_caller=l['first_caller'])
                           for l in sorted(lacunas[f], key=lambda l: (l['first_frame'], -l['calls']))]
                       for f in FRENTES},
        routines=linhas)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--captura', help='directory holding the S1 files (default: the git object at 82ec5ea)')
    ap.add_argument('--saida', default=str(RAIZ / 'relatorios/cobertura-s1.json'))
    a = ap.parse_args()
    rel = levantar(a.captura)
    Path(a.saida).write_text(json.dumps(rel, indent=1, sort_keys=True) + '\n')
    print(json.dumps(dict(totals=rel['totals'], by_owner=rel['by_owner']), indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
