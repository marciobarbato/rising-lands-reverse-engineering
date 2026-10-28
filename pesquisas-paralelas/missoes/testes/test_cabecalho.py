"""Independent prelude snapshots and whole-buffer native composition checks."""
import hashlib
import json
import os
from pathlib import Path
import random
import struct
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
from ambiente_missoes import CD
from carregador_cabecalho import continuar_cabecalho
from formatos import Leitor, ErroFormato
from economia import Economia


def buffers():
    return [bytearray([0xa5])*size for size in (65536, 131072, 65536, 65536)]


def state(layers, economy, dimensions, view):
    return tuple(bytes(x) for x in layers)+(bytes(economy.memoria),bytes(dimensions),bytes(view))


class CapturasCabecalho(unittest.TestCase):
    def test_original_only_captures(self):
        report = json.loads((OWNED/'evidencias/captura-cabecalho-original.json').read_text())
        data = (CD/'WORLD/MONDE01.ETA').read_bytes()
        for case in report['cases']:
            self.assertEqual(hashlib.sha256(data).hexdigest(), case['source_sha256'])
            layers, economy = buffers(), Economia(bytes((i*17+0x53)&255 for i in range(128)))
            dimensions, view = bytearray(b'\xa5'*4), bytearray(b'\x11\x22\x33\x44')
            result = continuar_cabecalho(Leitor(data), *layers, economy, dimensions, view, case['camera'])
            self.assertEqual([hashlib.sha256(x).hexdigest() for x in state(layers,economy,dimensions,view)], case['output_sha256'])
            self.assertEqual(result.fim, case['cursor'])
            self.assertEqual(result.rotina_seguinte, 0x42ee1c)

    def test_strict_read_failure_retains_prior_layer(self):
        layers, economy = buffers(), Economia(bytes([0x63])*128)
        dimensions, view = bytearray(b'abcd'), bytearray(b'efgh')
        data = b'V0.3'+b'\x19'*65536+b'\x20'*100
        reader = Leitor(data)
        with self.assertRaises(ErroFormato):
            continuar_cabecalho(reader,*layers,economy,dimensions,view,0)
        self.assertEqual(layers[0], b'\x19'*65536)
        self.assertEqual(layers[1], b'\xa5'*131072)
        self.assertEqual((reader.posicao,economy.memoria,dimensions,view),(65540,b'c'*128,b'abcd',b'efgh'))

    def test_resource_failure_keeps_normalization_and_prior_setter(self):
        data = bytearray((CD/'WORLD/MONDE01.ETA').read_bytes())
        data[0x30004+65535] = 54
        data[0x40004+65535] = 88
        class RaisingEconomy(Economia):
            def atribuir(self, player, resource, amount):
                if player == 1:
                    raise RuntimeError('deliberate callback boundary')
                super().atribuir(player,resource,amount)
        layers, economy = buffers(), RaisingEconomy(bytes([0x63])*128)
        dimensions, view = bytearray(b'abcd'), bytearray(b'efgh')
        reader = Leitor(data)
        with self.assertRaises(RuntimeError):
            continuar_cabecalho(reader,*layers,economy,dimensions,view,0)
        self.assertEqual((layers[2][-1],layers[3][-1]),(66,1))
        self.assertEqual(reader.posicao,0x50008)
        self.assertEqual(economy.registro(1,1),b'c'*8)
        self.assertEqual((dimensions,view),(b'abcd',b'efgh'))

    def test_invalid_input_before_reads(self):
        data = (CD/'WORLD/MONDE01.ETA').read_bytes()
        layers, economy = buffers(), Economia()
        layers[2] = bytes(65536)
        reader = Leitor(data)
        with self.assertRaises(ValueError):
            continuar_cabecalho(reader,*layers,economy,bytearray(4),bytearray(4),0)
        self.assertEqual(reader.posicao,0)
        self.assertEqual(layers[0],b'\xa5'*65536)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1','Optional intact-x86: RISING_EMULAR=1')
class DiferencialCabecalho(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_cabecalho import BancadaCabecalho
        cls.native = BancadaCabecalho()

    def compare(self,data,camera,seed):
        rng = random.Random(seed)
        resources,dimensions,view = (rng.randbytes(n) for n in (128,4,4))
        regs = self.native.carregar(data,camera=camera,resources=resources,dimensions=dimensions,view=view)
        layers,economy = buffers(),Economia(resources)
        dimensions,view = bytearray(dimensions),bytearray(view)
        reader = Leitor(data)
        result = continuar_cabecalho(reader,*layers,economy,dimensions,view,camera)
        self.assertEqual(state(layers,economy,dimensions,view),self.native.estado())
        self.assertEqual((reader.posicao,result.rotina_seguinte),(self.native.cursor,regs['EIP']))
        self.assertEqual(self.native.resource_calls,[(p,r,struct.unpack_from('<H',data,0x50004+q*8+p*2)[0])
                                                    for q,r in enumerate((1,2,0)) for p in range(4)])

    def test_all_original_headers_and_camera_values(self):
        for index,path in enumerate(sorted((CD/'WORLD').glob('*.ETA'))):
            for camera in (0,1,2,3,4,255):
                with self.subTest(map=path.name,camera=camera):
                    self.compare(path.read_bytes(),camera,index*256+camera)

    def test_raw_layer_dimensions_resources_and_camera_wrap(self):
        data = bytearray((CD/'WORLD/MONDE01.ETA').read_bytes())
        data[:4] = b'ABCD'  # Original prelude skips four bytes, no version check.
        for cell in (0,63,255,256,65535):
            data[4+cell] = 255
            data[0x30004+cell] = 54
            data[0x40004+cell] = 254
        struct.pack_into('<12H',data,0x50004,0,65535,9999,10000,1,255,256,32768,65534,123,456,789)
        for size in ((1,256),(256,1),(0,65535)):
            struct.pack_into('<HH',data,0x5001c,*size)
            for camera in (0x100,0x103,-1):
                self.compare(data,camera,camera & 65535)
