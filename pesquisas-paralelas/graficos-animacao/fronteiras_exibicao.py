"""Declared DirectDraw display backend for the Core16 binding API (no engine body is replaced).

The original wrappers (AffInit/DDInit, DDLockSurface, DDUnlockSurface, DDFlipPage, DDSetPalette, ResetMode, RestoreAll,
AffGame, ...) execute natively. Their only external boundaries are DirectDrawCreate (IAT 0x5234C4, reached through the
jmp thunk 0x493A30) and the COM methods they call through the object pointers 0x4E1788 (IDirectDraw), 0x4E178C (primary),
0x4E1790 (offscreen 800x600) and 0x4E179C (palette). This module supplies those COM objects as declared handlers.

Everything is read from the original calls: surface geometry from the DDSURFACEDESC the original builds (DDInit), the
display mode from SetDisplayMode, pixels from the guest memory it blits. Surfaces are explicit buffers inside the declared
region (8 bpp, pitch = width). Declared fixture answers: surfaces are never lost; every call that succeeds returns DD_OK.
Any COM slot without a handler, unsupported flag, rectangle outside a surface, double lock or unknown object stops the run
with ParadaVinculoDeclarado. Importing this module executes nothing; ``instalar`` maps memory and declares bindings.
"""
import struct
from dataclasses import dataclass, field

from vinculos_declarados import ParadaVinculoDeclarado

DD_OK = 0
IAT_DIRECTDRAWCREATE = 0x5234c4   # DDRAW.dll DirectDrawCreate; DDInit calls it via thunk 0x493A30 (jmp [0x5234C4])
IAT_MESSAGEBEEP = 0x5232ac        # DDUtil_TreatError 0x43F145; reached only on an error path
OBJETOS_GLOBAIS = dict(dd=0x4e1788, primaria=0x4e178c, offscreen=0x4e1790, paleta=0x4e179c)

# DirectDraw v1 vtable (names from the SDK interface order; every offset used by the wrappers is confirmed in
# inventario-fronteiras-exibicao.json): (offset, name, stdcall argument words including `this`).
VT_DD = ((0x00, 'QueryInterface', 3), (0x04, 'AddRef', 1), (0x08, 'Release', 1), (0x0c, 'Compact', 1), (0x10, 'CreateClipper', 4),
    (0x14, 'CreatePalette', 5), (0x18, 'CreateSurface', 4), (0x1c, 'DuplicateSurface', 3), (0x20, 'EnumDisplayModes', 5),
    (0x24, 'EnumSurfaces', 5), (0x28, 'FlipToGDISurface', 1), (0x2c, 'GetCaps', 3), (0x30, 'GetDisplayMode', 2),
    (0x34, 'GetFourCCCodes', 3), (0x38, 'GetGDISurface', 2), (0x3c, 'GetMonitorFrequency', 2), (0x40, 'GetScanLine', 2),
    (0x44, 'GetVerticalBlankStatus', 2), (0x48, 'Initialize', 2), (0x4c, 'RestoreDisplayMode', 1),
    (0x50, 'SetCooperativeLevel', 3), (0x54, 'SetDisplayMode', 4), (0x58, 'WaitForVerticalBlank', 3))
VT_SUPERFICIE = ((0x00, 'QueryInterface', 3), (0x04, 'AddRef', 1), (0x08, 'Release', 1), (0x0c, 'AddAttachedSurface', 2),
    (0x10, 'AddOverlayDirtyRect', 2), (0x14, 'Blt', 6), (0x18, 'BltBatch', 4), (0x1c, 'BltFast', 6), (0x20, 'DeleteAttachedSurface', 3),
    (0x24, 'EnumAttachedSurfaces', 3), (0x28, 'EnumOverlayZOrders', 4), (0x2c, 'Flip', 3), (0x30, 'GetAttachedSurface', 3),
    (0x34, 'GetBltStatus', 2), (0x38, 'GetCaps', 2), (0x3c, 'GetClipper', 2), (0x40, 'GetColorKey', 3), (0x44, 'GetDC', 2),
    (0x48, 'GetFlipStatus', 2), (0x4c, 'GetOverlayPosition', 3), (0x50, 'GetPalette', 2), (0x54, 'GetPixelFormat', 2),
    (0x58, 'GetSurfaceDesc', 2), (0x5c, 'Initialize', 3), (0x60, 'IsLost', 1), (0x64, 'Lock', 5), (0x68, 'ReleaseDC', 2),
    (0x6c, 'Restore', 1), (0x70, 'SetClipper', 2), (0x74, 'SetColorKey', 3), (0x78, 'SetOverlayPosition', 3),
    (0x7c, 'SetPalette', 2), (0x80, 'Unlock', 2), (0x84, 'UpdateOverlay', 6), (0x88, 'UpdateOverlayDisplay', 2),
    (0x8c, 'UpdateOverlayZOrder', 3))
