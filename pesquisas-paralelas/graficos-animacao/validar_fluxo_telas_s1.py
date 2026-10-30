"""Compare each captured result/objectives drawing phase, including the original menu animation."""
import argparse,json
from pathlib import Path
from graficos import Catalogo
from telas_fluxo_s1 import compor_affgame_s1,BancoInventeS1
from validar_objetivos_s1 import CapturaTelaS1,AQUI,sha

def validar(path):
    cap=CapturaTelaS1(path);catalog=Catalogo();menu=BancoInventeS1(catalog);rows=[];assets={}
    for phase in cap.d['phases']:
        if phase['phase']!='between_frames' or not 17033<=phase['frame']<=17050:continue
        m=cap.memory(phase);mode=m.u8(0x4e2f78)
        assert mode==(0x13 if phase['frame']<=17043 else 0x11)
        # The query result is fixture input from the native research record, never a default in the compositor.
        branch=m.u8(0x5080f8) if mode==0x11 else None
        if mode==0x11:
            ident=1+(m.u16(0x508f84)&15);raw=menu.quadro(ident).comprimido;digest=sha(raw)
            matches=[name for name,v in phase['entry_blocks'].items() if v['sha256']==digest and v['bytes']==len(raw)]
            assert len(matches)==1,(ident,matches)
            assets[str(ident)]=dict(payload_sha256=digest,native_allocation=matches[0],bytes=len(raw))
        out=compor_affgame_s1(m,cap.blob(phase['before']),catalogo=catalog,catalogo_menu=menu,
            ramo_pesquisa_u16=branch)
        expected=cap.blob(phase['after']);pixels=sum(a!=b for a,b in zip(out['pixels'],expected))
        arguments=out['chamadas']!=phase['blits']
        assert not(pixels or arguments),(phase['frame'],pixels,arguments)
        rows.append(dict(frame=phase['frame'],screen='result' if mode==0x13 else 'objectives',equal=True,
            pixel_mismatches=pixels,argument_mismatches=int(arguments),drawing_calls=len(out['chamadas']),sha256=sha(out['pixels'])))
    assert len(rows)==18
    return dict(schema='rising-lands/s1-affgame-screen-comparison/1',cases=len(rows),equal=len(rows),mismatches=0,
        counts={name:sum(r['screen']==name for r in rows) for name in ('result','objectives')},
        boundary_contract='native INVENTE.CMP menu bank and STRAT glyph bank; no MenuInit or background claim',
        menu_asset_matches=assets,
        capture_sha256=sha(cap.raw),sources_sha256={name:sha((AQUI/name).read_bytes()) for name in
            ('telas_fluxo_s1.py','texto_bitmap_nativo.py','telas_objetivos_s1.py','validar_fluxo_telas_s1.py')},rows=rows)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--capture',default=str(AQUI/'evidencias/s1-telas-finais-nativas.json.xz'))
    p.add_argument('--output',required=True);a=p.parse_args();d=validar(a.capture)
    Path(a.output).write_text(json.dumps(d,indent=1)+'\n');print(d['counts'],'equal;',d['mismatches'],'mismatches')
