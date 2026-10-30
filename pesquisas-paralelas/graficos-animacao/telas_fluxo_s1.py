"""Bounded S1 AffGame result/objectives drawing, independent of gameplay-frame ABI1.9.

Mode0x13 returns immediately in the intact caller (0x417ef3..0x417f2f). Mode0x11 uses the caller's explicit
menu-bank provider and Economy's resolved RechercheGetBranche result before restoring the normal glyph bank.
MenuInit, mission advance, research updates and loading menu backgrounds remain external dependencies.
"""
from graficos import compor_indices,ler_cmp
from telas_objetivos_s1 import compor_objetivos_s1
from texto_bitmap_nativo import DependenciaTextoBitmap

class BancoInventeS1:
    """Read-only original72-frame INVENTE.CMP; raw menu-bank IDs start at1 independently of STRAT IDs."""
    def __init__(self,catalogo):
        self.quadros=ler_cmp(catalogo._ler('cd/INSTALHD/GRAPHICS/INVENTE.CMP'))
        if len(self.quadros)!=72:raise ValueError('Unexpected INVENTE.CMP frame count')
    def quadro(self,ident):
        if type(ident) is not int or not 1<=ident<=72:raise ValueError('Menu bob ID outside INVENTE.CMP')
        return self.quadros[ident-1]

def compor_affgame_s1(memoria,superficie,*,catalogo,catalogo_menu=None,ramo_pesquisa_u16=None):
    """Return pixels, ordered raster calls and clip effects; no memory or caller surface mutates.

    catalogo_menu must explicitly represent the bank SetBank selects; it is never guessed from the normal
    catalog. S1 selects INVENTE.CMP before the animation and restores STRAT before drawing text.
    Production menu-bank loading and any other branch/animation phase remain named dependencies.
    """
    if len(superficie)!=480000:raise ValueError('Expected800x600 indexed surface')
    modo=memoria.u8(0x4e2f78)
    if modo==0x13:return dict(pixels=bytes(superficie),chamadas=[],efeitos=[])
    if modo!=0x11:raise DependenciaTextoBitmap(0x4176a8,'Only captured S1 result/objectives modes are supported')
    if catalogo_menu is None:raise DependenciaTextoBitmap(0x418590,'The selected menu bank must be supplied explicitly')
    if type(ramo_pesquisa_u16) is not int or ramo_pesquisa_u16!=0:
        raise DependenciaTextoBitmap(0x4717b1,'S1 objectives require the actual captured research-branch result0')
    if memoria.u8(0x508041)!=0:raise DependenciaTextoBitmap(0x41783a,'Uncaptured menu player')
    phase=memoria.u16(0x508f84)&15
    if phase not in (1,2,3):raise DependenciaTextoBitmap(0x417765,'Menu animation outside the three captured S1 phases')
    ident=1+phase
    out=compor_indices(superficie,800,600,catalogo_menu.quadro(ident),397,484)
    result=compor_objetivos_s1(memoria,out,catalogo=catalogo)
    result['chamadas'].insert(0,['PasteBobCmp',397,484,ident,0])
    return result
