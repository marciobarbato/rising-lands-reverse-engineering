"""Original-only S1 TuyauEstSortie call sites + restored type/count/enable variants.

Capture first (--capturar); default mode reruns natively and compares the strict
provider over only the original's read-before-write bytes. 19-minute bound.
"""
import argparse
import json
import lzma
import signal
import struct
import subprocess

import sondar_lacunas_economia_s1 as base

PASTA, RAIZ = base.PASTA, base.RAIZ
CAPTURA = PASTA/'evidencias/lacunas-s1/captura-tuyau.json.xz'


def variantes(grupo, r, blocos):
    est = 0x49a0c8 + 276*(r['EAX'] & 0xffff)
    for n in range(256):
        yield f'counter +0x76 {n}', dict(r,EAX=r['EAX']|0xabcd0000), [(est+0x76,bytes([n]))]
    for n in (0,1,2,128,255):
        yield f'enable +0x75 {n}', r, [(est+0x75,bytes([n])),(est+0x76,b'\x0f')]
    for i in (0,999):
        for compteur,actif in ((15,1),(15,0),(14,255),(16,255)):
            regs = dict(zip(base.REG7,(0xabcd0000|i,0x01234567,0x89abcdef,0xfedcba98,
                                      0x12345678,0x87654321,0x98765432)))
            yield f'structure {i}, counter {compteur}, enabled {actif}',regs,[
                (0x49a0c8+276*i+0x75,bytes([actif,compteur]))]


def comparar(c, blocos=None):
    from tuyau_economia_s1 import TuyauEconomiaS1, provedor_tuyau_economia_s1
    from replay_ciclo_trabalho import MemoriaEsparsa
    regs = {k:int(v,16) for k,v in c['entry_registers'].items()}
    regs['ESP'] = int(c['esp'],16)
    m = MemoriaEsparsa(c['read_before_write'])
    t = TuyauEconomiaS1(m)
    saida = t.chamar(c['routine'],regs)
    provider = provedor_tuyau_economia_s1(t)(c['routine'],0,regs)
    dif = {k:[hex(saida[k]),v] for k,v in c['exit_registers'].items() if saida[k]!=int(v,16)}
    ok = not dif and not m.escritos and not c['changed_bytes'] and not c['stores']
    return dict(ok=ok and all(provider[k]==saida[k] for k in base.REG7),register_differences=dif)


def main():
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    signal.alarm(1140)
    ap=argparse.ArgumentParser();ap.add_argument('--capturar',action='store_true');a=ap.parse_args()
    if a.capturar and CAPTURA.exists():
        raise FileExistsError(CAPTURA)
    ref=None if a.capturar else json.loads(lzma.decompress(CAPTURA.read_bytes()))
    base.variantes=variantes
    ex=base.Execucao('tuyau',None if a.capturar else comparar)
    segundos=ex.executar()
    falhas=[]
    if ref is not None:
        for i,c in enumerate(ex.casos):
            cmp=c['comparison'];cmp['native_equals_capture']=i<len(ref['cases']) and ref['cases'][i]=={k:v for k,v in c.items() if k!='comparison'}
            cmp['ok'] &= cmp['native_equals_capture']
            if not cmp['ok']:falhas.append(dict(index=i,comparison=cmp))
    dados=dict(original_sha256=HASH_ORIGINAL,translation_executed=not a.capturar,seconds=segundos,
               source_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=RAIZ,text=True).strip(),
               reproduction=ex.bancada.reproducao(),cases=ex.casos)
    if a.capturar:
        dados['capture_sources']={p:base.hash_arquivo(PASTA/p) for p in ('sondar_tuyau_economia_s1.py','sondar_lacunas_economia_s1.py')}
        CAPTURA.write_bytes(lzma.compress((json.dumps(dados,sort_keys=True)+'\n').encode()))
        saida=CAPTURA
    else:
        dados.update(comparisons=len(ex.casos),mismatches=falhas,rerun_equals_capture=len(ex.casos)==len(ref['cases']) and all(c['comparison']['native_equals_capture'] for c in ex.casos),
                     capture_sha256=base.hash_arquivo(CAPTURA),by_routine={'TuyauEstSortie':dict(cases=len(ex.casos),mismatches=len(falhas))},
                     source_sha256={str((PASTA/p).relative_to(RAIZ)):base.hash_arquivo(PASTA/p) for p in ('sondar_tuyau_economia_s1.py','sondar_lacunas_economia_s1.py','tuyau_economia_s1.py','lacunas_economia_s1.py')})
        saida=PASTA/'validacao-tuyau-s1-emulada.json' if not falhas else RAIZ/'.local/tuyau-s1-falha.json'
        saida.write_text(json.dumps(dados,indent=1,sort_keys=True)+'\n')
    print(dict(output=str(saida),cases=len(ex.casos),mismatches=len(falhas),seconds=segundos),flush=True)
    encerrar_captura(2 if falhas else 0,saida)


if __name__=='__main__':main()
