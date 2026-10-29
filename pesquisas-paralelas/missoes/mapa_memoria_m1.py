"""One non-overlapping address-space model for the M1 MissionLoad composition.

The frozen entry snapshot (``entrada-carga-missao-original.json``) is the only
source of bytes. Provider objects keep their own live buffers: each one is
bound at its original address and filled IN PLACE (slice assignment) from the
snapshot; it is never rebound or replaced. Containing blocks (DGROUP or an
allocation) are split around those buffers, and every byte not owned by a
provider becomes a Missions gap segment, also filled from the snapshot.

Three representations are admitted, each declared once per address range:

* byte segments: a provider ``bytearray`` or a writable contiguous ``B``
  memoryview of one (the canonical bytes);
* list segments: Core keeps some u16 grids as Python ``list`` objects (tiles,
  regions, the structure-color stack). The list is canonical; serialization
  packs it. These ranges are not exposed as bytes to byte-addressed callers;
* cached scalars: a provider attribute (int, or a strided byte cache) that
  mirrors bytes owned by a byte segment. The bytes are canonical; the composer
  pulls the attribute before and pushes it after each provider call.

``serializar`` rebuilds the snapshot block layout so the whole state can be
compared byte for byte. Nothing here supplies a default value.
"""
import base64
import hashlib
import json
import struct
import zlib


def sha256(dados):
    return hashlib.sha256(bytes(dados)).hexdigest()


def carregar_blocos(blocos_json):
    """Decompress one snapshot ``blocks`` mapping, verifying every SHA-256."""
    blocos = {}
    for nome, bloco in blocos_json.items():
        dados = zlib.decompress(base64.b64decode(bloco['zlib_base64']))
        if len(dados) != bloco['bytes'] or sha256(dados) != bloco['sha256']:
            raise ValueError(f'Snapshot block {nome} does not match its recorded size/SHA-256')
        blocos[nome] = (int(bloco['base'], 16), dados)
    return blocos


def expandir_captura(captura, entrada):
    """Full ``final_state.blocks`` of a delta-encoded MissionLoad capture (display scenario).

    Blocks MissionLoad did not change are taken from the entry artifact; every
    block must still match the capture's recorded size and SHA-256.
    """
    final = captura['oracle']['final_state']
    if final.get('encoding') != 'delta_from_entry':
        return captura
    blocos = {}
    for nome, h in final['block_hashes'].items():
        bloco = final['blocks'].get(nome) or entrada['blocks'].get(nome)
        if bloco is None or bloco['sha256'] != h['sha256'] or bloco['bytes'] != h['bytes'] or bloco['base'] != h['base']:
            raise ValueError(f'Delta capture block {nome} is not reproduced by the entry artifact')
        blocos[nome] = bloco
    expandida = dict(captura)
    expandida['oracle'] = dict(captura['oracle'], final_state=dict(final, blocks=blocos))
    return expandida


def carregar_json(caminho):
    with open(caminho, 'rb') as arquivo:
        return json.loads(arquivo.read())


class ErroMapaMemoria(ValueError):
    pass


def _vista_bytes(buffer, nome):
    view = memoryview(buffer)
    if view.readonly or view.ndim != 1 or not view.c_contiguous or view.itemsize != 1:
        raise ErroMapaMemoria(f'{nome} must be a writable contiguous byte buffer')
    return view.cast('B') if view.format != 'B' else view


class SegmentoBytes:
    tipo = 'bytes'

    def __init__(self, base, buffer, dono, bloco):
        self.vista = _vista_bytes(buffer, dono)
        self.buffer = buffer
        self.base, self.fim, self.dono, self.bloco = base, base + len(self.vista), dono, bloco

    def bytes(self):
        return bytes(self.vista)


class SegmentoLista:
    tipo = 'list'

    def __init__(self, base, lista, formato, dono, bloco):
        if not isinstance(lista, list):
            raise ErroMapaMemoria(f'{dono} must be the provider list object')
        self.lista, self.formato = lista, formato
        self.largura = struct.calcsize('<' + formato)
        self.base, self.fim = base, base + len(lista) * self.largura
        self.dono, self.bloco = dono, bloco

    def bytes(self):
        return struct.pack(f'<{len(self.lista)}{self.formato}', *self.lista)

    def carregar(self, dados):
        if len(dados) != self.fim - self.base:
            raise ErroMapaMemoria(f'{self.dono} list load size mismatch')
        self.lista[:] = struct.unpack(f'<{len(self.lista)}{self.formato}', dados)


class CacheEscalar:
    """A provider attribute mirroring bytes that a byte segment owns."""

    def __init__(self, endereco, formato, obter, definir, dono):
        self.endereco, self.formato, self.obter, self.definir, self.dono = endereco, formato, obter, definir, dono
        self.largura = struct.calcsize('<' + formato)


