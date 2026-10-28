"""Cache lifecycle against original-only captures and the fresh native report."""
import hashlib
import json
import struct
import unittest
from graficos import RAIZ, Catalogo
from extrair_evidencias import imagem_pe
from cache_terreno import resolver_bloco_terreno
from ciclo_cache_terreno import (CicloCacheTerreno, MemoriaMotor, DependenciaCicloCache, blocos_banco_cache,
    CAPACIDADE_U16)
from vinculos_graficos import ArenaGlobalFixa, ArquivosDeclarados, RegistroVinculos, ParadaVinculo
from capturar_ciclo_cache import consultas


def sha(data): return hashlib.sha256(data).hexdigest()


class VinculosParciais:
    """Arena binding with selected imports removed, to reach dependency stops."""
    def __init__(self, arena, ausentes):
        for nome in ('global_alloc', 'global_lock', 'global_handle', 'global_unlock', 'global_free'):
            if nome not in ausentes: setattr(self, nome, getattr(arena, nome))


class CacheLifecycleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.captura = json.loads((RAIZ/'evidencias/captura-ciclo-cache-original.json').read_text())
        cls.inventario = json.loads((RAIZ/'evidencias/ciclo-cache.json').read_text())
        cls.report = json.loads((RAIZ/'validacao/x86-ciclo-cache.json').read_text())
        cls.catalogo = Catalogo(); cls.tabela = bytes.fromhex(cls.captura['shadow_table_hex'])
        cls.eventos = {e['event']: e for e in cls.captura['lifecycle']}

    def novo(self):
        banco = self.captura['LoadSTRATBank']; registro = RegistroVinculos()
        arena = ArenaGlobalFixa(inicio_u32=int(banco['arena_next_after'], 16), tamanho_u32=0x1000, registro=registro)
        return CicloCacheTerreno.apos_carregar_banco(self.catalogo), MemoriaMotor(contador_u32=banco['counter_after_u32'], vinculos=arena), arena

    def test_original_bytes_sections_and_static_callers(self):
        base, imagem = imagem_pe()
        for regiao in self.inventario['regions']:
            dados = bytes.fromhex(regiao['bytes_hex']); self.assertEqual(sha(dados), regiao['sha256'])
            self.assertEqual(dados, imagem[int(regiao['start'], 16)-base:int(regiao['end'], 16)-base])
        bss = next(s for s in self.inventario['sections'] if s['nome'] == '.bss')
        self.assertEqual((bss['rva'], bss['pointer_to_raw_data'], bss['characteristics']), ('0x9a000', 0, '0xc0000080'))
        chamadas = self.inventario['static_scan']['chamadas_rel32']
        self.assertEqual([c[2] for c in chamadas['0x40fa38']], ['MenuNewSelect+0x2c4', 'CalculGame+0x987'])
        self.assertEqual([c[2] for c in chamadas['0x40fa18']], ['ProgInit+0x2c4'])
        self.assertEqual([c[2] for c in chamadas['0x40fa2e']], ['ProgExit+0x23'])
        self.assertEqual([c[2] for c in chamadas['0x40fd95']], ['AffTerrain+0x1d1'])
        for morto in ('0x40fa72', '0x40fae0', '0x40fbc7'): self.assertEqual(chamadas[morto], [])
        escritores = {r[1].split('+')[0] for r in self.inventario['static_scan']['referencias_absolutas']['0x49a04e']}
        self.assertEqual(escritores, {'GetNumBob', 'SetCacheBloc', 'ConstruitCache'})
        for regiao in ('ProgInit_bank_then_CacheAlloc', 'CalculGame_start_InitCache_before_MissionLoad'):
            self.assertIn(regiao, {r['name'] for r in self.inventario['regions']})

    def test_process_load_state_and_real_bank_payloads(self):
        base, imagem = imagem_pe()
        for endereco, largura in ((0x49a04e, 2), (0x49a050, 4), (0x4e2f3c, 4)):
            self.assertEqual(imagem[endereco-base:endereco-base+largura], bytes(largura))
        self.assertEqual(struct.unpack('<H', imagem[0x495bc4-base:0x495bc6-base])[0], CAPACIDADE_U16)
        self.assertEqual(self.captura['process_load_state'], dict(ponteiro_chaves_u32=0, cursor_u16=0, contador_memoria_u32=0, capacidade_u16=256))
        banco = self.captura['LoadSTRATBank']; blocos = blocos_banco_cache(self.catalogo)
        self.assertEqual(sha(blocos), banco['cached_payload_sha256']); self.assertTrue(banco['cached_payload_equals_blocs_cmp'])
        self.assertEqual(sorted(len(v) for v in banco['cached_distinct_payloads'].values()), [1, 1, 254])
        self.assertEqual(len({d[4] for d in banco['cached_descriptors']}), 256)
        ciclo = CicloCacheTerreno.apos_carregar_banco(self.catalogo)
        self.assertEqual((ciclo.ponteiro_chaves_u32, ciclo.proximo_u16, ciclo.estado, ciclo.registros), (0, 0, 'sem_tabela', None))
        # Counter after LoadSTRATBank: header8 + table4*N + per-frame descriptor12 + payload bytes.
        quantidade = banco['count']; tamanhos = 13411692-2*6-8*quantidade
        self.assertEqual(banco['counter_after_u32'], 8+4*quantidade+12*quantidade+tamanhos)
        self.assertEqual(banco['bound_calls']['por_vinculo'], dict(GlobalAlloc=24314, GlobalLock=24314, fclose=12, fopen=12, fread=48636))

    def test_complete_lifecycle_replays_original_capture(self):
        ciclo, memoria, arena = self.novo(); alloc = self.captura['CacheAlloc']
        self.assertEqual(ciclo.alocar(memoria), alloc['pointer_u32'])
        self.assertEqual(arena.registro.desde(0), alloc['bound_calls']); self.assertEqual(memoria.contador_u32, alloc['counter_u32'])
        self.assertIsNone(ciclo.registros); self.assertEqual(set(bytes.fromhex(alloc['keys_hex'])), {0xa5})
        with self.assertRaises(DependenciaCicloCache): ciclo.cache
        fases = consultas(); deslocamento = 0
        for nome_init, nome_fase, lista in (('InitCache_1', 'GetNumBob_phase_1', fases['apos_primeiro_init']),
                ('InitCache_2', 'GetNumBob_phase_2', fases['apos_segundo_init'])):
            antes = sha(ciclo.blocos_crus); e = self.eventos[nome_init]
            self.assertEqual(ciclo.iniciar(), int(e['registers']['EAX'], 16))
            self.assertEqual(ciclo.registros, bytes.fromhex(e['keys_hex'])); self.assertEqual(ciclo.proximo_u16, e['cursor_u16'])
            self.assertEqual(sha(ciclo.blocos_crus), e['payload_sha256']); self.assertEqual(antes, e['payload_before_sha256'])
            for indice, ((fonte, descoberta, iluminacao), linha) in enumerate(zip(lista, self.eventos[nome_fase]['queries'])):
                plano = resolver_bloco_terreno(self.catalogo, ciclo.cache, id_terreno_u16=fonte, descoberta_u8=descoberta,
                    iluminacao_u8=iluminacao, tabela_sombra=self.tabela)
                self.assertEqual(linha[0][:3], [fonte, descoberta, iluminacao])
                self.assertEqual([plano['id_motor'], plano['motivo'], ciclo.proximo_u16, sha(ciclo.registros), sha(ciclo.blocos_crus)], linha[1:],
                    (nome_fase, indice))
            deslocamento += len(lista)
        self.assertEqual(deslocamento, 547)
        livre = self.eventos['CacheFree']; marca = arena.registro.marca()
        self.assertEqual(ciclo.liberar(memoria), int(livre['registers']['EAX'], 16))
        self.assertEqual(arena.registro.desde(marca), livre['bound_calls'])
        self.assertEqual((ciclo.ponteiro_chaves_u32, ciclo.proximo_u16, memoria.contador_u32),
            (livre['pointer_u32'], livre['cursor_u16'], livre['counter_u32']))
        self.assertEqual(sha(ciclo.blocos_crus), livre['payload_sha256'])
        for chamada in (ciclo.iniciar, lambda: ciclo.cache, lambda: ciclo.liberar(memoria), lambda: ciclo.alocar(memoria)):
            with self.assertRaises(DependenciaCicloCache): chamada()

    def test_restart_keeps_cursor_and_stale_payload_but_drops_keys(self):
        fase1 = self.eventos['GetNumBob_phase_1']['queries']; fase2 = self.eventos['GetNumBob_phase_2']['queries']
        self.assertEqual(self.eventos['InitCache_2']['cursor_before'], self.eventos['InitCache_2']['cursor_u16'])
        self.assertEqual(self.eventos['InitCache_2']['payload_before_sha256'], self.eventos['InitCache_2']['payload_sha256'])
        self.assertTrue(any(l[0][:3] == [777, 1, 1] and l[2] == 'miss' for l in fase1))
        self.assertEqual(fase2[0][0][:3], [777, 1, 1]); self.assertEqual((fase2[0][1], fase2[0][2]), (1090+18, 'miss'))
        self.assertEqual(self.eventos['CacheFree']['pointer_u32'], self.captura['CacheAlloc']['pointer_u32'])
        self.assertEqual(self.eventos['CacheFree']['counter_u32'], self.captura['CacheAlloc']['counter_u32'])

    def test_missing_bindings_stop_at_original_call_sites_retaining_effects(self):
        for ausente, endereco, chamadas in (('global_alloc', 0x467eb9, 0), ('global_lock', 0x467ec1, 1)):
            ciclo, memoria, arena = self.novo(); memoria.vinculos = VinculosParciais(arena, {ausente}); antes = memoria.contador_u32
            with self.assertRaises(DependenciaCicloCache) as erro: ciclo.alocar(memoria)
            self.assertEqual(erro.exception.endereco, endereco); self.assertEqual(memoria.contador_u32, antes+1024)
            self.assertEqual(arena.registro.marca(), chamadas); self.assertEqual((ciclo.estado, ciclo.ponteiro_chaves_u32), ('sem_tabela', 0))
        for ausente, endereco, chamadas in (('global_handle', 0x467ed1, 0), ('global_unlock', 0x467ed9, 1), ('global_free', 0x467ee9, 3)):
            ciclo, memoria, arena = self.novo(); ciclo.alocar(memoria); ciclo.iniciar(); marca = arena.registro.marca()
            memoria.vinculos = VinculosParciais(arena, {ausente})
            with self.assertRaises(DependenciaCicloCache) as erro: ciclo.liberar(memoria)
            self.assertEqual(erro.exception.endereco, endereco); self.assertEqual(arena.registro.marca()-marca, chamadas)
            self.assertEqual(ciclo.estado, 'iniciada')

    def test_null_table_and_out_of_order_lifecycle_are_named_dependencies(self):
        nulo = self.captura['null_pointer_initcache']
        self.assertEqual((nulo['eip'], nulo['key_pointer_u32'], nulo['bound_calls']), ('0x40fa49', 0, 0))
        ciclo, memoria, arena = self.novo()
        with self.assertRaises(DependenciaCicloCache) as erro: ciclo.iniciar()
        self.assertEqual(erro.exception.endereco, 0x40fa49)
        with self.assertRaises(DependenciaCicloCache): ciclo.liberar(memoria)
        ciclo.alocar(memoria)
        with self.assertRaises(DependenciaCicloCache) as erro: ciclo.alocar(memoria)
        self.assertEqual(erro.exception.endereco, 0x40fa18)
        nulo_lock = CicloCacheTerreno.apos_carregar_banco(self.catalogo)
        class LockNulo:
            def global_alloc(self, flags, n): return 0x12340
            def global_lock(self, handle): return 0
        nulo_lock.alocar(MemoriaMotor(contador_u32=0, vinculos=LockNulo()))
        with self.assertRaises(DependenciaCicloCache): nulo_lock.iniciar()
        for invalido in (lambda: CicloCacheTerreno(bytes(10), proximo_u16=0), lambda: CicloCacheTerreno(bytes(256*1056), proximo_u16=256),
                lambda: ciclo.alocar(object()), lambda: MemoriaMotor(contador_u32=-1, vinculos=arena)):
            with self.assertRaises(ValueError): invalido()
        class Largo:
            def global_alloc(self, flags, n): return 1 << 32
        with self.assertRaises(ValueError): MemoriaMotor(contador_u32=0, vinculos=Largo()).mem_alloc(4)

    def test_declared_fixtures_refuse_semantics_they_cannot_honor(self):
        registro = RegistroVinculos(); arena = ArenaGlobalFixa(inicio_u32=0x1000, tamanho_u32=64, registro=registro)
        for chamada in (lambda: arena.global_alloc(2, 16), lambda: arena.global_alloc(0, 0), lambda: arena.global_alloc(0, 65),
                lambda: arena.global_lock(0x2000), lambda: arena.global_free(0x1000)):
            with self.assertRaises(ParadaVinculo): chamada()
        p = arena.global_alloc(0, 10); self.assertEqual((p, arena.proximo), (0x1000, 0x1010))
        self.assertEqual((arena.global_unlock(p), arena.global_free(p)), (0, 0))
        with self.assertRaises(ParadaVinculo): arena.global_handle(p)
        arquivos = ArquivosDeclarados({'\\A.cmp': b'abc'}, registro=registro)
        for chamada in (lambda: arquivos.fopen('\\A.cmp', 'r'), lambda: arquivos.fopen('\\B.cmp', 'rb'), lambda: arquivos.fread(0, 1, 1, 7)):
            with self.assertRaises(ParadaVinculo): chamada()
        h = arquivos.fopen('\\A.cmp', 'rb'); self.assertEqual(arquivos.fread(0x10, 2, 1, h), (b'ab', 1))
        with self.assertRaises(ParadaVinculo): arquivos.fread(0x10, 2, 1, h)
        self.assertEqual(arquivos.fclose(h), 0)
        self.assertEqual([c[0] for c in registro.chamadas], ['GlobalAlloc', 'GlobalUnlock', 'GlobalFree', 'fopen', 'fread', 'fclose'])

    def test_fresh_native_report(self):
        r = self.report
        self.assertEqual((r['result'], r['synthetic_payload_binding'], r['expected_limits'], r['skips']), ('PASS', None, 0, 0))
        self.assertEqual(r['totals']['native_entries'], 554); self.assertEqual(r['totals']['whole_state_comparisons'], 552)
        self.assertEqual(r['getnumbob'], dict(phase_1=539, phase_2=8, branches=dict(undiscovered=3, direct=3, hit=7, miss=534)))
        self.assertEqual(r['expected_faults'][0]['eip'], '0x40fa49'); self.assertEqual(r['expected_faults'][0]['model'], '0x40fa49')
        self.assertEqual([s['step'] for s in r['steps']], ['CacheAlloc', 'InitCache_1', 'InitCache_2', 'CacheFree'])
        self.assertEqual(r['bindings']['LoadSTRATBank'], self.captura['LoadSTRATBank']['bound_calls'])


if __name__ == '__main__': unittest.main()
