"""Strict register boundary shared by the bounded fatal-fight providers."""
from ambiente_combate_raid import ROOT  # noqa: F401
from entrada_estruturas import ArgumentoNaoPassado

REG7 = ('EAX','EBX','ECX','EDX','ESI','EDI','EBP')
M32 = 0xffffffff


class DependenciaLutaFatal(NotImplementedError):
    def __init__(self, nome, endereco, argumentos=()):
        self.nome, self.endereco, self.argumentos = nome, endereco, tuple(argumentos)
        super().__init__(f'{nome} required at 0x{endereco:08x}{self.argumentos}; earlier effects retained')


def registradores_exigidos(nome, endereco, regs):
    missing = [r for r in REG7 if r not in regs]
    if missing:
        raise ArgumentoNaoPassado(nome, endereco, missing)
    return {r: regs[r] & M32 for r in REG7}


def assinado(value, bits=32):
    value &= (1 << bits)-1
    return value-(1 << bits) if value & (1 << (bits-1)) else value


def unidade(m, index):
    index &= 65535
    if index >= 800:
        raise ValueError('Protected fight unit index requires 0..799')
    return m.u32(0x4e19a0)+276*index
