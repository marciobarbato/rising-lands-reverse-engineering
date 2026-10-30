"""Native S1 MessageBoxAffiche; Core owns the complete InitGameZone translation."""
from quadro_jogo import DependenciaQuadro
from hud_scriptado_m3 import afftext,write
from ambiente_graficos_core import zonas_core


class DependenciaZonasAlerta(Exception):
    def __init__(self,address,reason):self.address,self.reason=address,reason;super().__init__(reason)


def stop(h,address,reason):
    raise DependenciaQuadro(address,reason,superficie=bytes(h.saida),chamadas=h.chamadas,efeitos=h.efeitos)


class MemoriaZonasGrafica:
    """Read-only caller memory plus ordered native-width stores in a local overlay."""
    def __init__(self,m):self.m,self.overlay,self.stores,self.changed=m,{},[],[]
    def value(self,address,width,value=None):
        old=int.from_bytes(bytes(self.overlay.get(address+i,self.m.u8(address+i)) for i in range(width)),'little')
        if value is None:return old
        value&=(1<<(8*width))-1
        self.stores.append((address,width,value))
        if value!=old:self.changed.append((address,width,value))
        self.overlay.update({address+i:v for i,v in enumerate(value.to_bytes(width,'little'))})
        return value
    def u8(self,address,value=None):return self.value(address,1,value)
    def u16(self,address,value=None):return self.value(address,2,value)
    def u32(self,address,value=None):return self.value(address,4,value)


def planejar_zonas(m,camera):
    """Core InitGameZone(1,0), with the actual Graphics message geometry domain."""
    if (m.u16(0x49a018),m.u16(0x49a01a),m.u16(0x508724),m.u16(0x508726),m.u8(0x508f90),camera)!=(800,600,25,17,0,0):
        raise DependenciaZonasAlerta(0x471830,'Alert outside captured 800x600 margin0 camera0 geometry')
    memory=MemoriaZonasGrafica(m)
    zonas_core().iniciar_zonas_jogo(memory,1,0)
    return memory


def reset_zones(h):
    try:plan=planejar_zonas(h.m,h.camera)
    except DependenciaZonasAlerta as error:stop(h,error.address,error.reason)
    h.chamadas.append(['InitGameZone',1,0])
    for address,width,value in plan.stores:write(h,'InitGameZone',address,value,width)


def escritas_zonas(m,plan):
    """Logical input-zone outputs; these stores must never become display-only mask bytes."""
    return tuple(plan.changed)


def message_box(h):
    """MessageBoxAffiche0x469c44 consumes actual bytes already in the native queue."""
    m=h.m;index=m.u16(0x507d54)
    if index==m.u16(0x507d56):return
    if index>=256:stop(h,0x469c5f,'Message queue index outside256 original slots')
    base=0x4e7754+518*index
    if m.u16(base+0x104)==399:return
    if m.u16(base+0x102)!=0xffff:stop(h,0x469d7f,'Two-line message queue wrapping is not proved')
    reset_zones(h)
    if m.u8(base+0x106):h.bob(0,480,0x2f3d+(m.u32(0x508f80)&31),True)
    text=bytearray()
    for i in range(128):
        value=m.u8(base+4+i)
        if not value:break
        text.append(value)
    else:stop(h,0x469d61,'Message line exceeds the proved bounded bitmap cursor')
    afftext(h,dict(text=bytes(text),x=0,y=496,right=768,bottom=512,font=1,flags=(0,1)))
