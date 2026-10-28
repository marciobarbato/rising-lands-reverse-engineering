"""Original read-only EnginRentreMatiere / EnginApporteMatiere queries."""
from recrutamento import Recrutamento,_word

_ESTADOS=frozenset((5,17,18))


class ConsultasTransporte:
    """Share existing recruitment buffers; defaults are synthetic, not loading."""
    def __init__(self,recrutamento=None):
        self.recrutamento=Recrutamento() if recrutamento is None else recrutamento

    def _registro(self,indice):
        indice&=65535
        if indice>=800 or len(self.recrutamento.unidades)!=220800:
            raise ValueError('Transport query requires unit0..799 and800 records')
        return indice*276

    def retorna(self,indice,tipo_construcao):
        """0x456cd9; AX unit, DL building TYPE byte, return AL bool.

        State5/17/18 and+82byte2 precede the+80 building reference. Invalid
        references are protected only if read; other branches return false.
        Actual native getter reads building+8, not owner+4. No mutation.
        """
        o=self._registro(indice)
        r=self.recrutamento
        u=r.unidades
        if u[o+2] not in _ESTADOS or u[o+0x82]!=2:
            return False
        alvo=_word(u,o+0x80)
        s=r.mundo.estruturas
        if alvo>=1000 or (alvo+1)*276>len(s):
            raise ValueError('Conditional building type lookup requires target0..999 in supplied pool')
        return s[alvo*276+8]==(tipo_construcao&255)

    def aporta(self,indice,valor84,modo82=0):
        """0x456d35; DL comparison byte, BL mode byte0 wildcard.

        State5/17/18, fullu16+84 equals lowu8DL, then BLzero or exact byte+82.
        Raw field names avoid assuming further cargo/destination semantics.
        No structure/reference/owner/Bag read or mutation occurs.
        """
        o=self._registro(indice)
        u=self.recrutamento.unidades
        modo82&=255
        return (u[o+2] in _ESTADOS and _word(u,o+0x84)==(valor84&255)
                and (modo82==0 or u[o+0x82]==modo82))
