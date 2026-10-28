"""Export SetDyingEngin, supported nested guard bodies and effect dispatch."""
import hashlib
import json
from pathlib import Path
import struct
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ.parent / 'source/python'))
HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
INTERVALOS = (
    ('SetDyingEngin', 0x444938, 0x444dad), ('GetBit', 0x467d97, 0x467da6),
    ('iagUnitSendMessage_prefix', 0x4829c8, 0x482a51),
    ('message44_null_group_guard', 0x482c50, 0x482c58),
    ('iagUnitSendMessage_epilogue', 0x482eb5, 0x482ebc),
    ('PlayerGetControle', 0x46d817, 0x46d838),
    ('PlaySnd_StopSound_jump', 0x48aac0, 0x48aac5),
    ('HandleSnd_StopHandle_inactive', 0x48a438, 0x48a446),
    ('TerrainEstDecouvert', 0x4766f0, 0x47670a),
    ('DeselectionEngin', 0x472648, 0x47268b), ('EnginGetPlayer', 0x442045, 0x442064),
    ('SetDyingEngin_epilogue', 0x44f29d, 0x44f2a3),
    ('shared_register_epilogue', 0x440d58, 0x440d5e),
    ('ResetEnginCollision', 0x442eac, 0x44302e),
)


def extrair():
    import capstone
    raw = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest() != HASH:
        raise ValueError('Original executable SHA-256 mismatch')
    pe = struct.unpack_from('<I', raw, 60)[0]
    n, op = (struct.unpack_from('<H', raw, pe+o)[0] for o in (6, 20))
    secoes = [struct.unpack_from('<III', raw, pe+24+op+i*40+12) for i in range(n)]
    def ler(a, tamanho):
        rva = a-0x400000
        for base, size, offset in secoes:
            if offset and base <= rva and rva+tamanho <= base+size:
                return raw[offset+rva-base:offset+rva-base+tamanho]
        raise ValueError('No original bytes at address')
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    pasta = RAIZ / 'evidencias/morte-unidades'
    pasta.mkdir(exist_ok=True, parents=True)
    trechos = []
    for nome, a, b in INTERVALOS:
        bruto = ler(a, b-a)
        ins = list(md.disasm(bruto, a))
        if sum(i.size for i in ins) != len(bruto):
            raise ValueError('Incomplete original disassembly')
        arquivo = f'{a:08x}.asm'
        linhas = [f'; {nome}; original executable SHA-256: {HASH}']
        linhas += [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in ins]
        (pasta / arquivo).write_text('\n'.join(linhas) + '\n')
        trechos.append(dict(name=nome, start=hex(a), end_exclusive=hex(b),
                            sha256=hashlib.sha256(bruto).hexdigest(), file=arquivo))
    tabela = ler(0x44491c, 28)
    dados = dict(original_sha256=HASH, capstone=capstone.__version__, intervals=trechos,
                 effect_dispatch=dict(address='0x44491c', first_type=11, bytes_hex=tabela.hex(),
                                      targets=[hex(a) for a in struct.unpack('<7I', tabela)],
                                      sha256=hashlib.sha256(tabela).hexdigest()),
                 scope='Complete ordinary hidden-unit physical returns and explicit native dependency stops; '
                       'no complete AI/sound/inventory/selection/effect/special-flag lifecycle.')
    (pasta / 'manifesto.json').write_text(json.dumps(dados, indent=2) + '\n')
    return dados


if __name__ == '__main__':
    print('Exported dying intervals:', len(extrair()['intervals']))
