"""Executa só os testes desta pesquisa e registra resultados aqui."""
import argparse
import json
import os
from pathlib import Path
import sys
import unittest

PASTA = Path(__file__).resolve().parent
sys.dont_write_bytecode = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emular', action='store_true')
    args = parser.parse_args()
    if args.emular:
        os.environ['RISING_EMULAR'] = '1'
    else:
        os.environ.pop('RISING_EMULAR', None)
    suite = unittest.defaultTestLoader.discover(str(PASTA / 'testes'))
    resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    from test_economia import Diferencial
    from test_construcoes import DiferencialConstrucoes
    from test_retirada_recalculo import DiferencialRetiradaRecalculo
    from test_init_cave import DiferencialInitCave
    from test_proprietarios import DiferencialProprietarios
    from test_extracao import DiferencialExtracao
    from test_recrutamento import DiferencialRecrutamento
    from test_producao import DiferencialProducao
    from test_aprendizagem import DiferencialAprendizagem
    from test_inicio_aprendizagem import DiferencialInicioAprendizagem
    from test_mercado import DiferencialMercado
    from test_transferencias_mercado import DiferencialTransferenciasMercado
    from test_saida_tropa import DiferencialSaidaTropa
    from test_ordem_mercado import DiferencialOrdemMercado
    from test_bonus_unidades import DiferencialBonusUnidades
    from test_mutacoes_bonus import DiferencialMutacoesBonus
    bancadas = {classe.__name__: getattr(classe, 'b', None)
                for classe in (Diferencial, DiferencialConstrucoes, DiferencialRetiradaRecalculo,
                               DiferencialInitCave, DiferencialProprietarios, DiferencialExtracao,
                               DiferencialRecrutamento, DiferencialProducao, DiferencialAprendizagem,
                               DiferencialInicioAprendizagem, DiferencialMercado,
                               DiferencialTransferenciasMercado)}
    # Include newer benches without rewriting predecessor reports or omitting
    # their executions from a future full-suite run. Some keep one CPU per
    # expected exception rather than a single class-level benchmark.
    grupos = {nome: [b] if b is not None else [] for nome, b in bancadas.items()}
    grupos.update({c.__name__: c.bancadas for c in
                   (DiferencialSaidaTropa, DiferencialOrdemMercado, DiferencialMutacoesBonus)})
    grupos['DiferencialBonusUnidades'] = ([DiferencialBonusUnidades.b]
                                         if DiferencialBonusUnidades.b is not None else [])
    contagens = {nome: sum(getattr(b, 'execucoes', 0) for b in bs) for nome, bs in grupos.items()}
    todas = [b for bs in grupos.values() for b in bs]
    excecoes = sum(getattr(b, 'excecoes_esperadas', 0) for b in todas)
    limites = sum(getattr(b, 'limites_esperados', 0) for b in todas)
    relatorio = dict(modo='x86 original e Python' if args.emular else 'Python sem emulação',
                     testes=resultado.testsRun, falhas=len(resultado.failures), erros=len(resultado.errors),
                     ignorados=[dict(teste=str(t), motivo=m) for t, m in resultado.skipped],
                     execucoes_x86_delimitadas=sum(contagens.values()),
                     execucoes_x86_por_bancada=contagens,
                     excecoes_x86_esperadas=excecoes,
                     limites_x86_esperados=limites,
                     execucoes_x86_ate_parada=sum(contagens.values()) - excecoes - limites,
                     paradas_dependencia_proprietarios=getattr(bancadas['DiferencialProprietarios'], 'paradas_dependencia', 0),
                     paradas_dependencia_recrutamento=getattr(bancadas['DiferencialRecrutamento'], 'paradas_dependencia', 0),
                     sufixos_isolados_recrutamento=getattr(bancadas['DiferencialRecrutamento'], 'sufixos_isolados', 0),
                     sucesso=resultado.wasSuccessful(),
                     sha256_original='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')
    arquivo = PASTA / ('validacao-emulada.json' if args.emular else 'validacao-local.json')
    arquivo.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2) + '\n')
    return 0 if resultado.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
