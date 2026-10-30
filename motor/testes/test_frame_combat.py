"""Raid projectile native captures, plus full-pool perturbed Python comparisons."""
from pinned_reference import activate, reference_file, pinned_file
SOURCE_ROOT = activate()

import base64
import ctypes as C
import hashlib
import json
from pathlib import Path
import random
import struct
import sys
import unittest
import zlib

from frame_abi import Frames
from test_frame_core_economy import Memory
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(SOURCE_ROOT/'pesquisas-paralelas/combate'))
from projeteis import PoolProjeteis
import quadro_economia as economy

CAPTURE=ROOT/'pesquisas-paralelas/combate/evidencias/captura-incursao-m2-3-original.json'
SET_CAPTURE=ROOT/'pesquisas-paralelas/combate/evidencias/captura-projectile-set-m2-3-original.json'
PINS={'pesquisas-paralelas/combate/evidencias/captura-incursao-m2-3-original.json': 'e5bab35b55f0f655a70ba311313895e963f6d990291d3b2f1f82f79bac5e4ab7', 'pesquisas-paralelas/combate/evidencias/captura-projectile-set-m2-3-original.json': '377a84541d42fe083cd17934863375a1c92aa7bbe0dc43efc8968e91d91a9aca', 'pesquisas-paralelas/combate/projeteis.py': 'a25e6f4c386410e09b96d3b94d5e787f0ed44984264312af350ccb5f44f3ce89', 'pesquisas-paralelas/economia/quadro_economia.py': '28342fb2e68f4e400e79ff321bc6eef5098628ac4941bff25fc48ff48bc38ea2'}


def data(field):
    raw=zlib.decompress(base64.b64decode(field['zlib_base64']))
    if 'sha256' in field:assert hashlib.sha256(raw).hexdigest()==field['sha256']
    return raw


