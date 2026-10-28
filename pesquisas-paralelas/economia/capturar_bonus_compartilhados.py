"""Record immutable original intervals for the composed producer/world callback."""
import hashlib
import json
from pathlib import Path
import sys

PASTA=Path(__file__).resolve().parent
RAIZ=PASTA.parents[1]
sys.dont_write_bytecode=True
sys.path.insert(0,str(RAIZ.parent/'source/python'))
import pefile
from capturar_saida_tropa import HASH


def main():
    data=(RAIZ.parent/'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(data).hexdigest()!=HASH:raise ValueError('Original executable hash mismatch')
    catalog=json.loads((RAIZ/'relatorios/simbolos-originais.json').read_text())
    sbl=(RAIZ.parent/'source/cd/INSTALHD/RISING.SBL').read_bytes()
    if hashlib.sha256(sbl).hexdigest()!=catalog['sha256_sbl']:raise ValueError('Original symbol hash mismatch')
    pe=pefile.PE(data=data)
    im,base=pe.get_memory_mapped_image(),pe.OPTIONAL_HEADER.ImageBase
    ranges=[]
    for a,b,n in ((0x428878,0x428c8a,'BonusSetEngin'),(0x4475ef,0x447676,'EnginResetCapacite'),
                  (0x440d55,0x440d5e,'shared capacity-refresh return'),(0x4475ac,0x4475ef,'EnginTypeGetCapacite'),
                  (0x4474c5,0x4474c7,'shared capacity query return'),(0x428cc0,0x428e71,'BonusGetValEngin')):
        raw=im[a-base:b-base]
        ranges.append(dict(symbol=n,start=f'0x{a:08x}',end_exclusive=f'0x{b:08x}',
                           bytes_hex=raw.hex(),sha256=hashlib.sha256(raw).hexdigest()))
    result=dict(sha256_exe=HASH,sha256_sbl=catalog['sha256_sbl'],
        scope='Whole original setter/800-slot refresh/query composition; synthetic loaded buffers, no mission run',
        original_intervals=ranges,
        committed_providers=dict(core_refresh='d458ea71838ff3dc0e30dbc5ec027996e2976420',
                                 economy_queries='b1eb0c06e3b016f9abc2d27f3a836f6c20abf2f9',
                                 economy_setter='de6d6361aebcdb95e93ce60ee27e8e19e8fb8f5f'),
        native_query_checkpoint=dict(address='0x0044763a',condition='ECX low word equals failing unit index',
                                     indices=[0,7,799],effect='Stop before unsupported/failing bonus query, retaining earlier table/unit stores'))
    (PASTA/'evidencias/bonus-compartilhados.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Captured six original composed-call intervals and committed-provider references.')


if __name__=='__main__':main()
