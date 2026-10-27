"""Auditoria estática reproduzível e leitura dos 38 ETA, sem executar o jogo.

Decodificação por símbolo NÃO é prova de alcançabilidade. As listas incluem
candidatos falsos em dados e registram a classificação, em vez de tratar todo
deslocamento 0x8a como pertencente a uma unidade. A varredura por byte é uma
segunda verificação das formas usuais de escrita; não resolve aliases arbitrários.
"""
import bisect
from collections import Counter
import hashlib
import json
import sys

from extrair_evidencias import HASH, PASTA, REPO, ler_imagem
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_AC_WRITE
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_REG_ESP

CAMPOS = (0x79, 0x7a, 0x8a, 0x8b)
INICIO, FIM = 0x401000, 0x493c00  # seção BEGTEXT inteira, tamanho bruto do PE
FASE_UNIDADE = {
    0x445a05: 0, 0x445ab3: 0, 0x445ad1: 0, 0x451e08: 1,
    0x452a3a: 0, 0x452af6: 1, 0x452b6c: 0, 0x4531fe: 0,
}


def auditar_codigo():
    im = ler_imagem()
    arquivo_simbolos = REPO / 'evidencias/simbolos-importados.tsv'
    bruto = arquivo_simbolos.read_bytes()
    simbolos = sorted((int(l.split('\t')[0], 16), l.split('\t')[1])
        for l in bruto.decode().splitlines()[1:] if INICIO <= int(l.split('\t')[0], 16) < FIM)
    enderecos = [a for a, _ in simbolos]
    cs = Cs(CS_ARCH_X86, CS_MODE_32)
    cs.detail, cs.skipdata = True, True
    candidatos, chamadas, ajustes, fronteiras = [], [], [], set()
    instrucoes, dados = 0, 0

    def rotulo(a):
        p = bisect.bisect_right(enderecos, a) - 1
        return simbolos[p][1] if p >= 0 else '(antes do primeiro símbolo)'

    def classificar(a):
        if 0x41b000 <= a < 0x428600:
            return 'estrutura de construção, não unidade'
        if a in (0x4479b7, 0x457337):
            return 'tabela de saltos interpretada como instrução'
        if 0x440000 <= a < 0x458000:
            return 'registro de unidade'
        return 'outro objeto ou decodificação não confirmada'

    # Reiniciar em cada símbolo reduz a perda de alinhamento causada por dados
    # intercalados. Capstone skipdata conserva as lacunas em vez de parar cedo.
    limites = sorted({INICIO, FIM, *enderecos})
    for a, z in zip(limites, limites[1:]):
        for i in cs.disasm(bytes(im[a - 0x400000:z - 0x400000]), a):
            if not i.id:
                dados += i.size
                continue
            instrucoes += 1
            fronteiras.add(i.address)
            for op in i.operands:
                if op.type != X86_OP_MEM or op.mem.base == X86_REG_ESP:
                    continue
                atingidos = [f for f in CAMPOS if op.mem.disp <= f < op.mem.disp + op.size]
                if op.access & CS_AC_WRITE and atingidos:
                    candidatos.append(dict(endereco=f'0x{i.address:08x}', simbolo=rotulo(i.address),
                        bytes=i.bytes.hex(), instrucao=f'{i.mnemonic} {i.op_str}',
                        campos=[f'0x{f:02x}' for f in atingidos],
                        classificacao=classificar(i.address)))
            if i.mnemonic == 'call' and i.operands[0].type == X86_OP_IMM:
                if i.operands[0].imm in (0x457350, 0x457b87):
                    chamadas.append(dict(endereco=f'0x{i.address:08x}', simbolo=rotulo(i.address), destino=i.op_str))
            alias = i.mnemonic == 'lea' and any(o.type == X86_OP_MEM and o.mem.disp in CAMPOS for o in i.operands)
            ajuste = (i.mnemonic in ('add', 'sub') and len(i.operands) == 2
                and i.operands[1].type == X86_OP_IMM and i.operands[1].imm in CAMPOS)
            if alias or ajuste:
                ajustes.append(dict(endereco=f'0x{i.address:08x}', simbolo=rotulo(i.address), instrucao=f'{i.mnemonic} {i.op_str}'))

    # Segunda passagem, sem confiar no alinhamento anterior. Inclui falsos
    # positivos por começar depois do prefixo 66 de um MOV de 16 bits.
    cs.skipdata = False
    por_byte = []
    for a in range(INICIO, FIM):
        k = a - 0x400000
        if im[k] not in (0x88, 0x89, 0xc6, 0xc7, 0xfe, 0xff, 0x80, 0x81, 0x83):
            continue
        for i in cs.disasm(bytes(im[k:k + 15]), a, count=1):
            if any(o.type == X86_OP_MEM and o.access & CS_AC_WRITE and o.mem.base != X86_REG_ESP
                   and o.mem.disp <= 0x8a < o.mem.disp + o.size for o in i.operands):
                por_byte.append(dict(endereco=f'0x{a:08x}', simbolo=rotulo(a),
                    instrucao=f'{i.mnemonic} {i.op_str}', fronteira_na_primeira_passagem=a in fronteiras))
    return dict(sha256_original=HASH, sha256_simbolos=hashlib.sha256(bruto).hexdigest(),
        intervalo=['0x00401000', '0x00493c00'], simbolos=len(simbolos),
        instrucoes_decodificadas=instrucoes, bytes_skipdata=dados,
        metodo='Varredura linear reiniciada por símbolo, mais candidatos por byte; sem prova geral de fluxo/alias.',
        candidatos_escrita=candidatos, candidatos_8a_por_byte=por_byte,
        ajustes_ponteiro_candidatos=ajustes, chamadas_inicializadores=chamadas,
        escritas_8a_unidade_confirmadas=[dict(endereco=f'0x{a:08x}', valor=v) for a, v in FASE_UNIDADE.items()],
        conclusao='Nenhum atribuidor direto de 2/3 à fase da unidade identificado; carregadores podem preservar valores externos.')


