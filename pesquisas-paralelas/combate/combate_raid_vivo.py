"""Combat entries over original live memory, including real M2.3 raid states.

The public methods mutate the supplied MemoriaQuadro-compatible memory.
No hidden initial state or callbacks are manufactured. Foreign effects are
explicit providers or DependenciaCombateRaid at the original callee entry.
SetDyingEngin and RetireEngin remain Core-owned providers.
"""
from ambiente_combate_raid import ROOT  # noqa: F401
from alvos_alcance import encontrar_alvo, aliados
from animacao_disparo import ContextoAtaque, calcular_ataque
from ataque_vivo import (_BuscaMundo, _Modificadores, _Recargas, _Terreno, definir_ataque,
                         ramo_estado_ataque, DEPENDENCIAS as DEPENDENCIAS_ATAQUE)
from bonus_combate import ConsultaBonusCombate
from consumo_dano import ConsumidorDanoUnidade
from grade_impacto import encontrar_estrutura_impacto
from impacto_unidades import ImpactoUnidades
from alvos_impacto import encontrar_vitima_impacto
from morte_dano import MorteDanoUnidade
from dano_estrutura_raid import DanoEstruturaRaid
from projeteis import PoolProjeteis
from maquina_projeteis import MaquinaProjeteis
from proximidade_ataque import ConsultaProximidadeAtaque
from bonus_unidades import BonusUnidades
from chamadas_quadro_core import terreno_esta_descoberto, caso_estrutura, aleatorio_mundo_memoria
from selecao_ordens import SelecaoOrdens, chamar_som
from mundo_vivo import mundo_vivo
from solucionador_vivo import SolucionadorCaminhosVivo

DEPENDENCIAS_RAID = dict(DEPENDENCIAS_ATAQUE, SetDyingEngin=0x444938, RetireEngin=0x457058,
                         iagVilleSendMessage=0x484808, VoixOffAsk=0x41a1ac,
                         PlaySnd_StopSound=0x48aac0, TypeBatimentGetDegat=0x418b8a,
                         BatimentInfligeDegat=0x41a2c1, BatimentGetVolume=0x41a0ab,
                         SortilegeGetTempsFin=0x47474f, InfligeDegat=0x450874)


class DependenciaCombateRaid(NotImplementedError):
    def __init__(self, nome, argumentos):
        self.nome, self.argumentos = nome, tuple(argumentos)
        self.endereco = DEPENDENCIAS_RAID[nome]
        super().__init__(f'{nome} at 0x{self.endereco:06x}{self.argumentos}; prior effects retained')


class _GradeRaid:
    def __init__(self, m):
        self.m = m

    def get(self, cell, default=None):
        return self.m.u16(self.m.u32(0x4e0f38) + 2 * (cell & 65535))


class _MaquinaRaid(MaquinaProjeteis):
    """The inherited presentation byte is live, including stores before a stop."""
    def __init__(self, m, pool, random, duration):
        self.m, self.pool, self.aleatorio, self.tempo_magia = m, pool, random, duration

    campo_4dfb44 = property(lambda self:self.m.u8(0x4dfb44), lambda self,v:self.m.u8(0x4dfb44,v))


class _ConsumidorRaid(ConsumidorDanoUnidade):
    """Existing damage algorithm with camera/bonus globals read live at each use."""
    def __init__(self, m, units, rows, query, effect, death):
        self.m, self.unidades, self.danos = m, units, rows
        self.consulta, self.efeito = query, effect
        self.morte, self.morte_sem_experiencia = death, death.sem_experiencia
        self.__post_init__()

    jogador_local = property(lambda self: self.m.u8(0x508041))
    bonus_4965ac = property(lambda self: self.m.u8(0x4965ac))
    danos_modo4 = property(lambda self: (self.m.u8(0x49716c), self.m.u8(0x49716e)))


class _ImpactoRaid(ImpactoUnidades):
    """The wrapper's clock/camera/alert fields are original live scalar addresses."""
    def __init__(self, m, units, pool, consume, query, effect):
        self.m, self.unidades, self.pool = m, units, pool
        self.consumir, self.consulta, self.efeito = consume, query, effect
        self.__post_init__()

    contador = property(lambda self: self.m.u32(0x508f7c))
    jogador_local = property(lambda self: self.m.u8(0x508041))
    ultimo_alerta = property(lambda self: self.m.u32(0x4e19c0), lambda self,v:self.m.u32(0x4e19c0,v))
    celula_alerta = property(lambda self: self.m.u16(0x496acc), lambda self,v:self.m.u16(0x496acc,v))


