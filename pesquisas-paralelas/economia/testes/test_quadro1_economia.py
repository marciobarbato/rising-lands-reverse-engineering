"""Economy frame calls at the exact MONDE01 frame-0/1 inputs against isolated original captures.

Each frozen case was captured natively from the exact entry state of the
first-frame path (Missions' frame bench, ``capturar_quadro1_economia_original``)
of a named oracle scenario: ``v1`` (display skipped) and ``exibicao`` (display
executed, the M2 reference). Python starts from that scenario's post-MissionLoad
memory overlaid with every byte the call
read before writing and every changed byte's entry value, runs the
translation, and must produce exactly the native set of changed bytes and the
native result register. For routines that read only through ``ler`` and
write only through ``vista``, the bytes read before written must equal the
native set exactly.
``RISING_EMULAR=1`` reruns the native captures and requires them to equal the frozen files.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PASTA = Path(__file__).resolve().parents[1]
RAIZ = PASTA.parents[1]
sys.path.insert(0, str(PASTA))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import quadro_economia as q  # noqa: E402
from test_quadro_economia import Memoria, Provedores, blocos as blocos_m1  # noqa: E402

PILHA = 0x2000000   # emulador.PILHA: the frame bench's native stack (0x10000 bytes)

CAPTURA = PASTA / 'evidencias/captura-quadro1-economia-original-v2.json'
CAPTURA_V1 = PASTA / 'evidencias/captura-quadro1-economia-original.json'
CAPTURA_EXIBICAO = PASTA / 'evidencias/captura-quadro1-economia-exibicao.json'
CAPTURA_CONSULTAS = PASTA / 'evidencias/captura-consultas-economia-exibicao-v2.json'
# v1 of the query capture (882c20c) lacks the caller-frame stack writes, so IntToBCD's output into its
# caller's buffer was not recorded; it is kept and must equal v2 without those fields.
CAPTURA_CONSULTAS_V1 = PASTA / 'evidencias/captura-consultas-economia-exibicao.json'
CAPTURAS = {'v1': CAPTURA, 'exibicao': CAPTURA_EXIBICAO, 'consultas': CAPTURA_CONSULTAS}
# Missions' artifact set each capture was recorded on: the frozen display captures predate Missions'
# Stage18 backend switch, so they replay over the Stage17 artifacts (now ``exibicao_interino``); fresh
# reruns use the current ``exibicao`` (v2) reference and must still equal them. ``campos`` is v2.
CENARIO_DA_CAPTURA = {'v1': 'v1', 'exibicao': 'exibicao_interino', 'consultas': 'exibicao_interino',
                      'campos': 'exibicao'}
_BASES = {}
SO_VISTA = {'RechercheCalcul', 'PlayerInitAllianceCompteur', 'CalculMatiere', 'CalculCompteurMarche',
            'CalculCompteurProposition', 'PlayerAttaqueCalculSympa', 'MAJSympathie', 'ResetTableauHangar',
            'EnginNextEtape:state7'}


def evidencia(cenario='v1'):
    return json.loads(CAPTURAS[cenario].read_text())


def base_cenario(cenario):
    """Post-MissionLoad blocks of the scenario (None = the accepted M1 state of test_quadro_economia)."""
    cenario = CENARIO_DA_CAPTURA.get(cenario, cenario)
    if cenario == 'v1':
        return None
    if cenario not in _BASES:
        # ambiente_missoes puts other fronts' folders ahead of economia (graficos-animacao also has a
        # construcoes.py): restore the path once Missions' loaders are imported.
        caminho = list(sys.path)
        sys.path.insert(0, str(RAIZ / 'pesquisas-paralelas/missoes'))
        try:
            import cenarios_oraculo
            from mapa_memoria_m1 import carregar_blocos, carregar_json, expandir_captura
        finally:
            # Keep economia's priority but keep the folders the imports added: cached modules such as
            # ambiente_missoes will not add them again (Missions' carregador_cabecalho needs graficos' sequenciais).
            sys.path[:] = caminho + [p for p in sys.path if p not in caminho]
        captura = expandir_captura(carregar_json(cenarios_oraculo.caminho(cenario, 'captura_m1')),
                                   carregar_json(cenarios_oraculo.caminho(cenario, 'entrada')))
        final = captura['oracle']['final_state']
        quadro = carregar_json(cenarios_oraculo.caminho(cenario, 'captura_quadro'))
        if final['summary'] != quadro['state_s0']['summary']:
            raise ValueError(f'{cenario}: MissionLoad final state is not the frame capture S0')
        _BASES[cenario] = [(nome, base, dados) for nome, (base, dados) in carregar_blocos(final['blocks']).items()]
    return _BASES[cenario]


def executar(nome, m, p, regs):
    """Run the translation for one isolated case; return the value comparable to native EAX, or None."""
    from bonus_unidades import BonusUnidades
    from construcoes_habitaveis import celula_central_estrutura
    from limpeza_saida import bag_contient_troupe
    if nome == 'RechercheCalcul':
        q.calcular_pesquisa(m)
    elif nome == 'PlayerInitAllianceCompteur':
        q.contar_aliancas(m)
    elif nome == 'SetUpdateChamp':
        q.agendar_campos(m, p.recursos)
    elif nome == 'UpdateChamp':
        q.atualizar_campos(m, p.recursos)
    elif nome == 'CalculMatiere':
        q.calcular_materia(m)
    elif nome == 'CalculCompteurMarche':
        q.calcular_contador_mercado(m, regs['EAX'])
    elif nome == 'CalculCompteurProposition':
        q.calcular_contador_proposicao(m, regs['EAX'], regs['EDX'])
    elif nome == 'PlayerAttaqueCalculSympa':
        q.calcular_simpatia_ataques(m)
    elif nome == 'MAJSympathie':
        q.atualizar_simpatia(m, regs['EAX'], regs['EDX'], regs['EBX'])
    elif nome == 'ResetTableauHangar':
        q.resetar_tabela_hangar(m)
    elif nome == 'EnginNextEtape:state7':
        q.estado_parado_unidade(m, regs['EDI'])
    elif nome == 'BatimentNextEtape:type1_2_13_16':
        q.ramo_producao_estrutura(p.producao, regs['EDI'], p.calcular_tropa)
    elif nome == 'CalculTroupe':
        p.producao.calcular_tropa(regs['EAX'])
    elif nome == 'BonusGetValEngin':
        b = BonusUnidades.da_memoria(m)
        return 0xffff, b.consultar(regs['EAX'], regs['EBX'], regs['EDX'], ecx=regs['ECX'])
    elif nome == 'BagContientTroupe':
        indice, resto = divmod(regs['EAX'] - 0x49a0d4, 276)
        assert resto == 0
        return 0xff, int(bag_contient_troupe(p.producao.recrutamento, indice))
    elif nome == 'BatimentGetCase':
        return 0xffff, celula_central_estrutura(m.vista(0x49a0c8, 276000), regs['EAX'])
    elif nome in CONSULTAS:
        return executar_consulta(nome, m, p, regs)
    else:
        raise AssertionError(f'No translation mapped for {nome}')
    return None


def argumento_pilha(regs):
    """TestRessource's player: the first byte of the callee-popped stack argument."""
    return bytes.fromhex(regs['stack_arguments'])[0]


