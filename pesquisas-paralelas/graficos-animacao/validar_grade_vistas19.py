"""Validate recorded native view effects without extending the historical display exclusion mask."""
import argparse,base64,hashlib,json,lzma,struct,subprocess,zlib
from pathlib import Path

AQUI=Path(__file__).resolve().parent
sha=lambda raw:hashlib.sha256(raw).hexdigest()

class MemoriaGrade:
    def __init__(self,d,row):
        self.dg=bytearray(zlib.decompress(base64.b64decode(d['opening_dgroup_zlib'])))
        self.pb=int(d['projectile_base'],16);self.proj=zlib.decompress(base64.b64decode(d['opening_projectiles_zlib']))
        for address,value in row['writes']:
            a=int(address,16)-0x494000;v=bytes.fromhex(value);self.dg[a:a+len(v)]=v
    def raw(self,a,n):
        if 0x494000<=a and a+n<=0x523000:return self.dg[a-0x494000:a-0x494000+n]
        if self.pb<=a and a+n<=self.pb+len(self.proj):return self.proj[a-self.pb:a-self.pb+n]
        raise KeyError((hex(a),n))
    def u8(self,a):return self.raw(a,1)[0]
    def u16(self,a):return int.from_bytes(self.raw(a,2),'little')
    def u32(self,a):return int.from_bytes(self.raw(a,4),'little')

def validar(partial=False,compare_provider=False):
    policy_path=AQUI.parent/'missoes/validacao/m2-3-politica-comparacao-9200-quadros.json'
    policy=json.loads(policy_path.read_text())
    display={a for lo,hi in policy['cumulative']['exclusion_mask'] if int(lo,16)<0x523000
             for a in range(int(lo,16),int(hi,16))}
    producer_versions={ref:sha(subprocess.check_output(['git','show',ref+':pesquisas-paralelas/graficos-animacao/capturar_grade_vistas19.py'],cwd=AQUI))
                       for ref in ('f19f498','8c9af14')}
    pins={};seen=set();rows=[];by_routine={'AffGame':set(),'RestoreAll':set()};seconds=[]
    functions={}
    if compare_provider:
        from efeitos_logicos_exibicao import desenhar_jogo,restaurar_tudo
        functions=dict(AffGame=desenhar_jogo,RestoreAll=restaurar_tudo)
    origins=[(x,y) for y in range(48) for x in range(40)]
    for path in sorted((AQUI/'evidencias').glob('grade-vistas19-[0-9][0-9][0-9][0-9].json.xz')):
        raw=path.read_bytes();pins[path.name]=sha(raw);d=json.loads(lzma.decompress(raw));seconds.append(d['elapsed_seconds'])
        assert d['executable_sha256']=='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
        assert d['code_sha256']=='02985de5c6218c3968a45fa5b5cdc4bf4be850a8d87d92520c6e184098518af4'
        assert d['source_sha256'] in producer_versions.values()
        assert d['map']==[64,64] and d['viewport']==[25,17] and len(d['rows'])==2*d['count']
        expected=[(name,origin) for origin in origins[d['offset']:d['offset']+d['count']] for name in by_routine]
        assert [(r['routine'],tuple(r['origin'])) for r in d['rows']]==expected
        for row in d['rows']:
            name=row['routine'];origin=tuple(row['origin']);key=(name,origin)
            assert key not in seen;seen.add(key);by_routine[name].add(origin)
            assert row['returned'] and row['registers']['EIP']==0x3000000 and not row['cursor_writer_hits']
            assert row['writes']==[[hex(a),struct.pack('<H',v).hex()] for a,v in zip((0x508720,0x508722),origin)]
            m=MemoriaGrade(d,row);assert m.u8(0x508041)==0 and m.u8(0x4e2f78)==0x12
            assert 'crt_thread_data' not in row['changed']
            outside=[];heap=[]
            for allocation,change in row['changed'].items():
                if allocation=='dgroup':
                    assert change['base']=='0x494000' and change['size']==len(m.dg) and change['before']==sha(m.dg)
                    rebuilt=bytearray(m.dg)
                    assert change['count']==len(change['changes'])
                    for address,old,new in change['changes']:
                        a=int(address,16);assert m.u8(a)==old and old!=new
                        rebuilt[a-0x494000]=new
                        if a not in display:outside.append(address)
                    assert sha(rebuilt)==change['after']
                else:
                    ident=int(allocation.removeprefix('alloc'))
                    assert ident in (2,24329) or 2196<=ident<2708 and ident%2==0,(allocation,change)
                    heap.append(allocation)
            assert not outside,(name,origin,outside)
            if compare_provider:assert functions[name](m).escritas==()
            rows.append(dict(routine=name,origin=list(origin),native_return=True,additional_logic_writes=[],crt_changes=0,
                cursor_writer_hits=0,display_heap_blocks=heap,provider_equal=True if compare_provider else None))
    complete=len(seen)==3840 and all(s==set(origins) for s in by_routine.values())
    if not partial:assert complete,('Incomplete native view matrix',len(seen))
    result=dict(schema='rising-lands/native-view-effects-comparison/1',cases=len(rows),expected_cases=3840,complete=complete,
        mismatches=0,provider_compared=compare_provider,origins_by_routine={n:sorted(map(list,v)) for n,v in by_routine.items()},
        native_capture_pins=pins,policy_contract='existing cumulative display mask, unchanged',producer_versions=producer_versions,
        comparison_sha256=sha(Path(__file__).read_bytes()),native_seconds_total=sum(seconds),native_seconds_max=max(seconds),rows=rows)
    if compare_provider:
        result['provider_sha256']=sha((AQUI/'efeitos_logicos_exibicao.py').read_bytes())
        result['domain_table_sha256']=sha((AQUI/'origens_efeitos_monde01.json').read_bytes())
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--partial',action='store_true');p.add_argument('--compare-provider',action='store_true')
    p.add_argument('--output',required=True);a=p.parse_args();d=validar(a.partial,a.compare_provider)
    Path(a.output).write_text(json.dumps(d,indent=1)+'\n');print(d['cases'],'native calls;',d['mismatches'],'mismatches;',d['complete'],'complete',flush=True)
