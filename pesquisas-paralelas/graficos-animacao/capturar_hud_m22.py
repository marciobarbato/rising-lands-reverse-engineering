"""Native capture of the AffGame tail after the HUD checkpoint 0x417B1C (bottom strip and cursor), M2.2 sequence.

Original only; no translation is imported.  The -v2 display scenario (Missions' bench) runs through MissionLoad, the
load tail and N frames.  At the entry of AffGame in every ``between_frames(k)`` the state is saved and the intact
AffGame runs natively to the checkpoint 0x417B1C, then on to 0x417D30 (the DDUnlockSurface call that ends the drawing
on the offscreen surface), with hooks that only record:

* the ordered entries of every named routine reached after the checkpoint, with EAX/EDX/EBX/ECX, the four stack words
  above the return address and the return address;
* the offscreen surface hash at each call boundary of the AffGame tail (``SEGMENTOS``);
* every DGROUP+.bss byte read before written (address, value, reading routine) and the arena bytes read before written
  (ranges and readers; values kept except for blitter reads of bank sprite data);
* every byte written to DGROUP+.bss or the arena (old and new value), and the offscreen pixels written (even when the
  value does not change), with the checkpoint and end values of exactly those pixels.

The exact entry state is then restored and the real AffGame continues; the phase-end surface hash is compared with
Missions' recorded hash, and with the native end-of-drawing surface of this capture.

    python3 -B pesquisas-paralelas/graficos-animacao/capturar_hud_m22.py --quadros 128 \
        --saida pesquisas-paralelas/graficos-animacao/evidencias/captura-hud-m22-v2.json
"""
import argparse, base64, hashlib, json, struct, subprocess, sys, time, zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'missoes'))
import ambiente_missoes
import cenarios_oraculo as cen
import oraculo_quadro_missao as oq
from emulador import x86
from mapa_memoria_m1 import carregar_json

AQUI = Path(__file__).resolve().parent
CHECKPOINT = 0x417b1c
FIM = 0x417d30            # AffGame: mov eax,[0x508F70]; call DDUnlockSurface (end of offscreen drawing)
DGROUP = (0x494000, 0x523000)
CODIGO = (0x401000, 0x493bff)
# AffGame tail call boundaries (address after each call, and the cursor branch): surface hash recorded at each.
SEGMENTOS = (0x417b46, 0x417b4b, 0x417b67, 0x417b83, 0x417b88, 0x417b8f, 0x417c3c, 0x417c48, 0x417c56, 0x417c5b,
             0x417c60, 0x417c76, 0x417c84, 0x417c8f, 0x417c94, 0x417ca0, 0x417cb8, 0x417cf2, 0x417d30)
AFFCOMPTEURMATIERE, AFFMINIMAP = 0x417f38, 0x46a70c
# Frame-1 matrix (native leaf calls from the paused checkpoint state; each from the exact restored state):
# resource counters (value word 0x4E2EAC+8*(4*camera+k), highlight byte +2) and the minimap view origin 0x508720/22.
VALORES_CONTADOR = (0, 7, 10, 99, 100, 305, 999, 1000, 1234, 2047, 3999, 4999, 9999)
BRILHOS_CONTADOR = (0x00, 0x0f, 0x05, 0x0a, 0x08)
ORIGENS_MINIMAPA = ((0, 0), (2, 4), (39, 47), (20, 10), (13, 31))   # MONDE01 is 64 x 64 cells; window 25 x 17
RECORTE_CONTADORES = (480, 536, 640, 600)      # x0, y0, x1, y1 (exclusive)
RECORTE_MINIMAPA = (0, 0, 140, 140)
BLITTERS = {'PasteBobCmp', 'PasteOmbreCmp', 'PastePlayerCmp', 'PasteNoirBlancCmp', 'PasteEclairCmp'}
LARGURA, ALTURA = 800, 600
sha = lambda d: hashlib.sha256(bytes(d)).hexdigest()
codificar = lambda d: base64.b64encode(zlib.compress(bytes(d), 9)).decode()
BLOBS = {}   # sha256[:16] -> zlib+base64 payload, shared by every frame (the HUD repeats across frames)


