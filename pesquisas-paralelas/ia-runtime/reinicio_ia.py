"""AI table providers: IaReset 0x47f36e (MissionLoad tail), IaAlloc 0x47fb15, IAResetAttaque 0x47c162.

Exact translation of the original routines and of every AI routine they reach,
operating on a ``MemoriaDeclarada`` with the original absolute addresses and
widths. Routines owned by other fronts are *world queries*, called through a
provider object by their original name with the original call site:

    PlayerGetType(jogador)            -> EAX (AL used)      RechercheGetNiveau(jogador, ramo) -> EAX (AX used)
    RechercheSetBranche(jogador, ramo)                        MissionGetNum() -> EAX (AX used)
    EnginEstVivant(unidade) -> EAX (AL used)                  EnginGetType(unidade) -> EAX (AL used)
    EnginGetEtat(unidade) -> EAX (AL used)                    TypeEnginEstMonstre(tipo) -> EAX (AL used)
    EnginSetPlayer(unidade, jogador)                          BatimentExiste(estrutura) -> EAX (AL used)
    BatimentGetPlayer(estrutura) -> EAX (AL used)             BatimentGetType(estrutura) -> EAX (AL used)
    GetRessource(jogador) -> four u16 outputs

each called as ``metodo(*args, sitio=original_call_address)``. A missing
provider raises ``DependenciaIA`` at its call site; every store made before it
is retained. IaAlloc's file I/O and clock are declared bindings
(``timeGetTime``, ``debugSymLoad``, ``iaProbLoadBinaryRules``, ``debugSymUnload``).
"""
from cadencia import proximo_aleatorio
from memoria_ia_runtime import s32, u32

UNIDADE = 0x114
UNIDADES = 0x4e19a0          # u32 pointer to the 800-unit pool
JOGADORES = 0x5080a8         # u32 pointer to the 4 player records of 20 bytes
GRUPOS = 0x51a9e0            # 100 groups x 32
DICA_GRUPO = 0x51b660        # u32 next free-group hint
POOLS = 0x51b664             # per player 0x60: u32 group-list heads by group type
CIDADES = 0x51b84c           # per player 0x7c
RECURSOS = 0x51ba3c          # per player 0xa8
GUERRA = 0x51bcfc            # per player 0x1144
CONTEXTOS = 0x51a98c         # per player 16
ESTADO_ALEATORIO = 0x498db4

# Absolute regions the translated routines may touch (exact original footprint).
REGIOES_REINICIO = (
    (0x498464, 0x498468, 'research thresholds 0x498464[4]'),
    (0x4989f8, 0x4989f8 + 26 * 4, 'unit-type masks u32[26]'),
    (0x498c10, 0x498c20, 'city mode values u32[4]'),
    (0x498c38, 0x498ca0, 'resource mode tables'),
    (0x498cb0, 0x498cd8, 'war mode tables'),
    (0x498cf4, 0x498d5c, 'war unit weights u32[26]'),
    (ESTADO_ALEATORIO, ESTADO_ALEATORIO + 4, 'iaRandom state'),
    (0x498ec4, 0x498ec4 + 17 * 4, 'group type -> behavior bytes'),
    (UNIDADES, UNIDADES + 4, 'unit pool pointer'),
    (JOGADORES, JOGADORES + 4, 'player table pointer'),
    (0x50a9cc, 0x50a9cd, 'monster byte +16'),
    (0x50ae80, 0x50ae84, 'monster u32'),
    (0x50af84, 0x50b134, 'monster group spec 16x26 + counts 16'),
    (0x50b134, 0x50b184, 'monster group list'),
    (0x512320, 0x514900, 'task pool, free list and five contexts'),
    (CONTEXTOS, 0x521350, 'AI contexts, groups, pools, cities, resources, war'),
)
REGIOES_ALOCACAO = (
    (0x498c10, 0x498c20, 'city mode values'),
    (0x498c38, 0x498c94, 'resource mode tables'),
    (0x498cb0, 0x498cd4, 'war mode tables'),
    (0x498cf4, 0x498d5c, 'war unit weights'),
    (ESTADO_ALEATORIO, ESTADO_ALEATORIO + 4, 'iaRandom state'),
    (0x51bcdc, 0x51bcfc, 'resource constants'),
    (0x521350, 0x521368, 'war constants'),
)
REGIOES_ATAQUES = ((0x50d5b4, 0x50d9a0, 'attack table 100x10 and count'),)