def executar_consulta(nome, m, p, regs):
    """The existing class forms bound live (Mercado/Economia.da_memoria), or the quadro_economia functions."""
    from consultas_reinicio_economia import tipo_estrutura
    from construcoes_habitaveis import estrutura_habitada
    from mercado import Mercado
    if nome == 'PlayerGetType':
        return 0xff, Mercado.da_memoria(m).tipo_jogador(regs['EAX'])
    if nome == 'PlayerEstAllie':
        return 0xff, Mercado.da_memoria(m).aliado(regs['EAX'], regs['EDX'])
    if nome == 'TestRessource':
        e = Mercado.da_memoria(m).economia
        return 0xff, int(e.suficiente(argumento_pilha(regs), regs['EAX'], regs['EDX'], regs['EBX']))
    if nome == 'BatimentGetType':
        return 0xff, tipo_estrutura(m.vista(0x49a0c8, 276000), regs['EAX'])
    if nome == 'BatimentEstHabiter':
        return 0xff, estrutura_habitada(p.producao, regs['EAX'])
    if nome == 'IntToBCD':
        return q.escrever_bcd(m, regs['EAX'], regs['EDX'])
    if nome == 'BCDToInt':
        return q.ler_bcd(m, regs['EAX'], regs['EDX'])
    if nome == 'BagVide':
        return 0xffffffff, q.bolsa_vazia(m, regs['EAX'])
    raise AssertionError(nome)


