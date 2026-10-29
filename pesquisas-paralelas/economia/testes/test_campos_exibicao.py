"""Field growth, BagVide and edge-player queries against original captures over the display post-load state.

Both captures (``capturar_campos_exibicao_original``,
``capturar_consultas_bordas_exibicao_original``) were recorded before this
replay. Python regenerates each scenario's declared steps from the same
script over its own copy of the display post-load memory, binds the tile
grids through Core's ``MundoFisico.vincular_grades`` and builds
``RecursosTerreno.do_mundo`` over them (``mundo.tiles.buffer`` is the
field-growth tile bytes). After every call the
grids and scalars must equal the original's (a mirror memory replays the
native writes), and each scenario's whole-state hash must equal the native one.
``RISING_EMULAR=1`` reruns both captures natively and requires them to equal the frozen files.
"""
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest

PASTA = Path(__file__).resolve().parents[1]
RAIZ = PASTA.parents[1]
sys.path.insert(0, str(PASTA))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import capturar_campos_exibicao_original as campos  # noqa: E402
import capturar_consultas_bordas_exibicao_original as bordas  # noqa: E402
import quadro_economia as q  # noqa: E402
from test_quadro_economia import Memoria, Provedores  # noqa: E402
from test_quadro1_economia import MemoriaPalavras, base_cenario  # noqa: E402

CAPTURA = PASTA / 'evidencias/captura-campos-exibicao-original.json'
CAPTURA_BORDAS = PASTA / 'evidencias/captura-consultas-bordas-exibicao-original.json'
SHA_CAPTURA = '11569b7241c965437a8a38808db80e762ee4eb8ff27d4592b730113e2ee1cecb'
SHA_CAPTURA_BORDAS = '47333cc94189e45dbcac270e0a3c62ec90808f45fc5d703283fd9d4463b279cc'
RAPIDO = ('import importlib, os, sys; sys.path.insert(0, sys.argv[1]); '
          'importlib.import_module(sys.argv[2]).capturar(sys.argv[3]); sys.stdout.flush(); os._exit(0)')
ESCALARES = ((campos.CONTADOR, 4), (campos.PERIODO, 2), (campos.LINHA, 2), (campos.FLAG, 1),
             (campos.ALEATORIO, 4), (0x509954, 80))


def evidencia(caminho=CAPTURA):
    return json.loads(caminho.read_text())


class Roteiro:
    """The capture scripts' ``c``: they only reload (a no-op on a fresh copy) and read addresses."""
    def __init__(self, m):
        self.ler = m.ler

    def recarregar(self):
        pass


def regioes(m):
    p = m.ponteiro
    return ESCALARES + ((p(campos.TIPOS), 65536), (p(0x507dac), 65536), (p(campos.ATRIBUTOS), 65536),
                        (p(campos.MOSAICOS), 131072))


def recursos_vivos(m):
    """RecursosTerreno over Core's MundoFisico with every field-growth grid bound live (``vincular_grades``)."""
    sys.path.append(str(RAIZ / 'ferramentas'))
    from avanco_unidades import MundoFisico
    from extracao import RecursosTerreno
    p = m.ponteiro
    mundo = MundoFisico()
    mundo.vincular_grades(tiles=m.vista(p(campos.MOSAICOS), 131072), atributos=m.vista(p(campos.ATRIBUTOS), 65536),
                          objetos=m.vista(p(campos.TIPOS), 65536), donos_objetos=m.vista(p(0x507dac), 65536))
    r = RecursosTerreno.do_mundo(mundo, minas=m.vista(0x509954, 80))
    assert r.mosaicos is mundo.tiles.buffer and r.atributos is mundo.atributos
    assert r.terreno.tipos is mundo.objetos and r.terreno.quantidades is mundo.donos_objetos
    return r


def executar_direto(m, recursos, rotulo, regs):
    if rotulo == 'SetUpdateChamp' or rotulo.startswith('SetUpdateChamp:'):
        return q.agendar_campos(m, recursos)
    if rotulo == 'UpdateChamp':
        return q.atualizar_campos(m, recursos)
    if rotulo.startswith('BagVide:'):
        return q.bolsa_vazia(m, regs['EAX'])
    raise AssertionError(rotulo)


def executar_provedores(m, recursos, rotulo, regs):
    from bonus_unidades import BonusUnidades
    from provedores_economia_quadro import provedores_economia_quadro
    p = provedores_economia_quadro(MemoriaPalavras(m), bonus=BonusUnidades.da_memoria(m),
                                   producao=Provedores(m).producao, recursos=recursos)
    if rotulo == 'SetUpdateChamp' or rotulo.startswith('SetUpdateChamp:'):
        return p['SetUpdateChamp'](sitio=0)
    if rotulo == 'UpdateChamp':
        return p['UpdateChamp'](sitio=0)
    if rotulo.startswith('BagVide:'):
        return p['BagVide'](sitio=0, bolsa=regs['EAX'])
    raise AssertionError(rotulo)


