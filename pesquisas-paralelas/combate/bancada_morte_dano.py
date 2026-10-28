"""Original lethal consumer prefixes and an isolated post-lifecycle fragment."""
import struct

from bancada_impacto_unidades import BancadaImpactoUnidades, WRAPPER, DEPENDENCIES
from bancada_combate import RETORNO, x86

LETHAL_EFFECTS = {0x44fb20: 'EnginSetLevelExperience', 0x444938: 'SetDyingEngin',
                  0x475118: 'MAJSympathie'}


class BancadaMorteDano(BancadaImpactoUnidades):
    def __init__(self):
        super().__init__()
        self.eventos_morte = []

    def _capture(self, result):
        at = result['EIP']
        if at in LETHAL_EFFECTS:
            a, d, b = (result[n] for n in ('EAX', 'EDX', 'EBX'))
            args = ((a & 65535, d & 255) if at == 0x44fb20 else
                    (a & 65535,) if at == 0x444938 else (a & 255, d & 255, b))
            self.eventos_morte.append((LETHAL_EFFECTS[at], args))
        return result

    def infligir_letal(self, vitima=1, atacante=0):
        self.eventos_morte = []
        return self._capture(self.executar(0x4502f0, WRAPPER,
            dict(EAX=vitima, EDX=1, EBX=atacante, ECX=255),
            parada={RETORNO, 0x44fb20, 0x444938, 0x475118, 0x48aa79},
            limite_instrucoes=100000))

    def simpatia_apos_dying(self, vitima, dono_fonte):
        """Synthetic post-provider inputs; does not execute/skip a lifecycle CALL.

        Start a separate original fragment at 0x4507af, not a forged return.
        Stop at MAJSympathie before the fragment's stack-frame epilogue.
        """
        self.eventos_morte = []
        return self._capture(self.executar(0x4507af, [(0x4507af, 0x45084f)],
            dict(EDI=vitima, EDX=vitima), pilha={0x28: bytes([dono_fonte & 255])},
            parada=0x475118))

    def impacto_letal(self, indice=37):
        from bancada_projeteis import PROJETEIS
        self.eventos_morte = []
        return self._capture(self.executar(0x46eaf8, WRAPPER,
            dict(EAX=PROJETEIS + 56 * indice),
            parada={RETORNO, 0x44fb20, 0x444938, *DEPENDENCIES},
            limite_instrucoes=100000))
