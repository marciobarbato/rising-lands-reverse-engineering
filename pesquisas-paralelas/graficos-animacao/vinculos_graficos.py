"""Declared external bindings for graphics oracle runs; pure Python fixtures.

Only Windows imports and statically linked C-runtime stream calls are bound.
Every call records its exact arguments and the returned fixture value. A
request outside what the fixture can honor raises ParadaVinculo: a reported
stop, never a pass. Graphics keeps these locally until core publishes its
generic declared-binding facility in ferramentas/emulador.py, then migrates.
"""
import hashlib
import json

# GlobalAlloc(GMEM_FIXED) contents are undefined; the fixture declares this
# fill so code that reads before writing is visible instead of reading zero.
PADRAO_NAO_INICIALIZADO = 0xA5


class ParadaVinculo(RuntimeError):
    def __init__(self, nome, argumentos, motivo):
        self.nome, self.argumentos, self.motivo = nome, tuple(argumentos), motivo
        super().__init__(f'Declared binding stop at {nome}{self.argumentos}: {motivo}')


class RegistroVinculos:
    """Ordered log of (binding, exact u32/str arguments, returned value)."""
    def __init__(self):
        self.chamadas = []

    def registrar(self, nome, argumentos, retorno):
        self.chamadas.append((nome, tuple(argumentos), retorno))
        return retorno

    def marca(self):
        return len(self.chamadas)

    def desde(self, marca, fim=None):
        return [list(c) for c in self.chamadas[marca:fim]]

    def resumo(self, marca=0, fim=None):
        trecho = self.chamadas[marca:fim]; contagem = {}
        digest = hashlib.sha256()
        for nome, argumentos, retorno in trecho:
            contagem[nome] = contagem.get(nome, 0)+1
            digest.update((json.dumps([nome, list(argumentos), retorno], separators=(',', ':'))+'\n').encode('ascii'))
        return dict(chamadas=len(trecho), por_vinculo=dict(sorted(contagem.items())), sha256=digest.hexdigest())


def _u32(valor, nome):
    if type(valor) is not int or not 0 <= valor <= 0xFFFFFFFF:
        raise ValueError(nome+' must be u32')


class ArenaGlobalFixa:
    """KERNEL32 Global* over a deterministic GMEM_FIXED arena.

    Honored: GlobalAlloc(0, n>0) inside the arena; GlobalLock/GlobalHandle/
    GlobalUnlock/GlobalFree of a live fixed block. Fixed memory has handle ==
    pointer and lock count zero, so GlobalUnlock returns 0 and GlobalFree
    returns NULL. Movable flags, failure, exhaustion and stale handles stop.
    """
    def __init__(self, *, inicio_u32, tamanho_u32, registro, alinhamento=16, preencher=None):
        _u32(inicio_u32, 'inicio_u32'); _u32(tamanho_u32, 'tamanho_u32')
        if not isinstance(registro, RegistroVinculos):
            raise ValueError('Expected explicit RegistroVinculos')
        if alinhamento not in (8, 16) or inicio_u32 % alinhamento:
            raise ValueError('Arena start must honor 8- or 16-byte alignment')
        self.inicio, self.fim, self.alinhamento = inicio_u32, inicio_u32+tamanho_u32, alinhamento
        self.proximo, self.vivos, self.registro, self.preencher = inicio_u32, {}, registro, preencher

    def derivar(self, *, registro, preencher=None):
        """Same arena position/live blocks for an independent model-side run."""
        copia = ArenaGlobalFixa(inicio_u32=self.inicio, tamanho_u32=self.fim-self.inicio, registro=registro,
            alinhamento=self.alinhamento, preencher=preencher)
        copia.proximo, copia.vivos = self.proximo, dict(self.vivos)
        return copia

    def _vivo(self, nome, valor):
        _u32(valor, nome)
        if valor not in self.vivos:
            raise ParadaVinculo(nome, (valor,), 'not a live GMEM_FIXED block of this arena')

    def global_alloc(self, flags_u32, bytes_u32):
        _u32(flags_u32, 'flags_u32'); _u32(bytes_u32, 'bytes_u32')
        if flags_u32 != 0:
            raise ParadaVinculo('GlobalAlloc', (flags_u32, bytes_u32), 'only GMEM_FIXED (flags 0) is honored')
        if bytes_u32 == 0:
            raise ParadaVinculo('GlobalAlloc', (flags_u32, bytes_u32), 'zero-byte allocation semantics not declared')
        endereco = self.proximo
        seguinte = (endereco+bytes_u32+self.alinhamento-1)//self.alinhamento*self.alinhamento
        if seguinte > self.fim:
            raise ParadaVinculo('GlobalAlloc', (flags_u32, bytes_u32), 'arena exhausted; failure semantics not declared')
        self.proximo = seguinte; self.vivos[endereco] = bytes_u32
        if self.preencher is not None:
            self.preencher(endereco, bytes_u32)
        return self.registro.registrar('GlobalAlloc', (flags_u32, bytes_u32), endereco)

    def global_lock(self, handle_u32):
        self._vivo('GlobalLock', handle_u32)
        return self.registro.registrar('GlobalLock', (handle_u32,), handle_u32)

    def global_handle(self, ponteiro_u32):
        self._vivo('GlobalHandle', ponteiro_u32)
        return self.registro.registrar('GlobalHandle', (ponteiro_u32,), ponteiro_u32)

    def global_unlock(self, handle_u32):
        self._vivo('GlobalUnlock', handle_u32)
        return self.registro.registrar('GlobalUnlock', (handle_u32,), 0)

    def global_free(self, handle_u32):
        self._vivo('GlobalFree', handle_u32)
        del self.vivos[handle_u32]
        return self.registro.registrar('GlobalFree', (handle_u32,), 0)