class DependenciaIA(NotImplementedError):
    """A world query or binding the caller did not provide, at its original call site."""

    def __init__(self, rotina, sitio):
        self.rotina, self.sitio = rotina, sitio
        super().__init__(f'{rotina} required at 0x{sitio:08x}; earlier stores retained')


class NaoTerminaNoOriginal(RuntimeError):
    """The original would loop forever from here; earlier stores retained."""

    def __init__(self, sitio, motivo):
        self.sitio = sitio
        super().__init__(f'{motivo} (original 0x{sitio:08x})')


def _s8(valor):
    """movsx of DL."""
    valor &= 0xff
    return valor - 0x100 if valor & 0x80 else valor


class _Rotinas:
    def __init__(self, memoria, mundo):
        self.m, self.mundo = memoria, mundo

    # ------------------------------------------------------------ helpers
    def _chamar(self, nome, sitio, *args):
        funcao = getattr(self.mundo, nome, None) if self.mundo is not None else None
        if funcao is None:
            raise DependenciaIA(nome, sitio)
        return funcao(*args, sitio=sitio)

    def _unidade(self, indice):
        return u32(self.m.u32(UNIDADES) + (indice & 0xffff) * UNIDADE)

    def _grupo(self, grupo):
        return u32(GRUPOS + u32(grupo) * 32)

    def _jogador_tipo_direto(self, deslocamento):
        """Player-record byte +1 read directly (iagVilleReset/iagRessReset)."""
        return self.m.u8(u32(self.m.u32(JOGADORES) + deslocamento + 1))

    # ------------------------------------------------------------ iaRandom 0x489728
    def ia_random(self, limite):
        if s32(limite) <= 0:
            raise DependenciaIA('iaRandom non-positive argument outside IaReset', 0x489728)
        estado = self.m.u32(ESTADO_ALEATORIO)
        try:
            novo, valor = proximo_aleatorio(estado, limite)  # core's positive path
        except ValueError as erro:
            raise DependenciaIA(f'iaRandom state 0x{estado:08x} outside core domain ({erro})', 0x489728) from None
        self.m.u32(ESTADO_ALEATORIO, novo)
        return valor

    # ------------------------------------------------------------ listInit 0x47cfd0
    def list_init(self, cabecalho, base, quantidade, passo, encadear):
        m = self.m
        m.u32(cabecalho + 4, quantidade)
        m.u32(cabecalho + 8, passo)
        m.u32(cabecalho + 0xc, base)
        if encadear:
            ultimo = u32(quantidade - 1)
            m.u32(cabecalho, 0)
            k, registro = 0, base
            while s32(k) < s32(ultimo):
                anterior = registro
                k += 1
                registro = u32(registro + passo)
                m.u32(anterior, k)
            m.u32(registro, 0xffffffff)
        else:
            m.u32(cabecalho, 0xffffffff)
        return cabecalho

    def ia_prob_reset(self):
        self.list_init(0x5148a0, 0x512320, 100, 0x60, 1)
        for contexto in range(0x5148b0, 0x514900, 0x10):
            self.list_init(contexto, 0x512320, 100, 0x60, 0)
        return 0

    # ------------------------------------------------------------ group table
    def ia_group_new(self, jogador, tipo):
        m = self.m
        indice = m.u32(DICA_GRUPO)
        deslocamento, encontrado = u32(indice * 32), 0xffffffff
        while s32(deslocamento) < 0xc80:
            if m.u8(u32(deslocamento + 0x51a9f8)) == 0:
                g = u32(deslocamento + GRUPOS)
                m.u32(g, 0xffffffff)
                m.u32(g + 4, 0xffffffff)
                m.u16(g + 0x12, 0)
                m.u16(g + 0x14, 0x7fff)
                m.u32(g + 8, 0xffffffff)
                m.u32(g + 0xc, 0xffffffff)
                m.u16(g + 0x10, 0xffff)
                m.u8(g + 0x18, 1)
                m.u8(g + 0x19, tipo)
                m.u8(g + 0x1a, 0xff)
                m.u16(g + 0x16, 0xffff)
                m.u32(g + 0x1c, 0)
                m.u8(g + 0x1b, m.u8(u32(tipo * 4 + 0x498ec4)))
                dica = m.u32(DICA_GRUPO)
                m.u32(DICA_GRUPO, dica + 1 if s32(dica) < 0x63 else 0)
                encontrado = indice
                break
            deslocamento, indice = u32(deslocamento + 0x20), u32(indice + 1)
        if encontrado == 0xffffffff:
            return 0xffffffff
        cabeca = u32(tipo * 4 + jogador * 0x60 + POOLS)
        anterior = m.u32(cabeca)
        m.u32(cabeca, encontrado)
        m.u32(self._grupo(encontrado), anterior)
        return encontrado

    def ia_group_delete(self, jogador, grupo):
        m = self.m
        if s32(grupo) < 0 or s32(grupo) >= 100:
            return
        m.u8(self._grupo(grupo) + 0x18, 0)
        if s32(grupo) < s32(m.u32(DICA_GRUPO)):
            m.u32(DICA_GRUPO, grupo)
        tipo = m.u8(self._grupo(grupo) + 0x19)
        cabeca = u32(jogador * 0x60 + tipo * 4 + POOLS)
        atual, anterior = m.u32(cabeca), 0xffffffff
        while atual != 0xffffffff:
            if atual == grupo:
                seguinte = m.u32(self._grupo(grupo))
                m.u32(cabeca if anterior == 0xffffffff else self._grupo(anterior), seguinte)
                return
            anterior, atual = atual, m.u32(self._grupo(atual))

    def unit_add_to_group(self, grupo, unidade):
        m = self.m
        endereco = self._unidade(unidade)
        g = self._grupo(grupo)
        if g == 0:
            return 0x1a1a0010
        m.u16(endereco + 0x108, m.u16(g + 0x10))
        m.u32(endereco + 0x10c, grupo)
        quantidade = m.u16(g + 0x12)
        m.u16(g + 0x10, unidade)
        m.u16(g + 0x12, quantidade + 1)
        return 0

    def unit_remove_from_group(self, grupo, unidade):
        m = self.m
        g = self._grupo(grupo)
        if g == 0:
            return 0x1a1a0010
        alvo, anterior, atual = unidade & 0xffff, 0xffff, m.u16(g + 0x10)
        while atual != 0xffff:
            if atual == alvo:
                seguinte = m.u16(self._unidade(atual) + 0x108)
                if anterior == 0xffff:
                    m.u16(g + 0x10, seguinte)
                else:
                    m.u16(self._unidade(anterior) + 0x108, seguinte)
                m.u16(g + 0x12, m.u16(g + 0x12) - 1)
                return 0
            anterior, atual = atual, m.u16(self._unidade(atual) + 0x108)
        return 0x1a1a0012

    def unit_remove_from_pool(self, jogador, unidade):
        pool = self.m.u32(u32(jogador * 0x60 + POOLS))
        if pool == 0xffffffff:
            return 0x1a1a0010
        return self.unit_remove_from_group(pool, unidade & 0xffff)

    def _procurar_em_grupo(self, grupo, aceita):
        m = self.m
        g = self._grupo(grupo)
        if g == 0:
            return 0xffff
        atual = m.u16(g + 0x10)
        while atual != 0xffff:
            endereco = self._unidade(atual)
            if aceita(m.u8(endereco + 1)):
                return atual
            atual = m.u16(endereco + 0x108)
        return 0xffff

    def unit_find_type_into_pool(self, jogador, tipo):
        pool = self.m.u32(u32(jogador * 0x60 + POOLS))
        if pool == 0xffffffff:
            return 0xffff
        return self._procurar_em_grupo(pool, lambda t: t == u32(tipo))

    def unit_find_type_into_group(self, tipo, grupo):
        return self._procurar_em_grupo(grupo, lambda t: t == u32(tipo))

    def unit_find_suitable_into_pool(self, jogador, tipo_grupo):
        pool = self.m.u32(u32(jogador * 0x60 + POOLS))
        if pool == 0xffffffff:
            return 0xffff
        mascara = 1 << (tipo_grupo & 31)
        return self._procurar_em_grupo(pool, lambda t: self.m.u32(u32(t * 4 + 0x4989f8)) & mascara)

    def unit_get_first_in_group(self, grupo):
        m = self.m
        g = self._grupo(grupo)
        m.u32(0x51b844, g)
        if g == 0:
            return 0xffff
        m.u16(0x51b848, m.u16(g + 0x10))
        return m.u16(0x51b848)

    # ------------------------------------------------------------ modes
    def ville_set_mode(self, jogador, modo):
        m, modo = self.m, _s8(modo)
        base = u32(jogador * 31 * 4)
        m.u32(u32(base + 0x51b8a4), m.u32(u32(modo * 4 + 0x498c10)))
        m.u32(u32(base + 0x51b8b0), modo)

    def ress_set_mode(self, jogador, modo):
        m, modo = self.m, _s8(modo)
        base = u32(jogador * 21 * 8)
        m.u32(u32(base + 0x51ba7c), m.u32(u32(modo * 4 + 0x498c38)))
        for k in range(4):
            m.u32(u32(base + 0x51ba6c + 4 * k), m.u32(u32(modo * 16 + 0x498c60 + 4 * k)))
        m.u32(u32(base + 0x51ba84), m.u32(u32(modo * 4 + 0x498c4c)))

    def war_set_mode(self, jogador, modo):
        m, modo = self.m, _s8(modo)
        base = u32(jogador * 0x1144)
        valor, extra = m.u32(u32(modo * 4 + 0x498cb0)), m.u32(u32(modo * 4 + 0x498cc4))
        m.u32(u32(base + GUERRA), valor)
        m.u32(u32(base + GUERRA + 8), extra)

    # ------------------------------------------------------------ IaReset 0x47f36e
    def ia_reset(self):
        m = self.m
        for jogador in range(4):
            if self._chamar('PlayerGetType', 0x47f576, jogador) & 0xff != 2:
                continue
            ctx = CONTEXTOS + jogador * 16
            if not any(m.u8(ctx + 5 + k) for k in range(4)):
                self._criar_limiares(jogador, ctx)
            self._escolher_ramo(jogador, ctx)
            if self._tem_unidade_viva(jogador):
                m.u8(ctx + 4, 0)
                m.u8(ctx, 0)
                self.ville_set_mode(jogador, 0)
                self.ress_set_mode(jogador, 0)
                self.war_set_mode(jogador, 0)
                m.u8(ctx + 1, 0)
                m.u8(ctx + 2, 1)
                m.u8(ctx + 3, 0)
                m.u8(ctx + 9, 0)
            else:
                m.u8(ctx + 4, 1)
        for rotina in (self.ia_prob_reset, self.iag_unit_reset, self.iag_ville_reset):
            resultado = rotina()
            if resultado:
                return resultado
        self.iaf_ressource_reset()
        for rotina in (self.iag_ress_reset, self.iag_war_reset):
            resultado = rotina()
            if resultado:
                return resultado
        self.init_mission_monstre()
        return 0

    def _criar_limiares(self, jogador, ctx):
        favorito = 0 if jogador == 3 else (1 if jogador == 1 else self.ia_random(4))
        peso = self.ia_random(0x14) + 0x1e
        outros = (100 - peso) // 3
        acumulado = 0
        for ramo in range(3):
            acumulado += peso if ramo == favorito else outros
            self.m.u8(ctx + 5 + ramo, acumulado)
        self.m.u8(ctx + 8, 0x64)

    def _escolher_ramo(self, jogador, ctx):
        m = self.m
        if all(m.u8(ctx + 5 + k) == 0xff for k in range(4)):
            return
        for ramo in range(4):
            minimo = m.u8(0x498464 + ramo)
            if (self._chamar('RechercheGetNiveau', 0x47f43f, jogador, ramo) & 0xffff) >= minimo:
                m.u8(ctx + 5 + ramo, 0xff)
        while True:
            sorteio = self.ia_random(100)
            ramo = 0
            while ramo < 4 and not sorteio < m.s8(ctx + 5 + ramo):
                ramo += 1
            escolhido = ramo
            if m.s8(ctx + 5 + ramo) == -1:
                escolhido = 0xffffffff
                for k in range(4):
                    if escolhido != 0xffffffff:
                        break
                    if m.s8(ctx + 5 + k) != -1:
                        escolhido = k
            if escolhido == 3 and self._chamar('MissionGetNum', 0x47f4b0) & 0xffff < 7:
                continue
            self._chamar('RechercheSetBranche', 0x47f4ca, jogador, escolhido & 0xff)
            return

    def _tem_unidade_viva(self, jogador):
        for unidade in range(800):
            if self._chamar('EnginEstVivant', 0x47f4e7, unidade) & 0xff:
                if self.m.u8(self._unidade(unidade)) == jogador:
                    return True
        return False

    # ------------------------------------------------------------ iagUnitReset 0x48270b
    def iag_unit_reset(self):
        m = self.m
        for deslocamento in range(0x20, 0xc80 + 0x20, 0x20):
            g = 0x51a9c0 + deslocamento
            m.u32(g, 0xffffffff)
            m.u32(g + 4, 0xffffffff)
            m.u16(g + 0x12, 0)
            m.u16(g + 0x14, 0x7fff)
            m.u16(g + 0x16, 0xffff)
            m.u16(g + 0x10, 0xffff)
            m.u8(g + 0x1a, 0xff)
            m.u32(g + 0x1c, 0)
            m.u32(g + 8, 0xffffffff)
            m.u8(g + 0x1b, 0xff)
            m.u32(g + 0xc, 0xffffffff)
            m.u8(g + 0x18, 0)
            m.u8(g + 0x19, 0)
        m.u32(DICA_GRUPO, 0)
        for jogador in range(5):
            if self._chamar('PlayerGetType', 0x4827e0, jogador) & 0xff != 2:
                continue
            pool = POOLS + jogador * 0x60
            for k in range(20):
                m.u32(pool + 4 * k, 0xffffffff)
            m.u32(pool + 0x50, 0xffffffff)
            if jogador == 4:
                continue
            if self.ia_group_new(jogador, 0) == 0xffffffff:
                continue
            for unidade in range(800):
                if not self._chamar('EnginEstVivant', 0x48283f, unidade) & 0xff:
                    continue
                endereco = self._unidade(unidade)
                if m.u8(endereco) != jogador:
                    continue
                grupo = m.u32(pool)
                g = self._grupo(grupo)
                if g == 0:
                    continue
                m.u16(endereco + 0x108, m.u16(g + 0x10))
                m.u32(endereco + 0x10c, grupo)
                quantidade = m.u16(g + 0x12)
                m.u16(g + 0x10, unidade)
                m.u16(g + 0x12, quantidade + 1)
        return 0

    # ------------------------------------------------------------ iagVilleReset 0x484310
    def iag_ville_reset(self):
        m = self.m
        for jogador in range(4):
            if self._jogador_tipo_direto(jogador * 0x14) != 2:
                continue
            cidade = CIDADES + jogador * 0x7c
            for k in range(22):
                m.u16(cidade + 2 * k, 0)
                m.u16(cidade + 0x2c + 2 * k, 0)
            m.u32(cidade + 0x6c, 0)
            for estrutura in range(1000):
                if not self._chamar('BatimentExiste', 0x484348, estrutura) & 0xff:
                    continue
                if self._chamar('BatimentGetPlayer', 0x484353, estrutura) & 0xff != jogador:
                    continue
                tipo = self._chamar('BatimentGetType', 0x484363, estrutura) & 0xff
                m.u16(u32(cidade + tipo * 2), m.u16(u32(cidade + tipo * 2)) + 1)
                m.u32(cidade + 0x6c, m.u32(cidade + 0x6c) + 1)
                if self._chamar('BatimentGetType', 0x48437a, estrutura) & 0xff == 3:
                    self.iag_ress_add_to_cave_list(jogador, estrutura)
            self._separar_colonos(jogador, cidade)
        return 0

    def _separar_colonos(self, jogador, cidade):
        m = self.m
        grupo = self.ia_group_new(jogador, 0xa)
        m.u32(cidade + 0x60, grupo)
        if grupo != 0xffffffff:
            grupo = self.ia_group_new(jogador, 0xb)
            m.u32(cidade + 0x5c, grupo)
            if grupo != 0xffffffff:
                while True:
                    unidade = self.unit_find_type_into_pool(jogador, 9)
                    if unidade == 0xffff:
                        break
                    self.unit_remove_from_pool(jogador, unidade)
                    if self._chamar('EnginGetEtat', 0x4843ea, unidade) & 0xff == 0xe:
                        self.unit_add_to_group(m.u32(cidade + 0x60), unidade)
                    elif self._chamar('EnginGetEtat', 0x484407, unidade) & 0xff == 7:
                        self.unit_add_to_group(m.u32(cidade + 0x5c), unidade)
        m.u32(cidade + 0x68, 0xffffffff)

    def iag_ress_add_to_cave_list(self, jogador, estrutura):
        base = u32(jogador * 0xa8 + RECURSOS)
        for k in range(8):
            if self.m.u16(u32(base + 2 * k + 0x8c)) == 0xffff:
                self.m.u16(u32(base + 2 * k + 0x8c), estrutura)
                return

    # ------------------------------------------------------------ iafRessourceReset 0x48134c
    def iaf_ressource_reset(self):
        for k in range(1, 0x15):  # inc before the store, jb after it: 0x51a9cc..0x51a9df
            self.m.u8(0x51a9cb + k, 0)

    # ------------------------------------------------------------ iagRessReset 0x485002
    def iag_ress_reset(self):
        m = self.m
        for jogador in range(4):
            if self._jogador_tipo_direto(jogador * 0x14) != 2:
                continue
            r = RECURSOS + jogador * 0xa8
            saidas = self._chamar('GetRessource', 0x4850b3, jogador)
            m.u32(r, saidas[0])
            m.u32(r + 4, saidas[1])
            m.u32(r + 8, saidas[2])
            for k in range(4):
                m.u32(r + 0x10 + 4 * k, m.u32(r + 4 * k))
            m.u32(r + 0x20, 0)
            m.u32(r + 0x24, 0)
            m.u32(r + 0x28, 0)
            m.u32(r + 0x44, 0xffffffff)
            for k in range(5):
                m.u32(r + 0x58 + 8 * k, 0xffffffff)
                m.u32(r + 0x54 + 8 * k, 0xffffffff)
            m.u32(r + 0x84, 0)
            m.u32(r + 0x88, 0)
            m.u32(r + 0x80, 0xffffffff)
            m.u32(r + 0x7c, 0xffffffff)
            for k in range(8):
                m.u16(r + 0x8c + 2 * k, 0xffff)
            if self.ia_group_new(jogador, 7) == 0xffffffff:
                return 0x1a1a000f
            if self.ia_group_new(jogador, 3) == 0xffffffff:
                return 0x1a1a000f
            m.u8(r + 0x9d, 0)
            m.u8(r + 0x9c, 0)
        return 0

    # ------------------------------------------------------------ iagWarReset 0x4864c1
    def iag_war_reset(self):
        m = self.m
        for jogador in range(4):
            if self._chamar('PlayerGetType', 0x4864fe, jogador) & 0xff != 2:
                continue
            w = GUERRA + jogador * 0x1144
            m.u32(w + 0xc, 0xff)
            m.u32(w + 0x14, 0xff)
            m.u32(w + 0x10, 0xff)
            grupo = self.ia_group_new(jogador, 9)
            m.u32(w + 4, grupo)
            if grupo != 0:
                forca = 0
                while True:
                    unidade = self.unit_find_suitable_into_pool(jogador, 9)
                    if unidade == 0xffff:
                        break
                    # imul: low 32 bits of NbBatBuiltTotal(p) x war-mode factor (W+8), compared signed
                    limite = s32(m.u32(u32(jogador * 0x7c + 0x51b8b8)) * m.u32(w + 8))
                    if s32(forca) >= limite:
                        break
                    self.unit_remove_from_pool(jogador, unidade)
                    self.unit_add_to_group(m.u32(w + 4), unidade)
                    tipo = m.u8(self._unidade(unidade) + 1)
                    forca = u32(forca + m.u32(u32(tipo * 4 + 0x498cf4)))
            for k in range(16):
                e = w + 0x28 + k * 0x110
                m.u32(e, 0xffffffff)
                m.u32(e + 4, 0xffffffff)
                m.u32(e + 8, 0xffffffff)
                m.u16(e + 0xc, 0)
                m.u16(e + 0xe, 0)
        for k in range(16):
            e = 0x52020c + 0x28 + k * 0x110
            m.u32(e, 0xffffffff)
            m.u32(e + 4, 0xffffffff)
            m.u16(e + 0xc, 0)
            m.u16(e + 0xe, 0)
        return 0

    # ------------------------------------------------------------ InitMissionMonstre 0x47af90
    def init_mission_monstre(self):
        m = self.m
        m.u8(0x50a9cc, 0)
        m.u32(0x50ae80, 0)
        m.u8(0x50b134, 0)
        m.u32(0x50b178, 0)
        reserva = self.ia_group_new(4, 0x10)
        if reserva == 0xffffffff:
            return
        for unidade in range(800):
            if not self._chamar('EnginEstVivant', 0x47aff1, unidade) & 0xff:
                continue
            tipo = self._chamar('EnginGetType', 0x47affc, unidade) & 0xff
            if not self._chamar('TypeEnginEstMonstre', 0x47b006, tipo) & 0xff:
                continue
            self.unit_add_to_group(reserva, unidade)
            self._chamar('EnginSetPlayer', 0x47b01f, unidade, 4)
            m.u32(0x50b178, m.u32(0x50b178) + 1)
        if self._chamar('MissionGetNum', 0x47b02c) & 0xffff == 0x17:
            self._registrar_grupo(reserva)
            return
        quantidades, grupos = [], []
        for grupo in range(16):
            quantidade = m.u8(0x50b124 + grupo)
            if quantidade:
                grupos.append(grupo)
                quantidades.append(quantidade)
        n = len(grupos)
        for i in range(n - 1):
            for j in range(i + 1, n):
                if quantidades[j] > quantidades[i]:
                    quantidades[i], quantidades[j] = quantidades[j], quantidades[i]
                    grupos[i], grupos[j] = grupos[j], grupos[i]
        for i in range(n):
            if s32(m.u32(0x50b178)) >= 0x32 or m.u8(0x50b134) >= 0x10:
                break
            continuar = True
            while continuar and s32(m.u32(0x50b178)) < 0x32 and m.u8(0x50b134) < 0x10:
                grupo = self.ia_group_new(4, 0x10)
                if grupo == 0xffffffff:
                    break
                for tipo in range(0x1a):
                    if s32(m.u32(0x50b178)) >= 0x32:
                        break
                    necessarios = m.u8(0x50af84 + grupos[i] * 0x1a + tipo)
                    movidos = 0
                    while movidos < necessarios:
                        unidade = self.unit_find_type_into_group(tipo, reserva)
                        if unidade == 0xffff:
                            continuar = False
                            break
                        self.unit_remove_from_group(reserva, unidade)
                        movidos += 1
                        self.unit_add_to_group(grupo, unidade)
                if self.unit_get_first_in_group(grupo) == 0xffff:
                    self.ia_group_delete(4, grupo)
                    if continuar:
                        raise NaoTerminaNoOriginal(0x47b1f4, 'Empty monster group with the creation flag still '
                                                             'set: the original recreates and deletes it forever')
                    continue
                if m.u8(0x50b134) >= 0x10:
                    break
                self._registrar_grupo(grupo)
        if self.unit_get_first_in_group(reserva) == 0xffff:
            self.ia_group_delete(4, reserva)
        elif m.u8(0x50b134) < 0x10:
            self._registrar_grupo(reserva)
        m.u32(0x50b180, 0xffff)
        m.u32(0x50b17c, 3)

    def _registrar_grupo(self, grupo):
        indice = self.m.u8(0x50b134)
        self.m.u32(0x50b138 + indice * 4, grupo)
        self.m.u8(0x50b134, indice + 1)

    # ------------------------------------------------------------ IaAlloc 0x47fb15
    def ia_alloc(self):
        m = self.m
        relogio = self._chamar('timeGetTime', 0x489789)
        m.u32(ESTADO_ALEATORIO, u32(relogio) % 0x7fffffff)  # iaRandom(0) seeding path
        self._chamar('debugSymLoad', 0x47fb21, 0x494f84)
        resultado = self._chamar('iaProbLoadBinaryRules', 0x47d1af, 0x494f28, 1)
        if resultado:
            return u32(resultado)
        for endereco, valor in INICIO_RECURSOS:
            m.u32(endereco, valor)
        if not 2 <= s32(m.u32(0x51bcf0)) <= 5:
            m.u32(0x51bcf0, 5)
        for endereco, valor in INICIO_RECURSOS_FIM:
            m.u32(endereco, valor)
        for endereco, valor in INICIO_CIDADES:
            m.u32(endereco, valor)
        for endereco, valor in INICIO_GUERRA:
            m.u32(endereco, valor)
        for k in range(26):  # iaConfigGetValue returns the current value as default: re-stored as is
            m.u32(0x498cf4 + 4 * k, m.u32(0x498cf4 + 4 * k))
        for endereco, valor in INICIO_GUERRA_FIM:
            m.u32(endereco, valor)
        return u32(self._chamar('debugSymUnload', 0x47fb67))


