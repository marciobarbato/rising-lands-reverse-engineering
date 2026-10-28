"""Capture joined cleanup provenance and an additive original-symbol erratum."""
import hashlib
import json
from pathlib import Path
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0,str(RAIZ.parent/'source/python'))
import capstone
import pefile
from capturar_saida_tropa import HASH


def main():
    dados = (RAIZ.parent/'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(dados).hexdigest()!=HASH:raise ValueError('Original EXE hash mismatch')
    catalogo = json.loads((RAIZ/'relatorios/simbolos-originais.json').read_text())
    sbl = (RAIZ.parent/'source/cd/INSTALHD/RISING.SBL').read_bytes()
    if hashlib.sha256(sbl).hexdigest()!=catalogo['sha256_sbl']:raise ValueError('Original SBL hash mismatch')
    simbolo = next(s for s in catalogo['simbolos'] if int(s['endereco'],16)==0x41aee2)
    if simbolo['nome_original']!='BatimentGetCase':raise ValueError('Unexpected original symbol')
    pe = pefile.PE(data=dados)
    inicio,fim = 0x420fb7,0x421250
    base = pe.OPTIONAL_HEADER.ImageBase
    codigo = pe.get_memory_mapped_image()[inicio-base:fim-base]
    md = capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
    arquivo = 'producao-limpa-00420fb7.asm'
    linhas = ['; Original cleanup context; terrain and AI calls remain unsupported.',
              f'; EXE SHA-256:{HASH}; exclusive end0x{fim:x}.']
    linhas += [f'{i.address:08x}  {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}'.rstrip()
               for i in md.disasm(codigo,inicio)]
    (PASTA/'evidencias'/arquivo).write_text('\n'.join(linhas)+'\n')
    refs = []
    for rel in ('evidencias/producao-solicitada.json','evidencias/limpeza-saida.json',
                '../../evidencias/ciclo-estruturas/manifesto.json','../../relatorios/simbolos-originais.json'):
        refs.append(dict(path=rel,sha256=hashlib.sha256((PASTA/rel).read_bytes()).hexdigest()))
    antigo = refs[1]
    r = dict(sha256_exe=HASH,sha256_sbl=catalogo['sha256_sbl'],
             scope='Actual CalculTroupe through supported request and existing cleanup; no terrain/AI/audio result substituted',
             captures=[dict(start=hex(inicio),end_exclusive=hex(fim),bytes_hex=codigo.hex(),
                            sha256=hashlib.sha256(codigo).hexdigest(),listing=arquivo)],
             committed_evidence=refs,request_composition_implementation='7fe62277516d4ebac77f1e862cb4a9b8f36f3b2b',
             cleanup_implementation='3a7ac12a4906553b73b84037a17f51c0c552cf88',
             native_entry='0x4259e6',first_terrain_query=dict(checkpoint='0x42110c',callee='0x41aee2',symbol='BatimentGetCase'),
             first_unit_message=dict(checkpoint='0x4211d3',callee='0x4829c8',message=70),
             reset_import_checkpoints=['0x421097','0x42116e'],
             fixture_contract='Distinct existing remaining unit; count/capacity discrepancies are explicit raw-state cases',
             native_execution='Actual core preserved-state minimap resumptions; no CALL/RET/algorithm replacement')
    (PASTA/'evidencias/producao-limpa.json').write_text(json.dumps(r,indent=2)+'\n')
    errata = dict(scope='Original-symbol naming correction only; predecessor evidence remains byte-identical',
                  sha256_sbl=catalogo['sha256_sbl'],predecessor=antigo,
                  symbol_catalog=refs[3],address='0x41aee2',incorrect_informal_label='BatimentGetPosition',
                  original_symbol=simbolo,checkpoint='0x42110c',
                  effect='Address, captured code, stop and reconstructed behavior are unchanged')
    (PASTA/'evidencias/limpeza-saida-symbol-erratum.json').write_text(json.dumps(errata,indent=2)+'\n')
    print('Captured joined cleanup evidence and identity-linked BatimentGetCase naming erratum.')


if __name__=='__main__':main()
