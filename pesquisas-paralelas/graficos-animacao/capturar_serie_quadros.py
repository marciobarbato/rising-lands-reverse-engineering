"""Native surfaces of the M2.2 sequence start and the chain-render verification (render API 1.2).

Original only for the native side.  The -v2 display scenario runs through MissionLoad, the load tail and N frames.  At the
entry of AffGame in every ``between_frames(k)`` the state is saved and AffGame runs natively to the HUD checkpoint
0x417B1C (state restored, the real run continues).  Written:

* the INITIAL SURFACE artifact: the offscreen surface at the entry of the first drawing phase (after the load tail),
  with its SHA-256, which must equal the capture's recorded ``load_tail`` surface hash;
* per frame: the native end-of-phase surface hash (compared with Missions' recorded hash), the native checkpoint
  surface hash, and the Python composition (``render_quadro.renderizar_quadro``) over (a) the native previous surface and
  (b) the chained Python output of the previous frame, with pixel-difference counts and the first stop.

    python3 -B pesquisas-paralelas/graficos-animacao/capturar_serie_quadros.py --quadros 12 \
        --superficie evidencias/superficie-inicial-m22-v2.json --verificacao evidencias/verificacao-cadeia-m22-v2.json
"""
import argparse, base64, hashlib, json, struct, subprocess, sys, zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'missoes'))
import ambiente_missoes
import cenarios_oraculo as cen
import oraculo_quadro_missao as oq
import capturar_quadro_original_pixels as cq
sys.path.insert(0, str(Path(__file__).resolve().parent))   # graphics modules win over same-named economy/missions ones
import render_quadro as RQ
from ciclo_cache_terreno import blocos_banco_cache
from graficos import Catalogo
from mapa_memoria_m1 import carregar_json

AQUI = Path(__file__).resolve().parent
sha = lambda d: hashlib.sha256(bytes(d)).hexdigest()


class Memoria:
    """MemoriaDeclarada read contract over captured blocks."""
    def __init__(self, blocos):
        self.seg = [(b, d) for b, d in blocos.values()]

    def ler_mundo(self, a, n):
        for base, d in self.seg:
            if base <= a and a+n <= base+len(d): return bytes(d[a-base:a-base+n])
        raise KeyError(hex(a))

    def u8(self, a): return self.ler_mundo(a, 1)[0]
    def u16(self, a): return struct.unpack('<H', self.ler_mundo(a, 2))[0]
    def u32(self, a): return struct.unpack('<I', self.ler_mundo(a, 4))[0]


