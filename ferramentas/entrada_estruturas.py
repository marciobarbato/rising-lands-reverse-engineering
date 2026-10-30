"""Structure entry, lodging and Bag routines over live original memory (M3/M4 groundwork).

Translated from the intact bytes (``evidencias/entrada-estruturas/*.asm``) after the native capture
``evidencias/entrada-estruturas/captura-entrada-estruturas-exibicao.json.xz`` was committed (``ebea7e6``).
Routines (the callers Economy's work cycle and lodging credit name, then their helpers):
- Bags: BagContient 0x4471b8 (every tag), BagContientTroupe 0x44724a, BagRetire 0x4472ea, BagPrend 0x447483,
  EnginGetBag 0x4474a6, BagAccepte 0x4470d2, BagGetNbContenu 0x447107, BagGetCode 0x4472d3, BagGetType 0x4472de;
- PlaceLibre 0x41f552, BatimentAdjacent 0x42381f, GetCaseCentrale 0x423b27, BatimentGetCaseEntrer 0x41d057,
  BatimentGetType/GetPlayer/GetModeEtat/EnDestruction, EnginGetVie/GetVieMax, EnginEstBlesse,
  EnginBombeEstMax, TypeEnginEstTroupe/APied/Engin, EnginResetType 0x4571d4;
- RetireEngin 0x457058, AnimWorkEngin 0x447f58;
- SetEnginRentreBatiment 0x445b10, SetEnginSelectRentreBatiment 0x473f4b, EnginSelectPeutEntrer 0x472b6c
  (modes 1 and 3; other modes return 0);
- CalculEntreBatiment 0x449716 for unit types 0..10 and 25 (the colonist, worker and soldier branch) and unit
  state 13's body 0x4558e4 inside EnginNextEtape (``estado_entrada``), up to its continuation 0x454ccd.

Every routine takes EAX..EBP at its entry and returns EAX..EBP as the original leaves them, callee-saved
registers included; arithmetic flags are not modeled. ``memoria``: ``u8/u16/u32(addr, value=None)`` plus
``vista(addr, n)`` (``memoria_quadro_core.MemoriaQuadro``) for the routines that use M2.3's live world.

Core routines reused (single implementations): ``selecao_ordens`` (DeselectionEngin, SetDeplaceEngin, EnginAsk,
EnginGetVolume, BatimentGetVolume), ``construcao_core`` (DeplaceEngin, BatimentCollision),
``chamadas_quadro_core`` (BatimentGetCase, SetEnginCollision, TerrainEstDecouvert, EnginGetType/Player,
EnginEstMiroir) and M2.3's live world for the physical effects that have no flat translation:
ResetEnginCollision (``ocupar``), SetMiniMap mode 5 (``minimapa``), EteintTerrain (``apagar_area``),
DecouvreTerrain (``descobrir_area``), IllumineTerrain (``iluminar_area``), BatimentModifyMap
(``modificar_minimapa_estrutura``) and EnginPeutPasser (``consultar_passagem``).

Uncertain register bits. Those world effects do not reconstruct the registers their loops leave. Where a result
depends on them it carries ``_incertos = {register: mask}`` (masked bits 0), never a guess: DecouvreTerrain's
and IllumineTerrain's EBX high word (stack residue), BatimentModifyMap/
EnginPeutPasser's clobbered registers, and DeplaceEngin's (``construcao_core``) deep-callee EAX. Every other
bit is exact.

Named dependencies (never defaulted; ``externo(nome, chamada, registradores) -> registradores``; a path that
reaches one without it raises ``DependenciaRamoCore`` at the original call, after the stores before it):
- Economy: BatimentLogeEngin 0x41f76e (CalculEntreBatiment 0x449976: AX structure, DX unit); BonusGetValEngin
  through ``bonus(jogador, tipo, seletor)`` for DeplaceEngin's CalculFatigue;
- ai-runtime: iagUnitSendMessage 0x4829c8 (AX unit, DL message, EBX argument) at 0x449bb8 (0x47), 0x4499ee and
  0x449af8; diplomacy: PlayerInitPropositionAlliance 0x46dadb at 0x449ad7 (a type-10 unit at a foreign
  sanctuary);
- Audio: PlaySnd_PostSound through ``som`` (EnginAsk's voice in SetEnginSelectRentreBatiment).
Outside the translated domain (``ForaDoDominioEntrada`` before any store of that branch): CalculEntreBatiment
for unit types 11..24 (vehicles 0x44a12f, type 16 0x449c56), state 13's vehicle entry (+0xb8 set, 0x4559c6),
BatimentRetireColon 0x41dde0 (captured, not translated: BatimentEnleveUnColon/SetSortEngin chain).
"""
from chamadas_quadro_core import (DependenciaRamoCore, caso_estrutura, colisao_estrutura, definir_colisao_unidade,
                                  dono_da_unidade, terreno_esta_descoberto, tipo_da_unidade, unidade_espelho)

M32 = 0xffffffff
REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
PONTEIRO_UNIDADES, PASSO = 0x4e19a0, 276
ESTRUTURAS = 0x49a0c8
TIPOS_ESTRUTURA = 0x495d8c              # stride 52: u16 width, u16 height; +0x12 Bag capacity byte
VIDA_MAXIMA = 0x4965b6                  # u16 per unit type, stride 50
SELECOES = 0x508728                     # u16 count + u16 units, stride 0x200 per player
JOGADOR_LOCAL = 0x508041
CONTADOR = 0x508f7c
LIMITE_CASERNA, LIMITE_HOSPITAL = 0x495be9, 0x495be8   # PlaceLibre's type-8 and type-0x13 bytes
BUSCA_UNIDADE, BUSCA_OCUPADA, BUSCA_SUCESSO, BUSCA_ROTA = 0x496304, 0x4e0f36, 0x4e0f37, 0x4e0f3c
CORPO_13, CONTINUACAO_13 = 0x4558e4, 0x454ccd
ROTINAS = {
    'BagContient': 0x4471b8, 'BagContientTroupe': 0x44724a, 'BagRetire': 0x4472ea, 'BagPrend': 0x447483,
    'EnginGetBag': 0x4474a6, 'BagAccepte': 0x4470d2, 'BagGetNbContenu': 0x447107, 'BagGetCode': 0x4472d3,
    'BagGetType': 0x4472de, 'PlaceLibre': 0x41f552, 'BatimentAdjacent': 0x42381f, 'GetCaseCentrale': 0x423b27,
    'BatimentGetCaseEntrer': 0x41d057, 'BatimentGetCase': 0x41aee2, 'BatimentGetType': 0x41a4f4,
    'BatimentGetPlayer': 0x41a08c, 'BatimentGetModeEtat': 0x41a6ec, 'BatimentEnDestruction': 0x41a70b,
    'BatimentGetVolume': 0x41a0ab, 'EnginGetVolume': 0x440c5d, 'EnginGetType': 0x442025,
    'EnginGetPlayer': 0x442045, 'TerrainEstDecouvert': 0x4766f0, 'RetireEngin': 0x457058,
    'AnimWorkEngin': 0x447f58, 'EnginResetType': 0x4571d4, 'SetEnginCollision': 0x442cb4,
    'SetDeplaceEngin': 0x4457d3, 'DeplaceEngin': 0x44930c, 'EnginPeutPasser': 0x442668,
    'DecouvreTerrain': 0x476851, 'IllumineTerrain': 0x476cb3, 'BatimentModifyMap': 0x419e97,
    'SetEnginRentreBatiment': 0x445b10, 'SetEnginSelectRentreBatiment': 0x473f4b,
    'EnginSelectPeutEntrer': 0x472b6c, 'CalculEntreBatiment': 0x449716, 'EnginNextEtape:state13': CORPO_13,
    'BatimentRetireColon': 0x41dde0,
}
RAIO_APAGAR = (20, 8, 10, 8, 5, 8, 8, 8, 8, None, 7, 7, None, 8, 8, 8, 8, 4, 8, 4, 8, 4)   # table 0x41dd88
NAO_TROPAS = frozenset((3, 11, 12, 13, 14, 15, 16, 17, 25))      # BagContientTroupe / TypeEnginEstTroupe
NAO_A_PE = frozenset((3, 11, 12, 13, 14, 15, 16, 17))            # TypeEnginEstAPied 0x4423b0


class ForaDoDominioEntrada(NotImplementedError):
    """A branch outside the translated domain; nothing was written by it."""
    def __init__(self, rotina, endereco, motivo):
        self.rotina, self.endereco = rotina, endereco
        super().__init__(f'{rotina}: {motivo} (0x{endereco:x}); no store was made by this branch')


def _b(v, b):
    """Replace the low byte."""
    return (v & 0xffffff00) | (b & 0xff)


def _w(v, w):
    """Replace the low word."""
    return (v & 0xffff0000) | (w & 0xffff)


def _h(v, b):
    """Replace bits 8..15 (AH/BH/CH/DH)."""
    return (v & 0xffff00ff) | ((b & 0xff) << 8)


def _s16(v):
    v &= 0xffff
    return v - 0x10000 if v & 0x8000 else v


def _s32(v):
    v &= M32
    return v - (1 << 32) if v & 0x80000000 else v


class _MundoEstruturasCopiadas:
    """The live world with a bytes snapshot of the structure pool, for the committed structure-geometry functions
    that require ``bytes``/``bytearray`` and only read it (BatimentModifyMap, CalculPosition)."""

    def __init__(self, mundo):
        self._mundo = mundo
        self.estruturas = bytes(mundo.estruturas)

    def __getattr__(self, nome):
        return getattr(self._mundo, nome)


