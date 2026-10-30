"""Compare existing Combat behavior at the newly captured real fight boundary."""
import hashlib
import json
import lzma
from pathlib import Path

from ambiente_combate_raid import ROOT  # noqa: F401
from delta_estado_missao import _decodificar, aplicar, resumo
from validar_combate_raid import execute, arguments_equal

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'evidencias/captura-contato-alvo-incursao-original-v1.json.xz'
BOUNDARY = HERE / 'evidencias/captura-fronteira-contato-original-v1.json'


def comparar_contato():
    first = json.loads(lzma.decompress(SOURCE.read_bytes()))
    boundary = json.loads(BOUNDARY.read_bytes())
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != boundary['source_artifact_sha256']:
        raise ValueError('Original contact artifact hash mismatch')
    cases = []
    for source, native in zip(first['calls'], boundary['cases']):
        if source['routine'] != native['routine']:
            raise ValueError('Original contact case order mismatch')
        before = {n: (int(v['base'], 16), _decodificar(v)) for n, v in source['full_state_before'].items()}
        if resumo(before) != native['state_before']:
            raise ValueError('Original contact input hash mismatch')
        after = aplicar(before, native['delta'], native['routine'])
        if resumo(after) != native['state_after']:
            raise ValueError('Original contact output hash mismatch')
        actual, regs, checked, dependency = execute(native, before, audio=True)
        equal = actual == after
        differences = {k: [hex(regs[k]), native['exit_registers'][k]] for k in checked
                       if regs[k] != int(native['exit_registers'][k], 16)}
        dependency_equal = (dependency is None and native['reached_return']) or (
            dependency is not None and dependency['name'] == native['stop'] and arguments_equal(dependency, native))
        cases.append(dict(routine=native['routine'], counter=native['counter'],
                          whole_state_equal=equal, registers_compared=list(checked),
                          register_differences=differences, dependency=dependency,
                          dependency_equal=dependency_equal))
    if len(cases) != 2:
        raise ValueError('Expected exactly two original contact entries')
    return dict(schema='rising-lands/combat-contact-boundary-differential/1',
                summary=dict(cases=len(cases), mismatches=sum(not c['whole_state_equal'] or bool(c['register_differences']) or not c['dependency_equal'] for c in cases)),
                capture_sha256=hashlib.sha256(BOUNDARY.read_bytes()).hexdigest(), cases=cases)


if __name__ == '__main__':
    report = comparar_contato()
    out = HERE / 'validacao/fronteira-contato-local.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=1) + '\n')
    print(json.dumps(report['summary']))
    raise SystemExit(bool(report['summary']['mismatches']))
