"""Core frame-0/frame-1 callees: replay of the committed isolated native calls (CPU-free).

Each captured call is replayed from exactly the bytes the original read before
writing them (``read_before_write``); every other byte is unknown and reading it
raises, so a translation that reads anything the original did not fails. The
translated stores must equal the native changed bytes and the translated
registers the native exit registers.
"""
import hashlib
import json
from pathlib import Path
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
sys.path.insert(0, str(RAIZ))
from chamadas_quadro_core import (ROTINAS, DependenciaRamoCore, PONTEIRO_UNIDADES, PASSO, obter_bit, definir_bit,
                                  calcular_fadiga, modificar_zona_caminho, provedores_core, CAMINHO_COLISAO)
from memoria_quadro_core import MemoriaQuadro, AcessoForaDosSegmentos

CAPTURA = RAIZ / 'evidencias/fundacoes-quadro/captura-chamadas-quadro1.json'
CAPTURA_SHA256 = 'fd209b2fb85794a52f778cb757ef79b6a4c42495763407ff731f98a05b4a5a8a'
REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
TABELA_BONUS, TAMANHO_BONUS = 0x4dfba0, 4 * 26 * 18


def captura():
    dados = CAPTURA.read_bytes()
    if hashlib.sha256(dados).hexdigest() != CAPTURA_SHA256:
        raise AssertionError('Committed frame-1 Core call capture changed')
    return json.loads(dados)


def bonus_economia():
    """Economy's BonusGetValEngin translation, through the public integration loader."""
    from integracao.providers import load_economy_bonus
    return load_economy_bonus().BonusUnidades


class MemoriaEsparsa:
    """Only the bytes the original read before writing are known; unknown reads raise."""
    def __init__(self, conhecidos, preenchimento=None):
        self.bytes = dict(conhecidos)
        self.iniciais = dict(conhecidos)
        self.preenchimento = preenchimento

    def _byte(self, a):
        a &= 0xffffffff
        if a not in self.bytes:
            raise AcessoForaDosSegmentos(a, 1)
        return self.bytes[a]

    def _acesso(self, n, a, valor):
        if valor is None:
            return int.from_bytes(bytes(self._byte(a + i) for i in range(n)), 'little')
        valor &= (1 << 8 * n) - 1
        for i in range(n):
            self.bytes[(a + i) & 0xffffffff] = valor >> 8 * i & 0xff
        return valor

    def u8(self, a, v=None):
        return self._acesso(1, a, v)

    def u16(self, a, v=None):
        return self._acesso(2, a, v)

    def u32(self, a, v=None):
        return self._acesso(4, a, v)

    def ler(self, a, n):
        return bytes(self.bytes.get((a + i) & 0xffffffff, self.preenchimento) for i in range(n))

    def mudancas(self):
        return sorted([hex(a), self.iniciais.get(a), v] for a, v in self.bytes.items() if self.iniciais.get(a) != v)

    def conferir(self, teste, capturadas):
        """Every captured change is reproduced and no known byte changes otherwise. Returns the
        number of stores to bytes the original never read whose native value did not change
        (absent from the capture by construction; the native differential compares them)."""
        esperado = {int(a, 16): (velho, novo) for a, velho, novo in capturadas}
        for a, (velho, novo) in esperado.items():
            teste.assertEqual(self.bytes.get(a), novo, hex(a))
            if a in self.iniciais:
                teste.assertEqual(self.iniciais[a], velho, hex(a))
        sem_leitura = 0
        for a, v in self.bytes.items():
            if a in esperado:
                continue
            if a in self.iniciais:
                teste.assertEqual(v, self.iniciais[a], f'unexpected change at {hex(a)}')
            else:
                sem_leitura += 1
        return sem_leitura


def regs(d):
    return {k: int(v, 16) for k, v in d.items()}


def bonus_de(memoria, classe):
    """Economy's live-bound query (BonusUnidades.vivo) over the replay bytes; table and
    runtime-type bytes the original did not read take the memory's declared fill."""
    if classe is None:
        return None
    return lambda jogador, tipo, seletor: classe.vivo(
        bytearray(memoria.ler(TABELA_BONUS, TAMANHO_BONUS)),
        tipos_unidades=bytearray(memoria.ler(0x4965ae, 1300))).consultar(jogador, tipo, seletor)


