"""Original-only economy research/type leaf captures, before translation.

No reconstructed owner or AI routine is imported. Use only when the
coordinator explicitly grants the native slot; no game query body is imported.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import sys
import subprocess

RAIZ = Path(__file__).resolve().parents[2]
LIMITES = ((0x4717c2, 0x4717de), (0x470b37, 0x470b46),
           (0x41a08c, 0x41a0ab), (0x41a4f4, 0x41a513))
PADRAO_REGS = dict(EBX=0x13579bdf, ECX=0x2468ace0, ESI=0xa1b2c3d4,
                   EDI=0x91827364, EBP=0x19283746)


def capturar(destino):
    destino = Path(destino)
    if destino.exists():raise FileExistsError('Preserve existing capture; choose a new output')
    # Imports and CPU construction happen only in this explicitly run entry.
    sys.path.insert(0, str(RAIZ/'ferramentas'))
    from emulador import BancadaX86, RETORNO, unicorn
    from casos_consultas_reinicio_economia import cenarios, PESQUISA, ESTRUTURAS
    b = BancadaX86()
    escritas = []
    faixas = ((PESQUISA-16, PESQUISA+64+16), (ESTRUTURAS-16, ESTRUTURAS+276000+16))
    def observar(cpu, acesso, endereco, tamanho, valor, dados):
        if any(a <= endereco < z for a,z in faixas):
            escritas.append(dict(endereco=hex(endereco), tamanho=tamanho, valor=valor))
    b.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, observar)
    def estado():
        return dict(pesquisa=bytes(b.cpu.mem_read(PESQUISA,64)).hex(),
                    estruturas_sha256=hashlib.sha256(bytes(b.cpu.mem_read(ESTRUTURAS,276000))).hexdigest(),
                    guardas=[bytes(b.cpu.mem_read(a,n)).hex() for a,n in
                             ((PESQUISA-16,16),(PESQUISA+64,16),(ESTRUTURAS-16,16),(ESTRUTURAS+276000,16))])
    resultados = []
    for caso in cenarios():
        b.cpu.mem_write(PESQUISA-16,b'\xa6'*16+caso['pesquisa']+b'\x6a'*16)
        b.cpu.mem_write(ESTRUTURAS-16,b'\xc7'*16+caso['estruturas']+b'\x7c'*16)
        inicial = estado()
        chamadas = []
        for c in caso['chamadas']:
            escritas.clear()
            regs = b.executar(c['entrada'],list(LIMITES),dict(PADRAO_REGS,**c['regs']))
            assert regs['EIP'] == RETORNO
            chamadas.append(dict(entrada=hex(c['entrada']),entrada_regs=c['regs'],
                                 saida_regs=regs,escritas=list(escritas),estado=estado()))
        resultados.append(dict(nome=caso['nome'],inicial=inicial,chamadas=chamadas))
    assert len(resultados)==14 and b.execucoes==20
    arquivos = [Path(__file__), Path(__file__).with_name('casos_consultas_reinicio_economia.py'), RAIZ/'ferramentas/emulador.py', Path(__file__).parent/'evidencias/contratos-economia-iareset-auditoria.json']
    origem = [dict(path=str(p.relative_to(RAIZ)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in arquivos]
    commit = subprocess.check_output(['git','-C',str(RAIZ),'rev-parse','HEAD'],text=True).strip()
    saida = dict(source_commit=commit, source_files=origem, captured_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 allowed_original_intervals=[[hex(a),hex(b)] for a,b in LIMITES],
                 scope='Original-only owner-leaf captures; no translation executed',
                 translation_executed=False,sha256_exe='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
                 scenarios=14,original_entries=b.execucoes,bounded_segments=b.execucoes,
                 captures=resultados)
    destino.write_text(json.dumps(saida,indent=2)+'\n')
    print('Captured original-only:14 scenarios,20 entries,20 real returns; translation_executed=False.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',required=True)
    capturar(p.parse_args().output)
