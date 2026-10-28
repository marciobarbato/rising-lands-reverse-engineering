"""Read-only volume, request order and explicit pending audio contracts."""
from dataclasses import asdict, replace
import struct
import unittest

from test_colocacao_saida import preparar
from colocacao_saida import ColocacaoSaidaTropa
from selecao_unidades import unidade_selecionada
from voz_unidades import (consultar_volume_unidade,solicitar_voz_unidade,retomar_solicitacao_saida,
                          DependenciaVozUnidade)


def preparar_voz(*,indice=7,dono=0,visivel=True,handle=0xffffffff,selecionada=1):
    m=preparar(indice=indice,dono=dono)
    m.palavra(indice,8,0x808)
    m.unidades[indice*276+0xbd]=selecionada
    struct.pack_into('<I',m.unidades,indice*276+0x104,handle)
    m.descoberto[m.jogador_local][0x808]=0 if visivel else 31
    m.efeitos=[]
    return m


class VozUnidades(unittest.TestCase):
    def test_selection_query_uses_flag_owner_and_no_list_or_activity(self):
        m=preparar_voz(handle=0)
        m.unidades[7*276+1],m.unidades[7*276+2]=255,0
        m.selecoes_unidades=None
        self.assertTrue(m.unidade_selecionada(0x100,0xabcd0007))
        self.assertFalse(unidade_selecionada(m,3,7))
        m.unidades[7*276+0xbd]=0
        self.assertFalse(unidade_selecionada(m,0,7))

    def test_volume_thresholds_full_eax_and_signed_distance_overflow(self):
        m=preparar_voz()
        for x,y,volume in ((12,1,256),(12,2,180),(10,14,180),(15,9,100),(24,5,0)):
            m.palavra(7,8,y*256+x)
            self.assertEqual(consultar_volume_unidade(m,7,(0,0,0,0)),volume)
            m.unidades[7*276+0xbd]=0
            self.assertEqual(m.consultar_volume_unidade(7,(0,0,0,0)),volume//2)
            m.unidades[7*276+0xbd]=1
        m.palavra(7,8,0)
        self.assertEqual(consultar_volume_unidade(m,7,(65535,65535,0,0)),256)
        self.assertEqual(consultar_volume_unidade(m,7,(65535,65535,3,3)),256)

    def test_hidden_guard_ignores_missing_viewport_and_inactive_handle(self):
        m=preparar_voz(visivel=False)
        antes=bytes(m.unidades)
        self.assertIsNone(m.solicitar_voz_unidade(7,16,255,janela='unneeded'))
        self.assertEqual(bytes(m.unidades),antes)

    def test_visible_queries_before_mode_override_or_active_handle_flag_store(self):
        m=preparar_voz(handle=0)
        antes=bytes(m.unidades)
        with self.assertRaises(DependenciaVozUnidade) as captura:
            solicitar_voz_unidade(m,7,16,255)
        self.assertEqual((captura.exception.endereco,captura.exception.checkpoint),(0x440c5d,0x440d9f))
        self.assertEqual(bytes(m.unidades),antes)
        solicitar_voz_unidade(m,7,16,0x1ff,janela=(0,0,16,16))
        esperado=bytearray(antes);esperado[7*276+0xf9]=255
        self.assertEqual(m.unidades,esperado)

    def test_pending_post_sound_preserves_or_overlap_volume_zero_and_live_handle(self):
        m=preparar_voz()
        m.unidades[7*276+1]=12
        m.palavra(7,8,0xf0f0)
        m.descoberto[0][0xf0f0]=0
        with self.assertRaises(DependenciaVozUnidade) as captura:
            solicitar_voz_unidade(m,7,0x1200,255,janela=(0,0,0,0))
        d=captura.exception
        self.assertEqual((d.endereco,d.checkpoint),(0x48aa79,0x440de7))
        self.assertEqual(asdict(d.solicitacao),dict(unidade=7,codigo=0x1e0000,flag=255,volume=0,
                                                  offset_handle=7*276+0x104,opcode=0x50))
        self.assertEqual(m.unidades[7*276+0xf9],255)
        self.assertEqual(struct.unpack_from('<I',m.unidades,7*276+0x104)[0],0xffffffff)

    def test_caller_live_owner_comparison_and_actual_supported_request_return(self):
        m=preparar_voz(handle=0)
        pedido=ColocacaoSaidaTropa(7,7,0x808,1,0x909)
        m.estruturas[7*276+4]=3
        antes=bytes(m.unidades)
        r=retomar_solicitacao_saida(m,pedido)
        self.assertEqual((r.endereco_dependencia,r.destino_ordem),(0x420fb7,0x909))
        self.assertEqual(bytes(m.unidades),antes)
        m.estruturas[7*276+4]=0
        r=retomar_solicitacao_saida(m,pedido,janela=(0,0,16,16))
        self.assertEqual((r.endereco_dependencia,m.unidades[7*276+0xf9]),(0x420fb7,0))

    def test_protected_inputs_and_wrong_handoff_preserve_records(self):
        m=preparar_voz(handle=0)
        antes=bytes(m.unidades)
        for indice,janela in ((800,(0,0,0,0)),(-1,(0,0,0,0)),(7,(0,0,0))):
            with self.assertRaises(ValueError):
                consultar_volume_unidade(m,indice,janela)
        with self.assertRaises(ValueError):
            retomar_solicitacao_saida(m,replace(ColocacaoSaidaTropa(7,7,0x808,1,0),endereco_dependencia=0x420fb7))
        self.assertEqual(bytes(m.unidades),antes)