# iaConfigGetValue 0x47fc54 returns its EBX default; each initializer is therefore an
# ordered list of constant u32 stores (original store order, values read from the bytes).
INICIO_RECURSOS = ((0x498c38, 0x64), (0x498c3c, 0x320), (0x498c40, 0x64), (0x498c44, 0x3e8), (0x498c4c, 0x14),
                   (0x498c50, 5), (0x498c54, 1), (0x498c58, 1), (0x498c60, 0), (0x498c70, 0x1e),
                   (0x498c80, 0x1e), (0x498c90, 0x14), (0x51bcdc, 0x64), (0x51bce0, 0x64), (0x51bce4, 0x64),
                   (0x51bce8, 5), (0x51bcec, 0x50), (0x51bcf0, 5))
INICIO_RECURSOS_FIM = ((0x51bcf4, 3), (0x51bcf8, 2))
INICIO_CIDADES = ((0x498c10, 0x7d0), (0x498c14, 0x9c4), (0x498c18, 0x3e8), (0x498c1c, 0x3e8))
INICIO_GUERRA = ((0x498cb0, 0x2904), (0x498cb4, 0xdac), (0x498cb8, 0x5dc), (0x498cbc, 0x3e8), (0x498cc4, 5),
                 (0x498cc8, 3), (0x498ccc, 0xf), (0x498cd0, 0xa))
