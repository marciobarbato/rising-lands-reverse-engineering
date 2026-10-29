"""M3 Step 0: static target extraction for the scripted-input probes P1-P5 and the run S1.

No emulation. Inputs are accepted original reference bytes only:

* the M2.2 frame-128 checkpoint (``state_after.full_state`` of phase ``frame128``
  in ``evidencias/captura-quadros128-monde01-exibicao-v2.json.xz``), the state S1
  starts from (F0 = 129);
* the accepted M1 MissionLoad final state (``captura-carga-missao-original-v2.json``),
  used only as a cross-check of what changed by frame 128;
* the intact ``RISING.EXE``, when present, only to verify that the code ranges
  this module cites still hash to the recorded SHA-256 values.

Every published item carries a label, as in docs/M3_PLAN.md:
``B`` = read from accepted state bytes or from an instruction encoding;
``S`` = inferred (a translation run over those bytes, a reachability or
ordering claim, or a preference). A ``B`` code fact is an encoding, never a
claim that the branch runs.

Committed providers are imported, not copied: Core ``incursao_core.caso_unidade``
(EnginGetCase), ``chamadas_quadro_core.caso_estrutura`` (BatimentGetCase),
Missions ``influencia_missao.zona_influencia`` (CaseGetZoneInfluence) and
Economy ``extracao.RecursosTerreno`` (MineGetIndice/MineGetCapacite,
TerrainEstChampi). The small predicates without a committed full translation
(TerrainEstSac, TerrainEstMine, TerrainEstGc, TerrainEstHerbe,
TerrainEstDecouvert, TerrainGetSacType, MouseZone, IconeGetZone, BatimentPosable
without EnginOccupeCase) are written here from the cited bytes and labelled S
when used as a prediction.

Run: ``python3 -B pesquisas-paralelas/missoes/m3/extrair_alvos_m3.py [--saida PATH]``.
Importing this module executes nothing.
"""
import argparse
import base64
import hashlib
import json
import lzma
from pathlib import Path
import sys
import zlib

AQUI = Path(__file__).resolve().parent
MISSOES = AQUI.parent
if str(MISSOES) not in sys.path:
    sys.path.insert(0, str(MISSOES))
import ambiente_missoes  # noqa: E402  (adds ferramentas, economia, source/python)

RAIZ = ambiente_missoes.ROOT
CAPTURA_128 = MISSOES / 'evidencias/captura-quadros128-monde01-exibicao-v2.json.xz'
MANIFESTO_128 = MISSOES / 'evidencias/captura-quadros128-monde01-exibicao-v2.manifest.json'
CAPTURA_M1 = MISSOES / 'evidencias/captura-carga-missao-original-v2.json'
EXECUTAVEL = ambiente_missoes.CD / 'INSTALHD/RISING.EXE'
SAIDA = AQUI / 'alvos-m3-monde01.json'
SCHEMA = 'rising-lands/monde01-m3-static-targets/1'
HASH_EXECUTAVEL = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'

# ---------------------------------------------------------------- addresses (all B: operands of the cited code)
UNIDADES_PTR, PASSO_UNIDADE = 0x4e19a0, 276
ESTRUTURAS, PASSO_ESTRUTURA = 0x49a0c8, 276
TIPOS_ESTRUTURA, PASSO_TIPO_ESTRUTURA = 0x495d8c, 52   # +0 w, +2 h, +0xc food, +0xe stone, +0x10 parts
SACOS_ORDEM_PTR, PASSO_SACO = 0x4e19b8, 104            # [[0x4e19b8]+4*owner] + type*104
RECURSOS, PASSO_JOGADOR = 0x4e2ea8, 32                  # TestRessource: parts +2, food +0xa, stone +0x12
GRADE_TILES, GRADE_OBJETOS, GRADE_ATRIBUTOS, GRADE_QUANTIDADES = 0x507d70, 0x507d74, 0x507da8, 0x507dac
GRADES_DESCOBERTA = 0x507d78                            # u32 grid pointer per player
INFLUENCIA = 0x50c614
MINAS = 0x509954
ZONAS_MOUSE, ZONA_TESTE = 0x5099b4, 0x50a9b4            # 16-byte records; u16 first, u16 last tested
TELA = 0x49a018                                         # u16 width, +2 height
VISTA_ORIGEM, VISTA_TAMANHO = 0x508720, 0x508724        # u16 x, y (cells); u16 w, h (cells)
DESLOCAMENTO_PAINEL = 0x508f90                          # s8 (high byte of the dword at 0x508f8d)
JOGADOR_LOCAL = 0x508041
SELECAO = 0x508728                                      # u16 count + u16 entries, 512 bytes per player

TIPO_CAVE, TIPO_BATISSEUR = 3, 7
UNIDADES_ALVO = (12, 13, 14, 11, 15)

