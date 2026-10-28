"""Record original caller composition and immutable committed-provider evidence."""
import hashlib
import json
from pathlib import Path
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(RAIZ.parent / 'source/python'))
import capstone
import pefile
from capturar_saida_tropa import HASH


def main():
    dados = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(dados).hexdigest() != HASH:
        raise ValueError('Original executable hash mismatch')
    pe = pefile.PE(data=dados)
    imagem, base = pe.get_memory_mapped_image(), pe.OPTIONAL_HEADER.ImageBase
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    inicio, fim = 0x420f5a, 0x420f81
    codigo = imagem[inicio-base:fim-base]
    arquivo = 'producao-compartilhada-00420f5a.asm'
    linhas = [f'; Original production continuation through fatigue; exclusive end 0x{fim:08x}.',
              f'; Original EXE SHA-256: {HASH}']
    linhas += [f'{i.address:08x}  {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}'.rstrip()
               for i in md.disasm(codigo, inicio)]
    (PASTA / 'evidencias' / arquivo).write_text('\n'.join(linhas) + '\n')
    referencias = []
    for relativo in ('evidencias/ciclo-producao.json', 'evidencias/saida-tropa.json',
                     '../../evidencias/posicao-saida/manifesto.json',
                     '../../evidencias/conversao-saida/manifesto.json',
                     '../../evidencias/recuperacao-unidades/manifesto.json'):
        p = PASTA / relativo
        if not p.exists():
            raise ValueError(f'Missing committed provider evidence: {relativo}')
        referencias.append(dict(path=relativo, sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    result = dict(sha256_exe=HASH,
        sha256_sbl=hashlib.sha256((RAIZ.parent / 'source/cd/INSTALHD/RISING.SBL').read_bytes()).hexdigest(),
        consumed_main='62b9d76941dbcf90a2dc5d45b71317136c8b5d28',
        provider_implementations=dict(core_recovery='3b7f71697095ab12e960bf4cbdf0952d20d554d8',
             core_conversion='90fdfa51ab2bb2243d1e81fbd6bc7ab9548c89fa',
             core_position='61e2a2e1201b7e0e020906bb67963a17e5364a8c',
             economy_caller='a9f055ca4fbf30327f5e83b4211ef1e4ad8a7802'),
        scope='Actual CalculTroupe entry through preparation and shared core position/conversion/healing/fatigue; '
              'stop before experience at 0x420f81',
        captures=[dict(start=hex(inicio),end_exclusive=hex(fim),bytes_hex=codigo.hex(),
                       sha256=hashlib.sha256(codigo).hexdigest(),listing=arquivo)],
        committed_evidence=referencias,
        shared_state='Identical live unit and structure objects; loaded type/bonus bytes; no copy/writeback',
        pending_address='0x420f81')
    (PASTA / 'evidencias/producao-compartilhada.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Captured caller interval and checked committed evidence identities.')


if __name__ == '__main__':
    main()