CONSULTAS = {'PlayerGetType', 'PlayerEstAllie', 'TestRessource', 'BatimentGetType', 'BatimentEstHabiter',
             'IntToBCD', 'BCDToInt', 'BagVide'}
SO_VISTA_CONSULTAS = {'IntToBCD', 'BCDToInt', 'BagVide'}


def funcoes_vivas(nome, m, p, regs):
    """The quadro_economia live-memory query functions (the providers' bodies) over ler/vista."""
    funcoes = {
        'PlayerGetType': (lambda: q.tipo_jogador(m, regs['EAX']), 0xff),
        'PlayerEstAllie': (lambda: q.aliado(m, regs['EAX'], regs['EDX']), 0xff),
        'TestRessource': (lambda: q.recursos_suficientes(m, argumento_pilha(regs), regs['EAX'], regs['EDX'],
                                                         regs['EBX']), 0xff),
        'BatimentGetType': (lambda: q.tipo_estrutura_viva(m, regs['EAX']), 0xff),
    }
    if nome not in funcoes:
        return executar_consulta(nome, m, p, regs)
    funcao, mascara = funcoes[nome]
    return mascara, funcao()


LER_VISTA_VIVAS = CONSULTAS - {'BatimentEstHabiter'}


class MemoriaPalavras:
    """Only u8/u16/u32(endereco, valor=None), like ai-runtime's MemoriaDeclarada."""
    def __init__(self, m):
        self.m = m

    def _acesso(self, largura, endereco, valor):
        v = self.m.vista(endereco, largura)
        if valor is None:
            return int.from_bytes(v, 'little')
        v[:] = (valor & ((1 << 8 * largura) - 1)).to_bytes(largura, 'little')
        return valor

    def u8(self, endereco, valor=None):
        return self._acesso(1, endereco, valor)

    def u16(self, endereco, valor=None):
        return self._acesso(2, endereco, valor)

    def u32(self, endereco, valor=None):
        return self._acesso(4, endereco, valor)


def via_provedores(nome, m, p, regs):
    """The same case through provedores_economia_quadro over a u8-only memory."""
    from bonus_unidades import BonusUnidades
    from provedores_economia_quadro import provedores_economia_quadro
    prov = provedores_economia_quadro(MemoriaPalavras(m), bonus=BonusUnidades.da_memoria(m), producao=p.producao,
                                      recursos=p.recursos, calcular_tropa=p.calcular_tropa)
    chamadas = {
        'EnginNextEtape:state7': ('EnginNextEtape:estado7', dict(unidade=regs['EDI']), None),
        'BatimentNextEtape:type1_2_13_16': ('BatimentNextEtape:tipo1_2_13_16', dict(estrutura=regs['EDI']), None),
        'BagContientTroupe': (nome, dict(bolsa=regs['EAX']), 0xff),
        'CalculTroupe': (nome, dict(estrutura=regs['EAX']), None),
        'BatimentGetCase': (nome, dict(estrutura=regs['EAX']), 0xffff),
        'BonusGetValEngin': (nome, dict(jogador=regs['EAX'], tipo=regs['EBX'], seletor=regs['EDX'], ecx=regs['ECX']),
                             0xffff),
        'MAJSympathie': (nome, dict(jogador=regs['EAX'], outro=regs['EDX'], evento=regs['EBX']), None),
        'CalculCompteurMarche': (nome, dict(jogador=regs['EAX']), None),
        'CalculCompteurProposition': (nome, dict(jogador=regs['EAX'], edx=regs['EDX']), None),
        'PlayerGetType': (nome, dict(jogador=regs['EAX']), 0xff),
        'PlayerEstAllie': (nome, dict(jogador=regs['EAX'], outro=regs['EDX']), 0xff),
        'TestRessource': (nome, dict(jogador=argumento_pilha(regs) if nome == 'TestRessource' else None,
                                     comida=regs['EAX'], pedra=regs['EDX'], pecas=regs['EBX']), 0xff),
        'BatimentGetType': (nome, dict(estrutura=regs['EAX']), 0xff),
        'BatimentEstHabiter': (nome, dict(estrutura=regs['EAX']), 0xff),
        'IntToBCD': (nome, dict(destino=regs['EAX'], valor=regs['EDX']), None),
        'BCDToInt': (nome, dict(destino=regs['EAX'], origem=regs['EDX']), None),
        'BagVide': (nome, dict(bolsa=regs['EAX']), 0xffffffff),
    }
    rotina, argumentos, mascara = chamadas.get(nome, (nome, {}, None))
    resultado = prov[rotina](sitio=0, **argumentos)
    return None if mascara is None else (mascara, resultado)


