"""Consumer routing: Core's actual query/search providers retain their distinct register contracts."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ambiente_ia_runtime  # noqa: E402,F401
from entrada_ordens_ia import REG7  # noqa: E402
from provedores_entrada_ia import DonosM3  # noqa: E402
from reinicio_ia import DependenciaIA  # noqa: E402


class Memoria:
    def __init__(self):
        self.bytes, self.reads = {}, []

    def _access(self, a, size, value):
        if value is None:
            self.reads.append((a, size))
            return sum(self.bytes[a + i] << (8 * i) for i in range(size))
        for i in range(size):
            self.bytes[a + i] = value >> (8 * i) & 255

    def u8(self, a, value=None):
        return self._access(a, 1, value)

    def u16(self, a, value=None):
        return self._access(a, 2, value)

    def u32(self, a, value=None):
        return self._access(a, 4, value)


class ContratosConsumidor(unittest.TestCase):
    def setUp(self):
        self.m = Memoria()
        self.d = DonosM3(self.m, som=None)
        self.regs = {k: 0x12340000 + i for i, k in enumerate(REG7)}

    def test_query_preserves_every_carried_register(self):
        self.m.u32(0x4e19a0, 0x2000000)
        self.m.u8(0x2000000 + 276 * 15 + 2, 7)
        regs = dict(self.regs, EAX=0xabcd000f)
        before = dict(self.m.bytes)
        self.assertEqual(self.d.externo('EnginEstVivant', 0x4731d3, regs), dict(regs, EAX=1))
        self.assertEqual(self.m.bytes, before)

    def test_query_missing_preserved_register_stops_before_read(self):
        with self.assertRaisesRegex(DependenciaIA, 'EnginEstVivant.*Core.*EBX'):
            self.d.externo('EnginEstVivant', 0x4731d3, {'EAX': 15})
        self.assertEqual(self.m.reads, [])

    def test_argument_only_search_marks_unknown_preserved_registers(self):
        self.m.u32(0x507d74, 0x3000000)
        self.m.u16(0x497168, 2)
        self.m.u16(0x49716a, 2)
        self.m.u8(0x3000000, 0x1e)
        before = dict(self.m.bytes)
        result = self.d.externo('ChercheGc', 0x44db70, dict(EAX=0, EDX=5))
        self.assertEqual(result['EAX'], 0)
        for k in ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'):
            self.assertEqual(result['_incertos'][k], 0xffffffff)
        self.assertEqual(self.m.bytes, before)

    def test_stack_dependent_query_refuses_missing_or_nominal_esp(self):
        for extra in ({}, {'ESP': 0}):
            with self.subTest(extra=extra), self.assertRaisesRegex(DependenciaIA, 'actual readable entry ESP'):
                self.d.externo('BatimentGetCaseAdjacent', 0x453abc, dict(self.regs, **extra))
        self.assertEqual(self.m.reads, [])


if __name__ == '__main__':
    unittest.main()
