"""Python replays of the native capture scenarios, producing capture-shaped records.

Each function mirrors one ``capturar_som`` scenario with the same fixture
(``provedores_som.SistemaFixo``), the same inherited bytes and the same
inputs, but runs the reconstruction in ``bancos_som``/``adpcm_som``. Equal
records mean equal effects, call order, arguments, results and buffers.
"""
import struct
from adpcm_som import (criar_superficie_som, decodificar_ima_estereo16, decodificar_ima_mono16,
                       iniciar_buffer_comprimido)
from bancos_som import (BancoSom, GlobaisSom, abrir_banco, arquivo_som, cabecalho_dados_som,
                        carregar_dados_em_memoria, carregar_info_som, carregar_todos_dados, criar_caminho_sons,
                        criar_id_som, entradas_banco, procurar_som, validar_cabecalho_banco)
from cenarios_som import (ARENA, ARENA_TAMANHO, ARGUMENTO_INFO, BANCOS, CONTADOR_INFO, CONTADORES_VARIANTE,
                          DECODIFICADOR_DIRETO, DIRETORIO, DIRETORIOS_TESTE, ECX_INFO, HERDADO_HANDLE, MAKE_ID,
                          NOME_ARQUIVO_BYTES, OBJETO_DIRECTSOUND, PREFIXO, arquivos_originais, arquivos_z,
                          banco_sintetico_superficies, banco_validacao, entrada_decodificador,
                          entradas_saturacao, sha)
from ambiente_audio import LETRAS_BANCO
from provedores_som import ParadaFixture, SistemaFixo


class Mundo:
    """Python-side equivalent of one bench: fixture, zeroed .bss globals and bank records."""

    def __init__(self, arquivos, diretorio=DIRETORIO, falhar_alocacao=()):
        self.sistema = SistemaFixo(arquivos, diretorio_corrente=diretorio, arena=ARENA,
                                   arena_tamanho=ARENA_TAMANHO, falhar_alocacao=falhar_alocacao)
        self.registro = self.sistema.registro
        self.globais = GlobaisSom(nome_arquivo=bytearray(NOME_ARQUIVO_BYTES), diretorio=bytearray(256),
                                  contador_variantes=0, contador_alocacoes=0, janela=0, comprimido=0,
                                  directsound=OBJETO_DIRECTSOUND)
        self.bancos = {letra: BancoSom(bytearray(28), endereco) for letra, endereco in BANCOS.items()}

    def chamar(self, funcao, *argumentos):
        inicio = len(self.registro)
        try:
            resultado, parada = funcao(*argumentos), None
        except ParadaFixture as erro:
            resultado, parada = None, str(erro)
        return resultado, [list(item) for item in self.registro[inicio:]], parada

    def estado(self, letra):
        return dict(record_hex=bytes(self.bancos[letra].registro).hex(),
                    file_name_hex=bytes(self.globais.nome_arquivo).hex(),
                    allocations=self.globais.contador_alocacoes)


def abrir(mundo, letra, nome=None):
    sistema, globais, banco = mundo.sistema, mundo.globais, mundo.bancos[letra]
    inicio = len(mundo.registro)
    criar_caminho_sons(sistema, globais)
    nome = arquivo_som(globais, letra.encode())
    eax, _, parada = mundo.chamar(abrir_banco, sistema, globais, nome, banco)
    estado = mundo.estado(letra)
    texto = bytes(globais.diretorio)
    estado.update(eax=eax, stop=parada, log=[list(item) for item in mundo.registro[inicio:]],
                  sound_directory=texto[:texto.index(0)].decode('latin-1'), bank_path=nome.decode('latin-1'),
                  header_sha256=sha(banco.cabecalho) if eax == 1 else None)
    return estado


def superficie(mundo, letra, deslocamento, chave):
    banco = mundo.bancos[letra]
    cabecalho = banco.cabecalho[deslocamento:deslocamento + 16]
    resultado, log, parada = mundo.chamar(criar_superficie_som, mundo.sistema, mundo.globais, banco, cabecalho)
    objeto, retornos = resultado if resultado else (0, [])
    conteudo = mundo.sistema.directsound.conteudos.get(objeto) if objeto else None
    chave.update(data_header_hex=bytes(cabecalho).hex(), eax_object=objeto, stop=parada, log=log,
                 decoder_returns=retornos, buffer_bytes=len(conteudo) if conteudo is not None else None,
                 buffer_sha256=sha(conteudo) if conteudo is not None else None)
    return chave


