"""The unit-state dispatcher past frame 220: states 5/13/19 reach their owners' providers (no native run).

``construcao_entrada_ia.proxima_etapa_entrada`` continues at the pinned switch's stop for a state whose body an
owner translated; ``instalar_donos`` binds state 19 to Economy's ``alimentacao.estado_fome`` with ESI = the unit
record and EDI = the unit; ``DonosM3._externo_fome`` lets the hunger body keep a register its callee preserved.
"""
from pathlib import Path
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
import ambiente_ia_runtime  # noqa: E402,F401
from reinicio_ia import DependenciaIA  # noqa: E402
import construcao_entrada_ia as cei  # noqa: E402

M32 = 0xffffffff


class Memoria:
    def __init__(self, valores):
        self.v = dict(valores)

    def u32(self, a, valor=None):
        if valor is None:
            return self.v[a]
        self.v[a] = valor


class Despacho(unittest.TestCase):
    def tabelas(self):
        estados = [0] * 25
        estados[5], estados[13], estados[19] = cei.ESTADO_5, cei.ESTADO_13, cei.ESTADO_19
        return dict(estados=estados)

    def test_estado_19_vai_ao_provedor(self):
        chamadas = []
        p = {'EnginNextEtape:state19': lambda sitio, unidade: chamadas.append((sitio, unidade))}

        def etapa():
            raise DependenciaIA('EnginNextEtape state 19', cei.ESTADO_19)
        saida = cei.proxima_etapa_entrada(None, p, 0x1000c, self.tabelas(), None, etapa=etapa)
        self.assertEqual(saida, cei.SAIDA)
        self.assertEqual(chamadas, [(cei.ESTADO_19, 0xc)])

    def test_estado_19_sem_provedor_continua_parada(self):
        def etapa():
            raise DependenciaIA('EnginNextEtape state 19', cei.ESTADO_19)
        with self.assertRaises(DependenciaIA):
            cei.proxima_etapa_entrada(None, {}, 12, self.tabelas(), None, etapa=etapa)

    def test_outro_alvo_nao_despacha(self):
        tabelas = self.tabelas()
        tabelas['estados'][19] = 0x455000            # a table that does not point at the translated body
        p = {'EnginNextEtape:state19': lambda sitio, unidade: self.fail('dispatched')}

        def etapa():
            raise DependenciaIA('EnginNextEtape state 19', cei.ESTADO_19)
        with self.assertRaises(DependenciaIA):
            cei.proxima_etapa_entrada(None, p, 12, tabelas, None, etapa=etapa)

    def test_instalar_donos_estado_19(self):
        recebidos = []

        class Fome:
            def estado_fome(self, regs):
                recebidos.append(regs)
                return dict(regs)

        class Donos:
            fome = Fome()

            def rotina_core(self, nome):
                return None
        m = Memoria({0x4e19a0: 0x2000000})
        p = {'BatimentNextEtape': lambda sitio, estrutura: None}
        cei.instalar_donos(m, p, Donos(), dict(estados=[0] * 25, tipos_estrutura=[0] * 21))
        self.assertNotIn('EnginSetFatigue', p)
        p['EnginNextEtape:state19'](sitio=cei.ESTADO_19, unidade=12)
        self.assertEqual(recebidos, [dict(EAX=0, EBX=0, ECX=0, EDX=0, ESI=0x2000000 + 12 * 276, EDI=12, EBP=0,
                                          ESP=0)])

    def test_instalar_donos_fadiga_quando_core_publica(self):
        chamadas = []

        class Donos:
            fome = None

            def rotina_core(self, nome):
                if nome == 'EnginSetFatigue':
                    return lambda regs, chamada=0: chamadas.append((regs, chamada)) or dict(regs, EAX=7)
                return None
        p = {'BatimentNextEtape': lambda sitio, estrutura: None}
        cei.instalar_donos(Memoria({}), p, Donos(), dict(estados=[0] * 25, tipos_estrutura=[0] * 21))
        self.assertEqual(p['EnginSetFatigue'](sitio=0x45498f, unidade=14), 7)
        self.assertEqual((chamadas[0][0]['EAX'], chamadas[0][1]), (14, 0x45498f))


