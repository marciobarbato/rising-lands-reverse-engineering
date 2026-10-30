"""Exact live Core owner callbacks for SortieTroupe (see RECRUITMENT_ADAPTERS.md).

Reuses Combat's conversion body on a live view, Core healing arithmetic and
physical collision/vision/minimap primitives. No mission state is constructed.
Partial input files follow entrada_estruturas' _incertos protocol; omitted
behaviour arguments raise ArgumentoNaoPassado before memory is accessed.
"""
from chamadas_quadro_core import M32, PONTEIRO_UNIDADES, PASSO, definir_colisao_unidade
from entrada_estruturas import ArgumentoNaoPassado
from experiencia_unidades import TIPOS_F7
from incursao_core import (TIPOS_UNIDADES, capacidade_tipo_engin, definir_minimapa, _BuscaPlana)
from unidades import curar_com_limite

REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
ROTINAS = {'EnginSetType': 0x457b87, 'EnginAddVie': 0x457122, 'EnginResetFatigue': 0x4530fd,
           'EnginSetExperimente': 0x44fe42, 'SetSortEngin': 0x445fbc}
ARGUMENTOS = {'EnginSetType': {'EAX': 0xffff, 'EDX': 0xffff, 'EBX': 0xff, 'ECX': 0xff},
              'EnginAddVie': {'EAX': 0xffff, 'EDX': 0xffff},
              'EnginResetFatigue': {'EAX': 0xffff}, 'EnginSetExperimente': {'EAX': 0xffff, 'EDX': 0xffff},
              'SetSortEngin': {'EAX': 0xffff, 'EDX': 0xffff}}
ALTERADOS = {'EnginSetType': ('EAX', 'EBX', 'ECX', 'EDX'), 'EnginAddVie': ('EAX', 'EDX'),
             'EnginResetFatigue': ('EAX',), 'EnginSetExperimente': ('EAX',), 'SetSortEngin': ('EAX', 'EDX')}
FILA_EXPERIENCIA = 0x4e19c4


class DependenciaRecrutamentoCore(NotImplementedError):
    def __init__(self, nome, endereco, motivo):
        self.rotina, self.endereco = nome, endereco
        super().__init__(f'{nome} at 0x{endereco:x}: {motivo}; earlier effects retained')


def bonus_recrutamento(memoria):
    """Economy's committed BonusUnidades bound to live buffers; never a copied/zero table."""
    from integracao.providers import load_economy_bonus
    return load_economy_bonus().BonusUnidades.da_memoria(memoria).consultar


