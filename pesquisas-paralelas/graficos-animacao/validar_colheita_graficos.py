"""Chained probe-window comparison with explicitly verified shared prefixes and bounded blob memory."""
import argparse,hashlib,json,struct,time,lzma
from pathlib import Path
from dataclasses import dataclass
from render_quadro import renderizar_quadro,EstadoCache
from validar_sondas_graficos_m3 import CapturaSondaGrafica,FronteiraTextoGravada,AQUI
from validar_entrada_m3 import MemoriaEntradaM3,CatalogoRastreado,ArgumentosRasterM3
from efeitos_logicos_exibicao import desenhar_jogo,DependenciaExibicao

sha=lambda b:hashlib.sha256(b).hexdigest()
PARTS={
 'P4':tuple(f'sonda-colheita-P4-{lo}-{hi}.json.xz' for lo,hi in ((129,728),(729,1328),(1329,1928),(1929,2528),(2529,3129))),
 'P5':tuple(f'sonda-colheita-P5-{lo}-{hi}.json.xz' for lo,hi in ((129,728),(729,1328),(1329,1928),(1929,2528),(2529,3129))),
 'K1':('janela-K1-129-629-api18.json.xz',)}
LIMITS={'P4':3129,'P5':3129,'K1':629}
SHARED={}
WAIT_CAPTURES=False

class CapturaLimitada(CapturaSondaGrafica):
    def blob(self,key):
        result=super().blob(key)
        while len(self.cache)>60:del self.cache[next(iter(self.cache))]
        return result

@dataclass
class Cadeia:
    pixels:bytes
    cache:object
    background:object=None

def referencias(probe):
    path=AQUI.parent/'missoes/m3/sondas'/probe/'quadros.jsonl.xz'
    return {r['frame']:r for r in map(json.loads,lzma.decompress(path.read_bytes()).splitlines())}

