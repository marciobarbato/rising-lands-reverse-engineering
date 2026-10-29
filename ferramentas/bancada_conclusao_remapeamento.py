"""Whole original Chemin_Remap with explicit finite fixed-memory fixtures only."""
from collections import Counter
import hashlib
import struct

from bancada_classificacao_remapeamento import BancadaClassificacaoRemapeamento, CLASSES
from emulador import RETORNO, PILHA, UNIDADES, unicorn, x86
from vinculos_declarados import ParadaVinculoDeclarado

PILHA_COMPONENTE, TAMANHO_PILHA_COMPONENTE = 0x1920000, 0x100000
REGISTRADORES_CHAMADOR = dict(EAX=0xa5a5a5a5, EBX=0x12345678, ECX=0x23456789,
                             EDX=0x3456789a, ESI=0x456789ab, EDI=0x56789abc, EBP=0x6789abcd)


class BancadaConclusaoRemapeamento(BancadaClassificacaoRemapeamento):
    pontos_retomada = BancadaClassificacaoRemapeamento.pontos_retomada + (0x42ef8b, 0x42efdf, 0x42f141)

    def __init__(self):
        super().__init__()
        self.cpu.mem_map(PILHA_COMPONENTE, TAMANHO_PILHA_COMPONENTE)
        for iat, nome, metodo in ((0x5231cc, 'GlobalHandle', self._handle),
                                  (0x5231d8, 'GlobalUnlock', self._desfixar),
                                  (0x5231c8, 'GlobalFree', self._liberar)):
            self.declarar_importacao(iat, nome, 1, metodo)
        self.origens_conclusao = Counter()
        self.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, self._observar_escrita_conclusao)

    def carregar_conclusao(self, mundo, caso):
        self.carregar_classificacao(mundo)
        self.caso, self.recursos, self.alocacoes_componentes = caso, {}, 0
        self.cpu.mem_write(PILHA_COMPONENTE, b'\xa7'*TAMANHO_PILHA_COMPONENTE)
        self.tracos_escritas = {n: hashlib.sha256() for n in ('stack', 'regions', 'attributes')}
        self.contagens_escritas = Counter()
        self.maior_offset_pilha = 0
        self.rastrear_conclusao = False

    def _alocar(self, chamada):
        flags, tamanho = chamada.argumentos
        if flags != 0 or tamanho not in (65536, TAMANHO_PILHA_COMPONENTE):
            raise ParadaVinculoDeclarado('Only explicitly sized GMEM_FIXED fixture allocations are available')
        ponteiro = CLASSES if tamanho == 65536 else PILHA_COMPONENTE
        if ponteiro in self.recursos and self.recursos[ponteiro]['active']:
            raise ParadaVinculoDeclarado('Finite fixture allocation is still live')
        if tamanho == TAMANHO_PILHA_COMPONENTE:
            if self.alocacoes_componentes >= 1024:
                raise ParadaVinculoDeclarado('Explicit 1024-component fixture allocation budget exhausted')
            self.alocacoes_componentes += 1
        # The declared fixed-memory fixture makes handle==pointer explicitly.
        # It does not supply a movable-memory implementation or allocation default.
        self.recursos[ponteiro] = dict(size=tamanho, active=True, locked=False,
                                      generation=self.alocacoes_componentes if ponteiro != CLASSES else 0)
        return ponteiro

    def _recurso(self, ponteiro):
        if ponteiro not in self.recursos or not self.recursos[ponteiro]['active']:
            raise ParadaVinculoDeclarado('Unknown or freed fixed-memory fixture handle/pointer')
        return self.recursos[ponteiro]

    def _fixar(self, chamada):
        ponteiro, = chamada.argumentos
        recurso = self._recurso(ponteiro)
        if ponteiro == PILHA_COMPONENTE:
            if self.caso == 'component_lock_unavailable':
                raise ParadaVinculoDeclarado('Component lock fixture deliberately unavailable; allocation retained')
            if self.caso == 'component_lock_null':
                return 0  # Observe the original unchecked NULL write; no synthetic clean return.
        if recurso['locked']:
            raise ParadaVinculoDeclarado('Repeated lock is outside this explicit fixture')
        recurso['locked'] = True
        return ponteiro

    def _handle(self, chamada):
        ponteiro, = chamada.argumentos
        self._recurso(ponteiro)
        return ponteiro

    def _desfixar(self, chamada):
        ponteiro, = chamada.argumentos
        recurso = self._recurso(ponteiro)
        if ponteiro == PILHA_COMPONENTE and self.caso == 'cleanup_unavailable':
            raise ParadaVinculoDeclarado('Component unlock fixture deliberately unavailable; prior labels retained')
        if not recurso['locked']:
            raise ParadaVinculoDeclarado('Fixture allocation has no retained lock')
        recurso['locked'] = False
        return 0  # Explicit fixture result: no lock remains; caller ignores this result.

    def _liberar(self, chamada):
        ponteiro, = chamada.argumentos
        recurso = self._recurso(ponteiro)
        if recurso['locked']:
            raise ParadaVinculoDeclarado('Freeing a retained fixture lock is unsupported')
        recurso['active'] = False
        return 0

    def _observar_escrita_conclusao(self, cpu, acesso, endereco, tamanho, valor, _):
        if not getattr(self, 'rastrear_conclusao', False):
            return
        for nome, inicio, tamanho_bloco in (('stack', PILHA_COMPONENTE, TAMANHO_PILHA_COMPONENTE),
                                            ('regions', self.grades['regioes'], 131072),
                                            ('attributes', self.grades['atributos'], 65536)):
            if inicio <= endereco < inicio+tamanho_bloco:
                # Compare the game's logical stores, excluding the already
                # validated CRT memset implementation of the prelude clear.
                if nome == 'regions' and cpu.reg_read(x86.UC_X86_REG_EIP) not in (0x42f01e, 0x42f175):
                    return
                offset = endereco-inicio
                self.tracos_escritas[nome].update(struct.pack('<IIQ', offset, tamanho,
                                                             valor & ((1 << (tamanho*8))-1)))
                self.contagens_escritas[nome] += 1
                if nome == 'stack':
                    self.maior_offset_pilha = max(self.maior_offset_pilha, offset+tamanho)
                return

    def imagem_inteira(self):
        # Include the complete original DGROUP+.bss and every mapped world/arena
        # allocation with tails. Native stack, instructions and trap pages are separate.
        blocos = {'0x494000': bytes(self.cpu.mem_read(0x494000, 0x523000-0x494000))}
        for inicio, fim, _ in self.cpu.mem_regions():
            if UNIDADES <= inicio < PILHA:
                blocos[hex(inicio)] = bytes(self.cpu.mem_read(inicio, fim-inicio+1))
        return blocos

    def concluir_original(self):
        self.origens_conclusao['0x42ee1c'] += 1
        self.rastrear_conclusao = True
        try:
            return self.executar(0x42ee1c, self.intervalos, REGISTRADORES_CHAMADOR, parada=RETORNO,
                                 limite_instrucoes=1000000, limite_vinculos=8192)
        finally:
            self.rastrear_conclusao = False

    def estado_conclusao(self):
        return dict(resources={hex(p): r.copy() for p, r in self.recursos.items()},
                    component_allocations=self.alocacoes_componentes,
                    stack_high_water_bytes=self.maior_offset_pilha,
                    write_trace={n: dict(count=self.contagens_escritas[n], sha256=h.hexdigest())
                                 for n, h in self.tracos_escritas.items()},
                    bindings=self.vinculos_declarados.eventos[:],
                    registers={n: self.cpu.reg_read(getattr(x86, 'UC_X86_REG_'+n))
                               for n in ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP', 'EIP', 'EFLAGS')},
                    native_stack_sha256=hashlib.sha256(bytes(self.cpu.mem_read(PILHA, 65536))).hexdigest(),
                    stopped_eip=hex(self.cpu.reg_read(x86.UC_X86_REG_EIP)))
