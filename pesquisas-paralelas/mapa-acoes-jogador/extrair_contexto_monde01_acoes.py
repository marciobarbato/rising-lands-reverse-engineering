"""Read immutable original type bytes and accepted M1 condition/roster bytes."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import struct
import zlib
from extrair_mapa_acoes_bytes import OriginalPE, INTACT_SHA, hx

ROOT=Path(__file__).resolve().parents[2]
CAPTURE='pesquisas-paralelas/missoes/evidencias/captura-carga-missao-original-v2.json'
CAPTURE_SHA='eb7d2303e13e62d4f5692c9cb6ef302b573d138df6a8b51183a6d9b0bd703afc'


def extract(exe,output):
    pe=OriginalPE(exe)
    unit_records=[]
    for kind in (0,7,9):
        address=0x4965ae+50*kind; data=pe.read(address,50)
        unit_records.append(dict(type_u8=kind,address=hx(address),bytes=50,hex=data.hex(),name_offset=12,
                                 name=data[12:].split(b'\0',1)[0].decode('ascii'),evidence='original_file_bytes'))
    raw=(ROOT/CAPTURE).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=CAPTURE_SHA:raise ValueError('Accepted M1 capture identity mismatch')
    cap=json.loads(raw);blocks=cap['oracle']['final_state']['blocks']
    def read(address,n):
        for block in blocks.values():
            base=int(block['base'],16)
            if base<=address and address+n<=base+block['bytes']:
                data=zlib.decompress(base64.b64decode(block['zlib_base64']))
                if hashlib.sha256(data).hexdigest()!=block['sha256']:raise ValueError('M1 block identity mismatch')
                return data[address-base:address-base+n]
        raise ValueError('Uncaptured address')
    conditions=read(0x4e1d20,100)
    records=[dict(index=i,address=hx(0x4e1d20+i*10),hex=conditions[i*10:i*10+10].hex(),
                  type_u8=conditions[i*10],pad_u8=conditions[i*10+1],parameters_u16=list(struct.unpack_from('<4H',conditions,i*10+2))) for i in range(10)]
    pool=struct.unpack('<I',read(0x4e19a0,4))[0]
    roster=[]
    for i in range(16):
        record=read(pool+276*i,276)
        roster.append(dict(index=i,address=hx(pool+276*i),owner_u8=record[0],type_u8=record[1],state_u8=record[2],
                           header_hex=record[:3].hex()))
    briefing=Path(exe).parents[1]/'WORLD/MONDE01.TXT'
    # The briefing is corroborating player text, not a condition evaluator.
    result=dict(schema='rising-lands/monde01-action-context/1',intact_executable_sha256=INTACT_SHA,
        unit_name_getter=dict(address=hx(0x441775),end_exclusive=hx(0x441792),hex=pe.read(0x441775,0x1d).hex(),
                              formula='0x4965ae + 50 * (AL & 255) + 12',evidence='original_file_bytes'),
        unit_type_records=unit_records,
        accepted_m1=dict(path=CAPTURE,sha256=CAPTURE_SHA,scenario='MONDE01 new campaign original-v2',
                         evidence='accepted_original_reference_bytes_not_a_new_action_execution',
                         conditions_address=hx(0x4e1d20),condition_records=records,
                         word_0x4e1a3a_hex=read(0x4e1a3a,2).hex(),unit_pool_pointer=hx(pool),
                         initial_roster_first_16=roster),
        briefing=dict(path='WORLD/MONDE01.TXT',sha256=hashlib.sha256(briefing.read_bytes()).hexdigest(),
                      role='corroborating player-visible objective text only'))
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--exe',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();extract(a.exe,a.output)
