"""Original raid-rule records plus perturbed live groups and task-VM comparisons.

Every callee runs real Rust/Python logic; native effects are never replayed as
callbacks. Frozen calls without outside providers also compare directly with Python. V_DeplaceGroupe uses real Rust movement providers. Movement
and whole-raid composition have their own original comparisons.
"""
from pinned_reference import activate, reference_file, pinned_file
SOURCE_ROOT = activate()

import ctypes as C
import hashlib
import importlib
import json
import random
import struct
import sys
import unittest
from pathlib import Path

from differential import ORIGINAL, declared_input, changed_bytes, expected_changes
from frame_abi import Frames
from pilot_abi import ROOT

CAPTURE = 'pesquisas-paralelas/ia-runtime/evidencias/captura-regras-incursao-9000-ia.json'
LATER_CAPTURE = 'pesquisas-paralelas/ia-runtime/evidencias/captura-regras-incursao-ia.json'
PINS = {'pesquisas-paralelas/ia-runtime/evidencias/captura-regras-incursao-9000-ia.json': 'cfa3095dcf26b26a02e41ed807d577a84d9f654fa0e70e79b934160fabbac204', 'pesquisas-paralelas/ia-runtime/incursao_ia.py': '2e6bc1cce71dcf589ce162902795e6dfd05ae99c607cf8e92840abcebb1cbffc', 'pesquisas-paralelas/ia-runtime/regras_incursao_ia.py': '35b14728659d305d792600106637fd0ed351e92ec70175b568d24f7851992a4c', 'ferramentas/tarefas_ia.py': 'c246e594c72307e3d2e726005bbe13e16c376fa81c82e4878d8cc066a6b4865d', 'ferramentas/incursao_core.py': '1f5fa0cd43247d83387aa8650de9edf0b8ccd356250df469953469e79ad5873b', 'ferramentas/simbolos_ia.py': '4f2525c345a21f3a89c4cfc10e1e82a31b1bc9ef84e5dc5bca3a4be3b2aabf7f', 'pesquisas-paralelas/ia-runtime/evidencias/captura-regras-incursao-ia.json': '46f827d6c10caa309c5c696809cfbd0d88a20a19f07c71a69186a6031e8ee081'}


class RaidTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for path, digest in PINS.items():
            if hashlib.sha256(pinned_file(ROOT / path).read_bytes()).hexdigest() != digest:
                raise ValueError('RaidReferenceIdentityMismatch: ' + path)
        for folder in ('ferramentas', 'pesquisas-paralelas/ia-runtime'):
            sys.path.insert(0, str(SOURCE_ROOT / folder))
        cls.raid = importlib.import_module('incursao_ia')
        cls.rules = importlib.import_module('regras_incursao_ia')
        cls.tasks = importlib.import_module('tarefas_ia')
        cls.symbols = importlib.import_module('simbolos_ia')
        cls.Memory = importlib.import_module('memoria_quadro_core').MemoriaQuadro
        cls.engine = Frames()
        cls.engine.lib.rl_executar_rotina_quadro.argtypes = [C.c_uint64, C.c_uint32, C.POINTER(C.c_uint32), C.c_uint32, C.POINTER(C.c_uint32)]
        cls.engine.lib.rl_executar_rotina_quadro.restype = C.c_int32

    def rust(self, identity, args, blocks):
        world = self.engine.create()
        try:
            self.engine.load(world, blocks)
            values = (C.c_uint32 * len(args))(*args)
            output = C.c_uint32()
            self.engine.check(self.engine.lib.rl_executar_rotina_quadro(world, identity, values, len(args), C.byref(output)))
            self.assertEqual(self.engine.clock(world), (0, 0))
            return output.value, sorted(self.engine.snapshot(world).items())
        finally:
            self.engine.free(world)

    def memory(self, blocks):
        buffers = [(a, bytearray(b)) for a, b in blocks]
        return self.Memory(buffers), buffers

    def test_twenty_five_frozen_original_rules_without_callback_replay(self):
        captures = [json.loads(pinned_file(ROOT / path).read_bytes()) for path in (CAPTURE, LATER_CAPTURE)]
        for capture in captures:
            self.assertEqual(capture['original_sha256'], ORIGINAL)
            self.assertFalse(capture['translation_executed'])
        count = 0
        for call in (call for capture in captures for call in capture['rule_calls']):
            case = dict(read_before_write=call['read_before_write'], changed_bytes=call['written_bytes'])
            before = declared_input(case)
            args = [int(v, 16) for v in call['arguments']]
            address = int(call['address'], 16)
            with self.subTest(rule=call['rule']):
                value, after = self.rust(409, [address, call['player'], call['task'], *args], before)
                self.assertEqual(value, int(call['exit']['EAX'], 16))
                self.assertEqual(changed_bytes(before, after), [v for v in expected_changes(case) if v[1] != v[2]])
                count += 1
                if call['outside_calls']:
                    continue  # real Rust providers above; Python world comparison is the whole-phase proof
                memory, buffers = self.memory(before)
                if call['rule'] in ('B_Superieur', 'B_Egalite', 'I_Soustraction'):
                    expected = self.tasks.MaquinaTarefas.executar_operacao(object.__new__(self.tasks.MaquinaTarefas), call['rule'], args, call['player'], call['task'])
                else:
                    expected = self.rules.REGRAS[call['rule']](memory, {}, args, call['player'], call['task'])
                self.assertEqual(value, expected & 0xffffffff)
                self.assertEqual(after, [(a, bytes(b)) for a, b in buffers])
        self.assertEqual(count, 25)

    def test_group_allocation_members_and_iterator_against_python(self):
        rng = random.Random(0x483bd8)
        for k in range(64):
            data = bytearray(rng.randbytes(0x523000 - 0x495000))
            def put(fmt, address, value): struct.pack_into(fmt, data, address - 0x495000, value)
            put('<I', 0x4e19a0, 0x60000000)
            put('<I', 0x51b660, k % 100)
            for i in range(100): put('<B', 0x51a9e0 + 32*i + 0x18, 1 if i < k % 100 + k % 3 else 0)
            pool = bytes(rng.randbytes(276 * 3))
            blocks = [(0x495000, bytes(data)), (0x60000000, pool)]
            memory, buffers = self.memory(blocks)
            expected = self.raid.novo_grupo(memory, 4, 16)
            value, after = self.rust(400, [4, 16], blocks)
            self.assertEqual(value, expected)
            self.assertEqual(after, [(a, bytes(b)) for a, b in buffers])
            if value == 0xffffffff:
                continue
            for member in (0, 2):
                blocks = after
                memory, buffers = self.memory(blocks)
                expected = self.raid.adicionar_ao_grupo(memory, value, member)
                _, after = self.rust(401, [value, member], blocks)
                self.assertEqual(after, [(a, bytes(b)) for a, b in buffers])
            blocks = after
            memory, buffers = self.memory(blocks)
            expected = self.raid.primeira_unidade(memory, value)
            result, after = self.rust(402, [value], blocks)
            self.assertEqual(result, expected)
            self.assertEqual(after, [(a, bytes(b)) for a, b in buffers])
            blocks = after
            memory, buffers = self.memory(blocks)
            expected = self.rules.proxima_unidade(memory)
            result, after = self.rust(403, [], blocks)
            self.assertEqual(result, expected)
            self.assertEqual(after, [(a, bytes(b)) for a, b in buffers])

    def test_task_vm_arithmetic_waits_children_and_lists_against_python(self):
        rng = random.Random(0x47d314)
        # Operation addresses are the original resolved RULE symbols. Each
        # synthetic program is represented both by Rust's actual memory table
        # and Python's immutable parser representation.
        operations = [('I_Addition', 0x4812ac), ('I_Soustraction', 0x4812b9),
                      ('I_Divise', 0x481302), ('I_PourcentageAB', 0x4812d0)]
        for k in range(64):
            opname, address = operations[k % len(operations)]
            child = k % 4 == 0
            wait = k % 4 == 1
            # 4: selected arithmetic -> variable 2; 5: compare -> terminate.
            # Child mode starts at6, invokes task type1, then waits for resume.
            instructions = [self.symbols.Instrucao('B_Bidon', 0, 1, 2, 0) for _ in range(7)]
            instructions[4] = self.symbols.Instrucao(opname, 0x122, 5, 3, rng.randrange(1, 1000))
            instructions[5] = self.symbols.Instrucao('V_Attendre' if wait else 'B_Superieur', 0x10 if wait else 0x220, 1, 2, 2 if wait else 0)
            instructions[6] = self.symbols.Instrucao(1, 0x110, 1, 2, 0)
            entries = (0, 4, 6)
            program = self.symbols.ProgramaRegras(0, 0, tuple(instructions), entries)
            base = self.tasks.MaquinaTarefas(program)
            base.postar(4, 2 if child else 1, (rng.randrange(1, 0x7fffffff),))
            state = bytearray(0x25e8)
            state[:9600] = base.memoria
            struct.pack_into('<4I', state, 0x5148a0 - 0x512320, base.livres[0] & 0xffffffff, base.livres[1], 96, 0x512320)
            for i, (head, count) in enumerate(base.contextos):
                struct.pack_into('<4I', state, 0x5148b0 - 0x512320 + 16*i, head & 0xffffffff, count, 96, 0x512320)
            struct.pack_into('<I', state, 0x514904 - 0x512320, base.ativas)
            table = bytearray(20 * len(instructions))
            resolved = {'B_Bidon':0x47f31c, 'B_Superieur':0x481296, 'V_Attendre':0x47da7a, opname:address}
            for i, instruction in enumerate(instructions):
                op = instruction.operacao if isinstance(instruction.operacao, int) else resolved[instruction.operacao]
                struct.pack_into('<5I', table, 20*i, op, instruction.formato, instruction.sucesso, instruction.falha, instruction.constante)
            blocks = [(0x496fe4, b'\x01'), (0x512320, bytes(state)), (0x514910, bytes(table)),
                      (0x51a720, struct.pack('<3H', *entries))]
            for _ in range(4):
                memory, buffers = self.memory(blocks)
                vm = self.tasks.MaquinaTarefasViva.sobre_memoria(program, memory)
                expected = vm.atualizar(4)
                result, after = self.rust(103, [0x5148f0], blocks)
                self.assertEqual(result, expected & 0xffffffff)
                self.assertEqual(after, [(a, bytes(b)) for a, b in buffers], (k, child, wait))
                blocks = after


if __name__ == '__main__':
    unittest.main()
