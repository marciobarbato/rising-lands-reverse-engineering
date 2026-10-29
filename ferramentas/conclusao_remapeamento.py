"""Chemin_Remap component stacks, ordered resource lifecycle and final AL result."""
from dataclasses import dataclass

from classificacao_remapeamento import ClassificacaoRemapeamento, _vista, _sem_sobreposicao


@dataclass
class EstadoConclusaoRemapeamento:
    classificacao: ClassificacaoRemapeamento
    fase: str = 'scan'
    celula: int = 0
    componentes: int = 0
    semente: int = 0
    memoria_pilha: object = None
    handle_pilha: int = 0
    handle_operacao: int = 0
    topo: int = 0
    resultado: object = None


class DependenciaConclusaoRemapeamento(NotImplementedError):
    def __init__(self, estado, checkpoint, importacao, argumentos):
        self.estado, self.checkpoint, self.importacao, self.argumentos = estado, checkpoint, importacao, argumentos
        super().__init__(f'Missing remap resource provider at 0x{checkpoint:x}, IAT 0x{importacao:x}; prior effects retained')


class FalhaMemoriaConclusaoRemapeamento(RuntimeError):
    def __init__(self, estado, checkpoint, endereco):
        self.estado, self.checkpoint, self.endereco = estado, checkpoint, endereco
        super().__init__(f'Original remap would write unavailable memory at 0x{checkpoint:x}, address 0x{endereco:x}')


def remapear_mundo(mundo, *, alocar=None, fixar=None, obter_handle=None, desfixar=None, liberar=None):
    """Whole natural Chemin_Remap; explicit resources, no occupant reinsertion."""
    from remapeamento_mundo import iniciar_remapeamento
    from classificacao_remapeamento import retomar_classificacao_remapeamento
    classificado = retomar_classificacao_remapeamento(mundo, iniciar_remapeamento(mundo),
                                                     alocar=alocar, fixar=fixar)
    if classificado is False:
        return False
    return retomar_conclusao_remapeamento(mundo, classificado, alocar=alocar, fixar=fixar,
                                          obter_handle=obter_handle, desfixar=desfixar, liberar=liberar)


def _chamar(estado, callback, checkpoint, importacao, argumentos, *, memoria=False):
    if callback is None:
        raise DependenciaConclusaoRemapeamento(estado, checkpoint, importacao, argumentos)
    resultado = callback(*argumentos)
    if memoria:
        return resultado
    if not isinstance(resultado, int):
        raise ValueError('Resource callbacks require explicit integer results')
    return resultado & 0xffffffff


def _escrever_pilha(estado, celula):
    if estado.topo+2 > 0x100000:
        raise FalhaMemoriaConclusaoRemapeamento(estado, 0x42efd9, estado.topo)
    v = memoryview(estado.memoria_pilha).cast('B')
    v[estado.topo:estado.topo+2] = (celula & 65535).to_bytes(2, 'little')
    estado.topo += 2


