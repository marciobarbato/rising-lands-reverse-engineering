"""Intact original audio routines on the shared x86 bench, with declared bindings.

Windows imports (``_lopen``, ``_hread``, ``_llseek``, ``_lclose``,
``GlobalAlloc``, ``GlobalFree``, ``MessageBoxA``) are bound by writing stop
addresses into their original import slots. The DirectSound objects are COM
stubs whose vtable slots are stop addresses. The Watcom CRT ``getcwd`` and
``free`` entries are bound at their own entry points because they reach
``GetCurrentDirectoryA`` and the CRT heap. Every other instruction executed is
original code inside the declared intervals. A binding the fixture cannot
honor raises ``ParadaFixture``; ``MessageBoxA`` is always a declared stop.

The generic binding facility promised by core Stage 15 does not exist yet; this
front keeps its bindings here and will migrate to it when it is committed.
"""
import struct
import ambiente_audio
from emulador import BancadaX86, RETORNO, x86
from cenarios_som import ARENA, ARENA_TAMANHO, OBJETO_DIRECTSOUND
from provedores_som import ParadaFixture, SistemaFixo

DS_BASE, DS_TAMANHO = 0x6000000, 0x100000
DS_OBJETOS = 0x6100000
FIXOS = 0x5000000

SLOTS = {0x5231c0: 'GlobalAlloc', 0x5231c8: 'GlobalFree', 0x5231e8: '_hread',
         0x5231f0: '_lclose', 0x5231f8: '_llseek', 0x5231fc: '_lopen', 0x5232b0: 'MessageBoxA'}
ARGUMENTOS = {'GlobalAlloc': 2, 'GlobalFree': 1, '_hread': 3, '_lclose': 1, '_llseek': 3,
              '_lopen': 2, 'MessageBoxA': 4, 'CreateSoundBuffer': 4, 'Release': 1,
              'Lock': 8, 'Unlock': 5}
PARADA_IMPORTACAO = {nome: RETORNO + 0x100 + 0x10 * i for i, nome in enumerate(SLOTS.values())}
PARADA_COM = {'CreateSoundBuffer': RETORNO + 0x200, 'Release': RETORNO + 0x210,
              'Lock': RETORNO + 0x220, 'Unlock': RETORNO + 0x230, 'COM_nao_suportado': RETORNO + 0x2f0}
VTABELA_DS, OBJETO_DS = RETORNO + 0x800, OBJETO_DIRECTSOUND
VTABELA_DSB = RETORNO + 0xa00
GETCWD, FREE = 0x48c481, 0x48d7f4

# Original code intervals allowed to execute (the exported intervals, with the
# CRT limited to the bytes sprintf/memset actually reach). Decoders first for speed.
INTERVALOS = [(0x48b8c9, 0x48ba96), (0x48ba96, 0x48bd12), (0x48b844, 0x48b8c9),
              (0x48c008, 0x48c06e), (0x48c070, 0x48c202), (0x48c204, 0x48c2d7),
              (0x48b390, 0x48b3ea), (0x48b3ec, 0x48b791), (0x48b794, 0x48b843),
              (0x48a0f4, 0x48a14a), (0x48a834, 0x48aa04), (0x48aa79, 0x48aac0),
              (0x48aad4, 0x48abb9), (0x48c3b0, 0x48c3c8), (0x48d890, 0x48d942),
              (0x48cfa8, 0x48cfeb), (0x48efe8, 0x48fb01)]
# Loop heads used as retained-state checkpoints so that no segment exceeds the
# shared bench's instruction limit. Pairs alternate (see ``executar_chamada``).
PONTOS_M16 = (0x48b8dd, 0x48b905)
PONTOS_S16 = (0x48bab1, 0x48bacd)
RETORNO_DECODIFICADOR = 0x48c11a


