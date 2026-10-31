"""M3.1 whole-state proof of the input chain over Missions' pass-2 probe windows (P1: frames 129-629, P2: 129-729).

The Python chain (``composicao_entrada_ia.ComposicaoEntrada``: the pinned M2.2/M2.3 frame composition plus this
front's InputGame, WndProc, SetPlayerOrdre and ProcessInputGame, fed by the probe's scripted-input file) starts
from the window's opening state (the accepted M2.2 frame-128 state) and is compared, phase by phase, with the
window's native capture (``rising-lands/m3-probe-window-part/1``, complete deltas). Python only; the native side
is Missions' committed capture.

One command, on a clean tree (the windows run in parallel; ``--lease`` wraps each in the machine's heavy lease):

    python3 -B pesquisas-paralelas/ia-runtime/provar_entrada_janelas_ia.py tudo --janelas P1 P2 \
        [--lease <path>/heavy_lease.py] --saida pesquisas-paralelas/ia-runtime/validacao/m3-1-prova-p1-p2.json

Step by step:

    python3 -B pesquisas-paralelas/ia-runtime/provar_entrada_janelas_ia.py janela P1     # one report per window
    python3 -B pesquisas-paralelas/ia-runtime/provar_entrada_janelas_ia.py agregar --janelas P1 P2 --saida <proof>

- **Reference** (per window): the manifest (SHA-256 pinned here) pins the part's xz and raw JSON and the mask;
  the mask file pins the window policy (display roots); the part pins the scripted-input file. Every phase is
  replayed from its deltas and checked against its summary, compared summary and masked hash, and the full
  states it carries (``comparar_quadros_ia.fases_referencia``). The opening full state must match its own hashes
  and equal the M2.2 frame-128 full state.
- **Per phase**, the M2.3 method (``comparar_quadros_ia.comparar_sequencia``, imported unchanged): every state byte
  outside the window's cumulative mask, Python's compared summary, both RNGs, bindings and boundaries outside
  display context, the allocation-record count, the between-frames exit registers and the carried entry
  registers. In addition, for M3.1:
  - the consumed scripted-input answers (peek/get/translate/dispatch with the WndProc flag bytes, cursor, keys)
    against the phase's ``scripted_inputs``;
  - the SetPlayerOrdre packets and ProcessInputGame dispatches of each frame phase against the probe's committed
    ``comandos.jsonl``;
  - the explicit M3.1 fields: each player's packet pointer [0x4e2458+4p] and its 10-byte packet, the per-player
    selection areas 0x508728+512p, and the order fields +2, +0xb2, +0xb7/+0xb8, +0xbe and +0x110 of every unit
    slot of the pool [0x4e19a0], with the count of those bytes the mask would hide (must be 0).
  The first difference stops the window.
- **Reports:** one JSON per window part under ``.local/m3-1/prova-<revision>/``; ``agregar`` requires reports from
  the current clean revision, equal and covering the whole window. A proof that is not accepted goes under
  ``.local/``; it still lists, per window, how far it goes (``reach``: the parts equal from the start, the first
  stop with its routine and site, every part's own result and ``phase_chain_sha256``).

Multi-part windows (P6, S1). Each part starts from its own checkpoint (the part's opening full state, checked
against the previous part's final reference summary by ``agregar``) with the declared entry registers, message
words, cursor and saved frame words, so the parts run in parallel, one process and one heavy-lease slot each. The
frame-128 allocation records apply up to the first phase that allocates or releases a block: a part stops at the
last whole frame before it (``allocation_stop``) and ``agregar`` refuses every later part.

S1 (pass-2 capture on feat/re-missions, unpinned until it lands):

    python3 -B pesquisas-paralelas/ia-runtime/provar_entrada_janelas_ia.py fixar S1 --ref origin/feat/re-missions
    git commit pesquisas-paralelas/ia-runtime/provar_entrada_janelas_ia.py     # the pinned SHA-256 and commit
    python3 -B pesquisas-paralelas/ia-runtime/provar_entrada_janelas_ia.py tudo --janelas S1 \
        --lease <path>/heavy_lease.py --saida pesquisas-paralelas/ia-runtime/validacao/m3-1-prova-s1.json

``fixar`` checks every part, the mask, the policy and the logs in that commit and rewrites the S1 entry; the files
are then read from that commit (``git show``, cached under .local/m3-1/ref/) until they are on the checkout.
Second machine: ``reproduzir <proof.json> --janela S1 [--partes N ...] --lease <heavy_lease.py>`` reruns parts and
compares each part's ``phase_chain_sha256`` and result with the proof's. ``tudo --diagnostico-planejamento``
runs the same parts in the Graphics planning diagnostic (.local only).
"""
import argparse
import bisect
import hashlib
import json
import lzma
import os
import platform
import resource
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))
from ambiente_ia_runtime import EXE, ORIGINAL_SHA256, ROOT, SBL  # noqa: E402

SCRIPT = 'pesquisas-paralelas/ia-runtime/provar_entrada_janelas_ia.py'
SONDAS = 'pesquisas-paralelas/missoes/m3/sondas'
M22 = 'pesquisas-paralelas/missoes/evidencias/captura-quadros128-monde01-exibicao-v2.json.xz'
SHA_M22 = '4c8f5c14a9623131dd019eafcdc49ea63054ee358f9defde58c12cb949f59ff3'
JANELAS = {
    'P1': dict(manifesto=f'{SONDAS}/P1/captura-janela.manifest.json',
               sha='5681219c9f29e90084678d271d0b29bc1255cee0f66cd74e5c4f0d331fd2d905',
               comandos=f'{SONDAS}/P1/comandos.jsonl.xz',
               sha_comandos='e5317d9fe5c12c6e5c6460af1eaa74c2fa2a0190a3a43e9f12488bfaaf856f23',
               entradas=f'{SONDAS}/P1/entradas.jsonl.xz', sha_entradas='b114b35d127926692f493971b177a7e92d4ca22091e9b042dec4cfbce35f18f9'),
    'P2': dict(manifesto=f'{SONDAS}/P2/captura-janela.manifest.json',
               sha='992cc38d37b7e147cfb812bfbbd660b7d1ba16e4fb36f1585f83c44fbbb9cd57',
               comandos=f'{SONDAS}/P2/comandos.jsonl.xz',
               sha_comandos='21e4cad942ff36d7895587e862555801f64e010e4a0cf326b08e08a0e8a182ac',
               entradas=f'{SONDAS}/P2/entradas.jsonl.xz', sha_entradas='d6f7b81f11f15bf0d8fe1e7e90a3afc4c317e013c282385179dcd11023dd0d61'),
    # P6 (P3 through cave lodging, frames 129-2400, 3 parts): Missions' d18add9, not yet on main. Until it is,
    # the pinned files are read from that commit (``git show``) into .local/m3-1/ref/P6 and hash-checked.
    'P6': dict(manifesto=f'{SONDAS}/P6/captura-janela.manifest.json',
               sha='9e66bb4fd23dae0777a983820b54952bedb11f3b4ab0b84a6481340945de754f',
               comandos=f'{SONDAS}/P6/comandos.jsonl.xz',
               sha_comandos='88e4fe171e9563189aa95b44c5e59abb460125a28085ba332fa8c0e98f278ed3',
               entradas=f'{SONDAS}/P6/entradas.jsonl.xz', sha_entradas='a9de5b5771a869d404ae25b51e6784dc146345f4cc6ba8e08226efe7ef268e0b',
               ref='d18add9e'),
    # S1 (frames 129-17050, ~17 parts): the Mac mini's pass-2 capture on feat/re-missions. Unpinned until it lands:
    # `fixar S1 --ref origin/feat/re-missions` rewrites this entry with the landed files' SHA-256 and the commit.
    # S1-BEGIN
    'S1': dict(manifesto=f'{SONDAS}/S1/captura-janela.manifest.json',
               sha='a7ee59f4226b1df92de375bf51fb9d2b57e79dfb17b607e8dfd5c38204b25a76',
               comandos=f'{SONDAS}/S1/comandos.jsonl.xz',
               sha_comandos='e73b75aab67caba52aac114f03709ad6b296e4cbef439668bbaef8f94824bbc7',
               entradas=f'{SONDAS}/S1/entradas.jsonl.xz',
               sha_entradas='fd1df062f4d197dd3930e2d817381485c15ee4bb8c6b290b3c3817d545edec1e',
               ref='559f148f6e6440244d562c4e192748240ce5c60a'),
    # S1-END
}
INICIO = 128
JOGADORES = 4                      # packet pointers and selection areas compared (players 0..3)
PACOTES, TAM_PACOTE = 0x4e2458, 10
SELECOES, TAM_SELECAO = 0x508728, 512
POOL, PASSO, UNIDADES = 0x4e19a0, 276, 800
CAMPOS_ORDEM = ((0x02, 1), (0xb2, 2), (0xb7, 1), (0xb8, 1), (0xbe, 1), (0x110, 4))
DETALHADAS = 6                     # order-frame phases (and their neighbours) kept in full in the proof