def comparar(teste, executor=None, cenario='v1'):
    executor = executor or executar
    total = 0
    fonte = base_cenario(cenario)
    for r in evidencia(cenario)['calls']:
        nome = r['routine']
        rotulo = f"{cenario}:{r['phase']}:{nome}:{total}"
        pilha_mudada = r.get('caller_stack_changes', [])
        pilha_inalterada = r.get('caller_stack_written_unchanged', [])
        enderecos = [int(e[0], 16) for campo in ('read_before_write', 'changed_bytes', 'written_unchanged')
                     for e in r[campo]] + [int(e[0], 16) for e in pilha_mudada + pilha_inalterada]
        if any(PILHA <= a < PILHA + 0x10000 for a in enderecos):
            # Caller buffers on the bench stack (IntToBCD/BCDToInt): only the recorded bytes are filled
            # in below; the exact read-set check rejects any other stack read.
            m = Memoria((fonte or blocos_m1()) + [('native_stack', PILHA, bytes(0x10000))])
        else:
            m = Memoria(fonte)
        conhecidos = set()
        for a, v, _ in r['read_before_write']:
            teste.assertIsNotNone(v, rotulo)
            m.escrever(int(a, 16), bytes([v]))
            conhecidos.add(int(a, 16))
        for a, velho, _ in r['changed_bytes']:
            m.escrever(int(a, 16), bytes([velho]))
            conhecidos.add(int(a, 16))
        for a, valor in r['written_unchanged'] + pilha_inalterada:
            m.escrever(int(a, 16), bytes([valor]))
        for a, velho, _ in pilha_mudada:
            m.escrever(int(a, 16), bytes([velho]))
        p = Provedores(m)
        antes = [bytes(raw) for _, _, raw in m.blocos]
        regs = {k: int(v, 16) for k, v in r['entry_registers'].items()}
        if 'stack_arguments' in r:
            regs['stack_arguments'] = r['stack_arguments']
        m.leituras.clear()
        m.ordem_acessos.clear()
        resultado = executor(nome, m, p, regs)
        mudados = {}
        for (_, base, raw), velho in zip(m.blocos, antes):
            if raw != velho:
                mudados.update({base + i: raw[i] for i in range(len(raw)) if raw[i] != velho[i]})
        teste.assertEqual(mudados, {int(a, 16): novo for a, _, novo in r['changed_bytes'] + pilha_mudada}, rotulo)
        if resultado is not None:
            mascara, valor = resultado
            teste.assertEqual(valor & mascara, int(r['exit_registers']['EAX'], 16) & mascara, rotulo)
        if ((executor is executar and (nome in SO_VISTA or nome in SO_VISTA_CONSULTAS))
                or (executor is funcoes_vivas and nome in LER_VISTA_VIVAS)):
            # These routines read only through ler and write only through vista: their bytes read
            # before written must be exactly the native ones.
            lidos, escritos = set(), set()
            for tipo, e, n in m.ordem_acessos:
                faixa = set(range(e, e + n))
                if tipo == 'ler':
                    lidos |= faixa - escritos
                else:
                    escritos |= faixa
            teste.assertEqual(lidos, {int(a, 16) for a, _, _ in r['read_before_write']}, rotulo)
        if nome == 'BatimentNextEtape:type1_2_13_16':
            teste.assertEqual(p.tropas, [regs['EDI'] & 0xffff], rotulo)
        total += 1
    return total


