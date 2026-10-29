"""Validate graph structure and every cited call/table/type byte against intact PE."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import struct
import zlib
from extrair_mapa_acoes_bytes import OriginalPE, INTACT_SHA, hx

OWNED=Path(__file__).resolve().parent


def require(value,detail):
    if not value:raise ValueError(detail)


def check_graph(graph,pe):
    require(graph['schema']=='rising-lands/monde01-player-action-static-graph/1','Wrong graph schema')
    require('static only' in graph['scope'],'Graph must preserve static-only scope')
    require(graph['intact_executable_sha256']==INTACT_SHA,'Graph executable identity mismatch')
    nodes={n['id']:n for n in graph['nodes']}
    require(len(nodes)==len(graph['nodes']),'Duplicate graph node')
    for node in nodes.values():
        address=int(node['address'],16)
        pe.offset(address)
        if node['kind']=='import_slot':require(address in pe.imports,'Unknown PE import slot')
        require(node['runtime_reachability'].startswith('not established'),'Node overclaims reachability')
    for edge in graph['edges']:
        require(edge['source'] in nodes and edge['target'] in nodes,'Dangling graph edge')
        site,target=int(edge['site'],16),int(edge['target_address'],16)
        raw=bytes.fromhex(edge['bytes_hex'])
        require(pe.read(site,len(raw))==raw,'Graph edge bytes differ from intact PE')
        require(int(nodes[edge['target']]['address'],16)==target,'Graph target address differs from node')
        if edge['kind']=='direct_e8':
            require(len(raw)==5 and raw[0]==0xe8,'Not an E8 instruction')
            require(site+5+struct.unpack('<i',raw[1:])[0]==target,'Relative call target differs')
            pe.offset(target)
        elif edge['kind']=='iat_indirect':
            require(raw[-6:-4]==b'\xff\x15','Not an absolute indirect IAT call')
            require(struct.unpack('<I',raw[-4:])[0]==target,'IAT instruction slot differs')
            require(pe.imports[target]==edge['target'],'IAT symbol differs')
        else:raise ValueError('Unreviewed edge kind')
    dispatch=graph['command_dispatch']
    require(dispatch['table_address']=='0x0045ed20','Unexpected command table')
    cases=dispatch['cases']
    require([c['code_u16'] for c in cases]==list(range(40)),'Wrong command index/order')
    table=struct.unpack('<40I',pe.read(0x45ed20,160))
    require(pe.read(0x45eddb,4).hex()=='6683fa27','Command upper-bound guard differs')
    require(pe.read(0x45edeb,8).hex()=='2eff249520ed4500','Command indirect dispatch differs')
    for case,target in zip(cases,table):
        require(int(case['table_entry'],16)==0x45ed20+4*case['code_u16'],'Wrong table-entry address')
        require(int(case['branch'],16)==target,'Command table target differs')
        require(0x45edc0<=target<0x45f32b,'Command dispatch escapes known routine')
        for call in case['possible_calls']:
            raw=bytes.fromhex(call['hex']);site=int(call['site'],16)
            require(pe.read(site,5)==raw,'Command call bytes differ')
            require(site+5+struct.unpack('<i',raw[1:])[0]==int(call['target'],16),'Command call target differs')
    for action in graph['actions']:
        require(action['successful_MONDE01_effect']=='not proven','Action overclaims successful effect')
        require(all(n in nodes for n in action['stages']),'Action references an absent node')
        require(all(0<=c<40 for c in action['commands']),'Action references absent command')
        for site in action['producer_sites']:
            raw=pe.read(int(site,16),5)
            require(raw[0]==0xe8 and int(site,16)+5+struct.unpack('<i',raw[1:])[0]==0x45ecd4,'Producer is not a SetPlayerOrdre call')
    for branch in graph['end_of_mission']['branches']:
        raw=bytes.fromhex(branch['bytes_hex']);site=int(branch['site'],16)
        require(pe.read(site,len(raw))==raw,'Transition branch bytes differ')
        if raw[0]==0xe9:target=site+5+struct.unpack('<i',raw[1:])[0]
        elif len(raw)==2:target=site+2+struct.unpack('<b',raw[1:])[0]
        else:raise ValueError('Unsupported transition branch encoding')
        require(target==int(branch['target'],16),'Transition branch target differs')
    return dict(nodes=len(nodes),edges=len(graph['edges']),commands=len(cases),actions=len(graph['actions']))


def validate(exe,graph_path=None):
    pe=OriginalPE(exe)
    graph_path=Path(graph_path or OWNED/'callgraph.json')
    graph=json.loads(graph_path.read_text())
    for item in graph['provenance']:
        require(hashlib.sha256((OWNED/item['path']).read_bytes()).hexdigest()==item['sha256'],'Evidence hash mismatch')
    evidence=json.loads((OWNED/'evidencias/original-player-action-bytes.json').read_text())
    instruction_count=0;candidate_calls=0
    for routine in evidence['routines']:
        start,end=int(routine['address'],16),int(routine['end_exclusive'],16)
        raw=pe.read(start,end-start)
        require(raw.hex()==routine['hex'] and hashlib.sha256(raw).hexdigest()==routine['sha256'],'Routine byte extent differs')
        for instruction in routine['instructions']:
            raw=bytes.fromhex(instruction['hex']);site=int(instruction['address'],16)
            require(start<=site<end and pe.read(site,len(raw))==raw,'Instruction differs from original')
            instruction_count+=1
        for call in routine['calls']:
            site=int(call['site'],16);raw=bytes.fromhex(call['hex'])
            require(pe.read(site,len(raw))==raw,'Candidate call bytes differ')
            if call['kind']=='direct_e8':
                require(raw[0]==0xe8 and site+5+struct.unpack('<i',raw[1:])[0]==int(call['target'],16),'Candidate E8 target differs')
            candidate_calls+=1
    context=json.loads((OWNED/'evidencias/monde01-action-context.json').read_text())
    getter=context['unit_name_getter'];require(pe.read(int(getter['address'],16),len(bytes.fromhex(getter['hex']))).hex()==getter['hex'],'Unit name getter differs')
    for item in context['unit_type_records']+evidence['structure_type_records']:
        data=pe.read(int(item['address'],16),item['bytes'])
        require(data.hex()==item['hex'],'Type record differs')
        require(data[item['name_offset']:].split(b'\0',1)[0].decode('ascii')==item['name'],'Type name differs')
    from extrair_contexto_monde01_acoes import CAPTURE, CAPTURE_SHA
    m1=context['accepted_m1']
    require(m1['path']==CAPTURE and m1['sha256']==CAPTURE_SHA,'Context must use the accepted M1 identity')
    raw=(OWNED.parents[1]/m1['path']).read_bytes()
    require(hashlib.sha256(raw).hexdigest()==m1['sha256'],'M1 accepted reference differs')
    blocks=json.loads(raw)['oracle']['final_state']['blocks']
    def captured(address,size):
        for block in blocks.values():
            base=int(block['base'],16)
            if base<=address and address+size<=base+block['bytes']:
                data=zlib.decompress(base64.b64decode(block['zlib_base64']))
                require(hashlib.sha256(data).hexdigest()==block['sha256'],'Accepted M1 block hash differs')
                return data[address-base:address-base+size]
        raise ValueError('Context address is not captured')
    require(len(m1['condition_records'])==10,'Missing condition record')
    for item in m1['condition_records']:
        raw=bytes.fromhex(item['hex'])
        require(raw==captured(0x4e1d20+10*item['index'],10),'Condition bytes differ from accepted M1')
        require(raw[0]==item['type_u8'] and list(struct.unpack_from('<4H',raw,2))==item['parameters_u16'],'Condition field decoding differs')
    pool=struct.unpack('<I',captured(0x4e19a0,4))[0]
    require(int(m1['unit_pool_pointer'],16)==pool,'Unit pool pointer differs')
    require(m1['word_0x4e1a3a_hex']==captured(0x4e1a3a,2).hex(),'Condition override word differs')
    for unit in m1['initial_roster_first_16']:
        header=captured(pool+276*unit['index'],3)
        require(header.hex()==unit['header_hex'],'Roster header differs')
        require(list(header)==[unit['owner_u8'],unit['type_u8'],unit['state_u8']],'Roster field decoding differs')
    stats=check_graph(graph,pe)
    return dict(status='passed',scope='static/provenance validation only; no native emulation',intact_executable_sha256=INTACT_SHA,
                routines=len(evidence['routines']),instruction_bytes_checked=instruction_count,candidate_call_encodings_checked=candidate_calls,
                type_records_checked=5,**stats)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--exe',type=Path,required=True);p.add_argument('--graph',type=Path);p.add_argument('--output',type=Path)
    a=p.parse_args();result=validate(a.exe,a.graph)
    if a.output:a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
