"""Original-only captures of the live attack chain over one shared Core world.

Real loaded inputs: the 26x50 type table and DEGAT rows that core's committed
`regras` rebuilds from the original RISING.EXE/RISING.INI. Declared synthetic
inputs: map, positions, owners, life, order fields, zero bonus table, players
table, discovery bytes and the frame counter. Units are created with combat's
committed EnginSetType translation. Writes
`evidencias/captura-ataque-vivo-original.json`; imports no Stage 18 module.
"""
import hashlib
import json
from pathlib import Path
import struct
import sys

import consumo_dano  # noqa: F401  (establishes the committed Core import path)
from navegacao_unidades import MundoNavegacao
from regras import extrair_regras
from extrair_evidencias import HASH, ler_imagem
from inicializacao_ataque import CaracteristicasTipo, definir_tipo
from animacao_disparo import BuscaAtaque
from projeteis import PoolProjeteis

PASTA = Path(__file__).resolve().parent
REPO = PASTA.parents[1]
sys.path.insert(0, str(REPO / 'pesquisas-paralelas/economia'))
from bonus_unidades import BonusUnidades, capacidade_tipo  # noqa: E402

CONTADOR_BASE = 1000  # declared frame counter at u32 0x508f7c, frame k uses base+k
ATACANTE, VITIMA, ESTRUTURA = 5, 9, 7
AREAS = ('unidades', 'estruturas', 'grupos', 'objetos', 'atributos', 'regioes', 'tiles', 'donos_objetos',
         'mini_final', 'mini_unidades', 'mini_estruturas', 'descoberto', 'luz_bordas', 'contagem_luz',
         'sombra', 'rotas', 'projeteis', 'busca', 'iteracao', 'alerta')


def _duelo(atacante, vitima, quadros, **extra):
    return dict(tipo='duelo', atacante=atacante, vitima=vitima, quadros=quadros, **extra)


def _a(dono, tipo, celula=0x2828):
    return dict(indice=ATACANTE, dono=dono, tipo=tipo, celula=celula, direcao=5)


def _v(dono=0, tipo=0, celula=0x2829, vida=None):
    return dict(indice=VITIMA, dono=dono, tipo=tipo, celula=celula, direcao=13, vida=vida)


CENARIOS = {
    # Complete chains: neutral monster attacker, human victim, local player 3 sees nothing.
    'melee-monster-to-death': _duelo(_a(200, 20), _v(), 900),
    'ranged-monster-to-death': _duelo(_a(200, 18), _v(celula=0x282e), 900),
    # Named stops reached by the same chain.
    'diplomacy-stop-ai-attacker': _duelo(_a(1, 18), _v(celula=0x282e), 400, controle=(1, 2, 1, 1)),
    'audio-stop-visible-attacker': _duelo(_a(200, 20), _v(), 200, local=0, visivel=(0, 0x2828)),
    'level-stop-soldier-kill': _duelo(_a(200, 0), _v(vida=15), 200),
    # Single branch entries from declared order fields (+2=1, +8a=0, +b7, +b8).
    'branch-mode1-target-dying': dict(tipo='ramo', ordem=(1, VITIMA), alvo=dict(estado=4)),
    'branch-mode1-target-owner200': dict(tipo='ramo', ordem=(1, VITIMA), alvo=dict(dono=200)),
    'branch-mode1-target-hidden72': dict(tipo='ramo', ordem=(1, VITIMA), alvo=dict(campo72=0)),
    'branch-mode1-no-target': dict(tipo='ramo', ordem=(1, 0xffff)),
    'branch-mode1-ai-attacker-stop': dict(tipo='ramo', ordem=(1, VITIMA), alvo=dict(estado=0), controle=(1, 2, 1, 1), dono=1),
    'branch-mode1-valid-prepare': dict(tipo='ramo', ordem=(1, VITIMA)),
    'branch-mode3-no-target': dict(tipo='ramo', ordem=(3, 0xffff)),
    'branch-mode3-destroying': dict(tipo='ramo', ordem=(3, ESTRUTURA), estrutura=dict(dono=1, estado=3)),
    'branch-mode3-owner200': dict(tipo='ramo', ordem=(3, ESTRUTURA), estrutura=dict(dono=200, estado=1)),
    'branch-mode3-valid-checkpoint': dict(tipo='ramo', ordem=(3, ESTRUTURA), estrutura=dict(dono=1, estado=1), checkpoint=True),
    'branch-mode5-cell': dict(tipo='ramo', ordem=(5, 0x282a)),
    # SetAttaqueEngin entries.
    'set-mode1-accept': dict(tipo='definir', pedido=(1, VITIMA)),
    'set-same-order-early': dict(tipo='definir', pedido=(1, VITIMA), ordem=(1, VITIMA)),
    'set-mode1-self': dict(tipo='definir', pedido=(1, ATACANTE)),
    'set-mode3-accept': dict(tipo='definir', pedido=(3, ESTRUTURA)),
    'set-mode5-accept': dict(tipo='definir', pedido=(5, 0x2a2a)),
    'set-mode2-reset-only': dict(tipo='definir', pedido=(2, VITIMA)),
    'set-colonist-refused': dict(tipo='definir', pedido=(1, VITIMA), tipo_atacante=9),
    'set-builder-refused': dict(tipo='definir', pedido=(1, VITIMA), tipo_atacante=7),
    'set-moving-attacker': dict(tipo='definir', pedido=(1, VITIMA), ordem=(1, 3), estado=2),
}


