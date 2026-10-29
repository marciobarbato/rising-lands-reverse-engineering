"""Explicit inherited memory registry for a future original MissionLoad oracle.

This module neither constructs game state nor loads/composes a mission.
Every byte and its provenance must come from the caller's declared input.
"""
from dataclasses import dataclass
import hashlib
import struct

DATA_BASE,DATA_SIZE=0x494000,0x8f000
POINTERS=((0x507da8,65536,'attributes'),(0x507d70,131072,'tiles'),
          (0x507d74,65536,'objects'),(0x507dac,65536,'object_auxiliary'),
          (0x4e0f38,131072,'regions'),(0x4e156c,65536,'structure_colors'),
          (0x4e19a0,220800,'units'),(0x4e19b8,16,'type_Bag_pointers'),
          (0x5080a8,80,'live_players'),(0x5080ac,80,'stored_players'),
          (0x5080f0,5600,'projectiles'),(0x4e1924,3200,'route_pointers'),
          (0x507db0,702,'obstacle_markers'))


@dataclass(frozen=True)
class BlocoHerdadoMissao:
    nome:str
    endereco:int
    dados:object
    proveniencia:str

    def __post_init__(self):
        view=memoryview(self.dados)
        if (not self.nome or not self.proveniencia or view.ndim!=1 or
                view.format!='B' or not view.c_contiguous or not len(view) or
                not 0<=self.endereco<self.endereco+len(view)<=0x100000000):
            raise ValueError('Inherited blocks require explicit contiguous bytes, address and provenance')


@dataclass(frozen=True)
class EstadoHerdadoMissao:
    revisao_origem:str
    descricao:str
    blocos:tuple

    def __post_init__(self):
        if not self.revisao_origem or not self.descricao or not self.blocos:
            raise ValueError('Declare an identified inherited state; no constructor defaults')
        if len({b.nome for b in self.blocos})!=len(self.blocos):
            raise ValueError('Inherited block IDs must be unique')
        ordered=sorted(self.blocos,key=lambda b:b.endereco)
        for left,right in zip(ordered,ordered[1:]):
            if left.endereco+len(left.dados)>right.endereco:
                raise ValueError('Declare overlapping views as aliases of one backing block')
        self.vista(DATA_BASE,DATA_SIZE)

    def vista(self,endereco,tamanho):
        if not isinstance(endereco,int) or not isinstance(tamanho,int) or endereco<0 or tamanho<0:
            raise ValueError('Declare an exact nonnegative memory range')
        for bloco in self.blocos:
            offset=endereco-bloco.endereco
            if 0<=offset and offset+tamanho<=len(bloco.dados):
                return memoryview(bloco.dados)[offset:offset+tamanho]
        raise ValueError(f'Inherited range is undeclared:0x{endereco:x}/{tamanho}')

    def ponteiro(self,slot,tamanho):
        address=struct.unpack('<I',self.vista(slot,4))[0]
        self.vista(address,tamanho)
        return address

    def validar_fechamento_m1(self):
        """Validate live pointers/aliases; never manufacture a missing pool."""
        aliases={name:dict(slot=hex(slot),base=hex(self.ponteiro(slot,size)),bytes=size)
                 for slot,size,name in POINTERS}
        for table in (0x507d78,0x507d88,0x507d98):
            for owner in range(4):
                self.ponteiro(table+owner*4,65536)
        bags=self.ponteiro(0x4e19b8,16)
        for owner in range(4):
            self.ponteiro(bags+owner*4,2704)
        routes=self.ponteiro(0x4e1924,3200)
        for unit in range(800):
            self.ponteiro(routes+unit*4,512)
        if self.vista(0x496fe4,1)[0]!=1:
            raise ValueError('This oracle proposal targets explicit mission byte1/MONDE01 only')
        live=self.ponteiro(0x5080a8,80);stored=self.ponteiro(0x5080ac,80)
        return dict(aliases=aliases,
            live_player_types=[self.vista(live+20*p+1,1)[0] for p in range(4)],
            stored_player_types=[self.vista(stored+20*p+1,1)[0] for p in range(4)])

    def manifesto(self):
        return dict(source_revision=self.revisao_origem,description=self.descricao,
            blocks=[dict(id=b.nome,base=hex(b.endereco),bytes=len(b.dados),
                         sha256=hashlib.sha256(b.dados).hexdigest(),provenance=b.proveniencia)
                    for b in self.blocos])