class ArquivosDeclarados:
    """C-runtime fopen/fread/fclose over exact requested names and file bytes.

    Only binary reads ("rb") of declared names are honored. fread must be able
    to copy the full size*count; short reads/EOF semantics stop. Handles are
    opaque nonzero values in an unmapped range, so a dereference would fault.
    """
    def __init__(self, arquivos, *, registro, primeiro_handle=0x0F000000):
        if not isinstance(registro, RegistroVinculos):
            raise ValueError('Expected explicit RegistroVinculos')
        self.arquivos = {nome: bytes(dados) for nome, dados in arquivos.items()}
        self.registro, self.proximo, self.abertos = registro, primeiro_handle, {}

    def fopen(self, nome, modo):
        if modo != 'rb':
            raise ParadaVinculo('fopen', (nome, modo), 'only binary read mode is honored')
        if nome not in self.arquivos:
            raise ParadaVinculo('fopen', (nome, modo), 'name is not a declared fixture file')
        handle = self.proximo; self.proximo += 0x100
        self.abertos[handle] = [nome, 0]
        return self.registro.registrar('fopen', (nome, modo), handle)

    def fread(self, buffer_u32, tamanho_u32, quantidade_u32, handle_u32):
        argumentos = (buffer_u32, tamanho_u32, quantidade_u32, handle_u32)
        if handle_u32 not in self.abertos:
            raise ParadaVinculo('fread', argumentos, 'handle is not open')
        nome, posicao = self.abertos[handle_u32]; total = tamanho_u32*quantidade_u32
        dados = self.arquivos[nome][posicao:posicao+total]
        if quantidade_u32 == 0 or tamanho_u32 == 0 or len(dados) != total:
            raise ParadaVinculo('fread', argumentos, 'short/empty read semantics not honored')
        self.abertos[handle_u32][1] = posicao+total
        self.registro.registrar('fread', argumentos+(nome, posicao), quantidade_u32)
        return dados, quantidade_u32

    def fclose(self, handle_u32):
        if handle_u32 not in self.abertos:
            raise ParadaVinculo('fclose', (handle_u32,), 'handle is not open')
        del self.abertos[handle_u32]
        return self.registro.registrar('fclose', (handle_u32,), 0)
