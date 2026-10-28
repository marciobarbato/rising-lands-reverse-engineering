"""Original-only discovery/light captures for vision sums 9..11, before translation."""
import hashlib
import json
from pathlib import Path
from capturar_colocacao_saida import preparar_saida, resumo_original

# (entry, map width/height, cell, BB, F5, owner, camera, light-count pattern)
CASOS = (('mission', 16, 16, 0x505, 9, 0, 0, 0, 'fresh'),
         ('mission', 256, 256, 0x0000, 10, 0, 3, 3, 'fresh'),
         ('mission', 64, 64, 63*256+32, 10, 1, 1, 1, 'mixed'),
         ('exit', 16, 16, 0x808, 10, 1, 2, 2, 'fresh'),
         ('exit', 256, 256, 0xffff, 11, 0, 0, 1, 'saturated'),
         ('discover', 256, 256, 0x8080, 13, 0, 3, 0, 'fresh'),
         ('light', 128, 64, 63*256+127, 11, 0, 2, 2, 'saturated'))


def preparar_caso(entrada, largura, altura, celula, bb, f5, dono, camera, luz, classe=None):
    extra = {} if classe is None else dict(classe=classe)
    m = preparar_saida(tipo=3, dono=dono, largura=largura, altura=altura, raio=bb, extra=f5, **extra)
    m.jogador_local = camera
    if entrada == 'mission':
        m.palavra(7, 8, celula)
    if luz == 'saturated':
        m.contagem_luz[dono][:] = b'\xff' * 65536
    elif luz == 'mixed':
        m.contagem_luz[dono][:] = bytes((0, 1, 2, 255)[c % 4] for c in range(65536))
        m.descoberto[dono][:] = bytes((31, 0, 16, 1)[(c >> 1) % 4] for c in range(65536))
    return m


def executar_nativo(bancada, entrada, celula, bb, dono):
    if entrada == 'mission':
        return bancada.colocar_missao(7)
    if entrada == 'exit':
        return bancada.colocar(7, celula)
    if entrada == 'discover':
        return bancada.descobrir(celula, bb, dono)
    return bancada.iluminar(celula, bb, dono)


def main():
    from bancada_descoberta_terreno import BancadaDescobertaTerreno
    from emulador import HASH_ORIGINAL
    b = BancadaDescobertaTerreno()
    casos = []
    for caso in CASOS:
        entrada, largura, altura, celula, bb, f5, dono, camera, luz = caso
        m = preparar_caso(*caso)
        b.carregar_saida(m)
        regs = executar_nativo(b, entrada, celula, bb, dono)
        saida = resumo_original(b, 7)
        saida['native_cell_trace_count'] = len(b.celulas)
        saida['native_cell_trace_sha256'] = hashlib.sha256(
            json.dumps([list(e) for e in b.celulas], separators=(',', ':')).encode()).hexdigest()
        casos.append(dict(input=dict(entry=entrada, width=largura, height=altura, cell=celula, bb=bb, f5=f5,
                                     owner=dono, camera=camera, light_pattern=luz),
                          returned_eip=hex(regs['EIP']), output=saida))
    p = Path(__file__).resolve().parents[1]/'relatorios/capturas-descoberta-terreno-original.json'
    p.write_text(json.dumps(dict(original_sha256=HASH_ORIGINAL, translation_executed=False,
                                 original_entries=dict(b.entradas_originais), bounded_segments=b.execucoes,
                                 preserved_minimap_resumptions=b.retomadas_minimapa,
                                 maximum_native_instructions_per_segment=b.maximo_instrucoes,
                                 cases=casos,
                                 scope='Original-only PlaceEngin/SetSortEngin vision sums 9..11 and direct '
                                       'DecouvreTerrain radius 13 / IllumineTerrain radius 11; synthetic inherited '
                                       'world, no Windows runtime, captured before the Python limit changed.'),
                            indent=1)+'\n')
    print(p, 'cases', len(casos), 'segments', b.execucoes, 'resumes', b.retomadas_minimapa,
          'max instructions', b.maximo_instrucoes)


if __name__ == '__main__':
    main()
