"""Original MakeMissionName filename bytes; no campaign-state defaults."""
import ambiente_missoes

_PREFIX=bytes.fromhex('5c576f726c645c4d6f6e6465303000')
_SUFFIXES=b'abcd'
_EXT=b'.ETA\0'


class DependenciaNomeMissao(NotImplementedError):
    def __init__(self,endereco,detalhe):
        self.endereco=endereco
        super().__init__(f'Nome de missão pendente em 0x{endereco:08x}: {detalhe}')


def nome_arquivo_missao(numero,destino,*,variante_u8=None,simpatia=None):
    """0x46c1b8: AL number, explicit writable destination of at least20 bytes.

    Number truncates to u8; arbitrary raw numbers need not identify a file.
    Number9 requires the inherited byte0x4e1d85, protected to indices0..3.
    Numbers10/12/17 require read-only sympathy(owner,0), consumed as signed
    low8 bits. Other numbers do not query either input. Prefix/digits precede
    dependencies; failed queries leave them visible without extension/suffix.
    Returns bytes before NUL, preserving original case/backslashes. No file
    exists/open operation, mission progress or player-state mutation occurs.
    """
    view=memoryview(destino)
    if view.readonly or not view.c_contiguous or view.ndim!=1 or view.format!='B' or len(view)<20:
        raise ValueError('Destino do nome de missão incompatível')
    number=numero&255
    view[:15]=_PREFIX
    view[12],view[13]=number//10+48,number%10+48
    suffix=b''
    if number==9:
        if variante_u8 is None:
            raise DependenciaNomeMissao(0x46c23e,'byte de variante não fornecido')
        variant=variante_u8&255
        if variant>=4:
            raise ValueError('Índice de variante fora de0..3')
        suffix=_SUFFIXES[variant:variant+1]
    elif number in (10,12,17):
        best,chosen=90,0
        for owner in (1,2,3):
            if simpatia is None:
                raise DependenciaNomeMissao(0x46dc6c,'consulta de simpatia não fornecida')
            raw=simpatia(owner,0)&255
            value=raw-256 if raw&128 else raw
            if best>value:
                best,chosen=value,owner-1
        suffix=_SUFFIXES[chosen:chosen+1]
    end=14
    if suffix:
        view[end:end+2]=suffix+b'\0'
        end+=1
    view[end:end+5]=_EXT
    return bytes(view[:end+4])
