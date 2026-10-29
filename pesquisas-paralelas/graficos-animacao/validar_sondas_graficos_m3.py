"""Compare scripted-input native render recordings, without executing the game."""
import argparse, hashlib, json, lzma, struct, time
from pathlib import Path
from validar_entrada_m3 import CapturaEntradaM3, CatalogoRastreado, ArgumentosRasterM3,MemoriaEntradaM3
from render_quadro import EstadoCache, renderizar_quadro

AQUI=Path(__file__).resolve().parent
sha=lambda d:hashlib.sha256(bytes(d)).hexdigest()

class FronteiraTextoGravada:
    """The probe's declared non-execution, accepted ONLY after exact input and partial-surface verification.

    This fixture adapter is not a glyph renderer and is never installed by the public API. Every invocation must
    match a committed native boundary's text, font, rectangle, flags and entire pre-boundary surface.
    """
    def __init__(self,cap,row):self.cap,self.pending,self.checked=cap,list(row['text_boundaries']),0
    def __call__(self,request,surface):
        if not self.pending:raise AssertionError('Unrecorded AffText boundary')
        native=self.pending.pop(0);r=native['registers'];stack=bytes.fromhex(native['stack'])
        expected=dict(text=bytes.fromhex(native['text_hex']),x=int(r['EAX'],16),y=int(r['EDX'],16),
            right=int(r['EBX'],16),bottom=int(r['ECX'],16),font=struct.unpack_from('<I',stack,8)[0],flags=struct.unpack_from('<II',stack,12))
        if request!=expected:raise AssertionError(('AffText arguments',request,expected))
        if sha(surface)!=native['surface_before']:raise AssertionError(('AffText partial surface',sha(surface),native['surface_before']))
        self.checked+=1
        return surface  # Explicit Missions display-v2 contract, attested above; never used as normal text rendering.

class CapturaSondaGrafica(CapturaEntradaM3):
    def __init__(self,path):
        raw=Path(path).read_bytes();self.sha=sha(raw)
        self.d=json.loads(lzma.decompress(raw) if str(path).endswith('.xz') else raw);self.cache={}

    def cache_entry(self,row):
        c=row['cache'];return EstadoCache(self.blob(c['keys']),self.blob(c['payloads']),c['cursor'])

    def render(self,row,catalog,previous=None,cache=None,saved_background=None,**kwargs):
        memory=self.memory(row)
        if saved_background is not None:memory=MemoriaEntradaM3([saved_background]+memory.blocks)
        def inhabited(index):
            # BatimentEstHabiter: the captured type-2 bag contains inhabitants; CAVE's bag is empty.
            r=memory.ler_mundo(0x49a0c8+276*index,276)
            return any(r[0x4e:0x4e+struct.unpack_from('<H',r,0xc)[0]])
        return renderizar_quadro(memory,superficie_anterior=self.blob(row['before']) if previous is None else previous,
            cache=self.cache_entry(row) if cache is None else cache,catalogo=catalog,habitado=inhabited,hud=True,
            relogio=lambda:struct.unpack_from('<I',self.blob(row['exit_dgroup']),0x4e17b4-0x494000)[0],**kwargs)

