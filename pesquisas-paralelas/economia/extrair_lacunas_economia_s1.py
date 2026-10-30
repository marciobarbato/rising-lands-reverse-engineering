"""Additive intact-executable listings for the S1 Economy gap delivery."""
import hashlib
import json
from pathlib import Path
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
sys.path.insert(0, str(RAIZ / '.local/python'))
from extrair_ordens_economia import ler_pe, HASH

NOMES = ('SacGetCapacite', 'TuyauEstSortie', 'RechercheCalculNew', 'TechnologieReset', 'InventionSetEffet',
         'TypeBatimentEstRealisable', 'SetBatimentRecrutable', 'SetTroupeRecrutable', 'RechercheGetBranche',
         'RechercheGetNiveau', 'RechercheGetEtat', 'InventionGetCout', 'IaRechercheAjuste', 'RechercheGetNbInvention',
         'SortilegeResetTechnologie', 'BonusReset', 'BatimentInitTechnologie', 'EnginSetTechnologie')


def main():
    import capstone
    catalogo = json.loads((RAIZ/'relatorios/simbolos-originais.json').read_bytes())
    simbolos = {s['nome_original']: int(s['endereco'], 16) for s in catalogo['simbolos']}
    enderecos = sorted(set(simbolos.values()))
    ler = ler_pe()
    saida = PASTA/'evidencias/lacunas-s1/listagens'
    saida.mkdir(parents=True, exist_ok=True)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    intervalos = []
    for nome in NOMES:
        a = simbolos[nome]
        z = next(e for e in enderecos if e > a)
        raw = ler(a,z-a)
        arquivo = f'{a:08x}.asm'
        (saida/arquivo).write_text(f'; {nome}; intact EXE {HASH}; exclusive end {z:#x}\n'+'\n'.join(
            f'{i.address:08x}  {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}' for i in md.disasm(raw,a))+'\n')
        intervalos.append(dict(routine=nome,start=hex(a),end_exclusive=hex(z),bytes_sha256=hashlib.sha256(raw).hexdigest(),file=arquivo))
    (saida/'manifesto.json').write_text(json.dumps(dict(original_sha256=HASH, intervals=intervalos),indent=2)+'\n')


if __name__ == '__main__':
    main()
