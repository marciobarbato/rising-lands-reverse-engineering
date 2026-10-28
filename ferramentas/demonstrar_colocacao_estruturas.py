"""Percursos com PlaceBatiment traduzido: edifício, parede e portão sem encaixe."""
import json
import struct
from pathlib import Path
from demonstrar_desvios import preparar_cenario
from solucionador_python import SolucionadorCaminhosPython


def preparar_colocacao_cenario(nome):
    if nome not in ('edificio','muro_com_portao','portao_sem_encaixe'):
        raise ValueError('Cenário de colocação desconhecido')
    m,maquina,_,_=preparar_cenario('obstaculo',SolucionadorCaminhosPython())
    m.objetos[0x406]=m.atributos[0x406]=0
    if nome=='muro_com_portao':m.objetos[6]=m.atributos[6]=1
    m.refazer_regioes()
    if nome=='edificio':estruturas=((7,0,0x405),)
    elif nome=='portao_sem_encaixe':estruturas=((7,12,0x406),)
    else:
        estruturas=tuple((y,9,6+y*256) for y in range(1,11) if y!=5)+((5,12,0x506),)
    for indice,tipo,celula in estruturas:
        p=indice*276
        struct.pack_into('<H',m.estruturas,p+2,celula)
        m.estruturas[p+4],m.estruturas[p+8]=1,tipo
    return m,maquina,estruturas


def colocar_cenario(m,estruturas):
    for indice,tipo,celula in estruturas:m.colocar_estrutura(indice)
    for indice,tipo,celula in estruturas:
        if tipo in (9,12):m.atualizar_muros_vizinhos(celula)


def executar_colocacao_cenario(nome,limite=1200):
    m,maquina,estruturas=preparar_colocacao_cenario(nome)
    colocar_cenario(m,estruturas)
    descricoes=[]
    for indice,tipo,celula in estruturas:
        descricoes.append(dict(indice=indice,tipo=tipo,celula=celula,
                               objeto=m.objetos[celula],tile=m.tiles[celula],atributos=m.atributos[celula],
                               valor_7c=struct.unpack_from('<H',m.estruturas,indice*276+0x7c)[0],
                               regiao=m.regioes[celula]))
    maquina.postar(0,1,(0,0x40a));maquina.atualizar(0)
    trajeto=[m.palavra(0,8)];eventos=[]
    for ciclo in range(1,limite+1):
        evento=m.atualizar_movimento(0,maquina)
        if evento:eventos.append(dict(ciclo=ciclo,**evento))
        celula=m.palavra(0,8)
        if celula!=trajeto[-1]:trajeto.append(celula)
        if m.unidades[2]==7:break
    else:raise RuntimeError('O trajeto não terminou no limite')
    maquina.atualizar(0)
    return dict(nome=nome,estruturas=descricoes,atualizacoes=ciclo,
                trajeto=[[c&255,c>>8] for c in trajeto],posicao_final=[celula&255,celula>>8],
                buscas=m.historico_navegacao,eventos=eventos,tarefas_ativas=maquina.ativas)


if __name__=='__main__':
    dados=dict(executa_x86=False,contexto='Registros e terreno sintéticos; sem criação, custos ou ordem de construir.',
               cenarios=[executar_colocacao_cenario(n) for n in ('edificio','muro_com_portao','portao_sem_encaixe')])
    destino=Path(__file__).resolve().parents[1]/'relatorios/colocacao-estruturas-python.json'
    destino.write_text(json.dumps(dados,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(destino)
