"""Independent native captures, live physical primitives and exit handoff."""
import hashlib
import json
from pathlib import Path
import struct
import unittest

from capturar_colocacao_saida import preparar_saida
from navegacao_unidades import MundoNavegacao
from experiencia_unidades import ExperienciaSaidaTropa
from colocacao_saida import colocar_unidade_saida, retomar_colocacao_saida, DependenciaColocacaoSaida


class MundoRastreado(MundoNavegacao):
    def __init__(self, *args):
        self.efeitos = []
        super().__init__(*args)

    def ocupar(self, indice, celula, inserir):
        self.efeitos.append(('collision' if inserir else 'remove', indice, celula))
        return super().ocupar(indice, celula, inserir)

    def descobrir_area(self, celula, raio, dono):
        self.efeitos.append(('discovery', celula, raio, dono))
        return super().descobrir_area(celula, raio, dono)

    def iluminar_area(self, celula, raio, dono):
        self.efeitos.append(('light', celula, raio, dono))
        return super().iluminar_area(celula, raio, dono)

    def minimapa(self, dono, celula, modo):
        self.efeitos.append(('minimap', dono, celula, modo))
        return super().minimapa(dono, celula, modo)

    def definir_movimento(self, indice, destino):
        self.efeitos.append(('move', indice, destino))
        return super().definir_movimento(indice, destino)


def preparar(*args, **kwargs):
    m = preparar_saida(*args, classe=MundoRastreado, **kwargs)
    m.efeitos = []
    return m


def resumo_python(m, indice):
    hashes = {}
    for nome in ('atributos','regioes','tiles','mini_final','mini_unidades','mini_estruturas',
                 'descoberto','luz_bordas','contagem_luz'):
        valor = getattr(m, nome)
        if nome in ('regioes','tiles'):
            dados = struct.pack('<65536H', *valor)
        elif nome in ('descoberto','luz_bordas','contagem_luz'):
            dados = b''.join(bytes(g) for g in valor)
        else:
            dados = bytes(valor)
        hashes[nome] = hashlib.sha256(dados).hexdigest()
    return dict(unit_hex=m.ler_unidade(indice).hex(),
                full_unit_pool_sha256=hashlib.sha256(m.unidades).hexdigest(),physical_sha256=hashes,
                native_effect_trace=[list(e) for e in m.efeitos])


class ColocacaoSaida(unittest.TestCase):
    def test_four_independent_original_captures_full_buffers_and_effect_order(self):
        p = Path(__file__).resolve().parents[1]/'relatorios/capturas-colocacao-saida-original.json'
        for caso in json.loads(p.read_text())['cases']:
            a = caso['input']
            m = preparar(a['tipo'], a['dono'], indice=a['indice'])
            colocar_unidade_saida(m, a['indice'], a['celula'])
            self.assertEqual(resumo_python(m, a['indice']), caso['output'])

    def test_old_occupancy_life_phase_and_completion_are_preserved(self):
        m = preparar()
        antes = m.ler_unidade(7)
        m.colocar_unidade_saida(0xabcd0007, 0x12340808)
        self.assertEqual((m.atributos[0x505], m.atributos[0x506], m.atributos[0x808]), (1, 1, 1))
        self.assertEqual((m.busca.unidade, m.busca.ocupada, m.busca.sucesso,
                          m.busca.ponteiro_rota, m.busca.concluida), (65535,0,0,0,77))
        self.assertEqual(m.ler_unidade(7)[0x9a:0x9c], antes[0x9a:0x9c])
        self.assertEqual(m.ler_unidade(7)[0x8a:0x8c], antes[0x8a:0x8c])

    def test_inactive_still_inserts_collision_and_visits_minimap(self):
        for estado in (0, 4):
            m = preparar(dono=200, estado=estado, raio=255, extra=255)
            colocar_unidade_saida(m, 7, 0x808)
            self.assertEqual((m.unidades[7*276+2], m.unidades[7*276+0x72]), (estado,1))
            self.assertEqual(m.efeitos, [('collision',7,0x808),('minimap',200,0x808,4)])

    def test_large_vision_stops_after_record_collision_and_enabled_flag(self):
        m = preparar(raio=9)
        descoberto = bytes(m.descoberto[0])
        with self.assertRaises(DependenciaColocacaoSaida) as captura:
            colocar_unidade_saida(m, 7, 0x808)
        self.assertEqual((captura.exception.endereco,captura.exception.checkpoint), (0x476851,0x446146))
        self.assertEqual((m.unidades[7*276+2],m.unidades[7*276+0x72]), (7,1))
        self.assertEqual(m.efeitos, [('collision',7,0x808)])
        self.assertEqual(bytes(m.descoberto[0]), descoberto)

    def test_continuation_uses_original_movement_provider_and_live_building_destination(self):
        for objeto, estado in ((0,2),(0x36,5)):
            m = preparar(tipo=6)
            struct.pack_into('<H',m.estruturas,7*276+0x7c,0x909)
            m.objetos[0x909] = objeto
            r = retomar_colocacao_saida(m, ExperienciaSaidaTropa(7,7,0x808,25))
            self.assertEqual((r.destino_ordem,r.endereco_dependencia,m.unidades[7*276+2]), (0x909,0x420f9e,estado))
            self.assertEqual(m.palavra(7,8),0x808)
            self.assertEqual(m.efeitos[-1], ('move',7,0x909))

    def test_protected_inputs_and_wrong_checkpoint_precede_mutation(self):
        m = preparar()
        antes = bytes(m.unidades)
        for indice,celula in ((800,0x808),(-1,0x808),(7,0x1010)):
            with self.assertRaises(ValueError):
                colocar_unidade_saida(m,indice,celula)
        with self.assertRaises(ValueError):
            retomar_colocacao_saida(m,ExperienciaSaidaTropa(1000,7,0x808,1))
        m.tamanho_minimapa = (64,64)
        with self.assertRaises(ValueError):
            colocar_unidade_saida(m,7,0x808)
        self.assertEqual(bytes(m.unidades),antes)
        self.assertEqual(m.efeitos,[])
