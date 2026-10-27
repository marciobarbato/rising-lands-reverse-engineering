"""Bancada x86 sem sistema operacional para rotinas delimitadas do EXE original.

Não inicia o PE, não resolve imports nem oferece APIs Windows. Cada chamada
precisa declarar intervalos permitidos e tem limites de tempo/instruções.
Dependência opcional: Unicorn; leitores e reconstruções não dependem dela.
"""
import hashlib
import struct
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / '.local/python'))
try:
    import unicorn
    from unicorn import x86_const as x86
except ImportError as erro:
    raise ImportError('Instale requirements-emulacao.txt em .local/python para esta bancada.') from erro

HASH_ORIGINAL = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
BASE = 0x400000
UNIDADES = 0x1000000
PILHA = 0x2000000
RETORNO = 0x3000000


class BancadaX86:
    def __init__(self, arquivo=None):
        arquivo = arquivo or RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE'
        dados = Path(arquivo).read_bytes()
        if hashlib.sha256(dados).hexdigest() != HASH_ORIGINAL:
            raise ValueError('Executável incompatível com a bancada')
        self.cpu = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_32)
        self.cpu.mem_map(BASE, 0x200000)
        pe = struct.unpack_from('<I', dados, 0x3c)[0]
        secoes = struct.unpack_from('<H', dados, pe + 6)[0]
        opcional = struct.unpack_from('<H', dados, pe + 20)[0]
        for i in range(secoes):
            cab = pe + 24 + opcional + i * 40
            rva, tamanho, offset = struct.unpack_from('<III', dados, cab + 12)
            if offset and tamanho:
                self.cpu.mem_write(BASE + rva, dados[offset:offset + tamanho])
        self.cpu.mem_map(UNIDADES, 0x40000)
        self.cpu.mem_map(PILHA, 0x10000)
        self.cpu.mem_map(RETORNO, 0x1000)
        self.cpu.mem_write(0x4e19a0, struct.pack('<I', UNIDADES))
        self.permitidos = []
        self.paradas = set()
        self.execucoes = 0
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._conferir_endereco)

    def _conferir_endereco(self, cpu, endereco, tamanho, _):
        if endereco in self.paradas:
            cpu.emu_stop()
            return
        if not any(inicio <= endereco and endereco + tamanho <= fim for inicio, fim in self.permitidos):
            raise RuntimeError(f'Execução fora do trecho declarado: 0x{endereco:08x}')

    def escrever_unidade(self, memoria, indice=0):
        if len(memoria) != 276 or not 0 <= indice < 800:
            raise ValueError('Unidade deve ter 276 bytes e índice 0..799')
        self.cpu.mem_write(UNIDADES + indice * 276, bytes(memoria))

    def ler_unidade(self, indice=0):
        return bytes(self.cpu.mem_read(UNIDADES + indice * 276, 276))

    def executar(self, entrada, intervalos, registradores=None, parada=RETORNO, pilha=None):
        self.execucoes += 1
        self.permitidos = intervalos
        self.paradas = {parada} if isinstance(parada, int) else set(parada)
        for nome in ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP'):
            self.cpu.reg_write(getattr(x86, 'UC_X86_REG_' + nome), 0)
        self.cpu.reg_write(x86.UC_X86_REG_EFLAGS, 2)
        self.cpu.reg_write(x86.UC_X86_REG_ESP, PILHA + 0x8000)
        self.cpu.mem_write(PILHA, bytes(0x10000))
        self.cpu.mem_write(PILHA + 0x8000, struct.pack('<I', RETORNO))
        for offset, dados in (pilha or {}).items():
            if not 4 <= offset < 0x4000 or offset + len(dados) > 0x4000:
                raise ValueError('Dados de teste fora da área de pilha')
            self.cpu.mem_write(PILHA + 0x8000 + offset, dados)
        for nome, valor in (registradores or {}).items():
            self.cpu.reg_write(getattr(x86, 'UC_X86_REG_' + nome.upper()), valor & 0xffffffff)
        self.cpu.emu_start(entrada, RETORNO, timeout=1_000_000, count=20000)
        if self.cpu.reg_read(x86.UC_X86_REG_EIP) not in self.paradas:
            raise RuntimeError('Trecho não alcançou a parada dentro do limite da bancada')
        return {nome: self.cpu.reg_read(getattr(x86, 'UC_X86_REG_' + nome))
                for nome in ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP', 'EIP')}
