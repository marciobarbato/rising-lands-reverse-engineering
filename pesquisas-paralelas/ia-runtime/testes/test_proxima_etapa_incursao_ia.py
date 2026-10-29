"""EnginNextEtape for the raid unit (counters 9000..9011, forced input) against captura-proxima-etapa-incursao-ia.json.

Each captured call runs ``proxima_etapa_unidade`` on a memory holding only the bytes the original read before
writing them. The outside calls (Economy's BonusGetValEngin, Core's GetBit, CalculFatigue, SetEnginCollision
and DeplaceEngin, PlayerGetType, Combat's EnginTrouveCible) must come in the native order with the native
arguments; they return the native EAX and apply the native net writes. Every byte the call changed must equal
the native value, and every byte the translation writes must be a native write.
"""
import json
from pathlib import Path
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
sys.path.insert(0, str(OWNED / 'testes'))
import ambiente_ia_runtime  # noqa: E402,F401
from test_incursao_ia import MemoriaEsparsa, em_pilha  # noqa: E402

CAPTURA = json.loads((OWNED / 'evidencias/captura-proxima-etapa-incursao-ia.json').read_bytes())
H = lambda v: int(v, 16)  # noqa: E731
ARGUMENTOS = {
    'BonusGetValEngin': dict(jogador=('EAX', 0xff), seletor=('EDX', 0xff), tipo=('EBX', 0xff),
                             ecx=('ECX', 0xffffffff)),          # call site 0x454565..0x45456e
    'GetBit': dict(valor=('EAX', 0xff), bit=('EDX', 0xff)),
    'CalculFatigue': dict(unidade=('EAX', 0xffff)),
    'SetEnginCollision': dict(unidade=('EAX', 0xffff), caso=('EDX', 0xffff)),
    'DeplaceEngin': dict(unidade=('EAX', 0xffff)),
    'PlayerGetType': dict(jogador=('EAX', 0xff)),
    'EnginTrouveCible': dict(unidade=('EAX', 0xffff))}


class RaidUnitNextStep(unittest.TestCase):
    def test_capture(self):
        self.assertEqual(CAPTURA['routine'], 'EnginNextEtape')
        self.assertEqual([c['counter'] for c in CAPTURA['rule_calls']], list(range(9000, 9012)))

    def test_each_call(self):
        from inventario_ia_runtime import OriginalImage
        from proxima_etapa_quadro import proxima_etapa_unidade, tabelas_imagem
        tabelas = tabelas_imagem(OriginalImage())
        for chamada in CAPTURA['rule_calls']:
            with self.subTest(contador=chamada['counter']):
                memoria = MemoriaEsparsa({H(a): v for a, v in chamada['read_before_write']})
                feitas, fora = [], chamada['outside_calls']

                def provedor(nome):
                    def chamar(sitio, **argumentos):
                        esperado = fora[len(feitas)]
                        feitas.append(nome)
                        self.assertEqual((esperado['routine'], H(esperado['caller_return'])), (nome, sitio + 5))
                        for arg, (registrador, mascara) in ARGUMENTOS[nome].items():
                            self.assertEqual(argumentos[arg] & mascara, H(esperado['entry'][registrador]) & mascara,
                                             f'{nome}.{arg}')
                        for a, _antes, depois in esperado['changed_bytes']:
                            if not em_pilha(H(a)):
                                memoria._acesso(1, H(a), depois, propria=False)
                        return H(esperado['exit']['EAX'])
                    return chamar
                proxima_etapa_unidade(memoria, {n: provedor(n) for n in ARGUMENTOS}, chamada['unit'], tabelas)
                self.assertEqual(feitas, [c['routine'] for c in fora])
                escritos = {H(a): depois for a, _antes, depois in chamada['written_bytes']}
                for a in memoria.proprias:
                    self.assertIn(a, escritos, hex(a))
                    self.assertEqual(memoria.atuais[a], escritos[a], hex(a))
                for a, antes, depois in chamada['changed_bytes']:
                    self.assertEqual(memoria.atuais.get(H(a)), depois, a)


if __name__ == '__main__':
    unittest.main()
