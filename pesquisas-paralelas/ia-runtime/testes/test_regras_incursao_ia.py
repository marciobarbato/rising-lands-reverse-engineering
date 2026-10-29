"""The raid task's iaSolver rule calls at counter 9000 against the native capture captura-regras-incursao-9000-ia.json.

Each captured rule call runs on a memory holding only the bytes the original read before writing them. Each
outside call must match the native arguments; it then returns the native exit EAX and applies the native net
writes. The rule's EAX and every byte it writes must equal the native values, and every native change must be
reproduced. Every native write is made either by the translation or by an outside call (whose written bytes the
capture records).
B_Superieur is Core's (``MaquinaTarefas``) and is checked through it.
"""
import json
from pathlib import Path
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
sys.path.insert(0, str(OWNED / 'testes'))
import ambiente_ia_runtime  # noqa: E402,F401
from regras_incursao_ia import REGRAS  # noqa: E402
from test_incursao_ia import MemoriaEsparsa, em_pilha  # noqa: E402

CAPTURA = json.loads((OWNED / 'evidencias/captura-regras-incursao-9000-ia.json').read_bytes())
POSTERIOR = json.loads((OWNED / 'evidencias/captura-regras-incursao-ia.json').read_bytes())
DO_VM = ('B_Superieur', 'B_Egalite', 'I_Soustraction')     # Core's MaquinaTarefas operations
H = lambda v: int(v, 16)  # noqa: E731
ARGUMENTOS = {'EnginEstVivant': dict(unidade=('EAX', 0xffff)), 'EnginGetCase': dict(unidade=('EAX', 0xffff)),
              'SetDeplaceEngin': dict(unidade=('EAX', 0xffff), destino=('EDX', 0xffff))}


def replay(memoria, chamadas, feitas):
    def provedor(nome):
        def chamar(sitio, **argumentos):
            esperado = chamadas[len(feitas)]
            feitas.append(nome)
            if esperado['routine'] != nome or H(esperado['caller_return']) != sitio + 5:
                raise AssertionError(f'{nome}@0x{sitio:x} vs {esperado["routine"]} {esperado["caller_return"]}')
            for arg, (registrador, mascara) in ARGUMENTOS[nome].items():
                if argumentos[arg] & mascara != H(esperado['entry'][registrador]) & mascara:
                    raise AssertionError(f'{nome}.{arg}')
            for a, _antes, depois in esperado['changed_bytes']:
                if not em_pilha(H(a)):
                    memoria._acesso(1, H(a), depois, propria=False)
            return H(esperado['exit']['EAX'])
        return chamar
    return {nome: provedor(nome) for nome in ARGUMENTOS}


class RaidRules9000(unittest.TestCase):
    def test_capture(self):
        self.assertFalse(CAPTURA['translation_executed'])
        self.assertEqual(CAPTURA['rules'], ['B_AttenteConflit', 'B_NewConflit', 'B_Superieur', 'B_TestGroupeVide',
                                            'I_DetermineTempsTrajet', 'V_DeplaceGroupe'])

    def test_each_rule_call(self):
        self.verificar(CAPTURA['rule_calls'])

    def test_later_rule_calls(self):
        """Counters 9500 (group position, re-post), 9700, 10200, 11100 (battle freed, group re-queued), 11101."""
        self.assertEqual(POSTERIOR['recorded_counters'], [9500, 9700, 10200, 11100, 11101])
        self.assertEqual(len(POSTERIOR['rule_calls']), 19)
        self.verificar(POSTERIOR['rule_calls'])

    def verificar(self, chamadas):
        for chamada in chamadas:
            nome = chamada['rule']
            with self.subTest(nome, contador=chamada['counter']):
                argumentos = [H(v) for v in chamada['arguments']]
                if nome in DO_VM:
                    from tarefas_ia import MaquinaTarefas
                    eax = MaquinaTarefas.executar_operacao(object.__new__(MaquinaTarefas), nome, argumentos, 0, 0)
                    self.assertEqual(eax, H(chamada['exit']['EAX']))
                    continue
                memoria = MemoriaEsparsa({H(a): v for a, v in chamada['read_before_write']})
                feitas = []
                eax = REGRAS[nome](memoria, replay(memoria, chamada['outside_calls'], feitas), argumentos,
                                   chamada['player'], chamada['task'])
                self.assertEqual(eax & 0xffffffff, H(chamada['exit']['EAX']))
                self.assertEqual(feitas, [c['routine'] for c in chamada['outside_calls']])
                escritos = {H(a): (antes, depois) for a, antes, depois in chamada['written_bytes']}
                for a in memoria.proprias:                   # every byte the rule writes, at its native value
                    self.assertIn(a, escritos, hex(a))
                    self.assertEqual(memoria.atuais[a], escritos[a][1], hex(a))
                for a, (antes, depois) in escritos.items():  # every native change is reproduced
                    if antes != depois:
                        self.assertEqual(memoria.atuais.get(a), depois, hex(a))
                fora = {H(a) for c in chamada['outside_calls'] for a, _x, _y in c['written_bytes']}
                sem_par = [hex(a) for a, (antes, depois) in escritos.items()   # unmatched same-value writes
                           if a not in memoria.proprias and a not in fora and antes == depois]
                self.assertEqual(sem_par, [], 'native same-value writes the translation does not make')


if __name__ == '__main__':
    unittest.main()