def reproduzir_banco(letra, memoria_amostras=3, conteudos=None):
    """Bank scenario; ``conteudos`` (optional dict) receives each decoded buffer."""
    mundo = Mundo(arquivos_originais(letra))
    caso = dict(bank=letra, open=abrir(mundo, letra))
    eax, log, _ = mundo.chamar(iniciar_buffer_comprimido, mundo.sistema, mundo.globais)
    caso['init_compressed'] = dict(eax=eax, pointer=mundo.globais.comprimido, log=log)
    banco = mundo.bancos[letra]
    sons = []
    for indice, (ident, _, variantes, deslocamento) in enumerate(entradas_banco(banco)):
        for variante in range(max(variantes, 1)):
            som = superficie(mundo, letra, deslocamento + 16 * variante, dict(
                index=indice, id=ident, variant=variante, data_header_offset=deslocamento + 16 * variante))
            if conteudos is not None and som['eax_object']:
                conteudos[(indice, variante)] = mundo.sistema.directsound.conteudos[som['eax_object']]
            sons.append(som)
    caso['surfaces_from_file'] = sons
    mundo = Mundo(arquivos_originais(letra))
    abrir(mundo, letra)
    iniciar_buffer_comprimido(mundo.sistema, mundo.globais)
    banco = mundo.bancos[letra]
    eax, log, parada = mundo.chamar(carregar_dados_em_memoria, mundo.sistema, mundo.globais, banco)
    caso['load_data_in_memory'] = dict(eax=eax, stop=parada, log=log, state=mundo.estado(letra),
                                       data_sha256=sha(banco.dados) if banco.ponteiro_dados else None)
    escolhidos = [s for s in sons if s['data_header_hex'][24:26] == '00'][:1] + sons[:memoria_amostras]
    caso['surfaces_from_memory'] = [superficie(mundo, letra, s['data_header_offset'],
                                               {k: s[k] for k in ('index', 'id', 'variant', 'data_header_offset')})
                                    for s in escolhidos]
    return caso


def reproduzir_indice():
    mundo = Mundo(arquivos_originais())
    resultado = {}
    for letra in LETRAS_BANCO:
        abrir(mundo, letra)
        banco, globais = mundo.bancos[letra], mundo.globais
        ids = [e[0] for e in entradas_banco(banco)]
        ausentes = sorted({0xffffffff, 0x00ffffff, max(ids) + 1, 0x7fff0000, 0} - set(ids))
        busca = [dict(id=i, entry_offset=procurar_som(i, banco)) for i in ids + ausentes]
        variantes = []
        for indice in range(banco.quantidade):
            for inicial in CONTADORES_VARIANTE:
                globais.contador_variantes = inicial
                deslocamento = cabecalho_dados_som(globais, 12 * indice, banco)
                variantes.append(dict(index=indice, counter_before=inicial, counter_after=globais.contador_variantes,
                                      data_header_offset=deslocamento))
        info = []
        for i in ids + ausentes[:2]:
            registro = bytearray([HERDADO_HANDLE]) * 0x40
            globais.contador_variantes = CONTADOR_INFO
            eax = carregar_info_som(globais, registro, i, banco, ECX_INFO, ARGUMENTO_INFO)
            info.append(dict(id=i, eax=eax, counter_after=globais.contador_variantes, handle_hex=registro.hex()))
        resultado[letra] = dict(header_pointer=banco.ponteiro_cabecalho, find=busca, get_data_header=variantes,
                                load_data_info=info)
    resultado['make_id'] = [dict(eax=a, edx=b, ebx=c, result=criar_id_som(a, b, c)) for a, b, c in MAKE_ID]
    return resultado


def _abrir_z(mundo, registro=None, nome_arquivo=None):
    if registro is not None:
        mundo.bancos['A'].registro[:] = registro
    if nome_arquivo is not None:
        mundo.globais.nome_arquivo[:] = nome_arquivo
    return mundo.chamar(abrir_banco, mundo.sistema, mundo.globais, PREFIXO + b'Z', mundo.bancos['A'])


