"""M2.2 preparation: N-frame phase naming and the CRT fseek/fgets fixtures (CPU-free)."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ambiente_missoes  # noqa: F401
from fronteiras_carga_missao import ArquivosCRT
from oraculo_quadro_missao import eh_fase_quadro, nomes_fases
from vinculos_declarados import ParadaVinculoDeclarado
from test_carga_missao_original import CPUFalsa, ChamadaFalsa


class MidiaFalsa:
    def __init__(self, arquivos):
        self.arquivos, self.lidos = arquivos, {}

    def ler(self, caminho):
        dados = self.arquivos.get(bytes(caminho))
        if dados is None:
            return None, None
        self.lidos[caminho.decode()] = dict(path=caminho.decode())
        return caminho.decode(), dados


class TestFases(unittest.TestCase):
    def test_frame1_keeps_committed_names_and_later_frames_are_numbered(self):
        self.assertEqual(nomes_fases(1), ('between_frames', 'frame1'))
        self.assertEqual(nomes_fases(7), ('between_frames7', 'frame7'))
        for f in ('load_tail', 'between_frames', 'frame1', 'between_frames12', 'frame12'):
            self.assertTrue(eh_fase_quadro(f), f)
        for f in ('startup', 'oracle', 'isolated', 'frames', 'frame', '', None):
            self.assertFalse(eh_fase_quadro(f), f)


class TestCRTDeclarado(unittest.TestCase):
    def abrir(self, dados, modo=b'rb'):
        cpu = CPUFalsa()
        cpu.mem_map(0, 0x2000)
        cpu.mem_write(0x100, b'X.TXT\0')
        cpu.mem_write(0x200, modo+b'\0')
        crt = ArquivosCRT(MidiaFalsa({b'X.TXT': dados}))
        fluxo = crt.fopen(ChamadaFalsa(cpu, 0x100, 0x200))
        return cpu, crt, fluxo

    def test_fgets_keeps_lf_stops_at_n_minus_1_and_returns_zero_at_eof(self):
        cpu, crt, f = self.abrir(b'ab\ncdefgh')
        self.assertEqual(crt.fgets_crt(ChamadaFalsa(cpu, 0x400, 10, f)), 0x400)
        self.assertEqual(cpu.mem_read(0x400, 4), b'ab\n\0')
        self.assertEqual(crt.fgets_crt(ChamadaFalsa(cpu, 0x400, 4, f)), 0x400)
        self.assertEqual(cpu.mem_read(0x400, 4), b'cde\0')
        crt.fgets_crt(ChamadaFalsa(cpu, 0x400, 100, f))
        self.assertEqual(cpu.mem_read(0x400, 4), b'fgh\0')
        self.assertEqual(crt.fgets_crt(ChamadaFalsa(cpu, 0x400, 100, f)), 0)
        self.assertEqual(crt.fgets_crt(ChamadaFalsa(cpu, 0x500, 1, f)), 0x500)
        self.assertEqual(cpu.mem_read(0x500, 1), b'\0')

    def test_fgets_text_mode_cr_is_not_declared(self):
        cpu, crt, f = self.abrir(b'ab\r\n', b'r')
        with self.assertRaises(ParadaVinculoDeclarado):
            crt.fgets_crt(ChamadaFalsa(cpu, 0x400, 10, f))

    def test_fseek_whence_and_bounds(self):
        cpu, crt, f = self.abrir(b'0123456789')
        self.assertEqual(crt.fseek_crt(ChamadaFalsa(cpu, f, 4, 0)), 0)
        self.assertEqual(crt.fseek_crt(ChamadaFalsa(cpu, f, 0xfffffffe, 1)), 0)
        crt.fgets_crt(ChamadaFalsa(cpu, 0x400, 3, f))
        self.assertEqual(cpu.mem_read(0x400, 3), b'23\0')
        self.assertEqual(crt.fseek_crt(ChamadaFalsa(cpu, f, 0xffffffff, 2)), 0)
        crt.fgets_crt(ChamadaFalsa(cpu, 0x400, 5, f))
        self.assertEqual(cpu.mem_read(0x400, 2), b'9\0')
        with self.assertRaises(ParadaVinculoDeclarado):
            crt.fseek_crt(ChamadaFalsa(cpu, f, 0, 3))
        with self.assertRaises(ParadaVinculoDeclarado):
            crt.fseek_crt(ChamadaFalsa(cpu, f, 0xfffffff0, 0))


if __name__ == '__main__':
    unittest.main()
