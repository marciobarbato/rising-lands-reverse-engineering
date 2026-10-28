"""Original-only audio observations, recorded before any Python translation.

Runs the intact routines on the shared bench with the declared bindings of
``bancada_som``. Commercial bytes (HED tables, SND samples, decoded audio) are
recorded only as SHA-256; synthetic fixture inputs come from ``cenarios_som``.
Usage: ``capturar_som.py [A B P]`` (default all banks).
"""
import json
import struct
import sys
import time
from ambiente_audio import LETRAS_BANCO, ORIGINAL_SHA256, OWNED
from bancada_som import FIXOS, PONTOS_M16, PONTOS_S16, RETORNO_DECODIFICADOR, BancadaSom, ParadaFixture
from cenarios_som import (ALOCACOES, ARGUMENTO_INFO, BANCOS, COMPRIMIDO, CONTADOR, CONTADOR_INFO,
                          CONTADORES_VARIANTE, DECODIFICADOR_DIRETO, DIRETORIO, DIRETORIO_SONS,
                          DIRETORIOS_TESTE, ECX_INFO, HERDADO_HANDLE, MAKE_ID, NOME_ARQUIVO,
                          NOME_ARQUIVO_BYTES, NOME_LETRA, PREFIXO, arquivos_originais, arquivos_z,
                          banco_sintetico_superficies, banco_validacao, entrada_decodificador,
                          entradas_saturacao, sha)

PONTOS = PONTOS_M16 + PONTOS_S16 + (RETORNO_DECODIFICADOR,)
ROTINA = dict(CreateSoundPath=0x48a834, SoundFile=0x48a87f, MakeID=0x48a894, Open=0x48b5a6,
              ControleValiditeHeader=0x48b44e, LoadAllData=0x48b6e7, LoadDataInMemory=0x48b733,
              InitCompressedBuffer=0x48c16c, FindId=0x48b390, GetDataHeader=0x48b3b3,
              LoadDataInfo=0x48a0f4, Surface=0x48aad4, M16=0x48b8c9, S16=0x48ba96)
FIXTURE = ('C:\\RISING working directory; files matched by exact path; GlobalAlloc arena 0x4000000, '
           '16-byte aligned; non-zeroinit memory and new DirectSound buffers filled with 0xcd; one '
           'DirectSound buffer mapped at 0x6000000 at a time; IDirectSound pointer set to the fixture object')


def nova_bancada(arquivos, **opcoes):
    bancada = BancadaSom(arquivos, diretorio_corrente=opcoes.pop('diretorio', DIRETORIO), **opcoes)
    bancada.ativar_directsound()
    return bancada


def chamar(bancada, nome, registradores=None, argumentos=(), pontos=()):
    """One native call; returns (EAX or None, log slice, stop text or None)."""
    inicio = len(bancada.registro)
    try:
        regs = bancada.executar_chamada(ROTINA[nome], registradores, argumentos, pontos)
        return regs['EAX'], [list(item) for item in bancada.registro[inicio:]], None
    except ParadaFixture as parada:
        return None, [list(item) for item in bancada.registro[inicio:]], str(parada)


def estado_banco(bancada, letra):
    return dict(record_hex=bancada.ler(BANCOS[letra], 28).hex(),
                file_name_hex=bancada.ler(NOME_ARQUIVO, NOME_ARQUIVO_BYTES).hex(),
                allocations=bancada.u32(ALOCACOES))


def abrir(bancada, letra):
    """CreateSoundPath, SoundFile and BanqSon_Open, as InitSoundLib orders them."""
    _, log_caminho, _ = chamar(bancada, 'CreateSoundPath')
    _, log_nome, _ = chamar(bancada, 'SoundFile', {'EAX': NOME_LETRA[letra], 'EDX': FIXOS})
    nome = bancada.cadeia(FIXOS)
    eax, log, parada = chamar(bancada, 'Open', {'EAX': FIXOS, 'EDX': BANCOS[letra]})
    estado = estado_banco(bancada, letra)
    cabecalho = bancada.u32(BANCOS[letra] + 0xc)
    tamanho = len(bancada.arquivos.arquivos.get(PREFIXO + f'{letra}.HED'.encode(), b'')) - 16
    estado.update(eax=eax, stop=parada, log=log_caminho + log_nome + log,
                  sound_directory=bancada.cadeia(DIRETORIO_SONS).decode('latin-1'),
                  bank_path=nome.decode('latin-1'),
                  header_sha256=sha(bancada.ler(cabecalho, tamanho)) if eax == 1 else None)
    return estado


