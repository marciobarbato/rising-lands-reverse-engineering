#!/usr/bin/env python3
"""Gera relatórios reproduzíveis em português a partir do CD local, sem executá-lo."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
import zlib

from formatos import ler_cmp, ler_eta, ler_paleta
from regras import extrair_regras

RAIZ = Path(__file__).resolve().parents[1]
HASH_ESTUDADO = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
# Limites exclusivos; trechos selecionados, não uma decompilação completa.
TRECHOS = {
    'carregador_mapa': (0x46c2cf, 0x46c5e3),
    'carregador_unidades_eta': (0x46acbf, 0x46b01e),
    'carregador_danos': (0x441792, 0x44188b),
    'carregador_atributos': (0x44188b, 0x441a1b),
    'alocacao_unidades': (0x441a1b, 0x441ade),
    'carregador_cmp': (0x4186ba, 0x41877a),
    'agregador_cmp': (0x41877a, 0x4189b5),
    'entrada_render_terreno': (0x41068e, 0x41087d),
    'origem_visualizacao': (0x474b08, 0x474beb),
    'composicao_cmp': (0x45c779, 0x45c7fe),
    'leitura_arquivo': (0x458420, 0x4584a3),
    'atribuir_recurso': (0x46799c, 0x4679d0),
    'tabela_47534a': (0x47534a, 0x47539c),
    'tabela_47c24d': (0x47c24d, 0x47c2ec),
    'tabela_47bcc7': (0x47bcc7, 0x47bd3f),
    'tabela_47c04a': (0x47c04a, 0x47c0bd),
    'tabela_458b05': (0x458b05, 0x458b72),
    'descartar_bytes_eta': (0x47c30f, 0x47c359),
    'listas_jogadores_eta': (0x47c404, 0x47c4b7),
    'tabela_47ac30': (0x47ac30, 0x47ad6a),
}


def sha(dados):
    return hashlib.sha256(dados).hexdigest()


def gravar_json(caminho, valor):
    caminho.write_text(json.dumps(valor, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def dependencias():
    # Reutiliza bibliotecas já presentes, sem alterar a instalação existente.
    try:
        import pefile
        import capstone
    except ImportError:
        sys.path.insert(0, str(RAIZ.parent / 'source/python'))
        try:
            import pefile
            import capstone
        except ImportError as erro:
            raise SystemExit('Instale requirements.txt em um ambiente virtual deste repositório.') from erro
    return pefile, capstone


def analisar_pe(dados, destino):
    pefile, capstone = dependencias()
    pe = pefile.PE(data=dados)
    base = pe.OPTIONAL_HEADER.ImageBase
    imagem = pe.get_memory_mapped_image()
    importacoes = {}
    nomes_importacoes = {}
    for biblioteca in pe.DIRECTORY_ENTRY_IMPORT:
        nome = biblioteca.dll.decode('ascii')
        entradas = []
        for item in biblioteca.imports:
            simbolo = item.name.decode('ascii') if item.name else f'ordinal_{item.ordinal}'
            entradas.append(dict(nome=simbolo, endereco_iat=f'0x{item.address:08x}'))
            nomes_importacoes[item.address] = f'{nome}!{simbolo}'
        importacoes.setdefault(nome, []).extend(entradas)
    strings = {}
    for achado in re.finditer(rb'[\x20-\x7e]{4,}', imagem):
        if any(termo in achado.group().lower() for termo in (b'.cmp', b'.ini', b'.pie', b'watcom')):
            strings[base + achado.start()] = achado.group().decode('ascii')
    referencias = []
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    cs.detail = True
    cs.skipdata = True
    for secao in pe.sections:
        if not secao.Characteristics & 0x20000000:
            continue
        for ins in cs.disasm(secao.get_data(), base + secao.VirtualAddress):
            if not ins.id:
                continue
            for op in ins.operands:
                if op.type == capstone.x86.X86_OP_IMM and op.imm in strings:
                    referencias.append(dict(instrucao=f'0x{ins.address:08x}',
                                             destino=f'0x{op.imm:08x}', texto=strings[op.imm]))
    nomes = {inicio: nome for nome, (inicio, _) in TRECHOS.items()}
    for nome, (inicio, fim) in TRECHOS.items():
        linhas = [f'; {nome}: trecho estático, nomes atribuídos pela pesquisa.',
                  f'; SHA-256 RISING.EXE: {sha(dados)}',
                  '; Endereços virtuais da imagem preferencial; fim exclusivo.',
                  '; As anotações não recuperam nomes originais nem comprovam execução.']
        for ins in cs.disasm(imagem[inicio-base:fim-base], inicio):
            comentarios = []
            if ins.id:
                for op in ins.operands:
                    if op.type == capstone.x86.X86_OP_IMM:
                        valor = op.imm
                        if ins.mnemonic == 'call' and valor in nomes:
                            comentarios.append(nomes[valor])
                        elif base <= valor < base + len(imagem):
                            texto = imagem[valor-base:valor-base+120].split(b'\0')[0]
                            if len(texto) >= 4 and all(32 <= c < 127 for c in texto):
                                comentarios.append(repr(texto.decode('ascii')))
                    elif op.type == capstone.x86.X86_OP_MEM and op.mem.disp in nomes_importacoes:
                        comentarios.append(nomes_importacoes[op.mem.disp])
            linha = f'{ins.address:08x}  {ins.bytes.hex():20}  {ins.mnemonic:8} {ins.op_str}'
            linhas.append((linha + (' ; ' + '; '.join(comentarios) if comentarios else '')).rstrip())
        (destino / f'{nome}.asm').write_text('\n'.join(linhas) + '\n', encoding='utf-8')
    return imagem, base, dict(
        sha256=sha(dados), tamanho=len(dados), arquitetura='x86 de 32 bits',
        base=f'0x{base:08x}', entrada=f'0x{base + pe.OPTIONAL_HEADER.AddressOfEntryPoint:08x}',
        ferramentas=dict(pefile=pefile.__version__, capstone=capstone.__version__),
        secoes=[dict(nome=s.Name.rstrip(b'\0').decode('ascii'),
                     rva=f'0x{s.VirtualAddress:x}', tamanho_virtual=s.Misc_VirtualSize,
                     tamanho_no_arquivo=s.SizeOfRawData, offset_arquivo=s.PointerToRawData,
                     caracteristicas=f'0x{s.Characteristics:08x}') for s in pe.sections],
        importacoes=importacoes, strings_selecionadas={f'0x{k:08x}': v for k, v in strings.items()},
        referencias_candidatas=referencias,
        limite='Varredura linear pode interpretar dados como instruções; conferir os trechos contextualizados.')


def salvar_png(caminho, largura, altura, rgb):
    """PNG RGB sem dependências de imagem; filtro zero, uma linha por vez."""
    def bloco(tipo, dados):
        return struct.pack('>I', len(dados)) + tipo + dados + struct.pack('>I', zlib.crc32(tipo + dados))
    linhas = b''.join(b'\0' + rgb[y*largura*3:(y+1)*largura*3] for y in range(altura))
    caminho.write_bytes(b'\x89PNG\r\n\x1a\n' +
                       bloco(b'IHDR', struct.pack('>IIBBBBB', largura, altura, 8, 2, 0, 0, 0)) +
                       bloco(b'IDAT', zlib.compress(linhas, 9)) + bloco(b'IEND', b''))


def renderizar_terreno(mapa, quadros, paleta, caminho):
    largura, altura = mapa['largura'] * 32, mapa['altura'] * 32
    rgb = bytearray(largura * altura * 3)
    for celula, identificador in enumerate(mapa['terreno']):
        if not 1 <= identificador <= len(quadros):
            raise ValueError(f'ID de terreno inválido: {identificador}')
        quadro = quadros[identificador - 1]
        if (quadro.largura, quadro.altura) != (32, 32):
            raise ValueError('Terreno fora do formato 32 × 32')
        x, y = (celula % mapa['largura']) * 32, (celula // mapa['largura']) * 32
        for linha in range(32):
            pixels = quadro.pixels[linha*32:(linha+1)*32]
            inicio = ((y + linha) * largura + x) * 3
            rgb[inicio:inicio+96] = b''.join(paleta[p*3:p*3+3] for p in pixels)
    salvar_png(caminho, largura, altura, rgb)


def main():
    argumentos = argparse.ArgumentParser(description=__doc__)
    argumentos.add_argument('--cd', type=Path, default=RAIZ.parent / 'source/cd',
                            help='Diretório do CD já extraído (somente leitura)')
    args = argumentos.parse_args()
    cd = args.cd.resolve()
    jogo = cd / 'INSTALHD'
    saida, evidencias = RAIZ / 'relatorios', RAIZ / 'evidencias'
    dados_exe = (jogo / 'RISING.EXE').read_bytes()
    if sha(dados_exe) != HASH_ESTUDADO:
        raise SystemExit('Executável diferente da versão estudada; endereços fixos não serão aplicados.')
    saida.mkdir(exist_ok=True)
    evidencias.mkdir(exist_ok=True)
    imagem, base, executavel = analisar_pe(dados_exe, evidencias)
    gravar_json(saida / 'executavel.json', executavel)
    regras = extrair_regras(imagem, base, (jogo / 'RISING.INI').read_bytes())
    gravar_json(saida / 'unidades.json', regras)
    mapas = []
    arquivos_mapa = sorted((cd / 'WORLD').glob('*.ETA'))
    arquivos_cmp = sorted((jogo / 'GRAPHICS').glob('*.CMP'))
    if len(arquivos_mapa) != 38 or len(arquivos_cmp) != 8:
        raise SystemExit('Corpus incompleto: esperados 38 ETA e 8 CMP nesta edição.')
    for arquivo in arquivos_mapa:
        mapa = ler_eta(arquivo.read_bytes())
        resumo = {k: v for k, v in mapa.items() if k not in ('terreno', 'atributos', 'objetos', 'variantes')}
        resumo.update(arquivo=str(arquivo.relative_to(cd)), sha256=sha(arquivo.read_bytes()),
                      intervalo_ids_terreno=[min(mapa['terreno']), max(mapa['terreno'])],
                      histograma_atributos=dict(sorted(Counter(mapa['atributos']).items())),
                      conversoes_objeto_0x36=sum(v == 0x36 for v in mapa['objetos']))
        for unidade in resumo['unidades']:
            tipo = unidade['tipo']
            unidade['nome_tipo'] = regras['unidades'][tipo]['nome'] if tipo < 26 else 'TIPO NÃO IDENTIFICADO'
        mapas.append(resumo)
    gravar_json(saida / 'mapas.json', mapas)
    graficos = []
    blocos = None
    for arquivo in arquivos_cmp:
        quadros = ler_cmp(arquivo.read_bytes())
        graficos.append(dict(arquivo=str(arquivo.relative_to(cd)), quadros=len(quadros),
                             pixels_decodificados=sum(q.largura*q.altura for q in quadros),
                             sha256=sha(arquivo.read_bytes())))
        if arquivo.stem == 'BLOCS':
            blocos = quadros
    gravar_json(saida / 'graficos.json', graficos)
    paleta = ler_paleta((jogo / 'PLATGAME.PIE').read_bytes())
    referencia_paleta = (jogo / 'CHARGE.LZS').read_bytes()[12:780]
    if paleta[48:765] != referencia_paleta[48:765]:
        raise ValueError('A paleta não coincide com a referência LZS nos índices 16..254')
    renderizar_terreno(ler_eta((cd / 'WORLD/MONDE01.ETA').read_bytes()), blocos,
                      paleta, saida / 'missao01-terreno.png')
    manifesto = []
    fontes = [jogo / 'RISING.EXE', jogo / 'RISING.INI', jogo / 'PLATGAME.PIE', jogo / 'CHARGE.LZS']
    for arquivo in sorted(fontes + arquivos_mapa + arquivos_cmp):
        dados = arquivo.read_bytes()
        manifesto.append(dict(arquivo=str(arquivo.relative_to(cd)), tamanho=len(dados), sha256=sha(dados)))
    gravar_json(saida / 'fontes.json', manifesto)
    linhas = ['# Unidades recuperadas', '',
              'Extraídas de RISING.EXE e RISING.INI. Tempos em unidades internas não calibradas.', '',
              '| ID | Seção original | Nome português | Comida | Pedra | Peças | Visão | Alcance | Recrutamento |',
              '|---:|---|---|---:|---:|---:|---:|---:|---:|']
    for u in regras['unidades']:
        linhas.append(f"| {u['id']} | {u['secao_original']} | {u['nome']} | {u['custo_comida']} | "
                      f"{u['custo_pedra']} | {u['custo_pecas']} | {u['raio_visao']} | "
                      f"{u['alcance_ataque']} | {u['tempo_recrutamento']} |")
    (saida / 'UNIDADES.md').write_text('\n'.join(linhas) + '\n', encoding='utf-8')
    print(f'Concluído: {len(mapas)} mapas, {len(regras["unidades"])} tipos de unidade, '
          f'{sum(g["quadros"] for g in graficos)} quadros e {len(TRECHOS)} trechos x86.')
    print(f'Relatórios: {saida}')


if __name__ == '__main__':
    main()