_REGRAS = None


def regras():
    """Loaded type table (26 x 50 bytes) and DEGAT rows rebuilt from the original files."""
    global _REGRAS
    if _REGRAS is None:
        r = extrair_regras(bytes(ler_imagem()), 0x400000, (REPO.parent / 'source/cd/INSTALHD/RISING.INI').read_bytes())
        tipos = b''.join(bytes.fromhex(u['registro_memoria_hex']) for u in r['unidades'])
        _REGRAS = dict(tipos=tipos, danos=[bytes(u['danos_por_alvo']) for u in r['unidades']],
                       caracteristicas=[CaracteristicasTipo(u['raio_visao'], u['alcance_ataque_quadrado_u16'], u['recarga'])
                                        for u in r['unidades']],
                       vida=[u['vida_maxima'] for u in r['unidades']],
                       fadiga=[struct.unpack_from('<H', tipos, t * 50 + 0x2e)[0] for t in range(26)])
    return _REGRAS


def criar_unidade(mundo, bonus, d):
    r = regras()
    p = d['indice'] * 276
    u = memoryview(mundo.unidades)[p:p + 276]
    u[:] = bytes(276)
    u[0], u[2] = d['dono'], 7
    definir_tipo(u, d['indice'], d['celula'], d['direcao'], d['tipo'], r['caracteristicas'][d['tipo']],
                 capacidade_tipo, lambda dono, tipo, seletor: bonus.consultar(dono, tipo, seletor), BuscaAtaque())
    struct.pack_into('<H', u, 0x9a, d.get('vida') or r['vida'][d['tipo']])
    u[0x72] = 1
    for off in (0x104, 0x10c):
        struct.pack_into('<I', u, off, 0xffffffff)
    mundo.ocupar(d['indice'], d['celula'], True)


def criar_mundo(c):
    """Declared synthetic world around real loaded tables; returns (mundo, danos, pool, tipos, bonus)."""
    r = regras()
    w = MundoNavegacao(256, 256)
    w.regioes[:] = [1] * 65536
    w.controle_jogadores[:] = bytes(c.get('controle', (1, 1, 1, 1)))
    w.jogador_local = c.get('local', 3)
    w.limites_fadiga = list(r['fadiga'])
    if 'visivel' in c:
        jogador, celula = c['visivel']
        w.descoberto[jogador][celula] = 0
    bonus = BonusUnidades(bytes(1872), tipos_unidades=r['tipos'])
    if c['tipo'] == 'duelo':
        criar_unidade(w, bonus, c['atacante'])
        criar_unidade(w, bonus, c['vitima'])
    else:
        criar_unidade(w, bonus, _a(c.get('dono', 0), c.get('tipo_atacante', 0)))
        criar_unidade(w, bonus, _v(dono=1))
        a, v = (memoryview(w.unidades)[i * 276:(i + 1) * 276] for i in (ATACANTE, VITIMA))
        if 'ordem' in c:
            a[2], a[0x8a], a[0xb7] = c.get('estado', 1), 0, c['ordem'][0]
            struct.pack_into('<H', a, 0xb8, c['ordem'][1])
        alvo = c.get('alvo', {})
        if 'estado' in alvo:
            v[2] = alvo['estado']
        if 'dono' in alvo:
            v[0] = alvo['dono']
        if 'campo72' in alvo:
            v[0x72] = alvo['campo72']
        if 'estrutura' in c:
            s = memoryview(w.estruturas)[ESTRUTURA * 276:(ESTRUTURA + 1) * 276]
            s[4], s[5], s[8] = c['estrutura']['dono'], c['estrutura']['estado'], 2
    return w, r['danos'], PoolProjeteis(bytearray(5600)), r['tipos'], bonus


