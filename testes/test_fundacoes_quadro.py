"""Core frame foundations: frozen original replay over M1 state and input protection (CPU-free)."""
import hashlib
import json
from pathlib import Path
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
from cadencia import proximo_aleatorio
from estado_m1_quadro import carregar_m1, DGROUP, THREAD
from fundacoes_quadro import (avancar_quadro_jogo, aleatorio_mundo, randomizar_mundo, definir_semente_mundo,
                              obter_semente_mundo, aleatorio_ia, aleatorio_crt, consumir_permutacao,
                              avancar_contadores_iteracao, zerar_contadores_carga, DependenciaRelogioIA,
                              CONTADOR_QUADRO_JOGO, SEMENTE_MUNDO, SEMENTE_IA, CONTADORES_ITERACAO,
                              TABELA_PERMUTACAO, CURSOR_PERMUTACAO, CHAMADA_RELOGIO_IA)

CAPTURA = RAIZ / 'evidencias/fundacoes-quadro/captura-original.json'
CAPTURA_SHA256 = 'a374666338c99b0a898d7cc935f283293aacebb967504a82500389f61f78b638'
SEMENTE_CRT = THREAD[0] + 0xc
PRESERVA_TUDO_MENOS_EAX = ('Random', 'Randomize', 'SetRandomSeed', 'GetRandomSeed', 'iaRandom', 'LongRand')
REGS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')


def captura():
    return json.loads(CAPTURA.read_text())


class EstadoQuadro:
    """Whole DGROUP + thread blocks as live bytearrays; routines get views into them."""
    def __init__(self, dgroup, thread, sobrescritas=()):
        self.dg, self.th = bytearray(dgroup), bytearray(thread)
        for endereco, dados in sobrescritas:
            self.vista(endereco, len(dados))[:] = dados

    def vista(self, endereco, tamanho):
        if DGROUP[0] <= endereco and endereco+tamanho <= DGROUP[1]:
            return memoryview(self.dg)[endereco-DGROUP[0]:endereco-DGROUP[0]+tamanho]
        if THREAD[0] <= endereco and endereco+tamanho <= THREAD[1]:
            return memoryview(self.th)[endereco-THREAD[0]:endereco-THREAD[0]+tamanho]
        raise ValueError(hex(endereco))

    def u32(self, endereco):
        return int.from_bytes(self.vista(endereco, 4), 'little')

    def bytes(self):
        return bytes(self.dg), bytes(self.th)


def executar_python(estado, rotina, eax, relogio=None):
    """Run the Python translation; return (EAX or None, ordered expected non-stack stores)."""
    v = estado.vista
    if rotina == 'GameNextFrame':
        avancar_quadro_jogo(v(CONTADOR_QUADRO_JOGO, 4))
        return None, [(CONTADOR_QUADRO_JOGO, 4, estado.u32(CONTADOR_QUADRO_JOGO))]
    if rotina in ('Random', 'Randomize', 'SetRandomSeed', 'GetRandomSeed'):
        s = v(SEMENTE_MUNDO, 4)
        r = dict(Random=lambda: aleatorio_mundo(s), Randomize=lambda: randomizar_mundo(s, eax),
                 SetRandomSeed=lambda: definir_semente_mundo(s, eax),
                 GetRandomSeed=lambda: obter_semente_mundo(bytes(s)))[rotina]()
        return r, ([] if rotina == 'GetRandomSeed' else [(SEMENTE_MUNDO, 4, estado.u32(SEMENTE_MUNDO))])
    if rotina == 'iaRandom':
        r = aleatorio_ia(v(SEMENTE_IA, 4), eax, None if relogio is None else (lambda: relogio))
        return r, [(SEMENTE_IA, 4, estado.u32(SEMENTE_IA))]
    if rotina == 'LongRand':
        r = aleatorio_crt(memoryview(estado.th))
        return r, [(SEMENTE_CRT, 4, estado.u32(SEMENTE_CRT))]
    if rotina == 'ProgIteration_counter_prefix':
        gravados = avancar_contadores_iteracao(v(CONTADORES_ITERACAO, 12))
        return None, [(CONTADORES_ITERACAO+o, 4, estado.u32(CONTADORES_ITERACAO+o)) for o in gravados]
    if rotina == 'CalculGame_load_counter_reset':
        gravados = zerar_contadores_carga(v(CONTADORES_ITERACAO, 12))
        return None, [(CONTADORES_ITERACAO+o, 4, 0) for o in gravados]
    if rotina == 'CalculGame_cd_permutation_draw':
        b = consumir_permutacao(bytes(v(TABELA_PERMUTACAO, 256)), v(CURSOR_PERMUTACAO, 1))
        return b, [(CURSOR_PERMUTACAO, 1, v(CURSOR_PERMUTACAO, 1)[0])]
    raise KeyError(rotina)


