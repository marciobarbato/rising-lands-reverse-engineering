"""Exact per-phase state deltas for N-frame captures (M2.2 delta form), and their replay check.

A phase's ``state_delta`` turns the previous phase's block state into the next
one, applied in this order:

* ``released``: names of blocks no longer live;
* ``allocated``: ``{name: {base, zlib_base64}}`` for new blocks (or a block whose
  base or size changed, which is released and allocated again);
* ``ranges``: ``[{address, hex | zlib_base64}]``, each inside one live block,
  carrying the new bytes.  Ranges cover every differing byte; two differing runs
  closer than ``FOLGA`` bytes share one range (the bytes between them are
  carried with their unchanged value).

``state_after.summary`` is ``resumo_imagem`` of the state after the phase
(``native_stack`` excluded), and checkpoint phases add ``full_state``
(``{name: {base, zlib_base64}}``).  This is the form AI/runtime's
``comparar_quadros_ia`` reads.  Importing this module executes nothing.
"""
import base64
import bisect
import hashlib
import json
import lzma
import struct
import zlib

FOLGA = 8          # merge differing runs separated by fewer bytes than this
TROCO = 64         # chunk size of the first equality scan
HEX_MAXIMO = 32    # ranges up to this length are stored as hex, longer ones as zlib_base64


class ReplayDivergente(RuntimeError):
    """The capture's deltas do not rebuild its own summaries or checkpoint states."""


def resumo(blocos):
    """``oraculo_carga_missao.resumo_imagem`` without ``native_stack``."""
    h = hashlib.sha256()
    blocos = {n: v for n, v in blocos.items() if n != 'native_stack'}
    for nome in sorted(blocos):
        base, dados = blocos[nome]
        h.update(struct.pack('<II', base, len(dados)))
        h.update(dados)
    return dict(blocks=len(blocos), bytes=sum(len(d) for _, d in blocos.values()), sha256=h.hexdigest())


def _codificar(dados):
    if len(dados) <= HEX_MAXIMO:
        return dict(hex=dados.hex())
    return dict(zlib_base64=base64.b64encode(zlib.compress(dados, 9)).decode('ascii'))


def _decodificar(campo):
    if 'zlib_base64' in campo:
        return zlib.decompress(base64.b64decode(campo['zlib_base64']))
    return bytes.fromhex(campo['hex'])


def faixas_diferentes(velho, novo):
    """[(offset, end)) runs covering every differing byte of two equal-length buffers."""
    n, faixas = len(novo), []
    for i in range(0, n, TROCO):
        if velho[i:i+TROCO] == novo[i:i+TROCO]:
            continue
        fim = min(i+TROCO, n)
        j = i
        while j < fim:
            if velho[j] != novo[j]:
                k = j+1
                while k < fim and velho[k] != novo[k]:
                    k += 1
                if faixas and j - faixas[-1][1] < FOLGA:
                    faixas[-1][1] = k
                else:
                    faixas.append([j, k])
                j = k
            else:
                j += 1
    return [tuple(f) for f in faixas]


def delta(anterior, atual):
    """``state_delta`` from block state ``anterior`` to ``atual`` (both name -> (base, bytes))."""
    liberados, alocados, faixas = [], {}, []
    for nome in sorted(anterior):
        if nome == 'native_stack':
            continue
        if nome not in atual or atual[nome][0] != anterior[nome][0] or len(atual[nome][1]) != len(anterior[nome][1]):
            liberados.append(nome)
    for nome in sorted(atual):
        if nome == 'native_stack':
            continue
        base, dados = atual[nome]
        if nome not in anterior or nome in liberados:
            alocados[nome] = dict(base=hex(base), zlib_base64=base64.b64encode(zlib.compress(dados, 9)).decode('ascii'))
            continue
        velho = anterior[nome][1]
        if velho == dados:
            continue
        for o, f in faixas_diferentes(velho, dados):
            faixas.append(dict(address=hex(base+o), **_codificar(dados[o:f])))
    return dict(released=liberados, allocated=alocados, ranges=faixas)


