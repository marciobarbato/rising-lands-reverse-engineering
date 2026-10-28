"""Capture original producer request caller and immutable provider provenance."""
import hashlib
import json
from pathlib import Path
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
sys.path.insert(0, str(RAIZ.parent/'source/python'))
import capstone
import pefile
from capturar_saida_tropa import HASH


def main():
    dados = (RAIZ.parent/'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(dados).hexdigest()!=HASH:
        raise ValueError('Original executable hash mismatch')
    pe = pefile.PE(data=dados)
    inicio,fim = 0x420f9e,0x420fb7
    base = pe.OPTIONAL_HEADER.ImageBase
    codigo = pe.get_memory_mapped_image()[inicio-base:fim-base]
    md = capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
    arquivo = 'producao-solicitada-00420f9e.asm'
    linhas = [f'; Original conditional unit request; exclusive end0x{fim:x}.',f'; Original EXE SHA-256:{HASH}']
    linhas += [f'{i.address:08x}  {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}'.rstrip()
               for i in md.disasm(codigo,inicio)]
    (PASTA/'evidencias'/arquivo).write_text('\n'.join(linhas)+'\n')
    refs = []
    for rel in ('evidencias/producao-colocada.json','../../evidencias/voz-unidades/manifesto.json'):
        p = PASTA/rel
        refs.append(dict(path=rel,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    r = dict(sha256_exe=HASH,sha256_sbl='c3a5411255847d36161aea1aeef06ab280265c55fa5a6626cfeb7bab523cc627',
             scope='Actual CalculTroupe through supported request return; missing viewport/PostSound remain explicit',
             request_implementation='b1585b4bd8a64c92aa28455fc39b13c87993a067',
             request_main='66e83062f1dd821b04a59b820fcc7e2712839f60',
             captures=[dict(start=hex(inicio),end_exclusive=hex(fim),bytes_hex=codigo.hex(),
                            sha256=hashlib.sha256(codigo).hexdigest(),listing=arquivo)],
             committed_evidence=refs,native_entry='0x4259e6',pending_cleanup='0x420fb7',
             pending_viewport='0x440d9f',pending_post_sound='0x440de7',
             viewport='four explicit loaded u16 words at0x508720',
             native_execution='Actual core minimap CPU-state resumptions; no native subcall result substituted')
    (PASTA/'evidencias/producao-solicitada.json').write_text(json.dumps(r,indent=2)+'\n')
    print('Captured conditional caller and committed request evidence identities.')


if __name__=='__main__':
    main()
