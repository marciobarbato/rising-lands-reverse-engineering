"""Whole-routine native runs of IaReset, IaAlloc and IAResetAttaque, and their replay.

The native run executes the intact routine *and every routine it reaches*
from the image on core's ``BancadaX86``; no engine routine is replaced. The
world routines owned by other fronts (players, research, mission number,
units, structures, resources) are only *observed*: at their entry the run
records the logical arguments, lets the original body execute, then records
EAX and every non-stack store the body made. File I/O and the clock are the
only declared bindings (IaAlloc). The observations drive ``MundoRepetido``, a
strict replay provider for the Python translation: each query must arrive in
the original order, from the original call site, with the original arguments.

Fixtures are whole inherited images: DGROUP+.bss (0x494000..0x523000), the
800×276-byte unit pool and the 4×20-byte player table, built without Unicorn.
"""
from dataclasses import dataclass
import hashlib
import random
import struct
import sys

from ambiente_ia_runtime import CD, EXE, ORIGINAL_SHA256, ROOT

DADOS_BASE, DADOS_FIM = 0x494000, 0x523000
UNIDADES_BASE, UNIDADES_TAMANHO = 0x1000000, 800 * 276
JOGADORES_BASE, JOGADORES_TAMANHO = 0x1100000, 4 * 20
PONTEIRO_UNIDADES, PONTEIRO_JOGADORES = 0x4e19a0, 0x5080a8
NUMERO_MISSAO = 0x496fe4
ESTRUTURAS = 0x49a0c8
CODIGO = (0x401000, 0x494000)


def _al(r, s):
    return (r['EAX'] & 0xff,)


def _ax(r, s):
    return (r['EAX'] & 0xffff,)


# Observed world routines: original name and the logical arguments read from registers/stack.
MUNDO = {
    0x46d817: ('PlayerGetType', _al),
    0x4717c2: ('RechercheGetNiveau', lambda r, s: (r['EAX'] & 0xff, r['EDX'] & 0xffff)),
    0x470b37: ('RechercheSetBranche', lambda r, s: (r['EAX'] & 0xff, r['EDX'] & 0xff)),
    0x46c11a: ('MissionGetNum', lambda r, s: ()),
    0x443dad: ('EnginEstVivant', _ax),
    0x442025: ('EnginGetType', _ax),
    0x440e11: ('EnginGetEtat', _ax),
    0x4422dd: ('TypeEnginEstMonstre', _al),
    0x443108: ('EnginSetPlayer', lambda r, s: (r['EAX'] & 0xffff, r['EDX'] & 0xff)),
    0x41a735: ('BatimentExiste', _ax),
    0x41a08c: ('BatimentGetPlayer', _ax),
    0x41a4f4: ('BatimentGetType', _ax),
    0x467670: ('GetRessource', lambda r, s: (s[0] & 0xff,)),
}
SAIDAS_GETRESSOURCE = ('EAX', 'EDX', 'EBX', 'ECX')  # four u16 output pointers


@dataclass
class Imagem:
    dados: bytearray
    unidades: bytearray
    jogadores: bytearray

    def copia(self):
        return Imagem(bytearray(self.dados), bytearray(self.unidades), bytearray(self.jogadores))

    def segmentos(self):
        return ((DADOS_BASE, self.dados), (UNIDADES_BASE, self.unidades), (JOGADORES_BASE, self.jogadores))

    def hashes(self):
        return {nome: hashlib.sha256(bytes(buf)).hexdigest()
                for nome, buf in (('dados', self.dados), ('unidades', self.unidades), ('jogadores', self.jogadores))}

    def u8(self, endereco, valor):
        self.dados[endereco - DADOS_BASE] = valor & 0xff

    def u16(self, endereco, valor):
        struct.pack_into('<H', self.dados, endereco - DADOS_BASE, valor & 0xffff)

    def u32(self, endereco, valor):
        struct.pack_into('<I', self.dados, endereco - DADOS_BASE, valor & 0xffffffff)

    def vista(self, endereco, tamanho):
        return memoryview(self.dados)[endereco - DADOS_BASE:endereco - DADOS_BASE + tamanho]


