"""Economy M2 frame routines against the original capture over the M1 post-load state.

The frozen capture (v2) was recorded before translation. Python runs the same
call sequence over its own copy of the M1 memory and must reproduce every
call's outcome (return or dependency stop with the same arguments), every
natively written byte, and the whole-state hash after each scenario.
``RISING_EMULAR=1`` also reruns the original capture and requires it to equal
the frozen file.
"""
import bisect
import hashlib
import json
import os
from pathlib import Path
import struct
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
import capturar_quadro_m2_original as captura  # noqa: E402
import quadro_economia as q  # noqa: E402

CAPTURA = PASTA / 'evidencias/captura-quadro-m2-original-v2.json'
_BLOCOS = None


def evidencia():
    return json.loads(CAPTURA.read_text())


def blocos():
    global _BLOCOS
    if _BLOCOS is None:
        _BLOCOS = captura.blocos_m1()
    return _BLOCOS


class Memoria:
    """M1 blocks (or another declared base state) as separate bytearrays; ``vista`` is a live view, like
    MapaMemoriaM1.vista."""
    def __init__(self, fonte=None):
        self.blocos = [(nome, base, bytearray(raw)) for nome, base, raw in (blocos() if fonte is None else fonte)]
        self.ordem = sorted(self.blocos, key=lambda b: b[1])
        self.bases = [b[1] for b in self.ordem]
        self.acessos = []    # vista calls (writes, and reads by bound providers)
        self.leituras = []   # ler calls
        self.ordem_acessos = []  # both, in call order

    def vista(self, endereco, tamanho):
        i = bisect.bisect_right(self.bases, endereco) - 1
        if i >= 0:
            _, base, raw = self.ordem[i]
            if endereco + tamanho <= base + len(raw):
                self.acessos.append((endereco, tamanho))
                self.ordem_acessos.append(('vista', endereco, tamanho))
                return memoryview(raw)[endereco - base:endereco - base + tamanho]
        raise KeyError(f'0x{endereco:08x}+{tamanho} is not mapped in the M1 state')

    def ler(self, endereco, tamanho):
        dados = bytes(self.vista(endereco, tamanho))
        self.acessos.pop()
        self.ordem_acessos[-1] = ('ler', endereco, tamanho)
        self.leituras.append((endereco, tamanho))
        return dados

    def escrever(self, endereco, dados):
        self.vista(endereco, len(dados))[:] = bytes(dados)

    def ponteiro(self, endereco):
        return struct.unpack('<I', self.ler(endereco, 4))[0]

    def sha(self):
        h = hashlib.sha256()
        for nome, _, raw in self.blocos:
            h.update(nome.encode() + bytes(raw))
        return h.hexdigest()


class Provedores:
    """Existing economy providers bound to the live memory by identity (as the composer does)."""
    def __init__(self, m):
        from construcoes import EconomiaConstrucoes, TerrenoSacolas
        from extracao import RecursosTerreno
        from producao import Producao
        from recrutamento import Recrutamento
        terreno = TerrenoSacolas()
        terreno.tipos = m.vista(m.ponteiro(0x507d74), 65536)
        terreno.quantidades = m.vista(m.ponteiro(0x507dac), 65536)
        self.recursos = RecursosTerreno(terreno)
        self.recursos.atributos = m.vista(m.ponteiro(0x507da8), 65536)
        self.recursos.mosaicos = m.vista(m.ponteiro(0x507d70), 131072)
        self.recursos.minas = m.vista(0x509954, 80)
        construcoes = EconomiaConstrucoes()
        construcoes.estruturas = m.vista(0x49a0c8, 276000)
        recrutamento = Recrutamento(construcoes)
        recrutamento.unidades = m.vista(m.ponteiro(0x4e19a0), 220800)
        self.producao = Producao(recrutamento)
        self.producao.tipos_construcoes = m.vista(0x495d8c, 1144)
        self.tropas = []

    def calcular_tropa(self, indice):
        self.tropas.append(indice)
        return self.producao.calcular_tropa(indice)


def parar_simpatia(a, b, evento):
    """The v2 capture declares MAJSympathie's entry 0x475118 as a stop."""
    raise q.DependenciaQuadro('MAJSympathie', 0x475118, 'declared capture stop', dict(AL=a, DL=b, EBX=evento))