def sha(caminho):
    return hashlib.sha256(Path(caminho).read_bytes()).hexdigest()


def git(*args):
    return subprocess.run(['git', '-C', str(ROOT), *args], capture_output=True, text=True).stdout


def revisao():
    return git('rev-parse', 'HEAD').strip()


def sujos():
    return git('status', '--porcelain').splitlines()


def pasta_relatorios(rev=None):
    return f'.local/m3-1/prova-{(rev or revisao())[:12]}'


def arquivo(nome, caminho, esperado=None):
    """The file at repository path ``caminho`` of window ``nome``: the checkout's when it exists and has the
    expected SHA-256 ``esperado`` (when given), otherwise, for a window pinned to a Missions commit not yet merged
    (``ref``), that commit's blob read once into .local/m3-1/ref/<window>/<commit>/. Every caller checks the pinned
    hash."""
    local = ROOT / caminho
    ref = JANELAS[nome].get('ref')
    if not local.exists() and (ROOT / f'{caminho}.xz').exists():
        # Missions may publish a large JSON (S1's window policy) xz-compressed; the pinned hash is the raw file's.
        copia = ROOT / '.local/m3-1/xz' / caminho
        if not copia.exists():
            copia.parent.mkdir(parents=True, exist_ok=True)
            copia.write_bytes(lzma.decompress((ROOT / f'{caminho}.xz').read_bytes()))
        return copia
    if not ref or (local.exists() and (esperado is None or sha(local) == esperado)):
        return local
    copia = ROOT / '.local/m3-1/ref' / nome / ref[:12] / Path(caminho).name
    if not copia.exists():
        copia.parent.mkdir(parents=True, exist_ok=True)
        dados = subprocess.run(['git', '-C', str(ROOT), 'show', f'{ref}:{caminho}'], capture_output=True,
                               check=True).stdout
        copia.write_bytes(dados)
    return copia


def manifesto(nome):
    j = JANELAS[nome]
    if j['sha'] is None:
        raise SystemExit(f'{nome} is not pinned yet: run `{SCRIPT} fixar {nome} --ref <Missions commit>` once its '
                         'capture has landed, and commit the pinned script')
    if sha(arquivo(nome, j['manifesto'], j['sha'])) != j['sha']:
        raise SystemExit(f'{nome}: the window manifest is not the pinned one')
    m = json.loads(arquivo(nome, j['manifesto'], j['sha']).read_bytes())
    if [p['part'] for p in m['parts']] != list(range(len(m['parts']))):
        raise SystemExit(f'{nome}: the manifest parts are not 0..n-1')
    if sha(arquivo(nome, m['mask']['path'], m['mask']['sha256'])) != m['mask']['sha256']:
        raise SystemExit(f'{nome}: the mask file differs from the manifest')
    if sha(arquivo(nome, j['comandos'], j['sha_comandos'])) != j['sha_comandos'] or \
            sha(arquivo(nome, j['entradas'], j['sha_entradas'])) != j['sha_entradas']:
        raise SystemExit(f'{nome}: comandos.jsonl or entradas.jsonl differs from the pinned file')
    return m


def nome_relatorio(nome, parte, partes, quadros=None):
    base = nome if partes == 1 else f'{nome}-parte{parte:02d}'
    return f'{base}.json' if not quadros else f'{base}-{quadros}q.json'


class Leitor:
    """Reads original addresses from a block state (name -> (base, bytes))."""
    def __init__(self, estado):
        self.blocos = sorted((b, d) for n, (b, d) in estado.items() if n != 'native_stack')
        self.bases = [b for b, _ in self.blocos]

    def __call__(self, endereco, n):
        i = bisect.bisect_right(self.bases, endereco) - 1
        if i < 0:
            return None
        base, dados = self.blocos[i]
        if endereco + n > base + len(dados):
            return None
        return dados[endereco - base:endereco - base + n]


def campos_m31(ler):
    """The M3.1 fields of one state: packets, selection areas and the unit order fields."""
    u32 = lambda a: int.from_bytes(ler(a, 4), 'little')  # noqa: E731
    pacotes = []
    for p in range(JOGADORES):
        ptr = u32(PACOTES + 4 * p)
        corpo = ler(ptr, TAM_PACOTE) if ptr else None
        pacotes.append([hex(ptr), corpo.hex() if corpo is not None else None])
    selecoes = [ler(SELECOES + TAM_SELECAO * p, TAM_SELECAO) for p in range(JOGADORES)]
    base = u32(POOL)
    unidades = ler(base, PASSO * UNIDADES)
    ordens = [b''.join(unidades[i * PASSO + o:i * PASSO + o + k] for o, k in CAMPOS_ORDEM) for i in range(UNIDADES)]
    return dict(packets=pacotes, selection=[s.hex() for s in selecoes], pool=hex(base), unit_order_fields=ordens)


def enderecos_m31(campos):
    """Every original address the M3.1 fields cover (to check that the mask hides none of them)."""
    for p in range(JOGADORES):
        yield from range(PACOTES + 4 * p, PACOTES + 4 * p + 4)
        ptr = int(campos['packets'][p][0], 16)
        if ptr:
            yield from range(ptr, ptr + TAM_PACOTE)
        yield from range(SELECOES + TAM_SELECAO * p, SELECOES + TAM_SELECAO * (p + 1))
    base = int(campos['pool'], 16)
    for i in range(UNIDADES):
        for o, k in CAMPOS_ORDEM:
            yield from range(base + i * PASSO + o, base + i * PASSO + o + k)


def comparar_m31(py, ref):
    dif_unidades = [i for i, (a, b) in enumerate(zip(py['unit_order_fields'], ref['unit_order_fields'])) if a != b]
    h = lambda c: hashlib.sha256(b''.join(c['unit_order_fields'])).hexdigest()  # noqa: E731
    r = dict(packets=dict(python=py['packets'], reference=ref['packets'], equal=py['packets'] == ref['packets']),
             selection=dict(equal=py['selection'] == ref['selection'],
                            python_sha256=hashlib.sha256(''.join(py['selection']).encode()).hexdigest(),
                            reference_sha256=hashlib.sha256(''.join(ref['selection']).encode()).hexdigest(),
                            player0_head=[py['selection'][0][:16], ref['selection'][0][:16]]),
             unit_order_fields=dict(equal=not dif_unidades and py['pool'] == ref['pool'], python_sha256=h(py),
                                    reference_sha256=h(ref), differing_units=[
                                        dict(unit=i, python=py['unit_order_fields'][i].hex(),
                                             reference=ref['unit_order_fields'][i].hex()) for i in dif_unidades[:8]]))
    r['equal'] = r['packets']['equal'] and r['selection']['equal'] and r['unit_order_fields']['equal']
    return r


