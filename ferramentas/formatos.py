"""Leitores independentes, em português, dos formatos observados no CD brasileiro.

Não executam o jogo. Campos sem semântica comprovada permanecem anônimos.
Os limites e offsets estão explicados em documentacao/FORMATOS.md.
"""
from dataclasses import dataclass
import hashlib
import struct


class ErroFormato(ValueError):
    """Arquivo truncado ou incompatível com a variante estudada."""


class Leitor:
    def __init__(self, dados, posicao=0):
        self.dados = dados
        self.posicao = posicao

    def ler(self, tamanho):
        fim = self.posicao + tamanho
        if tamanho < 0 or fim > len(self.dados):
            raise ErroFormato(f"Leitura inválida em 0x{self.posicao:x}: {tamanho} bytes")
        trecho = self.dados[self.posicao:fim]
        self.posicao = fim
        return trecho

    def u16(self):
        return struct.unpack('<H', self.ler(2))[0]

    def u32(self):
        return struct.unpack('<I', self.ler(4))[0]


@dataclass
class Quadro:
    largura: int
    altura: int
    pixels: bytes


def ler_cmp(dados):
    """Decodifica os comandos: positivo pula zeros; negativo copia literais.

    A imagem retornada usa índice zero para a transparência. Este leitor
    valida a expansão; a rotina original de desenho pula pixels no destino.
    """
    leitor = Leitor(dados)
    quadros = []
    for indice in range(leitor.u16()):
        largura, altura, tamanho = leitor.u16(), leitor.u16(), leitor.u32()
        if not largura or not altura or largura * altura > 16_777_216:
            raise ErroFormato(f"Dimensões inválidas no quadro {indice}")
        comandos = Leitor(leitor.ler(tamanho))
        pixels = bytearray()
        while comandos.posicao < len(comandos.dados):
            comando = comandos.ler(1)[0]
            if comando == 128:
                # Não ocorre no corpus. NEG BL seguido de MOVSX conserva -128;
                # tratá-lo como +128 presumiria uma semântica não comprovada.
                raise ErroFormato("Comando CMP 0x80 não suportado pela variante estudada")
            quantidade = 256 - comando if comando >= 128 else comando
            if len(pixels) + quantidade > largura * altura:
                raise ErroFormato(f"Expansão excede o quadro {indice}")
            pixels.extend(comandos.ler(quantidade) if comando >= 128 else bytes(quantidade))
        if len(pixels) != largura * altura:
            raise ErroFormato(f"Quantidade de pixels incorreta no quadro {indice}")
        quadros.append(Quadro(largura, altura, bytes(pixels)))
    if leitor.posicao != len(dados):
        raise ErroFormato("Bytes extras após o último quadro CMP")
    return quadros


def ler_paleta(dados):
    if len(dados) < 777 or dados[:3] != b'Pie' or struct.unpack_from('<H', dados, 7)[0] != 256:
        raise ErroFormato("Cabeçalho de paleta PIE inválido")
    return bytes((v & 63) * 4 + 3 if v & 63 else 0 for v in dados[9:777])


def ler_eta(dados):
    """Reconstrói a sequência de leituras de 0x46c2cf, incluindo subrotinas.

    O sufixo de 0xe0000 bytes é observado em todo o corpus, mas não é
    consumido por esse caminho de carregamento. Seu conteúdo não é descartado
    silenciosamente: tamanho, offset e hash entram no relatório.
    """
    leitor = Leitor(dados)
    if leitor.ler(4) != b'V0.3':
        raise ErroFormato("Versão ETA diferente de V0.3")
    camadas = {}
    for nome, tamanho in [('atributos', 0x10000), ('terreno', 0x20000),
                          ('objetos', 0x10000), ('variantes', 0x10000)]:
        camadas[nome] = leitor.ler(tamanho)
    recursos = {str(tipo): [leitor.u16() for _ in range(4)] for tipo in (1, 2, 0)}
    largura, altura = leitor.u16(), leitor.u16()
    if not 1 <= largura <= 256 or not 1 <= altura <= 256:
        raise ErroFormato("Dimensões ETA fora de 1..256")
    origens = [[leitor.u16(), leitor.u16()] for _ in range(4)]
    blocos = []
    registros = {}

    def bloco(nome, rotina, tamanho_fixo=None, indexado=False):
        inicio = leitor.posicao
        quantidade = leitor.u16()
        tamanho = leitor.u16() if tamanho_fixo is None else tamanho_fixo
        if quantidade and not tamanho:
            raise ErroFormato(f"Registro de tamanho zero em {nome}")
        itens = []
        for _ in range(quantidade):
            indice = leitor.u16() if indexado else None
            itens.append((indice, leitor.ler(tamanho)))
        blocos.append(dict(nome=nome, rotina=rotina, offset=inicio,
                           fim=leitor.posicao, quantidade=quantidade,
                           tamanho_registro=tamanho, indexado=indexado))
        registros[nome] = itens

    bloco('estruturas', '0x46c517', indexado=True)
    bloco('unidades', '0x46acbf', indexado=True)
    if blocos[0]['tamanho_registro'] != 204 or blocos[1]['tamanho_registro'] != 784:
        raise ErroFormato("Variante de estruturas/unidades ainda não estudada")
    bloco('tabela_47534a', '0x47534a', tamanho_fixo=4)
    bloco('tabela_47c24d', '0x47c24d')
    bloco('tabela_47bcc7', '0x47bcc7', tamanho_fixo=6)
    bloco('tabela_47c04a', '0x47c04a')
    bloco('tabela_458b05', '0x458b05')
    for nome, rotina, tamanho in [('bytes_descartados', '0x47c30f', 16),
                                  ('listas_por_jogador', '0x47c404', 1200)]:
        inicio = leitor.posicao
        leitor.ler(tamanho)
        blocos.append(dict(nome=nome, rotina=rotina, offset=inicio, fim=leitor.posicao,
                           tamanho_total=tamanho))
    bloco('tabela_47ac30', '0x47ac30')
    fim_carregamento = leitor.posicao
    sufixo = leitor.ler(len(dados) - leitor.posicao)
    if len(sufixo) != 0xe0000:
        raise ErroFormato(f"Sufixo ETA inesperado: {len(sufixo)} bytes")

    def recortar(camada, formato):
        valores = struct.unpack('<65536' + formato, camadas[camada])
        return [valores[y * 256 + x] for y in range(altura) for x in range(largura)]

    unidades = []
    for indice, bruto in registros['unidades']:
        # 0x46ad19..0x46ad6d: 140 bytes, pula 512, lê o restante.
        memoria = bruto[:0x8c] + bruto[0x28c:]
        unidades.append(dict(indice=indice, tipo=memoria[1],
                             byte_estado=memoria[2], tamanho_memoria_serializada=len(memoria)))
    return dict(largura=largura, altura=altura, recursos_por_tipo=recursos,
                origens_visualizacao=origens, blocos=blocos, unidades=unidades,
                fim_carregamento=fim_carregamento,
                sufixo=dict(offset=fim_carregamento, tamanho=len(sufixo),
                            sha256=hashlib.sha256(sufixo).hexdigest()),
                terreno=recortar('terreno', 'H'), atributos=recortar('atributos', 'B'),
                objetos=recortar('objetos', 'B'), variantes=recortar('variantes', 'B'))
