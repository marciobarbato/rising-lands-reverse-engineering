"""Original-only ProjectileReset captures over deterministic dirty state.

Fixtures are generated from explicit seeds; the capture runs the intact EXE
and records whole-region digests and every changed byte. It does not import
any Python reconstruction. Writes `evidencias/captura-reinicio-projeteis-original.json`.
"""
import hashlib
import json
import random
from pathlib import Path

HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
GLOBAIS = (0x494000, 0x523000)
REGIOES_POOL = (0x1200000, 0x1f000000)
TAMANHO_REGIAO = 0x10000
FIM_REGIAO = TAMANHO_REGIAO - 5600
RETORNO_BANCADA, TOPO_PILHA = 0x3000000, 0x8000  # emulador.RETORNO; ESP_ENTRADA - PILHA
MASCARA_FLAGS = 0xcd5  # CF PF AF ZF SF DF OF; TF/IF stay clear in the harness
NOMES = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
CASOS = (
    dict(nome='random-pool-region0-start', semente=1, regiao=0, deslocamento=0),
    dict(nome='random-pool-region0-unaligned', semente=2, regiao=0, deslocamento=0x1235),
    dict(nome='random-pool-region0-end', semente=3, regiao=0, deslocamento=FIM_REGIAO),
    dict(nome='random-pool-high-region', semente=4, regiao=1, deslocamento=0x40),
    dict(nome='random-pool-high-region-end', semente=5, regiao=1, deslocamento=FIM_REGIAO),
    dict(nome='random-pool-region0-mid', semente=6, regiao=0, deslocamento=0x8000),
    dict(nome='plus2-values-0-99', semente=7, regiao=0, deslocamento=0x200, mais2=0),
    dict(nome='plus2-values-100-199', semente=8, regiao=1, deslocamento=0x200, mais2=100),
    dict(nome='plus2-values-200-255-wrap', semente=9, regiao=0, deslocamento=0x3000, mais2=200),
    dict(nome='pool-all-ff', semente=10, regiao=0, deslocamento=0x100, preencher=0xff),
    dict(nome='pool-already-clear-plus2', semente=11, regiao=1, deslocamento=0x100, mais2_zero=True),
    dict(nome='pool-all-zero', semente=12, regiao=0, deslocamento=0x100, preencher=0),
    dict(nome='call-MissionReStart', semente=21, regiao=0, deslocamento=0x400, chamador=0x46b5ac),
    dict(nome='call-GameLoad', semente=22, regiao=1, deslocamento=0x400, chamador=0x46b8c1),
    dict(nome='call-MissionLoad', semente=23, regiao=0, deslocamento=0x800, chamador=0x46c373),
    dict(nome='call-MissionLoadName', semente=24, regiao=1, deslocamento=0x800, chamador=0x46c623),
)


def entradas(caso):
    """Deterministic dirty state for one case; pool bytes live inside a dirty 64 KiB region."""
    rng = random.Random(caso['semente'])
    globais = rng.randbytes(GLOBAIS[1] - GLOBAIS[0])
    unidades = rng.randbytes(0x40000)
    pilha = bytearray(rng.randbytes(0x10000))
    if 'chamador' not in caso:
        pilha[TOPO_PILHA:TOPO_PILHA + 4] = RETORNO_BANCADA.to_bytes(4, 'little')
    regioes = {base: bytearray(rng.randbytes(TAMANHO_REGIAO)) for base in REGIOES_POOL}
    base = REGIOES_POOL[caso['regiao']]
    inicio = caso['deslocamento']
    regiao = regioes[base]
    if 'preencher' in caso:
        regiao[inicio:inicio + 5600] = bytes([caso['preencher']]) * 5600
    for i in range(100):
        if 'mais2' in caso:
            regiao[inicio + i * 56 + 2] = (caso['mais2'] + i) & 255
        elif caso.get('mais2_zero'):
            regiao[inicio + i * 56 + 2] = 0
    registradores = {nome: rng.getrandbits(32) for nome in NOMES}
    eflags = 2 | (rng.getrandbits(32) & MASCARA_FLAGS)
    return dict(globais=globais, unidades=unidades, pilha=pilha, regioes=regioes,
                ponteiro=base + inicio, registradores=registradores, eflags=eflags)


def sha(dados):
    return hashlib.sha256(bytes(dados)).hexdigest()


def diferencas(antes, depois):
    return [[k, antes[k], depois[k]] for k in range(len(antes)) if antes[k] != depois[k]]


def capturar(bancada, caso):
    e = entradas(caso)
    bancada.preparar(e['globais'], e['unidades'], e['pilha'], e['regioes'], e['ponteiro'])
    antes = bancada.instantaneo()
    saida = bancada.resetar(e['registradores'], e['eflags'], caso.get('chamador'))
    depois = bancada.instantaneo()
    base = REGIOES_POOL[caso['regiao']]
    pool_antes = antes[f'pool_{base:#x}'][caso['deslocamento']:caso['deslocamento'] + 5600]
    pool_depois = depois[f'pool_{base:#x}'][caso['deslocamento']:caso['deslocamento'] + 5600]
    return dict(caso, chamador=hex(caso['chamador']) if 'chamador' in caso else None,
        ponteiro=hex(e['ponteiro']),
        registradores_entrada={n: hex(v) for n, v in e['registradores'].items()},
        eflags_entrada=hex(e['eflags']),
        registradores_saida={n: hex(v) for n, v in saida.items()},
        pool=dict(entrada_sha256=sha(pool_antes), saida_sha256=sha(pool_depois),
                  mais2_nao_nulos=sum(1 for i in range(100) if pool_antes[i * 56 + 2])),
        regioes={nome: dict(antes_sha256=sha(antes[nome]), depois_sha256=sha(depois[nome]),
                            alteracoes=diferencas(antes[nome], depois[nome]))
                 for nome in antes})


def main():
    from bancada_reinicio_projeteis import BancadaReinicioProjeteis, ROTINA, RETORNO, ESP_ENTRADA, PILHA
    assert (RETORNO, ESP_ENTRADA - PILHA) == (RETORNO_BANCADA, TOPO_PILHA)
    bancada = BancadaReinicioProjeteis()
    capturas = [capturar(bancada, caso) for caso in CASOS]
    relatorio = dict(sha256_original=HASH, rotina=dict(nome='ProjectileReset', inicio=hex(ROTINA[0]),
            fim_exclusivo=hex(ROTINA[1])),
        origem='Original-only native runs captured before the Stage 17 Python entry; no reconstruction imported',
        fixture=('Deterministic Python random.Random(seed) bytes for DGROUP/.bss 0x494000..0x523000, the 256 KiB unit area, '
                 'the 64 KiB stack and two 64 KiB pool regions; pool pointer then written at 0x5080f0. '
                 'Dirty registers/flags are entry inputs. Direct entries return to the harness address; '
                 'caller entries execute the original 5-byte CALL and stop at its return address.'),
        execucoes_x86=bancada.execucoes, capturas=capturas)
    destino = Path(__file__).resolve().parent / 'evidencias/captura-reinicio-projeteis-original.json'
    destino.write_text(json.dumps(relatorio, indent=1) + '\n')
    print(destino, bancada.execucoes)


if __name__ == '__main__':
    main()
