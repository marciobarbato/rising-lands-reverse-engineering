"""ProjectileReset 0x46e00a: entry contract, original captures and native whole-state equality."""
import hashlib
import json
import os
import random
import struct
import unittest
from pathlib import Path

from capturar_reinicio_projeteis import CASOS, FIM_REGIAO, REGIOES_POOL, RETORNO_BANCADA, TOPO_PILHA, entradas
from projeteis import PoolProjeteis
from reinicio_projeteis import CHAMADAS, EAX_RETORNO, ENTRADA, resetar_projeteis

CAPTURA = Path(__file__).resolve().parent / 'evidencias/captura-reinicio-projeteis-original.json'
FLAGS_ARITMETICOS, FLAGS_CMP_IGUAL = 0x8d5, 0x44  # cmp 0x64,0x64: ZF and PF set, CF/AF/SF/OF clear


class Gravador(bytearray):
    def __init__(self, dados):
        super().__init__(dados)
        self.stores = []

    def __setitem__(self, chave, valor):
        self.stores.append((chave, valor))
        super().__setitem__(chave, valor)


def sha(dados):
    return hashlib.sha256(bytes(dados)).hexdigest()


def esperado(caso, antes):
    """Python prediction for every mapped region: only the pool slice is reset."""
    depois = dict(antes)
    nome = f'pool_{REGIOES_POOL[caso["regiao"]]:#x}'
    regiao = bytearray(antes[nome])
    inicio = caso['deslocamento']
    eax = resetar_projeteis(memoryview(regiao)[inicio:inicio + 5600])
    depois[nome] = bytes(regiao)
    return depois, eax


def pilha_esperada(pilha, caso, registradores):
    """Native-only stack scratch: CALL return address, then push ebx, push edx."""
    p = bytearray(pilha)
    valores = [registradores['EBX'], registradores['EDX']]
    if 'chamador' in caso:
        valores.insert(0, caso['chamador'] + 5)
    for k, valor in enumerate(valores):
        struct.pack_into('<I', p, TOPO_PILHA - 4 * (k + 1), valor)
    return bytes(p)


class ContratosReinicioProjeteis(unittest.TestCase):
    def test_clears_only_active_bytes_in_index_order(self):
        dados = random.Random(0x46e00a).randbytes(5600)
        pool = Gravador(dados)
        self.assertEqual(resetar_projeteis(pool), EAX_RETORNO)
        self.assertEqual(pool.stores, [(i * 56 + 2, 0) for i in range(100)])
        self.assertEqual(bytes(pool), bytes(0 if k % 56 == 2 else v for k, v in enumerate(dados)))

    def test_idempotent_and_zero_pool(self):
        for dados in (bytes(5600), bytes(0 if k % 56 == 2 else 0xa5 for k in range(5600))):
            pool = bytearray(dados)
            self.assertEqual(resetar_projeteis(pool), 0x64)
            self.assertEqual(bytes(pool), dados)

    def test_live_views_inside_a_larger_arena(self):
        for formato in ('B', 'b'):
            arena = bytearray(range(256)) * 30
            vista = memoryview(arena).cast(formato)[100:5700]
            antes = bytes(arena)
            resetar_projeteis(vista)
            self.assertEqual(arena[:100], antes[:100])
            self.assertEqual(arena[5700:], antes[5700:])
            self.assertEqual(arena[100:5700], bytes(0 if k % 56 == 2 else v for k, v in enumerate(antes[100:5700])))

    def test_rejects_before_any_store(self):
        base = bytearray([0xee] * 11200)
        invalidos = (bytes(5600), bytearray(5599), bytearray(5601), memoryview(bytes(5600)),
                     memoryview(base)[::2], memoryview(base)[:5600].cast('H'),
                     memoryview(base)[:5600].cast('B', (100, 56)), list(range(5600)), None)
        for pool in invalidos:
            with self.subTest(tipo=type(pool).__name__), self.assertRaisesRegex(ValueError, '5600-byte'):
                resetar_projeteis(pool)
        self.assertEqual(base, bytearray([0xee] * 11200))

    def test_pool_object_delegates_to_entry(self):
        dados = random.Random(5600).randbytes(5600)
        p, direto = PoolProjeteis(bytearray(dados)), bytearray(dados)
        self.assertEqual(p.resetar(), resetar_projeteis(direto))
        self.assertEqual(p.memoria, direto)
        self.assertEqual(p.chamadas, [])

    def test_call_sites_and_entry(self):
        self.assertEqual(ENTRADA, 0x46e00a)
        self.assertEqual(CHAMADAS, {'MissionReStart': 0x46b5ac, 'GameLoad': 0x46b8c1,
                                    'MissionLoad': 0x46c373, 'MissionLoadName': 0x46c623})

    def test_original_only_captures_reproduced(self):
        """Committed native captures: Python reproduces every region digest from the same seeds."""
        relatorio = json.loads(CAPTURA.read_text())
        self.assertEqual(relatorio['sha256_original'], '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')
        capturas = {c['nome']: c for c in relatorio['capturas']}
        self.assertEqual(set(capturas), {c['nome'] for c in CASOS})
        valores_mais2 = set()
        for caso in CASOS:
            c, e = capturas[caso['nome']], entradas(caso)
            base = REGIOES_POOL[caso['regiao']]
            antes = {f'pool_{b:#x}': bytes(d) for b, d in e['regioes'].items()}
            for nome, regiao in antes.items():
                self.assertEqual(sha(regiao), c['regioes'][nome]['antes_sha256'])
            depois, eax = esperado(caso, antes)
            for nome in antes:
                self.assertEqual(sha(depois[nome]), c['regioes'][nome]['depois_sha256'], (caso['nome'], nome))
            pool = antes[f'pool_{base:#x}'][caso['deslocamento']:caso['deslocamento'] + 5600]
            valores_mais2.update(pool[i * 56 + 2] for i in range(100))
            self.assertEqual(sha(pool), c['pool']['entrada_sha256'])
            for nome in ('imagem', 'unidades', 'retorno'):
                self.assertEqual(c['regioes'][nome]['alteracoes'], [], nome)
            pilha = bytes(e['pilha'])
            self.assertEqual(sha(pilha), c['regioes']['pilha']['antes_sha256'])
            self.assertEqual(sha(pilha_esperada(pilha, caso, e['registradores'])), c['regioes']['pilha']['depois_sha256'])
            saida = {n: int(v, 16) for n, v in c['registradores_saida'].items()}
            self.assertEqual(saida['EAX'], eax)
            for nome in ('EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP'):
                self.assertEqual(saida[nome], e['registradores'][nome])
            self.assertEqual(saida['EFLAGS'], (e['eflags'] & ~FLAGS_ARITMETICOS) | FLAGS_CMP_IGUAL)
        self.assertEqual(valores_mais2, set(range(256)))
        self.assertEqual({int(c['chamador'], 16) for c in capturas.values() if c['chamador']}, set(CHAMADAS.values()))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional: RISING_EMULAR=1')
