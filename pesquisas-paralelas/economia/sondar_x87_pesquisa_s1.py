"""Original-only x87 attestation for RechercheGetEtat at the S1 result screen.

The generic seven-register observer cannot attest a floating result. This
additive capture records FP0..FP7/FPSW before and after the real getter, then
restored finite-double variants from that S1 state. No translation imported.
"""
import json
import argparse
import lzma
from pathlib import Path
import signal
import struct
import subprocess

import sondar_lacunas_economia_s1 as base
import bancada_s1 as bs

PASTA, RAIZ = base.PASTA, base.RAIZ
CAPTURA = PASTA/'evidencias/lacunas-s1/captura-recherche-get-etat-x87.json.xz'


def fp(b):
    from unicorn import x86_const as x
    return {k:b.cpu.reg_read(getattr(x,'UC_X86_REG_'+k)) for k in
            ('FPCW','FPSW','FPTAG')+tuple(f'FP{i}' for i in range(8))}


class Observacao(base.ObservacaoEconomia):
    def _entrada(self,nome):
        n=len(self.abertos)
        super()._entrada(nome)
        if len(self.abertos)>n:self.abertos[-1]['fp_before']=fp(self.b)

    def _retorno(self,endereco):
        if self.abertos:
            c=self.abertos[-1]
            if c['retorno']==endereco and self._regs()['ESP']==c['regs']['ESP']+4:
                self.fp_before=c['fp_before'];self.fp_after=fp(self.b)
        super()._retorno(endereco)


def main():
    from emulador import HASH_ORIGINAL,RETORNO
    from encerramento_captura import encerrar_captura
    from unicorn import x86_const as x
    import unicorn
    signal.alarm(1140)
    ap=argparse.ArgumentParser();ap.add_argument('--validar',action='store_true');args=ap.parse_args()
    if CAPTURA.exists() and not args.validar:raise FileExistsError(CAPTURA)
    bancada=bs.BancadaS1(17000);b=bancada.b
    casos=[];pendentes=[]
    def fechar(c,blocos):
        c.update(obs.extra,x87_before=obs.fp_before,x87_after=obs.fp_after)
        casos.append(c);pendentes.append((c,blocos,b.cpu.context_save()))
    obs=Observacao(b,{'RechercheGetEtat':0},ao_fechar=fechar)
    while bancada.k<17044:bancada.avancar(obs)
    obs.ativo=False
    atual,contexto=bs.imagem(b),b.cpu.context_save()
    try:
        for c,blocos,ctx in pendentes:
            for valor in (0.0,-0.0,1.0,-1.0,1.5,123456.125,2.0**-1022,2.0**1023):
                bs.restaurar(b,blocos);b.cpu.context_restore(ctx)
                regs={k:int(v,16) for k,v in c['entry_registers'].items()}
                a=0x5080fc+16*(regs['EAX']&255)
                before=fp(b);fim=[]
                def retorno(cpu,address,size,_):fim.append(fp(b))
                # The runner stops before the trampoline executes. Observe the
                # getter's RET instead, after its FLD and before context restore.
                h=b.cpu.hook_add(unicorn.UC_HOOK_CODE,retorno,begin=0x4717b0,end=0x4717b0)
                esp=b.cpu.reg_read(x.UC_X86_REG_ESP)-0x100
                g,hooks=base.gravador(b,esp)
                try:
                    caso,_=bs.folha(b,'RechercheGetEtat',regs,escritas=[(a,struct.pack('<d',valor))],
                                    rotulo=f'finite double {valor!r}',quadro=c['frame'])
                finally:
                    extra=base.finalizar(b,g,hooks);b.cpu.hook_del(h)
                if len(fim)!=1:raise RuntimeError('Missing native x87 return')
                caso.update(extra,x87_before=before,x87_after=fim[0]);casos.append(caso)
    finally:
        bs.restaurar(b,atual);b.cpu.context_restore(contexto);obs.remover()
    dados=dict(original_sha256=HASH_ORIGINAL,translation_executed=False,
               source_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=RAIZ,text=True).strip(),
               source_sha256=base.hash_arquivo(__file__),reproduction=bancada.reproducao(),cases=casos)
    saida=CAPTURA
    falhas=[]
    if args.validar:
        from tecnologia_economia_s1 import TecnologiaEconomiaS1,provedor_tecnologia_economia_s1
        from replay_ciclo_trabalho import MemoriaEsparsa
        ref=json.loads(lzma.decompress(CAPTURA.read_bytes()))
        registros=[]
        for i,c in enumerate(casos):
            m=MemoriaEsparsa(c['read_before_write']);t=TecnologiaEconomiaS1(m)
            regs={k:int(v,16) for k,v in c['entry_registers'].items()};regs['ESP']=int(c['esp'],16)
            r=t.chamar(c['routine'],regs)
            p=provedor_tecnologia_economia_s1(t)(c['routine'],0,regs)
            top=(c['x87_after']['FPSW']>>11)&7
            igual=tuple(c['x87_after'][f'FP{top}'])==r['_x87_push']==p['_x87_push']
            push=top==(((c['x87_before']['FPSW']>>11)-1)&7)
            gerais=all(r[k]==int(v,16) for k,v in c['exit_registers'].items())
            # Unicorn's FP registers are tuples in memory and JSON arrays on
            # disk; compare the canonical JSON representation without masks.
            replay=i<len(ref['cases']) and ref['cases'][i]==json.loads(json.dumps(c))
            ok=igual and push and gerais and replay and not m.escritos and not c['changed_bytes']
            registro=dict(case=i,ok=ok,x87_equal=igual,one_push=push,registers_equal=gerais,native_equals_capture=replay)
            registros.append(registro)
            if not ok:falhas.append(registro)
        dados.update(translation_executed=True,comparisons=len(casos),mismatches=falhas,
                     rerun_equals_capture=len(casos)==len(ref['cases']) and all(r['native_equals_capture'] for r in registros),
                     capture_sha256=base.hash_arquivo(CAPTURA),results=registros,
                     source_sha256={str((PASTA/p).relative_to(RAIZ)):base.hash_arquivo(PASTA/p) for p in
                                    ('sondar_x87_pesquisa_s1.py','tecnologia_economia_s1.py')})
        saida=PASTA/'validacao-recherche-get-etat-x87-emulada.json'
        if falhas:saida=RAIZ/'.local/recherche-get-etat-x87-falha.json'
        saida.write_text(json.dumps(dados,indent=1,sort_keys=True)+'\n')
    else:
        CAPTURA.write_bytes(lzma.compress((json.dumps(dados,sort_keys=True)+'\n').encode()))
    print(dict(output=str(saida),cases=len(casos),mismatches=len(falhas)),flush=True)
    encerrar_captura(2 if falhas else 0,saida)


if __name__=='__main__':main()
