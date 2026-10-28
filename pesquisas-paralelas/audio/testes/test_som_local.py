"""Python audio reconstruction against committed original-only captures (no Unicorn)."""
import hashlib
import json
from pathlib import Path
import struct
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
from ambiente_audio import CD, IDENTIDADES, LETRAS_BANCO, ORIGINAL_SHA256, ler_original
from adpcm_som import (INDICE_IMA, PASSO_IMA, criar_superficie_som, decodificar_ima_estereo16,
                       decodificar_ima_mono16)
from bancos_som import (BancoSom, DependenciaSom, GlobaisSom, arquivo_som, criar_caminho_sons,
                        criar_id_som)
from catalogo_som import DESTINO, construir, variantes_alcancaveis
import reproduzir_som
from cenarios_som import ARENA, ARENA_TAMANHO
from provedores_som import SistemaFixo

CONTADORES = ('instructions', 'segments', 'instructions_file', 'segments_file', 'instructions_memory',
              'segments_memory', 'file_seconds', 'original_sha256', 'created_before_translation', 'fixture')


def carregar(nome):
    return json.loads((OWNED / 'evidencias' / nome).read_text())


def limpar(valor):
    if isinstance(valor, dict):
        return {k: limpar(v) for k, v in valor.items() if k not in CONTADORES}
    if isinstance(valor, list):
        return [limpar(v) for v in valor]
    return valor


def normalizar(valor):
    return limpar(json.loads(json.dumps(valor)))


def globais():
    return GlobaisSom(nome_arquivo=bytearray(104), diretorio=bytearray(256), contador_variantes=0,
                      contador_alocacoes=0, janela=0, comprimido=0, directsound=1)


class Evidencia(unittest.TestCase):
    def test_exported_intervals_match_intact_executable(self):
        manifesto = carregar('som-manifesto.json')
        raw = (CD / 'INSTALHD/RISING.EXE').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), ORIGINAL_SHA256)
        pe = struct.unpack_from('<I', raw, 0x3c)[0]
        secoes = []
        for i in range(struct.unpack_from('<H', raw, pe + 6)[0]):
            c = pe + 24 + struct.unpack_from('<H', raw, pe + 20)[0] + 40 * i
            secoes.append(struct.unpack_from('<IIII', raw, c + 8))

        def ler(endereco, tamanho):
            for _, rva, bruto, deslocamento in ((s[0], s[1], s[2], s[3]) for s in secoes):
                if rva <= endereco - 0x400000 < rva + bruto:
                    inicio = deslocamento + endereco - 0x400000 - rva
                    return raw[inicio:inicio + tamanho]
            raise AssertionError(hex(endereco))
        self.assertEqual(len(manifesto['intervals']), 47)
        for intervalo in manifesto['intervals']:
            inicio, fim = int(intervalo['start'], 16), int(intervalo['end_exclusive'], 16)
            self.assertEqual(hashlib.sha256(ler(inicio, fim - inicio)).hexdigest(), intervalo['sha256'],
                             intervalo['name'])
        tabelas = {t['name']: t for t in manifesto['tables']}
        self.assertEqual(struct.pack('<16h', *INDICE_IMA).hex(), tabelas['ima_index_words']['hex'])
        self.assertEqual(struct.pack('<89H', *PASSO_IMA).hex(), tabelas['ima_step_words']['hex'])
        for nome in ('ima_index_words', 'ima_step_words'):
            t = tabelas[nome]
            self.assertEqual(ler(int(t['start'], 16), t['bytes']).hex(), t['hex'])

    def test_bank_identities(self):
        for nome, (tamanho, sha) in IDENTIDADES.items():
            dados = ler_original(nome)
            self.assertEqual((len(dados), hashlib.sha256(dados).hexdigest()), (tamanho, sha))
        manifesto = carregar('som-manifesto.json')
        self.assertEqual({k: (v['bytes'], v['sha256']) for k, v in manifesto['banks'].items()}, IDENTIDADES)

    def test_no_decoded_audio_or_media_in_owned_paths(self):
        proibidos = {'.wav', '.raw', '.pcm', '.snd', '.hed', '.aif', '.aiff', '.mp3', '.ogg', '.flac'}
        for caminho in OWNED.rglob('*'):
            self.assertNotIn(caminho.suffix.lower(), proibidos, caminho)


