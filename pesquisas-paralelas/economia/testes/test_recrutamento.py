"""Débitos, ocupação e progresso; a dependência de saída permanece explícita."""
import json
import os
from pathlib import Path
import random
import struct
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(PASTA))
from construcoes import EconomiaConstrucoes
from recrutamento import Recrutamento, SaidaRecrutamentoPendente, TIPOS_RECRUTADORES


def w(mem, o, v):
    struct.pack_into('<H', mem, o, v & 65535)


def d(mem, o, v):
    struct.pack_into('<I', mem, o, v & 0xffffffff)


def preparar(tipo=1, jogador=0, indice=0):
    m = EconomiaConstrucoes(estruturas=bytes(1000 * 276))
    r = Recrutamento(m)
    w(r.selecoes, jogador * 2, indice)
    o = indice * 276
    m.estruturas[o + 8] = tipo
    m.estruturas[o + 4] = jogador
    m.estruturas[o + 5] = 3
    for recurso in (0, 1, 2):
        m.economia.atribuir(jogador, recurso, 100)
    # Passo 50: tempo, comida, peças, pedra, vida máxima.
    for t in range(26):
        struct.pack_into('<5H', r.tipos_unidades, t * 50, 10 + t, 3, 5, 4, 50 + t)
    for t in range(5):
        w(r.tipos_sortilegios, t * 46, 20 + t)
    return r