VT_PALETA = ((0x00, 'QueryInterface', 3), (0x04, 'AddRef', 1), (0x08, 'Release', 1), (0x0c, 'GetCaps', 2), (0x10, 'GetEntries', 5),
    (0x14, 'Initialize', 4), (0x18, 'SetEntries', 5))

DDSD_CAPS, DDSD_HEIGHT, DDSD_WIDTH = 1, 2, 4
DDSCAPS_PRIMARYSURFACE, DDSCAPS_OFFSCREENPLAIN, DDSCAPS_SYSTEMMEMORY = 0x200, 0x40, 0x800
DDSCL_FLAGS_ORIGINAL = 0x13       # DDInit pushes 0x13 for SetCooperativeLevel
DDPCAPS_8BIT_ALLOW256 = 0x44      # DDSetPalette pushes 0x44 for CreatePalette
DDLOCK_WAIT = 1
DDBLTFAST_WAIT = 0x10
MODOS_SUPORTADOS = ((800, 600), (640, 480))  # DDInit 0x43F519 / 0x43F53E


@dataclass
class Superficie:
    objeto: int          # guest COM object address
    base: int            # pixel buffer
    largura: int
    altura: int
    pitch: int
    papel: str           # 'primaria' | 'offscreen'
    bloqueada: int = 0   # lock pointer returned, or 0
    paleta: int = 0


@dataclass
class Paleta:
    objeto: int
    entradas: bytes      # 256 PALETTEENTRY (R,G,B,flags)


