"""Static difficulty-candidate inventory. Never executes/emulates game code."""
import argparse
import bisect
import configparser
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys

OWNED = Path(__file__).resolve().parent
ROOT = OWNED.parents[1]
ORIGINAL_SHA256 = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
BASELINE = 'a7427fd0e416d212f08af7f0df3d36a224d12f2d'
CODE = (0x401000, 0x493c00)
PROFILE_FIELDS = {0x50a9bc:'HumanOnly',0x50a9c0:'ProbaCaveJoueur',0x50a9c4:'ProbaCaveIA',0x50a9c8:'ProbaEmbuscade'}
CALL_TARGETS = {0x47a601:'InitEntrerMonstre',0x47aba9:'ReadConfigMonstre',0x47b796:'ChargeMonstre',0x47fc54:'iaConfigGetValue',0x47f8b7:'iaSetMode'}
INTERVALS = [('InitEntrerMonstre',0x47a601,0x47a81d),('ReadConfigMonstre',0x47aba9,0x47ac30),
             ('LoadEntrerMonstre',0x47ac30,0x47ad6a),('AvanceMonstre_and_wait_response_prefix',0x47b283,0x47b6f1),
             ('ChargeMonstre',0x47b796,0x47b8e8),('LoadCalculMissionDivers',0x47c30f,0x47c359),
             ('iaConfigGetValue',0x47fc54,0x47fc57),('iaSetMode',0x47f8b7,0x47f8e7)]
REFERENCES = ['ferramentas/formatos.py','ferramentas/unidades.py','ferramentas/extrair_fundacoes_quadro.py',
              'ferramentas/regras.py','pesquisas-paralelas/missoes/carregador_cadeia_auxiliar.py',
              'pesquisas-paralelas/missoes/fim_missao.py','pesquisas-paralelas/ia-runtime/reinicio_ia.py',
              'pesquisas-paralelas/ia-runtime/incursao_ia.py','relatorios/simbolos-originais.tsv']


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_modules():
    sys.path.insert(0,str(ROOT/'ferramentas'))
    import formatos
    import extrair_fundacoes_quadro
    return formatos,extrair_fundacoes_quadro


def collect_missions(cd,formats):
    paths=sorted((cd/'WORLD').glob('MONDE*.ETA'))
    if len(paths)!=38:
        raise ValueError('MissionCorpusMismatch: expected38 MONDE*.ETA files')
    missions=[]
    for path in paths:
        data=path.read_bytes()
        decoded=formats.ler_eta(data) # unchanged committed format reader, read-only
        blocks={block['nome']:block for block in decoded['blocos']}
        monsters=blocks['tabela_47ac30']
        if (monsters['quantidade'],monsters['tamanho_registro'])!=(100,6):
            raise ValueError('MonsterRecordVariantMismatch: '+path.name)
        entries=[]
        for i in range(monsters['quantidade']):
            offset=monsters['offset']+4+i*6
            cell,mask,period=struct.unpack_from('<HHH',data,offset)
            if cell!=0xffff:
                entries.append(dict(index=i,file_offset=hex(offset),cell=hex(cell),group_mask=hex(mask),disk_period=period,
                                    loaded_u16_period=period*30&0xffff))
        conditions=blocks['tabela_458b05']
        if conditions['tamanho_registro']!=10:
            raise ValueError('ConditionRecordVariantMismatch: '+path.name)
        condition_entries=[]
        for i in range(conditions['quantidade']):
            offset=conditions['offset']+4+i*10
            kind,pad,*words=struct.unpack_from('<BB4H',data,offset)
            condition_entries.append(dict(index=i,file_offset=hex(offset),kind=kind,pad=pad,words=words))
        divers=blocks['bytes_descartados']
        missions.append(dict(path='WORLD/'+path.name,sha256=sha(data),bytes=len(data),
                             dimensions=[decoded['largura'],decoded['altura']],resources_by_type=decoded['recursos_por_tipo'],
                             monster_table=dict(file_offset=hex(monsters['offset']),count=100,disk_record_bytes=6,
                                                active_cell_records=len(entries),records=entries),
                             conditions=dict(file_offset=hex(conditions['offset']),records=condition_entries),
                             discarded16=dict(file_offset=hex(divers['offset']),raw_hex=data[divers['offset']:divers['fim']].hex()),
                             consumed_end=hex(decoded['fim_carregamento']),unconsumed_suffix=decoded['sufixo']))
    return missions


