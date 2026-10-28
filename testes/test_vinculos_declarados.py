"""Small CPU-independent checks of the external-binding protocol, not an x86 oracle."""
import struct
import unittest

from vinculos_declarados import (ArgumentoVinculo, RetornoVinculo, RegistroVinculosDeclarados,
                                 ParadaVinculoDeclarado, GPRS, importacoes_pe)


class CPURegistro:
    def __init__(self):
        self.memoria = bytearray(4096)
        self.regs = {n: 0xabc00000+i for i, n in enumerate(GPRS)}
        self.regs.update(ESP=0x100, EIP=0x400, EFLAGS=0x202)
        struct.pack_into('<III', self.memoria, 0x100, 0x222, 0xffffffff, 0x87654321)

    def reg_read(self, nome): return self.regs[nome]
    def reg_write(self, nome, valor): self.regs[nome] = valor
    def mem_read(self, endereco, tamanho): return self.memoria[endereco:endereco+tamanho]
    def mem_write(self, endereco, dados): self.memoria[endereco:endereco+len(dados)] = dados


class VinculosDeclarados(unittest.TestCase):
    def test_only_actual_intact_pe_import_metadata_defines_iat_slots(self):
        from pathlib import Path
        root = Path(__file__).resolve().parents[1]
        dados = (root.parent/'source/cd/INSTALHD/RISING.EXE').read_bytes()
        slots = importacoes_pe(dados, 0x400000)
        self.assertEqual(slots[0x5231c0]['symbol'], 'GlobalAlloc')
        self.assertEqual(slots[0x5231d0]['symbol'], 'GlobalLock')
        self.assertEqual(slots[0x5231b8]['symbol'], 'GetTickCount')
        self.assertNotIn(0x4e19a0, slots)

    def preparar(self):
        cpu = CPURegistro()
        registro = RegistroVinculosDeclarados(cpu, {n: n for n in cpu.regs}, codigo_protegido=((0x500, 0x600),))
        return cpu, registro

    def test_exact_argument_widths_callee_pop_results_and_preserved_registers(self):
        cpu, r = self.preparar()
        antes = dict(cpu.regs)
        def atender(c):
            self.assertEqual(c.argumentos, (antes['EDX'] & 255, -1, 0x4321))
            self.assertEqual(c.retorno, 0x222)
            self.assertEqual(c.ler(0x108, 4), bytes.fromhex('21436587'))
            with self.assertRaises(TypeError): c.registradores['ECX'] = 0
            c.escrever(0x300, b'data')
            return RetornoVinculo(-1, {'EDX': 0x100000002})
        r.declarar(0x400, 'Fixture', (ArgumentoVinculo('EDX', 8), ArgumentoVinculo(4, 32, True),
                                     ArgumentoVinculo(8, 16)), atender, desempilhar=8, natureza='importacao')
        self.assertEqual(r.invocar(0x400), 0x222)
        self.assertEqual(cpu.regs, {**antes, 'EAX': 0xffffffff, 'EDX': 2, 'ESP': 0x10c, 'EIP': 0x222})
        self.assertEqual(cpu.memoria[0x300:0x304], b'data')
        self.assertEqual((r.eventos[0]['status'], r.eventos[0]['memory_writes'][0]['size']), ('returned', 4))

    def test_register_abi_pops_only_return_and_preserves_caller_stack_arguments(self):
        cpu, r = self.preparar()
        r.declarar(0x400, 'CRT_IO', ('EAX', 'EDX'), lambda c: 7, natureza='io')
        r.invocar(0x400)
        self.assertEqual((cpu.regs['ESP'], cpu.regs['EIP'], cpu.regs['EAX']), (0x104, 0x222, 7))
        self.assertEqual(struct.unpack_from('<I', cpu.memoria, 0x104)[0], 0xffffffff)

    def test_explicit_stop_preserves_prior_fixture_writes_and_native_frame(self):
        cpu, r = self.preparar()
        antes = dict(cpu.regs)
        def parar(c):
            c.escrever(0x300, b'prior')
            raise ParadaVinculoDeclarado('Declared fixture exhausted')
        r.declarar(0x400, 'Exhausted', (), parar, natureza='backend')
        with self.assertRaisesRegex(ParadaVinculoDeclarado, 'exhausted'): r.invocar(0x400)
        self.assertEqual(cpu.regs, antes)
        self.assertEqual(cpu.memoria[0x300:0x305], b'prior')
        self.assertEqual(r.eventos[0]['status'], 'stopped')

    def test_none_and_invalid_register_results_are_errors_without_fabricated_success(self):
        for resposta in (None, RetornoVinculo(1, {'ESP': 0}), RetornoVinculo(1, {'EAX': 2})):
            cpu, r = self.preparar(); antes = dict(cpu.regs)
            r.declarar(0x400, 'Invalid', (), lambda c: resposta, natureza='backend')
            with self.assertRaises(ValueError): r.invocar(0x400)
            self.assertEqual(cpu.regs, antes)
            self.assertEqual(r.eventos[0]['status'], 'error')

    def test_binding_write_cannot_patch_original_code(self):
        cpu, r = self.preparar()
        def atender(c):
            c.escrever(0x500, b'\xc3')
            return 0
        r.declarar(0x400, 'NoPatch', (), atender, natureza='io')
        with self.assertRaisesRegex(ValueError, 'instructions'): r.invocar(0x400)
        self.assertEqual(cpu.memoria[0x500], 0)
        self.assertEqual(r.eventos[0]['memory_writes'], [])

    def test_invalid_duplicate_or_unknown_bindings_fail_before_registration(self):
        _, r = self.preparar()
        for args in ((ArgumentoVinculo('EAX', 7),), ('ESP',), (0,), (6,)):
            with self.assertRaises(ValueError): r.declarar(0x400, 'Invalid', args, lambda c: 0, natureza='io')
        with self.assertRaises(ValueError): r.declarar(0x400, 'Missing', (), None, natureza='io')
        with self.assertRaises(ValueError): r.declarar(0x400, 'Engine', (), lambda c: 0, natureza='engine')
        self.assertEqual(r.vinculos, {})
        r.declarar(0x400, 'First', (), lambda c: 0, natureza='relogio')
        with self.assertRaises(ValueError): r.declarar(0x400, 'Duplicate', (), lambda c: 1, natureza='relogio')
