"""AffGame in-game frames against original captures and the fresh native report."""
import hashlib
import json
import struct
import unittest
from graficos import RAIZ, Catalogo
from extrair_evidencias import imagem_pe
from cenas_quadro import (GLOBAIS, GATILHOS_FACHADA as GATILHOS_CENA, CODIGOS_AFFVEGET as CODIGOS_CENA,
    cenas_validacao, monde01_fixado, fundo, globais_base)
from ciclo_cache_terreno import CicloCacheTerreno, MemoriaMotor
from vinculos_graficos import ArenaGlobalFixa, RegistroVinculos
from quadro_jogo import (compor_quadro, calcular_frame, travar_superficie, EstadoTela, MundoQuadro, DependenciaQuadro,
    GLOBAIS_QUADRO, GATILHOS_FACHADA, CODIGOS_AFFVEGET, OFICINA, CHECKPOINT_HUD, DDERR_SURFACELOST)

SUPERFICIE = 0x8000000


def sha(data): return hashlib.sha256(bytes(data)).hexdigest()


class DD:
    def __init__(self, perdida=0, resultado=0): self.perdida, self.resultado, self.chamadas = perdida, resultado, []
    def is_lost(self): self.chamadas.append('IsLost'); return self.perdida
    def restore(self): self.chamadas.append('Restore'); return 0
    def lock(self): self.chamadas.append('Lock'); return self.resultado, SUPERFICIE


def mundo_modelo(cena):
    m = cena['mundo']
    return MundoQuadro(terreno=m['terreno'], objetos=m['objetos'], auxiliares=m['auxiliares'], regioes=m['regioes'],
        unidades=m['unidades'], projeteis=m['projeteis'], descoberta=m['descoberta'], iluminacao=m['iluminacao'])


def tabelas():
    sombra = bytes.fromhex(json.loads((RAIZ/'validacao/x86-cache-terreno.json').read_text())['tables_hex'][0])
    ecl = next(t for t in json.loads((RAIZ/'validacao/x86-eclairage.json').read_text())['tables'] if t['name'] == 'PLATGAME' and t['percentage'] == 60)
    return sombra, bytes.fromhex(ecl['table_hex'])


class FrameTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((RAIZ/'validacao/x86-quadro-jogo.json').read_text())
        cls.captura = json.loads((RAIZ/'evidencias/captura-quadro-original.json').read_text())
        cls.inventario = json.loads((RAIZ/'evidencias/quadro-jogo.json').read_text())
        cls.catalogo = Catalogo(); cls.sombra, cls.eclairage = tabelas(); cls.base = monde01_fixado()
        registros = {int(t): bytes.fromhex(h) for t, h in cls.captura['unit_initializer_records'].items()}
        cls.cenas = cenas_validacao(cls.base, registros)
        f = cls.report['cache_alloc_fixture']; registro = RegistroVinculos()
        memoria = MemoriaMotor(contador_u32=f['counter_u32'], vinculos=ArenaGlobalFixa(inicio_u32=f['arena_next'],
            tamanho_u32=f['arena_end']-f['arena_next'], registro=registro))
        cls.ciclo = CicloCacheTerreno.apos_carregar_banco(cls.catalogo); cls.ciclo.alocar(memoria)
        cls.alocacao = registro.desde(0); cls.resultados = []
        for cena in cls.cenas:
            if cena['antes'] == 'InitCache': cls.ciclo.iniciar()
            tela = EstadoTela(cena['globais']); ticks = list(cena['ticks'])
            try:
                q = compor_quadro(mundo_modelo(cena), tela, ciclo_cache=cls.ciclo, catalogo=cls.catalogo, tabela_sombra=cls.sombra,
                    tabela_eclairage=cls.eclairage, superficie=fundo(), relogio=lambda: ticks.pop(0), directdraw=DD())
                cls.resultados.append((cena, tela, q, None))
            except DependenciaQuadro as erro:
                cls.resultados.append((cena, tela, None, erro))
            cls.resultados[-1] += (cls.ciclo.proximo_u16, sha(cls.ciclo.registros), sha(cls.ciclo.blocos_crus))

    def test_original_bytes_tables_and_constants(self):
        base, imagem = imagem_pe()
        for regiao in self.inventario['regions']:
            dados = bytes.fromhex(regiao['bytes_hex']); self.assertEqual(sha(dados), regiao['sha256'])
            self.assertEqual(dados, imagem[int(regiao['start'], 16)-base:int(regiao['end'], 16)-base])
        self.assertEqual(GLOBAIS, GLOBAIS_QUADRO)
        self.assertEqual(set(GATILHOS_FACHADA), set(GATILHOS_CENA)); self.assertEqual(set(CODIGOS_AFFVEGET), set(CODIGOS_CENA))
        self.assertEqual(list(imagem[0x415a58-base:0x415a6f-base]), sorted(CODIGOS_AFFVEGET, key=lambda c: list(CODIGOS_CENA).index(c)))
        switch = bytes.fromhex(next(r for r in self.inventario['regions'] if r['name'] == 'AffBatiments_terrain_switch_and_tail')['bytes_hex'])
        for palavra in GATILHOS_FACHADA: self.assertIn(b'\x66\x3d'+struct.pack('<H', palavra), switch)
        self.assertEqual(struct.unpack('<H', imagem[0x402883-base:0x402885-base])[0], OFICINA)
        self.assertEqual(imagem[0x497284-base], 1)  # initial draw divisor
        escritas = self.inventario['static_absolute_writes']
        self.assertEqual(sorted(escritas['CalculFrame']['escritas']), ['0x496394', '0x496395', '0x496396', '0x4e17ae', '0x4e17b0', '0x4e17b4'])
        self.assertEqual(sorted(escritas['DDLockSurface']['escritas']), ['0x4e17a0', '0x4e17a4', '0x4e17a8'])
        self.assertEqual(escritas['AffTerrain']['escritas'], {}); self.assertEqual(escritas['AffSprite']['escritas'], {})

    def test_nine_frames_replay_the_fresh_native_report(self):
        self.assertEqual(self.alocacao, self.captura['cache_alloc'])
        linhas = {l['cena']: l for l in self.report['frames']}; self.assertEqual(len(linhas), 9)
        for cena, tela, q, erro, cursor, chaves, blocos in self.resultados:
            l = linhas[cena['nome']]
            self.assertEqual((cursor, chaves, blocos), (l['cache']['cursor'], l['cache']['keys_sha256'], l['cache']['payload_sha256']), cena['nome'])
            if erro is None:
                self.assertEqual(l['model'], 'complete'); self.assertEqual(sha(q['superficie']), l['surface_sha256'])
                self.assertEqual([list(e) for e in q['efeitos']], l['effects'])
                self.assertEqual(sha(json.dumps(q['chamadas'], separators=(',', ':')).encode('ascii')), l['trace']['sha256'])
            else:
                self.assertEqual((l['model'], l['stop'], l['detail']), ('named_stop', hex(erro.endereco), erro.detalhe))
                self.assertEqual(sha(erro.superficie), l['surface_sha256']); self.assertEqual([list(e) for e in erro.efeitos], l['effects'])
                self.assertEqual(sha(json.dumps(erro.chamadas, separators=(',', ':')).encode('ascii')), l['trace']['sha256'])

    def test_monde01_checkpoint_reaches_the_cave_facade_trigger(self):
        cena, tela, q, erro = self.resultados[0][:4]
        self.assertIsNone(q); self.assertEqual(erro.endereco, 0x40F23B); self.assertEqual(erro.chamadas[-1], ['AffBatiments', 544, 416, 3345])
        self.assertEqual(struct.unpack_from('<H', self.base['terreno'], 3345*2)[0], 0x2ed)
        pinned = self.captura['monde01_checkpoint']
        self.assertEqual((pinned['mission_stop'], pinned['eta_sha256']), (self.base['parada_missao'], self.base['eta_sha256']))
        self.assertEqual(sum(1 for c in erro.chamadas if c[0] == 'GetNumBob'), 425)
        captura = next(f for f in self.captura['frames'] if f['nome'] == 'monde01_checkpoint')
        self.assertEqual((captura['parada'], captura['rastro']['por_funcao']['AffEngin']), ('0x417b1c', 16))

    def test_draw_gate_and_calculframe_arithmetic(self):
        nao = next(r for r in self.resultados if r[0]['nome'] == 'nao_desenhado_divisor')
        self.assertFalse(nao[2]['desenhado']); self.assertEqual(nao[2]['parada'], 'retorno'); self.assertEqual(nao[2]['chamadas'], [['CalculFrame']])
        tela = EstadoTela(globais_base(fps_contador_u16=0xffff, fps_ultimo_tick_u32=0xfffffff0, paginas_u8=123))
        calcular_frame(tela, lambda: 0x3e0)
        self.assertEqual((tela.u('fps_contador_u16'), tela.bruto('fps_digitos'), tela.bruto('paginas_texto')), (0, b'00\0', b'123\0'))
        tela = EstadoTela(globais_base(fps_contador_u16=140, fps_ultimo_tick_u32=0)); calcular_frame(tela, lambda: 999)
        self.assertEqual((tela.u('fps_contador_u16'), tela.u('fps_tick_u32'), tela.u('fps_ultimo_tick_u32')), (141, 999, 0))
        calcular_frame(tela, lambda: 1000)
        self.assertEqual((tela.u('fps_contador_u16'), tela.bruto('fps_digitos')), (0, b'99\0'))
        forcado = next(r for r in self.resultados if r[0]['nome'] == 'forcado_e_evento')
        self.assertTrue(forcado[2]['desenhado'] and forcado[2]['evento'])

    def test_surface_lock_paths(self):
        tela = EstadoTela(globais_base(dd_travas_u32=2, dd_ponteiro_u32=0x1234)); dd = DD()
        self.assertEqual(travar_superficie(tela, dd), 0x1234); self.assertEqual((dd.chamadas, tela.u('dd_travas_u32')), ([], 3))
        tela = EstadoTela(globais_base(pitch_u32=640)); dd = DD(perdida=DDERR_SURFACELOST)
        self.assertEqual(travar_superficie(tela, dd), SUPERFICIE); self.assertEqual(dd.chamadas, ['IsLost', 'Restore', 'Lock'])
        self.assertEqual((tela.u('pitch_u32'), tela.u('dd_travas_u32')), (800, 1))
        tela = EstadoTela(globais_base()); dd = DD(resultado=0x88760096)
        self.assertEqual(travar_superficie(tela, dd), 0); self.assertEqual(tela.efeitos, [])

    def test_named_stops_before_drawing_and_missing_bindings(self):
        cena = self.cenas[1]; mundo = mundo_modelo(cena)
        def tentar(globais, **kw):
            args = dict(ciclo_cache=self.ciclo, catalogo=self.catalogo, tabela_sombra=self.sombra, tabela_eclairage=self.eclairage,
                superficie=fundo(), relogio=lambda: 5000, directdraw=DD()); args.update(kw)
            with self.assertRaises(DependenciaQuadro) as erro: compor_quadro(mundo, EstadoTela(globais), **args)
            return erro.exception
        self.assertEqual(tentar(globais_base(modo_jogo_u8=0x11)).endereco, 0x4176A8)
        self.assertEqual(tentar(globais_base(divisor_u8=0, quadro_u32=1)).endereco, 0x417921)
        self.assertEqual(tentar(globais_base(limpar_u8=1)).endereco, 0x41794B)
        self.assertEqual(tentar(globais_base(restaurar_fundo_u8=1)).endereco, 0x4179E1)
        self.assertEqual(tentar(globais_base(janela=struct.pack('<HH', 20, 13))).endereco, 0x41068E)
        self.assertEqual(tentar(globais_base(origem=struct.pack('<HH', 230, 0))).endereco, 0x416864)
        erro = tentar(globais_base(), relogio=None); self.assertEqual(erro.endereco, 0x43F71A)
        self.assertEqual([e[0] for e in erro.efeitos], ['fps_contador_u16'])
        erro = tentar(globais_base(), directdraw=object()); self.assertEqual(erro.endereco, 0x43F3D7)
        self.assertEqual(tentar(globais_base(), directdraw=DD(resultado=1)).endereco, 0x4179D4)
        for invalido in (lambda: EstadoTela({}), lambda: EstadoTela(dict(globais_base(), camera_u8=b'\0\0')),
                lambda: MundoQuadro(terreno=bytes(10), objetos=bytes(65536), auxiliares=bytes(65536), regioes=bytes(131072),
                    unidades=bytes(220800), projeteis=bytes(5600), descoberta=[bytes(65536)]*4, iluminacao=[bytes(65536)]*4)):
            with self.assertRaises(ValueError): invalido()

    def test_unit_guard_stops_outside_the_validated_body_domain(self):
        cena = next(c for c in self.cenas if c['nome'] == 'unidades_e_projeteis'); unidades = bytearray(cena['mundo']['unidades'])
        alvo = next(r for r in self.resultados if r[0]['nome'] == 'unidades_e_projeteis')[2]
        indice = next(c[3] for c in alvo['chamadas'] if c[0] == 'AffEngin')
        self.assertIn(unidades[indice*276+1], (0, 5, 6, 7, 9))
        struct.pack_into('<H', unidades, indice*276+0x74, 99)
        mundo = mundo_modelo(dict(cena, mundo=dict(cena['mundo'], unidades=bytes(unidades))))
        ciclo = CicloCacheTerreno.apos_carregar_banco(self.catalogo)
        ciclo.alocar(MemoriaMotor(contador_u32=0, vinculos=ArenaGlobalFixa(inicio_u32=0x1000, tamanho_u32=0x1000, registro=RegistroVinculos())))
        ciclo.iniciar()
        with self.assertRaises(DependenciaQuadro) as erro:
            compor_quadro(mundo, EstadoTela(cena['globais']), ciclo_cache=ciclo, catalogo=self.catalogo, tabela_sombra=self.sombra,
                tabela_eclairage=self.eclairage, superficie=fundo(), relogio=lambda: 2140, directdraw=DD())
        self.assertEqual((erro.exception.endereco, erro.exception.chamadas[-1][0], erro.exception.chamadas[-1][3]), (0x41591F, 'AffEngin', indice))

    def test_report_totals(self):
        r = self.report
        self.assertEqual((r['result'], r['expected_limits'], r['skips'], r['checkpoint']), ('PASS', 0, 0, hex(CHECKPOINT_HUD)))
        self.assertEqual((r['totals']['frames'], r['totals']['complete'], r['totals']['named_stops']), (9, 6, 3))
        self.assertEqual(self.captura['totals']['native_entries'], 21)


if __name__ == '__main__': unittest.main()
