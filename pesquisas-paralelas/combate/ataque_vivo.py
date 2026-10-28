"""Live attack chain over one shared Core world (intact EXE 6c556520…43fb).

`definir_ataque` is SetAttaqueEngin 0x445a36. `ramo_estado_ataque` is the
EnginNextEtape state-1/24 branch 0x456886..0x4568ad (exit 0x454ccd), which
validates the order's target and calls CalculAttaqueEngin 0x451914.
`AtaqueVivo` connects those to the live projectile pool, ProjectileCalcul
0x46fc0f, the unit impact wrapper, damage and Core's physical death. AI
messages, audio, diplomacy, movement and RNG are named dependencies unless
the caller supplies them; nothing is defaulted.
"""
import struct

from alvos_alcance import aliados, alvo_ordem_valido, ordem_apos_reset, ordem_ja_definida, palavra
from alvos_impacto import encontrar_vitima_impacto
from animacao_disparo import ContextoAtaque, calcular_ataque, guardar
from bonus_combate import ConsultaBonusCombate
from consumo_fisico import criar_consumidor_fisico
from grade_impacto import encontrar_estrutura_impacto
from impacto_unidades import ImpactoUnidades
from maquina_projeteis import MaquinaProjeteis
from projeteis import PoolProjeteis
from proximidade_ataque import ConsultaProximidadeAtaque

ENTRADA_ORDEM, ENTRADA_RAMO, SAIDA_RAMO = 0x445a36, 0x456886, 0x454ccd
MODOS_ATAQUE = (1, 3, 5)
MENSAGEM_ALVO_INVALIDO = 0x4a
# Original entry of each dependency the composition never implements itself.
DEPENDENCIAS = {
    'iagUnitSendMessage': 0x4829c8, 'EnginGetVolume': 0x440c5d, 'PlaySnd_PostSound': 0x48aa79,
    'MAJSympathie': 0x475118, 'PlayerResetAllie': 0x46d8cb, 'PlayerAAttaqueSet': 0x46d600,
    'EnginSetLevelExperience': 0x44fb20, 'DeplaceEngin': 0x44930c, 'Random': 0x4704dc,
    'SortilegeEffet': 0x473510, 'AnimBallonStatic': 0x447b2f, 'BatimentGetCase': 0x41aee2,
    'BatimentGetCaseAdjacent': 0x4239a0, 'BatimentAdjacent': 0x42381f,
    'ChercheBatimentProximiteCaveOuSanctuaire': 0x4539f3, 'CalculDirection': 0x477042,
    'CalculDirCase': 0x4770ee, 'SortilegeGetPortee': 0x4746c9, 'SortilegeGetRayonEffet': 0x474734,
    'DecouvreTerrain': 0x476851, 'IllumineTerrain': 0x476cb3, 'EteintTerrain': 0x476e82,
    'CreerExplosion': 0x475710,
}


class DependenciaAtaqueVivo(NotImplementedError):
    """A provider the caller did not supply, raised at the original call boundary."""

    def __init__(self, nome, args):
        self.nome, self.argumentos, self.endereco = nome, tuple(args), DEPENDENCIAS.get(nome)
        local = f' 0x{self.endereco:06x}' if self.endereco else ''
        super().__init__(f'Named dependency {nome}{local}{self.argumentos}')


def tipo_jogador(controle, dono):
    """PlayerGetType 0x46d817: AL = control byte for owners 0..3, otherwise 2."""
    dono &= 255
    return controle[dono] & 255 if dono < 4 else 2


def _estrutura(estruturas, indice, campo):
    indice &= 65535
    if indice >= 1000:
        raise ValueError('Structure ID is outside the 1000-record pool (the original reads beyond it)')
    return estruturas[indice * 276 + campo]


def batiment_en_destruction(estruturas, indice):
    """BatimentEnDestruction 0x41a70b: AL = (structure +5 == 3)."""
    return int(_estrutura(estruturas, indice, 5) == 3)


def batiment_get_player(estruturas, indice):
    """BatimentGetPlayer 0x41a08c: AL = structure +4 (upper EAX bits not modeled)."""
    return _estrutura(estruturas, indice, 4)


def definir_ataque(unidades, indice, modo, referencia, redefinir_ordem):
    """SetAttaqueEngin 0x445a36: AX=unit, DL=mode, BX=reference; returns whether stored.

    The same active order (state 1, +b7, +b8) returns before ResetOrdre. Every
    other call resets the order through `redefinir_ordem` (Core ResetOrdre
    0x44357c) and only then refuses types 5/6/7/9/10/13, modes other than
    1/3/5 and a mode-1 self target. Accepted orders store +2=1, +8a=0, +b7, +b8.
    """
    indice, modo, referencia = indice & 65535, modo & 255, referencia & 65535
    if indice >= 800:
        raise ValueError('Unit ID must be in 0..799')
    u = unidades[indice]
    if ordem_ja_definida(u, modo, referencia):
        return False
    redefinir_ordem(indice)
    registro, aceitou = ordem_apos_reset(u, indice, modo, referencia)
    if aceitou:
        for campo in (2, 0x8a, 0xb7, 0xb8, 0xb9):
            u[campo] = registro[campo]
    return aceitou


