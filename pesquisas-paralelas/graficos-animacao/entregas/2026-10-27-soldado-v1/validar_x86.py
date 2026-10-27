"""Gera relatório diferencial. Falha imediatamente em divergência ou timeout."""
from pathlib import Path
import hashlib
import json
import struct
import time
from graficos import Catalogo, ORDEM, QUANTIDADES, consultar, compor_indices, avancar_animacao, ler_cmp
from bancada_x86 import Bancada, UNIDADE, RETORNO, unicorn
from extrair_evidencias import RAIZ, HASH_EXE, COMMIT, exigir_area_editavel


def validar():
    exigir_area_editavel()
    inicio=time.monotonic(); b=Bancada(); c=Catalogo()
    report=dict(commit=COMMIT,exe_sha256=HASH_EXE,unicorn=unicorn.__version__,
                limites=dict(instrucoes_por_chamada_maximo=1000000,microssegundos_por_chamada=2000000),
                substituicoes={'LoadSTRATBank':['0x458420 abrir arquivo','0x458461 ler bytes','0x45844c fechar','0x467ea6 alocar heap'],
                                'captura_desenho':['0x45b796 sombra: registra argumentos e retorna; corpo executado até PasteBobCmp'],
                                'animacao':[], 'PasteBobCmp':[]})
    fontes={n:c._ler('cd/INSTALHD/GRAPHICS/'+n) for n in ORDEM}
    carga=b.carregar_banco_original(fontes)
    assert carga['quantidade']==sum(QUANTIDADES)
    assert carga['aberturas']==list(ORDEM)*2
    registros=[];glob=0
    for nome,conta in zip(ORDEM,QUANTIDADES):
        seq=c.banco(nome)
        for local,q in enumerate(seq):
            ptr,=struct.unpack('<I',b.ler(carga['tabela']+glob*4,4))
            w,h,n,dados=struct.unpack('<HHII',b.ler(ptr,12))
            assert (w,h,n)==(q.largura,q.altura,len(q.comprimido))
            assert b.ler(dados,n)==q.comprimido
            glob+=1
        registros.append(dict(arquivo=nome,quadros=conta,ultimo_id_motor=glob,
                              sha256=hashlib.sha256(fontes[nome]).hexdigest()))
    report['agregacao']=dict(quadros_comparados=glob,aberturas=carga['aberturas'],bancos=registros,
                             descricao='Todos os descritores, dimensões, tamanhos e bytes comprimidos comparados na ordem original.')
    print('Agregação original:',glob,'quadros conferidos',flush=True)
    init=b.inicializar_soldado()
    assert (init[0xa5],init[0xa7])==(8,2)
    report['inicializacao_soldado']={'quantidade_0xa5':8,'periodo_0xa7':2}
    for fase in range(8):
        u=bytearray(init);u[0xa4]=fase;b.escrever(UNIDADE,u)
        r=b.executar(0x448194,[(0x448194,0x448228)],{'EAX':0})
        assert b.ler(UNIDADE+0xa4,1)==b'\x02' and r['EAX']&255==1
    report['parada']=dict(casos=8,fase_resultante=2,rotina='0x448194',sem_substituicoes=True)
    capturas=[]
    for direcao in range(1,17):
        for estado,fases in [('andando',range(8)),('parado',[2])]:
            for fase in fases:
                original=b.capturar_desenho(direcao,fase,estado=2 if estado=='andando' else 7,ate_blitter=True)
                esperado=consultar(0,estado,direcao,fase)
                assert original['id_motor']==esperado['id_motor']
                assert (original['x'],original['y'])==(88,106)
                assert original['sombras']==[dict(id_motor=10784,x=130,y=154)]
                capturas.append(dict(tipo=0,estado=estado,direcao=direcao,fase=fase,**original))
    report['capturas_desenho']=capturas
    deslocamentos=[]
    for dx,dy in [(0,0),(1,2),(-1,-2),(31,31),(-31,-31),(-128,127),(127,-128)]:
        original=b.capturar_desenho(1,2,dx=dx,dy=dy,ate_blitter=True)
        assert (original['x'],original['y'])==(88+dx,106+dy)
        deslocamentos.append(dict(dx=dx,dy=dy,resultado=original))
    report['ancoragem']=deslocamentos
    print('Seleção e ancoragem:',len(capturas)+len(deslocamentos),'capturas conferidas',flush=True)
    casos=0
    for fase in range(8):
        pares=[(2,contador) for contador in range(256)]
        pares += [(periodo,contador) for periodo in (0,1,3,255) for contador in (0,1,2,254,255)]
        for periodo,contador in pares:
            esperado=avancar_animacao(fase,contador,periodo)
            u=bytearray(init);u[0xa4]=fase;u[0xa9]=contador;u[0xa7]=periodo
            # AvanceEngin suite: passo já preparado; pára ANTES de giro/avanço físico.
            u[0x86]=1;struct.pack_into('<H',u,8,0x202);struct.pack_into('<H',u,0x7c,0x203)
            for entrada,intervalos,paradas in [
                (0x448088,[(0x448088,0x44812b),(0x448084,0x448088)],()),
                (0x448f50,[(0x448f50,0x449048)],[0x449048])]:
                b.escrever(UNIDADE,u)
                b.executar(entrada,intervalos,{'EAX':0},paradas=paradas)
                result=b.ler(UNIDADE,276)
                assert (result[0xa4],result[0xa9])==esperado
                casos+=1
    report['contadores']=dict(casos=casos,rotinas=['0x448088','0x448f50..0x449048'],
                              periodos=[0,1,2,3,255],contadores_periodo_2='todos 0..255',
                              fases='todas 0..7',taxa_segundos=None)
    # Quando não há próximo passo, a animação não avança nesse caminho.
    u=bytearray(init);u[0xa4]=2;u[0x86]=1;b.escrever(UNIDADE,u)
    b.executar(0x448f50,[(0x448f50,0x449048)],{'EAX':0},paradas=[0x440d58])
    assert b.ler(UNIDADE,276)==u
    report['contadores']['sem_passo_preserva']=True
    print('Contadores:',casos,'comparações conferidas',flush=True)
    direcoes=[]
    from graficos import VETORES
    for n,(dx,dy) in enumerate(VETORES):
        atual=0x202;destino=atual+256*dy+dx
        r=b.executar(0x477042,[(0x477042,0x4770ee)],{'EAX':atual,'EDX':destino})
        assert r['EAX']&255==n*2+1
        direcoes.append(dict(dx=dx,dy=dy,direcao=r['EAX']&255))
    report['direcoes']=direcoes
    composicoes=[];w=h=128;fundo=bytes((i*17+23)%256 for i in range(w*h))
    for id_motor in range(2082,2146):
        q=c.quadro(id_motor);rec=(0,0,w-1,h-1)
        x,y=24,30
        original=b.blit(id_motor,x,y,w,h,fundo,rec)
        assert original==compor_indices(fundo,w,h,q,x,y,rec)
        composicoes.append(dict(id_motor=id_motor,x=x,y=y,recorte=rec,sha256_superficie=hashlib.sha256(original).hexdigest()))
    q=c.quadro(2084)
    for x,y,rec in [(-20,30,(0,0,127,127)),(30,-20,(0,0,127,127)),(100,30,(0,0,127,127)),
                    (30,100,(0,0,127,127)),(-100,30,(0,0,127,127)),(30,-100,(0,0,127,127)),
                    (200,30,(0,0,127,127)),(30,200,(0,0,127,127)),(12,12,(24,24,70,70)),
                    (-10,-10,(0,0,127,127)),(125,125,(0,0,127,127))]:
        original=b.blit(2084,x,y,w,h,fundo,rec)
        assert original==compor_indices(fundo,w,h,q,x,y,rec),(x,y,rec)
        composicoes.append(dict(id_motor=2084,x=x,y=y,recorte=rec,sha256_superficie=hashlib.sha256(original).hexdigest()))
    # Literal 0, cor 255 e salto: testar sem assumir que índice 0 é transparente.
    raw=struct.pack('<H',1)+struct.pack('<HHI',4,1,5)+bytes([1,254,0,255,1])
    q=ler_cmp(raw)[0];ptr=b.alocar(12);data=b.alocar(5);b.escrever(data,q.comprimido)
    b.escrever(ptr,struct.pack('<HHII',4,1,5,data))
    b.escrever(carga['tabela'],struct.pack('<I',ptr))
    original=b.blit(1,2,3,w,h,fundo,(0,0,127,127))
    assert original==compor_indices(fundo,w,h,q,2,3)
    report['composicao']=dict(casos=len(composicoes)+1,comparacoes=composicoes,literal_zero_opaco=True,
                              rotina='0x45b247',substituicoes=[])
    report['execucoes_delimitadas']=b.execucoes
    report['instrucoes_observadas']=b.instrucoes
    report['duracao_segundos']=round(time.monotonic()-inicio,3)
    report['resultado']='PASSOU'
    report['limites_de_conclusao']=[
        'Não executa o jogo inteiro; unidade e superfície são cenários sintéticos.',
        'IO e alocação do agregador substituídos; todos os bytes CMP comparados.',
        'Sombra interceptada na captura. Transformação de cores da sombra não validada.',
        'Palette PIE herdada de evidência commitada; nenhuma comparação DirectDraw.',
        'Taxa em segundos e despacho completo de simulação não determinados.']
    pasta=RAIZ/'validacao';pasta.mkdir(exist_ok=True)
    (pasta/'x86.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PASSOU:',b.execucoes,'execuções delimitadas;',report['duracao_segundos'],'segundos',flush=True)


if __name__=='__main__':
    validar()
