"""Original-only Audio/M2.2 dependency audit. No sound translation or playback.

Static bytes are exported from the intact PE. Native modes must run through the
coordinator's heavy lease. Accepted captures and policies are read-only inputs.
"""
import argparse
from collections import Counter
import hashlib
import json
import lzma
from pathlib import Path
import struct
import subprocess
import sys
import time

import ambiente_audio
from ambiente_audio import ROOT, OWNED, CD, ORIGINAL_SHA256
from extrair_som import simbolos, imagem, intervalo

CAPTURE = ROOT/'pesquisas-paralelas/missoes/evidencias/captura-quadros128-monde01-exibicao-v2.json.xz'
CAPTURE_SHA = '4c8f5c14a9623131dd019eafcdc49ea63054ee358f9defde58c12cb949f59ff3'
RAW_SHA = '1ad031b96300e5c632fd5b6b7857ae30792f78e86531e4f17d1bf7124c6dd930'
POLICY = ROOT/'pesquisas-paralelas/missoes/validacao/m2-2-politica-comparacao-128-quadros.json'
POLICY_SHA = 'bf36e6e8f6a38202fa3248256d3de9f768497caa835a563a3ef119be994127f0'
# Static sound records/table neighborhood, not the game's separate CD flags.
SOUND_RANGES = ((0x498f14, 0x498f6c, 'initialized_sound_scalars'),
                (0x521358, 0x522234, 'request_waiting_logical_physical_bank_state'))
SHARED_RANGES = ((0x496fdc, 0x496fe0, 'mci_clock_copy'),
                 (0x4e2f28, 0x4e2f34, 'game_cd_playing_and_mci_initialized_flags'),
                 (0x4e1d18, 0x4e1d1c, 'shared_random_permutation_cursor'))


def sha(data): return hashlib.sha256(data).hexdigest()


def capture_input():
    compressed = CAPTURE.read_bytes()
    if sha(compressed) != CAPTURE_SHA: raise ValueError('Accepted capture compressed identity mismatch')
    raw = lzma.decompress(compressed)
    if sha(raw) != RAW_SHA: raise ValueError('Accepted capture raw identity mismatch')
    if sha(POLICY.read_bytes()) != POLICY_SHA: raise ValueError('Accepted policy identity mismatch')
    return json.loads(raw)


