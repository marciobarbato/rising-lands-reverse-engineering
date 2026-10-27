"""Executa a suíte e registra um resumo reproduzível, sem ocultar testes ignorados."""
import argparse
import json
import os
from pathlib import Path
import platform
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]


class Resultado(unittest.TextTestResult):
    def startTest(self, teste):
        super().startTest(teste)
        bancada = getattr(teste, 'bancada', None)
        self.inicio_execucoes = bancada.execucoes if bancada else 0

    def stopTest(self, teste):
        bancada = getattr(teste, 'bancada', None)
        self.execucoes_x86 += (bancada.execucoes - self.inicio_execucoes) if bancada else 0
        auxiliares = sum(b.execucoes for b in getattr(teste, 'bancadas_auxiliares', ()))
        self.execucoes_x86 += auxiliares
        self.execucoes_x86_auxiliares += auxiliares
        super().stopTest(teste)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.execucoes_x86 = 0
        self.execucoes_x86_auxiliares = 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emular', action='store_true', help='Exige Unicorn e permissão para JIT')
    args = parser.parse_args()
    # A escolha é explícita, mesmo se o shell herdou outra preferência.
    os.environ['RISING_EMULAR'] = '1' if args.emular else '0'
    suite = unittest.defaultTestLoader.discover(str(RAIZ / 'testes'), pattern='test_*.py')
    resultado = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(suite)
    relatorio = dict(python=platform.python_version(), emulacao_habilitada=args.emular,
                     testes=resultado.testsRun, falhas=len(resultado.failures), erros=len(resultado.errors),
                     ignorados=[dict(teste=t.id(), motivo=m) for t, m in resultado.skipped],
                     execucoes_x86_delimitadas=resultado.execucoes_x86,
                     execucoes_x86_backend_navegacao=resultado.execucoes_x86_auxiliares,
                     sucesso=resultado.wasSuccessful())
    if args.emular:
        from emulador import unicorn, HASH_ORIGINAL
        relatorio.update(unicorn=unicorn.__version__, sha256_original=HASH_ORIGINAL,
                         limite='Trechos isolados com memória sintética; não é validação do jogo completo.')
    destino = RAIZ / ('relatorios/validacao-emulada.json' if args.emular else 'relatorios/validacao-local.json')
    destino.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    raise SystemExit(0 if resultado.wasSuccessful() else 1)


if __name__ == '__main__':
    main()