class ContratosQuadro1Economia(unittest.TestCase):
    def test_frozen_capture_precedes_translation_and_reproduces_the_frame_path(self):
        r = evidencia()
        self.assertFalse(r['translation_executed'])
        self.assertTrue(r['path_reproduction']['passed'])
        self.assertTrue(all(c['reached_exit'] for c in r['calls']))
        frame = RAIZ / r['frame_capture']['path']
        self.assertEqual(hashlib.sha256(frame.read_bytes()).hexdigest(), r['frame_capture']['sha256'])
        self.assertEqual(len(r['calls']), 102)
        self.assertEqual(hashlib.sha256(CAPTURA.read_bytes()).hexdigest(), SHA_CAPTURA)
        v1 = json.loads(CAPTURA_V1.read_text())['calls']
        self.assertEqual([{k: v for k, v in c.items() if k != 'written_unchanged'} for c in r['calls']], v1)

    def test_python_reproduces_every_exact_frame_call(self):
        self.assertEqual(comparar(self), 102)

    def test_providers_over_word_memory_reproduce_every_exact_frame_call(self):
        self.assertEqual(comparar(self, via_provedores), 102)

    def test_providers_cover_every_validated_routine(self):
        from provedores_economia_quadro import provedores_economia_quadro
        from bonus_unidades import BonusUnidades
        m = Memoria()
        p = Provedores(m)
        nomes = set(provedores_economia_quadro(m, bonus=BonusUnidades.da_memoria(m), producao=p.producao,
                                               recursos=p.recursos))
        renomeados = {'EnginNextEtape:state7': 'EnginNextEtape:estado7',
                      'BatimentNextEtape:type1_2_13_16': 'BatimentNextEtape:tipo1_2_13_16'}
        capturados = {renomeados.get(c['routine'], c['routine'])
                      for cap in ('v1', 'exibicao', 'consultas') for c in evidencia(cap)['calls']}
        # Validated by their own captures: RechercheGetNbInvention (captura-invencoes-original), GetMeteo
        # (captura-temporizadores-original) and PlayerGetColor (captura-cor-jogador-original).
        self.assertEqual(nomes - capturados, {'RechercheGetNbInvention', 'GetMeteo', 'PlayerGetColor'})
        self.assertEqual(capturados - nomes, set())


SHA_CAPTURA = '747bca33fd2d5c5b2e6f20cc01ec65ab9e0949f725e54717fab29a70ef25b42b'
SHA_CAPTURA_CONSULTAS = 'fada576f61e00203097cb8c6b610650117416620011835fd9f55c86aea4559c0'
SHA_CAPTURA_EXIBICAO = '53c9d5db27d66483750e9a9df24f6de8538cead45621e81425cc89812fef4439'


class ContratosQuadro1EconomiaExibicao(unittest.TestCase):
    """The same routines at the exact frame-0/1 inputs of the display scenario (the M2 reference)."""
    def test_frozen_capture_precedes_translation_and_reproduces_the_display_frame_path(self):
        r = evidencia('exibicao')
        self.assertFalse(r['translation_executed'])
        self.assertEqual(r['scenario'], 'exibicao')
        self.assertTrue(r['path_reproduction']['passed'])
        self.assertTrue(all(c['reached_exit'] for c in r['calls']))
        frame = RAIZ / r['frame_capture']['path']
        self.assertEqual(hashlib.sha256(frame.read_bytes()).hexdigest(), r['frame_capture']['sha256'])
        self.assertEqual(json.loads(frame.read_bytes())['scenario'], 'exibicao')
        self.assertEqual(hashlib.sha256(CAPTURA_EXIBICAO.read_bytes()).hexdigest(), SHA_CAPTURA_EXIBICAO)

    def test_v1_call_counts_plus_two_affgame_bag_queries(self):
        # AffGame runs natively between frames and reaches BagContientTroupe through BatimentEstHabiter.
        esperado = dict(evidencia('v1')['call_counts'], **{'between_frames:BagContientTroupe': 2})
        self.assertEqual(evidencia('exibicao')['call_counts'], esperado)

    def test_v1_and_display_calls_match_after_relocation_except_caller_leftover_registers(self):
        import comparar_quadro1_economia_cenarios as cc
        r = cc.comparar()
        self.assertEqual(r['changed'], ['between_frames:BagContientTroupe', 'frame1:PlayerAttaqueCalculSympa',
                                        'load_tail:PlayerAttaqueCalculSympa'])
        for linha in r['routines']:
            if linha['routine'] == 'PlayerAttaqueCalculSympa':
                # Only the caller's leftover EAX/EDX differ; EDX passes through unchanged, EAX is overwritten.
                for d in linha['differing_calls']:
                    self.assertEqual(set(d['differences']), {'entry_registers', 'exit_registers'})
                    self.assertEqual(set(d['differences']['entry_registers']), {'EAX', 'EDX'})
                    self.assertEqual(set(d['differences']['exit_registers']), {'EDX'})
            elif linha['phase'] == 'between_frames':
                self.assertEqual(linha['calls'], [0, 2])

    def test_python_reproduces_every_exact_display_frame_call(self):
        self.assertEqual(comparar(self, cenario='exibicao'), 104)

    def test_providers_over_word_memory_reproduce_every_exact_display_frame_call(self):
        self.assertEqual(comparar(self, via_provedores, cenario='exibicao'), 104)


