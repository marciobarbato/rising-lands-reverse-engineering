"""CPU-free replay of original city-message evidence and explicit callback ABI."""
from pathlib import Path
import json
import lzma
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OWNED))
import ambiente_ia_runtime  # noqa: F401
from capturar_mensagem_cidade_ia import CAPTURA, comparar, MemoriaCapturada
from entrada_estruturas import ArgumentoNaoPassado
from mensagem_cidade_ia import ARGUMENTOS, mensagem_cidade


class Cidade(unittest.TestCase):
    def test_casos_originais(self):
        cases = json.loads(lzma.decompress(CAPTURA.read_bytes()))['cases']
        self.assertEqual(len(cases),27)
        self.assertEqual(sum(c['stop'] is not None for c in cases),4)
        for i,c in enumerate(cases):
            with self.subTest(case=i,kind=c['kind']):
                self.assertTrue(comparar(c)['equal'])

    def test_argumento_ausente_ou_incerto_antes_de_ler(self):
        for k,mask in ARGUMENTOS.items():
            for r in ({r:0 for r in ARGUMENTOS if r != k},dict(EAX=0,EDX=3,EBX=0,_incertos={k:mask & -mask})):
                with self.subTest(register=k), self.assertRaises(ArgumentoNaoPassado):
                    mensagem_cidade(None,r)

    def test_registros_preservados_sao_incertos_quando_omitidos(self):
        c = json.loads(lzma.decompress(CAPTURA.read_bytes()))['cases'][3]
        m = MemoriaCapturada(c['read_before_write'])
        r = mensagem_cidade(m,dict(EAX=0,EDX=3,EBX=0))
        self.assertEqual(r['_incertos'],dict.fromkeys(('ECX','ESI','EDI','EBP'),0xffffffff))
        self.assertEqual((r['EAX'],r['EBX'],r['EDX']),(1,0,0))
        r = mensagem_cidade(m,dict(EAX=0,EDX=3,EBX=0,ECX=0x12340000,_incertos={'ECX':0xffff}))
        self.assertEqual((r['ECX'],r['_incertos']['ECX']),(0x12340000,0xffff))
        self.assertFalse(m.escritos)


if __name__ == '__main__':
    unittest.main()
