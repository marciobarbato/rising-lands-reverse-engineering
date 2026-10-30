"""Original-first register queries requested by AI/runtime, with native read sets for CPU-free replay.

Declare leaves from S1's verified frame-11250 snapshot, not new in-situ S1 observations. Every state byte and
type byte is exercised, with upper register bits and pool endpoints. Only the intact original executes during
--capturar; commit that capture before comparison. All native invocations go through heavy_lease.py.

    python3 .../heavy_lease.py core -- python3 -B ferramentas/validar_consultas_estado_core.py --capturar
    # commit the original-only capture
    python3 .../heavy_lease.py core -- python3 -B ferramentas/validar_consultas_estado_core.py
"""
import argparse
from collections import Counter
import hashlib
import json
import lzma
from pathlib import Path
import struct
import subprocess
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
import bancada_s1 as bs

CAPTURA = RAIZ / 'evidencias/lacunas-s1/consultas-estado-original.json.xz'
RELATORIO = RAIZ / 'relatorios/consultas-estado-core-emulada.json'
FONTES = ('ferramentas/validar_consultas_estado_core.py', 'ferramentas/consultas_estado_core.py',
          'ferramentas/provedores_lacunas_core.py', 'ferramentas/selecao_ordens.py',
          'ferramentas/memoria_quadro_core.py', 'ferramentas/bancada_s1.py')
REG7, M32 = bs.REGISTROS, 0xffffffff
INTERVALOS = (('EnginEstVivant', 0x443dad, 0x443ddd),
              ('BatimentGetDecalageConstruction', 0x41aea4, 0x41aee2),
              ('construction jump table', 0x41ae4c, 0x41aea4))


def revisao():
    return subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=RAIZ, check=True,
                          capture_output=True, text=True).stdout.strip()


def declaracoes(pool):
    r = dict(EAX=0, EBX=0x12345678, ECX=0x87654321, EDX=0xabcdef01,
             ESI=0x13572468, EDI=0x24681357, EBP=0x76543210)
    for unidade, estados, alto in ((15, range(256), 0x5a5a0000),
                                   (0, (0, 4, 1, 255), 0xffff0000),
                                   (799, (0, 4, 1, 255), 0x80000000)):
        for estado in estados:
            yield ('EnginEstVivant', f'unit {unidade}, state {estado}, high {alto:#x}',
                   dict(r, EAX=alto | unidade), [(pool + 276 * unidade + 2, bytes([estado]))])
    for alto in (0, 0xffff0000, 0x80000000, 0x12340000):
        yield ('EnginEstVivant', f'unit 15 active, high {alto:#x}',
               dict(r, EAX=alto | 15), [(pool + 276 * 15 + 2, b'\x01')])
    for alto, tipos in ((0xa5a50000, range(256)), (0, range(22))):
        for tipo in tipos:
            yield ('BatimentGetDecalageConstruction', f'type {tipo}, high {alto:#x}',
                   dict(r, EAX=alto | tipo), [])


def memoria_leituras(leituras):
    """Writable copies of exactly the native non-stack reads; unobserved bytes stay unmapped."""
    from memoria_quadro_core import MemoriaQuadro
    segmentos = []
    for a, v in sorted((int(a, 16), v) for a, v in leituras.items()):
        if segmentos and segmentos[-1][0] + len(segmentos[-1][1]) == a:
            segmentos[-1][1].append(v)
        else:
            segmentos.append((a, bytearray([v])))
    return MemoriaQuadro(segmentos), segmentos


def comparar(caso):
    from consultas_estado_core import ConsultasEstadoCore, provedor_consultas_estado
    from provedores_lacunas_core import provedor_lacunas_s1
    entrada = {k: int(caso['entry_registers'][k], 16) for k in REG7}
    entrada['ESP'] = int(caso['esp'], 16)
    esperado = {k: int(caso['exit_registers'][k], 16) for k in REG7 + ('ESP',)}
    diferencas, alteracoes = {}, {}
    try:
        for modo in ('direct', 'provider', 's1_provider'):
            m, segmentos = memoria_leituras(caso['entry_reads'])
            antes = [bytes(d) for _, d in segmentos]
            t = ConsultasEstadoCore(m)
            if modo == 'direct':
                saida = t.chamar(caso['routine'], entrada)
                nomes = REG7 + ('ESP',)
            else:
                p = provedor_consultas_estado(t) if modo == 'provider' else provedor_lacunas_s1(m)
                saida = p(caso['routine'], 0x4731d3 if caso['routine'] == 'EnginEstVivant' else 0x44ad30,
                          dict(entrada))
                nomes = REG7
            diferencas[modo] = {k: [hex(saida[k]), hex(esperado[k])] for k in nomes if saida[k] != esperado[k]}
            alteracoes[modo] = any(bytes(d) != v for (_, d), v in zip(segmentos, antes))
        ok = not any(diferencas.values()) and not any(alteracoes.values()) and not caso['changed_bytes']
        return dict(ok=ok, register_differences=diferencas, memory_changed=alteracoes)
    except Exception as erro:  # comparison failure, never a fabricated result
        return dict(ok=False, python_error=f'{type(erro).__name__}: {erro}')


