"""Independent original table snapshots and exact native loading comparisons."""
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
from carregador_condicoes import carregar_condicoes_fim,carregar_objetivos
from formatos import Leitor,ErroFormato,ler_eta


class CapturasCondicoes(unittest.TestCase):
    def test_original_only_snapshots(self):
        from capturar_condicoes import objetivo_sintetico
        report = json.loads((OWNED/'evidencias/captura-condicoes-original.json').read_text())
        mission = (CD/'WORLD/MONDE01.ETA').read_bytes()
        for case in report['cases']:
            fin = bytearray((i*13+0x63)&255 for i in range(114))
            obj = bytearray((i*17+0x52)&255 for i in range(804))
            data = (struct.pack('<HH',0,10) if case['name']=='empty_fin' else
                    objetivo_sintetico() if case['name']=='synthetic_objectives' else mission)
            reader = Leitor(data,case['offset'])
            if case['entry']=='0x458b05':
                carregar_condicoes_fim(reader,fin)
            else:
                carregar_objetivos(reader,obj)
            self.assertEqual((fin.hex(),obj.hex(),reader.posicao),(case['fin_hex'],case['objectives_hex'],case['cursor']))

    def test_empty_fin_preserves_status_result_and_other_record_bytes(self):
        memory = bytearray([0x63])*114
        carregar_condicoes_fim(Leitor(struct.pack('<HH',0,10)),memory)
        self.assertEqual(memory[100:],b'c'*14)
        self.assertEqual(memory[:100],b''.join(b'\xff'+b'c'*9 for _ in range(10)))

    def test_fin_read_failure_keeps_prior_reset_copy_and_status(self):
        memory = bytearray([0x63])*114
        data = struct.pack('<HH',2,10)+b'\x19'*10+b'\x20'*9
        reader = Leitor(data)
        with self.assertRaises(ErroFormato):
            carregar_condicoes_fim(reader,memory)
        self.assertEqual((reader.posicao,memory[:10],memory[10:20],memory[104:106]),
                         (14,b'\x19'*10,b'\xff'+b'c'*9,b'\0c'))

    def test_objective_read_failure_keeps_word_before_discarded_flag(self):
        memory = bytearray([0x63])*804
        reader = Leitor(b'\x34\x12')
        with self.assertRaises(ErroFormato):
            carregar_objetivos(reader,memory)
        self.assertEqual((reader.posicao,memory[:2],memory[2:800],memory[800:]),
                         (2,b'\x34\x12',b'\xff'*798,b'c'*4))

    def test_input_protection_precedes_effects_and_header_protection_retains_reset(self):
        for function,size in ((carregar_condicoes_fim,114),(carregar_objetivos,804)):
            reader = Leitor(b'')
            with self.assertRaises(ValueError):
                function(reader,bytes(size))
            self.assertEqual(reader.posicao,0)
        memory = bytearray([0x63])*114
        reader = Leitor(struct.pack('<HH',11,10))
        with self.assertRaises(ValueError):
            carregar_condicoes_fim(reader,memory)
        self.assertEqual((reader.posicao,memory[104:]),(4,b'c'*10))
        self.assertEqual(memory[0],255)


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional intact-x86: RISING_EMULAR=1')
class DiferencialCondicoes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_condicoes import BancadaCondicoes
        cls.native = BancadaCondicoes()

    def compare(self,entry,data,offset=0,seed=1):
        rng = random.Random(seed)
        fin,obj = bytearray(rng.randbytes(114)),bytearray(rng.randbytes(804))
        self.native.carregar(entry,data,offset,fin,obj)
        reader = Leitor(data,offset)
        if entry==0x458b05:
            carregar_condicoes_fim(reader,fin)
        else:
            carregar_objetivos(reader,obj)
        self.assertEqual((bytes(fin),bytes(obj)),self.native.estado())
        self.assertEqual(reader.posicao,self.native.cursor)

    def test_all_original_tables(self):
        for index,path in enumerate(sorted((CD/'WORLD').glob('*.ETA'))):
            data = path.read_bytes()
            blocks = ler_eta(data)['blocos']
            for entry,name in ((0x458b05,'tabela_458b05'),(0x47c404,'listas_por_jogador')):
                self.compare(entry,data,next(b['offset'] for b in blocks if b['nome']==name),index)

    def test_fin_counts_patterns_and_opaque_codes(self):
        for count in range(11):
            for pattern in (0,0x63,255):
                records = bytes((pattern+i*23)&255 for i in range(count*10))
                self.compare(0x458b05,struct.pack('<HH',count,10)+records,seed=pattern+count*256)

    def test_objective_flags_and_u16_values(self):
        for flag in (0,1,255):
            data = b''.join(struct.pack('<HB',(0,1,255,256,65535)[i%5],flag) for i in range(400))
            self.compare(0x47c404,data,seed=flag)
