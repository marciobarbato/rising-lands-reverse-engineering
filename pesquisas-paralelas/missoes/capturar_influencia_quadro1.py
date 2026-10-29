"""Original-only captures of the influence-zone queries at the exact MONDE01 frame-1 inputs.

CaseGetZoneInfluence 0x47bf66 and GetTopLeftCaseZoneInfluence 0x47c114 are
not entered in frames 0-1 (MONDE01 has no type-3 structure yet).  This script
reruns the committed first-frame path, pauses at the frame-1 TestFinDeMission
entry (``Isolamento``), and from that exact state injects native leaf calls:

* CaseGetZoneInfluence for every AX cell 0..65535, plus 256 calls with
  non-zero upper EAX bits;
* GetTopLeftCaseZoneInfluence for every zone record 0..399;
* local read/write footprints for a sample of both.

Every injected call must return to the bench trampoline with EBX/ECX/EDX/ESI/
EDI/EBP preserved; afterwards every state block must equal the paused state,
which is then restored, and the phases continue.  The run must still
reproduce every committed phase state and the entry trace.  No Python
translation is imported.

    python3 -B pesquisas-paralelas/missoes/capturar_influencia_quadro1.py \
        --saida pesquisas-paralelas/missoes/evidencias/captura-influencia-quadro1.json
"""
import argparse
import base64
import hashlib
import json
import struct
import subprocess
import sys
import time
import zlib

import ambiente_missoes
import capturar_isolados_quadro1 as ci