class RecrutamentoCore:
    def __init__(self, memoria, *, bonus=None):
        self.m, self.bonus = memoria, bonus
        self._mundo = None

    @staticmethod
    def argumentos(nome):
        return ARGUMENTOS[nome]

    def _registro(self, eax):
        indice = eax & 0xffff
        if indice >= 800:
            raise ValueError('Recruitment requires unit AX in 0..799')
        return (self.m.u32(PONTEIRO_UNIDADES) + indice * PASSO) & M32

    def chamar(self, nome, regs, pilha=()):
        if nome not in ROTINAS:
            raise KeyError(nome)
        faltando = [k for k in REG7 if k not in regs]
        if faltando:
            raise ArgumentoNaoPassado(nome, ROTINAS[nome], faltando)
        if pilha:
            raise ValueError(f'{nome} takes no pushed words')
        r = {k: regs[k] & M32 for k in REG7}
        r.update(getattr(self, '_' + nome)(r))
        if 'ESP' in regs:
            r['ESP'] = (regs['ESP'] + 4) & M32
        return r

    def _EnginSetType(self, r):
        if self.bonus is None:
            raise DependenciaRecrutamentoCore('EnginSetType', 0x457b87, 'live BonusGetValEngin provider required')
        from conversao_unidades import _provedor
        from mundo_vivo import vista_de
        provedor = _provedor()
        m, tipo = self.m, r['ECX'] & 255
        if tipo >= 26:
            raise ValueError('Recruitment conversion requires type CL in 0..25')
        u = self._registro(r['EAX'])
        registro = vista_de(m, u, PASSO)
        if registro[0] not in (0, 1, 2, 3, 4, 200):
            raise ValueError('Conversion requires owner 0..3, 4 or 200')
        base = TIPOS_UNIDADES + tipo * 50
        caracteristicas = provedor.CaracteristicasTipo(*(m.u8(base + off) for off in (0x2a, 0x2c, 0x30)))
        capacidade = capacidade_tipo_engin(tipo)['EAX']
        consultas = {}
        def bonus(dono, t, seletor):
            consultas[seletor] = self.bonus(dono, t, seletor) & M32
            return consultas[seletor]
        # The same body as incursao_core.definir_tipo_unidade, on the live
        # record so bonus callbacks see earlier stores and failure retains them.
        provedor.definir_tipo(registro, r['EAX'] & 65535, r['EDX'] & 65535, r['EBX'] & 255,
                              tipo, caracteristicas, lambda t: capacidade, bonus, _BuscaPlana(m))
        # Neutral owners skip the owner's modifier in the local body; the
        # native BonusGetValEngin call still returns its neutral-owner zero.
        if 1 not in consultas:
            bonus(registro[0], tipo, 1)
        return dict(EAX=(capacidade + consultas[1]) & M32, EBX=0x1d, ECX=(u+10) & M32, EDX=0x1e)

    def _EnginAddVie(self, r):
        m, u = self.m, self._registro(r['EAX'])
        if m.u8(u+1) >= 26:
            raise ValueError('Healing requires live type 0..25')
        soma, _ = curar_com_limite(m.u16(u+0x9a), r['EDX'], 65535)
        m.u16(u+0x9a, soma)
        maximo = m.u16(TIPOS_UNIDADES + 50*m.u8(u+1) + 8)
        vida, excedeu = curar_com_limite(soma, 0, maximo)
        if excedeu:
            m.u16(u+0x9a, vida)
        return dict(EAX=(maximo & 0xff00) | int(excedeu), EDX=u)

    def _EnginResetFatigue(self, r):
        m, u = self.m, self._registro(r['EAX'])
        m.u16(u+0x74, 0)
        m.u16(u+4, m.u16(u+0x76))
        return dict(EAX=u)

    def _EnginSetExperimente(self, r):
        m, u = self.m, self._registro(r['EAX'])
        dono = m.u8(u)
        if dono >= 4:
            raise ValueError('Experience queue requires owner 0..3')
        fila = FILA_EXPERIENCIA + dono*10
        experiencia = m.u8(fila+1)
        if not experiencia or m.u8(fila) != m.u8(u+1):
            return dict(EAX=dono*10)
        # Raw-memory adaptation of consumir_experiencia_unidade / aplicar_nova_experiencia.
        # AF is committed before a nested type-table read; the queue shifts only afterwards.
        m.u8(u+0xaf, experiencia)
        nivel = experiencia >> 5
        if nivel in (2, 3):
            m.u8(u + (0xf6 if nivel == 2 else 0xf5), 1)
        elif nivel in (1, 4):
            tipo = m.u8(u+1)
            armee = tipo in TIPOS_F7
            if nivel == 1 and armee:
                m.u8(u+0xf7, 1)
            else:
                if tipo >= 26:
                    raise ValueError('Experience characteristic requires type 0..25; AF retained')
                palavra = m.u16(TIPOS_UNIDADES + tipo*50 + 0x2e)
                m.u8(u+0xf8, (palavra * (2 if nivel == 4 and not armee else 1) // 100) & 255)
        for i in range(4):
            m.u8(fila+i*2+1, m.u8(fila+i*2+3))
            m.u8(fila+i*2, m.u8(fila+i*2+2))
        m.u8(fila+9, 0)
        m.u8(fila+8, 255)
        return dict(EAX=dono*5)

    def _SetSortEngin(self, r):
        from insercao_unidades import SOMA_VISAO_MAXIMA_INSERCAO
        from visao_grupos import _MinimapaPlano, _VistaPlana
        m, u = self.m, self._registro(r['EAX'])
        indice, celula = r['EAX'] & 65535, r['EDX'] & 65535
        dono = m.u8(u)
        if m.u8(u+1) >= 26 or dono not in (0, 1, 2, 3, 4, 200):
            raise ValueError('Placement requires type 0..25 and owner 0..3, 4 or 200')
        largura, altura = m.u16(0x497168), m.u16(0x49716a)
        if not (1 <= largura <= 256 and 1 <= altura <= 256 and
                celula % 256 < largura and celula // 256 < altura and m.u8(0x508041) < 4 and
                (m.u16(0x496fe0), m.u16(0x496fe2)) == (128, 128)):
            raise ValueError('Placement requires an in-map cell, local owner 0..3 and 128x128 minimap')
        for off in (0x7e, 0x7c, 8, 0x7e):
            m.u16(u+off, celula)
        if m.u16(0x496304) == indice:
            m.u8(0x4e0f36, 0)
            m.u8(0x4e0f37, 0)
            m.u16(0x496304, 65535)
            m.u32(0x4e0f3c, 0)
        m.u8(u+0x88, 0)
        if m.u8(u+2) not in (0, 4):
            m.u8(u+2, 7)
            _BuscaPlana(m).liberar(indice)
        m.u16(u+0xc0, 65535)
        m.u16(u+0xb8, 65535)
        m.u8(u+0x87, 0)
        m.u8(u+0x86, 0)
        definir_colisao_unidade(m, indice, celula)
        m.u8(u+0x72, 1)
        if dono not in (4, 200):
            raio = m.u8(u+0xbb) + m.u8(u+0xf5)
            if raio > SOMA_VISAO_MAXIMA_INSERCAO:
                raise DependenciaRecrutamentoCore('SetSortEngin', 0x446146, f'vision sum {raio} exceeds validated domain')
            if self._mundo is None:
                self._mundo = _MinimapaPlano(m)
                self._mundo.contagem_luz = [_VistaPlana(m, m.u32(0x507d98 + 4*j)) for j in range(4)]
            self._mundo.descobrir_area(celula, raio+2, dono)
            self._mundo.iluminar_area(celula, m.u8(u+0xbb)+m.u8(u+0xf5), m.u8(u))
        out = definir_minimapa(m, m.u8(u), 4, celula)
        return dict(EAX=out['EAX'], EDX=out['EDX'])


def provedor_recrutamento(owner, outros=None):
    """externo(nome, chamada, regs) -> all seven registers and explicit unknown preserved bits."""
    def externo(nome, chamada, regs):
        if nome not in ROTINAS:
            if outros is None:
                raise DependenciaRecrutamentoCore(nome, chamada, 'no recruitment owner provider')
            return outros(nome, chamada, regs)
        masks = dict(regs.get('_incertos') or {})
        missing = [k for k, width in ARGUMENTOS[nome].items() if k not in regs or masks.get(k, 0) & width]
        if missing:
            raise ArgumentoNaoPassado(nome, chamada, missing)
        if regs.get('_pilha'):
            raise ValueError(f'{nome} takes no pushed words')
        entrada = {k: regs.get(k, 0) & M32 for k in REG7}
        for k in REG7:
            if k not in regs:
                masks[k] = M32
        out = owner.chamar(nome, entrada)
        result = {k: out[k] for k in REG7}
        unknown = {k: masks[k] & M32 for k in REG7 if masks.get(k) and k not in ALTERADOS[nome]}
        if unknown:
            result['_incertos'] = unknown
        return result
    return externo
