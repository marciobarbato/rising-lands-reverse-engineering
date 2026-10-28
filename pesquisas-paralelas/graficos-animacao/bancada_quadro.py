"""Native AffGame 0x417698 in-game frames over declared bindings.

AffGame, CalculFrame, EvenementEnCours, DDLockSurface, AffTerrain, AffSprite
and every renderer execute unchanged inside the whole code section. Declared
bindings: the Stage 16 bank/memory bindings, KERNEL32 GetTickCount (IAT
0x5231B8) and the DirectDraw surface methods IsLost/Lock/Restore/Unlock
reached through the COM object at 0x4E1790. The run stops at the HUD
checkpoint 0x417B1C or at AffGame's own return; whole writable memory is
diffed so every write made while drawing is observed.
"""
import struct
from bancada_x86 import RETORNO, PILHA, UNIDADE, SUPERFICIE
from bancada_ciclo_cache import BancadaCicloCache, TRAMPOLINS, ARENA
from vinculos_graficos import ParadaVinculo

CODIGO = (0x401000, 0x493c00)
DADOS = (0x494000, 0x522400)  # DGROUP + .bss
CHECKPOINT_HUD = 0x417B1C
LARGURA, ALTURA = 800, 600
COM_OBJETO = TRAMPOLINS+0x400
COM_VTABELA = TRAMPOLINS+0x500
# (vtable offset, IDirectDrawSurface method, stdcall argument count incl. this)
METODOS_COM = ((0x60, 'IsLost', 1), (0x64, 'Lock', 5), (0x6c, 'Restore', 1), (0x80, 'Unlock', 2))
RENDERIZADORES = {0x41068e: 'AffTerrain', 0x416864: 'AffSprite', 0x415acf: 'AffVeget', 0x407dd3: 'AffBatiments',
    0x40f49b: 'AffBatimentOmbre', 0x41591f: 'AffEngin', 0x46ff70: 'AffProjectile', 0x40fd95: 'GetNumBob',
    0x45c72a: 'AffBloc', 0x410085: 'AffVegetTerrain', 0x43f710: 'CalculFrame', 0x43f3b4: 'DDLockSurface',
    0x45c912: 'Box'}
LIMITE_QUADRO = dict(instrucoes=60_000_000, timeout_us=900_000_000)


class SuperficieDirectDraw:
    """IDirectDrawSurface fixture: never lost; Lock fills lpSurface/lPitch.

    Honored: IsLost -> DD_OK; Lock(NULL rect, DDSURFACEDESC dwSize 0x6C,
    DDLOCK_WAIT, NULL event) -> DD_OK with lpSurface (+0x24) and lPitch
    (+0x10). Restore and any other argument shape stop.
    """
    def __init__(self, *, registro, endereco_u32, pitch_u32):
        self.registro, self.endereco, self.pitch = registro, endereco_u32, pitch_u32

    def is_lost(self, this):
        return self.registro.registrar('IDirectDrawSurface::IsLost', (this,), 0)

    def lock(self, this, retangulo, descritor_tamanho, flags, evento):
        argumentos = (this, retangulo, descritor_tamanho, flags, evento)
        if retangulo != 0 or descritor_tamanho != 0x6c or flags != 1 or evento != 0:
            raise ParadaVinculo('IDirectDrawSurface::Lock', argumentos, 'only whole-surface DDLOCK_WAIT locks are honored')
        return self.registro.registrar('IDirectDrawSurface::Lock', argumentos, 0)

    def restore(self, this):
        raise ParadaVinculo('IDirectDrawSurface::Restore', (this,), 'lost-surface restoration is not honored')

    def unlock(self, this, ponteiro):
        raise ParadaVinculo('IDirectDrawSurface::Unlock', (this, ponteiro), 'unlock is outside the world-view prefix')


class RelogioDeclarado:
    """KERNEL32 GetTickCount returning a declared tick sequence."""
    def __init__(self, ticks, *, registro):
        self.ticks, self.registro = list(ticks), registro

    def __call__(self):
        if not self.ticks:
            raise ParadaVinculo('GetTickCount', (), 'declared tick sequence exhausted')
        return self.registro.registrar('GetTickCount', (), self.ticks.pop(0))


