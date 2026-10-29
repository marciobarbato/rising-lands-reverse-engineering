"""Declared DirectDraw backend for the display-executing Missions oracle (interim).

The intact program reaches DirectDraw only through the import
``DDRAW.DirectDrawCreate`` (IAT 0x5234c4) and COM vtables.  This module
answers them with declared objects: every method a native run reaches is a
``backend`` binding on its own trampoline that records the exact arguments
and returns a declared HRESULT; every other vtable slot is a trap that stops
the run with the interface name and offset.  No engine body is replaced.

Surfaces are declared memory regions outside the allocation arena; their
pixels are display output, never game state.  Lock fills dwHeight, dwWidth,
lPitch and lpSurface of the caller's DDSURFACEDESC (dwFlags gains
DDSD_HEIGHT|DDSD_WIDTH|DDSD_PITCH|DDSD_LPSURFACE).  Graphics owns the final
display backend; this module is replaced when it lands.  Importing this module
executes nothing.
"""
import struct

import ambiente_missoes  # noqa: F401  (bootstrap of the flat module path)
from vinculos_declarados import ParadaVinculoDeclarado

REGIAO_COM = 0x3600000          # objects, vtables and trampolines (one 64 KiB page set)
REGIAO_SUPERFICIES = 0x60000000  # declared surface pixels
DD_OK = 0

# (offset, method, stdcall argument count including ``this``)
IDIRECTDRAW = {0x08: ('Release', 1), 0x14: ('CreatePalette', 5), 0x18: ('CreateSurface', 4),
               0x28: ('FlipToGDISurface', 1), 0x4c: ('RestoreDisplayMode', 1),
               0x50: ('SetCooperativeLevel', 3), 0x54: ('SetDisplayMode', 4)}
IDIRECTDRAWSURFACE = {0x08: ('Release', 1), 0x14: ('Blt', 6), 0x1c: ('BltFast', 6), 0x2c: ('Flip', 3),
                      0x44: ('GetDC', 2), 0x60: ('IsLost', 1), 0x64: ('Lock', 5), 0x68: ('ReleaseDC', 2),
                      0x6c: ('Restore', 1), 0x7c: ('SetPalette', 2), 0x80: ('Unlock', 2)}
IDIRECTDRAWPALETTE = {0x08: ('Release', 1), 0x18: ('SetEntries', 5)}
VTABELAS = (('IDirectDraw', IDIRECTDRAW, 0x5c), ('IDirectDrawSurface', IDIRECTDRAWSURFACE, 0x90),
            ('IDirectDrawPalette', IDIRECTDRAWPALETTE, 0x1c))


