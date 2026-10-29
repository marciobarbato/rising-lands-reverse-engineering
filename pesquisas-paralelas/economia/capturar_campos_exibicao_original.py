"""Original-only isolated captures over the display post-load state: field growth and BagVide.

Input: the M2 reference post-load state, Missions' display-scenario MissionLoad
capture (``captura-carga-missao-exibicao.json``, delta-encoded) expanded over
its entry snapshot; its summary must equal the display frame capture's S0. It
is the snapshot at MissionLoad's return, NOT a frame input: the frame
counter, the field row/flag/period, the RNG and every grid or Bag override
below are declared inputs. The frame oracle stops at frame 1, so field growth
(UpdateChamp's fields are in MONDE01 rows 32..61) is only reachable this way.

Routines: SetUpdateChamp 0x475328 (flag 0x509952 when counter 0x508f7c is a
multiple of period u16 0x4973ea, 128 in MONDE01), UpdateChamp 0x478806 (one
row 0x4973e8 per call; calls ScanNouvellePatate 0x478319, NouvellePatate
inlined, and Random 0x4704dc on 0x497164; reads the type grid [0x507d74], the
attribute grid [0x507da8] and the u16 tile grid [0x507d70], writes only the
type grid and the scalars) and BagVide 0x4470b9. Original code runs unpatched
over the whole code section (``capturar_quadro_m2_original.Captura``); no
reconstructed routine is imported.

    python3 -B pesquisas-paralelas/economia/capturar_campos_exibicao_original.py \
        --output pesquisas-paralelas/economia/evidencias/captura-campos-exibicao-original.json
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys

import capturar_quadro_m2_original as base

RAIZ = base.RAIZ
MISSOES = RAIZ / 'pesquisas-paralelas/missoes'
SET_UPDATE_CHAMP, UPDATE_CHAMP, BAG_VIDE = 0x475328, 0x478806, 0x4470b9
CONTADOR, PERIODO, LINHA, FLAG, ALEATORIO = 0x508f7c, 0x4973ea, 0x4973e8, 0x509952, 0x497164
TIPOS, ATRIBUTOS, MOSAICOS = 0x507d74, 0x507da8, 0x507d70
# Declared edge-row content: every field stage 0x1d..0x34, the bush 0x1c and the types just outside.
TIPOS_BORDA = (0x00, 0x1b, 0x1c, *range(0x1d, 0x35), 0x35, 0x42, 0xff)
# Tile words around ScanNouvellePatate's accepted ranges 0x84..0x86 and 0x9d..0xdc (u16 compare).
MOSAICOS_BORDA = (0x83, 0x84, 0x85, 0x86, 0x87, 0x9c, 0x9d, 0xc0, 0xdc, 0xdd, 0x184, 0x0000, 0x9d00)
SEMENTES = (0x00000001, 0x12345678, 0x7ffffffe, 0x2b5e0c3a, 0x5d1f00c7, 0x6a09e667)
LINHAS_BORDA = (0, 1, 2, 100, 254, 255)


def blocos_exibicao():
    """(name, base, bytes) of the display post-load state, in the capture's block order."""
    caminho = list(sys.path)
    sys.path.insert(0, str(MISSOES))
    try:
        import cenarios_oraculo as cen
        from mapa_memoria_m1 import carregar_blocos, carregar_json, expandir_captura
    finally:
        sys.path[:] = caminho
    captura = expandir_captura(carregar_json(cen.caminho('exibicao', 'captura_m1')),
                               carregar_json(cen.caminho('exibicao', 'entrada')))
    final = captura['oracle']['final_state']
    quadro = carregar_json(cen.caminho('exibicao', 'captura_quadro'))
    if final['summary'] != quadro['state_s0']['summary']:
        raise ValueError('Display MissionLoad final state is not the frame capture S0')
    blocos = [(nome, b, dados) for nome, (b, dados) in carregar_blocos(final['blocks']).items()]
    return blocos, final['summary'], [cen.caminho('exibicao', k) for k in ('captura_m1', 'entrada', 'captura_quadro')]