class RaidCombat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for path,wanted in PINS.items():
            if hashlib.sha256(pinned_file(ROOT/path).read_bytes()).hexdigest()!=wanted:raise ValueError('ReferenceIdentityMismatch: '+path)
        cls.abi=Frames()
        fn=cls.abi.lib.rl_executar_rotina_quadro
        fn.argtypes=[C.c_uint64,C.c_uint32,C.POINTER(C.c_uint32),C.c_uint32,C.POINTER(C.c_uint32)]
        fn.restype=C.c_int32
    def run_rust(self,identifier,arguments,blocks):
        h=self.abi.create()
        try:
            self.abi.load(h,blocks)
            a=(C.c_uint32*len(arguments))(*arguments);out=C.c_uint32(0xdeadbeef)
            self.abi.check(self.abi.lib.rl_executar_rotina_quadro(h,identifier,a,len(a),C.byref(out)))
            return self.abi.snapshot(h),out.value
        finally:self.abi.free(h)
    def test_original_raid_projectile_init_set_and_calcul(self):
        capture=json.loads(CAPTURE.read_bytes());self.assertFalse(capture['translation_executed'])
        cases={(r['routine'],c['case']):c for r in capture['calls'] for c in r['cases']}
        spawn=cases['AvanceMonstre','forced-counter-9000'];calcul=cases['ProjectileCalcul','after-forced-avance-monstre']
        entry=next(e for e in spawn['entries'] if e[0]=='ProjectileInit')
        args=[int(v,16) for v in entry[2:11]];pool=0x418e2000
        before=data(spawn['pool_before'])
        actual,slot=self.run_rust(550,args,[(0x5080f0,struct.pack('<I',pool)),(pool,before)])
        self.assertEqual(slot,0);self.assertEqual(actual[pool],data(calcul['pool_before']))
        changed=[[hex(pool+i),a,b] for i,(a,b) in enumerate(zip(before,actual[pool])) if a!=b]
        self.assertEqual(changed,[c for c in spawn['changed_bytes'] if pool<=int(c[0],16)<pool+5600])
        before=data(calcul['pool_before'])
        actual,_=self.run_rust(305,[],[(0x5080f0,struct.pack('<I',pool)),(0x508f7c,struct.pack('<I',calcul['counter'])),(pool,before)])
        self.assertEqual([[hex(pool+i),a,b] for i,(a,b) in enumerate(zip(before,actual[pool])) if a!=b],calcul['changed_bytes'])
        captured=json.loads(SET_CAPTURE.read_bytes());case=captured['calls'][0]['cases'][0]
        regs={k:int(v,16) for k,v in case['entry_registers'].items()};args=[regs['EAX'],regs['EDX'],regs['EBX'],regs['ECX']]+[int(v,16) for v in case['stack_words']]
        before=data(case['pool_before']);actual,_=self.run_rust(551,args,[(0x5080f0,struct.pack('<I',pool)),(pool,before)])
        self.assertEqual([[hex(pool+i),a,b] for i,(a,b) in enumerate(zip(before,actual[pool])) if a!=b],case['changed_bytes'])
    def test_perturbed_projectile_set_all_callback_free_types(self):
        rng=random.Random(0x46e208)
        for kind in range(256):
            if kind in (26,28):continue  # required world callbacks are explicit stops
            slot=rng.randrange(100)
            args=[kind]+[rng.getrandbits(32) for _ in range(8)]
            # Exact supplied opaque initial bytes, rather than a zero-initialized pool.
            initial=bytearray(rng.randbytes(5600));expected=PoolProjeteis(bytearray(initial));expected.definir(slot,*args)
            actual,result=self.run_rust(551,[slot]+args,[(0x5080f0,struct.pack('<I',0x60000000)),(0x60000000,initial)])
            self.assertEqual(actual[0x60000000],bytes(expected.memoria),kind);self.assertEqual(result,slot)
    def test_unported_projectile_callbacks_are_named_and_atomic(self):
        for kind,address in [(26,'0x00450874'),(28,'0x00474734')]:
            blocks=[(0x5080f0,struct.pack('<I',0x60000000)),(0x60000000,bytes([0xa7])*5600)]
            h=self.abi.create()
            try:
                self.abi.load(h,blocks)
                a=(C.c_uint32*10)(0,kind,0x1234,0x2345,1,0,0,16,16,0)
                out=C.c_uint32(0xdeadbeef)
                code=self.abi.lib.rl_executar_rotina_quadro(h,551,a,10,C.byref(out))
                self.assertEqual(code,5);self.assertIn(address,self.abi.error())
                self.assertEqual(out.value,0xdeadbeef)
                self.assertEqual(self.abi.snapshot(h),dict(blocks))
            finally:self.abi.free(h)
    def test_periodic_weather_and_sympathy_perturbations(self):
        rng=random.Random(0x475118)
        for i in range(96):
            m=Memory([(0x494000,bytes(0x523000-0x494000)),(0x60000000,rng.randbytes(80))])
            m.u32(0x5080a8,0x60000000)
            for p in range(4):m.u8(0x51a990+16*p,int(rng.randrange(8)==0))
            a,b,event=rng.randrange(4),rng.randrange(4),rng.randrange(32)
            r=0x497288+16*event;m.u32(r,rng.getrandbits(32));m.u8(r+4,rng.randrange(2));m.u32(r+8,rng.randrange(16));m.u32(r+12,rng.randrange(16))
            initial=list(m.export().items());economy.atualizar_simpatia(m,a,b,event)
            actual,_=self.run_rust(254,[a,b,event],initial);self.assertEqual(actual,m.export())
            m.u32(0x508f7c,rng.choice([0,100,900,1800,8999,9000,9200,0xffffffff]));m.u32(0x497164,rng.getrandbits(32));m.u8(0x496d2c,rng.randrange(256));m.u16(0x496d2e,rng.randrange(65536))
            initial=list(m.export().items());economy.calcular_meteo(m)
            actual,_=self.run_rust(258,[],initial);self.assertEqual(actual,m.export())

if __name__=='__main__':unittest.main()