def ramo_estado_ataque(ctx, indice, consultar, efetuar, calcular=calcular_ataque):
    """EnginNextEtape branch for unit states 1 and 24, from 0x456886 to the exit.

    `ctx` is the live ContextoAtaque. Mode 1 checks the target record (state
    not 0/4, owner not 200, +72 nonzero); mode 3 asks BatimentEnDestruction and
    BatimentGetPlayer; mode 5 needs no check. A valid order runs one
    CalculAttaqueEngin step. An invalid order queries PlayerGetType(owner): an
    AI owner (2) gets iagUnitSendMessage(unit, 0x4a, 0); otherwise
    SetDeplaceEngin(unit, +7e) is requested before +b8 becomes 0xffff.
    Other modes reach CalculAttaqueEngin untranslated and fail before effects.
    """
    indice &= 65535
    if indice >= 800:
        raise ValueError('Unit ID must be in 0..799')
    u = ctx.unidades[indice]
    if u[0xb7] not in MODOS_ATAQUE:
        raise NotImplementedError(f'CalculAttaqueEngin 0x451914 is translated for modes 1/3/5, not {u[0xb7]}')
    valido = alvo_ordem_valido(ctx.unidades, indice,
        construcao_invalida=lambda ref: consultar('BatimentEnDestruction', (ref,)) & 255,
        dono_construcao=lambda ref: consultar('BatimentGetPlayer', (ref,)) & 255)
    if valido:
        calcular(ctx, indice)
        return
    if consultar('PlayerGetType', (u[0],)) & 255 == 2:
        efetuar('iagUnitSendMessage', (indice, MENSAGEM_ALVO_INVALIDO, 0))
        return
    efetuar('SetDeplaceEngin', (indice, palavra(u, 0x7e)))
    guardar(u, 0xb8, 0xffff)


class _BuscaMundo:
    """Combat's search release (four stores) applied to Core's ContextoBusca."""

    def __init__(self, mundo):
        self.mundo = mundo

    def liberar(self, indice):
        b = self.mundo.busca
        if b.unidade == indice:
            b.unidade = 0xffff
            b.ocupada = b.sucesso = b.ponteiro_rota = 0


class _Recargas:
    def __init__(self, tipos):
        self.tipos = tipos

    def __getitem__(self, tipo):
        if not 0 <= tipo < 26:
            raise KeyError(tipo)
        return struct.unpack_from('<H', self.tipos, tipo * 50 + 0x30)[0]


class _Modificadores:
    """Live Modificateur(owner, selector, type) through the loaded bonus provider."""

    def __init__(self, bonus):
        self.bonus = bonus

    def get(self, chave, _padrao=None):
        dono, tipo, seletor = chave
        return self.bonus.consultar(dono, tipo, seletor)


class _Terreno:
    def __init__(self, mundo):
        self.mundo = mundo

    def get(self, celula, _padrao=0):
        return self.mundo.tiles[celula & 65535]


