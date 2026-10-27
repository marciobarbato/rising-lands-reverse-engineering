"""Duas demonstrações sintéticas de navegação, integralmente em Python."""
import json
import struct
from pathlib import Path
from demonstrar_desvios import preparar_cenario
from solucionador_python import SolucionadorCaminhosPython


def preparar_integracao(nome, solucionador=None):
    m, maquina, bloqueios, _ = preparar_cenario(
        'parede_com_passagem' if nome == 'muros' else 'sem_passagem',
        solucionador or SolucionadorCaminhosPython())
    if nome == 'muros':
        for i, (x,y) in enumerate(bloqueios):
            c, p = x+y*256, i*276
            struct.pack_into('<H',m.estruturas,p+2,c)
            m.estruturas[p+4],m.estruturas[p+8] = 1,9
            m.modificar_regiao_estrutura(i,0,c,True)
            m.objetos[c] = 0
        indices = (0,)
    elif nome == 'aliados_bloqueadores':
        for i,c in ((1,0x403),(2,0x303)):
            u = bytearray(m.ler_unidade(0))
            u[0x72] = 1
            u[0x10a] = u[2]
            struct.pack_into('<I',u,0x10c,0xffffffff)
            for off in (8,0x7c,0x7e): struct.pack_into('<H',u,off,c)
            m.escrever_unidade(i,u); m.ocupar(i,c,True)
        indices = (0,1,2)
    else:
        raise ValueError('Cenário desconhecido')
    return m,maquina,bloqueios,indices


def executar_integracao(nome, limite=1200):
    m,maquina,bloqueios,indices = preparar_integracao(nome)
    trajetos = {i:[m.palavra(i,8)] for i in indices}
    ordens,eventos = [],[]
    maquina.postar(0,1,(0,0x40a)); maquina.atualizar(0)
    for ciclo in range(1,limite+1):
        destinos = {i:m.palavra(i,0x7e) for i in indices}
        for i in indices:
            evento = m.atualizar_movimento(i,maquina)
            if evento: eventos.append(dict(ciclo=ciclo,**evento))
            if m.palavra(i,8) != trajetos[i][-1]: trajetos[i].append(m.palavra(i,8))
        for i in indices[1:]:
            if m.palavra(i,0x7e) != destinos[i]:
                ordens.append(dict(ciclo=ciclo,unidade=i,destino=m.palavra(i,0x7e)))
        if all(m.unidades[i*276+2] == 7 for i in indices): break
    else:
        raise RuntimeError('Cenário não terminou dentro do limite')
    maquina.atualizar(0)
    def xy(c): return [c&255,c>>8]
    return dict(nome=nome,atualizacoes=ciclo,
                trajetos={str(i):[xy(c) for c in cs] for i,cs in trajetos.items()},
                ordens_a_bloqueadores=ordens,eventos=eventos,
                posicoes_finais={str(i):xy(m.palavra(i,8)) for i in indices},
                buscas=m.historico_navegacao,tarefas_ativas=maquina.ativas)


if __name__ == '__main__':
    dados = dict(executa_x86=False,contexto='Mapas, muros, unidades e tarefas sintéticos.',
                 cenarios=[executar_integracao(n) for n in ('muros','aliados_bloqueadores')])
    destino = Path(__file__).resolve().parents[1]/'relatorios/estruturas-desbloqueio-python.json'
    destino.write_text(json.dumps(dados,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(destino)
