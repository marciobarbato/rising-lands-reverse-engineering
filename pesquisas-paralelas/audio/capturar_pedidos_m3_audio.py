"""Original-only M3 sound requests and bounded raid access audit. Use heavy lease."""
import argparse
from collections import Counter
import copy
import hashlib
import json
import lzma
import signal
import struct
import sys
import time

import ambiente_audio
from ambiente_audio import ROOT, OWNED, ORIGINAL_SHA256
from audio_m22_soundness import capture_input, accepted_states, range_bytes, SOUND_RANGES, SHARED_RANGES

MISSIONS = ROOT/'pesquisas-paralelas/missoes'
sys.path.insert(0, str(MISSIONS))
PART = MISSIONS/'evidencias/m2-3/captura-quadros9200-monde01-exibicao-v2.parte09.json.xz'


def sha(data): return hashlib.sha256(data).hexdigest()


def leaves():
    from capturar_fila_audio import run_case
    from audio_queue_fixtures import QueueFixtureMemory
    capture = capture_input()
    phase, state = list(accepted_states(capture))[-1]
    core_path = ROOT/'evidencias/selecao-ordens/captura-selecao-ordens-exibicao.json'
    core = json.loads(core_path.read_bytes())
    requests = []
    for case in core['cases']:
        for e in case['boundaries']:
            if e['routine'] in ('PlaySnd_PostSound', 'PlaySnd_StopSound'):
                requests.append((case['case'], e))
    results = []
    for number, (label, e) in enumerate(requests):
        regs = {k: int(v, 16) for k,v in e['registers'].items()}
        post = e['routine'] == 'PlaySnd_PostSound'
        reference = regs['EBX' if post else 'EAX']
        # Caller bytes come from the accepted frame-128 state, not the Core
        # bench's synthetic case stores. Only request arguments are reused.
        value = range_bytes(state, reference, reference+4)
        regions = [(a, bytearray(range_bytes(state,a,z))) for a,z,_ in SOUND_RANGES]
        regions.append((reference, bytearray(value)))
        f = dict(name=f'display-{number}-{label}', operation='post' if post else 'stop_handle',
                 regs=regs, arguments=[int(e['stack_words'][0],16)] if post else [],
                 memory=QueueFixtureMemory(regions).snapshot(), com=[])
        # QueueNativeBench maps its declared fixture pages; real unit-reference
        # addresses are added explicitly below, without initializing any bank.
        from capturar_fila_audio import QueueNativeBench, ENTRIES, x86
        from emulador import mapear_paginas
        b = QueueNativeBench.__new__(QueueNativeBench)
        # Use the ordinary bench with its reference region temporarily absent.
        original_memory = f['memory']
        f['memory'] = original_memory[:-1]
        b.__init__(f)
        f['memory'] = original_memory
        page = reference & ~0xfff
        if not any(a <= page <= z for a,z,_ in b.cpu.mem_regions()):
            mapear_paginas(b.cpu, [page])
        b.cpu.mem_write(reference, value)
        stop = None
        try:
            out = b.executar(ENTRIES[f['operation']], [(0x489dac,0x48c204)], regs,
                            pilha={4:struct.pack('<I',f['arguments'][0])} if post else {},
                            limite_instrucoes=20000)
            eax = hex(out['EAX'])
        except Exception as exc:
            stop = dict(type=type(exc).__name__, detail=str(exc), eip=hex(b.cpu.reg_read(x86.UC_X86_REG_EIP)))
            eax = None
        results.append(dict(name=f['name'], operation=f['operation'], input=f, output=b.snapshot(),
                            eax=eax, stop=stop, reference_value=value.hex()))
    return dict(schema='rising-lands/audio-m3-original-requests/1', original_sha256=ORIGINAL_SHA256,
                translation_executed=False, state_phase=phase, state_capture_sha256=sha(capture_input_bytes()),
                argument_capture_sha256=sha(core_path.read_bytes()),
                domain='Accepted frame-128 private state and caller handle words; declared Core request arguments',
                cases=results)


def capture_input_bytes():
    from audio_m22_soundness import CAPTURE
    return CAPTURE.read_bytes()


def display_bench():
    from fronteiras_carga_missao import EntradasNomeadas
    from oraculo_quadro_missao import EntradasQuadro
    from oraculo_exibicao_missao import EntradasExibicao, BancadaExibicaoOriginal
    ni = json.loads((MISSIONS/'evidencias/captura-carga-missao-exibicao-v2.json').read_bytes())['named_inputs']
    base = EntradasNomeadas(diretorio_instalacao=ni['install_directory'].encode('latin-1'),
        unidade_cd=ni['cd_drive'].encode(), rotulo_cd=ni['cd_volume_label'].encode('latin-1'),
        relogio_ms=tuple(ni['clock_ms']), preenchimento_alocacao=ni['allocation_fill'],
        estado_memoria=bytes.fromhex(ni['memory_status_hex']), teclas=tuple(map(tuple,ni['async_keys'])),
        id_thread=ni['thread_id'], proveniencia=ni['provenance'])
    frame=EntradasQuadro(base=base,cursor=tuple(ni['frame']['cursor']),
        registradores_chamador={k:int(v,16) for k,v in ni['frame']['caller_registers'].items()},
        proveniencia=ni['frame']['provenance'])
    d=ni['display']
    return BancadaExibicaoOriginal(EntradasExibicao(quadro=frame,ticks=tuple(d['display_ticks']),
        preenchimento_superficie=d['surface_fill'],proveniencia=d['provenance']),segundos=300)


