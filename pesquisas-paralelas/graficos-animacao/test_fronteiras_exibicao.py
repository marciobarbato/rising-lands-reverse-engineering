"""Declared DirectDraw backend: original wrappers execute natively over declared COM objects."""
import re
import struct
import sys
import unittest

from extrair_evidencias import imagem_pe
from fechamento_escritas_affgame import varrer, CODIGO as CODIGO_IMAGEM
from graficos import RAIZ

sys.path.insert(0, str(RAIZ.parents[1]/'ferramentas'))
from emulador import BancadaX86, UNIDADES  # noqa: E402
from vinculos_declarados import ParadaVinculoDeclarado  # noqa: E402
from fronteiras_exibicao import ExibicaoDeclarada, VT_DD, VT_SUPERFICIE, VT_PALETA  # noqa: E402

CODIGO = [(0x401000, 0x493c00)]
# DDInit, DDSetPalette, DDLockSurface, DDUnlockSurface, DDFlipPage, DDRestoreAll: every COM offset is a declared handler.
USADOS = {'IDirectDraw': {0x14, 0x18, 0x50, 0x54}, 'IDirectDrawSurface': {0x1c, 0x60, 0x64, 0x6c, 0x7c, 0x80}, 'IDirectDrawPalette': {0x18}}


class TabelasEstaticasTest(unittest.TestCase):
    def test_vtable_offsets_and_names_are_unique_and_aligned(self):
        for tabela in (VT_DD, VT_SUPERFICIE, VT_PALETA):
            self.assertEqual([o for o, n, a in tabela], list(range(0, 4*len(tabela), 4)))
            self.assertEqual(len({n for o, n, a in tabela}), len(tabela))

    def test_every_com_offset_in_the_executed_wrappers_has_semantics(self):
        base, _ = imagem_pe(); simbolos = {}
        for linha in (RAIZ.parents[1]/'relatorios/simbolos-originais.tsv').read_text().splitlines()[1:]:
            a, n = linha.split('\t')[:2]; simbolos.setdefault(n, int(a, 16))
        achados = set()
        for nome in ('DDInit', 'DDSetPalette', 'DDLockSurface', 'DDUnlockSurface', 'DDFlipPage', 'DDRestoreAll'):
            _, _, indiretos, _ = varrer(simbolos[nome])
            achados |= {int(m.group(1), 16) for a, t in indiretos for m in [re.search(r'\+ (0x[0-9a-f]+)\]$', t)] if m}
        declarados = USADOS['IDirectDraw'] | USADOS['IDirectDrawSurface'] | USADOS['IDirectDrawPalette']
        self.assertEqual(achados, declarados)
        por_interface = dict(IDirectDraw={o: n for o, n, a in VT_DD}, IDirectDrawSurface={o: n for o, n, a in VT_SUPERFICIE},
            IDirectDrawPalette={o: n for o, n, a in VT_PALETA})
        nomes = {i: {por_interface[i][o] for o in os_} for i, os_ in USADOS.items()}
        self.assertEqual(nomes, dict(IDirectDraw={'CreatePalette', 'CreateSurface', 'SetCooperativeLevel', 'SetDisplayMode'},
            IDirectDrawSurface={'BltFast', 'IsLost', 'Lock', 'Restore', 'SetPalette', 'Unlock'}, IDirectDrawPalette={'SetEntries'}))


class NativoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b = BancadaX86(); cls.ex = ExibicaoDeclarada().instalar(cls.b)

    def chamar(self, entrada, **regs):
        return self.b.executar(entrada, CODIGO, regs, limite_instrucoes=1000000)

    def u(self, endereco, n=4): return int.from_bytes(self.b.cpu.mem_read(endereco, n), 'little')

    def test_ddinit_lock_unlock_palette_and_flip_run_natively_over_the_declared_objects(self):
        b, ex = self.b, self.ex
        self.assertEqual(self.chamar(0x43f50b, EAX=0x1770, EDX=1)['EAX'] & 0xff, 1)
        self.assertEqual((self.u(0x49a018, 2), self.u(0x49a01a, 2), self.u(0x508724, 2), self.u(0x508726, 2), self.u(0x4e17a0)), (800, 600, 25, 17, 800))
        self.assertEqual([e['method'] for e in ex.eventos[:5]], ['DirectDrawCreate', 'SetCooperativeLevel', 'SetDisplayMode', 'CreateSurface', 'CreateSurface'])
        self.assertEqual((ex.eventos[1]['hwnd'], ex.eventos[1]['flags']), (0x1770, 0x13))
        self.assertEqual([(e['role'], e['width'], e['height'], e['pitch']) for e in ex.eventos[3:5]], [('primaria', 800, 600, 800), ('offscreen', 800, 600, 800)])
        tabela = bytes((i*3+j) & 255 for i in range(256) for j in range(3)); b.cpu.mem_write(UNIDADES, tabela)
        self.chamar(0x43ee31, EAX=UNIDADES)
        paleta = next(iter(ex.paletas.values())).entradas
        self.assertEqual([paleta[4*i:4*i+3] for i in range(256)], [tabela[3*i:3*i+3] for i in range(256)])
        ponteiro = self.chamar(0x43f3b4)['EAX']
        self.assertEqual((ponteiro, self.u(0x4e17a4), self.u(0x4e17a8)), (ex.superficies[self.u(0x4e1790)].base, ponteiro, 1))
        pixels = bytes((i*7) & 255 for i in range(800*600)); b.cpu.mem_write(ponteiro, pixels)
        self.assertEqual(self.chamar(0x43f445, EAX=ponteiro)['EAX'] & 0xff, 1)
        self.assertEqual((self.u(0x4e17a8), self.u(0x4e17a4)), (0, 0))
        self.chamar(0x43f14f, EAX=1)
        blits = [e for e in ex.eventos if e['method'] == 'BltFast']
        self.assertEqual([e['rect'] for e in blits], [[0, 0, 800, 544], [0, 544, 800, 600]])
        self.assertEqual(ex.pixels('primaria'), pixels)

    def test_unsupported_com_slot_stops_with_its_name(self):
        if not self.ex.superficies: self.chamar(0x43f50b, EAX=0x1770, EDX=1)
        with self.assertRaises(ParadaVinculoDeclarado) as erro: self.chamar(0x43ef40)  # DDGetDC -> IDirectDrawSurface::GetDC
        self.assertIn('GetDC', str(erro.exception))


if __name__ == '__main__': unittest.main()
