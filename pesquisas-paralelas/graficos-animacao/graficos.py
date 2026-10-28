"""Adaptador independente de gráficos validados. Python 3.9+, sem x86 no uso normal.

IDs do motor começam em 1; índices locais e globais desta API começam em 0.
Tipos 0, 5, 6, 7 e 9: corpo base, parada estabelecida e movimento.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import hashlib
import json
import struct
import zlib

RAIZ = Path(__file__).resolve().parent
ORDEM = ('BLOCS.CMP', 'TROOPS.CMP', 'VEHICULE.CMP', 'CREATURE.CMP', 'BUILDING.CMP', 'OTHERS.CMP')
QUANTIDADES = (1345, 2848, 915, 1920, 611, 4517)
DIRECOES = ('O', 'NO', 'N', 'NE', 'L', 'SE', 'S', 'SO')
VETORES = ((-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1))
# Campos lidos nas tabelas originais e comparados em validar_trabalhadores.py.
# Bases são IDs do motor (base 1); bolsa_u16 corresponde somente a +0x0a.
TIPOS = {
    0: dict(nome='SOLDADO', chave_ini='SOLDAT', bases=(2082,), parada=2,
            ancora=(40, 22), ramo=0x412cfe, init=0x45761b, stop=0x4481c7),
    5: dict(nome='FAZENDEIRO', chave_ini='FERMIER', bases=(1602, 1698), parada=5,
            ancora=(11, 11), ramo=0x412b7b, init=0x45785a, stop=0x4481ff),
    6: dict(nome='MECÂNICO', chave_ini='MECANO', bases=(2978, 3042), parada=2,
            ancora=(16, 20), ramo=0x412ae5, init=0x4578bb, stop=0x4481c7),
    7: dict(nome='CONSTRUTOR', chave_ini='BATISSEUR', bases=(1346, 1474), parada=3,
            ancora=(26, 26), ramo=0x4129b6, init=0x45785a, stop=0x4481e3),
    9: dict(nome='COLONO', chave_ini='COLON', bases=(1826,), parada=5,
            ancora=(19, 14), ramo=0x412c1c, init=0x45785a, stop=0x4481ff),
}


class ErroFormato(ValueError):
    pass


@dataclass(frozen=True)
class Quadro:
    largura: int
    altura: int
    pixels: bytes
    opacidade: bytes
    offset_cabecalho: int
    comprimido: bytes


def ler_cmp(dados):
    """RLE por linha, com máscara explícita: literal 0 continua opaco."""
    def ler(n):
        nonlocal pos
        if n < 0 or pos+n > len(dados):
            raise ErroFormato(f'CMP truncado em {pos:#x}')
        r = dados[pos:pos+n]
        pos += n
        return r
    pos = 0
    n, = struct.unpack('<H', ler(2))
    quadros = []
    for _ in range(n):
        offset = pos
        w, h, tamanho = struct.unpack('<HHI', ler(8))
        if not w or not h or w*h > 16_777_216:
            raise ErroFormato('Dimensões inválidas')
        bloco = ler(tamanho)
        pixels, mascara = bytearray(), bytearray()
        p = 0
        for y in range(h):
            x = 0
            while x < w:
                if p >= len(bloco):
                    raise ErroFormato('Comando truncado')
                c = bloco[p]
                p += 1
                if c == 128:
                    raise ErroFormato('0x80 não validado no original')
                conta = 256-c if c > 128 else c
                if x+conta > w:
                    raise ErroFormato('Comando cruza limite de linha')
                if c > 128:
                    if p+conta > len(bloco):
                        raise ErroFormato('Literal truncado')
                    pixels.extend(bloco[p:p+conta]); mascara.extend(b'\xff'*conta)
                    p += conta
                else:
                    pixels.extend(bytes(conta)); mascara.extend(bytes(conta))
                x += conta
        # Há terminadores zero no corpus. Não expandem pixels; permanecem no
        # bloco comprimido preservado. O blitter encerra ao atingir a altura.
        if any(bloco[p:]):
            raise ErroFormato('Bytes extras não nulos após as linhas')
        quadros.append(Quadro(w, h, bytes(pixels), bytes(mascara), offset, bloco))
    if pos != len(dados):
        raise ErroFormato('Bytes extras após CMP')
    return quadros


def ler_paleta(dados):
    if len(dados) < 777 or dados[:3] != b'Pie' or struct.unpack_from('<H', dados, 7)[0] != 256:
        raise ErroFormato('Paleta PIE inválida')
    # LoadPalette 0x47998d..0x4799ba: SHL byte,2 e primeira cor preta.
    # Corrige a expansão 4*v+3 herdada do leitor do snapshot (v1/v2).
    return bytes(3)+bytes((v << 2) & 255 for v in dados[12:777])


def localizar(id_motor):
    if not isinstance(id_motor, int) or not 1 <= id_motor <= sum(QUANTIDADES):
        raise ValueError('ID fora do banco agregado')
    base = 0
    for nome, quantidade in zip(ORDEM, QUANTIDADES):
        if id_motor <= base+quantidade:
            return dict(arquivo_cmp=nome, indice_local=id_motor-base-1,
                        indice_global=id_motor-1, id_motor=id_motor, base_global=base)
        base += quantidade


def consultar(tipo=0, estado='parado', direcao=1, fase=0, *, bolsa_u16=None):
    if type(tipo) is not int or tipo not in TIPOS:
        raise NotImplementedError('Tipos validados: 0, 5, 6, 7 e 9')
    spec = TIPOS[tipo]
    if bolsa_u16 is not None and (type(bolsa_u16) is not int or not 0 <= bolsa_u16 <= 65535):
        raise ValueError('bolsa_u16 deve ser um inteiro em 0..65535')
    usa_bolsa = len(spec['bases']) == 2
    if usa_bolsa and bolsa_u16 is None:
        raise ValueError('Forneça bolsa_u16: u16 little-endian no offset +0x0a; não presumir bolsa vazia')
    if estado not in ('parado', 'andando'):
        raise ValueError('Estado deve ser parado ou andando')
    if not isinstance(direcao, int) or not 1 <= direcao <= 16:
        raise ValueError('Direção deve estar em 1..16')
    if not isinstance(fase, int) or not 0 <= fase < 8:
        raise ValueError('Fase deve estar em 0..7')
    grupo = (direcao-1)//2
    quadro = spec['parada'] if estado == 'parado' else fase
    variante = int(bolsa_u16 != 0) if usa_bolsa else 0
    resultado = localizar(spec['bases'][variante]+8*grupo+quadro)
    ax, ay = spec['ancora']
    resultado.update(tipo=tipo, nome=spec['nome'], estado=estado, direcao=direcao,
                     direcao_sprite=DIRECOES[grupo],
                     vetor_mapa=VETORES[grupo] if direcao % 2 else None,
                     vetor_direcao_sprite=VETORES[grupo],
                     fase=quadro, sequencia=list(range(8)) if estado == 'andando' else [spec['parada']],
                     ancoragem=dict(x=ax, y=ay, referencia='origem da celula de 32x32'),
                     deslocamento_desenho=dict(x=-ax, y=-ay),
                     periodo_chamadas=2 if estado == 'andando' else None,
                     confianca='confirmada_codigo_e_comparacao_x86',
                     evidencia=['0x495bc8', '0x41877a', '0x45b259', '0x412328',
                                hex(spec['ramo']), '0x410f64', hex(spec['init']),
                                hex(spec['stop']), '0x44900b..0x449048'])
    if tipo != 0:
        resultado.update(variante=('bolsa_nao_vazia' if variante else 'bolsa_vazia') if usa_bolsa else 'base',
                         bolsa_u16=bolsa_u16 if usa_bolsa else None,
                         condicao_variante='u16(+0x0a) != 0' if usa_bolsa else 'independente de +0x0a')
        if usa_bolsa:
            resultado['evidencia'].append('0x4470b9..0x4470c5')
    return resultado


def avancar_animacao(fase, contador, periodo=2, quantidade=8):
    """Uma chamada efetiva, não um quadro de vídeo. Igualdade e overflow u8."""
    if not 0 <= fase <= 255 or not 0 <= contador <= 255 or not 0 <= periodo <= 255 or not 1 <= quantidade <= 255:
        raise ValueError('Campos fora dos limites u8; quantidade deve ser positiva')
    contador = (contador+1) & 255
    return ((fase+1) % quantidade, 0) if contador == periodo else (fase, contador)


def posicao_desenho(celula_x, celula_y, origem_x=0, origem_y=0, deslocamento_x=0, deslocamento_y=0, *, tipo=0):
    if type(tipo) is not int or tipo not in TIPOS:
        raise NotImplementedError('Tipo sem âncora validada')
    if not -128 <= deslocamento_x <= 127 or not -128 <= deslocamento_y <= 127:
        raise ValueError('Deslocamentos devem ser i8')
    ax, ay = TIPOS[tipo]['ancora']
    return (32*(celula_x-origem_x)+deslocamento_x-ax,
            32*(celula_y-origem_y)+deslocamento_y-ay)


def compor_indices(destino, largura, altura, quadro, x, y, recorte=None):
    """PasteBobCmp básico; recorte (esquerda, topo, direita, fundo) inclusivo."""
    if len(destino) != largura*altura:
        raise ValueError('Superfície inválida')
    l, t, r, b = recorte if recorte is not None else (0, 0, largura-1, altura-1)
    l, t, r, b = max(l, 0), max(t, 0), min(r, largura-1), min(b, altura-1)
    saida = bytearray(destino)
    for sy in range(max(0, t-y), min(quadro.altura, b-y+1)):
        for sx in range(max(0, l-x), min(quadro.largura, r-x+1)):
            i = sy*quadro.largura+sx
            if quadro.opacidade[i]:
                saida[(y+sy)*largura+x+sx] = quadro.pixels[i]
    return bytes(saida)


def rgba(quadro, paleta):
    return b''.join(paleta[p*3:p*3+3]+bytes([a]) for p, a in zip(quadro.pixels, quadro.opacidade))


def png(largura, altura, pixels_rgba):
    if len(pixels_rgba) != largura*altura*4:
        raise ValueError('RGBA com tamanho incorreto')
    def chunk(tipo, dados):
        return struct.pack('>I', len(dados))+tipo+dados+struct.pack('>I', zlib.crc32(tipo+dados) & 0xffffffff)
    linhas = b''.join(b'\0'+pixels_rgba[y*largura*4:(y+1)*largura*4] for y in range(altura))
    return (b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR', struct.pack('>IIBBBBB', largura, altura, 8, 6, 0, 0, 0))
            +chunk(b'IDAT', zlib.compress(linhas, 9))+chunk(b'IEND', b''))


class Catalogo:
    def __init__(self, fontes=None):
        self.fontes = Path(fontes or RAIZ / 'fontes')
        self.manifesto = json.loads((self.fontes/'manifesto.json').read_text())
        self._bancos = {}

    def _ler(self, relativo):
        caminho = self.fontes/relativo
        esperado = next((x['sha256'] for x in self.manifesto if x['copia'] == 'fontes/'+relativo), None)
        dados = caminho.read_bytes()
        if esperado is None or hashlib.sha256(dados).hexdigest() != esperado:
            raise ValueError(f'SHA-256 incompatível: {relativo}')
        return dados

    def banco(self, nome):
        if nome not in ORDEM:
            raise ValueError('Banco não agregado')
        if nome not in self._bancos:
            quadros = ler_cmp(self._ler('cd/INSTALHD/GRAPHICS/'+nome))
            if len(quadros) != QUANTIDADES[ORDEM.index(nome)]:
                raise ErroFormato('Contagem divergente')
            self._bancos[nome] = quadros
        return self._bancos[nome]

    def quadro(self, id_motor):
        info = localizar(id_motor)
        return self.banco(info['arquivo_cmp'])[info['indice_local']]

    def paleta(self):
        return ler_paleta(self._ler('cd/INSTALHD/PLATGAME.PIE'))

    def imagem_png(self, **consulta):
        info = consultar(**consulta)
        quadro = self.quadro(info['id_motor'])
        return png(quadro.largura, quadro.altura, rgba(quadro, self.paleta()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tipo', type=int, default=0)
    parser.add_argument('--estado', choices=('parado', 'andando'), default='parado')
    parser.add_argument('--direcao', type=int, default=1)
    parser.add_argument('--fase', type=int, default=0)
    parser.add_argument('--bolsa-u16', type=int, default=None)
    args = parser.parse_args()
    print(json.dumps(consultar(**vars(args)), ensure_ascii=False, indent=2))
