"""Finite declared external boundaries for the whole-MissionLoad original oracle.

These handlers are *fixtures* for the Core16 binding transport: Windows
KERNEL32/USER32/WINMM imports and the inventoried CRT fopen/fread/fclose and
FileSeek I/O entries. They never replace an engine body. Every answer comes
from an explicit named input or from a read-only copy of the original media.
Unsupported requests raise ``ParadaVinculoDeclarado`` so the native run stops
with all earlier effects retained. Importing this module executes nothing.
"""
from dataclasses import dataclass, field
import hashlib
from pathlib import Path
import struct

import ambiente_missoes
from vinculos_declarados import ParadaVinculoDeclarado

GMEM_ZEROINIT = 0x40
SEEK = {0: 'SEEK_SET', 1: 'SEEK_CUR', 2: 'SEEK_END'}


def _sha(dados):
    return hashlib.sha256(bytes(dados)).hexdigest()


def rotulo_volume_iso(bin_path):
    """Read the ISO9660 primary-volume label from a raw MODE2/2352 CD image."""
    with open(bin_path, 'rb') as f:
        f.seek(16*2352+24)
        pvd = f.read(2048)
    if pvd[:7] != b'\x01CD001\x01':
        raise ValueError('Primary volume descriptor not found at sector 16 (MODE2/2352)')
    return pvd[40:72].rstrip(b' '), dict(source=str(bin_path), sector=16, offset=24,
                                          pvd_sha256=_sha(pvd))


@dataclass(frozen=True)
class EntradasNomeadas:
    """Explicit named inputs that the original program obtains from Windows.

    None of them is a game-state default; each is recorded in the capture.
    """
    diretorio_instalacao: bytes      # GetCurrentDirectoryA result (installer TemplateTargetDir)
    unidade_cd: bytes                # drive letter that FindCD probes first as CD-ROM
    rotulo_cd: bytes                 # GetVolumeInformationA label, from the BIN PVD
    relogio_ms: tuple                # ordered timeGetTime/GetTickCount results
    preenchimento_alocacao: int      # initial byte of non-ZEROINIT GlobalAlloc memory
    estado_memoria: bytes            # 32-byte MEMORYSTATUS written by GlobalMemoryStatus
    teclas: tuple                    # ordered GetAsyncKeyState answers: (vkey, i16 result)
    id_thread: int                   # GetCurrentThreadId stored by __InitThreadData
    proveniencia: dict = field(default_factory=dict)

    def __post_init__(self):
        if (not self.diretorio_instalacao or b'\0' in self.diretorio_instalacao
                or len(self.unidade_cd) != 1 or not self.unidade_cd.isalpha()
                or not 0 <= self.preenchimento_alocacao <= 255 or len(self.estado_memoria) != 32
                or not self.rotulo_cd):
            raise ValueError('Declare every named Windows input explicitly')

    def manifesto(self):
        return dict(install_directory=self.diretorio_instalacao.decode('latin-1'),
                    cd_drive=self.unidade_cd.decode(), cd_volume_label=self.rotulo_cd.decode('latin-1'),
                    clock_ms=list(self.relogio_ms), allocation_fill=self.preenchimento_alocacao,
                    memory_status_hex=self.estado_memoria.hex(),
                    async_keys=[list(t) for t in self.teclas], thread_id=self.id_thread,
                    provenance=self.proveniencia)


class MidiaOriginal:
    """Read-only resolution of Windows paths to the original media copies."""
    def __init__(self, entradas, cd_dir=None):
        self.cd = Path(cd_dir or ambiente_missoes.CD)
        self.instalacao = self.cd / 'INSTALHD'
        self.raizes = {entradas.diretorio_instalacao.lower().rstrip(b'\\'): self.instalacao,
                       entradas.unidade_cd.lower() + b':': self.cd}
        self.dir_corrente = entradas.diretorio_instalacao.lower().rstrip(b'\\')
        self.lidos = {}

    def resolver(self, caminho):
        bruto = bytes(caminho)
        nome = bruto.lower().replace(b'/', b'\\')
        if len(nome) < 2 or nome[1:2] != b':':
            nome = self.dir_corrente + b'\\' + nome.lstrip(b'\\')
        for raiz, destino in sorted(self.raizes.items(), key=lambda x: -len(x[0])):
            if nome == raiz or nome.startswith(raiz + b'\\'):
                atual = destino
                # '.\\' components (e.g. "./monstre.ini", the idiom that makes a
                # private-profile name relative to the current directory) are no-ops.
                for parte in [p for p in nome[len(raiz):].split(b'\\') if p and p != b'.']:
                    if parte == b'..' or not atual.is_dir():
                        return None
                    achados = [c for c in atual.iterdir() if c.name.lower().encode('latin-1') == parte]
                    if len(achados) != 1:
                        return None
                    atual = achados[0]
                return atual if atual.is_file() else None
        raise ParadaVinculoDeclarado(f'Path outside the declared install/CD roots: {bruto!r}')

    def ler(self, caminho):
        arquivo = self.resolver(caminho)
        if arquivo is None:
            return None, None
        dados = arquivo.read_bytes()
        self.lidos[str(arquivo)] = dict(path=str(arquivo.relative_to(self.cd.parent)),
                                        bytes=len(dados), sha256=_sha(dados))
        return arquivo, dados


