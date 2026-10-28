"""Comparações opcionais e delimitadas; nunca inicializa o jogo ou Windows.

Derivada da infraestrutura commitada de ferramentas/emulador.py. Dependências
copiadas para esta pasta. Uso normal de graficos.py não importa este módulo.
"""
import struct
import sys
from extrair_evidencias import RAIZ, imagem_pe

sys.path.insert(0, str(RAIZ/'dependencias'))
import unicorn
from unicorn import x86_const as x86

UNIDADE = 0x1000000
PILHA = 0x2000000
RETORNO = 0x3000000
HEAP = 0x4000000
SUPERFICIE = 0x8000000


class Bancada:
    def __init__(self):
        base, imagem = imagem_pe()  # verifica SHA-256 antes de toda emulação
        self.cpu = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_32)
        self.cpu.mem_map(base, (len(imagem)+4095)//4096*4096)
        self.cpu.mem_write(base, imagem)
        for a, n in [(UNIDADE,0x40000), (PILHA,0x10000), (RETORNO,0x2000),
                     (HEAP,0x2000000), (SUPERFICIE,0x100000)]:
            self.cpu.mem_map(a,n)
        gdt = RETORNO+0x1000
        self.cpu.mem_write(gdt, struct.pack('<3Q',0,0x00cf9a000000ffff,0x00cf92000000ffff))
        self.cpu.reg_write(x86.UC_X86_REG_GDTR,(0,gdt,23,0))
        self.cpu.reg_write(x86.UC_X86_REG_CS,8)
        for nome in ('DS','ES','SS'):
            self.reg(nome,16)
        self.escrever(0x4e19a0,struct.pack('<I',UNIDADE))
        self.intervalos = []
        self.paradas = set()
        self.stubs = {}
        self.execucoes = 0
        self.instrucoes = 0
        self.proximo = HEAP
        self.cpu.hook_add(unicorn.UC_HOOK_CODE,self._hook)

    def reg(self,nome,valor=None):
        r = getattr(x86,'UC_X86_REG_'+nome.upper())
        if valor is None:
            return self.cpu.reg_read(r)
        self.cpu.reg_write(r,valor & 0xffffffff)

    def escrever(self,a,dados):
        self.cpu.mem_write(a,bytes(dados))

    def ler(self,a,n):
        return bytes(self.cpu.mem_read(a,n))

    def alocar(self,n):
        a=self.proximo; self.proximo += (n+3)//4*4
        if self.proximo >= HEAP+0x2000000:
            raise RuntimeError('Limite do heap isolado')
        return a

    def retornar_stub(self, eax=None):
        esp=self.reg('ESP')
        ret,=struct.unpack('<I',self.ler(esp,4))
        if eax is not None:
            self.reg('EAX',eax)
        self.reg('ESP',esp+4); self.reg('EIP',ret)

    def _hook(self,cpu,a,n,_):
        self.instrucoes += 1
        if a in self.paradas:
            cpu.emu_stop(); return
        if a in self.stubs:
            self.stubs[a](self); return
        if not any(inicio <= a and a+n <= fim for inicio,fim in self.intervalos):
            raise RuntimeError(f'Execução fora dos intervalos declarados: {a:#x}')

    def executar(self,entrada,intervalos,regs=None,paradas=(),stubs=None,limite=100000):
        if not 1 <= limite <= 1000000:
            raise ValueError('Limite de instruções inválido')
        self.execucoes += 1
        self.intervalos=intervalos
        self.paradas=set(paradas)|{RETORNO}
        self.stubs=stubs or {}
        for nome in ('EAX','EBX','ECX','EDX','ESI','EDI','EBP'):
            self.reg(nome,0)
        self.reg('EFLAGS',2); self.reg('ESP',PILHA+0x8000)
        self.escrever(PILHA,bytes(0x10000))
        self.escrever(PILHA+0x8000,struct.pack('<I',RETORNO))
        for nome,v in (regs or {}).items(): self.reg(nome,v)
        self.cpu.emu_start(entrada,RETORNO,timeout=2_000_000,count=limite)
        if self.reg('EIP') not in self.paradas:
            raise RuntimeError('Limite de tempo/instruções atingido antes da parada')
        return {nome:self.reg(nome) for nome in ('EAX','EBX','ECX','EDX','ESI','EDI','EBP','ESP','EIP')}

    def inicializar_soldado(self):
        return self.inicializar_tipo(0)

    def inicializar_tipo(self, tipo):
        unidade = bytearray(276)
        unidade[1] = tipo
        self.escrever(UNIDADE, unidade)
        self.executar(0x457350,[(0x457350,0x457b87)],{'EAX':0})
        return self.ler(UNIDADE,276)

    def carregar_banco_original(self,arquivos):
        """LoadSTRATBank original; somente IO/allocator substituídos explicitamente."""
        self.escrever(0x509494,b'\0')
        aberto=None; pos=0; aberturas=[]
        def abrir(b):
            nonlocal aberto,pos
            nome=b.ler(b.reg('EAX'),256).split(b'\0')[0].decode('ascii')
            chave=nome.replace('\\','/').split('/')[-1].upper()
            aberto=arquivos[chave];pos=0;aberturas.append(chave)
            b.retornar_stub(1)
        def ler(b):
            nonlocal pos
            n=b.reg('EDX')
            dados=aberto[pos:pos+n]
            if len(dados)!=n: raise RuntimeError('Leitura emulada truncada')
            b.escrever(b.reg('EAX'),dados);pos+=n;b.retornar_stub()
        def fechar(b): b.retornar_stub()
        def malloc(b): b.retornar_stub(b.alocar(b.reg('EAX')))
        regs=self.executar(0x41877a,[(0x41877a,0x4189c2)],
                            stubs={0x458420:abrir,0x458461:ler,0x45844c:fechar,0x467ea6:malloc},
                            limite=1000000)
        banco=regs['EAX']
        quantidade,=struct.unpack('<H',self.ler(banco,2))
        tabela,=struct.unpack('<I',self.ler(banco+4,4))
        self.executar(0x418590,[(0x418590,0x418599)],{'EAX':banco})
        return dict(banco=banco,tabela=tabela,quantidade=quantidade,aberturas=aberturas)

    def capturar_desenho(self,direcao,fase,estado=2,dx=0,dy=0,x=128,y=128,ate_blitter=False,
                        *,tipo=0,bolsa_u16=0,resto_bolsa=b'\0'*6):
        unidade=bytearray(self.inicializar_tipo(tipo))
        unidade[2]=estado;unidade[0x91]=direcao;unidade[0xa4]=fase
        struct.pack_into('<H',unidade,0xa,bolsa_u16)
        if len(resto_bolsa)!=6: raise ValueError('Seis bytes auxiliares da bolsa esperados')
        unidade[0xc:0x12]=resto_bolsa
        unidade[0x86]=dx&255;unidade[0x87]=dy&255
        self.escrever(UNIDADE,unidade)
        sombras=[]
        def sombra(b):
            sombras.append(dict(id_motor=b.reg('EBX')&65535,x=b.reg('EAX'),y=b.reg('EDX')))
            b.retornar_stub()
        intervalos=[(0x41591f,0x415a56),(0x412390,0x41374c),(0x410fcc,0x4110bf)]
        intervalos.append((0x4470b9,0x4470c5))  # BagVide original, sem stub
        parada=0x411147
        if ate_blitter:
            intervalos += [(0x411147,0x41209d),(0x442025,0x442065),(0x44fffe,0x450054),
                           (0x467d97,0x467da6)]
            parada=0x45b247
        r=self.executar(0x41591f,intervalos,{'EAX':x,'EDX':y,'EBX':0},
                         paradas=[parada],stubs={0x45b796:sombra})
        if r['EIP']!=parada: raise RuntimeError('Corpo não alcançado')
        def i16(v): return (v+32768)%65536-32768
        return dict(id_motor=r['EBX']&65535,x=i16(r['EAX']),y=i16(r['EDX']),sombras=sombras)

    def blit(self,id_motor,x,y,largura,altura,fundo,recorte):
        self.escrever(SUPERFICIE,fundo)
        self.escrever(0x508f70,struct.pack('<I',SUPERFICIE))
        self.escrever(0x4e17a0,struct.pack('<I',largura))
        l,t,r,b=recorte
        self.escrever(0x49a01c,struct.pack('<4H',t,b,l,r))
        self.executar(0x45b247,[(0x45b247,0x45b4fd)],
                        {'EAX':x,'EDX':y,'EBX':id_motor,'ECX':1},limite=500000)
        return self.ler(SUPERFICIE,largura*altura)
