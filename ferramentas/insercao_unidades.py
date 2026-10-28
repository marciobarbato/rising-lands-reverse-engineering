"""Shared physical insertion tail used by original mission/production entries."""
import struct


class DependenciaInsercaoUnidade(NotImplementedError):
    def __init__(self,unidade,checkpoint):
        self.unidade,self.endereco,self.checkpoint=unidade,0x476851,checkpoint
        super().__init__('Vision radius above the validated 0..8 sum requires DecouvreTerrain; '
                         'prior record/collision effects retained')


def _preparar_insercao(mundo,indice,celula=None):
    indice &= 65535
    u=mundo.unidades
    if not isinstance(u,bytearray) or len(u) != 220800 or indice >= 800:
        raise ValueError('Insertion requires a writable 800-record pool and unit 0..799')
    p=indice*276
    if celula is None:
        celula=struct.unpack_from('<H',u,p+8)[0]
    celula &= 65535
    if (not 1 <= mundo.largura <= 256 or not 1 <= mundo.altura <= 256
            or not 0 <= mundo.jogador_local < 4 or mundo.tamanho_minimapa != (128,128)
            or (celula & 255) >= mundo.largura or (celula >> 8) >= mundo.altura):
        raise ValueError('Insertion requires an in-map cell/camera and 128x128 minimap')
    if u[p+1] >= 26 or u[p] not in (0,1,2,3,4,200):
        raise ValueError('Insertion requires known type 0..25 and owner 0..3/4/200')
    return indice,celula,p


def _aplicar_insercao(mundo,indice,celula,dependencia):
    u,p=mundo.unidades,indice*276
    mundo.ocupar(indice,celula,True)
    u[p+0x72]=1
    atual=struct.unpack_from('<H',u,p+8)[0]
    dono=u[p]
    if dono not in (4,200):
        raio=u[p+0xbb]+u[p+0xf5]
        if raio > 8:
            raise dependencia(indice)
        mundo.descobrir_area(atual,raio+2,dono)
        raio=u[p+0xbb]+u[p+0xf5]
        mundo.iluminar_area(atual,raio,u[p])
    mundo.minimapa(u[p],atual,4)
