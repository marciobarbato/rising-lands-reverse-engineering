"""Record original full-producer placement composition and shared raw pointers."""
import hashlib
import json
from pathlib import Path
import sys

PASTA=Path(__file__).resolve().parent
RAIZ=PASTA.parents[1]
sys.path.insert(0,str(RAIZ.parent/'source/python'))
import capstone
import pefile
from capturar_saida_tropa import HASH


def main():
    dados=(RAIZ.parent/'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(dados).hexdigest()!=HASH:raise ValueError('Original executable hash mismatch')
    pe=pefile.PE(data=dados)
    imagem,base=pe.get_memory_mapped_image(),pe.OPTIONAL_HEADER.ImageBase
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
    captures=[]
    for a,z,n in ((0x420f8a,0x420f9e,'Original placement and live-destination movement caller'),
                  (0x475736,0x475763,'Terrain paired raw-byte pointer consumers'),
                  (0x47610f,0x476134,'Movement raw-object query'),
                  (0x476662,0x4766f0,'Resource-removal pointer context')):
        codigo=imagem[a-base:z-base]
        arquivo=f'producao-colocada-{a:08x}.asm'
        linhas=[f'; {n}; exclusive end0x{z:x}.',f'; Original EXE SHA-256:{HASH}',
                '; Context evidence; this composition does not invoke every resource-removal branch.']
        linhas += [f'{i.address:08x}  {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}'.rstrip()
                   for i in md.disasm(codigo,a)]
        (PASTA/'evidencias'/arquivo).write_text('\n'.join(linhas)+'\n')
        captures.append(dict(start=hex(a),end_exclusive=hex(z),description=n,bytes_hex=codigo.hex(),
                             sha256=hashlib.sha256(codigo).hexdigest(),listing=arquivo))
    refs=[]
    for rel in ('evidencias/producao-experiente.json','../../evidencias/colocacao-saida/manifesto.json'):
        p=PASTA/rel
        refs.append(dict(path=rel,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    r=dict(sha256_exe=HASH,sha256_sbl='c3a5411255847d36161aea1aeef06ab280265c55fa5a6626cfeb7bab523cc627',
           scope='Actual CalculTroupe through economy, conversion/recovery/experience, physical exit/order; before request',
           placement_implementation='6b3882b5b4a3a0c99dddcaccbd4d1c08a765f8ce',
           placement_main='aa9cba47af34aef3b0b4b67faded0b884bb1e428',captures=captures,committed_evidence=refs,
           raw_aliases={'0x507d74':'economic terreno.tipos IS physical objetos',
                        '0x507dac':'economic terreno.quantidades IS physical donos_objetos'},
           native_entry='0x4259e6',pending='0x420f9e',
           native_execution='Actual core harness preserves registers/flags/stack at declared minimap entry pauses; no call/ret replacement')
    (PASTA/'evidencias/producao-colocada.json').write_text(json.dumps(r,indent=2)+'\n')
    print('Captured caller/raw pointer evidence and committed placement identities.')


if __name__=='__main__':main()
