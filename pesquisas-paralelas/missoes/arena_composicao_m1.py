"""Deterministic Python GlobalAlloc arena continuing the frozen MissionLoad entry state.

It reproduces the oracle's declared policy (``fronteiras_carga_missao.ArenaAlocacoes``)
from the entry snapshot: GMEM_FIXED with handle == pointer, page-aligned bump
from the recorded next-free address, never reused, non-ZEROINIT bytes equal to
the declared fill and ZEROINIT bytes zero. Each live allocation is one new
block of the shared :class:`mapa_memoria_m1.MapaMemoriaM1`; a freed one leaves
the map and keeps its record (bytes SHA-256 at free) for comparison.

The five callbacks match ``conclusao_remapeamento.remapear_mundo``:
``alocar(flags,size)->handle``, ``fixar(handle)->live buffer``,
``obter_handle(buffer)->handle`` (by buffer identity: the locked pointer),
``desfixar(handle)->0`` and ``liberar(handle)->0``. Every request is logged in
order for the binding-sequence comparison; no recorded native result is used.
"""
from mapa_memoria_m1 import sha256

GMEM_ZEROINIT = 0x40
PAGINA = 0x1000


class ErroArenaM1(RuntimeError):
    pass


class ArenaComposicaoM1:
    def __init__(self, mapa, arena, alocacoes, registro):
        """``arena``/``alocacoes``: the entry snapshot ``arena`` dict and ``allocations`` list."""
        self.mapa = mapa
        self.base, self.limite = int(arena['base'], 16), int(arena['limit'], 16)
        self.proximo = int(arena['next_free'], 16)
        self.preenchimento = arena['fill']
        self.maximo = arena['count_budget']
        self.registros = [dict(a) for a in alocacoes]
        if len(self.registros) != arena['allocations']:
            raise ErroArenaM1('Entry arena count does not match its allocation records')
        ultimo = max(int(a['pointer'], 16) + a['size'] for a in self.registros)
        if (ultimo + PAGINA - 1) & ~(PAGINA - 1) > self.proximo:
            raise ErroArenaM1('Recorded next-free address precedes an existing allocation')
        self.vivos = {}            # handle -> (record, buffer, block name)
        self.por_buffer = {}       # id(buffer) -> handle
        self.registro = registro   # shared ordered binding-request log

    def _evento(self, nome, argumentos, resultado):
        self.registro.append(dict(name=nome, args=tuple(argumentos), result=resultado))

    def alocar(self, flags, tamanho):
        flags &= 0xffffffff
        if flags & ~GMEM_ZEROINIT or not 0 < tamanho <= 0x2000000:
            raise ErroArenaM1(f'GlobalAlloc flags 0x{flags:x}/size {tamanho} outside the declared policy')
        if len(self.registros) >= self.maximo:
            raise ErroArenaM1('Declared allocation budget exhausted')
        ponteiro = self.proximo
        if ponteiro + tamanho > self.limite:
            raise ErroArenaM1('Declared arena exhausted')
        self.proximo = (ponteiro + tamanho + PAGINA - 1) & ~(PAGINA - 1)
        inicial = 0 if flags & GMEM_ZEROINIT else self.preenchimento
        buffer = bytearray([inicial]) * tamanho
        indice = len(self.registros)
        nome = f'alloc{indice:05d}'
        registro = dict(active=True, events='alloc', flags=flags, index=indice, initial_byte=inicial,
                        locks=0, pointer=hex(ponteiro), size=tamanho)
        self.registros.append(registro)
        self.mapa.adicionar_bloco(nome, ponteiro, buffer, f'arena:{nome}')
        self.vivos[ponteiro] = (registro, buffer, nome)
        self.por_buffer[id(buffer)] = ponteiro
        self._evento('KERNEL32.GlobalAlloc', (flags, tamanho), ponteiro)
        return ponteiro

    def _vivo(self, handle, operacao):
        handle &= 0xffffffff
        if handle not in self.vivos:
            raise ErroArenaM1(f'{operacao} on 0x{handle:08x}, which is not a live arena handle')
        return handle, self.vivos[handle]

    def fixar(self, handle):
        handle, (registro, buffer, _) = self._vivo(handle, 'GlobalLock')
        registro['locks'] += 1
        registro['events'] += ' lock'
        self._evento('KERNEL32.GlobalLock', (handle,), handle)
        return buffer

    def obter_handle(self, buffer):
        handle = self.por_buffer.get(id(buffer))
        if handle is None or self.vivos.get(handle, (None, None))[1] is not buffer:
            raise ErroArenaM1('GlobalHandle received a buffer that is not a live locked arena pointer')
        registro = self.vivos[handle][0]
        registro['events'] += ' handle'
        self._evento('KERNEL32.GlobalHandle', (handle,), handle)
        return handle

    def desfixar(self, handle):
        handle, (registro, _, _) = self._vivo(handle, 'GlobalUnlock')
        if not registro['locks']:
            raise ErroArenaM1('GlobalUnlock without a lock')
        registro['locks'] -= 1
        registro['events'] += ' unlock'
        self._evento('KERNEL32.GlobalUnlock', (handle,), 0)
        return 0

    def liberar(self, handle):
        handle, (registro, buffer, nome) = self._vivo(handle, 'GlobalFree')
        if registro['locks']:
            raise ErroArenaM1('GlobalFree while locked')
        dados = self.mapa.remover_bloco(nome)
        registro.update(active=False, freed_sha256=sha256(dados))
        registro['events'] += ' free'
        del self.vivos[handle]
        del self.por_buffer[id(buffer)]
        self._evento('KERNEL32.GlobalFree', (handle,), 0)
        return 0
