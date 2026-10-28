"""Independent original-only reset captures before the translation exists."""
import hashlib
import json
from pathlib import Path
import struct

from capturar_colocacao_saida import preparar_saida


def preparar_remapeamento(seed=165,unidade=7):
    m = preparar_saida()
    m.busca.unidade = unidade
    m.busca.ocupada,m.busca.sucesso = seed,255-seed
    m.busca.ponteiro_rota,m.busca.concluida = seed*0x01010101,seed
    m.regioes[:] = [(i*17+seed) & 65535 for i in range(65536)]
    c = m.cores_estruturas
    c.grade[:] = bytes((i*13+seed) & 255 for i in range(65536))
    c.livres[:] = bytes((i*7+seed) & 255 for i in range(256))
    c.liberadas[:] = bytes((i*31+seed) & 255 for i in range(256))
    c.pilha[:] = [seed+i for i in range(1024)]
    return m


def resumo_original(b):
    from bancada_remapeamento_mundo import CORES
    from emulador import UNIDADES
    ler = lambda a,n: bytes(b.cpu.mem_read(a,n))
    sha = lambda a,n: hashlib.sha256(ler(a,n)).hexdigest()
    return dict(search=dict(unidade=struct.unpack('<H',ler(0x496304,2))[0],
                            ocupada=ler(0x4e0f36,1)[0],sucesso=ler(0x4e0f37,1)[0],
                            ponteiro_rota=struct.unpack('<I',ler(0x4e0f3c,4))[0],
                            concluida=ler(0x496302,1)[0]),
                colors_sha256=sha(CORES,65536),regions_sha256=sha(b.grades['regioes'],131072),
                free_hex=ler(0x4e1570,256).hex(),released_hex=ler(0x4e1670,256).hex(),
                units_sha256=sha(UNIDADES,220800),attributes_sha256=sha(b.grades['atributos'],65536),
                native_fill_calls=[list(e) for e in b.preenchimentos])


def main():
    from bancada_remapeamento_mundo import BancadaRemapeamentoMundo
    from emulador import HASH_ORIGINAL
    b = BancadaRemapeamentoMundo()
    casos = []
    for seed,unidade in ((0,0),(31,799),(165,65535),(255,7)):
        b.carregar_remapeamento(preparar_remapeamento(seed,unidade))
        regs = b.iniciar()
        args = struct.unpack('<II',b.cpu.mem_read(regs['ESP'],8))
        casos.append(dict(input=dict(seed=seed,unidade=unidade),output=resumo_original(b),
                          pending_stack_arguments=list(args)))
    report = dict(original_sha256=HASH_ORIGINAL,translation_executed=False,
                  bounded_x86_executions=b.execucoes,reached_stops=dict(b.paradas_atingidas),
                  scope='Four original pre-allocation captures; no Windows imports reached or substituted',cases=casos)
    destino = Path(__file__).resolve().parents[1]/'relatorios/capturas-remapeamento-original.json'
    destino.write_text(json.dumps(report,indent=2)+'\n')
    print(destino)


if __name__ == '__main__':
    main()
