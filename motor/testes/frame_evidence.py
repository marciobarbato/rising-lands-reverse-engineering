"""Pure offline evidence helpers copied mechanically from the accepted Python harness.

The source definitions are unchanged; only their imports are supplied here so
loading a frozen capture does not import the x86 emulator. FRAME_AUDIT.md records
source pins. This module never simulates game behavior.
"""
import base64
import bisect
import hashlib
import json
import struct
import zlib
from contexto_exibicao_ia import ContextoAmbiguo
METADADOS_ALOCACAO = ('caller_return', 'stack', 'freed_caller_return')
VINCULO = ('name', 'arguments', 'caller_return', 'results', 'memory_writes')
FRONTEIRA = ('phase', 'routine', 'caller_return', 'caller', 'top_callee', 'registers', 'declared_eax',
             'stack_cleanup', 'guards', 'stack_words')

def comparar_eventos(python, original, campos):
    saida = dict(python=len(python), original=len(original), equal=len(python) == len(original), not_modeled=[])
    for i, (p, o) in enumerate(zip(python, original)):
        for campo in campos:
            pv, ov = p.get(campo), o.get(campo)
            if campo == 'stack_words' and (pv is None or None in pv):
                pv = pv or [None] * 4
                saida['not_modeled'].append(dict(index=i, routine=o.get('routine'),
                                                 words=[k for k, w in enumerate(pv) if w is None]))
                pv = [o[campo][k] if w is None else w for k, w in enumerate(pv)]
            if pv != ov:
                saida['equal'] = False
                saida.setdefault('first_difference', dict(index=i, field=campo, python=pv, original=ov))
    return saida


class MascaraEnderecos:
    """Exclusion ranges by address: N-frame ``[[start, end], ...]`` or M2.1 ``[{block, start, end}, ...]``."""
    def __init__(self, faixas):
        pares = sorted((int(f['start'], 16), int(f['end'], 16)) if isinstance(f, dict) else
                       (int(f[0], 16), int(f[1], 16)) for f in faixas)
        self.inicios, self.fins = [a for a, _ in pares], [z for _, z in pares]
        self.bytes = sum(z - a for a, z in pares)

    def _sobrepostas(self, base, fim):
        i = max(0, bisect.bisect_right(self.inicios, base) - 1)
        while i < len(self.inicios) and self.inicios[i] < fim:
            if self.fins[i] > base:
                yield max(self.inicios[i], base), min(self.fins[i], fim)
            i += 1

    def aplicar(self, base, dados):
        faixas = list(self._sobrepostas(base, base + len(dados)))
        if not faixas:
            return dados, 0
        b = bytearray(dados)
        for a, z in faixas:
            b[a - base:z - base] = bytes(z - a)
        return bytes(b), sum(z - a for a, z in faixas)

    def mascarado(self, endereco):
        return any(True for _ in self._sobrepostas(endereco, endereco + 1))


class IntegridadeCaptura(RuntimeError):
    """The capture's own replay (deltas, summaries, checkpoint full states) is inconsistent."""


def resumo_estado(blocos):
    """Missions' ``oraculo_carga_missao.resumo_imagem`` over a block dict (name -> (base, bytes))."""
    h = hashlib.sha256()
    for nome in sorted(blocos):
        base, dados = blocos[nome]
        h.update(struct.pack('<II', base, len(dados)))
        h.update(dados)
    return dict(blocks=len(blocos), bytes=sum(len(d) for _, d in blocos.values()), sha256=h.hexdigest())


def resumos_mascarados(mascara, blocos):
    """(compared_summary, masked_sha256) with the definitions of Missions' ``pacotes_quadros_missao``.

    compared_summary is ``resumo_imagem`` with every masked byte set to 0. masked_sha256 is SHA-256 over, for
    each block sorted by name and each mask range intersecting it in address order,
    ``<II start, length>`` + those bytes. ``native_stack`` is never a block.
    """
    comparado, mascarado = {}, hashlib.sha256()
    for nome in sorted(blocos):
        if nome == 'native_stack':
            continue
        base, dados = blocos[nome]
        faixas = list(mascara._sobrepostas(base, base + len(dados)))
        if faixas:
            buf = bytearray(dados)
            for a, z in faixas:
                mascarado.update(struct.pack('<II', a, z - a))
                mascarado.update(dados[a - base:z - base])
                buf[a - base:z - base] = bytes(z - a)
            dados = bytes(buf)
        comparado[nome] = (base, dados)
    return resumo_estado(comparado), mascarado.hexdigest()


