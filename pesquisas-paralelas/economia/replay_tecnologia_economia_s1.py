"""Exact sparse replay of the original-first S1 research/technology capture.

Foreign read-only MissionGetNum/PlayerGetType calls are the original's own
recorded calls, with arguments checked in sequence and exact exit registers.
All Economy bodies and memory writes run in Python, including nested resets,
unlocks, technology Bags and level stores. No unknown return is synthesized.
"""
import json
import lzma
from pathlib import Path

from replay_ciclo_trabalho import MemoriaEsparsa
from tecnologia_economia_s1 import REG7,M32,TecnologiaEconomiaS1,provedor_tecnologia_economia_s1

PASTA=Path(__file__).resolve().parent
CAPTURA=PASTA/'evidencias/lacunas-s1/captura-tecnologia.json.xz'
EXTERNAS=frozenset(('MissionGetNum','PlayerGetType'))


class MemoriaGravada(MemoriaEsparsa):
    def __init__(self,runs):
        super().__init__(runs);self.lojas=[]

    def _acesso(self,n,a,valor):
        if valor is not None:self.lojas.append((a,n,valor&((1<<(8*n))-1)))
        return super()._acesso(n,a,valor)


class Replay:
    def __init__(self,c):
        self.lista=[x for x in c['calls'] if x[1] in EXTERNAS]
        self.pos=0;self.erros=[]

    def __call__(self,nome,chamada,regs):
        if any(k not in regs for k in REG7):raise AssertionError('Callback omitted a general register')
        if self.pos>=len(self.lista):raise AssertionError(f'Extra foreign call {nome} at {chamada:#x}')
        c=self.lista[self.pos];self.pos+=1
        dif={k:[hex(regs[k]),v] for k,v in c[2].items() if regs[k]!=int(v,16)}
        if c[1]!=nome or dif:
            self.erros.append(dict(index=self.pos-1,python=nome,native=c[1],registers=dif,call=hex(chamada)))
            raise AssertionError(self.erros[-1])
        if len(c)!=6:raise AssertionError('Native callback did not return')
        return {k:int(v,16) for k,v in c[5].items()}


def comparar(caso,blocos=None):
    entrada={k:int(v,16) for k,v in caso['entry_registers'].items()};entrada['ESP']=int(caso['esp'],16)
    native={k:int(v,16) for k,v in caso['exit_registers'].items()}
    try:
        m=MemoriaGravada(caso['read_before_write']);rp=Replay(caso)
        t=TecnologiaEconomiaS1(m,externo=rp)
        saida=t.chamar(caso['routine'],entrada)
        dif={k:[hex(saida[k]),hex(v)] for k,v in native.items() if saida[k]!=v}
        esperado=[(int(s[2],16),s[3],int(s[4],16)) for s in caso['stores']]
        stores_equal=m.lojas==esperado
        finais={}
        for a,n,v in esperado:
            for i in range(n):finais[a+i]=v>>(8*i)&255
        bad_stores=[hex(a) for a,v in m.escritos.items() if finais.get(a,m.bytes.get(a))!=v]
        changed=[hex(int(a,16)) for a,_,v in caso['changed_bytes'] if m.escritos.get(int(a,16),m.bytes.get(int(a,16)))!=v]
        all_calls=rp.pos==len(rp.lista)
        pm=MemoriaGravada(caso['read_before_write']);prp=Replay(caso)
        pt=TecnologiaEconomiaS1(pm,externo=prp)
        servida=provedor_tecnologia_economia_s1(pt)(caso['routine'],0,entrada)
        provider_equal=all(servida[k]==native[k] for k in REG7) and pm.lojas==m.lojas and prp.pos==len(prp.lista)
        ok=not dif and not bad_stores and not changed and stores_equal and all_calls and provider_equal
        r=dict(ok=ok,register_differences=dif,ordered_stores_equal=stores_equal,changed_equal=not changed,
               stored_values_equal=not bad_stores,foreign_calls=rp.pos,all_calls_consumed=all_calls,provider_equal=provider_equal)
        if bad_stores:r['wrong_stored_bytes']=bad_stores[:16]
        if changed:r['wrong_changed_bytes']=changed[:16]
        if not stores_equal:
            r['python_store_count'],r['native_store_count']=len(m.lojas),len(esperado)
            r['first_different_store']=next(([i,a,b] for i,(a,b) in enumerate(zip(m.lojas,esperado)) if a!=b),None)
        return r
    except Exception as e:
        return dict(ok=False,error=f'{type(e).__name__}: {e}')


def replay():
    cap=json.loads(lzma.decompress(CAPTURA.read_bytes()));counts={};falhas=[]
    for i,c in enumerate(cap['cases']):
        r=comparar(c);n=counts.setdefault(c['routine'],dict(cases=0,mismatches=0));n['cases']+=1
        if not r['ok']:n['mismatches']+=1;falhas.append(dict(index=i,routine=c['routine'],**r))
    return counts,falhas


if __name__=='__main__':
    counts,bad=replay();print(json.dumps(dict(by_routine=counts,mismatches=bad[:20]),indent=1))
    raise SystemExit(bool(bad))