class ArenaAlocacoes:
    """Finite explicit GlobalAlloc arena with handle==pointer GMEM_FIXED identity.

    The whole arena is mapped once (per-allocation mapping would flush the
    native translation cache thousands of times). Each allocation receives a
    fresh page-aligned range that is never reused; its contents are the
    declared fill byte (ZEROINIT gives zero, as documented by Windows). A freed
    range keeps its bytes but is marked inactive; later handle/lock/free on it
    stops. Bytes outside active ranges are not part of any declared block.
    """
    def __init__(self, cpu, base, limite, maximo, preenchimento):
        self.cpu, self.base, self.limite = cpu, base, limite
        self.maximo, self.preenchimento = maximo, preenchimento
        self.proximo = base
        self.recursos, self.ordem = {}, []
        cpu.mem_map(base, limite-base)

    def alocar(self, chamada):
        flags, tamanho = chamada.argumentos
        if flags & ~GMEM_ZEROINIT or not 0 < tamanho <= 0x2000000:
            raise ParadaVinculoDeclarado(f'GlobalAlloc flags 0x{flags:x}/size {tamanho} outside fixed fixture')
        if len(self.ordem) >= self.maximo:
            raise ParadaVinculoDeclarado('Declared GlobalAlloc count budget exhausted')
        paginas = (tamanho+0xfff) & ~0xfff
        ponteiro = self.proximo
        if ponteiro+paginas > self.limite:
            raise ParadaVinculoDeclarado('Declared GlobalAlloc address budget exhausted')
        self.proximo += paginas
        inicial = 0 if flags & GMEM_ZEROINIT else self.preenchimento
        self.cpu.mem_write(ponteiro, bytes([inicial])*tamanho)
        self.recursos[ponteiro] = dict(index=len(self.ordem), pointer=ponteiro, size=tamanho,
                                       flags=flags, initial_byte=inicial,
                                       caller_return=hex(chamada.retorno), active=True, locks=0,
                                       events=['alloc'], stack=[hex(x) for x in struct.unpack(
                                           '<8I', chamada.ler(chamada.registradores['ESP']+4, 32))])
        self.ordem.append(ponteiro)
        return ponteiro

    def reservar(self, chamada):
        """VirtualAlloc(NULL, size, MEM_COMMIT[|MEM_RESERVE], RW/RWX): new zeroed pages."""
        endereco, tamanho, tipo, protecao = chamada.argumentos
        if endereco or tipo not in (0x1000, 0x3000) or protecao not in (4, 0x40) or not 0 < tamanho <= 0x1000000:
            raise ParadaVinculoDeclarado(f'VirtualAlloc 0x{endereco:x}/{tamanho}/0x{tipo:x}/0x{protecao:x} outside fixture')
        paginas = (tamanho+0xfff) & ~0xfff
        ponteiro = self.proximo
        if ponteiro+paginas > self.limite or len(self.ordem) >= self.maximo:
            raise ParadaVinculoDeclarado('Declared VirtualAlloc budget exhausted')
        self.proximo += paginas
        self.cpu.mem_write(ponteiro, bytes(paginas))
        self.recursos[ponteiro] = dict(index=len(self.ordem), pointer=ponteiro, size=paginas, flags=tipo,
                                       initial_byte=0, caller_return=hex(chamada.retorno), active=True,
                                       locks=0, events=['virtual_alloc'], kind='VirtualAlloc')
        self.ordem.append(ponteiro)
        return ponteiro

    def _recurso(self, valor, operacao):
        r = self.recursos.get(valor)
        if r is None or not r['active']:
            raise ParadaVinculoDeclarado(f'{operacao} on unknown or freed fixture handle/pointer 0x{valor:x}')
        r['events'].append(operacao)
        return r

    def fixar(self, chamada):
        r = self._recurso(chamada.argumentos[0], 'lock')
        r['locks'] += 1
        return r['pointer']

    def handle(self, chamada):
        return self._recurso(chamada.argumentos[0], 'handle')['pointer']

    def desfixar(self, chamada):
        r = self._recurso(chamada.argumentos[0], 'unlock')
        if r['locks'] <= 0:
            raise ParadaVinculoDeclarado('GlobalUnlock without a retained fixture lock')
        r['locks'] -= 1
        return 0   # GMEM_FIXED: no lock remains; the original ignores this result

    def liberar(self, chamada):
        r = self._recurso(chamada.argumentos[0], 'free')
        if r['locks']:
            raise ParadaVinculoDeclarado('GlobalFree of a fixture allocation with retained lock')
        dados = bytes(self.cpu.mem_read(r['pointer'], r['size']))
        r.update(active=False, freed_sha256=_sha(dados), freed_caller_return=hex(chamada.retorno))
        return 0   # NULL means success; the original ignores this result

    def ativos(self):
        return [self.recursos[p] for p in self.ordem if self.recursos[p]['active']]

    def manifesto(self):
        return [dict({k: v for k, v in self.recursos[p].items() if k != 'events'},
                     pointer=hex(p), events=' '.join(self.recursos[p]['events']))
                for p in self.ordem]


