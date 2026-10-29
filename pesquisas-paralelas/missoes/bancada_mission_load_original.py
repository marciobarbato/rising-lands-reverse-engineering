"""Light Stage12 scaffold for an intact whole-MissionLoad oracle.

No native execution occurs on import. No default fixture, allocator, player
type, file, profile, or Python MissionLoad composition is installed here.
This scaffold itself has not been run natively or accepted as a whole-load oracle.
"""
from dataclasses import dataclass,fields
import hashlib
import time
import ambiente_missoes
from bancada_terreno_estruturas_missao import BancadaTerrenoEstruturasMissao
from estado_herdado_missao import EstadoHerdadoMissao
from vinculos_declarados import ArgumentoVinculo
from emulador import RETORNO


@dataclass(frozen=True)
class FronteirasExternasCargaMissao:
    fopen:object
    fread:object
    fclose:object
    file_seek:object
    global_alloc:object
    global_lock:object
    global_handle:object
    global_unlock:object
    global_free:object
    profile_int:object
    profile_string:object
    proveniencia:str

    def validar(self):
        if not self.proveniencia or any(not callable(getattr(self,f.name))
                                       for f in fields(self) if f.name!='proveniencia'):
            raise ValueError('Every external boundary needs an explicit identified handler')


@dataclass(frozen=True)
class LimitesOraculoCargaMissao:
    segundos:float
    segmentos:int
    vinculos:int
    instrucoes_por_segmento:int

    def __post_init__(self):
        if (not 0<self.segundos<=300 or not 0<self.segmentos<=10000 or
                not 0<self.vinculos<=10000 or not 0<self.instrucoes_por_segmento<=1000000):
            raise ValueError('Declare finite bounded oracle limits before execution')


class BancadaMissionLoadOriginal(BancadaTerrenoEstruturasMissao):
    # Additional original loop heads; registers, flags and stack are retained
    # by the committed Core segmentation machinery, with no synthetic CALL/RET.
    pontos_retomada=BancadaTerrenoEstruturasMissao.pontos_retomada+(
        0x46c3ea,0x42eee1,0x42ef22,0x42efd9,0x42f0e2)

    def __init__(self,heranca,fronteiras,*,arenas_externas,limites):
        if not isinstance(heranca,EstadoHerdadoMissao) or not isinstance(limites,LimitesOraculoCargaMissao):
            raise ValueError('Provide actual declared inherited state and finite limits')
        aliases=heranca.validar_fechamento_m1()
        fronteiras.validar()
        super().__init__()
        # Replace every game-state block created by the lower fixture harness;
        # none of its synthetic construction bytes may be consumed implicitly.
        for name,(base,end) in self.blocos.items():
            self.cpu.mem_write(base,bytes(heranca.vista(base,end-base)))
        existing=[(a,z+1) for a,z,_ in self.cpu.mem_regions()]
        for bloco in heranca.blocos:
            base,end=bloco.endereco,bloco.endereco+len(bloco.dados)
            if any(a<=base and end<=z for a,z in existing):
                self.cpu.mem_write(base,bytes(bloco.dados));continue
            if base%4096 or len(bloco.dados)%4096 or any(base<z and a<end for a,z in existing):
                raise ValueError('Extra inherited allocations must be whole nonoverlapping mapped pages')
            self.cpu.mem_map(base,len(bloco.dados));self.cpu.mem_write(base,bytes(bloco.dados))
            existing.append((base,end));self.blocos[bloco.nome]=(base,end)
        # External allocation contents/addresses are explicit inputs too. The
        # owner maintains handle<->locked-pointer<->live-buffer identity.
        for bloco in arenas_externas:
            base,end=bloco.endereco,bloco.endereco+len(bloco.dados)
            if (base%4096 or len(bloco.dados)%4096 or bloco.nome in self.blocos or
                    any(base<z and a<end for a,z in existing)):
                raise ValueError('Declare unique nonoverlapping external arena pages')
            self.cpu.mem_map(base,len(bloco.dados));self.cpu.mem_write(base,bytes(bloco.dados))
            existing.append((base,end));self.blocos[bloco.nome]=(base,end)
        self.heranca=heranca;self.proveniencia_herdada=heranca.manifesto()
        self.aliases=aliases;self.limites=limites
        self.fronteiras=fronteiras;self._inicio=None;self._segmento_inicial=0
        self.declarar_vinculo(0x48c71f,'CRT.fopen',('EAX','EDX'),fronteiras.fopen,natureza='io')
        self.declarar_vinculo(0x48c97b,'CRT.fread',('EAX','EDX','EBX','ECX'),fronteiras.fread,natureza='io')
        self.declarar_vinculo(0x48c80b,'CRT.fclose',('EAX',),fronteiras.fclose,natureza='io')
        # This inventoried I/O wrapper has no global store; the explicit
        # handler consumes offset EAX/origin DL and live stream[4e1d1c].
        self.declarar_vinculo(0x45848b,'FileSeek',('EAX',ArgumentoVinculo('EDX',8)),
                             fronteiras.file_seek,natureza='io')
        for slot,name,argc,handler in (
                (0x5231c0,'GlobalAlloc',2,fronteiras.global_alloc),
                (0x5231d0,'GlobalLock',1,fronteiras.global_lock),
                (0x5231cc,'GlobalHandle',1,fronteiras.global_handle),
                (0x5231d8,'GlobalUnlock',1,fronteiras.global_unlock),
                (0x5231c8,'GlobalFree',1,fronteiras.global_free),
                (0x5231ac,'GetPrivateProfileIntA',4,fronteiras.profile_int),
                (0x5231b0,'GetPrivateProfileStringA',6,fronteiras.profile_string)):
            self.declarar_importacao(slot,name,argc,handler)
        self.intervalos_oraculo=tuple(self.vinculos_declarados.codigo_protegido)
        self.entrada_herdada=self.estado()

    def _conferir_endereco(self,cpu,endereco,tamanho,_):
        if self._inicio is not None:
            if self.execucoes-self._segmento_inicial>self.limites.segmentos:
                raise RuntimeError('Whole-load declared segment budget exhausted; state retained')
            if time.monotonic()-self._inicio>self.limites.segundos:
                raise RuntimeError('Whole-load declared total wall budget exhausted; state retained')
        return super()._conferir_endereco(cpu,endereco,tamanho,_)

    def executar_original(self,*,paradas):
        """Requires a separate explicit heavy grant; caller must save failure/partial state."""
        self._inicio=time.monotonic();self._segmento_inicial=self.execucoes
        try:
            return self.executar(0x46c2cf,self.intervalos_oraculo,parada={RETORNO,*paradas},
                limite_instrucoes=self.limites.instrucoes_por_segmento,
                limite_vinculos=self.limites.vinculos)
        finally:
            self._inicio=None

    def resumo_oraculo(self):
        return dict(inherited=self.proveniencia_herdada,aliases=self.aliases,
            state_sha256={name:hashlib.sha256(data).hexdigest() for name,data in self.estado().items()},
            external_fixture=self.fronteiras.proveniencia,imports=self.importacoes_declaradas,
            bound_events=self.vinculos_declarados.eventos,binding_resumes=self.retomadas_vinculos,
            bounded_segments=self.execucoes,whole_load_python_composed=False,m1_accepted=False)
