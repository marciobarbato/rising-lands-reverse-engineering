"""Fresh original continuation, binding ABI/budget and readonly query checks."""
import os
import struct
import unittest

from test_classificacao_remapeamento import (preparar_classificacao, executar_classificacao,
                                            ClassificacaoRemapeamento, HANDLE)
from consultas_unidades import tipo_unidade, tipo_unidade_monstro


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1','Optional x86: RISING_EMULAR=1')
class DiferencialClassificacaoRemapeamento(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_classificacao_remapeamento import BancadaClassificacaoRemapeamento
        cls.bancada=BancadaClassificacaoRemapeamento()
        cls.lock_stops=cls.binding_limits=0

    def comparar(self,nome):
        from vinculos_declarados import ParadaVinculoDeclarado
        b=self.bancada;m,nula,desconhecido,_=preparar_classificacao(nome)
        b.carregar_classificacao(m,nula,desconhecido)
        if desconhecido:
            with self.assertRaises(ParadaVinculoDeclarado):b.classificar()
            type(self).lock_stops += 1
        else:regs=b.classificar()
        recursos,r=executar_classificacao(m,nula,desconhecido)
        self.assertEqual(b.conferir_remapeamento(m),[])
        self.assertEqual(b.classes(),bytes(recursos.memoria))
        eventos=b.vinculos_declarados.eventos
        self.assertEqual([e['arguments'] for e in eventos],[[0,65536],[0 if nula else HANDLE]])
        if isinstance(r,ClassificacaoRemapeamento):
            self.assertEqual(regs['EIP'],0x42ef8b)
            self.assertEqual(b.consultas_naturais,list(range(65536)))
        elif nula:
            from emulador import RETORNO
            self.assertEqual((regs['EIP'],regs['EAX'] & 255),(RETORNO,0))
            self.assertEqual(b.consultas_naturais,[])
        else:
            self.assertEqual(eventos[-1]['status'],'stopped')
            self.assertTrue(recursos.alocada)

    def test_fresh_all_original_capture_inputs_and_partial_lock_stop(self):
        from cenarios_classificacao_remapeamento import CASOS_CLASSIFICACAO
        for nome in CASOS_CLASSIFICACAO:self.comparar(nome)

    def test_finite_binding_budget_stops_before_next_handler_with_frame_retained(self):
        from vinculos_declarados import LimiteVinculosDeclarados
        from remapeamento_mundo import iniciar_remapeamento
        from emulador import x86
        m,*_=preparar_classificacao('mixed');b=self.bancada;b.carregar_classificacao(m)
        with self.assertRaises(LimiteVinculosDeclarados):b.classificar(limite_vinculos=1)
        type(self).binding_limits += 1
        self.assertEqual(b.parada_limite_vinculos['handled'],1)
        self.assertEqual(len(b.vinculos_declarados.eventos),1)
        esp=b.cpu.reg_read(x86.UC_X86_REG_ESP)
        self.assertEqual(struct.unpack('<II',b.cpu.mem_read(esp,8)),(0x42eecc,HANDLE))
        iniciar_remapeamento(m)
        self.assertEqual(b.conferir_remapeamento(m),[])
        self.assertEqual(b.classes(),b'\xa5'*65536)

    def test_iat_metadata_and_engine_boundary_guards_precede_mutation(self):
        b=self.bancada;antes=bytes(b.cpu.mem_read(0x4e19a0,4))
        with self.assertRaises(ValueError):b.declarar_importacao(0x4e19a0,'NotAnImport',0,lambda c:0)
        with self.assertRaises(ValueError):b.declarar_vinculo(0x457122,'HealAsBackend',(),lambda c:0,natureza='backend')
        self.assertEqual(bytes(b.cpu.mem_read(0x4e19a0,4)),antes)

    def test_direct_type_and_monster_queries_all_bytes_edge_slots_preserve_consumed_state(self):
        from emulador import BancadaX86,UNIDADES
        b=BancadaX86();self.bancadas_auxiliares=(b,)
        type(self).bancada_consultas=b
        intervalos=((0x442025,0x442045),(0x4422dd,0x4422e8),(0x4422da,0x4422dd))
        m,*_=preparar_classificacao('zero');b.cpu.mem_write(UNIDADES,bytes(m.unidades))
        for indice in (0,799):
            for tipo in range(256):
                m.unidades[indice*276+1]=tipo;b.cpu.mem_write(UNIDADES+indice*276+1,bytes([tipo]))
                r=b.executar(0x442025,intervalos,dict(EAX=0xabcd0000|indice,EDX=0x12345678))
                self.assertEqual((r['EAX'] & 255,r['EDX']),(tipo_unidade(m,indice),0x12345678))
                self.assertEqual(bytes(b.cpu.mem_read(UNIDADES,220800)),bytes(m.unidades))
        for tipo in range(256):
            r=b.executar(0x4422dd,intervalos,dict(EAX=0xabcd0000|tipo,EDX=0x12345678))
            self.assertEqual((r['EAX'] & 255,r['EDX']),(int(tipo_unidade_monstro(tipo)),0x12345678))

    def test_native_io_wrappers_execute_original_bodies_over_declared_crt_boundaries(self):
        from emulador import BancadaX86,UNIDADES,RETORNO
        b=BancadaX86();self.bancadas_auxiliares=(b,)
        type(self).bancada_io=b;type(self).origens_io=[]
        nome,modo,destino,handle=UNIDADES,UNIDADES+128,0x509954,UNIDADES+512
        b.cpu.mem_write(nome,b'MONDE01.ETA\0');b.cpu.mem_write(modo,b'rb\0')
        dados=b'original-fixture'
        def abrir(c):
            self.assertEqual(c.argumentos,(nome,modo))
            self.assertEqual(c.ler(modo,3),b'rb\0')
            return handle
        def ler(c):
            self.assertEqual(c.argumentos,(destino,len(dados),1,handle))
            c.escrever(destino,dados)
            return 1
        b.declarar_vinculo(0x48c71f,'CRT.fopen',('EAX','EDX'),abrir,natureza='io')
        b.declarar_vinculo(0x48c97b,'CRT.fread',('EAX','EDX','EBX','ECX'),ler,natureza='io')
        intervalos=((0x458420,0x458430),(0x458461,0x458476))
        type(self).origens_io.append('0x458420')
        r=b.executar(0x458420,intervalos,dict(EAX=nome,EDX=modo))
        self.assertEqual((r['EIP'],r['EAX'] & 255),(RETORNO,1))
        self.assertEqual(struct.unpack('<I',b.cpu.mem_read(0x4e1d1c,4))[0],handle)
        type(self).origens_io.append('0x458461')
        r=b.executar(0x458461,intervalos,dict(EAX=destino,EDX=len(dados),EBX=0x1234,ECX=0x5678))
        self.assertEqual((r['EIP'],r['EAX'],r['EBX'],r['ECX']),(RETORNO,1,0x1234,0x5678))
        self.assertEqual(bytes(b.cpu.mem_read(destino,len(dados))),dados)
        self.assertEqual([e['status'] for e in b.vinculos_declarados.eventos],['returned','returned'])
        self.assertEqual(b.retomadas_vinculos,2)