def executar(m, p, entrada, regs):
    rotinas = {
        0x47125c: lambda: q.calcular_pesquisa(m),
        0x46da3b: lambda: q.contar_aliancas(m, simpatia=parar_simpatia),
        0x475328: lambda: q.agendar_campos(m, p.recursos),
        0x478806: lambda: q.atualizar_campos(m, p.recursos),
        0x467718: lambda: q.calcular_materia(m),
        0x466dd1: lambda: q.calcular_contador_mercado(m, regs['EAX']),
        0x466e9b: lambda: q.calcular_contador_proposicao(m, regs['EAX'], regs['EDX']),
        0x46d629: lambda: q.calcular_simpatia_ataques(m, simpatia=parar_simpatia),
        0x456966: lambda: q.estado_parado_unidade(m, regs['EDI']),
        0x426918: lambda: q.ramo_producao_estrutura(p.producao, regs['EDI'], p.calcular_tropa),
    }
    try:
        rotinas[entrada]()
    except q.DependenciaQuadro as erro:
        return erro
    return None


def argumentos_nativos(nome, regs):
    r = {k: int(v, 16) for k, v in regs.items()}
    if nome == 'InventionSetEffet':
        return dict(AL=r['EAX'] & 0xff, DL=r['EDX'] & 0xff, BL=r['EBX'] & 0xff, ECX=r['ECX'])
    if nome == 'InitGameZone':
        return dict(EAX=r['EAX'], EDX=r['EDX'], EBX=r['EBX'], ECX=r['ECX'])
    if nome == 'MAJSympathie':
        return dict(AL=r['EAX'] & 0xff, DL=r['EDX'] & 0xff, EBX=r['EBX'])
    if nome == 'AnimBallonStatic':
        return dict(EAX=r['EAX'])
    return dict(indice=r['EBX'] & 0xff)  # market branch checkpoints: EBX holds the state index


def comparar(teste, memoria=None):
    """Replay every frozen scenario in Python; return the number of compared calls."""
    original = evidencia()
    base = Memoria()
    roteiro = captura.cenarios(base)
    teste.assertEqual([r[0] for r in roteiro], [c['name'] for c in original['captures']])
    total = 0
    for (nome, _, overrides, passos), obs in zip(roteiro, original['captures']):
        m, espelho = Memoria(), Memoria()
        for a, dados in overrides:
            m.escrever(a, dados)
            espelho.escrever(a, dados)
        teste.assertEqual(m.sha(), obs['initial_state_sha256'], nome)
        p = Provedores(m)
        chamadas = iter(obs['calls'])
        for passo in passos:
            if passo[0] == 'contador':
                m.escrever(captura.CONTADOR, struct.pack('<I', passo[1]))
                espelho.escrever(captura.CONTADOR, struct.pack('<I', passo[1]))
                continue
            c = next(chamadas)
            teste.assertEqual((c['call'], int(c['entry'], 16)), (passo[1], passo[2]))
            regs = {k: int(v, 16) for k, v in c['regs_in'].items()}
            m.acessos.clear()
            m.leituras.clear()
            erro = executar(m, p, int(c['entry'], 16), regs)
            if c['outcome'] == 'return':
                teste.assertIsNone(erro, f'{nome}/{c["call"]}')
            else:
                teste.assertIsNotNone(erro, f'{nome}/{c["call"]}')
                teste.assertEqual((erro.endereco, erro.argumentos),
                                  (int(c['stop']['address'], 16), argumentos_nativos(c['stop']['name'], c['regs_out'])),
                                  f'{nome}/{c["call"]}')
            for endereco, tamanho, valor in c['writes']:
                espelho.escrever(int(endereco, 16), valor.to_bytes(tamanho, 'little'))
            for endereco, tamanho in m.acessos + m.leituras + [(int(a, 16), t) for a, t, _ in c['writes']]:
                teste.assertEqual(m.ler(endereco, tamanho), espelho.ler(endereco, tamanho),
                                  f'{nome}/{c["call"]} at 0x{endereco:08x}')
            total += 1
        teste.assertIsNone(next(chamadas, None))
        teste.assertEqual(m.sha(), obs['final_state_sha256'], nome)
        teste.assertEqual(espelho.sha(), obs['final_state_sha256'], nome)
        if nome == 'm1_structure0_type2_branch':
            teste.assertEqual(p.tropas, [0])
    return total