class Capturas(unittest.TestCase):
    def test_structure_scenarios(self):
        estrutura = carregar('captura-som-estrutura.json')
        self.assertTrue(estrutura['created_before_translation'])
        for parte, chave in (('validacao', 'validation'), ('indice', 'index'), ('decodificador', 'decoder')):
            with self.subTest(parte=parte):
                self.assertEqual(normalizar(getattr(reproduzir_som, 'reproduzir_' + parte)()),
                                 normalizar(estrutura[chave]))

    def test_every_sound_in_every_bank(self):
        for letra in LETRAS_BANCO:
            with self.subTest(banco=letra):
                gravado = carregar(f'captura-som-banco-{letra}.json')
                self.assertTrue(gravado['created_before_translation'])
                self.assertEqual(normalizar(reproduzir_som.reproduzir_banco(letra)), normalizar(gravado))

    def test_sound_counts(self):
        contagem = {l: len(carregar(f'captura-som-banco-{l}.json')['surfaces_from_file']) for l in LETRAS_BANCO}
        self.assertEqual(contagem, {'A': 14, 'B': 102, 'P': 435})

    def test_catalogue_is_reproducible(self):
        gravado = json.loads(DESTINO.read_text())
        self.assertEqual(json.loads(json.dumps(construir(), ensure_ascii=False)), gravado)
        self.assertEqual(len(gravado['sounds']), 551)


class Contratos(unittest.TestCase):
    def test_make_id_full_width_or(self):
        self.assertEqual(criar_id_som(1, 0x1ff, 0x10000), 0x1ff00)
        self.assertEqual(criar_id_som(0xffff, 0xff, 0xff), 0xffffffff)

    def test_reachable_variants(self):
        self.assertEqual([variantes_alcancaveis(n) for n in range(6)],
                         [[0], [0], [0, 1], [0, 2], [0, 1, 2, 3], [0, 4]])

    def test_paths_and_unsupported_empty_directory(self):
        sistema = SistemaFixo({}, diretorio_corrente=b'C:\\', arena=ARENA, arena_tamanho=ARENA_TAMANHO)
        g = globais()
        self.assertEqual(criar_caminho_sons(sistema, g), b'C:\\SOUND')
        self.assertEqual(arquivo_som(g, b'A'), b'C:\\SOUND\\A')
        vazio = SistemaFixo({}, diretorio_corrente=b'', arena=ARENA, arena_tamanho=ARENA_TAMANHO)
        with self.assertRaises(DependenciaSom):
            criar_caminho_sons(vazio, globais())
        self.assertEqual([r[0] for r in vazio.registro], ['getcwd'])

    def test_decoder_domains(self):
        with self.assertRaises(DependenciaSom):
            decodificar_ima_mono16(bytes(8), 3)
        with self.assertRaises(DependenciaSom):
            decodificar_ima_estereo16(bytes(100), 72)
        with self.assertRaises(DependenciaSom):
            decodificar_ima_estereo16(bytes(76), 76)
        self.assertEqual(decodificar_ima_mono16(b'\1\2\3', 512), (b'', 0))
        self.assertEqual(decodificar_ima_estereo16(b'', 512), (b'', 0))

    def test_invalid_step_index_keeps_partial_output(self):
        bloco = struct.pack('<hBB', 10, 0, 0) + b'\x11' * 4 + struct.pack('<hBB', 0, 89, 0) + b'\0' * 4
        dados, eax = decodificar_ima_mono16(bloco, 8)
        self.assertEqual((len(dados), eax), (18, 0))

    def test_shapes_are_explicit(self):
        with self.assertRaises(ValueError):
            BancoSom(bytes(28), 0x521fc8)
        with self.assertRaises(ValueError):
            BancoSom(bytearray(27), 0x521fc8)
        with self.assertRaises(ValueError):
            GlobaisSom(nome_arquivo=bytearray(103), diretorio=bytearray(256), contador_variantes=0,
                       contador_alocacoes=0, janela=0, comprimido=0, directsound=0)

    def test_surface_without_compressed_buffer_is_a_dependency(self):
        hed, snd = reproduzir_som.banco_sintetico_superficies()
        mundo = reproduzir_som.Mundo(reproduzir_som.arquivos_z(hed, snd))
        reproduzir_som._abrir_z(mundo)
        cabecalho = mundo.bancos['A'].cabecalho[48:64]
        with self.assertRaises(DependenciaSom) as erro:
            criar_superficie_som(mundo.sistema, mundo.globais, mundo.bancos['A'], cabecalho)
        self.assertEqual(erro.exception.endereco, 0x48c14f)
        self.assertEqual([r[0] for r in mundo.registro[-3:]], ['_llseek', 'CreateSoundBuffer', '_llseek'])

    def test_without_directsound_no_buffer_is_created(self):
        hed, snd = reproduzir_som.banco_sintetico_superficies()
        mundo = reproduzir_som.Mundo(reproduzir_som.arquivos_z(hed, snd))
        reproduzir_som._abrir_z(mundo)
        mundo.globais.directsound = 0
        cabecalho = mundo.bancos['A'].cabecalho[64:80]
        self.assertEqual(criar_superficie_som(mundo.sistema, mundo.globais, mundo.bancos['A'], cabecalho), (0, []))
        self.assertEqual(mundo.registro[-1][0], '_llseek')


if __name__ == '__main__':
    unittest.main()
