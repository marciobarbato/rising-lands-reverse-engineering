"""S1's Core gaps at their real call sites (native): capture original-first, then compare the translations.

``docs/core/S1_COVERAGE.md`` lists the Core routines S1 reaches with no native differential on main. This script
captures them in situ on the S1 trajectory itself (``bancada_s1``: Missions' scripted-input oracle resumed from an
S1 snapshot, every frame checked against the replay-checked S1 record) and, from the in-situ entry states, runs
declared variants of the original as leaf calls between frames (state restored afterwards, so the trajectory stays
S1's).

Windows (snapshot frame -> last frame) and routines:
- ``a`` 2250 -> 3200: ChercheVeget/ChercheGc (CalculWorkEngin 2352, 2407), ChercheGcLibre (3116), and the path
  search's TypeEnginPeutEcraser/IsIndirectlyBlocking/IsDirectlyBlocking (CheminCalcul/Chemin_Verouille from 2604);
- ``b`` 3250 -> 4450: ChercheVeget/ChercheGc (3384, 3424, 4396, 4423), ChercheGcLibre (4129, 4174);
- ``c`` 11250 -> 12500, the first fight: TerrainEstMontagne (EnginLigneDeTir, from 11741), BatimentGetCaseAdjacent
  (CalculAttaqueEngin, from 11860), ChercheCaseBatiment and GetCaseIndiceBatiment (11860), listDeleteElem and
  listUnlinkElem (iaSolver, 11500/11859/12460), iaProbReturnTo (11663...), VoixOffAsk (BatimentInfligeDegat, 12178).

``--capturar`` writes the original-only capture ``evidencias/lacunas-s1/captura-<w>.json.xz`` (no translation
imported). The default mode reruns natively, checks every case against that capture and compares
``buscas_bloqueios`` (windows a/b) or ``consultas_luta`` (c) over a copy of each case's exact entry state (stack page included, with the case's ESP):
EAX..EBP, ESP, every changed byte and the boundary calls (VoixOffAsk's two sound requests: arguments and pushed
word; the translation's ``som`` returns each boundary's declared EAX).

    python3 "…/heavy_lease.py" core -- python3 -B ferramentas/validar_lacunas_s1.py --janela a --capturar
    python3 "…/heavy_lease.py" core -- python3 -B ferramentas/validar_lacunas_s1.py --janela a
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
if str(RAIZ / 'ferramentas') not in sys.path:
    sys.path.insert(0, str(RAIZ / 'ferramentas'))

import bancada_s1 as bs  # noqa: E402

REGISTROS = bs.REGISTROS
M32 = 0xffffffff
JANELAS = {'a': (2250, 3200), 'b': (3250, 4450), 'c': (11250, 12500)}
BUSCAS = {'ChercheVeget': 0, 'ChercheGc': 0, 'ChercheGcLibre': 0, 'TypeEnginPeutEcraser': 0,
          'IsDirectlyBlocking': 0, 'IsIndirectlyBlocking': 0}
LUTA = {'TerrainEstMontagne': 0, 'BatimentGetCaseAdjacent': 0, 'ChercheCaseBatiment': 0, 'GetCaseIndiceBatiment': 0,
        'listDeleteElem': 0, 'listUnlinkElem': 0, 'iaProbReturnTo': 0, 'VoixOffAsk': 0}
ROTINAS = {'a': BUSCAS, 'b': BUSCAS, 'c': LUTA}          # routine -> RET immediate, per window
MAX_VARIANTES_POR_SITIO = 2           # in-situ entry states per (routine, caller) that seed declared variants
PONTEIRO_UNIDADES, PASSO = 0x4e19a0, 276
LARGURA, ALTURA = 0x497168, 0x49716a
PARADOS_PASSAM = 0x4e1771
FONTES = ('ferramentas/validar_lacunas_s1.py', 'ferramentas/bancada_s1.py', 'ferramentas/buscas_bloqueios.py',
          'ferramentas/consultas_luta.py', 'ferramentas/fadiga_vegetacao.py', 'ferramentas/chamadas_quadro_core.py',
          'ferramentas/incursao_core.py')


def captura_padrao(janela):
    return RAIZ / f'evidencias/lacunas-s1/captura-{janela}.json.xz'


def relatorio_padrao(janela):
    return RAIZ / f'relatorios/lacunas-s1-{janela}-emulada.json'


class Execucao:
    def __init__(self, janela, traduzir=None):
        self.janela, self.traduzir = janela, traduzir
        self.casos, self.pendentes, self.sitios = [], [], {}
        self.bancada = self.obs = None

    def registrar(self, caso, blocos):
        if self.traduzir is not None:
            caso['comparison'] = self.traduzir(caso, blocos)
        self.casos.append(caso)

    def fechar(self, caso, blocos):
        caso['label'] = f'{caso["routine"]} in situ from {caso["caller"]} (frame {caso["frame"]})'
        self.registrar(caso, blocos)
        chave = (caso['routine'], caso['caller_return'])
        if self.sitios.get(chave, 0) < MAX_VARIANTES_POR_SITIO:
            self.sitios[chave] = self.sitios.get(chave, 0) + 1
            regs = {k: int(caso['entry_registers'][k], 16) for k in REGISTROS}
            self.pendentes.append((caso['routine'], regs, blocos, caso['frame']))

    # -- declared variants, run between frames from a saved in-situ entry state
    def _rodar(self, rotina, regs, blocos, rotulo, quadro, escritas=()):
        b = self.bancada.b
        bs.restaurar(b, blocos)
        caso, antes = bs.folha(b, rotina, regs, (), escritas, rotulo, quadro)
        self.registrar(caso, antes)

    def _variantes(self, rotina, r0, blocos, quadro):
        b = self.bancada.b
        u16 = lambda a: struct.unpack('<H', bytes(b.cpu.mem_read(a, 2)))[0]
        larg, alt = u16(LARGURA), u16(ALTURA)
        cel = r0['EAX'] & 0xffff
        cantos = (('corner (0,0)', 0), ('corner (w-1,0)', larg - 1), ('corner (0,h-1)', (alt - 1) * 256),
                  ('corner (w-1,h-1)', (alt - 1) * 256 + larg - 1), ('left edge', (cel & 0xff00)),
                  ('top edge', cel & 0xff), ('right edge', (cel & 0xff00) + larg - 1))
        casos = []
        if rotina in ('ChercheVeget', 'ChercheGc', 'ChercheGcLibre'):
            casos += [(f'radius {r}', dict(EDX=r)) for r in (0, 1, 2, 3, 6, 12, 30)]
            casos += [(f'{n}, radius 8', dict(EAX=c, EDX=8)) for n, c in cantos]
            casos.append(('upper register bits', dict(EAX=0x5a5a0000 | cel, EDX=0x77770000 | (r0['EDX'] & 0xffff),
                                                      EBX=r0['EBX'] ^ 0x12340000, ECX=r0['ECX'] ^ 0xabcd0000)))
        if rotina == 'ChercheVeget':
            casos += [(f'bounds {lo:#x}..{hi:#x}, radius 10', dict(EBX=lo, ECX=hi, EDX=10))
                      for lo, hi in ((0x1e, 0x35), (0x43, 0x43), (1, 0xff), (0, 0), (0x35, 0x1e))]
        if rotina == 'ChercheGcLibre':
            base = struct.unpack('<I', bytes(b.cpu.mem_read(PONTEIRO_UNIDADES, 4)))[0]
            for u in range(11, 17):
                if u != r0['EBX'] & 0xffff and b.cpu.mem_read(base + PASSO * u + 1, 1)[0] in (0, 1, 2, 4, 5, 6, 7,
                                                                                              8, 9, 10):
                    casos.append((f'unit {u}, radius 6', dict(EBX=u, EDX=6)))
        if rotina in ('IsDirectlyBlocking', 'IsIndirectlyBlocking'):
            casos += [(f'direction {d}', dict(EDX=d)) for d in range(8)]
            casos.append(('direction with upper bits', dict(EDX=0x12345600 | (r0['EDX'] & 0xff))))
            casos.append(('stopped allies pass ([0x4e1771] = 1)', {}, [(PARADOS_PASSAM, b'\x01')]))
            casos.append(('stopped allies blocked ([0x4e1771] = 0)', {}, [(PARADOS_PASSAM, b'\x00')]))
            for u in range(11, 17):
                if u != r0['EAX']:
                    casos.append((f'occupant unit {u}', dict(EAX=u)))
        if rotina == 'TerrainEstMontagne':
            casos += [(f'cell {c:#x}', dict(EAX=(r0['EAX'] & 0xffff0000) | c))
                      for c in (0, cel ^ 1, (cel + 0x101) & 0xffff, (alt - 1) * 256 + larg - 1)]
            casos.append(('upper EAX bits', dict(EAX=0x13570000 | cel)))
        if rotina in ('BatimentGetCaseAdjacent', 'ChercheCaseBatiment'):
            alvo = r0['EDX'] if rotina == 'BatimentGetCaseAdjacent' else r0['EAX']
            for nome_c, d in (('cell - 1', -1), ('cell + 1', 1), ('cell - 256', -256), ('cell + 256', 256),
                              ('cell + 2', 2), ('cell - 514', -514), ('cell + 0x303', 0x303)):
                c = (alvo + d) & 0xffff
                casos.append((nome_c, dict(EDX=c) if rotina == 'BatimentGetCaseAdjacent' else dict(EAX=c)))
            casos += [(f'{n}', dict(EDX=c) if rotina == 'BatimentGetCaseAdjacent' else dict(EAX=c))
                      for n, c in cantos]
            casos.append(('upper register bits', dict(EAX=r0['EAX'] ^ 0x24680000, EDX=r0['EDX'] ^ 0x13570000)))
        if rotina == 'BatimentGetCaseAdjacent':
            casos += [(f'structure {i}', dict(EAX=i)) for i in (0, 1, 2, 3)]
        if rotina == 'GetCaseIndiceBatiment':
            # The pool has 1,000 records. The predecessor's 0x1234 variant faults in the original at
            # 0x41aac4 (outside mapped structure memory); it is not a supported query input.
            casos += [(f'structure {i}', dict(EAX=i)) for i in (0, 1, 2, 5, 999)]
        if rotina == 'VoixOffAsk':
            casos += [(f'DX = {k}', dict(EDX=(r0['EDX'] & 0xffff0000) | k)) for k in range(9)]
            casos.append(('BL and upper bits', dict(EBX=0x5a5a5a07, ECX=0x12345678)))
        if rotina == 'TypeEnginPeutEcraser':
            casos += [(f'type {t:#x}', dict(EAX=(r0['EAX'] & 0xffffff00) | t)) for t in range(0, 0x1b)]
            casos.append(('upper EAX bits', dict(EAX=0xdead0000 | (r0['EAX'] & 0xff))))
        for c in casos:
            rotulo, trocas = c[0], c[1]
            escritas = c[2] if len(c) > 2 else ()
            self._rodar(rotina, dict(r0, **trocas), blocos, f'{rotina} (frame {quadro} state): {rotulo}', quadro,
                        escritas)

    def processar_pendentes(self):
        if not self.pendentes:
            return
        b = self.bancada.b
        contexto, atual = b.cpu.context_save(), bs.imagem(b)
        self.obs.ativo = False
        try:
            for rotina, regs, blocos, quadro in self.pendentes:
                self._variantes(rotina, regs, blocos, quadro)
        finally:
            self.pendentes = []
            self.obs.ativo = True
            bs.restaurar(b, atual)
            b.cpu.context_restore(contexto)
        if bs.imagem(b) != atual:
            raise RuntimeError('the variants did not restore the state')

    def executar(self):
        de, ate = JANELAS[self.janela]
        t0 = time.monotonic()
        self.bancada = bs.BancadaS1(de)
        self.obs = bs.Observacao(self.bancada.b, ROTINAS[self.janela], ao_fechar=self.fechar)
        while self.bancada.k < ate:
            self.bancada.avancar(self.obs)
            self.processar_pendentes()
            if self.bancada.k % 100 == 0:
                print(f'frame {self.bancada.k} {time.monotonic() - t0:.0f}s cases {len(self.casos)}',
                      file=sys.stderr, flush=True)
        if self.obs.erros:
            raise RuntimeError(f'observation errors: {self.obs.erros[:4]}')
        return round(time.monotonic() - t0, 1)


# ------------------------------------------------------------------ translation comparison
def traduzir(caso, blocos):
    """``buscas_bloqueios`` (windows a/b) or ``consultas_luta`` (c) over a copy of the case's entry state against
    the native result."""
    from validar_fadiga_vegetacao import memoria_caso, mudancas
    m, copias = memoria_caso(blocos)          # a variant's entry blocks already hold its declared writes
    entrada = {k: int(caso['entry_registers'][k], 16) for k in REGISTROS}
    entrada['ESP'] = int(caso['esp'], 16)
    sons = []

    def som(nome, regs, pilha):
        i = len(sons)
        sons.append(dict(routine=nome, registers={k: hex(regs[k]) for k in ('EAX', 'EDX', 'EBX', 'ECX')},
                         pushed=[hex(w) for w in pilha]))
        if i >= len(caso['boundaries']):
            raise RuntimeError('a sound request the original did not make')
        declarado = caso['boundaries'][i]['declared_eax']
        return regs['EAX'] if declarado is None else declarado
    try:
        if caso['routine'] in BUSCAS:
            from buscas_bloqueios import BuscasBloqueios
            t = BuscasBloqueios(m)
        else:
            from consultas_luta import ConsultasLuta
            t = ConsultasLuta(m, som=som)
        saida = t.chamar(caso['routine'], entrada, [int(w, 16) for w in caso['stack_args']])
    except Exception as erro:                 # a mismatch, never ignored
        return dict(ok=False, python_error=f'{type(erro).__name__}: {erro}')
    incertos = saida.get('_incertos') or {}
    nativos = {k: int(caso['exit_registers'][k], 16) for k in REGISTROS + ('ESP',)}
    dif = {k: [hex(saida[k]), hex(nativos[k])] for k in REGISTROS + ('ESP',) if (saida[k] ^ nativos[k]) & M32}
    py = mudancas(blocos, copias)
    sons_nativos = [dict(routine=e['routine'], registers={k: e['registers'][k] for k in ('EAX', 'EDX', 'EBX', 'ECX')},
                         pushed=e['stack_words'][:1 if e['routine'] == 'PlaySnd_PostSound' else 0])
                    for e in caso['boundaries']]
    ok = not dif and py == caso['changed_bytes'] and sons == sons_nativos and not incertos
    r = dict(ok=ok, register_differences=dif, changed_equal=py == caso['changed_bytes'],
             native_changed=len(caso['changed_bytes']), sounds_equal=sons == sons_nativos,
             uncertain_bits={k: hex(v) for k, v in incertos.items() if v})
    if sons != sons_nativos:
        r.update(python_sounds=sons, native_sounds=sons_nativos)
    if py != caso['changed_bytes']:
        r.update(python_only=py[:16], native_only=caso['changed_bytes'][:16])
    return r


def _sem_comparacao(caso):
    return {k: v for k, v in caso.items() if k != 'comparison'}


def resumo(casos):
    saida = {}
    for c in casos:
        s = saida.setdefault(c['routine'], dict(cases=0, in_situ=0, variants=0, frames=[]))
        s['cases'] += 1
        s['in_situ' if c['kind'] == 'in_situ' else 'variants'] += 1
        if c['kind'] == 'in_situ' and c['frame'] not in s['frames']:
            s['frames'].append(c['frame'])
    return saida


def _revisao():
    return subprocess.run(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()


def capturar(janela, saida):
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    ex = Execucao(janela)
    segundos = ex.executar()
    if 'buscas_bloqueios' in sys.modules or 'consultas_luta' in sys.modules:
        raise RuntimeError('The capture imported the translation')
    dados = dict(schema='rising-lands/core-s1-gaps-capture/1', original_sha256=HASH_ORIGINAL,
                 translation_executed=False, window=janela, frames=list(JANELAS[janela]),
                 s1=dict(revision=bs.S1_REV, records=bs.S1_QUADROS), source_revision=_revisao(),
                 capture_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 reproduction=ex.bancada.reproducao(), seconds=segundos, summary=resumo(ex.casos), cases=ex.casos)
    saida.parent.mkdir(parents=True, exist_ok=True)
    bruto = (json.dumps(dados, sort_keys=True) + '\n').encode()
    saida.write_bytes(lzma.compress(bruto, preset=9))
    print(json.dumps(dict(output=str(saida), raw_sha256=hashlib.sha256(bruto).hexdigest(),
                          reproduction=dados['reproduction'], summary=dados['summary'], seconds=segundos), indent=1))
    encerrar_captura(0, saida)


def validar(janela, captura, saida):
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    ref = json.loads(lzma.decompress(captura.read_bytes()))
    ex = Execucao(janela, traduzir=traduzir)
    segundos = ex.executar()
    registros, mismatches = [], []
    for i, caso in enumerate(ex.casos):
        cmp = caso['comparison']
        cmp['native_equals_capture'] = i < len(ref['cases']) and ref['cases'][i] == _sem_comparacao(caso)
        cmp['ok'] = cmp['ok'] and cmp['native_equals_capture']
        r = dict(routine=caso['routine'], label=caso['label'], kind=caso['kind'], frame=caso['frame'], **cmp)
        registros.append(r)
        if not r['ok']:
            mismatches.append(r)
    por_rotina = {}
    for r in registros:
        p = por_rotina.setdefault(r['routine'], dict(cases=0, mismatches=0))
        p['cases'] += 1
        p['mismatches'] += int(not r['ok'])
    reproducao = ex.bancada.reproducao()
    relatorio = dict(
        schema='rising-lands/core-s1-gaps-differential/1', original_sha256=HASH_ORIGINAL, window=janela,
        frames=list(JANELAS[janela]), capture=dict(path=str(captura.relative_to(RAIZ)),
                                                   sha256=hashlib.sha256(captura.read_bytes()).hexdigest()),
        source_revision=_revisao(),
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in FONTES},
        reproduction=reproducao, comparisons=len(registros), capture_cases=len(ref['cases']), by_routine=por_rotina,
        mismatches=mismatches, cases=registros, seconds=segundos)
    ok = reproducao['code_unchanged'] and not mismatches and len(registros) == len(ref['cases'])
    if not ok:
        saida = RAIZ / '.local/lacunas-s1' / f'falha-{janela}-{time.strftime("%Y%m%dT%H%M%S")}.json'
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'w') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), comparisons=len(registros), mismatches=len(mismatches),
                          by_routine=por_rotina, reproduction=reproducao, seconds=segundos), indent=1))
    encerrar_captura(0 if ok else 2, saida)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--janela', choices=sorted(JANELAS), required=True)
    ap.add_argument('--capturar', action='store_true', help='write the original-only capture')
    ap.add_argument('--captura', help='capture to compare with (default evidencias/lacunas-s1/captura-<w>.json.xz)')
    ap.add_argument('--saida', help='report path (default relatorios/lacunas-s1-<w>-emulada.json)')
    ap.add_argument('--ate', type=int, help='last frame (smoke runs only)')
    a = ap.parse_args()
    if a.ate:
        JANELAS[a.janela] = (JANELAS[a.janela][0], a.ate)
    import emulador  # noqa: F401  (puts .local/python, with unicorn, on sys.path)
    if a.capturar:
        capturar(a.janela, RAIZ / a.captura if a.captura else captura_padrao(a.janela))
    else:
        validar(a.janela, RAIZ / a.captura if a.captura else captura_padrao(a.janela),
                RAIZ / a.saida if a.saida else relatorio_padrao(a.janela))


if __name__ == '__main__':
    main()