class BancadaSom(BancadaX86):
    def __init__(self, arquivos, *, falhar_alocacao=(), diretorio_corrente=b'C:\\RISING'):
        super().__init__()
        self.cpu.mem_map(ARENA, ARENA_TAMANHO)
        self.cpu.mem_map(DS_BASE, DS_TAMANHO)
        self.cpu.mem_map(DS_OBJETOS, 0x10000)
        self.cpu.mem_map(FIXOS, 0x10000)
        self.sistema = SistemaFixo(arquivos, diretorio_corrente=diretorio_corrente, arena=ARENA,
                                   arena_tamanho=ARENA_TAMANHO, falhar_alocacao=falhar_alocacao)
        self.registro = self.sistema.registro
        self.arquivos, self.alocador = self.sistema.arquivos, self.sistema.alocador
        self.directsound = self.sistema.directsound
        self.instrucoes = 0
        self.observacoes = []
        self._ultimo = INTERVALOS[0]
        self.objetos_dsb = {}
        self.objeto_mapeado = None
        for slot, nome in SLOTS.items():
            self.cpu.mem_write(slot, struct.pack('<I', PARADA_IMPORTACAO[nome]))
        nao_suportado = struct.pack('<I', PARADA_COM['COM_nao_suportado'])
        self.cpu.mem_write(VTABELA_DS, nao_suportado * 32)
        self.cpu.mem_write(VTABELA_DS + 0xc, struct.pack('<I', PARADA_COM['CreateSoundBuffer']))
        self.cpu.mem_write(VTABELA_DSB, nao_suportado * 32)
        for deslocamento, nome in ((0x8, 'Release'), (0x2c, 'Lock'), (0x4c, 'Unlock')):
            self.cpu.mem_write(VTABELA_DSB + deslocamento, struct.pack('<I', PARADA_COM[nome]))
        self.cpu.mem_write(OBJETO_DS, struct.pack('<I', VTABELA_DS))
        self.paradas_base = (set(PARADA_IMPORTACAO.values()) | set(PARADA_COM.values())
                             | {GETCWD, FREE, RETORNO})

    def ativar_directsound(self):
        """Declared fixture: the IDirectSound pointer InitDirectSound would store."""
        if OBJETO_DS != RETORNO + 0x900:
            raise ValueError('Fixture IDirectSound object must sit in the stop page')
        self.cpu.mem_write(0x522228, struct.pack('<I', OBJETO_DS))

    def _conferir_endereco(self, cpu, endereco, tamanho, _):
        if endereco in self.paradas:
            cpu.emu_stop()
            return
        self.instrucoes += 1
        inicio, fim = self._ultimo
        if inicio <= endereco and endereco + tamanho <= fim:
            return
        for intervalo in self.permitidos:
            if intervalo[0] <= endereco and endereco + tamanho <= intervalo[1]:
                self._ultimo = intervalo
                return
        raise RuntimeError(f'Execução fora do trecho declarado: 0x{endereco:08x}')

    # -- memory helpers -------------------------------------------------
    def u32(self, endereco):
        return struct.unpack('<I', self.cpu.mem_read(endereco, 4))[0]

    def ler(self, endereco, tamanho):
        return bytes(self.cpu.mem_read(endereco, tamanho))

    def escrever(self, endereco, dados):
        self.cpu.mem_write(endereco, bytes(dados))

    def cadeia(self, endereco, limite=512):
        dados = self.ler(endereco, limite)
        if b'\0' not in dados:
            raise ParadaFixture('Unterminated string passed to a binding')
        return dados[:dados.index(b'\0')]

    # -- execution --------------------------------------------------------
    def executar_chamada(self, entrada, registradores=None, argumentos=(), pontos=(), limite=1000000):
        """Run one original call to its return, servicing bindings and checkpoints.

        ``pontos`` are retained-state checkpoints: a segment stops at any of them
        except the one it resumed from, so alternating loop heads bound every
        segment while the original code runs unchanged.
        """
        pilha = {4 + 4 * i: struct.pack('<I', valor & 0xffffffff) for i, valor in enumerate(argumentos)}
        pontos = set(pontos)
        regs = self.executar(entrada, INTERVALOS, registradores, parada=self.paradas_base | pontos,
                             pilha=pilha, limite_instrucoes=limite)
        while regs['EIP'] != RETORNO:
            eip = regs['EIP']
            if eip in pontos:
                if eip == RETORNO_DECODIFICADOR:
                    self.observacoes.append(('decoder_return', regs['EAX']))
                regs = self.retomar(eip, INTERVALOS, parada=self.paradas_base | (pontos - {eip}),
                                    limite_instrucoes=limite)
                continue
            retorno, regs = self._vincular(regs)
            regs = self.retomar(retorno, INTERVALOS, parada=self.paradas_base | pontos,
                                limite_instrucoes=limite)
        return regs

    def _vincular(self, regs):
        eip, esp = regs['EIP'], regs['ESP']
        retorno = self.u32(esp)
        if eip in (GETCWD, FREE):
            if eip == GETCWD:
                valor = self._getcwd(regs['EAX'], regs['EDX'])
            else:
                valor = self.sistema.free(regs['EAX'])
            self.cpu.reg_write(x86.UC_X86_REG_EAX, valor)
            self.cpu.reg_write(x86.UC_X86_REG_ESP, esp + 4)
            return retorno, regs
        nome = next((n for n, a in list(PARADA_IMPORTACAO.items()) + list(PARADA_COM.items()) if a == eip), None)
        if nome is None or nome == 'COM_nao_suportado':
            raise ParadaFixture(f'Unsupported binding reached at 0x{eip:08x}')
        args = struct.unpack(f'<{ARGUMENTOS[nome]}I', self.ler(esp + 4, 4 * ARGUMENTOS[nome]))
        valor = getattr(self, '_vinculo_' + nome.lstrip('_'))(*args)
        self.cpu.reg_write(x86.UC_X86_REG_EAX, valor & 0xffffffff)
        self.cpu.reg_write(x86.UC_X86_REG_ESP, esp + 4 + 4 * ARGUMENTOS[nome])
        return retorno, regs

    # -- bindings ---------------------------------------------------------
    def _getcwd(self, buffer, tamanho):
        ponteiro = self.sistema.getcwd(buffer, tamanho)
        self.escrever(ponteiro, self.alocador.blocos[ponteiro])
        return ponteiro

    def _vinculo_GlobalAlloc(self, flags, tamanho):
        ponteiro = self.alocador.alocar(flags, tamanho)
        if ponteiro:
            self.escrever(ponteiro, self.alocador.blocos[ponteiro])
        return ponteiro

    def _vinculo_GlobalFree(self, ponteiro):
        return self.alocador.liberar(ponteiro)

    def _vinculo_lopen(self, caminho, modo):
        return self.arquivos.abrir(self.cadeia(caminho), modo)

    def _vinculo_hread(self, handle, buffer, quantidade):
        dados = self.arquivos.ler(handle, quantidade)
        self.escrever(buffer, dados)
        return len(dados)

    def _vinculo_llseek(self, handle, deslocamento, origem):
        return self.arquivos.posicionar(handle, struct.unpack('<i', struct.pack('<I', deslocamento))[0], origem)

    def _vinculo_lclose(self, handle):
        return self.arquivos.fechar(handle)

    def _vinculo_MessageBoxA(self, janela, texto, titulo, tipo):
        return self.sistema.mensagem(janela, self.cadeia(texto), self.cadeia(titulo), tipo)

    def _vinculo_CreateSoundBuffer(self, este, descricao, saida, externo):
        if este != OBJETO_DS or externo:
            raise ParadaFixture('CreateSoundBuffer outside the fixture')
        desc = self.ler(descricao, 20)
        formato = self.ler(struct.unpack_from('<I', desc, 16)[0], 16)
        objeto = self.directsound.criar(desc[:16] + b'\0\0\0\0', formato)
        tamanho = len(self.directsound.buffers[objeto])
        if tamanho > DS_TAMANHO:
            raise ParadaFixture('Sound buffer larger than the fixture region')
        endereco = DS_OBJETOS + 4 * objeto
        self.escrever(endereco, struct.pack('<I', VTABELA_DSB))
        self.objetos_dsb[endereco] = objeto
        self.objeto_mapeado = objeto
        self.escrever(DS_BASE, self.directsound.buffers[objeto])
        self.escrever(saida, struct.pack('<I', endereco))
        return 0

    def _objeto(self, este):
        objeto = self.objetos_dsb.get(este)
        if objeto is None or objeto != self.objeto_mapeado:
            raise ParadaFixture('Sound buffer object not mapped by the fixture')
        return objeto

    def _vinculo_Lock(self, este, deslocamento, quantidade, ponteiro1, bytes1, ponteiro2, bytes2, flags):
        objeto = self._objeto(este)
        inicio = self.directsound.travar(objeto, deslocamento, quantidade, flags)
        self.escrever(ponteiro1, struct.pack('<I', DS_BASE + inicio))
        self.escrever(bytes1, struct.pack('<I', quantidade))
        if ponteiro2 or bytes2:
            raise ParadaFixture('Wrapped lock regions are outside the fixture')
        return 0

    def _vinculo_Unlock(self, este, ponteiro1, bytes1, ponteiro2, bytes2):
        objeto = self._objeto(este)
        tamanho = len(self.directsound.buffers[objeto])
        self.directsound.buffers[objeto][:] = self.ler(DS_BASE, tamanho)
        return self.directsound.destravar(objeto, ponteiro1 - DS_BASE, bytes1, ponteiro2, bytes2)

    def _vinculo_Release(self, este):
        raise ParadaFixture('IDirectSoundBuffer::Release is outside stage 1')

    def conteudo_buffer(self, objeto):
        return self.directsound.conteudos[objeto]
