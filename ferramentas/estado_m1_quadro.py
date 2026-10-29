"""Frozen M1 post-load blocks used as frame-foundation input (no CPU needed).

Reads Missions' read-only original MissionLoad capture v2 and returns the final
DGROUP (0x494000..0x523000) and CRT thread-data (0x3400000, 228 bytes) blocks at
the real return 0x42d22d. This is M1 post-load input, not yet frame-1 input.
"""
import base64
import hashlib
import json
from pathlib import Path
import zlib

RAIZ = Path(__file__).resolve().parents[1]
CAPTURA_M1 = RAIZ / 'pesquisas-paralelas/missoes/evidencias/captura-carga-missao-original-v2.json'
CAPTURA_M1_SHA256 = 'eb7d2303e13e62d4f5692c9cb6ef302b573d138df6a8b51183a6d9b0bd703afc'
DGROUP = (0x494000, 0x523000)
THREAD = (0x3400000, 0x3400000 + 228)


def _bloco(blocos, nome):
    b = blocos[nome]
    dados = zlib.decompress(base64.b64decode(b['zlib_base64']))
    if len(dados) != b['bytes'] or hashlib.sha256(dados).hexdigest() != b['sha256']:
        raise ValueError(f'M1 block {nome} does not match its recorded size/hash')
    return int(b['base'], 16), dados


def carregar_m1():
    """Return (dgroup bytes, thread bytes, provenance) from the frozen capture."""
    bruto = CAPTURA_M1.read_bytes()
    if hashlib.sha256(bruto).hexdigest() != CAPTURA_M1_SHA256:
        raise ValueError('Frozen M1 capture v2 hash mismatch')
    captura = json.loads(bruto)
    final = captura['oracle']['final_state']
    if not captura['oracle']['reached_real_return'] or captura['oracle']['real_return'] != '0x42d22d':
        raise ValueError('M1 capture did not reach the real MissionLoad return')
    base_dg, dgroup = _bloco(final['blocks'], 'dgroup')
    base_th, thread = _bloco(final['blocks'], 'crt_thread_data')
    if (base_dg, base_dg+len(dgroup)) != DGROUP or (base_th, base_th+len(thread)) != THREAD:
        raise ValueError('Unexpected M1 block layout')
    proveniencia = dict(file=str(CAPTURA_M1.relative_to(RAIZ)), sha256=CAPTURA_M1_SHA256,
                        final_state_sha256=final['summary']['sha256'], blocks_used=['dgroup', 'crt_thread_data'],
                        label='M1 post-load input, not yet frame-1 input')
    return dgroup, thread, proveniencia
