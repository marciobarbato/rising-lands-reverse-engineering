"""Leitores reais, fronteiras e limites explícitos da máquina de tarefas."""
import sys
import struct
import unittest
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
from simbolos_ia import ler_sbl, ler_rul, enderecar_simbolos, Instrucao, ProgramaRegras
from tarefas_ia import MaquinaTarefas


def programa(ops, entradas=(0, 4)):
    vazio = Instrucao(0, 0, 0, 0, 0)
    return ProgramaRegras(0, 0, (vazio,) * 4 + tuple(ops), tuple(entradas))


class LeitoresIA(unittest.TestCase):
    @unittest.skipUnless((RAIZ.parent / 'source/cd/INSTALHD/RISING.SBL').is_file(), 'Corpus SBL não disponível')
    def test_sbl_nomes_enderecos_e_aliases(self):
        s = ler_sbl((RAIZ.parent / 'source/cd/INSTALHD/RISING.SBL').read_bytes())
        base, nomes = enderecar_simbolos(s)
        self.assertEqual(len(s), 1995)
        self.assertEqual(base, 0x401000)
        self.assertEqual(nomes['iaSolver'], 0x47d314)
        self.assertEqual(nomes['CheminCalcul'], 0x42f214)
        self.assertEqual(nomes['V_Attendre'], 0x47da7a)
        self.assertEqual(nomes['B_Bidon'], nomes['B_AccessibiliteChemin'])
        self.assertEqual(nomes['EnginGetSpeed'], next(base+x.deslocamento for x in s if x.nome=='EnginGetSpeed'))

    @unittest.skipUnless((RAIZ.parent / 'source/cd/INSTALHD/RISING.RUL').is_file(), 'Corpus RULE não disponível')
    def test_rul_corpus_e_referencias(self):
        p = ler_rul((RAIZ.parent / 'source/cd/INSTALHD/RISING.RUL').read_bytes())
        self.assertEqual((len(p.instrucoes), len(p.entradas), p.tamanho_strings), (1157, 64, 2915))
        self.assertEqual(p.entradas[14], 420)
        self.assertEqual(p.instrucoes[467], Instrucao('V_Attendre', 16, 468, 468, 500))
        _, s = enderecar_simbolos(ler_sbl((RAIZ.parent / 'source/cd/INSTALHD/RISING.SBL').read_bytes()))
        nomes = {i.operacao for i in p.instrucoes if isinstance(i.operacao, str)}
        self.assertEqual(len(nomes), 140)
        self.assertTrue(nomes <= set(s))

    def test_formatos_truncados_e_offsets_invalidos(self):
        for dados in (b'', b'\0'*15, struct.pack('<4sIIHH', b'RULE', 0, 0, 1201, 0)):
            with self.assertRaises(ValueError): ler_rul(dados)
        bruto = struct.pack('<4sIIHH', b'RULE', 0, 0, 4, 0) + bytes(80)
        self.assertEqual(len(ler_rul(bruto).instrucoes), 4)
        with self.assertRaises(ValueError): ler_rul(bruto[:-1])
        with self.assertRaises(ValueError): ler_sbl(b'')
        invalido = struct.pack('<IIII', 0, 100, 0xffffffff, 0)
        with self.assertRaises(ValueError): ler_sbl(bytes(x ^ 255 for x in invalido))

    def test_argumentos_misturam_variaveis_e_constante(self):
        op = Instrucao('X', 0x302030, 1, 2, 77)
        self.assertEqual(op.argumentos([11, 22, 33]), [77, 22, 77])

    def test_espera_zero_nao_termina_sozinha(self):
        m = MaquinaTarefas(programa([Instrucao('V_Attendre', 0x10, 1, 3, 0)]))
        i = m.postar(0, 1)
        for _ in range(5): self.assertEqual(m.atualizar(0), 0)
        self.assertEqual(m.byte(i, 0x5e), 1)
        self.assertEqual(m.ativas, 1)

    def test_operacao_de_mundo_desconhecida_nao_inventa_sucesso(self):
        m = MaquinaTarefas(programa([Instrucao('V_ConstruireBatiment', 0, 1, 3, 0)]))
        m.postar(0, 1)
        with self.assertRaises(NotImplementedError): m.atualizar(0)

    def test_limite_interrompe_ciclo_de_regras(self):
        m = MaquinaTarefas(programa([Instrucao('B_Bidon', 0, 4, 4, 0)]))
        m.postar(0, 1)
        with self.assertRaises(RuntimeError): m.atualizar(0, limite=20)
