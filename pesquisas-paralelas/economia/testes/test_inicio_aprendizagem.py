"""Custos, início sem revalidar saldos e ciclo completo da biblioteca."""
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
import test_aprendizagem as _comparacoes
from test_aprendizagem import preparar, w, d
from test_proprietarios import preencher_ordens


def preparar_inicio(jogador=0, indice=0, tipo=0):
    a = preparar(jogador=jogador, indice=indice, tipo=tipo)
    r = a.producao.recrutamento
    r.mundo.estruturas[indice * 276 + 0x74] = 0
    w(r.selecoes, jogador * 2, indice)
    for t in range(5):
        struct.pack_into('<3H', r.tipos_sortilegios, t * 46 + 2, 4, 6, 8)
    for j in range(4):
        for recurso in (0, 1, 2):
            r.mundo.economia.atribuir(j, recurso, 100)
    return a


class ExemplosInicioAprendizagem(unittest.TestCase):
    def test_custos_passos46_ordem_e_truncamento(self):
        a = preparar_inicio()
        r = a.producao.recrutamento
        struct.pack_into('<3H', r.tipos_sortilegios, 4 * 46 + 2, 0x1234, 0xabcd, 65535)
        self.assertEqual(a.custos(0x12340004), (0xabcd, 0x1234, 65535, 0))

    def test_nao_revalida_saldos_e_nao_debita_pecas(self):
        a = preparar_inicio()
        e = a.producao.recrutamento.mundo.economia
        e.atribuir(0, 1, 2)
        e.atribuir(0, 2, 3)
        e.atribuir(0, 0, 1)
        self.assertIsNone(a.iniciar(0, 0))
        self.assertEqual(e.consultar(0)[:3], (0, 0, 1))
        self.assertEqual(a.producao.recrutamento.mundo.estruturas[0x74], 1)

    def test_cobra_jogador_do_comando_e_ignora_tipo_dono_e_tecnologia(self):
        a = preparar_inicio(jogador=1, indice=999)
        r = a.producao.recrutamento
        o = 999 * 276
        r.mundo.estruturas[o + 4], r.mundo.estruturas[o + 8] = 255, 255
        a.iniciar(0x101, 0x100)
        self.assertEqual(r.mundo.economia.consultar(1)[:3], (94, 96, 100))
        self.assertEqual(r.mundo.economia.consultar(0)[:3], (100, 100, 100))
        self.assertEqual(a.inventados, bytes(20))
        self.assertEqual(a.propriedade.sortilegios, bytes(20))

    def test_ocupado_retorna_antes_de_consultar_tipo_invalido(self):
        a = preparar_inicio()
        r = a.producao.recrutamento
        r.mundo.estruturas[0x74] = 255
        antes = bytes(r.mundo.estruturas), bytes(r.mundo.economia.memoria)
        self.assertIsNone(a.iniciar(0, 255))
        self.assertEqual((bytes(r.mundo.estruturas), bytes(r.mundo.economia.memoria)), antes)

    def test_inicio_altera_so_quatro_campos_do_registro(self):
        a = preparar_inicio()
        r = a.producao.recrutamento
        s = r.mundo.estruturas
        s[:276] = b'\xa5' * 276
        s[0x74] = 0
        esperado = bytearray(s)
        esperado[5], esperado[0x74], esperado[0x7b] = 4, 1, 2
        d(esperado, 0x8c, 1)
        a.iniciar(0, 2)
        self.assertEqual(s, esperado)

    def test_capacidade_zero_falha_apos_comida_antes_de_pedra_e_campos(self):
        for comida in (0, 6):
            a = preparar_inicio()
            r = a.producao.recrutamento
            r.mundo.capacidades.configurar(0, 1, 0)
            w(r.tipos_sortilegios, 4, comida)
            antes = bytes(r.mundo.estruturas)
            with self.assertRaises(ZeroDivisionError):
                a.iniciar(0, 0)
            self.assertEqual(r.mundo.economia.consultar(0)[:3], (100 - comida, 100, 100))
            self.assertEqual(r.mundo.estruturas, antes)

    def test_termino_explicito_nao_verifica_tempo_flag_ou_progresso(self):
        a = preparar_inicio(tipo=3)
        r = a.producao.recrutamento
        d(r.mundo.estruturas, 0x8c, 0)
        w(r.tipos_sortilegios, 3 * 46, 65535)
        a.terminar_biblioteca(0)
        self.assertEqual(a.disponivel(0, 3), 1)
        self.assertEqual(r.mundo.estruturas[0x7b], 255)
        self.assertEqual(r.mundo.economia.consultar(0)[:3], (100, 100, 100))

    def test_inicio_e_conclusao_usam_jogadores_distintos_se_dono_diverge(self):
        a = preparar_inicio(jogador=1, tipo=2)
        r = a.producao.recrutamento
        r.mundo.estruturas[4] = 3
        w(r.tipos_sortilegios, 2 * 46, 1)
        a.iniciar(1, 2)
        a.calcular_biblioteca(0)
        self.assertEqual(r.mundo.economia.consultar(1)[:3], (94, 96, 100))
        self.assertEqual(r.mundo.economia.consultar(3)[:3], (100, 100, 100))
        self.assertEqual((a.disponivel(1, 2), a.disponivel(3, 2)), (0, 1))

    def test_guardas_adicionais_e_selecao_ffff(self):
        a = preparar_inicio()
        with self.assertRaises(ValueError):
            a.custos(5)
        with self.assertRaises(ValueError):
            a.iniciar(4, 0)
        with self.assertRaises(ValueError):
            a.iniciar(0, 255)
        r = a.producao.recrutamento
        w(r.selecoes, 0, 65535)
        with self.assertRaises(ValueError):
            a.iniciar(0, 0)
        r.mundo.estruturas[8] = 20
        with self.assertRaises(NotImplementedError):
            a.terminar_biblioteca(0)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: usar --emular')