def normalizar(eventos):
    """Input events as the window part's ``scripted_inputs`` records them (no hwnd, no WndProc flag bytes)."""
    return [{c: v for c, v in e.items() if c not in ('hwnd', 'wndproc_flags_after')} for e in eventos]


def bandeiras(eventos):
    """The WndProc flag bytes 0x5099a8..0x5099b2 after each dispatch (the probe's ``entradas.jsonl`` records)."""
    return [e['wndproc_flags_after'] for e in eventos if e['kind'] == 'dispatch_message']


def chave_ordem(o):
    return (o.get('event', 'SetPlayerOrdre'), o.get('player'), o['tag'], o.get('word2'), o.get('word4'),
            o.get('word6'), o.get('word8'), o.get('packet'), o.get('jump_target'))


def carregar_m22():
    from comparar_quadros_ia import _dados, resumo_estado
    caminho = ROOT / M22
    if sha(caminho) != SHA_M22:
        raise SystemExit('The M2.2 128-frame capture is not the pinned one')
    cap = json.loads(lzma.decompress(caminho.read_bytes()))
    fase = cap['phases'][-1]
    if fase['phase'] != 'frame128':
        raise SystemExit('The M2.2 capture does not end at frame128')
    estado = {n: (int(b['base'], 16), _dados(b)) for n, b in fase['state_after']['full_state'].items()}
    if resumo_estado({n: v for n, v in estado.items() if n != 'native_stack'}) != fase['state_after']['summary']:
        raise SystemExit('frame128 full state does not match its summary')
    return cap, estado


def codigo_importado():
    saida = {}
    for modulo in list(sys.modules.values()):
        f = getattr(modulo, '__file__', None)
        if not f:
            continue
        p = Path(f).resolve()
        if p.suffix == '.py' and p.is_relative_to(ROOT):
            saida[str(p.relative_to(ROOT))] = sha(p)
    return dict(sorted(saida.items()))