class BancadaQuadro(BancadaCicloCache):
    def __init__(self, catalogo):
        self.rastro = None; self.parar_evento = None; self.evento_parada = None
        super().__init__(catalogo)
        # ProgInit order: PaletteAlloc 0x474DAA precedes LoadSTRATBank/SetBank/CacheAlloc.
        r = self.executar(0x45f6e1, [(0x45f6e1, 0x45f760), (0x467ea6, 0x467ecb)], {'EAX': 0, 'EDX': 0x2468ace1})
        if r['EIP'] != RETORNO: raise RuntimeError('PaletteAlloc did not return')
        self.shadow, self.eclairage = self.u32(0x4e24b4), self.u32(0x4e24b8)
        self.carregar_banco()
        self.mundo = {}
        for nome, ponteiro, tamanho in (('terreno', 0x507d70, 131072), ('objetos', 0x507d74, 65536),
                ('auxiliares', 0x507dac, 65536), ('atributos', 0x507da8, 65536), ('regioes', 0x4e0f38, 131072),
                ('projeteis', 0x5080f0, 5600)):
            p = self.alocar(tamanho); self.escrever(ponteiro, struct.pack('<I', p)); self.mundo[nome] = p
        self.contagem_luz = []
        for camera in range(4):
            p = self.alocar(65536); self.escrever(0x507d98+4*camera, struct.pack('<I', p)); self.contagem_luz.append(p)
        self.directdraw = SuperficieDirectDraw(registro=self.registro, endereco_u32=SUPERFICIE, pitch_u32=LARGURA)
        self.escrever(0x4e1790, struct.pack('<I', COM_OBJETO)); self.escrever(COM_OBJETO, struct.pack('<I', COM_VTABELA))
        for indice, (deslocamento, nome, argumentos) in enumerate(METODOS_COM):
            trampolim = TRAMPOLINS+0x200+16*indice
            self.escrever(COM_VTABELA+deslocamento, struct.pack('<I', trampolim))
            self.vinculos[trampolim] = self._com(nome, argumentos)
        self.relogio = RelogioDeclarado([], registro=self.registro)
        trampolim = TRAMPOLINS+0x300; self.escrever(0x5231b8, struct.pack('<I', trampolim))
        self.vinculos[trampolim] = self._get_tick_count
        self.resolucao_iat.append(dict(slot='0x5231b8', importacao='KERNEL32.GetTickCount', trampolim=hex(trampolim)))

    def _com(self, nome, argumentos):
        def stdcall(b):
            esp = b.reg('ESP'); valores = struct.unpack('<%dI' % (argumentos+1), b.ler(esp, 4*(argumentos+1)))
            if valores[1] != COM_OBJETO:
                raise ParadaVinculo('IDirectDrawSurface::'+nome, valores[1:], 'unknown COM object')
            if nome == 'IsLost': r = b.directdraw.is_lost(valores[1])
            elif nome == 'Restore': r = b.directdraw.restore(valores[1])
            elif nome == 'Unlock': r = b.directdraw.unlock(*valores[1:])
            else:
                descritor = valores[3]; tamanho = struct.unpack('<I', b.ler(descritor, 4))[0]
                r = b.directdraw.lock(valores[1], valores[2], tamanho, valores[4], valores[5])
                b.escrever(descritor+0x10, struct.pack('<I', b.directdraw.pitch))
                b.escrever(descritor+0x24, struct.pack('<I', b.directdraw.endereco))
            b.reg('EAX', r); b.reg('ESP', esp+4+4*argumentos); b.reg('EIP', valores[0])
        return stdcall

    @staticmethod
    def _get_tick_count(b):
        esp = b.reg('ESP'); retorno = struct.unpack('<I', b.ler(esp, 4))[0]
        b.reg('EAX', b.relogio()); b.reg('ESP', esp+4); b.reg('EIP', retorno)

    def _hook(self, cpu, endereco, tamanho, dados):
        if self.rastro is not None and endereco in RENDERIZADORES:
            nome = RENDERIZADORES[endereco]
            if nome != 'AffBatimentOmbre' or struct.unpack('<I', self.ler(self.reg('ESP'), 4))[0] == 0x416bd7:
                i16 = lambda v: (v+32768) % 65536-32768
                evento = [nome, i16(self.reg('EAX')), i16(self.reg('EDX')), self.reg('EBX') & 0xffff]
                self.rastro.append(evento)
                if self.parar_evento is not None and len(self.rastro)-1 == self.parar_evento:
                    self.evento_parada = evento; cpu.emu_stop(); return
        super()._hook(cpu, endereco, tamanho, dados)

    def regioes_mutaveis(self):
        return [('dados', DADOS[0], DADOS[1]-DADOS[0]), ('heap', 0x4000000, self.proximo-0x4000000),
            ('arena', ARENA, self.arena.proximo-ARENA), ('unidades', UNIDADE, 220800),
            ('superficie', SUPERFICIE, LARGURA*ALTURA)]

    def fotografia(self):
        return {nome: self.ler(inicio, n) for nome, inicio, n in self.regioes_mutaveis()}

    @staticmethod
    def diferencas(antes, depois, ignorar=()):
        """Changed byte runs {region: [[offset, old_hex, new_hex], ...]}."""
        saida = {}
        for nome in antes:
            if nome in ignorar: continue
            a, d = antes[nome], depois[nome]
            if a == d: continue
            corridas = []; i = 0; n = len(a)
            while i < n:
                if a[i] != d[i]:
                    j = i
                    while j < n and a[j] != d[j]: j += 1
                    corridas.append([i, a[i:j].hex(), d[i:j].hex()]); i = j
                else:
                    # Skip equal stretches quickly.
                    k = i+4096
                    if k <= n and a[i:k] == d[i:k]: i = k
                    else: i += 1
            saida[nome] = corridas
        return saida

    def calcular_tabelas_jogador(self):
        """ProgInit 0x474F3D: native CalculTabPlayer into PaletteAlloc's tables."""
        r = self.executar(0x45ff61, [(0x45ff61, 0x46003b), (0x45fdd9, 0x45fddf)], {'EAX': self.u32(0x4e24b0), 'EDX': 4})
        if r['EIP'] != RETORNO: raise RuntimeError('CalculTabPlayer did not return')
        return [self.ler(self.u32(0x4e24c8+4*i), 256) for i in range(5)]

    def carregar_cena(self, cena, *, tabela_sombra, tabela_eclairage, fundo, globais_nomes):
        """Write one scene's explicit inputs; the cache/bank lifecycle persists."""
        m = cena['mundo']
        for nome in ('terreno', 'objetos', 'auxiliares', 'atributos', 'regioes', 'projeteis'):
            self.escrever(self.mundo[nome], m[nome])
        for camera in range(4):
            self.escrever(self.maps[0][camera], m['descoberta'][camera]); self.expected_maps[0][camera] = bytearray(m['descoberta'][camera])
            self.escrever(self.maps[1][camera], m['iluminacao'][camera]); self.expected_maps[1][camera] = bytearray(m['iluminacao'][camera])
            self.escrever(self.contagem_luz[camera], m['contagem_luz'][camera])
        self.escrever(UNIDADE, m['unidades']); self.escrever(0x49a0c8, m['estruturas'])
        self.escrever(self.shadow, tabela_sombra); self.escrever(self.eclairage, tabela_eclairage)
        self.escrever(SUPERFICIE, fundo)
        for nome, endereco, largura in globais_nomes:
            self.escrever(endereco, cena['globais'][nome])

    def quadro(self, *, ticks, parar_evento=None):
        """Run AffGame from its entry; stop at the HUD checkpoint or return."""
        self.relogio = RelogioDeclarado(ticks, registro=self.registro)
        self.rastro = []; self.parar_evento = parar_evento; self.evento_parada = None
        marca = self.registro.marca(); antes_instr = self.instrucoes
        self.execucoes += 1; self.intervalos = [CODIGO]; self.paradas = {RETORNO, CHECKPOINT_HUD}; self.stubs = dict(self.vinculos)
        for nome in ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP'): self.reg(nome, 0)
        self.reg('EFLAGS', 2); self.reg('ESP', PILHA+0x8000)
        self.escrever(PILHA, bytes(0x10000)); self.escrever(PILHA+0x8000, struct.pack('<I', RETORNO))
        self.cpu.emu_start(0x417698, RETORNO, timeout=LIMITE_QUADRO['timeout_us'], count=LIMITE_QUADRO['instrucoes'])
        eip = self.reg('EIP'); rastro = self.rastro; self.rastro = None
        if self.evento_parada is None and eip not in (RETORNO, CHECKPOINT_HUD):
            raise RuntimeError(f'AffGame frame exceeded its declared budget at 0x{eip:08x}')
        return dict(eip=eip, esp=self.reg('ESP'), rastro=rastro, evento_parada=self.evento_parada,
            vinculos=self.registro.desde(marca), instrucoes=self.instrucoes-antes_instr)