def capturar_superficie(bancada, letra, endereco, chave):
    bancada.observacoes.clear()
    eax, log, parada = chamar(bancada, 'Surface', {'EAX': endereco, 'EDX': BANCOS[letra]}, pontos=PONTOS)
    objeto = bancada.objetos_dsb.get(eax) if eax else None
    conteudo = bancada.directsound.conteudos.get(objeto) if objeto else None
    chave.update(data_header_hex=bancada.ler(endereco, 16).hex(), eax_object=objeto or 0, stop=parada, log=log,
                 decoder_returns=[v for k, v in bancada.observacoes if k == 'decoder_return'],
                 buffer_bytes=len(conteudo) if conteudo is not None else None,
                 buffer_sha256=sha(conteudo) if conteudo is not None else None)
    return chave


def capturar_banco(letra, memoria_amostras=3):
    bancada = nova_bancada(arquivos_originais(letra))
    caso = dict(bank=letra, open=abrir(bancada, letra))
    eax, log, _ = chamar(bancada, 'InitCompressedBuffer')
    caso['init_compressed'] = dict(eax=eax & 255, pointer=bancada.u32(COMPRIMIDO), log=log)
    cabecalho = bancada.u32(BANCOS[letra] + 0xc)
    quantidade = struct.unpack('<H', bancada.ler(BANCOS[letra] + 4, 2))[0]
    entradas = [struct.unpack('<IHHI', bancada.ler(cabecalho + 12 * i, 12)) for i in range(quantidade)]
    sons, inicio = [], time.time()
    for indice, (ident, _, variantes, deslocamento) in enumerate(entradas):
        for variante in range(max(variantes, 1)):
            sons.append(capturar_superficie(bancada, letra, cabecalho + deslocamento + 16 * variante, dict(
                index=indice, id=ident, variant=variante, data_header_offset=deslocamento + 16 * variante)))
    caso['surfaces_from_file'] = sons
    caso['file_seconds'] = round(time.time() - inicio, 1)
    caso['instructions_file'], caso['segments_file'] = bancada.instrucoes, bancada.execucoes
    # Dead-code memory path on a freshly opened bank: LoadDataInMemory does not
    # seek, so it needs the data file still at position 0.
    bancada = nova_bancada(arquivos_originais(letra))
    abrir(bancada, letra)
    chamar(bancada, 'InitCompressedBuffer')
    eax, log, parada = chamar(bancada, 'LoadDataInMemory', {'EAX': BANCOS[letra]})
    dados = bancada.u32(BANCOS[letra] + 0x14)
    tamanho = bancada.u32(BANCOS[letra] + 0x18)
    caso['load_data_in_memory'] = dict(eax=eax, stop=parada, log=log, state=estado_banco(bancada, letra),
                                       data_sha256=sha(bancada.ler(dados, tamanho)) if dados else None)
    escolhidos = [s for s in sons if s['data_header_hex'][24:26] == '00'][:1] + sons[:memoria_amostras]
    caso['surfaces_from_memory'] = [capturar_superficie(bancada, letra, cabecalho + s['data_header_offset'],
                                                        {k: s[k] for k in ('index', 'id', 'variant', 'data_header_offset')})
                                    for s in escolhidos]
    caso['instructions_memory'], caso['segments_memory'] = bancada.instrucoes, bancada.execucoes
    return caso


def capturar_indice():
    """FindIdInBanque, GetDataHeader and HndSound_LoadDataInfo over every ID."""
    bancada = nova_bancada(arquivos_originais())
    resultado = {}
    for letra in LETRAS_BANCO:
        abrir(bancada, letra)
        banco = BANCOS[letra]
        cabecalho = bancada.u32(banco + 0xc)
        quantidade = struct.unpack('<H', bancada.ler(banco + 4, 2))[0]
        ids = [bancada.u32(cabecalho + 12 * i) for i in range(quantidade)]
        ausentes = sorted({0xffffffff, 0x00ffffff, max(ids) + 1, 0x7fff0000, 0} - set(ids))
        busca = []
        for i in ids + ausentes:
            eax = chamar(bancada, 'FindId', {'EAX': i, 'EDX': banco})[0]
            busca.append(dict(id=i, entry_offset=eax - cabecalho if eax else None))
        variantes = []
        for indice in range(quantidade):
            for inicial in CONTADORES_VARIANTE:
                bancada.escrever(CONTADOR, struct.pack('<I', inicial))
                eax = chamar(bancada, 'GetDataHeader', {'EAX': cabecalho + 12 * indice, 'EDX': banco})[0]
                variantes.append(dict(index=indice, counter_before=inicial, counter_after=bancada.u32(CONTADOR),
                                      data_header_offset=eax - cabecalho))
        info = []
        for i in ids + ausentes[:2]:
            bancada.escrever(FIXOS + 0x100, bytes([HERDADO_HANDLE]) * 0x40)
            bancada.escrever(CONTADOR, struct.pack('<I', CONTADOR_INFO))
            eax = chamar(bancada, 'LoadDataInfo', {'EAX': FIXOS + 0x100, 'EDX': i, 'EBX': banco, 'ECX': ECX_INFO},
                         argumentos=(ARGUMENTO_INFO,))[0]
            info.append(dict(id=i, eax=eax, counter_after=bancada.u32(CONTADOR),
                             handle_hex=bancada.ler(FIXOS + 0x100, 0x40).hex()))
        resultado[letra] = dict(header_pointer=cabecalho, find=busca, get_data_header=variantes, load_data_info=info)
    resultado['make_id'] = [dict(eax=a, edx=b, ebx=c, result=chamar(bancada, 'MakeID', {'EAX': a, 'EDX': b, 'EBX': c})[0])
                            for a, b, c in MAKE_ID]
    resultado['instructions'], resultado['segments'] = bancada.instrucoes, bancada.execucoes
    return resultado


