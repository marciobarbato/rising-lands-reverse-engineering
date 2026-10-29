"""Replay original-first M3 display captures through the public renderer (no emulation)."""
import argparse, base64, hashlib, inspect, json, struct, time, zlib
from contextlib import ExitStack
from unittest.mock import patch
from pathlib import Path
from graficos import Catalogo
from render_quadro import renderizar_quadro, EstadoCache

AQUI=Path(__file__).resolve().parent
sha=lambda d:hashlib.sha256(bytes(d)).hexdigest()

class CatalogoRastreado(Catalogo):
    def quadro(self,ident):
        self.ultimo_id=ident
        return super().quadro(ident)

class ArgumentosRasterM3:
    """Observe Python raster entry arguments, including old bodies/facades, without changing API call output.

    Each compositor obtains its asset immediately before the raster call. The calling compositor supplies the
    operation (plain/player/shadow/gray) and clip flag; no ID is inferred from pixels or from the native answer.
    """
    def __init__(self,catalog):self.catalog,self.calls=catalog,[]
    def __enter__(self):
        import composicao, construcoes, corpo_tipos1_8, hud_quadro, objetos, projeteis_graficos, quadro_jogo, sobreposicoes_entrada_m3
        import cave_scriptada_m3, hud_scriptado_m3
        self.stack=ExitStack()
        def wrap(fn,shadow):
            def call(*args,**kwargs):
                caller=inspect.currentframe().f_back
                name,local=caller.f_code.co_name,caller.f_locals
                routine,owner='PasteOmbreCmp' if shadow else 'PasteBobCmp',None
                clip=1
                if not shadow and name=='compor_fachada' and local['camada']['operacao']=='jogador':
                    routine,owner='PastePlayerCmp',local['camada']['jogador']
                elif not shadow and name=='_icone_fadiga':routine,owner='PastePlayerCmp',local['r'][0]
                elif not shadow and name=='player':routine,owner='PastePlayerCmp',local['owner']
                elif not shadow and name=='bob':
                    if 'owner' in local and local['owner'] is not None:routine,owner='PastePlayerCmp',local['owner']
                    if 'recorte' in local:clip=int(bool(local['recorte']))
                elif shadow and name=='zona_icone_acao':routine,clip='PasteNoirBlancCmp',0
                elif shadow and name=='gray':routine='PasteGrisCmp'
                x,y=args[4:6];i16=lambda v:(v+32768)%65536-32768
                self.calls.append([routine,i16(x),i16(y),self.catalog.ultimo_id,clip]+([] if owner is None else [owner]))
                return fn(*args,**kwargs)
            return call
        for module in (composicao,construcoes,corpo_tipos1_8,hud_quadro,objetos,projeteis_graficos,quadro_jogo,sobreposicoes_entrada_m3,cave_scriptada_m3):
            for attr,shadow in (('compor_indices',False),('compor_sombra',True)):
                if hasattr(module,attr):self.stack.enter_context(patch.object(module,attr,wrap(getattr(module,attr),shadow)))
        original_box=hud_quadro._Hud.caixa
        def box(h,*args):self.calls.append(['Box',*args[:5],int(bool(args[5]))]);return original_box(h,*args)
        self.stack.enter_context(patch.object(hud_quadro._Hud,'caixa',box))
        original_fill=sobreposicoes_entrada_m3.filled
        def fill(c,*args):self.calls.append(['FilledBox',*args,1]);return original_fill(c,*args)
        self.stack.enter_context(patch.object(sobreposicoes_entrada_m3,'filled',fill))
        original_drag=sobreposicoes_entrada_m3.drag
        def drag(c):
            x0,y0,x1,y1=(c.leitura_entrada.i16(a) for a in (0x49a024,0x49a026,0x49a028,0x49a02a));w,h=c.tela.palavras('janela')
            self.calls.append(['Box',x0,y0,min(x1,w*32),min(y1,h*32),1,1]);return original_drag(c)
        self.stack.enter_context(patch.object(sobreposicoes_entrada_m3,'drag',drag))
        def observe_direct(fn,names):
            def call(c,*args,**kwargs):
                before=len(c.chamadas);result=fn(c,*args,**kwargs)
                self.calls.extend(ev for ev in c.chamadas[before:] if ev[0] in names)
                return result
            return call
        for name,ops in (('save_background',('GetBob',)),('restore_background',('PasteBob',)),('shaded_box',('FilledBoxGris','FilledBoxOmbre'))):
            self.stack.enter_context(patch.object(hud_scriptado_m3,name,observe_direct(getattr(hud_scriptado_m3,name),ops)))
        return self
    def __exit__(self,*args):return self.stack.__exit__(*args)


