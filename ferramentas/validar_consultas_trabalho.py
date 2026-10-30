"""TerrainEstGc and SetMiniMap at CalculWorkEngin's real calls (native): AI/runtime's M3.1 stops P7/P4 and P5.

AI/runtime's chain stops at two Core names inside CalculWorkEngin (feat/re-ai-runtime ``M3_1_CADEIA_ALEM_220.md``):
TerrainEstGc at 0x44d8cd for an object byte >= 0x1d (P7 2801, P4 460) and SetMiniMap at 0x44c437 (P5 760; the
builder leaving its mine re-enters the unit layer, mode 4 for a player owner). Both are reached by Economy's committed
work-cycle scenario (``capturar_ciclo_trabalho.ordens``): TerrainEstGc from frame 261 (unit 14 on its field), the
mine exit at frame 572.

Bench and method are ``validar_fadiga_vegetacao``'s (``Execucao``): only TerrainEstGc and SetMiniMap are isolated
(TerrainEstGc always; SetMiniMap from CalculWorkEngin always and AvanceEngin's mode-4 call for its first
``MAX_AVANCE`` calls); each isolated call is an in-situ case, and from its entry state declared variants run the
original as a leaf (TerrainEstGc: object bytes 0x00..0xff at the cell, upper register bits; SetMiniMap mode 4: owners
0..3/4/0xc8, the cell lit or not for the local player, map corners, upper register bits). Translations compared:
``incursao_core.terreno_esta_gc`` and ``incursao_core.definir_minimapa`` (the flat providers ``traducao_core``
serves), EAX..EBP, ESP and every byte.

    python3 "…/heavy_lease.py" core -- python3 -B ferramentas/validar_consultas_trabalho.py \\
        --capturar evidencias/consultas-trabalho/captura-trabalho.json.xz
    python3 "…/heavy_lease.py" core -- python3 -B ferramentas/validar_consultas_trabalho.py
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import struct
import subprocess
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
for _p in (RAIZ / 'ferramentas', RAIZ / 'pesquisas-paralelas/economia'):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import validar_fadiga_vegetacao as vf  # noqa: E402

REGISTROS = vf.REGISTROS
M32 = 0xffffffff
ISOLADAS = ('TerrainEstGc', 'SetMiniMap')
ATE = 600
RETORNOS_TRABALHO = {0x44c43c: 'CalculWorkEngin 0x44c437', 0x44c248: 'CalculWorkEngin 0x44c243'}
RETORNO_AVANCE_MINIMAPA = 0x4489c8         # AvanceEngin's mode-4 SetMiniMap
MAX_AVANCE = 2
CAPTURA = RAIZ / 'evidencias/consultas-trabalho/captura-trabalho.json.xz'
RELATORIO = RAIZ / 'relatorios/consultas-trabalho-emulada.json'
FONTES = ('ferramentas/validar_consultas_trabalho.py', 'ferramentas/validar_fadiga_vegetacao.py',
          'ferramentas/incursao_core.py', 'ferramentas/chamadas_quadro_core.py')
GRADES_LUZ = 0x507d88


class ExecucaoTrabalho(vf.Execucao):
    def __init__(self, traduzir=None):
        super().__init__('trabalho', traduzir)
        self.feitos = set()

    def escolher(self, nome, regs, c):
        retorno = c.u32(regs['ESP'])
        if nome == 'TerrainEstGc':
            return True
        if retorno in RETORNOS_TRABALHO:
            return True
        if retorno == RETORNO_AVANCE_MINIMAPA and self.avance < MAX_AVANCE:
            self.avance += 1
            return True
        return False

    def observador(self, nome, regs, blocos, resultado):
        caso = dict(routine=nome, label=f'{nome} in situ from {resultado["caller"]}', kind='in_situ',
                    frame=resultado['frame'], caller=resultado['caller'], caller_return=resultado['caller_return'],
                    entry_registers={k: hex(regs[k]) for k in REGISTROS}, esp=hex(regs['ESP']), stack_args=[],
                    writes=[], exit_registers={k: resultado['exit_registers'][k] for k in REGISTROS + ('ESP',)},
                    changed_bytes=resultado['changed_bytes'],
                    boundaries=[dict(routine=e['routine'], caller=e['caller'], registers=e['registers'],
                                     stack_words=e['stack_words'], declared_eax=e['declared_eax'])
                                for e in resultado['boundaries']])
        self.registrar(caso, blocos)
        sitio = (nome, resultado['caller_return'])
        if sitio not in self.feitos:
            self.feitos.add(sitio)
            if nome == 'TerrainEstGc':
                self._variantes_gc(regs, blocos)
            elif int(resultado['caller_return'], 16) in RETORNOS_TRABALHO:
                self._variantes_minimapa(regs, blocos)
        self._restaurar(blocos)

    def _variantes_gc(self, regs, blocos):
        c = self.ciclo
        r0 = {k: regs[k] for k in REGISTROS}
        celula = r0['EAX'] & 0xffff
        endereco = c.u32(vf.GRADE_OBJETOS) + celula
        for objeto in (0x00, 0x01, 0x1c, 0x1d, 0x1e, 0x28, 0x33, 0x34, 0x35, 0x36, 0x42, 0x43, 0x46, 0x80, 0xff):
            self._rodar('TerrainEstGc', r0, (), [(endereco, bytes([objeto]))],
                        f'TerrainEstGc: object {objeto:#x}', blocos)
        self._rodar('TerrainEstGc', dict(r0, EAX=0xabcd0000 | celula, EDX=0x12345678, EBX=0x9abcdef0), (), (),
                    'TerrainEstGc: upper register bits', blocos)

    def _variantes_minimapa(self, regs, blocos):
        c = self.ciclo
        r0 = {k: regs[k] for k in REGISTROS}
        celula = r0['EBX'] & 0xffff
        larg, alt = c.u16(vf.LARGURA), c.u16(vf.ALTURA)
        local = c.u8(vf.JOGADOR_LOCAL)
        luz = c.u32(GRADES_LUZ + 4 * local) + celula
        casos = [(f'owner {d}', dict(EAX=d), []) for d in (0, 1, 2, 3, 4, 0xc8)]
        casos += [('cell lit (light byte 0)', {}, [(luz, b'\x00')]), ('cell unlit (light byte 0x10)', {},
                                                                       [(luz, b'\x10')])]
        casos += [(f'{n}', dict(EBX=cel), []) for n, cel in (('corner (0,0)', 0), ('corner (w-1,h-1)',
                                                                                    (alt - 1) * 256 + larg - 1))]
        casos += [('upper register bits', dict(EAX=0x11110000 | (r0['EAX'] & 0xff), EDX=0x22220004,
                                               EBX=0x33330000 | celula, ECX=0x44444444), [])]
        for rotulo, trocas, escritas in casos:
            self._rodar('SetMiniMap', dict(r0, **trocas), (), escritas, f'SetMiniMap mode 4: {rotulo}', blocos)

    def executar(self):
        import capturar_ciclo_trabalho as cct
        from bancada_ciclo_trabalho import Ciclo
        self.ciclo = Ciclo(ISOLADAS, self.escolher, cct.ordens(cct.Estado()), observador=self.observador)

        def progresso(k, t):
            if k % 100 == 0:
                print(f'frame {k} {t:.0f}s cases {len(self.casos)}', file=sys.stderr, flush=True)
        return self.ciclo.executar(ATE, progresso)


def traduzir(caso, blocos):
    """``incursao_core`` over a copy of the case's entry state against the native result."""
    from incursao_core import definir_minimapa, terreno_esta_gc
    m, copias = vf.memoria_caso(blocos)
    r = {k: int(caso['entry_registers'][k], 16) for k in REGISTROS}
    try:
        if caso['routine'] == 'TerrainEstGc':
            saida = terreno_esta_gc(m, r['EAX'])
        else:
            saida = definir_minimapa(m, r['EAX'], r['EDX'], r['EBX'])
    except Exception as erro:                 # a mismatch, never ignored
        return dict(ok=False, python_error=f'{type(erro).__name__}: {erro}')
    final = dict(r, **saida)
    final['ESP'] = (int(caso['esp'], 16) + 4) & M32
    nativos = {k: int(caso['exit_registers'][k], 16) for k in REGISTROS + ('ESP',)}
    dif = {k: [hex(final[k]), hex(nativos[k])] for k in REGISTROS + ('ESP',) if (final[k] ^ nativos[k]) & M32}
    py = vf.mudancas(blocos, copias)
    ok = not dif and py == caso['changed_bytes'] and not caso['boundaries']
    resultado = dict(ok=ok, register_differences=dif, changed_equal=py == caso['changed_bytes'],
                     native_changed=len(caso['changed_bytes']), uncertain_bits={})
    if py != caso['changed_bytes']:
        a, b = {x[0]: x for x in py}, {x[0]: x for x in caso['changed_bytes']}
        resultado.update(python_only=[a[k] for k in a if a[k] != b.get(k)][:16],
                         native_only=[b[k] for k in b if b[k] != a.get(k)][:16])
    return resultado


