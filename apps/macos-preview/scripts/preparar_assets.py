"""Extrai somente por leitura; usa leitores do snapshot e verifica hashes do CD."""
import hashlib, json, struct, sys, zlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def png(path, w, h, rgba):
    def chunk(kind, data):
        return struct.pack('>I', len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))
    raw=b''.join(b'\0'+rgba[y*w*4:(y+1)*w*4] for y in range(h))
    path.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b''))

def main():
    manifest=json.loads((ROOT/'snapshot.json').read_text()); snap=ROOT/manifest['snapshot']
    sys.path.insert(0,str(snap/'ferramentas'))
    from formatos import ler_cmp, ler_eta, ler_paleta
    cd=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parents[2]/'source/cd'
    known={f['arquivo']:f['sha256'] for f in json.loads((snap/'relatorios/fontes.json').read_text())}
    used=[]
    def read(name):
        data=(cd/name).read_bytes(); sha=hashlib.sha256(data).hexdigest()
        if known.get(name)!=sha: raise ValueError('Hash original diferente do snapshot: '+name)
        used.append({'source':str(cd/name),'path':name,'sha256':sha,'bytes':len(data)})
        return data
    pal=ler_paleta(read('INSTALHD/PLATGAME.PIE'))
    out=ROOT/'assets'; out.mkdir(exist_ok=True)
    metadata={}
    for name, output, limit in [('BLOCS','terreno',None),('TROOPS','tropas',128)]:
        frames=ler_cmp(read('INSTALHD/GRAPHICS/'+name+'.CMP'))
        if limit:frames=frames[:limit]
        cell=32 if name=='BLOCS' else 96; cols=32 if name=='BLOCS' else 16
        w=cols*cell; h=((len(frames)+cols-1)//cols)*cell; rgba=bytearray(w*h*4); items=[]
        for idx,f in enumerate(frames):
            if f.largura>cell or f.altura>cell: raise ValueError('Quadro maior que atlas')
            x=(idx%cols)*cell; y=(idx//cols)*cell
            for yy in range(f.altura):
                for xx in range(f.largura):
                    c=f.pixels[yy*f.largura+xx]; d=((y+yy)*w+x+xx)*4
                    rgba[d:d+4]=pal[c*3:c*3+3]+bytes([255 if c else 0])
            items.append({'index':idx,'x':x,'y':y,'w':f.largura,'h':f.altura})
        png(out/(output+'.png'),w,h,rgba);metadata[output]={'cols':cols,'cell':cell,'frames':items}
    m=ler_eta(read('WORLD/MONDE01.ETA'))
    scene={k:m[k] for k in ('largura','altura','terreno','atributos','objetos','variantes','unidades','recursos_por_tipo')}
    (out/'missao01.json').write_text(json.dumps(scene,ensure_ascii=False,separators=(',',':')))
    (out/'atlas.json').write_text(json.dumps(metadata,separators=(',',':')))
    (out/'fontes.json').write_text(json.dumps({'commit':manifest['commit'],'sources':used,'outputs':[{'path':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(out.iterdir()) if p.name!='fontes.json']},ensure_ascii=False,indent=2)+'\n')
    print('Assets originais verificados e extraídos:',len(used),'fontes;',m['largura'],'×',m['altura'])
if __name__=='__main__': main()
