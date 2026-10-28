"""Avanço de produção, sem criar unidades nem concluir aprendizagem.

ConstruitPerso e ConstruitSort usam AX como índice de construção. O modelo
reproduz seus efeitos de memória sob o controle x87 inicial 0x127f: precisão
53, arredondamento ao mais próximo e exceções mascaradas. Ver PRODUCAO.md.
"""
import struct

from recrutamento import Recrutamento, _word

BASE_TIPOS_CONSTRUCOES = 0x495d8c
BASE_AJUSTE_HOSPITAL = 0x495be8
CONTROLE_X87_INICIAL = 0x127f


def incremento_producao(quantidade, divisor, coeficiente):
    """FDIV, FMUL, armazenamento double, __CHP e FISTP (domínio protegido).

    A ordem dos dois arredondamentos binary64 importa. Não substituir por
    quantidade * coeficiente // divisor. Com divisor zero e exceções x87
    mascaradas, FISTP gera 0x80000000; AND 0xffff elimina esse valor.
    """
    if not 0 <= quantidade <= 30 or not 0 <= divisor <= 255 or coeficiente not in (10, 100):
        raise ValueError('Incremento fora do domínio: 0..30, 0..255, coeficiente 10/100')
    convertido = 0x80000000 if divisor == 0 else int((quantidade / divisor) * float(coeficiente))
    return 100 + (convertido & 65535)


class Producao:
    def __init__(self, recrutamento=None, *, tipos_construcoes=None, ajuste_hospital=5):
        self.recrutamento = Recrutamento() if recrutamento is None else recrutamento
        # Buffer sintético por padrão; carregar a tabela do jogo na integração.
        self.tipos_construcoes = bytearray(22 * 52 if tipos_construcoes is None else tipos_construcoes)
        if len(self.tipos_construcoes) != 22 * 52:
            raise ValueError('Tabela de construções deve ter 1144 bytes')
        self.ajuste_hospital = ajuste_hospital & 255

    def contar_unidades(self, indice, tipo=9):
        """BagContient 0x4471b8, somente modo DL=1, alvo BX=tipo.

        Percorre a capacidade word +2 da Bag, situada em construção +0xc.
        Conta slots com etiqueta 1 cujo índice aponta a uma unidade do tipo
        pedido. Não usa ocupação, não remove duplicatas, não altera a Bag.
        """
        r = self.recrutamento
        o = r._offset(indice)
        s = r.mundo.estruturas
        capacidade = _word(s, o + 0xe)
        if capacidade > 30:
            raise ValueError('Capacidade de Bag fora de 0..30 no modelo protegido')
        quantidade = 0
        for slot in range(capacidade):
            if s[o + 0x4e + slot] != 1:
                continue
            unidade = _word(s, o + 0x12 + 2 * slot)
            if unidade >= 800:
                raise ValueError('Referência de unidade fora de 0..799')
            quantidade += r.unidades[unidade * 276 + 1] == (tipo & 65535)
        return quantidade

    def _avancar(self, indice, sortilegio):
        r = self.recrutamento
        o = r._offset(indice)
        s = r.mundo.estruturas
        tipo_solicitado = s[o + 0x7b]
        # ConstruitSort consulta uma vez antes dos retornos antecipados e
        # outra vez no ramo ativo. ConstruitPerso só consulta no ramo ativo.
        if sortilegio:
            r.tempo_sortilegio(tipo_solicitado)
        progresso = struct.unpack_from('<I', s, o + 0x8c)[0]
        if progresso == 0 or s[o + 0x74] == 0:
            return False
        tempo = (r.tempo_sortilegio if sortilegio else r.tempo_unidade)(tipo_solicitado)
        if progresso >= tempo * 100:
            return True
        quantidade = self.contar_unidades(indice, 9)
        tipo_construcao = s[o + 8]
        if tipo_construcao >= 22:
            raise ValueError('Tipo de construção fora de 0..21')
        divisor = self.tipos_construcoes[tipo_construcao * 52 + 18]
        if tipo_construcao == 14:
            divisor = (divisor - 1) & 255
        elif tipo_construcao == 19:
            divisor = (divisor - (self.ajuste_hospital & 255)) & 255
        incremento = incremento_producao(quantidade, divisor, 10 if tipo_construcao == 14 else 100)
        struct.pack_into('<I', s, o + 0x8c, (progresso + incremento) & 0xffffffff)
        return True

    def avancar_unidade(self, indice):
        """ConstruitPerso 0x423b9b. True significa ativo, não concluído."""
        return self._avancar(indice, False)

    def avancar_sortilegio(self, indice):
        """ConstruitSort 0x423d14. True não implica aprendizagem concluída."""
        return self._avancar(indice, True)