def abrir_z(bancada, registro=None, nome_arquivo=None):
    bancada.escrever(FIXOS, PREFIXO + b'Z\0')
    if registro is not None:
        bancada.escrever(BANCOS['A'], registro)
    if nome_arquivo is not None:
        bancada.escrever(NOME_ARQUIVO, nome_arquivo)
    return chamar(bancada, 'Open', {'EAX': FIXOS, 'EDX': BANCOS['A']})


def capturar_validacao():
    """Header validation and open failure branches, dead-code loaders and paths."""
    casos = []
    hed_ok, snd, variantes = banco_validacao()
    for nome, (hed, dados) in variantes.items():
        for herdado in (0x00, 0xa5):
            bancada = nova_bancada(arquivos_z(hed, dados))
            eax, log, parada = abrir_z(bancada, bytes([herdado]) * 28, bytes([herdado]) * NOME_ARQUIVO_BYTES)
            casos.append(dict(case=nome, inherited=herdado, routine='BanqSon_Open', eax=eax, stop=parada, log=log,
                              **estado_banco(bancada, 'A')))
    bancada = nova_bancada(arquivos_z(hed_ok, snd))
    eax, log, parada = abrir_z(bancada, struct.pack('<I', 1) + b'\xa5' * 24)
    casos.append(dict(case='already_open', inherited=0xa5, routine='BanqSon_Open', eax=eax, stop=parada, log=log,
                      **estado_banco(bancada, 'A')))
    bancada = nova_bancada(arquivos_z(hed_ok, snd), falhar_alocacao=(0,))
    eax, log, parada = abrir_z(bancada)
    casos.append(dict(case='header_allocation_failure', inherited=0, routine='BanqSon_Open', eax=eax, stop=parada,
                      log=log, **estado_banco(bancada, 'A')))
    reais = arquivos_originais()
    for nome, hed in [(f'{l}.HED', reais[PREFIXO + f'{l}.HED'.encode()]) for l in LETRAS_BANCO] + [
            ('bad_magic', variantes['bad_magic'][0])]:
        bancada = nova_bancada({PREFIXO + b'Q.HED': hed})
        handle = bancada.arquivos.abrir(PREFIXO + b'Q.HED', 0)
        bancada.escrever(FIXOS + 0x40, b'\xa5' * 4)
        bancada.escrever(BANCOS['A'], b'\xa5' * 28)
        eax, log, parada = chamar(bancada, 'ControleValiditeHeader',
                                  {'EAX': handle, 'EDX': FIXOS + 0x40, 'EBX': BANCOS['A']})
        casos.append(dict(case=nome, inherited=0xa5, routine='BanqSon_ControleValiditeHeader', eax=eax, stop=parada,
                          log=log, fixture_setup='handle opened by the fixture before the call',
                          out_hex=bancada.ler(FIXOS + 0x40, 4).hex(), record_hex=bancada.ler(BANCOS['A'], 28).hex()))
    for nome, dados in (('complete', snd), ('short_snd', snd[:1000])):
        bancada = nova_bancada(arquivos_z(hed_ok, dados))
        abrir_z(bancada)
        eax, log, parada = chamar(bancada, 'LoadAllData', {'EAX': BANCOS['A']})
        casos.append(dict(case=nome, inherited=0, routine='BanqSon_LoadAllData', eax=eax, stop=parada, log=log,
                          data_sha256=sha(bancada.ler(eax, len(snd))) if eax else None, **estado_banco(bancada, 'A')))
    bancada = nova_bancada({})
    bancada.escrever(BANCOS['A'], b'\0' * 4 + b'\xa5' * 24)
    eax, log, parada = chamar(bancada, 'LoadDataInMemory', {'EAX': BANCOS['A']})
    casos.append(dict(case='closed_bank', inherited=0xa5, routine='BanqSon_LoadDataInMemory', eax=eax, stop=parada,
                      log=log, **estado_banco(bancada, 'A')))
    caminhos = []
    for cwd in DIRETORIOS_TESTE:
        bancada = nova_bancada({}, diretorio=cwd)
        bancada.escrever(DIRETORIO_SONS, b'\xa5' * 64)
        _, log, _ = chamar(bancada, 'CreateSoundPath')
        _, log2, _ = chamar(bancada, 'SoundFile', {'EAX': NOME_LETRA['P'], 'EDX': FIXOS})
        caminhos.append(dict(cwd=cwd.decode('latin-1'), sound_directory_hex=bancada.ler(DIRETORIO_SONS, 64).hex(),
                             sound_file=bancada.cadeia(FIXOS).decode('latin-1'), log=log + log2))
    return dict(cases=casos, paths=caminhos)


