"""Original-only first-frame combat captures over the M1 post-load input.

Input: the frozen accepted M1 `MissionLoad` oracle state (Missions'
`captura-carga-missao-original-v2.json`, `oracle.final_state.blocks`), mapped
read-only at its original addresses. Each case starts from a fresh copy of that
state; only the u32 frame counter `0x508f7c` may be declared per case. Nothing
from the Python reconstruction is imported. Writes
`evidencias/captura-quadro-m1-original.json`.

Cases are the Combat-relevant calls of the `CalculGame` frame body `0x42d2de`:
`PlayerAttaqueReset 0x46d628`, `ProjectileCalcul 0x46fc0f` and
`PlayerAttaqueCalculSympa 0x46d629`. `ProjectileAvance 0x46eaf8` and
`MAJSympathie 0x475118` are named stops: reaching them ends the case and is
recorded, never emulated through.
"""
import base64
import hashlib
import json
import struct
import sys
import zlib
from pathlib import Path

AQUI = Path(__file__).resolve().parent
REPO = AQUI.parents[1]
sys.path.insert(0, str(REPO / 'ferramentas'))

HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
ENTRADA_M1 = REPO / 'pesquisas-paralelas/missoes/evidencias/captura-carga-missao-original-v2.json'
DESTINO = AQUI / 'evidencias/captura-quadro-m1-original.json'
CONTADOR, PONTEIRO_POOL = 0x508f7c, 0x5080f0
PROJECTILE_CALCUL = [(0x46fc0f, 0x46fc8b), (0x46eaf4, 0x46eaf8), (0x46e528, 0x46e5fe)]
ROTINAS = {
    'PlayerAttaqueReset': (0x46d628, [(0x46d628, 0x46d629)], {}),
    'ProjectileCalcul': (0x46fc0f, PROJECTILE_CALCUL, {0x46eaf8: 'ProjectileAvance'}),
    'PlayerAttaqueCalculSympa': (0x46d629, [(0x46d629, 0x46d6a3)], {0x475118: 'MAJSympathie'}),
}
OBSERVADAS = {0x46e52c: 'ProjectileAnim'}
# Counter 0 is the M1 post-load value; counter 1 is the declared frame-1 value
# after GameNextFrame's increment (docs/AI_RUNTIME.md), pending the Missions
# frame-1 capture. Sympathy is also captured at its first periodic value.
CASOS = (
    dict(nome='reset-m1', rotina='PlayerAttaqueReset', contador=None),
    dict(nome='projectile-calcul-m1-counter0', rotina='ProjectileCalcul', contador=None),
    dict(nome='projectile-calcul-m1-counter1', rotina='ProjectileCalcul', contador=1),
    dict(nome='sympa-m1-counter1', rotina='PlayerAttaqueCalculSympa', contador=1),
    dict(nome='sympa-m1-counter2000', rotina='PlayerAttaqueCalculSympa', contador=2000),
)


def sha(dados):
    return hashlib.sha256(bytes(dados)).hexdigest()


def blocos_m1():
    d = json.loads(ENTRADA_M1.read_text())
    if d['original_sha256'] != HASH or not d['oracle']['reached_real_return'] or d['oracle']['al'] != 1:
        raise ValueError('M1 input is not the intact-EXE MissionLoad oracle with AL=1')
    blocos = {}
    for nome, b in d['oracle']['final_state']['blocks'].items():
        dados = zlib.decompress(base64.b64decode(b['zlib_base64']))
        if len(dados) != int(b['bytes']) or sha(dados) != b['sha256']:
            raise ValueError(f'M1 block {nome} fails its recorded size/hash')
        blocos[nome] = (int(b['base'], 16), dados)
    return sha(ENTRADA_M1.read_bytes()), blocos


class BancadaQuadroM1:
    def __init__(self, blocos):
        from emulador import BancadaX86, BASE, PILHA, RETORNO
        import unicorn
        from unicorn import x86_const
        self.x86, self.pilha, self.retorno = x86_const, PILHA, RETORNO
        self.b = BancadaX86()
        self.cpu = self.b.cpu
        imagem = (BASE, BASE + 0x200000)
        paginas = set()
        for base, dados in blocos.values():
            if imagem[0] <= base and base + len(dados) <= imagem[1]:
                continue
            paginas.update(range(base >> 12, (base + len(dados) + 0xfff) >> 12))
        for inicio, fim, _ in self.cpu.mem_regions():
            if any(inicio >> 12 <= p <= fim >> 12 for p in paginas):
                raise ValueError(f'M1 block overlaps harness region {inicio:#x}')
        for p in sorted(paginas):
            self.cpu.mem_map(p << 12, 0x1000)
        self.blocos = blocos
        self.escritas, self.instrucoes, self.observadas = [], 0, {}
        self.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, self._escrita)
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._codigo)

    def _escrita(self, cpu, _acesso, endereco, tamanho, valor, _):
        if not self.pilha <= endereco < self.pilha + 0x10000:
            self.escritas.append([hex(endereco), tamanho, hex(valor & ((1 << 8 * tamanho) - 1))])

    def _codigo(self, cpu, endereco, _tamanho, _):
        self.instrucoes += 1
        if endereco in OBSERVADAS:
            nome = OBSERVADAS[endereco]
            self.observadas[nome] = self.observadas.get(nome, 0) + 1

    def restaurar(self):
        for base, dados in self.blocos.values():
            self.cpu.mem_write(base, dados)
        self.escritas, self.instrucoes, self.observadas = [], 0, {}

    def ler(self, base, n):
        return bytes(self.cpu.mem_read(base, n))