INICIO_GUERRA_FIM = ((0x521350, 0xa), (0x521354, 0xa), (0x521358, 0x28), (0x52135c, 0xa), (0x521360, 0xa),
                     (0x521364, 0x1770))


def reiniciar_ia(memoria, mundo):
    """IaReset 0x47f36e. Returns the original EAX (0, or the first nonzero tail result).

    ``memoria``: ``MemoriaDeclarada`` whose regions include ``REGIOES_REINICIO`` plus the unit
    pool (800×276 at [0x4e19a0]) and the player table (4×20 at [0x5080a8]).
    ``mundo``: provider of the world queries listed in the module docstring.
    """
    return _Rotinas(memoria, mundo).ia_reset()


def iniciar_ia_programa(memoria, ligacoes):
    """IaAlloc 0x47fb15 (program start). ``ligacoes`` supplies the declared bindings."""
    return _Rotinas(memoria, ligacoes).ia_alloc()


def resetar_ataques_ia(memoria):
    """IAResetAttaque 0x47c162: no caller or pointer exists in the intact image."""
    m = memoria
    m.u32(0x50d99c, 0)
    for indice in range(100):
        r = 0x50d5b4 + indice * 10
        m.u8(r, 0xc8)
        m.u8(r + 4, 0xff)
        m.u8(r + 5, 0xff)
        m.u8(r + 1, 0xff)
        m.u16(r + 2, 0xffff)
        m.u16(r + 6, 0xffff)
        m.u8(r + 8, 0)
