"""Bounded original fight calls with the established external profile binding.

All game bodies execute intact. Only KERNEL32.GetPrivateProfileStringA is
answered by Missions' media-backed PerfilWindows through Core's binding API.
Hooks record or halt; native code is never replaced by a translated callee.
"""
import hashlib
import json
import lzma
import struct
import time
from pathlib import Path

from bancada_combate_raid import BancadaCombateRaid
from delta_estado_missao import _decodificar, delta, resumo
from fronteiras_carga_missao import MidiaOriginal, PerfilWindows
from capturar_carga_missao_original import entradas

HERE = Path(__file__).resolve().parent
CONTACT = HERE / 'evidencias/captura-contato-alvo-incursao-original-v1.json.xz'


def estado_contato():
    raw = CONTACT.read_bytes()
    capture = json.loads(lzma.decompress(raw))
    source = capture['calls'][-1]
    state = {n: (int(v['base'], 16), _decodificar(v)) for n, v in source['full_state_before'].items()}
    return state, dict(artifact=str(CONTACT.relative_to(HERE)), sha256=hashlib.sha256(raw).hexdigest(),
                      routine=source['routine'], counter=source['counter'], summary=resumo(state),
                      scope='Staged original unit window from real M2.3 frame9000, before first damage; not S1/D1.')


class BancadaLutaFatal(BancadaCombateRaid):
    def __init__(self, state):
        super().__init__(state)
        self.media = MidiaOriginal(entradas(0xa7, 0x123456))
        self.profile = PerfilWindows(self.media)
        self.b.declarar_importacao(0x5231b0, 'KERNEL32.GetPrivateProfileStringA', 6, self.profile.texto)

    def call(self, name, registers, *, words=(), stops=None, seconds=5):
        stops = {} if stops is None else stops
        declared = self.b.vinculos_declarados
        regs = dict(EAX=0x13579bdf, EBX=0x2468ace0, ECX=0x31415926, EDX=0x27182818,
                    ESI=0x12345678, EDI=0x23456789, EBP=0x3456789a, ESP=self.stack + 0x8000, EFLAGS=2)
        regs.update(registers)
        self.cpu.mem_write(self.stack, bytes(65536))
        self.cpu.mem_write(regs['ESP'], struct.pack('<' + 'I' * (1 + len(words)), self.return_address, *words))
        for r, v in regs.items():
            self.cpu.reg_write(getattr(self.x86, 'UC_X86_REG_' + r), v & 0xffffffff)
        entry = self.symbols[name]
        self.cpu.reg_write(self.x86.UC_X86_REG_EIP, entry)
        before = self.snapshot()
        self.stores, self.entries, self.outside = [], [], []
        self.stops = set(stops) | set(declared.vinculos)
        self.stopped = None
        p0, e0 = len(self.profile.chamadas), len(declared.eventos)
        self.active = True
        started = time.monotonic(); address = entry; fault = None
        try:
            for _ in range(65):
                remaining = seconds - (time.monotonic() - started)
                if remaining <= 0:
                    break
                self.stopped = None
                self.cpu.emu_start(address, self.return_address, timeout=int(remaining * 1e6), count=2000000)
                result = self.registers()
                if result['EIP'] not in declared.vinculos:
                    break
                address = declared.invocar(result['EIP'])
            else:
                raise RuntimeError('65-segment external binding budget')
        except Exception as exc:
            fault = f'{type(exc).__name__}: {exc}'
        finally:
            self.active = False
        result = self.registers(); after = self.snapshot()
        record = dict(routine=name, entry_registers={k: hex(v) for k, v in dict(regs, EIP=entry).items()},
                      exit_registers={k: hex(v) for k, v in result.items()}, stack_words=list(words),
                      reached_return=result['EIP'] == self.return_address, stop=stops.get(result['EIP']), fault=fault,
                      limit=not fault and result['EIP'] != self.return_address and result['EIP'] not in stops,
                      state_before=resumo(before), state_after=resumo(after), delta=delta(before, after),
                      stores=self.stores, entries=self.entries, writes_outside_checkpoint=self.outside,
                      profile_calls=self.profile.chamadas[p0:], bindings=declared.eventos[e0:],
                      seconds=round(time.monotonic()-started, 4))
        return record, before, after


def json_bytes(value):
    if isinstance(value, bytes):
        return dict(bytes_hex=value.hex())
    raise TypeError(type(value).__name__)
