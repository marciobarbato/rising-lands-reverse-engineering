"""Declared Windows/DirectSound binding fixtures for audio captures and comparisons.

These are test fixtures, not recovered game behavior. Each call records its
exact arguments and the fixture result. The native bench binds the original
import slots and COM methods to these objects; the Python reconstruction calls
the same objects through its provider parameters. Identical logs therefore
mean identical call order, arguments and results.

A request the fixture cannot honor raises ``ParadaFixture``: an unknown file
handle, a lock outside its buffer, or a user-visible message box.
"""
import hashlib

HFILE_ERROR = 0xffffffff
GMEM_ZEROINIT = 0x40
VENENO = 0xcd


class ParadaFixture(RuntimeError):
    """The declared fixture cannot honor the requested Windows semantics."""


class ArquivosFixos:
    """``_lopen``/``_hread``/``_llseek``/``_lclose`` over exact-path byte images.

    Paths match byte for byte; any other path returns HFILE_ERROR, as a missing
    file does. Handles are numbered from ``primeiro``. ``_hread`` returns fewer
    bytes at end of file, as Windows does for a file.
    """

    def __init__(self, arquivos, registro, primeiro=5):
        self.arquivos = {bytes(caminho): bytes(dados) for caminho, dados in arquivos.items()}
        self.registro = registro
        self.proximo = primeiro
        self.abertos = {}

    def abrir(self, caminho, modo):
        caminho = bytes(caminho)
        if caminho in self.arquivos:
            handle = self.proximo
            self.proximo += 1
            self.abertos[handle] = [caminho, 0]
        else:
            handle = HFILE_ERROR
        self.registro.append(('_lopen', caminho.decode('latin-1'), modo & 0xffffffff, handle))
        return handle

    def _aberto(self, handle):
        if handle not in self.abertos:
            raise ParadaFixture(f'File handle {handle:#x} is not open in the fixture')
        return self.abertos[handle]

    def ler(self, handle, quantidade):
        estado = self._aberto(handle)
        dados = self.arquivos[estado[0]][estado[1]:estado[1] + quantidade]
        estado[1] += len(dados)
        self.registro.append(('_hread', handle, quantidade & 0xffffffff, len(dados)))
        return dados

    def posicionar(self, handle, deslocamento, origem):
        estado = self._aberto(handle)
        base = {0: 0, 1: estado[1], 2: len(self.arquivos[estado[0]])}.get(origem)
        if base is None or base + deslocamento < 0:
            raise ParadaFixture(f'Seek origin/offset not honored: {origem}, {deslocamento}')
        estado[1] = base + deslocamento
        self.registro.append(('_llseek', handle, deslocamento & 0xffffffff, origem & 0xffffffff, estado[1]))
        return estado[1]

    def fechar(self, handle):
        self._aberto(handle)
        del self.abertos[handle]
        self.registro.append(('_lclose', handle, 0))
        return 0


class AlocadorFixo:
    """``GlobalAlloc``/``GlobalFree`` as a deterministic 16-byte-aligned arena.

    Without GMEM_ZEROINIT new memory is filled with ``VENENO`` so that any
    dependence on uninitialized content is visible in comparisons.
    ``falhar_em`` lists allocation ordinals (0-based) that return NULL.
    """

    def __init__(self, base, tamanho, registro, falhar_em=()):
        self.base, self.limite, self.proximo = base, base + tamanho, base
        self.registro, self.falhar_em, self.chamadas = registro, set(falhar_em), 0
        self.blocos = {}

    def alocar(self, flags, tamanho):
        ordinal, self.chamadas = self.chamadas, self.chamadas + 1
        if ordinal in self.falhar_em:
            ponteiro = 0
        else:
            if self.proximo + tamanho > self.limite:
                raise ParadaFixture(f'Fixture arena cannot hold {tamanho} bytes')
            ponteiro = self.proximo
            self.proximo = (self.proximo + tamanho + 15) & ~15
            self.blocos[ponteiro] = bytearray(b'\0' * tamanho if flags & GMEM_ZEROINIT else bytes([VENENO]) * tamanho)
        self.registro.append(('GlobalAlloc', flags & 0xffffffff, tamanho & 0xffffffff, ponteiro))
        return ponteiro

    def liberar(self, ponteiro):
        if ponteiro not in self.blocos:
            raise ParadaFixture(f'GlobalFree of unknown block {ponteiro:#x}')
        del self.blocos[ponteiro]
        self.registro.append(('GlobalFree', ponteiro, 0))
        return 0