# Code ranges this module relies on: (name, start, end_exclusive, sha256 of the intact image bytes).
ANCORAS = (
    ('WndProc message dispatch', 0x4181b5, 0x4181f4, 'c24d4d2f5c3c0e5088a514d1fc403623d479ac41c069c6e2f509be573193fe9d'),
    ('WndProc mouse stores', 0x418207, 0x418272, 'eba103cc87841a29c6f225d82708d0b28797dfa6b0814daa1a0edd989e3001d8'),
    ('WndProc 0x200/0x201 dispatch', 0x41852b, 0x41853d, '17ee9d22e68475cbee2beaca8a42dc35c53d25afcba9e8b20fb62519982c113c'),
    ('ProgIteration click-flag clear', 0x475068, 0x47507f, '06ec03b38130629fb9486b8f11f055dd2f88dbcc5452a24d4fe7b5e0c2763658'),
    ('MouseZone', 0x479cac, 0x479d0d, '4cc877b957873ac6f76cd9586e66ceac82cf9048ffb7626c73fcc3444a38bf1e'),
    ('InputGame zone dispatch', 0x4297c1, 0x429800, '3126a37f19aaa08bc484c7b53d43652af09b82f791f3ea4bbd4ed46ddf80c5ca'),
    ('InputGame zone dispatch tail', 0x42c287, 0x42c2ae, '38b4d788d51fb25b47ea5baa0f108f7c984dda33b3facd2a5117e978261e3b25'),
    ('InputGame playfield cell mapping and guard', 0x429800, 0x4298cc, 'ec8f587ab5ff8fb8da83d790228183235353f9b56e7a46f196aabc112c0821f3'),
    ('InputGame HUD icon branch', 0x42bcd9, 0x42bdf1, '579cb711b6d8d8f7652a5677409be01a038bc63db7e5767c942f020ce7dc8523'),
    ('InputGame bag-code dispatch', 0x42c25e, 0x42c287, '4a1481b524020c8252396337072b1d06c0b0281f2bc8e2e4b6f3775a4d8e6d3a'),
    ('InputGame bag-code jump table', 0x429260, 0x429278, 'ec92cffc84fdc2f800632303e4afe6258da88d6998f8c5e272008a09efe78238'),
    ('InputGame structure icon (code 3)', 0x42c116, 0x42c1ff, 'b023dd838405bbd80d40b5742f8c30076d981b19bce1cc3b91c3ef5a27d4bb0f'),
    ('InputGame build-site click (mode 3)', 0x429f46, 0x42a077, 'b12c6db103c0e151e5cee09398da0cfe5e41f5c926e778308d600d0736160d1e'),
    ('InputGame food/stone click', 0x42b311, 0x42b64d, '7a1fba67e3487318288f6621ce1315e4d21cc3f5b25a0f97cf44ca256fdbddde'),
    ('InputGame mode-9 dispatch', 0x429c32, 0x429da1, 'fabe8925ad6a3cd7e16585eb0a9f9ab31d46a2264ec309a6c5703e45649ff3b6'),
    ('InputGame mode-9 jump table', 0x42923c, 0x42924c, 'bd4bc395500385f2fb784f10899e8705154c4cb27cde9361900b319941171ae2'),
    ('InputGame Ctrl transport mode', 0x4295f3, 0x429634, '0476ec2a8143eae8e2c21f0cef81d689b69a89ef98a1eaabc34503c3cf72fdcc'),
    ('IconeGetZone', 0x45da4e, 0x45db1f, 'c00e2b001065ce79221efcd4967a6d235c2e99f8984c1cb0983803d05a753cef'),
    ('BagGetCode/BagGetType', 0x4472d3, 0x4472ea, '7a22b6740a41459a768627b354721423533418f648c46e5b7407c01ea509bf78'),
    ('EnginGetBagOrdre', 0x4474f3, 0x447543, '46ea374a731f4a679de84498e45122f2bdcbabea2033529fe009681ddb0e344c'),
    ('EnginTravailSelectionne', 0x47248f, 0x47253d, 'f9c4b5503f8a597ff0d2dc348137cedde78df046e046c32b504562775a58fbfa'),
    ('BatimentGetRessource', 0x41aace, 0x41ab04, 'f876ad480c0a9a881c49c8aea29a94ca8b39576067d1d6b372dfb602f9cc927c'),
    ('TestRessource', 0x4676e5, 0x467718, 'e36bd212078b4516f4132bdd36bc6d8d5d393aea5cc58401af613ecdee840c26'),
    ('CreerBatiment', 0x41fea2, 0x4202ce, '73064d19967425415199c4a6ce7159703ec7bfad27401e8a8bae4400cbdd7c98'),
    ('BatimentGetDecalageConstruction', 0x41aea4, 0x41aee2, '41eb0b671cabaff25da6c4c837a83e2f92584040fe7cbe7d4036719dd85b4756'),
    ('BatimentGetDecalageConstruction table', 0x41ae4c, 0x41aea4, '040e1af18b93888fe6e3ef7a274dc5f275edd724377af7f325686f36297876de'),
    ('BatimentConstructible', 0x41fb12, 0x41fc40, '48c12c20e2a75144fb59499aa8864d6d6ef23ae242ce5781efd67a73427b567e'),
    ('BatimentPosable', 0x41fc40, 0x41fea2, 'e60c908f8c843c883ede6f7c329d9bf9be121b178d82c5cbdefd56dcdfd6555a'),
    ('CalculConstruireBatiment build step', 0x44ad13, 0x44ad8e, '17e1eaa9e08cf8dacfa230f09c2b3ca7727cd9f9faef579e57eb221bbe3d8065'),
    ('BatimentLogeEngin owner store', 0x41fa53, 0x41fa8d, '7bb187523aebc97a75a6219644fc57c6b64adfa570be5cf18c0a907052e1c8dd'),
    ('BatimentGetPlayer', 0x41a08c, 0x41a0ab, '73c7960bdd0b83a8016cc9f7097a635079ae215bfcd10f91c37badd7e6c90932'),
    ('TerrainEstSac', 0x4766b1, 0x4766d6, '0a70f7139b964d20c3c44927595f2bda3e164264471fe41ecd346dda4fd96b51'),
    ('TerrainEstDecouvert', 0x4766f0, 0x47670a, 'c7d7973f063848a5fbb332c9d87310bfea7ce416069d880fc6c7cfb2f0a58262'),
    ('TerrainEstMine', 0x476263, 0x4762b9, '1934a68fa555d506d65dafc944a289236f2cbed75caf5c0bbc45e084732d5ab2'),
    ('TerrainEstGc', 0x4762b9, 0x4762de, '4f523a14bd0d0338368b49566cd8b203840756e80549e0bb53ed7d95ecd90ea1'),
    ('TerrainEstHerbe', 0x47636a, 0x4763c0, '7c2d8f0eb66baa5c4d38f0c2fedc64b2ecdb1fa2f2acc0a834b307e7dc7de78e'),
    ('TerrainGetSacType', 0x476038, 0x47605d, '5b95493c9fa209925cd47688ab4a0400a6f939ca433f0cb18dafa5a07b1191ad'),
    ('TerrainEnCollision', 0x4761d4, 0x4761f1, '5a4df51651db84b2b01819a672e0ad7c0253524d5ee65192abfde4bffdf41b3a'),
    ('EnginGetCase', 0x44113e, 0x44115f, '43c2b33fd2e3a5d6941ebe6d8dda3a737e1c3f254486eac0414c2b7d6734eea3'),
    ('CaseEstDecouverte', 0x4766d6, 0x4766f0, '2e3c150188cd700809900fd0e8561f2dc67c915400e3deb4e739a86cca1e613a'),
    ('InputGame undiscovered-cell gate', 0x4298cc, 0x4299ad, 'aded738f0c0034288e06a5db4f136eb645430512c862b5e9a57788dd68b2ba17'),
    ('InputGame minimap branch', 0x42bade, 0x42bbff, 'ad5a7fc438e7522abc4ad1990c85f2cff5064b3a177ca2d10c8b179db7fa3c8b'),
    ('MiniMapGetCase', 0x46a224, 0x46a273, '76ac30d678406bb4f8b9b74377d0c97d842c18f635667f61b541ffbdaf47101e'),
    ('MiniMapGetCenterSelect', 0x46a273, 0x46a369, 'aa866c6361c0b7fc34c53ebea82a0f9c5ed0fb1b7e02fe3feacbf158d7ff2a85'),
)


def _sha256(dados):
    return hashlib.sha256(dados).hexdigest()


def _rel(caminho):
    return str(Path(caminho).resolve().relative_to(RAIZ))


# ---------------------------------------------------------------- loading accepted state
def _memoria(segmentos):
    from memoria_quadro_core import MemoriaQuadro
    return MemoriaQuadro(segmentos)


def carregar_quadro128(caminho=CAPTURA_128):
    """MemoriaQuadro over the frame-128 checkpoint; the recorded summary SHA-256 must be reproduced."""
    from delta_estado_missao import resumo
    bruto = Path(caminho).read_bytes()
    captura = json.loads(lzma.decompress(bruto))
    fase = captura['phases'][-1]
    if fase['phase'] != 'frame128':
        raise ValueError(f"last phase is {fase['phase']}, expected frame128")
    blocos = {}
    for nome, bloco in fase['state_after']['full_state'].items():
        blocos[nome] = (int(bloco['base'], 16), bytearray(zlib.decompress(base64.b64decode(bloco['zlib_base64']))))
    gravado, obtido = fase['state_after']['summary'], resumo(blocos)
    if obtido != gravado:
        raise ValueError(f'frame128 checkpoint does not reproduce its recorded summary: {obtido} != {gravado}')
    fonte = dict(path=_rel(caminho), xz_sha256=_sha256(bruto), phase='frame128',
                 summary=gravado, summary_reproduced=True, label='B')
    return _memoria((b, d) for n, (b, d) in blocos.items() if n != 'native_stack'), fonte


