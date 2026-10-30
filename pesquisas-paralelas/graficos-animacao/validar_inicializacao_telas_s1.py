"""Prepared MenuInit pixel plans against fresh isolated native dependencies, with strict boundary adapters."""
import argparse,json,struct
from pathlib import Path
from telas_inicializacao_s1 import compor_inicializacao_s1
from validar_objetivos_s1 import CapturaTelaS1,AQUI,sha

def i16(v):return (v&65535)-65536 if v&32768 else v&65535

class FronteirasTelaS1Gravadas:
    """Validation only: each deliberate non-execution must attest arguments and the entire incoming surface."""
    def __init__(self,cap,row):
        self.cap,self.row=cap,row;self.pie_checked=False;self.text_checked=False
    def pie(self,request,pixels):
        cases=[r for r in self.row['leaf_calls'] if r['routine']=='LoadPie'];assert len(cases)==1
        case=cases[0]
        assert case['declared_nonexecution']==dict(routine='LoadPie',eax=None,stack_cleanup=0)
        assert request==dict(arquivo=bytes.fromhex(case['text_hex']))
        assert sha(pixels)==case['surface_before']==case['surface_after']
        assert not self.pie_checked;self.pie_checked=True
        return bytes(pixels)
    def text(self,request,pixels):
        assert len(self.row['text_boundaries'])==1;case=self.row['text_boundaries'][0]
        regs={n:int(v,16) for n,v in case['registers'].items()};stack=struct.unpack('<5I',bytes.fromhex(case['stack'])[:20])
        assert (request['x'],request['y'],request['right'],request['bottom'])==tuple(i16(regs[n]) for n in ('EAX','EDX','EBX','ECX'))
        assert (request['font'],tuple(request['flags']))==(stack[2]&255,(stack[3]&255,stack[4]&255))
        if case['text_read_stop'] is not None:
            assert request['text'] is None and request['text_pointer']==int(case['text_pointer'],16)==0
        else:assert request['text']==bytes.fromhex(case['text_hex'])
        assert sha(pixels)==case['surface_before'];assert not self.text_checked;self.text_checked=True
        return bytes(pixels)

def validar(path):
    cap=CapturaTelaS1(path);rows=[]
    assert 'dependency_observer' in cap.d
    for row in cap.d['rows']:
        if row['routine']!='MenuInit':continue
        assert row['dependency_arguments_equal'];m=cap.memory(row);target=row['entry_registers']['EDX']&255
        adapter=FronteirasTelaS1Gravadas(cap,row)
        args=dict(jogador_u8=row['entry_registers']['EAX']&255,modo_destino_u8=target,carregar_pie=adapter.pie,texto=adapter.text)
        if target==0x13:args['mensagem']=dict(pointer=0,text=None)
        else:
            after=next(i for i,c in enumerate(row['leaf_calls']) if c['routine']=='RechercheCalculNew')
            levels={}
            for case in row['leaf_calls'][after+1:]:
                if case['routine']=='RechercheGetNiveau':levels[case['registers']['EDX']&65535]=case['return_eax']&65535
            assert set(levels)==set(range(4))
            args.update(numero_missao_u16=2,niveis_pesquisa=tuple(levels[i] for i in range(4)),
                cor_jogador_u8=160,percentual_texto=b'0%')
            colors=[r['return_eax']&255 for r in row['leaf_calls'] if r['routine']=='PlayerGetColor']
            assert colors==[160]*8
        before=m.ler_mundo(0x494000,0x8f000)
        out=compor_inicializacao_s1(m,cap.blob(row['before']),**args)
        pixels=sum(a!=b for a,b in zip(out['pixels'],cap.blob(row['after'])));arguments=out['chamadas']!=row['blits']
        assert adapter.pie_checked and adapter.text_checked and not(pixels or arguments)
        assert m.ler_mundo(0x494000,0x8f000)==before
        rows.append(dict(frame=row['frame'],target_mode=hex(target),equal=True,pixel_mismatches=pixels,
            argument_mismatches=int(arguments),drawing_calls=len(out['chamadas']),pie_boundaries=1,text_boundaries=1,
            sha256=sha(out['pixels'])))
    assert len(rows)==2
    return dict(schema='rising-lands/s1-menuinit-pixel-comparison/1',cases=2,equal=2,mismatches=0,
        boundary_contract='strict recorded LoadPie and AffText non-execution; opaque text remains an explicit pointer token',
        prepared_queries='actual native research levels/colour and percentage text; next-mission number and message token; no query body translated',
        capture_sha256=sha(cap.raw),sources_sha256={name:sha((AQUI/name).read_bytes()) for name in
            ('telas_inicializacao_s1.py','validar_inicializacao_telas_s1.py')},rows=rows)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--capture',default=str(AQUI/'evidencias/s1-dependencias-nativas.json.xz'))
    p.add_argument('--output',required=True);a=p.parse_args();d=validar(a.capture)
    Path(a.output).write_text(json.dumps(d,indent=1)+'\n');print(d['equal'],'/',d['cases'],'MenuInit surfaces;0 mismatches')
