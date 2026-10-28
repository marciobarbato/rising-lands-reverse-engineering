"""Original-only exit captures made independently of the new translation."""
import hashlib
import json
from pathlib import Path
from navegacao_unidades import MundoNavegacao
from ordens_unidades import ContextoBusca


def preparar_saida(tipo=1, dono=0, estado=14, indice=7, *, largura=16, altura=16,
                   raio=1, extra=0, classe=MundoNavegacao):
    m = classe(largura, altura)
    m.unidades[:] = b'\xa5' * 220800
    m.regioes[:] = [1]*65536
    p = indice*276
    m.unidades[p], m.unidades[p+1], m.unidades[p+2] = dono, tipo, estado
    m.unidades[p+0xbb], m.unidades[p+0xf5] = raio, extra
    m.palavra(indice, 8, 0x505)
    m.palavra(indice, 0x7c, 0x506)
    m.busca = ContextoBusca(indice, 1, 1, 0x12345678, 77)
    m.ocupar(indice, 0x505, True)
    m.ocupar(indice, 0x506, True)
    return m


def resumo_original(bancada, indice):
    from emulador import UNIDADES
    hashes = {}
    for nome in ('atributos','regioes','tiles','mini_final','mini_unidades','mini_estruturas',
                 'descoberto','luz_bordas','contagem_luz'):
        tamanho = 262144 if nome in ('descoberto','luz_bordas','contagem_luz') else 131072 if nome in ('regioes','tiles') else 65536
        hashes[nome] = hashlib.sha256(bytes(bancada.cpu.mem_read(bancada.grades[nome], tamanho))).hexdigest()
    return dict(unit_hex=bytes(bancada.cpu.mem_read(UNIDADES+indice*276, 276)).hex(),
                full_unit_pool_sha256=hashlib.sha256(bytes(bancada.cpu.mem_read(UNIDADES,220800))).hexdigest(),
                physical_sha256=hashes, native_effect_trace=bancada.efeitos)


def main():
    from bancada_colocacao_saida import BancadaColocacaoSaida
    from emulador import HASH_ORIGINAL
    b = BancadaColocacaoSaida()
    casos = []
    for tipo, dono in ((1,0), (3,0), (16,4), (1,200)):
        m = preparar_saida(tipo, dono)
        b.carregar_saida(m)
        b.colocar(7, 0x808)
        casos.append(dict(input=dict(tipo=tipo,dono=dono,indice=7,celula=0x808),output=resumo_original(b,7)))
    p = Path(__file__).resolve().parents[1]/'relatorios/capturas-colocacao-saida-original.json'
    p.write_text(json.dumps(dict(original_sha256=HASH_ORIGINAL,bounded_x86_executions=b.execucoes,
                                 translation_executed=False,cases=casos,
                                 scope='Four original-only synthetic exit captures; no Windows runtime.'),indent=2)+'\n')
    print(p)


if __name__ == '__main__':
    main()
