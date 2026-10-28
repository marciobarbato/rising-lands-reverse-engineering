"""Original-only continuation and initialization-query captures before translation."""
import hashlib
import json
from pathlib import Path

from cenarios_classificacao_remapeamento import preparar_classificacao, CASOS_CLASSIFICACAO

RAIZ = Path(__file__).resolve().parents[1]
DESTINOS = ('capturas-classificacao-remapeamento-original.json',
            'capturas-consultas-inicializacao-original.json')


def _novo_destino(nome):
    destino = RAIZ/'relatorios'/nome
    if destino.exists():
        raise FileExistsError(f'Preserve the original-first capture: {destino}')
    return destino


def capturar_classificacao():
    destino = _novo_destino(DESTINOS[0])
    from bancada_classificacao_remapeamento import BancadaClassificacaoRemapeamento
    from vinculos_declarados import ParadaVinculoDeclarado
    from emulador import HASH_ORIGINAL
    b = BancadaClassificacaoRemapeamento(); casos = []
    for nome in CASOS_CLASSIFICACAO:
        m, nula, desconhecido, fonte = preparar_classificacao(nome)
        b.carregar_classificacao(m, nula, desconhecido)
        parada = None
        try: regs = b.classificar(); parada = hex(regs['EIP'])
        except ParadaVinculoDeclarado: parada = 'declared_lock_stop'
        casos.append(dict(name=nome, source=fonte, checkpoint=parada, output=b.resumo(m),
                          bindings=b.vinculos_declarados.eventos[:]))
    report = dict(original_sha256=HASH_ORIGINAL, translation_executed=False,
                  original_calls=dict(b.origens), bounded_segments=b.execucoes,
                  binding_resumptions=b.retomadas_vinculos, preserved_loop_resumptions=b.retomadas_laco,
                  import_resolutions=b.importacoes_declaradas, cases=casos,
                  scope='Two declared resource imports; intact reset/fill/obstacle/classification bodies; no labeling/cleanup or full MissionLoad')
    with destino.open('x') as arquivo:
        arquivo.write(json.dumps(report, indent=2)+'\n')
    print('Original classification cases:', len(casos), 'segments:', b.execucoes)


def capturar_consultas():
    destino = _novo_destino(DESTINOS[1])
    from emulador import BancadaX86, UNIDADES, HASH_ORIGINAL
    b = BancadaX86(); intervalos = [(0x442025,0x442045),(0x4422dd,0x4422e8),(0x4422da,0x4422dd)]
    b.cpu.mem_write(UNIDADES, b'\xa5'*220800)
    getters = []
    for indice in (0, 799):
        valores = []
        for tipo in range(256):
            b.cpu.mem_write(UNIDADES+indice*276+1, bytes([tipo]))
            antes = bytes(b.cpu.mem_read(UNIDADES,220800))
            regs = b.executar(0x442025, intervalos, dict(EAX=0xabcd0000|indice, EDX=0x12345678))
            assert regs['EDX'] == 0x12345678 and bytes(b.cpu.mem_read(UNIDADES,220800)) == antes
            valores.append(regs['EAX'] & 255)
        getters.append(dict(index=indice, al_hex=bytes(valores).hex()))
    monstros = []
    for tipo in range(256):
        regs = b.executar(0x4422dd, intervalos, dict(EAX=0xabcd0000|tipo, EDX=0x12345678))
        assert regs['EDX'] == 0x12345678
        monstros.append(regs['EAX'] & 255)
    report = dict(original_sha256=HASH_ORIGINAL, translation_executed=False, original_entries=b.execucoes,
                  getters=getters, monster_al=monstros, scope='Consumed AL only; getter retains complete unit pool and EDX')
    with destino.open('x') as arquivo:
        arquivo.write(json.dumps(report, indent=2)+'\n')
    print('Original initialization-query entries:', b.execucoes)


if __name__ == '__main__':
    for nome in DESTINOS:
        _novo_destino(nome)
    capturar_classificacao()
    capturar_consultas()
