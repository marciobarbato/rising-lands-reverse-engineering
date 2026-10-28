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
    from test_projeteis import ContratosProjeteis, DiferencialProjeteis
    from test_avanco_projeteis import ContratosAvanco, DiferencialAvanco
    from test_maquina_projeteis import ContratosMaquina, DiferencialMaquina
    from test_cadencia_projeteis import ContratosCadenciaProjeteis, DiferencialCadenciaProjeteis
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c)
        for c in (Contratos, Diferencial, ContratosMira, DiferencialMira, ContratosAnimacao, DiferencialAnimacao,
                  ContratosInicializacao, DiferencialInicializacao, ContratosProjeteis, DiferencialProjeteis,
                  ContratosAvanco, DiferencialAvanco, ContratosMaquina, DiferencialMaquina,
                  ContratosCadenciaProjeteis, DiferencialCadenciaProjeteis))
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(suite)
    saida = Path(__file__).resolve().parent / ('validacao-emulada.json' if args.emular else 'validacao-local.json')
    relatorio = dict(sucesso=r.wasSuccessful(), testes=r.testsRun, falhas=len(r.failures),
        erros=len(r.errors), ignorados=[dict(teste=t.id(), motivo=m) for t, m in r.skipped],
        sha256_original='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
        execucoes_x86_delimitadas=sum(t['execucoes_x86_delimitadas'] for t in r.contagens),
        por_teste=r.contagens,
        limites=dict(tempo_por_chamada_segundos=1, instrucoes_padrao=20000,
            instrucoes_selecao=1000000, instrucoes_linha=100000, instrucoes_avanco_impacto=500000,
            maquina_instrucoes_por_fatia=500000, maquina_maximo_retomadas=20000),
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
        projeteis=dict(rotinas=['0x46e00a', '0x46e02c', '0x46e422', '0x46e44c',
                '0x46e208', '0x46e049', '0x46e4ca'],
            comparacao='5600 bytes do pool e ordem/argumentos dos efeitos; tipos 0..255; trajetórias e overflow de palavras.',
            limites='Nesta etapa: dano com grade vazia; descoberta/iluminação com dimensões zero e raio 0..10, sem células visitadas. Avance é validado nas etapas seguintes; renderização permanece externa.'),
        avanco_projeteis=dict(rotinas=['0x46e52c', '0x46e5fe'],
            avanco_parcial='0x46eaf8: tipos 1..5, 9..13, 17, 20..23 e 29, incluindo chegada.',
            comparacao='5600 bytes, sequência de pedidos de dano, marcadores/resultados Random e argumentos de ProjectileSet.',
            consultas='Random original executado; seus resultados são entradas externas do Python. Não se revalida nem duplica o gerador.',
            limites='Nesta etapa: InfligeDegat original com grade vazia, sem dano em vítimas. Os demais ramos e o despacho são validados em maquina_projeteis.'),
        maquina_projeteis=dict(rotinas=['0x46eaf8', '0x46fc0f'],
            escopo='Todos os bytes de tipo em Avance, círculo do tipo 30, sorteio do tipo 33, expiração e 30 passagens sobre o pool vivo.',
            comparacao='5600 bytes, global 0x4dfb44, dois buffers de 65536 bytes, sequência e argumentos das chamadas, atividade durante efeitos e ordem de IDs processados.',
            referencia='Random, CreerExplosion, consultas de magia e EteintTerrain originais executados sem substituir CALLs; resultados Random são entradas externas do Python.',
            fatiamento='Paradas antes de Avance e de cada célula do tipo 30; retomada sem alterar registradores, pilha ou memória. Cada fatia conta como execução delimitada.',
            limites='Dano com unidades inativas e grade vazia; EteintTerrain com dimensões zero e raio 0..7, sem células visitadas. Não valida iluminação real, vítimas, desenho ou duração em segundos.'),
        cadencia_projeteis=dict(trechos=['0x42d14c..0x42d184', '0x42d2e3..0x42d2f0',
                '0x42d3c0..0x42d3e1', '0x42d3f0..0x42d3f5', '0x43f14f..0x43f220'],
            comparacao='Portões locais, pool completo, dois bytes de apresentação, retângulo e preservação da tabela de 256 bytes.',
            referencia='EvenementEnCours original executado; CALL de ProjectileCalcul em CalculGame executado até antes da atualização das unidades. Contadores reutilizam a tradução existente e executam o trecho x86 de ProgIteration.',
            limites='Não executa menus, comandos/jogadores, laço Windows, DirectDraw ou jogo completo. Cadência em segundos não medida; tabela visual sintética, sem reconstruir seu preenchimento.'),
        diagnosticos=[dict(teste=t.id(), detalhe=e) for t, e in [*r.failures, *r.errors]])
    saida.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Relatório: {saida}\nExecuções x86 delimitadas: {relatorio["execucoes_x86_delimitadas"]}')
    raise SystemExit(not r.wasSuccessful())


if __name__ == '__main__':
    main()
