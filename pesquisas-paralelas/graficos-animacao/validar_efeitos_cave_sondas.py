"""Current logic-effect domain against native P3/P6/P7 images and the reported input-origin stops."""
import hashlib,json,struct
from pathlib import Path
from validar_janelas_api18 import CapturaLimitada,AQUI,PARTS
from efeitos_logicos_exibicao import desenhar_jogo,_guardas_estruturas,DependenciaExibicao

class EntradaEfeitos:
    def __init__(self,cap,row):
        self.dg=cap.blob(row['entry']['dgroup'][1]);a,key=row['entry']['projectiles'];self.pb=int(a,16);self.proj=cap.blob(key)
    def raw(self,a,n):
        if 0x494000<=a and a+n<=0x523000:return self.dg[a-0x494000:a-0x494000+n]
        if self.pb<=a and a+n<=self.pb+len(self.proj):return self.proj[a-self.pb:a-self.pb+n]
        raise KeyError((hex(a),n))
    def u8(self,a):
        if 0x494000<=a<0x523000:return self.dg[a-0x494000]
        return self.raw(a,1)[0]
    def u16(self,a):return int.from_bytes(self.raw(a,2),'little')
    def u32(self,a):return int.from_bytes(self.raw(a,4),'little')

def validar():
    counts={};prefix={};pins={};domains=set();next_stops={}
    for probe in ('P3','P6','P7'):
        count=0
        if probe=='P6':
            count=prefix['P3-2000']
            if 'P3' in next_stops and next_stops['P3']['frame']<=2000:next_stops[probe]=dict(next_stops['P3'])
        if probe=='P7':
            count=counts['P6']
            if 'P6' in next_stops:next_stops[probe]=dict(next_stops['P6'])
        for filename in PARTS[probe]:
            path=AQUI/'evidencias'/filename;cap=CapturaLimitada(path);pins[filename]=cap.sha
            for row in cap.d['rows']:
                memory=EntradaEfeitos(cap,row)
                _guardas_estruturas(memory,'AffGame',[],habitado=lambda i:True)
                try:
                    result=desenhar_jogo(memory,habitado=lambda i:True)
                    if result.escritas:raise AssertionError((probe,row['frame'],result.escritas))
                except DependenciaExibicao as stop:
                    next_stops.setdefault(probe,dict(frame=row['frame'],address=hex(stop.sitio),reason=stop.motivo))
                count+=1
                states=tuple((i,memory.u8(0x49a0c8+276*i+8),memory.u8(0x49a0c8+276*i+5),memory.u8(0x49a0c8+276*i+4)) for i in range(2))
                domains.add(states)
                if probe=='P3' and row['frame']==2000:prefix['P3-2000']=count
        counts[probe]=count
    origin_rows=[]
    for probe,filename,frame,expected in (
        ('K1','janela-K1-129-629-api18.json.xz',141,(1,0)),
        ('P4','sonda-colheita-P4-129-728.json.xz',422,(10,16)),
        ('P5','sonda-colheita-P5-129-728.json.xz',572,(31,0))):
        cap=CapturaLimitada(AQUI/'evidencias'/filename);row=next(r for r in cap.d['rows'] if r['frame']==frame);m=EntradaEfeitos(cap,row)
        origin=(m.u16(0x508720),m.u16(0x508722));assert origin==expected
        assert desenhar_jogo(m).escritas==();origin_rows.append(dict(probe=probe,frame=frame,origin=list(origin),passed=True))
    return dict(schema='rising-lands/cave-logic-domain-comparison/1',probes=counts,mismatches=0,next_unrelated_stops=next_stops,origins=origin_rows,
        domains=sorted(domains),capture_pins=pins,provider_sha256=hashlib.sha256((AQUI/'efeitos_logicos_exibicao.py').read_bytes()).hexdigest())

if __name__=='__main__':
    result=validar();(AQUI/'validacao/cave-dominio-atual.json').write_text(json.dumps(result,indent=1)+'\n');print(result['probes'],result['mismatches'],flush=True)