def capturar_serie(n):
    cap = carregar_json(cen.caminho('exibicao', 'captura_quadro'))
    ni = cap['named_inputs']['m1']
    b, _, _ = cen.bancada('exibicao', ni['allocation_fill'], ni['clock_ms'][0])
    b.iniciar_relogio(); b.executar_inicio(); b.executar_mission_load(60)
    iso = oq.Isolamento(b, ('AffGame',)); iso.instalar()
    alvos = {'between_frames' if k == 1 else f'between_frames{k}' for k in range(1, n+1)}
    frames, fins = {}, {}
    finais = capturar_serie.finais = {}   # native end-of-phase surfaces of the drawing phases
    dd = b.directdraw

    def executar(self, regs):
        fase = b.fase
        if fase not in alvos or fase in frames: return
        m = b.cpu.mem_read
        u = lambda a, c: int.from_bytes(m(a, c), 'little')
        contexto, imagem = self._salvar()
        trava0 = {k: v.bloqueada for k, v in dd.superficies.items()}
        eventos0 = len(dd.eventos)
        sup0 = bytes(m(dd.base_superficies, dd.tamanho_superficies))
        pulos0, front0 = len(b.eventos_pulados), len(b.eventos_fronteira)
        entrada = regs['EIP']
        blocos = {'dgroup': (cq.DGROUP[0], bytes(m(*cq.DGROUP)))}
        for nome, slot, tam in cq.BLOCOS:
            base = u(slot, 4); blocos[nome] = (base, bytes(m(base, tam)))
        for ini, fim, nome in RQ.regioes_necessarias(Memoria(blocos), hud=True)[1+len(cq.BLOCOS):]:
            blocos[nome] = (ini, bytes(m(ini, fim-ini)))   # HUD tail buffers (render API 1.4): minimap, player table
        pool = blocos['dgroup'][1][0x49a0c8-cq.DGROUP[0]:0x49a0c8-cq.DGROUP[0]+276000]
        habitacao = {}
        for i in range(1000):
            if pool[i*276+5]:
                habitacao[i] = self.chamar_folha(0x41a5b8, dict(EAX=i), regs['ESP'])['EAX'] & 0xff
                self._restaurar(contexto, imagem)
        antes = bytes(dd.pixels('offscreen'))
        keys = bytes(m(u(0x49a050, 4), 1024))
        payloads = b''.join(bytes(imagem[f'alloc{2196+2*i:05d}'][1]) for i in range(256))
        cache_nativo = (keys, payloads, u(0x49a04e, 2))
        ganchos = [b.cpu.hook_add(oq.unicorn.UC_HOOK_CODE, b._parar_se_pedido, begin=cq.CHECKPOINT, end=cq.CHECKPOINT)]
        b.cpu.ctl_flush_tb(); b._retomando = {entrada}
        r = oq.BancadaCargaMissaoOriginal._correr(b, 'isolated', entrada, {}, (cq.CHECKPOINT,), retomar=True)
        for g in ganchos: b.cpu.hook_del(g)
        frames[fase] = dict(cache=cache_nativo, blocos=blocos, habitacao=habitacao, antes=antes, checkpoint=bytes(dd.pixels('offscreen')),
                            parou_em=hex(r['EIP']), contador=u(0x508f7c, 4))
        self._restaurar(contexto, imagem)
        for k, v in trava0.items(): dd.superficies[k].bloqueada = v
        del dd.eventos[eventos0:], b.eventos_pulados[pulos0:], b.eventos_fronteira[front0:]
        b.cpu.mem_write(dd.base_superficies, sup0)
    iso.executar = lambda regs: executar(iso, regs)
    fins['load_tail'] = None
    for fase, _ in b.executar_quadros(n):
        fins[fase] = sha(dd.pixels('offscreen'))
        if fase.startswith('between_frames'): finais[fase] = dd.pixels('offscreen')
        if fase == ('between_frames' if n == 1 else f'frame{n}'): break
    return frames, fins