def evidence_path(path):
    path = ROOT/path
    if path.exists(): raise ValueError('Refusing to overwrite evidence: '+str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def inventory(destination):
    from analisar import dependencias
    pefile, cs = dependencias()
    raw = (CD/'INSTALHD/RISING.EXE').read_bytes()
    if sha(raw) != ORIGINAL_SHA256: raise ValueError('Intact PE identity mismatch')
    pe = pefile.PE(data=raw)
    md = cs.Cs(cs.CS_ARCH_X86, cs.CS_MODE_32); md.detail = True
    symbols = simbolos()
    selected = [(a,n,z) for (a,n),(z,_) in zip(symbols,symbols[1:])
                if n.startswith('MCICD_') or 0x489dac <= a < 0x48c204]
    routines, lines = [], ['; Intact executable SHA-256 '+ORIGINAL_SHA256,
                          '; Static evidence only, not translated sound semantics.']
    for start,name,end in selected:
        stop, instructions = intervalo(pe, md, start, end)
        accesses = []
        lines.append('; '+name)
        for ins in instructions:
            lines.append(f'{ins.address:08x} {ins.bytes.hex():<24} {ins.mnemonic} {ins.op_str}'.rstrip())
            for operand in ins.operands:
                if operand.type == cs.x86.X86_OP_MEM and 0x400000 <= operand.mem.disp < 0x600000:
                    accesses.append(dict(instruction=hex(ins.address), address=hex(operand.mem.disp),
                        bytes=operand.size, read=bool(operand.access & cs.CS_AC_READ),
                        write=bool(operand.access & cs.CS_AC_WRITE),
                        indexed=bool(operand.mem.base or operand.mem.index), text=ins.mnemonic+' '+ins.op_str))
        routines.append(dict(name=name,start=hex(start),end=hex(stop),bytes=stop-start,
                             sha256=sha(imagem(pe,start,stop-start)),accesses=accesses))
    result=dict(schema='rising-lands/audio-m22-original-inventory/1',original_sha256=ORIGINAL_SHA256,
                translation_executed=False,scope='All symbol intervals MCICD_* and sound library 0x489dac..0x48c204',
                ranges=[dict(start=hex(a),end=hex(z),name=n) for a,z,n in SOUND_RANGES+SHARED_RANGES],
                routines=routines,source_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip())
    path=evidence_path(destination)
    path.write_text(json.dumps(result,indent=2)+'\n')
    path.with_suffix('.asm').write_text('\n'.join(lines)+'\n')
    return result


def accepted_states(capture):
    missions=ROOT/'pesquisas-paralelas/missoes'
    sys.path.insert(0,str(missions))
    from mapa_memoria_m1 import carregar_blocos, expandir_captura
    from delta_estado_missao import aplicar, resumo
    m1=expandir_captura(json.loads((missions/'evidencias/captura-carga-missao-exibicao-v2.json').read_bytes()),
                       json.loads((missions/'evidencias/entrada-carga-missao-exibicao-v2.json').read_bytes()))
    state=carregar_blocos(m1['oracle']['final_state']['blocks'])
    if resumo(state)!=capture['state_s0']['summary']: raise ValueError('Opening state mismatch')
    yield 'state_s0', state
    for phase in capture['phases']:
        state=aplicar(state,phase['state_delta'],phase['phase'])
        if resumo(state)!=phase['state_after']['summary']: raise ValueError('Phase summary mismatch')
        yield phase['phase'], state


def range_bytes(state,a,z):
    for base,data in state.values():
        if base<=a and z<=base+len(data): return data[a-base:z-base]
    raise ValueError(f'Uncaptured range {a:x}..{z:x}')


def native_pumps(destination):
    from emulador import BancadaX86, RETORNO, PILHA, unicorn, x86
    capture=capture_input()
    t0=time.monotonic()
    unique={}; state_count=0
    for phase,state in accepted_states(capture):
        state_count+=1
        values=tuple(range_bytes(state,a,z) for a,z,_ in SOUND_RANGES+SHARED_RANGES[:-1])
        key=sha(b''.join(values))
        unique.setdefault(key,dict(phases=[],state=state))['phases'].append(phase)
    cases=[]
    for key,group in unique.items():
        state=group['state']
        for name,address in [('PlaySnd_Manage',0x48aaca),('MCICD_Play',0x467a8c),('MCICD_Manage',0x467bf0)]:
            bench=BancadaX86()
            for a,z,_ in SOUND_RANGES+SHARED_RANGES:
                bench.cpu.mem_write(a,range_bytes(state,a,z))
            reads,writes,trace=Counter(),[],[]
            def read(cpu,kind,a,n,value,_):
                if a<PILHA or a>=PILHA+0x10000:
                    reads[(cpu.reg_read(x86.UC_X86_REG_EIP),a,n)]+=1
            def write(cpu,kind,a,n,value,_):
                if not PILHA<=a<PILHA+0x10000:
                    writes.append(dict(instruction=hex(cpu.reg_read(x86.UC_X86_REG_EIP)),address=hex(a),bytes=n,
                                       old=bytes(cpu.mem_read(a,n)).hex(),value=hex(value & ((1<<(8*n))-1))))
            def code(cpu,a,n,_): trace.append(a)
            bench.cpu.hook_add(unicorn.UC_HOOK_MEM_READ,read)
            bench.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE,write)
            bench.cpu.hook_add(unicorn.UC_HOOK_CODE,code)
            before={n:sha(range_bytes(state,a,z)) for a,z,n in SOUND_RANGES+SHARED_RANGES}
            stop=None
            try:
                result=bench.executar(address,[(0x4679d0,0x467cbf),(0x489dac,0x48c204)],limite_instrucoes=10000)
                registers={n:hex(v) for n,v in result.items() if isinstance(v,int)}
            except Exception as exc:
                stop=dict(type=type(exc).__name__,detail=str(exc));registers={}
            after={n:sha(bytes(bench.cpu.mem_read(a,z-a))) for a,z,n in SOUND_RANGES+SHARED_RANGES}
            cases.append(dict(routine=name,entry=hex(address),input_ranges_sha256=key,phases=group['phases'],
                              inherited_ranges_before=before,inherited_ranges_after=after,returned=stop is None,
                              stop=stop,registers=registers,reads=[dict(instruction=hex(ip),address=hex(a),bytes=n,count=c)
                              for (ip,a,n),c in sorted(reads.items())],writes=writes,
                              trace=[hex(a) for a in trace],instructions=len(trace)))
    result=dict(schema='rising-lands/audio-m22-original-pumps/1',original_sha256=ORIGINAL_SHA256,
                translation_executed=False,accepted_capture_sha256=CAPTURE_SHA,accepted_policy_sha256=POLICY_SHA,
                declared_input='No CD track playing; sound library and MCI CD initializer not executed',
                coverage=dict(states=state_count,distinct_input_range_images=len(unique),routine_calls=len(cases)),
                cases=cases,seconds=round(time.monotonic()-t0,3))
    path=evidence_path(destination);path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(output=str(path),coverage=result['coverage'],stops=sum(c['stop'] is not None for c in cases))))



