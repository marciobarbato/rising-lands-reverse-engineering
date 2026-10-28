"""Export intact original audio routines, data tables and bank identities.

Every interval runs from its original SBL symbol to the next symbol, minus
trailing zero padding. The exported bytes come from the intact executable;
the normalized analysis PE is not used here.
"""
import hashlib
import json
import struct
from ambiente_audio import ANALYSIS_SHA256, CD, IDENTIDADES, ORIGINAL_SHA256, OWNED, ROOT
from analisar import dependencias

# (group, symbol). Groups name the inventory role, not a recovered semantic.
ROTINAS = (
    ('bank', 'UseBank_FindIdInBanque'), ('bank', 'UseBank_GetDataHeader'),
    ('bank', 'BanqSon_OpenDataFile'), ('bank', 'BanqSon_CloseDataFile'),
    ('bank', 'BanqSon_ControleValiditeHeader'), ('bank', 'BanqSon_LoadHeader'),
    ('bank', 'BanqSon_FreeHeader'), ('bank', 'BanqSon_Open'),
    ('bank', 'BanqSon_FreeDataInMemory'), ('bank', 'BanqSon_Close'),
    ('bank', 'BanqSon_LoadAllData'), ('bank', 'BanqSon_LoadDataInMemory'),
    ('buffer', 'PSB_CreateMySurfaceWithSound'), ('buffer', 'DSB_CreateEmptySoundBuffer'),
    ('decode', 'imaadpcmNextStepIndex'), ('decode', 'imaadpcmSampleDecode'),
    ('decode', 'imaadpcmValidStepIndex'), ('decode', 'imaadpcmDecode4Bit_M16'),
    ('decode', 'imaadpcmDecode4Bit_S16'),
    ('decode', 'LoadSoundBuffer_LoadDataFromFileInSoundBuffer'),
    ('decode', 'LoadSoundBuffer_DecompactInSoundBuffer'),
    ('decode', 'LoadSoundBuffer_PlaceOnSample'), ('decode', 'LoadSoundBuffer_LoadCompactedData'),
    ('decode', 'LoadSoundBuffer_InitCompressedBuffer'),
    ('decode', 'LoadSoundBuffer_FreeCompressedBuffer'),
    ('decode', 'LoadSoundBuffer_LoadDataFromMemoryInSoundBuffer'),
    ('wrapper', 'CreatM'), ('wrapper', 'OpenM'), ('wrapper', 'CloseM'), ('wrapper', 'ReadM'),
    ('wrapper', 'WriteM'), ('wrapper', 'SeekM'), ('wrapper', 'OurAlloc'),
    ('wrapper', 'OurCalloc'), ('wrapper', 'OurFree'),
    ('identity', 'HndSound_LoadDataInfo'), ('identity', 'PlaySnd_CreateSoundPath'),
    ('identity', 'SoundFile'), ('identity', 'PlaySnd_MakeID'),
    ('identity', 'PlaySnd_InitSoundLib'), ('identity', 'PlaySnd_PostSound'),
    ('crt', 'memset'), ('crt', '__STOSB'), ('crt', '__STOSD'), ('crt', 'sprintf'), ('crt', '__prtf'),
)
# The sprintf character sink has no SBL symbol; it precedes sprintf inside
# the strnicmp symbol range and sprintf passes its address in ECX.
SEM_SIMBOLO = (('crt', 'sprintf_character_sink', 0x48cfa8, 0x48cfbb),)
IMPORTACOES = {0x5231c0: 'KERNEL32.GlobalAlloc', 0x5231c8: 'KERNEL32.GlobalFree',
               0x5231e8: 'KERNEL32._hread', 0x5231ec: 'KERNEL32._hwrite',
               0x5231f0: 'KERNEL32._lclose', 0x5231f4: 'KERNEL32._lcreat',
               0x5231f8: 'KERNEL32._llseek', 0x5231fc: 'KERNEL32._lopen',
               0x5232b0: 'USER32.MessageBoxA'}
TABELAS = (('ima_index_words', 0x498f6c, 32), ('ima_step_words', 0x498f8c, 178),
           ('sound_strings', 0x49537c, 0x1c2))
GLOBAIS = {'bank_A': ('0x521fc8', 28), 'bank_B': ('0x521fe4', 28), 'bank_P': ('0x522000', 28),
           'sound_directory': ('0x52201c', 256), 'bank_file_name': ('0x5221c0', 128),
           'variant_counter': ('0x5221bc', 4), 'direct_sound': ('0x522228', 4),
           'compressed_buffer': ('0x52222c', 4), 'allocation_count': ('0x522230', 4),
           'physical_count': ('0x498f60', 4), 'game_volume': ('0x498f58', 4)}
CRT_LIMITADOS = {'__prtf'}


def simbolos():
    linhas = (ROOT / 'relatorios/simbolos-originais.tsv').read_text().splitlines()[1:]
    return sorted({int(a, 16): n for a, n in (linha.split('\t') for linha in linhas)}.items())


