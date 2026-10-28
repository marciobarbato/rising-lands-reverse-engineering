"""Comparação original dos tipos 5/6/7/9. Não investiga regras de economia."""
import hashlib
import json
import struct
import time
from graficos import Catalogo, ORDEM, consultar, avancar_animacao, compor_indices, TIPOS
from bancada_x86 import Bancada, UNIDADE, unicorn
from extrair_evidencias import RAIZ, COMMIT, HASH_EXE, exigir_area_editavel


def validar():
    exigir_area_editavel()
    inicio=time.monotonic();b=Bancada();c=Catalogo()
    report=dict(commit_snapshot=COMMIT,commit_anterior='e531dbbdbe650ae2cbdeab03567981d2d8cd15bd',
                exe_sha256=HASH_EXE,unicorn=unicorn.__version__,
                limites=dict(instrucoes_por_chamada_maximo=1000000,microssegundos_por_chamada=2000000),
                substituicoes={'captura_desenho':['PasteOmbreCmp: registra argumentos e retorna'],
                               'BagVide':[], 'EnginSetTypeCaract':[], 'EnginEnArret':[],
                               'animacao':[], 'PasteBobCmp':[],
                               'LoadSTRATBank':['IO e alocação conforme bancada_x86.py']})
    # Valores transcritos dos ramos, independentemente da estrutura TIPOS da API.
    parametros={5:(5,11,11,1602,1698),6:(2,16,20,2978,3042),
                7:(3,26,26,1346,1474),9:(5,19,14,1826,None)}
    report['parametros']=[];report['paradas']=[];report['capturas_desenho']=[]
    report['campos_bolsa']=[];report['ancoragem']=[];report['contadores']=[]
    for tipo,(stop,ax,ay,base_vazio,base_cheio) in parametros.items():
        init=b.inicializar_tipo(tipo)
        assert (init[0xa5],init[0xa7],init[0x99])==(8,2,0)
        report['parametros'].append(dict(tipo=tipo,quantidade=8,periodo=2,oscilacao_0x99=0))
        for fase in range(8):
            u=bytearray(init);u[0xa4]=fase;u[0xa9]=77;b.escrever(UNIDADE,u)
            r=b.executar(0x448194,[(0x448194,0x448228)],{'EAX':0})
            final=b.ler(UNIDADE,276)
            assert final[0xa4]==stop and final[0xa9]==77 and r['EAX']&255==1
            report['paradas'].append(dict(tipo=tipo,fase_entrada=fase,fase_saida=stop,contador_preservado=77))
        for bolsa in ([0,1] if base_cheio else [0]):
            for direcao in range(1,17):
                for estado,fases in [('andando',range(8)),('parado',[stop])]:
                    for fase in fases:
                        o=b.capturar_desenho(direcao,fase,estado=2 if estado=='andando' else 7,
                            tipo=tipo,bolsa_u16=bolsa,ate_blitter=True)
                        api=consultar(tipo,estado,direcao,fase,bolsa_u16=bolsa)
                        base=base_cheio if bolsa else base_vazio
                        assert o['id_motor']==base+8*((direcao-1)//2)+fase==api['id_motor']
                        assert (o['x'],o['y'])==(128-ax,128-ay)
                        assert o['sombras']==[dict(id_motor=10784,x=130,y=154)]
                        report['capturas_desenho'].append(dict(tipo=tipo,bolsa_u16=bolsa,
                            estado=estado,direcao=direcao,fase=fase,**o))
        # u16 inteiro, incluindo bits do segundo byte, e seis bytes posteriores.
        for bolsa in sorted({0,1,255,256,65535}|{1<<bit for bit in range(16)}):
            for resto in (bytes(6),bytes([255])*6):
                o=b.capturar_desenho(15,stop,tipo=tipo,bolsa_u16=bolsa,
                                     resto_bolsa=resto,ate_blitter=True)
                api=consultar(tipo,'parado',15,bolsa_u16=bolsa)
                assert o['id_motor']==api['id_motor']
                report['campos_bolsa'].append(dict(tipo=tipo,bolsa_u16=bolsa,
                    resto_hex=resto.hex(),id_motor=o['id_motor']))
        for dx,dy in [(0,0),(1,2),(-1,-2),(31,31),(-31,-31),(-128,127),(127,-128)]:
            o=b.capturar_desenho(1,stop,tipo=tipo,bolsa_u16=1,dx=dx,dy=dy,ate_blitter=True)
            assert (o['x'],o['y'])==(128+dx-ax,128+dy-ay)
            assert o['sombras']==[dict(id_motor=10784,x=130+dx,y=154+dy)]
            report['ancoragem'].append(dict(tipo=tipo,dx=dx,dy=dy,**o))
        # Exaustivo para período inicial 2: 8 fases x 256 contadores x 2 caminhos.
        casos=0
        for fase in range(8):
            for contador in range(256):
                u=bytearray(init);u[0xa4]=fase;u[0xa9]=contador
                u[0x86]=1;struct.pack_into('<H',u,8,0x202);struct.pack_into('<H',u,0x7c,0x203)
                for entrada,intervalos,paradas in [
                    (0x448088,[(0x448084,0x44812b)],()),
                    (0x448f50,[(0x448f50,0x449048)],[0x449048])]:
                    b.escrever(UNIDADE,u);b.executar(entrada,intervalos,{'EAX':0},paradas=paradas)
                    result=b.ler(UNIDADE,276)
                    assert (result[0xa4],result[0xa9])==avancar_animacao(fase,contador)
                    casos+=1
        report['contadores'].append(dict(tipo=tipo,casos=casos,periodo=2,quantidade=8))
        print('Tipo',tipo,': desenho, bolsa, parada, âncora e contador conferidos',flush=True)
    # Descritores carregados pelo agregador original antes da comparação do blitter.
    b.carregar_banco_original({n:c._ler('cd/INSTALHD/GRAPHICS/'+n) for n in ORDEM})
    w=h=128;fundo=bytes((i*17+23)%256 for i in range(w*h));composicoes=[]
    for tipo,(_,ax,ay,b0,b1) in parametros.items():
        for base in ([b0,b1] if b1 else [b0]):
            for frame in range(64):
                id_motor=base+frame;x=y=24;rec=(0,0,127,127);q=c.quadro(id_motor)
                original=b.blit(id_motor,x,y,w,h,fundo,rec)
                assert original==compor_indices(fundo,w,h,q,x,y,rec)
                composicoes.append(dict(id_motor=id_motor,x=x,y=y,recorte=rec,
                                        sha256_superficie=hashlib.sha256(original).hexdigest()))
    report['composicoes']=composicoes
    report['execucoes_delimitadas']=b.execucoes;report['instrucoes_observadas']=b.instrucoes
    report['duracao_segundos']=round(time.monotonic()-inicio,3)
    report['limites_de_conclusao']=[
        'Jogador 0 e sem efeitos especiais; somente corpo até PasteBobCmp.',
        'Bolsa é apenas o predicado u16(+0x0a)!=0: nenhum conteúdo, recurso ou regra econômica inferido.',
        'Sombra capturada, transformação de cores não executada.',
        'Estado parado significa EnginEnArret já aplicado; o renderizador não impõe a fase.',
        'Contador avaliado antes do giro/avanço físico, sem frequência global em segundos.',
        'ETA descreve disco; estado 14 dos Colonos não é coberto pelo ramo validado.']
    report['resultado']='PASSOU'
    (RAIZ/'validacao/x86-trabalhadores.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PASSOU:',b.execucoes,'execuções;',len(report['capturas_desenho']),'associações;',len(composicoes),'blits',flush=True)


if __name__=='__main__':validar()
