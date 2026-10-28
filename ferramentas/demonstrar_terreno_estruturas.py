"""Navegação com edifícios aplicados pela máscara e remoção durante o movimento."""
import json
import struct
from pathlib import Path
from demonstrar_desvios import preparar_cenario
from solucionador_python import SolucionadorCaminhosPython


def preparar_terreno_cenario(nome):
    if nome not in ('edificio','edificio_retirado','parede'):
        raise ValueError('Cenário de terreno desconhecido')
    m,maquina,_,_=preparar_cenario('obstaculo',SolucionadorCaminhosPython())
    m.objetos[0x406]=m.atributos[0x406]=0
    m.refazer_regioes()
    estruturas=tuple((i,9,6+y*256) for i,y in enumerate(range(11))) if nome=='parede' else ((7,0,0x405),)
    for indice,tipo,origem in estruturas:
        p=indice*276
        struct.pack_into('<H',m.estruturas,p+2,origem)
        m.estruturas[p+4],m.estruturas[p+8]=1,tipo
    return m,maquina,estruturas


def aplicar_cenario(m,estruturas):
    for indice,tipo,origem in estruturas:
        m.aplicar_terreno_estrutura(indice,origem,400)


def retirar_cenario(m,estruturas):
    for indice,_,_ in estruturas:
        m.resetar_terreno_estrutura(indice,1)
        m.remover_regioes_estrutura(indice)
        m.resetar_terreno_estrutura(indice,0)


def executar_terreno_cenario(nome,limite=1200):
    m,maquina,estruturas=preparar_terreno_cenario(nome)
    aplicar_cenario(m,estruturas)
    trajeto=[m.palavra(0,8)];eventos=[];mudancas=[]
    rotulos=lambda:sum(bool(v&0x8000) for v in m.regioes)
    mudancas.append(dict(ciclo=0,acao='aplicar',celulas_de_estrutura=rotulos()))
    maquina.postar(0,1,(0,0x40a));maquina.atualizar(0)
    for ciclo in range(1,limite+1):
        if nome=='edificio_retirado' and ciclo==28:
            retirar_cenario(m,estruturas)
            mudancas.append(dict(ciclo=ciclo,acao='retirar',celulas_de_estrutura=rotulos()))
        evento=m.atualizar_movimento(0,maquina)
        if evento:eventos.append(dict(ciclo=ciclo,**evento))
        celula=m.palavra(0,8)
        if celula!=trajeto[-1]:trajeto.append(celula)
        if m.unidades[2]==7:break
    else:raise RuntimeError('O trajeto não terminou no limite')
    maquina.atualizar(0)
    return dict(nome=nome,atualizacoes=ciclo,mudancas_terreno=mudancas,
                trajeto=[[c&255,c>>8] for c in trajeto],posicao_final=[celula&255,celula>>8],
                buscas=m.historico_navegacao,eventos=eventos,tarefas_ativas=maquina.ativas)


if __name__=='__main__':
    dados=dict(executa_x86=False,contexto='Edifícios, terreno e tarefas sintéticos; não é uma missão carregada.',
               cenarios=[executar_terreno_cenario(n) for n in ('edificio','edificio_retirado','parede')])
    destino=Path(__file__).resolve().parents[1]/'relatorios/terreno-estruturas-python.json'
    destino.write_text(json.dumps(dados,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(destino)