def retomar_conclusao_remapeamento(mundo, pedido, *, alocar=None, fixar=None,
                                   obter_handle=None, desfixar=None, liberar=None):
    """Consume the live 0x42ef8b handoff, returning the original consumed AL bool.

    Missing-provider exceptions retain a resumable state. Handle queries consume
    the actual live buffer object, whose pointer identity belongs to the owner.
    A NULL second lock exposes the original write fault, never a clean False.
    """
    if isinstance(pedido, ClassificacaoRemapeamento):
        if pedido.endereco_dependencia != 0x42ef8b:
            raise ValueError('Expected the exact remap component-scan checkpoint')
        estado = EstadoConclusaoRemapeamento(pedido)
    elif isinstance(pedido, EstadoConclusaoRemapeamento):
        estado = pedido
    else:
        raise ValueError('Expected a classified remap handoff or its retained continuation state')
    classes = _vista(estado.classificacao.memoria, 65536)
    atributos = _vista(mundo.atributos, 65536, gravavel=True)
    if (not isinstance(mundo.regioes, list) or len(mundo.regioes) != 65536
            or any(not isinstance(r, int) or not 0 <= r <= 65535 for r in mundo.regioes)
            or not isinstance(mundo.largura, int) or not 0 <= mundo.largura <= 65535
            or not isinstance(mundo.altura, int) or not 0 <= mundo.altura <= 65535):
        raise ValueError('Completion requires live u16 regions, writable attributes and u16 dimensions')
    while True:
        fase = estado.fase
        if fase == 'complete':
            return estado.resultado
        if fase == 'scan':
            while estado.celula < 65536 and mundo.regioes[estado.celula] != 0:
                estado.celula += 1
            if estado.celula == 65536:
                estado.fase = 'edge'
                continue
            estado.componentes += 1
            estado.semente = estado.celula
            estado.fase = 'allocate'
        elif fase == 'allocate':
            estado.handle_pilha = _chamar(estado, alocar, 0x42efba, 0x5231c0, (0, 0x100000))
            estado.fase = 'lock'
        elif fase == 'lock':
            estado.memoria_pilha = _chamar(estado, fixar, 0x42efca, 0x5231d0,
                                          (estado.handle_pilha,), memoria=True)
            estado.fase = 'null_write' if estado.memoria_pilha is None else 'seed'
        elif fase == 'null_write':
            raise FalhaMemoriaConclusaoRemapeamento(estado, 0x42efd9, 0)
        elif fase == 'seed':
            pilha = _vista(estado.memoria_pilha, 0x100000, gravavel=True)
            _sem_sobreposicao(pilha, (classes, atributos))
            estado.topo = 0
            _escrever_pilha(estado, estado.celula)
            estado.fase = 'fill'
        elif fase == 'fill':
            pilha = memoryview(estado.memoria_pilha).cast('B')
            classe = classes[estado.semente]
            rotulo = estado.componentes & 65535
            while estado.topo:
                estado.topo -= 2
                c = pilha[estado.topo] | pilha[estado.topo+1] << 8
                if classes[c] != classe or mundo.regioes[c] != 0:
                    continue
                mundo.regioes[c] = rotulo
                x, y = c & 255, c >> 8
                if x: _escrever_pilha(estado, c-1)
                if x < 255: _escrever_pilha(estado, c+1)
                if y < 255: _escrever_pilha(estado, c+256)
                if y: _escrever_pilha(estado, c-256)
                if classe == 0:
                    if x and y: _escrever_pilha(estado, c-257)
                    if x and y < 255: _escrever_pilha(estado, c+255)
                    if x < 255 and y: _escrever_pilha(estado, c-255)
                    if x < 255 and y < 255: _escrever_pilha(estado, c+257)
            estado.fase = 'handle_stack_unlock'
        elif fase == 'handle_stack_unlock':
            estado.handle_operacao = _chamar(estado, obter_handle, 0x42ef4e, 0x5231cc, (estado.memoria_pilha,))
            estado.fase = 'unlock_stack'
        elif fase == 'unlock_stack':
            _chamar(estado, desfixar, 0x42ef56, 0x5231d8, (estado.handle_operacao,))
            estado.fase = 'handle_stack_free'
        elif fase == 'handle_stack_free':
            estado.handle_operacao = _chamar(estado, obter_handle, 0x42ef5e, 0x5231cc, (estado.memoria_pilha,))
            estado.fase = 'free_stack'
        elif fase == 'free_stack':
            _chamar(estado, liberar, 0x42ef66, 0x5231c8, (estado.handle_operacao,))
            estado.celula += 1
            estado.fase = 'scan'
        elif fase == 'edge':
            for y in range(256):
                for x in range(mundo.largura if y < mundo.altura else 0, 256):
                    c = y*256+x
                    mundo.regioes[c] = 0
                    mundo.atributos[c] = 1
            estado.fase = 'handle_class_unlock'
        elif fase == 'handle_class_unlock':
            estado.handle_operacao = _chamar(estado, obter_handle, 0x42f1a0, 0x5231cc,
                                             (estado.classificacao.memoria,))
            estado.fase = 'unlock_class'
        elif fase == 'unlock_class':
            _chamar(estado, desfixar, 0x42f1ac, 0x5231d8, (estado.handle_operacao,))
            estado.fase = 'handle_class_free'
        elif fase == 'handle_class_free':
            estado.handle_operacao = _chamar(estado, obter_handle, 0x42f1b4, 0x5231cc,
                                             (estado.classificacao.memoria,))
            estado.fase = 'free_class'
        elif fase == 'free_class':
            _chamar(estado, liberar, 0x42f1bc, 0x5231c8, (estado.handle_operacao,))
            estado.resultado = (estado.componentes & 65535) < 0x4000
            estado.fase = 'complete'
        else:
            raise ValueError('Unknown retained remap continuation phase')
