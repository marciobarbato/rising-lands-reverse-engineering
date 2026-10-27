"""Efeitos incrementais de ganho/neutralização, com dependências delimitadas."""
import os
from pathlib import Path
import random
import struct
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
from construcoes import BASE_CONSTRUCOES, EconomiaConstrucoes
from proprietarios import (DependenciaBalaoPendente, PASSO_ORDENS_JOGADOR,
                           PropriedadeConstrucoes, inicializar_bag)


def word(mem, o):
    return struct.unpack_from('<H', mem, o)[0]


def setword(mem, o, v):
    struct.pack_into('<H', mem, o, v & 65535)


def preparar(tipo=3, jogador=0, indice=0, estado=3, dono=None):
    m = EconomiaConstrucoes(estruturas=bytes(1000 * 276))
    o = indice * 276
    m.estruturas[o + 4] = jogador if dono is None else dono
    m.estruturas[o + 5] = estado
    m.estruturas[o + 8] = tipo
    setword(m.estruturas, o + 2, 0x2020)
    p = PropriedadeConstrucoes(m, jogador_deposito=jogador)
    for j in range(4):
        setword(p.baloes, j * 8, 2)
    return p


class ExemplosProprietarios(unittest.TestCase):
    def test_ganho_cave_incrementa_word_e_pode_virar_zero(self):
        p = preparar()
        p.mundo.capacidades.configurar(0, 255, 100)
        p.inicializar_jogador(0, 0)
        self.assertEqual(p.mundo.capacidades.parametros(0)[0], 256)
        p.mundo.capacidades.configurar(0, 65535, 100)
        p.mundo.capacidades.escrever_nivel(0, 77)
        p.inicializar_jogador(0, 0)
        self.assertEqual(p.mundo.capacidades.parametros(0)[0], 0)
        self.assertEqual(p.mundo.capacidades.nivel(0), 77)

    def test_neutralizacao_estado3_so_decrementa_com_underflow(self):
        p = preparar(estado=3)
        antes = bytes(p.mundo.estruturas), bytes(p.mundo.economia.memoria)
        p.inicializar_neutro(0, 0)
        self.assertEqual(p.mundo.capacidades.parametros(0)[0], 65535)
        self.assertEqual((bytes(p.mundo.estruturas), bytes(p.mundo.economia.memoria)), antes)

    def test_neutralizacao_retira_materia_e_pedra_compete_pela_mesma_celula(self):
        p = preparar(estado=1)
        p.mundo.capacidades.configurar(0, 2, 100)
        p.mundo.economia.creditar(0, 1, 40)
        p.mundo.economia.creditar(0, 2, 40)
        p.inicializar_neutro(0, 0)
        self.assertEqual(p.mundo.economia.consultar(0)[:2], (20, 20))
        self.assertEqual(p.mundo.terreno.tipos[0x2222], 0x43)
        self.assertEqual(p.mundo.terreno.quantidades[0x2222], 20)
        self.assertEqual(sum(p.mundo.terreno.quantidades), 20)  # Pedido de pedra recusado.

    def test_deposito_usa_jogador_global_em_vez_do_argumento(self):
        p = preparar(jogador=1, estado=1)
        p.jogador_deposito = 0
        p.mundo.capacidades.configurar(1, 2, 100)
        p.mundo.capacidades.configurar(0, 4, 100)
        p.mundo.economia.creditar(0, 1, 40)
        p.inicializar_neutro(0, 1)
        self.assertEqual(p.mundo.economia.consultar(0).comida, 35)
        self.assertEqual(p.mundo.capacidades.parametros(1)[0], 1)
        self.assertEqual(p.mundo.terreno.quantidades[0x2222], 5)

    def test_ultima_biblioteca_limpa_flags_e_bag_preservando_reservados(self):
        p = preparar(6)
        p.bibliotecas[0] = 1
        p.sortilegios[:] = b'\xa5' * 20
        p.ordens[:] = b'\x83' * len(p.ordens)
        p.inicializar_neutro(0, 0)
        o = 4 * 104
        self.assertEqual(p.sortilegios[:5], bytes(5))
        self.assertEqual(p.sortilegios[5:], b'\xa5' * 15)
        self.assertEqual(word(p.ordens, o + 2), 5)
        self.assertEqual(p.ordens[o + 0x60:o + 0x66], b'\x83' * 6)

    def test_biblioteca_wrap_nao_aciona_limpeza_no_ganho_ou_underflow(self):
        p = preparar(6)
        p.sortilegios[:] = b'\xa5' * 20
        p.inicializar_neutro(0, 0)
        self.assertEqual(p.bibliotecas[0], 255)
        p.inicializar_jogador(0, 0)
        self.assertEqual(p.bibliotecas[0], 0)
        self.assertEqual(p.sortilegios, b'\xa5' * 20)

    def test_tipo20_reseta_tres_campos_sem_mudar_propriedade(self):
        p = preparar(20)
        p.mundo.estruturas[0x7a] = 9
        p.mundo.estruturas[0x104] = 7
        p.mundo.estruturas[0x108:0x10c] = b'\xff' * 4
        p.inicializar_neutro(0, 0)
        self.assertEqual((p.mundo.estruturas[0x7a], p.mundo.estruturas[0x104]), (0, 0))
        self.assertEqual(p.mundo.estruturas[0x108:0x10c], b'\x01\x00\x00\x00')
        self.assertEqual(p.mundo.estruturas[4:6], b'\x00\x03')

    def test_heliporto_cria_pendencia_e_neutralizacao_a_esvazia(self):
        p = preparar(18)
        p.inicializar_jogador(0, 0)
        o = p._pendencia(0)
        self.assertEqual((word(p.pendencias, o), word(p.pendencias, o + 2), word(p.pendencias, o + 6)), (1, 1, 16))
        self.assertEqual(p.pendencias[o + 0x42], 6)
        p.inicializar_neutro(0, 0)
        self.assertEqual(word(p.pendencias, o), 0)
        self.assertEqual(word(p.baloes, 0), 2)

    def test_balao_pendente_e_explicito_antes_dos_efeitos(self):
        for ganho, contador, endereco in ((True, 0, 0x441baa), (False, 1, 0x441d4f)):
            p = preparar(18)
            setword(p.baloes, 0, contador)
            with self.assertRaises(DependenciaBalaoPendente) as ctx:
                (p.inicializar_jogador if ganho else p.inicializar_neutro)(0, 0)
            self.assertEqual((ctx.exception.endereco, ctx.exception.jogador), (endereco, 0))
            self.assertEqual(word(p.baloes, 0), contador)
            self.assertEqual(p.mundo.contagens_tipo18[0], 0)

    def test_funcoes_nao_atribuem_dono_ou_estado_nem_recontam_tipos(self):
        p = preparar(3, jogador=0, dono=2)
        p.mundo.contagens_por_tipo[:] = b'\xa5' * 88
        p.inicializar_jogador(0, 0)
        self.assertEqual(p.mundo.estruturas[4:6], b'\x02\x03')
        self.assertEqual(p.mundo.contagens_por_tipo, b'\xa5' * 88)

    def test_argumentos_truncados_e_indices_protegidos(self):
        p = preparar(6, jogador=1, indice=2)
        p.inicializar_jogador(0x10002, 0x101)
        self.assertEqual(p.bibliotecas[1], 1)
        with self.assertRaises(ValueError):
            p.inicializar_jogador(0, 4)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: RISING_EMULAR=1')