ROOT, OWNED = ambiente_missoes.ROOT, ambiente_missoes.OWNED
ZONA, CANTO, TABELA = 0x47bf66, 0x47c114, 0x50c614
PRESERVADOS = ('EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
AMOSTRA_CELULAS = (0, 1, 28, 29, 25*256, 26*256, 25*256+28, 25*256+29, 0x7fff, 0xff00, 0xffff)
AMOSTRA_ZONAS = (0, 1, 254, 255, 256, 399)


def compactar(valores, formato):
    dados = struct.pack('<%d%s' % (len(valores), formato), *valores)
    return dict(count=len(valores), format=formato, sha256=hashlib.sha256(dados).hexdigest(),
                zlib_base64=base64.b64encode(zlib.compress(dados, 9)).decode('ascii'))


class Varredura:
    """Injected native calls at the frame-1 TestFinDeMission pause (one or more tables)."""
    def __init__(self, tabelas=None, celulas=range(65536), observador=None):
        self.tabelas = tabelas or [dict(case='captured_inputs', writes=[])]
        self.celulas, self.observador = list(celulas), observador
        self.resultados = []

    def __call__(self, iso, fase, regs):
        if fase != 'frame1':
            return
        b, esp = iso.b, regs['ESP']
        contexto, blocos = iso._salvar()
        base = {n: regs[n] for n in PRESERVADOS}
        for tabela in self.tabelas:
            iso._restaurar(contexto, blocos)
            for endereco, dados in tabela['writes']:
                b.cpu.mem_write(endereco, bytes(dados))
            bytes_tabela = bytes(b.cpu.mem_read(TABELA, 4000))
            zonas, preservado, altos = [], True, []
            for c in self.celulas:
                r = iso.chamar_folha(ZONA, dict(base, EAX=c), esp)
                zonas.append(r['EAX'])
                preservado &= all(r[n] == base[n] for n in PRESERVADOS)
            for c in range(0, 65536, 257):
                r = iso.chamar_folha(ZONA, dict(base, EAX=0xabcd0000 | c), esp)
                altos.append([hex(c), hex(r['EAX'])])
                preservado &= all(r[n] == base[n] for n in PRESERVADOS)
            cantos = []
            for z in range(400):
                r = iso.chamar_folha(CANTO, dict(base, EAX=z, EDX=0x5a5a0000 | z), esp)
                cantos.append(r['EAX'])
                preservado &= all(r[n] == (0x5a5a0000 | z if n == 'EDX' else base[n]) for n in PRESERVADOS)
            pegadas = []
            for alvo, args in ((ZONA, AMOSTRA_CELULAS), (CANTO, AMOSTRA_ZONAS)):
                for a in args:
                    lidos, escritos, ganchos = iso._rastrear(blocos)
                    try:
                        r = iso.chamar_folha(alvo, dict(base, EAX=a), esp)
                    finally:
                        for g in ganchos:
                            b.cpu.hook_del(g)
                        b.cpu.ctl_flush_tb()
                    pilha = range(esp-0x100-0x40, esp)
                    pegadas.append(dict(routine=b.nome(alvo), eax_in=hex(a), eax_out=hex(r['EAX']),
                                        reads=[hex(x) for x in sorted(lidos) if x not in pilha],
                                        writes_outside_call_stack=[hex(x) for x in sorted(escritos) if x not in pilha]))
            iso.verificar_puro(blocos, esp, tabela['writes'])
            linha = dict(case=tabela['case'], writes=[[hex(a), bytes(d).hex()] for a, d in tabela['writes']],
                         table_sha256=hashlib.sha256(bytes_tabela).hexdigest(),
                         table_zlib_base64=base64.b64encode(zlib.compress(bytes_tabela, 9)).decode('ascii'),
                         case_get_zone_influence=compactar(zonas, 'I'),
                         zone_counts={hex(k): zonas.count(k) for k in sorted(set(zonas))},
                         high_eax_bits=altos, top_left=compactar(cantos, 'I'),
                         registers_preserved=preservado, footprints=pegadas, entry_registers={
                             k: hex(v) for k, v in regs.items()})
            self.resultados.append(linha)
            if self.observador is not None:
                self.observador(linha, bytes_tabela, zonas, altos, cantos)
        iso._restaurar(contexto, blocos)


def executar(varredura):
    return ci.executar(injecoes={'TestFinDeMission': varredura}, rotinas=('TestFinDeMission',))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    saida = ROOT/a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    revisao = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    sujo = subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain', '--', 'pesquisas-paralelas/missoes'],
                          capture_output=True, text=True).stdout
    t0 = time.monotonic()
    v = Varredura()
    b, iso, cap, reproducao = executar(v)
    relatorio = dict(
        schema='rising-lands/monde01-frame1-influence-queries/1', original_sha256=ci.HASH_ORIGINAL,
        translation_executed=False, source_revision=revisao, source_dirty_paths=sujo.splitlines(),
        source_sha256={n: hashlib.sha256((OWNED/n).read_bytes()).hexdigest()
                       for n in ('oraculo_quadro_missao.py', 'capturar_isolados_quadro1.py', 'capturar_influencia_quadro1.py')},
        frame_capture=dict(path=str(ci.CAPTURA.relative_to(ROOT)), sha256=hashlib.sha256(ci.CAPTURA.read_bytes()).hexdigest()),
        pause='frame1 TestFinDeMission entry 0x458606 (exact frame-1 inputs)',
        routines=dict(CaseGetZoneInfluence=hex(ZONA), GetTopLeftCaseZoneInfluence=hex(CANTO)),
        path_reproduction=reproducao, injections=v.resultados,
        method='Each injected call: declared EAX (EDX for GetTopLeftCaseZoneInfluence), other registers from '
               'the pause, return slot 0x100 below the paused ESP, emu_start to the bench trampoline; results '
               'are little-endian u32 EAX arrays (cells 0..65535, zones 0..399); state blocks are compared '
               'with the pause after all calls, then restored',
        seconds=round(time.monotonic()-t0, 3))
    ok = (reproducao['passed'] and len(v.resultados) == 1 and v.resultados[0]['registers_preserved'])
    if not ok:
        saida = ROOT/'.local'/('m2-influence-failed-'+time.strftime('%Y%m%dT%H%M%S')+'.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    r = v.resultados[0] if v.resultados else {}
    print(json.dumps(dict(output=str(saida), sha256=hashlib.sha256(saida.read_bytes()).hexdigest(),
                          reproduction=reproducao.get('passed'), zone_counts=r.get('zone_counts'),
                          registers_preserved=r.get('registers_preserved'),
                          seconds=relatorio['seconds']), indent=1))
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
