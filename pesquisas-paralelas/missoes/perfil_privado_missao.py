"""Declared KERNEL32 profile binding consumed by InitEntrerMonstre 0x47a601.

This is not engine code: it answers GetPrivateProfileIntA/StringA from files
the caller declares explicitly. An undeclared file raises; a file declared as
None is absent and yields the documented Windows default. Only a strict INI
subset is accepted: ``[section]`` and ``key=value`` lines without surrounding
blanks, quotes or duplicates; matching is ASCII case-insensitive.
"""


class DependenciaPerfil(LookupError):
    def __init__(self,arquivo):
        self.arquivo=arquivo
        super().__init__(f'Profile file {arquivo!r} is not a declared binding input')


def _analisar(dados):
    secoes,atual={},None
    for linha in bytes(dados).split(b'\n'):
        linha=linha[:-1] if linha.endswith(b'\r') else linha
        if not linha.strip():
            continue
        if linha!=linha.strip():
            raise ValueError('Unsupported profile line padding')
        if linha.startswith(b'[') and linha.endswith(b']'):
            atual=linha[1:-1].lower()
            if atual in secoes:
                raise ValueError('Duplicate profile section')
            secoes[atual]={}
            continue
        chave,igual,valor=linha.partition(b'=')
        if atual is None or not igual or chave!=chave.strip() or valor!=valor.strip() or valor[:1] in (b'"',b"'"):
            raise ValueError('Unsupported profile syntax')
        if chave.lower() in secoes[atual]:
            raise ValueError('Duplicate profile key')
        secoes[atual][chave.lower()]=valor
    return secoes


class PerfilPrivado:
    def __init__(self,arquivos):
        self.arquivos={bytes(nome).lower():(None if dados is None else _analisar(dados))
                       for nome,dados in arquivos.items()}
        self.chamadas=[]

    def _valor(self,secao,chave,arquivo):
        nome=bytes(arquivo).lower()
        if nome not in self.arquivos:
            raise DependenciaPerfil(bytes(arquivo))
        secoes=self.arquivos[nome]
        if secoes is None:
            return None
        return secoes.get(bytes(secao).lower(),{}).get(bytes(chave).lower())

    def inteiro(self,secao,chave,padrao,arquivo):
        """GetPrivateProfileIntA: declared decimal value, else nDefault."""
        valor=self._valor(secao,chave,arquivo)
        if valor is None:
            resultado=padrao&0xffffffff
        elif valor.isdigit() and int(valor)<2**31:
            resultado=int(valor)
        else:
            raise ValueError('Unsupported profile integer value')
        self.chamadas.append(('int',bytes(secao),bytes(chave),padrao&0xffffffff,bytes(arquivo),resultado))
        return resultado

    def texto(self,secao,chave,padrao,tamanho,arquivo):
        """GetPrivateProfileStringA: value or lpDefault, truncated to nSize-1 bytes."""
        if tamanho<1:
            raise ValueError('Unsupported profile buffer size')
        valor=self._valor(secao,chave,arquivo)
        resultado=bytes(padrao if valor is None else valor)[:tamanho-1]
        self.chamadas.append(('string',bytes(secao),bytes(chave),bytes(padrao),tamanho,bytes(arquivo),resultado))
        return resultado
