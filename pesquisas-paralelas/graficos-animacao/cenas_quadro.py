"""Deterministic AffGame frame inputs: the committed MONDE01 checkpoint and
bounded scenes derived from its real terrain. Pure Python; no x86.

Every value that does not come from the original or a committed provider is
named in the scene's 'sinteticos' list.
"""
import hashlib
import json
import struct
import sys
from extrair_evidencias import RAIZ

MISSOES = RAIZ.parent/'missoes'
# AffBatiments terrain switch 0x40F23B..0x40F342 plus AffVehiculeAtelier 0x402880.
GATILHOS_FACHADA = (0x2cb, 0x2ed, 0x2fb, 0x30d, 0x326, 0x343, 0x35e, 0x37a, 0x388, 0x390, 0x398,
    0x3b0, 0x3ce, 0x3e1, 0x3f8, 0x406, 0x40e, 0x42a, 0x436)
OFICINA = 0x356
# AffVeget 0x415A58 table: these codes reach a handler.
CODIGOS_AFFVEGET = (65, 64, 63, 62, 61, 60, 59, 58, 57, 56, 55, 27, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1)
# (name, address, width) of every AffGame-prefix global, in address order.
GLOBAIS = (
    ('rng_u8', 0x4e1d18, 1), ('evento_u8', 0x4e1b0e, 1), ('pitch_u32', 0x4e17a0, 4),
    ('dd_ponteiro_u32', 0x4e17a4, 4), ('dd_travas_u32', 0x4e17a8, 4), ('fps_contador_u16', 0x4e17ae, 2),
    ('fps_ultimo_tick_u32', 0x4e17b0, 4), ('fps_tick_u32', 0x4e17b4, 4), ('caixa_selecao_u8', 0x4e19b0, 1),
    ('forcar_desenho_u8', 0x4e05a2, 1), ('modo_jogo_u8', 0x4e2f78, 1), ('fps_digitos', 0x496394, 3),
    ('paginas_texto', 0x4963b4, 4), ('selecionada_unidade_u16', 0x496ac2, 2),
    ('selecionada_estrutura_u16', 0x496ac4, 2), ('divisor_u8', 0x497284, 1), ('largura_tela_u16', 0x49a018, 2),
    ('altura_tela_u16', 0x49a01a, 2), ('recorte', 0x49a01c, 8), ('recorte_salvo', 0x49a02c, 8),
    ('restaurar_fundo_u8', 0x49a041, 1), ('paginas_u8', 0x49a05b, 1), ('camera_u8', 0x508041, 1),
    ('origem', 0x508720, 4), ('janela', 0x508724, 4), ('superficie_u32', 0x508f70, 4),
    ('quadro_u32', 0x508f7c, 4), ('modo_selecao_u8', 0x508f8f, 1), ('margem_i8', 0x508f90, 1),
    ('limpar_u8', 0x508f92, 1))


def sha(dados): return hashlib.sha256(bytes(dados)).hexdigest()


def empacotar(nome, valor):
    largura = next(w for n, a, w in GLOBAIS if n == nome)
    if isinstance(valor, int): return valor.to_bytes(largura, 'little', signed=nome.endswith('_i8') and valor < 0)
    if len(valor) != largura: raise ValueError('Global width mismatch: '+nome)
    return bytes(valor)


def globais_base(**mudancas):
    """800x600 mode (DDInit 0x43F519): 25x17 cells, pitch 800, ResetMode clip."""
    margem = mudancas.get('margem_i8', 0); w, h = 25, 17
    valores = dict(rng_u8=0, evento_u8=0, pitch_u32=800, dd_ponteiro_u32=0, dd_travas_u32=0, fps_contador_u16=7,
        fps_ultimo_tick_u32=1000, fps_tick_u32=1000, caixa_selecao_u8=0, forcar_desenho_u8=0, modo_jogo_u8=0x12,
        fps_digitos=b'00\0', paginas_texto=b'1\0\0\0', selecionada_unidade_u16=0xffff, selecionada_estrutura_u16=0xffff,
        divisor_u8=1, largura_tela_u16=800, altura_tela_u16=600,
        recorte=struct.pack('<4H', margem*32, h*32-1-margem*32, margem*32, w*32-1-margem*32), recorte_salvo=bytes(8),
        restaurar_fundo_u8=0, paginas_u8=1, camera_u8=0, origem=struct.pack('<HH', 0, 0), janela=struct.pack('<HH', w, h),
        superficie_u32=0, quadro_u32=0, modo_selecao_u8=0, margem_i8=margem, limpar_u8=0)
    valores.update(mudancas)
    if 'margem_i8' in mudancas and 'recorte' not in mudancas:
        valores['recorte'] = struct.pack('<4H', margem*32, h*32-1-margem*32, margem*32, w*32-1-margem*32)
    return {n: empacotar(n, valores[n]) for n, a, w in GLOBAIS}


