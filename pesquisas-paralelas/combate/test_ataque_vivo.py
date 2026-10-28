"""Live attack chain: contracts, original captures and native lockstep whole-state equality."""
import hashlib
import json
import os
from pathlib import Path
import struct
import unittest

from ataque_vivo import (AtaqueVivo, DependenciaAtaqueVivo, batiment_en_destruction, batiment_get_player,
                         definir_ataque, ramo_estado_ataque, tipo_jogador)
from animacao_disparo import ContextoAtaque, guardar, animar
from capturar_ataque_vivo import AREAS, ATACANTE, CENARIOS, CONTADOR_BASE, VITIMA, criar_mundo
from combate import avancar_recarga
from projeteis import u16

CAPTURA = Path(__file__).resolve().parent / 'evidencias/captura-ataque-vivo-original.json'
INATIVOS = (1, 1, 1, 1)  # declared fixture: original sympathy inactive bytes at 0x51a990+16*owner


class Checkpoint(Exception):
    pass


def efeito_fixture(mundo):
    """Only the original no-effect guards the native fixtures execute; anything else is a named stop."""
    def efeito(nome, args):
        if nome == 'iagUnitSendMessage':
            unidade, mensagem, _ = args
            p = unidade * 276
            dono, grupo = mundo.unidades[p], struct.unpack_from('<I', mundo.unidades, p + 0x10c)[0]
            if dono < 4 and mundo.controle_jogadores[dono] != 2:
                return None  # PlayerGetType != 2: the message prefix returns
            if grupo == 0xffffffff and mensagem in (0x44, 0x48, 0x4c):
                return None  # proven null-group guards for combat messages
        elif nome == 'MAJSympathie':
            a, b, _ = args
            if a == b or a >= 4 or b >= 4 or INATIVOS[a]:
                return None  # 0x475121..0x475145 early returns
        elif nome == 'PlayerAAttaqueSet':
            if args[0] >= 4 or args[1] >= 4:
                return None  # 0x46d609/0x46d612 owner-range returns before the statistic store
        raise DependenciaAtaqueVivo(nome, args)
    return efeito


def criar_vivo(c):
    w, danos, pool, tipos, bonus = criar_mundo(c)
    vivo = AtaqueVivo(w, pool, danos, tipos, bonus, bytes(5), bonus_4965ac=0,
                      ultimo_alerta=0, celula_alerta=0x1234, efeito=efeito_fixture(w))
    vivo.contador = CONTADOR_BASE
    return vivo


def preludio(vivo, i):
    """Harness-only model of the declared prelude head 0x45442c..0x454591 (ai-runtime owns its place)."""
    u = vivo.unidades[i]
    if u[2]:
        if struct.unpack_from('<I', u, 0x104)[0] != 0xffffffff:
            raise DependenciaAtaqueVivo('EnginGetVolume', (i,))
        u[0xf9] = 0
    if u[2] in (0, 4):
        raise AssertionError('Only alive attack-state units are dispatched by this chain')
    if u[1] == 16:
        animar(u, u[0xa7], u[0xa5])
    recarga = struct.unpack_from('<H', vivo.tipos, u[1] * 50 + 0x30)[0]
    guardar(u, 0x102, avancar_recarga(u16(u, 0x102), recarga, vivo.bonus.consultar(u[0], u[1], 3) & 65535))


def areas_mundo(vivo):
    w, b = vivo.mundo, vivo.mundo.busca
    return dict(
        unidades=bytes(w.unidades), estruturas=bytes(w.estruturas), grupos=bytes(w.grupos), objetos=bytes(w.objetos),
        atributos=bytes(w.atributos), regioes=struct.pack('<65536H', *w.regioes), tiles=struct.pack('<65536H', *w.tiles),
        donos_objetos=bytes(w.donos_objetos), mini_final=bytes(w.mini_final), mini_unidades=bytes(w.mini_unidades),
        mini_estruturas=bytes(w.mini_estruturas), descoberto=b''.join(bytes(g) for g in w.descoberto),
        luz_bordas=b''.join(bytes(g) for g in w.luz_bordas), contagem_luz=b''.join(bytes(g) for g in w.contagem_luz),
        sombra=bytes(w.sombra), rotas=b''.join(bytes(r) for r in w.rotas), projeteis=bytes(vivo.pool.memoria),
        busca=struct.pack('<HBBIB', b.unidade, b.ocupada, b.sucesso, b.ponteiro_rota, b.concluida),
        iteracao=struct.pack('<IH', w.grupo_em_iteracao, w.unidade_em_iteracao),
        alerta=struct.pack('<IH', vivo.impacto.ultimo_alerta, vivo.impacto.celula_alerta & 0xffff))


