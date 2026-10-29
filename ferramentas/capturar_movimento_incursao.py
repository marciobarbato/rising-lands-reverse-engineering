"""Original-only isolated captures of the Core routines the raid reaches in counters 9000..9200 (M2.3).

Forced input, Combat's method (``pesquisas-paralelas/combate/capturar_vida_incursao_m2_3.py``):
- Missions' committed v1 path is rerun with their read-only bench: startup, MissionLoad, load_tail,
  between_frames.
- At frame 1's CalculGame entry u32 0x508f7c is written to 9000.
- Whole frames then run natively, with the real ProgIteration tail and window loop between them
  (``sondar_vida_incursao.BancadaVida``), so frame k runs with counter 8999+k.
- Every other byte is the original's own state.

Missions' ``Isolamento`` pauses at the Core routines below. Each paused call runs natively from its
exact saved entry state to its return (registers, changed bytes, bytes read before written), the
state is restored, and the frame resumes unchanged. Which calls are isolated:
- EnginNextEtape: the raid unit's (EAX = 16) and the first of every frame;
- SetEnginCollision / SetCollision / Chemin_ModifieZone: the first of every frame;
- every other listed routine: every call.

Volumes are from a probe of the same window. The run ends with ``encerrar_captura``, and
``read_before_write``/``changed_bytes`` use the lossless run encoding of
``compactar_captura_isolada``. No Python translation is imported.

    python3 -B ferramentas/capturar_movimento_incursao.py \
        --saida evidencias/fundacoes-quadro/captura-movimento-incursao-v1.json
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
CONTADOR, CONTADOR_FORCADO, UNIDADE_INCURSAO = 0x508f7c, 9000, 16
ROTINAS = ('EnginNextEtape', 'DeplaceEngin', 'AvanceEngin', 'CalculNextCase', 'CalculDirCase', 'CalculDirection',
           'RotateEngin', 'EnginNextCase', 'EnginOccupeCase', 'EnginPeutPasser', 'EnginEstVivant', 'SetDeplaceEngin',
           'ResetOrdre', 'ResetEnginCollision', 'ResetCollision', 'TerrainEnCollision', 'SetEnginCollision',
           'SetCollision', 'Chemin_ModifieZone', 'Distance2d', 'ChercheIndiceEngin', 'CheminCalcul',
           'Chemin_Verouille', 'OptimiseChemin', 'TestLigneOptimise', 'EnginNextCaseChemin', 'memset')
PRIMEIRA_POR_QUADRO = ('SetEnginCollision', 'SetCollision', 'Chemin_ModifieZone')


def escolher(nome, regs, ordem):
    """Whether the ``ordem``-th call of ``nome`` in this frame is isolated."""
    if nome == 'EnginNextEtape':
        return regs['EAX'] & 0xffff == UNIDADE_INCURSAO or ordem == 1
    if nome in PRIMEIRA_POR_QUADRO:
        return ordem == 1
    return True


def executar(quadros, observador=None, rotinas=ROTINAS, janelas=None):
    """``observador(nome, caso, antes, resultado)``, optional, after every isolated case (validators).
    ``janelas``: optional [(first counter, last counter)]; outside them no call is isolated (frames still run
    natively), inside them every call of ``rotinas`` is."""
    sys.path.insert(0, str(RAIZ / 'pesquisas-paralelas/missoes'))
    sys.path.insert(0, str(RAIZ / 'pesquisas-paralelas/combate'))
    import ambiente_missoes  # noqa: F401  (Missions bootstrap)
    import capturar_quadro_missao_original as cq
    from capturar_isolados_combate_quadro1 import CAPTURA
    from oraculo_quadro_missao import Isolamento
    from sondar_vida_incursao import BancadaVida
    cap = json.loads(CAPTURA.read_bytes())
    ni = cap['named_inputs']['m1']
    b = BancadaVida(cq.entradas_quadro(ni['allocation_fill'], ni['clock_ms'][0]), segundos=120)
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)

    class IsolamentoMovimento(Isolamento):
        def executar(self, regs):
            if self.quadro is None:         # frames 0/1 before the forced write: not isolated
                return
            nome = self.entradas[regs['EIP']]
            if janelas is not None:
                contador = struct.unpack('<I', self.b.cpu.mem_read(CONTADOR, 4))[0]
                if any(a <= contador <= z for a, z in janelas):
                    super().executar(regs)
                return
            chave = (nome, self.quadro)
            self.vistos[chave] = self.vistos.get(chave, 0) + 1
            if escolher(nome, regs, self.vistos[chave]):
                super().executar(regs)

    quadro_de = []
    def observar(nome, fase, caso, antes, resultado):
        quadro_de.append(iso.quadro)
        if observador is not None:
            observador(nome, caso, antes, resultado)

    iso = IsolamentoMovimento(b, rotinas, {'(no routine)': []}, observar)
    iso.vistos, iso.quadro = {}, None
    iso.instalar()
    b.executar_cauda_carga(600)
    b.executar_entre_quadros(120)
    if struct.unpack('<I', b.cpu.mem_read(CONTADOR, 4))[0] != 1:
        raise RuntimeError('Frame 1 must enter CalculGame with counter 1 before the forced write')
    b.cpu.mem_write(CONTADOR, struct.pack('<I', CONTADOR_FORCADO))
    resumo = []
    unidades = struct.unpack('<I', b.cpu.mem_read(0x4e19a0, 4))[0]
    for k in range(1, quadros + 1):
        if k > 1:
            b.executar_entre_quadros_k(120, k)
        contador = struct.unpack('<I', b.cpu.mem_read(CONTADOR, 4))[0]
        iso.quadro = k
        b.executar_quadro(300, k)
        resumo.append(dict(frame=k, counter=contador, raid_unit=bytes(b.cpu.mem_read(
            unidades + 0x114 * UNIDADE_INCURSAO, 0x114)).hex()))
    return b, cap, iso, quadro_de, resumo


def main():
    from compactar_captura_isolada import compactar, expandir
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--quadros', type=int, default=201, help='frames from counter 9000 (201 = up to 9200)')
    a = ap.parse_args()
    saida = RAIZ / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    revisao = subprocess.run(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    t0 = time.monotonic()
    try:
        b, cap, iso, quadro_de, resumo = executar(a.quadros)
    except Exception as erro:          # recorded under .local/raid with its traceback, exit 2
        import traceback
        falha = RAIZ / '.local/raid' / ('movimento-incursao-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
        falha.parent.mkdir(parents=True, exist_ok=True)
        with open(falha, 'x') as f:
            json.dump(dict(error=repr(erro), traceback=traceback.format_exc(), source_revision=revisao,
                           seconds=round(time.monotonic() - t0, 3)), f, indent=1)
        print(f'FAILED: {erro!r} -> {falha}', file=sys.stderr)
        encerrar_captura(2, falha)
    casos = [(r, c) for r in iso.registros for c in r['cases']]
    if len(casos) != len(quadro_de):
        raise RuntimeError('Observer and isolated case records disagree')
    chamadas = []
    for (r, c), quadro in zip(casos, quadro_de):
        chamadas.append(compactar(dict(routine=r['routine'], entry=r['entry'], frame=quadro,
                                       counter=8999 + quadro, caller=r['caller'], caller_return=r['caller_return'],
                                       **{k: c[k] for k in ('entry_registers', 'exit_registers', 'al',
                                                            'reached_return', 'changed_bytes', 'read_before_write')})))
    if [expandir(c)['read_before_write'] for c in chamadas] != [c['read_before_write'] for _, c in casos]:
        raise RuntimeError('Run encoding is not lossless for this capture')
    contagem, vistas = {}, {}
    for c in chamadas:
        contagem[c['routine']] = contagem.get(c['routine'], 0) + 1
    for (n, q), k in iso.vistos.items():
        vistas[n] = vistas.get(n, 0) + k
    relatorio = dict(
        schema='rising-lands/monde01-raid-movement-core-calls/1', original_sha256=HASH_ORIGINAL,
        translation_executed=False, source_revision=revisao, scenario='v1',
        label=f'forced input: v1 path, u32 0x508f7c = {CONTADOR_FORCADO} at frame 1\'s CalculGame entry, '
              f'{a.quadros} whole native frames (counters 9000..{8999 + a.quadros})',
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in (
            'ferramentas/capturar_movimento_incursao.py', 'pesquisas-paralelas/combate/sondar_vida_incursao.py',
            'pesquisas-paralelas/missoes/oraculo_quadro_missao.py')},
        routines={n: hex(b.sym[n]) for n in ROTINAS}, entries_seen=vistas, isolated_counts=contagem,
        selection='EnginNextEtape: EAX = 16 or the first of each frame; SetEnginCollision/SetCollision/'
                  'Chemin_ModifieZone: the first of each frame; every other routine: every call',
        frames=resumo, code_unchanged=b.sha256_codigo() == cap['code_integrity']['after'], calls=chamadas,
        encoding=dict(scheme='rising-lands/isolated-call-runs/1', decoder='ferramentas/compactar_captura_isolada.py:expandir'),
        method='Missions Isolamento: native call from the exact saved entry state to its stack return with local '
               'read/write hooks; the state is restored and the frame resumes',
        seconds=round(time.monotonic() - t0, 3))
    ok = relatorio['code_unchanged'] and all(c['reached_return'] for c in chamadas) and len(resumo) == a.quadros
    if not ok:
        saida = RAIZ / '.local/raid' / ('movimento-incursao-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=None, sort_keys=True, separators=(',', ':'))
        f.write('\n')
    print(json.dumps(dict(output=str(saida), isolated=contagem, seen=vistas, frames=len(resumo),
                          seconds=relatorio['seconds']), indent=1))
    encerrar_captura(0 if ok else 2, saida)


if __name__ == '__main__':
    main()
