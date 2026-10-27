"""x86 original para primitivas; IA com chamadas internas explicitamente substituídas."""
import os
import random
import struct
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ferramentas'))
from caminhos import aliados, mesma_regiao, Ocupante, classificar_passagem, serializar_rota
from ia import EstadoIA, atualizar_ia, ETAPAS
from cadencia import proximo_aleatorio

GRADE = 0x1100000
JOGADORES = 0x1120000
ORIGEM_ROTA = 0x1121000
DESTINO_ROTA = 0x1122000


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: RISING_EMULAR=1')
class DiferencialCaminhosIA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from emulador import BancadaX86
        cls.bancada = BancadaX86()
        cls.bancada.cpu.mem_map(GRADE, 0x30000)
        cls.bancada.cpu.mem_write(0x4e0f38, struct.pack('<I', GRADE))
        cls.bancada.cpu.mem_write(0x5080a8, struct.pack('<I', JOGADORES))

    def mascaras(self, valores):
        for i, valor in enumerate(valores):
            self.bancada.cpu.mem_write(JOGADORES + i * 20 + 6, bytes([valor]))

    def test_aliancas_800_mascaras_e_ids_especiais(self):
        for mascara in range(32):
            mascaras = [mascara] * 5
            self.mascaras(mascaras)
            for a in range(5):
                for b in range(5):
                    r = self.bancada.executar(0x46d838, [(0x46d838, 0x46d877)], dict(EAX=a, EDX=b))
                    self.assertEqual(bool(r['EAX'] & 255), aliados(a, b, mascaras))
        for a, b in [(200, 200), (200, 0), (0, 200), (255, 255)]:
            r = self.bancada.executar(0x46d838, [(0x46d838, 0x46d877)], dict(EAX=a, EDX=b))
            self.assertEqual(bool(r['EAX'] & 255), aliados(a, b, [0] * 5))

    def test_regioes_512_ocupacoes_e_bordas(self):
        rng = random.Random(0x42d4f8)
        from emulador import UNIDADES
        for n in range(512):
            unidades = [[rng.randrange(0x10000) for _ in range(4)] for _ in range(3)]
            estruturas = [[rng.randrange(0x10000) for _ in range(32)] for _ in range(3)]
            # Iguala um rótulo para exercitar também comparações verdadeiras.
            unidades[1][2] = estruturas[2][7] = 23
            for i, valores in enumerate(unidades):
                self.bancada.cpu.mem_write(UNIDADES + i * 276 + 0xfa, struct.pack('<4H', *valores))
            for i, valores in enumerate(estruturas):
                self.bancada.cpu.mem_write(0x49a194 + i * 276, struct.pack('<32H', *valores))
            valores = [23, 24, 0x400a, 0x400e, 0x8047, 0x8000, 0x4013]
            grade = {0x102: rng.choice(valores), 0x203: rng.choice(valores)}
            for celula, valor in grade.items():
                self.bancada.cpu.mem_write(GRADE + celula * 2, struct.pack('<H', valor))
            largura, altura = ((3, 2) if n % 5 == 0 else (64, 64))
            self.bancada.cpu.mem_write(0x497168, struct.pack('<HH', largura, altura))
            r = self.bancada.executar(0x42d4f8, [(0x42d4f8, 0x42d64c)], dict(EAX=0x102, EDX=0x203))
            self.assertEqual(bool(r['EAX'] & 255), mesma_regiao(0x102, 0x203, largura, altura, grade, unidades, estruturas))

    def test_passagem_tipos_direcoes_e_estados(self):
        rng = random.Random(0x42eba4)
        casos = [(a, b, 1, 1, 0, 0, 0, False, False) for a in range(26) for b in range(26)]
        casos += [(0, 0, a, b, 0, 0, 0, True, True) for a in range(17) for b in range(17)]
        casos += [(rng.randrange(26), rng.randrange(26), rng.randrange(17), rng.randrange(17),
                   rng.choice([1, 15]), rng.randrange(2), rng.randrange(2), bool(rng.randrange(2)),
                   bool(rng.randrange(2))) for _ in range(512)]
        # Exceções de estado precisam de casos explícitos, não só amostra aleatória.
        casos += [(0, t, 1, 1, e, c89, c8a, amigo, parado)
                  for t, e, c89, c8a in [(0, 1, 0, 1), (1, 1, 0, 1), (20, 1, 0, 1),
                                        (21, 1, 0, 1), (6, 15, 1, 0), (7, 15, 1, 0)]
                  for amigo in (False, True) for parado in (False, True)]
        for n, (tipo, outro, direcao, desejada, estado, c89, c8a, amigo, permitir) in enumerate(casos):
            mascaras = [2 if amigo else 0, 0, 0, 0, 0]
            self.mascaras(mascaras)
            movel, ocupante = bytearray(276), bytearray(276)
            movel[1], ocupante[0], ocupante[1], ocupante[2] = tipo, 1, outro, estado
            ocupante[0x89], ocupante[0x8a], ocupante[0x90] = c89, c8a, direcao
            atual, destino = 0x101, (0x101 if n % 3 == 0 else 0x102)
            struct.pack_into('<H', ocupante, 8, atual)
            struct.pack_into('<H', ocupante, 0x7e, destino)
            self.bancada.escrever_unidade(movel, 0)
            self.bancada.escrever_unidade(ocupante, 1)
            self.bancada.cpu.mem_write(0x496304, b'\0\0')
            self.bancada.cpu.mem_write(0x4e1771, bytes([permitir]))
            o = Ocupante(1, outro, atual, destino, direcao, estado, c89, c8a)
            for entrada, booleana in [(0x42eba4, False), (0x42ece0, True)]:
                r = self.bancada.executar(entrada, [(0x42eba4, 0x42ee1c), (0x46d838, 0x46d877),
                                         (0x4423d2, 0x442416)], dict(EAX=1, EDX=desejada))
                self.assertEqual(r['EAX'] & 255, classificar_passagem(0, tipo, o, desejada, mascaras, permitir, booleana), (n, entrada))

    def test_serializacao_original_256_comprimentos(self):
        rng = random.Random(0x43b2be)
        self.bancada.cpu.mem_write(0x4e0f3c, struct.pack('<I', DESTINO_ROTA))
        for quantidade in range(256):
            celulas = [rng.randrange(65536) for _ in range(quantidade)]
            self.bancada.cpu.mem_write(ORIGEM_ROTA, struct.pack('<' + 'H' * (quantidade + 1), quantidade, *celulas))
            self.bancada.executar(0x43b2be, [(0x43b2be, 0x43b300)], dict(EDX=ORIGEM_ROTA), parada=0x43b300)
            self.assertEqual(bytes(self.bancada.cpu.mem_read(DESTINO_ROTA, 2 + quantidade * 2)), serializar_rota(celulas))

    def test_gerador_caminhos_tem_estado_separado(self):
        estado = 12345
        for _ in range(256):
            self.bancada.cpu.mem_write(0x497164, struct.pack('<I', estado))
            self.bancada.cpu.mem_write(0x498db4, struct.pack('<I', 998877))
            r = self.bancada.executar(0x4704dc, [(0x4704dc, 0x470520)])
            estado, _ = proximo_aleatorio(estado, 1)
            self.assertEqual(r['EAX'], estado)
            self.assertEqual(struct.unpack('<I', self.bancada.cpu.mem_read(0x498db4, 4))[0], 998877)

    def test_orquestrador_ia_com_etapas_substituidas(self):
        # Intercepta somente as chamadas declaradas, preservando os registradores
        # como nas convenções observadas. NÃO valida os corpos dessas etapas.
        from emulador import unicorn, x86
        chamadas, retornos = [], {}
        alvos = set(ETAPAS) | {0x47b283, 0x483d95}
        def interceptar(cpu, endereco, tamanho, _):
            if endereco not in alvos:
                return
            eax = cpu.reg_read(x86.UC_X86_REG_EAX)
            edx = cpu.reg_read(x86.UC_X86_REG_EDX)
            chamadas.append((endereco, (eax, edx) if endereco == 0x4866d7 else (eax,)))
            esp = cpu.reg_read(x86.UC_X86_REG_ESP)
            retorno = struct.unpack('<I', cpu.mem_read(esp, 4))[0]
            cpu.reg_write(x86.UC_X86_REG_EAX, retornos.get(endereco, 0))
            cpu.reg_write(x86.UC_X86_REG_ESP, esp + 4)
            cpu.reg_write(x86.UC_X86_REG_EIP, retorno)
        hook = self.bancada.cpu.hook_add(unicorn.UC_HOOK_CODE, interceptar)
        try:
            for jogador in range(5):
                for contador in (0, 8, 9, 10, 255):
                    for inativo, efetivo in [(0, 0), (0, 1), (1, 0)]:
                        for etapa in (None,) + ETAPAS:
                            chamadas.clear()
                            retornos.clear()
                            if etapa:
                                retornos[etapa] = 0x1a1a000e
                            estado = EstadoIA(inativo, contador)
                            esperadas = []
                            def chamar(endereco, *argumentos):
                                esperadas.append((endereco, argumentos))
                                return retornos.get(endereco, 0)
                            esperado = atualizar_ia(jogador, 13, estado, efetivo, 0, chamar)
                            self.bancada.cpu.mem_write(0x51a990 + jogador * 16, bytes([inativo]))
                            self.bancada.cpu.mem_write(0x51a995 + jogador * 16, bytes([contador]))
                            self.bancada.cpu.mem_write(0x4dfaa8 + jogador * 4, struct.pack('<I', efetivo))
                            self.bancada.cpu.mem_write(0x4e1928 + jogador * 2, b'\0\0')
                            r = self.bancada.executar(0x47f927, [(0x47f927, 0x47fa2f)] + [(a, a + 16) for a in alvos], dict(EAX=jogador, EDX=13))
                            self.assertEqual(r['EAX'], esperado)
                            self.assertEqual(chamadas, esperadas)
                            self.assertEqual(self.bancada.cpu.mem_read(0x51a990 + jogador * 16, 1)[0], estado.inativo)
                            self.assertEqual(self.bancada.cpu.mem_read(0x51a995 + jogador * 16, 1)[0], estado.ciclos_sem_efetivo)
        finally:
            self.bancada.cpu.hook_del(hook)

    def test_espera_todos_os_256_contadores(self):
        from caminhos import atualizar_espera
        from emulador import UNIDADES
        for contador in range(256):
            unidade = bytearray(276)
            unidade[0x88], unidade[0x8b] = 6, contador
            self.bancada.escrever_unidade(unidade)
            self.bancada.executar(0x4494fc, [(0x4494fc, 0x449526)], dict(ESI=UNIDADES), parada=0x440d58)
            unidade = self.bancada.ler_unidade()
            self.assertEqual((unidade[0x88], unidade[0x8b]), atualizar_espera(contador))

    def test_mascara_e_excecao_objeto_fd(self):
        from caminhos import testar_mascara_celula
        self.bancada.cpu.mem_write(0x507d74, struct.pack('<I', ORIGEM_ROTA))
        self.bancada.cpu.mem_write(0x507da8, struct.pack('<I', DESTINO_ROTA))
        for objeto in (0, 0xfd, 0xff):
            self.bancada.cpu.mem_write(ORIGEM_ROTA, bytes([objeto]))
            for atributo in range(256):
                self.bancada.cpu.mem_write(DESTINO_ROTA, bytes([atributo]))
                for mascara in (1, 2, 3):
                    r = self.bancada.executar(0x43ec0c, [(0x43ec0c, 0x43ec48)], dict(EDX=mascara))
                    self.assertEqual(bool(r['EAX'] & 255), testar_mascara_celula(objeto, atributo, mascara))

    def test_propria_ocupacao_classes_e_bordas(self):
        from caminhos import pertence_a_propria_ocupacao
        for atual in (0, 1, 256, 257, 0x202):
            for consultada in {atual, (atual - 1) & 65535, (atual - 256) & 65535,
                               (atual - 257) & 65535, (atual + 1) & 65535}:
                for classe in (1, 2, 3):
                    for estado in (7, 14):
                        for campo_ab in (0, 50):
                            for mascara in (1, 2):
                                unidade = bytearray(276)
                                unidade[2], unidade[0xab] = estado, campo_ab
                                struct.pack_into('<H', unidade, 8, atual)
                                self.bancada.escrever_unidade(unidade)
                                r = self.bancada.executar(0x43eb64, [(0x43eb64, 0x43ec0c)], dict(EDX=consultada, ECX=classe, EBX=mascara))
                                self.assertEqual(bool(r['EAX'] & 255), pertence_a_propria_ocupacao(atual, consultada, classe, estado, campo_ab, mascara))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: RISING_EMULAR=1')