def estado(areas):
    return hashlib.sha256(b''.join(areas[n] for n in AREAS)).hexdigest()


class ExecutorPython:
    def __init__(self, nome):
        self.c = CENARIOS[nome]
        self.vivo = criar_vivo(self.c)

    def _rodar(self, chamada):
        try:
            chamada()
        except DependenciaAtaqueVivo as e:
            return e.nome
        except Checkpoint:
            return 'CalculAttaqueEngin'
        return None

    def contador(self, valor):
        self.vivo.contador = valor

    def definir_ataque(self, i, modo, ref):
        return self._rodar(lambda: self.vivo.definir_ataque(i, modo, ref))

    def projeteis(self):
        return self._rodar(self.vivo.calcular_projeteis)

    def preludio(self, i):
        return self._rodar(lambda: preludio(self.vivo, i))

    def ramo(self, i, checkpoint=False):
        def parar(ctx, indice):
            raise Checkpoint
        return self._rodar(lambda: self.vivo.ramo(i, parar) if checkpoint else self.vivo.ramo(i))

    def unidades(self):
        return bytes(self.vivo.mundo.unidades)

    def pool_ativo(self):
        return any(self.vivo.pool.memoria[k * 56 + 2] for k in range(100))


def conduzir(nome, ex, ao_segmento):
    """Same frame order as capturar_ataque_vivo.executar_nativo."""
    c = CENARIOS[nome]

    def passo(segmento, quadro, unidade, chamada):
        parada = chamada()
        ao_segmento(segmento, quadro, unidade, parada)
        return parada

    ex.contador(CONTADOR_BASE)
    if c['tipo'] == 'definir':
        passo('SetAttaqueEngin', 0, ATACANTE, lambda: ex.definir_ataque(ATACANTE, *c['pedido']))
        return
    if c['tipo'] == 'ramo':
        passo('ramo', 0, ATACANTE, lambda: ex.ramo(ATACANTE, c.get('checkpoint', False)))
        return
    if passo('SetAttaqueEngin', 0, ATACANTE, lambda: ex.definir_ataque(ATACANTE, 1, VITIMA)):
        return
    for quadro in range(1, c['quadros'] + 1):
        ex.contador(CONTADOR_BASE + quadro)
        if passo('ProjectileCalcul', quadro, None, ex.projeteis):
            return
        i = 0
        while i < 800:
            unidades = ex.unidades()
            j = next((k for k in range(i, 800) if unidades[k * 276 + 2] in (1, 24)), None)
            if j is None:
                break
            if passo('preludio', quadro, j, lambda: ex.preludio(j)) or passo('ramo', quadro, j, lambda: ex.ramo(j)):
                return
            i = j + 1
        unidades = ex.unidades()
        if not any(unidades[k * 276 + 2] in (1, 24) for k in range(800)) and not ex.pool_ativo():
            return


