"""CRT fseek/fgets as inventoried I/O boundaries: static owner evidence and registration rules."""
import hashlib
from pathlib import Path
import re
import struct
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
EXE = RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE'
FSEEK, FGETS, FOPEN = 0x48cda2, 0x48ce96, 0x48c71f


def _bytes(raw, inicio, fim):
    from extrair_fundacoes_quadro import _bytes as ler
    return ler(raw, inicio, fim)


def chamadores(raw, alvo):
    codigo = _bytes(raw, 0x401000, 0x401000 + 601088)
    for m in re.finditer(b'\xe8', codigo):
        a = 0x401000 + m.start()
        if m.start() + 5 <= len(codigo) and (a + 5 + struct.unpack_from('<i', codigo, m.start() + 1)[0]) & 0xffffffff == alvo:
            yield a


@unittest.skipUnless(EXE.exists(), 'Original executable not available locally')
class FronteirasIOCRT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = EXE.read_bytes()
        import csv
        with (RAIZ / 'evidencias/simbolos-importados.tsv').open() as f:
            cls.simbolos = {int(r['endereco'], 16): r['nome_original'] for r in csv.DictReader(f, delimiter='\t')}

    def test_table_contains_exactly_the_reviewed_entries(self):
        from emulador import FRONTEIRAS_IO
        self.assertEqual(FRONTEIRAS_IO, frozenset((0x458420, 0x45844c, 0x458461, 0x45848b, 0x48c71f, 0x48c97b,
                                                   0x48c80b, FSEEK, FGETS)))
        self.assertEqual((self.simbolos[FSEEK], self.simbolos[FGETS]), ('fseek', 'fgets'))

    def test_intact_bodies_and_register_abi(self):
        # Pinned intact bodies: fseek 0x48cda2..0x48ce96, fgets 0x48ce96..0x48cf11.
        self.assertEqual(hashlib.sha256(_bytes(self.raw, FSEEK, FGETS)).hexdigest(), 'debc184562810af2082c2ae35e0904df1a58690b737c0d00e9553b4eae93f463')
        self.assertEqual(hashlib.sha256(_bytes(self.raw, FGETS, 0x48cf11)).hexdigest(), '96e2f198008dd7b97d5b468d312aaa70328f150ee2d162721a5608ef0e5cc836')
        # fseek: push ecx/esi/edi; ECX = FILE* (EAX), ESI = offset (EDX); EBX (whence) is only read.
        self.assertEqual(_bytes(self.raw, FSEEK, FSEEK + 7), bytes.fromhex('51565789c189d6'))
        # fgets: push ecx/esi/edi/ebp; ESI = buf (EAX), ECX = n (EDX), FILE* in EBX; ends 'mov eax, esi'.
        self.assertEqual(_bytes(self.raw, FGETS, FGETS + 14), bytes.fromhex('5156575583ec0489c689d18b4310'))
        self.assertEqual(_bytes(self.raw, 0x48cf07, 0x48cf11), bytes.fromhex('89f083c4045d5f5e59c3'))
        self.assertEqual(_bytes(self.raw, 0x48ce92, 0x48ce96), bytes.fromhex('5f5e59c3'))

    def test_every_call_site_takes_its_file_from_the_inventoried_fopen(self):
        nome = lambda a: next(f'{self.simbolos[b]}+0x{a - b:x}' for b in sorted(self.simbolos, reverse=True) if b <= a)
        self.assertEqual(sorted(nome(a) for a in chamadores(self.raw, FGETS)),
                         ['FileReadLine+0xd', 'iaProbLoadTextRules+0x74'])
        self.assertEqual(sorted(nome(a) for a in chamadores(self.raw, FSEEK)),
                         ['FileSeek+0x10', 'FileSize+0x29', 'FileSize+0xf', 'ReadLZSImage+0x4c', '__open_flags+0x183'])
        self.assertIn('iaProbLoadTextRules+0x11', [nome(a) for a in chamadores(self.raw, FOPEN)])
        self.assertIn('LoadLZSAt+0x1d', [nome(a) for a in chamadores(self.raw, FOPEN)])
        # FileReadLine/FileSeek/FileSize load the FILE* from FileOpen's handle global 0x4e1d1c.
        for a, padrao in ((0x4584a4, '8b1d1c1d4e00'), (0x45848f, '8b0d1c1d4e00'), (0x4584c4, 'a11c1d4e00')):
            self.assertEqual(_bytes(self.raw, a, a + len(padrao) // 2).hex(), padrao)

    def test_registration_accepts_io_only_at_the_exact_entries(self):
        from emulador import BancadaX86
        b = BancadaX86()
        b.declarar_vinculo(FSEEK, 'CRT.fseek', ('EAX', 'EDX', 'EBX'), lambda c: 0, natureza='io')
        b.declarar_vinculo(FGETS, 'CRT.fgets', ('EAX', 'EDX', 'EBX'), lambda c: c.argumentos[0], natureza='io')
        for endereco, natureza in ((FGETS + 1, 'io'), (0x48cf11, 'io'), (FSEEK, 'backend')):
            with self.assertRaises(ValueError):
                BancadaX86().declarar_vinculo(endereco, 'X', ('EAX',), lambda c: 0, natureza=natureza)


if __name__ == '__main__':
    unittest.main()
