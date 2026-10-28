"""Whole-image original capture replay and retained lifecycle boundaries."""
import json
from pathlib import Path
import unittest

from modelo_capturas_conclusao_remapeamento import conferir_captura, RecursosConclusao
from cenarios_conclusao_remapeamento import preparar_conclusao
from remapeamento_mundo import iniciar_remapeamento
from classificacao_remapeamento import retomar_classificacao_remapeamento
from conclusao_remapeamento import (retomar_conclusao_remapeamento, DependenciaConclusaoRemapeamento,
                                    EstadoConclusaoRemapeamento)

RAIZ = Path(__file__).resolve().parents[1]


class ConclusaoRemapeamento(unittest.TestCase):
    def test_seven_original_first_whole_images_ordered_writes_resources_and_returns(self):
        for nome in ('stage17-original-MONDE01.json', 'stage17-original-discriminating.json'):
            d = json.loads((RAIZ/'relatorios'/nome).read_text())
            self.assertFalse(d['translation_executed'])
            for c in d['cases']:
                with self.subTest(case=c['name']): conferir_captura(c)

    def preparar(self):
        m, _ = preparar_conclusao('uniform_zero_edge');r = RecursosConclusao('uniform_zero_edge')
        p = retomar_classificacao_remapeamento(m, iniciar_remapeamento(m), alocar=r.alocar, fixar=r.fixar)
        return m,r,p

    def test_missing_allocation_retains_resumable_state_without_repeating_reset(self):
        m,r,p = self.preparar()
        with self.assertRaises(DependenciaConclusaoRemapeamento) as erro: retomar_conclusao_remapeamento(m,p)
        e = erro.exception
        self.assertEqual((e.checkpoint,e.importacao,e.argumentos),(0x42efba,0x5231c0,(0,0x100000)))
        self.assertEqual((e.estado.fase,e.estado.componentes),('allocate',1))
        self.assertTrue(retomar_conclusao_remapeamento(m,e.estado,**r.callbacks()))
        self.assertEqual(r.componentes,1)

    def test_cleanup_missing_provider_keeps_labels_stack_and_live_allocation_then_resumes(self):
        m,r,p = self.preparar();callbacks=r.callbacks();callbacks['desfixar']=None
        with self.assertRaises(DependenciaConclusaoRemapeamento) as erro:
            retomar_conclusao_remapeamento(m,p,**callbacks)
        e=erro.exception
        self.assertEqual((e.checkpoint,e.estado.fase),(0x42ef56,'unlock_stack'))
        self.assertEqual(set(m.regioes),{1})
        self.assertTrue(r.recursos[0x1920000]['active'])
        self.assertTrue(retomar_conclusao_remapeamento(m,e.estado,**r.callbacks()))
        self.assertEqual(set(m.regioes),{0,1})
        self.assertFalse(any(x['active'] for x in r.recursos.values()))

    def test_count_threshold_uses_low_u16_after_class_cleanup_and_completed_resume_is_inert(self):
        for compte, attendu in ((0x3fff,True),(0x4000,False),(0xffff,False),(0x10000,True)):
            m,r,p=self.preparar();e=EstadoConclusaoRemapeamento(p,fase='handle_class_unlock',componentes=compte)
            self.assertIs(retomar_conclusao_remapeamento(m,e,**r.callbacks()),attendu)
            events=r.eventos[:]
            self.assertIs(retomar_conclusao_remapeamento(m,e,**r.callbacks()),attendu)
            self.assertEqual(r.eventos,events)
            self.assertFalse(r.recursos[0x1900000]['active'])

    def test_invalid_regions_or_dimensions_precede_resource_or_world_writes(self):
        for caso in ('regions','width','attributes'):
            m,r,p=self.preparar();events=r.eventos[:]
            if caso=='regions':m.regioes.pop()
            if caso=='width':m.largura=65536
            if caso=='attributes':m.atributos=bytes(m.atributos)
            with self.assertRaises(ValueError):retomar_conclusao_remapeamento(m,p,**r.callbacks())
            self.assertEqual(r.eventos,events)
