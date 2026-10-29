"""M2.3 part manifests: pins and the hash chain between parts (partes_quadros_ia.verificar), with tiny fake parts."""
import hashlib
import json
import lzma
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
import ambiente_ia_runtime  # noqa: E402,F401
import partes_quadros_ia as pq  # noqa: E402

POLITICA = 'pesquisas-paralelas/missoes/validacao/m2-2-politica-comparacao-128-quadros.json'


class Cadeia(unittest.TestCase):
    def setUp(self):
        self.pasta = Path(tempfile.mkdtemp(dir=pq.ROOT / '.local' if (pq.ROOT / '.local').is_dir() else None))
        self.addCleanup(shutil.rmtree, self.pasta)
        self.politica = dict(path=POLITICA, sha256=hashlib.sha256((pq.ROOT / POLITICA).read_bytes()).hexdigest())

    def escrever(self, partes):
        registros = []
        anterior = None
        for i, parte in enumerate(partes):
            parte = dict(parte, policy=self.politica, previous_part_raw_sha256=anterior)
            bruto = json.dumps(parte).encode()
            caminho = self.pasta / f'p{i}.json.xz'
            caminho.write_bytes(lzma.compress(bruto))
            anterior = hashlib.sha256(bruto).hexdigest()
            registros.append(dict(part=i, artifact=str(caminho.relative_to(pq.ROOT)), raw_sha256=anterior,
                                  compressed_sha256=hashlib.sha256(caminho.read_bytes()).hexdigest()))
        manifesto = self.pasta / 'm.json'
        manifesto.write_text(json.dumps(dict(parts=registros, policy=self.politica)))
        return manifesto

    def partes(self, abertura_1='h2'):
        h = lambda x: dict(summary=x, compared_summary=x + 'c', masked_sha256=x + 'm')  # noqa: E731
        return [dict(frames=[0, 1], opening_state=h('h0'), phases=[dict(phase='load_tail', state_after=h('h1')),
                                                                    dict(phase='frame1', state_after=h('h2'))]),
                dict(frames=[2, 2], opening_state=h(abertura_1), phases=[dict(phase='between_frames2',
                                                                             state_after=h('h3'))])]

    def test_chain_checked_from_hashes(self):
        v = pq.verificar(self.escrever(self.partes()))
        self.assertEqual([p['first_phase'] for p in v['parts']], ['load_tail', 'between_frames2'])

    def test_broken_chain_is_refused(self):
        with self.assertRaises(SystemExit):
            pq.verificar(self.escrever(self.partes(abertura_1='outro')))


if __name__ == '__main__':
    unittest.main()