def comparar_janela(nome, quadros=None, n_parte=0, planejamento=False):
    """The window's comparison body (see the module docstring)."""
    from comparar_quadros_ia import (MascaraEnderecos, _dados, carregar_captura, comparar_sequencia,
                                     fases_referencia, resumo_estado, resumos_mascarados, travessias_medidas)
    from composicao_entrada_ia import JANELA, ComposicaoEntrada, RoteiroEntrada
    from composicao_encadeada_ia import MemoriaMapaRapida
    from composicao_quadros_ia import REGISTRADORES, carregar_cenario_exibicao, fases_quadros
    from contexto_exibicao_ia import ContextoExibicao
    from inventario_ia_runtime import OriginalImage
    m = manifesto(nome)
    entrada_m = m['parts'][n_parte]
    artefato = arquivo(nome, entrada_m['artifact'], entrada_m['compressed_sha256'])
    if sha(artefato) != entrada_m['compressed_sha256']:
        raise SystemExit(f'{nome}: the xz part differs from the manifest')
    parte, sha_bruto = carregar_captura(artefato, entrada_m['raw_sha256'])
    if parte['mask'] != m['mask'] or parte['probe'] != nome or parte['part'] != n_parte:
        raise SystemExit(f'{nome}: the part names another mask, probe or part number')
    anterior = m['parts'][n_parte - 1]['raw_sha256'] if n_parte else None
    if parte.get('previous_part_raw_sha256') != anterior:
        raise SystemExit(f'{nome}: part {n_parte} does not chain to the previous manifest part')
    mascara_doc = json.loads(arquivo(nome, m['mask']['path'], m['mask']['sha256']).read_bytes())
    pol = mascara_doc['window_policy']
    if sha(arquivo(nome, pol['path'], pol['sha256'])) != pol['sha256'] or not pol['passed']:
        raise SystemExit(f'{nome}: the window policy differs from the mask file or did not pass')
    politica = json.loads(arquivo(nome, pol['path'], pol['sha256']).read_bytes())
    mascara = MascaraEnderecos(mascara_doc['cumulative']['exclusion_mask'])
    if mascara.bytes != mascara_doc['cumulative']['bytes']:
        raise SystemExit(f'{nome}: mask byte count differs from the mask file')
    if sha(arquivo(nome, parte['input']['path'], parte['input']['sha256'])) != parte['input']['sha256']:
        raise SystemExit(f'{nome}: the scripted-input file differs from the part')
    dados_entrada = json.loads(arquivo(nome, parte['input']['path'], parte['input']['sha256']).read_bytes())

    aberto = parte['opening_state']
    s0 = {n: (int(b['base'], 16), _dados(b)) for n, b in aberto['full_state'].items()}
    comparado, mascarado = resumos_mascarados(mascara, s0)
    abertura = dict(summary_equal=resumo_estado(s0) == aberto['summary'],
                    compared_summary_equal=comparado == aberto['compared_summary'],
                    masked_sha256_equal=mascarado == aberto['masked_sha256'])
    cap128, estado128 = carregar_m22()
    if n_parte == 0:
        abertura['equals_m22_frame128_full_state'] = s0 == {n: v for n, v in estado128.items()
                                                            if n != 'native_stack'}
    if not all(abertura.values()):
        raise SystemExit(f'{nome}: opening state check failed: {abertura}')

    nomes = [f['phase'] for f in parte['phases']]
    total = len(nomes) // 2
    n = min(quadros, total) if quadros else total
    inicio = int(nomes[0][len('between_frames'):]) - 1
    if (n_parte == 0) != (inicio == INICIO) or nomes != fases_quadros(total, inicio):
        raise SystemExit(f'{nome}: part phases are not whole frames after frame {inicio}')
    nomes = nomes[:2 * n]
    _, cap_v2, entrada, m1 = carregar_cenario_exibicao()
    alocacoes = cap128['allocations']
    # The frame-128 allocation records are a declared input. They apply to this part only when no earlier part
    # allocates or releases (checked by ``agregar`` over every part's ``allocation_events``) and up to this part's
    # first allocation event: the comparison stops at the last whole frame before it.
    if parte['phases'][0]['entry']['allocations'] != len(alocacoes):
        raise SystemExit(f'{nome}: part {n_parte} opens with {parte["phases"][0]["entry"]["allocations"]} allocation '
                         f'records; the frame-128 records ({len(alocacoes)}) do not apply')
    eventos_alocacao = [f['phase'] for f in parte['phases'] if f['state_delta'].get('allocated') or
                        f['state_delta'].get('released') or f['exit']['allocations'] != len(alocacoes)]
    parada_alocacao = None
    if eventos_alocacao:
        primeira_alocacao = [f['phase'] for f in parte['phases']].index(eventos_alocacao[0])
        if primeira_alocacao // 2 < n:
            n = primeira_alocacao // 2
            parada_alocacao = dict(phase=eventos_alocacao[0], frames_compared=n,
                                   reason='the original allocates or releases a block here; the frame-128 '
                                          'allocation records end their validity at this phase')
            if n == 0:
                raise SystemExit(f'{nome}: part {n_parte} allocates in its first frame ({eventos_alocacao[0]})')
            nomes = nomes[:2 * n]
    regs = {k: v for k, v in parte['phases'][0]['entry']['registers'].items() if k in REGISTRADORES}
    roteiro = RoteiroEntrada(dados_entrada, inicio=INICIO)
    roteiro.posicionar(inicio)
    comp = ComposicaoEntrada(s0, dict(named_inputs=cap_v2['named_inputs'], phases=parte['phases']), entrada, m1,
                             roteiro, inicio=inicio, alocacoes=alocacoes, regs_inicio=regs, planejamento=planejamento)
    if inicio != INICIO:
        comp.palavras_msg = roteiro.ultima_mensagem(inicio, MemoriaMapaRapida(comp.mapa).u32(JANELA))
        comp.palavras_inicio = roteiro.palavras_salvas(inicio)
    contexto = ContextoExibicao(OriginalImage(), politica['display_roots'])

    comandos = [json.loads(x) for x in lzma.decompress(arquivo(nome, JANELAS[nome]['comandos'],
                                                               JANELAS[nome]['sha_comandos']).read_bytes())
                .decode().splitlines() if x.strip()]
    entradas_p1 = [json.loads(x) for x in lzma.decompress(arquivo(nome, JANELAS[nome]['entradas'],
                                                                  JANELAS[nome]['sha_entradas']).read_bytes())
                   .decode().splitlines() if x.strip()]
    lado_py, lado_ref = [], []
    # The window harness (entrada_roteirizada) records top_callee = null on every boundary, where the M2.3 oracle
    # recorded the issuing top-level callee. When the whole window carries null, the field is not compared: Python's
    # value is counted in the report and set to null; every other boundary field is compared.
    topo_nulo = all(b.get('top_callee') is None for f in parte['phases'] for b in f['boundaries'])
    topos_python = {}

    class Proxy:
        """``comp`` for ``comparar_sequencia``, recording the M3.1 extras at each phase end."""
        def __init__(self, c):
            self.c = c

        def __getattr__(self, a):
            return getattr(self.c, a)

        def executar(self, k):
            for passo in self.c.executar(k):
                if topo_nulo:
                    for e in passo['registro'].fronteiras:
                        chave = f"{e['routine']}:{e.get('top_callee')}"
                        topos_python[chave] = topos_python.get(chave, 0) + 1
                        e['top_callee'] = None
                lado_py.append(dict(phase=passo['phase'], m31=campos_m31(lambda a, t: self.c.mapa.ler(a, t)),
                                    inputs=normalizar(passo['eventos']), flags=bandeiras(passo['eventos']),
                                    orders=list(passo['ordens'])))
                yield passo

    def referencia_m31(gen):
        for fase_cap, estado, integridade in gen:
            lado_ref.append(dict(phase=fase_cap['phase'], m31=campos_m31(Leitor(estado)),
                                 inputs=normalizar(fase_cap.get('scripted_inputs', []))))
            yield fase_cap, estado, integridade

    referencia = referencia_m31(fases_referencia(dict(phases=parte['phases'][:2 * n]), s0, mascara))
    fases, hud, resultado = comparar_sequencia(Proxy(comp), nomes, n, referencia, mascara, contexto)
    if parada_alocacao and resultado == 'equal':
        resultado = 'stopped_allocation_' + parada_alocacao['phase']

    # The M3.1 extras, phase by phase (the base comparison stopped at its own first difference, if any).
    escondidos = None
    for py, ref in zip(lado_py, lado_ref):
        fase = py['phase']
        if fase not in fases or ref['phase'] != fase:
            break
        r = fases[fase]
        r['m31_fields'] = comparar_m31(py['m31'], ref['m31'])
        if escondidos is None:
            escondidos = sum(mascara.mascarado(a) for a in set(enderecos_m31(ref['m31'])))
        flags_ref = bandeiras([e for e in entradas_p1 if e.get('phase') == fase])
        r['scripted_inputs'] = dict(python=len(py['inputs']), reference=len(ref['inputs']),
                                    wndproc_flags=dict(python=py['flags'], reference=flags_ref),
                                    equal=py['inputs'] == ref['inputs'] and py['flags'] == flags_ref)
        if not r['scripted_inputs']['equal']:
            r['scripted_inputs'].update(python_events=py['inputs'][:12], reference_events=ref['inputs'][:12])
        if fase.startswith('frame'):
            k = int(fase[len('frame'):])
            o_py = [chave_ordem(o) for o in py['orders']]
            o_ref = [chave_ordem(c) for c in comandos if c['frame'] == k]
            r['orders'] = dict(python=[list(x) for x in o_py], reference=[list(x) for x in o_ref],
                               equal=o_py == o_ref)
        base = r['equal']
        r['equal_base'] = base
        r['equal'] = base and r['m31_fields']['equal'] and r['scripted_inputs']['equal'] and \
            r.get('orders', {}).get('equal', True)
        if not r['equal'] and resultado == 'equal':
            resultado = 'first_difference_' + fase
    primeira = next((f for f, r in fases.items() if not r['equal']), None)
    if primeira:
        corte = list(fases).index(primeira) + 1
        fases = dict(list(fases.items())[:corte])
        resultado = 'first_difference_' + primeira if fases[primeira].get('result') == 'returned' else \
            f'stopped_{primeira}'
    elif parada_alocacao:
        resultado = 'stopped_allocation_' + parada_alocacao['phase']
    ordens_py = [dict(o, phase=p['phase']) for p in lado_py for o in p['orders']]
    return dict(
        window=nome, manifest=dict(path=JANELAS[nome]['manifesto'], sha256=JANELAS[nome]['sha']),
        part=dict(path=entrada_m['artifact'], sha256=entrada_m['compressed_sha256'], raw_json_sha256=sha_bruto,
                  frames=parte['frames'], first_phase=nomes[0], last_phase=nomes[-1], phases=len(parte['phases']),
                  phases_requested=len(nomes), number=n_parte, parts=len(m['parts']),
                  previous_part_raw_sha256=parte.get('previous_part_raw_sha256'),
                  opening_summary=aberto['summary'],
                  final_reference_summary=parte['phases'][-1]['state_after']['summary'],
                  opening_state=dict(abertura, start_frame=inicio,
                                     allocation_records=dict(
                                         count=len(alocacoes),
                                         source=f'{M22} allocations (frame 128; the window allocates/releases '
                                                'nothing and keeps the count)'),
                                     declared=None if n_parte == 0 else dict(
                                         entry_registers=regs, msg_words=[hex(x) for x in comp.palavras_msg],
                                         cursor=list(roteiro.xy),
                                         saved_frame_words=[hex(x) for x in comp.palavras_inicio])),
                  full_states=[f for f, v in fases.items() if v.get('reference_integrity', {}).get(
                      'checkpoint_full_state_equal')]),
        mask=dict(path=m['mask']['path'], sha256=m['mask']['sha256'], masked_bytes=mascara.bytes,
                  ranges=len(mascara_doc['cumulative']['exclusion_mask']), added_display_only=mascara_doc[
                      'added_display_only'], removed_game_logic_conflicts=mascara_doc['removed_game_logic_conflicts']),
        policy=dict(path=pol['path'], sha256=pol['sha256'], display_roots=len(politica['display_roots'])),
        input=parte['input'], commands=dict(path=JANELAS[nome]['comandos'], sha256=JANELAS[nome]['sha_comandos'],
                                            records=len(comandos)),
        input_log=dict(path=JANELAS[nome]['entradas'], sha256=JANELAS[nome]['sha_entradas'], records=len(entradas_p1),
                       use='WndProc flag bytes after each DispatchMessageA (the window part does not carry them)'),
        m22_frame128=dict(path=M22, sha256=SHA_M22),
        m31_fields_hidden_by_mask=escondidos,
        allocation_events=eventos_alocacao, allocation_stop=parada_alocacao,
        boundary_top_callee=dict(
            compared=not topo_nulo, reference='null on every boundary of the window' if topo_nulo else 'recorded',
            python_values_not_compared=topos_python),
        graphics_planning_stops=comp.ctx.paradas_planejamento if planejamento else None,
        crossings=travessias_medidas(comp, mascara), hud_flag=hud, phases=fases, orders_python=ordens_py,
        text_boundary=comp.textos,
        summary=dict(result=resultado, phases_compared=len(fases),
                     phases_equal=sum(1 for v in fases.values() if v['equal']), phases_total=len(nomes),
                     orders_equal=sum(1 for v in fases.values() if v.get('orders', {}).get('equal')),
                     m31_fields_equal=sum(1 for v in fases.values() if v.get('m31_fields', {}).get('equal')),
                     scripted_inputs_equal=sum(1 for v in fases.values() if v.get('scripted_inputs', {}).get('equal'))))


