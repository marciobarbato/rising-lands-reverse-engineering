"""Add caller/queue provider identities for the new full production prefix."""
import hashlib
import json
from pathlib import Path
import sys

PASTA=Path(__file__).resolve().parent
RAIZ=PASTA.parents[1]
sys.path.insert(0,str(RAIZ.parent/'source/python'))
import pefile
import capstone
from capturar_saida_tropa import HASH


def main():
    dados=(RAIZ.parent/'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(dados).hexdigest()!=HASH:
        raise ValueError('Original executable hash mismatch')
    pe=pefile.PE(data=dados)
    inicio,fim=0x420f81,0x420f8a
    codigo=pe.get_memory_mapped_image()[inicio-pe.OPTIONAL_HEADER.ImageBase:fim-pe.OPTIONAL_HEADER.ImageBase]
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
    arquivo='producao-experiente-00420f81.asm'
    linhas=[f'; Original caller through experience, exclusive end0x{fim:x}.',f'; Original EXE SHA-256:{HASH}']
    linhas += [f'{i.address:08x}  {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}'.rstrip()
               for i in md.disasm(codigo,inicio)]
    (PASTA/'evidencias'/arquivo).write_text('\n'.join(linhas)+'\n')
    refs=[]
    for relativo in ('evidencias/producao-compartilhada.json','../../evidencias/experiencia-unidades/manifesto.json'):
        p=PASTA/relativo
        refs.append(dict(path=relativo,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    r=dict(sha256_exe=HASH,sha256_sbl='c3a5411255847d36161aea1aeef06ab280265c55fa5a6626cfeb7bab523cc627',
           scope='Actual CalculTroupe through preparation/conversion/recovery/experience; no placement',
           core_experience_implementation='f67898b75423adcfaf90a7b6e6c710c409e6f9ee',
           core_experience_main='dae42125f45c348c10dff7e727e803138be7670f',
           captures=[dict(start=hex(inicio),end_exclusive=hex(fim),bytes_hex=codigo.hex(),
                          sha256=hashlib.sha256(codigo).hexdigest(),listing=arquivo)],
           committed_evidence=refs,queue=dict(address='0x4e19c4',size=40,domain='four owners; supplied raw state'),
           pending_address='0x420f8a')
    (PASTA/'evidencias/producao-experiente.json').write_text(json.dumps(r,indent=2)+'\n')
    print('Captured experience caller and committed evidence identities.')


if __name__=='__main__':
    main()