class DirectDrawDeclarado:
    """Declared DirectDraw objects bound on a ``BancadaX86``-derived bench."""
    def __init__(self, bancada, *, preenchimento_superficie=0, metodos=None):
        self.b, self.cpu = bancada, bancada.cpu
        self.preenchimento = preenchimento_superficie
        self.metodos_honrados = metodos   # optional subset {(interface, method)} to honor
        self.objetos = {}                 # pointer -> dict(interface, ...)
        self.chamadas = []
        self.paleta = None
        self.cpu.mem_map(REGIAO_COM, 0x10000)
        self.cpu.mem_write(REGIAO_COM, bytes(0x10000))
        self.cpu.mem_map(REGIAO_SUPERFICIES, 0x400000)
        self._proximo_objeto, self._proxima_superficie = REGIAO_COM+0x8000, REGIAO_SUPERFICIES
        self.vtabelas = {}
        trampolim = REGIAO_COM
        for i, (interface, metodos, tamanho) in enumerate(VTABELAS):
            vt = REGIAO_COM+0x4000+0x100*i
            self.vtabelas[interface] = vt
            for deslocamento in range(0, tamanho, 4):
                self.cpu.mem_write(trampolim, b'\xc3')
                if deslocamento in metodos:
                    nome, n = metodos[deslocamento]
                    bancada.declarar_vinculo(trampolim, f'{interface}::{nome}', tuple(4+4*k for k in range(n)),
                                             self._despachar(interface, nome), desempilhar=4*n, natureza='backend')
                else:
                    bancada.declarar_vinculo(trampolim, f'{interface}+0x{deslocamento:x}', (4,),
                                             self._armadilha(interface, deslocamento), natureza='backend')
                self.cpu.mem_write(vt+deslocamento, struct.pack('<I', trampolim))
                trampolim += 16

    # ------------------------------------------------------------ objects
    def _novo(self, interface, **atributos):
        p = self._proximo_objeto
        self._proximo_objeto += 0x40
        self.cpu.mem_write(p, struct.pack('<I', self.vtabelas[interface]))
        self.objetos[p] = dict(interface=interface, referencias=1, **atributos)
        return p

    def _superficie(self, largura, altura, papel):
        tamanho = largura*altura
        p = self._proxima_superficie
        self._proxima_superficie += (tamanho+0xffff) & ~0xffff
        if self._proxima_superficie > REGIAO_SUPERFICIES+0x400000:
            raise ParadaVinculoDeclarado('Declared surface region exhausted')
        self.cpu.mem_write(p, bytes([self.preenchimento])*tamanho)
        return self._novo('IDirectDrawSurface', largura=largura, altura=altura, pitch=largura, pixels=p,
                          papel=papel, travada=False)

    def criar(self, chamada):
        """DDRAW.DirectDrawCreate(lpGUID, lplpDD, pUnkOuter)."""
        guid, destino, externo = chamada.argumentos
        if guid != 0 or externo != 0:
            raise ParadaVinculoDeclarado('DirectDrawCreate outside the declared default-driver call')
        self.modo = None
        p = self._novo('IDirectDraw')
        chamada.escrever(destino, struct.pack('<I', p))
        self.chamadas.append(dict(method='DirectDrawCreate', object=hex(p)))
        return DD_OK

    def _objeto(self, this, interface):
        o = self.objetos.get(this)
        if o is None or o['interface'] != interface:
            raise ParadaVinculoDeclarado(f'{interface} method on an undeclared object 0x{this:x}')
        return o

    def _armadilha(self, interface, deslocamento):
        def atender(chamada):
            raise ParadaVinculoDeclarado(f'Undeclared COM method {interface}+0x{deslocamento:x}')
        return atender

    def _despachar(self, interface, nome):
        def atender(chamada):
            if self.metodos_honrados is not None and (interface, nome) not in self.metodos_honrados:
                raise ParadaVinculoDeclarado(f'{interface}::{nome} is not honored by this backend')
            o = self._objeto(chamada.argumentos[0], interface)
            r = getattr(self, f'_{interface[1:].lower()}_{nome.lower()}')(chamada, o)
            self.chamadas.append(dict(method=f'{interface}::{nome}', args=[hex(a) for a in chamada.argumentos],
                                      result=hex(r)))
            return r
        return atender

    # ------------------------------------------------------------ IDirectDraw
    def _directdraw_release(self, c, o):
        o['referencias'] -= 1
        return o['referencias']

    def _directdraw_setcooperativelevel(self, c, o):
        return DD_OK

    def _directdraw_setdisplaymode(self, c, o):
        _, w, h, bpp = c.argumentos
        if bpp != 8:
            raise ParadaVinculoDeclarado('SetDisplayMode outside the declared 8-bit modes')
        self.modo = (w, h)
        return DD_OK

    def _directdraw_restoredisplaymode(self, c, o):
        return DD_OK

    def _directdraw_fliptogdisurface(self, c, o):
        return DD_OK

    def _directdraw_createsurface(self, c, o):
        _, desc, destino, externo = c.argumentos
        tamanho, flags, altura, largura = struct.unpack('<4I', c.ler(desc, 16))
        caps = struct.unpack('<I', c.ler(desc+0x68, 4))[0]
        if tamanho != 0x6c or externo != 0:
            raise ParadaVinculoDeclarado('CreateSurface descriptor outside the declared DDSURFACEDESC')
        if caps & 0x200:                                 # DDSCAPS_PRIMARYSURFACE
            if self.modo is None:
                raise ParadaVinculoDeclarado('Primary surface before SetDisplayMode')
            p = self._superficie(*self.modo, 'primary')
        elif flags & 0x6 == 0x6 and caps & 0x40:         # DDSD_HEIGHT|DDSD_WIDTH, DDSCAPS_OFFSCREENPLAIN
            p = self._superficie(largura, altura, 'offscreen')
        else:
            raise ParadaVinculoDeclarado(f'CreateSurface flags 0x{flags:x} caps 0x{caps:x} outside fixture')
        c.escrever(destino, struct.pack('<I', p))
        return DD_OK

    def _directdraw_createpalette(self, c, o):
        _, flags, entradas, destino, externo = c.argumentos
        if externo != 0:
            raise ParadaVinculoDeclarado('CreatePalette aggregation outside fixture')
        p = self._novo('IDirectDrawPalette', flags=flags, entries=c.ler(entradas, 1024))
        c.escrever(destino, struct.pack('<I', p))
        return DD_OK

    # ------------------------------------------------------------ IDirectDrawSurface
    def _directdrawsurface_release(self, c, o):
        o['referencias'] -= 1
        return o['referencias']

    def _directdrawsurface_islost(self, c, o):
        return DD_OK

    def _directdrawsurface_restore(self, c, o):
        return DD_OK

    def _directdrawsurface_lock(self, c, o):
        _, retangulo, desc, flags, evento = c.argumentos
        if retangulo != 0 or evento != 0 or o['travada']:
            raise ParadaVinculoDeclarado('Only whole-surface, non-nested, eventless locks are declared')
        dw = struct.unpack('<I', c.ler(desc, 4))[0]
        if dw != 0x6c:
            raise ParadaVinculoDeclarado('Lock descriptor outside the declared DDSURFACEDESC')
        flags_desc = struct.unpack('<I', c.ler(desc+4, 4))[0] | 0x100e
        c.escrever(desc+4, struct.pack('<5I', flags_desc, o['altura'], o['largura'], o['pitch'],
                                       struct.unpack('<I', c.ler(desc+0x14, 4))[0]))
        c.escrever(desc+0x24, struct.pack('<I', o['pixels']))
        o['travada'] = True
        return DD_OK

    def _directdrawsurface_unlock(self, c, o):
        o['travada'] = False
        return DD_OK

    def _directdrawsurface_setpalette(self, c, o):
        _, paleta = c.argumentos
        if paleta and paleta not in self.objetos:
            raise ParadaVinculoDeclarado('SetPalette with an undeclared palette')
        o['paleta'] = paleta
        return DD_OK

    def _directdrawsurface_flip(self, c, o):
        raise ParadaVinculoDeclarado('IDirectDrawSurface::Flip is not declared yet')

    def _directdrawsurface_blt(self, c, o):
        raise ParadaVinculoDeclarado('IDirectDrawSurface::Blt is not declared yet')

    def _directdrawsurface_bltfast(self, c, o):
        """BltFast(dest, x, y, src, RECT*, flags): exact copy; only DDBLTFAST_WAIT, in-bounds, non-null RECT."""
        _, x, y, fonte, retangulo, flags = c.argumentos
        f = self._objeto(fonte, 'IDirectDrawSurface')
        if flags != 0x10 or retangulo == 0 or f is o:
            raise ParadaVinculoDeclarado('BltFast outside the declared DDBLTFAST_WAIT copy between two surfaces')
        esquerda, topo, direita, base = struct.unpack('<4i', c.ler(retangulo, 16))
        largura, altura = direita-esquerda, base-topo
        if (min(esquerda, topo, x, y) < 0 or largura <= 0 or altura <= 0 or direita > f['largura']
                or base > f['altura'] or x+largura > o['largura'] or y+altura > o['altura']):
            raise ParadaVinculoDeclarado('BltFast rectangle outside the declared surfaces')
        for linha in range(altura):
            dados = self.cpu.mem_read(f['pixels']+(topo+linha)*f['pitch']+esquerda, largura)
            self.cpu.mem_write(o['pixels']+(y+linha)*o['pitch']+x, bytes(dados))
        return DD_OK

    def _directdrawsurface_getdc(self, c, o):
        raise ParadaVinculoDeclarado('IDirectDrawSurface::GetDC (GDI) is not declared')

    def _directdrawsurface_releasedc(self, c, o):
        raise ParadaVinculoDeclarado('IDirectDrawSurface::ReleaseDC (GDI) is not declared')

    # ------------------------------------------------------------ IDirectDrawPalette
    def _directdrawpalette_release(self, c, o):
        o['referencias'] -= 1
        return o['referencias']

    def _directdrawpalette_setentries(self, c, o):
        _, flags, inicio, quantidade, entradas = c.argumentos
        if inicio+quantidade > 256:
            raise ParadaVinculoDeclarado('SetEntries beyond 256 entries')
        o['entries'] = o['entries'][:4*inicio] + c.ler(entradas, 4*quantidade) + o['entries'][4*(inicio+quantidade):]
        return DD_OK

    def resumo(self):
        return dict(objects={hex(p): {k: (hex(v) if isinstance(v, int) else v) for k, v in o.items()
                                      if k != 'entries'} for p, o in self.objetos.items()},
                    calls=len(self.chamadas), mode=getattr(self, 'modo', None))
