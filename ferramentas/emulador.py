"""Bancada x86 sem sistema operacional para rotinas delimitadas do EXE original.

Não inicia o PE, não resolve imports nem oferece APIs Windows. Cada chamada
precisa declarar intervalos permitidos e tem limites de tempo/instruções.
Dependência opcional: Unicorn; leitores e reconstruções não dependem dela.
"""
import hashlib
import struct
import sys
from pathlib import Path
from vinculos_declarados import RegistroVinculosDeclarados, LimiteVinculosDeclarados, importacoes_pe

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
DESCRITORES = 0x3100000
TRAMPOLINS_DECLARADOS = 0x3200000
# Only source-inventoried I/O boundaries may replace an original code entry: the game
# wrappers FileOpen/FileClose/FileRead/FileSeek and the statically linked Watcom CRT
# fopen/fread/fclose/fseek/fgets (see docs/core/DECLARED_BINDINGS.md for each ABI).
FRONTEIRAS_IO = frozenset((0x458420, 0x45844c, 0x458461, 0x45848b, 0x48c71f, 0x48c97b, 0x48c80b,
                           0x48cda2, 0x48ce96))


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
        codigo_protegido = []
        for i in range(secoes):
            cab = pe + 24 + opcional + i * 40
            rva, tamanho, offset = struct.unpack_from('<III', dados, cab + 12)
            if offset and tamanho:
                self.cpu.mem_write(BASE + rva, dados[offset:offset + tamanho])
                if struct.unpack_from('<I', dados, cab + 36)[0] & 0x20000000:
                    codigo_protegido.append((BASE+rva, BASE+rva+tamanho))
        self.cpu.mem_map(UNIDADES, 0x40000)
        self.cpu.mem_map(PILHA, 0x10000)
        self.cpu.mem_map(RETORNO, 0x1000)
        # O runtime Watcom troca ES por DS nas rotinas de strings. Seletores
        # nulos implícitos do Unicorn não bastam depois de MOV/POP ES.
        # Segmentos planos de 32 bits: base zero, limite 4 GiB; não são APIs Windows.
        self.cpu.mem_map(DESCRITORES, 0x1000)
        self.cpu.mem_write(DESCRITORES, struct.pack('<3Q', 0, 0x00cf9a000000ffff, 0x00cf92000000ffff))
        self.cpu.reg_write(x86.UC_X86_REG_GDTR, (0, DESCRITORES, 23, 0))
        self.cpu.reg_write(x86.UC_X86_REG_CS, 8)
        for nome in ('DS', 'ES', 'SS'):
            self.cpu.reg_write(getattr(x86, 'UC_X86_REG_' + nome), 16)
        self.cpu.mem_write(0x4e19a0, struct.pack('<I', UNIDADES))
        self.permitidos = []
        self.paradas = set()
        self.execucoes = 0
        nomes = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP', 'EIP', 'EFLAGS')
        self.vinculos_declarados = RegistroVinculosDeclarados(
            self.cpu, {n: getattr(x86, 'UC_X86_REG_'+n) for n in nomes}, codigo_protegido=codigo_protegido)
        self.importacoes_declaradas = []
        self.importacoes_originais = importacoes_pe(dados, BASE)
        self.retomadas_vinculos = 0
        self.parada_limite_vinculos = None
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

    def executar(self, entrada, intervalos, registradores=None, parada=RETORNO, pilha=None, limite_instrucoes=20000,
                 limite_vinculos=65536):
        if self.vinculos_declarados._ativo:
            raise RuntimeError('A binding handler cannot start nested native execution')
        if not 1 <= limite_instrucoes <= 1000000:
            raise ValueError('Limite de instruções deve estar entre 1 e 1000000')
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
        return self._rodar_com_vinculos(entrada, limite_instrucoes, limite_vinculos)

    def retomar(self, entrada, intervalos, parada=RETORNO, limite_instrucoes=20000, limite_vinculos=65536):
        """Retoma um checkpoint explícito, preservando registradores e pilha.

        Cada trecho retomado conta como uma execução delimitada e usa os mesmos
        limites de endereço/tempo da entrada normal. Não inicializa uma chamada.
        """
        if self.vinculos_declarados._ativo:
            raise RuntimeError('A binding handler cannot resume nested native execution')
        if not 1 <= limite_instrucoes <= 1000000:
            raise ValueError('Limite de instruções deve estar entre 1 e 1000000')
        self.execucoes += 1
        self.permitidos = intervalos
        self.paradas = {parada} if isinstance(parada, int) else set(parada)
        return self._rodar_com_vinculos(entrada, limite_instrucoes, limite_vinculos)

    def declarar_vinculo(self, endereco, nome, argumentos, atender, *, desempilhar=0, natureza):
        """Declare only an external/I/O boundary, never an unknown engine body."""
        if BASE <= endereco < BASE+0x200000 and (endereco not in FRONTEIRAS_IO or natureza != 'io'):
            raise ValueError('Original PE entries may be bound only at inventoried I/O boundaries')
        return self.vinculos_declarados.declarar(endereco, nome, argumentos, atender,
                                               desempilhar=desempilhar, natureza=natureza)

    def declarar_importacao(self, iat, nome, quantidade_argumentos, atender):
        """Resolve one explicit stdcall IAT slot; the private thunk never executes."""
        if (not isinstance(iat, int) or iat not in self.importacoes_originais
                or not isinstance(quantidade_argumentos, int) or not 0 <= quantidade_argumentos <= 64
                or not callable(atender) or not nome or len(self.importacoes_declaradas) >= 256
                or any(x['iat'] == hex(iat) for x in self.importacoes_declaradas)
                or any(a <= iat < z for a, z in self.vinculos_declarados.codigo_protegido)):
            raise ValueError('Declare an explicit data IAT slot and supported stdcall argument count')
        antigo = struct.unpack('<I', self.cpu.mem_read(iat, 4))[0]
        if not self.importacoes_declaradas:
            self.cpu.mem_map(TRAMPOLINS_DECLARADOS, 4096)
        alvo = TRAMPOLINS_DECLARADOS + 16*len(self.importacoes_declaradas)
        self.cpu.mem_write(alvo, b'\xc3')
        v = self.declarar_vinculo(alvo, nome, tuple(4+4*i for i in range(quantidade_argumentos)),
                                 atender, desempilhar=4*quantidade_argumentos, natureza='importacao')
        self.cpu.mem_write(iat, struct.pack('<I', alvo))
        self.importacoes_declaradas.append(dict(iat=hex(iat), original_target=hex(antigo),
                                                target=hex(alvo), name=nome, arguments=quantidade_argumentos,
                                                original_import=self.importacoes_originais[iat]))
        return v

    def _rodar_com_vinculos(self, entrada, limite_instrucoes, limite_vinculos=65536):
        if not isinstance(limite_vinculos, int) or not 0 <= limite_vinculos <= 1000000:
            raise ValueError('Binding resumption budget must be explicitly bounded in 0..1000000')
        self.parada_limite_vinculos = None
        declarados = self.vinculos_declarados.vinculos
        if not declarados:
            return self._executar_ate_parada(entrada, limite_instrucoes)
        pedidos = set(self.paradas)
        adicionados = set(declarados)-pedidos
        self.paradas.update(adicionados)
        realizadas = 0
        try:
            while True:
                regs = self._executar_ate_parada(entrada, limite_instrucoes)
                endereco = regs['EIP']
                if endereco not in declarados or endereco in pedidos:
                    return regs
                if realizadas >= limite_vinculos:
                    self.parada_limite_vinculos = dict(address=hex(endereco), limit=limite_vinculos, handled=realizadas)
                    raise LimiteVinculosDeclarados(endereco, limite_vinculos)
                entrada = self.vinculos_declarados.invocar(endereco)
                realizadas += 1
                self.retomadas_vinculos += 1
                self.execucoes += 1
        finally:
            self.paradas.difference_update(adicionados)

    def _executar_ate_parada(self, entrada, limite_instrucoes):
        self.cpu.emu_start(entrada, RETORNO, timeout=1_000_000, count=limite_instrucoes)
        if self.cpu.reg_read(x86.UC_X86_REG_EIP) not in self.paradas:
            raise RuntimeError('Trecho não alcançou a parada dentro do limite da bancada')
        return {nome: self.cpu.reg_read(getattr(x86, 'UC_X86_REG_' + nome))
                for nome in ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP', 'EIP')}
