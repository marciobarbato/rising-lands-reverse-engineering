"""Native GetNumBob cache lifecycle over declared Windows/C-runtime bindings.

LoadSTRATBank, SetBank, MemAlloc/MemFree, the game's File* wrappers,
CacheAlloc, InitCache, GetNumBob and CacheFree execute unchanged. Only the
five KERNEL32 Global* imports (IAT slots resolved to binding trampolines, as
the Windows loader would) and the statically linked C-runtime fopen/fread/
fclose are bound. Cached payloads are the bank's own allocations: no
synthetic payload binding. Explicit inputs (visibility maps, shadow table,
camera, bank path prefix) stay harness-owned and are reported as such.
"""
import struct
from bancada_x86 import RETORNO, PILHA
from validar_composicao import BancadaComposicao
from vinculos_graficos import (RegistroVinculos, ArenaGlobalFixa, ArquivosDeclarados, ParadaVinculo,
    PADRAO_NAO_INICIALIZADO)
from cache_terreno import RAW_BLOCK, SLOTS, FIRST_CACHED_ID

ARENA, ARENA_BYTES = 0x10000000, 0x2000000
TRAMPOLINS = 0x0E000000
# (IAT slot, KERNEL32 import, stdcall argument count)
IMPORTACOES = ((0x5231c0, 'GlobalAlloc', 2), (0x5231c8, 'GlobalFree', 1), (0x5231cc, 'GlobalHandle', 1),
    (0x5231d0, 'GlobalLock', 1), (0x5231d8, 'GlobalUnlock', 1))
CRT = ((0x48c71f, 'fopen'), (0x48c80b, 'fclose'), (0x48c97b, 'fread'))
PREFIXO_CAMINHO = 0x509494
TABELA_NOMES = 0x495bc8
PONTEIRO_CHAVES, CURSOR, CAPACIDADE, CONTADOR_MEMORIA, TABELA_BANCO = 0x49a050, 0x49a04e, 0x495bc4, 0x4e2f3c, 0x508f6c
INTERVALOS = dict(
    LoadSTRATBank=[(0x41877a, 0x4189c2), (0x467ea6, 0x467ecb), (0x458420, 0x458430), (0x45844c, 0x458476)],
    SetBank=[(0x418590, 0x418599)],
    CacheAlloc=[(0x40fa18, 0x40fa2e), (0x467ea6, 0x467ecb)],
    InitCache=[(0x40fa38, 0x40fa72)],
    CacheFree=[(0x40fa2e, 0x40fa38), (0x467ecb, 0x467ef4)],  # MemFree falls into MemClose RET
    GetNumBob=[(0x40fd95, 0x410085), (0x4766d6, 0x4766f0), (0x47693a, 0x476968), (0x476702, 0x47670a),
        (0x45c779, 0x45c8df), (0x45f7ba, 0x45f7d8), (0x45f6de, 0x45f6e1)])
RAMOS = {0x40fdb8: 'undiscovered', 0x40fe06: 'direct', 0x40fe6c: 'hit', 0x40fedd: 'miss'}
LIMITE_BANCO = dict(instrucoes=4_000_000, timeout_us=300_000_000)
PRESERVADOS = dict(EBX=0xcafebabe, ECX=0x13579bdf, EDX=0x2468ace1, ESI=0x2468ace0, EDI=0x0badf00d, EBP=0x7f112233)