def principal(args):
    frames, fins = capturar_serie(args.quadros)
    tabela = json.loads((AQUI/'evidencias/superficies-fase-m22-v2.json').read_text())
    gravado = {p['phase']: p['offscreen'] for p in tabela['phases']}
    primeiro = frames['between_frames']
    inicial = primeiro['antes']
    revisao = subprocess.run(['git', '-C', str(AQUI), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    artefato = dict(schema='rising-lands/m22-initial-surface/1', scenario='exibicao (-v2 display reference)',
        phase='entry of AffGame in between_frames, after the load tail (RestoreAll, MenuInit tail)', width=800, height=600,
        format='palette indices, row-major, origin top-left, pitch 800', sha256=sha(inicial),
        recorded_load_tail_surface_sha256=gravado['load_tail'], equals_recorded_load_tail_hash=sha(inicial) == gravado['load_tail'],
        source_capture=tabela['source_xz'], source_capture_sha256=tabela['source_xz_sha256'], producing_revision=revisao,
        command=f'python3 -B pesquisas-paralelas/graficos-animacao/capturar_serie_quadros.py --quadros {args.quadros}',
        pixels_zlib_base64=base64.b64encode(zlib.compress(inicial, 9)).decode())
    Path(args.superficie).write_text(json.dumps(artefato))
    keys0, pay0, cur0 = primeiro['cache']
    cru = blocos_banco_cache(Catalogo())
    alterados = {i: base64.b64encode(zlib.compress(pay0[i*1056:(i+1)*1056], 9)).decode() for i in range(256) if pay0[i*1056:(i+1)*1056] != cru[i*1056:(i+1)*1056]}
    cache_art = dict(schema='rising-lands/m22-initial-terrain-cache/1', scenario=artefato['scenario'], phase=artefato['phase'],
        keys_sha256=sha(keys0), cursor=cur0, keys_zlib_base64=base64.b64encode(zlib.compress(keys0, 9)).decode(),
        base_payloads='BLOCS.CMP engine ids 1090..1345 as LoadSTRATBank reads them (ciclo_cache_terreno.blocos_banco_cache)',
        base_payloads_sha256=sha(cru), modified_slots_zlib_base64=alterados, full_payloads_sha256=sha(pay0),
        producing_revision=revisao, source_capture=tabela['source_xz'], source_capture_sha256=tabela['source_xz_sha256'])
    Path(args.cache).write_text(json.dumps(cache_art))
    cache0 = RQ.EstadoCache(*primeiro['cache'][:2], primeiro['cache'][2])
    linhas, anterior, cache_cad = [], inicial, cache0
    nativo_anterior = inicial
    primeira_parada = primeira_dif = None
    ref = 'full_surface' if args.hud else 'checkpoint'
    for k in range(1, args.quadros+1):
        fase = 'between_frames' if k == 1 else f'between_frames{k}'
        fr = frames[fase]
        mem = Memoria(fr['blocos'])
        hab = lambda i, fr=fr: bool(fr['habitacao'][i])
        nat_cache = RQ.EstadoCache(fr['cache'][0], fr['cache'][1], fr['cache'][2])
        q_nat = RQ.renderizar_quadro(mem, superficie_anterior=fr['antes'], habitado=hab, cache=nat_cache, hud=args.hud)
        q_cad = RQ.renderizar_quadro(mem, superficie_anterior=anterior, habitado=hab, cache=cache_cad, hud=args.hud)
        cp = capturar_serie.finais[fase] if args.hud else fr['checkpoint']
        def dif(p): 
            d = [i for i in range(len(cp)) if cp[i] != p[i]]
            return dict(pixels=len(d), first_row=(min(d)//800 if d else None))
        linha = dict(frame=k, phase=fase, counter=fr['contador'], native_end_of_phase_sha256=fins[fase], recorded_sha256=gravado[fase],
                     reference='native end-of-phase surface (full 800x600)' if args.hud else 'native checkpoint 0x417B1C surface',
                     chained_sha256_equals_recorded=sha(q_cad.pixels) == gravado[fase],
                     end_hash_equals_recorded=fins[fase] == gravado[fase], **{'native_'+ref+'_sha256': sha(cp)},
                     over_native_previous=dict(stop=q_nat.parada, **dif(q_nat.pixels), sha256=sha(q_nat.pixels), **{'equals_native_'+ref: q_nat.pixels == cp}),
                     chained=dict(stop=q_cad.parada, **dif(q_cad.pixels), sha256=sha(q_cad.pixels), **{'equals_native_'+ref: q_cad.pixels == cp}),
                     chain_input_equals_native_previous=anterior == fr['antes'],
                     chain_cache_equals_native_entry_cache=(cache_cad.registros == nat_cache.registros and cache_cad.proximo == nat_cache.proximo and cache_cad.blocos_crus == nat_cache.blocos_crus))
        un = Memoria(fr['blocos']).ler_mundo(Memoria(fr['blocos']).u32(0x4e19a0), 220800)
        linha['units_called'] = [(c[3], un[c[3]*276+1], un[c[3]*276+2], c[1], c[2]) for c in q_cad.chamadas if c[0] == 'AffEngin']
        linhas.append(linha)
        anterior = q_cad.pixels
        cache_cad = q_cad.cache
        if primeira_parada is None and q_cad.parada: primeira_parada = (k, q_cad.parada)
        if primeira_dif is None and not linha['chained']['equals_native_'+ref]: primeira_dif = k
    Path(args.verificacao).write_text(json.dumps(dict(schema='rising-lands/m22-chain-render-check/1', frames=args.quadros,
        render_api_version=list(RQ.VERSAO_RENDER_QUADRO), hud=args.hud, initial_surface_sha256=artefato['sha256'],
        chained_equals_recorded_count=sum(l['chained_sha256_equals_recorded'] for l in linhas),
        first_stop=dict(frame=primeira_parada[0], **primeira_parada[1]) if primeira_parada else None,
        first_chained_difference_frame=primeira_dif, rows=linhas), indent=1))
    print(json.dumps(dict(initial=artefato['sha256'][:12], equals_recorded=artefato['equals_recorded_load_tail_hash'], first_stop=primeira_parada,
                          first_diff=primeira_dif, end_hashes_equal=all(l['end_hash_equals_recorded'] for l in linhas),
                          chained_equals_recorded=sum(l['chained_sha256_equals_recorded'] for l in linhas))))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--quadros', type=int, default=12)
    ap.add_argument('--hud', action='store_true', help='render API 1.4 hud=True, compared with the full end-of-phase surface')
    ap.add_argument('--cache', required=True); ap.add_argument('--superficie', required=True); ap.add_argument('--verificacao', required=True)
    principal(ap.parse_args())