def conferir_registradores(teste, rotina, regs_in, regs_out, eax, estado):
    """Assert the consumed EAX and the preserved registers of each routine."""
    if rotina == 'GameNextFrame' or rotina in PRESERVA_TUDO_MENOS_EAX:
        if rotina != 'GameNextFrame':
            teste.assertEqual(regs_out['EAX'], eax, 'EAX')
        for n in REGS:
            if n != 'EAX' or rotina == 'GameNextFrame':
                teste.assertEqual(regs_out[n], regs_in[n], n)
    elif rotina == 'CalculGame_cd_permutation_draw':
        teste.assertEqual(regs_out['EAX'], 2 + eax % 2)
        teste.assertEqual((regs_out['EDX'], regs_out['ECX']), (0, 2))
        teste.assertEqual(regs_out['EBX'], regs_in['EBX'] & ~0xff | estado.vista(CURSOR_PERMUTACAO, 1)[0])
    elif rotina == 'CalculGame_load_counter_reset':
        # MenuInit arguments prepared around the stores (composed by ai-runtime).
        teste.assertEqual((regs_out['EAX'], regs_out['EBX'], regs_out['ECX'], regs_out['EDX']),
                          (estado.vista(0x508041, 1)[0], 0, 1, 0x12))


class ReplayCapturaOriginal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dgroup, cls.thread, cls.proveniencia = carregar_m1()
        cls.dados = captura()

    def test_capture_is_the_committed_original_only_evidence(self):
        d = self.dados
        self.assertEqual(hashlib.sha256(CAPTURA.read_bytes()).hexdigest(), CAPTURA_SHA256)
        self.assertFalse(d['translation_executed'])
        self.assertEqual(d['m1_input'], self.proveniencia)
        self.assertEqual(d['code_sha256_before'], d['code_sha256_after'])
        self.assertEqual(len(d['cases']), 62)
        self.assertEqual(sum(len(c['steps']) for c in d['cases']), 195)
        for c in d['cases']:
            self.assertEqual(c['input'], 'M1 post-load input, not yet frame-1 input')
            self.assertEqual(bool(c['derived_overrides']), c['name'].startswith('derived_'), c['name'])

    def test_every_captured_step_matches_python_whole_state_writes_and_registers(self):
        for c in self.dados['cases']:
            with self.subTest(c['name']):
                estado = EstadoQuadro(self.dgroup, self.thread,
                                      [(int(a, 16), bytes.fromhex(d)) for a, d in c['derived_overrides']])
                self.assertEqual(hashlib.sha256(b''.join(estado.bytes())).hexdigest(), c['initial_sha256'])
                for p in c['steps']:
                    antes = estado.bytes()
                    regs_in = {k: int(v, 16) for k, v in p['registers_in'].items()}
                    relogio = None if p['declared_clock'] is None else int(p['declared_clock'], 16)
                    eax, escritas = executar_python(estado, p['routine'], regs_in['EAX'], relogio)
                    depois = estado.bytes()
                    mudancas = [[hex(DGROUP[0]+i), antes[0][i], depois[0][i]] for i in range(len(antes[0]))
                                if antes[0][i] != depois[0][i]]
                    mudancas += [[hex(THREAD[0]+i), antes[1][i], depois[1][i]] for i in range(len(antes[1]))
                                 if antes[1][i] != depois[1][i]]
                    self.assertEqual(mudancas, p['state_changes'], p['routine'])
                    self.assertEqual([[hex(a), t, hex(x)] for a, t, x in escritas], p['writes'], p['routine'])
                    regs_out = {k: int(v, 16) for k, v in p['registers'].items()}
                    conferir_registradores(self, p['routine'], regs_in, regs_out, eax, estado)
                    self.assertEqual(len(p['clock']), relogio is not None)
                self.assertEqual(hashlib.sha256(b''.join(estado.bytes())).hexdigest(), c['final_sha256'])

    def test_m1_inputs_documented_in_frame_foundations(self):
        e = EstadoQuadro(self.dgroup, self.thread)
        self.assertEqual([e.u32(CONTADORES_ITERACAO+o) for o in (0, 4, 8)], [0, 0, 0])
        self.assertEqual(e.u32(CONTADOR_QUADRO_JOGO), 1)
        self.assertEqual(e.vista(CURSOR_PERMUTACAO, 1)[0], 0)
        self.assertEqual(sorted(e.vista(TABELA_PERMUTACAO, 256)), list(range(256)))
        self.assertEqual(int.from_bytes(e.vista(0x508724, 2), 'little'), 0)  # viewport width
        self.assertEqual(int.from_bytes(e.vista(0x508726, 2), 'little'), 0)  # viewport height
        self.assertEqual(int.from_bytes(e.vista(0x4973ea, 2), 'little'), 128)  # field period
        self.assertEqual((e.vista(0x4e0730, 1)[0], e.vista(0x4e2f28, 1)[0]), (0, 0))
        self.assertEqual(e.u32(0x522244), THREAD[0])
        self.assertEqual(e.u32(0x4990cc), 0x48e7c7)