class BancadaCicloCache(BancadaComposicao):
    def __init__(self, catalogo, *, prefixo=b''):
        self.ramo = None; self.vinculos = {}
        super().__init__(); self.catalogo = catalogo
        self.cpu.mem_map(ARENA, ARENA_BYTES); self.cpu.mem_map(TRAMPOLINS, 0x1000)
        self.registro = RegistroVinculos()
        self.arena = ArenaGlobalFixa(inicio_u32=ARENA, tamanho_u32=ARENA_BYTES, registro=self.registro,
            preencher=lambda endereco, n: self.escrever(endereco, bytes([PADRAO_NAO_INICIALIZADO])*n))
        self.estado_carga = dict(ponteiro_chaves_u32=self.u32(PONTEIRO_CHAVES), cursor_u16=self.u16(CURSOR),
            contador_memoria_u32=self.u32(CONTADOR_MEMORIA), capacidade_u16=self.u16(CAPACIDADE))
        nomes = [self.ler_c(self.u32(TABELA_NOMES+4*i)) for i in range(6)]
        self.prefixo = prefixo.decode('ascii'); self.escrever(PREFIXO_CAMINHO, prefixo+b'\0')
        arquivos = {}; self.arquivos_declarados = []
        for nome in nomes:
            disco = 'cd/INSTALHD/GRAPHICS/'+nome.split('\\')[-1].upper(); dados = catalogo._ler(disco)
            arquivos[self.prefixo+nome] = dados
            self.arquivos_declarados.append(dict(nome=self.prefixo+nome, copia='fontes/'+disco, bytes=len(dados)))
        self.arquivos = ArquivosDeclarados(arquivos, registro=self.registro)
        self.resolucao_iat = []
        for indice, (slot, nome, argumentos) in enumerate(IMPORTACOES):
            trampolim = TRAMPOLINS+16*indice; self.escrever(slot, struct.pack('<I', trampolim))
            self.vinculos[trampolim] = self._windows(nome, argumentos)
            self.resolucao_iat.append(dict(slot=hex(slot), importacao='KERNEL32.'+nome, trampolim=hex(trampolim)))
        self.vinculos.update({0x48c71f: BancadaCicloCache._fopen, 0x48c80b: BancadaCicloCache._fclose,
            0x48c97b: BancadaCicloCache._fread})
        self.maps = []; self.expected_maps = []
        for global_pointer in (0x507d78, 0x507d88):
            pointers = []; expected = []
            for camera in range(4):
                pointer = self.alocar(65536); payload = bytearray([16])*65536
                self.escrever(pointer, payload); pointers.append(pointer); expected.append(payload)
                self.escrever(global_pointer+camera*4, struct.pack('<I', pointer))
            self.maps.append(pointers); self.expected_maps.append(expected)
        self.shadow = self.alocar(256); self.escrever(0x4e24b4, struct.pack('<I', self.shadow))
        self.banco = None

    # Fixed-width reads of original globals.
    def u16(self, endereco): return struct.unpack('<H', self.ler(endereco, 2))[0]
    def u32(self, endereco): return struct.unpack('<I', self.ler(endereco, 4))[0]

    def ler_c(self, endereco):
        dados = self.ler(endereco, 260)
        if b'\0' not in dados:
            raise ParadaVinculo('C string', (endereco,), 'no terminator within 260 bytes')
        return dados.split(b'\0')[0].decode('ascii')

    def _windows(self, nome, argumentos):
        metodo = getattr(self.arena, {'GlobalAlloc': 'global_alloc', 'GlobalFree': 'global_free',
            'GlobalHandle': 'global_handle', 'GlobalLock': 'global_lock', 'GlobalUnlock': 'global_unlock'}[nome])
        def stdcall(b):
            esp = b.reg('ESP'); valores = struct.unpack('<%dI' % (argumentos+1), b.ler(esp, 4*(argumentos+1)))
            b.reg('EAX', metodo(*valores[1:])); b.reg('ESP', esp+4+4*argumentos); b.reg('EIP', valores[0])
        return stdcall

    @staticmethod
    def _fopen(b):
        b.retornar_stub(b.arquivos.fopen(b.ler_c(b.reg('EAX')), b.ler_c(b.reg('EDX'))))

    @staticmethod
    def _fread(b):
        dados, quantidade = b.arquivos.fread(b.reg('EAX'), b.reg('EDX'), b.reg('EBX'), b.reg('ECX'))
        b.escrever(b.reg('EAX'), dados); b.retornar_stub(quantidade)

    @staticmethod
    def _fclose(b):
        b.retornar_stub(b.arquivos.fclose(b.reg('EAX')))

    def _hook(self, cpu, endereco, tamanho, dados):
        ramo = RAMOS.get(endereco)
        if ramo is not None: self.ramo = ramo
        super()._hook(cpu, endereco, tamanho, dados)

    def executar(self, entrada, intervalos, regs=None, paradas=(), stubs=None, limite=100000):
        todos = dict(self.vinculos); todos.update(stubs or {})
        return super().executar(entrada, intervalos, regs, paradas, todos, limite)

    def executar_declarado(self, entrada, intervalos, regs=None, *, instrucoes, timeout_us):
        """Same entry protocol as Bancada.executar with an explicit larger budget."""
        self.execucoes += 1; self.intervalos = intervalos; self.paradas = {RETORNO}; self.stubs = dict(self.vinculos)
        for nome in ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP'): self.reg(nome, 0)
        self.reg('EFLAGS', 2); self.reg('ESP', PILHA+0x8000)
        self.escrever(PILHA, bytes(0x10000)); self.escrever(PILHA+0x8000, struct.pack('<I', RETORNO))
        for nome, valor in (regs or {}).items(): self.reg(nome, valor)
        self.cpu.emu_start(entrada, RETORNO, timeout=timeout_us, count=instrucoes)
        if self.reg('EIP') != RETORNO:
            raise RuntimeError('Declared bank-loading budget reached before return')
        return {nome: self.reg(nome) for nome in ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP', 'EIP')}

    def _rotina(self, nome, regs=None, limite=100000):
        entrada = INTERVALOS[nome][0][0]; antes = self.instrucoes
        r = self.executar(entrada, INTERVALOS[nome], dict(PRESERVADOS, **(regs or {})), limite=limite)
        if r['EIP'] != RETORNO or r['ESP'] != 0x2008004:
            raise RuntimeError(nome+' did not reach its original return')
        r['instrucoes'] = self.instrucoes-antes
        return r

    def carregar_banco(self):
        """ProgInit order 0x474e9b..0x474eaa: LoadSTRATBank then SetBank."""
        if self.banco is not None: raise RuntimeError('Bank already loaded')
        marca = self.registro.marca(); antes = self.instrucoes
        r = self.executar_declarado(0x41877a, INTERVALOS['LoadSTRATBank'], dict(PRESERVADOS),
            instrucoes=LIMITE_BANCO['instrucoes'], timeout_us=LIMITE_BANCO['timeout_us'])
        banco = r['EAX']; quantidade = self.u16(banco); tabela = self.u32(banco+4)
        self._rotina('SetBank', dict(EAX=banco))
        if self.u32(TABELA_BANCO) != tabela: raise RuntimeError('SetBank did not publish the table')
        self.banco = dict(banco=banco, tabela=tabela, quantidade=quantidade, registradores=r,
            instrucoes=self.instrucoes-antes, marca_vinculos=(marca, self.registro.marca()))
        return self.banco

    def descritor(self, id_motor):
        ponteiro = self.u32(self.banco['tabela']+(id_motor-1)*4)
        largura, altura, tamanho, dados = struct.unpack('<HHII', self.ler(ponteiro, 12))
        return dict(descritor=ponteiro, largura=largura, altura=altura, tamanho=tamanho, dados=dados)

    def blocos_cache(self):
        partes = []
        for slot in range(SLOTS):
            d = self.descritor(FIRST_CACHED_ID+slot)
            if (d['largura'], d['altura'], d['tamanho']) != (32, 32, RAW_BLOCK):
                raise RuntimeError('Cached bank descriptor left the verified 32x32/1056 domain')
            partes.append(self.ler(d['dados'], RAW_BLOCK))
        return b''.join(partes)

    def estado(self):
        ponteiro = self.u32(PONTEIRO_CHAVES)
        return dict(ponteiro_chaves_u32=ponteiro, cursor_u16=self.u16(CURSOR), contador_memoria_u32=self.u32(CONTADOR_MEMORIA),
            capacidade_u16=self.u16(CAPACIDADE), chaves=self.ler(ponteiro, SLOTS*4) if ponteiro else None,
            blocos=self.blocos_cache() if self.banco else None)

    def cache_alloc(self):
        marca = self.registro.marca(); r = self._rotina('CacheAlloc')
        return r, self.registro.desde(marca)

    def init_cache(self):
        return self._rotina('InitCache')

    def cache_free(self):
        marca = self.registro.marca(); r = self._rotina('CacheFree')
        return r, self.registro.desde(marca)

    def get_num_bob(self, fonte_u16, descoberta_u8, iluminacao_u8, celula_u16, camera_u8, tabela):
        self.escrever(0x508041, bytes([camera_u8])); self.escrever(self.shadow, tabela)
        for indice, flag in enumerate((descoberta_u8, iluminacao_u8)):
            self.escrever(self.maps[indice][camera_u8]+celula_u16, bytes([flag]))
            self.expected_maps[indice][camera_u8][celula_u16] = flag
        self.ramo = None; marca = self.registro.marca()
        r = self._rotina('GetNumBob', dict(EAX=fonte_u16, EDX=celula_u16), limite=300000)
        for nome in ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'):
            if r[nome] != PRESERVADOS[nome]: raise RuntimeError('GetNumBob changed callee-saved '+nome)
        if self.ramo is None or self.registro.marca() != marca: raise RuntimeError('Unexpected GetNumBob path')
        return r['EAX'], self.ramo

    def verificar_entradas(self):
        for indice in (0, 1):
            for camera in range(4):
                if self.ler(self.maps[indice][camera], 65536) != bytes(self.expected_maps[indice][camera]):
                    raise RuntimeError('Visibility input changed')
        if self.u16(CAPACIDADE) != 256 or self.u32(0x4e24b4) != self.shadow:
            raise RuntimeError('Static capacity or shadow pointer changed')
