"""Explicit test-resource counterpart and complete frozen-image projections."""
import base64
import hashlib
import struct
import zlib

from cenarios_conclusao_remapeamento import preparar_conclusao
from conclusao_remapeamento import remapear_mundo, FalhaMemoriaConclusaoRemapeamento
from vinculos_declarados import ParadaVinculoDeclarado

CLASSES, PILHA_COMPONENTE = 0x1900000, 0x1920000


class RecursosConclusao:
    """Finite explicit fixed allocations matching only the captured fixtures."""
    def __init__(self, caso):
        self.caso = caso
        self.memoria = {CLASSES: bytearray(b'\xa5'*65536), PILHA_COMPONENTE: bytearray(b'\xa7'*0x100000)}
        self.recursos, self.eventos, self.componentes = {}, [], 0

    def _registrar(self, nome, argumentos, operacao, *, memoria=False):
        evento = dict(name=nome, arguments=list(argumentos), status='entered')
        self.eventos.append(evento)
        try:
            resultado = operacao()
            eax = (0 if resultado is None else next(p for p, b in self.memoria.items() if b is resultado)) if memoria else resultado
            evento.update(status='returned', eax=eax)
            return resultado
        except ParadaVinculoDeclarado:
            evento['status'] = 'stopped'
            raise

    def alocar(self, flags, tamanho):
        def executar():
            if flags != 0 or tamanho not in (65536, 0x100000):
                raise ParadaVinculoDeclarado('Unsupported fixture allocation')
            p = CLASSES if tamanho == 65536 else PILHA_COMPONENTE
            if self.recursos.get(p, {}).get('active'):
                raise ParadaVinculoDeclarado('Fixture allocation still live')
            if p == PILHA_COMPONENTE: self.componentes += 1
            self.recursos[p] = dict(size=tamanho, active=True, locked=False,
                                   generation=self.componentes if p != CLASSES else 0)
            return p
        return self._registrar('GlobalAlloc', (flags, tamanho), executar)

    def fixar(self, handle):
        def executar():
            if handle == PILHA_COMPONENTE:
                if self.caso == 'component_lock_unavailable': raise ParadaVinculoDeclarado('Unavailable lock')
                if self.caso == 'component_lock_null': return None
            self.recursos[handle]['locked'] = True
            return self.memoria[handle]
        return self._registrar('GlobalLock', (handle,), executar, memoria=True)

    def obter_handle(self, memoria):
        p = next(p for p, b in self.memoria.items() if b is memoria)
        return self._registrar('GlobalHandle', (p,), lambda: p)

    def desfixar(self, handle):
        def executar():
            if self.caso == 'cleanup_unavailable' and handle == PILHA_COMPONENTE:
                raise ParadaVinculoDeclarado('Unavailable unlock')
            self.recursos[handle]['locked'] = False
            return 0
        return self._registrar('GlobalUnlock', (handle,), executar)

    def liberar(self, handle):
        def executar():
            self.recursos[handle]['active'] = False
            return 0
        return self._registrar('GlobalFree', (handle,), executar)

    def callbacks(self):
        return dict(alocar=self.alocar, fixar=self.fixar, obter_handle=self.obter_handle,
                    desfixar=self.desfixar, liberar=self.liberar)


class Traco:
    def __init__(self):
        self.hashes = {n: hashlib.sha256() for n in ('stack', 'regions', 'attributes')}
        self.contagens = {n: 0 for n in self.hashes}
        self.maior_offset_pilha = 0

    def escrever(self, nome, offset, tamanho, valor):
        self.hashes[nome].update(struct.pack('<IIQ', offset, tamanho, valor))
        self.contagens[nome] += 1
        if nome == 'stack': self.maior_offset_pilha = max(self.maior_offset_pilha, offset+tamanho)

    def resumo(self):
        return {n: dict(count=self.contagens[n], sha256=h.hexdigest()) for n, h in self.hashes.items()}


