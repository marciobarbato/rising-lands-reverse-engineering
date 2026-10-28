"""Fresh native comparison of AffGame in-game frames against compor_quadro.

Each scene runs the complete native frame (checked against the committed
original-only capture). When Python completes, the whole 800x600 surface,
canonical renderer trace, every prefix global, the cache state and the
complete writable-memory diff must match. When Python stops at a named
dependency, native memory is restored and rerun to that same original
address after the same trace event, and the partial state is compared.
"""
import hashlib
import json
import struct
import time
from extrair_evidencias import RAIZ, HASH_EXE, exigir_area_editavel
from graficos import Catalogo, png
from bancada_x86 import unicorn, SUPERFICIE, RETORNO
from bancada_quadro import BancadaQuadro, LIMITE_QUADRO, CHECKPOINT_HUD
from cenas_quadro import GLOBAIS, cenas_validacao, mundo_monde01, fundo, sha
from capturar_quadro import tabelas
from capturar_ciclo_cache import json_compacto, HASH_NORMALIZADO
from vinculos_graficos import RegistroVinculos
from ciclo_cache_terreno import CicloCacheTerreno, MemoriaMotor
from quadro_jogo import (compor_quadro, EstadoTela, MundoQuadro, DependenciaQuadro, GLOBAIS_QUADRO)

CURSOR_CACHE = 0x49a04e


def canonico(evento):
    """Native [name, i16 EAX, i16 EDX, EBX] -> the model's trace row."""
    nome, eax, edx, ebx = evento
    if nome in ('CalculFrame', 'DDLockSurface', 'AffBloc', 'Box'): return [nome]
    if nome in ('AffTerrain', 'AffSprite'): return [nome, eax, edx]
    if nome == 'GetNumBob': return [nome, eax & 0xffff, edx & 0xffff]
    if nome == 'AffProjectile': return [nome, eax & 0xffff]
    return [nome, eax, edx, ebx]


class DirectDrawModelo:
    def __init__(self): self.chamadas = []
    def is_lost(self): self.chamadas.append('IsLost'); return 0
    def lock(self): self.chamadas.append('Lock'); return 0, SUPERFICIE


def mundo_modelo(cena):
    m = cena['mundo']
    return MundoQuadro(terreno=m['terreno'], objetos=m['objetos'], auxiliares=m['auxiliares'], regioes=m['regioes'],
        unidades=m['unidades'], projeteis=m['projeteis'], descoberta=m['descoberta'], iluminacao=m['iluminacao'])


def globais_nativas(b):
    return {nome: b.ler(endereco, largura) for nome, endereco, largura in GLOBAIS}


def restaurar(b, foto):
    for nome, inicio, n in b.regioes_mutaveis(): b.escrever(inicio, foto[nome])