def rodar_janela(nome, relatorios, quadros=None, n_parte=0, planejamento=False):
    from provar_quadros_9200_ia import cadeia_fases
    partes = len(manifesto(nome)['parts'])
    saida = ROOT / relatorios / (('diagnostico-planejamento-' if planejamento else '') +
                                 nome_relatorio(nome, n_parte, partes, quadros))
    if planejamento and not saida.resolve().is_relative_to((ROOT / '.local').resolve()):
        raise SystemExit('A planning diagnostic writes under .local/ only')
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    rev, sujo = revisao(), sujos()
    t0 = time.monotonic()
    corpo = comparar_janela(nome, quadros, n_parte, planejamento)
    segundos = round(time.monotonic() - t0, 1)
    pico = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rel = dict(schema='rising-lands/ai-runtime-m3.1-window-comparison/1', source_revision=rev,
               diagnostic_graphics_planning=planejamento,
               source_dirty_paths=sujo, seconds=segundos,
               peak_rss_bytes=pico if sys.platform == 'darwin' else pico * 1024,
               machine=dict(system=platform.system(), release=platform.release(), machine=platform.machine(),
                            processor=platform.processor(), python=platform.python_version()),
               code_sha256=codigo_importado(), phase_chain_sha256=cadeia_fases(corpo['phases']), **corpo)
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(rel, f, indent=1, sort_keys=True, default=str)
        f.write('\n')
    primeira = next(((f, r) for f, r in rel['phases'].items() if not r['equal']), None)
    print(json.dumps(dict(window=nome, output=str(saida), summary=rel['summary'], seconds=segundos,
                          crossings=rel['crossings'], phase_chain_sha256=rel['phase_chain_sha256'],
                          first_difference=primeira and dict(phase=primeira[0], **{
                              k: v for k, v in primeira[1].items()
                              if k in ('stop', 'state', 'rng', 'm31_fields', 'orders', 'scripted_inputs', 'result')}),
                          peak_rss_mb=round(rel['peak_rss_bytes'] / 2**20)), indent=1, default=str), flush=True)
    return 0 if rel['summary']['result'] == 'equal' else 2


# ---------------------------------------------------------------------------------------------------- aggregation

def partes_manifesto(nome):
    return [dict(path=mp['artifact'], sha256=mp['compressed_sha256']) for mp in manifesto(nome)['parts']]


def resumo_parte(r):
    """One part report in a line: its range, result, first unequal phase (with its stop) and chain."""
    primeira = next(((f, v) for f, v in r['phases'].items() if not v['equal']), None)
    return dict(part=r['part'].get('number', 0), frames=r['part']['frames'], result=r['summary']['result'],
                phases_equal=r['summary']['phases_equal'], phases=r['part']['phases'],
                first_unequal=primeira and dict(phase=primeira[0], result=primeira[1].get('result'),
                                                stop=primeira[1].get('stop')),
                allocation_stop=r.get('allocation_stop'), crossings=r['crossings'],
                phase_chain_sha256=r['phase_chain_sha256'], source_revision=r['source_revision'],
                diagnostic_graphics_planning=r.get('diagnostic_graphics_planning'))


def alcance_janela(m, partes_rel):
    """How far the window goes: the parts equal over every phase from the start (each part starts from its own
    checkpoint, so a later part can be equal after an earlier stop), the first phase that is not, and every
    part's own line."""
    linhas = [None if r is None else resumo_parte(r) for r in partes_rel]
    prefixo = 0
    for mp, linha in zip(m['parts'], linhas):
        if linha is None or linha['result'] != 'equal' or linha['phases_equal'] != mp['phases']:
            break
        prefixo += 1
    corte = linhas[prefixo] if prefixo < len(linhas) else None
    return dict(parts=len(m['parts']), equal_parts_from_start=prefixo,
                equal_through_frame=m['parts'][prefixo - 1]['frames'][1] if prefixo else None,
                first_stop=None if prefixo == len(linhas) else (
                    dict(part=prefixo, report=None) if corte is None else
                    dict(part=prefixo, phase=(corte['first_unequal'] or {}).get('phase'),
                         result=corte['result'], stop=(corte['first_unequal'] or {}).get('stop'),
                         allocation_stop=corte['allocation_stop'])),
                equal_parts=[linha['part'] for mp, linha in zip(m['parts'], linhas) if linha and
                             linha['result'] == 'equal' and linha['phases_equal'] == mp['phases']])


