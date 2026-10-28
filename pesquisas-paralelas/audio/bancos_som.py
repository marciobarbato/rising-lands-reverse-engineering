"""Original sound-bank paths, header validation, index and data-header lookup.

Reconstructs intact routines listed in ``evidencias/som-manifesto.json``:
``PlaySnd_CreateSoundPath``, ``SoundFile``, ``PlaySnd_MakeID``,
``BanqSon_ControleValiditeHeader``/``LoadHeader``/``Open``/``LoadAllData``/
``LoadDataInMemory``, ``UseBank_FindIdInBanque``/``GetDataHeader`` and
``HndSound_LoadDataInfo``, with the ``OurAlloc``/``OurFree`` wrappers.

The caller supplies every inherited buffer and an explicit ``sistema``
provider for the Windows/CRT calls (``arquivos.abrir/ler/posicionar/fechar``,
``alocador.alocar/liberar``, ``getcwd``, ``free``, ``mensagem``). Nothing is
opened, allocated or defaulted implicitly; provider exceptions propagate after
all earlier effects, as the original has no rollback.
"""
import struct

MAGIA = 0x44434241  # b'ABCD' read as a little-endian dword
HFILE_ERROR = 0xffffffff
NOME_ARQUIVO_BYTES = 104  # 0x5221c0 up to the DirectSound pointer at 0x522228
DIRETORIO_BYTES = 256     # 0x52201c up to the physical table at 0x52211c
TEXTOS = {
    'cabecalho_alocar': b'BanqSon_LoadHeader:Allocation buffer Header',
    'cabecalho_liberar': b'BanqSon_LoadHeader:Liberation du buffer Header',
    'liberar_cabecalho': b'BanqSon_FreeHeader',
    'dados_alocar': b'BanqSon_LoadAllData: Allocation buffer data sonore',
    'dados_liberar': b'BanqSon_LoadAllData:Liberation anticip\xe9',
    'comprimido_alocar': b'LoadSoundBuffer_InitCompressedBuffer: Allocation buffer',
}
# MessageBoxA captions: 0x495530 (OurAlloc), 0x495532 (OurFree NULL), 0x49553d (failed GlobalFree).
TITULO_ALOCAR, TITULO_PONTEIRO_NULO, TITULO_LIBERAR = b'', b'Ptr NULL !', b''


class DependenciaSom(NotImplementedError):
    def __init__(self, endereco, detalhe):
        self.endereco = endereco
        super().__init__(f'Audio dependency at 0x{endereco:08x}: {detalhe}')


def _u32(valor):
    return valor & 0xffffffff


def _buffer(memoria, tamanho, nome):
    view = memoryview(memoria)
    if view.readonly or not view.c_contiguous or view.ndim != 1 or view.format != 'B' or len(view) != tamanho:
        raise ValueError(f'{nome} must be a writable contiguous {tamanho}-byte buffer')
    return view


class GlobaisSom:
    """Inherited audio globals. Every field is explicit caller state.

    ``nome_arquivo`` is the 104-byte bank file name at 0x5221c0,
    ``diretorio`` the 256-byte sound directory at 0x52201c. Counters are u32:
    variant selector 0x5221bc, allocation count 0x522230. ``janela`` is the
    window handle at 0x4e27e8 passed to MessageBoxA, ``comprimido`` the
    compressed-buffer pointer at 0x52222c, ``directsound`` the IDirectSound
    pointer at 0x522228 (zero means DirectSound was never initialized).
    """

    def __init__(self, *, nome_arquivo, diretorio, contador_variantes, contador_alocacoes, janela,
                 comprimido, directsound):
        self.nome_arquivo = _buffer(nome_arquivo, NOME_ARQUIVO_BYTES, 'Bank file name')
        self.diretorio = _buffer(diretorio, DIRETORIO_BYTES, 'Sound directory')
        self.contador_variantes = _u32(contador_variantes)
        self.contador_alocacoes = _u32(contador_alocacoes)
        self.janela = _u32(janela)
        self.comprimido = _u32(comprimido)
        self.directsound = _u32(directsound)