class SistemaFixo:
    """All declared bindings of one capture, sharing one ordered log.

    ``getcwd``/``free`` stand for the Watcom CRT entries 0x48c481/0x48d7f4,
    whose Windows calls are outside the fixture: getcwd returns a fixture
    arena block holding ``diretorio_corrente``. ``mensagem`` is MessageBoxA,
    always a declared stop.
    """

    def __init__(self, arquivos, *, diretorio_corrente, arena, arena_tamanho, falhar_alocacao=()):
        self.registro = []
        self.arquivos = ArquivosFixos(arquivos, self.registro)
        self.alocador = AlocadorFixo(arena, arena_tamanho, self.registro, falhar_alocacao)
        self.directsound = DirectSoundFixo(self.registro)
        self.diretorio_corrente = bytes(diretorio_corrente)

    def getcwd(self, buffer, tamanho):
        if buffer != 0:
            raise ParadaFixture('getcwd with a caller buffer is outside the fixture')
        if len(self.diretorio_corrente) + 1 > tamanho:
            raise ParadaFixture('Fixture directory longer than the getcwd buffer')
        ponteiro = self.alocador.alocar(0, tamanho)
        self.registro[-1] = ('getcwd', buffer, tamanho, ponteiro)
        self.alocador.blocos[ponteiro][:len(self.diretorio_corrente) + 1] = self.diretorio_corrente + b'\0'
        return ponteiro

    def free(self, ponteiro):
        self.registro.append(('free', ponteiro))
        return ponteiro

    def mensagem(self, janela, texto, titulo, tipo):
        self.registro.append(('MessageBoxA', janela, bytes(texto).decode('latin-1'),
                              bytes(titulo).decode('latin-1'), tipo))
        raise ParadaFixture('MessageBoxA is a declared stop')


class DirectSoundFixo:
    """IDirectSound::CreateSoundBuffer and IDirectSoundBuffer Lock/Unlock.

    Every created buffer is new memory filled with ``VENENO`` (DirectSound
    leaves new buffer content undefined). Buffers are numbered objects; the
    native bench maps each to emulated memory. Unlock snapshots the content.
    """

    def __init__(self, registro, primeiro=1):
        self.registro, self.proximo = registro, primeiro
        self.buffers = {}
        self.conteudos = {}

    def criar(self, descricao, formato):
        descricao, formato = bytes(descricao), bytes(formato)
        tamanho = int.from_bytes(descricao[8:12], 'little')
        if len(descricao) != 20 or int.from_bytes(descricao[:4], 'little') != 20 or tamanho == 0:
            raise ParadaFixture('Sound buffer description not honored by the fixture')
        objeto = self.proximo
        self.proximo += 1
        self.buffers[objeto] = bytearray([VENENO]) * tamanho
        self.registro.append(('CreateSoundBuffer', descricao.hex(), formato.hex(), objeto, 0))
        return objeto

    def travar(self, objeto, deslocamento, quantidade, flags):
        buffer = self.buffers.get(objeto)
        if buffer is None or flags or deslocamento + quantidade > len(buffer):
            raise ParadaFixture('Sound buffer lock not honored by the fixture')
        self.registro.append(('Lock', objeto, deslocamento, quantidade, flags, 0))
        return deslocamento

    def destravar(self, objeto, deslocamento, quantidade, deslocamento2, quantidade2):
        conteudo = bytes(self.buffers[objeto])
        self.conteudos[objeto] = conteudo
        self.registro.append(('Unlock', objeto, deslocamento, quantidade, deslocamento2, quantidade2,
                              hashlib.sha256(conteudo).hexdigest()))
        return 0
