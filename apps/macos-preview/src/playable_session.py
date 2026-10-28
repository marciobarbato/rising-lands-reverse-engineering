"""Explicit exercise policy connecting committed providers to a live world.

The map, cargo workflow and clock are app fixtures. They are not reconstructed
mission rules. Combat intentionally calls the bounded direct-unit consumer;
the original InfligeDegat reaction/diplomacy/presentation wrapper is excluded.
"""
import struct

from alvos_alcance import a_portee, linha_de_tiro, ordem_apos_reset, ordem_ja_definida
from alvos_impacto import encontrar_vitima_impacto
from animacao_disparo import ContextoAtaque, BuscaAtaque, calcular_ataque
from inicializacao_ataque import definir_tipo, CaracteristicasTipo
from bonus_unidades import BonusUnidades, capacidade_tipo
from bonus_combate import ConsultaBonusCombate
from proximidade_ataque import ConsultaProximidadeAtaque
from consumo_dano import ConsumidorDanoUnidade, LimiteMorte
from combate import avancar_recarga
from extracao import RecursosTerreno


class SessaoJogavel:
    def __init__(self, preview):
        self.preview, self.world = preview, preview.world
        self.rows = [memoryview(self.world.unidades)[i * 276:(i + 1) * 276] for i in range(800)]
        self.types = b''.join(bytes.fromhex(t['registro_memoria_hex']) for t in preview.catalog)
        # These loaded zeros and the silent observer are explicit fixture inputs.
        self.bonus = BonusUnidades(bytearray(1872), tipos_unidades=self.types)
        self.world.controle_jogadores[:] = bytes([1] * 4)
        self.observer = 3
        self.attacks, self.cargo, self.delivered, self.hits = set(), {}, 0, 0
        self.boundary = None
        self.depot = [2, 12]
        self.supply = [4, 9]
        self.resources = RecursosTerreno(preview.research.buildings.terreno)
        c = self.supply[1] * 256 + self.supply[0]
        self.resources.terreno.tipos[c], self.resources.terreno.quantidades[c] = 0x43, 8
        for i, (x, y, kind, owner) in enumerate(((2, 4, 0, 0), (2, 9, 7, 0), (10, 4, 0, 1))):
            self.world.ocupar(i, self.world.palavra(i, 8), False)
            u = self.rows[i]
            u[:] = bytes(276)
            u[0], u[2], u[0x72] = owner, 7, 1
            table = preview.catalog[kind]
            props = CaracteristicasTipo(table['raio_visao'], table['alcance_ataque_quadrado_u16'], table['recarga'])
            definir_tipo(u, i, x + y * 256, 9, kind, props, capacidade_tipo,
                         self.bonus.consultar, BuscaAtaque())
            struct.pack_into('<H', u, 0x9a, 100)
            struct.pack_into('<I', u, 0x104, 0xffffffff)
            struct.pack_into('<I', u, 0x10c, 0xffffffff)
            # Base-body rendering contract only; selected/active effects absent.
            struct.pack_into('<H', u, 0x74, 100)
            self.world.ocupar(i, x + y * 256, True)
            self.world.limites_fadiga[kind] = table['fadiga']
            preview.trails[i], preview.routes[i], preview.plans[i] = [[x, y]], [], 'sem ordem'
        self.context = ContextoAtaque(self.rows, recargas={t['id']: t['recarga'] for t in preview.catalog},
                                      largura=16, altura=16, descoberto=lambda c: self.query('TerrainEstDecouvert', (c,)),
                                      efeito_externo=self.effect)
        self.query_bonus = ConsultaBonusCombate(self.bonus, self.query)
        self.consumer = ConsumidorDanoUnidade(self.rows, [t['danos_por_alvo'] for t in preview.catalog],
                                             consulta=self.query_damage, efeito=self.effect,
                                             jogador_local=self.observer)
        preview.log('Treino livre: mova o soldado até o adversário e use Atacar. Leve sacolas ao depósito com o construtor.')

    def controllable(self, index):
        if self.rows[index][0] != 0:
            raise ValueError('Esta unidade pertence ao adversário; selecione uma unidade do jogador 0.')
        if self.boundary:
            raise ValueError('O treino chegou a uma rotina pendente. Reinicie o cenário para continuar.')

    def query_damage(self, name, args):
        grid = struct.pack('<65536H', *self.world.regioes)
        return ConsultaProximidadeAtaque(self.rows, grid, self.query_bonus)(name, args)

    def query(self, name, args):
        if name == 'TerrainEstDecouvert':
            # Camera 3 stays hidden. The exercise UI is an omniscient observer.
            return int(not (self.world.descoberto[self.observer][args[0] & 65535] & 31))
        raise NotImplementedError('Consulta externa ainda indisponível: ' + name)

    def effect(self, name, args):
        if name == 'iagUnitSendMessage':
            unit = self.rows[args[0]]
            owner = unit[0]
            group = struct.unpack_from('<I', unit, 0x10c)[0]
            if (owner < 4 and self.world.controle_jogadores[owner] != 2) or group == 0xffffffff:
                return
        elif name == 'InfligeDegat':
            cell, mode, attacker, direction, flag = args
            victim = encontrar_vitima_impacto(self.rows, cell, 65535, flag)
            if victim != 65535:
                try:
                    self.consumer.infligir(victim, mode, attacker, direction)
                except LimiteMorte:
                    self.stop('Morte da unidade ainda depende de rotinas externas; o golpe final não foi aplicado.')
                    return
                self.hits += 1
                self.preview.log(f'Golpe direto: U{attacker} → U{victim}; vida {self.world.palavra(victim, 0x9a)}.')
            return
        raise NotImplementedError('Efeito externo ainda indisponível: ' + name)

    def interact(self, operation, unit, target):
        self.controllable(unit)
        if operation == 'attack':
            if isinstance(target, bool) or not isinstance(target, int) or target not in (0, 1, 2):
                raise ValueError('Alvo inválido.')
            if self.rows[unit][1] != 0 or target == unit or self.rows[target][0] == 0:
                raise ValueError('Use o soldado e escolha o adversário.')
            if self.rows[unit][0x86] or self.rows[unit][0x87] or self.rows[unit][2] == 2:
                raise ValueError('Espere o soldado terminar o movimento antes de atacar.')
            if not a_portee(self.rows, unit, 1, target) or not linha_de_tiro(
                    self.rows[unit], self.world.palavra(target, 0x7c), {}, 16, 16):
                raise ValueError('Aproxime o soldado do adversário: golpe corpo a corpo exige uma célula vizinha.')
            if not ordem_ja_definida(self.rows[unit], 1, target):
                self.world.redefinir_ordem(unit)
                updated, accepted = ordem_apos_reset(self.rows[unit], unit, 1, target)
                if not accepted:
                    raise ValueError('A ordem de ataque foi recusada.')
                self.rows[unit][:] = updated
            self.attacks.add(unit)
            self.preview.plans[unit] = 'golpe direto em treino; mira, animação e recarga recuperadas'
            self.preview.log(f'U{unit}: ataque contínuo contra U{target}. Use Mover para interromper.')
        elif operation in ('collect', 'deposit'):
            if unit != 1 or self.rows[unit][2] != 7:
                raise ValueError('Use o construtor parado sobre a célula indicada.')
            position = [self.world.palavra(unit, 8) & 255, self.world.palavra(unit, 8) >> 8]
            if operation == 'collect':
                if position != self.supply or unit in self.cargo:
                    raise ValueError('Leve o construtor até a sacola (4, 9), sem carga.')
                cell = self.supply[0] + self.supply[1] * 256
                if not self.resources.terreno.quantidades[cell]:
                    raise ValueError('A sacola está vazia.')
                self.cargo[unit] = self.resources.retirar_sacola(cell)
                self.preview.log('Uma unidade de comida retirada da sacola; leve a carga até o depósito (2, 12).')
            else:
                if position != self.depot or unit not in self.cargo:
                    raise ValueError('Leve o construtor com carga até o depósito (2, 12).')
                resource = self.cargo[unit]
                self.preview.research.buildings.adicionar(0, resource, 1, 0)
                del self.cargo[unit]
                self.delivered += 1
                self.preview.log(f'Depósito recebido. Entregas do exercício: {self.delivered}.')
        else:
            raise ValueError('Interação desconhecida.')

    def stop(self, message):
        if not self.boundary:
            self.boundary = message
            self.preview.log(message)
        self.preview.paused = True

    def step(self):
        if self.boundary:
            self.preview.paused = True
            return
        for index in tuple(self.attacks):
            u = self.rows[index]
            if u[2] != 1:
                self.attacks.remove(index)
                continue
            recharge = avancar_recarga(self.world.palavra(index, 0x102), self.context.recargas[u[1]])
            self.world.palavra(index, 0x102, recharge)
            self.context.chamadas.clear()
            calcular_ataque(self.context, index)

    def state(self):
        cell = self.supply[0] + self.supply[1] * 256
        return {'depot': self.depot, 'supply': self.supply,
                'remaining': self.resources.terreno.quantidades[cell], 'cargo': dict(self.cargo),
                'delivered': self.delivered, 'hits': self.hits, 'boundary': self.boundary,
                'objective': 'Treino livre: leve sacolas ao depósito e pratique golpes com o soldado.'}
