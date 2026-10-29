"""Native capture of the type-1 and type-8 unit bodies (AffEngin 0x41591F) in the M2.2 display sequence.

Original only; no translation is imported.  The -v2 display scenario (Missions' bench) runs through MissionLoad, the
load tail and N frames.  At the entry of AffGame in every ``between_frames(k)`` the state is saved and AffGame runs
natively to the HUD checkpoint 0x417B1C with a stop at every AffEngin entry (state restored afterwards, the real run
continues).  At each AffEngin call whose unit type is 1 or 8 (MONDE01's units 11 and 15):

* the paused state is saved and the intact AffEngin runs once more as a native leaf call with the captured inputs,
  recording every blitter call (PasteBobCmp 0x45B247, PasteOmbreCmp 0x45B796, PastePlayerCmp 0x45C455 with its
  pushed owner argument, PasteEclairCmp 0x45BA23), the ordered entries of named routines, the basic-block path inside
  AffCorpsEnginDecalage..AffAttaqueEngin (0x410FCC..0x41374C), the RNG cursor 0x4E1D18 and the offscreen surface before
  and after (a fixed crop around the cell, and the full-surface difference count/box);
* at the first call of each target unit, a perturbation matrix runs the same native call from the same paused state
  with record bytes changed (state 2/7, direction 1..16, every phase below the record's count, body shifts, life
  word values), each from the exact restored state;
* the state is restored and the real AffGame continues, so the checkpoint surface is the unperturbed original's.

    python3 -B pesquisas-paralelas/graficos-animacao/capturar_corpos_tipos1_8.py --quadros 6 \
        --saida pesquisas-paralelas/graficos-animacao/evidencias/captura-corpos-tipos1-8-m22-v2.json
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
AFFENGIN = 0x41591f
TIPOS_ALVO = (1, 8)
BLITTERS = {0x45b247: 'PasteBobCmp', 0x45b796: 'PasteOmbreCmp', 0x45c455: 'PastePlayerCmp', 0x45ba23: 'PasteEclairCmp'}
CAMINHO = (0x410fcc, 0x41374c)        # AffCorpsEnginDecalage .. AffAttaqueEngin (exclusive): body routines
CODIGO = (0x401000, 0x493bff)
RNG = 0x4e1d18
GLOBAIS = dict(camera_u8=(0x508041, 1), selecionada_unidade_u16=(0x496ac2, 2), modo_selecao_u8=(0x508f8f, 1),
               recorte_u16x4=(0x49a01c, 8), origem_u16x2=(0x508720, 4), janela_u16x2=(0x508724, 4), quadro_u32=(0x508f7c, 4),
               superficie_u32=(0x508f70, 4), pitch_u32=(0x4e17a0, 4))
MARGEM = 96                            # crop: cell origin +- 96 pixels, clamped to the 800 x 600 surface
LARGURA, ALTURA = 800, 600
sha = lambda d: hashlib.sha256(bytes(d)).hexdigest()
codificar = lambda d: base64.b64encode(zlib.compress(bytes(d), 9)).decode()
i16 = lambda v: (v & 0xffff) - 0x10000 if v & 0x8000 else v & 0xffff


def caixa(x, y):
    return (max(0, x-MARGEM), max(0, y-MARGEM), min(LARGURA, x+MARGEM), min(ALTURA, y+MARGEM))


def recortar(p, c):
    x0, y0, x1, y1 = c
    return b''.join(p[y*LARGURA+x0:y*LARGURA+x1] for y in range(y0, y1))


def diferenca(a, b):
    d = [i for i in range(len(a)) if a[i] != b[i]]
    if not d: return dict(pixels=0, box=None)
    xs, ys = [i % LARGURA for i in d], [i//LARGURA for i in d]
    return dict(pixels=len(d), box=[min(xs), min(ys), max(xs)+1, max(ys)+1])


def dentro(box, c):
    return box is None or (c[0] <= box[0] and c[1] <= box[1] and box[2] <= c[2] and box[3] <= c[3])


def perturbacoes(registro):
    """Native matrix around one real record: (name, [(offset, bytes)])."""
    casos = []
    contagem = registro[0xa5]
    for estado in (2, 7):
        for direcao in range(1, 17):
            for fase in range(contagem):
                casos.append((f'state{estado}_dir{direcao}_phase{fase}', [(2, bytes([estado])), (0x91, bytes([direcao])), (0xa4, bytes([fase]))]))
    for dx, dy in ((-6, 4), (5, -3), (12, 9)):   # body shifts +0x86/+0x87 with life 100 (no tired icon)
        casos.append((f'shift_{dx}_{dy}_life100', [(2, bytes([2])), (0x91, bytes([5])), (0xa4, bytes([2])), (0x86, struct.pack('<b', dx)),
                                                   (0x87, struct.pack('<b', dy)), (0x74, struct.pack('<H', 100))]))
    for vida in (0, 5, 99, 100, 101):            # life word +0x74: tired-icon parity/threshold
        casos.append((f'life{vida}', [(0x74, struct.pack('<H', vida))]))
    return casos


class Chamador:
    """Native leaf calls of AffEngin from the paused state at its entry, state restored before and after each."""
    def __init__(self, iso, regs):
        self.iso, self.b, self.regs = iso, iso.b, regs
        dd = self.b.directdraw
        self.dd = dd
        self.contexto, self.imagem = iso._salvar()
        self.superficie_mem = bytes(self.b.cpu.mem_read(dd.base_superficies, dd.tamanho_superficies))
        self.antes = dd.pixels('offscreen')
        self.unidade = regs['EBX'] & 0xffff
        self.base = int.from_bytes(self.b.cpu.mem_read(0x4e19a0, 4), 'little') + 276*self.unidade
        self.registro = bytes(self.b.cpu.mem_read(self.base, 276))

    def restaurar(self):
        self.iso._restaurar(self.contexto, self.imagem)
        self.b.cpu.mem_write(self.dd.base_superficies, self.superficie_mem)

    def chamar(self, escritas=(), rastrear=False):
        cpu = self.b.cpu
        self.restaurar()
        for o, dados in escritas:
            cpu.mem_write(self.base+o, bytes(dados))
        blits, rotinas, caminho = [], [], []

        def blit(c, a, t, _):
            r = lambda n: c.reg_read(getattr(x86, 'UC_X86_REG_'+n)) & 0xffffffff
            ev = dict(routine=BLITTERS[a], x=i16(r('EAX')), y=i16(r('EDX')), id=r('EBX') & 0xffff, clip=r('ECX') & 0xff)
            if a == 0x45c455:   # PastePlayerCmp: owner/table index pushed before the call (above the return address)
                ev['pushed'] = struct.unpack('<I', c.mem_read(r('ESP')+4, 4))[0]
            blits.append(ev)

        def bloco(c, a, t, _):
            if a in self.b.nomes: rotinas.append(self.b.nomes[a])
            if CAMINHO[0] <= a < CAMINHO[1] and (not caminho or caminho[-1] != a): caminho.append(a)
        ganchos = [cpu.hook_add(oq.unicorn.UC_HOOK_CODE, blit, None, begin=a, end=a) for a in BLITTERS]
        if rastrear: ganchos.append(cpu.hook_add(oq.unicorn.UC_HOOK_BLOCK, bloco, None, begin=CODIGO[0], end=CODIGO[1]))
        cpu.ctl_flush_tb()
        rng0 = cpu.mem_read(RNG, 1)[0]
        registradores = {n: self.regs[n] for n in ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')}
        self.b._passar_uma_vez.add(AFFENGIN)   # the bench's own AffEngin stop must let this call through once
        try:
            r = self.iso.chamar_folha(AFFENGIN, registradores, self.regs['ESP'])
            retorno = dict(returned=True, esp_balanced=True)
        except Exception as e:   # a bench stop is a named result, never a guess
            retorno = dict(returned=False, error=f'{type(e).__name__}: {e}'[:300])
        self.b._passar_uma_vez.discard(AFFENGIN)
        rng1 = cpu.mem_read(RNG, 1)[0]
        for g in ganchos: cpu.hook_del(g)
        cpu.ctl_flush_tb()
        depois = self.dd.pixels('offscreen')
        pool_depois = bytes(cpu.mem_read(self.base, 276))
        registro_entrada = bytearray(self.registro)
        for o, dados in escritas: registro_entrada[o:o+len(dados)] = dados
        out = dict(**retorno, blits=blits, rng_before=rng0, rng_after=rng1, record_unchanged=pool_depois == bytes(registro_entrada))
        if rastrear:
            out['record_hex'] = bytes(registro_entrada).hex()
            compacto = []   # consecutive repeats of one routine entry (per-row blit helpers) as [name, count]
            for nome in rotinas:
                if compacto and compacto[-1][0] == nome: compacto[-1][1] += 1
                else: compacto.append([nome, 1])
            out['routines'] = compacto
            out['path'] = [hex(a) for a in caminho]
        return out, depois

    def fim(self):
        self.restaurar()


def globais(b):
    m = b.cpu.mem_read
    return {n: bytes(m(a, w)).hex() for n, (a, w) in GLOBAIS.items()}


def capturar(n):
    cap = carregar_json(cen.caminho('exibicao', 'captura_quadro'))
    ni = cap['named_inputs']['m1']
    b, _, _ = cen.bancada('exibicao', ni['allocation_fill'], ni['clock_ms'][0])
    b.iniciar_relogio(); b.executar_inicio(); b.executar_mission_load(60)
    iso = oq.Isolamento(b, ('AffGame',)); iso.instalar()
    alvos = {'between_frames' if k == 1 else f'between_frames{k}' for k in range(1, n+1)}
    frames, matriz_feita, fins = {}, set(), {}
    dd = b.directdraw
    estatistica = dict(native_calls=0, matrix_calls=0)

    def executar(self, regs):
        fase = b.fase
        if fase not in alvos or fase in frames: return
        m = b.cpu.mem_read
        contexto, imagem = self._salvar()
        trava0 = {k: v.bloqueada for k, v in dd.superficies.items()}
        eventos0 = len(dd.eventos)
        sup0 = bytes(m(dd.base_superficies, dd.tamanho_superficies))
        pulos0, front0 = len(b.eventos_pulados), len(b.eventos_fronteira)
        entrada = regs['EIP']
        antes_quadro = dd.pixels('offscreen')
        ganchos = [b.cpu.hook_add(oq.unicorn.UC_HOOK_CODE, b._parar_se_pedido, begin=a, end=a) for a in (CHECKPOINT, AFFENGIN)]
        b.cpu.ctl_flush_tb(); b._retomando = {entrada}
        pc, chamadas, alvos_cap = entrada, [], []
        while True:
            r = oq.BancadaCargaMissaoOriginal._correr(b, 'isolated', pc, {}, (CHECKPOINT, AFFENGIN), retomar=True)
            if r['EIP'] != AFFENGIN: break
            unidade = r['EBX'] & 0xffff
            reg = bytes(m(int.from_bytes(m(0x4e19a0, 4), 'little')+276*unidade, 276))
            x, y = i16(r['EAX']), i16(r['EDX'])
            chamadas.append([unidade, reg[1], reg[2], x, y])
            if reg[1] in TIPOS_ALVO:
                ch = Chamador(self, r)
                c = caixa(x, y)
                real, depois = ch.chamar(rastrear=True); estatistica['native_calls'] += 1
                dif = diferenca(ch.antes, depois)
                ev = dict(unit=ch.unidade, type=reg[1], state=reg[2], owner=reg[0], x=x, y=y,
                          registers={k: hex(r[k] & 0xffffffff) for k in ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP')},
                          globals=globais(b), crop_box=list(c), crop_before_sha256=sha(recortar(ch.antes, c)),
                          crop_before_zlib_base64=codificar(recortar(ch.antes, c)), crop_after_sha256=sha(recortar(depois, c)),
                          crop_after_zlib_base64=codificar(recortar(depois, c)), surface_difference=dif,
                          difference_inside_crop=dentro(dif['box'], c), call=real)
                if ch.unidade not in matriz_feita:
                    matriz_feita.add(ch.unidade)
                    casos = []
                    for nome, escritas in perturbacoes(reg):
                        res, dep = ch.chamar(escritas); estatistica['matrix_calls'] += 1
                        d2 = diferenca(ch.antes, dep)
                        casos.append(dict(name=nome, writes=[(hex(o), bytes(v).hex()) for o, v in escritas], **res,
                                          crop_after_sha256=sha(recortar(dep, c)), surface_difference=d2,
                                          difference_inside_crop=dentro(d2['box'], c)))
                    ev['matrix'] = casos
                alvos_cap.append(ev)
                ch.fim()
            pc = AFFENGIN; b._retomando = {pc}; b._passar_uma_vez.add(pc)
        for g in ganchos: b.cpu.hook_del(g)
        b.cpu.ctl_flush_tb()
        checkpoint = dd.pixels('offscreen')
        frames[fase] = dict(phase=fase, counter=int.from_bytes(m(0x508f7c, 4), 'little'), stop=hex(r['EIP']),
                            surface_before_sha256=sha(antes_quadro), checkpoint_surface_sha256=sha(checkpoint),
                            affengin_calls=chamadas, targets=alvos_cap)
        self._restaurar(contexto, imagem)
        for k, v in trava0.items(): dd.superficies[k].bloqueada = v
        del dd.eventos[eventos0:], b.eventos_pulados[pulos0:], b.eventos_fronteira[front0:]
        b.cpu.mem_write(dd.base_superficies, sup0)
    iso.executar = lambda regs: executar(iso, regs)
    ultimo = 'between_frames' if n == 1 else f'frame{n}'
    for fase, _ in b.executar_quadros(n):
        fins[fase] = sha(dd.pixels('offscreen'))
        if fase == ultimo: break
    return frames, fins, estatistica, b


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
        linhas.append(f)
    exe = (ambiente_missoes.CD/'INSTALHD/RISING.EXE').read_bytes()
    revisao = subprocess.run(['git', '-C', str(AQUI), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    out = dict(schema='rising-lands/unit-body-types1-8-capture/1',
               scenario='exibicao (-v2 display reference), Missions display bench',
               executable_sha256=sha(exe), code_sha256=b.sha256_codigo(),
               source_capture=tabela['source_xz'], source_capture_sha256=tabela['source_xz_sha256'],
               producing_revision=revisao, frames=a.quadros,
               command=f'python3 -B pesquisas-paralelas/graficos-animacao/capturar_corpos_tipos1_8.py --quadros {a.quadros} --saida {a.saida}',
               method=('AffGame isolated at its real entry in between_frames(k); stop at each AffEngin 0x41591F entry; for unit types 1/8 '
                       'the intact AffEngin runs as a native leaf call from the paused state (blitter hooks record arguments only, '
                       'nothing is substituted); the matrix rewrites record bytes before the same call; the exact state is restored '
                       'after every call and the real AffGame continues to 0x417B1C.'),
               crop=f'cell origin +- {MARGEM} pixels clamped to 800x600; offscreen surface palette indices, row-major',
               native_calls=est['native_calls'], matrix_calls=est['matrix_calls'], elapsed_seconds=round(time.monotonic()-t0, 1),
               rows=linhas)
    Path(a.saida).write_text(json.dumps(out))
    alvo = [(f['frame'], t['unit'], t['type'], t['state'], t['x'], t['y'], t['surface_difference']['pixels'], t['call']['returned'])
            for f in linhas for t in f['targets']]
    print(json.dumps(dict(native=est, elapsed=out['elapsed_seconds'], end_hashes_equal=all(f['end_hash_equals_recorded'] for f in linhas),
                          targets=alvo, size=Path(a.saida).stat().st_size)))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--quadros', type=int, default=6)
    ap.add_argument('--saida', required=True)
    principal(ap.parse_args())