def chamar_decodificador(bancada, tipo, semente, bloco, origem):
    origem_ptr, destino = 0x4800000, 0x4900000
    bancada.escrever(origem_ptr, origem)
    bancada.escrever(destino, b'\xcd' * (len(origem) * 4 + 64))
    pontos = PONTOS_M16 if tipo == 'm16' else PONTOS_S16
    eax, _, parada = chamar(bancada, tipo.upper(), {'EAX': origem_ptr, 'EDX': len(origem), 'ECX': bloco,
                                                    'EBX': destino}, argumentos=(0, 0, 0), pontos=pontos)
    return dict(decoder=tipo, seed=semente, block_align=bloco, input_bytes=len(origem), input_sha256=sha(origem),
                eax=eax, stop=parada, output_sha256=sha(bancada.ler(destino, len(origem) * 4 + 64)),
                output_window=len(origem) * 4 + 64, poison='0xcd')


def capturar_decodificador():
    """Direct M16/S16 calls and synthetic surfaces (stereo, PCM, unsupported format)."""
    bancada = nova_bancada({})
    diretos = [chamar_decodificador(bancada, tipo, semente, bloco, entrada_decodificador(tipo, semente, bloco, n))
               for tipo, semente, bloco, n in DECODIFICADOR_DIRETO]
    diretos += [chamar_decodificador(bancada, tipo, semente, bloco, dados)
                for tipo, semente, bloco, dados in entradas_saturacao()]
    hed, snd = banco_sintetico_superficies()
    superficies = []
    bancada = nova_bancada(arquivos_z(hed, snd))
    abrir_z(bancada)
    chamar(bancada, 'InitCompressedBuffer')
    cabecalho = bancada.u32(BANCOS['A'] + 0xc)
    for i in range(4):
        superficies.append(capturar_superficie(bancada, 'A', cabecalho + 48 + 16 * i, dict(synthetic=i, path='file')))
    # LoadDataInMemory after file reads: short read, block freed, flag still set with a NULL pointer.
    eax, log, parada = chamar(bancada, 'LoadDataInMemory', {'EAX': BANCOS['A']})
    apos_leitura = dict(case='load_data_in_memory_after_reads', eax=eax, stop=parada, log=log,
                        **estado_banco(bancada, 'A'))
    bancada = nova_bancada(arquivos_z(hed, snd))
    abrir_z(bancada)
    chamar(bancada, 'InitCompressedBuffer')
    chamar(bancada, 'LoadDataInMemory', {'EAX': BANCOS['A']})
    cabecalho = bancada.u32(BANCOS['A'] + 0xc)
    for i in range(4):
        superficies.append(capturar_superficie(bancada, 'A', cabecalho + 48 + 16 * i, dict(synthetic=i, path='memory')))
    return dict(direct=diretos, synthetic_bank=dict(hed_sha256=sha(hed), snd_sha256=sha(snd)),
                surfaces=superficies, memory_after_reads=apos_leitura,
                instructions=bancada.instrucoes)


def main(letras):
    saida = OWNED / 'evidencias'
    inicio = time.time()
    relatorio = dict(original_sha256=ORIGINAL_SHA256, created_before_translation=True,
                     bench='pesquisas-paralelas/audio/bancada_som.py on ferramentas/emulador.py', fixture=FIXTURE,
                     validation=capturar_validacao(), index=capturar_indice(), decoder=capturar_decodificador())
    (saida / 'captura-som-estrutura.json').write_text(json.dumps(relatorio, indent=1) + '\n')
    print('structure captures', round(time.time() - inicio, 1), 's', flush=True)
    for letra in letras:
        caso = capturar_banco(letra)
        caso.update(original_sha256=ORIGINAL_SHA256, created_before_translation=True, fixture=FIXTURE)
        (saida / f'captura-som-banco-{letra}.json').write_text(json.dumps(caso, indent=1) + '\n')
        print('bank', letra, len(caso['surfaces_from_file']), 'surfaces', caso['instructions_file'],
              'file instructions', round(time.time() - inicio, 1), 's', flush=True)


if __name__ == '__main__':
    main(sys.argv[1:] or list(LETRAS_BANCO))
