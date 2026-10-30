"""Check isolated original probe-origin effects against the existing Graphics/AI ownership contract."""
import argparse,hashlib,json,sys
from pathlib import Path
from validar_janelas_api18 import CapturaLimitada,AQUI
from efeitos_logicos_exibicao import desenhar_jogo

sys.path.insert(0,str(AQUI.parent/'ia-runtime'))
import ambiente_ia_runtime
from affgame_hud_ia import affgame_hud

sha=lambda b:hashlib.sha256(b).hexdigest()

def validar():
    policy_path=AQUI.parent/'missoes/validacao/m2-3-politica-comparacao-9200-quadros.json'
    policy=json.loads(policy_path.read_text())
    display={a for lo,hi in policy['cumulative']['exclusion_mask'] if int(lo,16)<0x523000
             for a in range(int(lo,16),int(hi,16))}
    paths=[AQUI/'evidencias/sonda-origens-K1-129-189.json.xz.origins.json']
    paths+=sorted((AQUI/'evidencias').glob('sonda-colheita-P[45]-*.json.xz.origins.json'))
    rows=[];origins=set();pins={}
    for path in paths:
        isolated=json.loads(path.read_text());pins[path.name]=sha(path.read_bytes())
        cap=CapturaLimitada(Path(str(path).removesuffix('.origins.json')))
        assert cap.d['status']=='complete'
        assert all(c['surface_equal'] and c['state_equal'] for c in cap.d['checks'])
        for case in isolated['records']:
            row=next(r for r in cap.d['rows'] if r['frame']==case['frame']);m=cap.memory(row)
            result=desenhar_jogo(m,habitado=lambda i:True)
            assert result.escritas==(),result
            # This byte is game logic, separately implemented by AI; it is never added to the display mask.
            effect=affgame_hud(m,desenhar_jogo)
            flag=m.u8(0x4e05a2)
            for address,width,value in effect.escritas:
                assert (address,width)==(0x4e05a2,1)
                flag=value
            native=dict((int(a,16),(old,new)) for a,old,new in case['changed'].get('dgroup',[]))
            assert native.get(0x4e05a2,(m.u8(0x4e05a2),)*2)[1]==flag
            assert int(case['exit_registers']['EAX'],16)==effect.eax
            outside=[hex(a) for a in native if a not in display and a!=0x4e05a2]
            assert not outside,outside
            assert 'crt_thread_data' not in case['changed']
            heap=[]
            for name,change in case['changed'].items():
                if name=='dgroup':continue
                ident=int(name.removeprefix('alloc'))
                # Original display bank metadata, 256 mutable BLOCS cache bitmaps, and cache-key allocation.
                assert ident in (2,24329) or 2196<=ident<2196+512 and ident%2==0,(name,change)
                heap.append(name)
            assert case['returned'] and not case['declared_writes']
            assert case['surface_sha256']==case['published_phase_sha256']==row['after']
            origins.add(tuple(case['origin']))
            rows.append(dict(probe=case['probe'],frame=case['frame'],origin=case['origin'],returned=True,
                surface_equal=True,additional_logic_writes=[],crt_changes=0,ai_flag=flag,ai_eax=effect.eax,display_heap_blocks=heap))
    return dict(schema='rising-lands/probe-origin-effects-comparison/1',cases=len(rows),unique_origins=sorted(map(list,origins)),
        mismatches=0,recording_pins=pins,policy_sha256=sha(policy_path.read_bytes()),
        ai_provider_sha256=sha((AQUI.parent/'ia-runtime/affgame_hud_ia.py').read_bytes()),
        graphics_provider_sha256=sha((AQUI/'efeitos_logicos_exibicao.py').read_bytes()),
        layer_data_sha256=sha((AQUI/'camadas_colheita_m3.json').read_bytes()),
        comparison_source_sha256=sha(Path(__file__).read_bytes()),rows=rows)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    result=validar();Path(a.output).write_text(json.dumps(result,indent=1)+'\n')
    print(result['cases'],'cases',len(result['unique_origins']),'origins',result['mismatches'],'mismatches')
