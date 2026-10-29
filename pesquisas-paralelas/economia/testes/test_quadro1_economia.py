"""Economy frame calls at the exact MONDE01 frame-0/1 inputs against isolated original captures.

Each frozen case was captured natively from the exact entry state of the
first-frame path (Missions' frame bench, ``capturar_quadro1_economia_original``).
Python starts from the M1 post-load memory overlaid with every byte the call
read before writing and every changed byte's entry value, runs the
translation, and must produce exactly the native set of changed bytes and the
native result register. For routines that read only through ``ler`` and
write only through ``vista``, the bytes read before written must equal the
native set exactly.
``RISING_EMULAR=1`` reruns the native capture and requires it to equal the frozen file.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PASTA = Path(__file__).resolve().parents[1]
RAIZ = PASTA.parents[1]
sys.path.insert(0, str(PASTA))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import quadro_economia as q  # noqa: E402
from test_quadro_economia import Memoria, Provedores  # noqa: E402

CAPTURA = PASTA / 'evidencias/captura-quadro1-economia-original-v2.json'
CAPTURA_V1 = PASTA / 'evidencias/captura-quadro1-economia-original.json'
SO_VISTA = {'RechercheCalcul', 'PlayerInitAllianceCompteur', 'CalculMatiere', 'CalculCompteurMarche',
            'CalculCompteurProposition', 'PlayerAttaqueCalculSympa', 'MAJSympathie', 'ResetTableauHangar',
            'EnginNextEtape:state7'}


def evidencia():
    return json.loads(CAPTURA.read_text())


def executar(nome, m, p, regs):
    """Run the translation for one isolated case; return the value comparable to native EAX, or None."""
    from bonus_unidades import BonusUnidades
    from construcoes_habitaveis import celula_central_estrutura
    from limpeza_saida import bag_contient_troupe
    if nome == 'RechercheCalcul':
        q.calcular_pesquisa(m)
    elif nome == 'PlayerInitAllianceCompteur':
        q.contar_aliancas(m)
    elif nome == 'SetUpdateChamp':
        q.agendar_campos(m, p.recursos)
    elif nome == 'UpdateChamp':
        q.atualizar_campos(m, p.recursos)
    elif nome == 'CalculMatiere':
        q.calcular_materia(m)
    elif nome == 'CalculCompteurMarche':
        q.calcular_contador_mercado(m, regs['EAX'])
    elif nome == 'CalculCompteurProposition':
        q.calcular_contador_proposicao(m, regs['EAX'], regs['EDX'])
    elif nome == 'PlayerAttaqueCalculSympa':
        q.calcular_simpatia_ataques(m)
    elif nome == 'MAJSympathie':
        q.atualizar_simpatia(m, regs['EAX'], regs['EDX'], regs['EBX'])
    elif nome == 'ResetTableauHangar':
        q.resetar_tabela_hangar(m)
    elif nome == 'EnginNextEtape:state7':
        q.estado_parado_unidade(m, regs['EDI'])
    elif nome == 'BatimentNextEtape:type1_2_13_16':
        q.ramo_producao_estrutura(p.producao, regs['EDI'], p.calcular_tropa)
    elif nome == 'CalculTroupe':
        p.producao.calcular_tropa(regs['EAX'])
    elif nome == 'BonusGetValEngin':
        b = BonusUnidades.da_memoria(m)
        return 0xffff, b.consultar(regs['EAX'], regs['EBX'], regs['EDX'], ecx=regs['ECX'])
    elif nome == 'BagContientTroupe':
        indice, resto = divmod(regs['EAX'] - 0x49a0d4, 276)
        assert resto == 0
        return 0xff, int(bag_contient_troupe(p.producao.recrutamento, indice))
    elif nome == 'BatimentGetCase':
        return 0xffff, celula_central_estrutura(m.vista(0x49a0c8, 276000), regs['EAX'])
    else:
        raise AssertionError(f'No translation mapped for {nome}')
    return None


class MemoriaPalavras:
    """Only u8/u16/u32(endereco, valor=None), like ai-runtime's MemoriaDeclarada."""
    def __init__(self, m):
        self.m = m

    def _acesso(self, largura, endereco, valor):
        v = self.m.vista(endereco, largura)
        if valor is None:
            return int.from_bytes(v, 'little')
        v[:] = (valor & ((1 << 8 * largura) - 1)).to_bytes(largura, 'little')
        return valor

    def u8(self, endereco, valor=None):
        return self._acesso(1, endereco, valor)

    def u16(self, endereco, valor=None):
        return self._acesso(2, endereco, valor)

    def u32(self, endereco, valor=None):
        return self._acesso(4, endereco, valor)


