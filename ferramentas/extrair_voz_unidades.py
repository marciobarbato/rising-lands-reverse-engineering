"""Export intact original unit-volume/request and selection-query bodies."""
import hashlib
import json
from pathlib import Path
import struct
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ.parent / 'source/python'))
HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'


def extrair():
    import capstone
    raw = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest() != HASH:
        raise ValueError('Original executable SHA-256 mismatch')
    pe = struct.unpack_from('<I', raw, 60)[0]
    n, op = (struct.unpack_from('<H', raw, pe+o)[0] for o in (6, 20))
    secoes = [struct.unpack_from('<III', raw, pe+24+op+i*40+12) for i in range(n)]
    pasta = RAIZ / 'evidencias/voz-unidades'
    pasta.mkdir(exist_ok=True, parents=True)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    trechos = []
    for nome, inicio, fim in (('EnginEstSelectionne', 0x472174, 0x4721a8),
                              ('EnginGetVolume', 0x440c5d, 0x440d5e),
                              ('EnginAsk', 0x440d5e, 0x440df0),
                              ('SortieTroupe_conditional_request', 0x420f9e, 0x420fb7),
                              ('PlaySnd_PostSound_dependency', 0x48aa79, 0x48aac0),
                              ('HandlSnd_Insert_dependency', 0x48a218, 0x48a438)):
        rva = inicio - 0x400000
        for base, tamanho, offset in secoes:
            if offset and base <= rva and rva + fim-inicio <= base+tamanho:
                bruto = raw[offset+rva-base:offset+rva-base+fim-inicio]
                break
        else:
            raise ValueError('No original PE bytes at address')
        ins = list(md.disasm(bruto, inicio))
        if sum(i.size for i in ins) != len(bruto):
            raise ValueError('Incomplete original disassembly')
        arquivo = f'{inicio:08x}.asm'
        linhas = [f'; {nome}; original executable SHA-256: {HASH}']
        linhas += [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in ins]
        (pasta / arquivo).write_text('\n'.join(linhas) + '\n')
        trechos.append(dict(name=nome, start=hex(inicio), end_exclusive=hex(fim),
                            sha256=hashlib.sha256(bruto).hexdigest(), file=arquivo))
    manifesto = dict(original_sha256=HASH, capstone=capstone.__version__, intervals=trechos,
                     unit_pool_pointer='0x4e19a0', unit_count=800, stride=276,
                     viewport='four u16 at 0x508720',
                     pending_sound='0x440de7 call 0x48aa79; full handle subsystem not implemented',
                     scope='Read-only volume/selection and bounded request/caller; actual sound insertion remains pending.')
    (pasta / 'manifesto.json').write_text(json.dumps(manifesto, indent=2) + '\n')
    return manifesto


if __name__ == '__main__':
    print('Exported unit request intervals:', len(extrair()['intervals']))