class ExibicaoDeclarada:
    """Declared COM display objects. ``base``: first byte of a region this module maps for objects/trampolines;
    ``base_superficies``: separate region for the pixel buffers. Both must be free in the bench's address space and the
    trampoline region must be whitelisted as executable by the bench (see ``regiao_executavel``)."""

    def __init__(self, *, base=0x3600000, tamanho=0x10000, base_superficies=0x3800000, tamanho_superficies=0x200000):
        self.base, self.tamanho = base, tamanho
        self.base_superficies, self.tamanho_superficies = base_superficies, tamanho_superficies
        self.cursor_objetos = base+0x4000      # objects after the trampoline page(s)
        self.cursor_superficies = base_superficies
        self.superficies, self.paletas = {}, {}
        self.dd = 0
        self.modo = None
        self.cooperacao = None
        self.eventos = []          # ordered backend log (method, key arguments)
        self._cpu = None
        self.trampolins = {}

    @property
    def regiao_executavel(self):
        """(start, end) the bench must allow execution to fetch from (trampoline `ret` bytes live here)."""
        return (self.base, self.base+0x4000)

    # ---------------------------------------------------------------- installation
    def instalar(self, bancada):
        """Map regions, build the vtables, declare every binding. ``bancada``: a Core16 bench (declarar_vinculo,
        declarar_importacao, importacoes_originais, cpu)."""
        cpu = self._cpu = bancada.cpu
        for inicio, n in ((self.base, self.tamanho), (self.base_superficies, self.tamanho_superficies)):
            cpu.mem_map(inicio, n)
        simbolo = bancada.importacoes_originais.get(IAT_DIRECTDRAWCREATE)
        if not simbolo or simbolo['symbol'] != 'DirectDrawCreate':
            raise ValueError('IAT 0x5234C4 is not DDRAW.DirectDrawCreate in this image')
        mensagem = bancada.importacoes_originais.get(IAT_MESSAGEBEEP)
        if not mensagem or mensagem['symbol'] != 'MessageBeep':
            raise ValueError('IAT 0x5232AC is not USER32.MessageBeep in this image')
        proximo = [self.base]

        def trampolim(nome, argumentos, atender, desempilhar):
            alvo = proximo[0]; proximo[0] += 16
            if proximo[0] > self.base+0x4000: raise ValueError('Trampoline region exhausted')
            cpu.mem_write(alvo, b'\xc3')
            bancada.declarar_vinculo(alvo, nome, tuple(4+4*i for i in range(argumentos)), atender,
                desempilhar=desempilhar, natureza='backend')
            self.trampolins[alvo] = nome
            return alvo

        def vtable(interface, tabela, metodos):
            endereco = self._alocar_objeto(4*len(tabela))
            for deslocamento, nome, argumentos in tabela:
                atender = metodos.get(nome)
                if atender is None:
                    atender = self._sem_semantica(interface, nome)
                    alvo = trampolim(f'{interface}::{nome}', argumentos, atender, 0)
                else:
                    alvo = trampolim(f'{interface}::{nome}', argumentos, atender, 4*argumentos)
                cpu.mem_write(endereco+deslocamento, struct.pack('<I', alvo))
            return endereco
        self._vt_dd = vtable('IDirectDraw', VT_DD, dict(CreatePalette=self._criar_paleta, CreateSurface=self._criar_superficie,
            SetCooperativeLevel=self._cooperacao, SetDisplayMode=self._modo))
        self._vt_superficie = vtable('IDirectDrawSurface', VT_SUPERFICIE, dict(IsLost=self._perdida, Restore=self._restaurar,
            Lock=self._bloquear, Unlock=self._desbloquear, BltFast=self._bltfast, SetPalette=self._definir_paleta))
        self._vt_paleta = vtable('IDirectDrawPalette', VT_PALETA, dict(SetEntries=self._entradas))
        self.dd = self._alocar_objeto(4); cpu.mem_write(self.dd, struct.pack('<I', self._vt_dd))
        bancada.declarar_importacao(IAT_DIRECTDRAWCREATE, 'DDRAW.DirectDrawCreate', 3, self._direct_draw_create)
        bancada.declarar_importacao(IAT_MESSAGEBEEP, 'USER32.MessageBeep', 1, self._beep)
        return self

    def _alocar_objeto(self, n):
        endereco = self.cursor_objetos; self.cursor_objetos += (n+15) & ~15
        if self.cursor_objetos > self.base+self.tamanho: raise ValueError('Object region exhausted')
        return endereco

    def _alocar_pixels(self, n):
        endereco = self.cursor_superficies; self.cursor_superficies += (n+4095) & ~4095
        if self.cursor_superficies > self.base_superficies+self.tamanho_superficies: raise ValueError('Surface region exhausted')
        return endereco

    @staticmethod
    def _sem_semantica(interface, nome):
        def atender(chamada):
            raise ParadaVinculoDeclarado(f'{interface}::{nome} has no declared display semantics')
        return atender

    def _log(self, metodo, **dados):
        self.eventos.append(dict(method=metodo, **dados))

    def _u32(self, chamada, endereco): return struct.unpack('<I', chamada.ler(endereco, 4))[0]

    # ---------------------------------------------------------------- DirectDrawCreate
    def _direct_draw_create(self, chamada):
        guid, destino, agregado = chamada.argumentos
        if guid != 0 or agregado != 0:
            raise ParadaVinculoDeclarado('DirectDrawCreate: only the default driver without aggregation is declared')
        chamada.escrever(destino, struct.pack('<I', self.dd)); self._log('DirectDrawCreate', out=hex(destino))
        return DD_OK

    def _beep(self, chamada):
        raise ParadaVinculoDeclarado('MessageBeep reached from DDUtil_TreatError: a DirectDraw call failed')

    # ---------------------------------------------------------------- IDirectDraw
    def _exigir_dd(self, chamada):
        if chamada.argumentos[0] != self.dd: raise ParadaVinculoDeclarado('IDirectDraw method on an unknown object')

    def _cooperacao(self, chamada):
        self._exigir_dd(chamada); _, hwnd, flags = chamada.argumentos
        if flags != DDSCL_FLAGS_ORIGINAL:
            raise ParadaVinculoDeclarado(f'SetCooperativeLevel flags 0x{flags:x} differ from the original 0x13')
        self.cooperacao = (hwnd, flags); self._log('SetCooperativeLevel', hwnd=hwnd, flags=flags)
        return DD_OK

    def _modo(self, chamada):
        self._exigir_dd(chamada); _, largura, altura, bpp = chamada.argumentos
        if (largura, altura) not in MODOS_SUPORTADOS or bpp != 8:
            raise ParadaVinculoDeclarado(f'SetDisplayMode {largura}x{altura}x{bpp} is outside the original 800x600/640x480 8bpp modes')
        self.modo = (largura, altura); self._log('SetDisplayMode', width=largura, height=altura, bpp=bpp)
        return DD_OK

    def _criar_paleta(self, chamada):
        self._exigir_dd(chamada); _, flags, tabela, destino, agregado = chamada.argumentos
        if flags != DDPCAPS_8BIT_ALLOW256 or agregado != 0 or tabela == 0:
            raise ParadaVinculoDeclarado('CreatePalette: only an explicit 256-entry 8-bit palette without aggregation is declared')
        objeto = self._alocar_objeto(4); self._cpu.mem_write(objeto, struct.pack('<I', self._vt_paleta))
        self.paletas[objeto] = Paleta(objeto, chamada.ler(tabela, 1024))
        chamada.escrever(destino, struct.pack('<I', objeto)); self._log('CreatePalette', palette=hex(objeto))
        return DD_OK

    def _criar_superficie(self, chamada):
        self._exigir_dd(chamada); _, descritor, destino, agregado = chamada.argumentos
        if agregado != 0: raise ParadaVinculoDeclarado('CreateSurface: aggregation is not declared')
        tamanho, flags, altura, largura = struct.unpack('<IIII', chamada.ler(descritor, 16))
        caps = self._u32(chamada, descritor+0x68)
        if tamanho != 0x6c: raise ParadaVinculoDeclarado('CreateSurface: DDSURFACEDESC dwSize is not 0x6C')
        if flags == DDSD_CAPS and caps == DDSCAPS_PRIMARYSURFACE:
            if self.modo is None: raise ParadaVinculoDeclarado('CreateSurface primary before SetDisplayMode')
            largura, altura = self.modo; papel = 'primaria'
        elif flags == DDSD_CAPS|DDSD_HEIGHT|DDSD_WIDTH and caps == DDSCAPS_OFFSCREENPLAIN|DDSCAPS_SYSTEMMEMORY:
            papel = 'offscreen'
        else:
            raise ParadaVinculoDeclarado(f'CreateSurface flags 0x{flags:x} caps 0x{caps:x} are outside the two original descriptors')
        if any(s.papel == papel for s in self.superficies.values()):
            raise ParadaVinculoDeclarado(f'CreateSurface: a {papel} surface already exists')
        objeto = self._alocar_objeto(4); self._cpu.mem_write(objeto, struct.pack('<I', self._vt_superficie))
        pixels = self._alocar_pixels(largura*altura)
        self.superficies[objeto] = Superficie(objeto, pixels, largura, altura, largura, papel)
        chamada.escrever(destino, struct.pack('<I', objeto))
        self._log('CreateSurface', role=papel, width=largura, height=altura, pitch=largura, pixels=hex(pixels), object=hex(objeto))
        return DD_OK

    # ---------------------------------------------------------------- IDirectDrawSurface
    def _superficie(self, endereco):
        s = self.superficies.get(endereco)
        if s is None: raise ParadaVinculoDeclarado('IDirectDrawSurface method on an unknown object')
        return s

    def _perdida(self, chamada):
        self._superficie(chamada.argumentos[0]); return DD_OK  # declared fixture: never lost

    def _restaurar(self, chamada):
        self._superficie(chamada.argumentos[0]); self._log('Restore', surface=hex(chamada.argumentos[0])); return DD_OK

    def _bloquear(self, chamada):
        s = self._superficie(chamada.argumentos[0]); _, retangulo, descritor, flags, evento = chamada.argumentos
        if retangulo != 0 or flags != DDLOCK_WAIT or evento != 0 or self._u32(chamada, descritor) != 0x6c:
            raise ParadaVinculoDeclarado('Lock: only a whole-surface DDLOCK_WAIT lock with a 0x6C descriptor is declared')
        if s.bloqueada: raise ParadaVinculoDeclarado('Lock on an already locked surface')
        s.bloqueada = s.base
        chamada.escrever(descritor+0x10, struct.pack('<I', s.pitch)); chamada.escrever(descritor+0x24, struct.pack('<I', s.base))
        self._log('Lock', role=s.papel, pixels=hex(s.base), pitch=s.pitch)
        return DD_OK

    def _desbloquear(self, chamada):
        s = self._superficie(chamada.argumentos[0]); ponteiro = chamada.argumentos[1]
        if not s.bloqueada or ponteiro != s.bloqueada:
            raise ParadaVinculoDeclarado('Unlock does not match the locked surface pointer')
        s.bloqueada = 0; self._log('Unlock', role=s.papel); return DD_OK

    def _bltfast(self, chamada):
        destino = self._superficie(chamada.argumentos[0]); _, x, y, origem_obj, retangulo, trans = chamada.argumentos
        origem = self._superficie(origem_obj)
        if trans != DDBLTFAST_WAIT or retangulo == 0:
            raise ParadaVinculoDeclarado('BltFast: only DDBLTFAST_WAIT with an explicit source rectangle is declared')
        if destino.bloqueada or origem.bloqueada: raise ParadaVinculoDeclarado('BltFast on a locked surface')
        esq, topo, dir_, base = struct.unpack('<4i', chamada.ler(retangulo, 16))
        if not (0 <= esq < dir_ <= origem.largura and 0 <= topo < base <= origem.altura
                and 0 <= x and x+dir_-esq <= destino.largura and 0 <= y and y+base-topo <= destino.altura):
            raise ParadaVinculoDeclarado(f'BltFast rectangle ({esq},{topo},{dir_},{base}) to ({x},{y}) is outside a surface')
        n = dir_-esq
        for linha in range(base-topo):
            dados = chamada.ler(origem.base+(topo+linha)*origem.pitch+esq, n)
            chamada.escrever(destino.base+(y+linha)*destino.pitch+x, dados)
        self._log('BltFast', dst=destino.papel, src=origem.papel, x=x, y=y, rect=[esq, topo, dir_, base])
        return DD_OK

    def _definir_paleta(self, chamada):
        s = self._superficie(chamada.argumentos[0]); paleta = chamada.argumentos[1]
        if paleta not in self.paletas: raise ParadaVinculoDeclarado('SetPalette with an unknown palette object')
        s.paleta = paleta; self._log('SetPalette', role=s.papel, palette=hex(paleta)); return DD_OK

    # ---------------------------------------------------------------- IDirectDrawPalette
    def _entradas(self, chamada):
        _, flags, inicio, quantidade, tabela = chamada.argumentos
        paleta = self.paletas.get(chamada.argumentos[0])
        if paleta is None: raise ParadaVinculoDeclarado('SetEntries on an unknown palette')
        if flags != 0 or inicio != 0 or quantidade != 256:
            raise ParadaVinculoDeclarado('SetEntries: only the whole 256-entry table with flags 0 is declared')
        paleta.entradas = chamada.ler(tabela, 1024); self._log('SetEntries', palette=hex(paleta.objeto))
        return DD_OK

    # ---------------------------------------------------------------- inspection
    def pixels(self, papel):
        s = next(s for s in self.superficies.values() if s.papel == papel)
        return bytes(self._cpu.mem_read(s.base, s.largura*s.altura))

    def manifesto(self):
        return dict(base=hex(self.base), surfaces_base=hex(self.base_superficies), mode=self.modo, cooperation=self.cooperacao,
            surfaces=[dict(role=s.papel, width=s.largura, height=s.altura, pitch=s.pitch, pixels=hex(s.base), object=hex(s.objeto))
                for s in self.superficies.values()], palettes=[hex(p.objeto) for p in self.paletas.values()],
            declared_fixture='surfaces are never lost; every supported call returns DD_OK', events=len(self.eventos))