class ExemplosRecrutamento(unittest.TestCase):
    def test_recusa_cada_recurso_sem_efeitos(self):
        for recurso, saldo in ((1, 2), (2, 3), (0, 4)):
            r = preparar()
            r.mundo.economia.atribuir(0, recurso, saldo)
            antes = bytes(r.mundo.economia.memoria), bytes(r.mundo.estruturas)
            self.assertFalse(r.iniciar(0, 0))
            self.assertEqual((bytes(r.mundo.economia.memoria), bytes(r.mundo.estruturas)), antes)

    def test_tipos_aceitos_e_flag_ocupada(self):
        for tipo in range(22):
            r = preparar(tipo)
            if tipo in TIPOS_RECRUTADORES:
                with self.assertRaises(SaidaRecrutamentoPendente):
                    r.iniciar(0, 0)
            else:
                self.assertFalse(r.iniciar(0, 0))
        r = preparar()
        r.mundo.estruturas[0x74] = 255
        self.assertFalse(r.iniciar(0, 0))
        self.assertEqual(r.mundo.economia.consultar(0)[:3], (100, 100, 100))

    def test_cobranca_usa_jogador_e_ignora_dono_estado_e_compatibilidade(self):
        r = preparar(tipo=2, jogador=1, indice=999)
        o = 999 * 276
        r.mundo.estruturas[o + 4:o + 6] = b'\xff\x00'
        self.assertTrue(r.iniciar(25, 1, escolher_saida=lambda i: 0xffff))
        self.assertEqual(r.mundo.economia.consultar(1)[:3], (97, 96, 95))
        self.assertEqual(r.mundo.estruturas[o + 4:o + 6], b'\xff\x04')
        self.assertEqual(struct.unpack_from('<H', r.mundo.estruturas, o + 0x7c)[0], 65535)

    def test_campos_de_inicio_e_excecao_do_tipo20(self):
        for tipo in (1, 20):
            r = preparar(tipo)
            r.mundo.estruturas[0x7a:0x90] = b'\xa5' * 22
            with self.assertRaises(SaidaRecrutamentoPendente):
                r.iniciar(3, 0)
            s = r.mundo.estruturas
            self.assertEqual((s[5], s[0x74], s[0x7a], s[0x7b]), (4, 1, 0, 3))
            self.assertEqual(s[0x7c:0x80], b'\xa5\xa5\0\0')
            self.assertEqual(s[0x80:0x84], b'\xa5' * 4 if tipo == 20 else bytes(4))
            self.assertEqual(s[0x8c:0x90], b'\1\0\0\0')

    def test_dependencia_pendente_nao_deve_ser_reiniciada(self):
        r = preparar()
        with self.assertRaises(SaidaRecrutamentoPendente) as ctx:
            r.iniciar(0, 0)
        self.assertEqual((ctx.exception.endereco, ctx.exception.indice), (0x41d1d0, 0))
        saldo = bytes(r.mundo.economia.memoria)
        self.assertFalse(r.iniciar(0, 0))
        self.assertTrue(r.concluir_saida(0, 0x12345678))
        self.assertEqual(r.mundo.economia.memoria, saldo)
        self.assertEqual(struct.unpack_from('<H', r.mundo.estruturas, 0x7c)[0], 0x5678)

    def test_callback_observa_estado_cobrado_e_ocupado(self):
        r = preparar()
        def saida(indice):
            self.assertEqual(indice, 0)
            self.assertEqual(r.mundo.economia.consultar(0)[:3], (97, 96, 95))
            self.assertEqual(r.mundo.estruturas[0x74], 1)
            return 0x3040
        self.assertTrue(r.iniciar(0x100, 0x100, escolher_saida=saida))

    def test_divisao_zero_depois_de_comida_antes_de_pedra_e_estado(self):
        r = preparar()
        r.mundo.capacidades.configurar(0, 1, 0)
        antes = bytes(r.mundo.estruturas)
        with self.assertRaises(ZeroDivisionError):
            r.iniciar(0, 0)
        self.assertEqual(r.mundo.economia.consultar(0)[:3], (97, 100, 100))
        self.assertEqual(r.mundo.estruturas, antes)

    def test_selecao_invalida_so_e_acessada_apos_suficiencia(self):
        r = preparar()
        w(r.selecoes, 0, 65535)
        r.mundo.economia.atribuir(0, 1, 0)
        self.assertFalse(r.iniciar(0, 0))
        r.mundo.economia.atribuir(0, 1, 100)
        with self.assertRaises(ValueError):
            r.iniciar(0, 0)
        self.assertFalse(r.unidade_em_recrutamento(0, 0))
        self.assertEqual(r.status(255, 0), 0)

    def test_consulta_em_recrutamento_nao_confere_atividade(self):
        r = preparar(tipo=255)
        r.mundo.estruturas[5] = 0
        r.mundo.estruturas[0x74] = 0
        r.mundo.estruturas[0x7b] = 255
        self.assertTrue(r.unidade_em_recrutamento(255, 0))
        self.assertTrue(r.sortilegio_em_recrutamento(0x1ff, 0))

    def test_status_usa_tipo_do_argumento_e_nao_satura(self):
        r = preparar()
        r.mundo.estruturas[0x7b] = 255
        d(r.mundo.estruturas, 0x8c, 4000)
        self.assertEqual(r.status(0, 0), 400)
        self.assertEqual(r.calcular_status(0, 10), 200)
        self.assertEqual(r.calcular_status(65535, 255), 0)

    def test_status_sortilegio_e_reparo_usa_vida_maxima(self):
        r = preparar(tipo=6)
        d(r.mundo.estruturas, 0x8c, 2000)
        self.assertEqual(r.status(0, 0), 100)
        r.mundo.estruturas[8] = 14
        w(r.mundo.estruturas, 0x88, 799)
        r.unidades[799 * 276 + 1] = 25
        self.assertEqual(r.status(255, 0), 2000 // 75)
        r.mundo.estruturas[8] = 18
        r.mundo.estruturas[0x7a] = 1
        self.assertEqual(r.status(255, 0), 2000 // 75)
        r.mundo.estruturas[0x7a] = 0
        self.assertEqual(r.status(0, 0), 200)

    def test_nova_wrap_32_bits_e_sentinela(self):
        r = preparar()
        d(r.mundo.estruturas, 0x108, 0x40000000)
        self.assertEqual(r.progresso_nova(0), 0)
        r.periodo_nova = 0
        self.assertEqual(r.progresso_nova(65535), 0)
        with self.assertRaises(ZeroDivisionError):
            r.progresso_nova(0)

    def test_guardas_de_tipos_indices_e_buffers(self):
        with self.assertRaises(ValueError):
            Recrutamento(selecoes=bytes(7))
        r = preparar()
        for f, args in ((r.iniciar, (26, 0)), (r.status, (0, 4)),
                        (r.tempo_sortilegio, (5,)), (r.vida_maxima_unidade, (800,)),
                        (r.calcular_status, (1000, 0))):
            with self.assertRaises(ValueError):
                f(*args)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: RISING_EMULAR=1')
class DiferencialRecrutamento(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_recrutamento import BancadaRecrutamento
        cls.b = BancadaRecrutamento()

    def setUp(self):
        self.rng = random.Random(0x4283e2)
        self.b.sujeira_pilha = None

    def carregar(self, r):
        self.b.carregar_recrutamento(r)
        self.guardas = self.b.guardas_recrutamento()

    def conferir(self, r):
        m = r.mundo
        esperado = dict(economia=bytes(m.economia.memoria), capacidades=bytes(m.capacidades.memoria),
                        estruturas=bytes(m.estruturas), tipos=bytes(m.terreno.tipos),
                        quantidades=bytes(m.terreno.quantidades), semente=m.terreno.semente)
        esperado.update({k:bytes(getattr(r,k)) for k in ('selecoes','tipos_unidades','tipos_sortilegios','unidades')})
        esperado['periodo_nova'] = r.periodo_nova
        atual = self.b.estado()
        atual.update(self.b.estado_recrutamento())
        for campo, valor in atual.items():
            if valor != esperado[campo]:
                if isinstance(valor, bytes):
                    i = next(i for i,(a,b) in enumerate(zip(valor,esperado[campo])) if a != b)
                    self.fail(f'{campo}[{i:#x}]: x86={valor[i]:#x}, Python={esperado[campo][i]:#x}')
                self.assertEqual(valor, esperado[campo], campo)
        self.assertEqual(self.b.guardas_recrutamento(), self.guardas)
        self.assertEqual(self.b.guardas(), (b'\xa6' * 16, b'\x6a' * 16))
        self.assertEqual(self.b.outras_guardas(), (b'\xc7' * 8,b'\x7c' * 8,b'\xe9' * 8,b'\x9e' * 8,0x12345678))

    def iniciar(self, r, tipo=0, jogador=0):
        from emulador import RETORNO
        self.carregar(r)
        pendente = False
        try:
            esperado = r.iniciar(tipo, jogador)
        except SaidaRecrutamentoPendente as erro:
            pendente = True
            indice = erro.indice
        regs = {k:self.rng.getrandbits(32) for k in ('EBX','ECX','ESI','EDI','EBP')}
        atual = self.b.chamar(0x4283e2, tipo, jogador, regs)
        self.conferir(r)
        if pendente:
            self.assertEqual(atual['EIP'], 0x41d1d0)
            self.assertEqual(atual['EAX'] & 65535, indice)
            self.assertEqual(struct.unpack('<I',self.b.cpu.mem_read(atual['ESP'],4))[0],0x428640)
            debitos = [c for c in self.b.chamadas if c['entrada'] == 0x46792c]
            self.assertEqual([c['EAX'] & 255 for c in debitos], [1,2,0])
            self.assertEqual([c['EBX'] & 65535 for c in debitos], [jogador & 255] * 3)
        else:
            self.assertEqual(atual['EIP'], RETORNO)
            self.assertEqual(atual['EAX'] & 255, esperado)
            self.assertFalse(any(c['entrada'] == 0x46792c for c in self.b.chamadas))
            for nome, valor in regs.items():
                self.assertEqual(atual[nome], valor)

    def consulta(self, r, entrada, metodo, *args, mascara=0xffffffff):
        self.carregar(r)
        esperado = getattr(r, metodo)(*args)
        atual = self.b.chamar(entrada,args[0],args[1] if len(args)>1 else 0)
        self.assertEqual(atual['EAX'] & mascara, esperado)
        self.conferir(r)

    def test_iniciar_256_tipos_com_flag_livre_e_ocupada(self):
        for tipo in range(256):
            for flag in (0,255):
                r = preparar(tipo)
                r.mundo.estruturas[0x74] = flag
                self.iniciar(r)

    def test_512_inicios_com_saldos_custos_donos_indices_e_pilha_suja(self):
        for n in range(512):
            jogador, indice, tipo = n % 4, self.rng.choice((0,1,999)), n % 26
            r = preparar(self.rng.choice(tuple(sorted(TIPOS_RECRUTADORES))), jogador, indice)
            o = indice * 276
            r.mundo.estruturas[o:o+276] = self.rng.randbytes(276)
            r.mundo.estruturas[o+8] = self.rng.choice(tuple(sorted(TIPOS_RECRUTADORES)))
            r.mundo.estruturas[o+0x74] = 0
            r.mundo.economia.memoria[:] = self.rng.randbytes(128)
            for recurso, campo in ((1,2),(2,6),(0,4)):
                total = self.rng.randrange(65536)
                w(r.mundo.economia.memoria, jogador*32+recurso*8+2, total)
                w(r.tipos_unidades,tipo*50+campo,self.rng.randrange(total+1))
            r.mundo.capacidades.configurar(jogador,self.rng.choice((0,1,2,255,65535)),self.rng.randrange(1,65536))
            self.b.sujeira_pilha = n & 255
            self.iniciar(r,tipo | 0xaa550000,jogador | 0xbb660000)
        self.b.sujeira_pilha = None

    def test_192_recusas_por_saldo_antes_de_acessar_selecao_ou_estado(self):
        for n in range(192):
            r = preparar()
            recurso, custo = ((1,3),(2,4),(0,5))[n % 3]
            r.mundo.economia.atribuir(0,recurso,custo-1)
            if n % 2:
                w(r.selecoes,0,65535)
            self.iniciar(r)

    def test_512_consultas_em_recrutamento_incluem_sentinela_e_inatividade(self):
        for n in range(256):
            r = preparar(n)
            r.mundo.estruturas[5],r.mundo.estruturas[0x74] = n, n ^ 255
            r.mundo.estruturas[0x7b] = n
            if n % 4 == 0:
                w(r.selecoes,0,65535)
            tipo = n if n % 2 else (n+1) & 255
            for entrada, metodo in ((0x420ba5,'sortilegio_em_recrutamento'),(0x420bdf,'unidade_em_recrutamento')):
                self.consulta(r,entrada,metodo,tipo | 0x12340000,0x56780000,mascara=255)

    def test_512_status_cobrem_256_tipos_de_construcao_e_reparo(self):
        for t in range(256):
            r = preparar(t)
            tipo = t % (5 if t == 6 else 26)
            d(r.mundo.estruturas,0x8c,self.rng.getrandbits(32))
            r.mundo.estruturas[0x7b] = 255
            w(r.mundo.estruturas,0x88,799)
            r.unidades[799*276+1] = 25
            r.mundo.estruturas[0x7a] = 1
            self.consulta(r,0x423f9d,'calcular_status',0x12340000,tipo | 0xffe00000)
            self.consulta(r,0x423f83,'status',tipo | 0x11110000,0x22220000)
        # O outro ramo do heliporto e as sentinelas não leem tipos inválidos.
        r = preparar(18)
        d(r.mundo.estruturas,0x8c,0xffffffff)
        self.consulta(r,0x423f9d,'calcular_status',0,0)
        self.consulta(r,0x423f9d,'calcular_status',65535,255)
        w(r.selecoes,0,65535)
        self.consulta(r,0x423f83,'status',255,0)

    def test_256_novas_wrap_e_sentinela(self):
        for n in range(256):
            r = preparar()
            r.periodo_nova = self.rng.choice((1,50,65535))
            d(r.mundo.estruturas,0x108,self.rng.choice((0,1,0xffffffff,0x40000000,self.rng.getrandbits(32))))
            self.consulta(r,0x423e65,'progresso_nova',0x10000)
        r.periodo_nova = 0
        self.consulta(r,0x423e65,'progresso_nova',0xffffffff)

    def test_128_sufixos_isolados_com_frame_sintetico(self):
        for n in range(128):
            i = self.rng.choice((0,1,999))
            r = preparar(indice=i)
            self.carregar(r)
            celula = self.rng.getrandbits(32)
            esperado = r.concluir_saida(i,celula)
            atual = self.b.sufixo_isolado(i,celula)
            self.assertEqual(atual['EAX'] & 255,esperado)
            self.conferir(r)

    def test_40_excecoes_divisao_por_zero_com_efeitos_delimitados(self):
        from bancada_recrutamento import BancadaRecrutamento
        from emulador import unicorn,x86
        for n in range(40):
            antigo = self.b
            type(self).b = BancadaRecrutamento()
            for campo in ('execucoes','excecoes_esperadas','limites_esperados','paradas_dependencia','sufixos_isolados'):
                setattr(self.b,campo,getattr(antigo,campo))
            modo = n % 5
            r = preparar(6 if modo == 2 else 1)
            if modo == 0:
                r.mundo.capacidades.configurar(0,1,0)
                if n % 2 == 0:
                    w(r.tipos_unidades,2,0)  # Débito zero também exige recálculo.
                entrada, metodo, args, fault = 0x4283e2,'iniciar',(0,0),0x4284e6
            elif modo in (1,2):
                w(r.tipos_unidades,0,0)
                w(r.tipos_sortilegios,0,0)
                entrada, metodo, args, fault = 0x423f9d,'calcular_status',(0,0),0x423eca
            elif modo == 3:
                r.periodo_nova = 0
                entrada, metodo, args, fault = 0x423e65,'progresso_nova',(0,),0x423ea8
            else:
                r.mundo.estruturas[8] = 14 if n % 2 == 0 else 18
                r.mundo.estruturas[0x7a] = 1
                w(r.tipos_unidades,8,0)
                entrada, metodo, args, fault = 0x423f9d,'calcular_status',(0,255),0x423eca
            self.carregar(r)
            with self.assertRaises(ZeroDivisionError):
                getattr(r,metodo)(*args)
            with self.assertRaises(unicorn.UcError) as erro:
                self.b.chamar(entrada,args[0],args[1] if len(args)>1 else 0)
            self.assertEqual(erro.exception.errno,unicorn.UC_ERR_EXCEPTION)
            self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_EIP),fault)
            self.b.excecoes_esperadas += 1
            self.conferir(r)

    def test_26_tipos_reais_custos_tempo_vida_e_consultas(self):
        tipos = json.loads((PASTA.parents[1]/'relatorios/unidades.json').read_text())['unidades']
        self.assertEqual(len(tipos),26)
        for t in tipos:
            r = preparar()
            r.tipos_unidades[:] = b''.join(bytes.fromhex(a['registro_memoria_hex']) for a in tipos)
            r.unidades[1] = t['id']
            self.consulta(r,0x4410b7,'tempo_unidade',t['id'],mascara=65535)
            self.assertEqual(r.tempo_unidade(t['id']),t['tempo_recrutamento'])
            self.consulta(r,0x441108,'vida_maxima_unidade',0,mascara=65535)
            self.assertEqual(r.vida_maxima_unidade(0),t['vida_maxima'])
            for recurso in (0,1,2):
                r.mundo.economia.atribuir(0,recurso,65535)
            self.iniciar(r,t['id'],0)
            d(r.mundo.estruturas,0x8c,t['tempo_recrutamento']*100)
            self.consulta(r,0x423f83,'status',t['id'],0)
        for t in range(5):
            r = preparar()
            w(r.tipos_sortilegios,t*46,65535-t)
            self.consulta(r,0x47476a,'tempo_sortilegio',t | 0x12340000,mascara=65535)