class BancoSom:
    """The original 28-byte bank record (0x521fc8 A, 0x521fe4 B, 0x522000 P).

    +0 open u32, +4 entry count u16, +6 untouched u16, +8 data-file handle,
    +0xc header pointer, +0x10 data-in-memory u32, +0x14 data pointer,
    +0x18 data size. ``cabecalho``/``dados`` hold the bytes the provider-owned
    pointers address; they are None when no buffer is attached.
    """
    CAMPOS = {'aberto': 0, 'arquivo': 8, 'ponteiro_cabecalho': 0xc, 'em_memoria': 0x10,
              'ponteiro_dados': 0x14, 'tamanho_dados': 0x18}

    def __init__(self, registro, endereco):
        self.registro = _buffer(registro, 28, 'Bank record')
        self.endereco = _u32(endereco)
        self.cabecalho = None
        self.dados = None

    def __getattr__(self, nome):
        if nome in BancoSom.CAMPOS:
            return struct.unpack_from('<I', self.registro, BancoSom.CAMPOS[nome])[0]
        raise AttributeError(nome)

    def __setattr__(self, nome, valor):
        if nome in BancoSom.CAMPOS:
            struct.pack_into('<I', self.registro, BancoSom.CAMPOS[nome], _u32(valor))
        else:
            object.__setattr__(self, nome, valor)

    @property
    def quantidade(self):
        return struct.unpack_from('<H', self.registro, 4)[0]

    @quantidade.setter
    def quantidade(self, valor):
        struct.pack_into('<H', self.registro, 4, valor & 0xffff)


# -- allocation wrappers -----------------------------------------------------
def alocar(sistema, globais, tamanho, texto):
    """OurAlloc 0x48c204: GlobalAlloc(0, n); NULL shows a message box and still counts."""
    ponteiro = sistema.alocador.alocar(0, _u32(tamanho))
    if ponteiro == 0:
        sistema.mensagem(globais.janela, texto, TITULO_ALOCAR, 0)
    globais.contador_alocacoes = _u32(globais.contador_alocacoes + 1)
    return ponteiro


def liberar(sistema, globais, ponteiro, texto):
    """OurFree 0x48c27f on a pointer variable; returns the value stored back (0)."""
    if ponteiro == 0:
        sistema.mensagem(globais.janela, texto, TITULO_PONTEIRO_NULO, 0)
        return 0
    if sistema.alocador.liberar(ponteiro):
        sistema.mensagem(globais.janela, texto, TITULO_LIBERAR, 0)
    globais.contador_alocacoes = _u32(globais.contador_alocacoes - 1)
    return 0


# -- identity and paths ------------------------------------------------------
def criar_id_som(a, b, c):
    """PlaySnd_MakeID 0x48a894: (a << 16) | (b << 8) | c on full u32 inputs."""
    return _u32((_u32(a) << 16) | (_u32(b) << 8) | _u32(c))


def _cadeia(texto, nome):
    texto = bytes(texto)
    if b'\0' in texto:
        raise ValueError(f'{nome} must not contain NUL')
    return texto


def criar_caminho_sons(sistema, globais):
    """PlaySnd_CreateSoundPath 0x48a834 (inlined in PlaySnd_InitSoundLib).

    getcwd(NULL, 1000); ``%s%s`` with "SOUND" when the directory ends in a
    backslash, else ``%s\\%s``; free. Only the formatted bytes and NUL are
    written. An empty directory reads before its buffer and is unsupported.
    """
    ponteiro = sistema.getcwd(0, 1000)
    bloco = sistema.alocador.blocos[ponteiro]
    corrente = bytes(bloco[:bloco.index(0)])
    if not corrente:
        raise DependenciaSom(0x48a84b, 'empty working directory reads before the getcwd buffer')
    texto = corrente + (b'SOUND' if corrente[-1:] == b'\\' else b'\\SOUND')
    if len(texto) + 1 > DIRETORIO_BYTES:
        raise DependenciaSom(0x48a86e, 'sound directory longer than its 256-byte global')
    globais.diretorio[:len(texto) + 1] = texto + b'\0'
    sistema.free(ponteiro)
    return texto