def collect_code(cd,reader):
    try:
        import capstone
    except ImportError as error:
        raise RuntimeError('StaticDependencyMissing: capstone5.0.7 (no emulator needed)') from error
    raw=(cd/'INSTALHD/RISING.EXE').read_bytes()
    if sha(raw)!=ORIGINAL_SHA256:
        raise ValueError('OriginalIdentityMismatch')
    symbols=sorted((int(a,16),name) for a,name in (line.split('\t') for line in (ROOT/'relatorios/simbolos-originais.tsv').read_text().splitlines()[1:]))
    starts=[address for address,_ in symbols]
    def label(address):
        index=bisect.bisect_right(starts,address)-1
        return symbols[index][1] if index>=0 else None
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
    md.detail=True;md.skipdata=True
    code=reader._bytes(raw,*CODE)
    field_refs=[];calls=[];instruction_count=0;skipped_bytes=0
    for ins in md.disasm(code,CODE[0]):
        if not ins.id:
            skipped_bytes+=ins.size
            continue
        instruction_count+=1
        for operand in ins.operands:
            if operand.type==capstone.x86.X86_OP_MEM and operand.mem.disp in PROFILE_FIELDS:
                field_refs.append(dict(address=hex(ins.address),bytes=ins.bytes.hex(),symbol=label(ins.address),
                                       instruction=ins.mnemonic+' '+ins.op_str,field=PROFILE_FIELDS[operand.mem.disp],
                                       absolute_field=not operand.mem.base and not operand.mem.index,access=operand.access))
        if ins.mnemonic in ('call','jmp') and ins.operands and ins.operands[0].type==capstone.x86.X86_OP_IMM:
            target=ins.operands[0].imm
            if target in CALL_TARGETS:
                calls.append(dict(address=hex(ins.address),bytes=ins.bytes.hex(),symbol=label(ins.address),instruction=ins.mnemonic+' '+ins.op_str,target=CALL_TARGETS[target]))
    intervals=[];lines=['; Static disassembly only; no original execution.','; Original SHA-256 '+ORIGINAL_SHA256]
    for name,start,end in INTERVALS:
        data=reader._bytes(raw,start,end)
        intervals.append(dict(name=name,start=hex(start),end_exclusive=hex(end),sha256=sha(data),bytes=len(data)))
        lines+=['','; '+name+' '+hex(start)+'..'+hex(end)+' sha256 '+sha(data)]
        lines += [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in md.disasm(data,start)]
    getter=reader._bytes(raw,0x47fc54,0x47fc57)
    if getter!=bytes.fromhex('89d8c3'):
        raise ValueError('ConfigStubMismatch')
    profile_strings=[]
    for address in [0x494e4c,0x494e5a,0x494e64,0x494e7a,0x494ea0,0x494ec2,0x494fc8,0x494fd3,0x4951f8,0x495203,0x495207,0x495214]:
        value=reader._bytes(raw,address,address+100).split(b'\0')[0]
        profile_strings.append(dict(address=hex(address),bytes=value.hex(),text=value.decode('cp1252')))
    return dict(original_sha256=sha(raw),capstone=capstone.__version__,text_interval=[hex(x) for x in CODE],
                text_sha256=sha(code),decoded_instructions=instruction_count,skipdata_bytes=skipped_bytes,
                scan_limit='Linear disassembly; exact absolute operands/direct calls only. Indexed forms separately labeled; indirect calls/alias writes and global UI absence are NOT proved.',
                profile_field_references=field_refs,direct_calls=calls,reviewed_intervals=intervals,
                config_getter=dict(address='0x47fc54',bytes=getter.hex(),effect='mov eax,ebx; ret; no config file or UI read'),
                original_strings=profile_strings), '\n'.join(lines)+'\n'


def collect(cd):
    formats,reader=read_modules()
    missions=collect_missions(cd,formats)
    code,assembly=collect_code(cd,reader)
    monstre=(cd/'INSTALHD/MONSTRE.INI').read_bytes()
    rising=(cd/'INSTALHD/RISING.INI').read_bytes()
    ini=configparser.ConfigParser(interpolation=None);ini.read_string(monstre.decode('cp1252'))
    rules=configparser.ConfigParser(interpolation=None);rules.read_string(rising.decode('cp1252').replace('\x1a',''))
    defaults={'HumanOnly':0,'ProbaCaveJoueur':5,'ProbaCaveIA':2,'ProbaEmbuscade':2}
    selected={section:{key:rules[section][key] for key in ('TMPSRECRUTE','RECHARGE','FATIGUE','TMPSCONSTRUCTION') if key in rules[section]}
              for section in rules.sections()}
    references=[]
    for relative in REFERENCES:
        data=(ROOT/relative).read_bytes()
        commit=subprocess.check_output(['git','log','-1','--format=%H','--',relative],cwd=ROOT,text=True).strip()
        references.append(dict(path=relative,sha256=sha(data),last_commit=commit))
    result=dict(schema='rising-lands/static-difficulty-scan/1',baseline_main=BASELINE,
                evidence_class='static original-byte and data inspection; no game behavior executed',
                references=references,mission_count=len(missions),missions=missions,
                monstre_ini=dict(path='INSTALHD/MONSTRE.INI',sha256=sha(monstre),bytes=len(monstre),
                                 keys=dict(ini['GENERAL']),missing_profile_keys=[key for key in defaults if key not in ini['GENERAL']],defaults=defaults),
                rising_ini=dict(path='INSTALHD/RISING.INI',sha256=sha(rising),bytes=len(rising),
                                selected_rate_values=selected,divers=dict(rules['DIVERS'])),code=code)
    return result,assembly


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cd',type=Path,required=True)
    parser.add_argument('--write',action='store_true',help='Create initial artifacts exclusively; never replace them')
    args=parser.parse_args()
    result,assembly=collect(args.cd)
    report=OWNED/'evidence/static-scan-v1.json';asm=OWNED/'evidence/reviewed-routines.asm'
    encoded=json.dumps(result,indent=2)+'\n'
    if args.write:
        if report.exists() or asm.exists():parser.error('Refusing to overwrite original research artifacts')
        report.parent.mkdir(parents=True,exist_ok=True)
        with report.open('x') as f:f.write(encoded)
        with asm.open('x') as f:f.write(assembly)
    elif json.loads(report.read_text())!=result or asm.read_text()!=assembly:
        raise SystemExit('StaticEvidenceMismatch: original/reference/artifact identity or scan changed')
    print(json.dumps(dict(passed=True,missions=len(result['missions']),profile_keys_missing=result['monstre_ini']['missing_profile_keys'],
                          absolute_profile_operands=sum(r['absolute_field'] for r in result['code']['profile_field_references']),
                          config_calls=sum(r['target']=='iaConfigGetValue' for r in result['code']['direct_calls']),
                          emulated_calls=0),indent=2))
    return 0


if __name__=='__main__':raise SystemExit(main())