def imagem_base():
    """DGROUP+.bss exactly as the bench maps the intact sections, plus the two pool pointers."""
    raw = EXE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != ORIGINAL_SHA256:
        raise ValueError('Original EXE SHA-256 mismatch')
    memoria = bytearray(0x200000)
    pe = struct.unpack_from('<I', raw, 0x3c)[0]
    secoes, opcional = struct.unpack_from('<H', raw, pe + 6)[0], struct.unpack_from('<H', raw, pe + 20)[0]
    for i in range(secoes):
        rva, tamanho, offset = struct.unpack_from('<III', raw, pe + 24 + opcional + i * 40 + 12)
        if offset and tamanho:
            memoria[rva:rva + tamanho] = raw[offset:offset + tamanho]
    imagem = Imagem(memoria[DADOS_BASE - 0x400000:DADOS_FIM - 0x400000], bytearray(UNIDADES_TAMANHO),
                    bytearray(JOGADORES_TAMANHO))
    imagem.u32(PONTEIRO_UNIDADES, UNIDADES_BASE)
    imagem.u32(PONTEIRO_JOGADORES, JOGADORES_BASE)
    return imagem


def _missoes():
    caminho = str(ROOT / 'pesquisas-paralelas/missoes')
    if caminho not in sys.path:
        sys.path.insert(0, caminho)
    import ambiente_missoes  # noqa: F401  (missions' own bootstrap)


def carregar_mundo_monde01(imagem):
    """MONDE01's structures, units and monster tables through missions' committed loaders."""
    _missoes()
    from formatos import Leitor, ler_eta
    from carregador_estruturas import carregar_estruturas_missao
    from carregador_unidades import carregar_unidades_missao
    from carregador_cadeia_auxiliar import BuffersCadeiaAuxiliar, carregar_cadeia_auxiliar
    from entradas import tipos_originais
    from perfil_privado_missao import PerfilPrivado
    dados = (CD / 'WORLD/MONDE01.ETA').read_bytes()
    blocos = {b['nome']: b['offset'] for b in ler_eta(dados)['blocos']}
    carregar_estruturas_missao(Leitor(dados, blocos['estruturas']), imagem.vista(ESTRUTURAS, 276000))
    selecoes = bytearray(imagem.vista(0x508728, 2048))  # core's SelectionInit requires a bytearray
    carregar_unidades_missao(Leitor(dados, blocos['unidades']), imagem.unidades, imagem.vista(0x4e19bc, 4),
                             tipos_originais(), selecoes)
    imagem.vista(0x508728, 2048)[:] = selecoes
    buffers = BuffersCadeiaAuxiliar(
        imagem.vista(0x509954, 80), imagem.vista(0x50d5b4, 1004), imagem.vista(0x50b18c, 5254),
        imagem.vista(0x50c614, 4000), imagem.vista(0x4e1d20, 114), imagem.vista(0x511ffc, 804),
        imagem.vista(0x50a9bc, 1220), imagem.vista(0x50af84, 432), imagem.vista(0x497164, 4))
    perfil = PerfilPrivado({b'./monstre.ini': (CD / 'INSTALHD/MONSTRE.INI').read_bytes()})
    carregar_cadeia_auxiliar(Leitor(dados, blocos['tabela_47534a']), buffers,
                             tipos_grupo8=bytes(imagem.vista(0x498400, 8)), perfil=perfil)
    return imagem


def definir_jogadores(imagem, tipos):
    for jogador, tipo in enumerate(tipos):
        imagem.jogadores[jogador * 20 + 1] = tipo


def fixture_monde01(tipos=(1, 0, 0, 0)):
    imagem = carregar_mundo_monde01(imagem_base())
    imagem.u8(NUMERO_MISSAO, 1)
    definir_jogadores(imagem, tipos)
    return imagem


def poluir(imagem, rng, intervalos):
    """Inherited dirty state: random bytes over the given absolute intervals of DGROUP+.bss."""
    for inicio, fim in intervalos:
        imagem.dados[inicio - DADOS_BASE:fim - DADOS_BASE] = rng.randbytes(fim - inicio)


