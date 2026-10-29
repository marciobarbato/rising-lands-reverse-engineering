"""Native reference for the pixel comparison of the AffGame composition (M3 preparation).

Original only.  The display scenario runs to the real entry of AffGame in ``between_frames`` (frame k), the entry
state is saved, and AffGame runs natively to the HUD checkpoint 0x417B1C (the end of the composed passes).  The
fixture holds the entry state the Python composition needs (every block hash-verified on load) and the offscreen
surface before and at the checkpoint, so later comparisons need no native run.

    python3 -B pesquisas-paralelas/graficos-animacao/capturar_quadro_original_pixels.py --saida DIR [--quadro 1]
        [--perturbar 0x4e19a0+...]  (named perturbations are listed in PERTURBACOES)
"""
import argparse, base64, hashlib, json, struct, sys, zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'missoes'))
import ambiente_missoes
import cenarios_oraculo as cen
import oraculo_quadro_missao as oq
from emulador import x86
from mapa_memoria_m1 import carregar_json

CHECKPOINT = 0x417b1c
# (name, pointer slot or None, absolute base, size): the entry state of the composed passes
BLOCOS = (('terreno', 0x507d70, 131072), ('objetos', 0x507d74, 65536), ('auxiliares', 0x507dac, 65536),
          ('regioes', 0x4e0f38, 131072), ('unidades', 0x4e19a0, 220800), ('projeteis', 0x5080f0, 5600),
          *((f'descoberta{i}', 0x507d78+4*i, 65536) for i in range(4)),
          *((f'iluminacao{i}', 0x507d88+4*i, 65536) for i in range(4)))
DGROUP = (0x494000, 0x523000-0x494000)
sha = lambda d: hashlib.sha256(bytes(d)).hexdigest()
codificar = lambda d: base64.b64encode(zlib.compress(bytes(d), 9)).decode()


def capturar(quadro, casos=None, recorte=None, observador=None):
    """Fixtures for AffGame in ``between_frames{quadro}``: the entry state once, then one result per case.

    ``casos``: [(name, [(address, bytes)])] byte perturbations applied to the saved entry state (default: the captured
    inputs only).  Each case restarts from the exact saved state; the full state and surface are returned for the first
    case, later cases keep their entry blocks' hashes and the checkpoint surface inside ``recorte`` (x0, y0, x1, y1).
    """
    casos = casos or [('captured_inputs', [])]
    cap = carregar_json(cen.caminho('exibicao', 'captura_quadro'))
    ni = cap['named_inputs']['m1']
    b, _, _ = cen.bancada('exibicao', ni['allocation_fill'], ni['clock_ms'][0])
    b.iniciar_relogio(); b.executar_inicio(); b.executar_mission_load(60)
    iso = oq.Isolamento(b, ('AffGame',))
    iso.instalar()
    alvo = 'between_frames' if quadro == 1 else f'between_frames{quadro}'
    resultados = []

    def executar(self, regs):
        if b.fase != alvo or resultados:
            return
        m = b.cpu.mem_read
        u = lambda a, n: int.from_bytes(m(a, n), 'little')
        contexto, imagem = self._salvar()
        dd = b.directdraw
        trava0 = {k: v.bloqueada for k, v in dd.superficies.items()}
        eventos0 = len(dd.eventos)
        sup0 = bytes(m(dd.base_superficies, dd.tamanho_superficies))
        pulos0, front0 = len(b.eventos_pulados), len(b.eventos_fronteira)
        entrada, retorno = regs['EIP'], struct.unpack('<I', m(regs['ESP'], 4))[0]
        for nome, escritas in casos:
            self._restaurar(contexto, imagem)
            for k, v in trava0.items():
                dd.superficies[k].bloqueada = v
            del dd.eventos[eventos0:], b.eventos_pulados[pulos0:], b.eventos_fronteira[front0:]
            b.cpu.mem_write(dd.base_superficies, sup0)
            for endereco, dados in escritas:
                b.cpu.mem_write(endereco, bytes(dados))
            dg = bytes(m(*DGROUP))
            blocos = {'dgroup': (DGROUP[0], dg)}
            for n, slot, tam in BLOCOS:
                base = u(slot, 4)
                blocos[n] = (base, bytes(m(base, tam)))
            pool = bytes(m(0x49a0c8, 276000))
            antes = bytes(dd.pixels('offscreen'))
            contexto2, imagem2 = self._salvar()
            habitacao = {}
            for i in range(1000):   # BatimentEstHabiter 0x41A5B8, native leaf call per occupied record, state restored
                if pool[i*276+5]:
                    r = self.chamar_folha(0x41a5b8, dict(EAX=i), regs['ESP'])
                    habitacao[i] = r['EAX'] & 0xff
                    self._restaurar(contexto2, imagem2)
            ganchos = [b.cpu.hook_add(oq.unicorn.UC_HOOK_CODE, b._parar_se_pedido, begin=CHECKPOINT, end=CHECKPOINT)]
            obs = observador(b) if observador else None
            if obs: ganchos += obs.ganchos
            b.cpu.ctl_flush_tb()
            b._retomando = {entrada}
            try:
                r = oq.BancadaCargaMissaoOriginal._correr(b, 'isolated', entrada, {}, (CHECKPOINT,), retomar=True)
                parou = hex(r['EIP'])
            except Exception as e:   # a bench stop is a named result
                parou = f'{type(e).__name__}: {e}'[:200]
            for g in ganchos:
                b.cpu.hook_del(g)
            depois = bytes(dd.pixels('offscreen'))
            resultados.append(dict(nome=nome, escritas=[(hex(a), bytes(d).hex()) for a, d in escritas], parou_em=parou,
                                   blocos=blocos, estruturas=pool, pixels_antes=antes, pixels_depois=depois,
                                   habitacao=habitacao, contador=u(0x508f7c, 4), fase=b.fase,
                                   observado=obs.resultado() if obs else None))
        self._restaurar(contexto, imagem)
        raise StopIteration
    iso.executar = lambda regs: executar(iso, regs)
    try:
        for fase, _ in b.executar_quadros(quadro):
            if resultados:
                break
    except (StopIteration, RuntimeError):
        pass
    if not resultados:
        raise SystemExit('AffGame entry not reached')
    return resultados


