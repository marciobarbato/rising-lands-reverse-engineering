"""Extrai símbolos originais e o grafo de instruções da IA para relatórios JSON."""
import hashlib
import json
from dataclasses import asdict
from pathlib import Path
from simbolos_ia import ler_sbl, enderecar_simbolos, ler_rul

RAIZ = Path(__file__).resolve().parents[1]


def main():
    cd = RAIZ.parent / 'source/cd/INSTALHD'
    exe = (cd / 'RISING.EXE').read_bytes()
    hash_exe = hashlib.sha256(exe).hexdigest()
    if hash_exe != '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb':
        raise ValueError('Executável não corresponde à âncora estudada')
    sbl, rul = (cd / 'RISING.SBL').read_bytes(), (cd / 'RISING.RUL').read_bytes()
    simbolos = ler_sbl(sbl)
    base, enderecos = enderecar_simbolos(simbolos)
    programa = ler_rul(rul)
    operacoes = sorted({i.operacao for i in programa.instrucoes if isinstance(i.operacao, str)})
    ausentes = [n for n in operacoes if n not in enderecos and n != 'NULL']
    if ausentes:
        raise ValueError('Operações não resolvidas: ' + repr(ausentes))
    resultados = {
        'fontes-ia.json': [dict(arquivo=n, tamanho=len(d), sha256=hashlib.sha256(d).hexdigest())
                           for n,d in [('RISING.EXE', exe), ('RISING.SBL', sbl), ('RISING.RUL', rul)]],
        'simbolos-originais.json': dict(sha256_sbl=hashlib.sha256(sbl).hexdigest(), base=hex(base),
            quantidade=len(simbolos), simbolos=[dict(nome_original=s.nome, deslocamento=hex(s.deslocamento),
                                                    endereco=hex(base+s.deslocamento)) for s in simbolos]),
        'regras-ia.json': dict(sha256_rul=hashlib.sha256(rul).hexdigest(), campo_04=programa.campo_04,
            tamanho_strings=programa.tamanho_strings, entradas=programa.entradas,
            quantidade_instrucoes=len(programa.instrucoes), quantidade_operacoes=len(operacoes),
            operacoes=[dict(nome_original=n, endereco=hex(enderecos[n]) if n in enderecos else None,
                           ocorrencias=[i for i, op in enumerate(programa.instrucoes) if op.operacao == n]) for n in operacoes],
            instrucoes=[dict(indice=i, **asdict(op)) for i, op in enumerate(programa.instrucoes)]),
    }
    for nome, dados in resultados.items():
        (RAIZ / 'relatorios' / nome).write_text(json.dumps(dados, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (RAIZ / 'relatorios/simbolos-originais.tsv').write_text(
        'endereco\tnome_original\n' + ''.join(f'{base+s.deslocamento:08x}\t{s.nome}\n' for s in simbolos), encoding='utf-8')
    print(f'{len(simbolos)} símbolos; {len(programa.instrucoes)} instruções; {len(operacoes)} operações resolvidas.')


if __name__ == '__main__':
    main()
