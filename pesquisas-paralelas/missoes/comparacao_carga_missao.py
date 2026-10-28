"""Whole-state and binding-sequence comparison of the composed MissionLoad with the original capture.

State: every block of the frozen original final image (DGROUP+.bss, CRT thread
data, all live allocations) is compared byte for byte with the composition's
serialized map, plus every allocation record (live and freed, with the freed
bytes' SHA-256) and AL. Nothing is masked. Bytes that are equal because both
sides consume the same entry bytes (e.g. untouched allocation fill) are simply
equal; they are not excluded. The only fields not compared are the oracle's
native observation metadata of allocation records (caller return addresses and
the eight caller-stack dwords), which the Python callback contract does not
carry and which are not memory state; they are listed in the report.

Bindings: the composition's ordered requests are compared with the original
1,400-event log after normalizing both to (name, arguments, result, cursor,
transferred-bytes SHA-256). Original string arguments are read from the
original final DGROUP (constants) or from the capture's CRT file records.
"""
import struct

from mapa_memoria_m1 import carregar_blocos

CAMPOS_REGISTRO = ('active', 'events', 'flags', 'index', 'initial_byte', 'locks', 'pointer', 'size',
                   'freed_sha256', 'kind')
CAMPOS_NATIVOS_NAO_COMPARADOS = ('caller_return', 'freed_caller_return', 'stack')


class NaoCapturado(str):
    """An original argument string that lives in a native stack frame the capture does not keep."""


def _cadeia(dgroup_base, dgroup, endereco):
    p = endereco - dgroup_base
    if not 0 <= p < len(dgroup):
        return NaoCapturado(f'<native stack 0x{endereco:08x}: not captured>')
    fim = dgroup.index(b'\0', p)
    return bytes(dgroup[p:fim])


def normalizar_vinculos_originais(captura):
    """Original binding events -> normalized requests (same shape as the composition log)."""
    final = carregar_blocos({'dgroup': captura['oracle']['final_state']['blocks']['dgroup']})
    base, dgroup = final['dgroup']
    caminhos = {int(f['stream'], 16): f['path'].encode('latin-1') for f in captura['crt_files'] if 'stream' in f}
    cursores, saida = {}, []
    for e in captura['oracle']['binding_events']:
        nome = e['name']
        a = [int(x, 16) for x in e['arguments']]
        r = int(e['results']['EAX'], 16)
        item = dict(name=nome)
        if nome == 'CRT.fopen':
            item.update(args=(caminhos.get(r), _cadeia(base, dgroup, a[1])), result=r)
            cursores[r] = 0
            fluxo_atual = r
        elif nome == 'CRT.fread':
            _, tamanho, quantidade, fluxo = a
            item.update(args=(tamanho, quantidade), result=r, cursor=cursores[fluxo], stream=fluxo,
                        sha256=e['memory_writes'][0]['sha256'] if e['memory_writes'] else None)
            cursores[fluxo] += tamanho * r
        elif nome == 'FileSeek':
            deslocamento, origem = a
            cursores[fluxo_atual] = (0 if origem == 0 else cursores[fluxo_atual]) + deslocamento
            item.update(args=(deslocamento, origem), result=r, cursor=cursores[fluxo_atual], stream=fluxo_atual)
        elif nome == 'CRT.fclose':
            item.update(args=(a[0],), result=r)
        elif nome == 'KERNEL32.GetPrivateProfileIntA':
            item.update(args=(_cadeia(base, dgroup, a[0]), _cadeia(base, dgroup, a[1]), a[2],
                              _cadeia(base, dgroup, a[3])), result=r)
        elif nome == 'KERNEL32.GetPrivateProfileStringA':
            item.update(args=(_cadeia(base, dgroup, a[0]), _cadeia(base, dgroup, a[1]),
                              _cadeia(base, dgroup, a[2]), a[4], _cadeia(base, dgroup, a[5])), result=r,
                        written_sha256=e['memory_writes'][0]['sha256'] if e['memory_writes'] else None)
        elif nome == 'KERNEL32.GlobalAlloc':
            item.update(args=(a[0], a[1]), result=r)
        elif nome in ('KERNEL32.GlobalLock', 'KERNEL32.GlobalHandle', 'KERNEL32.GlobalUnlock',
                      'KERNEL32.GlobalFree'):
            item.update(args=(a[0],), result=r)
        else:
            raise ValueError(f'Unexpected original binding {nome}')
        saida.append(item)
    return saida


_CHAVES = ('name', 'args', 'result', 'cursor', 'sha256', 'written_sha256', 'stream')


def _iguais(o, c, nao_observados):
    """Field equality; an original argument kept only in an uncaptured stack frame is not compared."""
    for k in _CHAVES:
        a, b = o.get(k), c.get(k)
        if k == 'args' and isinstance(a, tuple) and isinstance(b, tuple) and len(a) == len(b):
            for x, y in zip(a, b):
                if isinstance(x, NaoCapturado):
                    nao_observados.append(x)
                elif x != y:
                    return False
        elif a != b:
            return False
    return True


