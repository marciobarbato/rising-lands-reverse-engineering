"""AvanceMonstre's raid frame (counter forced to 9000) against the native capture ``captura-incursao-ia.json``.

The translation runs on a memory that holds only the bytes the original read before writing them; any other
read fails. Each outside call must come in the original order with the original arguments. It then returns the
original's exit EAX and applies its net writes (stack scratch excluded). At the end, every byte the
translation itself wrote and every byte the whole call changed must equal the native values.
"""
import json
from pathlib import Path
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
import ambiente_ia_runtime  # noqa: E402,F401
from incursao_ia import avancar_monstros  # noqa: E402

CAPTURA = json.loads((OWNED / 'evidencias/captura-incursao-ia.json').read_bytes())
PILHA = (0x2000000, 0x2010000)
H = lambda v: int(v, 16)  # noqa: E731

# provider argument -> (entry register or stack word index, mask)
ARGUMENTOS = {
    'GetFreeCell': dict(celula=('EAX', 0xffff), tipo=('EDX', 0xffff)),
    'CreerEngin': dict(celula=('EAX', 0xffffffff), edx=('EDX', 0xffffffff), tipo=('EBX', 0xff),
                       jogador=('ECX', 0xffffffff)),
    'EnginSetPlayer': dict(unidade=('EAX', 0xffff), jogador=('EDX', 0xffffffff)),
    'PlaceEngin': dict(unidade=('EAX', 0xffff)),
    'ProjectileInit': dict(tipo=('EAX', 0xffffffff), origem=('EDX', 0xffffffff), alvo=('EBX', 0xffffffff),
                           modo=('ECX', 0xffffffff), pilha=(5, None)),
    'EnginGetCase': dict(unidade=('EAX', 0xffff)),
    'EnginGetType': dict(unidade=('EAX', 0xffff)),
    'GetRandCaseTypeBatPlayer': dict(jogador=('EAX', 0xff), tipo=('EDX', 0xffffffff)),
    'Chemin_Accessible': dict(origem=('EAX', 0xffff), destino=('EDX', 0xffff)),
    'iaProbPost': dict(jogador=('EAX', 0xffffffff), tipo=('EDX', 0xffffffff), ebx=('EBX', 0xffffffff),
                       ecx=('ECX', 0xffffffff), pilha=(4, None)),
    'PlayerGetType': dict(jogador=('EAX', 0xff)),
    'MissionGetNum': {}, 'Random': {}, 'GetRandCaseChamps': {}}


def em_pilha(a):
    return PILHA[0] <= a < PILHA[1]


class MemoriaEsparsa:
    def __init__(self, iniciais):
        self.iniciais, self.atuais, self.proprias = dict(iniciais), {}, set()
        self.fora_do_rastro = []

    def _ler(self, a):
        if a in self.atuais:
            return self.atuais[a]
        if a not in self.iniciais:
            self.fora_do_rastro.append(hex(a))
            raise KeyError(f'0x{a:x}: the original did not read this byte before writing it')
        return self.iniciais[a]

    def _acesso(self, largura, a, valor, propria=True):
        if valor is None:
            return int.from_bytes(bytes(self._ler(a + i) for i in range(largura)), 'little')
        valor &= (1 << 8 * largura) - 1
        for i in range(largura):
            self.atuais[a + i] = (valor >> 8 * i) & 0xff
            if propria:
                self.proprias.add(a + i)
        return valor

    def u8(self, a, v=None):
        return self._acesso(1, a, v)

    def u16(self, a, v=None):
        return self._acesso(2, a, v)

    def u32(self, a, v=None):
        return self._acesso(4, a, v)


def replay(memoria, chamadas, feitas):
    """Providers that check each call against the next native outside call and apply its native effect."""
    def provedor(nome):
        def chamar(sitio, **argumentos):
            esperado = chamadas[len(feitas)]
            feitas.append(nome)
            if esperado['routine'] != nome:
                raise AssertionError(f'call {len(feitas)}: Python {nome}, original {esperado["routine"]}')
            if H(esperado['caller_return']) != sitio + 5:
                raise AssertionError(f'{nome}: site 0x{sitio:x} vs caller return {esperado["caller_return"]}')
            for arg, (fonte, mascara) in ARGUMENTOS[nome].items():
                if isinstance(fonte, int):
                    original = tuple(H(w) for w in esperado['stack_words'][:fonte])
                    python = tuple(argumentos[arg])
                else:
                    original, python = H(esperado['entry'][fonte]) & mascara, argumentos[arg] & mascara
                if python != original:
                    raise AssertionError(f'{nome}.{arg}: Python {python} original {original}')
            for a, _antes, depois in esperado['changed_bytes']:
                if not em_pilha(H(a)):
                    memoria._acesso(1, H(a), depois, propria=False)
            return H(esperado['exit']['EAX'])
        return chamar
    return {nome: provedor(nome) for nome in ARGUMENTOS}


class RaidFrame(unittest.TestCase):
    def test_capture_reproduces_the_committed_path(self):
        self.assertTrue(CAPTURA['path_reproduction']['passed'])
        self.assertFalse(CAPTURA['translation_executed'])

    def test_avance_monstre_forced_9000(self):
        caso = next(c for r in CAPTURA['avance_monstre_cases'] for c in r['cases']
                    if c['case'] == 'forced-counter-9000')
        registro = CAPTURA['forced_outside_calls'][0]
        memoria = MemoriaEsparsa({H(a): v for a, v, _ in caso['read_before_write']})
        feitas = []
        avancar_monstros(memoria, replay(memoria, registro['outside_calls'], feitas))
        self.assertEqual(feitas, [c['routine'] for c in registro['outside_calls']])
        proprias = {H(a): depois for a, _antes, depois in registro['own_writes'] if not em_pilha(H(a))}
        self.assertEqual(sorted(memoria.proprias), sorted(proprias))       # the same bytes written
        for a, depois in proprias.items():
            self.assertEqual(memoria.atuais[a], depois, hex(a))
        mudados = {H(a): novo for a, _velho, novo in caso['changed_bytes'] if not em_pilha(H(a))}
        for a, novo in mudados.items():
            self.assertEqual(memoria.atuais.get(a), novo, hex(a))
        for a, v in memoria.atuais.items():                                  # nothing else changed
            if a not in mudados:
                antes = memoria.iniciais.get(a, next((x[1] for x in registro['own_writes'] if H(x[0]) == a), None))
                self.assertIsNotNone(antes, hex(a))
                self.assertEqual(v, antes, hex(a))


if __name__ == '__main__':
    unittest.main()
