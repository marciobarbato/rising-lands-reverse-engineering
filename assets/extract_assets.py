#!/usr/bin/env python3
"""Deterministic, lossless game-content export using committed reference readers.

No emulation or game behavior. Inputs are read-only; only a new destination is
written. --check rebuilds every expected byte through the same readers and
compares it to the complete published directory (including the manifest).
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import wave

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
OWNED = Path(__file__).resolve().parent
MAX_PART_BYTES = 32 * 1024 * 1024
ASSETS_REPOSITORY = 'https://github.com/marciobarbato/rising-lands-assets.git'
INVENTORY_SHA256 = 'd5057f3fae7f24d87e423856040962fdd09fbe4e80b9a0905726e9bbc7340211'
ORIGINAL_SHA256 = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')


def load_module(relative, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def decoder_info(relative, entrypoint):
    commit = subprocess.check_output(['git', 'log', '-1', '--format=%H', '--', relative], cwd=ROOT, text=True).strip()
    if len(commit) != 40:
        raise ValueError('UnknownDecoderCommit: ' + relative)
    return dict(module=relative, commit=commit, sha256=sha((ROOT / relative).read_bytes()), entrypoint=entrypoint)


def pcm_wave(data, channels, bits, rate):
    if bits not in (8, 16) or channels not in (1, 2) or not rate:
        raise ValueError('UnsupportedPcmWaveFormat')
    alignment = channels * (bits // 8)
    if len(data) % alignment:
        raise ValueError('IncompletePcmFrame')
    output = io.BytesIO()
    with wave.open(output, 'wb') as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(bits // 8)
        wav.setframerate(rate)
        wav.writeframes(data)
    encoded = output.getvalue()
    with wave.open(io.BytesIO(encoded), 'rb') as wav:
        if wav.readframes(wav.getnframes()) != data:
            raise ValueError('WaveRoundTripMismatch')
    return encoded


def lossless_pcm_parts(data,channels,bits,rate):
    if bits not in (8,16) or channels not in (1,2):
        raise ValueError('UnsupportedPcmWaveFormat')
    complete=len(data)-(len(data)%(channels*(bits//8)))
    encoded=pcm_wave(data[:complete],channels,bits,rate)
    tail=data[complete:]
    with wave.open(io.BytesIO(encoded),'rb') as wav:
        if wav.readframes(wav.getnframes())+tail!=data:
            raise ValueError('PcmTailRoundTripMismatch')
    return encoded,tail


class Inputs:
    def __init__(self, root, inventory=None, inventory_path=None):
        self.root = Path(root).resolve()
        if inventory is None:
            if inventory_path is None:
                raise ValueError('SourceInventoryRequired')
            if not Path(inventory_path).is_file() or Path(inventory_path).is_symlink():
                raise ValueError('SourceInventoryMissing')
            raw=Path(inventory_path).read_bytes()
            if sha(raw)!=INVENTORY_SHA256:
                raise ValueError('SourceInventoryIdentityMismatch')
            inventory=json.loads(raw)
        self.inventory = inventory
        self.records = {row['path']: row for row in self.inventory['files']}

    def read(self, relative):
        row = self.records[relative]
        path = (self.root / relative).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError('EscapingInputPath: ' + relative)
        data = path.read_bytes()
        if len(data) != row['bytes'] or sha(data) != row['sha256']:
            raise ValueError('SourceIdentityMismatch: ' + relative)
        return data

    def verify(self):
        actual = {p.relative_to(self.root).as_posix() for p in self.root.rglob('*') if p.is_file()}
        if actual != set(self.records):
            raise ValueError('SourceInventoryMismatch')
        for relative in sorted(self.records):
            self.read(relative)

    def source(self, relative, offset=0, length=None):
        row = self.records[relative]
        length = row['bytes'] - offset if length is None else length
        if offset < 0 or length < 0 or offset + length > row['bytes']:
            raise ValueError('SourceRangeOutsideFile: ' + relative)
        return dict(path=relative, sha256=row['sha256'], bytes=row['bytes'], offset=offset, length=length)


class Writer:
    def __init__(self, output, check, manifest_path=None):
        if Path(output).is_symlink():
            raise ValueError('RefusingSymlinkExtractionDirectory')
        self.output, self.check = Path(output).resolve(), check
        self.manifest_path=Path(manifest_path).resolve() if manifest_path else self.output/'manifest.json'
        if not check and (self.manifest_path.exists() or self.manifest_path.is_symlink()):
            raise ValueError('RefusingExistingManifest')
        self.outputs = []
        self.seen = set()
        if check:
            if not self.output.is_dir():
                raise ValueError('MissingExtractionDirectory')
        else:
            if self.output.exists() or self.output.is_symlink():
                raise ValueError('RefusingExistingExtractionDirectory')
            self.output.mkdir(parents=True)

    def emit(self, relative, data, source, decoder, kind, proof, **metadata):
        if len(data) > MAX_PART_BYTES:
            raise ValueError('OutputRequiresSplitting: ' + relative)
        if relative in self.seen:
            raise ValueError('DuplicateOutput: ' + relative)
        self.seen.add(relative)
        destination = self.output / relative
        if not destination.resolve().is_relative_to(self.output):
            raise ValueError('EscapingOutputPath')
        if self.check:
            if destination.is_symlink() or destination.read_bytes() != data:
                raise ValueError('OutputByteMismatch: ' + relative)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open('xb') as stream:
                stream.write(data)
        record = dict(path=relative, bytes=len(data), sha256=sha(data), source=source,
                      decoder=decoder, category=kind, proof=proof, **metadata)
        self.outputs.append(record)
        return record

    def finish(self, manifest):
        data = canonical(manifest)
        path = self.manifest_path
        if self.check:
            if path.is_symlink() or path.read_bytes() != data:
                raise ValueError('ManifestByteMismatch')
            actual = {p.relative_to(self.output).as_posix() for p in self.output.rglob('*') if p.is_file()}
            expected=self.seen | ({'manifest.json'} if path==self.output/'manifest.json' else set())
            if actual != expected:
                raise ValueError('UnmanifestedOrMissingOutput')
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            with path.open('xb') as stream:
                stream.write(data)


def export_graphics(inputs, writer, counts):
    relative = 'pesquisas-paralelas/graficos-animacao/graficos.py'
    graphics = load_module(relative, 'assets_reference_graphics')
    class ExplicitCatalog(graphics.Catalogo):
        def _ler(self, relative):
            if not relative.startswith('cd/'):
                raise ValueError('NonCdCatalogDependency')
            data = inputs.read(relative[3:])
            expected = next((row['sha256'] for row in self.manifesto if row['copia'] == 'fontes/' + relative), None)
            if sha(data) != expected:
                raise ValueError('GraphicsCatalogIdentityMismatch')
            return data
    catalog = ExplicitCatalog(ROOT / 'pesquisas-paralelas/graficos-animacao/fontes')
    for source in sorted(p for p in inputs.records if p.endswith('.CMP')):
        raw = inputs.read(source)
        name = Path(source).name
        frames = catalog.banco(name) if name in graphics.ORDEM else graphics.ler_cmp(raw)
        base = 'graphics/' + Path(source).stem
        indices, opacity, records = bytearray(), bytearray(), []
        for index, frame in enumerate(frames):
            records.append(dict(index=index, width=frame.largura, height=frame.altura,
                                decoded_offset=len(indices), decoded_bytes=len(frame.pixels),
                                source_header_offset=frame.offset_cabecalho,
                                source_header_bytes=8, source_payload_offset=frame.offset_cabecalho + 8,
                                source_payload_bytes=len(frame.comprimido), compressed_sha256=sha(frame.comprimido),
                                indices_sha256=sha(frame.pixels), opacity_sha256=sha(frame.opacidade)))
            if raw[frame.offset_cabecalho + 8:frame.offset_cabecalho + 8 + len(frame.comprimido)] != frame.comprimido:
                raise ValueError('CmpSourceOffsetMismatch')
            indices.extend(frame.pixels)
            opacity.extend(frame.opacidade)
        decoder = decoder_info(relative, 'Catalogo.banco -> ler_cmp' if name in graphics.ORDEM else 'ler_cmp')
        index_path = base + '/frames.json'
        for plane, data in [('indices.u8', indices), ('opacity.u8', opacity)]:
            writer.emit(base + '/' + plane, bytes(data), inputs.source(source), decoder, 'decoded_graphics_plane',
                        dict(kind='native_decoder_output_byte_equality', frame_count=len(frames)),
                        format='u8 row-major concatenated frames; see frames.json', offset_table=index_path)
        writer.emit(index_path, canonical(dict(frames=records, bank=name,
                    anchors_and_clipping='Not encoded in CMP; supplied by the game renderer, never defaulted here',
                    palette='../../palettes/PLATGAME.rgb8', opacity='0 transparent skip,255 opaque; literal index0 can be opaque')),
                    inputs.source(source), decoder, 'decoded_graphics_index',
                    dict(kind='native_decoder_metadata_and_source_ranges_equal'), format='json')
        counts['decoded_graphics_banks'] += 1
        counts['decoded_graphics_frames'] += len(frames)
    for source in sorted(p for p in inputs.records if p.endswith('.PIE')):
        raw = inputs.read(source)
        palette = graphics.ler_paleta(raw)
        writer.emit('palettes/' + Path(source).stem + '.rgb8', palette, inputs.source(source, 9, 768),
                    decoder_info(relative, 'ler_paleta'), 'decoded_palette',
                    dict(kind='native_decoder_output_byte_equality', transform='first RGB black; remaining VGA6 bytes shifted left2 modulo256'),
                    format='256 RGB triplets,8-bit, no gamma')
        counts['decoded_palettes'] += 1


def export_audio(inputs, writer, counts):
    audio = ROOT / 'pesquisas-paralelas/audio'
    sys.path.insert(0, str(audio))
    env = load_module('pesquisas-paralelas/audio/ambiente_audio.py', 'ambiente_audio')
    env.CD = inputs.root
    env.SOUND = inputs.root / 'INSTALHD/SOUND'
    replay = load_module('pesquisas-paralelas/audio/reproduzir_som.py', 'assets_reference_audio_replay')
    metadata = []
    for letter in 'ABP':
        content = {}
        case = replay.reproduzir_banco(letter, conteudos=content)
        capture_path = 'pesquisas-paralelas/audio/evidencias/captura-som-banco-' + letter + '.json'
        capture = json.loads((ROOT / capture_path).read_text())
        if capture['original_sha256'] != ORIGINAL_SHA256 or not capture['created_before_translation']:
            raise ValueError('OriginalAudioProvenanceMismatch')
        if case['surfaces_from_file'] != capture['surfaces_from_file']:
            raise ValueError('OriginalAudioCaptureMismatch: ' + letter)
        hed_source, snd_source = ['INSTALHD/SOUND/' + letter + '.' + extension for extension in ('HED','SND')]
        hed, snd = inputs.read(hed_source), inputs.read(snd_source)
        for sound in case['surfaces_from_file']:
            header = bytes.fromhex(sound['data_header_hex'])
            offset, size, channels, bits, rate, fmt, unknown, alignment = struct.unpack('<IIBBHBBH', header)
            header_offset = 16 + sound['data_header_offset']
            if hed[header_offset:header_offset + 16] != header:
                raise ValueError('HedSourceOffsetMismatch')
            buffer = bytes(content[(sound['index'],sound['variant'])])
            if sha(buffer) != sound['buffer_sha256']:
                raise ValueError('NativeAudioBufferHashMismatch')
            written = sound['decoder_returns'][0] if sound['decoder_returns'] else size
            if written < 0 or written > len(buffer) or sound['stop'] is not None:
                raise ValueError('IncompleteAudioDecode')
            pcm = buffer[:written]
            path = 'audio/' + letter + '/%04d-v%02d.wav' % (sound['index'],sound['variant'])
            module = 'pesquisas-paralelas/audio/adpcm_som.py'
            decoder = decoder_info(module, 'criar_superficie_som; ' + ('decodificar_ima_mono16' if channels==1 else 'decodificar_ima_estereo16') if fmt==4 else 'criar_superficie_som PCM copy')
            encoded,tail=lossless_pcm_parts(pcm,channels,bits,rate)
            tail_path=path+'.incomplete-frame-tail.bin' if tail else None
            if tail:
                writer.emit(tail_path,tail,inputs.source(snd_source,offset,size),decoder,
                            'decoded_audio_incomplete_tail',dict(kind='native_decoder_output_slice_equal',
                            decoded_output_offset=len(pcm)-len(tail),native_written_sha256=sha(pcm)),
                            format='uninterpreted incomplete PCM frame bytes; append to WAV data for exact native output')
                counts['audio_incomplete_frame_tails']+=1
            writer.emit(path, encoded, inputs.source(snd_source, offset, size), decoder,
                        'decoded_audio_sample', dict(kind='wav_pcm_plus_incomplete_tail_equals_native_decoder_written_bytes',
                        incomplete_frame_tail=tail_path,incomplete_frame_tail_bytes=len(tail),
                        pcm_sha256=sha(pcm), native_buffer_sha256=sound['buffer_sha256'], original_capture=capture_path,
                        original_capture_sha256=sha((ROOT / capture_path).read_bytes())),
                        related_sources=[inputs.source(hed_source,16+12*sound['index'],12), inputs.source(hed_source,header_offset,16)],
                        format='RIFF WAVE PCM; original rate/channels/bit depth',
                        decoded_bytes=written, unwritten_tail_bytes_not_exported=len(buffer)-written,
                        bank=letter, index=sound['index'],variant=sound['variant'],id=sound['id'], data_header_hex=sound['data_header_hex'])
            metadata.append(dict(bank=letter,index=sound['index'],variant=sound['variant'],id=sound['id'],wave=path,
                                 hed_header_offset=header_offset,snd_offset=offset,snd_bytes=size,
                                 channels=channels,bits=bits,sample_rate=rate,format=fmt,block_align=alignment,
                                 byte_0d=unknown,decoded_bytes=written,decoded_sha256=sha(pcm),incomplete_frame_tail=tail_path,incomplete_frame_tail_bytes=len(tail)))
            counts['decoded_audio_samples'] += 1
            counts['original_audio_buffers_equal'] += 1
        writer.emit('audio/' + letter + '/header.hex.json', canonical(dict(source=hed_source,hex=hed.hex())),
                    inputs.source(hed_source), decoder_info('assets/extract_assets.py','identity_hex_transport'),
                    'opaque_audio_header', dict(kind='hex_reencodes_to_original_bytes'), format='json full HED bytes as hex')
    writer.emit('audio/samples.json', canonical(metadata), [inputs.source('INSTALHD/SOUND/' + l + '.' + ext) for l in 'ABP' for ext in ('HED','SND')],
                decoder_info('pesquisas-paralelas/audio/reproduzir_som.py','reproduzir_banco'),
                'decoded_audio_index', dict(kind='native_decoder_metadata_equal'), format='json')


def export_worlds(inputs, writer, counts, dependencies):
    sys.path.insert(0,str(ROOT/'ferramentas'))
    relative='ferramentas/formatos.py'
    formats=load_module(relative,'assets_reference_world_formats')
    for source in sorted(p for p in inputs.records if Path(p).suffix.upper() in ('.ETA','.NET')):
        raw=inputs.read(source)
        try:
            decoded=formats.ler_eta(raw)
        except formats.ErroFormato as error:
            dependencies.append(dict(source=source,dependency='world_format_outside_validated_reader',detail=str(error)))
            continue
        writer.emit('worlds/'+source+'.json',canonical(decoded),inputs.source(source),decoder_info(relative,'ler_eta'),
                    'decoded_world',dict(kind='canonical_json_equals_native_reader_output'),format='json',
                    source_bytes_preserved_separately=True)
        counts['structured_worlds']+=1


def export_preserved(inputs,writer,counts,dependencies):
    handled={'.CMP','.HED','.SND'}
    text={'.TXT','.INI','.RUL'}
    opaque_dependencies={'.PIE':'pie_picture_pixels','.LZS':'lzs_picture_pixels','.FNT':'font_glyph_layout',
                         '.FLC':'flc_frame_decode','.AVI':'avi_frame_decode'}
    for source,row in sorted(inputs.records.items()):
        if row['category']!='game_resource' or Path(source).suffix.upper() in handled:
            continue
        raw=inputs.read(source); extension=Path(source).suffix.upper()
        if extension in text:
            decoded=raw.decode('latin-1');transport=decoded.encode('utf-8')
            if transport.decode('utf-8').encode('latin-1')!=raw:
                raise ValueError('TextRoundTripMismatch')
            writer.emit('text/'+source+'.utf8.txt',transport,inputs.source(source),
                        decoder_info('assets/extract_assets.py','reversible_latin1_byte_transport'),
                        'reversible_text',dict(kind='utf8_to_latin1_equals_original_bytes'),
                        format='UTF8 reversible Latin1 byte mapping; original Windows code page not asserted')
            counts['reversible_text_files']+=1
            continue
        parts=[]
        for index,offset in enumerate(range(0,len(raw),MAX_PART_BYTES)):
            data=raw[offset:offset+MAX_PART_BYTES]
            path='preserved/'+source+'.part-%04d.bin'%index
            writer.emit(path,data,inputs.source(source,offset,len(data)),decoder_info('assets/extract_assets.py','identity_copy'),
                        'opaque_preserved_part',dict(kind='byte_identical_original_source_slice'),
                        format='opaque original bytes',part=index)
            parts.append(dict(path=path,offset=offset,bytes=len(data),sha256=sha(data)))
        reassembled=hashlib.sha256()
        for part in parts:
            reassembled.update((writer.output/part['path']).read_bytes())
        if reassembled.hexdigest()!=row['sha256']:
            raise ValueError('PreservedSourceReassemblyMismatch')
        for record in writer.outputs[-len(parts):]:
            record['proof']['whole_source_reassembly_sha256']=reassembled.hexdigest()
        counts['preserved_sources']+=1
        counts['preserved_parts']+=len(parts)
        if extension in opaque_dependencies:
            dependencies.append(dict(source=source,dependency=opaque_dependencies[extension],
                                     detail='Opaque bytes preserved exactly; not counted as decoded pictures/glyphs/video frames'))
        elif extension not in ('.ETA','.NET'):
            dependencies.append(dict(source=source,dependency='opaque_format_semantics',detail='Preserved bytes; no new structure inferred'))


def extract(cd_root,output,check=False,manifest_path=None,inventory_path=None):
    inputs=Inputs(cd_root,inventory_path=inventory_path);inputs.verify()
    if Path(output).resolve().is_relative_to(inputs.root) or (manifest_path and Path(manifest_path).resolve().is_relative_to(inputs.root)):
        raise ValueError('InputOutputRootOverlap')
    writer=Writer(output,check,manifest_path);counts=Counter();dependencies=[]
    export_graphics(inputs,writer,counts)
    export_audio(inputs,writer,counts)
    export_worlds(inputs,writer,counts,dependencies)
    export_preserved(inputs,writer,counts,dependencies)
    counts['source_inventory_files']=len(inputs.records)
    counts['selected_source_files']=sum(r['category']=='game_resource' for r in inputs.records.values())
    counts['outputs']=len(writer.outputs)
    manifest=dict(schema='rising-lands/extracted-assets/1',content_root=os.path.relpath(writer.output,writer.manifest_path.parent),source_inventory_sha256=sha(Path(inventory_path).read_bytes()),
                  source_inventory='source-inventory.json',max_part_bytes=MAX_PART_BYTES,
                  counts=dict(counts),total_output_payload_bytes=sum(r['bytes'] for r in writer.outputs),
                  decoder_dependencies=dependencies,outputs=writer.outputs,
                  scope='Runtime/campaign/shell media, original game font/documentation; installation/platform binaries excluded',
                  proof_scope='Validated unchanged Python decoder output; original audio buffer captures checked. Opaque slices are exact originals, not semantic decodes.',
                  no_native_emulation=True)
    writer.finish(manifest)
    return {k:v for k,v in manifest.items() if k not in ('outputs','decoder_dependencies')}


def git_value(root,*arguments):
    result=subprocess.run(['git','-C',str(root),*arguments],capture_output=True,text=True)
    if result.returncode:
        raise ValueError('AssetsGitIdentityUnavailable: '+' '.join(arguments))
    return result.stdout.strip()


def repository_identity(data_root):
    data_root=Path(data_root).resolve()
    if not data_root.is_dir():
        raise ValueError('AssetsCheckoutMissing')
    top=Path(git_value(data_root,'rev-parse','--show-toplevel')).resolve()
    if top!=data_root:
        raise ValueError('AssetsCheckoutRootMismatch')
    url=git_value(data_root,'config','--get','remote.origin.url')
    if url.removesuffix('.git')!=ASSETS_REPOSITORY.removesuffix('.git'):
        raise ValueError('AssetsRepositoryMismatch')
    return data_root


def load_origin(path=None):
    path=Path(path or OWNED/'ORIGIN.json')
    if not path.is_file() or path.is_symlink():
        raise ValueError('AssetsOriginMissing')
    try:
        origin=json.loads(path.read_bytes())
        required=('repository','release_tag','release_commit','tag_object','manifest_sha256','source_inventory_sha256')
        if origin['schema']!='rising-lands/assets-origin/1' or any(not isinstance(origin[k],str) for k in required):
            raise ValueError('schema')
        import re
        for key,width in [('release_commit',40),('tag_object',40),('manifest_sha256',64),('source_inventory_sha256',64)]:
            if not re.fullmatch('[0-9a-f]{%d}'%width,origin[key]):raise ValueError(key)
        if not re.fullmatch('v[0-9]+-[a-z0-9-]+',origin['release_tag']):raise ValueError('tag')
        if origin['repository']!=ASSETS_REPOSITORY:raise ValueError('repository')
    except (KeyError,ValueError,TypeError) as error:
        raise ValueError('InvalidAssetsOriginPin') from error
    return origin


def verify_data_checkout(data_root,origin):
    data_root=repository_identity(data_root)
    if origin['repository']!=ASSETS_REPOSITORY:
        raise ValueError('AssetsRepositoryPinMismatch')
    if git_value(data_root,'rev-parse','HEAD')!=origin['release_commit']:
        raise ValueError('AssetsCommitMismatch')
    ref='refs/tags/'+origin['release_tag']
    try:
        tag_object=git_value(data_root,'rev-parse','--verify',ref)
        tag_commit=git_value(data_root,'rev-parse','--verify',ref+'^{commit}')
    except ValueError as error:
        raise ValueError('AssetsReleaseTagMissing') from error
    if git_value(data_root,'cat-file','-t',ref)!='tag':
        raise ValueError('AssetsReleaseTagNotAnnotated')
    if tag_object!=origin['tag_object'] or tag_commit!=origin['release_commit']:
        raise ValueError('AssetsReleaseTagMismatch')
    manifest=data_root/'manifest.json'
    inventory=data_root/'source-inventory.json'
    if not manifest.is_file() or manifest.is_symlink():raise ValueError('AssetsManifestMissing')
    if sha(manifest.read_bytes())!=origin['manifest_sha256']:
        raise ValueError('AssetsManifestPinMismatch')
    if not inventory.is_file() or inventory.is_symlink():raise ValueError('AssetsSourceInventoryMissing')
    if sha(inventory.read_bytes())!=origin['source_inventory_sha256']:
        raise ValueError('AssetsSourceInventoryPinMismatch')
    parsed=json.loads(manifest.read_bytes())
    if parsed.get('content_root')!='data' or parsed.get('source_inventory')!='source-inventory.json':
        raise ValueError('AssetsManifestLayoutMismatch')
    if parsed.get('source_inventory_sha256')!=origin['source_inventory_sha256']:
        raise ValueError('AssetsInventoryManifestBindingMismatch')
    if git_value(data_root,'status','--porcelain','--untracked-files=all'):
        raise ValueError('AssetsCheckoutModified')
    return origin


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cd-root',type=Path,required=True)
    parser.add_argument('--data-root',type=Path,required=True)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data_root=repository_identity(args.data_root)
    if args.check:
        verify_data_checkout(data_root,load_origin())
    result=extract(args.cd_root,data_root/'data',args.check,data_root/'manifest.json',data_root/'source-inventory.json')
    if args.check:
        verify_data_checkout(data_root,load_origin())
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
