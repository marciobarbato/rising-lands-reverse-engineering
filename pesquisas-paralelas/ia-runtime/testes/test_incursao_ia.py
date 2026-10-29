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

    preenchimento = None   # cross-checks only: a filler for bytes another owner's translation reads beyond the footprint

    def _ler(self, a):
        if a in self.atuais:
            return self.atuais[a]
        if a not in self.iniciais and self.preenchimento is not None:
            self.fora_do_rastro.append(hex(a))
            return self.preenchimento
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

    def ler(self, a, n):
        return bytes(self._ler(a + i) for i in range(n))

    def vista(self, a, n):
        """Write-through view of n bytes (index or slice assignment), for helpers that write via ``vista``."""
        memoria = self

        class Vista:
            def __len__(self):
                return n

            def __getitem__(self, k):
                if isinstance(k, slice):
                    return bytes(memoria._ler(a + i) for i in range(n)[k])
                return memoria._ler(a + range(n)[k])

            def __setitem__(self, k, v):
                indices = range(n)[k] if isinstance(k, slice) else [range(n)[k]]
                valores = bytes(v) if isinstance(k, slice) else bytes([v])
                if len(valores) != len(indices):
                    raise ValueError('view assignment changes the size')
                for i, b in zip(indices, valores):
                    memoria._acesso(1, a + i, b)
        return Vista()

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


class RaidFrameWithCoreProviders(unittest.TestCase):
    """The same forced call, with Core's committed raid translations (``incursao_core``) answering every call
    they cover, and the native effect replayed only for the rest. Each call keeps its order and arguments.

    CreerEngin keeps its native effect here: it calls Economy's BonusGetValEngin inside, which this sparse memory
    cannot host. A Core translation that reads a byte beyond the original's footprint reads the filler 0xa5,
    and every byte the call changes must still equal the native value.
    """

    def test_core_translations_in_place(self):
        import incursao_core as ic
        caso = next(c for r in CAPTURA['avance_monstre_cases'] for c in r['cases']
                    if c['case'] == 'forced-counter-9000')
        registro = CAPTURA['forced_outside_calls'][0]
        memoria = MemoriaEsparsa({H(a): v for a, v, _ in caso['read_before_write']})
        feitas = []
        p = replay(memoria, registro['outside_calls'], feitas)
        core = {
            'EnginSetPlayer': lambda a: ic.definir_dono_unidade(memoria, a['unidade'], a['jogador'])['EAX'],
            'PlaceEngin': lambda a: ic.colocar_unidade(memoria, a['unidade'])['EAX'],
            'EnginGetCase': lambda a: ic.caso_unidade(memoria, a['unidade'])['EAX'],
            'GetRandCaseChamps': lambda a: ic.caso_campo_aleatoria(memoria)['EAX'],
            'Chemin_Accessible': lambda a: ic.acessivel(memoria, a['origem'], a['destino'])['EAX'],
            'iaProbPost': lambda a: ic.postar_tarefa(memoria, a['jogador'], a['tipo'], a['ebx'], a['ecx'],
                                                     a['pilha'])['EAX']}
        usados = []

        def com_core(nome, nativo):
            def chamar(sitio, **argumentos):
                esperado = registro['outside_calls'][len(feitas)]
                feitas.append(nome)
                self.assertEqual(esperado['routine'], nome)
                usados.append(nome)
                memoria.preenchimento = 0xa5
                try:
                    eax = core[nome](argumentos)
                finally:
                    memoria.preenchimento = None
                self.assertEqual(eax & 0xffff, H(esperado['exit']['EAX']) & 0xffff, nome)
                return eax
            return chamar
        for nome in core:
            p[nome] = com_core(nome, p[nome])
        avancar_monstros(memoria, p)
        self.assertEqual(feitas, [c['routine'] for c in registro['outside_calls']])
        self.assertEqual(sorted(set(usados)), sorted(core))
        mudados = {H(a): novo for a, _velho, novo in caso['changed_bytes'] if not em_pilha(H(a))}
        for a, novo in mudados.items():
            self.assertEqual(memoria.atuais.get(a), novo, hex(a))
        self.fora_do_rastro = sorted(set(memoria.fora_do_rastro))


class AmbushRepost(unittest.TestCase):
    """AvanceMonstre at counters 11100 and 11101 (captura-avance-monstre-emboscada-ia.json, routine mode).

    At 11101 the re-queued group is ordered to the ambush cell 0x320e (StockeAction 0x2e). In this capture this
    front's own iagUnitGetFirstUnitInGroup and StockeAction appear as outside calls; the translation runs them
    itself, so they are checked through the bytes of the whole call. iaProbPost (nested in StockeAction) is
    Core's ``incursao_core.postar_tarefa``; a byte it reads beyond the footprint reads the filler 0xa5.
    """

    def test_both_calls(self):
        import incursao_core as ic
        cap = json.loads((OWNED / 'evidencias/captura-avance-monstre-emboscada-ia.json').read_bytes())
        self.assertEqual([c['counter'] for c in cap['rule_calls']], [11100, 11101])
        proprias = {'iagUnitGetFirstUnitInGroup', 'StockeAction'}
        for chamada in cap['rule_calls']:
            with self.subTest(contador=chamada['counter']):
                memoria = MemoriaEsparsa({H(a): v for a, v in chamada['read_before_write']})
                fora = [c for c in chamada['outside_calls'] if c['routine'] not in proprias]
                feitas = []
                p = replay(memoria, fora, feitas)

                def postar(sitio, jogador, tipo, ebx, ecx, pilha):
                    memoria.preenchimento = 0xa5
                    try:
                        return ic.postar_tarefa(memoria, jogador, tipo, ebx, ecx, tuple(pilha))['EAX']
                    finally:
                        memoria.preenchimento = None
                p['iaProbPost'] = postar
                avancar_monstros(memoria, p)
                self.assertEqual(feitas, [c['routine'] for c in fora])
                escritos = {H(a): depois for a, _antes, depois in chamada['written_bytes']}
                for a in memoria.proprias:
                    self.assertIn(a, escritos, hex(a))
                    self.assertEqual(memoria.atuais[a], escritos[a], hex(a))
                for a, _antes, depois in chamada['changed_bytes']:
                    self.assertEqual(memoria.atuais.get(H(a)), depois, a)


if __name__ == '__main__':
    unittest.main()