def memory_width_audit():
    """Conservative static operand-width audit over the immutable original text.

    REP strings are observed element-by-element by Unicorn. Legacy x87 80-bit
    loads are wider than dwords; a 15-byte prefix conservatively covers them.
    """
    from analisar import dependencias
    pefile,cs=dependencias()
    raw=(CD/'INSTALHD/RISING.EXE').read_bytes()
    if sha(raw)!=ORIGINAL_SHA256:raise ValueError('Intact PE identity mismatch')
    text=pefile.PE(data=raw).get_data(0x1000,0x92c00)
    md=cs.Cs(cs.CS_ARCH_X86,cs.CS_MODE_32);md.detail=True;md.skipdata=True
    sizes=[];skipped=0
    for instruction in md.disasm(text,0x401000):
        if instruction.id==0:skipped+=instruction.size;continue
        sizes.extend(o.size for o in instruction.operands if o.type==cs.x86.X86_OP_MEM)
    maximum=max(sizes)
    if maximum>16:raise ValueError('Original text contains a wider operand; enlarge hook prefix')
    return dict(text_start='0x401000',text_bytes=len(text),text_sha256=sha(text),
                max_explicit_memory_operand_bytes=maximum,hook_backward_prefix=15,
                linear_skipdata_bytes=skipped,
                scope='Static original-text disassembly, including legacy x87. REP accesses are per element.')