def reproduzir_validacao():
    casos = []
    hed_ok, snd, variantes = banco_validacao()
    for nome, (hed, dados) in variantes.items():
        for herdado in (0x00, 0xa5):
            mundo = Mundo(arquivos_z(hed, dados))
            eax, log, parada = _abrir_z(mundo, bytes([herdado]) * 28, bytes([herdado]) * NOME_ARQUIVO_BYTES)
            casos.append(dict(case=nome, inherited=herdado, routine='BanqSon_Open', eax=eax, stop=parada, log=log,
                              **mundo.estado('A')))
    mundo = Mundo(arquivos_z(hed_ok, snd))
    eax, log, parada = _abrir_z(mundo, struct.pack('<I', 1) + b'\xa5' * 24)
    casos.append(dict(case='already_open', inherited=0xa5, routine='BanqSon_Open', eax=eax, stop=parada, log=log,
                      **mundo.estado('A')))
    mundo = Mundo(arquivos_z(hed_ok, snd), falhar_alocacao=(0,))
    eax, log, parada = _abrir_z(mundo)
    casos.append(dict(case='header_allocation_failure', inherited=0, routine='BanqSon_Open', eax=eax, stop=parada,
                      log=log, **mundo.estado('A')))
    reais = arquivos_originais()
    for nome, hed in [(f'{l}.HED', reais[PREFIXO + f'{l}.HED'.encode()]) for l in LETRAS_BANCO] + [
            ('bad_magic', variantes['bad_magic'][0])]:
        mundo = Mundo({PREFIXO + b'Q.HED': hed})
        handle = mundo.sistema.arquivos.abrir(PREFIXO + b'Q.HED', 0)
        banco = mundo.bancos['A']
        banco.registro[:] = b'\xa5' * 28
        resultado, log, parada = mundo.chamar(validar_cabecalho_banco, mundo.sistema, handle, banco)
        casos.append(dict(case=nome, inherited=0xa5, routine='BanqSon_ControleValiditeHeader',
                          eax=resultado[0] if resultado else None, stop=parada, log=log,
                          fixture_setup='handle opened by the fixture before the call',
                          out_hex=struct.pack('<I', resultado[1]).hex(), record_hex=bytes(banco.registro).hex()))
    for nome, dados in (('complete', snd), ('short_snd', snd[:1000])):
        mundo = Mundo(arquivos_z(hed_ok, dados))
        _abrir_z(mundo)
        resultado, log, parada = mundo.chamar(carregar_todos_dados, mundo.sistema, mundo.globais, mundo.bancos['A'])
        casos.append(dict(case=nome, inherited=0, routine='BanqSon_LoadAllData', eax=resultado[0], stop=parada,
                          log=log, data_sha256=sha(resultado[1]) if resultado[0] else None, **mundo.estado('A')))
    mundo = Mundo({})
    mundo.bancos['A'].registro[:] = b'\0' * 4 + b'\xa5' * 24
    eax, log, parada = mundo.chamar(carregar_dados_em_memoria, mundo.sistema, mundo.globais, mundo.bancos['A'])
    casos.append(dict(case='closed_bank', inherited=0xa5, routine='BanqSon_LoadDataInMemory', eax=eax, stop=parada,
                      log=log, **mundo.estado('A')))
    caminhos = []
    for cwd in DIRETORIOS_TESTE:
        mundo = Mundo({}, diretorio=cwd)
        mundo.globais.diretorio[:64] = b'\xa5' * 64
        inicio = len(mundo.registro)
        criar_caminho_sons(mundo.sistema, mundo.globais)
        nome = arquivo_som(mundo.globais, b'P')
        caminhos.append(dict(cwd=cwd.decode('latin-1'), sound_directory_hex=bytes(mundo.globais.diretorio[:64]).hex(),
                             sound_file=nome.decode('latin-1'), log=[list(i) for i in mundo.registro[inicio:]]))
    return dict(cases=casos, paths=caminhos)


def _direto(tipo, semente, bloco, origem):
    dados, eax = (decodificar_ima_mono16 if tipo == 'm16' else decodificar_ima_estereo16)(origem, bloco)
    janela = len(origem) * 4 + 64
    return dict(decoder=tipo, seed=semente, block_align=bloco, input_bytes=len(origem), input_sha256=sha(origem),
                eax=eax, stop=None, output_sha256=sha(dados + b'\xcd' * (janela - len(dados))),
                output_window=janela, poison='0xcd')


def reproduzir_decodificador():
    diretos = [_direto(tipo, semente, bloco, entrada_decodificador(tipo, semente, bloco, n))
               for tipo, semente, bloco, n in DECODIFICADOR_DIRETO]
    diretos += [_direto(*caso) for caso in entradas_saturacao()]
    hed, snd = banco_sintetico_superficies()
    superficies = []
    mundo = Mundo(arquivos_z(hed, snd))
    _abrir_z(mundo)
    iniciar_buffer_comprimido(mundo.sistema, mundo.globais)
    for i in range(4):
        superficies.append(superficie(mundo, 'A', 48 + 16 * i, dict(synthetic=i, path='file')))
    eax, log, parada = mundo.chamar(carregar_dados_em_memoria, mundo.sistema, mundo.globais, mundo.bancos['A'])
    apos_leitura = dict(case='load_data_in_memory_after_reads', eax=eax, stop=parada, log=log, **mundo.estado('A'))
    mundo = Mundo(arquivos_z(hed, snd))
    _abrir_z(mundo)
    iniciar_buffer_comprimido(mundo.sistema, mundo.globais)
    carregar_dados_em_memoria(mundo.sistema, mundo.globais, mundo.bancos['A'])
    for i in range(4):
        superficies.append(superficie(mundo, 'A', 48 + 16 * i, dict(synthetic=i, path='memory')))
    return dict(direct=diretos, synthetic_bank=dict(hed_sha256=sha(hed), snd_sha256=sha(snd)),
                surfaces=superficies, memory_after_reads=apos_leitura)