def auditar_corpus():
    # Reutiliza somente o leitor existente. Não duplica o formato ETA nem o
    # integra à simulação. -B no comando impede criação de __pycache__ externo.
    sys.path.insert(0, str(REPO / 'ferramentas'))
    from formatos import ler_eta
    totais = {f: Counter() for f in CAMPOS}
    arquivos, fases23 = [], []
    for p in sorted((REPO.parent / 'source/cd/WORLD').glob('*.ETA')):
        b = p.read_bytes()
        mapa = ler_eta(b)
        for u in mapa['unidades']:
            off = u['offset_registro']
            for f in CAMPOS:
                totais[f][b[off + f]] += 1
            if b[off + 0x8a] in (2, 3):
                fases23.append(dict(arquivo=p.name, indice=u['indice'], fase=b[off + 0x8a]))
        arquivos.append(dict(arquivo=p.name, sha256=hashlib.sha256(b).hexdigest(), unidades=len(mapa['unidades'])))
    return dict(arquivos=arquivos, quantidade_arquivos=len(arquivos),
        quantidade_registros=sum(a['unidades'] for a in arquivos),
        histogramas={f'0x{f:02x}': dict(sorted(c.items())) for f, c in totais.items()},
        fases_2_3=fases23, escopo='Bytes serializados no CD, antes de LoadEngin; não é captura de uma partida em execução.')


def main():
    relatorio = dict(codigo=auditar_codigo(), corpus=auditar_corpus())
    p = PASTA / 'evidencias/rastreio-campos.json'
    p.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(relatorio["codigo"]["candidatos_escrita"])} candidatos; '
          f'{relatorio["corpus"]["quantidade_registros"]} registros; {p}')


if __name__ == '__main__':
    main()