class EntradaEstruturas:
    """The routines over one live memory. Providers: ``externo`` (named dependencies, see the module docstring),
    ``som`` (Audio's PlaySnd_PostSound, as in ``selecao_ordens``) and ``bonus`` (Economy's BonusGetValEngin
    value, as in ``construcao_core``)."""

    def __init__(self, memoria, *, externo=None, som=None, bonus=None):
        self.m = memoria
        self.externo, self.som, self.bonus = externo, som, bonus
        self._selecao = self._construcao = None

    # ------------------------------------------------------------ composition
    def selecao(self):
        if self._selecao is None:
            from selecao_ordens import SelecaoOrdens
            self._selecao = SelecaoOrdens(self.m, som=self.som)
        return self._selecao

    def construcao(self):
        if self._construcao is None:
            from construcao_core import ConstrucaoCore
            self._construcao = ConstrucaoCore(self.m, bonus=self.bonus)
        return self._construcao

    def mundo(self):
        return self.construcao().mundo()

    def _ext(self, nome, chamada, r, **regs):
        """Named dependency ``nome`` called at ``chamada`` with the caller's registers ``r`` updated by ``regs``;
        returns the callee's exit registers."""
        if self.externo is None:
            raise DependenciaRamoCore(nome, chamada, 'provider required')
        entrada = dict(r, **{k: v & M32 for k, v in regs.items()})
        saida = self.externo(nome, chamada, {k: entrada[k] for k in REG7})
        return {k: saida[k] & M32 if k in saida else entrada[k] for k in REG7}

    # ------------------------------------------------------------ memory helpers
    def _pool(self):
        return self.m.u32(PONTEIRO_UNIDADES)

    def _rec(self, u):
        return (self._pool() + (u & 0xffff) * PASSO) & M32

    @staticmethod
    def _est(s):
        return (ESTRUTURAS + (s & 0xffff) * PASSO) & M32

    def _tamanho(self, tipo):
        return self.m.u16(TIPOS_ESTRUTURA + 52 * tipo), self.m.u16(TIPOS_ESTRUTURA + 52 * tipo + 2)

    def _liberar_busca(self, u):
        """The inlined search-context release when unit ``u`` owns it (0x496304). True when released."""
        if (u & 0xffff) == self.m.u16(BUSCA_UNIDADE):
            self.m.u8(BUSCA_OCUPADA, 0)
            self.m.u8(BUSCA_SUCESSO, 0)
            self.m.u32(BUSCA_ROTA, 0)
            self.m.u16(BUSCA_UNIDADE, 0xffff)
            return True
        return False

    def _vivo(self, u):
        """EnginEstVivant's test inlined (state not 0/4)."""
        return self.m.u8(self._rec(u) + 2) not in (0, 4)

    # ------------------------------------------------------------ entry point
    def chamar(self, nome, regs, pilha=()):
        """Run routine ``nome`` with entry registers ``regs`` (EAX..EBP; missing keys are an error)."""
        r = {k: regs[k] & M32 for k in REG7}
        metodo = {
            'BagContient': self.bag_contient, 'BagContientTroupe': self.bag_contient_troupe,
            'BagRetire': self.bag_retire, 'BagPrend': self.bag_prend, 'EnginGetBag': self.engin_get_bag,
            'BagAccepte': self.bag_accepte, 'BagGetNbContenu': self.bag_get_nb_contenu,
            'BagGetCode': self.bag_get_code, 'BagGetType': self.bag_get_type, 'PlaceLibre': self.place_libre,
            'BatimentAdjacent': self.batiment_adjacent, 'GetCaseCentrale': self.get_case_centrale,
            'BatimentGetCaseEntrer': self.batiment_get_case_entrer, 'BatimentGetCase': self.batiment_get_case,
            'BatimentGetType': self.batiment_get_type, 'BatimentGetPlayer': self.batiment_get_player,
            'BatimentGetModeEtat': self.batiment_get_mode_etat,
            'BatimentEnDestruction': self.batiment_en_destruction, 'BatimentGetVolume': self.batiment_get_volume,
            'EnginGetVolume': self.engin_get_volume, 'EnginGetType': self.engin_get_type,
            'EnginGetPlayer': self.engin_get_player, 'TerrainEstDecouvert': self.terrain_est_decouvert,
            'RetireEngin': self.retire_engin, 'AnimWorkEngin': self.anim_work_engin,
            'EnginResetType': self.engin_reset_type, 'SetEnginCollision': self.set_engin_collision,
            'SetDeplaceEngin': self.set_deplace_engin, 'DeplaceEngin': self.deplace_engin,
            'EnginPeutPasser': self.engin_peut_passer, 'DecouvreTerrain': self.decouvre_terrain,
            'IllumineTerrain': self.illumine_terrain, 'BatimentModifyMap': self.batiment_modify_map,
            'SetEnginRentreBatiment': self.set_engin_rentre_batiment,
            'SetEnginSelectRentreBatiment': self.set_engin_select_rentre_batiment,
            'EnginSelectPeutEntrer': self.engin_select_peut_entrer,
            'CalculEntreBatiment': self.calcul_entre_batiment, 'EnginNextEtape:state13': self.estado_entrada,
            'BatimentRetireColon': self.batiment_retire_colon,
        }.get(nome)
        if metodo is None:
            raise KeyError(f'{nome} is not a translated structure-entry routine')
        return metodo(r)

    # ------------------------------------------------------------ Bags
    def bag_get_nb_contenu(self, r):
        """BagGetNbContenu 0x447107: AX = count (u16 +0). Only AX changes."""
        return dict(r, EAX=_w(r['EAX'], self.m.u16(r['EAX'])))

    def bag_get_code(self, r):
        """BagGetCode 0x4472d3: EDX &= 0xffff; AL = tag byte +0x42 + DX."""
        edx = r['EDX'] & 0xffff
        return dict(r, EDX=edx, EAX=_b(r['EAX'], self.m.u8((r['EAX'] + edx + 0x42) & M32)))

    def bag_get_type(self, r):
        """BagGetType 0x4472de: EDX &= 0xffff; AX = value word +6 + 2*DX."""
        edx = r['EDX'] & 0xffff
        return dict(r, EDX=edx, EAX=_w(r['EAX'], self.m.u16((r['EAX'] + 2 * edx + 6) & M32)))

    def bag_accepte(self, r):
        """BagAccepte 0x4470d2: EAX Bag, DL tag, BX amount (tags 1..4 count 1). AL = +0x66 + amount <= capacity
        (signed); EAX = capacity with AL replaced, EDX = the sum; EBX preserved."""
        bag = r['EAX']
        dl = r['EDX'] & 0xff
        ebx = 1 if 1 <= dl <= 4 else r['EBX']
        edx = (self.m.u16((bag + 0x66) & M32) + (ebx & 0xffff)) & M32
        eax = self.m.u16((bag + 2) & M32)
        return dict(r, EDX=edx, EAX=_b(eax, int(_s32(edx) <= _s32(eax))))

    def bag_contient(self, r):
        """BagContient 0x4471b8: EAX Bag, DL tag, BX target, over the capacity +2 slots. Tag 1: count of units
        whose type is BX; tag 2: count of values BX; tags 3/6/7: EAX = 1 at the first value BX; tags 4/5 and
        tags 0/8+: count 0. EAX = EBX = the count, EDX = the slot index reached; ECX/ESI/EDI/EBP preserved."""
        m, bag = self.m, r['EAX']
        tag, alvo = r['EDX'] & 0xff, r['EBX'] & 0xffff
        ebx = edx = 0
        while (edx & 0xffff) < m.u16((bag + 2) & M32):
            i = edx & 0xffff
            if m.u8((bag + i + 0x42) & M32) == tag:
                caso = (tag - 1) & 0xff
                valor = m.u16((bag + 2 * i + 6) & M32) if caso in (0, 1, 2, 5, 6) else None
                if caso == 0:
                    if m.u8((self._pool() + valor * PASSO + 1) & M32) == alvo:
                        ebx = (ebx + 1) & M32
                elif caso == 1:
                    if valor == alvo:
                        ebx = (ebx + 1) & M32
                elif caso in (2, 5, 6):
                    if valor == alvo:
                        return dict(r, EAX=1, EBX=ebx, EDX=edx)
            edx = (edx + 1) & M32
        return dict(r, EAX=ebx, EBX=ebx, EDX=edx)

    def bag_contient_troupe(self, r):
        """BagContientTroupe 0x44724a: EAX Bag. AL = 1 at the first tag-1 slot (over the capacity) holding a troop
        type (not 3, 11..17, 25). Only EAX changes: AX = 0x101 and the upper word of unit * 276 on a troop;
        otherwise the last slot's tag or type with AL = 0 (the Bag address when no slot)."""
        m, bag = self.m, r['EAX']
        eax = bag
        i = 0
        while i < m.u16((bag + 2) & M32):
            eax = m.u8((bag + i + 0x42) & M32)
            if eax == 1:
                u = m.u16((bag + 2 * i + 6) & M32)
                eax = (u * PASSO) & M32
                tipo = m.u8((self._pool() + eax + 1) & M32)
                if tipo not in NAO_TROPAS:
                    return dict(r, EAX=(eax & 0xffff0000) | 0x101)
                eax = (eax & 0xffff0000) | tipo
            i += 1
        return dict(r, EAX=eax & 0xffffff00)

    def bag_retire(self, r):
        """BagRetire 0x4472ea: EAX Bag, DL tag, BX type (tag 1, the unit's type) or value (other tags). The first
        matching slot (over the count +0) is removed by shifting the tail; +0x66 decreases. EAX = the removed
        value (0xffff when none; bits 16+ are the volume word's borrow on tag 1), EBX/EDX as the loops leave
        them; ECX/ESI/EDI/EBP preserved."""
        m, bag = self.m, r['EAX']
        tag, valor_alvo = r['EDX'] & 0xff, r['EBX'] & 0xffff
        esi, ecx, edi = 0xffff, (r['ECX'] & 0xffff0000) | (r['ECX'] & 0xff00), r['EDI']
        achado = None
        ebx, edx = 0, r['EDX']
        while True:
            if (ebx & 0xffff) >= m.u16(bag):
                break
            edx = esi & 0xffff
            if edx != 0xffff:
                break
            edx = ebx & 0xffff
            ch = m.u8((bag + edx + 0x42) & M32)
            ecx = _h(ecx, ch)
            if ch == tag:
                edx = (2 * edx + bag) & M32
                if ch == 1:
                    u = m.u16((edx + 6) & M32)
                    tipo = m.u8((self._pool() + u * PASSO + 1) & M32)
                    if tipo == valor_alvo:
                        esi = (_w(esi, m.u16((bag + 0x66) & M32)) - 1) & M32
                        ecx = _b(ecx, 1)
                        m.u16((bag + 0x66) & M32, esi)
                        achado = ebx
                        esi = _w(esi, m.u16((edx + 6) & M32))
                    edi = 0
                else:
                    edi = _w(edi, m.u16((edx + 6) & M32))
                    if (edi & 0xffff) == valor_alvo:
                        ecx = (_w(ecx, m.u16((bag + 0x66) & M32)) - 1) & M32
                        achado = ebx
                        m.u16((bag + 0x66) & M32, ecx)
                        ecx = _b(ecx, 1)
                        esi = _w(esi, m.u16((edx + 6) & M32))
            ebx = (ebx + 1) & M32
        if achado is not None:
            j = achado & 0xffff
            while True:
                n = m.u16(bag)
                edx = (bag + j) & M32
                ebx = (2 * j + bag) & M32
                if _s32(j) >= _s32(n - 1):
                    break
                m.u8((edx + 0x42) & M32, m.u8((edx + 0x43) & M32))
                m.u16((ebx + 6) & M32, m.u16((ebx + 8) & M32))
                j += 1
            m.u8((edx + 0x42) & M32, 0)
            m.u16((ebx + 6) & M32, 0)
            m.u16(bag, (m.u16(bag) - 1) & 0xffff)
        return dict(r, EAX=esi, EBX=ebx, EDX=edx)

    def bag_prend(self, r):
        """BagPrend 0x447483: EAX Bag, DL tag, BX value. +0x66 += 1, then tag and value at the count, count += 1
        (no capacity test). EDX = the count before, EBX = the count before (zero-extended)."""
        m, bag = self.m, r['EAX']
        m.u16((bag + 0x66) & M32, (m.u16((bag + 0x66) & M32) + 1) & 0xffff)
        n = m.u16(bag)
        m.u8((bag + n + 0x42) & M32, r['EDX'] & 0xff)
        m.u16((bag + 2 * n + 6) & M32, r['EBX'] & 0xffff)
        m.u16(bag, (n + 1) & 0xffff)
        return dict(r, EBX=n, EDX=n)

    def engin_get_bag(self, r):
        """EnginGetBag 0x4474a6: EAX = the unit record + 0xa (the Bag). Only EAX changes."""
        return dict(r, EAX=(self._rec(r['EAX']) + 0xa) & M32)

    # ------------------------------------------------------------ structure and unit getters
    def batiment_get_type(self, r):
        """BatimentGetType 0x41a4f4: AL = type +8 over the record address. Only EAX changes."""
        e = self._est(r['EAX'])
        return dict(r, EAX=_b(e, self.m.u8(e + 8)))

    def batiment_get_player(self, r):
        """BatimentGetPlayer 0x41a08c: AL = owner +4 over the record address. Only EAX changes."""
        e = self._est(r['EAX'])
        return dict(r, EAX=_b(e, self.m.u8(e + 4)))

    def batiment_get_mode_etat(self, r):
        """BatimentGetModeEtat 0x41a6ec: AL = state +5 over the record address. Only EAX changes."""
        e = self._est(r['EAX'])
        return dict(r, EAX=_b(e, self.m.u8(e + 5)))

    def batiment_en_destruction(self, r):
        """BatimentEnDestruction 0x41a70b: EAX = (+5 == 3). Only EAX changes."""
        return dict(r, EAX=int(self.m.u8(self._est(r['EAX']) + 5) == 3))

    def batiment_get_case(self, r):
        """BatimentGetCase 0x41aee2 (``chamadas_quadro_core.caso_estrutura``). Only EAX changes."""
        return dict(r, EAX=caso_estrutura(self.m, r['EAX'])['EAX'])

    def batiment_get_volume(self, r):
        """BatimentGetVolume 0x41a0ab (``selecao_ordens``). Only EAX changes."""
        return dict(r, EAX=self.selecao()._volume_estrutura(r['EAX']))

    def engin_get_volume(self, r):
        """EnginGetVolume 0x440c5d (``selecao_ordens``). Only EAX changes."""
        return dict(r, EAX=self.selecao()._volume_unidade(r['EAX']))

    def engin_get_type(self, r):
        return dict(r, EAX=tipo_da_unidade(self.m, r['EAX'])['EAX'])

    def engin_get_player(self, r):
        return dict(r, EAX=dono_da_unidade(self.m, r['EAX'])['EAX'])

    def terrain_est_decouvert(self, r):
        return dict(r, **terreno_esta_descoberto(self.m, r['EAX'], r['EDX']))

    def _vie(self, u):
        """EnginGetVie 0x45718a: EAX = pool upper word | life +0x9a."""
        return _w(self._pool(), self.m.u16(self._rec(u) + 0x9a))

    def _vie_max(self, u):
        """EnginGetVieMax 0x441108: EAX = the type's maximum life (u16 0x4965b6 + 50 * type)."""
        return self.m.u16(VIDA_MAXIMA + 50 * self.m.u8(self._rec(u) + 1))

    def _blesse(self, u):
        """EnginEstBlesse 0x4420a6: EAX = life with AL = (maximum != life)."""
        vida = self.m.u16(self._rec(u) + 0x9a)
        maximo = self._vie_max(u)
        base = ((self.m.u8(self._rec(u) + 1) * 25) & 0xffff0000) | vida
        return _b(base, int(maximo != vida))

    def _bombe_max(self, u):
        """EnginBombeEstMax 0x44841b: EAX = (+0xda == 5)."""
        return int(self.m.u8(self._rec(u) + 0xda) == 5)

    @staticmethod
    def _est_troupe(eax):
        """TypeEnginEstTroupe 0x442347: AX = 0x101 for a troop type, 0 otherwise."""
        return _w(eax, 0 if eax & 0xff in NAO_TROPAS else 0x101)

    @staticmethod
    def _est_a_pied(eax):
        """TypeEnginEstAPied 0x4423b0: AL = 0 for types 3 and 11..17, else 1."""
        return _b(eax, 0 if eax & 0xff in NAO_A_PE else 1)

    @staticmethod
    def _est_engin(eax):
        """TypeEnginEstEngin 0x442434: EAX = 1 for types 11..17; else AL - 11 then AL = 0."""
        t = (eax - 0xb) & 0xff
        return 1 if t <= 6 else eax & 0xffffff00

    def _tipo_unidade(self, u):
        """EnginGetType's EAX."""
        return tipo_da_unidade(self.m, u)['EAX']

    # ------------------------------------------------------------ PlaceLibre
    def place_libre(self, r):
        """PlaceLibre 0x41f552: AX structure, DX unit. AL = room for the unit:
        - type 8: count < [0x495be9] / 2 + 1;
        - type 0x13: a unit not at full life, or a full-life colonist: BagAccepte(1); then a full-life colonist
          needs (full-life colonists inside) < capacity byte - [0x495be8], any other unit (other tag-1 units)
          < [0x495be8];
        - other types: BagAccepte(Bag, 1).
        Only EAX and EDX change."""
        m = self.m
        s, u = r['EAX'] & 0xffff, r['EDX'] & 0xffff
        e = self._est(s)
        tipo = m.u8(e + 8)
        bag = e + 0xc
        if tipo == 8:
            n = m.u16(bag)
            limite = ((m.u8(LIMITE_CASERNA) >> 1) + 1) & M32
            ok = n < limite
            return dict(r, EAX=_b(limite, int(ok)), EDX=_b(n, int(ok)))
        if tipo != 0x13:
            a = self.bag_accepte(dict(r, EAX=bag, EDX=1))
            ok = a['EAX'] & 0xff
            return dict(r, EAX=_b(a['EAX'], int(bool(ok))), EDX=_b(a['EDX'], int(bool(ok))))
        vida, maximo = self._vie(u), self._vie_max(u)
        colono = (self._tipo_unidade(u) & 0xff) == 9
        if (vida & 0xffff) == maximo and not colono:
            return dict(r, EAX=_b(self._tipo_unidade(u) & 0xff, 0), EDX=_b(u, 0))
        a = self.bag_accepte(dict(r, EAX=bag, EDX=1, EBX=vida))
        if not a['EAX'] & 0xff:
            return dict(r, EAX=_b(a['EAX'], 0), EDX=_b(a['EDX'], 0))
        n = m.u16(bag)
        outros = cheios = 0
        for i in range(n):
            if m.u8(bag + 0x42 + i) != 1:
                continue
            v = m.u16(bag + 6 + 2 * i)
            if (self._tipo_unidade(v) & 0xff) != 9:
                outros += 1
            elif (self._vie(v) & 0xffff) == self._vie_max(v):
                cheios += 1
            else:
                outros += 1
        if colono and (self._vie(u) & 0xffff) == self._vie_max(u):
            limite = (m.u8(TIPOS_ESTRUTURA + 52 * m.u8(e + 8) + 0x12) - m.u8(LIMITE_HOSPITAL)) & 0xff
            ok = cheios < limite
            return dict(r, EAX=int(ok), EDX=_b(cheios, int(ok)))
        limite = m.u8(LIMITE_HOSPITAL)
        ok = (outros & 0xffff) < limite
        return dict(r, EAX=_b(limite, int(ok)), EDX=_b(outros & 0xffff, int(ok)))

    # ------------------------------------------------------------ geometry
    def batiment_adjacent(self, r):
        """BatimentAdjacent 0x42381f: AX structure, DX cell. AL = 1 when one of the 8 in-grid neighbours (0..255
        on each axis) of the cell is a footprint cell whose BatimentCollision mask is set (rows of neighbours
        top to bottom, then columns; footprint rows then columns). EAX: BatimentCollision's with AL = 1, or 0;
        EDX as the loops leave it; EBX..EBP preserved."""
        m = self.m
        s = r['EAX'] & 0xffff
        celula = r['EDX'] & 0xffff
        x, y = celula % 256, celula // 256
        e = self._est(s)
        edx = r['EDX']
        for dy in (-1, 0, 1):
            edx = y
            if not 0 <= y + dy < 256:
                continue
            for dx in (-1, 0, 1):
                edx = x
                if not 0 <= x + dx < 256:
                    continue
                vizinho = (celula + dy * 256 + dx) & 0xffff
                origem = m.u16(e + 2)
                tipo = m.u8(e + 8)
                edx = tipo * 0x34
                w, h = self._tamanho(tipo)
                largura_dword = (((s * PASSO) & 0xffff0000) | w)
                for cy in range(h):
                    for cx in range(w):
                        alvo = origem + (cy << 8) + cx
                        edx = vizinho
                        if alvo != vizinho:
                            continue
                        indice = ((largura_dword * cy) + cx) & 0xffff
                        c = colisao_estrutura(m, m.u8(e + 8), indice)
                        edx = c.get('EDX', indice)
                        if c['EAX'] & 0xff:
                            return dict(r, EAX=_b(c['EAX'], 1), EDX=edx)
        return dict(r, EAX=0, EDX=edx)

    def get_case_centrale(self, r):
        """GetCaseCentrale 0x423b27: AX structure. EAX = origin + ((h >> 1) << 8) + (w >> 1) (u16 halves of the
        type's width/height, 32-bit sum over the origin word). Only EAX changes."""
        e = self._est(r['EAX'])
        w, h = self._tamanho(self.m.u8(e + 8))
        eax = (((h >> 1) << 8) + (w >> 1) + ((r['EDI'] & 0xffff0000) | self.m.u16(e + 2))) & M32
        return dict(r, EAX=eax)

    def batiment_get_case_entrer(self, r):
        """BatimentGetCaseEntrer 0x41d057: AX structure, DX unit. Type 14: origin + 0x402 (over the high word of
        index * 276); type 8: origin + 0x403 for a type-3 unit or a vehicle (TypeEnginEstEngin), else origin +
        0x303; other types 0. EDX = the structure record address; EBX..EBP preserved."""
        s = r['EAX'] & 0xffff
        e = self._est(s)
        tipo = self.m.u8(e + 8)
        if tipo == 0xe:
            return dict(r, EAX=((((s * PASSO) & 0xffff0000) | self.m.u16(e + 2)) + 0x402) & M32, EDX=e)
        if tipo != 8:
            return dict(r, EAX=0, EDX=e)
        t = self._tipo_unidade(r['EDX'] & 0xffff) & 0xff
        origem = self.m.u16(e + 2)
        if t == 3 or self._est_engin(t) & 0xff:
            return dict(r, EAX=origem + 0x403, EDX=e)
        return dict(r, EAX=origem + 0x303, EDX=e)

    # ------------------------------------------------------------ unit primitives
    def engin_reset_type(self, r):
        """EnginResetType 0x4571d4: AX unit becomes a colonist: type 9 and its fixed bytes (+0x93 = 1, +0x98 = 2,
        +0xa7 = 2, +0xa8 = 4, +0xa5 = 8, +0x9d = 0xff, +0xac = +0xad = 3, +0x99 = 0, +0xbb = 5), its Bag reset
        (count/volume/+4/capacity 0, 30 slots cleared), life clamped to the type-9 maximum. EBX..EBP preserved;
        EAX = the maximum life (type * 25 high word)."""
        m = self.m
        u = r['EAX'] & 0xffff
        c = self._rec(u)
        for off, v in ((1, 9), (0x93, 1), (0x98, 2), (0xa7, 2), (0xa8, 4), (0xa5, 8), (0x9d, 0xff), (0xac, 3),
                       (0xad, 3), (0x99, 0), (0xbb, 5)):
            m.u8(c + off, v)
        bag = c + 0xa
        for off in (0, 0x66, 4, 2):
            m.u16(bag + off, 0)
        for i in range(30):
            m.u16(bag + 6 + 2 * i, 0)
            m.u8(bag + 0x42 + i, 0)
        m.u16(bag + 2, 0)
        tipo = m.u8(self._rec(u) + 1)
        maximo = m.u16(VIDA_MAXIMA + 50 * tipo)
        if maximo < m.u16(c + 0x9a):
            m.u16(c + 0x9a, maximo)
        return dict(r, EAX=((tipo * 25) & 0xffff0000) | maximo)

    def retire_engin(self, r):
        """RetireEngin 0x457058: AX unit leaves the map: DeselectionEngin; ResetEnginCollision at +8, and at +0x7c
        when different; +0x72 = 0; SetMiniMap(owner, +8, 5); owners other than 0xc8/4 EteintTerrain(+8,
        +0xbb + +0xf5). EBX/ECX/EDX/ESI preserved; EAX: SetMiniMap's row counter, or EteintTerrain's last row index
        (radius + 1, sign-extended word: its loop bound at 0x476fba)."""
        m = self.m
        u = r['EAX'] & 0xffff
        c = self._rec(u)
        celula = m.u16(c + 8)
        self.selecao().deselection_engin(dict(r, EAX=u, EDX=0))
        w = self.mundo()
        w.ocupar(u, celula, False)
        if m.u16(c + 8) != m.u16(c + 0x7c):
            w.ocupar(u, m.u16(c + 0x7c), False)
        m.u8(c + 0x72, 0)
        dono = m.u8(c)
        w.minimapa(dono, celula, 5)
        if dono in (0xc8, 4):
            return dict(r, EAX=self._linhas_minimapa())
        raio = (m.u8(c + 0xbb) + m.u8(c + 0xf5)) & 0xffff
        w.apagar_area(m.u16(c + 8), raio, dono)
        return dict(r, EAX=_s16(raio + 1) & M32)          # EteintTerrain's: its last row index, sign-extended

    def _linhas_minimapa(self):
        """SetMiniMap 0x46a388's exit EAX: its row counter after the rows of one cell (minimap height / map
        height, at least 1), the same for every mode (``incursao_core.definir_minimapa``)."""
        from incursao_core import MINIMAPA_ALTURA, ALTURA_MAPA
        m = self.m
        sy = m.u16(MINIMAPA_ALTURA) // m.u16(ALTURA_MAPA)
        return sy if sy & 0xffff else 1

    def anim_work_engin(self, r):
        """AnimWorkEngin 0x447f58: AX unit; the work animation step of type 5 (phase 1), 7 (phase 12) and 13
        (phases 1 and 4): the tick +0xa9 rises; at +0xa7 it is cleared and the frame +0xa4 becomes (+0xa4 + 1)
        mod 4 (type 7: mod +0xa5, signed IDIV). EBX/ECX/EDX preserved; EAX: the entry EAX with AL = the type (or
        the phase on the paths that read it, AH = the tick or +0xa7 on types 13/7), or IDIV's quotient after a
        frame change."""
        m = self.m
        c = self._rec(r['EAX'])
        tipo = m.u8(c + 1)
        eax = _b(r['EAX'], tipo)
        if tipo not in (5, 7, 0xd):
            return dict(r, EAX=eax)
        fase = m.u8(c + 0x89)
        eax = _b(eax, fase)
        if tipo == 5 and fase != 1 or tipo == 7 and fase != 0xc or tipo == 0xd and fase not in (1, 4):
            return dict(r, EAX=eax)
        a9 = (m.u8(c + 0xa9) + 1) & 0xff
        m.u8(c + 0xa9, a9)
        if tipo == 7:
            eax = _h(eax, m.u8(c + 0xa7))
        elif tipo == 0xd and fase == 4:
            eax = _h(eax, a9)
        if a9 != m.u8(c + 0xa7):
            return dict(r, EAX=eax)
        dividendo = m.u8(c + 0xa4) + 1
        divisor = m.u8(c + 0xa5) if tipo == 7 else 4
        if divisor == 0:
            raise ForaDoDominioEntrada('AnimWorkEngin', 0x447fc7, 'divisor +0xa5 = 0 (the original faults)')
        m.u8(c + 0xa9, 0)
        m.u8(c + 0xa4, dividendo % divisor)
        return dict(r, EAX=dividendo // divisor)

    # ------------------------------------------------------------ adapters of existing Core translations
    def set_engin_collision(self, r):
        """SetEnginCollision 0x442cb4 (``chamadas_quadro_core.definir_colisao_unidade``)."""
        return dict(r, **definir_colisao_unidade(self.m, r['EAX'], r['EDX']))

    def set_deplace_engin(self, r):
        """SetDeplaceEngin 0x4457d3 (``selecao_ordens``, M2.3's live world): EAX = EDX = the unit record."""
        return self.selecao().set_deplace_engin(r)

    def deplace_engin(self, r):
        """DeplaceEngin 0x44930c (``construcao_core``); EAX may carry ``_incertos``."""
        return self.construcao().deplace_engin(dict(r))

    def engin_peut_passer(self, r):
        """EnginPeutPasser 0x442668 (M2.3's ``consultar_passagem``): AL exact; EAX bits 8+, EBX and EDX are the
        loops' and are marked uncertain (ECX too: the routine keeps its flags in CL/CH). ESI/EDI/EBP preserved."""
        from passagem_unidades import consultar_passagem
        ok = consultar_passagem(self.mundo(), r['EAX'] & 0xffff, r['EDX'] & 0xffff, r['EBX'] & 0xff)[0]
        return dict(r, EAX=int(bool(ok)), EBX=0, ECX=0, EDX=0,
                    _incertos={'EAX': 0xffffff00, 'EBX': M32, 'ECX': M32, 'EDX': M32})

    def decouvre_terrain(self, r):
        """DecouvreTerrain 0x476851 (M2.3's ``descobrir_area``; the body adds one to DX). Exit registers from the
        loop bounds: EAX = DX + 1 (u16), EDX = DX + 2 (sign-extended word), EBX low word = the row past the
        disc; EBX's high word is uninitialized stack (uncertain). ECX/ESI/EDI/EBP preserved."""
        celula, raio, dono = r['EAX'] & 0xffff, r['EDX'], r['EBX'] & 0xff
        self.mundo().descobrir_area(celula, raio & 0xffff, dono)
        edi = (raio + 1) & M32
        fim = (_s16(edi) + 1) & 0xffff
        y = celula // 256
        return dict(r, EAX=edi & 0xffff, EDX=_s16(fim) & M32, EBX=(y + _s16(edi) + 1) & 0xffff,
                    _incertos={'EBX': 0xffff0000})

    def illumine_terrain(self, r):
        """IllumineTerrain 0x476cb3 (M2.3's ``iluminar_area``). Exit registers from its second row loop's bound
        (0x476df9): EAX = DX + 1 (the row word, sign-extended), EDX = DX (u16), EBX low word = DX + 1 (the row
        dword incremented: its high word is a 16-bit local's never-written upper half, uncertain). ECX/ESI/EDI/EBP
        preserved."""
        raio = r['EDX'] & 0xffff
        self.mundo().iluminar_area(r['EAX'] & 0xffff, raio, r['EBX'] & 0xff)
        return dict(r, EAX=_s16(raio + 1) & M32, EBX=(raio + 1) & 0xffff, EDX=raio, _incertos={'EBX': 0xffff0000})

    def batiment_modify_map(self, r):
        """BatimentModifyMap 0x419e97 (``minimapa_estruturas``): DL nonzero mode 6, zero mode 7. EBX/ECX/ESI/EDI/
        EBP preserved; EAX and EDX are the loops' (uncertain)."""
        from minimapa_estruturas import modificar_minimapa_estrutura
        modificar_minimapa_estrutura(_MundoEstruturasCopiadas(self.mundo()), r['EAX'] & 0xffff, r['EDX'] & 0xff)
        return dict(r, EAX=0, EDX=0, _incertos={'EAX': M32, 'EDX': M32})

    # ------------------------------------------------------------ order setters
    def set_engin_rentre_batiment(self, r):
        """SetEnginRentreBatiment 0x445b10: AX unit, DX structure (BL unused). Sets the entry order: destination
        +0x7e (and +0xb2 for types 8/14/0x12), +0xc0 = structure, +0x88 = 0, the search released when the unit
        owns it; then a live unit (state not 0/4) goes to state 13 (0x15 for a non-colonist at a type-8
        structure). Type 8 with a non-colonist: +0xb2 = +0x7e = BatimentGetCaseEntrer; type 14 with a vehicle
        (11..17) unless the structure's +5 is 4: the same; type 0x12 with a type-16 unit: BatimentGetCase + 1;
        otherwise +0x7e = BatimentGetCase. Only EAX and EDX change."""
        m = self.m
        ecx, esi = r['ECX'], r['EDX']
        u, s = r['EAX'] & 0xffff, r['EDX'] & 0xffff
        ecx = r['EAX']
        rec = self._rec(u)
        tipo_s = m.u8(self._est(s) + 8)
        tipo_u = m.u8(rec + 1) if tipo_s in (8, 0xe, 0x12) else None    # read only where the original does
        if tipo_s == 8 and tipo_u != 9:
            ax = self.batiment_get_case_entrer(dict(r, EAX=s, EDX=u))['EAX']
            m.u16(rec + 0xb2, ax)
            m.u16(rec + 0x7e, ax)
            self._liberar_busca(u)
            m.u8(rec + 0x88, 0)
            m.u16(rec + 0xc0, esi)
            edx = ecx
            if not self._vivo(u):
                return dict(r, EAX=0, EDX=edx)
            m.u8(rec + 2, 0x15)
            eax = 0 if self._liberar_busca(u) else rec
            return dict(r, EAX=eax, EDX=edx)
        if tipo_s == 0xe and ((tipo_u - 0xb) & 0xff) <= 6 and m.u8(self._est(s) + 5) != 4:
            ax = self.batiment_get_case_entrer(dict(r, EAX=s, EDX=u))['EAX']
            m.u16(rec + 0xb2, ax)
            m.u16(rec + 0x7e, ax)
            self._liberar_busca(u)
            m.u8(rec + 0x88, 0)
            m.u16(rec + 0xc0, esi)
            if not self._vivo(u):
                return dict(r, EAX=0, EDX=self._pool())
            m.u8(rec + 2, 0xd)
            self._liberar_busca(u)
            return dict(r, EAX=rec, EDX=((u * PASSO) & 0xffffff00) | 0xd)
        if tipo_s == 0x12 and tipo_u == 0x10:
            c = (caso_estrutura(m, s)['EAX'] + 1) & M32
            m.u16(rec + 0xb2, c)
        else:
            c = caso_estrutura(m, s)['EAX']
        m.u16(rec + 0x7e, c)
        self._liberar_busca(u)
        m.u8(rec + 0x88, 0)
        m.u16(rec + 0xc0, esi)
        if not self._vivo(u):
            return dict(r, EAX=0, EDX=(u * PASSO) & M32)
        m.u8(rec + 2, 0xd)
        if self._liberar_busca(u):
            return dict(r, EAX=rec & 0xffff00ff, EDX=0xffff)
        return dict(r, EAX=rec, EDX=(self._pool() & 0xffffff00) | 0xd)

    def set_engin_select_rentre_batiment(self, r):
        """SetEnginSelectRentreBatiment 0x473f4b: AL player, DX structure. Every live unit of the player's
        selection gets SetEnginRentreBatiment(unit, structure, BL = its type). For the local player the first live
        unit speaks (EnginAsk, BL = 0): mode 0xe at structure types 1/10/13, 0xa at a sanctuary (not a type-10
        unit), 0x19 (colonist) or 0x24 (type 10) at type 16. Only EAX and EDX change."""
        m = self.m
        jogador = r['EAX'] & 0xff
        s = r['EDX'] & 0xffff
        eax = self.batiment_get_type(dict(r, EAX=s))['EAX']
        stipo = eax & 0xff
        edx = r['EDX']
        di = si = 0
        while si < m.u16(SELECOES + (jogador << 9)):
            u = m.u16(SELECOES + (jogador << 9) + 2 + 2 * si)
            si += 1
            vivo = self._vivo(u)
            eax = int(vivo)
            if not vivo:
                continue
            t = self._tipo_unidade(u)
            rr = self.set_engin_rentre_batiment(dict(r, EAX=u, EDX=s, EBX=_b(r['EBX'], t), ECX=u))
            eax, edx = rr['EAX'], rr['EDX']
            eax = di
            if di >= 1:
                continue
            local = m.u8(JOGADOR_LOCAL)
            eax = (local << 8) | jogador
            di += 1
            if jogador != local:
                continue
            edx = _b(edx, stipo)
            modo = None
            if stipo in (1, 0xa, 0xd):
                modo = 0xe
            elif stipo == 2:
                eax = t & 0xff
                if eax != 0xa:
                    modo = 0xa
            elif stipo == 0x10:
                edx = t & 0xff
                modo = {9: 0x19, 0xa: 0x24}.get(edx)
            if modo is not None:
                p = self.selecao().engin_ask(dict(r, EAX=u, EDX=modo, EBX=0, ECX=u))
                eax, edx = p['EAX'], p['EDX']
        return dict(r, EAX=eax, EDX=edx)

    def engin_select_peut_entrer(self, r):
        """EnginSelectPeutEntrer 0x472b6c: AL player, DL mode, BX structure (mode 3) or unit (mode 1).
        AL = 0 when a live selected unit is a mirror (EnginEstMiroir). Mode 3, at an own or 0xc8 structure: a
        selection of live colonists only enters any type but 9. Then, at an own structure only: type 0x15 when
        every live unit is on foot; type 2 when every live unit is a troop; type 0x13 when every live unit is a
        troop and one is wounded; type 0xe when every live unit is a vehicle and one is wounded or has its bomb
        not full; type 0x12 when every live unit has type 16; type 8 always. At a foreign structure: type 16 when
        every live unit has type 10. Mode 1: a vehicle target (11..17, not 16) when every live unit is a troop;
        a type-17 target refuses a selection holding a live type-8 unit. Other modes give 0. "Every" needs at
        least one live unit. ECX/ESI preserved; EAX (AL set), EBX and EDX as the loops leave them."""
        m = self.m
        st = dict(EAX=r['EAX'], EBX=r['EBX'], EDX=r['EDX'])
        jogador, modo, alvo = r['EAX'] & 0xff, r['EDX'] & 0xff, r['EBX'] & 0xffff
        lista = SELECOES + (jogador << 9)
        n = lambda: m.u16(lista)
        unidade = lambda i: m.u16(lista + 2 + 2 * i)

        def sair(al):
            return dict(r, EAX=_b(st['EAX'], al), EBX=st['EBX'], EDX=st['EDX'])

        def vivo_bx(i):
            """Shape with the index in EBX: EDX = player << 9 at the test; EAX = EDX = unit, then EnginEstVivant."""
            u = unidade(i)
            st['EAX'] = st['EDX'] = u
            v = self._vivo(u)
            st['EAX'] = int(v)
            return u, v

        def todos_bx(teste):
            """CL = 1 at each live match, 0 (and stop) at the first live miss; index in EBX."""
            st['EBX'] = 0
            cl = 0
            while True:
                st['EDX'] = jogador << 9
                if (st['EBX'] & 0xffff) >= n():
                    return bool(cl)
                u, v = vivo_bx(st['EBX'] & 0xffff)
                if v:
                    if teste(u):
                        cl = 1
                    else:
                        return False
                st['EBX'] = (st['EBX'] + 1) & M32

        def conta_bx(teste):
            """ECX counts live units passing ``teste``; index in EBX. Returns the count."""
            st['EBX'] = 0
            c = 0
            while True:
                st['EDX'] = jogador << 9
                if (st['EBX'] & 0xffff) >= n():
                    return c
                u, v = vivo_bx(st['EBX'] & 0xffff)
                if v and teste(u):
                    c += 1
                st['EBX'] = (st['EBX'] + 1) & M32

        def tipo(u):
            st['EAX'] = self._tipo_unidade(u) & 0xff
            return st['EAX']

        # the mirror test (index EBX)
        st['EBX'] = 0
        while True:
            st['EDX'] = jogador << 9
            if (st['EBX'] & 0xffff) >= n():
                st['EAX'] = _b(st['EAX'], 0)
                break
            u, v = vivo_bx(st['EBX'] & 0xffff)
            if v:
                st['EAX'] = unidade_espelho(m, u)['EAX']
                if st['EAX'] & 0xff:
                    return sair(0)
            st['EBX'] = (st['EBX'] + 1) & M32
        if modo == 3:
            e = self._est(alvo)
            st['EDX'] = alvo
            stipo = m.u8(e + 8)
            dono = m.u8(e + 4)
            st['EAX'] = _b(e, dono)
            if dono == jogador or dono == 0xc8:
                # every live unit a colonist (index in EDX, EBX = player << 9 / unit / unit * 276)
                st['EDX'] = 0
                cl = 0
                while True:
                    st['EBX'] = jogador << 9
                    if (st['EDX'] & 0xffff) >= n():
                        break
                    u = unidade(st['EDX'] & 0xffff)
                    st['EAX'] = st['EBX'] = u
                    v = self._vivo(u)
                    st['EAX'] = int(v)
                    if v:
                        st['EBX'] = (u * PASSO) & M32
                        st['EAX'] = self._pool()
                        if m.u8(self._rec(u) + 1) == 9:
                            cl = 1
                        else:
                            cl = 0
                            break
                    st['EDX'] = (st['EDX'] + 1) & M32
                if cl:
                    st['EAX'] = stipo
                    if stipo != 9:
                        return sair(1)
            st['EAX'] = _b(st['EAX'], dono)
            if dono != jogador:
                st['EAX'] = stipo
                if stipo != 0x10:
                    return sair(0)
                ok = todos_bx(lambda u: (st.__setitem__('EAX', (u * PASSO) & M32) or
                                          st.__setitem__('EDX', self._pool()) or
                                          m.u8(self._rec(u) + 1) == 0xa))
                return sair(1 if ok else 0)
            st['EAX'] = stipo
            if stipo == 0x15:
                st['EBX'] = 0
                todos_a_pe = True
                while True:
                    st['EDX'] = jogador << 9
                    if (st['EBX'] & 0xffff) >= n():
                        break
                    u, v = vivo_bx(st['EBX'] & 0xffff)
                    if v:
                        st['EAX'] = self._est_a_pied(tipo(u))
                        if not st['EAX'] & 0xff:
                            todos_a_pe = False
                            break
                    st['EBX'] = (st['EBX'] + 1) & M32
                if todos_a_pe:
                    return sair(1)
            if todos_bx(lambda u: (st.__setitem__('EAX', self._est_troupe(tipo(u))) or st['EAX'] & 0xff)):
                st['EAX'] = stipo
                if stipo == 2:
                    return sair(1)
                if stipo == 0x13:
                    c = conta_bx(lambda u: (st.__setitem__('EAX', self._blesse(u)) or st['EAX'] & 0xff))
                    st['EAX'] = int(c >= 1)
                    if c >= 1:
                        return sair(1)
            st['EAX'] = stipo
            if stipo == 0xe:
                if todos_bx(lambda u: (st.__setitem__('EAX', self._est_engin(tipo(u))) or st['EAX'] & 0xff)):
                    c = conta_bx(lambda u: (st.__setitem__('EAX', self._blesse(u)) or st['EAX'] & 0xff))
                    st['EAX'] = int(c >= 1)
                    if c >= 1:
                        return sair(1)
                    c = conta_bx(lambda u: (st.__setitem__('EAX', self._bombe_max(u)) or not st['EAX'] & 0xff))
                    st['EAX'] = int(c >= 1)
                    if c >= 1:
                        return sair(1)
            st['EAX'] = stipo
            if stipo == 0x12:
                st['EDX'] = 0
                cl = 0
                while True:
                    st['EBX'] = jogador << 9
                    if (st['EDX'] & 0xffff) >= n():
                        break
                    u = unidade(st['EDX'] & 0xffff)
                    st['EAX'] = st['EBX'] = u
                    v = self._vivo(u)
                    st['EAX'] = int(v)
                    if v:
                        st['EAX'] = (u * PASSO) & M32
                        st['EBX'] = self._pool()
                        if m.u8(self._rec(u) + 1) == 0x10:
                            cl = 1
                        else:
                            cl = 0
                            break
                    st['EDX'] = (st['EDX'] + 1) & M32
                if cl:
                    return sair(1)
            st['EAX'] = stipo
            return sair(1 if stipo == 8 else 0)
        if modo == 1:
            st['EDX'] = alvo
            t = tipo(alvo)
            if t == 0x10:
                return sair(0)
            st['EAX'] = self._est_engin(tipo(alvo))
            if not st['EAX'] & 0xff:
                return sair(0)
            if not todos_bx(lambda u: (st.__setitem__('EAX', self._est_troupe(tipo(u))) or st['EAX'] & 0xff)):
                return sair(0)
            st['EDX'] = alvo
            if tipo(alvo) != 0x11:
                return sair(1)
            tipo(alvo)
            st['EBX'] = 0
            while True:
                st['EDX'] = jogador << 9
                if (st['EBX'] & 0xffff) >= n():
                    return sair(1)
                u, v = vivo_bx(st['EBX'] & 0xffff)
                if v and tipo(u) == 8:
                    return sair(0)
                st['EBX'] = (st['EBX'] + 1) & M32
        return sair(0)

    # ------------------------------------------------------------ CalculEntreBatiment and unit state 13
    def _estado_vivo_para(self, u, estado):
        """The inlined 'alive (state not 0/4) -> state := estado, search released' tail. Returns the EAX it leaves:
        0 when not alive; else the pool pointer (0 when the release clears it)."""
        if not self._vivo(u):
            return 0
        self.m.u8(self._rec(u) + 2, estado)
        return self._pool()

    def calcul_entre_batiment(self, r):
        """CalculEntreBatiment 0x449716: AX unit, its target structure +0xc0. Unit types 0..10 and 25 (others are
        outside this translation). Every register but EAX is preserved.
        - +0xc0 = 0xffff: nothing (EAX = 0xffff).
        - A type-8 structure of the unit's owner: +0xb2 = +0x7e = BatimentGetCaseEntrer, search released,
          +0x88 = 0; a live unit goes to state 0x15.
        - Otherwise, when +0x86 and +0x87 are zero and BatimentAdjacent(structure, +8): BatimentLogeEngin
          (Economy). Refused: a live unit goes to state 7. Lodged: RetireEngin, then +0x7c = +8 = BatimentGetCase,
          DeselectionEngin, state 14. Type-10 units: at a type-16 structure state 0 after DeselectionEngin(0x44)
          and iagUnitSendMessage; at a foreign sanctuary PlayerInitPropositionAlliance first. Other units (not
          colonists) entering a structure other than 0x13/0x15: iagUnitSendMessage(0x47) and EnginResetType.
        - Not adjacent: at +0x7e == +8 the destination becomes BatimentGetCase (search released, +0x88 = 0); then
          DeplaceEngin."""
        m = self.m
        u = r['EAX'] & 0xffff
        rec = self._rec(u)
        tu = m.u8(rec + 1)
        if not (tu <= 10 or tu == 0x19):
            raise ForaDoDominioEntrada('CalculEntreBatiment', 0x449c56 if tu == 0x10 else 0x44a12f,
                                       f'unit type {tu} (vehicle or type-16 entry)')
        s = m.u16(rec + 0xc0)
        if s == 0xffff:
            return dict(r, EAX=0xffff)
        e = self._est(s)
        if m.u8(e + 8) == 8 and m.u8(e + 4) == m.u8(rec):
            c = self.batiment_get_case_entrer(dict(r, EAX=s, EDX=u))['EAX']
            m.u16(rec + 0xb2, c)
            m.u16(rec + 0x7e, c)
            self._liberar_busca(u)
            m.u8(rec + 0x88, 0)
            if not self._vivo(u):
                return dict(r, EAX=0)
            m.u8(rec + 2, 0x15)
            return dict(r, EAX=0 if self._liberar_busca(u) else self._pool())
        adjacente = False
        if not m.u8(rec + 0x86) and not m.u8(rec + 0x87):
            adjacente = bool(self.batiment_adjacent(dict(r, EAX=s, EDX=m.u16(rec + 8)))['EAX'] & 0xff)
        if not adjacente:
            if m.u16(rec + 0x7e) == m.u16(rec + 8):
                c = caso_estrutura(m, s)['EAX']
                m.u16(rec + 0x7e, c)
                self._liberar_busca(u)
                m.u8(rec + 0x88, 0)
            d = self.deplace_engin(dict(r, EAX=u))
            saida = dict(r, EAX=d['EAX'])
            if d.get('_incertos', {}).get('EAX'):
                saida['_incertos'] = {'EAX': d['_incertos']['EAX']}
            return saida
        regs_loge = dict(r, EAX=s, EDX=u, ECX=u, EBX=(u * PASSO) & M32,
                         EBP=(u * PASSO) & M32, ESI=rec, EDI=r['EAX'])
        loge = self._ext('BatimentLogeEngin', 0x449976, regs_loge)
        if not loge['EAX'] & 0xff:
            if not self._vivo(u):
                return dict(r, EAX=0)
            m.u8(rec + 2, 7)
            self._liberar_busca(u)
            return dict(r, EAX=self._pool())
        c = caso_estrutura(m, s)['EAX']
        self.retire_engin(dict(r, EAX=u, EDX=c, EBX=(u * PASSO) & M32, ECX=u))
        tu = m.u8(rec + 1)
        ts = m.u8(e + 8)
        if tu == 0xa and ts == 0x10:
            m.u16(rec + 0x7c, c)
            m.u16(rec + 8, c)
            self.selecao().deselection_engin(dict(r, EAX=u, EDX=0x44, EBX=0))
            self._ext('iagUnitSendMessage', 0x4499ee, dict(r, EAX=u, EDX=0x44, EBX=0, ECX=u))
            if not self._vivo(u):
                return dict(r, EAX=0)
            m.u8(rec + 2, 0)
            return dict(r, EAX=0 if self._liberar_busca(u) else self._pool())
        if tu == 0xa and ts == 2 and m.u8(e + 4) != m.u8(rec):
            dono_s = m.u8(e + 4)
            self._ext('PlayerInitPropositionAlliance', 0x449ad7,
                      dict(r, EAX=m.u8(rec), EDX=dono_s, ECX=u))
            m.u16(rec + 0x7c, c)
            m.u16(rec + 8, c)
            self.selecao().deselection_engin(dict(r, EAX=u, EDX=0x44, EBX=0))
            self._ext('iagUnitSendMessage', 0x449af8, dict(r, EAX=u, EDX=0x44, EBX=0, ECX=u))
            if not self._vivo(u):
                return dict(r, EAX=0)
            m.u8(rec + 2, 0)
            return dict(r, EAX=0 if self._liberar_busca(u) else self._pool())
        if tu != 9 and ts not in (0x13, 0x15):
            self._ext('iagUnitSendMessage', 0x449bb8, dict(r, EAX=u, EDX=0x47, EBX=0, ECX=u))
            self.engin_reset_type(dict(r, EAX=u))
        m.u16(rec + 0x7c, c)
        m.u16(rec + 8, c)
        d = self.selecao().deselection_engin(dict(r, EAX=u))
        m.u8(rec + 2, 0xe)
        return dict(r, EAX=d['EAX'])

    def estado_entrada(self, r):
        """Unit state 13's body 0x4558e4 inside EnginNextEtape: ESI = the unit record, DI = the unit; it ends at
        the continuation 0x454ccd (returned registers are those there). With a structure +0xc0:
        - BatimentEnDestruction, or a refused entry (see below): SetDeplaceEngin(unit, +0x7e), +0xc0 = 0xffff;
        - type-10 units: refused at a 0xc8 structure and at an own type-16 structure, else CalculEntreBatiment;
        - other units: CalculEntreBatiment at an own structure, or at a 0xc8 structure for a colonist; refused
          otherwise.
        Without a structure and without a vehicle (+0xb8 = 0xffff): nothing. A vehicle entry is outside this
        translation."""
        m = self.m
        rec, u = r['ESI'], r['EDI'] & 0xffff
        s = m.u16(rec + 0xc0)
        if s == 0xffff:
            v = m.u16(rec + 0xb8)
            if v == 0xffff:
                return dict(r, EAX=0xffff)
            raise ForaDoDominioEntrada('EnginNextEtape state 13', 0x4559c6, 'entering a vehicle (+0xb8)')
        e = self._est(s)
        recusa = bool(m.u8(e + 5) == 3)
        if not recusa:
            dono_s, dono_u = m.u8(e + 4), m.u8(rec)
            if m.u8(rec + 1) == 0xa:
                recusa = dono_s == 0xc8 or (dono_s == dono_u and m.u8(e + 8) == 0x10)
            else:
                recusa = dono_s != dono_u and not (dono_s == 0xc8 and m.u8(rec + 1) == 9)
        if recusa:
            d = self.set_deplace_engin(dict(r, EAX=u, EDX=m.u16(rec + 0x7e)))
            m.u16(rec + 0xc0, 0xffff)
            return dict(r, EAX=d['EAX'], EDX=d['EDX'])
        c = self.calcul_entre_batiment(dict(r, EAX=u))
        saida = dict(r, EAX=c['EAX'])
        if c.get('_incertos'):
            saida['_incertos'] = c['_incertos']
        return saida


    # ------------------------------------------------------------ releasing a colonist (tag 0x21)
    def _recherche_decalage_sortie(self, s):
        """RechercheDecalageSortie 0x41d1d0 (AX structure), its AX: the first in-grid cell of the 8 around
        CalculPosition (rows then columns) whose attribute bit 0 is clear (TerrainEnCollision mask 1), else the
        CalculPosition cell. Types 9/12/17 skip CalculPosition and read uninitialized locals (outside)."""
        from incursao_core import terreno_em_colisao
        m = self.m
        tipo = m.u8(self._est(s) + 8)
        if tipo > 0x15 or tipo in (9, 0xc, 0x11):
            raise ForaDoDominioEntrada('RechercheDecalageSortie', 0x41d23d, f'structure type {tipo}')
        cp = self._calcul_position(s)
        x, y = cp % 256, cp // 256
        for dy in (-1, 0, 1):
            if not 0 <= y + dy < 256:
                continue
            for dx in (-1, 0, 1):
                if not 0 <= x + dx < 256 or (dx == 0 and dy == 0):
                    continue
                celula = (cp + dy * 256 + dx) & 0xffff
                if not terreno_em_colisao(m, celula, 1)['EAX'] & 0xff:
                    return celula
        return cp

    def _calcul_position(self, s):
        """CalculPosition 0x420698 (``posicao_saida``) with the live geometry words; its AX."""
        from posicao_saida import calcular_posicao_saida
        tipo = self.m.u8(self._est(s) + 8)
        return calcular_posicao_saida(_MundoEstruturasCopiadas(self.mundo()), s, 0, self._tamanho(tipo)) & 0xffff

    def _enleve_un_colon(self, s):
        """BatimentEnleveUnColon 0x41d931 for structure types other than 5 and 8: the structure's rally cell +0x7c =
        RechercheDecalageSortie; the exit cell = CalculPosition; the first colonist BagRetire(Bag, 1, 9) gets
        EnginResetFatigue, SetSortEngin(exit cell), iagUnitSendMessage(0x42) and SetDeplaceEngin(+0x7c).
        Returns BagRetire's EAX (0xffff when the Bag holds no colonist)."""
        m = self.m
        e = self._est(s)
        if m.u8(e + 8) in (5, 8):
            raise ForaDoDominioEntrada('BatimentEnleveUnColon', 0x41d964 if m.u8(e + 8) == 8 else 0x41d9e1,
                                       f'structure type {m.u8(e + 8)}')
        m.u16(e + 0x7c, self._recherche_decalage_sortie(s))
        saida = self._calcul_position(s)
        bag = e + 0xc
        for _ in range(m.u16(bag)):
            u = self.bag_retire(dict(EAX=bag, EDX=1, EBX=9, ECX=0, ESI=0, EDI=0, EBP=0))['EAX']
            if u & 0xffff == 0xffff:
                continue
            rec = self._rec(u)
            m.u16(rec + 0x74, 0)                        # EnginResetFatigue 0x4530fd (recuperacao_unidades):
            m.u16(rec + 4, m.u16(rec + 0x76))           # +0x74 = 0, +4 = +0x76
            self._set_sort_engin(u & 0xffff, saida)
            self._ext('iagUnitSendMessage', 0x41da48, {k: 0 for k in REG7}, EAX=u & 0xffff, EDX=0x42)
            self.set_deplace_engin(dict(EAX=u & 0xffff, EDX=m.u16(e + 0x7c), EBX=0, ECX=0, ESI=0, EDI=0, EBP=0))
            return u
        return 0xffff

    def _set_sort_engin(self, u, celula):
        """SetSortEngin 0x445fbc over the live memory, in ``colocacao_saida.colocar_unidade_saida``'s order (that
        function protects its input with a ``bytearray`` pool check a live memory view cannot pass, so its body
        order is followed here with the same world effects): +0x7e, +0x7c, +8, +0x7e = cell; search released;
        +0x88 = 0; a live unit goes to state 7 (search released again); +0xc0 = +0xb8 = 0xffff; +0x87 = +0x86 = 0;
        ``ocupar(True)`` (SetEnginCollision); +0x72 = 1; owners other than 4/200 ``descobrir_area(cell, bb+f5+2)``
        and ``iluminar_area(cell, bb+f5)``; ``minimapa(owner, cell, 4)``."""
        from insercao_unidades import SOMA_VISAO_MAXIMA_INSERCAO
        m, w = self.m, self.mundo()
        rec = self._rec(u)
        for off in (0x7e, 0x7c, 8, 0x7e):
            m.u16(rec + off, celula)
        self._liberar_busca(u)
        m.u8(rec + 0x88, 0)
        if m.u8(rec + 2) not in (0, 4):
            m.u8(rec + 2, 7)
            self._liberar_busca(u)
        m.u16(rec + 0xc0, 0xffff)
        m.u16(rec + 0xb8, 0xffff)
        m.u8(rec + 0x87, 0)
        m.u8(rec + 0x86, 0)
        w.ocupar(u, celula, True)
        m.u8(rec + 0x72, 1)
        atual, dono = m.u16(rec + 8), m.u8(rec)
        if dono not in (4, 200):
            raio = m.u8(rec + 0xbb) + m.u8(rec + 0xf5)
            if raio > SOMA_VISAO_MAXIMA_INSERCAO:
                raise ForaDoDominioEntrada('SetSortEngin', 0x446146, f'vision sum {raio}')
            w.descobrir_area(atual, raio + 2, dono)
            w.iluminar_area(atual, m.u8(rec + 0xbb) + m.u8(rec + 0xf5), m.u8(rec))
        w.minimapa(m.u8(rec), atual, 4)

    def batiment_retire_colon(self, r):
        """BatimentRetireColon 0x41dde0 (tag 0x21): AX structure. Type 12: nothing (EAX = 0xffff). Otherwise
        BatimentEnleveUnColon releases one colonist (see ``_enleve_un_colon``). When the structure then holds no
        colonist (types 2/0x15 also no troop), it is abandoned: EteintTerrain(BatimentGetCase, the type's radius,
        owner) except types 9/12, InitBatimentNeutre(structure, owner) (Economy), for types 1/2/5 the production
        fields are reset (+0x78 = 0xffff, +0x7b = 0xff, +0x7c = +0x7e = 0, +0x86 = 0xffff, +0x80 = +0x82 = 0
        unless type 0x14, +0x74 = 0, +0x8c = 0, +5 = 5 unless 3), the owner's structure selection 0x495be0 :=
        0xffff, owner := 0xc8 and BatimentModifyMap(structure, 1). EAX = the released unit (BagRetire's EAX) or
        0xffff; every other register preserved. Types 5/8/0xe with one colonist and types 0x13/0x15 are outside
        this translation."""
        m = self.m
        s = r['EAX'] & 0xffff
        e = self._est(s)
        tipo = m.u8(e + 8)
        if tipo == 0xc:
            return dict(r, EAX=0xffff)
        bag = e + 0xc
        um = (self.bag_contient(dict(r, EAX=bag, EDX=1, EBX=9))['EAX'] & 0xffff) == 1
        if um and tipo in (5, 8, 0xe):
            raise ForaDoDominioEntrada('BatimentRetireColon', 0x41de73 if tipo != 0xe else 0x41de3f,
                                       f'the last colonist of a type-{tipo} structure')
        if tipo in (0x13, 0x15):
            raise ForaDoDominioEntrada('BatimentRetireColon', 0x41df1c if tipo == 0x13 else 0x41df46,
                                       f'structure type {tipo:#x}')
        edi = self._enleve_un_colon(s)
        tipo = m.u8(e + 8)
        if tipo == 2 and self.bag_contient_troupe(dict(r, EAX=bag))['EAX'] & 0xff:
            return dict(r, EAX=edi)
        if self.bag_contient(dict(r, EAX=bag, EDX=1, EBX=9))['EAX'] & 0xffff:
            return dict(r, EAX=edi)
        dono = m.u8(e + 4)
        if tipo not in (9, 0xc):
            if tipo > 0x15:
                raise ForaDoDominioEntrada('BatimentRetireColon', 0x41e09f, f'structure type {tipo} (no radius)')
            centro = caso_estrutura(m, s)['EAX'] & 0xffff
            self.mundo().apagar_area(centro, RAIO_APAGAR[tipo], dono)
        self._ext('InitBatimentNeutre', 0x41e0d7, dict(r), EAX=s, EDX=dono, EBX=s)
        if m.u8(e + 8) in (1, 2, 5):
            m.u16(e + 0x78, 0xffff)
            m.u8(e + 0x7b, 0xff)
            m.u16(e + 0x7c, 0)
            m.u16(e + 0x7e, 0)
            m.u16(e + 0x86, 0xffff)
            if m.u8(e + 8) != 0x14:
                m.u16(e + 0x80, 0)
                m.u16(e + 0x82, 0)
            m.u8(e + 0x74, 0)
            m.u32(e + 0x8c, 0)
            if m.u8(e + 5) != 3:
                m.u8(e + 5, 5)
        m.u16(0x495be0 + 2 * m.u8(e + 4), 0xffff)
        m.u8(e + 4, 0xc8)
        self.batiment_modify_map(dict(r, EAX=s, EDX=1))
        if m.u8(e + 4) == m.u8(JOGADOR_LOCAL):
            raise ForaDoDominioEntrada('BatimentRetireColon', 0x41e152, 'local player 0xc8')
        return dict(r, EAX=edi)


def provedor_entrada(entrada, outros=None):
    """Economy's ``externo(nome, chamada, registradores) -> registradores`` for the Core routines its work cycle
    and lodging credit call (``ROTINAS_ECONOMIA``), run by ``entrada`` (an ``EntradaEstruturas`` over the same
    memory). Same shape as ``construcao_core.provedor_construcao``.

    Input: the argument registers (Economy passes only those, at their ``ARGUMENTOS`` widths) or all of EAX..EBP,
    optionally ``_incertos``. A missing register enters as 0 with a full uncertain mask. Output: EAX..EBP as the
    callee leaves them, after its stores; ``_incertos`` marks the bits not reconstructed (see the module
    docstring) and carries input masks for registers the callee leaves unchanged. Any other name goes to
    ``outros`` (same signature) or raises ``DependenciaRamoCore`` at its call."""
    def externo(nome, chamada, regs):
        if nome not in ROTINAS_ECONOMIA:
            if outros is None:
                raise DependenciaRamoCore(nome, chamada, 'no provider for this routine')
            return outros(nome, chamada, regs)
        entrada_regs = {k: regs.get(k, 0) & M32 for k in REG7}
        incertos_in = dict(regs.get('_incertos') or {})
        for k in REG7:
            if k not in regs:
                incertos_in[k] = M32
        saida = entrada.chamar(nome, entrada_regs)
        resultado = {k: saida[k] & M32 for k in REG7}
        incertos = {k: v for k, v in incertos_in.items() if resultado.get(k) == entrada_regs.get(k)}
        for k, v in (saida.get('_incertos') or {}).items():
            incertos[k] = incertos.get(k, 0) | v
        if incertos:
            resultado['_incertos'] = incertos
        return resultado
    return externo


ROTINAS_ECONOMIA = ('DeplaceEngin', 'SetDeplaceEngin', 'BatimentGetCase', 'GetCaseCentrale', 'BatimentAdjacent',
                    'EnginPeutPasser', 'SetEnginCollision', 'RetireEngin', 'AnimWorkEngin', 'EnginGetVolume',
                    'EnginGetType', 'EnginGetPlayer', 'EnginGetBag', 'PlaceLibre', 'BatimentModifyMap',
                    'BatimentGetVolume', 'BagContient', 'BagContientTroupe', 'BagRetire', 'BagPrend',
                    'DecouvreTerrain', 'IllumineTerrain', 'TerrainEstDecouvert')
