"""Consumer register completeness and the explicitly projected sack query."""
import json
from pathlib import Path
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
import ambiente_ia_runtime  # noqa: F401
from capturar_mensagem_cidade_ia import MemoriaCapturada
from entrada_estruturas import ArgumentoNaoPassado
from provedores_entrada_ia import DonosM3, REG7


class NoMemory:
    def __getattr__(self, name):
        raise AssertionError(f'Unexpected memory access: {name}')


class Routes(unittest.TestCase):
    def test_every_register_required_before_memory(self):
        d = DonosM3(NoMemory(), som=None)
        for name in d._economia_s1:
            for missing in REG7:
                with self.subTest(routine=name, missing=missing):
                    with self.assertRaises(ArgumentoNaoPassado) as e:
                        d.externo(name, 0x4299da, {k: i for i, k in enumerate(REG7) if k != missing})
                    self.assertEqual(e.exception.registradores, (missing,))

    def test_real_sack_call_and_projected_query(self):
        c = json.loads((OWNED/'evidencias/s1-parada-saco-original.json').read_text())['cases'][0]
        m = MemoriaCapturada(c['read_before_write'])
        d = DonosM3(m, som=None)
        regs = {k: int(v, 16) for k, v in c['entry_registers'].items()}
        out = d.externo('SacGetCapacite', 0x4299da, regs)
        self.assertEqual(out, {k: int(c['exit_registers'][k], 16) for k in REG7})
        self.assertEqual(d.capacidade_saco(regs['EAX']), out['EAX'])
        regs['_incertos'] = dict(EDX=0xffffffff)
        self.assertEqual(d.externo('SacGetCapacite', 0x4299da, regs)['_incertos'], regs['_incertos'])
        self.assertFalse(m.escritos)

    def test_uncertain_behavior_rejected_and_x87_metadata_preserved(self):
        d = DonosM3(NoMemory(), som=None)
        regs = dict.fromkeys(REG7, 0)
        with self.assertRaises(ArgumentoNaoPassado):
            d.externo('SacGetCapacite', 0x4299da, dict(regs, _incertos=dict(EAX=1)))
        # Negative zero: the owned route must retain the exact owner's push.
        m = MemoriaCapturada([['0x5080fc', '0000000000000080']])
        d = DonosM3(m, som=None)
        out = d.externo('RechercheGetEtat', 0x42ca00, regs)
        self.assertEqual(out['_x87_push'], (0, 0x8000))
        self.assertFalse(m.escritos)


if __name__ == '__main__':
    unittest.main()