def fixture_sintetica(semente, *, tipos=(1, 2, 2, 2), missao=3, unidades=220, estruturas=60, monstros=0,
                      sujo=False, contextos_zerados=True, pesquisa=0, tipos_monstro=None, grupos_monstros=None):
    """A valid synthetic world (units, structures, research, resources, monster specs)."""
    rng = random.Random(0x1a0000 + semente)
    imagem = imagem_base()
    if sujo:
        poluir(imagem, rng, ((0x512320, 0x514900), (0x51a98c, 0x521350), (0x50a9cc, 0x50a9cd),
                             (0x50ae80, 0x50ae84), (0x50b134, 0x50b184)))
        if contextos_zerados:
            for jogador in range(4):
                base = 0x51a98c + jogador * 16
                imagem.dados[base + 5 - DADOS_BASE:base + 9 - DADOS_BASE] = bytes(4)
    imagem.u8(NUMERO_MISSAO, missao)
    imagem.u32(0x498db4, rng.randrange(1, 0x7fffffff))  # iaRandom state inside core's domain
    definir_jogadores(imagem, tipos)
    # research levels read by RechercheGetNiveau (0x5080f4 + player*16 + branch); ``pesquisa`` raises them
    imagem.dados[0x5080f4 - DADOS_BASE:0x5080f4 - DADOS_BASE + 64] = bytes(pesquisa + rng.randrange(6)
                                                                       for _ in range(64))
    for jogador in range(4):  # GetRessource reads three u16 per 32-byte player record
        for campo in (0x4e2eaa, 0x4e2eb2, 0x4e2eba):
            imagem.u16(campo + jogador * 32, rng.randrange(0x10000))
    vivos = rng.sample(range(800), unidades + monstros)
    for ordem, indice in enumerate(vivos):
        base = indice * 276
        monstro = ordem >= unidades
        imagem.unidades[base] = rng.randrange(5) if not monstro else rng.randrange(4)
        imagem.unidades[base + 1] = ((rng.choice(tipos_monstro) if tipos_monstro else rng.randrange(20, 25))
                                     if monstro else rng.choice((0, 1, 2, 5, 7, 8, 9, 9, 9, 3)))
        imagem.unidades[base + 2] = rng.choice((1, 2, 3, 4, 5, 7, 7, 14, 14, 18)) if not monstro else 7
        imagem.unidades[base + 0x108:base + 0x110] = rng.randbytes(8)
    for indice in rng.sample(range(1000), estruturas):
        base = ESTRUTURAS + indice * 276
        imagem.u8(base + 4, rng.randrange(5))
        imagem.u8(base + 5, rng.choice((0, 1, 1, 2, 3)))
        imagem.u8(base + 8, rng.choice((1, 2, 3, 3, 4, 5, 6, 9, 10, 12, 17)))
    grupos = imagem.vista(0x50af84, 432)
    grupos[:] = bytes(432)
    if grupos_monstros is None:  # every spec needs at least one type, else the original never terminates
        grupos_monstros = {g: (rng.randrange(1, 4), {t: rng.randrange(1, 4) for t in rng.sample(range(20, 25),
                                                                                                rng.randrange(1, 4))})
                           for g in rng.sample(range(16), rng.randrange(3, 9))}
    for grupo, (quantidade, tipos_grupo) in grupos_monstros.items():
        grupos[416 + grupo] = quantidade
        for tipo, necessarios in tipos_grupo.items():
            grupos[grupo * 26 + tipo] = necessarios
    return imagem