def carregar_m1(caminho=CAPTURA_M1):
    """MemoriaQuadro over the accepted M1 MissionLoad final state; every block SHA-256 is checked."""
    from mapa_memoria_m1 import carregar_blocos
    bruto = Path(caminho).read_bytes()
    final = json.loads(bruto)['oracle']['final_state']
    blocos = carregar_blocos(final['blocks'])
    fonte = dict(path=_rel(caminho), sha256=_sha256(bruto), summary=final['summary'],
                 block_hashes_verified=True, label='B')
    return _memoria((b, bytearray(d)) for n, (b, d) in blocos.items() if n != 'native_stack'), fonte


def verificar_ancoras(caminho=EXECUTAVEL):
    """Recompute each cited code range from the intact image; None when the executable is absent."""
    if not Path(caminho).exists():
        return None
    from analisar import dependencias
    pefile, _ = dependencias()
    dados = Path(caminho).read_bytes()
    if _sha256(dados) != HASH_EXECUTAVEL:
        raise ValueError('RISING.EXE is not the intact executable')
    imagem = pefile.PE(data=dados).get_memory_mapped_image()
    base = 0x400000
    return [dict(name=n, start=f'0x{a:06x}', end_exclusive=f'0x{b:06x}', sha256=h,
                 verified=_sha256(imagem[a - base:b - base]) == h) for n, a, b, h in ANCORAS]


# ---------------------------------------------------------------- small helpers
def xy(celula):
    celula &= 0xffff
    return celula & 0xff, celula >> 8


def celula(x, y):
    return ((y & 0xff) << 8) | (x & 0xff)


def _s8(v):
    return v - 0x100 if v & 0x80 else v


def vista(m):
    return dict(origin=(m.u16(VISTA_ORIGEM), m.u16(VISTA_ORIGEM + 2)),
                size=(m.u16(VISTA_TAMANHO), m.u16(VISTA_TAMANHO + 2)),
                screen=(m.u16(TELA), m.u16(TELA + 2)),
                panel_offset=_s8(m.u8(DESLOCAMENTO_PAINEL)))


def pixel_de_celula(m, c):
    """Centre pixel (32(x-vx)+16, 32(y-vy)+16) of cell c under the current view, or None off-screen."""
    v = vista(m)
    x, y = xy(c)
    (vx, vy), (vw, vh), d = v['origin'], v['size'], v['panel_offset']
    px, py = 32 * (x - vx) + 16, 32 * (y - vy) + 16
    if not (32 * d <= px < 32 * (vw - d) and 32 * d <= py < 32 * (vh - d)):
        return None
    return px, py


def celula_de_pixel(m, px, py):
    """InputGame 0x429800..0x42984a encoding: cell = ((Y>>5)+vy)<<8 + (X>>5)+vx, under the guard
    d*32 <= X < (vw-d)*32, d*32 <= Y < (vh-d)*32 (0x42984c..0x4298c6); None outside the guard."""
    v = vista(m)
    (vx, vy), (vw, vh), d = v['origin'], v['size'], v['panel_offset']
    if not (32 * d <= px < 32 * (vw - d) and 32 * d <= py < 32 * (vh - d)):
        return None
    return ((((py >> 5) + vy) << 8) + (px >> 5) + vx) & 0xffff


def zonas_mouse(m):
    """The MouseSetZone table 0x5099b4 (16-byte records of four u32: x0, y0, x1, y1) and the tested range."""
    primeira, ultima = m.u16(ZONA_TESTE), m.u16(ZONA_TESTE + 2)
    return primeira, ultima, {i: tuple(m.u32(ZONAS_MOUSE + 16 * i + 4 * k) for k in range(4)) for i in range(ultima + 1)}


def zona_mouse(m, px, py):
    """MouseZone 0x479cac: first zone in [first..last] with x0<=X<=x1 and y0<=Y<=y1, else 0."""
    primeira, ultima, zonas = zonas_mouse(m)
    for i in range(primeira, ultima + 1):
        x0, y0, x1, y1 = zonas[i]
        if x0 <= px <= x1 and y0 <= py <= y1:
            return i
    return 0


def retangulos_icones(m):
    """IconeGetZone 0x45da4e: action icons 0..3 and scroll icons 8/9, inclusive pixel rectangles."""
    y0 = 0x1a4 if m.u16(TELA) == 0x280 else 0x224
    icones = {i: (0x1f + 0x3c * i, y0, 0x1f + 0x3c * i + 0x3a, y0 + 0x32) for i in range(4)}
    icones[8] = (8, y0, 0x1e, y0 + 0x34)
    icones[9] = (0x110, y0, 0x126, y0 + 0x34)
    return icones


def icone_em(m, px, py):
    for i, (x0, y0, x1, y1) in retangulos_icones(m).items():
        if x0 <= px <= x1 and y0 <= py <= y1:
            return i
    return 0xffff


def unidade(m, i):
    u = (m.u32(UNIDADES_PTR) + i * PASSO_UNIDADE) & 0xffffffff
    return dict(owner=m.u8(u), type=m.u8(u + 1), state=m.u8(u + 2), cell_plus8=m.u16(u + 8))


def saco_ordens(m, i):
    """EnginGetBagOrdre 0x4474f3 for unit i, read with BagGetType (+6+2k) and BagGetCode (+0x42+k)."""
    u = unidade(m, i)
    saco = (m.u32(m.u32(SACOS_ORDEM_PTR) + 4 * u['owner']) + u['type'] * PASSO_SACO) & 0xffffffff
    quantidade, rolagem = m.u16(saco), m.u16(saco + 4)
    entradas = [dict(index=k, type=m.u16(saco + 6 + 2 * k), code=m.u8(saco + 0x42 + k)) for k in range(quantidade)]
    return dict(address=f'0x{saco:08x}', count=quantidade, scroll=rolagem, entries=entradas)


def custo_estrutura(m, tipo):
    """BatimentGetRessource 0x41aace / CreerBatiment 0x41ff1e: food, stone, parts of a structure type."""
    t = TIPOS_ESTRUTURA + PASSO_TIPO_ESTRUTURA * tipo
    return dict(food=m.u16(t + 0xc), stone=m.u16(t + 0xe), parts=m.u16(t + 0x10))


def dimensoes_estrutura(m, tipo):
    t = TIPOS_ESTRUTURA + PASSO_TIPO_ESTRUTURA * tipo
    return m.u16(t), m.u16(t + 2)


def estoque(m, jogador):
    r = RECURSOS + PASSO_JOGADOR * jogador
    return dict(parts=m.u16(r + 2), food=m.u16(r + 0xa), stone=m.u16(r + 0x12))


def _grade(m, ponteiro):
    return m.u32(ponteiro)


def objeto(m, c):
    return m.u8(_grade(m, GRADE_OBJETOS) + (c & 0xffff))


def tile(m, c):
    return m.u16(_grade(m, GRADE_TILES) + 2 * (c & 0xffff))


def atributo(m, c):
    return m.u8(_grade(m, GRADE_ATRIBUTOS) + (c & 0xffff))


def descoberta(m, c, jogador):
    return m.u8(m.u32(GRADES_DESCOBERTA + 4 * jogador) + (c & 0xffff))


