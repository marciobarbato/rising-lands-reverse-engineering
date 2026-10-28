"""Original auxiliary prefix snapshots and retained mine/AI bytes."""
import hashlib
import json
import os
from pathlib import Path
import random
import struct
import subprocess
import sys
import unittest

OWNED=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OWNED))
from ambiente_missoes import CD,ROOT
from carregador_auxiliares import carregar_minas_missao,carregar_ataques_missao,carregar_minas_e_ataques
from capturar_auxiliares import bloco_sintetico
from formatos import Leitor,ler_eta,ErroFormato


class CapturasAuxiliares(unittest.TestCase):
    def test_original_only_prefix_snapshots(self):
        report=json.loads((OWNED/'evidencias/captura-auxiliares-original.json').read_text())
        for case in report['cases']:
            data=(bloco_sintetico(0,0) if case['name']=='empty' else bloco_sintetico(20,100)
                  if case['name']=='full' else (CD/'WORLD/MONDE01.ETA').read_bytes())
            self.assertEqual(hashlib.sha256(data).hexdigest(),case['source_sha256'])
            mines,attacks=bytearray(b'\x63'*80),bytearray(b'\xa5'*1004)
            result=carregar_minas_e_ataques(Leitor(data,case['offset']),mines,attacks)
            self.assertEqual((mines.hex(),attacks.hex(),result.fim),
                             (case['mines_hex'],case['attacks_hex'],case['cursor']))
            self.assertEqual(result.rotina_seguinte,0x47bcc7)

    def test_actual_economy_buffer_identity_and_unloaded_reserve_retention(self):
        # Existing economic/graphics flat `construcoes` names collide. Keep the
        # actual provider test isolated; do not rewrite either owner's imports.
        script='''import sys,struct
sys.path.insert(0,sys.argv[1])
from extracao import RecursosTerreno
sys.path.insert(0,sys.argv[2])
from carregador_auxiliares import carregar_minas_missao
from formatos import Leitor
r=RecursosTerreno(minas=b"\\x63"*80)
memory=r.minas
carregar_minas_missao(Leitor(struct.pack("<H",0)),memory)
assert r.minas is memory
for i in range(20):
    assert memory[i*4:i*4+2]==b"\\0\\0"
    assert r.capacidade_mina(i)==0x6363
'''
        result=subprocess.run([sys.executable,'-B','-c',script,
                               str(ROOT/'pesquisas-paralelas/economia'),str(OWNED)],
                              capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        attacks=bytearray(b'\xa5'*1004)
        carregar_ataques_missao(Leitor(struct.pack('<HH',0,8)),attacks)
        self.assertEqual((attacks[9:1000:10],attacks[1000:]),(b'\xa5'*100,bytes(4)))

    def test_reader_failure_retains_prior_loader_and_initialization(self):
        data=struct.pack('<H',1)+b'\x19'*4+struct.pack('<HH',1,8)+b'\x20'*7
        reader=Leitor(data);mines,attacks=bytearray(b'\x63'*80),bytearray(b'\xa5'*1004)
        with self.assertRaises(ErroFormato):
            carregar_minas_e_ataques(reader,mines,attacks)
        self.assertEqual((reader.posicao,mines[:8]),(10,b'\x19'*4+b'\0\0cc'))
        self.assertEqual(attacks[:10],b'\xc8'+b'\xff'*7+b'\0\xa5')
        self.assertEqual(attacks[1000:],bytes(4))

    def test_input_guards_and_protected_headers_keep_reached_effects(self):
        reader=Leitor(b'')
        with self.assertRaises(ValueError):
            carregar_minas_missao(reader,bytes(80))
        self.assertEqual(reader.posicao,0)
        mines=bytearray(b'\x63'*80);reader=Leitor(struct.pack('<H',21))
        with self.assertRaises(ValueError):
            carregar_minas_missao(reader,mines)
        self.assertEqual((reader.posicao,mines),(2,b'c'*80))
        attacks=bytearray(b'\xa5'*1004);reader=Leitor(struct.pack('<HH',101,8))
        with self.assertRaises(ValueError):
            carregar_ataques_missao(reader,attacks)
        self.assertEqual((reader.posicao,attacks[1000:],attacks[9]),(4,bytes(4),0xa5))


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional intact-x86: RISING_EMULAR=1')
class DiferencialAuxiliares(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_auxiliares import BancadaAuxiliares
        cls.native=BancadaAuxiliares()

    def compare(self,data,offset,caller,seed=1):
        rng=random.Random(seed)
        mines,attacks=bytearray(rng.randbytes(80)),bytearray(rng.randbytes(1004))
        self.native.carregar(data,offset,mines,attacks,caller)
        reader=Leitor(data,offset)
        carregar_minas_e_ataques(reader,mines,attacks)
        self.assertEqual((bytes(mines),bytes(attacks)),self.native.estado())
        self.assertEqual(reader.posicao,self.native.cursor)

    def test_both_original_callers_all_maps(self):
        for seed,path in enumerate(sorted((CD/'WORLD').glob('*.ETA'))):
            data=path.read_bytes();offset=next(b['offset'] for b in ler_eta(data)['blocos'] if b['nome']=='tabela_47534a')
            for caller in ('MissionLoad','MissionLoadName'):
                self.compare(data,offset,caller,seed)

    def test_every_supported_count_in_both_prefixes(self):
        for caller in ('MissionLoad','MissionLoadName'):
            for count in range(21):
                self.compare(bloco_sintetico(count,0),0,caller,count)
            for count in range(101):
                self.compare(bloco_sintetico(2,count),0,caller,256+count)
