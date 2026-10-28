"""Original selection branches: full body returns or declared overlay stops."""
import hashlib
import json
import struct
import time
from bancada_x86 import UNIDADE, RETORNO, SUPERFICIE, unicorn
from extrair_evidencias import RAIZ, HASH_EXE, imagem_pe, exigir_area_editavel
from graficos import Catalogo, ORDEM
from unidade_tipo2 import consultar_corpo_tipo2, compor_corpo_tipo2
from validar_unidade_tipo2 import BancadaTipo2, record, observed


def sha(data):return hashlib.sha256(data).hexdigest()


def selection(values):
    _,_,camera,mode,index,hover=values
    return dict(indice_u16=index,camera_u8=camera,indice_selecionado_u16=hover,modo_selecao_u8=mode)


def runtime_record(template,values):
    state,selected,_,_,index,_=values
    raw=bytearray(record(template,[state,16,7,8,0,0,64,48,index]));raw[0xbd]=selected
    return bytes(raw)


class BancadaSelecao(BancadaTipo2):
    def draw_selection(self,raw,values,*,pixels=False,shadow=None):
        args=selection(values);index=args['indice_u16'];pool=bytearray(800*276)
        pool[index*276:index*276+276]=raw;self.escrever(UNIDADE,pool)
        self.escrever(0x508041,bytes([args['camera_u8']]))
        self.escrever(0x508f8f,bytes([args['modo_selecao_u8']]))
        self.escrever(0x496ac2,struct.pack('<H',args['indice_selecionado_u16']))
        intervals=[(0x41591f,0x415a57),(0x412390,0x41374c),(0x410fcc,0x41209d),
            (0x442025,0x442065),(0x44fffe,0x45007a),(0x467d97,0x467da6)]
        stubs={address:lambda b:b.retornar_stub() for address in (0x45b247,0x45b796)}
        if pixels:
            background=bytes((i*17+23)%256 for i in range(128*128))
            self.preparar_superficie(128,128,background,(0,0,127,127),shadow)
            intervals += [(0x45b247,0x45b4fd)]+self.intervalos_sombra();stubs={}
        self.layers=[]
        result=self.executar(0x41591f,intervals,dict(EAX=64,EDX=48,EBX=index),
            stubs=stubs,paradas=[0x4124c4,0x410be4],limite=300000)
        assert self.ler(UNIDADE,len(pool))==bytes(pool)
        assert self.ler(0x508041,1)==bytes([args['camera_u8']])
        assert self.ler(0x508f8f,1)==bytes([args['modo_selecao_u8']])
        assert self.ler(0x496ac2,2)==struct.pack('<H',args['indice_selecionado_u16'])
        if result['EIP']==RETORNO:assert result['ESP']==0x2008004
        return result,list(self.layers),self.ler(SUPERFICIE,128*128) if pixels else b''


def validate():
    exigir_area_editavel();start=time.monotonic();b=BancadaSelecao();catalog=Catalogo();template=b.inicializar_tipo(2)
    base,image=imagem_pe();regions=[]
    for name,first,last in [('selection_prefix',0x4124a9,0x4124c4),('selection_tail',0x412a53,0x412a9f),
            ('image_camera',0x508041,0x508042),('image_selected_index',0x496ac2,0x496ac4),('image_mode',0x508f8f,0x508f90)]:
        data=image[first-base:last-base];regions.append(dict(name=name,start=hex(first),end=hex(last),bytes_hex=data.hex(),sha256=sha(data)))
    evidence=dict(exe_sha256=HASH_EXE,regions=regions,unchanged_reports={name:sha((RAIZ/name).read_bytes()) for name in ('validacao/x86-unidade-tipo2.json','evidencias/unidade-tipo2.json')})
    (RAIZ/'evidencias/selecao-tipo2.json').write_text(json.dumps(evidence,indent=2)+'\n')
    report=dict(exe_sha256=HASH_EXE,unicorn_version=unicorn.__version__,initial_record_hex=template.hex(),
        input_vector=['state_u8','selection_bd_u8','camera_u8','mode_u8','pool_index','selected_index_u16'],
        substitutions=dict(captures=['copy/shadow blitters intercepted'],pixels=[],bank_loading=['IO/allocation']),
        captures=[],pixels=[],limits=dict(instructions_per_call=300000,timeout_us=2000000))
    fixtures=[];seen=set()
    def add(values):
        if tuple(values) not in seen:seen.add(tuple(values));fixtures.append(values)
    for state in (2,7):
        for index in (0,799):
            for selected in (0,1,255):
                for camera in range(256):add([state,selected,camera,0,index,65535])
            for mode in range(256):add([state,0,0,mode,index,65535])
        for selected in range(256):
            for camera in (0,1):add([state,selected,camera,0,799,65535])
        for index in (0,1,799):
            for hover in (0,1,798,799,800,65535):add([state,0,0,0,index,hover])
    for values in fixtures:
        raw=runtime_record(template,values);native,layers,_=b.draw_selection(raw,values)
        try:plan=consultar_corpo_tipo2(raw,x=64,y=48,**selection(values))
        except NotImplementedError:assert native['EIP'] in (0x4124c4,0x410be4)
        else:assert native['EIP']==RETORNO and observed(plan)==layers
        report['captures'].append([values,hex(native['EIP']),layers,native['ESP']])
    b.carregar_banco_original({name:catalog._ler('cd/INSTALHD/GRAPHICS/'+name) for name in ORDEM})
    shadow=bytes.fromhex(json.loads((RAIZ/'validacao/x86-unidade-tipo2.json').read_text())['shadow_table_hex'])
    report['shadow_table_hex']=shadow.hex()
    for state in (2,7):
        for index in (0,799):
            for selected,camera in ((0,0),(0,255),(1,1),(255,255)):
                values=[state,selected,camera,0,index,65535];raw=runtime_record(template,values)
                native,layers,pixels=b.draw_selection(raw,values,pixels=True,shadow=shadow)
                background=bytes((i*17+23)%256 for i in range(128*128))
                out,plan=compor_corpo_tipo2(catalog,background,128,128,raw,x=64,y=48,tabela_sombra=shadow,**selection(values))
                assert native['EIP']==RETORNO and pixels==out and layers==observed(plan)
                report['pixels'].append(dict(input=values,sha256=sha(pixels)))
    report.update(result='PASS',bounded_executions=b.execucoes,instructions=b.instrucoes,
        full_capture_returns=sum(row[1]==hex(RETORNO) for row in report['captures']),
        expected_selection_prefix_stops=sum(row[1]=='0x4124c4' for row in report['captures']),
        expected_selection_info_stops=sum(row[1]=='0x410be4' for row in report['captures']),
        expected_exceptions=0,expected_limits=0,skips=0,seconds=round(time.monotonic()-start,3))
    parts=[]
    for key,value in report.items():
        encoded=('[\n'+',\n'.join('    '+json.dumps(v,separators=(',',':')) for v in value)+'\n  ]' if key=='captures' else json.dumps(value,indent=2))
        parts.append('  '+json.dumps(key)+': '+encoded)
    (RAIZ/'validacao/x86-selecao-tipo2.json').write_text('{\n'+',\n'.join(parts)+'\n}\n')
    print('PASS:',len(fixtures),'selection captures;',len(report['pixels']),'indexed buffers;',b.execucoes,'native calls',flush=True)


if __name__=='__main__':validate()
