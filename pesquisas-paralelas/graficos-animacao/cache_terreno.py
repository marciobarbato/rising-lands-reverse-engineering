"""Original GetNumBob cache: explicit 256-key/raw-block state and mask order."""
import struct
from composicao import compor_sombra
from graficos import compor_indices


SLOTS=256
RAW_BLOCK=1056
FIRST_CACHED_ID=1090
MASK_IDS=(None,1085,1084,1088,1083,1081,1087,1081,1082,1089,1081,1081,1086,1081,1081,1081)


class CacheTerreno:
    """Own mutable copies of explicit key/payload snapshots; no startup defaults."""
    def __init__(self,registros,blocos_crus,*,proximo_u16):
        self.registros=bytearray(registros);self.blocos_crus=bytearray(blocos_crus);self.proximo_u16=proximo_u16
        self.validar()

    def validar(self):
        if not isinstance(self.registros,bytearray) or len(self.registros)!=SLOTS*4:
            raise ValueError('Expected 256 four-byte cache records')
        if not isinstance(self.blocos_crus,bytearray) or len(self.blocos_crus)!=SLOTS*RAW_BLOCK:
            raise ValueError('Expected 256 raw 1056-byte block payloads')
        if type(self.proximo_u16) is not int or not 0<=self.proximo_u16<SLOTS:
            raise ValueError('Expected replacement cursor0..255')

    def pixels(self,indice_u8):
        self.validar()
        if type(indice_u8) is not int or not 0<=indice_u8<SLOTS:raise ValueError('Expected cache slot0..255')
        raw=self.blocos_crus[indice_u8*RAW_BLOCK:(indice_u8+1)*RAW_BLOCK]
        return b''.join(raw[row*33+1:row*33+33] for row in range(32))


def _u8(value,name):
    if type(value) is not int or not 0<=value<=255:raise ValueError(name+' must be raw u8')


def resolver_bloco_terreno(catalogo,cache,*,id_terreno_u16,descoberta_u8,iluminacao_u8,tabela_sombra):
    """Return a plan/engine ID, mutating only an explicit graphics cache on miss.

    Inputs are already-selected camera bytes, not ETA attributes. Copy sources
    on misses are verified full-literal32x32 blocks1..1081. Hidden/direct/hit
    paths do not fetch an asset; direct raw IDs do not prove drawable assets.
    """
    if not isinstance(cache,CacheTerreno):raise ValueError('Expected explicit CacheTerreno state')
    cache.validar()
    if type(id_terreno_u16) is not int or not 0<=id_terreno_u16<=65535:raise ValueError('Expected raw u16 terrain ID')
    _u8(descoberta_u8,'descoberta_u8');_u8(iluminacao_u8,'iluminacao_u8')
    if len(tabela_sombra)!=256:raise ValueError('Expected explicit256-byte shadow table')
    table=bytes(tabela_sombra)
    if descoberta_u8&16:return dict(id_motor=1081,motivo='undiscovered',indice_cache=None)
    fog=descoberta_u8&15;light=15 if iluminacao_u8&16 else iluminacao_u8&15
    if fog==0 and light==0:return dict(id_motor=id_terreno_u16,motivo='direct',indice_cache=None)
    key=struct.pack('<HBB',id_terreno_u16,light,fog)
    for slot in range(SLOTS):
        if cache.registros[slot*4:slot*4+4]==key:
            return dict(id_motor=FIRST_CACHED_ID+slot,motivo='hit',indice_cache=slot,
                mascara_iluminacao_u8=light,mascara_descoberta_u8=fog)
    if not 1<=id_terreno_u16<=1081:
        raise NotImplementedError('A miss requires a verified full-literal static block1..1081')
    source=catalogo.quadro(id_terreno_u16);raw=bytes(source.comprimido)
    if (source.largura,source.altura)!=(32,32) or len(raw)!=RAW_BLOCK or any(raw[y*33]!=224 for y in range(32)):
        raise NotImplementedError('Copy source is outside the verified raw32x33 block domain')
    light_frame=catalogo.quadro(MASK_IDS[light]) if MASK_IDS[light] is not None else None
    fog_frame=catalogo.quadro(MASK_IDS[fog]) if MASK_IDS[fog] is not None else None
    for frame in (light_frame,fog_frame):
        if frame is not None and ((frame.largura,frame.altura)!=(32,32) or len(frame.pixels)!=1024 or len(frame.opacidade)!=1024):
            raise ValueError('Expected verified32x32 terrain masks')
    slot=cache.proximo_u16;offset=slot*RAW_BLOCK
    # Original visible order: key word, lighting byte, discovery byte, cursor,
    # raw copy, destination remap mask, then literal fog-mask copy.
    struct.pack_into('<H',cache.registros,slot*4,id_terreno_u16)
    cache.registros[slot*4+2]=light;cache.registros[slot*4+3]=fog
    cache.proximo_u16=(slot+1)%SLOTS;cache.blocos_crus[offset:offset+RAW_BLOCK]=raw
    pixels=cache.pixels(slot)
    if light_frame is not None:
        pixels=compor_sombra(pixels,32,32,light_frame,0,0,table)
        for row in range(32):cache.blocos_crus[offset+row*33+1:offset+row*33+33]=pixels[row*32:row*32+32]
    if fog_frame is not None:
        pixels=compor_indices(pixels,32,32,fog_frame,0,0)
        for row in range(32):cache.blocos_crus[offset+row*33+1:offset+row*33+33]=pixels[row*32:row*32+32]
    return dict(id_motor=FIRST_CACHED_ID+slot,motivo='miss',indice_cache=slot,
        mascara_iluminacao_u8=light,mascara_descoberta_u8=fog)