def via_provedores(nome, m, p, regs):
    """The same case through provedores_economia_quadro over a u8-only memory."""
    from bonus_unidades import BonusUnidades
    from provedores_economia_quadro import provedores_economia_quadro
    prov = provedores_economia_quadro(MemoriaPalavras(m), bonus=BonusUnidades.da_memoria(m), producao=p.producao,
                                      recursos=p.recursos, calcular_tropa=p.calcular_tropa)
    chamadas = {
        'EnginNextEtape:state7': ('EnginNextEtape:estado7', dict(unidade=regs['EDI']), None),
        'BatimentNextEtape:type1_2_13_16': ('BatimentNextEtape:tipo1_2_13_16', dict(estrutura=regs['EDI']), None),
        'BagContientTroupe': (nome, dict(bolsa=regs['EAX']), 0xff),
        'CalculTroupe': (nome, dict(estrutura=regs['EAX']), None),
        'BatimentGetCase': (nome, dict(estrutura=regs['EAX']), 0xffff),
        'BonusGetValEngin': (nome, dict(jogador=regs['EAX'], tipo=regs['EBX'], seletor=regs['EDX'], ecx=regs['ECX']),
                             0xffff),
        'MAJSympathie': (nome, dict(jogador=regs['EAX'], outro=regs['EDX'], evento=regs['EBX']), None),
        'CalculCompteurMarche': (nome, dict(jogador=regs['EAX']), None),
        'CalculCompteurProposition': (nome, dict(jogador=regs['EAX'], edx=regs['EDX']), None),
    }
    rotina, argumentos, mascara = chamadas.get(nome, (nome, {}, None))
    resultado = prov[rotina](sitio=0, **argumentos)
    return None if mascara is None else (mascara, resultado)


def comparar(teste, executor=None):
    executor = executor or executar
    total = 0
    for r in evidencia()['calls']:
        nome = r['routine']
        rotulo = f"{r['phase']}:{nome}:{total}"
        m = Memoria()
        conhecidos = set()
        for a, v, _ in r['read_before_write']:
            teste.assertIsNotNone(v, rotulo)
            m.escrever(int(a, 16), bytes([v]))
            conhecidos.add(int(a, 16))
        for a, velho, _ in r['changed_bytes']:
            m.escrever(int(a, 16), bytes([velho]))
            conhecidos.add(int(a, 16))
        for a, valor in r['written_unchanged']:
            m.escrever(int(a, 16), bytes([valor]))
        p = Provedores(m)
        antes = [bytes(raw) for _, _, raw in m.blocos]
        regs = {k: int(v, 16) for k, v in r['entry_registers'].items()}
        m.leituras.clear()
        m.ordem_acessos.clear()
        resultado = executor(nome, m, p, regs)
        mudados = {}
        for (_, base, raw), velho in zip(m.blocos, antes):
            if raw != velho:
                mudados.update({base + i: raw[i] for i in range(len(raw)) if raw[i] != velho[i]})
        teste.assertEqual(mudados, {int(a, 16): novo for a, _, novo in r['changed_bytes']}, rotulo)
        if resultado is not None:
            mascara, valor = resultado
            teste.assertEqual(valor & mascara, int(r['exit_registers']['EAX'], 16) & mascara, rotulo)
        if nome in SO_VISTA and executor is executar:
            # These routines read only through ler and write only through vista: their bytes read
            # before written must be exactly the native ones.
            lidos, escritos = set(), set()
            for tipo, e, n in m.ordem_acessos:
                faixa = set(range(e, e + n))
                if tipo == 'ler':
                    lidos |= faixa - escritos
                else:
                    escritos |= faixa
            teste.assertEqual(lidos, {int(a, 16) for a, _, _ in r['read_before_write']}, rotulo)
        if nome == 'BatimentNextEtape:type1_2_13_16':
            teste.assertEqual(p.tropas, [regs['EDI'] & 0xffff], rotulo)
        total += 1
    return total


