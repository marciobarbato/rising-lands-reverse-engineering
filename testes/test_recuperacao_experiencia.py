"""Engin_RetrieveExperimente: frozen original replay and input protection (CPU-free)."""
import hashlib
import json
from pathlib import Path
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
from ordens_unidades import MundoUnidades
from recuperacao_experiencia import (recuperar_experiencias, recuperar_experiencia_missao,
                                     DependenciaExperienciaGuardada, RetornoRecuperacaoExperiencia,
                                     EAX_RETORNO, LEITURA_GUARDADA)

CAPTURA = RAIZ / 'evidencias/recuperacao-experiencia/captura-original.json'
CAPTURA_SHA256 = '5c734542db10337117b8167f15fe7bd49c47a4e4c5553fd6ea750949c2c220d3'
PRESERVADOS = ('EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')


def captura():
    return json.loads(CAPTURA.read_text())


class ReplayCapturaOriginal(unittest.TestCase):
    def test_capture_is_the_committed_original_only_evidence(self):
        self.assertEqual(hashlib.sha256(CAPTURA.read_bytes()).hexdigest(), CAPTURA_SHA256)
        d = captura()
        self.assertFalse(d['translation_executed'])
        self.assertEqual(len(d['cases']), 20)
        self.assertEqual(d['original_entries'], {'0x441623': 20, '0x441470': 1, '0x4414f8': 1})

    def test_every_captured_case_matches_python_memory_registers_and_flags(self):
        for c in captura()['cases']:
            with self.subTest(c['name']):
                atuais = bytearray.fromhex(c['before']['current'])
                guardadas = bytes.fromhex(c['before']['saved'])
                identidade = atuais
                r = recuperar_experiencias(atuais, guardadas)
                self.assertIs(atuais, identidade)
                self.assertEqual(atuais.hex(), c['after']['current'])
                self.assertEqual(guardadas.hex(), c['after']['saved'])
                regs = {k: int(v, 16) for k, v in c['retrieve']['registers'].items()}
                entrada = {k: int(v, 16) for k, v in c['registers_in'].items()}
                self.assertEqual(r.eax, regs['EAX'])
                self.assertEqual(RetornoRecuperacaoExperiencia.eflags(entrada['EFLAGS']), regs['EFLAGS'])
                for nome in PRESERVADOS:
                    self.assertEqual(regs[nome], entrada[nome], nome)
                self.assertEqual(regs['ESP'], 0x2008004)
                # Original image changes are exactly the current-queue bytes Python changed.
                antes = bytes.fromhex(c['before']['current'])
                esperado = [[hex(0x4e19c4+i), antes[i], atuais[i]] for i in range(40) if antes[i] != atuais[i]]
                self.assertEqual(c['retrieve']['image_changes'], esperado)
                # Ordered u16 writes ascend through all four owners, five words each.
                dados = [w for w in c['retrieve']['writes'] if int(w[0], 16) < 0x2000000]
                self.assertEqual(dados, [[hex(0x4e19c4+2*i), 2, hex(guardadas[2*i] | guardadas[2*i+1] << 8)]
                                         for i in range(20)])
                self.assertEqual([int(w[2], 16) for w in c['retrieve']['stack_writes']],
                                 [entrada[n] for n in ('EBX', 'ECX', 'EDX', 'ESI')])

    def test_provenance_chains_saved_bytes(self):
        casos = {c['name']: c for c in captura()['cases']}
        self.assertEqual(casos['chain_fresh_campaign_reset']['before']['saved'], 'ff00'*20)
        self.assertEqual(casos['chain_mission_end_store']['producer']['entry'], '0x4414f8')


class ProtecaoEntradas(unittest.TestCase):
    def setUp(self):
        self.atuais = bytearray(range(40))
        self.guardadas = bytes(range(100, 140))

    def nao_mudou(self):
        self.assertEqual(self.atuais, bytearray(range(40)))

    def test_missing_saved_queue_is_named_dependency_before_any_store(self):
        with self.assertRaises(DependenciaExperienciaGuardada) as ctx:
            recuperar_experiencias(self.atuais, None)
        self.assertEqual(ctx.exception.endereco, LEITURA_GUARDADA)
        self.assertEqual(LEITURA_GUARDADA, 0x441645)
        self.nao_mudou()

    def test_malformed_buffers_fail_before_first_store(self):
        for atuais, guardadas in ((bytearray(39), self.guardadas), (bytes(40), self.guardadas),
                                  (memoryview(bytearray(40)), self.guardadas), (self.atuais, bytes(41)),
                                  (self.atuais, memoryview(self.guardadas)), (self.atuais, [0]*40),
                                  (self.atuais, self.atuais)):
            with self.subTest(f"{type(atuais).__name__}/{type(guardadas).__name__}"):
                with self.assertRaises(ValueError):
                    recuperar_experiencias(atuais, guardadas)
                self.nao_mudou()

    def test_world_entry_uses_live_queue_by_identity(self):
        m = MundoUnidades()
        fila = m.experiencias_unidades
        fila[:] = bytes(range(40))
        guardadas = bytearray(b'\xff\x00'*20)
        r = recuperar_experiencia_missao(m, guardadas)
        self.assertIs(m.experiencias_unidades, fila)
        self.assertEqual(fila, guardadas)
        self.assertIsNot(fila, guardadas)
        self.assertEqual(r.eax, EAX_RETORNO)
        self.assertEqual(guardadas, bytearray(b'\xff\x00'*20))


if __name__ == '__main__':
    unittest.main()