class ContratosAtaqueVivo(unittest.TestCase):
    def test_player_type_and_structure_getters(self):
        self.assertEqual([tipo_jogador(bytes([1, 2, 0, 7]), d) for d in (0, 1, 2, 3, 4, 200, 0x100)], [1, 2, 0, 7, 2, 2, 1])
        s = bytearray(276000)
        s[7 * 276 + 4], s[7 * 276 + 5] = 3, 3
        self.assertEqual((batiment_en_destruction(s, 7), batiment_get_player(s, 0x10007)), (1, 3))
        with self.assertRaises(ValueError):
            batiment_get_player(s, 1000)

    def test_set_attack_resets_before_refusal_and_keeps_same_order(self):
        for tipo, modo, ref, aceito in ((0, 1, VITIMA, True), (9, 1, VITIMA, False), (0, 1, ATACANTE, False),
                                       (0, 2, VITIMA, False), (0, 5, 0x2a2a, True), (13, 3, 7, False)):
            vivo = criar_vivo(dict(CENARIOS['set-mode1-accept'], tipo_atacante=tipo))
            resets = []
            u = vivo.unidades[ATACANTE]
            self.assertEqual(definir_ataque(vivo.unidades, ATACANTE, modo, ref, resets.append), aceito)
            self.assertEqual(resets, [ATACANTE])
            if aceito:
                self.assertEqual((u[2], u[0x8a], u[0xb7], u16(u, 0xb8)), (1, 0, modo, ref))
            resets.clear()
            if aceito:
                self.assertFalse(definir_ataque(vivo.unidades, ATACANTE, modo, ref | 0x10000, resets.append))
                self.assertEqual(resets, [])

    def test_invalid_target_paths_and_order(self):
        vivo = criar_vivo(CENARIOS['branch-mode1-target-dying'])
        chamadas = []
        def consultar(nome, args):
            chamadas.append((nome, args))
            return 1
        def efetuar(nome, args):
            chamadas.append((nome, args))
            self.assertEqual(u16(vivo.unidades[ATACANTE], 0xb8), VITIMA)  # +b8 is cleared after the request
        ramo_estado_ataque(vivo.contexto, ATACANTE, consultar, efetuar)
        self.assertEqual(chamadas, [('PlayerGetType', (0,)), ('SetDeplaceEngin', (ATACANTE, 0x2828))])
        self.assertEqual(u16(vivo.unidades[ATACANTE], 0xb8), 0xffff)
        chamadas.clear()
        u = vivo.unidades[ATACANTE]
        guardar(u, 0xb8, VITIMA)
        ramo_estado_ataque(vivo.contexto, ATACANTE, lambda n, a: chamadas.append((n, a)) or 2, lambda n, a: chamadas.append((n, a)))
        self.assertEqual(chamadas, [('PlayerGetType', (0,)), ('iagUnitSendMessage', (ATACANTE, 0x4a, 0))])
        self.assertEqual(u16(u, 0xb8), VITIMA)

    def test_mode3_queries_and_untranslated_modes(self):
        vivo = criar_vivo(CENARIOS['branch-mode3-destroying'])
        chamadas = []
        def consultar(nome, args):
            chamadas.append((nome, args))
            return {'BatimentEnDestruction': 0, 'BatimentGetPlayer': 1}[nome]
        def parar(ctx, i):
            raise Checkpoint
        with self.assertRaises(Checkpoint):
            ramo_estado_ataque(vivo.contexto, ATACANTE, consultar, None, parar)
        self.assertEqual(chamadas, [('BatimentEnDestruction', (7,)), ('BatimentGetPlayer', (7,))])
        u = vivo.unidades[ATACANTE]
        antes = bytes(vivo.mundo.unidades)
        for modo in (0, 2, 4, 6, 255):
            u[0xb7] = modo
            with self.assertRaisesRegex(NotImplementedError, '0x451914'):
                ramo_estado_ataque(vivo.contexto, ATACANTE, None, None)
        u[0xb7] = 3
        self.assertEqual(bytes(vivo.mundo.unidades), antes)

    def test_missing_providers_are_named(self):
        c = CENARIOS['melee-monster-to-death']
        w, danos, pool, tipos, bonus = criar_mundo(c)
        vivo = AtaqueVivo(w, pool, danos, tipos, bonus, bytes(5), bonus_4965ac=0, ultimo_alerta=0, celula_alerta=0)
        u = vivo.unidades[ATACANTE]
        u[0], u[2], u[0xb7] = 1, 1, 1
        w.controle_jogadores[1] = 2
        guardar(u, 0xb8, 0xffff)
        with self.assertRaises(DependenciaAtaqueVivo) as e:
            vivo.ramo(ATACANTE)
        self.assertEqual((e.exception.nome, e.exception.endereco, e.exception.argumentos), ('iagUnitSendMessage', 0x4829c8, (ATACANTE, 0x4a, 0)))
        with self.assertRaises(ValueError):
            AtaqueVivo(w, bytearray(5600), danos, tipos, bonus, bytes(5), bonus_4965ac=0, ultimo_alerta=0, celula_alerta=0)

    def test_original_only_captures_reproduced(self):
        """Python reproduces every captured segment: same stops and whole-area digests."""
        relatorio = json.loads(CAPTURA.read_text())
        self.assertEqual(relatorio['sha256_original'], '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')
        self.assertEqual(set(relatorio['capturas']), set(CENARIOS))
        for nome, capturados in relatorio['capturas'].items():
            ex = ExecutorPython(nome)
            obtidos = []
            def conferir(seg, q, un, parada):
                self.assertLess(len(obtidos), len(capturados), nome)
                cap = capturados[len(obtidos)]
                obtidos.append(seg)
                self.assertEqual((seg, q, un, parada), (cap['segmento'], cap['quadro'], cap['unidade'], cap['parada']), nome)
                self.assertEqual(cap['quantidade_nao_modelados'], 0, nome)
                areas = areas_mundo(ex.vivo)
                if estado(areas) != cap['estado']:
                    diferentes = [n for n in AREAS if hashlib.sha256(areas[n]).hexdigest()[:16] != cap['areas'][n]]
                    self.fail(f'{nome} {seg} frame {q} unit {un}: areas {diferentes}')
            conduzir(nome, ex, conferir)
            self.assertEqual(len(obtidos), len(capturados), nome)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional: RISING_EMULAR=1')