class DiferencialInicioAprendizagem(unittest.TestCase):
    # Reutiliza a comparação de todos os buffers; não herda os testes anteriores.
    carregar = _comparacoes.DiferencialAprendizagem.carregar
    conferir = _comparacoes.DiferencialAprendizagem.conferir

    @classmethod
    def setUpClass(cls):
        from bancada_inicio_aprendizagem import BancadaInicioAprendizagem
        cls.b = BancadaInicioAprendizagem()

    def setUp(self):
        self.rng = random.Random(0x422d9f)
        self.b.sujeira_pilha = None

    def iniciar(self, a, jogador=0, tipo=0):
        from emulador import RETORNO
        self.carregar(a)
        r = a.producao.recrutamento
        j, indice = r._selecao(jogador)
        ocupado = r.mundo.estruturas[indice * 276 + 0x74] != 0
        custos = a.custos(tipo) if not ocupado else None
        a.iniciar(jogador, tipo)
        regs = {k: self.rng.getrandbits(32) for k in ('EBX', 'ECX', 'ESI', 'EDI', 'EBP')}
        atual = self.b.chamar_inicio(0x422d9f, jogador, tipo, regs)
        self.assertEqual(atual['EIP'], RETORNO)
        for k, valor in regs.items():
            self.assertEqual(atual[k], valor, k)
        self.assertEqual(self.b.acessos_inicio, [] if ocupado else [0x4746fe])
        debitos = [c for c in self.b.chamadas if c['entrada'] == 0x46792c]
        self.assertEqual([(c['EAX'] & 255, c['EDX'] & 65535, c['EBX'] & 65535) for c in debitos],
                         [] if ocupado else [(1, custos.comida, j), (2, custos.pedra, j)])
        self.conferir(a)

    def terminar(self, a, indice=0):
        self.carregar(a)
        a.terminar_biblioteca(indice)
        regs = {k: self.rng.getrandbits(32) for k in ('EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')}
        atual = self.b.chamar_inicio(0x421250, indice, regs['EDX'], regs)
        for k, valor in regs.items():
            self.assertEqual(atual[k], valor, k)
        self.assertEqual([c['entrada'] for c in self.b.acessos_aprendizagem
                          if c['entrada'] in (0x474974, 0x474a38, 0x41c76c)],
                         [0x474974, 0x474a38, 0x41c76c])
        self.conferir(a)

    def calcular(self, a, indice=0):
        self.b.chamadas.clear()
        _comparacoes.DiferencialAprendizagem.calcular(self, a, indice, carregar=False)

    def custos(self, a, tipo):
        self.carregar(a)
        esperado = bytearray(b'\xa7' * 32)
        for offset, valor in zip((4, 12, 20), a.custos(tipo)[:3]):
            w(esperado, offset, valor)
        self.assertEqual(self.b.custos(tipo), esperado)
        self.conferir(a)

    def test_256_custos_u16_e_bytes_vizinhos_das_saidas(self):
        for n in range(256):
            a = preparar_inicio()
            tipo = n % 5
            t = a.producao.recrutamento.tipos_sortilegios
            t[:] = self.rng.randbytes(230)
            for offset in (2, 4, 6):
                w(t, tipo * 46 + offset, self.rng.choice((0, 1, 65535, self.rng.randrange(65536))))
            self.custos(a, tipo | 0xfedc0000)

    def test_512_tipos_de_construcao_livres_e_ocupados(self):
        for tipo_construcao in range(256):
            for flag in (0, 255):
                a = preparar_inicio()
                s = a.producao.recrutamento.mundo.estruturas
                s[4], s[8], s[0x74] = 255, tipo_construcao, flag
                self.iniciar(a, tipo=255 if flag else 2)

    def test_512_inicios_saldos_rmi_custos_capacidade_e_pilha_suja(self):
        for n in range(512):
            j, indice, tipo = n % 4, self.rng.choice((0, 1, 999)), n % 5
            a = preparar_inicio(j, indice, tipo)
            r = a.producao.recrutamento
            s = r.mundo.estruturas
            o = indice * 276
            s[o:o + 276] = self.rng.randbytes(276)
            s[o + 0x74] = 0
            r.mundo.economia.memoria[:] = self.rng.randbytes(128)
            for offset in (2, 4, 6):
                w(r.tipos_sortilegios, tipo * 46 + offset, self.rng.choice((0, 65535, self.rng.randrange(65536))))
            armazens = self.rng.choice((0, 1, 2, 65535))
            r.mundo.capacidades.configurar(j, armazens, self.rng.randrange(1, 65536) if armazens else 0)
            self.b.sujeira_pilha = n & 255
            self.iniciar(a, j | 0xabcd0000, tipo | 0x98760000)

    def test_16_excecoes_apos_primeiro_debito_preservam_estado_parcial(self):
        from bancada_inicio_aprendizagem import BancadaInicioAprendizagem
        from emulador import unicorn, x86
        for n in range(16):
            anterior = self.b
            type(self).b = BancadaInicioAprendizagem()
            for campo in ('execucoes', 'excecoes_esperadas', 'limites_esperados'):
                setattr(self.b, campo, getattr(anterior, campo))
            j, tipo = n % 4, n % 5
            a = preparar_inicio(jogador=j, tipo=tipo)
            r = a.producao.recrutamento
            r.mundo.capacidades.configurar(j, 1 + n, 0)
            w(r.tipos_sortilegios, tipo * 46 + 4, 0 if n % 2 else 6)
            self.carregar(a)
            with self.assertRaises(ZeroDivisionError):
                a.iniciar(j, tipo)
            with self.assertRaises(unicorn.UcError) as ctx:
                self.b.chamar_inicio(0x422d9f, j, tipo)
            self.assertEqual(ctx.exception.errno, unicorn.UC_ERR_EXCEPTION)
            self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_EIP), 0x422e62)
            self.b.excecoes_esperadas += 1
            self.assertEqual([c['EAX'] & 255 for c in self.b.chamadas if c['entrada'] == 0x46792c], [1])
            self.conferir(a)

    def test_256_terminos_explicitos_sem_condicoes_de_progresso(self):
        for n in range(256):
            j, indice, tipo = n % 4, self.rng.choice((0, 999)), n % 5
            a = preparar_inicio(j, indice, tipo)
            s = a.producao.recrutamento.mundo.estruturas
            o = indice * 276
            s[o + 0x75:o + 0x8c] = self.rng.randbytes(0x8c - 0x75)
            s[o + 5], s[o + 0x74], s[o + 0x7b] = n, n % 2, tipo
            d(s, o + 0x8c, self.rng.choice((0, 1, 0xffffffff)))
            a.inventados[:] = self.rng.randbytes(20)
            a.propriedade.sortilegios[:] = self.rng.randbytes(20)
            preencher_ordens(a.propriedade.ordens, self.rng.randbytes(10816))
            a.propriedade.pendencias[:] = self.rng.randbytes(9152)
            self.terminar(a, indice | 0xbeef0000)

    def test_cinco_registros_do_exe_e_20_ciclos_completos(self):
        tipos = json.loads((PASTA / 'evidencias/parametros-producao.json').read_text())['tipos_sortilegios']
        bloco = b''.join(bytes.fromhex(t['registro_hex']) for t in tipos)
        self.assertEqual(len(bloco), 230)
        for tipo in range(5):
            a = preparar_inicio()
            a.producao.recrutamento.tipos_sortilegios[:] = bloco
            self.custos(a, tipo)
        for j in range(4):
            for tipo in range(5):
                a = preparar_inicio(jogador=j, tipo=tipo)
                r = a.producao.recrutamento
                r.tipos_sortilegios[:] = bloco
                r.mundo.estruturas[0x4e:0x4e + 30] = b'\1' * 30
                a.producao.tipos_construcoes[6 * 52 + 18] = 1
                a.inventados[:] = b'\1' * 20
                self.iniciar(a, j, tipo)
                saldo = bytes(r.mundo.economia.memoria)
                for _ in range(64):
                    if r.mundo.estruturas[0x74] == 0:
                        break
                    self.calcular(a)
                self.assertEqual(r.mundo.estruturas[0x74], 0)
                self.assertEqual(a.disponivel(j, tipo), 1)
                self.assertEqual(r.mundo.economia.memoria, saldo)
                self.calcular(a)  # Sem acesso ao tipo 0xff após conclusão.

    def test_40_chamadas_com_dono_diferente_do_jogador_cobrado(self):
        for j in range(4):
            for tipo in range(5):
                a = preparar_inicio(jogador=j, tipo=tipo)
                r = a.producao.recrutamento
                dono = (j + 1) % 4
                r.mundo.estruturas[4] = dono
                w(r.tipos_sortilegios, tipo * 46, 1)
                self.iniciar(a, j, tipo)
                self.calcular(a)
                self.assertEqual(a.disponivel(dono, tipo), 1)
                self.assertEqual(a.disponivel(j, tipo), 0)
                self.assertEqual(r.mundo.economia.consultar(j)[:3], (94, 96, 100))
                self.assertEqual(r.mundo.economia.consultar(dono)[:3], (100, 100, 100))


if __name__ == '__main__':
    unittest.main()
