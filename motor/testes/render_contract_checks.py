"""Renderer contract, own-world pixels and original input-time cases."""
import ctypes as C
import hashlib,json,os,unittest,struct
from pathlib import Path
from render_abi import *
from render_proof import live,prove
from render_matrix import run

class RenderTests(unittest.TestCase):
    def test_reference_identity_is_pinned_graphics_17(self):
        pin=json.loads((ROOT/'motor/testes/render-reference-pins.json').read_text())
        self.assertEqual(pin['contract'],[1,7])
        f=Frames()
        for version in (0x00010000,0x00010001,0x00010002,0x00010003):
            handle=U64();f.check(f.lib.rl_criar_mundo(version,20,0,C.byref(handle)));f.free(handle.value)
        for name,digest in pin['sources'].items():self.assertEqual(hashlib.sha256(reference_file(ROOT/name).read_bytes()).hexdigest(),digest,name)

    def test_graphics17_production_glyph_prefixes_and_saved_background(self):
        from render_probe_proof import prove as probe_proof
        for probe,count,frame in [('P1',41,170),('P2',90,219),('P3',12,141)]:
            report=probe_proof(probe,binary=ROOT/'motor/target/debug/render_probe_stream',strict=True)
            self.assertEqual((report['full_equal'],report['first_stop']['frame']),(count,frame))
            self.assertEqual(report['first_stop']['stop'],'0x459454')
            self.assertTrue(report['first_stop']['native_partial_equal'])
            self.assertIsNone(report['first_difference'])

    def test_graphics17_original_all_health_facade_matrix(self):
        from render_facade_proof import prove as facade_proof
        report=facade_proof(binary=ROOT/'motor/target/debug/render_probe_stream')
        self.assertEqual((report['cases'],report['equal']),(600,600))

    def test_recorded_text_adapter_rejects_wrong_pixels_and_arguments(self):
        import contextlib,copy
        from render_probe_proof import Stream
        from validar_sondas_graficos_m3 import CapturaSondaGrafica
        cap=CapturaSondaGrafica(RAIZ/'evidencias/sonda-render-P3-api17.json.xz');row=next(r for r in cap.d['rows'] if r['text_boundaries']);memory=cap.memory(row)
        tick=struct.unpack_from('<I',cap.blob(row['exit_dgroup']),0x4e17b4-0x494000)[0]
        for field in ('pixels','arguments'):
            boundaries=copy.deepcopy(row['text_boundaries'])
            if field=='pixels':boundaries[0]['surface_before']='00'*32
            else:boundaries[0]['text_hex']=b'UNATTESTED'.hex()
            stream=Stream(ROOT/'motor/target/debug/render_probe_stream')
            try:
                with self.assertRaises(RuntimeError):stream.frame(memory,tick,initial=(cap.blob(row['before']),cap.cache_entry(row)),boundaries=boundaries)
            finally:
                with contextlib.suppress(RuntimeError,BrokenPipeError):stream.close()

    def test_original_input_time_full_surfaces_and_named_fire_stop(self):
        report=run()
        self.assertEqual((report['cases'],report['complete'],report['stops'],report['mismatches']),(114,113,1,0))

    def test_perturbed_stops_and_actual_partial_prefixes(self):
        from render_stops import run
        report=run()
        self.assertEqual((report['cases'],report['stops'],report['mismatches']),(26,26,0))

    def test_own_world_first_frame_surface_cache_effects_and_read_only(self):
        report=prove(1)
        self.assertEqual((report['full_frames'],report['original_equal'],report['python_equal']),(1,1,1))
        row=report['rows'][0]
        for name in ['cache_equal','stop_equal','world_read_only','palette_equal','effects_equal']:self.assertTrue(row[name],name)

    def test_copied_buffers_generation_query_reset_and_lifetimes(self):
        f,world,inp=live();r=Render(f);surface,cache=initial();h=r.create(world,surface,cache)
        try:
            self.assertEqual(r.lib.rl_render_contrato(),0x00010007)
            self.assertEqual(r.saved(h)[:2],(0,b''))
            generation,phase,counter=r.generation(world);self.assertEqual((phase,counter),(1,0))
            result=Result();r.pixels[0]=222;r.palette[0]=111
            code=r.lib.rl_render_quadro(h,generation,1,r.pixels,479999,r.palette,768,C.byref(result));self.assertEqual(code,6)
            self.assertEqual((result.required_pixels,result.required_palette),(480000,768));self.assertEqual((r.pixels[0],r.palette[0]),(222,111));self.assertEqual(r.cache(h),cache)
            sentinel=bytes(result)
            code=r.lib.rl_render_quadro(h,generation+1,1,r.pixels,480000,r.palette,768,C.byref(result));self.assertEqual(code,11);self.assertEqual(bytes(result),sentinel)
            first=r.draw(h,generation);pixels=bytes(r.pixels);after=r.cache(h);obs=r.observations(h);again=r.draw(h,generation)
            self.assertEqual(bytes(first),bytes(again));self.assertEqual(bytes(r.pixels),pixels);self.assertEqual(r.cache(h),after);self.assertEqual([bytes(x) for x in r.observations(h)],[bytes(x) for x in obs])
            r.reset(h,surface,cache);self.assertEqual(r.cache(h),cache);self.assertEqual(r.draw(h,generation).disposition,0);self.assertEqual(bytes(r.pixels),pixels)
            f.frame(world,2,inp);g2,p2,_=r.generation(world);self.assertGreater(g2,generation);self.assertEqual(p2,2)
            self.assertEqual(r.lib.rl_render_quadro(h,generation,1,r.pixels,480000,r.palette,768,C.byref(result)),11)
            self.assertEqual(r.lib.rl_render_quadro(h,g2,1,r.pixels,480000,r.palette,768,C.byref(result)),1)
            self.assertEqual(bytes(r.pixels),pixels)
            f.free(world);world=None
            self.assertEqual(r.lib.rl_render_quadro(h,g2,1,r.pixels,480000,r.palette,768,C.byref(result)),2)
        finally:r.free(h);f.free(world) if world else None
        self.assertEqual(r.lib.rl_render_liberar(h),2)

    def test_undrawn_preserves_surface_and_complete_cache(self):
        from render_matrix import cases,run
        name,blocks,surface,cache,tick,*_=cases()[0]
        changed=[]
        for base,data in blocks:
            data=bytearray(data)
            for address,value in ((0x508f7c,b'\1\0\0\0'),(0x497284,b'\2'),(0x4e05a2,b'\0')):
                if base<=address and address+len(value)<=base+len(data):data[address-base:address-base+len(value)]=value
            changed.append((base,bytes(data)))
        report=run(compare_python=True,rows=[('undrawn',changed,surface,cache,tick,surface,0)])
        self.assertEqual(report['mismatches'],0)
        self.assertTrue(report['rows'][0]['python_cache_equal'])

    def test_asset_identity_and_invalid_creation_are_atomic(self):
        f,world,inp=live();r=Render(f);surface,cache=initial();assets=original_assets();bad=list(assets);bad[0]=bytes([assets[0][0]^1])+assets[0][1:]
        try:
            with self.assertRaises(RuntimeError):r.create(world,surface,cache,bad)
            with self.assertRaises(RuntimeError):r.create(world,surface[:-1],cache,assets)
            h=r.create(world,surface,cache,assets);r.free(h)
        finally:f.free(world)

if __name__=='__main__':unittest.main()