def comparar_vinculos(registro, captura, limite=10):
    originais = normalizar_vinculos_originais(captura)
    composicao = [{k: v for k, v in item.items() if k in _CHAVES} for item in registro]
    diferencas, nao_observados = [], []
    for i in range(max(len(originais), len(composicao))):
        o = originais[i] if i < len(originais) else None
        c = composicao[i] if i < len(composicao) else None
        if o is None or c is None or not _iguais(o, c, nao_observados):
            diferencas.append(i)
    def _json(item):
        if item is None:
            return None
        return {k: (v.decode('latin-1') if isinstance(v, bytes) else
                    [x.decode('latin-1') if isinstance(x, bytes) else x for x in v] if isinstance(v, tuple) else v)
                for k, v in item.items()}
    return dict(original_events=len(originais), composed_requests=len(composicao),
                mismatching_positions=len(diferencas), equal=not diferencas,
                original_arguments_not_captured=dict(
                    count=len(nao_observados), values=sorted(set(nao_observados)),
                    reason='string built by the original in its own stack frame (e.g. the GROUPE%02d key '
                           'of GetPrivateProfileStringA); the capture keeps no final native stack, so only '
                           'the other fields (section, default, size, file, result, written-bytes SHA-256) '
                           'are compared at those positions'),
                first_mismatches=[dict(position=i, original=_json(originais[i] if i < len(originais) else None),
                                       composed=_json(composicao[i] if i < len(composicao) else None))
                                  for i in diferencas[:limite]])


def comparar_estado(composicao, captura, entrada_blocos, *, al=None, limite=12):
    """Compare the composition's serialized map with the original final image and records."""
    finais = carregar_blocos(captura['oracle']['final_state']['blocks'])
    python = composicao.mapa.serializar()
    blocos, total_diferentes, total_bytes = {}, 0, 0
    nomes = sorted(set(finais) | (set(python) - {'native_stack'}))
    for nome in nomes:
        if nome not in finais or nome not in python:
            blocos[nome] = dict(present_original=nome in finais, present_composed=nome in python)
            total_diferentes += 1
            continue
        (bo, do), (bp, dp) = finais[nome], python[nome]
        info = dict(base=hex(bo), bytes=len(do))
        if bo != bp or len(do) != len(dp):
            info.update(layout_mismatch=dict(composed_base=hex(bp), composed_bytes=len(dp)))
            total_diferentes += 1
        else:
            entrada = entrada_blocos.get(nome, (None, None))[1]
            difs = [i for i in range(len(do)) if do[i] != dp[i]] if do != dp else []
            info['differing_bytes'] = len(difs)
            total_bytes += len(do)
            total_diferentes += len(difs)
            if difs:
                primeiros = []
                for i in difs[:limite]:
                    dono, deslocamento = composicao.mapa.dono(bo + i)
                    primeiros.append(dict(address=hex(bo + i), owner=dono, owner_offset=deslocamento,
                                          original=do[i], composed=dp[i],
                                          entry=None if entrada is None else entrada[i]))
                info['first_mismatches'] = primeiros
                # Group into contiguous runs for root-cause analysis.
                corridas, inicio, anterior = [], difs[0], difs[0]
                for i in difs[1:]:
                    if i != anterior + 1:
                        corridas.append((inicio, anterior + 1))
                        inicio = i
                    anterior = i
                corridas.append((inicio, anterior + 1))
                info['runs'] = len(corridas)
                info['first_runs'] = [dict(start=hex(bo + a), end=hex(bo + b), bytes=b - a,
                                           owner=composicao.mapa.dono(bo + a)[0]) for a, b in corridas[:limite]]
        blocos[nome] = info
    registros = composicao.arena.registros
    originais = captura['allocations']
    reg_difs = []
    for i in range(max(len(registros), len(originais))):
        o = originais[i] if i < len(originais) else None
        c = registros[i] if i < len(registros) else None
        if o is None or c is None:
            reg_difs.append(dict(index=i, original=o, composed=c))
            continue
        campos = [k for k in CAMPOS_REGISTRO if o.get(k) != c.get(k)]
        if campos:
            reg_difs.append(dict(index=i, fields={k: dict(original=o.get(k), composed=c.get(k)) for k in campos}))
    al_original = captura['oracle']['al']
    return dict(
        blocks_compared=len(nomes), bytes_compared=total_bytes, differing_bytes_or_blocks=total_diferentes,
        blocks_with_differences=sorted(n for n, i in blocos.items() if i.get('differing_bytes') or
                                       'layout_mismatch' in i or 'present_original' in i),
        blocks={n: i for n, i in blocos.items() if i.get('differing_bytes') or 'layout_mismatch' in i
                or 'present_original' in i},
        allocation_records=dict(original=len(originais), composed=len(registros),
                                differing=len(reg_difs), first_differences=reg_difs[:limite],
                                compared_fields=list(CAMPOS_REGISTRO),
                                not_compared_native_metadata=list(CAMPOS_NATIVOS_NAO_COMPARADOS)),
        al=dict(original=al_original, composed=al, equal=al == al_original),
        native_stack='not in the original final capture; the composition models no stack locals',
        equal=(total_diferentes == 0 and not reg_difs and al == al_original))
