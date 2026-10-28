"""Original filename snapshots, exact query order and signed-byte boundaries."""
import itertools
import json
import os
from pathlib import Path
import sys
import unittest

OWNED=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OWNED))
from nome_missao import nome_arquivo_missao,DependenciaNomeMissao
from capturar_nome import jogadores_sinteticos
from mercado import Mercado


class CapturasNome(unittest.TestCase):
    def test_independent_original_snapshots(self):
        report=json.loads((OWNED/'evidencias/captura-nome-original.json').read_text())
        for case in report['cases']:
            output=bytearray(b'\xa5'*64)
            provider=Mercado(jogadores=jogadores_sinteticos(case['values']))
            queries=[]
            def query(owner,other):
                queries.append([owner,other])
                if len(queries)==case['stop_query']:
                    raise RuntimeError('deliberate native query checkpoint')
                return provider.simpatia(owner,other)
            if case['stop_query']:
                with self.assertRaises(RuntimeError):
                    nome_arquivo_missao(case['number'],output,variante_u8=case['variant'],simpatia=query)
            else:
                result=nome_arquivo_missao(case['number'],output,variante_u8=case['variant'],simpatia=query)
                self.assertEqual(result,bytes(output).split(b'\0',1)[0])
            self.assertEqual((output.hex(),queries),(case['output_hex'],case['queries']))

    def test_missing_inputs_keep_original_prefix_without_defaults(self):
        for number,address in ((9,0x46c23e),(10,0x46dc6c),(12,0x46dc6c),(17,0x46dc6c)):
            output=bytearray(b'\xa5'*64)
            with self.assertRaises(DependenciaNomeMissao) as error:
                nome_arquivo_missao(number,output)
            self.assertEqual(error.exception.endereco,address)
            self.assertEqual(output[14],0)
            self.assertEqual(output[15:],b'\xa5'*49)

    def test_buffer_guard_and_protected_variant_retention(self):
        output=bytearray(b'\x63'*19)
        with self.assertRaises(ValueError):
            nome_arquivo_missao(1,output)
        self.assertEqual(output,b'c'*19)
        output=bytearray(b'\x63'*64)
        with self.assertRaises(ValueError):
            nome_arquivo_missao(9,output,variante_u8=4)
        self.assertEqual((output[14],output[15:]),(0,b'c'*49))

    def test_actual_economy_query_and_threshold_tie(self):
        provider=Mercado(jogadores=jogadores_sinteticos((100,90,127)))
        output=bytearray(b'\x63'*64)
        result=nome_arquivo_missao(10,output,simpatia=provider.simpatia)
        # Original initial threshold90 and chosen1 retain suffixa on this tie.
        self.assertTrue(result.endswith(b'10a.ETA'))
        self.assertEqual(output[len(result)+1:],b'c'*(63-len(result)))


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional intact-x86: RISING_EMULAR=1')
class DiferencialNome(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_nome import BancadaNomeMissao
        cls.native=BancadaNomeMissao()

    def compare(self,number,variant,values,stop=None):
        players=jogadores_sinteticos(values)
        self.native.nome(number,variant,players,b'\xa5'*64,stop_query=stop)
        output=bytearray(b'\xa5'*64)
        provider=Mercado(jogadores=players)
        queries=[]
        def query(owner,other):
            queries.append((owner,other))
            if len(queries)==stop:
                raise RuntimeError('deliberate native query checkpoint')
            return provider.simpatia(owner,other)
        if stop:
            with self.assertRaises(RuntimeError):
                nome_arquivo_missao(number,output,variante_u8=variant,simpatia=query)
        else:
            nome_arquivo_missao(number,output,variante_u8=variant,simpatia=query)
        native_output,native_players=self.native.estado()
        self.assertEqual((bytes(output),bytes(players),queries),(native_output,native_players,self.native.queries))

    def test_all_raw_number_bytes_with_poisoned_upper_bits(self):
        for number in range(256):
            self.compare(0xabcd0000|number,number%4,(90,90,90))

    def test_signed_low_byte_query_boundaries_and_all_query_branches(self):
        values=(-32768,-128,-1,0,89,90,91,127,128,32767)
        for triple in itertools.product(values,repeat=3):
            for number in (10,12,17):
                self.compare(number,0,triple)

    def test_variants_and_partial_query_failures(self):
        for variant in (0,1,2,3,0x100,0x103):
            self.compare(9,variant,(0,0,0))
        for checkpoint in (1,2,3):
            self.compare(17,0,(-1,-2,-3),checkpoint)
        for number in (10,12,17):
            self.compare(number,0,(-255,257,128))