def mundo_monde01():
    """Committed missions checkpoint: MONDE01 load and unit placement until the
    named DecouvreTerrain stop at unit 15, with earlier effects retained."""
    if str(MISSOES) not in sys.path: sys.path.insert(0, str(MISSOES))
    import ambiente_missoes  # noqa: F401 (committed provider path bootstrap)
    from capturar_terreno_unidades import preparar_caso
    from terreno_unidades import preparar_unidades_no_terreno, provedores_terreno_core
    from carregador_unidades import carregar_unidades_missao
    from formatos import Leitor
    from bonus_unidades import BonusUnidades
    mundo, dados, deslocamento, tipos, bonus, carregador = preparar_caso('MONDE01')
    provedor = BonusUnidades(bonus)
    carregar_unidades_missao(Leitor(dados, deslocamento), mundo.unidades, carregador, tipos, mundo.selecoes_unidades,
        modificador12=lambda dono, tipo: provedor.consultar(dono, tipo, 12))
    parada = None
    try:
        preparar_unidades_no_terreno(provedores_terreno_core(mundo, bonus_unidades=provedor))
    except NotImplementedError as erro:
        parada = f'{type(erro).__name__}: {erro}'
    return dict(terreno=struct.pack('<65536H', *mundo.tiles), objetos=bytes(mundo.objetos),
        auxiliares=bytes(mundo.donos_objetos), atributos=bytes(mundo.atributos),
        regioes=struct.pack('<65536H', *mundo.regioes), unidades=bytes(mundo.unidades),
        descoberta=[bytes(g) for g in mundo.descoberto], iluminacao=[bytes(g) for g in mundo.luz_bordas],
        contagem_luz=[bytes(g) for g in mundo.contagem_luz], parada_missao=parada, eta_sha256=sha(dados))


def cena_monde01(base):
    """Real checkpoint buffers; camera/viewport and runtime globals declared."""
    return dict(nome='monde01_checkpoint', mundo=dict(base, projeteis=bytes(5600), estruturas=bytes(276000)),
        globais=globais_base(), ticks=[1500], antes='InitCache',
        sinteticos=['viewport origin (0,0), camera 0, frame counter 0, divisor 1 and the 800x600 mode are declared',
            'missions declare a 0xA5 unit-pool pre-fill, regions [1]*65536, a selection pattern, a search context and a 0x31 bonus table',
            'projectile pool and structure pool are zero: ProjectileReset/structure copy are not composed by the checkpoint',
            'surface starts from a declared background pattern; DirectDraw locks one fixture buffer'])


def _sanear(base):
    terreno = bytearray(base['terreno'])
    for celula in range(65536):
        if struct.unpack_from('<H', terreno, celula*2)[0] in GATILHOS_FACHADA+(OFICINA,):
            struct.pack_into('<H', terreno, celula*2, 300)
    objetos = bytearray(base['objetos']); auxiliares = bytearray(base['auxiliares'])
    for celula in range(65536):
        if objetos[celula] in (27, 253, 254) or 55 <= objetos[celula] <= 65: objetos[celula] = 0
        if 1 <= objetos[celula] <= 11 and auxiliares[celula] > 3: auxiliares[celula] &= 3
    return bytes(terreno), bytes(objetos), bytes(auxiliares)


def _mapas(semente, descobertos):
    descoberta, iluminacao = [], []
    for camera in range(4):
        d = bytearray(65536); l = bytearray(65536)
        for celula in range(65536):
            h = (celula*2654435761+(semente+camera)*40503) & 0xffffffff
            d[celula] = (0, 0, 0, 1, 2, 3, 4, 8, 9, 12, 15, 0xe0, 16, 0x30)[(h >> 9) % 14] if descobertos else 16
            l[celula] = (0, 0, 16, 1, 2, 4, 8, 15, 0xe0, 0x10, 3)[(h >> 17) % 11]
        descoberta.append(bytes(d)); iluminacao.append(bytes(l))
    return descoberta, iluminacao


def unidade_sintetica(registro_inicial, *, celula, estado, direcao, fase, prioridade, bolsa_u16=0, dx=0, dy=0):
    r = bytearray(registro_inicial)
    r[2] = estado; struct.pack_into('<H', r, 8, celula); r[0x91] = direcao; r[0xa4] = fase; r[0xab] = prioridade
    struct.pack_into('<H', r, 0xa, bolsa_u16); r[0x86] = dx & 255; r[0x87] = dy & 255
    struct.pack_into('<H', r, 0x74, 100)
    return bytes(r)


