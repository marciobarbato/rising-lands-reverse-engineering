"""Executa só os testes desta pesquisa e grava relatório na mesma pasta."""
import argparse
import json
import os
import unittest
from pathlib import Path


class Resultado(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.contagens = []

    def startTest(self, teste):
        self.antes = getattr(getattr(type(teste), 'b', None), 'execucoes', 0)
        super().startTest(teste)

    def stopTest(self, teste):
        depois = getattr(getattr(type(teste), 'b', None), 'execucoes', 0)
        self.contagens.append(dict(teste=teste.id(), execucoes_x86_delimitadas=depois - self.antes))
        super().stopTest(teste)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emular', action='store_true', help='Requer Unicorn e JIT permitido pelo host')
    args = parser.parse_args()
    if args.emular:
        os.environ['RISING_EMULAR'] = '1'
    else:
        os.environ.pop('RISING_EMULAR', None)
    from test_alvos_alcance import Contratos, Diferencial
    from test_mira_angular import ContratosMira, DiferencialMira
    from test_animacao_disparo import ContratosAnimacao, DiferencialAnimacao
    from test_inicializacao_ataque import ContratosInicializacao, DiferencialInicializacao
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c)
        for c in (Contratos, Diferencial, ContratosMira, DiferencialMira, ContratosAnimacao, DiferencialAnimacao,
                  ContratosInicializacao, DiferencialInicializacao))
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(suite)
    saida = Path(__file__).resolve().parent / ('validacao-emulada.json' if args.emular else 'validacao-local.json')
    relatorio = dict(sucesso=r.wasSuccessful(), testes=r.testsRun, falhas=len(r.failures),
        erros=len(r.errors), ignorados=[dict(teste=t.id(), motivo=m) for t, m in r.skipped],
        sha256_original='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
        execucoes_x86_delimitadas=sum(t['execucoes_x86_delimitadas'] for t in r.contagens),
        por_teste=r.contagens,
        limites=dict(tempo_por_chamada_segundos=1, instrucoes_padrao=20000,
            instrucoes_selecao=1000000, instrucoes_linha=100000),
        escopo='Trechos isolados do EXE original com memória sintética. Não inicia Windows/jogo.',
        consultas_resolvidas='O teste antigo de fragmentos fornece AL como entrada. Os novos testes de mira/manutenção executam EnginViseCible, AngleCalcul e chamadas x87 originais, sem substituições.',
        configuracao_x87=dict(control_word='0x037f', workaround_fpatan_0x49946c=0,
            escopo_python='Coordenadas u8, 8/32 setores; resultados discretos, não equivalência bit a bit de intermediários x87'),
        animacao_disparo=dict(efeitos='Callbacks explícitos; não integra física ou dano em Python.',
            referencia='Emissão x86 com pool cheio e um slot livre; corpo a corpo sem ocupantes; magia ID255; movimento/balão/áudio param na entrada.',
            comparacao='Registro inteiro, contexto de busca e argumentos na pilha/registradores de cada efeito.'),
        inicializacao=dict(rotinas=['0x457350', '0x457b87'],
            trechos_pos_carga=['0x46ad8b..0x46b019', '0x46b08f..0x46b0e3'],
            comparacao='276 bytes, quatro globais de busca e observação das escritas em +79/+7a/+8a/+8b.',
            limites='FileRead não executado; seus pedidos são comparados em checkpoints. Tipos 26..255 só testam o comportamento fora do domínio de tipos válidos.'),
        diagnosticos=[dict(teste=t.id(), detalhe=e) for t, e in [*r.failures, *r.errors]])
    saida.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Relatório: {saida}\nExecuções x86 delimitadas: {relatorio["execucoes_x86_delimitadas"]}')
    raise SystemExit(not r.wasSuccessful())


if __name__ == '__main__':
    main()