def compare(paths,boundaries=False):
    start=time.monotonic();catalog=CatalogoRastreado();probes=[]
    for path in paths:
        cap=CapturaSondaGrafica(path);rows=[];previous=cache=background=None;chain_live=True
        for row in cap.d['rows']:
            adapter=FronteiraTextoGravada(cap,row) if boundaries else None
            with ArgumentosRasterM3(catalog) as raster:result=cap.render(row,catalog,texto=adapter)
            expected=cap.blob(row['after']);pixels=sum(a!=b for a,b in zip(result.pixels,expected))
            args=[]
            if not result.parada and raster.calls!=row['blits']:
                args=[dict(index=i,python=a,native=b) for i,(a,b) in enumerate(zip(raster.calls,row['blits'])) if a!=b]
                if len(raster.calls)!=len(row['blits']):args.append(dict(python_count=len(raster.calls),native_count=len(row['blits'])))
            dg=cap.blob(row['exit_dgroup']);projected=bytearray(cap.memory(row).ler_mundo(0x494000,len(dg)))
            writes=[]
            for name,a,old,new in result.efeitos:
                value=bytes.fromhex(new)
                if 0x494000<=a<a+len(value)<=0x523000:projected[a-0x494000:a-0x494000+len(value)]=value
                else:writes.append(dict(address=hex(a),sha256=sha(value),bytes=len(value)))
            struct.pack_into('<H',projected,0x49a04e-0x494000,result.cache.proximo)
            excluded={a+i for a in (0x508f70,0x4e17a4) for i in range(4)}
            effects=[] if result.parada else [hex(0x494000+i) for i,(a,b) in enumerate(zip(projected,dg)) if a!=b and 0x494000+i not in excluded]
            chain=None
            if chain_live:
                native_cache=cap.cache_entry(row)
                cache_equal=cache is None or cache==native_cache
                background_equal=background is None or 'saved_background' not in row['entry'] or sha(background[1])==row['entry']['saved_background'][1]
                chained=cap.render(row,catalog,previous,cache,saved_background=background,texto=FronteiraTextoGravada(cap,row) if boundaries else None)
                chain=dict(stop=chained.parada,pixels=sum(a!=b for a,b in zip(chained.pixels,expected)),sha256=sha(chained.pixels),
                    entry_cache_equal=cache_equal,entry_saved_background_equal=background_equal)
                chain_live=not chained.parada and not chain['pixels']
                previous,cache=chained.pixels,chained.cache
                for name,a,old,new in chained.efeitos:
                    if name=='saved_background_pixels':background=(a,bytes.fromhex(new))
            if adapter is not None and not result.parada and adapter.pending:raise AssertionError('Unconsumed AffText boundary')
            rows.append(dict(frame=row['frame'],stop=result.parada,pixel_mismatches=pixels,sha256=sha(result.pixels),native_sha256=row['after'],
                argument_mismatches=args,effect_mismatches=effects,write_only_outputs=writes,text_boundaries_checked=adapter.checked if adapter else 0,
                drawing_calls=len(raster.calls),chained=chain))
            if len(rows)%50==0:print(cap.d['probe'],row['frame'],result.parada,pixels,flush=True)
        first=next((r for r in rows if r['stop'] or r['pixel_mismatches'] or r['argument_mismatches'] or r['effect_mismatches']
            or r['chained'] and (not r['chained']['entry_cache_equal'] or not r['chained']['entry_saved_background_equal'] or r['chained']['pixels'])),None)
        probes.append(dict(probe=cap.d['probe'],capture_sha256=cap.sha,frames=len(rows),surface_equal=sum(not r['stop'] and not r['pixel_mismatches'] for r in rows),
            chained_equal=sum(r['chained'] is not None and not r['chained']['stop'] and not r['chained']['pixels'] for r in rows),first_difference=first,rows=rows))
    return dict(schema='rising-lands/m3-scripted-render-comparison/1',probe_text_boundary_contract=boundaries,
        sources_sha256={p:sha((AQUI/p).read_bytes()) for p in ('render_quadro.py','quadro_jogo.py','hud_quadro.py','sobreposicoes_entrada_m3.py',
            'cave_scriptada_m3.py','hud_scriptado_m3.py','validar_entrada_m3.py','validar_sondas_graficos_m3.py')},elapsed_seconds=round(time.monotonic()-start,3),probes=probes)

def compare_matrix(path):
    from quadro_jogo import _Composicao,EstadoTela,MundoQuadro,GLOBAIS_QUADRO
    from render_quadro import BLOCOS
    from hud_quadro import LeituraHud
    from test_quadro_jogo import tabelas
    cap=CapturaSondaGrafica(path);catalog=CatalogoRastreado();rows=[]
    for row in cap.d['rows']:
        m=cap.memory(row);dg=cap.blob(row['exit_dgroup']);l=m.ler_mundo
        blocks={n:l(m.u32(slot),size) for n,slot,size in BLOCOS}
        world=MundoQuadro(**{n:blocks[n] for n in ('terreno','objetos','auxiliares','regioes','unidades','projeteis')},
            descoberta=[blocks[f'descoberta{i}'] for i in range(4)],iluminacao=[blocks[f'iluminacao{i}'] for i in range(4)],
            estruturas=l(0x49a0c8,276000))
        tela=EstadoTela({n:l(a,w) for n,a,w in GLOBAIS_QUADRO});sombra,ecl=tabelas()
        c=_Composicao(world,tela,cap.blob(row['before']),catalog,None,sombra,ecl)
        c.habitado=lambda i:False;c.leitura_entrada=LeituraHud(m)
        c.batiments(row['registers']['EAX'],row['registers']['EDX'],row['cell'])
        pixels=sum(a!=b for a,b in zip(c.saida,cap.blob(row['after'])))
        projected=bytearray(l(0x494000,len(dg)))
        for _,a,old,new in tela.efeitos:projected[a-0x494000:a-0x494000+len(bytes.fromhex(new))]=bytes.fromhex(new)
        effects=[hex(0x494000+i) for i,(a,b) in enumerate(zip(projected,dg)) if a!=b]
        calls=c.chamadas;args=[] if calls==row['blits'] else dict(python=calls,native=row['blits'])
        rows.append(dict(case=row['name'],pixels=pixels,arguments=args,effects=effects))
        if pixels or args or effects:print(rows[-1],flush=True)
    return dict(cases=len(rows),mismatches=sum(bool(r['pixels'] or r['arguments'] or r['effects']) for r in rows),rows=rows)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--capture',action='append');p.add_argument('--matrix');p.add_argument('--probe-text-boundary',action='store_true');p.add_argument('--output',required=True);a=p.parse_args()
    result=compare_matrix(a.matrix) if a.matrix else compare(a.capture,a.probe_text_boundary);Path(a.output).write_text(json.dumps(result,indent=1)+'\n')
