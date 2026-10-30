"""Original-first S1 Economy gaps at real call sites, then a fresh native differential.

Use --grupo sac --capturar before creating the translation; default mode compares
all seven registers, ESP, ordered stores, full changed memory and sparse replay.
Each segment is bounded to 19 minutes and checked against replay-verified S1.
Snapshots: ferramentas.bancada_s1's ignored .local/m3 paths (see HANDOFF).
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import signal
import struct
import subprocess
import sys
import time

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
for p in (RAIZ / 'ferramentas', PASTA):
    sys.path.insert(0, str(p))
import bancada_s1 as bs
from bancada_ordens_economia import _gravador

GRUPOS = {'sac': (3750, 3854, ('SacGetCapacite',)),
          'tuyau': (1750, 1980, ('TuyauEstSortie',))}
REG7 = bs.REGISTROS
M32 = 0xffffffff


def caminho(grupo):
    return PASTA / f'evidencias/lacunas-s1/captura-{grupo}.json.xz'


def hash_arquivo(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def gravador(b, esp):
    from oraculo_carga_missao import DGROUP, DADOS_THREAD_CRT
    from emulador import PILHA
    a = b.arena
    regioes = (DGROUP, (DADOS_THREAD_CRT, DADOS_THREAD_CRT + 0x1000), (a.base, a.proximo),
               (PILHA, PILHA + 0x10000))
    g = _gravador(b, regioes, (PILHA, PILHA + 0x10000), True)
    return g, g.armar(esp)


def finalizar(b, g, hooks):
    for h in hooks:
        b.cpu.hook_del(h)
    b.cpu.ctl_flush_tb()
    if g.abertas:
        raise RuntimeError('Unclosed nested calls')
    return dict(read_before_write=g.leituras_em_runs(), stores=g.escritas, calls=g.chamadas)


class ObservacaoEconomia(bs.Observacao):
    def _entrada(self, nome):
        n = len(self.abertos)
        super()._entrada(nome)
        if len(self.abertos) > n:
            c = self.abertos[-1]
            c['recorder'] = gravador(self.b, c['regs']['ESP'])

    def _retorno(self, endereco):
        if self.ativo and self.abertos:
            c = self.abertos[-1]
            esp = self._regs()['ESP']
            if c['retorno'] == endereco and esp == c['regs']['ESP'] + 4 + self.rotinas[c['routine']]:
                self.extra = finalizar(self.b, *c['recorder'])
        super()._retorno(endereco)


def variantes(grupo, r, blocos):
    if grupo == 'sac':
        cel = r['EAX'] & 0xffff
        # All object types, quantities on each recognized sack, u16 cell wrap,
        # upper EAX/EDX and other preserved-register sentinels.
        m = lambda a: struct.unpack('<I', next(d[a-b:a-b+4] for b, d in blocos.values()
                                               if b <= a and a+4 <= b+len(d)))[0]
        tipos, quant = m(0x507d74), m(0x507dac)
        for t in range(256):
            yield f'object {t:#x}', dict(r, EAX=0xabcd0000 | cel), [(tipos+cel, bytes([t]))]
        for t in (0x42, 0x43, 0x44):
            for q in (0, 1, 127, 128, 255):
                yield f'sack {t:#x} quantity {q}', r, [(tipos+cel, bytes([t])), (quant+cel, bytes([q]))]
        for cel in (0, 0xffff):
            yield f'cell {cel:#x}, sentinels', dict(zip(REG7, (0x98760000|cel, 0x12345678, 0xfedcba98,
                                                   0xa55a7711, 0x13579bdf, 0x2468ace0, 0x99887766))), []


class Execucao:
    def __init__(self, grupo, comparar=None):
        self.grupo, self.comparar = grupo, comparar
        self.casos, self.pendentes, self.vistos = [], [], set()

    def registrar(self, caso, blocos):
        if self.comparar:
            caso['comparison'] = self.comparar(caso, blocos)
        self.casos.append(caso)

    def fechar(self, caso, blocos):
        caso.update(self.obs.extra)
        self.registrar(caso, blocos)
        chave = caso['routine']
        if chave not in self.vistos:
            self.vistos.add(chave)
            self.pendentes.append((caso, blocos))

    def executar(self):
        de, ate, rotinas = GRUPOS[self.grupo]
        inicio = time.monotonic()
        self.bancada = bs.BancadaS1(de)
        b = self.bancada.b
        self.obs = ObservacaoEconomia(b, {n: 0 for n in rotinas}, ao_fechar=self.fechar)
        while self.bancada.k < ate:
            self.bancada.avancar(self.obs)
            if self.pendentes:
                contexto, atual = b.cpu.context_save(), bs.imagem(b)
                self.obs.ativo = False
                try:
                    for c, blocos in self.pendentes:
                        r = {k: int(c['entry_registers'][k], 16) for k in REG7}
                        for label, regs, writes in variantes(self.grupo, r, blocos):
                            bs.restaurar(b, blocos)
                            esp = self.obs._regs()['ESP'] - 0x100
                            g, hooks = gravador(b, esp)
                            try:
                                caso, antes = bs.folha(b, c['routine'], regs, escritas=writes,
                                                       rotulo=label, quadro=c['frame'])
                            finally:
                                extra = finalizar(b, g, hooks)
                            caso.update(extra)
                            self.registrar(caso, antes)
                finally:
                    self.pendentes.clear()
                    bs.restaurar(b, atual)
                    b.cpu.context_restore(contexto)
                    self.obs.ativo = True
            if self.bancada.k % 50 == 0:
                print(self.bancada.k, len(self.casos), round(time.monotonic()-inicio, 1), flush=True)
        if self.obs.erros or not self.vistos == set(rotinas):
            raise RuntimeError((self.obs.erros, self.vistos))
        self.obs.remover()
        return round(time.monotonic()-inicio, 3)


def traduzir(caso, blocos=None):
    from lacunas_economia_s1 import LacunasEconomiaS1, provedor_lacunas_economia_s1
    from replay_ciclo_trabalho import MemoriaEsparsa
    entrada = {k: int(v, 16) for k, v in caso['entry_registers'].items()}
    entrada['ESP'] = int(caso['esp'], 16)
    m = MemoriaEsparsa(caso['read_before_write'])
    t = LacunasEconomiaS1(m)
    saida = t.chamar(caso['routine'], entrada)
    p = provedor_lacunas_economia_s1(LacunasEconomiaS1(MemoriaEsparsa(caso['read_before_write'])))
    servida = p(caso['routine'], int(caso.get('caller_return', '0'), 16)-5, entrada)
    esperado = {k: int(v, 16) for k, v in caso['exit_registers'].items()}
    dif = {k: [hex(saida[k]), hex(v)] for k, v in esperado.items() if saida[k] != v}
    finais = {}
    for s in caso['stores']:
        a, n, v = int(s[2], 16), s[3], int(s[4], 16)
        for i in range(n):
            finais[a+i] = v >> (i*8) & 255
    mud = {int(a,16): novo for a, _, novo in caso['changed_bytes']}
    bytes_ok = all(m.escritos.get(a, m.bytes.get(a)) == v for a, v in mud.items())
    stores_ok = all(finais.get(a, m.bytes.get(a)) == v for a, v in m.escritos.items())
    provedor_ok = all(servida[k] == esperado[k] for k in REG7)
    return dict(ok=not dif and bytes_ok and stores_ok and provedor_ok,
                register_differences=dif, changed_equal=bytes_ok, stores_equal=stores_ok, provider_equal=provedor_ok)


def main():
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    signal.alarm(1140)
    ap = argparse.ArgumentParser()
    ap.add_argument('--grupo', choices=GRUPOS, required=True)
    ap.add_argument('--capturar', action='store_true')
    a = ap.parse_args()
    cap = caminho(a.grupo)
    if a.capturar and cap.exists():
        raise FileExistsError(cap)
    referencia = None if a.capturar else json.loads(lzma.decompress(cap.read_bytes()))
    ex = Execucao(a.grupo, None if a.capturar else traduzir)
    segundos = ex.executar()
    por_rotina, mismatches = {}, []
    for i, c in enumerate(ex.casos):
        p = por_rotina.setdefault(c['routine'], dict(cases=0, in_situ=0, variants=0, mismatches=0))
        p['cases'] += 1
        p['in_situ' if c['kind']=='in_situ' else 'variants'] += 1
        if referencia is not None:
            r = c['comparison']
            r['native_equals_capture'] = i < len(referencia['cases']) and referencia['cases'][i] == {
                k:v for k,v in c.items() if k != 'comparison'}
            r['ok'] &= r['native_equals_capture']
            if not r['ok']:
                mismatches.append(dict(index=i, routine=c['routine'], comparison=r))
                p['mismatches'] += 1
    dados = dict(schema='rising-lands/economy-s1-gaps/1', original_sha256=HASH_ORIGINAL,
                 source_revision=subprocess.check_output(['git','rev-parse','HEAD'], cwd=RAIZ, text=True).strip(),
                 group=a.grupo, translation_executed=not a.capturar, seconds=segundos,
                 reproduction=ex.bancada.reproducao(), by_routine=por_rotina, cases=ex.casos)
    if a.capturar:
        dados['capture_script_sha256'] = hash_arquivo(__file__)
        cap.parent.mkdir(parents=True, exist_ok=True)
        cap.write_bytes(lzma.compress((json.dumps(dados, sort_keys=True)+'\n').encode()))
        saida = cap
    else:
        dados.update(comparisons=len(ex.casos), mismatches=mismatches,
                     rerun_equals_capture=len(ex.casos)==len(referencia['cases']) and
                       all(c['comparison']['native_equals_capture'] for c in ex.casos),
                     source_sha256={str(p.relative_to(RAIZ)): hash_arquivo(p) for p in
                                    (Path(__file__), PASTA/'lacunas_economia_s1.py')}, capture_sha256=hash_arquivo(cap))
        saida = PASTA / f'validacao-lacunas-s1-{a.grupo}-emulada.json'
        if mismatches:
            saida = RAIZ / f'.local/lacunas-s1-{a.grupo}-falha.json'
        saida.write_text(json.dumps(dados, indent=1, sort_keys=True)+'\n')
    print(json.dumps(dict(output=str(saida), by_routine=por_rotina, seconds=segundos), indent=1), flush=True)
    encerrar_captura(2 if mismatches else 0, saida)


if __name__ == '__main__':
    main()
