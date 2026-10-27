"""Trajetos com obstáculos, busca original isolada e movimento reconstruído."""
import argparse
import json
import struct
from pathlib import Path
from navegacao_unidades import MundoNavegacao
from movimento import PARAMETROS_TIPOS
from simbolos_ia import Instrucao, ProgramaRegras
from tarefas_ia import MaquinaTarefas


def preparar_cenario(nome, solucionador=None):
    m=MundoNavegacao(16,16,solucionador)
    for y in range(256):
        for x in range(256):
            if x>=16 or y>=16:m.atributos[y*256+x]=1;m.objetos[y*256+x]=1
    cenarios={'obstaculo':[(6,4)],'parede_com_passagem':[(6,y) for y in range(11)],
              'sem_passagem':[(6,y) for y in range(16)],'destino_bloqueado':[(10,4)]}
    bloqueios=cenarios[nome]
    for x,y in bloqueios:m.atributos[y*256+x]=1;m.objetos[y*256+x]=1
    numero_regioes=m.refazer_regioes()
    u=bytearray(276)
    u[1],u[2],u[0x90],u[0x91],u[0x10a]=7,7,9,9,7
    u[0x98],u[0x93],u[0xa5],u[0xa7]=PARAMETROS_TIPOS[7]
    for off,val in ((8,0x402),(0x7c,0x402),(0xb8,0xffff),(0xc0,0xffff)):struct.pack_into('<H',u,off,val)
    struct.pack_into('<I',u,0x10c,0)
    m.escrever_unidade(0,u);m.ocupar(0,0x402,True)
    m.descobrir_area(0x402,2,0);m.iluminar_area(0x402,0,0);m.minimapa(0,0x402,4)
    m.definir_grupo(0,[0]);struct.pack_into('<H',m.grupos,0x16,1)
    vazio=Instrucao(0,0,0,0,0)
    p=ProgramaRegras(0,0,(vazio,)*4+(Instrucao('V_DeplaceGroupe',0x2120,5,3,0),Instrucao('I_AttenteMessageGroupe',0x123,1,2,8)),(0,4))
    maquina=MaquinaTarefas(p,mundo=m)
    return m,maquina,bloqueios,numero_regioes


def executar_cenario(nome,solucionador=None,limite=1200):
    m,maquina,bloqueios,numero_regioes=preparar_cenario(nome,solucionador)
    maquina.postar(0,1,(0,0x40a));maquina.atualizar(0)
    trajeto=[0x402];eventos=[];estados=[]
    for ciclo in range(1,limite+1):
        evento=m.atualizar_movimento(0,maquina)
        atual=m.palavra(0,8)
        if atual!=trajeto[-1]:trajeto.append(atual)
        estado=m.unidades[0x88]
        if not estados or estados[-1]['estado']!=estado:estados.append(dict(atualizacao=ciclo,estado=estado))
        if evento:eventos.append(dict(atualizacao=ciclo,**evento))
        if m.unidades[2]==7:break
    else:raise RuntimeError('Limite de atualizações do cenário: '+nome)
    maquina.atualizar(0)
    if any((c&255,c>>8) in bloqueios for c in trajeto):raise RuntimeError('Trajeto atravessou obstáculo')
    resultado = dict(nome=nome,inicio=[2,4],destino_solicitado=[10,4],
                destino_efetivo=[m.palavra(0,0x7e)&255,m.palavra(0,0x7e)>>8],
                posicao_final=[atual&255,atual>>8],alcancou_destino_solicitado=atual==0x40a,
                atualizacoes=ciclo,bloqueios=bloqueios,numero_regioes=numero_regioes,
                trajeto=[[c&255,c>>8] for c in trajeto],estados_caminho=estados,
                buscas=m.historico_navegacao,eventos=eventos,tarefas_ativas_ao_final=maquina.ativas)
    if solucionador is not None and hasattr(solucionador.bancada, 'otimizacoes_python'):
        resultado['otimizacoes_python'] = solucionador.bancada.otimizacoes_python
    return resultado


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    modo = parser.add_mutually_exclusive_group()
    modo.add_argument('--original',action='store_true',help='Habilita a busca geral original em Unicorn/JIT')
    modo.add_argument('--misto',action='store_true',help='Busca original com otimização reconstruída em Python')
    args=parser.parse_args()
    if args.original or args.misto:
        if args.misto:
            from solucionador_misto import SolucionadorComOtimizacaoPython as Solucionador
        else:
            from solucionador_original import SolucionadorOriginal as Solucionador
        resultados=[executar_cenario(n,Solucionador()) for n in ('obstaculo','parede_com_passagem','sem_passagem','destino_bloqueado')]
    else:
        resultados=[executar_cenario('obstaculo')]
    r=dict(contexto='Mapas, unidades e tarefas sintéticos; geração de regiões e movimento em Python.',
           busca_geral='Chemin_Verouille/CheminCalcul originais emulados' if args.original else 'não necessária neste cenário local',
           algoritmo_geral_traduzido=False,cenarios=resultados)
    if args.misto:
        r['busca_geral'] = 'Chemin_Verouille/CheminCalcul originais emulados; otimização em Python'
        r['rotinas_traduzidas'] = ['OptimiseChemin', 'TestLigneOptimise']
    nome = 'desvios-misto.json' if args.misto else ('desvios-original.json' if args.original else 'desvios-local.json')
    destino=Path(__file__).resolve().parents[1]/'relatorios'/nome
    destino.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(str(destino))


if __name__=='__main__':main()