def permitido(diff):
    """Every native write outside surface/cache must be a prefix global or the cache cursor."""
    faixas = [(a, a+w) for n, a, w in GLOBAIS]+[(CURSOR_CACHE, CURSOR_CACHE+2)]
    for regiao, corridas in diff.items():
        if regiao != 'dados': return False
        for deslocamento, antigo, novo in corridas:
            for i in range(len(antigo)//2):
                endereco = 0x494000+deslocamento+i
                if antigo[2*i:2*i+2] != novo[2*i:2*i+2] and not any(a <= endereco < z for a, z in faixas): return False
    return True


def comparar_estado(b, tela, ciclo, superficie, rotulo):
    nativo = globais_nativas(b)
    assert nativo == tela.instantaneo(), (rotulo, {k: (nativo[k].hex(), tela.instantaneo()[k].hex()) for k in nativo if nativo[k] != tela.instantaneo()[k]})
    estado = b.estado()
    assert estado['chaves'] == ciclo.registros and estado['blocos'] == ciclo.blocos_crus and estado['cursor_u16'] == ciclo.proximo_u16, rotulo
    assert b.ler(SUPERFICIE, 800*600) == superficie, rotulo


def validar():
    exigir_area_editavel(); inicio = time.monotonic(); catalogo = Catalogo(); sombra, eclairage = tabelas()
    captura = json.loads((RAIZ/'evidencias/captura-quadro-original.json').read_text())
    capturados = {f['nome']: f for f in captura['frames']}
    assert [n for n, a, w in GLOBAIS] == [n for n, a, w in GLOBAIS_QUADRO] and GLOBAIS == GLOBAIS_QUADRO
    b = BancadaQuadro(catalogo)
    memoria = MemoriaMotor(contador_u32=b.u32(0x4e2f3c), vinculos=b.arena.derivar(registro=RegistroVinculos()))
    fixture_alloc = dict(arena_next=b.arena.proximo, arena_end=b.arena.fim, counter_u32=memoria.contador_u32)
    ciclo = CicloCacheTerreno.apos_carregar_banco(catalogo); _, log = b.cache_alloc(); ciclo.alocar(memoria)
    assert memoria.vinculos.registro.desde(0) == log == captura['cache_alloc'] and b.u32(0x49a050) == ciclo.ponteiro_chaves_u32
    jogadores = b.calcular_tabelas_jogador()
    registros = {t: b.inicializar_tipo(t) for t in (0, 2, 5, 6, 7, 9)}
    assert {str(t): r.hex() for t, r in registros.items()} == captura['unit_initializer_records']
    base = mundo_monde01(); cenas = cenas_validacao(base, registros)
    relatorio = []
    for cena in cenas:
        if cena['antes'] == 'InitCache':
            r = b.init_cache(); assert r['EAX'] == ciclo.iniciar() == 256
        b.carregar_cena(cena, tabela_sombra=sombra, tabela_eclairage=eclairage, fundo=fundo(), globais_nomes=GLOBAIS)
        foto = b.fotografia(); nativo = b.quadro(ticks=list(cena['ticks'])); depois = b.fotografia()
        diff = b.diferencas(foto, depois, ignorar=('superficie', 'arena'))
        rastro = [canonico(e) for e in nativo['rastro']]
        if cena['nome'] in capturados:
            c = capturados[cena['nome']]
            assert sha(json.dumps(nativo['rastro'], separators=(',', ':')).encode('ascii')) == c['rastro']['sha256']
            assert sha(depois['superficie']) == c['superficie_sha256'] and diff == c['escritas'] and hex(nativo['eip']) == c['parada']
        assert permitido(diff), (cena['nome'], diff)
        tela = EstadoTela(cena['globais']); modelo_dd = DirectDrawModelo(); ticks = list(cena['ticks'])
        try:
            q = compor_quadro(mundo_modelo(cena), tela, ciclo_cache=ciclo, catalogo=catalogo, tabela_sombra=sombra,
                tabela_eclairage=eclairage, superficie=fundo(), relogio=lambda: ticks.pop(0), directdraw=modelo_dd)
            parada = None
        except DependenciaQuadro as erro:
            q = None; parada = erro
        linha = dict(cena=cena['nome'], antes=cena['antes'], native=dict(stop=hex(nativo['eip']), instructions=nativo['instrucoes'],
            events=len(rastro), surface_sha256=sha(depois['superficie'])))
        if parada is None:
            assert rastro == q['chamadas'], (cena['nome'], next((i, a, m) for i, (a, m) in enumerate(zip(rastro, q['chamadas'])) if a != m))
            assert q['parada'] == (CHECKPOINT_HUD if nativo['eip'] == CHECKPOINT_HUD else 'retorno') and q['desenhado'] == (nativo['eip'] == CHECKPOINT_HUD)
            comparar_estado(b, tela, ciclo, q['superficie'], cena['nome'])
            linha.update(model='complete', comparison='whole frame through '+('0x417b1c' if q['desenhado'] else 'AffGame return'),
                surface_sha256=sha(q['superficie']), effects=[list(e) for e in q['efeitos']],
                trace=dict(events=len(q['chamadas']), sha256=sha(json.dumps(q['chamadas'], separators=(',', ':')).encode('ascii'))))
        else:
            # Restore the pre-frame native state and stop at the model's original address.
            restaurar(b, foto); indice = len(parada.chamadas)-1
            parcial = b.quadro(ticks=list(cena['ticks']), parar_evento=indice, parar_endereco=parada.endereco)
            assert [canonico(e) for e in parcial['rastro']] == parada.chamadas, cena['nome']
            comparar_estado(b, tela, ciclo, parada.superficie, cena['nome'])
            linha.update(model='named_stop', stop=hex(parada.endereco), detail=parada.detalhe, stop_event=parada.chamadas[-1],
                comparison='partial state at the same original address after trace event %d' % indice,
                partial_native_instructions=parcial['instrucoes'], surface_sha256=sha(parada.superficie),
                effects=[list(e) for e in parada.efeitos],
                trace=dict(events=len(parada.chamadas), sha256=sha(json.dumps(parada.chamadas, separators=(',', ':')).encode('ascii'))))
        if cena['nome'] == 'monde01_checkpoint':
            # Preview of the first real-mission partial frame: the 25x17-cell window, original palette.
            paleta = catalogo.paleta(); janela = parada.superficie[:800*544]
            (RAIZ/'artefatos/quadro-monde01-parcial.png').write_bytes(png(800, 544, bytes(v for i in janela for v in (*paleta[i*3:i*3+3], 255))))
        linha['cache'] = dict(cursor=ciclo.proximo_u16, keys_sha256=sha(ciclo.registros), payload_sha256=sha(ciclo.blocos_crus))
        relatorio.append(linha); print('Native/Python frame', cena['nome'], linha['model'], linha.get('stop', ''), flush=True)
    report = dict(exe_sha256=HASH_EXE, analysis_pe_sha256_not_executed=HASH_NORMALIZADO, unicorn_version=unicorn.__version__,
        result='PASS', limits=LIMITE_QUADRO, checkpoint=hex(CHECKPOINT_HUD),
        bindings=dict(iat_resolution=b.resolucao_iat, directdraw='IDirectDrawSurface IsLost/Lock (Restore/Unlock stop) via COM object 0x4E1790',
            model_side='DirectDrawModelo returns DD_OK and the same fixture surface address; GetTickCount uses the same declared ticks'),
        cache_alloc_fixture=fixture_alloc, player_tables_sha256=[sha(t) for t in jogadores], frames=relatorio,
        totals=dict(native_entries=b.execucoes, instructions_observed=b.instrucoes, bound_calls=b.registro.marca(), frames=len(relatorio),
            complete=sum(1 for l in relatorio if l['model'] == 'complete'), named_stops=sum(1 for l in relatorio if l['model'] == 'named_stop')),
        expected_limits=0, skips=0, seconds=round(time.monotonic()-inicio, 3))
    (RAIZ/'validacao/x86-quadro-jogo.json').write_text(json_compacto(report)+'\n')
    print('PASS:', report['totals'], flush=True)


if __name__ == '__main__': validar()
