"""M2.1 MONDE01 first-frame oracle: CPU-free guards plus one gated native replay.

The light tests check the declared frame-phase Windows answers with fake
binding calls and the boundary table against the intact code bytes. They do
not validate x86 behavior. The optional native test (RISING_EMULAR=1) re-runs
the intact original from the program start through frame 1 and compares the
committed original-only capture.
"""
import json
import os
from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ambiente_missoes
from oraculo_carga_missao import PULOS_INICIO
from oraculo_quadro_missao import (EntradasQuadro, FRONTEIRAS_QUADRO, WindowsQuadro, eax_lido_pelo_chamador,
                                   limpeza_estatica)
from vinculos_declarados import ParadaVinculoDeclarado
from test_carga_missao_original import ChamadaFalsa, CPUFalsa, entradas

CAPTURA = ambiente_missoes.OWNED/'evidencias/captura-quadro1-monde01-original.json'
RASTRO = ambiente_missoes.OWNED/'evidencias/rastro-quadro1-monde01.json'
EXE = ambiente_missoes.CD/'INSTALHD/RISING.EXE'


def quadro(**mudar):
    base = dict(base=entradas(), cursor=(0, 0), registradores_chamador=dict(ECX=0, EDX=0, ESI=0, EDI=0, EBP=0))
    base.update(mudar)
    return EntradasQuadro(**base)


def codigo():
    dados = EXE.read_bytes()[0x400:0x400+0x92c00]
    return lambda a, n: dados[a-0x401000:a-0x401000+n]


def simbolos():
    tabela = {}
    for linha in (ambiente_missoes.ROOT/'relatorios/simbolos-originais.tsv').read_text().splitlines()[1:]:
        endereco, nome = linha.split('\t')[:2]
        tabela[nome] = int(endereco, 16)
    return tabela


class TestQuadroDeclarado(unittest.TestCase):
    def test_frame_inputs_must_be_complete(self):
        with self.assertRaises(ValueError):
            quadro(cursor=(0,))
        with self.assertRaises(ValueError):
            quadro(registradores_chamador=dict(ECX=0, EDX=0))

    def test_frame_answers_only_in_frame_phases(self):
        cpu = CPUFalsa()
        cpu.mem_map(0, 0x4000)
        w = WindowsQuadro(entradas(teclas=()), quadro(cursor=(7, 9)))
        with self.assertRaises(ParadaVinculoDeclarado):
            w.tecla(ChamadaFalsa(cpu, 0x1b))
        with self.assertRaises(ParadaVinculoDeclarado):
            w.cursor(ChamadaFalsa(cpu, 0x100))
        w.fase = 'frame1'
        self.assertEqual(w.tecla(ChamadaFalsa(cpu, 0x1b)), 0)
        self.assertEqual(w.cursor(ChamadaFalsa(cpu, 0x100)), 1)
        self.assertEqual(struct.unpack('<ii', cpu.mem_read(0x100, 8)), (7, 9))
        self.assertEqual(w.mensagem(ChamadaFalsa(cpu, 0x200, 0, 0, 0, 0)), 0)
        with self.assertRaises(ParadaVinculoDeclarado):
            w.mensagem(ChamadaFalsa(cpu, 0x200, 0x1234, 0, 0, 0))

    def test_startup_key_script_still_precedes_not_pressed_answers(self):
        cpu = CPUFalsa()
        cpu.mem_map(0, 0x1000)
        w = WindowsQuadro(entradas(teclas=((0x0d, 0x8000),)), quadro())
        w.fase = 'load_tail'
        with self.assertRaises(ParadaVinculoDeclarado):
            w.tecla(ChamadaFalsa(cpu, 0x1b))
        self.assertEqual(w.tecla(ChamadaFalsa(cpu, 0x0d)), 0x8000)

    @unittest.skipUnless(EXE.exists(), 'Original executable not present')
    def test_boundary_cleanup_matches_original_ret_immediates(self):
        ler, sym = codigo(), simbolos()
        # Shared epilogues and thunks are followed by the intra-procedural walk.
        for nome, (_, limpeza, _) in FRONTEIRAS_QUADRO.items():
            self.assertEqual(limpeza_estatica(ler, sym[nome]), ('rets', [limpeza]), nome)
        self.assertEqual({n: v[:2] for n, v in FRONTEIRAS_QUADRO.items() if n in PULOS_INICIO}, PULOS_INICIO)

    @unittest.skipUnless(EXE.exists(), 'Original executable not present')
    def test_caller_eax_classifier_on_known_sites(self):
        ler = codigo()
        self.assertEqual(eax_lido_pelo_chamador(ler, 0x474b61)[0], 'read')       # mov [0x508f70], eax
        self.assertEqual(eax_lido_pelo_chamador(ler, 0x474b8f)[0], 'overwritten')  # mov eax, 1

    @unittest.skipUnless(CAPTURA.exists() and RASTRO.exists(), 'Frame-1 capture not committed yet')
    def test_committed_capture_is_complete_and_trace_matches(self):
        cap = json.loads(CAPTURA.read_bytes())
        self.assertTrue(cap['frame1_return']['reached'])
        self.assertFalse(cap['translation_executed'])
        self.assertTrue(cap['m1_path']['entry_equal_committed'])
        self.assertTrue(cap['m1_path']['final_equal_capture_v2'])
        self.assertTrue(cap['m1_path']['binding_log_equal_capture_v2'])
        self.assertEqual([p['phase'] for p in cap['phases']], ['load_tail', 'between_frames', 'frame1'])
        rastro = json.loads(RASTRO.read_bytes())
        self.assertTrue(rastro['complete'])
        self.assertEqual(rastro['phases'], cap['entry_trace'])


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional intact-x86: RISING_EMULAR=1')
class TestQuadroNativo(unittest.TestCase):
    def test_program_start_frame1_reproduces_committed_capture(self):
        import capturar_quadro_missao_original as cq
        from oraculo_quadro_missao import BancadaQuadroMissaoOriginal
        cap = json.loads(CAPTURA.read_bytes())
        ni = cap['named_inputs']['m1']
        b = BancadaQuadroMissaoOriginal(cq.entradas_quadro(ni['allocation_fill'], ni['clock_ms'][0]), segundos=120)
        b.iniciar_relogio()
        b.executar_inicio()
        b.executar_mission_load(60)
        resumos = []
        for correr in (lambda: b.executar_cauda_carga(600), lambda: b.executar_entre_quadros(120),
                       lambda: b.executar_quadro(600)):
            correr()
            resumos.append(b.resumo_imagem(b.imagem()))
        self.assertEqual(resumos, [p['state_after']['summary'] for p in cap['phases']])
        self.assertEqual(b.sha256_codigo(), cap['code_integrity']['after'])


if __name__ == '__main__':
    unittest.main()