class DiferencialReinicioProjeteis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_reinicio_projeteis import BancadaReinicioProjeteis, ESP_ENTRADA
        cls.b, cls.esp = BancadaReinicioProjeteis(), ESP_ENTRADA
        cls.comparacoes = cls.chamadas_originais = 0

    def comparar(self, caso):
        e = entradas(caso)
        self.b.preparar(e['globais'], e['unidades'], e['pilha'], e['regioes'], e['ponteiro'])
        antes = self.b.instantaneo()
        saida = self.b.resetar(e['registradores'], e['eflags'], caso.get('chamador'))
        depois = self.b.instantaneo()
        previsto, eax = esperado(caso, antes)
        previsto['pilha'] = pilha_esperada(antes['pilha'], caso, e['registradores'])
        self.assertEqual(set(depois), set(previsto))
        for nome in depois:
            self.assertEqual(depois[nome], previsto[nome], (caso['nome'], nome))
        self.assertEqual(saida['EAX'], eax)
        for nome in ('EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP'):
            self.assertEqual(saida[nome], e['registradores'][nome], nome)
        chamador = caso.get('chamador')
        self.assertEqual(saida['ESP'], self.esp + (0 if chamador else 4))
        self.assertEqual(saida['EIP'], chamador + 5 if chamador else RETORNO_BANCADA)
        self.assertEqual(saida['EFLAGS'], (e['eflags'] & ~FLAGS_ARITMETICOS) | FLAGS_CMP_IGUAL)
        type(self).comparacoes += 1
        type(self).chamadas_originais += bool(chamador)
        return depois

    def test_captured_cases_whole_state(self):
        relatorio = json.loads(CAPTURA.read_text())
        capturas = {c['nome']: c for c in relatorio['capturas']}
        for caso in CASOS:
            with self.subTest(caso=caso['nome']):
                depois = self.comparar(caso)
                for nome, regiao in depois.items():
                    self.assertEqual(sha(regiao), capturas[caso['nome']]['regioes'][nome]['depois_sha256'], nome)

    def test_fresh_dirty_states_and_callers(self):
        rng = random.Random(0x46c373)
        chamadores = [None, *CHAMADAS.values()]
        for k in range(60):
            caso = dict(nome=f'fresh-{k}', semente=1000 + k, regiao=k % 2,
                        deslocamento=rng.randrange(FIM_REGIAO + 1))
            if chamadores[k % 5] is not None:
                caso['chamador'] = chamadores[k % 5]
            padrao = k % 4
            if padrao == 1:
                caso['mais2'] = rng.randrange(256)
            elif padrao == 2:
                caso['mais2_zero'] = True
            elif padrao == 3:
                caso['preencher'] = rng.randrange(256)
            with self.subTest(caso=caso):
                self.comparar(caso)


if __name__ == '__main__':
    unittest.main()