class CapturaExibicao(base.Captura):
    """``base.Captura`` over a given block list instead of the M1 snapshot (same bench, same hooks)."""
    def __init__(self, blocos):
        sys.path.insert(0, str(RAIZ / 'ferramentas'))
        from emulador import BancadaX86, RETORNO, PILHA, unicorn, x86
        self.RETORNO, self.PILHA, self.x86, self.unicorn = RETORNO, PILHA, x86, unicorn
        self.b = BancadaX86()
        self.blocos = blocos
        paginas = set()
        for nome, inicio, raw in self.blocos:
            if nome == 'dgroup':
                continue
            paginas.update(range(inicio & ~0xfff, (inicio + len(raw) + 0xfff) & ~0xfff, 0x1000))
        for p in sorted(paginas):
            self.b.cpu.mem_map(p, 0x1000)
        self.codigo = list(self.b.vinculos_declarados.codigo_protegido)
        self.escritas = []
        self.b.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, self._observar)
        self.b.cpu.ctl_flush_tb()


def u16(v):
    return struct.pack('<H', v & 0xffff)


def u32(v):
    return struct.pack('<I', v & 0xffffffff)


def quadro_campos(k):
    return [('contador', k), ('chamar', 'SetUpdateChamp', SET_UPDATE_CHAMP, {}),
            ('chamar', 'UpdateChamp', UPDATE_CHAMP, {})]


def linha_borda(c, linha):
    """Overrides that fill row ``linha`` and its two linear neighbours (u16 wrap) with the edge patterns."""
    tipos, atributos, mosaicos = (struct.unpack('<I', c.ler(g, 4))[0] for g in (TIPOS, ATRIBUTOS, MOSAICOS))
    overrides = []
    for deslocamento, r in ((-1, (linha - 1) % 256), (0, linha), (1, (linha + 1) % 256)):
        celulas = range(r * 256, r * 256 + 256)
        if deslocamento == 0:
            t = bytes(TIPOS_BORDA[x % len(TIPOS_BORDA)] for x in range(256))
        else:
            # Neighbour rows: mostly empty (plantable), some occupied, so priority order is visible.
            t = bytes(0 if (x + deslocamento) % 3 else 0x1d for x in range(256))
        overrides.append((tipos + celulas[0], t))
        overrides.append((atributos + celulas[0], bytes((x * 7 + r) & 3 for x in range(256))))
        overrides.append((mosaicos + 2 * celulas[0],
                          b''.join(u16(MOSAICOS_BORDA[(x + r) % len(MOSAICOS_BORDA)]) for x in range(256))))
    return overrides