class DiferencialProprietarios(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_proprietarios import BancadaProprietarios
        cls.b = BancadaProprietarios()

    def setUp(self):
        self.rng = random.Random(0x41be88)
        self.b.sujeira_pilha = None

    def conferir(self, p):
        m = p.mundo
        mundo = dict(economia=bytes(m.economia.memoria), capacidades=bytes(m.capacidades.memoria),
                     estruturas=bytes(m.estruturas), tipos=bytes(m.terreno.tipos),
                     quantidades=bytes(m.terreno.quantidades), semente=m.terreno.semente,
                     contagens_por_tipo=bytes(m.contagens_por_tipo), contagens_tipo18=bytes(m.contagens_tipo18))
        esperado = dict(mundo=mundo, **{n:bytes(getattr(p,n)) for n in ('bibliotecas','baloes','numeros_unidades','pendencias','ordens','sortilegios')},
                        jogador_deposito=p.jogador_deposito)
        atual = self.b.estado_propriedade()
        for campo in esperado:
            if campo == 'mundo':
                for n in mundo:self.assertEqual(atual[campo][n],mundo[n],n)
            else:self.assertEqual(atual[campo],esperado[campo],campo)
        self.assertEqual(self.b.guardas(),(b'\xa6'*16,b'\x6a'*16))
        self.assertEqual(self.b.guardas_propriedade(),(b'\xc7'*8,b'\x7c'*4,b'\xb2'*8,b'\xf1'*8,b'\x1f'*8,b'\xd3'*8,b'\x3d'*8))

    def comparar(self, p, ganho, indice=0, jogador=0):
        self.b.carregar_propriedade(p)
        (p.inicializar_jogador if ganho else p.inicializar_neutro)(indice,jogador)
        (self.b.inicializar_jogador if ganho else self.b.inicializar_neutro)(indice,jogador)
        self.conferir(p)

    def test_todos_os_256_tipos_512_chamadas(self):
        for tipo in range(256):
            for ganho in (False, True):
                j=tipo%4
                p=preparar(tipo,jogador=j)
                p.mundo.capacidades.configurar(j,1,100)
                self.comparar(p,ganho,jogador=j)

    def test_ganho_armazem_512_estados_e_pilha_suja(self):
        for n in range(512):
            j=n%4;p=preparar(3,jogador=j,indice=n%8,dono=255)
            p.mundo.economia.memoria[:]=self.rng.randbytes(128)
            p.mundo.capacidades.memoria[:]=self.rng.randbytes(24)
            count=(0,1,255,256,65534,65535,self.rng.randrange(65536))[n%7]
            p.mundo.capacidades.configurar(j,count,self.rng.randrange(1,65536))
            self.b.sujeira_pilha=(None,0xa5,0xff,0x42)[n%4]
            self.comparar(p,True,0xabcd0000|n%8,0x12340000|j)

    def test_neutralizacao_armazem_256_estados_e_jogadores_distintos(self):
        for n in range(256):
            j=n%4;p=preparar(3,jogador=j,estado=(0,1,3,4,255)[n%5])
            p.jogador_deposito=n//4%4
            for k in range(4):
                p.mundo.capacidades.configurar(k,(0,1,2,3,65535)[(n+k)%5],100)
                p.mundo.economia.creditar(k,1,self.rng.randrange(41))
                p.mundo.economia.creditar(k,2,self.rng.randrange(41))
            p.mundo.terreno.semente=self.rng.randrange(0x80000000)
            self.comparar(p,False,jogador=j)

    def test_bibliotecas_flags_e_bags_256_chamadas(self):
        for n in range(128):
            for ganho in (False,True):
                j=n%4;p=preparar(6,jogador=j,dono=255)
                p.bibliotecas[:]=self.rng.randbytes(4)
                p.bibliotecas[j]=(0,1,2,255)[n%4]
                p.sortilegios[:]=self.rng.randbytes(20)
                p.ordens[:]=self.rng.randbytes(len(p.ordens))
                self.comparar(p,ganho,jogador=j)

    def test_heliportos_baloes_existentes_e_listas_256_chamadas(self):
        for n in range(256):
            j=n%4;dono=n//4%4;p=preparar(18,jogador=j,dono=dono)
            p.mundo.contagens_tipo18[:]=self.rng.randbytes(4)
            p.numeros_unidades[:]=self.rng.randbytes(208)
            setword(p.numeros_unidades,dono*52+32,(0,1,100,65535)[n%4])
            setword(p.baloes,j*8,(0 if n%2==0 else 65535) if n%3==0 else 2)
            # Ganho com zero exige criação: estes casos são testados na parada da dependência.
            ganho=n%2==1
            p.pendencias[:]=self.rng.randbytes(len(p.pendencias))
            bag=p._pendencia(j);inicializar_bag(p.pendencias,bag,n%31)
            if n%5==0 and n%31:
                p.pendencias[bag+0x42]=6;setword(p.pendencias,bag+6,16)
            self.comparar(p,ganho,jogador=j)

    def test_dependencias_de_balao_32_paradas_explicitas(self):
        for n in range(16):
            for ganho in (False,True):
                j=n%4;p=preparar(18,jogador=j)
                setword(p.baloes,j*8,0 if ganho else 1)
                self.b.carregar_propriedade(p)
                with self.assertRaises(DependenciaBalaoPendente):
                    (p.inicializar_jogador if ganho else p.inicializar_neutro)(0,j)
                r=(self.b.inicializar_jogador if ganho else self.b.inicializar_neutro)(0,j)
                self.assertEqual(r['EIP'],0x441baa if ganho else 0x441d4f)
                self.assertEqual(r['EAX'] & 255,j)
                self.conferir(p)

    def test_divisao_zero_16_excecoes_apos_incremento_ou_debito(self):
        from bancada_proprietarios import BancadaProprietarios,x86
        from emulador import unicorn
        for n in range(8):
            for ganho in (False,True):
                anterior=self.b;type(self).b=BancadaProprietarios()
                for nome in ('execucoes','excecoes_esperadas','limites_esperados','paradas_dependencia'):
                    setattr(self.b,nome,getattr(anterior,nome))
                p=preparar(3,estado=1);p.mundo.capacidades.configurar(0,2,0)
                p.mundo.economia.creditar(0,1,24)
                self.b.carregar_propriedade(p)
                with self.assertRaises(ZeroDivisionError):
                    (p.inicializar_jogador if ganho else p.inicializar_neutro)(0,0)
                with self.assertRaises(unicorn.UcError) as ctx:
                    (self.b.inicializar_jogador if ganho else self.b.inicializar_neutro)(0,0)
                self.assertEqual(ctx.exception.errno,unicorn.UC_ERR_EXCEPTION)
                self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_EIP),0x41bfbe if ganho else 0x41bccf)
                self.b.excecoes_esperadas+=1
                self.conferir(p)

    def test_transferencia_com_recontagem_24_chamadas(self):
        for n in range(8):
            antigo=n%4;novo=(n+1)%4;p=preparar(3,jogador=antigo)
            p.mundo.capacidades.configurar(antigo,1,100)
            self.b.carregar_propriedade(p)
            p.inicializar_neutro(0,antigo);self.b.inicializar_neutro(0,antigo);self.conferir(p)
            p.mundo.estruturas[4]=novo;self.b.cpu.mem_write(BASE_CONSTRUCOES+4,bytes([novo]))
            p.inicializar_jogador(0,novo);self.b.inicializar_jogador(0,novo);self.conferir(p)
            p.mundo.inicializar_armazens();self.b.inicializar_armazens();self.conferir(p)


if __name__ == '__main__':
    unittest.main()
