"""Comparação x86 delimitada dos objetos 54/66/67/68 e normalização inicial."""
import hashlib
import json
import time
from graficos import Catalogo, ORDEM
from extrair_evidencias import RAIZ, COMMIT, HASH_EXE, exigir_area_editavel
from validar_objetos import BancadaObjetos, eventos
from objetos import compor_passe
from sequenciais import (CODIGOS_SEQUENCIAIS, consultar_sequencial,
                         ler_objetos_eta_v6, normalizar_inicio)


def sha(dados):
    return hashlib.sha256(dados).hexdigest()


def validar():
    exigir_area_editavel()
    inicio = time.monotonic()
    b = BancadaObjetos()
    c = Catalogo()
    r = dict(commit_snapshot=COMMIT,
        commit_predecessor='d96034af2a264e77dc49269c6e0fe563cfddabf4',
        exe_sha256=HASH_EXE,
        limites=dict(instrucoes_maximo=1000000, microssegundos=2000000),
        substituicoes=dict(bancos=['IO e alocação em memória'],
            leitura_ETA=['FileRead em memória'], capturas=['dois blitters interceptados'],
            pixels=[], normalizacao=[], next_anim=[]),
        escopo=['Códigos 54/66/67/68; desenho público 66..68 limitado a auxiliar 0..31',
                'Capturas brutas 32..255 não ampliam o contrato público',
                'Sem regra de alteração econômica do auxiliar; sem tempo em segundos'])
    eta = c._ler('cd/WORLD/MONDE01.ETA')
    r['leituras_ETA'] = b.carregar_eta(eta)
    r['eta'] = ler_objetos_eta_v6(eta)
    r['normalizacao'] = []
    fixtures = [
        ('MONDE01', eta[0x30004:0x40004], eta[0x40004:0x50004]),
        ('todos_codigos_e_auxiliares', bytes(i//256 for i in range(65536)),
         bytes(i%256 for i in range(65536)))]
    for nome, objetos, auxiliares in fixtures:
        b.escrever(b.ptrs['objetos'], objetos)
        b.escrever(b.ptrs['auxiliares'], auxiliares)
        atributos = b.ler(b.ptrs['atributos'], 65536)
        terreno = b.ler(b.ptrs['terreno'], 131072)
        b.executar(0x46c3de, [(0x46c3de,0x46c40a)], paradas=[0x46c40a], limite=1000000)
        out = normalizar_inicio(objetos, auxiliares)
        assert b.ler(b.ptrs['objetos'],65536) == out['objetos']
        assert b.ler(b.ptrs['auxiliares'],65536) == out['auxiliares']
        assert b.ler(b.ptrs['atributos'],65536) == atributos
        assert b.ler(b.ptrs['terreno'],131072) == terreno
        r['normalizacao'].append(dict(fixture=nome,
            objetos_entrada=sha(objetos), auxiliares_entrada=sha(auxiliares),
            objetos_saida=sha(out['objetos']), auxiliares_saida=sha(out['auxiliares']),
            alteradas=out['alteradas'], outras_camadas_preservadas=True))
    print('Normalização: duas camadas completas, duas fixtures conferidas', flush=True)
    r['capturas'] = []
    for codigo in CODIGOS_SEQUENCIAIS:
        for aux in range(256):
            for d,l in ((0,0),(0,16),(16,0)):
                for passe in ('terreno','sprites'):
                    ev,_ = b.desenhar(codigo,aux,d,l,passe)
                    permitido = codigo == 54 or aux <= 31
                    if permitido:
                        plano = consultar_sequencial(codigo,auxiliar_u8=aux,
                            descoberta_u8=d,iluminacao_u8=l)
                        assert ev == eventos(plano,passe), (codigo,aux,d,l,passe,ev)
                    else:
                        # Confirma o acesso bruto do original, sem autorizar outro sprite na API.
                        mid = 0x2a47 + (codigo-66)*16 + aux//2
                        esperado = [] if d or passe == 'sprites' else [
                            dict(id_motor=mid,x=60 if codigo == 66 else 64,y=108,operacao=op)
                            for op in (('copiar',) if l == 0 else ('copiar','sombra'))]
                        assert ev == esperado
                    r['capturas'].append(dict(codigo=codigo,auxiliar=aux,descoberta=d,
                        iluminacao=l,passe=passe,dentro_contrato=permitido,camadas=ev))
    r['next_anim'] = []
    for codigo in CODIGOS_SEQUENCIAIS:
        for aux in range(256):
            for relogio in (0,1,2,3):
                out = b.animar(codigo,aux,relogio,255,bytes(256))
                assert out == dict(fase=aux,indice=255,consumiu=False)
                r['next_anim'].append([codigo,aux,relogio,out['fase'],out['indice']])
    print('Capturas:',len(r['capturas']),'NextAnim:',len(r['next_anim']),flush=True)
    b.carregar_banco_original({n:c._ler('cd/INSTALHD/GRAPHICS/'+n) for n in ORDEM})
    tab = bytes(json.loads((RAIZ/'validacao/x86-composicao.json').read_text())['tabelas_sombra'][1]['indices'])
    r['tabela_sombra'] = list(tab)
    r['pixels'] = []
    fundo = bytes((i*17+23)%256 for i in range(160*160))
    cases = []
    for codigo in CODIGOS_SEQUENCIAIS:
        for aux in ((0,) if codigo == 54 else range(0,32,2)):
            for l in (0,16):cases.append(dict(codigo=codigo,aux=aux,l=l,x=64,y=108,
                recorte=(0,0,159,159),origem='sequencia_completa'))
        for x,y,rec in ((0,0,(0,0,159,159)),(154,154,(0,0,159,159)),
                        (64,108,(70,105,78,118))):
            cases.append(dict(codigo=codigo,aux=31,l=16,x=x,y=y,recorte=rec,origem='recorte'))
    for item in r['eta']['registros']:
        if item['codigo'] in CODIGOS_SEQUENCIAIS:
            for l in (0,16):cases.append(dict(codigo=item['codigo'],aux=item['auxiliar_u8'],
                l=l,x=64,y=108,recorte=(0,0,159,159),origem='MONDE01',celula=item['celula']))
    for case in cases:
        co,aux,l,x,y,rec = (case[k] for k in ('codigo','aux','l','x','y','recorte'))
        plano = consultar_sequencial(co,auxiliar_u8=aux,descoberta_u8=0,iluminacao_u8=l)
        ev,out = b.desenhar(co,aux,0,l,'terreno',x=x,y=y,pixels=True,recorte=rec,tabela=tab)
        assert ev == eventos(plano,'terreno',x,y)
        assert out == compor_passe(c,fundo,160,160,plano,'terreno',x,y,
                                   tabela_sombra=tab,recorte=rec)
        r['pixels'].append(dict(**case,sha256=sha(out)))
    r.update(resultado='PASSOU',execucoes_delimitadas=b.execucoes,
        instrucoes=b.instrucoes,duracao_segundos=round(time.monotonic()-inicio,3))
    (RAIZ/'validacao/x86-sequenciais.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    print('PASSOU:',len(r['pixels']),'buffers;',b.execucoes,'execuções',flush=True)


if __name__ == '__main__':
    validar()
