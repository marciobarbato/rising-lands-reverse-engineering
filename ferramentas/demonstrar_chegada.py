"""Demonstra uma rota fornecida: ordem, avanço físico, chegada e retomada da tarefa.

O coordenador pesquisa somente esta sequência delimitada; não inicia uma partida
nem executa todo o despacho por unidade do jogo. --emular confronta cada etapa
com suas funções x86 originais, sem interceptar as chamadas internas.
"""
import argparse
import json
import struct
from pathlib import Path
from avanco_unidades import MundoFisico
from caminhos import serializar_rota
from movimento import PARAMETROS_TIPOS
from tarefas_ia import MaquinaTarefas
from simbolos_ia import Instrucao, ProgramaRegras


def programa(ops):
    vazio=Instrucao(0,0,0,0,0)
    return ProgramaRegras(0,0,(vazio,)*4+tuple(ops),(0,4))


def preparar_trajeto():
    mundo=MundoFisico()
    u=bytearray(276)
    u[1],u[2]=7,7
    u[0x90]=u[0x91]=9
    u[0x98],u[0x93],u[0xa5],u[0xa7]=PARAMETROS_TIPOS[7]
    u[0xbb]=1
    u[0x10a]=7
    for o,v in ((8,0x505),(0x7c,0x505),(0xb8,0xffff),(0xc0,0xffff)):
        struct.pack_into('<H',u,o,v)
    struct.pack_into('<I',u,0x10c,0)
    mundo.escrever_unidade(0,u)
    mundo.ocupar(0,0x505,True)
    mundo.descobrir_area(0x505,3,0)
    mundo.iluminar_area(0x505,1,0)
    mundo.minimapa(0,0x505,4)
    mundo.definir_grupo(0,[0])
    struct.pack_into('<H',mundo.grupos,0x16,1)
    mundo.rotas[0]=bytearray(serializar_rota([0x506,0x507]))
    p=programa([Instrucao('V_DeplaceGroupe',0x2120,5,3,0),
                Instrucao('I_AttenteMessageGroupe',0x123,1,2,8)])
    maquina=MaquinaTarefas(p,mundo=mundo)
    return mundo,maquina



def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emular',action='store_true')
    args=parser.parse_args()
    mundo,maquina=preparar_trajeto()
    if args.emular:
        from bancada_avanco import BancadaAvanco
        bancada=BancadaAvanco()
        bancada.carregar(maquina.programa)
        bancada.carregar_fisica(mundo)
    tarefa=maquina.postar(0,1,(0,0x507))
    if args.emular and bancada.postar(0,1,(0,0x507))!=tarefa:
        raise RuntimeError('Alocação divergente')
    retorno=maquina.atualizar(0)
    if args.emular and bancada.atualizar(0)!=retorno:
        raise RuntimeError('Início da tarefa divergente')
    etapas=[]
    eventos=[]
    for ciclo in range(1,65):
        if args.emular:
            no_destino=mundo.palavra(0,8)==mundo.palavra(0,0x7e)
            bancada.concluir(0)
            if not no_destino:
                if mundo.palavra(0,8)==mundo.palavra(0,0x7c) and not mundo.unidades[0x86] and not mundo.unidades[0x87]:
                    bancada.escolher_proximo(0)
                bancada.avancar(0)
            bancada.notificar(0)
        evento=mundo.atualizar_movimento(0,maquina)
        if args.emular:
            erros=bancada.conferir_fisica(mundo)
            if erros or bancada.memoria_tarefas()!=bytes(maquina.memoria):
                raise RuntimeError('Estado divergente no ciclo '+str(ciclo)+': '+repr(erros))
        etapas.append(dict(atualizacao=ciclo,celula=mundo.palavra(0,8),celula_passo=mundo.palavra(0,0x7c),
                           deslocamento_x_u8=mundo.unidades[0x86],deslocamento_y_u8=mundo.unidades[0x87],
                           progresso=mundo.unidades[0x97],estado=mundo.unidades[2],
                           rota_restante=struct.unpack_from('<H',mundo.rotas[0])[0],
                           tarefa_suspensa=maquina.byte(tarefa,0x5e),resultado_pendente=maquina.byte(tarefa,0x5f)))
        if evento:
            eventos.append(dict(atualizacao=ciclo,**evento))
            break
    if not eventos:
        raise RuntimeError('Trajeto não concluiu no limite declarado')
    retorno=maquina.atualizar(0)
    if args.emular:
        if bancada.atualizar(0)!=retorno or bancada.memoria_tarefas()!=bytes(maquina.memoria):
            raise RuntimeError('Retomada da tarefa divergente')
        if bancada.estado_listas()!=dict(livres=maquina.livres,contextos=maquina.contextos,ativas=maquina.ativas):
            raise RuntimeError('Listas de tarefas divergentes')
    relatorio=dict(contexto='RAM, tarefa e rota sintéticas; sequência delimitada de funções originais, não uma partida completa.',
                   origem=[5,5],destino=[7,5],tipo_unidade=7,perfil_mensagens=1,mascara_esperada=8,
                   verificado_no_x86=args.emular,limite_instrucoes_por_chamada=1000000,
                   execucoes_x86_delimitadas=bancada.execucoes if args.emular else 0,
                   etapas=etapas,eventos=eventos,tarefas_ativas_ao_final=maquina.ativas,
                   resultado_da_espera=maquina.ler(tarefa,0x20))
    nome='chegada-emulada.json' if args.emular else 'chegada-local.json'
    destino=Path(__file__).resolve().parents[1]/'relatorios'/nome
    destino.write_text(json.dumps(relatorio,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(str(destino))


if __name__=='__main__':
    main()