class CombateRaidVivo:
    """Live attack/order/target/projectile/damage composition.

    ``consulta(name, args) -> int`` and ``efeito(name, args)`` may mutate the
    same memory in place. Missing foreign providers raise at their entries;
    exceptions retain all earlier effects. Re-entering repeats effects.
    Buffer bases must stay allocated and must not be replaced during a call.
    Core movement and Economy bonus queries are committed providers.
    Full register APIs are supplied for SetAttaqueEngin and EnginTrouveCible.
    The state-1/24 branch, attack, damage and projectile methods are void APIs;
    path-dependent unconsumed EAX/flags are not claimed by those methods.
    """
    def __init__(self, memoria, *, consulta=None, efeito=None, mundo=None, som=None):
        self.m, self.consulta, self.efeito, self.som = memoria, consulta, efeito, som
        self.mundo = mundo if mundo is not None else mundo_vivo(memoria, SolucionadorCaminhosVivo(memoria))
        self.ordens = SelecaoOrdens(memoria)
        self.bonus = BonusUnidades.da_memoria(memoria)
        self.tipos = memoria.vista(0x4965ae, 1300)
        base = memoria.u32(0x4e19a0)
        self.unidades = tuple(memoria.vista(base + 276 * i, 276) for i in range(800))
        self.danos = tuple(memoria.vista(memoria.u32(memoria.u32(0x4e199c) + 4 * i), 27) for i in range(26))
        self.pool = PoolProjeteis(memoria.vista(memoria.u32(0x5080f0), 5600), efeito_externo=self._efeito,
            raio_magia=lambda *a:self._query('SortilegeGetRayonEffet', a))
        self.maquina = _MaquinaRaid(memoria, self.pool, lambda marcador:self._query('Random', (marcador,)),
                                   lambda *a:self._query('SortilegeGetTempsFin', a))
        self.dano_estrutura = DanoEstruturaRaid(memoria, self._query, self._emissor(0x41a331))
        self.grade = _GradeRaid(memoria)
        self.consumidor = _ConsumidorRaid(memoria, self.unidades, self.danos, self._query, self._emissor(0x45063f),
                                        MorteDanoUnidade(self.unidades, self.pool, self._efeito))

    def _externa(self, name, args):
        if self.consulta is None:
            raise DependenciaCombateRaid(name, args)
        return self.consulta(name, tuple(args))

    def _externo(self, name, args):
        if self.efeito is None:
            raise DependenciaCombateRaid(name, args)
        return self.efeito(name, tuple(args))

    def _mascaras(self):
        p = self.m.u32(0x5080a8)
        return bytes(self.m.u8(p + 20 * i + 6) for i in range(5))

    def _regioes(self):
        return self.m.vista(self.m.u32(0x4e0f38), 131072)

    def _query(self, name, args):
        m = self.m
        if name == 'Modificateur':
            return ConsultaBonusCombate(self.bonus)(name, args)
        if name == 'TerrainEstDecouvert':
            cell = args[0]
            player = args[1] if len(args) == 2 else m.u8(0x508041)
            return terreno_esta_descoberto(m, cell, player)['EAX'] & 255
        if name == 'ChercheTypeEnginProximite':
            return ConsultaProximidadeAtaque(self.unidades, self._regioes())(name, args)
        if name == 'ChercheIndiceBatiment':
            return encontrar_estrutura_impacto(self._regioes(), *args)
        if name == 'ChercheIndiceEnginCible':
            return encontrar_vitima_impacto(self.unidades, *args)
        if name == 'PlayerGetType':
            owner = args[0] & 255
            return m.u8(m.u32(0x5080a8) + owner * 20 + 1) if owner < 4 else 2
        if name == 'PlayerEstAllie':
            return int(aliados(*args, self._mascaras()))
        if name in ('BatimentGetPlayer', 'BatimentGetType', 'BatimentEnDestruction'):
            index = args[0] & 65535
            if index >= 1000:
                raise ValueError('Structure ID is outside 0..999')
            rec = 0x49a0c8 + 276 * index
            if name == 'BatimentEnDestruction':
                return int(m.u8(rec + 5) == 3)
            return m.u8(rec + (4 if name == 'BatimentGetPlayer' else 8))
        if name == 'BatimentGetCase':
            return caso_estrutura(m, args[0])['EAX'] & 65535
        if name == 'EnginGetVolume':
            return self.ordens._volume_unidade(args[0])
        if name == 'BatimentGetVolume':
            return self.ordens._volume_estrutura(args[0])
        if name == 'Random':
            return aleatorio_mundo_memoria(m)['EAX']
        return self._externa(name, args)

    def _emissor(self, chamada):
        """Bind the single PostSound CALL of this emitter; nested effects keep their own origin."""
        return lambda name, args: self._efeito(name, args, chamada=chamada)

    def _efeito(self, name, args, *, chamada=None):
        if name == 'EnginGetVolume':
            return self._query(name, args)
        if name == 'PlaySnd_PostSound':
            selector, code, flags, volume, reference = args
            if selector == 0x50 and isinstance(reference, int) and reference < 800:
                reference = self.m.u32(0x4e19a0) + 276 * reference + 0x104
            elif reference == '0x496ac8':
                reference = 0x496ac8
            if self.som is not None:
                if chamada is None:
                    raise ValueError('Original PostSound call site required')
                return chamar_som(self.som, name,
                    dict(EAX=selector, EDX=code, EBX=reference, ECX=flags), [volume], chamada)
            return self._externo(name, (selector, code, flags, volume, reference))
        if name == 'ResetOrdre':
            return self.mundo.redefinir_ordem(*args)
        if name == 'SetDeplaceEngin':
            return self.mundo.definir_movimento(*args)
        if name == 'DeplaceEngin':
            return self.mundo.deslocar(*args)
        if name == 'SetAttaqueEngin':
            return self.definir_ataque(*args)
        if name == 'ProjectileInit':
            return self.pool.iniciar(*args)
        if name == 'InfligeDegat':
            return self.infligir(*args)
        return self._externo(name, args)

    def definir_ataque(self, indice, modo, referencia):
        return definir_ataque(self.unidades, indice, modo, referencia, self.mundo.redefinir_ordem)

    def set_attaque_engin(self, registradores):
        """Core order callback: AX unit, DL mode, BX target; exact EAX/EDX, others kept."""
        r = dict(registradores)
        unit, mode, target = r['EAX'] & 65535, r['EDX'] & 255, r['EBX'] & 65535
        if unit >= 800:
            raise ValueError('Unit ID is outside 0..799')
        u = self.unidades[unit]
        same = u[2] == 1 and u[0xb7] == mode and self.m.u16(self.m.u32(0x4e19a0)+276*unit+0xb8) == target
        self.definir_ataque(unit, mode, target)
        r['EAX'] = 1 if same else u[1]
        r['EDX'] = self.m.u32(0x4e19a0) + 276 * unit
        return r

    def ordem_core(self, unidade, modo, referencia):
        """SelecaoOrdens definir_ataque callback: three arguments, exact EAX/EDX result."""
        r = self.set_attaque_engin(dict(EAX=unidade, EDX=modo, EBX=referencia))
        return {k:r[k] for k in ('EAX','EDX')}

    def encontrar_alvo(self, indice):
        indice &= 65535
        if indice >= 800:
            raise ValueError('Unit ID is outside 0..799')
        return encontrar_alvo(self.unidades, indice, self.grade, self._mascaras())

    def engin_trouve_cible(self, registradores):
        return dict(registradores, EAX=self.encontrar_alvo(registradores['EAX']))

    def _contexto(self):
        return ContextoAtaque(self.unidades, recargas=_Recargas(self.tipos), modificadores=_Modificadores(self.bonus),
            terreno=_Terreno(self.mundo), largura=self.mundo.largura, altura=self.mundo.altura,
            busca=_BuscaMundo(self.mundo),
            celula_construcao=lambda *a: self._query('BatimentGetCase', a),
            celula_construcao_adjacente=lambda *a: self._query('BatimentGetCaseAdjacent', a),
            adjacente_construcao=lambda *a: self._query('BatimentAdjacent', a),
            alcance_magia=lambda *a: self._query('SortilegeGetPortee', a),
            descoberto=lambda cell: self._query('TerrainEstDecouvert', (cell,)), efeito_externo=self._emissor(0x4525a1))

    def calcular_ataque(self, indice):
        indice &= 65535
        if indice >= 800:
            raise ValueError('Unit ID is outside 0..799')
        if self.unidades[indice][1] >= 26:
            raise ValueError('Unit type is outside 0..25')
        calcular_ataque(self._contexto(), indice)

    def ramo(self, indice):
        ramo_estado_ataque(self._contexto(), indice, self._query, self._efeito)

    def calcular_projeteis(self):
        self.maquina.calcular(self.m.u32(0x508f7c) & 255)

    def infligir_unidade(self, vitima, modo, atacante, direcao=0):
        if modo & 255 not in (1, 3, 4):
            raise NotImplementedError('Live raid consumer supports initialized damage modes 1/3/4')
        return self.consumidor.infligir(vitima, modo, atacante, direcao)

    def infligir_estrutura(self, indice, dano, dono_fonte):
        self.dano_estrutura.infligir(indice, dano, dono_fonte)

    def infligir_estrutura_registradores(self, regs):
        return self.dano_estrutura.registradores(regs)

    def infligir(self, celula, modo, atacante, direcao, flag):
        celula, modo, atacante, direcao, flag = celula & 65535, modo & 255, atacante & 65535, direcao & 255, flag & 255
        if modo not in (1, 3, 4) or (modo == 4 and direcao not in (29, 30)):
            raise NotImplementedError('Initialized InfligeDegat modes are 1/3 and 4 with direction 29/30')
        if not flag:
            building = self._query('ChercheIndiceBatiment', (celula,)) & 65535
            if building != 65535:
                return self._infligir_batiment(celula, building, modo, atacante, direcao)
        impact = _ImpactoRaid(self.m, self.unidades, self.pool, self.infligir_unidade,
            lambda name, args: 65535 if name == 'ChercheIndiceBatiment' else self._query(name, args), self._emissor(0x4510b1))
        return impact.infligir(celula, modo, atacante, direcao, flag)

    def _infligir_batiment(self, celula, alvo, modo, fonte, direcao):
        if alvo >= 1000:
            raise ValueError('Decoded structure ID is outside the 1000-record pool')
        if modo in (1, 4) and fonte >= 800:
            raise ValueError('Unit source is outside 0..799')
        if modo == 1:
            u = self.unidades[fonte]
            if u[1] >= 26:
                raise ValueError('Unit source type is outside 0..25')
            damage = (self.danos[u[1]][26] + self._query('Modificateur', (u[0], 5, u[1]))) & 0xffffffff
            owner = u[0]
            self._efeito('iagVilleSendMessage', (alvo, 4, fonte))
        elif modo == 3:
            target_type = self._query('BatimentGetType', (alvo,))
            source_type = self._query('BatimentGetType', (fonte,))
            damage = self._query('TypeBatimentGetDegat', (source_type, 3, target_type))
            owner = self._query('BatimentGetPlayer', (fonte,)) & 255
        else:
            owner = self.unidades[fonte][0]
            damage = self.m.u16(0x49716c if direcao == 29 else 0x49716e) // 2
        self.infligir_estrutura(alvo, damage & 65535, owner)
        value = self._query('Random', (0x21,))
        self.pool.iniciar(15 + (value & 1), celula, celula, 0, 0, 0, 0, 0, 0)
        target_owner = self._query('BatimentGetPlayer', (alvo,)) & 255
        if self._query('PlayerEstAllie', (owner, target_owner)) & 255:
            self._efeito('MAJSympathie', (self._query('BatimentGetPlayer', (alvo,)) & 255, owner, 10))
            self._efeito('MAJSympathie', (self._query('BatimentGetPlayer', (alvo,)) & 255, owner, 6))
            self._efeito('PlayerResetAllie', (owner, self._query('BatimentGetPlayer', (alvo,)) & 255))
            self._efeito('PlayerResetAllie', (self._query('BatimentGetPlayer', (alvo,)) & 255, owner))
        self._efeito('PlayerAAttaqueSet', (owner, self._query('BatimentGetPlayer', (alvo,)) & 255))

    def iniciar_morte(self, indice):
        return self._externo('SetDyingEngin', (indice & 65535,))

    def retirar(self, indice):
        return self._externo('RetireEngin', (indice & 65535,))