def blob(dados):
    """Store bytes (or a JSON-serializable value) once; return its key (first 16 hex digits of the SHA-256)."""
    if not isinstance(dados, (bytes, bytearray)): dados = json.dumps(dados, separators=(',', ':')).encode()
    chave = sha(dados)[:16]
    BLOBS.setdefault(chave, codificar(dados))
    return chave


def faixas(enderecos_valores):
    """{address: (value, reader)} -> [[start_hex, bytes_hex, reader]] runs of consecutive addresses and one reader."""
    saida = []
    for a in sorted(enderecos_valores):
        v, leitor = enderecos_valores[a]
        if saida and saida[-1][0]+len(saida[-1][1]) == a and saida[-1][2] == leitor:
            saida[-1][1].append(v)
        else:
            saida.append([a, [v], leitor])
    return [[hex(a), bytes(vs).hex(), leitor] for a, vs, leitor in saida]


class Gravador:
    """Recording hooks for one AffGame tail (CHECKPOINT..FIM).  Nothing is written to emulated memory."""
    def __init__(self, b, superficie):
        self.b, self.cpu = b, b.cpu
        self.sup_base = superficie
        self.entradas, self.segmentos = [], []
        self.lidos_dg, self.lidos_arena, self.escritos = {}, {}, {}
        self.tocados = bytearray(LARGURA*ALTURA)
        self.ultimo_bloco = None
        a = b.arena
        self.arena = (a.base, a.proximo)
        dd = b.directdraw
        self.sup_mem = (dd.base_superficies, dd.base_superficies+dd.tamanho_superficies)

    def _leitor(self, cpu):
        return self.b.nome(cpu.reg_read(x86.UC_X86_REG_EIP))

    def _ler_dg(self, cpu, acesso, endereco, tamanho, valor, _):
        for a in range(endereco, endereco+tamanho):
            if a not in self.escritos and a not in self.lidos_dg:
                self.lidos_dg[a] = (cpu.mem_read(a, 1)[0], self._leitor(cpu))

    def _ler_arena(self, cpu, acesso, endereco, tamanho, valor, _):
        if self.sup_mem[0] <= endereco < self.sup_mem[1]: return
        for a in range(endereco, endereco+tamanho):
            if a not in self.escritos and a not in self.lidos_arena:
                self.lidos_arena[a] = (cpu.mem_read(a, 1)[0], self._leitor(cpu))

    def _escrever(self, cpu, acesso, endereco, tamanho, valor, _):
        if self.sup_mem[0] <= endereco < self.sup_mem[1]: return
        for a in range(endereco, endereco+tamanho):
            if a not in self.escritos:
                self.escritos[a] = cpu.mem_read(a, 1)[0]

    def _pixel(self, cpu, acesso, endereco, tamanho, valor, _):
        o = endereco-self.sup_base
        for i in range(max(0, o), min(LARGURA*ALTURA, o+tamanho)):
            self.tocados[i] = 1

    def _bloco(self, cpu, endereco, tamanho, _):
        esp = cpu.reg_read(x86.UC_X86_REG_ESP)
        if (endereco, esp) == self.ultimo_bloco: return
        self.ultimo_bloco = (endereco, esp)
        if endereco not in self.b.nomes: return
        r = lambda n: cpu.reg_read(getattr(x86, 'UC_X86_REG_'+n)) & 0xffffffff
        pilha = struct.unpack('<5I', cpu.mem_read(esp, 20))
        self.entradas.append([self.b.nomes[endereco], hex(pilha[0]), r('EAX'), r('EDX'), r('EBX'), r('ECX'), list(pilha[1:])])

    def _segmento(self, cpu, endereco, tamanho, _):
        self.segmentos.append([hex(endereco), sha(cpu.mem_read(self.sup_base, LARGURA*ALTURA))])

    def instalar(self):
        c, U = self.cpu, oq.unicorn
        self.ganchos = [
            c.hook_add(U.UC_HOOK_MEM_READ, self._ler_dg, None, begin=DGROUP[0], end=DGROUP[1]-1),
            c.hook_add(U.UC_HOOK_MEM_READ, self._ler_arena, None, begin=self.arena[0], end=self.arena[1]-1),
            c.hook_add(U.UC_HOOK_MEM_WRITE, self._escrever, None, begin=DGROUP[0], end=DGROUP[1]-1),
            c.hook_add(U.UC_HOOK_MEM_WRITE, self._escrever, None, begin=self.arena[0], end=self.arena[1]-1),
            c.hook_add(U.UC_HOOK_MEM_WRITE, self._pixel, None, begin=self.sup_base, end=self.sup_base+LARGURA*ALTURA-1),
            c.hook_add(U.UC_HOOK_BLOCK, self._bloco, None, begin=CODIGO[0], end=CODIGO[1]),
            *(c.hook_add(U.UC_HOOK_CODE, self._segmento, None, begin=a, end=a) for a in SEGMENTOS)]
        c.ctl_flush_tb()

    def remover(self):
        for g in self.ganchos: self.cpu.hook_del(g)
        self.cpu.ctl_flush_tb()

    def escritas(self):
        m = self.cpu.mem_read
        return [[hex(a), v, m(a, 1)[0]] for a, v in sorted(self.escritos.items())]

    def leituras_arena(self):
        rotina = lambda leitor: leitor.split('+')[0]
        valores = {a: v for a, v in self.lidos_arena.items() if rotina(v[1]) not in BLITTERS}
        so_faixas = {a: (0, v[1]) for a, v in self.lidos_arena.items() if rotina(v[1]) in BLITTERS}
        por_rotina = {}
        for ini, dados, leitor in faixas(so_faixas):
            por_rotina[rotina(leitor)] = por_rotina.get(rotina(leitor), 0)+len(dados)//2
        return dict(values=faixas(valores), blitter_bank_bytes=por_rotina)