class ExperimentosSolucionador(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_caminhos import BancadaCaminhos
        cls.bancada = BancadaCaminhos()

    def test_nove_cenarios_documentados(self):
        import json
        arquivo = Path(__file__).resolve().parents[1] / 'relatorios/caminhos-experimentos.json'
        for caso in json.loads(arquivo.read_text())['casos']:
            entrada = caso['entrada']
            entrada['inicio'], entrada['destino'] = tuple(entrada['inicio']), tuple(entrada['destino'])
            if 'regioes' in entrada:
                entrada['regioes'] = {tuple(r['posicao']): r['rotulo'] for r in entrada['regioes']}
            resultado = self.bancada.buscar(**entrada)
            self.assertEqual(resultado, caso['resultado'], caso['nome'])
            anterior = entrada['inicio']
            for posicao in resultado['rota']:
                self.assertNotIn(posicao, entrada.get('bloqueios', []))
                self.assertLessEqual(max(abs(posicao[i] - anterior[i]) for i in range(2)), 1)
                self.assertTrue(all(0 <= c < 16 for c in posicao))
                anterior = posicao

    def test_consumo_da_rota_acontece_na_chegada(self):
        from caminhos import serializar_rota, consumir_passo_concluido
        from bancada_caminhos import ROTA, JOGADORES
        # A tabela de ponteiros cabe na região já reservada pela bancada.
        self.bancada.cpu.mem_write(0x4e1924, struct.pack('<I', JOGADORES))
        self.bancada.cpu.mem_write(JOGADORES, struct.pack('<I', ROTA))
        for quantidade in range(256):
            buffer = serializar_rota([0x100 + i for i in range(quantidade)])
            self.bancada.cpu.mem_write(ROTA, buffer)
            self.bancada.executar(0x448aaa, [(0x448aaa, 0x448ac6)], dict(EDI=0), parada=0x448ac6)
            self.assertEqual(bytes(self.bancada.cpu.mem_read(ROTA, len(buffer))), consumir_passo_concluido(buffer))
