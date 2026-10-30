"""Whole-state and full-register comparison of original turret input leaves."""
import argparse
import hashlib
import json
from pathlib import Path

from bancada_ordens_torres_combate import carregar_estados_torres
from bancada_combate_raid import BancadaCombateRaid
from delta_estado_missao import aplicar, resumo
from ordens_torres_combate import OrdensTorresCombate, REGISTERS
from validar_combate_raid import memory, serialize, write_state

HERE = Path(__file__).resolve().parent
CAPTURE = HERE / 'evidencias/captura-ordens-torres-original-v1.json'


class _WriteTrace:
    def __init__(self, memoria):
        self.m = memoria
        self.stores = []

    def __getattr__(self, name):
        underlying = getattr(self.m, name)
        if name not in ('u8', 'u16', 'u32'):
            return underlying
        width = {'u8': 1, 'u16': 2, 'u32': 4}[name]
        def access(address, value=None):
            if value is not None:
                self.stores.append((address, width, value & ((1 << (8 * width)) - 1)))
            return underlying(address, value)
        return access


def comparar(*, native=False):
    capture = json.loads(CAPTURE.read_bytes())
    states, pins = carregar_estados_torres()
    if pins != capture['state_provenance']:
        raise ValueError('Original state provenance mismatch')
    b = BancadaCombateRaid(next(iter(states.values()))) if native else None
    results = []
    for case in capture['cases']:
        before = write_state(states[case['state']], case['declared_writes'])
        if resumo(before) != case['state_before']:
            raise ValueError(f'Original input hash mismatch: {case["case"]}')
        after = aplicar(before, case['delta'], case['case'])
        if resumo(after) != case['state_after']:
            raise ValueError(f'Original output hash mismatch: {case["case"]}')
        regs = {k: int(v, 16) for k, v in case['entry_registers'].items()}
        expected = {k: int(v, 16) for k, v in case['exit_registers'].items()}
        native_errors = []
        if native:
            b.restore(before)
            original, _, fresh_after = b.call(case['routine'], {k: v for k, v in regs.items() if k != 'EIP'}, stops={})
            for key in ('exit_registers', 'state_after', 'stores'):
                if original[key] != case[key]:
                    native_errors.append(key)
            if not original['reached_return'] or original['fault'] or original['limit'] or original['writes_outside_checkpoint']:
                native_errors.append('native completion')
            if fresh_after != after:
                native_errors.append('whole native state')
        m, blocks = memory(before)
        traced = _WriteTrace(m)
        live = OrdensTorresCombate(traced)
        declared_return = int(case['entries'][0]['caller_return'], 16)
        actual = live.chamar(case['routine'], regs, retorno=declared_return)
        differences = {k: [hex(actual[k]), hex(expected[k])] for k in (*REGISTERS, 'ESP', 'EIP', 'EFLAGS') if actual[k] != expected[k]}
        whole_state_equal = serialize(blocks) == after
        store_order_equal = traced.stores == [(int(a, 16), size, int(value, 16)) for _, a, size, value in case['stores']]
        results.append(dict(case=case['case'], routine=case['routine'],
                            registers_compared=list(actual), register_differences=differences,
                            whole_state_equal=whole_state_equal, store_order_equal=store_order_equal, native_errors=native_errors))
    return dict(schema='rising-lands/combat-turret-orders-differential/1', native=native,
                capture_sha256=hashlib.sha256(CAPTURE.read_bytes()).hexdigest(),
                summary=dict(cases=len(results), mismatches=sum(bool(c['register_differences'] or not c['whole_state_equal'] or not c['store_order_equal'] or c['native_errors']) for c in results),
                             routines={n: sum(c['routine'] == n for c in results) for n in ('BatimentPeutAttaquer', 'BatimentInitAttaqueSelect')}),
                cases=results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emular', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = comparar(native=args.emular)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=1) + '\n')
    print(json.dumps(report['summary']))
    for c in report['cases']:
        if c['register_differences'] or not c['whole_state_equal'] or not c['store_order_equal'] or c['native_errors']:
            print(json.dumps(c))
    raise SystemExit(bool(report['summary']['mismatches']))
