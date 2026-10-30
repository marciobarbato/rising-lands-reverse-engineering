"""Full native S1 objectives buffers, glyph arguments and clip effects against the independent compositor."""
import argparse,base64,hashlib,json,lzma,zlib
from pathlib import Path
from graficos import Catalogo
from telas_objetivos_s1 import compor_objetivos_s1

AQUI=Path(__file__).resolve().parent
sha=lambda raw:hashlib.sha256(raw).hexdigest()

class CapturaTelaS1:
    def __init__(self,path):
        self.raw=Path(path).read_bytes();self.d=json.loads(lzma.decompress(self.raw));self.cache={}
    def blob(self,key):
        if key not in self.cache:
            raw=zlib.decompress(base64.b64decode(self.d['blobs'][key]));assert sha(raw)==key;self.cache[key]=raw
        return self.cache[key]
    def memory(self,row,side='entry'):
        blocks=[(int(a,16),self.blob(key)) for a,key in row[side+'_inputs']['regions'].values()]
        return MemoriaTelaS1(blocks)

class MemoriaTelaS1:
    def __init__(self,blocks):self.blocks=blocks
    def ler_mundo(self,a,n):
        for base,raw in self.blocks:
            if base<=a and a+n<=base+len(raw):return raw[a-base:a-base+n]
        raise KeyError(('Undeclared screen input',hex(a),n))
    def u8(self,a):return self.ler_mundo(a,1)[0]
    def u16(self,a):return int.from_bytes(self.ler_mundo(a,2),'little')
    def u32(self,a):return int.from_bytes(self.ler_mundo(a,4),'little')

def validar(path):
    cap=CapturaTelaS1(path);catalog=Catalogo();rows=[]
    for row in cap.d['rows']:
        if row['routine']!='AffObjectif':continue
        assert row['returned'] and row['surface_equal'] and row['whole_state_equal'] and row['raster_arguments_equal']
        m=cap.memory(row);before=m.ler_mundo(0x494000,0x8f000)
        out=compor_objetivos_s1(m,cap.blob(row['before']),catalogo=catalog)
        expected=cap.blob(row['after']);pixels=sum(a!=b for a,b in zip(out['pixels'],expected))
        assert len(out['pixels'])==480000
        args=out['chamadas']!=row['blits'];projected=bytearray(before)
        for name,address,old,new in out['efeitos']:
            raw=bytes.fromhex(new);assert projected[address-0x494000:address-0x494000+len(raw)]==bytes.fromhex(old)
            projected[address-0x494000:address-0x494000+len(raw)]=raw
        dg=cap.memory(row,'exit').ler_mundo(0x494000,0x8f000)
        changes=[hex(0x494000+i) for i,(a,b) in enumerate(zip(projected,dg)) if a!=b]
        assert not(pixels or args or changes),(row['frame'],pixels,args,changes)
        assert m.ler_mundo(0x494000,0x8f000)==before
        rows.append(dict(frame=row['frame'],equal=True,pixel_mismatches=pixels,argument_mismatches=int(args),
            dgroup_mismatches=changes,drawing_calls=len(out['chamadas']),sha256=sha(out['pixels'])))
    assert len(rows)==7
    return dict(schema='rising-lands/s1-objectives-comparison/1',cases=len(rows),equal=len(rows),mismatches=0,
        boundary_contract='AffObjectif executes real font1 glyphs; no AffText, LoadPie or text callback in these calls',
        capture_sha256=sha(cap.raw),sources_sha256={name:sha((AQUI/name).read_bytes()) for name in
            ('texto_bitmap_nativo.py','telas_objetivos_s1.py','validar_objetivos_s1.py')},rows=rows)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--capture',default=str(AQUI/'evidencias/s1-telas-finais-nativas.json.xz'))
    p.add_argument('--output',required=True);a=p.parse_args();d=validar(a.capture)
    Path(a.output).write_text(json.dumps(d,indent=1)+'\n');print(d['equal'],'/',d['cases'],'objectives screens;0 mismatches')