class MapaMemoriaM1:
    def __init__(self, blocos):
        """``blocos``: name -> (base, bytes) from :func:`carregar_blocos`."""
        self.origem = {nome: (base, bytes(dados)) for nome, (base, dados) in blocos.items()}
        self.vinculos = []        # provider segments before closing
        self.segmentos = []       # every segment after closing, sorted
        self.caches = []
        self.blocos = {nome: (base, base + len(dados)) for nome, (base, dados) in self.origem.items()}
        self.fechado = False
        self.liberados = {}       # block name -> final bytes at GlobalFree

    # -- binding -------------------------------------------------------
    def _bloco_de(self, base, fim, dono):
        for nome, (inicio, final) in self.blocos.items():
            if inicio <= base and fim <= final:
                return nome
        raise ErroMapaMemoria(f'{dono} [0x{base:08x},0x{fim:08x}) is not inside one snapshot block')

    def _verificar_livre(self, base, fim, dono):
        for s in self.vinculos:
            if base < s.fim and s.base < fim:
                raise ErroMapaMemoria(f'{dono} overlaps {s.dono} at 0x{max(base, s.base):08x}')

    def _dados(self, bloco, base, fim):
        inicio, dados = self.origem[bloco]
        return dados[base - inicio:fim - inicio]

    def ler_origem(self, endereco, tamanho):
        """Entry-snapshot bytes (used only to resolve pointer slots while binding)."""
        return self._dados(self._bloco_de(endereco, endereco + tamanho, 'ler_origem'), endereco, endereco + tamanho)

    def tamanho_bloco(self, base):
        for inicio, fim in self.blocos.values():
            if inicio == base:
                return fim - inicio
        raise ErroMapaMemoria(f'No block starts at 0x{base:08x}')

    def vincular(self, endereco, buffer, dono):
        """Bind a provider byte buffer at ``endereco`` and fill it in place from the snapshot."""
        if self.fechado:
            raise ErroMapaMemoria('Map already closed')
        view = _vista_bytes(buffer, dono)
        fim = endereco + len(view)
        bloco = self._bloco_de(endereco, fim, dono)
        self._verificar_livre(endereco, fim, dono)
        view[:] = self._dados(bloco, endereco, fim)
        segmento = SegmentoBytes(endereco, buffer, dono, bloco)
        self.vinculos.append(segmento)
        return segmento

    def vincular_lista(self, endereco, lista, formato, dono):
        """Bind a provider list (canonical) and fill it in place by slice assignment."""
        if self.fechado:
            raise ErroMapaMemoria('Map already closed')
        segmento = SegmentoLista(endereco, lista, formato, dono, None)
        segmento.bloco = self._bloco_de(segmento.base, segmento.fim, dono)
        self._verificar_livre(segmento.base, segmento.fim, dono)
        segmento.carregar(self._dados(segmento.bloco, segmento.base, segmento.fim))
        self.vinculos.append(segmento)
        return segmento

    def cache(self, endereco, formato, obter, definir, dono):
        """Declare a provider scalar mirroring canonical bytes (pulled/pushed by the composer)."""
        c = CacheEscalar(endereco, formato, obter, definir, dono)
        self.caches.append(c)
        return c

    def fechar(self):
        """Create Missions gap segments for every byte not owned by a provider."""
        segmentos = list(self.vinculos)
        for nome, (inicio, fim) in self.blocos.items():
            dentro = sorted((s for s in self.vinculos if s.bloco == nome), key=lambda s: s.base)
            cursor = inicio
            for s in dentro + [None]:
                limite = fim if s is None else s.base
                if limite > cursor:
                    gap = bytearray(self._dados(nome, cursor, limite))
                    segmentos.append(SegmentoBytes(cursor, gap, f'gap:{nome}', nome))
                if s is not None:
                    cursor = s.fim
        self.segmentos = sorted(segmentos, key=lambda s: s.base)
        for a, b in zip(self.segmentos, self.segmentos[1:]):
            if a.fim > b.base:
                raise ErroMapaMemoria(f'Segments {a.dono} and {b.dono} overlap')
        self.fechado = True
        for c in self.caches:
            self._segmento_bytes(c.endereco, c.largura, c.dono)
        self.puxar()

    # -- access -------------------------------------------------------
    def _segmento(self, endereco, tamanho):
        for s in self.segmentos:
            if s.base <= endereco and endereco + tamanho <= s.fim:
                return s
        raise ErroMapaMemoria(f'[0x{endereco:08x},+{tamanho}) is not inside one mapped segment')

    def _segmento_bytes(self, endereco, tamanho, dono='access'):
        s = self._segmento(endereco, tamanho)
        if s.tipo != 'bytes':
            raise ErroMapaMemoria(f'{dono}: 0x{endereco:08x} belongs to list-backed {s.dono}')
        return s

    def vista(self, endereco, tamanho):
        """Writable view into the single byte segment holding the range."""
        s = self._segmento_bytes(endereco, tamanho)
        return s.vista[endereco - s.base:endereco - s.base + tamanho]

    def ler(self, endereco, tamanho):
        s = self._segmento(endereco, tamanho)
        if s.tipo == 'bytes':
            return bytes(s.vista[endereco - s.base:endereco - s.base + tamanho])
        return s.bytes()[endereco - s.base:endereco - s.base + tamanho]

    def u32(self, endereco):
        return struct.unpack('<I', self.ler(endereco, 4))[0]

    def u16(self, endereco):
        return struct.unpack('<H', self.ler(endereco, 2))[0]

    def u8(self, endereco):
        return self.ler(endereco, 1)[0]

    # -- scalar caches ------------------------------------------------
    def puxar(self):
        """Load every cached provider scalar from its canonical bytes."""
        for c in self.caches:
            c.puxado = struct.unpack('<' + c.formato, self.ler(c.endereco, c.largura))[0]
            c.definir(c.puxado)

    def empurrar(self):
        """Store provider scalars that changed since the last pull.

        A cache whose canonical bytes were also changed meanwhile by a byte
        writer, or two caches of one address changed to different values, is a
        divergence and raises instead of choosing a winner.
        """
        escritos = {}
        for c in self.caches:
            valor = c.obter() & ((1 << (8 * c.largura)) - 1)
            if valor == c.puxado:
                continue
            atual = struct.unpack('<' + c.formato, self.ler(c.endereco, c.largura))[0]
            anterior = escritos.get(c.endereco)
            if anterior is not None and anterior[0] != valor:
                raise ErroMapaMemoria(f'Cached scalars {anterior[1]} and {c.dono} diverged at 0x{c.endereco:08x}')
            if anterior is None and atual not in (c.puxado, valor):
                raise ErroMapaMemoria(f'{c.dono} and a byte writer both changed 0x{c.endereco:08x}')
            escritos[c.endereco] = (valor, c.dono)
            self.vista(c.endereco, c.largura)[:] = struct.pack('<' + c.formato, valor)
        for c in self.caches:
            c.puxado = struct.unpack('<' + c.formato, self.ler(c.endereco, c.largura))[0]
            c.definir(c.puxado)

    # -- dynamic allocations -----------------------------------------
    def adicionar_bloco(self, nome, base, buffer, dono):
        if nome in self.blocos:
            raise ErroMapaMemoria(f'Block {nome} already exists')
        segmento = SegmentoBytes(base, buffer, dono, nome)
        for s in self.segmentos:
            if segmento.base < s.fim and s.base < segmento.fim:
                raise ErroMapaMemoria(f'New block {nome} overlaps {s.dono}')
        self.blocos[nome] = (segmento.base, segmento.fim)
        self.segmentos = sorted(self.segmentos + [segmento], key=lambda s: s.base)
        return segmento

    def remover_bloco(self, nome):
        dados = self.bloco_bytes(nome)
        self.segmentos = [s for s in self.segmentos if s.bloco != nome]
        del self.blocos[nome]
        self.liberados[nome] = dados
        return dados

    # -- serialization ------------------------------------------------
    def bloco_bytes(self, nome):
        inicio, fim = self.blocos[nome]
        partes = sorted((s for s in self.segmentos if s.bloco == nome), key=lambda s: s.base)
        saida, cursor = bytearray(), inicio
        for s in partes:
            if s.base != cursor:
                raise ErroMapaMemoria(f'Block {nome} has a hole at 0x{cursor:08x}')
            saida += s.bytes()
            cursor = s.fim
        if cursor != fim:
            raise ErroMapaMemoria(f'Block {nome} ends at 0x{cursor:08x}, expected 0x{fim:08x}')
        return bytes(saida)

    def serializar(self):
        self.empurrar()
        return {nome: (self.blocos[nome][0], self.bloco_bytes(nome)) for nome in self.blocos}

    def dono(self, endereco):
        """Symbolic owner of one address (segment owner), for mismatch reports."""
        for s in self.segmentos:
            if s.base <= endereco < s.fim:
                return s.dono, endereco - s.base
        return None, None

    def memoria_declarada(self, regioes):
        """AI-runtime MemoriaDeclarada over the byte segments only (list-backed ranges excluded)."""
        from memoria_ia_runtime import MemoriaDeclarada
        return MemoriaDeclarada([(s.base, s.vista) for s in self.segmentos if s.tipo == 'bytes'], regioes)