def agregar(relatorios, janelas, planejamento=False):
    from provar_quadros_9200_ia import tabela_rle
    prefixo_rel = 'diagnostico-planejamento-' if planejamento else ''
    rev, sujo = revisao(), sujos()
    saida_janelas, problemas, codigo = [], [], {}
    for nome in janelas:
        m = manifesto(nome)
        erros, partes_rel, caminhos = [], [], []
        alocou_antes = None                     # first earlier part with an allocation event
        for mp in m['parts']:
            caminho = ROOT / relatorios / (prefixo_rel + nome_relatorio(nome, mp['part'], len(m['parts'])))
            rotulo = f"part {mp['part']}: "
            if not caminho.exists():
                erros.append(rotulo + 'no report (the run exited before writing one; see its log)')
                partes_rel.append(None)
                caminhos.append(caminho)
                continue
            r = json.loads(caminho.read_bytes())
            caminhos.append(caminho)
            partes_rel.append(r)
            if alocou_antes is not None:
                erros.append(rotulo + f'part {alocou_antes} allocates or releases a block, so the frame-128 '
                             'allocation records do not apply to this part')
            if r.get('allocation_events') and alocou_antes is None:
                alocou_antes = mp['part']
            if r['part']['raw_json_sha256'] != mp['raw_sha256']:
                erros.append(rotulo + 'report is not for the manifest part')
            if r['summary']['result'] != 'equal' or r['summary']['phases_equal'] != mp['phases']:
                erros.append(rotulo + f"result {r['summary']['result']} ({r['summary']['phases_equal']}/{mp['phases']})")
            if bool(r.get('diagnostic_graphics_planning')) != planejamento:
                erros.append(rotulo + 'diagnostic report mixed with proof reports')
            if r['source_revision'] != rev or r['source_dirty_paths']:
                erros.append(rotulo + f"report from revision {r['source_revision'][:12]} "
                             f"(dirty: {bool(r['source_dirty_paths'])})")
            if r['crossings']['count'] or r['crossings']['writing_compared_bytes']:
                erros.append(rotulo + f"crossings {r['crossings']}")
            if r['m31_fields_hidden_by_mask']:
                erros.append(rotulo + f"{r['m31_fields_hidden_by_mask']} M3.1 field bytes are masked")
            if mp['part'] and partes_rel[-2] is not None and \
                    r['part'].get('opening_summary') != partes_rel[-2]['part'].get('final_reference_summary'):
                erros.append(rotulo + 'opening state is not the previous part\'s final reference state')
            conflitos = sorted(f for f, h in r['code_sha256'].items() if codigo.get(f, h) != h)
            if conflitos:
                erros.append(rotulo + f'imported code differs from an earlier report: {conflitos}')
            codigo.update(r['code_sha256'])
        if erros:
            problemas.append(dict(window=nome, problems=erros))
        alcance = alcance_janela(m, partes_rel)
        if any(r is None for r in partes_rel):
            saida_janelas.append(dict(window=nome, result='incomplete', reach=alcance,
                                      parts=[None if r is None else resumo_parte(r) for r in partes_rel]))
            continue
        rel = dict(partes_rel[0])
        if len(partes_rel) > 1:
            rel.update(
                phases={f: v for r in partes_rel for f, v in r['phases'].items()},
                hud_flag=[h for r in partes_rel for h in r['hud_flag']],
                orders_python=[o for r in partes_rel for o in r['orders_python']],
                text_boundary=[t for r in partes_rel for t in r['text_boundary']],
                m31_fields_hidden_by_mask=max(r['m31_fields_hidden_by_mask'] or 0 for r in partes_rel),
                crossings={k: sum(r['crossings'][k] for r in partes_rel)
                           for k in ('count', 'writing_compared_bytes', 'core_provider_stops')},
                seconds=round(sum(r['seconds'] for r in partes_rel), 1),
                peak_rss_bytes=max(r['peak_rss_bytes'] for r in partes_rel),
                summary=dict(result='equal' if all(r['summary']['result'] == 'equal' for r in partes_rel) else
                             next(r['summary']['result'] for r in partes_rel if r['summary']['result'] != 'equal'),
                             **{k: sum(r['summary'][k] for r in partes_rel)
                                for k in ('phases_compared', 'phases_equal', 'phases_total', 'orders_equal',
                                          'm31_fields_equal', 'scripted_inputs_equal')}),
                phase_chain_sha256=hashlib.sha256(''.join(r['phase_chain_sha256'] for r in partes_rel)
                                                  .encode()).hexdigest())
            rel['part'] = dict(rel['part'], frames=m['parts'][0]['frames'][:1] + m['parts'][-1]['frames'][1:],
                               last_phase=partes_rel[-1]['part']['last_phase'],
                               full_states=[f for r in partes_rel for f in r['part']['full_states']])
        caminho = caminhos[0]
        partes_resumo = [dict(part=r['part']['number'] if 'number' in r['part'] else 0, frames=r['part']['frames'],
                              first_phase=r['part']['first_phase'], last_phase=r['part']['last_phase'],
                              result=r['summary']['result'], phases_equal=r['summary']['phases_equal'],
                              phases=r['summary']['phases_compared'], crossings=r['crossings'],
                              phase_chain_sha256=r['phase_chain_sha256'], seconds=r['seconds'],
                              opening_state=r['part']['opening_state'], report_sha256=sha(c))
                         for r, c in zip(partes_rel, caminhos)]
        fases = rel['phases']
        huds = {h['phase']: h['equal'] for h in rel['hud_flag']}
        frames_ordem = sorted({int(f[len('frame'):]) for f, r in fases.items()
                               if f.startswith('frame') and r.get('orders', {}).get('reference')})
        detalhe = []
        for k in frames_ordem[:DETALHADAS]:
            detalhe += [f'between_frames{k}', f'frame{k}']
        cont = lambda chave: sum(1 for r in fases.values() if chave(r))  # noqa: E731
        entre = [r for f, r in fases.items() if f.startswith('between_frames')]
        saida_janelas.append(dict(
            window=nome, frames=rel['part']['frames'], manifest=rel['manifest'], part=rel['part'], mask=rel['mask'],
            policy=rel['policy'], input=rel['input'], commands=rel['commands'], m22_frame128=rel['m22_frame128'],
            result=rel['summary']['result'], phases=rel['summary']['phases_compared'],
            phases_equal=rel['summary']['phases_equal'],
            equality=dict(
                state=cont(lambda r: r.get('state', {}).get('equal')),
                compared_bytes_per_phase=sorted({r['state']['compared_bytes'] for r in fases.values() if 'state' in r}),
                compared_byte_phase_total=sum(r['state']['compared_bytes'] for r in fases.values() if 'state' in r),
                compared_summary=cont(lambda r: r.get('compared_summary', {}).get('equal')),
                rng=cont(lambda r: r.get('rng', {}).get('equal')),
                bindings_outside_display=cont(lambda r: r.get('bindings', {}).get('equal')),
                boundaries_outside_display=cont(lambda r: r.get('boundaries', {}).get('equal')),
                allocation_count=cont(lambda r: r.get('allocation_count', {}).get('equal')),
                between_frames_exit_registers=dict(equal=sum(all(v['equal'] for v in r['registers'].values())
                                                             for r in entre), checked=len(entre)),
                carried_entry_registers=dict(equal=sum(all(v['equal'] for v in r['carried_entry_registers'].values())
                                                       for r in entre if 'carried_entry_registers' in r),
                                             checked=sum('carried_entry_registers' in r for r in entre)),
                hud_flag=dict(equal=sum(huds.values()), checked=len(huds)),
                scripted_inputs=cont(lambda r: r.get('scripted_inputs', {}).get('equal')),
                orders_frame_phases=dict(equal=rel['summary']['orders_equal'],
                                         checked=sum('orders' in r for r in fases.values())),
                m31_fields=rel['summary']['m31_fields_equal'],
                m31_fields_hidden_by_mask=rel['m31_fields_hidden_by_mask'],
                reference_integrity=dict(
                    summary=cont(lambda r: r['reference_integrity'].get('summary_equal')),
                    compared_summary=cont(lambda r: r['reference_integrity'].get('compared_summary_equal')),
                    masked_sha256=cont(lambda r: r['reference_integrity'].get('masked_sha256_equal')),
                    full_states=rel['part']['full_states'])),
            bindings_boundaries=dict(
                bindings_compared=sum(r['bindings']['original'] for r in fases.values() if 'bindings' in r),
                boundaries_compared=sum(r['boundaries']['original'] for r in fases.values() if 'boundaries' in r),
                display_context_bindings_not_modeled=sum(r['bindings']['display_context_not_modeled']
                                                         for r in fases.values() if 'bindings' in r),
                display_context_boundaries_not_modeled=sum(len(r['boundaries']['display_context_not_modeled'])
                                                           for r in fases.values() if 'boundaries' in r)),
            orders=rel['orders_python'], text_boundary=dict(events=len(rel['text_boundary']),
                                                            frames=sorted({t['frame'] for t in rel['text_boundary']})),
            crossings=rel['crossings'], phase_chain_sha256=rel['phase_chain_sha256'], seconds=rel['seconds'],
            parts=partes_resumo,
            peak_rss_mb=round(rel['peak_rss_bytes'] / 2**20), machine=rel['machine'],
            report_sha256=sha(caminho),
            final_indicators=dict(phase=list(fases)[-1], rng=fases[list(fases)[-1]].get('rng'),
                                  indicators=fases[list(fases)[-1]].get('indicators')),
            phase_table=tabela_rle(fases, huds), order_phases={f: fases[f] for f in detalhe if f in fases},
            reach=alcance))
    resultado = 'equal' if not problemas and all(j['result'] == 'equal' for j in saida_janelas) else 'not_accepted'
    completas = [w for w in saida_janelas if w['result'] != 'incomplete']
    tempos = json.loads((ROOT / relatorios / 'tempo.json').read_bytes()) \
        if (ROOT / relatorios / 'tempo.json').exists() else None
    return dict(
        schema='rising-lands/ai-runtime-m3.1-window-proof/1', source_revision=rev, source_dirty_paths=sujo,
        diagnostic_graphics_planning=planejamento,
        reproduction=dict(
            one_command=f'python3 -B {SCRIPT} tudo --janelas {" ".join(janelas)} [--lease <heavy_lease.py>] '
                        '--saida <proof.json>',
            per_window=f'python3 -B {SCRIPT} janela <P>', aggregate=f'python3 -B {SCRIPT} agregar --janelas '
                                                                    f'{" ".join(janelas)} --saida <proof.json>',
            reports=relatorios),
        evidence_sha256={**{JANELAS[j]['manifesto']: JANELAS[j]['sha'] for j in janelas},
                         **{p['path']: p['sha256'] for j in janelas for p in partes_manifesto(j)},
                         **{w['mask']['path']: w['mask']['sha256'] for w in completas},
                         **{w['policy']['path']: w['policy']['sha256'] for w in completas},
                         **{w['input']['path']: w['input']['sha256'] for w in completas},
                         **{w['commands']['path']: w['commands']['sha256'] for w in completas},
                         M22: SHA_M22,
                         str(EXE.relative_to(ROOT)) if EXE.is_relative_to(ROOT) else 'RISING.EXE': ORIGINAL_SHA256,
                         'RISING.SBL': sha(SBL)},
        code_sha256=dict(sorted(codigo.items())),
        crossings=dict(count=sum(w['crossings']['count'] for w in completas),
                       writing_compared_bytes=sum(w['crossings']['writing_compared_bytes'] for w in completas),
                       core_provider_stops=sum(w['crossings']['core_provider_stops'] for w in completas),
                       note='measured: mode \'prova\' carries no crossing data, so any crossing would stop the window'),
        m31_fields=dict(
            packets=f'u32 [0x{PACOTES:x}+4p] and its {TAM_PACOTE}-byte packet, p = 0..{JOGADORES - 1}',
            selection=f'0x{SELECOES:x}+{TAM_SELECAO}p, {TAM_SELECAO} bytes, p = 0..{JOGADORES - 1}',
            unit_order_fields=f'+2 (u8), +0xb2 (u16), +0xb7, +0xb8, +0xbe (u8), +0x110 (u32) of each of the '
                              f'{UNIDADES} slots of the pool [0x{POOL:x}] ({PASSO}-byte records)'),
        windows=saida_janelas, problems=problemas,
        timing=dict(per_window_seconds={w['window']: w['seconds'] for w in completas}, run=tempos),
        unmodeled=[
            'stack words of MCICD_Play in the CalculGame frame bodies (uninitialized caller locals), EFLAGS and EIP',
            'bindings and boundaries issued inside policy display roots, counted per phase in phase_table',
            'masked display-only state (the window\'s cumulative exclusion_mask) and the surfaces',
            'TextGetMessage: Missions\' declared display-scenario boundary (EAX 0, no cleanup), compared as a '
            'boundary event',
            'the frame-128 allocation records (M2.2 capture) are a declared input; no phase allocates or releases a '
            'block and every phase keeps the count',
            'the between_frames129 entry registers are a declared input from the window capture'],
        summary=dict(result=resultado, windows={w['window']: f"{w['phases_equal']}/{w['phases']}"
                                                for w in completas},
                     reach={w['window']: w['reach'] for w in saida_janelas},
                     phases=sum(w['phases'] for w in completas),
                     phases_equal=sum(w['phases_equal'] for w in completas),
                     crossings=sum(w['crossings']['count'] for w in completas)))


