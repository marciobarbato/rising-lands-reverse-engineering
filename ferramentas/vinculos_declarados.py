"""Explicit external-call fixtures; no native execution or Windows defaults."""
from dataclasses import dataclass, field
import hashlib
import struct
from types import MappingProxyType

GPRS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')


@dataclass(frozen=True)
class ArgumentoVinculo:
    origem: object                 # full register name, or byte offset from ESP (>=4)
    bits: int = 32
    assinado: bool = False


@dataclass(frozen=True)
class RetornoVinculo:
    eax: int
    registradores: dict = field(default_factory=dict)


@dataclass(frozen=True)
class VinculoDeclarado:
    endereco: int
    nome: str
    argumentos: tuple
    atender: object
    desempilhar: int
    natureza: str


class ParadaVinculoDeclarado(NotImplementedError):
    """A declared fixture cannot honor this call; completed effects stay visible."""


class LimiteVinculosDeclarados(RuntimeError):
    def __init__(self, endereco, limite):
        self.endereco, self.limite = endereco, limite
        super().__init__(f'Declared binding resumption budget {limite} reached at 0x{endereco:x}')


def importacoes_pe(dados, base):
    """Read actual PE32 import slots/names; arbitrary data is never an IAT slot."""
    pe = struct.unpack_from('<I', dados, 0x3c)[0]
    opcional = pe+24
    if struct.unpack_from('<H', dados, opcional)[0] != 0x10b:
        raise ValueError('Declared imports require PE32 metadata')
    quantidade = struct.unpack_from('<H', dados, pe+6)[0]
    tamanho_opcional = struct.unpack_from('<H', dados, pe+20)[0]
    secoes = [struct.unpack_from('<III', dados, opcional+tamanho_opcional+i*40+12)
              for i in range(quantidade)]
    def ler(rva, n):
        for a, tamanho, offset in secoes:
            if offset and a <= rva and rva+n <= a+tamanho:
                return dados[offset+rva-a:offset+rva-a+n]
        raise ValueError(f'Import metadata outside original PE raw sections: 0x{rva:x}')
    def texto(rva):
        texto = bytearray()
        for i in range(4096):
            b = ler(rva+i, 1)
            if b == b'\0': return texto.decode('ascii')
            texto += b
        raise ValueError('Unterminated PE import name')
    rva, tamanho = struct.unpack_from('<II', dados, opcional+96+8)
    resultado = {}
    for p in range(rva, rva+tamanho, 20):
        lookup, _, _, nome, iat = struct.unpack('<5I', ler(p, 20))
        if not any((lookup, nome, iat)): return resultado
        dll = texto(nome)
        for i in range(65536):
            entrada = struct.unpack('<I', ler((lookup or iat)+i*4, 4))[0]
            if entrada == 0: break
            simbolo = f'ordinal:{entrada & 65535}' if entrada & 0x80000000 else texto(entrada+2)
            resultado[base+iat+i*4] = dict(dll=dll, symbol=simbolo)
        else: raise ValueError('Unterminated PE import thunk table')
    raise ValueError('Unterminated PE import descriptor table')


class ChamadaVinculo:
    def __init__(self, registro, vinculo, argumentos, registradores, retorno, evento):
        self.vinculo, self.argumentos = vinculo, argumentos
        self.registradores = MappingProxyType(registradores)
        self.retorno = retorno
        self._registro, self._evento = registro, evento

    def ler(self, endereco, tamanho):
        if not isinstance(endereco, int) or not isinstance(tamanho, int) or not 0 <= endereco <= endereco+tamanho <= 0x100000000:
            raise ValueError('Binding read requires an exact nonnegative u32 memory range')
        return bytes(self._registro.cpu.mem_read(endereco, tamanho))

    def escrever(self, endereco, dados):
        if not isinstance(dados, (bytes, bytearray, memoryview)):
            raise ValueError('Binding writes require explicit bytes')
        dados = bytes(dados)
        if not isinstance(endereco, int) or not 0 <= endereco <= endereco+len(dados) <= 0x100000000:
            raise ValueError('Binding write requires an exact u32 memory range')
        if any(endereco < z and a < endereco+len(dados) for a, z in self._registro.codigo_protegido):
            raise ValueError('A declared binding cannot patch original executable instructions')
        self._registro.cpu.mem_write(endereco, dados)
        self._evento['memory_writes'].append(dict(address=hex(endereco), size=len(dados),
                                                  sha256=hashlib.sha256(dados).hexdigest()))


