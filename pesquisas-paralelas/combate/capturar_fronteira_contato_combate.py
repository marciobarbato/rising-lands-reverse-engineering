"""Original-only isolated callback boundary from the preserved native contact.

Unlike the first inventory, halt before the AI damage message. This exposes a
reproducible game-code boundary before the unresolved presentation import.
No game callee is replaced and no state byte is varied.
"""
import hashlib
import json
import lzma
from pathlib import Path

from bancada_combate_raid import BancadaCombateRaid
from delta_estado_missao import _decodificar

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'evidencias/captura-contato-alvo-incursao-original-v1.json.xz'
OUTPUT = HERE / 'evidencias/captura-fronteira-contato-original-v1.json'


def main():
    if OUTPUT.exists():
        raise SystemExit(f'Refusing to overwrite {OUTPUT}')
    original = json.loads(lzma.decompress(SOURCE.read_bytes()))
    records = []
    for source in original['calls']:
        state = {n: (int(v['base'], 16), _decodificar(v)) for n, v in source['full_state_before'].items()}
        b = BancadaCombateRaid(state)
        regs = {k: int(v, 16) for k, v in source['entry_registers'].items() if k != 'EIP'}
        record, _, _ = b.call(source['routine'], regs, words=source['stack_words'],
                              stops={0x4829c8: 'iagUnitSendMessage'})
        record.update(counter=source['counter'], phase=source['phase'],
                      actual_caller_return=source['actual_caller_return'])
        records.append(record)
    output = dict(schema='rising-lands/combat-contact-boundary-original/1',
                  translation_executed=False, original_sha256=original['original_sha256'],
                  source_artifact=str(SOURCE.relative_to(HERE)),
                  source_artifact_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), cases=records)
    OUTPUT.write_text(json.dumps(output, indent=1) + '\n')
    print(json.dumps([dict(routine=c['routine'], returned=c['reached_return'], stop=c['stop'],
                           fault=c['fault'], limit=c['limit']) for c in records]))
    return any(c['fault'] or c['limit'] or c['writes_outside_checkpoint'] for c in records)


if __name__ == '__main__':
    raise SystemExit(main())