def escrever_prova(relatorios, janelas, saida_nome, planejamento=False):
    saida = ROOT / saida_nome
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    prova = agregar(relatorios, janelas, planejamento)
    ok = prova['summary']['result'] == 'equal' and not prova['source_dirty_paths'] and not planejamento
    if not ok:
        rotulo = 'm3-1-diagnostic-planning-' if planejamento else 'm3-1-proof-not-accepted-'
        saida = ROOT / '.local' / (rotulo + '-'.join(janelas) + '-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(prova, f, indent=1, sort_keys=True, default=str)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), summary=prova['summary'], problems=prova['problems'],
                          timing=prova['timing'], part_chains={w['window']: [
                              p and dict(part=p['part'], result=p['result'], chain=p['phase_chain_sha256'])
                              for p in w['parts']] for w in prova['windows']}), indent=1, default=str))
    return 0 if ok else 2


def rodar_partes(tarefas, lease, relatorios, paralelo=None, planejamento=False):
    """Run each (window, part, parts) as its own ``janela`` process (under the heavy lease when given: each part
    takes one slot, so the lease bounds the machine's load). Returns (label, exit code, wall seconds) per part."""
    logs = ROOT / relatorios
    logs.mkdir(parents=True, exist_ok=True)

    def uma(tarefa):
        nome, n_parte, partes = tarefa
        rotulo = ('diagnostico-planejamento-' if planejamento else '') + \
            nome_relatorio(nome, n_parte, partes)[:-len('.json')]
        cmd = [sys.executable, '-B', str(ROOT / SCRIPT), 'janela', nome, '--parte', str(n_parte),
               '--relatorios', relatorios] + (['--diagnostico-planejamento'] if planejamento else [])
        if lease:
            cmd = [sys.executable, lease, f'ai-m31-{rotulo}', '--'] + cmd
        inicio = time.monotonic()
        with open(logs / f'{rotulo}.log', 'x') as log:
            codigo = subprocess.run(cmd, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT).returncode
        return rotulo, codigo, round(time.monotonic() - inicio, 1)

    with ThreadPoolExecutor(max_workers=paralelo or len(tarefas)) as ex:
        resultados = []
        for r in ex.map(uma, tarefas):
            print(f'{r[0]}: exit {r[1]}, {r[2]} s wall', flush=True)
            resultados.append(r)
    return resultados


def tudo(janelas, lease, relatorios, saida, paralelo=None, partes=None, planejamento=False):
    if sujos() and not planejamento:
        raise SystemExit('The one-command proof runs on a clean tree only')
    t0 = time.monotonic()
    tarefas = [(nome, mp['part'], len(manifesto(nome)['parts'])) for nome in janelas
               for mp in manifesto(nome)['parts'] if partes is None or mp['part'] in partes]
    resultados = rodar_partes(tarefas, lease, relatorios, paralelo, planejamento)
    with open(ROOT / relatorios / ('tempo-planejamento.json' if planejamento else 'tempo.json'), 'x') as f:
        json.dump(dict(parallel=paralelo or len(tarefas), lease=bool(lease),
                       wall_seconds=round(time.monotonic() - t0, 1),
                       window_wall_seconds={n: s for n, _, s in resultados},
                       window_exit_codes={n: c for n, c, _ in resultados}), f, indent=1)
    return escrever_prova(relatorios, janelas, saida, planejamento)