class ContratosQuadro1Economia(unittest.TestCase):
    def test_frozen_capture_precedes_translation_and_reproduces_the_frame_path(self):
        r = evidencia()
        self.assertFalse(r['translation_executed'])
        self.assertTrue(r['path_reproduction']['passed'])
        self.assertTrue(all(c['reached_exit'] for c in r['calls']))
        frame = RAIZ / r['frame_capture']['path']
        self.assertEqual(hashlib.sha256(frame.read_bytes()).hexdigest(), r['frame_capture']['sha256'])
        self.assertEqual(len(r['calls']), 102)
        self.assertEqual(hashlib.sha256(CAPTURA.read_bytes()).hexdigest(), SHA_CAPTURA)
        v1 = json.loads(CAPTURA_V1.read_text())['calls']
        self.assertEqual([{k: v for k, v in c.items() if k != 'written_unchanged'} for c in r['calls']], v1)

    def test_python_reproduces_every_exact_frame_call(self):
        self.assertEqual(comparar(self), 102)

    def test_providers_over_word_memory_reproduce_every_exact_frame_call(self):
        self.assertEqual(comparar(self, via_provedores), 102)

    def test_providers_cover_every_validated_routine(self):
        from provedores_economia_quadro import provedores_economia_quadro
        from bonus_unidades import BonusUnidades
        m = Memoria()
        p = Provedores(m)
        nomes = set(provedores_economia_quadro(m, bonus=BonusUnidades.da_memoria(m), producao=p.producao,
                                               recursos=p.recursos))
        renomeados = {'EnginNextEtape:state7': 'EnginNextEtape:estado7',
                      'BatimentNextEtape:type1_2_13_16': 'BatimentNextEtape:tipo1_2_13_16'}
        capturados = {renomeados.get(c['routine'], c['routine']) for c in evidencia()['calls']}
        self.assertEqual(nomes - capturados, {'RechercheGetNbInvention'})
        self.assertEqual(capturados - nomes, set())


SHA_CAPTURA = '747bca33fd2d5c5b2e6f20cc01ec65ab9e0949f725e54717fab29a70ef25b42b'


@unittest.skipUnless(os.environ.get('RISING_EMULAR'), 'set RISING_EMULAR=1 to rerun the original frame capture')
class DiferencialQuadro1Economia(unittest.TestCase):
    execucoes = 0

    def test_fresh_isolated_capture_equals_frozen(self):
        with tempfile.TemporaryDirectory(dir=RAIZ / '.local') as pasta:
            saida = Path(pasta) / 'captura.json'
            subprocess.run([sys.executable, '-B', str(PASTA / 'capturar_quadro1_economia_original.py'),
                            '--saida', str(saida.relative_to(RAIZ))], check=True, cwd=RAIZ,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
            fresca = json.loads(saida.read_text())
        frozen = evidencia()
        self.assertTrue(fresca['path_reproduction']['passed'])
        self.assertEqual(fresca['calls'], frozen['calls'])
        type(self).execucoes += len(fresca['calls'])


if __name__ == '__main__':
    unittest.main()