def _dados(campo):
    if 'zlib_base64' in campo:
        return zlib.decompress(base64.b64decode(campo['zlib_base64']))
    return bytes.fromhex(campo['hex'])


def aplicar_delta(estado, delta, fase):
    """``state_delta`` onto a copy of ``estado``: released, then allocated, then the byte ranges."""
    novo = dict(estado)
    for nome in delta.get('released', ()):
        if nome not in novo:
            raise IntegridadeCaptura(f'{fase}: released block {nome} is not live')
        del novo[nome]
    for nome, bloco in delta.get('allocated', {}).items():
        if nome in novo:
            raise IntegridadeCaptura(f'{fase}: allocated block {nome} already live')
        novo[nome] = (int(bloco['base'], 16), _dados(bloco))
    por_base = sorted((b, n) for n, (b, _) in novo.items())
    bases = [b for b, _ in por_base]
    editados = {}
    for faixa in delta.get('ranges', ()):
        endereco, dados = int(faixa['address'], 16), _dados(faixa)
        i = bisect.bisect_right(bases, endereco) - 1
        nome = por_base[i][1] if i >= 0 else None
        if nome is None or endereco + len(dados) > novo[nome][0] + len(novo[nome][1]):
            raise IntegridadeCaptura(f'{fase}: range 0x{endereco:x}+{len(dados)} is not inside one live block')
        if nome not in editados:
            editados[nome] = bytearray(novo[nome][1])
        o = endereco - novo[nome][0]
        editados[nome][o:o + len(dados)] = dados
    for nome, dados in editados.items():
        novo[nome] = (novo[nome][0], bytes(dados))
    return novo


def fases_referencia(cap, s0, mascara=None):
    """Yield (phase capture, full block state after it, integrity record), replaying from ``s0``.

    With ``mascara``, a phase's ``compared_summary`` and ``masked_sha256`` (M2.3 parts) are checked too."""
    estado = dict(s0)
    for fase in cap['phases']:
        apos = fase['state_after']
        if 'blocks_changed_since_previous' in apos:
            estado = dict(estado)
            for nome, bloco in apos['blocks_changed_since_previous'].items():
                estado[nome] = (int(bloco['base'], 16), _dados(bloco))
            estado = {n: v for n, v in estado.items() if n in apos['block_hashes']}
            forma = 'v2_blocks'
        else:
            estado = aplicar_delta(estado, fase['state_delta'], fase['phase'])
            forma = 'delta'
        integridade = dict(form=forma)
        if 'summary' in apos:
            resumo = resumo_estado({n: v for n, v in estado.items() if n != 'native_stack'})
            integridade['summary_equal'] = resumo == apos['summary']
            if not integridade['summary_equal']:
                raise IntegridadeCaptura(f"{fase['phase']}: replayed state {resumo} != summary {apos['summary']}")
        if 'compared_summary' in apos or 'masked_sha256' in apos:
            if mascara is None:
                raise IntegridadeCaptura(f"{fase['phase']}: compared_summary present but no mask given")
            comparado, mascarado = resumos_mascarados(mascara, estado)
            integridade['compared_summary_equal'] = comparado == apos.get('compared_summary', comparado)
            integridade['masked_sha256_equal'] = mascarado == apos.get('masked_sha256', mascarado)
            if not (integridade['compared_summary_equal'] and integridade['masked_sha256_equal']):
                raise IntegridadeCaptura(f"{fase['phase']}: replayed compared_summary/masked_sha256 differ")
        if 'full_state' in apos:
            completo = {n: (int(b['base'], 16), _dados(b)) for n, b in apos['full_state'].items()}
            atual = {n: v for n, v in estado.items() if n in completo or n != 'native_stack'}
            integridade['checkpoint_full_state_equal'] = completo == atual
            if not integridade['checkpoint_full_state_equal']:
                diferentes = sorted(n for n in set(completo) | set(atual) if completo.get(n) != atual.get(n))
                raise IntegridadeCaptura(f"{fase['phase']}: checkpoint full state differs from the replay in "
                                         f"{diferentes[:8]}")
        elif forma == 'delta' and 'summary' not in apos:
            raise IntegridadeCaptura(f"{fase['phase']}: delta phase without a summary hash")
        yield fase, estado, integridade


