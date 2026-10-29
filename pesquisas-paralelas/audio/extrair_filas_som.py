"""Export intact request/queue bytes for the original-first audio stage.

This is static evidence only: it imports neither the emulator nor a Python
queue implementation, and it does not execute any original instruction.
Stage-1 sound captures and manifests are deliberately not rewritten.
"""
import hashlib
import json

from ambiente_audio import CD, ORIGINAL_SHA256, OWNED, ROOT
from analisar import dependencias
from extrair_som import imagem, intervalo, simbolos


def exportar_filas():
    pefile, capstone = dependencias()
    raw = (CD / 'INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest() != ORIGINAL_SHA256:
        raise ValueError('Intact executable identity mismatch')
    pe = pefile.PE(data=raw)
    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    symbols = simbolos()
    next_symbol = {address: symbols[i + 1][0] for i, (address, _) in enumerate(symbols[:-1])}
    selected = [(address, name) for address, name in symbols if 0x489dac <= address < 0x48b390]
    lines = [f'; Intact original SHA-256 {ORIGINAL_SHA256}',
             '; Static request/queue inventory; no execution or reconstructed behavior claim.']
    intervals = []
    for address, name in selected:
        end, instructions = intervalo(pe, decoder, address, next_symbol[address])
        data = imagem(pe, address, end - address)
        intervals.append({'name': name, 'start': hex(address), 'end_exclusive': hex(end),
                          'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
        lines.append(f'; {name}')
        lines.extend(f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip()
                     for i in instructions)
    # Preserve these original initialized bytes without inferring their fields.
    data_address, data_size = 0x498f14, 0x58
    data = imagem(pe, data_address, data_size)
    manifest = {'original_sha256': ORIGINAL_SHA256,
                'symbol_source': 'relatorios/simbolos-originais.tsv',
                'symbol_source_sha256': hashlib.sha256((ROOT / 'relatorios/simbolos-originais.tsv').read_bytes()).hexdigest(),
                'intervals': intervals, 'disassembly': 'filas-som-rotinas.asm',
                'initialized_data': {'start': hex(data_address), 'bytes': len(data),
                                     'hex': data.hex(), 'sha256': hashlib.sha256(data).hexdigest()},
                'scope': 'Static evidence for request/queue original-first capture planning. '
                         'No queue translation, native execution, playback or complete-flow claim.'}
    destination = OWNED / 'evidencias'
    (destination / 'filas-som-rotinas.asm').write_text('\n'.join(lines) + '\n')
    (destination / 'filas-som-manifesto.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


if __name__ == '__main__':
    print('Static intact queue intervals:', len(exportar_filas()['intervals']))
