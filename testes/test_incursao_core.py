"""Raid-frame Core translations replayed without a CPU over the original-first capture."""
import json
from pathlib import Path
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
sys.path.insert(0, str(RAIZ / 'testes'))
CAPTURAS = sorted((RAIZ / 'evidencias/fundacoes-quadro').glob('captura-incursao-core-*.json'))
# GetCaseIndiceBatiment: MONDE01 has no cave. TerrainEnCollision, ResetCollision and memset run in the
# movement window after the spawn (captura-movimento-incursao, validar_movimento_incursao), not in it.
NAO_ALCANCADAS = {'GetCaseIndiceBatiment', 'TerrainEnCollision', 'ResetCollision', 'memset'}
REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')


def chamadas():
    from compactar_captura_isolada import expandir
    for caminho in CAPTURAS:
        for c in json.loads(caminho.read_bytes())['calls']:
            yield caminho.name, expandir(c)


def replay(chamada, classe_bonus):
    from test_chamadas_quadro_core import MemoriaEsparsa, bonus_de, regs
    conhecidos = {int(a, 16): v for a, v, _ in chamada['read_before_write']}
    m = MemoriaEsparsa(conhecidos, 0)
    entrada = regs(chamada['entry_registers'])
    pilha = [int(x, 16) for x in chamada['stack_words']]
    from incursao_core import traducao_core
    saida = traducao_core(chamada['routine'])(m, entrada, pilha, bonus_de(m, classe_bonus))
    return m, dict(entrada, **saida)


@unittest.skipUnless(CAPTURAS, 'No raid capture committed')
class IncursaoCore(unittest.TestCase):
    def test_every_translated_call_replays_exactly(self):
        from incursao_core import ROTINAS, traducao_core
        from integracao.providers import load_economy_bonus
        classe = load_economy_bonus().BonusUnidades
        vistos = {}
        for nome_captura, c in chamadas():
            if traducao_core(c['routine']) is None:
                raise AssertionError(f"{c['routine']} has no Core translation")
            with self.subTest(capture=nome_captura, case=c['case'], index=c['index'], routine=c['routine']):
                m, saida = replay(c, classe)
                nativo = {k: int(v, 16) for k, v in c['exit_registers'].items()}
                self.assertEqual({k: hex(saida[k]) for k in REGISTROS}, {k: hex(nativo[k]) for k in REGISTROS})
                m.conferir(self, c['changed_bytes'])
                vistos[c['routine']] = vistos.get(c['routine'], 0) + 1
        # MONDE01 has no cave (type-3 structure): the cave pick finds none and never reads a structure cell.
        self.assertEqual(set(ROTINAS) - set(vistos), NAO_ALCANCADAS)

    def test_unreached_minimap_mode_raises_at_its_handler(self):
        from chamadas_quadro_core import DependenciaRamoCore
        from incursao_core import definir_minimapa
        from test_chamadas_quadro_core import MemoriaEsparsa
        m = MemoriaEsparsa({a: 0x40 if a in (0x496fe0, 0x496fe2, 0x497168, 0x49716a) else 0
                            for a in range(0x496fe0, 0x496fe4)} | {a: 0x40 if a % 2 == 0 else 0
                                                                  for a in range(0x497168, 0x49716c)})
        with self.assertRaises(DependenciaRamoCore) as e:
            definir_minimapa(m, 1, 2, 0x0101)
        self.assertEqual(e.exception.endereco, 0x46a4d9)


if __name__ == '__main__':
    unittest.main()