def terreno_est_sac(m, c):            # 0x4766b1
    return 0x42 <= objeto(m, c) <= 0x44


def terreno_get_sac_type(m, c):       # 0x476038
    o = objeto(m, c)
    return o - 0x42 if 0x42 <= o <= 0x44 else 0xff


def terreno_est_gc(m, c):             # 0x4762b9
    return 0x1d <= objeto(m, c) < 0x35


def terreno_est_mine(m, c):           # 0x476263
    return 0x251 <= tile(m, c) <= 0x252 or 0x255 <= tile(m, c) <= 0x256


def terreno_est_herbe(m, c):          # 0x47636a
    return 0x15d <= tile(m, c) < 0x1a5


def terreno_est_decouvert(m, c, jogador):   # 0x4766f0: AL = (discovery & 0x1f) == 0
    return descoberta(m, c, jogador) & 0x1f == 0


def terreno_en_collision(m, c, mascara=1):  # 0x4761d4
    return bool(atributo(m, c) & mascara)


def case_est_decouverte(m, c, jogador):
    """Core CaseEstDecouverte 0x4766d6 (AL = (discovery & 0x10) == 0), the gate InputGame applies at 0x4298d9."""
    from chamadas_quadro_core import caso_esta_descoberta
    return bool(caso_esta_descoberta(m, c, jogador)['EAX'] & 0xff)


MINIMAPA_POS, MINIMAPA_TAMANHO = 0x507d68, 0x496fe0


def _idiv(a, b):
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b > 0) else -q


def minimapa_centrar(m, px, py):
    """MiniMapGetCenterSelect 0x46a273 as called at 0x42bbf5 (nothing selected, 0x5099ae set, MouseZone 10):
    the view origin it stores at 0x508720/0x508722 for a press at screen pixel (px, py)."""
    mx, my = px - m.u16(MINIMAPA_POS), py - m.u16(MINIMAPA_POS + 2)
    mmw, mmh = m.u16(MINIMAPA_TAMANHO), m.u16(MINIMAPA_TAMANHO + 2)
    mapw, maph = m.u16(0x497168), m.u16(0x49716a)
    vw, vh = m.u16(VISTA_TAMANHO), m.u16(VISTA_TAMANHO + 2)
    hx, hy = _idiv(_idiv(vw * mmw, mapw), 2), _idiv(_idiv(vh * mmh, maph), 2)
    vx, vy = _idiv(((mx & 0xffff) - hx) * mapw, mmw), _idiv(((my & 0xffff) - hy) * maph, mmh)
    vx, vy = max(vx, 0), max(vy, 0)
    if vx + vw > mapw:
        vx = mapw - vw
    if vy + vh > maph:
        vy = maph - vh
    return vx, vy


def _pixels_minimapa(m):
    x0, y0 = m.u16(MINIMAPA_POS), m.u16(MINIMAPA_POS + 2)
    x1, y1 = x0 + m.u16(MINIMAPA_TAMANHO), y0 + m.u16(MINIMAPA_TAMANHO + 2)
    for py in range(y0, y1 + 1):
        for px in range(x0, x1 + 1):
            if zona_mouse(m, px, py) == 10:
                yield px, py, min(px - x0, py - y0, x1 - px, y1 - py, px, py)


def pressao_minimapa(m, vx, vy):
    """Pixel in MouseZone 10, farthest from the minimap and screen borders, whose press (nothing selected)
    recentres the view at (vx, vy); None when no pixel does."""
    validos = [(margem, -py, -px) for px, py, margem in _pixels_minimapa(m) if minimapa_centrar(m, px, py) == (vx, vy)]
    if not validos:
        return None
    _, py, px = max(validos)
    return -px, -py


def minimapa_celula(m, px, py):
    """MiniMapGetCase 0x46a224 as called at 0x42bbc1: the tag-5 destination of a minimap press with troops selected."""
    mx, my = (px - m.u16(MINIMAPA_POS)) & 0xffff, (py - m.u16(MINIMAPA_POS + 2)) & 0xffff
    cx = _idiv(mx * m.u16(0x497168), m.u16(MINIMAPA_TAMANHO))
    cy = _idiv(my * m.u16(0x49716a), m.u16(MINIMAPA_TAMANHO + 2))
    return ((cy << 8) + cx) & 0xffff


def pressao_minimapa_mover(m, alvo):
    """Pixel in MouseZone 10 (largest border margin) whose press with troops selected orders a move to ``alvo``."""
    validos = [(margem, -py, -px) for px, py, margem in _pixels_minimapa(m) if minimapa_celula(m, px, py) == alvo]
    if not validos:
        return None
    _, py, px = max(validos)
    return [-px, -py]


