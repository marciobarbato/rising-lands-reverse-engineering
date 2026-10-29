"""Static graph/provenance regressions; no emulator or game algorithm is implemented."""
import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from extrair_mapa_acoes_bytes import OriginalPE
from validar_mapa_acoes_jogador import check_graph, validate

OWNED=Path(__file__).resolve().parent
EXE=Path(os.environ.get('RISING_ACTIONS_EXE','/Users/marcio/git/Rising Lands/source/cd/INSTALHD/RISING.EXE'))


class PlayerActionStaticMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pe=OriginalPE(EXE)
        cls.graph=json.loads((OWNED/'callgraph.json').read_text())

    def test_real_graph_and_evidence_match_intact_bytes(self):
        result=validate(EXE)
        self.assertEqual(result['commands'],40)
        self.assertEqual(result['actions'],6)
        self.assertEqual(result['type_records_checked'],5)
        self.assertGreater(result['edges'],200)

    def test_executable_identity_is_strict(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'modified.exe';path.write_bytes(b'not the intact executable')
            with self.assertRaisesRegex(ValueError,'identity'):OriginalPE(path)

    def test_modified_edge_and_dangling_node_are_rejected(self):
        graph=copy.deepcopy(self.graph);graph['edges'][0]['bytes_hex']='e800000000'
        with self.assertRaises(ValueError):check_graph(graph,self.pe)
        graph=copy.deepcopy(self.graph);graph['edges'][0]['target']='invented'
        with self.assertRaisesRegex(ValueError,'Dangling'):check_graph(graph,self.pe)

    def test_wrong_command_order_or_table_target_is_rejected(self):
        graph=copy.deepcopy(self.graph);graph['command_dispatch']['cases'].reverse()
        with self.assertRaisesRegex(ValueError,'index/order'):check_graph(graph,self.pe)
        graph=copy.deepcopy(self.graph);graph['command_dispatch']['cases'][4]['branch']='0x0045efc1'
        with self.assertRaisesRegex(ValueError,'table target'):check_graph(graph,self.pe)

    def test_reachability_and_success_overclaims_are_rejected(self):
        graph=copy.deepcopy(self.graph);graph['actions'][0]['successful_MONDE01_effect']='accepted'
        with self.assertRaisesRegex(ValueError,'overclaims'):check_graph(graph,self.pe)
        graph=copy.deepcopy(self.graph);graph['nodes'][0]['runtime_reachability']='proven'
        with self.assertRaisesRegex(ValueError,'overclaims'):check_graph(graph,self.pe)

    def test_transition_target_and_packet_candidates_remain_byte_bound(self):
        graph=copy.deepcopy(self.graph);graph['end_of_mission']['branches'][0]['target']='0x0042c92d'
        with self.assertRaisesRegex(ValueError,'branch target'):check_graph(graph,self.pe)
        graph=copy.deepcopy(self.graph);graph['actions'][0]['producer_sites']=['0x00401000']
        with self.assertRaisesRegex(ValueError,'Producer'):check_graph(graph,self.pe)