def recortar(pixels, caixa, largura=800):
    x0, y0, x1, y1 = caixa
    return b''.join(pixels[y*largura+x0:y*largura+x1] for y in range(y0, y1))


def gravar(saida, destino):
    fx = dict(schema='rising-lands/affgame-pixel-reference/1', stop=saida['parou_em'], phase=saida['fase'],
              counter=saida['contador'], habitation={str(k): v for k, v in saida['habitacao'].items()},
              blocks={n: dict(base=hex(b), size=len(d), sha256=sha(d), zlib_base64=codificar(d)) for n, (b, d) in saida['blocos'].items()},
              structure_pool=dict(sha256=sha(saida['estruturas']), zlib_base64=codificar(saida['estruturas'])),
              surface_before=dict(sha256=sha(saida['pixels_antes']), zlib_base64=codificar(saida['pixels_antes'])),
              surface_at_checkpoint=dict(sha256=sha(saida['pixels_depois']), zlib_base64=codificar(saida['pixels_depois'])))
    return fx


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--quadro', type=int, default=1)
    ap.add_argument('--modos', action='store_true', help='also capture the Santuario in structure modes 0..7')
    a = ap.parse_args()
    Path(a.saida).mkdir(parents=True, exist_ok=True)
    casos = [('captured_inputs', [])]
    if a.modos:   # the Santuario record (pool index 0) in every structure mode
        casos += [(f'santuario_mode_{k}', [(0x49a0c8+5, bytes([k]))]) for k in range(8)]
    rs = capturar(a.quadro, casos)
    fx = gravar(rs[0], a.saida)
    out = Path(a.saida)/f'quadro{a.quadro}.json'
    out.write_text(json.dumps(fx))
    caixa = (256, 120, 480, 300)
    extra = dict(schema='rising-lands/affgame-pixel-modes/1', box=list(caixa), cases={})
    for r in rs[1:]:
        recorte = recortar(r['pixels_depois'], caixa)
        extra['cases'][r['nome']] = dict(writes=r['escritas'], stop=r['parou_em'], habitation={str(k): v for k, v in r['habitacao'].items()},
                                         surface_sha256=sha(r['pixels_depois']), crop_sha256=sha(recorte), crop_zlib_base64=codificar(recorte),
                                         pixels_changed_vs_base=sum(1 for x, y in zip(r['pixels_depois'], rs[0]['pixels_depois']) if x != y))
    if a.modos:
        (Path(a.saida)/f'quadro{a.quadro}-modos.json').write_text(json.dumps(extra))
    print(out, out.stat().st_size, rs[0]['parou_em'], rs[0]['fase'], rs[0]['contador'], fx['surface_at_checkpoint']['sha256'][:12],
          {k: v['pixels_changed_vs_base'] for k, v in extra['cases'].items()})