def u32(dados, base, endereco):
    return struct.unpack_from('<I', dados, endereco - base)[0]


def capturar(bancada, caso):
    bancada.restaurar()
    dgroup_base, dgroup = bancada.blocos['dgroup']
    if caso['contador'] is not None:
        bancada.cpu.mem_write(CONTADOR, struct.pack('<I', caso['contador']))
    entrada, intervalos, paradas = ROTINAS[caso['rotina']]
    antes = {n: bancada.ler(b, len(d)) for n, (b, d) in bancada.blocos.items()}
    bancada.escritas, bancada.instrucoes, bancada.observadas = [], 0, {}
    regs = bancada.b.executar(entrada, intervalos, parada={bancada.retorno, *paradas}, limite_instrucoes=400000)
    parada = paradas.get(regs['EIP'])
    depois = {n: bancada.ler(b, len(d)) for n, (b, d) in bancada.blocos.items()}
    alteracoes = {}
    for nome, (base, _d) in bancada.blocos.items():
        mud = [[hex(base + k), antes[nome][k], depois[nome][k]]
               for k in range(len(antes[nome])) if antes[nome][k] != depois[nome][k]]
        if mud:
            alteracoes[nome] = mud
    pool = u32(dgroup, dgroup_base, PONTEIRO_POOL)
    return dict(caso, entrada=hex(entrada), contador_entrada=struct.unpack('<I', bancada.ler(CONTADOR, 4))[0]
                if caso['contador'] is None else caso['contador'],
                parada=dict(nome=parada, eip=hex(regs['EIP'])) if parada else None,
                retornou=regs['EIP'] == bancada.retorno,
                registradores_saida={n: hex(v) for n, v in regs.items() if n not in ('EIP', 'ESP')},
                esp_saida_relativo=regs['ESP'] - (bancada.pilha + 0x8000),
                instrucoes=bancada.instrucoes, chamadas_observadas=dict(bancada.observadas),
                escritas_ordenadas_fora_da_pilha=bancada.escritas,
                alteracoes_por_bloco=alteracoes,
                pool=dict(ponteiro=hex(pool), entrada_sha256=sha(fatia_pool(antes, bancada, pool)),
                          saida_sha256=sha(fatia_pool(depois, bancada, pool))),
                blocos_depois_sha256=sha(b''.join(depois[n] for n in sorted(depois))))


def fatia_pool(estado, bancada, ponteiro):
    for nome, (base, dados) in bancada.blocos.items():
        if base <= ponteiro and ponteiro + 5600 <= base + len(dados):
            return estado[nome][ponteiro - base:ponteiro - base + 5600]
    raise ValueError('Projectile pool is not inside one M1 block')


def main():
    entrada_sha, blocos = blocos_m1()
    bancada = BancadaQuadroM1(blocos)
    codigo_antes = sha(bancada.ler(0x401000, 0x93000))
    capturas = [capturar(bancada, caso) for caso in CASOS]
    if sha(bancada.ler(0x401000, 0x93000)) != codigo_antes:
        raise RuntimeError('Original code bytes changed during capture')
    relatorio = dict(
        rotulo='M1 post-load input', sha256_original=HASH,
        entrada=dict(caminho=str(ENTRADA_M1.relative_to(REPO)), sha256=entrada_sha,
                     parte='oracle.final_state.blocks', blocos=len(blocos),
                     bytes=sum(len(d) for _b, d in blocos.values())),
        origem='Original-only native runs; no Python reconstruction imported',
        fixture=('Every M1 block is restored at its original address before each case. Only u32 0x508f7c is '
                 'declared where a case names a counter. The harness stack/return address replace the caller '
                 'frame; these routines read no stack arguments. Code and image sections come from the intact EXE.'),
        rotinas={n: dict(entrada=hex(e), intervalos=[[hex(a), hex(b)] for a, b in i],
                         paradas_nomeadas={hex(k): v for k, v in p.items()}) for n, (e, i, p) in ROTINAS.items()},
        execucoes_x86=bancada.b.execucoes, capturas=capturas)
    DESTINO.write_text(json.dumps(relatorio, indent=1) + '\n')
    print(DESTINO.relative_to(REPO), bancada.b.execucoes,
          [(c['nome'], c['instrucoes'], c['parada'], len(c['escritas_ordenadas_fora_da_pilha'])) for c in capturas])


if __name__ == '__main__':
    main()