def audit(limit=None):
    """Re-enter each original phase from its committed input, retaining boundaries.

    This is a bounded phase replay, not a resumable whole-engine checkpoint.
    Exact output summaries and request boundaries must equal the source.
    """
    from delta_estado_missao import _decodificar, aplicar, resumo
    from emulador import unicorn, x86
    from audio_m22_soundness import memory_width_audit
    raw = lzma.decompress(PART.read_bytes()); part = json.loads(raw)
    state = {n:(int(v['base'],16),_decodificar(v)) for n,v in part['opening_state']['full_state'].items()}
    if resumo(state) != part['opening_state']['summary']: raise ValueError('Opening state identity')
    b = display_bench(); b.iniciar_relogio(); b.executar_inicio(); b.executar_mission_load(60)
    b._ganchar_quadros()
    # The accepted last part has no allocation/release. Retain its exact final
    # records, checked against each phase's count and opening block layout.
    records = copy.deepcopy(part['allocations'])
    if any(p['state_delta']['allocated'] or p['state_delta']['released'] for p in part['phases']):
        raise ValueError('Allocation changes require a real resumable snapshot')
    b.arena.ordem = [int(r['pointer'],16) for r in records]
    b.arena.recursos = {}
    for r in records:
        p = int(r['pointer'],16); r['pointer']=p; r['events']=r['events'].split()
        b.arena.recursos[p]=r
    b.arena.proximo=max(p+((r['size']+4095)&~4095) for p,r in b.arena.recursos.items())
    access=Counter(); stores=Counter(); rows=[]
    ranges=SOUND_RANGES+SHARED_RANGES
    def hook(counter):
        def observe(cpu,kind,a,n,value,_):
            ip=cpu.reg_read(x86.UC_X86_REG_EIP)
            for start,end,label in ranges:
                if a<end and start<a+n: counter[(b.fase,ip,a,n,label)]+=1
        return observe
    for a,z,_ in ranges:
        b.cpu.hook_add(unicorn.UC_HOOK_MEM_READ,hook(access),begin=a-15,end=z-1)
        b.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE,hook(stores),begin=a-15,end=z-1)
    b.cpu.ctl_flush_tb()
    for phase in part['phases'][:limit]:
        name=phase['phase']; expected=aplicar(state,phase['state_delta'],name)
        for a,data in state.values(): b.cpu.mem_write(a,data)
        for reg,value in phase['entry']['registers'].items():
            b.cpu.reg_write(getattr(x86,'UC_X86_REG_'+reg),int(value,16))
        esp=int(phase['entry']['registers']['ESP'],16)
        # The full-state format excludes native stack. Declare only the actual
        # return and WinMain/ProgIteration saved words already established by
        # the accepted bench contract; a summary mismatch stops the audit.
        if name.startswith('frame'):
            b.cpu.mem_write(esp,struct.pack('<I',0x475063))
            b._fase(name.replace('frame','between_frames',1))
        else:
            b.cpu.mem_write(esp+4,struct.pack('<4I',0x2007fe8,0,0,0x460212))
        b.windows.ticks=[int(x[2]) for x in phase['windows_answers'] if x[0]=='display_clock']
        start=len(b.eventos_fronteira)
        if name.startswith('frame'):
            b.executar_quadro(180,k=int(name[5:]))
        else:
            b._fase(name); b.limite_segundos=180; b.iniciar_relogio()
            b._correr(name,0x475063,{},(0x42c868,),retomar=True)
        actual=b.imagem()
        diffs=[]
        for block,(a,data) in expected.items():
            got=actual.get(block)
            if got != (a,data):
                if got is None or got[0]!=a or len(got[1])!=len(data): diffs.append([block,'layout'])
                else: diffs.extend([hex(a+i),old,new] for i,(old,new) in enumerate(zip(data,got[1])) if old!=new)
        events=b.eventos_fronteira[start:]
        equal_events=events==phase['boundaries']
        rows.append(dict(phase=name,summary_equal=resumo(actual)==phase['state_after']['summary'],
                         differences=diffs[:100],difference_count=len(diffs),boundaries_equal=equal_events))
        if not rows[-1]['summary_equal'] or not equal_events: break
        state=expected
        if len(rows)%40==0: print(json.dumps(dict(completed=len(rows),phase=name)),flush=True)
    def encode(counter):
        return [dict(phase=p,instruction=hex(ip),routine=b.nome(ip),address=hex(a),bytes=n,range=label,count=c)
                for (p,ip,a,n,label),c in sorted(counter.items())]
    return dict(schema='rising-lands/audio-m3-original-raid-accesses/1',original_sha256=ORIGINAL_SHA256,
                translation_executed=False,source_compressed_sha256=sha(PART.read_bytes()),source_raw_sha256=sha(raw),
                scope='Independent native phase re-entry, frames 8991..9200, declared accepted display boundaries',
                phases=rows,complete=len(rows)==len(part['phases']) and all(r['summary_equal'] and r['boundaries_equal'] for r in rows),
                reads=encode(access),writes=encode(stores),memory_width_audit=memory_width_audit(),
                code_sha256=b.sha256_codigo())


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('mode',choices=('leaves','audit'))
    parser.add_argument('--output',required=True); parser.add_argument('--limit',type=int)
    a=parser.parse_args(); path=ROOT/a.output
    if path.exists(): raise ValueError('Refusing evidence overwrite')
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('18-minute native budget')))
    signal.alarm(1080); start=time.monotonic()
    result=leaves() if a.mode=='leaves' else audit(a.limit)
    result['seconds']=round(time.monotonic()-start,3)
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(result,indent=1)+'\n')
    print(json.dumps(dict(output=str(path),seconds=result['seconds'],cases=len(result.get('cases',[])),complete=result.get('complete'))),flush=True)
    from encerramento_captura import encerrar_captura
    encerrar_captura(0,path)


if __name__=='__main__': main()