class RegistroVinculosDeclarados:
    """Reusable with a bench CPU; invocation happens only after emulation stops."""
    def __init__(self, cpu, registradores, *, codigo_protegido=()):
        self.cpu, self.registradores = cpu, dict(registradores)
        self.codigo_protegido = tuple(codigo_protegido)
        self.vinculos, self.eventos = {}, []
        self._ativo = False

    def declarar(self, endereco, nome, argumentos, atender, *, desempilhar=0, natureza):
        if (self._ativo or not isinstance(endereco, int) or not 0 <= endereco < 0x100000000
                or endereco in self.vinculos or not isinstance(nome, str) or not nome
                or not callable(atender) or not isinstance(desempilhar, int)
                or not 0 <= desempilhar <= 16380 or desempilhar % 4
                or natureza not in ('importacao', 'io', 'relogio', 'backend')):
            raise ValueError('Declare a unique external boundary, explicit handler, kind and aligned stack cleanup')
        args = []
        for arg in argumentos:
            arg = arg if isinstance(arg, ArgumentoVinculo) else ArgumentoVinculo(arg)
            if arg.bits not in (8, 16, 32) or not isinstance(arg.assinado, bool):
                raise ValueError('Binding argument widths are explicit 8/16/32 bits')
            origem = arg.origem
            if isinstance(origem, str):
                if origem not in GPRS:
                    raise ValueError('Binding register arguments require full uppercase GPR names')
            elif not isinstance(origem, int) or not 4 <= origem <= 16380 or origem % 4:
                raise ValueError('Binding stack arguments use aligned offsets from ESP, excluding the return address')
            args.append(arg)
        v = VinculoDeclarado(endereco, nome, tuple(args), atender, desempilhar, natureza)
        self.vinculos[endereco] = v
        return v

    def invocar(self, endereco):
        if self._ativo:
            raise RuntimeError('Declared bindings are not reentrant')
        v = self.vinculos[endereco]
        regs = {n: self.cpu.reg_read(i) for n, i in self.registradores.items()}
        esp = regs['ESP']
        retorno = struct.unpack('<I', self.cpu.mem_read(esp, 4))[0]
        args = []
        for a in v.argumentos:
            valor = (regs[a.origem] if isinstance(a.origem, str)
                     else int.from_bytes(self.cpu.mem_read(esp+a.origem, a.bits//8), 'little'))
            valor &= (1 << a.bits)-1
            if a.assinado and valor & (1 << (a.bits-1)):
                valor -= 1 << a.bits
            args.append(valor)
        evento = dict(name=v.nome, address=hex(endereco), kind=v.natureza,
                      arguments=args, caller_return=hex(retorno), esp_before=hex(esp),
                      stack_pop=v.desempilhar, registers_before=dict(regs),
                      memory_writes=[], status='entered')
        self.eventos.append(evento)
        chamada = ChamadaVinculo(self, v, tuple(args), regs, retorno, evento)
        self._ativo = True
        try:
            resposta = v.atender(chamada)
            if isinstance(resposta, int):
                resposta = RetornoVinculo(resposta)
            if not isinstance(resposta, RetornoVinculo) or not isinstance(resposta.eax, int):
                raise ValueError('A fixture must return an explicit EAX value; None is not success')
            extras = dict(resposta.registradores)
            if any(n not in GPRS or n == 'EAX' or not isinstance(valor, int) for n, valor in extras.items()):
                raise ValueError('Extra fixture results may write explicit non-EAX GPRs only')
            resultados = {'EAX': resposta.eax & 0xffffffff, **{n: x & 0xffffffff for n, x in extras.items()}}
            for nome, valor in resultados.items():
                self.cpu.reg_write(self.registradores[nome], valor)
            self.cpu.reg_write(self.registradores['ESP'], (esp+4+v.desempilhar) & 0xffffffff)
            self.cpu.reg_write(self.registradores['EIP'], retorno)
            evento.update(status='returned', results=resultados, esp_after=hex((esp+4+v.desempilhar) & 0xffffffff))
            return retorno
        except Exception as erro:
            evento.update(status='stopped' if isinstance(erro, ParadaVinculoDeclarado) else 'error',
                          error_type=type(erro).__name__, reason=str(erro))
            raise
        finally:
            self._ativo = False