def arquivo_som(globais, nome):
    """SoundFile 0x48a87f: ``%s\\%s`` of the sound directory and ``nome``."""
    diretorio = bytes(globais.diretorio)
    if b'\0' not in diretorio:
        raise ValueError('Sound directory is not NUL-terminated')
    return diretorio[:diretorio.index(b'\0')] + b'\\' + _cadeia(nome, 'Sound name')


def _nome_arquivo(globais, nome, extensao):
    texto = _cadeia(nome, 'Bank name') + extensao
    if len(texto) + 1 > NOME_ARQUIVO_BYTES:
        raise DependenciaSom(0x48b3f8, 'bank file name longer than its 104-byte global')
    globais.nome_arquivo[:len(texto) + 1] = texto + b'\0'
    return texto


# -- header ------------------------------------------------------------------
def _ler_prefixo(sistema, handle):
    prefixo = sistema.arquivos.ler(handle, 16)
    if len(prefixo) != 16:
        raise DependenciaSom(0x48b45e, 'short 16-byte header read leaves stack bytes undefined')
    return struct.unpack('<IIII', prefixo)


def validar_cabecalho_banco(sistema, handle, banco):
    """BanqSon_ControleValiditeHeader 0x48b44e (no original caller).

    Reads 16 bytes; a bad magic writes 0 to the output and returns 0. A good
    magic writes the header size, stores count u16 at +4 and data size at +0x18.
    Returns ``(result, value written to the caller's output dword)``.
    """
    magia, tamanho, dados, quantidade = _ler_prefixo(sistema, handle)
    if magia != MAGIA:
        return 0, 0
    banco.quantidade = quantidade
    banco.tamanho_dados = dados
    return 1, tamanho


def carregar_cabecalho_banco(sistema, globais, nome, banco):
    """BanqSon_LoadHeader 0x48b496: returns the header pointer or 0."""
    caminho = _nome_arquivo(globais, nome, b'.HED')
    handle = sistema.arquivos.abrir(caminho, 0)
    if handle == HFILE_ERROR:
        return 0
    magia, tamanho, dados, quantidade = _ler_prefixo(sistema, handle)
    if magia != MAGIA:
        sistema.arquivos.fechar(handle)
        return 0
    banco.quantidade = quantidade
    banco.tamanho_dados = dados
    ponteiro = alocar(sistema, globais, tamanho, TEXTOS['cabecalho_alocar'])
    if ponteiro == 0:
        sistema.arquivos.fechar(handle)
        return 0
    corpo = sistema.arquivos.ler(handle, tamanho)
    if len(corpo) != tamanho:
        sistema.arquivos.fechar(handle)
        liberar(sistema, globais, ponteiro, TEXTOS['cabecalho_liberar'])
        return 0
    sistema.arquivos.fechar(handle)
    banco.cabecalho = corpo
    return ponteiro


def abrir_banco(sistema, globais, nome, banco):
    """BanqSon_Open 0x48b5a6: header, then the .SND handle kept open."""
    if banco.aberto == 1:
        return 0
    ponteiro = carregar_cabecalho_banco(sistema, globais, nome, banco)
    banco.ponteiro_cabecalho = ponteiro
    if ponteiro == 0:
        return 0
    caminho = _nome_arquivo(globais, nome, b'.SND')
    handle = sistema.arquivos.abrir(caminho, 0)
    banco.arquivo = handle
    if handle == HFILE_ERROR:
        banco.ponteiro_cabecalho = liberar(sistema, globais, ponteiro, TEXTOS['liberar_cabecalho'])
        banco.cabecalho = None
        return 0
    banco.ponteiro_dados = 0
    banco.em_memoria = 0
    banco.aberto = 1
    return 1


