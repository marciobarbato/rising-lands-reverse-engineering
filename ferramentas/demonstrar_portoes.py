"""Portão libera passagem e recusa fechamento com unidade na célula."""
import json
from pathlib import Path
from demonstrar_colocacao_estruturas import preparar_colocacao_cenario,colocar_cenario


def preparar_portao_cenario():
    m,maquina,estruturas=preparar_colocacao_cenario('muro_com_portao')
    colocar_cenario(m,estruturas)
    return m,maquina,5,0x506


def executar_portao_cenario(limite=1200):
    m,maquina,indice,celula=preparar_portao_cenario()
    maquina.postar(0,1,(0,0x40a));maquina.atualizar(0)
    m.alternar_portoes(celula,indice)
    comandos=[dict(ciclo=0,acao='solicitar_liberacao',fase=m.estruturas[indice*276+0x76])]
    mudancas=[];trajeto=[m.palavra(0,8)];eventos=[]
    recusou=solicitou=False
    for ciclo in range(1,limite+1):
        anterior=m.estruturas[indice*276+0x76]
        m.avancar_estado_portao(indice)
        fase=m.estruturas[indice*276+0x76]
        if fase in (0,15) and fase!=anterior:
            mudancas.append(dict(ciclo=ciclo,fase=fase,colisao=m.atributos[celula]&1,regiao=m.regioes[celula]))
        ocupada=celula in (m.palavra(0,8),m.palavra(0,0x7c))
        if ocupada and not recusou:
            m.alternar_portoes(celula,indice)
            comandos.append(dict(ciclo=ciclo,acao='bloqueio_recusado_com_ocupante',fase=m.estruturas[indice*276+0x76]))
            recusou=True
        elif recusou and not ocupada and not solicitou:
            m.alternar_portoes(celula,indice)
            comandos.append(dict(ciclo=ciclo,acao='solicitar_bloqueio_livre',fase=m.estruturas[indice*276+0x76]))
            solicitou=True
        evento=m.atualizar_movimento(0,maquina)
        if evento:eventos.append(dict(ciclo=ciclo,**evento))
        atual=m.palavra(0,8)
        if atual!=trajeto[-1]:trajeto.append(atual)
        if m.unidades[2]==7 and m.estruturas[indice*276+0x76]==0:break
    else:raise RuntimeError('Trajeto e portão não terminaram no limite')
    if not recusou or not solicitou or celula not in trajeto:raise RuntimeError('A demonstração não atravessou o portão')
    maquina.atualizar(0)
    return dict(atualizacoes=ciclo,portao=[celula&255,celula>>8],comandos=comandos,mudancas=mudancas,
                trajeto=[[c&255,c>>8] for c in trajeto],posicao_final=[atual&255,atual>>8],
                fase_final=m.estruturas[indice*276+0x76],colisao_final=m.atributos[celula]&1,
                buscas=m.historico_navegacao,eventos=eventos,tarefas_ativas=maquina.ativas)


if __name__=='__main__':
    r=dict(executa_x86=False,contexto='Portão, registros e trajeto sintéticos; sem desenho ou seleção de quadros.',
           cenario=executar_portao_cenario())
    destino=Path(__file__).resolve().parents[1]/'relatorios/portoes-python.json'
    destino.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(destino)