def vista_para(m, alvo, companheira=None):
    """A view origin (S) that shows ``alvo`` (and ``companheira`` when possible) at least 4 cells from the
    minimap corner, with the minimap press that sets it and the target's pixel under it."""
    vw, vh = m.u16(VISTA_TAMANHO), m.u16(VISTA_TAMANHO + 2)
    mapw, maph = m.u16(0x497168), m.u16(0x49716a)
    tx, ty = xy(alvo)
    melhores = []
    for vy in range(0, maph - vh + 1):
        for vx in range(0, mapw - vw + 1):
            if not (vx <= tx < vx + vw and vy <= ty < vy + vh) or (tx - vx <= 3 and ty - vy <= 3):
                continue
            junto = companheira is not None and (lambda cx, cy: vx <= cx < vx + vw and vy <= cy < vy + vh
                                                 and not (cx - vx <= 3 and cy - vy <= 3))(*xy(companheira))
            centro = abs(tx - (vx + vw // 2)) + abs(ty - (vy + vh // 2))
            melhores.append((not junto, centro, vy, vx, junto))
    if not melhores:
        return None
    _, _, vy, vx, junto = min(melhores)
    press = pressao_minimapa(m, vx, vy)
    return dict(view_origin=[vx, vy], target_pixel=[32 * (tx - vx) + 16, 32 * (ty - vy) + 16],
                minimap_move_press_pixel=pressao_minimapa_mover(m, alvo),
                companion_also_on_screen=junto,
                companion_pixel=([32 * (xy(companheira)[0] - vx) + 16, 32 * (xy(companheira)[1] - vy) + 16] if junto else None),
                minimap_press_pixel=list(press) if press else None, label='S')


def batiment_posable(m, tipo, c, jogador):
    """BatimentPosable 0x41fc40 for a type other than 0xc, WITHOUT EnginOccupeCase 0x44246e.

    Footprint w x h centred at c (start = c - w//2 - (h//2)<<8), bounds as 0x41fd02..0x41fd2d.
    Each cell must be TerrainEstHerbe and TerrainEstDecouvert(owner) and either free of
    collision bit 0 or occupied by the ordering unit itself (EnginOccupeCase). Returns
    'valid' when every cell passes without collision, 'invalid' when a cell fails a test that
    does not depend on EnginOccupeCase, 'needs_EnginOccupeCase' otherwise.
    """
    w, h = dimensoes_estrutura(m, tipo)
    x, y = xy(c)
    if w // 2 > x or y < h // 2 or x - w // 2 + w - 1 > 0x100 or y - h // 2 + h - 1 > 0x100:
        return 'invalid', []
    inicio = (c - w // 2 - ((h // 2) << 8)) & 0xffff
    celulas = [(inicio + (r << 8) + k) & 0xffff for r in range(h) for k in range(w)]
    pendente = False
    for cc in celulas:
        if not terreno_est_herbe(m, cc) or not terreno_est_decouvert(m, cc, jogador):
            return 'invalid', celulas
        if terreno_en_collision(m, cc, 1):
            pendente = True
    return ('needs_EnginOccupeCase' if pendente else 'valid'), celulas


def centro_estrutura_hipotetica(m, tipo, origem):
    """Core BatimentGetCase 0x41aee2 on a scratch DGROUP copy holding one record of this type/origin."""
    from chamadas_quadro_core import caso_estrutura
    dgroup = bytearray(m.ler(0x494000, 585728))
    scratch = _memoria([(0x494000, dgroup)])
    indice = 999
    base = ESTRUTURAS + indice * PASSO_ESTRUTURA
    scratch.u16(base + 2, origem)
    scratch.u8(base + 8, tipo)
    return caso_estrutura(scratch, indice)['EAX'] & 0xffff


def _alvo_celula(m, c, rotulo_celula):
    px = pixel_de_celula(m, c)
    item = dict(cell=c, xy=list(xy(c)), cell_label=rotulo_celula, discovery_byte_player0=descoberta(m, c, 0),
                caseEstDecouverte=case_est_decouverte(m, c, 0))
    if px is None:
        item.update(pixel=None, pixel_label='S', on_screen=False)
    else:
        item.update(pixel=list(px), pixel_label='S', on_screen=True, mouse_zone=zona_mouse(m, *px),
                    mouse_zone_label='S', inputgame_cell=celula_de_pixel(m, *px))
    return item


def _dist(a, b):
    (ax, ay), (bx, by) = xy(a), xy(b)
    return max(abs(ax - bx), abs(ay - by))


# ---------------------------------------------------------------- extraction
def alvos_unidades(m):
    from incursao_core import caso_unidade
    saida = []
    for i in range(16):
        u = unidade(m, i)
        c = caso_unidade(m, i)['EAX'] & 0xffff
        item = dict(unit=i, owner=u['owner'], type=u['type'], state=u['state'], fields_label='B',
                    enginGetCase=c, cell_plus8=u['cell_plus8'])
        item.update(_alvo_celula(m, c, 'B'))
        saida.append(item)
    return saida


def zona0(m):
    from influencia_missao import zona_influencia
    tabela = m.vista(INFLUENCIA, 4000)
    registro = [m.u16(INFLUENCIA + 2 * k) for k in range(4)]
    celulas = [c for c in range(0x10000) if zona_influencia(tabela, c) == 0]
    return registro, celulas, (lambda c: zona_influencia(tabela, c))


def locais_cave(m, jogador, construtor, zona, n=12):
    """Candidate CAVE build-site clicks: BatimentPosable without EnginOccupeCase, centre in zone 0."""
    w, h = dimensoes_estrutura(m, TIPO_CAVE)
    deslocamento = 0x202                          # BatimentGetDecalageConstruction(3), table 0x41ae4c
    from incursao_core import caso_unidade
    origem_construtor = caso_unidade(m, construtor)['EAX'] & 0xffff
    todos, contagem = [], dict(valid=0, invalid=0, needs_EnginOccupeCase=0)
    centro_rel = (centro_estrutura_hipotetica(m, TIPO_CAVE, 0x0808) - 0x0808) & 0xffff
    for c in range(0x10000):
        x, y = xy(c)
        if x >= m.u16(0x497168) or y >= m.u16(0x49716a):
            continue
        estado, celulas = batiment_posable(m, TIPO_CAVE, c, jogador)
        contagem[estado] += 1
        if estado != 'valid':
            continue
        origem = (c + deslocamento - ((h - 1) << 8) - (w - 1)) & 0xffff
        centro = (origem + centro_rel) & 0xffff
        if zona(centro) != 0:
            continue
        objetos = sorted({objeto(m, cc) for cc in celulas} - {0})
        item = _alvo_celula(m, c, 'S')
        item.update(posable='valid', posable_label='S',
                    footprint_origin=origem, footprint_origin_xy=list(xy(origem)),
                    footprint_xy=[list(xy(celulas[0])), list(xy(celulas[-1]))],
                    batimentGetCase=centro, batimentGetCase_xy=list(xy(centro)), zone=0, placement_label='S',
                    footprint_objects=objetos, chebyshev_to_builder=_dist(c, origem_construtor))
        todos.append(item)
    utilizaveis = [t for t in todos if t['on_screen'] and t['mouse_zone'] == 0 and not t['footprint_objects']]
    utilizaveis.sort(key=lambda t: (t['chebyshev_to_builder'], t['cell']))
    return dict(counts_over_map=contagem, valid_in_zone0=len(todos),
                valid_on_screen_no_objects=len(utilizaveis), candidates=utilizaveis[:n])


def _recursos_terreno():
    """Economy's RecursosTerreno through the shared loader (economy and graphics both ship a flat ``construcoes``)."""
    from integracao.providers import load_economy_resources
    return load_economy_resources().RecursosTerreno


def alvos_comida(m, referencia, n=12):
    RecursosTerreno = _recursos_terreno()
    recursos = RecursosTerreno.da_memoria(m)
    largura, altura = m.u16(0x497168), m.u16(0x49716a)
    campos, sacos, arbustos = [], [], []
    for y in range(altura):
        for x in range(largura):
            c = celula(x, y)
            o = objeto(m, c)
            if terreno_est_gc(m, c):
                if recursos.e_campo(c) != terreno_est_gc(m, c):
                    raise AssertionError('Economy TerrainEstChampi and TerrainEstGc disagree')
                item = _alvo_celula(m, c, 'B')
                item.update(object=o, stage_label='B', chebyshev_to_reference=_dist(c, referencia))
                campos.append(item)
            elif terreno_est_sac(m, c):
                item = _alvo_celula(m, c, 'B')
                item.update(object=o, sac_type=terreno_get_sac_type(m, c),
                            quantity=m.u8(_grade(m, GRADE_QUANTIDADES) + c), chebyshev_to_reference=_dist(c, referencia))
                sacos.append(item)
            elif o == 0x1c:
                arbustos.append(_alvo_celula(m, c, 'B'))
    visiveis = [t for t in campos if t['on_screen'] and t['mouse_zone'] == 0]
    perto = sorted(campos, key=lambda t: (t['chebyshev_to_reference'], t['cell']))
    return dict(field_cells=len(campos), field_cells_on_screen=len(visiveis),
                field_cells_discovered=sum(1 for t in campos if t['caseEstDecouverte']), nearest_fields=perto[:n],
                sacks=sorted(sacos, key=lambda t: t['cell']), bush_cells=[t['cell'] for t in arbustos])


def alvos_pedra(m):
    RecursosTerreno = _recursos_terreno()
    recursos = RecursosTerreno.da_memoria(m)
    minas = []
    for i in range(20):
        origem, reserva = m.u16(MINAS + 4 * i), m.u16(MINAS + 4 * i + 2)
        if not origem:
            continue
        celulas = [(origem + d) & 0xffff for d in (0, 1, 0x100, 0x101)]
        if any(recursos.indice_mina(c) != i for c in celulas) or recursos.capacidade_mina(i) != reserva:
            raise AssertionError('Economy MineGetIndice/MineGetCapacite disagree with the mine table')
        minas.append(dict(index=i, origin=origem, origin_xy=list(xy(origem)), reserve=reserva, label='B',
                          cells_mineGetIndice=celulas,
                          clickable_cells_terrainEstMine=[_alvo_celula(m, c, 'B') | dict(tile=f'0x{tile(m, c):x}')
                                                          for c in celulas if terreno_est_mine(m, c)]))
    largura, altura = m.u16(0x497168), m.u16(0x49716a)
    ladrilhos = [celula(x, y) for y in range(altura) for x in range(largura) if terreno_est_mine(m, celula(x, y))]
    sacos = [celula(x, y) for y in range(altura) for x in range(largura) if terreno_get_sac_type(m, celula(x, y)) == 2]
    return dict(mines=minas, terrainEstMine_cells=ladrilhos, stone_sacks=sacos)


def extrair():
    m, fonte = carregar_quadro128()
    m1, fonte_m1 = carregar_m1()
    ancoras = verificar_ancoras()
    jogador = m.u8(JOGADOR_LOCAL)
    v = vista(m)
    primeira, ultima, zonas = zonas_mouse(m)
    nomes_zonas = {1: 'edge top-left', 2: 'edge top', 3: 'edge top-right', 4: 'edge right', 5: 'edge bottom-right',
                   6: 'edge bottom', 7: 'edge bottom-left', 8: 'edge left', 9: 'empty (0,0,0,0)', 10: 'minimap',
                   11: 'HUD panel (IconeGetZone inside)', 26: 'contact panel', 27: 'message box',
                   28: 'alliance 0', 29: 'alliance 1', 30: 'alliance 2', 31: 'alliance 3'}

    unidades = alvos_unidades(m)
    unidades_m1 = alvos_unidades(m1)
    por_indice = {u['unit']: u for u in unidades}
    construtor = por_indice[12]

    saco = saco_ordens(m, 12)
    icones = retangulos_icones(m)
    cave_icone = None
    for e in saco['entries']:
        slot = e['index'] - saco['scroll']
        if e['code'] == 3 and e['type'] == TIPO_CAVE and 0 <= slot < 4:
            x0, y0, x1, y1 = icones[slot]
            centro = ((x0 + x1) // 2, (y0 + y1) // 2)
            cave_icone = dict(bag_index=e['index'], slot=slot, rect_inclusive=[x0, y0, x1, y1],
                              center_pixel=list(centro), mouse_zone_at_center=zona_mouse(m, *centro),
                              iconeGetZone_at_center=icone_em(m, *centro), label='B (rect, bag bytes); S (that a click reaches it)')

    custo = custo_estrutura(m, TIPO_CAVE)
    estoque0 = estoque(m, jogador)
    registro_zona0, celulas_zona0, zona = zona0(m)
    santuario_centro = __import__('chamadas_quadro_core').caso_estrutura(m, 0)['EAX'] & 0xffff
    sites = locais_cave(m, jogador, 12, zona)
    proposto = sites['candidates'][0] if sites['candidates'] else None
    comida = alvos_comida(m, por_indice[13]['cell'])
    pedra = alvos_pedra(m)

    def _difs():
        difs = []
        for a, b in zip(unidades_m1, unidades):
            for k in ('owner', 'type', 'state', 'cell'):
                if a[k] != b[k]:
                    difs.append(dict(unit=a['unit'], field=k, m1=a[k], frame128=b[k]))
        for nome, f in (('view', vista), ('stock_player0', lambda mm: estoque(mm, jogador)),
                        ('cave_cost', lambda mm: custo_estrutura(mm, TIPO_CAVE)),
                        ('builder_bag', lambda mm: saco_ordens(mm, 12)['entries']),
                        ('mouse_zones', lambda mm: zonas_mouse(mm)[2])):
            a, b = f(m1), f(m)
            if json.dumps(a, sort_keys=True, default=list) != json.dumps(b, sort_keys=True, default=list):
                difs.append(dict(item=nome, m1=json.loads(json.dumps(a, default=list)), frame128=json.loads(json.dumps(b, default=list))))
        for i in range(20):
            if m1.ler(MINAS + 4 * i, 4) != m.ler(MINAS + 4 * i, 4):
                difs.append(dict(item=f'mine {i}'))
        objetos = [c for c in range(0x10000) if objeto(m1, c) != objeto(m, c)]
        if objetos:
            difs.append(dict(item='object grid cells changed', cells=objetos))
        return difs

    alvo_pedra = pedra['mines'][0]['clickable_cells_terrainEstMine'][0] if pedra['mines'] else None
    resultado = dict(
        schema=SCHEMA,
        scope='MONDE01 M3 Step 0 (docs/M3_PLAN.md section 2): static targets for P1-P5 and S1. No emulation; '
              'nothing here claims that a branch runs.',
        labels=dict(B='read from accepted state bytes (frame-128 checkpoint / M1) or an instruction encoding of the intact executable',
                    S='inferred: a translation run over those bytes, a reachability/ordering claim, or a preference'),
        sources=dict(frame128=fonte, m1=fonte_m1,
                     executable=dict(sha256=HASH_EXECUTAVEL, anchors=ancoras,
                                     anchors_status='verified' if ancoras and all(a['verified'] for a in ancoras)
                                     else ('executable not available' if ancoras is None else 'MISMATCH'))),
        view=dict(state_label='B', origin=list(v['origin']), viewport_cells=list(v['size']), screen=list(v['screen']),
                  panel_offset=v['panel_offset'], local_player=jogador,
                  mapping='cell (x,y) = (cell mod 256, cell div 256); screen pixel = (32(x-vx)+16, 32(y-vy)+16); '
                          'with view origin (0,0): (32x+16, 32y+16)',
                  mapping_label='S',
                  mapping_byte_evidence='InputGame 0x429800..0x42984a encodes cell = ((Y>>5)+[0x508722])<<8 + (X>>5)+[0x508720] '
                                        'for MouseZone result 0 (dispatch 0x42c2a5), guard 0x42984c..0x4298c6 '
                                        'd*32 <= X < (vw-d)*32, d*32 <= Y < (vh-d)*32 with d = s8 [0x508f90]. '
                                        'Encoding B; that a click reaches it is S.',
                  playfield_pixels=[0, 0, 32 * v['size'][0] - 1, 32 * v['size'][1] - 1]),
        mouse_zones=dict(label='B (frame-128 table bytes; MouseSetZone writers are InitGameZone, InitZoneMarche, '
                               'MarcheRestoreZone, AffIconeSousCurseur, CalculMarcheProposition only)',
                         table=f'0x{ZONAS_MOUSE:x}', tested_range=[primeira, ultima],
                         zones=[dict(zone=i, rect_inclusive=list(zonas[i]), name=nomes_zonas.get(i, 'unused (12..25 never set by InitGameZone mode 1)'))
                                for i in range(1, ultima + 1)],
                         builder_selection_effect='S: InitGameZone mode 1 (the in-game layout) reads screen size, minimap flag/position, '
                                                  'viewport, panel offset, contact/message-box/alliance state; not the selection. '
                                                  'Selecting the builder therefore adds no MouseSetZone rectangle; the action icons '
                                                  'are hit-tested by IconeGetZone inside zone 11.',
                         action_icons=dict(label='B (IconeGetZone 0x45da4e constants; screen width 800 -> y0 = 0x224)',
                                           rects_inclusive={str(k): list(r) for k, r in icones.items()},
                                           selection_rule='InputGame 0x42bcd9: icons index the bag of the selected structure '
                                                          '(BatimentGetSelection) or, when exactly one unit is selected '
                                                          '(EnginGetNbSelection == 1), that unit\'s EnginGetBagOrdre; icon slot s '
                                                          'reads bag entry bag[+4] + s (BagGetCode +0x42, BagGetType +6).'),
                         unavailable_minimap_cells='S: centre pixels of cells with x-vx <= 3 and y-vy <= 3 fall in zone 10 (minimap)'),
        units=dict(targets=[por_indice[i] for i in UNIDADES_ALVO], all=unidades,
                   hit_test='B encoding: InputGame 0x429ae3 hovers the unit ChercheIndiceEngin(cell) at the clicked cell; '
                            'the selection producers 0x42b9aa/0x42ba20 were not traced here (open)'),
        builder_bag=dict(unit=12, label='B (frame-128 bag bytes)', **saco),
        cave_icon=cave_icone,
        cave_icon_click=dict(label='B encoding, S reachability',
                             effect='code 3 entry -> BatimentGetRessource(type) then TestRessource(player, food, stone, 0); '
                                    'on success with type != 0x14: u16 0x4e05ae := 3, u8 0x496207 := type (0x42c1e6..0x42c1f5)',
                             requires='u8 0x5099ae and u8 0x5099af both nonzero in the same InputGame pass',
                             predicted_0x496207=TIPO_CAVE if cave_icone else None,
                             test_ressource_passes=estoque0['food'] >= custo['food'] and estoque0['stone'] >= custo['stone']),
        cave=dict(type=TIPO_CAVE, dims=list(dimensoes_estrutura(m, TIPO_CAVE)), dims_label='B',
                  cost=custo, cost_label='B (table 0x495d98 + 52*type, read by BatimentGetRessource and CreerBatiment)',
                  construction_offset='0x202', construction_offset_label='B (BatimentGetDecalageConstruction table entry 3 -> 0x41aec1)',
                  placement='S: CalculConstruireBatiment builds when unit +8 == +0xb2 (the clicked cell), at cell +8 + 0x202 '
                            '(CreerBatiment reference = bottom-right); origin = reference - (w-1) - (h-1)*256, i.e. the 5x5 '
                            'footprint centred on the clicked cell, the same footprint BatimentPosable tests at the click.',
                  owner_after_creation='B: CreerBatiment stores owner +4 = 0xc8 (0x4200b5); only types 0x11 (0x4200c8) and 9/0xc '
                                       '(0x420295) get the player byte there. The only store found that turns a 0xc8 owner into '
                                       'a player is BatimentLogeEngin 0x41fa77 (symbol-bounded linear scan, not exhaustive).'),
        stock=dict(player=jogador, label='B', **estoque0,
                   victory_needs=dict(food=50, stone=50, label='B (records 1, 2, 9 at 0x4e1d20)'),
                   after_cave_cost=dict(food=estoque0['food'] - custo['food'], stone=estoque0['stone'] - custo['stone'], label='S'),
                   to_gather_after_cave=dict(food=50 - (estoque0['food'] - custo['food']),
                                             stone=50 - (estoque0['stone'] - custo['stone']),
                                             label='S (assumes no other expense or income before victory)')),
        zone0=dict(record=registro_zona0, record_label='B', cells=len(celulas_zona0),
                   rect_xy=[[registro_zona0[0], registro_zona0[1]], [registro_zona0[2], registro_zona0[3]]],
                   sanctuary=dict(structure=0, origin=m.u16(ESTRUTURAS + 2), origin_xy=list(xy(m.u16(ESTRUTURAS + 2))),
                                  dims=list(dimensoes_estrutura(m, m.u8(ESTRUTURAS + 8))), batimentGetCase=santuario_centro,
                                  batimentGetCase_xy=list(xy(santuario_centro)), zone=zona(santuario_centro), label='B state, S zone query')),
        cave_sites=dict(rule='S: BatimentPosable 0x41fc40 (type 3, player 0) without EnginOccupeCase; footprint free of '
                             'collision bit 0, every cell TerrainEstHerbe and TerrainEstDecouvert; Core BatimentGetCase of the '
                             'resulting record in zone 0; candidates also on screen, MouseZone 0 and with no object in the '
                             'footprint (preference, keeps fields/sacks); sorted by Chebyshev distance to unit 12.',
                        **sites, proposed=proposto),
        food=dict(rule='B encoding: InputGame 0x42b311: with troops selected, a TerrainEstGc cell (object 0x1d..0x34), a food '
                       'sack (TerrainGetSacType 1) or a hovered CAVE, and EnginTravailSelectionne(player, 1) (every selected '
                       'live unit of type 5 or 13); click: TerrainEstGc -> tag 7 at 0x42b486 (BX = cell), otherwise tag 0x12.',
                  view_for_nearest_field=vista_para(m, comida['nearest_fields'][0]['cell'], por_indice[13]['cell'])
                  if comida['nearest_fields'] else None,
                  **comida),
        stone=dict(rule='B encoding: InputGame 0x42b4b5: TerrainEstMine (tile 0x251/0x252/0x255/0x256), a stone sack '
                        '(TerrainGetSacType 2) or a hovered CAVE, and EnginTravailSelectionne(player, 2) (every selected live '
                        'unit of type 7); click: TerrainEstSac -> tag 0x12, otherwise tag 6 via 0x42ad8e.',
                   view_for_first_mine_cell=vista_para(m, alvo_pedra['cell'], construtor['cell']) if alvo_pedra else None,
                   **pedra),
        undiscovered_cell_gate=dict(
            label='B encoding and frame-128 bytes; S reachability',
            rule='InputGame 0x4298d9: a playfield click on a cell with CaseEstDecouverte(cell, local) == 0 (discovery & 0x10 '
                 'set) skips the sack/field/mine classification unless 0x4e05ae is 5 or 0xd or u8 0x496208 is 0; with troops '
                 'selected and 0x4e05ae == 0 it issues tag 5 (move) to that cell (0x429973 -> 0x42aecf).',
            frame128_0x496208=m.u8(0x496208), frame128_0x4e05ae=m.u16(0x4e05ae),
            consequence='S: every field cell and both mine cells are undiscovered for player 0 at frame 128, so a click on '
                        'them moves the selected units instead of ordering a harvest or a mine; the units must first reveal '
                        'the target cell.'),
        minimap=dict(label='B encoding (InputGame 0x42bade, MiniMapGetCenterSelect 0x46a273, MiniMapGetCase 0x46a224), S use',
                     rect=list(zonas.get(10, (0, 0, 0, 0))),
                     press_rule='u8 0x5099ae set (a WM_LBUTTONDOWN; no release needed) with MouseZone 10: troops selected -> '
                                'tag 5 move to MiniMapGetCase(X-mmx, Y-mmy); nothing selected -> view origin := '
                                'MiniMapGetCenterSelect(X-mmx, Y-mmy). Right button (0x5099b1) locks/drags the minimap.',
                     center_formula='vx = (mx - (vw*mmw/mapw)/2) * mapw / mmw, vy likewise (C division), clamped to '
                                    '[0, map - viewport]; with 128x128 minimap, 64x64 map, 25x17 view: vx = (mx-25)/2, vy = (my-17)/2'),
        input_semantics=dict(label='B encoding, S ordering within a frame',
                             wndproc='0x200 -> u16 0x5099a8 = LOWORD(lParam), 0x5099aa = HIWORD; 0x201 -> 0x5099ae = 1; '
                                     '0x202 -> 0x5099af = 1; 0x203 (double click) -> 0x5099b0 = 1 if Y < vh*32 else 0x5099ae = 1; '
                                     '0x204 -> 0x5099b1 = 1; 0x205 -> 0x5099b2 = 1',
                             clear='ProgIteration 0x475068: after AffGame, if 0x5099af then 0x5099af = 0x5099ae = 0',
                             click_test='the icon, build-site, harvest and mine clicks test 0x5099ae && 0x5099af in one '
                                        'InputGame pass; with DOWN at k+1 and UP at k+3 both are set from k+3 until the clear',
                             cursor='ProgIteration stores u16 0x5099aa before CalculGame (0x475058), so the GetCursorPos answer '
                                    'must hold the point while the click is tested',
                             deselect='InputGame 0x4295a1: u8 0x5099b1 (WM_RBUTTONDOWN) with MouseZone != 11 -> DeSelectionGroupe, '
                                      'BatimentDeselectionner, 0x4e05ae := 0, 0x496207 := 0xff'),
        m1_vs_frame128=_difs(),
    )
    resultado['open_questions'] = questoes_abertas(resultado)
    return resultado


def questoes_abertas(r):
    """M3_PLAN section 2 'Uncertain until it runs': what this static data narrows; nothing here is a native result."""
    cave, ic, est = r['cave'], r['cave_icon'], r['stock']
    sitio = r['cave_sites']['proposed']
    return [
        dict(question='whether the CAVE icon sets 0x496207 to 3, and its screen rectangle', status='narrowed',
             static=f"unit 12 bag at frame 128: {[(e['type'], e['code']) for e in r['builder_bag']['entries']]} "
                    f"(type, code), scroll {r['builder_bag']['scroll']}; CAVE = slot {ic['slot']}, rect {ic['rect_inclusive']}, "
                    f"centre {ic['center_pixel']} [B]. Code-3 click stores 0x4e05ae = 3 and 0x496207 = BagGetType = 3 after "
                    f"TestRessource({cave['cost']['food']}, {cave['cost']['stone']}, 0) [B encoding], which passes at 30/30 [S].",
             remains='that the press reaches 0x42c1f5 with exactly one unit selected and 0x5099ae/0x5099af both set (P3)'),
        dict(question='the cave cost, and therefore the real food/stone targets', status='narrowed',
             static=f"cost food {cave['cost']['food']}, stone {cave['cost']['stone']}, parts {cave['cost']['parts']} [B]; "
                    f"CreerBatiment tests the same words and charges EnleveMatiere(1, food), EnleveMatiere(2, stone) [B encoding]; "
                    f"after paying {est['after_cave_cost']['food']}/{est['after_cave_cost']['stone']}, so "
                    f"{est['to_gather_after_cave']['food']} food and {est['to_gather_after_cave']['stone']} stone to gather [S].",
             remains='any other expense or income before victory'),
        dict(question="placement validity and zone 0's extent", status='zone settled from bytes; placement narrowed',
             static=f"zone 0 = record {r['zone0']['record']} ({r['zone0']['cells']} cells) [B]; sanctuary BatimentGetCase "
                    f"{r['zone0']['sanctuary']['batimentGetCase_xy']} is in zone 0 [S]. BatimentPosable without EnginOccupeCase: "
                    f"{r['cave_sites']['counts_over_map']} over the map; {r['cave_sites']['valid_in_zone0']} valid with the cave's "
                    f"BatimentGetCase in zone 0; proposed click {sitio['xy']} -> footprint {sitio['footprint_xy']}, "
                    f"BatimentGetCase {sitio['batimentGetCase_xy']} [S].",
             remains='the builder reaching the cell, BatimentConstructible at build time (its own cell needs EnginOccupeCase), '
                     'and any discovery/collision change before the click'),
        dict(question='whether a cave under construction already passes record 0 (BatimentExiste + type)', status='narrowed',
             static='CreerBatiment stores state +5 = 2 and type +8 at once but owner +4 = 0xc8 for type 3 [B encoding]; '
                    'record 0 requires owner == player 0 [B, fim_missao]; the only store found that turns a 0xc8 owner into '
                    'a player is BatimentLogeEngin 0x41fa77, followed by BatimentHabitable [B encoding, scan not exhaustive]. '
                    'So a freshly created cave should fail record 0 until a unit lodges in it [S].',
             remains='which event lodges a unit in the new cave, and when (P3/S1)'),
        dict(question='which unit type mines stone, and whether colonists must leave the sanctuary', status='narrowed',
             static='EnginTravailSelectionne 0x47248f requires every selected live unit to be type 7 for resource 2 (stone), '
                    'type 5 or 13 for resource 1 (food), type 6 for resource 0 [B encoding]. MONDE01 has one type 7 (unit 12, '
                    'the builder); units 13/14 are type 5; units 11 (type 1), 15 (type 8) and the colonists (type 9) cannot '
                    'take these orders through this UI path [S].',
             remains='that the mine cycle credits stone to the player totals (P5)'),
        dict(question='the tag-8 producer', status='narrowed',
             static='InputGame 0x429d61/0x429d7a (mode-9 table 0x42923c, entry 0x4e05b0 == 2: the first resource press was a '
                    'sack). Mode 9 is stored only on branches that test mode 8 (0x42ad08, 0x42b3d5, 0x42b55d, 0x42b6f1), and the only store of 8 to 0x4e05ae found is 0x429629, reached while GetAsyncKeyState(VK_CONTROL) < 0 [B encoding]. '
                    'Without keys S1 issues tag 7 (field) or tag 6 (mine) directly [S].',
             remains='whether a deposit order is needed at all (CalculWorkEngin/CalculTransporteEngin behaviour)'),
        dict(question='whether TestRessource reads player totals only', status='settled as an encoding',
             static='TestRessource 0x4676e5 compares AX <= u16 [0x4e2eb2+32p], DX <= [0x4e2eba+32p], BX <= [0x4e2eaa+32p] '
                    '(player record 0x4e2ea8+32p: +0xa food, +0x12 stone, +2 parts) and reads nothing else [B].',
             remains='how harvested goods reach those totals'),
        dict(question='whether victory comes before frame 9000', status='open',
             static=f"targets are far: the nearest field {r['food']['nearest_fields'][0]['xy']} is "
                    f"{r['food']['nearest_fields'][0]['chebyshev_to_reference']} cells from unit 13, mine 0 at "
                    f"{r['stone']['mines'][0]['origin_xy']} (reserve {r['stone']['mines'][0]['reserve']}) is outside the start "
                    f"view, and every field and mine cell is undiscovered for player 0 at frame 128 [B]; no timing follows "
                    f"statically.",
             remains='S1'),
    ]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--saida', default=str(SAIDA))
    args = parser.parse_args(argv)
    resultado = extrair()
    texto = json.dumps(resultado, indent=1, sort_keys=False) + '\n'
    Path(args.saida).write_text(texto)
    print(f'wrote {args.saida} ({len(texto)} bytes); anchors: {resultado["sources"]["executable"]["anchors_status"]}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