class AtaqueVivo:
    """SetAttaqueEngin, the attack-state branch and ProjectileCalcul over one Core world.

    Inputs, all explicit and shared by reference: `mundo` (Core world with the
    800 x 276 `unidades` bytearray, 1000 x 276 `estruturas`, `regioes`, `tiles`,
    `descoberto`, `controle_jogadores`, `jogador_local`, `busca`, ResetOrdre,
    SetDeplaceEngin and physical death), the live `PoolProjeteis`, 26 loaded
    DEGAT rows, the loaded 26 x 50 type table, the loaded bonus provider
    (BonusUnidades.consultar), five alliance mask bytes (players 0..4, byte +6),
    the u8 global 0x4965ac and the inherited alert globals 0x4e19c0/0x496acc.
    `contador` mirrors u32 0x508f7c and must be set by the frame driver.
    `consulta(name, args)` and `efeito(name, args)` supply the remaining
    providers; when absent, their calls raise DependenciaAtaqueVivo.
    The pool's `efeito_externo`/`raio_magia` callbacks are taken over here.
    """

    def __init__(self, mundo, pool, danos, tipos, bonus, mascaras, *, bonus_4965ac,
                 ultimo_alerta, celula_alerta, consulta=None, efeito=None):
        if not isinstance(pool, PoolProjeteis):
            raise ValueError('Expected the live PoolProjeteis')
        if len(tipos) != 1300 or len(mascaras) != 5 or len(mundo.estruturas) != 276000:
            raise ValueError('Expected the 26x50 type table, five mask bytes and the 1000-record structure pool')
        self.mundo, self.pool, self.tipos, self.bonus = mundo, pool, tipos, bonus
        self.mascaras = bytes(mascaras)
        self.consulta, self.efeito = consulta, efeito
        self.consumidor = criar_consumidor_fisico(mundo, pool, danos, consulta=self._consulta_dano,
            efeito=self._externo, bonus_4965ac=bonus_4965ac, mortes_sem_experiencia=True)
        self.unidades = self.consumidor.unidades
        self.impacto = ImpactoUnidades(self.unidades, pool, self.consumidor.infligir, self._consulta_impacto,
            self._efeito_impacto, jogador_local=mundo.jogador_local,
            ultimo_alerta=ultimo_alerta, celula_alerta=celula_alerta)
        self.contexto = ContextoAtaque(self.unidades, recargas=_Recargas(tipos), modificadores=_Modificadores(bonus),
            terreno=_Terreno(mundo), largura=mundo.largura, altura=mundo.altura, busca=_BuscaMundo(mundo),
            celula_construcao=lambda *a: self._externa('BatimentGetCase', a),
            celula_construcao_adjacente=lambda *a: self._externa('BatimentGetCaseAdjacent', a),
            adjacente_construcao=lambda *a: self._externa('BatimentAdjacent', a),
            alcance_magia=lambda *a: self._externa('SortilegeGetPortee', a),
            descoberto=lambda celula: self._descoberto(celula, mundo.jogador_local),
            efeito_externo=self._efeito_ataque)
        pool.efeito_externo, pool.raio_magia = self._efeito_projetil, lambda *a: self._externa('SortilegeGetRayonEffet', a)
        self.maquina = MaquinaProjeteis(pool, aleatorio=lambda marcador: self._externa('Random', (marcador,)))

    @property
    def contador(self):
        return self.impacto.contador

    @contador.setter
    def contador(self, valor):
        self.impacto.contador = valor & 0xffffffff

    # Public entries.
    def definir_ataque(self, indice, modo, referencia):
        return definir_ataque(self.unidades, indice, modo, referencia, self.mundo.redefinir_ordem)

    def ramo(self, indice, calcular=calcular_ataque):
        self.contexto.chamadas.clear()
        ramo_estado_ataque(self.contexto, indice, self._consulta_ramo, self._efeito_ramo, calcular)

    def calcular_projeteis(self):
        """ProjectileCalcul 0x46fc0f; animation uses the low byte of `contador`."""
        self.maquina.calcular(self.contador & 255)

    # Providers.
    def _externa(self, nome, args):
        if self.consulta is None:
            raise DependenciaAtaqueVivo(nome, args)
        return self.consulta(nome, tuple(args))

    def _externo(self, nome, args):
        if self.efeito is None:
            raise DependenciaAtaqueVivo(nome, args)
        return self.efeito(nome, tuple(args))

    def _descoberto(self, celula, jogador):
        return int((self.mundo.descoberto[jogador & 255][celula & 65535] & 31) == 0)

    def _regioes(self):
        return struct.pack('<65536H', *self.mundo.regioes)

    def _consulta_dano(self, nome, args):
        if nome == 'TerrainEstDecouvert':
            return self._descoberto(*args)
        if nome == 'Modificateur':
            return ConsultaBonusCombate(self.bonus)(nome, args)
        if nome == 'ChercheTypeEnginProximite':
            return ConsultaProximidadeAtaque(self.unidades, self._regioes())(nome, args)
        return self._externa(nome, args)

    def _consulta_impacto(self, nome, args):
        if nome == 'ChercheIndiceBatiment':
            return encontrar_estrutura_impacto(self._regioes(), *args)
        if nome == 'ChercheIndiceEnginCible':
            return encontrar_vitima_impacto(self.unidades, *args)
        if nome == 'PlayerGetType':
            return tipo_jogador(self.mundo.controle_jogadores, *args)
        if nome == 'PlayerEstAllie':
            return int(aliados(args[0], args[1], self.mascaras))
        if nome == 'BatimentGetPlayer':
            return batiment_get_player(self.mundo.estruturas, *args)
        return self._externa(nome, args)

    def _consulta_ramo(self, nome, args):
        if nome == 'PlayerGetType':
            return tipo_jogador(self.mundo.controle_jogadores, *args)
        if nome == 'BatimentEnDestruction':
            return batiment_en_destruction(self.mundo.estruturas, *args)
        if nome == 'BatimentGetPlayer':
            return batiment_get_player(self.mundo.estruturas, *args)
        return self._externa(nome, args)

    def _efeito_ramo(self, nome, args):
        if nome == 'SetDeplaceEngin':
            return self.mundo.definir_movimento(*args)
        return self._externo(nome, args)

    def _efeito_impacto(self, nome, args):
        if nome == 'SetDeplaceEngin':
            return self.mundo.definir_movimento(*args)
        if nome == 'SetAttaqueEngin':
            return self.definir_ataque(*args)
        return self._externo(nome, args)

    def _efeito_ataque(self, nome, args):
        if nome == 'ProjectileInit':
            return self.pool.iniciar(*args)
        if nome == 'InfligeDegat':
            return self.impacto.infligir(*args)
        if nome == 'SetDeplaceEngin':
            return self.mundo.definir_movimento(*args)
        if nome == 'ResetOrdre':
            return self.mundo.redefinir_ordem(*args)
        return self._externo(nome, args)

    def _efeito_projetil(self, nome, args):
        if nome == 'InfligeDegat':
            return self.impacto.receber(nome, args)
        return self._externo(nome, args)