def sub_chemin(memoria, entrada):
    """Pushed sub byte of an isolated Chemin_ModifieZone call: the slot ECX = unit +0xfa + 2*sub.

    The stack word lies below the call's exit ESP, so the capture does not list
    it; it is recovered from the captured unit pointer and slot (the native
    differential reads the actual stack word).
    """
    registro = (memoria.u32(PONTEIRO_UNIDADES) + (entrada['EDX'] & 0xffff) * PASSO) & 0xffffffff
    sub, resto = divmod(entrada['ECX'] - registro - 0xfa, 2)
    if resto or not 0 <= sub <= 3:
        raise AssertionError('Chemin_ModifieZone slot is not a unit footprint slot')
    return sub


def replay(chamada, classe_bonus, preenchimento=None):
    conhecidos = {int(a, 16): v for a, v, _ in chamada['read_before_write']}
    m = MemoriaEsparsa(conhecidos, preenchimento)
    entrada = regs(chamada['entry_registers'])
    if chamada['routine'] == 'Chemin_ModifieZone':
        pilha = sub_chemin(m, entrada)
    elif chamada['routine'] == 'MouseSetZone':
        # The pushed y1 word lies below the exit ESP, so the capture does not list it; the
        # callee leaves it in EDX. Recovered here (the native differential reads the stack).
        pilha = int(chamada['exit_registers']['EDX'], 16)
    else:
        pilha = None
    saida = ROTINAS[chamada['routine']][1](m, entrada, pilha, bonus_de(m, classe_bonus))
    return m, entrada, saida


class ReplayChamadasQuadro1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.captura = captura()
        cls.bonus = bonus_economia()

    def test_capture_is_original_only_and_reproduced_the_path(self):
        c = self.captura
        self.assertFalse(c['translation_executed'])
        self.assertEqual(c['original_sha256'], '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')
        self.assertTrue(c['path_reproduction']['passed'])
        self.assertEqual(len(c['calls']), 678)
        self.assertTrue(all(x['reached_return'] for x in c['calls']))
        self.assertEqual({n: int(a, 16) for n, a in c['routines'].items()},
                         {n: ROTINAS[n][0] for n in c['routines']})

    def test_every_captured_call_replays_exactly(self):
        for i, chamada in enumerate(self.captura['calls']):
            with self.subTest(i=i, routine=chamada['routine'], phase=chamada['phase']):
                m, entrada, saida = replay(chamada, self.bonus, 0x00)
                self.assertEqual(m.mudancas(), chamada['changed_bytes'])
                esperado = dict(entrada, **saida)
                saida_nativa = regs(chamada['exit_registers'])
                self.assertEqual({k: esperado[k] for k in REGISTROS}, {k: saida_nativa[k] for k in REGISTROS})

    def test_bonus_table_bytes_outside_the_native_footprint_do_not_matter(self):
        for chamada in self.captura['calls']:
            if chamada['routine'] == 'CalculFatigue':
                for fill in (0x5a, 0xa7, 0xff):
                    m, _, saida = replay(chamada, self.bonus, fill)
                    self.assertEqual(m.mudancas(), chamada['changed_bytes'])

    def test_reached_domain(self):
        chamadas = self.captura['calls']
        fadiga = [c for c in chamadas if c['routine'] == 'CalculFatigue']
        self.assertEqual(sum(bool(c['changed_bytes']) for c in fadiga), 16)   # counter-increment path
        tipos = {next(v for a, v, r in c['read_before_write'] if r == 'SetEnginCollision+0x28')
                 for c in chamadas if c['routine'] == 'SetEnginCollision'}
        self.assertEqual(tipos, {0, 1, 5, 7, 8})
        self.assertTrue(all(CAMINHO_COLISAO[t] == 'single' for t in tipos))
        self.assertTrue(all(int(c['exit_registers']['EAX'], 16) & 0xff == 0
                            for c in chamadas if c['routine'] == 'Chemin_ModifieZone'))
        for nome in ('BatimentEstDecouvert', 'BatimentContourEstIllumine'):
            self.assertTrue(all(int(c['exit_registers']['EAX'], 16) & 0xff == 0 for c in chamadas if c['routine'] == nome))