def _ler_dados(sistema, globais, banco):
    ponteiro = alocar(sistema, globais, banco.tamanho_dados, TEXTOS['dados_alocar'])
    if ponteiro == 0:
        return 0, None
    dados = sistema.arquivos.ler(banco.arquivo, banco.tamanho_dados)
    if len(dados) != banco.tamanho_dados:
        return liberar(sistema, globais, ponteiro, TEXTOS['dados_liberar']), None
    return ponteiro, dados


def carregar_todos_dados(sistema, globais, banco):
    """BanqSon_LoadAllData 0x48b6e7 (no original caller): returns ``(pointer, bytes)``.

    Reads from the data file's current position; the record is not changed.
    """
    return _ler_dados(sistema, globais, banco)


def carregar_dados_em_memoria(sistema, globais, banco):
    """BanqSon_LoadDataInMemory 0x48b733 (no original caller).

    A closed bank returns 0. Otherwise the in-memory flag is set even when the
    allocation or the read failed, leaving a NULL data pointer.
    """
    if banco.aberto == 0:
        return 0
    ponteiro, dados = _ler_dados(sistema, globais, banco)
    banco.ponteiro_dados = ponteiro
    banco.dados = dados
    banco.em_memoria = 1
    return 1


# -- index ---------------------------------------------------------------------
def procurar_som(identificador, banco):
    """UseBank_FindIdInBanque 0x48b390: offset of the 12-byte entry, or None."""
    identificador = _u32(identificador)
    for indice in range(banco.quantidade):
        if struct.unpack_from('<I', banco.cabecalho, 12 * indice)[0] == identificador:
            return 12 * indice
    return None


def cabecalho_dados_som(globais, entrada, banco):
    """UseBank_GetDataHeader 0x48b3b3: header offset of the selected variant.

    Increments the u32 variant counter first. With n variants and n-1 > 0
    (signed), selects ``(n-1) & counter``; a 3-variant entry therefore never
    selects variant 1. Otherwise returns the first data header.
    """
    globais.contador_variantes = _u32(globais.contador_variantes + 1)
    variantes, deslocamento = struct.unpack_from('<HI', banco.cabecalho, entrada + 6)
    if variantes - 1 > 0:
        return _u32(deslocamento + (((variantes - 1) & globais.contador_variantes) << 4))
    return deslocamento


def carregar_info_som(globais, registro, identificador, banco, ecx, argumento):
    """HndSound_LoadDataInfo 0x48a0f4 over an inherited handle record (>= 32 bytes).

    Store order: +0x18 entry pointer (0 when absent, then return 0); +0 ID;
    +4 bank address; variant selection; +0x1c data-header pointer; +0xc ECX;
    +0x10 = 0x100 when the entry word +4 is 0x100, else the stack argument;
    +0x14 = 0. Pointers are the bank's header pointer plus offsets.
    """
    view = memoryview(registro)
    if view.readonly or not view.c_contiguous or view.format != 'B' or len(view) < 32:
        raise ValueError('Handle record must be a writable contiguous buffer of at least 32 bytes')
    entrada = procurar_som(identificador, banco)
    ponteiro = 0 if entrada is None else _u32(banco.ponteiro_cabecalho + entrada)
    struct.pack_into('<I', view, 0x18, ponteiro)
    if entrada is None:
        return 0
    struct.pack_into('<II', view, 0, _u32(identificador), banco.endereco)
    dados = cabecalho_dados_som(globais, entrada, banco)
    struct.pack_into('<I', view, 0x1c, _u32(banco.ponteiro_cabecalho + dados))
    struct.pack_into('<I', view, 0xc, _u32(ecx))
    palavra = struct.unpack_from('<H', banco.cabecalho, entrada + 4)[0]
    struct.pack_into('<II', view, 0x10, 0x100 if palavra == 0x100 else _u32(argumento), 0)
    return 1


def entradas_banco(banco):
    """Read-only view of the index: (ID, word +4, variant count, data offset) per entry."""
    return [struct.unpack_from('<IHHI', banco.cabecalho, 12 * i) for i in range(banco.quantidade)]