def fixar(nome, ref):
    """Pin window ``nome`` to the Missions commit ``ref`` resolves to: read its manifest, pass-1 command and input
    logs from that commit (git show), check that every part, the mask, the policy and the scripted-input file the
    manifest and parts name are in that commit with the stated SHA-256 (parts: the manifest's compressed hash),
    then rewrite the window's entry between ``# <P>-BEGIN``/``# <P>-END`` in this script. Commit the script."""
    commit = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', '--verify', f'{ref}^{{commit}}'],
                            capture_output=True, text=True, check=True).stdout.strip()

    def blob(caminho):
        r = subprocess.run(['git', '-C', str(ROOT), 'show', f'{commit}:{caminho}'], capture_output=True)
        if r.returncode:
            rx = subprocess.run(['git', '-C', str(ROOT), 'show', f'{commit}:{caminho}.xz'], capture_output=True)
            if rx.returncode:
                raise SystemExit(f'{nome}: {caminho} is not in {commit[:12]}')
            return lzma.decompress(rx.stdout)
        return r.stdout
    j = JANELAS[nome]
    bruto = blob(j['manifesto'])
    m = json.loads(bruto)
    if m.get('probe') != nome or [p['part'] for p in m['parts']] != list(range(len(m['parts']))):
        raise SystemExit(f'{nome}: the manifest names probe {m.get("probe")} or its parts are not 0..n-1')
    for mp in m['parts']:
        if hashlib.sha256(blob(mp['artifact'])).hexdigest() != mp['compressed_sha256']:
            raise SystemExit(f'{nome}: part {mp["part"]} differs from the manifest')
    mascara = blob(m['mask']['path'])
    if hashlib.sha256(mascara).hexdigest() != m['mask']['sha256']:
        raise SystemExit(f'{nome}: the mask differs from the manifest')
    pol = json.loads(mascara)['window_policy']
    if hashlib.sha256(blob(pol['path'])).hexdigest() != pol['sha256'] or not pol['passed']:
        raise SystemExit(f'{nome}: the window policy differs from the mask or did not pass')
    comandos, entradas = blob(j['comandos']), blob(j['entradas'])
    entrada = f'{SONDAS.rsplit("/", 1)[0]}/entradas/{nome}.json'
    novo = (f"    '{nome}': dict(manifesto=f'{{SONDAS}}/{nome}/captura-janela.manifest.json',\n"
            f"               sha='{hashlib.sha256(bruto).hexdigest()}',\n"
            f"               comandos=f'{{SONDAS}}/{nome}/comandos.jsonl.xz',\n"
            f"               sha_comandos='{hashlib.sha256(comandos).hexdigest()}',\n"
            f"               entradas=f'{{SONDAS}}/{nome}/entradas.jsonl.xz',\n"
            f"               sha_entradas='{hashlib.sha256(entradas).hexdigest()}',\n"
            f"               ref='{commit}'),\n")
    fonte = Path(__file__).read_text()
    inicio, fim = f'    # {nome}-BEGIN\n', f'    # {nome}-END\n'
    a, b = fonte.index(inicio) + len(inicio), fonte.index(fim)
    Path(__file__).write_text(fonte[:a] + novo + fonte[b:])
    print(json.dumps(dict(window=nome, commit=commit, parts=len(m['parts']),
                          frames=[m['parts'][0]['frames'][0], m['parts'][-1]['frames'][1]],
                          phases=sum(p['phases'] for p in m['parts']), manifest_sha256=hashlib.sha256(bruto).hexdigest(),
                          scripted_input=entrada, next=f'commit {SCRIPT}, then `{SCRIPT} tudo --janelas {nome} '
                                                       '--lease <heavy_lease.py> --saida <proof.json>`'), indent=1))
    return 0


def reproduzir(prova_caminho, nome, partes, lease, relatorios, paralelo=None):
    """Second-machine reproduction: run parts of window ``nome`` (all when ``partes`` is None) on this machine and
    compare each part's ``phase_chain_sha256`` and result with the proof (or not-accepted proof) file."""
    prova = json.loads(Path(prova_caminho).read_bytes())
    janela = next(w for w in prova['windows'] if w['window'] == nome)
    esperado = {p['part']: p for p in janela['parts'] if p}
    m = manifesto(nome)
    tarefas = [(nome, mp['part'], len(m['parts'])) for mp in m['parts']
               if (partes is None or mp['part'] in partes) and mp['part'] in esperado]
    planejamento = bool(prova.get('diagnostic_graphics_planning'))
    rodar_partes(tarefas, lease, relatorios, paralelo, planejamento)
    linhas, iguais = [], 0
    for _, n_parte, total in tarefas:
        caminho = ROOT / relatorios / (('diagnostico-planejamento-' if planejamento else '') +
                                       nome_relatorio(nome, n_parte, total))
        r = json.loads(caminho.read_bytes()) if caminho.exists() else None
        e = esperado[n_parte]
        cadeia = r and r['phase_chain_sha256']
        ok = r is not None and cadeia == e['phase_chain_sha256'] and r['summary']['result'] == e['result']
        iguais += ok
        linhas.append(dict(part=n_parte, equal=ok, chain=cadeia, expected_chain=e['phase_chain_sha256'],
                           result=r and r['summary']['result'], expected_result=e['result'],
                           revision=r and r['source_revision'], expected_revision=e.get('source_revision')))
    print(json.dumps(dict(window=nome, proof=str(prova_caminho), proof_revision=prova['source_revision'],
                          parts_reproduced=f'{iguais}/{len(linhas)}', parts=linhas), indent=1))
    return 0 if iguais == len(linhas) else 2


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='comando', required=True)
    p = sub.add_parser('janela', help='compare one window and write its report')
    p.add_argument('nome', choices=sorted(JANELAS))
    p.add_argument('--relatorios', help='repo-relative report folder (default .local/m3-1/prova-<revision>)')
    p.add_argument('--quadros', type=int, help='diagnostic only: the first N frames (report named <P>-<N>q.json)')
    p.add_argument('--parte', type=int, default=0, help='part of a multi-part window (default 0)')
    p.add_argument('--diagnostico-planejamento', action='store_true',
                   help='diagnostic only (never evidence; report named diagnostico-planejamento-*): a Graphics '
                        'display-path stop is recorded and the drawing taken as writing no logic byte')
    g = sub.add_parser('agregar', help='the proof from the window reports')
    g.add_argument('--janelas', nargs='+', choices=sorted(JANELAS), required=True)
    g.add_argument('--relatorios')
    g.add_argument('--diagnostico-planejamento', action='store_true', help='aggregate diagnostic reports (.local)')
    g.add_argument('--saida', required=True)
    t = sub.add_parser('tudo', help='every part of every window in parallel, then the proof')
    t.add_argument('--janelas', nargs='+', choices=sorted(JANELAS), required=True)
    t.add_argument('--lease', help="path of the machine's heavy_lease.py (each part takes one slot)")
    t.add_argument('--relatorios')
    t.add_argument('--paralelo', type=int, help='parts started at a time (default: all; the lease bounds the load)')
    t.add_argument('--partes', type=int, nargs='+', help='only these part numbers (the proof then lists the rest '
                                                          'as missing)')
    t.add_argument('--diagnostico-planejamento', action='store_true',
                   help='diagnostic only (.local; a dirty tree is allowed): see `janela`')
    t.add_argument('--saida', required=True)
    f = sub.add_parser('fixar', help='pin a window that is not pinned yet (S1) to the Missions commit holding it')
    f.add_argument('nome', choices=sorted(JANELAS))
    f.add_argument('--ref', required=True, help='e.g. origin/feat/re-missions (resolved to its commit)')
    r = sub.add_parser('reproduzir', help='rerun parts here and compare their phase chains with a proof file')
    r.add_argument('prova')
    r.add_argument('--janela', required=True, choices=sorted(JANELAS))
    r.add_argument('--partes', type=int, nargs='+')
    r.add_argument('--lease')
    r.add_argument('--relatorios')
    r.add_argument('--paralelo', type=int)
    a = ap.parse_args()
    if a.comando == 'fixar':
        return fixar(a.nome, a.ref)
    relatorios = a.relatorios or pasta_relatorios()
    if a.comando == 'janela':
        return rodar_janela(a.nome, relatorios, a.quadros, a.parte, a.diagnostico_planejamento)
    if a.comando == 'agregar':
        return escrever_prova(relatorios, a.janelas, a.saida, a.diagnostico_planejamento)
    lease = os.path.abspath(a.lease) if a.lease else None
    if a.comando == 'reproduzir':
        return reproduzir(a.prova, a.janela, a.partes, lease, a.relatorios or pasta_relatorios() + '-reproducao',
                          a.paralelo)
    return tudo(a.janelas, lease, relatorios, a.saida, a.paralelo, a.partes, a.diagnostico_planejamento)


if __name__ == '__main__':
    sys.exit(main())
