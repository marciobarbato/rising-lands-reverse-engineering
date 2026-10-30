"""Original-first city-message calls from complete Economy fixtures and verified S1.

Run via heavy_lease.py. Capture refuses replacement and imports no translation.
The bounded declared cases stop at 0x48484c for AI owners; no callee is stubbed.
Comparison freshly reproduces every native case and uses only captured read-
before-write bytes in Python. No foreign source hashes are pinned.
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ambiente_ia_runtime import ROOT, ORIGINAL_SHA256
from emulador import BancadaX86, PILHA, RETORNO, mapear_paginas

ENTRY, CALL, AI_STOP = 0x484808, 0x4211e5, 0x48484c
REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
CAPTURA = ROOT / 'pesquisas-paralelas/ia-runtime/evidencias/mensagem-cidade-original.json.xz'
ECONOMIA = ROOT / 'pesquisas-paralelas/economia/evidencias/caverna-recrutamento/captura-caverna-recrutamento-exibicao.json.xz'


class Leituras:
    def __init__(self, uc):
        import unicorn
        self.uc, self.ativo, self.dados, self.escritos = uc, False, {}, set()
        self.hooks = [uc.hook_add(unicorn.UC_HOOK_MEM_READ, self.ler),
                      uc.hook_add(unicorn.UC_HOOK_MEM_WRITE, self.escrever)]

    def iniciar(self):
        self.dados, self.escritos, self.ativo = {}, set(), True

    def ler(self, uc, access, a, n, value, extra):
        if self.ativo and not PILHA <= a < PILHA + 0x10000:
            raw = bytes(uc.mem_read(a, n))
            for i, v in enumerate(raw):
                if a+i not in self.escritos:
                    self.dados.setdefault(a+i, v)

    def escrever(self, uc, access, a, n, value, extra):
        if self.ativo and not PILHA <= a < PILHA + 0x10000:
            self.escritos.update(range(a, a+n))

    def finalizar(self):
        self.ativo = False
        saida = []
        for a in sorted(self.dados):
            if saida and int(saida[-1][0], 16) + len(saida[-1][1])//2 == a:
                saida[-1][1] += f'{self.dados[a]:02x}'
            else:
                saida.append([hex(a), f'{self.dados[a]:02x}'])
        return saida


class MemoriaCapturada:
    def __init__(self, leituras):
        self.dados = {int(a, 16)+i: v for a, h in leituras for i, v in enumerate(bytes.fromhex(h))}
        self.escritos = set()

    def _acesso(self, a, n, v):
        if v is None:
            return int.from_bytes(bytes(self.dados[a+i] for i in range(n)), 'little')
        for i, b in enumerate((v & ((1 << (n*8))-1)).to_bytes(n, 'little')):
            self.dados[a+i] = b
            self.escritos.add(a+i)
        return v

    def u8(self, a, v=None):
        return self._acesso(a, 1, v)

    def u16(self, a, v=None):
        return self._acesso(a, 2, v)

    def u32(self, a, v=None):
        return self._acesso(a, 4, v)


def comparar(c):
    from mensagem_cidade_ia import mensagem_cidade
    from reinicio_ia import DependenciaIA
    m = MemoriaCapturada(c['read_before_write'])
    regs = {k: int(v, 16) for k, v in c['entry_registers'].items()}
    try:
        out = mensagem_cidade(m, regs, CALL)
        dif = {k: [hex(out[k]), c['exit_registers'][k]] for k in REG7
               if out[k] != int(c['exit_registers'][k], 16)}
        stop = None
    except DependenciaIA as e:
        out, dif, stop = None, {}, hex(e.sitio)
    changed = [[hex(a), int.from_bytes(bytes([v]), 'little'), m.dados[a]]
               for a, v in sorted({int(a,16)+i:b for a,h in c['read_before_write']
                                   for i,b in enumerate(bytes.fromhex(h))}.items()) if m.dados[a] != v]
    return dict(equal=not dif and stop == c.get('stop') and changed == c['changed_bytes'],
                register_differences=dif, python_stop=stop, changed_bytes_equal=changed == c['changed_bytes'])


def executar(traduzir=False):
    import unicorn
    from unicorn import x86_const as X
    import bancada_s1 as bs
    casos = []
    def registrar(c):
        if traduzir:
            c['comparison'] = comparar(c)
        casos.append(c)

    raw = ECONOMIA.read_bytes()
    cap = json.loads(lzma.decompress(raw))
    if cap['original_sha256'] != ORIGINAL_SHA256:
        raise ValueError('Wrong original identity')
    fixtures = [c for c in cap['calls'] if c['routine'] == 'CalculTroupe' and c['frame'] in (297, 869, 1363)]
    if len(fixtures) != 3:
        raise ValueError('Expected three real complete producer fixtures')
    for f in fixtures:
        b = BancadaX86()
        uc = b.cpu
        regions = list(uc.mem_regions())
        pages = {a & ~4095 for s,h in f['read_before_write'] for a in range(int(s,16),int(s,16)+len(h)//2)
                 if not any(lo <= a <= hi for lo,hi,_ in regions)}
        pages |= {int(store[2],16) & ~4095 for store in f['stores']
                  if not any(lo <= int(store[2],16) <= hi for lo,hi,_ in regions)}
        mapear_paginas(uc, pages)
        for a,h in f['read_before_write']:
            uc.mem_write(int(a,16), bytes.fromhex(h))
        uc.reg_write(X.UC_X86_REG_FPCW, 0x127f)
        regs = {k:int(f['entry_registers'][k],16) for k in REG7}
        entry = b.executar(0x4259e6, [(0x401000,0x494000)], regs, parada=ENTRY, limite_instrucoes=1000000)
        if (entry['EIP'] != ENTRY or int.from_bytes(uc.mem_read(entry['ESP'],4),'little') != CALL+5
                or entry['EDX'] & 255 != 3 or entry['EBX'] != 0):
            raise RuntimeError('Missed the actual city-message call')
        ref = next(c for c in f['calls'] if c[1] == 'iagVilleSendMessage')
        if any(entry[k] != int(v,16) for k,v in ref[2].items()):
            raise RuntimeError('Native entry differs from Economy capture')
        reads = Leituras(uc)
        reads.iniciar()
        out = b.retomar(ENTRY, [(0x401000,0x494000)], parada=CALL+5, limite_instrucoes=100000)
        rbw = reads.finalizar()
        if out['EIP'] != CALL+5 or out['ESP'] != entry['ESP']+4 or reads.escritos:
            raise RuntimeError('Expected a returning read-only real city message')
        if any(out[k] != int(ref[5][k],16) for k in REG7):
            raise RuntimeError('Native exit differs from Economy capture')
        registrar(dict(kind='economy_fixture', frame=f['frame'], caller_return=hex(CALL+5),
                       entry_registers={k:hex(entry[k]) for k in REG7},
                       exit_registers={k:hex(out[k]) for k in REG7},
                       read_before_write=rbw, changed_bytes=[], stop=None))

    s1 = bs.BancadaS1(2500)
    reads = Leituras(s1.b.cpu)
    seeds = []
    def escolher(n, r, ret, o):
        if ret == CALL+5:
            reads.iniciar()
            return True
        return False
    def fechar(c, blocks):
        c['read_before_write'] = reads.finalizar()
        c['stop'] = None
        registrar(c)
        seeds.append((c,blocks))
    obs = bs.Observacao(s1.b, {'iagVilleSendMessage':0}, escolher=escolher, ao_fechar=fechar)
    while s1.k < 2547:
        s1.avancar(obs)
    obs.remover()
    if obs.erros or len(seeds) != 1 or seeds[0][0]['frame'] != 2547:
        raise RuntimeError(f'Expected the S1 frame-2547 message: {obs.erros}, {len(seeds)}')
    # Original bounded leaves from the actual entry state's observed inputs.
    seed, blocks = seeds[0]
    original_regs = {k:int(v,16) for k,v in seed['entry_registers'].items()}
    if original_regs['EDX'] & 255 != 3 or original_regs['EBX'] != 0:
        raise RuntimeError('S1 call does not have the requested DL=3 / EBX=0 contract')
    original_reads = MemoriaCapturada(seed['read_before_write'])
    structure = original_regs['EAX'] & 65535
    for owner in (0, 1, 2, 3, 4, 200, 255):
        for player_type in ((0,1,2,3,255) if owner < 4 else (None,)):
            # Only the owner and player table fields used by the prefix are varied.
            b = BancadaX86()
            uc = b.cpu
            regions = list(uc.mem_regions())
            pages = {a & ~4095 for s,h in seed['read_before_write']
                     for a in range(int(s,16),int(s,16)+len(h)//2)
                     if not any(lo <= a <= hi for lo,hi,_ in regions)}
            mapear_paginas(uc, pages)
            for a,h in seed['read_before_write']:
                uc.mem_write(int(a,16), bytes.fromhex(h))
            uc.mem_write(0x49a0c8+276*structure+4,bytes([owner]))
            if owner < 4:
                table = original_reads.u32(0x5080a8)
                regions = list(uc.mem_regions())
                mapear_paginas(uc, {a & ~4095 for a in (table,table+80)
                                   if not any(lo <= a <= hi for lo,hi,_ in regions)})
                uc.mem_write(table+20*owner+1,bytes([player_type]))
            regs = {k: (v ^ (0x12340000+i*0x110000)) & 0xffffffff for i,(k,v) in enumerate(original_regs.items())}
            regs['EAX'] = (regs['EAX'] & 0xffff0000) | structure
            regs['EDX'] = (regs['EDX'] & 0xffffff00) | 3
            regs['EBX'] = 0
            reads_v = Leituras(uc)
            reads_v.iniciar()
            out = b.executar(ENTRY,[(0x401000,0x494000)],regs,parada={RETORNO,AI_STOP},limite_instrucoes=10000)
            rbw = reads_v.finalizar()
            if out['EIP'] not in (RETORNO,AI_STOP) or reads_v.escritos:
                raise RuntimeError('Declared city-message prefix did not reach its exact stop')
            registrar(dict(kind='declared_prefix', owner=owner, player_type=player_type,
                           entry_registers={k:hex(v) for k,v in regs.items()},
                           exit_registers={k:hex(out[k]) for k in REG7},
                           read_before_write=rbw, changed_bytes=[],
                           stop=hex(AI_STOP) if out['EIP'] == AI_STOP else None))
    reproduction = s1.reproducao()
    if not reproduction['code_unchanged']:
        raise RuntimeError('Original code changed during S1 capture')
    return dict(original_sha256=ORIGINAL_SHA256, economy_fixture=str(ECONOMIA.relative_to(ROOT)),
                economy_fixture_sha256=hashlib.sha256(raw).hexdigest(), s1=reproduction, cases=casos)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--comparar', action='store_true')
    ap.add_argument('--saida')
    a = ap.parse_args()
    t0 = time.monotonic()
    if not a.comparar and CAPTURA.exists():
        raise SystemExit('Refusing to replace original-only evidence')
    if a.comparar:
        raw = CAPTURA.read_bytes()
        if raw != subprocess.check_output(['git','show',f'HEAD:{CAPTURA.relative_to(ROOT)}'],cwd=ROOT):
            raise SystemExit('Commit the original-only capture first')
        ref = json.loads(lzma.decompress(raw))
    d = executar(a.comparar)
    d.update(source_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
             seconds=round(time.monotonic()-t0,3))
    if not a.comparar:
        if 'mensagem_cidade_ia' in sys.modules:
            raise RuntimeError('Translation imported during original-only capture')
        d.update(schema='rising-lands/ai-runtime-city-message-original/1',translation_executed=False)
        CAPTURA.write_bytes(lzma.compress((json.dumps(d,sort_keys=True)+'\n').encode()))
        path = CAPTURA
    else:
        results = []
        native_cases = d.pop('cases')
        if len(native_cases) != len(ref['cases']):
            raise RuntimeError('Native case count differs from the original capture')
        for c, expected in zip(native_cases, ref['cases']):
            cmp = c.pop('comparison')
            cmp['native_equals_capture'] = c == expected
            cmp['equal'] &= cmp['native_equals_capture']
            results.append(dict(kind=c['kind'],frame=c.get('frame'),owner=c.get('owner'),
                                player_type=c.get('player_type'),**cmp))
        d.update(schema='rising-lands/ai-runtime-city-message-native/1',cases=results,
                 comparisons=len(results), equal=sum(c['equal'] for c in results),
                 named_stops=sum(c['python_stop'] is not None for c in results),
                 mismatches=sum(not c['equal'] for c in results),capture_sha256=hashlib.sha256(raw).hexdigest())
        path = ROOT / (a.saida or 'pesquisas-paralelas/ia-runtime/validacao/mensagem-cidade-native.json')
        path.write_text(json.dumps(d,indent=1,sort_keys=True)+'\n')
    print(json.dumps(dict(output=str(path),cases=len(d['cases']),mismatches=d.get('mismatches'),seconds=d['seconds'])),flush=True)
    return 2 if d.get('mismatches') else 0


if __name__ == '__main__':
    raise SystemExit(main())