def carregar_captura(caminho, sha256_bruto=None):
    """The capture JSON, xz-decompressed when the name ends in .xz; the raw JSON hash checked when pinned."""
    import lzma
    bruto = caminho.read_bytes()
    if caminho.suffix == '.xz':
        bruto = lzma.decompress(bruto)
    h = hashlib.sha256(bruto).hexdigest()
    if sha256_bruto is not None and h != sha256_bruto:
        raise IntegridadeCaptura(f'raw capture SHA-256 {h} != pinned {sha256_bruto}')
    return json.loads(bruto), h


def comparar_estado(mascara, python, referencia):
    diferentes, comparados, primeiras = [], 0, {}
    for nome in sorted(set(python) | set(referencia)):
        if nome == 'native_stack':
            continue
        if nome not in python or nome not in referencia:
            diferentes.append(nome)
            primeiras.setdefault(nome, 'missing in Python' if nome not in python else 'extra in Python')
            continue
        base, o = referencia[nome]
        pb, p = python[nome]
        o, excluidos = mascara.aplicar(base, o)
        p, _ = mascara.aplicar(pb, p)
        comparados += len(o) - excluidos
        if pb != base or p != o:
            diferentes.append(nome)
            if len(primeiras) < 5:
                primeiras[nome] = [[hex(base + i), o[i], p[i]] for i in range(min(len(o), len(p)))
                                   if o[i] != p[i]][:12]
    return dict(equal=not diferentes, blocks=len(referencia), compared_bytes=comparados,
                differing_blocks=diferentes[:40], first_differences=primeiras)


def eventos_logicos(referencia, python, classe, campos):
    """Reference events outside display context, aligned with Python's events in order."""
    saida, exibicao, ambiguos_resolvidos, ambiguos_sem_par = [], [], [], []
    j = 0
    for i, e in enumerate(referencia):
        try:
            c = classe(e)
        except ContextoAmbiguo as erro:
            if j < len(python) and comparar_eventos([python[j]], [e], campos)['equal']:
                saida.append(e)
                ambiguos_resolvidos.append(dict(index=i, issuer=erro.rotina))
                j += 1
            else:
                ambiguos_sem_par.append(dict(index=i, issuer=erro.rotina, event=e.get('name') or e.get('routine')))
            continue
        if c == 'display':
            exibicao.append(i)
            continue
        saida.append(e)
        j += 1
    return saida, exibicao, ambiguos_resolvidos, ambiguos_sem_par


def comparar_eventos_fase(python, referencia, classe, campos, rotulo):
    filtrados, exibicao, resolvidos, sem_par = eventos_logicos(referencia, python, classe, campos)
    r = comparar_eventos(python, filtrados, campos)
    r.update(display_context_not_modeled=len(exibicao), shared_issuers_matched=resolvidos,
             shared_issuers_unmatched=sem_par)
    if rotulo == 'boundaries':
        r['display_context_not_modeled'] = [referencia[i]['routine'] + ' @ ' + referencia[i]['caller']
                                            for i in exibicao]
    if sem_par:
        r['equal'] = False
    return r


def comparar_alocacoes(python, referencia):
    limpo = lambda r: {k: v for k, v in r.items() if k not in METADADOS_ALOCACAO}  # noqa: E731
    a, b = [limpo(r) for r in python], [limpo(r) for r in referencia]
    dif = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
    return dict(equal=a == b, python=len(a), reference=len(b),
                first_differences=[dict(index=i, python=a[i], reference=b[i]) for i in dif[:5]],
                excluded_metadata=list(METADADOS_ALOCACAO))


def ler_estado(estado, endereco, largura):
    for base, dados in estado.values():
        if base <= endereco and endereco + largura <= base + len(dados):
            return int.from_bytes(dados[endereco - base:endereco - base + largura], 'little')
    return None