def cenarios(c):
    """(name, description, overrides, steps); addresses are read from the loaded display state."""
    c.recarregar()
    saida = []
    passos = [p for k in range(128, 128 + 258) for p in quadro_campos(k)]
    saida.append(('pass_from_128', 'MONDE01 fields as loaded: counter 128..385, one SetUpdateChamp + UpdateChamp '
                  'per frame (a full 255-row pass, the idle frame after it, and the restart at 384)', [], passos))
    passos = [p for k in range(0, 64) for p in quadro_campos(k)]
    saida.append(('pass_from_0', 'MONDE01 as loaded, counter 0..63 (frame 0 starts a pass; field rows 32..61)',
                  [], passos))
    agenda = []
    for periodo in (128, 1, 3, 0x8000, 0xffff):
        for contador in (0, 1, 127, 128, 129, 255, 256, 0x7fffff80, 0xffffff80, 0xffffffff):
            agenda += [('escrever', PERIODO, u16(periodo)), ('escrever', FLAG, b'\x00'),
                       ('contador', contador), ('chamar', f'SetUpdateChamp:p{periodo:#x}:c{contador:#x}',
                                                SET_UPDATE_CHAMP, {})]
    agenda += [('escrever', PERIODO, u16(128)), ('escrever', FLAG, b'\x01'), ('contador', 5),
               ('chamar', 'SetUpdateChamp:flag_kept', SET_UPDATE_CHAMP, {})]
    saida.append(('schedule_edges', 'SetUpdateChamp over declared periods and counters; the flag is never cleared',
                  [], agenda))
    for estado, linha, flag in (('idle', 1, 0), ('in_progress', 5, 0), ('end_of_pass', 255, 1), ('row0', 0, 1)):
        saida.append((f'flag_{estado}', f'UpdateChamp with row {linha}, flag {flag} (MONDE01 grids)',
                      [(LINHA, u16(linha)), (FLAG, bytes([flag]))],
                      [('chamar', 'UpdateChamp', UPDATE_CHAMP, {})]))
    for linha in LINHAS_BORDA:
        for semente in SEMENTES:
            saida.append((f'edge_row{linha}_seed{semente:#x}',
                          f'UpdateChamp on declared edge row {linha} (all field stages, tile and attribute edges, '
                          f'u16-wrapped neighbours), RNG {semente:#x}',
                          linha_borda(c, linha) + [(LINHA, u16(linha)), (FLAG, b'\x01'), (ALEATORIO, u32(semente))],
                          [('chamar', 'UpdateChamp', UPDATE_CHAMP, {})]))
    # Same edge row three times in a row: stages advance on already-modified cells.
    saida.append(('edge_row100_three_calls', 'UpdateChamp on edge row 100, then rows 101 and 102 as left by it',
                  linha_borda(c, 100) + [(LINHA, u16(100)), (FLAG, b'\x01'), (ALEATORIO, u32(SEMENTES[1]))],
                  [('chamar', 'UpdateChamp', UPDATE_CHAMP, {})] * 3))
    pool = struct.unpack('<I', c.ler(0x4e19a0, 4))[0]
    bolsas = (pool + 0xf22, pool + 0xe0e, pool + 0xcfa, 0x49a0d4)   # the three AffGame unit Bags, structure 0's
    vazia = []
    for bolsa in bolsas:
        for contagem in (0, 1, 2, 0xff, 0x100, 0x101, 0x8000, 0xffff):
            vazia += [('escrever', bolsa, u16(contagem)),
                      ('chamar', f'BagVide:{bolsa:#x}:{contagem:#x}', BAG_VIDE, {'EAX': bolsa})]
    saida.append(('bagvide_counts', 'BagVide on the display unit Bags and structure 0 Bag with declared counts',
                  [], vazia))
    return saida


def capturar(destino):
    destino = Path(destino)
    if destino.exists():
        raise FileExistsError('Preserve existing capture; choose a new output')
    original = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(original).hexdigest() != base.HASH_EXE:
        raise ValueError('Not the intact executable')
    blocos, resumo, entradas = blocos_exibicao()
    c = CapturaExibicao(blocos)
    resultados = [base.cenario(c, *x) for x in cenarios(c)]
    chamadas = [k for r in resultados for k in r['calls']]
    arquivos = [Path(__file__), Path(base.__file__), RAIZ / 'ferramentas/emulador.py']
    saida = dict(
        schema='rising-lands/economy-display-fields-original-capture/1', sha256_exe=base.HASH_EXE,
        input=dict(paths=[str(p.relative_to(RAIZ)) for p in entradas],
                   input_sha256=[hashlib.sha256(p.read_bytes()).hexdigest() for p in entradas], state_summary=resumo,
                   label='display-scenario post-load state (MissionLoad return); NOT a frame input'),
        source_commit=subprocess.check_output(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], text=True).strip(),
        source_files=[dict(path=str(p.relative_to(RAIZ)), sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                      for p in arquivos],
        captured_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        x87_control_word=hex(base.CONTROLE_X87), translation_executed=False,
        allowed_original_intervals=[[hex(a), hex(b)] for a, b in c.codigo],
        stops={hex(a): n for a, n in base.PARADAS.items()},
        scenarios=len(resultados), original_entries=len(chamadas),
        returns=sum(k['outcome'] == 'return' for k in chamadas),
        dependency_stops=sum(k['outcome'] == 'stop' for k in chamadas),
        captures=resultados)
    destino.write_text(json.dumps(saida, separators=(',', ':')) + '\n')
    print(f"Captured original-only: {saida['scenarios']} scenarios, {saida['original_entries']} entries, "
          f"{saida['returns']} returns, {saida['dependency_stops']} dependency stops; translation_executed=False.")


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', required=True)
    capturar(p.parse_args().output)
