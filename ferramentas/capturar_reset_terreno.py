"""Original-only TerrainReset/MiniMapReset/BatimentModifyMap captures before translation."""
import hashlib
import json
from pathlib import Path
import random
import struct
from navegacao_unidades import MundoNavegacao

# (entry, map width/height, minimap size, seed, structure index/origin/owner/type, DL, camera, pattern)
CASOS = (('terrain', 64, 64, (128, 128), 0x12345678, None, 0, 0, 1),
         ('terrain', 256, 256, (128, 128), 0, None, 0, 0, 2),
         ('terrain', 16, 16, (128, 128), 0xffffffff, None, 0, 0, 3),
         ('minimap', 64, 64, (128, 128), 1, None, 0, 0, 4),
         ('minimap', 64, 64, (64, 32), 1, None, 0, 0, 5),
         ('structure', 64, 64, (128, 128), 1, (7, 0x0b0c, 0, 2), 1, 0, 6),
         ('structure', 256, 256, (128, 128), 1, (999, 0xfefd, 200, 5), 0, 1, 7),
         ('structure', 256, 256, (128, 128), 1, (0, 0xff00, 3, 0), 0x80, 3, 8))


def preparar_reset(entrada, largura, altura, minimapa, semente, estrutura, ativo, camera, padrao,
                   classe=MundoNavegacao, *, visibilidade=None, unidades_minimapa=None):
    """Deterministic patterned inherited state; none of it is loaded mission data.

    visibilidade 'lit'/'discovered'/'hidden' overwrites the camera's grids;
    unidades_minimapa 0/1 clears or fills the minimap unit layer.
    """
    r = random.Random(padrao)
    m = classe(largura, altura)
    m.tamanho_minimapa = minimapa
    m.jogador_local = camera
    m.unidades[:] = b'\xa5'*220800
    m.estruturas[:] = bytes(r.randrange(256) for _ in range(276000))
    for nome in ('objetos', 'donos_objetos', 'atributos', 'mini_final', 'mini_unidades', 'mini_estruturas'):
        getattr(m, nome)[:] = r.randbytes(65536)
    for nome in ('descoberto', 'luz_bordas', 'contagem_luz'):
        for g in getattr(m, nome):
            g[:] = r.randbytes(65536)
    m.tiles[:] = [r.randrange(720) for _ in range(65536)]
    m.cores_tiles[:] = r.randbytes(702)
    m.sombra[:] = r.randbytes(256)
    m.cores_jogadores[:] = r.randbytes(32)
    if estrutura is not None:
        indice, origem, dono, tipo = estrutura
        p = indice*276
        struct.pack_into('<H', m.estruturas, p+2, origem)
        m.estruturas[p+4], m.estruturas[p+8] = dono, tipo
    if visibilidade is not None:
        descoberto, luz = dict(lit=(0, 0), discovered=(0, 0x1f), hidden=(0x1f, 0x1f))[visibilidade]
        m.descoberto[camera][:] = bytes([descoberto]) * 65536
        m.luz_bordas[camera][:] = bytes([luz]) * 65536
    if unidades_minimapa is not None:
        m.mini_unidades[:] = bytes([unidades_minimapa * 0x5b]) * 65536
    minas = bytearray(r.randbytes(80))
    aleatorio = bytearray(struct.pack('<I', semente))
    return m, minas, aleatorio


def resumo(m, minas, aleatorio, efeitos, chamadas_aleatorio, memsets):
    hashes = {}
    for nome in ('unidades', 'estruturas', 'objetos', 'donos_objetos', 'atributos', 'mini_final',
                 'mini_unidades', 'mini_estruturas', 'sombra'):
        hashes[nome] = hashlib.sha256(bytes(getattr(m, nome))).hexdigest()
    for nome in ('regioes', 'tiles'):
        hashes[nome] = hashlib.sha256(struct.pack('<65536H', *getattr(m, nome))).hexdigest()
    for nome in ('descoberto', 'luz_bordas', 'contagem_luz'):
        hashes[nome] = hashlib.sha256(b''.join(bytes(g) for g in getattr(m, nome))).hexdigest()
    return dict(buffers_sha256=hashes, mines_hex=bytes(minas).hex(), random_state_hex=bytes(aleatorio).hex(),
                random_calls=chamadas_aleatorio, memsets=[list(e) for e in memsets],
                minimap_trace=[list(e) for e in efeitos])


