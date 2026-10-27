"""Demonstra tarefas emitindo ordens em estados sintéticos da RAM.

--emular compara cada cenário com o EXE original; sem a opção, usa somente a
reconstrução Python. A demonstração não avança a posição física das unidades.
"""
import argparse
import json
import struct
from dataclasses import asdict
from pathlib import Path
from ordens_unidades import MundoUnidades, ContextoBusca
from tarefas_ia import MaquinaTarefas
from simbolos_ia import Instrucao, ProgramaRegras

RAIZ = Path(__file__).resolve().parents[1]


def resumir(mundo, indices):
    return [dict(indice=i, dono=mundo.ler_unidade(i)[0], tipo=mundo.ler_unidade(i)[1],
                 estado=mundo.ler_unidade(i)[2], celula_atual=mundo.palavra(i, 8),
                 destino=mundo.palavra(i, 0x7e), estado_caminho=mundo.ler_unidade(i)[0x88],
                 campo_89=mundo.ler_unidade(i)[0x89], campo_b2=mundo.palavra(i, 0xb2),
                 campo_b8=mundo.palavra(i, 0xb8), campo_c0=mundo.palavra(i, 0xc0)) for i in indices]


def cenarios():
    for nome, tipo, estado, objeto in [('movimento_comum', 0, 7, 0), ('unidade_inativa', 0, 4, 0),
                                      ('tipo_6_caixa', 6, 7, 0x42), ('construtor', 13, 7, 0)]:
        mundo = MundoUnidades()
        u = bytearray(276)
        u[0], u[1], u[2], u[0x88] = 3, tipo, estado, 5
        for offset, valor in [(8, 0x202), (0x7c, 0x202), (0x7e, 0x303),
                               (0xb8, 12), (0xc0, 7 if tipo == 13 else 0xffff)]:
            struct.pack_into('<H', u, offset, valor)
        mundo.escrever_unidade(2, u)
        mundo.objetos[0x608] = objeto
        mundo.busca = ContextoBusca(2, 1, 1, 123, 1)
        mundo.estruturas[7 * 276 + 0x74:7 * 276 + 0x77] = bytes([9, 1, 15])
        yield nome, mundo, [2], 'V_DeplacerUnite', (0x608, 2)
    mundo = MundoUnidades()
    for i, estado in enumerate((7, 1, 4)):
        u = bytearray(276)
        u[2] = estado
        struct.pack_into('<H', u, 8, 0x202 + i)
        struct.pack_into('<H', u, 0xb8, 12)
        mundo.escrever_unidade(i, u)
    mundo.definir_grupo(3, [0, 1, 2])
    yield 'grupo_misto', mundo, [0, 1, 2], 'V_DeplaceGroupe', (3, 0x608)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emular', action='store_true')
    args = parser.parse_args()
    resultados, execucoes = [], 0
    for nome, mundo, indices, operacao, argumentos in cenarios():
        vazio = Instrucao(0, 0, 0, 0, 0)
        p = ProgramaRegras(0, 0, (vazio,) * 4 + (Instrucao(operacao, 0x2120, 1, 3, 0),), (0, 4))
        m = MaquinaTarefas(p, mundo=mundo)
        antes, busca_antes = resumir(mundo, indices), asdict(mundo.busca)
        estrutura_antes = list(mundo.estruturas[7 * 276 + 0x74:7 * 276 + 0x77])
        if args.emular:
            from bancada_ordens import BancadaOrdens
            b = BancadaOrdens()
            b.carregar(p)
            b.carregar_mundo(mundo)
        indice = m.postar(0, 1, argumentos)
        if args.emular and b.postar(0, 1, argumentos) != indice:
            raise RuntimeError('Alocação divergente')
        retorno = m.atualizar(0)
        if args.emular:
            if b.atualizar(0) != retorno or b.conferir_mundo(mundo) or b.memoria_tarefas() != bytes(m.memoria):
                raise RuntimeError('Divergência entre reconstrução e x86: ' + nome)
            if b.estado_listas() != dict(livres=m.livres, contextos=m.contextos, ativas=m.ativas):
                raise RuntimeError('Listas de tarefas divergentes: ' + nome)
            execucoes += b.execucoes
        resultados.append(dict(nome=nome, operacao=operacao, argumentos=argumentos,
                               antes=antes, depois=resumir(mundo, indices),
                               busca_antes=busca_antes, busca_depois=asdict(mundo.busca),
                               estrutura_7_campos_74_75_76_antes=estrutura_antes,
                               estrutura_7_campos_74_75_76_depois=list(mundo.estruturas[7 * 276 + 0x74:7 * 276 + 0x77]),
                               tarefas_ativas_depois=m.ativas, retorno=hex(retorno)))
    relatorio = dict(contexto='RAM sintética; emissão de ordens sem avanço físico das unidades.',
                     programa_sintetico=True, verificado_no_x86=args.emular,
                     execucoes_x86_delimitadas=execucoes, cenarios=resultados)
    nome = 'movimento-ia-emulado.json' if args.emular else 'movimento-ia-local.json'
    destino = RAIZ / 'relatorios' / nome
    destino.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(str(destino))


if __name__ == '__main__':
    main()
