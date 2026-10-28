"""Run original-only Stage 11 captures after the coordinator grants heavy work.

This defines the exporter without running it on import. No current-stage
Python traversal exists or is called. Prior integrated providers prepare
declared inputs only; all observed traversal/effect instructions run intact.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from ambiente_missoes import OWNED,CD
from casos_terreno_estruturas_missao import casos_captura_terreno_estruturas
from analisar import HASH_ESTUDADO


def capturar_consulta_numero_missao():
    """Four intact getter observations; no Python getter is called."""
    from emulador import BancadaX86
    original=BancadaX86()
    samples=[]
    for numero,vizinho,eax in ((0,255,0xa5a55a5a),(1,0,0x100ff00),
                               (127,255,0xffffffff),(255,1,0xffff00ff)):
        original.cpu.mem_write(0x496fe4,bytes([numero,vizinho]))
        antes=bytes(original.cpu.mem_read(0x494000,0x8f000))
        regs=original.executar(0x46c11a,[(0x46c11a,0x46c122)],dict(EAX=eax),
                              limite_instrucoes=1000)
        depois=bytes(original.cpu.mem_read(0x494000,0x8f000))
        if antes!=depois:
            raise ValueError('Original MissionGetNum unexpectedly changed global memory')
        samples.append(dict(mission_byte=numero,neighbor_byte=vizinho,input_eax=hex(eax),
                            output_eax=hex(regs['EAX']),output_ax=regs['EAX']&65535,
                            global_image_sha256=hashlib.sha256(depois).hexdigest()))
    return dict(original_entries=original.execucoes,cases=samples,
                scope='MissionGetNum46c11a: live byte496fe4; zero AH, retain high EAX16, never read neighbor')


def capturar(destino):
    if destino.exists():
        raise FileExistsError('Preserve the previous capture; choose a fresh output path')
    from bancada_terreno_estruturas_missao import BancadaTerrenoEstruturasMissao
    bancada=BancadaTerrenoEstruturasMissao()
    result=[]
    for caso in casos_captura_terreno_estruturas():
        bancada.carregar_caso(caso)
        entrada={nome:hashlib.sha256(dados).hexdigest() for nome,dados in bancada.antes.items()}
        regs=bancada.executar_caso(caso)
        result.append(dict(name=caso.nome,entry=caso.entrada,declared_stop=caso.parada,
            provenance=caso.economico.origem,
            input_sha256=entrada,output=bancada.resumo(),checkpoint=hex(regs['EIP'])))
    eta=(CD/'WORLD/MONDE01.ETA').read_bytes()
    report=dict(original_sha256=HASH_ESTUDADO,translation_executed=False,
        source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=OWNED,text=True).strip(),
        required_core_main='b610bfad77ffadaa0ee5f6af02160d786ccfdc7b',
        monde01_eta_sha256=hashlib.sha256(eta).hexdigest(),
        block_registry={nome:dict(base=hex(inicio),bytes=fim-inicio)
                        for nome,(inicio,fim) in bancada.blocos.items()},
        original_entries=bancada.entradas,returns=bancada.retornos,
        declared_dependency_stops=bancada.dependencias,bounded_segments=bancada.execucoes,
        minimap_resumes=bancada.retomadas_minimapa,loop_resumes=bancada.retomadas_laco,
        max_segment_instructions=getattr(bancada,'maximo_instrucoes',None),cases=result,
        mission_number_query=capturar_consulta_numero_missao(),
        scope='Original-only L8 structure scan and one joined MissionPlaceTerrain entry. Actual MONDE01 records plus explicit synthetic inherited physical/economic/selection/rule allocations. Every engine body intact, no external binding reached. Whole DGROUP+.bss and all declared non-stack fixture arenas hashed; no complete MissionLoad/remap or running mission claim.')
    destino.write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--saida',type=Path,
                        default=OWNED/'evidencias/captura-terreno-estruturas-missao-original.json')
    args=parser.parse_args()
    r=capturar(args.saida)
    print('Original entries:',r['original_entries'],'returns:',r['returns'],
          'dependency stops:',r['declared_dependency_stops'],'segments:',r['bounded_segments'])