class ExecucaoNativa:
    """One fully native run of an original routine over an inherited image."""

    def __init__(self, image, imagem):
        from emulador import BancadaX86, PILHA, RETORNO
        self.image, self.retorno, self.pilha = image, RETORNO, (PILHA, PILHA + 0x10000)
        self.bench = BancadaX86()
        self.cpu = self.bench.cpu
        self.cpu.mem_map(JOGADORES_BASE, 0x1000)
        for base, buf in imagem.segmentos():
            self.cpu.mem_write(base, bytes(buf))
        self.thunks, self.escritas = {}, None

    def _escrita(self, _uc, _acesso, endereco, tamanho, valor, _dados):
        if self.escritas is None or self.pilha[0] <= endereco < self.pilha[1]:
            return
        self.escritas.append((endereco, (valor & ((1 << 8 * tamanho) - 1)).to_bytes(tamanho, 'little')))

    def ligar_importacao(self, slot, retorno):
        thunk = self.retorno + 0x100 + 0x10 * len(self.thunks)
        self.cpu.mem_write(slot, struct.pack('<I', thunk))
        self.thunks[thunk] = (self.image.imports[slot].split('!')[-1], retorno)  # e.g. timeGetTime
        return thunk

    def _ler(self, endereco, tamanho):
        return bytes(self.cpu.mem_read(endereco, tamanho))

    def executar(self, entrada, *, ligacoes=None, registradores=None, limite=1000000, parar_antes=None,
                 parar_em=None):
        """Run to the original return.

        ``ligacoes``: declared bindings {address: (name, eax, argument reader, tail-jump site)};
        the bound routine is not executed and its stack arguments are popped as its ``ret N`` would.
        """
        import unicorn
        from unicorn import x86_const
        ligacoes = dict(ligacoes or {})
        self.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, self._escrita)
        permitidos = [CODIGO, (self.retorno + 0x100, self.retorno + 0x1000)]
        paradas = set(MUNDO) | set(ligacoes) | set(self.thunks) | {self.retorno}
        if parar_em is not None:
            paradas.add(parar_em)
        observacoes, segmentos = [], 1
        resultado = self.bench.executar(entrada, permitidos, registradores or {}, parada=paradas,
                                        limite_instrucoes=limite)
        while resultado['EIP'] != self.retorno:
            alvo, esp = resultado['EIP'], resultado['ESP']
            if alvo == parar_em:
                break
            ret = struct.unpack('<I', self._ler(esp, 4))[0]
            pilha = struct.unpack('<4I', self._ler(esp + 4, 16))
            if parar_antes is not None and len(observacoes) == parar_antes:
                break  # declared checkpoint: entry of the next world call, not executed
            if alvo in MUNDO:
                nome, argumentos = MUNDO[alvo]
                obs = dict(nome=nome, sitio=_sitio(self.image, ret), argumentos=list(argumentos(resultado, pilha)))
                ponteiros = [resultado[r] for r in SAIDAS_GETRESSOURCE]
                self.escritas = []
                resultado = self.bench.retomar(alvo, permitidos, parada={ret}, limite_instrucoes=limite)
                segmentos += 1
                obs['eax'] = resultado['EAX']
                if nome == 'GetRessource':  # its outputs are stack locals of the caller
                    obs['saidas'] = [struct.unpack('<H', self._ler(p, 2))[0] for p in ponteiros]
                obs['escritas'] = [(a, d.hex()) for a, d in self.escritas]
                self.escritas = None
                observacoes.append(obs)
            else:
                if alvo in self.thunks:
                    (nome, valor), limpeza, argumentos = self.thunks[alvo], 0, ()
                else:
                    nome, valor, leitura, cauda = ligacoes[alvo]
                    limpeza, argumentos = self.image.stack_cleanup(alvo), leitura(resultado, pilha)
                sitio = _sitio(self.image, ret)
                if sitio is None and alvo not in self.thunks:
                    sitio = cauda  # entered by the caller's tail jump at this declared address
                observacoes.append(dict(nome=nome, sitio=sitio, ligacao=True, argumentos=list(argumentos), eax=valor))
                self.cpu.reg_write(x86_const.UC_X86_REG_EAX, valor)
                self.cpu.reg_write(x86_const.UC_X86_REG_ESP, esp + 4 + limpeza)
                if ret == self.retorno:
                    resultado = dict(resultado, EIP=ret, EAX=valor)
                    break
            resultado = self.bench.retomar(ret, permitidos, parada=paradas, limite_instrucoes=limite)
            segmentos += 1
        final = Imagem(bytearray(self._ler(DADOS_BASE, DADOS_FIM - DADOS_BASE)),
                       bytearray(self._ler(UNIDADES_BASE, UNIDADES_TAMANHO)),
                       bytearray(self._ler(JOGADORES_BASE, JOGADORES_TAMANHO)))
        return dict(eax=resultado['EAX'], observacoes=observacoes, segmentos=segmentos, imagem=final,
                    parada=resultado['EIP'])


def _sitio(image, ret):
    """Original call site ending at ``ret`` (None when entered by a tail jump)."""
    if not CODIGO[0] + 7 <= ret <= CODIGO[1]:
        return None
    for tamanho in (5, 7, 6, 3, 2):
        try:
            insn = image.instruction(ret - tamanho)
        except ValueError:
            continue
        if insn.mnemonic == 'call' and insn.size == tamanho:
            return ret - tamanho
    return None


class DivergenciaRepeticao(AssertionError):
    """The translation asked the world for something the original did not."""