def resumo(b, antes, depois, nome, r, segmento, quadro, unidade):
    areas = b.areas()
    modelado = b.modelado()
    fora = [a for a in b.alteracoes(antes, depois) if not any(i <= a < i + t for i, t in modelado)]
    total = hashlib.sha256(b''.join(areas[n] for n in AREAS)).hexdigest()
    return dict(segmento=segmento, quadro=quadro, unidade=unidade, parada=nome, eip=hex(r['EIP']),
                estado=total, areas={n: hashlib.sha256(areas[n]).hexdigest()[:16] for n in AREAS},
                nao_modelados=[hex(a) for a in fora[:20]], quantidade_nao_modelados=len(fora),
                escritas_8a=[[hex(e), u, v] for e, u, v in b.escritas_8a])


def executar_nativo(b, nome):
    """Frame driver: counter, ProjectileCalcul, then attack-state units in live index order."""
    from emulador import UNIDADES
    c = CENARIOS[nome]
    w, danos, pool, tipos, _ = criar_mundo(c)
    b.preparar_vivo(w, danos, pool, tipos)
    segmentos = []

    def passo(segmento, quadro, unidade, chamada):
        antes = b.instantaneo()
        b.escritas_8a = []
        parada, r = chamada()
        segmentos.append(resumo(b, antes, b.instantaneo(), parada, r, segmento, quadro, unidade))
        return parada

    b.contador(CONTADOR_BASE)
    if c['tipo'] == 'definir':
        passo('SetAttaqueEngin', 0, ATACANTE, lambda: b.definir_ataque(ATACANTE, *c['pedido']))
        return segmentos
    if c['tipo'] == 'ramo':
        passo('ramo', 0, ATACANTE, lambda: b.ramo(ATACANTE, checkpoint_ataque=c.get('checkpoint', False)))
        return segmentos
    if passo('SetAttaqueEngin', 0, ATACANTE, lambda: b.definir_ataque(ATACANTE, 1, VITIMA)):
        return segmentos
    for quadro in range(1, c['quadros'] + 1):
        b.contador(CONTADOR_BASE + quadro)
        if passo('ProjectileCalcul', quadro, None, b.projeteis):
            return segmentos
        i = 0
        while i < 800:
            unidades = bytes(b.cpu.mem_read(UNIDADES, 220800))
            j = next((k for k in range(i, 800) if unidades[k * 276 + 2] in (1, 24)), None)
            if j is None:
                break
            if passo('preludio', quadro, j, lambda: b.preludio(j)) or passo('ramo', quadro, j, lambda: b.ramo(j)):
                return segmentos
            i = j + 1
        unidades = bytes(b.cpu.mem_read(UNIDADES, 220800))
        if not any(unidades[k * 276 + 2] in (1, 24) for k in range(800)) and not any(
                b.ler_pool()[k * 56 + 2] for k in range(100)):
            break
    return segmentos


def main(nomes=None):
    from bancada_ataque_vivo import BancadaAtaqueVivo
    b = BancadaAtaqueVivo()
    capturas = {}
    for nome in nomes or CENARIOS:
        capturas[nome] = executar_nativo(b, nome)
        ult = capturas[nome][-1]
        print(nome, len(capturas[nome]), ult['segmento'], ult['quadro'], ult['parada'], b.execucoes)
    relatorio = dict(sha256_original=HASH, contador_base=CONTADOR_BASE, areas=list(AREAS),
        origem='Original-only native runs captured before the Stage 18 Python composition; no Stage 18 module imported',
        execucoes_x86=b.execucoes, capturas=capturas)
    destino = PASTA / 'evidencias/captura-ataque-vivo-original.json'
    destino.write_text(json.dumps(relatorio, separators=(',', ':')) + '\n')
    print(destino)


if __name__ == '__main__':
    main(sys.argv[1:] or None)