class ContratosQuadroEconomia(unittest.TestCase):
    def test_frozen_capture_precedes_translation(self):
        r = evidencia()
        self.assertFalse(r['translation_executed'])
        self.assertEqual((r['scenarios'], r['original_entries'], r['returns'], r['dependency_stops']),
                         (52, 6692, 6674, 18))
        self.assertEqual(r['input']['state_sha256'], captura.SHA_ESTADO_M1)
        self.assertIn('NOT a frame-1 input', r['input']['label'])
        self.assertEqual(hashlib.sha256(CAPTURA.read_bytes()).hexdigest(),
                         'ffe92da558f360f4b01b9f74e0c539a4988aeba3d19b9fd7329d55f25915ec4e')

    def test_python_reproduces_original_capture(self):
        self.assertEqual(comparar(self), 6692)

    def test_monde01_first_frames(self):
        m = Memoria()
        for k in range(1, 9):
            m.escrever(captura.CONTADOR, struct.pack('<I', k))
            q.calcular_pesquisa(m)
            q.contar_aliancas(m)
            q.calcular_materia(m)
            q.calcular_contador_mercado(m, 0)
            q.calcular_contador_proposicao(m, 0, 0)
            q.calcular_simpatia_ataques(m)
            exibidos = [struct.unpack('<H', m.ler(0x4e2ea8 + 8 * r + 4, 2))[0] for r in range(4)]
            self.assertEqual(exibidos, [0, 10 * (k // 2) if k < 6 else 30, 10 * (k // 2) if k < 6 else 30, 0])

    def test_unreached_calls_are_named_dependencies(self):
        m = Memoria()
        m.escrever(q.IA_INATIVO, b'\x00')
        m.escrever(q.IA_INATIVO + 16, b'\x00')
        m.escrever(captura.CONTADOR, struct.pack('<I', 2000))
        with self.assertRaises(q.DependenciaQuadro) as erro:
            q.calcular_simpatia_ataques(m)
        self.assertEqual((erro.exception.endereco, erro.exception.argumentos), (0x47515d, dict(EAX=0, EDX=1, EBX=0x13)))
        chamadas = []
        m = Memoria()
        m.escrever(captura.CONTADOR, struct.pack('<I', 4000))
        q.calcular_simpatia_ataques(m, simpatia=lambda *a: chamadas.append(a))
        self.assertEqual(chamadas, [(p, d, 0x13) for p in range(4) for d in range(4) if p != d])

    def test_research_count_query_matches_original_capture(self):
        r = json.loads((PASTA / 'evidencias/captura-invencoes-original.json').read_text())
        self.assertFalse(r['translation_executed'])
        self.assertEqual((r['original_entries'], r['returns']), (1024, 1024))
        for cenario in r['captures']:
            m = Memoria()
            for o in cenario['overrides']:
                m.escrever(int(o['address'], 16), bytes.fromhex(o['bytes']))
            self.assertEqual(m.sha(), cenario['initial_state_sha256'])
            for c in cenario['calls']:
                self.assertEqual(c['writes'], [])
                # The original zero-extends: and eax, 0xff, then loads AL.
                self.assertEqual(q.numero_invencoes(m, int(c['regs_in']['EAX'], 16)), int(c['regs_out']['EAX'], 16))
            self.assertEqual(m.sha(), cenario['final_state_sha256'])

    def test_random_matches_existing_sack_generator(self):
        from construcoes import TerrenoSacolas
        m = Memoria()
        t = TerrenoSacolas(semente=struct.unpack('<I', m.ler(q.ALEATORIO, 4))[0])
        for _ in range(1000):
            self.assertEqual(q.aleatorio(m), t._aleatorio())


@unittest.skipUnless(os.environ.get('RISING_EMULAR'), 'set RISING_EMULAR=1 to rerun the original capture')
class DiferencialQuadroEconomia(unittest.TestCase):
    execucoes = 0

    def test_fresh_original_capture_equals_frozen(self):
        import tempfile
        with tempfile.TemporaryDirectory() as pasta:
            destino = Path(pasta) / 'captura.json'
            captura.capturar(destino)
            fresca = json.loads(destino.read_text())
        frozen = evidencia()
        self.assertEqual(fresca['captures'], frozen['captures'])
        self.assertEqual((fresca['original_entries'], fresca['returns'], fresca['dependency_stops']),
                         (frozen['original_entries'], frozen['returns'], frozen['dependency_stops']))
        type(self).execucoes += fresca['original_entries']


if __name__ == '__main__':
    unittest.main()