class MemoriaEntradaM3:
    def __init__(self, blocks): self.blocks=blocks
    def ler_mundo(self,a,n):
        for base,d in self.blocks:
            if base<=a and a+n<=base+len(d):return bytes(d[a-base:a-base+n])
        raise KeyError(hex(a))
    def u8(self,a):return self.ler_mundo(a,1)[0]
    def u16(self,a):return struct.unpack('<H',self.ler_mundo(a,2))[0]
    def u32(self,a):return struct.unpack('<I',self.ler_mundo(a,4))[0]

class CapturaEntradaM3:
    def __init__(self,path):
        raw=Path(path).read_bytes();self.sha=sha(raw);self.d=json.loads(raw);self.cache={}
    def blob(self,key):
        if key not in self.cache:
            value=zlib.decompress(base64.b64decode(self.d['blobs'][key]))
            if sha(value)!=key:raise ValueError('Capture blob hash mismatch')
            self.cache[key]=value
        return self.cache[key]
    def memory(self,case):return MemoriaEntradaM3([(int(a,16),self.blob(k)) for a,k in case['entry'].values()])
    def render(self,case,catalog):
        c=case['cache'];cache=EstadoCache(self.blob(c['keys']),self.blob(c['payloads']),c['cursor'])
        return renderizar_quadro(self.memory(case),superficie_anterior=self.blob(case['before']),catalogo=catalog,
                                 cache=cache,habitado=lambda i: {0: True}[i],hud=True,
                                 relogio=lambda:struct.unpack_from('<I',self.blob(case['exit_dgroup']),0x4e17b4-0x494000)[0])

def validar(paths):
    t0=time.monotonic();catalog=CatalogoRastreado();rows=[]
    for path in paths:
        cap=CapturaEntradaM3(path)
        for case in cap.d['cases']:
            with ArgumentosRasterM3(catalog) as raster:result=cap.render(case,catalog)
            ref=cap.blob(case['after'])
            expected_stop = '0x004085cb' if case['name']=='sanctuary_health600_malus100' else None
            mismatch=None if expected_stop else sum(a!=b for a,b in zip(result.pixels,ref))
            calls,native=raster.calls,case['blits']
            argument_errors=[]
            expected_calls=native[:len(calls)] if expected_stop else native
            if calls!=expected_calls:
                argument_errors=[dict(index=i,python=a,native=b) for i,(a,b) in enumerate(zip(calls,expected_calls)) if a!=b]
                if len(calls)!=len(expected_calls):argument_errors.append(dict(python_count=len(calls),native_count=len(expected_calls)))
            # Compare the entire DGROUP after applying ALL exported effects and the returned terrain-cache cursor.
            # Only two process-local DD pointer words belong to the public API binding, rather than game state.
            dg=cap.blob(case['exit_dgroup']);projected=bytearray(cap.memory(case).ler_mundo(0x494000,len(dg)))
            for _,a,old,new in result.efeitos:
                value=bytes.fromhex(new);projected[a-0x494000:a-0x494000+len(value)]=value
            struct.pack_into('<H',projected,0x49a04e-0x494000,result.cache.proximo)
            excluded={a+i for a in (0x508f70,0x4e17a4) for i in range(4)}
            effects=[] if expected_stop else [hex(0x494000+i) for i,(a,b) in enumerate(zip(projected,dg))
                                             if a!=b and 0x494000+i not in excluded]
            rows.append(dict(expected_stop=expected_stop,case=case['name'],capture_sha256=cap.sha,stop=result.parada,pixel_mismatches=mismatch,
                             drawing_calls_checked=len(calls),argument_mismatches=argument_errors,effect_mismatches=effects,
                             surface_sha256=sha(result.pixels),native_sha256=case['after']))
            print(case['name'],result.parada,mismatch,argument_errors[:2],effects,flush=True)
    sources={name:sha((AQUI/name).read_bytes()) for name in ('render_quadro.py','quadro_jogo.py','hud_quadro.py',
             'sobreposicoes_entrada_m3.py','corpo_tipos1_8.py','construcoes.py','validar_entrada_m3.py')}
    return dict(schema='rising-lands/m3-input-render-comparison/1',sources_sha256=sources,cases=len(rows),
                complete_cases=sum(r['expected_stop'] is None for r in rows),dependency_stops=sum(r['expected_stop'] is not None for r in rows),
                ignored_binding_fields={'0x004e17a4':'DD lock pointer supplied by the public API test binding',
                                        '0x00508f70':'offscreen pointer supplied by the public API test binding'},
                mismatches=sum(bool((r['stop'] or {}).get('endereco')!=r['expected_stop'] or r['pixel_mismatches'] or r['argument_mismatches'] or r['effect_mismatches']) for r in rows),
                elapsed_seconds=round(time.monotonic()-t0,3),rows=rows)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--captura',action='append');p.add_argument('--saida',required=True);a=p.parse_args()
    result=validar(a.captura or [AQUI/'evidencias/captura-entrada-m3.json',AQUI/'evidencias/captura-entrada-m3-suplementar.json'])
    Path(a.saida).write_text(json.dumps(result,indent=1)+'\n');raise SystemExit(bool(result['mismatches']))