def native_logic_reads(destination,frames,execute_pumps=False):
    """Run the original accepted scenario with sound/CD declared boundaries unchanged.

    This measures only native game accesses to the explicit static neighborhoods;
    it is not a claim about arbitrary initialized DirectSound heaps or code.
    """
    sys.path.insert(0,str(ROOT/'pesquisas-paralelas/missoes'))
    import ambiente_missoes
    import cenarios_oraculo as cen
    from emulador import unicorn,x86
    from mapa_memoria_m1 import carregar_blocos,expandir_captura
    capture=capture_input()
    width=memory_width_audit()
    m1=json.loads((ROOT/'pesquisas-paralelas/missoes/evidencias/captura-carga-missao-exibicao-v2.json').read_bytes())
    ni=m1['named_inputs']
    t0=time.monotonic()
    # Reuse the accepted declared Windows answers directly. The convenience
    # factory additionally reads an ISO PVD, unavailable in the authorized CD
    # tree; no ISO or volume-label guess is required for this exact replay.
    from fronteiras_carga_missao import EntradasNomeadas
    from oraculo_quadro_missao import EntradasQuadro
    from oraculo_exibicao_missao import EntradasExibicao, BancadaExibicaoOriginal
    base=EntradasNomeadas(diretorio_instalacao=ni['install_directory'].encode('latin-1'),
        unidade_cd=ni['cd_drive'].encode(),rotulo_cd=ni['cd_volume_label'].encode('latin-1'),
        relogio_ms=tuple(ni['clock_ms']),preenchimento_alocacao=ni['allocation_fill'],
        estado_memoria=bytes.fromhex(ni['memory_status_hex']),teclas=tuple(map(tuple,ni['async_keys'])),
        id_thread=ni['thread_id'],proveniencia=ni['provenance'])
    frame=EntradasQuadro(base=base,cursor=tuple(ni['frame']['cursor']),
        registradores_chamador={k:int(v,16) for k,v in ni['frame']['caller_registers'].items()},
        proveniencia=ni['frame']['provenance'])
    display=ni['display']
    entry=EntradasExibicao(quadro=frame,ticks=tuple(display['display_ticks']),
        preenchimento_superficie=display['surface_fill'],proveniencia=display['provenance'])
    b=BancadaExibicaoOriginal(entry,segundos=300)
    b.iniciar_relogio();b.executar_inicio();b.executar_mission_load(60)
    if b.resumo_imagem(b.imagem())!=capture['state_s0']['summary']: raise ValueError('Native initial state differs')
    if execute_pumps:
        for name in ('PlaySnd_Manage','MCICD_Play','MCICD_Manage'):
            address=b.sym[name]
            b.pulos.pop(address,None);b.fronteiras.pop(address,None)
        b.cpu.ctl_flush_tb()
    access=Counter();writes=Counter();executed=Counter()
    code_before=b.sha256_codigo()
    for name in ('PlaySnd_Manage','MCICD_Play','MCICD_Manage'):
        def reached(cpu,address,size,label):executed[label]+=1
        b.cpu.hook_add(unicorn.UC_HOOK_CODE,reached,name,begin=b.sym[name],end=b.sym[name])
    def hook(target):
        def capture_access(cpu,kind,a,n,value,_):
            for start,end,label in SOUND_RANGES+SHARED_RANGES:
                if a<end and start<a+n:
                    ip=cpu.reg_read(x86.UC_X86_REG_EIP)
                    target[(b.fase,ip,a,n,label)]+=1
        return capture_access
    for a,z,_ in SOUND_RANGES+SHARED_RANGES:
        b.cpu.hook_add(unicorn.UC_HOOK_MEM_READ,hook(access),None,begin=a-15,end=z-1)
        b.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE,hook(writes),None,begin=a-15,end=z-1)
    b.cpu.ctl_flush_tb()
    phases=[];expected={p['phase']:p for p in capture['phases']}
    references=iter(accepted_states(capture));next(references)
    stop=None;summary=capture['state_s0']['summary'];phase='state_s0'
    try:
        for phase,regs in b.executar_quadros(frames,segundos=180):
            actual=b.imagem();summary=b.resumo_imagem(actual)
            equal=summary==expected[phase]['state_after']['summary']
            name,reference=next(references)
            if name!=phase:raise ValueError('Reference order differs')
            differences=[]
            for block in sorted(set(actual)|set(reference)):
                if block=='native_stack':continue
                av,rv=actual.get(block),reference.get(block)
                if av==rv:continue
                if av is None or rv is None or av[0]!=rv[0] or len(av[1])!=len(rv[1]):
                    differences.append(dict(block=block,layout_differs=True));continue
                differences.extend(dict(block=block,address=hex(av[0]+i),accepted=old,actual=new)
                                   for i,(new,old) in enumerate(zip(av[1],rv[1])) if new!=old)
            phases.append(dict(phase=phase,summary_equal=equal,differences=differences))
            if not equal and not execute_pumps: raise ValueError('Native phase differs from accepted capture: '+phase)
            if execute_pumps and any(d.get('address')!='0x498f5c' for d in differences):
                raise ValueError('Chained pumps changed bytes outside the original pump write set: '+phase)
    except Exception as exc:
        stop=dict(type=type(exc).__name__,reason=str(exc),phase=phase,completed_phases=len(phases))
    def rows(counter):
        return [dict(phase=phase,instruction=hex(ip),routine=b.nome(ip),address=hex(a),bytes=n,range=label,count=count,
                             code_owner='sound-library' if 0x489dac<=ip<0x48c204 else 'mci-cd' if 0x4679d0<=ip<0x467cbf else 'game-or-display')
                for (phase,ip,a,n,label),count in sorted(counter.items())]
    result=dict(schema='rising-lands/audio-m22-original-native-accesses/1',original_sha256=ORIGINAL_SHA256,
                translation_executed=False,accepted_capture_sha256=CAPTURE_SHA,accepted_policy_sha256=POLICY_SHA,
                scope='Original native accesses in the M2.2 scenario',execute_original_pumps=execute_pumps,
                sound_boundaries_removed=['PlaySnd_Manage','MCICD_Play','MCICD_Manage'] if execute_pumps else [],
                declared_cd_input='No CD track playing, flag 0x4e2f28 stays zero; MCICD_Init never executed',
                frames=frames,phases=phases,reads=rows(access),writes=rows(writes),
                stop=stop,complete=stop is None and len(phases)==1+2*frames,
                memory_width_audit=width,original_pump_entries=dict(executed),code_sha256_before=code_before,
                boundary_counts=dict(Counter(e['routine'] for e in b.eventos_fronteira if e.get('phase') in expected)),
                declared_inputs_source='Exact named_inputs of the accepted display-v2 M1 capture; no new ISO-label inference',
                source_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                script_sha256=sha(Path(__file__).read_bytes()),
                watched_ranges=[dict(start=hex(a),end=hex(z),name=n) for a,z,n in SOUND_RANGES+SHARED_RANGES],
                start_summary=capture['state_s0']['summary'],end_summary=summary,
                code_sha256_after=b.sha256_codigo(),seconds=round(time.monotonic()-t0,3))
    path=evidence_path(destination);path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(output=str(path),frames=frames,phases=len(phases),seconds=result['seconds'])),flush=True)
    from encerramento_captura import encerrar_captura
    encerrar_captura(0 if stop is None else 1,path)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=('inventory','pumps','logic'))
    parser.add_argument('--output',required=True);parser.add_argument('--frames',type=int,default=128);parser.add_argument('--execute-pumps',action='store_true')
    args=parser.parse_args()
    if args.mode != 'inventory':
        import signal
        signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('18-minute native job limit')))
        signal.alarm(18*60)
    if args.mode=='inventory': print('Exported',len(inventory(args.output)['routines']),'original intervals')
    elif args.mode=='pumps':native_pumps(args.output)
    else:native_logic_reads(args.output,args.frames,args.execute_pumps)


if __name__=='__main__':main()