class DominioEDependencias(unittest.TestCase):
    def test_pure_bit_helpers(self):
        self.assertEqual(obter_bit(0xffffff24, 0x105), dict(EAX=1))
        self.assertEqual(obter_bit(0x80, 0x27), dict(EAX=1))      # count masked to 5 bits
        m = MemoriaQuadro([(0x1000, bytearray([0xff, 0x00]))])
        self.assertEqual(definir_bit(m, 0x1000, 0x23, 0x500), dict(EAX=0x1000, EBX=0x5f7, EDX=0xf7))
        self.assertEqual(definir_bit(m, 0x1001, 9, 1), dict(EAX=0x1001, EDX=0))   # 8-bit shift >= 8
        self.assertEqual(definir_bit(m, 0x1001, 1, 2), dict(EAX=0x1001))
        self.assertEqual(m.ler(0x1000, 2), bytes([0xf7, 0]))

    def test_fatigue_threshold_consumes_a_provision_or_raises_on_hunger(self):
        unidades = bytearray(PASSO)
        unidades[0x72], unidades[1], unidades[0x74:0x76] = 1, 0, (0xbb7).to_bytes(2, 'little')
        dgroup = bytearray(0x523000 - 0x494000)
        dgroup[PONTEIRO_UNIDADES - 0x494000:PONTEIRO_UNIDADES - 0x494000 + 4] = (0x1000).to_bytes(4, 'little')
        dgroup[0x4965dc - 0x494000:0x4965dc - 0x494000 + 2] = (0xbb8).to_bytes(2, 'little')
        m = MemoriaQuadro([(0x494000, dgroup), (0x1000, unidades)])
        with self.assertRaises(DependenciaRamoCore) as e:          # no provisions: hunger branch
            calcular_fadiga(m, 0, lambda j, t, s: 0)
        self.assertEqual(e.exception.endereco, 0x452d6f)
        self.assertEqual(unidades[0x74:0x76], (0xbb8).to_bytes(2, 'little'))   # stored before the comparison
        unidades[0x74:0x76], unidades[4:6] = (0xbb7).to_bytes(2, 'little'), (3).to_bytes(2, 'little')
        self.assertEqual(calcular_fadiga(m, 0, lambda j, t, s: 0), dict(EAX=3))
        self.assertEqual((unidades[0x74:0x76], unidades[4:6]), (bytes(2), (2).to_bytes(2, 'little')))

    def test_unreached_branches_raise_before_any_store(self):
        unidades = bytearray(PASSO)
        unidades[0x72], unidades[1], unidades[0x74:0x76] = 1, 0, (0xbb7).to_bytes(2, 'little')
        dgroup = bytearray(0x523000 - 0x494000)
        dgroup[PONTEIRO_UNIDADES - 0x494000:PONTEIRO_UNIDADES - 0x494000 + 4] = (0x1000).to_bytes(4, 'little')
        dgroup[0x4965dc - 0x494000:0x4965dc - 0x494000 + 2] = (0xbb8).to_bytes(2, 'little')
        m = MemoriaQuadro([(0x494000, dgroup), (0x1000, unidades)])
        antes = (bytes(dgroup), bytes(unidades))
        with self.assertRaises(DependenciaRamoCore) as e:
            calcular_fadiga(m, 0, None)
        self.assertEqual(e.exception.endereco, 0x452d48)
        for modo, alvo in ((0, 0x43e153), (1, 0x43e1b4), (3, 0x43e256), (4, 0x43e29c)):
            with self.assertRaises(DependenciaRamoCore) as e:
                modificar_zona_caminho(m, 0, 0, modo, 0x1000, 0)
            self.assertEqual(e.exception.endereco, alvo)
        self.assertEqual((bytes(dgroup), bytes(unidades)), antes)

    def test_memory_refuses_unmapped_and_readonly(self):
        with self.assertRaises(ValueError):
            MemoriaQuadro([(0, b'abc')])
        with self.assertRaises(ValueError):
            MemoriaQuadro([(0, bytearray(4)), (2, bytearray(4))])
        m = MemoriaQuadro([(0x10, bytearray(4))])
        with self.assertRaises(AcessoForaDosSegmentos):
            m.u32(0x11)

    def test_provider_adapters_use_ai_runtime_keywords(self):
        m = MemoriaQuadro([(0x10, bytearray(4))])
        p = provedores_core(m)
        self.assertEqual(p['GetBit'](sitio=0x456ead, valor=4, bit=2), 1)
        self.assertTrue({'CaseEstDecouverte', 'BatimentEstDecouvert', 'BatimentContourEstIllumine', 'BatimentGetCase',
                         'CalculFatigue', 'SetEnginCollision', 'Random', 'GetBit', 'CaseEstIlluminee'} <= set(p))