class ContratosConsultasEconomiaExibicao(unittest.TestCase):
    """Economy queries reached in the display-scenario frames, isolated at their exact inputs."""
    def test_frozen_query_capture_precedes_translation_and_reproduces_the_display_frame_path(self):
        r = evidencia('consultas')
        self.assertFalse(r['translation_executed'])
        self.assertEqual((r['scenario'], r['routine_set']), ('exibicao', 'consultas'))
        self.assertTrue(r['path_reproduction']['passed'])
        self.assertTrue(all(c['reached_exit'] for c in r['calls']))
        frame = RAIZ / r['frame_capture']['path']
        self.assertEqual(hashlib.sha256(frame.read_bytes()).hexdigest(), r['frame_capture']['sha256'])
        self.assertEqual(hashlib.sha256(CAPTURA_CONSULTAS.read_bytes()).hexdigest(), SHA_CAPTURA_CONSULTAS)
        self.assertEqual({c['routine'] for c in r['calls']}, CONSULTAS)
        self.assertEqual({c['routine'] for c in r['calls'] if 'stack_arguments' in c}, {'TestRessource'})
        v1 = json.loads(CAPTURA_CONSULTAS_V1.read_text())['calls']
        novos = ('caller_stack_changes', 'caller_stack_written_unchanged')
        self.assertEqual([{k: v for k, v in c.items() if k not in novos} for c in r['calls']], v1)
        self.assertTrue(all(set(novos) <= set(c) for c in r['calls']))

    def test_existing_class_forms_bound_live_reproduce_every_query_call(self):
        self.assertEqual(comparar(self, cenario='consultas'), len(evidencia('consultas')['calls']))

    def test_live_functions_reproduce_every_query_call_with_exact_reads(self):
        self.assertEqual(comparar(self, funcoes_vivas, cenario='consultas'), len(evidencia('consultas')['calls']))

    def test_providers_over_word_memory_reproduce_every_query_call(self):
        self.assertEqual(comparar(self, via_provedores, cenario='consultas'), len(evidencia('consultas')['calls']))


@unittest.skipUnless(os.environ.get('RISING_EMULAR'), 'set RISING_EMULAR=1 to rerun the original frame capture')
class DiferencialQuadro1Economia(unittest.TestCase):
    execucoes = 0

    def _fresca(self, cenario, conjunto='quadro'):
        with tempfile.TemporaryDirectory(dir=RAIZ / '.local') as pasta:
            saida = Path(pasta) / 'captura.json'
            subprocess.run([sys.executable, '-B', str(PASTA / 'capturar_quadro1_economia_original.py'),
                            '--cenario', cenario, '--conjunto', conjunto, '--saida', str(saida.relative_to(RAIZ))],
                           check=True, cwd=RAIZ,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
            fresca = json.loads(saida.read_text())
        frozen = evidencia('consultas' if conjunto == 'consultas' else cenario)
        if cenario == 'exibicao':
            # The fresh run uses Missions' current reference (Graphics' backend, -v2 artifacts); the frozen
            # captures were made on Stage17. Equal calls show the moved backend pointers reach no economy call.
            self.assertTrue(fresca['frame_capture']['path'].endswith('captura-quadro1-monde01-exibicao-v2.json'))
            self.assertTrue(frozen['frame_capture']['path'].endswith('captura-quadro1-monde01-exibicao.json'))
        self.assertTrue(fresca['path_reproduction']['passed'])
        self.assertEqual(fresca['calls'], frozen['calls'])
        type(self).execucoes += len(fresca['calls'])

    def test_fresh_isolated_capture_equals_frozen(self):
        self._fresca('v1')

    def test_fresh_isolated_display_capture_equals_frozen(self):
        self._fresca('exibicao')

    def test_fresh_isolated_display_query_capture_equals_frozen(self):
        self._fresca('exibicao', 'consultas')


if __name__ == '__main__':
    unittest.main()
