"""Full unit loader composition against independent native selection state."""
import hashlib
import json
import os
from pathlib import Path
import random
import struct
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OWNED))
from ambiente_missoes import CD
from carregador_unidades import carregar_unidades_missao,DependenciaCargaUnidades
from entradas import tipos_originais,bloco_unidades
from capturar_original import sparse_fixture
from formatos import Leitor
from bonus_unidades import BonusUnidades


class CapturasSelecaoCarga(unittest.TestCase):
    def test_original_only_complete_entry_snapshots(self):
        report=json.loads((OWNED/'evidencias/captura-selecao-carga-original.json').read_text())
        types=tipos_originais()
        bonuses=BonusUnidades(bytes((i*19+71)&255 for i in range(1872)))
        for case in report['cases']:
            data=((CD/'WORLD/MONDE01.ETA').read_bytes() if case['name']=='MONDE01' else
                  struct.pack('<HH',0,784) if case['name']=='empty' else sparse_fixture())
            self.assertEqual(hashlib.sha256(data).hexdigest(),case['input_sha256'])
            pool,flags=bytearray(b'\xa5'*220800),bytearray(b'\x11\x22\x33\x44')
            selections=bytearray((i*23+0x53)&255 for i in range(2048))
            reader=Leitor(data,case['offset'])
            modifier=None if case['dependency_stop'] else lambda owner,kind:bonuses.consultar(owner,kind,12)
            if case['dependency_stop']:
                with self.assertRaises(DependenciaCargaUnidades):
                    carregar_unidades_missao(reader,pool,flags,types,selections,modificador12=modifier)
            else:
                carregar_unidades_missao(reader,pool,flags,types,selections,modificador12=modifier)
            self.assertEqual((selections.hex(),hashlib.sha256(pool).hexdigest(),flags.hex(),reader.posicao),
                             (case['selections_hex'],case['unit_pool_sha256'],case['loader_bytes_hex'],case['cursor']))

    def test_selection_effect_precedes_continuation_validation(self):
        selections=bytearray(b'\x63'*2048)
        flags=bytearray(b'abcd')
        reader=Leitor(b'')
        with self.assertRaises(ValueError):
            carregar_unidades_missao(reader,bytearray(1),flags,bytes(1300),selections)
        self.assertEqual((reader.posicao,flags),(0,b'abcd'))
        self.assertEqual([selections[i:i+2] for i in (0,512,1024,1536)],[b'\0\0']*4)
        self.assertEqual(sum(v!=0x63 for v in selections),8)

    def test_invalid_selection_guard_precedes_loader_effects(self):
        reader=Leitor(b'')
        pool,flags=bytearray(b'\x63'*220800),bytearray(b'abcd')
        with self.assertRaises(ValueError):
            carregar_unidades_missao(reader,pool,flags,bytes(1300),bytes(2048))
        self.assertEqual((reader.posicao,flags,pool[0xbd]),(0,b'abcd',0x63))


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional intact-x86: RISING_EMULAR=1')
class DiferencialSelecaoCarga(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_unidades import BancadaCargaUnidades
        cls.native=BancadaCargaUnidades()
        cls.types=tipos_originais()
        cls.bonuses=bytes((i*19+71)&255 for i in range(1872))
        cls.provider=BonusUnidades(cls.bonuses)

    def compare(self,data,offset=0,seed=1,missing=False):
        rng=random.Random(seed)
        pool,flags,selections=(bytearray(rng.randbytes(n)) for n in (220800,4,2048))
        self.native.carregar(data,offset,pool,flags,self.types,self.bonuses,
                             selecoes=selections,parar_bonus=missing)
        reader=Leitor(data,offset)
        if missing:
            with self.assertRaises(DependenciaCargaUnidades):
                carregar_unidades_missao(reader,pool,flags,self.types,selections)
        else:
            carregar_unidades_missao(reader,pool,flags,self.types,selections,
                modificador12=lambda owner,kind:self.provider.consultar(owner,kind,12))
        self.assertEqual((bytes(pool),bytes(flags)),self.native.estado())
        self.assertEqual(bytes(selections),self.native.estado_selecoes())
        self.assertEqual(reader.posicao,self.native.cursor)

    def test_all_original_unit_blocks_and_inherited_selection_lists(self):
        for seed,path in enumerate(sorted((CD/'WORLD').glob('*.ETA'))):
            data=path.read_bytes()
            self.compare(data,bloco_unidades(data)['offset'],seed)

    def test_empty_sparse_and_query_stop(self):
        self.compare(struct.pack('<HH',0,784))
        self.compare(sparse_fixture())
        self.compare(sparse_fixture(),missing=True)
