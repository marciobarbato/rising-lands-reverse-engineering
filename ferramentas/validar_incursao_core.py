"""Native differential of the raid-frame Core translations at the forced first-raid states (M2.3).

Reruns ``capturar_incursao_core`` (Missions' committed frame path, read-only
``Isolamento`` on AvanceMonstre, the same declared forced cases) with a
recorder that, at every nested Core call, also runs the Python translation
(``incursao_core.traducao_core``). The translation runs over a copy-on-write
view of the live CPU memory at that exact entry state. When the native call
returns, the translation's registers EAX..EBP and its changed bytes are
compared with the original's (stack excluded). A ``DependenciaRamoCore`` is
recorded as a dependency stop. Any other Python exception is recorded as a
mismatch. The native run is never altered.

    python3 -B ferramentas/validar_incursao_core.py --cenario v1
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
M32 = 0xffffffff


class MemoriaCPU:
    """Flat memory over the live engine: reads see this view's own stores first; stores never reach it."""
    def __init__(self, cpu):
        self.cpu, self.escritas = cpu, {}

    def _byte(self, a):
        a &= M32
        return self.escritas[a] if a in self.escritas else self.cpu.mem_read(a, 1)[0]

    def _acesso(self, n, a, valor):
        if valor is None:
            return int.from_bytes(bytes(self._byte(a + i) for i in range(n)), 'little')
        valor &= (1 << 8 * n) - 1
        for i in range(n):
            self.escritas[(a + i) & M32] = valor >> 8 * i & 0xff
        return valor

    def u8(self, a, v=None):
        return self._acesso(1, a, v)

    def u16(self, a, v=None):
        return self._acesso(2, a, v)

    def u32(self, a, v=None):
        return self._acesso(4, a, v)

    def ler(self, a, n):
        return bytes(self._byte(a + i) for i in range(n))

    def mudancas(self):
        saida = []
        for a in sorted(self.escritas):
            velho = self.cpu.mem_read(a, 1)[0]
            if velho != self.escritas[a]:
                saida.append([hex(a), velho, self.escritas[a]])
        return saida


def main():
    import capturar_incursao_core as ci
    from chamadas_quadro_core import DependenciaRamoCore
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    from incursao_core import traducao_core
    from integracao.providers import load_economy_bonus
    ap = argparse.ArgumentParser()
    ap.add_argument('--cenario', choices=('exibicao', 'v1'), required=True)
    ap.add_argument('--saida')
    ap.add_argument('--casos', type=int, help='first N forced cases only (smoke run, output under .local/)')
    a = ap.parse_args()
    saida = RAIZ / (a.saida or f'relatorios/incursao-core-{a.cenario}-emulada.json')
    if a.casos is not None and not str(saida.relative_to(RAIZ)).startswith('.local/'):
        raise SystemExit('A --casos smoke run writes under .local/ only')
    classe = load_economy_bonus().BonusUnidades
    registro = dict(comparisons=0, by_routine={}, mismatches=[], dependencies=[], untranslated={})

    def bonus_de(m):
        tabela = classe.vivo(bytearray(m.ler(0x4dfba0, 1872)), tipos_unidades=bytearray(m.ler(0x4965ae, 1300)))
        return lambda jogador, tipo, seletor: tabela.consultar(jogador, tipo, seletor)

    class GravadorDiferencial(ci.Gravador):
        def _entrada(self, cpu, endereco, tamanho, _):
            super()._entrada(cpu, endereco, tamanho, _)
            f = self.pilha[-1]
            traduzir = traducao_core(f['routine'])
            if traduzir is None:
                registro['untranslated'][f['routine']] = registro['untranslated'].get(f['routine'], 0) + 1
                f['python'] = None
                return
            m = MemoriaCPU(cpu)
            try:
                regs = dict(f['regs'], **traduzir(m, f['regs'], list(f['stack']), bonus_de(m)))
                f['python'] = dict(registers=regs, changed=m.mudancas())
            except DependenciaRamoCore as e:
                f['python'] = dict(dependency=hex(e.endereco), reason=str(e))
            except Exception as e:      # recorded as a failing comparison, never ignored
                f['python'] = dict(error=f'{type(e).__name__}: {e}')

        def _fechar(self, cpu, f):
            super()._fechar(cpu, f)
            py = f.get('python')
            if py is None:
                return
            nativo = self.chamadas[f['index']]
            chave = dict(routine=f['routine'], case=self.caso, index=f['index'])
            if 'dependency' in py:
                registro['dependencies'].append(dict(chave, address=py['dependency'], reason=py['reason']))
                return
            registro['comparisons'] += 1
            registro['by_routine'][f['routine']] = registro['by_routine'].get(f['routine'], 0) + 1
            if 'error' in py:
                registro['mismatches'].append(dict(chave, python_error=py['error']))
                return
            exit_nativo = {k: int(v, 16) for k, v in nativo['exit_registers'].items()}
            iguais_regs = all(py['registers'][k] & M32 == exit_nativo[k] for k in REGISTROS)
            if not iguais_regs or py['changed'] != nativo['changed_bytes'] or not nativo['reached_return']:
                registro['mismatches'].append(dict(
                    chave, python_registers={k: hex(py['registers'][k] & M32) for k in REGISTROS},
                    native_registers={k: hex(exit_nativo[k]) for k in REGISTROS},
                    python_changed=py['changed'][:24], native_changed=nativo['changed_bytes'][:24]))

    ci.Gravador = GravadorDiferencial          # the capture run, with the comparing recorder
    t0 = time.monotonic()
    b, iso, gravador, reproducao = ci.executar(a.cenario, a.casos)
    registro.update(
        schema='rising-lands/monde01-raid-core-differential/1', original_sha256=HASH_ORIGINAL,
        scenario=a.cenario, path_reproduction=reproducao, forced_cases=[c['case'] for c in ci.casos_forcados(a.casos)],
        native_calls=len(gravador.chamadas),
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in (
            'ferramentas/incursao_core.py', 'ferramentas/chamadas_quadro_core.py',
            'ferramentas/validar_incursao_core.py', 'ferramentas/capturar_incursao_core.py')},
        seconds=round(time.monotonic() - t0, 3))
    ok = (all(reproducao.values()) and not registro['mismatches'] and not registro['dependencies']
          and not registro['untranslated'] and all(c is not None and c['reached_return'] for c in gravador.chamadas))
    if not ok:
        saida = RAIZ / '.local/raid' / f'incursao-core-{a.cenario}-falha-{time.strftime("%Y%m%dT%H%M%S")}.json'
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(registro, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps({k: registro[k] for k in ('comparisons', 'by_routine', 'path_reproduction', 'native_calls',
                                               'untranslated', 'seconds')}
                     | dict(mismatches=len(registro['mismatches']), dependencies=len(registro['dependencies']),
                            output=str(saida)), indent=1))
    encerrar_captura(0 if ok else 2, saida)


if __name__ == '__main__':
    main()
