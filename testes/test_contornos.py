"""Propriedades do passo e dos dois sentidos, sem Unicorn."""
import sys
import json
import subprocess
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ferramentas'))
from contornos_caminhos import escolher_passo_contorno
from otimizacao_caminhos import ContextoLinha
from test_emulacao_navegacao import preparar


class Contornos(unittest.TestCase):
    def test_dois_sentidos_ao_redor_da_mesma_celula(self):
        m = preparar()
        m.atributos[0x506] = 1
        c = ContextoLinha.da_unidade(m, 0)
        a, b = (escolher_passo_contorno(c, 0x505, 0x506, s) for s in (-1, 1))
        self.assertEqual((a.celula, b.celula), (0x406, 0x606))
        self.assertEqual((a.anterior, b.anterior), (0x506, 0x506))
        self.assertEqual(a.tentativas, (0x506, 0x406))

    def test_volta_ao_obstaculo_recusa_passo(self):
        m = preparar()
        m.atributos[:] = bytes([1]) * 65536
        r = escolher_passo_contorno(ContextoLinha.da_unidade(m, 0), 0x505, 0x506, -1)
        self.assertEqual(r.celula, 0xffff)
        self.assertEqual(len(r.tentativas), 8)

    def test_trajetos_sem_importar_emulador_reproduzem_relatorio_original(self):
        codigo = '''
import json,sys
sys.path.insert(0, 'ferramentas')
for nome in ('emulador', 'unicorn', 'solucionador_original', 'solucionador_misto'):
    sys.modules[nome] = None
from demonstrar_desvios import executar_cenario
from solucionador_python import SolucionadorCaminhosPython
print(json.dumps([executar_cenario(n, SolucionadorCaminhosPython()) for n in
      ('obstaculo','parede_com_passagem','sem_passagem','destino_bloqueado')]))
'''
        raiz = Path(__file__).resolve().parents[1]
        proc = subprocess.run([sys.executable, '-c', codigo], cwd=raiz, text=True, capture_output=True, check=True)
        novos = json.loads(proc.stdout)
        originais = json.loads((raiz / 'relatorios/desvios-original.json').read_text())['cenarios']
        for novo, original in zip(novos, originais):
            for campo, esperado in original.items():
                self.assertEqual(novo[campo], esperado, (novo['nome'],campo))
