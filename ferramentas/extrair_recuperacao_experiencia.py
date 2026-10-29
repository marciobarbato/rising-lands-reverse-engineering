"""Export intact Engin_RetrieveExperimente bytes and static saved-buffer provenance.

Static analysis only: no instruction is executed. The intact executable is the
byte source; the normalized analysis PE is not read here.
"""
import bisect
import csv
import hashlib
import json
from pathlib import Path
import struct
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ.parent / 'source/python'))
HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
ATUAL, GUARDADA, FIM = 0x4e19c4, 0x4e19ec, 0x4e1a14

# (role, name, start, end_exclusive). Only the first two are translated by Core.
TRECHOS = (
    ('translated', 'Engin_RetrieveExperimente', 0x441623, 0x441659),
    ('translated', 'retrieve_shared_epilogue', 0x440d59, 0x440d5e),
    ('provenance', 'Engin_ResetExperience', 0x441470, 0x4414ad),
    ('provenance', 'reset_shared_epilogue', 0x440d5a, 0x440d5e),
    ('provenance', 'Engin_LoadExperimente', 0x4414ad, 0x4414d7),
    ('provenance', 'Engin_SaveExperimente', 0x4414d7, 0x4414f8),
    ('provenance', 'Engin_StoreExperimente', 0x4414f8, 0x441623),
    ('provenance', 'store_shared_epilogue', 0x440d55, 0x440d5e),
    ('caller', 'MissionLoad_tail_call_site', 0x46c5af, 0x46c5c3),
    ('caller', 'PlayerRetrieve_entry_consumes_no_EAX', 0x46df41, 0x46df4d),
    ('caller', 'CalculGame_mission_end_store_site', 0x42ca6e, 0x42ca91),
    ('caller', 'MenuInit_reset_site', 0x468e28, 0x468e37),
    ('caller', 'MissionLoadName_reset_site', 0x46c687, 0x46c696),
    ('caller', 'GameLoad_load_site', 0x46bae9, 0x46baf5),
    ('caller', 'GameSave_save_site', 0x46c070, 0x46c075),
)


def _imagem(raw):
    pe = struct.unpack_from('<I', raw, 60)[0]
    n, op = (struct.unpack_from('<H', raw, pe+o)[0] for o in (6, 20))
    secoes = []
    for i in range(n):
        cab = pe+24+op+i*40
        rva, tamanho, offset = struct.unpack_from('<III', raw, cab+12)
        secoes.append((raw[cab:cab+8].rstrip(b'\0').decode(), rva, tamanho, offset,
                       struct.unpack_from('<I', raw, cab+36)[0]))
    return secoes


def _bytes(raw, secoes, inicio, fim):
    rva = inicio - 0x400000
    for _, base, tamanho, offset, _ in secoes:
        if offset and base <= rva and rva + fim-inicio <= base+tamanho:
            return raw[offset+rva-base:offset+rva-base+fim-inicio]
    raise ValueError(f'No original PE bytes at 0x{inicio:x}')