ZONAS = RAIZ / 'evidencias/fundacoes-quadro/captura-zonas-animacao-quadro1.json'
ZONAS_SHA256 = '277496ffb203b28e02120f202cd7430af757bedc777f4941b2eb752fba8f1adc'


class ReplayZonasAnimacaoQuadro1(unittest.TestCase):
    """SetClipping, InitGameZone (and the routines it calls), NextAnimTerrain/NextAnimVeget."""
    @classmethod
    def setUpClass(cls):
        dados = ZONAS.read_bytes()
        if hashlib.sha256(dados).hexdigest() != ZONAS_SHA256:
            raise AssertionError('Committed zone/animation capture changed')
        cls.captura = json.loads(dados)

    def test_capture_scope(self):
        c = self.captura
        self.assertFalse(c['translation_executed'])
        self.assertTrue(c['path_reproduction']['passed'])
        self.assertEqual(len(c['calls']), 61)
        self.assertEqual(c['not_reached'], ['MarcheGetPos', 'MarcheGetTaille', 'NextAnimVegetFullMap'])
        self.assertEqual({n: int(a, 16) for n, a in c['routines'].items()}, {n: ROTINAS[n][0] for n in c['routines']})

    def test_every_captured_call_replays_exactly(self):
        self.sem_leitura = 0
        for i, chamada in enumerate(self.captura['calls']):
            with self.subTest(i=i, routine=chamada['routine'], phase=chamada['phase']):
                m, entrada, saida = replay(chamada, None)
                self.sem_leitura += m.conferir(self, chamada['changed_bytes'])
                esperado, nativo = dict(entrada, **saida), regs(chamada['exit_registers'])
                self.assertEqual({k: esperado[k] for k in REGISTROS}, {k: nativo[k] for k in REGISTROS})

    def test_reached_branches(self):
        chamadas = self.captura['calls']
        zonas = [c for c in chamadas if c['routine'] == 'InitGameZone']
        self.assertEqual([c['caller'] for c in zonas], ['MenuInit+0x1ce', 'CalculGame+0xa76'])
        for c in zonas:
            blocos = {int(b, 16) for b in c['native_blocks']}
            self.assertIn(0x471aa4, blocos)                 # mode 1
            self.assertIn(0x471d74, blocos)                 # screen width != 640 (0x49a018 = 0)
            self.assertIn(0x471d7d, blocos)                 # minimap rectangle
            self.assertIn(0x471ec7, blocos)                 # contact type not 1/2/3: default zone 0x1a
            self.assertIn(0x471f30, blocos)                 # no message box
            self.assertNotIn(0x471f7f, blocos)              # no alliance zone
        for c in chamadas:
            if c['routine'] in ('NextAnimTerrain', 'NextAnimVeget'):
                self.assertNotIn(0x477737 if c['routine'] == 'NextAnimTerrain' else 0x47731b,
                                 {int(b, 16) for b in c['native_blocks']})

    def test_mode3_refusals_before_any_store(self):
        from chamadas_quadro_core import iniciar_zonas_jogo
        dgroup = bytearray(0x523000 - 0x494000)
        m = MemoriaQuadro([(0x494000, dgroup)])
        with self.assertRaises(ValueError):                    # zero items returns the caller EBX/ECX
            iniciar_zonas_jogo(m, 3, 0)
        dgroup[0x4e2f40 - 0x494000:0x4e2f42 - 0x494000] = (0x100).to_bytes(2, 'little')
        with self.assertRaises(DependenciaRamoCore) as e:      # byte index never reaches 256 items
            iniciar_zonas_jogo(m, 3, 0, 0, 0)
        self.assertEqual(e.exception.endereco, 0x4719ba)
        self.assertEqual(bytes(dgroup[0x5099b4 - 0x494000:0x50a9c0 - 0x494000]), bytes(0x100c))