class DiferencialAtaqueVivo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_ataque_vivo import BancadaAtaqueVivo
        cls.b = BancadaAtaqueVivo()
        cls.segmentos = cls.quadros = 0
        cls.paradas, cls.escritas_8a = {}, {}

    def lockstep(self, nome):
        b, captura = self.b, json.loads(CAPTURA.read_text())['capturas'][nome]
        py = ExecutorPython(nome)
        w, danos, pool, tipos, _ = criar_mundo(CENARIOS[nome])
        b.preparar_vivo(w, danos, pool, tipos)
        teste, seq = self, iter(captura)

        class Par:
            def contador(self, valor):
                b.contador(valor)
                py.contador(valor)

            def _par(self, nativo, python):
                antes = b.instantaneo()
                b.escritas_8a = []
                parada_n, _ = nativo()
                depois = b.instantaneo()
                parada_p = python()
                teste.assertEqual(parada_n, parada_p)
                modelado = b.modelado()
                fora = [a for a in b.alteracoes(antes, depois) if not any(i <= a < i + t for i, t in modelado)]
                teste.assertEqual(fora, [], 'native write outside the modeled areas')
                nat, pyt = b.areas(), areas_mundo(py.vivo)
                for n in AREAS:
                    if nat[n] != pyt[n]:
                        k = next(k for k in range(len(nat[n])) if nat[n][k] != pyt[n][k])
                        teste.fail(f'{nome}: area {n} differs at +0x{k:x}: native {nat[n][k]} python {pyt[n][k]}')
                cap = next(seq)
                teste.assertEqual(estado(nat), cap['estado'])
                for e, unidade, valor in b.escritas_8a:
                    type(teste).escritas_8a[(hex(e), valor)] = type(teste).escritas_8a.get((hex(e), valor), 0) + 1
                return parada_n

            def definir_ataque(self, i, modo, ref):
                return self._par(lambda: b.definir_ataque(i, modo, ref), lambda: py.definir_ataque(i, modo, ref))

            def projeteis(self):
                return self._par(b.projeteis, py.projeteis)

            def preludio(self, i):
                return self._par(lambda: b.preludio(i), lambda: py.preludio(i))

            def ramo(self, i, checkpoint=False):
                return self._par(lambda: b.ramo(i, checkpoint_ataque=checkpoint), lambda: py.ramo(i, checkpoint))

            def unidades(self):
                return py.unidades()

            def pool_ativo(self):
                return py.pool_ativo()

        ultimo = []
        conduzir(nome, Par(), lambda seg, q, un, parada: ultimo.append((seg, q, parada)))
        self.assertEqual(len(ultimo), len(captura))
        type(self).segmentos += len(ultimo)
        type(self).quadros += ultimo[-1][1]
        type(self).paradas[nome] = ultimo[-1][2]
        return ultimo

    def test_melee_monster_chain_to_physical_death(self):
        fim = self.lockstep('melee-monster-to-death')
        self.assertEqual(fim[-1][2], 'iagUnitSendMessage')

    def test_ranged_monster_chain_to_physical_death(self):
        fim = self.lockstep('ranged-monster-to-death')
        self.assertEqual(fim[-1][2], 'iagUnitSendMessage')

    def test_named_stops_in_the_chain(self):
        for nome, parada in (('diplomacy-stop-ai-attacker', 'PlayerAAttaqueSet'),
                             ('audio-stop-visible-attacker', 'EnginGetVolume'),
                             ('level-stop-soldier-kill', 'EnginSetLevelExperience')):
            with self.subTest(nome):
                self.assertEqual(self.lockstep(nome)[-1][2], parada)

    def test_branch_and_set_attack_entries(self):
        for nome, c in CENARIOS.items():
            if c['tipo'] in ('ramo', 'definir'):
                with self.subTest(nome):
                    self.lockstep(nome)


if __name__ == '__main__':
    unittest.main()
