"""Original CalculEclairage table and indexed PasteEclairCmp mask behavior."""
from composicao import compor_sombra


def tabela_eclairage(paleta,*,percentual,ciclos):
    """768 RGB bytes; percentage is original DL, restricted to 1..255.

    Each zero scaled component targets 30; other components cap at 255.
    Initial palette candidate zero remains eligible even inside a cycle.
    """
    if len(paleta)!=768:raise ValueError('Expected 768 RGB palette bytes')
    if type(percentual) is not int or not 1<=percentual<=255:
        raise ValueError('percentual must be an integer in 1..255')
    ciclos=tuple(ciclos)
    if len(ciclos)>255:raise ValueError('At most 255 cycle intervals are supported')
    for interval in ciclos:
        if len(interval)!=2 or any(type(v) is not int or not 0<=v<=255 for v in interval) or interval[0]>interval[1]:
            raise ValueError('Expected inclusive ordered u8 cycle intervals')
    colors=[tuple(paleta[offset:offset+3]) for offset in range(0,768,3)]
    candidates=[0]+[index for index in range(1,256) if not any(low<=index<=high for low,high in ciclos)]
    table=bytearray()
    for color in colors:
        scaled=[component*100//percentual for component in color]
        target=tuple(30 if component==0 else min(component,255) for component in scaled)
        table.append(min(candidates,key=lambda index:sum((a-b)**2 for a,b in zip(target,colors[index]))))
    return bytes(table)


def compor_eclairage(destino,largura,altura,quadro,x,y,tabela,recorte=None):
    """Clipping-enabled destination remap under opacity; source colors ignored."""
    if any(type(value) is not int or not -32768<=value<=32767 for value in (x,y)):
        raise ValueError('x/y must be signed 16-bit positions')
    return compor_sombra(destino,largura,altura,quadro,x,y,tabela,recorte)
