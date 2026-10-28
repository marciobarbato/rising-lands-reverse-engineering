"""Whole structure-pool captures, sparse file IDs and both original callers."""
import hashlib
import json
import os
from pathlib import Path
import random
import struct
import sys
import unittest

OWNED=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OWNED))
from ambiente_missoes import CD
from carregador_estruturas import carregar_estruturas_missao
from capturar_estruturas import bloco_sintetico
from formatos import Leitor,ler_eta,ErroFormato


class CapturasEstruturas(unittest.TestCase):
    def test_independent_original_snapshots(self):
        report=json.loads((OWNED/'evidencias/captura-estruturas-original.json').read_text())
        for case in report['cases']:
            data=(struct.pack('<HH',0,204) if case['name']=='empty' else bloco_sintetico()
                  if case['name']=='sparse_repeated' else (CD/'WORLD/MONDE01.ETA').read_bytes())
            self.assertEqual(hashlib.sha256(data).hexdigest(),case['source_sha256'])
            pool=bytearray(b'\xa5'*276000)
            reader=Leitor(data,case['offset'])
            result=carregar_estruturas_missao(reader,pool)
            self.assertEqual((hashlib.sha256(pool).hexdigest(),result.fim),
                             (case['output_pool_sha256'],case['cursor']))
            for item in case['changed']:
                self.assertEqual(pool[item['index']*276:(item['index']+1)*276].hex(),item['record_hex'])

    def test_committed_raw_reader_and_retained_tail(self):
        from integracao.providers import load_graphics_structures
        ler_estruturas_eta=load_graphics_structures().ler_estruturas_eta
        data=(CD/'WORLD/MONDE01.ETA').read_bytes()
        pool=bytearray(b'\x63'*276000)
        result=carregar_estruturas_missao(Leitor(data,ler_eta(data)['blocos'][0]['offset']),pool)
        raw=ler_estruturas_eta(data)
        self.assertEqual(result.indices,tuple(r['indice'] for r in raw))
        for record in raw:
            p=record['indice']*276
            self.assertEqual(pool[p:p+204],record['bytes'])
            self.assertEqual(pool[p+204:p+276],b'c'*72)

    def test_strict_read_failure_preserves_previous_copy(self):
        data=struct.pack('<HH',2,204)+struct.pack('<H',999)+b'\x19'*204+struct.pack('<H',7)+b'\x20'*203
        pool=bytearray(b'\x63'*276000);reader=Leitor(data)
        with self.assertRaises(ErroFormato):
            carregar_estruturas_missao(reader,pool)
        self.assertEqual((reader.posicao,pool[999*276:999*276+204],pool[7*276:8*276]),
                         (212,b'\x19'*204,b'c'*276))

    def test_input_guards_preserve_reached_state(self):
        reader=Leitor(b'')
        with self.assertRaises(ValueError):
            carregar_estruturas_missao(reader,bytes(276000))
        self.assertEqual(reader.posicao,0)
        for data,cursor in ((struct.pack('<HH',0,203),4),
                            (struct.pack('<HHH',1,204,1000),6)):
            pool=bytearray(b'\x63'*276000);reader=Leitor(data)
            with self.assertRaises(ValueError):
                carregar_estruturas_missao(reader,pool)
            self.assertEqual((reader.posicao,pool),(cursor,b'c'*276000))


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional intact-x86: RISING_EMULAR=1')
class DiferencialEstruturas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_estruturas import BancadaCargaEstruturas
        cls.native=BancadaCargaEstruturas()

    def compare(self,data,offset,caller,seed=1):
        pool=bytearray(random.Random(seed).randbytes(276000))
        self.native.carregar(data,offset,pool,caller)
        reader=Leitor(data,offset)
        carregar_estruturas_missao(reader,pool)
        self.assertEqual((bytes(pool),reader.posicao),(self.native.estado(),self.native.cursor))

    def test_both_original_callers_all_maps(self):
        for seed,path in enumerate(sorted((CD/'WORLD').glob('*.ETA'))):
            data=path.read_bytes();offset=ler_eta(data)['blocos'][0]['offset']
            for caller in ('MissionLoad','MissionLoadName'):
                self.compare(data,offset,caller,seed)

    def test_empty_sparse_and_count_above_pool_capacity(self):
        long=struct.pack('<HH',1001,204)+(struct.pack('<H',999)+b'\x19'*204)*1001
        for caller in ('MissionLoad','MissionLoadName'):
            for data in (struct.pack('<HH',0,204),bloco_sintetico(),long):
                self.compare(data,0,caller)