EXIBICAO = RAIZ / 'evidencias/fundacoes-quadro/captura-exibicao-quadro1.json'
EXIBICAO_SHA256 = 'b4e6747324346ac1aacc1a36b5c31f4ae87b3a35551c6303b32265133385dee0'


class ReplayExibicaoQuadro1(unittest.TestCase):
    """Display scenario (M2 reference): 25x17 viewport, NextAnim* loops and the CRT rand stream."""
    @classmethod
    def setUpClass(cls):
        dados = EXIBICAO.read_bytes()
        if hashlib.sha256(dados).hexdigest() != EXIBICAO_SHA256:
            raise AssertionError('Committed display-scenario capture changed')
        cls.captura = json.loads(dados)

    def test_capture_scope(self):
        c = self.captura
        self.assertEqual((c['scenario'], c['translation_executed'], c['path_reproduction']['passed']),
                         ('exibicao', False, True))
        self.assertEqual(len(c["calls"]), 70)
        self.assertEqual(c['routine_entries']['rand:frame1'], 425)
        self.assertEqual(c['not_reached'], ['MarcheGetPos', 'MarcheGetTaille', 'NextAnimVegetFullMap'])

    def test_every_captured_call_replays_exactly(self):
        sem_leitura = 0
        for i, chamada in enumerate(self.captura['calls']):
            with self.subTest(i=i, routine=chamada['routine'], phase=chamada['phase']):
                m, entrada, saida = replay(chamada, None)
                sem_leitura += m.conferir(self, chamada['changed_bytes'])
                esperado, nativo = dict(entrada, **saida), regs(chamada['exit_registers'])
                self.assertEqual({k: esperado[k] for k in REGISTROS}, {k: nativo[k] for k in REGISTROS})

    def test_crt_rand_matches_the_frame_foundation_arithmetic(self):
        from fundacoes_quadro import aleatorio_crt
        for chamada in self.captura['calls']:
            if chamada['routine'] == 'rand':
                lidos = {int(a, 16): v for a, v, _ in chamada['read_before_write']}
                bloco = bytearray(16)
                bloco[12:16] = bytes(lidos[0x340000c + i] for i in range(4))
                self.assertEqual(aleatorio_crt(bloco), int(chamada['exit_registers']['EAX'], 16))


SEGUINTES = RAIZ / 'evidencias/fundacoes-quadro/captura-quadros-seguintes.json'
SEGUINTES_SHA256 = 'f0ae7513a28e312a496531c76a7aff18aaf4dfa8868f0c920be8d8fc81dafd5c'


class ReplayQuadrosSeguintes(unittest.TestCase):
    """Display-reference frames 0..128: later-frame NextAnim*, InitGameZone modes, FullMap, queries."""
    @classmethod
    def setUpClass(cls):
        from compactar_captura_isolada import expandir
        dados = SEGUINTES.read_bytes()
        if hashlib.sha256(dados).hexdigest() != SEGUINTES_SHA256:
            raise AssertionError('Committed frames 0..128 capture changed')
        cls.captura = json.loads(dados)
        cls.chamadas = [expandir(c) for c in cls.captura['calls']]

    def test_capture_scope(self):
        c = self.captura
        self.assertEqual((c['scenario'], c['translation_executed'], c['frames_run'], c['code_unchanged']),
                         ('exibicao', False, 128, True))
        self.assertTrue(all(c['reproduction_frames_0_1'].values()))
        self.assertTrue(all(x['reached_return'] for x in self.chamadas))
        modos = {x['case'] for x in self.chamadas if x['routine'] == 'InitGameZone'}
        self.assertTrue({'mode2_mission1', 'mode2_mission7', 'mode3_five_items', 'mode4', 'mode0_invalid'} <= modos)
        self.assertEqual(sorted({x['frame'] for x in self.chamadas if x['routine'] == 'NextAnimVegetFullMap'}),
                         [1, 2, 64, 128])

    def test_every_captured_case_replays_exactly(self):
        for i, chamada in enumerate(self.chamadas):
            with self.subTest(i=i, routine=chamada['routine'], frame=chamada['frame'], case=chamada['case']):
                regs_entrada = {k: int(v, 16) for k, v in chamada['entry_registers'].items()}
                regs_entrada.update({k: int(v, 16) for k, v in chamada['perturbation']['registers'].items()})
                conhecidos = {int(a, 16): v for a, v, _ in chamada['read_before_write'] if v is not None}
                m = MemoriaEsparsa(conhecidos)
                pilha = int(chamada['exit_registers']['EDX'], 16) if chamada['routine'] == 'MouseSetZone' else None
                saida = ROTINAS[chamada['routine']][1](m, regs_entrada, pilha, None)
                sem_leitura = m.conferir(self, chamada['changed_bytes'])
                if chamada['routine'] not in ('InitGameZone', 'MouseSetZone', 'MouseTestZone'):
                    self.assertEqual(sem_leitura, 0)        # only the zone setters store unread bytes
                esperado, nativo = dict(regs_entrada, **saida), regs(chamada['exit_registers'])
                self.assertEqual({k: esperado[k] for k in REGISTROS}, {k: nativo[k] for k in REGISTROS})


