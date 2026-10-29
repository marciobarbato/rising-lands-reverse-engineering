"""Original FileReadLine/FileSeek bodies over declared CRT fgets/fseek fixtures (RISING_EMULAR=1)."""
import os
from pathlib import Path
import struct
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional x86: RISING_EMULAR=1')
class WrappersSobreFronteirasCRT(unittest.TestCase):
    def setUp(self):
        from emulador import BancadaX86, UNIDADES
        self.b = BancadaX86()
        self.handle, self.buffer = UNIDADES + 0x800, UNIDADES + 0x100
        self.b.cpu.mem_write(0x4e1d1c, struct.pack('<I', self.handle))     # FileOpen's FILE* global

    def test_file_read_line_over_fgets(self):
        from emulador import RETORNO
        linhas = [b'PRIMEIRA LINHA\n', b'fim']
        chamadas = []

        def fgets(c):
            buf, n, fluxo = c.argumentos
            chamadas.append((buf, n, fluxo))
            if not linhas:
                return 0                           # EOF before any byte: NULL
            linha = linhas.pop(0)[:max(n - 1, 0)]
            c.escrever(buf, linha + b'\0')
            return buf

        self.b.declarar_vinculo(0x48ce96, 'CRT.fgets', ('EAX', 'EDX', 'EBX'), fgets, natureza='io')
        intervalo = ((0x4584a3, 0x4584bc),)
        resultados = []
        for _ in range(3):
            r = self.b.executar(0x4584a3, intervalo, dict(EAX=self.buffer, EDX=0xabcd0040, EBX=0x1234, ECX=0x77))
            resultados.append((r['EIP'], r['EAX'] & 0xff, r['EBX'], r['ECX']))
            if len(resultados) == 1:
                self.assertEqual(bytes(self.b.cpu.mem_read(self.buffer, 16)), b'PRIMEIRA LINHA\n\0')
        self.assertEqual(resultados, [(RETORNO, 1, 0x1234, 0x77)] * 2 + [(RETORNO, 0, 0x1234, 0x77)])
        # FileReadLine passes EDX & 0xffff and the FILE* from 0x4e1d1c in EBX.
        self.assertEqual(chamadas, [(self.buffer, 0x40, self.handle)] * 3)
        self.assertEqual([e['status'] for e in self.b.vinculos_declarados.eventos], ['returned'] * 3)

    def test_file_seek_over_fseek(self):
        from emulador import RETORNO
        chamadas = []

        def fseek(c):
            chamadas.append(c.argumentos)
            return 0 if c.argumentos[2] in (0, 1, 2) else 0xffffffff

        self.b.declarar_vinculo(0x48cda2, 'CRT.fseek', ('EAX', 'EDX', 'EBX'), fseek, natureza='io')
        intervalo = ((0x45848b, 0x4584a3),)
        saidas = []
        for deslocamento, origem in ((0x300, 0x100), (0xfffffff0, 0x201), (5, 0x7)):
            r = self.b.executar(0x45848b, intervalo, dict(EAX=deslocamento, EDX=origem, EBX=0x5555, ECX=0x6666))
            saidas.append((r['EIP'], r['EAX'], r['EBX'], r['ECX']))
        # FileSeek: EAX = FILE*, EDX = offset, EBX = DL (whence); EBX/ECX restored.
        self.assertEqual(chamadas, [(self.handle, 0x300, 0), (self.handle, 0xfffffff0, 1), (self.handle, 5, 7)])
        self.assertEqual(saidas, [(RETORNO, 0, 0x5555, 0x6666), (RETORNO, 0, 0x5555, 0x6666),
                                  (RETORNO, 0xffffffff, 0x5555, 0x6666)])

    def test_file_size_over_fseek_and_ftell(self):
        from emulador import RETORNO
        posicao, chamadas = [0], []

        def fseek(c):
            fluxo, deslocamento, origem = c.argumentos
            chamadas.append(('fseek', fluxo, deslocamento, origem))
            posicao[0] = {0: deslocamento, 2: 0x1234 + deslocamento}[origem]
            return 0

        def ftell(c):
            chamadas.append(('ftell', c.argumentos[0]))
            return posicao[0]

        self.b.declarar_vinculo(0x48cda2, 'CRT.fseek', ('EAX', 'EDX', 'EBX'), fseek, natureza='io')
        self.b.declarar_vinculo(0x48cf11, 'CRT.ftell', ('EAX',), ftell, natureza='io')
        r = self.b.executar(0x4584bc, ((0x4584bc, 0x4584f0),), dict(EAX=0x99, EBX=0x1111, ECX=0x2222, EDX=0x3333))
        # FileSize: fseek(end), ftell, fseek(set 0); EAX = size; EBX/ECX/EDX restored.
        self.assertEqual((r['EIP'], r['EAX'], r['EBX'], r['ECX'], r['EDX']), (RETORNO, 0x1234, 0x1111, 0x2222, 0x3333))
        self.assertEqual(chamadas, [('fseek', self.handle, 0, 2), ('ftell', self.handle), ('fseek', self.handle, 0, 0)])


if __name__ == '__main__':
    unittest.main()
