"""Original AffGame replay at recorded display entries, enabling only AffText.

First reproduce the historical full surface with its declared text boundary. Restore
the identical entry, remove only AffText, then execute the intact original again.
TextGetMessage/InitTextLangue remain the display-v2 declared boundaries: TEXTES.TXT
is not fabricated or loaded by this experiment. Literal tooltip bytes and the six
bitmap font banks already loaded by the original display scenario are consumed.
These are isolated display calls, not a glyph-enabled whole-state mission replay.
"""
import argparse, base64, json, lzma, signal, struct, time, zlib
from pathlib import Path
from capturar_escritas_cave_m3 import original, REF, sha
from oraculo_quadro_missao import BancadaCargaMissaoOriginal
from emulador import RETORNO, PILHA


def main(a):
    signal.alarm(1140)
    output = Path(a.output)
    if output.exists(): raise FileExistsError(output)
    original.REF = REF
    b, _, _ = original.modulo_entrada().abrir(a.start, None)
    cpu = b.cpu
    table=int.from_bytes(cpu.mem_read(0x508f6c,4),'little')
    glyph_metrics=[]
    for font,base in enumerate((0x23d5,0x24b5,0x2595,0x2675,0x2755,0x2835),1):
        for code in range(32,256):
            ident=base+code-32
            pointer=int.from_bytes(cpu.mem_read(table+4*(ident-1),4),'little')
            width,height=struct.unpack('<HH',cpu.mem_read(pointer,4))
            glyph_metrics.append(dict(font=font,byte=code,id=ident,pointer=hex(pointer),width=width,height=height))
    image = b.imagem()
    payload_addresses = [image[f'alloc{2196+2*i:05d}'][0] for i in range(256)]
    cap = original.CapturadorSondasGraficos(b)
    cap.phase_frame = None
    cpu.hook_add(original.unicorn.UC_HOOK_CODE, b._parar_se_pedido, begin=RETORNO, end=RETORNO)
    aff = b.sym['AffText']; skipped = (b.pulos[aff], b.fronteiras[aff])
    rows = []; blobs = {}; sources = {}; started = time.monotonic()
    for spec in a.capture:
        name, selection = spec.rsplit(':', 1)
        path = original.AQUI / 'evidencias' / name
        raw = path.read_bytes(); d = json.loads(lzma.decompress(raw))
        sources[name] = sha(raw)
        lo, hi = map(int, selection.split('-'))
        def blob(key):
            value = zlib.decompress(base64.b64decode(d['blobs'][key])); assert sha(value) == key
            return value
        for entry in d['rows']:
            if not lo <= entry['frame'] <= hi: continue
            outputs = []
            for enabled in (False, True):
                for base, key in entry['entry'].values(): cpu.mem_write(int(base, 16), blob(key))
                u = lambda p, n: int.from_bytes(cpu.mem_read(p, n), 'little')
                surface = u(0x508f70, 4); cpu.mem_write(surface, blob(entry['before']))
                cache = entry['cache']; cpu.mem_write(u(0x49a050, 4), blob(cache['keys']))
                payload = blob(cache['payloads'])
                for i, address in enumerate(payload_addresses): cpu.mem_write(address, payload[i*1056:(i+1)*1056])
                cpu.mem_write(0x49a04e, struct.pack('<H', cache['cursor']))
                tick = struct.unpack_from('<I', blob(entry['exit_dgroup']), 0x4e17b4-0x494000)[0]
                b.windows.ticks = [tick]*8
                if enabled: b.pulos.pop(aff, None); b.fronteiras.pop(aff, None)
                else: b.pulos[aff], b.fronteiras[aff] = skipped
                esp = PILHA+0x8000; cpu.mem_write(esp, struct.pack('<I', RETORNO))
                for register, value in dict(EAX=0, EDX=0, EBX=0, ECX=0, ESP=esp).items():
                    cpu.reg_write(getattr(original.x86, 'UC_X86_REG_'+register), value)
                cap.phase_frame = entry['frame']; cpu.ctl_flush_tb()
                out = BancadaCargaMissaoOriginal._correr(b, 'glyph-enabled-AffGame', b.sym['AffGame'], {}, (RETORNO,), retomar=True)
                assert out['EIP'] == RETORNO and out['ESP'] == esp+4
                captured = cap.rows.pop(); cap.phase_frame = None
                outputs.append(captured)
            old, new = outputs
            assert old['after'] == entry['after'] and old['blits'] == entry['blits'], (name, entry['frame'], 'baseline restoration')
            # Earlier real glyphs legitimately change a later call's incoming
            # surface and raster offset. The original request itself must agree.
            requests=lambda row:[{k:v for k,v in call.items() if k not in ('surface_before','blits_before')}
                                 for call in row['text_boundaries']]
            assert requests(new)==requests(old)
            for key in (new['after'], new['exit_dgroup']): blobs[key] = cap.blobs[key]
            rows.append(dict(source=name, frame=entry['frame'], baseline_equal=True,
                before=entry['before'], after=new['after'], exit_dgroup=new['exit_dgroup'],
                blits=new['blits'], text_calls=len(new['text_boundaries']),
                text_requests=requests(new),
                changed_pixels=sum(x != y for x, y in zip(blob(entry['after']), zlib.decompress(base64.b64decode(cap.blobs[new['after']]))))))
            cap.blobs.clear()
            if len(rows)%50 == 0: print('original glyph-enabled surfaces', len(rows), flush=True)
            if time.monotonic()-started > 1000: raise RuntimeError('Native budget exhausted')
    result = dict(schema='rising-lands/affgame-native-glyphs/1', method=__doc__,
        executable_sha256=__import__('emulador').HASH_ORIGINAL, code_sha256=b.sha256_codigo(),
        source_sha256=sha(Path(__file__).read_bytes()), inputs=sources,
        start_manifest_sha256=sha((Path(a.start)/'manifesto.json').read_bytes()),
        glyph_metrics=glyph_metrics, bitmap_pointer_table=hex(table),
        text_boundaries={n: dict(address=hex(b.sym[n]), declaration=b.fronteiras[b.sym[n]]) for n in ('InitTextLangue', 'TextGetMessage')},
        elapsed_seconds=time.monotonic()-started, rows=rows, blobs=blobs)
    output.write_bytes(lzma.compress(json.dumps(result).encode(), preset=3))
    print('native full surfaces', len(rows), 'text calls', sum(r['text_calls'] for r in rows), flush=True)


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--start', required=True)
    p.add_argument('--capture', action='append', required=True, help='owned native fixture filename:first-last')
    p.add_argument('--output', required=True); main(p.parse_args())