QUADRO1 = RAIZ / 'pesquisas-paralelas/missoes/evidencias/captura-quadro1-monde01-original.json'
RASTRO = RAIZ / 'pesquisas-paralelas/missoes/evidencias/rastro-quadro1-monde01.json'


class ReValidacaoFundacoesQuadro1(unittest.TestCase):
    """Frame foundations against the Missions frame-0/frame-1 phase snapshots (exact frame inputs)."""
    @classmethod
    def setUpClass(cls):
        import base64
        import zlib
        from estado_m1_quadro import carregar_m1
        cap = json.loads(QUADRO1.read_bytes())
        if hashlib.sha256(QUADRO1.read_bytes()).hexdigest() != \
                'c06f78ea2f611d668b4a2fc7bde712b07c21ed8eb0a929668d4d70e56d47fed8':
            raise unittest.SkipTest('Missions\' frame-1 capture is foreign and not pinned: it changed since these '
                                    'replays were derived; rerun them against the new capture')
        cls.fases = {p['phase']: p for p in cap['phases']}
        s0 = bytearray(carregar_m1()[0])
        cls.dgroup = {'s0': s0}
        anterior = s0
        for nome in ('load_tail', 'between_frames', 'frame1'):
            blocos = cls.fases[nome]['state_after']['blocks_changed_since_previous']
            atual = (bytearray(zlib.decompress(base64.b64decode(blocos['dgroup']['zlib_base64'])))
                     if 'dgroup' in blocos else bytearray(anterior))
            cls.dgroup[nome] = anterior = atual
        rastro = json.loads(RASTRO.read_bytes())['phases']
        cls.contagens = {f: {r['routine']: r['entries'] for r in v['routines_in_first_entry_order']}
                         for f, v in rastro.items()}

    def janela(self, fase, endereco, n):
        return bytearray(self.dgroup[fase][endereco - 0x494000:endereco - 0x494000 + n])

    def test_load_counter_reset_then_progiteration_prefix(self):
        from fundacoes_quadro import zerar_contadores_carga, avancar_contadores_iteracao
        c = self.janela('s0', 0x508f7c, 12)
        self.assertEqual(zerar_contadores_carga(c), (0, 4, 8))
        self.assertEqual(c, self.janela('load_tail', 0x508f7c, 12))
        self.assertEqual(avancar_contadores_iteracao(c), (0,))
        self.assertEqual(c, self.janela('between_frames', 0x508f7c, 12))
        self.assertEqual(self.fases['between_frames']['memory_changes']['changed']['dgroup']['first_ranges'],
                         [['0x508f7c', '0x508f7e']])
        self.assertEqual(self.janela('frame1', 0x508f7c, 12), c)     # frame 1 itself leaves them

    def test_game_next_frame_once_per_frame(self):
        from fundacoes_quadro import avancar_quadro_jogo
        for antes, depois in (('s0', 'load_tail'), ('between_frames', 'frame1')):
            fase = 'frame1' if depois == 'frame1' else 'load_tail'
            self.assertEqual(self.contagens[fase]['GameNextFrame'], 1)
            c = self.janela(antes, 0x496d40, 4)
            avancar_quadro_jogo(c)
            self.assertEqual(c, self.janela(depois, 0x496d40, 4))

    def test_world_rng_advances_once_per_state7_unit_and_ai_rng_untouched(self):
        from fundacoes_quadro import aleatorio_mundo
        for antes, depois, fase in (('s0', 'load_tail', 'load_tail'), ('between_frames', 'frame1', 'frame1')):
            s = self.janela(antes, 0x497164, 4)
            for _ in range(self.contagens[fase]['Random']):
                aleatorio_mundo(s)
            self.assertEqual(s, self.janela(depois, 0x497164, 4))
            self.assertNotIn('iaRandom', self.contagens[fase])
            self.assertEqual(self.janela(antes, 0x498db4, 4), self.janela(depois, 0x498db4, 4))
        self.assertEqual(self.contagens['frame1']['Random'], 8)

    def test_cd_branch_permutation_draw_matches_mcicd_play_arguments(self):
        from fundacoes_quadro import consumir_permutacao
        for antes, fase, depois in (('s0', 'load_tail', 'load_tail'), ('between_frames', 'frame1', 'frame1')):
            tabela, cursor = self.janela(antes, 0x4e1c18, 256), self.janela(antes, 0x4e1d18, 1)
            eventos = [e for e in self.fases[fase]['boundaries'] if e['routine'] == 'MCICD_Play']
            self.assertEqual(eventos[-1]['caller'], 'CalculGame+0xac5')
            for e in eventos:                  # load tail: MenuInit+0x202, then the CalculGame CD branch
                self.assertEqual(e['guards'], {'0x4e2f28': 0, '0x4e2f29': 0})
                valor = consumir_permutacao(tabela, cursor)
                r = {k: int(v, 16) for k, v in e['registers'].items()}
                self.assertEqual((r['EAX'], r['EDX'], r['EBX'] & 0xff), (2 + valor % 2, 0, cursor[0]))
            self.assertEqual(cursor, self.janela(depois, 0x4e1d18, 1))

    def test_viewport_size_still_zero_so_next_anim_visits_no_cells(self):
        for fase in ('load_tail', 'frame1'):
            self.assertEqual(self.janela(fase, 0x508724, 4), bytearray(4))
            self.assertEqual(self.contagens[fase]['NextAnimVeget'], 1)