def imagem(pe, endereco, tamanho):
    return pe.get_data(endereco - 0x400000, tamanho)


def intervalo(pe, md, inicio, proximo):
    code = imagem(pe, inicio, proximo - inicio)
    instrucoes = list(md.disasm(code, inicio))
    consumido = sum(i.size for i in instrucoes)
    if any(code[consumido:]):
        raise ValueError(f'Incomplete original disassembly at 0x{inicio:08x}')
    while instrucoes and instrucoes[-1].bytes == b'\0\0':
        instrucoes.pop()
    fim = instrucoes[-1].address + instrucoes[-1].size
    return fim, instrucoes


def exportar():
    pefile, capstone = dependencias()
    raw = (CD / 'INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest() != ORIGINAL_SHA256:
        raise ValueError('Original EXE SHA-256 mismatch')
    pe = pefile.PE(data=raw)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    tabela = simbolos()
    enderecos = {nome: endereco for endereco, nome in tabela}
    seguinte = {endereco: tabela[i + 1][0] for i, (endereco, _) in enumerate(tabela[:-1])}
    destino = OWNED / 'evidencias'
    destino.mkdir(exist_ok=True)
    linhas, intervalos = [], []
    pedidos = [(grupo, nome, enderecos[nome], seguinte[enderecos[nome]]) for grupo, nome in ROTINAS]
    for grupo, nome, inicio, proximo in sorted(pedidos + list(SEM_SIMBOLO), key=lambda item: item[2]):
        fim, instrucoes = intervalo(pe, md, inicio, proximo)
        code = imagem(pe, inicio, fim - inicio)
        intervalos.append(dict(group=grupo, name=nome, start=hex(inicio), end_exclusive=hex(fim),
                               bytes=len(code), sha256=hashlib.sha256(code).hexdigest()))
        if grupo == 'crt' and nome in CRT_LIMITADOS:
            linhas += [f'; {nome} 0x{inicio:08x}..0x{fim:08x}: Watcom CRT, hash only']
            continue
        linhas += [f'; {nome} ({grupo})'] + [
            f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in instrucoes]
    cabecalho = [f'; Intact original SHA-256 {ORIGINAL_SHA256}',
                 '; Exported by pesquisas-paralelas/audio/extrair_som.py; symbols from INSTALHD/RISING.SBL']
    (destino / 'som-rotinas.asm').write_text('\n'.join(cabecalho + linhas) + '\n')
    tabelas = []
    for nome, inicio, tamanho in TABELAS:
        dados = imagem(pe, inicio, tamanho)
        tabelas.append(dict(name=nome, start=hex(inicio), bytes=tamanho,
                            sha256=hashlib.sha256(dados).hexdigest(), hex=dados.hex()))
    iat = {hex(endereco): nome for endereco, nome in IMPORTACOES.items()}
    for imp in (i for e in pe.DIRECTORY_ENTRY_IMPORT for i in e.imports):
        if imp.address in IMPORTACOES and IMPORTACOES[imp.address].split('.', 1)[1] != imp.name.decode():
            raise ValueError(f'Import slot 0x{imp.address:08x} is {imp.name!r}')
    bancos = {nome: dict(bytes=tamanho, sha256=sha) for nome, (tamanho, sha) in IDENTIDADES.items()}
    resultado = dict(
        original_sha256=ORIGINAL_SHA256, analysis_pe_sha256=ANALYSIS_SHA256,
        analysis_note='Analysis PE identity named for cross-reference only; all bytes here are from the intact executable.',
        symbols='relatorios/simbolos-originais.tsv (original RISING.SBL)',
        intervals=intervalos, disassembly='som-rotinas.asm', tables=tabelas, globals=GLOBAIS,
        import_slots=iat, banks=bancos,
        bank_letters={'A': '0x41 -> 0x521fc8', 'B': '0x42 -> 0x521fe4', 'P': '0x50 -> 0x522000'},
        no_direct_callers_note='No rel32 CALL/JMP and no absolute 32-bit reference anywhere in the intact image.',
        no_direct_callers=['BanqSon_OpenDataFile', 'BanqSon_CloseDataFile', 'BanqSon_ControleValiditeHeader',
                           'BanqSon_LoadAllData', 'BanqSon_LoadDataInMemory', 'PlaySnd_CreateSoundPath',
                           'SoundFile', 'PlaySnd_MakeID'],
        scope='Stage 1 inventory: bank header/index/data-header readers, buffer creation and sample decoding, '
              'file/allocation wrappers, sound identity. Queue tables, emitters and DirectSound playback are later stages.')
    (destino / 'som-manifesto.json').write_text(json.dumps(resultado, indent=2) + '\n')
    return resultado


if __name__ == '__main__':
    print('Audio intervals:', len(exportar()['intervals']))
