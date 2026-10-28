"""Bounded EnginInfligeDegat modes 1/8, with live world callbacks.

This is the unit consumer at 0x4502f0, not InfligeDegat's cell selection,
reaction, diplomacy or presentation wrapper. Other modes are explicit
boundaries; death stops by default or delegates to an opt-in handler. The core
arithmetic is imported from a committed baseline; no second implementation of
its fixed-width rules is introduced.
"""
from dataclasses import dataclass
from pathlib import Path
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'ferramentas'))
from combate import dano_bruto_unidade, reduzir_dano, aplicar_dano_parcial
from projeteis import u16, por16


class LimiteMorte(NotImplementedError):
    """Original execution would enter 0x4506a1; prior effects remain visible."""
    endereco = 0x4506a1

    def __init__(self, vitima, atacante, dano, modo=1):
        self.vitima, self.atacante, self.dano = vitima, atacante, dano
        self.modo = modo
        super().__init__('EnginInfligeDegat death branch at 0x4506a1 is external')


@dataclass
class ConsumidorDanoUnidade:
    """800 mutable 276-byte records; 26 rows, or 27 for special mode 8.

    consulta(name, args) supplies the original query result, efeito(name, args)
    performs an external effect. Both may mutate live records/context. Rows
    contain at least 26 u8 entries indexed by the victim's original type.
    Missing callbacks raise at their call site without rolling back effects.
    Native pointer &victim[0x104] is represented by the victim ID in the final
    PlaySnd_PostSound argument, matching the existing combat sound adapter.
    """
    unidades: object
    danos: object
    consulta: object = None
    efeito: object = None
    jogador_local: int = 0
    bonus_4965ac: int = 0
    morte: object = None

    def __post_init__(self):
        if len(self.unidades) != 800 or any(len(u) != 276 for u in self.unidades):
            raise ValueError('Expected 800 live 276-byte unit records')
        if len(self.danos) not in (26, 27) or any(len(row) < 26 for row in self.danos):
            raise ValueError('Expected 26 or 27 damage rows with at least 26 u8 entries')

    def _consultar(self, nome, *args):
        if self.consulta is None:
            raise NotImplementedError('External query required: ' + nome)
        return self.consulta(nome, args)

    def _emitir(self, nome, *args):
        if self.efeito is None:
            raise NotImplementedError('External effect required: ' + nome)
        self.efeito(nome, args)

    def infligir(self, vitima, modo, atacante, direcao=0):
        """Consume AX/DL/BX/CL inputs; direction is unused in modes 1/8.

        Returns None on the original nonlethal return. LimiteMorte is raised
        before death when no mode-1 handler is supplied, and always in mode 8.
        Unsupported modes/types/IDs fail before queries, effects or writes.
        """
        vitima, atacante, modo = vitima & 65535, atacante & 65535, modo & 255
        if modo not in (1, 8):
            raise NotImplementedError('Only EnginInfligeDegat mode 1 or 8 is supported')
        if modo == 8 and len(self.danos) != 27:
            raise ValueError('Mode 8 requires the explicitly loaded damage row 26')
        if vitima >= 800 or atacante >= 800:
            raise ValueError('Unit IDs must be in 0..799 after u16 truncation')
        alvo, fonte = self.unidades[vitima], self.unidades[atacante]
        if alvo[1] >= 26 or fonte[1] >= 26:
            raise ValueError('Unit types must be in 0..25')
        celula_entrada = u16(alvo, 0x7c)  # saved at 0x45033f before any callback

        if modo == 1:
            # Save matrix+bonus before queries; reread live fields at call sites.
            bruto = dano_bruto_unidade(self.danos[fonte[1]][alvo[1]], fonte[0xf7])
            mod5 = self._consultar('Modificateur', fonte[0], 5, fonte[1])
            bruto = dano_bruto_unidade(bruto, modificador5=mod5)
            proximo = self._consultar('ChercheTypeEnginProximite', 2, fonte[0], u16(fonte, 0x7c), 10)
            if proximo & 255:
                bruto = dano_bruto_unidade(bruto, bonus_proximidade=self.bonus_4965ac & 255)
            self._emitir('iagUnitSendMessage', vitima, 0x48, atacante)
            dono_morte = fonte[0]  # saved before reduction/visibility
        else:
            # 0x450475: mode 8 uses only the separately loaded special row.
            bruto = self.danos[26][alvo[1]]

        # 0x45059c: reduction +f6 is the victim's; modifier 6 uses the attacker.
        reducao = alvo[0xf6]
        mod6 = self._consultar('Modificateur', fonte[0], 6, fonte[1])
        dano = reduzir_dano(bruto, reducao, mod6)
        visivel = self._consultar('TerrainEstDecouvert', u16(alvo, 8), self.jogador_local & 255)
        if visivel & 255:
            volume = self._consultar('EnginGetVolume', vitima) & 0xffffffff
            handle = struct.unpack_from('<I', alvo, 0x104)[0]
            alvo[0xf9] = 0
            if handle == 0xffffffff:
                self._emitir('PlaySnd_PostSound', 0x50, (alvo[1] << 16) | 0x100,
                             0, volume, vitima)
        resultado = aplicar_dano_parcial(u16(alvo, 0x9a), dano, bool(alvo[0xdc] & 8))
        if resultado['entra_no_ramo_morte']:
            if modo == 1 and self.morte is not None:
                return self.morte(vitima, atacante, resultado['dano_com_sinal'],
                                  celula_entrada, dono_morte)
            raise LimiteMorte(vitima, atacante, resultado['dano_com_sinal'], modo)
        por16(alvo, 0x9a, resultado['vida'])