def recortar(p, c):
    x0, y0, x1, y1 = c
    return b''.join(p[y*LARGURA+x0:y*LARGURA+x1] for y in range(y0, y1))


def matriz(iso, esp, base_off):
    """Leaf calls of AffCompteurMatiere and AffMiniMap from the paused checkpoint state of frame 1."""
    b, cpu = iso.b, iso.b.cpu
    dd = b.directdraw
    contexto, imagem = iso._salvar()
    sup = bytes(cpu.mem_read(dd.base_superficies, dd.tamanho_superficies))
    antes = dd.pixels('offscreen')
    camera = cpu.mem_read(0x508041, 1)[0]
    casos = []

    def chamar(nome, alvo, regs, escritas, recorte):
        iso._restaurar(contexto, imagem); cpu.mem_write(dd.base_superficies, sup)
        for a, v in escritas: cpu.mem_write(a, v)
        try:
            iso.chamar_folha(alvo, regs, esp); ok = True
        except Exception as e:
            ok = f'{type(e).__name__}: {e}'[:200]
        depois = dd.pixels('offscreen')
        fora = sum(1 for i in range(LARGURA*ALTURA) if antes[i] != depois[i]
                   and not (recorte[0] <= i % LARGURA < recorte[2] and recorte[1] <= i//LARGURA < recorte[3]))
        casos.append(dict(name=nome, routine=b.nomes[alvo], registers={k: hex(v) for k, v in regs.items()},
                          writes=[[hex(a), bytes(v).hex()] for a, v in escritas], returned=ok, crop=list(recorte),
                          crop_after=blob(recortar(depois, recorte)), changed_outside_crop=fora))
    for k, x in enumerate((0x1ec, 0x21c, 0x24c)):
        endereco = 0x4e2eac + 8*(4*camera+k)
        for v in VALORES_CONTADOR:
            for brilho in BRILHOS_CONTADOR:
                chamar(f'counter{k}_value{v}_bits{brilho:02x}', AFFCOMPTEURMATIERE, dict(EAX=x, EDX=0x22d, EBX=k, ECX=camera),
                       [(endereco, struct.pack('<H', v)), (endereco+2, bytes([brilho]))], RECORTE_CONTADORES)
    for ox, oy in ORIGENS_MINIMAPA:
        chamar(f'minimap_origin_{ox}_{oy}', AFFMINIMAP, {}, [(0x508720, struct.pack('<HH', ox, oy))], RECORTE_MINIMAPA)
    iso._restaurar(contexto, imagem); cpu.mem_write(dd.base_superficies, sup)
    return dict(camera=camera, crop_before=dict(counters=blob(recortar(antes, RECORTE_CONTADORES)),
                                               minimap=blob(recortar(antes, RECORTE_MINIMAPA))), cases=casos)


def capturar(n):
    cap = carregar_json(cen.caminho('exibicao', 'captura_quadro'))
    ni = cap['named_inputs']['m1']
    b, _, _ = cen.bancada('exibicao', ni['allocation_fill'], ni['clock_ms'][0])
    b.iniciar_relogio(); b.executar_inicio(); b.executar_mission_load(60)
    iso = oq.Isolamento(b, ('AffGame',)); iso.instalar()
    alvos = {'between_frames' if k == 1 else f'between_frames{k}' for k in range(1, n+1)}
    frames, fins, vistos = {}, {}, set()
    dd = b.directdraw
    estat = dict(dgroup_reads=0, writes=0)

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
        antes = dd.pixels('offscreen')
        base_off = next(s for s in dd.superficies.values() if s.papel == 'offscreen').base
        ganchos = [b.cpu.hook_add(oq.unicorn.UC_HOOK_CODE, b._parar_se_pedido, begin=a, end=a) for a in (CHECKPOINT, FIM)]
        b.cpu.ctl_flush_tb(); b._retomando = {entrada}
        r = oq.BancadaCargaMissaoOriginal._correr(b, 'isolated', entrada, {}, (CHECKPOINT,), retomar=True)
        assert r['EIP'] == CHECKPOINT, hex(r['EIP'])
        checkpoint = dd.pixels('offscreen')
        if not frames: estat['matrix'] = matriz(self, r['ESP'], base_off)
        g = Gravador(b, base_off); g.instalar()
        b._retomando = {CHECKPOINT}; b._passar_uma_vez.add(CHECKPOINT)
        r = oq.BancadaCargaMissaoOriginal._correr(b, 'isolated', CHECKPOINT, {}, (FIM,), retomar=True)
        g.remover()
        for h in ganchos: b.cpu.hook_del(h)
        b.cpu.ctl_flush_tb()
        fim = dd.pixels('offscreen')
        tocados = bytes(g.tocados)
        idx = [i for i in range(LARGURA*ALTURA) if tocados[i]]
        entradas = blob(g.entradas)
        representante = entradas not in vistos   # first frame with this exact HUD call sequence: keep its pixels
        vistos.add(entradas)
        linhas = sorted({i//LARGURA for i in idx})
        estat['dgroup_reads'] += len(g.lidos_dg); estat['writes'] += len(g.escritos)
        frames[fase] = dict(
            phase=fase, counter=u(0x508f7c, 4), stop=hex(r['EIP']),
            surface_before_sha256=sha(antes), checkpoint_surface_sha256=sha(checkpoint), end_surface_sha256=sha(fim),
            routines=entradas, representative=representante, segments=g.segmentos,
            dgroup_reads=blob(faixas(g.lidos_dg)), arena_reads=blob(g.leituras_arena()), writes=g.escritas(),
            touched=dict(pixels=len(idx), rows=[linhas[0], linhas[-1]] if linhas else None, mask=blob(tocados),
                         checkpoint_values_sha256=sha(bytes(checkpoint[i] for i in idx)), end_values_sha256=sha(bytes(fim[i] for i in idx)),
                         **(dict(checkpoint_values=blob(bytes(checkpoint[i] for i in idx)), end_values=blob(bytes(fim[i] for i in idx)))
                            if representante else {})),
            changed_outside_touched=[[i % LARGURA, i//LARGURA, checkpoint[i], fim[i]] for i in range(LARGURA*ALTURA)
                                     if checkpoint[i] != fim[i] and not tocados[i]])
        self._restaurar(contexto, imagem)
        for k, v in trava0.items(): dd.superficies[k].bloqueada = v
        del dd.eventos[eventos0:], b.eventos_pulados[pulos0:], b.eventos_fronteira[front0:]
        b.cpu.mem_write(dd.base_superficies, sup0)
    iso.executar = lambda regs: executar(iso, regs)
    ultimo = 'between_frames' if n == 1 else f'frame{n}'
    for fase, _ in b.executar_quadros(n):
        fins[fase] = sha(dd.pixels('offscreen'))
        if fase == ultimo: break
    return frames, fins, estat, b


def principal(a):
    t0 = time.monotonic()
    frames, fins, est, b = capturar(a.quadros)
    tabela = json.loads((AQUI/'evidencias/superficies-fase-m22-v2.json').read_text())
    gravado = {p['phase']: p['offscreen'] for p in tabela['phases']}
    linhas = []
    for k in range(1, a.quadros+1):
        fase = 'between_frames' if k == 1 else f'between_frames{k}'
        f = frames[fase]
        f['frame'] = k
        f['native_end_of_phase_sha256'] = fins.get(fase)
        f['end_hash_equals_recorded'] = fins.get(fase) == gravado.get(fase)
        f['end_of_drawing_equals_end_of_phase'] = f['end_surface_sha256'] == fins.get(fase)
        linhas.append(f)
    exe = (ambiente_missoes.CD/'INSTALHD/RISING.EXE').read_bytes()
    revisao = subprocess.run(['git', '-C', str(AQUI), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    out = dict(schema='rising-lands/affgame-hud-tail-capture/1',
               scenario='exibicao (-v2 display reference), Missions display bench',
               executable_sha256=sha(exe), code_sha256=b.sha256_codigo(),
               source_capture=tabela['source_xz'], source_capture_sha256=tabela['source_xz_sha256'],
               producing_revision=revisao, frames=a.quadros,
               command=f'python3 -B pesquisas-paralelas/graficos-animacao/capturar_hud_m22.py --quadros {a.quadros} --saida {a.saida}',
               method=('AffGame isolated at its real entry in between_frames(k); native run to 0x417B1C, then native run to 0x417D30 '
                       'with recording-only hooks (routine entries and arguments, surface hash per tail segment, DGROUP/arena '
                       'reads-before-write and writes, offscreen pixels written); exact entry state restored, the real AffGame '
                       'continues.'),
               routine_entry_format='[name, return_address, EAX, EDX, EBX, ECX, [4 stack words above the return address]]',
               touched_format='mask: 800x600 bytes (1 = written during the tail); values: checkpoint/end bytes of the written pixels in row-major order',
               blob_format='frames reference blobs by key; blobs[key] = base64(zlib(payload)); JSON payloads are compact UTF-8 JSON',
               representative=('touched checkpoint/end values are stored for the first frame of each distinct HUD call sequence '
                               '(routines blob, arguments included); every frame keeps their SHA-256'),
               matrix=est.pop('matrix'), elapsed_seconds=round(time.monotonic()-t0, 1), statistics=est, rows=linhas, blobs=BLOBS)
    Path(a.saida).write_text(json.dumps(out))
    print(json.dumps(dict(elapsed=out['elapsed_seconds'], end_hashes_equal=all(f['end_hash_equals_recorded'] for f in linhas),
                          end_of_drawing_equal=all(f['end_of_drawing_equals_end_of_phase'] for f in linhas),
                          outside=sum(len(f['changed_outside_touched']) for f in linhas), size=Path(a.saida).stat().st_size)))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--quadros', type=int, default=128)
    ap.add_argument('--saida', required=True)
    principal(ap.parse_args())