def estado_completo(blocos):
    return {n: dict(base=hex(b), zlib_base64=base64.b64encode(zlib.compress(d, 9)).decode('ascii'))
            for n, (b, d) in sorted(blocos.items()) if n != 'native_stack'}


def aplicar(estado, d, fase):
    """Apply one ``state_delta`` to a copy of ``estado``."""
    novo = dict(estado)
    for nome in d['released']:
        if nome not in novo:
            raise ReplayDivergente(f'{fase}: released block {nome} is not live')
        del novo[nome]
    for nome, bloco in d['allocated'].items():
        if nome in novo:
            raise ReplayDivergente(f'{fase}: allocated block {nome} already live')
        novo[nome] = (int(bloco['base'], 16), _decodificar(bloco))
    por_base = sorted((b, n) for n, (b, _) in novo.items())
    bases = [b for b, _ in por_base]
    editados = {}
    for faixa in d['ranges']:
        endereco, dados = int(faixa['address'], 16), _decodificar(faixa)
        i = bisect.bisect_right(bases, endereco) - 1
        nome = por_base[i][1] if i >= 0 else None
        if nome is None or endereco + len(dados) > novo[nome][0] + len(novo[nome][1]):
            raise ReplayDivergente(f'{fase}: range {hex(endereco)}+{len(dados)} is not inside one live block')
        buf = editados.setdefault(nome, bytearray(novo[nome][1]))
        o = endereco - novo[nome][0]
        buf[o:o+len(dados)] = dados
    for nome, buf in editados.items():
        novo[nome] = (novo[nome][0], bytes(buf))
    return novo


def verificar_replay(captura, s0):
    """Rebuild every phase from ``s0``; every summary and checkpoint full state must match.

    Returns the per-phase record; raises ``ReplayDivergente`` at the first mismatch.
    """
    if resumo(s0) != captura['state_s0']['summary']:
        raise ReplayDivergente('s0 does not match state_s0.summary')
    estado, registro = dict(s0), []
    for fase in captura['phases']:
        nome = fase['phase']
        estado = aplicar(estado, fase['state_delta'], nome)
        apos = fase['state_after']
        if resumo(estado) != apos['summary']:
            raise ReplayDivergente(f'{nome}: replayed summary {resumo(estado)} != {apos["summary"]}')
        item = dict(phase=nome, summary_equal=True)
        if 'full_state' in apos:
            completo = {n: (int(b['base'], 16), _decodificar(b)) for n, b in apos['full_state'].items()}
            atual = {n: v for n, v in estado.items() if n != 'native_stack'}
            if completo != atual:
                diferentes = sorted(n for n in set(completo) | set(atual) if completo.get(n) != atual.get(n))
                raise ReplayDivergente(f'{nome}: checkpoint full state differs in {diferentes[:8]}')
            item['checkpoint_full_state_equal'] = True
        registro.append(item)
    return registro


def carregar(caminho):
    """(capture dict, SHA-256 of the raw JSON bytes); ``.xz`` files are decompressed."""
    bruto = caminho.read_bytes()
    if caminho.suffix == '.xz':
        bruto = lzma.decompress(bruto)
    return json.loads(bruto), hashlib.sha256(bruto).hexdigest()


def s0_exibicao():
    """The -v2 display scenario's MissionLoad final state, rebuilt from its committed capture."""
    import cenarios_oraculo
    from mapa_memoria_m1 import carregar_blocos, carregar_json, expandir_captura
    m1 = expandir_captura(carregar_json(cenarios_oraculo.caminho('exibicao', 'captura_m1')),
                          carregar_json(cenarios_oraculo.caminho('exibicao', 'entrada')))
    return carregar_blocos(m1['oracle']['final_state']['blocks'])