def comparar(teste, executor):
    original = evidencia()
    base = base_cenario('campos')
    roteiro = campos.cenarios(Roteiro(Memoria(base)))
    teste.assertEqual([r[0] for r in roteiro], [c['name'] for c in original['captures']])
    total = 0
    for (nome, _, overrides, passos), obs in zip(roteiro, original['captures']):
        m, espelho = Memoria(base), Memoria(base)
        for a, dados in overrides:
            m.escrever(a, dados)
            espelho.escrever(a, dados)
        teste.assertEqual(m.sha(), obs['initial_state_sha256'], nome)
        recursos = recursos_vivos(m)
        faixas = regioes(m)
        chamadas = iter(obs['calls'])
        for passo in passos:
            if passo[0] in ('contador', 'escrever'):
                a, dados = (campos.CONTADOR, struct.pack('<I', passo[1])) if passo[0] == 'contador' else passo[1:]
                m.escrever(a, dados)
                espelho.escrever(a, dados)
                continue
            c = next(chamadas)
            teste.assertEqual((c['call'], int(c['entry'], 16), c['outcome']), (passo[1], passo[2], 'return'))
            regs = {k: int(v, 16) for k, v in c['regs_in'].items()}
            resultado = executor(m, recursos, c['call'], regs)
            for endereco, tamanho, valor in c['writes']:
                espelho.escrever(int(endereco, 16), valor.to_bytes(tamanho, 'little'))
            rotulo = f'{nome}/{c["call"]}/{total}'
            for a, n in faixas + tuple((int(e, 16), t) for e, t, _ in c['writes']):
                teste.assertEqual(m.ler(a, n), espelho.ler(a, n), f'{rotulo} at 0x{a:08x}')
            if c['call'].startswith('BagVide:'):
                teste.assertEqual(resultado, int(c['regs_out']['EAX'], 16), rotulo)
            total += 1
        teste.assertIsNone(next(chamadas, None))
        teste.assertEqual(espelho.sha(), obs['final_state_sha256'], nome)
        teste.assertEqual(m.sha(), obs['final_state_sha256'], nome)
    return total


def comparar_bordas(teste, forma):
    from economia import Economia
    from mercado import Mercado
    original = evidencia(CAPTURA_BORDAS)
    base = base_cenario('campos')
    roteiro = bordas.cenarios(Roteiro(Memoria(base)))
    teste.assertEqual([r[0] for r in roteiro], [c['name'] for c in original['captures']])
    total = 0
    for (nome, _, overrides, passos), obs in zip(roteiro, original['captures']):
        m = Memoria(base)
        for a, dados in overrides:
            m.escrever(a, dados)
        teste.assertEqual(m.sha(), obs['initial_state_sha256'], nome)
        prov = None
        if forma == 'provedores':
            from bonus_unidades import BonusUnidades
            from provedores_economia_quadro import provedores_economia_quadro
            prov = provedores_economia_quadro(MemoriaPalavras(m), bonus=BonusUnidades.da_memoria(m),
                                              producao=Provedores(m).producao)
        for passo, c in zip(passos, obs['calls']):
            teste.assertEqual((c['call'], c['outcome'], c['writes']), (passo[1], 'return', []))
            r = {k: int(v, 16) for k, v in c['regs_in'].items()}
            if c['call'].startswith('PlayerEstAllie:'):
                if forma == 'funcoes':
                    valor = q.aliado(m, r['EAX'], r['EDX'])
                elif forma == 'classe':
                    valor = Mercado.da_memoria(m).aliado(r['EAX'], r['EDX'])
                else:
                    valor = prov['PlayerEstAllie'](sitio=0, jogador=r['EAX'], outro=r['EDX'])
            else:
                jogador = int(c['stack_argument'], 16) & 0xff
                if forma == 'funcoes':
                    valor = q.recursos_suficientes(m, jogador, r['EAX'], r['EDX'], r['EBX'])
                elif forma == 'classe':
                    valor = int(Economia.da_memoria(m).suficiente(jogador, r['EAX'], r['EDX'], r['EBX']))
                else:
                    valor = prov['TestRessource'](sitio=0, jogador=jogador, comida=r['EAX'], pedra=r['EDX'],
                                                  pecas=r['EBX'])
            teste.assertEqual(valor, int(c['regs_out']['EAX'], 16) & 0xff, f'{nome}/{c["call"]}')
            total += 1
        teste.assertEqual(m.sha(), obs['final_state_sha256'], nome)
    return total