def resumo_original(b, m):
    from emulador import UNIDADES
    from bancada_ordens import BASE_ESTRUTURAS, OBJETOS
    leitura = dict(unidades=(UNIDADES, 220800), estruturas=(BASE_ESTRUTURAS, 276000), objetos=(OBJETOS, 65536))
    hashes = {}
    for nome in ('unidades', 'estruturas', 'objetos', 'donos_objetos', 'atributos', 'mini_final',
                 'mini_unidades', 'mini_estruturas', 'sombra'):
        endereco, tamanho = leitura.get(nome, (b.grades.get(nome), 4096 if nome == 'sombra' else 65536))
        dados = bytes(b.cpu.mem_read(endereco, tamanho))
        hashes[nome] = hashlib.sha256(dados[:256] if nome == 'sombra' else dados).hexdigest()
    for nome in ('regioes', 'tiles'):
        hashes[nome] = hashlib.sha256(bytes(b.cpu.mem_read(b.grades[nome], 131072))).hexdigest()
    for nome in ('descoberto', 'luz_bordas', 'contagem_luz'):
        hashes[nome] = hashlib.sha256(bytes(b.cpu.mem_read(b.grades[nome], 262144))).hexdigest()
    minas, aleatorio = b.ler_reset()
    return dict(buffers_sha256=hashes, mines_hex=minas.hex(), random_state_hex=aleatorio.hex(),
                random_calls=b.chamadas_aleatorio, memsets=[list(e) for e in b.memsets],
                minimap_trace=[list(e) for e in b.efeitos])


def executar_nativo(b, entrada, estrutura, ativo):
    if entrada == 'terrain':
        return b.resetar_terreno()
    if entrada == 'minimap':
        return b.resetar_minimapa()
    return b.modificar_minimapa_estrutura(estrutura[0], ativo)


def main():
    from bancada_reset_terreno import BancadaResetTerreno
    from emulador import HASH_ORIGINAL
    b = BancadaResetTerreno()
    casos = []
    for caso in CASOS:
        m, minas, aleatorio = preparar_reset(*caso)
        b.carregar_reset(m, minas, aleatorio)
        regs = executar_nativo(b, caso[0], caso[5], caso[6])
        entrada, largura, altura, minimapa, semente, estrutura, ativo, camera, padrao = caso
        casos.append(dict(input=dict(entry=entrada, width=largura, height=altura, minimap=list(minimapa),
                                     seed=semente, structure=list(estrutura) if estrutura else None, dl=ativo,
                                     camera=camera, pattern=padrao),
                          returned_eip=hex(regs['EIP']), output=resumo_original(b, m)))
    p = Path(__file__).resolve().parents[1]/'relatorios/capturas-reset-terreno-original.json'
    p.write_text(json.dumps(dict(original_sha256=HASH_ORIGINAL, translation_executed=False,
                                 original_entries=dict(b.entradas_originais), bounded_segments=b.execucoes,
                                 preserved_loop_head_resumptions=b.retomadas_laco,
                                 preserved_minimap_resumptions=b.retomadas_minimapa,
                                 maximum_native_instructions_per_segment=b.maximo_instrucoes, cases=casos,
                                 scope='Original-only TerrainReset, MiniMapReset and BatimentModifyMap (DL 1, 0, '
                                       '0x80) over deterministic synthetic inherited layers; no mission data, no '
                                       'caller orchestration, no Windows runtime.'), indent=1)+'\n')
    print(p, 'cases', len(casos), 'segments', b.execucoes, 'loop resumes', b.retomadas_laco,
          'max instructions', b.maximo_instrucoes)


if __name__ == '__main__':
    main()
