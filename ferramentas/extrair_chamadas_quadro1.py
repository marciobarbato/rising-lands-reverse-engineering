"""Export the intact intervals of the Core callees reached by MONDE01 frame 0/frame 1.

Static only: no instruction is executed. For each routine (and the shared tails
and jump tables it uses) the manifest records the SHA-256 of the original bytes;
it also records the static data tables the translations index, and for every
call site in the isolated native capture whether the caller overwrites the
arithmetic flags before reading any (``caller_flag_use``), which is why the
translations do not reproduce flags.
"""
import hashlib
import json
from pathlib import Path
import struct
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
from extrair_fundacoes_quadro import HASH, _bytes   # noqa: E402

PASTA = RAIZ / 'evidencias/fundacoes-quadro/chamadas-quadro1'
CAPTURA = RAIZ / 'evidencias/fundacoes-quadro/captura-chamadas-quadro1.json'
# (role, name, start, end_exclusive)
TRECHOS = (
    ('routine', 'GetBit', 0x467d97, 0x467da6),
    ('routine', 'SetBit', 0x467d71, 0x467d97),
    ('routine', 'CaseEstDecouverte', 0x4766d6, 0x4766f0),
    ('routine', 'CaseEstIlluminee', 0x47693a, 0x476951),
    ('routine', 'BatimentCollision', 0x41ab5c, 0x41ac8b),
    ('routine', 'BatimentGetCase', 0x41aee2, 0x41aff8),
    ('shared_epilogue', 'BatimentGetCase_epilogue_0x41db1e', 0x41db1e, 0x41db24),
    ('routine', 'BatimentEstDecouvert', 0x419c4f, 0x419d54),
    ('shared_tail', 'BatimentEstDecouvert_tail_0x419c3f', 0x419c3f, 0x419c4f),
    ('routine', 'BatimentContourEstIllumine', 0x4199f9, 0x419b3f),
    ('routine', 'SetCollision', 0x47622e, 0x47623e),
    ('routine', 'Chemin_ModifieZone', 0x43e138, 0x43e2a3),
    ('routine', 'SetEnginCollision', 0x442cb4, 0x442e41),
    ('shared_epilogue', 'SetEnginCollision_epilogue_0x445f27', 0x445f27, 0x445f2d),
    ('routine', 'CalculFatigue', 0x452cc8, 0x452ef7),
    ('shared_epilogue', 'CalculFatigue_epilogue_0x440d58', 0x440d58, 0x440d5e),
)
TABELAS_SALTO = (('BatimentCollision', 0x41ab04, 22), ('Chemin_ModifieZone', 0x43e128, 4),
                 ('SetEnginCollision', 0x442c4c, 26), ('CalculFatigue', 0x452cac, 7))
# Initialized DGROUP data the translations index (bytes from the PE image).
DADOS = (('structure mask tables 0x495c04..0x495d8c', 0x495c04, 0x495d8c),
         ('structure width/height per type, stride 52', 0x495d8c, 0x495d8c + 52 * 26),
         ('unit occupation class per type', 0x4962c8, 0x4962c8 + 26),
         ('unit fatigue threshold u16 per type, stride 50', 0x4965dc, 0x4965dc + 50 * 26))
FLAGS = ('AF', 'CF', 'OF', 'PF', 'SF', 'ZF')


def uso_flags(md, raw, retorno, limite=16):
    """Walk forward from a call's return: does any arithmetic flag get read before all are written?"""
    from capstone import x86 as cx
    escritos, passos, a = set(), [], retorno
    for _ in range(limite):
        i = next(md.disasm(_bytes(raw, a, a + 16), a, 1))
        passos.append(f'{i.address:x} {i.mnemonic} {i.op_str}')
        lidos = {f for f in FLAGS if i.eflags & getattr(cx, f'X86_EFLAGS_TEST_{f}')}
        if lidos - escritos:
            return dict(result='reads_flags_first', instructions=passos)
        for f in FLAGS:
            if i.eflags & (getattr(cx, f'X86_EFLAGS_MODIFY_{f}') | getattr(cx, f'X86_EFLAGS_RESET_{f}')
                           | getattr(cx, f'X86_EFLAGS_SET_{f}') | getattr(cx, f'X86_EFLAGS_UNDEFINED_{f}')):
                escritos.add(f)
        if escritos == set(FLAGS):
            return dict(result='overwritten_before_read', instructions=passos)
        if i.mnemonic in ('jmp', 'call') and i.op_str.startswith('0x'):
            a = int(i.op_str, 16)      # a direct call continues into the callee's entry
            continue
        if i.mnemonic in ('ret', 'call') or i.mnemonic.startswith('j'):
            return dict(result='undecided', instructions=passos)
        a += i.size
    return dict(result='undecided', instructions=passos)


def extrair():
    import capstone
    raw = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest() != HASH:
        raise ValueError('Original executable SHA-256 mismatch')
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    md.detail = True
    PASTA.mkdir(parents=True, exist_ok=True)
    trechos = []
    for papel, nome, inicio, fim in TRECHOS:
        bruto = _bytes(raw, inicio, fim)
        ins = list(md.disasm(bruto, inicio))
        if sum(i.size for i in ins) != len(bruto):
            raise ValueError(f'{nome}: interval does not decode to instruction boundaries')
        asm = PASTA / f'{inicio:08x}.asm'
        asm.write_text(''.join(f'{i.address:08x}  {i.bytes.hex():<20} {i.mnemonic} {i.op_str}\n' for i in ins))
        trechos.append(dict(role=papel, name=nome, start=hex(inicio), end_exclusive=hex(fim), bytes=len(bruto),
                            sha256=hashlib.sha256(bruto).hexdigest(), instructions=len(ins), asm=asm.name,
                            calls=[f'{i.address:x} {i.op_str}' for i in ins if i.mnemonic == 'call']))
    tabelas = [dict(routine=n, address=hex(a), targets=[hex(v) for v in struct.unpack(f'<{k}I', _bytes(raw, a, a + 4 * k))])
               for n, a, k in TABELAS_SALTO]
    dados = [dict(name=n, start=hex(a), end_exclusive=hex(z), sha256=hashlib.sha256(_bytes(raw, a, z)).hexdigest())
             for n, a, z in DADOS]
    captura = json.loads(CAPTURA.read_bytes())
    sitios = sorted({(c['routine'], c['caller'], c['caller_return']) for c in captura['calls']})
    flags = [dict(routine=r, caller=c, caller_return=a, **uso_flags(md, raw, int(a, 16))) for r, c, a in sitios]
    manifesto = dict(original_sha256=HASH, capstone=capstone.__version__, scope='static only; no execution',
                     capture_sha256=hashlib.sha256(CAPTURA.read_bytes()).hexdigest(), intervals=trechos,
                     jump_tables=tabelas, initialized_data=dados, caller_flag_use=flags)
    (PASTA / 'manifesto.json').write_text(json.dumps(manifesto, indent=1) + '\n')
    return manifesto


if __name__ == '__main__':
    m = extrair()
    print(json.dumps(dict(intervals=len(m['intervals']),
                          flag_use={f['caller']: f['result'] for f in m['caller_flag_use']}), indent=1))
