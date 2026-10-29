"""Original-only capture of the Core calls inside the forced first-raid frame (M2.3).

Combat's static trigger (``pesquisas-paralelas/combate/HANDOFF.md``, M2.3):
AvanceMonstre 0x47b283 spawns MONDE01's first monster group when the cycle
counter u32 0x508f7c reaches 9000. Its forced capture
(``captura-incursao-m2-3-original.json``) reruns Missions' committed frame
path with their read-only ``Isolamento`` and adds, at frame 1's AvanceMonstre
entry, a case that writes the counter. This script does the same for the
named scenario ('exibicao', the M2 reference; 'v1', Combat's scenario) and
declares more forced cases at that entry. Every other byte is the exact
frame-1 input:

* counter 9000 (Combat's case);
* counter 9000 with the world RNG u32 0x497164 set to declared seeds (projectile
  type parity, target player, cave/ambush/field choice, field cell);
* counter 10800 (records 0 and 1 both fire: two spawns);
* counter 9000 with record 0's cell (u16 0x50a9d0) moved to declared cells.

``read_before_write``/``changed_bytes`` are written in the lossless run encoding of
``compactar_captura_isolada`` (GetRandCaseChamps reads the whole 64 KiB type grid).

Inside each forced case, a nested recorder (armed only for that case) pauses
nothing. In one native pass it records every call to the Core routines below:
- entry and exit registers, and the six stack words after the return address;
- the enclosing recorded call;
- bytes read before written, with their values and reading routine;
- changed bytes (old, new).

It tracks the same regions as ``Isolamento`` (DGROUP+.bss, CRT thread page,
allocation arena, native stack). Stack bytes are excluded from changes. Stack
reads before any write are kept, including those below the exit ESP: a local
read before it is written holds residue from earlier calls, which is a real input. No Python translation is
imported.

    python3 -B ferramentas/capturar_incursao_core.py --cenario exibicao \
        --saida evidencias/fundacoes-quadro/captura-incursao-core-exibicao.json
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
CONTADOR, ALEATORIO, REGISTROS_MONSTROS = 0x508f7c, 0x497164, 0x50a9d0
CODIGO = (0x401000, 0x493c00)
# Core routines the raid frame reaches (Combat HANDOFF M2.3), their callees, and the cave branch's pick.
CORE = ('GetFreeCell', 'CreerEngin', 'EnginSetType', 'EnginSetTypeCaract', 'EnginTypeGetCapacite', 'EnginEnArret',
        'EnginSetPlayer', 'PlaceEngin', 'SetEnginCollision', 'SetCollision', 'Chemin_ModifieZone', 'SetMiniMap',
        'PlayerGetColor', 'TerrainEstIllumine', 'EnginGetCase', 'EnginGetType', 'GetRandCaseChamps',
        'GetRandCaseTypeBatPlayer', 'Chemin_Accessible', 'iaProbPost', 'iaProbNew', 'listNewElem',
        'listLinkElemToTail', 'Random', 'MissionGetNum', 'GetNumIndiceTypeBatiment', 'GetCaseIndiceBatiment')
SEMENTES = (0x00000001, 0x00000002, 0x00000003, 0x12345678, 0x2b5e0c3a, 0x3c6ef372, 0x5d1f00c7, 0x6a09e667,
            0x7ffffffe, 0x9e3779b9, 0xa54ff53a, 0xbb67ae85, 0xdeadbeef, 0xfffffffe, 0x00010001, 0x0badf00d)
CELULAS = (0x3e3e, 0x8080, 0x2e03, 0x4a20)
# Wall budgets: the isolated cases share frame 1's budget (the display bench takes ~91 s per case).
QUADRO_S, CASO_S = 600, 150
REGS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP', 'EIP')


def casos_forcados(limite=None):
    """The declared forced cases; ``limite`` keeps the first N (smoke runs only, never evidence)."""
    u32 = lambda v: list(struct.pack('<I', v))
    c = lambda nome, *escritas: dict(case=nome, writes=[(CONTADOR, u32(9000))] + list(escritas), registers={})
    casos = [c('counter9000')]
    casos += [c(f'counter9000_seed{s:08x}', (ALEATORIO, u32(s))) for s in SEMENTES]
    casos.append(dict(case='counter10800', writes=[(CONTADOR, u32(10800))], registers={}))
    casos += [c(f'counter9000_cell{x:04x}', (REGISTROS_MONSTROS, list(struct.pack('<H', x)))) for x in CELULAS]
    return casos[:limite]


class Gravador:
    """Nested per-call recorder over the four Isolamento regions; armed for one forced case at a time."""
    def __init__(self, bancada):
        self.b = bancada
        self.entradas = {bancada.sym[n]: n for n in CORE}
        self.pilha, self.chamadas, self.caso = [], [], None

    def armar(self, caso, regioes):
        import unicorn
        cpu = self.b.cpu
        self.caso, self.pilha = caso, []
        g = [cpu.hook_add(unicorn.UC_HOOK_CODE, self._entrada, begin=a, end=a) for a in sorted(self.entradas)]
        g.append(cpu.hook_add(unicorn.UC_HOOK_BLOCK, self._bloco, begin=CODIGO[0], end=CODIGO[1] - 1))
        for inicio, fim in regioes:
            g.append(cpu.hook_add(unicorn.UC_HOOK_MEM_READ, self._ler, begin=inicio, end=fim - 1))
            g.append(cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, self._escrever, begin=inicio, end=fim - 1))
        self.pilha_nativa = regioes[-1]
        return g

    def _regs(self, cpu):
        from unicorn import x86_const as x86
        return {r: cpu.reg_read(getattr(x86, 'UC_X86_REG_' + r)) for r in REGS}

    def _entrada(self, cpu, endereco, tamanho, _):
        regs = self._regs(cpu)
        palavras = struct.unpack('<7I', bytes(cpu.mem_read(regs['ESP'], 28)))
        self.pilha.append(dict(routine=self.entradas[endereco], entry=endereco, regs=regs, retorno=palavras[0],
                               stack=palavras[1:], parent=self.pilha[-1]['index'] if self.pilha else None,
                               index=len(self.chamadas), lidos={}, velhos={}))
        self.chamadas.append(None)

    def _bloco(self, cpu, endereco, tamanho, _):
        from unicorn import x86_const as x86
        while self.pilha and endereco == self.pilha[-1]['retorno'] and \
                cpu.reg_read(x86.UC_X86_REG_ESP) > self.pilha[-1]['regs']['ESP']:
            self._fechar(cpu, self.pilha.pop())

    def _ler(self, cpu, acesso, endereco, tamanho, valor, _):
        if not self.pilha:
            return
        dados = bytes(cpu.mem_read(endereco, tamanho))
        eip = None
        for f in self.pilha:
            for i in range(tamanho):
                a = endereco + i
                if a not in f['velhos'] and a not in f['lidos']:
                    if eip is None:
                        from unicorn import x86_const as x86
                        eip = cpu.reg_read(x86.UC_X86_REG_EIP)
                    f['lidos'][a] = (dados[i], eip)

    def _escrever(self, cpu, acesso, endereco, tamanho, valor, _):
        if not self.pilha:
            return
        dados = bytes(cpu.mem_read(endereco, tamanho))
        for f in self.pilha:
            for i in range(tamanho):
                f['velhos'].setdefault(endereco + i, dados[i])

    def _fechar(self, cpu, f):
        regs = self._regs(cpu)
        p0, p1 = self.pilha_nativa
        mudados = []
        for a in sorted(f['velhos']):
            if p0 <= a < p1:
                continue
            novo = cpu.mem_read(a, 1)[0]
            if novo != f['velhos'][a]:
                mudados.append([hex(a), f['velhos'][a], novo])
        # Stack reads before any write are kept, below the exit ESP too: a local read before it is
        # written is residue from earlier calls, a real input (GetFreeCell returns such upper words).
        leituras = [[hex(a), v, self.b.nome(eip)] for a, (v, eip) in sorted(f['lidos'].items())]
        self.chamadas[f['index']] = dict(
            case=self.caso, index=f['index'], routine=f['routine'], entry=hex(f['entry']),
            parent=f['parent'], caller=self.b.nome(f['retorno']), caller_return=hex(f['retorno']),
            entry_registers={k: hex(v) for k, v in f['regs'].items()}, stack_words=[hex(x) for x in f['stack']],
            exit_registers={k: hex(v) for k, v in regs.items()}, reached_return=regs['EIP'] == f['retorno'],
            changed_bytes=mudados, read_before_write=leituras)


def executar(cenario, limite=None):
    import percurso_quadro1 as pq
    from oraculo_quadro_missao import Isolamento
    from oraculo_carga_missao import DGROUP, DADOS_THREAD_CRT
    from emulador import PILHA
    b, cap = pq._bancada(cenario)
    gravador = Gravador(b)
    forcados = {c['case'] for c in casos_forcados(limite)}
    t0 = time.monotonic()
    estado = dict(caso=None)

    class IsolamentoGravado(Isolamento):
        def _rastrear(self, blocos):
            lidos, escritos, ganchos = super()._rastrear(blocos)
            nome = estado['caso']
            if nome in forcados:
                a = self.b.arena
                ganchos += gravador.armar(nome, ((DGROUP[0], DGROUP[1]), (DADOS_THREAD_CRT, DADOS_THREAD_CRT + 0x1000),
                                                 (a.base, a.proximo), (PILHA, PILHA + 0x10000)))
                self.b.cpu.ctl_flush_tb()
            return lidos, escritos, ganchos

    # Isolamento applies each case's writes before _rastrear; the observer runs after the case, so the
    # case order (captured inputs first, then the declared list) names the case being armed.
    ordem = []

    def observador(rotina, fase, caso, antes, resultado):
        if gravador.pilha:
            raise RuntimeError(f'Unclosed nested Core calls after case {caso["case"]}')
        ordem.append((rotina, fase, caso['case']))
        print(f'[{time.monotonic() - t0:8.1f}s] {rotina} {fase} {caso["case"]}: {len(resultado["changed_bytes"])} '
              f'changed, {sum(c is not None for c in gravador.chamadas)} Core calls', file=sys.stderr, flush=True)
        proximo = len([o for o in ordem if o[:2] == (rotina, fase)])
        lista = ['captured_inputs'] + [c['case'] for c in iso.perturbacoes.get(rotina, ())]
        estado['caso'] = lista[proximo] if proximo < len(lista) else None

    iso = IsolamentoGravado(b, ('AvanceMonstre',), {'(no routine)': []}, observador)
    iso.instalar()
    referencia = {p['phase']: p['state_after']['summary'] for p in cap['phases']}
    reproducao = {}
    for nome, correr in (('load_tail', lambda: b.executar_cauda_carga(600)),
                         ('between_frames', lambda: b.executar_entre_quadros(300)),
                         ('frame1', lambda: b.executar_quadro(QUADRO_S + CASO_S * len(casos_forcados(limite))))):
        if nome == 'frame1':
            iso.perturbacoes['AvanceMonstre'] = casos_forcados(limite)
        estado['caso'] = 'captured_inputs'
        correr()
        reproducao[nome] = b.resumo_imagem(b.imagem()) == referencia[nome]
        print(f'[{time.monotonic() - t0:8.1f}s] phase {nome} reproduced={reproducao[nome]}', file=sys.stderr, flush=True)
    reproducao['code_unchanged'] = b.sha256_codigo() == cap['code_integrity']['after']
    return b, iso, gravador, reproducao


def main():
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    from compactar_captura_isolada import compactar, expandir
    ap = argparse.ArgumentParser()
    ap.add_argument('--cenario', choices=('exibicao', 'v1'), required=True)
    ap.add_argument('--saida', required=True)
    ap.add_argument('--casos', type=int, help='smoke run: first N forced cases only (output under .local/ only)')
    a = ap.parse_args()
    if a.casos is not None and not a.saida.startswith('.local/'):
        raise SystemExit('A --casos smoke run writes under .local/ only')
    saida = RAIZ / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    revisao = subprocess.run(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    t0 = time.monotonic()
    try:
        b, iso, gravador, reproducao = executar(a.cenario, a.casos)
    except Exception as erro:          # recorded under .local/raid with its traceback, exit 2
        import traceback
        falha = RAIZ / '.local/raid' / ('incursao-core-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
        falha.parent.mkdir(parents=True, exist_ok=True)
        with open(falha, 'x') as f:
            json.dump(dict(scenario=a.cenario, forced_cases=len(casos_forcados(a.casos)), error=repr(erro),
                           traceback=traceback.format_exc(), seconds=round(time.monotonic() - t0, 3),
                           source_revision=revisao), f, indent=1)
        print(f'FAILED: {erro!r} -> {falha}', file=sys.stderr)
        encerrar_captura(2, falha)
    avance = [dict(phase=r['phase'], case=c['case'], reached_return=c['reached_return'],
                   changed=len(c['changed_bytes']), exit_eax=c['exit_registers']['EAX'])
              for r in iso.registros for c in r['cases']]
    chamadas = gravador.chamadas
    contagem = {}
    for c in chamadas:
        if c is not None:
            contagem[c['routine']] = contagem.get(c['routine'], 0) + 1
    import cenarios_oraculo
    import capturar_isolados_quadro1 as ci
    ref = cenarios_oraculo.caminho('exibicao', 'captura_quadro') if a.cenario == 'exibicao' else ci.CAPTURA
    relatorio = dict(
        schema='rising-lands/monde01-raid-core-calls/1', original_sha256=HASH_ORIGINAL, translation_executed=False,
        source_revision=revisao, scenario=a.cenario,
        reference=dict(path=str(Path(ref).relative_to(RAIZ)), sha256=hashlib.sha256(Path(ref).read_bytes()).hexdigest()),
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest()
                       for p in ('ferramentas/capturar_incursao_core.py', 'ferramentas/percurso_quadro1.py',
                                 'pesquisas-paralelas/missoes/oraculo_quadro_missao.py')},
        label='forced inputs at frame 1\'s AvanceMonstre entry: every other byte is the exact frame-1 input',
        forced_cases=[dict(case=c['case'], writes=[[hex(x), bytes(d).hex()] for x, d in c['writes']])
                      for c in casos_forcados(a.casos)],
        core_routines={n: hex(b.sym[n]) for n in CORE}, path_reproduction=reproducao, avance_monstre_cases=avance,
        counts=contagem, calls=[compactar(c) if c else None for c in chamadas],
        encoding=dict(scheme='rising-lands/isolated-call-runs/1', decoder='ferramentas/compactar_captura_isolada.py:expandir',
                      applies_to='calls[*].read_before_write and calls[*].changed_bytes'),
        method='nested recorder armed only during each forced AvanceMonstre case (Missions Isolamento, which '
               'restores the exact entry state after every case): code hooks at the Core entries, a code-range '
               'block hook for returns (return address with ESP above the entry ESP), read/write hooks over the '
               'Isolamento regions; values are read before each access',
        seconds=round(time.monotonic() - t0, 3))
    ok = (all(reproducao.values()) and all(x['reached_return'] for x in avance)
          and all(c is not None and c['reached_return'] for c in chamadas) and len(avance) == 1 + 1 + len(casos_forcados(a.casos)))
    if [expandir(c) if c else None for c in relatorio['calls']] != chamadas:
        raise RuntimeError('Run encoding is not lossless for this capture')
    if not ok:
        saida = RAIZ / '.local/raid' / ('incursao-core-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=None, sort_keys=True, separators=(',', ':'))
        f.write('\n')
    print(json.dumps(dict(output=str(saida), reproduction=reproducao, counts=contagem,
                          avance=[(x['case'], x['changed']) for x in avance], seconds=relatorio['seconds']), indent=1))
    encerrar_captura(0 if ok else 2, saida)


if __name__ == '__main__':
    main()