class ContratoEntradas(unittest.TestCase):
    def test_positive_ia_path_agrees_with_existing_cadencia_domain(self):
        for estado in (1, 2, 127772, 127773, 0x12345678, 0x7ffffffe, 0x7fffffff):
            for limite in (1, 3, 1000, 0x7fffffff):
                s = bytearray(estado.to_bytes(4, 'little'))
                r = aleatorio_ia(s, limite)
                self.assertEqual((int.from_bytes(s, 'little'), r), proximo_aleatorio(estado, limite))

    def test_negative_and_zero_limits(self):
        s = bytearray(4)
        self.assertEqual(aleatorio_ia(s, 0x80000000), 0)
        self.assertEqual(bytes(s), b'\xff\xff\xff\xff')
        self.assertEqual(aleatorio_ia(s, -5), 0)
        self.assertEqual(int.from_bytes(s, 'little'), 5)
        self.assertEqual(aleatorio_ia(s, 0, lambda: 0xffffffff), 0)
        self.assertEqual(int.from_bytes(s, 'little'), 1)

    def test_clock_dependency_is_named_and_writes_nothing(self):
        s = bytearray(b'\x11\x22\x33\x44')
        with self.assertRaises(DependenciaRelogioIA) as e:
            aleatorio_ia(s, 0)
        self.assertEqual(e.exception.endereco, CHAMADA_RELOGIO_IA)
        self.assertEqual(bytes(s), b'\x11\x22\x33\x44')
        for invalido in (None, -1, 1 << 32, 1.0):
            with self.assertRaises(ValueError):
                aleatorio_ia(s, 0, lambda v=invalido: v)
            self.assertEqual(bytes(s), b'\x11\x22\x33\x44')

    def test_malformed_buffers_rejected_before_mutation(self):
        for f in (avancar_quadro_jogo, aleatorio_mundo, lambda b: randomizar_mundo(b, 1),
                  lambda b: definir_semente_mundo(b, 1), lambda b: aleatorio_ia(b, 7)):
            for ruim in (bytes(4), bytearray(3), bytearray(5), [0, 0, 0, 0], memoryview(bytes(4)),
                         memoryview(bytearray(8)).cast('I')):
                with self.assertRaises(ValueError):
                    f(ruim)
        for ruim in (bytes(16), bytearray(15), memoryview(bytes(16))):
            with self.assertRaises(ValueError):
                aleatorio_crt(ruim)
        with self.assertRaises(ValueError):
            consumir_permutacao(bytes(255), bytearray(1))
        with self.assertRaises(ValueError):
            consumir_permutacao(bytes(256), bytes(1))
        for f in (avancar_contadores_iteracao, zerar_contadores_carga):
            with self.assertRaises(ValueError):
                f(bytearray(8))

    def test_views_mutate_the_owner_in_place(self):
        dono = bytearray(16)
        avancar_quadro_jogo(memoryview(dono)[4:8])
        self.assertEqual(dono[4], 1)
        self.assertEqual(obter_semente_mundo(bytes(4)), 0)
        cursor = bytearray([255])
        self.assertEqual(consumir_permutacao(bytes(range(256)), cursor), 255)
        self.assertEqual(cursor[0], 0)
        contadores = bytearray(b'\xff' * 4 + bytes(8))
        self.assertEqual(avancar_contadores_iteracao(contadores), (0, 4, 8))
        self.assertEqual(bytes(contadores), bytes(4) + b'\x01\x00\x00\x00' + b'\x01\x00\x00\x00')


if __name__ == '__main__':
    unittest.main()
