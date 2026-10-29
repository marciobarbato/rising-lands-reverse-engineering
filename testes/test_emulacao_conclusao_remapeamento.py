"""Fresh intact whole-remap observations and a separate final-u16-tail fixture."""
import json
import os
from pathlib import Path
import struct
import unittest

from modelo_capturas_conclusao_remapeamento import conferir_captura, expandir
from cenarios_conclusao_remapeamento import preparar_conclusao

RAIZ = Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional x86: RISING_EMULAR=1')
class DiferencialConclusaoRemapeamento(unittest.TestCase):
    def conferir_imagem(self, atual, captura):
        esperado=expandir(captura)
        atual={int(a,16):dados for a,dados in atual.items()}
        self.assertEqual(set(atual),set(esperado))
        for a,dados in atual.items():
            # Whole-byte equality with bounded diagnostics, never a megabyte
            # unittest/difflib pretty-print of two complete image dictionaries.
            self.assertTrue(dados==esperado[a],f'Whole mapped block mismatch at0x{a:x}')

    @classmethod
    def setUpClass(cls):
        from bancada_conclusao_remapeamento import BancadaConclusaoRemapeamento
        cls.bancada = BancadaConclusaoRemapeamento()
        cls.observacoes = []

    def test_fresh_seven_cases_equal_frozen_whole_images_and_translation(self):
        from emulador import unicorn, x86
        from vinculos_declarados import ParadaVinculoDeclarado
        b=self.bancada
        for nome in ('stage17-original-MONDE01.json','stage17-original-discriminating.json'):
            for c in json.loads((RAIZ/'relatorios'/nome).read_text())['cases']:
                with self.subTest(case=c['name']):
                    m,_=preparar_conclusao(c['name']);b.carregar_conclusao(m,c['name'])
                    self.conferir_imagem(b.imagem_inteira(),c['initial'])
                    if c['outcome']=='declared_fixture_stop':
                        with self.assertRaises(ParadaVinculoDeclarado):b.concluir_original()
                    elif c['outcome']=='expected_original_null_lock_fault':
                        with self.assertRaises(unicorn.UcError) as erro:b.concluir_original()
                        self.assertEqual((erro.exception.errno,b.cpu.reg_read(x86.UC_X86_REG_EIP)),
                                         (unicorn.UC_ERR_WRITE_UNMAPPED,0x42efd9))
                    else:
                        regs=b.concluir_original()
                        self.assertEqual(regs['EAX'],int(c['eax'],16))
                    self.conferir_imagem(b.imagem_inteira(),c['final'])
                    n=b.estado_conclusao()
                    for k in ('resources','component_allocations','stack_high_water_bytes','write_trace','bindings','registers','stopped_eip'):
                        self.assertTrue(n[k]==c['native_state'][k],k)
                    type(self).observacoes.append(conferir_captura(c))

    def test_final_tail_reads_low_u16_and_restores_original_saved_register_frame(self):
        from emulador import BancadaX86,RETORNO
        from bancada_conclusao_remapeamento import REGISTRADORES_CHAMADOR
        b=BancadaX86();self.bancadas_auxiliares=(b,);type(self).bancada_cauda=b
        regs_salvos=['EBP','EDI','ESI','EDX','ECX','EBX']
        for contador, esperado in ((0x3fff,1),(0x4000,0),(0xffff,0),(0x10000,1)):
            quadro={0x18:struct.pack('<I',contador),0x38:struct.pack('<I',RETORNO)}
            quadro.update({0x20+i*4:struct.pack('<I',REGISTRADORES_CHAMADOR[n]) for i,n in enumerate(regs_salvos)})
            regs=b.executar(0x42f1c3,[(0x42eed4,0x42eedb),(0x42f1c3,0x42f1e1)],pilha=quadro)
            self.assertEqual((regs['EIP'],regs['EAX'] & 255),(RETORNO,esperado))
            self.assertEqual({n:regs[n] for n in regs_salvos},{n:REGISTRADORES_CHAMADOR[n] for n in regs_salvos})