def capturar(saida):
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    ex = ExecucaoTrabalho()
    segundos = ex.executar()
    if 'incursao_core' in sys.modules:
        raise RuntimeError('The capture imported the translation')
    revisao = subprocess.run(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    dados = dict(schema='rising-lands/core-work-cycle-queries-capture/1', original_sha256=HASH_ORIGINAL,
                 translation_executed=False, scenario='trabalho', last_counter=ATE, source_revision=revisao,
                 capture_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 economy_sources=vf.fontes_economia(), path_reproduction=ex.ciclo.reproducao, seconds=segundos,
                 summary=vf.resumo(ex.casos), cases=ex.casos)
    saida.parent.mkdir(parents=True, exist_ok=True)
    bruto = (json.dumps(dados, sort_keys=True) + '\n').encode()
    saida.write_bytes(lzma.compress(bruto, preset=9))
    print(json.dumps(dict(output=str(saida), raw_sha256=hashlib.sha256(bruto).hexdigest(),
                          reproduction=ex.ciclo.reproducao, summary=dados['summary'], seconds=segundos), indent=1))
    encerrar_captura(0, saida)


def validar(saida):
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    ref = json.loads(lzma.decompress(CAPTURA.read_bytes()))
    ex = ExecucaoTrabalho(traduzir=traduzir)
    segundos = ex.executar()
    registros, mismatches, por_rotina = [], [], {}
    for i, caso in enumerate(ex.casos):
        cmp = caso['comparison']
        cmp['native_equals_capture'] = i < len(ref['cases']) and ref['cases'][i] == vf._sem_comparacao(caso)
        cmp['ok'] = cmp['ok'] and cmp['native_equals_capture']
        r = dict(routine=caso['routine'], label=caso['label'], kind=caso['kind'], frame=caso['frame'], **cmp)
        registros.append(r)
        p = por_rotina.setdefault(r['routine'], dict(cases=0, mismatches=0))
        p['cases'] += 1
        if not r['ok']:
            mismatches.append(r)
            p['mismatches'] += 1
    relatorio = dict(
        schema='rising-lands/core-work-cycle-queries-differential/1', original_sha256=HASH_ORIGINAL,
        capture=dict(path=str(CAPTURA.relative_to(RAIZ)), sha256=hashlib.sha256(CAPTURA.read_bytes()).hexdigest()),
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in FONTES},
        economy_sources=vf.fontes_economia(), path_reproduction=ex.ciclo.reproducao, comparisons=len(registros),
        capture_cases=len(ref['cases']), per_routine=por_rotina, mismatches=mismatches,
        changed_bytes_compared=sum(len(c['changed_bytes']) for c in ex.casos), cases=registros, seconds=segundos)
    ok = all(ex.ciclo.reproducao.values()) and not mismatches and len(registros) == len(ref['cases'])
    if not ok:
        saida = RAIZ / '.local/consultas-trabalho' / f'falha-{time.strftime("%Y%m%dT%H%M%S")}.json'
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'w') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), comparisons=len(registros), mismatches=len(mismatches),
                          per_routine=por_rotina, reproduction=ex.ciclo.reproducao, seconds=segundos), indent=1))
    encerrar_captura(0 if ok else 2, saida)


def main():
    global ATE
    ap = argparse.ArgumentParser()
    ap.add_argument('--capturar', help='write the original-only capture here (relative to the repository)')
    ap.add_argument('--saida', default=str(RELATORIO.relative_to(RAIZ)))
    ap.add_argument('--ate', type=int, help='last frame counter (smoke runs only)')
    a = ap.parse_args()
    if a.ate:
        ATE = a.ate
    import emulador  # noqa: F401
    if a.capturar:
        capturar(RAIZ / a.capturar)
    else:
        validar(RAIZ / a.saida)


if __name__ == '__main__':
    main()