class ContratosCamposExibicao(unittest.TestCase):
    def test_frozen_captures_precede_translation(self):
        for caminho, sha in ((CAPTURA, SHA_CAPTURA), (CAPTURA_BORDAS, SHA_CAPTURA_BORDAS)):
            r = evidencia(caminho)
            self.assertFalse(r['translation_executed'])
            self.assertEqual(r['returns'], r['original_entries'])
            self.assertIn('NOT a frame input', r['input']['label'])
            self.assertEqual(hashlib.sha256(caminho.read_bytes()).hexdigest(), sha)

    def test_monde01_natural_pass_timeline(self):
        """Frames (counter values) where the isolated natural pass calls Random and changes the type grid.

        Random runs only on field (0x1d..0x34) and bush (0x1c) cells, so the Random frames follow from the
        map: rows 32..41, 45..47 and 55..62 (frame k processes row k + 1). Which cells grow or plant depends
        on the shared RNG 0x497164, which other frame code also draws in a real game; those frames hold
        for this isolated sequence only.
        """
        r = evidencia()
        tipos = Memoria(base_cenario('campos')).ponteiro(campos.TIPOS)
        for nome, inicio in (('pass_from_0', 0), ('pass_from_128', 128)):
            passe = next(c for c in r['captures'] if c['name'] == nome)
            aleatorio, crescimento = [], []
            for k, c in enumerate(c for c in passe['calls'] if c['call'] == 'UpdateChamp'):
                enderecos = [int(e, 16) for e, _, _ in c['writes']]
                if campos.ALEATORIO in enderecos:
                    aleatorio.append(inicio + k)
                crescimento += [(inicio + k, (e - tipos) // 256) for e in enderecos if tipos <= e < tipos + 65536]
            self.assertEqual(aleatorio, [inicio + k for k in (*range(31, 41), 44, 45, 46, *range(54, 62))], nome)
            # (frame, type-grid row written): a plant may land in a neighbouring row of the one processed.
            self.assertEqual(crescimento, [(inicio + k, linha) for k, linha in
                                           ((32, 33), (35, 36), (35, 36), (46, 47), (46, 47), (56, 56), (59, 60))],
                             nome)

    def test_python_reproduces_field_growth_and_bagvide(self):
        self.assertEqual(comparar(self, executar_direto), evidencia()['original_entries'])

    def test_providers_over_word_memory_reproduce_field_growth_and_bagvide(self):
        self.assertEqual(comparar(self, executar_provedores), evidencia()['original_entries'])

    def test_live_functions_reproduce_edge_players(self):
        self.assertEqual(comparar_bordas(self, 'funcoes'), evidencia(CAPTURA_BORDAS)['original_entries'])

    def test_live_bound_class_forms_reproduce_edge_players(self):
        self.assertEqual(comparar_bordas(self, 'classe'), evidencia(CAPTURA_BORDAS)['original_entries'])

    def test_providers_reproduce_edge_players(self):
        self.assertEqual(comparar_bordas(self, 'provedores'), evidencia(CAPTURA_BORDAS)['original_entries'])


@unittest.skipUnless(os.environ.get('RISING_EMULAR'), 'set RISING_EMULAR=1 to rerun the original captures')
class DiferencialCamposExibicao(unittest.TestCase):
    execucoes = 0

    def _fresca(self, script, frozen):
        with tempfile.TemporaryDirectory(dir=RAIZ / '.local') as pasta:
            saida = Path(pasta) / 'captura.json'
            # Exit right after the capture is written: Unicorn's uc_close teardown of the ~25k display
            # blocks can spin for over an hour in interpreter finalization (round 5, lease journal -15).
            subprocess.run([sys.executable, '-B', '-c', RAPIDO, str(PASTA), script[:-3], str(saida)], check=True,
                           cwd=RAIZ, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
            fresca = json.loads(saida.read_text())
        self.assertEqual(fresca['captures'], evidencia(frozen)['captures'])
        type(self).execucoes += fresca['original_entries']

    def test_fresh_field_capture_equals_frozen(self):
        self._fresca('capturar_campos_exibicao_original.py', CAPTURA)

    def test_fresh_edge_query_capture_equals_frozen(self):
        self._fresca('capturar_consultas_bordas_exibicao_original.py', CAPTURA_BORDAS)


if __name__ == '__main__':
    unittest.main()