def executar(probe,stop=None,dependencies=None):
    dependencies={} if dependencies is None else dependencies
    stop=stop or LIMITS[probe];catalog=CatalogoRastreado();start=time.monotonic();waited=0;rows=[];state=None;checkpoints={};prefix=None;capture_pins={}
    refs=referencias(probe)
    if probe in SHARED:
        parent,at=SHARED[probe]
        if parent not in dependencies:dependencies[parent]=executar(parent,at,dependencies=dependencies)
        inherited=dependencies[parent];parent_refs=referencias(parent)
        for k in range(129,at+1):
            for key in ('state_sha256','surfaces_between','surfaces_frame'):
                if refs[k][key]!=parent_refs[k][key]:raise AssertionError(('Shared prefix differs',probe,k,key))
        rows=[dict(r,shared_from=parent) for r in inherited['rows'] if r['frame']<=at]
        prefix=dict(probe=parent,through=at,phases=len(rows),published_state_and_surface_hashes_equal=True)
        if len(rows)!=at-128 or inherited['_checkpoints'].get(at) is None:
            return dict(probe=probe,drawn_total=stop-128,equal=sum(r['equal'] for r in rows),first_stop=inherited['first_stop'],rows=rows,
                        shared_prefix=prefix,_checkpoints={})
        inherited_state=inherited['_checkpoints'][at]
        state=Cadeia(inherited_state.pixels,inherited_state.cache,inherited_state.background)
    for filename in PARTS[probe]:
        if rows and rows[-1]['frame']>=stop:break
        path=AQUI/'evidencias'/filename
        if WAIT_CAPTURES:
            begin=time.monotonic();manifest=Path(str(path)+'.manifest.json')
            if not manifest.exists():print(probe,'waiting for native capture',filename,flush=True)
            while not manifest.exists():time.sleep(2)
            waited+=time.monotonic()-begin
            assert json.loads(manifest.read_text())['status']=='complete'
        cap=CapturaLimitada(path);capture_pins[filename]=cap.sha
        for row in cap.d['rows']:
            frame=row['frame']
            if frame>stop:break
            if row['after']!=refs[frame]['surfaces_between']['offscreen']:raise AssertionError('Captured drawing is not the published phase')
            if refs[frame]['surfaces_between']!=refs[frame]['surfaces_frame']:raise AssertionError('Additional frame drawing requires its own provider')
            m=cap.memory(row);native_cache=cap.cache_entry(row)
            if state is None:state=Cadeia(cap.blob(row['before']),native_cache)
            entry_equal=sha(state.pixels)==row['before'] and state.cache==native_cache
            if state.background is not None and 'saved_background' in row['entry']:
                entry_equal=entry_equal and sha(state.background[1])==row['entry']['saved_background'][1]
                m=MemoriaEntradaM3([state.background]+m.blocks)
            if not entry_equal:raise AssertionError(('Chained entry differs',probe,frame))
            def inhabited(index):
                r=m.ler_mundo(0x49a0c8+276*index,276);capacity=struct.unpack_from('<H',r,0xe)[0]
                units=m.u32(0x4e19a0);accepted=[]
                for slot in range(capacity):
                    if r[0x4e+slot]!=1:continue
                    ident=struct.unpack_from('<H',r,0x12+2*slot)[0];kind=m.u8(units+276*ident+1)
                    accepted.append(kind)
                # Exact published predicate: type 2/21 accepts troop types; other types require colonists (9).
                if r[8] in (2,21):return any(t not in (3,11,12,13,14,15,16,17,25) for t in accepted)
                return 9 in accepted
            logic_stop=None
            try:logic=desenhar_jogo(m,habitado=inhabited)
            except DependenciaExibicao as error:logic_stop=dict(address=hex(error.sitio),reason=error.motivo)
            adapter=FronteiraTextoGravada(cap,row)
            with ArgumentosRasterM3(catalog) as raster:
                result=renderizar_quadro(m,superficie_anterior=state.pixels,cache=state.cache,catalogo=catalog,habitado=inhabited,hud=True,
                    texto=adapter,relogio=lambda:struct.unpack_from('<I',cap.blob(row['exit_dgroup']),0x4e17b4-0x494000)[0])
            pixels=sum(a!=b for a,b in zip(result.pixels,cap.blob(row['after'])))
            args=0 if raster.calls==row['blits'] else sum(a!=b for a,b in zip(raster.calls,row['blits']))+abs(len(raster.calls)-len(row['blits']))
            dg=cap.blob(row['exit_dgroup']);projected=bytearray(cap.memory(row).ler_mundo(0x494000,len(dg)))
            for name,a,old,new in result.efeitos:
                value=bytes.fromhex(new)
                if 0x494000<=a<a+len(value)<=0x523000:projected[a-0x494000:a-0x494000+len(value)]=value
                elif name=='saved_background_pixels':state.background=(a,value)
            struct.pack_into('<H',projected,0x49a04e-0x494000,result.cache.proximo)
            ignored={a+i for a in (0x508f70,0x4e17a4) for i in range(4)}
            effects=[] if result.parada else [hex(0x494000+i) for i,(a,b) in enumerate(zip(projected,dg)) if a!=b and 0x494000+i not in ignored]
            equal=not(result.parada or logic_stop or pixels or args or effects or adapter.pending)
            item=dict(frame=frame,equal=equal,stop=result.parada,logic_stop=logic_stop,pixel_mismatches=pixels,argument_mismatches=args,effect_mismatches=effects,
                drawing_calls=len(raster.calls),text_boundaries=adapter.checked,sha256=sha(result.pixels),native_sha256=row['after'])
            if args:item['argument_details']=[dict(i=i,python=a,native=b) for i,(a,b) in enumerate(zip(raster.calls,row['blits'])) if a!=b][:4]
            rows.append(item);state=Cadeia(result.pixels,result.cache,state.background)
            if frame in (2000,2400):checkpoints[frame]=Cadeia(state.pixels,state.cache,state.background)
            if not equal:
                print(probe,'FIRST DIFFERENCE',item,flush=True);break
            if frame%100==0:print(probe,frame,'chained equal',flush=True)
        if rows and not rows[-1]['equal']:break
    first=next((r for r in rows if not r['equal']),None)
    return dict(probe=probe,drawn_total=stop-128,equal=sum(r['equal'] for r in rows),first_stop=first,
        shared_prefix=prefix,capture_pins=capture_pins,elapsed_seconds=round(time.monotonic()-start-waited,3),capture_wait_seconds=round(waited,3),rows=rows,_checkpoints=checkpoints)

def public(report):return {k:v for k,v in report.items() if not k.startswith('_')}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--probe',action='append',choices=tuple(PARTS),required=True);p.add_argument('--stop',type=int);p.add_argument('--wait-captures',action='store_true');p.add_argument('--output',required=True);a=p.parse_args()
    WAIT_CAPTURES=a.wait_captures
    reports={}
    for probe in a.probe:reports[probe]=executar(probe,a.stop,dependencies=reports)
    sources=('render_quadro.py','quadro_jogo.py','hud_quadro.py','sobreposicoes_entrada_m3.py','cave_scriptada_m3.py',
        'hud_scriptado_m3.py','camadas_exibicao_m3.py','camadas_m3_api18.json','colheita_exibicao_m3.py','camadas_colheita_m3.json',
        'efeitos_logicos_exibicao.py','validar_colheita_graficos.py')
    result=dict(schema='rising-lands/m3-harvest-window-comparison/1',boundary_contract='recorded AffText non-execution; default renderer retains missing-glyph stops',
        sources_sha256={n:sha((AQUI/n).read_bytes()) for n in sources},windows=[public(r) for r in reports.values()])
    Path(a.output).write_text(json.dumps(result,indent=1)+'\n')