class MundoRepetido:
    """Strict replay of native world observations for the Python translation."""

    def __init__(self, observacoes, memoria, *, ate=None):
        """``ate``: after that many replayed calls the provider is absent (named dependency)."""
        self.observacoes, self.memoria, self.posicao, self.ate = list(observacoes), memoria, 0, ate

    def _proxima(self, nome, sitio, argumentos):
        if self.posicao >= len(self.observacoes):
            raise DivergenciaRepeticao(f'{nome} at 0x{sitio:08x} after the original finished its world calls')
        obs = self.observacoes[self.posicao]
        self.posicao += 1
        esperado = (obs['nome'], obs['sitio'], list(obs['argumentos']))
        if (nome, sitio, list(argumentos)) != esperado:
            raise DivergenciaRepeticao(f'call {self.posicao}: got {(nome, sitio, argumentos)}, original {esperado}')
        for endereco, dados in obs.get('escritas', ()):
            self.memoria.escrever_mundo(endereco, bytes.fromhex(dados))
        return obs

    def completo(self):
        return self.posicao == len(self.observacoes)

    def __getattr__(self, nome):
        if nome not in {n for n, _ in MUNDO.values()} | {'timeGetTime', 'debugSymLoad', 'debugSymUnload',
                                                         'iaProbLoadBinaryRules'}:
            raise AttributeError(nome)
        if self.ate is not None and self.posicao >= self.ate:
            raise AttributeError(nome)  # provider absent from here on

        def consulta(*argumentos, sitio):
            obs = self._proxima(nome, sitio, argumentos)
            return tuple(obs['saidas']) if nome == 'GetRessource' else obs['eax']
        return consulta


def provar_ciclo_grupo_vazio(image, imagem):
    """One transient native visit, then three identical complete checkpoint states.

    Every resumed segment must reach its declared checkpoint under the unchanged
    bench limits. Timeouts/instruction-limit errors propagate and never prove a
    cycle. Each back-edge JMP executes natively before the loop is resumed.
    """
    from unicorn import x86_const
    ponto, destino = 0x47b1f4, 0x47b137
    salto = image.instruction(ponto)
    if salto.mnemonic != 'jmp' or image.direct_target(salto) != destino:
        raise AssertionError('Original empty-group back edge changed')
    execucao = ExecucaoNativa(image, imagem.copia())
    inicial = execucao.executar(0x47f36e, parar_em=ponto)
    if inicial['parada'] != ponto:
        raise AssertionError('Fixture did not reach the empty-group checkpoint')
    registros = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP', 'EIP', 'EFLAGS',
                 'CS', 'DS', 'ES', 'SS', 'FS', 'GS')

    def estado():
        cpu = {r: execucao.cpu.reg_read(getattr(x86_const, 'UC_X86_REG_' + r)) for r in registros}
        buffers = {str(base): execucao._ler(base, len(buf)) for base, buf in imagem.segmentos()}
        buffers['stack'] = execucao._ler(execucao.pilha[0], execucao.pilha[1] - execucao.pilha[0])
        return cpu, buffers

    estados = [estado()]
    externos = set(MUNDO) | {0x48d5fd, 0x47e437, 0x48d699, 0x493a24}
    for _ in range(3):
        for entrada, esperado in ((ponto, destino), (destino, ponto)):
            resultado = execucao.bench.retomar(entrada, [CODIGO], parada={esperado} | externos)
            if resultado['EIP'] != esperado:
                raise AssertionError(f'External effect reached during the cycle: 0x{resultado["EIP"]:08x}')
        estados.append(estado())
    repetidos = estados[1:]
    if repetidos[0] != repetidos[1] or repetidos[1] != repetidos[2]:
        diferencas = []
        for anterior, seguinte in zip(repetidos, repetidos[1:]):
            cpu_antes, memoria_antes = anterior
            cpu_depois, memoria_depois = seguinte
            diferencas.append(dict(registers={r: (cpu_antes[r], cpu_depois[r]) for r in cpu_antes
                                              if cpu_antes[r] != cpu_depois[r]},
                buffers={nome: [i for i, (a, b) in enumerate(zip(dados, memoria_depois[nome])) if a != b][:32]
                         for nome, dados in memoria_antes.items() if dados != memoria_depois[nome]}))
        raise AssertionError(f'Native checkpoint states differ; no cycle demonstrated: {diferencas}')
    cpu, buffers = repetidos[0]
    prova = dict(checkpoint=f'0x{ponto:08x}', target=f'0x{destino:08x}', visits=len(estados),
                 equal_cpu_stack_and_images=True, registers=cpu,
                 sha256={nome: hashlib.sha256(dados).hexdigest() for nome, dados in buffers.items()},
                 resumed_segments=6, identical_visits=[2, 3, 4], initial_visit_is_transient=True,
                 external_calls_during_cycle=0, bindings_during_cycle=[],
                 inputs="Inherited image/pools/stack only; no external input call reached")
    return inicial, prova