def projetil_sintetico(tipo, *, x, y, fase=0, direcao=0, ativo=1):
    r = bytearray(56); r[0] = tipo; r[2] = ativo; struct.pack_into('<HH', r, 0xc, x, y); r[0x18] = fase; r[0x22] = direcao
    return bytes(r)


def cenas_sinteticas(base, registros_iniciais):
    """Bounded scenes inside committed renderer domains, on real MONDE01 terrain."""
    terreno, objetos, auxiliares = _sanear(base)
    descoberta, iluminacao = _mapas(17, True)
    vazio = dict(terreno=terreno, objetos=objetos, auxiliares=auxiliares, atributos=base['atributos'],
        regioes=struct.pack('<H', 1)*65536, unidades=bytes(220800), projeteis=bytes(5600), estruturas=bytes(276000),
        descoberta=descoberta, iluminacao=iluminacao, contagem_luz=[bytes(65536)]*4)
    unidades = bytearray(220800); indice = 0
    for i, (tipo, x, y, estado, prioridade) in enumerate(((0, 7, 15, 2, 0), (5, 12, 16, 7, 1), (6, 14, 16, 2, 0), (7, 17, 16, 7, 0),
            (9, 9, 16, 2, 1), (0, 8, 18, 7, 0), (5, 3, 4, 2, 0), (9, 20, 10, 7, 0), (6, 23, 14, 2, 1), (7, 1, 1, 2, 0))):
        registro = unidade_sintetica(registros_iniciais[tipo], celula=y*256+x, estado=estado, direcao=1+(i*5) % 16,
            fase=i % 8, prioridade=prioridade, bolsa_u16=(0 if i % 2 else 3) if tipo in (5, 9) else 0, dx=(i % 3)-1, dy=(i % 2)*2)
        unidades[(3+indice*37)*276:(4+indice*37)*276] = registro; indice += 1
    projeteis = bytearray(5600)
    for i, (tipo, x, y) in enumerate(((1, 200, 300), (6, 420, 210), (14, 610, 120), (7, 333, 444), (20, 90, 500))):
        projeteis[i*56:(i+1)*56] = projetil_sintetico(tipo, x=x, y=y, fase=i % 4)
    comuns = ['viewport/camera/frame/divisor globals and the 800x600 mode are declared',
        'MONDE01 terrain words equal to AffBatiments facade triggers or 0x356 are replaced by 300; object codes 27, 55..65, 253, 254 removed; tree auxiliaries masked to 0..3',
        'visibility maps are a deterministic synthetic pattern; regions [1]*65536; no structures',
        'units are native EnginInit records with state/cell/direction/phase/priority/bag/offsets and +0x74=100 set',
        'projectiles are synthetic 56-byte records of committed renderer types',
        'surface starts from a declared background pattern; DirectDraw locks one fixture buffer']
    cenas = [
        dict(nome='terreno_e_objetos', mundo=vazio, globais=globais_base(), ticks=[2100], antes='InitCache', sinteticos=comuns),
        dict(nome='unidades_e_projeteis', mundo=dict(vazio, unidades=bytes(unidades), projeteis=bytes(projeteis)),
            globais=globais_base(quadro_u32=4, rng_u8=77), ticks=[2140], antes=None, sinteticos=comuns),
        dict(nome='margem_e_origem', mundo=dict(vazio, unidades=bytes(unidades), projeteis=bytes(projeteis)),
            globais=globais_base(margem_i8=1, origem=struct.pack('<HH', 2, 3), camera_u8=0, quadro_u32=9,
                fps_ultimo_tick_u32=1200), ticks=[2300], antes=None, sinteticos=comuns),
        dict(nome='nao_desenhado_divisor', mundo=vazio, globais=globais_base(divisor_u8=3, quadro_u32=7), ticks=[2310],
            antes=None, sinteticos=comuns),
        dict(nome='forcado_e_evento', mundo=dict(vazio, unidades=bytes(unidades)),
            globais=globais_base(divisor_u8=3, quadro_u32=7, forcar_desenho_u8=1, evento_u8=1, fps_contador_u16=140,
                fps_ultimo_tick_u32=1000), ticks=[2400], antes=None, sinteticos=comuns),
        dict(nome='reinicio_cache', mundo=vazio, globais=globais_base(origem=struct.pack('<HH', 40, 30), quadro_u32=12),
            ticks=[2500], antes='InitCache', sinteticos=comuns),
    ]
    return cenas


def fundo():
    return bytes((i*17+23) % 256 for i in range(800*600))


def resumo_mundo(mundo):
    saida = {}
    for nome, valor in mundo.items():
        if isinstance(valor, list): saida[nome] = [sha(v) for v in valor]
        elif isinstance(valor, (bytes, bytearray)): saida[nome] = sha(valor)
        else: saida[nome] = valor
    return saida