def executar(comparar_python=False):
    import emulador
    import unicorn
    b = bs.BancadaS1(11250)
    cpu = b.b.cpu
    pool = struct.unpack('<I', bytes(cpu.mem_read(0x4e19a0, 4)))[0]
    leituras, ativo = {}, False

    def ler(cpu, acesso, endereco, tamanho, valor, dados):
        if ativo and not bs.PILHA_NATIVA <= endereco < bs.PILHA_NATIVA + bs.TAMANHO_PILHA:
            for i, v in enumerate(bytes(cpu.mem_read(endereco, tamanho))):
                leituras.setdefault(hex(endereco + i), v)

    gancho = cpu.hook_add(unicorn.UC_HOOK_MEM_READ, ler)
    casos = []
    t0 = time.monotonic()
    try:
        for nome, rotulo, regs, escritas in declaracoes(pool):
            leituras = {}
            ativo = True
            try:
                caso, _ = bs.folha(b.b, nome, regs, (), escritas, rotulo, 11250)
            finally:
                ativo = False
            caso['entry_reads'] = dict(leituras)
            if caso['changed_bytes'] or caso['boundaries']:
                raise RuntimeError(f'{rotulo}: a supposedly read-only query had effects')
            if comparar_python:
                caso['comparison'] = comparar(caso)
            casos.append(caso)
            if len(casos) % 100 == 0:
                print(f'{len(casos)} cases, {time.monotonic() - t0:.1f}s', file=sys.stderr, flush=True)
    finally:
        cpu.hook_del(gancho)
    raw = bs.EXE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != emulador.HASH_ORIGINAL:
        raise RuntimeError('original executable identity changed')
    intervalos = [dict(name=n, start=hex(a), end_exclusive=hex(z),
                       sha256=hashlib.sha256(raw[a - 0x401000 + 0x400:z - 0x401000 + 0x400]).hexdigest())
                  for n, a, z in INTERVALOS]
    return dict(original_sha256=emulador.HASH_ORIGINAL, source_revision=revisao(),
                fixture=b.reproducao(), scope='declared read-only leaves from S1 frame 11250; no frame advance',
                original_intervals=intervalos, cases=casos,
                by_routine=dict(Counter(c['routine'] for c in casos)), seconds=round(time.monotonic() - t0, 2))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--capturar', action='store_true')
    a = ap.parse_args()
    from encerramento_captura import encerrar_captura
    if a.capturar:
        if CAPTURA.exists():
            raise SystemExit(f'Refusing to overwrite {CAPTURA}')
        d = executar()
        if 'consultas_estado_core' in sys.modules or 'provedores_lacunas_core' in sys.modules:
            raise RuntimeError('capture imported the new translation')
        d.update(schema='rising-lands/core-state-queries-capture/1', translation_executed=False,
                 capture_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
        CAPTURA.write_bytes(lzma.compress((json.dumps(d, sort_keys=True) + '\n').encode(), preset=9))
        print(json.dumps(dict(output=str(CAPTURA), cases=len(d['cases']), by_routine=d['by_routine'],
                              code_unchanged=d['fixture']['code_unchanged'], seconds=d['seconds']), indent=1))
        encerrar_captura(0, CAPTURA)
    else:
        bruto = CAPTURA.read_bytes()
        publicado = subprocess.run(['git', 'show', f'HEAD:{CAPTURA.relative_to(RAIZ)}'], cwd=RAIZ,
                                   check=True, capture_output=True).stdout
        if bruto != publicado:
            raise SystemExit('Commit the original-only capture before comparing')
        ref = json.loads(lzma.decompress(bruto))
        d = executar(comparar_python=True)
        registros = []
        for i, c in enumerate(d.pop('cases')):
            cmp = c.pop('comparison')
            cmp['native_equals_capture'] = i < len(ref['cases']) and c == ref['cases'][i]
            cmp['ok'] = cmp['ok'] and cmp['native_equals_capture']
            registros.append(dict(routine=c['routine'], label=c['label'], **cmp))
        d.update(schema='rising-lands/core-state-queries-differential/1',
                 capture=dict(path=str(CAPTURA.relative_to(RAIZ)), sha256=hashlib.sha256(bruto).hexdigest()),
                 source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in FONTES},
                 comparisons=len(registros), capture_cases=len(ref['cases']), cases=registros,
                 mismatches=[c for c in registros if not c['ok']])
        ok = (not d['mismatches'] and d['comparisons'] == d['capture_cases'] and
              d['fixture']['code_unchanged'] and d['original_intervals'] == ref['original_intervals'])
        saida = RELATORIO if ok else RAIZ / '.local/lacunas-s1/consultas-estado-falha.json'
        saida.parent.mkdir(exist_ok=True, parents=True)
        saida.write_text(json.dumps(d, indent=1, sort_keys=True) + '\n')
        print(json.dumps(dict(output=str(saida), comparisons=d['comparisons'],
                              mismatches=len(d['mismatches']), by_routine=d['by_routine'], seconds=d['seconds']), indent=1))
        encerrar_captura(0 if ok else 2, saida)


if __name__ == '__main__':
    main()
