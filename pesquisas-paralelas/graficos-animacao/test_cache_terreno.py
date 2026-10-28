"""Replay independent full-state/raw-pixel GetNumBob cache captures."""
import hashlib
import json
import struct
import unittest
from graficos import RAIZ, Catalogo
from extrair_evidencias import imagem_pe
from cache_terreno import CacheTerreno, resolver_bloco_terreno


def sha(data):return hashlib.sha256(data).hexdigest()


def make_cache(initial):
    return CacheTerreno(bytes.fromhex(initial['entries_hex']),bytes([initial['raw_fill_u8']])*(256*1056),proximo_u16=initial['next_u16'])


class TerrainCacheTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((RAIZ/'validacao/x86-cache-terreno.json').read_text());cls.catalog=Catalogo()
        cls.tables=[bytes.fromhex(v) for v in cls.report['tables_hex']]

    def test_8522_original_cache_states_and_raw_block_pixels(self):
        self.assertEqual(self.report['result'],'PASS');count=0
        for group in self.report['groups']:
            cache=make_cache(group['initial'])
            for v,ident,branch,next_index,entries_hash,raw_hash,pixels_hash in group['captures']:
                source,discovery,light,table,_,_=v
                plan=resolver_bloco_terreno(self.catalog,cache,id_terreno_u16=source,descoberta_u8=discovery,
                    iluminacao_u8=light,tabela_sombra=self.tables[table])
                self.assertEqual((plan['id_motor'],plan['motivo'],cache.proximo_u16),(ident,branch,next_index))
                self.assertEqual(sha(cache.registros),entries_hash);self.assertEqual(sha(cache.blocos_crus),raw_hash)
                if 1090<=ident<=1345:self.assertEqual(sha(cache.pixels(ident-1090)),pixels_hash)
                elif pixels_hash is not None:self.assertEqual(sha(self.catalog.quadro(ident).pixels),pixels_hash)
                count+=1
        self.assertEqual(count,8522)
        self.assertEqual(self.report['branches'],dict(undiscovered=770,direct=40,hit=711,miss=7001))

    def test_native_duplicate_precedence_and_cursor_wrap(self):
        duplicates=next(g for g in self.report['groups'] if g['name']=='duplicates_and_raw_hit')['captures']
        self.assertEqual(duplicates[0][1:4],[1095,'hit',255]);self.assertEqual(duplicates[1][1:4],[1095,'hit',255])
        self.assertEqual(duplicates[2][1:4],[1093,'hit',255])
        self.assertEqual(duplicates[3][1:4],[1345,'miss',0]);self.assertEqual(duplicates[4][1:4],[1090,'miss',1])
        group=next(g for g in self.report['groups'] if g['name']=='all_static_sources')
        self.assertEqual(group['captures'][0][1:4],[1345,'miss',0]);self.assertEqual(group['captures'][1][1:4],[1090,'miss',1])

    def test_native_table_changes_do_not_invalidate_a_hit(self):
        group=next(g for g in self.report['groups'] if g['name']=='table_staleness');rows=group['captures']
        self.assertEqual(rows[0][2],'miss');self.assertEqual(rows[1][2],'hit')
        self.assertEqual(rows[0][1],rows[1][1]);self.assertEqual(rows[0][4:],rows[1][4:])
        self.assertEqual(rows[-1][2],'miss');self.assertNotEqual(rows[0][-1],rows[-1][-1])

    def test_literal_fog_mask_follows_shadow_and_preserves_row_headers(self):
        group=next(g for g in self.report['groups'] if g['name']=='masks_and_tables')
        rows=[row for row in group['captures'] if row[0][0:4]==[300,15,15,2]]
        self.assertEqual(len(rows),1);self.assertEqual(rows[0][-1],sha(bytes([2])*1024))
        initial=self.report['groups'][0]['initial'];cache=make_cache(initial)
        plan=resolver_bloco_terreno(self.catalog,cache,id_terreno_u16=300,descoberta_u8=15,iluminacao_u8=15,tabela_sombra=self.tables[2])
        self.assertEqual(cache.pixels(plan['indice_cache']),bytes([2])*1024)
        raw=cache.blocos_crus[:1056];self.assertTrue(all(raw[row*33]==224 for row in range(32)))
        self.assertNotEqual(self.tables[2][2],2)

    def test_hidden_direct_and_hit_paths_do_not_fetch_assets(self):
        class NoCatalog:
            def quadro(self,_):raise AssertionError('Fast cache branch fetched an asset')
        cache=make_cache(self.report['groups'][0]['initial']);before=(bytes(cache.registros),bytes(cache.blocos_crus),cache.proximo_u16)
        for source,discovery,light,expected in ((65535,16,255,1081),(0,16,0,1081),(0,0,0,0),(65535,224,224,65535)):
            p=resolver_bloco_terreno(NoCatalog(),cache,id_terreno_u16=source,descoberta_u8=discovery,iluminacao_u8=light,tabela_sombra=self.tables[0])
            self.assertEqual(p['id_motor'],expected)
        self.assertEqual((bytes(cache.registros),bytes(cache.blocos_crus),cache.proximo_u16),before)
        cache=make_cache(next(g for g in self.report['groups'] if g['name']=='duplicates_and_raw_hit')['initial'])
        p=resolver_bloco_terreno(NoCatalog(),cache,id_terreno_u16=65535,descoberta_u8=1,iluminacao_u8=1,tabela_sombra=self.tables[0])
        self.assertEqual(p['id_motor'],1093)

    def test_owned_snapshot_copies_and_protected_input_domain(self):
        initial=self.report['groups'][0]['initial'];entries=bytearray.fromhex(initial['entries_hex']);blocks=bytearray([82])*(256*1056)
        before=(bytes(entries),bytes(blocks));cache=CacheTerreno(entries,blocks,proximo_u16=0);table=bytearray(self.tables[2]);old_table=bytes(table)
        resolver_bloco_terreno(self.catalog,cache,id_terreno_u16=1,descoberta_u8=1,iluminacao_u8=2,tabela_sombra=table)
        self.assertEqual((bytes(entries),bytes(blocks)),before);self.assertEqual(bytes(table),old_table)
        snapshot=(bytes(cache.registros),bytes(cache.blocos_crus),cache.proximo_u16)
        with self.assertRaises(NotImplementedError):resolver_bloco_terreno(self.catalog,cache,id_terreno_u16=1082,descoberta_u8=1,iluminacao_u8=1,tabela_sombra=table)
        self.assertEqual((bytes(cache.registros),bytes(cache.blocos_crus),cache.proximo_u16),snapshot)
        for args in (dict(id_terreno_u16=65536,descoberta_u8=1,iluminacao_u8=1),dict(id_terreno_u16=1,descoberta_u8=False,iluminacao_u8=1)):
            with self.assertRaises(ValueError):resolver_bloco_terreno(self.catalog,cache,tabela_sombra=table,**args)
        with self.assertRaises(ValueError):CacheTerreno(entries,blocks,proximo_u16=256)
        with self.assertRaises(ValueError):CacheTerreno(entries[:-1],blocks,proximo_u16=0)
        with self.assertRaises(TypeError):resolver_bloco_terreno(self.catalog,cache)

    def test_original_bytes_source_blocks_predecessors_and_reviewed_rea(self):
        e=json.loads((RAIZ/'evidencias/cache-terreno.json').read_text());base,image=imagem_pe()
        for region in e['regions']:
            data=bytes.fromhex(region['bytes_hex']);self.assertEqual(sha(data),region['sha256'])
            self.assertEqual(data,image[int(region['start'],16)-base:int(region['end'],16)-base])
        for path,digest in e['predecessor_sources'].items():self.assertEqual(sha((RAIZ/path).read_bytes()),digest)
        hashes=[]
        for ident in range(1,1082):
            frame=self.catalog.quadro(ident);self.assertEqual((frame.largura,frame.altura,len(frame.comprimido)),(32,32,1056))
            self.assertTrue(all(frame.comprimido[row*33]==224 for row in range(32)));hashes.append(sha(frame.comprimido))
        self.assertEqual(sha(''.join(hashes).encode('ascii')),self.report['source_block_sha256'])
        review=json.loads((RAIZ/'evidencias/rea-cache-terreno-review.json').read_text());native=review['instruction_observation']['normalized_result']
        self.assertEqual(native['bytes'],image[0x40ff39-base:0x40ff3b-base].hex());self.assertEqual(native['mnemonic'],'IDIV')


if __name__=='__main__':unittest.main()