class ExternoFome(unittest.TestCase):
    def test_registro_preservado_fica_com_o_chamador(self):
        from provedores_entrada_ia import DonosM3
        d = DonosM3.__new__(DonosM3)
        d.externo = lambda nome, chamada, regs: dict(EAX=1, EBX=0, ECX=0, EDX=5, ESI=0, EDI=0, EBP=0x33,
                                                     _incertos=dict(EBX=M32, ECX=M32, ESI=M32, EDI=M32, EBP=M32,
                                                                    EDX=0xff00))
        saida = d._externo_fome('BatimentAdjacent', 0x455584, dict(EAX=3, EDX=5))
        # EBX/ECX/ESI/EDI were not passed and came back 0 fully uncertain: dropped (the caller keeps its own);
        # EBP changed (0x33) so it stays, still marked; EDX was passed and keeps its partial mark.
        self.assertEqual(saida, dict(EAX=1, EDX=5, EBP=0x33, _incertos=dict(EBP=M32, EDX=0xff00)))


class TerrainGetSacType(unittest.TestCase):
    """This front's leaf against the original bytes 0x476038 under Unicorn: every object byte, two register files."""

    def test_contra_o_original(self):
        try:
            import unicorn
            from unicorn import x86_const as X
            from inventario_ia_runtime import OriginalImage
        except ImportError as erro:
            self.skipTest(f'native check unavailable: {erro}')
        from entrada_quadro_ia import terrain_get_sac_type
        imagem = OriginalImage()
        uc = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_32)
        uc.mem_map(0x476000, 0x1000)
        uc.mem_write(0x476000, imagem.read(0x476000, 0x477000))
        uc.mem_map(0x507000, 0x1000)
        uc.mem_map(0x1000000, 0x20000)
        uc.mem_map(0x2000000, 0x10000)
        grade = 0x1003456
        uc.mem_write(0x507d74, grade.to_bytes(4, 'little'))
        nomes = dict(EAX=X.UC_X86_REG_EAX, EBX=X.UC_X86_REG_EBX, ECX=X.UC_X86_REG_ECX, EDX=X.UC_X86_REG_EDX,
                     ESI=X.UC_X86_REG_ESI, EDI=X.UC_X86_REG_EDI, EBP=X.UC_X86_REG_EBP)

        class Mem:
            def u32(self, a):
                return int.from_bytes(uc.mem_read(a, 4), 'little')

            def u8(self, a):
                return uc.mem_read(a, 1)[0]
        casos = 0
        for objeto in range(256):
            for celula, resto in ((0x0a14, 0x12345678), (0xfff0, 0x9abcdef0)):
                uc.mem_write(grade + celula, bytes([objeto]))
                regs = dict(EAX=(resto & 0xffff0000) | celula, EBX=resto ^ 1, ECX=resto ^ 2, EDX=resto ^ 3,
                            ESI=resto ^ 4, EDI=resto ^ 5, EBP=resto ^ 6)
                for k, v in regs.items():
                    uc.reg_write(nomes[k], v)
                uc.reg_write(X.UC_X86_REG_ESP, 0x2008000)
                uc.mem_write(0x2008000, (0xdead0000).to_bytes(4, 'little'))
                uc.emu_start(0x476038, 0xdead0000)
                nativo = {k: uc.reg_read(r) for k, r in nomes.items()}
                self.assertEqual(terrain_get_sac_type(Mem(), dict(regs)), nativo, (objeto, hex(celula)))
                casos += 1
        self.assertEqual(casos, 512)


if __name__ == '__main__':
    unittest.main()