def extrair():
    import capstone
    raw = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest() != HASH:
        raise ValueError('Original executable SHA-256 mismatch')
    secoes = _imagem(raw)
    simbolos = sorted((int(r['endereco'], 16), r['nome_original']) for r in
                      csv.DictReader((RAIZ / 'evidencias/simbolos-importados.tsv').open(), delimiter='\t'))
    enderecos = [s[0] for s in simbolos]

    def simbolo(a):
        i = bisect.bisect_right(enderecos, a)-1
        return f'{simbolos[i][1]}+0x{a-simbolos[i][0]:x}'

    pasta = RAIZ / 'evidencias/recuperacao-experiencia'
    pasta.mkdir(exist_ok=True, parents=True)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    md.detail = True
    trechos = []
    for papel, nome, inicio, fim in TRECHOS:
        bruto = _bytes(raw, secoes, inicio, fim)
        ins = list(md.disasm(bruto, inicio))
        if sum(i.size for i in ins) != len(bruto):
            raise ValueError(f'Incomplete original disassembly of {nome}')
        arquivo = f'{inicio:08x}.asm'
        linhas = [f'; {nome} ({papel}); original executable SHA-256: {HASH}']
        linhas += [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in ins]
        (pasta / arquivo).write_text('\n'.join(linhas) + '\n')
        trechos.append(dict(role=papel, name=nome, start=hex(inicio), end_exclusive=hex(fim),
                            sha256=hashlib.sha256(bruto).hexdigest(), file=arquivo))

    # Every decoded BEGTEXT instruction whose displacement/immediate addresses the
    # 80 bytes (current + saved), including the -2 biased displacements of the copy.
    texto = next(s for s in secoes if s[4] & 0x20000000)
    _, base_texto, tamanho_texto, offset_texto, _ = texto
    codigo = raw[offset_texto:offset_texto+tamanho_texto]
    referencias = {}
    for off in range(len(codigo)-3):
        v = struct.unpack_from('<I', codigo, off)[0]
        if not ATUAL-2 <= v < FIM:
            continue
        alvo = 0x400000+base_texto+off
        # Linear sweep from the containing original symbol gives true boundaries
        # (a backward guess could drop the 0x66 operand-size prefix).
        i = bisect.bisect_right(enderecos, alvo)-1
        cursor, ins = simbolos[i][0], None
        while cursor <= alvo:
            ins = next(md.disasm(codigo[cursor-0x400000-base_texto:cursor-0x400000-base_texto+16], cursor, 1), None)
            if ins is None or ins.address+ins.size > alvo:
                break
            cursor += ins.size
        if ins is None or not ins.address <= alvo < ins.address+ins.size:
            continue
        valores = [op.mem.disp & 0xffffffff for op in ins.operands if op.type == capstone.x86.X86_OP_MEM]
        valores += [op.imm & 0xffffffff for op in ins.operands if op.type == capstone.x86.X86_OP_IMM]
        if v in valores:
            referencias[ins.address] = dict(address=hex(ins.address), function=simbolo(ins.address),
                                            value=hex(v), text=f'{ins.mnemonic} {ins.op_str}',
                                            bytes=ins.bytes.hex())
    chamadas = []
    for alvo in (0x441623, 0x441470, 0x4414ad, 0x4414d7, 0x4414f8):
        for off in range(len(codigo)-4):
            if codigo[off] == 0xe8 and 0x400000+base_texto+off+5+struct.unpack_from('<i', codigo, off+1)[0] == alvo:
                origem = 0x400000+base_texto+off
                chamadas.append(dict(target=hex(alvo), target_symbol=simbolo(alvo), call=hex(origem),
                                     caller=simbolo(origem)))
    bss = next(s for s in secoes if s[0] == '.bss')
    manifesto = dict(
        original_sha256=HASH, capstone=capstone.__version__, intervals=trechos,
        current_queue=dict(start=hex(ATUAL), end_exclusive=hex(GUARDADA)),
        saved_queue=dict(start=hex(GUARDADA), end_exclusive=hex(FIM),
                         section='.bss', section_start=hex(0x400000+bss[1]),
                         section_end_exclusive=hex(0x400000+bss[1]+bss[2]), file_backed=False),
        buffer_references=[referencias[a] for a in sorted(referencias)],
        direct_calls=chamadas,
        scope='Static byte export. Only Engin_RetrieveExperimente and its 5-byte shared epilogue are '
              'translated by Core; reset/load/save/store routines and call sites are provenance evidence.')
    (pasta / 'manifesto.json').write_text(json.dumps(manifesto, indent=1) + '\n')
    return manifesto


if __name__ == '__main__':
    m = extrair()
    print('Exported intervals:', len(m['intervals']), 'buffer references:', len(m['buffer_references']),
          'direct calls:', len(m['direct_calls']))
