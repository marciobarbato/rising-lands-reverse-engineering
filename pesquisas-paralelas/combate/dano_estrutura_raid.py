"""BatimentInfligeDegat 0x41a2c1 over live original structure/global memory.

Original-first matrix: capture-combate-raid-original-v1.json, committed 4d4e2f4.
The caller owns all query/effect providers. No structure removal is performed;
this routine accumulates damage and marks destruction in the original order.
"""


class DanoEstruturaRaid:
    def __init__(self, memoria, consultar, efetuar):
        self.m, self.consultar, self.efetuar = memoria, consultar, efetuar

    def infligir(self, indice, dano, dono_fonte):
        """AX target:u16, full EDX damage:u32, BL owner:u8; returns clobbered registers.

        Nonlethal EAX/EBX/EDX are exact. On destruction, foreign providers may
        return their clobbered register dict; EBX is needed only by the full
        register API if no final VoixOffAsk overwrites it. A void consumer does
        not consume those registers. Missing effects raise in the supplied
        provider and retain earlier stores.
        """
        m = self.m
        indice, dano, dono_fonte = indice & 65535, dano & 0xffffffff, dono_fonte & 255
        if indice >= 1000:
            raise ValueError('Structure ID is outside the original 1000-record pool')
        rec = 0x49a0c8 + 276 * indice
        m.u16(rec + 6, m.u16(rec + 6) + dano)
        if m.u8(rec + 4) == m.u8(0x508041):
            volume = self.consultar('BatimentGetVolume', (indice,)) & 0xffffffff
            if m.u32(rec + 0x100) == 0xffffffff:
                self.efetuar('PlaySnd_PostSound', (0x42, (m.u8(rec + 8) << 16) | 0x100,
                                                    0, volume, rec + 0x100))
        if m.u8(rec + 4) == m.u8(0x508041) and m.u8(0x4dfb9b) == 0:
            self.efetuar('VoixOffAsk', (1, 3, 0))
            m.u8(0x4dfb9b, 1)
        kind = m.u8(rec + 8)
        if kind >= 22:
            raise ValueError('Structure characteristic type is outside 0..21')
        maximum = m.u16(0x495d90 + 52 * kind)
        if maximum == 0:
            raise ZeroDivisionError('Original BatimentInfligeDegat IDIV by zero after accumulated-damage store')
        scaled = 200 * m.u16(rec + 6) // maximum
        limit, remainder = divmod(200 * m.u16(rec + 0xa), maximum)
        if (limit & 65535) >= (scaled & 65535):
            return dict(EAX=limit, EBX=maximum, EDX=remainder)
        # ESI and ECX refer to the same stable live record at this point.
        self.efetuar('iagVilleSendMessage', (indice, 2, 0))
        m.u8(rec + 0x90, 1)
        kind = m.u8(rec + 8)
        m.u8(rec + 5, 3)
        if kind not in (9, 12):
            m.u8(0x4dfb44, 20)
        if m.u8(rec + 8) == 20:
            m.u16(rec + 0x84, 0x113)
        sympathy = self.efetuar('MAJSympathie', (dono_fonte, m.u8(rec + 4), 8))
        local = m.u8(0x508041)
        if local == m.u8(rec + 4):
            return self.efetuar('VoixOffAsk', (1, 1, 0))
        if local >= 4:
            raise ValueError('Visibility-index domain for destruction requires local player 0..3')
        if m.u8(rec + 0x110 + local):
            return self.efetuar('VoixOffAsk', (1, 4, 0))
        # EAX/EDX are overwritten after sympathy, EBX is a foreign result.
        ebx = sympathy.get('EBX') if isinstance(sympathy, dict) else None
        return dict(EAX=276 * indice, EDX=local, EBX=ebx)

    def registradores(self, regs):
        result = self.infligir(regs['EAX'], regs['EDX'], regs['EBX'])
        if not isinstance(result, dict) or any(result.get(k) is None for k in ('EAX', 'EBX', 'EDX')):
            raise NotImplementedError('Destruction return requires foreign EAX/EBX/EDX register results; use the void API')
        return dict(regs, **{k: result[k] & 0xffffffff for k in ('EAX', 'EBX', 'EDX')})
