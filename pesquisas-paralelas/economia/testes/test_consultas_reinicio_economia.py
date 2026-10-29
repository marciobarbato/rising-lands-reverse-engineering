"""Three small owner leaves against frozen original evidence and live views."""
import array
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
from consultas_reinicio_economia import nivel_pesquisa, definir_ramo_pesquisa, tipo_estrutura
from casos_consultas_reinicio_economia import cenarios

CAPTURA = PASTA/'evidencias/captura-consultas-reinicio-economia-original.json'


def evidencia():
    return json.loads(CAPTURA.read_text())


def replay(teste):
    chamadas = 0
    teste.assertEqual(len(cenarios()),len(evidencia()['captures']))
    for caso, original in zip(cenarios(), evidencia()['captures']):
        teste.assertEqual(caso['nome'], original['nome'])
        teste.assertEqual(len(caso['chamadas']),len(original['chamadas']))
        arena_p = bytearray(b'\xa6'*16+caso['pesquisa']+b'\x6a'*16)
        arena_e = bytearray(b'\xc7'*16+caso['estruturas']+b'\x7c'*16)
        pesquisa, estruturas = memoryview(arena_p)[16:80], memoryview(arena_e)[16:276016]
        for c, observado in zip(caso['chamadas'], original['chamadas']):
            regs = c['regs']
            if c['entrada'] == 0x4717c2:
                teste.assertEqual(nivel_pesquisa(pesquisa,regs['EAX'],regs['EDX']),observado['saida_regs']['EAX'] & 65535)
            elif c['entrada'] == 0x470b37:
                teste.assertIsNone(definir_ramo_pesquisa(pesquisa,regs['EAX'],regs['EDX']))
            elif c['entrada'] == 0x41a4f4:
                teste.assertEqual(tipo_estrutura(estruturas,regs['EAX']),observado['saida_regs']['EAX'] & 255)
            else:
                # Six preexisting GetPlayer observations belong to the reused
                # Combat bridge. No duplicate Python owner getter is created.
                teste.assertEqual(c['entrada'],0x41a08c)
                continue
            chamadas += 1
            estado = dict(pesquisa=bytes(pesquisa).hex(),
                          estruturas_sha256=hashlib.sha256(estruturas).hexdigest(),
                          guardas=[bytes(v).hex() for v in (arena_p[:16],arena_p[80:],arena_e[:16],arena_e[276016:])])
            teste.assertEqual(estado,observado['estado'])
    teste.assertEqual(chamadas,14)


class ContratosConsultasReinicioEconomia(unittest.TestCase):
    def test_frozen_original_capture_precedes_translation(self):
        r = evidencia()
        self.assertEqual((r['scenarios'],r['original_entries'],r['bounded_segments']),(14,20,20))
        self.assertFalse(r['translation_executed'])
        self.assertEqual(hashlib.sha256(CAPTURA.read_bytes()).hexdigest(),
                         '367acf6ff363f5f490409960f0db562eac78d4886e3d977c14e101170a938af2')
        for f in r['source_files']:
            raw = subprocess.check_output(['git','show',r['source_commit']+':'+f['path']],cwd=PASTA.parents[1])
            self.assertEqual(hashlib.sha256(raw).hexdigest(),f['sha256'])
        absent = subprocess.run(['git','cat-file','-e',r['source_commit']+':pesquisas-paralelas/economia/consultas_reinicio_economia.py'],
                                cwd=PASTA.parents[1],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        self.assertNotEqual(absent.returncode,0)

    def test_recorded_original_replay_checks_all_fourteen_new_leaf_calls(self):
        replay(self)

    def test_widths_and_protected_indices(self):
        p = bytearray(range(64)); e = bytearray(276000)
        e[999*276+8] = 255
        self.assertEqual(nivel_pesquisa(p,0x100,0xbeef0003),3)
        self.assertEqual(tipo_estrutura(e,0xa55a03e7),255)
        for action in (lambda:nivel_pesquisa(p,4,0),lambda:nivel_pesquisa(p,0,0x103),
                       lambda:definir_ramo_pesquisa(p,0x104,7),lambda:tipo_estrutura(e,1000)):
            before = bytes(p)
            with self.assertRaises(ValueError):action()
            self.assertEqual(bytes(p),before)

    def test_one_byte_write_through_slice_and_live_reads(self):
        arena = bytearray(range(96)); p = memoryview(arena)[19:83]
        expected = bytearray(arena); expected[19+2*16+4] = 254
        definir_ramo_pesquisa(p,0x102,0x12fe)
        self.assertEqual(arena,expected)
        arena[19+16+3] = 213
        self.assertEqual(nivel_pesquisa(p.toreadonly(),1,3),213)

    def test_signed_views_and_read_only_query_buffers(self):
        p = array.array('b',[-1]*64)
        self.assertEqual(nivel_pesquisa(memoryview(p),0,0),255)
        definir_ramo_pesquisa(memoryview(p),0,257)
        self.assertEqual(p[4],1)
        self.assertEqual(nivel_pesquisa(bytes(64),0,0),0)
        with self.assertRaises(ValueError):definir_ramo_pesquisa(bytes(64),0,3)

    def test_buffer_shape_guards_precede_stores(self):
        for p in (None,bytes(63),memoryview(bytearray(128))[::2],
                  memoryview(bytearray(64)).cast('B',(4,16)),array.array('H',[0]*32)):
            with self.assertRaises(ValueError):nivel_pesquisa(p,0,0)
            with self.assertRaises(ValueError):definir_ramo_pesquisa(p,0,7)
        with self.assertRaises(ValueError):tipo_estrutura(bytes(276),0)

    def test_type_is_raw_and_observes_later_live_mutation(self):
        e = bytearray(276000)
        e[8] = 255
        self.assertEqual(tipo_estrutura(memoryview(e).toreadonly(),0),255)
        e[5],e[4],e[8] = 3,200,17
        self.assertEqual(tipo_estrutura(e,0x10000),17)


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional original x86: RISING_EMULAR=1')
class DiferencialConsultasReinicioEconomia(unittest.TestCase):
    bancadas = []

    def test_fresh_twenty_original_returns_match_frozen_observations_and_python(self):
        from bancada_consultas_reinicio_economia import BancadaConsultasReinicioEconomia
        b = BancadaConsultasReinicioEconomia()
        type(self).bancadas.append(b)
        for caso, frozen in zip(cenarios(),evidencia()['captures']):
            b.carregar(caso)
            self.assertEqual(b.estado(),frozen['inicial'])
            for c, observed in zip(caso['chamadas'],frozen['chamadas']):
                self.assertEqual(b.chamar(c),observed)
        self.assertEqual((b.execucoes,b.retornos),(20,20))
        replay(self)


if __name__=='__main__':unittest.main()