EXE = RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE'
MANIFESTO = RAIZ / 'evidencias/fundacoes-quadro/chamadas-quadro1/manifesto.json'


@unittest.skipUnless(EXE.exists(), 'Original executable not available locally')
class EvidenciaEstatica(unittest.TestCase):
    def test_manifest_regenerates_from_intact_bytes(self):
        from extrair_chamadas_quadro1 import extrair
        committed = json.loads(MANIFESTO.read_bytes())
        self.assertEqual(json.loads(json.dumps(extrair())), committed)
        self.assertTrue(all(f['result'] == 'overwritten_before_read' for f in committed['caller_flag_use']))

    def test_translation_tables_equal_the_jump_tables(self):
        import chamadas_quadro_core as q
        tabelas = {t['routine']: [int(v, 16) for v in t['targets']]
                   for t in json.loads(MANIFESTO.read_bytes())['jump_tables']}
        # BatimentCollision cases are 'and eax,0xffff; mov al,[eax+table]' (13 bytes each).
        from extrair_fundacoes_quadro import _bytes
        raw = EXE.read_bytes()
        bases = [int.from_bytes(_bytes(raw, alvo + 7, alvo + 11), 'little') for alvo in tabelas['BatimentCollision']]
        self.assertEqual(tuple(bases), q.MASCARAS_ESTRUTURA)
        caminhos = {0x442cf4: q.UMA_CELULA, 0x442d38: q.QUATRO_CELULAS, 0x442df4: q.QUATRO_CELULAS_SEM_REGIAO,
                    0x442d27: q.UMA_CELULA_SEM_REGIAO}
        self.assertEqual(tuple(caminhos[a] for a in tabelas['SetEnginCollision']), q.CAMINHO_COLISAO)
        self.assertEqual(tabelas['Chemin_ModifieZone'], [0x43e153, 0x43e1b4, 0x43e1ee, 0x43e256])
        self.assertEqual(set(tabelas['CalculFatigue']), {0x452cf7})


if __name__ == '__main__':
    unittest.main()
