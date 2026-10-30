"""Original-first research/result-screen S1 calls, frames 17001..17044.

--capturar imports no game translation. Captures are immutable. The default
mode reruns the identical native segment and compares tecnologia_economia_s1.
Every frame must equal Missions' replay-checked S1 record. 19-minute bound.
"""
import argparse
import json
import lzma
from pathlib import Path
import signal
import subprocess
import time

import sondar_lacunas_economia_s1 as base

PASTA, RAIZ = base.PASTA, base.RAIZ
ROTINAS = ('RechercheCalculNew', 'InventionSetEffet', 'TypeBatimentEstRealisable', 'TypeEnginEstRealisable',
           'BatimentInitTechnologie', 'EnginSetTechnologie', 'SetBatimentRecrutable', 'SetTroupeRecrutable',
           'RechercheGetBranche', 'RechercheGetNiveau', 'BonusReset', 'IaRechercheAjuste', 'InventionGetCout',
           'RechercheGetEtat', 'RechercheGetNbInvention', 'SortilegeResetTechnologie', 'TechnologieReset')
CAPTURA = PASTA/'evidencias/lacunas-s1/captura-tecnologia.json.xz'


class ObservacaoTecnologia(base.bs.Observacao):
    """Prearmed observers only: never flush the active native TB at a nested CALL.

    Adding/removing the leaf recorder hooks in a running native block can
    reexecute stack operations under Unicorn. All hooks here exist before
    emulation starts; opening/closing a scope only changes Python bookkeeping.
    """
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        import unicorn
        from emulador import PILHA
        from bancada_ordens_economia import _gravador
        self._pilha=(PILHA,PILHA+0x10000)
        self._fabrica=_gravador
        def ler(cpu,acesso,a,n,v,_):
            if self.ativo:
                for c in self.abertos:c['recorder']._ler(cpu,acesso,a,n,v,None)
        def escrever(cpu,acesso,a,n,v,_):
            if self.ativo:
                for c in self.abertos:c['recorder']._escrever(cpu,acesso,a,n,v,None)
        def bloco(cpu,a,n,_):
            if self.ativo:
                for c in self.abertos:c['recorder']._bloco(cpu,a,n,None)
        for tipo,callback in ((unicorn.UC_HOOK_MEM_READ,ler),(unicorn.UC_HOOK_MEM_WRITE,escrever),
                              (unicorn.UC_HOOK_BLOCK,bloco)):
            self._ganchos.append(self.b.cpu.hook_add(tipo,callback))
        self.b.cpu.ctl_flush_tb()

    def _entrada(self,nome):
        n=len(self.abertos)
        super()._entrada(nome)
        if len(self.abertos)>n:
            c=self.abertos[-1]
            g=self._fabrica(self.b,(),self._pilha,True)
            g.escritas,g.chamadas,g.abertas,g.ultimo=[],[],[],None
            g.lidos,g.escritos={},set()
            g.esp_inicial=c['regs']['ESP']
            c['recorder']=g

    def _retorno(self,endereco):
        if self.ativo and self.abertos:
            c=self.abertos[-1]
            if c['retorno']==endereco and self._regs()['ESP']==c['regs']['ESP']+4:
                g=c['recorder']
                if g.abertas:raise RuntimeError('Unclosed native calls')
                self.extra=dict(read_before_write=g.leituras_em_runs(),stores=g.escritas,calls=g.chamadas)
        super()._retorno(endereco)


def main():
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    signal.alarm(1140)
    ap = argparse.ArgumentParser()
    ap.add_argument('--capturar', action='store_true')
    a = ap.parse_args()
    if a.capturar and CAPTURA.exists():
        raise FileExistsError(CAPTURA)
    ref = None if a.capturar else json.loads(lzma.decompress(CAPTURA.read_bytes()))
    base.GRUPOS['tecnologia'] = (17000, 17044, ROTINAS)
    base.ObservacaoEconomia = ObservacaoTecnologia
    comparar = None
    if not a.capturar:
        from replay_tecnologia_economia_s1 import comparar
    ex = base.Execucao('tecnologia', comparar)
    segundos = ex.executar()
    resumo, falhas = {}, []
    for i,c in enumerate(ex.casos):
        p = resumo.setdefault(c['routine'], dict(cases=0,mismatches=0))
        p['cases'] += 1
        if ref is not None:
            r = c['comparison']
            r['native_equals_capture'] = i<len(ref['cases']) and ref['cases'][i]=={k:v for k,v in c.items() if k!='comparison'}
            r['ok'] &= r['native_equals_capture']
            if not r['ok']:
                p['mismatches'] += 1
                falhas.append(dict(index=i,routine=c['routine'],comparison=r))
    dados = dict(original_sha256=HASH_ORIGINAL,translation_executed=not a.capturar,
                 source_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=RAIZ,text=True).strip(),
                 reproduction=ex.bancada.reproducao(),seconds=segundos,by_routine=resumo,cases=ex.casos)
    if a.capturar:
        dados['capture_sources'] = {p:base.hash_arquivo(PASTA/p) for p in
                                   ('sondar_tecnologia_economia_s1.py','sondar_lacunas_economia_s1.py')}
        CAPTURA.parent.mkdir(parents=True, exist_ok=True)
        CAPTURA.write_bytes(lzma.compress((json.dumps(dados,sort_keys=True)+'\n').encode()))
        saida = CAPTURA
    else:
        dados.update(comparisons=len(ex.casos),mismatches=falhas,capture_sha256=base.hash_arquivo(CAPTURA),
                     rerun_equals_capture=len(ex.casos)==len(ref['cases']) and
                        all(c['comparison']['native_equals_capture'] for c in ex.casos),
                     source_sha256={str((PASTA/p).relative_to(RAIZ)):base.hash_arquivo(PASTA/p) for p in
                                    ('sondar_tecnologia_economia_s1.py','sondar_lacunas_economia_s1.py',
                                     'tecnologia_economia_s1.py','replay_tecnologia_economia_s1.py')})
        saida = PASTA/'validacao-tecnologia-s1-emulada.json'
        if falhas:
            saida = RAIZ/'.local/tecnologia-s1-falha.json'
        saida.write_text(json.dumps(dados,indent=1,sort_keys=True)+'\n')
    print(json.dumps(dict(output=str(saida),by_routine=resumo,seconds=segundos,mismatches=len(falhas)),indent=1),flush=True)
    encerrar_captura(2 if falhas else 0,saida)


if __name__=='__main__':
    main()