def executar_modelo(nome):
    import conclusao_remapeamento as modulo
    from copy import deepcopy
    mundo, _ = preparar_conclusao(nome)
    retidos = {k: deepcopy(v) for k, v in vars(mundo).items()
               if k not in ('busca', 'regioes', 'atributos', 'cores_estruturas')}
    traco = Traco()
    class Regioes(list):
        def __setitem__(self, chave, valor):
            if isinstance(chave, int): traco.escrever('regions', chave*2, 2, valor)
            super().__setitem__(chave, valor)
    class Atributos(bytearray):
        def __setitem__(self, chave, valor):
            if isinstance(chave, int): traco.escrever('attributes', chave, 1, valor)
            super().__setitem__(chave, valor)
    mundo.regioes, mundo.atributos = Regioes(mundo.regioes), Atributos(mundo.atributos)
    recursos = RecursosConclusao(nome)
    original = modulo._escrever_pilha
    def escrever(estado, celula):
        offset = estado.topo
        original(estado, celula)
        traco.escrever('stack', offset, 2, celula & 65535)
    modulo._escrever_pilha = escrever
    resultado = None
    erro = None
    try:
        resultado = remapear_mundo(mundo, **recursos.callbacks())
        outcome = 'original_return'
    except ParadaVinculoDeclarado as e:
        outcome, erro = 'declared_fixture_stop', e
    except FalhaMemoriaConclusaoRemapeamento as e:
        outcome, erro = 'expected_original_null_lock_fault', e
    finally:
        modulo._escrever_pilha = original
    assert {k: v for k, v in vars(mundo).items() if k in retidos} == retidos, 'Unrelated world state changed'
    return mundo, recursos, traco, outcome, resultado, erro


def expandir(blocos):
    r = {}
    for a, b in blocos.items():
        dados = zlib.decompress(base64.b64decode(b['zlib_base64']))
        if len(dados) != b['size'] or hashlib.sha256(dados).hexdigest() != b['sha256']:
            raise ValueError('Frozen original block hash mismatch')
        r[int(a, 16)] = bytearray(dados)
    return r


def imagem_modelo(inicial, mundo, recursos):
    """Overlay every intended remap store onto the whole inherited native image.

    All other mapped bytes/tails must match the independently captured final
    image. The model also asserts its other complete world fields unchanged.
    """
    blocos = expandir(inicial)
    def escrever(endereco, dados):
        for a, b in blocos.items():
            if a <= endereco and endereco+len(dados) <= a+len(b):
                b[endereco-a:endereco-a+len(dados)] = dados
                return
        raise ValueError('Expected mapped original fixture range')
    for a, fmt, valor in ((0x496304, 'H', mundo.busca.unidade), (0x4e0f36, 'B', mundo.busca.ocupada),
                           (0x4e0f37, 'B', mundo.busca.sucesso), (0x4e0f3c, 'I', mundo.busca.ponteiro_rota)):
        escrever(a, struct.pack('<'+fmt, valor))
    escrever(0x1800000, bytes(mundo.cores_estruturas.grade))
    escrever(0x4e1570, bytes(mundo.cores_estruturas.livres))
    escrever(0x4e1670, bytes(mundo.cores_estruturas.liberadas))
    escrever(0x1400000, bytes(mundo.atributos))
    escrever(0x1410000, struct.pack('<65536H', *mundo.regioes))
    for a, dados in recursos.memoria.items(): escrever(a, dados)
    return blocos


def conferir_captura(caso):
    mundo, recursos, traco, outcome, resultado, erro = executar_modelo(caso['name'])
    assert outcome == caso['outcome'], (outcome, caso['outcome'])
    if outcome == 'original_return': assert int(resultado) == caso['consumed_al']
    if outcome == 'expected_original_null_lock_fault': assert (erro.checkpoint, erro.endereco) == (0x42efd9, 0)
    esperado = imagem_modelo(caso['initial'], mundo, recursos)
    assert esperado == expandir(caso['final']), 'Whole mapped world/resource image mismatch'
    n = caso['native_state']
    assert {hex(p): r for p, r in recursos.recursos.items()} == n['resources']
    assert traco.resumo() == n['write_trace'], 'Ordered stack/region/edge writes mismatch'
    assert traco.maior_offset_pilha == n['stack_high_water_bytes']
    assert recursos.componentes == n['component_allocations']
    projeção = [dict(name=e['name'], arguments=e['arguments'], status=e['status'],
                    **({'eax': e['results']['EAX']} if e['status'] == 'returned' else {})) for e in n['bindings']]
    assert recursos.eventos == projeção, 'Ordered resource calls/results/stops mismatch'
    return dict(case=caso['name'],outcome=outcome,whole_bytes=sum(map(len, esperado.values())),
                component_allocations=recursos.componentes,ordered_writes_equal=True,
                resource_calls=len(recursos.eventos),consumed_al=None if resultado is None else int(resultado))