class ArquivosCRT:
    """fopen/fread/fclose/FileSeek fixture over read-only original media.

    The FILE* identity is an unmapped opaque value: any CRT body that would
    dereference it (fgets/ftell/fwrite) faults rather than returning invented data.
    """
    BASE_FLUXO = 0x7f000000

    def __init__(self, midia, maximo=4096):
        self.midia, self.maximo = midia, maximo
        self.abertos, self.historico = {}, []
        self.proximo = 0

    def fopen(self, chamada):
        caminho = _cadeia(chamada, chamada.argumentos[0], 512)
        modo = _cadeia(chamada, chamada.argumentos[1], 16)
        if modo not in (b'rb', b'r'):
            raise ParadaVinculoDeclarado(f'fopen mode {modo!r} is outside the read-only fixture')
        if self.proximo >= self.maximo:
            raise ParadaVinculoDeclarado('Declared fopen budget exhausted')
        arquivo, dados = self.midia.ler(caminho)
        registro = dict(path=caminho.decode('latin-1'), mode=modo.decode(),
                        file=None if arquivo is None else self.midia.lidos[str(arquivo)]['path'])
        self.historico.append(registro)
        if arquivo is None:
            # The original media really lacks this path under the declared roots.
            registro['result'] = 'NULL (absent from original media)'
            return 0
        self.proximo += 1
        fluxo = self.BASE_FLUXO + 0x100*self.proximo
        self.abertos[fluxo] = dict(data=dados, cursor=0, record=registro, reads=0)
        registro['stream'] = hex(fluxo)
        return fluxo

    def _fluxo(self, fluxo):
        if fluxo not in self.abertos:
            raise ParadaVinculoDeclarado(f'CRT stream 0x{fluxo:x} is not an open fixture stream')
        return self.abertos[fluxo]

    def fread(self, chamada):
        destino, tamanho, quantidade, fluxo = chamada.argumentos
        f = self._fluxo(fluxo)
        if not tamanho or not quantidade:
            return 0
        if tamanho*quantidade > 0x1000000:
            raise ParadaVinculoDeclarado('fread request exceeds the declared fixture transfer size')
        disponivel = len(f['data'])-f['cursor']
        itens = min(quantidade, max(disponivel, 0)//tamanho)
        parcial = 0 if itens == quantidade else min(disponivel-itens*tamanho, tamanho)
        n = itens*tamanho+max(parcial, 0)
        if n:
            chamada.escrever(destino, f['data'][f['cursor']:f['cursor']+n])
        f['cursor'] += n
        f['reads'] += 1
        return itens

    def fclose(self, chamada):
        f = self._fluxo(chamada.argumentos[0])
        f['record'].update(closed=True, final_cursor=f['cursor'], reads=f['reads'])
        del self.abertos[chamada.argumentos[0]]
        return 0

    def file_seek(self, chamada):
        deslocamento, origem = chamada.argumentos
        fluxo = struct.unpack('<I', chamada.ler(0x4e1d1c, 4))[0]
        f = self._fluxo(fluxo)
        if origem not in SEEK:
            raise ParadaVinculoDeclarado(f'fseek origin {origem} outside fixture')
        base = (0, f['cursor'], len(f['data']))[origem]
        alvo = base+(deslocamento if deslocamento < 0x80000000 else deslocamento-0x100000000)
        if alvo < 0:
            raise ParadaVinculoDeclarado('fseek before file start is outside the fixture')
        f['cursor'] = alvo
        return 0

    def fseek_crt(self, chamada):
        """CRT fseek 0x48cda2 (Core inventory): EAX FILE*, EDX s32 offset, EBX whence; EAX 0."""
        fluxo, deslocamento, origem = chamada.argumentos
        f = self._fluxo(fluxo)
        if origem not in SEEK:
            raise ParadaVinculoDeclarado(f'fseek whence {origem} (errno path) is outside the fixture')
        base = (0, f['cursor'], len(f['data']))[origem]
        alvo = base+(deslocamento if deslocamento < 0x80000000 else deslocamento-0x100000000)
        if alvo < 0:
            raise ParadaVinculoDeclarado('fseek before file start is outside the fixture')
        f['cursor'] = alvo
        return 0

    def fgets_crt(self, chamada):
        """CRT fgets 0x48ce96 (Core inventory): EAX buf, EDX n, EBX FILE*; EAX buf, or 0 at EOF.

        Stores at most n-1 bytes up to and including LF, then a NUL. Only binary
        streams are declared: a text-mode stream reaching a CR would need the CRT
        CR/LF translation, which this fixture does not model, so it stops.
        """
        destino, n, fluxo = chamada.argumentos
        f = self._fluxo(fluxo)
        n = n if n < 0x80000000 else n-0x100000000
        if n <= 1:
            if n == 1:
                chamada.escrever(destino, b'\0')
            return destino
        dados, c = f['data'], f['cursor']
        if c >= len(dados):
            return 0
        fim = dados.find(b'\n', c, c+n-1)
        linha = dados[c:(fim+1 if fim >= 0 else min(c+n-1, len(dados)))]
        if f['record']['mode'] == 'r' and b'\r' in linha:
            raise ParadaVinculoDeclarado('fgets on a text-mode stream with CR: CRT CR/LF translation not declared')
        chamada.escrever(destino, linha+b'\0')
        f['cursor'] = c+len(linha)
        f['reads'] += 1
        return destino


class ArquivosWin32:
    """KERNEL32 file-handle fixture reached only through original CRT bodies.

    debugSymLoad (IaAlloc) uses Watcom open/lseek/read/close, whose original
    bodies call CreateFileA/SetFilePointer/ReadFile/CloseHandle. Only
    read-only OPEN_EXISTING access to the original media is supported.
    """
    BASE = 0x7e000000

    def __init__(self, midia, maximo=256):
        self.midia, self.maximo = midia, maximo
        self.abertos, self.historico, self.proximo = {}, [], 0
        self.ultimo_erro = None

    def criar(self, chamada):
        nome, acesso, _, _, criacao, _, modelo = chamada.argumentos
        caminho = _cadeia(chamada, nome, 512)
        if acesso != 0x80000000 or criacao != 3 or modelo:
            raise ParadaVinculoDeclarado(f'CreateFileA access 0x{acesso:x}/disposition {criacao} outside fixture')
        arquivo, dados = self.midia.ler(caminho)
        registro = dict(path=caminho.decode('latin-1'),
                        file=None if arquivo is None else self.midia.lidos[str(arquivo)]['path'])
        self.historico.append(registro)
        if arquivo is None:
            self.ultimo_erro = 2   # ERROR_FILE_NOT_FOUND: the path is absent from the media
            registro['result'] = 'INVALID_HANDLE_VALUE'
            return 0xffffffff
        if self.proximo >= self.maximo:
            raise ParadaVinculoDeclarado('Declared CreateFileA budget exhausted')
        self.proximo += 1
        h = self.BASE+4*self.proximo
        self.abertos[h] = dict(data=dados, cursor=0, record=registro)
        registro['handle'] = hex(h)
        return h

    def _h(self, h):
        if h not in self.abertos:
            raise ParadaVinculoDeclarado(f'Win32 handle 0x{h:x} is not an open fixture file')
        return self.abertos[h]

    def ler(self, chamada):
        h, destino, n, lidos, sobreposto = chamada.argumentos
        f = self._h(h)
        if sobreposto or not lidos:
            raise ParadaVinculoDeclarado('ReadFile overlapped/without count is outside fixture')
        bloco = f['data'][f['cursor']:f['cursor']+n]
        if bloco:
            chamada.escrever(destino, bloco)
        f['cursor'] += len(bloco)
        chamada.escrever(lidos, struct.pack('<I', len(bloco)))
        return 1

    def posicionar(self, chamada):
        h, distancia, alta, metodo = chamada.argumentos
        f = self._h(h)
        if alta and struct.unpack('<i', chamada.ler(alta, 4))[0] not in (0, -1):
            raise ParadaVinculoDeclarado('SetFilePointer 64-bit distance outside fixture')
        if metodo not in (0, 1, 2):
            raise ParadaVinculoDeclarado('SetFilePointer method outside fixture')
        delta = distancia-0x100000000 if distancia & 0x80000000 else distancia
        alvo = (0, f['cursor'], len(f['data']))[metodo]+delta
        if alvo < 0:
            raise ParadaVinculoDeclarado('SetFilePointer before file start')
        f['cursor'] = alvo
        if alta:
            chamada.escrever(alta, struct.pack('<I', 0))
        return alvo

    def fechar(self, chamada):
        h, = chamada.argumentos
        f = self._h(h)
        f['record'].update(closed=True, final_cursor=f['cursor'])
        del self.abertos[h]
        return 1

    def tipo(self, chamada):
        h, = chamada.argumentos
        if h in self.abertos:
            return 1   # FILE_TYPE_DISK
        raise ParadaVinculoDeclarado(f'GetFileType(0x{h:x}) on an undeclared handle')

    def erro(self, chamada):
        if self.ultimo_erro is None:
            raise ParadaVinculoDeclarado('GetLastError without a declared preceding failure')
        valor, self.ultimo_erro = self.ultimo_erro, None
        return valor


def _cadeia(chamada, endereco, maximo):
    dados = chamada.ler(endereco, 1)
    texto = b''
    while dados != b'\0':
        texto += dados
        if len(texto) > maximo:
            raise ParadaVinculoDeclarado('Unterminated string argument')
        dados = chamada.ler(endereco+len(texto), 1)
    return texto


def _analisar_ini(dados):
    """Windows private-profile reading subset: sections and first-match keys.

    Lines whose first non-blank byte is ';' are comments; spaces/tabs around
    names and values are trimmed; inline text after the value is retained.
    A queried key with duplicates raises instead of choosing an occurrence.
    """
    secoes, atual = {}, None
    for linha in bytes(dados).split(b'\n'):
        linha = linha.rstrip(b'\r').strip(b' \t')
        if not linha or linha.startswith(b';'):
            continue
        if linha.startswith(b'['):
            fim = linha.find(b']')
            if fim < 0:
                continue
            atual = linha[1:fim].strip(b' \t').lower()
            secoes.setdefault(atual, {})
            continue
        chave, igual, valor = linha.partition(b'=')
        if atual is None or not igual:
            continue
        secoes[atual].setdefault(chave.strip(b' \t').lower(), []).append(valor.strip(b' \t'))
    return secoes


class PerfilWindows:
    def __init__(self, midia):
        self.midia, self.cache, self.chamadas = midia, {}, []

    def _valor(self, secao, chave, arquivo):
        if arquivo not in self.cache:
            caminho, dados = self.midia.ler(arquivo)
            if caminho is None:
                raise ParadaVinculoDeclarado(f'Profile file {arquivo!r} absent from original media')
            self.cache[arquivo] = _analisar_ini(dados)
        valores = self.cache[arquivo].get(secao.lower(), {}).get(chave.lower())
        if valores and len(valores) > 1:
            raise ParadaVinculoDeclarado(f'Duplicate profile key {secao!r}/{chave!r} is ambiguous')
        return None if not valores else valores[0]

    def inteiro(self, chamada):
        app, chave, padrao, arquivo = chamada.argumentos
        if not app or not chave:
            raise ParadaVinculoDeclarado('Profile enumeration is outside the fixture')
        s, k, f = (_cadeia(chamada, a, 512) for a in (app, chave, arquivo))
        valor = self._valor(s, k, f)
        if valor is None:
            resultado = padrao
        elif valor.isdigit():
            resultado = int(valor) & 0xffffffff
        else:
            raise ParadaVinculoDeclarado(f'Profile integer {s!r}/{k!r}={valor!r} outside decimal subset')
        self.chamadas.append(('int', s, k, padrao, f, resultado))
        return resultado

    def texto(self, chamada):
        app, chave, padrao, destino, tamanho, arquivo = chamada.argumentos
        if not app or not chave or not tamanho:
            raise ParadaVinculoDeclarado('Profile enumeration/zero buffer is outside the fixture')
        s, k, f = (_cadeia(chamada, a, 512) for a in (app, chave, arquivo))
        valor = self._valor(s, k, f)
        if valor is None:
            valor = _cadeia(chamada, padrao, 4096) if padrao else b''
        if len(valor) >= 2 and valor[:1] == valor[-1:] and valor[:1] in (b'"', b"'"):
            valor = valor[1:-1]
        resultado = valor[:tamanho-1]
        chamada.escrever(destino, resultado+b'\0')
        self.chamadas.append(('string', s, k, f, tamanho, resultado))
        return len(resultado)


class WindowsDeclarado:
    """Small KERNEL32/USER32/WINMM answers taken from EntradasNomeadas."""
    def __init__(self, entradas):
        self.e = entradas
        self.relogio = list(entradas.relogio_ms)
        self.teclas = list(entradas.teclas)
        self.consumidos = []

    def tempo(self, chamada):
        if not self.relogio:
            raise ParadaVinculoDeclarado('Declared clock sequence exhausted')
        valor = self.relogio.pop(0)
        self.consumidos.append(('clock', hex(chamada.retorno), valor))
        return valor

    def tecla(self, chamada):
        vk, = chamada.argumentos
        if not self.teclas or self.teclas[0][0] != vk:
            raise ParadaVinculoDeclarado(f'GetAsyncKeyState(0x{vk:x}) is not the next declared key answer')
        _, valor = self.teclas.pop(0)
        self.consumidos.append(('key', hex(chamada.retorno), vk, valor))
        return valor & 0xffff

    def estado_memoria(self, chamada):
        chamada.escrever(chamada.argumentos[0], self.e.estado_memoria)
        return 0

    def diretorio(self, chamada):
        tamanho, destino = chamada.argumentos
        texto = self.e.diretorio_instalacao
        if len(texto)+1 > tamanho:
            raise ParadaVinculoDeclarado('GetCurrentDirectoryA buffer smaller than declared directory')
        chamada.escrever(destino, texto+b'\0')
        return len(texto)

    def tipo_unidade(self, chamada):
        raiz = _cadeia(chamada, chamada.argumentos[0], 16).lower()
        if raiz == self.e.unidade_cd.lower()+b':\\':
            return 5   # DRIVE_CDROM
        if len(raiz) == 3 and raiz[1:] == b':\\' and b'd' <= raiz[:1] < self.e.unidade_cd.lower():
            return 1   # DRIVE_NO_ROOT_DIR: declared absent drive probed before the CD drive
        raise ParadaVinculoDeclarado(f'GetDriveTypeA({raiz!r}) is not a declared drive')

    def volume(self, chamada):
        raiz, nome, tamanho = chamada.argumentos[:3]
        if _cadeia(chamada, raiz, 16).lower() != self.e.unidade_cd.lower()+b':\\':
            raise ParadaVinculoDeclarado('GetVolumeInformationA on an undeclared drive')
        if len(self.e.rotulo_cd)+1 > tamanho:
            raise ParadaVinculoDeclarado('Volume label buffer too small for declared label')
        # Only the label is written; serial/length/flags/filesystem outputs are
        # left untouched and FindCD reads only the label (strnicmp at 0x45859b).
        chamada.escrever(nome, self.e.rotulo_cd+b'\0')
        return 1

    @staticmethod
    def constante(valor, rotulo):
        def atender(chamada):
            return valor
        atender.__doc__ = rotulo
        return atender
