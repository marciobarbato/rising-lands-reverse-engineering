"""Static byte provenance of the HUD tail translation (hud_quadro.py, render API 1.4).

Reads the intact executable only (no execution) and writes the SHA-256 of every original byte interval the
translation relies on, with the pinned native capture hash.

    python3 -B pesquisas-paralelas/graficos-animacao/extrair_proveniencia_hud.py \
        --saida pesquisas-paralelas/graficos-animacao/evidencias/hud-quadro.json
"""
import argparse, hashlib, json, struct
from pathlib import Path

AQUI = Path(__file__).resolve().parent
EXE = AQUI.parents[2]/'source/cd/INSTALHD/RISING.EXE'
CAPTURA = AQUI/'evidencias/captura-hud-m22-v2.json'
INTERVALOS = (
    ('AffGame HUD-mode switch table (4 slots, all 0x417B32)', 0x417688, 0x417698),
    ('AffGame tail from the HUD checkpoint through the DDUnlockSurface call', 0x417b1c, 0x417d35),
    ('AffCompteurMatiere', 0x417f38, 0x4180d8),
    ('IntToBCD', 0x467cd1, 0x467d3a),
    ('GetBit', 0x467d97, 0x467da6),
    ('AffZoneIconeAction', 0x416f29, 0x4171f8),
    ('AffTrame', 0x41721f, 0x417435),
    ('AffDrapeauAlliance', 0x417581, 0x417675),
    ('AffMarche', 0x46677d, 0x4668aa),
    ('AffMiniMap and its shared epilogue', 0x46a70c, 0x46a8a2),
    ('shared epilogue 0x46A198', 0x46a198, 0x46a19e),
    ('Box', 0x45c912, 0x45cacd),
    ('PasteBobCmp clip-window prologue', 0x45b247, 0x45b2a6),
    ('AffChrono selection test', 0x401cc6, 0x401d18),
    ('AffChrono no-selection exit', 0x40208a, 0x402094),
    ('AffZoneInfo', 0x40f758, 0x40f8aa),
    ('AffInfoAide tooltip test', 0x40f8aa, 0x40f8d3),
    ('AffDebug', 0x4408b7, 0x4408c7),
    ('EvenementEnCours', 0x4581b6, 0x4581bc),
    ('MessageBoxAffiche queue test', 0x469c44, 0x469c5f),
    ('PlayerEstAllie', 0x46d838, 0x46d877),
    ('PlayerEstContacterPourAlliance', 0x46da1e, 0x46da3b),
)


def secoes(dados):
    pe = struct.unpack_from('<I', dados, 0x3c)[0]
    n, opt = struct.unpack_from('<H', dados, pe+6)[0], struct.unpack_from('<H', dados, pe+20)[0]
    base = struct.unpack_from('<I', dados, pe+24+28)[0]
    tab = pe+24+opt
    for i in range(n):
        nome, vsize, va, rsize, raw = struct.unpack_from('<8sIIII', dados, tab+40*i)
        yield nome.rstrip(b'\0').decode(), base+va, max(vsize, rsize), raw


def ler(dados, ini, fim):
    for _, va, tam, raw in secoes(dados):
        if va <= ini and fim <= va+tam: return dados[raw+ini-va:raw+fim-va]
    raise ValueError(hex(ini))


def principal(a):
    dados = EXE.read_bytes()
    out = dict(schema='rising-lands/hud-tail-provenance/1', executable='RISING.EXE (intact, ../source/cd/INSTALHD)',
               executable_sha256=hashlib.sha256(dados).hexdigest(),
               note=('Original byte intervals the HUD tail translation (hud_quadro.py, render API 1.4) relies on; raw-offset '
                     'mapping of the section table. The behaviour is established by the native capture, committed before the '
                     'translation.'),
               intervals=[dict(name=n, start=hex(i), end_exclusive=hex(f), sha256=hashlib.sha256(ler(dados, i, f)).hexdigest())
                          for n, i, f in INTERVALOS],
               native_capture=dict(path='evidencias/captura-hud-m22-v2.json',
                                   sha256=hashlib.sha256(CAPTURA.read_bytes()).hexdigest()))
    Path(a.saida).write_text(json.dumps(out, indent=1)+'\n')
    print(json.dumps(dict(intervals=len(out['intervals']), capture=out['native_capture']['sha256'][:16])))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    principal(ap.parse_args())
